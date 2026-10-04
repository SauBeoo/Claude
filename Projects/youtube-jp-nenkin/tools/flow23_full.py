# -*- coding: utf-8 -*-
"""
flow23_full.py — xuất TOÀN BỘ prompt Veo cho video 23, từ chính bảng `_scenes23.py`.

Copy khuôn từ `flow22_full.py` + **đã gộp sẵn 3 miếng vá đắt nhất của video 22** (khỏi phải
chạy `redo2`/`redo3`):
  ① CHÍNH SÁCH SỐ THEO TỪNG KHE (`_scenes23.NUM`) — khe không nói về tiền thì **bỏ hẳn**
     yêu cầu số to, thay vì dán một cặp số vào cả lô (video 22: 22/62 khe bị nhét cùng một
     cặp ⇒ model coi số là hoa văn rồi bóp méo: 36,0000 · 1800000 · 180,00円).
  ② GUARD CHỮ CŨNG PHẢI ĐỔI THEO KHE — đây là chỗ video 22 dính **hai lần**: sửa khe NONE
     xong mà khối chung `TXT` vẫn còn câu "printed large and crisp" ⇒ ngay sau khi cấm số to,
     prompt lại xin số to. Ở đây `TXT` có hai bản, chọn theo chính sách số.
  ③ Số CHỐT của mỗi scene vẫn do Remotion dán đè bằng font (`papercut-stat`/`telop`) ⇒ luôn
     sắc và luôn đúng. Veo chỉ dựng **khung rỗng** (`SCREEN_FILL` của `_scenes23.py`).

Xuất 3 file + 3 lô:
  flow23_FULL_FLOW.txt      — mỗi prompt 1 dòng, bơm thẳng vào extension
  flow23_FULL_TENFILE.txt   — dòng ↔ tên file đích ↔ scene ↔ khuôn ↔ bên chừa trống
  flow23_LOT1.txt           — 12 prompt ĐẦU đủ mọi khuôn, GEN THỬ TRƯỚC
  (LOT2/LOT3 chia phần còn lại)

🔴 VÌ SAO CÓ LÔ 1: lô 16 clip của video 21 hỏng CẢ LÔ vì lỗi cấp khuôn (chữ nát 0/6 · glow
   tô đỏ da tay). Chạy thẳng ~90 cái là hỏng ~90 cái.
"""
import collections, io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
from _scenes23 import NUM  # noqa: E402

OUT = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
       r"\23_nenkin-seikyusho-todokanai")

# ── KHỐI CHUNG ───────────────────────────────────────────────────────────────
# 🔴 PHÒNG + ÁNH SÁNG + PALETTE đi THÀNH BỘ và xoay theo `idx`. Tách ba thứ đó ra rồi xoay
#    riêng là sinh tổ hợp vô lý (bếp + rèm voan phòng khách + tatami vàng rơm).
# 🔴 Đo trên 73 prompt cũ của video 22: **52 prompt chứa nguyên văn "sheer curtains"** ⇒ 52
#    clip CÙNG MỘT CĂN PHÒNG. Không phải Veo kém — nó trả về đúng thứ được yêu cầu.
SETTINGS = [
    ("a Japanese living room with a low table, a shoji screen and a garden window behind",
     "warm morning sunlight through the shoji, soft diffused light, high key but not blown out",
     "cream walls, warm wood, one green houseplant"),
    ("a small Japanese kitchen with a dining table, wall cupboards and a kettle on the stove",
     "flat overcast daylight from a side window plus a warm ceiling lamp",
     "pale mint cupboards, stainless steel, a deep red kettle"),
    ("a tatami room with a low chabudai table and a wall alcove",
     "late afternoon sun raking low across the tatami, long soft shadows",
     "straw-gold tatami, dark wood posts, one indigo floor cushion"),
    ("an engawa veranda looking out onto a small garden",
     "bright outdoor daylight bouncing in, cool shade under the eaves",
     "green garden foliage, weathered wood, white shoji paper"),
    ("a cluttered home study with a desk, filing shelves and a wall calendar",
     "a desk lamp plus dim window light, a warmer pool of light on the desk",
     "brown box files, olive walls, warm amber lamplight"),
    ("the genkan entrance hall of a Japanese house, shoe step and open front door",
     "hard daylight coming through the open door, deep shade further inside",
     "grey concrete step, pale wood frame, a navy door mat"),
    ("a public waiting area with rows of linked chairs and a wall notice board",
     "even fluorescent ceiling light plus daylight from a tall window wall",
     "grey-blue chairs, white walls, one green corner plant"),
    ("a bank branch counter with low partitions and a queue rail",
     "bright even interior lighting, a glass frontage behind",
     "pale wood counters, teal accents, brushed metal"),
]


