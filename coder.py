import os
KEY = None
IP = None
PORT = None

def path(text):
	path_to_file = os.path.abspath(__file__)
	filename = os.path.basename(path_to_file)
	return path_to_file[:-len(filename)] + text

def setting():
	global KEY, IP, PORT
	# создание файла настроек при отсутствии
	if not os.path.isfile(path("settings.txt")):
		with open(path("settings.txt"), "w", encoding="utf-8") as file:
			file.write("key:defaultkey\nip:localhost\nport:10001")

	# чтиение и проверка настроек
	with open(path("settings.txt"), "r") as file:
		lines = file.readlines() # считывание всех строк в файле
		#lines[0] = lines[0][:-1] # удаление \n

		if lines[0][:4] != "key:":
			lines[0] = 'key:defaultkey\n'
			KEY = 'defaultkey'
		else:
			KEY = lines[0][4:-1]
			KEY = KEY.lower()

		if lines[1][:3] != "ip:":
			lines[1] = 'ip:localhost'
			IP = 'localhost'
		else:
			IP = lines[1][3:-1]
			IP = IP.lower()

		if lines[2][:5] != "port:":
			lines[2] = 'port:10001'
			PORT = 10001
		else:
			try:
				PORT = int(lines[2][5:])
			except:
				print('в порте есть буквы!')

	# перезапись настроек
	with open(path("settings.txt"), "w") as rfile:
		rfile.writelines(lines)

	print("KEY:",KEY)
	print("IP:",IP)

def visener_square(alfabet):
	# формирование квадрата виженера
	square = {}
	alfabet_copy = alfabet.copy()
	for j in alfabet:

		square[j] = {}
		for i in range(0, len(alfabet)):
			square[j][alfabet[i]] = alfabet_copy[i]

		alfabet_copy.append(alfabet_copy.pop(0))
	return square

def coding(inp, square, mode = 'cript'):
	global KEY
	inp = inp.lower()
	length = len(inp)

	if len(inp) > len(KEY):
		# Create key_now variable
		key_now = KEY * (length // len(KEY)) + KEY[:length % len(KEY)]
	else:
		key_now = KEY[:len(inp)]
	
	if mode == 'cript':
		# шифрование текста
		out = ''
		for i in range(0, length):
			if key_now[i] in square and inp[i] in square:
				out += square[key_now[i]][inp[i]]
			else:
				out += '~'
		return out
	elif mode == 'encript':
		out = ''
		for i in range(0, length):
			if key_now[i] in square and inp[i] in square:
				x = next(key for key, value in square[key_now[i]].items() if value == inp[i])
				out += x
			else:
				out += '~'
		return out


if __name__ == '__main__':
	alfabet_str = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя!?,. abcdefghijklmnopqrstuvwxyz1234567890'
	alfabet = list(alfabet_str)
	alfabet_small = ["а","б","в","г","д"]

	square = visener_square(alfabet)

	setting()

	print("'~' - означает недопустимый символ, (отсутствующий в алфавите)")

	while True:
		x = input(">>> ")

		y = input("1) зашифровать\n2) расшифровать\n>")

		if y == '1':
			print(coding(x, square, mode = 'cript'))
		elif y == '2':
			print(coding(x, square, mode = 'encript'))
		else:
			print('нужно было ввести 1 или 2')
