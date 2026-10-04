# -*- coding: utf-8 -*-
r"""build_remotion_19real.py — BAN NGUOI THAT (photoreal) cua video 19.

Copy tu `build_remotion_19vox.py`, doi DUNG BA CHO theo bai hoc do duoc 2026-09-03:
  (1) **speed toi da 1.0** — khong bao gio ep nhanh (ban vox dat toi 1,25x o 7 scene,
      tuc day nguoi xem toi phan clip loang nhanh hon 25%; do duoc: nua sau clip tut
      15,1% chi tiet hinh, nang nhat 41,3%). Scene ngan hon clip thi CAT DUOI.
  (2) **dissolve 0,60s / 0,80s** thay cho 0,30s / 0,40s — user: *"hieu ung muot ma
      chuyen canh nhu dien anh"*. Prompt real da bat moi clip mo/dong bang khung TINH
      nen dissolve dai khong lam nhoe.
  (3) asset `rclip19_*` (lo photoreal) thay `clip19_*` (lo collage).
Moi thu khac giu nguyen: bang so, the 原典, banner, punch, phu de, voice, BGM.

(ban goc:) BAN VOX cua video 19: clip AI full-bleed + bang so + 原典.

User chot 2026-09-03: *"F:\Youtube\Du_an_moi_7_qnpzs39n cac video o day nhe. Dung
video cho tao va van muon co cac frame so lieu voi frame screen shot nhe"*, va
chon **"Nen collage, bo cast (dong bo)"** cho scene bang so + screenshot.

KHAC ban `build_remotion_19.py` (dang chay tren kenh) o DUNG BA CHO:
  (1) scene co anh  -> **CLIP VIDEO AI full-bleed** (74 clip Veo da crop watermark)
                       thay cho photocard hero + sticker.
  (2) **BO 2 CAST** o moi scene -> khong con trk-cast-l/r. Ca video mot ngon ngu hinh.
  (3) bang so (`papercut-stat`/`papercut-formula`) va the 原典 **GIU NGUYEN** —
      day la thu user noi "van muon co".
Moi thu khac (timeline, phu de, BGM, SFX, punch, tag) di theo ban 19.

⚖️ CAI GIA da biet truoc khi bo cast: 2 cast モニター la ban sac kenh (CLAUDE.md §②).
   Doi lai: het canh doi qua doi lai giua full-bleed collage va khung co cast 29 lan.
   User da can va chon.

📐 CHIA GIAY CHO CLIP — moi clip Veo dai **dung 8,000s**, nhung scene can `per = d/N`
   giay (min 4,98 · median 7,30 · max 9,00).
   · Khop chinh xac bang `speed` thi 10 clip phai chay >1,3x (max 1,61x) => gap gap,
     pha chat calm cua tep 45+.
   · Nen dung **speed = clamp(8/per, 0.85, 1.25)**, phan du CAT DUOI.
     Khong bao gio gap gap; clip ngan nhat mat ~2s duoi (phan "dung yen" cua prompt
     CLOSE) — chap nhan duoc vi chuyen dong chinh nam o dau clip.

🔴 WATERMARK: clip nguon co chu "Veo" goc duoi-phai (x 1865..1895 · y 1042..1055,
   do 16/16 lan). `tools/ingest_aiclips_19.py` crop 1856x1044 -> scale 1920x1080.
   Builder nay DOC clip da crop, khong doc file goc.

CHAY:  python tools/build_remotion_19vox.py
"""
import io
import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
RV = Path(r"E:\Claude\Projects\remotion-vox")
STEM = "19_kounenrei-koyou-keizoku-kyufu"
NAME = "nenkin-19real"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#E0A32A"

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
import channels  # noqa: E402
from _scenes19 import SCENES, STAT, FORMULA, PUNCH  # noqa: E402

_CH = channels.CHANNELS["nenkin"]
BGM_SRC = (PROJ / _CH["bgm"]).resolve()
BGM_VOL = 10 ** (float(_CH["bgm_gain"]) / 20)          # −40 dB -> 0.01
SFX = {42: ("sfx/thud.wav", 0.30), 60: ("sfx/paper.wav", 0.35), 90: ("sfx/drop.wav", 0.30)}

