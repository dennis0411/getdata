import json
import pprint
import time
import pandas as pd
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
from pymongo import MongoClient
from warnings import simplefilter
import datetime
import yfinance as yf  # Yahoo Finance python API

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# 取消 future warning


simplefilter(action='ignore', category=FutureWarning)

# 引入密碼
path = "mongodb_password"
with open(path) as f:
    word = f.readline().split(',')
    account = word[0]
    password = word[1]

# mongodb connection
CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)


def write_fundament(tickers):
    start = time.time()
    db = client.getdata
    collection = db.fundament
    collection.delete_many({})

    for ticker in tickers:
        data = finvizfinance(ticker).ticker_fundament()
        data['Ticker'] = ticker
        collection.insert_one(data)

    end = time.time()
    print(f'write_fundament total time: {end - start} seconds')


def write_ticker(tickers, name):
    start = time.time()
    db = client.getdata
    collection = db.ticker
    collection.insert_one({'name': name, 'date': datetime.date.today().strftime("%Y/%m/%d"), 'tickers': tickers})
    end = time.time()
    print(f'write_ticker total time: {end - start} seconds')


def write_bb(file):
    start = time.time()
    db = client.getdata
    collection = db.bb
    df = pd.read_csv(file)
    data = json.loads(df.to_json())  # 到底為何要這樣處理??
    collection.insert_one({'name': 'spx', 'date': datetime.date.today().strftime("%Y/%m/%d"), 'data': data})
    end = time.time()
    print(f'write_bb total time: {end - start} seconds')


if __name__ == "__main__":
    write_bb('data.csv')
    # df = pd.read_csv('Ticker.csv')
    # df = df.dropna()
    # tickers = list(df.Ticker[:])
    # write_ticker(tickers, 'US Stock')
    # print(type(str(datetime.date.today())))
