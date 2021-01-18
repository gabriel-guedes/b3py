from b3py import history

one_day_file = 'b3py/sample/COTAHIST_D10112020.TXT'

prices = history.lazy_read_prices(one_day_file)

# for lines in prices:
#     print(type(lines))
#     for stock in lines:
#         print(stock)
#         print('\n')

from b3py import config

logger = config.get_logger()
logger.info('balbalba \n pulou?')