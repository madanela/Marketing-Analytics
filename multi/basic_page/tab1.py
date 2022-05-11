from lib2to3.pgen2.pgen import DFAState
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
from regex import P
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
import plotly.figure_factory as ff




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
    dbc.DropdownMenuItem("boot_means_diff",id = "boot_mean"),
    dbc.DropdownMenuItem("Density of Treatment effect 7 days",id = "dens_treat_effect_day7"),
    dbc.DropdownMenuItem("Density of Treatment effect 1 day",id = 'dens_treat_effect_day1'),
    dbc.DropdownMenuItem("Conversation Rate 1 day",id = 'conv_rate_day1'),
        dbc.DropdownMenuItem("Conversation Rate 7 days",id = 'conv_rate_day7'),


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
            Input('boot_mean',"n_clicks"),
            Input('dens_treat_effect_day1','n_clicks'),
            Input('dens_treat_effect_day7','n_clicks'),
            Input('conv_rate_day1','n_clicks'),
            Input('conv_rate_day7','n_clicks')


            ],
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
    elif button_id == 'dens_treat_effect_day7':
        boot_7d = []

        for i in range(100):
            boot_mean = data.sample(frac=1,replace=True).groupby('version')['day_7_active'].mean() 
            boot_7d.append(boot_mean)
        boot_7d = pd.DataFrame(boot_7d)
        lst = []
        for each in boot_7d.columns:
            if each!='control':
                lst.append((boot_7d[each] - boot_7d['control'])/boot_7d['control'] *100)
        fig = ff.create_distplot(lst, group_labels = boot_7d.columns[1:],show_hist=False)
        fig.update_layout(title_text = "Density of 7 days active By treatment Groups")
        return fig
    elif button_id == 'dens_treat_effect_day1':
        boot_1d = []

        for i in range(100):
            boot_mean = data.sample(frac=1,replace=True).groupby('version')['day_1_active'].mean() 
            boot_1d.append(boot_mean)
        boot_1d = pd.DataFrame(boot_1d)
        lst = []
        for each in boot_1d.columns:
            if each!='control':
                lst.append((boot_1d[each] - boot_1d['control'])/boot_1d['control'] *100)
        fig = ff.create_distplot(lst, group_labels = boot_1d.columns[1:],show_hist=False)
        fig.update_layout(title_text = "Density of 1 day active By treatment Groups")
        return fig
    elif button_id == 'conv_rate_day1':
        fig = px.bar(x=data['version'],
             y=data['day_1_active'],
             color = data['version'],
             labels = {"version": "Group",
                       "day_1_active":"active"})
        fig.update_layout(title_text = "Conversion Rate 1 day")
        return fig
    elif button_id == 'conv_rate_day7':
        fig = px.bar(x=data['version'],
             y=data['day_7_active'],
             color = data['version'],
             labels = {"version": "Group",
                       "day_7_active":"active"})
        fig.update_layout(title_text = "Conversion Rate 7 days")
        return fig    
    
    else:
        data['minutes_play_integers'] = round(data['minutes_play'])
        fig = px.bar(data, x='minutes_play_integers', y='user_id',title = "minutes play", height = 400)
        
        return fig
    return px.bar()
