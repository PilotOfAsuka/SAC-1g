from aiogram import F

from misc import dp, bot
from aiogram.types import (Message, CallbackQuery)
from aiogram.filters import Command
from menu import *

from modules import admin_panael, var_config

udr_value_chache = 0
day_value_chache = 0
water_value_chache = 0
sort_name = None
udr_name = None
date_of_grow = None

@dp.message(Command("id"))
async def get_chat_id(msg: Message):
    chat_id = str(msg.chat.id)
    await msg.answer("ИД данного чата: " + chat_id)


@dp.message(Command("my_id"))
async def get_user_id(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer("Твой ID: " + user_id)


@dp.message(Command("start"))
@admin_panael.check_admins
async def start_handler(msg: Message):
    user_id = str(msg.from_user.id)
    # Отправляем приветственное сообщение
    await msg.delete()
    await msg.answer(cfg.start_text)
    if user_box.get(user_id) is None:
        set_user_state(msg, "set_box")
        await msg.answer(text=f"Привет {msg.from_user.first_name}, Выбери свой бокс:", reply_markup=box_menu)
    else:
        await msg.answer(cfg.update_info(box=user_box.get(user_id)), reply_markup=info_menu)
        await msg.answer(text=f"Привет {msg.from_user.first_name} и добро пожаловать!", reply_markup=main_menu_1)
        set_user_state(msg, "idle")


async def handle_menu(msg, menu_actions):
    selected_option = menu_actions.get(msg.text)
    if user_states.get(str(msg.from_user.id)) is not None:
        if selected_option:
            user_state, response_text, reply_markup = selected_option
            set_user_state(msg, user_state)
            await msg.answer(response_text, reply_markup=reply_markup)
        else:
            await msg.answer("Неизвестная опция в меню.")
    else:
        await msg.answer(text="Кажется было произведено обновление на сервере, выполните команду /start")


def create_menu_handler(menu_list, menu_actions):
    @dp.message(lambda message: message.text in menu_list)
    @admin_panael.check_admins
    async def create_menu(msg: Message):
        await handle_menu(msg, menu_actions)


# Ивенты Маин меню
@dp.message(lambda message: message.text in main_menu_list)
@admin_panael.check_admins
async def main_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) is not None:
        if msg.text != main_menu_list[4]:
            await handle_menu(msg, main_menu_actions)
        else:
            await msg.answer(cfg.update_info(box=user_box.get(user_id)), reply_markup=info_menu)
    else:
        await msg.answer(text="Кажется было произведено обновление на сервере, выполните команду /start")


# История поливов
@dp.message(lambda message: message.text == water_menu_list[3])
@admin_panael.check_admins
async def get_history(msg: Message):
    user_id = str(msg.from_user.id)
    await msg.answer(func.load_from_file(box=user_box.get(user_id)))


