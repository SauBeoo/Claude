# -*- coding: utf-8 -*-
"""host_insert_01.py — chen NGUOI DAN NHEP MIENG (clip Veo/Dola, tieng = VOICEVOX) vao SLIDES kinishinai bai 1.

1) Khop mieng TU DONG: MFCC (CMVN) cua tieng clip <-> doan VOICEVOX cung cau trong voice.wav -> DTW ->
   ham thoi gian vv_t -> clip_t (don dieu, lam muot, kep do doc 0,45-2,2). Nghiem thu = do trung
   "dang noi/dang nghi" (VAD) sau khi co gian; < 0,70 -> canh bao.
2) Dung clip: cat watermark (Veo: ✦ ~0,92W + chu "Veo" goc duoi-phai; Dola: chu day) -> 1920x1080 30fps,
   tron 2 frame ke nhau, + O CHU trang ben TRAI (khuon mau ku8qF5wrFxg). Tieng clip BO.
3) SLIDES: cau cua nguoi dan = [dau cau - 0,15s, dau cau ke tiep). Phan con lai cua slide -> entry "resume"
   (anh/clip still_kb cua slide chay tiep tu dung giay do). Entry moi APPEND (khong xo chi so cu).
   Nguoi dan o dau slide -> chinh entry cua slide thanh nguoi dan, clip still_kb cu doi ten _kb_full_NN.mp4.
Chay: python tools/host_insert_01.py 01_kuchiguse-hitonome [--only H03] [--dry]
"""
import sys, io, json, re, argparse, subprocess, shutil, difflib
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
W, H, FPS, SR = 1920, 1080, 30, 16000
PRE = 0.15
FONT = "C:/Windows/Fonts/YuGothB.ttc"

# ma -> (file clip, watermark, chu o trai). file: duong dan tuong doi 06_VIDEO/<stem>/ hoac tuyet doi
HOSTS = {
    "H01": ("_host_raw/z19_20/Woman_speaking_Japanese_at_desk_20261001193614_2.mp4", "veo", "心当たりは\nありませんか"),
    "H02": (r"C:\Users\tuana\Downloads\動画生成.mp4", "dola", "デパートの売り場で\n三十四年"),
    "H03": ("_host_raw/z19_20/Woman_speaking_Japanese_at_desk_20261001193614.mp4", "veo", "ラジオのように\n気楽に"),
    "H05": ("_host_raw/z19_20/Woman_speaking_Japanese_at_desk_20261001193614_3.mp4", "veo", "誰も\n見ていなかった"),
    "H06": ("_host_raw/z19_19/Woman_speaking_Japanese_at_desk_20261001194518.mp4", "veo", "次は\nもっと近い人"),
    "H07": ("_host_raw/z19_19/Elderly_woman_speaking_Japanese_20261001194518_3.mp4", "veo", "弱音をひとつ\n言えたら"),
    "H08": ("_host_raw/z19_19/Elderly_woman_speaking_Japanese_20261001194518_2.mp4", "veo", "いくつ\n当てはまりましたか"),
    "H09": ("_host_raw/z19_19/Elderly_woman_speaking_Japanese_20261001194518.mp4", "veo", "七つ目だけは…"),
    "H10": ("_host_raw/z19_19/Woman_speaking_in_Japanese_room_20261001194518.mp4", "veo", "我慢をひとつ\n正直に"),
    "H11": ("_host_raw/z19_48/Elderly_woman_speaking_Japanese_20261001195137.mp4", "veo", "今年の\nお正月の話"),
    "H14": ("_host_raw/z19_48/Elderly_woman_speaking_Japanese_…_20261001195138.mp4", "veo", "チャンネル登録"),
    "H15": ("_host_raw/z19_48/Woman_speaking_Japanese_at_desk_20261001195137_2.mp4", "veo", "あなたの\nままで"),
}
# Khop TAY (veo_a, veo_b, vv_a, vv_b) khi DTW trung VAD < 0,70 — vv tinh tu dau doan (dau cau - PRE).
# veo_a == veo_b = giu khung (VOICEVOX nghi o 「、」 ma Veo noi lien).
MANUAL = {
    # VV: 誰も 0,24-0,80 | nghi | 見ていませんでした 1,30-2,60 | 。 | ちょっと 3,08-3,66 | 、 | がっかりしたくらいです 4,24-5,74
    # Veo: 誰も見ていませんでしたね 0,40-2,50 | nghi | ちょっとがっかりしたくらいですね 3,16-6,40 (+ね 6,40-6,76 bo)
    "H05": [(0.00, 0.40, 0.00, 0.24), (0.40, 0.75, 0.24, 0.80), (0.75, 0.75, 0.80, 1.30), (0.75, 2.50, 1.30, 2.60),
            (2.50, 3.16, 2.60, 3.08), (3.16, 3.70, 3.08, 3.66), (3.70, 3.70, 3.66, 4.24), (3.70, 6.30, 4.24, 5.74),
            (6.30, 6.45, 5.74, 5.95)],
}

