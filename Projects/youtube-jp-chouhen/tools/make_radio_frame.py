# -*- coding: utf-8 -*-
"""make_radio_frame.py — bộ khung "phòng thu đêm khuya" (radio frame) cho 真夜中の朗読便.

Học từ format đối thủ (video uWTUB9BIWfk, user đưa 2026-08-20): hàng trên = typing-cam
+ player UI + avatar tròn, nền mood phủ toàn khung, phụ đề chữ to hạ 1/3.

Sinh 3 loại asset MỘT LẦN (dùng lại mọi video — chúng là bản sắc kênh, như logo):
  player_ui.png   — UI máy phát: thanh tiến trình + nút play/pause/skip + loa (nền trong suốt).
                    ⚠️ KHÔNG chứa cột sóng — sóng do ffmpeg showfreqs sinh THẬT từ voice.wav
                    lúc render (xem cmd_demo để biết vị trí đặt).
  avatar.png      — ảnh persona crop TRÒN + viền kem 6px (nền trong suốt).
  demo frame      — 1 frame 1920×1080 hoàn chỉnh để duyệt mắt trước khi vá scene_render.

CHẠY:
  python tools/make_radio_frame.py assets                 # sinh player_ui.png + avatar.png
  python tools/make_radio_frame.py demo                   # dựng 2 demo frame (sub outline / sub box)
Assets nằm ở 06_VIDEO/_radio_frame/.

Layout 1920×1080 (scale 1.5x từ bản mẫu 1280×720):
  typing-cam : (0, 0)      705×352   — clip loop, đè thẳng góc trái-trên
  player UI  : x 830–1425, y 30–330  — vẽ lên nền, không hộp
  waveform   : x 855–1400, y 45–175  — vùng showfreqs (demo vẽ bars giả)
  avatar     : tâm (1725, 172) Ø 330
  subtitle   : căn giữa, đáy ~y 960, cỡ 72, 2 dòng
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

PROJ = Path(__file__).resolve().parent.parent
OUT = PROJ / "06_VIDEO" / "_radio_frame"
W, H = 1920, 1080

# vùng layout (đổi số ở đây là đổi mọi video sau)
CAM_W, CAM_H = 705, 352
PLAYER = (830, 30, 1425, 330)          # x0 y0 x1 y1
WAVE = (855, 45, 1400, 175)            # vùng cột sóng (showfreqs đặt vào đây khi render thật)
AV_CX, AV_CY, AV_D = 1725, 172, 330
CREAM = (238, 233, 220, 255)
FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"


def draw_player_ui() -> Image.Image:
    """UI máy phát trong suốt: thanh tiến trình + 5 nút. Không waveform (ffmpeg lo)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = PLAYER

    # thanh tiến trình — vệt sáng đã chạy 1/3
    bar_y = 205
    d.rounded_rectangle([x0 + 25, bar_y - 3, x1 - 25, bar_y + 3], 3, fill=(255, 255, 255, 235))
    d.ellipse([x0 + 25 + 180 - 9, bar_y - 9, x0 + 25 + 180 + 9, bar_y + 9], fill=(255, 255, 255, 255))

    # hàng nút: loa · prev · play(pause) · next · mute — tâm y 275
    cy = 275
    cx_mid = (x0 + x1) // 2

    # nút play/pause: đĩa tròn trắng + 2 vạch pause navy
    r = 34
    d.ellipse([cx_mid - r, cy - r, cx_mid + r, cy + r], fill=(255, 255, 255, 245))
    for dx in (-9, 5):
        d.rounded_rectangle([cx_mid + dx, cy - 14, cx_mid + dx + 5, cy + 14], 2, fill=(30, 34, 60, 255))

    wh = (255, 255, 255, 235)

    def tri(cx, cy2, s, flip=False):
        pts = [(cx - s, cy2 - s), (cx - s, cy2 + s), (cx + s, cy2)]
        if flip:
            pts = [(cx + s, cy2 - s), (cx + s, cy2 + s), (cx - s, cy2)]
        d.polygon(pts, fill=wh)

    # prev |◀  — vạch + tam giác trái
    px = cx_mid - 120
    tri(px + 6, cy, 14, flip=True)
    d.rounded_rectangle([px - 16, cy - 14, px - 10, cy + 14], 2, fill=wh)
    # next ▶| — tam giác phải + vạch
    nx = cx_mid + 120
    tri(nx - 6, cy, 14)
    d.rounded_rectangle([nx + 10, cy - 14, nx + 16, cy + 14], 2, fill=wh)

    def speaker(cx, cy2, muted=False):
        d.polygon([(cx - 16, cy2 - 6), (cx - 8, cy2 - 6), (cx + 2, cy2 - 15),
                   (cx + 2, cy2 + 15), (cx - 8, cy2 + 6), (cx - 16, cy2 + 6)], fill=wh)
        if muted:
            d.line([cx + 8, cy2 - 9, cx + 20, cy2 + 9], fill=wh, width=4)
            d.line([cx + 8, cy2 + 9, cx + 20, cy2 - 9], fill=wh, width=4)
        else:
            d.arc([cx + 4, cy2 - 12, cx + 26, cy2 + 12], -55, 55, fill=wh, width=4)

    speaker(cx_mid - 215, cy)
    speaker(cx_mid + 215, cy, muted=True)
    return img


