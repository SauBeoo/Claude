r"""Khám kênh 年金と老後のお金研究室 — đo 3 thứ quyết định YouTube có phân phối hay không:
  ① kênh CÓ ĐƯỢC CẤP impressions không (và xu hướng qua từng video)
  ② retention 60 GIÂY ĐẦU (audienceWatchRatio + relativeRetentionPerformance)
  ③ traffic đến từ đâu (browse/related/search) — có vào được rail đề xuất chưa

Chạy: python tools\diagnose_channel.py  → in bảng + ghi 06_VIDEO/_diagnose/out.txt
Cùng khuôn với mổ health 2026-07-27 (CHANNEL_DIAGNOSIS_2026-07-27.md) để so được chéo.
"""
import io, sys, json, datetime, collections
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
CRED = ROOT / "credentials" / "token.json"
creds = Credentials.from_authorized_user_file(str(CRED))
if not creds.valid:
    creds.refresh(Request())
    CRED.write_text(creds.to_json(), encoding="utf-8")
yt = build("youtube", "v3", credentials=creds)
ana = build("youtubeAnalytics", "v2", credentials=creds)

TODAY = datetime.date.today().isoformat()
out = []
def p(s=""):
    print(s); out.append(str(s))


def q(**kw):
    try:
        return ana.reports().query(ids="channel==MINE", **kw).execute().get("rows", [])
    except Exception as e:
        p(f"    [analytics lỗi] {kw.get('metrics')}: {str(e)[:160]}")
        return []


# ═══════ 1. KÊNH
ch = yt.channels().list(part="snippet,statistics,contentDetails,brandingSettings,status",
                        mine=True).execute()["items"][0]
st, sn = ch["statistics"], ch["snippet"]
bs = ch.get("brandingSettings", {}).get("channel", {})
p("═" * 74)
p(f"KÊNH: {sn['title']}  ({ch['id']})")
p(f"  sub={int(st.get('subscriberCount',0)):,} · video={st.get('videoCount')} · view tổng={int(st.get('viewCount',0)):,}")
p(f"  lập kênh: {sn['publishedAt'][:10]} · country={sn.get('country')} · defaultLanguage={sn.get('defaultLanguage')}")
kw = bs.get("keywords", "")
p(f"  channel keywords: {len(kw)} ký → {kw[:200]}")
p(f"  channel description: {len(bs.get('description','') or sn.get('description',''))} ký")
p(f"  unsubscribedTrailer: {bs.get('unsubscribedTrailer') or '(chưa đặt)'}")

# ═══════ 2. DANH SÁCH VIDEO
up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
items, tok = [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50,
                                pageToken=tok).execute()
    items += r["items"]; tok = r.get("nextPageToken")
    if not tok:
        break
vids = [i["contentDetails"]["videoId"] for i in items]
vr = yt.videos().list(part="snippet,contentDetails,statistics,status",
                      id=",".join(vids)).execute()["items"]
vr.sort(key=lambda v: v["snippet"]["publishedAt"])

WD = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
p("\n" + "═" * 74)
p("VIDEO ĐÃ ĐĂNG (giờ JST)")
meta = []
for v in vr:
    dt = datetime.datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=9)
    d = v["contentDetails"]["duration"]
    tags = v["snippet"].get("tags", []) or []
    meta.append((v["id"], dt, v["snippet"]["title"]))
    p(f"  {dt:%Y-%m-%d %H:%M} {WD[dt.weekday()]} | {d:>9} | cat {v['snippet']['categoryId']:>2}"
      f" | {int(v['statistics'].get('viewCount',0)):>6,} view"
      f" | {int(v['statistics'].get('likeCount',0)):>3} like"
      f" | tag {len(tags):>2} | {v['status']['privacyStatus']:>7} | {v['snippet']['title'][:44]}")

# ═══════ 3. VIEW THEO NGÀY (tìm vách đá kiểu health)
p("\n" + "═" * 74)
p("VIEW TOÀN KÊNH THEO NGÀY (30 ngày gần nhất) — tìm 'vách đá' phân phối")
start = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
rows = q(startDate=start, endDate=TODAY, metrics="views,estimatedMinutesWatched,subscribersGained",
         dimensions="day", sort="day")
if not rows:
    p("  (không có dữ liệu view — kênh chưa được phát impressions nào đáng kể)")
for d, vw, mn, sg in rows:
    bar = "█" * min(40, int(vw))
    p(f"  {d}  view {vw:>4}  phút {mn:>5}  sub +{sg}  {bar}")

# ═══════ 4. TỪNG VIDEO: impressions / CTR / AVD / retention 60s
p("\n" + "═" * 74)
p("TỪNG VIDEO — impressions · CTR · AVD · RETENTION 60 GIÂY")
p("(mốc quyết định: relPerf@60s ≥0,40 mới được coi là khỏe; health chết ở 0,10–0,14)")
for vid, dt, title in meta:
    pub = dt.date().isoformat()
    days = (datetime.date.today() - dt.date()).days
    p(f"\n── {dt:%m-%d} {WD[dt.weekday()]} · {title[:52]}  (đăng {days} ngày)")
    f = f"video=={vid}"
    r = q(startDate=pub, endDate=TODAY, filters=f,
          metrics="views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,"
                  "subscribersGained,likes")
    if r:
        vw, mw, avd, avp, sg, lk = r[0]
        p(f"   view {vw:.0f} · phút xem {mw:.0f} · AVD {avd:.0f}s · AVP {avp:.1f}% · sub +{sg:.0f} · like {lk:.0f}")
    r = q(startDate=pub, endDate=TODAY, filters=f,
          metrics="impressions,impressionsClickThroughRate")
    if r:
        p(f"   IMPRESSIONS {r[0][0]:,.0f} · CTR {r[0][1]:.2f}%")
    r = q(startDate=pub, endDate=TODAY, filters=f, metrics="views",
          dimensions="insightTrafficSourceType", sort="-views")
    if r:
        p("   traffic: " + " · ".join(f"{k}={v:.0f}" for k, v in r))
    # retention: audienceWatchRatio + relativeRetentionPerformance theo elapsedVideoTimeRatio
    for metric in ("audienceWatchRatio", "relativeRetentionPerformance"):
        r = q(startDate=pub, endDate=TODAY, filters=f, metrics=metric,
              dimensions="elapsedVideoTimeRatio")
        if not r:
            continue
        dur = None
        for v in vr:
            if v["id"] == vid:
                iso = v["contentDetails"]["duration"]
                import re
                m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
                h, mi, s = (int(x) if x else 0 for x in m.groups())
                dur = h * 3600 + mi * 60 + s
        pick = []
        for ratio, val in r:
            sec = ratio * dur if dur else 0
            if 25 <= sec <= 130 or ratio in (0.0,):
                pick.append(f"{sec:.0f}s={val:.2f}")
        p(f"   {metric}: " + " ".join(pick[:14]))

SC = ROOT / "06_VIDEO" / "_diagnose"
SC.mkdir(parents=True, exist_ok=True)
(SC / "out.txt").write_text("\n".join(out), encoding="utf-8")
print("\n=== DONE ===")
