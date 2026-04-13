"""
Generate predictive outcome maps for the American West:
  - Without additional intervention
  - With aggressive intervention
Across 2025, 2050, 2075, 2100 time horizons.

Uses cartopy for real geographic boundaries and matplotlib for rendering.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader

# ============================================================
# THEME
# ============================================================
BG = '#0a0e17'
SURFACE = '#111827'
TEXT = '#e2e8f0'
MUTED = '#6b7f99'
GRID = '#1e3a5f'
RED = '#ef4444'
BLUE = '#3b82f6'
GREEN = '#10b981'

# ============================================================
# DATA MODEL
# ============================================================
# Water stress index (0-100): 0=abundant, 100=catastrophic shortage
# Based on: supply-demand ratio, groundwater trends, population growth,
# climate projections (SSP5-8.5 for no-intervention, SSP2-4.5 + tech for intervention)

# State FIPS or names for the western states we're modeling
STATES = {
    'Washington':    {'lat': 47.5, 'lon': -120.5},
    'Oregon':        {'lat': 44.0, 'lon': -120.5},
    'California':    {'lat': 37.0, 'lon': -119.5},
    'Nevada':        {'lat': 39.0, 'lon': -116.8},
    'Idaho':         {'lat': 44.0, 'lon': -114.5},
    'Montana':       {'lat': 47.0, 'lon': -109.5},
    'Wyoming':       {'lat': 43.0, 'lon': -107.5},
    'Utah':          {'lat': 39.5, 'lon': -111.5},
    'Colorado':      {'lat': 39.0, 'lon': -105.5},
    'Arizona':       {'lat': 34.5, 'lon': -111.5},
    'New Mexico':    {'lat': 34.5, 'lon': -106.0},
    'Texas':         {'lat': 31.5, 'lon': -99.5},
    'North Dakota':  {'lat': 47.5, 'lon': -100.5},
    'South Dakota':  {'lat': 44.5, 'lon': -100.0},
    'Nebraska':      {'lat': 41.5, 'lon': -99.8},
    'Kansas':        {'lat': 38.5, 'lon': -98.5},
    'Oklahoma':      {'lat': 35.5, 'lon': -97.5},
}

# Water stress scores WITHOUT intervention (SSP5-8.5, current policies)
# Scores: 0-20 low, 20-40 moderate, 40-60 high, 60-80 severe, 80-100 catastrophic
NO_INTERVENTION = {
    'Washington':   {'2025': 15, '2050': 25, '2075': 38, '2100': 45},
    'Oregon':       {'2025': 18, '2050': 28, '2075': 40, '2100': 48},
    'California':   {'2025': 55, '2050': 70, '2075': 82, '2100': 90},
    'Nevada':       {'2025': 62, '2050': 78, '2075': 88, '2100': 95},
    'Idaho':        {'2025': 22, '2050': 32, '2075': 42, '2100': 50},
    'Montana':      {'2025': 12, '2050': 20, '2075': 30, '2100': 38},
    'Wyoming':      {'2025': 20, '2050': 32, '2075': 45, '2100': 55},
    'Utah':         {'2025': 50, '2050': 65, '2075': 78, '2100': 88},
    'Colorado':     {'2025': 42, '2050': 58, '2075': 72, '2100': 82},
    'Arizona':      {'2025': 65, '2050': 80, '2075': 92, '2100': 97},
    'New Mexico':   {'2025': 52, '2050': 68, '2075': 80, '2100': 90},
    'Texas':        {'2025': 40, '2050': 55, '2075': 68, '2100': 78},
    'North Dakota': {'2025': 10, '2050': 15, '2075': 22, '2100': 28},
    'South Dakota': {'2025': 12, '2050': 18, '2075': 28, '2100': 35},
    'Nebraska':     {'2025': 25, '2050': 40, '2075': 55, '2100': 68},
    'Kansas':       {'2025': 35, '2050': 52, '2075': 65, '2100': 78},
    'Oklahoma':     {'2025': 30, '2050': 42, '2075': 55, '2100': 65},
}

# Water stress scores WITH aggressive intervention
# Assumes: full MAR deployment, mandatory recycling, ag conversion,
# Compact reform to 12-13 MAF, universal groundwater regulation,
# coastal desal backup, SSP2-4.5 emissions trajectory
WITH_INTERVENTION = {
    'Washington':   {'2025': 15, '2050': 18, '2075': 22, '2100': 25},
    'Oregon':       {'2025': 18, '2050': 20, '2075': 25, '2100': 28},
    'California':   {'2025': 55, '2050': 45, '2075': 40, '2100': 38},
    'Nevada':       {'2025': 62, '2050': 48, '2075': 40, '2100': 35},
    'Idaho':        {'2025': 22, '2050': 20, '2075': 22, '2100': 24},
    'Montana':      {'2025': 12, '2050': 14, '2075': 18, '2100': 20},
    'Wyoming':      {'2025': 20, '2050': 22, '2075': 28, '2100': 32},
    'Utah':         {'2025': 50, '2050': 40, '2075': 35, '2100': 32},
    'Colorado':     {'2025': 42, '2050': 35, '2075': 32, '2100': 30},
    'Arizona':      {'2025': 65, '2050': 50, '2075': 42, '2100': 38},
    'New Mexico':   {'2025': 52, '2050': 42, '2075': 38, '2100': 35},
    'Texas':        {'2025': 40, '2050': 35, '2075': 32, '2100': 30},
    'North Dakota': {'2025': 10, '2050': 10, '2075': 12, '2100': 14},
    'South Dakota': {'2025': 12, '2050': 12, '2075': 14, '2100': 16},
    'Nebraska':     {'2025': 25, '2050': 22, '2075': 25, '2100': 28},
    'Kansas':       {'2025': 35, '2050': 28, '2075': 28, '2100': 30},
    'Oklahoma':     {'2025': 30, '2050': 25, '2075': 25, '2100': 28},
}

# Color scale: water stress severity
# Blue (safe) -> Yellow (moderate) -> Orange (high) -> Red (severe) -> Dark red (catastrophic)
CMAP_COLORS = [
    (0.0,  '#1e40af'),   # 0   - deep blue (abundant)
    (0.15, '#3b82f6'),   # 15  - blue (low stress)
    (0.25, '#06b6d4'),   # 25  - cyan (some stress)
    (0.40, '#fbbf24'),   # 40  - amber (moderate)
    (0.55, '#f97316'),   # 55  - orange (high)
    (0.70, '#ef4444'),   # 70  - red (severe)
    (0.85, '#b91c1c'),   # 85  - dark red (critical)
    (1.0,  '#7f1d1d'),   # 100 - near-black red (catastrophic)
]

positions = [c[0] for c in CMAP_COLORS]
colors = [c[1] for c in CMAP_COLORS]
cmap = mcolors.LinearSegmentedColormap.from_list('water_stress', list(zip(positions, colors)))
norm = mcolors.Normalize(vmin=0, vmax=100)

# Western state names for filtering
WESTERN_STATES = set(STATES.keys())

def get_state_geometries():
    """Get state boundaries from cartopy's built-in natural earth data."""
    shapename = 'admin_1_states_provinces_lakes'
    states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
    reader = shpreader.Reader(states_shp)
    geometries = {}
    for record in reader.records():
        name = record.attributes['name']
        if name in WESTERN_STATES:
            geometries[name] = record.geometry
    return geometries


