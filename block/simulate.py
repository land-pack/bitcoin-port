import time
import zmq

context = zmq.Context()
zmq_socket = context.socket(zmq.PUSH)
zmq_socket.bind("tcp://127.0.0.1:55551")

def producer():

    # Start your result manager and workers before you start your producers
    work_message = { 'data' : '00000000000000087ddf2cf4453b96ecc9e2e405d0d6cd1245f14ae39162ddb4'}
    zmq_socket.send_json(work_message)

if __name__ == '__main__':
    producer()
