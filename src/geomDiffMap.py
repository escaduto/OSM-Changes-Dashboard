from ipyleaflet import Map, WKTLayer, MarkerCluster, basemaps, basemap_to_tiles
from geomEdits import getGeomTrueDF 
from tab1_main import map_coord, map_zoom 


def createGeomEditMap(output_csv_name):
    terrain_base = basemap_to_tiles(basemaps.Stamen.Toner)

    m = Map(layers=(terrain_base, ), center=eval(map_coord.value), zoom=map_zoom.value)
    marker_list = [] 
    geom_df = getGeomTrueDF(output_csv_name).reset_index(drop=True)
    for i, row in geom_df.iterrows():
        if 'POLYGON' in row['old_geom']:
            w_oldlayer = WKTLayer(
                wkt_string=row['old_geom'],
                style={"fillColor": "red", "color":"red"},
            )
            w_newlayer = WKTLayer(
                wkt_string=row['new_geom'],
                style={"fillColor": "green", "color":"green"},
            )
            m.add_layer(w_oldlayer)
            m.add_layer(w_newlayer)
        elif 'POINT' in row['old_geom']:
            w_oldlayer = WKTLayer(
                wkt_string=row['old_geom'],
                style={"fillColor": "red", "color":"red"},
            )
            w_newlayer = WKTLayer(
                wkt_string=row['new_geom'],
                style={"fillColor": "green", "color":"green"},
            )
            marker_list.append(w_newlayer)
            marker_list.append(w_oldlayer)

    marker_cluster = MarkerCluster(
        markers=(marker_list),
    )

    m.add_layer(marker_cluster)

    m.layout.width='auto'
    m.layout.height='600'
    return m 