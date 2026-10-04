# -*- coding: utf-8 -*-
"""Sinh 19_haisuiko-naze-tsumaru_SLIDES.json + bo prompt anh (FLOW/NAMES).

Dung script vi 2 ly do:
  1) moi `match` PHAI la substring that cua mot dong _TTS.md — sai la render gay giua duong
  2) cue chon bang luat >=55 ky/slide => <=6 doi hinh/phut (audience-45plus.md §2)
"""
import re, json, sys
from pathlib import Path

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
SLUG = "19_haisuiko-naze-tsumaru"
VD = f"E:/Claude/Projects/youtube-jp-co-dai/06_VIDEO/{SLUG}"

L = [re.sub(r"\[[^\]]*\]", "", l).strip()
     for l in (PROJ / "03_SCRIPTS" / f"{SLUG}_TTS.md").read_text(encoding="utf-8").split("\n")]
L = [l for l in L if l and not l.startswith(("#", "TARGET_QUERY", "INTENT"))]


def P(n):
    return f"{VD}/ai_clean/{n}.jpeg"


VOX = {
 5: ("stat", {"kicker": "台所の勝ち目", "big": "20", "unit": "度",
              "sub": "40度から60度のあいだ", "note": "ここを外すと、何をしても届きません"},
     "thermometer_40_to_60"),
 15: ("compare", {"kicker": "同じ水の、二つの温度", "title": "出ていく時と、届く時",
                  "left": {"label": "流しから出る水", "mark": "o", "verdict": "40度前後"},
                  "right": {"label": "床下の管の中", "mark": "x", "verdict": "20度を下回る"}}, "warm_dishwater_surface"),
 18: ("source", {"kicker": "出典", "org": "東京都下水道局", "asof": "油・断・快適！下水道",
                 "number": "冷えて固まる",
                 "quote": "台所から流れた油は下水道管内で冷えて固まり、つまりや悪臭の原因になります",
                 "note": "大雨で剥がれた塊は、オイルボールと呼ばれます"}, "oil_congealed_in_pipe"),
 19: ("flow", {"kicker": "一日ずつ、一枚ずつ", "head": "膜の上に、次の膜が重なる",
               "pins": [[1300, 235, "きのうの膜"], [1300, 350, "きょうの膜"],
                        [1300, 465, "内径が細る"]],
               "arrows": [[1260, 300, 980, 390, 0.18]]}, "pipe_inner_wax_layers"),
 22: ("bar", {"kicker": "温度（度）", "title": "隙間は、たしかにある",
              "bars": [["脂が溶ける", 50], ["配管の限界", 60]], "hot": 0,
              "note": "この20度のあいだだけ、手が届きます"}, "tallow_starting_to_melt"),
 23: ("process", {"kicker": "今夜の一手", "title": "洗い物の、すぐあとに",
                  "steps": [{"label": "50度のお湯", "sub": "熱湯にしない"},
                            {"label": "30秒だけ流す", "sub": "管が温まっているうちに"},
                            {"label": "それで終わり", "sub": "道具は要りません", "hot": True}]},
      "warm_water_running_into_drain"),
 25: ("line", {"kicker": "取り戻せる分", "title": "一晩ごとに、一枚ずつ硬くなる",
               "points": [["今夜", 90], ["三日", 70], ["一月", 40], ["半年", 15], ["三年", 5]],
               "last_label": "芯", "note": "遅れるほど、戻せる分が減っていきます"}, "waxy_flakes_stacked"),
 27: ("flow", {"kicker": "呼びかけは三つだけ", "head": "ふき取る・吸い取る・使い切る",
               "pins": [[1300, 235, "紙でふき取る"], [1300, 350, "新聞紙に吸わせる"],
                        [1300, 465, "漉して使う"]]}, "newspaper_wiping_frying_pan"),
 31: ("timeline", {"kicker": "油こし器のあった台所", "title": "油は、捨てるものではなかった",
                   "marks": [["昔", "こし器で漉して缶へ"], ["次の日", "もう一度、揚げ物に"],
                             ["最後", "炒め物に回す"]],
                   "note": "コンロの右奥、いつも同じ場所に"}, "old_oil_strainer_can_on_stove"),
 36: ("title", {"kicker": "隙間が通用しない相手", "title": "小麦粉",
                "note": "薄まるのではなく、濃くなります"}, "flour_dusted_bowl_rim"),
 40: ("flow", {"kicker": "糊化", "head": "60度を超えると、糊になる",
               "pins": [[1300, 235, "粒がふくらむ"], [1300, 350, "分子が出る"],
                        [1300, 465, "網目になる"]],
               "arrows": [[1260, 300, 960, 390, 0.18]]}, "flour_and_water_paste"),
 43: ("line", {"kicker": "老化の進みやすさ", "title": "冷えるほど、速く硬くなる",
               "points": [["60度", 5], ["40度", 25], ["20度", 60], ["10度", 85], ["2〜4度", 100]],
               "last_label": "最速", "note": "ちょうど、冷蔵庫の中の温度です"}, "cold_hardened_rice"),
 44: ("source", {"kicker": "出典", "org": "澱粉科学", "asof": "第19巻第2号・1972年",
                 "number": "60度以上",
                 "quote": "でんぷん糊の老化は60度以上ではほとんど起こらず、温度の低下とともに速く進む",
                 "note": "つまり、固めないためには60度より上が要ります"}, "old_journal_page_on_desk"),
 47: ("compare", {"kicker": "二つの60度", "title": "隙間は、閉じています",
                  "left": {"label": "でんぷんに必要", "mark": "o", "verdict": "60度より上"},
                  "right": {"label": "配管の限界", "mark": "x", "verdict": "60度まで"}}, "thermometer_at_60"),
 55: ("stat", {"kicker": "入り口で止める道具", "big": "100", "unit": "円",
               "sub": "流しのゴミ受け",
               "note": "置くだけでは働きません。その日のうちに捨てる"}, "mesh_sink_strainer_basket"),
 60: ("title", {"kicker": "いちばんやってはいけない", "title": "熱湯",
                "note": "詰まりを、手の届かない奥へ運びます"}, "steaming_kettle_over_sink"),
 64: ("stat", {"kicker": "熱が届く範囲", "big": "2", "unit": "メートル",
              "sub": "そこから先は、ただの水",
              "note": "奥に運ばれた油は、届かない場所で固まります"}, "pipe_running_into_dark"),
 70: ("source", {"kicker": "出典", "org": "配管メーカー資料",
                 "asof": "硬質ポリ塩化ビニル管・排水用", "number": "60度以下",
                 "quote": "排水用の硬質塩化ビニル管の使用温度は60度以下",
                 "note": "超え続けると、継ぎ目の力が落ちます"}, "grey_pvc_pipe_under_sink"),
 72: ("bar", {"kicker": "温度（度）", "title": "70度には、別の管が要る",
              "bars": [["普通の管", 60], ["食洗機の排水", 70], ["耐熱用の管", 90]], "hot": 1,
              "note": "設計上、わざわざ管を替えています"}, "dishwasher_drain_hose"),
 74: ("process", {"kicker": "10秒の自己診断", "title": "熱は、届いていない",
                  "steps": [{"label": "お湯を流す", "sub": "いつもどおりに"},
                            {"label": "扉を開けて管に触る", "sub": "流しの下"},
                            {"label": "冷たければ届いていない", "sub": "熱は途中で消えます",
                             "hot": True}]}, "hand_touching_pipe_under_sink"),
 85: ("compare", {"kicker": "温度が効かない相手", "title": "50度でも、90度でも",
                  "left": {"label": "冷やす", "mark": "x", "verdict": "固まらない"},
                  "right": {"label": "温める", "mark": "x", "verdict": "ゆるまない"}},
      "wet_coffee_grounds_closeup"),
 92: ("flow", {"kicker": "一つの塊、三つの材料",
               "head": "油が接着面、でんぷんが糊、かすが中身",
               "pins": [[1300, 235, "油の膜"], [1300, 350, "でんぷんの糊"],
                        [1300, 465, "かすが中身"]]}, "three_layer_sludge_in_pipe"),
 100: ("timeline", {"kicker": "三つの性質", "title": "性質は違うのに、答えは一つ",
                    "marks": [["油", "温度で戻せる"], ["でんぷん", "戻せない"],
                              ["かす", "温度が関係ない"]],
                    "note": "三つとも、入り口を指しています"}, "kitchen_sink_drain_opening"),
 111: ("timeline", {"kicker": "昔の行き先", "title": "どれも、管の外へ",
                    "marks": [["油", "漉して缶へ"], ["研ぎ汁", "庭の木の根元へ"],
                              ["茶がら", "たたきに撒いて土へ"]],
                    "note": "流しは、捨てる場所ではありませんでした"}, "tea_leaves_dried_on_paper"),
 124: ("compare", {"kicker": "なぜ広まらないのか", "title": "売るものが、無い",
                   "left": {"label": "月に一度使うもの", "mark": "x",
                            "verdict": "毎月の収入になる"},
                   "right": {"label": "入れない", "mark": "o",
                             "verdict": "一度覚えたら終わり"}}, "coin_and_newspaper"),
 132: ("process", {"kicker": "今夜からの順番", "title": "三つだけ",
                   "steps": [{"label": "油を紙で拭く", "sub": "洗い物の前に"},
                             {"label": "粉・麺・ご飯・かす", "sub": "ゴミ受けへ"},
                             {"label": "50度を30秒", "sub": "洗い物のすぐあと。熱湯は使わない",
                              "hot": True}]}, "newspaper_and_strainer_on_counter"),
}

