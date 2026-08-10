"""
stellar_classifier.py
Stellar Classification & H–R Diagram — Interactive Star Card Activity
Space Science Fundamentals | Module 3

HOW IT WORKS:
  - 20 real stars shown as "colour/brightness cards" (left panel)
  - User drags a slider to set Temperature & Luminosity guesses
  - User selects Spectral Class and Luminosity Class
  - App classifies the star and plots it live on the H–R diagram (right panel)
  - Score tracked across all 20 cards
  - Custom star entry: type in any T_eff & L to see where it lands

Run:  python3 stellar_classifier.py
Requires: matplotlib, numpy  (pip3 install matplotlib numpy)
"""

import numpy as np
import matplotlib
matplotlib.use("TkAgg")          # interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.widgets import Button, RadioButtons, Slider, TextBox
from matplotlib.patches import FancyBboxPatch
import random

# ══════════════════════════════════════════════════════════════════
# VERIFIED STELLAR DATA
# Sources: HIPPARCOS, Mamajek 2013, IAU, Wikipedia stellar articles
# ══════════════════════════════════════════════════════════════════
STARS = [
    # name,           T_eff,   L/L☉,       sp_class, lum_class,  hint_color,   radius_R☉
    ("Sun",           5778,    1.00,        "G",      "V",        "#FFF200",    1.0),
    ("Sirius A",      9940,    25.4,        "A",      "V",        "#C8D8FF",    1.71),
    ("Vega",          9602,    40.12,       "A",      "V",        "#D0E0FF",    2.36),
    ("Procyon A",     6530,    7.00,        "F",      "V",        "#FFE880",    2.05),
    ("α Cen A",       5790,    1.52,        "G",      "V",        "#FFE45E",    1.22),
    ("61 Cyg A",      4526,    0.153,       "K",      "V",        "#FFA040",    0.67),
    ("Proxima Cen",   3042,    0.00155,     "M",      "V",        "#FF4500",    0.15),
    ("Barnard's Star",3134,    0.00350,     "M",      "V",        "#FF5500",    0.20),
    ("Betelgeuse",    3500,    126000.0,    "M",      "Ia",       "#FF3300",    887.0),
    ("Antares",       3570,    57500.0,     "M",      "Ib",       "#FF4411",    680.0),
    ("Aldebaran",     3910,    518.0,       "K",      "III",      "#FF6633",    44.2),
    ("Arcturus",      4286,    170.0,       "K",      "III",      "#FF8C00",    25.4),
    ("Capella Aa",    4970,    78.7,        "G",      "III",      "#FFAA33",    11.98),
    ("Pollux",        4865,    32.7,        "K",      "III",      "#FFAA55",    8.80),
    ("Rigel",         12100,   120000.0,    "B",      "Ia",       "#AACCFF",    78.9),
    ("Deneb",         8525,    196000.0,    "A",      "Ia",       "#CCE0FF",    203.0),
    ("Spica",         25300,   12100.0,     "B",      "V",        "#9BB0FF",    7.40),
    ("Sirius B",      25200,   0.0026,      "A",      "VII",      "#DDEEFF",    0.0084),
    ("40 Eri B",      16500,   0.013,       "A",      "VII",      "#CCDEFF",    0.014),
    ("Canopus",       7400,    10700.0,     "A",      "II",       "#E0EEFF",    71.4),
]

SPECTRAL_CLASSES = ["O", "B", "A", "F", "G", "K", "M"]
LUM_CLASSES      = ["Ia", "Ib", "II", "III", "IV", "V", "VII"]
LUM_LABELS       = {
    "Ia":  "Bright Supergiant",
    "Ib":  "Supergiant",
    "II":  "Bright Giant",
    "III": "Giant",
    "IV":  "Subgiant",
    "V":   "Main Sequence (Dwarf)",
    "VII": "White Dwarf",
}

