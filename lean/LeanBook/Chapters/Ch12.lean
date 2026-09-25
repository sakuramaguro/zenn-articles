import Mathlib

namespace LeanBook.Ch12

-- BEGIN SOURCE ch12_001
open scoped NNReal

-- 非空な完備距離空間 ℝ 上で、縮小性から一意存在を得る
theorem half_map_recap : ∃! z : ℝ, (fun x : ℝ => x / 2) z = z := by
  have hf : ContractingWith (1 / 2 : ℝ≥0) (fun x : ℝ => x / 2) := by
    refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
    simp only [Real.dist_eq]
    rw [← sub_div, abs_div]
    norm_num
    ring_nf
    exact le_rfl
  refine ⟨hf.fixedPoint (fun x : ℝ => x / 2), hf.fixedPoint_isFixedPt, ?_⟩
  intro y hy
  exact hf.fixedPoint_unique hy
-- END SOURCE ch12_001

-- BEGIN SOURCE ch12_002
open MeasureTheory Filter
open scoped ENNReal Topology

-- Part 3の到達点：既存の収束定理を、仮定を確認して適用する。
#check @lintegral_iSup
-- 非負可測関数列 + 各点で単調増加 → 上限と非負積分の交換。
#check @lintegral_liminf_le
#check @lintegral_liminf_le'
-- Measurable 版と AEMeasurable 版。結論は等号ではなく不等式。
#check @tendsto_integral_of_dominated_convergence
-- 実数値の例では、各項のAE 強可測性、可積分な優関数、
-- ノルムのAE 支配、AE 収束を揃えると、積分列の収束が得られる。
-- 引数の順：bound hFm hbound hle htends。
-- END SOURCE ch12_002

-- BEGIN SOURCE ch12_003
open MeasureTheory

-- 確率空間の Lean での表現
-- 数学：(Ω, ℱ, P) が確率空間
section Example3

variable (Ω : Type*) [MeasurableSpace Ω]          -- 数学：可測空間 (Ω, ℱ)
         (P : Measure Ω) [IsProbabilityMeasure P]  -- 数学：確率測度 P（P(Ω)=1）

-- 確率変数 X : Ω → ℝ の正体は「可測関数」
variable (X : Ω → ℝ) (hX : Measurable X) (hXi : Integrable X P)

-- 期待値 E[X] の正体は「Lebesgue 積分」
#check ∫ ω, X ω ∂P   -- ℝ

end Example3
-- END SOURCE ch12_003

-- BEGIN SOURCE ch12_004

theorem univ_measurable : MeasurableSet (Set.univ : Set ℝ) := MeasurableSet.univ

theorem compl_measurable (s : Set ℝ) (hs : MeasurableSet s) :
    MeasurableSet sᶜ := hs.compl

theorem countable_union_measurable (f : ℕ → Set ℝ)
    (hf : ∀ n, MeasurableSet (f n)) : MeasurableSet (⋃ n, f n) :=
  MeasurableSet.iUnion hf

-- 以下は型とインスタンスの確認。borel の定義は12.4節で確認する。
#check @MeasurableSpace.generateFrom
#check @borel
#check (inferInstance : BorelSpace ℝ)
#check (inferInstance : OpensMeasurableSpace ℝ)

theorem open_measurable (U : Set ℝ) (hU : IsOpen U) : MeasurableSet U :=
  hU.measurableSet
-- END SOURCE ch12_004

-- BEGIN SOURCE ch12_005

#print MeasurableSpace

-- 冪集合のσ-代数にも測度を定義できることの確認
section Powerset
local instance : MeasurableSpace ℝ := ⊤

theorem all_sets_measurable (s : Set ℝ) : MeasurableSet s :=
  MeasurableSpace.measurableSet_top

theorem zero_measure_on_powerset (s : Set ℝ) :
    (0 : MeasureTheory.Measure ℝ) s = 0 := by
  simp

end Powerset
-- END SOURCE ch12_005

-- BEGIN SOURCE ch12_006

section Example6

variable {α : Type*} [MeasurableSpace α]

-- 数学：∅ は可測 / Lean：MeasurableSet.empty
theorem empty_measurable : MeasurableSet (∅ : Set α) := MeasurableSet.empty

-- 数学：A, B が可測なら A ∩ B も可測 / Lean：MeasurableSet.inter
theorem inter_measurable (s t : Set α) (hs : MeasurableSet s) (ht : MeasurableSet t) :
    MeasurableSet (s ∩ t) := hs.inter ht

