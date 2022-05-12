import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_table
import utils
import numpy as np
import pandas as pd
layoutt3 = dbc.Row(
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
def layout3(data):
    print("open")
    global var
    if not data.empty:
       var = data.copy()
    items = [
    dbc.DropdownMenuItem("CrossTable",id = "cross_table"),
    ]
    df = data.copy()
    print(df.to_numpy())
    a = np.unique(df.to_numpy())
    df = pd.crosstab(df['cost'], df['version']).reindex(columns=a, index=a, fill_value=0)#.reset_index()

    iname = df.index.name
    cname = df.columns.name
    df = df.reset_index()
    
    df.rename(columns={df.columns[0]: iname + ' / ' + cname}, inplace=True)
    print(df)
    return  dbc.Row([
                    html.Div([
                        dbc.Row(id = 'hidden-div_tab3',style = {'display':'none'}),
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
                               dash_table.DataTable(
                                    id='table',
                                    columns=[{"name": i, "id": i} for i in df.columns],
                                    df=df.to_dict('records'),
                                )
                            ]),

                        ]),
                    ])
         ])