# -*- coding: utf-8 -*-
"""grab_stills.py — cắt ẢNH TĨNH (1 frame) từ phim tư liệu PD/CC0 thành JPG 1920x1080 đã grade.

Vì sao có tool này (2026-08-29, user: "không muốn dùng ảnh AI nữa"): kho ẢNH THẬT hợp pháp về đời
sống Nhật 1955–1975 gần như rỗng trên Commons, nhưng một phim 40′ CC0 = hàng nghìn frame thật.
Frame-grab + grade = "ảnh thật" đúng nghĩa, không AI, quyền sạch như chính phim.

Dùng CHUNG crop/grade với cut_archival.py (import) để ảnh tĩnh và clip cùng tông.
Ghi SỔ ĐEN như clip: mỗi still chiếm [t, t+0.5] trong FOOTAGE_USED.json (--record <slug>),
cut_archival.py sau này sẽ né đoạn đó (ov > 0.5 mới chặn, nên still 0.5s không chặn oan clip
cạnh nó — nhưng 2 video không cắt cùng 1 frame).

Usage:
  python tools/grab_stills.py --spec tools/stills_spec_06.json --outdir 06_VIDEO/06_x/real_photos --record 06_x
spec: {"src": "...mp4", "stills": [{"id": "st06_01_boy_train", "t": 542.3, "ybias": 0.5, "note": "..."}]}
"""
import argparse, json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cut_archival import ACTIVE, build_vf  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True); ap.add_argument("--outdir", required=True)
    ap.add_argument("--record", default=""); ap.add_argument("--allow-reuse", action="store_true")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
    src = Path(spec["src"]); active = ACTIVE.get(src.name)
    if active is None:
        print(f"❌ chưa đo vùng ảnh thật cho {src.name}"); return 2
    ledger_p = Path(__file__).resolve().parent.parent / "06_VIDEO" / "_footage_test" / "FOOTAGE_USED.json"
    ledger = json.loads(ledger_p.read_text(encoding="utf-8"))
    item = ledger.get("aliases", {}).get(src.name, src.name)
    clashes = []
    for st in spec["stills"]:
        for u in ledger["used"]:
            if u["item"] != item or (a.record and u["video"] == a.record): continue
            if u["ss"] <= st["t"] <= u["end"] and not u["id"].startswith("st"):
                # frame nằm TRONG clip video khác đã lên sóng → cũng là tái dùng hình
                clashes.append((st["id"], st["t"], u["video"], u["id"]))
    if clashes:
        print(f"🔴 SỔ ĐEN: {len(clashes)} still nằm trong clip đã lên sóng:")
        for c in clashes: print("   ", c)
        if not a.allow_reuse: return 4
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    made = []
    for st in spec["stills"]:
        vf = build_vf(active, float(st.get("ybias", 0.5)), float(st.get("grade", 1.0)), src.name)
        dst = out / f"{st['id']}.jpg"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(st["t"]), "-i", str(src), "-frames:v", "1",
                            "-vf", vf, "-q:v", "2", str(dst)], capture_output=True, text=True)
        if r.returncode:
            print("❌", st["id"], r.stderr[-200:]); return 3
        made.append(st["id"]); print(f"  ✓ {st['id']:28} t={st['t']:7.1f}  {st.get('note','')}")
    print(f"OK {len(made)} still → {out}")
    if a.record and made:
        ledger["used"] = [u for u in ledger["used"] if not (u["video"] == a.record and u["id"] in made)]
        for st in spec["stills"]:
            if st["id"] in made:
                ledger["used"].append({"item": item, "file": src.name, "ss": float(st["t"]), "end": round(float(st["t"]) + 0.5, 2),
                                       "video": a.record, "id": st["id"], "kind": "still"})
        ledger_p.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"   📒 ghi {len(made)} still vào sổ đen '{a.record}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
