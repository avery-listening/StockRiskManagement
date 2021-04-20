
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from app import app

from datetime import date
import pandas as pd
import os 
import yfinance as yf

DATA_DIR="/Users/baobao/Dropbox/CMC_Lab/FYP/Dash/Data/"
NEWS_FILE = os.path.join(DATA_DIR,"TopNews.csv")
FEATURE_FILE = os.path.join(DATA_DIR,"price_feature_AAPL.csv")
current_date = "2016-06-01"

# Load experimental data
news = pd.read_csv(NEWS_FILE)
feat_a = pd.read_csv(os.path.join(DATA_DIR,"price_feature_AAPL.csv"))[-710:-10]
feat_g = pd.read_csv(os.path.join(DATA_DIR,"price_feature_GOOG.csv"))[-710:-10]
feat_t = pd.read_csv(os.path.join(DATA_DIR,"price_feature_TSLA.csv"))[-710:-10]

risk_a = pd.read_csv(os.path.join(DATA_DIR, "risk_history_AAPL.csv"))[-700:]
risk_g = pd.read_csv(os.path.join(DATA_DIR, "risk_history_GOOG.csv"))[-700:]
risk_t = pd.read_csv(os.path.join(DATA_DIR, "risk_history_TSLA.csv"))[-700:]

risk_m = pd.read_csv(os.path.join(DATA_DIR, "market_risk.csv"))[-700:]

feature = [x for x in feat_a.columns if x not in ['Date','true_close','normVol']]

feat_options = []
for f in feature:
	feat_options.append({'label': f, 'value':f})

table_header = [
    html.Thead(html.Tr([html.Th("Top Market News")]),className="table-dark")
]
rows=[]
for line in news.loc[news['Date'] == current_date]['News'].values:
	rows.append(html.Tr([html.Td(line)]))
table_body = [html.Tbody(rows, className="table-secondary")]

nav_bar = dbc.Row([
				dbc.Col([
					dcc.DatePickerRange(
                    id='date-picker',
                    min_date_allowed=date(2008, 8, 8),
                    max_date_allowed=date(2016, 7, 1),
                    initial_visible_month=date(2016, 6, 1),
                    start_date=date(2015, 1, 1),
                    end_date=date(2016, 6, 1),
                    display_format='MMMM Y, DD'),
					], width=4),

                dbc.Col([dcc.Dropdown(id="slct_stock",
		            options=[
		                {"label": "AAPL", "value": "AAPL"},
		                {"label": "GOOG", "value": "GOOG"},
		                {"label": "TSLA", "value": "TSLA"}],
		            placeholder="Select a stock"
		            )],width=2),

                dbc.Col(html.Img(height="80px", id='logo_dev'),width=0.5),
                dbc.Col(html.H3(className="ml-2", id='stock_title_dev',style={"color":"white"})),

	        ], className="navbar navbar-expand-lg navbar-dark bg-dark")
			
dev_cont = [
        dbc.Row([dbc.Col([

	            dcc.Graph(id='feature_graph', figure={}),
	            dcc.Dropdown(
	                id = 'feat_list',
	                options=feat_options,
	                value=['Close'],
	                multi=True,
	            ) ,

        		], width=8),

        	dbc.Col([
        		dbc.Card(
        			dbc.CardBody([
        				dbc.Row([
			            	dbc.Col([dcc.Graph(id='risk_1', figure={}, config={'displayModeBar':False})], 
			            		width=6, style={"margin": (10,10,10,10)}),
				        	dbc.Col([dcc.Graph(id='risk_10', figure={}, config={'displayModeBar':False})], 
				        		width=6, style={"margin": (10,10,10,10)}),
				        ]),
				  		dbc.Row([
				        	dbc.Col([dcc.Graph(id='risk_m', figure={}, config={'displayModeBar':False})], 
				        		width={"size": 6, "offset": 3})
		                ]),
        				],
                		className="card border-danger")
        			),

        		dcc.Checklist(
				    options=[
				        {'label': '1-day risk', 'value': '1_day_risk'},
				        {'label': '10-day risk', 'value': '10_day_risk'},
				        {'label': 'market risk', 'value': 'market_risk'},
				    ],
				    value=[],
				    id = "risk_plot",
				    labelClassName="mr-5"
				) ,
        		], width=4)]),

        html.Div([
			dbc.Table(table_header + table_body, 
				bordered=True,
				)
            ], id="market_news")
        ]

layout = html.Div([
	nav_bar,

    html.Div(dev_cont, className="Content", id="dev_container")
])

