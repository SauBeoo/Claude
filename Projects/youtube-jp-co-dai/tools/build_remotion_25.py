# -*- coding: utf-8 -*-
r"""build_remotion_25.py — `project.json` Remotion cho video 25 (甕・行水盥, 16′41″).

⭐ ĐƯỜNG DỰNG MỚI CỦA KÊNH co-dai (user chốt 2026-08-27: *"render theo dạng video mới nhất
của nenkin"*). Chép khuôn `youtube-jp-nenkin/tools/build_remotion_17.py` (user đã duyệt qua
12 vòng demo), đổi đúng 4 thứ: đường dẫn kênh · cast ảnh thật của co-dai · phụ đề cỡ co-dai ·
nội dung SCENES/PUNCH/STAT của bài 25. ⛔ KHÔNG dùng make_vox/make_shot/video_render cho lớp
hình nữa — bảng vox cũ (bar/stat/compare/process/source/timeline) chuyển hết sang `papercut-stat`.

KHUÔN (không đổi so với nenkin):
  · khung 2 cast 2 mép, chân chạm y=1052 · hero = photocard giữa, trần theo CHIỀU CAO
  · scene có ẢNH → sticker NGOÀI ảnh, 2 góc TRÊN, 2 cái sống cùng lúc
  · scene có BẢNG → làn dọc bên phải bảng, 1-tại-1-lúc, KHÔNG hero
  · chữ = `papercut-banner` (tag + punch) · số liệu = `papercut-stat` / `papercut-formula`
  · scene neo bằng CHỈ SỐ DÒNG timeline (`L=`), không hardcode giây

KHÁC nenkin — 3 chỗ, mỗi chỗ có lý do:
  ① CAST là ảnh THẬT cắt nền (`_media_library/avatars/co-dai/_cut/*.png`, canvas 1376×768) ⇒
     builder tự crop bbox + đo ratio, KHÔNG hardcode CAST_RATIO (bài học nenkin: thêm 1 cast
     rộng là bóp dải cả video). Cast co-dai đứng thẳng, hẹp (ratio 0,33–0,61) ⇒ dải rộng hơn.
  ② Phụ đề co-dai cỡ 48 (template co-dai.json ghi 52; 44 của nenkin nhỏ so với hồ sơ outline/26
     của kênh). CaptionLayer maxWidth = 86% khung = 1651px ⇒ 48px chứa ~34 ký/dòng ⇒ CAP_MAX 66.
  ③ Sticker: dùng lại 5 sticker nenkin đúng nghĩa (coin/calendar/burst/teacup/newspaper) + 13
     sticker mới của bài (甕・植木鉢・盥…). Tái dùng sticker là cái rẻ của lớp này.

CHẠY:  python tools/build_remotion_25.py            # → remotion-vox/projects/co-dai-25/project.json
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
ML = Path(r"E:\Claude\Projects\_media_library")
NENKIN17 = RV / "public" / "projects" / "nenkin-17" / "assets"
STEM = "25_mizugame-suyaki-tarai"
NAME = "co-dai-25"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#F2B84B"
TAG_BG = "#F5D58A"                                  # chip tag phẳng, vàng ấm
PUNCH_COL = {INK: "#FFFFFF", RED: "#FF8A7A"}         # preset `punch`: nền đen, chữ = color

# ── CAST: ĐÃ BỎ (phương án C). Khoá l/r trong SCENES giữ lại nhưng KHÔNG dùng. ──────
CAST_MARGIN = 4
# ── HERO — trần theo CHIỀU CAO (nenkin: 140…900 ⇒ 1132px) ────────────────────
HERO_Y = 140
HERO_BOTTOM = 900
HW = round((HERO_BOTTOM - HERO_Y) * 1.49)
HX = (1920 - HW) // 2
SUP_ENTER0, SUP_ENTER1 = 0.12, 0.88
SUP_ROT = (-7, 7, -5)
# ⭐ PHƯƠNG ÁN C (user chốt 2026-08-28: *"làm C đi"*): BỎ CAST 2 mép — 2 người đứng y hệt ở
# 47/47 scene và sẽ lặp qua mọi video (khung nào cũng giống nhau). Hai dải bên x 0–394 ·
# 1526–1920 nay trống TRỌN chiều cao ⇒ 4 ô sticker (2 mỗi bên), 4 cái sống cùng lúc.
# Trần dọc: ô dưới y + 330 + ~20px phình xoay phải < 900 (vùng phụ đề) ⇒ 540/500.
OUT_W = 330
OUT_XY = ((1555, 110), (25, 185), (1555, 500), (25, 540))
OUT_ROT = (-6, 6, 5, -5)
TBL_INK_X1 = 1140
SW_TBL = 280
_EXT_TBL = round((SW_TBL * math.cos(math.radians(7))
                  + SW_TBL * math.sin(math.radians(7)) - SW_TBL) / 2) + 4
# nenkin dùng (250,480,610) — chỗ 610 + 280 + phần phình do xoay 5° = 901 > 900 với sticker
# vuông ⇒ gate "chạm phụ đề" bắt ngay lượt đầu. Hạ 20px là hết.
SW_TBL_Y = (250, 470, 590)

# ══════════════════════════════════════════════════════════════════════════════
# SCENES — `L` = chỉ số dòng timeline nơi scene BẮT ĐẦU (xem `timeline.json`).
#   hero : photocard `card_*` (None = vùng giữa để trống cho bảng)
#   sup  : sticker `el_*` (5 cái tái dùng từ nenkin-17: coin_stack/calendar/burst_red/teacup/newspaper)
#   l / r: cast trái (kataribe = người kể) / phải (haha = bà, đứng nghe)
#   sp   : 2 màu splash nền giấy
# 40 scene / 1001s = 25s/scene (nenkin 17: 39 scene / 843s).
# ══════════════════════════════════════════════════════════════════════════════
K_T, K_P, K_W = "kataribe_talk", "kataribe_point", "kataribe_wry"
H_T, H_B = "haha_talk", "haha_back"
EARTH, INDIGO, CREAM, CLAY, MOSS = "#B9765A", "#41536F", "#C8B88A", "#A65E3A", "#8A9A7B"

SCENES = [
    # ⭐ 2026-08-28 user: "sticker hầu như không trùng nhau" + "ảnh mở đầu phải gây shock".
    #   · mỗi scene ĐÚNG 2 sticker RIÊNG — không vật nào xuất hiện ở 2 scene (gate 🔴 bên dưới)
    #   · scene 0 = hero SHOCK 7s (căn hộ tối, người gục cạnh quạt đứng im, đèn cấp cứu) rồi
    #     mới vào bảng 39/33 — trước đó cold open mở bằng BẢNG, không có hình đâm.
    # ── 第1章 cold open: 100人 ────────────────────────────────────────────────
    dict(L=0,  tag="ある夏の夜",    hero="card_shock_yakan",   sup=["el_kyukyusha", "el_ondokei"],
         sp=[RED, INDIGO]),
    dict(L=1,  tag="都内で100人",  hero=None, sup=["el_tsuki_yoru", "el_burst_red"],
         sp=[RED, CREAM], stat="yakan"),
    dict(L=3,  tag="蛇口の水",     hero="card_jaguchi",       sup=["el_jaguchi", "el_te_no_kou"],
         sp=[INDIGO, CREAM]),
    dict(L=5,  tag="古代の秘訣",   hero="card_kame_daidokoro", sup=["el_mizugame", "el_hishaku"],
         sp=[CLAY, CREAM]),
    dict(L=6,  tag="生ぬるい麦茶",  hero="card_reizouko_mugicha", sup=["el_reizouko", "el_mugicha"],
         sp=[INDIGO, CREAM]),
    dict(L=10, tag="冷たい水、ありますか", hero="card_koppu_mizu", sup=["el_koppu", "el_mizu_shizuku"],
         sp=[CREAM, INDIGO]),
    dict(L=11, tag="冷やすには、時間", hero="card_reizouko_jikan", sup=["el_tokei", "el_remocon"],
         sp=[INDIGO, CREAM]),
    # ── 第2章 素焼きの仕組み ─────────────────────────────────────────────────
    dict(L=14, tag="祖母の甕",     hero="card_sobo_kame",     sup=["el_kappogi", "el_furoshiki"],
         sp=[CLAY, CREAM]),
    dict(L=16, tag="小さな穴",     hero="card_suyaki_macro",  sup=["el_uekibachi", "el_kakudai"],
         sp=[EARTH, CREAM]),
    dict(L=19, tag="蒸発が、熱を奪う", hero="card_kika_netsu", sup=["el_yuge", "el_koorimizu"],
         sp=[INDIGO, CREAM]),
    dict(L=22, tag="2〜6度",       hero=None, sup=["el_flask", "el_plug_off"],
         sp=[INDIGO, CREAM], stat="jikken"),
    # ── 第3章 自宅で確かめる ─────────────────────────────────────────────────
    dict(L=24, tag="植木鉢を二つ",  hero="card_uekibachi_futatsu", sup=["el_nasu", "el_bottle"],
         sp=[CLAY, CREAM]),
    dict(L=27, tag="手順",         hero=None, sup=["el_suna", "el_nureta_nuno"],
         sp=[CLAY, CREAM], stat="tejun"),
    dict(L=30, tag="半信半疑",     hero="card_yubisaki",      sup=["el_yubi", "el_hatena"],
         sp=[EARTH, CREAM]),
    dict(L=33, tag="大切なのは、風", hero="card_kaze_sukima", sup=["el_uchiwa", "el_kaze"],
         sp=[MOSS, CREAM]),
    dict(L=35, tag="数百円",       hero="card_homecenter",    sup=["el_coin_stack", "el_nefuda"],
         sp=[CREAM, CLAY]),
    dict(L=38, tag="天気を選ぶ",    hero="card_tenki",         sup=["el_taiyou", "el_amagumo"],
         sp=[INDIGO, CREAM]),
    # ── 第4章 乾いた土地の知恵 ───────────────────────────────────────────────
    dict(L=40, tag="乾いた土地",    hero="card_nigeria_kyoushi", sup=["el_tsubo_nijuu", "el_tomato"],
         sp=[EARTH, CREAM]),
    dict(L=43, tag="3日 → 27日",   hero=None, sup=["el_calendar", "el_medal"],
         sp=[EARTH, CREAM], stat="nasu"),
    dict(L=47, tag="停電のとき",    hero="card_camp_teiden",   sup=["el_lantern", "el_cooler"],
         sp=[INDIGO, CREAM]),
    # ── 第5章 美しい壺ほど、冷えない ─────────────────────────────────────────
    dict(L=49, tag="意外な事実",    hero=None, sup=["el_tsubo_tsuya", "el_kirakira"],
         sp=[CLAY, CREAM], stat="tsuya"),
    dict(L=53, tag="同じ土から",    hero="card_shigaraki",     sup=["el_kama", "el_tanuki"],
         sp=[EARTH, CREAM]),
    dict(L=56, tag="江戸の旅人",    hero="card_edo_tabibito",  sup=["el_tokkuri", "el_sugegasa"],
         sp=[CREAM, INDIGO]),
    # ── 第6章 祖母の記憶 ─────────────────────────────────────────────────────
    dict(L=58, tag="柄杓の音",     hero="card_hishaku",       sup=["el_hamon", "el_ido"],
         sp=[CLAY, CREAM]),
    dict(L=61, tag="ここにあるやろ", hero="card_sobo_kappogi", sup=["el_teacup", "el_tenugui"],
         sp=[CREAM, CLAY]),
    # ── 第7章 行水盥 ────────────────────────────────────────────────────────
    dict(L=65, tag="喉の渇きだけ",  hero="card_gutta",         sup=["el_keihou", "el_denwa"],
         sp=[RED, CREAM]),
    dict(L=69, tag="行水盥",       hero="card_gyouzui_tarai", sup=["el_tarai", "el_furin"],
         sp=[INDIGO, CREAM]),
    dict(L=73, tag="扇風機より早い", hero="card_hada_jouhatsu", sup=["el_senpuuki", "el_ase"],
         sp=[MOSS, CREAM]),
    dict(L=76, tag="ひとすくい",    hero="card_hitosukui",     sup=["el_take_hishaku", "el_shibuki"],
         sp=[INDIGO, CREAM]),
    dict(L=78, tag="ぬるめの水から", hero="card_chuui_nurume", sup=["el_koori_bucket", "el_batsu"],
         sp=[RED, CREAM]),
    dict(L=81, tag="救急の現場でも", hero=None, sup=["el_taoru", "el_kyukyu_bako"],
         sp=[INDIGO, CREAM], stat="kyukyu"),
    dict(L=83, tag="1枚のタオル",   hero="card_nure_taoru",    sup=["el_sensu", "el_kubi_taoru"],
         sp=[INDIGO, CREAM]),
    # ── 第8章 昭和の行水 ─────────────────────────────────────────────────────
    dict(L=85, tag="昭和の日課",    hero="card_showa_gyouzui", sup=["el_kuwa", "el_kaki"],
         sp=[CREAM, EARTH]),
    dict(L=88, tag="夕涼み",       hero="card_yuusuzumi",     sup=["el_katorisenko", "el_mugiwara"],
         sp=[CREAM, MOSS]),
    # ── CTA ─────────────────────────────────────────────────────────────────
    dict(L=91, tag="お願い",       hero="card_share_kazoku",  sup=["el_smartphone", "el_kyuusu"],
         sp=[CREAM, INDIGO]),
    # ── 第9章 なぜ消えたのか ─────────────────────────────────────────────────
    dict(L=94, tag="消えなかった盥", hero="card_vinyl_pool",   sup=["el_pool", "el_ukiwa"],
         sp=[INDIGO, CREAM]),
    dict(L=99, tag="なぜ消えたのか", hero="card_kieta_dougu",  sup=["el_kumonosu", "el_dry_flower"],
         sp=[CREAM, INDIGO]),
    dict(L=101, tag="1957年 → 1970年", hero=None, sup=["el_terebi", "el_sentakuki"],
         sp=[INDIGO, CREAM], stat="fukyu"),
    dict(L=104, tag="三種の神器",    hero="card_sanshu_jingi",  sup=["el_kamidana", "el_newspaper"],
         sp=[CREAM, INDIGO]),
    dict(L=107, tag="水道が届いた",  hero="card_suidou",        sup=["el_suidoukan", "el_baketsu"],
         sp=[INDIGO, CREAM]),
    dict(L=110, tag="いちばんの基本", hero="card_mizu_soba",   sup=["el_megane", "el_zabuton"],
         sp=[CREAM, INDIGO]),
    dict(L=113, tag="買うものに",    hero="card_denkidai",      sup=["el_fuutou", "el_horeizai"],
         sp=[EARTH, CREAM]),
    dict(L=117, tag="今も作る窯元",  hero="card_kamamoto_gendai", sup=["el_kame_modern", "el_fukuro"],
         sp=[CLAY, CREAM]),
    dict(L=119, tag="両方の役目",    hero="card_ryouhou",       sup=["el_tenbin", "el_plug"],
         sp=[CREAM, INDIGO]),
    # ── 第10章 答え + 締め ───────────────────────────────────────────────────
    dict(L=121, tag="あの確かめ方の答え", hero="card_suidoukan", sup=["el_concrete", "el_netsu"],
         sp=[INDIGO, CREAM]),
    dict(L=124, tag="両方、使える",  hero="card_kame_tarai_ryouyou", sup=["el_mado", "el_niwaki"],
         sp=[CREAM, CLAY]),
    dict(L=127, tag="0円の涼しさ",   hero="card_zero_en",       sup=["el_saifu", "el_hoshi"],
         sp=[CREAM, MOSS]),
    dict(L=130, tag="ご実家の記憶",  hero="card_jikka_kioku",   sup=["el_jitensha", "el_akari"],
         sp=[CREAM, EARTH]),
]

# banner PUNCH — chữ đâm, neo theo chỉ số dòng (mọi câu phải CÓ trong lời)
PUNCH = [
    (1,   "夜のほうが、多かった",        RED),
    (4,   "ぬるかったはずです",          INK),
    (8,   "エアコンはあるのに",          RED),
    (14,  "電気もないのに、なぜ",        INK),
    (17,  "小さな穴が、無数に",          INK),
    (20,  "まわりから熱を奪います",      INK),
    (23,  "電気を、一切使わずに",        RED),
    (29,  "30分もすれば",              INK),
    (37,  "今週末、試してみてください",   INK),
    (45,  "壺一つ。電気代0円。",         RED),
    (50,  "美しい壺ほど、この冷たさは生まれません", RED),
    (61,  "「ここにあるやろ」",          INK),
    (64,  "ただの水入れ",               INK),
    (69,  "行水盥",                    INK),
    (79,  "一気にかけるのは、おすすめできません", RED),
    (84,  "同じ一本の線で",             INK),
    (95,  "たらいそのものは、消えなかった", INK),
    (103, "たった13年",                RED),
    (114, "0円でできた涼しさが",        RED),
    (128, "0円の涼しさも、もう一つ",     INK),
]

# bảng số liệu — key khớp `stat=` ở SCENES. `*` = dòng nhấn (chỉ định tường minh).
STAT = {
    "yakan":  ("屋内で亡くなった|97人" + NL + "*夜間|39人" + NL + "日中|33人", 52),
    "jikken": ("食品メーカーの実験|電気なし" + NL + "*まわりの温度より|−2〜6度", 52),
    "tejun":  ("① 素焼きの鉢を二つ|大小" + NL + "② 小さい鉢に|ボトル・果物" + NL
               + "③ 鉢のあいだに|濡れた砂か布" + NL + "*④ 日陰で風を|30分", 44),
    "nasu":   ("収穫から|3日で傷む" + NL + "*二重の壺＋湿った砂|27日もつ" + NL
               + "トマト・唐辛子|3週間", 48),
    "tsuya":  ("*素焼き（つやなし）|◯ 冷える" + NL + "施釉（つやあり）|✕ 穴がふさがる", 48),
    "kyukyu": ("*首すじ|◯" + NL + "わきの下|◯" + NL + "太もものつけ根|◯", 52),
    "fukyu":  ("1957年|3軒／100軒" + NL + "*1970年|89軒／100軒", 52),
}

# ── phụ đề: co-dai fontSize 48 ⇒ ~34 ký/dòng ⇒ trần 1 khối (2 dòng) = 66 ký ────
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

    STAGE_X0, STAGE_X1 = HX, HX + HW          # không cast ⇒ dải sân khấu = chính span hero
    PX = STAGE_X0 + 20
    # Cast co-dai HẸP (303px) ⇒ dải sân khấu 1258px, rộng hơn nenkin 460px. Bảng 810px neo ở
    # STAGE_X0+16 như nenkin thì nửa phải khung trống hẳn (soi still frame 100). ⇒ CĂN GIỮA
    # bảng trong khe [STAGE_X0, làn sticker]; mực bảng ước ≤ x0+800 phải < làn sticker.
    STAT_X = 960 - 405                        # bảng căn giữa khung; sticker ở 2 dải bên

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
    # PUNCH phải là chuỗi CÓ trong lời của dòng đó (bỏ dấu ngoặc kép/chấm khi so)
    strip = lambda s: s.replace("「", "").replace("」", "").rstrip("。")   # noqa: E731
    badp = [(i, b) for i, b, _ in PUNCH if strip(b) not in lines[i]["text"]]
    if badp:
        print("🔴 PUNCH không nằm trong lời dòng đó:")
        for i, b in badp:
            print(f"     dòng {i}: {b}  |  {lines[i]['text'][:40]}")
        return 1

    # ⭐ STICKER ANIME CAO (nhiệt kế 216×664, quạt, tủ lạnh) — đặt theo BỀ NGANG 330 như nenkin
    # (sticker nenkin đều rộng) thì cao >1000px, gate bắt 12 cái lọt khung ngay lượt đầu.
    # ⇒ cỡ = vừa Ô VUÔNG cạnh S: w = S nếu rộng hơn cao, w = S·aspect nếu cao hơn rộng.
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
        print(f"🔴 sticker dùng ở >1 scene (user: hầu như không trùng): {_dup}")
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
        tbl = bool(s.get("stat") or s.get("formula"))
        sups = s.get("sup") or []
        n = len(sups)
        st = [f + max(18, int(d * (SUP_ENTER0 + i * (SUP_ENTER1 - SUP_ENTER0) / n)))
              for i in range(n)]
        # mọi scene (ảnh lẫn bảng) dùng 4 ô dải bên; tiếp sức trong cùng ô khi >4
        npos = len(OUT_XY)
        step = npos
        for j, el in enumerate(sups):
            trk = (sup1, sup2, sup3, sup4)[j % 4]
            f0 = st[j]
            nxt = j + step
            fend = st[nxt] if nxt < n else to
            sx, sy = OUT_XY[j % npos]
            sw = fitw(el, OUT_W)
            sx += (OUT_W - sw) // 2
            rot = OUT_ROT[j % npos]
            trk.append(stick(f"s{j}-{k}", el, f0, fend - f0, sx, sy, sw,
                             rot=rot, ent="pop", amp=5, ph=1.2 + j * 2, sh="sm"))
        # ANIME (user chốt 2026-08-27): bỏ mọi preset cắt giấy. tag = chip phẳng màu ấm,
        # punch = hộp đen chữ sáng (khuôn okura), bảng = `flat-stat` (ô bo tròn, không nghiêng).
        tag.append(txt(f"tag-{k}", s["tag"], f + 4, d - 4, "tag", color=TAG_BG,
                       layout={"x": 74, "y": 58}, size=60))
        if s.get("stat"):
            body, sz = STAT[s["stat"]]
            f_st = f + max(20, int(d * 0.10))
            # không cast + không hero ⇒ bảng đứng một mình giữa khung: phóng ×1,3 (cỡ cũ tune
            # cho làn 810px cạnh cast của nenkin), hộp rộng 1050, canh giữa.
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

    # 🔴 PUNCH neo đáy (bottom:110, khuôn okura/nenkin) ĐÈ LÊN PHỤ ĐỀ 2 dòng — soi still frame
    # 300/1100: hộp đen nằm ngay trên dòng sub thứ nhất. Hero chiếm tới y=900, sub từ ~890 ⇒
    # đáy khung KHÔNG còn khe. Chỗ trống thật là DẢI TRÊN, bên phải chip tag (tag rộng
    # ≈ 60px×ký + 68 pad) tới mép sticker góc phải (x=1555). ⇒ punch lên y=58, một dòng,
    # font tự co cho vừa khe; scene nào tag dài thì punch nhỏ hơn, không bao giờ wrap.
    def scene_of(fr):
        return next(s for s in reversed(SCENES) if s["f"] <= fr)

    for idx, body, col in PUNCH:
        f = F(idx)
        end = round(lines[idx]["end"] * FPS)
        sc = scene_of(f)
        x0 = 74 + len(sc["tag"]) * 60 + 68 + 36
        avail = 1555 - 24 - x0 - 60                    # trừ padding 30×2 của preset
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
                 "createdAt": "2026-08-27T00:00:00.000Z",
                 "modifiedAt": "2026-08-27T00:00:00.000Z"},
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

    # ── ASSET: gom về public/projects/co-dai-25/assets ─────────────────────────
    ad = RV / "public" / "projects" / NAME / "assets"
    ad.mkdir(parents=True, exist_ok=True)
    for p in list((vd / "photocard").glob("*.png")) + list((vd / "sticker").glob("*.png")):
        shutil.copy(p, ad / p.name)
    if not (ad / "voice.mp3").exists() or \
            (ad / "voice.mp3").stat().st_mtime < (vd / "voice.wav").stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-i", str(vd / "voice.wav"), "-c:a", "libmp3lame",
                        "-q:a", "2", str(ad / "voice.mp3")], check=True, capture_output=True)

    want = {c["asset"].split("/")[-1] for t in tracks if t["type"] == "sticker"
            for c in t["clips"]} | {"voice.mp3"}
    miss = sorted(w for w in want if not (ad / w).exists())

    # ── GATE không-gian (chép nenkin, hộp đã tính phép xoay) ───────────────────
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

    # hero lặp — chỉ báo, lặp cố ý thì ghi rõ ở SCENES
    import collections
    cnt = collections.Counter(s["hero"] for s in SCENES if s.get("hero"))
    rep = [(v, k) for k, v in cnt.items() if v > 1]

    ns = sum(len(t["clips"]) for t in tracks if t["type"] == "sticker")
    nt = sum(len(t["clips"]) for t in tracks if t["type"] == "text")
    caps = proj["captions"]["lines"]
    print(f"✓ {out / 'project.json'}")
    print(f"   {DUR} frame ({DUR/FPS/60:.2f}′) · {len(SCENES)} scene "
          f"({len(SCENES)/(DUR/FPS/60):.2f}/phút) · {ns} sticker · {nt} text")
    print(f"   KHÔNG cast (phương án C) · HERO {HW}px = {HW*100//1920}% khung · "
          f"màn 390px ≈ {round(HW*390/1920)}px · 4 ô sticker 2 dải bên")
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
