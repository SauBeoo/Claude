# -*- coding: utf-8 -*-
r"""demo27b.py — DEMO v2: CHỮ LÀ CHÍNH, ảnh là minh hoạ (sửa sau phản hồi 2026-09-17).

🔴 VÌ SAO CÓ BẢN B: demo v1 (`demo27.py`) để ảnh phủ kín khung, chữ chỉ có chip chương
⇒ user: *"ảnh mày tĩnh quá, nó không có số liệu và chữ gì cả. Không giống video tao gửi"*.
Đúng. Mổ lại 3 video thắng: **chữ chiếm 50–65% khung, ảnh いらすとや chỉ là minh hoạ bên cạnh**
(完全攻略 telop đỏ/xanh + sơ đồ hộp · なぎさ thẻ trắng chứa số · ひろと chữ 2 dòng giữa khung).
⇒ Layout đảo lại: cột CHỮ trái (55%) · ảnh phải (45%), thêm dải phụ đề đáy.

CHẠY:  python tools/demo27b.py [số_ô]
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
ART, OUT = VD / "art", VD / "_demo_b"
W, H, FPS = 1920, 1080, 30

CREAM, NAVY, RED, TEAL = (246, 241, 228), (31, 56, 100), (192, 57, 43), (62, 124, 120)
GREY = (120, 126, 132)

FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDS = ["NotoSansJP-Bold.otf", "NotoSansCJKjp-Bold.otf", "meiryob.ttc",
              "YuGothB.ttc", "msgothic.ttc"]

# ── TELOP từng ô: (dòng chính, cỡ, màu) + danh sách phụ + ảnh dùng ────────────
# Chữ rút TỪ CHÍNH lời đọc của ô đó (YMYL: không thêm số mới — `CLAUDE.md` §③).
SHOTS = [
    dict(big=["去年、いくら", "引かれましたか"], color=NAVY, size=92,
         sub=[], art="Elderly_man_holding_blank_paper",
         cap="あなたの年金から、去年いくら引かれたか、ご存じですか。"),
    dict(big=["引かれるもの", "４つ"], color=NAVY, size=92,
         sub=["介護保険料", "後期高齢者医療保険料", "所得税", "住民税"],
         art="Four_deduction_icons_in_row",
         cap="この四つは、一円単位で、一年分すべて載っています。"),
    dict(big=["42万3,700円"], color=RED, size=132, circle=True,
         sub=["どこにも", "載っていません"], art="Elderly_man_holding_blank_paper",
         cap="では、受け取れるはずのお金は。年四十二万三千七百円。"),
    dict(big=["欄は８つ", "該当は０行"], color=NAVY, size=96,
         sub=[], art="Woman_holding_envelope_in_parkin",
         cap="八つある欄を探しても、一行もありません。"),
    dict(big=["５つのうち", "３つ"], color=TEAL, size=104, circle=True,
         sub=["おひとり暮らしの", "方のお金です"], art="Two_women_comparing_coin_holdings",
         cap="五つのうち三つは、お一人暮らしのかたのお金です。"),
    dict(big=["請求しないと", "動きません"], color=RED, size=92,
         sub=[], art="Elderly_couple_holding_rice_bowl",
         cap="資格があっても、一円も動きません。"),
]


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
    raise SystemExit(f"⛔ không thấy ảnh '{key}'")


def frame(sh: dict, chip: str) -> Image.Image:
    # 🔴 Canvas lấy ĐÚNG màu nền của chính ảnh. Bản đầu dùng hằng số CREAM (246,241,228)
    # trong khi ảnh gen ra nền (244-245, 234-238, 212-216) => lệch 10-16 o kenh B, du de
    # hien thanh KHUNG CHU NHAT quanh anh. Chi lo khi soi sheet, khong lo khi xem anh le.
    im = Image.open(art_for(sh["art"])).convert("RGB")
    bg = im.getpixel((6, 6))
    base = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(base)
    box_w, box_h = int(W * 0.45), int(H * 0.72)
    r = min(box_w / im.width, box_h / im.height)
    im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    base.paste(im, (int(W * 0.53) + (box_w - im.width) // 2, 150 + (box_h - im.height) // 2))

    # ── CHIP chương (góc trên-trái, khuôn 完全攻略)
    f = font(42)
    pad, tw = 20, d.textlength(chip, font=f)
    d.rounded_rectangle([64, 46, 64 + tw + pad * 2, 46 + 42 + pad * 2 - 10], radius=12, fill=NAVY)
    d.text((64 + pad, 46 + pad - 7), chip, font=f, fill=CREAM)

    # ── DÒNG CHÍNH: cột trái, đây là thứ người xem đọc trước
    y = 250
    fb = font(int(sh["size"] * 1.18))
    for line in sh["big"]:
        if sh.get("circle") and any(c.isdigit() for c in line):
            tw = d.textlength(line, font=fb)
            hh = int(sh["size"] * 1.18)
            d.ellipse([96 - 34, y - 22, 96 + tw + 34, y + hh + 16], outline=RED, width=7)
        d.text((96, y), line, font=fb, fill=sh["color"])
        y += int(sh["size"] * 1.18 * 1.20)

    # ── DANH SÁCH PHỤ: thẻ trắng viền navy (khuôn なぎさ)
    if sh["sub"]:
        fs = font(50)
        y += 18
        for s in sh["sub"]:
            tw = d.textlength(s, font=fs)
            d.rounded_rectangle([96, y, 96 + tw + 56, y + 78], radius=10,
                                fill=(255, 255, 255), outline=NAVY, width=3)
            d.text((96 + 28, y + 12), s, font=fs, fill=NAVY)
            y += 92

    # ── PHỤ ĐỀ: dải đáy, chữ navy trên kem đậm hơn (khuôn 完全攻略)
    if sh.get("cap"):
        fc = font(54)
        d.rectangle([0, H - 150, W, H], fill=(236, 226, 203))
        tw = d.textlength(sh["cap"], font=fc)
        d.text(((W - tw) / 2, H - 150 + 44), sh["cap"], font=fc, fill=(33, 39, 48))
    return base


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(SHOTS)
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    chap = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                       if c["chip_l"] else c["chip_r"]) for c in plan["chapters"]}
    shots = plan["shots"][:n]
    parts = []
    for k, s in enumerate(shots):
        dur = s["t1"] - s["t0"]
        sh = SHOTS[k % len(SHOTS)]
        fp = OUT / f"f{k:02d}.png"
        frame(sh, chap.get(s["chap"], "")).save(fp)
        pan = s.get("pan")
        if pan:
            z = 1 + pan["pct"] / 100.0
            dirs = {"lr": ("(iw-1920)*(t/D)", "0"), "rl": ("(iw-1920)*(1-t/D)", "0"),
                    "tb": ("0", "(ih-1080)*(t/D)"), "bt": ("0", "(ih-1080)*(1-t/D)")}
            ex, ey = dirs[pan["dir"]]
            vf = (f"scale={int(W*z)}:{int(H*z)},crop=1920:1080:"
                  f"'{ex.replace('D', str(dur))}':'{ey.replace('D', str(dur))}'")
        else:
            vf = "scale=1920:1080"
        mp = OUT / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{dur:.3f}",
                        "-i", str(fp), "-vf", f"{vf},fps={FPS},format=yuv420p",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(mp)],
                       check=True)
        parts.append(mp)
        print(f"  ô {k} {dur:>5.1f}s pan={pan['dir'] if pan else '—':<3} 「{'／'.join(sh['big'])}」")

    (OUT / "c.txt").write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
    sil = OUT / "_v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", "c.txt", "-c", "copy", str(sil)], check=True, cwd=OUT)
    fin = VD / "demo27b.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sil), "-i", str(VD / "voice_full.wav"),
                    "-t", f"{shots[-1]['t1']:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-4:LRA=7", "-shortest", str(fin)], check=True)
    print(f"\n→ {fin}  ({shots[-1]['t1']:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
