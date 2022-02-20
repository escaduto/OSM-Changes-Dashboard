
import pandas as pd 
import os 

def is_geometryEdit(output_csv_name):   
    is_geometry_edit = []
    df_complete = pd.read_csv(os.path.join('../data', output_csv_name)).drop(columns = ['Unnamed: 0'])
    df = df_complete.drop_duplicates(subset = ["change_type", "osm_id","osm_type", "end_ds"]).reset_index(drop=True).drop(columns = ['start_ds', 'tag_key', 'tag_value', 'history'])
    for i, row in df.iterrows():
        osm_id = row['osm_id']
        change_type = row['change_type']
        osm_type = row['osm_type']
        ds = row['end_ds']
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

    geom_df = pd.DataFrame(is_geometry_edit, columns =['change_type', 'osm_id', 'osm_type', 'end_ds', 'old_geom', 'new_geom', 'is_geometry_edit'])
    return geom_df


def getGeomTrueDF(output_csv_name):
    geom_df = is_geometryEdit(output_csv_name)
    geomTrue = geom_df[geom_df['is_geometry_edit'] == True]
    return geomTrue

