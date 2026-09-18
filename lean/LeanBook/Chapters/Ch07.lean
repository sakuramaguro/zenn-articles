import Mathlib

namespace LeanBook.Ch07

-- BEGIN SOURCE ch07_001
-- 本章の最終ゴール（これを証明できるようになることが目標）

-- 【勝利の命題①】開球は開集合である
theorem open_ball_preview (X : Type*) [MetricSpace X] (x : X) (r : ℝ) :
    IsOpen (Metric.ball x r) := by
  exact Metric.isOpen_ball

-- 【勝利の命題②】点を除かない極限の ε-δ による特徴付け（b = f a なら連続性）
theorem tendsto_epsilon_delta_preview (f : ℝ → ℝ) (a b : ℝ) :
    Filter.Tendsto f (nhds a) (nhds b) ↔
    ∀ ε > 0, ∃ δ > 0, ∀ x, dist x a < δ → dist (f x) b < ε := by
  exact Metric.tendsto_nhds_nhds
-- END SOURCE ch07_001

-- BEGIN SOURCE ch07_002

-- 固定版 Mathlib のフィールドを実際に表示する
#print PseudoMetricSpace
#print MetricSpace
#check @dist_self
#check @eq_of_dist_eq_zero
-- END SOURCE ch07_002

-- BEGIN SOURCE ch07_003

-- 実際に #check で確認
#check @dist_nonneg
-- dist_nonneg : ∀ {α : Type u_1} [inst : PseudoMetricSpace α] {x y : α}, 0 ≤ dist x y

#check @dist_comm
-- dist_comm : ∀ {α : Type u_1} [inst : PseudoMetricSpace α] (x y : α),
--   dist x y = dist y x

#check @dist_triangle
-- dist_triangle : ∀ {α : Type u_1} [inst : PseudoMetricSpace α] (x y z : α),
--   dist x z ≤ dist x y + dist y z
-- END SOURCE ch07_003

-- BEGIN SOURCE ch07_004

-- ℝ は MetricSpace のインスタンス
#check (inferInstance : MetricSpace ℝ)

-- ℝ での dist は絶対値
#check Real.dist_eq
-- Real.dist_eq : dist x y = |x - y|

-- 実際に計算
theorem real_distance : dist (3 : ℝ) 5 = 2 := by
  rw [Real.dist_eq]
  -- ⊢ |3 - 5| = 2  →  norm_num で解決
  norm_num

-- 三角不等式の確認
theorem real_triangle (x y z : ℝ) : dist x z ≤ dist x y + dist y z :=
  dist_triangle x y z  -- 公理そのまま
-- END SOURCE ch07_004

-- BEGIN SOURCE ch07_005

-- 数学：B(x, r) = { y | d(x, y) < r }
-- Lean：Metric.ball x r
#check @Metric.ball
-- Metric.ball : α → ℝ → Set α
-- Metric.ball x r = {y | dist y x < r}

-- 数学：B̄(x, r) = { y | d(x, y) ≤ r }
-- Lean：Metric.closedBall x r
#check @Metric.closedBall
-- Metric.closedBall x r = {y | dist y x ≤ r}
-- END SOURCE ch07_005

-- BEGIN SOURCE ch07_006

-- Metric.ball のメンバーシップ条件を確認
#check @Metric.mem_ball
-- Metric.mem_ball : y ∈ Metric.ball x r ↔ dist y x < r

-- 具体例：2 は ball 0 3 に属するか？
theorem two_mem_ball : (2 : ℝ) ∈ Metric.ball 0 3 := by
  rw [Metric.mem_ball]
  -- ⊢ dist 2 0 < 3
  norm_num [Real.dist_eq]
  -- No goals ✓
-- END SOURCE ch07_006

-- BEGIN SOURCE ch07_007

theorem two_mem_ball_steps : (2 : ℝ) ∈ Metric.ball 0 3 := by
-- END SOURCE ch07_007

-- BEGIN SOURCE ch07_008
  rw [Metric.mem_ball]
-- END SOURCE ch07_008

-- BEGIN SOURCE ch07_009
  norm_num [Real.dist_eq]
  -- dist 2 0 = |2 - 0| = 2 < 3 ✓
  -- No goals ✓
-- END SOURCE ch07_009

-- BEGIN SOURCE ch07_010

#check Filter.HasBasis
-- Filter.HasBasis : Filter α → (ι → Prop) → (ι → Set α) → Prop
-- f.HasBasis p s は「フィルター f の基底が {s i | p i} である」を意味する
-- END SOURCE ch07_010

-- BEGIN SOURCE ch07_011

#check @Metric.nhds_basis_ball
-- Metric.nhds_basis_ball :
--   (nhds x).HasBasis (fun ε => 0 < ε) (Metric.ball x)
-- END SOURCE ch07_011

-- BEGIN SOURCE ch07_012

