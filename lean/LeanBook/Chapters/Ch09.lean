import Mathlib

namespace LeanBook.Ch09

-- BEGIN SOURCE ch09_001

open Filter Topology

theorem complete_sequence_goal (X : Type*) [MetricSpace X] [CompleteSpace X]
    (a : ℕ → X) (ha : CauchySeq a) :
    ∃ L : X, Tendsto a atTop (nhds L) := cauchySeq_tendsto_of_complete ha

theorem real_sequence_goal (a : ℕ → ℝ) (ha : CauchySeq a) :
    ∃ L : ℝ, Tendsto a atTop (nhds L) := cauchySeq_tendsto_of_complete ha
-- END SOURCE ch09_001

-- BEGIN SOURCE ch09_002

open Filter Topology

#check (inferInstance : MetricSpace ℚ)
#check Rat.isDenseEmbedding_coe_real
#check irrational_sqrt_two
-- ここでは距離構造・ℝへの稠密な埋め込み・√2の無理性を確認する。
-- インスタンス探索の失敗だけでは ¬ CompleteSpace ℚ の証明にはならない。
-- END SOURCE ch09_002

-- BEGIN SOURCE ch09_003

open Filter Topology

#check (inferInstance : CompleteSpace ℝ)
-- END SOURCE ch09_003

-- BEGIN SOURCE ch09_004

open Filter Topology

#print CauchySeq
#check @Metric.cauchySeq_iff
-- 本章では添字をℕとする。定義自体は前順序を持つ添字型にも使える。
-- CauchySeq u は Cauchy (Filter.map u Filter.atTop) と定義される。
-- END SOURCE ch09_004

-- BEGIN SOURCE ch09_005

open Filter Topology

theorem cauchy_epsilon_tail (a : ℕ → ℝ) (ha : CauchySeq a) (ε : ℝ) (hε : 0 < ε) :
    ∃ N, ∀ m ≥ N, ∀ n ≥ N, dist (a m) (a n) < ε := by
-- END SOURCE ch09_005

-- BEGIN SOURCE ch09_006
  exact Metric.cauchySeq_iff.mp ha ε hε
-- END SOURCE ch09_006

-- BEGIN SOURCE ch09_007

open Filter Topology

open scoped Uniformity

#print Cauchy
#check @Metric.cauchy_iff

theorem cauchy_filter_definition (f : Filter ℝ) :
    Cauchy f ↔ f.NeBot ∧ f ×ˢ f ≤ uniformity ℝ := Iff.rfl
-- END SOURCE ch09_007

-- BEGIN SOURCE ch09_008

open Filter Topology

theorem cauchy_sequence_definition (a : ℕ → ℝ) :
    CauchySeq a ↔ Cauchy (Filter.map a Filter.atTop) := by
  rfl
-- END SOURCE ch09_008

-- BEGIN SOURCE ch09_009

open Filter Topology

#print CompleteSpace
#check @CompleteSpace.complete
-- [UniformSpace α] の下で、すべてのCauchyフィルターが収束するという条件。
-- END SOURCE ch09_009

-- BEGIN SOURCE ch09_010

open Filter Topology

#check (inferInstance : CompleteSpace ℝ)
#check (inferInstance : CompleteSpace ℂ)
-- 実・複素ノルム空間に完備性が加わるとBanach空間になる。
-- END SOURCE ch09_010

-- BEGIN SOURCE ch09_011

open Filter Topology

#check @cauchySeq_tendsto_of_complete
-- END SOURCE ch09_011

-- BEGIN SOURCE ch09_012

open Filter Topology

theorem complete_sequence_limit (X : Type*) [MetricSpace X] [CompleteSpace X]
    (a : ℕ → X) (ha : CauchySeq a) :
    ∃ L : X, Tendsto a atTop (nhds L) := by
-- END SOURCE ch09_012

-- BEGIN SOURCE ch09_013
  exact cauchySeq_tendsto_of_complete ha
-- END SOURCE ch09_013

-- BEGIN SOURCE ch09_014

open Filter Topology

theorem geometric_cauchy : CauchySeq (fun n : ℕ => (1 / 2 : ℝ) ^ n) := by
-- END SOURCE ch09_014

-- BEGIN SOURCE ch09_015
  apply Metric.cauchySeq_iff.mpr
-- END SOURCE ch09_015

-- BEGIN SOURCE ch09_016
  intro ε hε
  -- まず ε/2 > 0 を確保する
  have h_half : 0 < ε / 2 := half_pos hε
  -- (1/2)^N < ε/2 を満たす N を取る（ε ではなく ε/2 で取るのがポイント）
  obtain ⟨N, hN⟩ := exists_pow_lt_of_lt_one h_half (by norm_num : (1 : ℝ)/2 < 1)
-- END SOURCE ch09_016

