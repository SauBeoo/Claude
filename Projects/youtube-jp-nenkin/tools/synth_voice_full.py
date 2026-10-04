# -*- coding: utf-8 -*-
r"""synth_voice_full.py — synth voice TOÀN BỘ script bằng đúng hồ sơ giọng của kênh.

⭐ VÌ SAO CÓ TOOL NÀY, không gọi `tts_render.py` thẳng trong `.cmd`:
tên giọng của kênh là **雀松朱司** — ký tự non-ASCII. Nhét vào `.cmd` là vi phạm luật
`render-background.md` §2.6 ①: cmd.exe đọc file theo codepage OEM **trước khi** `chcp 65001`
kịp có tác dụng ⇒ dòng đó bị tách thành lệnh rác, và tệ nhất là tiến trình vẫn **exit 0**
trong khi log không được tạo. ⇒ mọi tham số tiếng Nhật phải nằm trong file `.py`.

Giọng đọc **từ `channels.py`**, không hằng-số-hoá ở đây — đó là nguồn sự thật duy nhất về
bản sắc kênh (`CLAUDE.md` §②).

CHẠY:  python tools/synth_voice_full.py <stem> [-o <wav>]
"""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")

PROJ = Path(__file__).resolve().parents[1]
HEALTH = Path(r"E:\Claude\Projects\youtube-jp-health\tools")


def main():
    if len(sys.argv) < 2:
        print("dùng: python tools/synth_voice_full.py <stem> [-o <wav>]")
        return 1
    stem = sys.argv[1]
    out = None
    if "-o" in sys.argv:
        out = sys.argv[sys.argv.index("-o") + 1]

    import channels  # noqa: E402
    ch = channels.CHANNELS["nenkin"]
    src = PROJ / "03_SCRIPTS" / f"{stem}_TTS.md"
    if not src.exists():
        print(f"🔴 không thấy {src}")
        return 1
    if out is None:
        out = str(PROJ / "06_VIDEO" / stem / "voice_full.wav")
    Path(out).parent.mkdir(parents=True, exist_ok=True)

    cmd = [sys.executable, str(HEALTH / "tts_render.py"), str(src), "-o", out,
           "--speaker", ch["speaker"], "--speed", str(ch["speed"]),
           "--intonation", str(ch["intonation"])]
    print(f"giọng: {ch['speaker']} / {ch['style']} / speed {ch['speed']} "
          f"/ 抑揚 {ch['intonation']}")
    print(f"→ {out}")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
