import binascii
import json
from decimal import Decimal
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from config import ConfigBasic

class BitPort(object):

    def __init__(self, config=None):
        self.conf = ConfigBasic()
        # pass
        self.rpc = AuthServiceProxy("http://{}:{}@{}".format(
        self.conf.rpc_user, self.conf.rpc_password, self.conf.rpc_host))

    def get_amount_by_addr(self, addr):
        return self.rpc.getreceivedbyaddress(addr)

    def get_unconfirm(self, addr):
        return self.rpc.getunconfirmedbalance(addr)

if __name__ == '__main__':
    addr = '2NCTreR1GmHXMNSYnt2J76QZgv8PH1k4PHB'
    addr = '2MsHfXEmutS2GWPgK55JD4i1gKSFYmJgKXv'
    bp = BitPort(config=ConfigBasic)
    print(bp.get_amount_by_addr(addr))
    #print(bp.get_unconfirm(addr))
