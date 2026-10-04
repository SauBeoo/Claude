# -*- coding: utf-8 -*-
r"""gen_flow21.py — prompt TEXT->VIDEO (8s) + so tay dung clip cho video 21.

⭐ STYLE: **AI NGUOI THAT (photoreal)** — khong con co `--style anime`.
   User chot 2026-09-04: *"tao muon dang AI nguoi that. Tu nay deu dung AI nguoi
   that het nhe"*. Nhanh anime cua `gen_flow20.py` KHONG duoc port sang day; muon
   xem lai thi doc file cua video 20.

XUAT ra `06_VIDEO/<STEM>/`:
  · `flow21_T2V.txt`      MOT prompt / MOT shot, moi prompt MOT DONG (bom vao
                          extension) — user chot 2026-09-03: *"gop thanh 1 file
                          prompt thoi, text chuyen thanh video"*
  · `flow21_TENFILE.txt`  dong -> ten clip -> giay -> scene -> loi doc
  · `flow21_BLOCKS.md`    ban NGUOI DOC: bang cast/prop + tung scene + prompt
  · `flow21_GENTEN.md`    4 khoi 原典 phai TU CHUP MAN HINH (khong gen AI)

THU TU TRONG PROMPT (bam theo `gen_flow20.py`, da chung minh chay duoc):
  CANH (co nguoi o the bat dau) -> VIEC nguoi do lam -> may quay -> chat anh ->
  khoa nhan vat/vat -> bo cuc -> nhip.  Canh va viec dung DAU vi model bam khoi
  dau; style/khoa la phan phu.

🔴 HAI LOP CHONG BO LOC AN TOAN GOOGLE — dung nguyen `_policy20.py`, dung viet lai:
  ① khong bao gio "xin phep" bang cach NHAC den dieu cam ("not a real person"
     => bo loc thay `real person`, khong thay `not`);
  ② mat do 「MUST」「NEVER」 cung la tin hieu => prompt ta canh thuan tuy, ~1.100–1.600 ky.

CHAY:  python tools/gen_flow21.py
"""
import collections
import io
import json
import math
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes21 import CAST, HANDS, PROP, SCENES, DOC_FOCUS   # noqa: E402
from _policy20 import GOOGLE_BLOCK, GOOGLE_SWAP              # noqa: E402
# POLICY_SWAP song trong `_scenes20_real` (module du lieu, khong chay gi khi
# import). Day la BANG CHINH SACH chung cho ca kenh, khong phai noi dung video 20
# — nen dung lai chu khong nhan ban.
from _scenes20_real import POLICY_SWAP                       # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
TL = os.path.join(VD, "timeline.json")

# regex tu lap ("dark-wood dark-wood shelf") — doi chu CHONG NHAU thi de lai
# tu lap, mat khong thay khi luot 84 prompt nen phai do bang may.
DUP_RE = re.compile(r"\b([a-z][\w-]{2,})\s+\1\b", re.I)
assert DUP_RE.search("the dark-wood dark-wood shelf"), "DUP_RE hong"

