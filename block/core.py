import sys
sys.path.append("..")
import traceback
import zmq
import time
from lib.rpc import rpc_connection
from pprint import pprint




def check_if_confirm_equal_block(block_id):
    """
    Call when a block notify has been received from the zeroMQ.
    """
    d = rpc_connection.getblock(block_id, 1)
    txes = d.get("tx")
    block_confirme = d.get("confirmations")
    total_cost = 0
    total_items = len(txes)
    for tx in txes:
        start = time.time()
        tx_obj = rpc_connection.getrawtransaction(tx, 1)
        end = time.time() - start
        confirme = tx_obj.get("confirmations")
        print("tx=%s | confirme=%s | block confirm=%s| cost time=%s | is equal=%s" % ( tx, confirme, block_confirme, end, confirme == block_confirme))
        total_cost += end
    print("Total items=%s | cost time=%s" % (total_items, total_cost))


def main():

    context = zmq.Context()
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:55551")

    while True:
        data = consumer_receiver.recv_json()
        try:
            block_id = data.get("data")
            check_if_confirm_equal_block(block_id)
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    #best_block_id = rpc_connection.getbestblockhash()
    #check_if_confirm_equal_block(best_block_id)

    main()