-- 数学：2つの集合の合併 / Lean：MeasurableSet.union
theorem union_measurable (s t : Set α) (hs : MeasurableSet s) (ht : MeasurableSet t) :
    MeasurableSet (s ∪ t) := hs.union ht

end Example6
-- END SOURCE ch12_006

-- BEGIN SOURCE ch12_007

#check @MeasurableSpace.generateFrom
#check @MeasurableSpace.generateFrom_le

theorem borel_definition_demo (α : Type*) [TopologicalSpace α] :
    borel α = MeasurableSpace.generateFrom {s | IsOpen s} := rfl
-- END SOURCE ch12_007

-- BEGIN SOURCE ch12_008
-- borel の定義を覗く
#print borel
-- END SOURCE ch12_008

-- BEGIN SOURCE ch12_009
-- borel の型を確認する
#check @borel
-- borel : (α : Type u_1) → [TopologicalSpace α] → MeasurableSpace α
-- END SOURCE ch12_009

-- BEGIN SOURCE ch12_010

#check @BorelSpace
#check @OpensMeasurableSpace
#check @IsOpen.measurableSet
#check (inferInstance : BorelSpace ℝ)
#check (inferInstance : OpensMeasurableSpace ℝ)
-- END SOURCE ch12_010

-- BEGIN SOURCE ch12_011

-- 目標：MeasurableSet (Set.Ioo (0 : ℝ) 1)
theorem open_interval_measurable : MeasurableSet (Set.Ioo (0 : ℝ) 1) := by
  apply IsOpen.measurableSet  -- ステップ②
  exact isOpen_Ioo             -- ステップ③
-- No goals ✓
-- END SOURCE ch12_011

-- BEGIN SOURCE ch12_012
-- 閉区間 [0, 1] も可測（IsClosed.measurableSet の恩恵）
theorem closed_interval_measurable : MeasurableSet (Set.Icc (0 : ℝ) 1) := measurableSet_Icc

-- 左開右閉区間 (0, 1] も可測（開集合 (0,∞) と閉集合 (-∞,1] の交わりとして表せる）
theorem half_open_interval_measurable : MeasurableSet (Set.Ioc (0 : ℝ) 1) := measurableSet_Ioc
-- END SOURCE ch12_012

-- BEGIN SOURCE ch12_014
section Example14

variable {α : Type*} [MeasurableSpace α]
theorem countable_inter_measurable (f : ℕ → Set α) (hf : ∀ n, MeasurableSet (f n)) :
    MeasurableSet (⋂ n, f n) := by
  exact MeasurableSet.iInter hf
  -- No goals ✓

end Example14
-- END SOURCE ch12_014

-- BEGIN SOURCE ch12_015

theorem countable_inter_measurable_alt {α : Type*} [MeasurableSpace α]
    (f : ℕ → Set α) (hf : ∀ n, MeasurableSet (f n)) :
    MeasurableSet (⋂ n, f n) := by
  apply MeasurableSet.iInter
  intro n
  exact hf n
-- END SOURCE ch12_015

-- BEGIN SOURCE ch12_016

#print borel

theorem rationals_measurable : MeasurableSet (Set.range ((↑) : ℚ → ℝ)) := by
  exact (Set.countable_range ((↑) : ℚ → ℝ)).measurableSet
-- END SOURCE ch12_016

-- BEGIN SOURCE ch12_017

theorem rationals_measurable_alt : MeasurableSet (Set.range ((↑) : ℚ → ℝ)) := by
  rw [← Set.iUnion_singleton_eq_range]
  apply MeasurableSet.iUnion
  intro q
  exact measurableSet_singleton (q : ℝ)
-- END SOURCE ch12_017

-- BEGIN SOURCE ch12_018

-- 空集合は構造体のフィールド。全体集合はそこから導かれる。
#print MeasurableSet.empty
#print MeasurableSet.univ

theorem empty_measurable_from_field {α : Type*} [MeasurableSpace α] :
    MeasurableSet (∅ : Set α) := MeasurableSet.empty
-- END SOURCE ch12_018

-- BEGIN SOURCE ch12_019
section Example19

variable {α : Type*} [MeasurableSpace α]
theorem empty_measurable_from_univ : MeasurableSet (∅ : Set α) := by
  have h : MeasurableSet (Set.univ : Set α) := MeasurableSet.univ
  have hc := h.compl
  rw [Set.compl_univ] at hc
  exact hc

end Example19
-- END SOURCE ch12_019

end LeanBook.Ch12
