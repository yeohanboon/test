# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 15:16:31 2018

@author: YEOHANBOON
"""

import pandas as pd
import datetime
import glob
import time
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import colors as mcolors
from RBG_code import get_color_rgb
from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Layout, Figure
from plotly import tools
from random import randint as ri
start = time.time() 

path = 'Sample Data/*/*.txt'   
files = glob.glob(path)  
#print(files)
#len(files)

def get_filenames(files):
    filename_list = [] 
    for name in files:
        with open(name) as f:
            filename_list.append(name)
    
    index_remove = []
    for i, filename in enumerate(filename_list):
        if filename.endswith('Check_Exceptions.txt'):
            index_remove.append(i)
    for i,index in enumerate(index_remove):
        filename_list.pop(index-i)
    return filename_list

#filename_list = get_filenames(files)




def getLog(filename):
    with open(filename, 'r') as log:
        line_list = log.readlines()
    
    
    for line in line_list:
        line_list.remove('\n')
    log_info = line_list[0].split()
    
    def get_station(info):
        stn_name = []
        stn_name.append(info[info.index('for')+1 : info.index('Station')])
        station = ' '. join(stn_name[0])
        return station
    station = get_station(log_info)
    #print(station)
    
    def get_gates(info):
        stn_abb = info[1].split()[0]
        gate_list = []
        i = 0
        while i < len(info)-1:
            if info[i].split()[1].startswith('G'):
                gate_list.append(info[i].split()[1])
            else:
                pass
            i += 1
        return stn_abb, gate_list
            
    stn_abb, gate_list = get_gates(line_list)
    numgates = len(gate_list)    
    
    
    def get_date(info):
        log_date = []
        log_date.append(info[info.index('on')+1 : info.index('started')])
        log_datestring = ' '.join(log_date[0])
        return log_datestring
    log_datestring = get_date(log_info)
    log_date = pd.to_datetime(log_datestring, format = '%d %b %Y')
    log_date = datetime.date(log_date.year, log_date.month, log_date.day)
    #print(log_date)   
    
    def get_gates(info):
        stn_abb = info[1].split()[0]
        gate_dict = {}
        i = 0
        for i in range(len(info)-1):
            line_split = info[i].split()
            
            if line_split[4] == 'Comms':
                gate_num = line_split[1]
                parameters = {'Intrusion':0, 
                              'Tailgate':0, 
                              'Passage_Cancel':0, 
                              'HCSS_Error':0, 
                              'Barrier_Hit':0}            
                gate_dict[gate_num] = parameters
            
            elif line_split[4] != 'Comms' and line_split[1].startswith('G'):
                gate_num = line_split[1]
                intrusion_index = line_split.index('Intrusion') + 3
                tailgate_index = line_split.index('Tailgate') + 3
                cancel_index = line_split.index('Cancel') + 2
                hcss_index = line_split.index('HCSS') + 3
                hit_index = line_split.index('HIT') + 3
                parameters = {'Intrusion': int(line_split[intrusion_index]), 
                              'Tailgate': int(line_split[tailgate_index]), 
                              'Passage_Cancel': int(line_split[cancel_index]), 
                              'HCSS_Error': int(line_split[hcss_index]), 
                              'Barrier_Hit': int(line_split[hit_index])}
                gate_dict[gate_num] = parameters
                
                
            else:
                pass
            i += 1
    
        return stn_abb, gate_dict
    
    stn_abb, gate_dict = get_gates(line_list)
    
     
    info_dict = {'Station': station,
                 'Station ABB': stn_abb,
                 'Date': log_date.isoformat(),
                 'Num Gates': numgates,
                 'Gates': gate_dict}
    #info_dict.update(gate_dict)
    #print(info_dict)
    
    
    df = pd.DataFrame.from_dict(info_dict['Gates'])
    df = df.transpose()
    df.rename_axis('Gates', axis = 0, inplace=True)
    df.reset_index(inplace=True)
    df['Station'] = info_dict['Station ABB']
    df['Date'] = info_dict['Date']
    #df.to_csv('Sample.csv')
    #df.set_index('Station', inplace = True)
#    print(df)
    
    return df

'''
labels = ['Date', 'Station', 'Gates', 'Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']
log_df = pd.DataFrame(columns=labels)
for filename in filename_list:
    df = getLog(filename)
    log_df= log_df.append(df)

log_df= log_df[['Date', 'Station', 'Gates', 'Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']]    
log_df.reset_index(inplace=True)       
log_df.drop(columns='index', inplace=True)    

log_df.to_csv('Sample.csv')    


end = time.time()
print('{0:5.2f}'.format(end-start), 's to extract logs.')    
 ''' 
#%%
#faregate_dict ={}
#cols = list(log_df)
#stn_list = list(log_df['Station'].unique())
#dates_list = list(log_df['Date'].unique())
#log_df.groupby('Date').sum()
#log_df.groupby('Station').sum()
#log_df.groupby(['Station','Date']).sum()
#log_df.groupby(['Station','Gates']).sum()
#log_df.groupby(['Date','Station','Gates']).sum()
#log_df.groupby(['Station','Date','Gates']).sum()
#log_df.groupby(['Station', 'Gates', 'Date']).sum()


#%%
#sum_HCSS_Error = groupby_stn.HCSS_Error.sum()
#data = [Bar(y=sum_HCSS_Error.nlargest(20).index,
#            x=sum_HCSS_Error.nlargest(20).values,
#            orientation = 'h'
#            )]            
#layout = Layout(title='HCSS Error Counts (Top 20 Stations)')
#fig = Figure(data=data, layout=layout)              
#plot(fig, filename='Sum HCSS Error.html')


#%%
###Colormap###
colors_cmap = []
for i in range(12):    
    rgb=plt.cm.Paired(i%12/12)
#    rgb=plt.cm.Pastel1(i%9/9)
#    rgb=plt.cm.Pastel2(i%8/8)
#    rgb=plt.cm.tab20(i%20/20)
#    rgb=plt.cm.Set1(i%9/9)    
#    rgb=plt.cm.Set3(i%12/12)
#    rgb=plt.cm.rainbow(i)
    rgb_tuple = (rgb[0], rgb[1], rgb[2])
    rgb_convert = tuple(int(x*255) for x in rgb_tuple)
    rgb_string = 'rgb' + str(rgb_convert)
    colors_cmap.append(rgb_string)
  
colors_rgb, colors_list = get_color_rgb()

#%%
###Parameters Counts Barchart###


#parameters_df = log_df[['Date', 'Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel','Tailgate']]
#by_date = parameters_df.groupby('Date').sum()
#m = len(colors_list)-len(dates_list)-1
#n = ri(0,m)
#traces_dict = {}
#for i,name in enumerate(dates_list):
#    traces_dict[name] = {
#            'type':'bar',
#            'x':by_date.iloc[i].index,
#            'y':by_date.iloc[i].values,
#            'hoverinfo':'x+y',
#            'name':name,
#            'marker': {'color': colors_list[i+n],
#                       'line': {'color': colors_rgb['navy'], 'width': 1}}
#            }
#       
#
#data = []
#trace_keys = list(traces_dict.keys())
#for key in trace_keys:
#    data.append(traces_dict[key])             
#layout = Layout(title='Parameters Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
#                titlefont=dict(size=16, color=colors_rgb['navy']),
#                barmode='group',
#                paper_bgcolor=colors_rgb['white'],
#                plot_bgcolor=colors_rgb['whitesmoke'],
#                xaxis=dict(
#                        title='Gate Parameters',
#                        titlefont=dict(size=16, color=colors_rgb['navy']),
#                        showgrid=False,
#                        zeroline=True,
#                        showline=True,
#                        gridcolor=colors_rgb['white'],
#                        gridwidth=1
#                        ),
#                yaxis=dict(
#                        title='Counts',
#                        titlefont=dict(size=16, color=colors_rgb['navy']),
#                        showgrid=True,
#                        zeroline=True,
#                        showline=True,
#                        gridcolor=colors_rgb['white'],
#                        gridwidth=2
#                        ),
#                )
#fig = Figure(data=data, layout=layout)              
#plot(fig, filename='Parameter Counts.html')

#%%
###Parameter Counts Barchart all Stations Function###

#groupby_df = log_df.groupby(['Date','Station']).sum()

def parameters_counts(parameter,dates,colors,colors_dict):
    m = len(colors)-len(dates)-1
    n = ri(0,m)
    traces_dict = {}
    for i,name in enumerate(dates):
        traces_dict[name] = {
                'type':'bar',
                'x':groupby_df.loc[dates[i]].index,
                'y':groupby_df.loc[dates[i]][parameter],
                'hoverinfo':'x+y',
                'name':name,
                'marker': {'color': colors_list[i+n],
                           'line': {'color': colors_dict['navy'], 'width': 1}}
                }    
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key])             
    layout = Layout(title=parameter+' Counts'+' ('+ dates[0] + ' to ' + dates[-1] + ')',
                    titlefont=dict(size=16, color=colors_dict['navy']),
                    barmode='stack',
                    paper_bgcolor=colors_dict['white'],
                    plot_bgcolor=colors_dict['whitesmoke'],
                    xaxis=dict(
                            title='Stations',
                            titlefont=dict(size=16, color=colors_dict['navy']),
                            showgrid=False,
                            zeroline=True,
                            showline=True,
                            gridcolor=colors_dict['white'],
                            gridwidth=1
                            ),
                    yaxis=dict(
                            title='Counts',
                            titlefont=dict(size=16, color=colors_dict['navy']),
                            showgrid=True,
                            zeroline=True,
                            showline=True,
                            gridcolor=colors_dict['white'],
                            gridwidth=2
                            ),
                    )
    fig = Figure(data=data, layout=layout)              

    return plot(fig, filename=parameter+' Counts.html')

#parameters_list = ['Barrier_Hit', 'HCSS_Error', 'Intrusion', 'Passage_Cancel', 'Tailgate']
#for gatesparameter in parameters_list:    
#    parameters_counts(gatesparameter,dates_list,colors_list,colors_rgb)


#%%
###Parameter Counts Barchart by Station Function###

#groupby_df = log_df.groupby(['Date','Station','Gates']).sum()

def parameters_counts(parameter,dates,station,colors,colors_dict):
    m = len(colors)-len(dates)-1
    n = ri(0,m)
    traces_dict = {}
    for i,name in enumerate(dates):
        traces_dict[name] = {
                'type':'bar',
                'x':groupby_df.loc[dates[i],station].index,
                'y':groupby_df.loc[dates[i]]['Tailgate'],
                'hoverinfo':'x+y',
                'name':name,
                'marker': {'color': colors[i+n],
                           'line': {'color': colors_dict['navy'], 'width': 1}}
                }    
    data = []
    trace_keys = list(traces_dict.keys())
    for key in trace_keys:
        data.append(traces_dict[key])             
    layout = Layout(title=station + ' Station,'+parameter+' Counts'+' ('+ dates[0] + ' to ' + dates[-1] + ')',
                    titlefont=dict(size=16, color=colors_dict['navy']),
                    barmode='stack',
                    paper_bgcolor=colors_dict['white'],
                    plot_bgcolor=colors_dict['whitesmoke'],
                    xaxis=dict(
                            title='Gates',
                            titlefont=dict(size=16, color=colors_dict['navy']),
                            showgrid=False,
                            zeroline=True,
                            showline=True,
                            gridcolor=colors_dict['white'],
                            gridwidth=1
                            ),
                    yaxis=dict(
                            title='Counts',
                            titlefont=dict(size=16, color=colors_dict['navy']),
                            showgrid=True,
                            zeroline=True,
                            showline=True,
                            gridcolor=colors_dict['white'],
                            gridwidth=2
                            ),
                    )
    fig = Figure(data=data, layout=layout)              
    plot(fig, filename=parameter+' Counts '+'station.html')    

#parameters_counts('Tailgate',dates_list,'JUR',colors_list,colors_rgb)










#%%
'''    
###Tailgate Counts Barchart###

groupby_df = log_df.groupby(['Date','Station']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i]].index,
            'y':groupby_df.loc[dates_list[i]]['Tailgate'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='Tailgate Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='Stations',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Tailgate Counts.html')    
    
#%% 
###HCSS Error Counts Barchart###

groupby_df = log_df.groupby(['Date','Station']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i]].index,
            'y':groupby_df.loc[dates_list[i]]['HCSS_Error'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='HCSS Error Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='Stations',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='HCSS Error Counts.html')      
    
#%%    
###Barrier Hit Counts Barchart###

groupby_df = log_df.groupby(['Date','Station']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i]].index,
            'y':groupby_df.loc[dates_list[i]]['Barrier_Hit'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='HCSS Error Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='Stations',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Barrier Hit Counts.html')      
       
#%%    
###Passage Cancel Counts Barchart###

groupby_df = log_df.groupby(['Date','Station']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i]].index,
            'y':groupby_df.loc[dates_list[i]]['Passage_Cancel'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='Passage Cancel Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='Stations',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Passage Cancel Counts.html')      
           
#%%    
###Intrusion Counts Barchart###

groupby_df = log_df.groupby(['Date','Station']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i]].index,
            'y':groupby_df.loc[dates_list[i]]['Intrusion'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='Intrusion Counts'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='Stations',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Intrusion Counts.html')      


#%%
###Tailgate Counts Barchart###
###JUR Station###
groupby_df = log_df.groupby(['Date','Station','Gates']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i],'JUR'].index,
            'y':groupby_df.loc[dates_list[i]]['Tailgate'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='Tailgate Counts by Gates'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='JUR Station',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Tailgate Counts JUR.html')      
    
#%%    
###Tailgate Counts Barchart###
###ORC Station###
groupby_df = log_df.groupby(['Date','Station','Gates']).sum()
m = len(colors_list)-len(dates_list)-1
n = ri(0,m)
traces_dict = {}
for i,name in enumerate(dates_list):
    traces_dict[name] = {
            'type':'bar',
            'x':groupby_df.loc[dates_list[i],'ORC'].index,
            'y':groupby_df.loc[dates_list[i]]['Tailgate'],
            'hoverinfo':'x+y',
            'name':name,
            'marker': {'color': colors_list[i+n],
                       'line': {'color': colors_rgb['slategray'], 'width': 1.5}}
            }    
data = []
trace_keys = list(traces_dict.keys())
for key in trace_keys:
    data.append(traces_dict[key])             
layout = Layout(title='Tailgate Counts by Gates'+' ('+ dates_list[0] + ' to ' + dates_list[-1] + ')',
                titlefont=dict(size=16, color=colors_rgb['navy']),
                barmode='stack',
                paper_bgcolor=colors_rgb['white'],
                plot_bgcolor=colors_rgb['whitesmoke'],
                xaxis=dict(
                        title='ORC Station',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=False,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=2
                        ),
                yaxis=dict(
                        title='Counts',
                        titlefont=dict(size=16, color=colors_rgb['navy']),
                        showgrid=True,
                        zeroline=True,
                        showline=True,
                        gridcolor=colors_rgb['white'],
                        gridwidth=1
                        ),
                )
fig = Figure(data=data, layout=layout)              
plot(fig, filename='Tailgate Counts ORC.html')      
        
'''    
#%%    
    

