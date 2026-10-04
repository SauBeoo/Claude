# -*- coding: utf-8 -*-
"""
set_pick.py — TINH field `pick` cho moi job co ten asset trung nhau, tu thu muc anh tai ve.

    python tools/set_pick.py <outdir> --json "<...>.json" --dl "<thu muc anh tai ve>" [--reverse]

🔴 VI SAO CAN: Flow tu dat caption nen nhieu anh KHAC NHAU co the TRUNG TEN. Tool Flow Batch
   doi khop DUY NHAT, gap nhom trung ten thi DUNG (co chu y — dinh sai anh = 100 credits ra
   clip sai nguoi, prompt van dung, khong mot dau hieu loi). `pick` (1-based) chi dich danh.

🔴🔴 LO TRONG BAN v1 CUA FILE NAY (bat duoc 2026-09-10, job sb_34):
   Ban dau hardcode 7 job, suy tu viec dem trung ten **GIUA 66 FRAME VOI NHAU**. Nhung bang
   chon cua Flow hien **CA PROJECT** = frame + anh tham chieu (66 + 36 = 102). Nen ten mot
   frame co the trung voi ten mot ANH THAM CHIEU — "Official documents arranged on desk" la
   ca do: trong 66 frame no chi xuat hien 1 lan, nhung trong project no co 2 anh.
   ⇒ Phai dem tren TOAN BO thu muc tai ve (102 file), khong dem trong pham vi jobs.
   📌 Bai hoc: dem trung ten phai dem trong **KHONG GIAN MA CONG CU KIA TIM KIEM**,
      khong phai trong khong gian danh sach cua minh.

📐 THU TU `pick`: khi tai ca lo ve, Windows danh duoi `_2`, `_3` cho file TRUNG TEN theo dung
   thu tu chung nam trong danh sach. Bang chung: nhom "Man stamping bank passbook" ra 1→2→3
   khop dung mach truyen (Positioning → Red Ink Strike → Finished Seal).

⚠️ MOT PHEP KIEM giai quyet ca lo: mo Flow → slot Start → go "Man stamping bank passbook"
   → xem preview HANG DAU:
     · con dau dang LO LUNG tren trang  → dung nhu file nay ghi
     · con dau ĐÃ IN, thay dau do tron  → chay lai voi --reverse
"""
import base64
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SUF = re.compile(r"[ _](\d{8,14})(?:[ _](\d{1,3}))?\.(?:jpe?g|png|webp)$", re.I)


def caption(fn):
    return SUF.sub("", fn).replace("_", " ").strip()


def order(fn):
    m = SUF.search(fn)
    return int(m.group(2)) if (m and m.group(2)) else 1


def flag(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        v = argv[i + 1] if i + 1 < len(argv) else ""
        del argv[i:i + 2]
        return v
    return default


def main():
    argv = sys.argv[1:]
    rev = "--reverse" in argv
    if rev:
        argv.remove("--reverse")
    src = flag(argv, "--json")
    dl = flag(argv, "--dl")
    if not argv or not src or not dl:
        print(__doc__); sys.exit(2)
    out = Path(argv[0])

    # ① gom TOAN BO file tai ve theo caption — day la khong gian Flow tim kiem
    groups = {}
    md5_to_fn = {}
    for fn in os.listdir(dl):
        if not re.search(r"\.(jpe?g|png|webp)$", fn, re.I):
            continue
        with open(os.path.join(dl, fn), "rb") as fh:
            md5_to_fn[hashlib.md5(fh.read()).hexdigest()] = fn
        groups.setdefault(caption(fn), []).append(fn)
    for c in groups:
        groups[c].sort(key=order)
    print(f"anh tai ve: {len(md5_to_fn)} file · {len(groups)} caption khac nhau")
    dupg = {c: v for c, v in groups.items() if len(v) > 1}
    print(f"caption co >1 anh TRONG CA PROJECT: {len(dupg)}")

    # ② md5 cua tung frame -> ten file -> vi tri trong nhom
    d = json.load(io.open(src, encoding="utf-8"))
    man = json.load(io.open(out / "_MANIFEST.json", encoding="utf-8"))
    idx2stem = {m["idx"]: m["file"][:-4] for m in man}
    stem2fn = {}
    for i, f in enumerate(d["frames"], 1):
        if i not in idx2stem:
            continue
        fn = md5_to_fn.get(hashlib.md5(base64.b64decode(f["base64"])).hexdigest())
        if fn:
            stem2fn[idx2stem[i]] = fn

    jf = out / "jobs.jsonl"
    jobs = [json.loads(l) for l in io.open(jf, encoding="utf-8") if l.strip() and not l.startswith("#")]

    setn, miss = 0, []
    for j in jobs:
        fn = stem2fn.get(j["id"])
        if not fn:
            j.pop("pick", None); miss.append(j["id"]); continue
        grp = groups.get(caption(fn), [fn])
        if len(grp) < 2:
            j.pop("pick", None); continue
        p = grp.index(fn) + 1
        j["pick"] = (len(grp) + 1 - p) if rev else p
        setn += 1

    with io.open(jf, "w", encoding="utf-8", newline="\n") as fh:
        for j in jobs:
            fh.write(json.dumps(j, ensure_ascii=False) + "\n")

    print(f"\nda dien pick cho {setn} job {'(DAO)' if rev else '(theo thu tu tai ve)'} -> {jf}")
    for j in jobs:
        if "pick" in j:
            print(f"   {j['id']:18} pick:{j['pick']}/{len(groups[caption(stem2fn[j['id']])])}"
                  f"  [{j['asset']}]")
    if miss:
        print(f"   ⚠ {len(miss)} job khong khop file tai ve nao: {miss[:5]}")


if __name__ == "__main__":
    main()
