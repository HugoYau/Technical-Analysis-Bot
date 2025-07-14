import myfun
import time

#select market to monitor
market = myfun.ask_session()
#select ticker of stock
tickers = myfun.ask_stock(market)
#initial stock data
stock_data = myfun.update_data(tickers)
#stop repeating notification
bull_noti = {ticker: None for ticker in tickers}
bear_noti = {ticker: None for ticker in tickers}

while True:
    for ticker in tickers:
        #checking if there is any signal of Major Trend Reversion
        signal = myfun.MTR_check(stock_data[ticker])
        bull_signal = signal[1] #bear reversion implies bull signal
        bear_signal = signal[0] #bull reversion implies bear signal
        #only send the signal for first time and not sending repeat messages
        if (bull_noti[ticker] != bull_signal) and (bull_signal != ''):
            bull_noti[ticker] = bull_signal
            myfun.bot_signal(ticker, bull_signal, bull=True)
        if (bear_noti[ticker] != bear_signal) and (bear_signal != ''):
            bear_noti[ticker] = bear_signal
            myfun.bot_signal(ticker, bear_signal, bull = False)
    time.sleep(300)
    #update data and redo analysis
    stock_data = myfun.update_data(tickers)
