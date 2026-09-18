import Mathlib

namespace LeanBook.Ch14

-- BEGIN SOURCE ch14_001
open MeasureTheory Filter

-- 完全な型には、定義域・値域の可測空間も現れる。
#check @Measurable
#check @AEMeasurable
#check @MeasureTheory.ae_restrict_of_ae

theorem ae_restrict_demo (f g : ℝ → ℝ) (h : f =ᵐ[volume] g) :
    f =ᵐ[volume.restrict (Set.Icc 0 1)] g :=
  ae_restrict_of_ae h
-- END SOURCE ch14_001

-- BEGIN SOURCE ch14_002
open MeasureTheory

#print Measurable
#check @Continuous.measurable

theorem measurable_iff_preimages {α β : Type*}
    [MeasurableSpace α] [MeasurableSpace β] (f : α → β) :
    Measurable f ↔ ∀ t : Set β, MeasurableSet t → MeasurableSet (f ⁻¹' t) := by
  constructor
  · intro hf t ht
    exact hf ht
  · intro h t ht
    exact h t ht
-- END SOURCE ch14_002

-- BEGIN SOURCE ch14_003
open MeasureTheory

-- 連続関数は可測（BorelSpace が必要）
theorem continuous_measurable (f : ℝ → ℝ) (hf : Continuous f) : Measurable f := hf.measurable

-- 定数関数は可測
theorem constant_measurable (c : ℝ) : Measurable (fun _ : ℝ => c) := measurable_const

-- 恒等関数は可測
theorem identity_measurable : Measurable (id : ℝ → ℝ) := measurable_id

-- 可測関数の合成は可測
theorem compose_measurable (f g : ℝ → ℝ) (hf : Measurable f) (hg : Measurable g) :
    Measurable (g ∘ f) := hg.comp hf

-- 可測関数の和は可測
theorem add_measurable (f g : ℝ → ℝ) (hf : Measurable f) (hg : Measurable g) :
    Measurable (fun x => f x + g x) := hf.add hg
-- END SOURCE ch14_003

-- BEGIN SOURCE ch14_004
open MeasureTheory

-- 目標：Measurable f
theorem continuous_measurable_tactic (f : ℝ → ℝ) (hf : Continuous f) : Measurable f := by
  exact hf.measurable   -- ステップ②
-- No goals ✓
-- END SOURCE ch14_004

-- BEGIN SOURCE ch14_005
open MeasureTheory

#check @MeasureTheory.ae
#check @Filter.EventuallyEq
#check @ae_iff

-- 実数値の指示関数としてディリクレ関数を書く。
theorem dirichlet_ae_zero :
    (Set.range ((↑) : ℚ → ℝ)).indicator (fun _ => (1 : ℝ)) =ᵐ[volume]
      (fun _ => 0) := by
  have hQ : ∀ᵐ x : ℝ ∂volume, x ∉ Set.range ((↑) : ℚ → ℝ) :=
    (Set.countable_range ((↑) : ℚ → ℝ)).ae_notMem volume
  filter_upwards [hQ] with x hx
  simp [Set.indicator_of_notMem hx]
-- END SOURCE ch14_005

-- BEGIN SOURCE ch14_006
open MeasureTheory

-- 集合 s の可測性は、この方向の推論には不要。
#check @MeasureTheory.ae_restrict_of_ae
#check @MeasureTheory.ae_restrict_le
-- END SOURCE ch14_006

-- BEGIN SOURCE ch14_007
open MeasureTheory
theorem ae_restrict_tactic (f g : ℝ → ℝ) (h : f =ᵐ[volume] g) :
    f =ᵐ[volume.restrict (Set.Icc 0 1)] g := by
  exact ae_restrict_of_ae h
-- END SOURCE ch14_007

-- BEGIN SOURCE ch14_008
open MeasureTheory

#print AEMeasurable
#check @AEMeasurable.congr
#check @Measurable.stronglyMeasurable
#check @StronglyMeasurable.measurable

theorem measurable_is_aemeasurable (f : ℝ → ℝ) (μ : Measure ℝ)
    (hf : Measurable f) : AEMeasurable f μ := hf.aemeasurable

theorem continuous_is_aemeasurable (f : ℝ → ℝ) (hf : Continuous f)
    (μ : Measure ℝ) : AEMeasurable f μ := hf.measurable.aemeasurable
-- END SOURCE ch14_008

-- BEGIN SOURCE ch14_009
-- 方法①：Continuous.measurable を使う
theorem square_measurable : Measurable (fun x : ℝ => x ^ 2) := by
  exact (continuous_pow 2).measurable
  -- No goals ✓
-- END SOURCE ch14_009

-- BEGIN SOURCE ch14_010
-- 方法②：fun_prop タクティクに任せる
theorem square_measurable_auto : Measurable (fun x : ℝ => x ^ 2) := by
  fun_prop
-- END SOURCE ch14_010

-- BEGIN SOURCE ch14_011
-- 多項式 f(x) = 3x² + 2x + 1 の可測性
theorem polynomial_measurable_auto : Measurable (fun x : ℝ => 3 * x ^ 2 + 2 * x + 1) := by
  fun_prop
  -- No goals ✓
-- END SOURCE ch14_011

-- BEGIN SOURCE ch14_012

theorem polynomial_measurable_manual :
    Measurable (fun x : ℝ => 3 * x ^ 2 + 2 * x + 1) := by
  apply Measurable.add
  · apply Measurable.add
    · simpa only [pow_two] using
        (measurable_const.mul (measurable_id.mul measurable_id) :
          Measurable (fun x : ℝ => 3 * (x * x)))
    · exact measurable_const.mul measurable_id
  · exact measurable_const
-- END SOURCE ch14_012

-- BEGIN SOURCE ch14_013
section Example13

variable {α : Type*} [MeasurableSpace α] (μ : MeasureTheory.Measure α)
theorem ae_change_measurable (f g : α → ℝ) (hf : Measurable f) (h : f =ᵐ[μ] g) :
    AEMeasurable g μ := by
  exact hf.aemeasurable.congr h
  -- No goals ✓

end Example13
-- END SOURCE ch14_013

-- BEGIN SOURCE ch14_014
section Example14

variable {α : Type*} [MeasurableSpace α] (μ : MeasureTheory.Measure α)
theorem ae_change_measurable_from_def (f g : α → ℝ) (hf : Measurable f) (h : f =ᵐ[μ] g) :
    AEMeasurable g μ := by
  exact ⟨f, hf, h.symm⟩

end Example14
-- END SOURCE ch14_014

-- BEGIN SOURCE ch14_015
open MeasureTheory

#check @measurable_of_measurable_on_compl_singleton

noncomputable def pointChange : ℝ → ℝ :=
  ({0} : Set ℝ).indicator (fun _ => (1 : ℝ))

theorem pointChange_measurable : Measurable pointChange :=
  measurable_const.indicator (measurableSet_singleton 0)

theorem pointChange_ae_zero : pointChange =ᵐ[volume] (fun _ => (0 : ℝ)) := by
  have h0 : ∀ᵐ x : ℝ ∂volume, x ∉ ({0} : Set ℝ) :=
    (Set.countable_singleton (0 : ℝ)).ae_notMem volume
  filter_upwards [h0] with x hx
  simp [pointChange, Set.indicator_of_notMem hx]

-- 積分の章を先取りした比較。同じ関数でも測度を変えると値が変わる。
theorem pointChange_integral_volume : (∫ x, pointChange x) = 0 := by
  simpa using integral_congr_ae pointChange_ae_zero

theorem pointChange_integral_dirac :
    (∫ x, pointChange x ∂Measure.dirac (0 : ℝ)) = 1 := by
  rw [integral_dirac]
  simp [pointChange]
-- END SOURCE ch14_015

end LeanBook.Ch14
