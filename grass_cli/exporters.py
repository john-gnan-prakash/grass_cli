import os
from typing import Dict, Any

def export_markdown(data: Dict[str, Any], filepath: str):
    md_content = f"""# 🌲 {data.get('trail_name', 'Outdoor Trail')}

> **Summary:** {data.get('summary', 'N/A')}

- **Distance:** {data.get('distance_km')} km
- **Difficulty:** {data.get('difficulty')}
- **Est. Duration:** {data.get('estimated_duration_mins')} mins
- **Elevation Gain:** +{data.get('elevation_gain_m')}m

---

## 📍 Waypoints

"""
    for wp in data.get("waypoints", []):
        md_content += f"### {wp.get('step')}. [{wp.get('type').upper()}] {wp.get('name')}\n"
        md_content += f"{wp.get('description')}\n"
        md_content += f"*Coords: {wp.get('latitude')}, {wp.get('longitude')}*\n\n"

    md_content += "---\n\n## 🎒 Packing Checklist\n\n"
    for item in data.get("packing_list", []):
        md_content += f"- [ ] {item}\n"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)


def export_gpx(data: Dict[str, Any], filepath: str):
    gpx_content = f"""<?xml version="1.1" encoding="UTF-8"?>
<gpx version="1.1" creator="grass-cli" xmlns="[http://www.topografix.com/GPX/1/1](http://www.topografix.com/GPX/1/1)">
  <metadata>
    <name>{data.get('trail_name')}</name>
    <desc>{data.get('summary')}</desc>
  </metadata>
  <trk>
    <name>{data.get('trail_name')}</name>
    <trkseg>
"""
    for wp in data.get("waypoints", []):
        lat = wp.get("latitude", 0.0)
        lon = wp.get("longitude", 0.0)
        gpx_content += f'      <trkpt lat="{lat}" lon="{lon}">\n'
        gpx_content += f'        <name>{wp.get("name")}</name>\n'
        gpx_content += f'        <desc>{wp.get("description")}</desc>\n'
        gpx_content += f'      </trkpt>\n'

    gpx_content += """    </trkseg>
  </trk>
</gpx>"""

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(gpx_content)