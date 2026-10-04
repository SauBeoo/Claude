# -*- coding: utf-8 -*-
r"""GATE DAN DIEN — moi kich ban mot DAN MAT KHAC, trong mot kich ban thi DONG NHAT.

    python tools\check_cast_unique.py 16          # kiem video 16
    python tools\check_cast_unique.py 16 --write   # kiem xong ghi vao so dang ky

🔴 VI SAO CO TOOL NAY (user bat 2026-09-18: *"mat cua cac nhan vat no dong nhat gan giong
   cac video cu"*). Do lai 4 video thi ra HAI nguyen nhan tach biet:

   ① CHEP NGUYEN VAN giua cac video — `haha` va `chichi` cua video 16 trung TUNG KY TU voi
     video 15. Loi thi hanh, de thay.
   ② ⭐ NANG HON: **khong mot cast nao cua 13/14/15/16 ta KHUON MAT.** Tat ca chi ta QUAN AO
     ("a woman in her forties in a white cook's smock..."). Model khong duoc cho mot khuon
     mat nao thi no roi ve **mat mac dinh cua phong cach do** => video 13 va 14 quan ao khac
     hoan toan ma mat van giong nhau. Doi quan ao KHONG chua duoc benh nay.

   ⇒ Tu nay moi cast phai co ca hai phan: **MAT (khong doi trong video) + DO (co the doi
     theo boi canh)**, va phan MAT phai KHAC voi moi video truoc.

⚖️ Gioi han da biet, ghi thang: t2v **khong khoa duoc mat** (gate cua videogen_lib da canh
   bao rieng dieu nay). Ta mat khong bien no thanh character-lock — no chi keo phan bo ve
   mot vung khac nhau giua cac video, va giu cho MOT video khoi troi lung tung. Thu that su
   khoa duoc danh tinh van la: giau mat, canh xa, quay lung, POV.
"""
import argparse, io, json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

TOOLS = Path(__file__).resolve().parent
REG = TOOLS / "CAST_REGISTRY.json"

# tu khoa chung to co ta KHUON MAT (khong phai quan ao)
FACE_WORDS = re.compile(
    r"\b(face|jaw|jawline|chin|brow|brows|eyebrow\w*|eyes?|eyelid\w*|cheek\w*|cheekbone\w*|"
    r"nose|mouth|lips?|forehead|temple\w*|complexion|skin|freckl\w*|wrinkl\w*|lines? (?:round|around|from)|"
    r"hairline|balding|receding|moustache|beard|stubble)\b", re.I)

# tu khoa chi la QUAN AO — de canh bao khi cast CHI co pha nay
CLOTH_WORDS = re.compile(
    r"\b(shirt|blouse|smock|apron|kimono|cardigan|jacket|suit|tie|trousers|skirt|dress|"
    r"coat|cap|hat|shorts|undershirt|haori|sash|pinafore|uniform)\b", re.I)

STOP = set("a an the in of and or with over under on at to his her their its one two plain "
           "very slightly about into from for as by is are be been that this".split())


def cast_of(path: Path):
    """Trich dict C tu mot gen_prompts_*.py ma KHONG chay file (tranh moi tac dung phu)."""
    s = io.open(path, encoding="utf-8").read()
    m = re.search(r"\nC = \{(.*?)\n\}", s, re.S)
    if not m:
        return {}
    out = {}
    for mm in re.finditer(r"""["'](\w+)["']\s*:\s*(["'])(.*?)\2\s*,""", m.group(1), re.S):
        key, val = mm.group(1), mm.group(3)
        if re.search(r"_pov", key):          # bien the POV: ta tay ao, khong phai danh tinh
            continue
        out[key] = " ".join(val.split())
    return out


def toks(s):
    return {w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2}


def jaccard(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / max(1, len(A | B))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="so thu tu video, vd 16")
    ap.add_argument("--write", action="store_true", help="ghi dan dien nay vao so dang ky")
    ap.add_argument("--force", action="store_true",
                    help="ghi DU con loi chan — CHI dung de nap video CU (13/14/15) vao so: chung "
                         "khong co mo ta mat, nhung van phai nam trong so de video sau khong chep "
                         "lai QUAN AO cua chung")
    ap.add_argument("--max-overlap", type=float, default=0.50,
                    help="tran trung tu giua mot cast va cast bat ky cua video KHAC")
    a = ap.parse_args()

    f = TOOLS / ("gen_prompts_%s.py" % a.video)
    if not f.exists():
        sys.exit("[LOI] khong thay %s" % f)
    C = cast_of(f)
    if not C:
        sys.exit("[LOI] khong doc duoc dict C trong %s" % f.name)

    reg = json.loads(io.open(REG, encoding="utf-8").read()) if REG.exists() else {}

    red, warn = [], []

    # --- 1. moi cast phai co phan KHUON MAT ---
    for k, v in sorted(C.items()):
        if not FACE_WORDS.search(v):
            red.append((k, "KHONG ta khuon mat — chi co do mac. Model se dung mat mac dinh "
                           "=> giong het video truoc"))
        elif not CLOTH_WORDS.search(v):
            warn.append((k, "co mat nhung khong co do mac"))

    # --- 2. khong duoc trung voi video KHAC ---
    for k, v in sorted(C.items()):
        worst = None
        for vid, cast in reg.items():
            if str(vid) == str(a.video):
                continue
            for k2, v2 in cast.items():
                j = jaccard(v, v2)
                if worst is None or j > worst[0]:
                    worst = (j, vid, k2)
        if worst and worst[0] >= a.max_overlap:
            j, vid, k2 = worst
            (red if j >= 0.80 else warn).append(
                (k, "trung %.0f%% tu voi video %s cast '%s'" % (j * 100, vid, k2)))

    # --- 3. trong CUNG video, hai cast khong duoc gan het nhau ---
    ks = sorted(C)
    for i in range(len(ks)):
        for j2 in range(i + 1, len(ks)):
            jj = jaccard(C[ks[i]], C[ks[j2]])
            if jj >= 0.70:
                warn.append((ks[i], "gan trung cast '%s' cung video (%.0f%%) — hai nguoi se"
                                    " nhin nhu mot" % (ks[j2], jj * 100)))

    print("=== GATE DAN DIEN — video %s (%d cast) ===" % (a.video, len(C)))
    for k, m in red:
        print("  🔴 %-12s %s" % (k, m))
    for k, m in warn:
        print("  ⚠️  %-12s %s" % (k, m))
    if not red and not warn:
        print("  (khong co gi)")
    print("-" * 62)
    print("da dang ky truoc do: %s" % (", ".join(sorted(reg, key=str)) or "(so trong)"))
    print("KET QUA: %s" % ("SACH" if not red else "%d LOI CHAN" % len(red)))

    if a.write:
        if red and not a.force:
            print("\n[TU CHOI GHI] con loi chan — sua xong roi ghi, dung de so nhiem ban.")
            return 1
        if red:
            print("\n[GHI DI SAN] con %d loi chan nhung --force: ghi de video sau doi chieu." % len(red))
        reg[str(a.video)] = C
        io.open(REG, "w", encoding="utf-8").write(
            json.dumps(reg, ensure_ascii=False, indent=1))
        print("\nda ghi %d cast cua video %s vao %s" % (len(C), a.video, REG.name))
    return 0 if not red else 1


if __name__ == "__main__":
    sys.exit(main())
