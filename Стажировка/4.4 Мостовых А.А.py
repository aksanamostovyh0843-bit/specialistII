import string

def analyze_text(text):
    """
    Анализирует текст и возвращает словарь с частотой каждого слова.
    
    Параметры:
    text (str): Текст для анализа
    
    Возвращает:
    dict: Словарь вида {слово: количество_вхождений}
    """
    # Приводим текст к нижнему регистру
    text = text.lower()
    
    # Удаляем знаки пунктуации
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator)
    
    # Разбиваем текст на слова
    words = cleaned_text.split()
    
    # Подсчитываем частоту слов
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    return word_count

def print_word_frequency(word_count):
    """
    Выводит результаты подсчета частоты слов в удобном формате.
    
    Параметры:
    word_count (dict): Словарь с частотой слов
    """
    # Сортируем слова по частоте (убывание) и алфавиту (возрастание)
    sorted_words = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    
    # Выводим заголовок таблицы
    print("Слово".ljust(20) + "| Количество")
    print("-" * 30)
    
    # Выводим каждое слово с его частотой
    for word, count in sorted_words:
        print(f"{word.ljust(20)}| {count}")

def main():
    """Основная функция программы"""
    print("Анализатор частоты слов в тексте")
    print("-------------------------------")
    
    # Получаем текст от пользователя
    text = input("Введите текст для анализа:\n")
    
    # Анализируем текст
    word_count = analyze_text(text)
    
    # Выводим результаты
    print("\nРезультаты анализа:")
    print_word_frequency(word_count)

if __name__ == "__main__":
    main()