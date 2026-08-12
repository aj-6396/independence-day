import requests
import json
from collections import defaultdict

url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
data = requests.get(url).json()

# Parse features
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

# Collect all edges
edge_counts = defaultdict(int)

def round_pt(pt):
    # Round to 5 decimal places to avoid floating point precision differences
    return (round(pt[0], 5), round(pt[1], 5))

for poly in polygons:
    n = len(poly)
    for i in range(n):
        p1 = round_pt(poly[i])
        p2 = round_pt(poly[(i + 1) % n])
        
        # Skip degenerate edges
        if p1 == p2:
            continue
            
        edge = tuple(sorted([p1, p2]))
        edge_counts[edge] += 1

outer_edges = [edge for edge, count in edge_counts.items() if count == 1]
internal_edges = [edge for edge, count in edge_counts.items() if count > 1]

print(f"Total polygons: {len(polygons)}")
print(f"Total unique edges: {len(edge_counts)}")
print(f"Outer edges (count=1): {len(outer_edges)}")
print(f"Internal edges (count>1): {len(internal_edges)}")
