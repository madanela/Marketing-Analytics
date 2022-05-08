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
                                                              id = 'group_number'),
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
                                                              id = 'datapoint_number'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                        # Block 4
                                         dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Number of Features"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'feature_number'),
                                                ],
                                                className="mb-3",
                                            )
                                        ]),
                                          dbc.Col([
                                            dbc.InputGroup(
                                                [
                                                    dbc.InputGroupText("Number of Features"),
                                                    dbc.Input(placeholder="Enter", 
                                                              type="number",
                                                              id = 'feature_number'),
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
             dbc.Row( # Select which option to use parameters
                [   
                    dbc.Card(
                        [
                            dbc.CardHeader("Select The Tool"),
                            
                            dbc.CardBody(
                                dbc.Row([
                                    # Visualisation
                                    dbc.Col([
                                        dbc.Label("Choose Which option to use"),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Option 1", "value": 1},
                                                {"label": "Option 2", "value": 2},
                                            ],
                                            value=1,
                                            id="radioitems-inline-input",
                                            inline=True,
                                        ),
                                    ]),
                                    # Statistics
                                    dbc.Col([
                                        dbc.Label("Choose Which option to use"),
                                        dbc.RadioItems(
                                            options=[
                                                {"label": "Option 1", "value": 1},
                                                {"label": "Option 2", "value": 2},
                                            ],
                                            value=1,
                                            id="radioitems-inline-input",
                                            inline=True,
                                        ),
                                    ]),
                                ])
                            ),
                        ],
                    ),
                    html.Br(),
                ],
                class_name="pd-2",
            ),
            dbc.Row( # Visualisation  
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Visualisation", tab_id="vis"),
                            dbc.Tab(label="Statistics", tab_id="stat"),
                            dbc.Tab(label="Cross_Table", tab_id="crosstable"),

                        ],
                        id="tabs",
                        active_tab="scatter",
                    ),
                ],
                class_name="pd-2",
            ),
        ],
        class_name="mx-5 mt-5",
    )

from app import app
from random import random

import dash
# Any callbacks for the page should go here
@app.callback(
    dash.dependencies.Output(__package__ + "-chart", "figure"),
    [dash.dependencies.Input(__package__ + "-button", "n_clicks")],
)
def button_click(n_update):
    # Plot some random numbers on a chart
    print("true")
    res = {
        "data": [
            {
                "x": [0 * random() - 1 for x in range(10)],
                "y": [2 * random() - 1 for y in range(10)],
                "mode": "markers",
                "name": "Demo",
            },
        ],
        "layout": {
            "margin": {"l": 0, "r": 0, "t": 0, "b": 0, "pad": 0},
            "xaxis": {"range": [-1, +1]},
            "yaxis": {"range": [-1, +1]},
        },
    }
    print(res)
    return res
