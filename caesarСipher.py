import random
from collections import Counter

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

# Функция шифрования/дешифрования текста
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

# Генерирует случайный ключ для шифра
def generate_key():
    return random.randint(1, len(alphabet) - 1)

# Взлом шифра методом перебора
def decrypt(ciphertext):
    enumeration = []
    for key in range(len(alphabet)):
        plaintext = cipher(ciphertext, key, mode='decryption')
        enumeration.append((key, plaintext))
    return enumeration

RUSSIAN_LETTER = {
    'о': 110,'е': 86,'а': 80,'и': 74,'н': 67,'т': 65,'с': 55,'р': 48,'в': 44,
    'л': 37,'к': 32,'м': 29,'д': 26,'п': 24,'у': 23,'я': 20,'ы': 18,'з': 17,
    'ь': 16,'б': 15,'г': 14,'ч': 13,'й': 12,'х': 10,'ж': 9,'ш': 8,
    'ю': 7,'ц': 5,'щ': 4,'э': 3,'ф': 2,'ъ': 1,'ё': 1
    }

RUSSIAN_DIGRAMS = {
    'ст': 95,'ен': 75,'то': 66,'на': 58,'но': 49,'ра': 47,'ов': 45,'ие': 43,'ни': 42,
    'ко': 40,'ал': 37,'ро': 35,'ре': 34,'во': 33,'пр': 32,'ос': 31,'не': 30,'ли': 28,
    'ло': 25,'по': 23,'ка': 21,'ве': 20,'ла': 18,'го': 16,'за': 15,'со': 14,'до': 13,
    'од': 12,'та': 11,'мо': 10,'па': 9,'те': 8,'ви': 7,'ва': 6,'ти': 5,'ши': 4,'ще': 3,
    'че': 2,'чу': 1
    }

def weighted_digrams_frequency_analysis(text):
    digram_counter = Counter([text[i:i+2].lower() for i in range(len(text)-1)])
    total_count = sum(digram_counter.values())

    # Считаем частоту каждой двуслога
    frequencies = {}
    for digram, count in digram_counter.items():
        if digram in RUSSIAN_DIGRAMS:
            weight = 1
            if digram in ['ст', 'ен', 'то']:
                weight = 2
            elif digram in ['на', 'но', 'ра']:
                weight = 1.5
            frequencies[digram] = count / total_count * 100 * weight

    # Сортируем по частоте
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    return sorted_frequencies

# Частотный анализ одиночных символов
def frequency_analysis(text):
    counter = Counter(text)
    total_count = sum(counter.values())

    # Считаем частоту каждой буквы
    frequencies = {}
    for char, count in counter.items():
        if char in RUSSIAN_LETTER:
            frequencies[char] = count / total_count * 100

    # Сортируем по частоте
    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    return sorted_frequencies

# меню программы
def main_menu():
    print('Шифр Цезаря')
    print('1. Шифрование')
    print('2. Дешифрование')
    print('3. Взлом')
    print('0. Выход')
    choice = input('Выберите пункт: ')
    return choice

def encryption():
    text = input('Введите сообщение для шифрования: ')
    if not text:
        print("Сообщение не может быть пустым.")
        return
    key = generate_key()
    encrypted_text = cipher(text, key, mode='encryption')
    print(f'Зашифрованное сообщение: {encrypted_text}')
    print(f'Сгенерированный ключ: {key}')

def decryption():
    text = input('Введите зашифрованное сообщение: ')
    if not text:
        print("Сообщение не может быть пустым.")
        return
    while True:
        try:
            key = int(input('Введите ключ для дешифрования: '))
            break
        except ValueError:
            print('Некорректный ключ. Введите целое число.')
    decrypted_text = cipher(text, key, mode='decryption')
    print(f'Дешифрованное сообщение: {decrypted_text}')

def cracking():
    text = input('Введите зашифрованное сообщение для взлома: ')
    if not text:
        print("Сообщение не может быть пустым.")
        return
    results = decrypt(text)

    # частотный анализ каждого возможного варианта расшифровки
    best_result = None
    best_score = float('-inf')
    for key, plaintext in results:
        letter_analysis = frequency_analysis(plaintext)
        digram_analysis = weighted_digrams_frequency_analysis(plaintext)

        # Оцениваем результат по совпадению с известной частотой букв и двуслогов
        score = 0
        for char, freq in letter_analysis:
            expected_freq = RUSSIAN_LETTER.get(char, 0)
            score += abs(freq - expected_freq)
        for digram, freq in digram_analysis:
            expected_freq = RUSSIAN_DIGRAMS.get(digram, 0)
            score += abs(freq - expected_freq)


        if score > best_score:
            best_score = score
            best_result = (key, plaintext)

    # Выводим лучший вариант
    print(f'Наиболее вероятная расшифровка:\nКлюч: {best_result[0]}, Текст: {best_result[1]}')

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