from .config import db_user, db_password, db_host, db_schema, db_port
from sqlalchemy import Column, String, Float, Integer, BigInteger, Date, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_schema}')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'

    session_date = Column(Date, primary_key=True)
    ticker = Column(String(12), primary_key=True)
    subclass = Column(String(4))
    event = Column(String(4))
    open_price = Column(Numeric(precision=10, scale=2))
    high_price = Column(Numeric(precision=10, scale=2))
    low_price = Column(Numeric(precision=10, scale=2))
    close_price = Column(Numeric(precision=10, scale=2))
    volume = Column(Numeric(precision=18, scale=2))
    quantity = Column(BigInteger)
    deals = Column(Integer)

    def __repr__(self):
        return f'<History(session_date="{self.session_date}", ticker="{self.ticker}")>'


class Dividends(Base):
    __tablename__ = 'dividends'

    ticker = Column(String(12), primary_key=True)
    data_com = Column(Date, primary_key=True)
    amount = Column(Numeric(precision=10, scale=2))

    def __repr__(self):
        return f'<Dividends(ticker="{self.ticker}", data_com="{self.data_com}", amount="{self.amount}")>'

def create_tables():
    """Drop and then create all declared tables
    
    Parameters
    ----------

    Returns
    -------
    """        
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all()