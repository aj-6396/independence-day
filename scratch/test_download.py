import requests
import json
import time

def test_url(name, url, headers=None):
    print(f"Testing {name}...")
    start = time.time()
    try:
        r = requests.get(url, timeout=15, headers=headers)
        duration = time.time() - start
        print(f"  Status: {r.status_code}")
        print(f"  Time taken: {duration:.2f}s")
        print(f"  Content length: {len(r.content)} bytes")
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  Valid JSON: Yes")
                print(f"  Features: {len(data.get('features', []))}")
            except Exception as e:
                print(f"  Valid JSON: No ({e})")
    except Exception as e:
        print(f"  Error: {e}")

print("--- Testing ESRI URL ---")
test_url(
    "ESRI Living Atlas",
    "https://livingatlas.esri.in/server/rest/services/IAB2024/India_Administrative_Boundaries_2024/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&f=geojson",
    headers={"User-Agent": "Mozilla/5.0"}
)

print("\n--- Testing Datameet Simplified URL ---")
test_url(
    "Datameet Simplified",
    "https://raw.githubusercontent.com/datameet/maps/master/Country/india-land-simplified.geojson"
)
