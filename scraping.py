import pandas as pd
import requests
from bs4 import BeautifulSoup
import pickle
import myfun

#####  For S&P500  #####
#Method 1: directly reading from wiki
#link of wikipedia about stocks in S&P500
wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'

#check availability of the website
response = requests.get(wiki_url)
response.raise_for_status()

#get the first table (consisting stocks data)
table = pd.read_html(response.text)
sp500 = table[0]
tickers = sp500['Symbol'].tolist() #extract the ticker only

#Method 2: alternative when pd.read_html is not working
# #set up directory to wikipedia
# soup = BeautifulSoup(response.text, 'html.parser')
# #find the table with constituents of S&P500
# table = soup.find('table', {'id' : 'constituents'})
# #get all row in table
# num_ticker = table.find_all('tr')
# #loop for getting all ticker
# tickers = []
# for ticker in num_ticker[1:]:
#     cols = ticker.find_all('td')
#     if len(cols) > 0:
#         symbol = cols[0].text.strip()
#         tickers.append(symbol)

with open('sp500_tickers.pickle', 'wb') as file:
    pickle.dump(tickers, file)
    print("S&P500 Updated")

##### For Hang Seng Index #####
#Method 1: directly reading
#link of wikipedia about stocks in S&P500
wiki_url = 'https://en.wikipedia.org/wiki/Hang_Seng_Index'

#check availability of the website
response = requests.get(wiki_url)
response.raise_for_status()

#get the table (consisting stocks data)
table = pd.read_html(response.text)
hsi = table[6]
#change the ticker to number
tickers = hsi['Ticker'].str.replace('SEHK:\xa0', '').tolist() #change the SEHK: to null
hkticker = []
#change the ticker to XXXX.HK for yfinance
for ticker in tickers:
    nticker = myfun.convert_hk(ticker)
    hkticker.append(nticker)

with open('hsi_tickers.pickle', 'wb') as file:
    pickle.dump(hkticker, file)
    print("HSI Updated")

#####  For Hong Kong Listed  #####
#read the data from our excel with all listed securities in HKEX
hk = pd.read_excel("ListOfSecurities.xlsx", skiprows = 2, usecols = ['Stock Code', 'Category'])

hk_ticker = []
for index, row in hk.iterrows():
    #get stock, etf and reits only
    if ((row['Category'] == 'Equity') or
            (row['Category'] == 'Exchange Traded Products') or
            (row['Category'] == 'Real Estate Investment Trusts')):
        ticker = myfun.convert_hk(row['Stock Code'])
        hk_ticker.append(ticker)

with open('hk_tickers.pickle', 'wb') as file:
    pickle.dump(hk_ticker, file)
    print("HK Listed Updated")
