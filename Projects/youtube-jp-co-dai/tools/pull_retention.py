# -*- coding: utf-8 -*-
r"""Pull retention curves (100 points @1%) + day-1 AVD + traffic for co-dai videos.

Why this tool exists (04_FORMULA.md §7, plan 2026-09-06):
  Every real retention number of this channel stops at video 07 (2026-08-12). Videos 18..30
  have ZERO audience numbers - only gate scores. 08_ANALYTICS_LOG.md died 3.5 weeks. Any gate
  tuning since then is guessing. This tool revives the measuring loop.

What it does per video with views >= MIN_VIEW:
  - audienceWatchRatio + relativeRetentionPerformance at 1% resolution (100 points) -> JSON
  - lifetime views / AVD / AVD%
  - day-1 AVD% (chouhen lesson: lifetime AVD is dragged down by trickle traffic)
  - traffic source split (search / browse / suggested / subscriber ...)
  - @15s @30s @45s @60s (vs the 70% benchmark of youtube-suggested-growth.md §4)
  - floor @3' @10' @20'
  - drop map: every 1% step that loses >= DROP_PT points -> the subtitle cue at that second,
    read from 07_UPLOADED/<NN>/_upload/subs.srt (matched by TITLE in METADATA.txt;
    duration is only a UNIQUE fallback - duration alone mismatched 2/5 on 2026-09-06).

Videos with views < MIN_VIEW OR organic views < MIN_VIEW are skipped - a curve on 3 views is
noise, and a curve fed by EXT_URL (links opened by hand) is not the audience (video 24: 52 views,
EXT_URL 21, search 5 -> AVD 4.7% is contaminated).

Usage:
    python tools\pull_retention.py                 # all videos
    python tools\pull_retention.py --min-view 5    # lower the bar (not recommended)

Output:
    06_VIDEO/_diagnose/curves/<NN>_<videoId>.json
    06_VIDEO/_diagnose/RETENTION_<YYYY-MM-DD>.md

Regression check (plan D5): rows for 02 and 07 must match check_coldopen.py docstring within
about 2 points (02: 88.9/61.1/50.0 · 07: 88.2/52.9/41.2 at @15/@30/@45). A big mismatch
means THIS tool is wrong, not that the channel changed.

Token pattern from youtube-jp-nenkin/tools/diagnose_channel.py:18-25.
Query pattern from youtube-jp-chouhen/tools/analytics_report.py:131 (which only PRINTS 5%
steps and saves nothing - here we keep all 100 points).
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from google.oauth2.credentials import Credentials  # noqa: E402
from google.auth.transport.requests import Request  # noqa: E402
from googleapiclient.discovery import build  # noqa: E402
from googleapiclient.errors import HttpError  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CRED = ROOT / "credentials" / "token.json"
OUT = ROOT / "06_VIDEO" / "_diagnose"
CURVES = OUT / "curves"
UPLOADED = ROOT / "07_UPLOADED"
TODAY = dt.date.today().isoformat()

MIN_VIEW = 10       # below this a curve is noise (CHANNEL_OPTIMIZE.md §7.2)
DROP_PT = 0.05      # a 1% step losing >= 5 points is a "drop"
MARK_S = (15, 30, 45, 60)
FLOOR_MIN = (3, 10, 20)
BENCH_60S = 0.70    # youtube-suggested-growth.md §4

sys.path.insert(0, str(ROOT / "tools"))
try:
    from check_coldopen import cues_srt  # reuse the srt reader, same second convention
except Exception:  # pragma: no cover
    cues_srt = None


def creds():
    c = Credentials.from_authorized_user_file(str(CRED))
    if not c.valid:
        c.refresh(Request())
        CRED.write_text(c.to_json(), encoding="utf-8")
    return c


def q(ana, retries=4, **kw):
    """Analytics query with backoff. Google returned 500 backendError mid-run on 2026-09-06."""
    for i in range(retries):
        try:
            return ana.reports().query(ids="channel==MINE", **kw).execute().get("rows") or []
        except HttpError as e:
            code = getattr(e.resp, "status", 0)
            if code in (500, 503, 429) and i < retries - 1:
                time.sleep(2 ** i)
                continue
            print(f"   [analytics] {kw.get('metrics')} -> HTTP {code}: {str(e)[:120]}")
            return []
    return []


def uploads(yt):
    ch = yt.channels().list(part="contentDetails,statistics,snippet", mine=True).execute()["items"][0]
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=50,
                                    pageToken=tok).execute()
        ids += [it["contentDetails"]["videoId"] for it in r.get("items", [])]
        tok = r.get("nextPageToken")
        if not tok:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).execute()
        vids += r.get("items", [])
    return ch, vids


def dur_s(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def at(curve, t, dur):
    """curve: list of (ratio, watch). Linear interpolate watch at second t."""
    if not curve or dur <= 0:
        return None
    r = t / dur
    if r >= 1:
        return curve[-1][1]
    prev = curve[0]
    for cur in curve:
        if cur[0] >= r:
            if cur[0] == prev[0]:
                return cur[1]
            f = (r - prev[0]) / (cur[0] - prev[0])
            return prev[1] + f * (cur[1] - prev[1])
        prev = cur
    return curve[-1][1]


ORGANIC = ("YT_SEARCH", "BROWSE", "RELATED_VIDEO", "YT_CHANNEL", "SUBSCRIBER",
           "NOTIFICATION", "PLAYLIST", "SHORTS", "END_SCREEN", "HASHTAGS")
# EXT_URL / NO_LINK_OTHER / NO_LINK_EMBEDDED = links opened by hand, tests, shares -> not the
# audience we are measuring. 2026-09-06: video 24 had 52 views but EXT_URL=21, search=5 ->
# its 4.7% AVD is contaminated and must NOT be read as a verdict on the 45s spec.


def _meta_title(p):
    """Title line right after the `[2] TITLE` header in _upload/METADATA.txt."""
    try:
        lines = p.read_text(encoding="utf-8", errors="ignore").split("\n")
    except Exception:
        return None
    for i, l in enumerate(lines):
        if "TITLE" in l and l.strip().startswith("["):
            for k in lines[i + 1:i + 4]:
                k = k.strip()
                if k and not set(k) <= set("-=─━_ "):
                    return k
    return None


def find_upload(title, dur):
    """Match 07_UPLOADED/<NN> by TITLE first, duration only as a UNIQUE fallback (+-3s).

    Duration alone mismatched 2/5 videos on 2026-09-06: 01 (22'47) grabbed 08's srt (22'49),
    24 (18'33) grabbed 28's (18'48) -> drop cues pointed at the wrong script.
    Returns (folder_name, cues, how) with how in {"title", "dur", "none"}.
    """
    for meta in UPLOADED.glob("*/_upload/METADATA.txt"):
        t = _meta_title(meta)
        if t and (t == title or t[:18] == title[:18]):
            folder = meta.parent.parent
            srt = folder / "_upload" / "subs.srt"
            cs = []
            if cues_srt and srt.exists():
                try:
                    cs = cues_srt(srt)
                except Exception:
                    cs = []
            return folder.name, cs, "title"
    cands = []
    if cues_srt:
        for p in UPLOADED.glob("*/_upload/subs.srt"):
            try:
                cs = cues_srt(p)
            except Exception:
                continue
            # +-8s: srt ends before the outro, so 02 (25'18) missed at +-3 on 2026-09-06.
            # UNIQUE is what protects us, not a tight tolerance (01/08 are 2s apart -> 2 cands -> none).
            if cs and abs(cs[-1][0] - dur) <= 8:
                cands.append((p.parent.parent.name, cs))
    if len(cands) == 1:
        return cands[0][0], cands[0][1], "dur"
    return None, [], "none"


def nn_of(title, folder):
    if folder:
        m = re.match(r"(\d+)", folder)
        if m:
            return m.group(1)
    return "??"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-view", type=int, default=MIN_VIEW)
    a = ap.parse_args()

    CURVES.mkdir(parents=True, exist_ok=True)
    c = creds()
    yt = build("youtube", "v3", credentials=c)
    ana = build("youtubeAnalytics", "v2", credentials=c)

    ch, vids = uploads(yt)
    st = ch["statistics"]
    print(f"▶ {ch['snippet']['title']} · sub {st.get('subscriberCount')} · view {st.get('viewCount')} · {len(vids)} video")

    rows, skipped = [], []
    for v in sorted(vids, key=lambda x: x["snippet"]["publishedAt"]):
        vid = v["id"]
        title = v["snippet"]["title"]
        pub = v["snippet"]["publishedAt"][:10]
        dur = dur_s(v["contentDetails"]["duration"])
        views = int(v.get("statistics", {}).get("viewCount", 0))
        folder, cs, how = find_upload(title, dur)
        nn = nn_of(title, folder)
        if views < a.min_view:
            skipped.append((nn, title[:34], views, pub, "—"))
            continue

        # traffic FIRST: organic views decide whether the curve is worth reading
        traf = q(ana, startDate=pub, endDate=TODAY, filters=f"video=={vid}",
                 metrics="views,estimatedMinutesWatched", dimensions="insightTrafficSourceType",
                 sort="-views")
        organic = sum(int(r[1]) for r in traf if r[0] in ORGANIC)
        ext = sum(int(r[1]) for r in traf if r[0] not in ORGANIC)
        print(f"\n── {nn} {title[:50]} · {pub} · {dur//60}'{dur%60:02d} · {views} view "
              f"(organic {organic} / ext {ext}) · srt:{how}")
        if organic < a.min_view:
            print(f"   ⚠️ organic {organic} < {a.min_view} → curve KHÔNG đọc được (EXT_URL/NO_LINK áp đảo)")
            skipped.append((nn, title[:34], views, pub, f"organic {organic}"))
            continue
        life = q(ana, startDate=pub, endDate=TODAY, filters=f"video=={vid}",
                 metrics="views,averageViewDuration,averageViewPercentage")
        curve = q(ana, startDate=pub, endDate=TODAY, filters=f"video=={vid}",
                  metrics="audienceWatchRatio,relativeRetentionPerformance",
                  dimensions="elapsedVideoTimeRatio")
        day = q(ana, startDate=pub, endDate=TODAY, filters=f"video=={vid}",
                metrics="views,averageViewDuration,averageViewPercentage",
                dimensions="day", sort="day")

        cur = [(float(r[0]), float(r[1])) for r in curve]
        rel = [(float(r[0]), float(r[2])) for r in curve] if curve and len(curve[0]) > 2 else []
        marks = {t: at(cur, t, dur) for t in MARK_S}
        floors = {m: at(cur, m * 60, dur) for m in FLOOR_MIN}
        avd = life[0][1] if life else None
        avdp = life[0][2] if life else None
        day1 = day[0] if day else None

        drops = []
        for i in range(1, len(cur)):
            d = cur[i - 1][1] - cur[i][1]
            if d >= DROP_PT:
                t = cur[i][0] * dur
                cue = ""
                if cs:
                    near = [x for x in cs if abs(x[0] - t) <= dur * 0.01 + 1]
                    cue = " / ".join(x[1][:28] for x in near[:3])
                drops.append({"t": round(t, 1), "drop": round(d * 100, 1), "cue": cue})

        rec = {
            "nn": nn, "videoId": vid, "title": title, "published": pub, "dur_s": dur,
            "views": views, "organic": organic, "ext": ext, "srt_match": how,
            "avd_s": avd, "avd_pct": avdp,
            "day1": {"views": day1[1], "avd_s": day1[2], "avd_pct": day1[3]} if day1 else None,
            "marks": {f"@{t}s": (None if marks[t] is None else round(marks[t] * 100, 1)) for t in MARK_S},
            "floor": {f"@{m}m": (None if floors[m] is None else round(floors[m] * 100, 1)) for m in FLOOR_MIN},
            "traffic": [{"src": r[0], "views": r[1], "min": r[2]} for r in traf],
            "srt_folder": folder, "drops": drops,
            "curve": [{"r": r, "watch": w} for r, w in cur],
            "relperf": [{"r": r, "rel": x} for r, x in rel],
            "pulled": TODAY,
        }
        safe_nn = nn if nn.isdigit() else "xx"   # "??" is not a valid Windows filename
        (CURVES / f"{safe_nn}_{vid}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        rows.append(rec)

        m15, m30, m45, m60 = (rec["marks"][f"@{t}s"] for t in MARK_S)
        f3, f10, f20 = (rec["floor"][f"@{m}m"] for m in FLOOR_MIN)
        fmt = lambda x: "—" if x is None else f"{x:.1f}"
        print(f"   AVD {fmt(avdp)}% · day1 {fmt(day1[3] if day1 else None)}% · "
              f"@15 {fmt(m15)} @30 {fmt(m30)} @45 {fmt(m45)} @60 {fmt(m60)} (bench 70) · "
              f"floor 3' {fmt(f3)} 10' {fmt(f10)} 20' {fmt(f20)} · {len(cur)} pts · drops {len(drops)}")
        for d in drops[:6]:
            print(f"      ↓ {int(d['t'])//60:02d}:{int(d['t'])%60:02d}  −{d['drop']}đ  {d['cue']}")

    # ── markdown report
    md = [f"# RETENTION co-dai — kéo {TODAY} (`tools/pull_retention.py`)", "",
          f"Kênh: sub {st.get('subscriberCount')} · view {st.get('viewCount')} · {len(vids)} video · "
          f"ngưỡng ≥{a.min_view} view · mốc @60s so chuẩn **{int(BENCH_60S*100)}%** (suggested-growth §4)", ""]
    if rows:
        md += ["| # | video | đăng | dài | view (organic/ext) | AVD% | AVD ngày1 | @15s | @30s | @45s | @60s | 3′ | 10′ | 20′ | search/browse/related | drops≥5đ |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            tr = {t["src"]: t["views"] for t in r["traffic"]}
            src = f"{tr.get('YT_SEARCH',0)}/{tr.get('BROWSE',0)}/{tr.get('RELATED_VIDEO',0)}"
            g = lambda k, d: "—" if d.get(k) is None else f"{d[k]:.0f}"
            avdp = "—" if r["avd_pct"] is None else f"{r['avd_pct']:.1f}"
            d1 = "—" if not r["day1"] else f"{r['day1']['avd_pct']:.1f}"
            md.append(f"| {r['nn']} | {r['title'][:26]} | {r['published']} | {r['dur_s']//60}′ | "
                      f"{r['views']} ({r['organic']}/{r['ext']}) | {avdp} | {d1} | "
                      f"{g('@15s', r['marks'])} | {g('@30s', r['marks'])} | {g('@45s', r['marks'])} | {g('@60s', r['marks'])} | "
                      f"{g('@3m', r['floor'])} | {g('@10m', r['floor'])} | {g('@20m', r['floor'])} | {src} | {len(r['drops'])} |")
        md += ["", "## Chỗ rớt ≥5 điểm trong một bước 1% (độ phân giải 1% ≈ 12–15s ⇒ cụm 2–3 câu)", ""]
        for r in rows:
            if r["drops"]:
                md.append(f"**{r['nn']} {r['title'][:30]}**")
                for d in r["drops"][:8]:
                    md.append(f"- {int(d['t'])//60:02d}:{int(d['t'])%60:02d} −{d['drop']}đ 「{d['cue']}」")
                md.append("")
    else:
        md += ["**Không video nào đạt ngưỡng.**", ""]
    if skipped:
        md += [f"## Bỏ qua (view < {a.min_view} HOẶC organic < {a.min_view} — curve là nhiễu)", "",
               "| # | video | view | đăng | lý do |", "|---|---|---|---|---|"]
        md += [f"| {nn} | {t} | {v} | {p} | {why} |" for nn, t, v, p, why in skipped]
    md += ["", "## Đọc thế nào", "",
           "- **Điều kiện dừng (plan D):** 3 lần kéo tuần liên tiếp mà không video 18→30 nào đạt ngưỡng → ghi "
           "\"kênh mù\" vào `08_ANALYTICS_LOG.md` §6, DỪNG tinh chỉnh gate WARN (O18/O19/⑥), thước đo chuyển "
           "hẳn sang `04_FORMULA.md` §7 (v1 có được nhận không cần v2).",
           "- **Hồi quy tool (plan D5):** 02 phải ≈ 88,9/61,1/50,0 · 07 ≈ 88,2/52,9/41,2 (@15/30/45, ±2đ). "
           "Lệch lớn = tool sai, không phải kênh đổi.",
           "- **Ngưỡng là ORGANIC ≥10, không phải view ≥10.** 2026-09-06: video 24 có 52 view nhưng "
           "EXT_URL=21 / search=5 — 4,7% AVD của nó là số bẩn, không phải phán quyết về spec 45s.",
           "- Ghép srt theo TITLE (`_upload/METADATA.txt`), thời lượng chỉ là fallback duy nhất ±3s "
           "(ghép theo thời lượng đã nhầm 01↔08, 24↔28).",
           "- Curve đầy đủ 100 điểm: `06_VIDEO/_diagnose/curves/<NN>_<videoId>.json`."]
    rep = OUT / f"RETENTION_{TODAY}.md"
    rep.write_text("\n".join(md), encoding="utf-8")
    print(f"\n✅ {len(rows)} video có curve · {len(skipped)} bỏ qua (<{a.min_view} view) → {rep}")
    if not any(r["nn"].isdigit() and int(r["nn"]) >= 18 for r in rows):
        print("⚠️ KHÔNG video nào 18→30 đạt ngưỡng — đây là lần kéo #1 của điều kiện dừng 3 tuần.")


if __name__ == "__main__":
    main()
