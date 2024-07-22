import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pyproj import Transformer

# Set the PROJ_LIB environment variable to point to the location of the PROJ data files
os.environ['PROJ_LIB'] = '/app/.apt/usr/share/proj'

# Your Mapbox access token
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGFyZGV2IiwiYSI6ImNsdWNnbTltcDExdmYyam5pazdtOGZ1MGwifQ.IBDBUPNj10UCQ9jMTV-pjA"
px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)

# Define the Irish Transverse Mercator projection for Ireland
utm_proj = 'epsg:29903'  # EPSG code for Irish Transverse Mercator

# Define the WGS84 projection
wgs84_proj = 'epsg:4326'  # EPSG code for WGS84

# Create a transformer object
transformer = Transformer.from_crs(utm_proj, wgs84_proj)

# Read the CSV Locally
input_file = 'Pothole_Enquiries_Current_Year.csv'  # Replace with your input file path
df = pd.read_csv(input_file, encoding='ISO-8859-1', on_bad_lines='skip')

# Convert easting and northing to latitude and longitude
def convert_coordinates(row):
    try:
        lat, lon = transformer.transform(row['EASTING'], row['NORTHING'])
        return pd.Series({'Latitude': lat, 'Longitude': lon})
    except Exception as e:
        print(f"Error converting coordinates for row {row.name}: {e}")
        return pd.Series({'Latitude': None, 'Longitude': None})

df[['Latitude', 'Longitude']] = df.apply(convert_coordinates, axis=1)
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Mapping of Pothole Enquiries in Northern Ireland", style={'font-family': 'Roboto', 'font-weight': '500', 'textAlign': 'center'}),
    dcc.Graph(id="map", style={'height': '90vh'}),
    dcc.Graph(id="heatmap", style={'height': '90vh'})
], style={'padding': '20px', 'backgroundColor': '#f0f0f0', 'font-family': 'Roboto', 'margin': '0 auto', 'width': '90%'})


# Callback to update the map and heatmap
@app.callback(
    [Output('map', 'figure'),
     Output('heatmap', 'figure')],
    Input('map', 'id')
)
def update_maps(_):
    scatter_map = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", zoom=7.4, mapbox_style="mapbox://styles/mapbox/satellite-streets-v12")
    scatter_map.update_layout(mapbox_center={"lat": 54.637039, "lon": -6.627607}, margin={"r":0, "t":0, "l":0, "b":0}, autosize=True)
    
    heatmap = px.density_mapbox(df, lat="Latitude", lon="Longitude", radius=10, center={"lat": 54.637039, "lon": -6.627607},
                                zoom=7.4, mapbox_style="mapbox://styles/mapbox/satellite-streets-v12")
    heatmap.update_layout(margin={"r":0, "t":0, "l":0, "b":0}, autosize=True)
    
    return scatter_map, heatmap

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
