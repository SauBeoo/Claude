# -*- coding: utf-8 -*-
r"""sync_report31.py — CHẠY KHÔ phép neo telop vào lời đọc (build28.sync_times), không render.

In mỗi ô: từng dòng chính / thẻ phụ → giây vào + chuỗi lời nó khớp. Soi bảng này TRƯỚC khi build:
khối «—» = không khớp được (vào sau khối trước 0,6s) ⇒ xem có phải telop viết lệch lời không.
CHẠY:  python tools/sync_report31.py   → 06_VIDEO/<stem>/telop_sync.txt
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ / "tools"))
import build31  # noqa: E402,F401  (đặt STEM/VD/PLAN/TELOP vào build28)
import build28 as b  # noqa: E402


def main():
    plan = json.loads((b.VD / b.PLAN_NAME).read_text(encoding="utf-8"))
    tl = json.loads((b.VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    shots = plan["shots"]
    out, n_el, n_miss, n_late, n_old_early = [], 0, 0, 0, 0
    for k, s in enumerate(shots):
        nxt = shots[k + 1]["t0"] if k + 1 < len(shots) else s["t1"]
        dur = nxt - s["t0"]
        sh = dict(b.TELOP[k]); sh.setdefault("sub", [])
        live = [i for i, ln in enumerate(tl) if ln["start"] < nxt - 1e-3 and ln["end"] > s["t0"] + 1e-3]
        tb, ts, rows = b.sync_times(sh, live, tl, s["t0"], dur)
        out.append(f"── ô {k:02d}  {dur:4.1f}s")
        old = [b.T_BIG + i * b.D_BIG for i in range(len(tb))] + [b.T_SUB + i * b.D_SUB for i in range(len(ts))]
        for (kind, txt, t, L, hit), t_old in zip(rows, old):
            n_el += 1
            n_miss += (L < 2 and not (kind == "big" and txt == sh["big"][0]))
            n_old_early += (t - t_old > 2.0)
            out.append(f"   {kind:3s} {t:5.1f}s (cũ {t_old:3.1f})  {txt:<16s}  ← {hit}")
    head = (f"khối: {n_el} · không khớp lời: {n_miss} · khối mà bản CŨ hiện sớm >2s so với lời: "
            f"{n_old_early}")
    (b.VD / "telop_sync.txt").write_text(head + "\n\n" + "\n".join(out) + "\n", encoding="utf-8")
    print(head)
    print(f"→ {b.VD / 'telop_sync.txt'}")


if __name__ == "__main__":
    main()
