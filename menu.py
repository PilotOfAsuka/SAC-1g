from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
import config as cfg
import json
import func


# Загрузка данных из файла
def load_json(name):
    try:
        with open(name, 'r') as file_user:
            file = json.load(file_user)
            print(f"{name} - loading successful")
            return file
    except FileNotFoundError:
        # Если файл не найден, начинаем с пустого словаря
        file = {}
        print(f"{name} not found, we make a new :)")
        return file


user_states = load_json(cfg.user_states_file)
user_box = load_json(cfg.user_box_file)


def time_buttons():
    back_button = KeyboardButton(text="Назад")
    time_buttons_set = [[KeyboardButton(text=str(i * 4 + j + 1)) for j in range(4)] for i in range(6)]
    time_buttons_set.append([back_button])
    time_button = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=time_buttons_set)
    return time_button


def test_back():
    back_button_test = [[KeyboardButton(text="🔙 Назад")]]
    t_b = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=back_button_test)
    return t_b


# изменение состояния user
def set_user_state(msg, state):
    user_id = str(msg.from_user.id)
    user_states[user_id] = state
    func.save_in_json(user_states, cfg.user_states_file)


def set_user_box(msg, box):
    user_id = str(msg.from_user.id)
    user_box[user_id] = box
    func.save_in_json(user_box, cfg.user_box_file)


def menu_generator(button_list, back_b=False):
    back_button = KeyboardButton(text="🔙 Назад")
    buttons = [[KeyboardButton(text=button)] for button in button_list]
    if back_b is not False:
        buttons.append([back_button])
    menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return menu


# Списки кнопок
# список боксов
box_list = ['Booba_kush', 'Lizard_king']

main_menu_list = ["🌧️ Контроль полива 🌧️", "💡 Контроль освещения 💡", "💨 Контроль обдува 💨",
                  "🔥 Контроль обогрева 🔥", "ℹ️ Информация ℹ️", "⚙️Настройки⚙️"]

water_menu_list = ["💧 Совершить полив 💧", "🌱 Добавить удобрение 🌱",
                   "⚙️ Настройка помпы ⚙️", "📜 История поливов и удобрений 🌧️"]

light_menu_list = ["⏲️ Установка интервала освещения ⏲️", "💡 Управление лампой 💡"]
light_set_menu_list = ["💡Включение/выключение 💡", "⚙️Настройка мощности ⚙️"]

wing_menu_list = ["⚙️Включение/выключение обдува⚙️"]

temp_menu_list = ["⚙️Включение/выключение обогрева⚙️"]

user_button_list = ["🔁 Обновить 🔁"]  # togo

setting_button_list = ['👤 Изменить имя', '🌿 Изменить название удобрения', '📅 Установить дату посева', 'ВЫБРАТЬ БОКС']


check_buttons_list = ["✅ Да", "❌ Нет"]

# Создаем клавиатуры
box_menu = menu_generator(box_list, back_b=True)

main_menu_1 = menu_generator(main_menu_list)  # главное меню
in_water_menu = menu_generator(water_menu_list, back_b=True)  # меню полива
in_light_menu = menu_generator(light_menu_list, back_b=True)  # меню света
in_light_set_menu = menu_generator(light_set_menu_list, back_b=True)

in_wing_menu = menu_generator(wing_menu_list, back_b=True)  # меню обдува
in_temp_menu = menu_generator(temp_menu_list, back_b=True)  # меню обогрева

# Кнопки информационного табло
info_buttons = [[InlineKeyboardButton(text=button, callback_data=button)] for button in user_button_list]
info_menu = InlineKeyboardMarkup(inline_keyboard=info_buttons)
# Кнопки индивидуальной настройки
settings_menu = menu_generator(setting_button_list, back_b=True)

# Кнопки да нет
check_menu = menu_generator(check_buttons_list)


# Словарь действий для главного меню user_state, text, menu
main_menu_actions = {
    main_menu_list[0]: ("water", "🌧️ Вы вошли в меню контроля поливом:", in_water_menu),
    main_menu_list[1]: ("light", "💡 Вы вошли в меню контроля света:", in_light_menu),
    main_menu_list[2]: ("wing", "💨 Вы вошли в меню контроля обдува:", in_wing_menu),
    main_menu_list[3]: ("temp", "🔥 Вы вошли в меню контроля обогревом:", in_temp_menu),
    main_menu_list[5]: ("in_settings", "⚙️ Меню настройки параметров:", settings_menu)

}

water_menu_actions = {
    water_menu_list[0]: ("water_set_w", "💧 Введите кол-во воды в литрах:", test_back()),
    water_menu_list[1]: ("water_set_udr", "Введите ко-во удобрения в литрах", test_back()),
    water_menu_list[2]: ("water_set", "⚙️ Настройки помпы:", test_back()),
}

light_menu_actions = {
    light_menu_list[0]: ("light_set_day", "⏲️ Укажите количество часов 'Дня':", time_buttons()),
    light_menu_list[1]: ("light_set", "💡 Меню управления лампой:", in_light_set_menu)
}

settings_menu_actions = {
    setting_button_list[0]: ('name_set', "👤 Укажите новое имя", test_back()),
    setting_button_list[1]: ('udobr_set', "🌿 Укажите новое удобрение", test_back()),
    setting_button_list[2]: ('set_date', "📅 Укажите новую дату посева в формате GGGG-MM-DD \nПример 2024-04-10",
                             test_back()),
    setting_button_list[3]: ('set_box', "Выберите бокс:", box_menu)
}
