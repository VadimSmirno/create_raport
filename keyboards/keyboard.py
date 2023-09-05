from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ParseMode

registrations_button = KeyboardButton('Регистрация')
info_button = KeyboardButton('Информация')
keyboard_registration = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(registrations_button)

keyboard_status_rang = InlineKeyboardMarkup(row_width=2)
group_1 = InlineKeyboardButton('Рядовой и сержанский состав', callback_data='group_1')
group_2 = InlineKeyboardButton('Офицерский состав', callback_data='group_2')
group_3 = InlineKeyboardButton('Вольнонаемный', callback_data='group_3')
back_button = InlineKeyboardButton('Назад', callback_data='Назад')
back_button.text = '⬅️ Назад'
keyboard_status_rang.add(
    group_1,
    group_2,
    # group_3
)
keyboard_status_rang.row(back_button)

keyboard_rang = InlineKeyboardMarkup(row_width=2)
private_button = InlineKeyboardButton('Рядовой', callback_data='рядовой rang')
junior_sergeant_button = InlineKeyboardButton('Младший сержант', callback_data='младший сержант rang')
sergeant_button = InlineKeyboardButton('Сержант', callback_data='сержант rang')
senior_sergeant_button = InlineKeyboardButton('Старший сержант', callback_data='старший сержант rang')
foreman_button = InlineKeyboardButton('Старшина', callback_data='старшина rang')
warrant_officer_button = InlineKeyboardButton('Прапоршик', callback_data='прапорщик rang')
senior_warrant_officer = InlineKeyboardButton('Старший прапоршик', callback_data='Старший прапорщик rang')
back_button_rang = InlineKeyboardButton('Назад', callback_data='Назад rang')
back_button_rang.text = '⬅️ Назад. '
keyboard_rang.add(
    private_button,
    junior_sergeant_button,
    sergeant_button,
    senior_sergeant_button,
    foreman_button,
    warrant_officer_button,
    senior_warrant_officer
)
keyboard_rang.row(back_button_rang)

keyboard_rag_officer = InlineKeyboardMarkup(row_width=2)
lieutenant_button = InlineKeyboardButton('Лейтенант', callback_data='лейтенант rang')
senior_lieutenant_button = InlineKeyboardButton('Старший лейтенант', callback_data='старший лейтенант rang')
captain_button = InlineKeyboardButton('Капитан', callback_data='капитан rang')
major_button = InlineKeyboardButton('Майор', callback_data='майор rang')
lieutenant_colonel_button = InlineKeyboardButton('Подполковник', callback_data='подполковник rang')
colonel_button = InlineKeyboardButton('Полковник', callback_data='полковник rang')
keyboard_rag_officer.add(
    lieutenant_button,
    senior_lieutenant_button,
    captain_button,
    major_button,
    lieutenant_colonel_button,
    colonel_button,
)
keyboard_rag_officer.row(back_button_rang)

keyboard_job_title = InlineKeyboardMarkup(row_width=2)
firefighter_button = InlineKeyboardButton('Пожарный', callback_data='пожарный_job')
senior_firefighter_button = InlineKeyboardButton('Старший пожарный', callback_data='старший пожарный_job')
squad_commander_button = InlineKeyboardButton('Командир отделения', callback_data='командир отделения_job')
assistant_watch_commander_button = InlineKeyboardButton('Помощник начальника караула', callback_data='помощник начальника караула_job')
watch_commander_button = InlineKeyboardButton('Начальник караула', callback_data='начальник караула_job')
unit_chief = InlineKeyboardButton('Начальник части', callback_data='начальник части_job')
deputy_head_chief = InlineKeyboardButton('Зам. начальника части', callback_data='заместитель начальника части_job')
senior_instructor_button = InlineKeyboardButton('Старший инструктор', callback_data='Старший инструктор_job')
back_button_job = InlineKeyboardButton('⬅️ Назад', callback_data='Назад job')

keyboard_job_title.add(
    firefighter_button,
    senior_firefighter_button,
    squad_commander_button,
    assistant_watch_commander_button,
    watch_commander_button,
    deputy_head_chief,
    unit_chief,
    senior_instructor_button,
)

keyboard_job_title.row(back_button_job)


keyboard_part_number = InlineKeyboardMarkup(row_width=2)
fire_rescue_service_button_1 = InlineKeyboardButton('ПСЧ-1', callback_data='ПСЧ-1')
fire_rescue_service_button_2 = InlineKeyboardButton('ПСЧ-2', callback_data='ПСЧ-2')
fire_rescue_service_button_3 = InlineKeyboardButton('ПСЧ-3', callback_data='ПСЧ-3')
fire_rescue_service_button_4 = InlineKeyboardButton('ПСЧ-4', callback_data='ПСЧ-4')
back_button_part = InlineKeyboardButton('⬅️ Назад', callback_data='Назад part_number')

keyboard_part_number.add(
    fire_rescue_service_button_1,
    fire_rescue_service_button_2,
    fire_rescue_service_button_3,
    fire_rescue_service_button_4
)
keyboard_part_number.row(back_button_part)

keyboard_edit = InlineKeyboardMarkup(row_width=2)
edit_button = InlineKeyboardButton('Редактировать профиль', callback_data='edit')
rank_button = InlineKeyboardButton('Звание', callback_data='звание_edit')
job_title_button = InlineKeyboardButton('Должность', callback_data='должность_edit')
part_number_button = InlineKeyboardButton('Номер части', callback_data='номер_части_edit')
service_start_date = InlineKeyboardButton('Дата начала службы', callback_data='дата_начала_edit')
telephone_number = InlineKeyboardButton('Номер телефона', callback_data='номер_телефона_edit')
close_button = InlineKeyboardButton('Закрыть', callback_data='Закрыть_edit')

keyboard_edit.add(
    rank_button,
    job_title_button,
    telephone_number,
    service_start_date,
    part_number_button,

)
keyboard_edit.row(close_button)



