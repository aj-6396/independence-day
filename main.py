import json
import math
import os
import time
import turtle
import requests
import subprocess
import atexit
from collections import defaultdict

# ============================================================
# 🇮🇳 INDIA GEOSPATIAL MAP — INTERACTIVE TURTLE ANIMATION
# Premium 80th Independence Day Map with Tricolour Fill,
# State Capitals, Clickable Interactive Card,
# and Native Windows Background Music
# ============================================================

# ------------------------------------------------------------
# CONFIGURATION & THEME
# ------------------------------------------------------------
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 850

DATA_DIR = "data"
GEOJSON_FILE = os.path.join(DATA_DIR, "india_boundary.geojson")
MUSIC_FILE = os.path.join(DATA_DIR, "bg_music.mp3")

# Curated, highly reliable 36-state/UT simplified boundary file (approx. 1 MB)
GEOJSON_URL = (
    "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112"
    "/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
)

# Colors - Modern Premium Dark Mode
BG_COLOR = "#0B0D17"         # Deep night blue space
SAFFRON = "#FF9933"          # Vibrant Indian saffron
WHITE = "#FFFFFF"            # Clean white
GREEN = "#138808"            # Vibrant Indian green
CHAKRA_BLUE = "#002F6C"      # Navy blue
STATE_BORDER = "#1E253A"     # Subtle slate navy
NATIONAL_BORDER = "#FFFFFF"  # Bold white for contrast
TEXT_COLOR = "#E2E8F0"       # Light gray-white text
TEXT_MUTED = "#94A3B8"       # Muted gray text
GOLD_COLOR = "#FFD700"       # Gold for capitals & compass
CARD_BG = "#131930"          # Deep blue-navy for info card
CARD_BORDER = "#2E3A5F"      # Slate border for info card

# State/UT Capital Names, Coordinates, and Facts database
STATE_DETAILS = {
    "Andhra Pradesh": ("Amaravati", 80.5135, 16.5417, "Known for the historic Tirupati Temple and its long coastal trade heritage."),
    "Arunachal Pradesh": ("Itanagar", 93.6053, 27.0844, "The Land of the Rising Sun, home to the largest monastery in India (Tawang)."),
    "Assam": ("Dispur", 91.7898, 26.1433, "Famous globally for Assam tea, exquisite silk, and the Kaziranga one-horned rhinos."),
    "Bihar": ("Patna", 85.1376, 25.5941, "The birthplace of Buddhism and Jainism, home to Nalanda, the world's oldest university."),
    "Chhattisgarh": ("Raipur", 81.6296, 21.2514, "Known as the Rice Bowl of India, famous for its rich waterfalls, forests, and temples."),
    "Goa": ("Panaji", 73.8182, 15.4909, "India's smallest state, globally renowned for its scenic beaches and Portuguese heritage."),
    "Gujarat": ("Gandhinagar", 72.6369, 23.2156, "Home to the Asiatic Lions of Gir, Mahatma Gandhi's Ashram, and the Statue of Unity."),
    "Haryana": ("Chandigarh", 76.7794, 30.7333, "Rich in agriculture, sports champions, and the historical battlefield of Kurukshetra."),
    "Himachal Pradesh": ("Shimla", 77.1734, 31.1048, "Nestled in the Himalayas, famous for apple orchards and the Toy Train heritage."),
    "Jharkhand": ("Ranchi", 85.3096, 23.3441, "Rich in minerals, forests, and waterfalls. Home to the sacred Baidyanath Temple."),
    "Karnataka": ("Bengaluru", 77.5946, 12.9716, "The Silicon Valley of India, famous for Hoysala architecture and Mysore Palace."),
    "Kerala": ("Thiruvananthapuram", 76.9366, 8.5241, "God's Own Country, famous for its backwaters, spices, and high quality of life."),
    "Madhya Pradesh": ("Bhopal", 77.4126, 23.2599, "The Heart of India, famous for Tiger Reserves and Khajuraho's ancient carvings."),
    "Maharashtra": ("Mumbai", 72.8777, 19.0760, "India's financial capital, home to Bollywood and the UNESCO Ajanta-Ellora caves."),
    "Manipur": ("Imphal", 93.9368, 24.8170, "Home to the unique floating islands (phumdis) of Loktak Lake and traditional dance."),
    "Meghalaya": ("Shillong", 91.8833, 25.5788, "The Abode of Clouds, home to the living root bridges and Mawsynram (wettest place)."),
    "Mizoram": ("Aizawl", 92.7176, 23.7307, "A land of evergreen hills, bamboo culture, and high literacy."),
    "Nagaland": ("Kohima", 94.1086, 25.6751, "Famous for its diverse indigenous tribes and the spectacular Hornbill Festival."),
    "Odisha": ("Bhubaneswar", 85.8245, 20.2961, "Famous for the classical Odissi dance, Puri Jagannath Yatra, and Chilika Lake."),
    "Punjab": ("Chandigarh", 76.7794, 30.7333, "The Land of Five Rivers, famous for Bhangra, agriculture, and the Golden Temple."),
    "Rajasthan": ("Jaipur", 75.7873, 26.9124, "The Land of Kings, famous for the Thar Desert, royal palaces, and grand forts."),
    "Sikkim": ("Gangtok", 88.6138, 27.3389, "India's first fully organic state, home to Kangchenjunga, the 3rd highest peak."),
    "Tamil Nadu": ("Chennai", 80.2707, 13.0827, "Center of Dravidian culture, famous for grand stone temples and Bharatanatyam dance."),
    "Telangana": ("Hyderabad", 78.4867, 17.3850, "Famous for Charminar monument, Nizami Biryani, and modern technology hubs."),
    "Tripura": ("Agartala", 91.2868, 23.8315, "Known for Neermahal water palace and the rock carvings of Unakoti."),
    "Uttar Pradesh": ("Lucknow", 80.9462, 26.8467, "India's most populous state, home to the Taj Mahal and ancient city of Varanasi."),
    "Uttarakhand": ("Dehradun", 78.0322, 30.3165, "The Land of Gods, famous for the Char Dham pilgrimage and yoga capitals."),
    "West Bengal": ("Kolkata", 88.3639, 22.5726, "The cultural hub of India, home to Nobel laureates and the Sundarbans mangrove forest."),
    "Andaman & Nicobar": ("Port Blair", 92.7265, 11.6234, "Breathtaking tropical archipelago, famous for the historical Cellular Jail."),
    "Chandigarh": ("Chandigarh", 76.7794, 30.7333, "A beautifully planned union territory, designed by architect Le Corbusier."),
    "Dadra and Nagar Haveli and Daman and Diu": ("Daman", 72.8397, 20.3974, "Scenic union territory combining rich Portuguese history and sandy beaches."),
    "Delhi": ("New Delhi", 77.2090, 28.6139, "The capital territory of India, blending ancient history with cosmopolitan life."),
    "Jammu & Kashmir": ("Srinagar", 74.7973, 34.0837, "Paradise on Earth, famous for snow peaks, houseboats, and saffron fields."),
    "Ladakh": ("Leh", 77.5771, 34.1526, "High-altitude desert known for Buddhist monasteries and dramatic mountain passes."),
    "Lakshadweep": ("Kavaratti", 72.6417, 10.5667, "A gorgeous archipelago of coral atolls, offering pristine marine ecosystems."),
    "Puducherry": ("Puducherry", 79.8083, 11.9416, "A seaside town with charming French colonial quarters and the Auroville commune.")
}

