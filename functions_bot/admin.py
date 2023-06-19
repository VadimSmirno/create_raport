from aiogram import types
from aiogram import Dispatcher
from datadase.models import Session, User
from bot import telegram_id


async def count_user(message: types.Message):
    user_id = message.from_user.id
    if user_id == int(telegram_id):
        with Session() as session:
            count_user = session.query(User).count()
            await message.answer(f'Зарегистрировано {count_user} пользователей')
    else:
        await message.answer('На выполнение этой команды у вас недостаточно прав')
    await message.delete()


def register_count_user(dp: Dispatcher):
    dp.register_message_handler(count_user, commands=['count'])
