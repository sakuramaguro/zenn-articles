# 段階4-B：第15・16章の単関数・積分を修正する

2026年9月17日完了。第15・16章の本文・掲載コード・演習・Q&Aを照合し、P2-026〜028に対応しました。第17章の指示関数の関連例も独立実行しています。Lean 4.29.0-rc6 / Mathlib `5c8398df528176d9c87ccd9226ba8f7c8852d59c` と間接依存8件を維持しました。

## 単関数の構造と積分

単関数の定数積分の補題名を `SimpleFunc.const_lintegral` に修正しました。一般の非負積分で使う `MeasureTheory.lintegral_const` との違いを説明し、定数3を `[0,1]` に制限したLebesgue測度で積分する証明を再構成しました。定義通りの有限和との等式も `rfl` で確認しています。

`SimpleFunc` の可測性・有限性のフィールド名には末尾に `'` が付きます。利用者向けの `measurableSet_fiber`・`finite_range` は、それらを取り出す補題です。値域に可測構造を要求せず、各値の逆像の可測性を持つ構造体であることを説明しました。通常の可測性から各値の逆像の可測性を得る向きには、一点集合の可測性が必要です。

定数単関数の値域が一点集合になる演習には `[Nonempty α]` を加えました。空の定義域では値域も空になることを別の定理で確認しています。`Set.range f`、`Finset` を返す `f.range`、有限性の証明 `f.finite_range` を区別しました。実数を含む値を `#eval` で実行する例は、定数の関数値を `rfl` で証明する例へ改めています。

区分的な単関数の積分は、`SimpleFunc.lintegral_eq_lintegral` で一般の非負積分へ移し、`lintegral_piecewise` と定数積分の公式で計算しました。`SimpleFunc.lintegral_piecewise` を仮定する解答を訂正しています。通常の指示関数を使う別解は、値域を `ℝ≥0∞` と明示し、`lintegral_indicator hA` の引数順に合わせました。

集合の外で0にする単関数は `f.restrict A` で扱います。`SimpleFunc.coe_restrict f hA` が `A.indicator f` との一致を与えますが、固定版の `restrict` は非可測な集合では零単関数となります。この点をQ&Aに明記し、存在しない `SimpleFunc.indicator` を前提にした説明を取り除きました。

定義・補題・引数は、固定版の [SimpleFunc.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Function/SimpleFunc.lean) と実出力に照合しています。

## eapproxとlintegralの定義

`eapprox f n` は、非負有理数の列挙 `ennrealRatEmbed` の先頭 `n` 個を使う近似です。可測な `f` について、`k < n` の候補のうち `f x` 以下のものと0から最大値を選びます。「n等分刻みで丸める」という説明を改めました。実装の `Finset.range n` と `approx_apply` を照合しています。

単調性や列の定義と、可測な `f` に対して各点で上限が `f x` と一致する定理を区別しました。演習では、拡張非負実数上の恒等関数について、0番目の近似、1番目と2番目の大小関係、各項の有限性、上限との一致を証明しています。`x = ∞` でも各項は有限で、上限が∞になる場合を含みます。

`lintegral` の定義は、`f` 以下の単関数全体の積分の上限です。特定の `eapprox` 列で定義するものではありません。可測な関数について近似列の積分の上限と一致する定理が `lintegral_eq_iSup_eapprox_lintegral` です。第15章でこの定理を適用し、第16章では定義自体の等式も証明しました。任意の非可測関数にも下積分として値を与えることと、加法性などを使う際の可測性の条件を区別しています。

参照した実装は [Lebesgue/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Integral/Lebesgue/Basic.lean) と [Lebesgue/Add.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean) です。

## 可積分性と規約値

第16章のコメントだけの抜粋 `ch16_004` を、実数全体の定数1についての完成証明へ置き換えました。非可積分性を証明し、`integral_undef` によるBochner積分の規約値0と、同じ定数を `ℝ≥0∞` 値で非負積分した値∞を確認しています。既に修正済みのディリクレ関数は、a.e.で0に等しいことから可積分性と積分0を証明する例として再検証しました。

