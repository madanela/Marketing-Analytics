import dash_bootstrap_components as dbc
from dash import dcc, html
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import utils
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

def statistics(data):
    lst = []
    for i in range(len(data['version'].unique())-1):
        control_results = data[data['version'] == 'control']['day_1_active']
        treatment1_results = data[data['version'] == f'treatment_{i+1}']['day_1_active']
        n_con = control_results.count()
        n_treat1 = treatment1_results.count()
        successes = [control_results.sum(), treatment1_results.sum()]
        nobs = [n_con, n_treat1]
        z_stat, pval = proportions_ztest(successes, nobs=nobs)

        lst.append(pval)
    return lst
def statistics_7d(data):
    lst = []
    for i in range(len(data['version'].unique())-1):
        control_results = data[data['version'] == 'control']['day_7_active']
        treatment1_results = data[data['version'] == f'treatment_{i+1}']['day_7_active']
        n_con = control_results.count()
        n_treat1 = treatment1_results.count()
        successes = [control_results.sum(), treatment1_results.sum()]
        nobs = [n_con, n_treat1]
        z_stat, pval = proportions_ztest(successes, nobs=nobs)
        lst.append(pval)
    return lst
dx = pd.DataFrame()
def layout2(data):
    global var
    if not data.empty:
       var = data.copy()

    df = data.copy()
    global dx
    dx = pd.DataFrame(zip(statistics(data),statistics_7d(data)))
    dx.columns = ['day_1_active','day_7_active']
    dx.index = data['version'].unique()[1:]

    
    return  dbc.Row([
                    html.Div([
                        dbc.Row(id = 'hidden-div_tab2',style = {'display':'none'}),
                        dbc.Col([
                            dbc.Label("Choose Statistical tool"),
    
                            dcc.Dropdown(['default', 'conversion_rate'], id='loading-states-table-prop'),

                            dbc.Col([
                                dash_table.DataTable(
                                        id='stat_table_tab2',
                                        columns = [{
                                            'name': i ,
                                            'id' : i,
                                            'deletable': True,
                                             'renamable': True
                                        } for i,j in zip(dx.columns,dx.index)],
                                        
                                        data = [{
                                            i: dx[i][j] for i in dx.columns} 
                                        for j in range(dx.shape[0])],
                                        editable=True
                                    ),
                            ]),

                        ]),
                    ])
         ])
@app.callback(
    Output('stat_table_tab2', 'data'),
    Input('loading-states-table-prop', 'value')
)
def loading_data(value):
    if value == 'conversion_rate':
        return [{
                i: dx[i][j] for i in dx.columns} 
            for j in range(dx.shape[0])]