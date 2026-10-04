# -*- coding: utf-8 -*-
r"""build_remotion_21.py — dung project Remotion cho video 21 扶養親族等申告書・二百五万円.

⭐ STYLE **AI NGUOI THAT (photoreal), full-bleed** — nay la khuon THUONG TRUC
   cua kenh (user chot 2026-09-04: *"tu nay deu dung AI nguoi that het nhe"*),
   khong con la thu nghiem nhu o video 20. Xem `CLAUDE.md` §② khoi ⭐⭐⭐⭐.

BON LOAI SCENE, VUNG GIUA CHO DUOC MOT THU:
  art      34 scene : footage clip 8s (clips/a21_<key>.mp4)
  stat      4 scene : the `papercut-stat`    tren nen kem, KHONG co footage
  formula   4 scene : the `papercut-formula` tren nen kem, KHONG co footage
  genten    4 scene : 9 anh chup THAT trang 国税庁/年金機構 (genten/genten21_0N.png)

🔴 CLIP NGAN HON KHE: nguon deu 8,000s, khe dai nhat ~8,8s => ha `speed`
   = 8,0/khe (0,90–0,99). **Chi duoc lam CHAM**, cam lam nhanh
   (`gen_flow19_real.py`: speed>1 day nguoi xem toi phan AI het da nhanh hon).

🔴 CROSS-DISSOLVE: keo clip dai them FADE frame de no LOT DUOI clip sau, roi cho
   clip sau `fadeInFrames=FADE`. Neu chi dat sat nhau thi khong co gi de hoa vao
   — `fadeInFrames` mot minh chi lam clip hien dan tu NEN, ra chop den.
   ⚠️ Chi keo khi khe KE TIEP cung la media; keo vao the chu thi footage nam
   duoi chu mat 0,6s.

🔴 `DUR - x` LA BAY: noi `DUR` thi moi clip viet `DUR - x` tu keo dai toi het
   video. Chot bang moc scene.

CHAY:  python tools/build_remotion_21.py
"""
import io
import json
import math
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes21 import SCENES  # noqa: E402

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
RV = os.path.join(os.path.dirname(PROJ), "remotion-vox")
NAME = "nenkin-21"
PDIR = os.path.join(RV, "projects", NAME)
ADIR = os.path.join(RV, "public", "projects", NAME, "assets")
# 🔴 `paper.jpg`/`bgm.mp3` KHONG con o `public/projects/nenkin-19` — Remotion
#    bundle TOAN BO `public/`, nen asset cua project cu duoc "park" sang
#    `_public_park/` (4,1 GB) va `public/` chi giu project dang render (387 MB).
#    => tim theo DANH SACH, lay cai ton tai dau tien; dung hard-code mot cho roi
#    tuong la mat file. Bo cai nay thi video ra NEN TRON + KHONG BGM ma khong
#    mot dong canh bao (link() im lang khi src khong ton tai).
REF_DIRS = [os.path.join(RV, "public", "projects", "nenkin-20", "assets"),
            os.path.join(RV, "_public_park", "projects", "nenkin-20", "assets"),
            os.path.join(RV, "_public_park", "projects", "nenkin-19", "assets"),
            os.path.join(RV, "public_n19r", "projects", "nenkin-19real", "assets")]


def ref(fn):
    for d in REF_DIRS:
        p = os.path.join(d, fn)
        if os.path.exists(p):
            return p
    return None

FPS = 30
W, H = 1920, 1080
FADE = 18          # 0,6s hoa hinh
SRC_SEC = 8.0      # do dai clip nguon
CAP_MAX = 78       # tran ky tu / khoi phu de (audience-45plus §3: <=2 dong)
STAT_X, STAT_Y, STAT_W = 385, 300, 1150   # full-bleed nen rong hon ban 976px

