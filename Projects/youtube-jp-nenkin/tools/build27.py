# -*- coding: utf-8 -*-
r"""build27.py — DỰNG ĐẦY ĐỦ video 27 (86 ô). Khuôn = demo27e đã được user duyệt.
KHUON = demo27e (user duyet 2026-09-17). Lich su 5 ban demo:

LỊCH SỬ 4 BẢN (đừng quay lại bản cũ):
  v1 ảnh phủ khung, không chữ          -> "không có số liệu và chữ gì cả"
  v2 chữ là chính nhưng đổ ập một lúc  -> "muốn ảnh trước rồi text từ từ"
  v3 build-on + pan 3%                 -> "để video tĩnh đi, thêm hiệu ứng cho đẹp"
  v4 PAN=0, hiệu ứng lúc chữ vào     -> user: "con cú vs hình surprise của tôi đâu"
  v5 (bản này): thêm lại **MASCOT CÚ** (nhận diện kênh) + **sticker biểu cảm cast**.

🦉 MASCOT CÚ — dùng **MỘT frame tĩnh**, không loop 192 frame.
   Lý do: cú là "vật cố định" duy nhất được phép (`audience-45plus.md` §2.0-quater mục 4, trần ≤1);
   để nó nhấp nháy suốt bài là thêm một nguồn động thường trực — đúng bệnh đã làm v26 lên MAD 9,97.
   Muốn cú động thì cho động ở VÀI mốc, không phải cả video.
😲 STICKER CAST (`josei_surprised`…) — bật ở khoảnh khắc lật, pop vào rồi đứng yên.
   ⚠️ `audience-45plus.md` §2.0f-bis: 1 sticker chỉ xuất hiện ĐÚNG 1 lần/ô, vào SAU hero ~2s.

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
ART, OUT = VD / "art_final", VD / "_build"
W, H, FPS = 1920, 1080, 30

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)
FONT_DIR = Path(r"C:\Windows\Fonts")
FONT_CANDS = ["NotoSansJP-Bold.otf", "NotoSansCJKjp-Bold.otf", "meiryob.ttc",
              "YuGothB.ttc", "msgothic.ttc"]

T_BIG, D_BIG = 0.8, 0.60      # chữ chính vào lúc 0,8s, mỗi dòng cách 0,60s
OWL = Path("E:/Claude/Projects/remotion-vox/public/projects/nenkin-26/assets/owl_idle/f_0001.png")
# 🔴 BỐN SỐ NÀY LẤY NGUYÊN TỪ `build_remotion_26.py` brand{} — KHÔNG tự đặt lại.
# user: "video cũ như nào mày phải làm như thế chứ". Bản đầu tao tự chọn OWL_H=190 và tự đặt
# lề đáy ⇒ cú nhỏ hơn thật 1,6 lần và LOGO bị bỏ quên hoàn toàn.
# user 2026-09-17: "cho nhỏ thôi, thấp xuống tí nữa không chắn vào các chữ"
# ⇒ nhỏ hơn v26 (300 -> 210) và hạ sát đáy hơn (lề 186 -> 104), để cú không ăn vào
# vùng ảnh minh hoạ bên phải.
OWL_H = 210                   # v26 để 300 — user thấy to quá
LOGO_H = 110                  # logoH của v26 — góc TRÊN-PHẢI
BOT_MASCOT = 158              # nâng lên (user: "con cú cho cao lên"); v26 để 186
BOT_SUBS = 46                 # nam GON trong dai phu de, sat goc duoi-trai (v26: 200)
LOGO = Path("E:/Claude/Projects/remotion-vox/public/projects/nenkin-26/assets/brand_logo.png")
OWL_SEQ = Path("E:/Claude/Projects/remotion-vox/public/projects/nenkin-26/assets/owl_idle")
SUBS_RED = (225, 43, 43)      # #E12B2B — lấy từ BrandOverlay.tsx, đừng đoán lại
STK_H = 330                   # sticker cast
T_SUB, D_SUB = 2.0, 0.45      # thẻ phụ
SLIDE_BIG, SLIDE_SUB = 26, 18  # px trượt vào
FADE = 0.30                   # thời gian hiện dần
XFADE = 0.35                  # dissolve giữa các ô
ARCS = 4                      # số cung vẽ vòng khoanh

sys.path.insert(0, str(PROJ / "tools"))
from telop27 import TELOP          # noqa: E402

def cap_of(text: str) -> str:
    """Phụ đề = câu ĐẦU của ô, cắt ở 。 — không tự viết lại lời."""
    s = text.strip()
    if not s:
        return ""
    for mark in ("。", "？"):
        if mark in s:
            s = s.split(mark)[0] + mark
            break
    return s[:38]



def font(size: int):
    for n in FONT_CANDS:
        p = FONT_DIR / n
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def art_for(k: int) -> Path:
    p = ART / f"shot_{k:03d}.png"
    if not p.exists():
        raise SystemExit(f"⛔ thiếu ảnh ô {k}: {p}")
    return p


def subscribe_layers():
    """4 trạng thái nút SUBSCRIBE, khớp nhịp của `BrandOverlay.tsx`:
       nằm im 0–2,6s · con trỏ trượt tới 2,6–3,0s · NẢY 1,12x 3,0–3,25s · giữ 3,25–4,0s.
       Vẽ 1 lần, dùng lại cho mọi ô (nút không đổi theo nội dung)."""
    f = font(25)   # nút nhỏ lại (user)
    out = []
    # user: "cái chuột thì ở chỗ subscribe luôn" ⇒ con trỏ ĐỨNG YÊN cạnh nút,
    # bỏ hẳn đoạn trượt tới/lui. Chỉ còn 2 trạng thái: thường và nảy.
    for name, scale, cx in (("a", 1.00, 4), ("b", 1.00, 4),
                            ("c", 1.12, 4), ("d", 1.00, 4)):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        lbl = "SUBSCRIBE"
        lw = dl.textlength(lbl, font=f)
        bw2, bh2 = int(44 + lw + 30), 50
        sw, sh2 = int(bw2 * scale), int(bh2 * scale)
        sx, sy = int(W * 0.012), H - BOT_SUBS - sh2   # neo MÉP ĐÁY, lề = subscribeBottom
        btn = Image.new("RGBA", (bw2, bh2), (0, 0, 0, 0))
        db = ImageDraw.Draw(btn)
        db.rounded_rectangle([0, 0, bw2 - 1, bh2 - 1], radius=10,
                             fill=SUBS_RED, outline=(255, 255, 255), width=3)
        db.rounded_rectangle([13, 15, 46, 36], radius=5, fill=(255, 255, 255))
        db.polygon([(25, 20), (38, 26), (25, 32)], fill=SUBS_RED)
        db.text((54, 12), lbl, font=f, fill=(255, 255, 255))
        lay.paste(btn.resize((sw, sh2), Image.LANCZOS), (sx, sy), btn.resize((sw, sh2)))
        # con trỏ chuột trượt tới rồi bấm
        px, py = sx + sw - 22 + cx, sy + sh2 - 10
        dl.polygon([(px, py), (px, py + 26), (px + 7, py + 19),
                    (px + 11, py + 28), (px + 16, py + 26), (px + 11, py + 17),
                    (px + 20, py + 16)], fill=(255, 255, 255), outline=(40, 40, 40))
        lp = OUT / f"sub_{name}.png"
        lay.save(lp)
        out.append(lp)
    return out


def caption_layers(k, lines_idx, tl_lines, t0):
    """Mỗi DÒNG lời đọc = một lớp phụ đề riêng, bật đúng khoảng của dòng đó."""
    fc = font(50)
    out = []
    for j, li in enumerate(lines_idx):
        ln = tl_lines[li]
        txt = ln["text"].strip()
        if not txt:
            continue
        # ≤2 dòng/khối, cỡ ≥22 (audience-45plus §3): ở 1920 thì 50px là thoả
        if len(txt) > 34:
            cut = txt.rfind("、", 0, 34)
            txt2 = [txt[:cut + 1], txt[cut + 1:][:34]] if cut > 12 else [txt[:34], txt[34:68]]
        else:
            txt2 = [txt]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        y0 = H - 150 + (30 if len(txt2) > 1 else 46)
        for r, line in enumerate(txt2):
            cw = dl.textlength(line, font=fc)
            CAP_X0 = 250
            dl.text((CAP_X0 + (W - CAP_X0 - cw) / 2, y0 + r * 58), line, font=fc,
                    fill=(33, 39, 48))
        lp = OUT / f"cap{k:02d}_{j}.png"
        lay.save(lp)
        out.append((lp, max(0.0, ln["start"] - t0), ln["end"] - t0))
    return out


def layers(sh, chip, k):
    """(nền, [(png, giây vào, px trượt)]). Vòng khoanh tách thành ARCS lớp cung."""
    im = Image.open(art_for(sh["k"])).convert("RGB")
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
    # 🔴 PHỤ ĐỀ ĐỔI THEO TỪNG DÒNG LỜI ĐỌC, không phải một câu cho cả ô.
    # Bản đầu lấy câu đầu của ô rồi cắt ở 。 ⇒ ô 1 đọc 4 khoản + một câu dài mà phụ đề chỉ
    # hiện 「介護保険料。」 suốt 11 giây. Phụ đề sai lời là lỗi nặng hơn mọi lỗi bố cục.
    # Nền chỉ vẽ DẢI; chữ do lớp riêng bật theo mốc của từng dòng (xem caption_layers).
    d.rectangle([0, H - 150, W, H], fill=(236, 226, 203))
    if False:
        fc = font(54)
        cw = d.textlength(sh["cap"], font=fc)
        # 🔴 Căn giữa trong vùng CÒN TRỐNG, không phải giữa khung: nút SUBSCRIBE nằm trong
        # dải phụ đề ở góc trái, căn giữa toàn khung thì chữ tràn vào và bị nút che mất
        # ký tự đầu (đã dính: 「あなたの…」 -> nhìn thành 「なたの…」).
        CAP_X0 = 250          # mép phải của nút + lề
        d.text((CAP_X0 + (W - CAP_X0 - cw) / 2, H - 150 + 44), sh["cap"], font=fc,
               fill=(33, 39, 48))
    # 🏷 LOGO — góc TRÊN-PHẢI (v26: logoH 110, right ~1,2% · top ~1,5%)
    if LOGO.exists():
        lg = Image.open(LOGO).convert("RGBA")
        r4 = LOGO_H / lg.height
        lg = lg.resize((int(lg.width * r4), LOGO_H), Image.LANCZOS)
        base.paste(lg, (W - lg.width - int(W * 0.012), int(H * 0.015)), lg)

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

    # 😲 STICKER CAST — vào SAU hero, đúng 1 lần trong ô (§2.0f-bis)
    if sh.get("stk"):
        sp = PROJ / "assets" / "cast" / f'{sh["stk"]}.png'
        if sp.exists():
            st = Image.open(sp).convert("RGBA")
            r3 = STK_H / st.height
            st = st.resize((int(st.width * r3), STK_H), Image.LANCZOS)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.paste(st, (int(W * 0.40), H - 150 - st.height - 10), st)
            lp = OUT / f"k{k:02d}.png"
            lay.save(lp)
            out.append((lp, sh.get("stk_t", 2.8), 0))

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
    # mặc định = TẤT CẢ ô trong plan (bản demo lấy len(SHOTS) — bảng đó đã bị xoá)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    OUT.mkdir(parents=True, exist_ok=True)
    plan = json.loads((VD / "plan27.json").read_text(encoding="utf-8"))
    tl_lines = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    chap = {c["num"]: (f'{c["num"]}. {c["chip_l"]} {c["chip_r"]}'.strip()
                       if c["chip_l"] else c["chip_r"]) for c in plan["chapters"]}
    shots = plan["shots"][:n] if n else plan["shots"]
    parts = []
    for k, s in enumerate(shots):
        # 🔴 dur = khoảng tới Ô SAU, KHÔNG phải (t1-t0). Giữa hai ô có khoảng lặng của giọng
        # đọc; lấy (t1-t0) thì mỗi ô hụt một ít và hình TRÔI DẦN so với tiếng — đo được ở bản
        # đầu: video 57,4s / tiếng 61,8s, frame cuối đen. Lỗi im lặng, chỉ lộ khi so duration.
        nxt = shots[k + 1]["t0"] if k + 1 < len(shots) else s["t1"]
        dur = nxt - s["t0"] + (XFADE if k < len(shots) - 1 else 0)
        sh = dict(TELOP[k]); sh["k"] = k
        sh.setdefault("size", 92); sh.setdefault("sub", [])
        sh["cap"] = cap_of(s["text"])
        bp, lays = layers(sh, chap.get(s["chap"], ""), k)
        caps = caption_layers(k, s["lines"], tl_lines, s["t0"])
        # ⚠️ PAN = 0: ảnh bất động (user chốt "để video tĩnh đi")
        chain = f"[0:v]scale={W}:{H}[bg0];"
        # 🦉 CÚ ĐỘNG — user: "video cú là video động mà". Nạp cả SEQUENCE owl_idle
        # (192 frame) và cho lặp; đây là lớp DUY NHẤT chạy liên tục trong khung.
        ins = ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(bp),
               "-stream_loop", "-1", "-framerate", str(FPS), "-t", f"{dur:.3f}",
               "-i", str(OWL_SEQ / "f_%04d.png")]
        subs = subscribe_layers()
        ow0 = Image.open(OWL_SEQ / "f_0001.png")
        ow_w = int(ow0.width * OWL_H / ow0.height)
        chain += (f"[1:v]scale={ow_w}:{OWL_H}[owl];"
                  f"[bg0][owl]overlay=x={W - ow_w - 56}:y={H - BOT_MASCOT - OWL_H}[sb0];")
        # ▶ SUBSCRIBE ĐỘNG — 4 trạng thái bật theo mod(t,4), khớp nhịp BrandOverlay
        wins = [(0.0, 2.6), (2.6, 3.0), (3.0, 3.25), (3.25, 4.0)]
        cur = "sb0"
        for j, (lp_s, (w0, w1)) in enumerate(zip(subs, wins)):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(lp_s)]
            nn = f"sb{j+1}"
            sidx = ins.count("-i") - 1
            chain += (f"[{cur}][{sidx}:v]overlay=0:0:"
                      f"enable='between(mod(t\,4)\,{w0}\,{w1})'[{nn}];")
            cur = nn
        for i, (lp, t0, slide) in enumerate(lays):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(lp)]  # input i+6 (0 nền·1 cú·2-5 subs)
            # ① fade alpha  ② x trượt dần về 0
            li = ins.count("-i") - 1
            chain += (f"[{li}:v]format=rgba,fade=in:st={t0:.2f}:d={FADE}:alpha=1[L{i}];")
            xs = (f"-{slide}*max(0\\,1-(t-{t0:.2f})/{FADE})" if slide else "0")
            chain += (f"[{cur}][L{i}]overlay=x='{xs}':y=0:"
                      f"enable='gte(t,{t0:.2f})'[v{i}];")
            cur = f"v{i}"
        for j, (lp_c, c0, c1) in enumerate(caps):
            ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", str(lp_c)]
            nn = f"cp{j}"
            # 🔴 index input phải ĐẾM THẬT: input cú có 8 phần tử (-stream_loop/-framerate)
            # còn input ảnh có 6 ⇒ chia cứng cho 6 là lệch.
            idx = ins.count("-i") - 1
            chain += (f"[{cur}][{idx}:v]overlay=0:0:"
                      f"enable='between(t\,{c0:.2f}\,{c1:.2f})'[{nn}];")
            cur = nn

        mp = OUT / f"p{k:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins,
                        "-filter_complex", chain.rstrip(";"), "-map", f"[{cur}]",
                        "-r", str(FPS), "-pix_fmt", "yuv420p", "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "18", str(mp)], check=True)
        parts.append((mp, nxt - s["t0"]))
        print(f"  ô {k} {nxt-s['t0']:>5.1f}s  {len(lays)} lớp  tĩnh(pan=0)")

    # ── ④ nối bằng dissolve xfade
    cur_lbl, ins, chain, off = "0:v", [], "", 0.0
    for i, (mp, d0) in enumerate(parts):
        ins += ["-i", str(mp)]
    for i in range(1, len(parts)):
        off += parts[i - 1][1]      # = mốc bắt đầu ô i; mỗi clip đã dài thêm XFADE nên vừa khít
        nxt = f"x{i}"
        chain += (f"[{cur_lbl}][{i}:v]xfade=transition=fade:duration={XFADE}:"
                  f"offset={off:.3f}[{nxt}];")
        cur_lbl = nxt
    sil = OUT / "_v.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", chain.rstrip(";"),
                    "-map", f"[{cur_lbl}]", "-r", str(FPS), "-pix_fmt", "yuv420p",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(sil)], check=True)
    fin = VD / "27_nenkin-tsuchisho-nai-okane-5tsu.mp4"
    t_end = shots[-1]["t1"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(sil), "-i", str(VD / "voice_full.wav"),
                    "-t", f"{t_end:.3f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-af", "loudnorm=I=-14:TP=-4:LRA=7", "-shortest", str(fin)], check=True)
    print(f"\n→ {fin}  ({t_end:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
