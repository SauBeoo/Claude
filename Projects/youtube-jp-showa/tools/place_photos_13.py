# -*- coding: utf-8 -*-
"""Video 13: dat 3 clip ANH TU LIEU THAT (da hoa dong) vao clips/clip_NN.mp4.

Chay SAU crop_place_13.py (tool do da bo qua 3 slot nay, xem PHOTO_SLOTS).

Anh that tim duoc 2026-09-14 sau khi user hoi "co anh cu va video cu nao hop script khong":
  slot   5  Kimono children in Ishinomaki   — Yasuhiko Ito, CC BY 2.0  (Wikimedia Commons)
  slot   8  Hosokawa family 1957            — Yasuhiko Ito, CC BY 2.0  (Wikimedia Commons)
  slot 154  People in Japan 1960s           — vo danh, CC0 1.0         (Internet Archive)

🔴 CC BY 2.0 = BAT BUOC ghi cong. Tool tu viet vao ATTRIBUTIONS.md; dong credit
   phai duoc dan sang 概要欄 luc upload, khong duoc bo.

⚠️ Anh CC0 o slot 154 do mot nguoi AN DANH tu khai — cung loai bay da ghi trong
   FOOTAGE_GO_NO_GO.md (NARA khai CC0 cho phim ma chu that la ABC News). Slide nghiep du
   vo danh thi rui ro thuc te thap, nhung khong phai bang khong.
"""
import io, os, json, sys, subprocess, shutil
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = Path(__file__).resolve().parent.parent / "06_VIDEO" / "13_kosodate-joushiki"
PH = VD / "photos_real"
DST = VD / "clips"
# 🔴 BO slot 5 + 8 (2026-09-14, user chot): ca hai LO MAT NGUOI THAT ro net.
#    CC BY phu BAN QUYEN, khong phu QUYEN NHAN THAN — kenh dang kiem tien.
#    Giu slot 154: me dat con di, QUAY LUNG lai may, khong nhan dien duoc ai.
MAP = {154: "anim_154_child_walk.mp4"}


def _dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except Exception:
        return 0.0


ok = 0
for slot, name in sorted(MAP.items()):
    src = PH / name
    if not src.exists():
        print("[CHAN] thieu clip hoa dong:", name)
        sys.exit(1)
    d = _dur(src)
    if d < 7.5:
        print("[CHAN] %s chi dai %.2fs (can >= 7.5s, neu ngan hon khe thi renderer LAP clip)" % (name, d))
        sys.exit(1)
    dst = DST / ("clip_%02d.mp4" % slot)
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    print("  slot %3d  <- %-28s %.2fs" % (slot, name, d))
    ok += 1

# --- credit (CC BY bat buoc) ---
meta = [m for m in json.loads((PH / "_meta.json").read_text(encoding="utf-8"))
        if m["slot"] in MAP]
att = VD / "ATTRIBUTIONS.md"
old = att.read_text(encoding="utf-8") if att.exists() else "# ATTRIBUTIONS — video 13\n"
block = ["\n## Anh tu lieu that (chen 2026-09-14)\n"]
for m in meta:
    block.append("- **slot %s** — %s / %s / %s — %s\n  %s\n"
                 % (m["slot"], m["title"], m["artist"], m["license"], m["source"], m["url"]))
if "Anh tu lieu that" not in old:
    att.write_text(old + "".join(block), encoding="utf-8")
    print("\nda ghi credit vao", att.name)
else:
    print("\ncredit da co trong", att.name)

print("\nDAT XONG %d/3 slot anh that" % ok)
print("ⓘ Slot 154 la CC0 — khong bat buoc ghi cong, nhung ATTRIBUTIONS.md van luu nguon.")
sys.exit(0 if ok == len(MAP) else 1)
