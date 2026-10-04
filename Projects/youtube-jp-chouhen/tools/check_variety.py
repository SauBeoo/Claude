# -*- coding: utf-8 -*-
"""check_variety.py — GATE XOAY KHUON 5 TRUC cho kenh chouhen.

Luat: .claude/skills/script-chouhen/SKILL.md MUC 11B (chot 2026-08-29).
Ly do ton tai: MUC 11 chi ep doi CHI TIET, khong ep doi LOAI TRUYEN
-> 27 script deu "qua gate 8/10" ma van ra cung mot mo-tip (do duoc:
san khau nghi le 11/13 bai gan nhat, ke ac trong nha 25/27, vat chung giay to 27/27).

Dung:
  python tools/check_variety.py --table [-n 8]     # xem 5 truc cua N bai gan nhat (chay TRUOC khi viet)
  python tools/check_variety.py <slug|duong_dan>   # gate mot script (exit 1 = chan)
"""
import sys, os, re, glob, io, argparse

try:  # console Windows mac dinh cp1252 -> vo chu Nhat
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AXES = ["T1", "T2", "T3", "T4", "T5"]
AXIS_NAME = {"T1": "舞台", "T2": "悪役", "T3": "物証", "T4": "逆転機構", "T5": "時間構造"}
# Gia tri da chiem ~90% kho -> toi da 1 lan trong 5 bai gan nhat
OVERLOADED = {"儀式", "家族", "紙", "供給停止", "直線+回想"}
WINDOW = 5           # so bai gan nhat dung lam moc so sanh
NEED_NEW = 3         # toi thieu so truc phai khac het cua sổ
MAX_STREAK = 2       # mot gia tri toi da 2 bai LIEN TIEP

# --- suy doan truc cho script CU (chua khai bao) - danh dau ~ de khong nham voi khai bao that
GUESS = {
 "T1": [("儀式", r"座敷|広間|仏間|法事|通夜|三回忌|四十九日|お盆|祝賀|式典|披露宴|還暦|傘寿|お祝い"),
        ("病室", r"病室|待合|救急|ナースステーション|四人部屋"),
        ("車内", r"車内|高速バス|新幹線|フェリー|バスツアー"),
        ("職場", r"朝礼|会議室|取引先|支店|現場|事務所"),
        ("店頭", r"レジ|サービスカウンター|店頭|売り場"),
        ("集合住宅", r"理事会|管理組合|ゴミ置き場"),
        ("教室", r"教室|保護者会|ＰＴＡ|PTA"),
        ("役所", r"窓口|調停室|市役所")],
 "T2": [("家族", r"義母|義父|姑|舅|義姉|義兄|義妹|義弟|夫|嫁|親族"),
        ("職", r"上司|部長|専務|同僚|取引先|支店長"),
        ("旧知", r"同窓会|同級生|幼なじみ"),
        ("地縁", r"隣人|町内会|自治会|管理組合"),
        ("業者", r"施設長|ケアマネ|リフォーム|業者"),
        ("他人", r"客|乗客|隣のベッド|見知らぬ")],
 "T3": [("紙", r"帳簿|登記簿|領収書|遺言|通知書|証書|契約書|議事録|手帳|判子|印鑑|届|証明書"),
        ("音", r"録音|ベル|咳|足音|声を覚え"),
        ("映像", r"ドラレコ|防犯カメラ|録画|スマホの動画"),
        ("身体", r"傷跡|利き手|匂い|字の癖"),
        ("技能", r"見立て|職業的|寸法|脈"),
        ("物", r"道具|靴|器")],
}


def scripts():
    """Tra ve [(sort_key, slug, path)] moi -> cu."""
    out, seen = [], set()
    pats = [os.path.join(ROOT, "03_SCRIPTS", "*.md"),
            os.path.join(ROOT, "07_UPLOADED", "*", "_scripts", "*.md")]
    for p in pats:
        for f in glob.glob(p):
            b = os.path.basename(f)
            if "_TTS" in b or b.startswith("_"):
                continue
            slug = os.path.splitext(b)[0]
            if slug in seen:
                continue
            seen.add(slug)
            m = re.match(r"(\d+)", slug)
            out.append((int(m.group(1)) if m else -1, slug, f))
    out.sort(key=lambda x: -x[0])
    return out


def read_axes(path):
    """(dict truc, da_khai_bao?)"""
    try:
        s = io.open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return {}, False
    m = re.search(r"\*\*Tr[uụ]c 5T:\*\*(.+)", s)
    if m:
        d = {}
        for part in m.group(1).split("·"):
            mm = re.search(r"(T[1-5])\s*=\s*([^\s·]+)", part.strip())
            if mm:
                d[mm.group(1)] = mm.group(2).strip()
        if len(d) == 5:
            return d, True
    d = {}
    for ax, rules in GUESS.items():
        best, bn = "?", 0
        for name, rx in rules:
            n = len(re.findall(rx, s))
            if n > bn:
                best, bn = name, n
        d[ax] = "~" + best if best != "?" else "?"
    d.setdefault("T4", "?")
    d.setdefault("T5", "?")
    return d, False