SP_TEMP = {   # representative midpoint T_eff per class
    "O": 40000, "B": 20000, "A": 9000,
    "F": 6750,  "G": 5500,  "K": 4500, "M": 3000,
}
SP_COLOR = {
    "O": "#9BB0FF", "B": "#AABFFF", "A": "#CAD7FF",
    "F": "#F8F7FF", "G": "#FFEECC", "K": "#FFD2A1", "M": "#FF9966",
}

# Main sequence T→L approximation
T_MS  = np.logspace(np.log10(2400), np.log10(60000), 500)
L_MS  = (T_MS / 5778) ** 4

# ══════════════════════════════════════════════════════════════════
# CLASSIFIER LOGIC
# ══════════════════════════════════════════════════════════════════
def classify_sp(T):
    if   T >= 30000: return "O"
    elif T >= 10000: return "B"
    elif T >= 7500:  return "A"
    elif T >= 6000:  return "F"
    elif T >= 5200:  return "G"
    elif T >= 3700:  return "K"
    else:            return "M"

def classify_lum(T, L):
    L_zams = (T / 5778) ** 4
    ratio  = L / max(L_zams, 1e-10)
    if L < 0.01:              return "VII"
    elif ratio > 5000:        return "Ia"
    elif ratio > 1000:        return "Ib"
    elif ratio > 200:         return "II"
    elif ratio > 30:          return "III"
    elif ratio > 3:           return "IV"
    else:                     return "V"

def score_answer(true_sp, true_lum, guess_sp, guess_lum):
    sp_score  = 2 if guess_sp  == true_sp  else 0
    lum_score = 2 if guess_lum == true_lum else 0
    return sp_score + lum_score   # max 4 per star

