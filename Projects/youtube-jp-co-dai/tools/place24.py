# -*- coding: utf-8 -*-
r"""Khop 78 anh tai ve <-> 78 slot cua video 24, roi copy vao dung ten.

    python tools\place24.py --src "C:\Users\tuana\Downloads\download (15)"           # XEM TRUOC
    python tools\place24.py --src "..." --apply                                      # ghi that

VI SAO KHONG DUNG MATCHER THAM LAM (bai hoc #21, 09_VIDEO_PIPELINE.md muc 4.1):
  o #21 matcher tham lam nhet anh "cua so mo, gio vao" vao slot "phong tam KHONG co cua so"
  — nguoc han nghia, khong gate nao bat duoc. Nguyen nhan: greedy chon cap tot nhat cho
  slot DAU TIEN roi khoa lai, nen slot sau phai nhan phan con lai.
  ⇒ Ban nay dung PHEP GAN TOI UU TOAN CUC (linear_sum_assignment / Hungarian): cuc dai
  TONG diem khop, moi anh dung dung 1 lan. Mot cap le vao sai thi khong keo do ca chuoi.

DOC BANG TRUOC KHI --apply. Cot DIEM thap (<0.20) = dang doan; ghim vao FORCE.
"""
import argparse, io, shutil, sys, re, os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "24_kamemushi-3mm-sukima"
VD = PROJ / "06_VIDEO" / SLUG

# Ghim tay khi matcher doan sai: {ten_slot: tien_to_ten_file_tai_ve}
FORCE = {
    # 🔴 HO CUA SO PHAI GAN BANG MAT — ten file khong chua "halfway"/"fully across",
    #    token-matching KHONG THE phan biet. Soi sheet win12.jpg roi chot tay.
    # ⚠️ ANH SO SLOT DOI KHI THEM/BOT CUE — bang nay da map lai sau khi them cue cho
    #    dong VAO BAI (2026-08-25). Them cue nua thi PHAI map lai.
    # man luoi mo HET (khung chong nhau, het khe)
    "slides_img/slide_02.jpg": "White_aluminium_sliding_window_202608252235.jpeg",
    "slides_img/slide_36.jpg": "Window_with_insect_screen_202608252235_2.jpeg",
    "slides_img/slide_63.jpg": "Sliding_window_on_wooden_veranda_202608252235.jpeg",
    "slides_img/slide_65.jpg": "Sliding_window_in_Japanese_house_202608252235.jpeg",
    "slides_img/slide_71.jpg": "Sliding_window_in_Japanese_house_202608252235_2.jpeg",
    # man luoi mo NUA (con khe doc)
    "slides_img/slide_26.jpg": "Window_with_partially_open_screen_202608252235.jpeg",
    "slides_img/slide_27.jpg": "White_aluminium_sliding_window_202608252235_3.jpeg",
    "slides_img/slide_34.jpg": "Sliding_window_on_wooden_veranda_202608252235_2.jpeg",
    "slides_img/slide_35.jpg": "Sliding_window_on_wooden_veranda_202608252235_4.jpeg",
    "slides_img/slide_64.jpg": "Window_with_insect_screen_202608252235.jpeg",
    # nen the vox "khai nao mo" — lo khong co anh ban dem
    "ai_clean/window_at_night_from_inside.jpeg": "Sliding_window_on_wooden_veranda_202608252235_3.jpeg",
    # 🔴 3 slot lo khong co ung vien dung: lo THIEU anh "cuon bang keo"
    #    (extension gen 2 tam "tay dan keo" thay vi 1 cuon) => lay tam sat nghia nhat.
    "slides_img/slide_03.jpg": "Hand_pressing_tape_into_window_202608252235.jpeg",
    "slides_img/slide_05.jpg": "Brown_insect_walking_on_wall_202608252235.jpeg",
    "slides_img/slide_10.jpg": "Stink_bug_on_wall_202608252235.jpeg",
    "slides_img/slide_07.jpg": "Brown_stink_bug_on_wall_202608252235.jpeg",
    # 2 anh keo / 3 slot keo -> the compare (nen bi lam toi sau chu) nhuong lai
    "slides_img/slide_23.jpg": "Hand_pressing_tape_along_window_202608252235.jpeg",
}

STOP = set("""a an the of on in at with and or for from to into onto by as is are
one two three four seven single plain simple ordinary japanese photorealistic
extreme close up macro photograph subject fills frame only thing visible tight
crop out focus background no room wall sky tools view unless named hard
directional light high micro detail muted warm palette calm documentary mood
horizontal text letters logos brand labels human faces watermark cinematic still
continuous story house white aluminium sliding window pale plaster wooden veranda
soft natural neutral colors shallow depth field fine quiet archival faded
gentle grain seen nobody present nothing else exactly same camera
position framing version""".split())
# 🔴 CO Y KHONG stopword: white aluminium sliding window veranda house screen sepia brown
#    — chung nam trong khoi STYLE nhung CUNG LA tu phan biet chu the. Ban dau tao stopword
#    chung => 9 slot ho cua so cham 0.00 va bi gan ngau nhien. Xem FORCE ben duoi.


