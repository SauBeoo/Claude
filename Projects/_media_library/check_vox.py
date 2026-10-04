# -*- coding: utf-8 -*-
r"""
check_vox.py — GATE MÁY cho lớp thẻ Vox (dùng chung mọi kênh). Khắc 2026-08-06.

VÌ SAO CÓ GATE NÀY
────────────────────────────────────────────────────────────────────────────────
Luật kiểm bằng mắt thì sẽ trôi — đã trôi thật: `16_tsukemono-shio-no-dan` có **39 thẻ
`title` trên 62 thẻ vox (63%)**, tức 39 khung giống hệt nhau, mà không ai chặn. Đó là
PowerPoint chứ không phải Vox, và còn rơi vào "inauthentic content"
(`youtube-compliance.md` §1: "video giống hệt nhau chỉ khác tiêu đề").
Cùng lúc chỉ **1 thẻ** mang ảnh thật + annotation, còn 58 ảnh full-khung thì KHÔNG có
annotation nào → hai lớp chạy song song, không bao giờ gặp nhau trong một khung.

5 LUẬT CHẶN (FAIL = KHÔNG RENDER) + 2 cảnh báo
────────────────────────────────────────────────────────────────────────────────
  X1  `title` ≤ title_cap (hồ sơ kênh, mặc định 4) VÀ không 2 thẻ `title` liền nhau
  X2  ≥50% thẻ vox mang ẢNH THẬT (`bg:"photo"` có ảnh, `collage`/`compare` có cutout)
  X3  không kind nào lặp >2 lần LIÊN TIẾP (`board` miễn — tích luỹ là bản chất; trần riêng 6)
  X4  mọi toạ độ chữ (pin của `flow`) nằm TRÊN safe_bottom của kênh
  X5  ≥1 thẻ `source` — nối gate `genten` của `handmade-layer.md` §3.2 (co-dai đã bỏ
      `tegami`, nên lớp không-copy-được của kênh là NGUỒN THẬT được trích)
  cảnh báo: số có đơn vị trong `_TTS.md` mà không thẻ chart nào phủ · kind lạ

CHẠY
────────────────────────────────────────────────────────────────────────────────
    python check_vox.py <SLIDES.json> --channel co-dai [--tts <..._TTS.md>]
    exit 0 = PASS · exit 1 = có FAIL

Chạy CÙNG LƯỢT với gate cấu trúc của kênh, ví dụ co-dai:
    python tools\check_coldopen.py 16 && python E:\Claude\Projects\_media_library\check_vox.py ^
        03_SCRIPTS\16_..._SLIDES.json --channel co-dai

⚠️ Gate này KHÔNG kiểm chuỗi `match` (cue) — đó là việc của `check_cues.py`
(`youtube-jp-health/tools`). Sửa lời thoại thì phải chạy CẢ HAI.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_vox as MV                                            # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CHART_KINDS = {"stat", "bar", "line", "dot"}
PHOTO_OK_KINDS = {"collage", "board"}  # kind vốn dựng từ cutout ảnh thật


def has_real_photo(v, idx, img_dir):
    if v.get("bg") == "photo":
        p = Path(v["photo"]) if v.get("photo") else MV.find_slide(img_dir, idx)
        if p and Path(p).exists():
            return True
    if v.get("kind") in PHOTO_OK_KINDS and any(it.get("cut") for it in (v.get("items") or [])):
        return True
    if v.get("kind") == "compare" and any(
            isinstance(v.get(s), dict) and v[s].get("cut") for s in ("left", "right")):
        return True
    return False


def main():
    ap = argparse.ArgumentParser(description="Gate lớp thẻ Vox")
    ap.add_argument("slides")
    ap.add_argument("--channel", required=True)
    ap.add_argument("--tts", help="file _TTS.md để soát số liệu chưa có chart (cảnh báo)")
    ap.add_argument("--img-dir", help="folder ảnh nền (mặc định suy từ hồ sơ kênh)")
    a = ap.parse_args()

    MV.apply_profile(a.channel)
    slides = Path(a.slides)
    cfg = json.loads(slides.read_text(encoding="utf-8"))
    img_dir = Path(a.img_dir) if a.img_dir else \
        slides.parent.parent / MV.CH.get(a.channel)["video_dir"]      # chỉ để dò tương đối
    if a.img_dir is None:
        # SLIDES nằm ở 0N_SCRIPTS, ảnh ở 0N_VIDEO/<slug>/<img_subdir> → dò theo stem
        stem = re.sub(r"_SLIDES.*$", "", slides.stem)
        cand = img_dir / stem / MV.CH.get(a.channel)["img_subdir"]
        img_dir = cand

    vox = [(i, e["vox"]) for i, e in enumerate(cfg) if e.get("vox")]
    if not vox:
        print("… không có entry vox nào → gate bỏ qua")
        return 0

    fails, warns = [], []
    kinds = [v.get("kind", "?") for _, v in vox]

    # ── X1 · thẻ chữ ─────────────────────────────────────────────────────────
    n_title = kinds.count("title")
    if n_title > MV.TITLE_CAP:
        fails.append(f"X1 · {n_title} thẻ 'title' > trần {MV.TITLE_CAP}. Thẻ chữ đang THAY "
                     f"nội dung hình — đổi sang flow/collage/stat/bar (skill video-vox GĐ2). "
                     f"Đây đúng bệnh của video 16 (39/62).")
    for k in range(len(kinds) - 1):
        if kinds[k] == "title" == kinds[k + 1]:
            fails.append(f"X1 · slot {vox[k][0]:02d} và {vox[k+1][0]:02d}: hai thẻ 'title' LIỀN NHAU")
            break

    # ── X2 · tỉ lệ ảnh thật ──────────────────────────────────────────────────
    n_photo = sum(1 for i, v in vox if has_real_photo(v, i, img_dir))
    pct = n_photo / len(vox) * 100
    if pct < 50:
        fails.append(f"X2 · chỉ {n_photo}/{len(vox)} thẻ ({pct:.0f}%) mang ảnh thật < 50%. "
                     f"Chữ ký Vox là ANNOTATE ĐÈ LÊN ảnh, không phải thẻ chữ đứng cạnh ảnh. "
                     f"Thêm \"bg\": \"photo\" cho các beat nói về VẬT.")

    # ── X3 · lặp layout liên tiếp ────────────────────────────────────────────
    # `board` được MIỄN: trang hồ sơ tích luỹ qua nhiều cue liên tiếp là bản chất của
    # kind đó (mỗi cue thêm 1 item bay vào, nội dung KHÔNG lặp — 2026-08-08). Trần mềm
    # riêng: chuỗi board >6 cue thì vẫn nhắc (trang treo quá lâu = người xem no).
    run, start = 1, 0
    for k in range(1, len(kinds) + 1):
        if k < len(kinds) and kinds[k] == kinds[k - 1]:
            run += 1
            continue
        if run > 2 and kinds[start] != "board":
            fails.append(f"X3 · kind '{kinds[start]}' lặp {run} lần LIÊN TIẾP "
                         f"(slot {vox[start][0]:02d}–{vox[k-1][0]:02d}) → xen kind khác")
        if kinds[start] == "board" and run > 6:
            fails.append(f"X3 · chuỗi 'board' dài {run} cue (slot {vox[start][0]:02d}–"
                         f"{vox[k-1][0]:02d}) — trang treo quá lâu, tách thành 2 trang")
        run, start = 1, k

    # ── X4 · chữ trên safe_bottom ────────────────────────────────────────────
    for i, v in vox:
        for pin in (v.get("pins") or []):
            if len(pin) >= 3 and pin[1] > MV.SB - 40:
                fails.append(f"X4 · slot {i:02d} pin '{pin[2]}' ở y={pin[1]} > safe_bottom "
                             f"{MV.SB} → hộp phụ đề sẽ đè mất chữ")
        if v.get("kind") not in MV.KINDS:
            warns.append(f"slot {i:02d}: kind '{v.get('kind')}' không tồn tại")

    # ── X5 · nguồn thật ──────────────────────────────────────────────────────
    if "source" not in kinds:
        fails.append("X5 · không có thẻ 'source' (原典). Lớp không-copy-được của kênh là "
                     "NGUỒN THẬT được trích (cơ quan + 年月 + số) — handmade-layer.md §3.2. "
                     "Không có thì ghi 'HANDMADE: hoãn — <lý do> — <ngày>' vào Đóng gói CTR.")

    # ── cảnh báo · số chưa có chart ───────────────────────────────────────────
    if a.tts and Path(a.tts).exists():
        txt = Path(a.tts).read_text(encoding="utf-8", errors="replace")
        nums = set(re.findall(r"([0-9]{1,3}(?:,[0-9]{3})*|[0-9]+(?:\.[0-9]+)?)\s*"
                              r"(?:人|％|%|円|度|℃|年|割|倍|グラム|ｇ|g|キロ|時間|日|件)", txt))
        blob = json.dumps([v for _, v in vox], ensure_ascii=False)
        miss = [n for n in nums if n not in blob and len(n) >= 2][:8]
        if miss and not any(k in CHART_KINDS for k in kinds):
            warns.append(f"TTS có số liệu ({', '.join(sorted(miss)[:6])}…) mà KHÔNG thẻ chart nào "
                         f"— mỗi con số đắt nên có 1 thẻ stat/bar/line/dot")
        elif miss:
            warns.append(f"số trong TTS chưa lên hình: {', '.join(sorted(miss)[:6])}")

    # ── kết ───────────────────────────────────────────────────────────────────
    from collections import Counter
    print(f"\n{len(vox)} thẻ vox · ảnh thật {n_photo} ({pct:.0f}%) · phân bố kind:")
    for k, c in Counter(kinds).most_common():
        print(f"    {k:9s} {c}")
    for w in warns:
        print(f"  ⚠ {w}")
    if fails:
        print()
        for f in fails:
            print(f"🔴 GATE VOX {f}")
        print(f"\n❌ FAIL {len(fails)} luật → KHÔNG render.")
        return 1
    print("\n✅ PASS X1–X5.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
