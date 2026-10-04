# -*- coding: utf-8 -*-
"""Quet video long-form JP <=30 ngay ngach 人生/老後/朗読/仏教 -> hot.json (xep theo view/ngay)."""
import io, sys, json, re, datetime
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
C = Path(r"E:\Claude\Projects\youtube-jp-nenkin\credentials\token.json")
cr = Credentials.from_authorized_user_file(str(C))
if not cr.valid: cr.refresh(Request()); C.write_text(cr.to_json(), encoding="utf-8")
yt = build("youtube", "v3", credentials=cr)
NOW = datetime.datetime.now(datetime.timezone.utc)
after = (NOW - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
Q = ["60代 人生", "60代 生き方", "老後 物語", "シニア 物語 朗読", "人生 朗読", "ブッダの教え", "仏教の教え 人生",
     "手放す 人生", "老後 後悔", "定年後 人生", "人生後半", "70代 生き方", "孤独 老後", "人生の話 睡眠"]
ids = {}
for q in Q:
    r = yt.search().list(part="id", q=q, type="video", order="viewCount", publishedAfter=after, regionCode="JP",
                         relevanceLanguage="ja", videoDuration="long", maxResults=50).execute()
    r2 = yt.search().list(part="id", q=q, type="video", order="viewCount", publishedAfter=after, regionCode="JP",
                          relevanceLanguage="ja", videoDuration="medium", maxResults=50).execute()
    for it in r["items"] + r2["items"]: ids.setdefault(it["id"]["videoId"], q)
vids = list(ids)
out = []
for i in range(0, len(vids), 50):
    for v in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(vids[i:i+50])).execute()["items"]:
        m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", v["contentDetails"].get("duration",""))
        if not m: continue
        sec = int(m[1] or 0)*3600 + int(m[2] or 0)*60 + int(m[3] or 0)
        if sec < 480 or v["snippet"].get("liveBroadcastContent")!="none": continue
        pub = datetime.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
        age = max((NOW - pub).total_seconds()/86400, 1)
        views = int(v["statistics"].get("viewCount", 0))
        out.append(dict(id=v["id"], ch=v["snippet"]["channelTitle"], chid=v["snippet"]["channelId"], t=v["snippet"]["title"],
                        views=views, age=round(age, 1), vpd=round(views/age), min=round(sec/60, 1), q=ids[v["id"]],
                        lang=v["snippet"].get("defaultAudioLanguage", "")))
chs = list({x["chid"] for x in out}); subs = {}
for i in range(0, len(chs), 50):
    for c in yt.channels().list(part="statistics,snippet", id=",".join(chs[i:i+50])).execute()["items"]:
        subs[c["id"]] = dict(subs=int(c["statistics"].get("subscriberCount", 0)), pub=c["snippet"]["publishedAt"][:10])
for x in out: x.update(subs.get(x["chid"], {}))
out.sort(key=lambda x: -x["vpd"])
json.dump(out, open("hot.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "video long-form <=30 ngay")
for x in out[:60]:
    print(f'{x["vpd"]:7d}/d {x["views"]:8d} {x["age"]:5.1f}d {x["min"]:5.1f}p sub {x.get("subs",0):7d} ch_since {x.get("pub","")} | {x["ch"][:18]} | {x["t"][:60]}')
