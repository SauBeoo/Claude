# -*- coding: utf-8 -*-
"""
story_extract.py — boc mot file export cua Flow Scenes/Story ra dia.

    python tools/story_extract.py "<...>/Untitled Story - ....json" <outdir>

Xuat ra <outdir>/:
    img/   sb_NN_sSSshHH.jpg      anh frame tung shot  (dung lam FIRST FRAME cho i2v)
    ref/   <type>_<ten>.jpg       anh tham chieu cua asset (character/location/prop)
    jobs.jsonl                    1 job / 1 dong  -> nap thang vao Flow Video Batch v2
    _MANIFEST.json                du lieu tho tung shot
    _REVIEW.md                    ⚠ bao cao: Flow tu them gi, cho nao phai duyet tay

🔴 VI SAO CO KHAU SANITIZE (do tren ban demo 2026-09-09, xem
   flow_batch_ext/DESIGN_i2v_2026-09-09.md §0.6 B): Flow TU SOAN visual/motionDescription va
   tu them 2 thu bi cam:
     ③ chuyen dong may  ("a slow zoom-in", "the camera tilts down") du kich ban ghi camera co dinh
        -> mau thuan truc tiep voi duoi prompt i2v ("the camera stays locked off, no zoom, no pan")
     ④ framing CHI CO TAY ("a tight shot on Kazuko's weathered hand")
        -> dung thu 04_VIDEOGEN_PROMPTS.md cam dich danh (showa: 14/21 clip hands-only bi hong)
   Tool BO ③ va DOI ④, roi ghi lai TUNG chi tiet vao _REVIEW.md. Khong sua im lang.
"""
import base64
import io
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── duoi prompt i2v: giu nguyen anh, chi cho dung mot thu chuyen dong ───────────
TAIL = (
    "Keep the framing, composition, characters, clothing, props and colours of the given image "
    "exactly as they are; the camera stays locked off and does not move, no zoom, no pan, no cut "
    "to another shot. Only what is described above moves, once, slowly, and it holds still for the "
    "rest of the shot. Any printing on paper or screens stays exactly as in the image; no new text "
    "appears, no captions, no watermark, no logo."
)
HOLD = "the subject holds the pose and only breathes and blinks"

CAM_WORD = r"(?:zoom|pan(?:s|ning)?|tilt(?:s|ing)?|push(?:es|ing)?\s+in|pull(?:s|ing)?\s+(?:back|out)|dolly|dollies|track(?:s|ing)?\s+(?:in|out|left|right)|crane|orbit|rack\s+focus)"
HANDS_ONLY = re.compile(
    r"(?:an?\s+)?(?:extreme\s+|tight\s+|very\s+)?(?:close[-\s]?up|insert|macro)\s+shot\s+"
    r"(?:that\s+)?(?:on|of|focus(?:es|ing)?\s+on)\s+[^.]*?\bhands?\b[^.]*?(?:\.|$)",
    re.I,
)
HANDS_FIX = ("filmed over the shoulder with the torso and both hands inside the frame, "
             "not a close-up of the hands alone")


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", (text or "").strip()) if s.strip()]


# 🔴 Flow hay GOI chuyen dong that CUA CHU THE ben trong mot cau noi ve MAY:
#    "The camera remains fixed in the entryway, watching her back as she disappears into the house."
#    Bo ca cau thi mat luon viec Kazuko dang di -> phai cuu menh de sau to follow/as/while/watching.
RESCUE = re.compile(r"\b(?:to follow(?:\s+the\s+movement\s+of)?|watching|showing|as|while)\s+(.+?)(?:\.|$)", re.I)
# dong tac CUA NGUOI — dung de suy chuyen dong tu visualDescription khi motion khong con gi
ACTION = re.compile(r"\b(draws?|picks?\s+up|reach(?:es|ing)|walks?|lifts?|holds?|places?|sets?|"
                    r"turns?|stands?|sits?|looks?|moves?|opens?|closes?|steps?|writes?|points?)\b", re.I)


def _clean_clause(c):
    c = re.sub(r"^(?:the\s+)?camera\s+", "", c.strip(), flags=re.I).strip(" ,.")
    return "" if re.search(CAM_WORD, c, re.I) else c


