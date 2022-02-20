import ipywidgets as widgets 
from ipywidgets import AppLayout, Button, Layout, Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider, DatePicker, Output, VBox, HBox, Text, SelectMultiple, Combobox, Accordion
from IPython.display import clear_output, HTML, display, Image
from drawMap import createMap
import threading
import time
from retrieveData import retrieveOSMDATA
from drawMap import getEmptyFeatureCollection

#-----------------------------------------------------WIDGETS-------------------------------------------# 
# HEADER
header = widgets.HTML("<h1>OSM Data Change Tracker</h1>", layout=Layout(height='auto'))
header.style.text_align='center'

footer = widgets.HTML('<h5 style="color:DodgerBlue;"> Source: OpenStreet Map via Overpass API </h5>', layout=Layout(height='auto'))

# DATE PICKER
start_dt = DatePicker(layout=Layout(flex='1 1 0%', width='auto'), disabled=False)
end_dt = DatePicker(layout=Layout(flex='1 1 0%', width='auto'), disabled=False)

# Map Coord
map_coord = widgets.Text(
        value= '(-51.71312453127716, -59.65015951499032)',
        description='Map Center:',
        disabled=False, style=dict(description_width='initial'),
        continuous_update=False
        )

# Map Zoom
map_zoom = widgets.IntText(
    value=15,
    description='Zoom:',
    disabled=False,
    continuous_update=False
)

# BBOX 
bbox_coord = widgets.Text(
    value= '(37.22828,131.85043,37.25282, 131.88316)',
    description='Bbox Coord:',
    disabled=False, style=dict(description_width='initial')
    )

# Filenam
input_filename = widgets.Text(
    value='sample.csv',
    placeholder='filename',
    description='Save File as:',
    disabled=False, style=dict(description_width='initial')
    )

# SPECIFY INTERVAL
hourly_slider = widgets.IntSlider(
    value=24,
    min=1,
    max=200,
    description='Hourly Interval:'
)

# REQUEST BUTTON 
Request_button = widgets.Button(
    description='Download Data',
    disabled=False,
    button_style='success',
    icon='table', layout = Layout(width='200px', height='auto'),
    style=dict(description_width='initial'))


# BBOX Refresh button
bbox_button = widgets.Button(
    description='Update',
    disabled=False,
    button_style='warning',
    icon='arrow-rotate-right', layout = Layout(width='80px', height='auto'),
    style=dict(description_width='initial'))

progress_search = widgets.FloatProgress(value=0.0, min=0.0, max=1.0, 
    description='Progress',
    bar_style='info',
    style={'bar_color': '#94b79f'})
Complete_msg = widgets.HTML()


#-----------------------------------------------------widget functions-----------------------------------------# 

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
    feature_collection = getEmptyFeatureCollection()
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

#-----------------------------------------------------getTab1------------------------------------------# 

def getTab1():
    tab1_header = widgets.HTML(value='<h2>OSM Change Downloader</h2>')
    tab1 = HBox(children=[VBox(children=[tab1_header, HBox(children=[Label(value='Start Date', layout=dict(height='auto')), 
                                                                    start_dt, Label(value='End Date', layout=dict(height='auto')), end_dt]), 
                                        hourly_slider, 
                                        HBox(children=[bbox_coord, bbox_button]), 
                                        input_filename, 
                                        Request_button, 
            
                                        HBox(children=[progress_search, Complete_msg]), footer]), 
                                        VBox(children=[HBox(children=[map_coord, map_zoom]), createMap(eval(map_coord.value), map_zoom.value)])])

    Request_button.on_click(callback)
    bbox_button.on_click(updateBBOX)
    map_coord.observe(tab1_on_value_change, names='value')
    map_zoom.observe(tab1_on_value_change, names='value')     
                                
    return tab1


def tab1_on_value_change(change):
    clear_output()
    tab1 = getTab1()
    display(tab1) 