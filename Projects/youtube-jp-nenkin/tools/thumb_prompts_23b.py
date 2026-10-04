# -*- coding: utf-8 -*-
r"""thumb_prompts_23b.py — GEN LAI thumbnail video 23, nang lop hinh cho "noi bat nhu 22".

User chot 2026-09-14: dan chinh anh live cua video 22 va noi *"tao muon no phai noi bat
nhu video 22"*. Do la cach chi khuon CHUAN NHAT (`ab-3title-3thumb.md` §3.1 Buoc 1:
lay khuon tu ANH DA LEN SONG, khong tu tai lieu).

⚠️ BIEN THU CUA LUOT NAY LA **HINH**, KHONG PHAI CHU.
   Bo chu cua ban 23 cu da qua **ca 2 phep do** (Trends 2026-09-13: 年金 81,0 la tu duy
   nhat co volume that; gate 7 `audience-45plus.md` §1 du 3 cau) ⇒ **giu nguyen tung ky
   tu**. Doi chu o day la lam hong phep do, khong phai cai thien.

BUOC 2 — DO BANG MAY, 2 anh live dat canh nhau (scratchpad/meas.py + meas2.py):

  |                              | V22 (user thich) | V23 hien tai |
  |------------------------------|------------------|--------------|
  | do sang TB toan khung        | **179,9**        | 127,0        |
  | nen sach: R-B (am/lanh)      | **+23 … +70**    | **-14** lanh |
  | %pixel VANG                  | 6,42%            | 8,96%        |
  | luoi VANG 3x3 — o BEN PHAI   | **4,8 / 6,0 / 3,3** | 1,5 / 2,2 / 1,5 |
  | luoi VANG 3x3 — o giua       | 17,4 / 22,0      | **31,3 / 33,1** |
  | HERO bbox                    | cao 64,0 rong 65,8 | cao 48,3 rong 73,1 |

  🔴 **KET LUAN NGUOC VOI TRUC GIAC, va day la phan dang gia nhat:** ban 23 KHONG thua
  vi hero nho — hero cua no con **RONG HON** (73,1% vs 65,8%) va tong vang con **NHIEU
  HON** (8,96% vs 6,42%). No thua vi **vang DON MOT CUC o giua** (2 o giua an 64% tong
  vang, ba o ben phai gan nhu trang) va vi **nen LANH** (R-B = -14, tuc xanh hon do).
  ⇒ Do "% vang" hay "co hero to khong" **khong do duoc do noi bat**; cai do duoc la
    **PHAN BO vang tren khung** + **nhiet do nen**. Cung ho bai hoc `audience-45plus.md`
    §6.10 (gate do sai thu no muon do).

BAY THU DO TU ANH 22 MA BAN 23 CU THIEU — day la noi dung sua, tung mon mot:
  (1) nen **KEM AM** (khong phai xam lanh)      (5) **4 dong ¥ VANG** noi quanh khung
  (2) **tia toc do den** toa tu 4 mep           (6) **hat sang bokeh vang** rai khap
  (3) **quang sang vang** no sau hero           (7) **3 vong ellipse do DAY** (cu: 1 manh)
  (4) vat cam **CO NOI DUNG** — cu la buu thiep TRANG TRON, thay bang to don A4 in san
      nhieu o ke; con 2 phong bi kraft TO (cu: 1 cai nhat)

⛔ KHONG dung `postcard` tron nua o T1/T2: no la thu lam khung "rong" nhat trong anh cu.
   はがき 65 tuoi van co trong bai (scene 51) nhung de o T3, va van phai co o ke.

§KHAC GI SO VOI 22 (user chot 2026-09-14: *"prompt phai khac khac ti chu"*)
  Muon lop LAP LANH cua 22, nhung khong duoc ra ban sao — vua la y user, vua la luat
  `youtube-compliance.md` §1 (cam lap NGUYEN BO visual giua cac video). Ba diem doi, moi
  diem deu CHO NGHIA cua chinh bai 23, khong phai doi cho khac:
  | | video 22 | video 23 |
  |---|---|---|
  | mat cast | toc bac ngan, mat thon | ⭐ **DAU HOI, MAT TRON** (user chi dinh; khop luon anh 23 dang chay) |
  | nhan hero | **3 vong ellipse** + mui ten CONG quet len tu duoi-trai | **1 vong day + 集中線 do toa** + mui ten THANG cheo tu tren-trai dam xuong |
  | do cu goc duoi-trai | 2 phong bi kraft | ⭐ **HOP THU NHAT MAU DO, nap mo, RONG** — dung noi dung "thu khong toi" va la mot mang DO to, diem nhan manh hon phong bi kraft |
  GIU nguyen lop lam nen do noi bat: nen kem am · tia toc do · quang sang vang · 4 dong ¥ ·
  hat bokeh. Doi may cai nay la mat luon thu vua sua duoc.

CHAY:  python tools/thumb_prompts_23b.py
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "23_nenkin-seikyusho-todokanai"
SLUG = "seikyusho-todokanai"

# 🔴 Giu nguyen tu `thumb_prompts_23.py`: cau "exactly N blocks" KHONG du — lo gen dau
#    tien model tu them the 「緊急事態」 dat GIUA banner, cat doi chu 年金 (mat keyword
#    duy nhat do duoc). Cam theo TEN LOAI vat the, vi model doc TU KHOA chu khong doc
#    phu dinh truu tuong.
NO_EXTRA = ("Do not add any badge, stamp, sticker, seal or extra label "
            "anywhere; the top banner must be one unbroken strip of text.")

QUALITY = (NO_EXTRA + " Text must be perfectly formed Japanese characters, "
           "crisp and legible. Keep the very bottom-right corner free of text. "
           "No watermark, no logo, no extra text. --ar 16:9")

HEAD = ("A 16:9 bright Japanese YouTube thumbnail in broadcast news telop "
        "style, with bold Japanese text burned into the image.")

# (1)(2) nen KEM AM + tia toc do — thay `cool pale blue-grey` cua ban cu
PAPER = ("Warm cream graph paper with a faint blue grid and aged warm edges, "
         "bright and evenly lit, with fine black speed lines radiating in "
         "from all four edges.")

# (3)(5)(6) lop lap lanh — khoi dung chung cho ca ba ban
SPARK = ("ACCENTS: a warm golden glow blooming behind the hero, four round "
         "golden yen coins floating at different sizes near the upper right, "
         "lower right and lower left, and small golden bokeh sparkles across "
         "the frame.")

# ── CHU: GIU NGUYEN tung ky tu tu ban 23 cu (da qua Trends + gate 7) ────────
TEXT_12 = [("top banner, white on deep navy", "もうすぐ年金を受け取る方へ"),
           ("second line, black with the first three characters in red",
            "出さないと0円"),
           ("HERO, largest and widest, golden-yellow with a thick black "
            "outline and a white halo", "156万円"),
           ("tilted red ribbon, white characters", "5年で消えます")]

TEXT_3 = [("top banner, white on deep navy", "年金は自動で始まらない"),
          ("second line, black with the first four characters in red",
           "あと二か月でした"),
          ("HERO, largest and widest, golden-yellow with a thick black "
           "outline and a white halo", "届かない人がいる")]

# ⭐ CAST (user chot 2026-09-14: "cu gia dau hoi hoi, mat tron") — mo ta MOT CHO,
#    dung chung ca 3 ban de nhan dang khong troi giua T1/T2/T3.
FACE = ("a Japanese man of about 68 with a balding head, bare on top with "
        "short grey hair at the sides, a round full face, thick grey "
        "eyebrows and a stocky build")

# ⭐ NHAN HERO — DOI so voi khuon 22 (22 = 3 ellipse + mui ten CONG quet len).
#    Day la mot trong ba diem "khac mot ti" (xem docstring §KHAC GI SO VOI 22).
RINGS = ("one thick hand-drawn red ellipse looping right round it, short red "
         "radiating burst lines fanning out behind it, and a bold straight "
         "red arrow slanting down into it from the upper left")

V = {
 "T1": dict(
   role="khuon 22 y nguyen — nen kem am + tia toc do + dong ¥ + so ho so trong tay",
   text=TEXT_12,
   layout=("Deep navy top banner across the top, one fifth of the frame tall; "
           "black second line just under it on the left; golden-yellow hero "
           "line in the middle of the left two thirds, by far the tallest and "
           "widest text, spanning four fifths of that area, with " + RINGS +
           " corner; a large red ribbon tilted a few degrees just under the "
           "hero on the right."),
   bg=PAPER,
   person=("RIGHT THIRD: " + FACE + ", in a pale blue knitted cardigan, cut "
           "out with a thick white outline, from just below the banner and "
           "cropped by the bottom edge at the hip, holding open in both hands "
           "a large printed A4 pension form of fine ruled rows and empty "
           "boxes, brows drawn together and mouth turned down in dismay."),
   bottom=("BOTTOM-LEFT PROP: a red Japanese letterbox tilted slightly, flap "
           "hanging open and nothing inside, one window envelope leaning at "
           "its foot with ruled empty boxes and no characters written "
           "anywhere.")),
 "T2": dict(
   role="doi MOT bien HINH (bo nguoi -> can canh tay cam don), CHU y het T1",
   text=TEXT_12,
   layout=("Same telop layout: deep navy banner across the top one fifth of "
           "the frame tall, black second line under it on the left, "
           "golden-yellow hero in the middle of the left two thirds as by far "
           "the tallest and widest text spanning four fifths of that area, "
           "with " + RINGS + " corner, and a large tilted red ribbon under "
           "the hero on the right."),
   bg=PAPER,
   person=("RIGHT THIRD: no person, instead a close pair of older hands "
           "holding up a large printed A4 pension form that fills the whole "
           "right third, covered in fine ruled rows and empty boxes with two "
           "rows circled in red marker, no characters written anywhere."),
   bottom=("BOTTOM-LEFT PROP: a red Japanese letterbox with its flap hanging "
           "open and nothing inside, and a slim red marker pen lying at a "
           "slight angle beside it.")),
 "T3": dict(
   role="doi LAYOUT (mat can to + hero khong lo, BO ruy-bang) + chu khong lap title",
   text=TEXT_3,
   layout=("Deep navy top banner across the top, only one seventh of the "
           "frame tall; black second line just under it on the left; no ribbon "
           "at all, so the golden-yellow hero line takes the whole lower half "
           "of the image, nearly half the frame tall and spanning four fifths "
           "of the frame width, by far the largest element, with " + RINGS +
           " corner."),
   bg=PAPER,
   person=("UPPER RIGHT: a close portrait of " + FACE + ", in a pale blue "
           "knitted cardigan, from the chest up, eyes wide and mouth open in "
           "astonishment, one hand half-raised toward his cheek, cut out with "
           "a thick white outline, his head almost touching the banner above "
           "him."),
   bottom=("BESIDE HIM: a large postcard held at an angle, ruled address boxes "
           "left completely empty and no characters written anywhere.")),
}


def build(v):
    lines = ", ".join(f"{role}: {txt}" for role, txt in v["text"])
    return (f"{HEAD} TEXT, exactly these {len(v['text'])} blocks and nothing "
            f"else: {lines}. LAYOUT: {v['layout']} BACKGROUND: {v['bg']} "
            f"{SPARK} {v['person']} {v['bottom']} {QUALITY}")


def plate(v):
    """Duong lui: plate KHONG chu, de render bang tool neu anh gen nat kanji.

    🔴 Phai o FILE RIENG — extension bom ca file; plate ghi `no lettering` nen ra anh
    trang chu DUNG thiet ke, tron vao FLOW.txt la tuong prompt chua sua
    (`ab-3title-3thumb.md` §3 muc 8, dinh that o chouhen 21).
    """
    return (f"{HEAD.replace(', with bold Japanese text burned into the image', '')} "
            f"LAYOUT: {v['layout']} BACKGROUND: {v['bg']} {SPARK} {v['person']} "
            f"{v['bottom']} A clean empty plate with no lettering anywhere, "
            f"leaving the banner strip, the middle band and the bottom band "
            f"clear for text to be added later. No watermark. --ar 16:9")


def main():
    vd = os.path.join(PROJ, "06_VIDEO", STEM)
    os.makedirs(vd, exist_ok=True)
    flow, plates, ten, blocks = [], [], [], []
    blocks.append(
        "# THUMBNAIL video 23 — GEN LAI v2 (\"noi bat nhu video 22\")\n\n"
        "User dan chinh anh live cua video 22 (2026-09-14). Bien thu cua luot nay la "
        "**HINH**; **chu giu nguyen tung ky tu** vi da qua Trends + gate 7.\n\n"
        "## So do 2 anh live (scratchpad/meas.py, meas2.py)\n\n"
        "|                          | V22 (thich) | V23 cu |\n"
        "|---|---|---|\n"
        "| do sang TB toan khung    | **179,9** | 127,0 |\n"
        "| nen sach: R-B (am/lanh)  | **+23…+70** | **-14 (lanh)** |\n"
        "| %pixel vang              | 6,42% | 8,96% |\n"
        "| luoi vang 3x3, ba o PHAI | **4,8 / 6,0 / 3,3** | 1,5 / 2,2 / 1,5 |\n"
        "| HERO bbox                | cao 64,0 rong 65,8 | cao 48,3 rong 73,1 |\n\n"
        "🔴 Ban cu KHONG thua vi hero nho — hero no **rong hon** va vang **nhieu hon**. "
        "No thua vi vang **don mot cuc o giua** va nen **lanh**. Do \"% vang\" khong do "
        "duoc do noi bat; cai do duoc la **PHAN BO vang** + **nhiet do nen**.\n\n"
        "## Bay thu them vao prompt (deu do tu anh 22)\n"
        "1. nen **kem am** thay xam lanh · 2. **tia toc do den** 4 mep · "
        "3. **quang sang vang** sau hero · 4. **4 dong ¥ vang** noi quanh khung · "
        "5. **hat bokeh vang** rai khap · 6. **3 ellipse do day** (cu 1 manh) · "
        "7. vat cam doi tu **buu thiep trang tron** -> **don A4 nhieu o ke** · "
        "8. **2 phong bi kraft TO** (cu 1 cai nhat)\n\n"
        "- ten anh dich: `thumb_T1_*.png` / `_T2_` / `_T3_` "
        "(`upload_pack.py` doc dung pattern nay)\n"
        "- ⛔ Anh gen xong **phai xoa ✦ watermark** truoc khi dung "
        "(`media-library.md` §2.10 ⑤b; lo 2752x1536 co **2 dau**)\n")
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

    w("thumb_prompts_v2_FLOW.txt", "\n".join(flow) + "\n")
    w("thumb_prompts_v2_PLATE.txt", "\n".join(plates) + "\n")
    w("thumb_prompts_v2_TENFILE.txt", "ban\tten file dich\n" + "\n".join(ten) + "\n")
    w("thumb_prompts_v2_BLOCKS.md", "\n".join(blocks) + "\n")

    # ── GATE (ab-3title-3thumb.md §3.1 buoc 3) ─────────────────────────────
    print(f"xuat 4 file -> 06_VIDEO/{STEM}/thumb_prompts_v2_*")
    bad = 0
    for tag, p in zip(("T1", "T2", "T3"), flow):
        pos = p.find("TEXT, exactly") * 100 // len(p)
        nl = len(V[tag]["text"])
        f1 = "OK" if pos <= 15 else "🔴 TEXT ra ngoai 15% dau"
        f2 = "OK" if len(p) <= 1500 else f"⚠️ dai {len(p)} > 1500 (gate PHU)"
        f3 = "OK" if nl <= 4 else f"🔴 {nl} dong > tran 4"
        f4 = "OK" if "no watermark" in p.lower() else "🔴 thieu no watermark"
        f5 = ("OK" if "bottom-right corner free of text" in p else
              "🔴 thieu chua trong goc duoi-phai")
        bad += sum(x != "OK" for x in (f1, f3, f4, f5))   # f2 = gate PHU, khong chan
        print(f"  {tag}: {len(p):>4} ky · TEXT@{pos:>2}% · {nl} dong "
              f"| {f1} | {f2} | {f3} | {f4} | {f5}")
    print("GATE PROMPT:", "SACH" if not bad else f"🔴 {bad} loi")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