# ══════════════════════════════════════════════════════════════════
# COLOUR CARD  (text-art style, drawn with matplotlib patches)
# ══════════════════════════════════════════════════════════════════
def draw_card(ax_card, star, revealed=False):
    ax_card.clear()
    ax_card.set_facecolor("#0A0A1E")
    ax_card.set_xlim(0, 10)
    ax_card.set_ylim(0, 14)
    ax_card.axis("off")

    name, T, L, sp, lum, col, R = star
    glow_col = col

    # Card border
    border = FancyBboxPatch((0.3, 0.3), 9.4, 13.4,
                             boxstyle="round,pad=0.1",
                             linewidth=2, edgecolor=glow_col,
                             facecolor="#0D0D2B", alpha=0.9)
    ax_card.add_patch(border)

    # Star glow layers
    for r, a in [(3.0, 0.06), (2.0, 0.12), (1.2, 0.22), (0.6, 0.60), (0.3, 1.0)]:
        ax_card.add_patch(plt.Circle((5, 9.5), r, color=col, alpha=a, zorder=5))

    # Brightness indicator bar
    brightness_norm = min(np.log10(L + 1e-6) / 6, 1.0)
    ax_card.add_patch(FancyBboxPatch((1, 7.0), 8 * brightness_norm, 0.4,
                                      boxstyle="round,pad=0.05",
                                      facecolor=col, alpha=0.8, edgecolor="none"))
    ax_card.add_patch(FancyBboxPatch((1, 7.0), 8, 0.4,
                                      boxstyle="round,pad=0.05",
                                      facecolor="none", edgecolor="#334466", lw=0.8))
    ax_card.text(5, 6.6, "Brightness", color="#AAAACC", fontsize=7, ha="center")

    # Temperature colour strip
    t_norm = (np.log10(T) - np.log10(2000)) / (np.log10(60000) - np.log10(2000))
    strip_colors = ["#FF4400", "#FF8800", "#FFEE00", "#FFFFFF", "#AACCFF", "#7799FF", "#5566FF"]
    strip_x = np.linspace(1, 9, len(strip_colors))
    for i in range(len(strip_colors) - 1):
        ax_card.add_patch(plt.Rectangle((strip_x[i], 5.8),
                                         strip_x[i+1] - strip_x[i], 0.5,
                                         color=strip_colors[i], alpha=0.7))
    # marker on strip
    marker_x = 1 + t_norm * 8
    ax_card.plot([marker_x, marker_x], [5.7, 6.45], color="white", lw=2, zorder=6)
    ax_card.text(5, 5.5, "Temperature  →  Cool to Hot", color="#AAAACC",
                 fontsize=6.5, ha="center")

    # Star name (always shown)
    ax_card.text(5, 13.2, name, color="white", fontsize=11,
                 ha="center", fontweight="bold",
                 path_effects=[pe.withStroke(linewidth=2, foreground="#0D0D2B")])

    if revealed:
        # Show full data
        ax_card.text(5, 12.5, f"T_eff = {T:,} K", color="#AADDFF", fontsize=8.5, ha="center")
        ax_card.text(5, 11.9, f"L = {L:.4g} L☉", color="#FFDDAA", fontsize=8.5, ha="center")
        ax_card.text(5, 11.3, f"Radius ≈ {R:.3g} R☉", color="#DDFFDD", fontsize=8, ha="center")
        ax_card.text(5, 10.6,
                     f"Class: {sp}{lum}  ({LUM_LABELS[lum]})",
                     color=col, fontsize=8, ha="center", fontweight="bold")
    else:
        # Show only visual clues
        ax_card.text(5, 12.4, "Clues:", color="#AAAACC", fontsize=8, ha="center")
        clue_L = ("Very high" if L > 10000 else "High" if L > 100
                  else "Medium" if L > 0.5 else "Low" if L > 0.001 else "Very low")
        clue_T = ("Very hot (blue-white)" if T > 15000 else
                  "Hot (white)"           if T > 8000  else
                  "Warm (yellow-white)"   if T > 6500  else
                  "Sun-like (yellow)"     if T > 5000  else
                  "Cool (orange)"         if T > 3700  else
                  "Very cool (red)")
        ax_card.text(5, 11.8, f"Colour: {clue_T}", color="#FFEECC", fontsize=7.5, ha="center")
        ax_card.text(5, 11.2, f"Brightness: {clue_L}", color="#FFEECC", fontsize=7.5, ha="center")
        ax_card.text(5, 10.5, f"Approx size: {R:.2g} R☉", color="#CCFFCC", fontsize=7.5, ha="center")

    # Spectral class colour chips at bottom
    for i, sc in enumerate(SPECTRAL_CLASSES):
        bx = 0.9 + i * 1.18
        ax_card.add_patch(plt.Circle((bx + 0.45, 1.5), 0.35,
                                      color=SP_COLOR[sc], alpha=0.85))
        ax_card.text(bx + 0.45, 1.5, sc, color="black",
                     fontsize=6.5, ha="center", va="center", fontweight="bold")
    ax_card.text(5, 0.8, "← M  K  G  F  A  B  O →   (cool → hot)",
                 color="#777799", fontsize=6, ha="center")