def build_price_graph(feat_data, risk_data, risk_data2, feat_list,risk_plot):
	fig = make_subplots(specs=[[{"secondary_y": True}]])
	for f in feat_list:
		new_fig = go.Scatter(x=feat_data['Date'],y=feat_data[f],name=f)
		fig.add_trace(new_fig,secondary_y=False)

	for risk in risk_plot:
		if risk == "market_risk":
			risk_fig = go.Scatter(x=risk_data2['Date'],y=risk_data2[risk],name=risk)
		else:
			risk_fig = go.Scatter(x=risk_data['Date'],y=risk_data[risk],name=risk)
		fig.add_trace(risk_fig,secondary_y=True)

	fig.update_layout(
            title={
                'text': "Historical Plot",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            margin_r=20,
            showlegend=True,
    )
	return fig


def get_info(ticker):
    if ticker == "AAPL":
    	return 'Apple Inc.', "https://logo.clearbit.com/apple.com"
    elif ticker == "GOOG":
    	return 'Alphabet Inc.', 'https://logo.clearbit.com/abc.xyz'
    else:
    	return 'Tesla, Inc.', 'https://logo.clearbit.com/tesla.com'

def build_risk_graph(risk_data, risk_data2, end, pre):
    d1_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = risk_data.loc[risk_data['Date'] == end]['1_day_risk'].values[0],
	    delta = {'reference': risk_data.loc[risk_data['Date'] == pre]['1_day_risk'].values[0]},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "1-Day Stock Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    d1_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    d10_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = risk_data.loc[risk_data['Date'] == end]['10_day_risk'].values[0],
	    delta = {'reference': risk_data.loc[risk_data['Date'] == pre]['10_day_risk'].values[0]},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "10-Day Stock Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    d10_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    market_risk = go.Figure(go.Indicator(
    	mode = 'number+gauge+delta',
	    value = risk_data2.loc[risk_data2['Date'] == end]['market_risk'].values[0],
	    delta = {'reference': risk_data2.loc[risk_data2['Date'] == pre]['market_risk'].values[0]},
	    gauge = {
	    	'bar': {'color': 'red'},
	    	'axis': {'visible': False, 'range': (0,1)}},
	    title = {'text': "Market Risk", 'font_size': 20},
	    domain = {'x': [0, 1], 'y': [0, 1]}))
    market_risk.update_layout(height=200, margin={'l': 30, 'r': 30, 't': 0, 'b': 0})

    return d1_risk, d10_risk, market_risk



@app.callback(
	[Output("dev_container", "style")],
	[Input("slct_stock", "value")])

def update_data(name):
	if name == None:
		return  [{'display':'none'}]
	else:
		return  [{'display':'block'}]


@app.callback(
    [Output("stock_title_dev", "children"), Output("logo_dev", "src"), Output("feature_graph", "figure"),Output("risk_1", "figure"), Output("risk_10", "figure"), Output("risk_m", "figure")],
    [Input("slct_stock", "value"), Input("feat_list","value"), Input("risk_plot","value"),Input("date-picker","start_date"),Input("date-picker","end_date")]
	)

def update_data(name,feat_list,risk_plot,start,end):
    if name == None:
        raise PreventUpdate

    if name == "AAPL":
    	feat_data = feat_a[(feat_a['Date'] >= start) & (feat_a['Date'] <= end)]
    	risk_data = risk_a[(risk_a['Date'] >= start) & (risk_a['Date'] <= end)]

    elif name == "GOOG":
    	feat_data = feat_g[(feat_g['Date'] >= start) & (feat_g['Date'] <= end)]
    	risk_data = risk_g[(risk_g['Date'] >= start) & (risk_g['Date'] <= end)]

    else:
    	feat_data = feat_t[(feat_t['Date'] >= start) & (feat_t['Date'] <= end)]
    	risk_data = risk_t[(risk_t['Date'] >= start) & (risk_t['Date'] <= end)]

    risk_data2 = risk_m[(risk_m['Date'] >= start) & (risk_m['Date'] <= end)]

    end = feat_data['Date'].values[-1]
    pre = feat_data['Date'].values[-2]
    a_name, a_url = get_info(name)
    fig1, fig2, fig3 = build_risk_graph(risk_data, risk_data2, end, pre)
    feature_fig = build_price_graph(feat_data, risk_data, risk_data2, feat_list, risk_plot)
    return [a_name,a_url,feature_fig,fig1, fig2, fig3]


