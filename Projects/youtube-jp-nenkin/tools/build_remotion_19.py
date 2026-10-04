# -*- coding: utf-8 -*-
r"""build_remotion_18.py — `project.json` cho TRỌN video 18 (13 chương, ~15:35).

Copy khuôn từ `build_remotion_17.py` (đã user chốt), chỉ đổi SCENES/PUNCH/STAT theo
kịch bản video 18 (60歳繰上げ｜窓口の一言). NEO SCENE BẰNG CHỈ SỐ DÒNG timeline, không
hardcode giây — sửa lời, re-synth, chạy lại builder là khớp lại.

3 hero là ẢNH THẬT (không AI): card_genten_01/02/03 — screenshot 日本年金機構 đã
khoanh đỏ + nhãn nguồn (`tools/ingest_genten_18.py`), bọc torn-paper qua make_photocard.

CHẠY:  python tools/build_remotion_18.py
"""
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
RV = Path(r"E:\Claude\Projects\remotion-vox")
ML = Path(r"E:\Claude\Projects\_media_library")   # tool dùng chung (check_frame_pace…)
STEM = "19_kounenrei-koyou-keizoku-kyufu"
NAME = "nenkin-19"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#E0A32A"
# ⭐ COLOR AXIS — học 1 lần dùng cả bài (đo từ りょう 970K: 繰上げ=1 màu · 繰下げ=1 màu giữ 36′).
KURIAGE, KURISAGE, BASE65 = RED, "#2E6B4F", AMBER      # 60歳/減る · 70歳/待つ · 65歳 gốc
SP_KURIAGE, SP_KURISAGE = "#C87A72", "#7FA893"          # splash nền theo trục
# ⭐ ÂM THANH — video 17 lên sóng CHỈ CÓ giọng (0 BGM · 0 SFX · 0 CTA). Đường Remotion chưa nối
# tới channels.py; nối lại ở đây. BGM đọc từ hồ sơ kênh, KHÔNG hằng-số-hoá đường dẫn.
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-health\tools")
import channels  # noqa: E402
from _scenes19 import SCENES, STAT, FORMULA, PUNCH, pad_sup, cap_reuse  # noqa: E402
_CH = channels.CHANNELS["nenkin"]
# channels.py ghi bgm là đường tương đối "../youtube-jp-health/…" tính từ THƯ MỤC PROJECT
# của kênh (video_render.py resolve từ cwd = project). Resolve theo đúng gốc đó.
BGM_SRC = (PROJ / _CH["bgm"]).resolve()
BGM_VOL = 10 ** (float(_CH["bgm_gain"]) / 20)          # −40 dB → 0.01 (Remotion volume tuyến tính)
# SFX: đúng 1 chùm mỗi đỉnh bài, ≤1 chùm/5′ (audience-45plus §2 mục 4). Đỉnh = dòng đã gắn
# [間1.2][速0.8][後間1.0] trong _TTS.md — lớp hình + tiếng làm CÙNG việc với lớp giọng.
# ⚠️ KHOÁ LÀ CHỈ SỐ DÒNG `L` — cold open v4 rút 13→11 dòng nên đã dịch −2
#    (44→42 · 62→60 · 92→90). Mọi dict đánh khoá theo L phải dịch CÙNG LƯỢT với
#    `SCENES`; quên một cái là `KeyError` — may mà nổ to, nhưng đừng dựa vào may.
SFX = {42: ("sfx/thud.wav", 0.30), 60: ("sfx/paper.wav", 0.35), 90: ("sfx/drop.wav", 0.30)}

CAST_H, CAST_FEET_Y, CAST_MARGIN = 500, 1052, 4
CAST_RATIO = {
    "sensei_serious": 801 / 1280, "sensei_caution": 990 / 1280,
    "sensei_point": 1044 / 1280, "sensei_reassure": 965 / 1280,
    "sensei_conclude": 806 / 1280, "sensei_present": 1101 / 1280,
    "kikite_worried": 871 / 1280, "kikite_surprised": 1028 / 1280,
    "kikite_listen": 967 / 1280, "kikite_nod": 908 / 1280,
    "kikite_think": 923 / 1280, "kikite_relieved": 863 / 1280,
}
_CW = round(CAST_H * max(CAST_RATIO.values()))
STAGE_X0 = CAST_MARGIN + _CW + 24
STAGE_X1 = 1920 - CAST_MARGIN - _CW - 24
CX = (STAGE_X0 + STAGE_X1) // 2
HERO_Y = 140
HERO_BOTTOM = 900
HW = round((HERO_BOTTOM - HERO_Y) * 1.49)
HX = (1920 - HW) // 2
HERO_BLEED = (CAST_MARGIN + _CW) - HX
SUP_ENTER0, SUP_ENTER1 = 0.12, 0.88   # (bản 18 — giữ để tra, KHÔNG dùng nữa)
SUP_AFTER_HERO = 60    # sticker vào SAU hero 2,0s (30fps) — user chốt 2026-08-31
SUP_STAGGER    = 165   # cách nhau 5,5s ⇒ mỗi sticker 1 lần, không lặp
SUP_LIFE       = 150   # sống 5,0s rồi exit (exit = 1 sự kiện cho sàn 7s)
SUP_ROT = (-7, 7, -5)
OUT_W = 330
OUT_XY = ((1555, 110), (25, 185))
OUT_ROT = (-6, 6)
TBL_INK_X1 = 1140
SW_TBL = 280
_EXT_TBL = round((SW_TBL * math.cos(math.radians(7))
                  + SW_TBL * math.sin(math.radians(7)) - SW_TBL) / 2) + 4
SW_TBL_X = STAGE_X1 - SW_TBL - _EXT_TBL
SW_TBL_Y = (250, 470, 590)   # slot 3 hạ 610→590: 610+280+_EXT_TBL = 904 > HERO_BOTTOM 900
                             # (bản 18 không lộ vì chưa bao giờ dùng tới slot thứ 3)
PX = STAGE_X0 + 20

