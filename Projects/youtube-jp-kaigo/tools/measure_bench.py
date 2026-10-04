# -*- coding: utf-8 -*-
"""Đo benchmark ngách 介護×お金: publishedAt (giờ JST) + categoryId + tags + duration.
Dùng token readonly sẵn có của nenkin. Ghi kết quả ra file utf-8.
"""
import io, json, sys, datetime, collections
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CRED = Path(r"E:\Claude\Projects\youtube-jp-nenkin\credentials")
creds = Credentials.from_authorized_user_file(str(CRED / "token.json"))
if not creds.valid:
    creds.refresh(Request())
    (CRED / "token.json").write_text(creds.to_json(), encoding="utf-8")
yt = build("youtube", "v3", credentials=creds)

TARGETS = {
    "ケアまど (介護とお金)": "UClVcmctoyJ_wXZ1xlrlBMlQ",
    "脱・税理士スガワラくん": "UCwKupwJ1EpdNH8Z98SKjY2Q",
    "みんなの給付金・補助金": "UCt8oGxc3GJUqFvBTygzTr4A",
    "節約看護師りょう": "UCx2HEX7jkwrRsKXNgmIUMeA",
}
# 親ケア.com + ゆるっとかいご: chỉ có handle → tìm bằng search
SEARCH = ["親ケア.com", "ゆるっとかいご", "介護 お金 チャンネル"]

out = []
def p(s=""):
    print(s); out.append(str(s))

# 1) tìm channel id còn thiếu
for q in SEARCH:
    try:
        r = yt.search().list(part="snippet", q=q, type="channel", maxResults=3, regionCode="JP", relevanceLanguage="ja").execute()
        for it in r.get("items", []):
            p(f"[search:{q}] {it['snippet']['title']} -> {it['snippet']['channelId']}")
    except Exception as e:
        p(f"[search:{q}] LỖI {e!r}")
p()

def analyze(name, cid, n=20):
    p(f"════ {name} ({cid})")
    try:
        ch = yt.channels().list(part="snippet,statistics,contentDetails,brandingSettings,topicDetails", id=cid).execute()
        if not ch.get("items"):
            p("  (không tìm thấy)"); p(); return
        c = ch["items"][0]
        st = c["statistics"]
        p(f"  sub={int(st.get('subscriberCount',0)):,} · video={st.get('videoCount')} · view={int(st.get('viewCount',0)):,}")
        p(f"  country={c['snippet'].get('country')} · defaultLanguage={c['snippet'].get('defaultLanguage')} · published={c['snippet']['publishedAt']}")
        bs = c.get("brandingSettings", {}).get("channel", {})
        kw = bs.get("keywords", "")
        p(f"  channel keywords ({len(kw)} ký): {kw[:600]}")
        desc = c["snippet"].get("description", "").replace("\n", " / ")
        p(f"  channel desc ({len(desc)} ký): {desc[:400]}")
        up = c["contentDetails"]["relatedPlaylists"]["uploads"]
        items, tok = [], None
        while len(items) < n:
            r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=min(50, n - len(items)), pageToken=tok).execute()
            items += r["items"]; tok = r.get("nextPageToken")
            if not tok: break
        vids = [i["contentDetails"]["videoId"] for i in items][:n]
        vr = yt.videos().list(part="snippet,contentDetails,statistics", id=",".join(vids)).execute()
        hours, wdays, cats, alltags, durs = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(), []
        p(f"  --- {len(vr['items'])} video gần nhất (giờ JST) ---")
        for v in vr["items"]:
            dt = datetime.datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9)
            hours[dt.hour] += 1; wdays[dt.weekday()] += 1
            cats[v["snippet"]["categoryId"]] += 1
            for t in v["snippet"].get("tags", []) or []:
                alltags[t] += 1
            dur = v["contentDetails"]["duration"]
            durs.append(dur)
            p(f"   {dt:%Y-%m-%d %H:%M} JST | {dur:>10} | cat {v['snippet']['categoryId']:>2} | {int(v['statistics'].get('viewCount',0)):>9,} view | #tag {len(v['snippet'].get('tags',[]) or [])} | {v['snippet']['title'][:60]}")
        wd = ["T2","T3","T4","T5","T6","T7","CN"]
        p(f"  GIỜ: {sorted(hours.items(), key=lambda x:-x[1])}")
        p(f"  NGÀY: {[(wd[k],c) for k,c in sorted(wdays.items(), key=lambda x:-x[1])]}")
        p(f"  categoryId: {cats.most_common()}")
        p(f"  TOP tag ({len(alltags)} tag khác nhau): {alltags.most_common(25)}")
    except Exception as e:
        p(f"  LỖI {e!r}")
    p()

for name, cid in TARGETS.items():
    analyze(name, cid)

Path(r"C:\Users\tuana\AppData\Local\Temp\claude\E--Claude\b81504a7-93e7-4e31-ac02-8302af10cb73\scratchpad\bench_kaigo_out.txt").write_text("\n".join(out), encoding="utf-8")
print("=== DONE ===")
