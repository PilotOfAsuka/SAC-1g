import json
from datetime import datetime


def save_in_json(var, file_dir):
    with open(file_dir, 'w') as file:
        json.dump(var, file)


def days_since_last_watering(last_watering_date):
    try:
        # Преобразование строковых дат в объекты datetime
        last_watering_date = datetime.strptime(last_watering_date, '%Y-%m-%d')
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_date = datetime.strptime(current_date, '%Y-%m-%d')
        # Вычисление разницы между датами
        days_difference = (current_date - last_watering_date).days

        return days_difference
    except TypeError:
        return None


def write_to_file(value, box, udobrenie=False):
    file_path = f"{box}_watering_history.txt"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    if udobrenie:
        text_to_write = f"{current_time} :Удобрено на {value} литров.\n"
    else:
        text_to_write = f"{current_time} :Полив на {value} литров.\n"

    # Запись текста в файл
    with open(file_path, 'a') as file:
        file.write(text_to_write)


def load_from_file(box):
    file_path = f"{box}_watering_history.txt"
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
    date = datetime.now().strftime('%Y-%m-%d')
    return date