# Global dictionary to cache projected state coordinates for interactive click detection
projected_states = {}

# ------------------------------------------------------------
# INITIAL TURTLE SETUP (Show loading screen)
# ------------------------------------------------------------
screen = turtle.Screen()
screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

# Enable borderless fullscreen mode
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
root.attributes('-fullscreen', True)

# Bind Escape key to close/exit the application
screen.listen()
screen.onkey(screen.bye, "Escape")

screen.title("India Interactive Map - Geospatial Animation")
screen.bgcolor(BG_COLOR)
screen.tracer(0, 0)

# Setup loading pen
loading_pen = turtle.Turtle(visible=False)
loading_pen.penup()

# Tricolour-themed 80th Independence Day Loading Screen
loading_pen.goto(0, 80)
loading_pen.color(SAFFRON)
loading_pen.write("80th INDEPENDENCE DAY SPECIAL", align="center", font=("Arial", 22, "bold"))

loading_pen.goto(0, 20)
loading_pen.color(WHITE)
loading_pen.write("INDIA INTERACTIVE MAP", align="center", font=("Arial", 28, "bold"))

loading_pen.goto(0, -30)
loading_pen.color(GREEN)
loading_pen.write("Loading geospatial coordinates...", align="center", font=("Arial", 13, "normal"))

screen.update()

# Setup interactive info panel pen
panel_pen = turtle.Turtle(visible=False)
panel_pen.speed(0)

