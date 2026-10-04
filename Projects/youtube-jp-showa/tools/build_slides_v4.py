# -*- coding: utf-8 -*-
"""BAN 4s/anh: build 289 khung tu _frame_plan.json + map anh Flow.
- 43 khung tai dung (41 anh v2 da xu ly + 2 clip PD)
- 246 khung moi: map tu gen_raw (auto _map_v3.json + manual + crop-fill)
- Xoa watermark ✦ (template astroid, logic fix_gen_01) cho anh moi
- Xuat: slides_img/slide_XXX.jpg (289) + clips/clip_XXX.mp4 + 01_kyushoku_SLIDES.json (offset 4s)
"""
import json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location("fx", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_gen_01.py"))
fx = importlib.util.module_from_spec(spec)
# fix_gen_01 co main() chay khi import? no dung __main__ guard -> an toan
spec.loader.exec_module(fx)

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
V2 = os.path.join(ROOT, "06_VIDEO", "01_kyushoku_v2")
RAW = os.path.join(V2, "gen_raw")
VID = os.path.join(ROOT, "06_VIDEO", "01_kyushoku")
IMG = os.path.join(VID, "slides_img")
CLIPS = os.path.join(VID, "clips")
BK = os.path.join(V2, "_slides_v2_backup")

plan = json.load(open(os.path.join(V2, "_frame_plan.json"), encoding="utf-8"))
frames = plan["frames"]
amap = json.load(open(os.path.join(V2, "_map_v3.json"), encoding="utf-8"))  # fr_XX -> [file, score]

def raw_by_prefix(prefix):
    for f in sorted(os.listdir(RAW)):
        if f.startswith(prefix):
            return f
    raise SystemExit(f"khong thay file prefix {prefix}")

MANUAL = {
    "fr_02_3.jpg": "Aluminum_lunch_tray_on_desk_202608072116",   # [0] ban dau tien theo sort
    "fr_27_1.jpg": "Aluminum_lunch_tray_on_desk_2026080721",     # [1] — xu ly rieng ben duoi
    "fr_03_3.jpg": "Child_counting_on_wooden_desk",
    "fr_04_1.jpg": "Child_hands_over_school_desk",               # vi xu? xem note — DAO: [5] la vi xu
    "fr_03_1.jpg": "Child_playing_counting_game",
    "fr_16_5.jpg": "Children_cleaning_floor_spill",
    "fr_50_1.jpg": "Children_fighting_at_school_desk",
    "fr_33_1.jpg": "Family_having_dinner_together",
    "fr_48_6.jpg": "Hands_together_in_thanks_gesture",
    "fr_34_3.jpg": "Noodles_steaming_in_classroom",
    "fr_36_2.jpg": "Rice_cooker_opening_in_kitchen",
}
# 2 file trung prefix "Aluminum_lunch_tray_on_desk" — phan biet theo sort order
alu = sorted(f for f in os.listdir(RAW) if f.startswith("Aluminum_lunch_tray_on_desk"))
child_hands = sorted(f for f in os.listdir(RAW) if f.startswith("Child_hands_over_school_desk"))
child_count = sorted(f for f in os.listdir(RAW) if f.startswith("Child_counting_on_wooden_desk"))
child_play = sorted(f for f in os.listdir(RAW) if f.startswith("Child_playing_counting_game"))
coin_purse = sorted(f for f in os.listdir(RAW) if f.startswith("Child_hands_over_school_desk"))

MANUAL_FILES = {
    "fr_02_3.jpg": alu[0],
    "fr_27_1.jpg": alu[1] if len(alu) > 1 else alu[0],
    "fr_03_1.jpg": raw_by_prefix("Child_playing_counting_game"),
    "fr_03_3.jpg": raw_by_prefix("Child_counting_on_wooden_desk"),
    "fr_04_1.jpg": raw_by_prefix("Child_hands_over_school_desk"),  # se DAO xuong duoi neu co vi xu
    "fr_16_5.jpg": raw_by_prefix("Children_cleaning_floor_spill"),
    "fr_50_1.jpg": raw_by_prefix("Children_fighting_at_school_desk"),
    "fr_33_1.jpg": raw_by_prefix("Family_having_dinner_together"),
    "fr_48_6.jpg": raw_by_prefix("Hands_together_in_thanks_gesture"),
    "fr_34_3.jpg": raw_by_prefix("Noodles_steaming_in_classroom"),
    "fr_36_2.jpg": raw_by_prefix("Rice_cooker_opening_in_kitchen"),
}
# vi xu (Still_life? khong — anh [5] ten gi?) — anh vi xu ten "Child_hands_over_school_desk"? KHONG.
# Theo sheet: [5] = coin purse — ten file bat dau bang gi thi do (Coin/Purse/Old...)
for f in os.listdir(RAW):
    low = f.lower()
    if ("purse" in low or "coin" in low) and f not in MANUAL_FILES.values():
        MANUAL_FILES["fr_04_1.jpg"] = f
        break

# CROP-FILL cho 8 slot trong: (slot, nguon, crop frac)
V2GEN = os.path.join(V2, "gen")
CROPFILL = {
    "fr_07_2.jpg":  (os.path.join(V2GEN, "gen_G07.jpg"), (0.30, 0.25, 0.95, 0.95)),  # can vung chao dau
    "fr_07_5.jpg":  (None, None),  # lay tu anh mapped fr_07_4 crop khac vung — xu ly sau khi map
    "fr_07_10.jpg": (os.path.join(V2GEN, "gen_G52.jpg"), (0.10, 0.15, 0.75, 0.90)),  # banh tren khay tatami
    "fr_08_1.jpg":  (None, None),  # crop tu fr_08_2 mapped
    "fr_08_6.jpg":  (os.path.join(V2GEN, "gen_G09.jpg"), (0.35, 0.05, 1.00, 0.70)),  # nen bep dusk
    "fr_10_1.jpg":  (os.path.join(V2GEN, "gen_G29.jpg"), (0.30, 0.30, 1.00, 0.95)),  # bang den da blur
    "fr_26_4.jpg":  (None, None),  # crop tu fr_26_3 mapped
    "fr_42_8.jpg":  (os.path.join(V2GEN, "gen_G10.jpg"), (0.25, 0.20, 0.95, 0.90)),  # cuoi hanh lang
}
DERIVE = {"fr_07_5.jpg": "fr_07_4.jpg", "fr_08_1.jpg": "fr_08_2.jpg", "fr_26_4.jpg": "fr_26_3.jpg"}
DERIVE_CROP = (0.18, 0.22, 0.92, 0.96)  # crop lech tam de khac khung goc


def clean_new(src_path):
    im = Image.open(src_path).convert("RGB")
    im, score = fx.remove_watermark(im)
    if im.width < 1920:
        im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
    return im


def crop16_9(im, box):
    w, h = im.size
    x1, y1, x2, y2 = int(w*box[0]), int(h*box[1]), int(w*box[2]), int(h*box[3])
    cw = x2 - x1
    ch = int(cw * 9 / 16)
    if y1 + ch > h: ch = h - y1
    im = im.crop((x1, y1, x1 + cw, y1 + ch))
    return im.resize((1920, 1080), Image.LANCZOS)


def main():
    # backup slides_img v2 (59 file) 1 lan
    if not os.path.exists(BK):
        shutil.copytree(IMG, BK)
        print("backup v2 slides ->", BK)
    # don slides_img + clips (bo v2, giu backup)
    for f in os.listdir(IMG):
        os.remove(os.path.join(IMG, f))
    old_clips = {}
    for f in list(os.listdir(CLIPS)):
        p = os.path.join(CLIPS, f)
        if f in ("clip_12.mp4", "clip_53.mp4"):
            old_clips[f] = p + ".keep"
            shutil.move(p, p + ".keep")
        else:
            os.remove(p)

    E = []
    fr_slot_output = {}   # fr code -> slide index (de derive)
    stats = {"old": 0, "new": 0, "clip": 0, "fill": 0}

    # thu tu khung moi trong tung beat -> ten fr theo VISUALS (theo thu tu xuat hien trong _prompts_v3)
    P = json.load(open(os.path.join(V2, "_prompts_v3.json"), encoding="utf-8"))
    fr_order = [p["file"] for p in P]
    new_frame_indices = [i for i, f in enumerate(frames) if "src" not in f]
    assert len(new_frame_indices) == len(fr_order), (len(new_frame_indices), len(fr_order))
    frame_fr = dict(zip(new_frame_indices, fr_order))

    for i, f in enumerate(frames):
        entry = {"match": f["text"], "photo": True}
        if f["offset"] > 0:
            entry["offset"] = f["offset"]
        src = f.get("src")
        out_img = os.path.join(IMG, f"slide_{i:02d}.jpg")
        if src and src.startswith("OLD:"):
            idx = int(src.split(":")[1])
            shutil.copyfile(os.path.join(BK, f"slide_{idx:02d}.jpg"), out_img)
            stats["old"] += 1
        elif src and src.startswith("CLIP:"):
            idx = int(src.split(":")[1])
            entry.pop("photo")
            entry["video"] = True
            keep = os.path.join(CLIPS, f"clip_{idx:02d}.mp4.keep")
            shutil.copyfile(keep, os.path.join(CLIPS, f"clip_{i:02d}.mp4"))
            # anh fallback cung index (phong clip loi)
            shutil.copyfile(os.path.join(BK, "slide_00.jpg"), out_img)
            stats["clip"] += 1
        else:
            fr = frame_fr[i]
            fr_slot_output[fr] = i
            if fr in MANUAL_FILES:
                im = clean_new(os.path.join(RAW, MANUAL_FILES[fr]))
                im.save(out_img, quality=95)
                stats["new"] += 1
            elif fr in amap:
                im = clean_new(os.path.join(RAW, amap[fr][0]))
                im.save(out_img, quality=95)
                stats["new"] += 1
            elif fr in CROPFILL and CROPFILL[fr][0]:
                im = Image.open(CROPFILL[fr][0]).convert("RGB")
                crop16_9(im, CROPFILL[fr][1]).save(out_img, quality=95)
                stats["fill"] += 1
            elif fr in DERIVE:
                entry["_derive"] = fr  # xu ly vong 2 (nguon la slide da xuat)
            else:
                raise SystemExit(f"khung {i} ({fr}) khong co nguon anh!")
        E.append(entry)

    # vong 2: derive crop tu slide nguon da xuat
    for i, e in enumerate(E):
        if "_derive" in e:
            fr = e.pop("_derive")
            src_fr = DERIVE[fr]
            src_idx = fr_slot_output[src_fr]
            im = Image.open(os.path.join(IMG, f"slide_{src_idx:02d}.jpg")).convert("RGB")
            crop16_9(im, DERIVE_CROP).save(os.path.join(IMG, f"slide_{i:02d}.jpg"), quality=95)
            stats["fill"] += 1

    json.dump(E, open(os.path.join(ROOT, "03_SCRIPTS", "01_kyushoku_SLIDES.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"XONG {len(E)} entry | old {stats['old']} · new {stats['new']} · fill {stats['fill']} · clip {stats['clip']}")
    n_img = len([f for f in os.listdir(IMG) if f.startswith("slide_")])
    print(f"slides_img: {n_img} file · clips: {len([f for f in os.listdir(CLIPS) if f.endswith('.mp4')])}")


if __name__ == "__main__":
    main()
