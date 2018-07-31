from rpc import rpc_connection
from pprint import pprint

class TravelTX(object):
 
    def get_tx_detail_addr(self, addr):
        tx_hex = rpc_connection.getrawtransaction(addr)
        raw_tx = rpc_connection.decoderawtransaction(tx_hex)
        tx = raw_tx.get("txid")
        vout_list = raw_tx.get("vout")
        all_list = []
        for i in vout_list:
            value = i.get("value")
            n = i.get("n")
            scriptPubKey = i.get("scriptPubKey")
            addresses = scriptPubKey.get("addresses")
            rows = []
            for addr in addresses:
                #ret = rpc_connection.validateaddress(addr)
                row = [addr, tx, value, n]
                rows.append(row)
            all_list.append(rows)
        return all_list

if __name__ == '__main__':
    txx = TravelTX()
    addr = '0b702b90b75cb52fb5e5c10a93e16ab1b68117f7f4f9569be9e71aa005d1af58'
    a = txx.get_tx_detail_addr(addr)
    pprint(a)
