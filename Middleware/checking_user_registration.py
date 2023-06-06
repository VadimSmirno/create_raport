from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from datadase.models import Session, User
from keyboards.keyboard import keyboard_registration



class RegistrationMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        command = message.text
        if command == '/start':
            await  message.answer('Вам необходимо пройти регистрацию', reply_markup=keyboard_registration)
        # Проверяем, зарегистрирован ли пользователь
        elif not is_user_registered(message.from_user.id):
            # Если пользователь не зарегистрирован, отменяем обработку сообщения
            raise CancelHandler()


# Пример функции для проверки регистрации пользователя
def is_user_registered(user_id):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=user_id).first()
        return user