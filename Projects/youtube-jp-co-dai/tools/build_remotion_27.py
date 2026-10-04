# -*- coding: utf-8 -*-
r"""build_remotion_27.py — `project.json` Remotion cho video 27 (換気扇の油・灰汁と鹸化, 23'36").

Chép khuôn `build_remotion_26.py`, đổi: đường dẫn/tên · SCENES/PUNCH/STAT theo nội dung
節子さん + 換気扇の油 + 灰汁/鹸化. Cùng khuôn ANIME, KHÔNG cast (phương án C).

⭐ KHÁC video 26 — SỬA LỚP STICKER (user kết án 2026-08-31, xem
`feedback_sticker_1_lan_vao_sau_hero_2s`): video 26 xoay vòng LẶP 2 sticker qua 4 vị trí
mỗi ~5,5s ("pulse scheduler") — máy sạch gate nhưng mắt thấy nhàm. Từ video 27:
  ① 1 sticker = ĐÚNG 1 lần xuất hiện trong scene của nó (không xoay vòng lặp file).
  ② Sticker đầu vào SAU hero ~2s (60 frame).
  ③ Sàn 7-9s trả bằng `exit` (rút đi = 1 sự kiện, check_frame_pace đếm) + scene dài thì
     SCENES khai nhiều sup hơn (2 cho scene ≤~20s, 3 cho scene >~28s) — KHÔNG lặp file cũ.
Hàm `schedule_stickers()` thay hẳn khối "pulse" cũ của video 26.

CHẠY:  python tools/build_remotion_27.py            # → remotion-vox/projects/co-dai-27/project.json
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
STEM = "27_kankisen-abura-akujiru"
NAME = "co-dai-27"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#F2B84B"
TAG_BG = "#F5D58A"
PUNCH_COL = {INK: "#FFFFFF", RED: "#FF8A7A"}

# ── khuôn khung (giữ nguyên như video 25/26 — phương án C, không cast) ───────────
HERO_Y = 140
HERO_BOTTOM = 900
HW = round((HERO_BOTTOM - HERO_Y) * 1.49)
HX = (1920 - HW) // 2
OUT_W = 330
OUT_XY = ((1555, 110), (25, 185), (1555, 500), (25, 540))
OUT_ROT = (-6, 6, 5, -5)

EARTH, INDIGO, CREAM, CLAY, MOSS, MUSTARD = \
    "#B9765A", "#41536F", "#C8B88A", "#A65E3A", "#8A9A7B", "#C99A3E"
FLAME, SOOT = "#B0402A", "#33302C"

# ══════════════════════════════════════════════════════════════════════════════
# SCENES — L = chỉ số dòng timeline.json nơi scene BẮT ĐẦU (92 dòng, xem timeline.json).
# 70 scene / 1416s ≈ 20,2s/scene. 7 scene STAT/FORMULA (miễn sàn 9s — audience-45plus §2.0b).
# ══════════════════════════════════════════════════════════════════════════════
SCENES = [
    # ── 第1章 導入：二重の代償（コールドオープン） ─────────────────────────
    dict(L=0,  tag="踏み台が揺れる",   hero="card_fumidai_yure",     sup=["el_ashimoto_gura", "el_kanki_mado_yogore"],
         sp=[INDIGO, CREAM]),
    dict(L=2,  tag="二重の代償",       hero="card_hane_abura_hi",    sup=["el_honoo_kage", "el_kegura_tumu"],
         sp=[FLAME, SOOT]),
    dict(L=4,  tag="最後にとっておく", hero="card_fumidai_yakusoku", sup=["el_tokei_matsu", "el_yubikiri"],
         sp=[CREAM, INDIGO]),
    # ── 第2章 節子さんのラジオ（謎の提示） ──────────────────────────────────
    dict(L=5,  tag="古代の秘訣へ",     hero="card_intro_kanban",     sup=["el_kaki_pen", "el_hon_hirogaru"],
         sp=[CREAM, MOSS]),
    dict(L=6,  tag="ラジオが聞こえにくい", hero="card_setsuko_radio", sup=["el_radio_reizouko", "el_onryou_dial"],
         sp=[INDIGO, CREAM]),
    dict(L=7,  tag="耳ではなかった",   hero="card_setsuko_utagau",   sup=["el_hatena_mimi"],
         sp=[CREAM, INDIGO]),
    dict(L=8,  tag="ティッシュ1枚の診断", hero="card_tissue_shindan", sup=["el_tissue_hirahira", "el_suikomiguchi"],
         sp=[CREAM, CLAY]),
    dict(L=9,  tag="半年前から",       hero="card_tissue_hattari",   sup=["el_calendar_hantoshi"],
         sp=[INDIGO, CREAM]),
    # ── 第3章 重曹の敗北 ────────────────────────────────────────────────────
    dict(L=10, tag="重曹の午後",       hero="card_juusou_kosuru",    sup=["el_juusou_bin", "el_zoukin", "el_yukazuwari"],
         sp=[EARTH, CREAM]),
    dict(L=12, tag="いちばん弱い薬",   hero="card_yaku_hakari",      sup=["el_tenbin_yaku"],
         sp=[CREAM, EARTH]),
    dict(L=13, tag="pHのはしご",       hero=None, sup=[], sp=[INDIGO, CREAM], stat="ph_ladder"),
    # ── 第4章 正体の告発（油から樹脂へ） ────────────────────────────────────
    dict(L=16, tag="洗剤が効かない謎", hero="card_gimon_senzai",     sup=["el_senzai_yajirushi", "el_hatena_daikizu"],
         sp=[CREAM, INDIGO]),
    dict(L=17, tag="かたくて指がすべる", hero="card_yubisaki_kachikachi", sup=["el_yubisaki_up", "el_kagami_han"],
         sp=[INDIGO, CREAM]),
    dict(L=18, tag="酸化と重合",       hero="card_sanka_juugou",     sup=["el_bunshi_te", "el_kemuri_abura"],
         sp=[FLAME, INDIGO]),
    dict(L=19, tag="油は樹脂に",       hero="card_purasuchikku_hen", sup=["el_ita_hikari"],
         sp=[INDIGO, CREAM]),
    dict(L=20, tag="油のコンクリート", hero="card_abura_concrete",   sup=["el_hokori_maru", "el_sen_ori"],
         sp=[EARTH, CREAM]),
    dict(L=21, tag="戦う相手はプラスチック", hero="card_taiketsu_ita", sup=["el_ken_kakera", "el_te_kobushi"],
         sp=[INDIGO, FLAME]),
    dict(L=22, tag="中性洗剤に取っ手なし", hero="card_chuusei_senzai", sup=["el_te_tsurutsuru", "el_mizu_shizuku2"],
         sp=[CREAM, INDIGO]),
    # ── 第5章 隠れた義務（火災予防条例） ────────────────────────────────────
    dict(L=23, tag="燃える板、火災の危険", hero=None, sup=[], sp=[FLAME, SOOT], stat="fire_stat"),
    dict(L=24, tag="条例で定められた掃除", hero="card_jourei_kanban", sup=["el_hanko_shorui", "el_houki"],
         sp=[CREAM, EARTH]),
    dict(L=25, tag="好みの問題ではない", hero="card_setsuko_hansei", sup=["el_karendaa_batsu"],
         sp=[INDIGO, CREAM]),
    # ── 第6章 核心：鹸化とは何か ────────────────────────────────────────────
    dict(L=27, tag="今日の核心",       hero="card_kakushin_taitoru", sup=["el_hikari_hourensou", "el_flask_alkali"],
         sp=[INDIGO, CREAM]),
    dict(L=29, tag="鹸化、油を石けんに", hero="card_kenka_zu",       sup=["el_yajirushi_henka"],
         sp=[CREAM, INDIGO]),
    dict(L=30, tag="汚れが洗剤に変わる", hero="card_kagayaki_kenka", sup=["el_awa_sekken", "el_te_douguzu", "el_hikari_bakuhatsu"],
         sp=[MUSTARD, CREAM]),
    dict(L=32, tag="最強はかまどの底", hero="card_kamado_soko",      sup=["el_hi_kamado", "el_hai_yama"],
         sp=[EARTH, SOOT]),
    dict(L=34, tag="灰の中のアルカリ、14", hero=None, sup=[], sp=[FLAME, CREAM], stat="ph14"),
    dict(L=36, tag="灰汁はその上をいく", hero="card_akujiru_hikaku", sup=["el_hakari_dejitaru"],
         sp=[CREAM, EARTH]),
    # ── 第7章 灰汁の作り方 ──────────────────────────────────────────────────
    dict(L=37, tag="作り方、灰と湯",   hero="card_akujiru_tsukurikata", sup=["el_bowl_stainless", "el_oyu_yugeki"],
         sp=[EARTH, CREAM]),
    dict(L=38, tag="上澄みが洗剤",     hero="card_akujiru_sumi",     sup=["el_migakiko_soko", "el_koppu_sumu"],
         sp=[CREAM, EARTH]),
    dict(L=39, tag="つけ置きと拭き取り", hero="card_tsukeoki_fuku",  sup=["el_hane_oyu", "el_nuno_fuku", "el_tokei_15fun"],
         sp=[INDIGO, CREAM]),
    dict(L=40, tag="私の失敗談",       hero="card_shippai_atsui_hai", sup=["el_suji_nokoru", "el_hai_atsui"],
         sp=[EARTH, SOOT]),
    dict(L=41, tag="灰の匂いの記憶",   hero="card_hai_nioi_kioku",   sup=["el_yubisaki_hai", "el_kamado_asa"],
         sp=[EARTH, CREAM]),
    # ── 第8章 扱いの注意 ────────────────────────────────────────────────────
    dict(L=42, tag="ペーハー14は強い薬", hero="card_gomu_tebukuro",  sup=["el_gomu_tebukuro2", "el_kanki_mado2", "el_megusuri"],
         sp=[FLAME, CREAM]),
    dict(L=44, tag="アルミには使えない", hero="card_arumi_seiryuuban", sup=["el_arumi_hikari", "el_senzai_chuusei2"],
         sp=[INDIGO, CREAM]),
    dict(L=45, tag="モーターに液体禁止", hero="card_motor_keikoku",  sup=["el_batsu_maaku", "el_katakushi_nuno"],
         sp=[CREAM, CLAY]),
    dict(L=46, tag="手入れの間隔",      hero=None, sup=[], sp=[INDIGO, CREAM], stat="maintenance"),
    dict(L=47, tag="灰がなければセスキ", hero="card_seski_bin",      sup=["el_supuun_koya", "el_mizu500ml"],
         sp=[CREAM, MUSTARD]),
    dict(L=48, tag="セスキの使い方",   hero="card_seski_pakku",      sup=["el_kitchen_paper", "el_yubi_kanshoku"],
         sp=[CREAM, INDIGO]),
    dict(L=49, tag="なぜ灰は消えたのか", hero="card_nazo_hai_kieta", sup=["el_hatena_hai"],
         sp=[EARTH, CREAM]),
    # ── CTA ─────────────────────────────────────────────────────────────────
    dict(L=50, tag="お願い",           hero="card_share_onegai",     sup=["el_smartphone_share", "el_ohanashi_kotoba", "el_haato_iine"],
         sp=[CREAM, MOSS]),
    # ── 第9章 灰屋の江戸（歴史） ────────────────────────────────────────────
    dict(L=51, tag="ただの燃えかすでない", hero="card_haigai_shounin", sup=["el_hai_bako"],
         sp=[EARTH, CREAM]),
    dict(L=53, tag="灰買いの声",       hero="card_haikai_koe",       sup=["el_kaminuno_hai", "el_nagaya_michi"],
         sp=[CREAM, EARTH]),
    dict(L=54, tag="紺灰座、たった3軒", hero=None, sup=[], sp=[EARTH, CREAM], stat="hai_shops"),
    dict(L=55, tag="想像してみてください", hero="card_souzou_ita",   sup=["el_kane_de", "el_kokoro_tobu"],
         sp=[FLAME, CREAM]),
    dict(L=56, tag="灰汁桶、洗濯にも", hero="card_akujiruoke",       sup=["el_tarai_sentaku", "el_sen_kuchi"],
         sp=[INDIGO, CREAM]),
    # ── 第10章 石けんの経済史 ───────────────────────────────────────────────
    dict(L=58, tag="石けんの経済史",   hero=None, sup=[], sp=[CREAM, INDIGO], stat="soap_history"),
    dict(L=62, tag="お金の流れの話",   hero="card_okane_nagare",     sup=["el_okane_saifu", "el_gyousha_denwa"],
         sp=[MUSTARD, CREAM]),
    dict(L=64, tag="江戸の商人は買いに来た", hero="card_edo_shounin_kai", sup=["el_zeni_bukuro"],
         sp=[EARTH, CREAM]),
    dict(L=65, tag="手間からお金へ",   hero="card_mukisagyaku",      sup=["el_te_to_okane", "el_saifu_kawaru"],
         sp=[CREAM, INDIGO]),
    # ── 第11章 節子さんのラジオ、解決 ───────────────────────────────────────
    dict(L=66, tag="ラジオへ戻る",     hero="card_radio_modoru",     sup=["el_hane_maku", "el_kaze_hosoi"],
         sp=[INDIGO, CREAM]),
    dict(L=68, tag="翌朝まで残る匂い", hero="card_kabegami_kiba",    sup=["el_agemono_nioi", "el_kabegami_shimi"],
         sp=[EARTH, CREAM]),
    dict(L=69, tag="3年かけて進んだ",  hero="card_3nen_shinkou",     sup=["el_calendar_3nen"],
         sp=[INDIGO, CREAM]),
    dict(L=70, tag="同じ前提の上に",   hero="card_kizuki_setsuko",   sup=["el_hatena_shousetsu", "el_te_ita"],
         sp=[CREAM, INDIGO]),
    # ── 第12章 本当の答え：10秒の自由 ───────────────────────────────────────
    dict(L=73, tag="重合の逆手",       hero="card_juugou_gyakute",   sup=["el_kuuki_toki", "el_netsu_kioku"],
         sp=[FLAME, INDIGO]),
    dict(L=74, tag="料理を終えたばかり", hero="card_ryouri_sara_sara", sup=["el_abura_tsubu"],
         sp=[CREAM, MUSTARD]),
    dict(L=75, tag="10秒、0円",        hero="card_juubyou_nuno_nade", sup=["el_nuno_kawaita"],
         sp=[MUSTARD, CREAM]),
    dict(L=76, tag="全部この10秒の話", hero="card_zenbu_10byou",     sup=["el_akujiru_mini", "el_oyu_mini"],
         sp=[CREAM, EARTH]),
    dict(L=77, tag="お金のことではない", hero="card_okane_dewanai",  sup=["el_kokoro_te"],
         sp=[INDIGO, CREAM]),
    # ── 第13章 転落という代価 ───────────────────────────────────────────────
    dict(L=78, tag="転落20年458件",    hero=None, sup=[], sp=[FLAME, SOOT], stat="fall_stat"),
    dict(L=79, tag="板ができなければ", hero="card_ita_naikara",      sup=["el_fumidai_muyou", "el_kaidan_anzen"],
         sp=[INDIGO, CREAM]),
    dict(L=80, tag="乗る回数を守る",   hero="card_kaisuu_mamoru",    sup=["el_kazu_kaunto"],
         sp=[CREAM, INDIGO]),
    dict(L=81, tag="古いタオル1枚",    hero="card_taorukake_furui",  sup=["el_taoru_hankaketa", "el_te_todoku"],
         sp=[CREAM, MOSS]),
    # ── 第14章 節子さんの結末 ───────────────────────────────────────────────
    dict(L=82, tag="音が戻った",       hero="card_oto_modotta",      sup=["el_radio_onryou_futuu", "el_akujiru_nuno"],
         sp=[INDIGO, CREAM]),
    dict(L=83, tag="もう乗らないの",   hero="card_fumidai_monooki",  sup=["el_neko_kao_niru"],
         sp=[CREAM, MOSS]),
    # ── 第15章 結び：正直な限界 ─────────────────────────────────────────────
    dict(L=84, tag="正直に、灰汁は万能でない", hero="card_shoujiki_genkai", sup=["el_arumi_batsu", "el_hai_nashi_ie"],
         sp=[EARTH, CREAM]),
    dict(L=86, tag="10秒はこれから先に", hero="card_korekara_saki",  sup=["el_ita_sudeni"],
         sp=[INDIGO, CREAM]),
    dict(L=87, tag="待ってしまうこと", hero="card_matteshimau",      sup=["el_tokei_osoi", "el_kutsu_takai"],
         sp=[CREAM, EARTH]),
    dict(L=88, tag="教えてください",   hero="card_comment_onegai2",  sup=["el_comment_fukidashi2", "el_chiiki_hai"],
         sp=[CREAM, MOSS]),
    dict(L=89, tag="次の話へ",         hero="card_tsugi_no_hanashi", sup=["el_tobira_hikari"],
         sp=[INDIGO, CREAM]),
    dict(L=90, tag="また次の知恵で",   hero="card_shimei_tojiru2",   sup=["el_andon_akari2", "el_tsuki_shime2", "el_hai_saigo"],
         sp=[INDIGO, CREAM]),
]

# banner PUNCH — chữ đâm, neo theo chỉ số dòng (mọi câu phải CÓ trong lời của DÒNG đó)
PUNCH = [
    (2,  "住宅火災の原因の第1位です",   RED),
    (3,  "あれは、もう油ではありません", INK),
    (7,  "耳ではありませんでした",       RED),
    (12, "選んだ薬が、いちばん弱いものだった", INK),
    (15, "もっと強いものが、昔の台所にはありました", RED),
    (19, "油は、樹脂に変わります",       RED),
    (20, "衣類の繊維や家の中のホコリも舞っています", INK),
    (21, "薄いプラスチックの板なのです", RED),
    (23, "着火して火災になる危険があることを", INK),
    (24, "火災予防条例で定められています", RED),
    (28, "油を、石けんに変えてしまうのです", RED),
    (30, "汚れそのものが、洗剤に変わるのです", INK),
    (34, "数字は、14でした",             RED),
    (39, "削るのではなく、待つのが仕事です", INK),
    (40, "私は最初、これに失敗しました", INK),
    (43, "必ずゴム手袋をお使いください", RED),
    (54, "わずか3軒だけでした",          RED),
    (58, "主食の米よりもはるかに高い値で", INK),
    (75, "10秒です。0円です",            RED),
    (78, "20年間で458件",                RED),
    (81, "わざわざ台所へ行くことは、もうありません", INK),
    (83, "もう、あれには乗らないの",     RED),
    (87, "待ってしまうことのほうにありました", INK),
]

# bảng số liệu — key khớp `stat=` ở SCENES. `*` = dòng nhấn.
STAT = {
    "ph_ladder":    ("重曹|8.2" + NL + "セスキ炭酸ソーダ|9.8" + NL + "*炭酸ソーダ|11.2" + NL
                      + "目盛り1つ|＝10倍の強さ", 40),
    "fire_stat":    ("こんろ火災は|住宅火災の原因 第1位" + NL + "*放置・忘れる|原因の4割", 44),
    "ph14":         ("炭酸ソーダ|11.2" + NL + "*かまどの灰汁|ペーハー14" + NL + "差は|桁ちがい", 40),
    "maintenance":  ("フィルター|1か月に1回" + NL + "*ファン全体|3〜6か月に1回", 46),
    "hai_shops":    ("紺灰座の灰屋|わずか3軒" + NL + "*江戸の油汚れ|商人が買い取り", 44),
    "soap_history": ("1543年|石けん、日本へ" + NL + "1873年|国産石けん誕生" + NL
                      + "*価格|お米より高い" + NL + "1890年代|ブランド化・値下がり", 34),
    "fall_stat":    ("20年間|458件の転落" + NL + "60歳以上が|約3分の2" + NL + "*入院|206件", 40),
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


def stick(i, asset, f, dur, x, y, w, rot=0, ent="rise", amp=5, ph=0.0, sh="lg", exit_variant=None):
    return {"id": i, "kind": "sticker", "from": f, "durationInFrames": max(1, dur),
            "asset": f"assets/{asset}.png",
            "layout": {"x": x, "y": y, "w": w, "rotation": rot, "opacity": 1},
            "entrance": {"variant": ent, "delayFrames": 0, "params": {}},
            "exit": ({"variant": exit_variant, "delayFrames": 0, "params": {}}
                     if exit_variant else None),
            "idle": {"amp": amp, "phase": ph}, "shadow": sh}


def txt(i, content, f, dur, preset, color=INK, layout=None, size=None):
    return {"id": i, "kind": "text", "from": f, "durationInFrames": max(1, dur),
            "content": content, "preset": preset, "color": color,
            "animation": "pop", "animationParams": {"restDeg": -1.5},
            "layout": layout or {}, "fontSize": size}


# ⭐ SCHEDULER MỚI (thay khối "pulse" của video 26 — feedback_sticker_1_lan_vao_sau_hero_2s):
#   · mỗi sticker trong `sups` xuất hiện ĐÚNG 1 LẦN, không xoay vòng lặp file.
#   · sticker đầu vào ở f + ENTER_DELAY (~2s) sau hero.
#   · các sticker sau giãn đều trên phần CÒN LẠI của scene (không dồn cụm đầu scene) —
#     để đạt sàn 9s (`check_frame_pace.py`) xuyên suốt cả scene, không chỉ 20s đầu.
#   · mỗi sticker BẬT exit ("fade") — bản thân lúc rút đi cũng là 1 sự kiện (miễn phí).
ENTER_DELAY = 60           # 2s @30fps — sticker đầu vào sau hero
STK_LIFE_MIN, STK_LIFE_MAX = 150, 200   # 5–6.7s sống trước khi exit
TAIL_MARGIN = 30           # chừa 1s cuối scene trống (đỡ đụng ranh giới scene sau)


def schedule_stickers(sups, f, to, fitw, k):
    """Trả về list clip sticker cho 1 scene, mỗi phần tử `sups` xuất hiện đúng 1 lần,
    giãn đều trên [f+ENTER_DELAY, to-TAIL_MARGIN], có exit, gán theo 4 vị trí OUT_XY
    xoay vòng CHỖ ĐẶT (không xoay vòng FILE — mỗi vị trí có thể tái dùng, file thì không)."""
    n = len(sups)
    if n == 0:
        return []
    span = max(to - f - ENTER_DELAY - TAIL_MARGIN, STK_LIFE_MIN)
    out = []
    for i, el in enumerate(sups):
        enter = f + ENTER_DELAY + round(span * i / n)
        life = min(STK_LIFE_MAX, max(STK_LIFE_MIN, round(span / n) - 10))
        slot = i % len(OUT_XY)
        sx, sy = OUT_XY[slot]
        sw = fitw(el, OUT_W)
        sx += (OUT_W - sw) // 2
        rot = OUT_ROT[slot]
        ent = ["grow", "rise", "flip", "zoom-through"][i % 4]
        out.append(stick(f"s{i}-{k}", el, enter, life, sx, sy, sw,
                         rot=rot, ent=ent, amp=5, ph=1.2 + i * 0.7, sh="sm",
                         exit_variant="fade"))
    return out


def main():
    vd = PROJ / "06_VIDEO" / STEM
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines = tl["lines"]
    F = lambda idx: round(lines[idx]["start"] * FPS)          # noqa: E731
    DUR = round(tl["total"] * FPS)

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
        sup_clips = schedule_stickers(s.get("sup") or [], f, to, fitw, k)
        for i, c in enumerate(sup_clips):
            (sup1, sup2, sup3, sup4)[i % 4].append(c)
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
                               layout={"x": 960 - 405, "y": 430 + off, "w": 830},
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
                 "createdAt": "2026-09-01T00:00:00.000Z",
                 "modifiedAt": "2026-09-01T00:00:00.000Z"},
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
