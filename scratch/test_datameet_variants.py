import requests
import json

urls = {
    "soi": "https://raw.githubusercontent.com/datameet/maps/master/Country/india-soi.geojson",
    "osm": "https://raw.githubusercontent.com/datameet/maps/master/Country/india-osm.geojson"
}

for name, url in urls.items():
    print(f"Testing {name}...")
    try:
        r = requests.get(url, timeout=10)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            features = data.get("features", [])
            print(f"  Features: {len(features)}")
            if features:
                geom = features[0]["geometry"]
                gtype = geom["type"]
                print(f"  Geometry type: {gtype}")
                # Count points
                pts = 0
                coords = geom["coordinates"]
                if gtype == "Polygon":
                    pts = len(coords[0])
                elif gtype == "MultiPolygon":
                    pts = sum(len(poly[0]) for poly in coords)
                print(f"  Total points: {pts}")
    except Exception as e:
        print(f"  Error: {e}")
