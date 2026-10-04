# -*- coding: utf-8 -*-
r"""Rai lop DONG cho CA video 19 (shokutaku) — dung muc hieu ung user da duyet o demo 30s.

    py -3 tools\build_overlays_20.py

Bat 4 thu (y nguyen demo `make_demo_18.py`, user chot "hieu ung oke roi"):
  ① KARAOKE phu de word-level (mora VOICEVOX) — style "karaoke"
  ② WIPE tuyen tinh 14 frame thay dissolve, doi huong luan phien, motion "none"
  ③ TEXT tag 'pop' — con so/y chot cua tung doan
  ④ PICTOGRAM cat giay 'peel' — tai dung bo 7 hinh PIL cua video 16

⛔ KHONG bat (dam vao feedback_video_no_motion_mot_giong + audience-45plus §2):
   idle.amp>0 · wobble/punch/spiral · motion pan · SFX rai theo scene.

MAT DO: audience-45plus §2 muc 1 (TRAN <=6/phut) chi do SLIDE — video 19 co 114 slide /
19'11 = 5,94/phut, duoi tran. Overlay o day phuc vu SAN (audience-45plus §2.0: su kien hinh
<=9s, KHONG tinh vao tran vi tran chi do "doi ANH CHINH"). Them 19 overlay (11 tag + 11
picto, mot vai doan trung ca hai) dat vao dung khe dai nhat cua PLAN slide (video 20 dung y
tuong nay nhung goi nham la "tran" — sua lai dung ten hai gate o day).
"""
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PROJ = ROOT / "projects" / "19_tanpakushitsu-asa" / "project.json"
PUB = ROOT / "public" / "projects" / "19_tanpakushitsu-asa" / "assets"
PICTO_SRC = ROOT / "public" / "projects" / "shokutaku-16-banana" / "assets"
FPS = 30

# (slide_idx, text tag hoac None, pictogram hoac None)
# 🔴 Moc theo SLIDE INDEX, khong theo giay: slide index gan chat voi cau thoai (cue `match`),
# nen overlay luon roi dung doan dang noi du timeline co xe dich.
# Tag = con so / y chot CO THAT trong loi doan do (YMYL: khong bia so len hinh).
# Picto: hiyari(het hon) · hatena(?) · hirameki(vo le) · mukumi(phu) · itami(dau) · zzz(ngu)
PLAN = [
    (4,   "1年で5kg",           "ex_hiyari"),      # cold open: phep tinh soc
    (14,  "ゲートは1日3回",     "ex_hatena"),      # co che an du: cong/xe tai/khung nha
    (19,  "夜だけで25%減",      "ex_hiyari"),      # nghien cuu 2014
    (21,  "同じ量でも1/4消える", None),             # ket qua nghien cuu (anh da bake 1/4)
    (26,  "腎臓の方はご注意",   "ex_hiyari"),      # canh bao YMYL (lan 1)
    (29,  "60g÷3=20g",          "ex_hirameki"),    # phep tinh hero (anh da bake 60g/20g)
    (34,  "30秒でわかる",       "ex_hirameki"),    # chi vong-ngon tay test
    (37,  "隙間があれば注意",   "ex_hiyari"),      # ket qua test — canh bao nhe
    (42,  "20gに届かない",      "ex_hatena"),      # bua trua chi mi — LOOP 1 gieo
    (46,  "+1品で約2倍",        "ex_hirameki"),    # cach sua don gian nhat
    (53,  "「なんでだ」",       "ex_hatena"),      # case Katsumi — cau thoai
    (60,  "半分も届かない",     "ex_hiyari"),      # <50% dat 20g o bua sang
    (64,  "10時間トラックなし", "ex_hiyari"),      # co che: dem khong co xe tai
    (71,  "パン1枚で5g",        None),             # 3 lo hong — lo thu nhat
    (79,  "あと一品は百円",     "ex_hirameki"),    # khong can mua protein bot
    (85,  "答えは卵",           "ex_hirameki"),    # TRA OPEN LOOP — dinh bai
    (98,  "数字より力が戻った", None),             # case Ayako — dong bang cam xuc
    (101, "夜は1/4こぼれる",    "ex_hiyari"),      # recap
    (112, "卵を一つ",           "ex_hirameki"),    # cau chot cuoi video
]
# 🔴 VI TRI — khung nay da co 4 cho CO CHU, overlay phai tranh het:
#   · goc tren-PHAI khung  = watermark 「60代の食卓」 (328x133, renderer dan sau)
#   · goc tren-TRAI the    = chip nhan doan (lop ingest)
#   · goc duoi-PHAI khung  = timestamp YouTube
#   · dai den y928..1080   = phu de
# TAG: thap ben trai, TRONG the (nen trang => hop vang doc rat ro).
# PICTO: dat NGOAI the, phia tren dau nhan vat ben TRAI. Ban dau dat trong the (1235,190)
# va no DE LEN NOI DUNG anh (dau ! vang che qua tao do — do duoc o probe frame 3980-4100);
# vung trong cua anh doi theo tung slide nen KHONG the dung mot toa do co dinh trong the.
# Ngoai the thi luon trong: dai ben rong 272px, cast cao 416 dan day 928 => y 140..500 rong.
TAG_XY = (330, 745)
PICTO_XY = (56, 148)
# 🔴 Dat pictogram theo CHIEU CAO, khong theo be ngang: 7 pictogram co ty le rat khac nhau
# (`ex_hirameki` la dau ! DOC => w=168 cho ra cao ~550px, tran xuong CHE DAU BA CU — do
# duoc o probe vong 2). Cast cao 416 dan day 928 => dinh cast o y=512; pictogram dat y=148
# nen cao toi da ~330px moi khong cham cast. Schema chi co `w`, nen suy w tu chieu cao that.
PICTO_H_MAX = 320
# Va kep CA BE NGANG: dai ben trai chi rong 272px (the bat dau x=272), pictogram dat x=56
# nen w toi da 200 moi khong de len the. `ex_mukumi` la hinh NGANG (424x320) => kep chieu
# cao mot minh cho ra w=424, de len the 208px. Hai chieu phai kep cung luc.
PICTO_W_MAX = 200


