# -*- coding: utf-8 -*-
"""ambience_bank.py — synth bộ TIẾNG KHUNG CẢNH (音の風景) cho kênh 朗読.

Khác `sfx_bank.py`: sfx = tiếng SỰ KIỆN một lần (điện thoại rung, gõ cửa); còn đây là
tiếng NỀN của không gian, chảy dưới cả một khối cảnh (bão tuyết ngoài cửa sổ, gió biển
trên boong tàu, cái im của phòng thờ). Đây là lớp mà khán giả kênh này — người NGHE,
không nhìn màn hình — cảm được ngay, và là thứ làm mỗi video có "chỗ" riêng.

Sinh vào 06_VIDEO/_amb/*.wav — 48kHz stereo, 32 giây, **loop liền mạch** (mọi LFO có chu kỳ
là ước của 32s nên đầu-cuối khớp biên độ, không click khi ffmpeg -stream_loop).
Loudness chuẩn hóa I=-23 để mọi bed cùng một mức; to/nhỏ điều bằng `gain` trong FX.json.

Chạy 1 lần: python tools/ambience_bank.py     (thêm bed = thêm entry BANK)
Dùng bởi: fx_mix.py qua event {"type":"ambience", ...} trong <slug>_FX.json.
License: 100% tự synth bằng ffmpeg — không tải ngoài, không attribution.
"""
import subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
OUT = PROJ / "06_VIDEO" / "_amb"
D = 32          # giây / bed
LOUD = "loudnorm=I=-23:TP=-4:LRA=7,aresample=48000"   # loudnorm đổi sample rate → phải aresample

