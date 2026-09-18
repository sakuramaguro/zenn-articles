# 段階4-A：第12〜14章の可測空間・測度・a.e.を修正する

2026年9月16日実施。第12〜14章の本文・掲載コード・演習・Q&Aを照合し、P2-020〜025に対応しました。環境はLean 4.29.0-rc6 / Mathlib `5c8398df528176d9c87ccd9226ba8f7c8852d59c` を維持しました。各完成例は、自身のimportと前提だけで独立実行できる形にしています。

## σ-代数と測度の条件

「冪集合には測度を定義できない」という説明を訂正しました。冪集合のσ-代数には、零測度・数え上げ測度・Dirac測度などを定義できます。通常の長さとの整合性・平行移動不変性・可算加法性を全て保って実数の全ての部分集合へ拡張することとは区別が必要です。Banach–Tarskiの説明にも、体積との一致・回転と平行移動への不変性・有限加法性の条件を補いました。

第12章には `MeasurableSpace ℝ := ⊤` を局所的に置き、全ての集合の可測性と零測度での値を示す2定理を追加しました。局所インスタンスは `section Powerset` 内に限定し、後のボレル可測構造へ持ち越しません。

固定版の `MeasurableSpace` は空集合の可測性をフィールド `measurableSet_empty` として持ちます。全体集合から空集合を導く数学の公理化とは同値ですが、Mathlib内部の定義順とは異なります。構造体の表示と演習解答を修正しました。なお、`MeasurableSpace.measurableSet_top` は冪集合の可測構造に使う補題として実在します。初回指摘P2-021の「架空」は、構造体のフィールドとして掲載したことを指し、補題そのものの不存在を意味しません。

`BorelSpace` は可測構造がボレルσ-代数と等しいことを表します。開集合の可測性に必要な `OpensMeasurableSpace` との違いを説明しました。可算交叉は `MeasurableSet.iInter`、有理数の可算性は `Set.countable_range` を使い、値域から一点集合の合併への書き換えを別解に補いました。可算集合の可測性には一点集合の可測性が必要であることも明示しています。

これらは固定版の [MeasurableSpace/Defs.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/MeasurableSpace/Defs.lean) と [BorelSpace/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.lean) に照合しています。

## Measureの構造と公開補題

`Measure α` が `OuterMeasure α` を継承すること、`m_iUnion` と `trim_le` が追加のフィールドであることを説明しました。`Measure.trimmed` はフィールドではなく、その整合性条件から得られる等式です。全ての部分集合で評価できる外測度としての値と、可測集合族で保証される可算加法性を区別しています。`measure_eq_iInf` により、任意の集合での値と可測な上位集合の測度の下限との関係も確認しました。

存在しない `Measure.empty`・`Measure.iUnion`・`Measure.mono` を、`measure_empty`・`measure_iUnion`・`measure_mono` に修正しました。公開補題 `measure_iUnion` の引数順は「互いに素、可測性」、構造体の `m_iUnion` では「可測性、互いに素」です。両者を同じ順序として説明する箇所を改め、前者を完成定理として適用しました。

区間の測度は `ENNReal.ofReal (b - a)` であり、端点が逆なら空集合で値は0です。実数の標準可測構造がボレルσ-代数であることと、Lebesgue可測集合を全て含む完備化を区別しました。数え上げ測度・Dirac測度の説明には可測性の条件を補い、`volume` が型ごとのデフォルト測度であることを訂正しています。

制限測度が確率測度になる演習では、検証版に存在しない補題名を取り除きました。`IsProbabilityMeasure` の条件を取り出し、`Measure.restrict_apply` と区間の測度で証明する解答、および `simp` による別解の両方を検証しています。

実装は固定版の [MeasureSpaceDef.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Measure/MeasureSpaceDef.lean) と [NullMeasurable.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Measure/NullMeasurable.lean) に照合しています。

## 可測性・a.e.等式・積分

可測な実数値関数が必ず可積分になるわけではないことを明記しました。連続関数の可測性には、一般形では定義域に `OpensMeasurableSpace`、値域に `BorelSpace` が必要です。開集合の逆像の議論を、生成されたボレル集合まで広げる説明に直しました。

