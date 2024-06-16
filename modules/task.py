from datetime import datetime, timedelta
import misc
import asyncio
from modules.temp_module import get_mi_sensor_data
from CONSTANTS import Box_device_address, Room_device_address

# Функция, которая отправляет сообщение в N часов каждый день
async def send_message_at(hour, minutes, text, chat_id):
    # 'ВРЕМЯ' - hours, minutes
    while True:
        # Получаем текущее время
        now = datetime.now()

        # Вычисляем время до 'ВРЕМЯ' сегодня
        target_time = datetime(now.year, now.month, now.day, hour, minutes)
        if now > target_time:
            # Если уже прошло 'ВРЕМЯ' сегодня, переходим к 'ВРЕМЯ' следующего дня
            target_time += timedelta(days=1)

        # Ожидаем до момента отправки сообщения
        await asyncio.sleep((target_time - now).total_seconds())

        # Отправляем сообщение
        await misc.bot.send_message(chat_id=chat_id,
                                    text=text)


async def send_message_func(chat_id):
    t, h, voltage = get_mi_sensor_data(Box_device_address)
    t2, h2, voltage2 = get_mi_sensor_data(Room_device_address)
    await misc.bot.send_message(chat_id=chat_id,
                                text=f"Температура: {t}.C,  Влажность: {h}\nТемпература2: {t2}.C,  Влажность2: {h2}")

    pass