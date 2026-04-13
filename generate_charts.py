"""
Generate static chart images for X/Twitter posts.
Uses matplotlib with a dark theme matching the website aesthetic.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ============================================================
# THEME (matches website dark theme)
# ============================================================
BG = '#0a0e17'
SURFACE = '#111827'
TEXT = '#e2e8f0'
MUTED = '#6b7f99'
GRID = '#1e3a5f'
RED = '#ef4444'
BLUE = '#3b82f6'
AMBER = '#f59e0b'
GREEN = '#10b981'
CYAN = '#06b6d4'

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': SURFACE,
    'axes.edgecolor': GRID,
    'axes.labelcolor': TEXT,
    'text.color': TEXT,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'grid.color': GRID,
    'grid.alpha': 0.4,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'Arial', 'Helvetica'],
    'font.size': 13,
    'axes.titlesize': 18,
    'axes.titleweight': 'bold',
    'figure.dpi': 200,
})


def save(fig, name):
    fig.savefig(f'{name}.png', bbox_inches='tight', pad_inches=0.4, facecolor=BG)
    plt.close(fig)
    print(f'  Saved {name}.png')


# ============================================================
# CHART 1: Colorado River Flow vs Allocation
# For Post 1 — "The deficit is today"
# ============================================================
print("Generating charts...")

years = list(range(2025, 2126, 5))
flow_mod = [12.77,12.77,12.56,12.34,12.17,12.0,11.87,11.74,11.61,11.48,11.4,11.31,11.27,11.23,11.18,11.14,11.1,11.05,11.05,11.05,11.05]
flow_high = [12.69,12.69,12.43,12.17,11.87,11.57,11.23,10.88,10.58,10.28,10.03,9.77,9.55,9.34,9.12,8.91,8.78,8.65,8.57,8.48,8.48]

fig, ax = plt.subplots(figsize=(12, 6.75))  # 16:9 ratio

ax.axhline(y=18.3, color=RED, linestyle='--', linewidth=2, alpha=0.7, label='Legal allocation (18.3 MAF)')
ax.axhline(y=13.2, color=AMBER, linestyle=':', linewidth=1.5, alpha=0.5, label='500-year average (13.2 MAF)')
ax.fill_between(years, flow_high, 18.3, alpha=0.08, color=RED)
ax.plot(years, flow_mod, color=BLUE, linewidth=2.5, marker='o', markersize=4, label='SSP2-4.5 (moderate)')
ax.plot(years, flow_high, color=RED, linewidth=2.5, marker='o', markersize=4, label='SSP5-8.5 (current trajectory)')

ax.fill_between(years, flow_mod, flow_high, alpha=0.12, color=RED)

ax.set_title('Colorado River: What\'s Promised vs. What Exists', pad=16)
ax.set_ylabel('Mean Annual Flow (MAF/year)')
ax.set_ylim(6, 20)
ax.set_xlim(2025, 2125)
ax.legend(loc='upper right', fontsize=10, framealpha=0.8, facecolor=SURFACE, edgecolor=GRID)
ax.grid(True, alpha=0.3)

# Annotate the gap
ax.annotate('6.0 MAF/yr\ndeficit TODAY',
            xy=(2025, 12.7), xytext=(2038, 16.5),
            fontsize=14, fontweight='bold', color=RED,
            arrowprops=dict(arrowstyle='->', color=RED, lw=2),
            bbox=dict(boxstyle='round,pad=0.4', facecolor=BG, edgecolor=RED, alpha=0.9))

ax.text(0.5, -0.12, 'Sources: Udall & Overpeck 2017, CMIP6 projections  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=8, color=MUTED)

save(fig, 'chart1_flow_deficit')


# ============================================================
# CHART 2: Drought Probability
# For Post 2 — "The probability numbers"
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6.75))

windows = ['10yr\n(2035)', '25yr\n(2050)', '50yr\n(2075)', '75yr\n(2100)', '100yr\n(2125)']
prob_mod = [29.0, 59.4, 86.5, 96.0, 98.9]
prob_high = [33.5, 68.2, 94.3, 99.3, 99.9]

x = np.arange(len(windows))
w = 0.35

bars1 = ax.bar(x - w/2, prob_mod, w, color=BLUE, label='SSP2-4.5 (moderate)', edgecolor='none', alpha=0.85, zorder=3)
bars2 = ax.bar(x + w/2, prob_high, w, color=RED, label='SSP5-8.5 (current trajectory)', edgecolor='none', alpha=0.85, zorder=3)

ax.axhline(y=50, color=AMBER, linestyle='--', linewidth=1.5, alpha=0.5, label='50% threshold')

# Value labels on bars
for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f'{h:.0f}%',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=BLUE)
for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.5, f'{h:.0f}%',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=RED)

ax.set_title('Probability of Major Drought in the American West', pad=16)
ax.set_ylabel('Cumulative Probability (%)')
ax.set_ylim(0, 115)
ax.set_xticks(x)
ax.set_xticklabels(windows)
ax.legend(loc='upper left', fontsize=10, framealpha=0.8, facecolor=SURFACE, edgecolor=GRID)
ax.grid(True, axis='y', alpha=0.3)

ax.text(0.5, -0.15, 'Based on: Cook et al. 2015, Ault et al. 2016, CMIP6 ensemble  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=8, color=MUTED)

save(fig, 'chart2_drought_probability')


# ============================================================
# CHART 3: Gap Analysis — Current efforts vs deficit
# For Post 3 — "Good news / bad news"
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6.75))

gap_years = [2025, 2035, 2050, 2075, 2100, 2125]
deficit_high = [5.61, 6.06, 7.19, 8.84, 10.76, 11.65]
deficit_mod = [5.53, 5.93, 6.76, 7.64, 8.53, 9.08]
drought_proof = [0.85, 1.1, 1.5, 1.8, 2.0, 2.1]
wet_year = [2.1, 2.8, 3.5, 4.0, 4.3, 4.5]

ax.fill_between(gap_years, deficit_high, wet_year, alpha=0.12, color=RED, label='_nolegend_')
ax.fill_between(gap_years, wet_year, drought_proof, alpha=0.08, color=AMBER, label='_nolegend_')
ax.fill_between(gap_years, drought_proof, 0, alpha=0.15, color=GREEN, label='_nolegend_')

ax.plot(gap_years, deficit_high, color=RED, linewidth=3, marker='s', markersize=7, label='Deficit (high emissions)', zorder=5)
ax.plot(gap_years, deficit_mod, color=AMBER, linewidth=2, marker='s', markersize=5, label='Deficit (moderate)', linestyle='--', zorder=4)
ax.plot(gap_years, wet_year, color=BLUE, linewidth=2.5, marker='o', markersize=6, label='Capacity (wet years)', zorder=5)
ax.plot(gap_years, drought_proof, color=GREEN, linewidth=3, marker='o', markersize=7, label='Capacity (drought-proof)', zorder=5)

ax.set_title('The Gap: What We Need vs. What We Have', pad=16)
ax.set_ylabel('Million Acre-Feet / Year')
ax.set_ylim(0, 13)
ax.set_xlim(2023, 2127)
ax.legend(loc='upper left', fontsize=10, framealpha=0.8, facecolor=SURFACE, edgecolor=GRID)
ax.grid(True, alpha=0.3)

# Annotate the gap
ax.annotate('THE GAP',
            xy=(2075, 5.3), fontsize=20, fontweight='bold', color=RED, alpha=0.4,
            ha='center', va='center')

ax.text(0.5, -0.12, 'Includes all active MAR, recycling, desal, conservation programs  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=8, color=MUTED)

save(fig, 'chart3_gap_analysis')


# ============================================================
# CHART 4: Technology cost comparison (horizontal bar)
# For Post 4 — "Solutions exist"
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6.75))

techs = [
    'Atmospheric Water Gen',
    'Rainwater Harvesting',
    'Seawater Desal',
    'Water Recycling (IPR)',
    'Stormwater Capture',
    'Brackish Desal',
    'Managed Aquifer\nRecharge',
]
cost_low = [3000, 3000, 1800, 1000, 500, 500, 150]
cost_high = [10000, 8000, 2500, 1800, 1500, 1200, 500]
cost_range = [h - l for h, l in zip(cost_high, cost_low)]

colors = [MUTED, MUTED, BLUE, GREEN, BLUE, BLUE, GREEN]
range_colors = ['#4a5568', '#4a5568', '#2563eb50', '#05966950', '#2563eb50', '#2563eb50', '#059669']

bars = ax.barh(techs, cost_low, color=colors, edgecolor='none', alpha=0.8, zorder=3, height=0.6)
ax.barh(techs, cost_range, left=cost_low, color=range_colors, edgecolor='none', alpha=0.4, zorder=3, height=0.6)

# Value labels
for i, (lo, hi) in enumerate(zip(cost_low, cost_high)):
    ax.text(hi + 150, i, f'${lo:,}–${hi:,}', va='center', fontsize=9, color=TEXT)

# Highlight MAR
bars[6].set_edgecolor(GREEN)
bars[6].set_linewidth(2)

ax.set_title('Cost per Acre-Foot by Technology', pad=16)
ax.set_xlabel('Cost ($/acre-foot)')
ax.set_xlim(0, 13000)
ax.grid(True, axis='x', alpha=0.3)
ax.invert_yaxis()

# Label proven vs unproven
ax.axhline(y=4.5, color=GRID, linestyle='-', linewidth=0.5, alpha=0.5)
ax.text(11000, 5.5, 'PROVEN\nAT SCALE', ha='center', fontsize=9, fontweight='bold', color=GREEN, alpha=0.6)
ax.text(11000, 0.5, 'LIMITED\nVIABILITY', ha='center', fontsize=9, fontweight='bold', color=MUTED, alpha=0.6)

ax.text(0.5, -0.1, 'Full analysis + interactive charts  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=8, color=MUTED)

save(fig, 'chart4_technology_cost')

print("\nAll charts generated. Attach to X posts:")
print("  Post 1 → chart1_flow_deficit.png")
print("  Post 2 → chart2_drought_probability.png")
print("  Post 3 → chart3_gap_analysis.png")
print("  Post 4 → chart4_technology_cost.png")
