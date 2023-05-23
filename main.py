import socket, coder, sys, time, threading
import tkinter as tk

# ОБЪЯВЛЯЕМ ШТУКИ ДЛЯ Tk ###################################
def output(text):
    text += "\n" # сообщение
    output_widget.configure(state=tk.NORMAL)  # Можно выводить
    output_widget.insert(tk.END, text) # вывод в поле
    output_widget.configure(state=tk.DISABLED)  # нельзя выводить

    
    output_widget.see(tk.END)  # Scroll to the end
    #threading.Timer(1.0, print_something).start()


def on_submit(message):
    global input_widget, ENTER_CHECK, opponent

    if ENTER_CHECK:
        ENTER_CHECK = False

    if not message:
        return False

    try:
        data = message.encode()
        opponent[0].send(data)
        opponent[2] = 0
    except:
        output(f"ОШИБКА!\nне удалось отправить сообщение \"{message}\"")
        return False

    output("you: "+message)
    input_widget.delete(0, tk.END) # удаление текста из поля ввода

    return message

# сделано для того чтобы передать input_widget.get() в on_submit() т.к. в строке input_widget.bind() предать значение нельзя
# и получить значение input_widget.get() нельзя, т.к. функция on_submit() исользуется для отправки системных сообщений
def off_submit(*args):
    message = input_widget.get()
    on_submit(message)

CONNECTION_CHECK = 'connection_checking_please_dont_answer'
ENTER_CHECK = False

# окно
root = tk.Tk()
root.title("Chat Window")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=2)
root.pack_propagate(0) # отключить изменение размера корневого виджета

# поле чата
output_widget = tk.Text(root, height=10, width=50, state=tk.DISABLED)
output_widget.grid(row=0, column=0, columnspan=4, pady=5, padx=5, sticky="nsew")

# вводить здесь
label_widget = tk.Label(root, text="Enter:")
label_widget.grid(row=1, column=0, sticky="w")



# поле ввода
input_widget = tk.Entry(root)
input_widget.bind("<Return>", off_submit)# привязать клавишу возврата
input_widget.grid(row=1, column=1, columnspan=2, sticky="we")


# ОБЪЯВЛЯЕМ ШТУКИ ДЛЯ Шифрования ###################################

coder.setting()

# ОБЪЯВЛЯЕМ ШТУКИ ДЛЯ socket ###################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # насторйка сокета отключение алгоритма нейгла (упаковки данных в пакеты)

HOST = False if coder.IP.isdigit() else True
HOST = False
opponent = None

if HOST:
    # bind the socket to the specified IP address and port number
    s.bind((coder.IP, coder.PORT))
    s.setblocking(0) # без задержки, без ожиданий
    s.listen(1)

def cycle():
    global HOST, opponent, s, ENTER_CHECK
    if not opponent:
        if HOST:
            # проверка, на подключение
            try:
                opponent_socket, opponent_ip = s.accept() # перенаправление подключившегося на новый сокет
                output('Новое подключение:'+opponent_ip)
                opponent_socket.setblocking(0)
                opponent = [opponent_socket, opponent_ip, 0]
            except:
                output("Нет подключений")
                time.sleep(3)
        else:
            # если не localhost, то подключаемся по ip
            '''
            print("s:", s)
            s.connect((coder.IP, coder.PORT)) # IP, Port
            output("Подключён к "+coder.IP +' '+ str(coder.PORT))
            opponent = [s, coder.IP, 0]
            '''
            try:
                s.connect((coder.IP, coder.PORT)) # IP, Port
                output("Подключён к "+coder.IP + str(coder.PORT))
                opponent = [s, coder.IP, 0]
            except Exception as e:
                output("Не удалось подключиться к серверу")
                output(str(e))
                output('<enter>, чтобы попробовать ещё раз\n')

                ENTER_CHECK = True
                while ENTER_CHECK:
                    pass

                output("Ожидайте . . .")

    else:
        
        try:
            data = opponent[0].recv(1024) # принятие информации
            data = data.decode() # декодирование
            output("opponent: "+data) # чат
        except:
            pass
        
        try:
            data = CONNECTION_CHECK.encode()
            opponent[0].send(data)
            opponent[2] = 0
            time.sleep(3)
        except:
            opponent[2] += 1 # если не получается отправить, + в счётчик ошибок
            if opponent[2] >= 50: # если много ошибок - отключение
                output("opponent отключился" if HOST else "отключение")
                opponent[0].close() # закрытие сокета
                opponent = None

    threading.Timer(0.5, cycle).start()

threading.Timer(1, cycle).start()
root.mainloop()
