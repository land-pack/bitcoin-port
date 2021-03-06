import json
import binascii
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import *
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))

#print(best_block_hash)

class MultiSign(object):
    
    def __init__(self, rpc):
        self.rpc = rpc


    def validate_address(self, addr):
        ret = self.rpc.validateaddress(addr)
        return ret
    
    def pubkey(self):
        pass


    def set_addr(self, addr_1, addr_2, addr_3, addr_4):
        self.addr_1 = addr_1
        self.addr_2 = addr_2
        self.addr_3 = addr_3
        self.addr_4 = addr_4


    def create_multisig(self, nrequired, keys):
        """
        Deprecated this <createmultisig>

        @param nrequired: numeric
        @param keys: string A json array of hex-encoded public keys
        
        @return {"address":"multi_sign_address", "redeemScript":"script"}
        """
        return self.rpc.createmultisig(nrequired, keys)

    def add_multisig_address(self, nrequired, keys):
        return self.rpc.addmultisigaddress(nrequired, keys)
    
    def dumpprivkey(self, addr):
        return self.rpc.dumpprivkey(addr)
    
    def send_address(self, addr, amount):
        return self.rpc.sendtoaddress(addr, amount)

    def get_rawtransaction(self, txid, flag=1):
        return self.rpc.getrawtransaction(txid, flag)

    def create_raw(self, txid, vout, dest_addr, amount):
        pass

    def go(self):
        #total_amount = self.rpc.getbalance()
        first_unspent = self.rpc.listunspent(0)
        print(first_unspent)
        x_first_unspent = first_unspent[-1] # get laste one
        total_amount = x_first_unspent.get("amount")
        print(total_amount)
        #utxo_vout = x_first_unspent.get("vout") or 0
        utxo_vout = 0
        print("utxo =%s" % utxo_vout)
        addr1 = self.rpc.getnewaddress()
        addr2 = self.rpc.getnewaddress()
        addr3 = self.rpc.getnewaddress()
        addr4 = self.rpc.getnewaddress() # destination address which we will send to 
        raw_change_address = self.rpc.getrawchangeaddress()
        fee_obj = self.rpc.estimatesmartfee(6)
        fee = fee_obj.get("feerate")
        #fee = Decimal(0.0001)
        
        #send_amount = Decimal(0.1)

        #change_amount = total_amount - send_amount - fee

        send_amount = total_amount / 2
        change_amount = total_amount / 2 -  fee
        print("total_amount=%s | send_amount=%s | change_amount=%s | fee=%s" % (total_amount, send_amount, change_amount, fee))
        
        if change_amount < 0.00001:
            print(change_amount)
            raise Exception("Insufficient funds")
        change_amount = "%.8f" % change_amount
        send_amount = "%0.8f" % send_amount
        # ======

        data = "@landpack"
        if len(data) > 75:
            print("Data length is {}".format(len(data)))
            raise Exception("Too much data, use OP_PUSHDATA1 instead")
        
        hex_format_data = binascii.hexlify(data)


        # validate each address
        #pub_obj_addr1 = self.validate_address(addr1)
        #pub_obj_addr2 = self.validate_address(addr2)
        #pub_key_addr1 = pub_obj_addr1.get("pubkey")
        #pub_key_addr2 = pub_obj_addr2.get("pubkey")
        pub_obj_addr3 = self.validate_address(addr3)
        pub_key_addr3 = pub_obj_addr3.get("pubkey")
        # dump prive key ..
        priv_addr1 = self.dumpprivkey(addr1)
        priv_addr2 = self.dumpprivkey(addr2)
        priv_addr3 = self.dumpprivkey(addr3)
        # add multi sign address
        ret = self.add_multisig_address(2, [addr1, addr2, pub_key_addr3])
        print("==" * 10)
        print(ret)
        addr5 = ret.get("address") # Do not store into the wallet if you don't call addmultisin ...
        redeemScript = ret.get("redeemScript")
        #
        txid = self.send_address(addr5, send_amount)
        # check the transaction by txid
        ret = self.get_rawtransaction(txid, 1)
        vout_obj = ret.get("vout")
        scriptPubKey_0 = vout_obj[0].get("scriptPubKey")
        scriptPubKey_1 = vout_obj[0].get("scriptPubKey")
        script_pub_key_0 = scriptPubKey_0.get("hex")
        script_pub_key_1 = scriptPubKey_1.get("hex")
        # create a raw transaction
        ret_hash = self.rpc.createrawtransaction([{"txid": txid, "vout": utxo_vout}], {"data":hex_format_data, addr4: send_amount, raw_change_address: change_amount})
        # sign transaction
        sign_raw_transaction = self.rpc.signrawtransaction(ret_hash, [{"txid":txid, "vout":utxo_vout, "redeemScript": redeemScript, "scriptPubKey": script_pub_key_1, "amount": total_amount}],[ priv_addr1])

        # ..
        party_hex = sign_raw_transaction.get("hex")
        sign_party_transaction = self.rpc.signrawtransaction(party_hex, [{"txid":txid, "vout":utxo_vout, "redeemScript": redeemScript, "scriptPubKey": script_pub_key_1, "amount": total_amount}],[ priv_addr3])
        # send to brodcas
        last_hex = sign_party_transaction.get("hex")
        print(sign_party_transaction)
        ret = self.rpc.sendrawtransaction(last_hex)


        return ret
    
if __name__ == '__main__':
    addr = 'tb1qffcx4mpft5lxk9clsz2du4t03elxl4qwx2hu8z'
    ms = MultiSign(rpc=rpc_connection)
    ms.validate_address(addr)
    print(ms.go())
