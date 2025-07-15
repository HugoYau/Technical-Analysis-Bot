import myfun
import time

#select ticker of stock
tickers = myfun.ask_stock()
#select method for analysis
move = myfun.ask_method()
#initial stock data
stock_data = myfun.update_data(tickers)
#stop repeating notification
MTR_bull_noti = {ticker: None for ticker in tickers}
MTR_bear_noti = {ticker: None for ticker in tickers}
X_bull_noti = {ticker: None for ticker in tickers}
X_bear_noti = {ticker: None for ticker in tickers}

while True:
    for ticker in tickers:
        #detect MTR pattern
        if (move == "MTR") or (move == "All"):
            #checking if there is any signal of Major Trend Reversion
            signal = myfun.MTR_check(stock_data[ticker])
            bull_signal = signal[1] #bear reversion implies bull signal
            bear_signal = signal[0] #bull reversion implies bear signal
            #only send the signal for first time and not sending repeat messages
            if (MTR_bull_noti[ticker] != bull_signal) and (bull_signal != ''):
                MTR_bull_noti[ticker] = bull_signal
                myfun.bot_signal(ticker, bull_signal,'MTR', bull = True)
            if (MTR_bear_noti[ticker] != bear_signal) and (bear_signal != ''):
                MTR_bear_noti[ticker] = bear_signal
                myfun.bot_signal(ticker, bear_signal,'MTR', bull = False)

        #detect golden cross or death cross
        if (move == "Cross") or (move == "All"):
            #checking if there is any crossing
            signal = myfun.Cross(stock_data[ticker])
            bull_signal = signal[0] #golden cross implies bull signal
            bear_signal = signal[1] #death cross implies bear signal
            #only send the signal for first time and not sending repeat messages
            if (X_bull_noti[ticker] != bull_signal) and (bull_signal != ''):
                X_bull_noti[ticker] = bull_signal
                myfun.bot_signal(ticker, bull_signal,'Cross', bull = True)
            if (X_bear_noti[ticker] != bear_signal) and (bear_signal != ''):
                X_bear_noti[ticker] = bear_signal
                myfun.bot_signal(ticker, bear_signal,'Cross', bull = False)
    #wait for 5 mins
    time.sleep(300)
    #update data and redo analysis
    stock_data = myfun.update_data(tickers)
