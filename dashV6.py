# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 14:27:00 2018

@author: YEOHANBOON
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_auth
#import datetime
#import glob
#import time
#import seaborn as sns
import matplotlib.pyplot as plt
#import numpy as np
#import random
#from matplotlib import colors as mcolors
from AFC_func import get_filenames, getLog
from RBG_code import get_color_rgb
#from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout, Figure
#from plotly import tools
from random import randint as ri

VALID_USERNAME_PASSWORD_PAIRS = [
    ['username', 'password'], 
    ['username2', 'password'], 
    ['username3', 'password'],
    ['username4', 'password'],
    ['username5', 'password'],
    ['username6', 'password'],
    ['username7', 'password'],
    ['username8', 'password'],
    ['username9', 'password'],

]


app = dash.Dash()
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)


log_df = pd.read_csv('Sample.csv')
tailgate_df = pd.read_csv('Tailgate.csv')
tailgate_df['Datetime'] = pd.to_datetime(tailgate_df['Datetime'])
tailgate_df.set_index('Datetime', inplace=True)

stn_list = list(log_df['Station'].unique())
dates_list = list(log_df['Date'].unique())
date_list_tailgate = list(tailgate_df['Date'].unique())
plots_type = ['bar', 'scatter']
parameters_list = ['Barrier_Hit', 'HCSS_Error', 'HCSS_Uncleared', 'Intrusion', 'Passage_Cancel', 'Tailgate']
bins_list = ['5 Mins', '15 Mins', '30 Mins', '1 Hour']
bins_dict = {'5 Mins': '5T', '15 Mins':'15T', '30 Mins':'30T', '1 Hour':'1H'}
stns_num = [3, 5, 10, 15 ]

colors_cmap = []
for i in range(9):    
#    rgb=plt.cm.Paired(i%12/12)
    rgb=plt.cm.Pastel1(i%9/9)
#    rgb=plt.cm.Pastel2(i%8/8)
#    rgb=plt.cm.tab20(i%20/20)
#    rgb=plt.cm.Set1(i%9/9)    
#    rgb=plt.cm.Set3(i%12/12)
#    rgb=plt.cm.rainbow(i)
    rgb_tuple = (rgb[0], rgb[1], rgb[2])
    rgb_convert = tuple(int(x*255) for x in rgb_tuple)
    rgb_string = 'rgb' + str(rgb_convert)
    colors_cmap.append(rgb_string)

colors_dict, colors_list = get_color_rgb()
groupby_df1 = log_df.groupby('Date').sum()
groupby_df2 = log_df.groupby(['Date','Station']).sum()
groupby_df3 = log_df.groupby(['Date','Station','Gates']).sum()   

app.layout = html.Div([
        
        html.H1(
            'DASHBOARD',
            style={'background-color': 'black', 'margin': '0', 'border': '15px solid black',
                    'color': 'gold', 'font-weight': 'bold','font-size': '60px','textAlign':'center'}
            ),
        
        html.H2(
            'Fare Gates Fault Trending',
            style={'background-color': 'black','margin': '0px', 'border': '15px solid black',
                   'color': 'gold', 'font-weight': 'bold','font-size': '50px','textAlign':'center'}
            ),
        
        dcc.Tabs(id="tabs", value='tab1', children=[
            dcc.Tab(label='Overview', value='tab1'),
            dcc.Tab(label='Tailgate Insights', value='tab2'),
            
        ], 
        
        style={'background': 'black', 'color': 'steelblue', 'font-weight': 'bold','font-size': '30px', 'textAlign':'center'}, 
        colors={'background': 'lavender', 'primary': 'gold'},
        
        ),
    
        html.Div(id='tabs-content')
        
    ], className="twelve columns", #style={'width': '95%'}
    )

app.config.supress_callback_exceptions = True
    
