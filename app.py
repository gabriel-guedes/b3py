from b3py.history import insert_prices, insert_prices_orm, read_prices, lazy_read_prices
from b3py.db import create_tables
import os

# one_day_file = 'b3py/sample/COTAHIST_D10112020.TXT'
# year_file = 'rawdata/COTAHIST_A2000.TXT'

all_files = os.listdir('rawdata')
all_files.sort()

for year_file in all_files:
    filepath = f'rawdata/{year_file}'
    if not os.path.isfile(filepath):
        continue
    result = 'bom'
    year_generator = lazy_read_prices(filepath)

    for prices_list in year_generator:
        try:
            # insert_prices(prices_list)
            insert_prices_orm(prices_list)
        except:
            result = 'ruim'
            break
        else:
            pass
        
    print(f'Deu {result} - {year_file}')