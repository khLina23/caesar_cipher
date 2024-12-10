import random

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def cipher(text, key, mode='encryption'):
    result = ''
    for letter in text.lower():
        if letter in alphabet:
            index = alphabet.find(letter)
            if mode == 'encryption':
                new_index = (index + key) % len(alphabet)
            elif mode == 'decryption':
                new_index = (index - key) % len(alphabet)
            result += alphabet[new_index]
        else:
            result += letter
    return result

def generate_key():
    return random.randint(1, len(alphabet) - 1)

def decrypt(ciphertext):
    enumeration = []
    for key in range(len(alphabet)):
        plaintext = cipher(ciphertext, key, mode='decryption')
        enumeration.append((key, plaintext))
    return enumeration

def main_menu():
    print('Шифр Цезаря')
    print('1. Шифрование')
    print('2. Дешифрование')
    print('3. Взлом')
    print('0. Выход')
    choice = input('Выберите пункт: ')
    return choice

def encryption():
    message = input('Введите сообщение для шифрования: ')
    if not message:
        print("Сообщение не может быть пустым.")
        return
    key = generate_key()
    encrypted_text = cipher(message, key, mode='encryption')
    print(f'Зашифрованное сообщение: {encrypted_text}')
    print(f'Сгенерированный ключ: {key}')

def decryption():
    message = input('Введите зашифрованное сообщение: ')
    if not message:
        print("Сообщение не может быть пустым.")
        return
    while True:
        try:
            key = int(input('Введите ключ для дешифрования: '))
            break
        except ValueError:
            print('Некорректный ключ. Введите целое число.')
    decrypted_text = cipher(message, key, mode='decryption')
    print(f'Дешифрованное сообщение: {decrypted_text}')

def cracking():
    message = input('Введите зашифрованное сообщение для взлома: ')
    if not message:
        print("Сообщение не может быть пустым.")
        return
    results = decrypt(message)
    print('Возможные варианты расшифровки:')
    for key, plaintext in results:
        print(f'Ключ: {key}, Текст: {plaintext}')

def run_program():
    while True:
        choice = main_menu()
        if choice == '1':
            encryption()
        elif choice == '2':
            decryption()
        elif choice == '3':
            cracking()
        elif choice == '0':
            print('До свидания!')
            break
        else:
            print('Неправильный выбор. Попробуйте снова.')

if __name__ == '__main__':
    run_program()
