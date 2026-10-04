# -*- coding: utf-8 -*-
r"""demo27d.py — DEMO v4: ẢNH TĨNH HOÀN TOÀN + hiệu ứng ở lúc CHỮ VÀO (user chốt 2026-09-17).

LỊCH SỬ 4 BẢN (đừng quay lại bản cũ):
  v1 ảnh phủ khung, không chữ          -> "không có số liệu và chữ gì cả"
  v2 chữ là chính nhưng đổ ập một lúc  -> "muốn ảnh trước rồi text từ từ"
  v3 build-on + pan 3%                 -> "để video tĩnh đi, thêm hiệu ứng cho đẹp"
  v4 (bản này): PAN = 0. Ảnh bất động. Hiệu ứng CHỈ ở khoảnh khắc khối chữ xuất hiện.

🔴 VÌ SAO HIỆU ỨNG Ở ĐÂY KHÔNG LẶP LẠI LỖI CỦA v26 (MAD 9,97): v26 động vì **footage AI 8 giây
chạy liên tục 62% thời lượng** + animation nền. Ở đây mọi hiệu ứng đều **ngắn (0,28–0,45s), một
lần, trên một mảng nhỏ của khung**, phần còn lại của ô là ảnh đứng yên tuyệt đối.
⇒ Vẫn phải đo lại bằng `check_motion.py` sau mỗi lần thêm hiệu ứng, đừng tin suy luận.

BỐN HIỆU ỨNG:
  ① chữ chính : trượt vào 26px từ trái + hiện dần, 0,30s
  ② thẻ phụ   : trượt 18px, lệch nhau 0,45s (cảm giác xếp chồng)
  ③ vòng khoanh đỏ: VẼ DẦN bằng 4 cung nối tiếp (0,10s/cung) — khuôn 完全攻略
  ④ chuyển ô  : dissolve 0,35s (`audience-45plus.md` §2 mục 3: transition mềm ≥0,4s → đây 0,35
                 vì cảnh tĩnh, mắt không cần lâu; nới lên nếu thấy giật)

CHẠY:  python tools/demo27d.py [số_ô]
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
ART, OUT = VD / "art", VD / "_demo_d"
W, H, FPS = 1920, 1080, 30

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)
FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDS = ["NotoSansJP-Bold.otf", "NotoSansCJKjp-Bold.otf", "meiryob.ttc",
              "YuGothB.ttc", "msgothic.ttc"]

T_BIG, D_BIG = 0.8, 0.60      # chữ chính vào lúc 0,8s, mỗi dòng cách 0,60s
T_SUB, D_SUB = 2.0, 0.45      # thẻ phụ
SLIDE_BIG, SLIDE_SUB = 26, 18  # px trượt vào
FADE = 0.30                   # thời gian hiện dần
XFADE = 0.35                  # dissolve giữa các ô
ARCS = 4                      # số cung vẽ vòng khoanh

SHOTS = [
    dict(big=["去年、いくら", "引かれましたか"], color=NAVY, size=92, sub=[],
         art="Elderly_man_holding_blank_paper",
         cap="あなたの年金から、去年いくら引かれたか、ご存じですか。"),
    dict(big=["引かれるもの", "４つ"], color=NAVY, size=92,
         sub=["介護保険料", "後期高齢者医療保険料", "所得税", "住民税"],
         art="Four_deduction_icons_in_row",
         cap="この四つは、一円単位で、一年分すべて載っています。"),
    dict(big=["42万3,700円"], color=RED, size=132, circle=True,
         sub=["どこにも", "載っていません"], art="Elderly_man_holding_blank_paper",
         cap="では、受け取れるはずのお金は。年四十二万三千七百円。"),
    dict(big=["欄は８つ", "該当は０行"], color=NAVY, size=96, sub=[],
         art="Woman_holding_envelope_in_parkin",
         cap="八つある欄を探しても、一行もありません。"),
    dict(big=["５つのうち", "３つ"], color=TEAL, size=104, circle_line=1,
         sub=["おひとり暮らしの", "方のお金です"], art="Two_women_comparing_coin_holdings",
         cap="五つのうち三つは、お一人暮らしのかたのお金です。"),
    dict(big=["請求しないと", "動きません"], color=RED, size=92, sub=[],
         art="Elderly_couple_holding_rice_bowl",
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


def layers(sh, chip, k):
    """(nền, [(png, giây vào, px trượt)]). Vòng khoanh tách thành ARCS lớp cung."""
    im = Image.open(art_for(sh["art"])).convert("RGB")
    bg = im.getpixel((6, 6))
    base = Image.new("RGB", (W, H), bg)
    bw, bh = int(W * 0.45), int(H * 0.72)
    r = min(bw / im.width, bh / im.height)
    im2 = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    base.paste(im2, (int(W * 0.53) + (bw - im2.width) // 2, 150 + (bh - im2.height) // 2))
    d = ImageDraw.Draw(base)
    f = font(42)
    pad, tw = 20, d.textlength(chip, font=f)
    d.rounded_rectangle([64, 46, 64 + tw + pad * 2, 46 + 42 + pad * 2 - 10], radius=12, fill=NAVY)
    d.text((64 + pad, 46 + pad - 7), chip, font=f, fill=(246, 241, 228))
    if sh.get("cap"):
        fc = font(54)
        d.rectangle([0, H - 150, W, H], fill=(236, 226, 203))
        cw = d.textlength(sh["cap"], font=fc)
        d.text(((W - cw) / 2, H - 150 + 44), sh["cap"], font=fc, fill=(33, 39, 48))
    bp = OUT / f"bg{k:02d}.png"
    base.save(bp)

    out, y = [], 250
    fb = font(int(sh["size"] * 1.18))
    for i, line in enumerate(sh["big"]):
        t_in = T_BIG + i * D_BIG
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((96, y), line, font=fb, fill=sh["color"])
        lp = OUT / f"b{k:02d}_{i}.png"
        lay.save(lp)
        out.append((lp, t_in, SLIDE_BIG))

        want = (sh.get("circle") and any(c.isdigit() for c in line)) or sh.get("circle_line") == i
        if want:
            fbb = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
            tw2 = fbb.textlength(line, font=fb)
            hh = int(sh["size"] * 1.18)
            box = [96 - 34, y - 22, 96 + tw2 + 34, y + hh + 16]
            for a in range(ARCS):      # ③ VẼ DẦN: mỗi lớp thêm một cung
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(lay).arc(box, start=-40, end=-40 + 360 * (a + 1) / ARCS,
                                        fill=RED, width=7)
                ap = OUT / f"c{k:02d}_{i}_{a}.png"
                lay.save(ap)
                out.append((ap, t_in + 0.30 + a * 0.10, 0))
        y += int(sh["size"] * 1.18 * 1.20)

    if sh["sub"]:
        fs = font(50)
        y += 18
        for i, s in enumerate(sh["sub"]):
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            tw2 = dl.textlength(s, font=fs)
            dl.rounded_rectangle([96, y, 96 + tw2 + 56, y + 78], radius=10,
                                 fill=(255, 255, 255), outline=NAVY, width=3)
            dl.text((96 + 28, y + 12), s, font=fs, fill=NAVY)
            lp = OUT / f"s{k:02d}_{i}.png"
            lay.save(lp)
            out.append((lp, T_SUB + i * D_SUB, SLIDE_SUB))
            y += 92
    return bp, out


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(SHOTS)
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    chap = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                       if c["chip_l"] else c["chip_r"]) for c in plan["chapters"]}
    shots = plan["shots"][:n]
    parts = []
    for k, s in enumerate(shots):
        dur = s["t1"] - s["t0"] + (XFADE if k < len(shots) - 1 else 0)
        sh = SHOTS[k % len(SHOTS)]
        bp, lays = layers(sh, chap.get(s["chap"], ""), k)
        # ⚠️ PAN = 0: ảnh bất động (user chốt "để video tĩnh đi")
        chain = f"[0:v]scale={W}:{H}[bg];"
        cur, ins = "bg", ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(bp)]
        for i, (lp, t0, slide) in enumerate(lays):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(lp)]
            # ① fade alpha  ② x trượt dần về 0
            chain += (f"[{i+1}:v]format=rgba,fade=in:st={t0:.2f}:d={FADE}:alpha=1[L{i}];")
            xs = (f"-{slide}*max(0\\,1-(t-{t0:.2f})/{FADE})" if slide else "0")
            chain += (f"[{cur}][L{i}]overlay=x='{xs}':y=0:"
                      f"enable='gte(t,{t0:.2f})'[v{i}];")
            cur = f"v{i}"
        mp = OUT / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins,
                        "-filter_complex", chain.rstrip(";"), "-map", f"[{cur}]",
                        "-r", str(FPS), "-pix_fmt", "yuv420p", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "18", str(mp)], check=True)
        parts.append((mp, s["t1"] - s["t0"]))
        print(f"  ô {k} {s['t1']-s['t0']:>5.1f}s  {len(lays)} lớp  tĩnh(pan=0)")

    # ── ④ nối bằng dissolve xfade
    cur_lbl, ins, chain, off = "0:v", [], "", 0.0
    for i, (mp, d0) in enumerate(parts):
        ins += ["-i", str(mp)]
    for i in range(1, len(parts)):
        off += parts[i - 1][1] - (XFADE if i > 1 else 0)
        nxt = f"x{i}"
        chain += (f"[{cur_lbl}][{i}:v]xfade=transition=fade:duration={XFADE}:"
                  f"offset={off:.3f}[{nxt}];")
        cur_lbl = nxt
    sil = OUT / "_v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", chain.rstrip(";"),
                    "-map", f"[{cur_lbl}]", "-r", str(FPS), "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(sil)], check=True)
    fin = VD / "demo27d.mp4"
    t_end = shots[-1]["t1"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sil), "-i", str(VD / "voice_full.wav"),
                    "-t", f"{t_end:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-4:LRA=7", "-shortest", str(fin)], check=True)
    print(f"\n→ {fin}  ({t_end:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
