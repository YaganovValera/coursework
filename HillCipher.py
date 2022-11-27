import numpy as np
import sqlite3

alpha_text = tuple("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ.,!? ")
alpha_login = tuple("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.,!?")
KEY = "АЛЬПИНИЗМ"

# Выбор алфавита
def alpha_definition(alpha):
    if alpha == 'text':
        return alpha_text
    return alpha_login

# Проверка ключа
def key_verification(key, alpha):
    try:
        alpha = alpha_definition(alpha)
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
def convert_text_to_digits(text, alpha):
    use_alpha = alpha_definition(alpha)
    try:
        if len(text) == 0:
            return 0
        array_text = []
        digit_text = list(text)
        index = 0
        for i in digit_text:
            digit_text[index] = use_alpha.index(i)
            index += 1
        while len(digit_text) % 3 != 0:
            if use_alpha == alpha_text:
                digit_text.append(use_alpha.index(' '))
            else:
                digit_text.append(use_alpha.index('_'))
        for i in range(0, len(digit_text) - 2, 3):
            array_text.append(digit_text[i:i + 3])
        return array_text
    except:
        return 0

# Преобразование цифр в текст
def convert_digits_to_text(coded_text, alpha):
    index = 0
    for i in coded_text:
        coded_text[index] = alpha[i]
        index += 1
    return ''.join(coded_text)

digit_KEY = key_verification(KEY, 'text')

# Кодирование текста
def encode(text, key_digit, alpha):
    alpha = alpha_definition(alpha)
    key_text = str(key_digit)
    key_digit = np.array(key_digit)
    key_digit = key_digit.reshape(3, 3)
    array_text = np.array(text)
    encoded_text = np.ravel(np.dot(array_text, key_digit) % len(alpha))
    encoded_text = encoded_text.tolist()
    encoded_text = convert_digits_to_text(encoded_text, alpha)
    if alpha == alpha_login:
        return encoded_text
    else:
        key_text = key_text.replace("]", "")
        key_text = key_text.replace("[", "")
        key_text = key_text.split(', ')
        key_text = '-'.join(key_text)
        with open('text.txt', 'r+', encoding='utf8') as text_file:
            for line in text_file:
                if key_text in line:
                    return False
            text_file.write("\n" + key_text + " " + encoded_text)
            return key_text

# Получение закодированного текста
def get_coding_text(key_file):
    with open('text.txt', 'r', encoding='utf8') as text_file:
        len_key = len(key_file)
        for line in text_file:
            if key_file in line:
                text = line[(len_key+1):]
                return text
        return False

# Декодирование текста
def decode(text, key, alpha):

    index = 0
    for i in key:
        key[index] = int(i)
        index += 1
    key = np.array(key)
    key = key.reshape(3, 3)

    alpha = alpha_definition(alpha)
    array_text = np.array(text)
    det_key = round(np.linalg.det(key))
    euclid_algorithm = gcd_extended(det_key, len(alpha))
    if det_key < 0 and euclid_algorithm[1] < 0:
        reverse_det = - euclid_algorithm[1]
    elif det_key > 0 and euclid_algorithm[1] < 0:
        reverse_det = euclid_algorithm[1] + len(alpha)
    else:
        reverse_det = euclid_algorithm[1]
    alg_compl = key.copy()
    for x in range(3):
        for y in range(3):
            current_array = key.copy()
            current_array = np.delete(current_array, x, axis=0)
            current_array = np.delete(current_array, y, axis=1)
            alg_compl[x, y] = round(np.linalg.det(current_array)) % len(alpha)
            alg_compl[x, y] = (alg_compl[x, y] * reverse_det) % len(alpha) * (-1) ** (x + y)
    alg_compl = np.transpose(alg_compl)
    for x in range(3):
        for y in range(3):
            if alg_compl[x, y] < 0:
                alg_compl[x, y] += len(alpha)
    encoded_text = np.ravel(np.dot(array_text, alg_compl) % len(alpha))
    encoded_text = convert_digits_to_text(encoded_text.tolist(), alpha)
    return encoded_text

# Проверка регистрации
def check_login(username, password, key):
    if len(username) <= 1 or len(username) > 50 or len(password) < 8 or len(password) > 30:
        return False
    key = key_verification(key, 'login')
    password = convert_text_to_digits(password, 'login')
    if key == 0 or password == 0:
        return False
    try:
        find_login = False
        password = encode(password, key, 'login')
        with open('login.txt', 'r', encoding='utf8') as login_file:
            for line in login_file:
                if (username + " " + password) in line:
                    find_login = True
            if find_login:
                return True
            return False
    except:
        return False

# Проверка входа
def check_registr(username, password, key):
    if (len(username) <= 1 or len(username) > 50) and (len(password) < 8 or len(password) > 30):
        return False
    try:
        flag_login = False
        key = key_verification(key, 'login')
        password = convert_text_to_digits(password, 'login')
        if key == 0 or password == 0:
            return False
        password = encode(password, key, 'login')
        with open('login.txt', 'r+', encoding='utf8') as login_file:
            for line in login_file:
                if (username in line) or (password in line):
                    flag_login = True
                    break
            if flag_login:
                return False
            new_login = "\n" + username + " " + password
            login_file.write(new_login)
            return True
    except:
        return False


