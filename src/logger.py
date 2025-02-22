import datetime

class Logger:
    __s = "[logger]: "

    def Error(self, msg):
        self.__log("ERROR: ", msg)

    def Warning(self, msg):
        self.__log("WARNING: ", msg)

    def Message(self, msg):
        self.__log("MESSAGE: ", msg)

    def __log(self, type, msg):
        match type:
            case "WARNING: ":
                print(f"{self.__s} {"\033[33m{}".format(type)} {"\033[0m{}".format(msg)} [{datetime.datetime.now().time()}]")
            case "MESSAGE: ":
                print(f"{self.__s} {"\033[34m{}".format(type)} {"\033[0m{}".format(msg)} [{datetime.datetime.now().time()}]")
            case "ERROR: ":
                print(f"{self.__s} {"\033[31m{}".format(type)} {"\033[0m{}".format(msg)} [{datetime.datetime.now().time()}]")
                