@app.callback(dash.dependencies.Output('tabs-content', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab1':
        return html.Div([

                html.Div([
                    
                    html.Div([
                        
                        html.Label(
                            'Select Dates:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='dates_drpdwn1',
                            options=[{'label': p, 'value': p} for p in dates_list],
                            value=dates_list,
                            multi=True,
                        ),                    
                 
                    ], className= "four columns", style={'margin-left': '8.7%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
    
                    html.Div([
                            
                        dcc.Graph(id='piechart-overview'),
                        
                    ], className= "twelve columns"
                    ),                
                    
                    html.Div([
    
                        html.Label(
                            'Select Plot Type:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                            
                        dcc.RadioItems(
                            id= 'plot_radioitem1',
                            options=[
                                {'label': '<Bar>', 'value': 'bar'},
                                {'label': '<Line>', 'value': 'scatter'}
                                ],
                            value='bar',
                            labelStyle={'display':'inline-block', 'font-size': '20px'},
          
                        ),                                 
        
                        html.Label(
                            'Select Parameters:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id = 'parameter_drpdwn',
                            options=[{'label': p, 'value': p} for p in parameters_list],
                            value='Tailgate',
                            multi=False
                        ),
                    ], className= "four columns", style={'margin-left': '8.7%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    html.Div([
                            
                        html.Label(
                            'Select Dates:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='dates_drpdwn2',
                            options=[{'label': p, 'value': p} for p in dates_list],
                            value=dates_list,
                            multi=True,
                        ),
                                
#                        html.Label(
#                            'Select Station:',
#                            style={'font-size': '20px', 'font-weight':'bold', 'font-style': 'oblique','textAlign':'left'}
#                        ),
#                        
#                        dcc.Dropdown(
#                            id='station_drpdwn',
#                            options=[{'label': p, 'value': p} for p in stn_list],
#                            value=stn_list,
#                            multi=False,
#                        ), 
                    
                    ], className= "four columns", style={'margin-left': '12.5%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'} 
                    ),
                
                    
                    html.Div([
                            
                        dcc.Graph(id='barchart-allStations'),
                        
                    ], className= "twelve columns"#style={'width': '100%', 'float': 'center','margin-top':700}   
                    ),
                
                    html.Div([
                        html.Br([]),    
                        html.Label(
                            'Select Plot Type:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.RadioItems(
                            id= 'plot_radioitem2',
                            options=[
                                {'label': '<Bar>', 'value': 'bar'},
                                {'label': '<Line>', 'value': 'scatter'}
                                ],
                            value='bar',
                            labelStyle={'display':'inline-block', 'font-size': '20px'},
          
                        ),                                
        
                        html.Label(
                            'Select Parameters:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id = 'parameter_drpdwn2',
                            options=[{'label': p, 'value': p} for p in parameters_list],
                            value='Tailgate',
                            multi=False
                        ),
                    ], className= "four columns", style={'margin-left': '8.7%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    html.Div([
                        html.Br([]),                            
                        html.Label(
                            'Select Dates:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='dates_drpdwn3',
                            options=[{'label': p, 'value': p} for p in dates_list],
                            value=dates_list,
                            multi=True,
                        ),
                                
                        html.Label(
                            'Select Station:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='station_drpdwn2',
                            options=[{'label': p, 'value': p} for p in stn_list],
                            value='ORC',
                            multi=False,
                        ), 
                    
                    ], className= "four columns", style={'margin-left': '12.5%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'} 
                    ),
                
                    
                html.Div([
                    html.Br([]),   
                     
                    dcc.Graph(id='barchart-selectedStations'),
                    
                ], className= "twelve columns"
                ),
                
             
                ], className="twelve columns"
                )
                
            ]),





    elif tab == 'tab2':
        return html.Div([
                
                
                    html.Div([
    
                        html.Label(
                            'Select Plot Type:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        

                        dcc.RadioItems(
                            id= 'plot_radioitem3',
                            options=[
                                {'label': '<Bar>', 'value': 'bar'},
                                {'label': '<Line>', 'value': 'scatter'}
                                ],
                            value='scatter',
                            labelStyle={'display':'inline-block', 'font-size': '20px'},
          
                        ),

                        html.Label(
                            'Select Dates:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='dates_drpdwn4',
                            options=[{'label': p, 'value': p} for p in date_list_tailgate],
                            value=date_list_tailgate,
                            multi=True,
                        ),



                    ], className= "four columns", style={'margin-left': '8.7%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                        
                    html.Div([                        
                        
                        html.Label(
                            'Select Intervals:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id = 'bins_drpdwn',
                            options=[{'label': p, 'value': p} for p in bins_list],
                            value='30 Mins',
                            multi=False
                        ),
                    ], className= "four columns", style={'margin-left': '12.5%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    html.Div([
                            
                        dcc.Graph(id='tailgate-allStations'),
                        
                    ], className= 'twelve columns'  
                    ),  
                            
                    
                    html.Div([
                        html.Br([]), 
                        
                        html.Label(
                            'Select Plot Type:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.RadioItems(
                            id= 'plot_radioitem4',
                            options=[
                                {'label': '<Bar>', 'value': 'bar'},
                                {'label': '<Line>', 'value': 'scatter'}
                                ],
                            value='bar',
                            labelStyle={'display':'inline-block', 'font-size': '20px'},
          
                        ),
        
                        html.Label(
                            'Select Intervals:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id = 'bins_drpdwn2',
                            options=[{'label': p, 'value': p} for p in bins_list],
                            value='30 Mins',
                            multi=False
                        ),
                                
                              
                    ], className= "four columns", style={'margin-left': '8.7%','font-size': '20px','font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    html.Div([
                        html.Br([]),

                        html.Label(
                            'Select Dates:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Dropdown(
                            id='dates_drpdwn5',
                            options=[{'label': p, 'value': p} for p in date_list_tailgate],
                            value=date_list_tailgate[0],
                            multi=False,
                        ),
                            
                        html.Label(
                            'Select Num of Stations of highest occurences:',
                            style={'font-size': '25px', 'font-weight':'bold'}
                        ),
                        
                        dcc.Slider(
                            id='stations_slider',
                            min=1,
                            max=20,
                            step=1,
                            marks={
                                    1: {'label': '1', 'style':{'font-size': '20px'}},
                                    3: {'label': '3', 'style':{'font-size': '20px'}},
                                    5: {'label': '5', 'style':{'font-size': '20px'}},
                                    10: {'label': '10', 'style':{'font-size': '20px'}},
                                    15: {'label': '15', 'style':{'font-size': '20px'}},
                                    20: {'label': '20', 'style':{'font-size': '20px'}},
                                },
                            value=5,
                            
                        ),


                    
                    ], className= "four columns", style={'margin-left': '12.5%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'} 
                    ),                    
                    
                    
                    html.Div([
                        html.Br([]),
                            
                        dcc.Graph(id='tailgate-nStations'),
                        
                    ], className= 'twelve columns',
                    ),    
                     
                ])                
                    
          
                


                
@app.callback(
dash.dependencies.Output('piechart-overview', 'figure'),
[dash.dependencies.Input('dates_drpdwn1', 'value')])
def update_piechart(dates):

    
    parameters_list = ['Barrier_Hit', 'HCSS_Error', 'HCSS_Uncleared', 'Intrusion', 'Passage_Cancel', 'Tailgate']
    n = len(parameters_list)
    s = 1/n
    b = 0.01
    domain = []
    for i in range(n):
        domain.append((s*i+b, s*(i+1)-b))
    colors = colors_cmap[1:6]
    traces_dict = {}
    for i,name in enumerate(parameters_list):
        traces_dict[name] = {
                'type': 'pie',            
                'values': groupby_df1[name][dates].values,
                'labels': groupby_df1[name][dates].index,
                'domain': {'x': domain[i]},
                'name': name,
                'textfont': {'size': 20, 'color':colors_dict['navy']},
                'sort': False,
                'direction': 'clockwise',
                'textinfo': 'value',
                'hoverlabel': {'font': {'size':20}},
                'hoverinfo':'label+percent',
                'hole': .4,
                'marker': {'colors': colors,
                           'line': {'color': colors_dict['black'], 'width': 1}}
                }            
        
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key]) 
    
    labels = ['Barrier Hit', 'HCSS Error', 'HCSS Uncleared', 'Intrusion', 'Passage Cancel', 'Tailgate']
    x_domain=[0.04, 0.2, 0.42, 0.58, 0.8, 0.95]
    annotations_dict = {}
    for i,name in enumerate(labels):
        annotations_dict[name] = {
                        'font': {'size': 25, 'color':colors_dict['navy']},
                        'showarrow': False,
                        'text': name,
                        'x': x_domain[i],
                        'y': -0.15
                        }
    annotations = []
    for name in labels:
        annotations.append(annotations_dict[name])     

    return {
        
        'data': data,
        'layout': {
            'title':'Overview',
            'titlefont':{'size':25, 'color':colors_dict['navy']},
            'annotations': annotations,
#            'legend': {'x':0.9, 'y':0.95}
            }
        }
          
    
@app.callback(
    dash.dependencies.Output('barchart-allStations', 'figure'),
    [dash.dependencies.Input('plot_radioitem1', 'value'),
     dash.dependencies.Input('parameter_drpdwn', 'value'),
     dash.dependencies.Input('dates_drpdwn2', 'value')])
def update_barchart(plots_type, parameter,dates):
    dates_list = dates
    m = len(colors_list)-len(dates_list)-1
    n = ri(0,m)

    traces_dict = {}
    for i,name in enumerate(dates_list):
        traces_dict[name] = {
                'type':plots_type,
                'x':groupby_df2.loc[dates_list[i]].index,
                'y':groupby_df2.loc[dates_list[i]][parameter],
                'fill':'tonexty',
                'opacity':0.5,
                'hoverinfo':'x+y',
                'hoverlabel': {'font': {'size':20}},
                'name':name,
                'marker': {'color': colors_list[i+n],
                           'line': {'color': colors_dict['navy'], 'width': 1}}
                }            
        
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key]) 
    
    return {
        'data' : data,
         
        'layout': {
                'title': parameter + ' Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                'titlefont':{'size':25, 'color':colors_dict['navy']},
                'barmode':'stack',
                'height':900,
                'paper_bgcolor':colors_dict['white'],
                'plot_bgcolor':colors_dict['whitesmoke'],
#                'dragmode': 'pan',
                'xaxis':{
                        'title':'Stations',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'tickfont':{'size':20},
                        'showgrid':False,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':1
                        },
                'yaxis':{
                        'title':'Counts',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'tickfont':{'size':20},
                        'showgrid':True,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':2
                        }            
                
                }
        }        


@app.callback(
    dash.dependencies.Output('barchart-selectedStations', 'figure'),
    [dash.dependencies.Input('plot_radioitem2', 'value'),
     dash.dependencies.Input('parameter_drpdwn2', 'value'),
     dash.dependencies.Input('dates_drpdwn3', 'value'),
     dash.dependencies.Input('station_drpdwn2', 'value')])
def update_barchart2(plots_type, parameter,dates,station):
    dates_list = dates
    m = len(colors_list)-len(dates_list)-1
    n = ri(0,m)

    traces_dict = {}
    for i,name in enumerate(dates_list):
        traces_dict[name] = {
                'type':plots_type,
                'x':groupby_df3.loc[dates[i],station].index,
                'y':groupby_df3.loc[dates[i],station][parameter],
                'fill':'tonexty',
                'opacity':0.5,
                'hoverinfo':'x+y',
                'hoverlabel': {'font': {'size':20}},
                'name':name,
                'marker': {'color': colors_list[i+n],
                           'line': {'color': colors_dict['navy'], 'width': 1}}
                }            
        
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key]) 
    
    return {
        'data' : data,
         
        'layout': {
                'title': station + ', ' + parameter + ' Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                'titlefont':{'size':25, 'color':colors_dict['navy']},
                'barmode':'stack',
                'height':900,
                'paper_bgcolor':colors_dict['white'],
                'plot_bgcolor':colors_dict['whitesmoke'],
                'xaxis':{
                        'title':'Gates',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'tickfont':{'size':20},
                        'showgrid':False,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':1
                        },
                'yaxis':{
                        'title':'Counts',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'tickfont':{'size':20},
                        'showgrid':True,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':2
                        }            
                
                }
        }          
    



@app.callback(
    dash.dependencies.Output('tailgate-allStations', 'figure'),
    [dash.dependencies.Input('plot_radioitem3', 'value'),
     dash.dependencies.Input('bins_drpdwn', 'value'),
     dash.dependencies.Input('dates_drpdwn4', 'value')])
def tailgate_allStns(plots_type, Bin, dates):
#    date_list_tailgate = list(tailgate_df['Date'].unique())
    date_list_tailgate = dates
    resample_df = tailgate_df.Gate.resample(bins_dict[Bin]).count()
    
    m = len(colors_list) - len(date_list_tailgate) -1
    n = ri(0,m)
    traces_dict = {}
    data = []
    for i,date in enumerate(date_list_tailgate):
        traces_dict[date] = {
                            'type':plots_type,
                            'x':resample_df.loc[str(date_list_tailgate[0])].index,
                            'y':resample_df.loc[str(date_list_tailgate[i])].values,                            
#                            'hoverinfo':'y',
#                            'opacity':0.5,
                            'name':date,
                            'marker': {'color': colors_list[n+i],
                                       'line': {'color': colors_dict['navy'], 'width': 2}}
                        }
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key])   


    return {
        'data' : data,
         
        'layout': {
          
                    'title': 'Tailgate Distribution (All Stations)',
                    'titlefont':{'size':25, 'color':colors_dict['navy']},
                    'barmode':'stack',
                    'height': 600,
                    'paper_bgcolor':colors_dict['white'],
                    'plot_bgcolor':colors_dict['whitesmoke'],
                    'xaxis': {
                            'title':'Time',
                            'titlefont':{'size':20, 'color':colors_dict['navy']},
                            'tickfont':{'size':20},
                            'showgrid':False,
                            'zeroline':False,
                            'showline':True,
                            'gridcolor':colors_dict['white'],
                            'gridwidth':1
                            },
                    'yaxis':{
                            'title':'Counts',
                            'titlefont':{'size':20, 'color':colors_dict['navy']},
                            'tickfont':{'size':20},
                            'showgrid':True,
                            'zeroline':False,
                            'showline':True,
                            'gridcolor':colors_dict['white'],
                            'gridwidth':1
                            }
                    }
                
                }



