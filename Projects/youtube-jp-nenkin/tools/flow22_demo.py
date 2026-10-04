# -*- coding: utf-8 -*-
"""
flow22_demo.py — prompt Veo cho video 22: 5 KHUÔN SHOT + mascot ông già + logo.

VÌ SAO 5 KHUÔN (user chốt 2026-09-07, kèm 3 ảnh mẫu): bản đầu chỉ có MỘT khuôn "giơ tờ
giấy có chữ" ⇒ 12 clip giống hệt nhau, xem 30 giây là chán. Bóc 3 khung mẫu ra thì kênh
chuẩn dùng ít nhất 3 khuôn khác hẳn, và chúng khác ở CƠ CHẾ chứ không chỉ ở góc máy:

  ① HOLD-FORM  giơ biểu mẫu có chữ to        -> tải MỘT mệnh đề, đọc trong 1 giây
  ② DESK-RICH  ngồi bàn chất đầy đồ, thao tác nhẹ, chữ to nằm trên TẤM DỰNG ĐỨNG ở
               tiền cảnh  -> tải KHÔNG KHÍ đời sống, không ai giơ gì cả
  ③ ALARM      cảm xúc mạnh, vật THẬT không hiệu ứng -> tải NGUY; quầng đỏ + dấu ✗ do
               Remotion vẽ đè (Veo tô đỏ thẳng lên da tay — xem §③)
  ④ GOOD-GLOW  vật phát sáng VÀNG ẤM, mặt giãn ra -> tải AN (nhận được, xong việc)
  ⑤ MACRO-OBJ  cận vật, KHÔNG người -> nhịp nghỉ giữa hai khuôn có người

⭐ Phát hiện đắt nhất từ ảnh mẫu #3: **chữ to KHÔNG nhất thiết phải cầm trên tay.**
   Nó nằm trên một tấm 振込通知書 dựng đứng ở tiền cảnh phải. Nhờ vậy tay nhân vật rảnh
   để làm việc khác, và ta tránh được đúng vùng Veo hỏng (thao tác tay với vật nhỏ).

⚖️ RỦI RO CHỮ, user đã biết và đã quyết: Veo dựng chữ Nhật kém (11/84 shot video 21 nát).
   Đường lui dựng sẵn: `still22_prompts.py` (gen ảnh tĩnh) + `_media_library/
   animate_still.py` (hoạt hoá) — chữ đứng tuyệt đối, đổi lại người không cử động.
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"

# ═══════════════════════════════════════════════════════════════════════════
# KHỐI DÙNG CHUNG
# ═══════════════════════════════════════════════════════════════════════════

# ĐO ĐƯỢC: bản mẫu sáng 173 / lô clip cũ 128. Bỏ trống phần ánh sáng thì Veo trả nội
# thất tối trầm. Hai vế cuối chống đúng cái user kêu ở vòng trước: cháy sáng.
LIGHT = ("bright airy room, white walls, warm morning sunlight through a large window with sheer "
         "curtains, soft diffused light, high key but not blown out, the window is not overexposed")

# Gọi TÊN MÀU của vật có thật trong nhà người Nhật cao tuổi. Để Veo tự chọn -> be và xám.
COLOR = ("rich natural colours, a green houseplant, warm wood furniture, a red-and-white calendar "
         "on the wall, patterned fabric cushions, not desaturated")

CAM = ("filmed straight on with a locked-off camera that does not move, the person does exactly one "
       "action for the whole shot, no watermark, no logo, no subtitles")

TXT_GUARD = ("perfectly formed Japanese characters, crisp and legible, in a plain bold sans-serif "
             "typeface")

# 🔴 Câu quyết định ăn/hỏng của khuôn có chữ: giấy là vật CỨNG, ĐỨNG YÊN; chuyển động nằm
#    ở NGƯỜI. Không có nó thì giấy vẫy và chữ chảy theo frame.
HOLD = ("the sheet is held completely still and rigid facing the camera for the entire shot, it "
        "does not bend, wobble or rotate, and the large printed text stays exactly the same and "
        "perfectly legible from the first frame to the last")

# 🔴 NỀN BIỂU MẪU — thứ làm tờ giấy trông THẬT (user: "trang giấy trắng viết 1 dòng trông
#    điêu vãi"). Cố ý KHÔNG đòi đọc được: soi ảnh mẫu thì phần chữ nhỏ đã nát sẵn mà không
#    ai nhận ra, vì mắt chỉ đọc dòng to. Mua vẻ "giấy tờ thật" gần như miễn phí.
FORM = ("the rest of the sheet is a realistic official Japanese form densely covered with printed "
        "elements — a ruled table of small cells, field labels down the left edge, checkboxes, a row "
        "of small square boxes for a postal code in the top right, thin black rules, a small title "
        "in the top left corner and rows of tiny print; this small print is blurred and does not "
        "need to be readable, only the large items must be sharp")

# ── CAST: khoá MÀU ÁO. ⛔ Không tả mặt/tóc chi tiết — model tự chế, và tả càng dài thì mỗi
#    clip ra một người khác (feedback_nhan_vat_dong_nhat_va_noi_lien).
HUSB = "an elderly Japanese man in his late sixties in a checked warm-red shirt under a grey cardigan"
WIFE = "an elderly Japanese woman in her late sixties in a patterned brown knit cardigan over a striped top"


def _items(lines):
    return f"LARGE TEXT, exactly these {len(lines)} items in big bold type: " + " ".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# ① HOLD-FORM — giơ biểu mẫu có chữ to (ảnh mẫu #1)
# ═══════════════════════════════════════════════════════════════════════════
def hold_form(who, lines, action):
    return (f"photorealistic live-action video of {who} holding up an official-looking printed "
            f"Japanese form toward the camera. {_items(lines)} {FORM}. The large items are "
            f"{TXT_GUARD}. ACTION: {action} {HOLD}. LAYOUT: the form fills the left two thirds of the "
            f"frame, tilted very slightly, its top edge near the top of the frame and its bottom edge "
            f"cropped by the bottom; the face is in the right third, large and close to the camera, "
            f"slightly out of focus behind the form.")


# ═══════════════════════════════════════════════════════════════════════════
# ② DESK-RICH — bàn chất đầy đồ, chữ to trên TẤM DỰNG ĐỨNG ở tiền cảnh (ảnh mẫu #3)
# 🔴 Khuôn chở "đời sống": bàn phải ĐẦY. Bàn trống là dấu hiệu rõ nhất của hình dựng.
#    Liệt kê thẳng 6-7 vật, đừng viết chung chung "some documents".
# ═══════════════════════════════════════════════════════════════════════════
def desk_rich(who, lines, action):
    return (f"photorealistic live-action video of {who} sitting at a wooden dining table covered with "
            f"everyday things. {_items(lines)} The large text is printed on a large notification card "
            f"standing upright in the right foreground, angled toward the camera and held perfectly "
            f"still; it is {TXT_GUARD}. ON THE TABLE: a pocket calculator, an open spiral notebook, a "
            f"stack of receipts, brown envelopes, a teacup and a pile of paperwork, cluttered "
            f"naturally. BACKGROUND: a bright window looking onto a small shopping street with shop "
            f"signs, a television, a bookshelf with framed photographs and a sofa with a folded "
            f"blanket, all soft and out of focus. ACTION: {action} LAYOUT: the person fills the "
            f"centre-left of the frame from the waist up, the notification card is large in the "
            f"foreground on the right.")


# ═══════════════════════════════════════════════════════════════════════════
# ③ ALARM — cảm xúc mạnh, VẬT THẬT, KHÔNG hiệu ứng (sửa 2026-09-07)
# 🔴 BỎ HẲN VẾ "vật phát sáng đỏ". Đo trên clip task_005: Veo hiểu "red glow spills onto
#    the hands" thành **TÔ ĐỎ BÀN TAY** — nhìn ra bàn tay bị sơn hoặc bị bỏng, không ra
#    ánh sáng; phong bì thì chẳng phát sáng gì; cường độ nhấp nháy loạn giữa các frame.
#    User: *"trông nó kiểu gì ấy"*.
# ⇒ Về đúng nguyên tắc đã lập từ đầu và tao đã tự phá ở khuôn này: **Veo lo NGƯỜI +
#    BỐI CẢNH, Remotion lo HIỆU ỨNG**. Cảnh báo giờ do fx `vignette` (quầng đỏ ở RÌA,
#    không chạm vào người) + `stampx` (dấu ✗ đỏ đập xuống) vẽ đè.
# 📌 Cùng bài học với chữ: thứ gì cần CHÍNH XÁC thì đừng giao cho model sinh video.
# ═══════════════════════════════════════════════════════════════════════════
def alarm(who, obj, action):
    return (f"photorealistic live-action video of {who} reacting in alarm. THE OBJECT: {obj}, an "
            f"ordinary everyday object with completely normal colours, lit by the same daylight as "
            f"the rest of the room. EXPRESSION: eyes wide open, mouth open in shock, eyebrows "
            f"raised high. ACTION: {action} LAYOUT: the person fills the centre of the frame from "
            f"the waist up, leaning slightly toward the camera, the object held up beside the face; "
            f"a home interior behind, soft and out of focus. Natural even lighting, no coloured "
            f"light, no glow, no lens flare, nothing glowing or emitting light. No text anywhere in "
            f"the frame, no letters, no numbers.")


# ═══════════════════════════════════════════════════════════════════════════
# ④ GOOD-GLOW — vật phát sáng VÀNG ẤM, mặt giãn ra (mặt còn lại của ③)
# ═══════════════════════════════════════════════════════════════════════════
def good_glow(who, obj, action):
    return (f"photorealistic live-action video of {who} looking relieved and quietly happy. THE "
            f"OBJECT: {obj}, and it emits a soft warm golden glow that lights the face and hands from "
            f"below, with tiny golden sparkles drifting slowly in the air around it. EXPRESSION: eyes "
            f"softening, a small warm smile, shoulders dropping. ACTION: {action} LAYOUT: the person "
            f"fills the centre of the frame from the waist up; a bright home interior behind, soft "
            f"and out of focus. No text anywhere in the frame, no letters, no numbers.")


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ MACRO-OBJ — cận vật, KHÔNG người. Nhịp nghỉ giữa hai khuôn có người.
# 🔴 Khuôn DUY NHẤT được phép không có người. Mọi khuôn khác phải thấy MẶT + THÂN: đo ở
#    showa video 10, 14/21 clip hands-only hỏng, 89/89 clip có người trong khung đạt.
# ═══════════════════════════════════════════════════════════════════════════
def macro_obj(obj, motion):
    return (f"photorealistic live-action macro video, no people in frame. SUBJECT: {obj}, filling most "
            f"of the frame, sharp and detailed. MOTION: {motion} the camera itself does not move. Warm "
            f"sunlight falls across the surface with soft shadows, a green houseplant and warm wood "
            f"out of focus behind. No text, no letters, no numbers, no watermark.")


# ═══════════════════════════════════════════════════════════════════════════
# 12 SHOT — cố ý XOAY VÒNG 5 khuôn, không để hai shot cạnh nhau cùng khuôn
# ═══════════════════════════════════════════════════════════════════════════
A_POINT = ("the form is already raised in one hand from the very first frame; the other index finger "
           "points firmly at it while speaking to the camera, shocked and open-mouthed.")
A_TAP = ("the form is already raised in one hand from the very first frame; the other index finger "
         "taps twice on one line while explaining to the camera, eyebrows raised.")

SHOTS = [
 ("c22_01_futatsu", hold_form(HUSB,
    ["a headline across the top: 同じ36万円"], A_POINT)),

 ("c22_02_kichou", desk_rich(WIFE,
    ["on the card: 通帳では同じ"],
    "she presses a key on the calculator with one hand while holding a small receipt in the other, "
    "looking down at the table with a puzzled frown, then glancing up.")),

 ("c22_03_katahou", hold_form(HUSB,
    ["a headline across the top: 片方は返金",
     "a box on the left containing: 受け取れる",
     "a box on the right containing: 返金する",
     "a thick black arrow from the left box to the right box with a large red X over it"], A_POINT)),

 ("c22_04_shibou", macro_obj(
    "a wall calendar and a closed bank passbook lying together on a wooden table",
    "a slow shift of sunlight moves across them and the calendar page lifts very slightly in a "
    "draught;")),

 ("c22_05_kigen", alarm(WIFE,
    "a brown official envelope held in one hand, already torn open at one end",
    "she throws up her free hand palm-out as if to stop something, pulling the envelope back toward "
    "her chest and staring at it; an open waste bin sits tilted in the near foreground.")),

 ("c22_06_mishikyu", hold_form(HUSB,
    ["a headline across the top: 未支給年金",
     "a box on the left containing: 請求が要る",
     "a box on the right containing: 自動ではない",
     "a thick black arrow from the left box to the right box with a large red X over it"], A_TAP)),

 ("c22_07_dare", desk_rich(HUSB,
    ["on the card: 請求できる人"],
    "he leans over the table turning the pages of an open notebook with one hand and tracing down a "
    "column with the other index finger, speaking quietly to the camera.")),

 ("c22_08_gonen", alarm(HUSB,
    "a plain printed notice held in both hands, ordinary white paper",
    "he leans back sharply, mouth open, holding the notice out at arm's length toward the camera.")),

 ("c22_09_kakunin", good_glow(WIFE,
    "an open bank passbook resting on her palms",
    "she lowers her shoulders and lets out a slow breath, looking down at the passbook and then up at "
    "the camera with a small smile.")),

 ("c22_10_madoguchi", desk_rich(WIFE,
    ["on the card: まず年金事務所へ"],
    "she picks up a teacup with one hand, both elbows on the table, nodding slowly as she looks at "
    "the camera.")),

 ("c22_11_futsuu", macro_obj(
    "two identical bank passbooks lying open side by side on a wooden table",
    "warm sunlight slowly sweeps across both pages from left to right;")),

 ("c22_12_owari", good_glow(HUSB,
    "a stamped official receipt held up in one hand",
    "he gives a slow single nod toward the camera and lowers the receipt to the table.")),
]

# ═══════════════════════════════════════════════════════════════════════════
# MASCOT ÔNG GIÀ — clip video, nền GREEN SCREEN
# 🔴 Green screen chứ không magenta: cardigan vàng + tóc bạc nằm gần vùng magenta trên vòng
#    màu. Key xanh cho khoảng cách màu lớn nhất.
# 🔴 3D cartoon, KHÔNG photoreal: mascot phải TÁCH khỏi footage người thật, cùng chất liệu
#    thì nó đọc ra như một người thứ hai lọt vào khung.
# ═══════════════════════════════════════════════════════════════════════════
MLOCK = ("a friendly elderly Japanese man mascot character, soft rounded 3D cartoon animation style "
         "with clean simple shapes and a slightly large head, white hair and a short white moustache, "
         "round gold-rimmed glasses, a mustard-yellow cardigan over a white shirt, a small red bow "
         "tie, brown trousers")
MFRAME = ("the character is centred and fills the whole height of the frame, the top of his head "
          "almost touching the top edge and his shoes almost touching the bottom edge, filmed "
          "straight on at eye level with a locked-off camera that does not move")
MBG = ("the background is a completely flat uniform chroma key green screen, pure saturated green, "
       "evenly lit with no gradient and no texture, the character casts no shadow on the background, "
       "there is no floor and no props, he is lit evenly from the front, no letters, no numbers, no "
       "watermark, no logo")
MSHOTS = [
 ("ojii_idle",  "he stands calmly with both hands clasped in front of him, breathing gently, blinking "
                "a few times and giving a small warm smile, he stays in exactly the same spot"),
 ("ojii_nod",   "he nods his head slowly twice in agreement with a warm smile, he stays in exactly "
                "the same spot"),
 ("ojii_point", "he raises his right hand and points upward to his left, mouth moving as if "
                "explaining, he stays in exactly the same spot"),
]

LOGO = ("a circular emblem badge in flat vector style, thick gold ring border, inside the ring a "
        "simple notebook with a magnifying glass resting on it, deep navy blue and warm gold only, "
        "bold thick shapes readable at very small size, the emblem fills the whole height of the "
        "picture and is centred. flat solid pure magenta background, hex FF00FF, absolutely uniform, "
        "no gradient, no letters and no numbers anywhere, no watermark, no signature")


def main():
    flow, names, blocks, kinds = [], [], [], []
    blocks.append("## A. 12 CLIP CẢNH — 5 khuôn xoay vòng\n")
    for stem, body in SHOTS:
        p = " ".join(f"{body} {LIGHT}. {COLOR}. {CAM}".split())
        flow.append(p); names.append(f"{stem}.mp4")
        k = ("HOLD-FORM" if "holding up an official-looking" in body else
             "DESK-RICH" if "covered with everyday things" in body else
             "ALARM" if "reacting in alarm" in body else
             "GOOD-GLOW" if "golden glow" in body else "MACRO-OBJ")
        kinds.append(k)
        blocks.append(f"### {stem}  ·  {k}\n\n```\n{p}\n```\n")

    blocks.append("\n## B. 3 CLIP MASCOT (green screen)\n")
    for stem, mo in MSHOTS:
        p = " ".join(f"{MLOCK}. {mo}. {MFRAME}. {MBG}".split())
        flow.append(p); names.append(f"{stem}.mp4"); kinds.append("MASCOT")
        blocks.append(f"### {stem}\n\n```\n{p}\n```\n")

    blocks.append("\n## C. LOGO (ảnh tĩnh, nền magenta)\n")
    flow.append(LOGO); names.append("brand_logo.png"); kinds.append("LOGO")
    blocks.append(f"### brand_logo\n\n```\n{LOGO}\n```\n")

    io.open(os.path.join(OUT, "flow22_FLOW.txt"), "w", encoding="utf-8").write("\n".join(flow) + "\n")
    io.open(os.path.join(OUT, "flow22_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1} -> {n}  [{kinds[i]}]" for i, n in enumerate(names)) + "\n")
    io.open(os.path.join(OUT, "flow22_PROMPTS.md"), "w", encoding="utf-8").write(
        "# Prompt video 22 — 5 khuôn shot\n\n"
        "Bơm `flow22_FLOW.txt` (mỗi prompt 1 dòng). Tên file: `flow22_TENFILE.txt`.\n\n"
        + "\n".join(blocks))

    for i, p in enumerate(flow):
        pos = p.find("LARGE TEXT")
        tag = f"TEXT@{pos*100//len(p)}%" if pos >= 0 else "—"
        print(f"{i+1:>3}. {names[i]:<22} {kinds[i]:<10} {len(p):>5} ky  {tag}")

    import collections
    c = collections.Counter(kinds[:len(SHOTS)])
    print(f"\nphân bổ khuôn: {dict(c)}")
    # GATE: hai shot cạnh nhau cùng khuôn = lớp hình bắt đầu đơn điệu
    dup = [i for i in range(1, len(SHOTS)) if kinds[i] == kinds[i - 1]]
    print(f"cặp cạnh nhau trùng khuôn: {len(dup)}" + ("  🔴 xen kẽ lại" if dup else "  ✓"))


if __name__ == "__main__":
    main()