# 🔴 Bối cảnh 6 và 7 KHÔNG CÓ BÀN RIÊNG (khu chờ ghế liền · quầy ngân hàng). Cảnh nào nói
#    「ngồi ở BÀN」/「TRÊN BÀN có…」 mà rơi vào đó là tự chọi: đo được 7/92 clip, nặng nhất
#    khuôn DESK (nó luôn kèm khối `ON THE TABLE:`). Cùng họ lỗi video 22 nhét tả phòng khách
#    vào 10 cảnh CROWD — chỉ khác là lần này thiếu chiều ngược lại.
TABLE_POOL = [0, 1, 2, 4]          # phòng khách · bếp · tatami · phòng làm việc


def setting(idx: int, need_table: bool = False):
    if need_table:
        return SETTINGS[TABLE_POOL[idx % len(TABLE_POOL)]]
    return SETTINGS[idx % len(SETTINGS)]


# ⭐ PHƯƠNG ÁN LAI: Veo gen NGƯỜI photoreal, còn mũi tên · bảng số · dấu ✗ · lấp lánh do
#    **Remotion vẽ đè** bằng lớp `fx`. ⇒ mỗi khung PHẢI CHỪA MỘT BÊN TRỐNG, nếu không đồ hoạ
#    dán chồng lên mặt người. Bên chừa xoay đều và ghi vào TENFILE cho builder.
CLEAR = ("COMPOSITION: keep the {s} third of the frame visually empty and simple — plain wall, "
         "plain floor or open space with nothing important in it — and put the subject in the "
         "other two thirds")


def gside(idx: int) -> str:
    return "right" if idx % 2 == 0 else "left"


# Đạo cụ TIỀN THẬT — chỉ gắn khi cảnh vốn nói về tiền/phong bì/sổ, đừng rải bừa.
MONEY_PROP = [
    "a banded bundle of ten-thousand-yen notes lying on the table",
    "three neat stacks of coins of clearly different heights on the table",
    "an opened envelope with banknotes showing at its mouth",
    "a bank passbook lying open next to a small heap of coins",
]
MONEY_CUE = ("envelope", "passbook", "notes", "bank", "coins", "calculator", "account book")

LIGHT_PUB = ("a bright public interior lit evenly by ceiling lights and by daylight from a tall "
             "window wall, soft diffused light, high key but not blown out")
COLOR_PUB = ("rich natural colours, pale wood counters, soft blue and grey office tones, a green "
             "plant in one corner, not desaturated")

# ── LỚP ĐỒ HOẠ 2D/3D ────────────────────────────────────────────────────────
# ⭐ Mẫu ngách TRỘN HAI STYLE: photoreal cho người thật, **illustration 2D/3D cho khối siêu
#    thực** (khiên vàng chặn chữ 税, đồng hồ cát, mặt đồng hồ 24h). Điều này KHÔNG phá luật
#    ⛔BỎ ANIME — nó GIẢI THÍCH luật đó: luật sinh ra vì "shot siêu thực với NGƯỜI THẬT thì
#    quái dị"; mẫu tránh đúng cái đó bằng cách đổi style cho riêng khối siêu thực.
# ⚠️ META là ẩn dụ VẬT THỂ 3D — gọi nó là "flat artwork" là chọi chính dòng style của nó
#    (gate ⑧). INFOG mới là mặt phẳng 2D.
LIGHT_2D = ("evenly lit flat artwork on a light neutral ground, soft even shading, high key "
            "but not blown out")
LIGHT_3D = ("an evenly lit rendered scene on a light neutral ground, soft directional key "
            "light and gentle ambient fill, high key but not blown out")
COLOR_GRAPH = ("a warm cream ground with navy, soft blue, amber and muted green accents, "
               "not desaturated")
