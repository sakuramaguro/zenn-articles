#!/usr/bin/env python3
"""Generate all 16 figures for Zenn vol3 article."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

plt.rcParams['font.family'] = 'Hiragino Sans'
plt.rcParams['axes.unicode_minus'] = False

OUT = os.path.expanduser("~/zenn-articles/images/vol3")
DPI = 300

def save(fig, name):
    fig.savefig(os.path.join(OUT, f"{name}.png"), dpi=DPI, bbox_inches='tight',
                facecolor='white')
    fig.savefig(os.path.join(OUT, f"{name}.svg"), bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print(f"{name} 完了")

# ── fig-01: 第2巻の積み上げ図 ──────────────────────────────────────────────────
def fig01():
    fig, ax = plt.subplots(figsize=(5, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    nodes = [
        ("Filter.Tendsto", 10.5, '#e8f4f8'),
        ("MetricSpace", 8.5,  '#d0e8f0'),
        ("TopologicalSpace", 6.5, '#b8dce8'),
        ("CompleteSpace", 4.5, '#a0d0e0'),
        ("ContractingWith\n(Banach不動点定理)", 2.0, '#2980b9'),
    ]

    for i, (label, y, color) in enumerate(nodes):
        text_color = 'white' if i == len(nodes) - 1 else '#1a1a2e'
        bbox = FancyBboxPatch((1.5, y - 0.8), 7, 1.6,
                               boxstyle="round,pad=0.15",
                               facecolor=color, edgecolor='#5a8fa8', linewidth=1.5)
        ax.add_patch(bbox)
        ax.text(5, y, label, ha='center', va='center',
                fontsize=10 if i < 4 else 9,
                color=text_color, fontweight='bold')

    # arrows
    ys = [n[1] for n in nodes]
    for i in range(len(ys) - 1):
        ax.annotate('', xy=(5, ys[i+1] + 0.8), xytext=(5, ys[i] - 0.8),
                    arrowprops=dict(arrowstyle='->', color='#5a8fa8',
                                   lw=2.0, connectionstyle='arc3,rad=0'))

    ax.set_title("第2巻：Banach不動点定理への道", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-01')

# ── fig-02: 第3巻ピラミッド図 ──────────────────────────────────────────────────
def fig02():
    fig, ax = plt.subplots(figsize=(6, 7))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    levels = [
        ("σ-代数", 0),
        ("測度", 1),
        ("可測関数", 2),
        ("単関数", 3),
        ("lintegral / integral", 4),
        ("収束定理", 5),
        ("L^p / 確率空間", 6),
    ]
    blues = ['#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa',
             '#3b82f6', '#2563eb', '#1d4ed8']

    n = len(levels)
    h = 1.0
    for i, (label, level) in enumerate(levels):
        half = 0.5 + (n - i - 1) * 0.55
        left = 5 - half
        bottom = i * (h + 0.15)
        rect = patches.FancyBboxPatch(
            (left, bottom), half * 2, h,
            boxstyle="round,pad=0.05",
            facecolor=blues[i], edgecolor='#1e3a5f', linewidth=1.2)
        ax.add_patch(rect)
        text_c = 'white' if i >= 4 else '#1a1a2e'
        ax.text(5, bottom + h / 2, label, ha='center', va='center',
                fontsize=9.5, color=text_c, fontweight='bold')

    ax.set_title("第3巻：測度論の構造ピラミッド", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-02')

# ── fig-03: σ-代数フィルタリング図 ────────────────────────────────────────────
def fig03():
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 7)
    ax.axis('off')

    # outer ellipse 2^X
    outer = mpatches.Ellipse((5, 3), 10, 6.5, facecolor='#f0f7ff',
                              edgecolor='#2c6e9e', linewidth=2)
    ax.add_patch(outer)
    ax.text(9.5, 5.8, r'$2^X$', fontsize=13, color='#2c6e9e', fontweight='bold')

    # inner ellipse σ-algebra M
    inner = mpatches.Ellipse((4.5, 2.8), 6, 4, facecolor='#cce4f7',
                              edgecolor='#1565c0', linewidth=2)
    ax.add_patch(inner)
    ax.text(4.5, 4.5, r'$\mathcal{M}$（σ-代数）', fontsize=11,
            ha='center', color='#1565c0', fontweight='bold')

    # elements inside M
    items = [(3.0, 3.4, r'$\emptyset$'), (5.5, 3.4, r'$X$'),
             (3.0, 2.0, r'$A_1$'), (5.5, 2.0, r'$A_2$'),
             (4.5, 1.1, r'$A^c$')]
    for x, y, t in items:
        ax.plot(x, y, 'o', color='#1565c0', ms=5)
        ax.text(x + 0.2, y, t, fontsize=9, color='#1565c0', va='center')

    # non-measurable points outside M
    rng = np.random.default_rng(42)
    for _ in range(12):
        theta = rng.uniform(0, 2 * np.pi)
        r = rng.uniform(3.5, 4.8)
        px, py = 5 + r * np.cos(theta) * 0.95, 3 + r * np.sin(theta) * 0.6
        if ((px - 4.5)**2 / 9 + (py - 2.8)**2 / 4) > 1.0:
            ax.plot(px, py, 'x', color='#e74c3c', ms=6, mew=1.5)

    ax.text(8.0, 1.0, '非可測集合', fontsize=8, color='#e74c3c',
            style='italic')

    ax.set_title("σ-代数によるフィルタリング", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-03')

# ── fig-04: 測度のマッピング図 ────────────────────────────────────────────────
def fig04():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    left_items = [("A1", 4.5), ("A2", 3.0), ("A3", 1.5)]
    right_items = [("μ(A1) = 2", 4.5), ("μ(A2) = 0.5", 3.0), ("μ(A3) = ∞", 1.5)]

    # boxes left
    for label, y in left_items:
        rect = FancyBboxPatch((0.5, y - 0.45), 2.5, 0.9,
                               boxstyle="round,pad=0.1",
                               facecolor='#d6eaf8', edgecolor='#2980b9', lw=1.5)
        ax.add_patch(rect)
        ax.text(1.75, y, label, ha='center', va='center',
                fontsize=11, color='#1a1a2e', fontweight='bold')

    # boxes right
    for label, y in right_items:
        rect = FancyBboxPatch((7.0, y - 0.45), 2.5, 0.9,
                               boxstyle="round,pad=0.1",
                               facecolor='#d5f5e3', edgecolor='#27ae60', lw=1.5)
        ax.add_patch(rect)
        ax.text(8.25, y, label, ha='center', va='center',
                fontsize=10, color='#1a1a2e', fontweight='bold')

    # arrows
    for _, y in left_items:
        ax.annotate('', xy=(7.0, y), xytext=(3.0, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.8))

    # μ label on arrows
    ax.text(5.0, 4.5 + 0.3, r'$\mu: \mathcal{M} \to [0, +\infty]$',
            ha='center', fontsize=11, color='#555', style='italic')

    # braces / labels
    ax.text(1.75, 5.4, r'$\sigma$-代数 $\mathcal{M}$', ha='center',
            fontsize=10, color='#2980b9', fontweight='bold')
    ax.text(8.25, 5.4, r'$[0, +\infty]$', ha='center',
            fontsize=10, color='#27ae60', fontweight='bold')

    ax.set_title("測度 μ：σ-代数から拡大非負実数への写像", fontsize=11,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-04')

# ── fig-05: 3種類の測度比較図 ──────────────────────────────────────────────────
def fig05():
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')

    cols = ["Lebesgue測度", "数え上げ測度", "Dirac測度 δx"]
    rows = ["定義", "具体例", "特徴"]
    data = [
        ["区間の長さ\n（通常の長さ概念）",
         "有限集合の要素数\n（無限集合は∞）",
         "点 x のみ質量1\n（他は0）"],
        ["λ([a,b]) = b-a",
         "ν({1,2,3}) = 3\nν(N) = ∞",
         "δx({x}) = 1\nδx(A) = 0 (x∉A)"],
        ["連続・平行移動不変",
         "離散・加算加法的",
         "点質量・確率測度"],
    ]
    col_colors = ['#d6eaf8', '#d5f5e3', '#fde8d8']
    header_colors = ['#2980b9', '#27ae60', '#e67e22']

    xs = [1.5, 4.5, 7.5]
    col_w = 2.6
    row_ys = [3.8, 2.3, 0.8]
    row_h = 1.2

    # column headers
    for j, (col, hc) in enumerate(zip(cols, header_colors)):
        rect = FancyBboxPatch((xs[j] - col_w / 2, 4.6), col_w, 0.7,
                               boxstyle="round,pad=0.05",
                               facecolor=hc, edgecolor='none')
        ax.add_patch(rect)
        ax.text(xs[j], 4.95, col, ha='center', va='center',
                fontsize=9, color='white', fontweight='bold')

    # row labels
    for i, row in enumerate(rows):
        ax.text(0.1, row_ys[i] + row_h / 2, row, ha='left', va='center',
                fontsize=9, color='#555', fontweight='bold')

    # cells
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 6)
    for j, cc in enumerate(col_colors):
        for i, row_y in enumerate(row_ys):
            rect = FancyBboxPatch((xs[j] - col_w / 2, row_y), col_w, row_h - 0.1,
                                   boxstyle="round,pad=0.05",
                                   facecolor=cc, edgecolor='#ccc', lw=0.8)
            ax.add_patch(rect)
            ax.text(xs[j], row_y + (row_h - 0.1) / 2, data[i][j],
                    ha='center', va='center', fontsize=8, color='#1a1a2e')

    ax.set_title("3種類の測度の比較", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-05')

# ── fig-06: 可測関数の逆像図 ──────────────────────────────────────────────────
def fig06():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # left ellipse
    left_e = mpatches.Ellipse((2.5, 3), 4, 4.5, facecolor='#eaf4fb',
                               edgecolor='#2980b9', lw=2)
    ax.add_patch(left_e)
    ax.text(2.5, 5.2, r'$(X, \mathcal{M})$', ha='center', fontsize=11,
            color='#2980b9', fontweight='bold')

    # right ellipse
    right_e = mpatches.Ellipse((7.5, 3), 4, 4.5, facecolor='#eafaf1',
                                edgecolor='#27ae60', lw=2)
    ax.add_patch(right_e)
    ax.text(7.5, 5.2, r'$(\mathbb{R}, \mathcal{B}(\mathbb{R}))$',
            ha='center', fontsize=11, color='#27ae60', fontweight='bold')

    # Borel set B in right
    bset = mpatches.Ellipse((7.5, 2.8), 2.2, 2.4, facecolor='#a9dfbf',
                             edgecolor='#1e8449', lw=1.5, alpha=0.8)
    ax.add_patch(bset)
    ax.text(7.5, 2.8, r'$B \in \mathcal{B}(\mathbb{R})$',
            ha='center', va='center', fontsize=9, color='#145a32')

    # preimage f^{-1}(B) in left
    pre = mpatches.Ellipse((2.5, 2.8), 2.2, 2.4, facecolor='#a9dfbf',
                            edgecolor='#1e8449', lw=1.5, alpha=0.8)
    ax.add_patch(pre)
    ax.text(2.5, 2.8, r'$f^{-1}(B) \in \mathcal{M}$',
            ha='center', va='center', fontsize=9, color='#145a32')

    # forward arrow f
    ax.annotate('', xy=(5.3, 3.5), xytext=(4.7, 3.5),
                arrowprops=dict(arrowstyle='->', color='#444', lw=2.0))
    ax.text(5.0, 3.85, r'$f$', ha='center', fontsize=12,
            color='#444', fontweight='bold')

    # backward arrow f^{-1}
    ax.annotate('', xy=(4.7, 2.5), xytext=(5.3, 2.5),
                arrowprops=dict(arrowstyle='->', color='#888', lw=1.5,
                                linestyle='dashed'))
    ax.text(5.0, 2.1, r'$f^{-1}$', ha='center', fontsize=10,
            color='#888', style='italic')

    ax.set_title("可測関数：逆像がσ-代数に属する写像", fontsize=11,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-06')

# ── fig-07: 単関数列の矩形近似図 ──────────────────────────────────────────────
def fig07():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    x = np.linspace(0, 1, 500)
    f = np.sqrt(x)

    configs = [(1, '#cde8f7', 0.4), (2, '#7bbfe0', 0.6), (4, '#2980b9', 0.9)]
    for n, color, alpha in configs:
        xs_step = np.linspace(0, 1, n + 1)
        for i in range(n):
            mid = (xs_step[i] + xs_step[i+1]) / 2
            val = np.sqrt(xs_step[i])
            rect = patches.Rectangle((xs_step[i], 0), xs_step[i+1] - xs_step[i],
                                       val, facecolor=color, edgecolor='#1a6fa8',
                                       lw=0.8, alpha=alpha,
                                       label=f'n={n}' if i == 0 else '_')
            ax.add_patch(rect)

    ax.plot(x, f, color='#c0392b', lw=2.5, label=r'$f(x) = \sqrt{x}$', zorder=5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.25)
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.legend(fontsize=9, loc='upper left')
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_title(r"単関数列による $f(x)=\sqrt{x}$ の近似（n=1,2,4）",
                 fontsize=11, fontweight='bold', color='#1a1a2e')
    save(fig, 'fig-07')

# ── fig-08: SimpleFunc.lintegral 計算構造図 ────────────────────────────────────
def fig08():
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')

    cs = ['c1', 'c2', 'c3']
    ys = [5.5, 3.5, 1.5]

    # c_i boxes
    for ci, y in zip(cs, ys):
        r = FancyBboxPatch((0.3, y - 0.4), 1.5, 0.8, boxstyle="round,pad=0.1",
                            facecolor='#d6eaf8', edgecolor='#2980b9', lw=1.5)
        ax.add_patch(r)
        ax.text(1.05, y, ci, ha='center', va='center', fontsize=11,
                color='#1a1a2e', fontweight='bold')

    # μ(φ^{-1}{c_i}) boxes
    for i, (ci, y) in enumerate(zip(cs, ys)):
        r = FancyBboxPatch((3.5, y - 0.4), 2.8, 0.8, boxstyle="round,pad=0.1",
                            facecolor='#d5f5e3', edgecolor='#27ae60', lw=1.5)
        ax.add_patch(r)
        ax.text(4.9, y, f'μ(φ^(-1){{{ci[-1]}}})', ha='center', va='center',
                fontsize=9.5, color='#1a1a2e', fontweight='bold')
        ax.annotate('', xy=(3.5, y), xytext=(1.8, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5))

    # c_i * μ(...) product boxes
    for ci, y in zip(cs, ys):
        r = FancyBboxPatch((7.5, y - 0.4), 2.8, 0.8, boxstyle="round,pad=0.1",
                            facecolor='#fde8d8', edgecolor='#e67e22', lw=1.5)
        ax.add_patch(r)
        ax.text(8.9, y, f'{ci} * μ(φ^(-1){{·}})', ha='center', va='center',
                fontsize=9, color='#1a1a2e', fontweight='bold')
        ax.annotate('', xy=(7.5, y), xytext=(6.3, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5))
        ax.text(6.9, y + 0.25, '×', ha='center', fontsize=11, color='#555')

    # sigma sum box
    r = FancyBboxPatch((10.5, 3.0), 1.3, 1.5, boxstyle="round,pad=0.1",
                        facecolor='#2c3e50', edgecolor='#1a1a2e', lw=1.5)
    ax.add_patch(r)
    ax.text(11.15, 3.75, 'Σ\n∫φ∂μ', ha='center', va='center',
            fontsize=10, color='white', fontweight='bold')

    for y in ys:
        ax.annotate('', xy=(10.5, 3.75), xytext=(10.3, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.2))

    ax.text(1.05, 6.5, '値域 (Finset)', ha='center', fontsize=9, color='#2980b9')
    ax.text(4.9, 6.5, '測度値', ha='center', fontsize=9, color='#27ae60')
    ax.text(8.9, 6.5, '積', ha='center', fontsize=9, color='#e67e22')

    ax.set_title("SimpleFunc.lintegral の計算構造", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-08')

# ── fig-09: lintegral と integral の型対比図 ────────────────────────────────────
def fig09():
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # dividing line
    ax.axvline(x=5, color='#ccc', lw=1.5, ymin=0.05, ymax=0.9)

    # headers
    for x, label, color in [(2.5, 'lintegral', '#2980b9'), (7.5, 'integral', '#e67e22')]:
        r = FancyBboxPatch((x - 2, 5.5), 4, 0.9, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='none')
        ax.add_patch(r)
        ax.text(x, 5.95, label, ha='center', va='center',
                fontsize=12, color='white', fontweight='bold')

    items = [
        (r'表記', r'$\int^- f \, \partial\mu$', r'$\int f \, \partial\mu$'),
        (r'型', r'$\mathbb{R}_{\geq 0}^\infty$（ENNReal）', r'$\mathbb{R}$（実数）'),
        (r'値域', r'$[0, +\infty]$', r'$(-\infty, +\infty)$'),
        (r'対象', r'非負可測関数', r'可積分関数'),
    ]
    ys = [4.5, 3.4, 2.3, 1.2]
    for (row_label, left_val, right_val), y in zip(items, ys):
        ax.text(0.3, y, row_label, ha='left', va='center', fontsize=9,
                color='#555', fontweight='bold')
        r1 = FancyBboxPatch((1.0, y - 0.38), 3.5, 0.76, boxstyle="round,pad=0.05",
                             facecolor='#d6eaf8', edgecolor='#2980b9', lw=0.8)
        ax.add_patch(r1)
        ax.text(2.75, y, left_val, ha='center', va='center', fontsize=9,
                color='#1a1a2e')
        r2 = FancyBboxPatch((5.5, y - 0.38), 3.5, 0.76, boxstyle="round,pad=0.05",
                             facecolor='#fde8d8', edgecolor='#e67e22', lw=0.8)
        ax.add_patch(r2)
        ax.text(7.25, y, right_val, ha='center', va='center', fontsize=9,
                color='#1a1a2e')

    ax.set_title("lintegral と integral の型対比", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-09')

# ── fig-10: lintegral → integral 変換フロー ──────────────────────────────────
def fig10():
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    boxes = [
        (1.5, 3.5, "非負可測関数\nf : X → R≥0", '#d6eaf8', '#2980b9'),
        (5.0, 3.5, "lintegral\n∫ f ∂μ ∈ R≥0∞", '#d5f5e3', '#27ae60'),
        (8.5, 3.5, "integral\n∫ f ∂μ ∈ R", '#fde8d8', '#e67e22'),
    ]
    for x, y, label, fc, ec in boxes:
        r = FancyBboxPatch((x - 1.4, y - 0.7), 2.8, 1.4,
                            boxstyle="round,pad=0.1",
                            facecolor=fc, edgecolor=ec, lw=1.8)
        ax.add_patch(r)
        ax.text(x, y, label, ha='center', va='center',
                fontsize=9, color='#1a1a2e', fontweight='bold')

    # arrows
    lemma = "integral_eq_lintegral_of_nonneg"
    ax.annotate('', xy=(3.6, 3.5), xytext=(2.9, 3.5),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))
    ax.annotate('', xy=(7.1, 3.5), xytext=(6.4, 3.5),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))
    ax.text(5.0, 4.55, lemma, ha='center', fontsize=7.5,
            color='#555', style='italic')
    ax.annotate('', xy=(7.1, 4.25), xytext=(2.9, 4.25),
                arrowprops=dict(arrowstyle='->', color='#aaa', lw=1.2,
                                connectionstyle='arc3,rad=-0.25'))

    # bottom note
    ax.add_patch(FancyBboxPatch((1.5, 0.5), 7.0, 1.0,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#f8f9fa', edgecolor='#bbb', lw=1.2))
    ax.text(5.0, 1.0,
            r"補足：一般の f に対しては $f = f^+ - f^-$ に分解して定義",
            ha='center', va='center', fontsize=9, color='#555')

    ax.set_title("lintegral から integral への変換フロー", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-10')

# ── fig-11: 単調収束定理 ──────────────────────────────────────────────────────
def fig11():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    x = np.linspace(0, 1, 300)
    colors = ['#cde8f7', '#93c5fd', '#3b82f6', '#1d4ed8']
    ns = [1, 2, 3, 5]

    for n, c in zip(ns, colors):
        fn = x * n / (n + 1)
        ax.plot(x, fn, color=c, lw=2, label=f'$f_{{{n}}}(x) = x\\cdot{n}/{n+1}$',
                alpha=0.85)

    ax.plot(x, x, color='#c0392b', lw=2.5, label=r'$f(x) = x$（極限）')

    ax.annotate('', xy=(0.7, 0.7), xytext=(0.7, 0.7 * 5 / 6),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
    ax.text(0.72, 0.67, r'$\int f_n \nearrow \int f$', fontsize=9, color='#555')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.legend(fontsize=8, loc='upper left')
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_title("単調収束定理：$f_n \\nearrow f$ ならば $\\int f_n \\to \\int f$",
                 fontsize=11, fontweight='bold', color='#1a1a2e')
    save(fig, 'fig-11')

# ── fig-12: Fatouの補題反例図 ────────────────────────────────────────────────
def fig12():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    colors = ['#2980b9', '#27ae60', '#e67e22', '#8e44ad']
    for n, c in enumerate(colors):
        rect = patches.Rectangle((n, 0), 1, 1, facecolor=c, edgecolor='white',
                                   lw=1.5, alpha=0.8,
                                   label=f'$f_{{{n}}} = \\mathbf{{1}}_{{[{n},{n+1}]}}$')
        ax.add_patch(rect)
        ax.text(n + 0.5, 0.5, f'$f_{{{n}}}$', ha='center', va='center',
                fontsize=11, color='white', fontweight='bold')

    ax.set_xlim(-0.2, 5)
    ax.set_ylim(-0.5, 1.8)
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.legend(fontsize=8, loc='upper right')
    ax.spines[['top', 'right']].set_visible(False)

    ax.text(0.0, -0.35,
            r"$\liminf f_n = 0$  だが  $\int \liminf f_n = 0 \leq \liminf \int f_n = 1$",
            fontsize=9, color='#555')
    ax.set_title("Fatouの補題：$\\int \\liminf f_n \\leq \\liminf \\int f_n$",
                 fontsize=11, fontweight='bold', color='#1a1a2e')
    save(fig, 'fig-12')

# ── fig-13: 優収束定理の3パネル図 ──────────────────────────────────────────────
def fig13():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
    fig.patch.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')
        ax.spines[['top', 'right']].set_visible(False)

    x = np.linspace(0, np.pi, 300)

    # Left: pointwise convergence
    ax0 = axes[0]
    ns = [1, 2, 5, 20]
    cs = ['#cde8f7', '#7bbfe0', '#3b82f6', '#1d4ed8']
    for n, c in zip(ns, cs):
        fn = np.sin(x) * np.exp(-x / n)
        ax0.plot(x, fn, color=c, lw=1.8, alpha=0.85, label=f'n={n}')
    ax0.plot(x, np.zeros_like(x), color='#c0392b', lw=2.5, label='f=0（極限）')
    ax0.set_title("点ごとの収束\n$f_n(x) \\to f(x)$", fontsize=9,
                  fontweight='bold', color='#1a1a2e')
    ax0.set_xlabel('x')
    ax0.set_ylabel('y')
    ax0.legend(fontsize=7)

    # Middle: dominating function
    ax1 = axes[1]
    g = np.sin(x)
    g = np.clip(g, 0, None)
    ax1.fill_between(x, -g, g, alpha=0.2, color='#e67e22', label=r'$|f_n| \leq g$')
    ax1.plot(x, g, color='#e67e22', lw=2.5, label=r'$g(x)$（優関数）')
    for n, c in zip([1, 5], ['#2980b9', '#27ae60']):
        fn = np.sin(x) * np.exp(-x / n)
        ax1.plot(x, fn, color=c, lw=1.5, alpha=0.7, label=f'$f_{{{n}}}$')
    ax1.set_title("優関数 g\n$|f_n(x)| \\leq g(x)$, $\\int g < \\infty$",
                  fontsize=9, fontweight='bold', color='#1a1a2e')
    ax1.set_xlabel('x')
    ax1.legend(fontsize=7)

    # Right: integral convergence
    ax2 = axes[2]
    ns_int = np.arange(1, 21)
    integrals = [np.trapezoid(np.sin(x) * np.exp(-x / n), x) for n in ns_int]
    ax2.plot(ns_int, integrals, 'o-', color='#2980b9', lw=2, ms=5,
             label=r'$\int f_n \, d\mu$')
    ax2.axhline(y=0, color='#c0392b', lw=2, ls='--',
                label=r'$\int f \, d\mu = 0$')
    ax2.set_title("積分の収束\n$\\int f_n \\to \\int f$",
                  fontsize=9, fontweight='bold', color='#1a1a2e')
    ax2.set_xlabel('n')
    ax2.set_ylabel(r'$\int f_n$')
    ax2.legend(fontsize=7)

    fig.suptitle("優収束定理（Dominated Convergence Theorem）",
                 fontsize=12, fontweight='bold', color='#1a1a2e', y=1.02)
    fig.tight_layout()
    save(fig, 'fig-13')

# ── fig-14: L^p 空間の包含関係入れ子図 ────────────────────────────────────────
def fig14():
    fig, ax = plt.subplots(figsize=(6, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ellipses = [
        (5, 3.5, 9, 5.5, '#dbeafe', '#2563eb', r'$L^1$',
         r'$\|f\|_1 = \int |f| \, d\mu$', 7.0),
        (5, 3.5, 6.5, 4.0, '#93c5fd', '#1d4ed8', r'$L^2$',
         r'$\|f\|_2 = \left(\int |f|^2\right)^{1/2}$', 5.0),
        (5, 3.5, 3.5, 2.5, '#1d4ed8', '#1e3a8a', r'$L^\infty$',
         r'$\|f\|_\infty = \text{ess\,sup}|f|$', 3.2),
    ]

    for cx, cy, ew, eh, fc, ec, label, norm, ty in reversed(ellipses):
        e = mpatches.Ellipse((cx, cy), ew, eh, facecolor=fc, edgecolor=ec,
                              lw=2, alpha=0.7)
        ax.add_patch(e)
        tc = 'white' if label == r'$L^\infty$' else '#1a1a2e'
        ax.text(cx, ty, label, ha='center', va='center',
                fontsize=12, color=tc, fontweight='bold')
        ax.text(cx, ty - 0.55, norm, ha='center', va='center',
                fontsize=7.5, color=tc, style='italic')

    ax.text(5, 0.5,
            r"有限測度の場合：$L^\infty \subset L^2 \subset L^1$",
            ha='center', fontsize=10, color='#1a1a2e', fontweight='bold')

    ax.set_title(r"$L^p$ 空間の包含関係（有限測度）", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-14')

# ── fig-15: 確率空間と Lean 型クラス対応図 ────────────────────────────────────
def fig15():
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Math side
    ax.add_patch(FancyBboxPatch((0.3, 1.0), 3.8, 5.0,
                                 boxstyle="round,pad=0.2",
                                 facecolor='#eaf4fb', edgecolor='#2980b9', lw=2))
    ax.text(2.2, 5.6, "数学の記法", ha='center', fontsize=11,
            color='#2980b9', fontweight='bold')
    math_items = [
        (r'$(\Omega,\, \mathcal{F},\, P)$', 4.7),
        (r'$\Omega$：標本空間', 3.7),
        (r'$\mathcal{F}$：σ-代数（事象の族）', 2.7),
        (r'$P$：確率測度 $(P(\Omega)=1)$', 1.7),
    ]
    for text, y in math_items:
        ax.text(2.2, y, text, ha='center', va='center', fontsize=9,
                color='#1a1a2e')

    # Lean side
    ax.add_patch(FancyBboxPatch((5.9, 1.0), 3.8, 5.0,
                                 boxstyle="round,pad=0.2",
                                 facecolor='#eafaf1', edgecolor='#27ae60', lw=2))
    ax.text(7.8, 5.6, "Lean の型クラス", ha='center', fontsize=11,
            color='#27ae60', fontweight='bold')
    lean_items = [
        (r'$\Omega$ : Type*', 4.7),
        (r'$\Omega$：型', 3.7),
        (r'MeasurableSpace $\Omega$', 2.7),
        (r'IsProbabilityMeasure $P$', 1.7),
    ]
    for text, y in lean_items:
        ax.text(7.8, y, text, ha='center', va='center', fontsize=9,
                color='#1a1a2e')

    # arrows
    for y in [4.7, 3.7, 2.7, 1.7]:
        ax.annotate('', xy=(5.9, y), xytext=(4.1, y),
                    arrowprops=dict(arrowstyle='<->', color='#7f8c8d', lw=1.8))

    ax.set_title("確率空間と Lean 型クラスの対応", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-15')

# ── fig-16: 確率変数の可測関数構造図 ────────────────────────────────────────────
def fig16():
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # left ellipse: probability space
    left_e = mpatches.Ellipse((2.5, 4.0), 4.2, 4.5,
                               facecolor='#eaf4fb', edgecolor='#2980b9', lw=2)
    ax.add_patch(left_e)
    ax.text(2.5, 5.9, r'確率空間 $(\Omega, \mathcal{F}, P)$',
            ha='center', fontsize=10, color='#2980b9', fontweight='bold')

    # right ellipse: real number space
    right_e = mpatches.Ellipse((7.5, 4.0), 4.2, 4.5,
                                facecolor='#eafaf1', edgecolor='#27ae60', lw=2)
    ax.add_patch(right_e)
    ax.text(7.5, 5.9, r'実数空間 $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$',
            ha='center', fontsize=10, color='#27ae60', fontweight='bold')

    # Borel set B in right
    bset = mpatches.Ellipse((7.5, 3.6), 2.2, 2.2,
                             facecolor='#a9dfbf', edgecolor='#1e8449', lw=1.5,
                             alpha=0.85)
    ax.add_patch(bset)
    ax.text(7.5, 3.6, r'$B \in \mathcal{B}(\mathbb{R})$',
            ha='center', va='center', fontsize=9, color='#145a32')

    # preimage X^{-1}(B)
    pre = mpatches.Ellipse((2.5, 3.6), 2.2, 2.2,
                            facecolor='#a9dfbf', edgecolor='#1e8449', lw=1.5,
                            alpha=0.85)
    ax.add_patch(pre)
    ax.text(2.5, 3.6, r'$X^{-1}(B) \in \mathcal{F}$',
            ha='center', va='center', fontsize=9, color='#145a32')

    # X arrow
    ax.annotate('', xy=(5.6, 4.6), xytext=(4.4, 4.6),
                arrowprops=dict(arrowstyle='->', color='#444', lw=2.2))
    ax.text(5.0, 5.0, r'$X: \Omega \to \mathbb{R}$',
            ha='center', fontsize=10, color='#444', fontweight='bold')

    # X^{-1} arrow
    ax.annotate('', xy=(4.4, 3.0), xytext=(5.6, 3.0),
                arrowprops=dict(arrowstyle='->', color='#888', lw=1.5,
                                linestyle='dashed'))
    ax.text(5.0, 2.6, r'$X^{-1}$', ha='center', fontsize=9,
            color='#888', style='italic')

    # conclusion
    ax.add_patch(FancyBboxPatch((0.5, 0.2), 9.0, 0.9,
                                 boxstyle="round,pad=0.1",
                                 facecolor='#2c3e50', edgecolor='none'))
    ax.text(5.0, 0.65,
            r"$X$ が確率変数  $\Longleftrightarrow$  $X$ が可測関数",
            ha='center', va='center', fontsize=10,
            color='white', fontweight='bold')

    ax.set_title("確率変数 = 可測関数としての構造", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-16')

# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig01(); fig02(); fig03(); fig04()
    fig05(); fig06(); fig07(); fig08()
    fig09(); fig10(); fig11(); fig12()
    fig13(); fig14(); fig15(); fig16()
    print("\n全16枚の生成完了！")
