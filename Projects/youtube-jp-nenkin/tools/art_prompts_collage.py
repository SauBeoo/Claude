# -*- coding: utf-8 -*-
r"""art_prompts_collage.py — sinh prompt ảnh AI phong cách PAPER-COLLAGE (Vox/newsprint)
cho lớp SÂN KHẤU của kênh nenkin.

⭐ VÌ SAO CÓ TOOL NÀY (user chốt 2026-08-26): *"tao muốn gen video dạng E:\vox-director
vẫn có khung nhưng prompt gen ảnh sẽ dạng như này"*. Tức **GIỮ NGUYÊN** layout sân khấu
`make_stage --channel nenkin` (2 cast 2 mép + card giữa + dải phụ đề), chỉ **ĐỔI STYLE
của ẢNH** bên trong card: từ `Clean flat vector illustration` (khuôn cũ, xem
`06_VIDEO/_demo_pict/art_prompts_FLOW.txt`) sang **paper-collage newsprint** — khuôn đã
chạy được ở `E:\vox-director\out\pho-30s\PROMPTS.md`.

🔴 BA CHỖ CỐ Ý LỆCH KHỎI VOX-DIRECTOR — đọc trước khi "sửa cho giống bản gốc":

1. ⛔ **KHÔNG bake chữ vào ảnh.** vox-director bake headline vào ảnh vì nó KHÔNG có lớp
   chữ nào khác. Mình thì CÓ: `make_stage` vẽ title/cap/label bằng Noto Sans JP, luôn sắc
   nét. Và chữ Nhật do AI gen thì **nát nét** (`media-library.md` §2.9, `ab-3title-3thumb.md`
   §3 mục 8 — kanji rậm gần như chắc méo). ⇒ mọi prompt ở đây kết bằng "no text".
   Đây là lý do prompt của tool này NGẮN hơn prompt pho-30s: bỏ trọn khối HEADLINE.
2. **`bgimg` phải NHẠT.** vox-director dùng "bold flat colour per beat" cho MỌI ảnh. Nhưng
   ảnh `bgimg` của mình có **chữ navy đè lên** + màn che `bg_veil 0.78` (`media-library.md`
   §2.10 ④) ⇒ nền đậm là chữ đánh nhau với hình. Chỉ `img`/`pict` (không có chữ đè) mới
   được dùng nền màu mạnh.
3. **Người phải là NGƯỜI NHẬT CAO TUỔI**, không phải Americana/Tây (memory
   `feedback_anh_nguoi_chau_a_dong_tac`). Style newsprint mid-century rất dễ trôi về ảnh
   Mỹ thập niên 50 nếu không ghim.

⚠️ Ràng buộc hình học vẫn nguyên (`media-library.md` §2.10):
- ① `--ar` BỊ BỎ QUA, generator luôn trả **1376×768**. Đừng thiết kế theo `--ar`.
- ② layout **cover-crop**: slot `img` cắt còn 1229px (mất 11% bên phải), `bgimg` mất 9%.
- ③ ⇒ **mọi thứ quan trọng nằm trong 85% BÊN TRÁI**; 15% phải để trống (crop + ✦ watermark).
- ⑥ prompt điều khiển được VỊ TRÍ, **không** điều khiển được TỈ LỆ ⇒ ép cỡ bằng quan hệ
  với MÉP KHUNG ("cropped by the bottom edge"), đừng tả phần trăm.

CHẠY:  python tools/art_prompts_collage.py <slug>          # xuất 3 file vào 06_VIDEO/<slug>/
       python tools/art_prompts_collage.py <slug> --probe   # chỉ lô probe (mặc định hiện tại)
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]

# ══════════════════════════════════════════════════════════════════════════════
# KHỐI STYLE — CHÉP NGUYÊN Ở MỌI ẢNH (đây là thứ làm cả video trông như MỘT phim)
# Nguồn: STYLE_LIBRARY["newsprint-editorial"] + COLLAGE_MECHANICS của vox-director
# (E:\vox-director\scripts\styles.py), đã ghim thêm "Japanese" + đổi palette cho khớp
# card kem (255,250,238) và chữ navy của kênh.
# ══════════════════════════════════════════════════════════════════════════════
STYLE = (
    "Vintage newsprint editorial paper collage in the style of a mid-century JAPANESE "
    "front-page news feature: bold cut-out photographs and illustrations laid over an aged "
    "broadsheet newspaper page, heavy halftone print dots, aged newsprint texture with "
    "slight ink misregistration, tactile editorial calm — reads like a newspaper feature "
    "spread brought to life, not an advertisement. "
    "Palette: cream white, deep navy ink, deep red, mustard yellow, charcoal black."
)

MECHANICS = (
    "Clearly layered hand-cut paper cut-outs with visible torn and scissor-cut edges, tape "
    "corners and soft real paper drop shadows, on a bold flat {bg} paper background. "
    "Halftone print dots, newspaper-clipping scraps, paper-stencil shapes, aged paper "
    "texture, slight print misregistration, scattered geometric paper accents (triangles, "
    "circles, zigzags, washi tape). Figures are PRINTED / illustrated cut-outs, NOT CGI, "
    "NOT a 3D render — keep print grain and paper imperfections. {contrast}tactile, "
    "hand-assembled."
)
# 🔴 `bgimg` phải BỎ "High-contrast" — nếu không thì MECHANICS và FRAME["bgimg"] ("LOW
# CONTRAST and airy") CHỎI NHAU trong cùng một prompt, và model bốc thăm chọn một cái.
# Lỗi này đã sinh ra thật ở lượt chạy đầu (2026-08-26), sửa ngay tại đây.
CONTRAST = {"loud": "High-contrast, ", "quiet": ""}

# Ghim tệp người: style mid-century newsprint rất dễ trôi về Americana thập niên 50.
# ⚠️ KHÔNG ghim địa điểm ở đây — cảnh ngoài trời (bờ sông ở 第11章) thì câu "inside a
# Japanese home" chỏi thẳng với SCENE. Địa điểm là việc của SCENE, không phải của khối này.
PEOPLE = (
    "Any person shown is JAPANESE and elderly (60s-70s), in modest everyday Japanese "
    "clothing — not Western, not American, not 1950s retro fashion, no Americana styling."
)

# ⛔ Khối KHÔNG CHỮ — chỗ lệch lớn nhất khỏi vox-director (lý do ở docstring mục 1).
NOTEXT = (
    "All paper surfaces, documents and signs in the image are BLANK and unprinted. "
    "No text, no letters, no numbers, no headline, no caption, no signage, no logo, "
    "no watermark anywhere in the image."
)

# ── Luật khung theo TỪNG LOẠI SLOT (bảng cover-crop `media-library.md` §2.10 ②) ──
FRAME = {
    # ảnh lớn giữa card — bị cắt 11% mép phải
    # 🔴 SỬA sau lô probe (2026-08-26): bản đầu xin "the right-hand FIFTH" (20%) trống.
    # Model để trống còn NHIỀU HƠN thế (~20–25%) ⇒ cắt 10,7% xong VẪN còn ~10–15% dải kem,
    # và trong card ảnh trông LỆCH TRÁI. Phép toán đúng: cắt bỏ đúng 147/1376 = **10,7%**
    # ⇒ chỉ nên xin ~1/10 trống, để cú cắt ăn trọn dải trống, không ăn vào chủ thể.
    "img": (
        "Composition: the scene FILLS the frame edge to edge, the subject large and slightly "
        "left of centre, cropped by the bottom edge of the frame; leave only a NARROW empty "
        "strip of flat paper along the right edge, about one tenth of the width — no wider."
    ),
    # ảnh NỀN của card — CÓ CHỮ ĐÈ ⇒ phải nhạt, chừa trống nửa trên
    "bgimg": (
        "Composition: LOW CONTRAST and airy, pale and faint like a washed-out newspaper "
        "back-page — no dark masses, no heavy shadows, no strong black areas. The upper half "
        "of the frame is almost empty pale paper; all objects sit low and small along the "
        "bottom-left. This image will sit behind printed text, so it must stay quiet."
    ),
    # panel dọc trong layout `pict` — dùng fit=True nên thấy trọn, nhưng vẫn giữ chủ thể giữa
    "pict": (
        "Composition: one single clear subject, centred, filling most of the frame, on plain "
        "flat paper with generous empty margin on all four sides so the image reads at a "
        "glance when shrunk into a narrow panel."
    ),
    # cận cảnh vật — thẻ nào cần chủ thể lấp khung (§2.11 STYLE_MACRO)
    "macro": (
        "Composition: MACRO — the subject FILLS THE FRAME, tight crop, plain flat paper "
        "background, no room, no window, no furniture, nothing else competing."
    ),
    # ⭐ FULL-BLEED (user chốt 2026-08-26 lần 2, khuôn showcase-football): ảnh lấp TRỌN
    # khung 16:9, KHÔNG có card, KHÔNG cast hai mép. Ba khác biệt so với slot `img`:
    #  ① **KHÔNG chừa dải phải** — không còn cú cover-crop 11% nào, chừa là ra dải trống thật
    #     (đo được ở frame `fb_00`: dải kem bên phải lộ rõ khi lên full-bleed).
    #  ② **PHẢI chừa băng trên cho banner headline** — `make_fullbleed.py` vẽ banner ở
    #     y≈8,5–30%; ảnh không chừa thì banner CHE MẶT nhân vật (đã dính ở `fb_01`).
    #  ③ **PHẢI chừa dải đáy cho phụ đề** + góc dưới-phải cho timestamp YouTube.
    "fullbleed": (
        "Composition: a full-bleed 16:9 editorial spread — the collage fills the entire frame "
        "edge to edge with no empty margins anywhere. Keep the UPPER FIFTH of the frame as "
        "quiet flat paper and torn-paper texture only (a headline banner will be placed there, "
        "so no faces, no hands and no key objects in that band). Keep the BOTTOM SIXTH quiet "
        "as well for burned-in subtitles, and leave the very bottom-right corner free of any "
        "important detail. Place the main subject in the middle band of the frame, large."
    ),
}

# Màu nền theo BEAT (vox-director: 1 màu phẳng mỗi beat, để palette đi xuyên phim).
# ⚠️ `bgimg` LUÔN dùng "pale cream" bất kể beat — xem docstring mục 2.
BG = {
    "cold":   "aged cream newsprint",      # cold open — trung tính, vào bài
    "trap":   "deep red",                  # 2 giai đoạn cuộc gọi — nguy hiểm
    "answer": "ink charcoal navy",         # khối đối chiếu 原典 — nghiêm
    "real":   "mustard yellow",            # giấy tờ thật — sáng, an toàn
    "calm":   "warm cream",                # đóng bài / chất người
    "pale":   "pale cream",                # BẮT BUỘC cho mọi bgimg
}


def compose(kind, scene, bg):
    """Ghép 1 prompt. Thứ tự khối cố định — đổi thứ tự là đổi kết quả gen."""
    bgtxt = BG["pale"] if kind == "bgimg" else BG[bg]
    con = CONTRAST["quiet" if kind == "bgimg" else "loud"]
    scene = scene.strip().rstrip(".;") + "."     # thiếu dấu chấm là dính vào khối sau
    parts = [STYLE, MECHANICS.format(bg=bgtxt, contrast=con),
             f"SCENE (as layered paper cut-outs): {scene}"]
    # Khối ghim tệp người chỉ chèn khi cảnh CÓ người — nhồi vào ảnh chỉ có vật thì vô ích,
    # và còn dụ model tự thêm một người vào khung.
    if any(w in scene.lower() for w in
           ("man", "woman", "men", "women", "person", "people", "hand", "couple", "figure")):
        parts.append(PEOPLE)
    parts += [FRAME[kind], NOTEXT]
    return " ".join(p.strip() for p in parts)


# ══════════════════════════════════════════════════════════════════════════════
# LÔ PROBE — video 17 (詐欺の手口). 5 ảnh, phủ đủ 3 loại slot để soi style TRƯỚC
# khi gen cả lô ~25 ảnh. Đây là cảnh THẬT trong script nên gen xong dùng được luôn,
# không phải ảnh nháp bỏ đi.
# ══════════════════════════════════════════════════════════════════════════════
CARD3 = [
    # ══════════════════════════════════════════════════════════════════════════
    # LÔ 3 — 7 ảnh XOÁ LẶP. user 2026-08-26: *"nhiều chỗ dùng trùng lặp ảnh"*.
    # Đo: 31 scene có hero / chỉ 22 ảnh khác nhau ⇒ 9/31 scene (29%) dùng lại ảnh.
    # Trừ `card_c10_quiz` lặp 3 lần (CỐ Ý giữ — 3 câu quiz cùng một khung nền, đổi ảnh
    # giữa các câu là mất cảm giác "cùng một bài kiểm tra") ⇒ cần đúng 7 ảnh.
    # 🔴 Vì sao thiếu: tao tính 871s ÷ 35s = 25 scene rồi gen 25 ảnh, nhưng khi viết
    # builder lại chia 39 scene (neo theo dòng lời cho khớp nhịp) mà KHÔNG gen thêm —
    # lấp bằng cách dùng lại. Bài học: chốt SỐ SCENE trước, rồi mới báo số ảnh cần gen.
    dict(file="card_c2_te_tomaru.png", kind="img", bg="trap",
         note="scene 手が止まった (第2章 kết) — thay `card_te` lặp lần 2. Cùng khoảnh khắc "
              "nhưng GÓC KHÁC: nhìn từ trên xuống, thấy cả mặt bàn.",
         scene=("seen from directly above: an elderly Japanese man's hand hovering flat over a "
                "smartphone on a low table, not touching it; a bank passbook and a teacup "
                "beside it; a jagged red paper gap between palm and phone")),
    dict(file="card_c9_hitokoto.png", kind="img", bg="calm",
         note="scene たったひと言 (第9章 kết) — thay `card_te` lặp lần 3. Nhẹ hơn, đã thoát: "
              "bàn tay đặt xuống, điện thoại úp mặt.",
         scene=("an elderly Japanese man's hand resting calmly on a table beside a smartphone "
                "lying face-DOWN, a cup of tea steaming nearby, a torn paper exhale-swirl "
                "above; relieved, quiet")),
    dict(file="card_c4_keisatsu.png", kind="img", bg="answer",
         note="scene 警察庁も (第4章) — thay `card_c4_mynumber` lặp lần 2. Chủ thể là TRANG "
              "CẢNH BÁO của 警察庁, không phải cái thẻ.",
         scene=("a public-notice poster pinned to a board with a large round official emblem "
                "at its top and BLANK ruled lines below, a magnifying glass held over it, a "
                "torn red paper circle marking one empty line")),
    dict(file="card_c9_mail_sms.png", kind="img", bg="trap",
         note="scene メールもSMSも (第9章) — thay `card_c4_mynumber` lặp lần 3. Chủ thể là "
              "TIN NHẮN giả, không phải thẻ.",
         scene=("a smartphone held in an elderly hand with a blank message bubble on its "
                "screen, three more blank bubbles stacked behind it as paper cut-outs, a "
                "torn red paper cross over the topmost bubble; deep red ground")),
    dict(file="card_c2_hito_no_koe.png", kind="img", bg="trap",
         note="scene 人の声 (第2章 mở) — thay `card_c5_futatsu_koe` lặp lần 1. Ở đây là "
              "GIỌNG NGƯỜI thân thiện (chưa lộ), khác cảnh đối chiếu máy-vs-người ở 第5章.",
         scene=("a smiling cut-out silhouette of an unseen operator behind a telephone "
                "handset, soft paper speech curves flowing out of it, an elderly Japanese man "
                "leaning in to listen at the right; deep red ground")),
    dict(file="card_c4_genten.png", kind="img", bg="answer",
         note="scene 原典 (第4章 mở) — thay `card_c7_honmono` lặp lần 1. Chủ thể là MÀN HÌNH "
              "trang web cơ quan, không phải giấy tờ gửi về nhà.",
         scene=("a desktop computer monitor seen straight on, its screen a plain BLANK page "
                "with empty ruled lines and one torn red paper rectangle drawn around an "
                "empty area; a hand pointing at the screen; charcoal navy ground")),
    dict(file="card_c12_jikai.png", kind="img", bg="calm",
         note="scene 次回予告 (第12章 kết) — thay `card_kazoku` lặp lần 2. Chủ thể là NGÃ BA "
              "TUỔI của tập sau (60/65/70), không phải gia đình.",
         scene=("three cut-out paper signposts of different heights standing in a row on a "
                "plain path, each blank, a small elderly figure standing at the fork looking "
                "up at them; warm cream page, quiet and open-ended")),
]

CARD2 = [
    # ══════════════════════════════════════════════════════════════════════════
    # LÔ PHOTOCARD 2 — 15 hero còn thiếu cho TRỌN video 17 (12 chương, 14,5′).
    # Đo: 871s ÷ ~35s/scene = **25 scene**; đã có 10 photocard ⇒ thiếu 15.
    # Cùng luật với CARD: cảnh đầy đủ, nền màu mạnh, KHÔNG chữ (chữ do lớp
    # `papercut-banner` của Remotion vẽ). Slot ~830×556 (ratio 1,49).
    # ══════════════════════════════════════════════════════════════════════════
    # ── 第3章 止まった、ひと言
    dict(file="card_c3_kiru.png", kind="img", bg="answer",
         note="第3章 — 「電話を切りました。ガチャ、という音が」. Khoảnh khắc cúp máy.",
         scene=("an elderly Japanese man's hand slamming a telephone handset back down onto "
                "its cradle, cut from a grainy halftone photograph; three short torn-paper "
                "impact lines burst from the cradle; a quiet empty room behind")),
    dict(file="card_c3_techo.png", kind="img", bg="real",
         note="第3章 — 「年金手帳の裏表紙に、本物の番号が印刷されています」.",
         scene=("a small booklet lying open face-down to show its back cover, an elderly "
                "hand pointing at one line on it, a magnifying glass resting beside it; "
                "all as layered halftone cut-outs")),
    # ── 第4章 答え合わせ：5つの「絶対にしないこと」
    dict(file="card_c4_gotsu.png", kind="img", bg="answer",
         note="第4章 — khối 5 điều 年金機構 không bao giờ làm. 5 vật xếp thành cột, mỗi vật "
              "một hành vi; chỗ chữ để trống cho banner Remotion.",
         scene=("five small cut-out objects stacked in a vertical column with generous empty "
                "paper beside each one: a telephone, a bank passbook, an ATM keypad, a "
                "smartphone chat bubble, and a coin; a torn red paper cross mark over the "
                "whole column")),
    dict(file="card_c4_mynumber.png", kind="img", bg="trap",
         note="第4章 — 警察庁 cảnh báo xin ảnh thẻ Mynumber. Đây là đòn của cả bài.",
         scene=("a blank plastic ID card held up in front of a smartphone camera as if being "
                "photographed, a torn red paper cross mark slashed across the phone; deep "
                "red newspaper ground")),
    # ── 第5章 なぜ「もっともらしく」聞こえたのか
    dict(file="card_c5_futatsu_koe.png", kind="img", bg="trap",
         note="第5章 — cơ chế: giọng MÁY đổi sang giọng NGƯỜI. Hai nguồn âm cạnh nhau.",
         scene=("two telephone handsets side by side: the left one wrapped in mechanical "
                "concentric paper arcs, the right one with a soft cut-out human silhouette "
                "behind it; a torn paper arrow curving from left to right between them")),
    dict(file="card_c5_jiki.png", kind="img", bg="real",
         note="第5章 — kẻ gian nhắm đúng lúc giấy tờ thật về nhà (支給日/書類の時期).",
         scene=("a household letterbox with two envelopes sticking out, a wall calendar "
                "beside it with one date circled in torn red paper, and a telephone ringing "
                "on a shelf below; mustard yellow page")),
    # ── 第7章 本物の通知書
    dict(file="card_c7_honmono.png", kind="img", bg="real",
         note="第7章 — 「本物は、いつも紙で来る」. Ba loại giấy thật đã xuất hiện ở video 08/09/16.",
         scene=("three official-looking sheets of paper fanned out on a table — one long "
                "notice slip, one large postcard, one folded letter — all with BLANK ruled "
                "boxes and no writing; a pair of reading glasses resting on top")),
    dict(file="card_c7_isoganai.png", kind="img", bg="calm",
         note="第7章 — 「本物の通知は、急ぎません」. Đối lập với cú giục bấm nút.",
         scene=("a wall clock with its hands cut from paper next to a calm stack of unopened "
                "envelopes, an armchair and a cup of tea beside them; unhurried domestic "
                "quiet; warm cream page")),
    # ── 第9章 もしも電話が鳴ったら、すること3つ
    dict(file="card_c9_watasanai.png", kind="img", bg="trap",
         note="第9章 bước ① — không đưa số tài khoản / ảnh thẻ, kể cả qua mail.",
         scene=("an elderly hand held up flat in a firm stop gesture in front of a bank "
                "passbook and a blank ID card, both crossed out with torn red paper marks; "
                "deep red ground")),
    dict(file="card_c9_kakenaosu.png", kind="img", bg="answer",
         note="第9章 bước ② — cúp máy rồi tự gọi lại số in trên giấy tờ.",
         scene=("a split composition: on the left a telephone with its cord cut by a jagged "
                "torn-paper line, on the right the same hand dialling from a number printed "
                "on a booklet; a paper arrow leading left to right")),
    dict(file="card_c9_soudan.png", keys=None, kind="img", bg="real",
         note="第9章 bước ③ — gọi 9110 / 188, đừng tự quyết một mình.",
         scene=("two elderly people sitting together at a table, one holding a telephone "
                "handset and the other pointing at a leaflet between them, a police cap and "
                "a small shield shape cut from mustard paper in the corner")),
    # ── 第10章 ○×クイズ
    dict(file="card_c10_quiz.png", kind="img", bg="answer",
         note="第10章 — nền cho khối ○×クイズ. Chừa TRỐNG giữa cho 3 dòng quiz của Remotion.",
         scene=("a large torn paper circle on the left and a large torn paper cross on the "
                "right, both cut from thick card, with a wide EMPTY band of plain paper "
                "running between them across the middle of the frame")),
    # ── 第11章 釣り仲間 + 奥さま
    dict(file="card_c11_okusama.png", kind="img", bg="calm",
         note="第11章 — 「奥さまは、湯呑みを置きながら」. Beat chất người, ấm.",
         scene=("an elderly Japanese woman setting a teacup down on a low table in front of "
                "her husband, both seated, evening warmth, a teapot between them; layered "
                "halftone cut-outs on a warm cream page")),
    # ── 第12章 研究ノート + gửi gia đình
    dict(file="card_c12_note.png", kind="img", bg="answer",
         note="第12章 — nền cho slide 研究ノート 5 dòng. Chừa TRỐNG phần lớn khung.",
         scene=("an open blank notebook filling the lower third of the frame with a fountain "
                "pen resting on it, a desk lamp glowing from the top-left corner, and wide "
                "EMPTY plain paper across the upper two thirds")),
    dict(file="card_c12_okuru.png", kind="img", bg="calm",
         note="第12章 — 「離れて暮らすご家族に、送ってあげてください」.",
         scene=("an elderly hand holding a smartphone with a blank screen, a torn paper arrow "
                "flying out of it toward a small cut-out house in the upper right corner; "
                "warm cream page")),
]

CARD = [
    # ══════════════════════════════════════════════════════════════════════════
    # LÔ "PHOTOCARD" — user chốt 2026-08-26 lần 5: gen thêm ảnh SCENE để đóng khung
    # thành mảnh ảnh dán (`tools/make_photocard.py`) rồi cắm vào frame Remotion.
    # ⚠️ KHÁC lô sticker (`sticker_prompts_collage.py`): ở đây là CẢNH đầy đủ, nhiều vật,
    # nền màu mạnh — vì nó sẽ nằm trong một khung ảnh có viền giấy, không cần cutout.
    # 📐 Slot photocard ~830×556 (ratio 1,49) trong dải sân khấu 852px ⇒ chủ thể phải
    # nằm GIỮA khung, chừa mép cho viền giấy xé + tape ăn vào ~26px mỗi bên.
    # ══════════════════════════════════════════════════════════════════════════
    dict(
        file="card_kikai_no_koe.png", kind="img", bg="trap",
        note="第1章 — giọng máy đọc lời thoại giả. Cảnh: điện thoại + loa + sóng âm.",
        scene=(
            "an old desk telephone with the handset lifted off the cradle, three concentric "
            "torn-paper sound-wave arcs blasting out of the earpiece, a small cut-out speaker "
            "grille beside it; everything laid on a deep red newspaper page"
        ),
    ),
    dict(
        file="card_yonhon_no_shitsumon.png", kind="img", bg="answer",
        note="第2章 — 4 câu hỏi leo thang. Cảnh: 4 vật xếp thành hàng đi xuống (ngày sinh → "
             "địa chỉ → sổ → thẻ), vật cuối có dấu ✗ đỏ.",
        scene=(
            "four cut-out objects arranged in a descending diagonal row like steps: a blank "
            "calendar page, a plain envelope, a closed navy passbook, and a blank plastic ID "
            "card; a torn red paper cross mark sits over the last one; charcoal navy page"
        ),
    ),
    dict(
        file="card_kaigi_madoguchi.png", kind="img", bg="real",
        note="第3章 — quầy 年金事務所 thật (đối lập với cuộc gọi giả). Nền vàng sáng = an toàn.",
        scene=(
            "a public service counter seen from the visitor's side: a low counter, a small "
            "numbered ticket dispenser, a chair, and an elderly Japanese man in a cardigan "
            "standing calmly at it, all as layered halftone cut-outs on a mustard yellow page"
        ),
    ),
    dict(
        file="card_keisatsu_toukei.png", kind="img", bg="answer",
        note="第8章 — khối số liệu 警察庁. Cảnh: đồ thị + cọc tiền, KHÔNG có chữ/số "
             "(số do lớp text papercut của Remotion vẽ).",
        scene=(
            "a rising bar chart of five bars cut from red and mustard paper with a steep arrow "
            "climbing over them, a tall stack of coins at the right, a plain round official "
            "emblem pinned top-left; all on a charcoal navy newspaper page"
        ),
    ),
    dict(
        file="card_kazoku_ni_okuru.png", kind="img", bg="calm",
        note="第12章 — đóng bài: gửi 研究ノート cho gia đình. Cảnh ấm, nền kem.",
        scene=(
            "an elderly Japanese couple sitting at a low table looking together at a single "
            "smartphone held between them, a teapot and two cups beside them, warm and calm; "
            "layered halftone cut-outs on a warm cream page"
        ),
    ),
]

PROBE = [
    dict(
        file="art_denwa_furueru.png", kind="img", bg="cold",
        note="entry 0 — CHỦ THỂ của bài là CUỘC GỌI (§2.0 + §2.10 ⑦: entry 0 phải là ảnh VẬT, "
             "thẻ chữ không tính). Cold open: 「机の上のスマートフォンを、震わせました」",
        scene=(
            "a smartphone lying face-up on a low wooden table, cut from glossy photographic "
            "paper, vibrating — three torn paper arcs radiate from it like ripples; a "
            "half-drunk cup of green tea and a folded newspaper sit beside it as flat "
            "cut-outs; the phone screen is a blank pale rectangle of paper"
        ),
    ),
    dict(
        file="art_te_tomaru.png", kind="img", bg="trap",
        note="CAO TRÀO — 第2章 kết: 「——ここで、手が、止まりました」. Khoảnh khắc đắt nhất bài, "
             "nên là ảnh nặng nhất về thị giác (nền đỏ đậm).",
        scene=(
            "an elderly Japanese man's hand, cut from a grainy halftone photograph, frozen "
            "in mid-air just above a smartphone; the hand does not touch the phone — a "
            "visible gap of red paper between them; a torn paper starburst behind the gap; "
            "a bank passbook lies closed at the edge of the table"
        ),
    ),
    dict(
        file="art_tsucho_kakenaosu.png", kind="pict", bg="answer",
        note="第3章 — 「年金手帳の裏表紙に印刷された本物の番号にかけ直した」. Panel trong layout "
             "`pict`, dùng fit=True nên thấy trọn ảnh.",
        scene=(
            "an elderly Japanese man holding a small blank booklet open in one hand while "
            "pressing a phone to his ear with the other, cut out from a halftone photograph "
            "with a torn white paper border, calm and deliberate"
        ),
    ),
    dict(
        file="bg_tsukue_denwa.png", kind="bgimg", bg="pale",
        note="ẢNH NỀN của thẻ có CHỮ ĐÈ — bắt buộc nhạt (§2.10 ④). Dùng cho thẻ giải thích "
             "cơ chế ở 第5章.",
        scene=(
            "a very pale, faint newspaper-page collage of an empty desk corner: a small "
            "telephone, a closed notebook and a pencil, all cut from washed-out pale paper "
            "and placed low in the bottom-left, with wide empty pale cream paper above them"
        ),
    ),
    dict(
        file="art_tsuri_nakama.png", kind="img", bg="calm",
        note="第11章 — beat CHẤT NGƯỜI (bạn câu cá: 「俺だったら、たぶん、送ってたな」). Ảnh này "
             "là chỗ duy nhất trong bài không có giấy tờ/điện thoại — cố ý, để đổi nhịp mắt.",
        scene=(
            "two elderly Japanese men sitting side by side on a riverbank, cut from grainy "
            "halftone photographs, each holding a long fishing rod that reaches out of the "
            "frame; torn paper water ripples layered below them; a paper tackle box between "
            "them; quiet late-afternoon mood"
        ),
    ),
]


# ══════════════════════════════════════════════════════════════════════════════
# CARD18 — 10 hero còn thiếu cho video 18 (60歳繰上げ｜窓口の一言, 13 chương, 15,6′).
# 3 hero KHÁC (原典 shot#1/#2/#3) là ẢNH THẬT (screenshot 日本年金機構 đã khoanh đỏ,
# `tools/ingest_genten_18.py`) — KHÔNG nằm trong lô AI này.
# ══════════════════════════════════════════════════════════════════════════════
CARD18 = [
    dict(file="card_18_madoguchi.png", kind="img", bg="cold",
         note="第1章/第2章/第3章 (reuse 3 scene) — quầy 年金事務所, 松本 điền đơn. Hero chính "
              "của cold open, PHẢI có chủ thể 'tờ đơn' rõ (media-library §2.0).",
         scene=("an elderly Japanese man sitting at a pension-office counter, filling out a "
                "form on a clipboard, a BLANK application form with empty ruled boxes visible "
                "on the counter in front of him, a name plate and a small potted plant on the "
                "counter; calm office mood")),
    dict(file="card_18_pen.png", kind="macro", bg="trap",
         note="第1章 — 「ペン先を紙につけた——そのときです」. Cận cảnh ngòi bút chạm giấy, "
              "khoảnh khắc dừng lại. Đỉnh của cold open.",
         scene=("extreme close-up of a ballpoint pen tip touching blank ruled paper, an "
                "elderly hand holding the pen frozen mid-motion, one torn red paper spark "
                "mark at the point of contact")),
    dict(file="card_18_kakari.png", kind="img", bg="answer",
         note="第1章/第5章/第7章/第10章 (reuse 4 scene) — 係のかた (nhân viên quầy) ngẩng đầu "
              "hỏi. Callback nhiều lần nên cần biểu cảm TRUNG TÍNH, dùng lại được cho cả hỏi "
              "lẫn giải thích.",
         scene=("a Japanese pension-office clerk behind a counter looking up and speaking, "
              "one hand resting on a BLANK open booklet on the counter; a calm, attentive "
              "expression")),
    # (đổi 2026-08-30: cảnh 手を止めました bị cắt khỏi lời v3 → dùng slot này cho L=7)
    dict(file="card_18_matsumoto_counter.png", kind="img", bg="cold",
         note="第1章 kết (L=7 「計算のもとにするのは、モニターの松本さん…月十八万円」) — 松本 ngồi "
              "quầy NGHE nhân viên đưa con số, KHÁC `madoguchi` (đang điền đơn).",
         scene=("a Japanese man in his early sixties sitting at a pension-office counter, "
              "hands resting on his knees, listening attentively to a clerk across the "
              "counter who holds up a BLANK sheet of paper toward him; calm, focused")),
    dict(file="card_18_kenkyu.png", kind="img", bg="calm",
         note="第1章 kết — 「年金と老後のお金研究室は…原典の資料とあわせて確かめる場所です」. "
              "Bàn nghiên cứu: sổ tay, báo cắt, kính lúp.",
         scene=("a small research desk with a pension handbook, a folded newspaper clipping "
              "and a magnifying glass laid out neatly side by side, warm desk-lamp light, "
              "no person, quiet and orderly")),
    dict(file="card_18_tsuri.png", kind="img", bg="calm",
         note="第2章 — 「釣り仲間の、ひと言」. Hai người bạn già ngồi câu cá, một người đang "
              "nói.",
         scene=("two elderly Japanese men sitting side by side on a riverbank, each holding "
              "a long fishing rod reaching over the water, one turned mid-sentence toward "
              "the other; relaxed afternoon mood")),
    dict(file="card_18_matsumoto.png", kind="img", bg="real",
         note="第2章/第7章/第10章 (reuse 3 scene) — 松本さんの横顔 (課長), dùng được cho cả "
              "profile lẫn 'はい'/mang đơn về.",
         scene=("a Japanese man in his early sixties in a plain office shirt, seen in "
              "three-quarter profile, a calm thoughtful expression, standing in a modest "
              "office corridor")),
    dict(file="card_18_tomato.png", kind="img", bg="calm",
         note="第2章/第10章 (reuse 2 scene) — 奥さまとベランダのミニトマト.",
         scene=("an elderly Japanese woman tending a small pot of cherry tomatoes on an "
              "apartment balcony railing, watering can in hand, a few ripe red tomatoes "
              "visible among the leaves; warm late-afternoon light")),
    dict(file="card_18_kazoku.png", kind="img", bg="calm",
         note="第6章(CTA)/第9章 (reuse 2 scene) — gia đình/お願い, dùng chung cho lời mời "
              "chia sẻ VÀ khối 加給年金(配偶者).",
         scene=("an elderly Japanese couple sitting together at a small kitchen table, one "
              "leaning toward the other and gently pointing at a BLANK open booklet between "
              "them, a teapot and two cups nearby; warm, companionable mood")),
    dict(file="card_18_jikai.png", kind="img", bg="calm",
         note="第13章 (次回予告) — 継続雇用の給料明細, ngã ba tuổi kế tiếp (高年齢雇用継続給付).",
         scene=("a BLANK payslip document lying on a desk beside a small calculator and a "
              "cup of tea, an elderly man's hand resting near it about to pick it up; quiet, "
              "forward-looking mood")),
    # ── 3 ảnh TÁCH LẶP (user chốt 2026-08-30: kakari 5→2 · madoguchi 3→2 · matsumoto 3→2)
    dict(file="card_18_kakari_explain.png", kind="img", bg="answer",
         note="第5章/第7章/第8章 — clerk GIẢI THÍCH (khác `kakari` = hỏi). Tay chỉ vào sổ mở, "
              "người xem nhìn từ phía 松本.",
         scene=("a Japanese pension-office clerk seen from across the counter, leaning "
              "forward slightly and pointing with one finger at a line in a BLANK open "
              "booklet lying between them, the other hand resting on the counter; patient, "
              "explaining expression")),
    dict(file="card_18_madoguchi_close.png", kind="macro", bg="cold",
         note="第2章 kết (三つの数字) — cận tờ 請求書 trên quầy, nhìn từ trên xuống, ba ô "
              "trống xếp hàng.",
         scene=("seen from directly above: a BLANK pension application form on a counter "
              "with three empty ruled boxes in a row, a ballpoint pen laid diagonally across "
              "it, one elderly hand resting flat at the paper's edge")),
    dict(file="card_18_matsumoto_home.png", kind="img", bg="calm",
         note="第10章 (持ち帰った) — 松本 về nhà, ngồi bàn ăn, tờ đơn CHƯA khoanh đặt trước "
              "mặt, đèn bếp ấm.",
         scene=("a Japanese man in his early sixties sitting alone at a small kitchen table "
              "in the evening, a BLANK application form lying flat in front of him, his hands "
              "folded on the table, a cup of tea beside the paper; warm kitchen lamp light, "
              "thoughtful and calm")),
]


# ══════════════════════════════════════════════════════════════════════════════
# CARD24 — 41 hero cho video 24 (年金生活者支援給付金・9月の緑の封筒, 45 scene, ~13,0′).
# 3 hero KHÁC (原典 shot #1/#2/#3) là ẢNH THẬT (screenshot 日本年金機構 đã khoanh đỏ,
# cần `tools/ingest_genten_24.py` — chưa viết) — KHÔNG nằm trong lô AI này.
# 渡辺さん (66, 新潟市) và 中村さん (71, 上越市) là cast CỐ ĐỊNH của kênh — mô tả THỂ CHẤT
# giữ NGUYÊN VĂN xuyên mọi ảnh của cùng người, để AI gen ra như "một diễn viên".
# ══════════════════════════════════════════════════════════════════════════════
_WATANABE = ("a Japanese woman in her mid-sixties with short grey hair and a warm round face, "
             "wearing a simple beige cardigan over a plain blouse")
_NAKAMURA = ("a Japanese woman in her early seventies, silver hair pulled back, wearing a "
             "modest navy home cardigan")

CARD24 = [
    # ── COLD OPEN ────────────────────────────────────────────────────────
    dict(file="card_24_futou.png", kind="img", bg="cold",
         note="L=0 冒頭フック — 郵便受けに緑の封筒を見つける瞬間。動画いちばん最初の絵、PEAK。",
         scene=("a hand reaching into a household mailbox slot and pulling out a plain GREEN "
                "envelope, the envelope thin like a flyer, a few other white flyers still "
                "inside the mailbox; morning light")),
    dict(file="card_24_futou_b.png", kind="macro", bg="cold",
         note="L=0 続き — 緑の封筒のクローズアップ、切手を貼る場所の余白が見える。",
         scene=("extreme close-up of a plain GREEN envelope lying on a table, one corner "
                "slightly lifted, an empty rectangle where a postage stamp would go")),
    dict(file="card_24_taisho.png", kind="img", bg="calm",
         note="L=2 対象は六十五歳以上 — 老夫婦が郵便受けの前に立っている。",
         scene=("an elderly Japanese couple standing together in front of their home mailbox, "
                "the woman holding a few letters, both looking at the letters together, calm "
                "everyday mood")),
    dict(file="card_24_tomaru.png", kind="img", bg="trap",
         note="L=4 もうひとつ、給付金が止まった — open-loop の謎かけ。空の郵便受けに手を伸ばすが "
              "何も入っていない。",
         scene=("an elderly Japanese hand reaching into a mailbox slot but finding it EMPTY, "
                "a single dry leaf inside instead of any envelope, a slightly puzzled pause")),
    dict(file="card_24_kenkyu.png", kind="img", bg="calm",
         note="L=5 「年金と老後のお金研究室です」 — 研究デスク、緑の封筒のサンプルが置かれている。",
         scene=("a small research desk with a pension handbook, a folded newspaper clipping "
                "and a magnifying glass, and one plain GREEN envelope laid flat beside them, "
                "warm desk-lamp light, no person, quiet and orderly")),
    # ── 第1章 誰に届くのか ───────────────────────────────────────────────
    dict(file="card_24_yubinbako.png", kind="img", bg="real",
         note="L=6 「誰の郵便受けに入って、誰の家を素通りするのか」 — 二軒の郵便受け、片方に緑の封筒。",
         scene=("two identical household mailboxes side by side on a residential wall, the "
                "left one has a GREEN envelope sticking out, the right one is empty and closed")),
    dict(file="card_24_yubinbako_b.png", kind="img", bg="real",
         note="L=6 続き — もう一方のアングル、素通りする方の郵便受けにフォーカス。",
         scene=("a single closed household mailbox with no mail inside, seen up close, plain "
                "and ordinary, nothing remarkable")),
    dict(file="card_24_naka.png", kind="macro", bg="answer",
         note="L=8 緑の封筒の中身 — はがき型の請求書が一枚。",
         scene=("a single BLANK postcard-style form partly slid out of an open GREEN envelope, "
                "seen from above, a few empty ruled boxes visible on the postcard")),
    dict(file="card_24_aratani.png", kind="img", bg="calm",
         note="L=9 新たに対象になった方 — 独立した子どもの部屋、静かな家。",
         scene=("a quiet, tidy small bedroom with an empty desk and a stripped bed, as if a "
                "grown child has recently moved out, soft afternoon light through a window")),
    dict(file="card_24_setai.png", kind="img", bg="trap",
         note="L=12 世帯の全員が非課税 — 落とし穴。同居する家族全員のシルエット、ひとりだけ濃く。",
         scene=("a simple paper silhouette of three family members standing together, two "
                "silhouettes are pale cut-outs and one is a solid dark cut-out, suggesting one "
                "person's tax status is different from the rest of the household")),
    dict(file="card_24_setai_b.png", kind="img", bg="calm",
         note="L=12 続き — 引っ越しの段ボール箱、独立していく様子。",
         scene=("a few packed cardboard moving boxes stacked by a front door, a pair of shoes "
                "missing from a shoe rack, quiet and orderly")),
    dict(file="card_24_kyonen.png", kind="img", bg="calm",
         note="L=13 去年と今年で答えが変わる — カレンダーの去年と今年のページ。",
         scene=("two torn calendar pages side by side, one marked with last year's small "
                "numbers and one with this year's, a paper arrow pointing from the old page "
                "to the new one")),
    # ── 第2章 あなたの金額 — モニター 渡辺さん ─────────────────────────────
    dict(file="card_24_keisan.png", kind="img", bg="real",
         note="L=14 「いよいよ、あなたの金額です」 — 計算タイム導入。電卓とペンと紙。",
         scene=("a simple calculator, a pen and a BLANK sheet of ruled paper laid out neatly "
                "on a desk, side lamp light, about to begin a calculation")),
    dict(file="card_24_watanabe.png", kind="img", bg="calm",
         note=f"L=17 渡辺さん登場（66歳・新潟市）。以後 {_WATANABE} を厳密に再利用。",
         scene=(_WATANABE + ", sitting at her kitchen table, hands folded, a calm and "
                "attentive expression, looking slightly to one side")),
    dict(file="card_24_watanabe_b.png", kind="img", bg="calm",
         note="L=17 続き — 別アングル、新潟の家の窓越しの光。",
         scene=(_WATANABE + ", seen in gentle profile near a kitchen window, soft daylight, "
                "calm expression")),
    dict(file="card_24_watanabe_hagaki.png", kind="img", bg="answer",
         note="L=18 渡辺さんがはがきを読む — 記入欄が少ないことに気づく。",
         scene=(_WATANABE + ", holding a small BLANK postcard-style form close and reading it "
                "carefully, a few empty ruled boxes visible on the card")),
    dict(file="card_24_watanabe_hagaki_b.png", kind="macro", bg="answer",
         note="L=18 続き — はがきのクローズアップ、切手を貼る手。",
         scene=("close-up of an elderly woman's hand pressing a postage stamp onto the corner "
                "of a small BLANK postcard, careful and deliberate")),
    dict(file="card_24_tsuchi.png", kind="img", bg="real",
         note="L=19 審査結果の通知が届く — 開封された通知書の封筒。",
         scene=("a plain white official envelope, already opened, with a folded notification "
                "letter half pulled out, a BLANK amount box visible on the letter")),
    dict(file="card_24_watanabe_kingaku.png", kind="macro", bg="trap",
         note="L=22 渡辺さんの年金は月七万二千円 — 通帳のクローズアップ、金額欄は空白。",
         scene=("close-up of a Japanese bank passbook lying open on a table, a BLANK amount "
                "column visible on the page, an elderly hand resting near it")),
    dict(file="card_24_zero.png", kind="img", bg="trap",
         note="L=25 三段目、ゼロ円 — 線を越えた場合。封筒に大きな×印、または空の通帳。",
         scene=("a plain white envelope with a bold red X mark stamped diagonally across it, "
                "lying flat on a table, stark and simple")),
    dict(file="card_24_menjo.png", kind="img", bg="real",
         note="L=27 免除の期間があれば足される — 保険料免除の証明書、古い記録。",
         scene=("a small BLANK official certificate document with a torn edge, looking like an "
                "old insurance-premium exemption record, laid flat on plain paper")),
    dict(file="card_24_shougai.png", kind="img", bg="calm",
         note="L=28 障害年金・遺族年金にも別枠 — 別の窓口のイメージ、もう一つの扉。",
         scene=("a second smaller wooden door standing slightly ajar beside a larger closed "
                "door, both plain and unmarked, suggesting an additional separate pathway")),
    dict(file="card_24_kitte.png", kind="img", bg="calm",
         note="L=29 渡辺さんが引き出しから古い切手を探す。",
         scene=(_WATANABE + ", opening a small wooden desk drawer and looking inside with a "
                "faint smile, a few old loose postage stamps visible in the drawer")),
    dict(file="card_24_kitte_b.png", kind="macro", bg="calm",
         note="L=30 台詞 「はがき一枚で年三万円なら、いちばん割のいい葉書だねえ」 — 切手を貼る瞬間。",
         scene=(_WATANABE + ", pressing an old postage stamp onto a postcard with one "
                "fingertip, a small content smile, close framing on her hands and the stamp")),
    dict(file="card_24_touyu.png", kind="img", bg="calm",
         note="L=31 灯油代のぶん — 冬の灯油タンク、ひと冬の暖房代の実感。",
         scene=("a home kerosene heater tank standing in a modest entryway, a winter coat "
                "hanging nearby, quiet and homely, suggesting the cost of a winter's heating")),
    dict(file="card_24_cta.png", kind="img", bg="calm",
         note="L=32 CTA — 研究室からのお願い。スマホとお茶、reuse pattern から。",
         scene=("a smartphone and a half-finished cup of green tea resting together on a "
                "wooden table, warm and relaxed, an open notebook nearby")),
    # ── 第3章 対象なのに来ない — モニター 中村さん ─────────────────────────
    dict(file="card_24_konai.png", kind="img", bg="trap",
         note="L=33 対象のはずなのに封筒が来ない — 空っぽの郵便受け、待つ様子。",
         scene=("an empty household mailbox standing open with nothing inside, an elderly "
                "hand resting on the mailbox door, a faint sense of waiting")),
    dict(file="card_24_3kagetsu.png", kind="img", bg="answer",
         note="L=34 新たに六十五歳、三か月以内 — カレンダーに三つの丸。",
         scene=("a wall calendar with three consecutive months circled in red pen, one "
                "highlighted date near the end of the third circle marked with a small red "
                "exclamation triangle")),
    dict(file="card_24_henkou.png", kind="img", bg="calm",
         note="L=35 世帯構成の変更 — 独立した子の部屋のドアが開いている、静かな家。",
         scene=("a half-open bedroom door revealing an empty tidy room beyond, seen from a "
                "hallway, quiet late-afternoon light, suggesting a family member has moved out")),
    dict(file="card_24_tomaru_2.png", kind="img", bg="trap",
         note="L=37 冒頭の答えへの橋渡し — 止まった給付金のイメージ、時計と空の封筒。",
         scene=("a plain white envelope lying still and untouched on a table beside a small "
                "clock, a light layer of dust suggesting it has not been opened in a long time")),
    dict(file="card_24_nakamura.png", kind="img", bg="calm",
         note=f"L=38 中村さん登場（71歳・上越市）。以後 {_NAKAMURA} を厳密に再利用。",
         scene=(_NAKAMURA + ", sitting at a small kitchen table with a household ledger book "
                "open in front of her, a pencil in hand, calm and thrifty expression")),
    dict(file="card_24_nakamura_b.png", kind="img", bg="calm",
         note="L=38 続き — 別アングル、上越の家の落ち着いた雰囲気。",
         scene=(_NAKAMURA + ", seen in gentle three-quarter profile near a window, quiet "
                "composed expression")),
    dict(file="card_24_tomatta.png", kind="img", bg="trap",
         note="L=39 PEAK「来ませんでした」— 郵便受けを開けて何もないと気づく決定的瞬間。",
         scene=(_NAKAMURA + ", standing at her open mailbox, looking inside at nothing but an "
                "empty slot, a still, disappointed pause, muted late-afternoon light")),
    dict(file="card_24_saikai.png", kind="img", bg="answer",
         note="L=41 再開のボタンはあなたの側に — 電話の受話器に手を伸ばす。",
         scene=(_NAKAMURA + ", reaching one hand toward an old telephone handset on the wall, "
                "a deliberate, decided expression")),
    dict(file="card_24_soudan.png", kind="macro", bg="real",
         note="L=42 相談先、給付金専用ダイヤル — 電話をかける手元。",
         scene=("close-up of an elderly hand dialling an old-style telephone, a small notepad "
                "with a BLANK phone-number box beside it")),
    dict(file="card_24_calendar_maru.png", kind="img", bg="calm",
         note="L=43 中村さんの家計簿は鉛筆書き、カレンダーの九月に消えないペンで丸。",
         scene=(_NAKAMURA + ", drawing one deliberate circle in dark pen ink around a date on "
                "a wall calendar in the month labelled with the number nine, a pencil-written "
                "household ledger visible on the table below")),
    # ── 第4章 期限 ───────────────────────────────────────────────────────
    dict(file="card_24_kigen.png", kind="img", bg="answer",
         note="L=43-45 提出期限が印刷されたはがき — 期限の数字部分はBLANK。",
         scene=("a small postcard-style form with a printed deadline notice near the bottom "
                "edge, the date itself left as a BLANK rectangle, lying on a plain table")),
    dict(file="card_24_ichigatsu.png", kind="img", bg="trap",
         note="L=45 昨年度の例、一月五日 — 年をまたぐカレンダー、期限に赤丸。",
         scene=("a calendar spread showing the turn of the year, December fading into January, "
                "with one early January date circled in red, a slight sense of urgency")),
    dict(file="card_24_sagi.png", kind="img", bg="trap",
         note="L=47-48 詐欺注意、ATMの操作 — ATM画面に手を伸ばす影、赤信号のイメージ。",
         scene=("an elderly hand hovering just above an ATM keypad, a bold red paper stop-hand "
                "shape overlapping the hand as a warning, tense mood")),
    # ── 研究ノート + 次回 ───────────────────────────────────────────────
    dict(file="card_24_cta2.png", kind="img", bg="calm",
         note="L=54-55 次の支給日の前にも直前チェックを — カレンダーと登録ベルのイメージ。",
         scene=("a wall calendar with the number fifteen circled, a small paper notification "
                "bell shape beside it, and a half-finished cup of green tea nearby, warm mood")),
    dict(file="card_24_yokoku.png", kind="img", bg="calm",
         note="L=56 次回予告 — 遺族年金、夫婦の写真立てのイメージ。",
         scene=("a small framed photograph of an elderly couple standing on a shelf, a folded "
                "pension handbook resting beside the frame, quiet forward-looking mood")),
    dict(file="card_24_yokoku_b.png", kind="img", bg="calm",
         note="L=56 続き — 遺族年金の書類イメージ、BLANK。",
         scene=("a BLANK official document with a torn paper edge, a small dark ribbon clipped "
                "to one corner, quiet and formal mood")),
]


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    if not slug:
        print("dùng: python tools/art_prompts_collage.py <slug-video> [--probe]")
        return 1
    vdir = PROJ / "06_VIDEO" / slug
    vdir.mkdir(parents=True, exist_ok=True)
    if "--card24" in sys.argv:
        spec, tag = CARD24, "photocard24"  # video 24: 34 hero (41 file kể _b)
    elif "--card19b" in sys.argv:
        from _card19b import CARD19B
        spec, tag = CARD19B, "photocard19b"  # video 19 lô 2: 47 beat bổ sung (nhịp 9s)
    elif "--card19" in sys.argv:
        from _card19 import CARD19
        spec, tag = CARD19, "photocard19"   # video 19 lô 1: 27 hero gốc
    elif "--card18" in sys.argv:
        spec, tag = CARD18, "photocard18"  # video 18: 10 hero còn thiếu
    elif "--card3" in sys.argv:
        spec, tag = CARD3, "photocard3"    # lô 3: 7 ảnh xoá lặp
    elif "--card2" in sys.argv:
        spec, tag = CARD2, "photocard2"    # lô 2: 15 hero còn thiếu cho TRỌN video
    elif "--card" in sys.argv:
        spec, tag = CARD, "photocard"      # lô ảnh SCENE cho khung Remotion
    else:
        spec, tag = PROBE, "probe"

    flow, blocks, tenfile = [], [], []
    blocks.append(f"# Prompt ảnh AI — paper-collage newsprint · {slug} · lô `{tag}`\n")
    blocks.append(
        "Khuôn: `tools/art_prompts_collage.py` (style từ `E:\\vox-director` "
        "newsprint-editorial, đã ghim tệp Nhật + BỎ khối bake chữ).\n\n"
        "**Chữ trong ảnh — phân biệt 2 loại (chốt sau lô probe 2026-08-26):**\n"
        "- ⛔ **LOẠI:** chữ MANG NGHĨA — headline, con số, tên chế độ, chữ trên giấy tờ đủ to "
        "để đọc. Chữ Nhật do `make_stage` vẽ bằng Noto Sans JP mới là chữ của video.\n"
        "- ✅ **NHẬN:** *micro-text* li ti trên mảnh báo cắt (không đọc được ở 1080p). "
        "Prompt đã ghi 'no text' mà model vẫn vẽ, vì `newspaper-clipping scraps` **chính là** "
        "DNA của style newsprint — bỏ nó là mất style. Đây là **texture, không phải chữ**. "
        "*(Bản đầu của tool này ghi 'có chữ là loại' — sai, sẽ loại oan 3/5 ảnh probe đạt.)*\n\n"
        "⛔ Gen xong **phải xoá watermark ✦** trước khi dùng "
        "(`.claude/rules/media-library.md` §2.10 ⑤b) — lô này 1376×768 nên đường xử lý là "
        "**CẮT mép phải** (`tools/ingest_art_17.py`, cắt về 1229px), không vá.\n"
    )
    for i, s in enumerate(spec, 1):
        p = compose(s["kind"], s["scene"], s["bg"])
        flow.append(p)
        tenfile.append(f'{s["file"]:<32}<- dòng {i} FLOW  [{s["kind"]}]')
        blocks.append(f"\n## {i}. `{s['file']}`  ·  slot **{s['kind']}**  ·  nền **{BG[s['bg']] if s['kind'] != 'bgimg' else BG['pale']}**\n")
        blocks.append(f"> {s['note']}\n")
        blocks.append(f"\n```\n{p}\n```\n")

    (vdir / f"art_prompts_{tag}_FLOW.txt").write_text("\n".join(flow) + "\n", encoding="utf-8")
    (vdir / f"art_prompts_{tag}_BLOCKS.md").write_text("".join(blocks), encoding="utf-8")
    (vdir / f"art_prompts_{tag}_TENFILE.txt").write_text("\n".join(tenfile) + "\n", encoding="utf-8")

    ln = [len(x) for x in flow]
    print(f"✓ {len(flow)} prompt → {vdir}")
    print(f"   FLOW.txt (1 prompt/dòng, bơm extension) · BLOCKS.md (người đọc) · TENFILE.txt")
    print(f"   độ dài prompt: min {min(ln)} · TB {sum(ln)//len(ln)} · max {max(ln)} ký")
    for s in spec:
        print(f"   - {s['file']:<32} [{s['kind']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
