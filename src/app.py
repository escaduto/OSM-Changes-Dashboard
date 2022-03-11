from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import date
from dash.dependencies import Input, Output
import plotly.express as px
import os
import dash_leaflet as dl
from geomDiffMap import getPoints, getPolygon


df_complete = pd.read_csv(os.path.join('../data', 'FalklandIsland_010122_020822.csv')).drop(columns = ['Unnamed: 0'])
df_unique = df_complete.drop_duplicates(subset = ["change_type", "osm_id","osm_type", "end_ds"]).reset_index(drop=True).drop(columns = ['start_ds', 'tag_key', 'tag_value', 'history'])

df_byChange = df_unique.groupby(["change_type", "osm_type"])['osm_id'].count().reset_index(name='count')
df_byDay = df_unique.groupby(["end_ds",  "osm_type"])['osm_id'].count().reset_index(name='count')


df2 = px.data.election()
geojson = px.data.election_geojson()
candidates = df2.winner.unique()

app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df_byChange, x="change_type", y="count", color="osm_type", barmode="group")
bar_fig = px.line(df_byDay, x="end_ds", y="count", color="osm_type")
pie_fig = px.pie(df_byChange, values='count', names='change_type', title='Change Type Count')


old_polygon = dl.Polygon(color="#ef2e46", weight=1, positions=[getPolygon('../data/Jan21_Jan22_weekly_LiancourtRocks.csv', 'old_geom')])
new_polygon = dl.Polygon(color="#49ab81", weight=1, positions=[getPolygon('../data/Jan21_Jan22_weekly_LiancourtRocks.csv', 'new_geom')])
old_point = dl.Marker(position=[getPoints('../data/Jan21_Jan22_weekly_LiancourtRocks.csv', 'old_geom')])
new_point = dl.Marker(position=[getPoints('../data/Jan21_Jan22_weekly_LiancourtRocks.csv', 'new_geom')])

app.layout = html.Div([
    html.Div(children=[
        html.H1(children='OpenStreetMap Data Change',style={'textAlign': 'center','color': colors['text'], 'padding':10}),

        html.Div(children='''Tool for data visualization: a more interactive approach towards investigating changes in osm data.''', 
                style={'textAlign': 'center', 'color': colors['text'], 'padding':20}),
        html.Div(dcc.DatePickerRange(id='my-date-picker-range',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2023, 3, 1),
                                initial_visible_month=date(2022, 2, 1)
                            ), style={'padding':20}),
        html.Div(dcc.Checklist(['Added', 'Modified', 'Deleted'],['Modified', 'Added']), style={'text-align': 'center'}),
        html.Div(dcc.Dropdown(['Liancourt Rocks', 'Falkland Islands', 'Pratas', 'James Shoal', 'Spratly Islands(1)', 'Spratly Islands(2)', 'Spratly Islands(3)', 'Kuril (1)', 'Kuril (2)', 'Kuril (3)'], 'Liancourt Rocks', id='demo-dropdown'), style={'padding':20})
    ], style={'padding': 10, 'flex': 0.5}),
    html.Div(children=[
        dcc.Graph(
            id='example3-graph',
            figure=bar_fig
        ),
        dl.Map(center=[37.24131312495323, 131.86714247259735], zoom=17, children = [dl.TileLayer(), old_polygon, new_polygon, old_point, new_point], style={'width': '900px', 'height': '500px'}, id='map1-graph',), 
        # html.Div(createGeomEditMap('../data/FalklandIsland_010122_020822.csv')),
    ], style={'padding': 5, 'flex': 1}),
    html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure=fig
        ),
        dcc.Graph(
            id='example2-graph',
            figure=pie_fig
        )
    ], style={'padding': 5, 'flex': 0.5}),
], style={'display': 'flex', 'flex-direction': 'row'})

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    # Output("choropleth", "figure"), 
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input("candidate", "value")
    )
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

def display_choropleth(candidate):
    # dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'})
    fig = px.choropleth(
        df2, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 