from aiogram import F
from misc import dp
from aiogram.types import (Message, ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)
from aiogram.filters import Command
from aiogram.methods import GetChat
import func
import json
import config as cfg


def time_buttons():
    time_buttons_set = [[KeyboardButton(text=str(i * 4 + j + 1)) for j in range(4)] for i in range(6)]
    time_buttons_set.append([back_button])
    time_button = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=time_buttons_set)
    return time_button


# изменение состояния user
def set_user_state(msg, state):
    user_id = str(msg.from_user.id)
    user_states[user_id] = state
    func.save_in_json(user_states, cfg.user_states_file)


def menu_generator(button_list, back_b=False):
    buttons = [[KeyboardButton(text=button)] for button in button_list]
    if back_b is not False:
        buttons.append([back_button])
    menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    return menu


# Списки кнопок
back_button = KeyboardButton(text="Назад")
back_button_test = [[KeyboardButton(text="Назад")]]
test_back = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=back_button_test)

main_menu_list = ["🌧️ Контроль полива 🌧️", "💡 Контроль освещения 💡", "💨 Контроль обдува 💨",
                  "🔥 Контроль обогрева 🔥", "ℹ️ Информация ℹ️"]
water_menu_list = ["⏲️ Установка интервала полива ⏲️", "💧 Установка кол-во воды 💧", "⚙️ Настройка помпы ⚙️"]
light_menu_list = ["⏲️ Установка интервала освещения ⏲️", "💡 Установка силы освещения 💡"]
wing_menu_list = ["💨 Установка силы обдува 💨"]
temp_menu_list = ["⏲️ Установка интервала обогрева ⏲️", "🌡️ Oбогрев по датчику 🌡️"]
user_button_list = ["🔁 Обновить 🔁"]  # togo


# Создаем клавиатуры
main_menu_1 = menu_generator(main_menu_list)
in_water_menu = menu_generator(water_menu_list, back_b=True)
in_light_menu = menu_generator(light_menu_list, back_b=True)
in_wing_menu = menu_generator(wing_menu_list, back_b=True)
in_temp_menu = menu_generator(temp_menu_list, back_b=True)

info_buttons = [[InlineKeyboardButton(text=button, callback_data=button)] for button in user_button_list]
info_menu = InlineKeyboardMarkup(inline_keyboard=info_buttons)

# Словарь действий для главного меню user_state, text, menu
main_menu_actions = {
    main_menu_list[0]: ("water", "🌧️ Вы вошли в меню контроля поливом:", in_water_menu),
    main_menu_list[1]: ("light", "💡 Вы вошли в меню контроля света:", in_light_menu),
    main_menu_list[2]: ("wing", "💨 Вы вошли в меню контроля обдува:", in_wing_menu),
    main_menu_list[3]: ("temp", "🔥 Вы вошли в меню контроля обогревом:", in_temp_menu),
    main_menu_list[4]: ("info", cfg.info_text, info_menu),
}

water_menu_actions = {
    water_menu_list[0]: ("water_set", "⏲️ Введите интервал в Часах:", time_buttons()),
    water_menu_list[1]: ("water_set", "💧 Введите кол-во воды в мл:", test_back),
    water_menu_list[2]: ("water_set", "⚙️ Настройки помпы:", test_back),
}

light_menu_actions = {
    light_menu_list[0]: ("light_set", "⏲️ Укажите количество часов 'Дня':", time_buttons()),
    light_menu_list[1]: ("light_set", "💡 Укажите мощность в процентах от 0 до 100:", test_back)
}

wing_menu_actions = {
    wing_menu_list[0]: ("wing_set", "💨 Укажите мощность в процентах от 0 до 100:", test_back)
}

temp_menu_actions = {
    temp_menu_list[0]: ("temp_set", "⏲️ Укажите время работы обогрева:", test_back),
    temp_menu_list[1]: ("temp_set", "🌡️ Установлен обогрев по датчику", test_back)
}


# Загрузка данных из файла
try:
    with open(cfg.user_states_file, 'r') as file_user_states:
        user_states = json.load(file_user_states)
        print(f"{cfg.user_states_file} - loading successful")
except FileNotFoundError:
    # Если файл не найден, начинаем с пустого словаря
    user_states = {}
    print(f"{cfg.user_states_file} not found, we make a new :)")


@dp.message(Command("start"))
async def start_handler(msg: Message):
    # user_id = str(msg.from_user.id)
    # Отправляем приветственное сообщение
    await msg.answer(cfg.start_text, reply_markup=main_menu_1)
    await msg.answer(cfg.info_text, reply_markup=info_menu)
    await msg.delete()
    set_user_state(msg, "idle")


async def handle_menu(msg, menu_actions):
    selected_option = menu_actions.get(msg.text)
    if selected_option:
        user_state, response_text, reply_markup = selected_option
        set_user_state(msg, user_state)
        await msg.answer(response_text, reply_markup=reply_markup)
    else:
        await msg.answer("Неизвестная опция в меню.")


# Ивенты Маин меню
@dp.message(lambda message: message.text in main_menu_list)
async def main_menu(msg: Message):
    await handle_menu(msg, main_menu_actions)


# Ивенты water_menu
@dp.message(lambda message: message.text in water_menu_list)
async def water_menu(msg: Message):
    await handle_menu(msg, water_menu_actions)


# Ивенты light_menu
@dp.message(lambda message: message.text in light_menu_list)
async def light_menu(msg: Message):
    await handle_menu(msg, light_menu_actions)


# Ивенты wing_menu
@dp.message(lambda message: message.text in wing_menu_list)
async def wing_menu(msg: Message):
    await handle_menu(msg, wing_menu_actions)


# Ивенты temp_menu
@dp.message(lambda message: message.text in temp_menu_list)
async def temp_menu(msg: Message):
    await handle_menu(msg, temp_menu_actions)


# Кнопка обновить
@dp.callback_query(F.data == user_button_list[0])
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(cfg.info_text, reply_markup=info_menu)


# Ивенты кнопки назад
@dp.message(lambda message: message.text == "Назад")
async def back(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) in ["light", "water", "wing", "temp"]:
        set_user_state(msg, "idle")
        await msg.answer("🏡 Вы в главном меню 🏡", reply_markup=main_menu_1)
    elif user_states.get(user_id) in ["water_set"]:
        set_user_state(msg, "water")
        await msg.answer("🌧️ Вы вошли в меню контроля поливом:", reply_markup=in_water_menu)
    elif user_states.get(user_id) in ["light_set"]:
        set_user_state(msg, "light")
        await msg.answer("💡 Вы вошли в меню контроля света:", reply_markup=in_light_menu)
    elif user_states.get(user_id) in ["wing_set"]:
        set_user_state(msg, "wing")
        await msg.answer("💨 Вы вошли в меню контроля обдува:", reply_markup=in_wing_menu)
    elif user_states.get(user_id) in ["temp_set"]:
        set_user_state(msg, "temp")
        await msg.answer("🔥 Вы вошли в меню контроля обогревом:", reply_markup=in_temp_menu)
    else:
        await msg.answer("Назад пути нет", reply_markup=main_menu_1)


@dp.message()
async def message_handler(msg: Message):
    # user_name = msg.from_user.username
    # user_id = str(msg.from_user.id)
    if msg.text is not None:
        await msg.answer("Используйте кнопки для навигации по меню")
