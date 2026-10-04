# -*- coding: utf-8 -*-
r"""ingest_art27.py — ghép 125 ảnh đã gen vào đúng 86 ô của video 27.

VÌ SAO CẦN TOOL: generator đặt tên file theo NỘI DUNG ảnh
(`Checklist_board_filled_with_print_2026...jpeg`), không theo số ô. Phải ghép bằng độ trùng
từ khoá giữa tên file và mô tả `SUBJ[k]` trong `img27_prompts.py`.

🔴 BẪY ĐÃ GHI Ở `media-library.md` §2.10 ⑨ mục ④: token-overlap ghép SAI khi hai ô cùng vài
từ chung. Ở đó là giới tính; ở đây là vật (nhiều ô cùng có "envelope"/"checklist"). ⇒ ghép
theo điểm trùng nhưng **mỗi ảnh chỉ dùng MỘT LẦN** (cấm trùng ảnh trong cùng video —
`feedback_slide_khong_trung_anh_trong_video`), và in bảng để soi mắt.

Ưu tiên kho: ô có giấy tờ (PRINT) lấy từ `art2/` (lô gen lại CÓ chữ texture); ô khác lấy
`art1/`; 7 ô đã chốt lấy `art/`.

CHẠY:  python tools/ingest_art27.py          → art_final/shot_000.png …
       python tools/ingest_art27.py --check  → chỉ in bảng ghép, không copy
"""
import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "27_nenkin-tsuchisho-nai-okane-5tsu"
VD = PROJ / "06_VIDEO" / STEM
OUT = VD / "art_final"

sys.path.insert(0, str(PROJ / "tools"))
src = (PROJ / "tools" / "img27_prompts.py").read_text(encoding="utf-8")
# 🔴 BỎ dòng gán sys.stdout của module kia trước khi exec: nó tạo TextIOWrapper mới, wrapper
# CŨ bị thu hồi và ĐÓNG LUÔN buffer ⇒ mọi print sau đó ném "I/O operation on closed file".
NL = chr(10)
head = NL.join(l for l in src.split("def main")[0].split(NL)
               if not l.startswith("sys.stdout"))
ns: dict = {}
exec(compile(head.replace("__file__", repr(str(PROJ / "tools" / "x.py"))), "img27", "exec"), ns)
SUBJ, HAVE, PRINT = ns["SUBJ"], ns["HAVE"], ns["PRINT"]

STOP = {"a", "an", "the", "of", "with", "and", "in", "on", "at", "to", "one", "two", "small",
        "large", "from", "its", "his", "her", "beside", "into", "for", "by", "it", "is"}


def toks(s: str) -> set:
    return {w for w in re.split(r"[^a-z]+", s.lower()) if w and w not in STOP and len(w) > 2}


def main() -> int:
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    pools = {"art": sorted((VD / "art").iterdir()),
             "art1": sorted((VD / "art1").iterdir()),
             "art2": sorted((VD / "art2").iterdir())}
    used, rows = set(), []
    for s in plan["shots"]:
        k = s["k"]
        if k in HAVE:
            src_p = next((p for p in pools["art"] if HAVE[k][:26] in p.name), None)
            rows.append((k, "art", src_p, 99))
            if src_p:
                used.add(src_p)
            continue
        want = toks(SUBJ[k])
        # ô giấy tờ ⇒ ưu tiên kho gen lại; hết thì mới lùi về kho cũ
        order = ["art2", "art1"] if k in PRINT else ["art1", "art2"]
        best, best_sc, best_pool = None, -1, ""
        for pool in order:
            for p in pools[pool]:
                if p in used:
                    continue
                sc = len(want & toks(p.stem))
                if sc > best_sc:
                    best, best_sc, best_pool = p, sc, pool
            if best_sc >= 3:      # đủ chắc thì không cần lùi kho
                break
        if best:
            used.add(best)
        rows.append((k, best_pool, best, best_sc))

    weak = [r for r in rows if r[3] < 2]
    print(f"{len(rows)} ô · ghép được {sum(1 for r in rows if r[2])} · "
          f"điểm trùng yếu (<2): {len(weak)} ô")
    for k, pool, p, sc in rows:
        if sc < 2:
            print(f"  ⚠️ ô {k:>3} điểm {sc} ← {pool}/{p.name[:44] if p else 'KHÔNG CÓ'}")
    if "--check" in sys.argv:
        for k, pool, p, sc in rows:
            print(f"  ô {k:>3} [{sc:>2}] {pool:<5} {p.name[:56] if p else '—'}")
        return 0

    OUT.mkdir(exist_ok=True)
    for k, pool, p, sc in rows:
        if not p:
            print(f"🔴 ô {k} KHÔNG có ảnh")
            continue
        shutil.copy(p, OUT / f"shot_{k:03d}.png")
    print(f"\n→ {len(list(OUT.iterdir()))} ảnh trong {OUT}")
    dup = len(rows) - len({r[2] for r in rows if r[2]})
    print(f"   ảnh bị dùng lại: {dup} (phải = 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
