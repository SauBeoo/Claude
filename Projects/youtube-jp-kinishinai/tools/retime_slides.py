# -*- coding: utf-8 -*-
"""retime_slides.py — ghi moc giay THAT (timeline.json) vao SLIDES + do lai nhip hinh.

Sau render_voice_only.py. Cung cach tim match voi video_render.build_slides (hit dau tien
co chua match). Ghi "_t" / "_dur" moi entry; entry "reveal" duoc dien "times" (giay tinh tu
dau slide, luc giong doc toi tung dong chu). In gate: hinh/phut (<=6), slide <6s, tong thoi luong.
Chay: python tools/retime_slides.py 01_kuchiguse-hitonome
"""
import sys, io, json, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]


def norm(s):
    return re.sub(r"[「」『』、。？！…・\s]", "", s)


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]
    sp = PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json"
    sl = json.loads(sp.read_text(encoding="utf-8"))
    starts = []
    for i, e in enumerate(sl):
        hit = next((k for k, ln in enumerate(lines) if e["match"] in ln["text"]), None)
        if hit is None:
            raise SystemExit(f"[LOI] slide {i}: khong thay「{e['match']}」trong timeline")
        starts.append((hit, lines[hit]["start"] if i else 0.0))
    for i, e in enumerate(sl):
        t0 = starts[i][1]
        t1 = starts[i + 1][1] if i + 1 < len(sl) else total
        e["_t"], e["_dur"] = round(t0, 2), round(t1 - t0, 2)
        e.pop("_est", None)
        if "reveal" in e:
            k0 = starts[i][0]; k1 = starts[i + 1][0] if i + 1 < len(sl) else len(lines)
            span = lines[k0:k1]
            times, last = [], 0.0
            for j, show in enumerate(e["reveal"]["lines"]):
                key = norm(show)[:5]
                hit = next((ln for ln in span if key and key in norm(ln["text"])), None)
                if hit is None:            # khong tim duoc dong doc -> rai deu trong slide
                    tt = e["_dur"] * j / len(e["reveal"]["lines"])
                else:
                    # dong chu thu 2+ nam CUNG dong doc voi dong 1 -> uoc theo ty le ky tu trong dong
                    txt = norm(hit["text"]); pos = txt.find(key)
                    tt = hit["start"] - t0 + (hit["end"] - hit["start"]) * (pos / max(len(txt), 1))
                tt = max(tt, last)
                times.append(round(tt, 2)); last = tt
            e["reveal"]["times"] = times
    sp.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8")
    durs = [e["_dur"] for e in sl]
    short = [(i, d) for i, d in enumerate(durs) if d < 6.0]
    pm = len(sl) / (total / 60)
    print(f"tong {total/60:.2f}′ · {len(sl)} slide · {pm:.2f} hinh/phut · trung vi {sorted(durs)[len(durs)//2]:.1f}s · dai nhat {max(durs):.1f}s")
    print(f"slide <6s ({len(short)}): {short}")
    print("🔴 VUOT 6 hinh/phut" if pm > 6 else "✅ <=6 hinh/phut")
    print("🔴 BAI >= 20′" if total >= 1200 else "✅ bai < 20′")
    for i, e in enumerate(sl):
        if "reveal" in e:
            print(f"  reveal slide {i}: dur {e['_dur']}s times {e['reveal']['times']}")


if __name__ == "__main__":
    main()
