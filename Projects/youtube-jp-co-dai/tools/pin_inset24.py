# -*- coding: utf-8 -*-
r"""Ghim TAY 6 khung ve `inset` cho video 24, sau khi autofocus da chay.

VI SAO CAN: autofocus do "ty le chi tiet" cua anh va ha 18/28 entry tu inset ve soft
vi anh "phang deu". Do dung ve KY THUAT (phong to vung khong co gi thi vo hat), nhung
no KHONG biet cau thoai dang YEU CAU nguoi xem nhin vao mot cho cu the. 6 khung duoi
day la nhung cau ma CHI TIET CHINH LA NOI DUNG:

  e2  「網戸を半分で止めず、いっぱいまで開けて寄せてください」 -> khung chong nhau
  e3  「時期を過ぎてから隙間をふさぐと、逆効果」               -> cho bang keo bit khe
  e35 「網戸の枠と、ガラス戸の枠が、重ならない場所ができます」 -> DUNG cho khong chong
  e36 「枠と枠が重なって、その線が消えます」                   -> cho line bien mat
  e63 「網戸をいっぱいまで寄せることと、戸車のねじを回すこと」 -> khung + ray
  e64 「網戸をいっぱいに開けても、まだ隙間が残る場合があります」-> khe doc con lai

THU TU BAT BUOC:  gen_slides -> autofocus --apply -> pin_inset24 --apply -> add_fx --apply
Chay pin TRUOC autofocus la vo ich (autofocus ghi de mode/focus).
Chay lai gen_slides la XOA het (pipeline muc 0).

Toa do doc bang MAT tren luoi 10x10 (scratchpad/pin6.jpg), khong phai do bang may.
"""
import argparse, io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
S = Path(r"E:\Claude\Projects\youtube-jp-co-dai\03_SCRIPTS\24_kamemushi-3mm-sukima_SLIDES.json")

# entry -> (focus [cx, cy, r], vi tri card). Card luon dat PHIA DOI DIEN vung nhin
# (pipeline muc 2) de mui ten di tu card sang chu the, khong cat ngang no.
PIN = {
    # 🔴 CHI CON e3. Demo cho thay 5 khung CUA SO TOAN CANH inset KHONG chay duoc:
    #    thu can phong la KHE 3mm, tren anh 1238px no rong 2-3 pixel => phong len chi
    #    ra "mep cua + bui cay". Va toa do tao doc tu LUOI TREN SHEET 620px — o co do
    #    khe do khong the dinh vi noi (dung bai hoc "sheet thu nho cho qua loi",
    #    media-library.md 2.10-6). 4 khung do da chuyen sang CALLOUT trong callout24.py.
    #    e3 giu lai vi chi tiet la BAN TAY DAN KEO — to, thay ro khi phong.
    3:  ([0.70, 0.55, 0.15], "bl"),
}

ap = argparse.ArgumentParser()
ap.add_argument("--apply", action="store_true")
a = ap.parse_args()

d = json.loads(S.read_text(encoding="utf-8"))
n = 0
for i, (foc, pos) in PIN.items():
    if i >= len(d):
        raise SystemExit(f"[LOI] entry {i} khong ton tai (SLIDES co {len(d)}) — "
                         "so entry da doi, PHAI ghim lai bang mat")
    e = d[i]
    s = e.get("shot")
    if not isinstance(s, dict):
        raise SystemExit(f"[LOI] entry {i} khong phai entry anh (co the la the vox) — "
                         "so entry da doi, PHAI ghim lai bang mat")
    if s.get("avatar"):
        print(f"  e{i}: BO QUA — co avatar (avatar + card inset = 3 lop chong nhau)")
        continue
    old = s.get("mode")
    s["mode"] = "inset"
    s["focus"] = foc
    s["inset_pos"] = pos
    print(f"  e{i:<3} {old:>6} -> inset  focus={foc}  card={pos}  {e['match'][:26]}")
    n += 1

if a.apply:
    S.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[OK] ghim {n} khung -> {S.name}")
    print("BUOC KE TIEP: add_fx --apply, roi DUNG LAI DEMO (e2/e3 nam trong 95s dau)")
else:
    print(f"(XEM TRUOC — chua ghi. {n} khung se doi sang inset)")
