# article01 検証記録

検証日：2026年9月18日（日本時間）

## 成果物と参照範囲

- 完成原稿：[lean4-ai-type-error.md](../../articles/lean4-ai-type-error.md)
- 採用タイトル：Lean 4の型エラーをAIに相談する前に、そろえたい3つの情報
- 本文：約2,759字。front matter、コード・出力・質問テンプレートの囲み、空白を除く簡易集計。Markdownの見出し等の記号は含む。
- 参照したもの：同梱の `PROMPT.md`、`BRIEF.md`、`references/chapter03.md`（主に3.2節）、`Ch03.lean`、`chapter03-catalog.md`、`sales-plan.md`、`book-config.yaml`、`lean-toolchain`、`lake-manifest.json`。
- ユーザーが指定した執筆要件を適用した。参照章の会話・体験談は記事の著者体験として転用せず、質問文は作成例として明記した。販売計画にある公開・募集・値上げ等は実施していない。
- ZIPは `output/article01-handoff/` に展開。展開済みの全9ファイルをZIP内の内容とバイト単位で照合し、一致を確認。参照資料、既存Lean環境、既刊原稿、`sources/` は変更していない。

## 実行環境

実際に使用したLean：

```text
Lean (version 4.29.0-rc6, arm64-apple-darwin24.6.0, commit 00659f8e6071d7e46131ed643bf8003b99b044e9, Release)
```

実行ファイル：elanにインストール済みのLean 4.29.0-rc6。以下の再現コマンドでは、その版を明示的に選択する。

同梱 `lean-toolchain` の `leanprover/lean4:v4.29.0-rc6` と一致する固定環境。最新版という扱いはしていない。

同梱manifestのMathlib rev：`5c8398df528176d9c87ccd9226ba8f7c8852d59c`。BRIEFにある既存Lean環境の `.lake/packages/mathlib` のHEADとも一致した。ただし記事の例はLean標準の定義だけで動くため、`import Mathlib` を省略し、Mathlibをロードせずに検証した。Mathlib全体のビルドや既刊全章の再検証は実施していない。

## 実行したファイルと結果

作業ディレクトリ：この成果物フォルダの `code/`。次のコマンドをそれぞれ別プロセスで実行し、標準出力・標準エラーをログに保存した。

```sh
lean +leanprover/lean4:v4.29.0-rc6 Failure.lean
lean +leanprover/lean4:v4.29.0-rc6 Fixed.lean
```

別環境ではLean 4.29.0-rc6を選択したうえで、同じファイルに対して `lean Failure.lean` と `lean Fixed.lean` を実行できる。Mathlibのインストールは不要。

| ファイル | 終了コード | 結果 |
| --- | --- | --- |
| [Failure.lean](code/Failure.lean) | 1 | 意図した型不一致を1件確認。文字列 `"hello"` の型が `String` で、要求される `Nat` と一致しない |
| [Fixed.lean](code/Fixed.lean) | 0 | エラー・警告なし。型表示、評価結果12・5・105を確認。任意の自然数についての `example` も検査を通過 |

証拠：[失敗ログ](logs/Failure.log)、[成功ログ](logs/Fixed.log)、[環境ログ](logs/environment.log)、[コマンドと終了コード](logs/results.json)。

失敗例の出力は元章の要約から転記せず、新規実行結果の全文を掲載した。記事内の質問記入例にも同じコードと全文を収録した。掲載Leanブロック3個（失敗例、質問内の失敗例、修正例）が対応する `.lean` ファイルと一致すること、掲載出力が実測ログと一致することを機械的に確認した。

数学的意図は「任意の自然数nに対しn+5を返す」。修正は呼び出しの引数を文字列から自然数に変えるもので、関数定義・型を維持している。`example (n : Nat) : add_five n = n + 5 := by rfl` はその定義に対応する命題を検査する。完成例に `sorry` や追加の公理宣言はない。名前付き定理を追加していないため、`#print axioms` は実施していない。

