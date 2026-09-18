# 段階5の図・画面の照合

旧原稿の画像参照53件（ローカル41、外部12）を照合し、掲載を31件（ローカル19、外部12）へ整理しました。既存のローカルPNG42枚を目視し、誤参照と図そのものの不正確さを区別しました。画像ファイルの編集・削除はしていません。

## 主な変更

| 原稿 | 対応 |
|---|---|
| [intro](../../books/lean4-formalization/intro.md) | 旧4巻構成の図を、現状と予定を分けた表へ変更。 |
| [ch03](../../books/lean4-formalization/ch03.md) | 型の宇宙の誤記と、質問テンプレートの不一致を表・文章へ変更。外部画面10枚の内容を照合。 |
| [ch04](../../books/lean4-formalization/ch04.md) | 探索コマンドから無条件に証明完了へ進む図を削除し、本文の手順で説明。 |
| [ch05](../../books/lean4-formalization/ch05.md) | 次元定理の古いAPI・証明手順の図を、現在の証明に合わせた表へ変更。 |
| [ch06](../../books/lean4-formalization/ch06.md) | 画面とされていた概念図の誤参照を修正。近傍と開近傍は数式で区別。 |
| [ch07](../../books/lean4-formalization/ch07.md) | 三角不等式・開球の参照先を修正。開集合の条件は数式へ変更。 |
| [ch08](../../books/lean4-formalization/ch08.md) | 構造の継承、全域での連続性、コンパクト性は表・数式・文章へ変更。近傍の図は基底とフィルターを区別。 |
| [ch09](../../books/lean4-formalization/ch09.md) | 実数と有理数の対比の参照先を修正。誤ったCauchy列の画像を文章へ変更。 |
| [ch10](../../books/lean4-formalization/ch10.md) | ソースコード画面・証明画面とされていた別図を削除。有限次元と無限次元の違いは閉単位球を明記した表へ変更。 |
| [ch11](../../books/lean4-formalization/ch11.md) | 縮小写像の反復図へ参照を修正。非空性と完備性、軌道の模式性を明示。 |
| [ch12](../../books/lean4-formalization/ch12.md) | 旧巻構成の図を章対応表へ変更。σ-代数の要素が集合であることを明示。 |
| [ch13](../../books/lean4-formalization/ch13.md) | 測度の値域と定義域を補足。誤字・条件不足の比較画像を条件付きの表へ変更。 |
| [ch14](../../books/lean4-formalization/ch14.md) | 逆像と逆関数を区別。 |
| [ch15](../../books/lean4-formalization/ch15.md) | 中点近似と下からの単調近似を区別。積分の図を実際の内容に合わせる。 |
| [ch16](../../books/lean4-formalization/ch16.md) | 積分の型・可測性・規約値の誤解を生む図を表と文章へ変更。 |
| [ch17](../../books/lean4-formalization/ch17.md) | 各グラフの定義域・添字・横軸を明示。図の正弦関数列と演習の式の違いを説明。 |
| [ch18](../../books/lean4-formalization/ch18.md) | 包含関係は真の包含と限らないことを補足。確率空間を構成するデータと条件を表へ変更。 |

## 最終的に掲載する画像

全31枚をブラウザーで直接表示し、読み込みと内容を確認しました。外部スクリーンショットは撮影時の記録として扱います。数値は読み込んだ画像の画素数です。

