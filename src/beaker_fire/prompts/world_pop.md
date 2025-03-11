You have access to WorldPop data for the United States for 2020. It is available at `data/worldpop/usa_ppp_2020_constrained.tif`. This is a huge file! So in lieu of using this, you should use the `data/worldpop/socal_population_2020_5km.tif` file, which is a 5km x 5km grid of the population of California in 2020. This is a derived dataset perfect for use for wildfire analysis in Southern California.

# Original description of the WorldPop data

Estimated total number of people per grid-cell. The dataset is available to download in Geotiff format at a resolution of 3 arc (approximately 100m at the equator). The projection is Geographic Coordinate System, WGS84. The units are number of people per pixel. "NoData" values represent areas that were mapped as unsettled based on the outputs of the Built-Settlement Growth Model (BSGM) developed by Jeremiah J.Nieves et al. 2020.

The mapping approach is the Random Forests-based dasymetric redistribution developed by Stevens et al. (2015). The disaggregation was done by Maksym Bondarenko (WorldPop) and David Kerr (WorldPop), using the Random Forests population modelling R scripts (Bondarenko et al., 2020), with oversight from Alessandro Sorichetta (WorldPop).

SOURCE DATA:

This dataset was produced based on the 2020 population census/projection-based estimates for 2020 (information and sources of the input population data can be found here).
Built-Settlement Growth Model (BSGM) outputs produced by Jeremiah J.Nieves et al. 2020.
Geospatial covariates representing factors related to population distribution, were obtained from the "Global High Resolution Population Denominators Project" (OPP1134076).

This data may be useful for plotting gridded population maps (e.g. visualizing population across California).

# Example code and use case: creating a map of population of Southern California

The following code will plot a gridded heat map of the population of Southern California with layers for regular and logarithmic population scales. Logarithmic scale is useful for visualizing population differences in areas with low and high population densities.

