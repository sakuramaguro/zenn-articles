import Mathlib

namespace LeanBook.Ch10

-- BEGIN SOURCE ch10_001
open scoped ENNReal

-- 本章では ℓ² の型を ell2 と名付ける
abbrev ell2 := lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)

#check (inferInstance : MetricSpace ell2)
#check (inferInstance : CompleteSpace ell2)

-- もう一つのゴール：単位閉球の非コンパクト性を証明し、
-- ¬ ProperSpace ell2 を導く（10.3節の完成証明）。
-- END SOURCE ch10_001

-- BEGIN SOURCE ch10_002
#check @lp
-- 出力の末尾は AddSubgroup (PreLp E)。引数の型クラスも確認する。
-- END SOURCE ch10_002

-- BEGIN SOURCE ch10_003
#check (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞) : Type)
#check (lp (fun _ : ℕ => ℝ) 2 : Type) -- 2 の型は引数から推論される
-- END SOURCE ch10_003

-- BEGIN SOURCE ch10_004
#print lp
#print Memℓp
#check memℓp_zero_iff
#check memℓp_infty_iff
#check @memℓp_gen_iff

-- 本章の実数列・指数2に特殊化した同値
theorem mem_two_iff (f : ℕ → ℝ) :
    Memℓp f (2 : ℝ≥0∞) ↔ Summable (fun n => ‖f n‖ ^ (2 : ℕ)) := by
  simpa using (memℓp_gen_iff (by norm_num : 0 < (2 : ℝ≥0∞).toReal) (f := f))
-- END SOURCE ch10_004

-- BEGIN SOURCE ch10_005
-- lp を型として使い、所属条件の証明を伴う標準基底ベクトルを作る
example (n : ℕ) : lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞) :=
  lp.single 2 n (1 : ℝ)
-- END SOURCE ch10_005

-- BEGIN SOURCE ch10_006
-- lp は NormedAddCommGroup のインスタンス
#check (inferInstance : NormedAddCommGroup (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)))

-- NormedAddCommGroup から MetricSpace が自動導出される
-- dist x y := ‖x - y‖
#check (inferInstance : MetricSpace (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)))
-- END SOURCE ch10_006

-- BEGIN SOURCE ch10_007
noncomputable example : MetricSpace (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)) := by
-- END SOURCE ch10_007

-- BEGIN SOURCE ch10_008
  exact inferInstance  -- No goals ✓
-- END SOURCE ch10_008

-- BEGIN SOURCE ch10_009
#check (inferInstance : CompleteSpace (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)))

-- 一般形では Fact (1 ≤ p) と各成分の完備性が必要
#check @lp.completeSpace
#check @lp.memℓp_of_tendsto
#check @lp.tendsto_lp_of_tendsto_pi
-- END SOURCE ch10_009

-- BEGIN SOURCE ch10_010
-- 10.0節の import と ell2 の定義の後に置く
#check ProperSpace
#check (inferInstance : ProperSpace ℝ)
-- ell2 については10.3節で ¬ ProperSpace ell2 を証明する。
-- END SOURCE ch10_010

-- BEGIN SOURCE ch10_011
-- 以降は10.0節の import・open scoped ENNReal・ell2 の定義に続けて置く
noncomputable def e (n : ℕ) : ell2 := lp.single 2 n 1

theorem norm_e (n : ℕ) : ‖e n‖ = 1 := by
  simp [e, lp.norm_single (by norm_num : (0 : ℝ≥0∞) < 2)]
-- END SOURCE ch10_011

-- BEGIN SOURCE ch10_012
theorem basis_separated (m n : ℕ) (hmn : m ≠ n) :
    1 ≤ dist (e m) (e n) := by
  have hcoord := lp.norm_apply_le_norm
    (by norm_num : (2 : ℝ≥0∞) ≠ 0) (e m - e n) m
  change ‖e m m - e n m‖ ≤ ‖e m - e n‖ at hcoord
  simpa [e, dist_eq_norm, lp.single_apply, hmn] using hcoord
-- END SOURCE ch10_012

-- BEGIN SOURCE ch10_013
theorem unitClosedBall_not_compact :
    ¬ IsCompact (Metric.closedBall (0 : ell2) 1) := by
  intro h
  have he (n : ℕ) : e n ∈ Metric.closedBall (0 : ell2) 1 := by
    simp [Metric.mem_closedBall, dist_zero_right, norm_e]
  obtain ⟨x, _, φ, hφ, hlim⟩ := h.isSeqCompact he
  obtain ⟨N, hN⟩ := Metric.cauchySeq_iff.mp hlim.cauchySeq 1 (by norm_num)
  have hlt := hN N (le_refl N) (N + 1) (by omega)
  have hge := basis_separated (φ N) (φ (N + 1))
    (ne_of_lt (hφ (Nat.lt_succ_self N)))
  exact (not_lt_of_ge hge) hlt

theorem ell2_not_proper : ¬ ProperSpace ell2 := by
  intro h
  exact unitClosedBall_not_compact (isCompact_closedBall (0 : ell2) 1)
-- END SOURCE ch10_013

