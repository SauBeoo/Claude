# -*- coding: utf-8 -*-
r"""demo27.py — dựng DEMO look mới cho video 27 (ffmpeg, không qua Remotion).

MỤC ĐÍCH: cho user duyệt LOOK trước khi đổ công vào 86 ảnh + builder Remotion.
Demo có đủ 4 thứ đang thử: ảnh phẳng nền kem · chip chương · pan chậm 3% · phụ đề cháy.
Theo `humanize-script-voice.md` §3 và `render-background.md`: RENDER DEMO TRƯỚC.

CHẠY:  python tools/demo27.py [số_ô]      (mặc định 5 ô đầu)
"""
import io
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "27_nenkin-tsuchisho-nai-okane-5tsu"
VD = PROJ / "06_VIDEO" / STEM
ART = VD / "art"
OUT = VD / "_demo"
W, H, FPS = 1920, 1080, 30

CREAM = (246, 241, 228)
NAVY = (31, 56, 100)
RED = (192, 57, 43)

FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDS = ["NotoSansJP-Bold.otf", "NotoSansCJKjp-Bold.otf", "meiryob.ttc",
              "YuGothB.ttc", "msgothic.ttc"]

# ô nào dùng ảnh nào (lô LOT1 — 7 ảnh thử)
PICK = ["Elderly_man_holding_blank_paper", "Four_deduction_icons_in_row",
        "Elderly_man_holding_blank_paper", "Woman_holding_envelope_in_parkin",
        "Two_women_comparing_coin_holdings"]


def font(size: int):
    for n in FONT_CANDS:
        p = FONT_DIR / n
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def art_for(key: str) -> Path:
    for p in sorted(ART.iterdir()):
        if key[:26] in p.name:
            return p
    raise SystemExit(f"⛔ không thấy ảnh cho '{key}' trong {ART}")


def build_frame(img_path: Path, chip: str) -> Image.Image:
    """Ảnh phủ kín khung nền kem + chip chương góc trên-trái."""
    base = Image.new("RGB", (W, H), CREAM)
    im = Image.open(img_path).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    base.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
    if chip:
        d = ImageDraw.Draw(base)
        f = font(44)
        pad = 22
        tw = d.textlength(chip, font=f)
        d.rounded_rectangle([56, 48, 56 + tw + pad * 2, 48 + 44 + pad * 2 - 12],
                            radius=14, fill=NAVY)
        d.text((56 + pad, 48 + pad - 8), chip, font=f, fill=CREAM)
    return base


def main() -> int:
    n_shot = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    chap_name = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                            if c["chip_l"] else c["chip_r"])
                 for c in plan["chapters"]}
    shots = plan["shots"][:n_shot]

    parts = []
    for k, s in enumerate(shots):
        dur = s["t1"] - s["t0"]
        chip = chap_name.get(s["chap"], "")
        frame = build_frame(art_for(PICK[k % len(PICK)]), chip)
        fp = OUT / f"f{k:02d}.png"
        frame.save(fp)

        pan = s.get("pan")
        if pan:
            z = 1 + pan["pct"] / 100.0
            zw, zh = int(W * z), int(H * z)
            dirs = {"lr": ("(iw-1920)*(t/D)", "0"), "rl": ("(iw-1920)*(1-t/D)", "0"),
                    "tb": ("0", "(ih-1080)*(t/D)"), "bt": ("0", "(ih-1080)*(1-t/D)")}
            ex, ey = dirs[pan["dir"]]
            vf = (f"scale={zw}:{zh},crop=1920:1080:"
                  f"'{ex.replace('D', str(dur))}':'{ey.replace('D', str(dur))}'")
        else:
            vf = "scale=1920:1080"
        mp = OUT / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{dur:.3f}",
                        "-i", str(fp), "-vf", f"{vf},fps={FPS},format=yuv420p",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(mp)],
                       check=True)
        parts.append(mp)
        print(f"  ô {k}  {dur:>5.1f}s  pan={pan['dir'] if pan else '—':<3}  chip「{chip}」")

    lst = OUT / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
    silent = OUT / "_video.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", str(silent)], check=True, cwd=OUT)

    t_end = shots[-1]["t1"]
    final = VD / "demo27.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent),
                    "-i", str(VD / "voice_full.wav"), "-t", f"{t_end:.3f}",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-4:LRA=7", "-shortest", str(final)], check=True)
    print(f"\n→ {final}  ({t_end:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
