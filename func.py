import json
from datetime import datetime


def save_in_json(dictionary, file_dir):
    """Принимает на вход словарь (dictionary) значений и сохраняет в файл JSON"""
    with open(file_dir, 'w') as file:
        json.dump(dictionary, file)


def days_since_last_watering(last_watering_date) -> int:
    """На вход принимает дату ГГГГ-ММ-ДД:str и возвращает количество дней прошедших с этой даты"""
    try:
        # Преобразование строковых дат в объекты datetime
        last_watering_date = datetime.strptime(last_watering_date, '%Y-%m-%d')
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        # Вычисление разницы между датами
        days_difference = (current_date - last_watering_date).days
        return days_difference
    except TypeError:
        return 0


def write_to_file(value, box, fertilizer=False):
    """Сохраняет историю полива или удобрения в TXT файл для конкретного бокса"""
    file_path = f"history/{box}_watering_history.txt"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    if fertilizer:
        text_to_write = f"{current_time} :Удобрено на {value} литров.\n"
    else:
        text_to_write = f"{current_time} :Полив на {value} литров.\n"
    # Запись текста в файл
    with open(file_path, 'a') as file:
        file.write(text_to_write)


def load_from_file(box) -> str:
    """Читает файл истории для конкретного бокса"""
    file_path = f"history/{box}_watering_history.txt"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            if content.strip():  # Проверка на пустой файл
                return content
            else:
                return '📜 История пуста 📜'
    except FileNotFoundError:
        err = f"Файл {file_path} не найден"
        return err


def get_date():
    """Возвращает дату в формате ГГГГ-ММ-ДД"""
    date = datetime.now().strftime('%Y-%m-%d')
    return date
