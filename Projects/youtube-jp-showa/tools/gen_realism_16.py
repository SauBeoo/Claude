# -*- coding: utf-8 -*-
"""
gen_realism_16 — 8 cảnh AI của video 16 theo CÔNG THỨC REALISM (user chốt 2026-09-22: "áp cho cả showa,
nhưng showa vẫn phải theo chủ đề showa").

GIỮ của showa: bối cảnh 昭和 thật (SC) · dàn cast có khuôn mặt (CA) · vật màu (PROPS) · chữ ký biểu cảm
(EXPR_BANK + sổ EXPR_REGISTRY) · chỗ máy đứng (STAND) — tất cả import từ gen_demo16_kioku, KHÔNG chép.
ĐỔI (khối chung `Projects/_media_library/realism_blocks.py`): ảnh Nano Banana làm khung đầu → Animate ·
máy KHOÁ (2/3) hoặc TRÔI một bước (1/3) thay 8 nước dolly · người cử động chậm · nắng vàng một nguồn ·
prompt 1,3–2,1k ký thay 3–4k.

⚠️ Đây là lớp L3 (AI lấp) của REAL-FIRST v2 — L1 phim thật/L2 ảnh thật của kênh giữ nguyên (CLAUDE.md §Visual).

Chạy:  python tools/gen_realism_16.py
Xuất:  06_VIDEO/16_omiai-kekkon/realism16_STILL_FLOW.txt · realism16_MOTION_FLOW.txt · realism16_T2V_FLOW.txt
       · realism16_TENFILE.txt
"""
import io, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "_media_library"))

from realism_blocks import build_pair, gate_prompt, LIMIT_SHOWA
import gen_demo16_kioku as K            # SC · CA · PROPS · PROP_TAIL · STAND · SHOTS · EXPR · pick_expr

OUT = K.OUT
VIDEO_ID = K.VIDEO_ID

# thế giới của showa = bối cảnh thật + vật màu (camera-language §5.1) — đặt vào ảnh khung đầu
def world_of(scene):
    return ("Setting: " + K.SC[scene].rstrip(",") + ". Bright colour only in the props: " + K.PROPS[scene]
            + K.PROP_TAIL + ". Real Japan of the early nineteen-seventies exactly as it was — a classical, ordinary, documentary "
            "world: no fantasy element, no futuristic or impossible architecture, no modern object anywhere.")

LIGHT_OF = {"office": "interior", "rouka": "interior", "yakusho": "interior", "chanoma": "night",
            "zashiki": "dusk", "densha": "day", "genkan": "day"}
HEIGHT_OF = {"table": "the height of the tabletop, seated", "seated": "seated eye height on the floor",
             "eye_st": "standing eye height", None: "standing eye height"}
# 1/3 trôi: hai cảnh chuyển/thở (tàu, tiễn ở cổng); cảnh cảm xúc thì khoá
DRIFT = {"s7_subj_densha", "s8_subj_wave"}


def freeze(action):
    """Khung đầu = nhịp 1: mệnh đề đầu của hành động."""
    c = action.split(";")[0].strip().rstrip(".,")
    return c[0].upper() + c[1:] + "."


def convert(sh, pick):
    (name, scene, size, angle, height, stand, move, land, expr, action, extras, _why) = sh
    for cast, lv in expr:
        action = action.replace("{EX:%s}" % cast, K.expr_text(cast, pick) + K.LEVEL[lv])
    for k, v in K.CA.items():
        action = action.replace("{%s}" % k, v)
    # POV cũ (s8: tay người xem vẫy) → góc thứ ba: bỏ mệnh đề về "the viewer's own hand"
    action = action.replace("the viewer's own one hand comes up at the edge of the frame and waves back once, "
                            "and at that ", "")
    return dict(
        id=name, light=LIGHT_OF[scene], cam="drift" if name in DRIFT else "locked",
        where=K.STAND[stand], height=HEIGHT_OF[height],
        still=K.SC[scene].rstrip(",") + ". " + freeze(action),
        act=action, alive="",
    ), scene


def main():
    pick, reg = K.pick_expr(VIDEO_ID)
    out = {"still": [], "motion": [], "t2v": []}
    rows, fails = [], 0
    for sh in K.SHOTS:
        sc, scene = convert(sh, pick)
        st, mo, tv = build_pair(sc, world_of(scene))
        for k, p in (("still", st), ("motion", mo), ("t2v", tv)):
            out[k].append(p)
            for e in gate_prompt(k, p, LIMIT_SHOWA):
                fails += 1
                print(f"  🔴 {sc['id']} [{k}]: {e}")
        # gate riêng của showa: hai cast cùng khung phải khác chữ ký (camera-language §6.7)
        sigs = [pick[c] for c, _ in sh[8]]
        if len(set(sigs)) != len(sigs):
            fails += 1; print(f"  🔴 {sc['id']}: hai cast cung mot chu ky")
        rows.append((sc["id"], sc["cam"], sc["light"], scene, len(st), len(mo)))
    OUT.mkdir(parents=True, exist_ok=True)
    for k, fn in (("still", "realism16_STILL_FLOW.txt"), ("motion", "realism16_MOTION_FLOW.txt"),
                  ("t2v", "realism16_T2V_FLOW.txt")):
        with io.open(OUT / fn, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(out[k]) + "\n")
    with io.open(OUT / "realism16_TENFILE.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# video 16 — 8 canh AI theo CONG THUC REALISM (khoi chung _media_library/realism_blocks.py)\n"
                 "# STILL -> Image (Nano Banana 2) -> chon anh -> Animate -> MOTION. T2V = duong lui.\n"
                 "# Chon anh: dung boi canh 昭和? cast dung khuon mat? nguoi o NHIP 1? khong chu bia?\n"
                 "# CHU KY RUT: " + ", ".join(c + "=" + pick[c] for c in sorted(pick)) + "\n#\n")
        for i, r in enumerate(rows, 1):
            fh.write(f"{i}\tdemo16_{r[0]}_i2v.mp4\t{r[1]}\t{r[2]}\t{r[3]}\tstill {r[4]} · motion {r[5]}\n")
    reg[VIDEO_ID] = pick
    K.REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"video 16 REALISM — {len(rows)} canh · may: khoa {sum(r[1]=='locked' for r in rows)} / troi {sum(r[1]=='drift' for r in rows)}")
    for k in out:
        L = [len(p) for p in out[k]]
        print(f"  {k:6s}: {min(L)}–{max(L)} ky, TB {sum(L)//len(L)}")
    print("GATE: " + ("✅ SACH" if not fails else f"🔴 {fails} loi"))
    print(f"-> {OUT}/realism16_*_FLOW.txt")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
