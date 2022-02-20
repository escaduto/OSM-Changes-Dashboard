from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import box
import pandas as pd 
import numpy as np

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
      
def getBBOX(xml_object): 
    bounds = xml_object.find('bounds')
    if bounds != None:
        minlat = float(bounds.get('minlat'))
        minlon = float(bounds.get('minlon'))
        maxlat = float(bounds.get('maxlat'))
        maxlon = float(bounds.get('maxlon'))
        b = box(minlon, minlat, maxlon, maxlat, ccw=True)
        return b.wkt

def findNodeAttributes(xml_object, history_type, feature_type, input_change_type): 
    body = xml_object.find(feature_type)
    osm_id = body.get('id')
    lat = body.get('lat')
    lon = body.get('lon')
    node_geom = Point(float(lon),float(lat))
    return (input_change_type, history_type, feature_type, osm_id, node_geom, getTag(body))

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