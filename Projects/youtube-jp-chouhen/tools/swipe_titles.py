# -*- coding: utf-8 -*-
"""Quét GROWTH VIDEO của đối thủ → nạp swipe file 01_SWIPE_TITLES.md cho từng kênh.

Thi hành rule `.claude/rules/youtube-suggested-growth.md` §2 (chốt 2026-08-21):
- growth video = view ≥ 3× sub của kênh đăng nó (khán giả đã bỏ phiếu vượt tệp sub)
- ưu tiên video ≤30 ngày (feedback_benchmark_30_ngay); 31–60 ngày đánh dấu 🟡
- long-form ≥8 phút, tách shorts

Standalone, token readonly nenkin (như measure_upload_days.py / bench_channels.py).
Chạy: python swipe_titles.py [--group chouhen,health] [--days 60] [--ratio 3.0]
Output: Projects/<project>/01_SWIPE_TITLES.md (chouhen: 01_SOURCES/SWIPE_TITLES.md)
"""
import io, sys, re, datetime, argparse
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

PROJ = Path(r"E:\Claude\Projects")
NOW = datetime.datetime.now(datetime.timezone.utc)

# nhóm kênh mình → (project folder, file output, list đối thủ [tên hoặc channelId])
GROUPS = {
    "chouhen": {
        "project": "youtube-jp-chouhen",
        "out": "01_SOURCES/SWIPE_TITLES.md",
        "rivals": [
            "毎日スカッと", "語り茶屋", "孤独な桜の木", "裏話オーディオ",
            "スカっとゼミ", "嫁子のスカッと朗読劇場", "苦しみの物語", "世界の中心でスカッと朗読",
        ],
    },
    "health": {
        "project": "youtube-jp-health",
        "out": "01_SWIPE_TITLES.md",
        "rivals": [
            "高齢者健康の真実", "健康長寿の知恵袋TV", "健康栄養研究室",
            "みんなの若返りアカデミア", "健康の知恵袋",
        ],
    },
    "shokutaku": {
        "project": "youtube-jp-shokutaku",
        "out": "01_SWIPE_TITLES.md",
        "rivals": [
            "高齢者健康の真実", "健康長寿の知恵袋TV", "健康栄養研究室", "シニア 食卓 健康",
        ],
    },
    "co-dai": {
        "project": "youtube-jp-co-dai",
        "out": "01_SWIPE_TITLES.md",
        "rivals": ["昔の人の知恵", "驚きの世界", "生活の知恵 昔ながら"],
    },
    "nenkin": {
        "project": "youtube-jp-nenkin",
        "out": "01_SWIPE_TITLES.md",
        "rivals": [
            "年金・給付金完全攻略チャンネル", "シニアの年金・給付金速報", "お金の保健室",
            "フクロウの年金・給付金解説室", "タヌキの年金相談室",
            "節約看護師りょう", "みんなの給付金・補助金",
        ],
    },
    "showa": {
        "project": "youtube-jp-showa",
        "out": "01_SWIPE_TITLES.md",
        "rivals": [
            "伊東彩のほんのり昭和回顧", "なつかし昭和チャンネル", "昭和の記憶装置",
            "THEヤバイ昭和", "存在しない街の記憶",
        ],
    },
}


def iso_dur(d):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def find_channel(name):
    if name.startswith("UC") and len(name) == 24:
        return name
    r = yt.search().list(part="snippet", q=name, type="channel", maxResults=3).execute()
    items = r.get("items", [])
    if not items:
        return None
    # ưu tiên kênh tên chứa query (search fuzzy hay trả kênh lạ)
    for it in items:
        t = it["snippet"]["title"]
        if name[:6] in t or t[:6] in name:
            return it["snippet"]["channelId"]
    return items[0]["snippet"]["channelId"]


