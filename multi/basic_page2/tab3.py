import dash_bootstrap_components as dbc
from dash import dcc, html

import utils


layout3 = dbc.Row(
        [
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
        ],
        class_name="mx-5 mt-5",
    )
