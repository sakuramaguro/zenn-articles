/-
Stage 0: reference corrections validated during review.
This module is separate from the still-unrevised manuscript.
-/
import Mathlib

open MeasureTheory Filter
open scoped Topology NNReal ENNReal

namespace ManuscriptReview

-- 第2章：自然数から整数への coercion は自動挿入される。
example (n : ℕ) : ℤ := n
#check (inferInstance : Field ℝ)
#check (inferInstance : LinearOrder ℝ)
#check (inferInstance : IsStrictOrderedRing ℝ)
#check (inferInstance : CommRing ℤ)
#check (inferInstance : IsStrictOrderedRing ℤ)

-- 第3章：偽の等式は証明できない。可換モノイドには mul_comm を使う。
example : (1 : ℕ) + 1 ≠ 3 := by norm_num
example {α : Type*} [CommMonoid α] (a b : α) : a * b = b * a := mul_comm a b
example (n : ℕ) : 2 ∣ n ^ 2 + n := by
  simpa [pow_two, Nat.mul_add] using (Nat.even_mul_succ_self n).two_dvd

-- 第5章：既存の次元定理を適用する。終域全体の有限次元性は不要。
theorem rankNullity {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    Module.finrank K (LinearMap.range f) + Module.finrank K (LinearMap.ker f) =
      Module.finrank K V := LinearMap.finrank_range_add_finrank_ker f

-- 第6章：外側の関数の連続性は f a で仮定する。
theorem continuousComposition (f g : ℝ → ℝ) (a : ℝ)
    (hf : ContinuousAt f a) (hg : ContinuousAt g (f a)) :
    ContinuousAt (g ∘ f) a := hg.comp hf

-- 第8・9章：この検証環境で実在する型クラス名・定義。
#check (inferInstance : ProperSpace ℝ)
example {α : Type*} [UniformSpace α] (u : ℕ → α) :
    CauchySeq u ↔ Cauchy (Filter.map u Filter.atTop) := Iff.rfl

-- 第10章：lp.single の p は明示引数。
noncomputable def basisVector (n : ℕ) : lp (fun _ : ℕ => ℝ) 2 := lp.single 2 n 1

-- 第11章：非空性を含め、現行の API から一意存在と反復の収束を得る。
theorem banachFixedPoint {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    (f : α → α) {K : ℝ≥0} (hf : ContractingWith K f) : ∃! z, f z = z := by
  refine ⟨hf.fixedPoint f, hf.fixedPoint_isFixedPt, ?_⟩
  intro y hy
  exact hf.fixedPoint_unique hy

theorem banachIteration {α : Type*} [MetricSpace α] [CompleteSpace α] [Nonempty α]
    (f : α → α) {K : ℝ≥0} (hf : ContractingWith K f) (x : α) :
    Tendsto (fun n : ℕ => f^[n] x) atTop (𝓝 (hf.fixedPoint f)) :=
  hf.tendsto_iterate_fixedPoint x

theorem halfContracting : ContractingWith (1 / 2 : ℝ≥0) (fun x : ℝ => x / 2) := by
  refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
  simp only [Real.dist_eq]
  rw [← sub_div, abs_div]
  norm_num
  ring_nf
  exact le_rfl

-- 第16章：有理数の指示関数は a.e. 0、したがってルベーグ可積分。
noncomputable def dirichlet : ℝ → ℝ := (Set.range ((↑) : ℚ → ℝ)).indicator (fun _ => 1)

theorem dirichletAeZero : dirichlet =ᵐ[volume] (fun _ => 0) := by
  filter_upwards [(Set.countable_range ((↑) : ℚ → ℝ)).ae_notMem volume] with x hx
  simp [dirichlet, Set.indicator_of_notMem hx]

theorem dirichletIntegrable : Integrable dirichlet volume :=
  (integrable_zero ℝ ℝ volume).congr dirichletAeZero.symm

theorem dirichletIntegral : (∫ x : ℝ, dirichlet x) = 0 := by
  calc
    (∫ x : ℝ, dirichlet x) = ∫ _x : ℝ, (0 : ℝ) := integral_congr_ae dirichletAeZero
    _ = 0 := integral_zero _ _

-- 第17章：Bochner 積分の優収束定理は AE 強可測性を受け取る。
theorem dominatedConvergence (F : ℕ → ℝ → ℝ) (f bound : ℝ → ℝ)
    (hFm : ∀ n, AEStronglyMeasurable (F n) volume)
    (hbound : Integrable bound volume)
    (hle : ∀ n, ∀ᵐ x ∂volume, ‖F n x‖ ≤ bound x)
    (hlim : ∀ᵐ x ∂volume, Tendsto (fun n => F n x) atTop (𝓝 (f x))) :
    Tendsto (fun n => ∫ x, F n x) atTop (𝓝 (∫ x, f x)) :=
  tendsto_integral_of_dominated_convergence bound hFm hbound hle hlim

-- 第18章：新しい API 名、期待値の非計算的定義。
#check MeasureTheory.MemLp
#check MeasureTheory.eLpNorm
noncomputable def expectation {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (X : Ω → ℝ) : ℝ := ∫ ω, X ω ∂P
example {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (c : ℝ) : (∫ _ω : Ω, c ∂P) = c := by simp

-- 第12〜16章：測度・単関数・非負積分の API。
#check MeasureTheory.measure_empty
#check MeasureTheory.measure_iUnion
#check MeasureTheory.measure_mono
#check MeasureTheory.ae
#check Metric.isCompact_iff_isClosed_bounded
example : (SimpleFunc.const ℝ (3 : ℝ≥0∞)).lintegral
    (volume.restrict (Set.Icc 0 1)) = 3 := by
  rw [SimpleFunc.const_lintegral]
  norm_num [Measure.restrict_apply_univ, Real.volume_Icc]

example (A : Set ℝ) (hA : MeasurableSet A) (μ : Measure ℝ) :
    (∫⁻ x, A.indicator (fun _ => (1 : ℝ≥0∞)) x ∂μ) = μ A := by
  rw [lintegral_indicator hA]
  simp

example {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : ℕ → α → ℝ≥0∞) (hf : ∀ n, Measurable (f n)) (hm : Monotone f) :
    (∫⁻ x, ⨆ n, f n x ∂μ) = ⨆ n, ∫⁻ x, f n x ∂μ := lintegral_iSup hf hm

example {α : Type*} [MeasurableSpace α] (μ : Measure α)
    (f : ℕ → α → ℝ≥0∞) (hf : ∀ n, AEMeasurable (f n) μ) :
    (∫⁻ x, liminf (fun n => f n x) atTop ∂μ) ≤
      liminf (fun n => ∫⁻ x, f n x ∂μ) atTop := lintegral_liminf_le' hf

-- 第18章：condExp の大文字小文字とマルチンゲールの補題名。
example {Ω : Type*} [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (ℱ : Filtration ℕ (‹MeasurableSpace Ω›)) (f : ℕ → Ω → ℝ)
    (hf : Martingale f ℱ P) (s t : ℕ) (hst : s ≤ t) :
    (condExp (ℱ s) P (f t)) =ᵐ[P] f s := hf.condExp_ae_eq hst

#print axioms rankNullity
#print axioms banachFixedPoint
#print axioms halfContracting
#print axioms dirichletIntegrable
#print axioms dirichletIntegral
#print axioms dominatedConvergence

end ManuscriptReview
