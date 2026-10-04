# -*- coding: utf-8 -*-
r"""thumb_prompts_20_21.py — prompt gen THUMBNAIL A/B 3x3 cho video 20 va 21.

QUY TRINH 5 BUOC cua `ab-3title-3thumb.md` §3.1 — da chay du, ghi so lieu lai:

BUOC 1 — KHUON LAY TU ANH DA LEN SONG, khong tu tai lieu:
  `07_UPLOADED/19_kounenrei-koyou-keizoku-kyufu/_upload/thumbnail.png`

BUOC 2 — DO BANG MAY (1376x768):
  · BANNER navy tren : cao **19,1%** khung (147px) — chip 対象, chu TRANG
  · HERO vang cam    : cao 15,9% nhung **RONG 63,4%** khung
    ⭐ dung phat hien §3.1 buoc 2: thu mua duoc legibility la **BE NGANG**,
      khong phai chieu cao (13 ca do duoc deu 20–31% chieu cao ma van doc ro
      o 120px — `audience-45plus.md` §6.10).
  · RUY-BANG do day  : bat dau tu **mep trai (0%)**, chu trang
  · NGUOI cat-nen    : ben PHAI, rong **37%** khung, cao tu duoi banner xuong day

BUOC 5 — CHU QUA 2 PHEP DO (Trends YouTube JP 30 ngay, do 2026-09-06 bang pytrends):
  video 21: 年金 税金 **25,5** ⭐ · 確定申告 年金 17,8 · 源泉徴収 16,0 ·
            扶養親族等申告書 **3,5** · 公的年金等控除 0
  video 20: 遺族年金 **16,3** ⭐ · 遺族厚生年金 3,8 · 遺族年金 手続き 2,7 ·
            年金 妻 0,4 · 遺族年金 いくら 0
  ⇒ 扶養親族等申告書 la CHU THE cua bai 21 nhung do duoc qua thap => day no vao
    **HINH** (to giay trong tay), con **CHU** thi dung tu do duoc cao nhat.
    Dung khuon nenkin 10 (`ab-3title-3thumb.md` §3.1 buoc 5: vat nhan dien di
    duong hinh, keyword di duong chu).

⚠️ RANG BUOC BAT BUOC:
  · **TEXT o khoi thu 2** (trong 15% dau prompt) — dat cuoi thi model nuot chu
    (chouhen 21). Do bang may o cuoi file nay.
  · tran **4 DONG chu** cho anh AI (5 dong gan nhu chac meo kanji)
  · chua trong **goc duoi-PHAI** (YouTube dong timestamp)
  · `no watermark` + cau chat luong chu Nhat
  · nenkin **MIEN gate mat nguoi** (`audience-45plus.md` §1.2) nhung khuon dang
    chay CO nguoi => giu, vi day la bien "baseline" cua T1.

BA BAN A/B — moi ban doi DUNG MOT BIEN (`ab-3title-3thumb.md` §3):
  T1 = baseline khuon TELOP (banner navy + hero vang + ruy-bang do + nguoi phai)
  T2 = doi MOT bien HINH, **giu nguyen chu** (bo nguoi, thay bang can canh giay
       to + tay; nen doi tong)
  T3 = doi LAYOUT + thu triet ly "thumbnail KHONG lap title"
       (`youtube-suggested-growth.md` §6 muc 1 — user chot 2026-08-21 thu qua T3)

CHAY:  python tools/thumb_prompts_20_21.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and "
           "legible. Keep the very bottom-right corner free of text. "
           "No watermark, no logo, no signature, no additional text. --ar 16:9")

VIDEOS = {
 "20_izoku-nenkin-yonbunno-san": dict(
   name="video 20 遺族年金・四分の三の誤解",
   kw="遺族年金 (16,3 — cao nhat ro)",
   T1=dict(
     text=[("top banner, white on navy", "遺族年金を受け取る方へ"),
           ("second line, black with 65 in red", "65歳で減ります"),
           ("HERO, largest and widest, golden-orange", "年63万円"),
           ("bottom ribbon, white on deep red", "四分の三は誤解")],
     layout=("The navy top banner runs the full width and is one fifth of the "
             "frame tall. The golden-orange hero line sits in the middle of the "
             "left two thirds, is both the tallest and the widest text on the "
             "image and spans about two thirds of the frame width, with a "
             "hand-drawn red ellipse looping round it and a curved red arrow "
             "rising to it from below. The deep red ribbon sits along the "
             "bottom-left, tilted very slightly, starting hard against the left "
             "edge."),
     bg=("Cream paper with a faint grid, flat and evenly lit, no shadows."),
     person=("RIGHT THIRD: a Japanese woman of about 68, short white hair, "
             "wearing a soft lilac cardigan over a white blouse, cut out with a "
             "clean white outline, standing from just below the banner down to "
             "the bottom edge, holding an official notice in both hands and "
             "looking down at it with a worried, disbelieving expression."),
     bottom=("BOTTOM-LEFT PROP: a pale green folded pension notice and a plain "
             "white window envelope lying at a slight angle, with fine printed "
             "rule lines and empty boxes and no characters written anywhere.")),
   T2=dict(
     text=[("top banner, white on navy", "遺族年金を受け取る方へ"),
           ("second line, black with 65 in red", "65歳で減ります"),
           ("HERO, largest and widest, golden-orange", "年63万円"),
           ("bottom ribbon, white on deep red", "四分の三は誤解")],
     layout=("Same layout as a broadcast telop: navy banner across the top one "
             "fifth, golden-orange hero line in the middle spanning about two "
             "thirds of the width as the tallest and widest text, red ellipse "
             "and curved red arrow around it, deep red ribbon along the "
             "bottom-left from the left edge."),
     bg=("A cool pale blue-grey paper ground with a faint grid, flat and evenly "
         "lit, no shadows."),
     person=("RIGHT THIRD: no person. Instead a close pair of older hands "
             "holding a pale green pension notice up at an angle, the paper "
             "large and clearly lit, fine printed rule lines and empty boxes "
             "and no characters written anywhere."),
     bottom=("BOTTOM-LEFT PROP: a plain white window envelope and a stubby "
             "pencil lying at a slight angle.")),
   T3=dict(
     text=[("top banner, white on navy", "65歳の誕生月"),
           ("HERO, largest and widest, golden-orange", "減っていた"),
           ("bottom ribbon, white on deep red", "知らないと損します")],
     layout=("The navy top banner runs the full width and is one sixth of the "
             "frame tall. The face is the centre of the image: a large close "
             "portrait fills the left two thirds from just under the banner to "
             "the bottom edge. The golden-orange hero line sits across the "
             "lower middle, tallest and widest text, spanning about half the "
             "width, with a hand-drawn red ellipse round it. The deep red "
             "ribbon sits along the very bottom-left from the left edge."),
     bg=("A softly blurred ordinary Japanese kitchen, warm and plain, flat "
         "lighting, no strong shadows."),
     person=("LEFT TWO THIRDS: a close portrait of a Japanese woman of about "
             "68 with short white hair in a lilac cardigan, seen from the chest "
             "up, eyes wide and mouth slightly open in disbelief, one hand "
             "half-raised toward her mouth, cut out with a clean white outline "
             "and cropped by the bottom edge at the chest."),
     bottom=("RIGHT SIDE: a pale green pension notice held up beside her at an "
             "angle, fine printed rule lines and empty boxes and no characters "
             "written anywhere.")),
 ),
 "21_fuyo-shinkokusho-205man": dict(
   name="video 21 扶養親族等申告書・二百五万円",
   kw="年金 税金 (25,5 — cao nhat) · 確定申告 年金 (17,8)",
   T1=dict(
     text=[("top banner, white on navy", "年金に税金がかかる方へ"),
           ("second line, black with the old figure struck through in red",
            "158万円は古い"),
           ("HERO, largest and widest, golden-orange", "205万円"),
           ("bottom ribbon, white on deep red", "出さないと年2万円")],
     layout=("The navy top banner runs the full width and is one fifth of the "
             "frame tall. The golden-orange hero line sits in the middle of the "
             "left two thirds, is both the tallest and the widest text on the "
             "image and spans about two thirds of the frame width, with a "
             "hand-drawn red ellipse looping round it and a curved red arrow "
             "rising to it from the struck-through line above. The deep red "
             "ribbon sits along the bottom-left, tilted very slightly, starting "
             "hard against the left edge."),
     bg=("Cream paper with a faint grid, flat and evenly lit, no shadows."),
     person=("RIGHT THIRD: a Japanese man of about 66, short grey hair, thin "
             "rectangular reading glasses, wearing an olive-grey cardigan over "
             "a pale checked shirt, cut out with a clean white outline, "
             "standing from just below the banner down to the bottom edge, "
             "holding a cream declaration form in both hands and looking down "
             "at it with a puzzled, slightly worried expression."),
     bottom=("BOTTOM-LEFT PROP: a plain white window envelope with a pale blue "
             "printed band, and a cream form beside it at a slight angle, with "
             "fine printed rule lines and a column of empty boxes and no "
             "characters written anywhere.")),
   T2=dict(
     text=[("top banner, white on navy", "年金に税金がかかる方へ"),
           ("second line, black with the old figure struck through in red",
            "158万円は古い"),
           ("HERO, largest and widest, golden-orange", "205万円"),
           ("bottom ribbon, white on deep red", "出さないと年2万円")],
     layout=("Same layout as a broadcast telop: navy banner across the top one "
             "fifth, golden-orange hero line in the middle spanning about two "
             "thirds of the width as the tallest and widest text, red ellipse "
             "and curved red arrow around it, deep red ribbon along the "
             "bottom-left from the left edge."),
     bg=("A warm pale wood desktop seen from straight above, flat and evenly "
         "lit, no strong shadows."),
     person=("RIGHT THIRD: no person. Instead a close pair of older hands "
             "drawing a cream declaration form halfway out of a white window "
             "envelope, the form large and clearly lit, fine printed rule lines "
             "and a column of empty boxes and no characters written anywhere."),
     bottom=("BOTTOM-LEFT PROP: a slim red ballpoint and a stubby wooden pencil "
             "lying at a slight angle.")),
   T3=dict(
     text=[("top banner, white on navy", "この秋、届く紙"),
           ("HERO, largest and widest, golden-orange", "出さないと損"),
           ("bottom ribbon, white on deep red", "期限は紙の上に")],
     layout=("The navy top banner runs the full width and is one sixth of the "
             "frame tall. The face is the centre of the image: a large close "
             "portrait fills the left two thirds from just under the banner to "
             "the bottom edge. The golden-orange hero line sits across the "
             "lower middle, tallest and widest text, spanning about half the "
             "width, with a hand-drawn red ellipse round it. The deep red "
             "ribbon sits along the very bottom-left from the left edge."),
     bg=("A softly blurred ordinary Japanese kitchen, warm and plain, flat "
         "lighting, no strong shadows."),
     person=("LEFT TWO THIRDS: a close portrait of a Japanese man of about 66 "
             "with short grey hair and thin rectangular reading glasses, in an "
             "olive-grey cardigan, seen from the chest up, brows drawn together "
             "and lips pressed as he looks down at a form, cut out with a clean "
             "white outline and cropped by the bottom edge at the chest."),
     bottom=("RIGHT SIDE: a cream declaration form held up beside him at an "
             "angle, fine printed rule lines and a column of empty boxes and no "
             "characters written anywhere.")),
 ),
}

HEAD = ("A 16:9 Japanese YouTube thumbnail for a calm pension-information "
        "channel, in the style of a broadcast news telop, with bold Japanese "
        "text burned into the image.")


def build(v):
    lines = ", ".join(f'{role}: {txt}' for role, txt in v["text"])
    n = len(v["text"])
    text_block = (f"TEXT, exactly these {n} blocks and nothing else: {lines}.")
    return (f"{HEAD} {text_block} LAYOUT: {v['layout']} BACKGROUND: {v['bg']} "
            f"{v['person']} {v['bottom']} {QUALITY}")


def plate(v):
    return (f"{HEAD.replace(', with bold Japanese text burned into the image','')} "
            f"LAYOUT: {v['layout']} BACKGROUND: {v['bg']} {v['person']} "
            f"{v['bottom']} A clean empty plate with no lettering anywhere, "
            f"leaving the banner strip, the middle band and the bottom ribbon "
            f"clear for text to be added later. No watermark. --ar 16:9")


def main():
    for stem, V in VIDEOS.items():
        vd = os.path.join(PROJ, "06_VIDEO", stem)
        os.makedirs(vd, exist_ok=True)
        flow, plates, ten, blocks = [], [], [], []
        blocks.append(f"# THUMBNAIL A/B 3x3 — {V['name']}\n\n"
                      f"- keyword do duoc (Trends YouTube JP 30 ngay, 2026-09-06): "
                      f"**{V['kw']}**\n"
                      f"- khuon do tu anh da len song (video 19): banner navy "
                      f"**19,1%** khung · hero vang **rong 63,4%** · nguoi **37%** "
                      f"ben phai · ruy-bang do tu mep trai\n"
                      f"- ten anh dich: `thumb_T1_*.png` / `_T2_` / `_T3_`\n")
        for tag in ("T1", "T2", "T3"):
            v = V[tag]
            p = " ".join(build(v).split())
            flow.append(p)
            plates.append(" ".join(plate(v).split()))
            ten.append(f"{tag}\tthumb_{tag}_{stem.split('_',1)[1][:22]}.png")
            role = {"T1": "baseline khuon TELOP",
                    "T2": "doi MOT bien hinh (bo nguoi + doi tong nen), GIU chu",
                    "T3": "doi LAYOUT (mat to) + thu 'khong lap title'"}[tag]
            blocks.append(f"\n## {tag} — {role}\n\n**CHU ({len(v['text'])} dong):**\n"
                          + "\n".join(f"- `{t}` — {r}" for r, t in v["text"])
                          + f"\n\n**PROMPT ({len(p)} ky, TEXT o "
                            f"{p.find('TEXT, exactly')*100//len(p)}%):**\n```\n{p}\n```\n")

        def w(n, t):
            io.open(os.path.join(vd, n), "w", encoding="utf-8",
                    newline="\n").write(t)
        w("thumb_prompts_FLOW.txt", "\n".join(flow) + "\n")
        w("thumb_prompts_PLATE.txt", "\n".join(plates) + "\n")
        w("thumb_prompts_TENFILE.txt", "ban\tten file dich\n" + "\n".join(ten) + "\n")
        w("thumb_prompts_BLOCKS.md", "\n".join(blocks) + "\n")

        print(f"\n→ 06_VIDEO/{stem}/")
        print(f"   thumb_prompts_FLOW.txt   3 prompt "
              f"({min(len(x) for x in flow)}–{max(len(x) for x in flow)} ky)")
        print(f"   thumb_prompts_PLATE.txt  3 plate KHONG chu (duong lui)")
        print(f"   thumb_prompts_TENFILE.txt · thumb_prompts_BLOCKS.md")
        bad = False
        for tag, p in zip(("T1", "T2", "T3"), flow):
            pos = p.find("TEXT, exactly") * 100 // len(p)
            nline = p.count("line") + p.count("banner,") + p.count("ribbon,")
            flag = "🔴" if pos > 15 else "✅"
            if pos > 15:
                bad = True
            print(f"   {tag}: {len(p):5d} ky · TEXT @ {pos:2d}% {flag}"
                  f" · {len(VIDEOS[stem][tag]['text'])} dong chu")
            if len(p) > 1500:
                print(f"       ⚠️ dai {len(p)} > 1.500 (gate phu, `ab-3title` §3.1)")
        if bad:
            print("   🔴 GATE CHINH: TEXT phai nam trong 15% DAU prompt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
