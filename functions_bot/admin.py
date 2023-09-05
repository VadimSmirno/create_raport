import os
from aiogram import types
from aiogram import Dispatcher
from datadase.models import Session, User
from bot import telegram_id
from logging_dir.log import logger


async def count_user(message: types.Message):
    user_id = message.from_user.id
    if user_id == int(telegram_id):
        with Session() as session:
            count_user = session.query(User).count()
            await message.answer(f'Зарегистрировано {count_user} пользователей')
    else:
        await message.answer('На выполнение этой команды у вас недостаточно прав')
    await message.delete()


async def user_limit(message: types.Message):
    user_id = message.from_user.id
    if user_id == int(telegram_id):
        with Session() as session:
            user_info = session.query(User.last_name, User.first_name, User.surname, User.part_number).order_by(
                User.id.desc()).limit(5).all()
            logger.info(user_info)
            user_list_str = "\n".join(
                [f" {info.last_name} {info.first_name} {info.surname} ПСЧ-{info.part_number}" for info in user_info])

            await message.answer(f"Список пользователей:\n{user_list_str}")


async def log(message: types.Message):
    user_id = message.from_user.id
    if user_id == int(telegram_id):
        log_file = os.path.join("logging_dir/bot.log")
        try:
            await message.answer_document(types.InputFile(log_file), caption="Логи бота")
        except Exception as e:
            await message.answer(f"Произошла ошибка при отправке логов: {e}")


def register_count_user(dp: Dispatcher):
    dp.register_message_handler(log,commands=['log'])
    dp.register_message_handler(count_user, commands=['count'])
    dp.register_message_handler(user_limit, commands=['users'])
