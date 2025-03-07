import zmq
import json

class Client:
    def __init__(self, ip):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUSH)
        self.socket.connect('tcp://'+ip)

    def on_key_press(self, key):
        data = {
            "action": "press",
            "key": key
            }
        self.push(data)

    def on_key_release(self, key):
        data = {
            "action": "release",
            "key": key
            }
        self.push(data)

    def push(self, msg):
        self.socket.send_json(json.dumps(msg))
