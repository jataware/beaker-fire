You have access to data from UN Comtrade on exports from Ukraine for 2023. The overall amount of Comtrade data is huge and you need special access to the API so we've provied you with a file-based version of the data.

The file is called `data/Ukraine_Exports_Comtrade_2023.csv`. This data contains exports from Ukraine for 2023 by HS code and country of destination. The `cmdCode` column contains the HS code and the `partnerCode` column contains the country code. The `partnerISO` column contains the ISO code for the country of destination. `qty` and `qtyUnitAbbr` can be used to understand the quantity of the export and the abbreviation for the unit of measure (e.g. 'kg').

When you read in this data you MUST do it like this:

```python
comtrade = pd.read_csv('data/Ukraine_Exports_Comtrade_2023.csv', encoding='cp1252', index_col=False)
```

This ensures that the encoding is correct and you don't improperly parse the index column.

You also have access to a refernce file called `data/HS_Commodity_Codes.csv` which you can use to look up commodity codes and descriptions if you find that helpful.

A good way to visualize this data is to plot the flows using folium. For example, plotting Iron flows can be done like this:

```python
import folium
import numpy as np
from math import radians, sin, cos, atan2, sqrt, degrees

# Load the raw Comtrade data
comtrade = pd.read_csv('data/Ukraine_Exports_Comtrade_2023.csv', encoding='cp1252', index_col=False)

# Define the HS codes for Iron products
iron_codes = ['2601', '7201', '7202', '7203', '7204', '7205']  # Iron ores and various iron products

# Filter for Iron-related exports
iron_exports = comtrade[comtrade['cmdCode'].astype(str).str.startswith(tuple(iron_codes))].copy()

# Group by destination country and sum the values
iron_exports = iron_exports.groupby('partnerDesc')['primaryValue'].sum().reset_index()

# Sort by value (ascending=True so larger flows are drawn first on map)
iron_exports_sorted = iron_exports.sort_values('primaryValue', ascending=True)

def create_curve_points(start, end, curve_factor=0.2, curve_direction=1):
    """Create points for a curved line between two coordinates."""
    # Convert to radians
    start_lat, start_lon = map(radians, start)
    end_lat, end_lon = map(radians, end)
    
    # Calculate midpoint
    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2
    
    # Calculate distance
    d_lon = end_lon - start_lon
    d = sqrt((end_lat - start_lat)**2 + d_lon**2)
    
    # Create perpendicular point for curve
    bearing = atan2(sin(d_lon), cos(start_lat) * sin(end_lat) - 
                   sin(start_lat) * cos(end_lat) * cos(d_lon))
    
    # Perpendicular angle (curve direction determines if curve goes left or right)
    perp_angle = bearing + curve_direction * np.pi/2
    
    # Control point distance
    ctrl_dist = d * curve_factor
    
    # Calculate control point
    ctrl_lat = mid_lat + ctrl_dist * cos(perp_angle)
    ctrl_lon = mid_lon + ctrl_dist * sin(perp_angle)
    
    # Convert back to degrees
    ctrl_point = [np.degrees(ctrl_lat), np.degrees(ctrl_lon)]
    
    # Create points for smooth curve
    t = np.linspace(0, 1, 100)
    points = []
    for ti in t:
        # Quadratic Bezier curve
        lat = (1-ti)**2 * start[0] + 2*(1-ti)*ti * ctrl_point[0] + ti**2 * end[0]
        lon = (1-ti)**2 * start[1] + 2*(1-ti)*ti * ctrl_point[1] + ti**2 * end[1]
        points.append([lat, lon])
    
    # Calculate final direction for arrow using last few points for better accuracy
    final_points = points[-5:]  # Use last 5 points
    dlat = final_points[-1][0] - final_points[0][0]
    dlon = final_points[-1][1] - final_points[0][1]
    final_direction = degrees(atan2(dlon, dlat))
    
    return points, final_direction

# Create base map centered on Ukraine
m = folium.Map(location=[48.3794, 31.1656], zoom_start=4, tiles='cartodb positron')

# Calculate line width scaling
def scale_weight(value):
    # Even more dramatic scaling
    return 2 + 48 * (value / iron_exports['primaryValue'].max()) ** 0.3

# Sort by value to draw larger lines first
iron_exports_sorted = iron_exports.sort_values('primaryValue', ascending=True)

# Add flows
for _, row in iron_exports_sorted.iterrows():
    if row['partnerDesc'] in partner_coords:
        # Get coordinates
        dest_coords = partner_coords[row['partnerDesc']]
        
        # Calculate line weight
        weight = scale_weight(row['primaryValue'])
        
        # Determine curve direction based on destination location
        curve_direction = 1 if dest_coords[1] > ukraine_coords[1] else -1
        
        # Create curved line points
        # Adjust curve_factor based on distance
        dist = sqrt((dest_coords[0] - ukraine_coords[0])**2 + 
                   (dest_coords[1] - ukraine_coords[1])**2)
        curve_factor = 0.5 if dist < 10 else 0.2  # More curve for closer countries
        
        curve_points, final_direction = create_curve_points(
            ukraine_coords, dest_coords, 
            curve_factor, curve_direction
        )
        
        # Add flow line
        folium.PolyLine(
            locations=curve_points,
            weight=weight,
            color='red',
            opacity=0.6,
            popup=f"Iron Exports to {row['partnerDesc']}: ${row['primaryValue']:,.0f}"
        ).add_to(m)
        
        # Add arrow at destination
        folium.RegularPolygonMarker(
            location=dest_coords,
            number_of_sides=3,
            radius=weight/3,  # Make arrows even smaller
            rotation=final_direction - 90,  # Adjust rotation to point along line
            popup=f"{row['partnerDesc']}<br>Iron Exports: ${row['primaryValue']:,.0f}",
            color='red',
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

# Add Ukraine marker last so it's on top
folium.CircleMarker(
    location=ukraine_coords,
    radius=10,
    popup='Ukraine',
    color='black',
    fill=True,
    fill_opacity=0.7
).add_to(m)

# Add a legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; height: 160px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white;
            padding: 10px;
            ">
            <b>Iron Exports from Ukraine</b><br>
            Line thickness proportional to<br>cube root of export value<br><br>
            Example values:<br>
            Thickest (Poland): $796M<br>
            Medium (Austria): $232M<br>
            Thin (Greece): $7.7M
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

m
```

