# -*- coding: utf-8 -*-
"""SCENES / STAT / PUNCH cho video 19 — import bởi build_remotion_19.py.
Tách file để builder giữ nguyên phần cơ khí; sửa nội dung chỉ đụng file này."""

SCENES = [
    # ── COLD OPEN v4 (0–74s) — ĐÂM あなた + SỐ NGAY, kể chuyện SAU ─────────
    # 🔴 Viết lại 2026-09-01 (user: "30s đầu phải đánh vào nỗi sợ"). Bản v3 dựng
    #    bối cảnh 3 dòng rồi mới ra số ⇒ 168万 tới giây 32, あなた tới giây 36.
    #    Cold open còn 11 dòng (v3: 13) ⇒ mọi L= của scene sau DỊCH −2.
    dict(L=0,  tag="働き続けるあなた", heroes=["card_19_hataraku", "card_19_hataraku_b"], sup=["el_two_men_desk"],
         l="sensei_serious", r="kikite_surprised", sp=["#C87A72", "#8A93A8"]),
    dict(L=2,  tag="もらわないまま",  heroes=["card_19_kyuryo_meisai", "card_19_kyuryo_meisai_b"], sup=["el_calendar"],
         l="sensei_caution", r="kikite_worried",   sp=["#8A93A8", "#C87A72"]),
    # bảng THAY ảnh ở đây: số là thứ đắt nhất của đoạn này, và nhờ vậy bộ
    # card_19_futari ×4 dồn hết cho callback ở ~453s ⇒ hết trùng ảnh trong video
    dict(L=4,  tag="二万八千円と、一円", hero=None, stat="hikaku", sup=["el_coin_stack", "el_zero_stamp"],
         l="sensei_point",   r="kikite_surprised", sp=["#C87A72", "#8A93A8"]),
    dict(L=6,  tag="対象は",       heroes=["card_19_hataraku_c", "card_19_hatena"], sup=["el_signpost", "el_hand_stop"],
         l="sensei_present", r="kikite_listen",    sp=["#9FB6C8", "#C8B88A"]),
    dict(L=7,  tag="三つの問い",    heroes=["card_19_hatena_b", "card_19_hatena_c"], sup=["el_magnifying_glass"],
         l="sensei_caution", r="kikite_think",     sp=["#8A93A8", "#C87A72"]),
    dict(L=9,  tag="年金も止まる",  heroes=["card_19_kenkyu"],  sup=["el_nenkin_techo"],
         l="sensei_serious", r="kikite_worried",   sp=["#C87A72", "#9FB6C8"]),
    dict(L=11, tag="研究室",       heroes=["card_19_kenkyu_b"], sup=["el_newspaper"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    # ── 第1章 制度の中身 ──────────────────────────────────────────────────
    dict(L=12, tag="下がった分を補う", heroes=["card_19_koyou_hoken", "card_19_koyou_hoken_b"], sup=["el_nenkin_techo", "el_coin_stack"],
         l="sensei_present", r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    dict(L=14, tag="条件は三つ",    hero=None, stat="jouken",  sup=["el_hand_stop", "el_percent_badge"],
         l="sensei_point",   r="kikite_listen",    sp=["#9FB6C8", "#8A93A8"]),
    dict(L=18, tag="七十五パーセント未満", heroes=["card_19_75percent", "card_19_75percent_b"], sup=["el_percent_badge"],
         l="sensei_caution", r="kikite_surprised", sp=["#C87A72", "#C8B88A"]),
    dict(L=19, tag="原典・ハローワーク", heroes=["card_genten19_01", "card_genten19_01_b", "card_genten19_01_c"], sup=["el_magnifying_glass", "el_newspaper"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#8FA9C0"]),
    # ── 第2章 松本さんの明細 (179–287s) ────────────────────────────────────
    dict(L=21, tag="松本さん",     heroes=["card_19_matsumoto", "card_19_matsumoto_b", "card_19_matsumoto_c"],   sup=["el_nenkin_techo"],
         l="sensei_present", r="kikite_listen",    sp=["#C8B88A", "#9FB6C8"]),
    dict(L=24, tag="五十五万から二十八万", hero=None, stat="matsumoto", sup=["el_kyuryo_meisai", "el_chart_down"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=26, tag="落とし穴",     heroes=["card_19_jougen", "card_19_jougen_b", "card_19_jougen_c", "card_19_jougen_d"],      sup=["el_hand_stop", "el_signpost"],
         l="sensei_caution", r="kikite_worried",   sp=["#C87A72", "#8A93A8"]),
    dict(L=30, tag="割ってみます",  hero=None, formula="warizan", sup=["el_percent_badge"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=33, tag="二万八千円",    heroes=["card_19_28000", "card_19_28000_b", "card_19_28000_c"],       sup=["el_coin_stack", "el_calendar"],
         l="sensei_present", r="kikite_relieved",     sp=["#C8B88A", "#9FB6C8"]),
    # ── 第3章 率が変わった (287–398s) — HERO 84万 ──────────────────────────
    dict(L=36, tag="ここからが本題", heroes=["card_19_hondai", "card_19_hondai_b"],     sup=["el_speaker_robot"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#C87A72"]),
    dict(L=38, tag="原典・厚労省",  heroes=["card_genten19_02", "card_genten19_02_b"],    sup=["el_newspaper", "el_magnifying_glass"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#8A93A8"]),
    dict(L=40, tag="四万二千円と二万八千円", hero=None, stat="rate", sup=["el_chart_down", "el_coin_stack"],
         l="sensei_present", r="kikite_surprised", sp=["#C87A72", "#C8B88A"]),
    dict(L=42, tag="八十四万円",    heroes=["card_19_84man", "card_19_84man_b"],       sup=[], peak=42,
         l="sensei_caution", r="kikite_surprised", sp=["#B44A4A", "#8A93A8"]),
    dict(L=44, tag="分かれ目は誕生日", heroes=["card_19_tanjoubi", "card_19_tanjoubi_b", "card_19_tanjoubi_c", "card_19_tanjoubi_d"],  sup=["el_calendar", "el_hand_stop"],
         l="sensei_serious", r="kikite_worried",   sp=["#C87A72", "#9FB6C8"]),
    dict(L=48, tag="六十一から六十四へ", hero=None, stat="hasetsu", sup=["el_percent_badge", "el_chart_up"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    # ── 第4章 同僚のゼロ (398–541s) — CALLBACK ────────────────────────────
    dict(L=52, tag="割合が厳しい",  heroes=["card_19_wariai"],      sup=["el_hand_stop"],
         l="sensei_caution", r="kikite_listen",    sp=["#8A93A8", "#C87A72"]),
    dict(L=53, tag="同僚のかた",    heroes=["card_19_douryou", "card_19_douryou_b", "card_19_douryou_c"],     sup=["el_kyuryo_meisai", "el_two_men_desk"],
         l="sensei_present", r="kikite_think",     sp=["#C8B88A", "#9FB6C8"]),
    dict(L=56, tag="七十六・六パーセント", hero=None, formula="douryou", sup=["el_percent_badge"],
         l="sensei_point",   r="kikite_surprised", sp=["#8FA9C0", "#8A93A8"]),
    dict(L=58, tag="一円も、出ません", heroes=["card_19_zero", "card_19_zero_b"],      sup=["el_zero_stamp"],
         l="sensei_serious", r="kikite_worried",   sp=["#C87A72", "#8A93A8"]),
    dict(L=60, tag="冒頭のふたり",  heroes=["card_19_futari", "card_19_futari_b", "card_19_futari_c", "card_19_futari_d"],      sup=[], peak=60,
         l="sensei_caution", r="kikite_surprised", sp=["#B44A4A", "#C8B88A"]),
    dict(L=63, tag="三十九万七千三百六十九円", hero=None, stat="jougengaku", sup=["el_signpost", "el_hand_stop"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#8A93A8"]),
    dict(L=66, tag="境目に近づくほど", hero=None, stat="hayami", sup=["el_chart_down", "el_percent_badge"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    # ── CTA (541–569s) ─────────────────────────────────────────────────────
    dict(L=70, tag="お願いです",    heroes=["card_19_cta", "card_19_cta_b", "card_19_cta_c", "card_19_cta_d"],         sup=["el_smartphone", "el_teacup"],
         l="sensei_reassure",   r="kikite_relieved",     sp=["#C8B88A", "#9FB6C8"]),
    # ── 第5章 もうひとつの窓口 (569–722s) ──────────────────────────────────
    dict(L=71, tag="二つ目の窓口",  heroes=["card_19_madoguchi2", "card_19_madoguchi2_b"],  sup=["el_signpost"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#8FA9C0"]),
    dict(L=74, tag="原典・年金機構", heroes=["card_genten19_03", "card_genten19_03_b", "card_genten19_03_c"],   sup=["el_magnifying_glass", "el_newspaper"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#8A93A8"]),
    dict(L=76, tag="一万一千二百円", hero=None, stat="teishi",   sup=["el_coin_stack", "el_chart_down"],
         l="sensei_present", r="kikite_surprised", sp=["#C87A72", "#C8B88A"]),
    dict(L=78, tag="ここは正確に",  heroes=["card_19_tadashi", "card_19_tadashi_b", "card_19_tadashi_c"],     sup=["el_hand_stop"],
         l="sensei_caution", r="kikite_think",     sp=["#9FB6C8", "#8A93A8"]),
    dict(L=81, tag="繰上げ受給",    heroes=["card_19_kuriage", "card_19_kuriage_b", "card_19_kuriage_c"],     sup=["el_nenkin_techo", "el_calendar"],
         l="sensei_serious", r="kikite_worried",   sp=["#C87A72", "#9FB6C8"]),
    dict(L=85, tag="二重に、削られます", heroes=["card_19_nijuu", "card_19_nijuu_b", "card_19_nijuu_c"],   sup=["el_chart_down"],
         l="sensei_caution", r="kikite_surprised", sp=["#B44A4A", "#8A93A8"]),
    dict(L=88, tag="同じページに",  heroes=["card_genten19_03", "card_genten19_03_b", "card_genten19_03_c"],    sup=["el_newspaper"],
         l="sensei_point",   r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=90, tag="戻りません",    heroes=["card_19_modoranai", "card_19_modoranai_b", "card_19_modoranai_c"],   sup=[], peak=90,
         l="sensei_serious", r="kikite_surprised", sp=["#B44A4A", "#C87A72"]),
    # ── 第6章 確かめる三つ (722–792s) ──────────────────────────────────────
    dict(L=93, tag="確かめる三つ",  hero=None, stat="kakumeru", sup=["el_hand_stop", "el_magnifying_glass"],
         l="sensei_present", r="kikite_think",     sp=["#9FB6C8", "#C8B88A"]),
    dict(L=95, tag="給料明細を見る", heroes=["card_19_meisai_check", "card_19_meisai_check_b"], sup=["el_kyuryo_meisai"],
         l="sensei_point",   r="kikite_listen",    sp=["#C8B88A", "#8FA9C0"]),
    dict(L=97, tag="四か月以内",    heroes=["card_19_4kagetsu", "card_19_4kagetsu_b", "card_19_4kagetsu_c"],    sup=["el_calendar", "el_hand_stop"],
         l="sensei_caution", r="kikite_worried",   sp=["#C87A72", "#8A93A8"]),
    dict(L=100, tag="二つの窓口",   heroes=["card_19_futatsu_mado", "card_19_futatsu_mado_b"], sup=["el_signpost"],
         l="sensei_serious", r="kikite_think",     sp=["#8A93A8", "#9FB6C8"]),
    # ── 研究ノート + セルフチェック + 次回 (792–928s) ───────────────────────
    # 研究ノート chẻ đôi: bản gộp dài 48,2s — khối tĩnh dài nhất bài, rơi đúng phút 13
    # ⛔ ĐỪNG chẻ đôi 研究ノート: bảng 2 dòng trôi giữa khung trống (soi still 2026-08-31).
    #    Bảng ít dòng thì bump font cũng không cứu — thiếu SỐ DÒNG, không thiếu cỡ chữ.
    #    Scene số liệu được miễn luật 9s nên 48s là hợp lệ; 5 dòng build-on = có chuyển động.
    dict(L=102, tag="研究ノート",   hero=None, stat="note",    sup=["el_nenkin_techo"],
         l="sensei_present", r="kikite_listen",    sp=["#8FA9C0", "#C8B88A"]),
    dict(L=108, tag="セルフチェック", hero=None, stat="self",  sup=["el_magnifying_glass", "el_percent_badge"],
         l="sensei_point",   r="kikite_think",     sp=["#9FB6C8", "#8A93A8"]),
    dict(L=112, tag="ご注意",       heroes=["card_19_chuui", "card_19_chuui_b", "card_19_chuui_c"],       sup=["el_hand_stop"],
         l="sensei_serious", r="kikite_listen",    sp=["#8A93A8", "#C8B88A"]),
    dict(L=113, tag="次回予告",     heroes=["card_19_yokoku", "card_19_yokoku_b", "card_19_yokoku_c", "card_19_yokoku_d"],      sup=["el_teacup", "el_nenkin_techo"],
         l="sensei_reassure",   r="kikite_relieved",     sp=["#C8B88A", "#9FB6C8"]),
]

# ── bảng số (papercut-stat) · mọi con số từ FACT SHEET GĐ0b đã verify ──────
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#E0A32A"
GET, LOSE = "#2E6B4F", "#A82026"

STAT = {
    # 🔴 KHÔNG TÊN モニター — bảng này nay nằm ở giây 22,6 (cold open v4), mà luật
    #    `CLAUDE.md` §③ cấm モニター trong 0–120s. `check_pace.py` đọc LỜI nên
    #    không thấy tên nằm trên BẢNG ⇒ gate xanh mà vẫn vi phạm; chỉ lộ khi soi
    #    still. Tên 松本 vào từ ~2:46 như lời, bảng cold open dùng 「ひとり」.
    "hikaku": (f"{GET}|ひとり|月2万8千円" + NL + f"{LOSE}|もうひとり|0円"
               + NL + "*5年の差|168万円", 58),
    "jouken": ("①年齢|60歳以上65歳未満" + NL + "②雇用保険|5年以上"
               + NL + "*③賃金|60歳時の75%未満", 58),
    "matsumoto": ("現役のころ|月55万円" + NL + "継続雇用|月28万円"
                  + NL + "*下がった割合|53.6%", 58),
    "rate": (f"{GET}|15%だったころ|月4万2千円" + NL + f"{LOSE}|いまの10%|月2万8千円"
             + NL + "*月の差|1万4千円", 58),
    "hasetsu": ("旧・15%|61%以下で上限" + NL + "新・10%|64%以下で上限"
                + NL + "*変わったのは|率と、この線", 56),
    "jougengaku": ("賃金の上限|39万7,369円" + NL + "賃金月額の上限|52万2,000円"
                   + NL + "*最低限度額|2,562円", 58),
    "hayami": ("64%以下|10.00%" + NL + "70%|4.16%" + NL + "73%|1.59%"
               + NL + "*75%以上|0%", 50),
    "teishi": (f"{GET}|受け取る給付金|月2万8千円" + NL + f"{LOSE}|止まる年金|月1万1,200円"
               + NL + "*差し引き|月1万6,800円", 56),
    "kakumeru": ("①申請するのは|会社" + NL + "②初回の期限|4か月以内"
                 + NL + "*③年金の受給開始|切り離さない", 58),
    "note": ("一｜75%未満に下がれば対象" + NL + "二｜上限は10%（R7.3.31までは15%）"
             + NL + "三｜賃金月額の上限52万2千円" + NL + "四｜繰上げた年金は最大4%停止"
             + NL + "*五｜一度通ると停止は戻らない", 48),
    "self": ("①60歳になった日|R7.4.1の前？後？" + NL + "②いまの給料|60歳時の何%？"
             + NL + "*③会社は申請した？|給料明細を見る", 58),
}

# ── công thức (papercut-formula) — chia lại từ số đã verify, không phải số mới ──
FORMULA = {
    "warizan": ("28万円 ÷ 52万2千円 ≒ 53.6%", 80),
    "douryou": ("40万円 ÷ 52万2千円 ≒ 76.6%", 80),
}

# ── punch banner (chữ, không cần asset) ────────────────────────────────────
PUNCH = [
    (4,   "制度どおりの、結果です",      INK),
    (8,   "働いていない人には、出ません", INK),
    (20,  "四分の三を、下回ること",      AMBER),
    (30,  "五十二万二千円で、頭打ち",    AMBER),
    (44,  "五年で、八十四万円",          LOSE),
    (49,  "一日違いで、変わる",          LOSE),
    (60,  "一円も、出ません",            LOSE),
    (67,  "金額ではなく、割合",          INK),
    (88,  "二重に、削られます",          LOSE),
    (92,  "やめても、戻りません",        LOSE),
    (98,  "会社が、していないことがある", AMBER),
]

# ── TỰ ĐỘNG LẤP SÀN 7s ─────────────────────────────────────────────────────
# Luật (memory feedback_sticker_1_lan_vao_sau_hero_2s + audience-45plus §2.0):
#   · 1 sticker = ĐÚNG 1 lần trong 1 scene  → pad phải KHÁC nhau trong cùng scene
#   · dùng lại file ở scene KHÁC thì được   → video 17 (bản đã duyệt) dùng 15 file/186 lượt
#   · mỗi sticker phủ ~7s (vào +2s, sống 5s, exit) ⇒ scene D giây cần ceil((D-2)/5.5) cái
# ⇒ Chọn 1–2 cái ĐẦU bằng NGHĨA (đã viết tay ở SCENES), phần đuôi lấp bằng pool chủ đề.
POOL = [
    "el_coin_stack", "el_calendar", "el_percent_badge", "el_hand_stop", "el_signpost",
    "el_newspaper", "el_nenkin_techo", "el_magnifying_glass", "el_chart_up", "el_chart_down",
    "el_kyuryo_meisai", "el_passbook", "el_smartphone", "el_house_bills", "el_mynumber_card",
    "el_speaker_robot", "el_teacup", "el_two_men_desk", "el_zero_stamp",
    "el_senior_phone", "el_burst_red",
]
# ⛔ el_shashou (huy hiệu công ty) BỊ LOẠI 2026-08-31: generator trả về ĐĨA TRẮNG
#    trống ruột, y hệt ca el_police_badge — prompt cấm chữ nên nó không vẽ nổi mặt
#    huy hiệu. Nhịp truyện vẫn còn ở photocard card_19_matsumoto_b (cận pin trong
#    lòng bàn tay), nên bỏ sticker này không mất gì.
# ⛔ el_police_badge bị loại: CLAUDE.md §② ghi nó là "vành TRỐNG RUỘT", to lên là lộ.
# ⛔ el_heart_pulse / el_medicine_bottle / el_two_anglers: lệch chủ đề bài này.

def pad_sup(scenes, starts, total, fps=30, after=2.0, cover=5.5, only_table=False):
    """Lấp sup cho đủ sàn 7s. starts = giây bắt đầu mỗi scene."""
    cur = 0
    for i, s in enumerate(scenes):
        d = (starts[i + 1] if i + 1 < len(starts) else total) - starts[i]
        tbl = bool(s.get("stat") or s.get("formula"))
        # ⭐ user chốt 2026-08-31: scene SỐ LIỆU được miễn luật 7s ⇒ nó cũng KHÔNG cần
        #    sticker để lấp sàn. Cộng với "không muốn sticker lặp nhiều lần trong 1 video"
        #    ⇒ MỌI scene chỉ giữ ĐÚNG 1 sticker làm điểm nhấn.
        if True:
            s["sup"] = list(s.get("sup") or [])[:1]
            continue
        if only_table and not tbl:
            # scene ẢNH: hero đã đổi mỗi ~7s ⇒ sàn tự đạt. Giữ ĐÚNG 1 sticker làm điểm
            # nhấn; thêm nữa là quay lại đúng cái user kết án (lặp nhiều lần/video).
            s["sup"] = list(s.get("sup") or [])[:1]
            continue
        need = max(1, int(-(-(d - after) // cover)))
        have = list(s.get("sup") or [])
        while len(have) < need:
            for _ in range(len(POOL)):
                cand = POOL[cur % len(POOL)]; cur += 1
                if cand not in have:
                    have.append(cand); break
            else:
                break
        s["sup"] = have
    return scenes

def cap_reuse(scenes, cap=3):
    """Trần số lần một sticker xuất hiện trong CẢ video (user chốt 2026-08-31:
    'không muốn sticker lặp lại quá nhiều lần trong 1 video').
    Cái vượt trần bị thay bằng file ít dùng nhất trong POOL."""
    import collections
    cnt = collections.Counter()
    for s in scenes:
        for a in (s.get("sup") or []):
            cnt[a] += 1
    for s in scenes:
        out = []
        for a in (s.get("sup") or []):
            if cnt[a] <= cap:
                out.append(a); continue
            alt = min((p for p in POOL if p not in out),
                      key=lambda p: (cnt[p], POOL.index(p)), default=None)
            if alt is None or cnt[alt] >= cap:
                out.append(a); continue
            cnt[a] -= 1; cnt[alt] += 1
            out.append(alt)
        s["sup"] = out
    return scenes
