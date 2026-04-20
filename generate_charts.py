"""
Generate chart images for X/Twitter — Colossal-inspired light editorial theme.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── Colossal-inspired palette ──
BG = '#FAFAF7'
WHITE = '#FFFFFF'
INK = '#1A1A1A'
INK_LIGHT = '#3D3D3D'
MUTED = '#9A9A9A'
BORDER = '#E5E2DB'
ACCENT = '#C4501A'
ACCENT_LIGHT = '#E86D2E'
TEAL = '#1A7A6D'
TEAL_LIGHT = '#2AA394'
BLUE = '#2563EB'
AMBER = '#B45309'
SAND = '#F5F2EB'

plt.rcParams.update({
    'figure.facecolor': BG,
    'axes.facecolor': WHITE,
    'axes.edgecolor': BORDER,
    'axes.labelcolor': INK_LIGHT,
    'text.color': INK,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'grid.color': BORDER,
    'grid.alpha': 0.6,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'Segoe UI', 'Arial'],
    'font.size': 12,
    'axes.titlesize': 17,
    'axes.titleweight': '600',
    'figure.dpi': 200,
    'axes.spines.top': False,
    'axes.spines.right': False,
})


def save(fig, name):
    fig.savefig(f'{name}.png', bbox_inches='tight', pad_inches=0.5, facecolor=BG)
    plt.close(fig)
    print(f'  saved {name}.png')


print("Generating charts (Colossal theme)...")

years = list(range(2025, 2126, 5))
flow_mod = [12.77,12.77,12.56,12.34,12.17,12.0,11.87,11.74,11.61,11.48,11.4,11.31,11.27,11.23,11.18,11.14,11.1,11.05,11.05,11.05,11.05]
flow_high = [12.69,12.69,12.43,12.17,11.87,11.57,11.23,10.88,10.58,10.28,10.03,9.77,9.55,9.34,9.12,8.91,8.78,8.65,8.57,8.48,8.48]

# ── CHART 1: Flow deficit ──
fig, ax = plt.subplots(figsize=(12, 6.75))

ax.axhline(y=18.3, color=ACCENT, linestyle='--', linewidth=1.5, alpha=0.4, label='Legal allocation (18.3 MAF)')
ax.axhline(y=13.2, color=AMBER, linestyle=':', linewidth=1, alpha=0.4, label='500-year average (13.2 MAF)')
ax.fill_between(years, flow_high, 18.3, alpha=0.04, color=ACCENT)
ax.plot(years, flow_mod, color=TEAL, linewidth=2.5, marker='o', markersize=3.5, label='SSP2-4.5 (moderate)', zorder=4)
ax.plot(years, flow_high, color=ACCENT, linewidth=2.5, marker='o', markersize=3.5, label='SSP5-8.5 (current trajectory)', zorder=4)
ax.fill_between(years, flow_mod, flow_high, alpha=0.06, color=ACCENT)

ax.set_title('Colorado River: What\'s Promised vs. What Exists', pad=20, loc='left')
ax.set_ylabel('Mean Annual Flow (MAF/year)', fontsize=11)
ax.set_ylim(6, 20)
ax.set_xlim(2025, 2125)
ax.legend(loc='upper right', fontsize=9.5, framealpha=0.95, facecolor=WHITE, edgecolor=BORDER)
ax.grid(True, axis='y', alpha=0.4)

ax.annotate('6.0 MAF/yr\ndeficit TODAY',
            xy=(2027, 12.7), xytext=(2042, 17),
            fontsize=13, fontweight='bold', color=ACCENT,
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.4', facecolor=WHITE, edgecolor=ACCENT, alpha=0.95))

ax.text(0.5, -0.1, 'Sources: Udall & Overpeck 2017, CMIP6  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=7.5, color=MUTED)
save(fig, 'chart1_flow_deficit')

# ── CHART 2: Drought probability ──
fig, ax = plt.subplots(figsize=(12, 6.75))
windows = ['10yr\n(2035)', '25yr\n(2050)', '50yr\n(2075)', '75yr\n(2100)', '100yr\n(2125)']
prob_mod = [29.0, 59.4, 86.5, 96.0, 98.9]
prob_high = [33.5, 68.2, 94.3, 99.3, 99.9]
x = np.arange(len(windows))
w = 0.32

bars1 = ax.bar(x - w/2, prob_mod, w, color=TEAL, label='SSP2-4.5 (moderate)', edgecolor='none', alpha=0.85, zorder=3)
bars2 = ax.bar(x + w/2, prob_high, w, color=ACCENT, label='SSP5-8.5 (current trajectory)', edgecolor='none', alpha=0.85, zorder=3)
ax.axhline(y=50, color=AMBER, linestyle='--', linewidth=1, alpha=0.4, label='50% threshold')

for bar in bars1:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.8, f'{h:.0f}%', ha='center', fontsize=8.5, fontweight='600', color=TEAL)
for bar in bars2:
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h + 1.8, f'{h:.0f}%', ha='center', fontsize=8.5, fontweight='600', color=ACCENT)

ax.set_title('Probability of Major Drought in the American West', pad=20, loc='left')
ax.set_ylabel('Cumulative Probability (%)', fontsize=11)
ax.set_ylim(0, 115)
ax.set_xticks(x)
ax.set_xticklabels(windows)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.95, facecolor=WHITE, edgecolor=BORDER)
ax.grid(True, axis='y', alpha=0.4)
ax.text(0.5, -0.13, 'Cook et al. 2015, Ault et al. 2016, CMIP6  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=7.5, color=MUTED)
save(fig, 'chart2_drought_probability')

# ── CHART 3: Gap analysis ──
fig, ax = plt.subplots(figsize=(12, 6.75))
gap_years = [2025, 2035, 2050, 2075, 2100, 2125]
deficit_high = [5.61, 6.06, 7.19, 8.84, 10.76, 11.65]
deficit_mod = [5.53, 5.93, 6.76, 7.64, 8.53, 9.08]
drought_proof = [0.85, 1.1, 1.5, 1.8, 2.0, 2.1]
wet_year = [2.1, 2.8, 3.5, 4.0, 4.3, 4.5]

ax.fill_between(gap_years, deficit_high, wet_year, alpha=0.06, color=ACCENT)
ax.fill_between(gap_years, wet_year, drought_proof, alpha=0.04, color=AMBER)
ax.fill_between(gap_years, drought_proof, 0, alpha=0.08, color=TEAL)

ax.plot(gap_years, deficit_high, color=ACCENT, linewidth=2.5, marker='s', markersize=6, label='Deficit (high emissions)', zorder=5)
ax.plot(gap_years, deficit_mod, color=AMBER, linewidth=1.5, marker='s', markersize=4, label='Deficit (moderate)', linestyle='--', zorder=4)
ax.plot(gap_years, wet_year, color=BLUE, linewidth=2, marker='o', markersize=5, label='Capacity (wet years)', zorder=5)
ax.plot(gap_years, drought_proof, color=TEAL, linewidth=2.5, marker='o', markersize=6, label='Capacity (drought-proof)', zorder=5)

ax.set_title('The Gap: What We Need vs. What We Have', pad=20, loc='left')
ax.set_ylabel('Million Acre-Feet / Year', fontsize=11)
ax.set_ylim(0, 13)
ax.set_xlim(2023, 2127)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.95, facecolor=WHITE, edgecolor=BORDER)
ax.grid(True, axis='y', alpha=0.4)

ax.text(2075, 5.5, 'THE GAP', fontsize=22, fontweight='bold', color=ACCENT, alpha=0.15, ha='center', va='center')
ax.text(0.5, -0.1, 'All active MAR, recycling, desal, conservation  |  kirkwarren.github.io/water-scarcity-west',
        transform=ax.transAxes, ha='center', fontsize=7.5, color=MUTED)
save(fig, 'chart3_gap_analysis')

# ── CHART 4: Technology cost ──
fig, ax = plt.subplots(figsize=(12, 6.75))
techs = ['Atmospheric Water Gen','Rainwater Harvesting','Seawater Desal',
         'Water Recycling (IPR)','Stormwater Capture','Brackish Desal','Managed Aquifer\nRecharge']
cost_low = [3000, 3000, 1800, 1000, 500, 500, 150]
cost_high = [10000, 8000, 2500, 1800, 1500, 1200, 500]
cost_range = [h - l for h, l in zip(cost_high, cost_low)]
colors = [MUTED, MUTED, BLUE, TEAL, BLUE, BLUE, TEAL]
range_c = [MUTED+'40', MUTED+'40', BLUE+'40', TEAL+'40', BLUE+'40', BLUE+'40', TEAL+'40']

ax.barh(techs, cost_low, color=colors, edgecolor='none', alpha=0.8, zorder=3, height=0.55)
ax.barh(techs, cost_range, left=cost_low, color=range_c, edgecolor='none', zorder=3, height=0.55)

for i, (lo, hi) in enumerate(zip(cost_low, cost_high)):
    ax.text(hi + 200, i, f'${lo:,}\u2013${hi:,}', va='center', fontsize=9, color=INK_LIGHT)

ax.set_title('Cost per Acre-Foot by Technology', pad=20, loc='left')
ax.set_xlabel('Cost ($/acre-foot)', fontsize=11)
ax.set_xlim(0, 13000)
ax.grid(True, axis='x', alpha=0.4)
ax.invert_yaxis()

ax.axhline(y=4.5, color=BORDER, linewidth=0.5)
ax.text(11500, 5.5, 'PROVEN\nAT SCALE', ha='center', fontsize=8, fontweight='bold', color=TEAL, alpha=0.5)
ax.text(11500, 0.8, 'LIMITED\nVIABILITY', ha='center', fontsize=8, fontweight='bold', color=MUTED, alpha=0.5)

ax.text(0.5, -0.08, 'kirkwarren.github.io/water-scarcity-west', transform=ax.transAxes, ha='center', fontsize=7.5, color=MUTED)
save(fig, 'chart4_technology_cost')

print("\nDone.")