def sanitize(motion, visual):
    """Tra ve (dau_prompt, [ghi_chu]). Dau prompt = CHUYEN DONG CUA CHU THE, khong cua may."""
    notes, keep = [], []
    for s in sentences(motion):
        if re.search(CAM_WORD, s, re.I) or re.search(r"\bthe camera\b", s, re.I):
            notes.append(("③ camera move bi BO", s))
            m = RESCUE.search(s)
            cl = _clean_clause(m.group(1)) if m else ""
            if cl and ACTION.search(cl):
                keep.append(cl)
                notes.append(("   ↳ cuu lai chuyen dong chu the", cl))
        else:
            keep.append(s.rstrip("."))

    head = ", then ".join(keep) if keep else ""

    # ⑤ khong con gi -> SUY tu visualDescription (cau dau tien co dong tac cua nguoi),
    #    thay vi roi thang ve HOLD lam mat hanh dong that cua shot.
    if not head:
        for s in sentences(visual):
            s2 = re.sub(HANDS_ONLY, "", s).strip(" ,.")
            s2 = re.sub(r"^(?:an?|the)\s+(?:\w+\s+){0,3}shot\s+(?:of|on)\s+", "", s2, flags=re.I)
            if ACTION.search(s2) and not re.search(CAM_WORD, s2, re.I):
                head = s2.rstrip(".")
                notes.append(("   ↳ suy chuyen dong tu visualDescription", head[:90]))
                break

    if HANDS_ONLY.search(visual or "") or HANDS_ONLY.search(motion or ""):
        src = HANDS_ONLY.search(visual or "") or HANDS_ONLY.search(motion or "")
        notes.append(("④ framing HANDS-ONLY bi DOI", src.group(0).strip()))
        head = (head + ", " if head else "") + HANDS_FIX

    if not head:
        head = HOLD
        notes.append(("⚠ khong con chuyen dong nao -> dung khuon HOLD", "(kiem tay)"))
    return head, notes


# ── ghép tên asset của Flow ↔ shot ──────────────────────────────────────────────
# Flow tự đặt CAPTION cho từng asset ("Woman walking down hallway"), không theo tên file
# mình. Tool Flow Batch v2 tìm asset bằng chính caption đó ⇒ phải ghép caption ↔ shot.
# Ghép bằng CHỒNG TỪ với visualDescription + title (bỏ stopword), báo điểm để soi tay.
STOP = set("a an the of on in at to and or with his her their its into from for is are was "
           "were be been as by that this it he she they shot camera view image video frame "
           "close up wide medium static slow gentle".split())


def stem(w):
    """Cat duoi tho. 'walks'/'walking' -> 'walk'; 'envelopes' -> 'envelope'.
    🔴 Khong co buoc nay thi 'walks' (trong visual) khong khop 'walking' (trong caption)
       va shot di-bo bi gan cho shot dung-yen — da dinh that."""
    for suf, keep in (("ing", 5), ("ed", 4), ("es", 4), ("s", 4)):
        if w.endswith(suf) and len(w) >= keep and not w.endswith("ss"):
            return w[: -len(suf)]
    return w


def toks(s):
    return {stem(w) for w in re.findall(r"[a-z]+", (s or "").lower())
            if len(w) > 2 and w not in STOP}


