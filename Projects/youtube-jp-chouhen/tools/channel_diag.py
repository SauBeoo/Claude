# -*- coding: utf-8 -*-
"""
channel_diag.py — mổ kênh bằng Analytics API: traffic source · nguồn RELATED · bộ peer cùng rail.

Sinh ra từ `CHANNEL_DIAGNOSIS_2026-08-12.md` (trước đó phải gõ inline mỗi lần — việc còn mở
đã ghi trong diagnosis 2026-08-01 §7).

⚠️ `impressions` / `impressionsClickThroughRate` đã bị Google RÚT từ 2026-07-30 → tool này
KHÔNG in CTR. Muốn CTR thì đọc tay trong YouTube Studio, đúng Chrome profile của kênh
(`.claude/rules/channel-browser.md`).

Dùng:
  python tools/channel_diag.py --traffic                  # mọi video: view/AVD/traffic source
  python tools/channel_diag.py --traffic --channel health
  python tools/channel_diag.py --related <videoId|all>    # RELATED đến TỪ video/kênh nào
  python tools/channel_diag.py --peers                    # bộ kênh peer: nhịp/độ dài/format title
  python tools/channel_diag.py --peers --peer-name 語り茶屋 --peer-name 毎日スカッと

`--peers` không truyền `--peer-name` thì tự suy bộ peer từ chính nguồn RELATED của kênh
(= bộ kênh YouTube THẬT SỰ ghép mình vào, không phải bộ tìm bằng search — đây là chỗ
`CTR_PLAN_2026-07-28.md` đã đo nhầm).
"""
import argparse
import collections
import datetime as dt
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).parent))

from googleapiclient.discovery import build

from upload_api import get_creds
from upload_pack import CHANNELS, PROJECTS_ROOT

START = "2026-01-01"


def _svc(key: str):
    proj = PROJECTS_ROOT / CHANNELS[key]["project"]
    creds = get_creds(proj)
    return (build("youtube", "v3", credentials=creds),
            build("youtubeAnalytics", "v2", credentials=creds))


def _mine(yt) -> dict:
    return yt.channels().list(part="snippet,contentDetails,statistics", mine=True).execute()["items"][0]


