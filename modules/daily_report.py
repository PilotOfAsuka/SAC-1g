import os
import asyncio
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from aiogram import types
import misc
from modules.temp_module import get_mi_sensor_data

# Глобальные переменные для хранения данных
daily_data = []

REPORTS_DIR = "daily_buffer"

async def send_message_func(chat_id):
    t, h, voltage = get_mi_sensor_data("Box_device_address")
    t2, h2, voltage2 = get_mi_sensor_data("Room_device_address")
    daily_data.append((datetime.now(), t, h, t2, h2))  # Сохранение данных с меткой времени
    await misc.bot.send_message(chat_id=chat_id,
                           text=f"Температура: {t}°C, Влажность: {h}%\nТемпература2: {t2}°C, Влажность2: {h2}%")


def create_plot():
    times = [data[0] for data in daily_data]
    temps1 = [data[1] for data in daily_data]
    hums1 = [data[2] for data in daily_data]
    temps2 = [data[3] for data in daily_data]
    hums2 = [data[4] for data in daily_data]

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(times, temps1, label='Temperature1 (°C)', color='r')
    plt.plot(times, temps2, label='Temperature2 (°C)', color='b')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.title('Temperature and Humidity Over Time')

    plt.subplot(2, 1, 2)
    plt.plot(times, hums1, label='Humidity1 (%)', color='r')
    plt.plot(times, hums2, label='Humidity2 (%)', color='b')
    plt.ylabel('Humidity (%)')
    plt.xlabel('Time')
    plt.legend()

    plt.tight_layout()

    plot_filename = os.path.join(REPORTS_DIR, f"daily_plot_{datetime.now().strftime('%Y%m%d')}.png")
    plt.savefig(plot_filename)
    plt.close()

    return plot_filename


async def generate_daily_report(chat_id):
    # Создание графика
    plot_filename = create_plot()

    # Отправка таблицы
    await misc.bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(plot_filename))

    # Сброс данных
    daily_data.clear()

    os.remove(plot_filename)


async def daily_report_task():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)

        if now >= target_time:
            # Если текущее время уже прошло 22:00, то следующая цель - 22:00 следующего дня
            target_time += timedelta(days=1)

        await asyncio.sleep((target_time - now).total_seconds())
        await generate_daily_report(chat_id="5848061277")