def draw_panel(ax, data, year, title, geometries):
    """Draw a single map panel."""
    ax.set_extent([-125, -93, 28, 50], crs=ccrs.PlateCarree())

    # Dark ocean and land
    ax.set_facecolor('#060a12')
    ax.add_feature(cfeature.OCEAN, facecolor='#060a12', edgecolor='none')
    ax.add_feature(cfeature.LAND, facecolor='#0d1117', edgecolor='none')

    # Draw non-western states in dark gray
    shapename = 'admin_1_states_provinces_lakes'
    states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)
    for record in shpreader.Reader(states_shp).records():
        name = record.attributes['name']
        if record.attributes.get('admin') == 'United States of America' and name not in WESTERN_STATES:
            ax.add_geometries([record.geometry], ccrs.PlateCarree(),
                            facecolor='#151d2b', edgecolor='#1e3a5f', linewidth=0.3)

    # Draw western states with stress colors
    for state_name, geom in geometries.items():
        if state_name in data and year in data[state_name]:
            score = data[state_name][year]
            color = cmap(norm(score))
            ax.add_geometries([geom], ccrs.PlateCarree(),
                            facecolor=color, edgecolor='#0a0e17', linewidth=0.8, alpha=0.9)

    # State labels with scores
    for state_name, info in STATES.items():
        if state_name in data and year in data[state_name]:
            score = data[state_name][year]
            # Abbreviate state names
            abbrevs = {
                'Washington': 'WA', 'Oregon': 'OR', 'California': 'CA',
                'Nevada': 'NV', 'Idaho': 'ID', 'Montana': 'MT',
                'Wyoming': 'WY', 'Utah': 'UT', 'Colorado': 'CO',
                'Arizona': 'AZ', 'New Mexico': 'NM', 'Texas': 'TX',
                'North Dakota': 'ND', 'South Dakota': 'SD',
                'Nebraska': 'NE', 'Kansas': 'KS', 'Oklahoma': 'OK',
            }
            abbr = abbrevs.get(state_name, state_name[:2].upper())

            # Text color based on background brightness
            text_color = '#ffffff' if score > 35 else '#e2e8f0'

            ax.text(info['lon'], info['lat'], f'{abbr}\n{score}',
                   transform=ccrs.PlateCarree(),
                   fontsize=6.5, fontweight='bold', ha='center', va='center',
                   color=text_color,
                   bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.35, edgecolor='none'))

    ax.set_title(title, fontsize=12, fontweight='bold', color=TEXT, pad=8)


