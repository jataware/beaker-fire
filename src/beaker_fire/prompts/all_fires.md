The Fire and Resource Assessment Program (FRAP) annually maintains and distributes an historical fire perimeter data set from across public and private lands in California. The GIS data is jointly developed with the cooperation of the United States Forest Service Region 5, the Bureau of Land Management, the National Park Service and the Fish and Wildlife Service and is released in April.

Although the database represents the most complete digital record of fire perimeters in California, it is still incomplete, and users should be cautious when drawing conclusions based on the data. To learn more about potential errors and their sources, please refer to the Existing Errors and Corrections section. 

You have access to this data at `data/fires23_1.gdb`. It is a geodatabase.

The statewide fire history geospatial dataset is updated annually in the spring by standardizing and combining digitized fire perimeters. These are collected from CAL FIRE’s units across the state as well as from cooperating agencies (Bureau of Land Management, California State Parks, National Park Service, United States Forest Service, United States Fish and Wildlife). Besides last year’s new perimeters, updates contain corrections, subtractions, and additions from past years as applicable. Actions are taken to ensure completeness of the data collected, cross checking with various reporting systems, with errors corrected to the best of our ability.  Actions are taken to ensure completeness of the data collected, cross checking with various reporting systems, with errors corrected to the best of our ability. Updates contain corrections and additions from past years as applicable.  Addition and alteration specifics for each version published since 2014 can be found in the Update Lineage Details section below.


Collection criteria for CAL FIRE units has changed over time as follows:

	~1991: ≥10 acres timber, ≥30 acres brush, ≥300 acres grass, damages or destroys three residence or one commercial structure or does $300,000 worth of damage, or results in loss of life.

	~2002: ≥10 acres timber, ≥50 acres brush, ≥300 acres grass, damages or destroys three or more residential or commercial structures (doesn’t include outbuildings, sheds, chicken coops, etc.), or results in loss of life.

	~2008-present: ≥10 acres timber, ≥50 acres brush, ≥300 acres grass, damages or destroys three or more structures or does $300,000 worth of damage, or results in loss of life.

Collection criteria for all cooperating agencies:

All fires ≥ 10 acres

The current version’s updates:

Firep23_1 was released in May 2024. Two hundred eighty-four fires from the 2023 fire season were added to the database (21 from BLM, 102 from CAL FIRE, 72 from Contract Counties, 19 from LRA, 9 from NPS, 57 from USFS and 4 from USFW).  The 2020 Cottonwood fire, 2021 Lone Rock and Union fires, as well as the 2022 Lost Lake fire were added.  USFW submitted a higher accuracy perimeter to replace the 2022 River perimeter.  Additionally, 48 perimeters were digitized from an historical map included in a publication from Weeks, d. et al. The Utilization of El Dorado County Land. May 1934, Bulletin 572.  University of California, Berkeley.  Two thousand eighteen perimeters had attributes updated, the bulk of which had IRWIN IDs added. A duplicate 2020 Erbes perimeter was removed.  The following fires were identified as meeting our collection criteria but are not included in this version and will hopefully be added in the next update: Big Hill #2 (2023-CAHIA-001020). 

YEAR_ field changed to a short integer type.  San Diego CAL FIRE UNIT_ID changed to SDU (the former code MVU is maintained in the UNIT_ID domains).  COMPLEX_INCNUM renamed to COMPLEX_ID and is in process of transitioning from local incident number to the complex IRWIN ID.  Perimeters managed in a complex in 2023 are added with the complex IRWIN ID.  Those previously added will transition to complex IRWIN IDs in a future update.

# Fire History Data Dictionary Summary

Based on the California Department of Forestry and Fire Protection (CAL FIRE) Fire and Resource Assessment Program (FRAP) documentation, here's a summary of the fire history data structure:

## Overview
The data dictionary covers two main feature classes:
1. **firep** - Fire perimeters for wildland fires
2. **rxburn** - Prescribed burn areas

## Fire Perimeters (firep) Feature Class