SUBJ = {
 0: "kitchen sink drain opening, extreme close up", 1: "water pooling slowly in a stainless sink",
 2: "a hand reaching for a kettle in an evening kitchen", 3: "warm water stream falling into a drain",
 4: "steam rising from a kettle spout, warning feel", 6: "a coffee filter being lifted from a dripper",
 7: "a covered pot lid held closed, something kept for later",
 8: "wide view of an old Japanese kitchen at dusk",
 9: "an old notebook and pencil on a kitchen table", 10: "kitchen sink beside a window, morning light",
 11: "a bottle of cooking oil on a counter", 13: "a stack of greasy frying pans",
 15: "warm dishwater in a basin, faint steam", 17: "an oil sheen spreading on water surface",
 20: "a cut drain pipe showing a waxy ring inside", 21: "a fingertip touching the inner pipe wall",
 24: "hardened grease core deep inside a pipe", 26: "folded newspaper lying beside a frying pan",
 28: "crumpled oily newspaper in a bin", 29: "a week of folded newspapers stacked",
 30: "a worn kitchen sponge on a sink edge", 32: "elderly hands straining hot oil through a mesh",
 33: "close up of an old oil can lid", 34: "a thermometer standing in warm water",
 35: "a paper sack of flour on a shelf", 37: "a bowl with tempura batter residue",
 38: "a finger streak drawn through wet flour", 39: "flour thickening in water, swirling",
 41: "cooling starch paste with a dull surface", 42: "a dry cracked lump of starch",
 45: "two thermometers standing side by side", 46: "steam over water at sixty degrees",
 48: "a closed gap between two pipe ends", 49: "oil on one side, flour on the other",
 50: "a sink strainer catching white flour", 51: "glue like paste smeared on metal",
 52: "small food bits stuck in paste", 53: "leftover noodles lying in a sink",
 54: "scraping a plate into a small bin", 56: "a strainer basket being emptied",
 57: "a person standing still at a kitchen sink", 58: "a boiling kettle, close up",
 59: "hot water poured straight into a drain", 61: "a hand drawn pipe diagram on paper",
 63: "grease melting on the inside of a pipe", 65: "grease pushed deep along a pipe",
 66: "water draining freely for a brief moment", 67: "an under sink cabinet standing open",
 68: "a grey plastic drain pipe under a sink", 69: "a hand opening a cabinet door",
 71: "a built in dishwasher control panel", 73: "two pipes of different type compared",
 75: "cooking oil and flour placed side by side", 76: "ice and steam in one frame, contrast",
 77: "used coffee grounds on a spoon", 79: "a kitchen in early morning light",
 80: "a mound of used coffee grounds", 81: "a pour over dripper with a wet filter",
 82: "coffee grounds swirling in water", 83: "coffee grounds settled at a container bottom",
 84: "magnified coffee particles, gritty texture", 86: "coffee grounds unchanged in hot water",
 87: "a pipe bend and joint, simple diagram feel", 88: "coffee grounds accumulating day by day",
 89: "wet sand squeezed in a hand, holding shape", 90: "a compacted layer of sediment",
 91: "three small materials arranged in a row", 93: "a sludge sample on a tray",
 94: "coffee grounds tipped into a bin", 95: "a filter lifted and drained of water",
 96: "garden soil mixed with coffee grounds", 97: "planter soil being turned over",
 98: "coffee grounds drying on spread newspaper", 99: "rich dark garden soil, close up",
 101: "three labelled glass jars in a row", 102: "a sink drain entrance in sharp focus",
 103: "an old farmhouse kitchen interior", 104: "a traditional Japanese stone kitchen sink",
 105: "simple old kitchen tools hanging", 106: "an empty wooden draining board",
 107: "an oil strainer and a metal can", 108: "a bucket of cloudy rice washing water",
 109: "cloudy rice water, close up", 110: "pouring rice water at a tree root",
 112: "dried tea leaves beside an oil can", 113: "an old dry stone sink",
 114: "a quiet kitchen in the evening", 115: "a modern faucet running water",
 116: "water disappearing down a drain", 117: "a pipe hidden behind an opened wall",
 118: "a shop shelf lined with cleaning bottles", 119: "a row of cleaning bottles, no labels",
 120: "a product label reading once a month, blank text", 121: "baking soda and a vinegar bottle",
 122: "a wide shop shelf of household goods", 123: "stacked boxes of repeat purchase goods",
 125: "a single inexpensive sink strainer", 126: "a plain shelf with unbranded containers",
 127: "a person choosing in front of a shelf", 128: "used coffee grounds, final still",
 129: "three household items lined up", 130: "newspaper wiping a frying pan again",
 131: "a strainer holding food scraps", 133: "only a strainer and folded newspaper",
 134: "an honest plain kitchen, wide", 135: "old hardened pipe interior",
 136: "a pipe with an age worn label", 137: "a calm kitchen in the evening",
 138: "a thermometer on a windowsill", 139: "three states as a still life",
 140: "old hands working in a kitchen", 141: "an empty shelf where a can once stood",
 142: "a soft focus memory of an oil can", 143: "a sink at night, quiet",
 144: "a house exterior at dusk", 145: "a lantern beside an old book",
}
# 🔴 Prompt cho ANH CUA THE VOX — phai lay tu day, KHONG duoc roi vao dflt():
#    bug 2026-08-12: 18/18 anh vox nhan prompt mac dinh cua khuc (the 原典 東京都下水道局
#    nhan prompt "chao dau") vi SUBJ chi co key cho dong anh thuong.
VOXSUBJ = {
 "thermometer_40_to_60": "an analog kitchen thermometer lying on a counter, needle resting midway",
 "oil_congealed_in_pipe": "pale congealed cooking oil coating the inside of a cut drain pipe",
 "pipe_inner_wax_layers": "a cut drain pipe showing several pale waxy layers built up inside",
 "warm_water_running_into_drain": "warm water running steadily into a stainless sink drain, faint steam",
 "newspaper_wiping_frying_pan": "a folded sheet of newspaper wiping the inside of a frying pan",
 "old_oil_strainer_can_on_stove": "an old metal oil strainer can standing at the back right of a gas stove",
 "flour_dusted_bowl_rim": "a mixing bowl rim dusted with fine white flour",
 "flour_and_water_paste": "thick white flour paste clinging to a metal whisk",
 "old_journal_page_on_desk": "an old hardbound scientific journal closed on a wooden desk, reading lamp",
 "mesh_sink_strainer_basket": "a simple wire mesh sink strainer basket, empty and clean",
 "steaming_kettle_over_sink": "a kettle held above a sink with steam rising from the spout",
 "grey_pvc_pipe_under_sink": "a grey plastic drain pipe under a kitchen sink, cabinet door open",
 "hand_touching_pipe_under_sink": "a hand resting flat against a drain pipe under a sink",
 "wet_coffee_grounds_closeup": "wet used coffee grounds, extreme close up, gritty texture",
 "three_layer_sludge_in_pipe": "a cut pipe showing three distinct sludge layers inside",
 "kitchen_sink_drain_opening": "a kitchen sink drain opening seen straight down from above",
 "tea_leaves_dried_on_paper": "used tea leaves spread out and drying on paper",
 # ── 8 ảnh THÊM 2026-08-12 (user: "3 thẻ nền phẳng lệch so với các frame khác").
 #    Trước đó bar/line/compare/stat để sub=None nên không có ảnh → nền kem phẳng, lệch
 #    hẳn với 81 frame ảnh. Chủ thể chọn KHÔNG trùng 81 cái đã có.
 "warm_dishwater_surface": "the surface of warm dishwater in a stainless sink, faint steam, macro",
 "tallow_starting_to_melt": "a block of solid white beef tallow softening and going glossy at the edges",
 "waxy_flakes_stacked": "thin pale waxy flakes stacked in layers, side lit",
 "cold_hardened_rice": "cold cooked rice with a dry hardened surface, macro",
 "thermometer_at_60": "an analog dial thermometer with the red needle pointing exactly at 60",
 "pipe_running_into_dark": "a long grey drain pipe receding into darkness",
 "dishwasher_drain_hose": "a corrugated plastic drain hose behind an appliance",
 "coin_and_newspaper": "a single coin lying beside a folded sheet of newspaper on a bare counter",
 "newspaper_and_strainer_on_counter": "folded newspaper and a wire mesh strainer side by side on a counter",
}