## リンク確認

2026年9月18日にWeb取得で次を確認した。

- [既刊トップ](https://zenn.dev/matsuteru/books/ab366ea6fa62f6)：取得可能。書名は『AI駆動で学ぶ Lean 4 入門』。序文・第1章・第2章に無料公開の表示あり。
- [無料の序文](https://zenn.dev/matsuteru/books/ab366ea6fa62f6/viewer/e8d7ab)：取得可能。「はじめに」「Chapter 01無料公開」の表示あり。記事末尾のリンク先に採用。

取得結果にはトップが「1週間前」、序文が「4週間前」のクロール情報と表示され、最新公開状態をリアルタイムに確認したものではない。ローカル設定の『Lean 4で学ぶ形式証明と線形代数【第1巻】』との違いを踏まえ、記事では特定の書名を断定せず「Lean 4入門の第1巻」とした。紹介文は参照資料の範囲に限定し、未確認の続巻・増補や価格を掲載していない。

## 編集上の確認

- 失敗例 → エラー読解 → 3情報 → 記入済み質問 → 修正と再確認 → 空欄テンプレート、を一例で構成。
- 自然数の計算と文字列の解析で必要な修正が異なることを説明。
- 質問には数学的意図を含め、環境と試行内容を補足に配置。
- テンプレートに「仮定・結論を勝手に変えない」「変更理由を説明」「未確認の補題名を断定しない」を明記。
- `#check` の限界と、計算例・一般的な証明の違いを説明。
- 書籍案内は最後の1段落のみ。記事単独で修正・確認まで完結。
- `type: tech`、`topics: [lean4, mathlib, ai]`、`published: false` を設定。
- 掲載コード・出力の照合、参照資料の同一性、字数、成果物のSHA-256は [editorial-check.json](logs/editorial-check.json) に記録。

## PR作成時の追加確認

- リポジトリ配置後の失敗例・修正例をLean 4.29.0-rc6で再実行し、終了コードと出力が保存済みログに完全一致することを確認。
- Node.js v24.14.1、既存環境の `zenn-markdown-html` 0.5.4で原稿をHTMLへ変換できることを確認。生成HTMLにコード例と無料序文リンクが含まれること、YAMLとして `published: false`、記事種別、topicsを読み取れることを確認。ブラウザでの見た目の確認は未実施。

## slug修正時の確認

- `article01` は9文字でZennの12〜50文字制約を満たさなかったため、記事を `articles/lean4-ai-type-error.md` へ改名。
- 新slug `lean4-ai-type-error` は19文字。`articles/` 内の全Markdownファイルが `[a-z0-9_-]{12,50}` に一致することを確認。
- 関連リンク・ハッシュ記録のパスを更新。記事本文のSHA-256が既存の検証記録と一致し、`published: false` が維持されていることを確認。

## 未実行の範囲と、残る公開前確認

1. Zennの実プレビューで、front matter、表、4連バッククォート内の質問文、スマートフォンでの読みやすさを確認する。ローカルでMarkdown構造は点検済みだが、Zenn画面上の描画は未確認。
2. 公開直前に無料序文のリンクをブラウザで開き、無料閲覧と現在の表示内容を確認する。今回のリンク確認はクロール済み情報を含むWeb取得であり、最新の改訂反映確認ではない。
3. 記事の実行可能なLeanコードはすべて実行済み。空欄テンプレートは説明用で、実行対象ではない。別のLean版・OS・エディタ表示での再検証、文字列解析処理の実装、実際のAIへの質問送信は未実施。

原稿作成時には自動公開、GitHubへの反映、他者への連絡は行っていない。その後のユーザーの依頼に従い、記事を `articles/lean4-ai-type-error.md`、検証資料を `docs/article01/` に配置してPRを作成する。`published: false` は維持し、公開・マージは行わない。ログ内の実行パスは、個人環境の絶対パスから再現可能な相対パス・版指定コマンドへ正規化した。