def match_assets(man, captions, floor=0.34):
    """Gan caption cho tung shot, **1-DOI-1**. Tra ve list (idx, caption, diem, canh_bao).

    🔴 Ban dau cham diem theo tung shot roi lay max ⇒ mot caption bi gan cho 4 shot
       ("Woman picking up white envelope" trung 4 lan). Hai loi:
         ① chuan hoa sai: chia cho len(caption)**0.5 lam caption dai duoc uu the ao;
         ② khong co rang buoc 1-doi-1.
       ⇒ Nay: diem = |giao| / |token caption| (ti le token caption XUAT HIEN trong shot),
       roi **gan tham lam theo diem giam dan**, moi shot & moi caption dung DUNG 1 lan.
       Caption thieu (shot khong con ung vien nao dat san) tra ve None — de trong con
       tot hon dinh sai anh.
    """
    base = {m["idx"]: toks(m.get("visual")) | toks(m.get("title")) | toks(m.get("motion"))
            for m in man}
    cap_t = {c: toks(c) for c in captions if toks(c)}

    # 🔴 CAN THEO IDF, khong dem tho: 'woman' co trong 3 caption nen no gan het moi shot
    #    co nguoi ⇒ hai cap cung ra 0.50 va tham lam boc bua. Token HIEM ('hallway',
    #    'arrow') moi la thu dinh danh duoc shot.
    import math
    df = {}
    for t in cap_t.values():
        for w in t:
            df[w] = df.get(w, 0) + 1
    N = max(1, len(cap_t))
    idf = lambda w: math.log(1 + N / (1 + df.get(w, 0)))

    pairs = []
    for idx, b in base.items():
        for c, t in cap_t.items():
            tot = sum(idf(w) for w in t) or 1e-9
            pairs.append((sum(idf(w) for w in (b & t)) / tot, idx, c))
    pairs.sort(reverse=True)

    best = {}                      # idx -> (caption, diem)
    runner = {}                    # idx -> diem cua ung vien ke tiep (do "sat nut")
    taken_i, taken_c = set(), set()
    for sc, idx, c in pairs:
        if sc < floor:
            break
        if idx in taken_i or c in taken_c:
            if idx not in runner and idx in taken_i and best.get(idx, ("", 0))[1] != sc:
                runner[idx] = sc
            continue
        best[idx] = (c, sc); taken_i.add(idx); taken_c.add(c)

    out = []
    for m in man:
        idx = m["idx"]
        cap, sc = best.get(idx, (None, 0.0))
        warn = []
        if not cap:
            warn.append("KHONG ghep duoc — dien tay field \"asset\"")
        else:
            if sc < 0.5:
                warn.append("diem THAP")
            if runner.get(idx) and sc - runner[idx] < 0.12:
                warn.append("sat nut voi ung vien khac")
        out.append((idx, cap, round(sc, 2), warn))
    return out


def write_b64(dst: Path, b64: str):
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(base64.b64decode(b64))
    return dst.stat().st_size


