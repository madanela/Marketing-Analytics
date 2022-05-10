from lib2to3.pgen2.pgen import DFAState
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import utils
import pandas as pd
import dash
import numpy as np
from statsmodels.stats.power import TTestIndPower
import chart_studio.plotly as py
from dash.dependencies import Input, Output, State
from app import app
import plotly
import plotly.tools as tls



def minutes_play(data):
  data['minutes_play_integers'] = round(data['minutes_play'])
  fig = px.bar(data, x='minutes_play_integers', y='user_id')
  return fig
var = pd.DataFrame()
#minutes_play(var.df)

def layout1(data):
    global var
    if not data.empty:
       print("oops")
       var = data.copy()
    items = [
    dbc.DropdownMenuItem("minutes_play_integers",id = "minutes_play_integers"),
    dbc.DropdownMenuItem("T-Test",id = "t-test"),
    dbc.DropdownMenuItem("Item 3"),
    ]
    return  dbc.Row([
                     dbc.Row(id = 'hidden-div2',style = {'display':'none'}),

                        dbc.Row([
                            dbc.Col([
                                dbc.DropdownMenu(items,
                                                    label = 'Menu',
                                                    color = 'black',
                                                    className = 'm-1'),
                                #  style={"display": "flex", "flexWrap": "wrap"},
                            ]),
                    ]),
                    
                            # Block 4
                            
                        dbc.Col([
                            html.Div([
                                html.H3('Tab content 2'),
                                dcc.Graph(
                                    id='graph-1-tabs-dcc',

                                )
                            ])
                        ]),

                ])

@app.callback(Output('graph-1-tabs-dcc','figure'),
			[Input('minutes_play_integers','n_clicks'),
            Input('t-test','n_clicks')],
			)

def update_graph_gg(*args):
    print("lol")
    global var
    if var.empty:
        return px.bar()
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "all"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    print(button_id)
    if button_id == 'minutes_play_integers':
        
        data = var.copy()
        data['minutes_play_integers'] = round(data['minutes_play'])
        fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
        return fig
    elif button_id == 't-test':
        
        fig =  TTestIndPower().plot_power(dep_var='nobs',
        nobs=np.array(range(5, 1000)),
        effect_size=np.array([0.07, 0.3, 0.5]),
        title='T - test results')
        return tls.mpl_to_plotly(fig)
    else:
        data = var.copy()
        data['minutes_play_integers'] = round(data['minutes_play'])
        fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
        return fig
    return px.bar()