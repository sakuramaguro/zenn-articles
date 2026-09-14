import Mathlib

namespace LeanBook.Ch11

-- BEGIN SOURCE ch11_001
open Filter
open scoped Topology NNReal ENNReal

theorem halfContracting :
    ContractingWith (1 / 2 : ℝ≥0) (fun x : ℝ => x / 2) := by
  refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
  simp only [Real.dist_eq]
  rw [← sub_div, abs_div]
  norm_num
  ring_nf
  exact le_rfl

theorem half_fixedPoint_zero :
    halfContracting.fixedPoint (fun x : ℝ => x / 2) = 0 :=
  (halfContracting.fixedPoint_unique (by norm_num : (0 : ℝ) / 2 = 0)).symm
-- END SOURCE ch11_001

-- BEGIN SOURCE ch11_002
-- 非空な完備距離空間上の縮小写像：一意存在と全初期点からの収束
theorem banach_fixed_point_and_convergence
    {X : Type*} [MetricSpace X] [CompleteSpace X] [Nonempty X]
    (f : X → X) {k : ℝ≥0} (hf : ContractingWith k f) :
    ∃! z : X, f z = z ∧
      ∀ x : X, Tendsto (fun n : ℕ => f^[n] x) atTop (𝓝 z) := by
  refine ⟨hf.fixedPoint f, ⟨hf.fixedPoint_isFixedPt,
    fun x => hf.tendsto_iterate_fixedPoint x⟩, ?_⟩
  intro y hy
  exact hf.fixedPoint_unique hy.1
-- END SOURCE ch11_002

-- BEGIN SOURCE ch11_003
-- 出力には一般の空間構造や宇宙変数も含まれる
#check @LipschitzWith
#check @ContractingWith
#check @ContractingWith.toLipschitzWith
-- END SOURCE ch11_003

-- BEGIN SOURCE ch11_004
theorem contracting_iff (k : ℝ≥0) (f : ℝ → ℝ) :
    ContractingWith k f ↔
      k < 1 ∧ ∀ x y, dist (f x) (f y) ≤ (k : ℝ) * dist x y := by
  constructor
  · intro ⟨hk, hlip⟩
    exact ⟨hk, hlip.dist_le_mul⟩
  · intro ⟨hk, h⟩
    exact ⟨hk, LipschitzWith.of_dist_le_mul h⟩
-- END SOURCE ch11_004

-- BEGIN SOURCE ch11_005
#check @ContractingWith.fixedPoint
#check @ContractingWith.fixedPoint_isFixedPt
#check @ContractingWith.fixedPoint_unique
#check @ContractingWith.fixedPoint_unique'
#check @ContractingWith.tendsto_iterate_fixedPoint
-- END SOURCE ch11_005

-- BEGIN SOURCE ch11_006
theorem half_map_fixed_point : ∃! z : ℝ, (fun x : ℝ => x / 2) z = z := by
-- END SOURCE ch11_006

-- BEGIN SOURCE ch11_007
  have hf : ContractingWith (1 / 2 : ℝ≥0) (fun x : ℝ => x / 2) := by
    constructor
    · norm_num
-- END SOURCE ch11_007

-- BEGIN SOURCE ch11_008
    · apply LipschitzWith.of_dist_le_mul
      intro x y
      simp only [Real.dist_eq]
-- END SOURCE ch11_008

-- BEGIN SOURCE ch11_009
      rw [← sub_div, abs_div]
      norm_num
      ring_nf
      exact le_rfl
-- END SOURCE ch11_009

-- BEGIN SOURCE ch11_010
  refine ⟨hf.fixedPoint (fun x : ℝ => x / 2), hf.fixedPoint_isFixedPt, ?_⟩
-- END SOURCE ch11_010

-- BEGIN SOURCE ch11_011
  intro y hy
  exact hf.fixedPoint_unique hy
-- END SOURCE ch11_011

-- BEGIN SOURCE ch11_012
theorem banach_fixed_point
    (X : Type*) [MetricSpace X] [CompleteSpace X] [Nonempty X]
    (k : ℝ≥0) (f : X → X) (hf : ContractingWith k f) :
    ∃! z : X, f z = z := by
  refine ⟨hf.fixedPoint f, hf.fixedPoint_isFixedPt, ?_⟩
  intro y hy
  exact hf.fixedPoint_unique hy
-- END SOURCE ch11_012

-- BEGIN SOURCE ch11_013
-- 初期点を引数として受け取る場合は、それから Nonempty を作れる
theorem banach_fixed_point_from_start
    {X : Type*} [MetricSpace X] [CompleteSpace X]
    (x₀ : X) (f : X → X) {k : ℝ≥0} (hf : ContractingWith k f) :
    ∃! z : X, f z = z := by
  letI : Nonempty X := ⟨x₀⟩
  exact banach_fixed_point X k f hf
-- END SOURCE ch11_013

-- BEGIN SOURCE ch11_014
theorem half_iterates_to_zero (x₀ : ℝ) :
    Tendsto (fun n : ℕ => (fun x : ℝ => x / 2)^[n] x₀) atTop (𝓝 0) := by
-- END SOURCE ch11_014

-- BEGIN SOURCE ch11_015
  simpa only [half_fixedPoint_zero] using
    halfContracting.tendsto_iterate_fixedPoint x₀
-- END SOURCE ch11_015

-- BEGIN SOURCE ch11_016
abbrev ell2 := lp (fun _ : ℕ => ℝ) 2