# ══════════════════════════════════════════════════════════════════════════
# KHOI STYLE — ban `real` cua gen_flow20, giu nguyen tung chu (da qua bo loc)
# ══════════════════════════════════════════════════════════════════════════
# 🔴 BO `cine camera` / `50mm lens` / `f/2.8` (2026-09-05). Model dien giai
#    thuat ngu may anh thanh **hien thong so len khung hinh**: clip 031 co HUD
#    cam `F/28 → F/26 → F/20` goc duoi-trai, clip 079 co `F/28 / F/25` goc
#    TREN-trai, va clip 050 in `2 /2.8` len the giay tren quay. Ta cung mot chat
#    anh bang ngon ngu thuong thi khong co ky hieu nao de model ve ra.
T2V_STYLE = (
    "Photorealistic live-action documentary footage, natural window light, "
    "muted warm colour grade, gentle film grain, the subject in sharp focus "
    "against a softly blurred background. "
    "Contemporary Japan, an ordinary middle-class setting that looks genuinely "
    "lived in — worn edges, honest textures, a little everyday clutter. Calm, "
    "respectful and unposed, like a quiet documentary."
)
T2V_JP = (
    "Everyone shown is Japanese, of the age described, in modest everyday "
    "Japanese clothing. Older faces carry their real age — lines, real skin "
    "texture, thinning or white hair."
)
T2V_FRAME = (
    "Composition: one clear subject, large in frame. Keep the top fifth of the "
    "frame simple and open — plain wall, window or sky — and the bottom fifth "
    "clear of faces. Any printing on paper is small and softly out of focus so "
    "the wording stays indistinct; keep lettering out of the picture "
    "otherwise. Horizontal 16:9, eight seconds."
)
T2V_DOC = (
    "The sheet is the subject of this shot, so give it fine printed rule lines, "
    "column dividers and boxes, with one row of crisp numerals; put a red pen "
    "circle or a pencil tick exactly where the hand points, so the gesture "
    "lands on something. The pen mark and the numerals stay crisp throughout."
)
T2V_TAIL = (
    "People move at the unhurried pace of real life, the way they actually "
    "handle paper, cups and small objects at home — nothing rushed, nothing "
    "theatrical — and the action reaches its natural end within the eight "
    "seconds and rests there. Faces and clothes stay consistent throughout; "
    "hands and objects have real weight. Nobody talks. The shot begins and "
    "ends on a steady frame. Silent."
)
CAM = {
    "static":   "The camera sits still on a tripod for the whole shot.",
    "parallax": ("The camera is handheld but held very still, so the frame "
                 "breathes only slightly."),
    "push":     ("The camera creeps in a little on a dolly over the eight "
                 "seconds and comes to rest."),
    "push_hard": ("The camera moves in a clear, steady dolly push toward the "
                  "subject and stops as the action lands."),
    "pull_out": ("The camera draws slowly back on a dolly, gradually taking in "
                 "more of the room, and comes to rest."),
}


def policy_clean(text, tally):
    """Lop cuoi: doi CHU, giu NGHIA. Tra ve text da sach + ghi so lan doi."""
    for pat, sub in list(POLICY_SWAP) + list(GOOGLE_SWAP):
        new, k = re.subn(pat, sub, text)
        if k:
            tally[pat] += k
            text = new
    return re.sub(r"\s{2,}", " ", text)


def locks(shot, first_of):
    """CAST LOCK + PROP LOCK cho mot shot."""
    bits = []
    cid, hid = shot.get("cast"), shot.get("hands")
    if cid:
        if first_of.get(cid) == shot["key"]:
            bits.append(f"CHARACTER {cid} — this shot establishes the character, "
                        f"so keep the description below unchanged in every later "
                        f"shot: {CAST[cid]['lock']}")
        else:
            bits.append(f"CHARACTER {cid} — the same character as before; keep "
                        f"the same age, hair, build and clothing so the series "
                        f"stays consistent: {CAST[cid]['lock']}")
    if hid:
        bits.append(f"The hands belong to {hid}: {HANDS[hid]}")
    props = shot.get("props", [])
    if props:
        parts = [PROP[props[0]]] + [re.sub(r"^the SAME [^:]+: ", "", PROP[q])
                                    for q in props[1:]]
        bits.append("PROP LOCK — " + ", and ".join(parts))
    return " ".join(b if b.endswith(".") else b + "." for b in bits)