def safe(name: str) -> str:
    return re.sub(r"[^0-9A-Za-z぀-ヿ一-鿿_-]+", "_", name or "x")[:40]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])

    # ── co, doc TRUOC cac tham so vi tri con lai ──────────────────────────────
    argv = sys.argv[3:]
    def flag(name, default=None):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else ""
            del argv[i:i + 2]
            return v
        return default
    dl = flag("--dl")                 # thu muc anh TAI TU FLOW -> ghep caption bang MD5
    only = flag("--scenes")           # vi du: 01,02,03  (chi xuat may scene nay)
    only = set(x.strip() for x in only.split(",")) if only else None

    # tuy chon: file caption cua Flow (output nut 📋 LIET KE ASSET), 1 ten/1 dong
    caps = []
    if argv:
        caps = [re.sub(r"^\s*\d+\s+", "", l).strip()
                for l in io.open(argv[0], encoding="utf-8") if l.strip()]
        caps = [c for c in caps if c and not c.startswith(("#", "📋", "Copy"))]

    # ⭐ GHEP BANG MD5 — chinh xac 100%, thay han cho phep doan stem+IDF.
    #    Anh tai tu Flow co ten file = CAPTION cua Flow + dau thoi gian, va byte anh
    #    y NGUYEN anh trong export ⇒ md5(anh trong json) == md5(file tai ve).
    #    Do that tren 66 frame: khop 66/66. Doan tu thi 5/7 — dung md5 thi khoi doan.
    dlmap = {}
    if dl:
        import hashlib
        for fn in os.listdir(dl):
            if not re.search(r"\.(jpe?g|png|webp)$", fn, re.I):
                continue
            with open(os.path.join(dl, fn), "rb") as fh:
                dlmap[hashlib.md5(fh.read()).hexdigest()] = \
                    re.sub(r"[ _]\d{8,14}(?:[ _]\d{1,3})?\.(?:jpe?g|png|webp)$", "", fn, flags=re.I).replace("_", " ").strip()
        print(f"   anh tai ve: {len(dlmap)} file trong {dl}")
    d = json.load(io.open(src, encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)

    frames = d.get("frames") or []
    assets = {a["id"]: a for a in (d.get("assets") or [])}
    # prompt Flow tu soan cho tung shot (neu da co) — de doi chieu, KHONG dung lam mac dinh
    flow_prompt = {}
    for r in (d.get("generatedResults") or []):
        for s in (r.get("segments") or []):
            if (s.get("prompt") or "").strip():
                flow_prompt[s.get("shotId")] = {"prompt": s["prompt"], "duration": s.get("duration")}

    print(f"== {d.get('projectTitle')} | style={d.get('globalStyle')} ==")
    print(f"   frames={len(frames)}  assets={len(assets)}  segment-co-prompt={len(flow_prompt)}")

    # --scenes: chi giu may scene duoc chi dinh (giu NGUYEN so thu tu goc de doi chieu)
    if only:
        keep = [f for f in frames if (f.get("sceneNumber") or "") in only]
        print(f"   --scenes {','.join(sorted(only))}: {len(keep)}/{len(frames)} shot")
        if not keep:
            print("   🔴 khong shot nao khop --scenes; scene co san: "
                  + ",".join(sorted({f.get('sceneNumber') or '?' for f in frames})))
            sys.exit(2)
        frames = keep

    # ① anh tham chieu cua asset
    nref = 0
    for a in assets.values():
        for i, si in enumerate(a.get("supportingImages") or []):
            if si.get("base64"):
                write_b64(out / "ref" / f"{a['type']}_{safe(a['name'])}{'' if i == 0 else f'_{i}'}.jpg",
                          si["base64"])
                nref += 1

    # ② anh frame + jobs
    man, jobs, review = [], [], []
    for i, f in enumerate(frames, 1):
        sid = f"s{f.get('sceneNumber') or '00'}sh{f.get('shotNumber') or '00'}"
        stem = f"sb_{i:02d}_{sid}"
        img = out / "img" / f"{stem}.jpg"
        kb = write_b64(img, f["base64"]) // 1024 if (f.get("base64") or "").strip() else 0

        head, notes = sanitize(f.get("motionDescription"), f.get("visualDescription"))
        prompt = f"{head}. {TAIL}"
        fp = flow_prompt.get(f.get("id"))

        man.append({"idx": i, "id": f.get("id"), "file": img.name, "scene": f.get("sceneNumber"),
                    "shot": f.get("shotNumber"), "sceneTitle": f.get("sceneTitle"),
                    "title": f.get("title"), "visual": f.get("visualDescription"),
                    "motion": f.get("motionDescription"),
                    "assets": [assets[x]["name"] for x in (f.get("linkedAssetIds") or []) if x in assets],
                    "kb": kb, "flowPrompt": (fp or {}).get("prompt")})
        job = {"id": stem, "mode": "frames", "first": str(img.resolve()).replace("\\", "/"),
               "prompt": prompt, "duration": (fp or {}).get("duration") or 8}
        # ⭐ --dl: ghep TEN ASSET FLOW bang MD5 (chinh xac 100%, khong doan chu)
        if dlmap:
            import hashlib as _h
            cap = dlmap.get(_h.md5(base64.b64decode(f["base64"])).hexdigest())
            if cap:
                job["asset"] = cap
                man[-1]["asset"] = cap
            else:
                man[-1]["asset"] = None
        jobs.append(job)
        if notes:
            review.append((stem, f.get("title"), notes))

    # ── ghép caption của Flow vào job (field "asset") ─────────────────────────
    amatch = []
    if dlmap:
        got = sum(1 for j in jobs if j.get("asset"))
        print(f"   ghép asset bằng MD5: {got}/{len(jobs)} shot"
              + ("" if got == len(jobs) else "   🔴 thiếu — thư mục --dl không đủ ảnh?"))
        # 🔴 TRUNG TEN: Flow co the dat CUNG mot caption cho 2 asset khac nhau.
        #    Tool Flow Batch doi khop DUY NHAT nen job do se DUNG — bao truoc o day
        #    thay vi de no chet giua lo.
        import collections as _c
        dup = {k: v for k, v in _c.Counter(j.get("asset") for j in jobs if j.get("asset")).items() if v > 1}
        if dup:
            print(f"   ⚠ {len(dup)} tên asset TRÙNG NHAU trong lô này — job đó phải chọn tay:")
            for k, v in dup.items():
                print(f"      {v}x  {k}")
    elif caps:
        amatch = match_assets(man, caps)
        # ⭐ MAP SỬA TAY THẮNG MÁY. Máy chỉ GỢI Ý (đo thật: 5/7 đúng, 2 cái sai đều có ⚠).
        #    Sửa `_ASSETMAP.tsv` một lần là chốt vĩnh viễn — chạy lại không mất.
        mp = out / "_ASSETMAP.tsv"
        manual = {}
        if mp.exists():
            for ln in io.open(mp, encoding="utf-8"):
                p = ln.rstrip("\n").split("\t")
                if len(p) >= 2 and p[0] and not p[0].startswith("#") and p[1].strip():
                    manual[p[0].strip()] = p[1].strip()
        nman = 0
        fixed = []
        for k, (idx, cap, sc, warn) in enumerate(amatch):
            f = man[idx - 1]["file"]
            if f in manual and manual[f] != cap:
                cap, sc, warn = manual[f], 1.0, ["SUA TAY"]
                nman += 1
            fixed.append((idx, cap, sc, warn))
        amatch = fixed
        for j, (idx, cap, sc, warn) in zip(jobs, amatch):
            if cap:
                j["asset"] = cap          # tool Flow Batch tìm asset bằng tên này
        with io.open(mp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# shot\tcaption Flow\tdiem\tcanh bao   ← SUA COT 2 roi chay lai; "
                     "cot 2 co gia tri thi THANG may\n")
            for (idx, cap, sc, warn) in amatch:
                fh.write(f"{man[idx-1]['file']}\t{cap or ''}\t{sc}\t{' · '.join(warn)}\n")
        print(f"   ghép caption: {sum(1 for _,c,_,_ in amatch if c)}/{len(man)} shot · "
              f"sửa tay: {nman} · cần soi: {sum(1 for _,_,_,w in amatch if w and 'SUA TAY' not in w)}")
        print(f"   -> _ASSETMAP.tsv  (sửa cột 2 ở dòng có ⚠ rồi chạy lại lệnh này)")

    (out / "_MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    with io.open(out / "jobs.jsonl", "w", encoding="utf-8", newline="\n") as fh:
        for j in jobs:
            fh.write(json.dumps(j, ensure_ascii=False) + "\n")

    # ③ bao cao duyet tay
    L = [f"# _REVIEW — {d.get('projectTitle')}", "",
         f"- frames: **{len(frames)}** · asset-ref: **{nref}** · jobs: **{len(jobs)}**",
         f"- shot phai duyet tay: **{len(review)}/{len(frames)}**", "",
         "> Flow tu soan visual/motionDescription. Tool da BO chuyen dong may (③) va DOI framing",
         "> hands-only (④) theo `04_VIDEOGEN_PROMPTS.md`. Doc lai tung dong duoi day truoc khi gen.", ""]
    for stem, title, notes in review:
        L.append(f"### {stem} — {title}")
        for tag, txt in notes:
            L.append(f"- **{tag}**: `{txt}`")
        L.append("")
    if not review:
        L.append("✅ Khong co shot nao bi Flow tu them camera-move / hands-only.")
    if amatch:
        L += ["", "## Ghep caption Flow ↔ shot (field `asset` trong jobs.jsonl)", "",
              "| shot | caption Flow | diem | canh bao |", "|---|---|---|---|"]
        for (idx, cap, sc, warn) in amatch:
            L.append(f"| {man[idx-1]['file']} | {cap or '—'} | {sc} | "
                     f"{'⚠ ' + ' · '.join(warn) if warn else 'ok'} |")
        L += ["", "> 🔴 Dong nao co canh bao thi **soi tay**: dinh sai anh thi prompt van dung,",
              "> clip ra sai nguoi, **100 credits**, khong mot dau hieu loi nao."]
    (out / "_REVIEW.md").write_text("\n".join(L), encoding="utf-8")

    print(f"   -> {out/'img'}  ({len(jobs)} anh frame)")
    print(f"   -> {out/'ref'}  ({nref} anh tham chieu asset)")
    print(f"   -> jobs.jsonl · _MANIFEST.json · _REVIEW.md")
    print(f"   ⚠ shot phai duyet tay: {len(review)}/{len(frames)}  (doc _REVIEW.md)")


if __name__ == "__main__":
    main()
