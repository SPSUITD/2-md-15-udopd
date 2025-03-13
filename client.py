import zmq
import json

class Client:
    def __init__(self, ip):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUSH)
        self.socket.connect('tcp://'+ip)

    def push(self, msg):
        self.socket.send_json(json.dumps(msg))
