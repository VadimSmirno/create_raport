import datetime
from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram_calendar import DialogCalendar, dialog_cal_callback

from bot import bot, dp, UserData, UserEditData
from datadase.models import Session, User
from datadase.request_database import update_user_data_in_database, update_user_telephone_number
from keyboards.keyboard import keyboard_registration
from Middleware.throttling import rate_limit
from keyboards.keyboard import keyboard_edit, \
    keyboard_status_rang,\
    keyboard_job_title,\
    keyboard_part_number, \
    keyboard_rang,\
    keyboard_rag_officer
from logging_dir.log import logger


@rate_limit(limit=3, key='/edit')
async def edit_profile_command(message: types.Message):
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user is not None:
            await message.answer('Отредактировать профиль', reply_markup=keyboard_edit)
        else:
            await  message.answer('Вам необходимо пройти регистрацию', reply_markup=keyboard_registration)


async def edit_button_press(message: types.CallbackQuery):
    if message.data.startswith('Закрыть'):
        await message.message.delete()
        return
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    res = message.data
    if res.startswith('звание'):
        await message.message.answer('Состав?', reply_markup=keyboard_status_rang)
        await UserEditData.rank.set()
    elif res.startswith('должность'):
        await message.message.answer('Должность?', reply_markup=keyboard_job_title)
        await UserEditData.job_title.set()
    elif res.startswith('номер_телефона'):
        await message.message.answer('Новый номер телефона?')
        await  UserEditData.telephone_number.set()
    elif res.startswith('дата_начала_'):
        year = datetime.datetime.now().year - 2
        await message.message.answer('Дата начала службы?',
                                     reply_markup=await DialogCalendar().start_calendar(year=year))
        await UserEditData.service_start_date.set()

    else:
        await message.message.answer('Номер части?', reply_markup=keyboard_part_number)
        await UserEditData.part_number.set()

async def update_telephone_number(message:types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    telephone_number = message.text
    update_user_telephone_number(telegram_id=telegram_id, telephone_number=telephone_number)
    await state.finish()
    await message.answer(f'Номер телефона обновлен на {telephone_number}')

async def edit_runk_job_part(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    result = message.data
    await state.finish()
    telegram_id = message.from_user.id
    if result.startswith('Назад'):
        await message.message.answer('Отредактировать профиль', reply_markup=keyboard_edit)
    elif result == 'group_1':
        await message.message.answer('Звание?', reply_markup=keyboard_rang)
        await UserEditData.rank.set()
    elif result == 'group_2':
        await message.message.answer('Звание?', reply_markup=keyboard_rag_officer)
        await UserEditData.rank.set()
    elif result.endswith('_job'):
        job_title = result[:-4]
        update_user_data_in_database(data=job_title,telegram_id=telegram_id, column_name='job')
        await state.finish()
        await message.message.answer(f'Должность обновлена на {job_title}')
    elif result.endswith('rang'):
        rang=result[:-5]
        logger.info(rang)
        update_user_data_in_database(data=rang,telegram_id=telegram_id, column_name='rang')
        await state.finish()
        await message.message.answer(f'Звание обновлено на {rang}')
    elif result.startswith('ПСЧ'):
        part_number = int(result[-1])
        update_user_data_in_database(data=part_number,telegram_id=telegram_id, column_name='part_number')
        await state.finish()
        await message.message.answer(f'Часть обновлена {result}')
    else:
        logger.info('Вольнонаемные')
        await state.finish()

async def edit_service_start_date(message:types.CallbackQuery, callback_data: dialog_cal_callback, state:FSMContext):
    selected, date = await DialogCalendar().process_selection(message, callback_data)
    if selected:
        telegram_id = message.from_user.id
        service_start_date = date.strftime("%d-%m-%Y")
        logger.info(service_start_date)
        update_user_data_in_database(telegram_id=telegram_id,column_name='date_start', data=service_start_date)
        await state.finish()
        await message.message.answer(f'Дата начала служба обновлена на {service_start_date}')
        try:
            await message.message.delete()
        except MessageToDeleteNotFound as err:
            logger.error(err)



def register_edit_command(dp: Dispatcher):
    dp.register_message_handler(edit_profile_command, commands=['edit'])
    dp.register_message_handler(update_telephone_number, state=UserEditData.telephone_number)


def register_edit_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(edit_service_start_date, dialog_cal_callback.filter(),
                                       state=UserEditData.service_start_date)
    dp.register_callback_query_handler(edit_button_press, Text(endswith='edit'))
    dp.register_callback_query_handler(edit_runk_job_part, state=UserEditData)
