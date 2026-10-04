# -*- coding: utf-8 -*-
"""run_voiceab.py — render CÙNG một đoạn bằng 2 giọng để nghe so sánh (A/B giọng kênh).

Lý do có file này: tên speaker là ký tự Nhật, đưa thẳng qua command line Windows
hay bị mangle (bài học ghi ở CLAUDE.md §Handoff) → gọi ambient_render qua wrapper .py.

    python tools/run_voiceab.py 03_SCRIPTS/_voiceab_demo_TTS.md

Output: 06_VIDEO/_voice_ab/<arm>/voice.wav  (+ subs.srt, timeline.json)
"""
import sys, subprocess
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]

ARMS = {
    # arm: (engine, speaker, speed, intonation)  — nguồn: CLAUDE.md chouhen §Voice
    "A_morioki":  ("aivis",    "morioki",  1.0,  1.0),   # giọng đang dùng của 真夜中の朗読便
    # nguồn: youtube-jp-health/tools/channels.py["co-dai"] — 青山龍星/ノーマル/0.9/1.15
    "B_aoyama":   ("voicevox", "青山龍星",  0.9,  1.15),  # y hệt co-dai (đo: nhanh hơn A 8,6%)
    # 3 bậc chậm hơn để chọn bằng TAI (user chốt 2026-08-01: giữ giọng nam, cho chậm lại)
    "B85_aoyama": ("voicevox", "青山龍星",  0.85, 1.15),
    "B83_aoyama": ("voicevox", "青山龍星",  0.83, 1.15),  # ≈ bằng nhịp A morioki 1.0
    "B80_aoyama": ("voicevox", "青山龍星",  0.80, 1.15),  # sàn — dưới nữa là méo tiếng
}


def main():
    src = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else \
        PROJ / "03_SCRIPTS" / "_voiceab_demo_TTS.md"
    only = sys.argv[2] if len(sys.argv) > 2 else None
    for arm, (engine, speaker, speed, into) in ARMS.items():
        if only and arm != only:
            continue
        out = PROJ / "06_VIDEO" / "_voice_ab" / arm
        out.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, str(PROJ / "tools" / "ambient_render.py"), str(src),
               "--engine", engine, "--speaker", speaker,
               "--speed", str(speed), "--intonation", str(into),
               "--voice-only", "--out-dir", str(out)]
        print(f"\n=== {arm}: {engine} / {speaker} / speed {speed} / 抑揚 {into} ===", flush=True)
        r = subprocess.run(cmd, cwd=str(PROJ))
        if r.returncode != 0:
            raise SystemExit(f"[LỖI] arm {arm} thất bại (exit {r.returncode})")
        print(f"→ {out / 'voice.wav'}")


if __name__ == "__main__":
    main()
