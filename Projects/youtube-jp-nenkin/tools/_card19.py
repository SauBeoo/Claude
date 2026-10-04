# -*- coding: utf-8 -*-
"""CARD19 — đặc tả 25 photocard cho video 19 (高年齢雇用継続給付).
Dùng: python tools/art_prompts_collage.py 19_kounenrei-koyou-keizoku-kyufu --card19

⚠️ Tên file PHẢI khớp `hero=` trong tools/_scenes19.py, không đổi tuỳ tiện.
⛔ KHÔNG bake chữ vào ảnh — chữ do Remotion vẽ bằng Noto Sans JP (kanji AI gen nát nét).
"""

CARD19 = [
    # ── COLD OPEN ─────────────────────────────────────────────────────────
    dict(file="card_19_futari.png", kind="img", bg="cold",
         note="scene 0 + scene 25 (callback cố ý) — HAI người đàn ông cùng công ty. "
              "Chủ thể phải là HAI NGƯỜI đặt cạnh nhau, đọc ra ngay là 'so sánh'.",
         scene=("two Japanese men in their early sixties in plain office shirts standing "
                "side by side in a company corridor, both holding identical brown envelopes, "
                "one looking calm and one looking uneasy, neutral office background")),
    dict(file="card_19_kyuryo_meisai.png", kind="img", bg="real",
         note="scene 2 — 給料明細 là đạo cụ chạy suốt bài (đã hứa ở cuối video 18).",
         scene=("an elderly Japanese man's hands holding a monthly payslip sheet at a kitchen "
                "table, a calculator and reading glasses beside it, the payslip showing blank "
                "ruled columns with no characters written, warm morning light")),
    dict(file="card_19_hataraku.png", kind="img", bg="calm",
         note="scene 3 — 対象は「働いているかた」. Người 60代 ĐANG làm việc, không phải nghỉ hưu.",
         scene=("a Japanese man in his early sixties in a work uniform checking inventory on "
                "a shelf in a small warehouse, a clipboard under his arm, daytime, ordinary "
                "workplace, he looks focused and unhurried")),
    dict(file="card_19_hatena.png", kind="img", bg="trap",
         note="scene 4 — ba câu hỏi mở. Không khí 'chưa biết', KHÔNG có chữ.",
         scene=("an elderly Japanese man sitting alone at a desk at dusk, looking at three "
                "identical brown envelopes fanned out in front of him, one hand resting on "
                "his chin, a desk lamp casting a soft pool of light")),
    dict(file="card_19_kenkyu.png", kind="img", bg="pale",
         note="scene 5 — nhận diện 研究室. Bàn nghiên cứu, giấy tờ chính phủ xếp gọn.",
         scene=("a tidy研究 desk seen from above with neatly stacked government leaflets, a "
                "magnifying glass, a fountain pen and a small brass desk clock on pale linen, "
                "no text visible on any paper")),
    # ── 第1章 制度の中身 ───────────────────────────────────────────────────
    dict(file="card_19_koyou_hoken.png", kind="img", bg="calm",
         note="scene 6 — 雇用保険 bù phần lương giảm. Ẩn dụ: bàn tay đỡ thêm vào.",
         scene=("a pair of older hands holding a small stack of banknotes while a second pair "
                "of hands in a public-office uniform adds a few more notes onto the stack, "
                "plain counter surface, neutral daylight")),
    dict(file="card_19_75percent.png", kind="img", bg="trap",
         note="scene 8 — ngưỡng 75%. Ẩn dụ vạch/mốc, KHÔNG viết số (Remotion vẽ chữ).",
         scene=("a measuring stick standing upright beside a short stack of coins on a wooden "
                "desk, a red thread stretched horizontally across at about three quarters of "
                "the stick's height, shallow depth of field")),
    # ── 第2章 松本さんの明細 ───────────────────────────────────────────────
    dict(file="card_19_matsumoto.png", kind="img", bg="real",
         note="scene 10 — 松本さん 60歳, 勤続38年, còn giữ 社章 trong ngăn kéo (chi tiết đời "
              "sống trong lời thoại — ảnh phải có ngăn kéo mở).",
         scene=("a Japanese man in his early sixties in a plain shirt opening a desk drawer at "
                "home and looking down at a small metal company lapel pin lying inside, quiet "
                "evening room, gentle expression of remembering")),
    dict(file="card_19_jougen.png", kind="img", bg="trap",
         note="scene 12 — 落とし穴: 賃金月額 bị KẸP TRẦN 52万2千円. Ẩn dụ: cái chặn trên.",
         scene=("a tall stack of coins on a desk with a flat wooden ruler pressed down "
                "horizontally on top of it, clearly stopping the stack from growing higher, "
                "plain surface, side lighting")),
    dict(file="card_19_28000.png", kind="img", bg="answer",
         note="scene 14 — số nhận được mỗi tháng. Không khí NHẸ NHÕM (sau khối tính).",
         scene=("an elderly Japanese man at a kitchen table looking at a bank passbook with a "
                "small relieved smile, a cup of green tea beside it, warm afternoon light "
                "through a window")),
    # ── 第3章 率が変わった ─────────────────────────────────────────────────
    dict(file="card_19_hondai.png", kind="img", bg="cold",
         note="scene 15 — 「ここからが本題」. Chuyển giọng, không khí nghiêm lại.",
         scene=("a government leaflet lying open on a desk under a desk lamp at night, one "
                "corner turned up, a pen laid across it, the rest of the room dark, no text "
                "readable on the leaflet")),
    dict(file="card_19_84man.png", kind="img", bg="trap",
         note="scene 18 — ĐỈNH BÀI, số hero 84万円. Có zoom-punch slam vào ảnh này. "
              "Cần hình ĐƠN GIẢN, đọc ra trong 1 giây khi phóng to.",
         scene=("a thick stack of ten-thousand-yen banknotes on a plain dark table with a "
                "large portion of the stack visibly torn away and missing, the torn edge "
                "ragged, dramatic single-source lighting")),
    dict(file="card_19_tanjoubi.png", kind="img", bg="trap",
         note="scene 19 — mốc chia là NGÀY SINH NHẬT 60 tuổi, không phải ngày nhận tiền.",
         scene=("a wall calendar page with one square circled in thick red marker, an elderly "
                "hand still holding the marker beside it, the other squares blank with no "
                "numbers or characters printed")),
    # ── 第4章 同僚のゼロ ───────────────────────────────────────────────────
    dict(file="card_19_wariai.png", kind="img", bg="cold",
         note="scene 21 — 「割合が厳しい」. Ẩn dụ cân/tỉ lệ.",
         scene=("an old brass balance scale on a desk, coins piled on one pan and a folded "
                "payslip on the other, the pans clearly tilted, plain background")),
    dict(file="card_19_douryou.png", kind="img", bg="real",
         note="scene 22 — người ĐỒNG NGHIỆP (lương xuống 40万, nhận 0). Có câu thoại "
              "「四十万でも十分もらってるだろう」→ vẻ cười khổ.",
         scene=("a Japanese man in his early sixties sitting alone in a company break room "
                "with a payslip in one hand, giving a wry resigned smile, a vending machine "
                "blurred in the background")),
    dict(file="card_19_zero.png", kind="img", bg="trap",
         note="scene 24 — 「一円も、出ません」. Trống rỗng, KHÔNG viết chữ ZERO.",
         scene=("an empty open palm of an elderly person held out over a desk, nothing in it, "
                "an empty brown envelope lying flat beside the hand, cold flat light")),
    # ── CTA ────────────────────────────────────────────────────────────────
    dict(file="card_19_cta.png", kind="img", bg="calm",
         note="scene 28 — khối CTA giữa video. Ấm, mời gọi.",
         scene=("two elderly Japanese people sitting together on a sofa looking at a tablet "
                "screen, both smiling gently, a teapot and two cups on the low table in front "
                "of them, warm living-room light")),
    # ── 第5章 もうひとつの窓口 ─────────────────────────────────────────────
    dict(file="card_19_madoguchi2.png", kind="img", bg="cold",
         note="scene 29 — HAI cửa sổ: 雇用保険 và 年金. Phải đọc ra là HAI quầy.",
         scene=("a public office interior with two service counters side by side, each with a "
                "blank unmarked sign above it, an elderly man standing between them looking "
                "from one to the other, clean daylight interior")),
    dict(file="card_19_tadashi.png", kind="img", bg="pale",
         note="scene 32 — 「ここは正確に申し上げます」. Cử chỉ dừng lại, đính chính.",
         scene=("an older Japanese man in a cardigan holding up one open palm in a gentle "
                "'wait a moment' gesture while seated at a desk, calm and precise expression, "
                "soft even lighting")),
    dict(file="card_19_kuriage.png", kind="img", bg="trap",
         note="scene 33 — 繰上げ受給, nối video 18. Ẩn dụ: lấy sớm thì phần còn lại nhỏ đi.",
         scene=("an hourglass tipped early on its side on a desk beside a pension handbook, "
                "sand spilled out onto the desk surface in a small pile, muted lighting")),
    dict(file="card_19_nijuu.png", kind="img", bg="trap",
         note="scene 34 — 「二重に、削られます」. HAI lần bị cắt, phải đọc ra là HAI.",
         scene=("a rectangular sheet of paper on a dark desk with two separate strips already "
                "cut away from it by scissors lying beside it, the two cut strips visible "
                "apart from the sheet, hard side light")),
    dict(file="card_19_modoranai.png", kind="img", bg="trap",
         note="scene 36 — ĐỈNH: 「やめても、戻りません」. Có zoom-punch. Hình phải ĐƠN GIẢN.",
         scene=("a one-way turnstile gate in an empty corridor seen head-on, an elderly "
                "person's hand resting on the barred arm, the gate clearly locked in one "
                "direction, cold overhead light")),
    # ── 第6章 確かめる三つ ─────────────────────────────────────────────────
    dict(file="card_19_meisai_check.png", kind="macro", bg="real",
         note="scene 38 — soi 給料明細 xem công ty có nộp không. Cận cảnh.",
         scene=("extreme close-up of an elderly finger tracing down a column on a payslip "
                "sheet, a magnifying glass held just above the paper, the ruled columns blank "
                "with no characters written")),
    dict(file="card_19_4kagetsu.png", kind="img", bg="trap",
         note="scene 39 — hạn 4 tháng cho lần nộp đầu.",
         scene=("four wall-calendar pages laid side by side on a desk, the last one with its "
                "corner already curling up, a red marker resting on top, no numbers or "
                "characters printed on the pages")),
    dict(file="card_19_futatsu_mado.png", kind="img", bg="cold",
         note="scene 40 — chốt: hai cửa sổ phải nhìn cùng lúc.",
         scene=("an elderly man seated at a desk with two separate paper documents laid out "
                "left and right in front of him, looking down at both at once, hands resting "
                "one on each, calm even daylight")),
    # ── đóng bài ───────────────────────────────────────────────────────────
    dict(file="card_19_chuui.png", kind="img", bg="pale",
         note="scene 44 — khối miễn trừ. Trung tính, không doạ.",
         scene=("a public-office information desk with a small stand holding blank leaflets, "
                "a clean counter and a chair, soft neutral daylight, nobody present")),
    dict(file="card_19_yokoku.png", kind="img", bg="calm",
         note="scene 45 — 次回予告: 佐藤さん (goá phụ, 仙台) + 通知書. Bắc cầu sang video 20.",
         scene=("an elderly Japanese woman in her mid-sixties sitting alone at a low table in "
                "a quiet room, holding an official-looking notice sheet with both hands and "
                "reading it, a cup of tea beside her, evening lamp light")),
]
