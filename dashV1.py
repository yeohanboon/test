# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 14:27:00 2018

@author: YEOHANBOON
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import glob
import time
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import colors as mcolors
from AFC_func import get_filenames, getLog
from RBG_code import get_color_rgb
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout, Figure
from plotly import tools
from random import randint as ri

#start = time.time() 
#path = 'Sample Data/*/*.txt'   
#files = glob.glob(path) 
#filename_list = get_filenames(files) 
#labels = ['Date', 'Station', 'Gates', 'Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']
#log_df = pd.DataFrame(columns=labels)
#for filename in filename_list:
#    df = getLog(filename)
#    log_df= log_df.append(df)
#
#log_df= log_df[['Date', 'Station', 'Gates', 'Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']]    
#log_df.reset_index(inplace=True)       
#log_df.drop(columns='index', inplace=True)    
#log_df.to_csv('Sample.csv')    
#
#end = time.time()
#print('{0:5.2f}'.format(end-start), 's to extract logs.')

log_df = pd.read_csv('Sample.csv') 
plots_list = ['By Stations', 'By Dates', 'By Gates']
stn_list = list(log_df['Station'].unique())
dates_list = list(log_df['Date'].unique())
parameters_list = ['Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']

app = dash.Dash()

app.layout = html.Div([
        
                html.H1(
                    'DASHBOARD',
                    style={'textAlign':'center'}
                    ),
                
                html.H2(
                    'Fare Gates Fault Trending',
                    style={'font-size': '40px', 'font-style': 'oblique','textAlign':'center'}
                    ),
                
                
                html.Div([

                    html.Label(
                        'Select Plots:',
                        style={'font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    dcc.Dropdown(
                        id= 'plot_drpdwn',
                        options=[{'label': p, 'value': p} for p in plots_list],
                        value=plots_list,
                        multi=True,
                    ),
    
                    html.Label(
                        'Select Parameters:',
                        style={'font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    dcc.Dropdown(
                        id = 'parameter_drpdwn',
                        options=[{'label': p, 'value': p} for p in parameters_list],
                        value='Tailgate',
                        multi=False
                    ),
                ], className= "col s4 push-s1", style={'font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                ),
                
                html.Div([
                        
                    html.Label(
                        'Select Dates:',
                        style={'font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    dcc.Dropdown(
                        id='dates_drpdwn',
                        options=[{'label': p, 'value': p} for p in dates_list],
                        value=dates_list,
                        multi=True,
                    ),
                            
                    html.Label(
                        'Select Station:',
                        style={'font-size': '20px', 'font-style': 'oblique','textAlign':'left'}
                    ),
                    
                    dcc.Dropdown(
                        id='station_drpdwn',
                        options=[{'label': p, 'value': p} for p in stn_list],
                        value=stn_list,
                        multi=False,
                    ), 
                
                ], className= "col s4 push-s2", style={'width': '40%','font-size': '20px', 'font-style': 'oblique','textAlign':'left'} 
                ),
            
                
                html.Div([
                        
                    dcc.Graph(id='graph-with-drpdwn'),
                    
                ],style={'width': '100%', 'float': 'center','margin-top':200}   
                )
         
            ], className="row"
            )





colors_dict, colors_list = get_color_rgb()
groupby_df = log_df.groupby(['Date','Station']).sum()         

@app.callback(
    dash.dependencies.Output('graph-with-drpdwn', 'figure'),
    [dash.dependencies.Input('parameter_drpdwn', 'value')])
def update_figure(parameter):

    m = len(colors_list)-len(dates_list)-1
    n = ri(0,m)

    traces_dict = {}
    for i,name in enumerate(dates_list):
        traces_dict[name] = {
                'type':'bar',
                'x':groupby_df.loc[dates_list[i]].index,
                'y':groupby_df.loc[dates_list[i]][parameter],
                'hoverinfo':'x+y',
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
                'height':800,
                'paper_bgcolor':colors_dict['white'],
                'plot_bgcolor':colors_dict['whitesmoke'],
                'xaxis':{
                        'title':'Stations',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'showgrid':False,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':1
                        },
                'yaxis':{
                        'title':'Counts',
                        'titlefont':{'size':20, 'color':colors_dict['navy']},
                        'showgrid':True,
                        'zeroline':True,
                        'showline':True,
                        'gridcolor':colors_dict['white'],
                        'gridwidth':2
                        }            
                
                }
        }        
        


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})
    
external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)
    
  
    
    
    
    
    
######################################        
#        html.H1(
#            'DASHBOARD',
#            style={'textAlign':'center'}
#        ),
#        
#        html.Div(
#            'Titan-E Gates Fault Trending.',
#            style={'textAlign':'center'}
#        ),
#        
#        html.Div([
#            html.Label('Select Plots'),
#            dcc.Dropdown(
#                id= 'plot_drpdwn',
#                options=[{'label': p, 'value': p} for p in plots_list],
#                value=plots_list,
#                multi=True,
#            ),
#            html.Label('Select Parameters'),
#            dcc.Dropdown(
#                id = 'parameter_drpdwn',
#                options=[{'label': p, 'value': p} for p in parameters_list],
#                value=parameters_list,
#                multi=False,
#            )                        
#                
#        ],
#        className="container",
#        style={'width': '25%', 'float': 'left','margin-left':300}
#        
#        ),
#
#        html.Div([
#            html.Label('Select Dates'),
#            dcc.Dropdown(
#                id='dates_drpdwn',
#                options=[{'label': p, 'value': p} for p in dates_list],
#                value=dates_list,
#                multi=True,
#            ),
#            html.Label('Select Station'),
#            dcc.Dropdown(
#                id='station_drpdwn',
#                options=[{'label': p, 'value': p} for p in stn_list],
#                value=stn_list,
#                multi=False,
#            )                        
#                
#        ],
#        className="container",
#        style={'width': '25%', 'float': 'right','margin-right':300}
#        
#        ),
#        
#
#
#
#
#        
#        html.Div(
#            children=html.Div(id='graph'),
##            className='row',
#            style={'width': '80%', 'float': 'centre','margin-top':250}
#        ),
#        
#    ]
#    )
#
#colors_dict, colors_list = get_color_rgb()
#groupby_df = log_df.groupby(['Date','Station']).sum()         
#
#@app.callback(
#    dash.dependencies.Output('graph', 'children'),
#    [dash.dependencies.Input('parameter_drpdwn', 'value')])
#def update_figure(parameter):
#
#    m = len(colors_list)-len(dates_list)-1
#    n = ri(0,m)
#    
#            
#    traces_dict = {}
#    for i,name in enumerate(dates_list):
#        traces_dict[name] = {
#                'type':'bar',
#                'x':groupby_df.loc[dates_list[i]].index,
#                'y':groupby_df.loc[dates_list[i]][parameter],
#                'hoverinfo':'x+y',
#                'name':name,
#                'marker': {'color': colors_list[i+n],
#                           'line': {'color': colors_dict['navy'], 'width': 1}}
#                }            
#        
#    data1 = []
#    trace_keys = list(traces_dict.keys())
#    for key in trace_keys:
#        data1.append(traces_dict[key])             
#    
#    
#    layout1 = Layout(title=' Counts',
#                    titlefont=dict(size=16, color=colors_dict['navy']),
#                    barmode='stack',
#                    height=1000,
#                    width=1800,
#                    paper_bgcolor=colors_dict['white'],
#                    plot_bgcolor=colors_dict['whitesmoke'],
#                    xaxis=dict(
#                            title='Stations',
#                            titlefont=dict(size=16, color=colors_dict['navy']),
#                            showgrid=False,
#                            zeroline=True,
#                            showline=True,
#                            gridcolor=colors_dict['white'],
#                            gridwidth=1
#                            ),
#                    yaxis=dict(
#                            title='Counts',
#                            titlefont=dict(size=16, color=colors_dict['navy']),
#                            showgrid=True,
#                            zeroline=True,
#                            showline=True,
#                            gridcolor=colors_dict['white'],
#                            gridwidth=2
#                            ),
#                    )
#
#    graph_plot = html.Div(dcc.Graph(
#            id = 'parameters_plot',
#            animate=True,
#            figure = Figure(data=data1, layout=layout1),
#        ))
#
#    return graph_plot
###################################################    