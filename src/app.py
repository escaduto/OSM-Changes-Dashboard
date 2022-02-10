import pandas as pd
import requests
import numpy as np 
from lxml.html.soupparser import fromstring 
import xml.etree.ElementTree as ET
import os
import geopandas as gpd
from pandas.io.json import json_normalize
import requests
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import box
from pandas.io.json import json_normalize
import datetime
from datetime import date, datetime, timedelta
import seaborn as sns 
import matplotlib.pyplot as plt
from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, GeoData, LayersControl
import ipywidgets as widgets 
from ipywidgets import AppLayout, Button, Layout, Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider, DatePicker, Output, VBox, HBox, Text, SelectMultiple, Combobox, Accordion
from ipywidgets.embed import embed_data
from IPython.display import clear_output, HTML, display, Image
import matplotlib.pyplot as plt
import datetime
from os import listdir
from os.path import isfile, join


# get node ID, node coordinates (lat/lon), tags (key/value) 
# [later TODO] get members of relation (tags?) and nodes (nd) of ways 

# Clean XML 

def getTag(xml_object):
    node_tags = xml_object.findall('tag')
    key = [] 
    val = [] 
    if len(node_tags) != 0:
        for tag in node_tags: 
            tag_key = tag.get('k')
            tag_value = tag.get('v')
            key.append(tag_key)
            val.append(tag_value)
    return list(zip(key, val))
      
def findNodeAttributes(xml_object, history_type, feature_type, input_change_type): 
    body = xml_object.find(feature_type)
    osm_id = body.get('id')
    lat = body.get('lat')
    lon = body.get('lon')
    node_geom = Point(float(lon),float(lat))
    return (input_change_type, history_type, feature_type, osm_id, node_geom, getTag(body))

def getBBOX(xml_object): 
    bounds = xml_object.find('bounds')
    if bounds != None:
        minlat = float(bounds.get('minlat'))
        minlon = float(bounds.get('minlon'))
        maxlat = float(bounds.get('maxlat'))
        maxlon = float(bounds.get('maxlon'))
        b = box(minlon, minlat, maxlon, maxlat, ccw=True)
        return b.wkt

def findWayAttributes(xml_object, history_type, feature_type, input_change_type): 
  body = xml_object.find(feature_type)
  osm_id = body.get('id')
  bbox = getBBOX(body)
  return (input_change_type, history_type, feature_type, osm_id, bbox, getTag(body))

def findRelationAttributes(xml_object, history_type, feature_type, input_change_type): 
  body = xml_object.find(feature_type)
  osm_id = body.get('id')
  bbox = getBBOX(body)
  return (input_change_type, history_type, feature_type, osm_id, bbox, getTag(body))

def getCreatedOSMIDS(root, input_change_type='create'): 
    created_list = [] 
    for action in root.findall('action'):
        changeType = action.get('type')
        if changeType == input_change_type: 
            if action.find('node') != None:
                output = findNodeAttributes(action, 'new', 'node', input_change_type)
                created_list.append(output)
            elif action.find('way') != None:
                output = findWayAttributes(action, 'new', 'way', input_change_type)
                created_list.append(output)
            elif action.find('relation') != None:
                output = findRelationAttributes(action, 'new', 'relation', input_change_type)
                created_list.append(output)
    return created_list

def getDeletedOSMIDS(root, input_change_type='delete'):
    deleted_list = [] 
    for action in root.findall('action'):
        changeType = action.get('type')
        if changeType == input_change_type: 
            old = action.find('old')
            new = action.find('new') # can get if visible key, but skip for now 
            if old.find('node') != None:
                output = findNodeAttributes(old,'old', 'node', input_change_type)
                deleted_list.append(output)
            elif old.find('way') != None:
                output = findWayAttributes(old, 'old', 'way', input_change_type)
                deleted_list.append(output)
            elif old.find('relation') != None:
                output = findRelationAttributes(old, 'old', 'relation', input_change_type)
                deleted_list.append(output)
    return deleted_list

