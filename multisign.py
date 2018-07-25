import json
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))

#best_block_hash = rpc_connection.getbestblockhash()

#print(best_block_hash)


class MultiSign(object):
    
    def __init__(self, rpc):
        self.rpc = rpc


    def validate_address(self, addr):
        ret = self.rpc.validateaddress(addr)
        print(ret)
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

    def go(self):
        addr1 = self.rpc.getnewaddress()
        addr2 = self.rpc.getnewaddress()
        addr3 = self.rpc.getnewaddress()
        addr4 = self.rpc.getnewaddress()
        
        # validate each address
        pub_obj_addr1 = self.validate_address(addr1)
        pub_obj_addr2 = self.validate_address(addr2)
        pub_key_addr1 = pub_obj_addr1.get("pubkey")
        pub_key_addr2 = pub_obj_addr2.get("pubkey")
        # add 
        
        
        return addr1, addr2, pub_key_addr1, pub_key_addr2
    
if __name__ == '__main__':
    addr = 'tb1qffcx4mpft5lxk9clsz2du4t03elxl4qwx2hu8z'
    ms = MultiSign(rpc=rpc_connection)
    ms.validate_address(addr)
    print(ms.go())