def table(n):
    print("BANG 5 TRUC — %d bai gan nhat  (~ = suy doan tu tu khoa, khong phai khai bao)\n" % n)
    hdr = "%-30s" % "script" + "".join("%-14s" % ("%s %s" % (a, AXIS_NAME[a])) for a in AXES)
    print(hdr); print("-" * len(hdr))
    rows = []
    for _, slug, path in scripts()[:n]:
        d, decl = read_axes(path)
        rows.append(d)
        print("%-30s" % slug[:29] + "".join("%-14s" % d.get(a, "?") for a in AXES) + ("" if decl else "  (suy doan)"))
    print("\nTAN SUAT trong %d bai — gia tri nao dong nghia PHAI TRANH:" % n)
    for a in AXES:
        c = {}
        for d in rows:
            v = d.get(a, "?").lstrip("~")
            c[v] = c.get(v, 0) + 1
        top = sorted(c.items(), key=lambda x: -x[1])
        print("  %s %-8s %s" % (a, AXIS_NAME[a], "  ".join("%s×%d%s" % (k, v, " ⛔" if k in OVERLOADED else "") for k, v in top)))


def gate(target):
    allx = scripts()
    hit = None
    for i, (_, slug, path) in enumerate(allx):
        if target == slug or os.path.abspath(target) == os.path.abspath(path) or target in slug:
            hit = (i, slug, path); break
    if hit is None:
        if os.path.exists(target):
            hit = (-1, os.path.basename(target), target)
        else:
            print("KHONG TIM THAY script: %s" % target); return 2
    i, slug, path = hit
    mine, decl = read_axes(path)
    print("== GATE XOAY KHUON (MUC 11B) — %s ==" % slug)
    errs, warns = [], []
    if not decl:
        errs.append("THIEU dong khai bao. Them vao header:\n"
                    "     - **Truc 5T:** T1=… · T2=… · T3=… · T4=… · T5=…")
        print("  truc (suy doan): " + "  ".join("%s=%s" % (a, mine.get(a, "?")) for a in AXES))
    else:
        print("  truc: " + "  ".join("%s=%s" % (a, mine[a]) for a in AXES))

    prev = [(s, p) for _, s, p in (allx[i + 1:i + 1 + WINDOW] if i >= 0 else allx[:WINDOW])]
    if not prev:
        print("  (chua co bai truoc de so — bo qua)"); return 0
    pax = [(s, read_axes(p)[0]) for s, p in prev]
    print("  so voi %d bai truoc: %s" % (len(pax), ", ".join(s[:22] for s, _ in pax)))

    new_axes = []
    for a in AXES:
        v = mine.get(a, "?").lstrip("~")
        used = [d.get(a, "?").lstrip("~") for _, d in pax]
        if v == "?":
            warns.append("%s chua xac dinh duoc gia tri" % a); continue
        if v not in used:
            new_axes.append(a)
        # luat 2: streak
        streak = 1
        for u in used:
            if u == v: streak += 1
            else: break
        if streak > MAX_STREAK:
            errs.append("%s (%s) = '%s' lap %d bai LIEN TIEP (tran %d)" % (a, AXIS_NAME[a], v, streak, MAX_STREAK))
        # luat 3: overloaded
        if v in OVERLOADED and used.count(v) >= 1:
            errs.append("%s = '%s' la gia tri ⛔ QUA TAI va da co %d lan trong %d bai gan nhat (tran 1)"
                        % (a, v, used.count(v), len(used)))
    print("  truc MOI: %d/%d  %s" % (len(new_axes), len(AXES), ",".join(new_axes) if new_axes else "(khong co)"))
    if len(new_axes) < NEED_NEW:
        errs.append("chi doi %d truc — luat doi >=%d/5 truc khac han %d bai gan nhat" % (len(new_axes), NEED_NEW, len(pax)))

    for w in warns: print("  [!] " + w)
    if errs:
        print("\n🔴 CHAN — %d loi:" % len(errs))
        for e in errs: print("   - " + e)
        print("\n   Chay `--table` de xem gia tri nao con trong. Doi LOAI truyen, dung doi ten nhan vat.")
        return 1
    print("\n✅ PASS — khuon du khac 5 bai gan nhat.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("-n", type=int, default=8)
    a = ap.parse_args()
    if a.table or not a.target:
        table(a.n); sys.exit(0)
    sys.exit(gate(a.target))
