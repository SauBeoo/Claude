# -*- coding: utf-8 -*-
r"""redo_flow21.py — loc RIENG lo prompt can GEN LAI cua video 21.

🔴 VI SAO CAN FILE RIENG (2026-09-04): 11/84 shot dung bang trang co viet chu,
   va Veo **khong viet duoc chu Nhat/so co nghia** — frame 10800 cua ban render
   thu ra 「50 ≒ 50 0 ハ」 loang ngoang chiem ~1/4 khung (`media-library.md` §2.9).
   User chot: *"nen thi trang oke"* => mat bang de TRONG, hanh dong chuyen sang
   ve KY HIEU (vong tron / mui tui / gach ngang / dau + =), van tai duoc an du
   so hoc ma khong can chu.
   ⇒ Gen lai ca 84 clip la vo ly; tron 11 prompt moi vao `flow21_T2V.txt` thi
   user phai tu do dong nao la dong nao. File rieng thi bom thang vao extension.

📛 **TEN FILE DICH GIU NGUYEN** (`a21_<key>.mp4`) => tha clip moi vao cung folder
   nguon roi chay lai `ingest_clips_21.py`: no so **mtime** nen tu ghi de dung
   11 cho, 73 clip con lai bo qua (`render-background.md` §2.5).

CHAY:  python tools/redo_flow21.py board          # 11 shot dung P_BOARD
       python tools/redo_flow21.py k1,k2,k3       # chi dinh key
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes21 import SCENES  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VD = os.path.join(PROJ, "06_VIDEO", "21_fuyo-shinkokusho-205man")


def main():
    if len(sys.argv) < 2:
        print(__doc__.split("CHAY:")[1])
        return 1
    arg = sys.argv[1]
    if arg == "board":
        keys = [sh["key"] for s in SCENES for sh in s.get("shots", [])
                if "P_BOARD" in sh.get("props", [])]
    else:
        keys = arg.split(",")

    # thu tu shot = thu tu dong trong flow21_T2V.txt / TENFILE
    order = [sh["key"] for s in SCENES for sh in s.get("shots", [])]
    t2v = [x.rstrip("\n") for x in
           io.open(os.path.join(VD, "flow21_T2V.txt"), encoding="utf-8")
           if x.strip()]
    if len(t2v) != len(order):
        print(f"🔴 flow21_T2V.txt co {len(t2v)} dong nhung SCENES co {len(order)} "
              f"shot — chay lai `gen_flow21.py` truoc")
        return 1

    rows, out = [], []
    for k in keys:
        if k not in order:
            print(f"🔴 key khong co trong SCENES: {k}")
            return 1
        i = order.index(k)
        out.append(t2v[i])
        rows.append((i + 1, f"a21_{k}.mp4", k))

    io.open(os.path.join(VD, "flow21_REDO.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(out) + "\n")
    io.open(os.path.join(VD, "flow21_REDO_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write(
        "thu_tu_bom\tdong_goc\tclip (GIU NGUYEN TEN)\tkey\n"
        + "\n".join(f"{j}\t{n:03d}\t{fn}\t{k}"
                    for j, (n, fn, k) in enumerate(rows, 1)) + "\n")

    print(f"→ {VD}")
    print(f"   flow21_REDO.txt          {len(out)} prompt CAN GEN LAI "
          f"({min(len(x) for x in out)}–{max(len(x) for x in out)} ky)")
    print(f"   flow21_REDO_TENFILE.txt  ten file dich GIU NGUYEN\n")
    for j, (n, fn, k) in enumerate(rows, 1):
        print(f"   bom thu {j:2d}  ->  {fn:34s} (dong goc {n:03d})")
    print(f"\n   Sau khi gen: tha 11 file vao F:\\Youtube\\nenkin_21_k95bsyz2 "
          f"dat ten task_<dong_goc>_1_1080p.mp4 (ghi de ban cu), roi chay lai\n"
          f"   `python tools/ingest_clips_21.py` — no so mtime nen chi xu ly 11 cho.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