-- U が a の近傍であるための必要十分条件
theorem nhds_iff_ball (a : ℝ) (U : Set ℝ) :
    U ∈ nhds a ↔ ∃ ε > 0, Metric.ball a ε ⊆ U := by
  rw [Metric.nhds_basis_ball.mem_iff]
  -- No goals：同じ式の同値になるため rw が閉じる
-- END SOURCE ch07_012

-- BEGIN SOURCE ch07_013

theorem nhds_iff_ball_steps (a : ℝ) (U : Set ℝ) :
    U ∈ nhds a ↔ ∃ ε > 0, Metric.ball a ε ⊆ U := by
-- END SOURCE ch07_013

-- BEGIN SOURCE ch07_014
  rw [Metric.nhds_basis_ball.mem_iff]
-- END SOURCE ch07_014

-- BEGIN SOURCE ch07_015

-- IsOpen の定義確認
#check @IsOpen
-- IsOpen : Set α → Prop

-- 距離空間での開集合の特徴付け
#check Metric.isOpen_iff
-- Metric.isOpen_iff :
--   IsOpen s ↔ ∀ x ∈ s, ∃ ε > 0, Metric.ball x ε ⊆ s
-- END SOURCE ch07_015

-- BEGIN SOURCE ch07_016

-- 目標：開球は開集合
theorem open_ball_from_triangle (X : Type*) [MetricSpace X] (x : X) (r : ℝ) :
    IsOpen (Metric.ball x r) := by
-- END SOURCE ch07_016

-- BEGIN SOURCE ch07_017
  rw [Metric.isOpen_iff]
-- END SOURCE ch07_017

-- BEGIN SOURCE ch07_018
  intro y hy
-- END SOURCE ch07_018

-- BEGIN SOURCE ch07_019
  rw [Metric.mem_ball] at hy
-- END SOURCE ch07_019

-- BEGIN SOURCE ch07_020
  refine ⟨r - dist y x, by linarith, ?_⟩
-- END SOURCE ch07_020

-- BEGIN SOURCE ch07_021
  intro z hz
  rw [Metric.mem_ball] at hz ⊢
-- END SOURCE ch07_021

-- BEGIN SOURCE ch07_022
  calc dist z x ≤ dist z y + dist y x := dist_triangle z y x
    _ < (r - dist y x) + dist y x    := by linarith
    _ = r                             := by ring
  -- No goals ✓
-- END SOURCE ch07_022

-- BEGIN SOURCE ch07_023

-- 実はMathlib に既に定理がある
theorem open_ball_library (X : Type*) [MetricSpace X] (x : X) (r : ℝ) :
    IsOpen (Metric.ball x r) :=
  Metric.isOpen_ball  -- ← 一行で終わる
-- END SOURCE ch07_023

-- BEGIN SOURCE ch07_024

#check @Metric.tendsto_nhds_nhds
-- Metric.tendsto_nhds_nhds :
--   Tendsto f (nhds a) (nhds b) ↔
--   ∀ ε > 0, ∃ δ > 0, ∀ ⦃x⦄, dist x a < δ → dist (f x) b < ε
-- END SOURCE ch07_024

-- BEGIN SOURCE ch07_025

-- フィルターの基底を使った Tendsto の特徴付け
#check Filter.HasBasis.tendsto_iff
-- HasBasis.tendsto_iff :
--   l.HasBasis p s → m.HasBasis q t →
--   (Tendsto f l m ↔ ∀ i, q i → ∃ j, p j ∧ ∀ x ∈ s j, f x ∈ t i)
-- END SOURCE ch07_025

-- BEGIN SOURCE ch07_026

-- 実際に Metric.tendsto_nhds_nhds を使った証明の実況
theorem tendsto_to_epsilon_delta (f : ℝ → ℝ) (a b : ℝ) (hf : Filter.Tendsto f (nhds a) (nhds b)) :
    ∀ ε > 0, ∃ δ > 0, ∀ x, dist x a < δ → dist (f x) b < ε := by
-- END SOURCE ch07_026

-- BEGIN SOURCE ch07_027
  exact Metric.tendsto_nhds_nhds.mp hf
  -- No goals ✓
-- END SOURCE ch07_027

-- BEGIN SOURCE ch07_028

-- 三者の同値を一気に確認
#check @Metric.continuousAt_iff
-- Metric.continuousAt_iff :
--   ContinuousAt f x ↔
--   ∀ ε > 0, ∃ δ > 0, ∀ ⦃y⦄, dist y x < δ → dist (f y) (f x) < ε
-- END SOURCE ch07_028

-- BEGIN SOURCE ch07_029

-- x² は ℝ 上の連続関数
theorem square_continuous : Continuous (fun x : ℝ => x ^ 2) := by
-- END SOURCE ch07_029

-- BEGIN SOURCE ch07_030
  exact continuous_pow 2
  -- No goals ✓
-- END SOURCE ch07_030

-- BEGIN SOURCE ch07_031