# 🔴🔴 NOTE CHỈ NÓI **HÌNH THỨC**, TUYỆT ĐỐI KHÔNG NÓI CHUYỂN ĐỘNG — chuyển động là NỘI DUNG,
#    và nội dung do mô tả scene quyết (CLAUDE.md §②). Bản copy từ video 22 kê sẵn hành vi
#    trong NOTE và nó CHỌI THẲNG mô tả scene, bắt được khi đọc trọn prompt 2026-09-12:
#    · GAUGE scene 73 「待っても増えない」 — SUBJECT: kim *nằm im giữa cung*; NOTE cũ:
#      *"kim quét từ trái sang rồi dừng"*. Cảnh mà cả ý nghĩa là KHÔNG NHÚC NHÍCH.
#    · META scene 23 「ひと月ずつ」 — SUBJECT: *mười một khối còn lại đứng im tuyệt đối*;
#      NOTE cũ: *"các vật trôi và xoay chậm"*.
#    Gate ⑧/㉓ đều xanh vì chúng chỉ hỏi "NOTE có mặt không", không hỏi "NOTE có nói ngược
#    mô tả không". ⇒ lần thứ tư của bệnh "khối chung huỷ mô tả scene".
GAUGE_NOTE = ("a large semicircular gauge dial with a needle, a green zone on the left and an "
              "amber zone on the right, tick marks around the arc, rendered as a clean 3D panel "
              "standing in the room")
# 🔴 Bỏ "gently glowing edges" — chọi `no glow` ở khối máy quay (lỗi này đã dính 3 lần).
META_NOTE = ("rendered as a polished 3D illustration, not a photograph: smooth stylised shapes, "
             "soft clean shading, clean crisp silhouettes")
# 🔴 KHUÔN ĐỒ HOẠ KHÔNG CÓ BIẾN XOAY NÀO ⇒ scene được cấp 2 clip sẽ ra HAI PROMPT GIỐNG HỆT
#    (bắt 2026-09-12: scene 9 dài 15,3s ⇒ 2 clip, và cả hai y nguyên một chuỗi).
#    Khuôn có người thì `FRAMING`/`REACTION`/`SETTINGS` tự xoay theo `idx` nên không dính;
#    khuôn đồ hoạ bỏ hết mấy khối đó nên mất luôn cơ chế phân biệt. ⇒ phải có biến GÓC NHÌN
#    riêng. Đây là biến KHÔNG đụng nội dung, chỉ đổi chỗ đứng của máy.
GFX_VIEW = [
    "seen straight on at eye level, the objects centred and filling most of the frame",
    "seen from slightly above and a little to one side, the objects grouped low in the frame",
    "seen from a low angle close to the surface, the objects large in the foreground",
    "seen straight on from further back, the objects smaller and the empty ground around them "
    "clearly visible",
]
INFOG_NOTE = ("a clean flat infographic panel fills almost the whole frame: rounded boxes in soft "
              "pastel colours, simple line icons, thin connector arrows between the blocks, and "
              "one or two small illustrated figures standing at the edge")

# ══ GUARD CHỮ — HAI BẢN, CHỌN THEO CHÍNH SÁCH SỐ CỦA KHE ════════════════════
# 🔴 Bài học 12 của video 22, vế thứ hai: khối chung nói NGƯỢC với miếng vá. Khe đã bị cấm
#    số to mà `TXT` vẫn xin "printed large and crisp" ⇒ Veo tự bịa một con số cho đủ.
#    Chỉ bắt được khi **đọc lại prompt ĐÃ XUẤT RA** — nên gate ở `check_flow23.py` quét
#    bản thành phẩm, không quét hằng nguồn.
TXT_NUM = ("the only characters meant to be read in the frame are Arabic numerals printed large "
           "and crisp in a clean sans-serif; any Japanese writing on signs, labels, book spines "
           "or form headings stays small and softly out of focus; no captions, no subtitles, "
           "no watermark, no logo")
TXT_NONE = ("nothing in the frame is meant to be read: every figure and every piece of Japanese "
            "writing on signs, labels, screens, books or forms stays small and softly out of "
            "focus, dense grey texture rather than anything legible; no captions, no subtitles, "
            "no watermark, no logo")

# Giấy tờ tiền của Nhật KÍN ĐẶC. user nhắc HAI lần ở video 22 (*"cả 1 trang giấy trắng và cả
# 1 cái màn hình, hiển thị được 1, 2 dòng"*). Nền là KẾT CẤU, cố ý nhỏ tới mức không đọc rời
# từng số được ⇒ nó không thể thành "số sai" trên màn hình.
DENSE = ("the page is DENSELY filled the way a real financial document is — more than twenty "
         "ruled lines running to the very bottom, several narrow columns, hundreds of small "
         "printed figures marching down those columns, tick boxes, a stamped seal and a totals "
         "line at the foot, with almost no empty white space left anywhere. Those background "
         "figures are deliberately tiny — dense grey texture rather than anything readable")


