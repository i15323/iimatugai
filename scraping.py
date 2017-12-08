# ---------------------------------- #
# Crawler for www.1101.com/iimatugai #
# ---------------------------------- #

# Author:      S. Komatsu (i15323@kagawa.kosen-ac.jp)
# Repository:  https://github.com/i15323/iimatugai

# モジュールの追加
import urllib.request
import re
import os
import csv
from collections import Counter
from bs4 import BeautifulSoup

# グローバル変数
URL_LIST = ""
WRITE_FILE_NAME = ""


def main():
    # URL Listを読み込む
    ul = []
    for row in open(URL_LIST, "r", encoding="UTF-8"):
        # コメント行の処理
        if row.find("#") == -1:
            ul.append(row)

    print("=== 終了したURL ===")

    # 全URLに対してクローリングを実行
    for url in ul:
        # 言い間違い例の全文を取得
        ft = getFullText(url)
        # 言い間違い例の部分を取得
        iimatigai = getIimatugai(url)
        
        # 言い間違いの分類を実行
        cl = classify(ft, url)

        # CSV形式で結果を保存
        writeFile(ft, iimatigai, cl, url)

        # 進行状況の表示
        print(url, end='')


def getFullText(url):
    # HTMLオブジェクト取得，テキスト変換
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("shift-jis")

    # HTMLのパース，スクレイピング
    soup = BeautifulSoup(html, "html.parser")

    # 条件付きTableタグの取得
    table = soup.findAll("table", attrs={'border': '0', 'cellspacing': '10', 'cellpadding' :'0'})

    # 詳細条件の設定，タグ除去
    f = []
    for e in table[2:-4]:
        e1 = e.findAll("td", attrs={'align': 'left', 'valign': 'top'})
        f.append(e1)

    pattern = re.compile("<.*?>")
    l = []
    for e in f:
        # 無駄な文字の削除
        e1 = pattern.sub("", str(e))
        e1 = e1.replace(',', '')
        e1 = e1.replace('[', '')
        e1 = e1.replace(']', '')
        e1 = e1.replace('\t', '')
        e1 = e1.replace(' ', '')
        # 改行コード変換(CRLF=>LF)
        e1 = e1.replace('\r\n', '\n')

        if e1 != '':
            l.append(e1)

    return l

def getIimatugai(url):
    # HTMLオブジェクト取得，テキスト変換
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('shift_jis')

    # HTMLのパース，スクレイピング
    soup = BeautifulSoup(html, "html.parser")

    # futojiタグの取得
    futoji = soup.find_all("span", class_="futoji")

    # 不要なタグの除去
    l = []
    pattern = re.compile("<.*?>")
    for e in futoji:
        e1 = pattern.sub("", str(e))
        l.append(e1)

    return l


def writeFile(f, i, c, url):
    # 書き込みファイル名の調整
    url = url.split("/")
    url = url[4]
    url = url.split(".")
    url = url[0]
    writeFileStream = open(WRITE_FILE_NAME + str(url) + "_" + str(c) + ".csv", "w", encoding="Shift-JIS")
    # writeFileStream = open(WRITE_FILE_NAME, "a", encoding="UTF-8")

    # 書き込み実行
    size = len(f)
    for c in range(size):
        try:
            writeFileStream.write('"' + f[c] + '",' + i[c])
            writeFileStream.write("\n")
        except UnicodeEncodeError:
            print("Oh..UnicodeEncodeError")

def classify(fullText, url):
    ''' 言い間違いの分類 '''
    # html ソース
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('shift_jis')
    
    fullText = str(html)
    
    # 使用CSVで言い間違いタイプを判別
    css_dict = {
                "css/yellow2009.css": "まつがい",
                "css/pink2009.css": "R指定",
                "css/black2009.css": "暗黒"
               }
    # 検索実行
    for k, v in css_dict.items():
        if fullText.find(k) != -1:
            return v

    # 本文中の用語で間違いタイプを判定
    class_list = [
                  "書きまつがい",
                  "元祖",
                  "まつがい電話",
                  "固有名詞",
                  "聞きまつがい",
                  "珍解答",
                  "誤メール",
                  "子供",
                  "かみ合わない",
                 ]

    for cl in class_list:
        if fullText.find(cl) != -1:
            return cl

    return "その他"


if __name__ == "__main__":
    print("Start crawling...")
    # ディレクトリごと一括処理
#    ld = os.listdir("urllist_archive")
#    for f in ld:
#        URL_LIST        = "./urllist_archive/" + f
#        WRITE_FILE_NAME = "./csv2/result_" + f
    URL_LIST        = "urllist_archive/urllist"
    WRITE_FILE_NAME = "csv3/urllist"
    main()
