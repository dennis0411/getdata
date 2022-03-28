import pprint
import threading
import time
import pandas as pd
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
from pymongo import MongoClient
import os

'''
source : https://pypi.org/project/finvizfinance/
'''

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# 取消 future warning
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

# 引入密碼
path = "mongodb_password"
with open(path) as f:
    account = f.readline().split(',')[0]
    password = f.readline().split(',')[1]

# mongodb connection
CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
db = client.getdata
collection_name = db.fundament

df = pd.read_csv('foverview')
tickers = df.Ticker[:]

start = time.time()

for ticker in tickers:
    data = {ticker: finvizfinance(ticker).ticker_fundament()}
    collection_name.insert_one(data)

end = time.time()
print(f'total time: {end - start} seconds')