# name -> (mô tả, [ (src_lavfi, post_filter), ... ])  mỗi layer mono, amix lại rồi làm rộng stereo.
# LFO: dùng chu kỳ 8 / 16 / 32 giây (ước của D) để loop không giật.
#
# ⚠️ LUẬT DẢI TẦN (đo thật 2026-07-30, v1 đã fail đúng chỗ này — cùng bài học sfx_bank v2):
# bản đầu dồn hết năng lượng xuống <250Hz → đo ra dải 200-600Hz thấp hơn full-band 47-56dB
# ⇒ **loa điện thoại/tablet không phát được gì**, mà khán giả kênh này (nữ 45-70) nghe bằng
# đúng mấy loa đó. Mọi bed BẮT BUỘC có thân ở **250-1500Hz** (đo: dải 200-600Hz không được
# thấp hơn full-band quá ~25dB — chạy `python tools/ambience_bank.py --check` để kiểm).
# Sub-bass <180Hz chỉ để lót, gain thấp: nó không nghe được trên loa nhỏ mà lại ăn hết
# headroom, khiến loudnorm kéo tụt phần nghe được.
BANK = {
    # bão tuyết ngoài cửa sổ: gió rít (thân 300-1500) + hạt tuyết đập kính + lót trầm
    "blizzard": ("bão tuyết / gió rít ngoài cửa sổ (bệnh viện, con dốc, nhà đêm)", [
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.85:seed=11",
         "highpass=f=200,lowpass=f=1800,volume='0.55+0.40*sin(2*PI*t/8)':eval=frame"),
        (f"anoisesrc=c=white:r=48000:d={D}:a=0.45:seed=23",
         "highpass=f=2600,lowpass=f=7000,volume='0.30+0.20*sin(2*PI*t/16)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.40:seed=37", "lowpass=f=170,volume=0.30"),
    ]),
    # boong tàu: gió biển + sóng đập thân tàu (nhịp chậm 16s) + bụi nước
    "sea_deck": ("gió biển + sóng trên boong tàu (cảnh クルーズ)", [
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.85:seed=41",
         "highpass=f=230,lowpass=f=2200,volume='0.50+0.42*sin(2*PI*t/16)':eval=frame"),
        (f"anoisesrc=c=white:r=48000:d={D}:a=0.42:seed=53",
         "bandpass=f=3800:t=h:w=3000,volume='0.28+0.18*sin(2*PI*t/8)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.40:seed=67", "lowpass=f=140,volume=0.28"),
    ]),
    # cái IM của phòng thờ / phòng có こたつ — phải nghe ra "đang ở trong nhà", không phải im tuyệt đối
    "room_still": ("phòng thờ / phòng khách im (仏間, こたつ) — room tone", [
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.55:seed=83",
         "bandpass=f=500:t=h:w=800,volume='0.45+0.10*sin(2*PI*t/32)':eval=frame"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.30:seed=89",
         "bandpass=f=1400:t=h:w=1200,volume=0.20"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.40:seed=71", "lowpass=f=150,volume=0.28"),
    ]),
    # hành lang bệnh viện đêm: máy chạy đều (có HÀI 300/450Hz để loa nhỏ phát được) + thông gió
    "hospital_night": ("hành lang / phòng bệnh đêm (máy chạy đều, thông gió)", [
        (f"aevalsrc=exprs='0.30*sin(2*PI*300*t)+0.18*sin(2*PI*450*t)"
         f"+0.10*sin(2*PI*150*t)':d={D}:s=48000", "lowpass=f=900,volume=0.85"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.60:seed=101",
         "bandpass=f=800:t=h:w=1100,volume='0.40+0.10*sin(2*PI*t/16)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.40:seed=97", "lowpass=f=160,volume=0.26"),
    ]),
    # mưa trên kính (dùng cho video khác — mùa mưa)
    "rain_window": ("mưa đập cửa kính", [
        (f"anoisesrc=c=white:r=48000:d={D}:a=0.62:seed=103",
         "highpass=f=1200,lowpass=f=8000,volume='0.42+0.16*sin(2*PI*t/8)':eval=frame"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.55:seed=139",
         "bandpass=f=700:t=h:w=900,volume='0.38+0.10*sin(2*PI*t/8)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.38:seed=107", "lowpass=f=190,volume=0.26"),
    ]),
    # phố đêm tuyết: xe xúc tuyết đi xa (hài 180/360Hz), tiếng thành phố
    "night_snowplow": ("phố đêm mùa tuyết, xe xúc tuyết đi xa (nhà mẹ)", [
        (f"aevalsrc=exprs='0.22*sin(2*PI*180*t)+0.16*sin(2*PI*360*t)':d={D}:s=48000",
         f"lowpass=f=700,volume='0.55+0.40*sin(2*PI*t/32)':eval=frame"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.62:seed=113",
         "bandpass=f=650:t=h:w=900,volume='0.38+0.14*sin(2*PI*t/16)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.45:seed=109", "lowpass=f=200,volume=0.30"),
    ]),
    # xe khách đêm: động cơ diesel đều (hài 90/180Hz) + tiếng lốp/đường cao tốc + rung sàn xe
    "night_bus": ("động cơ xe khách đêm + đường cao tốc (夜行バス車内)", [
        (f"aevalsrc=exprs='0.28*sin(2*PI*90*t)+0.16*sin(2*PI*180*t)"
         f"+0.09*sin(2*PI*45*t)':d={D}:s=48000", "lowpass=f=700,volume=0.85"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.60:seed=151",
         "bandpass=f=750:t=h:w=1000,volume='0.42+0.08*sin(2*PI*t/16)':eval=frame"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.42:seed=157", "lowpass=f=170,volume=0.30"),
    ]),
    # sảnh ga/bến xe sớm mai: vọng âm rộng + tiếng người xa xăm + nền yên tĩnh
    "terminal_hall": ("sảnh ga/bến xe sớm mai, vọng âm rộng (到着ターミナル)", [
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.55:seed=163",
         "bandpass=f=900:t=h:w=1400,volume='0.40+0.12*sin(2*PI*t/32)':eval=frame"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.32:seed=167",
         "bandpass=f=350:t=h:w=500,volume=0.22"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.35:seed=173", "lowpass=f=160,volume=0.24"),
    ]),
    # văn phòng / phòng họp: điều hòa + đèn (hài 240/360Hz nghe được trên loa nhỏ)
    "office_hum": ("văn phòng, phòng họp 理事会 (điều hòa + đèn)", [
        (f"aevalsrc=exprs='0.26*sin(2*PI*240*t)+0.15*sin(2*PI*360*t)"
         f"+0.08*sin(2*PI*120*t)':d={D}:s=48000", "lowpass=f=800,volume=0.85"),
        (f"anoisesrc=c=pink:r=48000:d={D}:a=0.58:seed=131",
         "bandpass=f=1100:t=h:w=1400,volume=0.35"),
        (f"anoisesrc=c=brown:r=48000:d={D}:a=0.38:seed=127", "lowpass=f=180,volume=0.26"),
    ]),
}