DEF = [(10, "an evening kitchen sink"), (34, "cooking oil and a frying pan"),
       (57, "flour and a mixing bowl"), (78, "a kettle and a drain pipe"),
       (100, "coffee grounds and garden soil"), (118, "an old Japanese kitchen"),
       (999, "a quiet kitchen still life")]


def dflt(i):
    for lim, s in DEF:
        if i < lim:
            return s
    return DEF[-1][1]


STYLE = ("Photorealistic cinematic documentary still, Japanese home interior, soft natural "
         "daylight from a side window, warm neutral palette, muted colors, shallow depth of "
         "field, fine detail, calm quiet mood, 16:9 horizontal, no text, no letters, no logos, "
         "no brand labels, no human faces, no watermark")

# 🔴 STYLE_MACRO — vá 2026-08-12 sau khi duyệt lô ảnh đầu.
#    Lô 1 ra 82 ảnh TÔNG RẤT ĐỒNG NHẤT nhưng KHÔNG CÓ ẢNH NÀO LÀ MACRO THẬT: mọi ảnh thành
#    "phòng washitsu đẹp + vật nhỏ ở đâu đó" (ống gốm thay ống thoát nước, bã cà phê rắc trên
#    mép bàn thay hạt phóng đại). Nguyên nhân là chính STYLE ở trên: cụm
#    "Japanese home interior ... side window" ép framing phòng vào MỌI ảnh.
#    Với thẻ vox thì đó là lỗi chí tử — vox annotate ĐÈ LÊN ảnh, chủ thể không rõ thì pin/mũi
#    tên trỏ vào không khí.
STYLE_MACRO = ("Photorealistic extreme close-up macro photograph, the subject FILLS THE FRAME "
               "and is the only thing visible, tight crop, plain dark out-of-focus background, "
               "NO room, NO window, NO furniture, NO tableware in view. Hard directional light, "
               "high micro-detail, muted warm palette, calm documentary mood, 16:9 horizontal, "
               "no text, no letters, no logos, no brand labels, no human faces, no watermark")

