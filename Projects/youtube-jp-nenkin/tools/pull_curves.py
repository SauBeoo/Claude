r"""pull_curves.py — kéo CURVE RETENTION 0-100% + AVD/AVP + traffic cho mọi video cua kenh.

Ban goc nam o 06_VIDEO/_diagnose/ va DA BI DON khi upload_pack --done move folder video.
=> Dat trong tools/ (bai hoc: tool khong bao gio de trong 06_VIDEO/).

Chay:  python tools/pull_curves.py [--min-view 20] [--days 400]
Ghi:   06_VIDEO/_diag/curves_<today>.txt + .json
"""
import io, sys, json, datetime, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
CRED = ROOT / "credentials" / "token.json"
creds = Credentials.from_authorized_user_file(str(CRED))
if not creds.valid:
    creds.refresh(Request()); CRED.write_text(creds.to_json(), encoding="utf-8")
yt  = build("youtube", "v3", credentials=creds)
ana = build("youtubeAnalytics", "v2", credentials=creds)

ap = argparse.ArgumentParser()
ap.add_argument("--min-view", type=int, default=20)
ap.add_argument("--days", type=int, default=400)
A = ap.parse_args()

TODAY = datetime.date.today()
START = (TODAY - datetime.timedelta(days=A.days)).isoformat()
END   = TODAY.isoformat()
out = []
def p(s=""):
    print(s); out.append(str(s))

def q(**kw):
    try:
        return ana.reports().query(ids="channel==MINE", startDate=START, endDate=END, **kw).execute().get("rows", [])
    except Exception as e:
        p(f"    [loi] {kw.get('metrics')} {kw.get('dimensions','')}: {str(e)[:150]}")
        return []

ch = yt.channels().list(part="snippet,statistics,contentDetails", mine=True).execute()["items"][0]
p("=" * 78)
p(f"KENH {ch['snippet']['title']} | sub={ch['statistics'].get('subscriberCount')} | view={ch['statistics'].get('viewCount')} | do {END}")
p("=" * 78)

up = ch["contentDetails"]["relatedPlaylists"]["uploads"]
vids, tok = [], None
while True:
    r = yt.playlistItems().list(part="contentDetails", playlistId=up, maxResults=50, pageToken=tok).execute()
    vids += [i["contentDetails"]["videoId"] for i in r["items"]]
    tok = r.get("nextPageToken")
    if not tok: break

meta = {}
for i in range(0, len(vids), 50):
    for v in yt.videos().list(part="snippet,contentDetails,statistics", id=",".join(vids[i:i+50])).execute()["items"]:
        d = v["contentDetails"]["duration"]
        import re as _re
        m = _re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d)
        secs = int(m.group(1) or 0)*3600 + int(m.group(2) or 0)*60 + int(m.group(3) or 0)
        meta[v["id"]] = dict(title=v["snippet"]["title"], pub=v["snippet"]["publishedAt"][:10],
                             dur=secs, views=int(v["statistics"].get("viewCount", 0)))

MARKS = [5, 10, 15, 20, 25, 30, 45, 60, 90, 120, 180, 300]
res = {}
rows_basic = q(metrics="views,averageViewDuration,averageViewPercentage", dimensions="video", sort="-views", maxResults=200)
basic = {r[0]: r[1:] for r in rows_basic}

p(f"{'vid':12} {'ngay':11} {'view':>5} {'len':>5} {'AVD':>6} {'AVP':>6} | " +
  " ".join(f"{m:>4}s" for m in MARKS))
p("-" * 78)

for vid in sorted(meta, key=lambda x: meta[x]["pub"]):
    mt = meta[vid]
    b = basic.get(vid)
    an_views = int(b[0]) if b else 0
    if an_views < A.min_view: continue
    avd, avp = (int(b[1]), float(b[2])) if b else (0, 0)
    rows = q(metrics="audienceWatchRatio,relativeRetentionPerformance",
             dimensions="elapsedVideoTimeRatio", filters=f"video=={vid}", sort="elapsedVideoTimeRatio")
    curve = {round(float(r[0]), 3): (float(r[1]), float(r[2]) if r[2] is not None else None) for r in rows}
    def at(sec):
        if not curve or not mt["dur"]: return None
        ratio = sec / mt["dur"]
        k = min(curve, key=lambda x: abs(x - ratio))
        return curve[k]
    vals = []
    for m in MARKS:
        c = at(m)
        vals.append(f"{c[0]:.2f}" if c else "  - ")
    res[vid] = dict(meta=mt, avd=avd, avp=avp, an_views=an_views,
                    marks={m: (at(m)[0] if at(m) else None) for m in MARKS},
                    relperf={m: (at(m)[1] if at(m) else None) for m in MARKS},
                    curve={str(k): v for k, v in curve.items()})
    p(f"{vid:12} {mt['pub']:11} {an_views:5} {mt['dur']:5} {avd//60}:{avd%60:02d}  {avp:5.1f}% | " +
      " ".join(f"{v:>5}" for v in vals))

p()
p("DELTA cac cua so quan trong (diem % tuyet doi)")
p(f"{'vid':12} {'ngay':11} {'10->30s':>9} {'20->30s':>9} {'30->60s':>9} {'60->120s':>9} {'120->180':>9} {'relP@30':>8} {'relP@120':>9}")
for vid, r in sorted(res.items(), key=lambda x: x[1]["meta"]["pub"]):
    m = r["marks"]; rp = r["relperf"]
    def d(a, b):
        return f"{(m[b]-m[a])*100:+.0f}" if m.get(a) is not None and m.get(b) is not None else "   -"
    p(f"{vid:12} {r['meta']['pub']:11} {d(10,30):>9} {d(20,30):>9} {d(30,60):>9} {d(60,120):>9} {d(120,180):>9} "
      f"{(f'{rp[30]:.2f}' if rp.get(30) else '  -'):>8} {(f'{rp[120]:.2f}' if rp.get(120) else '  -'):>9}")

p()
p("TITLE map:")
for vid, r in sorted(res.items(), key=lambda x: x[1]["meta"]["pub"]):
    p(f"  {vid}  {r['meta']['pub']}  {r['meta']['title'][:60]}")

od = ROOT / "06_VIDEO" / "_diag"; od.mkdir(parents=True, exist_ok=True)
(od / f"curves_{END}.txt").write_text("\n".join(out), encoding="utf-8")
(od / f"curves_{END}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
p(f"\n-> {od / f'curves_{END}.txt'}")
