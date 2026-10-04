# -*- coding: utf-8 -*-
"""
rebrand_channel.py — đổi mặt kênh YouTube từ `사우 오디오` sang `地形と地名の日本史`.

⏹ ĐÃ THI HÀNH XONG 2026-09-16 — nhưng **BẰNG TAY TRONG STUDIO**, không qua file này: token
   hiện có chỉ đọc được (xem tools/auth.py). Giữ file vì hai lý do: (a) nó là bản LƯU nội dung
   branding đang chạy trên kênh, (b) khi nào có token ghi thì `--apply` dùng lại được ngay.
   ⚠️ Sửa branding trên Studio mà không sửa DESC/KEYWORDS ở đây = hai bản lệch nhau.

🔴 MẶC ĐỊNH LÀ DRY-RUN. Muốn ghi thật phải gõ `--apply` (và user phải gật trước —
   memory `feedback_chot_truoc_khi_dang`: chốt trước MỌI cú ghi lên kênh).

Làm 2 việc, tách cờ riêng để bấm được từng cái:
    --apply --brand    : channels.update (title / description / keywords / country / lang)
    --apply --private  : videos.update  đặt 3 video KR cũ thành private

⚠️ KHÔNG làm được bằng API, phải vào Studio bằng tay (xem cuối file):
    handle (@...), avatar, banner, watermark, trailer, playlist, "kênh dành cho trẻ em".
"""
import io, sys, json, argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
CH_ID = "UCfXuolJMQ-3CMpmTeQVkwKA"

TITLE = "地形と地名の日本史"

DESC = """その地形が、その歴史を決めた。

渋谷はなぜ「谷」なのか。江戸はなぜ、日本一の城を築けたのか。
この番組では、国土地理院の地図データを使って、地形と地名から日本の歴史を読み解いていきます。陰影起伏図、色別標高図、治水地形分類図、標高タイル、そして1961年の空中写真。数字と地図で「なぜ」を確かめながら、ひとつの土地の物語を15〜20分でたどります。

■ こんな話をしています
・消えた川と暗渠 ― 渋谷川、利根川東遷、荒川放水路
・なぜこの町はここにあるのか ― 台地・扇状地・河岸段丘と、都市の立地
・土地の履歴 ― 空中写真で見る、60年前のその場所
・地名の由来 ― 「谷」「窪」「沢」が教える、水の通り道
・治水と土木の人物史 ― 川のかたちを変えた人たち

地理や歴史が好きな方、古地図や街歩きが好きな方に楽しんでいただける内容です。

■ 公開
毎週 火曜・金曜・日曜の20時。

■ 出典・データ
国土地理院ウェブサイト（淡色地図・陰影起伏図・色別標高図・傾斜量図・治水地形分類図・土地条件図・標高タイル・空中写真）
https://maps.gsi.go.jp/development/ichiran.html

※ 本チャンネルは土地の成り立ちを紹介するものです。個別の土地の安全性や資産価値を判断するものではありません。お住まいの地域については、自治体のハザードマップをご確認ください。
※ 音声は合成音声を使用しています。

#地形 #地名 #日本史"""

KEYWORDS = ("地形 地名 河川 地理 日本史 歴史 解説 地形図 標高 断面図 暗渠 旧河道 治水 "
            "古地図 空中写真 ブラタモリ 街歩き 地名の由来 土地の履歴 台地 扇状地 河岸段丘 "
            "東京 江戸 利根川 渋谷川 国土地理院 地理院地図")


def creds():
    c = Credentials.from_authorized_user_file(str(ROOT / "credentials" / "token.json"))
    if not c.valid:
        c.refresh(Request())
        (ROOT / "credentials" / "token.json").write_text(c.to_json(), encoding="utf-8")
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="ghi that len kenh")
    ap.add_argument("--brand", action="store_true")
    ap.add_argument("--private", action="store_true")
    g = ap.parse_args()
    if not (g.brand or g.private):
        g.brand = g.private = True
    yt = build("youtube", "v3", credentials=creds())

    cur = yt.channels().list(part="snippet,brandingSettings,contentDetails", id=CH_ID).execute()["items"][0]
    print("KENH HIEN TAI : %s | country=%s | lang=%s"
          % (cur["snippet"]["title"],
             cur["brandingSettings"].get("channel", {}).get("country"),
             cur["snippet"].get("defaultLanguage")))
    print("SE DOI THANH  : %s | country=JP | lang=ja" % TITLE)
    print("description   : %d ky | keywords: %d cum" % (len(DESC), len(KEYWORDS.split())))

    if g.brand:
        body = {
            "id": CH_ID,
            "brandingSettings": {
                "channel": {
                    "title": TITLE,
                    "description": DESC,
                    "keywords": KEYWORDS,
                    "country": "JP",
                    "defaultLanguage": "ja",
                }
            },
        }
        if g.apply:
            r = yt.channels().update(part="brandingSettings", body=body).execute()
            print("✅ BRAND DA GHI:", r["brandingSettings"]["channel"].get("title"))
        else:
            print("… (dry-run) se goi channels.update part=brandingSettings")

    if g.private:
        up = cur["contentDetails"]["relatedPlaylists"]["uploads"]
        items = yt.playlistItems().list(part="snippet", playlistId=up, maxResults=50).execute()["items"]
        for it in items:
            vid = it["snippet"]["resourceId"]["videoId"]
            t = it["snippet"]["title"][:46]
            if g.apply:
                yt.videos().update(part="status",
                                   body={"id": vid, "status": {"privacyStatus": "private"}}).execute()
                print("✅ PRIVATE:", vid, t)
            else:
                print("… (dry-run) se dat PRIVATE:", vid, t)

    if not g.apply:
        print("\n🔴 DRY-RUN — chua ghi gi. Chay lai voi --apply khi user da gat.")

    print("""
⚠️ API KHONG LAM DUOC, phai vao Studio (Chrome 'Profile 12') bang tay:
   1. Handle @... (doi sang vd @chikei-chimei)
   2. Anh dai dien + anh banner  -> 09_BRAND/
   3. Hinh mo dau / trailer cho nguoi chua dang ky
   4. Playlist theo truc (T1 なぜこの町 / T2 消えた川 / T3 土地の履歴)
   5. Kiem lai: doi tuong kenh = KHONG danh cho tre em""")


if __name__ == "__main__":
    main()
