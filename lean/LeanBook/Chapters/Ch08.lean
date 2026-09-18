import Mathlib

namespace LeanBook.Ch08

-- BEGIN SOURCE ch08_001

open Filter Topology

-- 連続性の合成は位相空間で成り立つ
theorem composition_goal (X Y Z : Type*)
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]
    (f : X → Y) (g : Y → Z) (hf : Continuous f) (hg : Continuous g) :
    Continuous (g ∘ f) := hg.comp hf

-- 非空なコンパクト集合上の実数値連続関数は最大値を達成する
theorem maximum_goal (f : ℝ → ℝ) (hf : Continuous f) (s : Set ℝ)
    (hs : IsCompact s) (hne : s.Nonempty) :
    ∃ x ∈ s, ∀ y ∈ s, f y ≤ f x := by
  obtain ⟨x, hx, hmax⟩ := hs.exists_isMaxOn hne hf.continuousOn
  exact ⟨x, hx, fun y hy => hmax hy⟩
-- END SOURCE ch08_001

-- BEGIN SOURCE ch08_002

open Filter Topology

-- 定義を表示し、実際のフィールドを調べる
#print TopologicalSpace
-- IsOpen・isOpen_univ・isOpen_inter・isOpen_sUnion を持つ。
-- isOpen_empty はフィールドではなく、任意合併から導く補題。
-- END SOURCE ch08_002

-- BEGIN SOURCE ch08_003

open Filter Topology

theorem empty_open_from_union (α : Type*) [TopologicalSpace α] :
    IsOpen (∅ : Set α) := by
  have : (∅ : Set α) = ⋃₀ (∅ : Set (Set α)) := by simp
  rw [this]
  exact isOpen_sUnion (fun t ht => ht.elim)
-- END SOURCE ch08_003

-- BEGIN SOURCE ch08_004

open Filter Topology

#check @isOpen_univ
#check @isOpen_empty
#check @IsOpen.inter
#check @IsOpen.union     -- 2つの開集合の合併
#check @isOpen_iUnion    -- 添字付きの任意合併
#check @isOpen_sUnion    -- 集合族の任意合併
-- END SOURCE ch08_004

-- BEGIN SOURCE ch08_005

open Filter Topology

#check (inferInstance : TopologicalSpace ℝ)
#check (fun (X : Type) [MetricSpace X] => (inferInstance : TopologicalSpace X))
-- END SOURCE ch08_005

-- BEGIN SOURCE ch08_006

open Filter Topology

