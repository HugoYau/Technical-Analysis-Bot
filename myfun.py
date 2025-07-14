import yfinance as yf
import datetime
import pickle
from scipy.signal import argrelextrema
import numpy as np
import requests

#function for update stock data
def update_data(tickers):
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

#function for getting data from desired market
def ask_session():
    #ask for what market do user want to check
    session = input("What is the trading session now? (Enter US/HK)")
    if session == 'US':
        with open('sp500_tickers.pickle', 'rb') as file:
            tickers = pickle.load(file)
            return tickers
    elif session == 'HK':
        with open('hk_tickers.pickle', 'rb') as file:
            tickers = pickle.load(file)
            return tickers
    else:
        print("This is not available.")
        ask_session()

#function for analyse what stock input
def ask_stock(stock_list):
    ticker_list = []
    share = input("What stock do you want to get announced? (Enter Tickers with , to separate. Enter All to get all announcements.)")
    #for market, we will return all the stock in market directly
    if (share == 'All') & (len(share) == 1):
        return stock_list
    else:
        #separate the input to list
        stocks = [i.strip() for i in share.split(',')]
        for stock in stocks:
            #HK tickers are in number and we need to change it to XXXX.HK for yf
            if stock.isdigit():
                stock = convert_hk(stock)
                if stock in stock_list:
                    ticker_list.append(stock)
                else:
                    print(stock, 'is not on the list')
            #US tickers remain unchanged here
            else:
                if stock in stock_list:
                    ticker_list.append(stock)
                else:
                    print(stock, 'is not on the list')
        return ticker_list

#function for checking Major Trend Reversion
def MTR_check(data):
    #get the high and low of each candles
    high = data['High'].values
    low = data['Low'].values
    #finding extrema among all
    local_max_index= argrelextrema(high, np.greater, order = 10)[0]
    local_min_index= argrelextrema(low, np.less, order = 10)[0]
    #get the value of high/low
    highs = high[local_max_index]
    lows = low[local_min_index]
    #get the time of high/low
    bull_times = data.index[local_max_index]
    bear_times = data.index[local_min_index]

    bull_reversion, bear_reversion = [], []
    for pt in range(1, len(highs)):
        #check for lower high
        current_high = highs[pt]
        previous_high = highs[pt-1]

        if current_high < previous_high:
                bull_reversion.append(bull_times[pt].strftime('%Y-%m-%d %H:%M:%S'))

    for pt in range(1, len(lows)):
        #check for higher low
        current_low = lows[pt]
        previous_low = lows[pt-1]

        if current_low > previous_low:
                bear_reversion.append(bear_times[pt].strftime('%Y-%m-%d %H:%M:%S'))

    #return latest time point detected
    return bull_reversion[-1:], bear_reversion[-1:]

#function for sending notification via discord bot
def bot_signal(ticker, data, bull = True):
    #discord webhook url
    bot_url = 'your-discord-bot-webhook-url'
    if bull:
        message = {"content": "{}: Last BULL timing is {}".format(ticker, data)}
    else:
        message = {"content": "{} Last BEAR timing is {}".format(ticker, data)}

    #sending message to bot
    response = requests.post(bot_url, json=message)

    if response.status_code == 204:
        print(f"Message sent at {datetime.datetime.now()}")
    else:
        print(f"Failed to send message: {response.status_code} - {response.text} at {datetime.datetime.now()}")

#function for changing number into HK stock code for yfinance
def convert_hk(stock_code):
    stock_code = str(stock_code).strip()
    if stock_code.endswith('.HK'):
        return stock_code.upper()
    #fill zero before the stock number
    stock_code_padded = stock_code.zfill(4)
    return f"{stock_code_padded}.HK"