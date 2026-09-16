# 段階3-C：第10・11章のℓ²・級数・不動点を修正する

2026年9月16日実施。第10・11章の本文・掲載コード・演習・Q&Aを照合し、P2-017・018に対応しました。段階1-B・1-Cで修正した非コンパクト性と不動点定理の証明も再検証しています。環境はLean 4.29.0-rc6 / Mathlib `5c8398df528176d9c87ccd9226ba8f7c8852d59c` を維持しました。

## ℓ²の定義と完備性

固定版の `lp E p` は `AddSubgroup (PreLp E)` として定義されています。型として使うときには、関数と所属条件の証明を持つ部分型に変換されます。「lpそのものがTypeなので所属記号は使えない」という説明を訂正しました。指数の `(2 : ℝ≥0∞)` という注釈は必須ではなく、注釈なしの `2` も引数の型から推論されることを、両方の `#check` で確認しています。

`Memℓp` は、指数0では有限台、∞では成分ノルムの有界性、正の有限指数ではノルムの冪の総和可能性を表します。実数値の `∑'` は総和可能でない場合にも規約値を持つため、その値の有限性では収束条件を表せません。`mem_two_iff` で実数列・指数2の場合を `Summable (fun n => ‖f n‖ ^ (2 : ℕ))` と結び付けました。

一般のノルム空間構造・完備性には `[Fact (1 ≤ p)]`、完備性にはさらに各成分の完備性が必要です。完備性の証明では、座標ごとの極限に加えてCauchy列の一様なノルム評価を使います。有限部分和に評価を移す `lp.memℓp_of_tendsto` と、ノルム収束を導く `lp.tendsto_lp_of_tendsto_pi` の役割を説明しました。この証明をBochner積分に直接依存するものとして説明する箇所を改めました。

定義・仮定・証明構造は、固定版の [lpSpace.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/Normed/Lp/lpSpace.lean) と実出力に照合しています。再現できないソース検索の行数を削除し、Lakeが取得したソースを開く手順に置き換えました。

## 級数の演習と数学上の区別

数列 `1 / (n + 1)` がℓ²に属する演習は、存在しない補題名や未証明部分を取り除き、2通りの完成解答にしました。どちらも `Real.summable_one_div_nat_pow` で指数2の級数の総和可能性を得ます。一方は `summable_nat_add_iff 1`、もう一方は `Summable.comp_injective` と `Nat.succ_injective` で添字をずらします。0番目の項の規約と、総和可能性だけを使いBasel問題の和の値は不要であることも説明しました。補題は固定版の [PSeries.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/PSeries.lean) にあります。

閉単位球の意味で使われていた「単位球」を「単位閉球」に揃えました。ℓ²内の個々のコンパクト集合にも定理を適用できること、実ノルム空間での閉球のコンパクト性と有限次元性の対応を区別しています。可算な正規直交基底と、有限の線形結合で全ての元を表す代数的な基底（Hamel基底）も区別しました。

実数列の内積を実数の積で表し、複素数へ広げる場合はMathlibが第1引数に共役を取ることを明記しました。`InnerProductSpace.toDual` はRiesz表現定理による同型を与える定義です。型クラスのインスタンスとする説明を訂正し、弱収束の紙上の証明とAPIの型を確認するコードの範囲を分けています。参照した実装は [l2Space.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/InnerProductSpace/l2Space.lean) と [Dual.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/InnerProductSpace/Dual.lean) です。

## 不動点定理と掲載例の前提

第11章の一般の一意存在・反復収束、実数のアフィン写像、ℓ²のスカラー倍の完成証明を再検証しました。距離空間での `fixedPoint` と、完備な拡張距離空間で初期点からの有限距離を仮定する `efixedPoint` の引数を、固定版の [Contracting.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Topology/MetricSpace/Contracting.lean) に照合しています。`efixedPoint`・`exists_fixedPoint` の型を確認するコマンドも追加しました。

両章の冒頭に、掲載順に引き継ぐimport・宣言と、別ファイルで実行する意図的な失敗・演習の穴を明示しました。独立実行では、その例が必要とする原稿の前提ブロックを列挙して使い、他の例の局所変数を持ち越しません。連結する3組の証明と級数の解答に `trace_state` を挿入し、本文のゴール説明を実出力に照合しました。第10・11章内の節番号と相互参照も通算番号に合わせています。

## 検証結果

| 対象 | 結果 |
|---|---|
| 第10・11章の全52ブロック | 完成・連結例49、意図したエラー1、未完成の演習2を検証 |
| 独立実行 | 完成・連結例49ブロックを42組に分けて成功。前提として再利用するブロックは別記 |
| 全体のビルド対象 | 302から311ブロックへ拡大 |
| 名前付き宣言の公理検査 | 195宣言。完成例に警告・`sorryAx`・未確認の公理なし |
| エラー・警告・完成例の公理 | 全35件を照合。新規1件は第10章の演習の穴 |
| 検査スクリプト | 23テスト成功 |
| 原稿との対応表 | 全23本・424ブロックが整合。IDの追加・削除・番号変更なし |

完成例は `warningAsError=true`・`autoImplicit=false` で検証し、名前付き宣言の公理も確認しました。許容する標準公理は `propext`・`Classical.choice`・`Quot.sound` です。演習の穴は別プロセスで警告と `sorryAx` を確認します。旧コードのハッシュと分類を保存した上で、実行可能にした抜粋と証明断片の分類を更新しました。全体の分類は完成例338、断片49、意図したエラー12、未完成24、抜粋1です。

[全体の実行結果](catalog/stage3c-verification.json)、[独立実行の結果](catalog/stage3c-source-checks.json)、[掲載例とゴールの実出力](catalog/stage3c-outputs.txt) を保存しています。再現手順は `lean/` で `python3 scripts/verify.py` と `python3 scripts/check_stage3c_sources.py` を実行します。後者の新しい結果は `.generated/stage3c-source-checks.json` に保存されます。

## 残る範囲

段階3の第6〜11章は、これで3つのまとまりを終えました。次は段階4-Aの第12〜14章（可測空間・測度・a.e.）です。全体の文体・図・Zenn表示の統一は段階5、新しい環境からの全体再現は段階6に残ります。第10章の弱収束や連続関数空間の無限次元性、第11章の区間上の微分の議論は紙上の解答であり、その全てをLeanの定理にしたわけではありません。
