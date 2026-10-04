# -*- coding: utf-8 -*-
r"""Rai lop DONG cho video 22 (shokutaku, ラーメン x 水道管を守る) — CHUAN MOI
tach rieng ① tran doi HERO va ② san su kien 7s (audience-45plus.md §2.0 +
feedback_nhip_hinh_san_7s, chot 2026-08-30), KHONG gop chung thanh mot con so
"6.0/phut" nhu ban video 20/21 con lam (bai hoc da ghi trong file luat).

    py -3 tools\build_overlays_22.py

Thuat toan (khac video 18-21: o day KHONG list tay tung diem, vi san 7s doi hoi
qua nhieu diem de liet ke dung tay ma khong sai so):
  1. Lay gio bat dau THAT cua moi slide hero (track trk-slides) — day la lop ①,
     KHONG dung toi (dung sua bang cach tang so slide — dam vao tran ①).
  2. Dat mot so tag CHU CO Y NGHIA (con so / ket luan CO THAT trong loi doc) tai
     dung cau trong phu de — tim bang KHOP CHUOI trong captions.lines, giong
     cach `build_slides_22.py` khop slide bang chuoi trong _TTS.md.
  3. Gop hero-times + tag-times thanh danh sach moc. O MOI KHE > 7s giua hai moc
     lien tiep, chen them cac diem STICKER cach deu (<=7s) lap DAY khe — day la
     lop ②, dung picto co san, xoay vong tranh lap lien 2 lan.
  4. Xuat lai project.json + in bao cao ①②③ tach rieng (dung triet ly cua
     `_media_library/check_frame_pace.py`, nhung do truc tiep tren schema
     trk-slides/trk-overlay cua remotion-vox thay vi trk-hero/sceneMarkers).

⛔ KHONG bat (feedback_video_no_motion_mot_giong + audience-45plus §2):
   idle.amp>0 · wobble/punch/spiral · motion pan · SFX rai theo scene.

⚠️ CHUA CHAY DUOC — project.json cua video 22 CHUA TON TAI (can anh AI da gen
+ ingest_slides_22.py + import_pipeline.py truoc). Script nay da viet xong va
SAN SANG, nhung LOI DUY NHAT o thoi diem viet la du lieu dau vao chua co —
dung tin bat ky con so nao trong docstring nay la "da chay that".
"""
import io
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
STEM = "22_ramen-kekkan"
PROJ = ROOT / "projects" / STEM / "project.json"
PUB = ROOT / "public" / "projects" / STEM / "assets"
PICTO_SRC = ROOT / "public" / "projects" / "shokutaku-16-banana" / "assets"
FPS = 30
MAX_GAP_S = 7.0          # san su kien — user chot 2026-08-30
MAX_HERO_PER_MIN = 6.0   # tran doi hero — audience-45plus.md §2 muc 1

# picto co san, xoay vong lam su kien LAP DAY khong can chu (san 7s)
PICTOS = ["ex_hatena", "ex_hirameki", "ex_hiyari", "ex_mukumi", "ex_furatsuki"]

# (chuoi can KHOP trong phu de, tag chu, mau) — chi dat o dung cau CO SO/KET
# LUAN THAT trong loi doc, KHONG bia. Dat truoc, phan con lai lap bang picto.
TAGS = [
    ("一日分の目安を、超えて",     "1日分超え",   "#FFD700"),
    ("硬く、もろくなって",         "管が硬く",     "#FFD700"),
    ("ろくグラムからはちグラム",   "6〜8g",        "#FFD700"),
    ("半分だけ残して",             "汁は半分",     "#FFD700"),
    ("動脈硬化につながる",         "動脈硬化",     "#FFD700"),
    ("サビのようなものができて",   "血管のサビ",   "#FFD700"),
    ("硬くする塩、詰まらせる脂",   "3つの場面",    "#FFD700"),
    ("汁は、半分で大丈夫です",     "ひと言",       "#FFD700"),
]
TAG_XY = (330, 745)
PICTO_XY = (56, 148)
PICTO_H_MAX = 320
PICTO_W_MAX = 200


