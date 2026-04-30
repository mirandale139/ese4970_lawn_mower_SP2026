import pandas as pd
import numpy as np
import random
import math
from shapely.geometry import Polygon, LineString, Point
from shapely.affinity import rotate
from pyproj import CRS, Transformer

# ---------------- CONFIGURATION ----------------
INPUT_FILE = "gps_boundary_0416_lawn2.csv"
OUTPUT_FILE = "advanced_path_planning.html"

BLADE_WIDTH_FT = 1.6
OVERLAP_PERCENT = 0.15 
EFFECTIVE_WIDTH_M = (BLADE_WIDTH_FT * (1 - OVERLAP_PERCENT)) * 0.3048 

# ---------------- 1. LOAD DATA ----------------
df = pd.read_csv(INPUT_FILE)
coords = df[['latitude', 'longitude']].values.tolist()

if not coords:
    print("No points found.")
    exit()

# ---------------- 2. PROJECTION & GEOMETRY ----------------
lat_center, lon_center = coords[0]
crs_wgs84 = CRS.from_epsg(4326) 
crs_local = CRS.from_string(f"+proj=aeqd +lat_0={lat_center} +lon_0={lon_center} +datum=WGS84 +units=m")

to_local = Transformer.from_crs(crs_wgs84, crs_local, always_xy=True)
to_wgs84 = Transformer.from_crs(crs_local, crs_wgs84, always_xy=True)

local_coords = [to_local.transform(lon, lat) for lat, lon in coords]
lawn_poly = Polygon(local_coords).buffer(0) 

def get_random_point(poly):
    minx, miny, maxx, maxy = poly.bounds
    while True:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(p):
            return p

def trace_boundary(p1, p2, boundary_poly):
    ring = boundary_poly.exterior
    d1 = ring.project(Point(p1))
    d2 = ring.project(Point(p2))
    L = ring.length
    
    diff = abs(d1 - d2)
    if diff < 1e-3: return [p2]
        
    if d1 <= d2: dists = np.linspace(d1, d2, 15) if diff <= L / 2 else np.linspace(d1, d2 - L, 15)
    else: dists = np.linspace(d1, d2, 15) if diff <= L / 2 else np.linspace(d1, d2 + L, 15)
        
    return [ring.interpolate(d % L).coords[0] for d in dists[1:]]

def route_around(p1, p2, obstacles):
    segment = LineString([p1, p2])
    polys = [obstacles] if obstacles.geom_type == 'Polygon' else list(obstacles.geoms)
    
    for poly in polys:
        inter = segment.intersection(poly)
        if inter.is_empty or inter.geom_type in ['Point', 'MultiPoint']: continue
        if inter.length < 1e-3: continue
            
        if inter.geom_type == 'LineString':
            enter_pt, exit_pt = inter.coords[0], inter.coords[-1]
        elif inter.geom_type == 'MultiLineString':
            lines = sorted(list(inter.geoms), key=lambda l: Point(p1).distance(Point(l.coords[0])))
            enter_pt, exit_pt = lines[0].coords[0], lines[0].coords[-1]
        else: continue
            
        path = []
        ring = poly.exterior
        d1, d2 = ring.project(Point(enter_pt)), ring.project(Point(exit_pt))
        L = ring.length
        
        diff = abs(d1 - d2)
        if d1 <= d2: dists = np.linspace(d1, d2, 15) if diff <= L / 2 else np.linspace(d1, d2 - L, 15)
        else: dists = np.linspace(d1, d2, 15) if diff <= L / 2 else np.linspace(d1, d2 + L, 15)
                
        arc = [ring.interpolate(d % L).coords[0] for d in dists]
        path.extend(arc)
        
        if Point(exit_pt).distance(Point(p2)) > 1e-3:
            path.extend(route_around(exit_pt, p2, obstacles))
        return path
            
    return [p2]

