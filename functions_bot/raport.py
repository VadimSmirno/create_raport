from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.dispatcher.filters import Text
from bot import bot, dp, RaportInfo
from datadase.models import Session, User
from keyboards.keyboard import keyboard_registration
from keyboards.keyboard_by_raport import keyboard_managers_name, \
    keyboard_vacation_part, \
    keyboard_departure, \
    keyboard_material_aid
from logging_dir.log import logger
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from datetime import datetime
from request_api.request_dadata import get_address


async def create_raport_command(message: types.Message):
    telegram_id = message.from_user.id
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if user is not None:
            await message.answer('Собрался в отпуск? Давай напишем рапорт.'
                                 'На чье имя?', reply_markup=keyboard_managers_name)
            await RaportInfo.manager_name.set()
        else:
            await  message.answer('Вам необходимо пройти регистрацию', reply_markup=keyboard_registration)


async def get_manager_name(message: types.CallbackQuery, state: FSMContext):
    manager_name = message.data
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if manager_name.endswith('name'):
        await state.update_data(manager_name=manager_name)
        await message.message.answer('Вид отпуска?', reply_markup=keyboard_vacation_part)
        await RaportInfo.vacation_part.set()
    elif manager_name.endswith('add'):
        await message.message.answer('Фамилия инициалы? Пример: Иванов И.И.')
        await RaportInfo.manager_name.set()


async def get_manager_name_by_hand(message: types.Message, state: FSMContext):
    manager_name = message.text
    logger.info(manager_name)
    await state.update_data(manager_name=manager_name)
    await message.answer('Вид отпуска?', reply_markup=keyboard_vacation_part)
    await RaportInfo.vacation_part.set()


async def get_vacation_part(message: types.CallbackQuery, state: FSMContext):
    vacation_part = message.data
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if vacation_part.startswith('Назад'):
        await message.message.answer('На чье имя?', reply_markup=keyboard_managers_name)
        await RaportInfo.manager_name.set()
    elif vacation_part.endswith('part'):
        await state.update_data(vacation_part=vacation_part[:1])
        res = await state.get_data()
        logger.info(res)
        await message.message.answer('Дата начала отпуска?', reply_markup=await SimpleCalendar().start_calendar())
        await RaportInfo.date_start_vacation.set()


async def get_date_vacation(message: types.CallbackQuery, callback_data: simple_cal_callback, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(message, callback_data)
    res = await state.get_data()
    res = res.get('vacation_part')
    if selected:
        date_start_vacation = date.strftime("%d-%m-%Y")
        await state.update_data(date_start_vacation=date_start_vacation)
        date_object = datetime.strptime(date_start_vacation, '%d-%m-%Y')
        month_number = date_object.month
        if res == '1':
            await message.message.answer('Дата окончания отпуска?',
                                         reply_markup=await SimpleCalendar().start_calendar(month=month_number))
            await RaportInfo.date_finish_vacation.set()
        else:
            date_finish = await state.get_data()
            if 'date_finish_vacation' in date_finish:
                del date_finish['date_finish_vacation']
            await message.message.answer('С выездом?', reply_markup=keyboard_departure)
            await RaportInfo.departure.set()


async def get_date_finish_vacation(message: types.CallbackQuery, callback_data: simple_cal_callback, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(message, callback_data)
    if selected:
        date_finish_vacation = date.strftime("%d-%m-%Y")
        logger.info(date_finish_vacation)
        await state.update_data(date_finish_vacation=date_finish_vacation)
        await message.message.answer('С выездом?', reply_markup=keyboard_departure)
        res = await state.get_data()
        logger.info(res)
        await RaportInfo.departure.set()


async def get_departure(message: types.CallbackQuery, state: FSMContext):
    logger.info(message.data)
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if message.data == 'Назад':
        await message.message.answer('Вид отпуска?', reply_markup=keyboard_vacation_part)
        await RaportInfo.vacation_part.set()
    elif message.data == 'С выездом':
        departure = message.data
        await state.update_data(departure=departure)
        await message.message.answer('Введите населеный пункт, где будете проводить отпуск...')
        await RaportInfo.city.set()
    else:
        departure = message.data
        await state.update_data(departure=departure)
        await message.message.answer('Материальная выплата к отпуску?', reply_markup=keyboard_material_aid)
        await RaportInfo.material_aid.set()



async def get_city(message: types.Message, state: FSMContext):
    city = message.text
    list_city = await get_address(city=city)
    keyboard_city = InlineKeyboardMarkup(row_width=1)
    button_list = [InlineKeyboardButton(
        text=address[0], callback_data=str(index)
    ) for index, address in enumerate(list_city)]
    keyboard_city.add(*button_list)
    await state.update_data(list_city=list_city)
    re = InlineKeyboardButton('Ввести повторно', callback_data='Ввести повторно')
    keyboard_city.row(re)
    await message.answer('Подтвертите', reply_markup=keyboard_city)


async def callback_city(message: types.CallbackQuery, state: FSMContext):
    logger.info(message.data)
    if message.data == 'Ввести повторно':
        await message.message.answer('Напиши подробнее, область + населеный пункт')
        await RaportInfo.city.set()
    else:
        index = int(message.data)
        data = await state.get_data()
        list_city = data.get('list_city')
        await state.update_data(list_city=list_city[index][0])
        data = await state.get_data()
        logger.info(data)

async def get_material_aid(message:types.CallbackQuery, state:FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    material_aid = message.data
    if material_aid == 'Назад':
        await message.message.answer('С выездом?', reply_markup=keyboard_departure)
        await RaportInfo.departure.set()
    else:
        await state.update_data(material_aid=material_aid)
        data = await state.get_data()
        logger.info(data)
        await message.message.answer('Готово, пишу рапорт')



def register_create_raport_command(dp: Dispatcher):
    dp.register_message_handler(create_raport_command, commands=['raport'])
    dp.register_message_handler(get_manager_name_by_hand, state=RaportInfo.manager_name)
    dp.register_message_handler(get_city, state=RaportInfo.city)


def register_create_raport_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(get_manager_name, state=RaportInfo.manager_name)
    dp.register_callback_query_handler(get_vacation_part, state=RaportInfo.vacation_part)
    dp.register_callback_query_handler(get_date_vacation, simple_cal_callback.filter(),
                                       state=RaportInfo.date_start_vacation)
    dp.register_callback_query_handler(get_date_finish_vacation, simple_cal_callback.filter(),
                                       state=RaportInfo.date_finish_vacation)
    dp.register_callback_query_handler(get_departure, state=RaportInfo.departure)
    dp.register_callback_query_handler(callback_city, state=RaportInfo.city)
    dp.register_callback_query_handler(get_material_aid, state=RaportInfo.material_aid)
