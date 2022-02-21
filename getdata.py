import datetime

import yfinance as yf  # Yahoo Finance python API
import fredapi  # FRED python API
import pytrends  # Google Trends python API
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
import mplfinance as mpf
from matplotlib.dates import DateFormatter
import datetime as dt
import requests
import time
import os



# 貼上連結
url = 'https://www.slickcharts.com/sp500'
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}


def downloadstocklist_from_slickcharts(url, headers):
    request = requests.get(url, headers=headers)
    data = pd.read_html(request.text)[0]
    stk_list = data.Symbol.apply(lambda x: x.replace('.', '-'))  # 用 replace 將符號進行替換
    print(data)
    return stk_list


'''
取得各種資料
# get stock info
msft.info

# get historical market data
hist = msft.history(period="max")

# show actions (dividends, splits)
msft.actions

# show dividends
msft.dividends

# show splits
msft.splits

# show financials
msft.financials
msft.quarterly_financials

# show major holders
msft.major_holders

# show institutional holders
msft.institutional_holders

# show balance sheet
msft.balance_sheet
msft.quarterly_balance_sheet

# show cashflow
msft.cashflow
msft.quarterly_cashflow

# show earnings
msft.earnings
msft.quarterly_earnings

# show sustainability
msft.sustainability

# show analysts recommendations
msft.recommendations

# show next event (earnings, etc)
msft.calendar

# show ISIN code - *experimental*
# ISIN = International Securities Identification Number
msft.isin

# show options expirations
msft.options

# show news
msft.news
'''


def download_marketdata(stock_list):
    ticker = stock_list[0]
    stock_basic_data = yf.Ticker(ticker).info

    # 將 yfinance 有提供的數據項目取出存在 info_columns，它將會成為 stock_info_df 這張總表的欄位項目
    info_columns = list(stock_basic_data.keys())

    # 創立一個名為 stock_info_df 的總表，用來存放所有股票的基本資料！其中 stk_list 是我們先前抓到的股票代碼喔！
    stock_info_df = pd.DataFrame(index=stock_list.sort_values(), columns=info_columns)

    # 創立一個紀錄失敗股票的 list
    failed_list = []

    for i in stock_info_df.index:
        try:
            # 打印出目前進度
            print('processing: ' + i)
            # 抓下來的資料暫存成 dictionary
            info_dict = yf.Ticker(i).info
            # 由於 yahoo finance 各檔股票所提供的欄位項目都不一致！所以這邊要針對每一檔股票分別取出欄位項目
            columns_included = list(info_dict.keys())
            # 因為在別檔公司裡有著 AAPL 裡所沒有的會計科目，因此要取兩家公司會計科目的交集
            intersect_columns = [x for x in info_columns if x in columns_included]
            # 有了該股欄位項目後，就可順利填入總表中相對應的位置
            stock_info_df.loc[i, intersect_columns] = list(pd.Series(info_dict)[intersect_columns].values)
            # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
            time.sleep(1)
        except:
            failed_list.append(i)
            continue
    print(stock_info_df)
    return stock_info_df


def ToExcel(path, excelname, df1, sheetname1):
    path = os.path.join(path, excelname)  # 設定路徑及檔名
    writer = pd.ExcelWriter(path, engine='openpyxl')  # 指定引擎openpyxl
    df1.to_excel(writer, sheet_name=sheetname1)  # 存到指定的sheet
    writer.save()  # 存檔生成excel檔案


def historyprice(ticker, startdate, enddate, interval):
    symbol = yf.Ticker(ticker)
    history = symbol.history(period="max"  # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                             , interval=interval)  # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    history = history[['Open', 'High', 'Low', 'Close', 'Volume']]
    history = history[startdate:enddate]
    print(history)
    return history


def tickernews(ticker):
    news = pd.DataFrame(yf.Ticker(ticker).news)
    PublishTime = []
    for x in news['providerPublishTime']:
        PublishTime.append(datetime.datetime.fromtimestamp(x))
    news['PublishTime'] = PublishTime
    news.set_index('PublishTime', inplace=True)
    news = news[['title', 'publisher', 'link']]
    return news


def tickerrec(ticker, startdate, enddate):
    rec = pd.DataFrame(yf.Ticker(ticker).recommendations[startdate:enddate])
    return rec


def plotprice(history, ticker):
    mpf.plot(history, type='candle', style='binance', title=ticker, mav=(20, 60), volume=True, warn_too_much_data=3000)


if __name__ == '__main__':
    ticker = 'AAPL'
    startdate = '2018-01-04'
    enddate = '2022-02-18'
    interval = '1d'
    print(historyprice(ticker, startdate, enddate, interval))


    # print(tickernews(ticker))
    # print(tickerrec(ticker, startdate, enddate))
    # print(yf.Ticker(ticker).financials)


    # stock_list = downloadstocklist_from_slickcharts(url, headers)
    # stk_info_df = download_marketdata(stock_list[0:3])
    # ToExcel(os.getcwd(), 'marketdata.xlsx', stk_info_df, 'data')
