import Mathlib

namespace LeanBook.Ch06

-- BEGIN SOURCE ch06_001
-- 第5章の予告に連続性の仮定 hf を追加した修正版
theorem continuous_search (f : ℝ → ℝ) (a : ℝ) (hf : ContinuousAt f a) :
    Filter.Tendsto f (nhds a) (nhds (f a)) := by
  exact?
-- END SOURCE ch06_001

-- BEGIN SOURCE ch06_002
-- 本章の最終ゴール：Part 1の予告コードの構造を理解する

-- 【勝利の命題①】Filter.Tendsto と ContinuousAt の関係
-- 数学：連続性の定義は「近傍フィルターが保たれること」と同値
-- Lean：ContinuousAt の定義そのものが Filter.Tendsto である
theorem continuous_preview (f : ℝ → ℝ) (a : ℝ) (hf : ContinuousAt f a) :
    Filter.Tendsto f (nhds a) (nhds (f a)) :=
  hf  -- No goals ✓

-- 【勝利の命題②】双方向の同値（これが本章の核心）
-- 数学：ここで指定した2つの近傍フィルターでの Tendsto は ContinuousAt と同じ命題
-- Lean：Iff.rfl が通る = 展開すると左辺と右辺が文字通り同じ
theorem tendsto_iff_continuousAt_preview (f : ℝ → ℝ) (a : ℝ) :
    Filter.Tendsto f (nhds a) (nhds (f a)) ↔ ContinuousAt f a :=
  Iff.rfl  -- No goals ✓

-- 【勝利の命題③】nhds の正体
-- 数学：nhds a は「a の近傍全体が生成するフィルター」
-- Lean：#check で型だけでも確認できる
#check @nhds
-- nhds : ∀ {α : Type u_1} [inst : TopologicalSpace α], α → Filter α
-- END SOURCE ch06_002

-- BEGIN SOURCE ch06_004

-- 内側の f は a で、外側の g は f a で連続と仮定する
theorem continuousCompositionEpsilonDelta (f g : ℝ → ℝ) (a : ℝ)
    (hf : ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - f a| < ε)
    (hg : ∀ ε > 0, ∃ δ > 0, ∀ y : ℝ, |y - f a| < δ → |g y - g (f a)| < ε) :
    ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ,
      |x - a| < δ → |(g ∘ f) x - (g ∘ f) a| < ε := by
  intro ε hε
  obtain ⟨η, hη, hgη⟩ := hg ε hε
  obtain ⟨δ, hδ, hfδ⟩ := hf η hη
  exact ⟨δ, hδ, fun x hx => hgη (f x) (hfδ x hx)⟩
-- END SOURCE ch06_004

-- BEGIN SOURCE ch06_005

#check Filter.NeBot
-- f.NeBot は f ≠ ⊥ を要求する。空集合が f に属さないことと同値。
theorem real_nhds_neBot (a : ℝ) : (nhds a).NeBot := inferInstance
-- END SOURCE ch06_005

-- BEGIN SOURCE ch06_006

-- Mathlib.Order.Filter.Defs の実際の構造を表示する
#print Filter
#check @Filter.univ_sets
#check @Filter.sets_of_superset
#check @Filter.inter_sets
-- END SOURCE ch06_006

-- BEGIN SOURCE ch06_007

-- 型の確認
#check Filter
-- Filter : Type u_1 → Type u_1
-- END SOURCE ch06_007

-- BEGIN SOURCE ch06_008

-- 数学：ℱ∞ = { S ⊆ ℕ | ∃ N, ∀ n ≥ N, n ∈ S }
-- Lean：Filter.atTop : Filter ℕ
#check @Filter.atTop ℕ _
-- Filter.atTop : Filter ℕ
-- END SOURCE ch06_008

-- BEGIN SOURCE ch06_009

theorem tail_mem_atTop : {n : ℕ | n ≥ 5} ∈ Filter.atTop := by
-- END SOURCE ch06_009

-- BEGIN SOURCE ch06_010
  apply Filter.mem_atTop_sets.mpr
-- END SOURCE ch06_010

-- BEGIN SOURCE ch06_011
  exact ⟨5, fun b hb => hb⟩
  -- No goals ✓
-- END SOURCE ch06_011

-- BEGIN SOURCE ch06_012

-- 数学：𝒩(a) = { U ⊆ X | ∃ 開集合 V, a ∈ V ⊆ U }
-- Lean：nhds a : Filter α
#check nhds
-- nhds : α → Filter α  （α は TopologicalSpace の型クラスを持つ型）

