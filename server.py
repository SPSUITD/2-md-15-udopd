import threading
import zmq
import json
import time

class Server:
    def __init__(self, pull_ip, delta_time = 0):
        self.delta_time = delta_time
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
