# -*- coding: utf-8 -*-
"""
animate_still.py — HOA DONG mot ANH TINH thanh clip, MA KHONG DI CHUYEN KHUNG.

Vi sao ton tai (do 2026-09-08 tren 3 video 191K-232K view cua nganh 昭和):
  · Ca 3 video deu la ANH TINH 100% — 0 pan, 0 zoom, 0 clip dong. MAD vung anh
    1,2-2,8 (chi nhieu nen); 34-44% frame Y HET frame truoc.
  · Chung giu MOT anh trung vi 15,8-18,0 giay (max 47-49s), 55-68% anh giu >10s.
  ⇒ Anh tinh la du de an 200K view. Nhung giu 16 giay mot anh CHET CUNG thi
    tang duoc: them chuyen dong CUC BO -> vua giu duoc bo cuc, vua het "dung hinh".

🔴 RANG BUOC CUNG: **KHUNG KHONG DI CHUYEN.** Khong Ken Burns, khong zoompan.
   User da bat loi "slide rung rung" (memory feedback_video_no_motion_mot_giong).
   Moi hieu ung o day la CUC BO (trong mot vung co mat na) hoac lop PHIM (grain/
   flicker/vignette) — tam anh dung yen, chi vai thu BEN TRONG no dong.

Dung:
  python animate_still.py anh.png --out clip.mp4 --dur 16 --preset kitchen
  python animate_still.py anh.png --out clip.mp4 --dur 16 --spec spec.json --sheet
  python animate_still.py --list-presets

Spec JSON:
{
 "film": {"grain":0.9,"flicker":0.012,"dust":0.6,"scratch":0.25,"vig":0.03},
 "fx": [ {"t":"steam","box":[0.40,0.35,0.62,0.66],"amp":0.55,"speed":0.35},
         {"t":"glow","ell":[0.14,0.12,0.07,0.09],"amp":0.20,"hz":0.6},
         {"t":"sway","box":[0.0,0.0,0.22,1.0],"amp":1.8,"hz":0.22},
         {"t":"ripple","box":[0.25,0.72,0.95,1.0],"amp":1.4,"hz":0.5} ] }
Toa do la TI LE 0..1: box=[x0,y0,x1,y1] · ell=[cx,cy,rx,ry].
"""
import argparse, io, json, os, subprocess, sys
import numpy as np
import cv2

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ============================================================ PRESET
# Moi preset = mot LOAI CANH cua nganh 昭和. Toa do mac dinh nham vao cho hay co
# nguon chuyen dong that trong canh do; sua box neu anh khac.
PRESETS = {
    "kitchen":  {"film": {"grain": .9, "flicker": .012, "dust": .5, "scratch": .2, "vig": .03},
                 "fx": [{"t": "steam",  "box": [.34, .30, .66, .70], "amp": .55, "speed": .35},
                        {"t": "glow",   "ell": [.50, .10, .16, .12], "amp": .14, "hz": .5},
                        {"t": "shimmer","box": [.30, .55, .70, .85], "amp": .6}]},
    "tatami":   {"film": {"grain": .8, "flicker": .014, "dust": .5, "scratch": .2, "vig": .04},
                 "fx": [{"t": "glow",   "ell": [.50, .08, .14, .10], "amp": .22, "hz": .35},
                        {"t": "sway",   "box": [.00, .00, .22, 1.0], "amp": 1.6, "hz": .20},
                        {"t": "dustbeam","box": [.25, .10, .80, .75], "amp": .45}]},
    "street":   {"film": {"grain": 1.0, "flicker": .010, "dust": .7, "scratch": .3, "vig": .03},
                 "fx": [{"t": "sway",   "box": [.00, .35, 1.0, .80], "amp": 1.2, "hz": .30},
                        {"t": "shimmer","box": [.10, .60, .95, 1.0], "amp": .8},
                        {"t": "dustbeam","box": [.20, .05, .90, .60], "amp": .35}]},
    "night":    {"film": {"grain": 1.1, "flicker": .022, "dust": .5, "scratch": .25, "vig": .06},
                 "fx": [{"t": "glow",   "ell": [.50, .18, .18, .16], "amp": .30, "hz": .8},
                        {"t": "smoke",  "box": [.30, .40, .70, .95], "amp": .35, "speed": .22}]},
    "office":   {"film": {"grain": .8, "flicker": .010, "dust": .4, "scratch": .15, "vig": .03},
                 "fx": [{"t": "smoke",  "box": [.20, .05, .85, .60], "amp": .30, "speed": .18},
                        {"t": "dustbeam","box": [.15, .05, .90, .70], "amp": .40},
                        {"t": "glow",   "ell": [.50, .06, .22, .08], "amp": .10, "hz": .9}]},
    "water":    {"film": {"grain": .9, "flicker": .012, "dust": .5, "scratch": .2, "vig": .03},
                 "fx": [{"t": "ripple", "box": [.10, .55, .95, 1.0], "amp": 1.8, "hz": .55},
                        {"t": "shimmer","box": [.10, .45, .95, .70], "amp": .7}]},
    "flat":     {"film": {"grain": .7, "flicker": .008, "dust": .3, "scratch": .12, "vig": .02},
                 "fx": []},   # chi lop phim — cho anh khong co nguon chuyen dong nao
}

