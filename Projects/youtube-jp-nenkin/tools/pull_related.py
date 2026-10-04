r"""pull_related.py — keo DANH SACH VIDEO DAN (RELATED_VIDEO) cua kenh.

Do thuoc "YouTube da hieu chu de chua" theo youtube-suggested-growth.md §1.5:
ti le video dan CUNG NGACH / tong. Ban goc tung nam o 06_VIDEO/_diagnose/ va
DA BI DON khi upload_pack --done move folder video => dat trong tools/.

Chay:  python tools/pull_related.py [--days 90] [--top 30]
Ghi:   06_VIDEO/_diag/related_<today>.txt + .json
"""
import io, sys, json, datetime, argparse
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

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
ap.add_argument("--days", type=int, default=90)
ap.add_argument("--top",  type=int, default=25)  # API tran 25, dat 30 la FIELD_UNKNOWN_VALUE
A = ap.parse_args()

TODAY = datetime.date.today()
START = (TODAY - datetime.timedelta(days=A.days)).isoformat()
END   = TODAY.isoformat()

out = []
def p(s=""):
    print(s); out.append(str(s))

p("=" * 100)
p(f"VIDEO DAN (RELATED_VIDEO) — {TODAY} · cua so {A.days} ngay ({START} -> {END})")
p("=" * 100)

def q(**kw):
    return ana.reports().query(ids="channel==MINE", startDate=START, endDate=END, **kw).execute()

# 1. tong quan traffic source
try:
    r = q(metrics="views,estimatedMinutesWatched,averageViewPercentage",
          dimensions="insightTrafficSourceType", sort="-views")
    p("\n[1] TRAFFIC SOURCE TOAN KENH")
    tot = sum(x[1] for x in r.get("rows", [])) or 1
    for row in r.get("rows", []):
        src, v, mins, avp = row[0], row[1], row[2], row[3]
        p(f"   {src:<22} {v:>6} view ({v*100/tot:>5.1f}%)  ·  {mins:>7.0f} phut  ·  AVP {avp:>5.1f}%")
except Exception as e:
    p(f"   [LOI] traffic source: {e}")

# 2. chi tiet RELATED — videoId dan sang
rows = []
try:
    r = q(metrics="views", dimensions="insightTrafficSourceDetail",
          filters="insightTrafficSourceType==RELATED_VIDEO",
          sort="-views", maxResults=min(A.top, 25))
    rows = r.get("rows", [])
except Exception as e:
    p(f"\n   [LOI] related detail: {e}")

p(f"\n[2] VIDEO DAN SANG KENH MINH — {len(rows)} dong")
data = []
if rows:
    ids = [x[0] for x in rows]
    meta = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        res = yt.videos().list(part="snippet,statistics", id=",".join(chunk)).execute()
        for it in res.get("items", []):
            meta[it["id"]] = it
    p(f"\n   {'view':>5} | {'kenh':<34} | title")
    p("   " + "-" * 96)
    for vid, v in rows:
        it = meta.get(vid)
        if not it:
            p(f"   {v:>5} | {'(khong doc duoc / da an)':<34} | id={vid}")
            data.append({"videoId": vid, "views": v, "channel": None, "title": None})
            continue
        sn = it["snippet"]
        ch, ti = sn["channelTitle"], sn["title"]
        vv = int(it.get("statistics", {}).get("viewCount", 0))
        p(f"   {v:>5} | {ch[:34]:<34} | {ti[:70]}")
        p(f"         {'':<34} | ^ {vv:,} view · {sn['publishedAt'][:10]}")
        data.append({"videoId": vid, "views": v, "channel": ch, "title": ti,
                     "srcViews": vv, "publishedAt": sn["publishedAt"][:10]})

OUT = ROOT / "06_VIDEO" / "_diag"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"related_{TODAY}.txt").write_text("\n".join(out), encoding="utf-8")
(OUT / f"related_{TODAY}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
p(f"\n-> {OUT / f'related_{TODAY}.txt'}")