def split_long_cues(caps, max_chars=46):
    """Tach cue phu de DAI thanh nhieu cue ngan — cat o dau cau tieng Nhat.

    🔴 Vi sao can: dai den chi 152px => o fontSize 38 chi vua 2 DONG. Nhung `lines` cua
    importer la MOT DONG = MOT CAU TTS, va cau dai nhat cua bai nay 174 ky => 3 dong, tran
    len anh (do duoc o frame 510/512 ban render dau). Renderer cu khong bi vi no tach cue
    o 42 ky (SUB_MAXLEN); Remotion khong tach gi.
    Chia thoi gian theo TY LE KY TU cua tung manh — chinh xac hon chia deu, vi cau tieng
    Nhat dai ngan that su ty le voi thoi gian doc.
    ⚠️ `words` gan theo `lineIndex`, nen sau khi tach phai gan LAI lineIndex theo THOI GIAN.
    """
    out = []
    for ln in caps.get("lines", []):
        txt = ln["text"]
        if len(txt) <= max_chars:
            out.append(ln)
            continue
        # cat o dau cau/dau phay, gom lai thanh cac manh <= max_chars
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

    # gan lai lineIndex cho words theo thoi gian
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

    # ── ② WIPE thay pan
    for i, c in enumerate(slides["clips"]):
        c["motion"] = "none"
        c["fadeInFrames"] = 0
        c["wipeInFrames"] = 0 if i == 0 else 14
        c["wipeDir"] = ("left", "up", "right", "down")[i % 4]

    # ── ① KARAOKE
    p["captions"]["style"] = "karaoke"
    p["captions"]["source"] = "voicevox-mora"
    # 🔴 fontSize 48 (mac dinh importer) lam phu de 2 DONG cao hon dai den 152px => dong dau
    # LEO LEN the (do duoc o probe). Dai den y 928..1080; 2 dong font 38 x leading 1,34
    # ≈ 102px + le => vua. Van >= tran co chu cua audience-45plus (sub_size 24 @ ASS ~ 38px
    # @1080 cua remotion — hai he don vi khac nhau, day la px thuc).
    p["captions"]["fontSize"] = 38
    split_long_cues(p["captions"], max_chars=46)

    # ── ③④ overlay
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
                "idle": {"amp": 0, "phase": 0},      # 0 = KHONG rung (luat kenh)
                "shadow": "lg",
            })
            need_picto.add(picto)

    # ── ⑤ WATERMARK nhan dien kenh — chay SUOT video
    # 🔴 Remotion KHONG tu dan watermark: badge 「60代の食卓」 la viec cua `video_render.py`
    # (make_watermark + overlay o step B). Doi sang duong remotion la MAT lop nhan dien —
    # do duoc bang mat o frame v_296/v_900 (goc tren-phai trong tron). Dan lai bang text
    # clip preset "tag" (nen vang chu den, dung khuon badge cu).
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

    for name in sorted(need_picto):
        src = PICTO_SRC / f"{name}.png"
        if src.exists():
            shutil.copy2(src, PUB / f"{name}.png")
        else:
            print(f"  🔴 THIEU pictogram {name}.png")

    PROJ.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")

    tags = sum(1 for c in clips if c["kind"] == "text")
    pics = len(clips) - tags
    # ⚠️ Watermark chay SUOT video nen KHONG phai mot "lan doi hinh" — dem no vao mat do
    # la lam sai phep do cua audience-45plus §2 (luat do so lan KHUNG DOI, khong do so lop).
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
          f"{'✅ 0 cue qua 46 ky (vua 2 dong trong dai den)' if not over else f'🔴 {over} cue >46 ky'}")
    print(f"   mat do: ({len(slides['clips'])} slide + {len(events)} overlay co thoi han)"
          f" / {mins:.1f} phut = {total_ev/mins:.1f} su kien/phut  (tran 6,0 — 45plus §2)"
          f"  [+{len(clips)-len(events)} lop chay suot: watermark]")
    if skipped:
        print(f"   ⚠️ bo qua slide idx khong co: {skipped}")


if __name__ == "__main__":
    main()