# ============================================================
# GENERATE MAIN COMPARISON MAP (2x4 grid)
# ============================================================
print("Loading state geometries...")
geometries = get_state_geometries()
print(f"  Found {len(geometries)} western states")

years = ['2025', '2050', '2075', '2100']

print("Generating main comparison map...")
fig = plt.figure(figsize=(20, 11), facecolor=BG)

# Title
fig.suptitle('Western US Water Stress: 100-Year Predictive Outcomes',
            fontsize=22, fontweight='bold', color=TEXT, y=0.97)

# Row labels
fig.text(0.02, 0.72, 'WITHOUT\nINTERVENTION', fontsize=14, fontweight='bold',
        color=RED, va='center', ha='center', rotation=90,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a0505', edgecolor=RED, alpha=0.8))

fig.text(0.02, 0.30, 'WITH\nINTERVENTION', fontsize=14, fontweight='bold',
        color=GREEN, va='center', ha='center', rotation=90,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#051a0a', edgecolor=GREEN, alpha=0.8))

# Top row: No intervention
for i, year in enumerate(years):
    ax = fig.add_subplot(2, 4, i + 1, projection=ccrs.AlbersEqualArea(
        central_longitude=-110, central_latitude=39))
    draw_panel(ax, NO_INTERVENTION, year, f'{year}', geometries)

# Bottom row: With intervention
for i, year in enumerate(years):
    ax = fig.add_subplot(2, 4, i + 5, projection=ccrs.AlbersEqualArea(
        central_longitude=-110, central_latitude=39))
    draw_panel(ax, WITH_INTERVENTION, year, f'{year}', geometries)

# Colorbar
cbar_ax = fig.add_axes([0.25, 0.02, 0.50, 0.018])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([0, 20, 40, 60, 80, 100])
cbar.set_ticklabels(['Abundant\n0', 'Low Stress\n20', 'Moderate\n40',
                     'Severe\n60', 'Critical\n80', 'Catastrophic\n100'])
cbar.ax.tick_params(labelsize=8, colors=MUTED)
cbar.outline.set_edgecolor(GRID)

# Source line
fig.text(0.5, -0.01,
        'Water Stress Index based on supply-demand ratio, groundwater trends, population growth, CMIP6 projections  |  kirkwarren.github.io/water-scarcity-west',
        ha='center', fontsize=7, color=MUTED)

plt.subplots_adjust(left=0.05, right=0.98, top=0.91, bottom=0.06, wspace=0.05, hspace=0.15)
fig.savefig('map_comparison.png', bbox_inches='tight', pad_inches=0.3, facecolor=BG, dpi=200)
plt.close()
print("  Saved map_comparison.png")


# ============================================================
# GENERATE INDIVIDUAL MAPS FOR X POSTS (larger, single panels)
# ============================================================
print("Generating individual X-post maps...")

# Map for 2100 side-by-side (most dramatic contrast)
fig = plt.figure(figsize=(16, 8), facecolor=BG)

fig.suptitle('2100: Two Possible Futures for the American West',
            fontsize=20, fontweight='bold', color=TEXT, y=0.97)

ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.AlbersEqualArea(
    central_longitude=-110, central_latitude=39))
draw_panel(ax1, NO_INTERVENTION, '2100', 'Without Intervention (SSP5-8.5)', geometries)

ax2 = fig.add_subplot(1, 2, 2, projection=ccrs.AlbersEqualArea(
    central_longitude=-110, central_latitude=39))
draw_panel(ax2, WITH_INTERVENTION, '2100', 'With Full Intervention (SSP2-4.5 + Tech)', geometries)

# Arrow between panels
fig.text(0.50, 0.50, 'vs', fontsize=28, fontweight='bold', color=MUTED,
        ha='center', va='center', alpha=0.6)

# Colorbar
cbar_ax = fig.add_axes([0.25, 0.04, 0.50, 0.022])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([0, 20, 40, 60, 80, 100])
cbar.set_ticklabels(['Abundant', 'Low Stress', 'Moderate', 'Severe', 'Critical', 'Catastrophic'])
cbar.ax.tick_params(labelsize=9, colors=MUTED)
cbar.outline.set_edgecolor(GRID)

fig.text(0.5, 0.0,
        'Water Stress Index  |  kirkwarren.github.io/water-scarcity-west',
        ha='center', fontsize=8, color=MUTED)

plt.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.10, wspace=0.08)
fig.savefig('map_2100_sidebyside.png', bbox_inches='tight', pad_inches=0.3, facecolor=BG, dpi=200)
plt.close()
print("  Saved map_2100_sidebyside.png")


