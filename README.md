# 🇮🇳 India Geospatial Map - Interactive Turtle Animation

An elegant, geospatial-data-driven Python project that downloads official administrative boundary coordinates of India and draws a highly accurate map using Python's standard `Turtle` library. The map features a beautiful dark-mode theme, a continuous flag tricolour fill, and a detailed Ashoka Chakra.

![Mockup of Map Output](https://images.unsplash.com/photo-1532375811409-eb464879b244?auto=format&fit=crop&w=1200&q=80)

## Features

- **Geospatial Accuracy**: Uses authentic geographic coordinate data (from the Survey of India and OpenStreetMap community) rather than basic sketches, resulting in a highly accurate shape.
- **Tricolour Fill Clipping**: Employs the **Sutherland-Hodgman Polygon Clipping Algorithm** to slice state and national boundaries horizontally into perfect Saffron, White, and Green bands, ensuring a clean and continuous tricolour fill across the map.
- **Topological Edge Classification**: Automatically classifies boundary edges:
  - **Outer National Boundary**: Drawn with a bold, crisp white line.
  - **Internal State Boundaries**: Drawn with thin, subtle navy-gray lines to show administrative divisions without cluttering the map.
- **State-by-State Animation**: Renders each state and union territory dynamically from North to South, updating a status bar at the bottom in real-time.
- **Interactive Info Card**: Click on any state or union territory in the window, and a custom-designed details panel in the bottom-left corner displays its Name, Capital, and a fun historical or geographical fact in real-time!
- **State Capitals Layer**: Displays glowing golden dots (`#FFD700`) at the exact geospatial locations of all state and union territory capitals.
- **Compass Rose**: Draws a detailed classical navigation compass rose in the top-right corner, enhancing the premium cartographic look of the map.
- **Precise Ashoka Chakra**: Draw an accurate 24-spoke Navy Blue wheel with central hub and 24 rim dots at the geographic center of India (Madhya Pradesh).
- **Responsive Layout**: Scales and centers coordinates automatically using an aspect-ratio-locked Equirectangular map projection.
- **Local Caching & Self-Healing Downloader**: Cache coordinates locally. If the standard Python network downloader fails due to local DNS blocks (e.g. for GitHub Gists), the script automatically falls back to Windows PowerShell's native network stack to download the file.

---

## Code Overview

1. **`MapProjection`**: Translates geodetic coordinates (longitude/latitude) into pixel coordinates `(x, y)` relative to a centered bounding box.
2. **`clip_polygon_horizontal`**: Performs linear polygon splitting. Given a horizontal boundary coordinate, it reconstructs a closed polygon segment matching the flag band constraints.
3. **`classify_edges`**: Creates a hash-map of all polygon coordinates and identifies edges appearing exactly once (outer national border) or twice (internal state boundaries).
4. **`draw_ashoka_chakra`**: Calculates radial spoke positions using trigonometric equations (`cos`, `sin`) to draw 24 navy blue spokes, a circular hub, and 24 decorative rim dots.
5. **`is_point_in_polygon`**: Implements a ray-casting (Jordan curve) algorithm to detect if mouse clicks fall inside a state's projected polygon borders.

---

## Setup Instructions

### 1. Prerequisites
Make sure you have **Python 3.8+** installed on your system. Python's standard installation includes Tkinter and Turtle graphics.

### 2. Install Dependencies
This project uses the `requests` package to fetch the GeoJSON file. Run:
```bash
pip install -r requirements.txt
```

### 3. Run the Project
Launch the animation:
```bash
python main.py
```

---

## Controls
- **Mouse Click**: Left-click on any state or union territory to view its capital and fun trivia in the bottom-left Info Card.
- **Exit**: Close the Turtle graphics window once the drawing is completed to exit the program.

## Data Attribution
The underlying state-level coordinates are sourced from the open-source community GIS maps of India (DataMeet/Survey of India variants).
