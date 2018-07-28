import binascii
from decimal import Decimal
import json
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))


first_unspent = rpc_connection.listunspent(0)[-1]

print(first_unspent)

address = first_unspent.get("address")
scriptPubKey = first_unspent.get("scriptPubKey")
redeemScript = first_unspent.get("redeemScript")
txid = first_unspent.get("txid")
vout = first_unspent.get("vout")

print(txid)
print(vout)

first_unspent_amount = Decimal(first_unspent.get("amount"))

print(first_unspent_amount)
raw_change_address = rpc_connection.getrawchangeaddress()
new_bitcoin_address = rpc_connection.getnewaddress()

print(raw_change_address)
print(new_bitcoin_address)

fee_obj = rpc_connection.estimatesmartfee(6)
fee = fee_obj.get("feerate")

print(fee)


send_amount = first_unspent_amount / 2
change_amount = first_unspent_amount / 2 -  fee

if change_amount < 0.00001:
    print(change_amount)
    raise Exception("Insufficient funds")

change_amount_string = "%.8f" % change_amount
send_amount_string = "%0.8f" % send_amount

data = "@rusticbison"

if len(data) > 75:
    print("Data length is {}".format(len(data)))
    raise Exception("Too much data, use OP_PUSHDATA1 instead")

hex_format_data = binascii.hexlify(data)

print(hex_format_data)

hexstring = rpc_connection.createrawtransaction(
    [{"txid": txid, "vout": vout}], {"data":hex_format_data, new_bitcoin_address: send_amount_string, raw_change_address: change_amount_string})


print("=" * 20)
print(hexstring)
print("-" * 20)

print("address ==>%s" % address)
privkey = rpc_connection.dumpprivkey(address)
print("/" * 20)

sign_raw_transaction = rpc_connection.signrawtransaction(hexstring,[{"txid":txid, "vout":vout, "redeemScript": redeemScript, "scriptPubKey": scriptPubKey, "amount": first_unspent_amount }], [privkey])
print(sign_raw_transaction)
print("+" * 20)

raw_hash = sign_raw_transaction.get("hex")

ret = rpc_connection.sendrawtransaction(raw_hash)
print(ret)
