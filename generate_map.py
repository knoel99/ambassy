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


def create_map():
    """Create the interactive G20 embassy distance map."""
    # Base map centered on the world
    m = folium.Map(
        location=[20, 0],
        zoom_start=3,
        tiles="CartoDB positron",
        control_scale=True,
    )

    distances = compute_distances()
    stats = get_statistics()

    # Create a feature group for each host country
    for host_country, host_info in POWER_CENTERS.items():
        fg = folium.FeatureGroup(name=f"{FLAGS.get(host_country, '')} {host_country}", show=False)

        pc_lat = host_info["lat"]
        pc_lon = host_info["lon"]

        # Add power center marker (star icon)
        power_center_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 280px;">
            <h3 style="margin:0 0 8px; color:#333; border-bottom: 2px solid #e74c3c;">
                {FLAGS.get(host_country, '')} {host_country}
            </h3>
            <p style="margin:4px 0;"><strong>Power Center:</strong> {host_info['name']}</p>
            <p style="margin:4px 0;"><strong>Capital:</strong> {host_info['capital']}</p>
            <p style="margin:4px 0;"><strong>Coordinates:</strong> {pc_lat:.4f}, {pc_lon:.4f}</p>
            <hr style="margin:8px 0;">
            <p style="margin:4px 0; font-size:0.9em;">
                <strong>Avg. embassy distance:</strong> {stats[host_country]['average']:.1f} km<br>
                <strong>Closest embassy:</strong> {FLAGS.get(stats[host_country]['closest'][0], '')}
                {stats[host_country]['closest'][0]} ({stats[host_country]['closest'][1]:.1f} km)<br>
                <strong>Farthest embassy:</strong> {FLAGS.get(stats[host_country]['farthest'][0], '')}
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

        # Add embassy markers and distance lines
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

                # Embassy marker popup
                embassy_html = f"""
                <div style="font-family: Arial, sans-serif; min-width: 250px;">
                    <h4 style="margin:0 0 6px; color:#333;">
                        {FLAGS.get(origin_country, '')} Embassy of {origin_country}
                    </h4>
                    <p style="margin:4px 0;">
                        <strong>Host:</strong> {FLAGS.get(host_country, '')} {host_country} ({host_info['capital']})
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

                # Embassy marker
                folium.CircleMarker(
                    location=[e_lat, e_lon],
                    radius=7,
                    color=COUNTRY_COLORS.get(origin_country, "#333"),
                    fill=True,
                    fill_color=COUNTRY_COLORS.get(origin_country, "#333"),
                    fill_opacity=0.8,
                    popup=folium.Popup(embassy_html, max_width=300),
                    tooltip=f"{FLAGS.get(origin_country, '')} {origin_country} - {dist_km:.1f} km",
                ).add_to(fg)

                # Distance line from embassy to power center
                folium.PolyLine(
                    locations=[[e_lat, e_lon], [pc_lat, pc_lon]],
                    color=line_color,
                    weight=2,
                    opacity=0.6,
                    dash_array="5 5",
                    tooltip=f"{origin_country} → {host_info['name']}: {dist_km:.1f} km",
                ).add_to(fg)

        fg.add_to(m)

    # Add an "Overview" layer with all power centers visible by default
    overview = folium.FeatureGroup(name="Overview: All Power Centers", show=True)
    for country, info in POWER_CENTERS.items():
        folium.Marker(
            location=[info["lat"], info["lon"]],
            tooltip=f"{FLAGS.get(country, '')} {country}: {info['name']}",
            icon=folium.Icon(color="darkred", icon="university", prefix="fa"),
        ).add_to(overview)
    overview.add_to(m)

    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)

    # Add a custom legend / info panel
    legend_html = _build_legend_html(stats)
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add fullscreen plugin
    plugins.Fullscreen().add_to(m)

    return m


def _build_legend_html(stats):
    """Build the HTML for the info panel / legend."""
    # Build the ranking table
    all_avg_distances = []
    for host, st in stats.items():
        all_avg_distances.append((host, st["average"]))
    all_avg_distances.sort(key=lambda x: x[1])

    ranking_rows = ""
    for i, (country, avg) in enumerate(all_avg_distances, 1):
        ranking_rows += f"""
        <tr>
            <td style="padding:2px 6px;">{i}</td>
            <td style="padding:2px 6px;">{FLAGS.get(country, '')} {country}</td>
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
            Use the layer control (top right) to explore each country.
        </p>
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
                    <span style="display:inline-block;width:12px;height:12px;
                    border-radius:50%;background:#555;"></span> Embassy location
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

    generate_distance_table()

    print(f"\nOpen {OUTPUT_FILE} in your browser to explore the interactive map.")
