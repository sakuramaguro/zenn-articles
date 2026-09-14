import Mathlib

namespace LeanBook.Ch10

-- BEGIN SOURCE ch10_001
open scoped ENNReal

-- 本章では ℓ² の型を ell2 と名付ける
abbrev ell2 := lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)

#check (inferInstance : MetricSpace ell2)
#check (inferInstance : CompleteSpace ell2)

-- もう一つのゴール：単位閉球の非コンパクト性を証明し、
-- ¬ ProperSpace ell2 を導く（5.3節の完成証明）。
-- END SOURCE ch10_001

-- BEGIN SOURCE ch10_005
-- 具体的な元の確認
-- e_n : n 番目だけ 1、残りは 0（標準基底ベクトル）
-- lp は型（Type）なので ∈ ではなく : で型宣言する
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
noncomputable example : MetricSpace (lp (fun _ : ℕ => ℝ) (2 : ℝ≥0∞)) := inferInstance
-- END SOURCE ch10_007

-- BEGIN SOURCE ch10_010
-- 5.0節の import と ell2 の定義の後に置く
#check ProperSpace
#check (inferInstance : ProperSpace ℝ)
-- ell2 については5.3節で ¬ ProperSpace ell2 を証明する。
-- END SOURCE ch10_010

-- BEGIN SOURCE ch10_011
-- 以降は5.0節の import・open scoped ENNReal・ell2 の定義に続けて置く
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
-- 5.3節の証明を使う
#check ell2_not_proper

theorem ell2_not_finiteDimensional : ¬ FiniteDimensional ℝ ell2 := by
  intro h
  exact ell2_not_proper (FiniteDimensional.proper ℝ ell2)

-- コンパクト集合に関する定理は ell2 内でも使える。
-- ただし単位閉球は、そのコンパクト性の仮定を満たさない。
-- END SOURCE ch10_015

-- BEGIN SOURCE ch10_017
-- 5.0節から5.3節までの完成例の後に置く
section Chapter5Summary

example : ¬ ProperSpace ell2 := ell2_not_proper
example : CompleteSpace ell2 := inferInstance

example (a : ℕ → ell2) (ha : CauchySeq a) :
    ∃ L : ell2, Filter.Tendsto a Filter.atTop (nhds L) :=
  cauchySeq_tendsto_of_complete ha

end Chapter5Summary
-- END SOURCE ch10_017

-- BEGIN SOURCE ch10_019
#check (inferInstance : ProperSpace (EuclideanSpace ℝ (Fin 100)))
-- END SOURCE ch10_019

-- BEGIN SOURCE ch10_020
-- 5.3節の完成証明を使う
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

end LeanBook.Ch10