-- BEGIN SOURCE ch10_014
-- ℓ² でも使えること
#check (inferInstance : MetricSpace ell2)     -- 距離の計算
#check (inferInstance : CompleteSpace ell2)   -- Cauchy 列は収束する
#check (inferInstance : NormedAddCommGroup ell2) -- ノルムの代数
-- → cauchySeq_tendsto_of_complete が使える
-- → dist_triangle（三角不等式）が使える
-- → 連続写像が定義できる
-- END SOURCE ch10_014

-- BEGIN SOURCE ch10_015
-- 10.3節の証明を使う
#check ell2_not_proper

theorem ell2_not_finiteDimensional : ¬ FiniteDimensional ℝ ell2 := by
  intro h
  exact ell2_not_proper (FiniteDimensional.proper ℝ ell2)

-- コンパクト集合に関する定理は ell2 内でも使える。
-- ただし単位閉球は、そのコンパクト性の仮定を満たさない。
-- END SOURCE ch10_015

-- BEGIN SOURCE ch10_016
-- ℓ² は内積空間（Hilbert 空間）
#check (inferInstance : Inner ℝ (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)))
#check (inferInstance : InnerProductSpace ℝ (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)))

-- Hilbert 空間 = 完備な内積空間
-- ℓ² は CompleteSpace + InnerProductSpace = Hilbert 空間
-- END SOURCE ch10_016

-- BEGIN SOURCE ch10_017
-- 10.0節から10.3節までの完成例の後に置く
section Chapter10Summary

example : ¬ ProperSpace ell2 := ell2_not_proper
example : CompleteSpace ell2 := inferInstance

example (a : ℕ → ell2) (ha : CauchySeq a) :
    ∃ L : ell2, Filter.Tendsto a Filter.atTop (nhds L) :=
  cauchySeq_tendsto_of_complete ha

end Chapter10Summary
-- END SOURCE ch10_017

-- BEGIN SOURCE ch10_018
-- 次章で使うMathlibのAPI（本章冒頭のimportを引き継ぐ）
#check ContractingWith
#check @ContractingWith.fixedPoint
#check @ContractingWith.fixedPoint_isFixedPt
#check @ContractingWith.fixedPoint_unique
#check @ContractingWith.tendsto_iterate_fixedPoint
-- END SOURCE ch10_018

-- BEGIN SOURCE ch10_019
#check (inferInstance : ProperSpace (EuclideanSpace ℝ (Fin 100)))
-- END SOURCE ch10_019

-- BEGIN SOURCE ch10_020
-- 10.3節の完成証明を使う
example : ¬ ProperSpace ell2 := ell2_not_proper
-- END SOURCE ch10_020

-- BEGIN SOURCE ch10_021
-- 無限次元の実ノルム空間について使う一般形
theorem notProperOfInfiniteDimensional {E : Type*}
    [NormedAddCommGroup E] [NormedSpace ℝ E]
    (h : ¬ FiniteDimensional ℝ E) : ¬ ProperSpace E := by
  intro hp
  exact h (FiniteDimensional.of_isCompact_closedBall ℝ
    (by norm_num : 0 < (1 : ℝ)) (isCompact_closedBall (0 : E) 1))
-- END SOURCE ch10_021

-- BEGIN SOURCE ch10_022
#check FiniteDimensional.proper
#check FiniteDimensional.of_isCompact_closedBall
-- END SOURCE ch10_022

-- BEGIN SOURCE ch10_024
-- 10.1節の mem_two_iff を使う
theorem reciprocal_mem_two :
    Memℓp (fun n : ℕ => (1 : ℝ) / (n + 1)) 2 := by
  rw [mem_two_iff]
  have hbase : Summable (fun n : ℕ => (1 : ℝ) / (n : ℝ) ^ 2) :=
    Real.summable_one_div_nat_pow.mpr (by norm_num)
  have hshift : Summable (fun n : ℕ => (1 : ℝ) / (n + 1) ^ 2) := by
    simpa only [Nat.cast_add, Nat.cast_one] using (summable_nat_add_iff 1).mpr hbase
  simpa only [Real.norm_eq_abs, sq_abs, div_pow, one_pow] using hshift
-- END SOURCE ch10_024

-- BEGIN SOURCE ch10_025
-- 添字のシフトを、単射による部分列として扱う別解
theorem reciprocal_mem_two_alt :
    Memℓp (fun n : ℕ => (1 : ℝ) / (n + 1)) 2 := by
  rw [mem_two_iff]
  have hbase : Summable (fun n : ℕ => (1 : ℝ) / (n : ℝ) ^ 2) :=
    Real.summable_one_div_nat_pow.mpr (by norm_num)
  have hshift : Summable (fun n : ℕ => (1 : ℝ) / (n + 1) ^ 2) := by
    simpa only [Function.comp_def, Nat.cast_succ] using
      hbase.comp_injective Nat.succ_injective
  simpa only [Real.norm_eq_abs, sq_abs, div_pow, one_pow] using hshift
-- END SOURCE ch10_025

-- BEGIN SOURCE ch10_026
-- Riesz表現定理による同型を確認する。弱収束そのものの証明ではない。
#check InnerProductSpace.toDual ℝ ell2
#check @lp.inner_single_right
-- END SOURCE ch10_026

end LeanBook.Ch10