-- もう少し手動で：恒等写像の連続性から組み立てる
theorem square_continuous_from_id : Continuous (fun x : ℝ => x ^ 2) := by
  have hid : Continuous (id : ℝ → ℝ) := continuous_id
  -- id は連続。x^2 = id * id なのでどうするか？
  exact hid.pow 2  -- Continuous.pow : Continuous f → Continuous (fun x => f x ^ n)
  -- No goals ✓
-- END SOURCE ch07_031

-- BEGIN SOURCE ch07_032

-- ユークリッド空間でも同じ開球の定理を使える
theorem euclidean_ball_open (n : ℕ) (x : EuclideanSpace ℝ (Fin n)) (r : ℝ) :
    IsOpen (Metric.ball x r) :=
  Metric.isOpen_ball

theorem euclidean_continuous_tendsto
    (f : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 2))
    (hf : Continuous f) (a : EuclideanSpace ℝ (Fin 3)) :
    Filter.Tendsto f (nhds a) (nhds (f a)) :=
  hf.continuousAt
-- END SOURCE ch07_032

-- BEGIN SOURCE ch07_033

-- (a) d(x, y) = d(y, x)
#check @dist_comm
-- dist_comm : ∀ {α} [PseudoMetricSpace α] (x y : α), dist x y = dist y x
-- Lean の表現: dist x y = dist y x（補題名: dist_comm）

-- (b) B(a, ε) = {x | |x - a| < ε}
#check @Metric.ball
-- Metric.ball : α → ℝ → Set α
-- Metric.ball a ε = {x | dist x a < ε}
-- ℝ では dist x a = |x - a| なので数学の定義と一致

-- (c) f が a で連続（ε-δ 定義）
theorem continuousAt_epsilon_delta (f : ℝ → ℝ) (a : ℝ) :
    ContinuousAt f a ↔
    ∀ ε > 0, ∃ δ > 0, ∀ x, dist x a < δ → dist (f x) (f a) < ε := by
  exact Metric.continuousAt_iff
-- END SOURCE ch07_033

-- BEGIN SOURCE ch07_034

#check @Metric.mem_ball
-- Metric.mem_ball : x ∈ Metric.ball a ε ↔ dist x a < ε

-- 実数上の開球の集合としての等式も確認する
theorem real_ball_eq (a ε : ℝ) :
    Metric.ball a ε = {x : ℝ | |x - a| < ε} := by
  ext x
  simp only [Metric.mem_ball, Set.mem_setOf_eq, Real.dist_eq]
-- END SOURCE ch07_034

-- BEGIN SOURCE ch07_036

-- 閉球は閉集合
theorem closedBall_closed (X : Type*) [MetricSpace X] (x : X) (r : ℝ) :
    IsClosed (Metric.closedBall x r) := by
  exact Metric.isClosed_closedBall
  -- No goals ✓
-- END SOURCE ch07_036

-- BEGIN SOURCE ch07_037

-- 距離関数の連続性と、閉集合の逆像を使う別解
theorem closedBall_closed_preimage (X : Type*) [MetricSpace X] (x : X) (r : ℝ) :
    IsClosed (Metric.closedBall x r) := by
  change IsClosed ((fun y : X => dist y x) ⁻¹' Set.Iic r)
  exact isClosed_Iic.preimage (continuous_id.dist continuous_const)
-- END SOURCE ch07_037

-- BEGIN SOURCE ch07_038

-- D3（三角不等式）の反例
theorem square_difference_not_metric : ¬ (∀ x y z : ℝ, (x - z)^2 ≤ (x - y)^2 + (y - z)^2) := by
  intro h
  have := h 0 1 2
  norm_num at this
  -- No goals ✓
-- END SOURCE ch07_038

-- BEGIN SOURCE ch07_039

-- 有理数の具体的な不等式を norm_num で否定する
theorem square_difference_rational_counterexample : ¬ ((0 - 2 : ℚ)^2 ≤ (0 - 1 : ℚ)^2 + (1 - 2 : ℚ)^2) := by
  norm_num
-- END SOURCE ch07_039

-- BEGIN SOURCE ch07_040

inductive TwoPoint | left | right

noncomputable instance : PseudoMetricSpace TwoPoint :=
  PseudoMetricSpace.induced (fun _ => (0 : ℝ)) inferInstance

theorem zeroDistanceDistinct :
    dist TwoPoint.left TwoPoint.right = 0 ∧ TwoPoint.left ≠ TwoPoint.right := by
  constructor
  · change dist (0 : ℝ) 0 = 0
    exact dist_self 0
  · intro h
    cases h
-- END SOURCE ch07_040

-- BEGIN SOURCE ch07_041
theorem zeroDistanceNotSeparating :
    ¬ (∀ x y : TwoPoint, dist x y = 0 → x = y) := by
  intro h
  exact zeroDistanceDistinct.2 (h _ _ zeroDistanceDistinct.1)
-- END SOURCE ch07_041

end LeanBook.Ch07
