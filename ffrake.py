#!/usr/bin/env python3
# ffmpegを使って、パートを抜き出してまとめるスクリプト
# print('usage: ./ffrake.py 入力ファイル 出力ファイル 開始時間1 終了時間1 ...')
import os
import subprocess
import sys


# 一時ファイルの削除
def deltmp(infile):
    try:
        os.remove(infile)
        # print('{}を削除しました'.format(infile))
    except Exception:
        pass
    return


# 時間を秒に変換 zipと複数のループ変数を使ってみた
def hms2sec(hms_str):
    sec, hms = 0, hms_str.split(':')
    # [[HH:]MM:]SSの時・分を省略できるように、reversedして秒から処理
    table = [1.0, 60.0, 3600.0]
    for t, s in zip(table, reversed(hms)):
        try:
            sec += t * float(s)
        except Exception:
            sys.exit('時間に文字か何かが紛れていますorz')
    return sec


# 入出力ファイルのチェック 内容には踏み込まない
def filechk(infile, outfile, ext_in):
    # 入力ファイルが無ければエラー
    if not os.path.exists(infile):
        sys.exit('入力ファイルが見つかりません')
    # 出力ファイルの拡張子を確認・修正する
    root_out = os.path.splitext(outfile)[0]
    ext_out = os.path.splitext(outfile)[1]
    if ext_out != ext_in:
        mes = '出力の拡張子{0}が入力の{1}と違ったので{1}に変更しました'
        print(mes.format(ext_out, ext_in))
        outfile = root_out + ext_in
    # 出力ファイルが被れば.bakにする、既に.bakがあれば消してしまう
    if os.path.exists(outfile):
        bakfile = root_out + '.bak'
        try:
            os.remove(bakfile)
            print('出力ファイルの.bakがあったのを削除しました')
        except Exception:
            pass
        os.rename(outfile, bakfile)
        print('出力ファイル名が被ったので前のを.bakにしました')
    return outfile


# ffmpegを使って部分ファイルを切り出す
def ffextract(infile, outfile, start_str, stop_str):
    # 前回異常終了などで一時ファイルが存在した場合は消しておく
    deltmp(outfile)
    # 開始時間
    start_sec = hms2sec(start_str)
    # 終了時間
    stop_sec = hms2sec(stop_str)
    # 経過時間
    dur_sec = stop_sec - start_sec
    if dur_sec <= 0:
        mes = '時間指定の異常な区間がありますorz(開始 {}, 終了 {}, 長さ {}秒)'
        sys.exit(mes.format(start_str, stop_str, dur_sec))
    dur_str = str(dur_sec)
    # ffmpegのコマンド生成
    cmd = 'ffmpeg -loglevel warning -ss ' + start_str \
        + ' -i ' + infile + ' -ss 0 -t ' + dur_str \
        + ' -acodec copy -vn -ignore_unknown ' + outfile
    print(cmd)
    subprocess.run(cmd.strip().split(' '))
    return


# ffmpegを使って部分ファイルを結合する
def ffconcat(infiles, listfile, outfile):
    # 結合用リストファイルの作成 リスト内包表記を使ってみた
    with open(listfile, 'w') as f:
        [f.write("file '" + infile + "'\n") for infile in infiles]
    # ffmpegのコマンド生成
    cmd = 'ffmpeg -loglevel warning -safe 0 -f concat ' \
        + '-i ' + listfile + ' -acodec copy ' + outfile
    print('結合:', cmd)
    subprocess.run(cmd.strip().split(' '))
    return


def main():
    # 引数取得 sys.argvで取得した要素の型はstr アンパックと*を使ってみた
    args = sys.argv
    try:
        command, infile, outfile, *ticks_str = args
    except Exception:
        mes = args[0] \
            + ' 入力ファイル 出力ファイル 開始時間1(HH:MM:SS) 終了1 開始2 終了2 ...'
        sys.exit('usage: {}'.format(mes))
    # 入出力拡張子が違うとffmpegのエラーが出ることがある。入力拡張子を変数に確保しておく
    ext_in = os.path.splitext(infile)[1]
    # 入力ファイルの存在確認と出力ファイルの諸々処理
    outfile = filechk(infile, outfile, ext_in)
    # 区間数は入力された時間の数/2, 奇数の入力はintで切り捨てて無視
    ticks_count = int(len(ticks_str)/2)
    # 一時ファイルのリストを内包表記とmapとlambdaで作成
    tmpfiles = \
        list(map(
            lambda i: 'ffrake' + str(i).zfill(3) + ext_in, range(ticks_count)))
    # ffmpegを使って部分ファイルを切り出す enumerateを使ってみた
    for i, tmpfile in enumerate(tmpfiles):
        print('抽出{}:'.format(i+1), end='')
        ffextract(infile, tmpfile, ticks_str[i*2], ticks_str[i*2+1])
    # 結合用リストファイル 名前は決め打ち
    listfile = 'ffconcat.lst'
    # ffmpegを使って部分ファイルを結合する
    ffconcat(tmpfiles, listfile, outfile)
    # 一時ファイル削除（デバッグ時はコメントアウトして残す）
    deltmp(listfile)
    [deltmp(f) for f in tmpfiles]
    # printで同じものを出すときはformat引数の番号を指定
    mes = '\n処理終了！\n{0}を確認して下さい(ex. mplayer {0} )\n'
    print(mes.format(outfile))


if __name__ == '__main__':
    main()
