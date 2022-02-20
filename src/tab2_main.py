import ipywidgets as widgets 
from ipywidgets import AppLayout, Button, Layout, Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider, DatePicker, Output, VBox, HBox, Text, SelectMultiple, Combobox, Accordion
from IPython.display import clear_output, HTML, display, Image
import os 
from os import listdir
from os.path import isfile, join
from geomDiffMap import createGeomEditMap
import dtale 
from createHist import get_freq_plot
from frequencyCheck import osmIDCounter
from geomEdits import getGeomTrueDF
import pandas as pd 


def get_files(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def tab2_on_value_change(change):
  df_complete = pd.read_csv(os.path.join('../data', selection_filename.value)).drop(columns = ['Unnamed: 0'])
  df_unique = df_complete.drop_duplicates(subset = ["change_type", "osm_id","osm_type", "end_ds"]).reset_index(drop=True).drop(columns = ['start_ds', 'tag_key', 'tag_value', 'history'])
  with plot_output: 
    clear_output()
    get_freq_plot(df_unique)

  with geomTable_output: 
    clear_output()
    geom_df = getGeomTrueDF(selection_filename.value).reset_index(drop=True)
    if len(geom_df) != 0:
      display(geom_df)
    else: 
      display(widgets.HTML(value='<h2>No Geometry Edits!</h2>'))

  with table_output:
    clear_output() 
    counter_df = osmIDCounter(os.path.join('../data', selection_filename.value)).head(10).reset_index(drop = True)
    display(HTML(counter_df.to_html(render_links=True, escape=False)))

  with completetable_output:
    clear_output()
    display(dtale.show(df_complete))

  with geom_map_output:
    clear_output()
    display(createGeomEditMap(selection_filename.value))


#-----------------------------------------------------WIDGETS-------------------------------------------# 

plot_output = widgets.Output(layout = Layout(width='auto', height='100'))
table_output = widgets.Output(layout = Layout(width='400px', height='auto'))
geomTable_output = widgets.Output(layout = Layout(width='auto', height='100'))
map_output = widgets.Output(layout = Layout(width='400px', height='auto'))
geom_map_output = widgets.Output(layout = Layout(width='600px', height='auto'))
completetable_output = widgets.Output(layout = Layout(width='auto', height='auto'))

selection_filename = widgets.Dropdown(
    options=get_files(os.path.join('../data')),
    description='Select File:',
    style=dict(description_width='initial')
)

selection_filename.observe(tab2_on_value_change, names='value')


def getTab2():
    tab2_header = widgets.HTML(value='<h2>Change Frequency</h2>')
    tab2 = HBox(children=[VBox(children=[tab2_header, selection_filename, HBox(children=[plot_output])])])          
    return tab2

def getTab3():
    tab3 = VBox(children=[geom_map_output, geomTable_output])
    return tab3

def getTab4():
    tab4 = HBox(children=[table_output])
    return tab4

def getTab5(): 
    tab5 = completetable_output
    return tab5