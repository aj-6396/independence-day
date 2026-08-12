import requests
import json

# Testing with exact punctuations and hyphen
url = 'https://archive.org/metadata/VandeMataramSong-R.N.TagoreToA.R.Rehman-54Songs'
try:
    r = requests.get(url, timeout=15)
    data = r.json()
    print("Keys in response:", list(data.keys()))
    
    files = data.get("files", [])
    print(f"Total files: {len(files)}")
    
    mp3_files = [f for f in files if f.get("name", "").endswith(".mp3")]
    print(f"MP3 files count: {len(mp3_files)}")
    
    # Print first 20 files
    for idx, f in enumerate(mp3_files[:25]):
        print(f"{idx+1}. Name: {f['name']}, Size: {f.get('size')} bytes")
except Exception as e:
    print("Error:", e)
