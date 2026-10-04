# -*- coding: utf-8 -*-
"""Đo tương quan: thời lượng render thật = ký/tốc-độ-đọc + tổng giây im lặng khai bằng tag."""
import io, re, os

ROOT = r"E:\Claude\Projects\youtube-jp-chouhen"


def stat(p):
    t = io.open(p, encoding="utf-8").read()
    lines = [l for l in t.split("\n") if l.strip() and not l.lstrip().startswith("#")]
    chars = sum(len(re.sub(r"\[[^\]]+\]", "", l)) for l in lines)
    pause = 0.0
    ntag = 0
    for tg in re.findall(r"\[([^\]]+)\]", t):
        for k, v in re.findall(r"(後間|間|速|抑揚|高|音量)([0-9.+-]*)", tg):
            ntag += 1
            if k in ("間", "後間") and v:
                try:
                    pause += float(v)
                except ValueError:
                    pass
    return chars, ntag, pause, len(lines)


cases = [
    ("21", r"07_UPLOADED\21_hachinen-no-yachin\_scripts\21_hachinen-no-yachin_TTS.md", 35 * 60 + 6),
    ("22", r"07_UPLOADED\22_tanin-no-hanko\_scripts\22_tanin-no-hanko_TTS.md", 36 * 60 + 1),
    ("23", r"07_UPLOADED\23_gakushi-hoken\_scripts\23_gakushi-hoken_TTS.md", 59 * 60 + 22),
    ("25", r"07_UPLOADED\25_shinya-no-genkan\_scripts\25_shinya-no-genkan_TTS.md", 57 * 60 + 25),
    ("26", r"07_UPLOADED\26_ginkonshiki-mukyuu\_scripts\26_ginkonshiki-mukyuu_TTS.md", 43 * 60 + 19),
    # 🔴 27 = ĐIỂM DỮ LIỆU ĐỘC LẬP ĐẦU TIÊN (đo 2026-08-16, ffprobe voice.wav = 3176,4 s).
    #    Mô hình fit trên 5 video TRÊN ước 50′47 → lệch −4,1%. Trong khi trên chính 5 video
    #    đã fit nó chỉ lệch −2,5%…+0,9%. ⇒ "<1%" là sai số HUẤN LUYỆN, không phải sai số dự báo:
    #    5 điểm dữ liệu cho 3 tham số thì fit khít là đương nhiên. **Coi tool này là ±4%.**
    #    Giả thuyết đã BÁC BỎ: tỉ lệ section-gap/gap (tách 4 biến vẫn lệch −3,0% ở 27).
    ("27", r"03_SCRIPTS\27_boshi-no-namae_TTS.md", 3176),
]

print("%-4s %6s %5s %5s %8s %7s %8s %9s %8s" % (
    "vid", "ky", "tag", "nhip", "pause_s", "that_s", "ky/phut", "conlai_s", "ky/s"))
rows = []
for name, rel, dur in cases:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print(name, "THIEU FILE", p)
        continue
    c, n, pa, nl = stat(p)
    rest = dur - pa
    rows.append((name, c, n, pa, dur, rest, nl))
    print("%-4s %6d %5d %5d %8.1f %7d %8.1f %9.1f %8.2f" % (
        name, c, n, nl, pa, dur, c / (dur / 60.0), rest, c / rest))

# fit tuyến tính: dur = a*chars + b*pause + c*nhip  (gap giữa dòng)
try:
    import numpy as np
    A = np.array([[c, pa, nl] for _, c, _, pa, _, _, nl in rows], dtype=float)
    y = np.array([d for _, _, _, _, d, _, _ in rows], dtype=float)
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    a, b, cc = sol
    print("\nFIT  dur = %.5f*ky + %.3f*pause_s + %.4f*nhip" % (a, b, cc))
    print("  -> toc do doc thuan: %.1f ky/phut" % (60.0 / a))
    print("  -> he so pause: %.2f  | gap moi nhip: %.3f s" % (b, cc))
    for (name, c, n, pa, d, r, nl), pred in zip(rows, A.dot(sol)):
        print("  %s: that %ds | fit %.0fs | lech %+.1f%%" % (name, d, pred, (pred - d) / d * 100))
    # ap cho video 27
    p27 = os.path.join(ROOT, r"03_SCRIPTS\27_boshi-no-namae_TTS.md")
    c, n, pa, nl = stat(p27)
    est = a * c + b * pa + cc * nl
    print("\n27: %d ky | %d tag | pause %.1fs | %d nhip" % (c, n, pa, nl))
    print("   UOC do dai = %.0f s = %d:%02d" % (est, int(est // 60), int(est % 60)))
except ImportError:
    print("\n(khong co numpy - bo qua buoc fit)")
