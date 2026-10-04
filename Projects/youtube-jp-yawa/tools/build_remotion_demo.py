# -*- coding: utf-8 -*-
"""build_remotion_demo.py — dung project Remotion cho MOT DOAN cua video yawa (demo lop Remotion).

  python tools/build_remotion_demo.py <stem> --t0 468.98 --t1 593.24 [--name yawa-01-demo]

Doc: 06_VIDEO/<stem>/timeline.json + 03_SCRIPTS/<stem>_SLIDES.json (khop `match` y nhu video_render.py:
dong timeline DAU TIEN chua match) + clips/clip_NN.mp4 (still_kb da duyet) + slides_img + voice.wav.
Ghi: remotion-vox/projects/<name>/project.json + public/projects/<name>/assets/.

Lop (user 2026-10-01 duyet phuong an): ① card chuong dong · ② chip tien do tren-trai · ③ cau chot tren giay
kem · ④ bui sang · ⑤ vignette tinh + hat phim · ⑥ tu khoa (KEYWORDS ben duoi, 1-2 lan/muc).
Phu de: tat trong luc card/reveal hien (chu tren the = dung cau dang doc, hien 2 lan la nhieu).
"""
import argparse, json, shutil, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-yawa")
RV = Path(r"E:\Claude\Projects\remotion-vox")
BGM = Path(r"E:\Claude\Projects\youtube-jp-health\06_VIDEO\bgm\Wholesome.mp3")
FPS, XF = 30, 12                       # dissolve 0,4s nhu renderer cu
KANJI = "〇一二三四五六七八九"
# cum tu khoa: (match dong timeline, chu hien, so dong timeline giu)
KEYWORDS = [("「……このままで", "このままで、いいじゃない", 2),
            ("家は、職場では", "家は、職場ではありません", 1)]
EXTRA_CHIPS = []

ap = argparse.ArgumentParser()
ap.add_argument("stem"); ap.add_argument("--t0", type=float, required=True); ap.add_argument("--t1", type=float, required=True)
ap.add_argument("--name", default="yawa-01-demo")
a = ap.parse_args()
VD = ROOT / "06_VIDEO" / a.stem
tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
slides = json.loads((ROOT / "03_SCRIPTS" / f"{a.stem}_SLIDES.json").read_text(encoding="utf-8"))
PLAN = VD / "_plan" / "remotion_plan.json"          # {"keywords": [[match, chu, so_dong]], "chips": [[giay, nhan]]}
if PLAN.exists():
    _pl = json.loads(PLAN.read_text(encoding="utf-8"))
    KEYWORDS = [tuple(k) for k in _pl.get("keywords", KEYWORDS)]
    EXTRA_CHIPS = [tuple(c) for c in _pl.get("chips", [])]
OUT = RV / "projects" / a.name
AS = RV / "public" / "projects" / a.name / "assets"
OUT.mkdir(parents=True, exist_ok=True); AS.mkdir(parents=True, exist_ok=True)

f = lambda sec: int(round((sec - a.t0) * FPS))
NT = f(a.t1)

def cp(src, name):
    dst = AS / name
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime or dst.stat().st_size != src.stat().st_size:
        shutil.copy2(src, dst)
    return "assets/" + name

def img_of(i):
    return next(p for e in (".jpg", ".jpeg", ".png") if (p := VD / "slides_img" / f"slide_{i:02d}{e}").exists())

# --- moc bat dau tung slide (dung luat renderer) ---
starts = []
for i, s in enumerate(slides):
    hit = next(l for l in tl if s["match"] in l["text"])
    starts.append(hit["start"])
idx = [i for i, st in enumerate(starts) if a.t0 - 0.01 <= st < a.t1 - 0.01]
print("slides", idx[0], "->", idx[-1], f"({len(idx)})")

