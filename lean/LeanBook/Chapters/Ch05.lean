import Mathlib

namespace LeanBook.Ch05

-- BEGIN SOURCE ch05_001

-- Mathlibの次元定理を適用し、等式の向きと加算の順を揃える。
theorem dimension_theorem_preview {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    Module.finrank K V = Module.finrank K (LinearMap.ker f) +
      Module.finrank K (LinearMap.range f) := by
  have key := LinearMap.finrank_range_add_finrank_ker f
  omega
-- END SOURCE ch05_001

-- BEGIN SOURCE ch05_002

-- LinearMap の定義を覗く
#print LinearMap
-- END SOURCE ch05_002

-- BEGIN SOURCE ch05_003
section
variable {K V W : Type*} [Field K] [AddCommGroup V] [Module K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W)
#check f
#check f.ker
#check f.range
end
-- END SOURCE ch05_003

-- BEGIN SOURCE ch05_005
-- have の名前・型・証明を、完成した小さい例で確認する。
theorem have_example (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  have h_ab : a ≤ b := h1
  exact le_trans h_ab h2
-- END SOURCE ch05_005

-- BEGIN SOURCE ch05_007
-- 次の4ブロックを順に連結して一つの宣言を作る。
theorem range_from_assumptions {K V W : Type*}
    [Field K]
-- END SOURCE ch05_007

-- BEGIN SOURCE ch05_008
    [AddCommGroup V] [Module K V]
-- END SOURCE ch05_008

-- BEGIN SOURCE ch05_009
    [AddCommGroup W] [Module K W]
-- END SOURCE ch05_009

-- BEGIN SOURCE ch05_010
    [FiniteDimensional K V] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.range f) := by
  infer_instance
-- END SOURCE ch05_010

-- BEGIN SOURCE ch05_011

theorem kernel_finite_search {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.ker f) := by
  exact?
-- END SOURCE ch05_011

-- BEGIN SOURCE ch05_012

theorem kernel_finite {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.ker f) :=
  FiniteDimensional.finiteDimensional_submodule f.ker
-- END SOURCE ch05_012

-- BEGIN SOURCE ch05_013

theorem range_finite_search {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.range f) := by
  exact?
-- END SOURCE ch05_013

-- BEGIN SOURCE ch05_014

theorem range_finite {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.range f) :=
  Module.Finite.range f
-- END SOURCE ch05_014

-- BEGIN SOURCE ch05_015
#check @LinearMap.finrank_range_add_finrank_ker
-- finrank K ↥(LinearMap.range f) + finrank K ↥(LinearMap.ker f) = finrank K V
-- END SOURCE ch05_015

-- BEGIN SOURCE ch05_016

-- 核の有限次元性はインスタンス探索でも得られる。
theorem kernel_finite_inferred {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.ker f) := by
  infer_instance
-- END SOURCE ch05_016

-- BEGIN SOURCE ch05_017

-- 像も、始域の有限次元性からインスタンス探索できる。
theorem range_finite_inferred {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.range f) := by
  infer_instance
-- END SOURCE ch05_017

-- BEGIN SOURCE ch05_018
#check @LinearMap.finrank_range_add_finrank_ker
-- END SOURCE ch05_018

-- BEGIN SOURCE ch05_019

-- 次の omega までを一つの証明として連結する。
theorem dimension_in_steps {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    Module.finrank K V = Module.finrank K (LinearMap.ker f) +
      Module.finrank K (LinearMap.range f) := by
  have key := LinearMap.finrank_range_add_finrank_ker f
-- END SOURCE ch05_019

-- BEGIN SOURCE ch05_020
  omega
-- END SOURCE ch05_020

-- BEGIN SOURCE ch05_021

-- 確認用の h_ker・h_range は使わず、既存の次元定理から導く。
theorem dimension_theorem {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    Module.finrank K V = Module.finrank K (LinearMap.ker f) +
      Module.finrank K (LinearMap.range f) := by
  have key := LinearMap.finrank_range_add_finrank_ker f
  omega
-- END SOURCE ch05_021

-- BEGIN SOURCE ch05_022
#print axioms dimension_theorem
-- END SOURCE ch05_022

-- BEGIN SOURCE ch05_024

-- LinearMap.ker と LinearMap.range の型シグネチャを確認する
#check LinearMap.ker
#check LinearMap.range
#print LinearMap.ker
-- END SOURCE ch05_024

-- BEGIN SOURCE ch05_025
#check @LinearMap.ker
section
variable {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [AddCommGroup W] [Module K W]
    (f : V →ₗ[K] W)
#check f.ker
#check f.range
end
-- END SOURCE ch05_025

-- BEGIN SOURCE ch05_027
theorem zero_kernel_finrank {K V : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V] :
    Module.finrank K (LinearMap.ker (0 : V →ₗ[K] V)) = Module.finrank K V := by
  rw [LinearMap.ker_zero]
  exact finrank_top K V
-- END SOURCE ch05_027

-- BEGIN SOURCE ch05_028
theorem zero_kernel_finrank_rw {K V : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V] :
    Module.finrank K (LinearMap.ker (0 : V →ₗ[K] V)) = Module.finrank K V := by
  have h : LinearMap.ker (0 : V →ₗ[K] V) = ⊤ := LinearMap.ker_zero
  rw [h, finrank_top]
-- END SOURCE ch05_028

-- BEGIN SOURCE ch05_030

theorem kernel_finite_exercise_answer {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.ker f) := by
  infer_instance
-- END SOURCE ch05_030

-- BEGIN SOURCE ch05_031

-- 同じ数学的事実を、補題名を明示して使う。
theorem kernel_finite_exercise_explicit {K V W : Type*} [Field K]
    [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    [AddCommGroup W] [Module K W] (f : V →ₗ[K] W) :
    FiniteDimensional K (LinearMap.ker f) :=
  FiniteDimensional.finiteDimensional_submodule f.ker
-- END SOURCE ch05_031

end LeanBook.Ch05
