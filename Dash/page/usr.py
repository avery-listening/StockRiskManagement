
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_table
import plotly.graph_objects as go


from app import app

from datetime import date
from random import random
import pandas as pd
import os 
import yfinance as yf

DATA_DIR="/Users/baobao/Dropbox/CMC_Lab/FYP/Dash/Data/"
NEWS_FILE = os.path.join(DATA_DIR,"today_news.csv")
FEATURE_FILE = os.path.join(DATA_DIR,"price_feature_AAPL_rt.csv")
RISK_FILE = os.path.join(DATA_DIR, "risk_history.csv")

Current_Date = "2021-04-17"

news = pd.read_csv(NEWS_FILE)
feat_a = pd.read_csv(os.path.join(DATA_DIR,"AAPL_10y.csv"))
feat_g = pd.read_csv(os.path.join(DATA_DIR,"GOOG_10y.csv"))
feat_t = pd.read_csv(os.path.join(DATA_DIR,"TSLA_10y.csv"))
mrisk = random()
mref = random()*0.5

table_header = [
    html.Thead(html.Tr([html.Th("Top Market News"),html.Th("URL")]), className="table-primary")
]
rows=[]
for line in news.values:
	rows.append(html.Tr([html.Td(line[0]), html.Td(html.A(line[1],href=line[1]))]))
table_body = [html.Tbody(rows)]

nav_bar = dbc.Row([
				dbc.Col([
					html.H3("Today: " + Current_Date)
					], width=4, style={'color':'white'}),

                dbc.Col([dcc.Dropdown(id="chose_stock",
		            options=[
		                {"label": "AAPL", "value": "AAPL"},
		                {"label": "TSLA", "value": "TSLA"},
		                {"label": "GOOG", "value": "GOOG"},],
		            placeholder="Select a stock")],width=2),

                dbc.Col(html.Img(height="50px", id='logo'),width=0.5),
                dbc.Col(html.H3(className="ml-2", id='stock_title', style={"color":"white"})),

	        ], className="navbar navbar-expand-lg navbar-dark bg-primary") 

stock_cont = dbc.Row([
        	dbc.Col([
        		dbc.Tabs(id='interval', active_tab='M', className="nav nav-tabs",
					children=[
			        dbc.Tab(label='Week', tab_id='W'),
			        dbc.Tab(label='Month', tab_id='M'),
			        dbc.Tab(label='6 Month', tab_id='6M'),
			        dbc.Tab(label='Year', tab_id='Y'),
			        dbc.Tab(label='10 Year', tab_id='10Y'),
			    ]),

	            dcc.Graph(id='stock_graph', figure={}),

        		], width=8),

        	dbc.Col([
        		dbc.Card(
        			dbc.CardBody([
        				dbc.Row([
			            	dbc.Col([dcc.Graph(id='next-day_risk', figure={}, config={'displayModeBar':False})], 
			            		width=6, style={"margin": (10,10,10,10)}),
				        	dbc.Col([dcc.Graph(id='10-day_risk', figure={}, config={'displayModeBar':False})], 
				        		width=6, style={"margin": (10,10,10,10)}),
				        ]),
				  		dbc.Row([
				        	dbc.Col([dcc.Graph(id='market_risk', figure={}, config={'displayModeBar':False})], 
				        		width={"size": 6, "offset": 3}, style={"margin": (10,10,10,10)})
		                ]),
        				],
                		className="card border-primary")
        			)
        		], width=4)
 
            ])

layout = html.Div([
	nav_bar,

    html.Div([
    	html.Div(stock_cont,className = "Container", id = "stock_container"),

        html.Div([
        		dbc.Table(table_header + table_body, 
				bordered=True,
				)
            ])

        ],className="Content")
])


def get_info(ticker):
    if ticker == "AAPL":
    	return 'Apple Inc.', "https://logo.clearbit.com/apple.com"
    elif ticker == "GOOG":
    	return 'Alphabet Inc.', 'https://logo.clearbit.com/abc.xyz'
    else:
    	return 'Tesla, Inc.', 'https://logo.clearbit.com/tesla.com'

def get_feat(ticker,interval):
	if ticker == "AAPL":
		feat_10 = feat_a
	elif ticker == "GOOG":
		feat_10 = feat_g
	else:
		feat_10 = feat_t

	if interval == "W":
		feat_data = feat_10[feat_10['Date'] > '2021-04-08']
	elif interval == "M":
		feat_data = feat_10[feat_10['Date'] > '2021-03-15']
	elif interval == "6M":
		feat_data = feat_10[feat_10['Date'] > '2020-10-15']
	elif interval == "Y":
		feat_data = feat_10[feat_10['Date'] > '2020-04-15']
	elif interval == "10Y":
		feat_data = feat_10
	return feat_data


def build_price_graph(feat_data):
	fig = go.Figure(data=[go.Candlestick(x=feat_data['Date'],
                open=feat_data['Open'], high=feat_data['High'],
                low=feat_data['Low'], close=feat_data['Close'])
                      ])
	fig.update_layout(
            title={
                'text': "Historical Plot",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            yaxis_title="Price",
            margin_r=20,
            xaxis_rangeslider_visible=False
    )
	return fig


def build_risk_graph():
    d1_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = random(),
	    delta = {'reference': random()*0.5},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "1-Day Stock Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    d1_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    d10_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = random(),
	    delta = {'reference': random()*0.5},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "10-Day Stock Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    d10_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    market_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = mrisk,
	    delta = {'reference': mref},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "Market Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    market_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    return d1_risk, d10_risk, market_risk


@app.callback(
	[Output("stock_container", "style")],
	[Input("chose_stock", "value")])

def update_data(name):
	if name == None:
		return  [{'display':'none'}]
	else:
		return  [{'display':'block'}]

@app.callback(
    [Output("stock_title", "children"), Output("logo", "src"), Output("stock_graph", "figure"),Output("next-day_risk", "figure"), Output("10-day_risk", "figure"), Output("market_risk", "figure")],
    [Input("chose_stock", "value"),Input("interval", "active_tab" )]
	)

def update_data(v,interval):
    if v == None:
        raise PreventUpdate

    a_name, a_url = get_info(v)
    feat_data = get_feat(v,interval)
    fig1, fig2, fig3 = build_risk_graph()
    feature_fig = build_price_graph(feat_data)
    return [a_name,a_url,feature_fig,fig1, fig2, fig3]
