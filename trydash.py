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
import datetime
from datetime import date
from plotly.subplots import make_subplots

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


def create_layout(app):
    pass


# mongodb connection
CONNECTION_STRING = f"mongodb+srv://{account}:{password}@getdata.dzc20.mongodb.net/getdata?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING, tls=True, tlsAllowInvalidCertificates=True)
db = client.getdata

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
    dcc.Graph(id="graph"),
    dcc.Dropdown(
        id="dropdown2",
        options=['市值', 'P/E', '總營收', 'EPS', '營收成長率', 'EPS 成長率', '資產成長率', '淨利成長率', 'EBITDA 成長率', '投入資本報酬率',
                 '自由現金流量成長率', '總資本支出成長率', 'P/B', '現金比率', 'P/S', '總投入資本營運報酬率', '普通股權益報酬率', '總債務/總資產', '毛利率', '獲利率'],
        value='營收成長率',
        clearable=False,
    ),
    dcc.Dropdown(
        id="dropdown3",
        options=['市值', 'P/E', '總營收', 'EPS', '營收成長率', 'EPS 成長率', '資產成長率', '淨利成長率', 'EBITDA 成長率', '投入資本報酬率',
                 '自由現金流量成長率', '總資本支出成長率', 'P/B', '現金比率', 'P/S', '總投入資本營運報酬率', '普通股權益報酬率', '總債務/總資產', '毛利率', '獲利率'],
        value='EPS 成長率',
        clearable=False,
    ),
    dcc.Graph(id="graph2"),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2014, 1, 1),
        max_date_allowed=date.today() - datetime.timedelta(1),
        initial_visible_month=date(2022, 1, 1),
        start_date=date(2021, 1, 1),
        end_date=date.today() - datetime.timedelta(1)
    ),
    html.Div(id='output-container-date-picker-range'),
    dcc.Graph(id="graph3"),
    dcc.Input(
        id="input-rate-hike",
        value=None,
        type='number',
        max=0,
        step=0.1,
        placeholder="Max Drowdown Limit"
    ),
    dcc.Graph(id="graph-rate-hike"),
])


@app.callback(
    Output("graph", "figure"),
    Input("input", "value"))
def write_financial(input):
    data = yf.Ticker(input).financials.T.rename_axis('Date').reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data['Date'],
                         y=data['Total Revenue'],
                         name='營收',
                         marker=dict(color='#38A67C',
                                     )))
    fig.add_trace(go.Bar(x=data['Date'],
                         y=data['Gross Profit'],
                         name='毛利',
                         marker=dict(color='#006FA6',
                                     )))
    fig.add_trace(go.Bar(x=data['Date'],
                         y=data['Net Income'],
                         name='淨利',
                         marker=dict(color='#CCCCCC',
                                     )))
    fig.update_layout(title=f'{input} financial',
                      xaxis=dict(gridcolor='white',
                                 gridwidth=2,
                                 ),
                      yaxis=dict(gridcolor='white',
                                 gridwidth=2,
                                 ),
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',
                      )
    fig.update_layout(autotypenumbers='convert types')

    return fig


@app.callback(
    Output("graph2", "figure"),
    Input("input", "value"),
    Input("dropdown2", "value"),
    Input("dropdown3", "value"))
