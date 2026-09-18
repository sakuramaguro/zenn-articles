import Mathlib

namespace LeanBook.Intro

-- BEGIN SOURCE intro_001
open MeasureTheory

-- Part 4への準備（予告）：確率微分方程式の登場人物たち
-- 数学：(Ω, ℱ, P) が確率空間、X : Ω → ℝ が確率変数
variable (Ω : Type*) [MeasurableSpace Ω]
         (P : Measure Ω) [IsProbabilityMeasure P]
-- Part 1でこのコードが「何を言っているか」が分かるようになります
-- END SOURCE intro_001

end LeanBook.Intro