def _uploads(yt, ch: dict, limit: int = 60) -> list:
    """Video của kênh, mới → cũ. Quét uploads playlist nên thấy cả private/unlisted."""
    pl = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while len(ids) < limit:
        r = yt.playlistItems().list(part="contentDetails", playlistId=pl,
                                    maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    out = []
    for i in range(0, len(ids[:limit]), 50):
        out += yt.videos().list(part="snippet,contentDetails,statistics",
                                id=",".join(ids[i:i + 50])).execute()["items"]
    out.sort(key=lambda v: v["snippet"]["publishedAt"], reverse=True)
    return out


def _minutes(iso: str) -> float:
    # Video đang live / sắp phát trả "P0D" (không có phần PT…) → regex không khớp.
    # Trả 0 để nhánh lọc Shorts tự loại chúng, thay vì nổ AttributeError giữa lượt gom.
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0.0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 60 + mi + s / 60


def _today() -> str:
    return dt.date.today().isoformat()


# ─────────────────────────────────────────────────────── traffic
def cmd_traffic(key: str) -> None:
    yt, an = _svc(key)
    ch = _mine(yt)
    ids = f"channel=={ch['id']}"
    vids = [v for v in _uploads(yt, ch) if _minutes(v["contentDetails"]["duration"]) >= 8]
    print(f"▶ {ch['snippet']['title']} [{key}] — sub {int(ch['statistics']['subscriberCount']):,} · "
          f"{int(ch['statistics']['viewCount']):,} view · {ch['statistics']['videoCount']} video")
    print(f"\n{'ngày':11} {'dài':>7} {'view':>5} {'AVD%':>6} {'phút':>7}  nguồn traffic")
    tot_related = 0
    for v in vids:
        vid = v["id"]
        base = an.reports().query(ids=ids, startDate=START, endDate=_today(),
                                  metrics="views,averageViewPercentage,estimatedMinutesWatched",
                                  filters=f"video=={vid}").execute().get("rows", [[0, 0, 0]])[0]
        src = an.reports().query(ids=ids, startDate=START, endDate=_today(), metrics="views",
                                 dimensions="insightTrafficSourceType",
                                 filters=f"video=={vid}", sort="-views").execute().get("rows", [])
        ts = " ".join(f"{a}:{b}" for a, b in src if b)
        rel = dict(src).get("RELATED_VIDEO", 0)
        tot_related += rel
        print(f"{v['snippet']['publishedAt'][:10]} {_minutes(v['contentDetails']['duration']):6.1f}' "
              f"{base[0]:5} {base[1]:6.1f} {base[2]:7.0f}  {ts}")
    print(f"\n{len(vids)} video long-form · tổng view RELATED = {tot_related}")
    print("📌 BROWSE_FEATURES vắng mặt ở mọi dòng trên = kênh CHƯA TỪNG được đưa vào trang chủ/feed.")


# ─────────────────────────────────────────────────────── related
def _related_rows(an, chid: str, vid: str) -> list:
    """maxResults của dimension `insightTrafficSourceDetail` trần ở 25 — vượt là HTTP 500."""
    return an.reports().query(
        ids=f"channel=={chid}", startDate=START, endDate=_today(), metrics="views",
        dimensions="insightTrafficSourceDetail",
        filters=f"video=={vid};insightTrafficSourceType==RELATED_VIDEO",
        sort="-views", maxResults=25).execute().get("rows", [])


def cmd_related(key: str, target: str) -> None:
    yt, an = _svc(key)
    ch = _mine(yt)
    vids = ([v["id"] for v in _uploads(yt, ch)
             if _minutes(v["contentDetails"]["duration"]) >= 8] if target == "all" else [target])
    for vid in vids:
        rows = _related_rows(an, ch["id"], vid)
        if not rows:
            continue
        meta = {}
        srcids = [a for a, _ in rows]
        for i in range(0, len(srcids), 50):
            for it in yt.videos().list(part="snippet", id=",".join(srcids[i:i + 50])).execute()["items"]:
                meta[it["id"]] = (it["snippet"]["channelId"], it["snippet"]["channelTitle"],
                                  it["snippet"]["title"])
        tot = sum(b for _, b in rows)
        own = sum(b for a, b in rows if meta.get(a, ("",))[0] == ch["id"])
        print(f"\n=== {vid} — top-25 nguồn RELATED = {tot} view (TỰ KÊNH: {own}) ===")
        for a, b in rows:
            _, cname, ctitle = meta.get(a, ("?", "(đã xoá/riêng tư)", ""))
            print(f"  {b:4}  {cname[:26]:26} | {ctitle[:44]}")
        print(f"  ⓘ top-25 chỉ gom được {tot} view → phần còn lại trải trên hàng trăm nguồn lẻ "
              f"= bị RẮC RỘNG chứ không phải vào rail tập trung.")


# ─────────────────────────────────────────────────────── peers
def _peer_names_from_related(yt, an, ch: dict, top: int = 8) -> list:
    """Suy bộ peer từ chính nguồn RELATED — bộ kênh YouTube thật sự ghép mình vào."""
    vids = [v["id"] for v in _uploads(yt, ch, limit=30)
            if _minutes(v["contentDetails"]["duration"]) >= 8]
    srcs = collections.Counter()
    for vid in vids:
        for a, b in _related_rows(an, ch["id"], vid):
            srcs[a] += b
    bych = collections.Counter()
    ids = list(srcs)
    for i in range(0, len(ids), 50):
        for it in yt.videos().list(part="snippet", id=",".join(ids[i:i + 50])).execute()["items"]:
            bych[it["snippet"]["channelTitle"]] += srcs[it["id"]]
    return [n for n, _ in bych.most_common(top)]


def cmd_peers(key: str, names: list) -> None:
    yt, an = _svc(key)
    ch = _mine(yt)
    if not names:
        names = _peer_names_from_related(yt, an, ch)
        print("Bộ peer suy từ nguồn RELATED của chính kênh:", " · ".join(names), "\n")
    for nm in names:
        r = yt.search().list(part="snippet", q=nm, type="channel", maxResults=3).execute()
        cid = next((i["snippet"]["channelId"] for i in r["items"]
                    if i["snippet"]["title"].strip() == nm.strip()), None)
        if not cid:
            print(f"?? không khớp chính xác tên kênh: {nm}")
            continue
        c = yt.channels().list(part="contentDetails,statistics", id=cid).execute()["items"][0]
        items = yt.playlistItems().list(
            part="contentDetails", maxResults=25,
            playlistId=c["contentDetails"]["relatedPlaylists"]["uploads"]).execute()["items"]
        vv = yt.videos().list(part="snippet,statistics,contentDetails",
                              id=",".join(i["contentDetails"]["videoId"] for i in items)).execute()["items"]
        vv = [v for v in vv if _minutes(v["contentDetails"]["duration"]) >= 8]
        if not vv:
            continue
        ds = sorted(v["snippet"]["publishedAt"][:10] for v in vv)
        span = (dt.date.fromisoformat(ds[-1]) - dt.date.fromisoformat(ds[0])).days or 1
        mins = sorted(_minutes(v["contentDetails"]["duration"]) for v in vv)
        tagfront = sum(1 for v in vv if v["snippet"]["title"].lstrip().startswith("【"))
        ntag = len(vv[0]["snippet"].get("tags") or [])
        print(f"▶ {nm} | sub {int(c['statistics']['subscriberCount']):,} | "
              f"{c['statistics']['videoCount']} video | nhịp {len(ds) / span * 7:.1f}/tuần | "
              f"dài {mins[0]:.0f}–{mins[-1]:.0f}′ | title mở 【】 {tagfront}/{len(vv)} | tag {ntag}")
        for v in sorted(vv, key=lambda x: int(x["statistics"].get("viewCount", 0)), reverse=True)[:3]:
            print(f"    {int(v['statistics'].get('viewCount', 0)):>8,}v "
                  f"{_minutes(v['contentDetails']['duration']):5.0f}'  {v['snippet']['title'][:56]}")
        print()


# ─────────────────────────────────────────────────────── premises
def cmd_premises(key: str, names: list, days: int, per: int) -> None:
    """Gom PREMISE proven-viral từ bộ peer → nguyên liệu cho chế độ A·REMAKE.

    Ở ngách 朗読スカッと thì TITLE *chính là* premise: nó kể trọn setup + cú lật. Nên
    bảng title xếp theo view/NGÀY là bảng premise, không cần transcript.
    ⚠️ Luật benchmark 30 ngày (`feedback_benchmark_30_ngay`): chỉ lấy video ≤`days` ngày,
    lọc Shorts (<8′), xếp theo view/ngày — KHÔNG xếp theo view tuyệt đối (hit 3 năm trước
    làm hỏng kết luận packaging).
    """
    yt, an = _svc(key)
    ch = _mine(yt)
    if not names:
        names = _peer_names_from_related(yt, an, ch)
        print("Bộ peer suy từ nguồn RELATED của chính kênh:", " · ".join(names), "\n")
    today = dt.date.today()
    rows = []
    for nm in names:
        r = yt.search().list(part="snippet", q=nm, type="channel", maxResults=3).execute()
        cid = next((i["snippet"]["channelId"] for i in r["items"]
                    if i["snippet"]["title"].strip() == nm.strip()), None)
        if not cid:
            print(f"?? không khớp chính xác tên kênh: {nm}")
            continue
        c = yt.channels().list(part="contentDetails", id=cid).execute()["items"][0]
        pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
        ids, tok = [], None
        while len(ids) < 100:
            r = yt.playlistItems().list(part="contentDetails", playlistId=pl,
                                        maxResults=50, pageToken=tok).execute()
            ids += [i["contentDetails"]["videoId"] for i in r["items"]]
            tok = r.get("nextPageToken")
            if not tok:
                break
        vv = []
        for i in range(0, len(ids), 50):
            vv += yt.videos().list(part="snippet,statistics,contentDetails",
                                   id=",".join(ids[i:i + 50])).execute()["items"]
        for v in vv:
            mins = _minutes(v["contentDetails"]["duration"])
            if mins < 8:                                   # lọc Shorts
                continue
            pub = dt.date.fromisoformat(v["snippet"]["publishedAt"][:10])
            age = max(1, (today - pub).days)
            if age > days:
                continue
            views = int(v["statistics"].get("viewCount", 0))
            rows.append({"ch": nm, "id": v["id"], "pub": pub.isoformat(), "age": age,
                         "views": views, "vpd": views / age, "mins": mins,
                         "title": v["snippet"]["title"]})
    rows.sort(key=lambda r: -r["vpd"])
    print(f"=== PREMISE BANK — {len(rows)} video long-form ≤{days} ngày, xếp theo view/NGÀY ===\n")
    seen_ch = collections.Counter()
    out = []
    for r in rows:
        if seen_ch[r["ch"]] >= per:                        # trần mỗi kênh, tránh 1 kênh chiếm hết
            continue
        seen_ch[r["ch"]] += 1
        out.append(r)
    for i, r in enumerate(out, 1):
        print(f"{i:3}. {r['vpd']:>8,.0f} v/ngày · {r['views']:>8,}v · {r['mins']:5.0f}′ · "
              f"{r['pub']} · {r['ch']}")
        print(f"     {r['title']}")
        print(f"     https://youtu.be/{r['id']}")
    print(f"\n→ {len(out)} premise. Chép sang 01_SOURCES/ rồi REMAKE: đổi ≥8/10 yếu tố · "
          "rewrite 100% · không đoạn ≥25 ký trùng nguồn (youtube-compliance.md §1).")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel", default="chouhen", choices=sorted(CHANNELS))
    ap.add_argument("--traffic", action="store_true", help="view/AVD/traffic source mọi video")
    ap.add_argument("--related", metavar="VIDEO_ID|all", help="RELATED đến từ video/kênh nào")
    ap.add_argument("--peers", action="store_true", help="bộ kênh peer cùng rail")
    ap.add_argument("--premises", action="store_true",
                    help="gom PREMISE proven-viral từ peer (title = premise ở ngách này)")
    ap.add_argument("--days", type=int, default=30, help="cửa sổ premise (mặc định 30 ngày)")
    ap.add_argument("--per-channel", type=int, default=8, help="trần premise mỗi kênh")
    ap.add_argument("--peer-name", action="append", default=[], help="chỉ định tên kênh peer")
    a = ap.parse_args()
    if not (a.traffic or a.related or a.peers or a.premises):
        ap.error("chọn ít nhất một trong --traffic / --related / --peers / --premises")
    if a.traffic:
        cmd_traffic(a.channel)
    if a.related:
        cmd_related(a.channel, a.related)
    if a.peers:
        cmd_peers(a.channel, a.peer_name)
    if a.premises:
        cmd_premises(a.channel, a.peer_name, a.days, a.per_channel)


if __name__ == "__main__":
    main()
