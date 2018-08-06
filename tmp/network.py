import sys
import zmq

# Socket to talk to server

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, '')
print("Collecting updates from weather server ...")
socket.connect("tcp://192.168.1.86:28332")
#socket.connect("tcp://127.0.0.1:98332")

# Subscribe

while True:
    s = socket.recv_string()
    #m = socket.recv_multipart()
    print(s)
    #print(m)
    d = s.decode()
    print(d)
