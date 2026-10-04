# -*- coding: utf-8 -*-
r"""make_fb19ch3.py — DEMO full-bleed kieu showcase-football cho CHUONG 3 video 19.

VI SAO CO FILE NAY (user chot 2026-09-02): *"toi muon lam video dang nay ma
E:\vox-director\assets\showcase-football.mp4"* + chon **Remotion/PIL ve de chu**
(khong bake kanji vao anh) + chon **thu 1 doan 60-90s truoc**.

🔴 DOC TRUOC KHI SUA — day la lan THU HAI cua duong nay:
Ban dau 2026-08-26 (`06_VIDEO/demo17fb/`) da bi BO. Nhung soi lai 5 frame cua no
o t=3/12/22/32/42 thi ca 5 la CUNG MOT tam anh, cung mot headline => no la
slideshow dung hinh 42s, khong phai showcase. Showcase co 12 shot/63s + chuyen
dong that + chat lieu giay giau. Ba thu do gio da co:
  - 74 anh (san nhip 9s, chot 2026-08-31 — SAU ngay bo full-bleed)
  - anh la paper-collage newsprint that (soi 2026-09-02, rat giau chat lieu)
  - bo prompt i2v da soan (`out/nenkin-19/motion.txt` cua vox-director)
=> Cai bi bo hoi do la BAN THI HANH, khong phai y tuong. Nhung CAI GIA ① cua
   CLAUDE.md:177 (cast モニター mat mat = ban sac kenh) VAN CON THAT — chuong 3
   duoc chon vi no la tinh vat, 0 khuon mat, nen khong mat cast nao.

CHON CHUONG 3 (八十四万円, L=36..47, 258.99-338.66s = 79.7s) vi:
  ① la PEAK cua bai — thay style o cho dat nhat
  ② 8 anh cua no co 0 KHUON MAT => banner dot len dinh khung khong che mat ai
     (day la cai gia ③ cua CLAUDE.md:178, ne duoc o dung chuong nay)
  ③ nen anh doi mau theo beat (kem -> do -> do) giong showcase

CHAY:  python tools/make_fb19ch3.py           # dung frame + ASS + wrapper
       cmd //c 06_VIDEO/_fb19ch3/run_fb.cmd   # render (chay NEN)
"""
import io
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_fullbleed import CREAM, INK, RED, W, H, headline, scraps  # noqa: E402
from PIL import Image  # noqa: E402
import random  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "19_kounenrei-koyou-keizoku-kyufu"
SRC = PROJ / "06_VIDEO" / STEM
CARD = SRC / "photocard"
OUT = PROJ / "06_VIDEO" / "_fb19ch3"
L0, L1 = 36, 47            # chuong 3: tu dong 36 den 47 cua timeline

