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



# def write_news():
#     start = time.time()
#     db = client.getdata
#     collection = db.bb
#
#     self.url = "https://news.cnyes.com"
#     self.news_url = {"us_stock": "/news/cat/us_stock",
#                      "world_stock": "/news/cat/wd_stock",
#                      "eu_asia_stock": "/news/cat/eu_asia_stock",
#                      "taiwan_stock": "/news/cat/tw_stock",
#                      "china_stock": "/news/cat/cn_stock",
#                      "crypto": "/news/cat/bc",
#                      "currency": "/news/cat/forex",
#                      "futures": "/news/cat/future",
#                      }
#     self.news_data = pd.DataFrame()
#
# def get_url_list(self):
#     url_list = []
#     market_list = []
#     for submarket in self.news_url.keys():
#         target_url = self.url + self.news_url.get(submarket)
#         r = requests.get(target_url)
#         soup = BeautifulSoup(r.text, 'html.parser')
#         for tag in soup.find_all(class_="_1Zdp"):
#             href = tag.get('href')
#             link = self.url + href
#             url_list.append(link)
#             market_list.append(submarket)
#     self.news_data["market"] = market_list
#
#     return url_list
#
# def download_data(self, target_url):
#     r = requests.get(target_url)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     news = " "
#     tag = soup.find('time')
#     datetime = tag.text.split(' ')
#     t = datetime[1]
#     d = datetime[0]
#     source = 'cnyes'
#     title = soup.h1.text
#
#     for sub_tag in soup.find(class_="_1UuP"):
#         for p in sub_tag.find_all('p'):
#             a = p.text
#             news += a
#
#     data = {"target_url": target_url,
#             "time": t,
#             "date": d,
#             "source": source,
#             "title": title,
#             "news": news,
#             "link": target_url,
#             "market":}
#
# def multi(self, url_list):
#     threads = []
#     for target_url in url_list:
#         threads.append(threading.Thread(target=self.download_data, args=(target_url,)))
#
#     for thread in threads:
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
# def write_db(self):
#     print(f'Loading data from cnyes')
#     list = self.get_url_list()
#     self.multi(list)



if __name__ == "__main__":
    write_bb('data.csv')
    # df = pd.read_csv('Ticker.csv')
    # df = df.dropna()
    # tickers = list(df.Ticker[:])
    # write_ticker(tickers, 'US Stock')
    # print(type(str(datetime.date.today())))
