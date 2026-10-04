# -*- coding: utf-8 -*-
"""Đo NGÀY đăng (weekday) + nhịp/tuần + median view theo ngày của đối thủ MỌI kênh workspace.

Standalone, dùng token readonly của nenkin (`youtube-jp-nenkin/credentials/token.json`).
Chạy: python measure_upload_days.py   → in bảng + ghi OUT_TXT/OUT_JSON.

Dùng để làm gì: nguồn số cho `.claude/rules/upload-schedule.md` (mục NGÀY ưu tiên).
Lần đo gần nhất 2026-07-28 → kết quả + kết luận: `.claude/rules/upload-schedule-measure-2026-07-28.md`.
**ĐO LẠI mỗi 6–8 tuần** (đối thủ dịch lịch thật: きな子 đã dời 18:00→20:00).

Đọc kết quả (rule §0 mục 2.5): số video/thứ = ngày đối thủ CHỌN · median view/thứ = ngày khán giả PHẢN ỨNG;
hai cái lệch nhau thì tin kênh có hiệu suất/video cao nhất, và luôn tách shorts (<8′) ra trước khi đếm.
Thêm/bớt kênh đối thủ: sửa list TARGETS (channelId None → tự search theo tên).
"""
import io, sys, json, datetime, collections, statistics
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

WD = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

# (nhóm kênh mình, tên đối thủ, channelId hoặc None -> search, tz offset giờ)
TARGETS = [
    # ── kaigo (ID đã biết)
    ("kaigo", "節約看護師りょう", "UCx2HEX7jkwrRsKXNgmIUMeA", 9),
    ("kaigo", "みんなの給付金・補助金", "UCt8oGxc3GJUqFvBTygzTr4A", 9),
    ("kaigo", "脱・税理士スガワラくん", "UCwKupwJ1EpdNH8Z98SKjY2Q", 9),
    ("kaigo", "ケアまど", "UClVcmctoyJ_wXZ1xlrlBMlQ", 9),
    # ── health / shokutaku
    ("health/shokutaku", "長生きの秘訣", None, 9),
    ("health/shokutaku", "みんなの若返りアカデミア", None, 9),
    ("health/shokutaku", "ご長寿ご健康", None, 9),
    # ── co-dai
    ("co-dai", "昔の人の知恵", None, 9),
    ("co-dai", "驚きの世界", None, 9),
    # ── chouhen
    ("chouhen", "苦しみの物語", None, 9),
    ("chouhen", "スカッとする話 朗読", None, 9),
    ("chouhen", "修羅場 朗読 スカッと", None, 9),
    # ── kr-romfan (KST cũng +9)
    ("kr-romfan", "민트 오디오북", None, 9),
    ("kr-romfan", "톡톡사이다", None, 9),
    ("kr-romfan", "랄라하", None, 9),
    ("kr-romfan", "사연튜브", None, 9),
    # ── nenkin
    ("nenkin", "年金・給付金完全攻略チャンネル", None, 9),
    ("nenkin", "シニアの年金・給付金速報", None, 9),
    # ── akiya
    ("akiya", "きな子のシニアお金ゼミ", None, 9),
    ("akiya", "まるごと安全相続ch-あまおう税理士", None, 9),
    ("akiya", "税理士勝部の相続チャンネル", None, 9),
    # ── showa (thêm 2026-08-14, lượt đo lập lịch cho kênh 昭和くらし図鑑)
    ("showa", "昭和の記憶装置", None, 9),
    ("showa", "伊東彩のほんのり昭和回顧", None, 9),
    ("showa", "ゆっくり昭和ボンバイエイ", None, 9),
    ("showa", "ヤチノちゃんねる", None, 9),
    ("showa", "昭和の女", None, 9),
    ("showa", "なつかし昭和チャンネル", None, 9),
    ("showa", "THEヤバイ昭和", None, 9),
    ("showa", "存在しない街の記憶", None, 9),
    ("showa", "昭和・平成 残響誌チャンネル", None, 9),
]

# Lọc nhóm: `python measure_upload_days.py --group showa` → chỉ đo cụm đó (đỡ đốt quota API).
# Không truyền cờ = đo hết như cũ. Nhiều nhóm: --group showa,co-dai
_g = None
for _i, _a in enumerate(sys.argv):
    if _a == "--group" and _i + 1 < len(sys.argv):
        _g = {x.strip() for x in sys.argv[_i + 1].split(",")}
    elif _a.startswith("--group="):
        _g = {x.strip() for x in _a.split("=", 1)[1].split(",")}
if _g:
    TARGETS = [t for t in TARGETS if t[0] in _g]
    if not TARGETS:
        sys.exit(f"Khong co target nao thuoc nhom {_g}")

out = []
def p(s=""):
    print(s); out.append(str(s))

def find_channel(q):
    try:
        r = yt.search().list(part="snippet", q=q, type="channel", maxResults=3,
                             regionCode="KR" if any(ord(c) > 0xAC00 and ord(c) < 0xD7A4 for c in q) else "JP").execute()
        items = r.get("items", [])
        if not items:
            return None, None
        # ưu tiên khớp tên chính xác
        for it in items:
            if it["snippet"]["title"].replace(" ", "") == q.replace(" ", ""):
                return it["snippet"]["channelId"], it["snippet"]["title"]
        return items[0]["snippet"]["channelId"], items[0]["snippet"]["title"]
    except Exception as e:
        p(f"   [search LỖI] {q}: {e!r}")
        return None, None

