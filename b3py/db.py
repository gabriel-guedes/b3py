from .config import db_user, db_password, db_host, db_schema, db_port
from sqlalchemy import Column, String, Float, Integer, BigInteger, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_schema}')

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'

    session_date = Column(Date, primary_key=True)
    ticker = Column(String(12), primary_key=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)
    quantity = Column(BigInteger)
    deals = Column(Integer)

    def __repr__(self):
        return f'<History(session_date="{self.session_date}", ticker="{self.ticker}")>'


class Stock(Base):
    __tablename__ = 'stocks'
    ticker = Column(String(12), primary_key=True)
    share_type = Column(String(5))
    first_session = Column(Date)
    last_session = Column(Date)

    def __repr__(self):
        return f'<Stock(ticker="{self.ticker}", share_type="{self.share_type}", first_session="{self.first_session}", last_session="{self.last_session}")>'

def create_tables():
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()