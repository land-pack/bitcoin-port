import time
import zmq

def producer(work_message):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")
    # Start your result manager and workers before you start your producers
    zmq_socket.send_json(work_message)
    

if __name__ == '__main__':
    
    for num in range(10):
        work_message = { 'num' : num }
        producer(work_message)
