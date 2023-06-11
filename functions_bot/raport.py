import os

from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageToDeleteNotFound
from bot import bot, dp, RaportInfo
from datadase.models import Session, User
from datadase.request_database import update_user_add_raport_info_json
from keyboards.keyboard import keyboard_registration
from keyboards.keyboard_by_raport import keyboard_managers_name, \
    keyboard_vacation_part, \
    keyboard_departure, \
    keyboard_material_aid, \
    keyboard_kind_of_transport, \
    keyboard_yes_or_no, \
    keyboard_family, \
    keyboard_rung
from logging_dir.log import logger
from aiogram_calendar import SimpleCalendar, simple_cal_callback
from datetime import datetime
from request_api.request_dadata import get_address, get_itinerary
from document_generation.document import generation_raport
import json


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
        await state.update_data(manager_name=manager_name[:-5])
        await message.message.answer('Звание руководителя?', reply_markup=keyboard_rung)
        await RaportInfo.rank.set()
    elif manager_name.endswith('add'):
        await message.message.answer('Фамилия инициалы? Пример: Иванову И.И.')
        await RaportInfo.manager_name.set()

async def get_rung(message: types.CallbackQuery, state:FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    rung = message.data
    await state.update_data(rung=rung[:-5])
    await message.message.answer('Вид отпуска?', reply_markup=keyboard_vacation_part)
    await RaportInfo.vacation_part.set()


async def get_manager_name_by_hand(message: types.Message, state: FSMContext):
    manager_name = message.text
    logger.info(manager_name)
    await state.update_data(manager_name=manager_name)
    await message.answer('Звание руководителя?', reply_markup=keyboard_rung)
    await RaportInfo.rank.set()


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
        await message.message.answer('Дата начала отпуска?', reply_markup=await SimpleCalendar().start_calendar())
        await RaportInfo.date_start_vacation.set()


async def get_date_vacation(message: types.CallbackQuery, callback_data: simple_cal_callback, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(message, callback_data)
    res = await state.get_data()
    res = res.get('vacation_part')
    if selected:
        try:
            await message.message.delete()
        except MessageToDeleteNotFound as err:
            logger.error(err)
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
        try:
            await message.message.delete()
        except MessageToDeleteNotFound as err:
            logger.error(err)
        date_finish_vacation = date.strftime("%d-%m-%Y")
        await state.update_data(date_finish_vacation=date_finish_vacation)
        await message.message.answer('С выездом?', reply_markup=keyboard_departure)
        await RaportInfo.departure.set()


async def get_departure(message: types.CallbackQuery, state: FSMContext):
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
        sent_message = await message.message.answer('Введите населеный пункт, где будете проводить отпуск...')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.city.set()
    else:
        departure = message.data
        await state.update_data(departure=departure)
        await message.message.answer('Материальная выплата к отпуску?', reply_markup=keyboard_material_aid)
        await RaportInfo.material_aid.set()


async def get_city(message: types.Message, state: FSMContext):
    message_id = await state.get_data()
    message_id_result = message_id.get('message_id')
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message_id_result)
    except MessageToDeleteNotFound as err:
        logger.error(err)
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
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if message.data == 'Ввести повторно':
        sent_message = await message.message.answer('Напиши подробнее, область + населеный пункт')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.city.set()
    else:
        index = int(message.data)
        data = await state.get_data()
        list_city = data.get('list_city')
        await state.update_data(list_city=list_city[index][0])
        data = await state.get_data()
        sent_message = await message.message.answer(
            'Маршрут следования от города Вологда до города ...(введите название города)?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.itinerary_city.set()


async def itinerary(message: types.Message, state: FSMContext):
    message_id = await state.get_data()
    message_id_result = message_id.get('message_id')
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message_id_result)
    except MessageToDeleteNotFound as err:
        logger.error(err)
    city = message.text
    itinerary = await get_itinerary(city=city)
    keyboard_city = InlineKeyboardMarkup(row_width=1)
    button_list = [InlineKeyboardButton(
        text=address, callback_data=address
    ) for address in itinerary]
    keyboard_city.add(*button_list)
    re = InlineKeyboardButton('Ввести повторно', callback_data='Ввести повторно')
    keyboard_city.row(re)
    await message.answer('Подтвертите', reply_markup=keyboard_city)


async def itinerary_callback(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    itinerary = message.data
    if message.data == 'Ввести повторно':
        sent_message = await message.message.answer('Маршрут следования от города Вологда до города ...'
                                                    '(Если не нашел нужный город, напиши подробнее '
                                                    'Например: Вологодская область Никольск)?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.itinerary_city.set()
    else:
        data = await state.get_data()
        if not data.get('itinerary'):
            dct = {itinerary: ''}
            await state.update_data(itinerary=dct)
        else:
            data = await state.get_data()
            data_dct: dict = data['itinerary']
            data_dct.update({itinerary: ''})
            await state.update_data(itinerary=data_dct)
        await state.update_data(city=itinerary)
        await message.message.answer(f'Вид транспорта до {itinerary}?', reply_markup=keyboard_kind_of_transport)
        await RaportInfo.kind_of_transport.set()


async def get_kind_of_transport(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    city = await state.get_data()
    city_str = city['city']
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    city['itinerary'][city_str] = message.data
    # city.pop('city', 'message_id')
    # await state.finish()
    await state.update_data(city)
    await message.message.answer('Добавить промежуточный город?', reply_markup=keyboard_yes_or_no)
    await RaportInfo.intermediate_city.set()


async def add_intermediate_city(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if message.data == 'да':
        data: dict = await state.get_data()
        city = data.get('city')
        sent_message = await message.message.answer(f'От города {city} куда? Введите промежуточный населенный пункт...')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.itinerary_city.set()
    else:
        await message.message.answer('Совместно с тобой кто-нибудь едет?', reply_markup=keyboard_yes_or_no)
        await RaportInfo.yes_or_no.set()


async def check_companions_for_vacation(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    if message.data == 'да':
        await message.message.answer('Кто поедет?', reply_markup=keyboard_family)
        await RaportInfo.family.set()
    else:
        await message.message.answer('Материальная выплата к отпуску?', reply_markup=keyboard_material_aid)
        await RaportInfo.material_aid.set()


async def get_family(message: types.CallbackQuery, state: FSMContext):
    try:
        await message.message.delete()
    except MessageToDeleteNotFound as err:
        logger.error(err)
    family_member = message.data
    await state.update_data(family_member=family_member)
    if family_member.startswith('Жена'):
        sent_message = await message.message.answer('Введите фамилию имя отчество жены?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.family_member.set()
    elif family_member.startswith('Муж'):
        sent_message = await message.message.answer('Введите фамилию имя отчество мужа?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.family_member.set()
    elif family_member.startswith('Дочь'):
        sent_message = await message.message.answer('Введите фамилию имя дочери?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.family_member.set()
    else:
        sent_message = await message.message.answer('Введите фамилию имя сына?')
        message_id = sent_message.message_id
        await state.update_data(message_id=message_id)
        await RaportInfo.family_member.set()


async def process_family_member_selection(message: types.Message, state: FSMContext):
    message_id = await state.get_data()
    message_id_result = message_id.get('message_id')
    try:
        await message.delete()
        await bot.delete_message(message.chat.id, message_id_result)
    except MessageToDeleteNotFound as err:
        logger.error(err)
    name = message.text
    data = await state.get_data()
    family_member = data.get('family_member')
    family_member = family_member.split()
    logger.info(family_member)
    await state.update_data(**{family_member[1]:name})
    await message.answer('Еще кто-нибудь едет?', reply_markup=keyboard_yes_or_no)
    await RaportInfo.yes_or_no.set()


async def get_material_aid(message: types.CallbackQuery, state: FSMContext):
    telegram_id = message.from_user.id
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
        await message.message.answer('Готово, пишу рапорт')
        data = await state.get_data()
        if data.get('city') and data.get('family_member') and data.get('message_id'):
            data.pop('city')
            data.pop('message_id')
            data.pop('family_member')
            await state.finish()
            await state.update_data(data)
        data = await state.get_data()
        json_data = json.dumps(data)
        update_user_add_raport_info_json(telegram_id=telegram_id, data=json_data)
        await state.finish()
        name_file = generation_raport(telegram_id=telegram_id)
        with open(f'document_generation/{name_file}', 'rb') as file:
            await bot.send_document(message.message.chat.id, file)
        os.remove(f'document_generation/{name_file}')
        with open(f'document_generation/ofont.ru_Denistina.ttf', 'rb') as file:
            await bot.send_document(message.message.chat.id, file, caption='Файл для установки шрифта')

       

def register_create_raport_command(dp: Dispatcher):
    dp.register_message_handler(create_raport_command, commands=['raport'])
    dp.register_message_handler(get_manager_name_by_hand, state=RaportInfo.manager_name)
    dp.register_message_handler(get_city, state=RaportInfo.city)
    dp.register_message_handler(itinerary, state=RaportInfo.itinerary_city)
    dp.register_message_handler(process_family_member_selection, state=RaportInfo.family_member)


def register_create_raport_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(get_manager_name, state=RaportInfo.manager_name)
    dp.register_callback_query_handler(get_rung, state=RaportInfo.rank)
    dp.register_callback_query_handler(get_vacation_part, state=RaportInfo.vacation_part)
    dp.register_callback_query_handler(get_date_vacation, simple_cal_callback.filter(),
                                       state=RaportInfo.date_start_vacation)
    dp.register_callback_query_handler(get_date_finish_vacation, simple_cal_callback.filter(),
                                       state=RaportInfo.date_finish_vacation)
    dp.register_callback_query_handler(get_departure, state=RaportInfo.departure)
    dp.register_callback_query_handler(callback_city, state=RaportInfo.city)
    dp.register_callback_query_handler(get_material_aid, state=RaportInfo.material_aid)
    dp.register_callback_query_handler(itinerary_callback, state=RaportInfo.itinerary_city)
    dp.register_callback_query_handler(get_kind_of_transport, state=RaportInfo.kind_of_transport)
    dp.register_callback_query_handler(add_intermediate_city, state=RaportInfo.intermediate_city)
    dp.register_callback_query_handler(check_companions_for_vacation, state=RaportInfo.yes_or_no)
    dp.register_callback_query_handler(get_family, state=RaportInfo.family)
