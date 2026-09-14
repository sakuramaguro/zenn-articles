import Mathlib

namespace LeanBook.Ch06

-- BEGIN SOURCE ch06_004

-- 内側の f は a で、外側の g は f a で連続と仮定する
theorem continuousCompositionEpsilonDelta (f g : ℝ → ℝ) (a : ℝ)
    (hf : ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ, |x - a| < δ → |f x - f a| < ε)
    (hg : ∀ ε > 0, ∃ δ > 0, ∀ y : ℝ, |y - f a| < δ → |g y - g (f a)| < ε) :
    ∀ ε > 0, ∃ δ > 0, ∀ x : ℝ,
      |x - a| < δ → |(g ∘ f) x - (g ∘ f) a| < ε := by
  intro ε hε
  obtain ⟨η, hη, hgη⟩ := hg ε hε
  obtain ⟨δ, hδ, hfδ⟩ := hf η hη
  exact ⟨δ, hδ, fun x hx => hgη (f x) (hfδ x hx)⟩
-- END SOURCE ch06_004

end LeanBook.Ch06