-- BEGIN SOURCE ch09_017
  refine ⟨N, fun m hm n hn => ?_⟩
  calc dist ((1 / 2 : ℝ) ^ m) ((1 / 2) ^ n)
      = |(1 / 2 : ℝ) ^ m - (1 / 2) ^ n| := Real.dist_eq _ _
    _ ≤ (1 / 2 : ℝ) ^ m + (1 / 2) ^ n := by
      apply abs_sub_le_iff.mpr
      constructor <;> linarith [pow_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) m,
        pow_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) n]
    _ ≤ (1 / 2 : ℝ) ^ N + (1 / 2) ^ N :=
      add_le_add (pow_le_pow_of_le_one (by norm_num) (by norm_num) hm)
        (pow_le_pow_of_le_one (by norm_num) (by norm_num) hn)
    _ < ε / 2 + ε / 2 := add_lt_add hN hN
    _ = ε := by ring

-- 上のCauchy性にℝの完備性を組み合わせると、極限の存在が得られる。
theorem geometric_has_limit :
    ∃ L : ℝ, Tendsto (fun n : ℕ => (1 / 2 : ℝ) ^ n) atTop (nhds L) :=
  cauchySeq_tendsto_of_complete geometric_cauchy
-- END SOURCE ch09_017

-- BEGIN SOURCE ch09_018

open Filter Topology

#check UniformSpace.Completion
#check Rat.uniformContinuous_coe_real
#check UniformSpace.Completion.extension
#check UniformSpace.Completion.extension_coe
#check UniformSpace.Completion.extension_unique
#check CompareReals.compareEquiv

-- 距離空間の完備化から、完備距離空間への一意な一様連続拡張。
theorem completion_extension_unique (X Y : Type*) [MetricSpace X] [MetricSpace Y]
    [CompleteSpace Y] (f : X → Y) (hf : UniformContinuous f) :
    ∃! g : UniformSpace.Completion X → Y,
      UniformContinuous g ∧ ∀ x : X, g (x : UniformSpace.Completion X) = f x := by
  refine ⟨UniformSpace.Completion.extension f, ⟨?_, ?_⟩, ?_⟩
  · exact UniformSpace.Completion.uniformContinuous_extension
  · exact UniformSpace.Completion.extension_coe hf
  · intro g hg
    exact (UniformSpace.Completion.extension_unique hf hg.1
      (fun x => (hg.2 x).symm)).symm
-- END SOURCE ch09_018

-- BEGIN SOURCE ch09_019

open Filter Topology

#check (inferInstance : MetricSpace ℝ)
#check (inferInstance : CompleteSpace ℝ)
#check (inferInstance : TopologicalSpace ℝ)
#check (inferInstance : NormedSpace ℝ (lp (fun _ : ℕ => ℝ) 2))
-- 次章では、lpに登録された構造の数学的内容を詳しく調べる。
-- END SOURCE ch09_019

-- BEGIN SOURCE ch09_020

open Filter Topology

theorem reciprocal_cauchy : CauchySeq (fun n : ℕ => (1 : ℝ) / n) := by
  have h : Tendsto (fun n : ℕ => (1 : ℝ) / n) atTop (nhds 0) :=
    tendsto_const_nhds.div_atTop tendsto_natCast_atTop_atTop
  exact h.cauchySeq
-- END SOURCE ch09_020

-- BEGIN SOURCE ch09_022

open Filter Topology

theorem constant_cauchy (x : ℝ) : CauchySeq (fun _ : ℕ => x) := by
  exact cauchySeq_const x
-- END SOURCE ch09_022

-- BEGIN SOURCE ch09_023

open Filter Topology

theorem constant_cauchy_from_limit (x : ℝ) : CauchySeq (fun _ : ℕ => x) := by
  have h : Tendsto (fun _ : ℕ => x) atTop (nhds x) := tendsto_const_nhds
  exact h.cauchySeq
-- END SOURCE ch09_023

-- BEGIN SOURCE ch09_024

open Filter Topology

section
variable (a : ℕ → ℝ) (ℱ : Filter ℝ) (X : Type*) [MetricSpace X]
#check (CauchySeq a : Prop)
#check (Cauchy ℱ : Prop)
#check (CompleteSpace X : Prop)
end
-- END SOURCE ch09_024

-- BEGIN SOURCE ch09_025

open Filter Topology

#check @cauchySeq_iff_le_tendsto_0
-- 非負の上界列 b N → 0 が存在し、N ≤ m,n なら dist (u m) (u n) ≤ b N。
#check @Metric.cauchySeq_iff
-- END SOURCE ch09_025

-- BEGIN SOURCE ch09_027

open Filter Topology

theorem convergent_cauchy (X : Type*) [MetricSpace X]
    (a : ℕ → X) (L : X) (ha : Tendsto a atTop (nhds L)) : CauchySeq a := by
  exact ha.cauchySeq
-- END SOURCE ch09_027

-- BEGIN SOURCE ch09_028

open Filter Topology

theorem convergent_cauchy_by_filter (X : Type*) [MetricSpace X]
    (a : ℕ → X) (L : X) (ha : Tendsto a atTop (nhds L)) : CauchySeq a := by
  change Cauchy (Filter.map a atTop)
  exact cauchy_nhds.mono ha
-- END SOURCE ch09_028

end LeanBook.Ch09