# ============================================================ NOISE
def _field(h, w, cell, seed):
    """Truong nhieu MEM (value noise): random tho -> blur -> phong to."""
    rs = np.random.RandomState(seed)
    small = rs.rand(max(2, h // cell), max(2, w // cell)).astype(np.float32)
    small = cv2.GaussianBlur(small, (0, 0), 1.2)
    f = cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC)
    f -= f.min()
    return f / max(f.max(), 1e-6)


def _scroll_field(h, w, cell, seed):
    """Truong cao GAP DOI de cuon theo chieu doc lien mach (mod h)."""
    f = _field(h * 2, w, cell, seed)
    return f


def _mask_box(h, w, box, feather):
    x0, y0, x1, y1 = box
    m = np.zeros((h, w), np.float32)
    m[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)] = 1.0
    k = max(3, int(feather * min(h, w)) | 1)
    return cv2.GaussianBlur(m, (k, k), 0)


def _mask_ell(h, w, ell, feather):
    cx, cy, rx, ry = ell
    m = np.zeros((h, w), np.float32)
    cv2.ellipse(m, (int(cx * w), int(cy * h)), (int(rx * w), int(ry * h)), 0, 0, 360, 1.0, -1)
    k = max(3, int(feather * min(h, w)) | 1)
    return cv2.GaussianBlur(m, (k, k), 0)


def _mask_of(fx, h, w):
    if "ell" in fx:  return _mask_ell(h, w, fx["ell"], fx.get("feather", .10))
    if "box" in fx:  return _mask_box(h, w, fx["box"], fx.get("feather", .06))
    return np.ones((h, w), np.float32)


