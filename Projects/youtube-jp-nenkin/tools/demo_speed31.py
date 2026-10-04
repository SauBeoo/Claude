# -*- coding: utf-8 -*-
r"""demo_speed31.py — demo NGHE THỬ tốc độ đọc cho video 31 (user 2026-09-27: "giọng đọc hơi nhanh").

Cùng một đoạn (dòng timeline 37–47, chương 148万円, dày số), synth bằng ĐÚNG đường của bài
(`video_render.render_audio_timeline`, hồ sơ `channels.CHANNELS["nenkin"]`), chỉ đổi 2 biến:
  A  speed 0.90 · gap 0.6/1.1   = bản hiện tại
  B  speed 0.85 · gap 0.6/1.1   = chỉ chậm giọng
  C  speed 0.90 · gap 0.9/1.4   = chỉ nghỉ dài hơn giữa câu
  D  speed 0.85 · gap 0.9/1.4   = cả hai
⚠️ `audience-45plus.md` §5.2 gate 1 ghi speed ≤0,90 "KHÔNG hạ thêm" — user nghe bản thật và thấy
nhanh ⇒ đo bằng tai user, không suy từ luật. Kết quả chọn xong phải ghi lại vào luật.
CHẠY:  python tools/demo_speed31.py   → 06_VIDEO/<stem>/demo_speed/{A,B,C,D}.wav + bảng giây
"""
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HEALTH = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(HEALTH))
import channels          # noqa: E402
import video_render      # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
STEM = "31_fuyo-shinkokusho-hikazei-domino"
VD = PROJ / "06_VIDEO" / STEM
OUT = VD / "demo_speed"
L0, L1 = 37, 48
VARIANTS = {"A": (0.90, 0.6, 1.1), "B": (0.85, 0.6, 1.1), "C": (0.90, 0.9, 1.4),
            "D": (0.85, 0.9, 1.4)}


def main():
    ch = channels.CHANNELS["nenkin"]
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    want = [re.sub(r"^(?:\[[^\]]*\])+", "", l["text"]).strip() for l in tl[L0:L1]]
    src = (PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md").read_text(encoding="utf-8").splitlines()
    raw = []
    for w in want:  # lấy NGUYÊN dòng TTS (giữ tag đầu dòng)
        hit = [s for s in src if re.sub(r"^(?:\[[^\]]*\])+", "", s).strip() == w]
        if len(hit) != 1:
            print(f"🔴 không khớp đúng 1 dòng TTS: {w[:30]} -> {len(hit)}")
            return 1
        raw.append(hit[0])
    OUT.mkdir(exist_ok=True)
    md = OUT / "demo_TTS.md"
    md.write_text("\n\n".join(raw) + "\n", encoding="utf-8")
    nch = sum(len(w) for w in want)
    print(f"đoạn: dòng {L0}–{L1 - 1} · {len(want)} dòng · {nch} ký")
    for key, (sp, g, sg) in VARIANTS.items():
        args = SimpleNamespace(engine="voicevox", gap=g, section_gap=sg, speaker=ch["speaker"],
                               style=ch.get("style"), speed=sp, intonation=ch["intonation"],
                               speaker2=ch.get("speaker2"), style2=ch.get("style2"))
        _tl, total = video_render.render_audio_timeline(str(md), str(OUT / f"{key}.wav"), args)
        print(f"  {key}  speed {sp:.2f} · nghỉ {g}/{sg}  →  {total:5.1f}s · {nch / total * 30:5.1f} ký/30s")
    print(f"→ {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
