import locale

import docx
from docx.shared import RGBColor
from docx.shared import Pt
from datetime import datetime
from logging_dir.log import logger
from datadase.request_database import get_data_user
from datadase.models import User


def get_month_in_genitive(date_string):
    locale.setlocale(locale.LC_TIME, 'ru')
    current_date = datetime.strptime(date_string, "%d-%m-%Y")

    month_cases = {
        "январь": "января",
        "февраль": "февраля",
        "март": "марта",
        "апрель": "апреля",
        "май": "мая",
        "июнь": "июня",
        "июль": "июля",
        "август": "августа",
        "сентябрь": "сентября",
        "октябрь": "октября",
        "ноябрь": "ноября",
        "декабрь": "декабря"
    }

    month_name = current_date.strftime("%B").lower()
    month_in_genitive = month_cases.get(month_name, "")

    return month_in_genitive


def format_itinerary(itinerary):
    result = ""
    for destination, transport in itinerary.items():
        city = destination.split()[1]
        result += f"{transport} транспортом от г. Вологда до г. {city}"

    return result


def format_itinerary2(itinerary):
    result = ""
    previous_destination = ""
    for destination, transport in itinerary.items():
        city = destination.split()[1]
        if previous_destination:
            result += f", {transport} транспортом от г. {previous_destination} до г. {city}"
        else:
            result += f"{transport} транспортом от г. Вологда до г. {city}"
        previous_destination = city
    return result


def format_vacation_followers(dct):
    result = "отпуска следуют:"
    if 'wife' in dct:
        result += f" жена {dct['wife']};"
    if 'husband' in dct:
        result += f" муж {dct['husband']};"
    if 'son' in dct:
        result += f" сын {dct['son']};"
    if 'daughter' in dct:
        result += f" дочь {dct['daughter']};"
    result = result.rstrip(";")  # Удаление последнего символа ";"
    return result


