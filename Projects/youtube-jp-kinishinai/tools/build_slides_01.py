# -*- coding: utf-8 -*-
"""build_slides_01.py — dung SLIDES cho kinishinai bai 1 tu 06_VIDEO/<stem>/_plan/plan.py.

Xuat:
  03_SCRIPTS/<stem>_SLIDES.json          (video_render.py doc: match / photo+static / card / reveal)
  06_VIDEO/<stem>/_plan/SHOTLIST.md       (ban nguoi duyet)
  06_VIDEO/<stem>/_plan/img_prompts_FLOW.txt   (1 prompt / dong, chi o anh AI — extension bom thang)
  06_VIDEO/<stem>/_plan/img_prompts_TENFILE.txt (dong N -> slides_img/slide_NN.png)
  06_VIDEO/<stem>/_plan/queries.py        (Pexels — anh that TRUOC, fetch_real.py cua yawa)
Gate (chan cung): match duy nhat & trung dung dong · <=6 hinh/phut · guard NO TEXT <=15% prompt.
Canh bao: shot <6s (so UOC 285 ky/phut — do lai tren timeline.json sau khi co voice).
Chay: python tools/build_slides_01.py 01_kuchiguse-hitonome
"""
import sys, io, json, re, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
CPS = 285 / 60

STYLE = ("NO TEXT: no letters, no numbers, no writing, no logos anywhere in the picture; every paper, sign, "
         "flyer, screen, book and box is blank. A 16:9 photorealistic photograph, natural documentary look, "
         "real Japanese people and real Japanese places of today unless an older era is stated, soft natural light, "
         "warm gentle colours, bright and airy, shallow depth of field. SCENE: ")
TAIL = " Keep the main subject inside the left 85% of the frame, bottom-right corner plain. No watermark, no signature, no text."


def load_plan(vd):
    spec = importlib.util.spec_from_file_location("plan", vd / "_plan" / "plan.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.P


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    raw = (PROJ / "03_SCRIPTS" / f"{stem}_TTS.md").read_text(encoding="utf-8").splitlines()
    L = [re.sub(r"^(\[[^\]]*\])+", "", l).strip() for l in raw if l.strip() and not l.startswith("#")]
    P = load_plan(vd)
    ats = [p["at"] for p in P]
    assert ats == sorted(ats) and len(set(ats)) == len(ats), "plan: 'at' phai tang dan, khong trung"
    assert ats[0] == 0, "shot dau phai bat dau o dong 0"
    err = []
    slides, rows, flow, ten, Q = [], [], [], [], {}
    n_img = 0
    for i, p in enumerate(P):
        a, b = p["at"], (P[i + 1]["at"] if i + 1 < len(P) else len(L))
        text = L[a:b]
        sec = sum(len(t) for t in text) / CPS
        # match: tien to ngan nhat ma dong DAU TIEN chua no chinh la dong a (video_render lay hit dau tien)
        m = None
        for k in range(6, len(L[a]) + 1):
            cand = L[a][:k]
            first = next(j for j, t in enumerate(L) if cand in t)
            if first == a:
                m = cand; break
        if m is None:
            err.append(f"shot {i}: khong tao duoc match duy nhat cho dong {a}: {L[a]}")
            m = L[a]
        e = {"match": m, "_shot": i, "_est": round(sec, 1)}
        k = p["k"]
        if k == "img":
            e.update({"photo": True, "static": True})
            prompt = STYLE + p["d"] + "." + TAIL
            pos = prompt.find("NO TEXT") * 100 // len(prompt)
            if pos > 15:
                err.append(f"shot {i}: guard NO TEXT o {pos}%")
            flow.append(prompt); n_img += 1
            ten.append(f"dong {n_img:3d} -> slide_{i:02d}.png")
            Q[i] = p.get("q", "AI")
            desc = p["d"] + (f"  〔Pexels: {p['q']}〕" if p.get("q") else "")
            typ = "ẢNH" if not p.get("q") else "ẢNH (thật trước)"
        elif k == "card":
            e.update({"photo": True, "static": True, "card": p["card"]})
            desc = " ／ ".join(p["card"].get("lines", [])) or p["card"]["type"]
            typ = f"THẺ {p['card']['type']}"
        elif k == "reveal":
            e.update({"video": True, "reveal": {"lines": p["lines"], "times": []}})
            desc = " ／ ".join(p["lines"])
            typ = "CHỮ HIỆN DẦN"
        else:
            raise SystemExit(f"kind la: {k}")
        slides.append(e)
        rows.append((i, sec, typ, " / ".join(text), desc))

    tot = sum(r[1] for r in rows)
    per_min = len(rows) / (tot / 60)
    short = [(r[0], round(r[1], 1)) for r in rows if r[1] < 6.0]
    if per_min > 6.0:
        err.append(f"{per_min:.2f} hinh/phut > 6")

    (PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json").write_text(json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")
    pl = vd / "_plan"
    (pl / "img_prompts_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (pl / "img_prompts_TENFILE.txt").write_text("\n".join(ten) + "\n", encoding="utf-8")
    (pl / "queries.py").write_text('# -*- coding: utf-8 -*-\n"""Pexels cho tung shot anh (key = _shot). "AI" = khong co stock hop -> gen AI."""\nQ = '
                                   + json.dumps(Q, ensure_ascii=False, indent=0).replace('"AI"', '"AI"') + "\n", encoding="utf-8")
    # SHOTLIST
    cnt = {}
    for r in rows:
        cnt[r[2].split()[0] if r[2].startswith("THẺ") else r[2]] = cnt.get(r[2].split()[0] if r[2].startswith("THẺ") else r[2], 0) + 1
    md = [f"# {stem} — SHOT LIST (dựng từ `_plan/plan.py`, `tools/build_slides_01.py`)", "",
          f"> **{len(rows)} slide ≈ {tot/60:.1f}′ ({per_min:.2f} hình/phút)** · " +
          " · ".join(f"{k} {v}" for k, v in cnt.items()) +
          f" · ảnh cần gen/tìm: **{n_img}** (có từ khoá Pexels: {sum(1 for v in Q.values() if v != 'AI')}).",
          "> ⚠️ Mốc giây là **ƯỚC 285 ký/phút** — sau khi render voice phải đo lại từ `timeline.json`. "
          f"Shot ước <6s: {short or 'không có'}.",
          "> Motif 「見張り番」 = đèn lồng giấy 行灯 (7 shot). Số liệu = thẻ FONT (không để AI vẽ số).", "",
          "| # | mốc ước | giây | loại | câu đang đọc | hình |", "|---|---|---|---|---|---|"]
    t = 0.0
    for i, sec, typ, txt, desc in rows:
        md.append(f"| {i} | {int(t//60):02d}:{int(t%60):02d} | {sec:.1f} | {typ} | {txt[:48].replace('|','｜')} | {desc[:140].replace('|','｜')} |")
        t += sec
    (pl / "SHOTLIST.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{len(rows)} slide · {tot/60:.2f}′ · {per_min:.2f} hinh/phut · anh {n_img} · the {cnt.get('THẺ',0)} · chu hien dan {cnt.get('CHỮ HIỆN DẦN',0)}")
    print(f"shot uoc <6s: {short}")
    if err:
        print("🔴 GATE DO:"); [print("  -", x) for x in err]; sys.exit(1)
    print("✅ GATE SACH: match duy nhat · <=6 hinh/phut · guard <=15%")


if __name__ == "__main__":
    main()
