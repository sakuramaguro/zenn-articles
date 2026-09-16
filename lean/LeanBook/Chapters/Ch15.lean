import Mathlib

namespace LeanBook.Ch15

-- BEGIN SOURCE ch15_001
open MeasureTheory
open scoped ENNReal

#check @SimpleFunc.lintegral
#check @SimpleFunc.const
#check @SimpleFunc.const_lintegral

-- 定数3を、[0,1]に制限したLebesgue測度で積分する。
theorem simple_const_unit_integral :
    (SimpleFunc.const ℝ (3 : ℝ≥0∞)).lintegral (volume.restrict (Set.Icc 0 1)) = 3 := by
  rw [SimpleFunc.const_lintegral]
  norm_num [Measure.restrict_apply_univ, Real.volume_Icc]
-- END SOURCE ch15_001

-- BEGIN SOURCE ch15_002
open MeasureTheory
open scoped ENNReal

#print SimpleFunc
#check @SimpleFunc.measurableSet_fiber
#check @SimpleFunc.finite_range
#check @SimpleFunc.measurable
-- END SOURCE ch15_002

-- BEGIN SOURCE ch15_003
open MeasureTheory
open scoped ENNReal

noncomputable def myConst : SimpleFunc ℝ ℝ≥0∞ := SimpleFunc.const ℝ 2

-- #evalではなく、等式として関数値を確認する。
theorem myConst_at_zero : myConst 0 = 2 := rfl

#check @SimpleFunc.piecewise
#check @SimpleFunc.restrict
#check @SimpleFunc.coe_restrict
-- END SOURCE ch15_003

-- BEGIN SOURCE ch15_004
open MeasureTheory
open scoped ENNReal

#check @SimpleFunc.lintegral
#check @SimpleFunc.const_lintegral

theorem simple_lintegral_definition {α : Type*} [MeasurableSpace α]
    (φ : SimpleFunc α ℝ≥0∞) (μ : Measure α) :
    φ.lintegral μ = ∑ c ∈ φ.range, c * μ (φ ⁻¹' {c}) := rfl
-- END SOURCE ch15_004

-- BEGIN SOURCE ch15_005
open MeasureTheory
open scoped ENNReal

theorem simple_const_unit_integral_steps :
    (SimpleFunc.const ℝ (3 : ℝ≥0∞)).lintegral (volume.restrict (Set.Icc 0 1)) = 3 := by
  rw [SimpleFunc.const_lintegral]
  rw [Measure.restrict_apply_univ]
  rw [Real.volume_Icc]
  norm_num
-- END SOURCE ch15_005

-- BEGIN SOURCE ch15_006
open MeasureTheory
open scoped ENNReal

#print SimpleFunc.eapprox
#check @SimpleFunc.approx_apply
#check @SimpleFunc.monotone_eapprox
#check @SimpleFunc.iSup_eapprox_apply
#check @lintegral_eq_iSup_eapprox_lintegral

theorem eapprox_sup_eq {α : Type*} [MeasurableSpace α]
    (f : α → ℝ≥0∞) (hf : Measurable f) (x : α) :
    (⨆ n, SimpleFunc.eapprox f n x) = f x :=
  SimpleFunc.iSup_eapprox_apply hf x

-- 可測なfについての等式。lintegral自体の定義とは区別する。
theorem lintegral_eapprox_formula {α : Type*} [MeasurableSpace α]
    (f : α → ℝ≥0∞) (hf : Measurable f) (μ : Measure α) :
    (∫⁻ x, f x ∂μ) = ⨆ n, (SimpleFunc.eapprox f n).lintegral μ :=
  lintegral_eq_iSup_eapprox_lintegral hf
-- END SOURCE ch15_006

-- BEGIN SOURCE ch15_007
open MeasureTheory
open scoped ENNReal

#check @SimpleFunc.finite_range
#check (SimpleFunc.const ℝ (3 : ℝ≥0∞)).finite_range

theorem const_three_finite_range :
    (Set.range (SimpleFunc.const ℝ (3 : ℝ≥0∞) : ℝ → ℝ≥0∞)).Finite :=
  (SimpleFunc.const ℝ (3 : ℝ≥0∞)).finite_range
-- END SOURCE ch15_007

-- BEGIN SOURCE ch15_008
open MeasureTheory
open scoped ENNReal

-- 値域が一点集合になるには、定義域の非空性が必要。
theorem const_range_nonempty {α : Type*} [MeasurableSpace α] [Nonempty α] :
    (SimpleFunc.const α (3 : ℝ≥0∞)).range = {3} :=
  SimpleFunc.range_const α 3

-- 空の定義域では値域も空。
theorem const_range_empty {α : Type*} [MeasurableSpace α] [IsEmpty α] :
    (SimpleFunc.const α (3 : ℝ≥0∞)).range = ∅ :=
  SimpleFunc.range_eq_empty_of_isEmpty _
-- END SOURCE ch15_008

-- BEGIN SOURCE ch15_009
open MeasureTheory
open scoped ENNReal

theorem eapprox_id_zero (x : ℝ≥0∞) :
    SimpleFunc.eapprox (id : ℝ≥0∞ → ℝ≥0∞) 0 x = 0 := by
  change (⊥ : SimpleFunc ℝ≥0∞ ℝ≥0∞) x = 0
  rfl

theorem eapprox_id_one_le_two (x : ℝ≥0∞) :
    SimpleFunc.eapprox (id : ℝ≥0∞ → ℝ≥0∞) 1 x ≤ SimpleFunc.eapprox id 2 x :=
  SimpleFunc.monotone_eapprox id (by decide : 1 ≤ 2) x

theorem eapprox_id_finite (n : ℕ) (x : ℝ≥0∞) :
    SimpleFunc.eapprox (id : ℝ≥0∞ → ℝ≥0∞) n x < ⊤ :=
  SimpleFunc.eapprox_lt_top id n x
-- END SOURCE ch15_009

-- BEGIN SOURCE ch15_010
open MeasureTheory
open scoped ENNReal

theorem eapprox_id_sup (x : ℝ≥0∞) :
    (⨆ n, SimpleFunc.eapprox (id : ℝ≥0∞ → ℝ≥0∞) n x) = x :=
  SimpleFunc.iSup_eapprox_apply measurable_id x
-- END SOURCE ch15_010

-- BEGIN SOURCE ch15_011
open MeasureTheory
open scoped ENNReal

theorem simple_indicator_unit_integral :
    (SimpleFunc.piecewise (Set.Icc (0 : ℝ) 1) measurableSet_Icc
      (SimpleFunc.const ℝ (1 : ℝ≥0∞))
      (SimpleFunc.const ℝ 0)).lintegral volume = 1 := by
  classical
  rw [← SimpleFunc.lintegral_eq_lintegral]
  simp only [SimpleFunc.coe_piecewise, SimpleFunc.coe_const]
  rw [lintegral_piecewise measurableSet_Icc]
  simp [Real.volume_Icc]
-- END SOURCE ch15_011

-- BEGIN SOURCE ch15_012
open MeasureTheory
open scoped ENNReal

theorem indicator_unit_lintegral :
    (∫⁻ x : ℝ, (Set.Icc 0 1).indicator (fun _ => (1 : ℝ≥0∞)) x) = 1 := by
  rw [lintegral_indicator measurableSet_Icc]
  simp [Real.volume_Icc]
-- END SOURCE ch15_012

end LeanBook.Ch15