| 原稿・図番号 | 画像 | 説明 | 大きさ |
|---|---|---|---|
| [ch01・図1-1](../../books/lean4-formalization/ch01.md) | [#eval "Hello, Lean!" の実行結果](https://storage.googleapis.com/zenn-user-upload/f90c9b22fefc-20260324.png) | #evalで文字列を評価した撮影時の画面です。定理の証明完了を示す画面ではありません。 | 1400×237 |
| [ch01・図1-2](../../books/lean4-formalization/ch01.md) | [1 + 1 = 2 の証明後のInfoView](https://storage.googleapis.com/zenn-user-upload/9a07ccebff91-20260324.png) | 画像では定理名がtestですが、命題と証明は本文のfirst_theoremと同じです。No goalsと警告の有無を併せて確認します。 | 1400×765 |
| [ch01・図1-3](../../books/lean4-formalization/ch01.md) | [ゴール確認、タクティク適用、新しいゴール確認を繰り返す模式図](../../images/vol1/fig-03.png) | InfoViewを使う手順の模式図です。実画面ではありません。ゴールが閉じた後は、ファイル全体のエラー・警告も確認します。 | 2617×1446 |
| [ch03・図3-1](../../books/lean4-formalization/ch03.md) | [rfl失敗のエラー画面](https://storage.googleapis.com/zenn-user-upload/571065a5753e-20260324.png) | 自然数の加法の交換法則にrflを使い、失敗した画面です。 | 1400×765 |
| [ch03・図3-2](../../books/lean4-formalization/ch03.md) | [型不一致エラー画面](https://storage.googleapis.com/zenn-user-upload/b2bc302415eb-20260324.png) | 自然数を受け取るadd_fiveに文字列を渡した型不一致です。 | 1400×765 |
| [ch03・図3-3](../../books/lean4-formalization/ch03.md) | [3点セット質問の送信画面](https://storage.googleapis.com/zenn-user-upload/3cd8c0c572b6-20260324.png) | コード・エラー・数学的意図を伝えた質問の記録です。再現時はLeanとMathlibの版も添えます。 | 1228×530 |
| [ch03・図3-4](../../books/lean4-formalization/ch03.md) | [Claudeの回答画面](https://storage.googleapis.com/zenn-user-upload/7a8c90c5b798-20260324.png) | 引数の型が異なることを説明する回答の記録です。回答の正しさは別途Leanで確認します。 | 1400×375 |
| [ch03・図3-5](../../books/lean4-formalization/ch03.md) | [修正後の動作確認画面](https://storage.googleapis.com/zenn-user-upload/9d1a6ed3a7ed-20260324.png) | 自然数3・0・100を渡した評価結果です。カーソル位置のNo info foundはエラーを意味しません。 | 1400×765 |
| [ch03・図3-6](../../books/lean4-formalization/ch03.md) | [Unknown constantエラー画面](https://storage.googleapis.com/zenn-user-upload/d0e20bd999d0-20260324.png) | 存在しない名前Nat.add_comm_wrongに対するエラーです。 | 1400×765 |
| [ch03・図3-7](../../books/lean4-formalization/ch03.md) | [exact?成功画面](https://storage.googleapis.com/zenn-user-upload/6034ff2cab45-20260324.png) | exact?がexact Nat.add_comm a bを提案した画面です。提案の表示は版や文脈によって変わります。 | 1400×765 |
| [ch03・図3-8](../../books/lean4-formalization/ch03.md) | [failed to synthesize instanceエラー画面](https://storage.googleapis.com/zenn-user-upload/bbe6380ae5b9-20260324.png) | 加法のインスタンスが見つからない画面です。メタ変数の番号は固定ではありません。 | 1400×765 |
| [ch03・図3-9](../../books/lean4-formalization/ch03.md) | [型クラス追加後・エラー消滅画面](https://storage.googleapis.com/zenn-user-upload/3093b01750b5-20260324.png) | [Add α]を加え、a + bの型を確認した画面です。加法の交換律を証明した画面ではありません。 | 1400×765 |
| [ch03・図3-10](../../books/lean4-formalization/ch03.md) | [sorry黄色波線警告画面](https://storage.googleapis.com/zenn-user-upload/69cbbf323933-20260324.png) | sorryによってNo goalsになっていても、未証明であることを示す警告が残っています。 | 1400×765 |
| [ch04・図4-1](../../books/lean4-formalization/ch04.md) | [rfl、ring、simpなどの代表的な用途を並べた表](../../images/vol1/fig-04.png) | 用途の概略です。ringは可換半環・可換環の多項式等式を扱い、applyの後には補題の仮定が新しいゴールとして残る場合があります。 | 2385×1792 |
| [ch05・図5-1](../../books/lean4-formalization/ch05.md) | [線形写像、核、像、有限次元の数学とLeanの記法の対応](../../images/vol1/fig-07.png) | 有限次元の場合の対応です。最下段のMathlib定理は像の次元＋核の次元の順なので、本文では加算の順番を揃えています。 | 2617×1677 |
| [ch06・図6-1](../../books/lean4-formalization/ch06.md) | [1/nが0に近づく様子をフィルターの望遠鏡に例えた図](../../images/vol2/fig-01.png) | 収束を捉えるための比喩です。フィルターが数値や極限を計算するという意味ではありません。 | 2385×1067 |
| [ch07・図7-1](../../books/lean4-formalization/ch07.md) | [3点x、y、zを結ぶ距離の三角不等式](../../images/vol2/fig-04.png) | 直接の距離は、別の点を経由した距離の和以下です。 | 1919×1529 |
| [ch07・図7-2](../../books/lean4-formalization/ch07.md) | [中心xから距離ε未満の点を集めたユークリッド平面の開球](../../images/vol2/fig-05.png) | 平面の開球を描いた模式図です。円周上の点は含みません。閉球では距離が半径以下の点を含めます。 | 1677×1791 |
| [ch08・図8-1](../../books/lean4-formalization/ch08.md) | [点xを含む開集合を使って近傍フィルターを構成する模式図](../../images/vol2/fig-08.png) | 図中の「開集合のみ」は構成に使う開近傍を指します。nhds xの要素には、それらを含む開でない集合も含まれます。円や入れ子は模式的で、距離や全開近傍の入れ子関係を仮定しません。 | 1536×1760 |
| [ch09・図9-1](../../books/lean4-formalization/ch09.md) | [実数の完備性と、平方根2へ近づく有理数列の対比](../../images/vol2/fig-11.png) | 実数ではCauchy列が実数へ収束します。有理数では、実数としての極限が有理数に属さないCauchy列が存在します。 | 3570×1545 |
| [ch11・図11-1](../../books/lean4-formalization/ch11.md) | [縮小写像の反復列が不動点へ近づく模式図](../../images/vol2/fig-15.png) | 非空な完備距離空間上の縮小写像の反復を表します。図は実数直線で描いていますが、一般の反復列が単調に動くとは限りません。 | 2152×1529 |
| [ch12・図12-1](../../books/lean4-formalization/ch12.md) | [べき集合の中のσ-代数と、その外にある非可測集合の模式図](../../images/vol3/fig-03.png) | 各点はXの部分集合を表します。選んだσ-代数に属さない集合を非可測と呼びます。σ-代数がべき集合全体に一致する場合もあります。 | 1455×1296 |
| [ch13・図13-1](../../books/lean4-formalization/ch13.md) | [可測集合に非負拡張実数の値を割り当てる測度の模式図](../../images/vol3/fig-04.png) | 数学での可測集合上の測度を表します。MathlibのMeasureは可測でない集合にも値を持ち、可算加法性などには可測性の仮定が使われます。 | 1687×1298 |
| [ch14・図14-1](../../books/lean4-formalization/ch14.md) | [実数値可測関数とBorel集合の逆像を示す図](../../images/vol3/fig-06.png) | 値域が実数の例です。点線の逆像は集合に対する操作で、逆関数の存在を意味しません。 | 1687×1292 |
| [ch15・図15-1](../../books/lean4-formalization/ch15.md) | [平方根関数を分割数1、2、4の中点の値で近似する階段関数](../../images/vol3/fig-07.png) | 中点の値を使った単関数近似です。この図の近似列は下から単調増加する列ではありません。上の単調近似の主張とは区別してください。 | 3269×1191 |
| [ch15・図15-2](../../books/lean4-formalization/ch15.md) | [各値とその逆像の測度を掛け、有限和を取る単関数積分の図](../../images/vol3/fig-08.png) | 値域の各値cについて、cとその逆像の測度を掛けて足します。定数単関数の計算は本文の別の例で確認します。 | 2385×1415 |
| [ch17・図17-1](../../books/lean4-formalization/ch17.md) | [区間0から1でn/(n+1)倍のxがxへ単調増加する関数列](../../images/vol3/fig-11.png) | 非負可測関数の単調増加の具体的な模式例です。区間[0,1]のLebesgue測度で積分も1/2へ増加します。本文の一般定理は非負拡張実数値で述べています。 | 1878×1423 |
| [ch17・図17-2](../../books/lean4-formalization/ch17.md) | [区間nからn+1の指示関数が右へ移動し、各点で0に収束する図](../../images/vol3/fig-12.png) | 実数全体のLebesgue測度で各積分は1ですが、点ごとの極限は0です。Fatouの補題で真の不等式になる例です。 | 1874×1423 |
| [ch17・図17-3](../../books/lean4-formalization/ch17.md) | [正弦関数列の点ごとの収束、定数1による支配、積分値の収束を示す3枚のグラフ](../../images/vol3/fig-13.png) | 区間[0,1]上のsin(nπx)/n（n≥1）の例です。左・中央の横軸はx、右はnです。有限区間なので優関数1は可積分です。章末演習のsin(nx)/nとは周波数が異なります。 | 3569×1392 |
| [ch18・図18-1](../../books/lean4-formalization/ch18.md) | [有限測度上のL∞、L2、L1の包含関係を示す入れ子図](../../images/vol3/fig-14.png) | 包含は真の包含とは限りません。a.e.同値類を自然に対応させた包含です。無限測度上では一般に成り立ちません。 | 1455×1298 |
| [ch18・図18-2](../../books/lean4-formalization/ch18.md) | [実数値確率変数と、Borel集合の逆像が事象になる関係を示す図](../../images/vol3/fig-16.png) | Borel集合Bの逆像が事象になります。確率はP(X⁻¹(B))で表します。逆像は逆関数を意味しません。 | 1687×1412 |