def demo_wavebars(d: ImageDraw.ImageDraw):
    """Cột sóng GIẢ chỉ cho demo frame — bản render thật dùng ffmpeg showfreqs từ voice.wav."""
    import random
    random.seed(7)
    x0, y0, x1, y1 = WAVE
    cy = (y0 + y1) // 2
    n = 34
    step = (x1 - x0) / n
    for i in range(n):
        h2 = random.randint(14, (y1 - y0) // 2)
        x = x0 + i * step
        d.rounded_rectangle([x, cy - h2, x + step * 0.45, cy + h2], 4, fill=(255, 255, 255, 235))


def make_avatar(src: Path) -> Image.Image:
    """Crop tròn + viền kem. Lấy phần trên-giữa ảnh (mặt)."""
    im = Image.open(src).convert("RGB")
    side = min(im.width, int(im.height * 0.62))
    left = (im.width - side) // 2
    top = int(im.height * 0.06)
    im = im.crop((left, top, left + side, top + side)).resize((AV_D, AV_D), Image.LANCZOS)

    mask = Image.new("L", (AV_D * 4, AV_D * 4), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, AV_D * 4 - 1, AV_D * 4 - 1], fill=255)
    mask = mask.resize((AV_D, AV_D), Image.LANCZOS)

    out = Image.new("RGBA", (AV_D, AV_D), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    ring = ImageDraw.Draw(out)
    ring.ellipse([3, 3, AV_D - 4, AV_D - 4], outline=CREAM, width=6)
    return out


def draw_sub(base: Image.Image, lines: list[str], style: str):
    """style: 'outline' (chữ trần viền đen dày — luật 45+ §3.1) | 'box' (hộp tối mờ kiểu đối thủ)."""
    font = ImageFont.truetype(FONT_BOLD, 72)
    d = ImageDraw.Draw(base, "RGBA")
    line_h = 96
    total_h = line_h * len(lines)
    y_start = 960 - total_h

    if style == "box":
        wmax = max(d.textlength(t, font=font) for t in lines)
        pad = 38
        x0 = (W - wmax) / 2 - pad
        d.rounded_rectangle([x0, y_start - 18, x0 + wmax + pad * 2, y_start + total_h + 14],
                            22, fill=(10, 12, 20, 175))

    fill = (72, 170, 255, 255)
    for i, t in enumerate(lines):
        tw = d.textlength(t, font=font)
        x = (W - tw) / 2
        y = y_start + i * line_h
        d.text((x, y), t, font=font, fill=fill, stroke_width=7,
               stroke_fill=(255, 255, 255, 255) if style == "box" else (12, 12, 16, 255))


def cmd_assets():
    OUT.mkdir(exist_ok=True)
    draw_player_ui().save(OUT / "player_ui.png")
    av_src = OUT / "av_31169640.jpg"
    av = make_avatar(av_src)
    av.save(OUT / "avatar.png")

    # frame_static.png = player UI + avatar + viền vùng cam, gộp MỘT lớp RGBA 1920×1080
    # → renderer chỉ cần 1 input + 1 overlay (eof_action=repeat) cho toàn bộ phần tĩnh.
    stat = draw_player_ui()
    stat.paste(av, (AV_CX - AV_D // 2, AV_CY - AV_D // 2), av)
    ImageDraw.Draw(stat).rectangle([0, 0, CAM_W - 1, CAM_H - 1],
                                   outline=(238, 233, 220, 120), width=2)
    stat.save(OUT / "frame_static.png")

    # chuẩn hoá tên clip typing để renderer không hardcode id Pexels
    src = OUT / "typing_27601321.mp4"
    dst = OUT / "typing_loop.mp4"
    if src.exists() and not dst.exists():
        import shutil
        shutil.copy2(src, dst)
    print("OK ->", OUT / "frame_static.png", "|", OUT / "avatar.png", "|", dst)


def cmd_demo():
    bg = Image.open(OUT / "bg_demo.jpg").convert("RGB").resize((W, H), Image.LANCZOS)
    # phủ tối nhẹ như scene_render vẫn làm, để chữ với UI trắng nổi
    veil = Image.new("RGBA", (W, H), (8, 10, 18, 70))
    base0 = Image.alpha_composite(bg.convert("RGBA"), veil)

    cam = Image.open(OUT / "typing_demo.jpg").convert("RGB")
    cam = cam.resize((CAM_W, int(cam.height * CAM_W / cam.width)), Image.LANCZOS)
    cam = cam.crop((0, (cam.height - CAM_H) // 2, CAM_W, (cam.height - CAM_H) // 2 + CAM_H))

    ui = Image.open(OUT / "player_ui.png")
    av = Image.open(OUT / "avatar.png")

    line_sets = ["「離婚して契約社員に成り下がった女が、", "よくこの会に面を出せたな」"]
    for style in ("outline", "box"):
        fr = base0.copy()
        fr.paste(cam, (0, 0))
        # viền mảnh quanh cam cho gọn
        ImageDraw.Draw(fr).rectangle([0, 0, CAM_W - 1, CAM_H - 1], outline=(238, 233, 220, 120), width=2)
        fr = Image.alpha_composite(fr, ui)
        demo_wavebars(ImageDraw.Draw(fr, "RGBA"))
        fr.paste(av, (AV_CX - AV_D // 2, AV_CY - AV_D // 2), av)
        draw_sub(fr, line_sets, style)
        p = OUT / f"demo_frame_{style}.png"
        fr.convert("RGB").save(p)
        print("OK ->", p)


def cmd_wave(voice_path: str, out_path: str):
    """Vẽ wave.mp4 (544×130, bars trắng nền đen) từ biên độ THẬT của voice.wav bằng PIL.

    ⛔ Đừng quay lại ffmpeg showfreqs: nó leak RAM vô hạn với voice.wav của kênh
    (đo 2026-08-20: 2,3–7 GB rồi 'Cannot allocate memory' — cả khi đứng một mình).
    Bars = RMS cửa sổ trượt quanh thời điểm hiện tại → sóng chạy phải→trái theo giọng."""
    import shutil
    import subprocess
    import tempfile
    import wave as wavmod

    import numpy as np

    W_, H_ = 544, 130
    NBAR, FPS_ = 34, 30
    with wavmod.open(voice_path, "rb") as wf:
        sr, nch = wf.getframerate(), wf.getnchannels()
        raw = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    if nch > 1:
        raw = raw.reshape(-1, nch).mean(axis=1)
    x = raw.astype(np.float32) / 32768.0
    dur = len(x) / sr
    n_frames = int(dur * FPS_)

    # RMS theo lưới 60Hz (mỗi bar cách nhau 1 ô lưới → sóng trôi mượt)
    hop = sr // 60
    n_cells = len(x) // hop
    rms = np.sqrt(np.mean(x[: n_cells * hop].reshape(-1, hop) ** 2, axis=1))
    rms = rms / (np.percentile(rms, 98) + 1e-9)          # chuẩn hoá theo giọng của video
    rms = np.clip(rms, 0.04, 1.0)                        # sàn nhỏ: im lặng vẫn còn vạch

    step = W_ / NBAR
    bw = max(2, int(step * 0.45))
    tmp = Path(tempfile.mkdtemp(prefix="wave_"))
    for f in range(n_frames):
        img = Image.new("RGB", (W_, H_), (0, 0, 0))
        d = ImageDraw.Draw(img)
        cell0 = int(f * 2)                               # 60 cell/s ÷ 30 fps = 2 cell/frame
        for i in range(NBAR):
            c = cell0 + (i - NBAR // 2) * 2              # bar i = RMS quanh hiện tại
            v = rms[c] if 0 <= c < len(rms) else 0.04
            h2 = max(3, int(v * (H_ // 2 - 4)))
            xx = int(i * step)
            d.rounded_rectangle([xx, H_ // 2 - h2, xx + bw, H_ // 2 + h2], 3,
                                fill=(255, 255, 255))
        img.save(tmp / f"w_{f:05d}.png")
    r = subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS_),
                        "-i", str(tmp / "w_%05d.png"),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                        "-pix_fmt", "yuv420p", out_path, "-loglevel", "error"])
    shutil.rmtree(tmp, ignore_errors=True)
    if r.returncode != 0:
        sys.exit("[LỖI] ffmpeg ghép wave PNG fail")
    print(f"OK -> {out_path} ({n_frames} frame, {dur:.1f}s)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "assets":
        cmd_assets()
    elif cmd == "demo":
        cmd_assets()
        cmd_demo()
    elif cmd == "wave":
        cmd_wave(sys.argv[2], sys.argv[3])
    else:
        sys.exit("assets | demo | wave <voice.wav> <out.mp4>")
