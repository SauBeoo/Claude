# -*- coding: utf-8 -*-
r"""Gom + chuan hoa 82 clip video cho video 28 (dannetsu-tenjo-alumi).

VI SAO CAN FILE NAY: clip nam o 4 thu muc, va CA BON deu danh so lai tu task_001.
Ghep tay chac chan lan. Bang duoi la HOP DONG duy nhat.

    python tools\ingest_clips28.py            # chay that
    python tools\ingest_clips28.py --dry      # chi in ke hoach

Chuan hoa: 1920x1080 (lo 1 la 720p -> upscale lanczos) - 30fps - BO AUDIO.
"""
import argparse
import io
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

L1 = Path(r"F:\Youtube\Dự_án_mới_4_z6pfl0t6")      # 32 clip, 720p
L2 = Path(r"F:\Youtube\codai_atjpxebb")            # 61 = 11 FIX + 50 lo 2, 1080p
L3 = Path(r"F:\Youtube\codai28_979il7fb")          # 5 FIX2, 1080p
L4 = Path(r"F:\Youtube\Dự_án_mới_5_6l87rza2")      # 1 FIX3, 1080p
DST = Path(r"E:\Claude\Projects\youtube-jp-co-dai\06_VIDEO\28_dannetsu-tenjo-alumi\clips")

# ── LO 1: 32 ten dich theo video_prompts_TENFILE.txt ────────────────────────
L1_NAMES = [
    "v_A1_fan-curtain-still", "v_A2_hand-touch-ceiling", "v_A3_iron-cloth-steam",
    "v_A4_window-black-night", "v_B1_sun-on-tatami", "v_B2_open-hatch-dust",
    "v_B3_attic-shimmer", "v_B4_attic-thermometer", "v_B5_roof-tiles-heat",
    "v_B6_hot-water-bottle", "v_C1_campfire-radiant", "v_C2_feather-no-air",
    "v_C3_remote-24", "v_C4_wall-thermometer", "v_C5_ceiling-pushin",
    "v_D1_foil-macro", "v_D2_black-paper", "v_D3_foil-on-glass-WRONG",
    "v_D4_wired-glass", "v_D5_glass-crack", "v_D6_foil-air-gap",
    "v_E1_thatch-exterior", "v_E2_thatch-stems-macro", "v_E3_thatch-interior",
    "v_E4_earth-wall-sun", "v_E5_earth-wall-interior", "v_E6_doma-cool",
    "v_F1_eave-vent", "v_F2_new-windows", "v_F3_tape-hatch-edge",
    "v_F4_foil-on-panel", "v_F5_closet-closing",
]
# LO 1 co 11 clip bi thay boi L2 task_001..011 (video_prompts_FIX_TENFILE.txt)
L1_REPLACED = {6: 1, 7: 2, 8: 3, 15: 4, 17: 5, 21: 6, 25: 7, 27: 8, 28: 9, 30: 10, 32: 11}