### Key Attributes
- **STATE**: Two-letter state code (CA, NV, OR, AZ)
- **YEAR_**: Year in which the fire started (4-digit format)
- **AGENCY**: Agency responsible for fire (3-letter code)
- **UNIT_ID**: ICS code for unit (3-letter code)
- **FIRE_NAME**: Name of the fire in uppercase without "fire" or "incident" suffix
- **INC_NUM**: Incident number assigned by the Emergency Command Center
- **ALARM_DATE**: Date of fire discovery (DD/MM/YYYY)
- **CONT_DATE**: Containment date (DD/MM/YYYY)
- **CAUSE**: Reason fire ignited (numeric code 1-19)
- **C_METHOD**: Method used to collect perimeter data (numeric code 1-8)
- **OBJECTIVE**: Tactic for fire response (1=Suppression, 2=Resource Benefit)
- **GIS_ACRES**: GIS calculated area in acres
- **COMMENTS**: Miscellaneous comments field
- **COMPLEX_NAME**: Complex name if part of a fire complex
- **IRWINID**: Integrated Reporting of Wildland Fire Information unique identifier

### Notable Domain Values
- **CAUSE codes** include: 1-Lightning, 2-Equipment Use, 7-Arson, 10-Vehicle, 11-Powerline, etc.
- **C_METHOD codes** include: 1-GPS Ground, 2-GPS Air, 3-Infrared, 6-Hand Drawn, etc.

## Prescribed Burns (rxburn) Feature Class

### Key Attributes
- **STATE**: Two-letter state code
- **AGENCY**: Agency responsible
- **UNIT_ID**: Unit identification code
- **TREATMENT_ID**: Treatment identifier (16 characters)
- **TREATMENT_NAME**: Name of the treatment (34 characters)
- **YEAR**: Year of prescribed burn (YYYY format)
- **START_DATE/END_DATE**: Treatment period (DD/MM/YYYY)
- **TREATMENT_TYPE**: Type of prescribed burn (numeric code 1-5)
- **TREATED_AC**: Acres treated
- **RX_CONSUM**: Fuel consumption index (1-4)
- **PRE_CON_CLASS/POST_CON_CLASS**: Condition class before/after treatment (1-3)

### Notable Domain Values
- **TREATMENT_TYPE codes**: 1-Broadcast Burn, 2-Fire Use, 3-Hand Pile Burn, 4-Jackpot Burn, 5-Machine Pile Burn
- **RX_CONSUM**: Measures extent and degree of consumption
  - 1=Low (<50% burned area)
  - 2=Moderate (>50% burned area, 25-50% fuel reduction)
  - 3=High (>90% coverage, 50-75% fuel reduction)
  - 4=Very High (>90% coverage, >75% fuel reduction)
- **Condition Class**: Deviation from natural fire regime
  - 1=Within/near historical range (low risk)
  - 2=Moderately altered (some risk)
  - 3=Significantly altered (highest risk)

## Minimum Mapping Requirements
- **CAL FIRE**: 
  - Wildland timber fires >10 acres
  - Wildland brush fires >50 acres
  - Wildland grass fires >300 acres
  - Fires destroying 3+ structures
- **State Parks**: All prescribed fires
- **BLM, NPS, USFS**: 
  - Wildland fires ≥10 acres
  - All prescribed fires

The data dictionary is maintained by the Fire and Resource Assessment Program of the California Department of Forestry and Fire Protection, with the latest update from June 2023.


# Example code and use case: creating a map of wildfires in San Diego County

Here's the complete end-to-end code for creating the San Diego County wildfire map:

