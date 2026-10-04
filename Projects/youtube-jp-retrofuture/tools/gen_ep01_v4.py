# -*- coding: utf-8 -*-
"""
TẬP 01 — CÔNG THỨC v4 "REALISM" (user chốt 2026-09-22 tối sau 3 vòng thử, `_realism/`).

Thay `gen_ep01_ichinichi.py` (POV · máy cầm tay · prompt 13,8k ký). Kịch bản 34 cảnh GIỮ NGUYÊN — import SCENES
từ đó; chỉ đổi CÁCH QUAY: góc thứ ba, máy khoá (2/3) hoặc trôi một bước (1/3), ảnh Nano Banana làm khung đầu →
Animate, nắng vàng ban ngày, người cử động chậm. Khối dùng chung: `Projects/_media_library/realism_blocks.py`.

Chạy:  python tools/gen_ep01_v4.py
Xuất:  06_VIDEO/01_tou-no-fumoto/v4_STILL_FLOW.txt   34 prompt ảnh  (bơm extension, chế độ Image)
       06_VIDEO/01_tou-no-fumoto/v4_MOTION_FLOW.txt  34 prompt động (dán tay sau Animate)
       06_VIDEO/01_tou-no-fumoto/v4_T2V_FLOW.txt     34 prompt t2v (đường lui khi hết ảnh)
       06_VIDEO/01_tou-no-fumoto/v4_TENFILE.txt
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "_media_library"))

from realism_blocks import build_pair, gate_prompt
from blocks_s100 import WORLD_SHORT
from gen_ep01_ichinichi import SCENES as SCENES_B          # kịch bản bản Ⓑ, giữ nguyên

# sky/light của bản Ⓑ → khoá ánh sáng v4
LIGHT_MAP = {("dawn", "dawn"): "dawn", ("day", "day"): "day", ("window", "interior"): "interior",
             ("dusk", "dusk"): "dusk", ("dusk", "interior"): "interior",
             ("night", "interior_night"): "night", ("night", "night"): "night"}

# 1/3 cảnh máy TRÔI (tỉ lệ đo ở mẫu: 32%) — chọn cảnh CHUYỂN và cảnh THỞ ngoại, không chọn cảnh cảm xúc
DRIFT_IDS = {"02_hoshimono", "05_kiri", "06_tsuugaku", "10_ichiba", "13_mahiru", "18_rojiura", "19_arcade",
             "21_sentou", "24_kage_gyaku", "26_kaerimichi", "31_yomichi", "33_machi_yoru"}


def first_clause(act):
    """Ảnh khung đầu = cảnh đóng băng ở NHỊP 1: lấy mệnh đề đầu của hành động, đổi sang thì hiện tại 'vừa mới'."""
    c = re.split(r"[;—]| — |\. ", act.strip())[0].rstrip(".,")
    return c[0].upper() + c[1:] + "."


def height_of(you):
    y = you.casefold()
    if "sitting" in y or "kneeling" in y or "seated" in y:
        return "seated eye height"
    return "standing eye height"


def convert(sb):
    light = LIGHT_MAP.get((sb["sky"], sb["light"]))
    if light is None:
        raise SystemExit(f"{sb['id']}: khong map duoc sky={sb['sky']} light={sb['light']}")
    you = sb["you"]
    return dict(
        id=sb["id"], light=light, mega=sb["mega"],
        cam="drift" if sb["id"] in DRIFT_IDS else "locked",
        where="someone " + you, height=height_of(you),
        still=sb["set"] + " " + first_clause(sb["act"]),
        act=sb["act"],
        alive="",     # ALIVE của bản Ⓑ đã nằm trong act (hơi nước, quạt, noren) — không lặp
    )


def main():
    vd = os.path.join(ROOT, "06_VIDEO", "01_tou-no-fumoto")
    out = {"still": [], "motion": [], "t2v": []}
    rows, fails = [], 0
    for sb in SCENES_B:
        sc = convert(sb)
        world = WORLD_SHORT if sc["mega"] else ""
        st, mo, tv = build_pair(sc, world)
        for k, p in (("still", st), ("motion", mo), ("t2v", tv)):
            out[k].append(p)
            for e in gate_prompt(k, p):
                fails += 1
                print(f"  🔴 {sc['id']} [{k}]: {e}")
        rows.append((sc["id"], sc["cam"], sc["light"], "THAP" if sc["mega"] else "-", len(st), len(mo)))
    for k, fn in (("still", "v4_STILL_FLOW.txt"), ("motion", "v4_MOTION_FLOW.txt"), ("t2v", "v4_T2V_FLOW.txt")):
        with io.open(os.path.join(vd, fn), "w", encoding="utf-8") as fh:
            fh.write("\n".join(out[k]) + "\n")
    with io.open(os.path.join(vd, "v4_TENFILE.txt"), "w", encoding="utf-8") as fh:
        fh.write("# TAP 01 v4 REALISM — 34 canh. Dong i cua STILL/MOTION/T2V = canh i.\n"
                 "# STILL -> Image (Nano Banana 2) -> chon anh -> Animate -> MOTION. T2V = duong lui.\n"
                 "# Chon anh: THAP o nua tren (canh ngoai)? nguoi o NHIP 1? khong chu bia?\n#\n")
        for i, r in enumerate(rows, 1):
            fh.write(f"{i:02d}\tep01_{r[0]}_i2v.mp4\t{r[1]}\t{r[2]}\t{r[3]}\tstill {r[4]} · motion {r[5]}\n")
    from collections import Counter
    print(f"TAP 01 v4 — {len(rows)} canh · may: {dict(Counter(r[1] for r in rows))} · anh sang: {dict(Counter(r[2] for r in rows))}")
    for k in out:
        L = [len(p) for p in out[k]]
        print(f"  {k:6s}: {min(L)}–{max(L)} ky, TB {sum(L)//len(L)}")
    print("GATE: " + ("✅ SACH" if not fails else f"🔴 {fails} loi"))
    print(f"-> {vd}/v4_*_FLOW.txt")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
