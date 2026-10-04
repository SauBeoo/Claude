# -*- coding: utf-8 -*-
"""fetch_bg.py — gom clip nền động (mood đêm khuya trầm) cho scene_render → _bg/.

⛔ KHÔNG TÁI DÙNG ASSET (user chốt 2026-07-29, rule .claude/rules/media-library.md §2 —
thay chính sách 2026-07-16 "check kho trước, tái dùng khi cần"): mỗi video tải bộ
clip/ảnh MỚI của riêng nó. Nhánh "TỪ KHO" đã tắt.

Kho `Projects/_media_library` còn 2 vai: ① SỔ ĐEN — mọi asset có `used_in` (đã lên
sóng ở video nào đó) hoặc nằm trong `_bg/rejected/` bị cấm tải lại từ Pexels, vì cùng
query Pexels luôn trả về đúng clip cũ ② hồ sơ license. Đầu run vẫn sync USAGE.log.

Usage:
    python tools/fetch_bg.py "rain on window night" "candle flame dark"
    python tools/fetch_bg.py --per-query 2 "snow falling night"
    python tools/fetch_bg.py            # bộ query mặc định mood 真夜中
    python tools/fetch_bg.py --photos --per-query 12   # ẢNH tĩnh → _bgphotos/
                                                       # (cho scene_render --motion photo)
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_media_library"))
import media_lib  # noqa: E402

PROJ = Path(__file__).resolve().parents[1].name          # youtube-jp-chouhen
BG_DIR = Path(__file__).resolve().parents[1] / "06_VIDEO" / "_bg"
PHOTO_DIR = Path(__file__).resolve().parents[1] / "06_VIDEO" / "_bgphotos"
KEY = (Path(__file__).resolve().parents[2] / "youtube-jp-health/tools/.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0"}

DEFAULT_QUERIES = [
    "rain on window night", "candle flame dark calm", "moon clouds night sky",
    "snow falling night", "mist mountain slow", "city night bokeh",
    "japanese garden night", "tea cup steam dark", "fireplace embers dark",
]


def search_pexels(query, per=20):
    u = ("https://api.pexels.com/videos/search?orientation=landscape&size=medium"
         "&per_page=%d&query=%s" % (per, urllib.parse.quote(query)))
    req = urllib.request.Request(u, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def pick_file(vid):
    best = None
    for f in vid.get("video_files", []):
        if f.get("file_type") != "video/mp4":
            continue
        h = f.get("height") or 0
        if h == 0:
            continue
        score = -abs(h - 1080) - (2000 if h > 1600 else 0)
        if best is None or score > best[0]:
            best = (score, f["link"], f.get("width"), f.get("height"))
    return best


def search_pexels_photos(query, per=40):
    u = ("https://api.pexels.com/v1/search?orientation=landscape&size=large"
         "&per_page=%d&query=%s" % (per, urllib.parse.quote(query)))
    req = urllib.request.Request(u, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_photos(queries, per_query):
    """Gom ẢNH tĩnh mood 真夜中 → _bgphotos/ (cho scene_render --motion photo).

    Cùng luật clip: check KHO CHUNG trước (hardlink), miss mới tải Pexels rồi nhập kho;
    ảnh từng bị loại khi duyệt mắt nằm ở _bgphotos/rejected/ → KHÔNG lấy lại.
    """
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    exts = ("*.jpg", "*.jpeg", "*.png")
    have_names = {p.name for e in exts for p in PHOTO_DIR.glob(e)}
    rejected = {p.name for e in exts for p in (PHOTO_DIR / "rejected").glob(e)}
    if rejected:
        print(f"đã loại trước đây, sẽ không lấy lại: {len(rejected)} ảnh")
    have_names |= rejected
    idx = media_lib.load_index()
    have_ids = {idx.get(n, {}).get("source_id") for n in have_names}
    have_ids.discard(None)
    # cùng vá 2026-07-30 như nhánh clip: id lấy TỪ TÊN FILE, không chỉ tra INDEX
    # (index hụt 1 entry là ảnh đó tải lại được dưới tên khác → lặp hình trong 1 video)
    for _n in have_names:
        _m = re.search(r"_(\d{5,})\.[a-z]+$", _n)
        if _m:
            have_ids.add(_m.group(1))
    # sổ đen: ảnh đã LÊN SÓNG ở video khác → cấm tải lại (rule media-library.md §2)
    for _n, _e in idx.items():
        if _e.get("kind") == "photo" and _e.get("used_in") and _e.get("source_id"):
            have_ids.add(str(_e["source_id"]))
    print(f"sổ đen chống lặp: {len(have_ids)} id ảnh đã dùng/đã loại")
    got_lib = got_dl = 0

    for q in queries:
        need = per_query
        # ⛔ LẤY TỪ KHO ĐÃ TẮT (user chốt 2026-07-29, rule media-library.md §2:
        # "làm video nào tải ảnh của video đó thôi"). Kho còn 2 vai: sổ cái used_in
        # (= sổ đen chặn tải trùng, xem AIRED_IDS) + hồ sơ license.
        print(f"=== Pexels ảnh: {q} ===")
        try:
            data = search_pexels_photos(q)
        except Exception as e:
            print("  lỗi:", e)
            continue
        for ph in data.get("photos", []):
            if need <= 0:
                break
            pid, w, h_ = str(ph["id"]), ph.get("width", 0), ph.get("height", 0)
            if pid in have_ids or w < 1920:
                continue
            link = ph["src"].get("original") or ph["src"].get("large2x")
            slug = media_lib._slug(q, 12)
            dest = PHOTO_DIR / f"{slug}_{pid}.jpg"
            try:
                req = urllib.request.Request(link, headers=UA)
                with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as fo:
                    fo.write(r.read())
            except Exception as e:
                print("  lỗi tải:", e)
                continue
            media_lib.add_file(dest, "photo", source="pexels", source_id=pid,
                               url=ph.get("url", ""), query=q, tags=[slug.split("-")[0]],
                               width=w, height=h_, name=dest.name)
            have_ids.add(pid)
            have_names.add(dest.name)
            got_dl += 1
            need -= 1
            print(f"  OK {dest.name} {w}x{h_} ({dest.stat().st_size // 1024} KB) — đã nhập kho")

    total = len({p.name for e in exts for p in PHOTO_DIR.glob(e)})
    print(f"\nXong: {got_dl} ảnh tải mới (kho KHÔNG cấp asset nữa — rule §2). _bgphotos hiện có {total} ảnh.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="*", default=None)
    ap.add_argument("--per-query", type=int, default=1)
    ap.add_argument("--photos", action="store_true",
                    help="gom ẢNH tĩnh vào _bgphotos/ (scene_render --motion photo) "
                         "thay vì clip vào _bg/")
    args = ap.parse_args()
    queries = args.queries or DEFAULT_QUERIES
    if args.photos:
        fetch_photos(queries, args.per_query)
        return

    BG_DIR.mkdir(parents=True, exist_ok=True)
    # sync usage của kênh vào kho (idempotent) trước khi hỏi kho
    media_lib.ingest_bg(BG_DIR, PROJ)
    have_ids = {media_lib.load_index().get(p.name, {}).get("source_id")
                for p in BG_DIR.glob("*.mp4")}
    # 🔴 VÁ 2026-07-30: dòng trên CHỈ biết id qua INDEX.json. Index hụt 1 entry là clip đó
    # tải lại được dưới tên khác (tên pool = "<query-slug>_<id>.mp4", nên cùng clip qua 2
    # query ra 2 tên). Quét thật ra **18 id trùng thành 45 file**, id 31387301 có 5 bản —
    # nghĩa là cùng một đoạn phim xuất hiện nhiều lần trong cùng một video, và `used_in` sai.
    # → Lấy id TRỰC TIẾP TỪ TÊN FILE làm nguồn sự thật thứ hai, không phụ thuộc index.
    for _p in list(BG_DIR.glob("*.mp4")) + list((BG_DIR / "rejected").glob("*.mp4")):
        _m = re.search(r"_(\d{5,})\.mp4$", _p.name)
        if _m:
            have_ids.add(_m.group(1))
    have_names = {p.name for p in BG_DIR.glob("*.mp4")}
    # Clip từng bị loại khi duyệt mắt → KHÔNG kéo lại từ kho, KHÔNG tải lại.
    # (bug 2026-07-26: kho chung không ghi nhận "đã loại" nên clip loại quay lại _bg
    #  qua hardlink và lọt vào bản render video 09.)
    rejected_names = {p.name for p in (BG_DIR / "rejected").glob("*.mp4")}
    if rejected_names:
        print(f"đã loại trước đây, sẽ không lấy lại: {len(rejected_names)} clip")
    have_names |= rejected_names
    rejected_ids = {media_lib.load_index().get(n, {}).get("source_id")
                    for n in rejected_names}
    have_ids |= {i for i in rejected_ids if i}
    got_lib = got_dl = 0

    # ⛔ LẤY TỪ KHO ĐÃ TẮT (user chốt 2026-07-29, rule media-library.md §2). Đổi lại:
    # mọi clip đã LÊN SÓNG ở video khác thành SỔ ĐEN — cấm tải lại từ Pexels, vì cùng
    # query Pexels luôn trả đúng clip cũ.
    for _n, _e in media_lib.load_index().items():
        if _e.get("kind") == "clip" and _e.get("used_in") and _e.get("source_id"):
            have_ids.add(str(_e["source_id"]))
    print(f"sổ đen chống lặp: {len(have_ids)} id đã dùng/đã loại")

    for q in queries:
        need = args.per_query
        print(f"=== Pexels: {q} ===")
        try:
            data = search_pexels(q)
        except Exception as e:
            print("  lỗi:", e)
            continue
        cands = []
        for v in data.get("videos", []):
            dur = v.get("duration", 0)
            if dur < 8 or dur > 90:
                continue
            pf = pick_file(v)
            if pf and str(v["id"]) not in have_ids:
                cands.append((v["id"], dur, pf, v.get("user", {}).get("name", "")))
        cands.sort(key=lambda c: c[2][0], reverse=True)
        for cid, dur, pf, author in cands[:need]:
            slug = media_lib._slug(q, 12)
            dest = BG_DIR / f"{slug}_{cid}.mp4"
            print(f"  tải id={cid} {pf[2]}x{pf[3]} {dur}s by {author} …")
            try:
                req = urllib.request.Request(pf[1], headers=UA)
                with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as fo:
                    fo.write(r.read())
            except Exception as e:
                print("  lỗi tải:", e)
                continue
            media_lib.add_file(dest, "clip", source="pexels", source_id=cid,
                               url=f"https://www.pexels.com/video/{cid}/",
                               query=q, tags=[slug.split("-")[0]],
                               width=pf[2], height=pf[3], duration=dur,
                               name=dest.name)
            have_ids.add(str(cid))
            have_names.add(dest.name)
            got_dl += 1
            print(f"  OK {dest.name} ({dest.stat().st_size // 1024} KB) — đã nhập kho")

    total = len(list(BG_DIR.glob("*.mp4")))
    print(f"\nXong: {got_dl} clip tải mới (kho KHÔNG cấp asset nữa — rule §2). _bg hiện có {total} clip.")


if __name__ == "__main__":
    main()