def num_clause(scene: int):
    """Mệnh đề SỐ của khe. Trả (clause, has_number).

    🔴 `ONE:` phải nói ĐÚNG MỘT LẦN + đánh vần từng chữ số. Hai ca méo của video 22
       (`c22_02`, `c22_38`) đều là ca model vẽ con số HAI LẦN rồi bản thứ hai degrade —
       guard cũ nói "đúng hai dòng được tô sáng" nhưng KHÔNG CẤM bản sao.
    """
    pol = NUM.get(scene)
    if not pol:
        return None, False
    if pol == "PAIR":
        return ("exactly TWO lines are printed much larger than the rest and highlighted in a "
                "pale colour band, and those two lines carry the SAME figure as each other, "
                "each appearing once and nowhere else in the frame"), True
    v = pol.split(":", 1)[1]
    spaced = " ".join(v)
    return (f"exactly ONE line is printed much larger than the rest and highlighted in a pale "
            f"colour band, reading the figure {v} — digit by digit that is {spaced} — and that "
            f"figure appears EXACTLY ONCE in the whole frame, with no second copy of it "
            f"anywhere"), True


# 🔴 "filmed straight on" đã bỏ: nó chọi FRAMING three-quarter. Cái cần khoá là máy KHÔNG
#    DI CHUYỂN, không phải góc.
CAM_BASE = ("the camera is locked off and does not move at any point, natural even lighting, "
            "no coloured light spilling onto skin or walls, no glow, no lens flare")

HUSB = ("an elderly Japanese man in his late sixties in a checked warm-red shirt under a grey "
        "cardigan")
WIFE = ("an elderly Japanese woman in her late sixties in a patterned brown knit cardigan over "
        "a striped top")
COUPLE = "an elderly Japanese couple in their late sixties, husband and wife"

_LOOK = ("photorealistic live-action video, natural skin texture, shallow depth of field, plain "
         "documentary look")
STYLE_PUB = f"{_LOOK}, Japanese public office interior"   # CROWD


def _cap(t: str) -> str:
    return t[:1].upper() + t[1:]


VIZ_REACT = [
    "one hand resting on the table edge, leaning in to look",
    "arms folded, studying the arrangement",
    "one eyebrow raised, head tilted",
    "a hand half-raised as if about to count",
    "leaning back slightly, eyes wide",
    "chin lowered, looking down at the objects",
]
VIZ = ("the objects have their own natural sheen under the daylight, nothing glows and "
       "nothing emits light")

# ⚠️ Ô càng nhiều thì mặt càng nhỏ: 3 ô ⇒ mỗi ô rộng 640px trên khung 1920 ⇒ mặt ~80px,
#    tệp 45+ không đọc được biểu cảm. Prompt của ô phải là CẬN NỬA NGƯỜI.
SPLIT_NOTE = ("framed as a medium close-up so the face fills a good part of the frame, "
              "because this shot will be placed in one half of a split screen")
PANEL_NOTE = ("framed as a tight medium close-up so the face and hands fill the frame, "
              "because this shot will be placed in one of three narrow side-by-side panels")

# 🔴 Đám đông là vùng Veo làm TỐT (không có thao tác tay với vật nhỏ) nhưng mặt sẽ méo ở hậu
#    cảnh ⇒ luôn để đám đông HƠI MỜ và đặt 1-2 người rõ nét ở tiền cảnh.
CROWD_NOTE = ("a large crowd of many elderly Japanese people fills the background, softly out of "
              "focus so individual faces are not distinct, with one or two people sharp in the "
              "foreground; the camera stays locked off")

