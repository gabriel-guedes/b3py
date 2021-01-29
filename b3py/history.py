from .db import session, History
import toml
import logging
from typing import TextIO
from .config import get_logger

logger = get_logger('history',logging.DEBUG)

with open('./b3py/filemap.toml', 'r') as fp:
    filemap = toml.load(fp)

def format_data(value, data_type):
    """Format value according to its data type
    decimals will always be divided by 100 to match 2 decimal places
    
    Parameters
    ----------
    value : str
        String containing values from raw data file
    data_type : str
        String containing the type of data (i.e. integer, string, float)

    Returns
    -------
        Data typed according to data_type parameter
    """    
    
    if data_type == 'decimal' and value:
        formatted_value = int(value)/100
    elif data_type == 'integer' and value:
        formatted_value = int(value)
    else:
        formatted_value = value
    
    return formatted_value

def parse_data(raw: str)->dict:
    """Parse raw data file line using positions mapped in filemap.toml
    
    Parameters
    ----------
    raw : str
        Line read from raw data file

    Returns
    -------
    dict
        Dictionary with key/values corresponding to historical data (i.e. session date, ticker, ohlc prices, etc) 
    """        

    values = {}
    for key in filemap:
        begin = filemap[key]['begin']
        end = filemap[key]['end']
        data_type = filemap[key]['type']

        value = raw[begin:end].strip()
        
        formatted_value = format_data(value, data_type)
        
        values.update({key: formatted_value})
    
    return values

def lazy_process_rawdata(fp: TextIO, step=1000)->list:
    """Generator function that reads/parses n-lines of raw data file
    
    
    Parameters
    ----------
    fp : TextIO
        File pointer
    
    step : int (default 100)
        Number of lines yielded

    Yields
    -------
    list
        List of tuples containing history data fields
    """        
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

def build_history_obj(parsed_data:tuple):
    """Build History object from parsed data
    
    Parameters
    ----------
    parsed_data : tuple
        Tuple containing History attributes

    Returns
    -------
    History
        History object
    """
    
    return History(
        session_date=parsed_data[0], 
        ticker=parsed_data[1], 
        subclass=parsed_data[2], 
        event=parsed_data[3], 
        open_price=parsed_data[4], 
        high_price=parsed_data[5],
        low_price=parsed_data[6], 
        close_price=parsed_data[7], 
        volume=parsed_data[8], 
        quantity=parsed_data[9], 
        deals=parsed_data[10]
    )

def load_history(filepath: str, step=1000):
    logger.info(f'NEW VERSION - Processing {filepath}...')
    with open(filepath, 'r', encoding='latin_1') as fp:
        for data in lazy_process_rawdata(fp, step=step):
            history_objects = [build_history_obj(n) for n in data]
            session.bulk_save_objects(history_objects)
            session.commit()

    logger.info(f'Done')