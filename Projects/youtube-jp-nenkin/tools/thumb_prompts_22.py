# -*- coding: utf-8 -*-
r"""thumb_prompts_22.py — prompt gen THUMBNAIL A/B 3x3 cho video 22 (未支給年金・36万円).

Copy cau truc tu `tools/thumb_prompts_20_21.py` (luat `ab-3title-3thumb.md` §3 muc 8:
ken nao da gen duoc mot ban chu Nhat dung net thi ban do la khuon).

QUY TRINH 5 BUOC cua `ab-3title-3thumb.md` §3.1 — da chay du:

BUOC 1 — KHUON LAY TU ANH DA LEN SONG, KHONG tu tai lieu:
  `07_UPLOADED/21_fuyo-shinkokusho-205man/_upload/thumbnail{,_T2,_T3}.png` (len song 09-07).
  🔴 Tai lieu cua video 21 ghi T2/T3 la "khuon カメ先生, nen navy tron, 0 nguoi, chu do
     `make_thumb_kame.py` ve". ANH THAT thi khac: **ca 3 ban deu la TELOP chu BAKE,
     nen sang, CO nguoi cat-nen ben phai, va co them mot DAI DO DOC ben trai**. Khong
     tool nao trong repo ve duoc dai doc co chu doc do (grep `158万円は古い` chi ra
     make_thumb_kame + file prompt). ⇒ tin ANH.

BUOC 2 — DO BANG MAY tren 3 anh live (1376x768, `scratchpad/m21b.py`):
  |        | dai DOC trai | banner tren | HERO cao | HERO rong | bang day |
  | T1 205万円 |  4,8% | 19,7% |  16,1% | 62,4% | 17,4% |
  | T2        |  3,9% | 16,5% |  17,3% | 55,5% | 13,9% |
  | T3 損します |  4,4% | 14,1% | **47,0%** | **81,8%** | **0%** |
  ⭐ T3 la ban AI-bake DAU TIEN cua kenh **QUA gate 2** (`audience-45plus.md` §1 gate 2,
    >=33,3% chieu cao) — va co che ro rang: **hero cao len la nho BO BANG DAY** (T3 khong
    co bang day, chi 1 dong tren hero). Them vao bang ca do §6.10.
  ⇒ T1/T2 giu bang day (baseline) · T3 bo bang day de hero an tron khe doc.

BUOC 5 — CHU QUA 2 PHEP DO (Trends YouTube JP 30 ngay, pytrends, do 2026-09-11):
  年金 **~73,8** ⭐ (quy ve cung thang qua anchor 遺族年金) · 遺族年金 35,1 ·
  未支給年金 **0,3** · 年金 死亡 手続き 0,4 · 年金 死亡 0,5 · 死亡届 0 ·
  未支給年金 請求 0 · 年金 返還 0 · 年金 いつまで 0 · 相続 年金 0,3
  Web 12 thang (doi chieu, loc nhieu mau nho): 未支給年金 5,7 · 死亡届 11,6 · 遺族年金 57,8
  ⇒ **未支給年金 la CHU THE cua bai nhung do gan nhu 0** => day no xuong **HINH**
    (thong ke 2 dong giong nhau, khoanh do) va cho **年金** (tu duy nhat co volume that)
    len BANNER. Dung khuon nenkin 10 + video 21.
  ⛔ **KHONG dat 遺族年金 len thumbnail** du no do 35,1: tu do **KHONG XUAT HIEN**
    trong video 22 (grep: 0 lan) => sai intent + misleading metadata
    (`youtube-upload-seo.md` §0.5 muc 4 + `youtube-compliance.md` muc 4).

GATE CHU (`audience-45plus.md` §1 gate 7 — che anh di van biet bai noi gi):
  ① ve cai gi  : 年金 (banner) + 36万円 + 通帳 trong hinh
  ② chuyen gi  : 片方は返します  (T3: 返す分がある)
  ③ phai lam gi: 請求が必要      (T3: 5年で消えます)

BA BAN A/B — moi ban doi DUNG MOT BIEN (`ab-3title-3thumb.md` §3):
  T1 = baseline khuon TELOP live cua kenh (dai doc + banner + hero + bang day + nguoi phai)
  T2 = doi MOT bien HINH, **chu giong het T1 tung ky tu** (bo nguoi -> can canh tay cam
       thong ke; doi tong nen sang-lanh)
  T3 = doi LAYOUT (mat to + hero khong lo, bo bang day) + thu triet ly "thumbnail KHONG
       lap title" (`youtube-suggested-growth.md` §6 muc 1 — user chot thu qua T3)

RANG BUOC (da kiem bang may o cuoi file):
  · TEXT o khoi thu 2, trong **15% dau prompt** · tran ~1.500 ky
  · tran **4 DONG chu** cho anh AI · chua trong **goc duoi-PHAI** (timestamp YouTube)
  · `no watermark` + cau chat luong chu Nhat · giay/thong ke trong hinh **de tron**
    (`no characters written anywhere` — chu Nhat AI gen la nat net)

CHAY:  python tools/thumb_prompts_22.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "22_mishikyu-nenkin-36man"

QUALITY = ("Text must be perfectly formed Japanese characters, crisp and "
           "legible. Keep the very bottom-right corner free of text. "
           "No watermark, no logo, no signature, no additional text. --ar 16:9")

HEAD = ("A 16:9 Japanese YouTube thumbnail for a calm pension-information "
        "channel, in the style of a broadcast news telop, with bold Japanese "
        "text burned into the image.")

# ── chu: T1 va T2 GIONG HET NHAU tung ky tu (bien thu cua T2 la HINH) ───────
TEXT_12 = [("narrow vertical red strip down the left edge, white characters "
            "stacked one under another", "請求が必要"),
           ("top banner, white on bright red", "年金を受け取るご家族へ"),
           ("HERO, largest and widest, golden-orange with a black outline and "
            "a white halo", "36万円"),
           ("bottom band, white on deep red", "片方は返します")]

TEXT_3 = [("narrow vertical red strip down the left edge, white characters "
           "stacked one under another", "5年で消えます"),
          ("top banner, white on bright red", "亡くなった月の年金"),
          ("HERO, largest and widest, golden-orange with a black outline and "
           "a white halo", "返す分がある")]

V = {
 "T1": dict(
   role="baseline khuon TELOP live cua kenh",
   text=TEXT_12,
   layout=("The bright red vertical strip runs the full height of the left "
           "edge and is about one twentieth of the frame wide. The red top "
           "banner runs from that strip to the right edge and is one fifth of "
           "the frame tall. The golden-orange hero line sits in the middle of "
           "the left two thirds, is both the tallest and the widest text on "
           "the image and spans about two thirds of the frame width, with a "
           "hand-drawn red ellipse looping round it. The deep red bottom band "
           "is one sixth of the frame tall, sits along the bottom-left and is "
           "tilted very slightly."),
   bg=("A softly blurred ordinary Japanese living room, warm cream walls and "
       "pale wood, bright and evenly lit, no strong shadows."),
   person=("RIGHT THIRD: a Japanese woman of about 70, short white hair, in "
           "a soft grey-blue cardigan, cut out with a clean white outline, "
           "standing from just below the banner and cropped by the bottom "
           "edge at the hip, holding an open bank passbook in both hands and "
           "looking down at it, puzzled and worried."),
   bottom=("BOTTOM-LEFT PROP: a plain white window envelope at a slight "
           "angle, fine printed rule lines and empty boxes and no characters "
           "written anywhere.")),
 "T2": dict(
   role="doi MOT bien HINH (bo nguoi + doi tong nen), GIU nguyen chu",
   text=TEXT_12,
   layout=("Same broadcast telop layout: bright red vertical strip down the "
           "full height of the left edge about one twentieth of the frame "
           "wide, red banner across the top one fifth, golden-orange hero "
           "line in the middle spanning about two thirds of the width as the "
           "tallest and widest text with a hand-drawn red ellipse round it, "
           "deep red bottom band one sixth of the frame tall along the "
           "bottom-left."),
   bg=("A cool pale blue-grey desktop seen from straight above, flat and "
       "evenly lit, no strong shadows."),
   person=("RIGHT THIRD: no person. Instead a close pair of older hands "
           "holding an open bank passbook up at an angle, the passbook large "
           "and clearly lit, two of its printed rows circled by hand in red "
           "marker, fine printed rule lines and empty boxes and no characters "
           "written anywhere."),
   bottom=("BOTTOM-LEFT PROP: a slim red marker pen and a plain white window "
           "envelope lying at a slight angle.")),
 "T3": dict(
   role="doi LAYOUT (mat to, hero khong lo, BO bang day) + thu 'khong lap title'",
   text=TEXT_3,
   layout=("The bright red vertical strip runs the full height of the left "
           "edge and is about one twentieth of the frame wide. The red top "
           "banner runs from that strip to the right edge and is one seventh "
           "of the frame tall, thinner than usual. There is no bottom band at "
           "all: the golden-orange hero line takes the whole lower half of the "
           "image, nearly half the frame tall and spanning four fifths of the "
           "frame width, the tallest and widest element by far, with a "
           "hand-drawn red ellipse looping round it."),
   bg=("A softly blurred ordinary Japanese living room, warm and plain, bright "
       "flat lighting, no strong shadows."),
   person=("UPPER RIGHT: a close portrait of a Japanese woman of about 70, "
           "short white hair, grey-blue cardigan, seen from the chest up, "
           "eyes wide in disbelief, one hand half-raised toward her cheek, "
           "cut out with a clean white outline, her head almost touching the "
           "banner above her."),
   bottom=("BESIDE HER: an open bank passbook held up at an angle, two of "
           "its printed rows circled by hand in red marker, fine rule lines "
           "and no characters written anywhere.")),
}


# =========================================================================
# BO "PHONG CACH CU" (user yeu cau 2026-09-11: "prompt theo phong cach cu nua")
# Hai khuon CU khac nhau han, deu do tu ANH DA LEN SONG:
#   O1/O3 = khuon **BAKE 9 KHOI** (video 09/10; `03_THUMBNAIL_TITLE_FORMULA.md`
#           §KHUON DANG KHOA — user chot 2026-08-10 bang cach dan chinh anh 09):
#           nen GIAY KE O kem + banner navy 21,2% + hero **VANG CHANH** vien den
#           day + 3 vong khoanh do + MUI TEN DO CONG TO + ruy-bang do nghieng
#           + mat NGAC NHIEN manh + badge. Do: hero **cao 31,7% · rong 63,2%**
#           (09) — cao nhat ho "co dong phu", dung dinh dai 20–31% cua §6.10.
#   O2    = khuon **NAVY-CREAM** (video 19/20): cung ho nhung NHA hon — hero
#           vang-cam gradient, ellipse manh, mui ten nho, khong badge.
#           Do: banner 19,1% · hero cao 18,2% rong 63,6% · ruy-bang 10,7% (19).
# Chu GIU NGUYEN bo T1/T3 => bien thu duy nhat la PHONG CACH.
# =========================================================================
PAPER = ("Cream graph paper with a faint blue grid and slightly aged edges, "
         "flat and evenly lit, no shadows.")

OLD = {
 "O1": dict(
   role="khuon BAKE 9 KHOI cua video 09/10 (vang chanh + mui ten do to)",
   text=[("top banner, white on deep navy", "年金を受け取るご家族へ"),
         ("second line, black with the first two characters in red",
          "請求が必要"),
         ("HERO, largest and widest, bright lemon-yellow with a thick black "
          "outline", "36万円"),
         ("tilted red ribbon, white characters", "片方は返します")],
   layout=("The deep navy top banner runs the full width and is one fifth of "
           "the frame tall. The black second line sits just under it on the "
           "left. The lemon-yellow hero line sits in the middle of the left "
           "two thirds, is by far the tallest and widest text and spans about "
           "two thirds of the frame width, with three loose hand-drawn red "
           "ellipses looping round it and a thick red curved arrow sweeping up "
           "to it from the bottom-left corner. The red ribbon is tilted a few "
           "degrees and sits just under the hero line on the right."),
   bg=PAPER,
   person=("RIGHT THIRD: a Japanese woman of about 70, short white hair, in a "
           "soft grey-blue cardigan, cut out with a thick clean white outline, "
           "standing from just below the banner and cropped by the bottom edge "
           "at the hip, holding an open bank passbook in both hands, eyes wide "
           "and mouth open in astonishment."),
   bottom=("BOTTOM-LEFT PROP: two plain kraft envelopes lying at a slight "
           "angle, fine printed rule lines and empty boxes and no characters "
           "written anywhere.")),
 "O2": dict(
   role="khuon NAVY-CREAM cua video 19/20 (nha hon, ellipse manh)",
   text=[("top banner, white on deep navy", "年金を受け取るご家族へ"),
         ("second line, black with the first two characters in red",
          "請求が必要"),
         ("HERO, largest and widest, golden-orange with a black outline and a "
          "white halo", "36万円"),
         ("deep red ribbon along the bottom-left, white characters",
          "片方は返します")],
   layout=("The deep navy top banner runs the full width and is one fifth of "
           "the frame tall. The black second line sits just under it on the "
           "left. The golden-orange hero line sits in the middle of the left "
           "two thirds, is the tallest and widest text and spans about two "
           "thirds of the frame width, with one thin hand-drawn red ellipse "
           "round it and a small curved red arrow rising to it from below. The "
           "deep red ribbon is one seventh of the frame tall and starts hard "
           "against the left edge at the bottom."),
   bg=PAPER,
   person=("RIGHT THIRD: a Japanese woman of about 70, short white hair, in a "
           "soft grey-blue cardigan, cut out with a clean white outline, "
           "standing from just below the banner and cropped by the bottom edge "
           "at the hip, holding an open bank passbook and looking down at it, "
           "brows drawn together."),
   bottom=("LOWER LEFT OF HER: a kraft envelope and an open bank passbook at a "
           "slight angle, two of its printed rows circled by hand in red "
           "marker, fine rule lines and no characters written anywhere.")),
 "O3": dict(
   role="khuon 9 KHOI + hero KHONG LO (bo ruy-bang) + chu khong lap title",
   text=[("top banner, white on deep navy", "亡くなった月の年金"),
         ("second line, black with the first character in red", "5年で消えます"),
         ("HERO, largest and widest, bright lemon-yellow with a thick black "
          "outline", "返す分がある")],
   layout=("The deep navy top banner runs the full width and is one seventh of "
           "the frame tall. The black second line sits just under it on the "
           "left. There is no ribbon at all: the lemon-yellow hero line takes "
           "the whole lower half of the image, nearly half the frame tall and "
           "spanning four fifths of the frame width, by far the largest "
           "element, with three loose hand-drawn red ellipses looping round it "
           "and a thick red curved arrow sweeping up to it from the "
           "bottom-left corner."),
   bg=PAPER,
   person=("UPPER RIGHT: a close portrait of a Japanese woman of about 70, "
           "short white hair, grey-blue cardigan, seen from the chest up, eyes "
           "wide and mouth open in astonishment, one hand half-raised toward "
           "her cheek, cut out with a thick clean white outline, her head "
           "almost touching the banner above her."),
   bottom=("BESIDE HER: an open bank passbook held up at an angle, two of its "
           "printed rows circled by hand in red marker, fine rule lines and no "
           "characters written anywhere.")),
}

def build(v):
    lines = ", ".join(f"{role}: {txt}" for role, txt in v["text"])
    return (f"{HEAD} TEXT, exactly these {len(v['text'])} blocks and nothing "
            f"else: {lines}. LAYOUT: {v['layout']} BACKGROUND: {v['bg']} "
            f"{v['person']} {v['bottom']} {QUALITY}")


def plate(v):
    return (f"{HEAD.replace(', with bold Japanese text burned into the image', '')} "
            f"LAYOUT: {v['layout']} BACKGROUND: {v['bg']} {v['person']} "
            f"{v['bottom']} A clean empty plate with no lettering anywhere, "
            f"leaving the left strip, the banner strip, the middle band and the "
            f"bottom band clear for text to be added later. No watermark. "
            f"--ar 16:9")


def main():
    vd = os.path.join(PROJ, "06_VIDEO", STEM)
    os.makedirs(vd, exist_ok=True)
    flow, plates, ten, blocks = [], [], [], []
    blocks.append(
        "# THUMBNAIL A/B 3x3 — video 22 未支給年金・36万円\n\n"
        "- keyword do duoc (Trends YouTube JP 30 ngay, pytrends 2026-09-11): "
        "**年金 ~73,8 (cao nhat, qua anchor)** · 遺族年金 35,1 · "
        "**未支給年金 0,3** · 死亡届 0 · 未支給年金 請求 0\n"
        "- ⛔ KHONG dat `遺族年金` len thumbnail: do cao nhung **khong co trong "
        "video 22** => sai intent + misleading\n"
        "- khuon do tu 3 ANH LIVE cua video 21: dai doc trai **4,8%** be ngang · "
        "banner tren **19,7%** · hero **rong 62,4%** · bang day **17,4%** · "
        "nguoi cat-nen ben phai\n"
        "- ⭐ T3 live cua 21 do duoc **hero cao 47,0% / rong 81,8%** = ban dau "
        "tien QUA gate 2, co che = **bo bang day**\n"
        "- ten anh dich: `thumb_T1_*.png` / `_T2_` / `_T3_`\n")
    for tag in ("T1", "T2", "T3"):
        v = V[tag]
        p = " ".join(build(v).split())
        flow.append(p)
        plates.append(" ".join(plate(v).split()))
        ten.append(f"{tag}\tthumb_{tag}_mishikyu-36man.png")
        blocks.append(
            f"\n## {tag} — {v['role']}\n\n**CHU ({len(v['text'])} dong):**\n"
            + "\n".join(f"- `{t}` — {r}" for r, t in v["text"])
            + f"\n\n**PROMPT ({len(p)} ky, TEXT o "
              f"{p.find('TEXT, exactly') * 100 // len(p)}%):**\n```\n{p}\n```\n")

    def w(n, t):
        io.open(os.path.join(vd, n), "w", encoding="utf-8", newline="\n").write(t)

    # -- bo PHONG CACH CU (cung bo chu, bien thu = PHONG CACH) --------------
    oflow, oplate, oten, oblocks = [], [], [], []
    oblocks.append(
        "# THUMBNAIL — BO PHONG CACH CU, video 22 \u672a\u652f\u7d66\u5e74\u91d1\u30fb36\u4e07\u5186\n\n"
        "- **Chu giong het bo T1/T3** => bien thu duy nhat la PHONG CACH.\n"
        "- O1/O3 = khuon **BAKE 9 KHOI** (video 09/10): giay ke o kem · banner "
        "navy **21,2%** · hero **VANG CHANH** vien den day, cao **31,7%** rong "
        "**63,2%** · 3 vong khoanh do · **mui ten do cong TO** · ruy-bang "
        "nghieng · mat ngac nhien manh\n"
        "- O2 = khuon **NAVY-CREAM** (video 19/20): banner **19,1%** · hero "
        "vang-cam cao **18,2%** rong **63,6%** · ellipse manh · ruy-bang "
        "**10,7%** · nha hon\n"
        "- ten anh dich: `thumb_O1_*.png` / `_O2_` / `_O3_`\n")
    for tag in ("O1", "O2", "O3"):
        v = OLD[tag]
        p = " ".join(build(v).split())
        oflow.append(p)
        oplate.append(" ".join(plate(v).split()))
        oten.append(f"{tag}\tthumb_{tag}_mishikyu-36man.png")
        oblocks.append(
            f"\n## {tag} — {v['role']}\n\n**CHU ({len(v['text'])} dong):**\n"
            + "\n".join(f"- `{t}` — {r}" for r, t in v["text"])
            + f"\n\n**PROMPT ({len(p)} ky, TEXT o "
              f"{p.find('TEXT, exactly') * 100 // len(p)}%):**\n```\n{p}\n```\n")
    w("thumb_prompts_OLD_FLOW.txt", "\n".join(oflow) + "\n")
    w("thumb_prompts_OLD_PLATE.txt", "\n".join(oplate) + "\n")
    w("thumb_prompts_OLD_TENFILE.txt", "ban\tten file dich\n" + "\n".join(oten) + "\n")
    w("thumb_prompts_OLD_BLOCKS.md", "\n".join(oblocks) + "\n")

    w("thumb_prompts_FLOW.txt", "\n".join(flow) + "\n")
    w("thumb_prompts_PLATE.txt", "\n".join(plates) + "\n")
    w("thumb_prompts_TENFILE.txt", "ban\tten file dich\n" + "\n".join(ten) + "\n")
    w("thumb_prompts_BLOCKS.md", "\n".join(blocks) + "\n")

    print(f"\n-> 06_VIDEO/{STEM}/")
    print(f"   thumb_prompts_FLOW.txt    3 prompt "
          f"({min(len(x) for x in flow)}–{max(len(x) for x in flow)} ky)")
    print("   thumb_prompts_PLATE.txt   3 plate KHONG chu (duong lui)")
    print("   thumb_prompts_TENFILE.txt · thumb_prompts_BLOCKS.md")
    bad = False
    for tag, p in zip(("T1", "T2", "T3"), flow):
        pos = p.find("TEXT, exactly") * 100 // len(p)
        flag = "OK" if pos <= 15 else "🔴"
        bad = bad or pos > 15
        print(f"   {tag}: {len(p):5d} ky · TEXT @ {pos:2d}% {flag} · "
              f"{len(V[tag]['text'])} dong chu")
        if len(p) > 1500:
            print(f"       ⚠️ dai {len(p)} > 1.500 (gate phu, `ab-3title` §3.1)")
    print("   thumb_prompts_OLD_FLOW.txt  3 prompt PHONG CACH CU "
          f"({min(len(x) for x in oflow)}-{max(len(x) for x in oflow)} ky)")
    print("   thumb_prompts_OLD_PLATE/TENFILE/BLOCKS")
    for tag, p in zip(("O1", "O2", "O3"), oflow):
        pos = p.find("TEXT, exactly") * 100 // len(p)
        flag = "OK" if pos <= 15 else "🔴"
        bad = bad or pos > 15
        print(f"   {tag}: {len(p):5d} ky · TEXT @ {pos:2d}% {flag} · "
              f"{len(OLD[tag]['text'])} dong chu")
        if len(p) > 1500:
            print(f"       ⚠️ dai {len(p)} > 1.500 (gate phu, `ab-3title` §3.1)")
    if bad:
        print("   🔴 GATE CHINH: TEXT phai nam trong 15% DAU prompt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
