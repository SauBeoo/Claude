# -*- coding: utf-8 -*-
"""Do GIO dang (hour) <-> HIEU SUAT VIEW cua doi thu — bo sung cho measure_upload_days.py.

Vi sao can tool rieng: measure_upload_days.py chi DEM so video theo gio (Counter), khong he
do view theo gio. Lan do 2026-07-28 ghi thang "Gio dang KHONG do lai lan nay" => gio dang cua
workspace CHUA TUNG duoc do theo view.

PHUONG PHAP — 2 nhieu phai xu ly, khong thi ra so rac:
  N1 TUOI VIDEO: view tho cong don theo thoi gian => video cu luon nhieu view hon video moi.
     => metric chinh la VIEW/NGAY (view / so ngay tuoi), khong phai view tho.
  N2 CONFOUND KENH: gop video nhieu kenh roi so theo gio = do CHAT LUONG KENH, khong phai do GIO.
     => phan "trong cung MOT kenh" (within-channel) moi la phep so sach confound.
        Kenh khoa 1 gio => KHONG dung duoc de so gio.

Chay: python measure_upload_hours.py [--group chouhen,co-dai,health]
Ghi ra: 06_VIDEO/_measure/hours_out.{txt,json}
"""
import io
import sys
import json
import datetime
import collections
import statistics
import re
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
NOW = datetime.datetime.utcnow()

# (nhom kenh minh, ten doi thu, channelId hoac None -> search, tz offset)
#
# !! PIN channelId, DUNG de None. Bai hoc 2026-08-26: nganh スカッと co RAT NHIEU kenh CLONE
# trung ten Y HET. search() tra ve ban clone chet (嫁子 sub=0/1 video thay vi 233K/3363 video;
# 苦しみ sub=15/1 video thay vi 2.770/233) => bang do ra rac ma KHONG bao loi.
# Ten thuc te tren YouTube thuong co hau to 【...】; khop ten "chinh xac" lai an dung ban clone.
TARGETS = [
    # chouhen — peer THAT lay tu insightTrafficSourceDetail (CHANNEL_DIAGNOSIS_2026-08-12) + winner nganh
    ("chouhen", "嫁子のスカッと朗読劇場【スカッとする話】", "UCYASX2PAaV_7aEX6EPpP8Dg", 9),
    ("chouhen", "苦しみの物語【スカッとする話】", "UC-EgddGPbeKgbZKERv1XTXA", 9),
    ("chouhen", "毎日スカッと", "UCr06YgwC3IQp_x0qxsy3hwA", 9),
    ("chouhen", "語り茶屋", "UCdRX0G2uAsqWvgCErQcdCqg", 9),
    ("chouhen", "孤独な桜の木", "UC8oKWtvsFdR1vLSWRKIEiDA", 9),
    # co-dai
    ("co-dai", "昔の人の知恵", "UCYJ2D_D1q7_sYGorIB2_6iA", 9),
    ("co-dai", "驚きの世界", "UCRtqwdwjc-5M9lqEIUa-kGg", 9),
    # health / shokutaku — winner DANG THANG (KHONG dung 長生きの秘訣: da sup 45x, so la rac)
    ("health", "高齢者健康の真実", "UC58rGTlnLfvViwxO5_37yUA", 9),
    ("health", "健康長寿の知恵袋TV", "UCMXi6TOZA2NBpUKsIcLtNWQ", 9),
    ("health", "健康栄養研究室", "UCd21DCYmbpJfAHPM1GNEENQ", 9),
    ("health", "みんなの若返りアカデミア", "UCMNjTg2ihpmNWvpdg_0WT8g", 9),
]

groups = None
for i, a in enumerate(sys.argv):
    if a == "--group" and i + 1 < len(sys.argv):
        groups = sys.argv[i + 1].split(",")
    elif a.startswith("--group="):
        groups = a.split("=", 1)[1].split(",")
if groups:
    TARGETS = [t for t in TARGETS if t[0] in groups]

out = []


def p(s=""):
    print(s)
    out.append(str(s))


