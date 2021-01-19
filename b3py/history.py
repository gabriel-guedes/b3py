from .parse import get_values
from .db import engine, History
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import logging
from .config import get_logger

logger = get_logger('history',logging.DEBUG)

def read_prices(filepath:str)->list:
    values = []
    with open(filepath, 'r') as rawdata:
        for line in rawdata:
            parsed = get_values(line)
            if parsed['rec_type'] in ['00', '99']:
                continue
            if parsed['market_type'] != '010':
                continue
            if parsed['bdi_code'] != '02':
                continue

            line_values = [
                parsed['session_date'],
                parsed['ticker'],
                parsed['open_price'],
                parsed['high_price'],
                parsed['low_price'],
                parsed['close_price'],
                parsed['volume'],
                parsed['quantity'],
                parsed['deals']
            ]
            
            values.append(line_values)
    
    return values

def lazy_read_prices(filepath:str, step=100)->list:
    values = []
    i = 0
    with open(filepath, 'r', encoding='latin-1') as rawdata:
        for line in rawdata:
            if i == 0:
                values = []
            parsed = get_values(line)
            if parsed['rec_type'] in ['00', '99']:
                continue
            if parsed['market_type'] != '010':
                continue
            if parsed['bdi_code'] != '02':
                continue

            line_values = (
                parsed['session_date'],
                parsed['ticker'],
                parsed['open_price'],
                parsed['high_price'],
                parsed['low_price'],
                parsed['close_price'],
                parsed['volume'],
                parsed['quantity'],
                parsed['deals']
            )
            
            values.append(line_values)
            i += 1

            if i == step:
                i = 0
                yield values
        
        yield values        

def insert_prices(table_lines:list):
    conn = engine.connect()
    table = History.__table__
    ins = table.insert(table_lines)
    try:
        result = conn.execute(ins)
    except:
        logger.exception(f'DB Insertion error from {table_lines[0]} to {table_lines[-1]}')
    else:
        pass
        # logger.info(f'{len(table_lines)} lines inserted into History table')

def insert_prices_orm(history_lines:list):
    Session = sessionmaker(bind=engine)
    session = Session()
    insertion_list = []

    for line in history_lines:
        row = History(session_date=line[0], ticker=line[1], open_price=line[2], high_price=line[3],
        low_price=line[4], close_price=line[5], volume=line[6], quantity=line[7], deals=line[8])
        insertion_list.append(row)
    
    if insertion_list:
        session.add_all(insertion_list)
        session.commit()
