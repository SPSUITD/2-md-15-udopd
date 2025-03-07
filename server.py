import threading
import zmq
import json

class Server:
    def __init__(self, pull_ip):
        self.__data = None
        self.context = zmq.Context()
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind('tcp://'+pull_ip)
        
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            self.__data = json.loads(self.pull_socket.recv_json())

    def get_data(self):
        return self.__data
