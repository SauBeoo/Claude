# -*- coding: utf-8 -*-
"""GHEP 289 ANH <-> 289 CANH cua video 38.

🔴 VI SAO PHAI CO TOOL NAY: anh tai ve theo LO (ZIP) nen MAT thu tu gen.
   Do duoc: Spearman(vi tri ZIP, canh khop nhat) = -0,011 (khong tuong quan),
   va margin top1-top2 khi ghep bang TEN FILE = 0,0 (ten qua ngan, 70 ten bi cat,
   23 ten trung nhau) => ghep bang ten la doan mo.
   => Nguon su that la NHAN SOI BANG MAT: `06_VIDEO/38_.../IMG_LABELS.txt`.

CACH GHEP: bai toan GAN 1-1 (Hungarian) tren diem tuong dong
   ① BOI CANH  (nang nhat — 6/12 nhom dem ra khop chinh xac tuyet doi voi so canh)
   ② POV hay khong (doc duoc ngay: co tay ao xam o mep duoi khung khong)
   ③ NHAN VAT thay duoc (Setsuko ao navy + bang vang · Ichinose ong gia + oxy ·
      Mago hoodie · vest · Gyosha ao mua · dong nguoi)

⚠️ GIOI HAN, noi truoc: trong MOT nhom co nhieu anh cung thuoc tinh thi thu tu
   giua chung la TUY Y — khong co tin hieu nao tach duoc. Sai trong nhom = hinh van
   dung boi canh, dung nguoi, chi lech HANH DONG. Sai CHEO nhom moi la sai that,
   va do la cai ma diem ① chan.
"""
import sys, os, re, io, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import numpy as np
from scipy.optimize import linear_sum_assignment

VD = r"E:\Claude\Projects\youtube-jp-chouhen\06_VIDEO\38_enpitsu-no-meibo"
IMGDIR = r"C:\Users\tuana\Downloads\Tháng 9 17 - 19_43"

# ── 1. doc nhan anh ───────────────────────────────────────────────────────────
labels = {}
for ln in io.open(os.path.join(VD, "IMG_LABELS.txt"), encoding="utf-8"):
    ln = ln.strip()
    if not ln or ln.startswith("#"):
        continue
    p = ln.split()
    labels[int(p[0])] = {"preset": p[1], "pov": p[2] == "1", "ch": set(p[3:]) - {"-"}}
print("nhan anh:", len(labels))

fs = sorted(glob.glob(os.path.join(IMGDIR, "*.jpeg")), key=lambda p: os.path.getmtime(p))
assert len(fs) == len(labels), "so anh khac so nhan"

# ── 2. doc canh ───────────────────────────────────────────────────────────────
txt = io.open(os.path.join(VD, "imggen_BLOCKS.md"), encoding="utf-8").read()
rows = re.findall(r"## (\d+)\. (\S+) \[(.*?) · (.*?) · (.*?)\]\n\n- \*\*ACT:\*\* (.*?)\n- \*\*FRAMING:\*\* (.*?)\n",
                  txt)
PRE = {"taiikukan": "TK", "uketsuke": "UK", "rouka": "RK", "sumi": "SM", "souko": "SK",
       "shokuin": "SJ", "soto": "ST", "asa": "AS", "supa": "SP", "haru": "HR",
       "genkan": "GK", "keijiban": "KJ"}
scenes = []
for n, sid, blk, preset, _t, act, fr in rows:
    ch = set()
    if "A_SETSUKO" in act or "navy jacket" in act or "navy blue windbreaker" in act:
        ch.add("S")
    if "A_ICHINOSE" in act or "oxygen" in act or "old man" in act:
        ch.add("I")
    if "A_MAGO" in act:
        ch.add("M")
    if "A_SHITSUCHO" in act or "A_KYOTO" in act or "suit" in act:
        ch.add("V")
    if "A_GYOSHA" in act or "A_KAICHO" in act:
        ch.add("G")
    if re.search(r"famil|evacuee|people|queue|line of|crowd|heads|rows of bedding", act, re.I):
        ch.add("C")
    pov = ("first-person" in fr) or ("their own" in act)
    scenes.append({"n": int(n), "sid": sid, "blk": blk,
                   "preset": PRE.get(preset, preset[:2].upper()),
                   "pov": pov, "ch": ch, "act": act})
scenes.sort(key=lambda s: s["n"])
print("canh:", len(scenes))

# ── 3. ma tran diem ───────────────────────────────────────────────────────────
NEAR = {("AS", "TK"), ("TK", "AS"), ("UK", "TK"), ("TK", "UK"),
        ("RK", "TK"), ("TK", "RK"), ("SM", "TK"), ("TK", "SM"),
        ("HR", "AS"), ("AS", "HR"), ("UK", "AS"), ("AS", "UK"),
        ("UK", "SJ"), ("SJ", "UK"), ("HR", "TK"), ("TK", "HR")}
ids = sorted(labels)
S = np.zeros((len(ids), len(scenes)))
for i, im in enumerate(ids):
    L = labels[im]
    for j, sc in enumerate(scenes):
        s = 0.0
        if L["preset"] == sc["preset"]:
            s += 30
        elif (L["preset"], sc["preset"]) in NEAR:
            s += 2
        else:
            s -= 60
        s += 6 if L["pov"] == sc["pov"] else -6
        for c in "SIMVG":
            a, b = c in L["ch"], c in sc["ch"]
            if a and b:
                s += 5
            elif a != b:
                s -= 2
        if ("C" in L["ch"]) == ("C" in sc["ch"]):
            s += 1
        S[i, j] = s

r, c = linear_sum_assignment(-S)
pair = {ids[i]: scenes[j] for i, j in zip(r, c)}
tot = S[r, c].sum()
same = sum(1 for i, j in zip(r, c) if labels[ids[i]]["preset"] == scenes[j]["preset"])
povok = sum(1 for i, j in zip(r, c) if labels[ids[i]]["pov"] == scenes[j]["pov"])
print("diem tong: %.0f | khop BOI CANH: %d/%d (%.0f%%) | khop POV: %d/%d (%.0f%%)"
      % (tot, same, len(ids), same * 100 / len(ids), povok, len(ids), povok * 100 / len(ids)))

bad = [(ids[i], labels[ids[i]]["preset"], scenes[j]["n"], scenes[j]["sid"], scenes[j]["preset"])
       for i, j in zip(r, c) if labels[ids[i]]["preset"] != scenes[j]["preset"]]
print("\nLECH BOI CANH (%d):" % len(bad))
for b in bad:
    print("   anh #%-3d %s  ->  canh %3d %s (%s)" % b)

# ── 4. xuat ban do ────────────────────────────────────────────────────────────
inv = {}
for im, sc in pair.items():
    inv[sc["n"]] = im
with io.open(os.path.join(VD, "IMG_ASSIGN.txt"), "w", encoding="utf-8") as f:
    f.write("# canh -> anh (id = thu tu file trong ZIP)\n")
    f.write("# sinh boi tools/match_imgs_38.py tu IMG_LABELS.txt (nhan soi bang MAT)\n")
    for sc in scenes:
        im = inv[sc["n"]]
        f.write("%3d  %-6s %-3s pov=%d  <-  anh #%-3d  %s\n"
                % (sc["n"], sc["sid"], sc["preset"], sc["pov"], im,
                   os.path.basename(fs[im - 1])))
print("\n-> IMG_ASSIGN.txt")