RESULTS = []

def analyze(group, name, cid, tzoff, n=50):
    ch = yt.channels().list(part="snippet,statistics,contentDetails", id=cid).execute()
    if not ch.get("items"):
        p(f"  ✗ {name}: không thấy channel"); return
    c = ch["items"][0]
    st = c["statistics"]
    up = c["contentDetails"]["relatedPlaylists"]["uploads"]
    items, tok = [], None
    while len(items) < n:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up,
                                    maxResults=min(50, n - len(items)), pageToken=tok).execute()
        items += r["items"]; tok = r.get("nextPageToken")
        if not tok: break
    vids = [i["contentDetails"]["videoId"] for i in items][:n]
    rows = []
    for i in range(0, len(vids), 50):
        vr = yt.videos().list(part="snippet,contentDetails,statistics",
                              id=",".join(vids[i:i+50])).execute()
        for v in vr["items"]:
            dt = datetime.datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(hours=tzoff)
            dur = v["contentDetails"]["duration"]
            secs = 0
            import re
            m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur)
            if m:
                h, mi, s = (int(x) if x else 0 for x in m.groups())
                secs = h*3600 + mi*60 + s
            rows.append((dt, secs, int(v["statistics"].get("viewCount", 0)), v["snippet"]["title"]))
    if not rows:
        p(f"  ✗ {name}: 0 video"); return
    rows.sort(key=lambda x: -x[0].timestamp())
    # chỉ tính long-form (>=8 phút) cho tín hiệu lịch long-form
    longs = [r for r in rows if r[1] >= 480]
    shorts_n = len(rows) - len(longs)
    span_days = max(1, (rows[0][0] - rows[-1][0]).days)
    per_week = len(rows) / (span_days / 7) if span_days else 0
    wd = collections.Counter(r[0].weekday() for r in rows)
    wdl = collections.Counter(r[0].weekday() for r in longs)
    hours = collections.Counter(r[0].hour for r in rows)
    # median view theo weekday (chỉ long-form, ≥3 mẫu)
    byday = collections.defaultdict(list)
    for r in longs:
        byday[r[0].weekday()].append(r[2])
    medview = {WD[k]: (int(statistics.median(v)), len(v)) for k, v in sorted(byday.items()) if len(v) >= 2}

    p(f"════ [{group}] {name}  ({cid})")
    p(f"  sub={int(st.get('subscriberCount',0)):,} · tổng video={st.get('videoCount')} · view={int(st.get('viewCount',0)):,}")
    p(f"  mẫu {len(rows)} video mới nhất ({rows[-1][0]:%Y-%m-%d} → {rows[0][0]:%Y-%m-%d}, {span_days} ngày) · shorts<8′: {shorts_n}")
    p(f"  NHỊP: {per_week:.2f} video/tuần")
    p(f"  NGÀY (tất cả): " + " ".join(f"{WD[k]}={wd.get(k,0)}" for k in range(7)))
    p(f"  NGÀY (long≥8′): " + " ".join(f"{WD[k]}={wdl.get(k,0)}" for k in range(7)))
    p(f"  GIỜ: {sorted(hours.items(), key=lambda x:-x[1])[:5]}")
    p(f"  median view theo NGÀY (long): {medview}")
    p(f"  3 video mới nhất: " + " | ".join(f"{r[0]:%m-%d %a %H:%M} {r[2]:,}v" for r in rows[:3]))
    p()
    RESULTS.append(dict(group=group, name=name, cid=cid, sub=int(st.get("subscriberCount", 0)),
                        per_week=round(per_week, 2), n=len(rows),
                        days_all={WD[k]: wd.get(k, 0) for k in range(7)},
                        days_long={WD[k]: wdl.get(k, 0) for k in range(7)},
                        medview_by_day=medview))

for group, q, cid, tzoff in TARGETS:
    if not cid:
        cid, title = find_channel(q)
        if not cid:
            p(f"════ [{group}] {q} → KHÔNG TÌM THẤY\n"); continue
        if title and title.replace(" ", "") != q.replace(" ", ""):
            p(f"  (search '{q}' → khớp kênh '{title}')")
        q = title or q
    try:
        analyze(group, q, cid, tzoff)
    except Exception as e:
        p(f"  ✗ {q}: LỖI {e!r}\n")

SC = Path(__file__).resolve().parents[1] / "06_VIDEO" / "_measure"; SC.mkdir(parents=True, exist_ok=True)
# Chạy có --group thì ghi file RIÊNG theo nhóm — đừng đè dữ liệu thô của lượt đo toàn bộ trước đó.
_sfx = ("_" + "-".join(sorted(_g))) if _g else ""
(SC / f"days_out{_sfx}.txt").write_text("\n".join(out), encoding="utf-8")
(SC / f"days_out{_sfx}.json").write_text(json.dumps(RESULTS, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"-> {SC / ('days_out' + _sfx + '.txt')}")
print("=== DONE ===")
