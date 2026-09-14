import Mathlib

namespace LeanBook.Ch08

-- BEGIN SOURCE ch08_018

-- 実数の閉区間はコンパクト
example (a b : ℝ) : IsCompact (Set.Icc a b) := isCompact_Icc

-- 距離空間で ProperSpace を仮定した Heine–Borel 型の同値
theorem compactIffClosedBounded {X : Type*} [MetricSpace X] [ProperSpace X]
    (s : Set X) : IsCompact s ↔ IsClosed s ∧ Bornology.IsBounded s :=
  Metric.isCompact_iff_isClosed_bounded

#check IsCompact.isSeqCompact
-- END SOURCE ch08_018

-- BEGIN SOURCE ch08_019

#check ProperSpace
#check (inferInstance : ProperSpace ℝ)
#check (inferInstance : ProperSpace (EuclideanSpace ℝ (Fin 3)))
#check @Metric.isCompact_iff_isClosed_bounded
-- END SOURCE ch08_019

end LeanBook.Ch08
