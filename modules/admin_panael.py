import os

from aiogram.types import Message
from functools import wraps


admins = os.getenv("admins")


# Функция-декоратор для проверки администраторских прав
def check_admins(func):
    @wraps(func)
    async def wrapper(mes: Message, *args, **kwargs):
        if str(mes.from_user.id) not in admins:
            await mes.answer("У вас нет прав на выполнение этой команды. Обратитесь к разработчику!")
            return
        return await func(mes, *args, **kwargs)
    return wrapper
