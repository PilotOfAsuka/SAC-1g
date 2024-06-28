import misc
import handlers
import asyncio
from modules.daily_report import send_message_func, daily_report_task, run_task
from func import get_time_text

handlers = handlers

ls = "5848061277"

async def on_startup():
    await misc.bot.send_message(chat_id=ls, text=f"{get_time_text()} - Сервер упал, но снова поднялся")



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
        loop.run_until_complete(asyncio.gather(startup_task(), run_task(interval=1, action=send_message_func, chat_id=ls), daily_report_task()))

    finally:
        loop.close()