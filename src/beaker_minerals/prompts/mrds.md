You have access to a large amount of data extracted from the USGS Mineral Resources Data System (MRDS).

This data is available in `data/combined_commodities_data_latest.csv`. It is a very large file (300MB+) but may be extremely useful as it contains the location of mineral sites around the world. It is probably the most comprehensive database of mineral sites in the world and should be used in conjunction with other data sources like the mine location data from Wikidata. It is more comprehensive than the Wikidata data by a wide margin though!

Here are the columns in the data:
| Column | Description |
|--------|-------------|
| id | Unique identifier for the record |
| record_ids | Related record IDs |
| mineral_site_ids | IDs of mineral sites |
| names | Names of the mineral site |
| type | Type of mineral site |
| rank | Rank/importance of the site |
| country | Country where site is located |
| province | Province/state/region |
| crs | Coordinate reference system |
| centroid_epsg_4326 | Lat/long coordinates in EPSG:4326 |
| wkt | Well-known text geometry |
| commodity | Primary commodity/mineral |
| contained_metal | Amount of contained metal |
| contained_metal_unit | Unit for contained metal |
| tonnage | Total tonnage of deposit |
| tonnage_unit | Unit for tonnage |
| grade | Grade/concentration of mineral |
| grade_unit | Unit for grade |
| top1_deposit_type | Primary deposit type |
| top1_deposit_group | Deposit group classification |
| top1_deposit_environment | Geological environment |
| top1_deposit_classification_confidence | Confidence in classification |
| top1_deposit_classification_source | Source of classification |

> Note that the location of the mineral site is given by the `centroid_epsg_4326` column which is a point e.g. `POINT(123.456 78.910)`. You can use this to plot the location of the mineral site on a map.

You can use code similar to the following to extract the coordinates from the `centroid_epsg_4326` column and plot the location of the mineral site on a map:

```python
def extract_coords(point_str):
    if isinstance(point_str, str):
        # Remove any extra spaces and split the coordinates
        coords = point_str.replace('POINT (', '').replace(')', '').split()
        if len(coords) == 2:
            return float(coords[1]), float(coords[0])  # lat, lon
    return None, None
```    

You can use folium to create a nice colored heat map of the mineral sites (e.g. for Ukraine) with:

```python
import pandas as pd
import folium
from folium import plugins
import numpy as np

# Create a color map for the top commodities
def get_commodity_color(commodity):
    color_map = {
        'Potassium': 'red',
        'Iron': 'blue',
        'Manganese': 'green',
        'Titanium': 'purple',
        'Copper': 'orange',
        'Holmium': 'yellow',
        'Neodymium': 'pink',
        'Praseodymium': 'lightblue',
        'Samarium': 'lightgreen',
        'Lutetium': 'brown'
    }
    return color_map.get(commodity, 'gray')

# Create base map
m = folium.Map(location=[48.3794, 31.1656], zoom_start=6, tiles='cartodb positron')

# Add heatmap layer
heat_data = [[row['lat'], row['lon']] for idx, row in ukraine_sites.iterrows() 
             if pd.notna(row['lat']) and pd.notna(row['lon'])]
plugins.HeatMap(heat_data).add_to(m)

# Create feature groups for each major commodity
commodity_groups = {}
for commodity in ukraine_sites['commodity'].unique():
    commodity_groups[commodity] = folium.FeatureGroup(name=commodity)

# Add points colored by commodity
for idx, row in ukraine_sites.iterrows():
    if pd.notna(row['lat']) and pd.notna(row['lon']):
        popup_text = f"""
        <b>Name:</b> {row['names']}<br>
        <b>Commodity:</b> {row['commodity']}<br>
        <b>Type:</b> {row['type']}<br>
        <b>Province:</b> {row['province']}<br>
        """
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=5,
            popup=popup_text,
            color=get_commodity_color(row['commodity']),
            fill=True,
            fillOpacity=0.7
        ).add_to(commodity_groups[row['commodity']])

# Add all feature groups to map
for group in commodity_groups.values():
    group.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

m
```