# ══════════════════════════════════════════════════════════════════
# HR DIAGRAM  (right panel)
# ══════════════════════════════════════════════════════════════════
def draw_hr(ax_hr, classified, current_star=None, custom_pts=None):
    ax_hr.clear()
    ax_hr.set_facecolor("#0B0B20")

    # Spectral bands
    band_T = [(30000,60000),(10000,30000),(7500,10000),
               (6000,7500),(5200,6000),(3700,5200),(2400,3700)]
    band_C = ["#9BB0FF","#AABFFF","#CAD7FF","#F8F7FF","#FFEECC","#FFD2A1","#FF9966"]
    for (T1, T2), c in zip(band_T, band_C):
        ax_hr.axvspan(T2, T1, alpha=0.05, color=c, zorder=0)

    ax_hr.grid(True, which="major", color="#1E2A44", lw=0.5, alpha=0.6)
    ax_hr.grid(True, which="minor", color="#141E33", lw=0.3, alpha=0.3)

    # ZAMS
    ax_hr.fill_betweenx(L_MS, T_MS*0.75, T_MS*1.28,
                         color="#2244CC", alpha=0.12, zorder=1)
    ax_hr.plot(T_MS, L_MS, color="#5577FF", lw=1.8,
               ls="--", alpha=0.75, zorder=2)
    ax_hr.text(7500, 3.5, "ZAMS", color="#7799FF", fontsize=7,
               rotation=-38, va="bottom",
               path_effects=[pe.withStroke(linewidth=2, foreground="#0B0B20")])

    # Region labels
    for T, L, lbl, col in [
        (3000, 5e5, "RED\nSUPERGIANTS", "#FF6644"),
        (3500, 200, "RED GIANTS",       "#FF9966"),
        (22000, 5e-4,"WHITE DWARFS",    "#CCDDFF"),
        (50000, 2e4, "BLUE\nGIANTS",   "#AACCFF"),
    ]:
        ax_hr.text(T, L, lbl, color=col, fontsize=7, ha="center",
                   fontweight="bold", alpha=0.7,
                   path_effects=[pe.withStroke(linewidth=1.5, foreground="#0B0B20")])

    # All 20 stars (faint background)
    for s in STARS:
        ax_hr.scatter(s[1], s[2], s=40, color=s[5],
                      alpha=0.18, edgecolors="none", zorder=2)

    # Classified stars (bright, with name)
    for s, correct in classified:
        col = "#44FF88" if correct else "#FF4444"
        ax_hr.scatter(s[1], s[2], s=90, color=s[5],
                      edgecolors=col, linewidths=1.5, zorder=5, alpha=0.95)
        ax_hr.text(s[1]*1.08, s[2], s[0], color="white",
                   fontsize=6.5, va="center", alpha=0.9,
                   path_effects=[pe.withStroke(linewidth=1.5, foreground="#0B0B20")])

    # Current star being classified
    if current_star:
        ax_hr.scatter(current_star[1], current_star[2], s=220,
                      color=current_star[5], edgecolors="white",
                      linewidths=2, zorder=6, alpha=1.0)
        for r, a in [(180, 0.08), (120, 0.15)]:
            ax_hr.scatter(current_star[1], current_star[2],
                          s=r, color=current_star[5], alpha=a,
                          edgecolors="none", zorder=4)

    # Custom points
    if custom_pts:
        for T, L, label in custom_pts:
            sp = classify_sp(T)
            col = SP_COLOR[sp]
            ax_hr.scatter(T, L, s=150, color=col,
                          edgecolors="#FFD700", linewidths=2, marker="*", zorder=7)
            ax_hr.text(T*1.08, L, label, color="#FFD700",
                       fontsize=7, va="center",
                       path_effects=[pe.withStroke(linewidth=1.5, foreground="#0B0B20")])

    # Axes
    ax_hr.set_xscale("log"); ax_hr.set_yscale("log")
    ax_hr.set_xlim(70000, 1800); ax_hr.set_ylim(5e-6, 5e7)
    ax_hr.invert_xaxis()

    T_ticks = [40000, 20000, 10000, 7000, 5000, 3500, 2500]
    ax_hr.set_xticks(T_ticks)
    ax_hr.set_xticklabels([f"{t:,}" for t in T_ticks], color="white", fontsize=7)
    L_ticks = [1e-4, 1e-2, 1, 1e2, 1e4, 1e6]
    ax_hr.set_yticks(L_ticks)
    ax_hr.set_yticklabels([f"$10^{{{int(np.log10(l))}}}$" for l in L_ticks],
                           color="white", fontsize=8)
    ax_hr.tick_params(colors="white", which="both", length=3)
    for sp in ax_hr.spines.values(): sp.set_edgecolor("#223355")

    ax_hr.set_xlabel("Temperature Teff (K) ← decreasing", color="white", fontsize=8)
    ax_hr.set_ylabel("Luminosity (L/L☉)", color="white", fontsize=8)
    ax_hr.set_title("H–R Diagram  (live)", color="white", fontsize=9, pad=6)

    # Spectral class labels top
    for cls, (T1, T2, col) in zip(SPECTRAL_CLASSES,
        [(30000,60000,"#9BB0FF"),(10000,30000,"#AABFFF"),(7500,10000,"#CAD7FF"),
         (6000,7500,"#F8F7FF"),(5200,6000,"#FFEECC"),(3700,5200,"#FFD2A1"),(2400,3700,"#FF9966")]):
        T_mid = np.sqrt(T1*T2)
        ax_hr.text(T_mid, 2e7, cls, color=col, fontsize=8,
                   ha="center", fontweight="bold",
                   path_effects=[pe.withStroke(linewidth=1.5, foreground="#0B0B20")])

