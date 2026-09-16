import Mathlib

namespace LeanBook.Ch16

-- BEGIN SOURCE ch16_001
open MeasureTheory
open scoped ENNReal

#check @lintegral
#check @integral
#check @integral_add
#check @integral_smul
#check @norm_integral_le_integral_norm

-- この不等式自体にはIntegrableの仮定は不要。
theorem norm_integral_bound_intro (f : ℝ → ℝ) :
    ‖∫ x, f x ∂volume‖ ≤ ∫ x, ‖f x‖ ∂volume :=
  norm_integral_le_integral_norm f
-- END SOURCE ch16_001

-- BEGIN SOURCE ch16_002
open MeasureTheory
open scoped ENNReal

theorem lintegral_notation (μ : Measure ℝ) (f : ℝ → ℝ≥0∞) :
    (∫⁻ x, f x ∂μ) = lintegral μ f := rfl

-- 全ての下側の単関数について上限を取る定義。
theorem lintegral_definition (μ : Measure ℝ) (f : ℝ → ℝ≥0∞) :
    (∫⁻ x, f x ∂μ) =
      ⨆ (g : SimpleFunc ℝ ℝ≥0∞) (_ : (g : ℝ → ℝ≥0∞) ≤ f), g.lintegral μ := by
  rw [lintegral]

theorem constant_lintegral (c : ℝ≥0∞) (μ : Measure ℝ) :
    (∫⁻ _x, c ∂μ) = c * μ Set.univ := lintegral_const c

theorem indicator_lintegral (A : Set ℝ) (hA : MeasurableSet A) (μ : Measure ℝ) :
    (∫⁻ x, A.indicator (fun _ => (1 : ℝ≥0∞)) x ∂μ) = μ A := by
  rw [lintegral_indicator hA]
  simp
-- END SOURCE ch16_002

-- BEGIN SOURCE ch16_003
open MeasureTheory
open scoped ENNReal

#print integral
#check @integral_undef
-- END SOURCE ch16_003

-- BEGIN SOURCE ch16_004
open MeasureTheory
open scoped ENNReal

-- Lebesgue測度で実数全体を考えると、定数1は可積分でない。
theorem one_not_integrable : ¬ Integrable (fun _ : ℝ => (1 : ℝ)) volume := by
  simp [integrable_const_iff, isFiniteMeasure_iff]

theorem one_integral_undef : (∫ _x : ℝ, (1 : ℝ)) = 0 :=
  integral_undef one_not_integrable

-- 同じ定数をENNReal値で非負積分すると、値は無限大。
theorem one_lintegral_infinite : (∫⁻ _x : ℝ, (1 : ℝ≥0∞)) = ⊤ := by
  simp
-- END SOURCE ch16_004

-- BEGIN SOURCE ch16_005
open MeasureTheory
open scoped ENNReal

#print Integrable
#print HasFiniteIntegral
-- 定義の要約（型の引数・型クラスなどは省略）：
-- Integrable f μ = AEStronglyMeasurable f μ ∧ HasFiniteIntegral f μ
-- HasFiniteIntegral f μ = ((∫⁻ a, ‖f a‖ₑ ∂μ) < ∞)
-- ‖f a‖ₑ は ℝ≥0∞ に値を取るノルム。
-- END SOURCE ch16_005

-- BEGIN SOURCE ch16_006
open MeasureTheory

theorem constant_integrable (c : ℝ) (μ : Measure ℝ) [IsFiniteMeasure μ] :
    Integrable (fun _ => c) μ :=
  integrable_const c

theorem sine_integrable_on_interval :
    IntegrableOn Real.sin (Set.Icc 0 (2 * Real.pi)) volume :=
  Real.continuous_sin.continuousOn.integrableOn_Icc
-- END SOURCE ch16_006

-- BEGIN SOURCE ch16_007
open MeasureTheory

-- 実数値のディリクレ関数。有理数の像で1、それ以外で0。
noncomputable def dirichlet : ℝ → ℝ :=
  (Set.range ((↑) : ℚ → ℝ)).indicator (fun _ => 1)

theorem rationals_volume_zero : volume (Set.range ((↑) : ℚ → ℝ)) = 0 :=
  (Set.countable_range ((↑) : ℚ → ℝ)).measure_zero volume

theorem dirichlet_ae_zero : dirichlet =ᵐ[volume] (fun _ => 0) := by
  filter_upwards [(Set.countable_range ((↑) : ℚ → ℝ)).ae_notMem volume] with x hx
  simp [dirichlet, Set.indicator_of_notMem hx]

theorem dirichlet_integrable : Integrable dirichlet volume :=
  (integrable_zero ℝ ℝ volume).congr dirichlet_ae_zero.symm

theorem dirichlet_integral : (∫ x : ℝ, dirichlet x) = 0 := by
  calc
    (∫ x : ℝ, dirichlet x) = ∫ _x : ℝ, (0 : ℝ) := integral_congr_ae dirichlet_ae_zero
    _ = 0 := integral_zero _ _
