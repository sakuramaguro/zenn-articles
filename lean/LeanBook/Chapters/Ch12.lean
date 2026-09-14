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

end LeanBook.Ch12