# ══════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════
class StellarClassifier:
    def __init__(self):
        self.order       = random.sample(range(len(STARS)), len(STARS))
        self.idx         = 0
        self.score       = 0
        self.max_score   = 0
        self.classified  = []   # list of (star, correct:bool)
        self.custom_pts  = []
        self.revealed    = False
        self.guess_sp    = "G"
        self.guess_lum   = "V"
        self.done        = False

        self._build_ui()
        self._update()

    def current_star(self):
        return STARS[self.order[self.idx]]

    def _build_ui(self):
        self.fig = plt.figure(figsize=(18, 10), facecolor="#07071A")
        self.fig.suptitle(
            "★  Stellar Classification Activity  ★   Classify stars from their colour & brightness cards",
            color="white", fontsize=13, fontweight="bold", y=0.98)

        # Layout grid
        gs = self.fig.add_gridspec(
            3, 4,
            left=0.03, right=0.97, top=0.93, bottom=0.04,
            wspace=0.35, hspace=0.55,
            height_ratios=[5, 1.2, 1.2],
        )

        self.ax_card  = self.fig.add_subplot(gs[0, 0])
        self.ax_hr    = self.fig.add_subplot(gs[0, 1:4])
        self.ax_ctrl  = self.fig.add_subplot(gs[1:, 0])
        self.ax_fb    = self.fig.add_subplot(gs[1:, 1:3])
        self.ax_cust  = self.fig.add_subplot(gs[1:, 3])

        for ax in [self.ax_ctrl, self.ax_fb, self.ax_cust]:
            ax.set_facecolor("#0D0D2B")
            ax.axis("off")

        self.ax_card.set_facecolor("#0A0A1E")
        self.ax_hr.set_facecolor("#0B0B20")

        # ── Spectral class radio ──
        self.fig.text(0.035, 0.38, "Spectral Class:", color="white", fontsize=8)
        ax_sp = self.fig.add_axes([0.03, 0.22, 0.10, 0.16],
                                   facecolor="#111133")
        self.radio_sp = RadioButtons(ax_sp, SPECTRAL_CLASSES, active=4)
        for lbl in self.radio_sp.labels:
            lbl.set_color(SP_COLOR.get(lbl.get_text(), "white"))
            lbl.set_fontsize(9)
        self.radio_sp.on_clicked(self._on_sp)

        # ── Luminosity class radio ──
        self.fig.text(0.035, 0.22, "Luminosity Class:", color="white", fontsize=8)
        ax_lum = self.fig.add_axes([0.03, 0.06, 0.10, 0.16],
                                    facecolor="#111133")
        self.radio_lum = RadioButtons(ax_lum, LUM_CLASSES, active=5)
        for lbl in self.radio_lum.labels:
            lbl.set_color("#AADDFF")
            lbl.set_fontsize(9)
        self.radio_lum.on_clicked(self._on_lum)

        # ── Buttons ──
        ax_sub  = self.fig.add_axes([0.39, 0.13, 0.10, 0.04])
        ax_rev  = self.fig.add_axes([0.51, 0.13, 0.10, 0.04])
        ax_nxt  = self.fig.add_axes([0.63, 0.13, 0.10, 0.04])
        ax_rst  = self.fig.add_axes([0.75, 0.13, 0.08, 0.04])

        self.btn_sub = Button(ax_sub, "✔ Submit",  color="#1A3A1A", hovercolor="#2A5A2A")
        self.btn_rev = Button(ax_rev, "👁 Reveal",  color="#1A1A3A", hovercolor="#2A2A5A")
        self.btn_nxt = Button(ax_nxt, "▶ Next Star",color="#2A1A0A", hovercolor="#4A2A0A")
        self.btn_rst = Button(ax_rst, "↺ Reset",   color="#3A0A0A", hovercolor="#5A1A1A")

        for b in [self.btn_sub, self.btn_rev, self.btn_nxt, self.btn_rst]:
            b.label.set_color("white")
            b.label.set_fontsize(9)

        self.btn_sub.on_clicked(self._submit)
        self.btn_rev.on_clicked(self._reveal)
        self.btn_nxt.on_clicked(self._next)
        self.btn_rst.on_clicked(self._reset)

        # ── Custom star entry ──
        self.fig.text(0.87, 0.36, "Custom Star Entry", color="#FFD700",
                      fontsize=8, fontweight="bold", ha="center")
        self.fig.text(0.87, 0.32, "T_eff (K):", color="#AAAACC", fontsize=7.5, ha="center")
        ax_t = self.fig.add_axes([0.83, 0.28, 0.08, 0.03], facecolor="#0D0D2B")
        self.tb_T = TextBox(ax_t, "", initial="5778", color="#0D0D2B",
                            hovercolor="#1A1A3A", label_pad=0)
        self.tb_T.label.set_color("white")

        self.fig.text(0.87, 0.26, "L / L☉:", color="#AAAACC", fontsize=7.5, ha="center")
        ax_l = self.fig.add_axes([0.83, 0.22, 0.08, 0.03], facecolor="#0D0D2B")
        self.tb_L = TextBox(ax_l, "", initial="1.0", color="#0D0D2B",
                            hovercolor="#1A1A3A", label_pad=0)
        self.tb_L.label.set_color("white")

        self.fig.text(0.87, 0.20, "Label:", color="#AAAACC", fontsize=7.5, ha="center")
        ax_n = self.fig.add_axes([0.83, 0.16, 0.08, 0.03], facecolor="#0D0D2B")
        self.tb_N = TextBox(ax_n, "", initial="My Star", color="#0D0D2B",
                            hovercolor="#1A1A3A", label_pad=0)
        self.tb_N.label.set_color("white")

        ax_cp = self.fig.add_axes([0.84, 0.10, 0.06, 0.04])
        self.btn_cp = Button(ax_cp, "Plot Star", color="#1A2A1A", hovercolor="#2A4A2A")
        self.btn_cp.label.set_color("#FFD700")
        self.btn_cp.label.set_fontsize(8)
        self.btn_cp.on_clicked(self._custom_plot)

        ax_clr = self.fig.add_axes([0.84, 0.06, 0.06, 0.03])
        self.btn_clr = Button(ax_clr, "Clear", color="#2A1A1A", hovercolor="#4A2A2A")
        self.btn_clr.label.set_color("#FFAAAA")
        self.btn_clr.label.set_fontsize(8)
        self.btn_clr.on_clicked(self._clear_custom)

        # Feedback text area
        self.fb_text = self.ax_fb.text(
            0.5, 0.5, "", transform=self.ax_fb.transAxes,
            color="white", fontsize=10, ha="center", va="center",
            wrap=True, multialignment="center"
        )

        # Score text
        self.score_text = self.fig.text(
            0.39, 0.08, "", color="#FFD700", fontsize=10, fontweight="bold"
        )

        # Progress
        self.progress_text = self.fig.text(
            0.39, 0.19, "", color="#AAAACC", fontsize=8
        )

    # ── Callbacks ──────────────────────────────────────────────────
    def _on_sp(self, label):
        self.guess_sp = label

    def _on_lum(self, label):
        self.guess_lum = label

    def _submit(self, event):
        if self.revealed or self.done:
            return
        star = self.current_star()
        pts  = score_answer(star[3], star[4], self.guess_sp, self.guess_lum)
        self.score     += pts
        self.max_score += 4
        correct = pts == 4

        self.classified.append((star, correct))

        sp_ok  = "✔" if self.guess_sp  == star[3] else f"✘ (ans: {star[3]})"
        lum_ok = "✔" if self.guess_lum == star[4] else f"✘ (ans: {star[4]})"
        fb = (f"{'✅ CORRECT!' if correct else '❌ Not quite...'}\n"
              f"Spectral: {self.guess_sp} {sp_ok}    "
              f"Lum Class: {self.guess_lum} {lum_ok}\n"
              f"+{pts}/4 pts  |  Total: {self.score}/{self.max_score}")
        self.fb_text.set_text(fb)
        self.fb_text.set_color("#88FF88" if correct else "#FF8888")
        self._update_score()
        self._redraw_hr()
        self.fig.canvas.draw_idle()

    def _reveal(self, event):
        self.revealed = True
        draw_card(self.ax_card, self.current_star(), revealed=True)
        self.fig.canvas.draw_idle()

    def _next(self, event):
        if self.idx < len(self.order) - 1:
            self.idx    += 1
            self.revealed = False
            self.fb_text.set_text("")
            self._update()
        else:
            self.done = True
            pct = (self.score / max(self.max_score, 1)) * 100
            self.fb_text.set_text(
                f"🎉 Activity complete!\n"
                f"Final score: {self.score}/{self.max_score}  ({pct:.0f}%)\n"
                f"{'⭐ Excellent!' if pct>=80 else '👍 Good effort!' if pct>=50 else '📚 Keep studying!'}"
            )
            self.fb_text.set_color("#FFD700")
            self.fig.canvas.draw_idle()

    def _reset(self, event):
        self.order      = random.sample(range(len(STARS)), len(STARS))
        self.idx        = 0
        self.score      = 0
        self.max_score  = 0
        self.classified = []
        self.revealed   = False
        self.done       = False
        self.fb_text.set_text("")
        self._update()

    def _custom_plot(self, event):
        try:
            T = float(self.tb_T.text)
            L = float(self.tb_L.text)
            n = self.tb_N.text.strip() or "Custom"
            sp  = classify_sp(T)
            lum = classify_lum(T, L)
            self.custom_pts.append((T, L, n))
            self.fb_text.set_text(
                f"Custom Star '{n}'\n"
                f"T={T:,.0f} K  |  L={L:.4g} L☉\n"
                f"Auto-classified: {sp}{lum}  ({LUM_LABELS[lum]})"
            )
            self.fb_text.set_color("#FFD700")
            self._redraw_hr()
            self.fig.canvas.draw_idle()
        except ValueError:
            self.fb_text.set_text("⚠ Enter valid numbers for T and L")
            self.fb_text.set_color("#FF8888")
            self.fig.canvas.draw_idle()

    def _clear_custom(self, event):
        self.custom_pts = []
        self._redraw_hr()
        self.fig.canvas.draw_idle()

    def _update(self):
        draw_card(self.ax_card, self.current_star(), revealed=self.revealed)
        self._redraw_hr()
        self._update_score()
        self.fig.canvas.draw_idle()

    def _redraw_hr(self):
        curr = self.current_star() if not self.done else None
        draw_hr(self.ax_hr, self.classified, curr, self.custom_pts)

    def _update_score(self):
        self.score_text.set_text(
            f"Score: {self.score} / {self.max_score} pts"
        )
        self.progress_text.set_text(
            f"Star {self.idx + 1} of {len(STARS)}   |   "
            f"Classified: {len(self.classified)}"
        )

    def show(self):
        plt.show(block=True)


if __name__ == "__main__":
    app = StellarClassifier()
    app.show()