`Filter.ae` を `MeasureTheory.ae` に訂正しました。一方、初回P2-024で不明とされた `ae_restrict_of_ae` は固定版に実在します。`open MeasureTheory` を含む原稿の文脈と、完全修飾名 `MeasureTheory.ae_restrict_of_ae` の両方で確認しています。補題を不存在として置換する必要はありません。`ae_restrict_le` のフィルターの順序と、この方向に制限集合の可測性が不要であることも照合しました。該当する実装は [Restrict.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Measure/Restrict.lean) です。

`AEMeasurable f μ` の定義でa.e.等式の向きを正し、`.congr h` による証明と、可測な代表元を直接与えて `h.symm` を使う証明を区別しました。実数値では可測性から強可測性へ進めますが、一般のBanach空間値では可分性などの条件を確認する必要があります。

第14章のQ&Aに `ch14_015` を追加しました。0でだけ1となる実数値関数について、可測性とLebesgue測度でのa.e.零性を証明し、Lebesgue積分が0、0に集中するDirac測度での積分が1になることを検証しています。零関数とのa.e.等式はLebesgue可積分性も保ちます。一点での変更が可測性を保つことと、どの測度で積分値を保つかを分けて説明しました。積分そのものの説明は第16章へつなげています。

## 掲載例と表示の照合

全ての完成ブロックに必要なimportと宣言を含め、変数宣言の範囲を `section` で限定しました。演習の `sorry` 2件は未完成であることを表示し、完成解答と別に検証しています。第12〜14章内の節番号・章参照を通算番号へ直し、Part 4は予定の範囲として明示しました。

8例に `trace_state` を挿入し、開区間の可測性、有理数集合の可測性、区間の測度、単調性、制限測度の確率性、連続性からの可測性、a.e.等式の制限、AE可測性の直接証明を照合しました。a.e.等式の実表示 `=ᶠ[ae μ]` と本文の `=ᵐ[μ]` が同じ命題を表すことも説明しています。構造体や定義の表示を整理・省略した箇所は、そのことを明記しています。

## 検証結果

| 対象 | 結果 |
|---|---|
| 第12〜14章の全51ブロック | 完成例49、未完成の演習2を検証 |
| 独立実行 | 完成例49件をそれぞれ別のLeanプロセスで実行し成功。他の例の前提を補わない |
| 全体のビルド対象 | 311から355ブロックへ拡大 |
| 名前付き宣言の公理検査 | 254宣言。完成例に警告・`sorryAx`・未確認の公理なし |
| エラー・警告・完成例の公理 | 全37件を照合。新規2件は第12・13章の演習の穴 |
| 検査スクリプト | 23テスト成功 |
| 原稿との対応表 | 全23本・425ブロックが整合。第14章末尾に1件追加し、既存IDを維持 |
| ローカルリンクと記法 | 原稿・検証資料の643リンクに不存在なし。対象3章のコードフェンス・details・messageの開始と終了を確認 |

完成例は `warningAsError=true`・`autoImplicit=false` で検証し、名前付き宣言の公理も確認しました。許容する標準公理は `propext`・`Classical.choice`・`Quot.sound` です。演習の穴は別プロセスで警告と `sorryAx` を確認します。全体の分類は完成例339、断片49、意図したエラー12、未完成24、抜粋1です。分類は掲載目的であり、全425ブロックの実行検証が完了したことを意味しません。

[全体の実行結果](catalog/stage4a-verification.json)、[独立実行の結果](catalog/stage4a-source-checks.json)、[掲載例とゴールの実出力](catalog/stage4a-outputs.txt) を保存しています。再現する場合は `lean/` で次を実行します。

```sh
python3 scripts/catalog.py extract
python3 scripts/verify.py
python3 scripts/check_stage4a_sources.py
```

新しい結果は `.generated/verification.json` と `.generated/stage4a-source-checks.json` に保存されます。本文の最後の語句・表示調整後にも、原稿全体のハッシュと全Leanブロックの内容・検証先の対応を照合しました。

## 残る範囲

次は段階4-Bの第15・16章（単関数・積分）です。その後、段階4-Cで第17・18章の周辺説明・演習まで照合します。全体の文体・図・Zenn表示の統一は段階5、新しい環境からの全体再現は段階6に残ります。Banach–Tarskiや冪集合への拡張不可能性などの数学的説明を、この段階で新たにLeanの定理として形式化したわけではありません。
