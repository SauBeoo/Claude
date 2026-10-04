# build_demo_sono1.py — DEMO video 01, muc その一 only (split-screen comparison + full-frame shots).
# 1) cut その一 out of the v4 _TTS.md  2) synth line by line via VOICEVOX (timeline from REAL wav)
# 3) write Remotion project.json -> remotion-vox/projects/teinengo-01-demo
# Also writes 3 voice auditions (first 4 lines) to 06_VIDEO/<slug>/demo/audition_*.wav
import io, json, os, re, shutil, sys, wave
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
import tts_render as T  # parse_script, synthesize, resolve_style, api

PRJ = r"E:\Claude\Projects\youtube-jp-teinengo"
SLUG = "01_teinengo-kurashi-7chigai"
VD = os.path.join(PRJ, "06_VIDEO", SLUG)
DEMO = os.path.join(VD, "demo"); os.makedirs(DEMO, exist_ok=True)
IMG = os.path.join(VD, "img_sono1")
RV = r"E:\Claude\Projects\remotion-vox"
NAME = os.environ.get("TEI_NAME", "teinengo-01-demo")
ASSETS = os.path.join(RV, "public", "projects", NAME, "assets"); os.makedirs(ASSETS, exist_ok=True)
os.makedirs(os.path.join(RV, "projects", NAME), exist_ok=True)
BASE = "http://127.0.0.1:50021"
SPEAKER, STYLE, SPEED, INTON = "麒ヶ島宗麟", "ノーマル", 0.90, 1.15
FPS, W, H = 30, 1920, 1080
BGM = r"E:\Claude\Projects\youtube-jp-health\06_VIDEO\bgm\Wholesome.mp3"

# ---------- 1. cut その一 ----------
src = io.open(os.path.join(PRJ, "03_SCRIPTS", SLUG + "_TTS.md"), encoding="utf-8").read()
seg = src[src.index("その一。"):src.index("その二。")].rstrip() + "\n"
demo_tts = os.path.join(DEMO, "demo_sono1_TTS.md")
io.open(demo_tts, "w", encoding="utf-8", newline="\n").write(seg)

speakers = T.api(BASE, "GET", "/speakers")
sid = T.resolve_style(speakers, SPEAKER, STYLE)
sid = sid[-1] if isinstance(sid, tuple) else sid

def render(events, style_id, out_wav):
    """returns list of (text, start_s, end_s) measured from the real wav."""
    segs, params, t, lines = [], None, 0.0, []
    for ev in events:
        if "pause" in ev:
            segs.append(float(ev["pause"])); t += ev["pause"]; continue
        wav = T.synthesize(BASE, ev["text"], style_id, ev["speed"] or SPEED, ev["intonation"] or INTON,
                           ev["pitch"], ev["volume"])
        p, fr = T.wav_params_and_frames(wav)
        params = params or p
        d = len(fr) / (p.framerate * p.sampwidth * p.nchannels)
        segs.append(fr); lines.append((ev["text"], t, t + d)); t += d
    segs.append(1.0); t += 1.0
    T.write_output(out_wav, segs, params)
    return lines, t

events = T.parse_script(demo_tts, gap=0.6, section_gap=1.1)
voice = os.path.join(DEMO, "voice_sono1.wav")
LINES, TOTAL = render(events, sid, voice)
print(f"voice {TOTAL:.1f}s, {len(LINES)} lines, speaker {SPEAKER}/{STYLE} id={sid}")
for i, (tx, a, b) in enumerate(LINES):
    print(f"{i:2d} {a:6.2f}-{b:6.2f} {tx[:30]}")

# auditions: first 4 lines, 3 voices
aud_ev = [e for e in events if "text" in e][:4]
aud_ev = sum(([e, {"pause": 0.6}] for e in aud_ev), [])
for name in ([] if os.environ.get("TEI_NO_AUD") else ["青山龍星", "麒ヶ島宗麟", "玄野武宏"]):
    s = T.resolve_style(speakers, name, "ノーマル"); s = s[-1] if isinstance(s, tuple) else s
    render(aud_ev, s, os.path.join(DEMO, f"audition_{name}.wav"))