#check @Continuous
#check @continuous_def
-- Continuous f ↔ ∀ s, IsOpen s → IsOpen (f ⁻¹' s)
-- END SOURCE ch08_006

-- BEGIN SOURCE ch08_007

open Filter Topology

#check @Metric.continuousAt_iff
#check @continuous_iff_continuousAt
#check @continuous_def

theorem continuous_at_every_point (X Y : Type*)
    [TopologicalSpace X] [TopologicalSpace Y] (f : X → Y) :
    (∀ x, ContinuousAt f x) ↔ ∀ s, IsOpen s → IsOpen (f ⁻¹' s) := by
  rw [← continuous_iff_continuousAt, ← continuous_def]
-- END SOURCE ch08_007

-- BEGIN SOURCE ch08_008

open Filter Topology

#check Filter.principal
#check nhds_def

-- 下界である：各開近傍の主フィルターより細かい。
theorem nhds_le_open_principal (a : ℝ) (s : Set ℝ) (ha : a ∈ s) (hs : IsOpen s) :
    nhds a ≤ Filter.principal s := by
  rw [nhds_def]
  exact iInf_le_of_le s (iInf_le_of_le ⟨ha, hs⟩ le_rfl)

-- 最大の下界である：どの共通の下界も nhds a 以下になる。
theorem le_nhds_from_open_principals (f : Filter ℝ) (a : ℝ)
    (h : ∀ s, a ∈ s → IsOpen s → f ≤ Filter.principal s) : f ≤ nhds a := by
  rw [nhds_def]
  exact le_iInf fun s => le_iInf fun hs => h s hs.1 hs.2
-- END SOURCE ch08_008

-- BEGIN SOURCE ch08_009

open Filter Topology

theorem neighborhood_infimum (a : ℝ) :
    nhds a = ⨅ s ∈ {s : Set ℝ | a ∈ s ∧ IsOpen s}, Filter.principal s := by
  exact nhds_def a
-- END SOURCE ch08_009

-- BEGIN SOURCE ch08_010

open Filter Topology

theorem composition_by_preimages (X Y Z : Type*)
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]
    (f : X → Y) (g : Y → Z) (hf : Continuous f) (hg : Continuous g) :
    Continuous (g ∘ f) := by
-- END SOURCE ch08_010

-- BEGIN SOURCE ch08_011
  rw [continuous_def]
-- END SOURCE ch08_011

-- BEGIN SOURCE ch08_012
  intro s hs
-- END SOURCE ch08_012

-- BEGIN SOURCE ch08_013
  simp only [Set.preimage_comp]
-- END SOURCE ch08_013

-- BEGIN SOURCE ch08_014
  apply hf.isOpen_preimage (g ⁻¹' s)
  exact hg.isOpen_preimage s hs
-- END SOURCE ch08_014

-- BEGIN SOURCE ch08_015

open Filter Topology

#check Continuous.isOpen_preimage
-- hf.isOpen_preimage s hs のように、集合 s も明示的に渡す。
-- END SOURCE ch08_015

-- BEGIN SOURCE ch08_016

open Filter Topology

theorem composition_one_line (X Y Z : Type*)
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]
    (f : X → Y) (g : Y → Z) (hf : Continuous f) (hg : Continuous g) :
    Continuous (g ∘ f) := hg.comp hf
-- END SOURCE ch08_016

-- BEGIN SOURCE ch08_017

open Filter Topology

#print IsCompact
#check IsCompact.elim_finite_subcover
-- IsCompact の定義はフィルターによる。
-- elim_finite_subcover は、開被覆から有限部分被覆を取り出す定理。
-- END SOURCE ch08_017

-- BEGIN SOURCE ch08_018

open Filter Topology

-- 実数の閉区間はコンパクト
theorem compact_interval (a b : ℝ) : IsCompact (Set.Icc a b) := isCompact_Icc

-- 距離空間で ProperSpace を仮定した Heine–Borel 型の同値
theorem compactIffClosedBounded {X : Type*} [MetricSpace X] [ProperSpace X]
    (s : Set X) : IsCompact s ↔ IsClosed s ∧ Bornology.IsBounded s :=
  Metric.isCompact_iff_isClosed_bounded

#check IsCompact.isSeqCompact
-- END SOURCE ch08_018

-- BEGIN SOURCE ch08_019

open Filter Topology

#check ProperSpace
#check (inferInstance : ProperSpace ℝ)
#check (inferInstance : ProperSpace (EuclideanSpace ℝ (Fin 3)))
#check @Metric.isCompact_iff_isClosed_bounded
-- END SOURCE ch08_019

-- BEGIN SOURCE ch08_020

open Filter Topology

#check @IsClosed
#check @isOpen_compl_iff
#check @interior
#check @mem_interior
#check @closure
#check @mem_closure_iff
-- 内部：最大の開部分集合。閉包：最小の閉上位集合。
-- END SOURCE ch08_020

-- BEGIN SOURCE ch08_021

open Filter Topology

theorem closed_iff_open_complement (s : Set ℝ) : IsClosed s ↔ IsOpen sᶜ := by
-- END SOURCE ch08_021

-- BEGIN SOURCE ch08_022
  exact isOpen_compl_iff.symm
-- END SOURCE ch08_022

-- BEGIN SOURCE ch08_023

open Filter Topology

#check IsCompact.exists_isMaxOn
-- hs : IsCompact s, hne : s.Nonempty, hf : ContinuousOn f s から
-- ∃ x ∈ s, IsMaxOn f s x を得る。

theorem no_maximizer_in_empty (f : ℝ → ℝ) :
    ¬ ∃ x ∈ (∅ : Set ℝ), ∀ y ∈ (∅ : Set ℝ), f y ≤ f x := by
  simp
-- END SOURCE ch08_023

-- BEGIN SOURCE ch08_024

open Filter Topology

theorem square_maximum :
    ∃ x ∈ Set.Icc (0 : ℝ) 1, ∀ y ∈ Set.Icc (0 : ℝ) 1, y ^ 2 ≤ x ^ 2 := by
-- END SOURCE ch08_024

-- BEGIN SOURCE ch08_025
  have hne : (Set.Icc (0 : ℝ) 1).Nonempty := by
-- END SOURCE ch08_025

-- BEGIN SOURCE ch08_026
    exact Set.nonempty_Icc.mpr (by norm_num)
-- END SOURCE ch08_026

-- BEGIN SOURCE ch08_027
  have hcont : ContinuousOn (fun x : ℝ => x ^ 2) (Set.Icc 0 1) :=
    (continuous_pow 2).continuousOn
  obtain ⟨x, hx, hmax⟩ := isCompact_Icc.exists_isMaxOn hne hcont
  exact ⟨x, hx, fun y hy => hmax hy⟩
-- END SOURCE ch08_027

-- BEGIN SOURCE ch08_028

open Filter Topology

theorem continuous_preimage_iff (f : ℝ → ℝ) :
    Continuous f ↔ ∀ s, IsOpen s → IsOpen (f ⁻¹' s) := continuous_def

#check isCompact_Icc (a := (0 : ℝ)) (b := 1)

theorem closure_by_distance (x : ℝ) (S : Set ℝ) :
    x ∈ closure S ↔ ∀ ε > 0, ∃ y ∈ S, dist x y < ε := Metric.mem_closure_iff
-- END SOURCE ch08_028

-- BEGIN SOURCE ch08_029

open Filter Topology

#check @mem_closure_iff_nhds
#check @closure_eq_cluster_pts
-- END SOURCE ch08_029

-- BEGIN SOURCE ch08_031

open Filter Topology

-- 閉区間 [a, b] 上の連続関数は最小値を持つ
theorem minimum_interval (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) (hab : a ≤ b) :
    ∃ x ∈ Set.Icc a b, ∀ y ∈ Set.Icc a b, f x ≤ f y := by
  -- ステップ①：[a,b] はコンパクト
  have hK : IsCompact (Set.Icc a b) := isCompact_Icc
  -- ステップ②：[a,b] は空でない（a ≤ b より）
  have hne : (Set.Icc a b).Nonempty := Set.nonempty_Icc.mpr hab
  -- ステップ③：コンパクト集合上の連続関数は最小値を達成する
  obtain ⟨x, hx, hxmin⟩ := hK.exists_isMinOn hne hf.continuousOn
  -- IsMinOn f K x ↔ ∀ y ∈ K, f x ≤ f y
  exact ⟨x, hx, fun y hy => hxmin hy⟩
  -- No goals ✓
-- END SOURCE ch08_031

-- BEGIN SOURCE ch08_032

open Filter Topology

theorem minimum_interval_term (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ) (hab : a ≤ b) :
    ∃ x ∈ Set.Icc a b, ∀ y ∈ Set.Icc a b, f x ≤ f y :=
  -- 一行版：exists_isMinOn をパイプラインで繋ぐ
  let ⟨x, hx, hm⟩ := isCompact_Icc.exists_isMinOn
    (Set.nonempty_Icc.mpr hab) hf.continuousOn
  ⟨x, hx, fun y hy => hm (a := y) hy⟩
-- END SOURCE ch08_032

-- BEGIN SOURCE ch08_034

open Filter Topology

-- すべての部分集合を開と定め、構造の各公理を証明する。
@[reducible]
def allOpenTopology (α : Type*) : TopologicalSpace α where
  IsOpen _ := True
  isOpen_univ := True.intro
  isOpen_inter _ _ _ _ := True.intro
  isOpen_sUnion _ _ := True.intro

-- ℕに既に登録された離散位相を使う例。
theorem singleton_open_discrete : IsOpen ({0} : Set ℕ) := by
  exact isOpen_discrete {0}
-- END SOURCE ch08_034

-- BEGIN SOURCE ch08_035

open Filter Topology

theorem singleton_open_apply : IsOpen ({0} : Set ℕ) := by
  apply isOpen_discrete
-- END SOURCE ch08_035

-- BEGIN SOURCE ch08_036

open Filter Topology

theorem singleton_open_simp : IsOpen ({0} : Set ℕ) := by
  simp only [isOpen_discrete]
-- END SOURCE ch08_036

end LeanBook.Ch08