#check @nhds ℝ _
-- nhds : ℝ → Filter ℝ
-- END SOURCE ch06_012

-- BEGIN SOURCE ch06_013

-- 数学：U ∈ 𝒩(a) ↔ ∃ δ > 0, B(a, δ) ⊆ U
-- Lean：(nhds a).HasBasis (· > 0) (Metric.ball a ·)
#check Metric.nhds_basis_ball
-- Metric.nhds_basis_ball :
--   (nhds a).HasBasis (fun ε => 0 < ε) (Metric.ball a ·)
-- END SOURCE ch06_013

-- BEGIN SOURCE ch06_014

-- 具体例：開区間 (a-ε, a+ε) は nhds a に属する
-- 数学：B(a, ε) = (a-ε, a+ε) ∈ 𝒩(a)
-- Lean：
theorem open_interval_mem_nhds (a ε : ℝ) (hε : ε > 0) : Set.Ioo (a - ε) (a + ε) ∈ nhds a := by
  apply Ioo_mem_nhds <;> linarith
  -- No goals ✓

-- 近傍は開集合に限らない：閉区間 [-1, 1] も 0 の近傍
theorem closed_interval_mem_nhds : Set.Icc (-1 : ℝ) 1 ∈ nhds 0 :=
  Icc_mem_nhds (by norm_num) (by norm_num)
-- END SOURCE ch06_014

-- BEGIN SOURCE ch06_015

-- Mathlib.Order.Filter.Defs の定義を表示する
#print Filter.Tendsto
-- 本体は Filter.map f l₁ ≤ l₂
-- END SOURCE ch06_015

-- BEGIN SOURCE ch06_016