-- END SOURCE ch16_007

-- BEGIN SOURCE ch16_008
open MeasureTheory

#check @integral_eq_lintegral_of_nonneg_ae
-- 仮定と結論を実数値関数に限定して確認する。
theorem nonnegative_integral (f : ℝ → ℝ) (μ : Measure ℝ)
    (hf : 0 ≤ᵐ[μ] f) (hfm : AEStronglyMeasurable f μ) :
    (∫ x, f x ∂μ) = (∫⁻ x, ENNReal.ofReal (f x) ∂μ).toReal :=
  integral_eq_lintegral_of_nonneg_ae hf hfm
-- END SOURCE ch16_008

-- BEGIN SOURCE ch16_009
open MeasureTheory
open scoped ENNReal

theorem integral_add_demo (f g : ℝ → ℝ)
    (hf : Integrable f volume) (hg : Integrable g volume) :
    (∫ x, (f x + g x) ∂volume) = (∫ x, f x ∂volume) + ∫ x, g x ∂volume := by
  exact integral_add hf hg
-- END SOURCE ch16_009

-- BEGIN SOURCE ch16_010
open MeasureTheory
open scoped ENNReal

theorem integral_smul_demo (r : ℝ) (f : ℝ → ℝ) (μ : Measure ℝ) :
    (∫ x, r • f x ∂μ) = r • ∫ x, f x ∂μ := by
  exact integral_smul r f
-- END SOURCE ch16_010

-- BEGIN SOURCE ch16_011
open MeasureTheory
open scoped ENNReal

theorem norm_integral_bound (f : ℝ → ℝ) (μ : Measure ℝ) :
    ‖∫ x, f x ∂μ‖ ≤ ∫ x, ‖f x‖ ∂μ :=
  norm_integral_le_integral_norm f
-- END SOURCE ch16_011

-- BEGIN SOURCE ch16_012
open MeasureTheory
open scoped ENNReal

theorem const_three_lintegral_top : (∫⁻ _x : ℝ, (3 : ℝ≥0∞) ∂volume) = ⊤ := by
  rw [lintegral_const, Real.volume_univ]
  simp
-- END SOURCE ch16_012

-- BEGIN SOURCE ch16_013
open MeasureTheory
open scoped ENNReal

theorem const_three_lintegral_top_alt : (∫⁻ _x : ℝ, (3 : ℝ≥0∞) ∂volume) = ⊤ := by
  calc
    (∫⁻ _x : ℝ, (3 : ℝ≥0∞) ∂volume) = 3 * volume (Set.univ : Set ℝ) := lintegral_const 3
    _ = ⊤ := by simp
-- END SOURCE ch16_013

-- BEGIN SOURCE ch16_014
open MeasureTheory

-- 開半直線での既存定理を、端点0を含む半直線へ移す。
theorem exp_neg_integrable :
    Integrable (fun x : ℝ => Real.exp (-x)) (volume.restrict (Set.Ici 0)) := by
  exact Iff.mpr integrableOn_Ici_iff_integrableOn_Ioi (integrableOn_exp_neg_Ioi 0)
-- END SOURCE ch16_014

-- BEGIN SOURCE ch16_015

-- 前の exp_neg_integrable を使い、Integrable の2条件を確認する。
theorem exp_neg_integrable_parts :
    Integrable (fun x : ℝ => Real.exp (-x)) (volume.restrict (Set.Ici 0)) := by
  refine ⟨?_, ?_⟩
  · exact (Real.continuous_exp.comp continuous_id.neg).aestronglyMeasurable
  · exact exp_neg_integrable.hasFiniteIntegral
-- END SOURCE ch16_015

-- BEGIN SOURCE ch16_016
open MeasureTheory

#check @integral_undef
-- 非可積分性を仮定した場合の規約値。
theorem integral_of_not_integrable (f : ℝ → ℝ) (hf : ¬Integrable f volume) :
    (∫ x, f x) = 0 :=
  integral_undef hf
-- END SOURCE ch16_016

-- BEGIN SOURCE ch16_017
-- 16.4節の dirichlet と dirichlet_ae_zero を引き継ぐ。
-- [0,1] への制限でも、可積分性と積分値0の両方を証明する。
theorem dirichlet_on_unit_interval :
    Integrable dirichlet (volume.restrict (Set.Icc 0 1)) ∧
      (∫ x, dirichlet x ∂volume.restrict (Set.Icc 0 1)) = 0 := by
  have h : dirichlet =ᵐ[volume.restrict (Set.Icc 0 1)] (fun _ => 0) :=
    ae_restrict_of_ae dirichlet_ae_zero
  constructor
  · exact (integrable_zero ℝ ℝ _).congr h.symm
  · calc
      (∫ x, dirichlet x ∂volume.restrict (Set.Icc 0 1)) =
          ∫ _x : ℝ, (0 : ℝ) ∂volume.restrict (Set.Icc 0 1) := integral_congr_ae h
      _ = 0 := integral_zero _ _
-- END SOURCE ch16_017

end LeanBook.Ch16
