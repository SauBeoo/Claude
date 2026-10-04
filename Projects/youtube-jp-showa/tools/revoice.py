# -*- coding: utf-8 -*-
"""revoice.py — synth LẠI giọng + timeline + subs cho một video, KHÔNG dựng lại hình.

Vì sao cần: `video_render.py` là pipeline trọn gói (voice → timeline → slides → mp4).
Khi chỉ đổi thông số GIỌNG (tốc độ, khoảng nghỉ) mà lớp hình đã chuyển sang remotion-vox
thì chạy trọn gói là thừa 30–40 phút và còn bị preflight chặn vì thiếu ảnh. Tool này gọi
thẳng `render_audio_timeline` + `write_srt` của video_render, dừng ngay sau khi có
voice.wav / timeline.json / subs.srt.

⚠️ Đổi giọng là đổi TOÀN BỘ mốc thời gian ⇒ sau tool này phải chạy lại đủ chuỗi:
    1) revoice.py                      (giọng + timeline mới)
    2) remotion-vox/tools/import_pipeline.py   (nạp timeline mới vào project)
    3) remotion-vox/tools/patch_archival.py    (26 clip hình)
    4) remotion-vox/tools/add_sfx.py           (4 lớp tiếng)
Bỏ bước nào cũng ra video lệch tiếng-hình mà KHÔNG có lỗi nào báo.

Usage:
  py -3 tools/revoice.py --stem 01_kyushoku --channel showa --gap 0.35 --section-gap 0.7
"""

import argparse
import json
import shutil
import sys
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
sys.stdout.reconfigure(encoding="utf-8")

import channels  # noqa: E402
import video_render as V  # noqa: E402

ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stem", required=True)
    ap.add_argument("--channel", required=True)
    ap.add_argument("--gap", type=float, required=True)
    ap.add_argument("--section-gap", type=float, default=None)
    ap.add_argument("--speed", type=float, default=None, help="ghi đè tốc độ nền của hồ sơ kênh")
    a = ap.parse_args()

    prof = channels.CHANNELS[a.channel]
    tts = ROOT / "03_SCRIPTS" / f"{a.stem}_TTS.md"
    vdir = ROOT / "06_VIDEO" / a.stem
    if not tts.exists():
        print(f"❌ không thấy {tts}")
        return 2

    args = Namespace(
        engine=prof.get("engine", "voicevox"),
        speaker=prof["speaker"],
        style=prof.get("style"),
        speed=a.speed if a.speed is not None else prof["speed"],
        intonation=prof.get("intonation", 1.15),
        gap=a.gap,
        section_gap=a.section_gap if a.section_gap is not None else round(a.gap * 1.1 / 0.6, 2),
        sub_size=prof.get("sub_size"),
        sub_style=prof.get("sub_style"),
        sub_accent=None,
    )
    print(f"giọng: {args.speaker}/{args.style} · speed {args.speed} · 抑揚 {args.intonation}")
    print(f"khe   : dòng trống {args.gap}s · đổi section {args.section_gap}s")

    # giữ bản cũ để so, và để quay lại được nếu nghe không ưng
    for f in ("voice.wav", "timeline.json", "subs.srt"):
        src = vdir / f
        if src.exists() and not (vdir / f"_old_{f}").exists():
            shutil.copy2(src, vdir / f"_old_{f}")

    old = None
    tl_path = vdir / "timeline.json"
    if tl_path.exists():
        old = json.loads(tl_path.read_text(encoding="utf-8"))["total"]

    timeline, total = V.render_audio_timeline(tts, vdir / "voice.wav", args)
    tl_path.write_text(json.dumps({"total": total, "lines": timeline},
                                  ensure_ascii=False, indent=1), encoding="utf-8")

    maxlen = V.SUB_MAXLEN if not args.sub_size else max(24, int(V.SUB_MAXLEN * 17 / args.sub_size))
    V.write_srt(timeline, vdir / "subs.srt", maxlen)

    print(f"\n✅ voice.wav {total/60:.2f} phút · {len(timeline)} dòng · subs.srt viết lại")
    if old:
        print(f"   trước: {old/60:.2f} phút → ngắn hơn {old-total:.1f}s ({(old-total)/old*100:.1f}%)")
    print("\n⚠️ CHƯA XONG. Chạy tiếp: import_pipeline → patch_archival → add_sfx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
