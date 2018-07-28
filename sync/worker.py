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


def get_rawtransaction(txid):
    d = rpc_connection.getrawtransaction(txid)
    p = rpc_connection.decoderawtransaction(d)
    pprint(p)

if __name__ == '__main__':
    txid = b'684e9534d14a3edb22546115519d8029842ef76c99b24e9f59735f719867a8c7'
    txid = txid.decode("utf-8")
    print(get_rawtransaction(txid))