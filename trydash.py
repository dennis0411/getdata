import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pymongo import MongoClient
from utils import Header, make_dash_table
from warnings import simplefilter
import numpy as np
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
import yfinance as yf  # Yahoo Finance python API
import pandas as pd
import ffn

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

# make app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
)
app.title = "Financial Report"
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


# function
def write_description(ticker):
    stock_description = finvizfinance(ticker).ticker_description()
    return stock_description


def write_recommendations(ticker, rec_startdate, enddate):
    data_yf = yf.Ticker(ticker).recommendations[rec_startdate:enddate]
    data_fv = finvizfinance(ticker).ticker_outer_ratings()
    return data_yf, data_fv


def write_financial(ticker):
    data_y = yf.Ticker(ticker).financials
    data_q = yf.Ticker(ticker).quarterly_financials
    return data_y, data_q


def write_rebase(ticker, benchmark, rebase_date, end_date):
    portfolio_list = list([ticker, benchmark])
    prices = ffn.get(portfolio_list, start=rebase_date, end=end_date)
    rebase = prices.rebase()
    return rebase


def create_layout(app):
    pass


# data
ticker = 'aapl'
rebase_date = '2010-01-01'
rec_start_date = '2021-01-01'
end_date = '2022-03-24'
benchmark = "spy"

if __name__ == "__main__":
    a, b = write_recommendations(ticker, rec_start_date, end_date)
    print(a)
    print(b)
    # app.run_server(debug=True)

