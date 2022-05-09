from lib2to3.pgen2.pgen import DFAState
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import utils
import pandas as pd

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
    return  dbc.Row([
                     dbc.Row(id = 'hidden-div2',style = {'display':'none'}),

                    #  dbc.Col([
                    #         dbc.InputGroup(
                    #             [
                    #                 dbc.InputGroupText("Select first column"),
                    #                 dbc.Input(placeholder="Enter", 
                    #                             type="number",
                    #                             id = 'first_col'),
                    #             ],
                    #             className="mb-3",
                    #         )
                    #     ]),
                    #     # Block 4
                    #         dbc.Col([
                    #         dbc.InputGroup(
                    #             [
                    #                 dbc.InputGroupText("Select second column"),
                    #                 dbc.Input(placeholder="Enter", 
                    #                             type="number",
                    #                             id = 'second_col'),
                    #             ],
                    #             className="mb-3",
                    #         )
                    #     ]),
                    html.Div([
                        html.H3('Tab content 2'),
                        dcc.Graph(
                            id='graph-1-tabs-dcc',

                        )
                    ])
                ]),
from dash.dependencies import Input, Output, State
from app import app

@app.callback(Output('graph-1-tabs-dcc','figure'),
			[Input('hidden-div2','value')],
			)

def update_graph_gg(value):
    print("lol")
    global var
    if var.empty:
        return px.bar()
    print("bhh")
    print(var)
    data = var.copy()
    print(type(data))
    print(data.dtypes)
    data['minutes_play_integers'] = round(data['minutes_play'])
    print(data.shape)
    fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
    return fig