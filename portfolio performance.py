import yfinance as yf  # Yahoo Finance python API
import pandas as pd
import numpy as np


class portfolio_performance():
    value = []

    def __init__(self, portfolio, period):
        self.portfolio = portfolio
        self.start = period.get('start')
        self.end = period.get('end')
        self.interval = period.get('interval')
        self.cash = 1000000
        self.list = list(self.portfolio.keys())[:-1]



    def downloadprice(self):
        # ticker = list(self.portfolio.keys())
        # ticker = ticker[:-1]
        history = yf.download(self.list, interval=self.interval, start=self.start, end=self.end)
        history = history['Close']
        return history

    @staticmethod
    def performance(self):
        history = portfolio_performance.downloadprice(self)
        pricechg = history.pct_change().dropna()
        r = pricechg.add(1).cumprod()
        v = self.cash * self.portfolio.get("CASH")
        for stk in self.list:
            v += r[stk] * self.portfolio.get(stk) * self.cash
        self.value.append(v)
        return r



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
    print(portfolio.performance(self=portfolio))
    print(portfolio.value)