def generate_sweeps(poly_area, obstacles=None, boundary_poly=None):
    if poly_area.is_empty: return []
    minx, miny, maxx, maxy = poly_area.bounds
    y_sweeps = np.arange(miny + (EFFECTIVE_WIDTH_M/2), maxy, EFFECTIVE_WIDTH_M)
    path_pts = []
    left_to_right = True

    for y in y_sweeps:
        sweep_line = LineString([(minx - 10, y), (maxx + 10, y)])
        intersection = poly_area.intersection(sweep_line)
        
        if intersection.is_empty: continue
        
        lines = []
        if intersection.geom_type == 'LineString': lines = [intersection]
        elif intersection.geom_type == 'MultiLineString': lines = list(intersection.geoms)
        elif intersection.geom_type == 'GeometryCollection':
            lines = [geom for geom in intersection.geoms if geom.geom_type == 'LineString']
            
        if not lines: continue
            
        lines = sorted(lines, key=lambda l: l.bounds[0])
        if not left_to_right: lines = list(reversed(lines))
            
        for line in lines:
            pts = list(line.coords)
            if not left_to_right: pts = pts[::-1] 
            
            for i, pt in enumerate(pts):
                if not path_pts:
                    path_pts.append(pt)
                    continue
                    
                last_pt = path_pts[-1]
                
                if i == 0 and boundary_poly is not None:
                    ring = boundary_poly.exterior
                    if ring.distance(Point(last_pt)) < 0.2 and ring.distance(Point(pt)) < 0.2:
                        b_trace = trace_boundary(last_pt, pt, boundary_poly)
                        path_pts.extend(b_trace)
                        continue
                
                if obstacles is not None and not obstacles.is_empty:
                    routed = route_around(last_pt, pt, obstacles)
                    path_pts.extend(routed)
                else:
                    path_pts.append(pt)
                
        left_to_right = not left_to_right 
    return path_pts

def generate_angled_sweeps(poly_area, angle_deg, origin_pt, obstacles=None, boundary_poly=None):
    if poly_area.is_empty: return []
    
    rot_poly = rotate(poly_area, -angle_deg, origin=origin_pt)
    rot_obs = rotate(obstacles, -angle_deg, origin=origin_pt) if obstacles else None
    rot_bound = rotate(boundary_poly, -angle_deg, origin=origin_pt) if boundary_poly else None

    path_pts_rot = generate_sweeps(rot_poly, rot_obs, rot_bound)

    path_pts = []
    for pt in path_pts_rot:
        p = rotate(Point(pt), angle_deg, origin=origin_pt)
        path_pts.append((p.x, p.y))
    return path_pts


# ---------------- METRICS EVALUATION ----------------
def evaluate_path(path_pts, boundary_poly, effective_width):
    if not path_pts or len(path_pts) < 2:
        return {"distance_m": 0, "turns": 0, "cumulative_angle_deg": 0, "coverage_pct": 0}

    # 1. Distance
    distance = sum(math.dist(path_pts[i], path_pts[i+1]) for i in range(len(path_pts)-1))

    # 2 & 3. Turns and Cumulative Angle
    turns = 0
    cumulative_angle = 0
    
    for i in range(len(path_pts)-2):
        x1, y1 = path_pts[i]
        x2, y2 = path_pts[i+1]
        x3, y3 = path_pts[i+2]
        
        angle1 = math.atan2(y2 - y1, x2 - x1)
        angle2 = math.atan2(y3 - y2, x3 - x2)
        
        diff = math.degrees(angle2 - angle1)
        # Normalize to -180 to 180
        diff = (diff + 180) % 360 - 180
        
        # Turn threshold filter (e.g. > 5 degrees)
        if abs(diff) > 5.0:
            turns += 1
        cumulative_angle += abs(diff)

    # 4. Coverage Percentage
    try:
        path_line = LineString(path_pts)
        # Buffer the path by half the effective mower width to simulate mowing path
        mowed_area = path_line.buffer(effective_width / 2)
        # Intersect with the actual boundary in case it bleeds outside
        valid_mowed_area = mowed_area.intersection(boundary_poly)
        coverage_pct = (valid_mowed_area.area / boundary_poly.area) * 100
    except:
        coverage_pct = 0.0

    return {
        "distance_m": distance,
        "turns": turns,
        "cumulative_angle_deg": cumulative_angle,
        "coverage_pct": coverage_pct
    }

