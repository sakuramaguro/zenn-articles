#!/usr/bin/env python3
"""Generate 8 figures for vol1 of the Lean 4 series."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as FancyBboxPatch
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ---------- Font setup ----------
plt.rcParams['font.family'] = ['Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

OUT = os.path.dirname(os.path.abspath(__file__))

COLORS = {
    'bg':       '#FFFFFF',
    'box':      '#F0F4F8',
    'box_dark': '#D6E4F0',
    'accent':   '#2563EB',   # blue
    'accent2':  '#059669',   # green
    'accent3':  '#DC2626',   # red
    'accent4':  '#D97706',   # amber
    'text':     '#1E293B',
    'subtext':  '#64748B',
    'border':   '#CBD5E1',
    'highlight':'#DBEAFE',
    'row_alt':  '#F8FAFC',
}

def save(fig, name):
    png = os.path.join(OUT, f'{name}.png')
    svg = os.path.join(OUT, f'{name}.svg')
    fig.savefig(png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(svg, bbox_inches='tight', facecolor='white')
    print(f'  saved: {name}.png / {name}.svg')
    plt.close(fig)

def rounded_box(ax, x, y, w, h, text, subtext=None,
                fc=COLORS['box'], ec=COLORS['border'], lw=1.2,
                fontsize=11, subfontsize=9, bold=False, radius=0.04):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle=f'round,pad=0,rounding_size={radius}',
                         fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ty = y + (h * 0.12 if subtext else 0)
    ax.text(x, ty, text, ha='center', va='center',
            fontsize=fontsize, color=COLORS['text'], weight=weight, zorder=4)
    if subtext:
        ax.text(x, y - h * 0.2, subtext, ha='center', va='center',
                fontsize=subfontsize, color=COLORS['subtext'], zorder=4)

def arrow(ax, x1, y1, x2, y2, color=COLORS['subtext'], lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, connectionstyle='arc3,rad=0'))

# =====================================================================
# fig-01: シリーズロードマップ
# =====================================================================
def fig01():
    fig, ax = plt.subplots(figsize=(7, 9))
    ax.set_xlim(0, 7); ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    ax.text(3.5, 8.55, 'Lean 4 形式化シリーズ ロードマップ',
            ha='center', va='center', fontsize=14, weight='bold', color=COLORS['text'])

    volumes = [
        ('第4巻', '確率微分方程式\n（SDE）の形式化',
         '確率過程・伊藤積分・filtration', COLORS['accent'], True),
        ('第3巻', '測度論・Lebesgue 積分\nの形式化',
         'σ-代数・測度空間・Lp 空間', COLORS['accent2'], False),
        ('第2巻', '位相空間論・Banach\nの形式化',
         'ε-δ・完備距離空間・不動点定理', COLORS['accent4'], False),
        ('第1巻（本書）', 'Lean 4 入門・型クラス・\n次元定理の機械検証',
         '型・証明・Mathlib 探索', '#BE185D', False),
    ]

    ys = [7.3, 5.6, 3.9, 2.2]

    for i, (vol, title, keywords, color, _) in enumerate(volumes):
        y = ys[i]
        is_current = (i == 3)  # 第1巻 = 最下段強調
        fc = COLORS['highlight'] if is_current else COLORS['box']
        ec = color
        lw = 2.5 if is_current else 1.5

        box = FancyBboxPatch((0.5, y - 0.65), 6, 1.3,
                             boxstyle='round,pad=0,rounding_size=0.08',
                             fc=fc, ec=ec, lw=lw, zorder=3)
        ax.add_patch(box)

        # 巻ラベル
        label_box = FancyBboxPatch((0.5, y - 0.65), 1.3, 1.3,
                                   boxstyle='round,pad=0,rounding_size=0.08',
                                   fc=color, ec=color, lw=0, zorder=4)
        ax.add_patch(label_box)
        ax.text(1.15, y, vol, ha='center', va='center',
                fontsize=9, weight='bold', color='white', zorder=5)

        ax.text(2.2, y + 0.18, title, ha='left', va='center',
                fontsize=10, weight='bold' if is_current else 'normal',
                color=COLORS['text'], zorder=4)
        ax.text(2.2, y - 0.27, keywords, ha='left', va='center',
                fontsize=8, color=COLORS['subtext'], zorder=4)

        if is_current:
            ax.text(6.3, y, '← いまここ', ha='right', va='center',
                    fontsize=9, color=color, weight='bold', zorder=4)

    # 矢印（上向き、第1巻→第4巻）
    for i in range(3):
        y_from = ys[3 - i] + 0.65
        y_to   = ys[3 - i - 1] - 0.65
        ax.annotate('', xy=(3.5, y_to), xytext=(3.5, y_from),
                    arrowprops=dict(arrowstyle='->', color=COLORS['subtext'],
                                    lw=1.5), zorder=2)

    ax.text(3.5, 0.75,
            '到達点：$dX_t = b(t, X_t)\\,dt + \\sigma(t, X_t)\\,dW_t$',
            ha='center', va='center', fontsize=11,
            color=COLORS['accent'], style='italic')

    save(fig, 'fig-01')

# =====================================================================
# fig-02: 型の階層図
# =====================================================================
def fig02():
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 7.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, 7.1, 'Lean 4 の型の階層', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    # ---- 中央の階層ツリー ----
    # Type* (root)
    root_y = 6.0
    ax.add_patch(FancyBboxPatch((2.8, root_y - 0.32), 2.4, 0.64,
                 boxstyle='round,pad=0,rounding_size=0.06',
                 fc=COLORS['accent'], ec=COLORS['accent'], lw=0, zorder=3))
    ax.text(4.0, root_y, 'Type*（宇宙・最上位）', ha='center', va='center',
            fontsize=10, weight='bold', color='white', zorder=4)

    nodes = [
        # (x, y, label, sublabel, color)
        (1.5, 4.4, 'Prop', '命題・証明の型', '#7C3AED'),
        (4.0, 4.4, 'Nat, Int, Real', 'データ型（数値）', COLORS['accent2']),
        (6.7, 4.4, 'List α, Option α', 'パラメータ付き型', COLORS['accent4']),
    ]

    for (x, y, label, sub, color) in nodes:
        ax.add_patch(FancyBboxPatch((x - 1.1, y - 0.38), 2.2, 0.76,
                     boxstyle='round,pad=0,rounding_size=0.06',
                     fc=color, ec=color, lw=0, zorder=3))
        ax.text(x, y + 0.1, label, ha='center', va='center',
                fontsize=9.5, weight='bold', color='white', zorder=4)
        ax.text(x, y - 0.18, sub, ha='center', va='center',
                fontsize=8, color='white', alpha=0.9, zorder=4)

    # 枝
    for (x, y, *_) in nodes:
        ax.annotate('', xy=(x, y + 0.38), xytext=(4.0, root_y - 0.32),
                    arrowprops=dict(arrowstyle='->', color=COLORS['subtext'],
                                    lw=1.2, connectionstyle='arc3,rad=0'), zorder=2)

    # Prop の子
    prop_children = [
        (0.7, 2.8, '0 = 0 : Prop', 'rfl で証明'),
        (2.3, 2.8, '1 + 1 = 2 : Prop', 'norm_num で証明'),
    ]
    for (x, y, label, sub) in prop_children:
        ax.add_patch(FancyBboxPatch((x - 0.75, y - 0.32), 1.5, 0.64,
                     boxstyle='round,pad=0,rounding_size=0.05',
                     fc='#EDE9FE', ec='#7C3AED', lw=1.2, zorder=3))
        ax.text(x, y + 0.08, label, ha='center', va='center',
                fontsize=8, color=COLORS['text'], zorder=4)
        ax.text(x, y - 0.16, sub, ha='center', va='center',
                fontsize=7.5, color=COLORS['subtext'], zorder=4)
        ax.annotate('', xy=(x, y + 0.32), xytext=(1.5, 4.4 - 0.38),
                    arrowprops=dict(arrowstyle='->', color='#7C3AED',
                                    lw=1.0, connectionstyle='arc3,rad=0'), zorder=2)

    # ---- 右側注釈パネル ----
    # 数学学部生向け
    ax.add_patch(FancyBboxPatch((7.6, 3.5), 2.1, 2.8,
                 boxstyle='round,pad=0,rounding_size=0.06',
                 fc='#F0FDF4', ec=COLORS['accent2'], lw=1.2, zorder=3))
    ax.text(8.65, 6.1, '数学との対応', ha='center', va='center',
            fontsize=9, weight='bold', color=COLORS['accent2'], zorder=4)
    math_notes = [
        ('型', '= 集合'),
        ('値 a : α', '= 元 a ∈ A'),
        ('Prop', '= 命題'),
        ('証明項', '= 証明'),
        ('Type*', '= 集合の宇宙'),
    ]
    for j, (k, v) in enumerate(math_notes):
        y_n = 5.75 - j * 0.45
        ax.text(7.75, y_n, k, ha='left', va='center',
                fontsize=8, color=COLORS['text'], zorder=4)
        ax.text(8.65, y_n, v, ha='center', va='center',
                fontsize=8, color=COLORS['subtext'], zorder=4)

    # プログラマ向け
    ax.add_patch(FancyBboxPatch((7.6, 0.4), 2.1, 2.8,
                 boxstyle='round,pad=0,rounding_size=0.06',
                 fc='#EFF6FF', ec=COLORS['accent'], lw=1.2, zorder=3))
    ax.text(8.65, 3.0, 'プログラマとの対応', ha='center', va='center',
            fontsize=9, weight='bold', color=COLORS['accent'], zorder=4)
    prog_notes = [
        ('型', '= TypeScript の型'),
        ('Prop', '= 論理式'),
        ('証明項', '= 型付き値'),
        ('Type*', '= Kind（型の型）'),
        ('型クラス', '= interface'),
    ]
    for j, (k, v) in enumerate(prog_notes):
        y_n = 2.65 - j * 0.45
        ax.text(7.75, y_n, k, ha='left', va='center',
                fontsize=8, color=COLORS['text'], zorder=4)
        ax.text(8.65, y_n, v, ha='center', va='center',
                fontsize=8, color=COLORS['subtext'], zorder=4)

    save(fig, 'fig-02')

# =====================================================================
# fig-03: 証明の実況中継フロー図
# =====================================================================
def fig03():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.5, 5.6, '証明の実況中継フロー', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    steps = [
        (1.6, 3.5, '①', 'ゴール確認\n（InfoView）', '現在の証明状態を\nInfoView で確認'),
        (5.5, 3.5, '②', 'タクティク適用', 'rfl / ring / simp など\nを書いてみる'),
        (9.4, 3.5, '③', '新しいゴール確認', '変化したゴールを\n再度 InfoView で確認'),
    ]

    for (x, y, step_no, title, desc) in steps:
        # 外枠
        ax.add_patch(FancyBboxPatch((x - 1.3, y - 0.9), 2.6, 1.8,
                     boxstyle='round,pad=0,rounding_size=0.08',
                     fc=COLORS['highlight'], ec=COLORS['accent'], lw=2.0, zorder=3))
        # ステップ番号
        circle = plt.Circle((x - 0.9, y + 0.55), 0.22,
                             color=COLORS['accent'], zorder=5)
        ax.add_patch(circle)
        ax.text(x - 0.9, y + 0.55, step_no, ha='center', va='center',
                fontsize=9, weight='bold', color='white', zorder=6)
        ax.text(x, y + 0.35, title, ha='center', va='center',
                fontsize=10, weight='bold', color=COLORS['text'], zorder=4)
        ax.text(x, y - 0.2, desc, ha='center', va='center',
                fontsize=8.5, color=COLORS['subtext'], zorder=4)

    # 矢印
    arrow(ax, 2.9, 3.5, 4.2, 3.5, lw=2)
    arrow(ax, 6.8, 3.5, 8.1, 3.5, lw=2)

    # 「繰り返す」ループ矢印
    ax.annotate('', xy=(1.6, 2.6), xytext=(9.4, 2.6),
                arrowprops=dict(arrowstyle='<-', color=COLORS['subtext'],
                                lw=1.5, connectionstyle='arc3,rad=-0.3'), zorder=2)
    ax.text(5.5, 1.85, '証明が完了するまで繰り返す', ha='center', va='center',
            fontsize=8.5, color=COLORS['subtext'], style='italic')

    # InfoView モック画面
    mock_y = 0.25
    ax.add_patch(FancyBboxPatch((1.5, mock_y), 8, 1.3,
                 boxstyle='round,pad=0,rounding_size=0.06',
                 fc='#1E293B', ec='#334155', lw=1.5, zorder=3))
    ax.text(2.0, mock_y + 1.0, '▌Lean InfoView',
            ha='left', va='center', fontsize=8.5, color='#94A3B8',
            fontfamily='monospace', zorder=4)
    ax.text(2.0, mock_y + 0.65, '⊢ ∀ (n : ℕ), 0 + n = n',
            ha='left', va='center', fontsize=9, color='#7DD3FC',
            fontfamily='monospace', zorder=4)
    ax.text(2.0, mock_y + 0.35, '─── after  simp ───',
            ha='left', va='center', fontsize=9, color='#94A3B8',
            fontfamily='monospace', zorder=4)
    ax.text(2.0, mock_y + 0.08, 'No goals  ✓',
            ha='left', va='center', fontsize=9, color='#4ADE80',
            fontfamily='monospace', weight='bold', zorder=4)

    save(fig, 'fig-03')

# =====================================================================
# fig-04: タクティクの守備範囲図
# =====================================================================
def fig04():
    tactics = [
        ('rfl',       '両辺が定義的に等しいとき（0 + 0 = 0 など）'),
        ('ring',      '環の等式（多項式の計算）を自動解決'),
        ('norm_num',  '数値計算・不等式を自動解決'),
        ('linarith',  '線形算術（一次不等式の組合せ）を解決'),
        ('omega',     '整数・自然数の線形算術を解決'),
        ('simp',      '定理データベースで式を簡約・書き換え'),
        ('exact',     '証明項を直接指定して完了させる'),
        ('apply',     '補題の結論がゴールに一致するとき適用'),
        ('intro',     '全称∀や含意P→Qをゴールから仮定へ移動'),
        ('have',      '補題を名前付きで導入（証明を分割する）'),
    ]

    n = len(tactics)
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, n + 1.2)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, n + 0.75, 'タクティクの守備範囲', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    # ヘッダー
    ax.add_patch(FancyBboxPatch((0.2, n + 0.05), 9.6, 0.55,
                 boxstyle='round,pad=0,rounding_size=0.04',
                 fc=COLORS['accent'], ec=COLORS['accent'], lw=0, zorder=3))
    ax.text(1.55, n + 0.32, 'タクティク名', ha='center', va='center',
            fontsize=10, weight='bold', color='white', zorder=4)
    ax.text(5.8, n + 0.32, '使う場面', ha='center', va='center',
            fontsize=10, weight='bold', color='white', zorder=4)

    for i, (tac, desc) in enumerate(tactics):
        y = n - 1 - i
        fc = COLORS['box'] if i % 2 == 0 else COLORS['row_alt']
        ax.add_patch(FancyBboxPatch((0.2, y + 0.05), 9.6, 0.85,
                     boxstyle='round,pad=0,rounding_size=0.03',
                     fc=fc, ec=COLORS['border'], lw=0.8, zorder=2))
        # タクティク名（モノスペース風）
        ax.add_patch(FancyBboxPatch((0.3, y + 0.14), 2.3, 0.67,
                     boxstyle='round,pad=0,rounding_size=0.04',
                     fc=COLORS['highlight'], ec=COLORS['accent'], lw=1.2, zorder=3))
        ax.text(1.45, y + 0.475, tac, ha='center', va='center',
                fontsize=11, color=COLORS['accent'], weight='bold',
                fontfamily='monospace', zorder=4)
        # 説明
        ax.text(2.8, y + 0.475, desc, ha='left', va='center',
                fontsize=9, color=COLORS['text'], zorder=3)

    save(fig, 'fig-04')

# =====================================================================
# fig-05: Claude への「3点セット」質問図
# =====================================================================
def fig05():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, 7.6, 'Claude への「3点セット」質問図', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    items = [
        ('①', '証明したいこと（Lean コード）',
         'theorem dim_theorem : ...\n-- sorry',
         '#7C3AED', '#F5F3FF'),
        ('②', 'エラーメッセージ（全文）',
         'failed to synthesize instance\n[FiniteDimensional K V]',
         COLORS['accent3'], '#FEF2F2'),
        ('③', '試したこと（タクティクの履歴）',
         'exact? -> timeout\napply? -> no match',
         COLORS['accent2'], '#F0FDF4'),
    ]

    ys = [6.0, 4.2, 2.4]
    for i, ((num, title, example, color, fc), y) in enumerate(zip(items, ys)):
        # 外枠
        ax.add_patch(FancyBboxPatch((0.3, y - 0.68), 5.8, 1.36,
                     boxstyle='round,pad=0,rounding_size=0.07',
                     fc=fc, ec=color, lw=2.0, zorder=3))
        # 番号バッジ
        ax.add_patch(plt.Circle((0.75, y), 0.24, color=color, zorder=5))
        ax.text(0.75, y, num, ha='center', va='center',
                fontsize=9.5, weight='bold', color='white', zorder=6)
        ax.text(3.0, y + 0.32, title, ha='center', va='center',
                fontsize=10, weight='bold', color=COLORS['text'], zorder=4)
        ax.text(3.0, y - 0.2, example, ha='center', va='center',
                fontsize=8.5, color=color,
                fontfamily=['Courier New', 'monospace'], zorder=4)

    # 矢印①→②→③→Claude
    for y_from, y_to in [(ys[0] - 0.68, ys[1] + 0.68),
                          (ys[1] - 0.68, ys[2] + 0.68)]:
        ax.annotate('', xy=(3.2, y_to), xytext=(3.2, y_from),
                    arrowprops=dict(arrowstyle='->', color=COLORS['subtext'],
                                    lw=1.5), zorder=2)

    # Claude へ
    claude_y = 1.0
    ax.add_patch(FancyBboxPatch((0.3, claude_y - 0.42), 5.8, 0.84,
                 boxstyle='round,pad=0,rounding_size=0.07',
                 fc=COLORS['accent'], ec=COLORS['accent'], lw=0, zorder=3))
    ax.annotate('', xy=(3.2, claude_y + 0.42), xytext=(3.2, ys[2] - 0.68),
                arrowprops=dict(arrowstyle='->', color=COLORS['accent'],
                                lw=2.0), zorder=2)
    ax.text(3.2, claude_y, 'Claude への質問', ha='center', va='center',
            fontsize=11, weight='bold', color='white', zorder=4)

    # やってはいけないこと（右パネル）
    ax.add_patch(FancyBboxPatch((6.5, 0.6), 3.2, 5.8,
                 boxstyle='round,pad=0,rounding_size=0.07',
                 fc='#FFF5F5', ec=COLORS['accent3'], lw=1.5, zorder=3))
    ax.text(8.1, 6.2, 'やってはいけないこと', ha='center', va='center',
            fontsize=10, weight='bold', color=COLORS['accent3'], zorder=4)

    ng_items = [
        '✗ 「証明して」だけを送る',
        '✗ エラーを省略して送る',
        '✗ 長いコードを\n  丸ごと貼り付ける',
        '✗ 試したことを\n  書かずに聞く',
        '✗ ゴールを説明せず\n  「なぜ動かない？」',
    ]
    for j, item in enumerate(ng_items):
        ax.text(6.75, 5.75 - j * 0.95, item, ha='left', va='center',
                fontsize=8.5, color=COLORS['accent3'], zorder=4)

    save(fig, 'fig-05')

# =====================================================================
# fig-06: Mathlib 探索フローチャート
# =====================================================================
def fig06():
    fig, ax = plt.subplots(figsize=(9, 10))
    ax.set_xlim(0, 9); ax.set_ylim(0, 10)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(4.5, 9.6, 'Mathlib 探索フローチャート', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    def box(x, y, text, w=2.8, h=0.58, fc=COLORS['box'], ec=COLORS['border'],
            fontsize=9, bold=False):
        ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h,
                     boxstyle='round,pad=0,rounding_size=0.05',
                     fc=fc, ec=ec, lw=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center',
                fontsize=fontsize, color=COLORS['text'],
                weight='bold' if bold else 'normal',
                zorder=4)

    def diamond(x, y, text, w=2.6, h=0.6):
        dx, dy = w/2, h/2
        pts = [(x, y+dy), (x+dx, y), (x, y-dy), (x-dx, y)]
        poly = plt.Polygon(pts, fc='#FFFBEB', ec=COLORS['accent4'],
                           lw=1.5, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center',
                fontsize=8.5, color=COLORS['text'], zorder=4)

    def done(x, y, text):
        ax.add_patch(FancyBboxPatch((x - 1.2, y - 0.28), 2.4, 0.56,
                     boxstyle='round,pad=0,rounding_size=0.05',
                     fc='#DCFCE7', ec=COLORS['accent2'], lw=1.5, zorder=3))
        ax.text(x, y, text, ha='center', va='center',
                fontsize=9, color=COLORS['accent2'], weight='bold', zorder=4)

    # スタート
    box(4.5, 9.0, '目的の補題を探したい', w=3.2, h=0.5,
        fc=COLORS['accent'], ec=COLORS['accent'], bold=False)
    ax.texts[-1].set_color('white')

    arrow(ax, 4.5, 8.75, 4.5, 8.2)
    box(4.5, 7.9, 'exact? を試す', w=2.6, fc=COLORS['highlight'], ec=COLORS['accent'])
    arrow(ax, 4.5, 7.62, 4.5, 7.1)

    diamond(4.5, 6.8, '見つかった？')

    # Yes → 完了
    arrow(ax, 5.8, 6.8, 7.0, 6.8)
    ax.text(6.35, 6.95, 'Yes', fontsize=8, color=COLORS['accent2'], ha='center')
    done(7.5, 6.8, '完了 ✓')

    # No → apply?
    arrow(ax, 4.5, 6.5, 4.5, 5.95)
    ax.text(4.75, 6.22, 'No /\nタイムアウト', fontsize=7.5, color=COLORS['subtext'],
            ha='left', va='center')
    box(4.5, 5.65, 'apply? を試す', w=2.6, fc=COLORS['highlight'], ec=COLORS['accent'])
    arrow(ax, 4.5, 5.37, 4.5, 4.85)

    diamond(4.5, 4.55, '見つかった？')

    arrow(ax, 5.8, 4.55, 7.0, 4.55)
    ax.text(6.35, 4.7, 'Yes', fontsize=8, color=COLORS['accent2'], ha='center')
    done(7.5, 4.55, '完了 ✓')

    arrow(ax, 4.5, 4.25, 4.5, 3.7)
    ax.text(4.75, 3.97, 'No', fontsize=7.5, color=COLORS['subtext'], ha='left')
    box(4.5, 3.4, 'Mathlib4Docs / Loogle で検索', w=3.4,
        fc='#FFFBEB', ec=COLORS['accent4'])
    arrow(ax, 4.5, 3.12, 4.5, 2.6)

    diamond(4.5, 2.3, '見つかった？')

    # Yes → #check
    arrow(ax, 5.8, 2.3, 6.5, 2.3)
    ax.text(6.1, 2.45, 'Yes', fontsize=8, color=COLORS['accent2'], ha='center')
    box(7.3, 2.3, '#check で型確認', w=2.4, fc=COLORS['highlight'],
        ec=COLORS['accent'])
    arrow(ax, 7.3, 2.02, 7.3, 1.52)
    done(7.3, 1.27, '完了 ✓')

    # No → Claude
    arrow(ax, 4.5, 2.0, 4.5, 1.45)
    ax.text(4.75, 1.72, 'No', fontsize=7.5, color=COLORS['subtext'], ha='left')
    ax.add_patch(FancyBboxPatch((2.0, 0.65), 5.0, 0.65,
                 boxstyle='round,pad=0,rounding_size=0.06',
                 fc='#EDE9FE', ec='#7C3AED', lw=1.5, zorder=3))
    ax.text(4.5, 0.975, 'Claude に 3点セットで質問', ha='center', va='center',
            fontsize=9, color='#7C3AED', weight='bold', zorder=4)

    save(fig, 'fig-06')

# =====================================================================
# fig-07: 線形写像の数学↔Lean 対比図
# =====================================================================
def fig07():
    rows = [
        ('$f: V \\to W$（線形）',       'f : V →ₗ[K] W',               '写像の型'),
        ('$\\ker f$',                    'LinearMap.ker f',              '核'),
        ('$\\operatorname{im} f$',       'LinearMap.range f',            '像'),
        ('$\\dim V$',                    'Module.finrank K V',           '次元'),
        ('$\\dim(\\ker f) + \\dim(\\operatorname{im} f)$\n$= \\dim V$',
                                         'LinearMap.finrank_range_add\n_finrank_ker',
                                                                         '次元定理'),
    ]

    n = len(rows)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11); ax.set_ylim(0, n + 1.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.5, n + 1.1, '線形写像の　数学 ↔ Lean 対比', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    col_colors = [COLORS['accent'], COLORS['accent2'], COLORS['accent4']]
    headers = ['数学の記法', 'Lean の記法', '意味']
    col_x = [2.0, 6.5, 9.8]
    col_w = [3.5, 4.5, 2.0]

    # ヘッダー
    for j, (hdr, cx, cw, cc) in enumerate(zip(headers, col_x, col_w, col_colors)):
        ax.add_patch(FancyBboxPatch((cx - cw/2, n + 0.05), cw - 0.1, 0.75,
                     boxstyle='round,pad=0,rounding_size=0.05',
                     fc=cc, ec=cc, lw=0, zorder=3))
        ax.text(cx, n + 0.425, hdr, ha='center', va='center',
                fontsize=10.5, weight='bold', color='white', zorder=4)

    row_fcs = ['#EFF6FF', '#F0FDF4', '#FFFBEB', '#F5F3FF', '#FFF1F2']

    for i, (math_text, lean_text, meaning) in enumerate(rows):
        y = n - 1 - i
        fc = row_fcs[i % len(row_fcs)]
        ax.add_patch(FancyBboxPatch((0.2, y + 0.05), 10.6, 0.85,
                     boxstyle='round,pad=0,rounding_size=0.04',
                     fc=fc, ec=COLORS['border'], lw=0.8, zorder=2))
        ax.text(col_x[0], y + 0.46, math_text, ha='center', va='center',
                fontsize=10, color=COLORS['text'], zorder=3)
        ax.text(col_x[1], y + 0.46, lean_text, ha='center', va='center',
                fontsize=9, color=COLORS['accent'], fontfamily='monospace', zorder=3)
        ax.text(col_x[2], y + 0.46, meaning, ha='center', va='center',
                fontsize=9, color=COLORS['subtext'], zorder=3)

        # 左右を結ぶ矢印
        ax.annotate('', xy=(col_x[1] - col_w[1]/2 + 0.15, y + 0.46),
                    xytext=(col_x[0] + col_w[0]/2 - 0.15, y + 0.46),
                    arrowprops=dict(arrowstyle='<->', color=COLORS['subtext'],
                                    lw=1.2), zorder=4)

    save(fig, 'fig-07')

# =====================================================================
# fig-08: 次元定理の証明構造図
# =====================================================================
def fig08():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.5, 7.1, '次元定理の証明構造図', ha='center', va='center',
            fontsize=14, weight='bold', color=COLORS['text'])

    # ルート
    root_y = 6.1
    ax.add_patch(FancyBboxPatch((2.8, root_y - 0.42), 5.4, 0.84,
                 boxstyle='round,pad=0,rounding_size=0.07',
                 fc=COLORS['accent'], ec=COLORS['accent'], lw=0, zorder=3))
    ax.text(5.5, root_y, '次元定理\n(finrank_range_add_finrank_ker)',
            ha='center', va='center', fontsize=10, weight='bold',
            color='white', zorder=4)

    # have で分解した3つのサブゴール
    sub_nodes = [
        (1.5, 4.2, 'h_ker',
         'ker の\n有限次元性',
         'Submodule.finite\nDimensional_of_le',
         '#7C3AED', '#F5F3FF'),
        (5.5, 4.2, 'h_range',
         'range の\n有限次元性',
         'LinearMap.finite\nDimensional_range',
         COLORS['accent2'], '#F0FDF4'),
        (9.5, 4.2, 'key',
         'dim ker +\ndim range = dim V',
         'finrank_add_finrank\n_compl',
         COLORS['accent4'], '#FFFBEB'),
    ]

    for (x, y, name, title, tactic, color, fc) in sub_nodes:
        # 上部ノード
        ax.add_patch(FancyBboxPatch((x - 1.6, y + 0.05), 3.2, 0.75,
                     boxstyle='round,pad=0,rounding_size=0.06',
                     fc=color, ec=color, lw=0, zorder=3))
        ax.text(x, y + 0.42, f'have {name}', ha='center', va='center',
                fontsize=8.5, weight='bold', color='white',
                fontfamily='monospace', zorder=4)

        # 下部詳細
        ax.add_patch(FancyBboxPatch((x - 1.6, y - 1.1), 3.2, 1.1,
                     boxstyle='round,pad=0,rounding_size=0.06',
                     fc=fc, ec=color, lw=1.5, zorder=3))
        ax.text(x, y - 0.27, title, ha='center', va='center',
                fontsize=9, weight='bold', color=COLORS['text'], zorder=4)
        ax.text(x, y - 0.78, tactic, ha='center', va='center',
                fontsize=7.5, color=color, fontfamily='monospace', zorder=4)

        # ルートからの矢印
        ax.annotate('', xy=(x, y + 0.8), xytext=(5.5, root_y - 0.42),
                    arrowprops=dict(arrowstyle='->', color=COLORS['subtext'],
                                    lw=1.5, connectionstyle='arc3,rad=0'), zorder=2)

    # 3つが合流して証明完了
    merge_y = 1.6
    for x in [1.5, 5.5, 9.5]:
        ax.annotate('', xy=(5.5, merge_y + 0.42), xytext=(x, 3.1),
                    arrowprops=dict(arrowstyle='->', color=COLORS['subtext'],
                                    lw=1.5, connectionstyle='arc3,rad=0'), zorder=2)

    ax.add_patch(FancyBboxPatch((2.8, merge_y - 0.42), 5.4, 0.84,
                 boxstyle='round,pad=0,rounding_size=0.07',
                 fc='#DCFCE7', ec=COLORS['accent2'], lw=2.0, zorder=3))
    ax.text(5.5, merge_y, '証明完了  No goals ✓',
            ha='center', va='center', fontsize=11, weight='bold',
            color=COLORS['accent2'], zorder=4)

    # タクティク注釈
    ax.text(5.5, 0.8, '使用タクティク: have · exact · apply · simp · linarith · finrank_add_finrank_compl',
            ha='center', va='center', fontsize=8.5, color=COLORS['subtext'],
            style='italic')

    save(fig, 'fig-08')


# ---- main ----
if __name__ == '__main__':
    print('Generating figures...')
    fig01()
    fig02()
    fig03()
    fig04()
    fig05()
    fig06()
    fig07()
    fig08()
    print('Done.')