def getModifiedOSMIDS(root, input_change_type='modify'):
    modified_list = [] 
    for action in root.findall('action'):
        changeType = action.get('type')
        if changeType == input_change_type: 
            old = action.find('old')
            new = action.find('new')
            if old.find('node') != None:
                old_output = findNodeAttributes(old, 'old', 'node', input_change_type)
                new_output = findNodeAttributes(new, 'new', 'node', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
            elif old.find('way') != None:
                old_output = findWayAttributes(old, 'old', 'way', input_change_type)
                new_output = findWayAttributes(new, 'new', 'way', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
            elif old.find('relation') != None:
                old_output = findRelationAttributes(old, 'old', 'relation', input_change_type)
                new_output = findRelationAttributes(new, 'new', 'relation', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
    return modified_list

def getModifiedOSMIDS(root, input_change_type='modify'):
    modified_list = [] 
    for action in root.findall('action'):
        changeType = action.get('type')
        if changeType == input_change_type: 
            old = action.find('old')
            new = action.find('new')
            if old.find('node') != None:
                old_output = findNodeAttributes(old, 'old', 'node', input_change_type)
                new_output = findNodeAttributes(new, 'new', 'node', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
            elif old.find('way') != None:
                old_output = findWayAttributes(old, 'old', 'way', input_change_type)
                new_output = findWayAttributes(new, 'new', 'way', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
            elif old.find('relation') != None:
                old_output = findRelationAttributes(old, 'old', 'relation', input_change_type)
                new_output = findRelationAttributes(new, 'new', 'relation', input_change_type)
                modified_list.append(old_output)
                modified_list.append(new_output)
    return modified_list

def clean_df(root):
    '''
    Create Dataframe w/ list of tuples
    Returns a dataframe with merged/concatenated results 
    '''
    # get osm data 
    deleted_Results = getDeletedOSMIDS(root)
    modified_Results = getModifiedOSMIDS(root)
    created_Results = getCreatedOSMIDS(root)

    # create df 
    df_deleted_Results = pd.DataFrame(deleted_Results, columns =['change_type', 'history', 'osm_type', 'osm_id', 'geometry', 'tags'])
    df_modified_Results = pd.DataFrame(modified_Results, columns =['change_type', 'history', 'osm_type', 'osm_id', 'geometry', 'tags'])
    df_created_Results = pd.DataFrame(created_Results, columns =['change_type', 'history', 'osm_type', 'osm_id', 'geometry', 'tags'])

    # merge df 
    list_df = [df_deleted_Results, df_modified_Results, df_created_Results]
    complete_df = pd.concat(list_df)

    return complete_df

def explodeTags(df, start_ds, end_ds):
    '''
    Explode tag lists into separate rows 
    Also added start, end dates from query 
    Returns a dataframe 
    '''
    df = df.explode('tags')
    df_nonNull = df.loc[df['tags'].notnull()]
    df_nonNull = pd.concat([df_nonNull,pd.DataFrame(df_nonNull.pop('tags').tolist(),index=df_nonNull.index)],axis=1)
    df_nonNull.columns = ['change_type', 'history', 'osm_type', 'osm_id', 'geometry', 'tag_key', 'tag_value']
    df_withNull = df.loc[df['tags'].isnull()]
    df_withNull.columns = ['change_type', 'history', 'osm_type', 'osm_id', 'geometry', 'tag_key']
    df_withNull['tag_value'] = np.nan

    lst = [df_withNull, df_nonNull]
    complete_df = pd.concat(lst)
    complete_df = complete_df.reset_index()
    complete_df = complete_df.drop(columns = ['index'])

    complete_df['start_ds'] = start_ds
    complete_df['end_ds'] = end_ds
    return complete_df

# Convert to Geopandas 

def tryParseWKT(x):
    try:
        return wkt.loads(x)
    except:
        return None

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

def generateDSList(time_interval, start_yr, start_mth, start_dt, end_yr, end_mth, end_dt):
    dts = [dt.strftime('%Y-%m-%dT%H:%M:%SZ') for dt in 
        datetime_range(datetime(start_yr, start_mth, start_dt, 0), datetime(end_yr, end_mth, end_dt, 0), 
        timedelta(hours=time_interval))]
    return dts

def retrieve_DS_List(interval, start_yr, start_mnth, start_dt, end_yr, end_mnth, end_dt):
    '''
    Create a list of start and end dates by interval
    '''
    dts = generateDSList(interval, start_yr, start_mnth, start_dt, end_yr, end_mnth, end_dt)
    start_dt_list = [] 
    end_dt_list = []

    for i in range(0, len(dts) - 1): 
        start_dt_list.append(dts[i])
        end_dt_list.append(dts[i+1])

    start_end_ds = list(zip(start_dt_list, end_dt_list))
    return start_end_ds 

def is_geometryEdit(df, output_csv_name):   
  is_geometry_edit = []
  for i, row in df.iterrows():
    osm_id = row['osm_id']
    change_type = row['change_type']
    osm_type = row['osm_type']
    ds = row['end_ds']
    df_complete = pd.read_csv(output_csv_name).drop(columns = ['Unnamed: 0'])
    if change_type == 'modify':
      old_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'old'))][:1].item()
      new_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'new'))][:1].item()
    elif change_type == 'create':
      old_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'new'))][:1].item()
      new_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'new'))][:1].item()
    elif change_type == 'delete':
      old_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'old'))][:1].item()
      new_geom = df_complete['geometry'].loc[((df_complete['end_ds'] == ds) & (df_complete['osm_id'] == osm_id) & (df_complete['history'] == 'old'))][:1].item()
    is_geometry_edit.append((change_type, osm_id, osm_type, ds, old_geom, new_geom, old_geom != new_geom))
  return is_geometry_edit