# ============================================================ RENDER
def render(img, dur, fps, spec, out, sheet=False, crf=18, seed=7):
    H, W = img.shape[:2]
    n = int(round(dur * fps))
    film = spec.get("film", {})
    fxs = spec.get("fx", [])

    base = img.astype(np.float32)
    gy, gx = np.mgrid[0:H, 0:W].astype(np.float32)

    # chuan bi tung hieu ung MOT LAN (mat na + truong nhieu)
    prep = []
    for i, fx in enumerate(fxs):
        m = _mask_of(fx, H, W)
        d = {"fx": fx, "m": m, "m3": m[..., None]}
        t = fx["t"]
        if t in ("steam", "smoke"):
            d["f"] = _scroll_field(H, W, fx.get("cell", 26 if t == "steam" else 40), seed + i)
        if t == "dustbeam":
            rs = np.random.RandomState(seed + 100 + i)
            k = int(fx.get("n", 90))
            d["p"] = np.stack([rs.rand(k) * W, rs.rand(k) * H,
                               (rs.rand(k) * .6 + .4), rs.rand(k) * 6.28], 1)   # x,y,size,phase
        prep.append(d)

    # vignette co dinh (chi bien do dao dong theo t)
    vy = (np.linspace(-1, 1, H) ** 2)[:, None]
    vx = (np.linspace(-1, 1, W) ** 2)[None, :]
    vig = np.clip(1.0 - 0.55 * (vy + vx), 0, 1).astype(np.float32)

    ff = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
         "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)

    rs_g = np.random.RandomState(seed + 999)
    scr = []          # vet xuoc dang song: [x, tuoi_con_lai]
    keep = []
    for k in range(n):
        t = k / fps
        fr = base.copy()

        # ---------- hieu ung CUC BO ----------
        mapx = mapy = None
        for d in prep:
            fx, m, m3 = d["fx"], d["m"], d["m3"]
            ty, amp = fx["t"], float(fx.get("amp", .5))
            if ty in ("steam", "smoke"):
                sp = float(fx.get("speed", .3))
                off = int((t * sp * H) % H)
                f = d["f"][off:off + H, :]
                # 🔴 CHI LAM SANG. Ban dau lay = (f-0.5)*k nen no lam TOI mot nua so
                # pixel => ra VET BAN tren mat go (soi sheet moi thay). Hoi/khoi thuc te
                # chi them anh sang, khong bao gio hut anh sang.
                lay = np.clip(f - .55, 0, None) * (255.0 * amp * .55)
                fr += lay[..., None] * m3
            elif ty == "glow":
                osc = np.sin(2 * np.pi * float(fx.get("hz", .5)) * t)
                osc += .35 * np.sin(2 * np.pi * float(fx.get("hz", .5)) * 2.7 * t + 1.1)
                fr *= (1.0 + amp * .5 * osc * m3)
            elif ty == "dustbeam":
                p = d["p"]
                yy = (p[:, 1] + (t * 9.0) % H) % H
                xx = (p[:, 0] + 14.0 * np.sin(.7 * t + p[:, 3])) % W
                for j in range(len(p)):
                    x, y, s = int(xx[j]), int(yy[j]), p[j, 2]
                    if 1 <= x < W - 1 and 1 <= y < H - 1 and m[y, x] > .25:
                        fr[y - 1:y + 2, x - 1:x + 2] += 190.0 * amp * s * m[y, x]
            elif ty in ("ripple", "sway", "shimmer"):
                if mapx is None:
                    mapx, mapy = gx.copy(), gy.copy()
                if ty == "ripple":
                    hz = float(fx.get("hz", .5))
                    dyv = amp * np.sin(2 * np.pi * (gy / 26.0) - 2 * np.pi * hz * t)
                    mapy += dyv * m
                elif ty == "sway":
                    hz = float(fx.get("hz", .25))
                    dxv = amp * np.sin(2 * np.pi * hz * t + gy / 90.0)
                    mapx += dxv * m
                else:  # shimmer — nhieu nho, khong theo chu ky ro
                    dxv = amp * np.sin(gy / 9.0 + 3.1 * t) * np.cos(gx / 13.0 - 2.2 * t)
                    mapx += dxv * m
        if mapx is not None:
            fr = cv2.remap(fr, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

        # ---------- lop PHIM ----------
        if film.get("vig", 0):
            a = float(film["vig"]) * (1 + .5 * np.sin(2 * np.pi * .07 * t))
            fr *= (1 - a) + a * vig[..., None]
        if film.get("flicker", 0):
            fr *= 1.0 + float(film["flicker"]) * (rs_g.rand() - .5) * 2
        if film.get("grain", 0):
            g = rs_g.normal(0, 4.2 * float(film["grain"]), (H // 2, W // 2)).astype(np.float32)
            g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
            fr += g[..., None]
        if film.get("dust", 0) and rs_g.rand() < .45 * float(film["dust"]):
            for _ in range(rs_g.randint(1, 4)):
                x, y = rs_g.randint(0, W), rs_g.randint(0, H)
                r = rs_g.randint(1, 3)
                cv2.circle(fr, (x, y), r, (235., 235., 235.), -1)
        if film.get("scratch", 0):
            if rs_g.rand() < .012 * float(film["scratch"]) * 4:
                scr.append([rs_g.randint(0, W), rs_g.randint(2, 5)])
            for s in scr:
                ov = fr.copy()
                cv2.line(ov, (s[0], 0), (s[0] + rs_g.randint(-2, 3), H), (215., 215., 215.), 1)
                fr = cv2.addWeighted(ov, .45, fr, .55, 0)     # mo di, khong phai vach ke
                s[1] -= 1
            scr = [s for s in scr if s[1] > 0]

        out_fr = np.clip(fr, 0, 255).astype(np.uint8)
        ff.stdin.write(out_fr.tobytes())
        if sheet and k in (0, n // 3, 2 * n // 3, n - 1):
            keep.append(out_fr)

    ff.stdin.close(); rc = ff.wait()
    if sheet and len(keep) == 4:
        sh = np.vstack([np.hstack([cv2.resize(x, (W // 2, H // 2)) for x in keep[:2]]),
                        np.hstack([cv2.resize(x, (W // 2, H // 2)) for x in keep[2:]])])
        cv2.imwrite(os.path.splitext(out)[0] + "_sheet.jpg", sh, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return rc


def measure(path, fps):
    """Do lai chinh clip vua dung — de biet no CO dong that va KHUNG co bi di khong."""
    cap = cv2.VideoCapture(path)
    prev = None; mads = []; shifts = []
    while True:
        ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(f, (320, 180)), cv2.COLOR_BGR2GRAY).astype(np.float32)
        if prev is not None:
            mads.append(float(np.mean(np.abs(g - prev))))
            (dx, dy), _ = cv2.phaseCorrelate(prev, g)
            shifts.append((abs(dx) ** 2 + abs(dy) ** 2) ** .5
                          )
        prev = g
    cap.release()
    return (float(np.median(mads)) if mads else 0.0,
            float(np.median(shifts)) if shifts else 0.0,
            float(np.max(shifts)) if shifts else 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("img", nargs="?")
    ap.add_argument("--out", default=None)
    ap.add_argument("--dur", type=float, default=16.0, help="giay (nganh nay giu 1 anh 15,8-18,0s)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preset", default="flat", choices=sorted(PRESETS))
    ap.add_argument("--spec", default=None, help="file JSON, ghi de --preset")
    ap.add_argument("--sheet", action="store_true", help="xuat sheet 4 frame de nghiem thu mat")
    ap.add_argument("--size", default="1920x1080")
    ap.add_argument("--crf", type=int, default=23,
                    help="grain la ke thu cua x264: crf18 ra 97MB/16s. Clip nay la FILE TRUNG GIAN "
                         "(video_render.py re-encode lai) nen 23 la du — do duoc 97MB -> ~18MB.")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--list-presets", action="store_true")
    a = ap.parse_args()

    if a.list_presets:
        for k, v in PRESETS.items():
            print(f"  {k:<9} fx: {[x['t'] for x in v['fx']] or '(chi lop phim)'}")
        return
    if not a.img: ap.error("thieu duong dan anh")
    out = a.out or os.path.splitext(a.img)[0] + "_anim.mp4"
    spec = json.load(io.open(a.spec, encoding="utf-8")) if a.spec else PRESETS[a.preset]

    img = cv2.imread(a.img, cv2.IMREAD_COLOR)
    if img is None: print("!! khong doc duoc anh:", a.img); sys.exit(2)
    W, H = (int(x) for x in a.size.split("x"))
    ih, iw = img.shape[:2]
    if (iw, ih) != (W, H):                      # COVER-crop dung ti le, khong keo meo
        s = max(W / iw, H / ih)
        img = cv2.resize(img, (int(round(iw * s)), int(round(ih * s))), interpolation=cv2.INTER_AREA)
        y0 = (img.shape[0] - H) // 2; x0 = (img.shape[1] - W) // 2
        img = img[y0:y0 + H, x0:x0 + W]

    rc = render(img, a.dur, a.fps, spec, out, sheet=a.sheet, crf=a.crf, seed=a.seed)
    mad, sh_med, sh_max = measure(out, a.fps)
    print(f"{'✅' if rc == 0 else '🔴'} {out}  {a.dur:.0f}s @ {a.fps}fps  preset={a.spec or a.preset}")
    print(f"   MAD frame-to-frame : {mad:5.2f}   (anh tinh cua doi thu: 1,2-2,8 -> can > 3 la CO dong that)")
    print(f"   DICH KHUNG (px)    : trung vi {sh_med:.2f} | max {sh_max:.2f}"
          f"   {'OK — khung dung yen' if sh_max < 1.0 else '🔴 KHUNG BI DI (rung) — sai rang buoc'}")
    sys.exit(0 if rc == 0 and sh_max < 1.0 else 1)


if __name__ == "__main__":
    main()