VD = PROJ / "06_VIDEO" / STEM
CLIP_LEN = 8.0                  # moi clip Veo dai dung 8,000s
SPEED_LO, SPEED_HI = 0.85, 1.25  # tran gian/nen — ngoai dai thi cat duoi
# ⭐ DIEN ANH (user chot 2026-09-03: "hieu ung muot ma chuyen canh nhu dien anh")
# Ban collage dung 9/12 frame (0,3/0,4s). Ban real day len 0,6/0,8s — prompt da
# bat moi clip "mo/dong bang mot khung TINH" nen dissolve dai khong lam nhoe.
FADE = 18                       # 0,60s dissolve giua cac clip trong scene
FADE_SCENE = 24                 # 0,80s o dau scene

# bang so: GIU nguyen hop cua ban 19 (da qua gate + duyet mat). Tam 962 = giua khung.
TBL_X, TBL_W = 474, 976
# the 原典: anh screenshot, phai DOC DUOC chu -> contain trong hop giua khung
GEN_X, GEN_Y, GEN_W, GEN_H = 300, 130, 1320, 760

# 🔴 NEN CHO SCENE BANG SO — soi frame probe (2026-09-03) thay 13 scene bang
# (296s = 33% video) la NEN TRONG HOAC: bo cast xong thi khong con gi o 2 mep,
# bang nam nua tren, nua duoi trong hoac. Dung cai `audience-45plus.md` §2.0c
# ket an ("noi voi nen trong").
# Chua bang: dat clip AI cua scene ANH GAN NHAT TRUOC DO lam NEN, lam mo manh
# + ha sang => co chuyen dong, dong bo ngon ngu hinh, ma khong tranh chap voi so.
# ⚠️ Day KHONG pham luat "khong trung anh trong cung video"
# (`feedback_slide_khong_trung_anh_trong_video`): o muc blur nay nguoi xem khong
# doc ra noi dung anh, no chi con la mang mau chuyen dong. Va ve NGHIA no dung —
# bang so luon dang noi ve chinh canh vua xem.
# soi frame 2026-09-03: bland brightness 0.62 lam nhan chu navy bi chim o cho
# nen toi. Nen phai SANG + PHANG (contrast thap) chu khong phai TOI — chu cua
# bang la navy dam, no noi tren nen sang.
# (giu lai lam ho so quy doi — phep mo nay nay do ffmpeg lam, xem make_bgblur_19.py)
BLUR_BG = {"blur": 24, "brightness": 1.18, "saturate": 0.30, "contrast": 0.55}


# ══ phu de: Remotion KHONG tu che khoi (bai hoc CLAUDE.md §②) ══════════════
def split_caption(line, cap=78):
    """Che khoi >cap ky, cat SAU dau cau, chia giay theo ti le ky tu.

    ⚠️ `timeline.json` dung `start`/`end` (GIAY); `captions.lines` cua Remotion
    dung `startMs`/`endMs` (MILI-giay) — doi don vi ngay tai day, dung de lech
    (CLAUDE.md §② canh bao dung suy schema tu project mau).
    """
    t = line["text"]
    ms0, ms1 = round(line["start"] * 1000), round(line["end"] * 1000)
    if len(t) <= cap:
        return [{"text": t, "startMs": ms0, "endMs": ms1}]
    out, cur, parts = [], "", []
    for ch in t:
        cur += ch
        if ch in "。、」）" and len(cur) >= cap * 0.55:
            parts.append(cur)
            cur = ""
    if cur:
        parts.append(cur)
    # gop lai cho khong khoi nao vuot cap
    merged, buf = [], ""
    for p in parts:
        if len(buf) + len(p) <= cap:
            buf += p
        else:
            if buf:
                merged.append(buf)
            buf = p
    if buf:
        merged.append(buf)
    if not merged:
        merged = [t[i:i + cap] for i in range(0, len(t), cap)]
    tot = sum(len(x) for x in merged)
    a, span = ms0, ms1 - ms0
    for x in merged:
        d = round(span * len(x) / tot)
        out.append({"text": x, "startMs": a, "endMs": a + d})
        a += d
    out[-1]["endMs"] = ms1
    return out


