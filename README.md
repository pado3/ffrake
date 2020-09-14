# ffrake
AAC等の音声ファイルから、必要な部分を抜き出してまとめるスクリプト


録音したファイルから、開始まで・中断・終了後などの不要部分を抜き去り、必要な部分だけをまとめた音声ファイルを作成するPython 3.xスクリプトです。（rake : 熊手）
必要部分の抽出と結合にffmpegを用い、エンコーディングなし（無劣化・高速）に編集します。
入出力ファイル名と編集ポイント（必要な部分の開始時間と終了時間）を一括入力することで、煩雑になりがちなffmpegのコマンドを自動的に生成し実行します。
ご利用は自己責任でお願いします。


動作環境
Python3とffmpegが必要です。動作確認は次の環境で行いました：
1. MacBook Air 2017,  Catalina 10.15.6, Python 3.7.7, ffmpeg version 4.2.2
2. TinkerBoard, Debian GNU/Linux 9.13 (stretch), Python 3.5.3, ffmpeg version 3.2.15-0+deb9u1
3. VAIO C (VPCCB4AJ), Windows 10 ver.2004, Python 3.8.6rc1, ffmpeg version git-2020-08-31-4a11a6f
手持ちのいくつかのAACとmp3で編集できることを確認しています。おそらくffmpegが対応している形式であれば動作すると思います。
なお、映像についてもffmpegのオプションを調整すれば対応可能だと思いますが、関心ありません。


使用方法
コマンドライン（コマンドプロンプト）から、次のように入力します：
python3 ffrake.py 入力ファイル名 出力ファイル名 開始時間1 終了時間1 開始2 終了2 ...
詳細は添付PDFを参照して下さい。


（参考）環境の構築方法
Python3は、開発などをするようでしたらAnacondaを導入するのがいいと思います。
但し、少々大きく重いです。
	Anaconda のインストール - python.jp 
	- https://www.python.jp/install/anaconda/ 
手軽に小さくインストールする方法は、OSによって異なります。
Debian系でしたら最初から入っていることが多いと思います。sudo apt update / upgrade推奨。
他のlinux系については分かりません。
MacOSでしたら公式パッケージが最も簡単確実だと思います。
	Download Python | Python.org
	- https://www.python.org/downloads/
Windows10でしたらコマンドプロンプトでpython3とタイプすると、アプリストアにジャンプします。
ちなみに私自身は、主にMacOSのコンソール + miエディタで開発しています。

ffmpegは、Debian系でしたらコンソールでsudo apt install ffmpeg一発です。
MacOS, Windows10は公式サイトから各OS用のビルド版を落としてくるのが簡単だと思います。
	Download FFmpeg 
	- https://ffmpeg.org/download.html
なお、Windows10ではパスを「システム環境設定」で手動で通す必要がありました。


以上