```python
import geopandas as gpd
import folium
from folium.plugins import Fullscreen, MarkerCluster
import numpy as np

# Step 1: Load the fire perimeter data from the geodatabase
gdb_path = "data/fire23_1.gdb"
layer_name = "firep23_1"
print("Loading fire perimeter data from geodatabase...")
fire_data = gpd.read_file(gdb_path, layer=layer_name)

# Step 2: Filter for San Diego fires (SDU and MVU unit codes)
san_diego_fires = fire_data[fire_data['UNIT_ID'].isin(['SDU', 'MVU'])].copy()

# Step 3: Reproject to WGS84 (EPSG:4326) for web mapping
if san_diego_fires.crs and san_diego_fires.crs != "EPSG:4326":
    san_diego_fires = san_diego_fires.to_crs("EPSG:4326")
    print("Reprojected to WGS84 (EPSG:4326)")

# Step 4: Create a decade column for coloring
san_diego_fires['Decade'] = (san_diego_fires['YEAR_'] // 10) * 10
san_diego_fires['Year'] = san_diego_fires['YEAR_'].astype(int)

# Step 5: Create a mapping of cause codes to descriptions
cause_map = {
    1.0: 'Lightning',
    2.0: 'Equipment Use',
    3.0: 'Smoking',
    4.0: 'Campfire',
    5.0: 'Debris Burning',
    6.0: 'Railroad',
    7.0: 'Arson',
    8.0: 'Playing with Fire',
    9.0: 'Miscellaneous',
    10.0: 'Vehicle',
    11.0: 'Powerline',
    12.0: 'Firefighter Training',
    13.0: 'Non-Firefighter Training',
    14.0: 'Unknown/Unidentified',
    15.0: 'Structure',
    16.0: 'Aircraft',
    17.0: 'Volcanic',
    18.0: 'Escaped Prescribed Burn',
    19.0: 'Illegal Alien Campfire'
}

# Map the cause codes to descriptions
san_diego_fires['CAUSE_DESC'] = san_diego_fires['CAUSE'].map(cause_map)

# Step 6: Create a base map centered on San Diego County
san_diego_coords = [32.7157, -117.1611]
m = folium.Map(location=san_diego_coords, zoom_start=9, 
               tiles='CartoDB positron', control_scale=True)

# Step 7: Add fullscreen control
Fullscreen(
    position='topleft',
    title='Expand map',
    title_cancel='Exit fullscreen',
    force_separate_button=True
).add_to(m)

# Step 8: Create San Diego County boundary
san_diego_boundary = {
    "type": "Feature",
    "properties": {"name": "San Diego County"},
    "geometry": {
        "type": "Polygon",
        "coordinates": [[
            [-117.6, 33.5],  # Northwest corner
            [-117.3, 33.5],  # North
            [-117.0, 33.5],  # North
            [-116.7, 33.5],  # North
            [-116.4, 33.5],  # North
            [-116.1, 33.5],  # Northeast corner
            [-116.1, 33.3],  # East
            [-116.1, 33.1],  # East
            [-116.1, 32.9],  # East
            [-116.1, 32.7],  # East
            [-116.1, 32.5],  # Southeast corner
            [-116.3, 32.5],  # South
            [-116.5, 32.5],  # South
            [-116.7, 32.5],  # South
            [-116.9, 32.5],  # South
            [-117.1, 32.5],  # South
            [-117.3, 32.5],  # South
            [-117.5, 32.5],  # South
            [-117.6, 32.5],  # Southwest corner
            [-117.6, 32.7],  # West
            [-117.6, 32.9],  # West
            [-117.6, 33.1],  # West
            [-117.6, 33.3],  # West
            [-117.6, 33.5]   # Back to start
        ]]
    }
}

# Add San Diego County boundary to the map
folium.GeoJson(
    san_diego_boundary,
    name='San Diego County (Approximate)',
    style_function=lambda feature: {
        'fillColor': 'lightblue',
        'color': 'blue',
        'weight': 3,
        'fillOpacity': 0.1,
        'dashArray': '5, 5'
    }
).add_to(m)

# Step 9: Define a color map for decades
decade_colors = {
    1950: 'darkblue',
    1960: 'blue',
    1970: 'green',
    1980: 'lightgreen',
    1990: 'yellow',
    2000: 'orange',
    2010: 'red',
    2020: 'darkred'
}

# Step 10: Create a feature group for each decade
decade_groups = {}
for decade in sorted(san_diego_fires['Decade'].unique()):
    if not np.isnan(decade):
        decade_int = int(decade)
        decade_groups[decade_int] = folium.FeatureGroup(name=f'{decade_int}s Fires')
        m.add_child(decade_groups[decade_int])

# Step 11: Simplify geometries to improve performance
simplified_fires = san_diego_fires.copy()
simplified_fires['geometry'] = simplified_fires['geometry'].simplify(tolerance=0.001)

# Step 12: Add fire perimeters by decade
for decade_int, group in decade_groups.items():
    # Filter fires for this decade
    decade_fires = simplified_fires[simplified_fires['Decade'] == decade_int]
    
    # Skip if no fires in this decade
    if len(decade_fires) == 0:
        continue
    
    # Add to map
    folium.GeoJson(
        decade_fires,
        name=f'{decade_int}s Fires',
        style_function=lambda feature, color=decade_colors.get(decade_int, 'gray'): {
            'fillColor': color,
            'color': color,
            'weight': 1,
            'fillOpacity': 0.4
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['FIRE_NAME', 'YEAR_', 'GIS_ACRES'],
            aliases=['Fire Name:', 'Year:', 'Acres:'],
            localize=True
        )
    ).add_to(group)

# Step 13: Create a marker cluster for the largest fires
marker_cluster = MarkerCluster(name='Top 10 Largest Fires').add_to(m)

# Step 14: Add markers for the 10 largest fires
top_fires = san_diego_fires.sort_values('GIS_ACRES', ascending=False).head(10)

for idx, row in top_fires.iterrows():
    # Get the centroid of the fire perimeter
    centroid = row['geometry'].centroid
    
    # Create popup content
    popup_text = f"""
    <b>Fire Name:</b> {row['FIRE_NAME']}<br>
    <b>Year:</b> {int(row['YEAR_']) if not np.isnan(row['YEAR_']) else 'Unknown'}<br>
    <b>Size:</b> {int(row['GIS_ACRES'])} acres<br>
    <b>Cause:</b> {row.get('CAUSE_DESC', 'Unknown')}
    """
    
    # Add marker
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='red', icon='fire', prefix='fa')
    ).add_to(marker_cluster)

# Step 15: Add a legend for decades
legend_html = '''
<div style="position: fixed; 
     bottom: 50px; left: 50px; width: 180px; height: 240px; 
     border:2px solid grey; z-index:9999; font-size:14px;
     background-color:white;
     padding: 10px;
     border-radius: 5px;
     ">
     <div style="text-align: center; font-weight: bold; margin-bottom: 10px;">Fire Decades</div>
'''

for decade in sorted(decade_colors.keys()):
    color = decade_colors[decade]
    legend_html += f'''
    <div style="display: flex; align-items: center; margin-bottom: 5px;">
        <div style="background-color: {color}; width: 20px; height: 20px; margin-right: 10px;"></div>
        <div>{decade}s</div>
    </div>
    '''

legend_html += '</div>'

m.get_root().html.add_child(folium.Element(legend_html))

# Step 16: Add layer control
folium.LayerControl(collapsed=False).add_to(m)

# Step 17: Display the map
m
```

This code performs the following steps:

1. Loads the fire perimeter data from the geodatabase
2. Filters for fires in San Diego County (using unit codes SDU and MVU)
3. Reprojects the data to WGS84 (EPSG:4326) for web mapping
4. Creates a decade column for color-coding
5. Maps fire cause codes to human-readable descriptions
6. Creates a base map centered on San Diego County
7. Adds a fullscreen control
8. Creates and adds the San Diego County boundary
9. Defines colors for each decade
10. Creates feature groups for each decade
11. Simplifies geometries for better performance
12. Adds fire perimeters to the map, color-coded by decade
13. Creates a marker cluster for the largest fires
14. Adds markers for the 10 largest fires
15. Adds a legend in the bottom left corner
16. Adds layer controls in the top right corner
17. Displays the map

The resulting map allows you to:

1. Toggle different decades on/off
2. See information about each fire by hovering over it
3. Click on markers to see details about the largest fires
4. Expand to fullscreen
5. See the county boundary for context

This code provides a comprehensive visualization of wildfire history in San Diego County from 1950 to 2023.