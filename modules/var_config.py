from func import *


def get_variables_from_json():
    # Загрузка данных из файла
    try:
        with open('variables.json', 'r') as file_var:
            variables = json.load(file_var)
            print(f"variables.json - loading successful")
            return variables
    except FileNotFoundError:
        # Если файл не найден, начинаем с пустого словаря
        variables = {"Booba_kush": {}, "Lizard_king": {}}

        print(f"variables.json not found, we make a new :)")
        return variables


def watering(variables, box):
    date = get_date()
    variables[box]["dates"] = date
    save_in_json(variables, 'variables.json')


def save_var(json_var, var, value, box):
    """Функция сохранения переменной в словаре JSON.
    На вход принимает json_var - переменная в которой хранится словарь.
    var - ссылка на переменную в словаре.
    value - значение переменной в словаре.
    box - ссылка на теплицу для которой будет сохраняться переменные .
    """

    if box not in json_var:
        json_var[box] = {}
    json_var[box][var] = value

    save_in_json(json_var, 'variables.json')
