from rpc import rpc_connection
from pprint import pprint

class DigTX(object):
 

    def mark_as_spent(self, vin_list):
        """
        UPDATE t_tx
        SET spent=1
        WHERE f_txid=%s
        """
        spent_txid = [ i.get("txid") for i in vin_list]
        return spent_txid   


    def dig(self, txid):
        tx_hex = rpc_connection.getrawtransaction(txid)
        raw_tx = rpc_connection.decoderawtransaction(tx_hex)
        tx = raw_tx.get("txid")
        vout_list = raw_tx.get("vout")
        
        vin_list = raw_tx.get("vin")
        spent_txid = self.mark_as_spent(vin_list)
        
        all_list = []
        for i in vout_list:
            value = i.get("value")
            n = i.get("n")
            scriptPubKey = i.get("scriptPubKey")
            addresses = scriptPubKey.get("addresses") or []
            rows = []
            for addr in addresses:
                row = [addr, tx, value, n]
                rows.append(row)
            if rows:
                all_list.append(rows)
        return {
            "spent": spent_txid,
            "unspent": all_list
        }

if __name__ == '__main__':
    txx = DigTX()
    #addr = '0b702b90b75cb52fb5e5c10a93e16ab1b68117f7f4f9569be9e71aa005d1af58'
    tx1 = '0b702b90b75cb52fb5e5c10a93e16ab1b68117f7f4f9569be9e71aa005d1af58'
    tx2 = '017a6025b93ebfd72b1194f9e795885cf330a6305d818108ab7a2f0fc25cb2f3'
    a1 = txx.dig(tx1)
    a2 = txx.dig(tx2)
    pprint(a1)
    pprint(a2)
