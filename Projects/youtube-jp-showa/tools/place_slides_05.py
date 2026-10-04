# -*- coding: utf-8 -*-
"""Dat anh vao slides_img/slide_NN.jpg theo dung vi tri SLIDES.json (video 05).
AI: chon file Downloads theo auto-match + OVERRIDE, cat watermark (x>=0.908W) + 16:9 -> 1376x768.
REAL: crop theo box da soi mat (bo mat nguoi), 16:9 -> 1376x768. Backup goc: _wm_orig/."""
import json, re, io, sys
from pathlib import Path
from PIL import Image
# stdout wrapper: build_scenes_05 import tu wrap
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\05_dagashiya-10en")
SRC = Path(r"C:\Users\tuana\Downloads\download (5)")
SL = json.load(open(VD.parent.parent/"03_SCRIPTS"/"05_dagashiya-10en_SLIDES.json", encoding="utf-8"))
MATCH = json.load(open(VD/"_ai_match_raw.json", encoding="utf-8"))
IMG = VD/"slides_img"; BAK = VD/"_wm_orig"; IMG.mkdir(exist_ok=True); BAK.mkdir(exist_ok=True)
CUT_X = 0.908
OVERRIDE = {
 "ai_137_smartball_table_sub": "Wooden_smart_ball_table_indoors_202608262304.jpeg",
 "ai_138_kuji_tickets_wall_sub": "Paper_lottery_tickets_on_wall_202608262304.jpeg",
 "ai_139_toy_rifle_red_sub": "Toy_rifle_on_red_counter_202608262304.jpeg",
 "ai_08_prize_jar": "Prize_tokens_stacked_in_jar_202608262304.jpeg",          # ban truoc lo mat ong gia AI
 "ai_28_hand_hesitate": "Hand_touching_paper_tickets_202608262304_2.jpeg",    # 2 ban truoc deu lo mat nguoi AI
 "ai_55_coinslot_machine_face": "Coin_slot_on_toy_machine_202608262304.jpeg",      # ban _2 co ¥100 YEN -> sai thoi dai
 "ai_116_priceboard_leaning": "Wooden_price_board_leaning_again…_202608262304.jpeg", # ban _2 chu nat
 "ai_120_weathered_signboard": "Weathered_wooden_sign_on_wall_202608262304.jpeg",    # Wooden_sign chu lo, rui ro nat
 "ai_98_needle_beside_board": "Sewing_needle_on_wooden_counter_202608262304.jpeg",   # ban 'resting' co hop chu nat
 "ai_135_storefront_a": "Candy_shop_storefront_on_street_202608262304.jpeg",
 "ai_136_storefront_b": "Candy_shop_storefront_on_street_202608262304_2.jpeg",
}
# crop box (x0,y0,x1,y1) tren anh goc — da soi mat, bo vung co mat nguoi / ao hien dai
REAL_CROP = {
 "item1_smartball_osaka": (0, 430, 600, 768),     # 600x800: chi lay dai duoi (tay+may)
 "item3_shateki_katori": (560, 250, 1600, 835),   # 1600x1200: 2/3 phai, ke giai thuong + sung
 "item9_katanuki": (700, 1700, 2300, 2600),       # 3872x2592: bang カタヌキ + tay + vun keo
}
def to169(im, box=None):
    if box: im = im.crop(box)
    W,H = im.size; tw = W; th = int(round(W*9/16))
    if th > H: th = H; tw = int(round(H*16/9))
    x0 = (W-tw)//2; y0 = (H-th)//2
    return im.crop((x0,y0,x0+tw,y0+th)).resize((1376,768), Image.LANCZOS)
def crop_wm(im):
    W,H = im.size; nw = int(W*CUT_X); nh = min(H, int(round(nw*9/16)))
    return im.crop((0,0,nw,nh)).resize((1376,768), Image.LANCZOS)
# --- gan KHONG LAP: tinh lai diem token, moi file dung dung 1 lan, uu tien cap co diem cao nhat ---
sys.path.insert(0, str(VD.parent.parent/"tools")); import build_scenes_05 as B
STOP=set("a an the of on in at with and to from its into for by no not or is are small old worn warm light soft shop showa era japanese japan wooden wood".split())
def toks(t): return {w for w in re.findall(r"[a-z]+", t.lower()) if w not in STOP and len(w)>2}
DESC={sh[0]:sh[2] for shots in B.SHOTS.values() for sh in shots if sh[3]=="ai"}
files=sorted(SRC.glob("*.jpeg")); FT={f.name: toks(re.sub(r"_2026\d+.*","",f.name).replace("_"," ").replace("…"," ")) for f in files}
need=[re.match(r"slides_img/(.+?)\.jpg", e["source"]).group(1) for e in SL if not e.get("video") and e["source"].startswith("slides_img/")]
ASSIGN=dict(OVERRIDE); taken=set(OVERRIDE.values())
pairs=[]
for n in need:
    if n in ASSIGN: continue
    dt=toks(DESC[n])
    for f,t in FT.items():
        sc=len(dt&t)/max(1,len(t)) + 0.01*len(dt&t)
        pairs.append((sc,n,f))
pairs.sort(reverse=True)
for sc,n,f in pairs:
    if n in ASSIGN or f in taken: continue
    ASSIGN[n]=f; taken.add(f)
lowc={n:round(next(sc for sc,nn,f in pairs if nn==n and f==ASSIGN[n]),2) for n in need if n not in OVERRIDE}
print("gan xong:", len(ASSIGN), "| diem thap (<0.4):", {k:v for k,v in lowc.items() if v<0.4})
n_ai=n_real=0; miss=[]; used={}
for i, e in enumerate(SL):
    if e.get("video"): continue
    src = e["source"]; dst = IMG/f"slide_{i:02d}.jpg"
    if src.startswith("real_photos/"):
        name = Path(src).stem; p = VD/"real_photos"/f"{name}.jpg"
        if not p.exists(): miss.append((i,src)); continue
        im = Image.open(p).convert("RGB"); to169(im, REAL_CROP.get(name)).save(dst, quality=95); n_real+=1
    else:
        name = re.match(r"slides_img/(.+?)\.jpg", src).group(1)
        f = ASSIGN[name]
        p = SRC/f
        if not p.exists(): miss.append((i,name,f)); continue
        used.setdefault(f, []).append(name)
        im = Image.open(p).convert("RGB"); im.save(BAK/f"slide_{i:02d}_{name}.jpg", quality=95)
        crop_wm(im).save(dst, quality=95); n_ai+=1
print(f"OK AI={n_ai} REAL={n_real} missing={len(miss)}")
for m in miss: print("  MISSING", m)
dup = {f:v for f,v in used.items() if len(v)>1}
print("file dung >1 lan:", len(dup))
for f,v in dup.items(): print("  ", f, "->", v)
json.dump(used, open(VD/"_ai_used_files.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
