# -*- coding: utf-8 -*-
r"""ĐO CẦU KEYWORD BẰNG YOUTUBE DATA API (thay Google Trends khi Trends không render).

    python tools\measure_kw_youtube.py "熱中症対策 飲み物" "熱中症 高齢者" --days 30

Vì sao có tool này (2026-08-03): Google Trends explore không còn render chart trên máy
này ("Google トレンドは新しいバージョンにアップグレードされたため、このデバイスでは
使用できません") → 3 lần thử đều ra panel trắng. Rule `youtube-upload-seo.md` §0.5 đòi
ĐO TRƯỚC khi chốt title/tag; đo bằng API còn mạnh hơn Trends vì trả **view thật** thay
vì chỉ số tương đối, và khớp luật benchmark ≤30 ngày.

Đọc bảng: `n` = số video long-form (≥8′) đăng trong `--days` ngày mà YouTube trả về cho
keyword đó (nguồn cung + tín hiệu YouTube có coi đây là truy vấn sống hay không);
`med v/ngày` = view/ngày trung vị (cầu trên mỗi video); `max` = video mạnh nhất.
"""
import argparse
import io
import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
TOKEN = Path(__file__).resolve().parent.parent / "credentials" / "token.json"


def yt():
    c = Credentials.from_authorized_user_file(str(TOKEN))
    if not c.valid and c.refresh_token:
        c.refresh(Request())
        TOKEN.write_text(c.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=c, cache_discovery=False)


def dur_sec(iso):
    n, cur = {"H": 0, "M": 0, "S": 0}, ""
    for ch in iso.replace("PT", ""):
        if ch.isdigit():
            cur += ch
        elif ch in n:
            n[ch] = int(cur or 0)
            cur = ""
    return n["H"] * 3600 + n["M"] * 60 + n["S"]


def measure(api, kw, days, minsec, want):
    after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = api.search().list(q=kw, part="id", type="video", maxResults=want, order="viewCount",
                          publishedAfter=after, regionCode="JP", relevanceLanguage="ja").execute()
    ids = [i["id"]["videoId"] for i in r.get("items", [])]
    if not ids:
        return []
    v = api.videos().list(id=",".join(ids), part="statistics,contentDetails,snippet").execute()
    out = []
    now = datetime.now(timezone.utc)
    for it in v.get("items", []):
        if dur_sec(it["contentDetails"]["duration"]) < minsec:
            continue
        pub = datetime.fromisoformat(it["snippet"]["publishedAt"].replace("Z", "+00:00"))
        age = max((now - pub).total_seconds() / 86400, 0.5)
        views = int(it["statistics"].get("viewCount", 0))
        out.append({"title": it["snippet"]["title"][:46], "ch": it["snippet"]["channelTitle"][:18],
                    "views": views, "vpd": views / age, "age": age})
    return sorted(out, key=lambda x: -x["vpd"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("keywords", nargs="+")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--min-min", type=float, default=8, help="lọc long-form, phút (0 = lấy hết)")
    ap.add_argument("--want", type=int, default=25)
    ap.add_argument("--top", type=int, default=3, help="in mấy video mạnh nhất mỗi keyword")
    a = ap.parse_args()

    api = yt()
    print(f"ĐO CẦU YOUTUBE — {a.days} ngày · JP/ja · long-form ≥{a.min_min:g}′ · "
          f"{datetime.now().strftime('%Y-%m-%d')}\n")
    rows = []
    for kw in a.keywords:
        vids = measure(api, kw, a.days, int(a.min_min * 60), a.want)
        if not vids:
            print(f"🔴 {kw}: 0 video long-form trong {a.days} ngày")
            rows.append((kw, 0, 0, 0))
            continue
        vpd = [x["vpd"] for x in vids]
        rows.append((kw, len(vids), statistics.median(vpd), max(vpd)))
        print(f"■ {kw} — n={len(vids)} · med {statistics.median(vpd):,.0f} v/ngày · "
              f"max {max(vpd):,.0f} v/ngày")
        for x in vids[:a.top]:
            print(f"    {x['vpd']:>8,.0f} v/ngày · {x['views']:>9,} view · {x['age']:>4.1f}d · "
                  f"{x['ch']} · {x['title']}")
        print()

    print("— BẢNG XẾP (theo med v/ngày) —")
    print(f"{'keyword':<28}{'n':>4}{'med v/ngày':>13}{'max v/ngày':>13}")
    for kw, n, med, mx in sorted(rows, key=lambda r: -r[2]):
        print(f"{kw:<28}{n:>4}{med:>13,.0f}{mx:>13,.0f}")


if __name__ == "__main__":
    main()
