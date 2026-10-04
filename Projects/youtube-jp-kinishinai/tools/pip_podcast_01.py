# -*- coding: utf-8 -*-
"""pip_podcast_01.py — ghep khung "nguoi ke o phong thu" (PiP) vao GOC PHAI video da render, KHOP NHIP giong doc.

Nhip lay tu timeline.json (moc tung dong cua chinh voice.wav):
  - dang doc (khe < GAP_TALK giua 2 dong gop thanh mot) -> doan NOI cua clip, ping-pong cho du dai
  - im lang >= GAP_TALK (tag [間], het doan)            -> doan LANG cua cung clip (cuoi / gat)
Chon clip theo TUNG SLIDE (doi clip dung luc doi hinh chinh = "chuyen may"):
  - cau co cam xuc ro -> clip dung cam xuc (cuoi -> C · hoi tuong/私 -> B · am ap/ket -> E)
  - con lai xoay vong A / D / E, khong 2 slide lien nhau cung clip
An PiP o slide THE CHU / CHU HIEN DAN (card, reveal) — chu cua the nam trong vung PiP.
Vi tri: phai, tren dai phu de (y 524-776; phu de 2 dong bat dau y~796), tranh goc duoi-phai (timestamp YouTube).
Clip nguon: cat ✦ 0,87W (clip Veo ✦ lech trai ~0,885W), keo len 30fps bang minterpolate.
Audio: copy giong + gioi han true peak <= -1 dBTP (alimiter level=disabled).
Chay: python tools/pip_podcast_01.py 01_kuchiguse-hitonome <in.mp4> <out.mp4> [--sheet]
"""
import sys, io, json, re, argparse, subprocess
from pathlib import Path
import numpy as np
import cv2

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
RAW = "_user_raw/zip_1001_1157"
W, H, FPS = 1920, 1080, 30
PW, PH = 440, 248                      # khung PiP 16:9
PX, PY = W - 40 - PW, 524              # goc tren-trai; day khung 776 < dinh phu de 2 dong (do: y 796)
RAD, BORDER = 18, 4
GAP_TALK = 0.9                         # khe ngan hon thi coi nhu van dang noi
XF = 8                                 # so frame hoa tron khi doi doan / doi clip / hien-an

# (file, (noi_a, noi_b), (lang_a, lang_b)) — chot bang MAT tren dai crop mieng 0,5s/khung
CLIPS = {
    "A": ("Woman_speaking_into_microphone_20261001120535_3.mp4", (0.4, 4.0), (4.6, 7.8)),   # 2 tay dat ban
    "B": ("Woman_speaking_into_microphone_20261001120535_2.mp4", (0.0, 4.0), (4.6, 7.8)),   # tay dat len nguc
    "C": ("Woman_smiling_and_shaking_head_20261001120535.mp4", (0.0, 1.0), (2.0, 7.8)),     # cuoi, lac dau
    "D": ("Woman_speaking_into_microphone_20261001120535.mp4", (0.0, 3.8), (0.0, 3.8)),     # chi noi (sau 4s can micro bien dang)
    "E": ("Woman_smiling_in_recording_room_20261001120535.mp4", (2.2, 7.8), (0.8, 1.8)),    # tay dan, vua noi vua cuoi
}
ROTATE = ["A", "D", "E"]
EMO = [  # (regex tren loi cua slide, clip) — kiem theo thu tu
    (r"笑|がっかり|照れ|楽しかった|大笑い", "C"),
    (r"私は|私が|私も|私の|三十四年|六十八", "B"),
    (r"ありがとう|ように|よかった|味方", "E"),
]


