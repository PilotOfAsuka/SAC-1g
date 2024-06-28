import asyncio
from datetime import datetime, timedelta
import misc
from modules.temp_module import get_mi_sensor_data
from CONSTANTS import Box_device_address, Room_device_address


# Глобальные переменные для хранения данных
daily_data_temp= []

REPORTS_DIR = "daily_buffer"

async def send_message_func(chat_id):
    t, h, voltage = get_mi_sensor_data(Box_device_address)
    t2, h2, voltage2 = get_mi_sensor_data(Room_device_address)
    mid_t = (t+t2)/2
    daily_data_temp.append(t)
    daily_data_temp.append(t2)
    await misc.bot.send_message(chat_id=chat_id,
                           text=f"Температура: {t}°C, Влажность: {h}%\nТемпература2: {t2}°C, Влажность2: {h2}%\nСредняя темп.: {mid_t}")


async def generate_daily_report(chat_id):
    # Удаляем все нулевые значения из списка
    cleaned_temperatures = [temp for temp in daily_data_temp if temp != 0]

    # Проверяем, что список не пустой
    if len(cleaned_temperatures) == 0:
        cleaned_temperatures = [1, 1]

    # Вычисляем среднее значение
    average_temperature = sum(cleaned_temperatures) / len(cleaned_temperatures)

    # Отправка ежедневного среднего значения температуры за день
    await misc.bot.send_message(chat_id=chat_id, text=f"Средняя температура за день: {average_temperature}")

    # Сброс данных
    daily_data_temp.clear()

async def daily_report_task():
    while True:
        now = datetime.now()
        target_time = now.replace(hour=22, minute=0, second=0, microsecond=0)

        if now >= target_time:
            # Если текущее время уже прошло 22:00, то следующая цель - 22:00 следующего дня
            target_time += timedelta(days=1)

        await asyncio.sleep((target_time - now).total_seconds())
        await generate_daily_report(chat_id="5848061277")


async def run_task(interval, unit='hours', action=None):
    if action is None:
        raise ValueError("Необходимо передать функцию для выполнения.")

    while True:
        await action()  # Выполняем переданную функцию
        now = datetime.now()  # Получаем текущее время

        # Определяем следующий запуск в зависимости от указанного интервала и единицы времени
        if unit == 'hours':
            next_run = now + timedelta(hours=interval)
        elif unit == 'minutes':
            next_run = now + timedelta(minutes=interval)
        elif unit == 'seconds':
            next_run = now + timedelta(seconds=interval)
        else:
            raise ValueError("Недопустимая единица времени. Используйте 'hours', 'minutes' или 'seconds'.")

        next_run = next_run.replace(microsecond=0)  # Обнуляем миллисекунды для точности
        sleep_duration = (next_run - now).total_seconds()

        await asyncio.sleep(sleep_duration)  # Засыпаем до следующего запуска

