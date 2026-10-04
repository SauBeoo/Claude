# -*- coding: utf-8 -*-
"""post_03_sfx.py — ghep SFX that (pocket-se.info) vao 3 clip phim tu lieu that cua
video 03 (kieta-kyoshitsu). cut_archival.py da MUTE toan bo clip (-an, dung luat:
tieng/nhac goc la quyen rieng) -> khong duoc de cam lang, phai ghep SFX THAT khop
dung canh, theo CLAUDE.md muc "MOI CLIP PHIM TU LIEU THAT PHAI DUOC GHEP SFX".

- Doc timestamp tu subs.srt (tim dong khop dung cau dau cua tung clip).
- -map 0:v -c:v copy giu nguyen hinh, chi re-encode audio.
- Nguon: pocket-se.info (kiem tien OK, cat/sua OK, BAT BUOC credit).
"""
import re, subprocess, sys
from pathlib import Path

VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\03_kieta-kyoshitsu")
SFX = VD / "_sfx"
SRC = VD / "03_kieta-kyoshitsu.mp4"
OUT = VD / "03_kieta-kyoshitsu_SFX.mp4"


def srt_time(text_frag):
    """Tim thoi diem bat dau (giay) cua dong phu de chua text_frag."""
    srt = (VD / "subs.srt").read_text(encoding="utf-8")
    blocks = srt.split("\n\n")
    for b in blocks:
        if text_frag in b:
            m = re.search(r"(\d\d):(\d\d):(\d\d),(\d\d\d)", b)
            h, mi, s, ms = map(int, m.groups())
            return h * 3600 + mi * 60 + s + ms / 1000
    raise SystemExit(f"[LOI] khong tim thay dong chua: {text_frag}")


def main():
    if not SRC.exists():
        raise SystemExit(f"[LOI] chua co video goc: {SRC}")

    # clip0 DA THAY 2026-08-22: ke giay dep truong hoc rong (khong con canh di choi
    # ngoai troi) -> doi SFX theo: cach ung dung "kacha" + day cua mo "gicho"
    # (khop dung "hitori de kagi wo akete hairimasu" - mo khoa vao mot minh)
    t0 = srt_time("朝の、七時。")                     # clip 0 - ke giay dep rong (cold open)
    t2 = srt_time("今日は、昭和の教室から消えた道具")   # clip 2 - toan canh lop hoc
    t3 = srt_time("さあ、いくつ、あなたの記憶に")        # clip 3 - can canh viet

    d0, d2, d3 = round(t0 * 1000), round(t2 * 1000), round(t3 * 1000)
    print(f"clip0 @ {t0:.2f}s | clip2 @ {t2:.2f}s | clip3 @ {t3:.2f}s")

    # 🔴 BOOST 2026-08-22 (user: "tieng that cua tao dau" - lan truoc volume=0.30/0.35
    # qua nho, do RMS chi tang ~0.1-0.14dB, gan nhu khong nghe duoc). Do lai bang
    # volumedetect: nguon SFX mean -20..-28dB trong khi video goc (voice+BGM) mean
    # -17.5dB. NHUNG lan boost dau tien (+8..+14dB) lam CLIP: keyopen/dooropen6 da
    # co max_volume rieng -0.5/0.0dB (gan full-scale) -> cong them dB la vuot 0dBFS
    # that su (do lai: Peak level dB +7.0 = clip). Sua: gain theo dung HEADROOM con
    # lai cua tung file, khong boost mu quang; keyopen/dooropen gan nhu khong can
    # boost vi ban than da to (transient tu nhien xuyen qua nen -17dB); chi write.mp3
    # (nen -6dB) moi con cho de +4dB. Them alimiter cuoi chuoi lam luoi an toan.
    fc = (
        # key + door: 2 tieng ngan (0.5s + 0.95s) - GIU NGUYEN gain (da gan full-scale)
        f"[1:a]adelay={d0}|{d0},volume=0dB[sfx_key];"
        f"[2:a]adelay={d0+400}|{d0+400},volume=-1dB[sfx_door];"
        # but/viet chi tren giay, lap 3 lan de phu du 2 canh lop hoc (~7.5s moi canh)
        f"[3:a]aloop=loop=2:size=999999,atrim=0:7.5,afade=t=out:st=6.5:d=1.0,"
        f"adelay={d2}|{d2},volume=4dB[sfx2];"
        f"[3:a]aloop=loop=2:size=999999,atrim=0:7.5,afade=t=out:st=6.5:d=1.0,"
        f"adelay={d3}|{d3},volume=4dB[sfx3];"
        f"[0:a][sfx_key][sfx_door][sfx2][sfx3]amix=inputs=5:duration=first:normalize=0,"
        f"alimiter=limit=0.97[aout]"
    )

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", str(SRC),
        "-i", str(SFX / "keyopen.mp3"),
        "-i", str(SFX / "dooropen6.mp3"),
        "-i", str(SFX / "write.mp3"),
        "-filter_complex", fc,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(OUT),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("[LOI ffmpeg]", r.stderr[-2000:])
        sys.exit(1)
    mb = OUT.stat().st_size / 1e6
    print(f"OK -> {OUT.name} ({mb:.0f} MB)")


if __name__ == "__main__":
    main()
