import Mathlib
open MeasureTheory
open scoped ENNReal

#check @MeasureTheory.L2.inner_def
#check @MeasureTheory.Lp.norm_def

theorem real_l2_inner {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f g : Lp ℝ 2 μ) : inner ℝ f g = ∫ x, f x * g x ∂μ := by
  rw [L2.inner_def]
  congr 1
  funext x
  exact mul_comm (g x) (f x)

theorem real_l2_norm_sq {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : Lp ℝ 2 μ) : ‖f‖ ^ 2 = ∫ x, (f x) ^ 2 ∂μ := by
  rw [← real_inner_self_eq_norm_sq, real_l2_inner]
  simp only [pow_two]

theorem complex_l2_inner {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f g : Lp ℂ 2 μ) :
    inner ℂ f g = ∫ x, star (f x) * g x ∂μ := by
  simpa only [RCLike.inner_apply, RCLike.star_def, mul_comm] using
    (L2.inner_def (𝕜 := ℂ) f g)

-- 問題18.3の「追加確認：内積とノルムの公式」の直後に置く。
noncomputable def unitIntervalMeasure : Measure ℝ :=
  volume.restrict (Set.Icc 0 1)

theorem unitInterval_probability : IsProbabilityMeasure unitIntervalMeasure := by
  constructor
  simp [unitIntervalMeasure, Real.volume_Icc]

def unitCoordinate (x : ℝ) : ℝ := x

-- 総合演習の共通準備を引き継ぐ。
theorem unitCoordinate_measurable : Measurable unitCoordinate := measurable_id

theorem unitCoordinate_integrable : Integrable unitCoordinate unitIntervalMeasure := by
  exact continuous_id.continuousOn.integrableOn_Icc

theorem unitCoordinate_sq_integrable :
    Integrable (fun x => unitCoordinate x ^ 2) unitIntervalMeasure := by
  exact (continuous_id.pow 2).continuousOn.integrableOn_Icc

-- 共通準備と、直前の可測性・可積分性の解答を引き継ぐ。
theorem unitCoordinate_expectation :
    (∫ x, unitCoordinate x ∂unitIntervalMeasure) = 1 / 2 := by
  change (∫ x in Set.Icc (0 : ℝ) 1, x) = 1 / 2
  rw [integral_Icc_eq_integral_Ioc,
    ← intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1),
    integral_id]
  norm_num

theorem unitCoordinate_second_moment :
    (∫ x, unitCoordinate x ^ 2 ∂unitIntervalMeasure) = 1 / 3 := by
  change (∫ x in Set.Icc (0 : ℝ) 1, x ^ 2) = 1 / 3
  rw [integral_Icc_eq_integral_Ioc,
    ← intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1),
    integral_pow]
  norm_num

-- 問題18.3の real_l2_norm_sq、共通準備、問題18.4の両方の解答を引き継ぐ。
theorem unitCoordinate_memLp : MemLp unitCoordinate 2 unitIntervalMeasure := by
  exact (memLp_two_iff_integrable_sq
    unitCoordinate_measurable.aestronglyMeasurable).2 unitCoordinate_sq_integrable

noncomputable def unitCoordinateL2 : Lp ℝ 2 unitIntervalMeasure :=
  unitCoordinate_memLp.toLp unitCoordinate

theorem unitCoordinateL2_ae :
    unitCoordinateL2 =ᵐ[unitIntervalMeasure] unitCoordinate :=
  unitCoordinate_memLp.coeFn_toLp

theorem unitCoordinateL2_norm_sq : ‖unitCoordinateL2‖ ^ 2 = 1 / 3 := by
  rw [real_l2_norm_sq]
  calc
    (∫ x, (unitCoordinateL2 x) ^ 2 ∂unitIntervalMeasure) =
        ∫ x, unitCoordinate x ^ 2 ∂unitIntervalMeasure := by
      apply integral_congr_ae
      filter_upwards [unitCoordinateL2_ae] with x hx
      rw [hx]
    _ = 1 / 3 := unitCoordinate_second_moment

#print axioms real_l2_inner

#print axioms real_l2_norm_sq

#print axioms complex_l2_inner

#print axioms unitIntervalMeasure

#print axioms unitInterval_probability

#print axioms unitCoordinate

#print axioms unitCoordinate_measurable

#print axioms unitCoordinate_integrable

#print axioms unitCoordinate_sq_integrable

#print axioms unitCoordinate_expectation

#print axioms unitCoordinate_second_moment

#print axioms unitCoordinate_memLp

#print axioms unitCoordinateL2

#print axioms unitCoordinateL2_ae

#print axioms unitCoordinateL2_norm_sq
