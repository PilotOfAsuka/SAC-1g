from func import days_since_last_watering


BOT_TOKEN = "6901244838:AAH-UQ20wD719cFHfOFqR2_Wn2sdc5mIDUY"

current_temp = "Датчика нет"
air_hud = "Датчика нет"
dirt_hud = "Датчика нет"
days = days_since_last_watering("2024-02-15")

variables_file = "variables.json"
user_states_file = 'user_states.json'

start_text = ("🌿 Добро пожаловать в 'Систему автоматического контроля гровбоксом' САК-1г 🌿"
              "\n🤖 Это набросок приложения на основе телеграм бота 🤖"
              "\n🚨 Может уведомлять о критичных показателях пользователю 🚨"
              "\n🌱 Ну и удобный контроль 🌱")


def update_info(day_w, light, wing, light_d, c_t=current_temp, air_h=air_hud, dirt_h=dirt_hud, days_life=days):

    days_w = days_since_last_watering(day_w)
    light_n = 24 - light_d

    info_text =(f"🌡️ Текущая температура: {c_t}°C"
                f"\n"
                f"\n💧 Влажность воздуха: {air_h}%"
                f"\n"
                f"\n💦 Влажность почвы: {dirt_h}%"
                f"\n"
                f"\n💧 Дней с последнего полива: {days_w}"
                f"\n"
                f"\n☀️ Освещение: {'Включено' if light else 'Выключено'}"
                f"\n"
                f"\n🌞 Интервал освещения {light_d} дня/{light_n} ночи 🌚"
                f"\n"
                f"\n💨 Обдув: {'Включено' if wing else 'Выключено'}"
                f"\n"
                f"\n🌱 Дней роста: {days_life}"
                f"\n")
    return info_text
