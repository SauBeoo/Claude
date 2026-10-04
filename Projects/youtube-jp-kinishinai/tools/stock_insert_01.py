# -*- coding: utf-8 -*-
"""stock_insert_01.py — chen 6 CLIP THAT (Pexels, free thuong mai) vao ban minh hoa 絵本 kinishinai bai 1.

User 2026-10-03: "parallax + ghep 6 clip that". Chi canh DO VAT / KHONG KHI (khong can mat nhan vat).
- THAY ca o: 16 (viet thu) · 23 (Shibuya) · 26 (kinh) · 110 (am tra) — o minh hoa cu khong dung.
- CHIA o (giu tranh co Kieko o nua dau, clip that nua sau): 94 (noi lau boc hoi) · 105 (quyt boc vo).
  Entry nua sau APPEND cuoi SLIDES (match cung dong + offset) -> khong xo chi so cu.
- Chinh mau ve tong KEM AM cua tranh (bot bao hoa, am do/vang, nang toi) + 1920x1080 30fps, cat dung thoi luong o.
- License + url goc ghi 06_VIDEO/<stem>/ATTRIBUTIONS.md; danh dau used_in vao so den _media_library (media-library §2).
Chay SAU kb_cells_01.py (no ghi de clip_NN cua o THAY):  python tools/stock_insert_01.py 01_kuchiguse-hitonome
"""
import sys, io, json, subprocess, urllib.request
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
PICK = {16: (0, "replace"), 23: (0, "replace"), 26: (1, "replace"), 110: (2, "replace"), 94: (0, "split"), 105: (1, "split")}
GRADE = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,"
         "eq=saturation=0.78:contrast=0.93:brightness=0.035:gamma=1.04,"
         "colorbalance=rs=0.07:gs=0.03:bs=-0.07:rm=0.06:gm=0.02:bm=-0.06:rh=0.04:bh=-0.05,"
         "noise=alls=4:allf=t,setsar=1,format=yuv420p")


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sp = PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json"
    sl = json.loads(sp.read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8")); L = tl["lines"]; T = tl["total"]
    cand = json.loads((vd / "_cand_video" / "cand.json").read_text(encoding="utf-8"))
    st = sorted((next(l for l in L if e["match"] in l["text"])["start"] + float(e.get("offset", 0)), i) for i, e in enumerate(sl))
    st[0] = (0.0, st[0][1])
    dur = {i: ((st[k + 1][0] if k + 1 < len(st) else T) - t) for k, (t, i) in enumerate(st)}
    raw = vd / "_stock_raw"; raw.mkdir(exist_ok=True)
    cd = vd / "clips"
    attr = ["# ATTRIBUTIONS — clip that (Pexels License: free thuong mai, khong bat buoc credit — ghi de truy nguon)", ""]
    for s, (k, how) in PICK.items():
        it = cand[str(s)]["items"][k]
        src = raw / f"pexels_{it['id']}.mp4"
        if not src.exists():
            req = urllib.request.Request(it["file"], headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r, open(src, "wb") as f:
                f.write(r.read())
        if how == "replace":
            idx, d = s, dur[s] + 0.5
        else:
            assert not any(e.get("_stock_of") == s for e in sl), f"o {s} da chia roi"
            half = round(dur[s] / 2, 2)
            idx = len(sl)
            sl.append({"match": sl[s]["match"], "offset": float(sl[s].get("offset", 0)) + half, "video": True,
                       "_stock_of": s})
            d = dur[s] - half + 0.5
        sl[idx]["video"] = True; sl[idx]["_stock"] = f"pexels {it['id']}"
        out = cd / f"clip_{idx:02d}.mp4"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", str(src), "-t", f"{d:.2f}", "-vf", GRADE,
                            "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium", str(out)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-400:]
        attr.append(f"- slide {s}{' (nua sau)' if how == 'split' else ''}: Pexels video {it['id']} by {it['user']} — {it['url']}")
        print(f"o {s:3d} {how:7s} -> clip_{idx:02d} ({d:.1f}s) pexels {it['id']}")
        try:
            import media_lib as ML
            nm = ML.add_file(str(src), kind="clip", source="pexels", source_id=str(it["id"]), url=it["url"],
                             license="Pexels License", used_by=f"kinishinai/{stem}")
            ML.mark_used(nm, f"kinishinai/{stem}")
        except Exception as ex:                       # so den la bat buoc — bao, khong im lang
            print("  ⚠️ chua ghi duoc so den media_lib:", ex)
    sp.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8")
    (vd / "ATTRIBUTIONS.md").write_text("\n".join(attr) + "\n", encoding="utf-8")
    print("OK ->", sp.name, "+ ATTRIBUTIONS.md")


if __name__ == "__main__":
    main()
