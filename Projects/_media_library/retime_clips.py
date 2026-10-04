# -*- coding: utf-8 -*-
r"""RETIME CLIP AI 8s -> 10s (dung chung moi kenh).

VI SAO: cong cu gen (Flow/Veo...) chi xuat 8 giay. Dung nguyen 8s thi nhip doi hinh
= 60/8 = 7,5 lan/phut, VUOT tran 6,0/phut cua `.claude/rules/audience-45plus.md` §2
(tep 45-70 roi video vi nhip met). Gian 8s -> 10s bang setpts:
  - so clip can: 1114s / 10 = 112 thay vi 140
  - nhip: 6,0/phut = dung tran
  - chuyen dong cham hon 20% = dung luat kenh "khung dung yen, khong giat"

CACH DUNG:
  python retime_clips.py <thu_muc_clip>                    # -> <thu_muc>_10s/
  python retime_clips.py clips --factor 1.25 --fps 30
  python retime_clips.py clips --check                     # chi do, khong encode

BAY DA BIET:
  - setpts chi gian TIMESTAMP. Clip 24fps -> sau khi gian con ~19,2fps hieu dung.
    Vi vay MAC DINH ep `-r 30` (ffmpeg tu nhan doi frame) de playback muot.
    Chuyen dong trong prompt cua ta von rat cham (bui bay, nuoc chay, anh sang bo)
    nen khong can noi suy. Neu VAN thay giat o clip nao: chay lai rieng clip do voi
    --interp (minterpolate) - cham hon nhieu va co the sinh artifact o mep vat the.
  - `-an` bo audio: clip AI hay kem tieng nen rac, video chi dung TTS + BGM.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FFMPEG = shutil.which("ffmpeg")
FFPROBE = shutil.which("ffprobe")


def dur_of(p: Path):
    """Do thoi luong that bang ffprobe. None neu doc khong duoc."""
    try:
        out = subprocess.run(
            [FFPROBE, "-v", "error", "-print_format", "json",
             "-show_entries", "format=duration:stream=r_frame_rate",
             "-select_streams", "v:0", str(p)],
            capture_output=True, text=True, timeout=60)
        j = json.loads(out.stdout or "{}")
        d = float(j.get("format", {}).get("duration", 0) or 0)
        fr = (j.get("streams") or [{}])[0].get("r_frame_rate", "0/1")
        n, _, dd = fr.partition("/")
        fps = float(n) / float(dd or 1) if float(dd or 1) else 0.0
        return d, fps
    except Exception:
        return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="thu muc chua clip .mp4 vua gen")
    ap.add_argument("-o", "--out", default=None, help="thu muc ra (mac dinh <src>_10s)")
    ap.add_argument("--factor", type=float, default=1.25, help="he so gian (1.25 = 8s->10s)")
    ap.add_argument("--fps", type=int, default=30, help="fps dau ra (0 = giu nguyen)")
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--interp", action="store_true",
                    help="noi suy khung (minterpolate) - CHI dung cho clip bi giat")
    ap.add_argument("--crop", type=float, default=0.0,
                    help="ti le cat MOI BEN de bo watermark AI + vien film gia "
                         "(vd 0.032 = cat 3,2%% moi ben roi phong lai). 0 = khong cat")
    ap.add_argument("--size", default=None,
                    help="ep kich thuoc dau ra, vd 1920x1080 (chuan hoa lo clip lan do phan giai)")
    ap.add_argument("--check", action="store_true", help="chi do thoi luong, khong encode")
    a = ap.parse_args()

    if not FFMPEG or not FFPROBE:
        print("🔴 KHONG TIM THAY ffmpeg/ffprobe trong PATH"); return 1

    src = Path(a.src)
    if not src.is_dir():
        print(f"🔴 khong phai thu muc: {src}"); return 1
    clips = sorted(p for p in src.glob("*.mp4") if not p.name.startswith("_"))
    if not clips:
        print(f"🔴 khong co .mp4 nao trong {src}"); return 1

    target = None
    print(f"── {len(clips)} clip trong {src}")
    if a.check:
        bad = 0
        for p in clips:
            d, fps = dur_of(p)
            flag = ""
            if d is None:
                flag = "  🔴 DOC KHONG DUOC"; bad += 1
            elif abs(d - 8.0) > 1.5:
                flag = f"  ⚠️ khong phai ~8s"
            print(f"  {p.name:44s} {d if d else 0:5.2f}s  {fps if fps else 0:5.1f}fps{flag}")
        print(f"\ntong {len(clips)} clip · sau khi gian x{a.factor}: "
              f"~{len(clips) * 8 * a.factor:.0f}s · nhip {60 / (8 * a.factor):.1f} doi hinh/phut")
        return 1 if bad else 0

    out = Path(a.out) if a.out else src.parent / (src.name + "_10s")
    out.mkdir(parents=True, exist_ok=True)

    chain = []
    if a.crop > 0:
        # cat deu MOI BEN theo ti le -> bo watermark goc duoi-phai + vien film o 2 mep
        k = a.crop
        chain.append(f"crop=in_w*{1-2*k:.6f}:in_h*{1-2*k:.6f}:in_w*{k:.6f}:in_h*{k:.6f}")
    if a.size:
        w, _, h = a.size.lower().partition("x")
        # setsar=1 BAT BUOC: crop le co the de lai sample aspect != 1 -> anh bi keo
        chain.append(f"scale={int(w)}:{int(h)},setsar=1")
    if a.interp:
        chain.append(f"minterpolate=fps={a.fps or 30}:mi_mode=mci:mc_mode=aobmc")
    chain.append(f"setpts={a.factor}*PTS")
    vf = ",".join(chain)

    print(f"   filter: {vf}")
    ok, fail, skip = 0, [], 0
    for i, p in enumerate(clips, 1):
        dst = out / p.name
        # BAY RESUME (`render-background.md` §2.5): hoi "con DUNG khong", khong hoi "co ton tai khong"
        if dst.exists() and dst.stat().st_mtime >= p.stat().st_mtime:
            d, _ = dur_of(dst)
            if d and abs(d - 8 * a.factor) < 0.4:
                skip += 1
                continue
        cmd = [FFMPEG, "-y", "-i", str(p), "-filter:v", vf, "-an",
               "-c:v", "libx264", "-crf", str(a.crf), "-preset", "veryfast",
               "-pix_fmt", "yuv420p"]
        if a.fps:
            cmd += ["-r", str(a.fps)]
        cmd += [str(dst)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        d, fps = dur_of(dst) if dst.exists() else (None, None)
        want = 8 * a.factor
        if r.returncode != 0 or d is None or abs(d - want) > 0.5:
            fail.append((p.name, r.returncode, d))
            print(f"  [{i}/{len(clips)}] 🔴 {p.name}  exit={r.returncode} dur={d}")
        else:
            ok += 1
            print(f"  [{i}/{len(clips)}] ✅ {p.name}  -> {d:.2f}s @{fps:.0f}fps")

    total = (ok + skip) * 8 * a.factor
    print(f"\n── XONG: {ok} moi · {skip} bo qua (da dung) · {len(fail)} loi")
    print(f"   tong thoi luong ~{total:.0f}s · nhip {60 / (8 * a.factor):.1f} doi hinh/phut")
    print(f"   dau ra: {out}")
    if fail:
        print("🔴 CAC CLIP LOI (gen lai hoac chay rieng voi --interp):")
        for n, rc, d in fail:
            print(f"   - {n}  exit={rc} dur={d}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
