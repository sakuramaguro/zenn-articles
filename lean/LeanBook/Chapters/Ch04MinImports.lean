import Mathlib

namespace LeanBook.Ch04

-- BEGIN SOURCE ch04_014
-- 調べたい宣言を #min_imports in の直後に置く。
#min_imports in
theorem import_example (n : ℕ) : n + 0 = n := Nat.add_zero n
-- 提案は記法や宣言に依存する。採用後に再ビルドして確認する。
-- END SOURCE ch04_014

end LeanBook.Ch04
