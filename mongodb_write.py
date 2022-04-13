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
import requests
import ffn
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


def write_ticker_with_sector(name):
    start = time.time()
    df = pd.DataFrame(downloadstocklist_from_slickcharts())

    for symbol in df["Symbol"]:
        try:
            stock = finvizfinance(symbol)
            stock_fundament = stock.ticker_fundament()
            sector = stock_fundament['Sector']
            df.loc[df[df['Symbol'] == symbol].index, 'Sector'] = sector
        except:
            pass
    df = df.dropna()
    data = json.loads(df.to_json())
    db = client.getdata
    collection = db.ticker
    collection.insert_one({'name': name, 'date': datetime.date.today().strftime("%Y/%m/%d"), 'data': data})
    end = time.time()
    print(f'write_ticker_with_sector total time: {end - start} seconds')


def downloadstocklist_from_slickcharts():
    url = 'https://www.slickcharts.com/sp500'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    request = requests.get(url, headers=headers)
    data = pd.read_html(request.text)[0]
    stk_list = data.Symbol.apply(lambda x: x.replace('.', '-'))  # 用 replace 將符號進行替換
    return stk_list


def write_return_mdd(name, start_date, end_date):
    start = time.time()
    db = client.getdata
    collection = db.ticker
    result = collection.find_one({'name': 'SPX'})
    data = pd.DataFrame(result['data'])
    data = data.dropna()
    for symbol in data['Symbol']:
        try:
            data.loc[data[data['Symbol'] == symbol].index, 'total_return'] = ffn.get(symbol, start=start_date,
                                                                                     end=end_date).calc_total_return().values
            data.loc[data[data['Symbol'] == symbol].index, 'max_drowdown'] = ffn.get(symbol, start=start_date,
                                                                                     end=end_date).calc_max_drawdown().values
        except:
            pass
    df = data.dropna()
    print(df)
    data = json.loads(df.to_json())
    collection.insert_one({'name': name, 'date': datetime.date.today().strftime("%Y/%m/%d"), 'data': data})
    end = time.time()
    print(f'write_return_mdd total time: {end - start} seconds')


if __name__ == "__main__":
    # write_bb('data.csv')
    # write_ticker_with_sector('SPX')
    start_date = '2015-12-15'
    end_date = '2016-03-31'
    name = 'rate hike'
    write_return_mdd(name, start_date, end_date)

    # df = pd.read_csv('Ticker.csv')
    # df = df.dropna()
    # tickers = list(df.Ticker[:])
    # write_ticker(tickers, 'US Stock')
    # print(type(str(datetime.date.today())))
