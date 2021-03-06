import binascii
from decimal import Decimal
import json
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

def submit_raw(rpc_user, rpc_password, rpc_host, send_addr=None, recv_addr=None, send_amount=None):



    rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))
    # ...
    #rpc_connection.walletpassphrase("openos", 10)
    # validate address
    ret = rpc_connection.validateaddress(recv_addr) if recv_addr else {}

    # ...

    first_unspent = rpc_connection.listunspent()[0]
    print(first_unspent)
    
    
    address = first_unspent.get("address")
    scriptPubKey = first_unspent.get("scriptPubKey")
    redeemScript = first_unspent.get("redeemScript")
    txid = first_unspent.get("txid")
    vout = first_unspent.get("vout")
    
    #first_unspent_amount = Decimal(first_unspent.get("amount"))
    #username = rpc_connection.getaccountaddress(send_addr)
    #print(username) 
    username = 'frank'
    first_unspent_amount = Decimal(rpc_connection.getbalance(username))

    raw_change_address = rpc_connection.getrawchangeaddress()
    new_bitcoin_address = recv_addr if recv_addr else  rpc_connection.getnewaddress()
    
    print("raw_change_address [{}]".format(raw_change_address))
    
    fee_obj = rpc_connection.estimatesmartfee(6)
    fee = fee_obj.get("feerate")
    
    
    # check 
    if send_amount:
        print(first_unspent_amount, fee, send_amount)
        change_amount = first_unspent_amount - fee - send_amount 
    else:
        send_amount = first_unspent_amount / 2
        change_amount = first_unspent_amount / 2 -  fee
    
    if change_amount < 0.00001:
        print(change_amount)
        raise Exception("Insufficient funds")
    
    change_amount_string = "%.8f" % change_amount
    send_amount_string = "%0.8f" % send_amount
    
    data = "@landpack"
    if len(data) > 75:
        print("Data length is {}".format(len(data)))
        raise Exception("Too much data, use OP_PUSHDATA1 instead")
    
    hex_format_data = binascii.hexlify(data)
    
    hexstring = rpc_connection.createrawtransaction(
        [{"txid": txid, "vout": vout}], {"data":hex_format_data, new_bitcoin_address: send_amount_string, raw_change_address: change_amount_string})
    privkey = rpc_connection.dumpprivkey(address)
    
    sign_raw_transaction = rpc_connection.signrawtransaction(hexstring,[{"txid":txid, "vout":vout, "redeemScript": redeemScript, "scriptPubKey": scriptPubKey, "amount": first_unspent_amount }], [privkey])
    raw_hash = sign_raw_transaction.get("hex")
    ret = rpc_connection.sendrawtransaction(raw_hash)
    return ret

if __name__ == '__main__':
    # https://test-insight.bitpay.com/tx/8a73f907a1b44dc2ba00e4a9e0dacb57b745f5cdbd336541be71dca8971c9a93
    #ret = submit_raw(rpc_user, rpc_password, rpc_host)
    rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))
    send_addr = rpc_connection.getnewaddress()
    recv_addr = rpc_connection.getnewaddress()
    ret = submit_raw(rpc_user, rpc_password, rpc_host, send_addr=send_addr, recv_addr=recv_addr)
    print(ret)
