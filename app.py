import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from pyproj import Transformer

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
    html.H1("Mapping of Pothole Enquiries in Nor