def split_long_cues(caps, max_chars=46):
    """Tach cue phu de DAI thanh nhieu cue ngan — cat o dau cau tieng Nhat."""
    out = []
    for ln in caps.get("lines", []):
        txt = ln["text"]
        if len(txt) <= max_chars:
            out.append(ln)
            continue
        parts, cur = [], ""
        for tok in re.split(r"(?<=[。、」！？])", txt):
            if not tok:
                continue
            if cur and len(cur) + len(tok) > max_chars:
                parts.append(cur)
                cur = tok
            else:
                cur += tok
        if cur:
            parts.append(cur)
        if len(parts) < 2:
            out.append(ln)
            continue
        total = sum(len(x) for x in parts)
        t0, span = ln["startMs"], ln["endMs"] - ln["startMs"]
        acc = 0
        for x in parts:
            s = t0 + span * acc / total
            acc += len(x)
            out.append({"text": x, "startMs": round(s),
                        "endMs": round(t0 + span * acc / total)})
    caps["lines"] = out

    for w in caps.get("words", []):
        mid = (w["startMs"] + w["endMs"]) / 2
        w["lineIndex"] = next((i for i, l in enumerate(out)
                               if l["startMs"] <= mid <= l["endMs"]), 0)


def find_tag_frames(caps, fps):
    """Khop tung TAGS[i][0] vao đúng 1 dong phu de -> tra ve frame bat dau."""
    out, missing, ambiguous = [], [], []
    for needle, text, color in TAGS:
        hits = [l for l in caps["lines"] if needle in l["text"]]
        if not hits:
            missing.append(needle)
            continue
        if len(hits) > 1:
            ambiguous.append(needle)
        frame = round(hits[0]["startMs"] / 1000 * fps)
        out.append((frame, text, color))
    return out, missing, ambiguous


