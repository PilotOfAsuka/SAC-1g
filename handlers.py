from aiogram import F

from misc import dp
from aiogram.types import (Message, CallbackQuery)
from aiogram.filters import Command
from menu import *

water_value = 0
day_value = 0


@dp.message(Command("start"))
async def start_handler(msg: Message):
    # user_id = str(msg.from_user.id)
    # Отправляем приветственное сообщение
    await msg.answer(cfg.start_text, reply_markup=main_menu_1)
    await msg.answer(cfg.update_info(dates.get("last_day"), light_on, wing_on, day_value), reply_markup=info_menu)
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


def create_menu_handler(menu_list, menu_actions):
    @dp.message(lambda message: message.text in menu_list)
    async def create_menu(msg: Message):
        await handle_menu(msg, menu_actions)


# Ивенты Маин меню
@dp.message(lambda message: message.text in main_menu_list)
async def main_menu(msg: Message):
    if msg.text == main_menu_list[4]:
        await msg.answer(cfg.update_info(dates.get("last_day"), light_on, wing_on, day_value), reply_markup=info_menu)
    else:
        await handle_menu(msg, main_menu_actions)


# История поливов
@dp.message(lambda message: message.text == water_menu_list[2])
async def get_history(msg: Message):
    await msg.answer(func.load_from_file())


@dp.message(lambda message: message.text in light_set_menu_list)  # Включение света
async def menu(msg: Message):
    global light_on
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "light_set":
        if msg.text == light_set_menu_list[0]:
            if light_on is True:
                light_on = False
                set_user_state(msg, "idle")
                await msg.answer('💡Лампа была выключена, возвращаем вас в главное меню:', reply_markup=main_menu_1)
            else:
                light_on = True
                set_user_state(msg, "idle")
                await msg.answer('💡Лампа была включена, возвращаем вас в главное меню:', reply_markup=main_menu_1)
    pass


@dp.message(lambda message: message.text in wing_menu_list)  # Включение обдува
async def menu(msg: Message):
    global wing_on
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "wing":
        if msg.text == wing_menu_list[0]:
            if wing_on is True:
                wing_on = False
                set_user_state(msg, "idle")
                await msg.answer('💨 Обдув был выключен, возвращаем вас в главное меню 💨', reply_markup=main_menu_1)
            else:
                wing_on = True
                set_user_state(msg, "idle")
                await msg.answer('💨 Обдув был включен, возвращаем вас в главное меню 💨', reply_markup=main_menu_1)
    pass


# Кнопка обновить
@dp.callback_query(F.data == user_button_list[0])
async def send_random_value(callback: CallbackQuery):
    await callback.message.answer(cfg.update_info(dates.get("last_day"), light_on, wing_on, day_value), reply_markup=info_menu)


# Ивенты да и нет
@dp.message(lambda message: message.text in check_buttons_list)
async def water_set_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "water_set_w":
        if msg.text == check_buttons_list[0]:
            await msg.answer("🌧️ Успешно совершен полив! 🌧️\nВозвращаем вас в главное меню.", reply_markup=main_menu_1)
            watering()
            func.write_to_file(water_value)
            set_user_state(msg, "idle")
        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")
    elif user_states.get(user_id) == "light_set_day":
        if msg.text == check_buttons_list[0]:
            await msg.answer("💡 Успешно установлен интервал работы лампы! 💡\nВозвращаем вас в главное меню.", reply_markup=main_menu_1)
            set_user_state(msg, "idle")
        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")
    else:
        await msg.answer("123")


# Ивенты для различных меню
create_menu_handler(water_menu_list, water_menu_actions)
create_menu_handler(light_menu_list, light_menu_actions)
create_menu_handler(temp_menu_list, temp_menu_actions)


# Ивенты кнопки назад
@dp.message(lambda message: message.text == "Назад")
async def back(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) in ["light", "water", "wing", "temp"]:
        set_user_state(msg, "idle")
        await msg.answer("🏡 Вы в главном меню 🏡", reply_markup=main_menu_1)
    elif user_states.get(user_id) in ["water_set", "water_set_w"]:
        set_user_state(msg, "water")
        await msg.answer("🌧️ Вы вошли в меню контроля поливом:", reply_markup=in_water_menu)
    elif user_states.get(user_id) in ["light_set", "light_set_day"]:
        set_user_state(msg, "light")
        await msg.answer("💡 Вы вошли в меню контроля света:", reply_markup=in_light_menu)
    elif user_states.get(user_id) in ["temp_set"]:
        set_user_state(msg, "temp")
        await msg.answer("🔥 Вы вошли в меню контроля обогревом:", reply_markup=in_temp_menu)
    else:
        await msg.answer("Назад пути нет", reply_markup=main_menu_1)


# обработка текстовой информации
@dp.message()
async def message_handler(msg: Message):
    global water_value
    global day_value
    # user_name = msg.from_user.username
    user_id = str(msg.from_user.id)
    if msg.text is not None:
        if user_states.get(user_id) == "water_set_w":
            try:
                water_value = int(msg.text)
                await msg.answer(f"🌧️ Вы хотите совершить полив на {water_value} литров 🌧️", reply_markup=check_menu)
            except ValueError:
                await msg.answer("❌ Это не число, повторите еще раз ❌")
            pass
        elif user_states.get(user_id) == "light_set_day":
            try:
                day_value = int(msg.text)
                await msg.answer(f"🌧️ Вы хотите установить день на {day_value} часов️", reply_markup=check_menu)
            except ValueError:
                await msg.answer("❌ Это не число, повторите еще раз ❌")

        else:
            await msg.answer("⚠️ Используйте кнопки для навигации по меню ⚠️")