@app.callback(
    dash.dependencies.Output('tailgate-nStations', 'figure'),
    [dash.dependencies.Input('plot_radioitem4', 'value'),
     dash.dependencies.Input('bins_drpdwn2', 'value'),
     dash.dependencies.Input('stations_slider', 'value'),
     dash.dependencies.Input('dates_drpdwn5', 'value')])
def tailgate_allStns(plots_type, Bin, num, date):
   
    groupby_df = tailgate_df.groupby('Station').count()
    stns_list = list(groupby_df.Gate.nlargest(num).index)
    

    m = len(colors_list)-len(stns_list)-1
    n = ri(0,m)
    traces_dict = {}
    
    for i,stn in enumerate(stns_list):
        resample_df = tailgate_df[tailgate_df.Station == stn].Gate.resample(bins_dict[Bin]).count()
        traces_dict[stn] = {
                            'type':plots_type,
                            'x':resample_df.loc[str(date)].index,
                            'y':resample_df.loc[str(date)].values,
                            'fill':'tonexty',
                            'hoverinfo':'all',
                            'opacity':0.5,
                            'name':stn,
                            'marker': {'color': colors_list[i+n],
                                       'line': {'color': colors_dict['navy'], 'width': 2}}
                            }    
    
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key]) 

    return {
        'data' : data,
         
        'layout': {

                
                    'title': 'Tailgate Distribution (Top ' + str(num) + ' Stations)',
                    'titlefont': {'size':25, 'color':colors_dict['navy']},
                    'barmode':'stack',
                    'height': 900,
                    'paper_bgcolor':colors_dict['white'],
                    'plot_bgcolor':colors_dict['whitesmoke'],
                    'xaxis':{
                            'title':'Time',
                            'titlefont':{'size':20, 'color':colors_dict['navy']},
                            'tickfont':{'size':20},
                            'showgrid':False,
                            'zeroline':False,
                            'showline':True,
                            'gridcolor':colors_dict['white'],
                            'gridwidth':1
                            },
                    'yaxis':{
                            'title':'Counts',
                            'titlefont':{'size':20, 'color':colors_dict['navy']},
                            'tickfont':{'size':20},
                            'showgrid':True,
                            'zeroline':False,
                            'showline':True,
                            'gridcolor':colors_dict['white'],
                            'gridwidth':1
                            }
                    
         
            }
        }

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css",
    "https://rawgit.com/plotly/dash-live-model-training/master/custom_styles.css"
]

#external_css = ['https://codepen.io/plotly/pen/EQZeaW.css']
#external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css"]                    
#external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css"]       
#external_css = ["//fonts.googleapis.com/css?family=Raleway:400,300,600"] 
#external_css = ["https://codepen.io/bcd/pen/KQrXdb.css"]
#external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]                    
#external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})
    
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0')