# ---------------- SCENARIO PREP ----------------
inner_poly = lawn_poly.buffer(-EFFECTIVE_WIDTH_M * 0.9)
if inner_poly.is_empty: inner_poly = lawn_poly 
perimeter_path_local = list(lawn_poly.exterior.coords)

# SCENARIO 1: Horizontal Systemic
path_s1_local = perimeter_path_local + generate_sweeps(inner_poly, boundary_poly=inner_poly)

# SCENARIO 2: Random Bounce (Roomba Style)
path_s2_local = []
curr_pt = get_random_point(lawn_poly)
path_s2_local.append((curr_pt.x, curr_pt.y))
curr_angle = random.uniform(0, 2 * math.pi)

for _ in range(150): 
    ray_len = 100  
    ray = LineString([curr_pt, Point(curr_pt.x + ray_len * math.cos(curr_angle), curr_pt.y + ray_len * math.sin(curr_angle))])
    intersect = ray.intersection(lawn_poly)
    
    if intersect.geom_type == 'LineString': next_pt = Point(intersect.coords[-1])
    elif intersect.geom_type == 'MultiLineString': next_pt = Point(intersect.geoms[0].coords[-1])
    else: break 
        
    path_s2_local.append((next_pt.x, next_pt.y))
    curr_pt = next_pt
    for _ in range(20):
        new_angle = random.uniform(0, 2 * math.pi)
        if lawn_poly.contains(Point(curr_pt.x + 0.1 * math.cos(new_angle), curr_pt.y + 0.1 * math.sin(new_angle))):
            curr_angle = new_angle
            break

# SCENARIO 3: Horizontal Obstacles
obs1, obs2 = get_random_point(inner_poly).buffer(1.0), get_random_point(inner_poly).buffer(1.2)
obstacles = obs1.union(obs2)
navigable_inner = inner_poly.difference(obstacles)
path_s3_local = perimeter_path_local + generate_sweeps(navigable_inner, obstacles=obstacles, boundary_poly=inner_poly)

obs_latlon = []
for poly in ([obstacles] if obstacles.geom_type == 'Polygon' else obstacles.geoms):
    obs_latlon.append([to_wgs84.transform(x, y)[::-1] for x, y in poly.exterior.coords])

# SCENARIO 4: Diagonal Sweeps (45 Degrees)
rot_origin = Point(lawn_poly.centroid)
path_s4_local = perimeter_path_local + generate_angled_sweeps(inner_poly, 45, rot_origin, boundary_poly=inner_poly)

# --- RUN METRICS ---
print("\n" + "="*50)
print("PATH PLANNING ALGORITHM METRICS EVALUATION")
print("="*50)
scenarios = [
    ("Scenario 1: Horizontal Systemic", path_s1_local),
    ("Scenario 2: Random Bounce", path_s2_local),
    ("Scenario 3: Horizontal with Obstacles", path_s3_local),
    ("Scenario 4: Diagonal Sweeps (45°)", path_s4_local)
]

for name, path in scenarios:
    # Use lawn_poly for baseline coverage boundary (minus obstacles for S3)
    eval_boundary = lawn_poly.difference(obstacles) if "Obstacles" in name else lawn_poly
    metrics = evaluate_path(path, eval_boundary, EFFECTIVE_WIDTH_M)
    
    print(f"\n{name}:")
    print(f"  - Distance:         {metrics['distance_m']:.2f} meters")
    print(f"  - Turn Count:       {metrics['turns']}")
    print(f"  - Cumulative Angle: {metrics['cumulative_angle_deg']:.2f}°")
    print(f"  - Area Covered:     {metrics['coverage_pct']:.2f}%")
print("\n" + "="*50 + "\n")