# 9 anh 原典 chia cho 4 scene (3 + 2 + 2 + 2) — thu tu = thu tu ke trong loi.
# URL + cau phai khoanh do: `tools/_scenes21.py` (da verify 2026-09-04) va
# `06_VIDEO/<STEM>/flow21_GENTEN.md`.
GENTEN = {16: ["genten21_01", "genten21_02", "genten21_03"],
          49: ["genten21_04", "genten21_05"],
          74: ["genten21_06", "genten21_07"],
          83: ["genten21_08", "genten21_09", "genten21_10"]}


# ── uoc BE RONG MUC de tu ha co chu ──────────────────────────
# (nguyen tac + bien an toan 1,06 lay tu build_remotion_19.py: preset la flex
#  NOWRAP co maxWidth, nen vuot tran thi o bi NEN va chu wrap BEN TRONG o —
#  khong tran ra ngoai nen mat khong thay, chi may do duoc.)
def _wide(s, size):
    w = 0.0
    for ch in s:
        w += 1.0 if ord(ch) > 0x2E80 else 0.55
    return w * size * 1.02


def _stat_ink(body, size):
    m = 0.0
    for row in body.split("\n"):
        row = row.strip().lstrip("*")
        if not row:
            continue
        if row.startswith("#"):
            row = row.split("|", 1)[1] if "|" in row else row
        m = max(m, _wide(row.replace("|", "  "), size) + 90)
    return m


def stat_size(body, rows):
    # audience-45plus §2.0c: co chu theo SO DONG, roi ha tiep neu muc khong lot
    size = {1: 60, 2: 58, 3: 56, 4: 50}.get(rows, 48)
    while size > 40 and _stat_ink(body, size) * 1.06 > STAT_W:
        size -= 2
    return size


def formula_size(s):
    # 🔴 tran that CHAT hon `STAT_W + 200`: preset la flex NOWRAP co maxWidth,
    #    vuot tran thi o bi NEN va chu wrap BEN TRONG o (「180万円」 -> 「180万」/
    #    「円」) — khong tran ra ngoai nen MAT KHONG THAY, chi still moi lo.
    #    Do tren still: chuoi ~14 ky @80 da wrap => lay tran 1150.
    size = 80
    while size > 44 and _wide(s, size) * 1.06 > 1150:
        size -= 4
    return size


def split_caption(text, t0, t1):
    """Chia 1 dong timeline thanh cac khoi <=CAP_MAX ky, cat SAU dau cau."""
    if len(text) <= CAP_MAX:
        return [(text, t0, t1)]
    parts, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。、」）" and len(cur) >= CAP_MAX * 0.55:
            parts.append(cur)
            cur = ""
        elif len(cur) >= CAP_MAX:
            parts.append(cur)
            cur = ""
    if cur:
        parts.append(cur)
    tot = sum(len(p) for p in parts) or 1
    out, t = [], t0
    for p in parts:
        d = (t1 - t0) * len(p) / tot
        out.append((p, t, t + d))
        t += d
    return out


def link(src, dst):
    if os.path.exists(dst):
        if os.path.getmtime(dst) >= os.path.getmtime(src):
            return
        os.remove(dst)
    try:
        os.link(src, dst)          # cung o dia => hardlink, 0 byte them
    except OSError:
        shutil.copy2(src, dst)