def main():
    lines = json.load(io.open(TL, encoding="utf-8"))["lines"]
    dur = lines[-1]["end"]
    os.makedirs(VD, exist_ok=True)
    tally = collections.Counter()

    # shot dau tien cua moi nhan vat = MASTER REFERENCE
    first_of, seen = {}, set()
    for s in SCENES:
        for sh in s.get("shots", []):
            c = sh.get("cast")
            if c and c not in seen:
                seen.add(c)
                first_of[c] = sh["key"]

    n_art = sum(len(s["shots"]) for s in SCENES if s["kind"] == "art")
    n_gen = sum(s["genten"]["shots"] for s in SCENES if s["kind"] == "genten")

    t2v, ten_rows, blocks, gen_blocks = [], [], [], []
    blocks.append(
        f"# flow21 — video 21 扶養親族等申告書・二百五万円 · STYLE: NGUOI THAT (photoreal)\n\n"
        f"- kich ban: `03_SCRIPTS/{STEM}_TTS.md` · **{len(lines)} dong · "
        f"{dur:.1f}s ({dur/60:.2f} phut)**\n"
        f"- **{len(SCENES)} scene** ({len(SCENES)/(dur/60):.2f} scene/phut) · "
        f"**{n_art} clip AI 8s** + **{n_gen} screenshot 原典**\n"
        f"- Thu tu duoi day = **thu tu THOI GIAN trong video**. Gen theo dung thu "
        f"tu nay thi lien mach doc ra duoc.\n"
        f"- ⚠️ Canh AI **realistic** => **PHAI TICK 'altered/synthetic content'** "
        f"luc upload (`youtube-compliance.md` §2.1).\n"
        f"- {len(DOC_FOCUS)} shot **DOC_FOCUS**: giay to phai co CHU SO doc duoc "
        f"+ dau danh dau o dung cho tay chi vao.\n")
    blocks.append("\n## CAST LOCK — gen shot MASTER truoc, roi dung lam anh tham chieu\n")
    blocks.append("| id | vai | shot MASTER |\n|---|---|---|")
    for cid, c in CAST.items():
        blocks.append(f"| **{cid}** | {c['who']} | `{first_of.get(cid, '—')}` |")
    blocks.append("\n## PROP LOCK\n")
    blocks.append("| id | phai giong nhau o moi shot |\n|---|---|")
    for pid, t in PROP.items():
        blocks.append(f"| **{pid}** | {t[:140]}… |")
    blocks.append("")

    n = 0
    for si, s in enumerate(SCENES):
        a = lines[s["L"]]["start"]
        b = lines[SCENES[si + 1]["L"]]["start"] if si + 1 < len(SCENES) else dur
        span = b - a
        L0 = s["L"]
        L1 = SCENES[si + 1]["L"] if si + 1 < len(SCENES) else len(lines)
        jp = "  \n".join(f"`L{i}` {lines[i]['text']}" for i in range(L0, L1))
        # 🔴 mm:ss phai dung // — `{a/60:.0f}` LAM TRON: 119,2s ra "2:59.2"
        blocks.append(
            f"\n---\n\n## SCENE {si:02d} · {int(a)//60}:{a % 60:04.1f}–"
            f"{int(b)//60}:{b % 60:04.1f} ({span:.1f}s) · {s['tag']} · "
            f"`{s['kind']}`\n\n**LOI DOC:**  \n{jp}\n")

        if s["kind"] == "stat":
            blocks.append("\n**BANG SO** (khong co anh hero — vung giua cho duoc "
                          "mot thu):\n")
            for lab, val in s["stat"]:
                blocks.append(f"- `{lab.lstrip('*')}` → **{val}**"
                              f"{' ⭐NHAN' if lab.startswith('*') else ''}")
            blocks.append("")
            continue
        if s["kind"] == "formula":
            blocks.append(f"\n**CONG THUC** (khong co anh hero): **`{s['formula']}`**"
                          f"{'  ⭐PEAK' if s.get('peak') else ''}\n")
            continue
        if s["kind"] == "genten":
            g = s["genten"]
            # 🔴 In CA HAI: `quote` = chu THAT tren trang (thu phai khoanh do), va
            #    `said` = cau loi doc doc ra. Chung LECH NHAU o ca 4 khoi cua bai
            #    nay (do fetch 2026-09-04) — in canh nhau de khong ai khoanh do
            #    theo cau loi doc, va de thay ngay khi lech qua xa.
            said = g.get("said")
            txt = (f"\n**原典 — SCREENSHOT THAT, ⛔ KHONG GEN AI** ({g['shots']} shot):\n"
                   f"- URL: {g['url'] or '🔴 **CHUA VERIFY — phai tu tra roi dien vao '
                                         '`_scenes21.py`**'}"
                   f"{'  · verify ' + g['verified'] if g.get('verified') else ''}\n"
                   f"- **chu THAT tren trang** (khoanh do dung cai nay): 「{g['quote']}」\n"
                   + (f"- **chu THAT (2)**: 「{g['quote2']}」\n" if g.get("quote2") else "")
                   + (f"- **chu THAT (3)**: 「{g['quote3']}」\n" if g.get("quote3") else "")
                   + (f"- ⚠️ **loi doc lai noi**: 「{said}」 → lech voi chu tren trang; "
                      f"xem canh bao cuoi ban in\n" if said else "")
                   + f"- danh dau: {g['mark']}\n"
                   f"- chup man hinh trang THAT, khoanh do dung cau tren, cat 16:9. "
                   f"Khoi nay **PHAI doc duoc** — no la bang chung, KHONG duoc gen AI "
                   f"va KHONG duoc lam mo chu.\n")
            blocks.append(txt)
            gen_blocks.append(f"\n## {s['tag']}  ·  scene {si:02d} · "
                              f"{int(a)//60}:{a % 60:04.1f} ({span:.1f}s)\n{txt}")
            continue

        k = len(s["shots"])
        for j, sh in enumerate(s["shots"]):
            n += 1
            t0, t1 = a + span * j / k, a + span * (j + 1) / k
            lk = locks(sh, first_of)
            doc = (" " + T2V_DOC) if sh["key"] in DOC_FOCUS else ""
            tp = (f"{sh['sc']}. {sh['mo']} {CAM[sh['cam']]} {T2V_STYLE} {lk} "
                  f"{T2V_JP} {T2V_FRAME}{doc} {T2V_TAIL}")
            tp = policy_clean(re.sub(r"\s+", " ", tp).strip(), tally)
            t2v.append(tp)
            fn = f"a21_{sh['key']}"
            master = (f" · ⭐KHUON {sh['cast']}"
                      if sh.get("cast") and first_of.get(sh["cast"]) == sh["key"]
                      else "")
            ten_rows.append(f"{n:03d}\t{fn}.mp4\t{t0:7.1f}-{t1:7.1f}s\t"
                            f"S{si:02d} {s['tag']}\t"
                            f"{lines[min(L0 + j, L1 - 1)]['text'][:38]}")
            blocks.append(f"\n### {n:03d} · `{fn}.mp4` · {t0:.1f}–{t1:.1f}s "
                          f"({t1-t0:.1f}s) · cam `{sh['cam']}`{master}"
                          f"\n\n**PROMPT (text → video, 8s):**\n```\n{tp}\n```\n")

    def w(name, text):
        io.open(os.path.join(VD, name), "w", encoding="utf-8",
                newline="\n").write(text)

    w("flow21_T2V.txt", "\n".join(t2v) + "\n")
    w("flow21_TENFILE.txt",
      "dong\tclip\tgiay\tscene\tloi doc\n" + "\n".join(ten_rows) + "\n")
    w("flow21_BLOCKS.md", "\n".join(blocks) + "\n")
    w("flow21_GENTEN.md",
      "# 原典 — 4 khoi phai TU CHUP MAN HINH (⛔ khong gen AI)\n"
      "\n> Bang chung cua bai. Chu phai DOC DUOC; cam lam mo, cam ve lai.\n"
      + "\n".join(gen_blocks) + "\n")

    # ══ GATE ═════════════════════════════════════════════════════════════
    # 🔴 Soi CHINH CHUOI DA XUAT. Bao cao cua mot lop KHONG chung minh lop do
    #    da chay (bai hoc 2026-09-03: 6 mau regex im lang vi loi escape).
    bad9, gshots, dup_word = [], set(), set()
    gblock = collections.Counter()
    for si, s in enumerate(SCENES):
        if s["kind"] != "art":
            continue
        a = lines[s["L"]]["start"]
        b = lines[SCENES[si + 1]["L"]]["start"] if si + 1 < len(SCENES) else dur
        per = (b - a) / len(s["shots"])
        if per > 9.05:
            bad9.append((si, s["tag"], round(per, 1), math.ceil((b - a) / 9)))
    for i, t in enumerate(t2v):
        for pat in GOOGLE_BLOCK:
            k = len(re.findall(pat, t, re.I))
            if k:
                gblock[pat] += k
                gshots.add(i + 1)
        for m in DUP_RE.finditer(t):
            dup_word.add((i + 1, m.group(0)))
    no_url = [s["tag"] for s in SCENES
              if s["kind"] == "genten" and not s["genten"]["url"]]
    keys = [sh["key"] for s in SCENES for sh in s.get("shots", [])]
    dupk = [k for k, v in collections.Counter(keys).items() if v > 1]
    lens = [len(x) for x in t2v]

    print(f"→ {VD}")
    print(f"   flow21_T2V.txt      {len(t2v):3d} prompt text→video "
          f"({min(lens)}–{max(lens)} ky)  ← MOT prompt / MOT shot")
    print(f"   flow21_TENFILE.txt  {len(ten_rows):3d} dong")
    print(f"   flow21_GENTEN.md    {n_gen} screenshot / "
          f"{sum(1 for s in SCENES if s['kind']=='genten')} khoi")
    print(f"   flow21_BLOCKS.md")
    print(f"   scene {len(SCENES)} ({len(SCENES)/(dur/60):.2f}/phut) · "
          f"clip {n_art} · screenshot {n_gen} · {dur/60:.2f} phut")
    if tally:
        print(f"   policy_clean: doi {sum(tally.values())} cum "
              f"({len(tally)} mau)")

    fail = False
    if bad9:
        fail = True
        print("\n🔴 GATE SAN 9s (audience-45plus §2.0b) — thieu shot:")
        for si, tag, per, need in bad9:
            print(f"   S{si:02d} {tag}: {per}s/anh → can {need} shot")
    if dupk:
        fail = True
        print(f"\n🔴 GATE KEY TRUNG (2 shot cung ten file): {dupk}")
    if gblock:
        fail = True
        print(f"\n🔴 GATE TU KHOA GOOGLE — {len(gshots)} prompt con tu bi chan:")
        for pat, k in gblock.most_common():
            print(f"   {k:3d}×  {pat}")
    if dup_word:
        fail = True
        print(f"\n🔴 GATE TU LAP ({len(dup_word)} cho, do doi chu chong nhau):")
        for i, w_ in sorted(dup_word)[:12]:
            print(f"   prompt {i}: “{w_}”")
    # 🔴 NGUONG DO DUOC, KHONG PHONG DOAN. Ban dau tao dat 1.900 theo cau
    #    "~1.100–1.600 ky" trong docstring cua `gen_flow20.py` — va no bao dong
    #    GIA ngay lan chay dau. Do lai `flow20_T2V.txt` (83 clip user DA gen
    #    thanh cong, video 20 render xong): **1.742–2.954 ky, trung binh 2.225**.
    #    Tuc 1.600 la Y DINH cua ban rut gon, khong phai thuc te da xuat.
    #    => tran = 3.000, sat tren mau da chay duoc.
    if max(lens) > 3000:
        print(f"\n⚠️  prompt dai nhat {max(lens)} ky — vuot mau da chay duoc cua "
              f"video 20 (max 2.954 ky). `_policy20.py` §②: prompt dai thi model "
              f"bam ta canh roi nuot phan con lai")
    if no_url:
        fail = True
        print(f"\n🔴 GATE 原典 — {len(no_url)} khoi CHUA co URL, phai verify "
              f"truoc khi chup (YMYL: cam bia nguon):")
        for t in no_url:
            print(f"   · {t}")
    # ⚠️ CANH BAO (khong chan): loi doc noi 「こう書かれています」 ma cau doc ra
    #    KHONG trung nguyen van trang nguon. Noi dung dung, chu thi lech — nguoi
    #    xem NGHE mot cau va THAY mot cau khac tren anh khoanh do.
    lech = [(s["tag"], s["genten"]) for s in SCENES
            if s["kind"] == "genten" and s["genten"].get("said")]
    if lech:
        print(f"\n⚠️  {len(lech)}/{sum(1 for s in SCENES if s['kind']=='genten')} "
              f"khoi 原典: loi doc KHONG trung nguyen van trang nguon")
        for tag, g in lech:
            print(f"   {tag}")
            print(f"      trang noi : 「{g['quote']}」")
            print(f"      loi doc noi: 「{g['said']}」")
        print("   → phai chon: sua loi cho khop nguyen van (re: cache TTS chi "
              "synth lai dong doi) HOAC doi cach dan tu 「こう書かれています」 sang "
              "「要点はこうです」")
    if not fail:
        print("\n✅ GATE SACH")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
