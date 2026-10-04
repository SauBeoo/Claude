# -*- coding: utf-8 -*-
"""CARD19B — 47 beat BỔ SUNG cho video 19 (nhịp đổi ảnh 9,0s).

Mỗi cảnh gốc ở `_card19.py` được chẻ thành 2–4 nhịp MÁY QUAY khác nhau của CÙNG một ý:
toàn → cận → chi tiết → dư âm. ⛔ Không phải ảnh khác chủ đề, cũng không phải cùng ảnh
đổi góc chữ — phải là **khuôn hình khác** thì mắt mới đọc ra là "đã sang cảnh mới".

Tên file PHẢI khớp `heroes=[...]` trong `_scenes19.py`.
⛔ KHÔNG bake chữ vào ảnh — chữ do Remotion vẽ (kanji AI gen nát nét).
"""

CARD19B = [
    # ── ふたりの男性 (cold open, 4 nhịp) ───────────────────────────────────
    dict(file="card_19_futari_b.png", kind="macro", bg="cold",
         note="nhịp 2 — cận HAI phong bì giống hệt nhau trong hai bàn tay khác nhau",
         scene=("close-up of two identical plain brown envelopes held side by side by two "
                "different pairs of older male hands, one pair gripping tightly, plain "
                "corridor wall behind")),
    dict(file="card_19_futari_c.png", kind="img", bg="cold",
         note="nhịp 3 — một người dừng lại đọc, người kia đi tiếp (bắt đầu tách số phận)",
         scene=("an office corridor seen from behind: one Japanese man in his sixties has "
                "stopped to read a sheet of paper, while another man of the same age walks "
                "on ahead toward a door, motion slightly blurred")),
    dict(file="card_19_futari_d.png", kind="img", bg="real",
         note="nhịp 4 — hai tủ đồ cạnh nhau, chi tiết nơi làm việc",
         scene=("two adjacent metal employee lockers in a workplace changing room, both "
                "doors closed, a folded work jacket hanging on a hook between them, plain "
                "fluorescent light")),
    # ── 五年で百六十八万円 ─────────────────────────────────────────────────
    dict(file="card_19_kyuryo_meisai_b.png", kind="macro", bg="real",
         note="nhịp 2 — cận tờ minh細 để trên bàn, vết vòng cốc cà phê",
         scene=("close-up of a payslip sheet lying flat on a wooden kitchen table with a "
                "faint coffee cup ring stain on the corner, reading glasses folded beside "
                "it, the ruled columns blank")),
    # ── 対象は ─────────────────────────────────────────────────────────────
    dict(file="card_19_hataraku_b.png", kind="img", bg="calm",
         note="nhịp 2 — bàn tay đang xếp thùng, nhấn 'vẫn đang lao động'",
         scene=("older Japanese hands lifting a cardboard box onto a shelf in a small "
                "warehouse, work gloves worn at the fingertips, daylight from a high window")),
    dict(file="card_19_hataraku_c.png", kind="img", bg="calm",
         note="nhịp 3 — bấm thẻ chấm công, đúng nghĩa 'người ĐANG làm'",
         scene=("an older man's hand inserting a blank time card into a wall-mounted time "
                "clock machine in a workplace entrance, no characters printed on the card")),
    # ── 三つの問い ─────────────────────────────────────────────────────────
    dict(file="card_19_hatena_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận ba phong bì xoè, chưa mở cái nào",
         scene=("close-up of three plain brown envelopes fanned out on a dark desk under a "
                "single lamp, all still sealed, no writing on them")),
    dict(file="card_19_hatena_c.png", kind="img", bg="trap",
         note="nhịp 3 — lật mặt sau một phong bì, cử chỉ ngờ vực",
         scene=("an elderly man turning one brown envelope over in his hands to look at the "
                "back of it, slight frown, dim evening room, desk lamp light from the side")),
    # ── 研究室 ─────────────────────────────────────────────────────────────
    dict(file="card_19_kenkyu_b.png", kind="macro", bg="pale",
         note="nhịp 2 — cận kính lúp trên tờ tài liệu",
         scene=("close-up of a magnifying glass resting on an open government leaflet on pale "
                "linen, the paper texture visible through the lens, no readable text")),
    # ── 下がった分を補う ───────────────────────────────────────────────────
    dict(file="card_19_koyou_hoken_b.png", kind="macro", bg="calm",
         note="nhịp 2 — cận đúng lúc mấy tờ tiền được đặt thêm vào",
         scene=("extreme close-up of two banknotes being placed on top of a small stack of "
                "banknotes resting in an open older palm, the giving hand only partly in "
                "frame, soft neutral light")),
    # ── 七十五パーセント未満 ───────────────────────────────────────────────
    dict(file="card_19_75percent_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận sợi chỉ đỏ cắt ngang thước, đúng chỗ 'vạch'",
         scene=("extreme close-up of a taut red thread crossing horizontally in front of a "
                "wooden measuring stick, the thread in sharp focus and the stick's markings "
                "blurred behind it")),
    # ── 松本さん ───────────────────────────────────────────────────────────
    dict(file="card_19_matsumoto_b.png", kind="macro", bg="real",
         note="nhịp 2 — cận huy hiệu công ty trong lòng bàn tay (chi tiết đời sống trong thoại)",
         scene=("close-up of a small worn metal company lapel pin lying in the centre of an "
                "older man's open palm, the enamel face plain and unmarked, warm lamp light")),
    dict(file="card_19_matsumoto_c.png", kind="img", bg="real",
         note="nhịp 3 — đóng ngăn kéo lại, nhìn nghiêng. Đóng một chương đời.",
         scene=("side view of an older Japanese man quietly pushing a desk drawer closed with "
                "one hand, looking down, a table lamp lit behind him in a plain room")),
    # ── 落とし穴（上限522,000円） ──────────────────────────────────────────
    dict(file="card_19_jougen_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận cây thước ép xuống đỉnh chồng xu",
         scene=("extreme close-up of a flat wooden ruler pressed down firmly on the top coin "
                "of a stack, the coins slightly compressed under it, hard side lighting")),
    dict(file="card_19_jougen_c.png", kind="img", bg="trap",
         note="nhịp 3 — mấy đồng xu rơi ra ngoài: phần vượt trần bị bỏ",
         scene=("a few coins that have slid off a stack and come to rest on the desk beside "
                "it, the stack itself still capped by a wooden ruler in the background, "
                "shallow depth of field")),
    dict(file="card_19_jougen_d.png", kind="img", bg="trap",
         note="nhịp 4 — bàn tay cố đặt thêm một đồng nữa, bị chặn",
         scene=("an older hand holding a single coin just above a capped stack of coins, "
                "unable to place it because a ruler lies across the top, the hand paused in "
                "mid-air, dramatic side light")),
    # ── 二万八千円 ─────────────────────────────────────────────────────────
    dict(file="card_19_28000_b.png", kind="macro", bg="answer",
         note="nhịp 2 — cận dòng trong sổ ngân hàng",
         scene=("extreme close-up of an open bank passbook page with ruled entry lines, an "
                "older finger resting under one line, the entries blank with no characters, "
                "warm window light")),
    dict(file="card_19_28000_c.png", kind="img", bg="answer",
         note="nhịp 3 — nhìn từ trên: sổ + tách trà, không khí nhẹ",
         scene=("overhead view of a kitchen table with an open bank passbook, a cup of green "
                "tea and a pair of reading glasses arranged on it, warm afternoon light "
                "falling across the wood")),
    # ── ここからが本題 ─────────────────────────────────────────────────────
    dict(file="card_19_hondai_b.png", kind="macro", bg="cold",
         note="nhịp 2 — cận góc tài liệu bị gập lên",
         scene=("extreme close-up of the turned-up corner of a government leaflet on a dark "
                "desk under a narrow beam of lamp light, the rest of the page falling into "
                "shadow, no readable text")),
    # ── 八十四万円（ĐỈNH） ────────────────────────────────────────────────
    dict(file="card_19_84man_b.png", kind="img", bg="trap",
         note="nhịp 2 — phần bị xé nằm RIÊNG ra: cái đã mất, không lấy lại được",
         scene=("a torn-away portion of a banknote stack lying separately on a dark table, "
                "well apart from the remaining stack, the torn edges ragged, single hard "
                "light source")),
    # ── 分かれ目は誕生日 ───────────────────────────────────────────────────
    dict(file="card_19_tanjoubi_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận ô lịch bị khoanh đỏ",
         scene=("extreme close-up of one square on a wall calendar circled in thick red "
                "marker, the surrounding squares blank with no numbers printed, paper "
                "texture visible")),
    dict(file="card_19_tanjoubi_c.png", kind="img", bg="trap",
         note="nhịp 3 — HAI tờ lịch cạnh nhau, một khoanh một không: đúng ý 'một ngày khác nhau'",
         scene=("two wall-calendar pages laid side by side on a desk, the left one with a "
                "single square circled in red and the right one completely unmarked, all "
                "squares blank of numbers")),
    dict(file="card_19_tanjoubi_d.png", kind="img", bg="trap",
         note="nhịp 4 — nắp bút để hở bên cạnh: dấu vết vừa quyết xong",
         scene=("a red marker lying uncapped beside a wall calendar on a desk, its cap "
                "resting a little apart, soft overhead light, quiet aftermath mood")),
    # ── 同僚のかた ─────────────────────────────────────────────────────────
    dict(file="card_19_douryou_b.png", kind="macro", bg="real",
         note="nhịp 2 — cận tờ minh細 trong tay ông đồng nghiệp",
         scene=("close-up of a payslip sheet held in one older male hand, the fingers "
                "gripping the paper slightly too hard so it creases, blurred break-room "
                "background")),
    dict(file="card_19_douryou_c.png", kind="img", bg="real",
         note="nhịp 3 — gấp tờ giấy cho lại vào phong bì: chấp nhận, không cãi",
         scene=("an older Japanese man sliding a folded sheet of paper back into a brown "
                "envelope while seated in a company break room, looking down, quiet resigned "
                "posture")),
    # ── 一円も、出ません ───────────────────────────────────────────────────
    dict(file="card_19_zero_b.png", kind="img", bg="trap",
         note="nhịp 2 — phong bì rỗng nằm một mình trên bàn",
         scene=("a single empty brown envelope lying flat and alone on a bare desk, its flap "
                "open, nothing else in the frame, flat cold lighting from above")),
    # ── お願いです (CTA) ───────────────────────────────────────────────────
    dict(file="card_19_cta_b.png", kind="macro", bg="calm",
         note="nhịp 2 — cận màn hình máy tính bảng (để TRỐNG, không chữ)",
         scene=("close-up of an older couple's hands holding a tablet with a completely blank "
                "pale screen, warm living-room light, no icons or text on the screen")),
    dict(file="card_19_cta_c.png", kind="img", bg="calm",
         note="nhịp 3 — rót thêm trà: nhịp nghỉ giữa bài",
         scene=("an older hand pouring green tea from a teapot into a second cup on a low "
                "living-room table, steam rising, warm evening light")),
    dict(file="card_19_cta_d.png", kind="img", bg="calm",
         note="nhịp 4 — hai người nhìn nhau, cùng hiểu ra",
         scene=("an elderly Japanese couple seated on a sofa turning to look at each other "
                "with small knowing smiles, a tablet resting face-down on the table in front "
                "of them, warm lamp light")),
    # ── 二つ目の窓口 ───────────────────────────────────────────────────────
    dict(file="card_19_madoguchi2_b.png", kind="img", bg="cold",
         note="nhịp 2 — một quầy, ghế trống trước mặt: chưa ai ngồi xuống",
         scene=("a single public-office service counter photographed straight on with an "
                "empty chair placed in front of it, a blank unmarked sign above, clean "
                "daylight interior, nobody present")),
    # ── ここは正確に ───────────────────────────────────────────────────────
    dict(file="card_19_tadashi_b.png", kind="macro", bg="pale",
         note="nhịp 2 — cận bàn tay ngửa ra, cử chỉ 'khoan đã'",
         scene=("close-up of an older open palm raised in a calm 'wait a moment' gesture, "
                "fingers relaxed, soft even light, plain pale background")),
    dict(file="card_19_tadashi_c.png", kind="img", bg="pale",
         note="nhịp 3 — chỉnh lại kính, cân nhắc câu chữ",
         scene=("an older Japanese man in a cardigan adjusting his reading glasses with one "
                "hand while looking down at a document on the desk, thoughtful and unhurried "
                "expression")),
    # ── 繰上げ受給 ─────────────────────────────────────────────────────────
    dict(file="card_19_kuriage_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận đống cát đã đổ ra ngoài",
         scene=("extreme close-up of a small pile of fine sand spilled on a dark desk "
                "surface, a few grains scattered away from the pile, the base of a glass "
                "hourglass blurred behind")),
    dict(file="card_19_kuriage_c.png", kind="img", bg="trap",
         note="nhịp 3 — đồng hồ cát dựng lại nhưng đã vơi: không hoàn nguyên",
         scene=("an hourglass standing upright again on a desk but visibly less than half "
                "full, a small amount of loose sand still on the desk beside it, muted "
                "side lighting")),
    # ── 二重に、削られます ─────────────────────────────────────────────────
    dict(file="card_19_nijuu_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận kéo và một dải giấy vừa cắt rời",
         scene=("close-up of a pair of scissors lying open beside one narrow strip of paper "
                "freshly cut from a larger sheet, the cut edge crisp, hard directional light")),
    dict(file="card_19_nijuu_c.png", kind="img", bg="trap",
         note="nhịp 3 — HAI dải giấy nằm song song: đọc ra ngay là hai lần bị cắt",
         scene=("two narrow paper strips laid parallel to each other on a dark desk, clearly "
                "separated from the remaining sheet beside them, even overhead light")),
    # ── 戻りません（ĐỈNH） ────────────────────────────────────────────────
    dict(file="card_19_modoranai_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận thanh chắn cửa quay, đã khoá một chiều",
         scene=("extreme close-up of the barred arm of a one-way turnstile gate with an "
                "older hand resting on it, the locking mechanism visible, cold overhead "
                "light, metal texture")),
    dict(file="card_19_modoranai_c.png", kind="img", bg="trap",
         note="nhịp 3 — hành lang phía bên kia cổng, trống: đã qua rồi",
         scene=("an empty corridor seen through and beyond a turnstile gate, the gate in the "
                "near foreground out of focus, nobody in the corridor, cold flat lighting")),
    # ── 給料明細を見る ─────────────────────────────────────────────────────
    dict(file="card_19_meisai_check_b.png", kind="img", bg="real",
         note="nhịp 2 — đặt kính lúp xuống cạnh tờ giấy: đã soi xong",
         scene=("a magnifying glass set down on a table beside a payslip sheet, an older "
                "hand withdrawing from frame, the ruled columns on the sheet blank, warm "
                "kitchen light")),
    # ── 四か月以内 ─────────────────────────────────────────────────────────
    dict(file="card_19_4kagetsu_b.png", kind="macro", bg="trap",
         note="nhịp 2 — cận góc tờ lịch cuối đang cong lên",
         scene=("extreme close-up of the curling corner of the last of several stacked "
                "calendar pages on a desk, the paper edge lifting, no numbers printed, "
                "shallow focus")),
    dict(file="card_19_4kagetsu_c.png", kind="img", bg="trap",
         note="nhịp 3 — xé một tờ lịch: thời gian đang trôi mất",
         scene=("an older hand tearing a page away from a wall calendar, the torn page "
                "half-detached and curling, remaining pages blank of numbers, plain wall "
                "behind")),
    # ── 二つの窓口 ─────────────────────────────────────────────────────────
    dict(file="card_19_futatsu_mado_b.png", kind="macro", bg="cold",
         note="nhịp 2 — cận HAI bàn tay đặt lên hai tờ giấy khác nhau",
         scene=("close-up from above of two older hands resting flat on two separate "
                "documents laid side by side on a desk, one hand on each, the papers blank "
                "and ruled, even daylight")),
    # ── ご注意 ─────────────────────────────────────────────────────────────
    dict(file="card_19_chuui_b.png", kind="macro", bg="pale",
         note="nhịp 2 — cận giá để tờ rơi, các tờ trống",
         scene=("close-up of a small counter-top leaflet stand holding several blank pale "
                "leaflets, soft neutral daylight, no printing on any of them")),
    dict(file="card_19_chuui_c.png", kind="img", bg="pale",
         note="nhịp 3 — chiếc ghế trống trước quầy: mời tới hỏi",
         scene=("a single empty chair placed in front of a clean public-office information "
                "counter, seen at a slight angle, soft daylight, nobody present")),
    # ── 次回予告 ───────────────────────────────────────────────────────────
    dict(file="card_19_yokoku_b.png", kind="macro", bg="calm",
         note="nhịp 2 — cận tờ thông báo trong tay bà (bắc cầu sang video 20)",
         scene=("close-up of an official-looking notice sheet held in both hands of an "
                "elderly Japanese woman, the printed area blank and ruled, soft evening "
                "lamp light")),
    dict(file="card_19_yokoku_c.png", kind="img", bg="calm",
         note="nhịp 3 — cặp kính đọc đặt xuống bên cạnh: vừa đọc xong",
         scene=("a pair of reading glasses set down on a low table beside a folded notice "
                "sheet and a teacup, warm lamp light, the chair behind slightly out of "
                "frame")),
    dict(file="card_19_yokoku_d.png", kind="img", bg="calm",
         note="nhịp 4 — bóng bà bên đèn, phòng lúc chạng vạng: đóng bài",
         scene=("an elderly Japanese woman seen in soft silhouette sitting alone beside a lit "
                "floor lamp in a quiet room at dusk, her posture calm, warm pool of light "
                "around her")),
]
