# from b3py.history import load_history, lazy_process_rawdata
# from b3py.db import create_tables
# import os

# import toml

# directory = './rawdata/archived/'
# files = os.listdir(directory)
# files.sort()

# create_tables()

# for filename in files:
#     load_history(directory+filename, step=1000)    

# one_day_file = 'b3py/sample/COTAHIST_D10112020.TXT'
# petr4_file = 'b3py/sample/PETR4_D10112020.TXT'



# load_history_new(petr4_file)

# with open(petr4_file, 'r') as fp:
#     for n in lazy_read_rawdata(fp):
#         print(n)

from b3py.scrape import scrape_adjustments

dividends = scrape_adjustments('MGLU', 'boni')
print(dividends)