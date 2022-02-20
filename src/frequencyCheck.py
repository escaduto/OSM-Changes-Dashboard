import pandas as pd 

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


    