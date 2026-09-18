# 段階4-C：第17・18章の収束定理・Lᵖ・確率を修正する

2026年9月18日完了。第17・18章の本文・掲載コード・演習・Q&Aを照合し、P2-034〜037とP3-046に対応しました。Lean 4.29.0-rc6 / Mathlib `5c8398df528176d9c87ccd9226ba8f7c8852d59c` と間接依存8件を維持しました。

## 収束定理の仮定と演習

第17章は、段階1-Dで修正した単調収束・Fatou・優収束の完成例を、各例のimportと明示した前提だけで再検証しました。非負拡張実数値の単調収束では∞も扱えること、`lintegral_iSup'` の仮定がAE可測性と `∀ᵐ x ∂μ, Monotone (fun n => f n x)` であることを明記しています。単関数近似への単調収束定理の適用と、`lintegral` 自体の定義も区別しました。

リーマン積分に関する導入の説明にはコンパクトな区間という範囲を加えました。正弦関数列の演習には `sineSequence_zero` を追加し、Leanでの0除算の規約と、数学で $n\geq1$ として読む評価を区別しています。優関数1が可積分なのは有限な制限測度を使うためであること、同じ例は積分の直接評価でも証明できることを説明しました。

Fatouの真の不等式の例、優収束定理による積分の収束、その直接評価による別解はすべて完成例です。前提が必要な2件は、`ch17_011` が `ch17_010`、`ch17_013` が `ch17_012` を同じファイルで先に実行することを章頭・本文・対応表に明記しました。

仮定を照合した実装は [Lebesgue/Add.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean) と [DominatedConvergence.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean) です。

## Lᵖの指数と可測性

第18章の `Memℒp`・`memℒp_const`・`memℒp_one_iff_integrable` を、固定版の `MemLp` 系の名前へ修正しました。引数順を `f p μ`、定義を `AEStronglyMeasurable f μ ∧ eLpNorm f p μ < ∞` として確認しています。

`eLpNorm` について、0では規約値0、有限の正の指数ではべき積分、∞では本質的上限となる3つの場合を、それぞれ定理で確認しました。通常のノルム空間・Banach空間の説明を $1\leq p\leq\infty$ に限定し、積分のべき乗公式は有限の指数について書いています。`IntegrableOn` との関係には制限測度を明示しました。

a.e.等しい関数を同一視した `Lp` と、関数についての条件 `MemLp` を区別しました。`Lp` の元を点で評価する際の代表関数にも触れています。有限測度上の包含関係は真の包含とは限らないこと、無限測度上へそのまま移せないことを補足しました。

定義は [LpSeminorm/Defs.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Function/LpSeminorm/Defs.lean)、ノルムと空間の構造は [LpSpace/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean) に照合しました。

## 期待値と条件付き期待値

`expectation`・`myExpectation` は `noncomputable def` とし、定義自身は可積分性や確率測度の証明を引数として持たないことを説明しました。加法性には両方の可積分性を渡し、非可積分時の規約値0を通常の有限な期待値と混同しないようにしています。

定数期待値の計算では、実際のゴール `P.real Set.univ • c = c` に合わせました。手動の演習解答は `Measure.real`・`measure_univ`・`ENNReal.toReal_one`・`one_smul` の順に展開します。従来の `ENNReal.one_toReal` は固定版に存在しません。

確率変数の可測性は「値を計算できる条件」とせず、Borel集合の逆像が事象になることとして説明しました。`IsProbabilityMeasure` の構造・型の確認には `No goals` を付けず、証明とは区別しています。インスタンスの構成は `⟨hP⟩` を実際に検証し、未確認の補題名を使う説明を除きました。

条件付き期待値は `condExp` です。必要なσ有限性は、元の測度ではなく、`hm : m ≤ m₀` に対する `P.trim hm` について確認します。確率測度の場合はこの測度も有限です。`trim` と部分集合への `restrict` の違い、定義の条件が成立しない場合の規約値0も明記しました。