# ── SPEC 10 SHOT ─────────────────────────────────────────────────────────────
# crop: (cx, cy) tam vung cat, 0..1 — de lay 2 shot khac nhau tu CUNG mot anh
#       (chinh la ky thuat cua showcase: shot a WIDE, shot b DETAIL)
# zoom: he so phong khi cat (1.0 = full-bleed ca anh · 1.6 = can vao)
# head: headline JP tren banner giay xe. None = shot cut-in, KHONG headline
#       (dung luat showcase: headline chi o shot wide, 1 cai moi beat)
SPEC = [
 # beat A — ここからが本題 (L=36,37)
 dict(src="card_19_hondai",     cx=.50, cy=.50, zoom=1.00, tone="cream",
      head="ここからが、本題です", sub=None,             lines=(36, 36), seed=11),
 dict(src="card_19_hondai_b",   cx=.50, cy=.52, zoom=1.25, tone=None,
      head=None, sub=None,                              lines=(37, 37), seed=12),
 # beat B — 原典・厚労省 (L=38,39) — CHE DOI: ban gop 13,5s vuot tran 9s
 dict(src="card_19_hondai_b",   cx=.42, cy=.46, zoom=1.55, tone="red",
      head="厚生労働省のページ", sub="令和七年四月一日以降",  lines=(38, 38), seed=13),
 dict(src="card_19_hondai_b",   cx=.62, cy=.62, zoom=1.85, tone=None,
      head=None, sub=None,                              lines=(39, 39), seed=23),
 # beat C — 率の比較 (L=40,41)
 dict(src="card_19_84man",      cx=.55, cy=.55, zoom=1.30, tone="mustard",
      head="十五から、十へ", sub=None,                    lines=(40, 40), seed=14),
 dict(src="card_19_84man",      cx=.62, cy=.58, zoom=1.75, tone=None,
      head=None, sub=None,                              lines=(41, 41), seed=15),
 # beat D — 八十四万円  ⭐ PEAK (L=42,43)
 dict(src="card_19_84man_b",    cx=.50, cy=.50, zoom=1.00, tone="red",
      head="五年で、八十四万円", sub=None,                 lines=(42, 42), seed=16),
 dict(src="card_19_84man_b",    cx=.44, cy=.48, zoom=1.70, tone=None,
      head=None, sub=None,                              lines=(43, 43), seed=17),
 # beat E — 分かれ目は誕生日 (L=44,45) — CHE DOI: ban gop 11,6s vuot tran 9s
 dict(src="card_19_tanjoubi",   cx=.50, cy=.52, zoom=1.00, tone="cream",
      head="分かれ目は、誕生日", sub=None,                 lines=(44, 44), seed=18),
 dict(src="card_19_tanjoubi",   cx=.42, cy=.72, zoom=1.70, tone=None,
      head=None, sub=None,                              lines=(45, 45), seed=24),
 # ⛔ card_19_tanjoubi_b (macro o khoanh do) DA BO khoi bo nay: soi frame render
 #    2026-09-02 -> khung TRONG HOAC, o do nho giua to lich trang. Anh macro cuc
 #    can khong ganh duoc full-bleed 16:9 — dung cho khuon card thi vua.
 dict(src="card_19_tanjoubi_c", cx=.50, cy=.58, zoom=1.15, tone=None,
      head=None, sub=None,                              lines=(46, 46), seed=19),
 # beat F — 一日の違い (L=47)
 # ⛔ card_19_tanjoubi_d DA BO: thu 2 crop (cy .55 roi .70) van TRONG nua duoi —
 #    anh do la "but do nam mot minh canh lich, quiet aftermath", chu the nho +
 #    nen trong nhieu => ban chat khong ganh duoc full-bleed. Cung ket luan voi
 #    tanjoubi_b o tren: anh cho khuon CARD khong tu dong dung duoc cho full-bleed.
 # Thay bang card_19_wariai (can dia lech) — hop nghia cau ket "mot ngay khac
 # biet lam lech ca can", va la anh MOI nen khong lap hinh trong video
 # (feedback_slide_khong_trung_anh_trong_video).
 dict(src="card_19_wariai",     cx=.50, cy=.52, zoom=1.05, tone="red",
      head="一日の違いで", sub=None,                      lines=(47, 47), seed=20),
]


def crop_fb(im, cx, cy, zoom):
    """Cover-crop 16:9 quanh tam (cx,cy) voi he so phong `zoom`, ra 1920x1080."""
    sc = max(W / im.width, H / im.height) * zoom
    im2 = im.resize((int(im.width * sc + .5), int(im.height * sc + .5)), Image.LANCZOS)
    x = int(im2.width * cx - W / 2)
    y = int(im2.height * cy - H / 2)
    x = max(0, min(x, im2.width - W))
    y = max(0, min(y, im2.height - H))
    return im2.crop((x, y, x + W, y + H))


