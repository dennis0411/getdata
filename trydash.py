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
import plotly.express as px
import plotly.graph_objects as go

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


# function
def write_description(ticker):
    stock_description = finvizfinance(ticker).ticker_description()
    return stock_description


def write_recommendations(ticker, rec_startdate, enddate):
    data_yf = yf.Ticker(ticker).recommendations[rec_startdate:enddate]
    data_fv = finvizfinance(ticker).ticker_outer_ratings()
    return data_yf, data_fv


# def write_financial(ticker, period='Y'):
#     if period == "Y":
#         data = yf.Ticker(ticker).financials.T.rename_axis('Date').reset_index()
#     else:
#         data = yf.Ticker(ticker).quarterly_financials.T.rename_axis('Date').reset_index()
#     return data


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
rec_startdate = '2021-01-01'
enddate = '2022-03-24'
benchmark = "spy"

if __name__ == "__main__":
    # mongodb connection
    CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
    db = client.getdata
    collection = db.fundament

    # make app
    app = dash.Dash()
    app.layout = html.Div([
        html.H4('Financial Overview'),
        dcc.Input(
            id="input",
            type="text",
            value='AAPL',
            placeholder="",
        ),
        dcc.Dropdown(
            id="dropdown",
            options=['Income Before Tax', 'Net Income',
                     'Selling General Administrative', 'Gross Profit', 'Ebit',
                     'Operating Income', 'Other Operating Expenses', 'Interest Expense',
                     'Extraordinary Items', 'Non Recurring', 'Other Items',
                     'Income Tax Expense', 'Total Revenue', 'Total Operating Expenses',
                     'Cost Of Revenue', 'Total Other Income Expense Net',
                     'Discontinued Operations', 'Net Income From Continuing Ops',
                     'Net Income Applicable To Common Shares'],
            value='Total Revenue',
            clearable=False,
        ),
        dcc.Graph(id="graph"),
        dcc.Dropdown(
            id="dropdown2",
            options=['P/E', 'EPS (ttm)', 'Insider Own', 'Shs Outstand', 'Perf Week',
                     'Forward P/E', 'EPS next Y', 'Insider Trans',
                     'Perf Month', 'Income', 'PEG', 'EPS next Q', 'Inst Own', 'Short Float',
                     'Perf Quarter', 'Sales', 'P/S', 'EPS this Y', 'Inst Trans', 'Short Ratio',
                     'Perf Half Y', 'Book/sh', 'P/B', 'ROA', 'Perf Year', 'Cash/sh',
                     'P/C', 'EPS next 5Y', 'ROE', '52W Range From', '52W Range To', 'Perf YTD', 'Dividend',
                     'P/FCF', 'EPS past 5Y', 'ROI', '52W High', 'Beta', 'Dividend %', 'Quick Ratio',
                     'Sales past 5Y', 'Gross Margin', '52W Low', 'ATR', 'Current Ratio',
                     'Sales Q/Q', 'Oper. Margin', 'RSI (14)', 'Volatility W', 'Volatility M',
                     'Debt/Eq', 'EPS Q/Q', 'Profit Margin', 'Rel Volume', 'LT Debt/Eq',
                     'Earnings', 'Payout', 'Avg Volume', 'Price', 'Recom', 'SMA20', 'SMA50', 'SMA200', 'Volume',
                     'Change'],
            value='P/E',
            clearable=False,
        ),
        dcc.Dropdown(
            id="dropdown3",
            options=['P/E', 'EPS (ttm)', 'Insider Own', 'Shs Outstand', 'Perf Week',
                     'Forward P/E', 'EPS next Y', 'Insider Trans',
                     'Perf Month', 'Income', 'PEG', 'EPS next Q', 'Inst Own', 'Short Float',
                     'Perf Quarter', 'Sales', 'P/S', 'EPS this Y', 'Inst Trans', 'Short Ratio',
                     'Perf Half Y', 'Book/sh', 'P/B', 'ROA', 'Perf Year', 'Cash/sh',
                     'P/C', 'EPS next 5Y', 'ROE', '52W Range From', '52W Range To', 'Perf YTD', 'Dividend',
                     'P/FCF', 'EPS past 5Y', 'ROI', '52W High', 'Beta', 'Dividend %', 'Quick Ratio',
                     'Sales past 5Y', 'Gross Margin', '52W Low', 'ATR', 'Current Ratio',
                     'Sales Q/Q', 'Oper. Margin', 'RSI (14)', 'Volatility W', 'Volatility M',
                     'Debt/Eq', 'EPS Q/Q', 'Profit Margin', 'Rel Volume', 'LT Debt/Eq',
                     'Earnings', 'Payout', 'Avg Volume', 'Price', 'Recom', 'SMA20', 'SMA50', 'SMA200', 'Volume',
                     'Change'],
            value='ROE',
            clearable=False,
        ),
        dcc.Graph(id="graph2"),
    ])


    @app.callback(
        Output("graph", "figure"),
        Input("input", "value"),
        Input("dropdown", "value"))
    def write_financial(input, dropdown):
        data = yf.Ticker(input).financials.T.rename_axis('Date').reset_index()
        fig = px.bar(data, x='Date', y=dropdown, title=f"{input} Financials")

        return fig


    @app.callback(
        Output("graph2", "figure"),
        Input("input", "value"),
        Input("dropdown2", "value"),
        Input("dropdown3", "value"))
    def write_bubble(input, dropdown2, dropdown3):
        symbol = collection.find_one(filter={'Ticker': input})
        data = collection.find(filter={'Sector': symbol['Sector']})
        data1 = []
        data2 = []
        data3 = []
        for a in data:
            data1.append(a[dropdown2])
            data2.append(a[dropdown3])
            data3.append(a['Ticker'])
        result = pd.DataFrame(zip(data1, data2, data3), columns=[dropdown2, dropdown3, 'Ticker'])
        fig = px.scatter(result, x=result[dropdown2], y=result[dropdown3], hover_name='Ticker', log_x=True)
        fig.update_layout(autotypenumbers='convert types')

        return fig


    # symbol = collection.find_one(filter={'Ticker': 'AAPL'})
    # data = collection.find(filter={'Sector': symbol['Sector']})
    #
    # data1 = []
    # data2 = []
    # data3 = []
    # for a in data:
    #     data1.append(a[dropdown2])
    #     data2.append(a[dropdown3])
    #     data3.append(a['Ticker'])
    # result = pd.DataFrame(zip(data1, data2, data3), columns=[dropdown2, dropdown3, 'Ticker'])
    # result.sort_values(by=dropdown2)
    #
    #
    # fig = px.scatter(result, x=result[dropdown2], y=result[dropdown3], hover_name='Ticker', log_x=True)
    # fig.update_layout(autotypenumbers='convert types')
    #
    # app.layout = html.Div([
    #     dcc.Graph(figure=fig)
    # ])

    # run server
    app.run_server(debug=True)