def getHistPlot(output_csv_name, plot_name):
    df_complete = pd.read_csv(output_csv_name).drop(columns = ['Unnamed: 0'])
    df_unique = df_complete.drop_duplicates(subset = ["change_type", "osm_id","osm_type", "end_ds"]).reset_index(drop=True).drop(columns = ['start_ds', 'tag_key', 'tag_value', 'history'])
    df_byDay = df_unique.groupby(["end_ds", "change_type"])['osm_id'].count().reset_index(name='count')
    df_byDay['end_ds'] = pd.to_datetime(df_byDay['end_ds']).dt.date
    sns.barplot(x = "end_ds", y = "count", hue="change_type", data = df_byDay)
    plt.ylabel("Count")
    plt.xlabel("Date Stamp")
    plt.xticks(rotation = 90)
    plt.title("Timeseries of OSM Changeset Counts")
    plt.savefig(os.path.join('../figs', plot_name), dpi=400, bbox_inches = "tight")
    plt.close()

# count by osm id 
def osmIDCounter(output_csv_name):
    '''
    Count num of changes by OSM ID
    [TODO] Be able to select by OSM_ID to populate old/new tags by date and see geom_edit if true.
    Returns dataframe with counts and osm links 
    '''
    df_complete = pd.read_csv(output_csv_name).drop(columns = ['Unnamed: 0'])
    df_unique = df_complete.drop_duplicates(subset = ["change_type", "osm_id","osm_type", "end_ds"]).reset_index(drop=True).drop(columns = ['start_ds', 'tag_key', 'tag_value', 'history'])
    df_byID = df_unique.groupby(["osm_type", "osm_id"])['end_ds'].count().reset_index(name='count')
    df_byID = df_byID.sort_values(by=['count'], ascending=False)
    df_byID['link'] =  [ 'https://www.openstreetmap.org/' + '/'.join(i) for i in zip(df_byID["osm_type"],df_byID["osm_id"].map(str))]
    df_byID['link'] = ['<a href="{}">{}</a>'.format(i,'osm link') for i in df_byID["link"]]

    return df_byID

def retrieveOSMDATA(interval, start_ds, end_ds, output_csv_name, bbox):
    start_yr = start_ds.year
    start_mnth = start_ds.month
    start_dt = start_ds.day
    end_yr = end_ds.year
    end_mnth = end_ds.month
    end_dt = end_ds.day
    df_complete = pd.DataFrame()
    url = 'http://overpass-api.de/api/interpreter'  # Overpass API URL
    start_end_ds = retrieve_DS_List(interval, start_yr, start_mnth, start_dt, end_yr, end_mnth, end_dt)

    for start_ds, end_ds in start_end_ds: 
        print(start_ds, end_ds)
        query = f"[out:xml][adiff:'%s','%s'];nwr%s;out geom;"% (start_ds, end_ds, str(bbox))
        r = requests.get(url, params={'data': query})
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            if len(root.findall('action')) != 0:
                ds_df = clean_df(root)
                ds_df = explodeTags(ds_df, start_ds, end_ds)
                df_complete = pd.concat([df_complete, ds_df])
            else: 
                print('empty request')
                continue
        else: 
            print('error in request')

    df_complete.to_csv(output_csv_name)
    return df_complete

def getDrawControl():
    draw_control = DrawControl(rectangle={ "shapeOptions": {
            "fillColor": "#fca45d",
            "color": "#fca45d",
            "fillOpacity":0.4}})
    return draw_control

def getEmptyFeatureCollection():
    feature_collection = {
        'type': 'FeatureCollection',
        'features': []
    }
    return feature_collection

def handle_draw(self, action, geo_json):
    feature_collection = getEmptyFeatureCollection()
    feature_collection['features'].append(geo_json)

def createMap(map_center, map_zoom, draw_control):
    terrain_base = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)

    m = Map(layers=(terrain_base, ), center=map_center, zoom=map_zoom)

    draw_control.on_draw(handle_draw)

    m.add_control(draw_control)
    m.layout.width='auto'
    m.layout.height='600'
    return m 

def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles




def work(progress_search):
    Complete_msg.value = ""
    total = 100
    for i in range(total):
        time.sleep(0.3)
        progress_search.value = float(i+1)/total
    Complete_msg.value = f"<h4 style='color:MediumSeaGreen;'> Complete! </h4>"

def callback(wdgt):
    thread = threading.Thread(target=work, args=(progress_search,))
    display(progress_search)
    thread.start()
    retrieveOSMDATA(hourly_slider.value, start_dt.value, end_dt.value, input_filename.value, bbox_coord.value)
    
def updateBBOX(wdgt):
  if len(feature_collection['features']) != 0: 
    coord_list = feature_collection['features'][0]['geometry']['coordinates'][0]
    minlon = coord_list[0][1]
    minlat = coord_list[0][0]
    maxlon = coord_list[1][1]
    maxlat = coord_list[2][0]
    bbox_tuple = (minlon, minlat, maxlon, maxlat)
    # bbox value 
    bbox_coord.value = str(bbox_tuple)
  else: 
    pass 


    
