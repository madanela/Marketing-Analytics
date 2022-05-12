from lib2to3.pgen2.pgen import DFAState
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
from regex import P
import utils
import pandas as pd
import dash
import dash_table
import numpy as np
from statsmodels.stats.power import TTestIndPower
import chart_studio.plotly as py
from dash.dependencies import Input, Output, State
from app import app
import plotly
import plotly.tools as tls
import plotly.figure_factory as ff
import plotly.graph_objs as go

var = pd.DataFrame()
def layout3(data):

    global var
    if not data.empty:
       var = data.copy()
    items = [
    dbc.DropdownMenuItem("Gain",id = "gain_tab3"),
    dbc.DropdownMenuItem("Day 1 active",id = "day_1_active_tab3"),
    dbc.DropdownMenuItem("Day 7 active",id = "day_7_active_tab3"),
    dbc.DropdownMenuItem("Cost",id = "cost_tab3"),

    ]
    df = data.copy()

    # a = np.unique(df.to_numpy())
    # df = pd.crosstab(df['cost'], df['version']).reindex(columns=a, index=a, fill_value=0)#.reset_index()

    # iname = df.index.name
    # cname = df.columns.name
    # df = df.reset_index()
    
    # df.rename(columns={df.columns[0]: iname + ' / ' + cname}, inplace=True)

    return  dbc.Row([
                    html.Div([
                        dbc.Row(id = 'hidden-div_tab3',style = {'display':'none'}),
                        dbc.Col([
                            dbc.Label("Choose column for cross table"),
                            dbc.Row([
                                dbc.Col([
                                    dbc.DropdownMenu(items,
                                                        label = 'Menu',
                                                        color = 'black',
                                                        className = 'm-1'),
                                ],
                                style = {'width' : '70%', 'margin-top' : '10px', 'margin-bottom' : '10px'}),
                            ]),

                            dbc.Col([
                                dcc.Graph(
                                        id='cross_table',

                                    )

                            ]),

                        ]),
                    ])
         ])
@app.callback(
    Output(component_id='cross_table', component_property='figure'),
    [Input('gain_tab3','n_clicks'),
     Input('day_1_active_tab3','n_clicks'),
     Input('day_7_active_tab3','n_clicks'),
     Input('cost_tab3','n_clicks'),
     ]
)
def display_table(*args):
    
    global var
    if var.empty:
        return px.bar()
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = "all"
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    data = var.copy()
   # if button_id == 'cross'
    if button_id == 'gain_tab3':
        target = 'gain'
    elif button_id == 'day_1_active_tab3':
        target = 'day_1_active'
    elif button_id == 'day_7_active_tab3':
        target = 'day_7_active'
    elif button_id == 'cost_tab3':
        target = 'cost'
    d1 = pd.crosstab(data['version'],data[target])
    d1.to_csv("a.csv")
    d1 = pd.read_csv("a.csv")
    columns = [{'name': col, 'id': col} for col in d1.columns.names]

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(d1.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=d1.transpose().values.tolist(),
                fill_color='lavender',
                align='left'))
    ])
    return fig