Here is an example of how to plot multiple commodities on the same map using dark mode with a beautiful color scheme and legend:

```python
import pandas as pd
import folium
import numpy as np
from math import radians, sin, cos, atan2, sqrt, degrees

# Load and process the data
comtrade = pd.read_csv('data/Ukraine_Exports_Comtrade_2023.csv', encoding='cp1252', index_col=False)

# Define the HS codes for each mineral
mineral_codes = {
    'Iron': ['2601', '7201', '7202', '7203', '7204', '7205'],
    'Titanium': ['2614', '8108'],
    'Aluminum': ['2606', '7601', '7602', '7603', '7604'],
    'Magnesite': ['2519'],
    'Manganese': ['2602', '8111']
}

# Process data for each mineral
mineral_exports = {}
for mineral, codes in mineral_codes.items():
    mineral_data = comtrade[comtrade['cmdCode'].astype(str).str.startswith(tuple(codes))].copy()
    mineral_data = mineral_data.groupby('partnerDesc')['primaryValue'].sum().reset_index()
    mineral_data = mineral_data[mineral_data['partnerDesc'] != 'World'].copy()
    mineral_data = mineral_data.sort_values('primaryValue', ascending=True)
    mineral_exports[mineral] = mineral_data

# Create a vibrant but harmonious color scheme
color_map = {
    'Iron': '#e63946',      # Rich red
    'Titanium': '#2a9d8f',  # Teal
    'Aluminum': '#457b9d',  # Steel blue
    'Magnesite': '#8338ec', # Purple
    'Manganese': '#f77f00'  # Orange
}

# Dictionary of major trading partner coordinates
partner_coords = {
    'Poland': [52.1283, 21.0038],
    'Slovakia': [48.6690, 19.6990],
    'Austria': [47.5162, 14.5501],
    'China': [35.8617, 104.1954],
    'Bulgaria': [42.7339, 25.4858],
    'Algeria': [36.7372, 3.0863],
    'Romania': [45.9432, 24.9668],
    'Turkey': [38.9637, 35.2433],
    'Italy': [41.8719, 12.5674],
    'Hungary': [47.1625, 19.5033],
    'Germany': [51.1657, 10.4515],
    'Spain': [40.4637, -3.7492],
    'Switzerland': [46.8182, 8.2275],
    'France': [46.2276, 2.2137],
    'Greece': [39.0742, 21.8243],
    'Morocco': [31.7917, -7.0926],
    'Peru': [-9.1900, -75.0152],
    'Netherlands': [52.1326, 5.2913],
    'Lithuania': [55.1694, 23.8813],
    'Serbia': [44.0165, 21.0059],
    'Uzbekistan': [41.3775, 64.5853],
    'Czechia': [49.8175, 15.473],
    'Mexico': [23.6345, -102.5528],
    'Rep. of Moldova': [47.4116, 28.3699],
    'USA': [37.0902, -95.7129],
    'India': [20.5937, 78.9629],
    'Rep. of Korea': [35.9078, 127.7669],
    'Japan': [36.2048, 138.2529],
    'Türkiye': [38.9637, 35.2433]  # Same as Turkey
}

def create_curve_points(start, end, curve_factor=0.2, curve_direction=1):
    """Create points for a curved line between two coordinates."""
    # Convert to radians
    start_lat, start_lon = map(radians, start)
    end_lat, end_lon = map(radians, end)
    
    # Calculate midpoint
    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2
    
    # Calculate distance
    d_lon = end_lon - start_lon
    d = sqrt((end_lat - start_lat)**2 + d_lon**2)
    
    # Create perpendicular point for curve
    bearing = atan2(sin(d_lon), cos(start_lat) * sin(end_lat) - 
                   sin(start_lat) * cos(end_lat) * cos(d_lon))
    
    # Perpendicular angle
    perp_angle = bearing + curve_direction * np.pi/2
    
    # Control point distance
    ctrl_dist = d * curve_factor
    
    # Calculate control point
    ctrl_lat = mid_lat + ctrl_dist * cos(perp_angle)
    ctrl_lon = mid_lon + ctrl_dist * sin(perp_angle)
    
    # Convert back to degrees
    ctrl_point = [np.degrees(ctrl_lat), np.degrees(ctrl_lon)]
    
    # Create points for smooth curve
    t = np.linspace(0, 1, 100)
    points = []
    for ti in t:
        # Quadratic Bezier curve
        lat = (1-ti)**2 * start[0] + 2*(1-ti)*ti * ctrl_point[0] + ti**2 * end[0]
        lon = (1-ti)**2 * start[1] + 2*(1-ti)*ti * ctrl_point[1] + ti**2 * end[1]
        points.append([lat, lon])
    
    # Calculate final direction for arrow
    final_points = points[-5:]  # Use last 5 points
    dlat = final_points[-1][0] - final_points[0][0]
    dlon = final_points[-1][1] - final_points[0][1]
    final_direction = degrees(atan2(dlon, dlat))
    
    return points, final_direction

def offset_coordinates(base_coords, mineral_index, total_minerals, radius_km=50):
    """Create a circle of points around the base coordinates for different minerals"""
    radius_deg = radius_km / 111
    angle = (mineral_index * 2 * np.pi / total_minerals) + np.pi/2
    dx = radius_deg * cos(angle)
    dy = radius_deg * sin(angle)
    return [base_coords[0] + dy, base_coords[1] + dx]

# Create the map
def create_mineral_flow_map(mineral_exports, partner_coords, color_map):
    # Ukraine coordinates
    ukraine_coords = [48.3794, 31.1656]
    
    # Create base map
    m = folium.Map(
        location=ukraine_coords,
        zoom_start=4,
        tiles='cartodbdark_matter'
    )
    
    # Calculate overall maximum value for consistent scaling
    max_value = max(data['primaryValue'].max() for data in mineral_exports.values())
    
    def scale_weight(value, max_val):
        # Scale between 1 and 20 pixels
        return 1 + 19 * (value / max_val) ** 0.3
    
    # Create a feature group for each mineral
    mineral_groups = {
        mineral: folium.FeatureGroup(name=mineral)
        for mineral in mineral_codes.keys()
    }
    
    # Count minerals per country
    country_mineral_count = {}
    for mineral, data in mineral_exports.items():
        for _, row in data.iterrows():
            if row['partnerDesc'] in partner_coords:
                country_mineral_count[row['partnerDesc']] = country_mineral_count.get(row['partnerDesc'], 0) + 1
    
    # Add flows for each mineral
    for mineral_idx, (mineral, data) in enumerate(mineral_exports.items()):
        for _, row in data.iterrows():
            if row['partnerDesc'] in partner_coords:
                base_coords = partner_coords[row['partnerDesc']]
                
                # Only offset if multiple minerals go to this country
                if country_mineral_count[row['partnerDesc']] > 1:
                    dest_coords = offset_coordinates(
                        base_coords, 
                        mineral_idx, 
                        len(mineral_codes),
                        radius_km=25
                    )
                else:
                    dest_coords = base_coords
                
                # Calculate line weight
                weight = scale_weight(row['primaryValue'], max_value)
                
                # Determine curve direction
                curve_direction = 1 if dest_coords[1] > ukraine_coords[1] else -1
                
                # Create curved line points
                dist = sqrt((dest_coords[0] - ukraine_coords[0])**2 + 
                           (dest_coords[1] - ukraine_coords[1])**2)
                curve_factor = 0.5 if dist < 10 else 0.2
                
                curve_points, final_direction = create_curve_points(
                    ukraine_coords, dest_coords, 
                    curve_factor, curve_direction
                )
                
                # Add flow line
                folium.PolyLine(
                    locations=curve_points,
                    weight=weight,
                    color=color_map[mineral],
                    opacity=0.8,
                    popup=f"{mineral} Exports to {row['partnerDesc']}: ${row['primaryValue']:,.0f}"
                ).add_to(mineral_groups[mineral])
                
                # Add destination marker
                folium.CircleMarker(
                    location=dest_coords,
                    radius=weight/4,
                    color=color_map[mineral],
                    fill=True,
                    fill_opacity=0.9,
                    popup=f"{mineral} Exports to {row['partnerDesc']}: ${row['primaryValue']:,.0f}",
                    weight=2
                ).add_to(mineral_groups[mineral])
                
                # Add country marker if multiple minerals
                if country_mineral_count[row['partnerDesc']] > 1:
                    folium.CircleMarker(
                        location=base_coords,
                        radius=2,
                        color='#ffffff',
                        fill=True,
                        fill_opacity=0.5,
                        weight=1,
                        popup=row['partnerDesc']
                    ).add_to(mineral_groups[mineral])
    
    # Add Ukraine marker
    folium.CircleMarker(
        location=ukraine_coords,
        radius=8,
        popup='Ukraine',
        color='#ffffff',
        fill=True,
        fill_opacity=0.8,
        weight=2
    ).add_to(m)
    
    # Add all feature groups to map
    for group in mineral_groups.values():
        group.add_to(m)
    
    # Add layer control
    folium.LayerControl(position='topright').add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="
        position: fixed; 
        bottom: 50px; 
        left: 50px; 
        width: 250px;
        height: auto;
        background-color: rgba(0, 0, 0, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
        padding: 20px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 14px;
        color: white;
        z-index: 9999;
        ">
        <div style="margin-bottom: 15px;"><strong>Ukraine Mineral Exports</strong></div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 30px; height: 3px; background: #e63946; margin-right: 10px;"></div>
            <span>Iron ($2.59B)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 30px; height: 3px; background: #2a9d8f; margin-right: 10px;"></div>
            <span>Titanium ($84.2M)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 30px; height: 3px; background: #457b9d; margin-right: 10px;"></div>
            <span>Aluminum ($74.6M)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 30px; height: 3px; background: #8338ec; margin-right: 10px;"></div>
            <span>Magnesite ($442K)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 8px 0;">
            <div style="width: 30px; height: 3px; background: #f77f00; margin-right: 10px;"></div>
            <span>Manganese ($63K)</span>
        </div>
        <div style="margin-top: 15px; font-size: 12px; color: rgba(255, 255, 255, 0.7);">
            Line thickness proportional to export value<br>
            Click lines for detailed values
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m

# Create and display the map
m = create_mineral_flow_map(mineral_exports, partner_coords, color_map)
m
```