foot, text, cap_off = [], [], []
for k, i in enumerate(idx):
    s, st = slides[i], starts[i]
    en = starts[i + 1] if i + 1 < len(slides) else a.t1
    fr, to = f(st), min(NT, f(en))
    lead = XF if k else 0
    cid = f"s{i}"
    if s.get("card"):
        ty = s["card"]["type"]
        prm, back = {}, 0
        if ty == "letter" and slides[i - 1].get("card", {}).get("type") == "letter":
            prev_l = slides[i - 1]["card"]["lines"]           # the thu noi tiep: giu phan da viet, khong dissolve
            if s["card"]["lines"][:len(prev_l)] == prev_l:
                prm["shown"] = len(prev_l)
        nx = slides[i + 1] if i + 1 < len(slides) else {}
        if ty == "letter" and nx.get("card", {}).get("type") == "letter"                 and nx["card"]["lines"][:len(s["card"]["lines"])] == s["card"]["lines"]:
            prm["holdOut"] = True
        text.append({"id": cid, "kind": "text", "from": fr, "durationInFrames": to - fr + (0 if prm.get("holdOut") else 6),
                     "preset": f"yawa-{ty}",
                     "content": "\n".join(s["card"]["lines"]), "animation": "none", "color": "#FFFFFF",
                     "animationParams": prm})
        cap_off.append((fr, to))
    elif s.get("reveal"):
        prev = img_of(i - 1)
        foot.append({"id": cid + "bg", "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                     "asset": cp(prev, f"bg_{i:02d}{prev.suffix}"), "fit": "cover", "motion": "none",
                     "fadeInFrames": lead, "filter": {"blur": 14, "brightness": 0.62, "saturate": 0.85}})
        text.append({"id": cid, "kind": "text", "from": fr, "durationInFrames": to - fr + 6, "preset": "yawa-reveal",
                     "content": "\n".join(s["reveal"]["lines"]), "animation": "none", "color": "#3A2E24",
                     "animationParams": {"times": s["reveal"]["times"]}})
        cap_off.append((fr, to))
    else:
        clip = VD / "clips" / f"clip_{i:02d}.mp4"
        foot.append({"id": cid, "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                     "asset": cp(clip, f"clip_{i:02d}.mp4"), "fit": "cover", "motion": "none", "fadeInFrames": lead})

# --- chip tien do: theo chuong, an khi card chuong hien ---
chips, cur = [], None
cards = [(i, starts[i]) for i in idx if slides[i].get("card", {}).get("type") == "chapter"]
prev_ch = next((slides[j]["card"]["lines"][0] for j in range(idx[0], -1, -1)
                if slides[j].get("card", {}).get("type") == "chapter"), None)
segs, t = [], a.t0
for i, st in cards:
    if prev_ch:
        segs.append((prev_ch, t, st))
    prev_ch = slides[i]["card"]["lines"][0]
    nxt = starts[i + 1]
    t = nxt
if prev_ch and t < a.t1:
    segs.append((prev_ch, t, a.t1))
if EXTRA_CHIPS:                     # moc phu (vd 最後の手紙 · まとめ) cat doan chuong dang chay
    out = []
    for ch, s0, s1 in segs:
        cur0 = s0
        for t_m, lab in sorted(EXTRA_CHIPS):
            if cur0 < t_m < s1:
                out.append((ch, cur0, t_m)); ch, cur0 = lab, t_m
        out.append((ch, cur0, s1))
    segs = out
for n, (ch, s0, s1) in enumerate(segs):
    if f(s1) - f(s0) > 40:
        text.append({"id": f"chip{n}", "kind": "text", "from": f(s0), "durationInFrames": f(s1) - f(s0),
                     "preset": "yawa-chip", "content": f"{ch} ／ 七" if ch.startswith("その") else ch,
                     "animation": "none", "color": "#F6EEDE"})

# --- tu khoa ---
for n, (m, word, nl) in enumerate(KEYWORDS):
    j = next((q for q, l in enumerate(tl) if m in l["text"] and a.t0 <= l["start"] < a.t1), None)
    if j is None:
        print("THIEU keyword", m); continue
    s0, s1 = tl[j]["start"], tl[j + nl - 1]["end"] + 1.2
    if any(c0 - 3 <= f(s0) < c1 for c0, c1 in cap_off):
        print("BO keyword (trung the chu dang hien)", word); continue
    e1 = min([f(s1)] + [c0 for c0, _ in cap_off if c0 > f(s0)])     # khong de len card/reveal ke tiep
    text.append({"id": f"kw{n}", "kind": "text", "from": f(s0) + 8, "durationInFrames": e1 - f(s0) - 8,
                 "preset": "yawa-keyword", "content": word, "animation": "none", "color": "#3A2E24",
                 "layout": {"x": 140, "y": 150}, "fontSize": 58})

# --- phu de: dong timeline trong cua so, bo dong nam trong card/reveal ---
caps = []
for l in tl:
    if l["end"] <= a.t0 or l["start"] >= a.t1:
        continue
    s0, s1 = max(0, f(l["start"])), min(NT, f(l["end"]))
    if any(c0 - 3 <= s0 < c1 for c0, c1 in cap_off):
        continue
    caps.append({"text": l["text"], "startMs": round(s0 * 1000 / FPS), "endMs": round(s1 * 1000 / FPS)})

voice = cp(VD / "voice.wav", "voice.wav")
bgm = cp(BGM, "bgm.mp3")
import subprocess
BGM_F = int(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                           "-of", "csv=p=0", str(BGM)])) * FPS) - 2
bgm_clips = [{"id": f"bgm{n}", "kind": "audio", "from": st0, "durationInFrames": min(BGM_F, NT - st0), "asset": bgm,
              "volume": 0.01} for n, st0 in enumerate(range(0, NT, BGM_F))]      # lap vong nhu renderer cu
proj = {
    "version": 1,
    "meta": {"name": a.name, "channel": "yawa", "fps": FPS, "width": 1920, "height": 1080},
    "timeline": {"durationInFrames": NT},
    "tracks": [
        {"id": "trk-foot", "name": "footage", "type": "video", "clips": foot},
        {"id": "trk-fx", "name": "fx", "type": "fx", "clips": [
            {"id": "dust", "kind": "fx", "variant": "dust", "from": 0, "durationInFrames": NT, "density": 22,
             "color": "#FFE7B0", "seed": 7, "fadeInFrames": 20, "fadeOutFrames": 20},
            {"id": "vig", "kind": "fx", "variant": "vignette-soft", "from": 0, "durationInFrames": NT,
             "color": "#0E0C14", "opacity": 0.55, "fadeInFrames": 0, "fadeOutFrames": 0}]},
        {"id": "trk-text", "name": "text", "type": "text", "clips": text},
        {"id": "trk-grain", "name": "grain", "type": "fx", "clips": [
            {"id": "grain", "kind": "fx", "variant": "grain", "from": 0, "durationInFrames": NT, "opacity": 0.10,
             "seed": 3, "fadeInFrames": 0, "fadeOutFrames": 0}]},
        {"id": "trk-audio", "name": "audio", "type": "audio", "clips": [
            {"id": "voice", "kind": "audio", "from": 0, "durationInFrames": NT, "asset": voice, "volume": 1,
             "trimStartFrames": int(round(a.t0 * FPS))},
            ] + bgm_clips},
    ],
    "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True, "fontSize": 50, "lines": caps},
    "theme": {"fontFamily": '"Yu Gothic", "Meiryo", sans-serif'},
    "brand": None,
}
(OUT / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK {OUT / 'project.json'} | {NT} frames ({NT / FPS:.2f}s) | foot {len(foot)} · text {len(text)} · caps {len(caps)}")
