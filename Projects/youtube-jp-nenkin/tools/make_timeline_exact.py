# -*- coding: utf-8 -*-
r"""make_timeline_exact.py — wav + timeline.json từ MỘT lượt synth, khớp tuyệt đối.

🔴 VÌ SAO CÓ TOOL NÀY (nenkin 18, 2026-08-30): `synth_voice_full.py` gọi `tts_render.py` CLI
(khoảng nghỉ mặc định của CLI) còn `make_timeline.py` ước độ dài bằng `/audio_query` với gap
0,45/1,0 ⇒ **hai phép tính khác nhau cho cùng một bài**. Đo trên video 18: lệch không đơn điệu
(+2,9 → −2,7 → +3,8 → +5,5 → **+8,6s ở đuôi**) ⇒ phụ đề/scene nửa sau lệch 3–8s và câu kết
bị cắt khỏi video (DUR lấy từ timeline 913,7s, wav thật 922,3s). Gate "lệch ≤1,5%" cho qua vì
nó chỉ so TỔNG.

Cách đúng: dùng `video_render.render_audio_timeline()` — synth từng dòng (cache hit ⇒ nhanh),
GHÉP wav và ghi start/end **từ chính đoạn wav vừa ghép**. Một nguồn, không thể lệch.
Khoảng nghỉ = mặc định của `video_render.py` (gap 0,6 · section 1,1) = chuẩn pipeline kênh.

CHẠY:  python tools/make_timeline_exact.py <stem>
       → 06_VIDEO/<stem>/voice_full.wav (ghi đè) + timeline.json (ghi đè) + bản cũ giữ *.bak
"""
import json
import shutil
import sys
from pathlib import Path
from types import SimpleNamespace

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HEALTH = Path(r"E:\Claude\Projects\youtube-jp-health\tools")
sys.path.insert(0, str(HEALTH))
import channels          # noqa: E402
import video_render      # noqa: E402

PROJ = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) < 2:
        print("dùng: python tools/make_timeline_exact.py <stem>")
        return 1
    stem = sys.argv[1]
    ch = channels.CHANNELS["nenkin"]
    src = PROJ / "03_SCRIPTS" / f"{stem}_TTS.md"
    vd = PROJ / "06_VIDEO" / stem
    vd.mkdir(parents=True, exist_ok=True)
    wav = vd / "voice_full.wav"
    tlp = vd / "timeline.json"
    for p in (wav, tlp):
        if p.exists():
            shutil.copy(p, p.with_suffix(p.suffix + ".bak_est"))
    args = SimpleNamespace(engine="voicevox", gap=0.6, section_gap=1.1,
                           speaker=ch["speaker"], style=ch.get("style"),
                           speed=ch["speed"], intonation=ch["intonation"],
                           # ⭐ 2026-09-06: giọng 2 cho dòng mở đầu [聞] (khuôn 2 vai).
                           # Tool này TỰ dựng args (không qua argparse của video_render)
                           # nên phải tự lấy 2 khoá này từ hồ sơ — quên là dòng [聞]
                           # im lặng đọc bằng giọng 1 và không ai biết.
                           speaker2=ch.get("speaker2"), style2=ch.get("style2"))
    print(f"giọng {ch['speaker']}/{ch.get('style')} speed {ch['speed']} · gap {args.gap}/{args.section_gap}")
    if ch.get("speaker2"):
        print(f"giọng 2 (聞き手, dòng [聞]) {ch['speaker2']}/{ch.get('style2')}")
    timeline, total = video_render.render_audio_timeline(str(src), str(wav), args)
    n2 = sum(1 for l in timeline if l.get("spk") == "s2")
    if n2:
        print(f"  ↳ {n2}/{len(timeline)} dòng là 聞き手 ({n2/len(timeline)*100:.0f}%)")
    tlp.write_text(json.dumps({"total": round(total, 3), "lines": timeline},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    # đối chiếu với wav thật bằng ffprobe — phải trùng tới 0,1%
    import subprocess
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(wav)], capture_output=True, text=True)
    real = float(r.stdout.strip() or 0)
    print(f"✓ {len(timeline)} dòng · timeline {total:.2f}s · wav {real:.2f}s · "
          f"lệch {abs(real-total)/real*100:.3f}%")
    print(f"→ {wav}\n→ {tlp}")
    return 0 if abs(real - total) / real < 0.001 else 2


if __name__ == "__main__":
    sys.exit(main())
