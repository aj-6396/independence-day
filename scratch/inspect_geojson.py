import requests
import json

url = 'https://raw.githubusercontent.com/datameet/maps/master/Country/india-land-simplified.geojson'
r = requests.get(url, timeout=15)
data = r.json()
feature = data['features'][0]
geom = feature['geometry']
gtype = geom['type']
print("Geometry Type:", gtype)

coords = geom['coordinates']
print("Coordinates depth structure:")
if gtype == "Polygon":
    print(f"Number of rings: {len(coords)}")
    print(f"Number of points in exterior ring: {len(coords[0])}")
    print(f"Sample points: {coords[0][:5]}")
elif gtype == "MultiPolygon":
    print(f"Number of Polygons: {len(coords)}")
    for idx, poly in enumerate(coords):
        print(f"  Polygon {idx}: {len(poly)} rings, exterior ring has {len(poly[0])} points")
        print(f"  Sample points of exterior ring: {poly[0][:3]}")