def load_clip(f):
    """Cat ✦ 0,87W + 16:9, thu ve PWxPH, minterpolate len 30fps -> mang frame BGR."""
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                    "stream=width,height", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout.strip().split(",")[:2])
    cw = int(w * 0.87) // 2 * 2; ch = round(cw * 9 / 16) // 2 * 2; cy = (h - ch) // 2
    vf = (f"crop={cw}:{ch}:0:{cy},scale={PW}:{PH}:flags=lanczos,"
          f"minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", vf, "-an", "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, PH, PW, 3)


def pingpong(t, a, b):
    L = b - a
    if L <= 0:
        return a
    k = t % (2 * L)
    return a + (k if k < L else 2 * L - k)


def plan(sl, lines, total):
    """-> list (t0, t1, clip|None, spans[(s0,s1,'talk'|'quiet')]) theo slide."""
    st = []
    for i, e in enumerate(sl):
        hit = next(ln for ln in lines if e["match"] in ln["text"])
        st.append((hit["start"] + float(e.get("offset", 0.0)), i))
    st.sort(); st[0] = (0.0, st[0][1])
    out, prev = [], None
    for k, (t0, i) in enumerate(st):
        t1 = st[k + 1][0] if k + 1 < len(st) else total
        e = sl[i]
        if e.get("card") or e.get("reveal"):
            out.append((t0, t1, None, [], "")); prev = None; continue
        txt = "".join(ln["text"] for ln in lines if t0 - 0.05 <= ln["start"] < t1 - 0.05)
        clip = next((c for rx, c in EMO if re.search(rx, txt)), None)
        if clip is None or clip == prev:
            pool = [c for c in ROTATE if c != prev]
            clip = pool[len(out) % len(pool)]
        # cac khoang dang doc trong slide
        talk = []
        for ln in lines:
            a, b = max(ln["start"], t0), min(ln["end"], t1)
            if b <= a:
                continue
            if talk and a - talk[-1][1] < GAP_TALK:
                talk[-1][1] = b
            else:
                talk.append([a, b])
        spans, cur = [], t0
        for a, b in talk:
            if a - cur >= GAP_TALK:
                spans.append((cur, a, "quiet"))
            elif spans:
                a = cur
            else:
                a = cur
            spans.append((a, b, "talk")); cur = b
        if t1 - cur > 0.01:
            spans.append((cur, t1, "quiet" if t1 - cur >= GAP_TALK or not spans else spans[-1][2]))
        out.append((t0, t1, clip, spans, txt[:30])); prev = clip
    return out


def round_mask():
    m = np.zeros((PH + 2 * BORDER, PW + 2 * BORDER), np.uint8)
    r = RAD + BORDER
    cv2.rectangle(m, (r, 0), (m.shape[1] - r, m.shape[0]), 255, -1)
    cv2.rectangle(m, (0, r), (m.shape[1], m.shape[0] - r), 255, -1)
    for cx, cy in ((r, r), (m.shape[1] - r - 1, r), (r, m.shape[0] - r - 1), (m.shape[1] - r - 1, m.shape[0] - r - 1)):
        cv2.circle(m, (cx, cy), r, 255, -1)
    return cv2.GaussianBlur(m, (3, 3), 0).astype(np.float32) / 255


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--sheet", action="store_true", help="chi in ke hoach + anh duyet, khong encode")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    sl = json.loads((PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json").read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    P = plan(sl, tl["lines"], tl["total"])
    shown = [p for p in P if p[2]]
    from collections import Counter
    print(f"{len(P)} slide · PiP hien o {len(shown)} · an o {len(P) - len(shown)} (the chu)")
    print("dung clip:", dict(Counter(p[2] for p in shown)))
    for t0, t1, c, sp, txt in P[:14]:
        print(f"  {t0:7.1f}-{t1:7.1f} {c or '-'}  {' '.join(f'{k[0]}{s1 - s0:.1f}' for s0, s1, k in sp)}  {txt}")

    frames = {k: load_clip(vd / RAW / f) for k, (f, _, _) in CLIPS.items()}
    print("da nap clip:", {k: len(v) for k, v in frames.items()})
    n = int(round(tl["total"] * FPS)) + 1
    # moi frame output: (clip, so frame nguon) hoac None
    src = [None] * n
    for t0, t1, c, sp, _ in P:
        if not c:
            continue
        _, talk_r, quiet_r = CLIPS[c]
        for s0, s1, kind in sp:
            ra, rb = talk_r if kind == "talk" else quiet_r
            for fi in range(int(round(s0 * FPS)), min(int(round(s1 * FPS)), n)):
                t = (fi / FPS - s0)
                src[fi] = (c, min(int(round(pingpong(t, ra, rb) * FPS)), len(frames[c]) - 1))
    mask = round_mask()
    shadow = cv2.GaussianBlur(np.pad(mask, 14), (0, 0), 9) * 0.45
    BX, BY = PX - BORDER, PY - BORDER

    def pip_img(s):
        c, k = s
        box = np.full((PH + 2 * BORDER, PW + 2 * BORDER, 3), 255, np.uint8)
        box[BORDER:BORDER + PH, BORDER:BORDER + PW] = frames[c][k]
        return box.astype(np.float32)

    def alpha_at(fi):
        """do hien cua PiP (fade XF frame o bien hien/an)."""
        on = src[fi] is not None
        if not on:
            return 0.0
        d = 0
        while d < XF and fi - d - 1 >= 0 and src[fi - d - 1] is not None:
            d += 1
        e = 0
        while e < XF and fi + e + 1 < n and src[fi + e + 1] is not None:
            e += 1
        return min(1.0, (d + 1) / XF, (e + 1) / XF)

    if a.sheet:
        ts = [p[0] + 2 for p in shown[:16]]
        cells = []
        for t in ts:
            fi = int(t * FPS)
            fr = np.full((H, W, 3), 90, np.uint8).astype(np.float32)
            comp(fr, pip_img(src[fi]), 1.0, mask, shadow, BX, BY)
            cells.append(cv2.resize(fr.astype(np.uint8), (480, 270)))
        rows = [np.hstack(cells[i:i + 4]) for i in range(0, len(cells) - 3, 4)]
        cv2.imwrite(str(vd / "_plan" / "_pip_sheet.jpg"), np.vstack(rows))
        return

    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-i", a.inp, "-map", "0:v", "-map", "1:a",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-af", "alimiter=limit=0.84:level=disabled:attack=1:release=50",
                            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
    fsz = W * H * 3
    prev_s, prev_img, blend_left, old_img = None, None, 0, None
    fi = 0
    while True:
        buf = dec.stdout.read(fsz)
        if len(buf) < fsz:
            break
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        s = src[fi] if fi < n else None
        al = alpha_at(fi) if fi < n else 0.0
        if s is not None and al > 0:
            img = pip_img(s)
            # doi clip / doi doan noi<->lang = nhay frame -> hoa tron XF frame
            if prev_s is not None and (s[0] != prev_s[0] or abs(s[1] - prev_s[1]) > 2):
                blend_left, old_img = XF, prev_img
            if blend_left and old_img is not None:
                w_ = blend_left / (XF + 1)
                img = img * (1 - w_) + old_img * w_
                blend_left -= 1
            f2 = fr.astype(np.float32)
            comp(f2, img, al, mask, shadow, BX, BY)
            fr = f2.astype(np.uint8)
            prev_s, prev_img = s, img
        else:
            prev_s, prev_img = None, None
        enc.stdin.write(fr.tobytes())
        fi += 1
        if fi % 3000 == 0:
            print(f"  {fi}/{n} frame", flush=True)
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"OK {fi} frame -> {a.out} (exit {enc.returncode})")
    sys.exit(enc.returncode)


def comp(fr, img, al, mask, shadow, BX, BY):
    hh, ww = mask.shape
    sh = shadow[:, :, None] * al
    y0, x0 = BY - 14 + 6, BX - 14 + 4
    reg = fr[y0:y0 + sh.shape[0], x0:x0 + sh.shape[1]]
    reg *= (1 - sh[:reg.shape[0], :reg.shape[1]])
    m = mask[:, :, None] * al
    reg = fr[BY:BY + hh, BX:BX + ww]
    reg[:] = reg * (1 - m) + img * m


if __name__ == "__main__":
    main()
