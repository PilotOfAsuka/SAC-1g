import misc
import handlers
import asyncio
from modules.task import send_message_fumc
from func import get_time_text

handlers = handlers

ls = "5848061277"

async def on_startup():
    await misc.bot.send_message(chat_id=ls, text=f"{get_time_text()} - Сервер упал, но снова поднялся")


async def main():
    global message_tasks

    while True:
        # Отменяем предыдущие задачи
        for task in message_tasks:
            print(f"{task}: Удалена!")
            task.cancel()


        message_tasks = [asyncio.create_task(send_message_fumc(chat_id=ls)),]

        print(f"{get_time_text(date=True)}: Созданы новые задачи")
        # Ждем один день перед повторным обновлением задач
        await asyncio.sleep(60*60)

async def startup_task():
    # Регистрация функции on_startup
    misc.dp.startup.register(on_startup)

    # Удаление вебхука и запуск long-polling
    await misc.bot.delete_webhook(drop_pending_updates=True)
    await misc.dp.start_polling(misc.bot, allowed_updates=misc.dp.resolve_used_update_types())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    message_tasks = []

    try:
        loop.run_until_complete(asyncio.gather(main(), startup_task()))

    finally:
        loop.close()