#check (inferInstance : MetricSpace ell2)
#check (inferInstance : CompleteSpace ell2)
#check (inferInstance : Nonempty ell2)

theorem ell2_banach (f : ell2 → ell2) (k : ℝ≥0)
    (hf : ContractingWith k f) : ∃! z : ell2, f z = z :=
  banach_fixed_point ell2 k f hf
-- END SOURCE ch11_016

-- BEGIN SOURCE ch11_018
theorem contracting_continuousAt
    {X : Type*} [MetricSpace X] {k : ℝ≥0} {f : X → X}
    (hf : ContractingWith k f) (a : X) : ContinuousAt f a :=
  hf.toLipschitzWith.continuous.continuousAt

theorem tendsto_at_fixedPoint
    {X : Type*} [MetricSpace X] [CompleteSpace X] [Nonempty X]
    {k : ℝ≥0} {f : X → X} (hf : ContractingWith k f) :
    Tendsto f (𝓝 (hf.fixedPoint f)) (𝓝 (hf.fixedPoint f)) := by
  simpa only [ContinuousAt, hf.fixedPoint_isFixedPt.eq] using
    contracting_continuousAt hf (hf.fixedPoint f)
-- END SOURCE ch11_018

-- BEGIN SOURCE ch11_019
example : (1 / 3 : ℝ≥0) < 1 := by norm_num
-- END SOURCE ch11_019

-- BEGIN SOURCE ch11_021
theorem affineContracting :
    ContractingWith (1 / 3 : ℝ≥0) (fun x : ℝ => x / 3 + 1) := by
  refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
  simp only [Real.dist_eq]
  rw [show x / 3 + 1 - (y / 3 + 1) = (x - y) / 3 by ring, abs_div]
  norm_num
  ring_nf
  exact le_rfl
-- END SOURCE ch11_021

-- BEGIN SOURCE ch11_022
theorem affineContracting_calc :
    ContractingWith (1 / 3 : ℝ≥0) (fun x : ℝ => x / 3 + 1) := by
  refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
  norm_num only [NNReal.coe_div, NNReal.coe_one, NNReal.coe_ofNat]
  simp only [Real.dist_eq]
  calc
    |x / 3 + 1 - (y / 3 + 1)| = |x - y| / 3 := by
      rw [show x / 3 + 1 - (y / 3 + 1) = (x - y) / 3 by ring, abs_div]
      norm_num
    _ ≤ (1 / 3 : ℝ) * |x - y| := le_of_eq (by ring)
-- END SOURCE ch11_022

-- BEGIN SOURCE ch11_023
theorem affine_map_fixed_point : ∃! z : ℝ, (fun x : ℝ => x / 3 + 1) z = z :=
  banach_fixed_point ℝ (1 / 3) (fun x : ℝ => x / 3 + 1) affineContracting

theorem affine_fixedPoint_value :
    affineContracting.fixedPoint (fun x : ℝ => x / 3 + 1) = 3 / 2 :=
  (affineContracting.fixedPoint_unique
    (by norm_num : (3 / 2 : ℝ) / 3 + 1 = 3 / 2)).symm
-- END SOURCE ch11_023

-- BEGIN SOURCE ch11_024
-- 不動点が3/2であることを使って、任意の初期点からの収束も得る
theorem affine_iterates (x₀ : ℝ) :
    Tendsto (fun n : ℕ => (fun x : ℝ => x / 3 + 1)^[n] x₀)
      atTop (𝓝 (3 / 2)) := by
  simpa only [affine_fixedPoint_value] using
    affineContracting.tendsto_iterate_fixedPoint x₀
-- END SOURCE ch11_024

-- BEGIN SOURCE ch11_025
-- 6.5節の ell2 の定義を引き継ぐ
noncomputable def halfEll2 (x : ell2) : ell2 := (1 / 2 : ℝ) • x

theorem halfEll2_apply (x : ell2) (n : ℕ) : halfEll2 x n = x n / 2 := by
  simp [halfEll2, lp.coeFn_smul, smul_eq_mul, div_eq_mul_inv, mul_comm]

theorem halfEll2Contracting : ContractingWith (1 / 2 : ℝ≥0) halfEll2 := by
  refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
  simp only [halfEll2, dist_eq_norm, ← smul_sub, norm_smul]
  norm_num

theorem halfEll2_unique : ∃! z : ell2, halfEll2 z = z :=
  banach_fixed_point ell2 (1 / 2) halfEll2 halfEll2Contracting

theorem halfEll2_fixedPoint_zero : halfEll2Contracting.fixedPoint halfEll2 = 0 := by
  apply Eq.symm
  apply halfEll2Contracting.fixedPoint_unique
  simp [Function.IsFixedPt, halfEll2]

theorem halfEll2_iterates (x₀ : ell2) :
    Tendsto (fun n : ℕ => halfEll2^[n] x₀) atTop (𝓝 0) := by
  simpa only [halfEll2_fixedPoint_zero] using
    halfEll2Contracting.tendsto_iterate_fixedPoint x₀
-- END SOURCE ch11_025

-- BEGIN SOURCE ch11_026
#check (inferInstance : CompleteSpace ell2)
#check (inferInstance : Nonempty ell2)
#check @ContractingWith.fixedPoint
#check @ContractingWith.tendsto_iterate_fixedPoint
#print axioms banach_fixed_point
#print axioms half_iterates_to_zero
#print axioms halfEll2_iterates
-- END SOURCE ch11_026

end LeanBook.Ch11
