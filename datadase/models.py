from sqlalchemy.orm import DeclarativeBase,sessionmaker
from sqlalchemy import Column, Integer, String, BigInteger, Date, JSON
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy import URL
import os

metadata = MetaData()

load_dotenv()
name_db = os.getenv('db_name')
username = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')

url_object = URL.create(
    "postgresql+psycopg2",
    username=username,
    password=password,
    host=host,
    database=name_db,
)

engine = create_engine(url_object)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase): pass

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    surname = Column(String, default=None)
    rank = Column(String)
    job_title = Column(String)
    part_number = Column(Integer)
    service_start_date = Column(Date)  # начало службы
    telephone_number = Column(String)
    raport_info_json = Column(JSON)




# Base.metadata.create_all(bind=engine)