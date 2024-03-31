from func import days_since_last_watering
#from modules.temp_module import get_sensor_data
from modules.var_config import get_variables_from_json
from modules.numtotex import text_rost
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

BOT_TOKEN = os.getenv("TEST_API")
variables = get_variables_from_json()


def light_night(light_day) -> int:
    try:
        night = 24 - light_day
        return night
    except TypeError:
        return 0


def update_info(box) -> str:
    try:
        day_w = variables.get(box).get('date_of_watering')
        light = variables.get(box).get('light_on')
        wing = variables.get(box).get('wing_on')
        light_day = variables.get(box).get('sun_value')
        termo = variables.get(box).get('termo_on')
        name_of_sort = variables.get(box).get('name')
        name_of_udobrenie = variables.get(box).get('name_udobr')

        current_temp, air_hud, voltage = 1,2,3

        days_w = days_since_last_watering(day_w)
        light_nigh = light_night(light_day)

        info_text = (f"\n🏷 Название сорта: {name_of_sort}"
                     f"\n"
                     f"\n🌡️ Текущая температура: {current_temp}°C"
                     f"\n"
                     f"\n💧 Влажность воздуха: {air_hud}%"
                     f"\n"
                     f"\n🔥 Обогрев: {'Включен' if termo else 'Выключен'}"
                     f"\n"
                     f"\n☀️ Освещение: {'Включено' if light else 'Выключено'}"
                     f"\n"
                     f"\n🌞 Интервал освещения {light_day} дня/{light_nigh} ночи 🌚"
                     f"\n"
                     f"\n💨 Обдув: {'Включено' if wing else 'Выключено'}"
                     f"\n"
                     f"\n📅 Дата посева: {variables.get(box).get('date_of_grow')}"
                     f"\n"
                     f"\n🌱Время роста: {text_rost(days_since_last_watering(variables.get(box).get('date_of_grow')))}"
                     f"\n"
                     f"\n🏷 Название удобрения: {name_of_udobrenie}"
                     f"\n"
                     f"\n💧 Дней с последнего полива: {days_w}")
        return info_text

    except Exception as e:
        return f"Произошла ошибка {e}"
