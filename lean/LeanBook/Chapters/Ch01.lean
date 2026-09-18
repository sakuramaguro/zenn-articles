import Mathlib

namespace LeanBook.Ch01

-- BEGIN SOURCE ch01_001

-- ゴール①：環境確認 ── #eval で Hello World
#eval "Hello, Lean!"
-- 出力："Hello, Lean!"

-- ゴール②：#check で型を調べる
-- 数学：命題「1 + 1 = 2」の「型」は何か / Lean：Prop（命題型）
#check (1 + 1 = 2)
-- 出力：1 + 1 = 2 : Prop

-- ゴール③：最初の定理証明
-- 数学：1 + 1 = 2 を証明する / Lean：norm_num タクティクで解決
theorem first_theorem : 1 + 1 = 2 := by
  norm_num
  -- No goals ✓
-- END SOURCE ch01_001

-- BEGIN SOURCE ch01_002
#eval "Hello, Lean!"
-- END SOURCE ch01_002

-- BEGIN SOURCE ch01_003

-- 数値の型を調べる
-- 数学：42 は自然数 / Lean：42 : ℕ
#check 42          -- 42 : ℕ
#check (3.14 : ℝ)  -- 3.14 : ℝ
#check "hello"     -- "hello" : String

-- 命題（数学的な主張）の型を調べる
-- 数学：「1 + 1 = 2」という主張そのものの「型」/ Lean：Prop（命題型）
#check (1 + 1 = 2)          -- 1 + 1 = 2 : Prop
#check (∀ n : ℕ, n ≥ 0)    -- ∀ n, n ≥ 0 : Prop
-- END SOURCE ch01_003

-- BEGIN SOURCE ch01_004

-- example：名前のない証明（動作確認・練習問題に使う）
-- 数学：1 + 1 = 2 を証明する（名前なし）/ Lean：example
example : 1 + 1 = 2 := by norm_num

-- theorem：名前のある証明（後から apply で再利用できる）
-- 数学：定理 one_plus_one：1 + 1 = 2 / Lean：theorem
theorem one_plus_one : 1 + 1 = 2 := by norm_num
-- END SOURCE ch01_004

-- BEGIN SOURCE ch01_005

-- 数学：1 + 1 = 2 を証明する
-- Lean：norm_num タクティクが数値計算を自動処理する
theorem first_theorem_recap : 1 + 1 = 2 := by
  norm_num
  -- No goals ✓
-- END SOURCE ch01_005

-- BEGIN SOURCE ch01_007
example : 3 * 7 = 21 := by
  norm_num
  -- No goals ✓
-- END SOURCE ch01_007

-- BEGIN SOURCE ch01_008
example : 3 * 7 = 21 := by
  rfl
  -- No goals ✓
-- END SOURCE ch01_008

-- BEGIN SOURCE ch01_010
example (a b : ℕ) : (a + b) * (a + b) = a * a + 2 * a * b + b * b := by
  ring
  -- No goals ✓
-- END SOURCE ch01_010

-- BEGIN SOURCE ch01_011
example (a b : ℕ) : (a + b) * (a + b) = a * a + 2 * a * b + b * b := by
  -- rw で分配法則を手動適用してから ring で整理する方法
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add]
  ring
-- END SOURCE ch01_011

-- BEGIN SOURCE ch01_013
example (a b c : ℝ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  linarith
  -- No goals ✓
-- END SOURCE ch01_013

-- BEGIN SOURCE ch01_014
example (a b c : ℝ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  -- Mathlib の le_trans 定理を直接 exact で提出する方法
  exact le_trans h1 h2
-- END SOURCE ch01_014

end LeanBook.Ch01
