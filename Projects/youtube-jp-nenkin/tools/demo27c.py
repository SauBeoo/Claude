# -*- coding: utf-8 -*-
r"""demo27c.py — DEMO v3: ẢNH hiện TRƯỚC, CHỮ hiện dần SAU (user chốt 2026-09-17).

LỊCH SỬ 3 BẢN — đọc để không quay lại bản cũ:
  v1 `demo27.py`  : ảnh phủ kín khung, không chữ        -> user: "không có số liệu và chữ gì cả"
  v2 `demo27b.py` : chữ là chính, nhưng ĐỔ ẬP một lúc   -> user: "muốn ảnh trước rồi text từ từ"
  v3 (bản này)    : ảnh vào trước, từng khối chữ hiện dần theo mốc giây

CÁCH DỰNG (quan trọng khi port sang Remotion):
  · Mỗi khối chữ là **một lớp PNG trong suốt riêng**, bật bằng `overlay:enable='gte(t,X)'`.
  · **Pan chỉ áp cho LỚP ẢNH**, chữ đứng yên tuyệt đối — chữ trôi thì tệp 65+ đọc không kịp.
  · Cắt cứng khi khối chữ vào (không fade): 完全攻略 làm vậy, và fade làm tăng MAD vô ích.

CHẠY:  python tools/demo27c.py [số_ô]
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
ART, OUT = VD / "art", VD / "_demo_c"
W, H, FPS = 1920, 1080, 30

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)
FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDS = ["NotoSansJP-Bold.otf", "NotoSansCJKjp-Bold.otf", "meiryob.ttc",
              "YuGothB.ttc", "msgothic.ttc"]

# mốc vào (giây, tính từ đầu ô) — ảnh 0,0 · chữ chính 0,8 · mỗi thẻ phụ cách 0,55s
T_BIG, T_SUB, D_SUB = 0.8, 2.0, 0.55

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


def layers(sh: dict, chip: str, k: int):
    """Trả (nền, [(lớp png, giây vào)]). Nền = ảnh + chip; mỗi khối chữ một lớp riêng."""
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
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        # 🔴 chỉ khoanh MỘT dòng (bản v2 khoanh cả hai dòng -> rối)
        want = (sh.get("circle") and any(c.isdigit() for c in line)) or sh.get("circle_line") == i
        if want:
            tw2 = dl.textlength(line, font=fb)
            hh = int(sh["size"] * 1.18)
            dl.ellipse([96 - 34, y - 22, 96 + tw2 + 34, y + hh + 16], outline=RED, width=7)
        dl.text((96, y), line, font=fb, fill=sh["color"])
        lp = OUT / f"b{k:02d}_{i}.png"
        lay.save(lp)
        out.append((lp, T_BIG + i * 0.6))
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
            out.append((lp, T_SUB + i * D_SUB))
            y += 92
    return bp, out


def main() -> int:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else len(SHOTS)
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    chap = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                       if c["chip_l"] else c["chip_r"]) for c in plan["chapters"]}
    parts = []
    for k, s in enumerate(plan["shots"][:n]):
        dur = s["t1"] - s["t0"]
        sh = SHOTS[k % len(SHOTS)]
        bp, lays = layers(sh, chap.get(s["chap"], ""), k)

        pan = s.get("pan")
        if pan:
            z = 1 + pan["pct"] / 100.0
            dd = {"lr": (f"(iw-{W})*(t/{dur})", "0"), "rl": (f"(iw-{W})*(1-t/{dur})", "0"),
                  "tb": ("0", f"(ih-{H})*(t/{dur})"), "bt": ("0", f"(ih-{H})*(1-t/{dur})")}
            ex, ey = dd[pan["dir"]]
            # ⚠️ pan CHỈ trên nền; chữ overlay sau nên đứng yên tuyệt đối
            chain = f"[0:v]scale={int(W*z)}:{int(H*z)},crop={W}:{H}:'{ex}':'{ey}'[bg];"
        else:
            chain = f"[0:v]scale={W}:{H}[bg];"
        cur, ins = "bg", ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(bp)]
        for i, (lp, t0) in enumerate(lays):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(lp)]
            nxt = f"v{i}"
            chain += (f"[{cur}][{i+1}:v]overlay=0:0:enable='gte(t,{t0:.2f})'[{nxt}];")
            cur = nxt
        chain = chain.rstrip(";")
        mp = OUT / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", chain,
                        "-map", f"[{cur}]", "-r", str(FPS), "-pix_fmt", "yuv420p",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(mp)],
                       check=True)
        parts.append(mp)
        print(f"  ô {k} {dur:>5.1f}s  {len(lays)} lớp chữ  vào lúc "
              f"{', '.join(f'{t:.1f}s' for _, t in lays)}")

    (OUT / "c.txt").write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
    sil = OUT / "_v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", "c.txt", "-c", "copy", str(sil)], check=True, cwd=OUT)
    fin = VD / "demo27c.mp4"
    t_end = plan["shots"][:n][-1]["t1"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sil), "-i", str(VD / "voice_full.wav"),
                    "-t", f"{t_end:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-4:LRA=7", "-shortest", str(fin)], check=True)
    print(f"\n→ {fin}  ({t_end:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
