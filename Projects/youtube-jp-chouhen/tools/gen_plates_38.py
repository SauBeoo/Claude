# -*- coding: utf-8 -*-
"""Video 38 chouhen — 3 ANH CAST PLATE (anh tham chieu nhan vat).

🔴 VI SAO KHONG DUNG `videogen_lib.plate_prompt()`:
   Ham do noi duoi bang AVOID cua VIDEO, ma AVOID do chua dung 3 cau CHONG LAI
   chinh muc dich cua anh plate:
       "not posed for the camera" / "nobody looking at the camera" / "no staged tableau"
   Plate PHAI la anh dung tao dang, nhin ve may. Kem theo la "fast cuts / camera shake /
   walking backwards / 16:9 widescreen video" — vo nghia voi anh tinh, va 16:9 lam
   nguoi bi nho trong khung.
   ⇒ Day la ca ham co san KHONG DUNG DUOC, khong phai ca "luoi doc hang so".

🔴 LOI THU HAI da vá: cu Ichinose trong C co "a blanket over his knees" (= dang NGOI)
   nhung ham cu ghep them "standing still and relaxed" => mau thuan tu the.
   Plate cua cu la anh NGOI, va bo chan ra khoi mo ta.

CACH DUNG: gen 3 anh nay TRUOC. Moi clip trong videogen_FLOW.txt co nhan vat nao
thi gui kem anh cua nhan vat do (1 anh / 1 lan gen — do la ly do tran <=2 nguoi/canh).
⇒ ANH giu HINH DANG · CHU giu HANH DONG. Da bo ta quan ao khoi prompt clip.
"""
import io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Chat lieu anh — phai CUNG the gioi voi clip (present-day Japan, anh sang tu nhien)
LOOK = ("present-day Japan, a plain honest reference photograph, true-to-life natural colour, "
        "clean and sharp, even soft frontal light with no harsh shadows, deep focus so the "
        "clothing stays readable, plain seamless light grey studio background, "
        "vertical portrait format, the whole figure inside the frame with a little space "
        "above the head and below the feet")

# AVOID rieng cho ANH — ⛔ da bo moi muc thuoc ve video
AVOID = ("Avoid: any letters, words, numbers or logos on the clothing or anywhere in the picture, "
         "brand logos, printed slogans, name tags with readable writing, "
         "props, scenery, other people, "
         "shallow blurred background, cinematic bokeh, dramatic side lighting, coloured gels, "
         "heavy make-up, glamour retouching, smoothed or plastic skin, "
         "extra fingers, deformed hands, distorted proportions, "
         "black and white, sepia, vintage film grain, any period styling earlier than today")

CAST = {
 "chizuru": dict(
   who  = "a Japanese woman in her late sixties, an ordinary retired woman, not glamorous",
   wear = "a plain dark grey zip-up fleece jacket closed to the chest, plain dark navy trousers, "
          "flat dark walking shoes, a small flat cloth shoulder bag on a long strap hanging at her hip",
   pose = "standing still and relaxed, three-quarter view turned slightly to her left, "
          "arms hanging at her sides, weight even on both feet, a calm neutral expression",
   note = "NGUOI KE — 44/68 clip la POV nen hiem khi thay ca nguoi; anh nay chu yeu "
          "khoa MAU AO + TAY AO xuat hien trong khung POV"),
 "setsuko": dict(
   who  = "a Japanese woman in her early sixties, brisk and self-important in bearing",
   wear = "a navy blue zip-up windbreaker, a plain yellow cloth armband on the left upper sleeve, "
          "a small blank white card in a clear holder on a cord round her neck, dark trousers",
   pose = "standing squarely facing the camera, three-quarter view turned slightly to her right, "
          "chin a little lifted, one hand resting flat against her own chest just below the card",
   note = "KE AC — 11 clip, 9 clip giau mat. Anh nay can ro MAU AO + BANG TAY VANG + THE DEO CO, "
          "vi ba ta luon duoc nhan ra bang ba thu do chu khong bang mat"),
 "ichinose": dict(
   who  = "a very frail Japanese man in his late eighties",
   wear = "a brown knitted cardigan over a pale checked shirt buttoned to the collar, "
          "loose grey trousers, a thin clear nasal oxygen tube looped over both ears "
          "and running down past his chin",
   pose = "SEATED on a plain wooden chair, three-quarter view turned slightly to his left, "
          "both hands resting loosely on his thighs, back slightly rounded, feet flat on the floor",
   note = "CU ONG — ca video ong ay NGOI. ⛔ Da bo 'blanket over his knees' khoi anh plate "
          "(chan la dao cu cua canh, khong phai dac diem nhan vat) va bo 'standing' "
          "vi no mau thuan voi tu the ngoi"),
}

ORDER = ["chizuru", "setsuko", "ichinose"]

def prompt(k):
    d = CAST[k]
    # 🔴 Ichinose NGOI tren ghe => khong duoc cam "furniture" o anh cua ong ay,
    #    nhung 2 nguoi kia DUNG nen van phai cam. Cam chung = mau thuan voi chinh prompt.
    extra_avoid = ("" if k == "ichinose" else " furniture,")
    head = ("full-body reference photograph of " if k != "ichinose"
            else "full-figure seated reference photograph of ")
    av = AVOID.replace("Avoid:", "Avoid:" + extra_avoid)
    if k == "ichinose":
        av += " No furniture except the single plain chair he is sitting on"
    return " ".join((f"{head}{d['who']}, wearing {d['wear']}, {d['pose']}, "
                     f"{LOOK}. {av}.").split())

OUT = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"
os.makedirs(OUT, exist_ok=True)
flow, names, blocks = [], [], []
for i, k in enumerate(ORDER, 1):
    p = prompt(k)
    flow.append(p)
    names.append(f"{i:3d}  cast_{k}.png   (A_{k.upper()})")
    blocks.append(f"## {i}. A_{k.upper()} — `cast_{k}.png`  ({len(p)} ky)\n\n"
                  f"> {CAST[k]['note']}\n\n```\n{p}\n```\n")

io.open(os.path.join(OUT, "cast_plates_FLOW.txt"), "w", encoding="utf-8").write("\n".join(flow) + "\n")
io.open(os.path.join(OUT, "cast_plates_TENFILE.txt"), "w", encoding="utf-8").write(
    "# dong FLOW.txt  ->  ten file anh\n" + "\n".join(names) + "\n")
io.open(os.path.join(OUT, "cast_plates_BLOCKS.md"), "w", encoding="utf-8").write(
    "# Video 38 — 3 anh CAST PLATE\n\n"
    "Gen 3 anh nay TRUOC. Sau do moi clip co nhan vat nao thi gui kem anh cua nhan vat do.\n"
    "**ANH giu HINH DANG · CHU giu HANH DONG** — prompt clip da bo phan ta quan ao.\n\n"
    + "\n".join(blocks))

# ── gate nho: ba cau chong-muc-dich khong duoc quay lai ──
BAD = ["not posed for the camera", "nobody looking at the camera", "no staged tableau",
       "fast cuts", "camera shake", "walking backwards", "16:9", "widescreen"]
bad = [(i + 1, b) for i, p in enumerate(flow) for b in BAD if b in p]
print("3 prompt plate | do dai:", [len(p) for p in flow])
print("gate cau chong-muc-dich:", "SACH" if not bad else bad)
print("XUAT ->", OUT, "\\cast_plates_FLOW.txt | _TENFILE.txt | _BLOCKS.md")
