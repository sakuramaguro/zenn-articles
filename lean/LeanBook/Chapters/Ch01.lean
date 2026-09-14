import Mathlib

namespace LeanBook.Ch01

-- BEGIN SOURCE ch01_001

-- ゴール①：環境確認 ── #eval で Hello World
#eval "Hello, Lean!"
-- 出力：Hello, Lean!

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

end LeanBook.Ch01