def bgm_clips(dur, ln):
    """BGM lap lai cho het video."""
    out, f, i = [], 0, 0
    while f < dur:
        out.append({"id": f"bgm-{i}", "kind": "audio", "from": f,
                    "durationInFrames": min(ln, dur - f), "asset": "assets/bgm.mp3",
                    "volume": BGM_VOL, "trimStartFrames": 0})
        f += ln
        i += 1
    return out


def T(tid, name, typ, clips):
    return {"id": tid, "name": name, "type": typ, "clips": clips}


def main():
    tl = json.load(io.open(VD / "timeline.json", encoding="utf-8"))
    lines, TOT = tl["lines"], tl["total"]
    DUR = math.ceil(TOT * FPS)

    def f_at(sec):
        return max(0, min(DUR, round(sec * FPS)))

    ad = RV / "public" / "projects" / NAME / "assets"
    ad.mkdir(parents=True, exist_ok=True)

    bg, vid, stat, formula, tag, punch, sfx = [], [], [], [], [], [], []
    n_ai = n_gen = n_tbl = 0
    slow = []
    last_ai = [None]   # clip AI gan nhat — dung lam nen mo cho scene bang
    n_bgv = [0]

    for k, s in enumerate(SCENES):
        a = lines[s["L"]]["start"]
        b = lines[SCENES[k + 1]["L"]]["start"] if k + 1 < len(SCENES) else TOT
        f, to = f_at(a), f_at(b)
        d = to - f
        if d <= 0:
            continue

        # ── nen collage (moi scene mot cap splash) ────────────────────────
        sp = s.get("sp") or ["#C87A72", "#8A93A8"]
        bg.append({"id": f"bg-{k}", "kind": "background", "from": f,
                   "durationInFrames": d, "paper": "assets/paper.jpg",
                   "tint": "#F2EDE4", "tintOpacity": 0.55, "grid": True,
                   "dots": True, "splash": list(sp)})

        # ── banner tag ────────────────────────────────────────────────────
        if s.get("tag"):
            tag.append({"id": f"tag-{k}", "kind": "text", "from": f + 4,
                        "durationInFrames": max(1, d - 4), "content": s["tag"],
                        "preset": "papercut-banner", "color": INK,
                        "animation": "pop", "animationParams": {"restDeg": -1.5},
                        "layout": {"x": 74, "y": 58}, "fontSize": 64})

        heroes = s.get("heroes") or ([s["hero"]] if s.get("hero") else [])
        gen = [h for h in heroes if h.startswith("card_genten")]
        ai = [h for h in heroes if not h.startswith("card_genten")]

        # scene BANG (khong anh, khong 原典) -> nen mo bang clip AI gan nhat truoc
        if not ai and not gen and last_ai[0]:
            vid.append({
                "id": f"bgv-{k}", "kind": "video", "from": f,
                "durationInFrames": d,
                # 🔴 dung file DA MO SAN (tools/make_bgblur_19.py), KHONG dung
                # CSS filter: `blur(24px)` tren OffthreadVideo full-screen lam
                # Chrome treo => delayRender timeout + kill EPERM, render chet o
                # frame 2765 sau 10% cua mot luot 1h45 (2026-09-03).
                "asset": f"assets/bgblur_rclip19_{last_ai[0]}.mp4",
                "trimStartFrames": 0, "fit": "cover", "layout": {},
                "motion": "none", "speed": 0.85, "mirror": False, "volume": 0,
                "fadeInFrames": FADE_SCENE, "wipeInFrames": 0, "wipeDir": "left",
                "filter": {}})
            n_bgv[0] += 1

        # ── (A) scene ANH -> clip AI full-bleed ───────────────────────────
        if ai:
            n_ai += len(ai)
            per = (b - a) / len(ai)
            # 🔴 BAN REAL: **KHONG BAO GIO speed > 1** (do duoc: nua sau clip tut
            # 15,1% chi tiet, ep nhanh la day nguoi xem toi phan loang nhanh hon).
            # Chi cho phep GIAN (speed < 1) khi scene dai hon clip; con lai cat duoi.
            speed = min(1.0, max(SPEED_LO, CLIP_LEN / per))
            if speed <= SPEED_LO + 1e-9:
                slow.append((s["tag"], round(per, 2), round(speed, 3)))
            for j, h in enumerate(ai):
                cf = f_at(a + per * j)
                ct = f_at(a + per * (j + 1)) if j + 1 < len(ai) else to
                vid.append({
                    "id": f"ai-{k}-{j}", "kind": "video", "from": cf,
                    "durationInFrames": max(1, ct - cf),
                    "asset": f"assets/rclip19_{h.replace('card_19_', '')}.mp4",
                    "trimStartFrames": 0, "fit": "cover", "layout": {},
                    "motion": "none", "speed": round(speed, 3), "mirror": False,
                    "volume": 0,
                    "fadeInFrames": FADE_SCENE if j == 0 else FADE,
                    "wipeInFrames": 0, "wipeDir": "left", "filter": {}})
            last_ai[0] = ai[-1].replace("card_19_", "")

        # ── (B) scene 原典 -> screenshot, contain trong hop giua ──────────
        if gen:
            n_gen += len(gen)
            per = (b - a) / len(gen)
            for j, h in enumerate(gen):
                cf = f_at(a + per * j)
                ct = f_at(a + per * (j + 1)) if j + 1 < len(gen) else to
                vid.append({
                    "id": f"gen-{k}-{j}", "kind": "video", "from": cf,
                    "durationInFrames": max(1, ct - cf),
                    "asset": f"assets/{h}.png", "trimStartFrames": 0,
                    "fit": "contain",
                    "layout": {"x": GEN_X, "y": GEN_Y, "w": GEN_W, "h": GEN_H},
                    "motion": "none", "speed": 1, "mirror": False, "volume": 0,
                    "fadeInFrames": FADE_SCENE if j == 0 else FADE,
                    "wipeInFrames": 0, "wipeDir": "left", "filter": {}})

        # ── (C) bang so lieu / cong thuc ──────────────────────────────────
        if s.get("stat"):
            n_tbl += 1
            body, size = STAT[s["stat"]]
            f_st = f + min(60, max(20, int(0.10 * d)))   # tran 2s (§2.0d)
            stat.append({"id": f"st-{k}", "kind": "text", "from": f_st,
                         "durationInFrames": max(1, to - f_st - 4), "content": body,
                         "preset": "papercut-stat", "color": AMBER,
                         "animation": "pop", "animationParams": {"restDeg": -1.5},
                         "layout": {"x": TBL_X, "y": 300, "w": TBL_W},
                         "fontSize": size})
        if s.get("formula"):
            n_tbl += 1
            body, size = FORMULA[s["formula"]]
            f_fm = f + min(60, max(20, int(0.10 * d)))
            formula.append({"id": f"fm-{k}", "kind": "text", "from": f_fm,
                            "durationInFrames": max(1, to - f_fm - 4), "content": body,
                            "preset": "papercut-formula", "color": AMBER,
                            "animation": "pop", "animationParams": {"restDeg": -1.5},
                            "layout": {"x": TBL_X, "y": 330, "w": TBL_W},
                            "fontSize": size})

        # ── (D) SFX o 3 dinh bai ──────────────────────────────────────────
        if s["L"] in SFX:
            asset, vol = SFX[s["L"]]
            sfx.append({"id": f"sfx-{k}", "kind": "audio", "from": f,
                        "durationInFrames": min(60, d), "asset": asset,
                        "volume": vol, "trimStartFrames": 0})

    # ── punch (dai giay chot doan), khoa theo chi so dong L ──────────────
    for i, (L, text, col) in enumerate(PUNCH):
        if L >= len(lines):
            continue
        pf = f_at(lines[L]["start"])
        pd = f_at(lines[min(L + 1, len(lines) - 1)]["start"]) - pf
        punch.append({"id": f"pn-{i}", "kind": "text", "from": pf + 6,
                      "durationInFrames": max(20, pd - 6), "content": text,
                      "preset": "papercut-punch", "color": col,
                      "animation": "pop", "animationParams": {"restDeg": 1.2},
                      "layout": {"x": 90, "y": 858}, "fontSize": 52})

    # ── phu de ───────────────────────────────────────────────────────────
    caps = []
    for ln in lines:
        caps += split_caption(ln)
    over = [c for c in caps if len(c["text"]) > 78]

    tracks = [
        T("trk-bg", "nen collage", "background", bg),
        T("trk-video", "clip AI + 原典", "video", vid),
        T("trk-stat", "bang so lieu", "text", stat),
        T("trk-formula", "cong thuc", "text", formula),
        T("trk-tag", "banner tag", "text", tag),
        T("trk-punch", "punch", "text", punch),
        T("trk-voice", "giong doc", "audio", [
            {"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
             "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]),
        T("trk-sfx", "SFX", "audio", sfx),
        T("trk-bgm", "BGM -40dB", "audio", bgm_clips(DUR, 10914)),
    ]

    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": "nenkin",
                 "fps": FPS, "width": 1920, "height": 1080,
                 "createdAt": "2026-09-03T00:00:00.000Z",
                 "modifiedAt": "2026-09-03T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        # ⚠️ SceneMarkerSchema doi CA `id` — thieu la Remotion tu choi ca project
        # ("sceneMarkers.0.id: Invalid input"), khong render duoc mot frame nao.
        "sceneMarkers": [{"id": f"sc-{i}", "atFrame": f_at(lines[s["L"]]["start"]),
                          "label": s.get("tag", "")} for i, s in enumerate(SCENES)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline",
                     "enabled": True, "fontSize": 44, "lines": caps, "words": []},
        # theme: chep tu ban 19 da render duoc — `canvasColor` kem la nen giay
        # cua kenh; de {} thi Remotion lay mac dinh khac (xanh navy).
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }

    out = RV / "projects" / NAME
    out.mkdir(parents=True, exist_ok=True)
    (out / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    # ── assets ───────────────────────────────────────────────────────────
    for p in (VD / "photocard").glob("card_genten19_*.png"):
        if not (ad / p.name).exists():
            shutil.copy(p, ad / p.name)
    voice, mp3 = VD / "voice_full.wav", ad / "voice.mp3"
    if voice.exists() and not mp3.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(voice),
                        "-b:a", "192k", str(mp3)], check=True)
    if not (ad / "bgm.mp3").exists():
        shutil.copy(BGM_SRC, ad / "bgm.mp3")
    paper = RV / "public" / "projects" / "nenkin-17-demo" / "assets" / "paper.jpg"
    if paper.exists() and not (ad / "paper.jpg").exists():
        shutil.copy(paper, ad / "paper.jpg")

    # ── GATE ─────────────────────────────────────────────────────────────
    want = {c["asset"].split("/")[-1] for t in tracks if t["type"] == "video"
            for c in t["clips"]} | {"paper.jpg", "voice.mp3", "bgm.mp3"}
    miss = sorted(w for w in want if not (ad / w).exists())

    print(f"OK  {NAME}  {DUR} frame = {DUR / FPS:.1f}s  ({len(SCENES)} scene)")
    print(f"   clip AI {n_ai} · the 原典 {n_gen} · bang so {n_tbl} "
          f"(nen mo {n_bgv[0]}) · tag {len(tag)} · punch {len(punch)} · sfx {len(sfx)}")
    print(f"   phu de {len(caps)} khoi (tu {len(lines)} dong)")
    if slow:
        print(f"   ⓘ {len(slow)} scene cham tran speed (cat duoi/gian het co): "
              + ", ".join(f"{t} per={p}s sp={q}" for t, p, q in slow[:5]))
    if over:
        print(f"🔴 {len(over)} khoi phu de > 78 ky — chua che het")
        sys.exit(1)
    if miss:
        print(f"🔴 THIEU {len(miss)} asset: {', '.join(miss[:8])}")
        sys.exit(1)
    print(f"   asset OK ({len(want)} file) -> {ad}")
    print(f"   -> {out / 'project.json'}")


if __name__ == "__main__":
    main()
