# 🇮🇳 India Geospatial Map - Premium 80th Independence Day Dashboard

An elegant, geospatial-data-driven Python project that celebrates India's 80th Independence Day. It fetches administrative boundary coordinates of India and draws a highly accurate map in slow motion using Python's standard `Turtle` library. The application features a beautiful, dynamic dark-theme dashboard with a low-opacity background image, a continuous tricolour fill, and detailed national symbols.

---

## Features

- **Geospatial Accuracy**: Uses authentic geographic coordinate data (from OpenStreetMap and Survey of India community sources) to draw states, union territories, and islands.
- **80th Independence Day Special Loading Screen**: A custom tricolour-themed startup screen (*Saffron, White, and Green*) that greets users.
- **Slower, Majestic Drawing Animation**: Draws the national boundary first, followed by the tricolour fill, internal state borders, and a final boundary refinement in a slow-motion animation.
- **Tricolour Fill Clipping**: Employs the **Sutherland-Hodgman Polygon Clipping Algorithm** to slice state and national boundaries horizontally into perfect Saffron, White, and Green flag bands, ensuring a continuous tricolour fill.
- **Topological Edge Classification**: Groups boundary edges into:
  - **Outer National Boundary**: Drawn with a bold, crisp white line first (and refreshed on top at the end).
  - **Internal State Boundaries**: Drawn with thin, subtle slate-navy lines.
- **Dashboard Sidebar Panels**:
  - **The Preamble (Top-Right)**: A beautifully typeset card containing the Preamble of the Constitution of India with highlighted key values (*Saffron, White, Green, and Gold*).
  - **Global Index Standing (Top-Left)**: Displays India's international standings in major global indices (Press Freedom, Hunger Index, HDI, Gender Gap, Henley Passport, and CCPI) using the latest 2025/2026 data.
  - **Tricolour & Symbols Significance (Middle-Left)**: Explains the representation of flag colors and the Ashoka Chakra.
  - **India Profile (Bottom-Right)**: Shows core facts (States/UTs count, total area, coastline length, and national animals/birds/flowers).
- **Interactive Info Card (Bottom-Left)**: Interactive point-in-polygon detection lets you left-click on any state or union territory to view its capital name and fun facts in real-time.
- **Exaggerated Lakshadweep & Andaman Islands**: Enhances the visibility and click-interactivity of small island groups (e.g. Lakshadweep's Kavaratti, Agatti, Andrott, Kalpeni, and Minicoy islands) by representing them as visible octagons.
- **State Capitals Layer**: Displays glowing golden dots (`#FFD700`) at the exact coordinates of all state and UT capitals.
- **Precise Ashoka Chakra**: Draws an accurate 24-spoke Navy Blue wheel with a central hub and 24 rim dots at the geographic center of India.
- **Borderless Fullscreen Mode**: The window launches automatically in borderless fullscreen. Press the **`Escape`** key to close/exit the application window safely at any time.
- **Low-Opacity Backdrop**: Automatically downloads, resizes, and blends a patriotic Getty Images background artwork at a subtle **12% opacity** behind the dashboard.
- **Local Caching & PowerShell Fallback**: Coordinates are cached locally. If the Python network stack is blocked, it falls back to PowerShell to download files seamlessly.

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
