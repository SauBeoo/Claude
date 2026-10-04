# -*- coding: utf-8 -*-
"""segment_shots.py — chia _TTS.md thanh shot (1 shot = 1 hinh) cho SLIDES kinishinai.

Luat (audience-45plus.md §2): moi hinh >= 6s, <= 6 lan doi hinh/phut. Chua co voice => uoc
285 ky/phut (4,75 ky/s). Dong "その◯。" = the chuong rieng, giu luon cau dau cua muc (the >=6s). Gop dong lien tiep toi khi du
MIN_S giay; khong vuot MAX_S tru khi 1 dong da dai hon. Sau khi co voice: do lai tu timeline.json.
Ghi 06_VIDEO/<stem>/_plan/shots_auto.json. Chay: python tools/segment_shots.py 01_kuchiguse-hitonome
"""
import sys, io, json, re
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
CPS = 285 / 60
MIN_S, MAX_S = 7.5, 13.0

def main():
    stem = sys.argv[1]
    raw = (PROJ / "03_SCRIPTS" / f"{stem}_TTS.md").read_text(encoding="utf-8").splitlines()
    lines = [re.sub(r"^(\[[^\]]*\])+", "", l).strip() for l in raw if l.strip() and not l.startswith("#")]
    shots, cur = [], []
    def sec(ls): return sum(len(x) for x in ls) / CPS
    def flush():
        nonlocal cur
        if cur: shots.append({"kind": "img", "lines": cur, "sec": round(sec(cur), 1)}); cur = []
    for l in lines:
        if re.match(r"^その[一二三四五六七]。", l):
            flush(); shots.append({"kind": "chapter", "lines": [l], "sec": 0}); pend_ch = True; continue
        if shots and shots[-1]["kind"] == "chapter" and not cur and shots[-1]["sec"] == 0:
            # the chuong giu luon cau dau cua muc (tranh the <6s) — hinh canh vao tu cau 2
            shots[-1]["lines"].append(l); shots[-1]["sec"] = round(sec(shots[-1]["lines"]), 1); continue
        if cur and sec(cur) >= MIN_S:
            flush()
        elif cur and sec(cur + [l]) > MAX_S and sec(cur) >= 4.0:
            flush()
        cur.append(l)
    flush()
    # shot cuoi qua ngan -> gop vao shot truoc
    for i in range(len(shots) - 1, 0, -1):
        if shots[i]["kind"] == "img" and shots[i]["sec"] < 5.0 and shots[i - 1]["kind"] == "img":
            shots[i - 1]["lines"] += shots[i]["lines"]; shots[i - 1]["sec"] = round(sec(shots[i - 1]["lines"]), 1); del shots[i]
    for i, s in enumerate(shots): s["id"] = i
    out = PROJ / "06_VIDEO" / stem / "_plan" / "shots_auto.json"
    out.write_text(json.dumps(shots, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum(s["sec"] for s in shots)
    short = [s["id"] for s in shots if s["sec"] < 6.0]
    print(f"{len(shots)} shot · {tot/60:.1f} phut · {len(shots)/(tot/60):.2f} hinh/phut · shot <6s: {short}")
    for s in shots:
        print(f'{s["id"]:3d} {s["kind"][:4]} {s["sec"]:5.1f}  ' + " / ".join(s["lines"])[:110])

if __name__ == "__main__":
    main()
