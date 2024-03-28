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


def save_var(variables, var, value, box):
    if box not in variables:
        variables[box] = {}
    variables[box][var] = value

    save_in_json(variables, 'variables.json')




