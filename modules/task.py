from datetime import datetime, timedelta
import misc
import asyncio
from modules.temp_module import get_mi_sensor_data

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

async def send_message_fumc(chat_id):
    t, h, voltage = get_mi_sensor_data()
    await misc.bot.send_message(chat_id=chat_id,
                                text=f"Температура: {t}.C,  Влажность: {h}")
    while True:
        # Ожидаем до момента отправки сообщения
        await asyncio.sleep((60*60) * 2)

        # Отправляем сообщение
        await misc.bot.send_message(chat_id=chat_id,
                                    text=f"Температура: {t}.C, Влажность: {h}")

    pass