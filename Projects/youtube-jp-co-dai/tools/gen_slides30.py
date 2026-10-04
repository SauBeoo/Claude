# -*- coding: utf-8 -*-
r"""Sinh SLIDES cho video 30 (FULL AI, 105 clip) + dat clip_XX.mp4 dung index.

Chep tu gen_slides29.py. video_render.py doi `clips/clip_{i:02d}.mp4` theo INDEX
cua entry SLIDES, KHONG theo ten mo ta.

🔴 BA BAY DA DINH THAT o video 29 (2026-09-04) — GIU NGUYEN cach chua:

 (1) SO CLIP != THU TU THOI GIAN. Neu lo 2 duoc viet de "lap cho lo 1 con thua"
     thi clip so lon co the thuoc doan dau bai. Sap theo so clip la lech (do duoc
     o video 29: 1.091 giay).
     => Tinh moc thoi gian cho TUNG clip roi SORT TOAN BO theo thoi gian.
 (2) Neo THUAN theo dong TTS -> nhip vo (72 entry <6s). Chia deu thoi gian THUAN
     -> clip lech >45s khoi doan no minh hoa.
     => ANCHOR lam moc cung, giua hai anchor noi suy theo THOI GIAN.
 (3) `used` set + ep tang dan se DON CUC neu thu tu vao sai -> sort TRUOC, gan dong SAU.

⚠️ KHAC video 29: bai 30 khong co cue thoai Nhat trong TENFILE (cot 3 la tieng Viet
   mo ta canh), nen KHONG co anchor tu cue. Thay bang ANCHOR THEO KHOI: moi khoi
   (A..N) neo vao dong TTS mo khoi do — xem BLOCK_ANCHOR.

    python tools\gen_slides30.py              # sinh SLIDES + gate
    python tools\gen_slides30.py --place      # + dat clip_XX.mp4
"""
import argparse
import json
import re
import shutil
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

P = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
VD = P / "06_VIDEO" / "30_futon-dani-uchinaoshi"
TTS = P / "03_SCRIPTS" / "30_futon-dani-uchinaoshi_TTS.md"
OUT = P / "03_SCRIPTS" / "30_futon-dani-uchinaoshi_SLIDES.json"

# clip dau cua tung khoi -> dong TTS mo khoi (substring, phai khop DUNG 1 dong)
BLOCK_ANCHOR = [
    (  1, "いま敷いている布団に"),
    (  7, "まず、相手の顔を"),
    ( 12, "よく晴れた夏の日に、4時間"),
    ( 20, "ダニが好むのは、温度20度から30度"),
    ( 24, "さて、取り込むときの"),
    ( 30, "ここで、掃除機の話をします"),
    ( 40, "かけ方には、目安があります"),
    ( 44, "家でできる形にすると"),
    ( 56, "防ダニシーツ、防ダニスプレー"),
    ( 61, "打ち直し、といいます"),
    ( 77, "昔の日本には、布団や着物を干す日に"),
    ( 84, "東京の、月ごとの平均湿度です"),
    ( 93, "やり方は、難しくありません"),
    ( 97, "私の母は、秋の終わりになると"),
    (101, "失われたのは、寒干しや打ち直し"),
]

MIN_GAP = 6.0   # audience-45plus.md §2 muc 2: khong entry nao <6 giay


def tts_lines():
    out = []
    for raw in TTS.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#") or s.startswith("<!--"):
            continue
        out.append(re.sub(r"\[[^\]]*\]", "", s).strip())
    return out