def main():
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))
    lines = tl["lines"]
    dur_s = lines[-1]["end"]
    DUR = round(dur_s * FPS)
    F = lambda t: round(t * FPS)                                  # noqa: E731

    os.makedirs(PDIR, exist_ok=True)
    os.makedirs(ADIR, exist_ok=True)

    # ── asset ──────────────────────────────────────────────────────────────
    n_as = 0
    for fn in sorted(os.listdir(os.path.join(VD, "clips"))):
        link(os.path.join(VD, "clips", fn), os.path.join(ADIR, fn))
        n_as += 1
    # 🔴 folder genten co the CHUA co (user chua chup 9 screenshot 原典) —
    #    khong duoc crash o day, de GATE asset bao thieu cho ro rang.
    gdir = os.path.join(VD, "genten")
    if os.path.isdir(gdir):
        for fn in sorted(os.listdir(gdir)):
            link(os.path.join(gdir, fn), os.path.join(ADIR, fn))
            n_as += 1
    link(os.path.join(VD, "voice_full.wav"), os.path.join(ADIR, "voice.wav"))
    ref_miss = []
    for fn in ("paper.jpg", "bgm.mp3"):
        src = ref(fn)
        if src:
            link(src, os.path.join(ADIR, fn))
        else:
            ref_miss.append(fn)

    # ── khe tung scene ─────────────────────────────────────────────────────
    slots = []
    for i, s in enumerate(SCENES):
        a = lines[s["L"]]["start"]
        b = lines[SCENES[i + 1]["L"]]["start"] if i + 1 < len(SCENES) else dur_s
        slots.append((a, b))

    vid, gen, stat_c, form_c, marks = [], [], [], [], []
    n_slow, warn = 0, []

    for i, s in enumerate(SCENES):
        a, b = slots[i]
        marks.append({"id": f"sc-{i}", "atFrame": F(a), "label": s["tag"]})
        nxt_is_media = (i + 1 < len(SCENES)
                        and SCENES[i + 1]["kind"] in ("art", "genten"))

        if s["kind"] in ("art", "genten"):
            if s["kind"] == "art":
                # 🖼️ shot `still=True` => ANH TINH `.png` (11 shot bang trang,
                #    user chot 2026-09-04: clip 8s "khong ro noi dung"). Chung
                #    van o `trk-video` vi van la CAT CANH; khac biet duy nhat la
                #    `motion: pan` + khong co `speed`.
                keys = [f"a21_{sh['key']}." + ("png" if sh.get("still") else "mp4")
                        for sh in s["shots"]]
            else:
                keys = [g + ".png" for g in GENTEN[s["L"]]]
            k = len(keys)
            for j, asset in enumerate(keys):
                t0 = a + (b - a) * j / k
                t1 = a + (b - a) * (j + 1) / k
                d = t1 - t0
                last = (j == k - 1)
                extra = FADE if (not last or nxt_is_media) else 0
                fr, to = F(t0), min(DUR, F(t1) + extra)
                c = {"id": f"{'g' if s["kind"] == "genten" else 'v'}-{i}-{j}",
                     "kind": "video", "from": fr,
                     "durationInFrames": max(1, to - fr),
                     "asset": f"assets/{asset}", "fit": "cover",
                     "volume": 0}
                if asset.endswith(".mp4"):
                    if d > SRC_SEC:                 # clip ngan hon khe -> lam CHAM
                        c["speed"] = round(SRC_SEC / d, 3)
                        n_slow += 1
                elif s["kind"] != "genten":
                    c["motion"] = "pan"             # anh tinh thuong -> troi cham
                # 🔴 THE 原典 KHONG PAN (bat 2026-09-05, soi frame t560):
                #    anh 原典 la screenshot 1920x1080 **khit khung**, va thu
                #    quan trong nhat tren no la **VONG KHOANH DO**. `motion: pan`
                #    zoom vao roi troi => o giua doan pan, vong khoanh bi day RA
                #    NGOAI khung: frame 560 chi con MOT VACH NGANG, mat ca khung
                #    bao va mat chu hai ben. Bang chung la bang chung — no phai
                #    dung yen de doc. Cac the 原典 khac (t108/t362/t626) tinh co
                #    dang o dau/cuoi doan pan nen van du => **loi nay khong lo
                #    ra o moi frame**, dung loai chi thay khi soi dung mot mocphut.
                if not (i == 0 and j == 0):
                    c["fadeInFrames"] = FADE
                (gen if s["kind"] == "genten" else vid).append(c)

        elif s["kind"] == "formula" and isinstance(s["formula"], list):
            # scene co NHIEU nhip tinh -> chia deu khe, moi nhip mot the
            fs = s["formula"]
            for j, one in enumerate(fs):
                t0 = a + (b - a) * j / len(fs)
                t1 = a + (b - a) * (j + 1) / len(fs)
                size = formula_size(one)
                ink = _wide(one, size) + 90
                form_c.append({"id": f"t-{i}-{j}", "kind": "text", "from": F(t0),
                            "durationInFrames": max(1, F(t1) - F(t0)),
                            "content": one, "preset": "papercut-formula",
                            "color": "#E0A32A", "animation": "pop",
                            "animationParams": {"restDeg": -1.5},
                            "layout": {"x": max(60, int((W - ink) / 2)),
                                       "y": int(H / 2 - size * 0.9),
                                       "w": STAT_W},
                            "fontSize": size})

        elif s["kind"] in ("stat", "formula"):
            if s["kind"] == "stat":
                body = "\n".join(f"{lab.lstrip('*')}|{val}"
                                 if not lab.startswith("*")
                                 else f"*{lab.lstrip('*')}|{val}"
                                 for lab, val in s["stat"])
                size = stat_size(body, len(s["stat"]))
                preset = "papercut-stat"
            else:
                body = s["formula"]
                size = formula_size(body)
                preset = "papercut-formula"
            # 🔴 CANH GIUA THEO MUC THAT, khong dat x/y co dinh.
            #    Preset neo khoi o `x` va khoi chi rong bang MUC (label col +
            #    value col), khong lap het `w` => x co dinh 385 lam bang lech
            #    han sang trai. Va y=300 co dinh lam bang "troi" tren khung
            #    trong menh mong — dung benh `audience-45plus.md` §2.0c.
            rows = len(s["stat"]) if s["kind"] == "stat" else 1
            ink = (_stat_ink(body, size) if s["kind"] == "stat"
                   else _wide(body, size) + 90)
            x = max(60, min(W - 60 - int(ink), int((W - ink) / 2)))
            y = int(max(200, min(560, (H / 2) - rows * size * 1.55 / 2)))
            (stat_c if s["kind"] == "stat" else form_c).append(
                       {"id": f"t-{i}", "kind": "text", "from": F(a),
                        "durationInFrames": max(1, F(b) - F(a)),
                        "content": body, "preset": preset, "color": "#E0A32A",
                        "animation": "pop", "animationParams": {"restDeg": -1.5},
                        "layout": {"x": x, "y": y, "w": STAT_W},
                        "fontSize": size})
            if s["kind"] == "stat" and len(s["stat"]) < 3:
                warn.append(f"scene {i} '{s['tag']}' chi co {len(s['stat'])} dong "
                            f"(stage-zu-layout §2 doi >=3)")

    # ── phu de ─────────────────────────────────────────────────────────────
    caps, over = [], 0
    for ln in lines:
        for t, x0, x1 in split_caption(ln["text"], ln["start"], ln["end"]):
            if len(t) > CAP_MAX:
                over += 1
            caps.append({"text": t, "startMs": round(x0 * 1000),
                         "endMs": round(x1 * 1000)})

    # ── audio ──────────────────────────────────────────────────────────────
    voice = [{"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
              "asset": "assets/voice.wav", "volume": 1, "trimStartFrames": 0}]
    bgm = []
    if os.path.exists(os.path.join(ADIR, "bgm.mp3")):
        seg = 10914
        t = 0
        while t < DUR:
            bgm.append({"id": f"b{t}", "kind": "audio", "from": t,
                        "durationInFrames": min(seg, DUR - t),
                        "asset": "assets/bgm.mp3", "volume": 0.01,   # -40dB
                        "trimStartFrames": 0})
            t += seg

    doc = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": "nenkin",
                 "fps": FPS, "width": W, "height": H,
                 "createdAt": "2026-09-04T00:00:00.000Z",
                 "modifiedAt": "2026-09-04T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        "sceneMarkers": marks,
        "tracks": [
            {"id": "trk-bg", "name": "nen", "type": "background", "clips": [
                {"id": "bg", "kind": "background", "from": 0,
                 "durationInFrames": DUR, "paper": "assets/paper.jpg",
                 "tint": "#F2EDE4", "tintOpacity": 0.55}]},
            {"id": "trk-video", "name": "footage", "type": "video", "clips": vid},
            # 🔴 BON TRACK RIENG, dat DUNG TEN ma `check_frame_pace.py` doc
            #    (`TRACKS`/`CENTER_TRACK`/`HERO_TRACK`). Builder 20 gop het vao
            #    MOT track `trk-text` => gate khong thay the chu nao va bao oan
            #    **8 scene "nen trong"** — dung 7 scene stat/formula. Cung ho voi
            #    `audience-45plus.md` §2.0f: gate va placement phai doc CUNG mot
            #    nguon, dung de hai tang goi ten khac nhau.
            #    Va `trk-genten` tach khoi `trk-video` co CHU Y: anh tai lieu
            #    TINH co pan cham **khong phai cat canh**, nen no khong duoc tinh
            #    vao tran "doi anh chinh 6/phut" (xem ghi chu trong gate).
            {"id": "trk-genten", "name": "原典", "type": "video", "clips": gen},
            {"id": "trk-stat", "name": "bang so", "type": "text", "clips": stat_c},
            {"id": "trk-formula", "name": "cong thuc", "type": "text",
             "clips": form_c},
            {"id": "trk-voice", "name": "giong", "type": "audio", "clips": voice},
            {"id": "trk-bgm", "name": "bgm", "type": "audio", "clips": bgm},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline",
                     "enabled": True, "fontSize": 44, "lines": caps, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }
    out = os.path.join(PDIR, "project.json")
    io.open(out, "w", encoding="utf-8").write(
        json.dumps(doc, ensure_ascii=False, indent=1))

    # ── GATE ───────────────────────────────────────────────────────────────
    miss = [c["asset"] for c in vid + gen
            if not os.path.exists(os.path.join(ADIR, os.path.basename(c["asset"])))]
    gap = []
    cov = sorted((c["from"], c["from"] + c["durationInFrames"])
                 for c in vid + gen)
    cov += sorted((c["from"], c["from"] + c["durationInFrames"])
                  for c in stat_c + form_c)
    cov.sort()
    cur = 0
    for f, t in cov:
        if f > cur + 2:
            gap.append((cur, f))
        cur = max(cur, t)
    if cur < DUR - 2:
        gap.append((cur, DUR))

    print(f"→ {out}")
    print(f"   {dur_s:.1f}s · {DUR} frame @ {FPS}fps · {len(SCENES)} scene")
    n_still = sum(1 for c in vid if c["asset"].endswith(".png"))
    print(f"   footage {len(vid)} clip ({n_slow} lam cham cho vua khe · "
          f"{n_still} ANH TINH) · "
          f"原典 {len(gen)} anh · bang {len(stat_c)} · cong thuc {len(form_c)} · "
          f"phu de {len(caps)} khoi · asset {n_as}")
    print(f"   GATE asset thieu   : {'✅ 0' if not miss else '🔴 ' + str(miss[:4])}")
    print(f"   GATE phu de >{CAP_MAX} ky : {'✅ 0' if not over else '🔴 ' + str(over)}")
    print(f"   GATE khoang TRONG  : "
          f"{'✅ 0' if not gap else '🔴 ' + str([(round(a/FPS,1), round(b/FPS,1)) for a, b in gap[:5]])}")
    if ref_miss:
        print(f"   🔴 GATE nen/BGM     : thieu {ref_miss} — video se ra nen tron "
              f"/ khong BGM. Tim trong REF_DIRS hoac copy tay vao ADIR")
    for w in warn:
        print("   ⚠️ " + w)
    return 0 if not (miss or over or gap or ref_miss) else 1


if __name__ == "__main__":
    sys.exit(main())
