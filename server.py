import zmq
import json
from src.logger import Logger

class Server:
    __data: None

    def __init__(self, pull_ip):
        self.__data = None
        self.context = zmq.Context()
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind('tcp://'+pull_ip)

    def run(self):
        while True:
            try:
                data = self.pull_socket.recv_json()
                self.__data = json.loads(data)
            except Exception as e:
                Logger().Error(e)

    def get_client_input(self):
        return self.__data
