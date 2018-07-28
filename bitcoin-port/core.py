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

    def get_unspent(self, addr):
        """
        @param addr: A array with address, ["0xxxxxx", "0x122222"]
        """
        return self.rpc.listunspent(0, 999999, addr)

    def sign_rawtransaction(self, addr):
        fee_obj = self.rpc.estimatesmartfee(6)
        fee = fee_obj.get("feerate")

    def sendrawtransaction(self, address, pubkey):
        pass




if __name__ == '__main__':
    addr = '2NCTreR1GmHXMNSYnt2J76QZgv8PH1k4PHB'
    addr = '2MsHfXEmutS2GWPgK55JD4i1gKSFYmJgKXv'
    addr = 'n2eMqTT929pb1RDNuqEnxdaLau1rxy3efi'
    bp = BitPort(config=ConfigBasic)
    print(bp.get_amount_by_addr(addr))
    #print(bp.get_unconfirm(addr))
    print(bp.get_unspent([addr]))