# ══════════════════════════════════════════════════════════════════════════════
# 39 SCENE — `L` = chỉ số dòng timeline nơi scene BẮT ĐẦU.
# ══════════════════════════════════════════════════════════════════════════════
# banner PUNCH — chữ đâm, neo theo chỉ số dòng
# bảng số liệu — key khớp `stat=` ở SCENES
CAP_MAX = 78
CAP_CUT = "。、」）"


def split_caption(line):
    t = line["text"]
    if len(t) <= CAP_MAX:
        return [line]
    parts, buf = [], ""
    for ch in t:
        buf += ch
        if ch in CAP_CUT and len(buf) >= CAP_MAX * 0.55:
            parts.append(buf)
            buf = ""
    if buf:
        if parts and len(parts[-1]) + len(buf) <= CAP_MAX:
            parts[-1] += buf
        else:
            parts.append(buf)
    fixed = []
    for p in parts:
        while len(p) > CAP_MAX:
            fixed.append(p[:CAP_MAX])
            p = p[CAP_MAX:]
        if p:
            fixed.append(p)
    span = line["end"] - line["start"]
    tot = sum(len(p) for p in fixed)
    out, t0 = [], line["start"]
    for p in fixed:
        d = span * len(p) / tot
        out.append({"start": round(t0, 3), "end": round(t0 + d, 3), "text": p})
        t0 += d
    return out


def stick(i, asset, f, dur, x, y, w, rot=0, ent="rise", amp=5, ph=0.0, sh="lg"):
    return {"id": i, "kind": "sticker", "from": f, "durationInFrames": max(1, dur),
            "asset": f"assets/{asset}.png",
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": ent, "delayFrames": 0, "params": {}},
            "exit": None, "idle": {"amp": amp, "phase": ph}, "shadow": sh}


_HB = {}


