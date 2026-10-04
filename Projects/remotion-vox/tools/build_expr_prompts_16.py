# -*- coding: utf-8 -*-
r"""build_expr_prompts_16.py — xuat prompt gen BIEU CAM CAT GIAY cho video 16.

    py -3 tools/build_expr_prompts_16.py

Xuat vao projects/shokutaku-16-banana/:
  expr_prompts_FLOW.txt      1 prompt / 1 DONG  -> bom thang vao extension
  expr_prompts_TENFILE.txt   dong FLOW <-> ten file phai dat
  expr_prompts_BLOCKS.md     ban nguoi doc: y nghia + MOC GHEP + vi tri tren khung

Khuon prompt lay tu lo sticker da chay duoc (banana/mugicha/zabuton/tokei):
  vat DON LE + nen TRANG PHANG + anh sang deu khong bong + chua le rong 4 phia
  -> rembg cat sach vien. Do la dieu kien SONG cua buoc cat, khong phai tham my.

⚠️ Khac lo truoc o mot cho: 3 mau co KY TU (? ! Z) nen KHONG duoc ghi "no letters".
   Doi thanh "no other text" — neu khong model se xoa luon chinh ky tu can ve.
"""
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VD = ROOT / "projects" / "shokutaku-16-banana"

BASE = ("photographed straight on from directly above against a completely plain flat "
        "pure white seamless background, even shadowless studio light, the whole piece "
        "inside the frame with generous empty white space on all four sides, sharp "
        "product photography, no watermark, no logo")
PAPER = ("cut from thick matte construction paper with slightly rough scissor-cut edges "
         "and visible paper fibre texture, flat solid colour, no gradient, no glow")

# key: (mo ta prompt, mau, nghia, moc ghep)
EXPR = [
    ("ex_itami",
     "a single jagged starburst shape with twelve sharp uneven points, like a comic "
     "impact mark, " + PAPER + ", deep brick red paper",
     "ĐAU / VA DAP", "0:26 「暗い廊下で、転びます」 + 5:22 va cham vai"),
    ("ex_mukumi",
     "a single rounded puffy blob shape with three short thick arrows pointing outward "
     "from it, like something swelling, " + PAPER + ", dusty slate blue paper",
     "SUNG / PHU", "7:46 「へこんだままなら、水がたまっています」"),
    ("ex_furatsuki",
     "a single flat spiral shape of about three turns with a rounded end, like a dizzy "
     "swirl, " + PAPER + ", mustard gold paper",
     "CHOANG / HOA MAT", "2:12 「くらっとする」"),
    ("ex_hiyari",
     "three vertical teardrop shapes of different lengths hanging side by side, like "
     "cold drips, " + PAPER + ", pale ice blue paper",
     "LANH / RON", "14:05 「廊下の床が、やけに冷たかった」"),
    ("ex_hatena",
     "a single large question mark, " + PAPER + ", deep navy paper. No other text, "
     "only the one question mark",
     "HOI / BI AN", "0:58 「あの水は、どこから来たのか」"),
    ("ex_hirameki",
     "a single large exclamation mark, " + PAPER + ", bright golden yellow paper. "
     "No other text, only the one exclamation mark",
     "VO LE / CU LAT", "8:30 xuong song + 13:46 「偶然ではありませんでした」"),
    ("ex_batsu",
     "a single thick X cross mark made of two crossed strips, " + PAPER + ", deep "
     "brick red paper. No other text, only the one X",
     "SAI / NG", "⭐ 3 loi an chuoi: 12:30 · 14:12 · 15:04 (di kem badge 一つめ/二つめ/三つめ)"),
    ("ex_maru",
     "a single thick ring shape like a hand-cut circle outline, " + PAPER + ", deep "
     "green paper. No other text, only the one circle",
     "DUNG / OK", "⭐ 21:26 mo khoi recap 「夕方の十分」 — doi trong voi ba dau X"),
    ("ex_omori",
     "a single old-fashioned rounded weight shape with a small handle on top, like a "
     "heavy stone weight, " + PAPER + ", charcoal grey paper",
     "NANG NE / MET", "0:22 「朝、体が重くありませんか」"),
    ("ex_zzz",
     "three letter Z shapes of increasing size arranged diagonally, " + PAPER + ", "
     "deep navy paper. No other text, only the three Z shapes",
     "NGU / TINH GIAC", "(du phong — chua chon cho, moi cho hop deu da co nhan khac)"),
]


def main():
    VD.mkdir(parents=True, exist_ok=True)
    flow, tenfile, blocks = [], [], []
    for i, (name, body, mean, where) in enumerate(EXPR, 1):
        p = " ".join(f"{body}, {BASE}".split())
        flow.append(p)
        tenfile.append(f"dong {i:2d} -> {name}.png   ({mean})")
        blocks.append(f"### {i}. `{name}.png` — {mean}\n\n"
                      f"- **ghep vao:** {where}\n- **{len(p)} ky**\n\n```\n{p}\n```\n")

    (VD / "expr_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (VD / "expr_prompts_TENFILE.txt").write_text("\n".join(tenfile) + "\n", encoding="utf-8")
    (VD / "expr_prompts_BLOCKS.md").write_text(
        "# Video 16 — BIEU CAM CAT GIAY (prompt gen)\n\n"
        "> Gen xong: de nguyen ten file cua tool gen, bo het vao MOT folder, roi bao\n"
        "> Claude. Claude se: doi ten theo bang TENFILE -> cat nen (rembg\n"
        "> `isnet-general-use`) -> ghep vao project.json dung moc o duoi.\n\n"
        "🔴 **Vi sao prompt bat buoc phai la VAT DON LE TREN NEN TRANG PHANG:**\n"
        "lo truoc da thu cat tu chinh anh cua video (canh bep/san nha) — rembg giu\n"
        "100% dien tich, khong tach duoc gi, vi anh documentary khong co ranh gioi\n"
        "chu the/nen. Nen trang phang la DIEU KIEN SONG cua buoc cat.\n\n"
        "⚠️ Ba mau co ky tu (`?` `!` `Z`) KHONG ghi 'no letters' ma ghi 'no other text',\n"
        "neu khong model xoa luon chinh ky tu can ve.\n\n"
        f"**Khoi chung cuoi moi prompt:**\n\n> {BASE}\n\n"
        f"**Chat lieu giay:**\n\n> {PAPER}\n\n---\n\n" + "\n".join(blocks),
        encoding="utf-8")

    print(f"OK {len(EXPR)} prompt")
    print(f"   do dai {min(len(p) for p in flow)}-{max(len(p) for p in flow)} ky")
    for f in ("expr_prompts_FLOW.txt", "expr_prompts_TENFILE.txt", "expr_prompts_BLOCKS.md"):
        print(f"   -> {(VD / f).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
