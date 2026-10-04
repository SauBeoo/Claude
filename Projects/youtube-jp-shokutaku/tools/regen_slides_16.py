# -*- coding: utf-8 -*-
r"""Prompt GEN LAI cho cac slide bi sai/yeu o vong 1 (video 16).

    python tools\regen_slides_16.py

Xuat:
  06_VIDEO/16_banana-yoru-toire/regen_FLOW.txt     (1 prompt / 1 DONG -> bom extension)
  06_VIDEO/16_banana-yoru-toire/regen_BLOCKS.md    (ban nguoi doc + ly do loai)

Giu nguyen van phap STORYBOARD cua vong 1 (SHOT/SUBJECT/SETTING/LIGHT/LENS/STYLE/NEG)
va giu nguyen STYLE + NEG hang so -> anh moi lap vao 94 anh cu khong lech tong.
"""
import io
import sys
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "06_VIDEO" / "16_banana-yoru-toire"

_s = importlib.util.spec_from_file_location("b", ROOT / "tools" / "build_slides_16.py")
B = importlib.util.module_from_spec(_s)
_s.loader.exec_module(B)   # module nay da tu boc sys.stdout thanh utf-8 -> KHONG boc lai
                           # (boc lan hai lam wrapper cu bi thu gom -> dong luon buffer)

# VONG 2 da DUYET va nap: 47 · 53 · 59 · 76  (xem tools/ingest_regen_16.py ACCEPT)
# Con lai vong 3:
# slide -> (ly do loai, SHOT, SUBJECT, SETTING, LIGHT, shot_code)
REGEN = {
    1: ("🔴🔴 VONG 2 TE HON VONG 1. Tao viet 'a single deep red-purple indented RING' "
        "-> model ve dung mot VET TRON mau tim nhu vet bam / ton thuong da, khong phai "
        "vet han tat. O kenh y te thi mot dom tim tron con doc ra 'benh ngoai da'. "
        "GOC LOI LA CHU 'ring': vet tat la mot DUONG NGANG chay VONG QUANH bap chan, "
        "khong phai mot hinh tron. Vong 3 doi han cach ta + phu dinh tuong minh.",
        "the calf fills the frame from the top edge to the bottom edge, the horizontal "
        "line running straight across the middle of the frame and out of both the left "
        "and the right edge",
        "an elderly bare lower leg, the sock pushed right down onto the foot, and one "
        "single horizontal crease line pressed into the skin all the way around the leg "
        "exactly where the sock elastic sat, the crease pale pink and slightly sunken "
        "like a fold, the skin just above it puffier and rounder than the skin below it, "
        "ordinary healthy skin everywhere else",
        "on a tatami floor beside a low chair in the evening",
        "one warm floor lamp low from the left raking almost along the skin so the "
        "crease throws its own thin shadow", "ECU",
        "no bruise, no purple patch, no round mark, no circle, no rash, no wound, "
        "no redness spot, no skin disease"),

    32: ("🟡 Vong 2 het sieu thuc (tot) nhung PHEP SO SANH KHONG DOC DUOC: chai nuoc nam "
         "o tien canh trai, ban chan o tan phia phai xa — hai vat khac co, khac khoang "
         "cach, mat khong noi duoc chung lai. Vong 3 keo hai vat ve SAT NHAU, chup sat "
         "san de chung cung mot co.",
         "camera resting on the floor, the two bottles at the left and the bare feet "
         "immediately beside them at the right, all four objects touching the bottom "
         "edge and at the same distance from the camera",
         "two full clear plastic water bottles standing upright on the floor right "
         "beside a pair of bare elderly feet, close enough to touch, the bottles and "
         "the ankles the same size in frame so the amount of water reads at a glance",
         "on a wooden floor in a Japanese living room in the evening",
         "one warm floor lamp from the right, the bottles and the feet sharing the same "
         "pool of light and the same shadow direction", "LOW",
         "no bottle far away, no wide room, no furniture between them"),
}


def main():
    flow, blocks = [], []
    for i in sorted(REGEN):
        why, frame, subj, setting, light, code, extra_neg = REGEN[i]
        bl = B.build_blocks(code, frame, subj, setting, light)
        # noi phu dinh RIENG cua shot vao cuoi khoi NEG (giu nguyen NEG hang so)
        bl = [(k, v + ", " + extra_neg if k == "NEG" and extra_neg else v) for k, v in bl]
        p = " ".join(f"{k}: {v}." for k, v in bl)
        flow.append(p)
        idx = B.PLAN[i][0]
        cue = B.body_lines()[idx]
        blocks.append(
            f"### slide_{i:02d}.jpg — {code} — GEN LAI\n\n"
            f"- cue: `{cue}`\n- **vi sao loai:** {why}\n- **{len(p)} ky**\n\n```\n"
            + "\n".join(f"{k:<8}: {v}" for k, v in bl if k not in ("STYLE", "NEG"))
            + "\n```\n")

    VD.mkdir(parents=True, exist_ok=True)
    (VD / "regen3_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "regen3_TENFILE.txt").write_text(
        "\n".join(f"dong {n+1} -> slide_{i:02d}.jpg" for n, i in enumerate(sorted(REGEN))) + "\n",
        encoding="utf-8")
    (VD / "regen3_BLOCKS.md").write_text(
        f"# Video 16 — GEN LAI {len(REGEN)} slide (vong 2)\n\n"
        "> Van phap va STYLE/NEG **giong het vong 1** -> anh moi lap vao 94 anh cu khong lech tong.\n"
        f"> STYLE: `{B.STYLE}`\n>\n> NEG: `{B.NEG}`\n\n"
        "> Gen xong: doi ten dung `slide_NN.jpg`, bo vao `_slides_orig/`, chay lai\n"
        "> `python tools\\ingest_slides_16.py` de cat watermark + resize 1920x1080.\n\n"
        + "\n".join(blocks), encoding="utf-8")

    print(f"OK  {len(REGEN)} prompt gen lai: " + " ".join(f"slide_{i:02d}" for i in sorted(REGEN)))
    print(f"    do dai: {min(len(p) for p in flow)}-{max(len(p) for p in flow)} ky")
    for f in ("regen3_FLOW.txt", "regen3_TENFILE.txt", "regen3_BLOCKS.md"):
        print(f"    -> {(VD / f).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
