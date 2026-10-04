# -*- coding: utf-8 -*-
"""bench_topic.py — đo CẦU THẬT của một chủ đề trên YouTube (không phải điểm Trends).

VÌ SAO CÓ TOOL NÀY:
Google Trends chỉ nói "có người gõ từ này nhiều hay ít", và điểm của nó là **tương đối
trong từng rổ** → KHÔNG so được giữa 2 lần đo khác rổ (bẫy đã gặp: 加給年金 24 vs
年金支給日 28 là hai rổ khác nhau, so trực tiếp là sai). Tệ hơn: từ có volume cao mà
**intent nông** (「年金支給日」= chỉ muốn biết ngày mấy) thì tra xong đi luôn, không xem
video 28 phút. Tool này đo thứ đúng hơn: **với từ khoá đó, video long-form THẬT ăn bao
nhiêu view, ai làm, và có còn tươi không.**

CÁCH ĐỌC (quan trọng):
  · median view của long-form  → cầu có chuyển thành lượt xem không
  · số video ≥100K            → chủ đề có "trần" cao hay bị đóng ở vài nghìn view
  · view/ngày của video ≤90d  → cầu CÒN SỐNG hay chỉ là hit cũ
  · sub của kênh làm nó       → chủ đề tự kéo view, hay chỉ kênh to mới kéo được
  · số video đăng ≤90d        → mật độ cạnh tranh / mức bão hoà

CHẠY:  python tools/bench_topic.py                      (rổ mặc định)
       python tools/bench_topic.py "加給年金" "遺族年金"   (rổ tự chọn)
Ra: bảng ra màn hình + 06_VIDEO/_bench_topic/topic_out.{txt,json}
"""
import collections
import datetime
import io
import json
import re
import statistics
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

PROJ = Path(__file__).resolve().parents[1]
CRED = PROJ / "credentials"
creds = Credentials.from_authorized_user_file(str(CRED / "token.json"))
if not creds.valid:
    creds.refresh(Request())
    (CRED / "token.json").write_text(creds.to_json(), encoding="utf-8")
yt = build("youtube", "v3", credentials=creds)

NOW = datetime.datetime.utcnow()
MIN_SEC = 8 * 60          # <8 phút = Shorts/clip ngắn, không phải đối thủ long-form
LOOKBACK_DAYS = 540       # ~18 tháng: đủ để thấy cả hit cũ lẫn nguồn cung mới

DEFAULT = [
    "年金振込通知書",      # tên chứng từ của video 08
    "年金支給日",          # keyword dẫn đang chốt
    "年金 手取り",         # keyword #2
    "加給年金",            # ⚖️ ĐỐI CHỨNG: chủ đề video 06 của chính kênh
    "年金 いくらもらえる",  # ⚖️ ĐỐI CHỨNG: mega-topic của ngách
]

OUT = PROJ / "06_VIDEO" / "_bench_topic"


def iso_dur(d):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    dd, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return dd * 86400 + h * 3600 + mi * 60 + s


def fetch(query):
    """Lấy video của 1 query theo 2 trục: view cao nhất + mới nhất."""
    ids, order_of = [], {}
    for order in ("viewCount", "date"):
        try:
            r = yt.search().list(
                part="id", q=query, type="video", order=order,
                regionCode="JP", relevanceLanguage="ja", maxResults=50,
                publishedAfter=(NOW - datetime.timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            ).execute()
        except Exception as e:
            print(f"  [LỖI search {order}] {e}")
            continue
        for it in r.get("items", []):
            vid = it["id"]["videoId"]
            if vid not in order_of:
                order_of[vid] = order
                ids.append(vid)

    vids = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,contentDetails,statistics",
                             id=",".join(ids[i:i + 50])).execute()
        for it in r.get("items", []):
            sec = iso_dur(it["contentDetails"].get("duration"))
            pub = datetime.datetime.strptime(it["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            age = max(1, (NOW - pub).days)
            vids.append({
                "id": it["id"], "title": it["snippet"]["title"],
                "channel": it["snippet"]["channelTitle"], "chId": it["snippet"]["channelId"],
                "pub": pub.strftime("%Y-%m-%d"), "age": age, "sec": sec,
                "view": int(it["statistics"].get("viewCount", 0)),
                "vpd": int(it["statistics"].get("viewCount", 0)) / age,
                "long": sec >= MIN_SEC, "found_by": order_of.get(it["id"]),
            })
    return vids


def chan_subs(ch_ids):
    out = {}
    ids = list(dict.fromkeys(ch_ids))
    for i in range(0, len(ids), 50):
        r = yt.channels().list(part="statistics", id=",".join(ids[i:i + 50])).execute()
        for it in r.get("items", []):
            out[it["id"]] = int(it["statistics"].get("subscriberCount", 0))
    return out


def main():
    queries = sys.argv[1:] or DEFAULT
    L, rows = [], {}

    def p(s=""):
        print(s)
        L.append(s)

    p(f"ĐO CẦU CHỦ ĐỀ — {NOW.strftime('%Y-%m-%d')} · geo=JP · long-form ≥{MIN_SEC // 60}′ · cửa sổ {LOOKBACK_DAYS} ngày")
    p("=" * 100)

    for q in queries:
        vids = fetch(q)
        lf = [v for v in vids if v["long"]]
        subs = chan_subs([v["chId"] for v in lf]) if lf else {}
        fresh = [v for v in lf if v["age"] <= 90]
        big = [v for v in lf if v["view"] >= 100_000]
        rows[q] = {
            "n_all": len(vids), "n_long": len(lf),
            "median_view": int(statistics.median([v["view"] for v in lf])) if lf else 0,
            "max_view": max([v["view"] for v in lf], default=0),
            "n_over_100k": len(big),
            "n_fresh_90d": len(fresh),
            "median_vpd_fresh": round(statistics.median([v["vpd"] for v in fresh]), 1) if fresh else 0,
            "top": [{k: v[k] for k in ("title", "channel", "pub", "view", "vpd", "sec")}
                    | {"subs": subs.get(v["chId"], 0)}
                    for v in sorted(lf, key=lambda x: -x["view"])[:5]],
        }
        r = rows[q]
        p()
        p(f"■ 「{q}」")
        p(f"  long-form: {r['n_long']}/{r['n_all']} video · median {r['median_view']:,} view · cao nhất {r['max_view']:,}")
        p(f"  video ≥100K: {r['n_over_100k']}   ·   đăng trong 90 ngày: {r['n_fresh_90d']} (median {r['median_vpd_fresh']} view/ngày)")
        for v in r["top"]:
            p(f"    {v['view']:>9,}  {v['vpd']:>7.0f}/ngày  {v['sec']//60:>3}′  {v['pub']}  [{v['subs']:>8,} sub]  {v['channel'][:22]:<22} {v['title'][:52]}")

    p()
    p("=" * 100)
    p("BẢNG SO — cột quyết định là median view của long-form (cầu → lượt xem) và số video ≥100K (trần)")
    p(f"{'query':<22}{'long':>6}{'median view':>14}{'max view':>12}{'≥100K':>7}{'mới 90d':>9}{'v/ngày':>9}")
    for q in queries:
        r = rows[q]
        p(f"{q:<22}{r['n_long']:>6}{r['median_view']:>14,}{r['max_view']:>12,}{r['n_over_100k']:>7}{r['n_fresh_90d']:>9}{r['median_vpd_fresh']:>9}")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "topic_out.txt").write_text("\n".join(L), encoding="utf-8")
    (OUT / "topic_out.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    p()
    p(f"→ {OUT / 'topic_out.txt'}")


if __name__ == "__main__":
    main()
