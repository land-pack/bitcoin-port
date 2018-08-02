import sys
sys.path.append("..")

import time
from lib.rpc import rpc_connection
from pprint import pprint


best = rpc_connection.getbestblockhash()

def check_if_confirm_equal_block():
    d = rpc_connection.getblock(best, 1)
    txes = d.get("tx")
    block_confirme = d.get("confirmations")
    total_cost = 0
    total_items = len(txes)
    for tx in txes:
        start = time.time()
        tx_obj = rpc_connection.getrawtransaction(tx, 1)
        end = time.time() - start
        confirme = tx_obj.get("confirmations")
        #if confirme == block_confirme:
        print("tx=%s | confirme=%s | block confirm=%s| cost time=%s | is equal=%s" % ( tx, confirme, block_confirme, end, confirme == block_confirme))
        total_cost += end
    print("Total items=%s | cost time=%s" % (total_items, total_cost))


if __name__ == '__main__':
    check_if_confirm_equal_block()
