# -*- coding: utf-8 -*-
"""
flow22_full.py — xuất TOÀN BỘ prompt Veo cho video 22, từ chính bảng `_scenes22.py`.

Không viết prompt tay: khối ánh sáng / màu / chống-lỗi phải giống hệt ở 73 prompt, và cái
rơi mất khi gõ tay bao giờ cũng là câu chống lỗi.

Xuất 3 file + 3 lô:
  flow22_FULL_FLOW.txt      — cả 73 prompt, mỗi prompt 1 dòng
  flow22_FULL_TENFILE.txt   — dòng ↔ tên file đích ↔ scene ↔ khuôn
  flow22_LOT1.txt           — 12 prompt ĐẦU đủ 5 khuôn, gen thử trước
  (LOT2/LOT3 chia phần còn lại)

🔴 VÌ SAO CÓ LÔ 1: lô 16 clip trước lộ ra hai lỗi cả-lô (chữ nát 0/6 · glow tô đỏ da tay).
   Chạy thẳng 73 cái là hỏng 73 cái. Lô 1 cố ý gồm đủ 5 khuôn để lỗi khuôn nào cũng lộ.

🔴 CHỮ: khuôn HOLD-FORM ở đây **để giấy TRƠN** — Veo dựng chữ Nhật nát (đo 0/6 lô trước).
   Chữ và số do lớp telop + thẻ `papercut-stat` của Remotion vẽ, luôn sắc.
   Nền biểu mẫu (bảng kẻ ô, checkbox, ô mã bưu điện, chữ li ti mờ) VẪN yêu cầu — đó là thứ
   làm tờ giấy trông thật, và nó cố ý không cần đọc được.
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
from plan22 import build  # noqa: E402

OUT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"

# ── KHỐI CHUNG ───────────────────────────────────────────────────────────────
# Đo được: bản mẫu ngách sáng 173 / lô clip cũ 128 ⇒ bỏ trống phần ánh sáng thì Veo trả
# nội thất tối trầm. Hai vế cuối chống cái user kêu ở vòng trước: cháy sáng.
# 🔴 BA BỘ ÁNH SÁNG/MÀU THEO NHÓM KHUÔN. Bản trước dùng MỘT bộ cho cả 73 prompt, và bộ
#    đó tả một PHÒNG KHÁCH ⇒ 10 cảnh CROWD (văn phòng bảo hiểm, bưu điện, hội trường) và
#    11 cảnh đồ hoạ 2D/3D đều bị nhét "warm morning sunlight through a large window with
#    sheer curtains" + "warm wood furniture, patterned fabric cushions". Với INFOG thì câu
#    đó vô nghĩa hoàn toàn — nó kéo Veo vẽ phòng khách vào giữa một sơ đồ phẳng.
# 🔴🔴 ĐÂY LÀ CHỖ HỎNG NẶNG NHẤT CỦA LÔ ĐẦU (user 2026-09-09: *"vẫn chỉ có mấy ông già
#    bà già ngồi 1 chỗ, không sinh động như ảnh trong video"*).
#    Đo bằng máy trên 73 prompt cũ: **52 prompt chứa nguyên văn "sheer curtains"** ⇒ 52 clip
#    CÙNG MỘT CĂN PHÒNG — cùng cửa sổ rèm voan, cùng kệ sách, cùng chậu cây, cùng ấm trà.
#    Không phải Veo kém: nó trả về đúng thứ được yêu cầu.
# ⇒ PHÒNG + ÁNH SÁNG + PALETTE phải đi THÀNH BỘ và xoay theo `idx`. ⚠️ Tách ba thứ đó ra rồi
#   xoay riêng là sinh tổ hợp vô lý (bếp + rèm voan phòng khách + tatami vàng rơm).
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


def setting(idx: int):
    return SETTINGS[idx % len(SETTINGS)]


# ⭐ PHƯƠNG ÁN LAI (user chốt 2026-09-09): Veo gen NGƯỜI photoreal, còn tháp xu · mũi tên đỏ ·
#    bảng số · dấu ✗ do **Remotion vẽ đè** bằng lớp `fx`. ⇒ mỗi khung PHẢI CHỪA MỘT BÊN TRỐNG,
#    nếu không đồ hoạ dán chồng lên mặt người. Bên chừa xoay đều và ghi vào TENFILE để builder
#    biết đặt đồ hoạ ở đâu — đừng để builder tự đoán.
CLEAR = ("COMPOSITION: keep the {s} third of the frame visually empty and simple — plain wall, "
         "plain floor or open space with nothing important in it — and put the subject in the "
         "other two thirds")


def gside(idx: int) -> str:
    return "right" if idx % 2 == 0 else "left"


# Đạo cụ TIỀN THẬT — mẫu khung nào cũng có tiền, lô cũ có **0/73**. Chỉ gắn khi cảnh vốn nói
# về tiền/phong bì/sổ, đừng rải bừa vào cảnh nói về tờ khai.
MONEY_PROP = [
    "a banded bundle of ten-thousand-yen notes lying on the table",
    "three neat stacks of coins of clearly different heights on the table",
    "an opened envelope with banknotes showing at its mouth",
    "a bank passbook lying open next to a small heap of coins",
]
MONEY_CUE = ("envelope", "passbook", "number card", "bank", "money", "coins", "transaction")

LIGHT_PUB_OLD_ANCHOR = None
LIGHT_PUB = ("a bright public interior lit evenly by ceiling lights and by daylight from a tall "
             "window wall, soft diffused light, high key but not blown out")
LIGHT_2D = ("evenly lit flat artwork on a light neutral ground, soft even shading, high key "
            "but not blown out")
# ⚠️ META là ẩn dụ VẬT THỂ 3D — gọi nó là "flat artwork" là chọi chính dòng style của nó.
LIGHT_3D = ("an evenly lit rendered scene on a light neutral ground, soft directional key "
            "light and gentle ambient fill, high key but not blown out")

# ⚠️ ĐÃ BỎ `COLOR_HOME`/`HOME_PROP`: palette giờ nằm trong chính bộ `SETTINGS` (mục 3 của
#    mỗi tuple) — tách ra thì lại rơi vào đúng bẫy "một palette cho mọi phòng".
COLOR_PUB = ("rich natural colours, pale wood counters, soft blue and grey office tones, a green "
             "plant in one corner, not desaturated")
COLOR_GRAPH = ("a warm cream ground with navy, soft blue, amber and muted green accents, "
               "not desaturated")

# 🔴🔴 GUARD CHỮ PHẢI PHÂN CẤP — LẦN THỨ BA CỦA CÙNG MỘT LỖI.
#    Bản trước ghi thẳng "no text anywhere, no letters, no numbers" vào cả 73 prompt, và nó
#    HUỶ chính nội dung mà mô tả yêu cầu: khối FORM xin "field labels, rows of tiny print"
#    (3 prompt HOLD) · 18 prompt SCREEN xin lịch/bảng/thẻ số/inbox · CROWD xin "electronic
#    number board" · GAUGE xin "tick marks". Cái mình thật sự cần chặn là chữ TO ĐỌC ĐƯỢC
#    (vì Veo viết chữ Nhật nát) chứ không phải mọi nét mực.
# 🔴🔴 GUARD CHỮ — ĐẢO CHIỀU 2026-09-09 (user: *"giấy phải có số liệu chứ, màn hình máy
#    tính cũng phải có số liệu chứ"*). Bản trước bắt "không đọc được chữ nào" ⇒ màn hình và
#    tờ giấy thành mảng trắng vô nghĩa; người xem nhìn vào không rút ra được gì.
# ⭐ Điều tao đã bỏ sót: phép đo "Veo gen chữ Nhật nát 0/6" là đo **KANJI**. `media-library.md`
#   §2.9 ghi sẵn *"chữ số Latin gen ổn định hơn kanji nhiều"* — mà bảng tiền của Nhật (sổ
#   ngân hàng, thông báo chuyển khoản, tờ khai) vốn ghi số bằng **chữ số Ả Rập**.
# ⇒ Guard phân theo LOẠI KÝ TỰ, không phân theo "đọc được hay không":
#   · chữ số Ả Rập → ĐƯỢC, và phải TO ĐỦ ĐỌC (đó là thứ chở thông tin)
#   · chữ Nhật     → chỉ làm nền, nhỏ và mờ (chỗ Veo hỏng)
#   · phụ đề/watermark → cấm (Remotion vẽ phụ đề)
TXT = ("the only characters meant to be read in the frame are Arabic numerals — yen figures and "
       "dates — printed large and crisp in a clean sans-serif; any Japanese writing on signs, "
       "labels, book spines or form headings stays small and softly out of focus; no captions, "
       "no subtitles, no watermark, no logo")

# ⚖️ YMYL: số Veo vẽ ra là ĐẠO CỤ, có thể sai một chữ số. Hai lớp phòng:
#   ① chỉ đưa vào prompt đúng những con số CÓ THẬT trong bài (180,000 · 360,000 · 4/15 · 6/15)
#      ⇒ Veo vẽ đúng thì cũng là số đúng, không bịa thêm số mới.
#   ② con số CHỐT của mỗi scene vẫn do Remotion dán đè bằng font ⇒ luôn sắc và luôn đúng.
FIG = ("the two highlighted lines read 180,000 and 360,000 with the dates 4/15 and 6/15")

# 🔴🔴 MẬT ĐỘ — user nhắc LẦN THỨ HAI (lần đầu: *"mỗi trang giấy trắng viết 1 dòng chữ trông
#    điêu vãi"*; lần này: *"cả 1 trang giấy trắng và cả 1 cái màn hình, hiển thị được 1, 2
#    dòng"*). Vòng 12 tao viết "four or five rows … nothing else" ⇒ dựng lại y nguyên lỗi cũ.
# ⇒ Giấy tờ tiền của Nhật KÍN ĐẶC. Ba TẦNG chữ số, và phải nói rõ cả ba:
#   ① nền: hàng chục dòng, hàng trăm con số nhỏ chạy dọc các cột — ĐÂY LÀ KẾT CẤU, cố ý
#      nhỏ tới mức không đọc rời từng số được (nên nó không thể thành "số sai" trên màn hình)
#   ② nhấn: ĐÚNG HAI dòng in to và tô sáng — đây mới là thông tin, và là số thật của bài
#   ③ nhãn tiếng Nhật: nhỏ và mờ (vùng Veo hỏng)
DENSE = ("the page is DENSELY filled the way a real financial document is — more than twenty "
         "ruled lines running to the very bottom, several narrow columns, hundreds of small "
         "printed figures marching down those columns, tick boxes, a stamped seal and a totals "
         "line at the foot, with almost no empty white space left anywhere. Those background "
         "figures are deliberately tiny — dense grey texture rather than anything readable")

# 🔴 "filmed straight on" đã bỏ: nó chọi FRAMING[3] ("three-quarter angle from the side"),
#    tức 1/4 số prompt PERSON tự mâu thuẫn. Cái cần khoá là máy KHÔNG DI CHUYỂN, không phải góc.
CAM_BASE = ("the camera is locked off and does not move at any point, natural even lighting, "
            "no coloured light spilling onto skin or walls, no glow, no lens flare")
# 🔴 Mệnh đề "the person does exactly one action" CHỈ gắn cho khuôn CÓ NGƯỜI. Dán nó vào
#    INFOG/META/GAUGE-không-người là đang GỢI Ý Veo thêm một người vào khung — scene 42 nói
#    rõ "no people in frame" rồi câu sau lại nhắc "the person".
CAM_P = (f"{CAM_BASE}, the person performs one single continuous action for the whole shot "
         f"and holds the posture above the rest of the time, {TXT}")
CAM_N = f"{CAM_BASE}, {TXT}"

HUSB = ("an elderly Japanese man in his late sixties in a checked warm-red shirt under a grey "
        "cardigan")
WIFE = ("an elderly Japanese woman in her late sixties in a patterned brown knit cardigan over "
        "a striped top")
COUPLE = "an elderly Japanese couple in their late sixties, husband and wife"

# Nền giấy — cố ý KHÔNG đòi đọc được (mắt chỉ đọc telop, và chữ Veo gen thì nát).
# 🔴 HAI khối, chọn theo VẬT. Bản trước chỉ có FORM (tờ A4 có ô mã bưu điện) và nó bị
#    dán cả vào 2 scene cầm SỔ NGÂN HÀNG ⇒ prompt vừa nói "bank passbook" vừa tả một
#    tờ đơn hành chính. Veo sẽ chọn một trong hai, và mình không điều khiển được cái nào.
FORM = ("the sheet is a realistic official Japanese form. " + DENSE + ". The Japanese field "
        "labels stay small and softly out of focus, BUT two amount cells are filled in with LARGE "
        "CRISP ARABIC NUMERALS the camera reads clearly: " + FIG)

_LOOK = ("photorealistic live-action video, natural skin texture, shallow depth of field, plain "
         "documentary look")
# 🔴 BỐI CẢNH PHẢI THEO KHUÔN. Bản trước nhét "Japanese home interior" vào MỌI prompt,
#    kể cả 10 cảnh CROWD ở văn phòng bảo hiểm / hội trường / bưu điện ⇒ Veo trộn đồ đạc
#    nhà ở vào quầy công sở. Ba bối cảnh, gán theo `classify()`, không gán một cỡ cho tất.
BOOK = ("the passbook is a small real Japanese bank passbook, held open in the hand with the "
        "page facing the camera and square-on to it. The open page is FULL: eighteen to twenty "
        "printed entry lines running from the top rule to the bottom of the page, each with a "
        "date, a small amount and a running balance in narrow columns — no blank lines left. Two "
        "of those lines are printed noticeably LARGER and read clearly in CRISP ARABIC NUMERALS: "
        "" + FIG + "; the rest are tiny dense print, and the Japanese column headings stay small "
        "and softly out of focus")

# 🔴 KHÔNG còn khoá "Japanese home interior" vào đây nữa — bối cảnh lấy từ `SETTINGS`
#    theo `idx`. Giữ lại đúng một biến cho CROWD, vì mô tả CROWD tự nói nơi chốn rồi.
STYLE_PUB = f"{_LOOK}, Japanese public office interior"   # CROWD


def _cap(t: str) -> str:
    """Viết hoa chữ đầu khối note — nó đứng ngay sau dấu chấm trong prompt."""
    return t[:1].upper() + t[1:]


# ── ⑥ MONEY-VIZ: TRỰC QUAN HOÁ CON SỐ BẰNG VẬT (user chốt 2026-09-07, kèm 4 ảnh mẫu) ──
# 🔴 KHUÔN CÒN THIẾU, VÀ LÀ KHUÔN MẠNH NHẤT CỦA NGÁCH. Bản trước của tao có 5 khuôn nhưng
#    tất cả đều là "người làm gì đó" — không khuôn nào BIẾN CON SỐ THÀNH HÌNH. Ảnh mẫu:
#    cột xu vàng xếp theo 1月→12月 cao dần · chồng tiền giấy chất đống cạnh dãy lịch
#    1985→2003 · hồ sơ mở ra toả sáng vàng. Đó là cách ngách này bán con số.
# 🔴 KHÔNG cho Veo viết số lên hình: cột xu / chồng tiền / dãy lịch là VẬT, Veo dựng tốt;
#    còn 年間67,440円 trong ảnh mẫu là chữ AI — mình để telop + thẻ `papercut-stat` của
#    Remotion vẽ đè, sắc tuyệt đối. Vật lo ĐỘ LỚN, chữ lo CON SỐ CHÍNH XÁC.
# ⚠️ Glow VÀNG ở đây khác vụ tô đỏ da tay (clip task_005): nó phát ra từ ĐỐNG VẬT và hắt
#    lên vật, không phải "ánh sáng màu tô lên người". Vẫn ghi rõ để model không tô lên mặt.
# 🔴 KHÔNG xin lấp lánh/ánh vàng trong prompt nữa (user chốt 2026-09-07: giữ `no glow,
#    no lens flare`). Lý do nhất quán với cả pipeline: **Veo lo NGƯỜI + VẬT, Remotion lo
#    HIỆU ỨNG**. Nhờ Veo làm ánh sáng thì nó tô màu lên da (đã đo ở clip task_005: "red
#    glow onto the hands" ⇒ bàn tay như bị sơn). Lấp lánh vàng giờ do fx `sparkle`/`coins`
#    của Remotion vẽ đè — đúng chỗ, tắt/bật được, không phải gen lại clip.
# ⇒ Prompt chỉ yêu cầu VẬT THẬT xếp cho ĐỌC ĐƯỢC ĐỘ LỚN. Đó là phần Veo làm tốt.
# 🔴 Sáu phản ứng KHÁC NHAU cho scene VIZ có người. Trần ngầm: mỗi cái xuất hiện ≤2 lần
#    trong cả video (12 VIZ ÷ 3 = 4 clip có người ⇒ mỗi phản ứng ≤1 lần thật).
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


# ── ⑦⑧ SPLIT + PANEL3 — hai khuôn GHÉP Ô (user chốt 2026-09-08, ảnh mẫu #9/#10) ──────
# Ảnh #9: BEFORE/AFTER hai nửa khung, mỗi nửa một nhãn (対象外 / 対象).
# Ảnh #10: BA Ô ngang, mỗi ô một thất bại, mỗi ô một nhãn cam.
#
# ⭐ ĐÂY LÀ CHỖ MÌNH HƠN MẪU, và cách làm khác hẳn: mẫu ghép ô **bên trong một ảnh tĩnh**
#    (nên mỗi ô đứng im, và nhãn là chữ AI ⇒ 3/3 nhãn ở ảnh #10 đều NÁT:
#    「通知知を搭える」「永外不備を見える」). Mình gen **từng ô là một CLIP RIÊNG** rồi
#    Remotion xếp cạnh nhau bằng `layout.x/y/w/h` + vẽ nhãn bằng font.
#    ⇒ mỗi ô CHUYỂN ĐỘNG THẬT, nhãn SẮC TUYỆT ĐỐI, và sửa nhãn không phải gen lại clip.
# 🔴 Vì thế KHÔNG có prompt riêng cho hai khuôn này — chúng là **cách LẮP ở builder**,
#    dùng lại chính các clip PERSON/DESK đã có. Ô nào cần cảnh riêng thì khai như một
#    scene `art` bình thường; builder quyết định nó nằm nửa trái hay ô giữa.
# ⚠️ Ô càng nhiều thì mặt càng nhỏ: 3 ô ⇒ mỗi ô rộng 640px trên khung 1920. Prompt của ô
#    phải là **cận nửa người**, không phải toàn cảnh — nếu không mặt chỉ còn ~80px và tệp
#    45+ không đọc được biểu cảm.
SPLIT_NOTE = ("framed as a medium close-up so the face fills a good part of the frame, "
              "because this shot will be placed in one half of a split screen")
PANEL_NOTE = ("framed as a tight medium close-up so the face and hands fill the frame, "
              "because this shot will be placed in one of three narrow side-by-side panels")


# ── ⑨ CROWD — ĐÁM ĐÔNG / QUY MÔ (user chốt 2026-09-08: "cứ lặp đi lặp lại ông bà già
#    nhìn chán đời quá"). Đếm lại chính video mẫu: khung 90s là **hàng trăm người trong
#    hội trường** đứng trước một biểu đồ khổng lồ; mẫu rất ÍT khung "một cụ già ngồi nói".
#    Khuôn này chở QUY MÔ ("729万人が受給") — thứ một người ngồi bàn không tải nổi.
# 🔴 Đám đông là vùng Veo làm TỐT (không có thao tác tay với vật nhỏ) nhưng mặt sẽ méo ở
#    hậu cảnh ⇒ luôn để đám đông HƠI MỜ và đặt 1-2 người rõ nét ở tiền cảnh.
CROWD_NOTE = ("a large crowd of many elderly Japanese people fills the background, softly out of "
              "focus so individual faces are not distinct, with one or two people sharp in the "
              "foreground; the camera stays locked off")


# ══ BỐN KHUÔN BÓC TỪ 85 CẢNH CỦA VIDEO MẪU (2026-09-08) ══════════════════════
# Cắt toàn bộ video mẫu ra 85 frame rồi phân loại. Phát hiện đắt nhất: **mẫu TRỘN HAI
# STYLE** — photoreal cho người thật, ILLUSTRATION 3D cho phần siêu thực + đồ hoạ
# (khung 029-034: gia đình vẽ + khiên vàng chặn chữ 税 bay như phi tiêu; 022: infographic
# 3 loại; 063: đồng hồ 24h).
# 🔴 Điều này KHÔNG phá luật ⛔BỎ ANIME của kênh — nó GIẢI THÍCH luật đó. Luật sinh ra vì
#    "25/83 shot siêu thực với người thật thành quái dị"; mẫu tránh đúng cái đó bằng cách
#    **đổi style cho riêng phần siêu thực**, thay vì bỏ phần siêu thực đi. Người vẫn
#    photoreal, chỉ khối ẩn dụ/đồ hoạ mới là illustration.
GAUGE_NOTE = ("a large semicircular gauge dial with a needle, a green zone on the left and an "
              "amber zone on the right, tick marks around the arc, rendered as a clean 3D panel "
              "standing in the room; the needle sweeps slowly from the left across the arc and "
              "settles, the rest of the panel stays perfectly still")
# 🔴 SCREEN là khuôn LỚN NHẤT của mẫu (26% thời lượng — đo bằng 101 mẫu đều 10s), lớn hơn
#    cả PERSON. Nửa sau video mẫu (510-670s) gần như toàn SCREEN. Và đây là cách mẫu đưa
#    SỐ vào khung mà không phải nhờ chữ AI to: số nằm TRONG giao diện trên màn hình, nát
#    cũng ít lộ, còn telop thì do tool vẽ.
# 📐 Bóc từ 20+ khung mẫu: màn hình luôn ĐỦ LỚN (chiếm 1/3–1/2 khung), đặt CẠNH người chứ
#    không phải sau lưng, và nội dung luôn là một trong bốn dạng: bảng hai cột · danh mục
#    có ô tích · biểu đồ thanh ngang · thẻ số. Người thì CHỈ vào màn hình hoặc nhìn vào nó.
# 🔴🔴 MÀN HÌNH LÀ **KHUNG RỖNG**, KHÔNG PHẢI ẢNH THÔNG TIN (user chốt 2026-09-09).
#    Bản trước xin "giao diện sạch, khối pastel" rồi khối `TXT` lại cấm đọc được chữ ⇒ Veo
#    trả về mấy mảng màu vô nghĩa; người xem nhìn màn hình mà không rút ra được gì.
#    Đây KHÔNG chữa được bằng cách xin Veo viết chữ — nó gen chữ Nhật nát 0/6 (đo lô trước).
# ⇒ Theo đúng PHƯƠNG ÁN LAI: Veo dựng **cái bảng rỗng** (kẻ ô, hàng trống — đó là KẾT CẤU,
#   không phải THÔNG TIN), Remotion dán số/chữ thật vào ô đó bằng font.
# 🔴 Hai câu bắt buộc để dán được: màn hình phải **CHÍNH DIỆN** (không thì hình chữ nhật bị
#   méo phối cảnh, dán vào lệch) và **KHÔNG DI CHUYỂN** (camera đã khoá, nên rect đứng yên
#   suốt 8 giây ⇒ dán một lần là khớp cả clip).
SCREEN_NOTE = ("the monitor is turned exactly square-on to the camera so its screen reads as a "
               "clean undistorted rectangle, and it fills between a third and a half of the "
               "frame. THE SCREEN SHOWS A FULL LEDGER TABLE, packed with data: more than twenty "
               "rows and five or six columns of small figures filling the screen right to its "
               "edges, banded row shading, a scroll bar down the side and a totals row at the "
               "bottom — a busy working spreadsheet, not a slide. Out of all that, exactly two "
               "rows are printed MUCH LARGER and highlighted in a pale colour band, in CRISP "
               "ARABIC NUMERALS the camera reads easily: " + FIG + "; every other figure is tiny "
               "dense texture. Neither the monitor nor the camera shifts by even a pixel for the "
               "whole shot, so the screen rectangle stays exactly where it starts")
# 🔴 Bỏ "gently glowing edges" — chọi `no glow` ở khối máy quay (lần thứ 3 của lỗi này).
META_NOTE = ("rendered as a polished 3D illustration, not a photograph: smooth stylised shapes, "
             "soft clean shading, clean crisp silhouettes; the objects drift and orbit slowly")


# ⑩ INFOG — INFOGRAPHIC THUẦN, không người thật (mẫu: 009 lịch+biểu đồ, 022 ba loại
#    icon tròn, 063 đồng hồ 24h). Chiếm 5% mẫu và tao bỏ sót hẳn khuôn này.
#    Khác META: META là ẩn dụ VẬT THỂ 3D (khiên, đồng hồ cát); INFOG là SƠ ĐỒ có cấu trúc
#    (mốc thời gian, nhóm phân loại, mặt đồng hồ) — nó tải QUAN HỆ, không tải cảm xúc.
# 📐 Bóc từ mẫu (khung 510-620s, 160s, 630s): panel phẳng chiếm gần trọn khung, icon tròn
#    pastel, người vẽ theo lối minh hoạ đứng nhỏ ở mép, mũi tên/đường mảnh nối các khối.
#    Khác META: META là VẬT 3D ẩn dụ (khiên, đồng hồ cát); INFOG là SƠ ĐỒ có cấu trúc.
INFOG_NOTE = ("a clean flat infographic panel fills almost the whole frame: rounded boxes in soft "
              "pastel colours, simple line icons, thin connector arrows between the blocks, and "
              "one or two small illustrated figures standing at the edge; the blocks fade in one "
              "after another from left to right and then hold still, the camera never moves")


# khuôn có tiền tố — thứ tự không quan trọng vì tiền tố là duy nhất
# ⚠️ ĐÃ BỎ "FLAT" và "MACRO": 0/91 scene dùng tới. Hằng số chết thì người sau tinh chỉnh
#    nó, render, thấy không có gì đổi, rồi đi tìm lỗi ở chỗ khác.
# ⚠️ GAUGE · META · INFOG vẫn nhận diện được, nhưng 11 scene dùng chúng đã chuyển
#    sang kind `gfx` ở `_scenes22.py` ⇒ Remotion vẽ, KHÔNG còn prompt Veo nào.
#    Giữ lại để ai thêm scene mới vẫn phân loại đúng và gate vẫn gác được.
KINDS = ("VIZ", "GAUGE", "SCREEN", "META", "INFOG",
         "CROWD", "SPLIT", "PANEL", "HOLD", "DESK")

# cụm chỉ cast ở ĐẦU mô tả — bị thay bằng đại từ để ACTION không lặp lại SUBJECT
CAST_RE = re.compile(r"^(?:an|the)\s+(?:same\s+)?elderly\s+(?:man|woman|couple)\b", re.I)


def classify(body: str) -> str:
    """Suy KHUÔN từ mô tả cảnh — để in ra bảng và để gate xen kẽ khuôn.

    🔴 Khuôn khai TƯỜNG MINH bằng tiền tố `XXX:` ở đầu mô tả, KHÔNG đoán bằng từ khoá.
       Bản trước đoán theo tiếng Việt («giơ»+«giấy» → HOLD, «bàn đầy» → DESK) nên lúc dịch
       mô tả sang tiếng Anh thì hai khuôn đó **biến mất im lặng**: 8 scene rơi hết về
       PERSON, prompt vẫn xuất bình thường, không gate nào báo. Đúng họ với bài học
       `feedback_gate_va_builder_phai_cung_ten` — chỉ khác là ở đây hai bên lệch NGÔN NGỮ.
    """
    for t in KINDS:
        if body.startswith(f"{t}:"):
            return t
    return "PERSON"


def cast_of(body: str):
    """(mô tả cast, đại từ chủ ngữ, sở hữu) — suy từ chính cụm tiếng Anh trong mô tả.

    🔴 Bản trước dò «ông»/«bà» tiếng Việt. Dịch xong thì mọi scene rơi về nhánh cuối và
       **73/73 prompt thành "an elderly Japanese couple"**, kể cả scene chỉ có một người.
    """
    low = body.lower()
    if "elderly couple" in low:
        return COUPLE, "they", "their"
    if "elderly woman" in low:
        return WIFE, "she", "her"
    return HUSB, "he", "his"


# 🔴 Xoay vòng CỠ CẢNH cho nhóm PERSON. Không có nó thì 54/73 clip là "một cụ già ngồi
#    bàn nói vào ống kính" ở đúng một cỡ — nhìn 3 clip là biết cả video. Bốn cỡ này chỉ
#    đổi KHOẢNG CÁCH MÁY, không đổi hành động, nên không đụng vùng Veo hỏng.
# 🔴 KHO ĐỘNG TÁC cho nhóm PERSON. Không có nó thì mô tả mỏng ("nói vào ống kính") để
#    Veo tự điền, và mặc định của nó LUÔN là chắp tay + mỉm cười — user đếm ra 4/16 frame.
#    Mỗi động tác gán xoay vòng, gate ở `plan22.py` chặn ≤3 lần/động tác trong cả video.
# ⚠️ Toàn bộ đều thuộc nhóm AN TOÀN của Veo: không cầm-nhặt-mở vật nhỏ (58/73 clip video 21
#    hỏng đúng ở đó), chỉ chuyển động THÂN + ĐẦU + tay không cầm gì.
# 🔴 ĐẠI TỪ LÀ KHUÔN `{p}`, KHÔNG viết cứng he/she. Bản trước viết cứng nên prompt ra
#    "SUBJECT: an elderly Japanese **woman** … **he** shifts his weight" — sai giới tính ở
#    khoảng một nửa số clip PERSON.
# 🔴🔴 ĐÂY LÀ KHO **TƯ THẾ**, KHÔNG PHẢI KHO HÀNH ĐỘNG. Bản trước là hành động và được nối
#    bằng "At the same time …" ⇒ prompt vừa mô tả HAI việc vừa có câu khoá "the person does
#    exactly one action for the whole shot" — chọi thẳng nhau ở 15 prompt PERSON, và Veo
#    xử lý mâu thuẫn kiểu đó bằng cách bỏ bớt một vế, mình không biết vế nào.
#    Tư thế thì mô tả NGƯỜI ĐANG GIỮ MÌNH THẾ NÀO — nó vẫn lấp đúng chỗ mà Veo hay tự điền
#    bằng "chắp tay + mỉm cười", mà không đẻ ra sự kiện thứ hai trong 8 giây.
# 🔴 HAI KHO, và phải chọn đúng kho theo ACTION. Tư thế nói về TAY chỉ dùng được khi ACTION
#    chưa quy định tay đang ở đâu. Bản một-kho ra prompt kiểu: ACTION "một phong bì trong
#    MỖI tay, đẩy tay trái ra kéo tay phải về" + POSTURE "một tay chống lên má" — tay không
#    làm hai việc cùng lúc, và Veo lại phải tự chọn bỏ vế nào.
# 🔴 ĐỔI TỪ "TƯ THẾ" SANG "PHẢN ỨNG". Kho tư thế (ngồi thẳng lưng, nghiêng đầu, thở chậm)
#    đúng về mặt kỹ thuật nhưng nó chính là thứ đẻ ra 72 khuôn mặt bình thản — đo lô cũ:
#    **0/73 prompt có cảm xúc mạnh**. Mẫu thì liên tục ôm đầu, há miệng, ngả bật ra sau.
# ⚠️ Vẫn KHÔNG đụng vùng Veo hỏng: đây là chuyển động THÂN + MẶT, không thao tác vật nhỏ.
REACT_FACE = [                         # chỉ mặt · thân — dùng được cả khi tay đang bận
    "{p} eyes widening and {p} mouth falling open",
    "leaning sharply back away from the table",
    "brows pulling together hard, jaw tightening",
    "{p} shoulders dropping and {p} head sinking forward",
    "{p} chin lifting as {p} lets out a long relieved breath",
    "{p} head snapping round toward the camera",
]
REACT_HAND = [                         # chỉ khi ACTION chưa chiếm tay
    "both hands rising to the sides of {p} head",
    "one hand pressing flat against {p} chest",
    "one palm coming down onto the table top",
    "one hand covering {p} mouth",
]
# 🔴 Kho phản ứng xoay theo `idx` nên MÙ với sắc thái cảnh — scene lạy trước bàn thờ bị
#    gán "mắt mở to, há miệng". Cảnh trang nghiêm / gật đầu / cúi chào lấy kho TRẦM.
REACT_CALM = [
    "{p} eyelids lowering for a moment",
    "{p} shoulders settling as {p} breathes out slowly",
    "{p} head bowing a few degrees lower",
    "{p} chin lifting slowly, expression softening",
]
QUIET_CUE = ("palms together", "bows", "bow", "nod", "quietly", "altar", "chrysanthemum")
# ACTION đã chiếm tay chưa — dò bằng chính từ chỉ tay/thao tác cầm nắm trong mô tả
HAND_BUSY = ("hand", "hands", "palms", "arm", "arms", "finger",
             "holds", "holding", "hold", "taps", "points", "propping", "lifting")

# 🔴 Lô cũ chỉ có 4 cỡ và cả 4 đều là "người ngồi, ngang tầm mắt" ⇒ xem 3 clip là biết cả
#    video. Mẫu đảo cỡ rất mạnh: cận sát mặt · toàn cảnh người bé trong phòng · góc thấp.
# ⚠️ CỐ Ý KHÔNG có cỡ "chỉ bàn tay, mặt ngoài khung": `feedback_ai_video_hong_thao_tac_tay`
#    đo được 14/21 shot hands-only là HỎNG. Mọi cỡ dưới đây đều còn THÂN người trong khung.
FRAMING = [
    "medium shot from the waist up",
    "tight close-up from the shoulders up, the face large in frame",
    "wide shot showing the whole room, the person small on one side of it",
    "low angle from table height, the objects large in the foreground and the face and torso "
    "behind them",
    "three-quarter angle from the side, from the waist up",
    # ⚠️ Không viết "over-the-shoulder" trần: nó nghĩa là KHÔNG thấy mặt, chọi thẳng câu
    #    "face clearly visible at all times" ở cuối prompt. Và đại từ "their" làm gate
    #    giới tính báo đỏ. Bản này giữ được cả góc lưng lẫn khuôn mặt.
    "a three-quarter view from slightly behind one shoulder, the face still visible in profile",
]


def prompt_for(body: str, idx: int = 0) -> str:
    kind = classify(body)
    who, subj, poss = cast_of(body)
    room, light, palette = setting(idx)          # phòng + sáng + màu đi THÀNH BỘ
    clear = CLEAR.format(s=gside(idx))           # chừa chỗ cho lớp đồ hoạ Remotion
    style = f"{_LOOK}, {room}"

    if kind == "VIZ":
        subj = body.split("VIZ:", 1)[1].strip()
        # 🔴 BỎ câu phản ứng CỐ ĐỊNH. Bản trước gắn cứng "surprised smile, hands together" vào
        #    MỌI prompt VIZ ⇒ 12/12 clip cùng một động tác.
        who_line = ""
        if idx % 3 == 0:
            who_line = (f" An elderly Japanese person is partly visible at the very edge of the "
                        f"frame, {VIZ_REACT[(idx // 3) % len(VIZ_REACT)]}.")
        return (f"{style}, a clean visual-explainer shot. SUBJECT: {subj}. The objects fill most "
                f"of the frame and are the clear focus, arranged so their relative size is "
                f"obvious at a glance. {_cap(VIZ)}.{who_line} FRAMING: wide shot, the whole "
                f"arrangement visible. {clear}. {light}. {palette}. {CAM_N}")

    if kind in ("GAUGE", "SCREEN", "META", "INFOG"):
        subj = body.split(":", 1)[1].strip()
        note = {"GAUGE": GAUGE_NOTE, "SCREEN": SCREEN_NOTE,
                "META": META_NOTE, "INFOG": INFOG_NOTE}[kind]
        graphic = kind in ("META", "INFOG")
        st = (style if not graphic else
              "a polished 3D illustration for an explainer video" if kind == "META" else
              "a clean 2D infographic animation for an explainer video")
        lg = (LIGHT_3D if kind == "META" else LIGHT_2D) if graphic else light
        cl = COLOR_GRAPH if graphic else palette
        # khuôn đồ hoạ tự lấp khung nên KHÔNG chừa chỗ — Remotion không dán gì lên nó
        extra_clear = "" if graphic else f" {clear}."
        return (f"{st}. SUBJECT: {subj}. {_cap(note)}.{extra_clear} {lg}. {cl}. {CAM_N}")

    if kind == "CROWD":
        subj = body.split("CROWD:", 1)[1].strip()
        return (f"{STYLE_PUB}. SUBJECT: {subj}. {_cap(CROWD_NOTE)}. FRAMING: wide shot showing "
                f"the whole space. {clear}. {LIGHT_PUB}. {COLOR_PUB}. {CAM_N}")

    # bỏ tiền tố khuôn, rồi thay cụm cast ĐẦU CÂU bằng đại từ — nếu giữ nguyên thì prompt đọc
    # thành "SUBJECT: an elderly Japanese man … ACTION: an elderly man sits…", và Veo hiểu là
    # HAI người trong khung.
    if kind in ("SPLIT", "PANEL", "HOLD", "DESK"):
        body = body.split(":", 1)[1].strip()
    body = CAST_RE.sub(subj, body, count=1)

    extra = ""
    if kind in ("SPLIT", "PANEL"):
        extra = " " + _cap(SPLIT_NOTE if kind == "SPLIT" else PANEL_NOTE) + "."
    if kind == "HOLD":
        # 🔴 Giấy có nền biểu mẫu nhưng KHÔNG đọc được (guard `TXT`); chữ thật do telop
        #    Remotion vẽ đè. 🔴 Viết TÍCH CỰC: "never picked up" cũ là câu cấm hoá gợi ý.
        paper = BOOK if "passbook" in body else FORM
        thing = "passbook" if "passbook" in body else "sheet"
        extra = (f" {_cap(paper)}. The {thing} is already in the hand and fully open in the very "
                 f"first frame, and it stays in exactly that same position for the whole shot, "
                 f"completely still and rigid.")
    if kind == "DESK":
        extra = (" ON THE TABLE: a pocket calculator, an open spiral notebook, a stack of "
                 "receipts, brown envelopes, a teacup and a pile of paperwork, cluttered "
                 "naturally.")

    # 💴 ĐẠO CỤ TIỀN THẬT — mẫu khung nào cũng có tiền, lô cũ **0/73**. Chỉ gắn khi cảnh vốn
    #    nói về tiền/phong bì/sổ; rải bừa vào cảnh nói tờ khai là sai nội dung.
    if kind in ("PERSON", "DESK", "SPLIT") and any(w in body.lower() for w in MONEY_CUE):
        extra += f" ALSO IN FRAME: {MONEY_PROP[idx % len(MONEY_PROP)]}."

    # 🔴 SPLIT/PANEL đã tự khai khung trong NOTE của chúng ⇒ nối thêm FRAMING xoay vòng là hai
    #    câu khung chọi nhau. 🔴 HOLD chỉ lấy 2 cỡ gần: khung rộng thì tờ giấy bé mất.
    if kind in ("SPLIT", "PANEL"):
        frame = ""
    elif kind == "HOLD":
        frame = f" FRAMING: {FRAMING[idx % 2]}."
    else:
        frame = f" FRAMING: {FRAMING[idx % len(FRAMING)]}."

    # 🔴 Gắn thêm MỘT phản ứng từ kho, xoay vòng — lấp đúng chỗ Veo vốn tự điền bằng "chắp tay
    #    + mỉm cười", và đây là thứ lô cũ thiếu hoàn toàn (0/73 có cảm xúc mạnh).
    # ⚠️ Cặp vợ chồng KHÔNG lấy từ kho: kho viết số ít, ghép vào là sai hoà hợp ("they widens").
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
    # ⚠️ Câu "miệng khép" CHỌI với phản ứng há miệng ⇒ tắt khi phản ứng đã nói về miệng.
    quiet = "" if ("mouth" in b2 or "palms together" in body) else \
            f" {_cap(pr + ' hands stay apart from each other throughout, and ' + mouth)}."
    return (f"{style}. SUBJECT: {who}. ACTION: {body}.{b2}{extra}{frame} "
            f"The face and upper body are clearly visible at all times.{quiet} "
            f"{clear}. {light}. {palette}. {CAM_P}")


def main():
    rows = build()
    items = []
    for r in rows:
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        for k in range(r["nshot"]):
            suf = f"_{k+1}" if r["nshot"] > 1 else ""
            items.append(dict(stem=f"c22_{r['i']:02d}{suf}", scene=r["i"],
                              kind=classify(r["body"]), body=r["body"],
                              prompt=" ".join(prompt_for(r["body"], len(items)).split())))

    io.open(os.path.join(OUT, "flow22_FULL_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(x["prompt"] for x in items) + "\n")
    io.open(os.path.join(OUT, "flow22_FULL_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1:>2} -> {x['stem']}.mp4   [scene {x['scene']:>2} · {x['kind']} · chua trong ben {gside(i)}]"
                  for i, x in enumerate(items)) + "\n")

    # ── LÔ 1: 12 prompt phủ đủ 4 khuôn, ưu tiên scene ĐẦU bài ────────────────
    lot1, seen = [], {}
    for x in items:
        c = seen.get(x["kind"], 0)
        if c < 3:                       # tối đa 3 cái mỗi khuôn
            lot1.append(x); seen[x["kind"]] = c + 1
        if len(lot1) >= 12:
            break
    rest = [x for x in items if x not in lot1]
    half = len(rest) // 2
    for name, grp in (("LOT1", lot1), ("LOT2", rest[:half]), ("LOT3", rest[half:])):
        io.open(os.path.join(OUT, f"flow22_{name}.txt"), "w", encoding="utf-8").write(
            "\n".join(x["prompt"] for x in grp) + "\n")
        io.open(os.path.join(OUT, f"flow22_{name}_TENFILE.txt"), "w", encoding="utf-8").write(
            "\n".join(f"dong {i+1:>2} -> {x['stem']}.mp4   [scene {x['scene']:>2} · {x['kind']}]"
                      for i, x in enumerate(grp)) + "\n")

    import collections
    c = collections.Counter(x["kind"] for x in items)
    print(f"\n⭐ {len(items)} prompt -> flow22_FULL_FLOW.txt")
    print(f"   khuôn: {dict(c)}")
    print(f"   LOT1 {len(lot1)} (gen thử trước) · LOT2 {half} · LOT3 {len(rest)-half}")
    print(f"   dài prompt: {min(len(x['prompt']) for x in items)}–"
          f"{max(len(x['prompt']) for x in items)} ký")


if __name__ == "__main__":
    main()
