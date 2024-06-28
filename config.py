from func import days_since_last_watering
from modules.temp_module import get_mi_sensor_data
from modules.var_config import get_variables_from_json
from modules.numtotex import text_rost
from dotenv import load_dotenv
import os
from CONSTANTS import Box_device_address, Room_device_address

# Загрузить переменные окружения из файла .env
load_dotenv()

BOT_TOKEN = os.getenv("API")
variables = get_variables_from_json()


def light_night(light_day) -> int:
    try:
        night = 24 - light_day
        return night
    except TypeError:
        return 0


def get_data_sensor(sensor):
    if sensor.lower() == 'booba_kush':
        t, h, = 0, 0
        return t, h, 0, 0
    elif sensor.lower() == 'lizard_king':
        t, h, voltage = get_mi_sensor_data(Box_device_address)
        t2, h2, voltage2 = get_mi_sensor_data(Room_device_address)
        if t and h and t2 and h2:
            return t, h, t2, h2
        else:
            return 0, 0, 0, 0
    else:
        return 0, 0


def update_info(box) -> str:
    try:
        day_w = variables.get(box).get('date_of_watering')
        light = variables.get(box).get('light_on')
        wing = variables.get(box).get('wing_on')
        light_day = variables.get(box).get('sun_value')
        termo = variables.get(box).get('termo_on')
        name_of_sort = variables.get(box).get('name')
        name_of_udobrenie = variables.get(box).get('name_udobr')

        current_temp, air_hud, t2, h2 = get_data_sensor(box)

        days_w = days_since_last_watering(day_w)
        light_nigh = light_night(light_day)

        info_text = get_info_text(box=box, name_of_sort=name_of_sort, current_temp=current_temp,
                                  air_hud=air_hud, termo=termo, light=light, light_day=light_day, light_nigh=light_nigh,
                                  wing=wing, name_of_udobrenie=name_of_udobrenie, days_w=days_w, t2=t2, h2=h2)
        return info_text


    except Exception as e:
        return f"Произошла ошибка {e}"


def get_info_text(box, name_of_sort, current_temp, air_hud, termo, light, light_day, light_nigh, wing, name_of_udobrenie, days_w, t2, h2) -> str:
    if box.lower() == 'booba_kush':
        harvest_day = variables.get(box).get("harvest_day")
        text_of_info = (f"\n🏷 Название сорта: {name_of_sort}"
                        f"\nХарвест {harvest_day} " if variables.get(box).get("harvest") is True else ""
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
        return text_of_info
    elif box.lower() == 'lizard_king':
        text_of_info = (f"\n🏷 Название сорта: {name_of_sort}"
                        f"\n"
                        f"\n🌡️ Температура в парнике: {current_temp}°C"
                        f"\n🌡️ Температура второй точки: {t2}°C"
                        f"\n🌡️ Средняя температура: {(t2+current_temp)/2}°C"
                        f"\n"
                        f"\n💧 Влажность в парнике: {air_hud}%"
                        f"\n💧 Влажность второй точки: {h2}%"
                        f"\n"
                        f"\n🔥 Обогрев: {'Включен' if termo else 'Выключен'}"
                        f"\n"
                        f"\n☀️ Освещение: {'Включено' if light else 'Выключено'}"
                        f"\n"
                        f"\n📅 Дата инокуляции: {variables.get(box).get('date_of_grow')}"
                        f"\n"
                        f"\n🌱 С момента инокуляции: {text_rost(days_since_last_watering(variables.get(box).get('date_of_grow')))}"
                        f"\n"
                        f"\n🏷 Кейк: {name_of_udobrenie}")
        return text_of_info
