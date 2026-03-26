#!/usr/bin/env python3
"""
G20 Embassy Distance Map Generator.

Generates an interactive HTML map showing:
- Power centers of each G20 country
- Embassy locations of G20 countries in each G20 capital
- Distance comparison between embassies and power centers
"""

import json
import folium
from folium import plugins
from src.data import (
    POWER_CENTERS,
    EMBASSIES,
    FLAGS,
    COUNTRY_COLORS,
    compute_distances,
    get_statistics,
    haversine_km,
)

OUTPUT_FILE = "dist/g20_embassy_map.html"

# Country code mapping for flag images
COUNTRY_CODES = {k: v["country_code"].lower() for k, v in POWER_CENTERS.items()}


def _flag_img(country, size=24):
    """Return an HTML img tag for a country's flag using flagcdn.com."""
    code = COUNTRY_CODES.get(country, "")
    if not code:
        return FLAGS.get(country, "")
    return f'<img src="https://flagcdn.com/w40/{code}.png" width="{size}" height="{int(size*0.67)}" style="vertical-align:middle;border:1px solid #ccc;border-radius:2px;" alt="{country}">'


def _flag_icon(country, size=28):
    """Return a folium DivIcon with a flag image."""
    code = COUNTRY_CODES.get(country, "")
    if not code:
        return folium.Icon(color="blue", icon="flag", prefix="fa")
    html = f'<img src="https://flagcdn.com/w40/{code}.png" width="{size}" style="border:1px solid rgba(0,0,0,0.2);border-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,0.3);cursor:pointer;">'
    return folium.DivIcon(
        html=html,
        icon_size=(size, int(size * 0.67)),
        icon_anchor=(size // 2, int(size * 0.67) // 2),
    )


def create_map():
    """Create the interactive G20 embassy distance map."""
    m = folium.Map(
        location=[20, 0],
        zoom_start=3,
        tiles="CartoDB positron",
        control_scale=True,
    )

    distances = compute_distances()
    stats = get_statistics()

    # Store layer references for JS navigation
    layer_var_names = {}

    # Create a feature group for each host country
    for idx, (host_country, host_info) in enumerate(POWER_CENTERS.items()):
        var_name = f"fg_{idx}"
        layer_var_names[host_country] = var_name

        fg = folium.FeatureGroup(
            name=f"{_flag_img(host_country, 16)} {host_country}",
            show=False,
        )

        pc_lat = host_info["lat"]
        pc_lon = host_info["lon"]

        # Power center marker (star icon)
        power_center_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 280px;">
            <h3 style="margin:0 0 8px; color:#333; border-bottom: 2px solid #e74c3c;">
                {_flag_img(host_country)} {host_country}
            </h3>
            <p style="margin:4px 0;"><strong>Power Center:</strong> {host_info['name']}</p>
            <p style="margin:4px 0;"><strong>Capital:</strong> {host_info['capital']}</p>
            <p style="margin:4px 0;"><strong>Coordinates:</strong> {pc_lat:.4f}, {pc_lon:.4f}</p>
            <hr style="margin:8px 0;">
            <p style="margin:4px 0; font-size:0.9em;">
                <strong>Avg. embassy distance:</strong> {stats[host_country]['average']:.1f} km<br>
                <strong>Closest embassy:</strong> {_flag_img(stats[host_country]['closest'][0], 16)}
                {stats[host_country]['closest'][0]} ({stats[host_country]['closest'][1]:.1f} km)<br>
                <strong>Farthest embassy:</strong> {_flag_img(stats[host_country]['farthest'][0], 16)}
                {stats[host_country]['farthest'][0]} ({stats[host_country]['farthest'][1]:.1f} km)
            </p>
        </div>
        """

        folium.Marker(
            location=[pc_lat, pc_lon],
            popup=folium.Popup(power_center_html, max_width=350),
            tooltip=f"{FLAGS.get(host_country, '')} {host_info['name']} ({host_country})",
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
        ).add_to(fg)

        # Embassy markers and distance lines
        if host_country in EMBASSIES:
            host_embassies = EMBASSIES[host_country]
            host_distances = distances[host_country]
            sorted_embassies = sorted(host_distances.items(), key=lambda x: x[1])

            for rank, (origin_country, dist_km) in enumerate(sorted_embassies, 1):
                if origin_country not in host_embassies:
                    continue

                e_lat, e_lon = host_embassies[origin_country]

                # Color gradient: green (close) -> yellow -> red (far)
                max_dist = sorted_embassies[-1][1] if sorted_embassies else 1
                min_dist = sorted_embassies[0][1] if sorted_embassies else 0
                dist_range = max_dist - min_dist if max_dist != min_dist else 1
                ratio = (dist_km - min_dist) / dist_range

                if ratio < 0.5:
                    r = int(255 * (ratio * 2))
                    g = 180
                    line_color = f"#{r:02x}{g:02x}00"
                else:
                    r = 255
                    g = int(180 * (1 - (ratio - 0.5) * 2))
                    line_color = f"#{r:02x}{g:02x}00"

                embassy_html = f"""
                <div style="font-family: Arial, sans-serif; min-width: 250px;">
                    <h4 style="margin:0 0 6px; color:#333;">
                        {_flag_img(origin_country)} Embassy of {origin_country}
                    </h4>
                    <p style="margin:4px 0;">
                        <strong>Host:</strong> {_flag_img(host_country, 16)} {host_country} ({host_info['capital']})
                    </p>
                    <p style="margin:4px 0;">
                        <strong>Distance to {host_info['name']}:</strong>
                        <span style="color: {line_color}; font-weight: bold;">{dist_km:.1f} km</span>
                    </p>
                    <p style="margin:4px 0;">
                        <strong>Rank:</strong> #{rank} / {len(sorted_embassies)}
                        {"  (closest)" if rank == 1 else "  (farthest)" if rank == len(sorted_embassies) else ""}
                    </p>
                </div>
                """

                # Embassy marker with flag image
                folium.Marker(
                    location=[e_lat, e_lon],
                    icon=_flag_icon(origin_country),
                    popup=folium.Popup(embassy_html, max_width=300),
                    tooltip=f"{FLAGS.get(origin_country, '')} {origin_country} - {dist_km:.1f} km",
                ).add_to(fg)

                # Distance line
                folium.PolyLine(
                    locations=[[e_lat, e_lon], [pc_lat, pc_lon]],
                    color=line_color,
                    weight=2,
                    opacity=0.6,
                    dash_array="5 5",
                    tooltip=f"{origin_country} → {host_info['name']}: {dist_km:.1f} km",
                ).add_to(fg)

        fg.add_to(m)

    # Overview layer with all power centers
    overview = folium.FeatureGroup(name="Overview: All Power Centers", show=True)
    for country, info in POWER_CENTERS.items():
        folium.Marker(
            location=[info["lat"], info["lon"]],
            tooltip=f"{FLAGS.get(country, '')} {country}: {info['name']}",
            icon=folium.Icon(color="darkred", icon="university", prefix="fa"),
        ).add_to(overview)
    overview.add_to(m)

    # Layer control (collapsed so it can be opened/closed)
    folium.LayerControl(collapsed=True).add_to(m)

    # Legend / info panel
    legend_html = _build_legend_html(stats)
    m.get_root().html.add_child(folium.Element(legend_html))

    # Navigation buttons panel
    nav_html = _build_nav_buttons()
    m.get_root().html.add_child(folium.Element(nav_html))

    # Fullscreen plugin
    plugins.Fullscreen().add_to(m)

    return m


def _build_nav_buttons():
    """Build navigation buttons to jump to each country."""
    buttons = ""
    for country, info in POWER_CENTERS.items():
        code = COUNTRY_CODES.get(country, "")
        flag_img = f'<img src="https://flagcdn.com/w20/{code}.png" width="20" style="vertical-align:middle;border-radius:2px;">' if code else ""
        lat = info["lat"]
        lon = info["lon"]
        # Determine zoom level based on country size
        zoom = 12
        buttons += f"""
        <button onclick="goToCountry({lat},{lon},'{country}')"
            style="display:flex;align-items:center;gap:6px;padding:4px 10px;border:1px solid #ddd;
            border-radius:6px;background:white;cursor:pointer;font-size:11px;white-space:nowrap;
            transition:all 0.15s;"
            onmouseover="this.style.background='#f0f0f0';this.style.borderColor='#999'"
            onmouseout="this.style.background='white';this.style.borderColor='#ddd'">
            {flag_img} <span>{country}</span>
        </button>"""

    return f"""
    <div id="nav-panel" style="
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: white;
        padding: 8px 12px;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.2);
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        max-width: 90vw;
        justify-content: center;
    ">
        {buttons}
    </div>
    <script>
    function goToCountry(lat, lon, name) {{
        // Find the map object
        var maps = document.querySelectorAll('.folium-map');
        if (maps.length > 0) {{
            var mapId = maps[0].id;
            var map = window[mapId];
            if (!map) {{
                // Try to find via L.Map instances
                for (var key in window) {{
                    if (window[key] instanceof L.Map) {{
                        map = window[key];
                        break;
                    }}
                }}
            }}
            if (map) {{
                map.setView([lat, lon], 12, {{animate: true, duration: 0.8}});

                // Try to activate the corresponding layer
                var inputs = document.querySelectorAll('.leaflet-control-layers-selector');
                inputs.forEach(function(input) {{
                    var label = input.closest('label') || input.parentElement;
                    var text = label ? label.textContent : '';
                    if (text.includes(name)) {{
                        if (!input.checked) {{
                            input.click();
                        }}
                    }}
                }});
            }}
        }}
    }}
    </script>
    """


def _build_legend_html(stats):
    """Build the HTML for the info panel / legend."""
    all_avg_distances = []
    for host, st in stats.items():
        all_avg_distances.append((host, st["average"]))
    all_avg_distances.sort(key=lambda x: x[1])

    ranking_rows = ""
    for i, (country, avg) in enumerate(all_avg_distances, 1):
        code = COUNTRY_CODES.get(country, "")
        flag = f'<img src="https://flagcdn.com/w20/{code}.png" width="16" style="vertical-align:middle;border-radius:1px;">' if code else ""
        ranking_rows += f"""
        <tr>
            <td style="padding:2px 6px;">{i}</td>
            <td style="padding:2px 6px;">{flag} {country}</td>
            <td style="padding:2px 6px; text-align:right;">{avg:.1f} km</td>
        </tr>"""

    return f"""
    <div id="info-panel" style="
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 1000;
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        max-width: 380px;
        max-height: 60vh;
        overflow-y: auto;
        font-family: Arial, sans-serif;
        font-size: 13px;
    ">
        <h3 style="margin:0 0 10px; color:#333;">
            G20 Embassy Distance Map
        </h3>
        <p style="margin:0 0 8px; color:#666; font-size:12px;">
            Distance between G20 embassies and host country power centers.
            Click a flag button above or use the layer control to explore.
        </p>
        <a href="g20_distance_matrix.html" style="display:inline-block;margin-bottom:10px;padding:6px 12px;
            background:#0066cc;color:white;border-radius:6px;text-decoration:none;font-size:12px;font-weight:500;">
            View Distance Matrix Table
        </a>
        <details>
            <summary style="cursor:pointer; font-weight:bold; color:#555; margin-bottom:6px;">
                Average Distance Ranking
            </summary>
            <table style="width:100%; border-collapse:collapse; font-size:12px;">
                <thead>
                    <tr style="border-bottom:1px solid #ddd;">
                        <th style="padding:2px 6px; text-align:left;">#</th>
                        <th style="padding:2px 6px; text-align:left;">Country</th>
                        <th style="padding:2px 6px; text-align:right;">Avg. Dist.</th>
                    </tr>
                </thead>
                <tbody>{ranking_rows}</tbody>
            </table>
        </details>
        <details style="margin-top:8px;">
            <summary style="cursor:pointer; font-weight:bold; color:#555; margin-bottom:6px;">
                Legend
            </summary>
            <div style="font-size:12px; color:#666;">
                <p style="margin:4px 0;">
                    <span style="color:red;">&#9733;</span> Power Center (government seat)
                </p>
                <p style="margin:4px 0;">
                    <img src="https://flagcdn.com/w20/us.png" width="14" style="vertical-align:middle;"> Embassy location (flag of origin country)
                </p>
                <p style="margin:4px 0;">
                    <span style="color:green;">---</span> Close to power center
                </p>
                <p style="margin:4px 0;">
                    <span style="color:red;">---</span> Far from power center
                </p>
            </div>
        </details>
    </div>
    """


def generate_distance_matrix_html():
    """Generate an HTML page with a distance matrix table."""
    distances = compute_distances()

    # Group countries by continent
    CONTINENTS = [
        ("Americas", ["Argentina", "Brazil", "Canada", "Mexico", "United States"]),
        ("Europe", ["European Union", "France", "Germany", "Italy", "Russia", "Turkey", "United Kingdom"]),
        ("Asia-Pacific", ["Australia", "China", "India", "Indonesia", "Israel", "Japan", "Saudi Arabia", "South Korea"]),
        ("Africa", ["South Africa"]),
    ]
    # Flat ordered list
    countries = []
    continent_ranges = []
    for continent, members in CONTINENTS:
        start = len(countries)
        countries.extend(members)
        continent_ranges.append((continent, start, len(countries)))

    # Use log scale for better color differentiation on small distances
    import math
    all_dists = []
    for host in countries:
        for origin in countries:
            if host != origin and host in distances and origin in distances[host]:
                all_dists.append(distances[host][origin])
    all_dists.sort()

    # Use percentile-based coloring for much better contrast
    def dist_color(d):
        """Color based on percentile rank among all distances."""
        # Find percentile
        idx = 0
        for i, v in enumerate(all_dists):
            if v >= d:
                idx = i
                break
        else:
            idx = len(all_dists) - 1
        ratio = idx / max(len(all_dists) - 1, 1)

        # Multi-stop gradient: deep green -> green -> yellow -> orange -> red
        if ratio < 0.25:
            t = ratio / 0.25
            r = int(0 + 80 * t)
            g = int(140 + 60 * t)
            b = int(60 - 30 * t)
        elif ratio < 0.5:
            t = (ratio - 0.25) / 0.25
            r = int(80 + 175 * t)
            g = int(200 - 10 * t)
            b = int(30 - 30 * t)
        elif ratio < 0.75:
            t = (ratio - 0.5) / 0.25
            r = 255
            g = int(190 - 100 * t)
            b = 0
        else:
            t = (ratio - 0.75) / 0.25
            r = 255
            g = int(90 - 90 * t)
            b = 0
        return f"rgb({r},{g},{b})"

    def text_color(d):
        """White text on dark backgrounds, black on light."""
        idx = 0
        for i, v in enumerate(all_dists):
            if v >= d:
                idx = i
                break
        else:
            idx = len(all_dists) - 1
        ratio = idx / max(len(all_dists) - 1, 1)
        return "#fff" if ratio < 0.2 or ratio > 0.8 else "#000"

    def flag_img(country, size=20):
        code = COUNTRY_CODES.get(country, "")
        if not code:
            return ""
        return f'<img src="https://flagcdn.com/w40/{code}.png" width="{size}" style="vertical-align:middle;border-radius:2px;">'

    # Continent colors for separator styling
    continent_colors = {
        "Americas": "#e3f2fd",
        "Europe": "#fce4ec",
        "Asia-Pacific": "#e8f5e9",
        "Africa": "#fff3e0",
    }

    # Build header row with continent grouping
    header_top = '<th colspan="1" style="position:sticky;left:0;top:0;z-index:3;background:#fff;"></th>'
    header_bottom = '<th style="position:sticky;left:0;top:28px;z-index:3;background:#f8f8f8;min-width:50px;"></th>'
    for continent, start, end in continent_ranges:
        span = end - start
        bg = continent_colors.get(continent, "#f8f8f8")
        header_top += f'<th colspan="{span}" style="position:sticky;top:0;z-index:2;background:{bg};padding:4px 6px;font-size:11px;font-weight:700;border-bottom:2px solid #999;letter-spacing:0.03em;">{continent}</th>'
    for c in countries:
        header_bottom += f'''<th style="padding:4px;font-size:9px;writing-mode:vertical-lr;text-align:left;
            white-space:nowrap;background:#f8f8f8;position:sticky;top:28px;z-index:2;min-width:38px;">
            {flag_img(c, 14)}<br>{c}</th>'''

    # Build data rows with continent separators
    rows = ""
    prev_continent = None
    for ci, (continent, start, end) in enumerate(continent_ranges):
        bg = continent_colors.get(continent, "#f8f8f8")
        # Continent separator row
        rows += f'<tr><td colspan="{len(countries)+1}" style="background:{bg};padding:3px 8px;font-size:10px;font-weight:700;letter-spacing:0.05em;color:#555;border-top:2px solid #bbb;">{continent}</td></tr>\n'
        for host in countries[start:end]:
            cells = f'<td style="position:sticky;left:0;z-index:1;background:#fafafa;padding:4px 8px;font-size:11px;white-space:nowrap;font-weight:600;border-right:2px solid #ddd;">{flag_img(host, 16)} {host}</td>'
            for oi, origin in enumerate(countries):
                # Add continent separator border
                border_left = ""
                for _, s2, _ in continent_ranges:
                    if oi == s2:
                        border_left = "border-left:2px solid #bbb;"
                        break

                if host == origin:
                    cells += f'<td style="background:#d0d0d0;{border_left}"></td>'
                elif host in distances and origin in distances[host]:
                    d = distances[host][origin]
                    bg_c = dist_color(d)
                    fg_c = text_color(d)
                    cells += f'<td style="background:{bg_c};color:{fg_c};padding:2px 4px;font-size:10px;text-align:right;white-space:nowrap;{border_left}" title="{origin} embassy → {host} power center: {d:.1f} km">{d:.0f}</td>'
                else:
                    cells += f'<td style="background:#f0f0f0;color:#999;font-size:9px;text-align:center;{border_left}">—</td>'
            rows += f"<tr>{cells}</tr>\n"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>G20 Embassy Distance Matrix</title>
<style>
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    margin: 0; padding: 20px; background: #fff;
}}
.header {{
    display: flex; align-items: center; gap: 16px; margin-bottom: 16px; flex-wrap: wrap;
}}
.header h1 {{ font-size: 20px; margin: 0; }}
.header a {{
    font-size: 13px; color: #0066cc; text-decoration: none;
    padding: 6px 14px; border: 1px solid #0066cc; border-radius: 6px;
}}
.header a:hover {{ background: #0066cc; color: #fff; }}
.legend {{
    display: flex; align-items: center; gap: 4px; font-size: 11px; color: #666; margin-left: auto;
}}
.legend-bar {{
    width: 160px; height: 14px; border-radius: 3px;
    background: linear-gradient(to right, rgb(0,140,60), rgb(80,200,30), rgb(255,190,0), rgb(255,90,0), rgb(255,0,0));
    border: 1px solid #ccc;
}}
.table-wrap {{
    overflow: auto; max-height: calc(100vh - 120px); border: 1px solid #ccc; border-radius: 8px;
}}
table {{
    border-collapse: collapse; font-size: 11px;
}}
th, td {{
    border: 1px solid #e0e0e0;
}}
th {{
    background: #f8f8f8; font-weight: 600;
}}
tr:hover td {{
    filter: brightness(0.9);
}}
.note {{
    margin-top: 12px; font-size: 11px; color: #888;
}}
</style>
</head>
<body>
<div class="header">
    <h1>G20 Embassy Distance Matrix (km)</h1>
    <a href="g20_embassy_map.html">← Back to Map</a>
    <div class="legend">
        <span>Close</span>
        <div class="legend-bar"></div>
        <span>Far</span>
    </div>
</div>
<p style="font-size:12px;color:#666;margin:0 0 12px;">
    Rows = host country (power center location). Columns = origin country (embassy).
    Each cell = distance (km) from embassy to host's power center. Grouped by continent.
</p>
<div class="table-wrap">
<table>
    <thead>
        <tr>{header_top}</tr>
        <tr>{header_bottom}</tr>
    </thead>
    <tbody>
{rows}
    </tbody>
</table>
</div>
<p class="note">Diagonal is empty (a country has no embassy in its own capital).
Colors use percentile ranking for maximum contrast. Distances computed with the Haversine formula.</p>
</body>
</html>"""
    return html