# User 2026-10-01: "chuyen canh nhanh qua" -> bo lan nguoi dan ngan / ke cum hinh ngan (do: 11 hinh < 6s)
SKIP = {"H01", "H06", "H07", "H08", "H14"}
# resume ngan -> cho slide KE TIEP vao som (nuot doan resume) thay vi cat them mot hinh
MERGE_NEXT = {"H10", "H03"}   # H03: the 「その一」 vao tu cau 「遠くの人から…」 (dan vao chuong 1)

LINES = {
    "H01": "そんな夜に、心当たりはありませんか。", "H02": "私は、ずっと、そうでした。",
    "H03": "家事をしながら、ラジオのように", "H05": "誰も、見ていませんでした。", "H06": "ご近所の次は、もっと近い人です。",
    "H07": "弱音を一つ言えた人には", "H08": "ここまでで、いくつ当てはまりましたか。", "H09": "でも、七つ目だけは",
    "H10": "今日、ひとつだけ、我慢していることを", "H11": "では最後に、私の、今年のお正月の話を",
    "H14": "よろしければ、チャンネル登録をして", "H15": "あなたが、あなたのままで",
}


def norm(s):
    return re.sub(r"[「」『』、。？！…・\s]", "", s)


def load_audio(path, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{ss:.3f}"] if ss is not None else []) + ["-i", str(path)] + \
          (["-t", f"{to - ss:.3f}"] if to is not None else []) + ["-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.int16).astype(np.float32) / 32768


def mfcc(x, hop=0.02):
    n, h = 512, int(SR * hop)
    if len(x) < n:
        x = np.pad(x, (0, n - len(x)))
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::h] * np.hanning(n)
    sp = np.abs(np.fft.rfft(fr, axis=1)) ** 2
    mel = lambda f: 2595 * np.log10(1 + f / 700)
    pts = 700 * (10 ** (np.linspace(mel(80), mel(7600), 42) / 2595) - 1)
    bins = np.floor((n + 1) * pts / SR).astype(int)
    fb = np.zeros((40, sp.shape[1]))
    for m in range(1, 41):
        a, b, c = bins[m - 1], bins[m], bins[m + 1]
        fb[m - 1, a:b] = (np.arange(a, b) - a) / max(b - a, 1)
        fb[m - 1, b:c] = (c - np.arange(b, c)) / max(c - b, 1)
    lm = np.log(sp @ fb.T + 1e-8)
    k = np.arange(40)
    dct = np.cos(np.pi / 40 * (k[None, :] + 0.5) * np.arange(1, 13)[:, None])
    c = lm @ dct.T
    e = np.log((fr ** 2).sum(1) + 1e-8)
    f = np.column_stack([c, e * 0.5])
    return (f - f.mean(0)) / (f.std(0) + 1e-6), e


