import Mathlib

namespace LeanBook.Ch02

-- BEGIN SOURCE ch02_001

-- ゴール①：型クラスという「免許証」の確認
-- 数学：ℕ は加法を持つか？ / Lean：[Add ℕ] のインスタンスが存在するか？
#check (inferInstance : Add ℕ)
-- inferInstance : Add ℕ   ← 自然数には足し算の免許証がある

-- ゴール②：#print で型クラスの構造を解剖する
-- 数学：「加法を持つ」とはどういう構造か / Lean：Add クラスの定義を覗く
#print Add
-- class Add (α : Type u) where
--   add : α → α → α   ← 「add 演算が一つある」だけのシンプルな免許証

-- ゴール③：have によるサブゴール分割
-- 数学：「a ≤ b かつ b ≤ c ならば a ≤ c」を段階的に証明する
-- Lean：have でサブゴールを宣言し、linarith で解く
example (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  have step : a ≤ b := h1
  linarith
  -- No goals ✓
-- END SOURCE ch02_001

-- BEGIN SOURCE ch02_002
#check 42         -- 42 : ℕ
#check "hello"    -- "hello" : String
#check true       -- true : Bool
-- END SOURCE ch02_002

-- BEGIN SOURCE ch02_003
#check (1 + 1 = 2)
#check (∀ n : ℕ, n ≥ 0)

-- 命題を型として、その項である証明を作る。
theorem proof_term_example : (0 : ℕ) = 0 := rfl

-- 整数が期待される文脈での自然数からの変換。
def natAsInt (n : ℕ) : ℤ := n
theorem natAsInt_eq (n : ℕ) : natAsInt n = Int.ofNat n := rfl
-- END SOURCE ch02_003

-- BEGIN SOURCE ch02_004
-- 数学：「型 α の値同士を足し算できる」という性質
-- Lean：Add α というクラスのインスタンスが存在すること
section
variable (α : Type) [Add α] (a b : α)
#check a + b  -- a + b : α   ← [Add α] が免許証として機能している
end
-- END SOURCE ch02_004

-- BEGIN SOURCE ch02_005
#print Add
-- class Add (α : Type u) where
--   add : α → α → α
-- END SOURCE ch02_005

-- BEGIN SOURCE ch02_006
#print Monoid
-- 継承の要約（npow の既定値などは省略）：
-- class Monoid (M : Type u) extends Semigroup M, MulOneClass M where ...
-- Semigroup が結合律、MulOneClass が単位元の法則を持つ。
#check @mul_assoc
#check @one_mul
#check @mul_one
-- END SOURCE ch02_006

-- BEGIN SOURCE ch02_007
#check (inferInstance : CommSemiring ℕ)
#check (inferInstance : Field ℝ)
#check (inferInstance : LinearOrder ℝ)
#check (inferInstance : IsStrictOrderedRing ℝ)
-- 表示はいずれも inferInstance : 指定した型。
-- 順序と代数構造、および両者の整合性を分けて確認する。
-- END SOURCE ch02_007

-- BEGIN SOURCE ch02_008

-- 数学：0 + n = n（加法の左単位元）
-- Lean：simp が Nat.zero_add を自動適用する
example (n : ℕ) : 0 + n = n := by
  simp
  -- No goals ✓
-- END SOURCE ch02_008

-- BEGIN SOURCE ch02_009
-- ループが心配なとき：使う補題を明示する
example (n : ℕ) : 0 + n = n := by
  simp only [Nat.zero_add]
  -- No goals ✓
-- END SOURCE ch02_009

-- BEGIN SOURCE ch02_010

-- 数学：a ≤ b かつ b ≤ c かつ c ≤ d ならば a ≤ d（3段の推移律）
-- Lean：have で中間ステップを明示する
example (a b c d : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) (h3 : c ≤ d) : a ≤ d := by
  -- ステップ①：a ≤ c を先に示す（have で宣言）
  have hac : a ≤ c := by
    exact le_trans h1 h2
  -- ステップ②：中間結果 hac と h3 を使って a ≤ d を示す
  exact le_trans hac h3
  -- No goals ✓
-- END SOURCE ch02_010

-- BEGIN SOURCE ch02_011
-- 問：ℤ（整数）は CommRing（可換環）のインスタンスか？
-- #check と #print を使ってインスタンスと構造を確認してください。
#check (inferInstance : CommRing ℤ)
#print CommRing
-- END SOURCE ch02_011

-- BEGIN SOURCE ch02_012
-- ℤ は CommRing のインスタンスを持つ
#check (inferInstance : CommRing ℤ)
-- inferInstance : CommRing ℤ   ← Mathlib が登録したインスタンス

-- CommRing の構造を解剖する
#print CommRing
-- class CommRing (α : Type u) extends Ring α, CommMonoid α
-- → Ring（環）と CommMonoid（可換モノイド）の両方を継承している
-- No goals ✓
-- END SOURCE ch02_012

-- BEGIN SOURCE ch02_013
#check (inferInstance : Ring ℤ)
#check (inferInstance : AddCommGroup ℤ)
#check (inferInstance : LinearOrder ℤ)
#check (inferInstance : IsStrictOrderedRing ℤ)
-- END SOURCE ch02_013

-- BEGIN SOURCE ch02_015
example (n : ℕ) : n + 0 = n := by
  simp
  -- No goals ✓
-- END SOURCE ch02_015

-- BEGIN SOURCE ch02_016
-- simp only で使う補題を明示する（ループ防止版）
example (n : ℕ) : n + 0 = n := by
  simp only [Nat.add_zero]
  -- No goals ✓

-- または exact を使って項モードで書く
example (n : ℕ) : n + 0 = n :=
  Nat.add_zero n
-- END SOURCE ch02_016

-- BEGIN SOURCE ch02_018
example (a b c d : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) (h3 : c < d) : a < d := by
  have hac : a ≤ c := by
    exact le_trans h1 h2
  exact lt_of_le_of_lt hac h3
  -- No goals ✓
-- END SOURCE ch02_018

-- BEGIN SOURCE ch02_019
-- 中間結果を名前にせず、その証明を直接渡す
example (a b c d : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) (h3 : c < d) : a < d :=
  lt_of_le_of_lt (le_trans h1 h2) h3

-- または calc ブロックで3段の推移律を書く
example (a b c d : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) (h3 : c < d) : a < d :=
  calc a ≤ b := h1
       _ ≤ c := h2
       _ < d := h3
-- END SOURCE ch02_019

end LeanBook.Ch02
