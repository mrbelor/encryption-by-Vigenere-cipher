import socket, coder, sys, time

'''
from coder import setting
setting()
from coder import *
'''
coder.setting()

#print(coder.KEY)

# specify the IP address and port number to use
#coder.IP
#coder.PORT

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # насторйка сокета отключение алгоритма нейгла (упаковки данных в пакеты)

HOST = False if coder.IP.isdigit() else True
HOST = False
opponent = None

if HOST:
    # bind the socket to the specified IP address and port number
    s.bind((coder.IP, coder.PORT))

    s.setblocking(0) # без задержки, без ожиданий

    # listen for incoming connections
    s.listen(1)

while True:

    if not opponent:
        if HOST:
            # проверка, на подключение
            try:
                opponent_socket, opponent_ip = s.accept() # перенаправление подключившегося на новый сокет
                print("Новое подключение:", opponent_ip)
                opponent_socket.setblocking(0)
                opponent = [opponent_socket, opponent_ip, 0]
            except:
                print("Нет подключений")
                time.sleep(3)
        else:
            # если не localhost, то подключаемся по ip
            try:
                s.connect((coder.IP, coder.PORT)) # IP, Port
                print("Подключён к", coder.IP, coder.PORT)
                opponent = [s, coder.IP, 0]
            except Exception as e:
                print("Не удалось подключиться к серверу")
                print("Ошибка:\n"+ str(e))
                input('Попробовать ещё раз')

    else:
        
        try:
            data = opponent[0].recv(1024) # принятие информации
            data = data.decode() # декодирование
            print("opponent:", data) # логи
        except:
            pass
        
        try:
            data = 'message '+str(opponent[2])
            print("you:", data) # логи
            data = data.encode()
            opponent[0].send(data)
            opponent[2] = 0
            time.sleep(3)
        except:
            opponent[2] += 1 # если не получается отправить, + в счётчик ошибок
            if opponent[2] >= 5: # если много ошибок - отключение
                print(f"{opponent[1]}\nopponent отключился")
                opponent[0].close() # закрытие сокета
                opponent = None
