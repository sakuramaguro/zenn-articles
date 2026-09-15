import Mathlib

namespace LeanBook.Ch17

-- BEGIN SOURCE ch17_001
open MeasureTheory Filter
open scoped ENNReal Topology

-- 型の全体は #check の出力で確認する。以下のコメントは要約。
#check @lintegral_iSup
-- 非負可測関数列と各点での単調増加性から、上限と非負積分を交換する。
#check @lintegral_liminf_le
-- Measurable 版の Fatou の補題。
#check @lintegral_liminf_le'
-- AEMeasurable 版の Fatou の補題。
#check @tendsto_integral_of_dominated_convergence
-- 優関数 bound の後に、各 Fₙ の AE 強可測性、bound の可積分性、
-- ノルムの AE 支配、AE 収束の4つの証明を渡す。
-- END SOURCE ch17_001

-- BEGIN SOURCE ch17_002
open MeasureTheory Filter
open scoped ENNReal Topology

#check @lintegral_iSup
#check @lintegral_iSup'
-- 本節は Measurable と Monotone を使う lintegral_iSup を扱う。
-- 末尾に ' が付く版は、AE 可測性と AE での単調性を受け取る。
-- END SOURCE ch17_002

-- BEGIN SOURCE ch17_003
open MeasureTheory Filter
open scoped ENNReal Topology

-- 各点での上限と非負積分を交換する。
theorem monotone_convergence {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : ℕ → α → ℝ≥0∞) (hf : ∀ n, Measurable (f n))
    (hmono : Monotone f) :
    (∫⁻ a, ⨆ n, f n a ∂μ) = ⨆ n, ∫⁻ a, f n a ∂μ := by
  exact lintegral_iSup hf hmono
-- END SOURCE ch17_003

-- BEGIN SOURCE ch17_004
open MeasureTheory Filter
open scoped ENNReal Topology

#check @lintegral_liminf_le
#check @lintegral_liminf_le'
-- 前者は ∀ n, Measurable (f n)、後者は ∀ n, AEMeasurable (f n) μ。
-- 結論はどちらも「各点の liminf の積分 ≤ 積分列の liminf」。
-- END SOURCE ch17_004

-- BEGIN SOURCE ch17_005
open MeasureTheory Filter
open scoped ENNReal Topology

-- AE 可測性を仮定するので、末尾に ' の付いた版を使う。
theorem fatou_ae {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : ℕ → α → ℝ≥0∞) (hf : ∀ n, AEMeasurable (f n) μ) :
    (∫⁻ a, liminf (fun n => f n a) atTop ∂μ) ≤
      liminf (fun n => ∫⁻ a, f n a ∂μ) atTop := by
  exact lintegral_liminf_le' hf
-- END SOURCE ch17_005

-- BEGIN SOURCE ch17_006
open MeasureTheory Filter
open scoped ENNReal Topology

#check @tendsto_integral_of_dominated_convergence

-- 実数値関数では、AE 可測性から定理に必要な AE 強可測性を得られる。
theorem real_ae_strongly_measurable (f : ℝ → ℝ) (hf : AEMeasurable f volume) :
    AEStronglyMeasurable f volume :=
  hf.aestronglyMeasurable
-- END SOURCE ch17_006

-- BEGIN SOURCE ch17_007
open MeasureTheory Filter
open scoped ENNReal Topology

-- bound の後に、定理が要求する順序で4つの証明を渡す。
theorem dominated_convergence (F : ℕ → ℝ → ℝ) (f bound : ℝ → ℝ)
    (hFm : ∀ n, AEStronglyMeasurable (F n) volume)
    (hbound : Integrable bound volume)
    (hle : ∀ n, ∀ᵐ a ∂volume, ‖F n a‖ ≤ bound a)
    (htends : ∀ᵐ a ∂volume, Tendsto (fun n => F n a) atTop (𝓝 (f a))) :
    Tendsto (fun n => ∫ a, F n a ∂volume) atTop (𝓝 (∫ a, f a ∂volume)) := by
  exact tendsto_integral_of_dominated_convergence bound hFm hbound hle htends
-- END SOURCE ch17_007

-- BEGIN SOURCE ch17_008
open MeasureTheory Filter
open scoped ENNReal Topology

#check @lintegral_iSup

theorem monotone_sequence_iff {α : Type*} (f : ℕ → α → ℝ≥0∞) :
    Monotone f ↔ ∀ m n, m ≤ n → ∀ a, f m a ≤ f n a := by
  rfl
-- END SOURCE ch17_008

-- BEGIN SOURCE ch17_009
open MeasureTheory Filter
open scoped ENNReal Topology
theorem increasing_constants {α : Type*} [MeasurableSpace α] (μ : Measure α) :
    (∫⁻ _a : α, ⨆ n : ℕ, (n : ℝ≥0∞) ∂μ) =
      ⨆ n : ℕ, (n : ℝ≥0∞) * μ Set.univ := by
  have hmono : Monotone (fun n : ℕ => fun _a : α => (n : ℝ≥0∞)) := by
    intro m n hmn a
    change (m : ℝ≥0∞) ≤ (n : ℝ≥0∞)
    exact_mod_cast hmn
  rw [lintegral_iSup (fun _ => measurable_const) hmono]
  simp