正部分・負部分の差による説明は、可積分な実数値関数に限定しています。一般のBanach空間値での条件は `AEStronglyMeasurable` と `HasFiniteIntegral` です。固定版の `integral` は値域が完備でない場合にも0を返すため、通常のBochner積分を扱う場面の完備性も説明しました。

`integral_add` の適用には両方の可積分性の証明が必要です。積分式を記述できることと、この補題を使えることを区別し、「非可積分な場合は必ず等式が偽になる」という説明を訂正しました。`integral_smul` の実数スカラーの例は、0の場合と、非零スカラー倍が可積分性を保つ場合に分けて説明しています。一般版のスカラーと作用の仮定も明記しました。ノルム不等式では、非可積分時に左辺が0、右辺は非負であるという段階1-Dの説明を維持しています。

指数関数の半直線上の可積分性、端点の追加、可積分性の2条件を取り出す補足も再検証しました。`exp_neg_integrable_parts` は前の解答を使う定義の確認であり、独立した有限性の別証明ではありません。参照した実装は [Bochner/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean) です。

## 実行方法と検証結果

各例に必要なimportと記法を揃えました。前の定理を使う補足2件だけは、原稿と対応表に前提を明示しています。`ch16_015` は `ch16_014`、`ch16_017` は `ch16_007` を同じファイルで先に実行します。独立実行の結果では、前提の再利用を対象ブロック数に加算しません。章・節番号も第15・16章の通算番号へ揃えました。

| 対象 | 結果 |
|---|---|
| 第15・16章 | 全29ブロックを検証。第15章12、第16章17 |
| 独立実行 | 上記29件と第17章の関連例 `ch17_010` の計30ケースが成功 |
| 全体のビルド対象 | 355から375ブロックへ拡大 |
| 名前付き宣言の公理検査 | 283宣言。完成例に警告・`sorryAx`・未確認の公理なし |
| エラー・警告・完成例の公理 | 既存37件の診断を全て再照合 |
| 検査スクリプト | 23テスト成功 |
| 原稿との対応表 | 全23本・425ブロックが整合。ブロックの追加・削除・ID変更なし |
| ローカルリンクと記法 | 原稿・検証資料の650リンクに不存在なし。対象2章のコードフェンス・details・messageの開始と終了を確認 |

完成例は `warningAsError=true`・`autoImplicit=false` で実行しています。許容する標準公理は `propext`・`Classical.choice`・`Quot.sound` で、依存を宣言ごとに記録しました。7ブロックに `trace_state` を挿入し、定数積分・区分的な単関数・0番目の近似・非可積分性・加法性・スカラー倍・可積分性の2条件のゴールを確認しています。

全体の分類は完成例340、断片49、意図したエラー12、未完成24、抜粋0です。コメントだけの抜粋1件を完成証明へ置き換えましたが、全425ブロックの実行確認が完了したことを意味しません。

[全体の実行結果](catalog/stage4b-verification.json)、[独立実行の結果](catalog/stage4b-source-checks.json)、[掲載例とゴールの実出力](catalog/stage4b-outputs.txt) を保存しています。再現する場合は `lean/` で次を実行します。

```sh
python3 scripts/catalog.py extract
python3 scripts/verify.py
python3 scripts/check_stage4b_sources.py
```

新しい結果は `.generated/verification.json` と `.generated/stage4b-source-checks.json` に保存されます。最後の本文・ゴール表示の調整はLeanブロックを変えておらず、調整後にも原稿全体のハッシュと掲載コードの内容・位置・検証先を照合しました。

## 残る範囲

次は段階4-Cの第17・18章（収束定理・Lᵖ・確率）です。第17章のコードは先行修正済みですが、周辺説明と演習を含めて再確認します。図の実内容・Zenn表示・全体の文体の統一は段階5、新しい環境からの全体再現は段階6に残ります。