def vad(e):
    thr = np.percentile(e, 20) + 0.45 * (np.percentile(e, 95) - np.percentile(e, 20))
    v = e > thr
    return np.convolve(v.astype(float), np.ones(5) / 5, "same") > 0.5


def dtw_map(fa, fb):
    """fa: vv (N), fb: clip (M). -> mang M_of_N (chi so clip cho moi frame vv)."""
    N, M = len(fa), len(fb)
    D = np.sqrt(((fa[:, None, :] - fb[None, :, :]) ** 2).sum(2))
    C = np.full((N + 1, M + 1), np.inf); C[0, 0] = 0
    for i in range(1, N + 1):
        ci, di = C[i - 1], D[i - 1]
        row = C[i]
        for j in range(1, M + 1):
            row[j] = di[j - 1] + min(ci[j - 1], ci[j] + 0.3, row[j - 1] + 0.3)
    i, j, path = N, M, []
    while i > 0 and j > 0:
        path.append((i - 1, j - 1))
        k = np.argmin([C[i - 1, j - 1], C[i - 1, j], C[i, j - 1]])
        i, j = (i - 1, j - 1) if k == 0 else ((i - 1, j) if k == 1 else (i, j - 1))
    m = np.zeros(N)
    for a, b in path:
        m[a] = b if m[a] == 0 else (m[a] + b) / 2
    m = np.maximum.accumulate(np.convolve(np.pad(m, 4, mode="edge"), np.ones(9) / 9, "valid"))
    return m


def crop_frame(f, wm):
    h, w = f.shape[:2]
    if wm == "dola":
        nh = int(h * 0.90); nw = int(nh * 16 / 9); f = f[:nh, w - nw:]
    else:   # veo: ✦ ~0,93W/0,82-0,92H + chu "Veo" ~0,95H — soi 1:1 ca 11 clip (2026-10-01).
        # GIU 79% PHIA TREN, lay ve PHIA PHAI (bo trai): cat 87% ben trai tung xen mat nguoi ngoi sat mep phai (H05/H09)
        nh = int(h * 0.79); nw = int(nh * 16 / 9); f = f[:nh, w - nw:]
    return cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)


def callout(text):
    """O chu trang bo goc ben trai (BGRA overlay)."""
    lines = text.split("\n")
    size = 64
    ft = ImageFont.truetype(FONT, size)
    ws = [ft.getbbox(l)[2] for l in lines]
    bw, bh = max(ws) + 96, len(lines) * int(size * 1.35) + 64
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    x0, y0 = 96, 300
    d.rounded_rectangle([x0 + 6, y0 + 8, x0 + bw + 6, y0 + bh + 8], 22, fill=(0, 0, 0, 60))
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], 22, fill=(255, 255, 255, 238))
    d.rectangle([x0, y0 + 18, x0 + 10, y0 + bh - 18], fill=(176, 120, 52, 255))   # vach nhan mau dong
    for k, l in enumerate(lines):
        d.text((x0 + 48, y0 + 30 + k * int(size * 1.35)), l, font=ft, fill=(40, 48, 72, 255))
    a = np.asarray(im).astype(np.float32)
    return a[:, :, [2, 1, 0]], a[:, :, 3:4] / 255


def piece_map(M, N):
    """ban do tay -> mang chi so frame clip (20ms) cho moi frame vv."""
    m = np.zeros(N)
    for k in range(N):
        t = k * 0.02
        va, vb, xa, xb = next((s for s in M if s[2] <= t < s[3]), M[-1])
        m[k] = (va if vb <= va else va + (min(t, xb) - xa) * (vb - va) / (xb - xa)) / 0.02
    return m