```python
import folium
from folium.plugins import Fullscreen
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
import requests
import json
from pyproj import CRS, Transformer

# Load the Southern California population data
population_file = "data/worldpop/socal_population_2020_5km.tif"

# Open the raster file and prepare data for folium
with rasterio.open(population_file) as src:
    # Read the data
    population = src.read(1)  # Read the first band
    
    # Get the source CRS and transform to WGS84 (EPSG:4326) which is what web maps use
    src_crs = src.crs
    dst_crs = CRS.from_epsg(4326)
    
    # Create a transformer for coordinate conversion
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    
    # Get the bounds in the destination CRS (WGS84)
    west, south, east, north = transform_bounds(src_crs, dst_crs, 
                                              src.bounds.left, src.bounds.bottom, 
                                              src.bounds.right, src.bounds.top)
    
    # Calculate the center for the map
    center_lat = (south + north) / 2
    center_lon = (west + east) / 2
    
    # Create a folium map centered on the data
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='CartoDB positron'
    )
    
    # Add fullscreen control
    Fullscreen(
        position='topleft',
        title='Expand map',
        title_cancel='Exit fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Define Southern California counties
    socal_counties = [
        'Los Angeles', 'Orange', 'San Diego', 'Riverside', 
        'San Bernardino', 'Ventura', 'Imperial', 'Santa Barbara'
    ]
    
    # Try to add Southern California county boundaries
    try:
        # Use a GeoJSON of California counties
        url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Load the GeoJSON data
            counties = json.loads(response.content)
            
            # Filter to SoCal counties
            socal_features = []
            for feature in counties['features']:
                if feature['properties']['name'] in socal_counties:
                    socal_features.append(feature)
            
            socal_geojson = {"type": "FeatureCollection", "features": socal_features}
            
            # Create a feature group for county boundaries so it can be controlled in layer control
            county_layer = folium.FeatureGroup(name='County Boundaries')
            
            # Add county boundaries to the layer
            folium.GeoJson(
                socal_geojson,
                style_function=lambda feature: {
                    'fillColor': 'transparent',
                    'color': 'black',
                    'weight': 1,
                    'dashArray': '5, 5',
                    'fillOpacity': 0
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=['name'],
                    aliases=['County:'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )
            ).add_to(county_layer)
            
            # Add the county layer to the map
            county_layer.add_to(m)
            
    except Exception as e:
        print(f"Could not add county boundaries: {e}")
    
    # Color schemes - Viridis is a good perceptually uniform colormap for population data
    viridis_colors = [
        '#440154', '#481567', '#482677', '#453781', '#404788', 
        '#39568C', '#33638D', '#2D708E', '#287D8E', '#238A8D', 
        '#1F968B', '#20A387', '#29AF7F', '#3CBB75', '#55C667', 
        '#73D055', '#95D840', '#B8DE29', '#DCE319', '#FDE725'
    ]
    
    # Find the max value for normalization
    max_val = np.max(population)
    log_population = np.log1p(population)
    max_log_val = np.max(log_population)
    
    # Create two separate feature groups for regular and log scale
    regular_layer = folium.FeatureGroup(name="Regular Population Scale")
    log_layer = folium.FeatureGroup(name="Logarithmic Population Scale")
    
    # Use proper georeferencing to create grid cells
    height, width = population.shape
    
    # Process each cell
    for row in range(height):
        for col in range(width):
            val = population[row, col]
            if val > 0:  # Only add cells with population
                # Get the four corners of the grid cell in the source CRS
                ul_x, ul_y = src.transform * (col, row)  # Upper left
                lr_x, lr_y = src.transform * (col + 1, row + 1)  # Lower right
                
                # Transform to WGS84
                ul_lon, ul_lat = transformer.transform(ul_x, ul_y)
                lr_lon, lr_lat = transformer.transform(lr_x, lr_y)
                
                # Regular scale cell
                norm_val = min(int(val / max_val * 19), 19)  # Map to 0-19 index range
                color = viridis_colors[norm_val]
                
                folium.Rectangle(
                    bounds=[[ul_lat, ul_lon], [lr_lat, lr_lon]],
                    color=None,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    tooltip=f"Population: {val:.0f}"
                ).add_to(regular_layer)
                
                # Log scale cell
                log_val = np.log1p(val)
                log_norm_val = min(int(log_val / max_log_val * 19), 19)
                log_color = viridis_colors[log_norm_val]
                
                folium.Rectangle(
                    bounds=[[ul_lat, ul_lon], [lr_lat, lr_lon]],
                    color=None,
                    fill=True,
                    fill_color=log_color,
                    fill_opacity=0.7,
                    tooltip=f"Population: {val:.0f} (Log: {log_val:.2f})"
                ).add_to(log_layer)
    
    # First add base layers (they'll be ON by default)
    county_layer.add_to(m)
    regular_layer.add_to(m)
    
    # Now add the log layer (will be available but initially OFF)
    # Need to use overlay=True to ensure it appears in the layer control
    m.add_child(log_layer)
    
    # Add layer control AFTER all layers have been added
    folium.LayerControl(position='topright').add_to(m)
    
    # Add a title
    title_html = '''
    <div style="position: fixed; 
        top: 10px; left: 50%; transform: translateX(-50%);
        z-index: 9999; font-size: 18px; font-weight: bold;
        background-color: white; padding: 10px; border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.3);">
        Southern California Population Density (2020)
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Add a legend for viridis color scheme
    legend_html = '''
    <div style="position: fixed; 
        bottom: 50px; right: 50px; 
        z-index: 9999; font-size: 14px;
        background-color: white; padding: 10px; border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.3);">
        <div style="text-align: center; font-weight: bold; margin-bottom: 5px;">Population Density</div>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="background: linear-gradient(to right, 
                #440154, #481567, #482677, #453781, #404788, 
                #39568C, #33638D, #2D708E, #287D8E, #238A8D, 
                #1F968B, #20A387, #29AF7F, #3CBB75, #55C667, 
                #73D055, #95D840, #B8DE29, #DCE319, #FDE725); 
                width: 150px; height: 20px; margin-right: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; width: 150px;">
            <span>Low</span>
            <span>High</span>
        </div>
        <div style="font-size: 12px; margin-top: 5px;">
            Data source: WorldPop 2020<br>
            Toggle layers using control panel →
        </div>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display the map
m
```