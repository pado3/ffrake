#!/usr/bin/env python3
# ffmpegを使って、パートを抜き出してまとめるスクリプト
# print('usage: ./ffrake.py 入力ファイル 出力ファイル 開始時間1 終了時間1 ...')
import os
import subprocess
import sys


# 時間を秒に変換 zipと複数のループ変数を使ってみた
def hms2sec(hms_str):
    sec = 0
    hms = hms_str.split(':')
    # [[HH:]MM:]SSが処理できるようにreversedして秒から処理
    table = [1, 60, 3600]
    for s, t in zip(table, reversed(hms)):
        try:
            sec += s * float(t)
        except Exception:
            sys.exit('時間に文字か何かが紛れていますorz')
    return sec


# 入出力ファイルのチェック 内容には踏み込まない
def filechk(infile, outfile):
    # 入力ファイルが無ければエラー
    if not os.path.exists(infile):
        sys.exit('入力ファイルが見つかりません')
    # 出力ファイルが被れば.bakにする, 既に.bakがあれば消してしまう
    if os.path.exists(outfile):
        oldfile = outfile
        bakfile = os.path.splitext(oldfile)[0] + '.bak'
        if os.path.exists(bakfile):
            os.remove(bakfile)
            print('出力ファイルの.bakがあったのを削除しました')
        os.rename(oldfile, bakfile)
        print('出力ファイルが被ったので.bakにしました')
    return


# ffmpegを使って部分ファイルを切り出す
def ffextract(infile, outfile, start_str, stop_str):
    # 入出力ファイルのチェック
    filechk(infile, outfile)
    # 開始時間
    start_sec = hms2sec(start_str)
    # 終了時間
    stop_sec = hms2sec(stop_str)
    # 経過時間
    dur_sec = stop_sec - start_sec
    if dur_sec <= 0:
        sys.exit('時間指定の異常な区間がありますorz(長さが{}秒)'.format(dur_sec))
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
    # 入出力ファイルのチェック(入力は最後のだけ)
    filechk(infiles[-1], outfile)
    # 結合用リストファイルの作成
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
    # 入出力の拡張子が違うとffmpegのエラーが出ることがある。入力拡張子を確保する
    ext_in = os.path.splitext(infile)[1]
    # ffmpegを使って部分ファイルを切り出す
    ticks_count = int(len(ticks_str)/2)
    tmpfiles = []
    for i in range(ticks_count):
        tmpfile = 'ffrake' + str(i).zfill(3) + ext_in
        tmpfiles.append(tmpfile)
        if os.path.exists(tmpfile):
            os.remove(tmpfile)
        print('抽出{}:'.format(i+1), end='')
        ffextract(infile, tmpfile, ticks_str[i*2], ticks_str[i*2+1])
    # ffmpegを使って部分ファイルを結合する
    # 結合用リストファイル
    listfile = 'ffconcat.lst'
    if os.path.splitext(outfile)[1] != ext_in:
        outfile = os.path.splitext(outfile)[0] + ext_in
        print("出力ファイルの拡張子が入力と違ったので修正しました")
    ffconcat(tmpfiles, listfile, outfile)
    # ごみ掃除
    if os.path.exists(listfile):
        os.remove(listfile)
    for tmpfile in tmpfiles:
        if os.path.exists(tmpfile):
            os.remove(tmpfile)
    mes = '\n処理終了！\n{}を確認して下さい(ex. mplayer {} )\n'
    print(mes.format(outfile, outfile))


if __name__ == '__main__':
    main()
