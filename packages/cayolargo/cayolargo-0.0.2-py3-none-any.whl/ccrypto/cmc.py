from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from binance.client import Client
from datetime import datetime
from datetime import datetime as dt
import pandas as pd
#from matplotlib import pyplot as plt
 
from .mycryptokeys import cmc_api_key
 
 
def coinsbymcap(n=100):
    """
    Fetches cryptocurrency data from the CoinMarketCap API based on market
    capitalization ranking.
 
    Args:
        n (int, optional): The maximum rank of cryptocurrencies to include
                           in the results. Default is 100.
 
    Returns:
        tuple or None: A tuple containing a pandas DataFrame and a list of 
                       cryptocurrency tickers (symbols) or None if an error 
                       occurred.
         
        The DataFrame contains the following columns:
        - 'fetched_on': The date when the data was fetched from the API in 
          the format 'YYYY-MM-DD'.
        - 'ranking': The rank of the cryptocurrency based on market 
          capitalization.
        - 'symbol': The ticker symbol of the cryptocurrency.
 
    Note:
        - This function fetches data from the CoinMarketCap API using a valid 
          API key stored inside mycryptokeys.cmc_api_key.
        - The fetched data includes information on multiple cryptocurrencies, 
          but only the top 'n' based on market capitalization ranking are returned.
        - If an error occurs during the data retrieval process, the function 
          returns None.
    """
     
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
    'start' : '1',
    'sort'  : 'cmc_rank',
    'limit' : '5000'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': cmc_api_key,
    }
 
    session = Session()
    session.headers.update(headers)
 
    err = None
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        fetched_on = dt.now().strftime('%Y-%m-%d')
    except (ConnectionError, Timeout, TooManyRedirects) as err:
        pass
     
    if data['status']['error_message'] is None:
        data = data['data']  # list with len(list) = parameters['limit']
 
        lst = list()
        for i, _ in enumerate(data):
            lst.extend([[fetched_on, int(data[i]['rank']), data[i]['symbol']]])
     
        df = pd.DataFrame(lst, columns=['fetched_on', 'ranking', 'symbol'])
        df = df[df.ranking <= n]
        lst = df['symbol'].values  # plain list with crypto tickers
         
        return (df, lst)
         
    else:
        return (None, None)
