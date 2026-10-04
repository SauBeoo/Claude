# -*- coding: utf-8 -*-
r"""make_timeline.py — mốc thời gian TỪNG DÒNG của `_TTS.md`, KHÔNG synth lại.

⭐ VÌ SAO CÓ TOOL NÀY: để đặt scene/sticker/banner khớp lời trong Remotion, cần biết mỗi
dòng bắt đầu và kết thúc ở giây nào. `tts_render.py` **không xuất timeline** (chỉ ra wav);
timeline vốn do `video_render.py::render_audio_timeline` sinh ra, nhưng chạy nó là kéo theo
cả khâu dựng slide + encode ffmpeg — vô ích khi mình dựng hình bằng Remotion.

🔴 CÁCH ĐO: gọi VOICEVOX **`/audio_query`** cho từng dòng rồi cộng độ dài mora
(`consonant_length + vowel_length` + `pause_mora` + `pre/postPhonemeLength`), chia
`speedScale`. Đây là **cùng con số** engine dùng khi synth, nên timeline khớp tuyệt đối với
`voice_full.wav` — mà **không phát lại một byte audio nào**.
⚠️ Dùng lại đúng `parse_script()` của `tts_render.py`, KHÔNG tự tách dòng: nó xử lý tag
`[速/抑揚/間/後間]`, dòng chỉ-có-tag (đổi mặc định), `---`, và luật gộp pause. Tự tách lại là
timeline lệch khỏi wav ngay dòng đầu có tag.

CHẠY:  python tools/make_timeline.py <stem>        # → 06_VIDEO/<stem>/timeline.json
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")

PROJ = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:50021"


def query_dur(tr, text, style_id, speed):
    """Độ dài dòng (giây) từ audio_query — không synth."""
    q = tr.api(BASE, "POST", "/audio_query", params={"text": text, "speaker": style_id})
    tot = q.get("prePhonemeLength", 0.1) + q.get("postPhonemeLength", 0.1)
    for ap in q.get("accent_phrases", []):
        for m in ap.get("moras", []):
            tot += (m.get("consonant_length") or 0.0) + (m.get("vowel_length") or 0.0)
        pm = ap.get("pause_mora")
        if pm:
            tot += (pm.get("consonant_length") or 0.0) + (pm.get("vowel_length") or 0.0)
    return tot / (speed or 1.0)


def main():
    if len(sys.argv) < 2:
        print("dùng: python tools/make_timeline.py <stem>")
        return 1
    stem = sys.argv[1]
    src = PROJ / "03_SCRIPTS" / f"{stem}_TTS.md"
    if not src.exists():
        print(f"🔴 không thấy {src}")
        return 1

    import channels  # noqa: E402
    import tts_render as tr  # noqa: E402
    ch = channels.CHANNELS["nenkin"]

    spk = tr.api(BASE, "GET", "/speakers")
    # ⚠️ `resolve_style` trả về TUPLE `(tên, style, id)`, không phải int. Truyền cả tuple
    # vào `?speaker=` thì VOICEVOX trả **422 int_parsing** — lấy phần tử thứ 3.
    style_id = tr.resolve_style(spk, ch["speaker"], ch["style"])[2]
    gap = tr.DEFAULT_GAP if hasattr(tr, "DEFAULT_GAP") else 0.45
    sgap = tr.DEFAULT_SECTION_GAP if hasattr(tr, "DEFAULT_SECTION_GAP") else 1.0
    events = tr.parse_script(src, gap, sgap)

    t, out = 0.0, []
    for e in events:
        if "pause" in e:
            t += e["pause"]
            continue
        sp = e.get("speed") or ch["speed"]
        d = query_dur(tr, e["text"], style_id, sp)
        out.append({"start": round(t, 3), "end": round(t + d, 3), "text": e["text"]})
        t += d

    vd = PROJ / "06_VIDEO" / stem
    vd.mkdir(parents=True, exist_ok=True)
    dst = vd / "timeline.json"
    dst.write_text(json.dumps({"total": round(t, 3), "lines": out},
                              ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"✓ {len(out)} dòng · tổng {t:.1f}s = {int(t)//60}:{int(t)%60:02d}")
    print(f"→ {dst}")
    # ⛔ Đối chiếu với wav THẬT — lệch >1,5% là parse khác cái đã synth, đừng cho qua.
    wav = vd / "voice_full.wav"
    if wav.exists():
        import wave
        with wave.open(str(wav)) as w:
            real = w.getnframes() / w.getframerate()
        dev = abs(real - t) / real * 100
        flag = "✓" if dev <= 1.5 else "🔴 LỆCH — timeline không khớp wav"
        print(f"{flag} wav thật {real:.1f}s · timeline {t:.1f}s · lệch {dev:.2f}%")
        if dev > 1.5:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
