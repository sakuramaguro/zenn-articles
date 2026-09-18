import Mathlib

namespace LeanBook.Ch13

-- BEGIN SOURCE ch13_001
open MeasureTheory

-- 一般の a,b では ENNReal.ofReal (b-a)。a ≤ b なら区間の長さに対応する。
#check @Real.volume_Icc
#check @Real.volume_Ioo
#check @Real.volume_singleton

theorem volume_unit_interval : volume (Set.Icc (0 : ℝ) 1) = 1 := by
  simp [Real.volume_Icc]

#check @IsProbabilityMeasure
#check @prob_le_one

theorem dirac_is_probability : IsProbabilityMeasure (Measure.dirac (0 : ℝ)) :=
  inferInstance
-- END SOURCE ch13_001

-- BEGIN SOURCE ch13_002
open MeasureTheory

#check @Measure
#print Measure
#check @Measure.trimmed
#check @measure_eq_iInf
-- END SOURCE ch13_002

-- BEGIN SOURCE ch13_003
open MeasureTheory

#check @Measure.toOuterMeasure
#check @measure_empty
#check @measure_iUnion
#check @measure_mono
#check @measure_union_le

theorem countable_additivity_demo {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (f : ℕ → Set α)
    (hd : Pairwise (fun i j => Disjoint (f i) (f j)))
    (hm : ∀ i, MeasurableSet (f i)) :
    μ (⋃ i, f i) = ∑' i, μ (f i) :=
  measure_iUnion hd hm
-- END SOURCE ch13_003

-- BEGIN SOURCE ch13_004
open MeasureTheory

-- Lebesgue 測度 volume : Measure ℝ
#check (volume : Measure ℝ)
-- volume : MeasureTheory.Measure ℝ
-- END SOURCE ch13_004

-- BEGIN SOURCE ch13_005
open MeasureTheory

-- 目標：volume (Set.Icc (0 : ℝ) 3) = 3
theorem volume_zero_three : volume (Set.Icc (0 : ℝ) 3) = 3 := by
  rw [Real.volume_Icc]    -- ステップ②
  norm_num                 -- ステップ③
-- No goals ✓
-- END SOURCE ch13_005

-- BEGIN SOURCE ch13_006
open MeasureTheory

-- 開区間でも端点の差（端点の差は変わらない）
theorem volume_open_unit_interval : volume (Set.Ioo (0 : ℝ) 1) = 1 := by
  simp [Real.volume_Ioo]
  -- No goals ✓

-- 一点集合の測度は 0（有理数・無理数にかかわらず）
-- 数学：λ({a}) = 0 / Lean：Real.volume_singleton
theorem volume_singleton_zero (a : ℝ) : volume ({a} : Set ℝ) = 0 := Real.volume_singleton
-- No goals ✓
-- END SOURCE ch13_006

-- BEGIN SOURCE ch13_007
open MeasureTheory

-- 数え上げ測度 Measure.count
#check @Measure.count
-- Measure.count : Measure α

-- 単集合の数え上げ：一点集合の数は 1
-- 数学：#({a}) = 1 / Lean：Measure.count_singleton
theorem count_singleton_one : Measure.count ({5} : Set ℕ) = 1 := Measure.count_singleton 5
-- No goals ✓

-- 空集合の数え上げ：0 個
theorem count_empty_zero : Measure.count (∅ : Set ℕ) = 0 := by simp
-- No goals ✓
-- END SOURCE ch13_007

-- BEGIN SOURCE ch13_008
open MeasureTheory

-- Dirac 測度 δ_a：点 a に全重量を集中させる
-- 数学：δ_a(A) = 1 if a ∈ A, 0 if a ∉ A / Lean：Measure.dirac
#check @Measure.dirac
-- Measure.dirac : α → Measure α

-- δ₀({0}) = 1（0 は {0} に属する）
theorem dirac_at_zero : Measure.dirac (0 : ℝ) {0} = 1 := by
  simp [Measure.dirac_apply']
  -- No goals ✓

-- δ₀({1}) = 0（0 は {1} に属さない）
theorem dirac_away_from_zero : Measure.dirac (0 : ℝ) {1} = 0 := by
  simp [Measure.dirac_apply']
  -- No goals ✓
-- END SOURCE ch13_008

-- BEGIN SOURCE ch13_009
open MeasureTheory

-- IsProbabilityMeasure の定義
#print IsProbabilityMeasure
-- class IsProbabilityMeasure (μ : Measure α) : Prop where
--   measure_univ : μ Set.univ = 1

-- Dirac測度は確率測度（自動的にインスタンスが解決される）
theorem dirac_probability_demo : IsProbabilityMeasure (Measure.dirac (0 : ℝ)) := inferInstance

-- 確率測度では任意の集合の測度は [0,1] に収まる
theorem probability_bound (μ : Measure ℝ) [IsProbabilityMeasure μ] (s : Set ℝ) :
    μ s ≤ 1 := prob_le_one
-- END SOURCE ch13_009

-- BEGIN SOURCE ch13_010
open MeasureTheory
section Example10

variable (Ω : Type*) [MeasurableSpace Ω]
         (P : Measure Ω) [IsProbabilityMeasure P]

end Example10
-- END SOURCE ch13_010

-- BEGIN SOURCE ch13_011
open MeasureTheory
theorem volume_one_four : volume (Set.Icc (1 : ℝ) 4) = 3 := by
  rw [Real.volume_Icc]
  norm_num
  -- No goals ✓
-- END SOURCE ch13_011

-- BEGIN SOURCE ch13_012
open MeasureTheory
theorem volume_one_four_alt : volume (Set.Icc (1 : ℝ) 4) = 3 := by
  simp [Real.volume_Icc, show (4:ℝ) - 1 = 3 from by norm_num]
-- END SOURCE ch13_012

-- BEGIN SOURCE ch13_014
open MeasureTheory
theorem interval_measure_mono : volume (Set.Icc (0 : ℝ) 1) ≤ volume (Set.Icc (0 : ℝ) 2) := by
  apply measure_mono
  exact Set.Icc_subset_Icc le_rfl (by norm_num)
  -- No goals ✓
-- END SOURCE ch13_014

-- BEGIN SOURCE ch13_015
open MeasureTheory
theorem interval_measure_mono_alt : volume (Set.Icc (0 : ℝ) 1) ≤ volume (Set.Icc (0 : ℝ) 2) := by
  apply measure_mono
  intro x ⟨hx0, hx1⟩
  exact ⟨hx0, by linarith⟩
-- END SOURCE ch13_015

-- BEGIN SOURCE ch13_016
open MeasureTheory
theorem restricted_volume_probability : IsProbabilityMeasure (volume.restrict (Set.Icc (0:ℝ) 1)) := by
  constructor
  rw [Measure.restrict_apply MeasurableSet.univ, Set.univ_inter]
  rw [Real.volume_Icc]
  norm_num
  -- No goals ✓
-- END SOURCE ch13_016

-- BEGIN SOURCE ch13_017
open MeasureTheory

theorem restricted_volume_probability_alt :
    IsProbabilityMeasure (volume.restrict (Set.Icc (0 : ℝ) 1)) := by
  refine ⟨?_⟩
  simp [Real.volume_Icc]
-- END SOURCE ch13_017

end LeanBook.Ch13
