import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:98332")

while True:
    zipcode = randrange(1, 100000)
    socket.send_string("%i" % zipcode)
