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
        variables = {'dates': "2024-02-17",
                     'light_on': False,
                     'wing_on': False,
                     'sun_value': 0,
                     'water_value': 0,
                     'termo_on': False,
                     'name': "BUBBA KUSH"}

        print(f"variables.json not found, we make a new :)")
        return variables


def watering(variables):
    date = get_date()
    variables["dates"] = date
    save_in_json(variables, 'variables.json')


def save_var(variables, var, value):
    variables[var] = value
    save_in_json(variables, 'variables.json')




