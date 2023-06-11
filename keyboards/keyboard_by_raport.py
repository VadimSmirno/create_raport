from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_managers_name= InlineKeyboardMarkup(row_width=3)

name1 = InlineKeyboardButton('Балчугов В.В', callback_data='Балчугову В.В name')
name2 = InlineKeyboardButton('Веретейников С.А', callback_data='Веретейникову С.А. name')
add_name = InlineKeyboardButton('Добавить в ручную...', callback_data='name_add')

keyboard_managers_name.add(
    name1,
    name2,
    add_name
)
# keyboard_managers_name.row(add_name)

keyboard_vacation_part = InlineKeyboardMarkup(row_width=3)

one_part = InlineKeyboardButton('Первая часть отпуска', callback_data='1 part')
two_part = InlineKeyboardButton('Вторая часть отпуска', callback_data='2 part')
total_vacation = InlineKeyboardButton('Отпуск целиком', callback_data='3 part')
back_button_part = InlineKeyboardButton('⬅️ Назад', callback_data='Назад')

keyboard_vacation_part.add(
    one_part,
    two_part,
    total_vacation,
)
keyboard_vacation_part.row(back_button_part)

keyboard_departure = InlineKeyboardMarkup(row_width=3)
departure_true = InlineKeyboardButton('С выездом', callback_data='С выездом')
departure_false = InlineKeyboardButton('Без выезда', callback_data='Без выезда')
travel_abroad = InlineKeyboardButton('С выездом за границе', callback_data='С выездом за границу')

keyboard_departure.add(
    departure_true,
    departure_false,
    travel_abroad
)
keyboard_departure.row(back_button_part)

keyboard_yes_or_no = InlineKeyboardMarkup(row_width=2)
keyboard_material_aid = InlineKeyboardMarkup(row_width=2)
material_aid_yes_button = InlineKeyboardButton('Да', callback_data='да')
material_aid_no_button = InlineKeyboardButton('Нет', callback_data='нет')

keyboard_material_aid.add(
    material_aid_yes_button,
    material_aid_no_button
)
keyboard_material_aid.row(back_button_part)

keyboard_yes_or_no.add(
    material_aid_yes_button,
    material_aid_no_button
)

keyboard_kind_of_transport = InlineKeyboardMarkup(row_width=3)
railway_button = InlineKeyboardButton('Ж/д', callback_data='железнодорожным')
air_button = InlineKeyboardButton('Воздушный', callback_data='воздушным')
automotive_button = InlineKeyboardButton('Автомобильный', callback_data='автомобильным')

keyboard_kind_of_transport.add(
    railway_button,
    air_button,
    automotive_button
)

keyboard_family = InlineKeyboardMarkup(row_width=4)

wife_button = InlineKeyboardButton(text="Жена", callback_data="Жена wife")
husband_button = InlineKeyboardButton(text="Муж", callback_data="Муж husband")
daughter_button = InlineKeyboardButton(text="Дочь", callback_data="Дочь daughter")
son_button = InlineKeyboardButton(text="Сын", callback_data="Сын son")
keyboard_family.add(
    wife_button,
    husband_button,
    daughter_button,
    son_button
)

keyboard_rung = InlineKeyboardMarkup(row_width=2)
captain_button = InlineKeyboardButton('Капитан', callback_data='капитану rang')
major_button = InlineKeyboardButton('Майор', callback_data='майору rang')
lieutenant_colonel_button = InlineKeyboardButton('Подполковник', callback_data='подполковнику rang')
colonel_button = InlineKeyboardButton('Полковник', callback_data='полковнику rang')
major_general_button =InlineKeyboardButton('Генерал-майор', callback_data='генерал-майору rang')
lieutenant_general = InlineKeyboardButton('Генерал-лейтенант', callback_data='генерал-лейтенанту rang')

keyboard_rung.add(
    major_general_button,
    lieutenant_general,
    colonel_button,
    lieutenant_colonel_button,
    major_button,
    captain_button
)