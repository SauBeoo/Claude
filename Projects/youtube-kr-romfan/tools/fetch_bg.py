# -*- coding: utf-8 -*-
"""fetch_bg.py — tải clip nền động cozy/romance từ Pexels Video API → 04_VIDEO/_bg/.

Khác chouhen (1 clip/lần): kênh KR dùng 20-25 cảnh động luân phiên MỖI video
(chống flag inauthentic "nền loop + giọng AI") → tool này tải NHIỀU clip một lượt.

Usage:
    python tools/fetch_bg.py                          # tải theo bộ query mặc định (mỗi query 1 clip)
    python tools/fetch_bg.py "rain on window night" "cozy candle"   # query tự chọn
    python tools/fetch_bg.py --per-query 2 "city night bokeh"       # 2 clip/query

Clip lưu `04_VIDEO/_bg/<id>.mp4`, nguồn ghi `04_VIDEO/_bg/SOURCES.md`
(Pexels: free thương mại, không bắt buộc attribution). Dedup theo id.

⛔ KHÔNG TÁI DÙNG ASSET (user chốt 2026-07-29, rule .claude/rules/media-library.md §2 —
thay chính sách 2026-07-16): mỗi video tải bộ clip MỚI của riêng nó, nhánh "TỪ KHO" đã tắt.
Kho còn 2 vai: ① SỔ ĐEN — clip có `used_in` (đã lên sóng) hoặc nằm trong `_bg/rejected/`
bị cấm tải lại (cùng query Pexels luôn trả clip cũ) ② hồ sơ license.
`rejected/` là lớp port từ chouhen 2026-07-29 (trước đó kr KHÔNG có → clip đã loại bằng
mắt vẫn quay lại pool _bg).
"""
import argparse
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_media_library"))
import media_lib  # noqa: E402

PROJ = Path(__file__).resolve().parents[1].name  # youtube-kr-romfan

KEY = (Path(__file__).resolve().parents[2] / "youtube-jp-health/tools/.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0"}

# Bộ query mặc định — mood romance Hàn hiện đại, nghe trước khi ngủ
DEFAULT_QUERIES = [
    "rain on window night city",
    "cozy bedroom warm lamp",
    "candle flame warm bokeh",
    "city night lights bokeh",
    "night sky moon clouds timelapse",
    "coffee cup steam window",
    "fairy lights bokeh warm",
    "cherry blossom petals falling",
    "curtain window sunlight morning",
    "fireplace warm cozy",
]


def search(query, per=20):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries", nargs="*", default=None)
    ap.add_argument("--per-query", type=int, default=1, help="số clip tải mỗi query")
    args = ap.parse_args()
    queries = args.queries or DEFAULT_QUERIES

    bg_dir = Path(__file__).resolve().parents[1] / "04_VIDEO" / "_bg"
    bg_dir.mkdir(parents=True, exist_ok=True)
    src_md = bg_dir / "SOURCES.md"
    # sync usage kênh này vào kho (idempotent) rồi mới hỏi kho
    media_lib.ingest_bg(bg_dir, PROJ)
    have = {p.stem for p in bg_dir.glob("*.mp4")}
    have_names = {p.name for p in bg_dir.glob("*.mp4")}
    got = got_lib = 0

    # ⛔ LẤY TỪ KHO ĐÃ TẮT (user chốt 2026-07-29, rule media-library.md §2:
    # "làm video nào tải clip của video đó thôi").
    # + PORT LỚP `rejected/` TỪ CHOUHEN (bug chouhen vá 2026-07-26, kr chưa có):
    # clip bị loại khi duyệt mắt phải KHÔNG BAO GIỜ quay lại pool _bg.
    rejected_names = {p.name for p in (bg_dir / "rejected").glob("*.mp4")}
    if rejected_names:
        print(f"đã loại trước đây, sẽ không lấy lại: {len(rejected_names)} clip")
    have_names |= rejected_names
    _idx = media_lib.load_index()
    skip_ids = {str(_idx.get(n, {}).get("source_id")) for n in rejected_names}
    skip_ids.discard("None")
    # sổ đen: clip đã LÊN SÓNG ở video khác → cấm tải lại (cùng query Pexels trả clip cũ)
    for _n, _e in _idx.items():
        if _e.get("kind") == "clip" and _e.get("used_in") and _e.get("source_id"):
            skip_ids.add(str(_e["source_id"]))
    print(f"sổ đen chống lặp: {len(skip_ids)} id đã dùng/đã loại")

    for q in queries:
        need = args.per_query
        print(f"=== Pexels: {q} ===")
        try:
            data = search(q)
        except Exception as e:
            print("  lỗi:", e)
            continue
        cands = []
        for v in data.get("videos", []):
            dur = v.get("duration", 0)
            if dur < 8 or dur > 90:
                continue
            pf = pick_file(v)
            if pf and str(v["id"]) not in have and str(v["id"]) not in skip_ids:
                cands.append((v["id"], dur, pf, v.get("user", {}).get("name", "")))
        cands.sort(key=lambda c: c[2][0], reverse=True)
        for cid, dur, pf, author in cands[:need]:
            dest = bg_dir / f"{cid}.mp4"
            print(f"  tải id={cid} {pf[2]}x{pf[3]} {dur}s by {author} ...")
            try:
                req = urllib.request.Request(pf[1], headers=UA)
                with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as fo:
                    fo.write(r.read())
            except Exception as e:
                print("  lỗi tải:", e)
                continue
            media_lib.add_file(dest, "clip", source="pexels", source_id=cid,
                               url=f"https://www.pexels.com/video/{cid}/",
                               query=q, width=pf[2], height=pf[3],
                               duration=dur, name=dest.name)
            have.add(str(cid))
            have_names.add(dest.name)
            got += 1
            with open(src_md, "a", encoding="utf-8") as f:
                f.write(f"- `{cid}.mp4` — Pexels video {cid} by {author}, query \"{q}\" "
                        f"(Pexels License: free commercial, no attribution required)\n")
            print(f"  OK {dest.name} ({dest.stat().st_size // 1024} KB) — đã nhập kho")
    print(f"\nXong: {got} clip tải mới (kho KHÔNG cấp asset nữa — rule §2), "
          f"tổng {len(list(bg_dir.glob('*.mp4')))} clip trong _bg")


if __name__ == "__main__":
    main()
