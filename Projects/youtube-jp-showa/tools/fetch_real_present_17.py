# -*- coding: utf-8 -*-
"""
[fetch_real_present_17] ban sao cua fetch_real_ima_ie_17 cho cac cau 'bay gio' (so lieu Heisei/Reiwa) — user 23/09: tim anh/video that truoc, thieu moi dung AI.
Kéo footage THẬT (Pexels, free thương mại) thay 8 cảnh AI "thời nay" (ima_ie) của video 17 — user 2026-09-23:
*"tạm thời tao không tạo được video AI nên những cái này mày thay bằng video thật cho tao"*.

Vì sao 8 cảnh này thay được bằng stock mà cảnh 昭和 thì không: ima_ie là ĐỜI THƯỜNG HÔM NAY (ông già, phòng khách,
tờ giấy cũ) — kho stock có; cảnh văn phòng 1970 thì không.

Chạy:  python tools/fetch_real_ima_ie_17.py              # tìm + tải ứng viên + contact sheet
       python tools/fetch_real_ima_ie_17.py --dry        # chỉ liệt kê, không tải
Xuất:  06_VIDEO/17_kaisha-ga-kureta/clips_real_ima_ie/   (mp4 ứng viên + MANIFEST.json + _sheet.jpg)
Luật: media-library.md §2 — mỗi video tải bộ MỚI, id đã lên sóng video khác (AIRED) không tải lại; license + url
      ghi MANIFEST để `ATTRIBUTIONS.md` (Pexels không bắt credit, vẫn ghi nguồn). Duyệt sheet bằng MẮT rồi mới gán slot.
"""
import io, json, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_media_library"))
import media_lib  # noqa: E402

KEY = (HERE.parents[1] / "youtube-jp-health" / "tools" / ".pexels_key").read_text().strip()
OUT = HERE.parent / "06_VIDEO" / "17_kaisha-ga-kureta" / "clips_real_present"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
MIN_W, MIN_DUR, MAX_DUR, PER_Q = 1280, 6, 40, 3

# 8 cảnh ima_ie (idx 4·5·102·103·104·108·109·111) → 6 nhóm hình cần có. Query tiếng Anh kiểu Pexels.
QUERIES = [
 ("P1_tokyo_office_crowd",  "tokyo business people walking office"),
 ("P2_tokyo_crossing",      "tokyo crosswalk crowd businessmen"),
 ("P3_tokyo_commute_train", "tokyo train commuters rush hour"),
 ("P4_japan_station",       "japan station platform commuters"),
 ("P5_japan_office",        "japanese office workers desk"),
 ("P6_tokyo_skyline",       "tokyo office buildings skyline"),
 ("P7_japan_apartment",     "japanese apartment complex buildings"),
 ("P8_danchi",              "old apartment block japan balcony laundry"),
 ("P9_yen_money",           "japanese yen banknotes counting"),
 ("P10_yen_coins",          "japanese yen coins"),
 ("P11_calculator_paper",   "calculator documents hands close up"),
 ("P12_salaryman",          "japanese salaryman"),
 ("P13_tokyo_evening",      "tokyo street evening office workers"),
 ("P14_hanko",              "japanese stamp hanko"),
]
# rac ro tu lan --dry (kinh VR, poker, video call, cannabis, oximeter, laptop, co vua)
BLOCK = {"8944276", "6667257", "7331781", "8139442", "7308048", "8375661", "10223723", "7924409",
         "5959769", "8086921", "7507165", "7507166", "8164521", "7577972", "8124296"}


def api(url):
    req = urllib.request.Request(url, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def best_file(v):
    fs = [f for f in v.get("video_files", []) if f.get("width") and f["width"] >= MIN_W and f.get("file_type") == "video/mp4"]
    fs.sort(key=lambda f: (abs(f["width"] - 1920), -f["width"]))
    return fs[0] if fs else None


def aired_ids():
    idx = media_lib.load_index()
    s = set()
    for e in idx.values() if isinstance(idx, dict) else idx:
        if e.get("kind") == "clip" and e.get("used_in"):
            s.add(str(e.get("source_id", "")))
            m = re.search(r"/video/[^/]*?-?(\d+)/?$", e.get("url", "") or "")
            if m: s.add(m.group(1))
    return s


def main():
    dry = "--dry" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    aired = aired_ids()
    print(f"so den AIRED: {len(aired)} clip")
    man, seen = [], set()
    for tag, q in QUERIES:
        url = ("https://api.pexels.com/videos/search?" +
               urllib.parse.urlencode({"query": q, "per_page": 15, "orientation": "landscape", "size": "medium"}))
        try:
            data = api(url)
        except Exception as e:
            print(f"  [{tag}] API loi: {e}"); continue
        got = 0
        for v in data.get("videos", []):
            vid = str(v["id"])
            if vid in aired or vid in seen or vid in BLOCK: continue
            if not (MIN_DUR <= v.get("duration", 0) <= MAX_DUR): continue
            f = best_file(v)
            if not f: continue
            seen.add(vid); got += 1
            dest = OUT / f"{tag}_{vid}.mp4"
            row = dict(tag=tag, query=q, id=vid, dur=v["duration"], w=f["width"], h=f["height"],
                       url=v["url"], file=dest.name, user=v.get("user", {}).get("name", ""),
                       license="Pexels License (free commercial, no attribution required)")
            man.append(row)
            print(f"  [{tag}] {vid} {v['duration']}s {f['width']}x{f['height']} {v['url']}")
            if not dry and not dest.exists():
                req = urllib.request.Request(f["link"], headers=UA)
                with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as fh:
                    while True:
                        c = r.read(1 << 20)
                        if not c: break
                        fh.write(c)
            if got >= PER_Q: break
        if got == 0: print(f"  [{tag}] KHONG co ket qua dat loc")
    with io.open(OUT / "MANIFEST.json", "w", encoding="utf-8") as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    print(f"\n{len(man)} ung vien -> {OUT}")
    if dry: return 0
    # contact sheet: 2 frame/clip (30% · 70%), nhan = tag_id
    tiles = []
    for row in man:
        p = OUT / row["file"]
        if not p.exists(): continue
        for k, t in enumerate((0.3, 0.7)):
            tile = OUT / f"_t_{row['id']}_{k}.jpg"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{row['dur']*t:.2f}", "-i", str(p), "-frames:v", "1",
                            "-vf", "scale=320:180", str(tile)])
            if tile.exists(): tiles.append((tile, f"{row['tag'][:2]} {row['id']} {row['dur']}s"))
    try:
        import cv2, numpy as np
        ims = []
        for t, lab in tiles:
            im = cv2.imread(str(t))
            if im is None: continue
            cv2.putText(im, lab, (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1); ims.append(im)
        cols = 8; rows = (len(ims) + cols - 1) // cols
        sheet = np.full((rows * 184, cols * 324, 3), 15, np.uint8)
        for i, im in enumerate(ims):
            r, c = divmod(i, cols); sheet[r*184:r*184+180, c*324:c*324+320] = im
        cv2.imwrite(str(OUT / "_sheet.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 82])
        print(f"sheet: {OUT / '_sheet.jpg'}")
    finally:
        for t, _ in tiles:
            try: t.unlink()
            except OSError: pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
