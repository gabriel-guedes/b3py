from .config import db_user, db_password, db_host, db_schema, db_port
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_schema}')

Base = declarative_base()

class History(Base):
    __tablename__ = 'History'

    session_date = sqlalchemy.Column(sqlalchemy.Date, primary_key=True)
    ticker = sqlalchemy.Column(sqlalchemy.String(12), primary_key=True)
    open_price = sqlalchemy.Column(sqlalchemy.Float)
    high_price = sqlalchemy.Column(sqlalchemy.Float)
    low_price = sqlalchemy.Column(sqlalchemy.Float)
    close_price = sqlalchemy.Column(sqlalchemy.Float)
    volume = sqlalchemy.Column(sqlalchemy.Float)
    quantity = sqlalchemy.Column(sqlalchemy.BigInteger)
    deals = sqlalchemy.Column(sqlalchemy.Integer)

class Stocks(Base):
    __tablename__ = 'Stocks'
    ticker = sqlalchemy.Column(sqlalchemy.String(12), primary_key=True)
    share_type = sqlalchemy.Column(sqlalchemy.String(5))
    first_appearence = sqlalchemy.Column(sqlalchemy.Date)
    last_appearence = sqlalchemy.Column(sqlalchemy.Date)

def create_tables():
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()