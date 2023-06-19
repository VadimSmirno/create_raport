from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import os
from aiogram.dispatcher.filters.state import State, StatesGroup

load_dotenv()
token = os.getenv('token_bot')
token_dadata = os.getenv('token_dadata')
secret = os.getenv('secret')
telegram_id = os.getenv('telegram_id')

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserData(StatesGroup):
    first_name = State()
    last_name = State()
    surname = State()
    rank = State()
    job_title = State()  # должность
    part_number = State()  # номер часит
    telephone_number = State()
    service_start_date = State()  # начало службы


class UserEditData(StatesGroup):
    rank = State()
    job_title = State()
    part_number = State()
    telephone_number = State()
    service_start_date = State()

class RaportInfo(StatesGroup):
    manager_name = State()
    rank = State()
    vacation_part = State()
    date_start_vacation = State()
    date_finish_vacation = State()
    departure = State()
    city = State()
    material_aid = State()
    itinerary_city = State()
    kind_of_transport = State()
    intermediate_city = State()
    yes_or_no = State()
    family = State()
    family_member = State()