def build_clip(src, wm, text, vv_seg, out, report, manual=None):
    ca = load_audio(src)
    fv, ev = mfcc(vv_seg); fc, ec = mfcc(ca)
    m = piece_map(manual, len(fv)) if manual else dtw_map(fv, fc)   # frame vv (20ms) -> frame clip (20ms)
    sl = np.diff(m) if len(m) > 1 else np.array([1.0])
    agree = (vad(ev) == vad(ec)[np.clip(m.astype(int), 0, len(ec) - 1)]).mean()
    report.append((agree, float(np.median(sl[sl > 0])) if (sl > 0).any() else 0))
    cap = cv2.VideoCapture(str(src)); vf = cap.get(cv2.CAP_PROP_FPS); fr = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        fr.append(crop_frame(f, wm))
    rgb, al = callout(text) if text else (None, None)   # text=None -> clip SACH (ban Remotion kieu yawa)
    dur = len(vv_seg) / SR
    n = int(round(dur * FPS))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
                            "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        k = min(int(t / 0.02), len(m) - 1)
        tc = m[k] * 0.02
        p = min(max(tc * vf, 0), len(fr) - 1); i0 = int(p); i1 = min(i0 + 1, len(fr) - 1); w1 = p - i0
        img = fr[i0].astype(np.float32) * (1 - w1) + fr[i1].astype(np.float32) * w1
        if rgb is not None:
            img = img * (1 - al) + rgb * al
        enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    return enc.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("--only"); ap.add_argument("--dry", action="store_true")
    ap.add_argument("--no-build", action="store_true", help="chi viet lai SLIDES + resume, dung clip nguoi dan da dung")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    sp = PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json"
    sl = json.loads(sp.read_text(encoding="utf-8"))
    assert not any(e.get("_host") or e.get("_resume") for e in sl), "SLIDES da co nguoi dan — khoi phuc ban _pre_host truoc"
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8")); lines, total = tl["lines"], tl["total"]
    voice = vd / "voice.wav"

    def st_of(e):
        hit = next(ln for ln in lines if e["match"] in ln["text"]); return hit["start"] + float(e.get("offset", 0.0))
    order = sorted(range(len(sl)), key=lambda i: st_of(sl[i]))
    starts = {i: st_of(sl[i]) for i in order}; starts[order[0]] = 0.0
    spans = {}
    for k, i in enumerate(order):
        spans[i] = (starts[i], starts[order[k + 1]] if k + 1 < len(order) else total)

    host = []   # (ma, line_idx, t0, t1)
    for code, key in LINES.items():
        if code in SKIP:
            continue
        hit = [n for n, ln in enumerate(lines) if key in ln["text"]]
        assert len(hit) == 1, f"{code}: 「{key}」 khop {len(hit)} dong"
        n = hit[0]
        t0 = lines[n]["start"] - PRE
        t1 = lines[n + 1]["start"] if n + 1 < len(lines) else total
        host.append((code, n, t0, t1))
    host.sort(key=lambda x: x[2])

    def uniq(n):
        """tien to ngan nhat ma dong DAU TIEN chua no chinh la dong n (build_slides lay hit dau tien)."""
        t = lines[n]["text"]
        for L in range(6, len(t) + 1):
            if next(k for k, ln in enumerate(lines) if t[:L] in ln["text"]) == n:
                return t[:L]
        raise SystemExit(f"khong tao duoc match duy nhat cho dong {n}")

    new = list(sl); cd = vd / "clips"; si = vd / "slides_img"
    plan = []
    for code, n, t0, t1 in host:
        s = next(i for i in order if spans[i][0] <= lines[n]["start"] < spans[i][1])
        a0, a1 = spans[s]
        at_head = lines[n]["start"] - a0 < 0.05
        if at_head:
            idx = s; new[s] = dict(new[s]); new[s]["offset"] = float(new[s].get("offset", 0.0)) - PRE
        else:
            idx = len(new); new.append({"match": uniq(n), "offset": -PRE})
        new[idx]["video"] = True; new[idx]["_host"] = code
        # phan con lai cua slide sau cau
        res = None
        nxt_host = any(abs(h[2] - t1) < 0.4 for h in host)   # cau ke tiep cung la nguoi dan -> khong resume
        if code in MERGE_NEXT and t1 < a1 - 0.3:
            k = order.index(s); nx = order[k + 1]
            nl = next(m for m in range(n + 1, len(lines)) if lines[m]["start"] >= t1 - 0.01)
            new[nx] = dict(new[nx]); new[nx]["match"] = uniq(nl); new[nx]["offset"] = 0.0; new[nx]["_merged"] = code
            print(f"   {code}: slide {nx} vao som tu dong {nl} (nuot resume)")
        elif t1 < a1 - 0.3 and not nxt_host:
            nxt = next(m for m in range(n + 1, len(lines)) if lines[m]["start"] >= t1 - 0.01)
            res = len(new); new.append({"match": uniq(nxt), "_resume": s, "_from": round(t1 - a0, 3)})
        plan.append((code, idx, s, at_head, res, t0, t1, a0))
        print(f"{code} {t0:7.1f}-{t1:7.1f}s ({t1 - t0:4.1f}s) slide {s}{' (dau slide)' if at_head else ''}"
              f"{' + resume #' + str(res) if res is not None else ''}")
    for i, e in enumerate(new[len(sl):], len(sl)):
        assert any(e["match"] in ln["text"] for ln in lines), i
    n_min = len(new) / (total / 60)
    print(f"SLIDES {len(sl)} -> {len(new)} entry · {n_min:.2f} hinh/phut")
    if a.dry:
        return

    report = []
    only = set(a.only.split(",")) if a.only else None
    for code, idx, s, at_head, res, t0, t1, a0 in plan:
        if (only and code not in only) or a.no_build:
            continue
        f, wm, text = HOSTS[code]
        src = Path(f) if Path(f).is_absolute() else vd / f
        seg = load_audio(voice, t0, t1)
        out = cd / f"clip_{idx:02d}.mp4"
        if at_head and out.exists() and not (cd / f"_kb_full_{s:02d}.mp4").exists():
            shutil.move(str(out), str(cd / f"_kb_full_{s:02d}.mp4"))
        rc = build_clip(src, wm, text, seg, out, report, MANUAL.get(code))
        ag, slope = report[-1]
        print(f"  {code} -> clip_{idx:02d} · khop VAD {ag:.0%} · do doc trung vi {slope:.2f}"
              + ("  ⚠️ khop thap" if ag < 0.70 else "") + ("" if rc == 0 else f"  LOI {rc}"))
    # resume
    for code, idx, s, at_head, res, t0, t1, a0 in plan:
        if res is None or (only and code not in only):
            continue
        e = sl[s]; frm = t1 - a0
        if e.get("video") and not e.get("reveal"):
            kb = cd / (f"_kb_full_{s:02d}.mp4" if (cd / f"_kb_full_{s:02d}.mp4").exists() else f"clip_{s:02d}.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{frm:.3f}", "-i", str(kb), "-an", "-c:v", "libx264",
                            "-crf", "17", "-preset", "veryfast", str(cd / f"clip_{res:02d}.mp4")], check=True)
            new[res]["video"] = True
        elif e.get("reveal"):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{frm:.3f}", "-i", str(cd / f"clip_{s:02d}.mp4"), "-an",
                            "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", str(cd / f"clip_{res:02d}.mp4")], check=True)
            new[res]["video"] = True
        else:   # the chu tinh / anh tinh
            shutil.copy(si / f"slide_{s:02d}.png", si / f"slide_{res:02d}.png")
            new[res]["photo"] = True; new[res]["static"] = True
    sp.write_text(json.dumps(new, ensure_ascii=False, indent=1), encoding="utf-8")
    print("OK ->", sp.name)


if __name__ == "__main__":
    main()
