---
title: "Part 3：Lebesgue 積分と測度論"
---

# Part 3：Lebesgue 積分と測度論

σ-代数・測度・可測関数から始め、
Lebesgue積分の主要定理（単調収束・Fatou・優収束）の仮定を確認し、Mathlibの定理を適用する例を形式化します。

**到達目標**: 非負積分の `lintegral_iSup`・`lintegral_liminf_le` と、実数値の積分に適用する `MeasureTheory.tendsto_integral_of_dominated_convergence` の理解。一般定理そのものの再証明ではなく、具体例で仮定を揃えて使うことを目指します。

第12〜17章は各3問、第18章は総合演習2問を含む5問で、計23問の章末問題があります。最後は[0,1]の一様分布の期待値と二乗の期待値を計算し、同じ関数からL²の元を作ってノルムの二乗まで求めます。

**前提知識**: Part 2 修了・実解析の基礎
