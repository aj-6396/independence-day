import json
from collections import defaultdict

f = 'data/india_boundary.geojson'
data = json.load(open(f, encoding='utf-8'))
edge_counts = defaultdict(int)
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

for _, polygons in states_data.items():
    for poly in polygons:
        n = len(poly)
        for i in range(n - 1):
            p1 = (round(poly[i][0], 5), round(poly[i][1], 5))
            p2 = (round(poly[i+1][0], 5), round(poly[i+1][1], 5))
            if p1 == p2:
                continue
            edge = tuple(sorted([p1, p2]))
            edge_counts[edge] += 1

outer = [e for e, c in edge_counts.items() if c == 1]
internal = [e for e, c in edge_counts.items() if c > 1]
print('Outer:', len(outer), 'Internal:', len(internal))
