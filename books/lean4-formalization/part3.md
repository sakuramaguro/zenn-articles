---
title: "Part 3：Lebesgue 積分と測度論"
---

# Part 3：Lebesgue 積分と測度論

σ-代数・測度・可測関数から始め、
Lebesgue積分の主要定理（単調収束・Fatou・優収束）の仮定を確認し、Mathlibの定理を適用する例を形式化します。

**到達目標**: 非負積分の `lintegral_iSup`・`lintegral_liminf_le` と、実数値の積分に適用する `MeasureTheory.tendsto_integral_of_dominated_convergence` の理解。一般定理そのものの再証明ではなく、具体例で仮定を揃えて使うことを目指します。

**前提知識**: Part 2 修了・実解析の基礎
