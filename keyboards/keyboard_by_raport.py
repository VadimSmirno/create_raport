from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_managers_name= InlineKeyboardMarkup(row_width=3)

name1 = InlineKeyboardButton('Балчугов В.В', callback_data='Балчугов В.В name')
name2 = InlineKeyboardButton('Веретейников', callback_data='Веретейников name')
name3 = InlineKeyboardButton('Самойленко', callback_data='Самойленко С.А name')
add_name = InlineKeyboardButton('Добавить в ручную...', callback_data='name_add')

keyboard_managers_name.add(
    name1,
    name2,
    name3
)
keyboard_managers_name.row(add_name)

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

keyboard_material_aid = InlineKeyboardMarkup(row_width=2)
material_aid_yes_button = InlineKeyboardButton('Да', callback_data='да')
material_aid_no_button = InlineKeyboardButton('Нет', callback_data='нет')

keyboard_material_aid.add(
    material_aid_yes_button,
    material_aid_no_button
)
keyboard_material_aid.row(back_button_part)