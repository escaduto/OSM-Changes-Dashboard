from cleanXML import clean_df, explodeTags
from timeRange import retrieve_DS_List
import pandas as pd 
import requests 
import xml.etree.ElementTree as ET


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