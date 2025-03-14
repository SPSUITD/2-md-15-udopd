import socket
import game
import gui_client

def main():
    IPAddr = socket.gethostbyname(socket.gethostname())

    cmd = int(input("1. Создать PvP игру на одном компьютере\n"
    "2. Создать игру в локальной сети\n"
    "3. Подключиться к игре в локальной сети\n"
    "0. Выйти\n"))

    match cmd:
        case 1:
            print("Игра на одном компе")
            game.start_game()
        case 2:
            count = int(input("Введите количество игроков в сети (2-4): "))
            count = 4 if count > 4 else count
            count = 2 if count < 2 else count
            print(f'Создана локальная компата на порте {IPAddr} для {count} игроков')
            game.start_game(IPAddr, count)
        case 3:
            ip = input("Введите ip адрес игры (формат: 192.168.0.0): ")
            if len(str(ip).split('.')) == 4:
                print(ip)
                gui_client.start_game(ip)
            else:
                print(f'Неккоректный ip {ip}')
        case _:
            print("Выход")
            
if __name__ == "__main__":
    main()