def load_map():
    m = []
    for f in ("video_prompts_TENFILE.txt",):
        p = VD / f
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            g = re.match(r"^\s*(\d+)\s*->\s*(\S+\.mp4)\s*\|\s*(.*)$", line)
            if g:
                m.append((int(g.group(1)), g.group(2), g.group(3).strip()))
    return sorted(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--place", action="store_true")
    a = ap.parse_args()

    lines = tts_lines()
    mp = load_map()
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
    T = float(tl["total"])
    starts = [float(x["start"]) for x in tl["lines"]]
    print(f"── {len(lines)} dong TTS · {len(starts)} dong timeline · "
          f"{len(mp)} clip · voice {T:.0f}s")
    if len(lines) != len(starts):
        print(f"🔴 len(TTS)={len(lines)} != len(timeline)={len(starts)} "
              f"— builder neo theo chi so dong se LECH. Dung lai.")
        return 1

    # 1) ANCHOR theo KHOI
    anc = {}
    for no, key in BLOCK_ANCHOR:
        hit = [i for i, L in enumerate(lines) if L.startswith(key)]
        if len(hit) != 1:
            print(f"🔴 anchor clip {no}: '{key}' khop {len(hit)} dong (phai 1)")
            return 1
        anc[no] = starts[hit[0]]
    print(f"   anchor khoi: {len(anc)}/{len(BLOCK_ANCHOR)} ✅")

    # 2) MOC THOI GIAN cho MOI clip — noi suy giua hai anchor lien tiep
    nos = [c[0] for c in mp]
    ks = sorted(anc)
    want = {}
    for n in nos:
        if n in anc:
            want[n] = anc[n]
            continue
        lo = max([k for k in ks if k < n], default=None)
        hi = min([k for k in ks if k > n], default=None)
        if lo is not None and hi is not None:
            want[n] = anc[lo] + (anc[hi] - anc[lo]) * (n - lo) / (hi - lo)
        elif lo is not None:
            want[n] = anc[lo] + (T - anc[lo]) * (n - lo) / max(nos[-1] - lo + 1, 1)
        else:
            want[n] = anc[hi] * n / max(hi, 1)

    # 3) SORT theo thoi gian TRUOC, gan dong SAU
    order = sorted(mp, key=lambda x: (want[x[0]], x[0]))
    used, slides, last_t = set(), [], -MIN_GAP
    for no, fn, cue in order:
        cand = [i for i in range(len(starts))
                if i not in used and starts[i] >= last_t + MIN_GAP]
        if not cand:
            cand = [i for i in range(len(starts)) if i not in used]
        c = min(cand, key=lambda i: (abs(starts[i] - want[no]), i))
        used.add(c)
        last_t = starts[c]
        slides.append({"match": lines[c], "video": True,
                       "_clip": fn, "_no": no, "_line": c})
    slides.sort(key=lambda s: s["_line"])
    prev = -1
    for s in slides:
        if s["_line"] <= prev:
            s["_line"] = min(prev + 1, len(lines) - 1)
            s["match"] = lines[s["_line"]]
        prev = s["_line"]

    # ── CAN BANG NHIP: day entry nao co gap <MIN_GAP sang dong ke tiep con trong.
    #    Vi sao can: vong chinh cap nhat `last_t` theo thu tu WANT, con ket qua cuoi
    #    duoc sort lai theo `_line` => vai cho van dinh gap nho. Do o video 30:
    #    7 entry <6s truoc khi co buoc nay.
    taken = {s["_line"] for s in slides}
    for k in range(1, len(slides)):
        prev_t = starts[slides[k - 1]["_line"]]
        if starts[slides[k]["_line"]] - prev_t >= MIN_GAP:
            continue
        hi = slides[k + 1]["_line"] - 1 if k + 1 < len(slides) else len(lines) - 1
        cand = [j for j in range(slides[k]["_line"] + 1, hi + 1)
                if j not in taken and starts[j] - prev_t >= MIN_GAP]
        if cand:
            taken.discard(slides[k]["_line"])
            slides[k]["_line"] = cand[0]
            slides[k]["match"] = lines[cand[0]]
            taken.add(cand[0])

    OUT.write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── GATE
    bad = [s for s in slides if sum(1 for L in lines if L == s["match"]) != 1]
    secs = [starts[s["_line"]] for s in slides]
    g = [secs[i + 1] - secs[i] for i in range(len(secs) - 1)]
    lech = [(s["_no"], s["_clip"], round(abs(anc[s["_no"]] - starts[s["_line"]])))
            for s in slides
            if s["_no"] in anc and abs(anc[s["_no"]] - starts[s["_line"]]) > 45]
    print(f"\n── SLIDES: {len(slides)} entry -> {OUT.name}")
    print(f"   khoang cach GIAY: min {min(g):.1f} · trung vi {statistics.median(g):.1f} "
          f"· max {max(g):.1f}")
    print(f"   entry <6s: {sum(1 for x in g if x < 6)} · >20s: {sum(1 for x in g if x > 20)}"
          f" · nhip {len(slides)/(T/60):.2f} doi hinh/phut (tran 6,0)")
    print("   ✅ moi `match` khop dung 1 dong" if not bad else f"   🔴 {len(bad)} match hong")
    if lech:
        print(f"   ⚠️ {len(lech)} anchor lech >45s:")
        for no, fn, d in lech[:5]:
            print(f"      clip {no:3d} {fn:30s} lech {d}s")
    else:
        print("   ✅ khong anchor nao lech >45s")

    if a.place:
        cl = VD / "clips"
        cl.mkdir(parents=True, exist_ok=True)
        n, miss = 0, []
        for i, s in enumerate(slides):
            src, dst = cl / s["_clip"], cl / f"clip_{i:02d}.mp4"
            if not src.exists():
                miss.append(s["_no"])
                continue
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dst)
                n += 1
        print(f"\n✅ dat {n} clip_XX.mp4")
        if miss:
            print(f"🔴 THIEU {len(miss)} clip (so {min(miss)}-{max(miss)}) "
                  f"-> KHONG render (render-background.md §1.5)")
            return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
