import Mathlib

namespace LeanBook.Ch03

-- BEGIN SOURCE ch03_001

-- ゴール①：rfl が失敗するケースを自力で読み、ring で修正できる
-- 数学：a + b = b + a（交換法則）/ Lean：rfl では解けない、ring や Nat.add_comm を使う
example (a b : ℕ) : a + b = b + a := by
  ring
  -- No goals ✓

-- ゴール②：型クラスエラーを自力で読み、[Add α] を追加して修正できる
-- 数学：「型 α に足し算は定義されているか？」/ Lean：[Add α] という免許証が必要
section
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
end
-- END SOURCE ch03_001

-- BEGIN SOURCE ch03_003
-- 失敗例とは別ファイルで実行する完成例。
theorem add_comm_fixed (a b : ℕ) : a + b = b + a := by
  ring
-- END SOURCE ch03_003

-- BEGIN SOURCE ch03_005

theorem one_add_one_ne_three : (1 : ℕ) + 1 ≠ 3 := by
  norm_num
-- END SOURCE ch03_005

-- BEGIN SOURCE ch03_007
-- 3.2節の失敗例と置き換えて実行する。
def add_five_fixed (n : Nat) : Nat := n + 5
#eval add_five_fixed 7
-- 出力：12
-- END SOURCE ch03_007

-- BEGIN SOURCE ch03_009

-- 数学：a + b = b + a（交換法則）を自動で探索させる
theorem test (a b : ℕ) : a + b = b + a := by
  exact?
-- END SOURCE ch03_009

-- BEGIN SOURCE ch03_010
theorem add_comm_explicit (a b : ℕ) : a + b = b + a := by
  exact Nat.add_comm a b
-- END SOURCE ch03_010

-- BEGIN SOURCE ch03_012
-- 数学：「α は加法の構造を持つ」という前提を追加する
-- Lean：[Add α] という型クラスの免許証を提示する
section
variable (α : Type) [Add α] (a b : α)

#check a + b  -- a + b : α
end
-- END SOURCE ch03_012

-- BEGIN SOURCE ch03_015

theorem hard_proof (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  have step1 : a ≤ b := h1    -- sorry → h1 に置き換え
  have step2 : b ≤ c := h2    -- sorry → h2 に置き換え
  linarith                    -- sorry → linarith に置き換え
  -- No goals ✓

#print axioms hard_proof
-- END SOURCE ch03_015

-- BEGIN SOURCE ch03_017
example (a b : ℕ) : a * b = b * a := by
  ring
  -- No goals ✓
-- END SOURCE ch03_017

-- BEGIN SOURCE ch03_018
example (a b : ℕ) : a * b = b * a := by
  exact Nat.mul_comm a b
-- END SOURCE ch03_018

-- BEGIN SOURCE ch03_020

-- 数学：α は可換モノイド（掛け算と単位元があり、交換律が成立）
-- Lean：[CommMonoid α] という型クラスの免許証を追加する
section
variable (α : Type) [CommMonoid α] (a b : α)

example : a * b = b * a := by
  exact mul_comm a b
  -- No goals ✓
end
-- END SOURCE ch03_020

-- BEGIN SOURCE ch03_021
-- CommMonoid では加法・分配法則を仮定していない。交換法則を直接使う。
theorem commMonoid_mul_comm {α : Type*} [CommMonoid α] (a b : α) :
    a * b = b * a :=
  mul_comm a b
-- END SOURCE ch03_021

-- BEGIN SOURCE ch03_023
theorem even_square_plus_self (n : ℕ) : 2 ∣ n ^ 2 + n := by
  -- 数学：n^2 + n = n * (n + 1) と変形する
  have h : n ^ 2 + n = n * (n + 1) := by ring
  -- 数学：n * (n + 1) は連続する2整数の積なので偶数
  rw [h]
  exact Nat.even_mul_succ_self n |>.two_dvd
  -- No goals ✓
-- END SOURCE ch03_023

-- BEGIN SOURCE ch03_024
-- 第1解で使った偶数性の補題に、式の変形を合わせる別の書き方。
theorem even_square_plus_self_calc (n : ℕ) : 2 ∣ n ^ 2 + n := by
  have h : n ^ 2 + n = n * (n + 1) := by ring
  simpa only [h] using (Nat.even_mul_succ_self n).two_dvd
-- END SOURCE ch03_024

end LeanBook.Ch03
