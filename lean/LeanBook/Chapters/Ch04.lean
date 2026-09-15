import Mathlib

namespace LeanBook.Ch04

-- BEGIN SOURCE ch04_001

-- ゴール①：#check で型シグネチャを読む
-- 数学：∀ n m ∈ ℕ, n + m = m + n の Lean での表現を確認する
#check Nat.add_comm
-- 出力：Nat.add_comm (n m : ℕ) : n + m = m + n

-- ゴール②：#print で定義の中身を解剖する
-- 数学：Nat.add_comm がどう証明されているか内部を覗く
#print Nat.add_comm
-- 出力：theorem Nat.add_comm : ∀ (n m : ℕ), n + m = m + n := ...

-- ゴール③：exact? でゴールにマッチする補題を自動発見する
-- 数学：a + b = b + a を自動で探索させる
example (a b : ℕ) : a + b = b + a := by
  exact?
  -- Try this: exact Nat.add_comm a b

-- ゴール④：名前空間を開いて補題名を短縮する
-- 数学：Nat.add_comm を add_comm と書けるようにする
example (a b : ℕ) : a + b = b + a := by
  open Nat in
  exact add_comm a b
  -- No goals ✓
-- END SOURCE ch04_001

-- BEGIN SOURCE ch04_002

-- 数学：Nat.add_comm の型シグネチャを確認する
#check Nat.add_comm
-- END SOURCE ch04_002

-- BEGIN SOURCE ch04_003

-- 数学：Nat.add_comm の証明がどう構成されているか覗く
#print Nat.add_comm
-- END SOURCE ch04_003

-- BEGIN SOURCE ch04_004

-- 数学：加法モノイドとは何か / Lean：AddMonoid の構造体を覗く
#print AddMonoid
-- END SOURCE ch04_004

-- BEGIN SOURCE ch04_005

-- 数学：a + b = b + a を証明したい、定理名が分からない
theorem test (a b : ℕ) : a + b = b + a := by
  exact?
-- END SOURCE ch04_005

-- BEGIN SOURCE ch04_006
theorem add_comm_explicit (a b : ℕ) : a + b = b + a := by
  exact Nat.add_comm a b
-- END SOURCE ch04_006

-- BEGIN SOURCE ch04_007

-- 数学：a ≤ c を証明したいが、a ≤ b と b ≤ c という仮定がある
example (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  apply?
-- END SOURCE ch04_007

-- BEGIN SOURCE ch04_008
theorem trans_explicit (a b c : ℕ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by
  exact le_trans h1 h2
-- END SOURCE ch04_008

-- BEGIN SOURCE ch04_009

-- Nat 名前空間内の定理は完全修飾名で参照する
#check Nat.add_comm      -- Nat 名前空間の add_comm
#check List.length_cons  -- List 名前空間の length_cons
#check LinearMap.ker     -- LinearMap 名前空間の ker
-- END SOURCE ch04_009

-- BEGIN SOURCE ch04_010

-- open なし：完全修飾名が必要
example (a b : ℕ) : a + b = b + a := Nat.add_comm a b

-- open Nat in：続く式で Nat. を省略できる
-- 数学：同じ命題を短縮記法で書く
example (a b : ℕ) : a + b = b + a :=
  open Nat in add_comm a b

-- ブロック全体に open を適用する
example (a b c : ℕ) : a + b + c = c + b + a := by
  open Nat in
  omega
  -- No goals ✓
-- END SOURCE ch04_010

-- BEGIN SOURCE ch04_011
-- import はモジュールの読込、open は名前の解決範囲の指定。
-- Mathlibの全定理がMathlib名前空間の中にあるわけではない。
open Nat in
#check add_comm

open MeasureTheory in
#check integral

-- 完全修飾名なら、open の範囲によらず参照できる。
#check Nat.add_comm
#check MeasureTheory.integral
-- END SOURCE ch04_011

-- BEGIN SOURCE ch04_012
-- 学習時は広く読み込んで探索する。
-- END SOURCE ch04_012

-- BEGIN SOURCE ch04_015

-- ring：可換半環・可換環での多項式の等式
-- 数学：(a + b)² = a² + 2ab + b²
example (a b : ℝ) : (a + b)^2 = a^2 + 2*a*b + b^2 := by ring

-- norm_num：具体的な数値の等式・不等式
-- 数学：2 + 2 = 4、具体的な有理数の大小比較など
example : (2 : ℝ) + 2 = 4 := by norm_num

-- omega：自然数・整数の線形算術（変数同士の積などは一般には扱わない）
-- 数学：n + 1 > n（自然数の性質）
example (n : ℕ) : n + 1 > n := by omega

-- linarith：線形不等式の推移
-- 数学：a ≤ b → b ≤ c → a ≤ c
example (a b c : ℝ) (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by linarith
-- END SOURCE ch04_015

-- BEGIN SOURCE ch04_016

-- 以下を実行して出力を読んでください
#check Nat.add_comm
#print Nat.add_comm
-- END SOURCE ch04_016

-- BEGIN SOURCE ch04_017
#check @Nat.add_comm
-- @ は暗黙引数の自動挿入を抑え、関数全体の型を確認するときに使う。
-- Nat.add_comm の n, m はもともと明示引数。
-- END SOURCE ch04_017

-- BEGIN SOURCE ch04_019
theorem succ_bound (n : ℕ) : n ≤ n + 1 := by
  exact Nat.le_add_right n 1
-- END SOURCE ch04_019

-- BEGIN SOURCE ch04_020
example (n : ℕ) : n ≤ n + 1 := by
  omega
  -- No goals ✓
-- END SOURCE ch04_020

-- BEGIN SOURCE ch04_022
-- まず #check で確認
-- #check Nat.zero_le
-- 出力：Nat.zero_le (n : ℕ) : 0 ≤ n

example (α : Type*) (s : Finset α) : 0 ≤ s.card := by
  -- 数学：Finset.card は ℕ なので Nat.zero_le が適用できる
  exact Nat.zero_le s.card
  -- No goals ✓
-- END SOURCE ch04_022

-- BEGIN SOURCE ch04_023
example (α : Type*) (s : Finset α) : 0 ≤ s.card := by
  omega
  -- No goals ✓
-- END SOURCE ch04_023

end LeanBook.Ch04
