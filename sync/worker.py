import binascii
from decimal import Decimal
import json
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from core import DigTx

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))

class TxidConsumer(object):

    def __init__(self):
        self.dig = DigTx()


    def get_rawtransaction(self, txid):
        trans_hex = rpc_connection.getrawtransaction(txid)
        print(trans_hex)
        trans_detail = rpc_connection.decoderawtransaction(trans_hex)
        return trans_detail

    def consume(self, txid):
        d = self.get_rawtransaction(txid)
        print('=' * 100)
        pprint(d)

    def save(self):
        pass

if __name__ == '__main__':
    txid = b'a2cf338d06e491c18988511fdb5a257e2b59a162bd8c281962fad5193352e3c5'
    txid = txid.decode("utf-8")
    tc = TxidConsumer()
    print(tc.consume(txid))
