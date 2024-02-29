from aiogram.types import Message
from functools import wraps


admins = [
    5848061277,  # Илья
    5611067209,  # Макс

]


# Функция-декоратор для проверки администраторских прав
def check_admins(func):
    @wraps(func)
    async def wrapper(mes: Message, *args, **kwargs):
        if mes.from_user.id not in admins:
            await mes.answer("У вас нет прав на выполнение этой команды. Обратитесь к разработчику!")
            return
        return await func(mes, *args, **kwargs)
    return wrapper