@dp.message(lambda message: message.text in light_set_menu_list)  # Включение света
@admin_panael.check_admins
async def light_on_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "light_set":
        if msg.text == light_set_menu_list[0]:
            if cfg.variables.get('light_on') is True:
                var_config.save_var(variables=cfg.variables, var='light_on', value=False, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('💡Лампа была выключена, возвращаем вас в главное меню:', reply_markup=main_menu_1)
            else:
                var_config.save_var(variables=cfg.variables, var='light_on', value=True, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('💡Лампа была включена, возвращаем вас в главное меню:', reply_markup=main_menu_1)
    pass


@dp.message(lambda message: message.text in wing_menu_list)  # Включение обдува
@admin_panael.check_admins
async def wing_on_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "wing":
        if msg.text == wing_menu_list[0]:
            if cfg.variables.get('wing_on') is True:
                var_config.save_var(variables=cfg.variables, var="wing_on", value=False, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('💨 Обдув был выключен, возвращаем вас в главное меню 💨', reply_markup=main_menu_1)
            else:
                var_config.save_var(variables=cfg.variables, var="wing_on", value=True, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('💨 Обдув был включен, возвращаем вас в главное меню 💨', reply_markup=main_menu_1)
    pass


@dp.message(lambda message: message.text in temp_menu_list)  # Включение обогрева
@admin_panael.check_admins
async def termo_on_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "temp":
        if msg.text == temp_menu_list[0]:
            if cfg.variables.get('termo_on') is True:
                var_config.save_var(variables=cfg.variables, var="termo_on", value=False, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('🔥 Обогрев был выключен, возвращаем вас в главное меню 🔥', reply_markup=main_menu_1)
            else:
                var_config.save_var(variables=cfg.variables, var="termo_on", value=True, box=user_box.get(user_id))
                set_user_state(msg, "idle")
                await msg.answer('🔥 Обогрев был включен, возвращаем вас в главное меню 🔥', reply_markup=main_menu_1)
    pass


# Кнопка обновить
@dp.callback_query(F.data == user_button_list[0])
@admin_panael.check_admins
async def send_update_value(callback: CallbackQuery):
    user_id = str(callback.from_user.id)
    await callback.message.answer(cfg.update_info(box=user_box.get(user_id)), reply_markup=info_menu)


# Ивенты да и нет
@dp.message(lambda message: message.text in check_buttons_list)
@admin_panael.check_admins
async def water_set_menu(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == "water_set_w":
        if msg.text == check_buttons_list[0]:
            await msg.answer("🌧️ Успешно совершен полив! 🌧️\nВозвращаем вас в главное меню.", reply_markup=main_menu_1)
            await bot.send_message(chat_id=5848061277,
                                   text=f"Совершен полив на {water_value_chache} литра")  # Уведомление в ЛС
            var_config.save_var(variables=cfg.variables, var="date_of_watering", value=func.get_date(), box=user_box.get(user_id))
            var_config.save_var(variables=cfg.variables, var="water_value", value=water_value_chache, box=user_box.get(user_id))
            func.write_to_file(cfg.variables[user_box.get(user_id)]['water_value'], box=user_box.get(user_id))
            set_user_state(msg, "idle")

        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню",
                             reply_markup=main_menu_1)
            set_user_state(msg, "idle")

    elif user_states.get(user_id) == "water_set_udr":
        if msg.text == check_buttons_list[0]:
            await msg.answer("Успешно добавлено удобрение️\nВозвращаем вас в главное меню.", reply_markup=main_menu_1)
            var_config.save_var(variables=cfg.variables, var="udr_value", value=udr_value_chache, box=user_box.get(user_id))
            func.write_to_file(cfg.variables[user_box.get(user_id)]['udr_value'],box=user_box.get(user_id), udobrenie=True)
            set_user_state(msg, "idle")

        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню",
                             reply_markup=main_menu_1)
            set_user_state(msg, "idle")
    elif user_states.get(user_id) == "light_set_day":
        if msg.text == check_buttons_list[0]:
            var_config.save_var(variables=cfg.variables, var="sun_value", value=day_value_chache, box=user_box.get(user_id))
            await msg.answer("💡 Успешно установлен интервал работы лампы! 💡\nВозвращаем вас в главное меню.",
                             reply_markup=main_menu_1)
            set_user_state(msg, "idle")

        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")

    elif user_states.get(user_id) == "name_set":
        if msg.text == check_buttons_list[0]:
            var_config.save_var(variables=cfg.variables, var="name", value=sort_name, box=user_box.get(user_id))
            await msg.answer("💡 Успешно установлено новое название! 💡\nВозвращаем вас в главное меню.",
                             reply_markup=main_menu_1)
            set_user_state(msg, "idle")
        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")

    elif user_states.get(user_id) == "udobr_set":
        if msg.text == check_buttons_list[0]:
            var_config.save_var(variables=cfg.variables, var="name_udobr", value=udr_name, box=user_box.get(user_id))
            await msg.answer("💡 Успешно установлено новое название! 💡\nВозвращаем вас в главное меню.",
                             reply_markup=main_menu_1)
            set_user_state(msg, "idle")
        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")

    elif user_states.get(user_id) == "set_date":
        if msg.text == check_buttons_list[0]:
            var_config.save_var(variables=cfg.variables, var="date_of_grow", value=date_of_grow, box=user_box.get(user_id))
            await msg.answer(text="Успешно установлена новая дата.\nВозвращаем вас в главное меню.", reply_markup=main_menu_1)
        elif msg.text == check_buttons_list[1]:
            await msg.answer("❌ Вы отказались! ❌\nВозвращаем вас в главное меню", reply_markup=main_menu_1)
            set_user_state(msg, "idle")

    else:
        await msg.answer("⚠️ Произошла ошибка в обработке запросов. 🔄\nВозврат в главное меню",
                         reply_markup=main_menu_1)


# Ивенты для различных меню
create_menu_handler(water_menu_list, water_menu_actions)
create_menu_handler(light_menu_list, light_menu_actions)
create_menu_handler(setting_button_list, settings_menu_actions)


@dp.message(lambda message: message.text in box_list)  # Выбор бокса
@admin_panael.check_admins
async def set_box(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) == 'set_box':
        set_user_box(msg, msg.text)
        await msg.answer(text=f"Вы выбрали {user_box.get(user_id)}, изменить можно в настройках:", reply_markup=main_menu_1)
        set_user_state(msg, "idle")
        pass
    pass


# Ивенты кнопки назад
@dp.message(lambda message: message.text == "🔙 Назад")
@admin_panael.check_admins
async def back(msg: Message):
    user_id = str(msg.from_user.id)
    if user_states.get(user_id) in ["light", "water", "wing", "temp", "in_settings"]:
        set_user_state(msg, "idle")
        await msg.answer("🏡 Вы в главном меню 🏡", reply_markup=main_menu_1)

    elif user_states.get(user_id) in ["water_set", "water_set_w", "water_set_udr"]:
        set_user_state(msg, "water")
        await msg.answer("🌧️ Вы вошли в меню контроля поливом:", reply_markup=in_water_menu)

    elif user_states.get(user_id) in ["light_set", "light_set_day"]:
        set_user_state(msg, "light")
        await msg.answer("💡 Вы вошли в меню контроля света:", reply_markup=in_light_menu)

    elif user_states.get(user_id) in ["temp_set"]:
        set_user_state(msg, "temp")
        await msg.answer("🔥 Вы вошли в меню контроля обогревом:", reply_markup=in_temp_menu)

    elif user_states.get(user_id) in ["set_box"]:
        await msg.answer(text="Назад пути нет, выберите свой бокс:")

    else:
        await msg.answer("!Возврат в главное меню!", reply_markup=main_menu_1)


# обработка текстовой информации
@dp.message()
@admin_panael.check_admins
async def message_handler(msg: Message):
    global water_value_chache
    global day_value_chache
    global sort_name
    global udr_name
    global udr_value_chache
    global date_of_grow

    user_id = str(msg.from_user.id)
    if msg.text is not None:
        if user_states.get(user_id) == "water_set_w":
            try:
                water_value_chache = int(msg.text)
                await msg.answer(f"🌧️ Вы хотите совершить полив на {water_value_chache} литров 🌧️",
                                 reply_markup=check_menu)
            except ValueError:
                await msg.answer("❌ Это не число, повторите еще раз ❌")
            pass

        elif user_states.get(user_id) == "water_set_udr":
            try:
                udr_value_chache = float(msg.text)
                await msg.answer(f"Вы хотите добавить удобрение на {udr_value_chache} литров",
                                 reply_markup=check_menu)
            except ValueError:
                await msg.answer("❌ Это не число, повторите еще раз ❌")
            pass

        elif user_states.get(user_id) == "light_set_day":
            try:
                day_value_chache = int(msg.text)
                await msg.answer(f"🌧️ Вы хотите установить день на {day_value_chache} часов️", reply_markup=check_menu)
            except ValueError:
                await msg.answer("❌ Это не число, повторите еще раз ❌")

        elif user_states.get(user_id) == "name_set":
            sort_name = str(msg.text)
            await msg.answer(f"❓ Вы хотите сменить имя с {cfg.variables.get('name')} на {msg.text}? ❓", reply_markup=check_menu)

        elif user_states.get(user_id) == "udobr_set":
            udr_name = str(msg.text)
            await msg.answer(f"❓ Вы хотите изменить название удобрения с {cfg.variables.get('name_udobr')} на {msg.text}? ❓", reply_markup=check_menu)

        elif user_states.get(user_id) == "set_date":
            date_of_grow = str(msg.text)
            await msg.answer(f"❓ Вы хотите установить дату на {msg.text}? ❓ ", reply_markup=check_menu)

        elif user_states.get(user_id) is None:
            await msg.answer(text="Кажется было произведено обновление на сервере, выполните команду /start")

        else:
            await msg.answer("⚠️ Используйте кнопки для навигации по меню ⚠️")

    else:
        await msg.answer(text="❗ Вы ничего не ввели ❗")
