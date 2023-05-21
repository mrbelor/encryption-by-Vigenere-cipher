import socket

main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание основного сокета
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # насторйка сокета отключение алгоритма нейгла (упаковки данных в пакеты)
main_socket.bind(("localhost", 10001)) # свой IP, Port
main_socket.setblocking(0) # без задержки, без ожиданий
main_socket.listen(5) # режиим прослушивания, количество подключений одновременно (не онлайн)