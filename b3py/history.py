from .parse import get_values
from .db import engine, History

def read_file(filepath:str)->list:
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