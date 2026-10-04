# -*- coding: utf-8 -*-
"""Kiểm mọi 'match' trong SLIDES.json có tồn tại và DUY NHẤT trong _TTS.md (bắt lỗi trước khi render)."""
import io, json, re, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

TTS = Path(r"E:\Claude\Projects\youtube-jp-kaigo\03_SCRIPTS\01_ninchisho-koza-toketsu_TTS.md")
SL = Path(r"E:\Claude\Projects\youtube-jp-kaigo\03_SCRIPTS\01_ninchisho-koza-toketsu_SLIDES.json")

lines = [re.sub(r"\[[^\]]*\]", "", l).strip() for l in TTS.read_text(encoding="utf-8").splitlines()]
lines = [l for l in lines if l and l != "---"]
slides = json.loads(SL.read_text(encoding="utf-8"))

bad, dup, ok = [], [], 0
seen_idx = {}
for i, s in enumerate(slides):
    m = s["match"]
    hits = [j for j, l in enumerate(lines) if m in l]
    if not hits:
        bad.append((i, m))
    else:
        if len(hits) > 1:
            dup.append((i, m, len(hits)))
        ok += 1
        seen_idx.setdefault(hits[0], []).append(i)

print(f"SLIDES: {len(slides)} entry · khớp {ok} · KHÔNG khớp {len(bad)} · match trùng nhiều dòng {len(dup)}")
for i, m in bad:
    print(f"  ❌ [{i}] không thấy: {m}")
for i, m, n in dup:
    print(f"  ⚠️ [{i}] khớp {n} dòng (lấy dòng đầu): {m[:40]}…")
clash = {k: v for k, v in seen_idx.items() if len(v) > 1}
for k, v in clash.items():
    print(f"  ⚠️ nhiều slide cùng trỏ dòng {k}: entry {v} → 「{lines[k][:40]}…」")

kinds = {}
for s in slides:
    k = "genten" if "genten" in s else "cast" if "cast" in s else "diagram" if "diagram" in s else ("card" if not s.get("photo") else "photo")
    kinds[k] = kinds.get(k, 0) + 1
print("Cơ cấu:", kinds, f"· tổng {len(slides)} slide / {len(lines)} dòng đọc")
print(f"→ 1 slide mỗi ~{len(lines)/len(slides):.1f} dòng đọc")
if kinds.get("cast", 0) > 20:
    print("  ⚠️ cast いらすとや > 20 ảnh/video — vi phạm license")