def hero_box(asset):
    """(x, y, w) của hero — fit theo CHIỀU CAO khi ảnh cao (genten card ratio ~1,3 fit bề ngang
    1132px là cao 1121px ⇒ TRÀN xuống dải phụ đề, thấy ở still 20322 lượt 2026-08-30).
    Ảnh ngang (ratio ≥1,49) giữ nguyên HW. Canh giữa khung."""
    if asset not in _HB:
        p = PROJ / "06_VIDEO" / STEM / "photocard" / f"{asset}.png"
        w = HW
        if p.exists():
            with Image.open(p) as im:
                w = min(HW, round((HERO_BOTTOM - HERO_Y) * im.width / im.height))
        _HB[asset] = ((1920 - w) // 2, HERO_Y, w)
    return _HB[asset]


def footage(i, asset, f, dur, x, y, w):
    """Ảnh tĩnh làm clip `video` với zoom-punch — cú slam 1.28→1.0 trong 8 frame (Footage.tsx)."""
    return {"id": i, "kind": "video", "from": f, "durationInFrames": max(1, dur),
            "asset": f"assets/{asset}.png", "trimStartFrames": 0, "fit": "contain",
            "layout": {"x": x, "y": y, "w": w, "opacity": 1}, "motion": "zoom-punch",
            "speed": 1, "mirror": False, "volume": 0, "fadeInFrames": 0,
            "wipeInFrames": 0, "wipeDir": "left", "filter": {}}


def txt(i, content, f, dur, preset, color=INK, layout=None, size=None):
    return {"id": i, "kind": "text", "from": f, "durationInFrames": max(1, dur),
            "content": content, "preset": preset, "color": color,
            "animation": "pop", "animationParams": {"restDeg": -1.5},
            "layout": layout or {}, "fontSize": size}


# 🔴 TỰ CO CỠ CÔNG THỨC THEO BỀ RỘNG (user bắt ở 4:10 — mỗi ô tự xuống dòng:
#    「28万」/「円」). `papercut-formula` là flex **nowrap**, nên khi tổng bề ngang
#    vượt `layout.w` thì các span BỊ NÉN (flex-shrink mặc định 1) và chữ wrap BÊN
#    TRONG ô — không có lỗi nào, không có gate nào, chỉ mắt thấy.
#    Cùng bệnh với thẻ 原典 ở 2:37: **thẻ chữ không tự co cỡ theo bề rộng**.
#    ⚠️ Chỗ ngắt dòng tại `≒` là CÓ CHỦ Ý (comment trong TextClip.tsx) — đừng gỡ;
#    thứ phải sửa là CỠ, không phải cách ngắt.
def _em(txt, fs):
    """Bề rộng chữ ước theo em: full-width JP ≈ 1,0em · ASCII ≈ 0,55em."""
    n = sum(0.55 if ord(c) < 0x2000 else 1.0 for c in txt)
    return n * fs + len(txt) * fs * 0.02          # + letterSpacing 0,02em


def _stat_ink(body, size):
    """Mực THẬT của `papercut-stat` = hàng rộng nhất (div absolute shrink-to-fit).

    🔴 Thay cho hằng số `TBL_INK_X1 = 1140` — con số đó là PHỎNG ĐOÁN, không đo gì
       cả, nên gate "sticker đè mực bảng" so 1162 < 1140 → cho qua, trong khi mực
       công thức thật chạy tới ~1215 và sticker đè lên dấu `≒` (user bắt ở 4:10).
       Cùng bệnh với `audience-45plus.md` §6.10: gate đo bằng proxy sai.
    """
    wide = 0
    for row in body.split(NL):
        row = row.strip()
        if not row:
            continue
        row = row.lstrip("*")
        if row[:1] == "#" and "|" in row[:9]:     # tiền tố màu #rrggbb|
            row = row.split("|", 1)[1]
        lab, _, val = row.partition("|")
        w = _em(lab.strip(), size * 0.82)
        if val.strip():
            w += size * 0.34 + max(_em(val.strip(), size) + 2 * round(size * 0.18),
                                   size * 4.6)
        wide = max(wide, w)
    return wide


def _fit_stat(body, size, w):
    """Hạ cỡ bảng tới khi mực lọt `w` — `papercut-stat` cũng nén-rồi-wrap như công thức.

    Đã dính thật ở thẻ セルフチェック: nhãn 「①60歳になった日」 gãy thành 「…なった」/「日」,
    ô 「給料明細を見る」 gãy thành 「…見」/「る」. Mực ước 928px > maxWidth 810.
    """
    while size > 42 and _stat_ink(body, size) * 1.06 > w:
        size -= 2
    return size


# 🔬 ĐỘ CHÍNH XÁC CỦA ƯỚC LƯỢNG — ĐO TRÊN STILL ĐÃ RENDER, không phải đoán.
#    Cách đo lại (khi đổi font/preset): render still scene đó, quét cột pixel mực
#      a = np.array(Image.open(png).convert('L'))[y0:y1, x0:x1]
#      xs = np.nonzero((a < 110).sum(axis=0) > 1)[0]; rộng = xs.max() - xs.min()
#    Số đo 2026-08-31 (nenkin 19) — hai preset gần như trùng nhau:
#      · papercut-stat    @48 → ước 693 · THẬT 661 ⇒ dư 4,6%
#      · papercut-formula @80 → ước 889 · THẬT 843 ⇒ dư 5,2%
#    ⇒ biên an toàn 1,06 đã phủ cả hai; KHÔNG cần hệ số hiệu chỉnh.
#
# 🔴 BÀI HỌC ĐO LƯỜNG (suýt cài một hệ số sai vào tool): lần đo đầu cho formula ra
#    "dư 27,3%" và tao suýt chốt `_FORMULA_K = 0.80` — nhưng con số đó sai vì **cửa
#    sổ quét `x < 1165` CẮT CỤT chính cái mực đang đo** (mực thật chạy tới 1333).
#    Ô quét hẹp hơn vật cần đo thì phép đo trả về mép cửa sổ, không trả về vật, và
#    nó **trông vẫn như một con số hợp lý**. Cùng bẫy đã ghi ở
#    `audience-45plus.md` §6.10 (ca 17) và `media-library.md` §2.10 ⑤.
#    ⇒ Trước khi tin một số đo pixel: kiểm xem kết quả có CHẠM MÉP cửa sổ không.
_FORMULA_K = 1.0


def _formula_ink(body, size):
    """Mực THẬT của `papercut-formula` (flex nowrap, ngắt dòng tại `=`/`≒`)."""
    parts = [p for p in body.split() if p]
    eq = next((i for i, p in enumerate(parts) if p in ("=", "≒")), -1)
    rows = [parts[:eq + 1], parts[eq + 1:]] if eq >= 0 else [parts]
    i0, wide = 0, 0
    for r, row in enumerate(rows):
        tot = 0
        for j, p in enumerate(row):
            if p in "÷×−+＋-=≒→":
                tot += size * 0.92
                continue
            fs = size * 1.16 if (eq >= 0 and (i0 + j) > eq) else size
            tot += _em(p, fs) + 2 * round(fs * 0.16)
        tot += max(0, len(row) - 1) * round(size * 0.22)
        wide = max(wide, tot + (size * 0.9 if r else 0))
        i0 += len(row)
    return wide * _FORMULA_K


def _fit_formula(body, size, w):
    """Hạ cỡ tới khi mực lọt `w`.

    🔴 `papercut-formula` là flex **nowrap**: vượt `layout.w` thì span BỊ NÉN
       (flex-shrink mặc định 1) và chữ wrap BÊN TRONG ô — ra 「28万」/「円」.
       Không lỗi, không gate, chỉ mắt thấy (user bắt ở 4:10).
       Cùng bệnh với thẻ 原典 ở 2:37: **thẻ chữ không tự co cỡ theo bề rộng**.
    ⚠️ Chỗ ngắt dòng tại `≒` là CÓ CHỦ Ý (comment trong TextClip.tsx) — đừng gỡ;
       thứ phải sửa là CỠ, không phải cách ngắt.
    """
    while size > 40 and _formula_ink(body, size) * 1.06 > w:
        size -= 4                 # 6% biên an toàn cho sai số bề rộng glyph
    return size


# ── MỘT NGUỒN SỰ THẬT cho hình học bảng/công thức ───────────────────────────
# Placement và gate PHẢI đọc cùng hàm này. Bản trước tính hai nơi bằng hai công
# thức (một cái quên `_EXT_TBL`) ⇒ làn "đã co" vẫn đè 8px — đúng cái bẫy
# stage-zu-layout.md §5 mục 2 đã ghi: hai đại lượng khác vai thì đừng gộp, mà
# một đại lượng thì đừng tính hai lần.
TBL_X0 = STAGE_X0 + 16
TBL_W_MAX = STAGE_X1 - TBL_X0 - 12          # trần bề rộng thật của dải sân khấu


def tbl_geom(s):
    """→ (cỡ bảng, cỡ công thức, mực rộng nhất, bề rộng làn sticker, x làn).

    `sw = 0` nghĩa là khe còn <200px ⇒ scene này KHÔNG đặt sticker.
    """
    sz = fz = ink = 0
    if s.get("stat"):
        b, z = STAT[s["stat"]]
        sz = _fit_stat(b, z, TBL_W_MAX)
        ink = max(ink, _stat_ink(b, sz))
    if s.get("formula"):
        b, z = FORMULA[s["formula"]]
        fz = _fit_formula(b, z, TBL_W_MAX)
        ink = max(ink, _formula_ink(b, fz))
    # 🔴 trừ `_EXT_TBL` HAI LẦN: sticker xoay 7° nở ra CẢ HAI bên, nên `sx` đã phải
    #    lùi vào _EXT_TBL để mép phải không tràn khung, rồi mép TRÁI lại nở thêm
    #    _EXT_TBL nữa (mép trái thật = sx − _EXT_TBL). Trừ một lần thì làn "đã co"
    #    vẫn đè 4–8px — gate kiểm-chứng-chéo bắt được, đúng vai của nó.
    gap = STAGE_X1 - (TBL_X0 + ink) - 12 - 2 * _EXT_TBL
    sw = 0 if gap < 200 else min(SW_TBL, int(gap))
    return sz, fz, ink, sw, (STAGE_X1 - sw - _EXT_TBL if sw else 0)


def bgm_clips(DUR):
    """BGM lặp vừa đủ DUR. Độ dài file đo bằng ffprobe, không hằng-số-hoá."""
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(BGM_SRC)], capture_output=True, text=True)
    sec = float(out.stdout.strip() or 0)
    if sec <= 0:
        raise SystemExit(f"🔴 không đo được BGM {BGM_SRC}")
    L = int(sec * FPS)
    clips, f, i = [], 0, 0
    while f < DUR:
        clips.append({"id": f"bgm-{i}", "kind": "audio", "from": f,
                      "durationInFrames": min(L, DUR - f), "asset": "assets/bgm.mp3",
                      "volume": BGM_VOL, "trimStartFrames": 0})
        f += L
        i += 1
    return clips


