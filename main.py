import os, socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета

sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # насторйка сокета отключение алгоритма нейгла (упаковки данных в пакеты)

try:
    sock.connect(("26.26.207.166", 10001)) # IP, Port
    print("Подключён к серверу")
except:
    print("Не удалось подключиться к серверу")
    input('press any key . . .')
    sys.exit()

# функции --------------------------------------
def pack(obj):
    if type(obj) == str:

        detect = 0 # можно писать или нет
        result = ""
        x = obj[::-1] # разворот строки

        j = 0
        if obj.find(']]') == -1  or obj.find('[[') == -1:
            for i in x:
                if i == ']':
                    detect = True

                elif i == '[':
                    detect = False

                if detect:
                    result = i + result # прибавление спереди (мы же с конца прокручиваем)
                elif result:
                    return eval('['+result)

        else:
            for i in x:
                if i == ']' and j+1<len(x) and x[j+1] == ']':
                    detect = True

                elif i == '[' and j+1<len(x) and x[j+1] == '[':
                    detect = False


                if detect:
                    result = i + result # прибавление спереди (мы же с конца прокручиваем)
                elif result:
                    return eval('[['+result)
                    
                j += 1
        
        return None

    elif  type(obj) == list:
        obj = str(obj)
        return obj
    else:
        return None # <- так правильнее


def path(text):
    path_to_file = os.path.abspath(__file__)
    filename = os.path.basename(path_to_file)
    
    return path_to_file[:-len(filename)] + text



humans = [] # подключённые игроки

