import os
import asyncio
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from aiogram import types
import misc
from modules.temp_module import get_mi_sensor_data
from CONSTANTS import Box_device_address, Room_device_address

# Глобальные переменные для хранения данных
daily_data = []

REPORTS_DIR = "daily_buffer"

async def send_message_func(chat_id):
    t, h, voltage = get_mi_sensor_data(Box_device_address)
    t2, h2, voltage2 = get_mi_sensor_data(Room_device_address)
    mid_t = (t+t2)/2
    daily_data.append((datetime.now(), t, t2))  # Сохранение данных с меткой времени
    await misc.bot.send_message(chat_id=chat_id,
                           text=f"Температура: {t}°C, Влажность: {h}%\nТемпература2: {t2}°C, Влажность2: {h2}%\nСредняя темп.: {mid_t}")


def create_plot():
    times = [data[0] for data in daily_data]
    temps1 = [data[1] for data in daily_data]
    temps2 = [data[2] for data in daily_data]

    # График для Temperature1
    plt.figure(figsize=(10, 6))
    plt.plot(times, temps1, label='Temperature1 (°C)', color='r')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Time')
    plt.legend()
    plt.title('Temperature1 Over Time')
    plt.tight_layout()
    plot_filename1 = os.path.join(REPORTS_DIR, f"temperature1_plot_{datetime.now().strftime('%Y%m%d')}.png")
    plt.savefig(plot_filename1)
    plt.close()

    # График для Temperature2
    plt.figure(figsize=(10, 6))
    plt.plot(times, temps2, label='Temperature2 (°C)', color='b')
    plt.ylabel('Temperature (°C)')
    plt.xlabel('Time')
    plt.legend()
    plt.title('Temperature2 Over Time')
    plt.tight_layout()
    plot_filename2 = os.path.join(REPORTS_DIR, f"temperature2_plot_{datetime.now().strftime('%Y%m%d')}.png")
    plt.savefig(plot_filename2)
    plt.close()

    return plot_filename1, plot_filename2


async def generate_daily_report(chat_id):
    # Создание графика
    plot_filename1, plot_filename2 = create_plot()

    # Отправка ежедневного графика
    await misc.bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(plot_filename1))
    await misc.bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(plot_filename2))
    # Сброс данных
    daily_data.clear()

    os.remove(plot_filename1)
    os.remove(plot_filename2)


async def daily_report_task():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)

        if now >= target_time:
            # Если текущее время уже прошло 22:00, то следующая цель - 22:00 следующего дня
            target_time += timedelta(days=1)

        await asyncio.sleep((target_time - now).total_seconds())
        await generate_daily_report(chat_id="5848061277")


