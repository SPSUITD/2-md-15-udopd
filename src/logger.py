import datetime
import sys
import os

V = "\033[35m"
W = "\033[0m"
R = "\033[31m ERROR:"
B = "\033[34m MESSAGE:"
Y = "\033[33m WARNING:"

class Logger:
    __s = "[logger]:"

    def Error(self, msg):
        print(f"{self.__s}{R}{V} {msg[0]} {W} [{datetime.datetime.now().time()}]:")
        print(f"           File {V}\"{os.path.abspath(sys.argv[0])}\", {W}line {V}{msg[2]}, {W}in {V}{msg[1]}{W}")
        print(f"           {msg[3]}")
        sys.exit()

    def Warning(self, msg):
            print(f"{self.__s}{Y}{W} {msg} [{datetime.datetime.now().time()}]")

    def Message(self, msg):
            print(f"{self.__s}{B}{W} {msg}  [{datetime.datetime.now().time()}]")