def build(name, layers):
    """Mix các layer mono → làm rộng stereo (Haas 13ms) → chuẩn hóa loudness."""
    srcs, parts, mix = [], [], ""
    for i, (src, post) in enumerate(layers):
        srcs += ["-f", "lavfi", "-i", src]
        parts.append(f"[{i}:a]{post}[L{i}]")
        mix += f"[L{i}]"
    parts.append(f"{mix}amix=inputs={len(layers)}:normalize=0[m]")
    # pseudo-stereo: kênh phải trễ 13ms → rộng ra mà không lệch pha nghe được
    parts.append("[m]asplit=2[ml][mr0];[mr0]adelay=13[mr]"
                 f";[ml][mr]join=inputs=2:channel_layout=stereo,{LOUD},"
                 "alimiter=limit=0.9,aformat=sample_fmts=s16[a]")
    f = OUT / f"{name}.wav"
    cmd = ["ffmpeg", "-y"] + srcs + ["-filter_complex", ";".join(parts),
                                     "-map", "[a]", "-t", str(D), str(f), "-loglevel", "error"]
    return subprocess.run(cmd).returncode == 0, f


def mean_db(f, af=None):
    """mean_volume của file (tùy chọn lọc dải trước khi đo)."""
    chain = f"{af},volumedetect" if af else "volumedetect"
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f),
                        "-af", chain, "-f", "null", "-"],
                       capture_output=True, text=True, errors="replace")
    for line in p.stderr.splitlines():
        if "mean_volume" in line:
            return float(line.split(":")[1].replace("dB", "").strip())
    return -99.0


GAP_MAX = 25.0   # dải 200-600Hz không được thấp hơn full-band quá bấy nhiêu dB


def check():
    """GATE loa nhỏ: bed nào thân nằm hết dưới 250Hz thì khán giả nghe bằng điện thoại
    KHÔNG nghe được gì. Chạy sau mỗi lần sửa BANK."""
    print(f"{'bed':16s} {'full':>7s} {'200-600':>8s} {'gap':>6s}  {'':4s}")
    bad = []
    for f in sorted(OUT.glob("*.wav")):
        full = mean_db(f)
        mid = mean_db(f, "bandpass=f=400:t=h:w=400")
        gap = full - mid
        ok = gap <= GAP_MAX
        if not ok:
            bad.append((f.stem, round(gap, 1)))
        print(f"{f.stem:16s} {full:7.1f} {mid:8.1f} {gap:6.1f}  {'OK' if ok else '✗ FAIL'}")
    if bad:
        print(f"\n✗ {len(bad)} bed thiếu thân 250-1500Hz (gap > {GAP_MAX}dB): {bad}")
        print("  → tăng gain layer bandpass giữa, hạ gain layer lowpass sub-bass.")
        return 1
    print(f"\n✅ Tất cả bed đều có thân nghe được trên loa nhỏ (gap ≤ {GAP_MAX}dB).")
    return 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (desc, layers) in BANK.items():
        ok, f = build(name, layers)
        print(("OK   " if ok else "FAIL "), f"{name:16s} {desc}")
    print(f"→ {OUT}\n")
    return check()


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    sys.exit(main())
