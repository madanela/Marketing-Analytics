import dash_bootstrap_components as dbc
from dash import dcc, html

import utils


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
                                        dbc.Button(
                                            "Gerenate",
                                            id=__package__ + "-button",
                                            color="primary",
                                        ),
                                        dbc.InputGroup(
                                            [
                                                dbc.InputGroupText("Number of Groups"),
                                                dbc.Input(placeholder="Enter", type="number"),
                                            ],
                                            className="mb-3",
                                        )
                                    ],
                                )
                            ),
                        ],
                    ),
                    html.Br(),
                ],
                class_name="pd-2",
            ),
            dbc.Row( # Visualisation  parameters
                [
                    dbc.Card(
                        [
                            dbc.CardHeader("Some points on a chart"),
                            dbc.CardBody(
                                [
                                    dcc.Graph(
                                        figure=utils.empty_figure(),
                                        id=__package__ + "-chart",
                                        config={"displayModeBar": False},
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
                class_name="pd-2",
            ),
        ],
        class_name="mx-5 mt-5",
    )
