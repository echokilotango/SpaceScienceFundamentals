"""
Hertzsprung-Russell Diagram v4
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.patheffects as pe

named_stars = [
    ("Sun",           5778,    1.00,       160,  "#FFF200"),
    ("Sirius A",      9940,    25.40,      150,  "#B0C8FF"),
    ("Vega",          9602,    40.12,      150,  "#C8D8FF"),
    ("Procyon A",     6530,    7.00,       130,  "#FFE880"),
    ("α Cen A",       5790,    1.52,       130,  "#FFE45E"),
    ("61 Cyg A",      4526,    0.153,      110,  "#FFA040"),
    ("Proxima Cen",   3042,    0.00155,    110,  "#FF4500"),
    ("Barnard's St",  3134,    0.00350,    110,  "#FF5500"),
    ("Betelgeuse",    3500,    126000.0,   200,  "#FF3300"),
    ("Antares",       3570,    57500.0,    190,  "#FF4411"),
    ("Aldebaran",     3910,    518.0,      160,  "#FF6633"),
    ("Arcturus",      4286,    170.0,      150,  "#FF8C00"),
    ("Capella Aa",    4970,    78.7,       140,  "#FFAA33"),
    ("Pollux",        4865,    32.7,       130,  "#FFAA55"),
    ("Sirius B",      25200,   0.0026,     110,  "#DDEEFF"),
    ("40 Eri B",      16500,   0.0130,     100,  "#CCDEFF"),
    ("Procyon B",     10000,   0.00049,    90,   "#BBBBFF"),
]

label_positions = {
    "Sun":          ( 0.12,   0.35, "left"),
    "Sirius A":     ( 0.08,   0.38, "left"),
    "Vega":         (-0.08,   0.38, "right"),
    "Procyon A":    ( 0.10,   0.35, "left"),
    "α Cen A":      ( 0.12,  -0.42, "left"),
    "61 Cyg A":     ( 0.12,   0.35, "left"),
    "Proxima Cen":  ( 0.12,   0.42, "left"),
    "Barnard's St": (-0.10,   0.42, "right"),
    "Betelgeuse":   (-0.12,   0.28, "right"),
    "Antares":      ( 0.10,  -0.35, "left"),
    "Aldebaran":    ( 0.10,   0.35, "left"),
    "Arcturus":     (-0.10,   0.35, "right"),
    "Capella Aa":   ( 0.10,   0.35, "left"),
    "Pollux":       (-0.10,  -0.35, "right"),
    "Sirius B":     ( 0.08,   0.42, "left"),
    "40 Eri B":     (-0.08,   0.42, "right"),
    "Procyon B":    ( 0.08,  -0.48, "left"),
}

ms_classes = {
    "O": (30000, 60000, "#9BB0FF"),
    "B": (10000, 30000, "#AABFFF"),
    "A": (7500,  10000, "#CAD7FF"),
    "F": (6000,   7500, "#F8F7FF"),
    "G": (5200,   6000, "#FFEECC"),
    "K": (3700,   5200, "#FFD2A1"),
    "M": (2400,   3700, "#FF9966"),
}

T_ms = np.logspace(np.log10(2400), np.log10(60000), 500)
L_ms = (T_ms / 5778) ** 4

fig, ax = plt.subplots(figsize=(16, 12))
fig.patch.set_facecolor("#07071A")
ax.set_facecolor("#0B0B20")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(80000, 1600)
ax.set_ylim(3e-5, 8e7)

band_colors = ["#9BB0FF","#AABFFF","#CAD7FF","#F8F7FF","#FFEECC","#FFD2A1","#FF9966"]
band_T = [(30000,60000),(10000,30000),(7500,10000),(6000,7500),(5200,6000),(3700,5200),(2400,3700)]
for (T1, T2), col in zip(band_T, band_colors):
    ax.axvspan(T2, T1, alpha=0.055, color=col, zorder=0)

ax.grid(True, which="major", color="#223355", lw=0.5, alpha=0.5, zorder=0)
ax.grid(True, which="minor", color="#1A2840", lw=0.3, alpha=0.3, zorder=0)

ax.fill_betweenx(L_ms, T_ms * 0.75, T_ms * 1.30,
                 color="#2244CC", alpha=0.13, zorder=1)
ax.plot(T_ms, L_ms, color="#5577FF", lw=2.0, ls="--", alpha=0.8, zorder=2)

ax.text(7800, 4.5, "ZAMS", color="#8899FF", fontsize=8.5,
        rotation=-38, ha="center", va="bottom", fontweight="bold",
        path_effects=[pe.withStroke(linewidth=2.5, foreground="#0B0B20")],
        zorder=7)

ax.fill_betweenx([8, 1e5], [5500,5500], [7500,7500],
                 color="#FFFF44", alpha=0.07, zorder=1)
ax.text(6450, 1.5e5, "Instability\nStrip",
        color="#FFFF99", fontsize=7.5, ha="center", alpha=0.8, style="italic",
        path_effects=[pe.withStroke(linewidth=2, foreground="#0B0B20")])

region_labels = [
    (2700,  3e6,  "RED\nSUPERGIANTS",  "#FF6644", 9),
    (3200,  300,  "RED GIANTS",         "#FF9966", 9),
    (22000, 8e-4, "WHITE DWARFS",       "#CCDDFF", 9),
    (9000,  6e3,  "BLUE GIANTS",        "#AACCFF", 8),
]
for T, L, lbl, col, fs in region_labels:
    ax.text(T, L, lbl, color=col, fontsize=fs, ha="center",
            fontweight="bold", alpha=0.85,
            path_effects=[pe.withStroke(linewidth=2, foreground="#0B0B20")])

for name, T, L, ms, col in named_stars:
    ax.scatter(T, L, s=ms*3.5, color=col, alpha=0.12, zorder=3, linewidths=0)
    ax.scatter(T, L, s=ms*1.5, color=col, alpha=0.25, zorder=3, linewidths=0)
    ax.scatter(T, L, s=ms,     color=col, edgecolors="white",
               linewidths=0.5, zorder=4, alpha=1.0)
    dx, dy, ha = label_positions.get(name, (0.12, 0.35, "left"))
    T_txt = T * (10 ** dx)
    L_txt = L * (10 ** dy)
    ax.annotate(
        name,
        xy=(T, L), xytext=(T_txt, L_txt),
        fontsize=8.5, color="white", ha=ha, va="center", fontweight="bold",
        zorder=6,
        path_effects=[pe.withStroke(linewidth=2.5, foreground="#0B0B20")],
        arrowprops=dict(arrowstyle="-", color="white",
                        alpha=0.35, lw=0.7, shrinkA=0, shrinkB=3),
    )

T_ticks = [50000, 30000, 20000, 10000, 7000, 5000, 3500, 2500]
ax.set_xticks(T_ticks)
ax.set_xticklabels([f"{t:,}" for t in T_ticks], color="white", fontsize=9)

L_ticks = [1e-4, 1e-2, 1, 1e2, 1e4, 1e6]
ax.set_yticks(L_ticks)
ax.set_yticklabels([f"$10^{{{int(np.log10(l))}}}$" for l in L_ticks],
                   color="white", fontsize=10)

ax.tick_params(colors="white", which="both", length=4)
for spine in ax.spines.values():
    spine.set_edgecolor("#223355")

for cls, (T1, T2, col) in ms_classes.items():
    T_mid = np.sqrt(T1 * T2)
    ax.text(T_mid, 1.8e-5, cls, color=col, fontsize=12,
            ha="center", fontweight="bold",
            path_effects=[pe.withStroke(linewidth=2, foreground="#07071A")])

ax2 = ax.twinx()
ax2.set_yscale("log")
ax2.set_ylim(3e-5, 8e7)
mag_ticks = [1e-4, 1e-2, 1, 1e2, 1e4, 1e6]
mag_labels = [f"{4.83 - 2.5*np.log10(l):.1f}" for l in mag_ticks]
ax2.set_yticks(mag_ticks)
ax2.set_yticklabels(mag_labels, color="#AAAACC", fontsize=9)
ax2.set_ylabel("Absolute Visual Magnitude  Mᵥ",
               color="#AAAACC", fontsize=10, labelpad=12)
ax2.tick_params(colors="#AAAACC", which="both")

ax.set_xlabel("Surface Temperature  Teff (K)   ← decreasing",
              color="white", fontsize=11, labelpad=12)
ax.set_ylabel("Luminosity  (L / L☉)",
              color="white", fontsize=11, labelpad=12)

fig.suptitle("Hertzsprung–Russell Diagram",
             color="white", fontsize=16, fontweight="bold", y=0.98)
ax.set_title("Stars Formation & Life Cycle  |  Spectral Classes: O  B  A  F  G  K  M",
             color="#AAAACC", fontsize=9, pad=10)

zams_line    = mlines.Line2D([], [], color="#5577FF", lw=2, ls="--",
                              label="ZAMS (Zero Age Main Sequence)")
instab_patch = mpatches.Patch(color="#FFFF44", alpha=0.5,
                               label="Instability Strip (Cepheids)")
sup_dot      = mlines.Line2D([], [], marker="o", color="none",
                              markerfacecolor="#FF4411", markeredgecolor="white",
                              markersize=10, label="Red / Blue Supergiants")
giant_dot    = mlines.Line2D([], [], marker="o", color="none",
                              markerfacecolor="#FF9966", markeredgecolor="white",
                              markersize=9,  label="Red Giants")
wd_dot       = mlines.Line2D([], [], marker="o", color="none",
                              markerfacecolor="#CCDDFF", markeredgecolor="white",
                              markersize=7,  label="White Dwarfs")
ms_dot       = mlines.Line2D([], [], marker="o", color="none",
                              markerfacecolor="#FFF200", markeredgecolor="white",
                              markersize=8,  label="Main Sequence Stars")

ax.legend(
    handles=[zams_line, instab_patch, ms_dot, giant_dot, sup_dot, wd_dot],
    loc="lower left",
    facecolor="#111133",
    edgecolor="#334466",
    labelcolor="white",
    fontsize=8.5,
    framealpha=0.92,
    borderpad=0.9,
)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("/Users/ekta/hr_diagram.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved: hr_diagram.png")