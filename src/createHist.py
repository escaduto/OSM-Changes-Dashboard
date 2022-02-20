import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

def checkPivot_ChangeType(dff):
    if 'create' not in dff:
        dff['create'] = 0
    elif 'delete' not in dff:
        dff['delete'] = 0 
    elif 'modify' not in dff: 
        dff['modify'] = 0 
    return dff 

def checkPivot_OsmType(dff):
    if 'node' not in dff:
        dff['node'] = 0
    elif 'relation' not in dff:
        dff['relation'] = 0 
    elif 'way' not in dff: 
        dff['way'] = 0 
    return dff 

def getChangeTypeDF(df_unique):
    df_byDay = df_unique.groupby(["end_ds", "change_type"])['osm_id'].count().reset_index(name='count')
    df_byDay['end_ds'] = pd.to_datetime(df_byDay['end_ds']).dt.date
    df_byDay['end_ds'] = df_byDay['end_ds'].apply(lambda x: x.strftime('%Y-%m-%d'))

    df1 = df_byDay.pivot(index='end_ds', columns='change_type', values='count').fillna(0)
    df1 = df1.reset_index()
    df1 = checkPivot_ChangeType(df1)
    df1 = checkPivot_ChangeType(df1)
    df1 = checkPivot_ChangeType(df1)
    return df1

def getOsmType(df_unique):
    df_byDay_osmType = df_unique.groupby(["end_ds", "osm_type"])['osm_id'].count().reset_index(name='count')
    df_byDay_osmType['end_ds'] = pd.to_datetime(df_byDay_osmType['end_ds']).dt.date
    df_byDay_osmType['end_ds'] = df_byDay_osmType['end_ds'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df2 = df_byDay_osmType.pivot(index='end_ds', columns='osm_type', values='count').fillna(0)
    df2 = df2.reset_index()
    df2 = checkPivot_OsmType(df2)
    df2 = checkPivot_OsmType(df2)
    df2 = checkPivot_OsmType(df2)
    return df2

def get_freq_plot(df_unique):
    df1  = getChangeTypeDF(df_unique)
    df2 = getOsmType(df_unique)
    fig = go.Figure(go.Bar(x=df1['end_ds'], y=df1['create'], marker_color= 'green', opacity=0.65, name='create'))
    fig.add_trace(go.Bar(x=df1['end_ds'], y=df1['delete'], marker_color= 'firebrick', opacity=0.65, name='delete'))
    fig.add_trace(go.Bar(x=df1['end_ds'], y=df1['modify'], marker_color= 'purple', opacity=0.65, name='modify'))
    fig.add_trace(go.Scatter(x=df2['end_ds'], y=df2['node'], opacity=0.85, marker_color='yellow', name='node'))
    fig.add_trace(go.Scatter(x=df2['end_ds'], y=df2['relation'], opacity=0.85, marker_color= 'orange', name='relation'))
    fig.add_trace(go.Scatter(x=df2['end_ds'], y=df2['way'], opacity=0.85, marker_color='steelblue', name='way'))
    fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})

    g1 = go.FigureWidget(data=fig,
                    layout=go.Layout(
                        title=dict(
                            text='Change Type'
                        ),
                        barmode='stack'
                    ))
    display(g1)