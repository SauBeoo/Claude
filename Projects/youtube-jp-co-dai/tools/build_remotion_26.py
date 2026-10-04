# -*- coding: utf-8 -*-
r"""build_remotion_26.py — `project.json` Remotion cho video 26 (障子・呼吸する紙, 16'46").

Chép khuôn `build_remotion_25.py` (đã duyệt), đổi: đường dẫn/tên · SCENES/PUNCH/STAT theo nội
dung ミツエさん + 障子. Cùng khuôn ANIME, KHÔNG cast (phương án C), 4 ô sticker 2 dải bên.

CHẠY:  python tools/build_remotion_26.py            # → remotion-vox/projects/co-dai-26/project.json
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
STEM = "26_shoji-kokyuu-kami"
NAME = "co-dai-26"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#F2B84B"
TAG_BG = "#F5D58A"
PUNCH_COL = {INK: "#FFFFFF", RED: "#FF8A7A"}

# ── khuôn khung (giữ nguyên như video 25 — phương án C, không cast) ──────────────
HERO_Y = 140
HERO_BOTTOM = 900
HW = round((HERO_BOTTOM - HERO_Y) * 1.49)
HX = (1920 - HW) // 2
SUP_ENTER0, SUP_ENTER1 = 0.12, 0.88
OUT_W = 330
OUT_XY = ((1555, 110), (25, 185), (1555, 500), (25, 540))
OUT_ROT = (-6, 6, 5, -5)

K_T, K_P = "kataribe_talk", "kataribe_point"  # giữ chữ ký cũ, không dùng (không cast)
EARTH, INDIGO, CREAM, CLAY, MOSS, MUSTARD = \
    "#B9765A", "#41536F", "#C8B88A", "#A65E3A", "#8A9A7B", "#C99A3E"

# ══════════════════════════════════════════════════════════════════════════════
# SCENES — L = chỉ số dòng timeline.json nơi scene BẮT ĐẦU (49 dòng, xem timeline.json).
# 46 scene / 1005s ≈ 21,8s/scene. Bỏ neo ở dòng 2 (marker), 3 và 35 (gộp vào scene liền trước
# vì <6s nếu tách riêng — xem phép tính trong ghi chú đầu phiên).
# ══════════════════════════════════════════════════════════════════════════════
SCENES = [
    # ── 第1章 窓辺の謎（コールドオープン） ──────────────────────────────────
    dict(L=0,  tag="窓辺の異変",     hero="card_mado_shimi",      sup=["el_yubisaki", "el_shimi_ten"],
         sp=[INDIGO, CREAM]),
    dict(L=1,  tag="カビでした",     hero="card_kabi_macro",      sup=["el_mushimegane", "el_yubi_sasu"],
         sp=[INDIGO, CREAM]),
    dict(L=4,  tag="半年前の決断",   hero="card_curtain_koukan",  sup=["el_neko_sakeru", "el_juushi_curtain"],
         sp=[CREAM, INDIGO]),
    dict(L=5,  tag="洗剤のせいでは", hero="card_gimon_kaji",      sup=["el_senzai_bin", "el_kanki_mado"],
         sp=[CREAM, CLAY]),
    dict(L=6,  tag="隠れた力",       hero="card_kami_hikari",     sup=["el_kami_ichimai", "el_hatena_ai"],
         sp=[INDIGO, CREAM]),
    dict(L=7,  tag="古代の秘訣",     hero="card_furui_ie_gaikan", sup=["el_noren", "el_niwaki"],
         sp=[CREAM, MOSS]),
    # ── 第2章 数字で分かる性能 ──────────────────────────────────────────────
    dict(L=8,  tag="ただの飾り？",   hero="card_mitsue_utagai",   sup=["el_shouji_koma", "el_hatena_dai"],
         sp=[CREAM, INDIGO]),
    dict(L=9,  tag="6.0→4.8",       hero=None, sup=["el_ondokei", "el_mado_danmen"],
         sp=[INDIGO, CREAM], stat="netsukanryu"),
    dict(L=10, tag="熱の量、半分に", hero=None, sup=["el_taiyou_ya", "el_yajirushi_ao"],
         sp=[INDIGO, CREAM], stat="netsutuka"),
    dict(L=11, tag="まだ序章です",   hero="card_mitsue_samuke",   sup=["el_kutsushita", "el_kaze_samu"],
         sp=[INDIGO, CREAM]),
    # ── 第3章 破れない障子紙、という罠 ─────────────────────────────────────
    dict(L=12, tag="大きな見落とし", hero="card_kasoku_hikaku",   sup=["el_purasuchikku_maki", "el_kagayaki"],
         sp=[CREAM, INDIGO]),
    dict(L=13, tag="破れない。色あせない。", hero="card_urikoba", sup=["el_nefuda_shiro", "el_hoshi_kagayaki"],
         sp=[CREAM, MUSTARD]),
    dict(L=14, tag="呼吸です",       hero="card_kami_iki",        sup=["el_senni_kirakira", "el_iki_moya"],
         sp=[CREAM, INDIGO]),
    dict(L=15, tag="見えないすきま", hero="card_washi_sen_macro", sup=["el_kensabikyou", "el_shitsuke_moya"],
         sp=[CREAM, INDIGO]),
    dict(L=16, tag="水滴となって",   hero="card_ketsuro_mado",    sup=["el_suiteki_retsu", "el_atatakai_kuuki"],
         sp=[INDIGO, CREAM]),
    dict(L=17, tag="皮肉なものです", hero="card_mitsue_kizuku",   sup=["el_kaaten_nunoji", "el_toho_kao"],
         sp=[INDIGO, CREAM]),
    dict(L=18, tag="湿度計を二つ",   hero="card_shitsudokei",     sup=["el_shitsudokei", "el_mado_kanki"],
         sp=[CREAM, MOSS]),
    # ── 第4章 もう一つの秘密（水と蝋の知恵） ───────────────────────────────
    dict(L=19, tag="呼吸を守るには", hero="card_shouji_taisetsu", sup=["el_te_yasashiku", "el_kami_kagayaki"],
         sp=[CREAM, INDIGO]),
    dict(L=20, tag="霧吹きの理由",   hero="card_shokunin_mizu",   sup=["el_kirifuki", "el_nori_bake"],
         sp=[CREAM, CLAY]),
    dict(L=21, tag="太鼓の皮のように", hero="card_taiko_hari",    sup=["el_taiko_kawa", "el_kansou_kage"],
         sp=[CREAM, MOSS]),
    dict(L=22, tag="少し感動しました", hero="card_watashi_taiken", sup=["el_kirifuki_bin", "el_pin_to"],
         sp=[CREAM, MUSTARD]),
    dict(L=23, tag="雪国の太鼓張り", hero="card_taikobari_yukiguni", sup=["el_yuki_mado", "el_kumiko_ryoumen"],
         sp=[INDIGO, CREAM]),
    dict(L=24, tag="材料費",         hero=None, sup=["el_daiso_kago", "el_kattaa2"],
         sp=[CREAM, CLAY], stat="zairyouhi"),
    dict(L=25, tag="西向きは早い",   hero="card_nishimuki_taiyou", sup=["el_taiyou_nishi", "el_kouyoku_kami"],
         sp=[MUSTARD, CREAM]),
    dict(L=26, tag="刃物に気をつけて", hero="card_kodomo_anzen",  sup=["el_kattaa_ha", "el_hikari_kazashi"],
         sp=[CREAM, CLAY]),
    dict(L=27, tag="でんぷんの糊",   hero="card_nori_hagasu",     sup=["el_taoru_nure", "el_airon"],
         sp=[CREAM, INDIGO]),
    # ── 第5章 敷居のろうそく ────────────────────────────────────────────────
    dict(L=28, tag="ホコリを呼び込む", hero="card_rousoku_shikii", sup=["el_rousoku", "el_souji_ki"],
         sp=[CLAY, CREAM]),
    dict(L=29, tag="夕暮れの光",     hero="card_kodomo_ana",      sup=["el_yuuhi_kage", "el_yubi_ana"],
         sp=[MUSTARD, CREAM]),
    dict(L=30, tag="母の記憶",       hero="card_haha_natsukashi", sup=["el_omoide_frame", "el_hohoemi"],
         sp=[CREAM, MOSS]),
    # ── 第6章 忘れられた理由（歴史） ────────────────────────────────────────
    dict(L=31, tag="当たり前の謎",   hero="card_nazo_toi",        sup=["el_hatena_shiro", "el_toji_mon"],
         sp=[INDIGO, CREAM]),
    dict(L=32, tag="武家だけのもの", hero="card_bushi_akari_shouji", sup=["el_bushi_katana", "el_washi_maki"],
         sp=[CLAY, CREAM]),
    dict(L=33, tag="職人の数",       hero=None, sup=["el_shokunin_te", "el_gurafu_ochiru"],
         sp=[CLAY, CREAM], stat="shokunin"),
    dict(L=34, tag="恥ずかしい話",   hero="card_watashi_machigai", sup=["el_shouji_ura", "el_warau_haha"],
         sp=[CREAM, MUSTARD]),
    # ── CTA ─────────────────────────────────────────────────────────────────
    dict(L=36, tag="お願い",         hero="card_share_onegai",    sup=["el_smartphone_ai", "el_kyuusu_cha"],
         sp=[CREAM, INDIGO]),
    # ── 第7章 静かに姿を消したもの ──────────────────────────────────────────
    dict(L=37, tag="静かに姿を消した", hero="card_kieta_dougu",   sup=["el_kumo_no_su", "el_hokori"],
         sp=[INDIGO, CREAM]),
    dict(L=38, tag="国が売るもの",   hero="card_kuni_uchimado",   sup=["el_fuutou_kuni", "el_hyou_shou"],
         sp=[INDIGO, CREAM]),
    dict(L=39, tag="国の補助金",     hero=None, sup=["el_kouji_gyousha", "el_uchimado_zu"],
         sp=[INDIGO, CREAM], stat="hojokin"),
    dict(L=40, tag="祖父母はすでに", hero="card_sofubo_shouji",   sup=["el_sofubo_kage", "el_dougu_bako"],
         sp=[CREAM, CLAY]),
    dict(L=41, tag="同じ原理",       hero="card_kuuki_sou_hikaku", sup=["el_garasu_nimai", "el_kuuki_sou"],
         sp=[INDIGO, CREAM]),
    dict(L=42, tag="最後の話",       hero="card_kaisou_boutou",   sup=["el_kaisou_moya", "el_kami_hikari2"],
         sp=[INDIGO, CREAM]),
    dict(L=43, tag="無料で取り戻す", hero="card_muryou_kaifuku",  sup=["el_te_kakeru", "el_muryou_fuda"],
         sp=[CREAM, MOSS]),
    # ── 第8章 結び ──────────────────────────────────────────────────────────
    dict(L=44, tag="万能ではない",   hero="card_bouhan_amado",    sup=["el_amado", "el_kagi"],
         sp=[CLAY, CREAM]),
    dict(L=45, tag="紙かガラスか",   hero="card_kumiawase",       sup=["el_tenbin_kami_garasu", "el_wa"],
         sp=[CREAM, INDIGO]),
    dict(L=46, tag="ミツエさんの結末", hero="card_mitsue_kaiketsu", sup=["el_neko_marumaru", "el_kansou_mado"],
         sp=[CREAM, MOSS]),
    dict(L=47, tag="あなたの家は",   hero="card_shichou_toikake", sup=["el_toikake_kumo", "el_comment_fukidashi"],
         sp=[CREAM, INDIGO]),
    dict(L=48, tag="また次の知恵で", hero="card_shimei_tojiru",   sup=["el_andon_akari", "el_tsuki_shime"],
         sp=[INDIGO, CREAM]),
]

# banner PUNCH — chữ đâm, neo theo chỉ số dòng (mọi câu phải CÓ trong lời của DÒNG đó)
PUNCH = [
    (0,  "じっとりと湿った感じ",      INK),
    (1,  "カビでした",              RED),
    (4,  "なぜか窓辺を避け",        INK),
    (6,  "いちばん奇妙なその力",     RED),
    (9,  "4.8まで下がる",           INK),
    (10, "熱の量が、ほぼ半分に",     INK),
    (12, "大きな見落とし",          RED),
    (13, "破れない。色あせない。長持ちする。", INK),
    (14, "呼吸です",                RED),
    (16, "水滴となって現れます",     INK),
    (17, "皮肉なものです",          RED),
    (21, "ぴんと張った状態になる",   INK),
    (22, "ぴんと張った、あの瞬間",   INK),
    (25, "変色が早く進む",          INK),
    (28, "ホコリを呼び込む",        RED),
    (32, "武家や、裕福な商人だけ",   INK),
    (33, "6万人まで減り",           RED),
    (38, "まったく違う金額で",       RED),
    (41, "同じ原理で働いています",   INK),
    (42, "同じ一つの原理でした",     RED),
    (46, "また、その窓辺で丸くなる", INK),
]

# bảng số liệu — key khớp `stat=` ở SCENES. `*` = dòng nhấn.
STAT = {
    "netsukanryu": ("ガラス1枚|6.0" + NL + "*障子を足すと|4.8" + NL + "体感温度|2〜3度上昇", 46),
    "netsutuka":   ("障子なし|熱の9割が通過" + NL + "*障子を足すと|4〜5割に半減", 46),
    "zairyouhi":   ("障子紙|100円〜4000円" + NL + "*業者に頼むと|2000円〜15000円", 46),
    "shokunin":    ("1983年|職人 28万人" + NL + "*2016年|職人 6万人" + NL + "生産額|5400億円→960億円", 40),
    "hojokin":     ("内窓1箇所|最大14万円" + NL + "*戸建て全体|最大100万円", 48),
}

# ── phụ đề: co-dai fontSize 48 ⇒ trần 1 khối (2 dòng) = 66 ký ─────────────────
CAP_SIZE = 48
CAP_MAX = 66
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


def txt(i, content, f, dur, preset, color=INK, layout=None, size=None):
    return {"id": i, "kind": "text", "from": f, "durationInFrames": max(1, dur),
            "content": content, "preset": preset, "color": color,
            "animation": "pop", "animationParams": {"restDeg": -1.5},
            "layout": layout or {}, "fontSize": size}


def main():
    vd = PROJ / "06_VIDEO" / STEM
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines = tl["lines"]
    F = lambda idx: round(lines[idx]["start"] * FPS)          # noqa: E731
    DUR = round(tl["total"] * FPS)

    STAGE_X0, STAGE_X1 = HX, HX + HW
    STAT_X = 960 - 405

    for k, s in enumerate(SCENES):
        s["f"] = F(s["L"])
        s["to"] = F(SCENES[k + 1]["L"]) if k + 1 < len(SCENES) else DUR
    bad = [f"  scene {k} (dòng {s['L']}) chỉ {(s['to']-s['f'])/FPS:.1f}s"
           for k, s in enumerate(SCENES) if s["to"] - s["f"] < 6 * FPS]
    if bad:
        print("🔴 scene ngắn hơn 6s (audience-45plus §2 mục 2):" + NL + NL.join(bad))
        return 1
    clash = [f"  scene {k} tag={s['tag']}" for k, s in enumerate(SCENES)
             if (s.get("stat") or s.get("formula")) and s.get("hero")]
    if clash:
        print("🔴 scene có bảng MÀ VẪN có hero:" + NL + NL.join(clash))
        return 1
    strip = lambda s: s.replace("「", "").replace("」", "").rstrip("。")   # noqa: E731
    badp = [(i, b) for i, b, _ in PUNCH if strip(b) not in lines[i]["text"]]
    if badp:
        print("🔴 PUNCH không nằm trong lời dòng đó:")
        for i, b in badp:
            print(f"     dòng {i}: {b}  |  {lines[i]['text'][:40]}")
        return 1

    stk_dir = vd / "sticker"
    _asp = {}
    for p in stk_dir.glob("el_*.png"):
        with Image.open(p) as im:
            _asp[p.stem] = im.width / im.height
    fitw = lambda el, S: S if _asp.get(el, 1.0) >= 1 else round(S * _asp[el])   # noqa: E731

    import collections as _c
    _use = _c.Counter(e for sc in SCENES for e in sc.get("sup", []))
    _dup = [(e, n) for e, n in _use.items() if n > 1]
    if _dup:
        print(f"🔴 sticker dùng ở >1 scene (mỗi vật chỉ 1 scene): {_dup}")
        return 1
    trk_bg, hero, sup1, sup2, sup3, sup4 = [], [], [], [], [], []
    tag, punch, stat, formula = [], [], [], []
    ENTS = ["grow", "rise", "flip", "zoom-through"]

    for k, s in enumerate(SCENES):
        f, to = s["f"], s["to"]
        d = to - f
        trk_bg.append(dict(id=f"bg-{k}", kind="background", **{"from": f},
                           durationInFrames=d, paper=None,
                           tint="#FBF5E8", tintOpacity=1.0, grid=False, dots=False,
                           splash=s["sp"]))
        if s.get("hero"):
            hero.append(stick(f"h-{k}", s["hero"], f + 6, d - 6, HX, HERO_Y, HW,
                              ent=ENTS[k % 4], amp=5))
        # ⛔⛔ KHỐI NÀY ĐÃ BỊ USER KẾT ÁN — ĐỪNG COPY SANG VIDEO 27+ (user chốt 2026-08-31,
        # xem memory `feedback_sticker_1_lan_vao_sau_hero_2s`): *"cứ lập đi lập lại 1 sticker
        # rồi thay đổi vị trí... rất nhàm. 1 Sticker chỉ xuất hiện ở 1 frame 1 lần thôi.
        # Sticker nên xuất hiện sau khi ảnh xuất hiện tầm 2s"*.
        # Pulse-lặp-file dưới đây đạt gate máy 7s nhưng MẮT thấy lặp ⇒ builder video sau phải:
        #   ① 1 sticker = vào ĐÚNG 1 lần/scene (cấm i % n xoay vòng cùng file)
        #   ② sticker đầu vào ở hero + ~60 frame (2s), các sticker sau giãn ~5-6s
        #   ③ đạt sàn 7s bằng: bật `exit` (rút đi = 1 sự kiện, check_frame_pace đếm cả exit)
        #      + scene >20s thì THÊM FILE sticker mới vào SCENES (~1 sticker/5-6s), đúng bài
        #      "tăng số FILE, GIỮ số lượt" của audience-45plus §2.0.
        # ---- (lịch sử) SÀN 7s bản video 26: xoay vòng lặp 2 sticker qua 4 vị trí ~5.5s/lượt ----
        sups = s.get("sup") or []
        n = len(sups)
        npos = len(OUT_XY)
        PULSE = 165                                    # ~5.5s/nhịp @30fps, dưới trần 210 (7s)
        n_beats = max(n, math.ceil(d / PULSE)) if n else 0
        if n_beats:
            edges = [f + round(i * d / n_beats) for i in range(n_beats + 1)]
            for i in range(n_beats):
                el = sups[i % n]
                slot = i % npos
                trk = (sup1, sup2, sup3, sup4)[slot]
                f0, f1 = edges[i], edges[i + 1]
                sx, sy = OUT_XY[slot]
                sw = fitw(el, OUT_W)
                sx += (OUT_W - sw) // 2
                rot = OUT_ROT[slot]
                trk.append(stick(f"s{i}-{k}", el, f0, f1 - f0, sx, sy, sw,
                                 rot=rot, ent=ENTS[i % 4], amp=5, ph=1.2 + i * 0.7, sh="sm"))
        tag.append(txt(f"tag-{k}", s["tag"], f + 4, d - 4, "tag", color=TAG_BG,
                       layout={"x": 74, "y": 58}, size=60))
        if s.get("stat"):
            body, sz = STAT[s["stat"]]
            f_st = f + max(20, int(d * 0.10))
            sz = round(sz * 1.3)
            stat.append(txt(f"st-{k}", body, f_st, to - f_st - 4, "flat-stat",
                            color=AMBER, layout={"x": 960 - 525, "y": 210, "w": 1050},
                            size=sz))
        if s.get("formula"):
            off = 150 if s.get("stat") else 0
            formula.append(txt(f"fm-{k}", s["formula"], f + int(d * 0.55),
                               d - int(d * 0.55) - 6, "papercut-formula", color=AMBER,
                               layout={"x": STAT_X, "y": 430 + off, "w": 830},
                               size=58))

    def scene_of(fr):
        return next(s for s in reversed(SCENES) if s["f"] <= fr)

    for idx, body, col in PUNCH:
        f = F(idx)
        end = round(lines[idx]["end"] * FPS)
        sc = scene_of(f)
        x0 = 74 + len(sc["tag"]) * 60 + 68 + 36
        avail = 1555 - 24 - x0 - 60
        size = int(min(46, avail / max(1, len(body)) * 0.98))
        if size < 30:
            print(f"⚠ punch dòng {idx} chỉ còn font {size} (tag '{sc['tag']}' dài) — rút ngắn 1 trong 2")
        punch.append(txt(f"p-{idx}", body, f + 8, max(60, end - f - 8),
                         "punch", color=PUNCH_COL[col],
                         layout={"x": x0, "y": 58, "w": avail + 60}, size=size))

    T = lambda i, n, ty, c: {"id": i, "name": n, "type": ty, "muted": False,   # noqa: E731
                             "hidden": False, "locked": False, "clips": c}
    tracks = [
        T("trk-bg", "nền giấy", "background", trk_bg),
        T("trk-hero", "hero ảnh", "sticker", hero),
        T("trk-sup1", "phụ 1", "sticker", sup1),
        T("trk-sup2", "phụ 2", "sticker", sup2),
        T("trk-sup3", "phụ 3", "sticker", sup3),
        T("trk-sup4", "phụ 4", "sticker", sup4),
        T("trk-stat", "bảng số liệu", "text", stat),
        T("trk-formula", "công thức", "text", formula),
        T("trk-tag", "tag", "text", tag),
        T("trk-punch", "punch", "text", punch),
        T("trk-voice", "giọng", "audio",
          [{"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
            "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]),
    ]
    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "co-dai", "templateRef": "co-dai", "fps": FPS,
                 "width": 1920, "height": 1080,
                 "createdAt": "2026-08-30T00:00:00.000Z",
                 "modifiedAt": "2026-08-30T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        "sceneMarkers": [{"id": f"sc-{k}", "atFrame": s["f"], "label": s["tag"]}
                         for k, s in enumerate(SCENES)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": CAP_SIZE,
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
    for p in list((vd / "photocard").glob("*.png")) + list((vd / "sticker").glob("*.png")):
        shutil.copy(p, ad / p.name)
    if (vd / "voice.wav").exists() and (not (ad / "voice.mp3").exists() or
            (ad / "voice.mp3").stat().st_mtime < (vd / "voice.wav").stat().st_mtime):
        subprocess.run(["ffmpeg", "-y", "-i", str(vd / "voice.wav"), "-c:a", "libmp3lame",
                        "-q:a", "2", str(ad / "voice.mp3")], check=True, capture_output=True)

    want = {c["asset"].split("/")[-1] for t in tracks if t["type"] == "sticker"
            for c in t["clips"]} | {"voice.mp3"}
    miss = sorted(w for w in want if not (ad / w).exists())

    aspect = {}
    for p in ad.glob("*.png"):
        with Image.open(p) as im:
            aspect[p.name] = im.width / im.height

    def _rect(c):
        L = c["layout"]
        w = L["w"]
        h = w / aspect.get(c["asset"].split("/")[-1], 1.0)
        th = math.radians(abs(L.get("rotation", 0)))
        ww = w * math.cos(th) + h * math.sin(th)
        hh = h * math.cos(th) + w * math.sin(th)
        cx, cy2 = L["x"] + w / 2, L["y"] + h / 2
        return (cx - ww / 2, cy2 - hh / 2, cx + ww / 2, cy2 + hh / 2)

    def _hit(a, b, pad=0):
        return (a[0] < b[2] - pad and b[0] < a[2] - pad
                and a[1] < b[3] - pad and b[1] < a[3] - pad)

    supclips = [c for t in tracks if t["id"].startswith("trk-sup")
                for c in t["clips"]]
    tbl_scene = {k for k, s in enumerate(SCENES) if s.get("stat") or s.get("formula")}
    heroR = (HX, HERO_Y, HX + HW, HERO_BOTTOM)
    lost, onhero = [], []
    for c in supclips:
        k = int(c["id"].split("-")[1])
        r = _rect(c)
        if r[0] < 4 or r[2] > 1916 or r[1] < 4 or r[3] > HERO_BOTTOM:
            lost.append(c["id"])
        if k not in tbl_scene and _hit(r, heroR, pad=6):
            onhero.append(c["id"])
    pairs = []
    for i, a in enumerate(supclips):
        for b in supclips[i + 1:]:
            if a["from"] < b["from"] + b["durationInFrames"] \
               and b["from"] < a["from"] + a["durationInFrames"] \
               and _hit(_rect(a), _rect(b), pad=6):
                pairs.append((a["id"], b["id"]))
    for lab, badl in (("lọt khỏi khung / chạm phụ đề", lost), ("ĐÈ LÊN ẢNH HERO", onhero),
                      ("đè lên nhau", pairs)):
        if badl:
            print(f"🔴 sticker {lab}: {len(badl)} — {badl[:8]}")
            return 1
    dupe = []
    for t in tracks:
        if t["type"] != "sticker":
            continue
        iv = sorted((c["from"], c["from"] + c["durationInFrames"], c["id"]) for c in t["clips"])
        for a, b in zip(iv, iv[1:]):
            if b[0] < a[1]:
                dupe.append(f"{t['id']}: {a[2]} × {b[2]}")
    if dupe:
        print(f"🔴 clip trùng thời gian trên CÙNG track: {dupe[:6]}")
        return 1

    import collections
    cnt = collections.Counter(s["hero"] for s in SCENES if s.get("hero"))
    rep = [(v, k) for k, v in cnt.items() if v > 1]

    ns = sum(len(t["clips"]) for t in tracks if t["type"] == "sticker")
    nt = sum(len(t["clips"]) for t in tracks if t["type"] == "text")
    caps = proj["captions"]["lines"]
    print(f"✓ {out / 'project.json'}")
    print(f"   {DUR} frame ({DUR/FPS/60:.2f}′) · {len(SCENES)} scene "
          f"({len(SCENES)/(DUR/FPS/60):.2f}/phút) · {ns} sticker · {nt} text")
    print(f"   KHÔNG cast (phương án C) · HERO {HW}px = {HW*100//1920}% khung · 4 ô sticker 2 dải bên")
    print(f"   scene ngắn nhất {min((s['to']-s['f'])/FPS for s in SCENES):.1f}s · "
          f"dài nhất {max((s['to']-s['f'])/FPS for s in SCENES):.1f}s")
    print(f"   phụ đề: {len(lines)} dòng → {len(caps)} khối · dài nhất "
          f"{max(len(c['text']) for c in caps)} ký (trần {CAP_MAX}, cỡ {CAP_SIZE})")
    nh = sum(1 for s in SCENES if s.get("hero"))
    print(f"   ảnh cần: {nh} photocard · "
          f"{len({e for s in SCENES for e in s.get('sup', [])})} sticker · "
          f"hero lặp: {rep or 'không'}")
    longc = [c for c in caps if len(c["text"]) > CAP_MAX]
    if longc:
        print(f"🔴 {len(longc)} khối phụ đề > {CAP_MAX} ký")
        return 1
    if miss:
        print(f"🔴 THIẾU {len(miss)} asset (chưa được render — render-background §1.5):")
        for m in miss:
            print(f"     · {m}")
        return 1
    print(f"   ✓ {len(want)} asset đủ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
