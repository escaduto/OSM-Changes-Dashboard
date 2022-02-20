from ipyleaflet import Map, basemaps, basemap_to_tiles, DrawControl, GeoData, LayersControl

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

def createMap(map_center, map_zoom):
    draw_control = getDrawControl() 

    terrain_base = basemap_to_tiles(basemaps.OpenStreetMap.Mapnik)

    m = Map(layers=(terrain_base, ), center=map_center, zoom=map_zoom)

    draw_control.on_draw(handle_draw)

    m.add_control(draw_control)
    m.layout.width='auto'
    m.layout.height='600'
    return m 