-- Filter.map の定義（概念的な確認）
-- def Filter.map (f : α → β) (l : Filter α) : Filter β where
--   sets := { V | f ⁻¹' V ∈ l }
--   -- f ⁻¹' V は Set.preimage f V の記法糖衣（Lean 4 ではこちらが標準）
--   -- 数学の記法 f⁻¹(V) と完全に対応する
--   -- （3条件の検証は l の性質から自動的に従う）
#check Filter.map
-- Filter.map : (α → β) → Filter α → Filter β
#check Set.preimage
-- Set.preimage : (α → β) → Set β → Set α
-- f ⁻¹' V  と  Set.preimage f V  は定義的に同じ
-- END SOURCE ch06_016

-- BEGIN SOURCE ch06_017

#check Filter.Tendsto
-- Filter.Tendsto : (α → β) → Filter α → Filter β → Prop

-- 逆像を取る集合ごとに書けば、包含の向きが明確になる
theorem continuousAt_iff_preimages (f : ℝ → ℝ) (a : ℝ) :
    ContinuousAt f a ↔ ∀ V ∈ nhds (f a), f ⁻¹' V ∈ nhds a :=
  Iff.rfl
-- END SOURCE ch06_017

-- BEGIN SOURCE ch06_018

-- 数学：Tendsto f (nhds a) (nhds b) ↔ ε-δ定義
-- Lean：Metric.tendsto_nhds_nhds
#check Metric.tendsto_nhds_nhds
-- Metric.tendsto_nhds_nhds :
--   Tendsto f (nhds a) (nhds b) ↔
--   ∀ ε > 0, ∃ δ > 0, ∀ ⦃x⦄, dist x a < δ → dist (f x) b < ε
-- END SOURCE ch06_018

-- BEGIN SOURCE ch06_019

theorem tendsto_to_epsilon_delta (f : ℝ → ℝ) (a b : ℝ)
    (h : Filter.Tendsto f (nhds a) (nhds b))
    (ε : ℝ) (hε : ε > 0) :
    ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - b| < ε := by
-- END SOURCE ch06_019

-- BEGIN SOURCE ch06_020
  rw [Metric.tendsto_nhds_nhds] at h
-- END SOURCE ch06_020

-- BEGIN SOURCE ch06_021
  obtain ⟨δ, hδ, hδε⟩ := h ε hε
-- END SOURCE ch06_021

-- BEGIN SOURCE ch06_022
  exact ⟨δ, hδ, fun x hx => by
    simpa [Real.dist_eq] using hδε (x := x) (by simpa [Real.dist_eq] using hx)⟩
  -- No goals ✓
-- END SOURCE ch06_022

-- BEGIN SOURCE ch06_024

theorem continuous_to_tendsto_steps (f : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a) :
    Filter.Tendsto f (nhds a) (nhds (f a)) := by
-- END SOURCE ch06_024

-- BEGIN SOURCE ch06_025
  exact hf
  -- No goals ✓
-- END SOURCE ch06_025

-- BEGIN SOURCE ch06_026

#print ContinuousAt
-- def ContinuousAt (f : α → β) (x : α) : Prop :=
--   Filter.Tendsto f (nhds x) (nhds (f x))
-- END SOURCE ch06_026

-- BEGIN SOURCE ch06_027

-- 定義的同値の確認：rfl で通る
theorem continuousAt_def_eq (f : ℝ → ℝ) (a : ℝ) :
    ContinuousAt f a = Filter.Tendsto f (nhds a) (nhds (f a)) := by
  rfl  -- rfl で通る ＝ 定義を開けば同じ式になる
-- END SOURCE ch06_027

-- BEGIN SOURCE ch06_028

#check Metric.tendsto_atTop
-- Metric.tendsto_atTop :
--   Tendsto f atTop (nhds b) ↔
--   ∀ ε > 0, ∃ N, ∀ n, N ≤ n → dist (f n) b < ε
-- END SOURCE ch06_028

-- BEGIN SOURCE ch06_029

theorem sequence_epsilon_N (a : ℕ → ℝ) (L : ℝ)
    (h : Filter.Tendsto a Filter.atTop (nhds L)) :
    ∀ ε > 0, ∃ N : ℕ, ∀ n ≥ N, |a n - L| < ε := by
-- END SOURCE ch06_029

-- BEGIN SOURCE ch06_030
  rw [Metric.tendsto_atTop] at h
-- END SOURCE ch06_030

-- BEGIN SOURCE ch06_031
  intro ε hε
  obtain ⟨N, hN⟩ := h ε hε
-- END SOURCE ch06_031

-- BEGIN SOURCE ch06_032
  exact ⟨N, fun n hn => by simpa [Real.dist_eq] using hN n hn⟩
  -- No goals ✓
-- END SOURCE ch06_032

-- BEGIN SOURCE ch06_033

theorem square_tendsto_atTop : Filter.Tendsto (fun x : ℝ => x ^ 2) Filter.atTop Filter.atTop := by
-- END SOURCE ch06_033

-- BEGIN SOURCE ch06_034
  exact Filter.tendsto_pow_atTop (by norm_num)
  -- Filter.tendsto_pow_atTop は指数 n ≠ 0 の証明を要求する
  -- ここでは (2 : ℕ) ≠ 0 を norm_num で示す
  -- No goals ✓
-- END SOURCE ch06_034

-- BEGIN SOURCE ch06_035

-- 数学：定数関数 f(x) = b はすべての点で連続
-- Lean：
theorem constant_continuousAt (b : ℝ) (a : ℝ) : ContinuousAt (fun _ : ℝ => b) a :=
  continuousAt_const  -- No goals ✓
-- END SOURCE ch06_035

-- BEGIN SOURCE ch06_036

theorem product_continuousAt (f g : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a) (hg : ContinuousAt g a) :
    ContinuousAt (fun x => f x * g x) a := by
-- END SOURCE ch06_036

-- BEGIN SOURCE ch06_037
  exact hf.mul hg
  -- No goals ✓
-- END SOURCE ch06_037

-- BEGIN SOURCE ch06_038

theorem composition_continuousAt (f g : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a)
    (hg : ContinuousAt g (f a)) :
    ContinuousAt (g ∘ f) a := by
-- END SOURCE ch06_038

-- BEGIN SOURCE ch06_039
  exact hg.comp hf
  -- No goals ✓
-- END SOURCE ch06_039

-- BEGIN SOURCE ch06_040

-- 形①：ContinuousAt を仮定として受け取る（最もシンプル）
-- 数学：「f が a で連続」ならば「f は a で連続」（同語反復に見えるが……）
theorem continuous_implies_tendsto
    (f : ℝ → ℝ) (a : ℝ) (hf : ContinuousAt f a) :
    Filter.Tendsto f (nhds a) (nhds (f a)) :=
  hf  -- 定義的同値なので証明項は hf そのまま

-- 形②：Continuous（全域連続）から点連続性を取り出す
-- 数学：f が（全域）連続 ⟹ f は a で連続
theorem tendsto_of_continuous
    (f : ℝ → ℝ) (hf : Continuous f) (a : ℝ) :
    Filter.Tendsto f (nhds a) (nhds (f a)) :=
  hf.continuousAt  -- Continuous → ContinuousAt への変換

-- 形③：双方向の同値（これが本章の核心）
-- 数学：Tendsto f (nhds a) (nhds (f a)) ⟺ f は a で連続
-- 定義が同じなので、同値の証明は Iff.rfl で構成できる
theorem tendsto_iff_continuousAt (f : ℝ → ℝ) (a : ℝ) :
    Filter.Tendsto f (nhds a) (nhds (f a)) ↔ ContinuousAt f a :=
  Iff.rfl  -- Iff.rfl で通る ＝ 定義が同じ
-- END SOURCE ch06_040

-- BEGIN SOURCE ch06_041

#check Metric.tendsto_atTop
-- Tendsto f atTop (nhds b) ↔ ∀ ε > 0, ∃ N, ∀ n ≥ N, dist (f n) b < ε
-- END SOURCE ch06_041

-- BEGIN SOURCE ch06_043

-- f が a で連続かつ g が f(a) で連続なら、合成 g ∘ f も a で連続
theorem composition_answer (f g : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a)
    (hg : ContinuousAt g (f a)) :
    ContinuousAt (g ∘ f) a := by
  exact hg.comp hf
  -- No goals ✓
-- END SOURCE ch06_043

-- BEGIN SOURCE ch06_044

theorem composition_answer_apply (f g : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a)
    (hg : ContinuousAt g (f a)) :
    ContinuousAt (g ∘ f) a := by
  apply ContinuousAt.comp hg hf
  -- No goals ✓
-- END SOURCE ch06_044

-- BEGIN SOURCE ch06_045

open scoped Topology

-- #check は命題の型を確認する。命題の証明ではない。
-- (a) lim_{n→∞} 1/n = 0（Lean では 1 / 0 = 0。有限個の初項は極限に影響しない）
#check Filter.Tendsto (fun n : ℕ => (1 : ℝ) / n) Filter.atTop (nhds 0)

-- (b) 0 を除いて両側から近づく極限
#check Filter.Tendsto (fun x : ℝ => x ^ 2) (𝓝[≠] (0 : ℝ)) (nhds 0)
-- x² は 0 で連続なので、0 を除かない次の強い命題も成り立つ
#check Filter.Tendsto (fun x : ℝ => x ^ 2) (nhds 0) (nhds 0)

-- (c) f の宣言を含めて実行する
section
variable (f : ℝ → ℝ)
#check ∀ a : ℝ, Filter.Tendsto f (nhds a) (nhds (f a))
#check Continuous f
-- Continuous f は連続性を表す命題で、型クラスではない
end
-- END SOURCE ch06_045

-- BEGIN SOURCE ch06_046

open scoped Topology

-- 𝓝[≠] a は nhdsWithin a {a}ᶜ の記法
#check (𝓝[≠] (0 : ℝ))
#check nhdsWithin (0 : ℝ) (Set.Ioi 0)  -- 右側、0 を除く
#check nhdsWithin (0 : ℝ) (Set.Iio 0)  -- 左側、0 を除く

noncomputable def spike (x : ℝ) : ℝ := if x = 0 then 1 else 0

theorem spike_punctured : Filter.Tendsto spike (𝓝[≠] (0 : ℝ)) (𝓝 0) := by
  apply (tendsto_const_nhds : Filter.Tendsto (fun _ : ℝ => (0 : ℝ)) _ _).congr'
  filter_upwards [eventually_mem_nhdsWithin] with x hx
  have hx0 : x ≠ 0 := by simpa using hx
  simp [spike, hx0]

theorem spike_not_continuous : ¬ ContinuousAt spike 0 := by
  intro h
  have hlim : Filter.Tendsto spike (𝓝[≠] (0 : ℝ)) (𝓝 (spike 0)) :=
    h.continuousWithinAt
  have heq := tendsto_nhds_unique spike_punctured hlim
  norm_num [spike] at heq
-- END SOURCE ch06_046

-- BEGIN SOURCE ch06_047

-- sin が任意の点 a で連続
theorem sine_continuousAt (a : ℝ) : ContinuousAt Real.sin a :=
  Real.continuous_sin.continuousAt
  -- No goals ✓
-- END SOURCE ch06_047

-- BEGIN SOURCE ch06_048

theorem sine_continuousAt_explicit (a : ℝ) : ContinuousAt Real.sin a := by
  exact Continuous.continuousAt Real.continuous_sin
  -- No goals ✓
-- END SOURCE ch06_048

end LeanBook.Ch06