def find_channel(q):
    try:
        r = yt.search().list(part="snippet", q=q, type="channel",
                             maxResults=3, regionCode="JP").execute()
        it = r.get("items", [])
        if not it:
            return None, None
        for x in it:
            if x["snippet"]["title"].replace(" ", "") == q.replace(" ", ""):
                return x["snippet"]["channelId"], x["snippet"]["title"]
        return it[0]["snippet"]["channelId"], it[0]["snippet"]["title"]
    except Exception as e:
        p("   [search LOI] %s: %r" % (q, e))
        return None, None


def iso_secs(d):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d)
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


POOL = collections.defaultdict(list)
CHAN = []


def analyze(group, name, cid, tz, n=50):
    ch = yt.channels().list(part="snippet,statistics,contentDetails", id=cid).execute()
    if not ch.get("items"):
        p("  x %s: khong thay channel" % name)
        return
    c = ch["items"][0]
    st = c["statistics"]
    up = c["contentDetails"]["relatedPlaylists"]["uploads"]
    items, tok = [], None
    while len(items) < n:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up,
                                    maxResults=min(50, n - len(items)),
                                    pageToken=tok).execute()
        items += r["items"]
        tok = r.get("nextPageToken")
        if not tok:
            break
    vids = [i["contentDetails"]["videoId"] for i in items][:n]
    rows = []
    for i in range(0, len(vids), 50):
        vr = yt.videos().list(part="snippet,contentDetails,statistics",
                              id=",".join(vids[i:i + 50])).execute()
        for v in vr["items"]:
            utc = datetime.datetime.strptime(v["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            loc = utc + datetime.timedelta(hours=tz)
            secs = iso_secs(v["contentDetails"]["duration"])
            age = max(1.0, (NOW - utc).total_seconds() / 86400)
            views = int(v["statistics"].get("viewCount", 0))
            rows.append(dict(h=loc.hour, wd=loc.weekday(), secs=secs, views=views,
                             age=age, vpd=views / age, date=loc,
                             title=v["snippet"]["title"]))
    longs = [r for r in rows if r["secs"] >= 480]
    if not longs:
        p("  x %s: 0 long-form\n" % name)
        return
    longs.sort(key=lambda r: -r["date"].timestamp())
    span = max(1, (longs[0]["date"] - longs[-1]["date"]).days)
    byh = collections.defaultdict(list)
    for r in longs:
        byh[r["h"]].append(r)
    p("---- [%s] %s  sub=%s | long-form %d/%d | %s -> %s (%dd) | %.2f vid/tuan"
      % (group, name, format(int(st.get("subscriberCount", 0)), ","), len(longs), len(rows),
         longs[-1]["date"].strftime("%Y-%m-%d"), longs[0]["date"].strftime("%Y-%m-%d"),
         span, len(rows) / (span / 7.0)))
    p("     gio   n   median view    median VIEW/NGAY   tuoi TB (ngay) <- N3")
    for h in sorted(byh, key=lambda x: -len(byh[x])):
        g = byh[h]
        p("     %02dh  %-3d %11s   %14.1f   %8.1f"
          % (h, len(g), format(int(statistics.median([x["views"] for x in g])), ","),
             statistics.median([x["vpd"] for x in g]),
             statistics.median([x["age"] for x in g])))
    usable = sorted([h for h in byh if len(byh[h]) >= 3])
    verdict = "SO DUOC gio trong kenh nay" if len(usable) >= 2 \
        else "KHOA 1 GIO -> KHONG so duoc gio trong kenh nay"
    p("     => gio co n>=3: %s | %s" % (usable, verdict))
    p()
    for r in longs:
        POOL[group].append(dict(r, ch=name))
    CHAN.append(dict(group=group, name=name, cid=cid,
                     sub=int(st.get("subscriberCount", 0)),
                     n_long=len(longs), span_days=span,
                     hours={str(h): dict(
                         n=len(g),
                         med_view=int(statistics.median([x["views"] for x in g])),
                         med_vpd=round(statistics.median([x["vpd"] for x in g]), 1),
                         med_age=round(statistics.median([x["age"] for x in g]), 1))
                         for h, g in sorted(byh.items())},
                     usable_hours=usable))


for group, q, cid, tz in TARGETS:
    if not cid:
        cid, title = find_channel(q)
        if not cid:
            p("---- [%s] %s -> KHONG TIM THAY\n" % (group, q))
            continue
        if title and title.replace(" ", "") != q.replace(" ", ""):
            p("   (canh bao: search tra ve kenh khac ten -> %s)" % title)
    try:
        analyze(group, q, cid, tz)
    except Exception as e:
        p("  x %s: %r\n" % (q, e))

p("=" * 92)
p("TONG HOP THEO NGACH — gop video moi kenh trong ngach")
p("!! CONFOUND KENH: bang nay do lan ca chat luong kenh voi gio. Doc cung phan within-channel.")
p("=" * 92)
for g, rows in POOL.items():
    byh = collections.defaultdict(list)
    for r in rows:
        byh[r["h"]].append(r)
    p("")
    p("### %s  (%d video long-form / %d kenh)" % (g, len(rows), len({r["ch"] for r in rows})))
    p("  gio   n   #kenh   median view    median VIEW/NGAY")
    for h in sorted(byh):
        gg = byh[h]
        if len(gg) < 3:
            continue
        p("  %02dh  %-3d %-5d  %11s   %14.1f"
          % (h, len(gg), len({x["ch"] for x in gg}),
             format(int(statistics.median([x["views"] for x in gg])), ","),
             statistics.median([x["vpd"] for x in gg])))
    best = sorted([(statistics.median([x["vpd"] for x in v]), h, len(v), len({x["ch"] for x in v}))
                   for h, v in byh.items() if len(v) >= 3], reverse=True)
    if best:
        p("  -> xep theo view/ngay: " + " > ".join(
            "%02dh(%.0f/d,n=%d,%dkenh)" % (h, v, n, c) for v, h, n, c in best))

p("")
p("=" * 92)
p("WITHIN-CHANNEL — phep so DUY NHAT sach confound kenh")
p("=" * 92)
any_within = False
for c in CHAN:
    if len(c["usable_hours"]) < 2:
        continue
    any_within = True
    hs = sorted(c["usable_hours"], key=lambda h: -c["hours"][str(h)]["med_vpd"])
    p("  [%s] %s: %s" % (c["group"], c["name"], " > ".join(
        "%02dh %.0f v/d (n=%d, tuoi %.0fd)"
        % (h, c["hours"][str(h)]["med_vpd"], c["hours"][str(h)]["n"], c["hours"][str(h)]["med_age"])
        for h in hs)))
    # N3 RECENCY: view don ve nhung ngay dau => video MOI co v/d cao gia tao.
    # Neu gio thang cung la gio co video TRE NHAT thi ket luan khong dung duoc.
    top, bot = hs[0], hs[-1]
    at, ab = c["hours"][str(top)]["med_age"], c["hours"][str(bot)]["med_age"]
    if at < ab * 0.6:
        p("       !! CANH BAO RECENCY: gio thang (%02dh) co video TRE hon nhieu (%.0fd vs %.0fd)"
          " -> con so nay co the la artifact tuoi, KHONG phai hieu ung gio." % (top, at, ab))
    elif at > ab * 1.6:
        p("       (gio thang lai la gio video GIA hon: %.0fd vs %.0fd -> ket luan CHAC hon,"
          " vi bias recency dang chay NGUOC lai)" % (at, ab))
if not any_within:
    p("  KHONG co kenh nao dang 2 gio khac nhau voi n>=3 moi gio.")
    p("  => Trong bo doi thu nay, GIO KHONG PHAI BIEN DO DUOC: moi kenh khoa 1 gio,")
    p("     nen moi khac biet view giua cac gio deu la khac biet GIUA CAC KENH.")

Path("../06_VIDEO/_measure").mkdir(parents=True, exist_ok=True)
Path("../06_VIDEO/_measure/hours_out.txt").write_text("\n".join(out), encoding="utf-8")
Path("../06_VIDEO/_measure/hours_out.json").write_text(
    json.dumps(dict(measured_utc=NOW.isoformat(), channels=CHAN), ensure_ascii=False, indent=1),
    encoding="utf-8")
p("")
p("[da ghi] 06_VIDEO/_measure/hours_out.{txt,json}")
