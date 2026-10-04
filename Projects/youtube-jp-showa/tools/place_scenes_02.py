# -*- coding: utf-8 -*-
"""Ghep 42 anh user gen -> slides_img/slide_XX.jpg cho video 02 + contact sheet duyet mat.

Map theo NOI DUNG (ten file gen do model dat, khong theo thu tu prompt).
Chay: python tools/place_scenes_02.py [--src "<folder>"]
"""
import io, sys, shutil, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "02_kieta-mise"
DST = VD / "slides_img"
FONT = r"E:\Claude\Projects\_media_library\fonts\NotoSansJP-Black.otf"

# slide_XX  <-  khoa nhan dang trong ten file gen (duy nhat)
MAP = [
    "Shopping_street_with_distant", "Milk_box_mounted_beside_house", "Finger_pressing_milk_bottle_cap",
    "Hands_arranging_paper_milk_caps", "Two_figures_at_shop_counter", "Shopkeeper_and_customer_talking",
    "Closed_shutter_between_open_shops", "Brass_horn_hanging_on_handcart", "Hands_holding_pot_with_tofu",
    "Okara_crumbs_in_paper_bag", "Steaming_vat_in_tofu_workshop", "Delivery_man_holding_notebook",
    "Rice_pouring_into_wooden_bin", "Ledger_notebook_on_shop_counter", "Interior_of_traditional_rice_shop",
    "Glass_bottle_and_metal_funnel", "Galvanised_tin_buckets_stacked", "Mosquito_coil_burning_in_room",
    "Hand_saw_cutting_ice_block", "Ice_inside_old_wooden_icebox", "Hand-cranked_ice_shaver_on_counter",
    "Electric_refrigerator_standing", "Shoppers_on_crowded_street", "Closed_shutters_on_shopping_street",
    "Supermarket_aisle_with_stocked", "Child_holding_coin_over_lottery", "Figure_inside_dark_sweet_shop",
    "Assorted_penny_sweets_in_shop", "Repairing_umbrella_frame", "Hands_threading_fabric_into_geta",
    "Cobbler_repairing_shoe", "Small_book_lending_shop_interior", "Magazines_on_shopping_street",
    "Light_between_tall_bookshelves", "Figure_seated_inside_service_window", "Red_public_telephone_on_shelf",
    "Figure_pointing_down_road", "Hand_pulling_vacuum_tube_from", "Ledger_and_banknotes_on_table",
    "People_watching_television_in_room", "Steam_rising_from_tofu_shop", "Lit_lanterns_on_shopping_street",
]

# Anh GEN LAI (dat de len ban tim thay trong --src). Them 1 dong moi khi gen lai anh nao.
OVERRIDE = {
    33: r"C:\Users\tuana\Downloads\Dust_motes_floating_in_bookstore_202608102305.jpeg",
    # 09: ban cu co siro do NAU SAM (giong mau kho o co nho) -> gen lai do tuoi
    20:  r"C:\Users\tuana\Downloads\Ice_shaver_on_shop_counter_202608102327.jpeg",
    # 39: ban cu co bien 「藤原豆腐店」 = tiem trong Initial D, lai o dung cau payoff
    40: r"C:\Users\tuana\Downloads\Steam_drifting_from_tofu_shop_202608102327.jpeg",
}

ap = argparse.ArgumentParser()
ap.add_argument("--src", default=r"C:\Users\tuana\Downloads\download (1)")
a = ap.parse_args()
SRC = Path(a.src)

files = sorted(p for p in SRC.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png"))
print(f"nguon: {SRC}  ({len(files)} anh)")

DST.mkdir(parents=True, exist_ok=True)
placed, missing, used = [], [], set()
for i, key in enumerate(MAP):
    if i in OVERRIDE:
        ov = Path(OVERRIDE[i])
        if not ov.exists():
            missing.append((i, f"OVERRIDE thieu file: {ov.name}")); placed.append(None); continue
        hit = [ov]
        print(f"  ↻ slide_{i:02d}: dung ban GEN LAI ({ov.name})")
    else:
        hit = [p for p in files if key.lower() in p.name.lower() and p not in used]
    if not hit:
        missing.append((i, key)); placed.append(None); continue
    if len(hit) > 1:
        print(f"  ⚠ slide_{i:02d}: {len(hit)} anh khop '{key}' -> lay ban dau")
    src = hit[0]; used.add(src)
    dst = DST / f"slide_{i:02d}.jpg"
    im = Image.open(src).convert("RGB")
    if im.size != (1920, 1080):                 # chuan hoa ve 16:9 1920x1080
        w, h = im.size
        s = max(1920 / w, 1080 / h)
        im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
        l, t = (im.width - 1920) // 2, (im.height - 1080) // 2
        im = im.crop((l, t, l + 1920, t + 1080))
    # 🔴 CAT WATERMARK ✦ (goc duoi phai) + vien den mep — PHAI nam TRONG tool.
    #    2026-08-10: buoc nay tung lam roi ben ngoai -> chay lai tool la mat sach,
    #    ca 42 anh quay ve ban dinh watermark ma khong mot dong canh bao.
    im = im.crop((14, 45, 1750, 1029)).resize((1920, 1080), Image.LANCZOS)
    im.save(dst, quality=94)
    placed.append(dst)

print(f"\nda dat: {sum(1 for p in placed if p)}/{len(MAP)}")
if missing:
    print("🔴 THIEU:")
    for i, k in missing: print(f"   slide_{i:02d}  <- '{k}'")
leftover = [p.name for p in files if p not in used]
if leftover:
    print(f"⚠ {len(leftover)} anh nguon khong dung den:")
    for n in leftover: print("   ", n)

# ---- contact sheet duyet mat (media-library §2.1) ----
COLS, TW, TH = 6, 320, 180
rows = (len(MAP) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * TW, rows * (TH + 26)), (18, 18, 18))
d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype(FONT, 17)
except Exception: f = ImageFont.load_default()
for i, p in enumerate(placed):
    x, y = (i % COLS) * TW, (i // COLS) * (TH + 26)
    if p:
        sheet.paste(Image.open(p).resize((TW, TH), Image.LANCZOS), (x, y))
    else:
        d.rectangle([x, y, x + TW - 2, y + TH], fill=(120, 90, 0))
        d.text((x + 10, y + TH // 2), "THIEU", font=f, fill=(255, 255, 255))
    d.text((x + 6, y + TH + 4), f"{i:02d}", font=f, fill=(240, 200, 90))
out = VD / "_scene_sheet.jpg"
sheet.save(out, quality=88)
print(f"\n-> contact sheet: {out}")
print("   ⛔ DUYET BANG MAT truoc khi render (media-library §2.1)")
