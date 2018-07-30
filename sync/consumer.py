import time
import traceback
import zmq
import random
import binascii
from worker import TxidConsumer

def consumer():
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5557")
    
    # instance a Txid Consumer
    txid_consumer = TxidConsumer()

    while True:
        work = consumer_receiver.recv_json()
        txid = work['data']
        try:
            txid_consumer.consume(txid)
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    consumer()