def write_bubble(input, dropdown2, dropdown3):
    collection = db.bb
    result = collection.find_one({'name': 'spx'})
    data = pd.DataFrame(result['data'])
    data = data[[dropdown2, dropdown3, 'Ticker', '市值', '總營收', '產業']].dropna()
    data = data.drop(data[data[dropdown2] == 'nodata'].index)
    data = data.drop(data[data[dropdown3] == 'nodata'].index)

    # hover_text
    hover_text = []
    for index, row in data.iterrows():
        hover_text.append((f"{row['Ticker']}<br>" +
                           f"市值 (mln): {row['市值'] / 1000000}<br>" +
                           f"總營收 (mln): {row['總營收'] / 1000000}<br>" +
                           f"產業: {row['產業']}<br>" +
                           f"{dropdown2}: {row[dropdown2]}<br>" +
                           f"{dropdown3}: {row[dropdown3]}<br>"))
    data['hover_text'] = hover_text

    # size
    size = data['市值']
    sizeref = 2. * max(size) / (100 ** 2)

    # data
    sector = data[data['Ticker'] == input]['產業'].values.item()
    data_sector = data[data['產業'] == sector]
    data_ticker = data[data['Ticker'] == input]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data[dropdown2],
                             y=data[dropdown3],
                             text=data['hover_text'],
                             name='標普五百',
                             mode='markers',
                             marker=dict(size=data['市值'],
                                         color='#CCCCCC',
                                         sizemode='area',
                                         sizeref=sizeref
                                         )
                             )
                  )
    fig.add_trace(go.Scatter(x=data_sector[dropdown2],
                             y=data_sector[dropdown3],
                             text=data_sector['hover_text'],
                             name=f'{sector}',
                             mode='markers',
                             marker=dict(size=data_sector['市值'],
                                         color='#38A67C',
                                         sizemode='area',
                                         sizeref=sizeref
                                         )
                             )
                  )
    fig.add_trace(go.Scatter(x=data_ticker[dropdown2],
                             y=data_ticker[dropdown3],
                             name=input,
                             text=data_ticker['hover_text'],
                             mode='markers',
                             marker=dict(size=data_ticker['市值'],
                                         color='#006FA6',
                                         sizemode='area',
                                         sizeref=sizeref
                                         )
                             )
                  )

    fig.update_layout(title=f'{dropdown2} vs {dropdown3}',
                      xaxis=dict(title=f'{dropdown2}',
                                 gridcolor='white',
                                 gridwidth=2,
                                 ),
                      yaxis=dict(title=f'{dropdown3}',
                                 gridcolor='white',
                                 gridwidth=2,
                                 ),
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',
                      )
    fig.update_layout(autotypenumbers='convert types')

    return fig


@app.callback(
    Output("graph3", "figure"),
    Input("input", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def write_performance(input, start_date, end_date):
    data = ffn.get([input, 'spy'], start=start_date, end=end_date).rebase()
    fig = go.Figure()
    hover_input = []
    for index, row in data.iterrows():
        hover_input.append((f"{index.strftime('%Y-%m-%d')}<br>" +
                            f"{input}<br>" +
                            f"{round(row[str(input).lower()], 2)}<br>"
                            ))
    fig.add_trace(go.Scatter(x=data.index,
                             y=data[str(input).lower()],
                             mode='lines',
                             name=input,
                             text=hover_input,
                             line=dict(color="#006FA6",
                                       width=2)
                             )
                  )

    hover_spy = []
    for index, row in data.iterrows():
        hover_spy.append((f"{index.strftime('%Y-%m-%d')}<br>" +
                          f"SPY<br>" +
                          f"{round(row['spy'], 2)}<br>"
                          ))
    fig.add_trace(go.Scatter(x=data.index,
                             y=data['spy'],
                             mode='lines',
                             name='SPY',
                             text=hover_spy,
                             line=dict(color="#B0B0B0",
                                       width=2)
                             )
                  )
    fig.update_xaxes(
        rangeslider_visible=False,
        title=f'{input} vs spy'
    )
    fig.update_layout(title=f'{input} vs spy base on $100',
                      xaxis=dict(gridcolor='white',
                                 gridwidth=2,
                                 ),
                      yaxis=dict(gridcolor='white',
                                 gridwidth=2,
                                 ),
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',
                      )
    return fig


@app.callback(
    Output("graph-rate-hike", "figure"),
    Input("input-rate-hike", "value"),
)
def update_rate_hike(value):
    # data
    collection = db.ticker
    result = collection.find_one({'name': 'rate hike'})
    data = pd.DataFrame(result['data'])
    data = data.dropna()

    data = data[data['max_drowdown'] > value] if value != None else data

    # fig
    fig = px.scatter(data, x="max_drowdown", y="total_return", color="Sector", hover_name='Symbol')

    fig.update_layout(title=f'Performance when Rate Hike',
                      xaxis=dict(title='max_drowdown',
                                 gridcolor='white',
                                 gridwidth=2,
                                 ),
                      yaxis=dict(title='total_return',
                                 gridcolor='white',
                                 gridwidth=2,
                                 ),
                      paper_bgcolor='rgb(243, 243, 243)',
                      plot_bgcolor='rgb(243, 243, 243)',
                      )
    fig.update_layout(autotypenumbers='convert types')

    return fig


if __name__ == "__main__":
    # run server
    app.run_server(debug=True)
