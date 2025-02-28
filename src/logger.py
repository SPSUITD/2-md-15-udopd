import datetime
import sys
import os

V = "\033[35m"
W = "\033[0m"
R = "\033[31m ERROR:"
B = "\033[34m MESSAGE:"
Y = "\033[33m WARNING:"

output = None

class Logger:
    __s = "[logger]:"

    def __init__(self):
        global output
        output = open("log.txt", "w")
        self.Message("game start. logger init")

    def Error(self, msg):
        global output
        if output is not None:
            output.write((f"{self.__s} {msg[0]} [{datetime.datetime.now().time()}]:\n"))
            output.write(f"           File \"{os.path.abspath(sys.argv[0])}\", line {msg[2]}, in {msg[1]}\n")
            sys.exit()
        else:
            print((f"{self.__s}{R}{V} {msg[0]} {W} [{datetime.datetime.now().time()}]:"))
            print(f"           File {V}\"{os.path.abspath(sys.argv[0])}\", {W}line {V}{msg[2]}, {W}in {V}{msg[1]}{W}")
            sys.exit()

    def Warning(self, msg):
        global output
        if output is not None:
            output.write(f"{self.__s} {msg} [{datetime.datetime.now().time()}]\n")
        else:
            print(f"{self.__s}{Y}{W} {msg} [{datetime.datetime.now().time()}]")

    def Message(self, msg):
        global output
        if output is not None:
            output.write(f"{self.__s} {msg}  [{datetime.datetime.now().time()}]\n")
        else:
            print(f"{self.__s}{B}{W} {msg}  [{datetime.datetime.now().time()}]")