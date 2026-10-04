# -*- coding: utf-8 -*-
"""Thi hành mục 4 + 6 của CHANNEL_DIAGNOSIS_2026-08-29.md (user gật 2026-08-30 "làm từ 1 đến 6"):
  6a  v09 (n1eDEoHbEMM) + v11 (KJicjlLpuP4): categoryId 22 -> 27
  6b  v01/v02/v04: thêm dòng credit 「音声: VOICEVOX:雀松朱司」 trước khối hashtag (license VOICEVOX)
  6c  channel description: 「毎週 月・水・金 の19時」 -> 「毎週 火・木・日 の19時」 (lịch thật T3·T5·CN)
  4   tạo 3 playlist theo 3 trụ + nạp video (playlist cũ 16 video giữ nguyên)
Chạy: python tools/apply_channel_fix_20260830.py          (dry-run, chỉ in)
      python tools/apply_channel_fix_20260830.py --apply  (ghi thật)
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

APPLY = "--apply" in sys.argv
ROOT = Path(__file__).resolve().parents[1]
creds = Credentials.from_authorized_user_file(str(ROOT / "credentials" / "token.json"))
yt = build("youtube", "v3", credentials=creds)
CREDIT = "音声: VOICEVOX:雀松朱司"


def upd_video(vid, cat=None, desc_fn=None):
    sn = yt.videos().list(part="snippet", id=vid).execute()["items"][0]["snippet"]
    body = {"id": vid, "snippet": {k: sn[k] for k in
            ("title", "description", "categoryId", "tags", "defaultLanguage", "defaultAudioLanguage") if k in sn}}
    if cat:
        body["snippet"]["categoryId"] = cat
    if desc_fn:
        body["snippet"]["description"] = desc_fn(sn["description"])
    changed = body["snippet"]["categoryId"] != sn["categoryId"] or body["snippet"]["description"] != sn["description"]
    print(f"{'APPLY' if APPLY else 'DRY  '} video {vid} {sn['title'][:28]} cat {sn['categoryId']}->{body['snippet']['categoryId']} "
          f"desc {'+credit' if body['snippet']['description'] != sn['description'] else 'same'}")
    if APPLY and changed:
        yt.videos().update(part="snippet", body=body).execute()


def add_credit(d):
    if "VOICEVOX" in d:
        return d
    i = d.rfind("\n#")
    return (d[:i].rstrip() + "\n\n" + CREDIT + "\n" + d[i:]) if i > 0 else d + "\n\n" + CREDIT


# 6a
for vid in ["n1eDEoHbEMM", "KJicjlLpuP4"]:
    upd_video(vid, cat="27")
# 6b
for vid in ["bWl2jE9l8z4", "uPlyzkGYfCs", "MfEKhbXdTXY"]:
    upd_video(vid, desc_fn=add_credit)
# 6c
ch = yt.channels().list(part="brandingSettings", mine=True).execute()["items"][0]
bs = ch["brandingSettings"]
d = bs["channel"]["description"]
if "毎週 月・水・金 の19時" in d:
    bs["channel"]["description"] = d.replace("毎週 月・水・金 の19時", "毎週 火・木・日 の19時")
    print(f"{'APPLY' if APPLY else 'DRY  '} channel desc: 月・水・金 -> 火・木・日")
    if APPLY:
        yt.channels().update(part="brandingSettings", body={"id": ch["id"], "brandingSettings": bs}).execute()
else:
    print("channel desc: đã đúng, bỏ qua")

# 4 — playlists theo trụ
PL = [
    ("年金はいくら？受け取り方で変わる金額｜年金と老後のお金研究室",
     "60歳・65歳・70歳、いつから受け取ると年金はいくらになるのか。在職老齢年金・繰り下げ・繰り上げ・加給年金・遺族年金を、モニターの見込み額で計算した研究記録です。",
     ["bWl2jE9l8z4", "uPlyzkGYfCs", "xWyfoi59uSs", "TTwuFmKa3T8", "zoTNI9KWgCg", "pn9Fi9Bx6_U"]),
    ("届く紙と期限｜給付金・公金受取口座・詐欺｜年金と老後のお金研究室",
     "日本年金機構や市役所から届く封筒・ハガキ・簡易書留。何の紙で、いつまでに何をすればいいのか。年金生活者支援給付金・公金受取口座・扶養親族等申告書・詐欺の見分け方をまとめた研究記録です。",
     ["MfEKhbXdTXY", "n1eDEoHbEMM", "cOpzaW2FYXc", "zr9uJbDFaoU", "KmmbwuRHBAg", "UzHj5gsqSVY"]),
    ("年金の手取り｜税金・介護保険料・住民税非課税｜年金と老後のお金研究室",
     "年金額は変わらないのに振込額が減るのはなぜか。介護保険料・所得税・住民税非課税の境目・退職金の申告書など、年金の手取りを左右する制度の研究記録です。",
     ["H9WisP5rcgI", "KJicjlLpuP4", "S0j16selKvs", "ZbEwsPFCcAA"]),
]
existing = {p["snippet"]["title"] for p in yt.playlists().list(part="snippet", mine=True, maxResults=50).execute().get("items", [])}
for title, desc, vids in PL:
    if title in existing:
        print("playlist đã có, bỏ qua:", title[:24]); continue
    print(f"{'APPLY' if APPLY else 'DRY  '} playlist {title[:24]}… ({len(vids)} video)")
    if APPLY:
        pl = yt.playlists().insert(part="snippet,status", body={
            "snippet": {"title": title, "description": desc + "\n\n#年金 #老後のお金 #年金と老後のお金研究室", "defaultLanguage": "ja"},
            "status": {"privacyStatus": "public"}}).execute()
        for v in vids:
            yt.playlistItems().insert(part="snippet", body={"snippet": {
                "playlistId": pl["id"], "resourceId": {"kind": "youtube#video", "videoId": v}}}).execute()
        print("   →", pl["id"])
print("DONE", "(APPLY)" if APPLY else "(dry-run — thêm --apply để ghi)")