def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build():
    tl = json.loads((SRC / "timeline.json").read_text(encoding="utf-8"))["lines"]
    t0 = tl[L0]["start"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "frames").mkdir(exist_ok=True)

    # ── 1. frame full-bleed ────────────────────────────────────────────────
    segs = []
    for i, s in enumerate(SPEC):
        p = CARD / f"{s['src']}.png"
        if not p.exists():
            print(f"🔴 THIEU {p.name}"); return 1
        im = crop_fb(Image.open(p).convert("RGB"), s["cx"], s["cy"], s["zoom"]).convert("RGBA")
        rng = random.Random(s["seed"])
        scraps(im, rng, n=10)
        if s["head"]:
            headline(im, s["head"], rng, tone=s["tone"], sub=s.get("sub"))
        f = OUT / "frames" / f"fb_{i:02d}.png"
        im.convert("RGB").save(f)
        a = tl[s["lines"][0]]["start"] - t0
        b = tl[s["lines"][1]]["end"] - t0
        segs.append(dict(f=f, a=a, b=b, d=round(b - a, 3)))
        print(f"   fb_{i:02d}  {s['src']:<24} zoom{s['zoom']:.2f}  "
              f"{a:6.2f}-{b:6.2f} ({b-a:5.2f}s)  {s['head'] or '(cut-in)'}")

    # gian khe: shot ke tiep bat dau ngay sau shot truoc (khong de ho)
    for i in range(len(segs) - 1):
        segs[i]["b"] = segs[i + 1]["a"]
        segs[i]["d"] = round(segs[i]["b"] - segs[i]["a"], 3)
    segs[-1]["b"] = tl[L1]["end"] - t0 + .6
    segs[-1]["d"] = round(segs[-1]["b"] - segs[-1]["a"], 3)
    total = segs[-1]["b"]

    # ── 2. phu de ASS — chu TO vien do canh giua, kieu showcase ───────────
    #    (khac han demo17fb: cho la dai den mong chu nho o day)
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080",
           "WrapStyle: 2", "", "[V4+ Styles]",
           "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BackColour,"
           "Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,"
           "Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
           # trang + vien DO day + bong.
           # 🔴 58 -> 76: soi frame render 2026-09-02, FontSize 58 cho ra glyph chi
           #    ~3% chieu cao khung (em size != chieu cao glyph; chu JP chiem ~70% em).
           #    Tep 45-70 tren full-bleed thi co chu la thu CHINH giu kha nang doc
           #    (`audience-45plus.md` §3.1 — sau khi bo nen duc). Margin 120 -> 88 de
           #    cau JP full-width khoi wrap qua 2 dong.
           "Style: fb,Noto Sans JP,76,&H00FFFFFF,&H001F20A8,&H64000000,"
           "-1,0,0,0,100,100,0.6,0,1,6,4,2,88,88,92,1", "", "[Events]",
           "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text"]
    n_cap = 0
    for i in range(L0, L1 + 1):
        ln = tl[i]
        txt = ln["text"].replace("\n", "")
        # <=2 dong (feedback_phu_de_toi_da_2_dong). NGUONG PHAI DOI THEO CO CHU:
        # be rong kha dung = 1920 - 88*2 = 1744px; chu JP full-width ~= FontSize
        # px/ky => 1744/76 ~= 22 ky/dong. De nguong 30 nhu ban FontSize 58 thi
        # ffmpeg tu wrap thanh 3 dong.
        if len(txt) > 22:
            cut = txt.rfind("、", 0, 24) + 1 or txt.rfind("。", 0, 24) + 1 or len(txt) // 2
            txt = txt[:cut] + r"\N" + txt[cut:]
        ass.append(f"Dialogue: 0,{ass_time(ln['start']-t0)},{ass_time(ln['end']-t0)},"
                   f"fb,,0,0,0,,{txt}")
        n_cap += 1
    (OUT / "subs.ass").write_text("\n".join(ass) + "\n", encoding="utf-8")

    # ── 3. concat list + wrapper ──────────────────────────────────────────
    cl = []
    for s in segs:
        cl.append(f"file '{s['f'].as_posix()}'")
        cl.append(f"duration {s['d']:.3f}")
    cl.append(f"file '{segs[-1]['f'].as_posix()}'")
    (OUT / "concat.txt").write_text("\n".join(cl) + "\n", encoding="utf-8")

    cmd = f"""@echo off
chcp 65001 >nul
cd /d {PROJ}
set VD=06_VIDEO\\_fb19ch3
set SRC=06_VIDEO\\{STEM}
ffmpeg -y -i "%SRC%\\voice_full.wav" -ss {t0:.3f} -t {total:.3f} ^
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" "%VD%\\voice.wav" > "%VD%\\render.log" 2>&1
>> "%VD%\\render.log" echo VOICE_EXIT=%ERRORLEVEL%
ffmpeg -y -f concat -safe 0 -i "%VD%\\concat.txt" -i "%VD%\\voice.wav" ^
  -vf "fps=30,scale=1920:1080,subtitles='%VD:\\=/%/subs.ass'" ^
  -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p ^
  -c:a aac -b:a 160k -shortest "%VD%\\demo_fb19ch3.mp4" >> "%VD%\\render.log" 2>&1
>> "%VD%\\render.log" echo EXITCODE=%ERRORLEVEL%
"""
    (OUT / "run_fb.cmd").write_bytes(cmd.replace("\n", "\r\n").encode("ascii"))

    print(f"\n✓ {len(segs)} frame · phu de {n_cap} dong · tong {total:.1f}s")
    print(f"  -> {OUT}")
    print(f"  render:  cmd //c \"{OUT / 'run_fb.cmd'}\"   (CHAY NEN)")
    return 0


if __name__ == "__main__":
    sys.exit(build())