def generate_distance_table():
    """Generate a summary of all distances for console output."""
    stats = get_statistics()
    print("\n" + "=" * 70)
    print("G20 EMBASSY DISTANCE ANALYSIS")
    print("=" * 70)

    for host_country in sorted(stats.keys()):
        s = stats[host_country]
        pc = POWER_CENTERS[host_country]
        print(f"\n{FLAGS.get(host_country, '')} {host_country} ({pc['capital']})")
        print(f"  Power Center: {pc['name']}")
        print(f"  Average distance: {s['average']:.1f} km")
        print(f"  Closest: {FLAGS.get(s['closest'][0], '')} {s['closest'][0]} ({s['closest'][1]:.1f} km)")
        print(f"  Farthest: {FLAGS.get(s['farthest'][0], '')} {s['farthest'][0]} ({s['farthest'][1]:.1f} km)")
        print(f"  All embassies:")
        for country, dist in s["all_sorted"]:
            bar_len = int(dist / s["farthest"][1] * 30) if s["farthest"][1] > 0 else 0
            bar = "█" * bar_len
            print(f"    {FLAGS.get(country, '')} {country:20s} {dist:8.1f} km  {bar}")


if __name__ == "__main__":
    import os

    os.makedirs("dist", exist_ok=True)

    print("Generating G20 Embassy Distance Map...")
    embassy_map = create_map()
    embassy_map.save(OUTPUT_FILE)
    print(f"Map saved to {OUTPUT_FILE}")

    print("Generating distance matrix...")
    matrix_html = generate_distance_matrix_html()
    matrix_file = "dist/g20_distance_matrix.html"
    with open(matrix_file, "w") as f:
        f.write(matrix_html)
    print(f"Matrix saved to {matrix_file}")

    generate_distance_table()

    print(f"\nOpen {OUTPUT_FILE} in your browser to explore the interactive map.")
