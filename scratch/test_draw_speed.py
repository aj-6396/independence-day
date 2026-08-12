import requests
import json
import time

print("Downloading GeoJSON...")
url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
data = requests.get(url).json()

print("Parsing features...")
polygons = []
for feat in data['features']:
    geom = feat['geometry']
    gtype = geom['type']
    coords = geom['coordinates']
    if gtype == 'Polygon':
        polygons.append(coords[0])
    elif gtype == 'MultiPolygon':
        for poly in coords:
            polygons.append(poly[0])

print(f"Extracted {len(polygons)} polygons.")

# Simulating drawing in turtle (calling mock functions or timing the math)
# Since turtle.tracer(0, 0) disables drawing rendering, the only time spent
# is calling goto(), pendown(), penup(), begin_fill(), end_fill()
# Let's time how long the python loops take for all polygons.
start_time = time.time()
points_count = sum(len(p) for p in polygons)
print(f"Simulating drawing {points_count} points...")

# Just simulating loop overhead
for poly in polygons:
    p0 = poly[0]
    for pt in poly[1:]:
        x, y = pt[0], pt[1] # Projection math
        _ = x * 2.0 + 10.0 # Some mock calculation
    # End of polygon fill simulation

duration = time.time() - start_time
print(f"Simulation completed in {duration:.4f} seconds.")
