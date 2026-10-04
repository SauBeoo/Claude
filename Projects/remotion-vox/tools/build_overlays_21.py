# -*- coding: utf-8 -*-
r"""Rai lop DONG cho video 21 (shokutaku, もち麦 × もう一つの台所) — cung muc hieu ung
da duyet o video 18/20 (karaoke sub + wipe 14 frame + tag pop + pictogram peel).

    py -3 tools\build_overlays_21.py

⛔ KHONG bat (feedback_video_no_motion_mot_giong + audience-45plus §2):
   idle.amp>0 · wobble/punch/spiral · motion pan · SFX rai theo scene.

MAT DO: 48 slide / ~16'13 => co the them toi ~50 overlay ma van duoi tran 6,0/phut
(audience-45plus §2). Chi dung 13 (7 tag + 8 picto = mot vai slide co ca hai) —
uu tien DAT DUNG DINH DOAN hon la lap day tran.
"""
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
STEM = "21_mochimugi-choukatsu"
PROJ = ROOT / "projects" / STEM / "project.json"
PUB = ROOT / "public" / "projects" / STEM / "assets"
PICTO_SRC = ROOT / "public" / "projects" / "shokutaku-16-banana" / "assets"
FPS = 30

# (slide_idx, text tag hoac None, pictogram hoac None)
# Tag = con so / y chot CO THAT trong loi doan do (YMYL: khong bia so len hinh).
# Uu tien dat tag o slide CHUA co chu bake san (14 slide da co chu — xem
# slide_prompts_BLOCKS.md — khong nhet them tag len do, se roi mat).
PLAN = [
    (0,  None,             "ex_hatena"),      # co dau: nghich ly can nang
    (1,  "誰も知らない台所", None),            # "誰も、教えてくれなかった台所です"
    (4,  None,              "ex_hirameki"),   # ITEM1: dai trang = hanh lang bep
    (8,  "壁を修理する",     None),            # co che sua chua thanh ruot
    (16, "続けやすさが力",   None),            # みのり tu thu — ket luan
    (18, "免疫にも関係",     "ex_hirameki"),   # ket noi mien dich
    (21, None,               "ex_zzz"),       # chieu buon ngu — duong huyet
    (26, "軽くなった",       None),            # 恵子さん nhe nguoi
    (28, "腎臓・お薬の方へ", "ex_hiyari"),     # canh bao than
    (30, "1週間で挫折",     "ex_hiyari"),      # NG habit — van de
    (33, "答えは食べ過ぎ",   "ex_hirameki"),   # TRA LOOP
    (41, "冬でも風邪なし",   None),            # 正雄さん khep vong
    (42, None,               "ex_hirameki"),  # cua bep mo, ket thuc tich cuc
]
# Vi tri — GIONG HET video 20 (cung khung san khau, cung geometry the/cast):
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


def main():
    p = json.loads(PROJ.read_text(encoding="utf-8"))
    slides = next(t for t in p["tracks"] if t["id"] == "trk-slides")
    by_idx = {}
    for c in slides["clips"]:
        i = int(Path(c["asset"]).stem.split("_")[1])
        by_idx[i] = c

    # ── WIPE thay pan
    for i, c in enumerate(slides["clips"]):
        c["motion"] = "none"
        c["fadeInFrames"] = 0
        c["wipeInFrames"] = 0 if i == 0 else 14
        c["wipeDir"] = ("left", "up", "right", "down")[i % 4]

    # ── KARAOKE
    p["captions"]["style"] = "karaoke"
    p["captions"]["source"] = "voicevox-mora"
    p["captions"]["fontSize"] = 38
    split_long_cues(p["captions"], max_chars=46)

    # ── overlay
    clips, need_picto, skipped = [], set(), []
    for idx, tag, picto in PLAN:
        c = by_idx.get(idx)
        if c is None:
            skipped.append(idx)
            continue
        base, dur = c["from"], c["durationInFrames"]
        if tag:
            clips.append({
                "id": f"tx-{idx}", "kind": "text", "from": base + 12,
                "durationInFrames": min(150, max(45, dur - 20)),
                "content": tag, "preset": "tag", "color": "#FFD700",
                "animation": "pop", "animationParams": {},
                "layout": {"x": TAG_XY[0], "y": TAG_XY[1], "rotation": -2},
                "fontSize": 56,
            })
        if picto:
            pw, ph = Image.open(PICTO_SRC / f"{picto}.png").size
            w = max(60, min(PICTO_W_MAX, int(round(PICTO_H_MAX * pw / ph))))
            clips.append({
                "id": f"st-{idx}", "kind": "sticker", "from": base + 45,
                "durationInFrames": min(120, max(40, dur - 55)),
                "asset": f"assets/{picto}.png",
                "layout": {"x": PICTO_XY[0], "y": PICTO_XY[1], "w": w,
                           "rotation": -8},
                "entrance": {"variant": "peel", "delayFrames": 0, "params": {}},
                "exit": {"variant": "fade", "delayFrames": 0, "params": {}},
                "idle": {"amp": 0, "phase": 0},
                "shadow": "lg",
            })
            need_picto.add(picto)

    # ── WATERMARK — chay SUOT video (Remotion khong tu dan)
    clips.insert(0, {
        "id": "wm", "kind": "text", "from": 0,
        "durationInFrames": p["timeline"]["durationInFrames"],
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

    tags = sum(1 for c in clips if c["kind"] == "text" and c["id"] != "wm")
    pics = sum(1 for c in clips if c["kind"] == "sticker")
    events = [c for c in clips if c["durationInFrames"] < p["timeline"]["durationInFrames"]]
    total_ev = len(slides["clips"]) + len(events)
    mins = p["timeline"]["durationInFrames"] / FPS / 60
    print(f"OK — overlay {len(clips)} clip: {tags} tag + {pics} pictogram "
          f"({len(need_picto)} hinh khac nhau)")
    caps = p["captions"]
    longest = max((len(l["text"]) for l in caps["lines"]), default=0)
    over = sum(1 for l in caps["lines"] if len(l["text"]) > 46)
    print(f"   karaoke ON · wipe 14f tren {len(slides['clips'])-1} ranh gioi · motion none")
    print(f"   phu de: {len(caps['lines'])} cue · dai nhat {longest} ky · "
          f"{'✅ 0 cue qua 46 ky' if not over else f'🔴 {over} cue >46 ky'}")
    print(f"   mat do: ({len(slides['clips'])} slide + {len(events)} overlay co thoi han)"
          f" / {mins:.1f} phut = {total_ev/mins:.1f} su kien/phut  (tran 6,0 — 45plus §2)"
          f"  [+1 lop chay suot: watermark]")
    if skipped:
        print(f"   ⚠️ bo qua slide idx khong co: {skipped}")


if __name__ == "__main__":
    main()
