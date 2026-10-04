# -*- coding: utf-8 -*-
r"""timeline_to_srt.py — `timeline.json` → `subs.srt` (khối ≤78 ký, cắt sau dấu câu).

VÌ SAO: đường Remotion không sinh srt (pipeline ffmpeg cũ có). srt cần cho 2 việc:
① `cta_inject.py --srt` tìm timestamp câu CTA 「ここで、ひとつだけお願いです」
② upload tay lên YouTube (`youtube-upload-seo.md` §1.2 — cấm auto-caption).
Dùng CHUNG `split_caption()` của builder để srt khớp y phụ đề cháy trong video.

CHẠY:  python tools/timeline_to_srt.py <stem>   # → 06_VIDEO/<stem>/subs.srt
"""
import importlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    if len(sys.argv) < 2:
        print("dùng: python tools/timeline_to_srt.py <stem>")
        return 1
    stem = sys.argv[1]
    num = stem.split("_")[0]
    # 🔴 VÁ 2026-09-20: tool hard-code builder Remotion, nhưng khuôn từ v27 dựng bằng
    # `build{num}.py` (ffmpeg thuần) — import thẳng là ModuleNotFoundError.
    # Thử lần lượt, và nếu builder KHÔNG có `split_caption` thì dùng bản nội bộ dưới đây.
    b = None
    for mod in (f"build_remotion_{num}", f"build{num}"):
        try:
            b = importlib.import_module(mod)
            break
        except ModuleNotFoundError:
            continue
    if b is None or not hasattr(b, "split_caption"):
        # ⚠️ CỐ Ý KHÔNG dùng logic wrap của build27: nó cắt cụt và VỨT chữ dư
        # (12 dòng của v27 mất đuôi, 3 dòng mất cả con số tiền).
        # srt là chỗ DUY NHẤT còn giữ đủ lời, nên ở đây chia mà không bao giờ bỏ ký tự nào.
        import re as _re

        def _split(txt, lim=78):
            txt = txt.strip()
            if len(txt) <= lim:
                return [txt]
            parts, cur = [], ""
            for seg in _re.split(r"(?<=[、。])", txt):
                if not seg:
                    continue
                if len(cur) + len(seg) <= lim:
                    cur += seg
                else:
                    if cur:
                        parts.append(cur)
                    while len(seg) > lim:      # đoạn dài hơn trần mà không có dấu câu
                        parts.append(seg[:lim])
                        seg = seg[lim:]
                    cur = seg
            if cur:
                parts.append(cur)
            return parts

        class _B:
            split_caption = staticmethod(_split)
        b = _B()
    vd = PROJ / "06_VIDEO" / stem
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    # 🔴🔴 BAN CU GOI `b.split_caption(l)` voi `l` la DICT, trong khi ham nhan STRING.
    #    `len(dict)` = so KHOA (~4) <= 78 nen ham tra ve `[dict]` — tuc **KHONG BAO GIO
    #    che khoi**, ma van chay tron tru va van xuat ra mot file srt hop le.
    #    Hau qua: srt 101 khoi, khoi dai nhat 162 ky, trong khi phu de CHAY trong video la
    #    105 khoi <=78 ky => file upload len YouTube **khong khop cai nguoi xem thay**, va
    #    vi pham tran 2 dong/khoi cua `audience-45plus.md` §3.
    #    Bat duoc 2026-09-17 o video 26; video 25 nhieu kha nang cung dinh.
    # ⇒ Chia gio theo TI LE KY TU, y het khoi `cap` cua `build_remotion_*.py`.
    out, i = [], 1
    for l in tl["lines"]:
        parts = b.split_caption(l["text"])
        span = (l["end"] - l["start"]) / max(1, sum(len(x) for x in parts))
        t = l["start"]
        for x in parts:
            d = span * len(x)
            out.append(f"{i}\n{ts(t)} --> {ts(t + d)}\n{x}\n")
            t += d
            i += 1
    (vd / "subs.srt").write_text("\n".join(out), encoding="utf-8")
    print(f"✓ {vd / 'subs.srt'} · {i-1} khối · {tl['total']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
