{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ae76c69b-6420-4ba8-86f4-b76ef27b92fe",
   "metadata": {},
   "outputs": [],
   "source": [
    "import dash\n",
    "from dash import dcc, html\n",
    "from dash.dependencies import Input, Output\n",
    "import plotly.express as px\n",
    "import pandas as pd\n",
    "from pyproj import Transformer\n",
    "\n",
    "# Your Mapbox access token\n",
    "MAPBOX_ACCESS_TOKEN = \"pk.eyJ1IjoiZGFyZGV2IiwiYSI6ImNsdWNnbTltcDExdmYyam5pazdtOGZ1MGwifQ.IBDBUPNj10UCQ9jMTV-pjA\"\n",
    "px.set_mapbox_access_token(MAPBOX_ACCESS_TOKEN)\n",
    "\n",
    "# Define the Irish Transverse Mercator projection for Ireland\n",
    "utm_proj = 'epsg:29903'  # EPSG code for Irish Transverse Mercator\n",
    "\n",
    "# Define the WGS84 projection\n",
    "wgs84_proj = 'epsg:4326'  # EPSG code for WGS84\n",
    "\n",
    "# Create a transformer object\n",
    "transformer = Transformer.from_crs(utm_proj, wgs84_proj)\n",
    "\n",
    "# Read the CSV Locally\n",
    "input_file = 'Pothole_Enquiries_Current_Year.csv'  # Replace with your input file path\n",
    "df = pd.read_csv(input_file, encoding='ISO-8859-1', on_bad_lines='skip')\n",
    "\n",
    "# Convert easting and northing to latitude and longitude\n",
    "def convert_coordinates(row):\n",
    "    try:\n",
    "        lat, lon = transformer.transform(row['EASTING'], row['NORTHING'])\n",
    "        return pd.Series({'Latitude': lat, 'Longitude': lon})\n",
    "    except Exception as e:\n",
    "        print(f\"Error converting coordinates for row {row.name}: {e}\")\n",
    "        return pd.Series({'Latitude': None, 'Longitude': None})\n",
    "\n",
    "df[['Latitude', 'Longitude']] = df.apply(convert_coordinates, axis=1)\n",
    "df.dropna(subset=['Latitude', 'Longitude'], inplace=True)\n",
    "\n",
    "# Initialize the Dash app\n",
    "app = dash.Dash(__name__)\n",
    "server = app.server\n",
    "\n",
    "# Define the layout of the app\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"Mapping of Pothole Enquiries in Nor\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