def scan_channel(cid, days, min_dur=480):
    r = yt.channels().list(part="snippet,statistics,contentDetails", id=cid).execute()
    if not r.get("items"):
        return None
    c = r["items"][0]
    subs = int(c["statistics"].get("subscriberCount", 0) or 0)
    upl = c["contentDetails"]["relatedPlaylists"]["uploads"]
    vids, page = [], None
    for _ in range(2):  # 100 video mới nhất là đủ cho cửa sổ 60 ngày
        pr = yt.playlistItems().list(part="contentDetails", playlistId=upl,
                                     maxResults=50, pageToken=page).execute()
        vids += [i["contentDetails"]["videoId"] for i in pr.get("items", [])]
        page = pr.get("nextPageToken")
        if not page:
            break
    rows = []
    for i in range(0, len(vids), 50):
        vr = yt.videos().list(part="snippet,statistics,contentDetails",
                              id=",".join(vids[i:i + 50])).execute()
        for v in vr.get("items", []):
            dur = iso_dur(v["contentDetails"].get("duration"))
            if dur < min_dur:
                continue
            pub = datetime.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            age = (NOW - pub).days
            if age > days:
                continue
            view = int(v["statistics"].get("viewCount", 0) or 0)
            rows.append({
                "id": v["id"], "title": v["snippet"]["title"], "view": view,
                "age": age, "dur": dur,
                "ratio": (view / subs) if subs else 0.0,
                "vpd": view / max(age, 1),
            })
    return {"name": c["snippet"]["title"], "cid": cid, "subs": subs, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", default=None, help="vd: chouhen,health — bỏ trống = tất cả")
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--ratio", type=float, default=3.0)
    a = ap.parse_args()
    groups = {k.strip() for k in a.group.split(",")} if a.group else set(GROUPS)

    today = datetime.date.today().isoformat()
    for key, cfg in GROUPS.items():
        if key not in groups:
            continue
        print(f"\n{'=' * 100}\n### NHÓM {key}")
        entries, notes = [], []
        for rv in cfg["rivals"]:
            cid = find_channel(rv)
            if not cid:
                notes.append(f"- ⚠️ không tìm thấy kênh: {rv}")
                print(f"  [MISS] {rv}")
                continue
            ch = scan_channel(cid, a.days)
            if not ch:
                continue
            print(f"  {ch['name']} · sub={ch['subs']:,} · {len(ch['rows'])} long-form ≤{a.days}d")
            for r in ch["rows"]:
                r["channel"] = ch["name"]
                r["subs"] = ch["subs"]
                entries.append(r)

        growth = sorted([e for e in entries if e["subs"] and e["ratio"] >= a.ratio],
                        key=lambda x: -x["ratio"])
        # fallback: nếu growth <10, bổ sung theo view/ngày để sổ vẫn có hàng đọc ngách
        top_vpd = sorted(entries, key=lambda x: -x["vpd"])[:15]

        lines = [
            f"# SWIPE TITLES — {key} (quét {today}, cửa sổ ≤{a.days} ngày, long-form ≥8′)",
            "",
            f"> Rule: `.claude/rules/youtube-suggested-growth.md` §2. GROWTH = view ≥ {a.ratio:g}× sub kênh đăng.",
            "> ✅ = nhận vào sổ (≤30 ngày) · 🟡 = 31–60 ngày, đo lại trước khi dùng · ⚪ = chưa đạt ngưỡng,",
            "> chỉ để đọc ngách đang ăn gì. Mục >6–8 tuần phải quét lại (chạy lại tool này).",
            "> Cách dùng: chọn đề tài mới thì mở sổ này TRƯỚC — lấy GÓC, viết bản tốt hơn, KHÔNG copy chữ.",
            "",
            "## GROWTH VIDEO (view/sub cao nhất)",
            "",
            "| | ratio | view | sub kênh | tuổi | dài | kênh | title |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for e in growth[:25]:
            mark = "✅" if e["age"] <= 30 else "🟡"
            lines.append(
                f"| {mark} | **{e['ratio']:.1f}×** | {e['view']:,} | {e['subs']:,} | {e['age']}d "
                f"| {e['dur'] // 60}′ | {e['channel']} | `{e['title']}` |")
        if not growth:
            lines.append("| — | | | | | | | (không có video nào đạt ngưỡng trong cửa sổ) |")
        lines += ["", "## THAM KHẢO — view/ngày cao nhất (đọc ngách, chưa chắc là growth)", "",
                  "| view/ngày | view | tuổi | kênh | title |", "|---|---|---|---|---|"]
        for e in top_vpd:
            lines.append(f"| {e['vpd']:,.0f} | {e['view']:,} | {e['age']}d | {e['channel']} | `{e['title']}` |")
        lines += [""] + notes + [""]

        outp = PROJ / cfg["project"] / cfg["out"]
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text("\n".join(lines), encoding="utf-8")
        print(f"  → {outp}  (growth: {len(growth)} · tham khảo: {len(top_vpd)})")


if __name__ == "__main__":
    main()