# ---------- 2. shot plan (by line index) ----------
f = lambda s: int(round(s * FPS))
st = lambda i: LINES[i][1]
en = lambda i: LINES[i][2]
N = len(LINES)
assert N == 21, f"plan expects 21 lines in その一, got {N} — script changed, re-plan"

for fn in os.listdir(IMG):
    if fn.endswith(".png") and not fn.startswith("_"):
        shutil.copy2(os.path.join(IMG, fn), os.path.join(ASSETS, fn))
shutil.copy2(voice, os.path.join(ASSETS, "voice.wav"))
shutil.copy2(BGM, os.path.join(ASSETS, "bgm.mp3"))

SPLIT_END = st(5)                       # split screen = lines 0..4
# full-frame shots: (asset, from_line, to_line_exclusive)
SHOTS = [("09_porch", 5, 7), ("07_door", 7, 9), ("01_tie", 9, 10), ("02_gate", 10, 11), ("03_closet", 11, 13),
         ("04_sofa", 13, 14), ("05_dusk", 14, 16), ("06_dress", 16, 18), ("08_mailbox", 18, 20),
         ("10_hall", 20, 21)]
DUR = f(TOTAL)
BOX_W, BOX_H, BOX_Y, GAP = 900, 506, 170, 40
LX = (W - 2 * BOX_W - GAP) // 2; RX = LX + BOX_W + GAP
D = 12  # dissolve frames (0.4s)

def cx(box_x, text, size): return int(box_x + BOX_W / 2 - len(text) * size / 2)
def txt(id_, content, preset, a, b, x=None, y=None, size=None, color="#FFE01B", anim="pop", w=None):
    lay = {k: v for k, v in (("x", x), ("y", y), ("w", w)) if v is not None}
    return {"id": id_, "kind": "text", "from": a, "durationInFrames": max(1, b - a), "content": content,
            "preset": preset, "color": color, "animation": anim, "layout": lay, "fontSize": size}
def pic(id_, asset, a, b, layout=None, filt=None, fade=D):
    c = {"id": id_, "kind": "video", "from": a, "durationInFrames": max(1, b - a), "asset": f"assets/{asset}.png",
         "fadeInFrames": fade}
    if layout: c["layout"] = layout
    if filt: c["filter"] = filt
    return c

sE = f(SPLIT_END) + D  # overlap so the first full shot dissolves over the split
TITLE_IMG = os.path.join(VD, "img_title", "00_title_sono1.png")
title_pics = []
if os.path.exists(TITLE_IMG):  # real photo under the その一 title, dimmed so the title reads
    shutil.copy2(TITLE_IMG, os.path.join(ASSETS, "00_title_sono1.png"))
    title_pics = [pic("T0", "00_title_sono1", 0, f(st(1)) + D, filt={"brightness": 0.72}, fade=0)]
else:
    print("NOTE: no img_title/00_title_sono1.png yet -> title card on plain background")
BG_FROM = f(st(1)) if title_pics else 0  # split background dissolves in over the title photo
pics = [pic("A", "A_left", f(st(1)), sE, {"x": LX, "y": BOX_Y, "w": BOX_W, "h": BOX_H}, {"saturate": 0.35, "brightness": 0.9}),
        pic("B", "B_right", f(st(2)), sE, {"x": RX, "y": BOX_Y, "w": BOX_W, "h": BOX_H}, {"saturate": 1.12, "brightness": 1.04})]
for k, (a, i0, i1) in enumerate(SHOTS):
    a_f = f(st(i0)) if k else f(SPLIT_END)
    b_f = (f(st(SHOTS[k + 1][1])) + D) if k + 1 < len(SHOTS) else DUR
    pics.append(pic(f"s{k}", a, a_f, b_f))

# ---------- 3. text synced to speech (VOICEVOX mora timing) ----------
sys.path.insert(0, os.path.join(RV, "tools"))
import vv_word_timing as VW
WORDS = []
for tx, a, b in LINES:
    q = VW.audio_query_cached(BASE, "voicevox", sid, tx)
    WORDS.append(VW.split_line_words(tx, VW.phrase_fractions(q), a * 1000, b * 1000))

