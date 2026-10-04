# -*- coding: utf-8 -*-
r"""Dung ban DEMO 30 giay cho video 18 (shokutaku) — de user duyet HIEU UNG truoc khi chot.

    py -3 tools\make_demo_18.py                 # tao projects/18-demo/project.json
    npx remotion render VoxProject --props=projects/18-demo/project.json out/18-demo.mp4 --overwrite

VI SAO CO FILE NAY: user *"tao muon cac hieu ung nhu video remotion-vox co ma. May ren demo
cho tao doan truoc khi chot di"*. Render ca video la ~70 phut; 900 frame chi ~1,5 phut.

⚖️ MUC HIEU UNG CHON CHO DEMO — co chu y, KHONG bat het:
Video 16 cua chinh kenh nay da chay qua remotion-vox va CO Y TAT gan het (idle.amp=0 moi
sticker, chi 'rise' cham, 5 phan tu cho 23 phut) vi hai rang buoc con hieu luc:
  · feedback_video_no_motion_mot_giong — user GHET rung / Ken Burns
  · audience-45plus.md §2 — <=6 doi hinh/phut, dissolve >=0,4s, SFX <=1 chum/5 phut
=> Demo nay bat 4 thu DONG MA KHONG RUNG, moi thu deu doc duoc o 45+:
  ① KARAOKE phu de word-level (tu dang doc doi vang) — thu "vox" nhat, mien phi (mora VOICEVOX)
  ② WIPE tuyen tinh thay dissolve o ranh gioi slide (dong ma khung khong xe dich)
  ③ TEXT tag 'pop' cho con so dat nhat cua doan (一万回)
  ④ PICTOGRAM cat giay 'peel' (ban le canh tren, dung chat giay dan) o dinh cam xuc
KHONG bat: idle.amp>0 · wobble/punch/spiral · motion pan · SFX rai theo scene.
Ba thu do doi user gat rieng (chung dam vao dung 2 rang buoc tren).
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "projects" / "18_ringo-tabekata" / "project.json"
DST_DIR = ROOT / "projects" / "18-demo"
PUB_SRC = ROOT / "public" / "projects" / "18_ringo-tabekata"
PUB_DST = ROOT / "public" / "projects" / "18-demo"
FPS = 30
DEMO_FRAMES = 900                      # 30 giay
# Bo pictogram cat giay cua video 16, TAI DUNG (khong ton luot gen anh — chung do bang PIL:
# ex_furatsuki / ex_hatena / ex_hirameki / ex_hiyari / ex_itami / ex_mukumi / ex_zzz).
# Cold open bai nay la STAKE (1万回 坂道 · mach mau mat/than) => 'hiyari' (het hon) khop nhat.
PICTO = "ex_hiyari.png"


def main():
    p = json.loads(SRC.read_text(encoding="utf-8"))
    p["meta"] = {**p["meta"], "name": "18-demo"}
    p["timeline"]["durationInFrames"] = DEMO_FRAMES

    # ── 1. cat moi track ve 30 giay dau
    for tr in p["tracks"]:
        keep = []
        for c in tr["clips"]:
            if c["from"] >= DEMO_FRAMES:
                continue
            c["durationInFrames"] = min(c["durationInFrames"], DEMO_FRAMES - c["from"])
            keep.append(c)
        tr["clips"] = keep

    slides = next(t for t in p["tracks"] if t["id"] == "trk-slides")

    # ── 2. WIPE thay pan: khung dung yen, cai dong la MEP LO DAN
    for i, c in enumerate(slides["clips"]):
        c["motion"] = "none"                       # tat Ken Burns (user ghet rung)
        c["fadeInFrames"] = 0
        c["wipeInFrames"] = 0 if i == 0 else 14    # ~0,47s — dat tran dissolve 0,4s cua 45+
        c["wipeDir"] = ("left", "up", "right", "down")[i % 4]

    # ── 3. phu de KARAOKE (word timing da sinh bang mora VOICEVOX)
    caps = p["captions"]
    caps["style"] = "karaoke"
    caps["source"] = "voicevox-mora"
    caps["lines"] = [l for l in caps["lines"] if l["startMs"] < DEMO_FRAMES / FPS * 1000]
    keep_idx = {i for i, _l in enumerate(caps["lines"])}
    caps["words"] = [w for w in caps["words"]
                     if w["lineIndex"] in keep_idx
                     and w["startMs"] < DEMO_FRAMES / FPS * 1000]

    # ── 4. lop OVERLAY: text tag + pictogram peel
    #    Moc lay tu chinh timeline: slide_02 la canh 「一万回」 (chu bake san trong anh),
    #    nen tag DONG hien ngay trươc no de "dan" con so vao tai nguoi xem.
    s2 = next(c for c in slides["clips"] if c["asset"].endswith("slide_02.jpg"))
    tag_from = s2["from"] + 10
    # ⚠️ Track BAT BUOC co `name` + `type` (TrackSchema) — thieu la parseProject nem
    # "tracks.2.name: Invalid input" ngay o buoc Getting composition, khong phai luc render.
    overlay = {
        "id": "trk-overlay",
        "name": "Overlay",
        "type": "sticker",
        "muted": False,
        "hidden": False,
        "locked": False,
        "clips": [
            {   # ③ con so dat nhat cua doan — tag pop, goc tren-PHAI la cua watermark nen ne
                "id": "tx-1man",
                "kind": "text",
                "from": tag_from,
                "durationInFrames": min(150, DEMO_FRAMES - tag_from),
                "content": "1万回の坂道",
                "preset": "tag",
                "color": "#FFD700",
                "animation": "pop",
                "layout": {"x": 300, "y": 760, "rotation": -2},
                "fontSize": 60,
            },
            {   # ④ pictogram cat giay — peel (ban le canh tren), dung chat giay dan
                # 🔴 TOA DO PHAI NHAM VUNG TRONG CUA ANH. Ban dau dat (1180,250) => no de
                # THANG len chu bake 「1万回」, va vi pictogram cung mau xanh nen trong nhu
                # chu bi nat. Slide_02 trong o nua TREN-TRAI (troi trang) => dat vao do.
                "id": "st-shock",
                "kind": "sticker",
                "from": tag_from + 40,
                "durationInFrames": min(120, DEMO_FRAMES - tag_from - 40),
                "asset": f"assets/{PICTO}",
                "layout": {"x": 420, "y": 130, "w": 190, "rotation": -8},
                "entrance": {"variant": "peel", "delayFrames": 0, "params": {}},
                "exit": {"variant": "fade", "delayFrames": 0, "params": {}},
                "idle": {"amp": 0, "phase": 0},     # 0 = KHONG rung (luat kenh)
                "shadow": "lg",
            },
        ],
    }
    p["tracks"].append(overlay)                     # cuoi mang = tren cung z-order

    # ── 5. ghi project + copy asset (30s dau + pictogram tai dung tu video 16)
    DST_DIR.mkdir(parents=True, exist_ok=True)
    (PUB_DST / "assets").mkdir(parents=True, exist_ok=True)
    need = {c["asset"] for tr in p["tracks"] for c in tr["clips"] if "asset" in c}
    copied = 0
    for rel in sorted(need):
        src = PUB_SRC / rel
        if not src.exists() and rel.endswith(PICTO):
            src = ROOT / "public" / "projects" / "shokutaku-16-banana" / rel
        if src.exists():
            dst = PUB_DST / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
        else:
            print(f"  🔴 THIEU asset: {rel}")
    (DST_DIR / "project.json").write_text(json.dumps(p, ensure_ascii=False, indent=1),
                                          encoding="utf-8")

    print(f"OK projects/18-demo/project.json — {DEMO_FRAMES} frame ({DEMO_FRAMES/FPS:.0f}s)")
    print(f"   slide {len(slides['clips'])} · wipe 14f · karaoke {len(caps['words'])} tu"
          f" / {len(caps['lines'])} dong · overlay {len(overlay['clips'])}")
    print(f"   asset copy {copied}/{len(need)}")
    print("\nrender:  npx remotion render VoxProject "
          "--props=projects/18-demo/project.json out/18-demo.mp4 --overwrite")


if __name__ == "__main__":
    main()
