import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import lxml
import logging
from .config import get_logger

logger = get_logger('scrape',logging.DEBUG)

logger.info('Testing logger')

def get_url_content(ticker: str):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    url = f'https://www.meusdividendos.com/empresa/{ticker}'
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        logger.debug(f'SCRAPE Error - Status: {r.status_code} for {url}')

    soup = BeautifulSoup(r.content, 'lxml')
    return(soup)

def meusdiv_ultimos(ticker):
    """
    Scrape www.meusdividendos.com/empresa/{ticker}
    Get data from ULTIMOS PROVENTOS table
    """

    soup = get_url_content(ticker)

    ult_css_selector = '#dividendos > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1)'
    ultimos = soup.select(ult_css_selector)
    if not ultimos:
        logger.info(f'No dividends found for ticker:{ticker.upper()}')
        return pd.DataFrame()
        # raise ValueError(f'No dividends found on {url}')
    
    for ult_table in ultimos:
        ult_data = ult_table.find_all('td')
    
    cells = [i.text.strip() for i in ult_data]
    ultimos_list = []
    i = 0
    while i < len(cells):
        acao = cells[i]
        provento = cells[i+1]
        data_com = datetime.strptime(cells[i+3][:15], f'%a %b %d %Y')
        valor = cells[i+5]

        ultimos_list.append([data_com, ticker.upper(), acao, provento, valor])

        i += 6

    df = pd.DataFrame(ultimos_list)
    if df.size:
        df.set_index(0, inplace=True)
    
    return(df)

def meusdiv_historico(ticker):
    """
    Scrape www.meusdividendos.com/empresa/{ticker}
    Get data from HISTORICO DE PROVENTOS table
    """
    soup = get_url_content(ticker)
    hist_css_selector = '.table-bordered > tbody:nth-child(1)'

    historico = soup.select(hist_css_selector)
    if not historico:
        logger.debug(f'No dividends found for {ticker}')
        return pd.DataFrame()
    
    for hist_table in historico:
        hist_data = hist_table.find_all('td')
    
    cells = [i.text.strip() for i in hist_data]
    hist_list = []
    i = 0
    while i < len(cells):
        acao = cells[i]
        provento = cells[i+1]
        data_com = datetime.strptime(cells[i+3][:15], f'%a %b %d %Y')
        valor = cells[i+5]

        hist_list.append([data_com, ticker.upper(), acao, provento, valor])

        i += 7

    df = pd.DataFrame(hist_list)
    if df.size > 0:
        df.set_index(0, inplace=True)
    
    return(df)

def meusdiv_bonificacao(ticker):
    """
    Scrape www.meusdividendos.com/empresa/{ticker}
    Get data from BONIFICACAO, DESDOBRAMENTO E GRUPAMENTO table
    """

    logger.debug('Trying to scrape bonif')

    soup = get_url_content(ticker)
    css_selector = 'div.row:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1)'

    table_body = soup.select(css_selector)
    if not table_body:
        logger.debug(f'No bonificacao/split/agrupamento found for {ticker}')
        return pd.DataFrame()
    
    for rows in table_body:
        boni_data = rows.find_all('td')
    
    cells = [i.text.strip() for i in boni_data]
    boni_list = []
    i = 0
    while i < len(cells):
        acao = cells[i]
        tipo = cells[i+1]
        data_com = datetime.strptime(cells[i+3][:15], f'%a %b %d %Y')
        fator = cells[i+4].replace(' para ', ':')

        boni_list.append([data_com, acao, tipo, fator])

        i += 5

    df = pd.DataFrame(boni_list)
    if df.size > 0:
        df.set_index(0, inplace=True)
    
    return(df)    

if __name__ == '__main__':
    # input_ticker = 'gluglu'
    # print(meusdiv_ultimos(input_ticker))
    # print(meusdiv_historico(input_ticker))
    # print(meusdiv_bonificacao(input_ticker))
    pass