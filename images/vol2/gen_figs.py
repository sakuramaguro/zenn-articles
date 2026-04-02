#!/usr/bin/env python3
"""Generate vol2 figures fig-01 through fig-18 as SVG and PNG."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc, Circle, Ellipse
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = os.path.expanduser("~/zenn-articles/images/vol2")

FONT_JP  = "Hiragino Sans"
FONT_CODE = "Courier New"
DPI = 300

def save(fig, name):
    svg_path = os.path.join(OUT, f"{name}.svg")
    png_path = os.path.join(OUT, f"{name}.png")
    fig.savefig(svg_path, format="svg", bbox_inches="tight", dpi=DPI)
    fig.savefig(png_path, format="png", bbox_inches="tight", dpi=DPI,
                facecolor="white")
    plt.close(fig)
    print(f"  saved {name}.svg / {name}.png")

# ── common style ──────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": FONT_JP,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

# =============================================================================
# fig-01  Filter telescope metaphor
# =============================================================================
def fig01():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10); ax.set_ylim(-1.5, 2.5); ax.axis("off")

    # number line
    ax.annotate("", xy=(4.0, 0), xytext=(0.5, 0),
                arrowprops=dict(arrowstyle="-|>", color="#333"))
    # convergent points 1/n
    xs = [3.5, 2.5, 1.8, 1.4, 1.15, 1.05, 1.01]
    for i, x in enumerate(xs):
        ax.plot(x, 0, "o", color="#4472C4", markersize=6 - i * 0.6, zorder=3)
        if i < 4:
            ax.text(x, -0.35, f"1/{i+1}", ha="center", fontsize=8,
                    fontfamily=FONT_CODE, color="#4472C4")
    ax.text(1.0, -0.35, "...", ha="center", fontsize=9, color="#4472C4")
    ax.text(2.0, 1.5, "1/n  -->  0", ha="center", fontsize=11,
            fontfamily=FONT_CODE, color="#4472C4",
            style="italic")

    # funnel / lens (trapezoid)
    trap = plt.Polygon([[4.2, 1.0],[5.8, 1.8],[5.8,-1.0],[4.2,-1.0]],
                       closed=True, facecolor="#FFF2CC", edgecolor="#C9A800", lw=2)
    ax.add_patch(trap)
    ax.text(5.0, 0.15, "Filter", ha="center", va="center", fontsize=13,
            fontfamily=FONT_JP, fontweight="bold", color="#7F5F00")
    ax.text(5.0, -0.5, "(toku-tei no\nshugo-zoku wo\ntosu)", ha="center",
            fontsize=7, fontfamily=FONT_JP, color="#7F5F00")

    # arrow to result
    ax.annotate("", xy=(7.5, 0), xytext=(6.0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
    ax.text(9.0, 0, "0", ha="center", va="center", fontsize=28,
            fontweight="bold", color="#C00000")
    ax.text(9.0, -0.6, "(shuusoku-saki)", ha="center", fontsize=9,
            fontfamily=FONT_JP, color="#C00000")

    ax.set_title("fig-01  Filter no bouentai-hiyu",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-01")

# =============================================================================
# fig-02  nhds concentric circles
# =============================================================================
def fig02():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)
    ax.axis("off")

    colors = ["#BDD7EE", "#9DC3E6", "#5B9BD5", "#2E75B6"]
    radii  = [3.2, 2.4, 1.6, 0.8]
    labels = ["U (open set)", "B(x, 2e)", "B(x, e)", "B(x, e/2)"]

    for r, c, lbl in zip(radii, colors, labels):
        circ = Circle((0, 0), r, facecolor=c, edgecolor="#2E75B6",
                      lw=1.5, alpha=0.5, linestyle="--")
        ax.add_patch(circ)
        ax.text(r * 0.72, r * 0.72, lbl, fontsize=8, fontfamily=FONT_CODE,
                ha="left", va="bottom", color="#1F4E79")

    ax.plot(0, 0, "o", color="#C00000", markersize=8, zorder=5)
    ax.text(0.15, 0.15, "x", fontsize=16, fontweight="bold",
            fontfamily=FONT_CODE, color="#C00000")

    ax.text(0, -3.8,
            "nhds x = all open neighborhoods containing x",
            ha="center", fontsize=10, fontfamily=FONT_CODE, color="#1F4E79")
    ax.set_title("fig-02  nhds no doushinen-zu (kyo-ri kuukan)",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-02")

# =============================================================================
# fig-03  Filter.Tendsto concept
# =============================================================================
def fig03():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11); ax.set_ylim(-1, 4); ax.axis("off")

    # left space X
    el_x = Ellipse((2.2, 1.5), 3.8, 3.5, facecolor="#DDEEFF",
                   edgecolor="#4472C4", lw=2, alpha=0.6)
    ax.add_patch(el_x)
    ax.text(2.2, 3.2, "X  (e.g. R)", ha="center", fontsize=12,
            fontfamily=FONT_CODE, fontweight="bold", color="#1F4E79")

    # right space Y
    el_y = Ellipse((8.8, 1.5), 3.8, 3.5, facecolor="#DDFFEE",
                   edgecolor="#548235", lw=2, alpha=0.6)
    ax.add_patch(el_y)
    ax.text(8.8, 3.2, "Y  (e.g. R)", ha="center", fontsize=12,
            fontfamily=FONT_CODE, fontweight="bold", color="#375623")

    # points in X
    ax.plot(1.2, 1.5, "o", color="#4472C4", ms=7)
    ax.text(1.05, 1.7, "x_n", fontsize=10, fontfamily=FONT_CODE, color="#4472C4")
    ax.plot(1.8, 1.5, "o", color="#4472C4", ms=7)
    ax.plot(2.2, 1.5, "o", color="#C00000", ms=9, zorder=5)
    ax.text(2.35, 1.7, "x", fontsize=12, fontfamily=FONT_CODE,
            fontweight="bold", color="#C00000")
    ax.annotate("", xy=(2.2, 1.5), xytext=(1.2, 1.5),
                arrowprops=dict(arrowstyle="-|>", color="#4472C4", lw=1.2))

    # filter F label
    ax.text(2.2, 0.4, "Filter F", ha="center", fontsize=10,
            fontfamily=FONT_CODE, color="#1F4E79",
            bbox=dict(fc="#BDD7EE", ec="#4472C4", boxstyle="round,pad=0.3"))

    # arrow f
    ax.annotate("", xy=(6.8, 1.8), xytext=(4.2, 1.8),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=2.5))
    ax.text(5.5, 2.3, "f", ha="center", fontsize=16, fontfamily=FONT_CODE,
            fontstyle="italic", fontweight="bold")

    # points in Y
    ax.plot(7.8, 1.5, "o", color="#548235", ms=7)
    ax.text(7.55, 1.7, "f(x_n)", fontsize=10, fontfamily=FONT_CODE,
            color="#548235")
    ax.plot(8.3, 1.5, "o", color="#548235", ms=7)
    ax.plot(8.8, 1.5, "o", color="#C00000", ms=9, zorder=5)
    ax.text(9.0, 1.7, "f(x)", fontsize=12, fontfamily=FONT_CODE,
            fontweight="bold", color="#C00000")
    ax.annotate("", xy=(8.8, 1.5), xytext=(7.8, 1.5),
                arrowprops=dict(arrowstyle="-|>", color="#548235", lw=1.2))

    # f* F <= nhds label
    ax.text(8.8, 0.4, "f* F <= nhds (f x)", ha="center", fontsize=10,
            fontfamily=FONT_CODE, color="#375623",
            bbox=dict(fc="#C6EFCE", ec="#548235", boxstyle="round,pad=0.3"))

    ax.set_title("fig-03  Filter.Tendsto no gainen-zu",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-03")

# =============================================================================
# fig-04  Triangle inequality
# =============================================================================
def fig04():
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.5, 4.5); ax.axis("off")

    pts = {"x": (0.5, 0.5), "y": (4.5, 0.5), "z": (2.5, 3.8)}

    # direct path x→z (shorter)
    ax.annotate("", xy=pts["z"], xytext=pts["x"],
                arrowprops=dict(arrowstyle="-|>", color="#C00000",
                                lw=2.5, linestyle="solid"))
    mx = ((pts["x"][0]+pts["z"][0])/2 - 0.5,
          (pts["x"][1]+pts["z"][1])/2)
    ax.text(mx[0], mx[1], "d(x,z)", ha="right", fontsize=11,
            fontfamily=FONT_CODE, color="#C00000", fontweight="bold")

    # detour x→y→z (longer)
    ax.annotate("", xy=pts["y"], xytext=pts["x"],
                arrowprops=dict(arrowstyle="-|>", color="#4472C4",
                                lw=1.8, linestyle="dashed"))
    ax.annotate("", xy=pts["z"], xytext=pts["y"],
                arrowprops=dict(arrowstyle="-|>", color="#4472C4",
                                lw=1.8, linestyle="dashed"))
    ax.text(2.5, -0.2, "d(x,y)", ha="center", fontsize=10,
            fontfamily=FONT_CODE, color="#4472C4")
    ax.text(4.0, 2.3, "d(y,z)", ha="left", fontsize=10,
            fontfamily=FONT_CODE, color="#4472C4")

    for name, pt in pts.items():
        ax.plot(*pt, "o", color="#333", ms=9, zorder=5)
        offset = {"x": (-0.25, -0.25), "y": (0.15, -0.25), "z": (0, 0.15)}
        ax.text(pt[0]+offset[name][0], pt[1]+offset[name][1], name,
                fontsize=16, fontfamily=FONT_CODE, fontweight="bold",
                color="#333")

    ax.text(2.5, 1.5,
            "d(x,z)  <=  d(x,y) + d(y,z)",
            ha="center", fontsize=12, fontfamily=FONT_CODE, color="#222",
            bbox=dict(fc="#FFFBE6", ec="#C9A800",
                      boxstyle="round,pad=0.5"))

    ax.set_title("fig-04  Sankaku-futo-shiki (triangle inequality)",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-04")

# =============================================================================
# fig-05  Open ball / epsilon-neighborhood
# =============================================================================
def fig05():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)
    ax.axis("off")

    # open ball (dashed boundary = open)
    circ = Circle((0, 0), 2.8, facecolor="#DDEEFF", edgecolor="#4472C4",
                  lw=2, linestyle="dashed", alpha=0.7)
    ax.add_patch(circ)

    # interior points
    rng = np.random.default_rng(42)
    for _ in range(12):
        r = rng.uniform(0.3, 2.5)
        theta = rng.uniform(0, 2*np.pi)
        ax.plot(r*np.cos(theta), r*np.sin(theta), ".",
                color="#4472C4", ms=6, alpha=0.8)

    ax.plot(0, 0, "o", color="#C00000", ms=8, zorder=5)
    ax.text(0.15, 0.2, "x", fontsize=16, fontfamily=FONT_CODE,
            fontweight="bold", color="#C00000")

    # radius arrow
    ax.annotate("", xy=(2.8, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=1.8))
    ax.text(1.4, 0.2, "e", fontsize=14, fontfamily=FONT_CODE,
            color="#C9A800", fontweight="bold")

    ax.text(0, -3.5,
            "B(x, e) = {y | d(x,y) < e}",
            ha="center", fontsize=12, fontfamily=FONT_CODE, color="#1F4E79")
    ax.text(0, -4.1, "(kyo-ri < e ... open boundary)",
            ha="center", fontsize=9, fontfamily=FONT_JP, color="#888")

    ax.set_title("fig-05  epsilon-kinbou to kaikyuu (open ball)",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-05")

# =============================================================================
# fig-06  MetricSpace class hierarchy
# =============================================================================
def fig06():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 8); ax.set_ylim(0, 9); ax.axis("off")

    classes = [
        ("MetricSpace",      "#C00000", "#FFDEDE",
         "d(x,y)=0 <-> x=y  (separation)"),
        ("PseudoMetricSpace","#4472C4", "#DDEEFF",
         "allows d(x,y)=0 for x!=y"),
        ("UniformSpace",     "#548235", "#DDFFEE",
         "uniform continuity / Cauchy filter"),
        ("TopologicalSpace", "#7030A0", "#EEE0FF",
         "open sets / nhds filter"),
    ]

    ys = [7.5, 5.5, 3.5, 1.5]
    boxes = []
    for (name, ec, fc, desc), y in zip(classes, ys):
        box = FancyBboxPatch((1.0, y - 0.55), 6.0, 1.1,
                             boxstyle="round,pad=0.1",
                             facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(box)
        ax.text(4.0, y + 0.18, name, ha="center", va="center",
                fontsize=13, fontfamily=FONT_CODE, fontweight="bold",
                color=ec)
        ax.text(4.0, y - 0.2, desc, ha="center", va="center",
                fontsize=9, fontfamily=FONT_CODE, color="#444")
        boxes.append(y)

    # arrows (extends upward = "more specific")
    for i in range(len(ys) - 1):
        y_top = ys[i] - 0.55
        y_bot = ys[i+1] + 0.55
        mid = (y_top + y_bot) / 2
        ax.annotate("", xy=(4.0, y_top), xytext=(4.0, y_bot),
                    arrowprops=dict(arrowstyle="-|>", color="#888",
                                   lw=2, mutation_scale=18))
        ax.text(4.5, mid, "extends", ha="left", fontsize=9,
                fontfamily=FONT_CODE, color="#888")

    ax.text(4.0, 8.7, "MetricSpace no keishou-zu (Lean 4)",
            ha="center", fontsize=13, fontfamily=FONT_JP,
            fontweight="bold", color="#222")
    save(fig, "fig-06")

# =============================================================================
# fig-07  Continuity equivalence (3 columns)
# =============================================================================
def fig07():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

    cols = [
        ("e-d  (epsilon-delta)",
         "For all e>0\nexists d>0:\n|x-a|<d\n -> |f(x)-L|<e",
         "#4472C4", "#DDEEFF"),
        ("Open Sets",
         "For all open V\ncontaining f(a):\nf^(-1)(V) is\nopen in X",
         "#548235", "#DDFFEE"),
        ("Filter (Lean)",
         "Filter.Tendsto f\n  (nhds a)\n  (nhds (f a))",
         "#7030A0", "#EEE0FF"),
    ]
    xs = [1.0, 4.5, 8.0]

    for (title, body, ec, fc), x in zip(cols, xs):
        box = FancyBboxPatch((x, 0.8), 3.0, 4.4,
                             boxstyle="round,pad=0.2",
                             facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(box)
        ax.text(x + 1.5, 4.8, title, ha="center", va="center",
                fontsize=10, fontfamily=FONT_CODE, fontweight="bold",
                color=ec)
        ax.text(x + 1.5, 2.7, body, ha="center", va="center",
                fontsize=10, fontfamily=FONT_CODE, color="#222",
                linespacing=1.6)

    # double arrows between columns
    for x1, x2 in [(4.0, 4.4), (7.5, 7.9)]:
        ax.annotate("", xy=(x2, 3.0), xytext=(x1, 3.0),
                    arrowprops=dict(arrowstyle="<->", color="#C9A800",
                                   lw=2.5, mutation_scale=18))
        ax.text((x1+x2)/2, 3.35, "<==>", ha="center", fontsize=10,
                fontfamily=FONT_CODE, color="#7F5F00", fontweight="bold")

    ax.text(6.0, 5.8, "Continuity: 3-tsu no douji-jouken",
            ha="center", fontsize=13, fontfamily=FONT_JP,
            fontweight="bold", color="#222")
    save(fig, "fig-07")

# =============================================================================
# fig-08  nhds in topological space (no metric)
# =============================================================================
def fig08():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-4.5, 4.5); ax.set_ylim(-4.5, 4.5)
    ax.axis("off")

    # irregular "open sets" -- not circles
    colors = ["#C6EFCE", "#A9D18E", "#70AD47", "#375623"]
    for i, (r, c) in enumerate(zip([3.5, 2.6, 1.8, 1.1], colors)):
        ell = Ellipse((0, 0), r*2.2, r*1.6, angle=15*i,
                      facecolor=c, edgecolor="#375623",
                      lw=1.5, linestyle="dashed", alpha=0.55)
        ax.add_patch(ell)
        angle_r = np.radians(30 + 40*i)
        lx = r * 1.05 * np.cos(angle_r)
        ly = r * 0.75 * np.sin(angle_r)
        labels = ["U3 (open set)", "U2 (open set)",
                  "U1 (open set)", "U0 (open set)"]
        ax.text(lx, ly, labels[i], fontsize=8, fontfamily=FONT_CODE,
                ha="center", color="#1E4117")

    ax.plot(0, 0, "o", color="#C00000", ms=9, zorder=5)
    ax.text(0.2, 0.2, "x", fontsize=16, fontfamily=FONT_CODE,
            fontweight="bold", color="#C00000")

    ax.text(0, -4.2, "no metric -- only open sets containing x",
            ha="center", fontsize=10, fontfamily=FONT_CODE, color="#1E4117")
    ax.text(0, -4.8, "nhds x = inf { P(U) | U open, x in U }",
            ha="center", fontsize=10, fontfamily=FONT_CODE, color="#1F4E79")

    ax.set_title("fig-08  nhds no doushinen-zu (iso-kuukan ban)",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-08")

# =============================================================================
# fig-09  Open / closed set relationship
# =============================================================================
def fig09():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.5, 6); ax.axis("off")

    # universe X
    rect_X = FancyBboxPatch((0, 0), 8, 5.5,
                            boxstyle="round,pad=0.1",
                            facecolor="#F2F2F2", edgecolor="#999",
                            lw=2, linestyle="solid")
    ax.add_patch(rect_X)
    ax.text(0.3, 5.2, "X", fontsize=14, fontfamily=FONT_CODE,
            fontweight="bold", color="#555")

    # open set U (dashed border, left half-ish)
    u_circ = Ellipse((3.0, 2.7), 4.0, 3.8,
                     facecolor="#BDD7EE", edgecolor="#4472C4",
                     lw=2.5, linestyle="dashed", alpha=0.7)
    ax.add_patch(u_circ)
    ax.text(2.2, 4.2, "U  (open set)", fontsize=11, fontfamily=FONT_CODE,
            fontweight="bold", color="#1F4E79")
    ax.text(2.2, 3.7, "(dashed = open boundary)", fontsize=8,
            fontfamily=FONT_CODE, color="#4472C4")

    # closed set U^c (solid border, rest)
    ax.text(6.8, 1.0, "U^c", fontsize=14, fontfamily=FONT_CODE,
            fontweight="bold", color="#C00000")
    ax.text(6.3, 0.5, "(closed set)", fontsize=9, fontfamily=FONT_CODE,
            color="#C00000")

    # boundary points
    boundary_angles = np.linspace(0, 2*np.pi, 10, endpoint=False)
    for ang in boundary_angles:
        bx = 3.0 + 2.0 * np.cos(ang)
        by = 2.7 + 1.9 * np.sin(ang)
        ax.plot(bx, by, "s", color="#C9A800", ms=6, zorder=5)
    ax.text(3.0, 0.65, "boundary  dU", ha="center", fontsize=9,
            fontfamily=FONT_CODE, color="#7F5F00")

    ax.text(4.0, -0.3, "complement of open set = closed set",
            ha="center", fontsize=10, fontfamily=FONT_CODE, color="#444")
    ax.set_title("fig-09  Kai-shugou to Hei-shugou no kankei",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-09")

# =============================================================================
# fig-10  Open cover and compactness
# =============================================================================
def fig10():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(-1, 9); ax.set_ylim(-1, 5.5); ax.axis("off")

    # compact set K
    K = Ellipse((4.0, 2.5), 7.0, 3.8,
                facecolor="#FFFBE6", edgecolor="#C9A800", lw=3, alpha=0.7)
    ax.add_patch(K)
    ax.text(4.0, 4.2, "K  (compact set)", ha="center", fontsize=12,
            fontfamily=FONT_CODE, fontweight="bold", color="#7F5F00")

    # open sets covering K
    cover = [
        (1.5, 1.5, 2.2, 2.0, "#BDD7EE", "#4472C4", "U1"),
        (3.5, 3.0, 2.0, 1.8, "#DDEEFF", "#4472C4", "U2"),
        (5.8, 1.8, 2.0, 2.0, "#C6EFCE", "#548235", "U3"),
        (3.0, 1.0, 1.8, 1.5, "#EEE0FF", "#7030A0", "U4"),
    ]
    for cx, cy, w, h, fc, ec, lbl in cover:
        ell = Ellipse((cx, cy), w, h,
                      facecolor=fc, edgecolor=ec,
                      lw=1.8, linestyle="dashed", alpha=0.5)
        ax.add_patch(ell)
        ax.text(cx, cy + h/2 + 0.1, lbl, ha="center", fontsize=10,
                fontfamily=FONT_CODE, color=ec, fontweight="bold")

    ax.text(4.0, -0.7,
            "Compact  <=>  any open cover has a finite subcover",
            ha="center", fontsize=11, fontfamily=FONT_CODE, color="#333",
            bbox=dict(fc="#FFFBE6", ec="#C9A800", boxstyle="round,pad=0.4"))
    ax.set_title("fig-10  Kai-hifuku to Compact-sei",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-10")

# =============================================================================
# fig-11  Cauchy sequence and completeness
# =============================================================================
def fig11():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax in axes:
        ax.set_ylim(-1.5, 2.5); ax.set_xlim(-0.5, 8)
        ax.axhline(0, color="#bbb", lw=1)
        ax.axis("off")

    # LEFT: complete (R) -- sequence converges
    ax = axes[0]
    ax.set_title("Complete (e.g. R)", fontsize=12, fontfamily=FONT_CODE,
                 fontweight="bold", color="#548235")
    xs = [7.0, 5.5, 4.2, 3.3, 2.7, 2.3, 2.05, 2.01]
    for i, x in enumerate(xs):
        ax.plot(x, 0, "o", color="#4472C4", ms=8 - i*0.7, zorder=3)
    ax.plot(2.0, 0, "D", color="#C00000", ms=10, zorder=5)
    ax.text(2.0, -0.5, "L  (limit exists)", ha="center", fontsize=9,
            fontfamily=FONT_CODE, color="#C00000")
    # brace showing d(a_m, a_n) < e
    ax.annotate("", xy=(2.3, 1.2), xytext=(3.3, 1.2),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=1.8))
    ax.text(2.8, 1.5, "d < e  (Cauchy)", ha="center", fontsize=8,
            fontfamily=FONT_CODE, color="#7F5F00")
    ax.text(4.5, -1.2, "All Cauchy sequences\nconverge in the space",
            ha="center", fontsize=9, fontfamily=FONT_CODE, color="#375623")

    # RIGHT: incomplete (Q) -- sqrt(2) missing
    ax = axes[1]
    ax.set_title("Incomplete (e.g. Q)", fontsize=12, fontfamily=FONT_CODE,
                 fontweight="bold", color="#C00000")
    # rational approximations to sqrt(2)
    target = np.sqrt(2)
    rationals = [1.0, 1.5, 1.4, 1.42, 1.414, 1.4142, 1.41421, 1.414213]
    mapped = [(r - 1.0) / (target - 1.0) * 5.5 + 0.5 for r in rationals]
    for i, x in enumerate(mapped):
        ax.plot(x, 0, "o", color="#4472C4", ms=8 - i*0.7, zorder=3)
    # hole at sqrt(2)
    ax.plot(6.0, 0, "o", color="white", ms=12, zorder=5,
            markeredgecolor="#C00000", markeredgewidth=2)
    ax.text(6.0, -0.5, "sqrt(2)  [HOLE]", ha="center", fontsize=9,
            fontfamily=FONT_CODE, color="#C00000")
    ax.annotate("", xy=(5.8, 0), xytext=(4.5, 0),
                arrowprops=dict(arrowstyle="-|>", color="#4472C4",
                                lw=1.5, linestyle="dashed"))
    ax.text(4.5, -1.2, "Cauchy in Q, but\nlimit is not in Q",
            ha="center", fontsize=9, fontfamily=FONT_CODE, color="#C00000")

    fig.suptitle("fig-11  Cauchy-retsu to Kanzen-sei",
                 fontsize=12, fontfamily=FONT_CODE, color="#555", y=1.01)
    save(fig, "fig-11")

# =============================================================================
# fig-12  UniformSpace structure (nested ellipses)
# =============================================================================
def fig12():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
    ax.axis("off")

    layers = [
        (4.5, 3.8, "#EEE0FF", "#7030A0",
         "TopologicalSpace\n(open sets / nhds)"),
        (3.5, 2.9, "#C6EFCE", "#548235",
         "UniformSpace\n(uniform continuity / Cauchy)"),
        (2.5, 2.0, "#BDD7EE", "#4472C4",
         "PseudoMetricSpace\n(d >= 0, triangle ineq.)"),
        (1.5, 1.1, "#FFDEDE", "#C00000",
         "MetricSpace\n(d=0 <-> x=y)"),
    ]
    for rx, ry, fc, ec, lbl in layers:
        ell = Ellipse((0, 0), rx*2, ry*2,
                      facecolor=fc, edgecolor=ec, lw=2, alpha=0.65)
        ax.add_patch(ell)

    # labels with arrows pointing outward
    offsets = [(3.2, 3.1), (2.4, 2.3), (1.6, 1.5), (0.8, 0.7)]
    for (_, _, _, ec, lbl), (ox, oy) in zip(layers, offsets):
        ax.text(ox, oy, lbl, fontsize=8.5, fontfamily=FONT_CODE,
                ha="left", va="bottom", color=ec, fontweight="bold",
                bbox=dict(fc="white", ec=ec, boxstyle="round,pad=0.2",
                          alpha=0.8))

    ax.set_title("fig-12  UniformSpace no kouzou (hougan-kankei)",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-12")

# =============================================================================
# fig-13  l^2 unit ball (2D and 3D slices)
# =============================================================================
def fig13():
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # 2D unit ball -- perfect circle
    ax = axes[0]
    ax.set_aspect("equal"); ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
    circ = Circle((0, 0), 1.0, facecolor="#BDD7EE", edgecolor="#4472C4",
                  lw=2, linestyle="dashed", alpha=0.7)
    ax.add_patch(circ)
    ax.axhline(0, color="#bbb", lw=0.8); ax.axvline(0, color="#bbb", lw=0.8)
    ax.plot(0, 0, "o", color="#C00000", ms=6)
    ax.set_title("2D: l2 unit ball (circle)", fontsize=11,
                 fontfamily=FONT_CODE, color="#1F4E79")
    ax.set_xlabel("x1", fontfamily=FONT_CODE); ax.set_ylabel("x2", fontfamily=FONT_CODE)
    ax.text(0, -1.6, "{ x : x1^2 + x2^2 < 1 }",
            ha="center", fontsize=9, fontfamily=FONT_CODE, color="#1F4E79")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    # 3D slice (cross-section as shaded circle)
    ax = axes[1]
    ax.set_aspect("equal"); ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
    # draw sphere cross section
    theta = np.linspace(0, 2*np.pi, 300)
    ax.fill(np.cos(theta), np.sin(theta), color="#BDD7EE", alpha=0.6)
    ax.plot(np.cos(theta), np.sin(theta), color="#4472C4", lw=2, ls="dashed")
    # ellipse for 3D effect
    ell = Ellipse((0, 0), 2.0, 0.5, facecolor="none",
                  edgecolor="#4472C4", lw=1.2, linestyle="dotted", alpha=0.6)
    ax.add_patch(ell)
    ax.axhline(0, color="#bbb", lw=0.8); ax.axvline(0, color="#bbb", lw=0.8)
    ax.set_title("3D cross-section (equator)", fontsize=11,
                 fontfamily=FONT_CODE, color="#1F4E79")
    ax.set_xlabel("x1", fontfamily=FONT_CODE); ax.set_ylabel("x3", fontfamily=FONT_CODE)
    ax.text(0, -1.6, "{ x in l2 : ||x||_2 < 1 }",
            ha="center", fontsize=9, fontfamily=FONT_CODE, color="#1F4E79")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    fig.suptitle("fig-13  l^2 kuukan no tan'i-kyuu",
                 fontsize=12, fontfamily=FONT_CODE, color="#555")
    save(fig, "fig-13")

# =============================================================================
# fig-14  Finite vs infinite dimension comparison
# =============================================================================
def fig14():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")

    # header
    ax.text(2.5, 6.6, "Finite Dim (R^n)", ha="center", fontsize=13,
            fontfamily=FONT_CODE, fontweight="bold", color="#4472C4")
    ax.text(7.5, 6.6, "Infinite Dim (l^2)", ha="center", fontsize=13,
            fontfamily=FONT_CODE, fontweight="bold", color="#C00000")
    ax.axvline(5.0, color="#999", lw=1.5, ls="dashed")

    rows = [
        ("Bounded closed set", "= compact  (Heine-Borel)", "!= compact", 5.5),
        ("Unit ball", "compact", "NOT compact", 4.0),
        ("Any bounded seq.", "has conv. subseq.", "may have none", 2.5),
        ("Example", "B_closed in R^2  -- finite pts", "e_n in l^2  d(e_m,e_n)=sqrt(2)", 1.0),
    ]
    for label, left, right, y in rows:
        ax.text(0.3, y + 0.3, label, fontsize=9, fontfamily=FONT_CODE,
                color="#555", fontstyle="italic")
        ax.text(2.5, y, left, ha="center", fontsize=10,
                fontfamily=FONT_CODE, color="#1F4E79",
                bbox=dict(fc="#DDEEFF", ec="#4472C4",
                          boxstyle="round,pad=0.3", alpha=0.8))
        ax.text(7.5, y, right, ha="center", fontsize=10,
                fontfamily=FONT_CODE, color="#C00000",
                bbox=dict(fc="#FFDEDE", ec="#C00000",
                          boxstyle="round,pad=0.3", alpha=0.8))

    ax.set_title("fig-14  Yuugen-jigen vs Mugen-jigen no chigai",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-14")

# =============================================================================
# fig-15  Contraction mapping iteration
# =============================================================================
def fig15():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 10); ax.set_ylim(-1.5, 2.5); ax.axis("off")

    # number line
    ax.annotate("", xy=(9.5, 0), xytext=(0.2, 0),
                arrowprops=dict(arrowstyle="-|>", color="#bbb", lw=1.5))

    # fixed point
    x_star = 7.0
    ax.plot(x_star, 0, "D", color="#C00000", ms=12, zorder=6)
    ax.text(x_star, -0.55, "x*  (fixed point)", ha="center", fontsize=9,
            fontfamily=FONT_CODE, color="#C00000", fontweight="bold")

    # sequence x0, Tx0, T^2 x0, ...
    pts = [1.5, 4.0, 5.7, 6.4, 6.75, 6.9, 6.96, 7.0]
    labels = ["x0", "T(x0)", "T^2(x0)", "T^3(x0)", "", "", "...", ""]
    colors_seq = ["#4472C4"] * len(pts)

    for i, (x, lbl) in enumerate(zip(pts, labels)):
        ax.plot(x, 0, "o", color="#4472C4", ms=9 - i*0.8, zorder=3)
        if lbl:
            ax.text(x, 0.35 + (i % 2)*0.5, lbl, ha="center", fontsize=8,
                    fontfamily=FONT_CODE, color="#1F4E79")

    for i in range(len(pts) - 1):
        ax.annotate("", xy=(pts[i+1], 0.08), xytext=(pts[i], 0.08),
                    arrowprops=dict(arrowstyle="-|>", color="#4472C4",
                                   lw=1.2, connectionstyle="arc3,rad=-0.4"))

    # contraction factor
    ax.annotate("", xy=(pts[1], -1.0), xytext=(pts[0], -1.0),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=1.8))
    ax.annotate("", xy=(pts[2], -1.0), xytext=(pts[1], -1.0),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=1.4))
    ax.text((pts[0]+pts[1])/2, -1.35, "|T(x)-T(y)| <= c*|x-y|  (c<1)",
            ha="center", fontsize=9, fontfamily=FONT_CODE, color="#7F5F00")

    ax.set_title("fig-15  Shukusho-shasou no hanpuku-zu",
                 fontsize=11, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-15")

# =============================================================================
# fig-16  Banach fixed-point theorem proof tree
# =============================================================================
def fig16():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")

    def node(x, y, text, sub, fc, ec, fontsize=10):
        box = FancyBboxPatch((x - 2.2, y - 0.55), 4.4, 1.2,
                             boxstyle="round,pad=0.15",
                             facecolor=fc, edgecolor=ec, lw=2, zorder=3)
        ax.add_patch(box)
        ax.text(x, y + 0.25, text, ha="center", va="center",
                fontsize=fontsize, fontfamily=FONT_CODE,
                fontweight="bold", color=ec, zorder=4)
        ax.text(x, y - 0.18, sub, ha="center", va="center",
                fontsize=7.5, fontfamily=FONT_CODE, color="#555", zorder=4)

    node(5.0, 6.8, "Banach Fixed Point Theorem",
         "T : X->X contraction, X complete => unique fixed point",
         "#FFDEDE", "#C00000", fontsize=11)

    node(2.0, 4.5, "Cauchy Sequence",
         "x_n = T^n(x0)  (cauchySeq_tendsto)",
         "#BDD7EE", "#4472C4")
    node(5.0, 4.5, "Convergence",
         "CauchySeq => converges  (complete_space)",
         "#C6EFCE", "#548235")
    node(8.0, 4.5, "Fixed Point",
         "lim T^n(x0) = x*  s.t. T(x*)=x*",
         "#EEE0FF", "#7030A0")

    # arrows from top to three branches
    for bx in [2.0, 5.0, 8.0]:
        ax.annotate("", xy=(bx, 5.1), xytext=(5.0, 6.2),
                    arrowprops=dict(arrowstyle="-|>", color="#888", lw=1.5))

    # Mathlib lemma labels
    lemmas = [
        (2.0, 3.6, "Mathlib: cauchySeq_tendsto_of_complete"),
        (5.0, 3.6, "Mathlib: CompleteSpace.complete"),
        (8.0, 3.6, "Mathlib: ContractingWith.fixedPoint"),
    ]
    for lx, ly, txt in lemmas:
        ax.text(lx, ly, txt, ha="center", fontsize=7, fontfamily=FONT_CODE,
                color="#4472C4", style="italic")

    ax.set_title("fig-16  Banach Fudou-ten Teiri no shoumei-kouzou",
                 fontsize=12, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-16")

# =============================================================================
# fig-17  Series roadmap (vol2 highlighted)
# =============================================================================
def fig17():
    fig, ax = plt.subplots(figsize=(12, 4.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis("off")

    vols = [
        ("Vol.1", "Lean 4 nyuumon\nkei-gaku / Mathlib", "#D9D9D9", "#999", False),
        ("Vol.2", "Iso-kuukan / Kyo-ri-kuukan\nFilter / e-d", "#2E75B6", "#1F4E79", True),
        ("Vol.3", "Lebesgue-sekibun\nSokudo-ron", "#D9D9D9", "#999", False),
        ("Vol.4", "Kaku-ritsu Bibun\nHoteishiki (SDE)", "#D9D9D9", "#999", False),
    ]
    xs = [1.2, 3.8, 6.4, 9.0]
    for (label, desc, fc, ec, current), x in zip(vols, xs):
        lw = 3.5 if current else 1.5
        box = FancyBboxPatch((x - 1.0, 0.8), 2.2, 3.2,
                             boxstyle="round,pad=0.15",
                             facecolor=fc, edgecolor=ec, lw=lw, zorder=3)
        ax.add_patch(box)
        ax.text(x + 0.1, 3.5, label, ha="center", fontsize=13,
                fontfamily=FONT_CODE, fontweight="bold",
                color=ec, zorder=4)
        ax.text(x + 0.1, 2.3, desc, ha="center", fontsize=9,
                fontfamily=FONT_CODE, color=ec, linespacing=1.5, zorder=4)
        if current:
            ax.text(x + 0.1, 1.3, "<<  ima koko  >>", ha="center",
                    fontsize=11, fontfamily=FONT_JP,
                    fontweight="bold", color="#C00000", zorder=5)

    # arrows between volumes
    for x1, x2 in zip(xs[:-1], xs[1:]):
        ax.annotate("", xy=(x2 - 1.05, 2.4), xytext=(x1 + 1.15, 2.4),
                    arrowprops=dict(arrowstyle="-|>", color="#bbb", lw=2))

    ax.text(6.0, 4.7, "Lean 4 Keishiki-ka Shiriizu Rodo-mappu (Vol.2 kyouchou)",
            ha="center", fontsize=12, fontfamily=FONT_JP,
            fontweight="bold", color="#1F4E79")
    save(fig, "fig-17")

# =============================================================================
# fig-18  Filter.Tendsto vs e-d correspondence
# =============================================================================
def fig18():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")

    # left box: e-d
    box_l = FancyBboxPatch((0.3, 0.5), 4.5, 5.0,
                           boxstyle="round,pad=0.2",
                           facecolor="#DDEEFF", edgecolor="#4472C4", lw=2)
    ax.add_patch(box_l)
    ax.text(2.55, 5.2, "e-d  definition", ha="center", fontsize=12,
            fontfamily=FONT_CODE, fontweight="bold", color="#1F4E79")
    ax.text(2.55, 3.9,
            "For all e > 0,",
            ha="center", fontsize=11, fontfamily=FONT_CODE, color="#222")
    ax.text(2.55, 3.2,
            "exists d > 0:",
            ha="center", fontsize=11, fontfamily=FONT_CODE, color="#222")
    ax.text(2.55, 2.5,
            "|x - a| < d",
            ha="center", fontsize=11, fontfamily=FONT_CODE,
            color="#C00000", fontweight="bold")
    ax.text(2.55, 1.9,
            "  ->  |f(x) - L| < e",
            ha="center", fontsize=11, fontfamily=FONT_CODE,
            color="#548235", fontweight="bold")

    # colored annotations
    ann = [
        (1.3, 4.35, "e", "#548235"),
        (1.3, 3.65, "d", "#C00000"),
    ]
    for ax2, ay2, lbl, c in ann:
        ax.text(ax2, ay2, lbl, fontsize=16, fontfamily=FONT_CODE,
                fontweight="bold", color=c, alpha=0.4)

    # right box: Filter
    box_r = FancyBboxPatch((7.2, 0.5), 4.5, 5.0,
                           boxstyle="round,pad=0.2",
                           facecolor="#EEE0FF", edgecolor="#7030A0", lw=2)
    ax.add_patch(box_r)
    ax.text(9.45, 5.2, "Filter definition", ha="center", fontsize=12,
            fontfamily=FONT_CODE, fontweight="bold", color="#7030A0")
    ax.text(9.45, 3.8,
            "Filter.Tendsto f",
            ha="center", fontsize=12, fontfamily=FONT_CODE,
            color="#222", fontweight="bold")
    ax.text(9.45, 3.1,
            "  (nhds a)",
            ha="center", fontsize=12, fontfamily=FONT_CODE,
            color="#C00000", fontweight="bold")
    ax.text(9.45, 2.4,
            "  (nhds L)",
            ha="center", fontsize=12, fontfamily=FONT_CODE,
            color="#548235", fontweight="bold")

    ann2 = [
        (7.5, 3.55, "nhds a", "#C00000"),
        (7.5, 2.85, "nhds L", "#548235"),
    ]
    for ax2, ay2, lbl, c in ann2:
        ax.text(ax2, ay2, lbl, fontsize=9, fontfamily=FONT_CODE,
                color=c, alpha=0.45)

    # center arrow
    ax.annotate("", xy=(7.1, 3.0), xytext=(4.9, 3.0),
                arrowprops=dict(arrowstyle="<->", color="#C9A800",
                                lw=3.0, mutation_scale=22))
    ax.text(6.0, 3.55, "<=>", ha="center", fontsize=18,
            fontfamily=FONT_CODE, color="#7F5F00", fontweight="bold")
    ax.text(6.0, 2.5, "equivalent", ha="center", fontsize=10,
            fontfamily=FONT_CODE, color="#7F5F00")

    ax.set_title("fig-18  Filter.Tendsto to e-d no taiou-zu",
                 fontsize=12, fontfamily=FONT_CODE, pad=8, color="#555")
    save(fig, "fig-18")


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    funcs = [
        fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09,
        fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18,
    ]
    for i, fn in enumerate(funcs, 1):
        print(f"generating fig-{i:02d} ...")
        fn()
    print("Done.")