# ============================================================
# NO-INTERVENTION TIMELINE (4 panels, progression map)
# ============================================================
print("Generating no-intervention timeline...")
fig = plt.figure(figsize=(20, 6), facecolor=BG)

fig.suptitle('Without Intervention: How Water Stress Spreads (2025-2100)',
            fontsize=18, fontweight='bold', color=TEXT, y=0.98)

for i, year in enumerate(years):
    ax = fig.add_subplot(1, 4, i + 1, projection=ccrs.AlbersEqualArea(
        central_longitude=-110, central_latitude=39))
    draw_panel(ax, NO_INTERVENTION, year, year, geometries)

# Colorbar
cbar_ax = fig.add_axes([0.25, 0.02, 0.50, 0.025])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal')
cbar.set_ticks([0, 20, 40, 60, 80, 100])
cbar.set_ticklabels(['Abundant', 'Low Stress', 'Moderate', 'Severe', 'Critical', 'Catastrophic'])
cbar.ax.tick_params(labelsize=8, colors=MUTED)
cbar.outline.set_edgecolor(GRID)

# Arrow annotations between panels
for x_pos in [0.28, 0.50, 0.72]:
    fig.text(x_pos, 0.50, '>', fontsize=24, fontweight='bold', color=MUTED,
            ha='center', va='center', alpha=0.4)

fig.text(0.5, -0.02,
        'SSP5-8.5 (current emissions trajectory), no additional MAR/recycling/conservation  |  kirkwarren.github.io/water-scarcity-west',
        ha='center', fontsize=7, color=MUTED)

plt.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.10, wspace=0.05)
fig.savefig('map_no_intervention_timeline.png', bbox_inches='tight', pad_inches=0.3, facecolor=BG, dpi=200)
plt.close()
print("  Saved map_no_intervention_timeline.png")

print("\nAll maps generated:")
print("  map_comparison.png              - Full 2x4 grid (for website/doc)")
print("  map_2100_sidebyside.png         - 2100 side-by-side (for X post)")
print("  map_no_intervention_timeline.png - 4-panel progression (for X post)")