def char_t(li, ci):
    """absolute seconds when char ci of line li is spoken."""
    k = 0
    for w in WORDS[li]:
        n = len(w["text"])
        if ci < k + n:
            return (w["startMs"] + (w["endMs"] - w["startMs"]) * (ci - k) / n) / 1000
        k += n
    return LINES[li][2]

def span(li, sub, until=None, after=0):
    """(a,b) absolute seconds: from start of `sub` to end of `until` (or of sub) in line li."""
    tx = LINES[li][0]
    i = tx.index(sub, after)
    j = tx.index(until, i) + len(until) if until else i + len(sub)
    return char_t(li, i), char_t(li, j - 1) + 0.12

def runs_for(spec, clip_from_s):
    """spec: lines; run = (display, li, sub[, until][, hot]) or ("->", a_s, b_s)."""
    out = []
    for line in spec:
        rl = []
        for r in line:
            if r[0] == "->":
                rl.append({"arrow": True, "a": round(r[1] - clip_from_s, 3), "b": round(r[2] - clip_from_s, 3)})
                continue
            disp, li, sub = r[0], r[1], r[2]
            until = r[3] if len(r) > 3 and isinstance(r[3], str) else None
            hot = isinstance(r[-1], bool) and r[-1]
            a, b = span(li, sub, until)
            rl.append({"t": disp, "a": round(a - clip_from_s, 3), "b": round(b - clip_from_s, 3), "hot": hot})
        out.append(rl)
    return out

def first_t(spec):
    for line in spec:
        for r in line:
            if r[0] != "->":
                return span(r[1], r[2])[0] - 0.15

def card(id_, spec, b_f, x=90, y=80, size=80, color="#FFC46B", box=False, ink="#FFFFFF"):
    a_f = max(0, f(first_t(spec)))
    return {"id": id_, "kind": "text", "from": a_f, "durationInFrames": max(1, b_f - a_f), "content": "",
            "preset": "tei-reveal", "color": color, "animation": "none",
            "animationParams": {"lines": runs_for(spec, a_f / FPS), "box": box, "ink": ink},
            "layout": {"x": x, "y": y}, "fontSize": size}

def label(id_, content, a_s, b_f, x, y, w, size, color, ink="#FFFFFF"):
    a_f = max(0, f(a_s))
    lay = {"x": x, "y": y}
    if w: lay["w"] = w
    return {"id": id_, "kind": "text", "from": a_f, "durationInFrames": max(1, b_f - a_f), "content": content,
            "preset": "tei-label", "color": color, "animation": "none", "animationParams": {"ink": ink},
            "layout": lay, "fontSize": size}

