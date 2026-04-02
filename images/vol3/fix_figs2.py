#!/usr/bin/env python3
"""Fix 3 figures: fig-02, fig-05, fig-07."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

# ── fig-02: ピラミッド図（figsize=(7,11)・上部余白25%確保・最上段2行） ──────────
def fig02():
    fig, ax = plt.subplots(figsize=(7, 9))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 10)
    # ピラミッド総高: 6*(1.0+0.18)+1.0 = 8.08。y_base=0.3 なら頂上=8.38
    # ylim を 8.7 にすればタイトルの下に 0.3 の余白のみ
    ax.set_ylim(0, 8.7)
    ax.axis('off')

    levels = [
        ("σ-代数",             0, False),
        ("測度",                1, False),
        ("可測関数",            2, False),
        ("単関数",              3, False),
        ("lintegral / integral", 4, False),
        ("収束定理",            5, False),
        (None,                  6, True),   # 最上段：2行テキストを個別描画
    ]
    blues = ['#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa',
             '#3b82f6', '#2563eb', '#1d4ed8']

    n_levels = len(levels)
    h = 1.0
    gap = 0.18
    y_base = 0.3          # ピラミッド下端（下部余白 0.3）

    for i, (label, _, is_top) in enumerate(levels):
        # 段が上になるほど幅を広くするピラミッド形状
        # 最上段だけ追加で +1.0 広くする
        extra = 1.0 if is_top else 0.0
        half = 0.5 + (n_levels - i - 1) * 0.55 + extra
        left   = 5 - half
        bottom = y_base + i * (h + gap)

        rect = patches.FancyBboxPatch(
            (left, bottom), half * 2, h,
            boxstyle="round,pad=0.05",
            facecolor=blues[i], edgecolor='#1e3a5f', linewidth=1.2)
        ax.add_patch(rect)

        text_c = 'white' if i >= 4 else '#1a1a2e'
        mid_y  = bottom + h / 2

        if is_top:
            # 最上段：2行に分けて描画（fontsize=11）
            ax.text(5, mid_y + 0.20, r'$L^p$ 空間',
                    ha='center', va='center', fontsize=11,
                    color=text_c, fontweight='bold')
            ax.text(5, mid_y - 0.22, '確率空間',
                    ha='center', va='center', fontsize=11,
                    color=text_c, fontweight='bold')
        else:
            ax.text(5, mid_y, label,
                    ha='center', va='center', fontsize=9.5,
                    color=text_c, fontweight='bold')

    ax.set_title("第3巻：測度論の構造ピラミッド", fontsize=13,
                 fontweight='bold', pad=12, color='#1a1a2e')
    save(fig, 'fig-02')

# ── fig-05: 3種類の測度比較（レイアウト再設計・ヘッダー重なり解消） ──────────────
def fig05():
    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.axis('off')
    ax.set_xlim(0, 9)
    # レイアウト（下から）:
    #   0.3  下余白
    #   3×(1.2+0.15) - 0.15 = 3.9  コンテンツ3行（行高1.2・行間0.15）
    #   0.15 ヘッダー↔コンテンツ間隔
    #   1.0  ヘッダー帯（Dirac の2行を収める高さ）
    #   残り タイトル余白
    # 合計軸高: 0.3 + 3.9 + 0.15 + 1.0 = 5.35 → ylim を 5.7 に設定
    ax.set_ylim(0, 5.7)

    rows = ["定義", "具体例", "特徴"]
    data = [
        ["区間の長さ\n（通常の長さ概念）",
         "有限集合の要素数\n（無限集合は∞）",
         "点 x のみ質量1\n（他は0）"],
        [r"$\lambda([a,b]) = b - a$",
         r"$\nu(\{1,2,3\}) = 3$" + "\n" + r"$\nu(\mathbb{N}) = \infty$",
         r"$\delta_x(\{x\}) = 1$" + "\n" + r"$\delta_x(A) = 0 \;(x \notin A)$"],
        ["連続・平行移動不変",
         "離散・加算加法的",
         "点質量・確率測度"],
    ]
    col_colors    = ['#d6eaf8', '#d5f5e3', '#fde8d8']
    header_colors = ['#2980b9', '#27ae60', '#e67e22']
    xs    = [1.5, 4.5, 7.5]
    col_w = 2.6
    row_h = 1.2
    row_gap = 0.15

    # コンテンツ行の下端座標（下から順に）
    row_ys = [0.3 + i * (row_h + row_gap) for i in range(3)]
    # コンテンツ最上端
    content_top = row_ys[2] + row_h   # = 0.3 + 2*1.35 + 1.2 = 4.2

    # ヘッダー帯: コンテンツ上端 + 0.15 の間隔をあけて開始
    hdr_bottom = content_top + 0.15   # = 4.35
    hdr_h      = 1.0                  # 2行テキストが収まる高さ

    # ── column headers ──────────────────────────────────────────────────────
    for j, hc in enumerate(header_colors):
        rect = FancyBboxPatch((xs[j] - col_w / 2, hdr_bottom), col_w, hdr_h,
                               boxstyle="round,pad=0.05",
                               facecolor=hc, edgecolor='none')
        ax.add_patch(rect)

    # 列0: Lebesgue（1行・中央）
    ax.text(xs[0], hdr_bottom + hdr_h / 2, "Lebesgue測度",
            ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # 列1: 数え上げ（1行・中央）
    ax.text(xs[1], hdr_bottom + hdr_h / 2, "数え上げ測度",
            ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # 列2: Dirac — 2行（上: 日本語、下: mathtext）をヘッダー帯中央に配置
    ax.text(xs[2], hdr_bottom + hdr_h * 0.67, "Dirac測度",
            ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    ax.text(xs[2], hdr_bottom + hdr_h * 0.30, r'$\delta_x$',
            ha='center', va='center', fontsize=12, color='white', fontweight='bold')

    # ── ヘッダー↔コンテンツ間の白い区切り線 ───────────────────────────────────
    ax.axhline(y=hdr_bottom, color='white', lw=1.5,
               xmin=0.08, xmax=0.98, zorder=5)

    # row_ys[0]=最下段, row_ys[2]=最上段 なので
    # 上から「定義→具体例→特徴」にするため逆順で割り当てる
    rows_disp = list(reversed(rows))   # ["特徴","具体例","定義"] → i=0 が最下段
    data_disp = list(reversed(data))

    # ── row labels ──────────────────────────────────────────────────────────
    for i, row in enumerate(rows_disp):
        ax.text(0.08, row_ys[i] + row_h / 2, row, ha='left', va='center',
                fontsize=9, color='#555', fontweight='bold')

    # ── cells ───────────────────────────────────────────────────────────────
    for j, cc in enumerate(col_colors):
        for i, row_y in enumerate(row_ys):
            rect = FancyBboxPatch((xs[j] - col_w / 2, row_y), col_w, row_h - 0.05,
                                   boxstyle="round,pad=0.05",
                                   facecolor=cc, edgecolor='#ccc', lw=0.8)
            ax.add_patch(rect)
            ax.text(xs[j], row_y + (row_h - 0.05) / 2, data_disp[i][j],
                    ha='center', va='center', fontsize=8, color='#1a1a2e')

    ax.set_title("3種類の測度の比較", fontsize=12,
                 fontweight='bold', pad=10, color='#1a1a2e')
    save(fig, 'fig-05')

# ── fig-07: 単関数列の矩形近似図（中点値を高さに使う・3列サブプロット） ──────────
def fig07():
    fig, axes = plt.subplots(1, 3, figsize=(11, 4))
    fig.patch.set_facecolor('white')
    for ax in axes:
        ax.set_facecolor('white')
        ax.spines[['top', 'right']].set_visible(False)

    x_fine   = np.linspace(0, 1, 500)
    f_curve  = np.sqrt(x_fine)
    fill_color = '#93c5fd'

    for idx, n in enumerate([1, 2, 4]):
        ax = axes[idx]
        xs_step = np.linspace(0, 1, n + 1)
        for i in range(n):
            # ★ 修正: 区間中点の値を高さとして使う
            mid = (xs_step[i] + xs_step[i + 1]) / 2
            val = np.sqrt(mid)
            w   = xs_step[i + 1] - xs_step[i]
            rect = patches.Rectangle(
                (xs_step[i], 0), w, val,
                facecolor=fill_color, edgecolor='black',
                linewidth=1.5, alpha=0.85,
                label='単関数' if i == 0 else '_')
            ax.add_patch(rect)

        # 赤の f(x)=√x 曲線を重ねる
        ax.plot(x_fine, f_curve, color='#c0392b', lw=2.2,
                label=r'$f(x)=\sqrt{x}$', zorder=5)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.25)
        ax.set_xlabel('x', fontsize=10)
        ax.set_ylabel('y', fontsize=10)
        ax.set_title(f'n = {n}', fontsize=11, fontweight='bold', color='#1a1a2e')
        ax.legend(fontsize=8, loc='upper left')

    fig.suptitle(r"単関数列による $f(x)=\sqrt{x}$ の近似（中点近似）",
                 fontsize=12, fontweight='bold', color='#1a1a2e')
    fig.tight_layout()
    save(fig, 'fig-07')


if __name__ == '__main__':
    fig02()
    fig05()
    fig07()
    print("\n修正完了（3枚）")