# Slot BUỘC macro: mọi ảnh thẻ vox (bị annotate đè) + các beat mà chủ thể LÀ cơ chế.
MACRO_LINES = {12, 17, 20, 21, 23, 25, 26, 31, 32, 33, 39, 41, 50, 52, 53, 55, 57, 59, 63, 68, 83}
MACRO_VOX = set(VOXSUBJ)   # 18/18 ảnh vox đều macro

# 🔴 duotone:ink cho the process/compare/stat CO ANH — vá 2026-08-12 sau khi duyet sheet:
#    photo_style 'darken' chi toi hoa vung DAY (vgrad tu H*0.30) + dai nhe vung kicker,
#    con TIEU DE cua process/compare/stat nam giua-tren nen bi anh toi NUOT (4 the doc
#    khong ra: 洗い物の・すぐあとに / 熱は、届いていない / 50度でも、90度でも / 三つだけ).
#    flow/timeline khong bi vi chung tu ve dai vang sau tieu de.
NO_PHOTO = {"warm_water_running_into_drain","hand_touching_pipe_under_sink",
            "newspaper_and_strainer_on_counter","wet_coffee_grounds_closeup"}
# ⇒ 3 process + 1 compare: tieu de ve bang MUC DAM (thiet ke cho nen phang) nen anh toi
#   nao cung giet no. duotone lam TE HON (thu 2026-08-12). Bo anh la dung: X2 con 14/26=54%.
CHART_PH = {"tallow_starting_to_melt","waxy_flakes_stacked",
            "cold_hardened_rice","dishwasher_drain_hose"}
