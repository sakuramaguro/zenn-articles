#!/usr/bin/env python3
"""Generate vol2 figures fig-01 through fig-18 with proper Japanese fonts."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Arc, Circle, Ellipse
import matplotlib.font_manager as fm
import numpy as np
import os

# ── 日本語フォント設定 ──────────────────────────────────────────────────────
jp_fonts = [f.name for f in fm.fontManager.ttflist if 'Hiragino' in f.name]
if jp_fonts:
    FONT_JP = jp_fonts[0]
else:
    FONT_JP = "DejaVu Sans"
print(f"Using Japanese font: {FONT_JP}")

FONT_CODE = "Courier New"
DPI = 300
OUT = os.path.expanduser("~/zenn-articles/images/vol2")

plt.rcParams.update({
    "font.family": [FONT_JP, "STIXGeneral", "DejaVu Sans"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

def save(fig, name):
    svg_path = os.path.join(OUT, f"{name}.svg")
    png_path = os.path.join(OUT, f"{name}.png")
    fig.savefig(svg_path, format="svg", bbox_inches="tight", dpi=DPI)
    fig.savefig(png_path, format="png", bbox_inches="tight", dpi=DPI,
                facecolor="white")
    plt.close(fig)
    print(f"  saved {name}.svg / {name}.png")


# =============================================================================
# fig-01  フィルターの望遠鏡比喩図
# =============================================================================
def fig01():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10); ax.set_ylim(-1.5, 2.5); ax.axis("off")

    # 数直線
    ax.annotate("", xy=(4.0, 0), xytext=(0.5, 0),
                arrowprops=dict(arrowstyle="-|>", color="#333"))
    # 収束点 1/n
    xs = [3.5, 2.5, 1.8, 1.4, 1.15, 1.05, 1.01]
    for i, x in enumerate(xs):
        ax.plot(x, 0, "o", color="#4472C4", markersize=6 - i * 0.6, zorder=3)
        if i < 4:
            ax.text(x, -0.35, f"1/{i+1}", ha="center", fontsize=8,
                    fontfamily=FONT_CODE, color="#4472C4")
    ax.text(1.0, -0.35, "...", ha="center", fontsize=9, color="#4472C4")
    ax.text(2.0, 1.5, "1/n  →  0", ha="center", fontsize=11,
            fontfamily=FONT_CODE, color="#4472C4", style="italic")

    # ファネル（台形）
    trap = plt.Polygon([[4.2, 1.0],[5.8, 1.8],[5.8,-1.0],[4.2,-1.0]],
                       closed=True, facecolor="#FFF2CC", edgecolor="#C9A800", lw=2)
    ax.add_patch(trap)
    ax.text(5.0, 0.15, "フィルター", ha="center", va="center", fontsize=13,
            fontweight="bold", color="#7F5F00")
    ax.text(5.0, -0.55, "（特定の集合族を通す）", ha="center",
            fontsize=7.5, color="#7F5F00")

    # 結果への矢印
    ax.annotate("", xy=(7.5, 0), xytext=(6.0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))
    ax.text(9.0, 0, "0", ha="center", va="center", fontsize=28,
            fontweight="bold", color="#C00000")
    ax.text(9.0, -0.6, "収束先", ha="center", fontsize=9, color="#C00000")

    ax.set_title("フィルターの望遠鏡比喩", fontsize=13, pad=10)
    save(fig, "fig-01")


# =============================================================================
# fig-02  nhds の同心円図（距離空間）
# =============================================================================
def fig02():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)
    ax.axis("off")

    colors = ["#BDD7EE", "#9DC3E6", "#5B9BD5", "#2E75B6"]
    radii  = [3.2, 2.4, 1.6, 0.8]
    labels = ["U（開集合）", "B(x, 2ε)", "B(x, ε)", "B(x, ε/2)"]

    for r, c, lbl in zip(radii, colors, labels):
        circ = Circle((0, 0), r, facecolor=c, edgecolor="#2E75B6",
                      lw=1.5, alpha=0.5, linestyle="--")
        ax.add_patch(circ)
        ax.text(r * 0.72, r * 0.72, lbl, fontsize=9,
                ha="left", va="bottom", color="#1F4E79")

    ax.plot(0, 0, "o", color="#C00000", markersize=8, zorder=5)
    ax.text(0.15, 0.15, "x", fontsize=14, fontweight="bold", color="#C00000")

    ax.set_title("nhds x の同心円（距離空間）", fontsize=13, pad=10)
    ax.text(0, -3.8, "nhds x = x を含むすべての開近傍の族",
            ha="center", fontsize=10, color="#1F4E79",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#DEEAF1", edgecolor="#2E75B6"))
    save(fig, "fig-02")


# =============================================================================
# fig-03  Filter.Tendsto の概念図
# =============================================================================
def fig03():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

    # X 楕円
    ex = Ellipse((2.5, 2.5), 4.0, 3.8, facecolor="#DEEAF1",
                 edgecolor="#2E75B6", lw=2, alpha=0.7)
    ax.add_patch(ex)
    ax.text(2.5, 4.3, "X（例: ℝ）", ha="center", fontsize=12, color="#1F4E79", fontweight="bold")

    # Y 楕円
    ey = Ellipse((7.5, 2.5), 4.0, 3.8, facecolor="#E2EFDA",
                 edgecolor="#538135", lw=2, alpha=0.7)
    ax.add_patch(ey)
    ax.text(7.5, 4.3, "Y（例: ℝ）", ha="center", fontsize=12, color="#375623", fontweight="bold")

    # フィルター F in X
    fx = Ellipse((2.0, 2.5), 1.4, 2.2, facecolor="#BDD7EE",
                 edgecolor="#2E75B6", lw=1.5, alpha=0.8)
    ax.add_patch(fx)
    ax.text(2.0, 2.5, "𝓕", ha="center", va="center", fontsize=18, color="#1F4E79")
    ax.text(2.0, 1.3, "（フィルター）", ha="center", fontsize=8, color="#1F4E79")

    # フィルター G in Y
    fy = Ellipse((7.5, 2.5), 1.4, 2.2, facecolor="#C6EFCE",
                 edgecolor="#538135", lw=1.5, alpha=0.8)
    ax.add_patch(fy)
    ax.text(7.5, 2.5, "𝓖", ha="center", va="center", fontsize=18, color="#375623")
    ax.text(7.5, 1.3, "（フィルター）", ha="center", fontsize=8, color="#375623")

    # f: X → Y 矢印
    ax.annotate("", xy=(5.8, 2.5), xytext=(4.2, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=2))
    ax.text(5.0, 2.9, "f", ha="center", fontsize=14, fontweight="bold", color="#333")

    # Filter.Tendsto ラベル
    ax.text(5.0, 0.4, "Filter.Tendsto f 𝓕 𝓖  ⟺  map f 𝓕 ≤ 𝓖",
            ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF2CC", edgecolor="#C9A800"))

    ax.set_title("Filter.Tendsto の概念図", fontsize=13, pad=10)
    save(fig, "fig-03")


# =============================================================================
# fig-04  距離の三角不等式
# =============================================================================
def fig04():
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.5, 8); ax.set_ylim(-0.5, 5); ax.axis("off")

    # 三点
    pts = {"x": (1.0, 1.0), "y": (6.0, 4.0), "z": (6.5, 1.0)}
    cols = {"x": "#C00000", "y": "#2E75B6", "z": "#538135"}

    # 辺
    for (a, b), color, style in [
        (("x","y"), "#4472C4", "-"),
        (("y","z"), "#4472C4", "-"),
        (("x","z"), "#C00000", "--"),
    ]:
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]],
                color=color, lw=2, linestyle=style)

    # 距離ラベル
    mx, my = (pts["x"][0]+pts["y"][0])/2, (pts["x"][1]+pts["y"][1])/2
    ax.text(mx-0.5, my+0.2, "d(x,y)", fontsize=11, color="#4472C4", fontweight="bold")
    mx2, my2 = (pts["y"][0]+pts["z"][0])/2, (pts["y"][1]+pts["z"][1])/2
    ax.text(mx2+0.1, my2, "d(y,z)", fontsize=11, color="#4472C4", fontweight="bold")
    mx3, my3 = (pts["x"][0]+pts["z"][0])/2, (pts["x"][1]+pts["z"][1])/2
    ax.text(mx3, my3-0.4, "d(x,z)", fontsize=11, color="#C00000", fontweight="bold")

    # 点
    for name, (px, py) in pts.items():
        ax.plot(px, py, "o", color=cols[name], markersize=10, zorder=5)
        offset = {"x": (-0.3, -0.3), "y": (0.1, 0.1), "z": (0.1, -0.3)}
        ox, oy = offset[name]
        ax.text(px+ox, py+oy, name, fontsize=14, fontweight="bold", color=cols[name])

    # 不等式ボックス
    ax.text(3.5, 2.5,
            "d(x,z) ≤ d(x,y) + d(y,z)",
            ha="center", fontsize=13,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF2CC",
                      edgecolor="#C9A800", lw=2))

    ax.set_title("距離の三角不等式", fontsize=13, pad=10)
    save(fig, "fig-04")


# =============================================================================
# fig-05  ε-近傍と開球
# =============================================================================
def fig05():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4, 4)
    ax.axis("off")

    # 外側（参考）
    outer = Circle((0, 0), 3.0, facecolor="#FFF2CC", edgecolor="#C9A800",
                   lw=1.5, alpha=0.4, linestyle="--")
    ax.add_patch(outer)

    # 開球 B(x, ε)
    ball = Circle((0, 0), 2.0, facecolor="#BDD7EE", edgecolor="#2E75B6",
                  lw=2.5, alpha=0.6, linestyle="--")
    ax.add_patch(ball)

    # 中心
    ax.plot(0, 0, "o", color="#C00000", markersize=8, zorder=5)
    ax.text(0.15, 0.2, "x", fontsize=14, fontweight="bold", color="#C00000")

    # ε 矢印
    ax.annotate("", xy=(2.0, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="<->", color="#333", lw=1.5))
    ax.text(1.0, 0.25, "ε", fontsize=14, ha="center", color="#333", fontweight="bold")

    # 境界点（境界は含まない）
    ax.plot(2.0, 0, "o", color="#2E75B6", markersize=10,
            markerfacecolor="white", markeredgewidth=2, zorder=5)
    ax.text(2.1, 0.25, "（境界を含まない）", fontsize=9, color="#2E75B6")

    ax.set_title("ε-近傍と開球 B(x, ε)", fontsize=13, pad=10)

    # キャプション
    ax.text(0, -3.5, "B(x, ε) = {y | d(x,y) < ε}",
            ha="center", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#DEEAF1", edgecolor="#2E75B6"))
    ax.text(0, -4.1, "（境界を含まない = 開集合）",
            ha="center", fontsize=10, color="#1F4E79")

    save(fig, "fig-05")


# =============================================================================
# fig-06  MetricSpace の継承図
# =============================================================================
def fig06():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    boxes = [
        (5.0, 8.5, "MetricSpace\nd(x,y)=0 ↔ x=y（分離公理）", "#C00000", "#FFCCCC"),
        (5.0, 6.2, "PseudoMetricSpace\nx≠y でも d(x,y)=0 を許す", "#2E75B6", "#DEEAF1"),
        (5.0, 3.9, "UniformSpace\n一様連続性・Cauchy フィルター", "#538135", "#E2EFDA"),
        (5.0, 1.6, "TopologicalSpace\n開集合・nhds フィルター", "#7030A0", "#EAD1F5"),
    ]

    for (cx, cy, text, ec, fc) in boxes:
        bbox = FancyBboxPatch((cx-3.2, cy-0.85), 6.4, 1.7,
                              boxstyle="round,pad=0.15",
                              facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(bbox)
        lines = text.split("\n")
        ax.text(cx, cy+0.25, lines[0], ha="center", va="center",
                fontsize=11, fontweight="bold", color=ec)
        if len(lines) > 1:
            ax.text(cx, cy-0.3, lines[1], ha="center", va="center",
                    fontsize=9, color=ec)

    # 矢印
    ys = [7.65, 5.35, 3.05]
    colors_arr = ["#C00000", "#2E75B6", "#538135"]
    for y, col in zip(ys, colors_arr):
        ax.annotate("", xy=(5.0, y-0.5), xytext=(5.0, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
        ax.text(5.4, y-0.25, "extends", fontsize=9, color=col)

    ax.set_title("MetricSpace の継承図（Lean 4）", fontsize=13, pad=10)
    save(fig, "fig-06")


# =============================================================================
# fig-07  連続性の3同値条件
# =============================================================================
def fig07():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis("off")

    boxes = [
        (2.0, 2.5, "ε-δ 定義",
         "∀ε>0, ∃δ>0,\nd(x,y)<δ ⟹ d(f(x),f(y))<ε",
         "#C00000", "#FFCCCC"),
        (5.5, 2.5, "開集合による定義",
         "V 開集合 ⟹\nf⁻¹(V) 開集合",
         "#2E75B6", "#DEEAF1"),
        (9.0, 2.5, "フィルター（Lean）",
         "Filter.Tendsto f\n  (nhds x) (nhds (f x))",
         "#538135", "#E2EFDA"),
    ]

    for (cx, cy, title, body, ec, fc) in boxes:
        bbox = FancyBboxPatch((cx-1.7, cy-1.6), 3.4, 3.2,
                              boxstyle="round,pad=0.2",
                              facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(bbox)
        ax.text(cx, cy+0.9, title, ha="center", va="center",
                fontsize=11, fontweight="bold", color=ec)
        ax.text(cx, cy-0.1, body, ha="center", va="center",
                fontsize=8.5, color="#333")

    # 同値矢印
    for x1, x2 in [(3.7, 3.8), (7.2, 7.3)]:
        ax.annotate("", xy=(x2, 2.5), xytext=(x1, 2.5),
                    arrowprops=dict(arrowstyle="<->", color="#555", lw=2))
        ax.text((x1+x2)/2, 2.8, "同値", ha="center", fontsize=9, color="#555")

    ax.set_title("連続性の3つの同値条件", fontsize=13, pad=10)
    save(fig, "fig-07")


# =============================================================================
# fig-08  nhds の同心円図（位相空間版）
# =============================================================================
def fig08():
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_aspect("equal"); ax.set_xlim(-4, 4); ax.set_ylim(-4.5, 4.5)
    ax.axis("off")

    # 不規則な「開集合」を楕円で表現
    shapes = [
        (Ellipse((0, 0), 6.0, 5.5, angle=15), "#BDD7EE", "#2E75B6", "U₁（開集合）", 3.0, 2.3),
        (Ellipse((0.2, 0), 4.5, 4.0, angle=-10), "#9DC3E6", "#2E75B6", "U₂（開集合）", 2.3, 1.6),
        (Ellipse((-0.1, 0.1), 2.8, 2.5, angle=5), "#5B9BD5", "#1F4E79", "U₃（開集合）", 1.4, 0.95),
    ]

    for (shape, fc, ec, lbl, tx, ty) in shapes:
        shape.set_facecolor(fc); shape.set_edgecolor(ec)
        shape.set_alpha(0.45); shape.set_linewidth(1.5)
        shape.set_linestyle("--")
        ax.add_patch(shape)
        ax.text(tx, ty, lbl, fontsize=8.5, ha="left", color="#1F4E79")

    ax.plot(0, 0, "o", color="#C00000", markersize=8, zorder=5)
    ax.text(0.15, 0.2, "x", fontsize=14, fontweight="bold", color="#C00000")

    ax.set_title("nhds x の構造（位相空間版）", fontsize=13, pad=10)
    ax.text(0, -3.8, "距離なし — x を含む開集合のみ",
            ha="center", fontsize=10, color="#1F4E79")
    ax.text(0, -4.35, "nhds x = ⨅ { P(U) | U open, x ∈ U }",
            ha="center", fontsize=9, color="#1F4E79",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#DEEAF1", edgecolor="#2E75B6"))

    save(fig, "fig-08")


# =============================================================================
# fig-09  開集合と閉集合
# =============================================================================
def fig09():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")

    # U（開集合）- 左半分
    u_patch = Ellipse((3.0, 2.5), 5.0, 3.5, facecolor="#DEEAF1",
                      edgecolor="#2E75B6", lw=2.5, linestyle="--", alpha=0.7)
    ax.add_patch(u_patch)
    ax.text(3.0, 2.5, "U（開集合）", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#1F4E79")
    ax.text(3.0, 1.5, "（点線 = 境界を含まない）", ha="center",
            fontsize=9, color="#1F4E79")

    # 補集合 Uᶜ（閉集合）- 右半分
    uc_patch = patches.FancyBboxPatch((5.8, 0.5), 3.8, 4.0,
                                       boxstyle="round,pad=0.1",
                                       facecolor="#FCE4D6", edgecolor="#C00000",
                                       lw=2.5, linestyle="-", alpha=0.7)
    ax.add_patch(uc_patch)
    ax.text(7.7, 2.5, "Uᶜ（閉集合）", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#C00000")

    # 補集合矢印
    ax.annotate("", xy=(6.5, 3.5), xytext=(4.8, 3.5),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5))
    ax.text(5.65, 3.8, "補集合", ha="center", fontsize=9, color="#555")

    ax.set_title("開集合と閉集合の関係", fontsize=13, pad=10)
    ax.text(5.0, 0.2, "開集合の補集合 = 閉集合",
            ha="center", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF2CC", edgecolor="#C9A800"))
    save(fig, "fig-09")


# =============================================================================
# fig-10  開被覆とコンパクト性
# =============================================================================
def fig10():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(-1, 11); ax.set_ylim(-1, 6); ax.axis("off")

    # コンパクト集合 K
    K = Ellipse((5, 3), 8.5, 4.2, facecolor="#FFF2CC", edgecolor="#C9A800",
                lw=2.5, alpha=0.5)
    ax.add_patch(K)
    ax.text(5, 5.2, "K（コンパクト集合）", ha="center", fontsize=12,
            fontweight="bold", color="#7F5F00")

    # 開被覆の円たち
    covers = [
        Circle((2.5, 3.2), 1.8, facecolor="#DEEAF1", edgecolor="#2E75B6",
               lw=1.5, alpha=0.55, linestyle="--"),
        Circle((4.8, 2.2), 2.0, facecolor="#E2EFDA", edgecolor="#538135",
               lw=1.5, alpha=0.55, linestyle="--"),
        Circle((7.2, 3.5), 1.7, facecolor="#EAD1F5", edgecolor="#7030A0",
               lw=1.5, alpha=0.55, linestyle="--"),
        Circle((5.5, 4.2), 1.4, facecolor="#FCE4D6", edgecolor="#C00000",
               lw=1.5, alpha=0.55, linestyle="--"),
    ]
    labels = ["U₁", "U₂", "U₃", "U₄"]
    cols = ["#1F4E79", "#375623", "#4B0082", "#C00000"]

    for circ, lbl, col in zip(covers, labels, cols):
        ax.add_patch(circ)
        cx, cy = circ.center
        ax.text(cx, cy, lbl, ha="center", va="center",
                fontsize=11, fontweight="bold", color=col)

    ax.set_title("開被覆とコンパクト性", fontsize=13, pad=10)
    ax.text(5, -0.6,
            "コンパクト ⟺ 任意の開被覆から有限部分被覆が取れる",
            ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF2CC", edgecolor="#C9A800"))
    save(fig, "fig-10")


# =============================================================================
# fig-11  Cauchy 列と完備性
# =============================================================================
def fig11():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Cauchy 列と完備性", fontsize=14, fontweight="bold", y=1.02)

    for ax in [ax1, ax2]:
        ax.set_xlim(-0.5, 7); ax.set_ylim(-0.5, 4)
        ax.axis("off")

    # 左：完備（ℝ）
    ax1.set_title("完備（例: ℝ）", fontsize=12, color="#2E75B6", fontweight="bold")
    xs = [1.0, 2.0, 2.8, 3.3, 3.6, 3.8, 3.9, 3.95, 4.0]
    ys = [3.0, 2.5, 2.1, 1.85, 1.7, 1.62, 1.58, 1.55, 1.53]
    ax1.plot(xs, ys, "o-", color="#2E75B6", markersize=6)
    ax1.plot(xs[-1], ys[-1], "*", color="#C00000", markersize=15, zorder=5)
    ax1.annotate("極限点 (収束先)", xy=(xs[-1], ys[-1]),
                 xytext=(xs[-1]+0.3, ys[-1]+0.5),
                 fontsize=9, color="#C00000",
                 arrowprops=dict(arrowstyle="->", color="#C00000"))
    ax1.text(2.5, 0.2, "すべての Cauchy 列が収束する",
             ha="center", fontsize=9, color="#2E75B6",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#DEEAF1", edgecolor="#2E75B6"))

    # 右：不完備（ℚ）
    ax2.set_title("不完備（例: ℚ）", fontsize=12, color="#C00000", fontweight="bold")
    xs2 = [1.0, 2.0, 2.8, 3.2, 3.5, 3.65, 3.72]
    ys2 = [3.0, 2.5, 2.1, 1.88, 1.75, 1.68, 1.64]
    ax2.plot(xs2, ys2, "o-", color="#C00000", markersize=6)
    # 行き先（irrational）はℚにない
    ax2.plot(4.2, 1.52, "x", color="#C00000", markersize=12, mew=3, zorder=5)
    ax2.annotate("√2 ∉ ℚ\n（収束先がℚにない）",
                 xy=(4.2, 1.52), xytext=(4.5, 2.2),
                 fontsize=9, color="#C00000",
                 arrowprops=dict(arrowstyle="->", color="#C00000"))
    ax2.text(2.5, 0.2, "ℚ 内の Cauchy 列が ℚ に収束しない",
             ha="center", fontsize=9, color="#C00000",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#FCE4D6", edgecolor="#C00000"))

    plt.tight_layout()
    save(fig, "fig-11")


# =============================================================================
# fig-12  UniformSpace の構造図
# =============================================================================
def fig12():
    fig, ax = plt.subplots(figsize=(8, 9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    boxes = [
        (5.0, 8.5, "TopologicalSpace\n（開集合・nhds）", "#7030A0", "#EAD1F5"),
        (5.0, 6.3, "UniformSpace\n（一様連続性・Cauchy）", "#538135", "#E2EFDA"),
        (5.0, 4.1, "PseudoMetricSpace\n（d ≥ 0, 三角不等式）", "#2E75B6", "#DEEAF1"),
        (5.0, 1.9, "MetricSpace\n（d=0 ↔ x=y）", "#C00000", "#FFCCCC"),
    ]

    for (cx, cy, text, ec, fc) in boxes:
        bbox = FancyBboxPatch((cx-3.0, cy-0.85), 6.0, 1.7,
                              boxstyle="round,pad=0.15",
                              facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(bbox)
        lines = text.split("\n")
        ax.text(cx, cy+0.28, lines[0], ha="center", va="center",
                fontsize=11, fontweight="bold", color=ec)
        ax.text(cx, cy-0.28, lines[1], ha="center", va="center",
                fontsize=9, color=ec)

    # 矢印（下から上：TopologicalSpace が最も一般）
    for y_from, y_to, col in [(2.75, 3.25, "#C00000"),
                               (4.95, 5.45, "#2E75B6"),
                               (7.15, 7.65, "#538135")]:
        ax.annotate("", xy=(5.0, y_to), xytext=(5.0, y_from),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2))

    ax.text(5.5, 3.0, "extends", fontsize=9, color="#C00000")
    ax.text(5.5, 5.2, "extends", fontsize=9, color="#2E75B6")
    ax.text(5.5, 7.4, "extends", fontsize=9, color="#538135")

    ax.set_title("UniformSpace の構造（包含関係）", fontsize=13, pad=10)
    save(fig, "fig-12")


# =============================================================================
# fig-13  ℓ² 空間の単位球
# =============================================================================
def fig13():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle("ℓ² 空間の単位球", fontsize=14, fontweight="bold")

    # 左：2D 単位球（円）
    ax1.set_title("2D: ℓ² 単位球（円）", fontsize=11, color="#2E75B6")
    theta = np.linspace(0, 2*np.pi, 300)
    ax1.fill(np.cos(theta), np.sin(theta), color="#BDD7EE", alpha=0.6)
    ax1.plot(np.cos(theta), np.sin(theta), color="#2E75B6", lw=2)
    ax1.plot(0, 0, "o", color="#C00000", markersize=6)
    ax1.annotate("", xy=(1, 0), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="<->", color="#333"))
    ax1.text(0.5, 0.1, "r=1", ha="center", fontsize=10)
    ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect("equal")
    ax1.axhline(0, color="#ddd", lw=0.5)
    ax1.axvline(0, color="#ddd", lw=0.5)

    # 右：3D 断面図（赤道面、ℓ²={x₁²+x₂²+x₃²≤1} の x₃=0 断面）
    ax2.set_title("3D 断面（赤道面）", fontsize=11, color="#538135")
    ax2.fill(np.cos(theta), np.sin(theta), color="#C6EFCE", alpha=0.6)
    ax2.plot(np.cos(theta), np.sin(theta), color="#538135", lw=2)
    ax2.plot(0, 0, "o", color="#C00000", markersize=6)
    ax2.set_xlim(-1.5, 1.5); ax2.set_ylim(-1.5, 1.5)
    ax2.set_aspect("equal")
    ax2.set_xlabel("x₁"); ax2.set_ylabel("x₂")
    ax2.axhline(0, color="#ddd", lw=0.5)
    ax2.axvline(0, color="#ddd", lw=0.5)
    ax2.text(0, -1.4,
             "{(x₁,x₂) | x₁²+x₂² ≤ 1}（x₃=0 断面）",
             ha="center", fontsize=9, color="#375623")

    plt.tight_layout()
    save(fig, "fig-13")


# =============================================================================
# fig-14  有限次元 vs 無限次元
# =============================================================================
def fig14():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis("off")

    # ヘッダー
    ax.add_patch(FancyBboxPatch((0.5, 5.5), 4.5, 1.2, boxstyle="round,pad=0.1",
                                facecolor="#DEEAF1", edgecolor="#2E75B6", lw=2))
    ax.text(2.75, 6.1, "有限次元（ℝⁿ）", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#1F4E79")

    ax.add_patch(FancyBboxPatch((6.0, 5.5), 4.5, 1.2, boxstyle="round,pad=0.1",
                                facecolor="#E2EFDA", edgecolor="#538135", lw=2))
    ax.text(8.25, 6.1, "無限次元（ℓ²）", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#375623")

    # 行データ
    rows = [
        ("有界閉集合", "コンパクト", "コンパクトとは限らない"),
        ("単位球", "コンパクト", "コンパクトでない"),
        ("有界列", "収束部分列あり", "収束部分列なし"),
        ("具体例", "ℝ, ℝ², ℝ³, ...", "ℓ², L², C([0,1])"),
    ]

    y_positions = [4.4, 3.3, 2.2, 1.1]
    row_colors = ["#DEEAF1", "#E8F4FD", "#DEEAF1", "#E8F4FD"]
    row_colors_r = ["#E2EFDA", "#EDF7E6", "#E2EFDA", "#EDF7E6"]

    for (label, left, right), y, fc_l, fc_r in zip(rows, y_positions, row_colors, row_colors_r):
        # 行ラベル
        ax.add_patch(FancyBboxPatch((-0.3, y-0.5), 1.3, 1.0,
                                     boxstyle="square,pad=0", facecolor="#F2F2F2",
                                     edgecolor="#999", lw=0.5))
        ax.text(0.35, y, label, ha="center", va="center", fontsize=9, color="#333")

        ax.add_patch(FancyBboxPatch((1.0, y-0.5), 4.0, 1.0,
                                     boxstyle="square,pad=0", facecolor=fc_l,
                                     edgecolor="#2E75B6", lw=0.5))
        ax.text(3.0, y, left, ha="center", va="center", fontsize=10, color="#1F4E79")

        ax.add_patch(FancyBboxPatch((5.5, y-0.5), 5.0, 1.0,
                                     boxstyle="square,pad=0", facecolor=fc_r,
                                     edgecolor="#538135", lw=0.5))
        ax.text(8.0, y, right, ha="center", va="center", fontsize=10, color="#375623")

    ax.set_title("有限次元 vs 無限次元の違い", fontsize=13, pad=10)
    save(fig, "fig-14")


# =============================================================================
# fig-15  縮小写像の反復と不動点
# =============================================================================
def fig15():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 9); ax.set_ylim(-0.5, 5); ax.axis("off")

    # 数直線
    ax.annotate("", xy=(8.5, 1.5), xytext=(0.5, 1.5),
                arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.5))

    # 反復点
    pts = [7.5, 6.2, 5.3, 4.7, 4.3, 4.1, 4.0]
    colors_pt = plt.cm.Blues(np.linspace(0.4, 0.9, len(pts)))
    for i, (x, col) in enumerate(zip(pts, colors_pt)):
        ax.plot(x, 1.5, "o", color=col, markersize=8-i*0.7, zorder=4)
        label = f"x_{i}" if i < 4 else ("..." if i == 4 else "")
        if label:
            ax.text(x, 1.1, label, ha="center", fontsize=9, fontfamily=FONT_CODE, color="#1F4E79")

    # 矢印：Tの適用
    for i in range(len(pts)-1):
        ax.annotate("", xy=(pts[i+1], 1.8), xytext=(pts[i], 1.8),
                    arrowprops=dict(arrowstyle="-|>", color="#4472C4", lw=1, connectionstyle="arc3,rad=-0.3"))

    # 不動点
    x_star = 4.0
    ax.plot(x_star, 1.5, "*", color="#C00000", markersize=18, zorder=5)
    ax.text(x_star, 0.8, "x*（不動点）", ha="center", fontsize=10,
            fontweight="bold", color="#C00000")

    # T の説明
    ax.text(5.5, 3.2, "T(xₙ) = xₙ₊₁", ha="center", fontsize=12,
            color="#4472C4",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#DEEAF1", edgecolor="#2E75B6"))

    ax.set_title("縮小写像の反復と不動点", fontsize=13, pad=10)
    ax.text(4.5, -0.3, "|T(x) - T(y)| ≤ c·|x-y|（c<1）",
            ha="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF2CC", edgecolor="#C9A800"))
    save(fig, "fig-15")


# =============================================================================
# fig-16  Banach 不動点定理の証明構造図
# =============================================================================
def fig16():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")

    # 頂点：定理
    top_box = FancyBboxPatch((2.5, 5.8), 9.0, 1.8,
                              boxstyle="round,pad=0.2",
                              facecolor="#FFF2CC", edgecolor="#C9A800", lw=3)
    ax.add_patch(top_box)
    ax.text(7.0, 6.9, "Banach 不動点定理",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#7F5F00")
    ax.text(7.0, 6.3, "T: X→X 縮小写像, X 完備  ⟹  唯一の不動点",
            ha="center", va="center", fontsize=10, color="#7F5F00")

    # 下3ボックス
    sub_boxes = [
        (2.2, 2.5, 2.8, "Cauchy 列\nx_n = Tⁿ(x₀)", "#2E75B6", "#DEEAF1"),
        (7.0, 2.5, 2.8, "収束\nCauchy ⟹ 収束", "#538135", "#E2EFDA"),
        (11.8, 2.5, 2.8, "不動点\nlim Tⁿ(x₀) = x*", "#C00000", "#FFCCCC"),
    ]

    for (cx, cy, w, text, ec, fc) in sub_boxes:
        bbox = FancyBboxPatch((cx-w/2, cy-0.8), w, 1.6,
                              boxstyle="round,pad=0.2",
                              facecolor=fc, edgecolor=ec, lw=2)
        ax.add_patch(bbox)
        lines = text.split("\n")
        ax.text(cx, cy+0.3, lines[0], ha="center", va="center",
                fontsize=11, fontweight="bold", color=ec)
        ax.text(cx, cy-0.3, lines[1], ha="center", va="center",
                fontsize=9, color=ec)

    # 上から各ボックスへの矢印
    for tx in [2.2, 7.0, 11.8]:
        ax.annotate("", xy=(tx, 3.3), xytext=(7.0, 5.8),
                    arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5,
                                   connectionstyle="arc3,rad=0"))

    # 横矢印
    ax.annotate("", xy=(4.1, 2.5), xytext=(3.0, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5))
    ax.annotate("", xy=(9.1, 2.5), xytext=(8.0, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.5))
    ax.text(3.55, 2.8, "完備性", ha="center", fontsize=9, color="#538135")
    ax.text(8.55, 2.8, "不動点方程式", ha="center", fontsize=9, color="#C00000")

    # 唯一性
    unique_box = FancyBboxPatch((5.5, 0.5), 3.0, 1.2,
                                 boxstyle="round,pad=0.2",
                                 facecolor="#EAD1F5", edgecolor="#7030A0", lw=2)
    ax.add_patch(unique_box)
    ax.text(7.0, 1.1, "唯一性: x* = y* ならば", ha="center", fontsize=10, color="#4B0082")
    ax.text(7.0, 0.75, "d(x*,y*) ≤ c·d(x*,y*) ⟹ d=0", ha="center",
            fontsize=9, color="#4B0082")
    ax.annotate("", xy=(7.0, 1.7), xytext=(7.0, 1.0),
                arrowprops=dict(arrowstyle="-|>", color="#7030A0", lw=1.5))

    ax.set_title("Banach 不動点定理の証明構造", fontsize=14, pad=12)
    save(fig, "fig-16")


# =============================================================================
# fig-17  第2巻シリーズロードマップ
# =============================================================================
def fig17():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12); ax.set_ylim(-0.5, 5); ax.axis("off")

    volumes = [
        (1.5, "第1巻\nLean 4 入門\n型・証明・Mathlib",
         "#538135", "#E2EFDA", False),
        (4.5, "第2巻\n位相空間・距離空間\nFilter・ε-δ\n≪ いまここ ≫",
         "#C00000", "#FFCCCC", True),
        (7.5, "第3巻\nLebesgue 積分\n測度論",
         "#2E75B6", "#DEEAF1", False),
        (10.5, "第4巻\n確率微分方程式\nSDE",
         "#7030A0", "#EAD1F5", False),
    ]

    for i, (cx, text, ec, fc, current) in enumerate(volumes):
        lw = 3.5 if current else 1.8
        h = 3.8 if current else 3.2
        bbox = FancyBboxPatch((cx-1.4, 0.5), 2.8, h,
                              boxstyle="round,pad=0.2",
                              facecolor=fc, edgecolor=ec, lw=lw)
        ax.add_patch(bbox)
        lines = text.split("\n")
        cy = 0.5 + h/2
        for j, line in enumerate(lines):
            offset = (len(lines)-1)/2 - j
            fs = 11 if j == 0 else (10 if current else 9)
            fw = "bold" if j == 0 or "いまここ" in line else "normal"
            ax.text(cx, cy + offset*0.55, line,
                    ha="center", va="center",
                    fontsize=fs, fontweight=fw, color=ec)

    # 矢印
    for x in [2.9, 5.9, 8.9]:
        ax.annotate("", xy=(x+0.1, 2.2), xytext=(x-0.1, 2.2),
                    arrowprops=dict(arrowstyle="-|>", color="#777", lw=2))

    ax.set_title("Lean 4 形式化シリーズ ロードマップ（第2巻）",
                 fontsize=13, pad=10)
    save(fig, "fig-17")


# =============================================================================
# fig-18  Filter.Tendsto ↔ ε-δ 対応図
# =============================================================================
def fig18():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")

    # 左ボックス：ε-δ 定義
    left_box = FancyBboxPatch((0.5, 1.5), 4.0, 4.5,
                               boxstyle="round,pad=0.3",
                               facecolor="#DEEAF1", edgecolor="#2E75B6", lw=2.5)
    ax.add_patch(left_box)
    ax.text(2.5, 5.5, "ε-δ 定義", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#1F4E79")
    lines_left = [
        "∀ε > 0,",
        "∃δ > 0,",
        "∀y, d(x,y) < δ",
        "  ⟹ d(f(x),f(y)) < ε",
    ]
    for i, line in enumerate(lines_left):
        ax.text(2.5, 4.6 - i*0.7, line, ha="center", va="center",
                fontsize=10, color="#1F4E79")

    # 右ボックス：フィルター定義
    right_box = FancyBboxPatch((7.5, 1.5), 4.0, 4.5,
                                boxstyle="round,pad=0.3",
                                facecolor="#E2EFDA", edgecolor="#538135", lw=2.5)
    ax.add_patch(right_box)
    ax.text(9.5, 5.5, "フィルター定義", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#375623")
    lines_right = [
        "Filter.Tendsto f",
        "  (nhds x)",
        "  (nhds (f x))",
        "",
        "⟺ map f (nhds x)",
        "    ≤ nhds (f x)",
    ]
    for i, line in enumerate(lines_right):
        ax.text(9.5, 4.6 - i*0.58, line, ha="center", va="center",
                fontsize=9.5, color="#375623")

    # 中央：同値
    ax.add_patch(FancyBboxPatch((4.8, 2.8), 2.4, 1.4,
                                 boxstyle="round,pad=0.3",
                                 facecolor="#FFF2CC", edgecolor="#C9A800", lw=2.5))
    ax.text(6.0, 3.5, "同値", ha="center", va="center",
            fontsize=16, fontweight="bold", color="#7F5F00")

    # 双方向矢印
    ax.annotate("", xy=(4.7, 3.5), xytext=(4.5, 3.5),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=2.5))
    ax.annotate("", xy=(7.5, 3.5), xytext=(7.3, 3.5),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=2.5))

    # 実際の矢印（longer）
    ax.annotate("", xy=(7.3, 3.5), xytext=(4.7, 3.5),
                arrowprops=dict(arrowstyle="<->", color="#C9A800", lw=2.5))

    ax.set_title("Filter.Tendsto と ε-δ の対応", fontsize=13, pad=10)
    save(fig, "fig-18")


# =============================================================================
# main
# =============================================================================
if __name__ == "__main__":
    print("Generating all figures with Japanese text...")
    fig01()
    fig02()
    fig03()
    fig04()
    fig05()
    fig06()
    fig07()
    fig08()
    fig09()
    fig10()
    fig11()
    fig12()
    fig13()
    fig14()
    fig15()
    fig16()
    fig17()
    fig18()
    print("\nAll 18 figures generated successfully!")
