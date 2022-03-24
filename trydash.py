from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import yfinance as yf
from finvizfinance.quote import finvizfinance
from finvizfinance.insider import Insider
from finvizfinance.news import News
from finvizfinance.screener.overview import Overview
import ffn

# 列印用
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

app = Dash(__name__)

ticker = 'aapl'

# stock = finvizfinance(ticker)
stock = yf.Ticker(ticker)

# print(stock_des)
# print(stock_sector)
df1 = stock.financials
# df2 = df1.T[['Total Revenue', 'Net Income']].reset_index(drop=True)
df2 = df1.T

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df = pd.DataFrame({
    "Total Revenue": df2[['Total Revenue']].values,
    "Net Income": df2[['Net Income']].values,
    "Date": df2.index.values,
    # "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Date", y=["Total Revenue", "Net Income"], barmode="group")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for your data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
