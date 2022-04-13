import pandas as pd
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview



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




# Quote
stock = finvizfinance('BLK')

# Fundament
stock_fundament = stock.ticker_fundament()
print(stock_fundament['Sector'])

# Description
stock_description = stock.ticker_description()
print(stock_description)

# Chart
# chart = stock.ticker_charts()
# print(f'Chart link: {chart}')

# Insider
finsider = Insider(option='top owner trade')
print(finsider.get_insider().head())

# outer_ratings
outer_ratings_df = stock.ticker_outer_ratings()
print(outer_ratings_df)

# News
# fnews = News()
# all_news = fnews.get_news()
# print(all_news)

# Screener
foverview = Overview()
filters_dict = {'Market Cap.': '+Small (over $300mln)'
                }
# filters_dict = {'Index': 'S&P 500',
#                 'Market Cap.': 'Large ($10bln to $200bln)',
#                 'Analyst Recom.': 'Buy',
#                 'Price': 'Over $10',
#                 'RSI (14)': "Oversold (40)"}
foverview.set_filter(filters_dict=filters_dict)
# df = foverview.screener_view()
# print(df)
# df.to_csv('over300mln')