def main():
    if not PROJ.exists():
        print(f"CHUA CO {PROJ.relative_to(ROOT)} — can chay xong "
              f"ingest_slides_22.py + import_pipeline.py truoc. Dung chay script nay som.")
        return 2

    p = json.loads(PROJ.read_text(encoding="utf-8"))
    fps = p.get("fps", FPS)
    dur = p["timeline"]["durationInFrames"]
    slides = next(t for t in p["tracks"] if t["id"] == "trk-slides")

    # ── WIPE thay pan (giong video 18/20/21) ──
    for i, c in enumerate(slides["clips"]):
        c["motion"] = "none"
        c["fadeInFrames"] = 0
        c["wipeInFrames"] = 0 if i == 0 else 14
        c["wipeDir"] = ("left", "up", "right", "down")[i % 4]

    # ── KARAOKE ──
    p["captions"]["style"] = "karaoke"
    p["captions"]["source"] = "voicevox-mora"
    p["captions"]["fontSize"] = 38
    split_long_cues(p["captions"], max_chars=46)

    # ── ① moc HERO (khong dung toi — day la tran, khong phai san) ──
    hero_frames = sorted(c["from"] for c in slides["clips"])
    hero_per_min = len(hero_frames) / (dur / fps / 60)

    # ── tag chu CO Y NGHIA, khop bang chuoi that trong phu de ──
    tag_hits, missing, ambiguous = find_tag_frames(p["captions"], fps)
    if missing:
        print("🔴 KHONG khop duoc cac TAGS sau (loi thoai da doi ma quen sua tag):")
        for m in missing:
            print("   -", m)
    if ambiguous:
        print("⚠️ TAGS khop NHIEU dong (dung dong DAU TIEN, kiem tra lai neu sai):")
        for m in ambiguous:
            print("   -", m)

    # ── gop moc, chen picto lap day khe > 7s (② san su kien) ──
    seed = sorted(set(hero_frames) | {f for f, *_ in tag_hits} | {0})
    fill_frames = []
    max_gap_f = MAX_GAP_S * fps
    for a, b in zip(seed, seed[1:] + [dur]):
        gap = b - a
        if gap <= max_gap_f:
            continue
        n_fill = int(gap // max_gap_f)  # so diem chen de moi khe con lai <=7s
        step = gap / (n_fill + 1)
        for k in range(1, n_fill + 1):
            fill_frames.append(round(a + step * k))

    clips = []
    # tag chu
    for frame, text, color in tag_hits:
        dur_f = min(150, 90)
        clips.append({
            "id": f"tx-{frame}", "kind": "text", "from": frame,
            "durationInFrames": dur_f, "content": text, "preset": "tag",
            "color": color, "animation": "pop", "animationParams": {},
            "layout": {"x": TAG_XY[0], "y": TAG_XY[1], "rotation": -2},
            "fontSize": 56,
        })
    # picto lap day san 7s, xoay vong tranh lap lien 2 lan
    prev_picto = None
    need_picto = set()
    for i, frame in enumerate(sorted(fill_frames)):
        choices = [x for x in PICTOS if x != prev_picto] or PICTOS
        picto = choices[i % len(choices)]
        prev_picto = picto
        need_picto.add(picto)
        img = PICTO_SRC / f"{picto}.png"
        pw, ph = Image.open(img).size if img.exists() else (200, 200)
        w = max(60, min(PICTO_W_MAX, int(round(PICTO_H_MAX * pw / ph))))
        dur_f = min(90, max(30, round(1.5 * fps)))
        clips.append({
            "id": f"st-{frame}", "kind": "sticker", "from": frame,
            "durationInFrames": dur_f, "asset": f"assets/{picto}.png",
            "layout": {"x": PICTO_XY[0], "y": PICTO_XY[1], "w": w, "rotation": -6},
            "entrance": {"variant": "peel", "delayFrames": 0, "params": {}},
            "exit": {"variant": "fade", "delayFrames": 0, "params": {}},
            "idle": {"amp": 0, "phase": 0},
            "shadow": "lg",
        })

    # ── WATERMARK — chay SUOT video (Remotion khong tu dan) ──
    clips.insert(0, {
        "id": "wm", "kind": "text", "from": 0, "durationInFrames": dur,
        "content": "60代の食卓", "preset": "tag", "color": "#FFD24A",
        "animation": "none", "animationParams": {},
        "layout": {"x": 1586, "y": 40, "rotation": 0}, "fontSize": 40,
    })

    p["tracks"] = [t for t in p["tracks"] if t["id"] != "trk-overlay"]
    p["tracks"].append({"id": "trk-overlay", "name": "Overlay", "type": "sticker",
                        "muted": False, "hidden": False, "locked": False,
                        "clips": clips})

    PUB.mkdir(parents=True, exist_ok=True)
    for name in sorted(need_picto):
        src = PICTO_SRC / f"{name}.png"
        if src.exists():
            shutil.copy2(src, PUB / f"{name}.png")
        else:
            print(f"  🔴 THIEU pictogram {name}.png")

    PROJ.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── BAO CAO — ①②③ tach rieng, khong gop thanh 1 con so ──
    all_events = sorted(hero_frames + [f for f, *_ in tag_hits] + fill_frames)
    gaps = [(b - a) / fps for a, b in zip(all_events, all_events[1:] + [dur])]
    mins = dur / fps / 60
    print(f"OK — {len(clips)} overlay clip: {len(tag_hits)} tag chu + "
          f"{len(fill_frames)} picto lap ({len(need_picto)} hinh khac nhau)")
    print(f"① TRAN doi HERO      : {hero_per_min:5.2f}/phut  "
          f"(tran {MAX_HERO_PER_MIN:.0f} — {'✅' if hero_per_min <= MAX_HERO_PER_MIN else '🔴 VUOT'})")
    print(f"② SAN su kien (<=7s) : khe dai nhat {max(gaps):.1f}s  "
          f"({'✅ sach' if max(gaps) <= MAX_GAP_S + 0.05 else '🔴 con khe qua 7s'})")
    print(f"   tong su kien (hero+tag+picto) = {len(all_events)} / {mins:.1f} phut "
          f"= {len(all_events)/mins:.2f}/phut")
    print(f"karaoke ON · wipe 14f · motion none")


if __name__ == "__main__":
    sys.exit(main())
