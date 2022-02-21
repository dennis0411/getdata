import yfinance as yf  # Yahoo Finance python API
import pandas as pd
import numpy as np


class portfolio_performance():

    def __init__(self, portfolio, period):
        self.portfolio = portfolio
        self.start = period.get('start')
        self.end = period.get('end')
        self.interval = period.get('interval')
        self.investamount = 1000000
        self.stklist = list(self.portfolio.keys())[:-1]


    def downloadprice(self):
        history = yf.download(self.stklist, interval=self.interval, start=self.start, end=self.end)
        history = history['Close']
        return history

    @staticmethod
    def pricechange(self):
        history = portfolio_performance.downloadprice(self)
        pricechange = history.pct_change().dropna()
        return pricechange

    @staticmethod
    def performance(self):
        pricechg = portfolio_performance.pricechange(self)
        r = pricechg.add(1).cumprod()
        r['CASH'] = 1
        weight = []
        for i in r.columns:
            weight.append(self.portfolio.get(i))
        weight = np.array(weight)
        weightreturn = r.mul(weight)
        r['Performance'] = weightreturn.sum(axis=1)
        r['Netvalue'] = r['Performance'] * self.investamount
        return r

    @staticmethod
    def return_risk(self):
        r = portfolio_performance.performance(self)
        r = r['Performance']
        dd = r.div(r.cummax()).sub(1)
        mdd = dd.min()
        end = dd.idxmin()
        start = r.loc[:end].idxmax()
        days = end-start
        print(f'最大跌幅:{mdd:.1%}, 起跌日:{start:%Y-%m-%d}, 止跌日:{end:%Y-%m-%d}, 下跌時間:{days}')
        return mdd, start, end, days






if __name__ == '__main__':
    portfolio = {'SPY': 0.5,
                 'AGG': 0.2,
                 'AAPL': 0.2,
                 'CASH': 0.1}
    period = {'start': '2010-12-31',
              'end': '2021-12-31',
              'interval': '1d'}
    portfolio = portfolio_performance(portfolio, period)
    print(portfolio.downloadprice())
    print(portfolio.pricechange(self=portfolio))
    print(portfolio.performance(self=portfolio))
    portfolio.return_risk(self=portfolio)