def main():
    tl = json.loads((PROJ / "06_VIDEO" / STEM / "timeline.json").read_text(encoding="utf-8"))
    lines = tl["lines"]
    F = lambda idx: round(lines[idx]["start"] * FPS)          # noqa: E731
    DUR = round(tl["total"] * FPS)

    # lấp sup cho đủ sàn 7s — phải chạy SAU khi có `lines` (cần độ dài từng scene)
    _starts = [lines[s["L"]]["start"] for s in SCENES]
    # ⚠️ pad_sup chỉ còn lo scene BẢNG (ảnh đã tự lo sàn 7s ở scene ảnh).
    #    user chốt 2026-08-31: "không muốn sticker lặp lại quá nhiều lần trong 1 video".
    pad_sup(SCENES, _starts, lines[-1]["end"], only_table=True)
    cap_reuse(SCENES, cap=3)   # trần 3 lần/video cho mỗi sticker

    for k, s in enumerate(SCENES):
        s["f"] = F(s["L"])
        s["to"] = F(SCENES[k + 1]["L"]) if k + 1 < len(SCENES) else DUR

    bad = [f"  scene {k} (dòng {s['L']}) chỉ {(s['to']-s['f'])/FPS:.1f}s"
           for k, s in enumerate(SCENES) if s["to"] - s["f"] < 6 * FPS]
    if bad:
        print("🔴 scene ngắn hơn 6s (audience-45plus §2 mục 2):")
        print(NL.join(bad))
        return 1

    clash = [f"  scene {k} (dòng {s['L']}) tag={s['tag']} hero={s['hero']} +{s.get('stat') or s.get('formula')}"
             for k, s in enumerate(SCENES)
             if (s.get("stat") or s.get("formula")) and s.get("hero")]
    if clash:
        print("🔴 scene có bảng/công thức MÀ VẪN có hero — bảng sẽ bị ảnh che:")
        print(NL.join(clash))
        return 1

    # 🔴 GATE peak: phải có hero ẢNH và KHÔNG có bảng/công thức (zoom-punch lên chữ là phá chữ).
    badpk = [f"  scene {k} L={s['L']} tag={s['tag']}" for k, s in enumerate(SCENES)
             if s.get("peak") is not None
             and (not (s.get("hero") or s.get("heroes")) or s.get("stat") or s.get("formula")
                  or not (s["L"] <= s["peak"] < (SCENES[k+1]["L"] if k+1 < len(SCENES) else 10**9)))]
    if badpk:
        print("🔴 peak sai: cần hero ảnh, không stat/formula, dòng peak nằm trong scene:")
        print(NL.join(badpk))
        return 1
    npk = sum(1 for s in SCENES if s.get("peak") is not None)
    if npk > math.ceil(DUR / FPS / 300):
        print(f"🔴 {npk} chùm SFX > trần ≤1 chùm/5′ (audience-45plus §2 mục 4)")
        return 1

    trk_bg, cl, cr, hero, sup1, sup2, sup3 = [], [], [], [], [], [], []
    tag, punch, stat, formula, peak, sfx = [], [], [], [], [], []
    dropped_sup = []      # scene bị bỏ sticker vì bảng quá rộng (in ở tổng kết)
    all_segs = []         # mốc ĐOẠN ẢNH toàn video — gate ⑤ đọc lại
    cy = CAST_FEET_Y - CAST_H

    for k, s in enumerate(SCENES):
        f, to = s["f"], s["to"]
        d = to - f
        trk_bg.append(dict(id=f"bg-{k}", kind="background", **{"from": f},
                           durationInFrames=d, paper="assets/paper.jpg",
                           tint="#F2EDE4", tintOpacity=0.55, grid=True, dots=True,
                           splash=s["sp"]))
        wl = round(CAST_H * CAST_RATIO[s["l"]])
        wr = round(CAST_H * CAST_RATIO[s["r"]])
        ent = "rise" if k == 0 else "none"
        cl.append(stick(f"cl-{k}", s["l"], f, d, CAST_MARGIN, cy, wl, ent=ent,
                        amp=3, ph=0.4, sh="sm"))
        cr.append(stick(f"cr-{k}", s["r"], f, d, 1920 - wr - CAST_MARGIN, cy, wr,
                        ent=ent, amp=3, ph=2.7, sh="sm"))
        pk_f = F(s["peak"]) if s.get("peak") is not None else None
        # 🔴 Đỉnh rơi NGAY đầu scene (L=3 ペン先): hero sticker bay vào (zoom-through) cùng lúc
        # footage slam ⇒ hai chuyển động chồng, still 1460 ra nền nhòe toàn khung. Khi đó footage
        # LÀ hero — bỏ sticker. Đỉnh rơi giữa scene thì sticker hiện trước, footage đè sau (đúng ý).
        tbl = bool(s.get("stat") or s.get("formula"))
        # ⭐ ĐỔI ẢNH MỖI ~7s (user chốt 2026-08-31): scene KHÔNG phải bảng số thì
        #    hero là một DÃY ảnh, thay nhau mỗi HERO_SWAP giây. Scene có stat/formula
        #    được miễn — bảng tự build-on nên không đứng yên.
        hs = s.get("heroes") or ([s["hero"]] if s.get("hero") else [])
        # 🔴🔴 ĐƠN VỊ HÌNH LÀ **ĐOẠN ẢNH**, KHÔNG CÒN LÀ SCENE (sửa 2026-09-01).
        #    Từ khi hero thành một DÃY ảnh, mọi lớp neo theo `to` (hết scene) đều sai:
        #    peak footage phủ trọn scene và nằm TRÊN hero ⇒ ảnh đổi bên dưới mà màn hình
        #    vẫn giữ ảnh cũ (user bắt ở 7:50); sticker vào ở ảnh 1 còn sống sang ảnh 2–3
        #    ("text sticker của ảnh trước sang ảnh mới vẫn còn").
        #    ⇒ `segs` là nguồn sự thật cho CẢ hero, peak và sticker.
        #    📌 Bài học: đổi ĐƠN VỊ CƠ BẢN thì phải rà lại mọi thứ đang neo vào đơn vị cũ —
        #       cùng họ với "đổi engine dựng hình thì rà lại thứ engine cũ làm hộ".
        segs = [(f, to)]
        if hs and len(hs) > 1 and not tbl:
            seg = d // len(hs)
            segs = [(f + hi * seg, (to if hi == len(hs) - 1 else f + (hi + 1) * seg))
                    for hi in range(len(hs))]
            for hi, (hf, he) in enumerate(segs):
                if pk_f is not None and hf <= pk_f < he:
                    continue          # đoạn có cú slam thì để footage lo
                hero.append(stick(f"h{hi}-{k}", hs[hi], hf + 4, he - hf - 4, HX, HERO_Y, HW,
                                  ent=["grow", "rise", "flip", "zoom-through"][(k + hi) % 4], amp=5))
            hs = []                    # đã dựng xong, bỏ qua nhánh 1-ảnh dưới
        all_segs.extend(segs)
        # dãy 1 ảnh cũng phải chạy qua đây — bản đầu đọc s["hero"] nên scene nào
        # đã đổi sang heroes=[...] mà chỉ có 1 phần tử thì MẤT HERO (gate ③ bắt được)
        if hs and not (pk_f is not None and pk_f <= f + 6):
            hx, hy, hw = hero_box(hs[0])
            hero.append(stick(f"h-{k}", hs[0], f + 6, d - 6, hx, hy, hw,
                              ent=["grow", "rise", "flip", "zoom-through"][k % 4], amp=5))
        if pk_f is not None:
            # footage nằm TRÊN hero, CÙNG HỘP hero_box ⇒ slam đúng vào ảnh đang hiện.
            # scene dùng dãy ảnh thì lấy đúng ảnh của ĐOẠN chứa cú slam.
            _hl = s.get("heroes") or [s.get("hero")]
            _i = next((i for i, (a, b) in enumerate(segs) if a <= pk_f < b), len(segs) - 1)
            pk_asset = _hl[min(_i, len(_hl) - 1)]
            hx, hy, hw = hero_box(pk_asset)
            # 🔴 kết thúc ở cuối ĐOẠN ẢNH, KHÔNG phải cuối scene. Bản trước để `to - pk_f`
            #    nên footage phủ trọn scene và đè lên các ảnh sau nó ⇒ "ảnh chuyển mà ảnh
            #    cũ vẫn còn" (user bắt ở 7:50, scene 冒頭のふたり: hero đổi ở 468,3s và
            #    475,5s nhưng peak sống 453,6→482,8 nên không ảnh nào hiện ra được).
            peak.append(footage(f"pk-{k}", pk_asset, pk_f, segs[_i][1] - pk_f, hx, hy, hw))
            a, v = SFX[s["peak"]]
            sfx.append({"id": f"sfx-{k}", "kind": "audio", "from": pk_f, "durationInFrames": 90,
                        "asset": a, "volume": v, "trimStartFrames": 0})
        sups = s.get("sup") or []
        # 🔴 LÀN STICKER CO THEO MỰC BẢNG THẬT (không phải hằng số 280). Bảng/công
        #    thức rộng bao nhiêu là do NỘI DUNG; ép làn 280px cố định thì 4/13 scene
        #    bảng bị sticker đè lên chữ (nặng nhất mực tới 1402 > làn 1162).
        #    Khe <200px thì BỎ sticker — scene số liệu vốn được MIỄN sàn nhịp 9s
        #    (audience-45plus §2.0b), bảng build-on đã là chuyển động rồi.
        sz_tbl, fz_tbl, sw_tbl, sx_tbl = 0, 0, SW_TBL, SW_TBL_X
        if tbl:
            sz_tbl, fz_tbl, _ink, sw_tbl, sx_tbl = tbl_geom(s)
            if sups and not sw_tbl:
                dropped_sup.append(
                    f"{s['tag']} (mực {TBL_X0 + _ink:.0f}, khe không đủ)")
                sups = []
        n = len(sups)
        # ⭐ LUẬT STICKER (user chốt 2026-08-31, memory feedback_sticker_1_lan_vao_sau_hero_2s):
        #   ① 1 sticker = ĐÚNG 1 lần trong scene — cấm xoay vòng lặp cùng file qua các vị trí
        #   ② sticker vào SAU hero ~2s (60 frame @30fps), KHÔNG vào cùng lúc với ảnh
        #   ③ sàn 7s trả bằng `exit` (mọi sticker) + thêm FILE, không phải lặp file
        # Bản 18 vào ở 12% thời lượng scene ⇒ scene 40s thì sticker đầu tới giây 4,8.
        # 🔴 NEO VÀO ĐOẠN ẢNH, KHÔNG VÀO SCENE (sửa 2026-09-01, user: *"text sticker
        #    hiển thị ở ảnh trước mà sang ảnh mới vẫn còn"*). Sticker là chú thích CHO
        #    TẤM ẢNH đang hiện ⇒ nó phải chết khi ảnh đổi. Bản trước rải theo `st[j]`
        #    tính từ đầu SCENE và kết thúc ở `to` ⇒ sticker vào ở ảnh 1 sống sang ảnh 3.
        #    Mỗi đoạn ảnh nhận sticker của riêng nó (vòng lại nếu nhiều sticker hơn đoạn).
        ns = len(segs)
        st, seg_of = [], []
        for i in range(n):
            si = i % ns
            s0, e0 = segs[si]
            st.append(s0 + SUP_AFTER_HERO + (i // ns) * SUP_STAGGER)
            seg_of.append(si)
        npos = len(SW_TBL_Y) if tbl else len(OUT_XY)
        step = 1 if tbl else len(OUT_XY)
        for j, el in enumerate(sups):
            trk = (sup1, sup2, sup3)[j % 3]
            f0 = st[j]
            _sg_end = segs[seg_of[j]][1]
            nxt = j + step
            # trần: hoặc sticker kế tiếp CÙNG ĐOẠN, hoặc mép đoạn ảnh
            fend = st[nxt] if (nxt < n and seg_of[nxt] == seg_of[j]) else _sg_end
            fend = min(fend, _sg_end - 4)
            if fend - f0 < 30:        # không đủ sống trong đoạn → bỏ, đừng nháy 1 cái
                continue
            if tbl:
                sx, sy, sw = sx_tbl, SW_TBL_Y[j % npos], sw_tbl
                rot = SUP_ROT[j % 3]
            else:
                sx, sy = OUT_XY[j % npos]
                sw, rot = OUT_W, OUT_ROT[j % npos]
            # ③ MỌI sticker đều exit — mỗi cú rút là 1 sự kiện hình miễn phí cho sàn 7s
            fend = min(fend, f0 + SUP_LIFE)
            ex = {"variant": "fade", "params": {}}
            # chỉ cắt sticker nào BẮT ĐẦU TRƯỚC cú slam; cái vào SAU thì để sống đủ
            # (bản 18 cắt cả hai ⇒ sticker sau peak chỉ sống 24 frame = nháy một cái)
            if pk_f is not None and f0 < pk_f and fend > pk_f:
                fend = max(f0 + 24, pk_f)
            sc = stick(f"s{j}-{k}", el, f0, fend - f0, sx, sy, sw,
                       rot=rot, ent="pop", amp=5, ph=1.2 + j * 2, sh="sm")
            sc["exit"] = ex
            trk.append(sc)
        tag.append(txt(f"tag-{k}", s["tag"], f + 4, d - 4, "papercut-banner",
                       layout={"x": 74, "y": 58}, size=64))
        if s.get("stat"):
            body, sz = STAT[s["stat"]]
            # 🔴 chặn trần 60 frame (2s): 0,10×d ở scene 48s = 4,8s khung TRỐNG
            #    (user bắt bằng mắt 2026-08-31). Gate ③ không đo được cái này.
            f_st = f + min(60, max(20, int(d * 0.10)))
            # y CĂN THEO SỐ DÒNG: bảng ít dòng mà neo y=240 thì chữ dạt lên đỉnh,
            # để trống nửa dưới khung (soi still 2026-08-31: 研究ノート 2 dòng trôi
            # giữa khoảng trống). Ước cao khối = rows × size × 1,55 rồi canh giữa
            # dải sân khấu (150…900).
            sz = sz_tbl or sz            # cỡ đã co cho khỏi wrap (tbl_geom)
            _rows = body.count(NL) + 1
            _h = _rows * sz * 1.55
            _y = max(200, min(300, int((150 + 900) / 2 - _h / 2)))
            stat.append(txt(f"st-{k}", body, f_st, to - f_st - 4, "papercut-stat",
                            color=AMBER,
                            layout={"x": TBL_X0, "y": _y, "w": TBL_W_MAX},
                            size=sz))
        if s.get("formula"):
            # tra DICT như STAT (bản 18 nhét thẳng chuỗi vào SCENES — dễ lệch,
            # và nếu quên thì render ra đúng cái KHOÁ, không ai bắt được)
            fbody, _ = FORMULA[s["formula"]]
            fsz = fz_tbl                 # cỡ đã co cho khỏi wrap (tbl_geom)
            stat_off = 150 if s.get("stat") else 0
            # 🔴 bản đầu để 0,55×d ⇒ scene 17,7s thì công thức tới giây 9,7 mới hiện,
            #    khung trống gần 10s (user bắt ở 4:10). Dùng CÙNG luật với bảng.
            _f_fm = f + min(60, max(20, int(d * 0.10)))
            formula.append(txt(f"fm-{k}", fbody, _f_fm,
                               to - _f_fm - 6, "papercut-formula",
                               color=s.get("fcolor", AMBER),
                               layout={"x": TBL_X0, "y": 430 + stat_off, "w": TBL_W_MAX},
                               size=fsz))

    for idx, body, col in PUNCH:
        f = F(idx)
        end = round(lines[idx]["end"] * FPS)
        punch.append(txt(f"p-{idx}", body, f + 8, max(60, end - f - 8),
                         "papercut-banner", color=col, layout={"x": PX}, size=62))

    T = lambda i, n, ty, c: {"id": i, "name": n, "type": ty, "muted": False,   # noqa: E731
                             "hidden": False, "locked": False, "clips": c}
    tracks = [
        T("trk-bg", "nền giấy", "background", trk_bg),
        T("trk-hero", "hero ảnh", "sticker", hero),
        T("trk-peak", "đỉnh bài (zoom-punch)", "video", peak),
        T("trk-sup1", "phụ 1", "sticker", sup1),
        T("trk-sup2", "phụ 2", "sticker", sup2),
        T("trk-sup3", "phụ 3", "sticker", sup3),
        T("trk-cast-l", "cast trái", "sticker", cl),
        T("trk-cast-r", "cast phải", "sticker", cr),
        T("trk-stat", "bảng số liệu", "text", stat),
        T("trk-formula", "công thức", "text", formula),
        T("trk-tag", "tag", "text", tag),
        T("trk-punch", "punch", "text", punch),
        T("trk-voice", "giọng", "audio",
          [{"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
            "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]),
        T("trk-sfx", "SFX đỉnh bài", "audio", sfx),
        T("trk-bgm", "BGM −40dB", "audio", bgm_clips(DUR)),
    ]
    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": "nenkin", "fps": FPS,
                 "width": 1920, "height": 1080,
                 "createdAt": "2026-08-29T00:00:00.000Z",
                 "modifiedAt": "2026-08-29T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        "sceneMarkers": [{"id": f"sc-{k}", "atFrame": s["f"], "label": s["tag"]}
                         for k, s in enumerate(SCENES)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44,
                     "lines": [{"text": c["text"],
                                "startMs": round(c["start"] * 1000),
                                "endMs": round(c["end"] * 1000)}
                               for l in lines for c in split_caption(l)],
                     "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }

    out = RV / "projects" / NAME
    out.mkdir(parents=True, exist_ok=True)
    (out / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    ad = RV / "public" / "projects" / NAME / "assets"
    ad.mkdir(parents=True, exist_ok=True)
    src = PROJ / "06_VIDEO" / STEM
    for p in list((src / "photocard").glob("*.png")) + list((src / "sticker").glob("*.png")):
        shutil.copy(p, ad / p.name)
    for c in CAST_RATIO:
        f = PROJ / "assets" / "cast" / f"{c}.png"
        if f.exists():
            shutil.copy(f, ad / f.name)
    voice = src / "voice_full.wav"
    mp3 = ad / "voice.mp3"
    if voice.exists() and not mp3.exists():
            subprocess.run(["ffmpeg", "-y", "-i", str(voice), "-b:a", "192k", str(mp3)],
                       check=True, capture_output=True)
    if not (ad / "bgm.mp3").exists():
        shutil.copy(BGM_SRC, ad / "bgm.mp3")
    old = RV / "public" / "projects" / "nenkin-17-demo" / "assets" / "paper.jpg"
    if old.exists() and not (ad / "paper.jpg").exists():
        shutil.copy(old, ad / "paper.jpg")

    # 🔴 phải quét CẢ track "video" (zoom-punch footage), không chỉ "sticker".
    #    Scene có peak ở đầu thì hero-sticker bị bỏ qua ⇒ ảnh đó CHỈ còn nằm ở clip
    #    footage; bản 18 chỉ quét "sticker" nên 2 ảnh đỉnh KHÔNG vào sổ thiếu —
    #    đúng lỗ mà render-background.md §1.5 cảnh báo (thêm khoá asset thì phải
    #    thêm vào sổ cùng lượt). Ảnh thiếu vẫn ra clip, EXITCODE=0, không ai biết.
    want = {c["asset"].split("/")[-1] for t in tracks
            if t["type"] in ("sticker", "video")
            for c in t["clips"] if c.get("asset")}
    want |= {"paper.jpg"}
    miss = sorted(w for w in want if not (ad / w).exists())

    HERO_BLEED_MAX = 90
    aspect = {}
    for p in (src / "sticker").glob("*.png"):
        with Image.open(p) as im:
            aspect[p.name] = im.width / im.height
    for p in (src / "photocard").glob("*.png"):
        with Image.open(p) as im:
            aspect[p.name] = im.width / im.height

    def _rect(c):
        L = c["layout"]
        w = L["w"]
        h = w / aspect.get(c["asset"].split("/")[-1], 1.0)
        th = math.radians(abs(L.get("rotation", 0)))
        ww = w * math.cos(th) + h * math.sin(th)
        hh = h * math.cos(th) + w * math.sin(th)
        cx, cy = L["x"] + w / 2, L["y"] + h / 2
        return (cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2)

    def _hit(a, b, pad=0):
        return (a[0] < b[2] - pad and b[0] < a[2] - pad
                and a[1] < b[3] - pad and b[1] < a[3] - pad)

    supclips = [c for t in tracks if t["id"] in ("trk-sup1", "trk-sup2", "trk-sup3")
                for c in t["clips"]]
    tbl_scene = {k for k, s in enumerate(SCENES) if s.get("stat") or s.get("formula")}
    heroR = (HX, HERO_Y, HX + HW, HERO_BOTTOM)
    lost, onhero, oncast = [], [], []
    for c in supclips:
        k = int(c["id"].split("-")[1])
        r = _rect(c)
        if r[0] < 4 or r[2] > 1916 or r[1] < 4 or r[3] > HERO_BOTTOM:
            lost.append(c["id"])
        if k not in tbl_scene and _hit(r, heroR, pad=6):
            onhero.append(c["id"])
        s = SCENES[k]
        for side, ratio in (("l", CAST_RATIO[s["l"]]), ("r", CAST_RATIO[s["r"]])):
            cw = round(CAST_H * ratio)
            cx0 = CAST_MARGIN if side == "l" else 1920 - cw - CAST_MARGIN
            if _hit(r, (cx0, CAST_FEET_Y - CAST_H, cx0 + cw, CAST_FEET_Y), pad=6):
                oncast.append(c["id"])
    pairs = []
    for i, a in enumerate(supclips):
        for b in supclips[i + 1:]:
            if a["from"] < b["from"] + b["durationInFrames"] \
               and b["from"] < a["from"] + a["durationInFrames"] \
               and _hit(_rect(a), _rect(b), pad=6):
                pairs.append((a["id"], b["id"]))
    for lab, bad in (("lọt khỏi khung / chạm phụ đề", lost),
                     ("ĐÈ LÊN ẢNH HERO", onhero),
                     ("đè lên cast", oncast),
                     ("đè lên nhau", pairs)):
        if bad:
            print(f"🔴 sticker {lab}: {len(bad)} — {bad[:8]}")
            return 1
    if HERO_BLEED > HERO_BLEED_MAX:
        print(f"🔴 hero lấn vào cast {HERO_BLEED}px > trần {HERO_BLEED_MAX}px")
        return 1

    ns = sum(len(t["clips"]) for t in tracks if t["type"] == "sticker")
    nt = sum(len(t["clips"]) for t in tracks if t["type"] == "text")
    print(f"✓ {out / 'project.json'}")
    print(f"   {DUR} frame ({DUR/FPS/60:.2f}′) · {len(SCENES)} scene · {ns} sticker "
          f"· {nt} text · {len(lines)} dòng phụ đề")
    print(f"   dải sân khấu {STAGE_X0}–{STAGE_X1} ({STAGE_X1-STAGE_X0}px) · "
          f"cast rộng {_CW}px")
    print(f"   HERO {HW}px = {HW*100//1920}% khung (lấn cast {HERO_BLEED}px/bên)")
    print(f"   ⭐ peak ×{len(peak)} (zoom-punch) · sfx ×{len(sfx)} · bgm {len(bgm_clips(DUR))} clip "
          f"@{BGM_VOL:.3f} ({_CH['bgm_gain']} dB) · trục màu 繰上げ={KURIAGE} 繰下げ={KURISAGE}")
    print(f"   scene ngắn nhất {min((s['to']-s['f'])/FPS for s in SCENES):.1f}s · "
          f"dài nhất {max((s['to']-s['f'])/FPS for s in SCENES):.1f}s · "
          f"{len(SCENES)/(DUR/FPS/60):.2f} scene/phút")

    # 🔴 ĐO MỰC THẬT, không dùng hằng số. Bản cũ so `SW_TBL_X < TBL_INK_X1(=1140)`
    #    — một con số phỏng đoán cho BẢNG, và nó **cho qua** ca công thức mực chạy
    #    tới ~1215 (sticker đè lên dấu `≒`, user bắt ở 4:10). Gate nào đo bằng proxy
    #    thì sớm muộn cũng gác nhầm thứ nó không đo.
    over, wrapped = [], []
    for s in SCENES:
        if not (s.get("stat") or s.get("formula")):
            continue
        sz, fz, ink, sw, sx = tbl_geom(s)
        # ① chữ có bị NÉN rồi wrap trong ô không (「①60歳になった」/「日」)
        if ink * 1.06 > TBL_W_MAX:
            wrapped.append(f"{s['tag']} (mực {ink:.0f} > trần {TBL_W_MAX})")
        # ② sticker có đè lên mực bảng/công thức không
        if (s.get("sup") or []) and sw and TBL_X0 + ink > sx - _EXT_TBL - 12:
            over.append(f"{s['tag']} (mực {TBL_X0 + ink:.0f} · làn {sw}px @{sx})")
    if wrapped:
        print("🔴 bảng/công thức tràn trần bề rộng → chữ sẽ wrap trong ô:")
        for o in wrapped:
            print("   " + o)
        return 1
    if over:
        print("🔴 sticker đè mực bảng/công thức:")
        for o in over:
            print("   " + o)
        return 1
    if dropped_sup:
        print(f"   ⓘ bỏ sticker ở {len(dropped_sup)} scene bảng rộng: "
              + " · ".join(dropped_sup))

    # ⑤ 🔴 GATE "SỐNG XUYÊN ĐOẠN ẢNH" — lớp nằm TRÊN hero mà sống qua lúc ảnh đổi thì
    #    ảnh mới bị che (peak) hoặc chú thích lạc sang ảnh khác (sticker). Cả hai đều
    #    KHÔNG bị bắt bởi gate "vượt ranh giới scene" hay "chồng nhau trong track",
    #    vì scene vẫn đúng và track vẫn không chồng — đơn vị sai, không phải số sai.
    _b = sorted({x for a, b in all_segs for x in (a, b)})

    def _seg_i(fr):
        import bisect as _bi
        return _bi.bisect_right(_b, fr) - 1

    cross = []
    for _tid, _cl in (("trk-peak", peak), ("trk-sup1", sup1),
                      ("trk-sup2", sup2), ("trk-sup3", sup3)):
        for c in _cl:
            a, z = c["from"], c["from"] + c["durationInFrames"]
            if _seg_i(a) != _seg_i(max(a, z - 1)):
                cross.append(f"{_tid}/{c['id']} {a/FPS:.1f}s→{z/FPS:.1f}s")
    if cross:
        print(f"🔴 {len(cross)} clip sống XUYÊN qua lúc ảnh đổi (che ảnh mới / chú thích lạc):")
        for x in cross[:12]:
            print("   " + x)
        return 1
    # 🔴 gate này PHẢI cộng _EXT_TBL — nếu không nó đo khác `_rect()` dùng ở gate
    #    "lọt khỏi khung", và hai gate cùng đo một thứ bằng hai công thức thì cái
    #    lỏng hơn sẽ cho qua thứ cái chặt hơn bắt (đã dính đúng vậy ở video 19).
    if max(SW_TBL_Y) + SW_TBL + _EXT_TBL > HERO_BOTTOM:
        print(f"🔴 sticker bảng slot cuối chạm vùng phụ đề")
        return 1

    dupe = []
    for t in tracks:
        if t["type"] != "sticker":
            continue
        iv = sorted((c["from"], c["from"] + c["durationInFrames"], c["id"])
                    for c in t["clips"])
        for a, b in zip(iv, iv[1:]):
            if b[0] < a[1]:
                dupe.append(f"{t['id']}: {a[2]} × {b[2]}")
    if dupe:
        print(f"🔴 clip trùng thời gian trên CÙNG track: {len(dupe)} — {dupe[:6]}")
        return 1

    caps = proj["captions"]["lines"]
    longc = [c for c in caps if len(c["text"]) > CAP_MAX]
    print(f"   phụ đề: {len(lines)} dòng timeline → {len(caps)} khối · "
          f"dài nhất {max(len(c['text']) for c in caps)} ký (trần {CAP_MAX})")
    if longc:
        print(f"🔴 {len(longc)} khối phụ đề > {CAP_MAX} ký ⇒ sẽ ra ≥3 dòng:")
        for c in longc[:5]:
            print(f"     · {len(c['text'])} ký | {c['text'][:40]}")
        return 1
    if miss:
        print(f"🔴 THIẾU {len(miss)} asset:")
        for m in miss:
            print(f"     · {m}")
        return 1
    if lost:
        print(f"🔴 sticker lọt khỏi dải (cast sẽ đè): {lost}")
        return 1
    print(f"   ✓ {len(want)} asset đủ · mọi sticker trong dải")

    # ── GATE NHỊP HÌNH (audience-45plus.md §2.0, user chốt 2026-08-30) ──────────
    # Gọi tool DÙNG CHUNG, không chép logic vào đây: một phép đo, một chỗ sửa.
    # ⛔ Đừng gỡ gate này khi copy builder sang video sau — nó chính là thứ bắt được
    #    ca video 18 (87,2% thời lượng frame đứng yên, khe dài nhất 40,6s).
    pace = subprocess.run(
        [sys.executable, str(ML / "check_frame_pace.py"), str(out / "project.json")],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(pace.stdout.rstrip())
    if pace.returncode != 0:
        print("🔴 GATE NHỊP HÌNH ĐỎ — cách chữa in ở trên; luật: audience-45plus.md §2.0")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
