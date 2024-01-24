from func import days_since_last_watering


BOT_TOKEN = "6540946269:AAFS9VxfD93UHtPHpFs5oNmENN34OCvNjzQ"

current_temp = 20
air_hud = 35
dirt_hud = 45
days = 10


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
