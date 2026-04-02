#!/usr/bin/env python3
"""Fix 7 figures: fig-02, 04, 05, 07, 08, 10, 13."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
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

# ── fig-02: ピラミッド図（高さ1.3倍・下にシフト・最上段テキスト修正） ──────────
def fig02():
    fig, ax = plt.subplots(figsize=(6, 9.1))   # 7 * 1.3 = 9.1
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
        (r"$L^p$ / 確率空間", 6),          # ← mathtext に変更
    ]
    blues = ['#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa',
             '#3b82f6', '#2563eb', '#1d4ed8']

    n = len(levels)
    h = 1.0
    y_offset = -0.5   # 全体を下に 10% シフト（ylim=10 なので 0.5≈5%）

    for i, (label, level) in enumerate(levels):
        half = 0.5 + (n - i - 1) * 0.55
        left = 5 - half
        bottom = y_offset + 0.7 + i * (h + 0.15)   # 下端に余白 0.7
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

# ── fig-04: 測度のマッピング図（添字修正・μラベル修正） ────────────────────────
def fig04():
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    left_items  = [(r'$A_1$', 4.5), (r'$A_2$', 3.0), (r'$A_3$', 1.5)]
    right_items = [(r'$\mu(A_1) = 2$',       4.5),
                   (r'$\mu(A_2) = 0.5$',      3.0),
                   (r'$\mu(A_3) = +\infty$',  1.5)]

    # boxes left
    for label, y in left_items:
        rect = FancyBboxPatch((0.5, y - 0.45), 2.5, 0.9,
                               boxstyle="round,pad=0.1",
                               facecolor='#d6eaf8', edgecolor='#2980b9', lw=1.5)
        ax.add_patch(rect)
        ax.text(1.75, y, label, ha='center', va='center',
                fontsize=12, color='#1a1a2e', fontweight='bold')

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

    # μ label on arrows — mathtext
    ax.text(5.0, 5.1, r'$\mu : \mathcal{M} \to [0, +\infty]$',
            ha='center', fontsize=11, color='#555', style='italic')

    # column headers
    ax.text(1.75, 5.4, r'$\sigma$-代数 $\mathcal{M}$', ha='center',
            fontsize=10, color='#2980b9', fontweight='bold')
    ax.text(8.25, 5.4, r'$[0, +\infty]$', ha='center',
            fontsize=10, color='#27ae60', fontweight='bold')

    ax.set_title(r"測度 $\mu$：$\sigma$-代数から拡大非負実数への写像",
                 fontsize=11, fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-04')

# ── fig-05: 3種類の測度比較図（Dirac列タイトル・具体例セル修正） ───────────────
def fig05():
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')

    # ヘッダーテキストは ax.text で個別描画するため空文字にしてから上書き
    cols_plain = ["Lebesgue測度", "数え上げ測度", r"Dirac測度 $\delta_x$"]
    rows = ["定義", "具体例", "特徴"]
    data = [
        ["区間の長さ\n（通常の長さ概念）",
         "有限集合の要素数\n（無限集合は∞）",
         "点 x のみ質量1\n（他は0）"],
        [r"$\lambda([a,b]) = b - a$",
         r"$\nu(\{1,2,3\}) = 3$" + "\n" + r"$\nu(\mathbb{N}) = \infty$",
         r"$\delta_x(\{x\}) = 1$" + "\n" + r"$\delta_x(A) = 0 \; (x \notin A)$"],
        ["連続・平行移動不変",
         "離散・加算加法的",
         "点質量・確率測度"],
    ]
    col_colors  = ['#d6eaf8', '#d5f5e3', '#fde8d8']
    header_colors = ['#2980b9', '#27ae60', '#e67e22']

    xs    = [1.5, 4.5, 7.5]
    col_w = 2.6
    row_ys = [3.8, 2.3, 0.8]
    row_h  = 1.2

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 6)

    # column headers
    for j, (col, hc) in enumerate(zip(cols_plain, header_colors)):
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

# ── fig-07: 単関数列の矩形近似図（3列サブプロット比較） ────────────────────────
def fig07():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    fig.patch.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')
        ax.spines[['top', 'right']].set_visible(False)

    x_fine = np.linspace(0, 1, 500)
    f_curve = np.sqrt(x_fine)
    fill_color = '#93c5fd'

    for idx, n in enumerate([1, 2, 4]):
        ax = axes[idx]
        xs_step = np.linspace(0, 1, n + 1)
        for i in range(n):
            val = np.sqrt(xs_step[i])          # 左端値
            w   = xs_step[i + 1] - xs_step[i]
            rect = patches.Rectangle(
                (xs_step[i], 0), w, val,
                facecolor=fill_color, edgecolor='black',
                linewidth=1.5, alpha=0.85,
                label='単関数' if i == 0 else '_')
            ax.add_patch(rect)
        # 曲線を赤で重ねる
        ax.plot(x_fine, f_curve, color='#c0392b', lw=2.2,
                label=r'$f(x)=\sqrt{x}$', zorder=5)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.25)
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)
        ax.set_title(f'n = {n}', fontsize=11, fontweight='bold', color='#1a1a2e')
        ax.legend(fontsize=8, loc='upper left')

    fig.suptitle(r"単関数列による $f(x)=\sqrt{x}$ の近似",
                 fontsize=12, fontweight='bold', color='#1a1a2e')
    fig.tight_layout()
    save(fig, 'fig-07')

# ── fig-08: SimpleFunc.lintegral 計算構造図（mathtext ラベル修正） ──────────────
def fig08():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7)
    ax.axis('off')

    cs_labels = [r'$c_1$', r'$c_2$', r'$c_3$']
    mu_labels = [
        r'$\mu(\phi^{-1}\{c_1\})$',
        r'$\mu(\phi^{-1}\{c_2\})$',
        r'$\mu(\phi^{-1}\{c_3\})$',
    ]
    prod_labels = [
        r'$c_1 \cdot \mu(\phi^{-1}\{c_1\})$',
        r'$c_2 \cdot \mu(\phi^{-1}\{c_2\})$',
        r'$c_3 \cdot \mu(\phi^{-1}\{c_3\})$',
    ]
    ys = [5.5, 3.5, 1.5]

    # c_i boxes
    for label, y in zip(cs_labels, ys):
        r = FancyBboxPatch((0.3, y - 0.45), 1.6, 0.9, boxstyle="round,pad=0.1",
                            facecolor='#d6eaf8', edgecolor='#2980b9', lw=1.5)
        ax.add_patch(r)
        ax.text(1.1, y, label, ha='center', va='center',
                fontsize=12, color='#1a1a2e', fontweight='bold')

    # μ(φ⁻¹{cᵢ}) boxes
    for label, y in zip(mu_labels, ys):
        r = FancyBboxPatch((3.2, y - 0.45), 3.4, 0.9, boxstyle="round,pad=0.1",
                            facecolor='#d5f5e3', edgecolor='#27ae60', lw=1.5)
        ax.add_patch(r)
        ax.text(4.9, y, label, ha='center', va='center',
                fontsize=10, color='#1a1a2e', fontweight='bold')
        ax.annotate('', xy=(3.2, y), xytext=(1.9, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5))

    # product boxes
    for label, y in zip(prod_labels, ys):
        r = FancyBboxPatch((7.6, y - 0.45), 3.8, 0.9, boxstyle="round,pad=0.1",
                            facecolor='#fde8d8', edgecolor='#e67e22', lw=1.5)
        ax.add_patch(r)
        ax.text(9.5, y, label, ha='center', va='center',
                fontsize=10, color='#1a1a2e', fontweight='bold')
        ax.annotate('', xy=(7.6, y), xytext=(6.6, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5))
        ax.text(7.1, y + 0.28, r'$\times$', ha='center', fontsize=12, color='#555')

    # Σ box
    r = FancyBboxPatch((11.6, 2.85), 1.1, 1.8, boxstyle="round,pad=0.1",
                        facecolor='#2c3e50', edgecolor='#1a1a2e', lw=1.5)
    ax.add_patch(r)
    ax.text(12.15, 3.75, r'$\Sigma$' + '\n' + r'$\int^-\!\phi\,\partial\mu$',
            ha='center', va='center', fontsize=10, color='white', fontweight='bold')

    for y in ys:
        ax.annotate('', xy=(11.6, 3.75), xytext=(11.4, y),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.2))

    # column headers
    ax.text(1.1,  6.5, '値域 (Finset)', ha='center', fontsize=9, color='#2980b9')
    ax.text(4.9,  6.5, '測度値', ha='center', fontsize=9, color='#27ae60')
    ax.text(9.5,  6.5, '積', ha='center', fontsize=9, color='#e67e22')

    ax.set_title("SimpleFunc.lintegral の計算構造", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-08')

# ── fig-10: lintegral → integral 変換フロー（mathtext ラベル修正） ──────────────
def fig10():
    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # 各ボックスのテキストを2行で描画（上段：日本語、下段：数式）
    boxes = [
        (1.5, 3.5,
         "非負可測関数",
         r"$f : X \to \mathbb{R}_{\geq 0}$",
         '#d6eaf8', '#2980b9'),
        (5.0, 3.5,
         "lintegral",
         r"$\int^- f \, d\mu \in [0, +\infty]$",
         '#d5f5e3', '#27ae60'),
        (8.5, 3.5,
         "integral",
         r"$\int f \, d\mu \in \mathbb{R}$",
         '#fde8d8', '#e67e22'),
    ]
    for x, y, line1, line2, fc, ec in boxes:
        r = FancyBboxPatch((x - 1.45, y - 0.75), 2.9, 1.5,
                            boxstyle="round,pad=0.1",
                            facecolor=fc, edgecolor=ec, lw=1.8)
        ax.add_patch(r)
        ax.text(x, y + 0.22, line1, ha='center', va='center',
                fontsize=9, color='#1a1a2e', fontweight='bold')
        ax.text(x, y - 0.28, line2, ha='center', va='center',
                fontsize=8.5, color='#1a1a2e')

    # arrows
    lemma = "integral_eq_lintegral_of_nonneg"
    ax.annotate('', xy=(3.55, 3.5), xytext=(2.95, 3.5),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))
    ax.annotate('', xy=(7.05, 3.5), xytext=(6.45, 3.5),
                arrowprops=dict(arrowstyle='->', color='#555', lw=2.0))
    ax.text(5.0, 4.65, lemma, ha='center', fontsize=7.5,
            color='#555', style='italic')
    ax.annotate('', xy=(7.05, 4.35), xytext=(2.95, 4.35),
                arrowprops=dict(arrowstyle='->', color='#aaa', lw=1.2,
                                connectionstyle='arc3,rad=-0.25'))

    # bottom note
    ax.add_patch(FancyBboxPatch((1.0, 0.4), 8.0, 1.1,
                                 boxstyle="round,pad=0.15",
                                 facecolor='#f8f9fa', edgecolor='#bbb', lw=1.2))
    ax.text(5.0, 0.95,
            r"補足：一般の $f$ に対しては $f = f^+ - f^-$ に分解して定義",
            ha='center', va='center', fontsize=9, color='#555')

    ax.set_title("lintegral から integral への変換フロー", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-10')

# ── fig-13: 優収束定理の3パネル図（fₙ = sin(nπx)/n に修正） ────────────────────
def fig13():
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))
    fig.patch.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')
        ax.spines[['top', 'right']].set_visible(False)

    x = np.linspace(0, 1, 600)

    # ── Left: pointwise convergence  fₙ(x) = sin(nπx)/n → 0 ──
    ax0 = axes[0]
    ns = [1, 2, 5, 20]
    cs = ['#cde8f7', '#7bbfe0', '#3b82f6', '#1d4ed8']
    for n, c in zip(ns, cs):
        fn = np.sin(n * np.pi * x) / n
        ax0.plot(x, fn, color=c, lw=1.8, alpha=0.9,
                 label=f'$n={n}$')
    ax0.axhline(y=0, color='#c0392b', lw=2.5, ls='--', label=r'$f \equiv 0$（極限）')
    ax0.set_title(r"点ごとの収束" + "\n" + r"$f_n(x)=\sin(n\pi x)/n \to 0$",
                  fontsize=9, fontweight='bold', color='#1a1a2e')
    ax0.set_xlabel('x')
    ax0.set_ylabel('y')
    ax0.legend(fontsize=7)

    # ── Middle: dominating function  g(x) = 1 ──
    ax1 = axes[1]
    ax1.axhline(y=1, color='#e67e22', lw=2.5, label=r'$g(x)=1$（優関数）')
    ax1.axhline(y=-1, color='#e67e22', lw=2.5, ls='--')
    ax1.fill_between(x, -1, 1, color='#e67e22', alpha=0.1, label=r'$|f_n|\leq g$')
    for n, c in zip([1, 2, 5], ['#2980b9', '#27ae60', '#9b59b6']):
        fn = np.sin(n * np.pi * x) / n
        ax1.plot(x, fn, color=c, lw=1.5, alpha=0.8, label=f'$f_{{{n}}}$')
    ax1.set_ylim(-1.4, 1.4)
    ax1.set_title(r"優関数 $g$" + "\n" + r"$|f_n(x)|\leq g(x)=1,\;\int g<\infty$",
                  fontsize=9, fontweight='bold', color='#1a1a2e')
    ax1.set_xlabel('x')
    ax1.legend(fontsize=7)

    # ── Right: integral convergence  ∫fₙ = (1-cos(nπ))/(n²π²) → 0 ──
    ax2 = axes[2]
    ns_int = np.arange(1, 21)
    # 解析解: ∫₀¹ sin(nπx)/n dx = [−cos(nπx)/(n²π)]₀¹ = (1−cos(nπ))/(n²π)
    integrals = [(1 - np.cos(n * np.pi)) / (n**2 * np.pi) for n in ns_int]
    ax2.plot(ns_int, integrals, 'o-', color='#2980b9', lw=2, ms=5,
             label=r'$\int f_n \, d\mu$')
    ax2.axhline(y=0, color='#c0392b', lw=2, ls='--',
                label=r'$\int f \, d\mu = 0$')
    ax2.set_ylim(-0.05, max(integrals) * 1.3 + 0.01)
    ax2.set_title(r"積分の収束" + "\n" + r"$\int f_n \to 0 = \int f$",
                  fontsize=9, fontweight='bold', color='#1a1a2e')
    ax2.set_xlabel('n')
    ax2.set_ylabel(r'$\int f_n \, d\mu$')
    ax2.legend(fontsize=7)

    fig.suptitle("優収束定理（Dominated Convergence Theorem）",
                 fontsize=12, fontweight='bold', color='#1a1a2e', y=1.02)
    fig.tight_layout()
    save(fig, 'fig-13')


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    fig02()
    fig04()
    fig05()
    fig07()
    fig08()
    fig10()
    fig13()
    print("\n修正完了（7枚）")
