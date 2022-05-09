import dash_bootstrap_components as dbc
from dash import dcc, html

import utils

from dash import html, dcc, Dash, dash_table
from dash.dependencies import Input, Output, State
from datetime import datetime as dt, timedelta
import plotly.express as px
import pandas_datareader.data as web
# from components.data import options
import pandas as pd

class data_class:
    df = pd.DataFrame()
var = data_class

def layout(params):
    # This function must return a layout for the page
    # Use __package__ as a prefix to each id to make sure they are unique between pages

    # Do something basic as a demo
    return dbc.Col(
        [
            dbc.Row( # Generation parameters
                [   
                    dbc.Card(
                        [
                            dbc.Row(id = 'hidden-div',style = {'display':'none'}),
                            dbc.CardHeader("Select Generation Parameters"),
                            
                            dbc.CardBody(
                                dbc.Row(
                                    [ 
                                        # Block 1, Button Generate
                                        dbc.Col([
                                            dbc.Button(
                                                "Gerenate",
                                                id=__package__ + "-button",
                                                color="primary",
                                            )
                                        ]),
                                        # Block 2 
                                        dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Number of Treatment Groups"),
                                                    dbc.Input(placeholder="Enter",
                                                              type="number",
                                                              id = 'num_of_groups'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                        # Block 3
                                        dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Number of Datapoints"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'num_of_datapoints'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                        # Block 4
                                         dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Minimum cost per group"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'mn_cost'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                          dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Maximum cost per group"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'mx_cost'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                          dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Gain per group"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'gain'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                    ]
                                )
                            ),
                        ],
                    ),
                    html.Br(),
                ],
                class_name="pd-2",
            ),
            dbc.Row( # Tabs  
                html.Div([
                    dcc.Tabs(id = "tabs_inp",value = 'vis',
                        children = [
                            dcc.Tab(label="Visualisation", value="vis"),
                            dcc.Tab(label="Statistics", value="stat"),
                            dcc.Tab(label="Cross_Table", value="crosstable"),

                        ]
                    ),
                    html.Div(id='tabs-content-out')
                ]),
                class_name="pd-2",
            ),
        ],  
        class_name="mx-5 mt-5",
    )
from app import app
from random import random
from basic_page.tab1 import layout1
from basic_page.tab2 import layout2
from basic_page.tab3 import layout3
@app.callback(Output('tabs-content-out', 'children'),
              [Input('tabs_inp', 'value')])
def render_content(tab):
    if tab == 'vis':
        return  layout1(var.df)
    elif tab == 'stat':
       return layout2
    elif tab == 'crosstable':
       return layout3


import dash

from data_gen.Generator import generate_dataset,generte_treatment_results
## generate button_click

@app.callback(
    Output("hidden-div", "figure"),

    [Input(__package__ + "-button", "n_clicks")],
    [
        State('num_of_groups','value'),   
        State('num_of_datapoints','value'),
        State('mn_cost','value'),
        State('mx_cost','value'),
        State('gain','value'),
        
    ]
)
def update_data(n_clicks,num_of_groups,num_of_datapoints,mn_cost,mx_cost,gain):
    global var
    var.df = generate_dataset(num_of_groups,num_of_datapoints,mn_cost,mx_cost,gain)
    print(var.df)
    return None
