# -*- coding: utf-8 -*-
r"""thumb_prompts_23.py — prompt gen THUMBNAIL A/B 3x3 cho video 23 (年金請求書が届かない).

User chot 2026-09-13: **"cho tôi prompt gen thumbnail theo dạng cũ nhé"**
=> bo chinh la khuon **BAKE 9 KHOI** cua video 09/10 (giay ke o kem + banner navy + hero
VANG CHANH vien den day + vong khoanh do + mui ten do cong to + ruy-bang nghieng + mat
ngac nhien), dung khuon `OLD` da chot o `thumb_prompts_22.py`. Ba ban xuat ra ten
`thumb_T1/T2/T3_*` de `upload_pack.py` doc duoc (gate 3x3).

QUY TRINH 5 BUOC cua `ab-3title-3thumb.md` §3.1 — da chay du:

BUOC 1 — KHUON LAY TU ANH DA LEN SONG, KHONG tu tai lieu:
  `07_UPLOADED/22_mishikyu-nenkin-36man/_upload/thumbnail.jpg` (do 2026-09-13).

BUOC 2 — DO BANG MAY tren anh live 22 (760x428):
  banner navy/do tren = **14,5% chieu cao** · hero vang = **59,3% be ngang**.
  Khop dai da ghi cho 09/19/21 (banner 19–21% · hero rong 62–64%) ⇒ giu "one fifth"
  cho banner va "two thirds" cho be ngang hero trong prompt.
  ⭐ Co che da do o video 21: hero chi vuot gate 2 (>=33,3% cao) khi **BO ruy-bang day**
  ⇒ T3 bo ruy-bang, T1/T2 giu (baseline).

BUOC 5 — CHU QUA 2 PHEP DO (Trends YouTube JP 30 ngay, pytrends, do 2026-09-13):
  年金 **81,0 / 81,3** ⭐ (do 2 ro, cung anchor) · 年金 手続き 0,5 · 年金 請求 0,3 ·
  年金請求書 **0,2** · 年金 はがき 0,2 · 特別支給の老齢厚生年金 0,3 ·
  年金 時効 0,0 · 年金 届かない 0,0 · 老齢年金 請求 0,0
  ⇒ Y HET video 22: **年金 la tu DUY NHAT co volume that**, moi tu dac ta deu ~0.
    Nen 年金 len BANNER, con chu the that (請求書/はがき) day xuong **HINH** (phong bi +
    buu thiep trong tay nguoi). Dung khuon nenkin 10 + 21 + 22.

GATE CHU (`audience-45plus.md` §1 gate 7 — che anh di van biet bai noi gi):
  (1) ve cai gi  : 年金 (banner) + 請求書/はがき trong hinh
  (2) chuyen gi  : 出さないと0円 + 156万円   (T3: 届かない人がいる)
  (3) phai lam gi: 5年で消えます            (T3: あと二か月でした)

BA BAN A/B — moi ban doi DUNG MOT BIEN (`ab-3title-3thumb.md` §3):
  T1 = baseline khuon BAKE 9 KHOI (giay ke o + banner + hero vang chanh + ruy-bang + nguoi)
  T2 = doi MOT bien HINH (bo nguoi -> can canh doi tay cam hagaki; doi tong nen sang-lanh),
       **chu giong het T1 tung ky tu**
  T3 = doi LAYOUT (mat to + hero khong lo, BO ruy-bang) + thu triet ly "thumbnail KHONG
       lap title" (`youtube-suggested-growth.md` §6 muc 1)

RANG BUOC (kiem bang may o cuoi file):
  · TEXT o khoi thu 2, trong **15% dau prompt** · tran ~1.500 ky
  · tran **4 DONG chu** cho anh AI · chua trong **goc duoi-PHAI** (timestamp YouTube)
  · `no watermark` + cau chat luong chu Nhat
  · giay to trong hinh phai **DE TRON** (`no characters written anywhere`) — chu Nhat AI
    gen la nat net (`media-library.md` §2.9)

CHAY:  python tools/thumb_prompts_23.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "23_nenkin-seikyusho-todokanai"
SLUG = "seikyusho-todokanai"

# 🔴 SIET 2026-09-13 sau lo gen dau tien: cau "exactly these N blocks and nothing else"
#    KHONG DU. Model tra ve T1 co them **ba** khoi tu bia — mot the do 「緊急事態」 dat
#    NGAY GIUA banner, **cat doi** dong 「もうすぐ年金を受け取る方へ」 thanh
#    「もうすぐ年」+「け取る方へ」 ⇒ mat han chu 年金, tuc mat keyword DUY NHAT do duoc
#    (Trends 81,0) — hong gate 7 muc (1). Cong them 「期限迫る!」 va 「今すぐ確認!」 =
#    khang dinh khan cap KHONG co trong video ⇒ misleading (`youtube-compliance.md` muc 4).
#    ⇒ Cam theo TEN LOAI vat the (badge/stamp/sticker/starburst), vi model doc TU KHOA chu
#      khong doc phu dinh truu tuong — cung bai hoc `_policy20.py` §(1).
NO_EXTRA = ("Do not add any badge, stamp, sticker, seal, starburst, callout "
            "bubble or extra label anywhere. The top banner must be one "
            "unbroken strip of text with nothing overlapping or interrupting "
            "it.")

QUALITY = (NO_EXTRA + " Text must be perfectly formed Japanese characters, "
           "crisp and legible. Keep the very bottom-right corner free of text. "
           "No watermark, no logo, no signature, no additional text. --ar 16:9")

HEAD = ("A 16:9 Japanese YouTube thumbnail for a calm pension-information "
        "channel, in the style of a broadcast news telop, with bold Japanese "
        "text burned into the image.")

PAPER = ("Cream graph paper with a faint blue grid and slightly aged edges, "
         "flat and evenly lit, no shadows.")

# ── chu: T1 va T2 GIONG HET NHAU tung ky tu (bien thu cua T2 la HINH) ───────
TEXT_12 = [("top banner, white on deep navy", "もうすぐ年金を受け取る方へ"),
           ("second line, black with the first three characters in red",
            "出さないと0円"),
           ("HERO, largest and widest, bright lemon-yellow with a thick black "
            "outline", "156万円"),
           ("tilted red ribbon, white characters", "5年で消えます")]

# T3: chu KHONG lap title, hero doi sang menh de (thu nghiem §6 muc 1)
TEXT_3 = [("top banner, white on deep navy", "年金は自動で始まらない"),
          ("second line, black with the first four characters in red",
           "あと二か月でした"),
          ("HERO, largest and widest, bright lemon-yellow with a thick black "
           "outline", "届かない人がいる")]

V = {
 "T1": dict(
   role="baseline khuon BAKE 9 KHOI (video 09/10) — giay ke o + hero vang chanh",
   text=TEXT_12,
   layout=("The deep navy top banner runs the full width and is one fifth of "
           "the frame tall. The black second line sits just under it on the "
           "left. The lemon-yellow hero line sits in the middle of the left "
           "two thirds, is by far the tallest and widest text and spans about "
           "two thirds of the frame width, with three loose hand-drawn red "
           "ellipses looping round it and a thick red curved arrow sweeping up "
           "to it from the bottom-left corner. The red ribbon is tilted a few "
           "degrees and sits just under the hero line on the right."),
   bg=PAPER,
   person=("RIGHT THIRD: a Japanese man of about 65, short grey hair, in a "
           "soft beige cardigan over a pale shirt, cut out with a thick clean "
           "white outline, standing from just below the banner and cropped by "
           "the bottom edge at the hip, holding a single plain postcard in "
           "both hands, eyes wide and mouth open in astonishment."),
   bottom=("BOTTOM-LEFT PROP: a plain kraft envelope and a plain postcard "
           "lying at a slight angle, fine printed rule lines and empty boxes "
           "and no characters written anywhere.")),
 "T2": dict(
   role="doi MOT bien HINH (bo nguoi + doi tong nen lanh), GIU nguyen chu",
   text=TEXT_12,
   layout=("Same nine-block telop layout: deep navy top banner across the full "
           "width one fifth of the frame tall, black second line just under it "
           "on the left, lemon-yellow hero line in the middle of the left two "
           "thirds spanning about two thirds of the width as by far the "
           "tallest and widest text, three loose hand-drawn red ellipses round "
           "it and a thick red curved arrow sweeping up from the bottom-left "
           "corner, tilted red ribbon just under the hero on the right."),
   bg=("A cool pale blue-grey desktop seen from straight above, flat and "
       "evenly lit, no strong shadows."),
   person=("RIGHT THIRD: no person. Instead a close pair of older hands "
           "holding a single plain postcard up at an angle, the postcard large "
           "and clearly lit, its address box left completely empty, fine "
           "printed rule lines and no characters written anywhere."),
   bottom=("BOTTOM-LEFT PROP: a plain kraft envelope torn open at one end and "
           "a slim red marker pen lying at a slight angle.")),
 "T3": dict(
   role="doi LAYOUT (mat to, hero khong lo, BO ruy-bang) + chu khong lap title",
   text=TEXT_3,
   layout=("The deep navy top banner runs the full width and is one seventh of "
           "the frame tall, thinner than usual. The black second line sits "
           "just under it on the left. There is no ribbon at all: the "
           "lemon-yellow hero line takes the whole lower half of the image, "
           "nearly half the frame tall and spanning four fifths of the frame "
           "width, by far the largest element, with three loose hand-drawn red "
           "ellipses looping round it and a thick red curved arrow sweeping up "
           "to it from the bottom-left corner."),
   bg=PAPER,
   person=("UPPER RIGHT: a close portrait of a Japanese man of about 65, short "
           "grey hair, beige cardigan, seen from the chest up, eyes wide and "
           "mouth open in astonishment, one hand half-raised toward his cheek, "
           "cut out with a thick white outline, his head almost touching "
           "the banner above him."),
   bottom=("BESIDE HIM: an empty postbox slot and a plain postcard slipping "
           "into it at an angle, fine rule lines and no characters written "
           "anywhere.")),
}


def build(v):
    lines = ", ".join(f"{role}: {txt}" for role, txt in v["text"])
    return (f"{HEAD} TEXT, exactly these {len(v['text'])} blocks and nothing "
            f"else: {lines}. LAYOUT: {v['layout']} BACKGROUND: {v['bg']} "
            f"{v['person']} {v['bottom']} {QUALITY}")


def plate(v):
    """Duong lui: plate KHONG chu, de render bang tool neu anh gen nat kanji.

    🔴 Phai o FILE RIENG — extension bom ca file, plate ghi `no lettering` nen ra anh
    trang chu DUNG thiet ke; tron vao FLOW.txt la tuong prompt chua sua
    (`ab-3title-3thumb.md` §3 muc 8, dinh that o chouhen 21).
    """
    return (f"{HEAD.replace(', with bold Japanese text burned into the image', '')} "
            f"LAYOUT: {v['layout']} BACKGROUND: {v['bg']} {v['person']} "
            f"{v['bottom']} A clean empty plate with no lettering anywhere, "
            f"leaving the banner strip, the middle band and the bottom band "
            f"clear for text to be added later. No watermark. --ar 16:9")


def main():
    vd = os.path.join(PROJ, "06_VIDEO", STEM)
    os.makedirs(vd, exist_ok=True)
    flow, plates, ten, blocks = [], [], [], []
    blocks.append(
        "# THUMBNAIL A/B 3x3 — video 23 年金請求書が届かない (khuon CU: BAKE 9 KHOI)\n\n"
        "- user chot 2026-09-13: *\"cho tôi prompt gen thumbnail theo dạng cũ nhé\"*\n"
        "- keyword do duoc (Trends YouTube JP 30 ngay, pytrends 2026-09-13): "
        "**年金 81,0** (cao nhat, do 2 ro) · 年金 手続き 0,5 · 年金 請求 0,3 · "
        "**年金請求書 0,2** · 年金 はがき 0,2 · 特別支給の老齢厚生年金 0,3 · "
        "年金 時効 0 · 年金 届かない 0\n"
        "- ⇒ chi `年金` co volume that ⇒ len BANNER; chu the (請求書/はがき) day "
        "xuong HINH. Y het ket luan cua video 21/22.\n"
        "- khuon do tu ANH LIVE video 22: banner **14,5% cao** · hero **59,3% rong**\n"
        "- ⭐ T3 bo ruy-bang day de hero an tron khe doc (co che da do o video 21: "
        "hero 47,0% cao = ban dau tien qua gate 2)\n"
        "- ten anh dich: `thumb_T1_*.png` / `_T2_` / `_T3_` "
        "(`upload_pack.py` doc dung pattern nay)\n"
        "\n### 3 TITLE A/B — moi ban mot gia thuyet\n\n"
        "| | title | ky | vi tri keyword | gia thuyet thu |\n"
        "|---|---|---|---|---|\n"
        "| **A1** ⭐ dung truoc | `年金請求書は、届かない人がいます｜出さないと"
        "156万円が0円に` | 32 | 年金@0 | keyword volume cao nhat dung dau |\n"
        "| **A2** | `年金請求書が届かない四つの理由｜出さないと年金は0円のままです` "
        "| 31 | 年金@0 | doi keyword dan sang chinh CHU THE (年金請求書) |\n"
        "| **A3** | `年金は自動では始まりません｜あと二か月で156万円が消えるところ"
        "でした` | 34 | 年金@0 | doi kieu hook: nghich ly + suyt mat |\n\n"
        "⚠️ Con lai cua goi CTR (ten file upload · 3 dong dau 概要欄 · mo ta day du · "
        "タグ) **chua lam** — xem `youtube-upload-seo.md`.\n")
    for tag in ("T1", "T2", "T3"):
        v = V[tag]
        p = " ".join(build(v).split())
        flow.append(p)
        plates.append(" ".join(plate(v).split()))
        ten.append(f"{tag}\tthumb_{tag}_{SLUG}.png")
        pos = p.find("TEXT, exactly") * 100 // len(p)
        blocks.append(
            f"\n## {tag} — {v['role']}\n\n**CHU ({len(v['text'])} dong):**\n"
            + "\n".join(f"- `{t}` — {r}" for r, t in v["text"])
            + f"\n\n**PROMPT ({len(p)} ky, TEXT o {pos}%):**\n```\n{p}\n```\n")

    def w(n, t):
        io.open(os.path.join(vd, n), "w", encoding="utf-8", newline="\n").write(t)

    w("thumb_prompts_FLOW.txt", "\n".join(flow) + "\n")
    w("thumb_prompts_PLATE.txt", "\n".join(plates) + "\n")
    w("thumb_prompts_TENFILE.txt", "ban\tten file dich\n" + "\n".join(ten) + "\n")
    w("thumb_prompts_BLOCKS.md", "\n".join(blocks) + "\n")

    # ── GATE (ab-3title-3thumb.md §3.1 buoc 3) ─────────────────────────────
    print(f"xuat 4 file -> {vd}")
    bad = 0
    for tag, p in zip(("T1", "T2", "T3"), flow):
        pos = p.find("TEXT, exactly") * 100 // len(p)
        nl = len(V[tag]["text"])
        f1 = "OK" if pos <= 15 else "🔴 TEXT ra ngoai 15% dau"
        f2 = "OK" if len(p) <= 1500 else f"⚠️ dai {len(p)} > 1500"
        f3 = "OK" if nl <= 4 else f"🔴 {nl} dong > tran 4"
        f4 = "OK" if "no watermark" in p.lower() else "🔴 thieu no watermark"
        f5 = ("OK" if "bottom-right corner free of text" in p else
              "🔴 thieu chua trong goc duoi-phai")
        bad += sum(x != "OK" for x in (f1, f3, f4, f5))   # f2 = tran do dai: GATE PHU
        print(f"  {tag}: {len(p):>4} ky · TEXT@{pos:>2}% · {nl} dong "
              f"| {f1} | {f2} | {f3} | {f4} | {f5}")
    print("GATE PROMPT:", "SACH" if not bad else f"🔴 {bad} loi")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
