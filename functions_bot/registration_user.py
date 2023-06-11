import datetime
from logging_dir.log import logger
from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram_calendar import DialogCalendar, SimpleCalendar, simple_cal_callback, dialog_cal_callback
from bot import UserData
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.types import ReplyKeyboardRemove
from keyboards.keyboard import keyboard_rang, \
    keyboard_status_rang, \
    keyboard_rag_officer, \
    keyboard_job_title, \
    keyboard_part_number
from datadase.request_database import writing_information_to_the_database


async def registration(message: types.Message):
    await message.answer('Ваше имя?', reply_markup=ReplyKeyboardRemove())
    await UserData.first_name.set()


async def get_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer('Ваша фамилия?')
    await UserData.last_name.set()


async def get_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer('Отчество?')
    await UserData.surname.set()

async def get_surname(message: types.Message, state: FSMContext):
    some_data = await state.get_data()
    if not some_data.get('surname'):
        surname = message.text
        await state.update_data(surname=surname)
    await message.answer('Номер телефона?')
    await UserData.telephone_number.set()

async def get_telephone_number(message: types.Message, state: FSMContext):
    some_data = await state.get_data()
    logger.info(some_data)
    if not some_data.get('telephone_number'):
        telephone_number = message.text
        await state.update_data(telephone_number=telephone_number)
    await message.answer('Состав?', reply_markup=keyboard_status_rang)


async def get_status_rang(message: types.CallbackQuery, state: FSMContext):
    number_group = message.data
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if number_group == 'group_1':
        await state.update_data(number_group=number_group)
        await  message.message.answer('Звание?', reply_markup=keyboard_rang)
        await UserData.rank.set()
    elif number_group == 'group_2':
        await state.update_data(number_group=number_group)
        await  message.message.answer('Звание?', reply_markup=keyboard_rag_officer)
        await UserData.rank.set()
    elif number_group == 'Назад':
        await state.finish()
        await registration(message.message)


async def get_rang(message: types.CallbackQuery, state: FSMContext):
    rang = message.data[:-5]
    logger.info(rang)
    current_state = await state.get_state()
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if rang == 'Назад':
        await get_telephone_number(message.message, state)
        await UserData.telephone_number.set()
    elif current_state != 'UserData:job_title':
        await state.update_data(rang=rang)
        await message.message.answer('Должность', reply_markup=keyboard_job_title)
        await UserData.job_title.set()
    else:
        await message.message.answer('Должность', reply_markup=keyboard_job_title)
        await UserData.job_title.set()


async def get_job_title(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    data = await state.get_data()
    status_group = data.get('number_group')
    if message.data.startswith('Назад') and status_group == 'group_1':
        await  message.message.answer('Звание?', reply_markup=keyboard_rang)
        await UserData.rank.set()
    elif message.data.startswith('Назад') and status_group == 'group_2':
        await  message.message.answer('Звание?', reply_markup=keyboard_rag_officer)
        await UserData.rank.set()
    else:
        job_title = message.data[:-4]
        if job_title == 'Старший инструктор':
            await state.update_data(job_title = 'Старший инструктор по вождению пожарной мшины - водитель')
        else:
            await state.update_data(job_title=job_title)
            await message.message.answer('Номер части', reply_markup=keyboard_part_number)
            await UserData.part_number.set()


async def get_part_number(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    part_number = message.data
    if part_number.startswith('Назад'):
        await UserData.job_title.set()
        await get_rang(message, state)
    else:
        part_number = int(part_number[-1:])
        await state.update_data(part_number=part_number)
        year = datetime.datetime.now().year - 2
        await message.message.answer('Дата начала службы?', reply_markup=await DialogCalendar().start_calendar(year=year))
        await UserData.service_start_date.set()


async def get_service_start_date(callback_query: types.CallbackQuery, callback_data: dict, state:FSMContext):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        service_start_date = date.strftime("%d-%m-%Y")
        await  state.update_data(service_start_date=service_start_date)
        data = await state.get_data()
        await callback_query.message.answer('Регистрация прошла успешно!')
        telegram_id = callback_query.from_user.id
        writing_information_to_the_database(telegram_id=telegram_id, data=data)
        await state.finish()

def register_registration_command(dp: Dispatcher):
    dp.register_message_handler(registration, Text(equals='Регистрация'))
    dp.register_message_handler(get_first_name, state=UserData.first_name)
    dp.register_message_handler(get_last_name, state=UserData.last_name)
    dp.register_message_handler(get_surname, state=UserData.surname)
    dp.register_message_handler(get_telephone_number, state=UserData.telephone_number)


def regiser_callbak_query(dp: Dispatcher):
    dp.register_callback_query_handler(get_status_rang, Text(startswith='group'))
    dp.register_callback_query_handler(get_status_rang, Text(endswith='Назад'), state=UserData.telephone_number)
    dp.register_callback_query_handler(get_status_rang, Text(startswith='group'), state=UserData.telephone_number)
    dp.register_callback_query_handler(get_rang, Text(endswith='rang'), state=UserData.rank)
    dp.register_callback_query_handler(get_job_title, Text(endswith='job'), state=UserData.job_title)
    dp.register_callback_query_handler(get_part_number, state=UserData.part_number)
    dp.register_callback_query_handler(get_service_start_date, dialog_cal_callback.filter(), state=UserData.service_start_date)