# ── LO 2: 50 ten dich theo video_prompts_TENFILE2.txt (L2 task_012..061) ────
L2_NAMES = [
    "v_G1_clock-2am", "v_G2_sit-up-reach", "v_G3_palm-macro", "v_G4_100yen-shelf",
    "v_G5_corridor-rooms", "v_H1_close-curtain", "v_H3_outdoor-thermo",
    "v_H4_sun-on-wall", "v_H5_wallclock-2am", "v_H6_window-outside-night",
    "v_H7_ceiling-streetlight", "v_H8_two-thermometers", "v_I1_push-bottle-away",
    "v_I3_setting-sun-rays", "v_I4_hand-near-cheek", "v_I5_thermo-wall-vs-air",
    "v_I8_electric-meter", "v_J1_blackout-curtain", "v_J2_fabric-weave-macro",
    "v_J3_ir-thermometer-gun", "v_J4_foil-vs-paper", "v_J5_touch-hot-curtain",
    "v_J6_unroll-foil", "v_J7_hesitate-at-glass", "v_K1_turn-foil-wall-ceiling",
    "v_K3_thatch-village", "v_K4_thatch-surface-sun", "v_K5_thatch-underside",
    "v_K6_woman-fan-farmhouse", "v_K7_susuki-bundle", "v_K8_glasswool-macro",
    "v_K9_thick-wall-window", "v_K10_earthwall-section", "v_L1_doors-open-night",
    "v_L2_engawa-lantern", "v_L3_lock-window-night", "v_L4_roof-turbine",
    "v_L5_eave-vent-inside", "v_L6_hardware-store", "v_L9_foil-vs-window-scale",
    "v_L10_attic-thermo-dusk", "v_M1_lift-panel-calm", "v_M3_insulation-gap",
    "v_M4_closet-to-bedroom", "v_M5_stepladder-ready", "v_M6_hand-along-wall",
    "v_M8_roofers-distant", "v_M9_sleeping-dawn", "v_M10_dawn-paper-screen",
    "v_M11_touch-ceiling-smile",
]
# LO 2 co 5 clip bi thay boi L3 (video_prompts_FIX2_TENFILE.txt) - so la task cua L2
L2_REPLACED = {15: 1, 23: 2, 30: 3, 32: 4, 39: 5}
# ...va task_030 cua L2 bi thay LAN NUA boi L4 (FIX3, ban lan 3 moi DAT)
L2_REPLACED_AGAIN = {30: 1}


def plan():
    """-> [(src, dest_name, need_upscale)]"""
    out = []
    for i, name in enumerate(L1_NAMES, start=1):
        if i in L1_REPLACED:
            out.append((L2 / f"task_{L1_REPLACED[i]:03d}_1_1080p.mp4", name, False))
        else:
            out.append((L1 / f"task_{i:03d}_1_720p.mp4", name, True))
    for j, name in enumerate(L2_NAMES, start=1):
        t = j + 11                       # L2 task_012 == lo2 clip 01
        if t in L2_REPLACED_AGAIN:       # uu tien ban sua MOI NHAT
            out.append((L4 / f"task_{L2_REPLACED_AGAIN[t]:03d}_1_1080p.mp4", name, False))
        elif t in L2_REPLACED:
            out.append((L3 / f"task_{L2_REPLACED[t]:03d}_1_1080p.mp4", name, False))
        else:
            out.append((L2 / f"task_{t:03d}_1_1080p.mp4", name, False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    DST.mkdir(parents=True, exist_ok=True)

    p = plan()
    names = [n for _, n, _ in p]
    assert len(names) == len(set(names)) == 82, f"ten trung hoac thieu: {len(names)}"
    srcs = [s for s, _, _ in p]
    assert len(srcs) == len(set(srcs)), "MOT FILE NGUON DUNG HAI LAN - kiem bang thay the"

    miss = [s for s in srcs if not s.exists()]
    if miss:
        print("🔴 THIEU %d FILE NGUON:" % len(miss))
        for m in miss[:10]:
            print("   ", m)
        sys.exit(1)
    print("✅ du 82/82 file nguon, 0 ten trung, 0 nguon dung lai")

    if a.dry:
        for s, n, up in p[:5]:
            print("  %s -> %s%s" % (s.name, n, "  [UPSCALE 720->1080]" if up else ""))
        print("  ... (%d clip)" % len(p))
        return

    done = skip = 0
    for k, (s, n, up) in enumerate(p, 1):
        o = DST / f"{n}.mp4"
        if o.exists() and o.stat().st_mtime >= s.stat().st_mtime:
            skip += 1
            continue
        vf = "scale=1920:1080:flags=lanczos,fps=30" if up else "fps=30"
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(s), "-vf", vf,
               "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
               "-pix_fmt", "yuv420p", str(o)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print("🔴 FAIL %s: %s" % (n, r.stderr[:200]))
            sys.exit(1)
        done += 1
        print("[%2d/82] %s%s" % (k, n, "  (upscaled)" if up else ""))
    print("XONG: %d moi, %d bo qua -> %s" % (done, skip, DST))


if __name__ == "__main__":
    main()
