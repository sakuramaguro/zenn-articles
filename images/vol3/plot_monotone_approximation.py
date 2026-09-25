#!/usr/bin/env python3
"""Rebuild figure 15-1: dyadic lower approximations to sqrt on [0, 1].

Requires matplotlib and numpy. Run from any directory; writes only fig-07.png/svg
next to this file. This illustrative sequence is not Mathlib's eapprox.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np


def main():
    available = {font.name for font in font_manager.fontManager.ttflist}
    font = next((name for name in ("Hiragino Sans", "Noto Sans CJK JP", "IPAexGothic")
                 if name in available), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "axes.unicode_minus": False,
                         "svg.hashsalt": "lean-book-monotone-approximation",
                         "font.size": 11})
    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.1), sharex=True, sharey=True)
    x = np.linspace(0, 1, 4097)
    curve = np.sqrt(x)
    previous = np.zeros_like(x)
    for n, ax in enumerate(axes, 1):
        steps = 2 ** n
        approximation = np.floor(steps * curve) / steps
        assert np.all(previous <= approximation)
        assert np.all(approximation <= curve)
        assert np.all(curve - approximation < 1 / steps)
        previous = approximation
        ax.plot(x, curve, color="#202b3b", linewidth=1.8, label=r"$f(x)=\sqrt{x}$")
        for k in range(steps):
            left, right = (k / steps) ** 2, ((k + 1) / steps) ** 2
            level = k / steps
            ax.hlines(level, left, right, color="#2563eb", linewidth=2)
            ax.plot(right, level, "o", color="#2563eb", markerfacecolor="white", markersize=4)
            ax.plot(left, level, "o", color="#2563eb", markersize=4)
        ax.plot(1, 1, "o", color="#2563eb", markersize=4)
        ax.plot([], [], color="#2563eb", linewidth=2, label=rf"$\varphi_{n}(x)$")
        ax.set_title(rf"$n={n}$：高さの刻み $1/{steps}$", fontsize=12, pad=12)
        ax.set_xlim(-0.025, 1.025)
        ax.set_ylim(-0.035, 1.06)
        ax.set_xticks([0, 0.5, 1])
        ax.set_yticks([0, 0.5, 1])
        ax.set_xlabel(r"$x$")
        ax.grid(alpha=0.18)
        ax.set_axisbelow(True)
        ax.legend(loc="lower right", fontsize=10, framealpha=0.94)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("関数の値")
    fig.suptitle("単関数による単調な下側近似", fontsize=16, y=0.99)
    fig.text(0.5, 0.035,
             r"$0\leq\varphi_1\leq\varphi_2\leq\varphi_3\leq\sqrt{x}$"
             "    ● 含む端点　○ 含まない端点",
             ha="center", fontsize=11)
    fig.subplots_adjust(top=0.79, bottom=0.22, left=0.065, right=0.985, wspace=0.17)
    output = Path(__file__).resolve().parent
    fig.savefig(output / "fig-07.png", dpi=210, facecolor="white")
    fig.savefig(output / "fig-07.svg", facecolor="white", metadata={"Date": None})
    svg = output / "fig-07.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    plt.close(fig)


if __name__ == "__main__":
    main()