# ------------------------------------------------------------
# DOWNLOAD & CACHE GEOJSON
# ------------------------------------------------------------
def download_boundary():
    """
    Download India states boundary GeoJSON and save locally.
    Supports fallback to PowerShell if Python requests fails due to DNS issues.
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(GEOJSON_FILE):
        try:
            with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
                json.load(file)
            print("[OK] Valid India boundary file found in local cache.")
            return
        except (json.JSONDecodeError, UnicodeDecodeError):
            print("[Warning] Cached GeoJSON is corrupted. Redownloading...")
            os.remove(GEOJSON_FILE)

    print("Downloading India boundary coordinates...")
    
    # 1. Try Python requests
    try:
        print("Attempting download via Python requests...")
        response = requests.get(GEOJSON_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Validate basic GeoJSON structure
        if "features" not in data or not data["features"]:
            raise ValueError("Invalid GeoJSON structure.")

        with open(GEOJSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print("[OK] India boundary downloaded successfully via Python requests.")
        return
    except Exception as error:
        print(f"[Warning] Python requests download failed: {error}")
        print("Attempting fallback download via Windows PowerShell...")

    # 2. Try PowerShell fallback (for DNS/proxy compatibility on Windows)
    try:
        cmd = [
            "powershell", 
            "-Command", 
            f"Invoke-WebRequest -Uri '{GEOJSON_URL}' -OutFile '{GEOJSON_FILE}'"
        ]
        # Run PowerShell command silently
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Verify the downloaded file is valid JSON
        with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
            json.load(file)
            
        print("[OK] India boundary downloaded successfully via PowerShell fallback.")
    except Exception as error:
        print(f"[Error] All download methods failed: {error}")
        loading_pen.goto(0, -50)
        loading_pen.color("#EF4444")
        loading_pen.write("Download failed. Please check your internet connection.", align="center", font=("Arial", 12, "bold"))
        screen.update()
        raise

# ------------------------------------------------------------
# NATIVE WINDOWS MP3 AUDIO PLAYER
# ------------------------------------------------------------
def play_bg_music(filepath):
    """
    Play MP3 background music asynchronously and looped on Windows.
    Uses winmm.dll (Media Control Interface) to avoid external dependencies.
    """
    try:
        import ctypes
        abs_path = os.path.abspath(filepath)
        # Ensure any previously opened instance is closed
        ctypes.windll.winmm.mciSendStringW("close bgmusic", None, 0, None)
        # Open the audio file and name it 'bgmusic'
        r1 = ctypes.windll.winmm.mciSendStringW(f'open "{abs_path}" type mpegvideo alias bgmusic', None, 0, None)
        # Play the audio file looped from 0:50 (50000 ms)
        r2 = ctypes.windll.winmm.mciSendStringW("play bgmusic from 50000 repeat", None, 0, None)
        if r1 == 0 and r2 == 0:
            print("[OK] Playing background music: Maa Tujhe Salaam")
        else:
            print(f"[Warning] MCI audio player returned error codes: Open={r1}, Play={r2}")
    except Exception as error:
        print(f"[Warning] Failed to play background music: {error}")

def stop_bg_music():
    """
    Stop background music playback and release resources.
    """
    try:
        import ctypes
        ctypes.windll.winmm.mciSendStringW("close bgmusic", None, 0, None)
        print("[OK] Background music playback stopped.")
    except Exception:
        pass

# Register the cleanup handler to turn off music when python exits
atexit.register(stop_bg_music)

# ------------------------------------------------------------
# LOAD & EXTRACT DATA
# ------------------------------------------------------------
def load_geojson():
    with open(GEOJSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def group_polygons_by_state(geojson):
    """
    Groups polygons by state name.
    Returns: dict { state_name: [list of polygons] }
    """
    states_data = {}
    features = geojson.get("features", [])

    for feature in features:
        properties = feature.get("properties", {})
        state_name = properties.get("ST_NM", "Unknown Territory")
        geometry = feature.get("geometry")
        if not geometry:
            continue

        geom_type = geometry.get("type")
        coords = geometry.get("coordinates")

        polygons = []
        if geom_type == "Polygon":
            if coords:
                polygons.append(coords[0])
        elif geom_type == "MultiPolygon":
            for poly in coords:
                if poly:
                    polygons.append(poly[0])

        if polygons:
            if state_name not in states_data:
                states_data[state_name] = []
            states_data[state_name].extend(polygons)

    return states_data

# ------------------------------------------------------------
# MAP PROJECTION UTILITY
# ------------------------------------------------------------
class MapProjection:
    def __init__(self, states_data, width, height, padding=120):
        # Calculate global bounding box
        longitudes = []
        latitudes = []
        for state_name, polygons in states_data.items():
            for poly in polygons:
                for lon, lat in poly:
                    longitudes.append(lon)
                    latitudes.append(lat)

        self.min_lon = min(longitudes)
        self.max_lon = max(longitudes)
        self.min_lat = min(latitudes)
        self.max_lat = max(latitudes)

        self.width = width
        self.height = height
        self.padding = padding

        drawable_w = width - 2 * padding
        drawable_h = height - 2 * padding

        lon_range = self.max_lon - self.min_lon
        lat_range = self.max_lat - self.min_lat

        # Keep aspect ratio correct
        scale_x = drawable_w / lon_range
        scale_y = drawable_h / lat_range
        self.scale = min(scale_x, scale_y)

        # Center alignment offset
        self.map_w = lon_range * self.scale
        self.map_h = lat_range * self.scale
        self.offset_x = -self.map_w / 2
        self.offset_y = -self.map_h / 2 + 30  # Shift up slightly to fit title at bottom

    def project(self, lon, lat):
        """
        Convert GPS coordinate (longitude, latitude) to screen coordinate (x, y)
        """
        x = (lon - self.min_lon) * self.scale + self.offset_x
        y = (lat - self.min_lat) * self.scale + self.offset_y
        return x, y

# ------------------------------------------------------------
# SUTHERLAND-HODGMAN POLYGON CLIPPING (Horizontal)
# ------------------------------------------------------------
def clip_polygon_horizontal(polygon, boundary_y, keep_above):
    """
    Clips a polygon against a horizontal line.
    keep_above=True: keeps coordinates where y >= boundary_y
    keep_above=False: keeps coordinates where y <= boundary_y
    """
    if not polygon:
        return []

    result = []

    def is_inside(pt):
        _, y = pt
        return (y >= boundary_y) if keep_above else (y <= boundary_y)

    def get_intersection(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if y1 == y2:
            return x1, boundary_y
        t = (boundary_y - y1) / (y2 - y1)
        x = x1 + t * (x2 - x1)
        return x, boundary_y

    previous = polygon[-1]
    for current in polygon:
        curr_inside = is_inside(current)
        prev_inside = is_inside(previous)

        if curr_inside:
            if not prev_inside:
                result.append(get_intersection(previous, current))
            result.append(current)
        elif prev_inside:
            result.append(get_intersection(previous, current))
        previous = current

    return result

# ------------------------------------------------------------
# TURTLE DRAWING FUNCTIONS
# ------------------------------------------------------------
def draw_filled_polygon(pen, points, color):
    """
    Draws a single filled polygon. Uses pencolor matching fill color
    to avoid showing visible seams or outlines during the fill phase.
    """
    if len(points) < 3:
        return

    pen.penup()
    pen.goto(points[0][0], points[0][1])
    pen.pendown()
    pen.fillcolor(color)
    pen.pencolor(color)
    pen.pensize(1)
    
    pen.begin_fill()
    for pt in points[1:]:
        pen.goto(pt[0], pt[1])
    pen.goto(points[0][0], points[0][1])
    pen.end_fill()
    pen.penup()

def draw_state_tricolour(pen, polygons, projection, min_y, max_y, state_name):
    """
    Clips and fills the state polygons into Saffron, White, and Green bands.
    Caches the projected coordinates for interactive click detection.
    """
    height = max_y - min_y
    stripe_1 = min_y + height / 3
    stripe_2 = min_y + 2 * height / 3

    if state_name not in projected_states:
        projected_states[state_name] = []

    for poly in polygons:
        # Project all coordinates to screen space
        projected_poly = [projection.project(lon, lat) for lon, lat in poly]
        if len(projected_poly) < 3:
            continue
        
        # Cache for click detection
        projected_states[state_name].append(projected_poly)

        # 1. Saffron (Top band)
        saffron_poly = clip_polygon_horizontal(projected_poly, stripe_2, keep_above=True)
        draw_filled_polygon(pen, saffron_poly, SAFFRON)

        # 2. White (Middle band)
        below_saffron = clip_polygon_horizontal(projected_poly, stripe_2, keep_above=False)
        white_poly = clip_polygon_horizontal(below_saffron, stripe_1, keep_above=True)
        draw_filled_polygon(pen, white_poly, WHITE)

        # 3. Green (Bottom band)
        green_poly = clip_polygon_horizontal(projected_poly, stripe_1, keep_above=False)
        draw_filled_polygon(pen, green_poly, GREEN)

# ------------------------------------------------------------
# TOPOLOGICAL BOUNDARY CLASSIFICATION
# ------------------------------------------------------------
def classify_edges(states_data):
    """
    Identifies which edges are national borders (appear once)
    and which are internal state borders (appear twice).
    """
    edge_counts = defaultdict(int)

    def round_coordinate(coord):
        return round(coord[0], 5), round(coord[1], 5)

    for _, polygons in states_data.items():
        for poly in polygons:
            n = len(poly)
            for i in range(n - 1):
                p1 = round_coordinate(poly[i])
                p2 = round_coordinate(poly[i+1])
                if p1 == p2:
                    continue
                edge = tuple(sorted([p1, p2]))
                edge_counts[edge] += 1

    outer_edges = [edge for edge, count in edge_counts.items() if count == 1]
    internal_edges = [edge for edge, count in edge_counts.items() if count > 1]
    return outer_edges, internal_edges

def get_continuous_chains(edges):
    """
    Groups unordered edges into continuous chains of vertices.
    This allows the turtle to draw in long, continuous strokes.
    """
    adj = defaultdict(list)
    for p1, p2 in edges:
        adj[p1].append(p2)
        adj[p2].append(p1)
        
    visited_edges = set()
    chains = []
    
    # Sort starting points by longitude then latitude to draw from West to East
    for start in sorted(adj.keys(), key=lambda pt: (pt[0], pt[1])):
        has_unvisited = False
        for neighbor in adj[start]:
            edge = tuple(sorted([start, neighbor]))
            if edge not in visited_edges:
                has_unvisited = True
                break
        if not has_unvisited:
            continue
            
        chain = [start]
        current = start
        while True:
            next_pt = None
            for neighbor in adj[current]:
                edge = tuple(sorted([current, neighbor]))
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    next_pt = neighbor
                    break
            if next_pt is None:
                break
            chain.append(next_pt)
            current = next_pt
        chains.append(chain)
        
    return chains


# ------------------------------------------------------------
# DRAW ASHOKA CHAKRA
# ------------------------------------------------------------
def draw_ashoka_chakra(projection, map_height):
    """
    Draws the Ashoka Chakra in Navy Blue at the center of India.
    Includes 24 spokes, inner ring, and 24 rim dots.
    """
    # Geographic center of India
    chakra_lon = 78.9629
    chakra_lat = 22.5937
    center_x, center_y = projection.project(chakra_lon, chakra_lat)

    # Size based on map dimensions
    radius = 42

    chakra_pen = turtle.Turtle(visible=False)
    chakra_pen.speed(0)
    chakra_pen.pensize(2.5)
    chakra_pen.pencolor(CHAKRA_BLUE)

    # 1. Outer Ring
    chakra_pen.penup()
    chakra_pen.goto(center_x, center_y - radius)
    chakra_pen.setheading(0)
    chakra_pen.pendown()
    chakra_pen.circle(radius)
    chakra_pen.penup()

    # 2. Inner Hub Ring
    inner_r = radius * 0.15
    chakra_pen.goto(center_x, center_y - inner_r)
    chakra_pen.pendown()
    chakra_pen.circle(inner_r)
    chakra_pen.penup()

    # 3. 24 Spokes and Decorative Rim Dots
    for i in range(24):
        angle = i * 15
        rad = math.radians(angle)

        # Coordinate calculations
        x_start = center_x + inner_r * math.cos(rad)
        y_start = center_y + inner_r * math.sin(rad)
        x_end = center_x + radius * math.cos(rad)
        y_end = center_y + radius * math.sin(rad)

        # Draw spoke line
        chakra_pen.goto(x_start, y_start)
        chakra_pen.pendown()
        chakra_pen.goto(x_end, y_end)
        chakra_pen.penup()

        # Draw decorative dot on the rim
        chakra_pen.goto(x_end, y_end)
        chakra_pen.dot(4, CHAKRA_BLUE)
        chakra_pen.penup()

        # Smooth rendering animation
        screen.update()
        time.sleep(0.01)

# ------------------------------------------------------------
# DRAW STATE CAPITALS
# ------------------------------------------------------------
def draw_capitals(projection):
    """
    Draws a golden glowing dot for each capital on the map.
    """
    capital_pen = turtle.Turtle(visible=False)
    capital_pen.speed(0)
    
    print("Drawing state capitals...")
    for state, info in STATE_DETAILS.items():
        cap_name, lon, lat, _ = info
        cx, cy = projection.project(lon, lat)
        
        # Golden glowing dot
        capital_pen.penup()
        capital_pen.goto(cx, cy)
        capital_pen.dot(5, GOLD_COLOR)
    screen.update()

# ------------------------------------------------------------
# DRAW PREAMBLE CARD
# ------------------------------------------------------------
def draw_preamble_card():
    """
    Draws a styled card in the top-right corner displaying the Preamble of the Constitution of India.
    """
    actual_w = screen.window_width()
    actual_h = screen.window_height()
    
    preamble_pen = turtle.Turtle(visible=False)
    preamble_pen.speed(0)
    
    # Card Bounds
    cx = actual_w / 2 - 360
    cy = actual_h / 2 - 425
    w = 320
    h = 390
    
    # Draw Background Card Box
    preamble_pen.penup()
    preamble_pen.goto(cx, cy)
    preamble_pen.pendown()
    preamble_pen.fillcolor(CARD_BG)
    preamble_pen.pencolor(CARD_BORDER)
    preamble_pen.pensize(2)
    
    preamble_pen.begin_fill()
    for _ in range(2):
        preamble_pen.forward(w)
        preamble_pen.left(90)
        preamble_pen.forward(h)
        preamble_pen.left(90)
    preamble_pen.end_fill()
    preamble_pen.penup()
    
    tx = cx + 18
    ty = cy + h - 28
    
    # Card Header
    preamble_pen.color(GOLD_COLOR)
    preamble_pen.goto(tx, ty)
    preamble_pen.write("THE PREAMBLE", align="left", font=("Georgia", 12, "bold"))
    
    preamble_pen.color(TEXT_MUTED)
    preamble_pen.goto(tx, ty - 16)
    preamble_pen.write("Constitution of India", align="left", font=("Arial", 8, "italic"))
    
    # Preamble text lines (styled and wrapped beautifully)
    preamble_lines = [
        ("WE, THE PEOPLE OF INDIA,", "Arial", 9, "bold", SAFFRON),
        ("having solemnly resolved to constitute India", "Arial", 8.5, "normal", TEXT_COLOR),
        ("into a SOVEREIGN, SOCIALIST,", "Arial", 9, "bold", WHITE),
        ("SECULAR, DEMOCRATIC, REPUBLIC", "Arial", 9, "bold", GREEN),
        ("and to secure to all its citizens:", "Arial", 8.5, "normal", TEXT_COLOR),
        ("", "Arial", 5, "normal", TEXT_COLOR), # Spacer
        ("JUSTICE,", "Arial", 9, "bold", GOLD_COLOR),
        ("  social, economic and political;", "Arial", 8.5, "normal", TEXT_COLOR),
        ("LIBERTY,", "Arial", 9, "bold", GOLD_COLOR),
        ("  of thought, expression, belief,", "Arial", 8.5, "normal", TEXT_COLOR),
        ("  faith and worship;", "Arial", 8.5, "normal", TEXT_COLOR),
        ("EQUALITY,", "Arial", 9, "bold", GOLD_COLOR),
        ("  of status and of opportunity;", "Arial", 8.5, "normal", TEXT_COLOR),
        ("and to promote among them all", "Arial", 8.5, "normal", TEXT_MUTED),
        ("FRATERNITY,", "Arial", 9, "bold", GOLD_COLOR),
        ("  assuring the dignity of the individual", "Arial", 8.5, "normal", TEXT_COLOR),
        ("  and the unity and integrity of the Nation.", "Arial", 8.5, "normal", TEXT_COLOR),
    ]
    
    start_y = ty - 40
    for text, font_name, size, weight, color in preamble_lines:
        if text == "":
            start_y -= 8
            continue
        preamble_pen.color(color)
        preamble_pen.goto(tx, start_y)
        preamble_pen.write(text, align="left", font=(font_name, int(size), weight))
        start_y -= 19
        
    screen.update()

# ------------------------------------------------------------
# INTERACTIVE INFO CARD (Point in Polygon & Click Handling)
# ------------------------------------------------------------
def is_point_in_polygon(x, y, poly):
    """
    Ray-casting algorithm to detect if coordinates (x, y) are inside a polygon.
    """
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def draw_text_wrapped(pen, text, x, y, max_width, line_height=18):
    """
    Helper to wrap text inside the info card to fit within max_width.
    """
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # Approximate pixel width: 7.2px per character at font size 10
        if len(test_line) * 7.2 > max_width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
        
    for idx, line in enumerate(lines):
        pen.goto(x, y - idx * line_height)
        pen.write(line, align="left", font=("Arial", 10, "normal"))

def draw_info_card(state_name=None):
    """
    Draws/Clears the info card in the empty bottom-left region of the window.
    """
    # Card Bounds
    actual_w = screen.window_width()
    actual_h = screen.window_height()
    cx = -actual_w / 2 + 40
    cy = -actual_h / 2 + 35
    w = 320
    h = 190
    
    # Draw Background Card Box
    panel_pen.clear()
    panel_pen.penup()
    panel_pen.goto(cx, cy)
    panel_pen.pendown()
    panel_pen.fillcolor(CARD_BG)
    panel_pen.pencolor(CARD_BORDER)
    panel_pen.pensize(2)
    
    panel_pen.begin_fill()
    for _ in range(2):
        panel_pen.forward(w)
        panel_pen.left(90)
        panel_pen.forward(h)
        panel_pen.left(90)
    panel_pen.end_fill()
    panel_pen.penup()
    
    # Writing offsets (pad coordinates inside the box)
    tx = cx + 18
    ty = cy + h - 30
    
    if not state_name:
        # Default state
        panel_pen.color(GOLD_COLOR)
        panel_pen.goto(tx, ty)
        panel_pen.write("INTERACTIVE MAP", align="left", font=("Arial", 12, "bold"))
        
        panel_pen.color(TEXT_COLOR)
        panel_pen.goto(tx, ty - 30)
        panel_pen.write("Click on any State or UT", align="left", font=("Arial", 11, "bold"))
        panel_pen.goto(tx, ty - 50)
        panel_pen.write("to explore details & interesting facts.", align="left", font=("Arial", 10, "normal"))
        
        panel_pen.color(TEXT_MUTED)
        panel_pen.goto(tx, ty - 90)
        panel_pen.write("Golden Dots show State Capitals.", align="left", font=("Arial", 9, "italic"))
    else:
        # State information state
        capital, cap_lon, cap_lat, fact = STATE_DETAILS.get(
            state_name, ("Unknown Capital", 0, 0, "No data available for this region.")
        )
        
        # 1. State Title (Saffron)
        panel_pen.color(SAFFRON)
        panel_pen.goto(tx, ty)
        panel_pen.write(state_name.upper(), align="left", font=("Arial", 13, "bold"))
        
        # 2. Capital Details (White)
        panel_pen.color(WHITE)
        panel_pen.goto(tx, ty - 28)
        panel_pen.write(f"Capital: {capital}", align="left", font=("Arial", 10, "bold"))
        
        # 3. Fun Fact (Light gray, word-wrapped)
        panel_pen.color(TEXT_COLOR)
        draw_text_wrapped(panel_pen, fact, tx, ty - 55, w - 30, line_height=18)
        
        # 4. Prompt to click another state (Muted)
        panel_pen.color(TEXT_MUTED)
        panel_pen.goto(tx, cy + 12)
        panel_pen.write("Click another state to explore.", align="left", font=("Arial", 8, "italic"))
        
    screen.update()

def draw_static_panels():
    """
    Draws static dashboard panels in the left and right empty spaces
    to show Tricolour significance, India's profile statistics, and global standings.
    """
    actual_w = screen.window_width()
    actual_h = screen.window_height()
    
    dash_pen = turtle.Turtle(visible=False)
    dash_pen.speed(0)
    
    # Helper to draw a card box
    def draw_box(cx, cy, w, h):
        dash_pen.penup()
        dash_pen.goto(cx, cy)
        dash_pen.pendown()
        dash_pen.fillcolor(CARD_BG)
        dash_pen.pencolor(CARD_BORDER)
        dash_pen.pensize(2)
        dash_pen.begin_fill()
        for _ in range(2):
            dash_pen.forward(w)
            dash_pen.left(90)
            dash_pen.forward(h)
            dash_pen.left(90)
        dash_pen.end_fill()
        dash_pen.penup()

    # --------------------------------------------------------
    # 1. LEFT PANEL: Tricolour & Symbols
    # --------------------------------------------------------
    lcx = -actual_w / 2 + 40
    lcy = -actual_h / 2 + 250
    lw = 320
    lh = 175
    draw_box(lcx, lcy, lw, lh)
    
    tx = lcx + 18
    ty = lcy + lh - 28
    
    dash_pen.color(GOLD_COLOR)
    dash_pen.goto(tx, ty)
    dash_pen.write("TRICOLOUR & SYMBOLS", align="left", font=("Arial", 11, "bold"))
    
    # Saffron stripe info
    dash_pen.color(SAFFRON)
    dash_pen.goto(tx, ty - 28)
    dash_pen.write("■ Saffron:", align="left", font=("Arial", 9, "bold"))
    dash_pen.color(TEXT_COLOR)
    dash_pen.goto(tx + 75, ty - 28)
    dash_pen.write("Strength, Courage & Sacrifice", align="left", font=("Arial", 9, "normal"))
    
    # White stripe info
    dash_pen.color(WHITE)
    dash_pen.goto(tx, ty - 52)
    dash_pen.write("■ White:", align="left", font=("Arial", 9, "bold"))
    dash_pen.color(TEXT_COLOR)
    dash_pen.goto(tx + 75, ty - 52)
    dash_pen.write("Peace, Truth & Purity", align="left", font=("Arial", 9, "normal"))
    
    # Green stripe info
    dash_pen.color(GREEN)
    dash_pen.goto(tx, ty - 76)
    dash_pen.write("■ Green:", align="left", font=("Arial", 9, "bold"))
    dash_pen.color(TEXT_COLOR)
    dash_pen.goto(tx + 75, ty - 76)
    dash_pen.write("Fertility, Growth & Prosperity", align="left", font=("Arial", 9, "normal"))
    
    # Chakra info
    dash_pen.color("#60A5FA") # Light blue for visibility
    dash_pen.goto(tx, ty - 100)
    dash_pen.write("■ Chakra:", align="left", font=("Arial", 9, "bold"))
    dash_pen.color(TEXT_COLOR)
    dash_pen.goto(tx + 75, ty - 100)
    dash_pen.write("24-Spoke Wheel of Righteousness", align="left", font=("Arial", 9, "normal"))

    # National Anthem info
    dash_pen.color(TEXT_MUTED)
    dash_pen.goto(tx, ty - 132)
    dash_pen.write("Anthem: Jana Gana Mana | Song: Vande Mataram", align="left", font=("Arial", 8, "italic"))

    # --------------------------------------------------------
    # 2. RIGHT PANEL: India Profile Stats
    # --------------------------------------------------------
    rcx = actual_w / 2 - 360
    rcy = -actual_h / 2 + 35
    rw = 320
    rh = 210
    draw_box(rcx, rcy, rw, rh)
    
    rtx = rcx + 18
    rty = rcy + rh - 28
    
    dash_pen.color(GOLD_COLOR)
    dash_pen.goto(rtx, rty)
    dash_pen.write("INDIA PROFILE", align="left", font=("Arial", 11, "bold"))
    
    stats = [
        ("States & UTs:", "28 States, 8 Union Territories"),
        ("Total Area:", "3.287 Million km² (7th)"),
        ("Coastline:", "7,516.6 Kilometers"),
        ("National Animal:", "Royal Bengal Tiger"),
        ("National Bird:", "Indian Peacock"),
        ("National Flower:", "Sacred Lotus (Nelumbo nucifera)")
    ]
    
    for idx, (label, val) in enumerate(stats):
        y_pos = rty - 26 - idx * 22
        dash_pen.color(SAFFRON)
        dash_pen.goto(rtx, y_pos)
        dash_pen.write(label, align="left", font=("Arial", 9, "bold"))
        
        # Color value
        dash_pen.color(WHITE)
        dash_pen.goto(rtx + 110, y_pos)
        dash_pen.write(val, align="left", font=("Arial", 9, "normal"))

    # --------------------------------------------------------
    # 3. TOP-LEFT PANEL: Global Index Standing
    # --------------------------------------------------------
    tlcx = -actual_w / 2 + 40
    tlcy = actual_h / 2 - 245
    tlw = 320
    tlh = 210
    draw_box(tlcx, tlcy, tlw, tlh)
    
    tltx = tlcx + 18
    tlty = tlcy + tlh - 28
    
    dash_pen.color(GOLD_COLOR)
    dash_pen.goto(tltx, tlty)
    dash_pen.write("GLOBAL INDEX STANDING", align="left", font=("Arial", 11, "bold"))
    
    index_ranks = [
        ("World Press Freedom:", "157 / 180 (2026)", SAFFRON),
        ("Global Hunger Index:", "102 / 123 (2025)", SAFFRON),
        ("Human Development (HDI):", "130 / 193 (2025)", WHITE),
        ("Global Gender Gap:", "131 / 148 (2025)", WHITE),
        ("Henley Passport Index:", "75 / 199 (2026)", GREEN),
        ("Climate Performance (CCPI):", "23 / 63 (2026)", GREEN)
    ]
    
    for idx, (label, val, color) in enumerate(index_ranks):
        y_pos = tlty - 26 - idx * 22
        dash_pen.color(color)
        dash_pen.goto(tltx, y_pos)
        dash_pen.write(label, align="left", font=("Arial", 9, "bold"))
        
        dash_pen.color(TEXT_COLOR)
        dash_pen.goto(tltx + 175, y_pos)
        dash_pen.write(val, align="left", font=("Arial", 9, "normal"))
        
    screen.update()

def handle_click(x, y):
    """
    On-click callback that runs point-in-polygon tests to find
    and display clicked state information.
    """
    clicked_state = None
    for state_name, polys in projected_states.items():
        for poly in polys:
            if is_point_in_polygon(x, y, poly):
                clicked_state = state_name
                break
        if clicked_state:
            break
            
    if clicked_state:
        print(f"Selected: {clicked_state}")
        draw_info_card(clicked_state)

# ------------------------------------------------------------
# MAIN EXECUTION FLOW
# ------------------------------------------------------------
# ------------------------------------------------------------
# MAIN EXECUTION FLOW
# ------------------------------------------------------------
def setup_background_image():
    """
    Downloads the user-requested background image, processes it to low opacity (12%),
    blended with our theme background color (#0B0D17), and sets it as the Turtle background.
    """
    from PIL import Image
    
    bg_url = "https://media.gettyimages.com/id/1087713054/photo/indian-independence-day-concepts.jpg?s=612x612&w=0&k=20&c=fYBedIQum9-sRA5I_X4KEw-cL5R2Qt9HhZMmwqHLDfY="
    os.makedirs(DATA_DIR, exist_ok=True)
    orig_path = os.path.join(DATA_DIR, "bg_orig.jpg")
    processed_path = os.path.join(DATA_DIR, "bg_processed.gif")
    
    # Download the image if not already cached
    if not os.path.exists(orig_path):
        try:
            print("Downloading background image...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = requests.get(bg_url, headers=headers, timeout=15)
            with open(orig_path, 'wb') as f:
                f.write(req.content)
            print("[OK] Background image downloaded.")
        except Exception as e:
            print(f"[Warning] Failed to download background image: {e}")
            return
            
    # Process and blend the image
    if os.path.exists(orig_path):
        try:
            actual_w = screen.window_width() or 1920
            actual_h = screen.window_height() or 1080
            
            with Image.open(orig_path) as im:
                # Resize to fit screen
                im_resized = im.resize((actual_w, actual_h), Image.Resampling.LANCZOS)
                # Create solid theme background
                bg = Image.new("RGBA", (actual_w, actual_h), BG_COLOR)
                # Convert resized to RGBA and set low opacity (12% alpha = 30 out of 255)
                im_rgba = im_resized.convert("RGBA")
                alpha = im_rgba.split()[3].point(lambda p: 30)
                im_rgba.putalpha(alpha)
                # Blend
                blended = Image.alpha_composite(bg, im_rgba)
                # Save as GIF
                blended.convert("RGB").save(processed_path, "GIF")
                
            # Set background picture
            screen.bgpic(processed_path)
            print("[OK] Background image applied successfully.")
        except Exception as e:
            print(f"[Warning] Failed to process background image: {e}")

def main():
    # 1. Download data
    download_boundary()

    # Download and apply background image
    setup_background_image()

    # Keep loading screen text visible for 2 seconds as requested
    time.sleep(2.0)

    # Clear Loading Text
    loading_pen.clear()

    # Start background music if file exists
    if os.path.exists(MUSIC_FILE):
        play_bg_music(MUSIC_FILE)
    else:
        print("[Warning] Music file not found at: " + MUSIC_FILE)

    try:
        # 2. Load geometries
        geojson = load_geojson()
        states_data = group_polygons_by_state(geojson)

        # Exaggerate Lakshadweep islands so they are visible and interactive (original is sub-pixel)
        if "Lakshadweep" in states_data:
            exaggerated_polygons = []
            islands_gps = [
                (72.6417, 10.5667), # Kavaratti
                (72.1861, 10.8539), # Agatti
                (73.6828, 10.8142), # Andrott
                (73.6347, 10.0828), # Kalpeni
                (73.0163, 8.2833)   # Minicoy
            ]
            for lon, lat in islands_gps:
                poly_gps = []
                deg = 0.16 # Exaggerated island radius in degrees (~4.2 pixels on screen)
                for i in range(8):
                    angle = math.radians(i * 45)
                    lon_p = lon + deg * math.cos(angle)
                    lat_p = lat + deg * math.sin(angle)
                    poly_gps.append((lon_p, lat_p))
                # Close the polygon
                poly_gps.append(poly_gps[0])
                exaggerated_polygons.append(poly_gps)
            states_data["Lakshadweep"] = exaggerated_polygons

        # 3. Initialize projection dynamically with actual screen dimensions to prevent cutoffs
        actual_w = screen.window_width()
        actual_h = screen.window_height()
        projection = MapProjection(states_data, actual_w, actual_h, padding=145)

        # Find global bounds of map on screen
        all_projected_y = []
        for state_name, polygons in states_data.items():
            for poly in polygons:
                for lon, lat in poly:
                    _, py = projection.project(lon, lat)
                    all_projected_y.append(py)
        
        min_y = min(all_projected_y)
        max_y = max(all_projected_y)

        # Status Writer
        status_pen = turtle.Turtle(visible=False)
        status_pen.penup()
        status_pen.color(TEXT_MUTED)
        status_pen.goto(-actual_w/2 + 50, -actual_h/2 + 50)

        # Map Pen
        map_pen = turtle.Turtle(visible=False)
        map_pen.speed(0)

        # 4. Classify boundaries
        print("Extracting boundaries...")
        outer_edges, internal_edges = classify_edges(states_data)

        # 5. Draw National Boundary (Bold, white line) in slow motion first
        print("Drawing national border...")
        status_pen.clear()
        status_pen.write("Drawing National Border...", align="left", font=("Arial", 11, "italic"))
        screen.update()

        map_pen.pencolor(NATIONAL_BORDER)
        map_pen.pensize(2.5)

        outer_chains = get_continuous_chains(outer_edges)
        edge_counter = 0
        for chain in outer_chains:
            if not chain:
                continue
            # Move to the start of the chain
            x0, y0 = projection.project(chain[0][0], chain[0][1])
            map_pen.penup()
            map_pen.goto(x0, y0)
            map_pen.pendown()
            
            # Draw the rest of the chain
            for pt in chain[1:]:
                x, y = projection.project(pt[0], pt[1])
                map_pen.goto(x, y)
                edge_counter += 1
                
                # Update screen and delay periodically to animate in slow motion (slower and smoother)
                if edge_counter % 15 == 0:
                    screen.update()
                    time.sleep(0.03)
        screen.update()

        # 6. Draw Tricolour Fill (Animate state-by-state)
        # Sort states by latitude center so drawing flows beautifully from North to South
        def get_state_lat_center(item):
            polys = item[1]
            lats = [pt[1] for p in polys for pt in p]
            return sum(lats) / len(lats) if lats else 0

        sorted_states = sorted(states_data.items(), key=get_state_lat_center, reverse=True)

        print("Drawing states and rendering tricolour fill...")
        for idx, (state_name, polygons) in enumerate(sorted_states):
            # Update status bar on screen
            status_pen.clear()
            status_pen.write(f"Rendering: {state_name} ({idx+1}/{len(states_data)})", 
                             align="left", font=("Arial", 11, "italic"))
            screen.update()

            # Render filled stripes
            draw_state_tricolour(map_pen, polygons, projection, min_y, max_y, state_name)
            
            # Micro-delay to create state-by-state visual loading effect (slower)
            time.sleep(0.12)

        status_pen.clear()
        status_pen.write("Drawing internal state borders...", align="left", font=("Arial", 11, "italic"))
        screen.update()

        # 7. Draw Internal Borders (Subtle, thin lines) in slow motion
        print("Drawing state borders...")
        map_pen.pencolor(STATE_BORDER)
        map_pen.pensize(1.0)

        internal_chains = get_continuous_chains(internal_edges)
        edge_counter = 0
        for chain in internal_chains:
            if not chain:
                continue
            # Move to the start of the chain
            x0, y0 = projection.project(chain[0][0], chain[0][1])
            map_pen.penup()
            map_pen.goto(x0, y0)
            map_pen.pendown()
            
            # Draw the rest of the chain
            for pt in chain[1:]:
                x, y = projection.project(pt[0], pt[1])
                map_pen.goto(x, y)
                edge_counter += 1
                
                # Update screen and delay periodically to animate in slow motion (slower and smoother)
                if edge_counter % 20 == 0:
                    screen.update()
                    time.sleep(0.03)
        screen.update()

        # 8. Redraw/Refresh National Boundary on top for clean outlines
        print("Refining national border...")
        status_pen.clear()
        status_pen.write("Refining borders...", align="left", font=("Arial", 11, "italic"))
        screen.update()

        map_pen.pencolor(NATIONAL_BORDER)
        map_pen.pensize(2.5)
        for chain in outer_chains:
            if not chain:
                continue
            x0, y0 = projection.project(chain[0][0], chain[0][1])
            map_pen.penup()
            map_pen.goto(x0, y0)
            map_pen.pendown()
            for pt in chain[1:]:
                x, y = projection.project(pt[0], pt[1])
                map_pen.goto(x, y)
        screen.update()

        # 9. Draw State Capitals (Golden dots layer)
        draw_capitals(projection)

        # 10. Draw Ashoka Chakra
        print("Drawing Ashoka Chakra...")
        draw_ashoka_chakra(projection, max_y - min_y)

        # 11. Draw Preamble of the Constitution
        draw_preamble_card()

        # 9. Draw Interactive Info Card Base
        draw_info_card()

        # Clear status text
        status_pen.clear()

        # 10. Draw Decorative Titles
        title_pen = turtle.Turtle(visible=False)
        title_pen.penup()
        title_pen.color(TEXT_COLOR)
        
        # Header Title
        title_pen.goto(0, actual_h / 2 - 65)
        title_pen.write("SATYAMEVA JAYATE", align="center", font=("Georgia", 22, "bold"))
        
        # Footer Title
        title_pen.goto(0, -actual_h / 2 + 65)
        title_pen.color(SAFFRON)
        title_pen.write("INDIA", align="center", font=("Arial", 28, "bold"))
        
        title_pen.goto(0, -actual_h / 2 + 35)
        title_pen.color(TEXT_COLOR)
        title_pen.write("Sovereign - Socialist - Secular - Democratic - Republic", align="center", font=("Arial", 12, "normal"))
        
        title_pen.goto(0, -actual_h / 2 + 13)
        title_pen.color(TEXT_MUTED)
        title_pen.write("Drawn with accurate geospatial boundary coordinates", align="center", font=("Arial", 9, "italic"))
        
        # 12. Draw static dashboard panels (Tricolour Significance & India Profile)
        draw_static_panels()
        
        screen.update()
        
        print("\n=============================================")
        print("JAI HIND! Map drawing completed successfully.")
        print("=============================================")
        print("Click on any state to view its information card!")
        print("Close the Turtle graphics window to exit.")

        # 11. Bind Click Handler for Interactive Tooltips
        screen.onclick(handle_click)

        screen.mainloop()
    except (turtle.Terminator, Exception) as e:
        # Check if the error is related to canvas/window closure
        err_msg = str(e)
        if "Terminator" in err_msg or "invalid command name" in err_msg:
            print("[Info] Map drawing window closed by user.")
        else:
            print(f"[Warning] Drawing interrupted: {e}")

if __name__ == "__main__":
    main()