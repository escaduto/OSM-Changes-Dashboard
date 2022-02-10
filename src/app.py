import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np 
import regex as re 
import lxml 
from lxml.html.soupparser import fromstring 
import xml.etree.ElementTree as ET
import numbers 
import os
import geopandas as gpd
import overpy
import overpass
import shapely.geometry
from pandas.io.json import json_normalize
import requests
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.geometry import box


# get node ID, node coordinates (lat/lon), tags (key/value) 
# [later TODO] get members of relation (tags?) and nodes (nd) of ways 

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














    