# 🔴🔴 MÀN HÌNH LÀ **KHUNG RỖNG**, KHÔNG PHẢI ẢNH THÔNG TIN. Veo dựng cái bảng (kẻ ô, hàng —
#    đó là KẾT CẤU), Remotion dán số/chữ thật vào ô đó bằng font (`_scenes23.SCREEN_FILL`).
#    Hai câu bắt buộc để dán được: màn hình CHÍNH DIỆN (không thì méo phối cảnh) và KHÔNG DI
#    CHUYỂN (rect đứng yên suốt 8 giây ⇒ dán một lần là khớp cả clip).
SCREEN_BASE = ("the monitor is turned exactly square-on to the camera so its screen reads as a "
               "clean undistorted rectangle, and it fills between a third and a half of the "
               "frame. THE SCREEN SHOWS A FULL LEDGER TABLE, packed with data: more than twenty "
               "rows and five or six columns of small figures filling the screen right to its "
               "edges, banded row shading, a scroll bar down the side and a totals row at the "
               "bottom — a busy working spreadsheet, not a slide")
SCREEN_TAIL = ("Neither the monitor nor the camera shifts by even a pixel for the whole shot, "
               "so the screen rectangle stays exactly where it starts")
BOOK_BASE = ("the passbook is a small real Japanese bank passbook, held open in the hand with "
             "the page facing the camera and square-on to it. The open page is FULL: eighteen "
             "to twenty printed entry lines running from the top rule to the bottom of the "
             "page, each with a date, a small amount and a running balance in narrow columns — "
             "no blank lines left")
FORM_BASE = "the sheet is a realistic official Japanese form. " + DENSE

KINDS = ("VIZ", "GAUGE", "SCREEN", "META", "INFOG",
         "CROWD", "SPLIT", "PANEL", "HOLD", "DESK")

CAST_RE = re.compile(r"^(?:an|the)\s+(?:same\s+)?elderly\s+(?:man|woman|couple)\b", re.I)


def classify(body: str) -> str:
    """Suy KHUÔN từ mô tả cảnh. Khuôn khai TƯỜNG MINH bằng tiền tố `XXX:`, KHÔNG đoán."""
    for t in KINDS:
        if body.startswith(f"{t}:"):
            return t
    return "PERSON"


def cast_of(body: str):
    low = body.lower()
    if "elderly couple" in low:
        return COUPLE, "they", "their"
    if "elderly woman" in low:
        return WIFE, "she", "her"
    return HUSB, "he", "his"


# 🔴🔴 KHO **PHẢN ỨNG**, KHÔNG PHẢI KHO HÀNH ĐỘNG — nối thêm việc thứ hai là tự chọi câu
#    khoá "one action". Đo lô cũ video 22: **0/73 prompt có cảm xúc mạnh**, trong khi mẫu
#    ngách liên tục ôm đầu, há miệng, ngả bật ra sau.
REACT_FACE = [
    "{p} eyes widening and {p} mouth falling open",
    "leaning sharply back away from the table",
    "brows pulling together hard, jaw tightening",
    "{p} shoulders dropping and {p} head sinking forward",
    "{p} chin lifting as {p} lets out a long relieved breath",
    "{p} head snapping round toward the camera",
]
REACT_HAND = [
    "both hands rising to the sides of {p} head",
    "one hand pressing flat against {p} chest",
    "one palm coming down onto the table top",
    "one hand covering {p} mouth",
]
REACT_CALM = [
    "{p} eyelids lowering for a moment",
    "{p} shoulders settling as {p} breathes out slowly",
    "{p} head bowing a few degrees lower",
    "{p} chin lifting slowly, expression softening",
]
QUIET_CUE = ("palms together", "bows", "bow", "nod", "quietly", "altar", "chrysanthemum")
HAND_BUSY = ("hand", "hands", "palms", "arm", "arms", "finger",
             "holds", "holding", "hold", "taps", "points", "propping", "lifting")

# ⚠️ CỐ Ý KHÔNG có cỡ "chỉ bàn tay, mặt ngoài khung": `feedback_ai_video_hong_thao_tac_tay`
#    đo được 14/21 shot hands-only là HỎNG. Mọi cỡ dưới đây đều còn THÂN người trong khung.
FRAMING = [
    "medium shot from the waist up",
    "tight close-up from the shoulders up, the face large in frame",
    "wide shot showing the whole room, the person small on one side of it",
    "low angle from table height, the objects large in the foreground and the face and torso "
    "behind them",
    "three-quarter angle from the side, from the waist up",
    "a three-quarter view from slightly behind one shoulder, the face still visible in profile",
]