# ---------------- 3. CONVERT PATHS TO GPS ----------------
def local_to_gps(local_path):
    return [(lat, lon) for lon, lat in [to_wgs84.transform(x, y) for x, y in local_path]]

path_s1_gps = local_to_gps(path_s1_local)
path_s2_gps = local_to_gps(path_s2_local)
path_s3_gps = local_to_gps(path_s3_local)
path_s4_gps = local_to_gps(path_s4_local)

# ---------------- 4. GENERATE HTML MAP ----------------
def to_js_array(gps_list): return ",\n    ".join([f"[{lat}, {lon}]" for lat, lon in gps_list])

js_boundary = to_js_array([(lat, lon) for lat, lon in coords])
js_path1 = to_js_array(path_s1_gps)
js_path2 = to_js_array(path_s2_gps)
js_path3 = to_js_array(path_s3_gps)
js_path4 = to_js_array(path_s4_gps)
js_obs_array = ",\n    ".join(["[" + to_js_array(obs) + "]" for obs in obs_latlon])

html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>Lawnmower Path Plan</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
  <style> #map {{ height: 100vh; margin: 0; padding: 0; }} </style>
</head>
<body>

<div id="map"></div>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  var map = L.map('map').setView([{lat_center}, {lon_center}], 20);

  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 22, attribution: '© OpenStreetMap'
  }}).addTo(map);

  var boundary = L.polygon([{js_boundary}], {{color: 'blue', fillOpacity: 0.1}}).addTo(map);

  // Scenario 1: Horizontal (Blue Path)
  var layerS1 = L.layerGroup();
  L.polyline([{js_path1}], {{color: '#007BFF', weight: 3}}).addTo(layerS1);
  if([{js_path1}].length > 0) L.circleMarker([{js_path1}][0], {{color: 'black', fillColor: 'black', fillOpacity: 1, radius: 6}}).addTo(layerS1).bindPopup("Start");

  // Scenario 2: Roomba (Orange Path)
  var layerS2 = L.layerGroup();
  L.polyline([{js_path2}], {{color: '#FF5733', weight: 2}}).addTo(layerS2);
  if([{js_path2}].length > 0) L.circleMarker([{js_path2}][0], {{color: 'black', fillColor: 'black', fillOpacity: 1, radius: 6}}).addTo(layerS2).bindPopup("Start");

  // Scenario 3: Obstacles (Purple Path)
  var layerS3 = L.layerGroup();
  var obstacleCoords = [{js_obs_array}];
  obstacleCoords.forEach(obs => L.polygon(obs, {{color: '#FF0000', fillColor: '#FF0000', fillOpacity: 0.5}}).addTo(layerS3));
  L.polyline([{js_path3}], {{color: '#9C27B0', weight: 3}}).addTo(layerS3);
  if([{js_path3}].length > 0) L.circleMarker([{js_path3}][0], {{color: 'black', fillColor: 'black', fillOpacity: 1, radius: 6}}).addTo(layerS3).bindPopup("Start");

  // Scenario 4: Diagonal (Green Path)
  var layerS4 = L.layerGroup();
  L.polyline([{js_path4}], {{color: '#28A745', weight: 3}}).addTo(layerS4);
  if([{js_path4}].length > 0) L.circleMarker([{js_path4}][0], {{color: 'black', fillColor: 'black', fillOpacity: 1, radius: 6}}).addTo(layerS4).bindPopup("Start");
  layerS4.addTo(map); // Default active layer

  // Layer Control Menu
  var overlayMaps = {{
      "S1: Horizontal Edge Trace (Blue)": layerS1,
      "S2: Random Bouncing (Orange)": layerS2,
      "S3: Obstacles + Edge Trace (Purple)": layerS3,
      "S4: Diagonal Edge Trace (Green)": layerS4
  }};
  L.control.layers(null, overlayMaps, {{collapsed: false}}).addTo(map);

</script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w") as f:
    f.write(html_content)

print(f"Success! Generated 4-scenario map to {OUTPUT_FILE}")
