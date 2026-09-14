import Mathlib

namespace LeanBook.Ch07

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
