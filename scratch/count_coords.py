import requests
import json

url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
r = requests.get(url)
data = r.json()

total_polygons = 0
total_points = 0

for feat in data['features']:
    geom = feat['geometry']
    gtype = geom['type']
    coords = geom['coordinates']
    
    if gtype == 'Polygon':
        total_polygons += 1
        total_points += len(coords[0])
    elif gtype == 'MultiPolygon':
        for poly in coords:
            total_polygons += 1
            total_points += len(poly[0])

print(f"Total Polygons: {total_polygons}")
print(f"Total Points: {total_points}")
