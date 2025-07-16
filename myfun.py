import yfinance as yf
import datetime
import pickle
import numpy as np
import pandas as pd
import requests

#function for updating stock data
def update_data(tickers):
    """
    :param tickers: list (stock ticker list)
    :return: df (stock data: OLHC and volume)
    """
    try:
        #get data from yahoo finance
        data = yf.download(tickers, period="3d", interval = '5m', group_by='ticker', threads=True)
        #change timezone to HK
        data.index = data.index.tz_convert('Asia/Hong_Kong')
        print('Data updated at {}'.format(datetime.datetime.now()))
        #drop the ticker with empty data
        data = {ticker: data[ticker].dropna() for ticker in tickers}
        return data
    except Exception as e:
        print('Data update failed at {}: {}'.format(datetime.datetime.now(), e))

#function for analysing what stock input
def ask_stock():
    """
    :return: list (formatted stock ticker list from user input)
    """
    ticker_list = []
    share = input("What stock do you want to monitor? (Enter Tickers with , to separate.)")
    #separate the input to list
    stocks = [i.strip() for i in share.split(',')]
    for stock in stocks:
        #HK tickers are in number and we need to change it to XXXX.HK for yf
        if stock.isdigit():
            stock = convert_hk(stock)
            ticker_list.append(stock)
        #get components of HSI
        elif stock == 'HSI':
            with open('hsi_tickers.pickle','rb') as file:
                ticker = pickle.load(file)
            for tick in ticker:
                ticker_list.append(tick)
        #get components of S&P 500
        elif stock == 'US':
            with open('sp500_tickers.pickle', 'rb') as file:
                ticker = pickle.load(file)
            for tick in ticker:
                ticker_list.append(tick)
        #get all HK listed stocks, ETFs, REITs
        elif stock == 'HK':
            with open('hk_tickers.pickle', 'rb') as file:
                ticker = pickle.load(file)
            for tick in ticker:
                ticker_list.append(tick)
        else:
            ticker_list.append(stock)
    return ticker_list

#function for using what technique
def ask_method():
    """
    :return: str (method of analysis)
    """
    #method input until get valid method
    method = input("What do you want to use to monitor the stock? (MTR or Cross or Both)")
    if method == "MTR":
        return "MTR"
    elif method == "Cross":
        return "Cross"
    elif method == "Both":
        return "All"
    else:
        ask_method()

#function for checking Major Trend Reversion
def MTR_check(data):
    """
    :param data: list (stock data from yfinance)
    :return: list (time of bull or bear reversion)
    """
    #get the high and low of each candles
    high = data['High'].values
    low = data['Low'].values
    #get latest 30 candles
    last_high = high[-30:]
    last_low = low[-30:]
    #get the highest and lowest point
    max_high = np.max(last_high)
    min_low = np.min(last_low)
    #get the index of highest and lowest point
    max_high_index = np.where(last_high == max_high)[0]
    min_low_index = np.where(last_low == min_low)[0]
    #only get the latest one to prevent same high or low
    last_max_high_idx = max_high_index[-1]
    last_min_low_idx = min_low_index[-1]
    #get data after max_high and min_low
    latest_high = last_high[last_max_high_idx + 1:]
    latest_low = last_low[last_min_low_idx + 1:]
    #get new high and new low
    if len(latest_high) > 0:
        new_high = argrelextrema(latest_high, np.greater, order = 1)
    else:
        new_high = None
    if len(latest_low) > 0:
        new_low = argrelextrema(latest_low, np.less, order = 1)
    else:
        new_low = None
    #getting time index of data
    time_index = len(data) - 30

    bull_reversion, bear_reversion = [], []
    #compare if there is lower high or higher low
    if (new_high is not None) and (new_high < max_high):
        #bull reversion occur
        bull_time = data.index[time_index + last_max_high_idx + 1]
        bull_reversion = bull_time.strftime('%Y-%m-%d %H:%M:%S')

    if (new_low is not None) and (new_low > min_low):
        #bull reversion occur
        bear_time = data.index[time_index + last_min_low_idx + 1]
        bear_reversion = bear_time.strftime('%Y-%m-%d %H:%M:%S')

    #return time point detected
    return bull_reversion, bear_reversion

#function for checking golden cross and death cross
def Cross(data):
    """
    :param data: list (stock data)
    :return: list (bull time and bear time)
    """
    #define period for moving average
    short_term = 5
    long_term = 20

    #get data and calculate moving average
    close = data['Close'].values
    df = pd.Series(close)
    short_ma = df.rolling(window = short_term).mean()
    long_ma = df.rolling(window = long_term).mean()

    #compare for data crossing
    GoldenX = (short_ma.shift(1) <= long_ma.shift(1)) & (short_ma > long_ma)
    DeathX = (short_ma.shift(1) >= long_ma.shift(1)) & (short_ma < long_ma)

    #if there is cross, add the time for return
    if GoldenX.any():
        golden_index = GoldenX[GoldenX].index.tolist()
        last_golden = golden_index[-1]
        bull_time = data.index[last_golden].strftime('%Y-%m-%d %H:%M:%S')
    else:
        bull_time = []
    if DeathX.any():
        death_index = DeathX[DeathX].index.tolist()
        last_death = death_index[-1]
        bear_time = data.index[last_death].strftime('%Y-%m-%d %H:%M:%S')
    else:
        bear_time = []

    return bull_time, bear_time

#function for sending notification via discord bot
def bot_signal(ticker, data, method, bull = True):
    """
    :param ticker: str (ticker name)
    :param data: str (time)
    :param method: str (method of technical analysis)
    :param bull: bool (bull or bear notice)
    """
    #discord webhook url
    bot_url = 'your-discord-bot-webhook-url'
    if bull:
        message = {"content": "{}: Last BULL timing is {} by {}".format(ticker, data, method)}
    else:
        message = {"content": "{}: Last BEAR timing is {} by {}".format(ticker, data, method)}

    #sending message to bot
    response = requests.post(bot_url, json=message)

    if response.status_code == 204:
        print(f"Message sent at {datetime.datetime.now()}: {message}")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text} at {datetime.datetime.now()}")

#function for changing number into HK stock code for yfinance
def convert_hk(stock_code):
    """
    :param stock_code: int (HK stock number)
    :return: str (HK stock code for yfinance: XXXX.HK)
    """
    stock_code = str(stock_code).strip()
    if stock_code.endswith('.HK'):
        return stock_code.upper()
    #fill zero before the stock number
    stock_code_padded = stock_code.zfill(4)
    return f"{stock_code_padded}.HK"
