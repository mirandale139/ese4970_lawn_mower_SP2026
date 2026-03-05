import csv

input_file = "/home/gle/ESE4970/gps_output/gps_boundary.csv"
output_file = "/home/gle/ESE4970/gps_output/boundary_map.html"

points = []

# Read CSV
with open(input_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lat = float(row["latitude"])
        lon = float(row["longitude"])
        points.append((lat, lon))

if not points:
    print("No points found.")
    exit()

center_lat = points[0][0]
center_lon = points[0][1]

# Convert to JS array format
js_points = ",\n".join(
    [f"[{lat}, {lon}]" for lat, lon in points]
)

html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>GPS Boundary</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>

  <style>
    #map {{
      height: 100vh;
    }}
  </style>
</head>
<body>

<div id="map"></div>

<!-- Leaflet JS -->
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<script>

  var map = L.map('map').setView([{center_lat}, {center_lon}], 18);

  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
  }}).addTo(map);

  var boundaryCoords = [
    {js_points}
  ];

  var polygon = L.polygon(boundaryCoords, {{
      color: 'blue',
      fillOpacity: 0.3
  }}).addTo(map);

  // Add markers
  boundaryCoords.forEach(function(coord, index) {{
      L.marker(coord).addTo(map)
        .bindPopup("Corner " + (index+1));
  }});

  map.fitBounds(polygon.getBounds());

</script>

</body>
</html>
"""

with open(output_file, "w") as f:
    f.write(html_content)

print(f"Map generated: {output_file}")