# ⇒ 4 thẻ bar/line: sau khi vá make_vox (_onph, 2026-08-12) nhãn trục/nhãn cột có
#   stroke nên đọc được trên ảnh → bật lại bg:photo, dùng darken như mọi thẻ khác.
DUO_INK = {'thermometer_40_to_60', 'wet_coffee_grounds_closeup', 'hand_touching_pipe_under_sink', 'warm_water_running_into_drain', 'mesh_sink_strainer_basket', 'newspaper_and_strainer_on_counter'}

# ── chon cue: don >=55 ky/slide, ep cue tai moi dong vox
CUE, acc = [], 0
for i, l in enumerate(L):
    if i == 0 or i in VOX or acc >= 55:
        CUE.append(i)
        acc = 0
    acc += len(l)

out, flow, names = [], [], []
bad = []
for i in CUE:
    m = L[i][:16]
    if sum(1 for x in L if m in x) != 1:
        bad.append((i, m, sum(1 for x in L if m in x)))
    if i in VOX:
        kind, spec, sub = VOX[i]
        v = {"kind": kind}
        v.update(spec)
        if sub:
            v["bg"] = "photo"
            v["photo"] = P(sub)
            v["photo_style"] = "darken"
            flow.append(f"{STYLE_MACRO}. {VOXSUBJ[sub]}")
            names.append(f"ai_clean/{sub}.jpeg")
        out.append({"match": m, "photo": False, "video": True, "vox": v})
    else:
        idx = len(out)
        flow.append(f"{STYLE_MACRO if i in MACRO_LINES else STYLE}. {SUBJ.get(i) or dflt(i)}")
        names.append(f"slides_img/slide_{idx:02d}.jpg")
        out.append({"match": m, "photo": True})

S = PROJ / "03_SCRIPTS"
(S / f"{SLUG}_SLIDES.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
(S / f"{SLUG}_IMG_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
(S / f"{SLUG}_IMG_NAMES.txt").write_text(
    "\n".join(f"{n+1:3d}  {p}" for n, p in enumerate(names)) + "\n", encoding="utf-8")

nv = [x["vox"]["kind"] for x in out if isinstance(x.get("vox"), dict)]
npho = sum(1 for x in out if x.get("photo") is True)
nvp = sum(1 for x in out if isinstance(x.get("vox"), dict) and x["vox"].get("photo"))
print(f"entry {len(out)} | anh thuong {npho} | vox {len(nv)} (co anh {nvp} = {nvp*100//len(nv)}%)")
print(f"doi hinh/phut {len(out)/(1154/60):.1f}  (tran 6)")
print(f"prompt {len(flow)} dong | match TRUNG/THIEU: {bad if bad else '0 — tat ca duy nhat'}")
print("kinds:", ", ".join(nv))
