import socket
import game

def main():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    game.start_game(IPAddr, 2)

main()