import numpy as np

alpha = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.!?"
              "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя ")
KEY_login = "stockfish"


# Подготовка ключа
def key_verification(key):
    global alpha
    try:
        digit_key = list(key)
        index = 0
        for i in digit_key:
            digit_key[index] = alpha.index(i)
            index += 1
        det_key = np.array(digit_key)
        det_key = det_key.reshape(3, 3)
        if len(digit_key) != 9 or round(np.linalg.det(det_key)) == 0:
            return 0
        return digit_key
    except:
        return 0


# Расширенный алгоритма Евклида
def gcd_extended(num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        div, x, y = gcd_extended(num2 % num1, num1)
    return (div, y - (num2 // num1) * x, x)


# Преобразование текста в цифры
def convert_text_to_digits(text):
    global alpha
    try:
        if len(text) == 0:
            return 0
        array_text = []
        digit_text = list(text)
        index = 0
        for i in digit_text:
            digit_text[index] = alpha.index(i)
            index += 1
        while len(digit_text) % 3 != 0:
            digit_text.append(alpha.index('_'))
        for i in range(0, len(digit_text) - 2, 3):
            array_text.append(digit_text[i:i + 3])
        return array_text
    except:
        return 0


# Преобразование цифр в текст
def convert_digits_to_text(coded_text):
    global alpha
    index = 0
    for i in coded_text:
        coded_text[index] = alpha[i]
        index += 1
    return ''.join(coded_text)


# Кодирование текста
def encode(data, key_digit):
    global alpha
    key_digit = np.array(key_digit)
    key_digit = key_digit.reshape(3, 3)
    array_text = np.array(data)
    encoded_text = np.ravel(np.dot(array_text, key_digit) % len(alpha))
    encoded_text = encoded_text.tolist()
    encoded_text = convert_digits_to_text(encoded_text)
    return encoded_text


# Проверка входа
def check_login(username, password, action):
    global KEY_login
    if len(username) <= 1 or len(username) > 50 or len(password) < 8 or len(password) > 30:
        return False
    if ' ' in password:
        return False
    key = key_verification(KEY_login)
    data = convert_text_to_digits(username+password)
    if key == 0 or data == 0:
        return False
    try:
        encoded_data = encode(data, key)
        with open('login.txt', 'r+', encoding='utf8') as login_file:
            for line in login_file:
                if encoded_data in line and action == 'Вход':
                    return True
                if encoded_data in line and action == 'Регистрация':
                    return False
            if action == 'Вход':
                return False
            new_login = encoded_data + "\n"
            login_file.write(new_login)
            return True
    except:
        return False