予告の `sorry` は `hf.condExp_ae_eq hst` で埋めました。これは既にマルチンゲールと仮定した過程の性質を取り出す証明であると明記し、各項の可積分性も `hf.integrable t` で確認しました。この性質の取り出しに確率測度・σ有限測度の型クラスを追加する必要はありません。原稿用の名前は `martingale_condExp_property` とし、既存の別定理 `MeasureTheory.martingale_condExp` との同名衝突を避けました。

参照した実装は [ConditionalExpectation/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean)、[Filtration.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Probability/Process/Filtration.lean)、[Martingale/Basic.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Probability/Martingale/Basic.lean) です。

## L²の内積と文章

定義域が曖昧にならないよう、型クラス確認の測度を `volume : Measure ℝ` と明示しました。内積と完備性を別々に確認し、それらを合わせてHilbert空間と呼ぶことを説明しています。

`Lp.inner_def` を `L2.inner_def` へ修正し、実数値の内積公式とノルムの二乗の積分公式を証明しました。複素数値の内積は第1変数が共役線形なので、`∫ x, star (f x) * g x ∂μ` になることも完成例で確認しています。一般のノルムの説明には実在する `Lp.norm_def` を使いました。定義は [L2Space.lean](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/MeasureTheory/Function/L2Space.lean) に照合しています。

第17・18章の通算章番号に揃え、第18章末のPart 3対応表も第12〜18章の番号へ修正しました。`Hibert` 等の表記を訂正し、既に直したFatouの説明を再確認してP3-046を解消しています。Part 4は執筆予定であることを明示し、本章の完成例と将来のSDEの議論を区別しました。

## 検証結果

| 対象 | 結果 |
|---|---|
| 第17・18章の独立実行 | 全28ケース成功。第17章13、第18章15 |
| 前提の再利用 | 第17章の2件。対象28ブロックに重複加算しない |
| 全体のビルド対象 | 375から390ブロックへ拡大。完成例341と断片49のすべてが対象 |
| 名前付き宣言の公理検査 | 309宣言。完成例に警告・`sorryAx`・未確認の公理なし |
| 意図したエラー等の診断 | 既存37件が成功。意図したエラー12件、演習の穴23件、完成例の公理2件 |
| 検査スクリプト | 23テスト成功 |
| 原稿との対応表 | 全23本・425ブロックが整合。ブロックの追加・削除・ID変更なし |
| ローカルリンク | 原稿・検証資料の659件に不存在なし |
| Markdownの構造 | 対象2章のコードフェンス・details・messageの開始と終了を確認 |

`ch18_008` を未完成例から完成例へ変更し、分類は完成例341、断片49、意図したエラー12、未完成23、抜粋0となりました。全425ブロックがビルド対象または診断対象に対応していますが、新しい環境からの再現と全ページの表示確認はまだ段階6の作業です。

完成例は `warningAsError=true`・`autoImplicit=false` で実行し、`propext`・`Classical.choice`・`Quot.sound` 以外の公理を許容しない基準を維持しました。7ブロックの `trace_state` で、収束定理・Fatouの反例・正弦関数列・定数期待値・L²の内積とノルムのゴールを確認しています。

[全体の実行結果](catalog/stage4c-verification.json)、[独立実行の結果](catalog/stage4c-source-checks.json)、[掲載例とゴールの実出力](catalog/stage4c-outputs.txt) を保存しています。再現する場合は `lean/` で次を実行します。

```sh
python3 scripts/catalog.py extract
python3 scripts/verify.py
python3 scripts/check_stage4c_sources.py
```

新しい結果は `.generated/verification.json` と `.generated/stage4c-source-checks.json` に保存されます。

## 次の段階

段階5は全23本の文章・構成・Zenn表示の統一です。Part構成と序文の範囲、残る章参照、図の実内容とalt・キャプション、折りたたみ記法、演習と解答の表示を確認します。段階6では読者向け手順による再現、全ページの表示確認、継続的な自動検査を仕上げます。
