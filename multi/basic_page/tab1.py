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
    dbc.DropdownMenuItem("Distribution of users", id = "dist_user"),
    dbc.DropdownMenuItem("boot_means_diff",id = "boot_mean")
    ]
    return  dbc.Row([
                    html.Div([
                        dbc.Row(id = 'hidden-div2',style = {'display':'none'}),
                        dbc.Col([
                            dbc.Label("Choose Visualisation from menu"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.DropdownMenu(items,
                                                        label = 'Menu',
                                                        color = 'black',
                                                        className = 'm-1'),
                                ],
                                style = {'width' : '70%', 'margin-top' : '10px', 'margin-bottom' : '10px'}),
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

                        ]),
                    ])
    ])

@app.callback(Output('graph-1-tabs-dcc','figure'),
			[Input('minutes_play_integers','n_clicks'),
            Input('t-test','n_clicks'),
            Input('dist_user','n_clicks'),
            Input('boot_mean',"n_clicks")],
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
    
    data = var.copy()
    if button_id == 'minutes_play_integers':
        
        data['minutes_play_integers'] = round(data['minutes_play'])
        fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
        return fig
    elif button_id == 't-test':
        
        fig =  TTestIndPower().plot_power(dep_var='nobs',
        nobs=np.array(range(5, 1000)),
        effect_size=np.array([0.07, 0.3, 0.5]),
        title='T - test results')
        return tls.mpl_to_plotly(fig)
    elif button_id == 'dist_user':

        data['minutes_play_integers'] = round(data['minutes_play'])
        plot_df = data.groupby('minutes_play_integers')['user_id'].count()
        ax = plot_df.head(n=50).plot(x="minutes_play_integer", y="user_id", kind="hist")
        return px.histogram(data, x ='minutes_play_integers',nbins = 20,histnorm= 'probability density',title="Users distribution by minutes_play" )
    elif button_id == 'boot_mean':
        
        boot_means = data.groupby('version')['minutes_play'].mean()
        boot_means = pd.DataFrame(boot_means)
        return px.line(boot_means)
    else:
        data['minutes_play_integers'] = round(data['minutes_play'])
        fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
        return fig
    return px.bar()