def tok(s):
    s = re.sub(r"20\d{10}", " ", s)          # bo dau thoi gian trong ten file
    s = re.sub(r"_\d+$", " ", s)             # bo hau to _2 _3 cua ban trung
    s = re.sub(r"\.(jpe?g|png)$", " ", s, flags=re.I)
    w = [x.lower() for x in re.split(r"[^A-Za-z]+", s) if len(x) > 2]
    return {x for x in w if x not in STOP}


def subject_of(prompt):
    """Phan CHU THE = doan sau khoi STYLE. Moi prompt deu ket thuc style bang 'no watermark. '."""
    k = "no watermark. "
    return prompt.split(k, 1)[1] if k in prompt else prompt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    src = Path(a.src)
    if not src.is_dir():
        raise SystemExit(f"[LOI] khong thay folder: {src}")

    S = PROJ / "03_SCRIPTS"
    names = [l.split()[-1] for l in
             (S / f"{SLUG}_IMG_NAMES.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    flow = [l for l in (S / f"{SLUG}_IMG_FLOW.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
    if len(names) != len(flow):
        raise SystemExit(f"[LOI] NAMES {len(names)} != FLOW {len(flow)}")

    files = sorted(f for f in os.listdir(src)
                   if f.lower().endswith((".jpg", ".jpeg", ".png")))
    print(f"slot {len(names)} | anh {len(files)}")
    if len(files) < len(names):
        print(f"  ⚠ THIEU {len(names)-len(files)} anh — se co slot bo trong")

    # ── ghim tay truoc ────────────────────────────────────────────────────────
    fixed = {}
    for slot, pref in FORCE.items():
        if slot not in names:
            raise SystemExit(f"[LOI] FORCE: slot khong ton tai: {slot}")
        hit = [f for f in files if f.startswith(pref)]
        if len(hit) != 1:
            raise SystemExit(f"[LOI] FORCE {slot}: {len(hit)} file bat dau bang {pref!r}")
        fixed[names.index(slot)] = hit[0]

    free_slots = [i for i in range(len(names)) if i not in fixed]
    free_files = [f for f in files if f not in fixed.values()]

    # ── phep gan toi uu toan cuc ──────────────────────────────────────────────
    subj = [tok(subject_of(flow[i])) for i in free_slots]
    ftok = [tok(f) for f in free_files]
    import numpy as np
    from scipy.optimize import linear_sum_assignment
    n, m = len(free_slots), len(free_files)
    C = np.zeros((n, m))
    for r in range(n):
        for c in range(m):
            inter = len(subj[r] & ftok[c])
            denom = (len(subj[r]) * len(ftok[c])) ** 0.5 or 1
            C[r, c] = inter / denom
    rr, cc = linear_sum_assignment(-C)
    pair = dict(fixed)
    score = {}
    for r, c in zip(rr, cc):
        pair[free_slots[r]] = free_files[c]
        score[free_slots[r]] = C[r, c]

    # ── bang doc bang mat ─────────────────────────────────────────────────────
    print()
    weak = 0
    for i, nm in enumerate(names):
        f = pair.get(i)
        sc = score.get(i, 9.99)
        flag = "GHIM" if i in fixed else ("  🔴" if sc < 0.20 else ("  ⚠" if sc < 0.32 else "    "))
        if sc < 0.20 and i not in fixed:
            weak += 1
        print(f"{i+1:3d} {flag} {sc if sc < 9 else 0:.2f}  {nm:42s} <- {f}")
        print(f"              {subject_of(flow[i])[:104]}")
    print(f"\ndiem <0.20 (dang doan, nen ghim FORCE): {weak}")

    if not a.apply:
        print("\n(XEM TRUOC — chua ghi gi. Doc bang tren, sai thi them vao FORCE, roi chay lai voi --apply)")
        return

    for sub in ("slides_img", "ai_clean"):
        (VD / sub).mkdir(parents=True, exist_ok=True)
    nw = 0
    for i, nm in enumerate(names):
        f = pair.get(i)
        if not f:
            continue
        dst = VD / nm
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / f, dst)
        nw += 1
    print(f"\nda ghi {nw} anh vao {VD}")
    print("BUOC KE TIEP: python tools\\strip_wm_crop.py 06_VIDEO\\%s --cut 0.900" % SLUG)
    print("  (✦ lo nay do duoc o x 1255-1302 = 0.912W-0.946W, y 647-694 — cong trung binh 78 anh)")


if __name__ == "__main__":
    main()