BGS = {  # name: (left label colour, right label colour, ink for text drawn on the background)
    "washi":    ("#7D8798", "#E8954A", "#2B2A28"),
    "split":    ("#96A6BE", "#F4A85C", "#FFFFFF"),
    "charcoal": ("#7D8798", "#E8954A", "#FFFFFF"),
    "blur":     ("#7D8798", "#E8954A", "#FFFFFF"),
}
BG = os.environ.get("TEI_BG", "washi")
LC, RC, BG_INK = BGS[BG]
Q = 54
mid = lambda box_x: box_x + BOX_W // 2
ACC_BG = "#D9772E" if BG == "washi" else "#FFC46B"
split_txt = [
    card("t_no", [[("その一", 0, "その一")]], f(st(1)) + 6, x=W // 2 - 195, y=420, size=130, ink=BG_INK),
    label("lab_l", "退屈になる人", span(1, "退屈")[0] - 0.1, sE, LX, 44, BOX_W, 62, LC),
    label("lab_r", "楽しくなる人", span(2, "楽しく")[0] - 0.1, sE, RX, 44, BOX_W, 62, RC),
    card("q_l", [[("「起きても、することがない」", 1, "「起きても", "ない」")]], sE,
         x=mid(LX) - 7 * Q, y=BOX_Y + BOX_H + 30, size=Q, ink=BG_INK),
    card("q_r", [[("「とりあえず、着替えるか」", 2, "「とりあえず", "か」")]], sE,
         x=mid(RX) - int(6.5 * Q), y=BOX_Y + BOX_H + 30, size=Q, ink=BG_INK),
    card("q_mid", [[("一年後、", 3, "一年後"), ("まるで", 3, "まるで"), ("別の人生", 3, "別の人生", True)]], sE,
         x=W // 2 - 270, y=820, size=64, color=ACC_BG, ink=BG_INK),
]
H1 = "#FFC46B"; COOL = "#B9C8E2"
a1 = span(13, "が十時")[0]; b1 = span(13, "十時")[0]
a2 = span(13, "になり")[0]; b2 = span(13, "昼")[0]
cards = [
    card("c_ba", [[("行動活性化", 7, "行動活性化", True)]], f(st(9)), size=96, color=H1),
    card("c_ba2", [[("やる気は、", 7, "やる気は")], [("動いたあとから", 7, "動いたあとから")], [("ついてくる", 7, "ついてくる", True)]],
         f(st(9)), y=220, size=76, color=H1),
    card("c_gone", [[("合図が、", 11, "合図が")], [("すべて消えた", 11, "すべて消え", True)]], f(st(12)), size=92, color=COOL),
    card("c_kono", [[("このままだと…", 12, "このままだと")]], f(st(14)), size=84, color=COOL),
    card("c_time", [[("九時", 13, "九時"), ("->", a1, b1), ("十時", 13, "十時"), ("->", a2, b2), ("昼", 13, "昼", True)]],
         f(st(14)), x=1000, y=250, size=86, color=COOL),
    label("c_case", "元営業部長", span(14, "元営業部長")[0] - 0.1, f(st(16)), 1060, 100, None, 52, "#96A6BE"),
    card("c_quote", [[("「着替える理由が、", 15, "「着替える理由が")], [("ひとつも、なかった」", 15, "ひとつも", "なかった")]],
         f(st(16)), x=1060, y=230, size=76, box=True),
    card("c_tano", [[("楽しくなる人", 16, "楽しくなる人", True), ("は", 16, "は")]], f(st(18)), size=80, color=H1),
    card("c_steps", [[("① 七時に着替える", 17, "七時に着替える")], [("② 玄関の外に出る", 17, "玄関の外に出る")],
                     [("③ 新聞を取りに行く", 17, "新聞を取りに行く")]], f(st(18)), x=1250, y=300, size=66, box=True),
    card("c_rule", [[("これをしたら", 18, "これをしたら")], [("一日が始まる", 18, "一日が始まる", True)]], f(st(20)), size=92, color=H1),
    card("c_next", [[("差がつくのは", 20, "差がつくのは")], [("人の前に出た瞬間", 20, "人の前に出た", "瞬間", True)]], DUR, size=84, color=H1),
]

# ---------- 4. background variants ----------
from PIL import Image, ImageFilter
import numpy as np
def save_bg(name):
    p = os.path.join(ASSETS, f"bg_{name}.png")
    rng = np.random.default_rng(7)
    if name == "washi":
        base = np.zeros((H, W, 3), np.float32) + np.array([238, 230, 214], np.float32)
        fib = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        fib = ((fib - fib.min()) / np.ptp(fib) * 255).astype(np.uint8)
        fib = np.array(Image.fromarray(fib).resize((W, H)).filter(ImageFilter.GaussianBlur(2)), np.float32)
        base += (fib[..., None] - 128) * 0.06 + rng.normal(0, 2.2, (H, W, 1))
    elif name == "split":
        x = np.linspace(0, 1, W)[None, :, None]
        cool = np.array([84, 92, 108], np.float32); warm = np.array([200, 138, 84], np.float32)
        k = np.clip((x - 0.42) / 0.16, 0, 1)
        base = cool * (1 - k) + warm * k + np.zeros((H, 1, 1), np.float32)
        y = np.linspace(-1, 1, H)[:, None, None]
        base = base * (1 - 0.18 * y ** 2) + rng.normal(0, 1.5, (H, W, 1))
    elif name == "charcoal":
        yy, xx = np.mgrid[-1:1:H * 1j, -1:1:W * 1j]
        v = 1 - 0.35 * (xx ** 2 * 0.6 + yy ** 2)
        base = np.array([46, 41, 38], np.float32) * v[..., None] + rng.normal(0, 1.8, (H, W, 1))
    else:  # blur: each half = its own picture, blurred + dimmed
        im = Image.new("RGB", (W, H))
        for fn, x0 in (("A_left.png", 0), ("B_right.png", W // 2)):
            src = Image.open(os.path.join(ASSETS, fn)).convert("RGB").resize((int(H * 1376 / 768), H))
            cx0 = (src.width - W // 2) // 2
            im.paste(src.crop((cx0, 0, cx0 + W // 2, H)).filter(ImageFilter.GaussianBlur(30)), (x0, 0))
        base = np.array(im, np.float32)
        base[:, :W // 2] = base[:, :W // 2] * 0.5 + 8
        base[:, W // 2:] = base[:, W // 2:] * 0.6
    Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(p)
    return f"assets/bg_{name}.png"
bg_asset = save_bg(BG)

# captions: split long lines (SUB_MAXLEN 42 -> ~2 rows of 21) at 、 near the middle, time by chars
def cap_lines():
    out = []
    for tx, a, b in LINES:
        parts = [tx]
        if len(tx) > 30:
            cuts = [m.end() for m in re.finditer("[、。]", tx[:-1])]
            if cuts:
                c = min(cuts, key=lambda c: abs(c - len(tx) / 2)); parts = [tx[:c], tx[c:]]
        tot = sum(len(p) for p in parts); t = a
        for p in parts:
            d = (b - a) * len(p) / tot
            out.append({"text": p, "startMs": int(t * 1000), "endMs": int((t + d) * 1000)}); t += d
    return out

proj = {
    "version": 1,
    "meta": {"name": NAME, "channel": "teinengo", "fps": FPS, "width": W, "height": H},
    "timeline": {"durationInFrames": DUR},
    "tracks": [
        {"id": "bg", "name": "bg", "type": "background", "clips": [
            {"id": "bg0", "kind": "background", "from": 0, "durationInFrames": DUR,
             "tint": "#1E2638", "tintOpacity": 1, "grid": False, "dots": False}]},
        {"id": "title", "name": "title photo", "type": "video", "clips": title_pics},
        {"id": "bgimg", "name": "bg image", "type": "video", "clips": [
            {"id": "bgi", "kind": "video", "from": BG_FROM, "durationInFrames": sE - BG_FROM, "asset": bg_asset,
             "fadeInFrames": D if BG_FROM else 0}]},
        {"id": "pics", "name": "pics", "type": "video", "clips": pics},
        {"id": "split", "name": "split text", "type": "text", "clips": split_txt},
        {"id": "cards", "name": "cards", "type": "text", "clips": cards},
        {"id": "aud", "name": "audio", "type": "audio", "clips": [
            {"id": "voice", "kind": "audio", "from": 0, "durationInFrames": DUR, "asset": "assets/voice.wav", "volume": 1},
            {"id": "bgm", "kind": "audio", "from": 0, "durationInFrames": DUR, "asset": "assets/bgm.mp3", "volume": 0.01}]},
    ],
    "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True, "fontSize": 44, "lines": cap_lines()},
}
out = os.path.join(RV, "projects", NAME, "project.json")
json.dump(proj, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# pace report
holds = [(c["asset"], c["durationInFrames"] / FPS) for c in pics if "layout" not in c]
print("shots:", [(a.split('/')[-1][:-4], round(d, 1)) for a, d in holds])
print(f"split {SPLIT_END:.1f}s | total {TOTAL:.1f}s | {len(holds)+1} pictures -> {(len(holds)+1)/(TOTAL/60):.1f}/min")
print("wrote", out)
