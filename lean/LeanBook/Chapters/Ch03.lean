import Mathlib

namespace LeanBook.Ch03

-- BEGIN SOURCE ch03_001

-- ゴール①：rfl が失敗するケースを自力で読み、ring で修正できる
-- 数学：a + b = b + a（交換法則）/ Lean：rfl では解けない、ring が必要
example (a b : ℕ) : a + b = b + a := by
  ring
  -- No goals ✓

-- ゴール②：型クラスエラーを自力で読み、[Add α] を追加して修正できる
-- 数学：「型 α に足し算は定義されているか？」/ Lean：[Add α] という免許証が必要
variable (α : Type) [Add α] (a b : α)
#check a + b  -- a + b : α

-- ゴール③：sorry で作った骨格を、実際の証明で埋められる
-- 数学：未証明の課題を切り分け、一つずつ証明する
-- Lean：以下は sorry を取り除いた完成例
theorem skeleton (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  have step1 : a ≤ b := h1
  have step2 : b ≤ c := h2
  linarith
  -- No goals ✓
-- END SOURCE ch03_001

-- BEGIN SOURCE ch03_005

theorem one_add_one_ne_three : (1 : ℕ) + 1 ≠ 3 := by
  norm_num
-- END SOURCE ch03_005

-- BEGIN SOURCE ch03_015

theorem hard_proof (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  have step1 : a ≤ b := h1    -- sorry → h1 に置き換え
  have step2 : b ≤ c := h2    -- sorry → h2 に置き換え
  linarith                    -- sorry → linarith に置き換え
  -- No goals ✓

#print axioms hard_proof
-- END SOURCE ch03_015

end LeanBook.Ch03
