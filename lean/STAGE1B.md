# 段階1-B：合成の仮定・擬距離と商・閉球のコンパクト性

2026年9月14日実施。P1-03・P1-07・P1-08について、本文・演習・予告・再掲を修正しました。Lean 4.29.0-rc6 / Mathlib `5c8398df528176d9c87ccd9226ba8f7c8852d59c` を継続使用しています。

## 修正内容

| 指摘 | 修正と確認 |
|---|---|
| P1-03：合成の連続性の仮定不足 | 第6章で、内側の関数の a での連続性と、外側の関数の f(a) での連続性を明記。ε-δによる完成証明と、自己合成で仮定を省けない反例の説明を追加。 |
| P1-07：擬距離と商の前後が逆 | 第7章で2点の距離が0になる擬距離を構成し、分離条件の否定を証明。ℝ/ℤでは0と1が同じ類であること、通常のL²は商を取った後の距離空間であることを訂正。第18章の説明も対応させた。 |
| P1-08：存在しない型クラスと探索失敗の誤解 | 第8〜11章を ProperSpace に基づく説明へ修正。距離空間でのHeine–Borel型の同値と、擬距離空間で必要となるT2Spaceの仮定を明記。第10章でℓ²の単位閉球の非コンパクト性、ProperSpaceの否定、有限次元性の否定を証明。 |

原稿は第6・7・8・9・10・11・18章の7ファイルを変更しました。第10章の型略記を `ell2` にし、`lp.single` の指数引数と、距離構造を項として与える例の `noncomputable` を補いました。第11章の不動点コード自体の修正は段階1-Cに残しています。

## ℓ²の証明と説明の対応

1. `e n := lp.single 2 n 1` を定義し、`lp.norm_single` からノルムが1であることを示します。
2. 異なる2項について、1つの成分のノルムが全体のノルム以下であることから距離が1以上と証明します。
3. 単位閉球がコンパクトだと仮定すると、標準基底列に収束部分列が存在します。そのCauchy条件が与える「十分先の距離は1未満」と、手順2の下界が矛盾します。
4. `ProperSpace ell2` なら単位閉球がコンパクトになるので、その否定を導きます。有限次元なら `FiniteDimensional.proper` が使えることから、有限次元性も否定できます。

距離の厳密値√2は本文で数学的に説明し、Leanでは非コンパクト性に十分な下界1を証明しています。√2という等式のLean形式化を完了したとは扱いません。

演習の C([0,1]) は、単項式族の線形独立性により無限次元であることを紙上で説明しています。Leanでは「無限次元の実ノルム空間はProperSpaceではない」という一般定理を検証し、C([0,1])自体の無限次元性の形式化は含めていません。Ascoli–Arzelàによる相対コンパクト性と、集合自体のコンパクト性に必要な閉性も区別しました。

## 検証結果

- 全23本・424コードブロックの内容ハッシュ、位置、文脈参照、検証先の対応を確認。今回はブロックの追加・削除・番号変更なし。
- 原稿から抽出したビルド対象を6ブロックから26ブロックへ拡張。追加した20ブロックは第6・7・8・10章の完成証明と確認コマンドです。
- 完成例と参照修正例のビルドに成功。名前を付けた28宣言の公理依存を検査し、`sorryAx` と未確認の追加公理への依存なし。
- 検査スクリプトの19テスト、段階1-Aで導入したエラー・警告・公理一覧の照合5件も成功。
- 分類は完成例・実行コマンド298、断片79、意図したエラー12、未完成24、抜粋11。分類は掲載目的であり、298件すべての実行成功を意味しません。

結果は [検証記録](catalog/stage1b-verification.json)、現在の対象一覧は [索引](catalog/index.json) と [README](README.md) にあります。新しい章別モジュール内の `BEGIN SOURCE` / `END SOURCE` を原稿と照合しています。

確認したMathlibの定義・定理は、固定版の [ProperSpace](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Topology/MetricSpace/ProperSpace.lean)、[コンパクト性と閉性・有界性](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Topology/MetricSpace/Bounded.lean)、[擬距離の引き戻し](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Topology/MetricSpace/Pseudo/Constructions.lean)、[lp空間](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/Normed/Lp/lpSpace.lean)、[有限次元性](https://github.com/leanprover-community/mathlib4/blob/5c8398df528176d9c87ccd9226ba8f7c8852d59c/Mathlib/Analysis/Normed/Module/FiniteDimension.lean) にあります。

## 残る作業

P1では、不動点定理のP1-04を段階1-C、積分・収束定理のP1-05・P1-06を段階1-Dで扱います。各章の全演習・出力・章番号・画像・Zenn表示の確認も未完了です。今回のビルド成功を全章の検証完了とは扱いません。
