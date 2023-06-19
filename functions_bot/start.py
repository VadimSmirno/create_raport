from aiogram import types
from aiogram import Dispatcher
from bot import bot, dp
from datadase.models import Session, User
from keyboards.keyboard import keyboard_registration
from Middleware.throttling import rate_limit


start_message = 'Приветствую тебя, '


@rate_limit(limit=3, key='/start')
async def start_command(message:types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, f'{start_message} {message.chat.first_name} {message.chat.last_name}')
    telegram_id = message.from_user.id
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user is not None:
            await bot.send_message(chat_id, 'Написать рапорт. /raport')
        else:
            await  message.answer('Вам необходимо пройти регистрацию', reply_markup=keyboard_registration)



def register_start_command(dp:Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])