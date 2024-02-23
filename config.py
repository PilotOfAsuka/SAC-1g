from func import days_since_last_watering


BOT_TOKEN = "6901244838:AAH-UQ20wD719cFHfOFqR2_Wn2sdc5mIDUY"

current_temp = "🛑"
air_hud = "🛑"
dirt_hud = "🛑"
name_sort = "BUBBA KUSH"
date_of_seed = '2024-02-14'


variables_file = "variables.json"
user_states_file = 'user_states.json'

start_text = ("🌿 Добро пожаловать в 'Систему автоматического контроля гровбоксом' САК-1г 🌿"
              "\n🤖 Это набросок приложения на основе телеграм бота 🤖"
              "\n🚨 Может уведомлять о критичных показателях пользователю 🚨"
              "\n🌱 Ну и удобный контроль 🌱")


def update_info(day_w, light, wing, light_day, termo, c_t=current_temp, air_h=air_hud, dirt_h=dirt_hud):

    days_w = days_since_last_watering(day_w)
    light_night = 24 - light_day

    info_text =(f"\n 🏷 Название сорта: {name_sort} "
                f"\n"
                f"\n🌡️ Текущая температура: {c_t}°C"
                f"\n"
                f"\n💧 Влажность воздуха: {air_h}%"
                f"\n"
                f"\n💦 Влажность почвы: {dirt_h}%"
                f"\n"
                f"\n🔥 Обогрев: {'Включен' if termo else 'Выключен'}"
                f"\n"
                f"\n☀️ Освещение: {'Включено' if light else 'Выключено'}"
                f"\n"
                f"\n🌞 Интервал освещения {light_day} дня/{light_night} ночи 🌚"
                f"\n"
                f"\n💨 Обдув: {'Включено' if wing else 'Выключено'}"
                f"\n"
                f"\n📅 Дата посева: {date_of_seed}"
                f"\n"
                f"\n🌱 Дней роста: {days_since_last_watering('2024-02-15')}"
                f"\n"
                f"\n💧 Дней с последнего полива: {days_w}")
    return info_text

