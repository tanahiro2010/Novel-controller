import os
import sys
import requests
import json
import time
from bs4 import BeautifulSoup

search_help = """
0: 未選択〔未選択〕
101: 異世界〔恋愛〕
102: 現実世界〔恋愛〕
201: ハイファンタジー〔ファンタジー〕
202: ローファンタジー〔ファンタジー〕
301: 純文学〔文芸〕
302: ヒューマンドラマ〔文芸〕
303: 歴史〔文芸〕
304: 推理〔文芸〕
305: ホラー〔文芸〕
306: アクション〔文芸〕
307: コメディー〔文芸〕
401: VRゲーム〔SF〕
402: 宇宙〔SF〕
403: 空想科学〔SF〕
404: パニック〔SF〕
9901: 童話〔その他〕
9902: 詩〔その他〕
9903: エッセイ〔その他〕
9904: リプレイ〔その他〕
9999: その他〔その他〕
9801: ノンジャンル〔ノンジャンル〕

connect to hyphen(-)
"""
def main():
    global search_help
    mode = sys.argv[1]

    if mode == "download":
        print(f"{time.time()} >> start download")
        ncode = sys.argv[2].lower()
        print(f"ncode = {ncode}")
        base_url = f"https://ncode.syosetu.com/{ncode}/"
        api_url = f"https://api.syosetu.com/novelapi/api?out=json&ncode={ncode}"
        api_response = json.loads(requests.get(api_url).content)[1]
        title = api_response["title"]
        general_all_no = api_response["general_all_no"]
        print(f"[INFO {time.time()}] title: #{title}")
        print(f"[INFO {time.time()}] general_all_no: {general_all_no}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }
        text = ""
        for i in range(general_all_no):
            book_url = base_url + str(i+1)
            print(f"[INFO {time.time()}] book_url: {book_url}. {i}/{general_all_no}")
            book_response = requests.get(book_url, headers=headers).content
            html = BeautifulSoup(book_response, 'html.parser')
            text += html.select("#novel_honbun")[0].text
        with open(f"{title}.txt", "w") as f:
            f.write(text)
        os.system("start {}.txt".format(title))
        return True
    elif mode == "search":
        search_url = f"https://api.syosetu.com/novelapi/api?genre={str(sys.argv[2])}&out=json"
        print(f"[INFO {time.time()}] search_url: {search_url}")
        response = json.loads(requests.get(search_url).content)
        del response[0]
        print(f"[INFO {time.time()}] start analysis.")
        for book in response:
            print('======================================================')
            print(f"Book title: {book['title']}")
            print(f"Book ncode: {book['ncode']}")
            print(f"Book url: https://ncode.syosetu.com/{book['ncode']}")
            print(f"Book story=======\n {book['story']}\n================")
            print(f"Author id: {book['userid']}")
            print('======================================================')
        return True
    elif mode == "help":
        print(f"Mode list\noption | text\ndownload \"ncode\" | book download\nsearch \"search code\" | book search\n\nsearch code{search_help}")
    return

if __name__ == "__main__":
    main()