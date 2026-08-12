import json
from collections import defaultdict

data = json.load(open('data/india_boundary.geojson', encoding='utf-8'))
features = data.get('features', [])
states_data = {}

for feat in features:
    properties = feat.get('properties', {})
    state_name = properties.get('ST_NM', 'Unknown')
    geom = feat.get('geometry')
    if not geom:
        continue
    gtype = geom.get('type')
    coords = geom.get('coordinates')
    polygons = []
    if gtype == 'Polygon':
        polygons.append(coords[0])
    elif gtype == 'MultiPolygon':
        for poly in coords:
            polygons.append(poly[0])
    if polygons:
        if state_name not in states_data:
            states_data[state_name] = []
        states_data[state_name].extend(polygons)

# Simulate MapProjection
longitudes = []
latitudes = []
for state_name, polygons in states_data.items():
    for poly in polygons:
        for lon, lat in poly:
            longitudes.append(lon)
            latitudes.append(lat)

min_lon, max_lon = min(longitudes), max(longitudes)
min_lat, max_lat = min(latitudes), max(latitudes)

width, height, padding = 1920, 1080, 145
drawable_w = width - 2 * padding
drawable_h = height - 2 * padding
lon_range = max_lon - min_lon
lat_range = max_lat - min_lat
scale = min(drawable_w / lon_range, drawable_h / lat_range)
map_w = lon_range * scale
map_h = lat_range * scale
offset_x = -map_w / 2
offset_y = -map_h / 2 + 30

def project(lon, lat):
    x = (lon - min_lon) * scale + offset_x
    y = (lat - min_lat) * scale + offset_y
    return x, y

lak_coords = states_data['Lakshadweep'][0]
projected = [project(lon, lat) for lon, lat in lak_coords]
print('Lakshadweep projected coordinates:', projected)
print('Min/Max Lon:', min_lon, max_lon, 'Min/Max Lat:', min_lat, max_lat)
print('Scale:', scale, 'Map size:', map_w, map_h)