def prompt_for(body: str, idx: int = 0, scene: int = -1) -> str:
    kind = classify(body)
    who, subj, poss = cast_of(body)
    # 🔴 PHAI DOAN TRUOC ca REACTION lan dao cu tien, KHONG chi doc `body`. Chung duoc noi
    #    vao prompt SAU khi boi canh da chon, ma ca hai kho deu co cau nhac BAN
    #    ("one palm coming down onto the table top" - "lying on the table") => ban chi doc
    #    `body` van de lot 4/92 clip (gate 26 bat). Day la bay THU TU: quyet dinh som bang
    #    du lieu chua du.
    _probe = (body + " " + " ".join(REACT_HAND)) if kind == "PERSON" else body
    if kind in ("PERSON", "DESK", "SPLIT") and any(w in body.lower() for w in MONEY_CUE):
        _probe += " " + " ".join(MONEY_PROP)
    # 🔴 Dò CHỮ «table» trần, đừng liệt kê cụm: bản liệt kê («on the table», «at the table»…)
    #    để lọt đúng một clip VIZ viết «on A table» — mạo từ khác một chữ. Cụm-hoá một phép
    #    thử vốn là "cảnh này có bàn không" thì lần nào cũng thiếu một biến thể.
    _tbl = kind == "DESK" or bool(re.search(r"\btable\b", _probe))
    room, light, palette = setting(idx, _tbl)
    clear = CLEAR.format(s=gside(idx))
    style = f"{_LOOK}, {room}"
    nc, has_num = num_clause(scene)
    txt = TXT_NUM if has_num else TXT_NONE
    cam_n = f"{CAM_BASE}, {txt}"
    cam_p = (f"{CAM_BASE}, the person performs one single continuous action for the whole shot "
             f"and holds the posture above the rest of the time, {txt}")

    if kind == "VIZ":
        subj = body.split("VIZ:", 1)[1].strip()
        who_line = ""
        if idx % 3 == 0:
            who_line = (f" An elderly Japanese person is partly visible at the very edge of the "
                        f"frame, {VIZ_REACT[(idx // 3) % len(VIZ_REACT)]}.")
        return (f"{style}, a clean visual-explainer shot. SUBJECT: {subj}. The objects fill most "
                f"of the frame and are the clear focus, arranged so their relative size is "
                f"obvious at a glance. {_cap(VIZ)}.{who_line} FRAMING: wide shot, the whole "
                f"arrangement visible. {clear}. {light}. {palette}. {cam_n}")

    # 🔴 BRANCH NÀY TỪNG BỊ BỎ SÓT khi copy tool (bắt 2026-09-12, user: *"có những cảnh 3d
    #    nhé"*). `KINDS` vẫn liệt kê META/GAUGE/INFOG nên `classify()` trả về đúng, nhưng
    #    KHÔNG có nhánh xử lý ⇒ prompt rơi xuống nhánh PERSON và thành
    #    "SUBJECT: an elderly Japanese man … ACTION: two hourglasses stand…".
    #    Lỗi IM LẶNG: file vẫn xuất đủ dòng. Gate ② (câu one-action ở khuôn KHÔNG NGƯỜI) là
    #    lưới an toàn, nhưng lưới không thay được nhánh — cùng họ
    #    `feedback_gate_va_builder_phai_cung_ten`.
    if kind in ("GAUGE", "META", "INFOG"):
        subj = body.split(":", 1)[1].strip()
        note = {"GAUGE": GAUGE_NOTE, "META": META_NOTE, "INFOG": INFOG_NOTE}[kind]
        graphic = kind in ("META", "INFOG")     # GAUGE là panel 3D ĐẶT TRONG phòng thật
        st = (style if not graphic else
              "a polished 3D illustration for an explainer video" if kind == "META" else
              "a clean 2D infographic animation for an explainer video")
        lg = (LIGHT_3D if kind == "META" else LIGHT_2D) if graphic else light
        cl = COLOR_GRAPH if graphic else palette
        # khuôn đồ hoạ tự lấp khung nên KHÔNG chừa chỗ — Remotion không dán gì lên nó
        extra_clear = "" if graphic else f" {clear}."
        view = f" VIEW: {GFX_VIEW[idx % len(GFX_VIEW)]}." if graphic else ""
        return f"{st}. SUBJECT: {subj}. {_cap(note)}.{view}{extra_clear} {lg}. {cl}. {cam_n}"

    if kind == "SCREEN":
        subj = body.split(":", 1)[1].strip()
        note = SCREEN_BASE
        if nc:
            note += ". Out of all that, " + nc + "; every other figure is tiny dense texture"
        else:
            note += (". Every figure on it stays tiny and unreadable, pure dense texture — no "
                     "row is enlarged and no figure is highlighted")
        note += ". " + SCREEN_TAIL
        return (f"{style}. SUBJECT: {subj}. {_cap(note)}. {clear}. {light}. {palette}. {cam_n}")

    if kind == "CROWD":
        subj = body.split("CROWD:", 1)[1].strip()
        return (f"{STYLE_PUB}. SUBJECT: {subj}. {_cap(CROWD_NOTE)}. FRAMING: wide shot showing "
                f"the whole space. {clear}. {LIGHT_PUB}. {COLOR_PUB}. {cam_n}")

    # bỏ tiền tố khuôn, rồi thay cụm cast ĐẦU CÂU bằng đại từ — giữ nguyên thì prompt đọc
    # thành "SUBJECT: an elderly man … ACTION: an elderly man sits…" và Veo hiểu là HAI người.
    if kind in ("SPLIT", "PANEL", "HOLD", "DESK"):
        body = body.split(":", 1)[1].strip()
    body = CAST_RE.sub(subj, body, count=1)

    extra = ""
    if kind in ("SPLIT", "PANEL"):
        extra = " " + _cap(SPLIT_NOTE if kind == "SPLIT" else PANEL_NOTE) + "."
    if kind == "HOLD":
        paper = BOOK_BASE if "passbook" in body else FORM_BASE
        thing = "passbook" if "passbook" in body else "sheet"
        if nc:
            paper += (". Two of those lines aside, " + nc + "; the rest is tiny dense print, "
                      "and the Japanese headings stay small and softly out of focus")
        else:
            paper += (". No line on it is enlarged and no figure is highlighted; the Japanese "
                      "headings stay small and softly out of focus")
        # 🔴 Viết TÍCH CỰC: "never picked up" là câu cấm hoá gợi ý. Và vật phải Ở TƯ THẾ CUỐI
        #    ngay từ frame đầu — `feedback_ai_video_hong_thao_tac_tay`: 58/73 clip video 21
        #    hỏng đúng ở thao tác làm vật ĐỔI TRẠNG THÁI.
        extra = (f" {_cap(paper)}. The {thing} is already in the hand and fully open in the very "
                 f"first frame, and it stays in exactly that same position for the whole shot, "
                 f"completely still and rigid.")
    if kind == "DESK":
        extra = (" ON THE TABLE: a pocket calculator, an open spiral notebook, a stack of "
                 "receipts, brown envelopes, a teacup and a pile of paperwork, cluttered "
                 "naturally.")

    if kind in ("PERSON", "DESK", "SPLIT") and any(w in body.lower() for w in MONEY_CUE):
        extra += f" ALSO IN FRAME: {MONEY_PROP[idx % len(MONEY_PROP)]}."

    # 🔴 SPLIT/PANEL đã tự khai khung trong NOTE ⇒ nối thêm FRAMING là hai câu khung chọi nhau.
    #    HOLD chỉ lấy 2 cỡ gần: khung rộng thì tờ giấy bé mất.
    if kind in ("SPLIT", "PANEL"):
        frame = ""
    elif kind == "HOLD":
        frame = f" FRAMING: {FRAMING[idx % 2]}."
    else:
        frame = f" FRAMING: {FRAMING[idx % len(FRAMING)]}."

    if any(w in body.lower() for w in QUIET_CUE):
        pool = REACT_CALM
    elif any(re.search(r"\b%s\b" % w, body) for w in HAND_BUSY):
        pool = REACT_FACE
    else:
        pool = REACT_FACE + REACT_HAND
    b2 = (pool[idx % len(pool)].format(s=subj, p=poss)
          if kind == "PERSON" and who is not COUPLE else "")
    b2 = f" REACTION: {b2}." if b2 else ""
    pr = poss.capitalize()
    mouth = ("their mouths are closed or only slightly parted" if who is COUPLE
             else "the mouth is closed or only slightly parted")
    quiet = "" if ("mouth" in b2 or "palms together" in body) else \
            f" {_cap(pr + ' hands stay apart from each other throughout, and ' + mouth)}."
    return (f"{style}. SUBJECT: {who}. ACTION: {body}.{b2}{extra}{frame} "
            f"The face and upper body are clearly visible at all times.{quiet} "
            f"{clear}. {light}. {palette}. {cam_p}")


