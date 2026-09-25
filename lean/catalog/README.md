# 原稿コードの分類と検証先

この表の分類は掲載目的を表し、実行成功の判定ではありません。完成例に不備があっても完成例のまま修正対象として残します。

前回の一次点検は各ブロックに import Mathlib を補って独立実行した結果です。本文の前提を引き継がないため、正常終了もエラーも完成度の判定には使いません。

現在のビルド対象は [README](../README.md) を参照してください。断片の文脈指定は組立て方の指示で、組立て済み・証明済みを意味しません。

生のコードは `python3 scripts/catalog.py extract` で `.generated/raw/ID.lean` に、importも含めて原文どおり抽出されます。

| 分類 | 数 |
|---|---:|
| 完成例・実行コマンド | 345 |
| 前後に続く断片 | 49 |
| 意図的なエラー例 | 12 |
| 練習問題・未完成の骨格 | 23 |
| 説明用の抜粋 | 0 |

対応表と機械可読データは章ごとに分けています。原稿全体の版とファイル一覧は [index.json](index.json) に記録しています。

| 原稿 | ブロック数 | 分類・文脈の表 | 機械可読データ |
|---|---:|---|---|
| [ch01.md](../../books/lean4-formalization/ch01.md) | 14 | [対応表](chapters/ch01.md) | [JSON](chapters/ch01.json) |
| [ch02.md](../../books/lean4-formalization/ch02.md) | 19 | [対応表](chapters/ch02.md) | [JSON](chapters/ch02.json) |
| [ch03.md](../../books/lean4-formalization/ch03.md) | 24 | [対応表](chapters/ch03.md) | [JSON](chapters/ch03.json) |
| [ch04.md](../../books/lean4-formalization/ch04.md) | 23 | [対応表](chapters/ch04.md) | [JSON](chapters/ch04.json) |
| [ch05.md](../../books/lean4-formalization/ch05.md) | 31 | [対応表](chapters/ch05.md) | [JSON](chapters/ch05.json) |
| [ch06.md](../../books/lean4-formalization/ch06.md) | 48 | [対応表](chapters/ch06.md) | [JSON](chapters/ch06.json) |
| [ch07.md](../../books/lean4-formalization/ch07.md) | 41 | [対応表](chapters/ch07.md) | [JSON](chapters/ch07.json) |
| [ch08.md](../../books/lean4-formalization/ch08.md) | 36 | [対応表](chapters/ch08.md) | [JSON](chapters/ch08.json) |
| [ch09.md](../../books/lean4-formalization/ch09.md) | 28 | [対応表](chapters/ch09.md) | [JSON](chapters/ch09.json) |
| [ch10.md](../../books/lean4-formalization/ch10.md) | 26 | [対応表](chapters/ch10.md) | [JSON](chapters/ch10.json) |
| [ch11.md](../../books/lean4-formalization/ch11.md) | 26 | [対応表](chapters/ch11.md) | [JSON](chapters/ch11.json) |
| [ch12.md](../../books/lean4-formalization/ch12.md) | 19 | [対応表](chapters/ch12.md) | [JSON](chapters/ch12.json) |
| [ch13.md](../../books/lean4-formalization/ch13.md) | 17 | [対応表](chapters/ch13.md) | [JSON](chapters/ch13.json) |
| [ch14.md](../../books/lean4-formalization/ch14.md) | 15 | [対応表](chapters/ch14.md) | [JSON](chapters/ch14.json) |
| [ch15.md](../../books/lean4-formalization/ch15.md) | 12 | [対応表](chapters/ch15.md) | [JSON](chapters/ch15.json) |
| [ch16.md](../../books/lean4-formalization/ch16.md) | 17 | [対応表](chapters/ch16.md) | [JSON](chapters/ch16.json) |
| [ch17.md](../../books/lean4-formalization/ch17.md) | 13 | [対応表](chapters/ch17.md) | [JSON](chapters/ch17.json) |
| [ch18.md](../../books/lean4-formalization/ch18.md) | 19 | [対応表](chapters/ch18.md) | [JSON](chapters/ch18.json) |
| [intro.md](../../books/lean4-formalization/intro.md) | 1 | [対応表](chapters/intro.md) | [JSON](chapters/intro.json) |
| [part1.md](../../books/lean4-formalization/part1.md) | 0 | Leanコードなし | — |
| [part2.md](../../books/lean4-formalization/part2.md) | 0 | Leanコードなし | — |
| [part3.md](../../books/lean4-formalization/part3.md) | 0 | Leanコードなし | — |
| [part4.md](../../books/lean4-formalization/part4.md) | 0 | Leanコードなし | — |