def generation_raport(telegram_id):
    fonts = ["Denistina", "PF Scandal Pro Black", "Marianna", "Shlapak Script"]
    result: User = get_data_user(telegram_id)
    if result.raport_info_json['vacation_part'] == '1':
        date_finish_vacation = result.raport_info_json['date_finish_vacation']
        date_start_vacation = result.raport_info_json['date_start_vacation']
        date1 = datetime.strptime(date_finish_vacation, "%d-%m-%Y")
        date2 = datetime.strptime(date_start_vacation, "%d-%m-%Y")
        count = date1 - date2
        count = str(count.days)
        if result.raport_info_json['departure'] == 'Без выезда':
            doc = docx.Document('document_generation/Рапорт 1ч без выезда без стажа.docx')
            style = doc.styles['Normal']
            font = style.font
            font.size = Pt(16)
            font.color.rgb = RGBColor(89, 131, 176)  # (89, 131, 176)
            font.name = 'Denistina'  # 'Denistina 16' "PF Scandal Pro Black  -14" "Marianna 16" ''Shlapak Script''
            for paragraph in doc.paragraphs:
                if result.raport_info_json[
                    'manager_name'] != "Балчугов В.В" and paragraph.text == "Начальнику главного управления":
                    paragraph.text = paragraph.text.replace("Начальнику", 'ВрИО начальника')
                if result.raport_info_json['manager_name'] != "Балчугов В.В" and 'генерал-майору' in paragraph.text:
                    paragraph.text = paragraph.text.replace('генерал-майору', result.raport_info_json['rung'])
                if result.raport_info_json['manager_name'] != "Балчугов В.В" and 'Балчугову В.В.' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Балчугову В.В.', result.raport_info_json['manager_name'])
                if '20.05.2023г' in paragraph.text:
                    paragraph.text = paragraph.text.replace('20.05.2023', datetime.now().strftime("%d.%m.%Y"))
                if '30 календарный дней' in paragraph.text:
                    paragraph.text = paragraph.text.replace('30', count)
                if '8900 536 71 36' in paragraph.text:
                    paragraph.text = paragraph.text.replace('8900 536 71 36', result.telephone_number)
                if 'Иванов Иван Иванович' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Иванов Иван Иванович',
                                                            f'{result.last_name} {result.first_name} {result.surname}')
                if 'Старший-инструктор ' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Старший-инструктор по вождению ', result.job_title)
                if '3 пожарно' in paragraph.text:
                    paragraph.text = paragraph.text.replace('3', str(result.part_number))
                if 'за 2023 год , с 2 августа.2023 года' in paragraph.text or '2023' in paragraph.text:
                    month = get_month_in_genitive(date_start_vacation)
                    paragraph.text = paragraph.text.replace('2023', str(date2.year))
                    paragraph.text = paragraph.text.replace('2 августа', f'{str(date2.day)} {month}')
                if result.raport_info_json['material_aid'] == 'нет' and 'Прошу выплатить мне' in paragraph.text:
                    p = paragraph._element
                    p.getparent().remove(p)
            doc.save(f'document_generation/{result.last_name} {result.first_name[0]}.{result.surname[0]}.docx')
        elif result.raport_info_json['departure'] == 'С выездом':
            doc = docx.Document('document_generation/Рапорт 1ч с выездом без стажа.docx')
            style = doc.styles['Normal']
            font = style.font
            font.size = Pt(16)
            font.color.rgb = RGBColor(89, 131, 176)  # (89, 131, 176)
            font.name = 'Denistina'  # 'Denistina 16' "PF Scandal Pro Black  -14" "Marianna 16" ''Shlapak Script''
            for paragraph in doc.paragraphs:
                if result.raport_info_json[
                    'manager_name'] != "Балчугову В.В" and paragraph.text == "Начальнику главного управления":
                    paragraph.text = paragraph.text.replace("Начальнику", 'ВрИО начальника')
                if result.raport_info_json['manager_name'] != "Балчугову В.В" and 'генерал-майору' in paragraph.text:
                    paragraph.text = paragraph.text.replace('генерал-майору', result.raport_info_json['rung'])
                if result.raport_info_json['manager_name'] != "Балчугову В.В" and 'Балчугову В.В.' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Балчугову В.В.', result.raport_info_json['manager_name'])
                if '30 календарный дней' in paragraph.text:
                    paragraph.text = paragraph.text.replace('30', count)
                if 'за 2023 год , с 2 августа.2023 года' in paragraph.text or '2023' in paragraph.text:
                    month = get_month_in_genitive(date_start_vacation)
                    paragraph.text = paragraph.text.replace('2023', str(date2.year))
                    paragraph.text = paragraph.text.replace('2 августа', f'{str(date2.day)} {month}')
                if '8900 536 71 36' in paragraph.text:
                    paragraph.text = paragraph.text.replace('8900 536 71 36', result.telephone_number)
                if '20.05.2023г' in paragraph.text:
                    paragraph.text = paragraph.text.replace('20.05.2023', datetime.now().strftime("%d.%m.%Y"))
                if '3 пожарно' in paragraph.text:
                    paragraph.text = paragraph.text.replace('3', str(result.part_number))
                if 'Старший-инструктор ' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Старший-инструктор по вождению ', result.job_title)
                if 'Иванов Иван Иванович' in paragraph.text:
                    paragraph.text = paragraph.text.replace('Иванов Иван Иванович',
                                                            f'{result.last_name} {result.first_name} {result.surname}')
                if 'буду проводить в городе Сочи' in paragraph.text:
                    list_city = result.raport_info_json['list_city']
                    list_city = list_city.split(', ')
                    paragraph.text = paragraph.text.replace('городе Сочи', f'{list_city[1]} {list_city[0]}')
                if 'железнодорожным транспортом' in paragraph.text:
                    itinerary = result.raport_info_json.get('itinerary')
                    if len(itinerary) == 1:
                        itinerary = format_itinerary(itinerary)
                        paragraph.text = paragraph.text.replace('железнодорожным транспортом', itinerary)
                    else:
                        itinerary = format_itinerary2(itinerary)
                        paragraph.text = paragraph.text.replace('железнодорожным транспортом', itinerary)
                if 'отпуска следуют:' in paragraph.text:
                    family = result.raport_info_json
                    family_str = format_vacation_followers(family)
                    if family_str.endswith('отпуска следуют:'):
                        p = paragraph._element
                        p.getparent().remove(p)
                    else:
                        paragraph.text = paragraph.text.replace('отпуска следуют:', family_str)

            doc.save(f'document_generation/{result.last_name} {result.first_name[0]}.{result.surname[0]}.docx')
    return f'{result.last_name} {result.first_name[0]}.{result.surname[0]}.docx'

# if __name__ == '__main__':
#     generation_raport(telegram_id='')