-- END SOURCE ch17_009

-- BEGIN SOURCE ch17_010
open MeasureTheory Filter
open scoped ENNReal Topology
noncomputable def movingIndicator (n : ℕ) : ℝ → ℝ≥0∞ :=
  (Set.Ico (n : ℝ) (n + 1)).indicator (fun _ => 1)

theorem movingIndicator_measurable (n : ℕ) : Measurable (movingIndicator n) :=
  measurable_const.indicator measurableSet_Ico

theorem movingIndicator_integral (n : ℕ) :
    (∫⁻ x : ℝ, movingIndicator n x) = 1 := by
  rw [movingIndicator, lintegral_indicator measurableSet_Ico]
  simp [Real.volume_Ico]
-- END SOURCE ch17_010

-- BEGIN SOURCE ch17_011
-- 直前の movingIndicator と、その積分値の証明を引き継ぐ。
theorem movingIndicator_tendsto (x : ℝ) :
    Tendsto (fun n => movingIndicator n x) atTop (𝓝 0) := by
  have hn : ∀ᶠ n : ℕ in atTop, x < (n : ℝ) :=
    tendsto_natCast_atTop_atTop.eventually (eventually_gt_atTop x)
  apply tendsto_const_nhds.congr'
  filter_upwards [hn] with n hn
  symm
  exact Set.indicator_of_notMem (fun hx => (not_le_of_gt hn) hx.1) _

theorem fatou_strict :
    (∫⁻ x : ℝ, liminf (fun n => movingIndicator n x) atTop) <
      liminf (fun n => ∫⁻ x : ℝ, movingIndicator n x) atTop := by
  simp only [(movingIndicator_tendsto _).liminf_eq, movingIndicator_integral]
  simp
-- END SOURCE ch17_011

-- BEGIN SOURCE ch17_012
open MeasureTheory Filter
open scoped ENNReal Topology
noncomputable def sineSequence (n : ℕ) (x : ℝ) : ℝ :=
  Real.sin ((n : ℝ) * x) / (n : ℝ)

theorem sineSequence_norm_le (n : ℕ) (x : ℝ) :
    ‖sineSequence n x‖ ≤ 1 / (n : ℝ) := by
  simp only [sineSequence, Real.norm_eq_abs, abs_div, Nat.abs_cast]
  exact div_le_div_of_nonneg_right (Real.abs_sin_le_one _) (Nat.cast_nonneg n)

theorem sineSequence_norm_le_one (n : ℕ) (x : ℝ) :
    ‖sineSequence n x‖ ≤ 1 := by
  cases n with
  | zero => norm_num [sineSequence]
  | succ n =>
    apply (sineSequence_norm_le (n + 1) x).trans
    apply (div_le_one (by positivity : (0 : ℝ) < (↑(n + 1) : ℝ))).2
    exact_mod_cast Nat.succ_le_succ (Nat.zero_le n)

theorem sineSequence_tendsto (x : ℝ) :
    Tendsto (fun n => sineSequence n x) atTop (𝓝 0) :=
  squeeze_zero_norm (fun n => sineSequence_norm_le n x)
    tendsto_one_div_atTop_nhds_zero_nat

theorem sineSequence_integral_tendsto :
    Tendsto (fun n => ∫ x, sineSequence n x ∂volume.restrict (Set.Icc 0 1))
      atTop (𝓝 0) := by
  have hFm (n : ℕ) : AEStronglyMeasurable (sineSequence n)
      (volume.restrict (Set.Icc 0 1)) :=
    ((Real.continuous_sin.comp (continuous_const.mul continuous_id)).div_const _).aestronglyMeasurable
  have h := tendsto_integral_of_dominated_convergence (μ := volume.restrict (Set.Icc 0 1))
    (F := sineSequence) (f := fun _ => 0) (fun _ => 1) hFm (integrable_const 1)
    (fun n => ae_of_all _ (sineSequence_norm_le_one n))
    (ae_of_all _ sineSequence_tendsto)
  simpa using h
-- END SOURCE ch17_012

-- BEGIN SOURCE ch17_013
-- 解答の sineSequence と sineSequence_norm_le を引き継ぐ。
theorem sineSequence_integral_tendsto_direct :
    Tendsto (fun n => ∫ x, sineSequence n x ∂volume.restrict (Set.Icc 0 1))
      atTop (𝓝 0) := by
  apply squeeze_zero_norm (a := fun n : ℕ => 1 / (n : ℝ))
  · intro n
    have h := norm_integral_le_of_norm_le_const
      (μ := volume.restrict (Set.Icc 0 1)) (ae_of_all _ (sineSequence_norm_le n))
    simpa [Measure.real, Real.volume_Icc] using h
  · exact tendsto_one_div_atTop_nhds_zero_nat
-- END SOURCE ch17_013

end LeanBook.Ch17
