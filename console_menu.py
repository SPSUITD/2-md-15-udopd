import socket
import game
import gui_client

def main():
    my_ip = socket.gethostbyname(socket.gethostname())

    cmd = int(input("B0mberm@n!\n"
    "1. Создать PvP игру на одном компьютере\n"
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
            print(f'Создана локальная комната на порте {my_ip} для {count} игроков')
            game.start_game(my_ip, count)
        case 3:
            print("Введите ip-адрес игры (формат: 192.168.0.0:0000)")
            host_ip = input("(ip и доступные порты вы можете узнать в окне хоста игры): ")
            if len(str(host_ip).split('.')) == 4 and ":" in host_ip:
                print(host_ip)
                gui_client.start_game(host_ip, my_ip)
            else:
                print(f'Неккоректный ip: {host_ip} (требуемый формат: 192.168.0.0:0000)')
        case _:
            print("Выход")
            
if __name__ == "__main__":
    main()