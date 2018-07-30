import time
import zmq
import random
import binascii
from worker import get_rawtransaction
from pprint import pprint

def consumer():
    consumer_id = random.randrange(1,10005)
    print("I am consumer #{}".format(consumer_id))
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5557")
    
    while True:
        work = consumer_receiver.recv_json()
        txid = work['data']
        #txid = binascii.hexlify(data)
        #txid = txid.decode("utf-8")
        d = get_rawtransaction(txid)
        pprint(d)


consumer()
