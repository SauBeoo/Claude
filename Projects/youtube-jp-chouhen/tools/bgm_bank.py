# -*- coding: utf-8 -*-
"""bgm_bank.py — synth bộ NHẠC NỀN cho kênh 朗読 (license sạch, không tải ngoài).

Vấn đề nó chữa (phát hiện 2026-07-30): cả kênh dùng **đúng 1 file** `bgm/Anguish.mp3` cho
mọi video — hardcode default trong scene_render.py. Nghe 3 video liên tiếp là nhận ra ngay
cùng một cái nền, và đó cũng đúng cái dấu hiệu "hàng loạt" mà YouTube quét.

Sinh vào 06_VIDEO/bgm/pad_*.mp3 — mỗi track một CAO ĐỘ GỐC + màu sắc khác nhau, nghe rõ là
khác track chứ không phải cùng bài đổi tempo. Đây là **mood bed** (drone trầm + nhịp thở
chậm), không phải nhạc có melody — vì ở -40dB dưới giọng đọc thì melody chỉ gây nhiễu,
còn cao độ gốc thì tai vẫn phân biệt được "video này tối hơn / lạnh hơn video kia".

⭐ Muốn nhạc thật có melody: cứ bỏ file .mp3 vào `06_VIDEO/bgm/` — vòng xoay của
scene_render (`--bgm auto`) tự nhặt, không cần sửa code. Chỉ cần license free-thương-mại
và ghi credit vào 概要欄 theo `.claude/rules/youtube-compliance.md`.

Chạy 1 lần: python tools/bgm_bank.py
License: 100% tự synth bằng ffmpeg — không attribution.
"""
import subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "06_VIDEO" / "bgm"
D = 150          # giây/track (scene_render loop lại cho đủ độ dài video)

# name -> (mô tả, root Hz, [ (hệ số tần, gain, chu kỳ LFO giây) ], lowpass)
# Quãng dùng: root + quãng năm (1.5) + quãng ba thứ (1.2) → màu tối, hợp thể loại.
# Chu kỳ LFO lệch nhau giữa các partial → nghe như "thở", không phải tiếng test tone.
TRACKS = {
    "pad_a_kan":   ("La thứ — lạnh, trống (mặc định mùa đông)", 110.0,
                    [(1.0, 0.30, 25), (1.5, 0.20, 15), (2.4, 0.13, 21)], 1100),
    "pad_d_omoi":  ("Rê thứ — nặng, đè (bài nhiều 屈辱)", 73.42,
                    [(1.0, 0.32, 23), (1.5, 0.19, 17), (2.4, 0.12, 29)], 950),
    "pad_e_hari":  ("Mi thứ — căng, sáng hơn (bài nhiều đối đầu)", 82.41,
                    [(1.0, 0.28, 19), (1.5, 0.21, 27), (3.0, 0.11, 13)], 1300),
    "pad_f_shizu": ("Fa — tĩnh, buồn dịu (bài nhiều hồi tưởng)", 87.31,
                    [(1.0, 0.30, 31), (1.5, 0.18, 21), (2.0, 0.12, 25)], 1000),
    "pad_g_fuka":  ("Sol thứ — sâu, trầm nhất (bài bi)", 98.0,
                    [(1.0, 0.33, 27), (1.5, 0.17, 19), (2.4, 0.10, 23)], 850),
    "pad_b_tsume": ("Si thứ — mảnh, lạnh gắt (bài trả thù khô)", 61.74,
                    [(1.0, 0.26, 21), (1.5, 0.22, 29), (3.0, 0.13, 17)], 1400),
}


def build(name, root, partials, lp):
    terms = "+".join(
        f"{g:.3f}*sin(2*PI*{root * m:.2f}*t)*(0.72+0.28*sin(2*PI*t/{p}))"
        for m, g, p in partials)
    # tầng "air": pink noise rất khẽ, có thân 300-1500Hz để loa nhỏ vẫn thấy chuyển động
    src_tone = f"aevalsrc=exprs='{terms}':d={D}:s=48000"
    src_air = f"anoisesrc=c=pink:r=48000:d={D}:a=0.30:seed={int(root)}"
    parts = [
        f"[0:a]lowpass=f={lp},volume=0.9[t]",
        "[1:a]bandpass=f=700:t=h:w=900,volume='0.16+0.08*sin(2*PI*t/33)':eval=frame[air]",
        "[t][air]amix=inputs=2:normalize=0,"
        "loudnorm=I=-23:TP=-4:LRA=7,aresample=48000,"
        "alimiter=limit=0.9,aformat=sample_fmts=s16:channel_layouts=stereo[a]",
    ]
    f = OUT / f"{name}.mp3"
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", src_tone, "-f", "lavfi", "-i", src_air,
           "-filter_complex", ";".join(parts), "-map", "[a]",
           "-c:a", "libmp3lame", "-b:a", "160k", "-t", str(D), str(f), "-loglevel", "error"]
    return subprocess.run(cmd).returncode == 0, f


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (desc, root, partials, lp) in TRACKS.items():
        ok, f = build(name, root, partials, lp)
        print(("OK   " if ok else "FAIL "), f"{f.name:18s} {desc}")
    tracks = sorted(p.name for p in OUT.glob("*.mp3"))
    print(f"\n→ {OUT}  ({len(tracks)} track trong vòng xoay)")
    print("  " + ", ".join(tracks))
    print("\nDùng: python tools/scene_render.py <slug> --bgm auto   (tự chọn track ít dùng nhất,")
    print("      ghi vào bgm/ROTATION.log; render lại cùng slug → LUÔN ra đúng track cũ)")


if __name__ == "__main__":
    main()
