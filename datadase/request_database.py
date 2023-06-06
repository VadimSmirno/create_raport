from sqlalchemy.exc import SQLAlchemyError
from logging_dir.log import logger
from datadase.models import Session, User


def writing_information_to_the_database(telegram_id, data: dict):
    logger.info(data)
    with Session() as session:
        new_user = User(
            telegram_id=telegram_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            rank=data.get('rang'),
            job_title=data.get('job_title'),
            part_number=data.get('part_number'),
            surname=data.get('surname'),
            telephone_number=data.get('telephone_number'),
            service_start_date = data.get('service_start_date')
        )
        session.add(new_user)
        try:
            session.commit()
            logger.info("Пользователь успешно добавлен в базу данных!")
        except SQLAlchemyError as e:
            logger.info("Ошибка при добавлении пользователя:", str(e))
        finally:
            session.close()


def update_user_data_in_database(data, column_name, telegram_id):
    logger.info(data)
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        if column_name == 'job':
            user.job_title = data
        elif column_name == 'rang':
            user.rank = data
        elif column_name == 'date_start':
            user.service_start_date = data
        else:
            user.part_number = data

        try:
            session.commit()
            logger.info('Успешное обновление данных')
        except SQLAlchemyError as err:
            logger.error('Ошибка обновления', err)
        finally:
            session.close()

def update_user_telephone_number(telegram_id, telephone_number):
    with Session() as session:
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        user.telephone_number = telephone_number
        try:
            session.commit()
            logger.info('Успешное обновление данных')
        except SQLAlchemyError as err:
            logger.error('Ошибка обновления', err)
        finally:
            session.close()