from .db import engine, History
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import toml
import logging
from typing import TextIO
from .config import get_logger

logger = get_logger('history',logging.DEBUG)

Session = sessionmaker(bind=engine)
session = Session()

with open('./b3py/filemap.toml', 'r') as fp:
    filemap = toml.load(fp)

def parse_data(raw: str)->dict:
    values = {}
    for key in filemap:
        begin = filemap[key]['begin']
        end = filemap[key]['end']
        value = raw[begin:end].replace('*', '').strip()
        if filemap[key]['type'] == 'float' and value:
            value = float(value)
        elif filemap[key]['type'] == 'integer' and value:
            value = int(value)
        
        values.update({key: value})
    
    return values

def lazy_read_rawdata(fp: TextIO, step=100)->list:
    values = []
    i = 0

    for line in fp:
        if i == 0:
            values = []
        
        parsed = parse_data(line)
        
        if parsed['rec_type'] in ['00', '99']:
            continue
        if parsed['market_type'] != '010':
            continue
        if parsed['bdi_code'] != '02':
            continue

        line_values = (
            parsed['session_date'],
            parsed['ticker'],
            parsed['subclass'],
            parsed['event'],
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

def insert_history_orm(history_lines:list):
    # Session = sessionmaker(bind=engine)
    # session = Session()
    insertion_list = []

    for line in history_lines:
        row = History(session_date=line[0], ticker=line[1], subclass=line[2], event=line[3], open_price=line[4], high_price=line[5],
        low_price=line[6], close_price=line[7], volume=line[8], quantity=line[9], deals=line[10])
        insertion_list.append(row)
    
    if insertion_list:
        session.bulk_save_objects(insertion_list)
        session.commit()

def load_history_file(filepath: str, step=100):
    logger.info(f'Processing {filepath}...')
    with open(filepath, 'r', encoding='latin_1') as fp:
        for lines in lazy_read_rawdata(fp):
            insert_history_orm(lines)