def main():
    from plan23 import build
    rows = build()
    items = []
    for r in rows:
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        for k in range(r["nshot"]):
            suf = f"_{k+1}" if r["nshot"] > 1 else ""
            items.append(dict(stem=f"c23_{r['i']:02d}{suf}", scene=r["i"],
                              kind=classify(r["body"]), body=r["body"],
                              prompt=" ".join(
                                  prompt_for(r["body"], len(items), r["i"]).split())))

    io.open(os.path.join(OUT, "flow23_FULL_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(x["prompt"] for x in items) + "\n")
    io.open(os.path.join(OUT, "flow23_FULL_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1:>3} -> {x['stem']}.mp4   [scene {x['scene']:>3} · {x['kind']:<6} "
                  f"· chua trong ben {gside(i)}]" for i, x in enumerate(items)) + "\n")

    # ── LÔ 1: 12 prompt phủ đủ mọi khuôn, ưu tiên scene ĐẦU bài ─────────────
    lot1, seen = [], {}
    for x in items:
        c = seen.get(x["kind"], 0)
        if c < 3:
            lot1.append(x); seen[x["kind"]] = c + 1
        if len(lot1) >= 12:
            break
    rest = [x for x in items if x not in lot1]
    half = len(rest) // 2
    for name, grp in (("LOT1", lot1), ("LOT2", rest[:half]), ("LOT3", rest[half:])):
        io.open(os.path.join(OUT, f"flow23_{name}.txt"), "w", encoding="utf-8").write(
            "\n".join(x["prompt"] for x in grp) + "\n")
        io.open(os.path.join(OUT, f"flow23_{name}_TENFILE.txt"), "w", encoding="utf-8").write(
            "\n".join(f"dong {i+1:>3} -> {x['stem']}.mp4   [scene {x['scene']:>3} · {x['kind']}]"
                      for i, x in enumerate(grp)) + "\n")

    # ── bản NGƯỜI ĐỌC: xem lô prompt mà không phải mở file 140KB một dòng ────
    # `feedback_luu_prompt_vao_file`: in ra chat là để đọc, FILE mới là bản dùng. Ba file
    # chở ba việc khác nhau, đừng gộp: FLOW = bơm vào extension · TENFILE = dòng ↔ tên file
    # đích (sai là `ingest` đổi tên mù) · PROMPTS.md = bản duyệt bằng mắt.
    md = ["# flow23 — lô prompt Veo video 23 (年金請求書が届かない)", "",
          f"**{len(items)} clip** · 8,000s/clip @24fps · khuôn: "
          + " · ".join(f"{k} {v}" for k, v in sorted(collections.Counter(
              x['kind'] for x in items).items())), "",
          "Khối dùng chung (ánh sáng/màu/máy quay/guard chữ) do `flow23_full.py` dán tự động —",
          "đừng sửa trong file FLOW, sửa ở tool rồi xuất lại.", "",
          "| dòng | file đích | scene | khuôn | telop | số trên hình | cảnh |",
          "|---|---|---|---|---|---|---|"]
    tel = {r["i"]: r["telop"] for r in rows}
    for i, x in enumerate(items, 1):
        pol = NUM.get(x["scene"], "—")
        body = x["body"].split(":", 1)[1].strip() if ":" in x["body"].split(",")[0] else x["body"]
        md.append(f"| {i} | `{x['stem']}.mp4` | {x['scene']} | {x['kind']} | "
                  f"{tel[x['scene']].replace(chr(10), ' / ')} | {pol} | {body[:96]} |")
    io.open(os.path.join(OUT, "flow23_PROMPTS.md"), "w", encoding="utf-8").write(
        "\n".join(md) + "\n")

    c = collections.Counter(x["kind"] for x in items)
    nnum = sum(1 for x in items if NUM.get(x["scene"]))
    print(f"\n⭐ {len(items)} prompt -> flow23_FULL_FLOW.txt")
    print(f"   khuôn: {dict(c)}")
    print(f"   khe CÓ số to: {nnum}/{len(items)} (còn lại guard TXT_NONE)")
    print(f"   LOT1 {len(lot1)} (gen thử trước) · LOT2 {half} · LOT3 {len(rest)-half}")
    print(f"   dài prompt: {min(len(x['prompt']) for x in items)}–"
          f"{max(len(x['prompt']) for x in items)} ký")


if __name__ == "__main__":
    main()
