from b3py.history import load_history_file
from b3py.db import create_tables
import os

import toml

one_day_file = 'b3py/sample/COTAHIST_D10112020.TXT'
# year_file = 'rawdata/COTAHIST_A2000.TXT'


directory = './rawdata/archived/'
files = os.listdir(directory)
files.sort()

create_tables()

for filename in files:
    load_history_file(directory+filename)

# load_history_file(one_day_file)