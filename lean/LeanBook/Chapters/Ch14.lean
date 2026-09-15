import Mathlib

namespace LeanBook.Ch14

-- BEGIN SOURCE ch14_005
open MeasureTheory

#check @MeasureTheory.ae
#check @Filter.EventuallyEq
#check @ae_iff

-- 実数値の指示関数としてディリクレ関数を書く。
theorem dirichlet_ae_zero :
    (Set.range ((↑) : ℚ → ℝ)).indicator (fun _ => (1 : ℝ)) =ᵐ[volume]
      (fun _ => 0) := by
  have hQ : ∀ᵐ x : ℝ ∂volume, x ∉ Set.range ((↑) : ℚ → ℝ) :=
    (Set.countable_range ((↑) : ℚ → ℝ)).ae_notMem volume
  filter_upwards [hQ] with x hx
  simp [Set.indicator_of_notMem hx]
-- END SOURCE ch14_005

-- BEGIN SOURCE ch14_006
-- 数学：μ-a.e. で P x ならば、任意の集合 S に対して (μ restricted to S)-a.e. で P x
#check @ae_restrict_of_ae
-- ae_restrict_of_ae :
--   (∀ᵐ x ∂μ, P x) → ∀ᵐ x ∂μ.restrict s, P x
-- END SOURCE ch14_006

-- BEGIN SOURCE ch14_007
example (f g : ℝ → ℝ) (h : f =ᵐ[volume] g) :
    f =ᵐ[volume.restrict (Set.Icc 0 1)] g := by
  exact ae_restrict_of_ae h
-- END SOURCE ch14_007

end LeanBook.Ch14
