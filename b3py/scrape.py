import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import lxml
import logging
from .config import get_logger

logger = get_logger('scrape',logging.DEBUG)

def get_url_content(ticker: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    url = f'https://www.meusdividendos.com/empresa/{ticker}'
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        logger.debug(f'SCRAPE Error - Status: {r.status_code} for {url}')
    soup = BeautifulSoup(r.content, 'lxml')
    return(soup)

def get_table_specs(section: str):
    """Returns css-selector, row lenght and field positions for tables to be scraped
    Prameters
    ---------
    section : {'ult', 'hist', 'boni'}
        Area where tabular data will be scraped
    
    Returns
    -------
    css-selector: str

    """    
    if section == 'ult':
        css_selector = '#dividendos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1)'
        row_length = 6
        cells_position = [0, 1, 3, 5]
    
    elif section == 'hist':
        css_selector = '.table-bordered > tbody:nth-child(1)'
        row_length = 7
        cells_position = [0, 1, 3, 5]        
        
    elif section == 'boni':
        css_selector = 'div.row:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1)'
        row_length = 5
        cells_position = [0, 1, 3, 4]

    return css_selector, row_length, cells_position

def build_output_row(content, positions):
        
        acao = content[positions[0]]
        tipo = content[positions[1]]
        data_com = datetime.strptime(content[positions[2]][:15], f'%a %b %d %Y')
        fator = content[positions[3]]

        return [data_com, acao, tipo, fator]


def scrape_adjustments(ticker: str, section: str):
    """Scrape www.meusdividendos.com/empresa/{ticker} data from sections:
    'ULTIMOS PROVENTOS', 'HISTORICO DE PROVENTOS' and 'BONIFICACAO, DESDOBRAMENTO AGRUPAMENTO'
    Prameters
    ---------
    ticker : str
        Ticker without subclass prefix (i.e. for 'PETR4' use 'PETR')
    
    section : {'ult', 'hist', 'boni'}
        Area where tabular data will be scraped
    
    Returns
    -------
    pd.Dataframe
        Pandas Dataframe with columns: ticker, type, data_com, amount or factor
    """

    if not section in {'ult', 'hist', 'boni'}:
        raise ValueError(f'Section must be "ult", "hist", "boni"')

    soup = get_url_content(ticker)
    css_selector, row_length, cells_position = get_table_specs(section)
    
    tbody = soup.select(css_selector)
    if len(tbody) != 1:
        logger.debug(f'{ticker} - No data found or page structure has changed')
        return
    
    td = tbody[0].find_all('td')
    
    content = [i.text.strip() for i in td]
    
    rows_start_positions = [i for i in range(0, len(content), row_length)]

    output_list = []
    
    for start_position in rows_start_positions:
        row_content = content[start_position:start_position+row_length]
        output_row = build_output_row(row_content, cells_position)
        output_list.append(output_row)

    df = pd.DataFrame(output_list)
    if df.size > 0:
        df.set_index(0, inplace=True)

    
    return(df)    