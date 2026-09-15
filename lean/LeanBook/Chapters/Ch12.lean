import Mathlib

namespace LeanBook.Ch12

-- BEGIN SOURCE ch12_001
open scoped NNReal

-- 非空な完備距離空間 ℝ 上で、縮小性から一意存在を得る
theorem half_map_recap : ∃! z : ℝ, (fun x : ℝ => x / 2) z = z := by
  have hf : ContractingWith (1 / 2 : ℝ≥0) (fun x : ℝ => x / 2) := by
    refine ⟨by norm_num, LipschitzWith.of_dist_le_mul fun x y => ?_⟩
    simp only [Real.dist_eq]
    rw [← sub_div, abs_div]
    norm_num
    ring_nf
    exact le_rfl
  refine ⟨hf.fixedPoint (fun x : ℝ => x / 2), hf.fixedPoint_isFixedPt, ?_⟩
  intro y hy
  exact hf.fixedPoint_unique hy
-- END SOURCE ch12_001

-- BEGIN SOURCE ch12_002
open MeasureTheory Filter
open scoped ENNReal Topology

-- 第3巻の到達点：既存の収束定理を、仮定を確認して適用する。
#check @lintegral_iSup
-- 非負可測関数列 + 各点で単調増加 → 上限と非負積分の交換。
#check @lintegral_liminf_le
#check @lintegral_liminf_le'
-- Measurable 版と AEMeasurable 版。結論は等号ではなく不等式。
#check @tendsto_integral_of_dominated_convergence
-- 実数値の例では、各項のAE 強可測性、可積分な優関数、
-- ノルムのAE 支配、AE 収束を揃えると、積分列の収束が得られる。
-- 引数の順：bound hFm hbound hle htends。
-- END SOURCE ch12_002

end LeanBook.Ch12
