# -*- coding: utf-8 -*-
"""
beats26.py — cầu nối: bảng scene của video 26  →  `beats.json` của **vox-director**.

⭐ ĐƯỜNG DỰNG LỚP HÌNH TỪ VIDEO 23: **Vox paper-collage (newsprint-editorial)**, không còn
   footage AI người thật (user chốt 2026-09-12, trỏ thẳng `E:\\vox-director`).

KIẾN TRÚC — chép đúng ghi chú user đã đặt trong `out/nenkin-19/beats.json` ngày 2026-09-02:
   *"Chỉ dùng stage KEYFRAME + CLIPS. Voice/music/assemble của vox-director KHÔNG dùng:
     giọng đã có (VOICEVOX 雀松朱司 + tag nhấn nhá), phụ đề/CTA/watermark do Remotion lo."*

  ┌ nenkin (giữ nguyên) ─────────────────────────────────────────────────────────┐
  │ _TTS.md → make_timeline_exact → timeline.json → _scenes26.py → plan26.py      │
  │ thẻ stat/formula/genten/gfx · telop · phụ đề · 3 overlay · CTA · render chunk │
  └──────────────────────────────────────────────────────────────────────────────┘
                 │ 92 clip `art`                       ▲ clips/clip_<key>.mp4
                 ▼                                     │
  ┌ vox-director (CHỈ 2 stage) ──────────────────────────────────────────────────┐
  │ beats.json → print_prompts.py (poster collage) → print_motion.py (i2v)        │
  └──────────────────────────────────────────────────────────────────────────────┘

🔴 KHÔNG dùng Atlas Cloud: `keyframes.py`/`clips.py` là đường TRẢ TIỀN, đã chốt bỏ 2026-09-02
   (`project_i2v_api_bo_2026_09_02` · `feedback_youtube_khong_dau_tu_them`). Hai script
   `print_*.py` là **free-tier helper** của chính vox-director — cùng một hàm compose, chỉ
   khác là dump prompt ra file để gen tay qua extension.

🔴 BỎ HẲN `NUM` (chính sách số in lên đạo cụ): guard của collage bắt **mọi mặt giấy để TRỐNG,
   không một chữ/số nào trong khung**. Số chốt do `papercut-stat`/telop của Remotion vẽ bằng
   font ⇒ luôn sắc, luôn đúng. Đây chính là khuôn `feedback_so_tren_hinh_phai_do_font_ve`
   nói tới, và collage làm nó thành ràng buộc CỨNG thay vì một lời dặn.

CHẠY:
    python tools/beats26.py                 # ghi beats.json
    cd E:/vox-director && python scripts/print_prompts.py out/nenkin-26
    cd E:/vox-director && python scripts/print_motion.py  out/nenkin-26
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
import flow23_full                      # noqa: E402  (classify + kho mô tả)
from plan26 import build                # noqa: E402

OUT = r"E:\vox-director\out\nenkin-26"

# ── GUARD dán vào cuối MỌI scene — bản đã dùng ở nenkin-19, giữ nguyên từng chữ ──
# ① người Nhật cao tuổi (không thì style mid-century trôi về Americana)
# ② mọi mặt giấy TRỐNG, không một chữ nào (Veo/nano-banana viết kanji là nát)
# ③ chừa dải phải 1/10 khung — chỗ Remotion dán mascot + logo (vùng cấm x1690–1910)
GUARD = (" Any person shown is JAPANESE and elderly (60s-70s), in modest everyday Japanese "
         "clothing — not Western, not American, not 1950s retro fashion, no Americana styling. "
         "NUMERALS ARE WANTED: where the scene names a figure, cut it as BIG bold Arabic "
         "numerals from coloured card with visible scissor edges, pasted flat onto the page — "
         "they are a core part of this collage language, not decoration. But NO WORDS in any "
         "language and NO Japanese lettering anywhere: no kanji, no kana, no headline, no "
         "caption, no signage, no logo, no watermark; every document, sign and label surface "
         "stays blank apart from those cut-out numerals. Leave a narrow empty strip of flat "
         "paper along the right edge, about one tenth of the width")

# ── khuôn của mình → cỡ cảnh + cú máy của vox-director ──────────────────────────
# ⚠️ `camera_move` phải nằm trong `clips.CAMERA_VOCAB`; và nhóm "bold" (orbit/dolly_zoom/roll/
#    whip) CHỈ dùng với constraints="loose" — kênh này chạy "strict" nên không đụng tới.
SHOT_SIZE = {"HOLD": "CLOSE", "SCREEN": "MEDIUM", "CROWD": "WIDE", "VIZ": "WIDE",
             "DESK": "MEDIUM", "PERSON": "CLOSE", "SPLIT": "MEDIUM", "PANEL": "CLOSE",
             "META": "WIDE", "GAUGE": "WIDE", "INFOG": "WIDE"}
# Xoay cú máy trong từng khuôn để 92 clip không cùng một chuyển động.
# 🔴 22/92 khung máy TĨNH + giấy động = vẫn thiếu sức. Giữ `static` cho đúng chỗ mà ĐỨNG YÊN
#    là nghĩa (mặt đồng hồ đo), còn lại cho khung thở. ⚠️ Vẫn bám `audience-45plus` §2 mục 6:
#    pan/zoom phải CHẬM + ease — vox vocab đã ghi "very slow smooth", không phải Ken Burns giật.
# 🔴🔴 ĐO SHOWCASE 2026-09-14 (`E:/vox-director/assets/showcase-football.mp4` + `-money.mp4`,
#    user trỏ thẳng: *"tao muốn nó có hồn như này cơ"*):
#      MAD frame-to-frame  **8,2–10,5**   (ảnh tĩnh hoá động của workspace chỉ 1,2–2,8)
#      dịch khung toàn cục **0,28–0,34 px/frame**  ⇒ **gần như KHÔNG có cú máy**
#    ⇒ Toàn bộ "hồn" nằm ở CHUYỂN ĐỘNG TRONG KHUNG, không ở Ken-Burns. Bản cũ xoay
#    push_in/pan/pull_out cho gần hết khuôn — tức đổ ngân sách chuyển động vào đúng chỗ
#    showcase KHÔNG dùng. Nay: `static` là mặc định, `parallax` (vox-director định nghĩa là
#    "camera otherwise steady") là biến thể; push_in/pan chỉ còn ở khuôn thật sự cần.
CAM = {"HOLD": ["static", "parallax"], "SCREEN": ["static", "push_in"],
       "CROWD": ["parallax", "static"], "VIZ": ["static", "parallax", "push_in"],
       "DESK": ["static", "parallax"], "PERSON": ["static", "parallax"],
       "SPLIT": ["static", "pan"], "PANEL": ["static", "push_in"],
       "META": ["parallax", "static"], "GAUGE": ["static", "parallax"],
       "INFOG": ["parallax", "static"]}

# ── BỐ CỤC THEO TỪNG SHOT ───────────────────────────────────────────────────────
# 🔴 Scene được cấp 2–3 clip mà mô tả y nguyên thì ra 2–3 POSTER GIỐNG HỆT (đo được 16/92 ở
#    bản đầu) — vừa đốt lượt gen, vừa cho hai hình giống nhau đứng cạnh nhau trên timeline.
#    Đường photoreal không dính vì nó xoay FRAMING/SETTINGS/REACTION theo idx; collage bỏ hết
#    mấy khối đó nên mất luôn cơ chế phân biệt. ⇒ mỗi shot phải là một CÁCH DỰNG khác của
#    cùng một beat, đúng cách user làm ở nenkin-19 (1a WIDE kho hàng · 1b CLOSE cut-in).
SHOT_FRAME = [
    # 🔴 Showcase KHÔNG có khung toàn cảnh "người bé trong phòng": nó cắt SÁT hành động
    #    (chỉ thấy hai cẳng chân, chiếm gần trọn khung). Khung rộng + biên độ nhỏ = ảnh chết.
    (" Composed as a TIGHT ACTION CROP: the moving part fills most of the frame, the figure"
     " cut-out cropped hard by the frame edges.", "CLOSE"),
    # 🔴 Bản đầu viết "the HANDS and the object fill the frame, the FIGURE'S FACE only partly
    #    in frame" ⇒ dán vào cảnh không có tay/không có mặt là tự bịa thêm bộ phận (11/92).
    (" Composed as a CLOSE cut-in: the nearest cut-outs fill the frame and the layers behind"
     " them fall away, the rest cropped hard by the frame edges.", "CLOSE"),
    (" Composed as a MEDIUM three-quarter view from the side, the figure cut-out turned"
     " slightly away and layered over a bold flat colour block.", "MEDIUM"),
    (" Composed from a LOW ANGLE at table height: the objects loom large as foreground paper"
     " cut-outs and the figure cut-out sits behind them.", "MEDIUM"),
    (" Composed as a TIGHT DETAIL cut-in: the object alone fills the frame as one big paper"
     " cut-out, no figure in shot.", "CLOSE"),
]
# 🔴🔴 DÃY THỨ HAI CHO CẢNH KHÔNG CÓ NGƯỜI. Dãy trên nhắc "the figure cut-out" ở 3/5 biến
#    thể ⇒ dán vào cảnh vật-thuần (đồng hồ đo "no people in frame", hai hộp hồ sơ, dải xu)
#    là khối chung TỰ THÊM NGƯỜI vào cảnh cố ý không có người — đo được 8/92.
#    Đây là lần thứ NĂM của cùng một bệnh trong dự án này (guard chữ · câu one-action ·
#    NOTE kê chuyển động · bối cảnh không bàn · giờ là bố cục nhắc người).
#    ⇒ Mỗi lần thêm một câu vào khối chung: hỏi "câu này có chọi mô tả của cảnh nào không?"
SHOT_FRAME_OBJ = [
    (" Composed as a TIGHT ACTION CROP: the moving objects fill most of the frame, the rest"
     " cropped hard by the frame edges.", "CLOSE"),
    (" Composed as a CLOSE cut-in: one part of the arrangement fills the frame as large paper"
     " cut-outs, the rest running off the edges.", "CLOSE"),
    (" Composed as a MEDIUM three-quarter view from the side, the objects layered over a bold"
     " flat colour block.", "MEDIUM"),
    (" Composed from a LOW ANGLE close to the surface, the nearest objects looming large in the"
     " foreground.", "MEDIUM"),
    (" Composed as a TIGHT DETAIL cut-in: a single object fills the frame as one big paper"
     " cut-out.", "CLOSE"),
]
_PPL = re.compile(r"(elderly|clerk|visitor|person|staff|master|customer|figure|hand)", re.I)

# 🔴 Dãy này phải DÀI HƠN số shot nhiều nhất của một scene, nếu không nó quay vòng và shot
#    thứ N+1 trùng hệt shot 1 — đã dính: scene 62 có 4 shot, dãy 3 biến thể ⇒ a và d giống nhau.

# ── ĐỘNG CỦA GIẤY — thứ vox-director gọi là `element_motion` ────────────────────
# 🔴 Đây là lớp NỘI DUNG, không phải lớp hình thức: nó tả TỪNG MẢNH GIẤY nhúc nhích thế nào.
#    Bài học `flow23_full` vừa rút (NOTE kê chuyển động thì chọi mô tả cảnh) áp y nguyên ở
#    đây — nên chuyển động phải suy từ CHÍNH hành động của scene, không lấy từ kho chung.
#    Kho dưới chỉ là lớp NỀN thứ hai (giấy/ánh sáng/halftone), luôn cộng thêm, không thay thế.
# 🔴 LỚP NỀN phải ĐỘNG THẬT, không phải "nhích một milimét". Bản đầu viết toàn
#    "settles a millimetre" · "breathe softly" · "a hair" ⇒ đúng nghĩa `calm`, và đó là thứ
#    user gọi là vô tri. Showcase: bóng bay ngang khung, vạt áo tung, chân đá.
# 🔴 Lớp thứ BA. Đo showcase: bóng bay + chân đá + vạt áo tung + halftone đập = 3–4 chuyển
#    động CÙNG LÚC. Lô của tao chỉ 1,88 mệnh đề/shot ⇒ khung thiếu việc để mắt bám.
# 🔴 KHO PHẢI LỚN HƠN LÔ, nếu không lặp là chuyện hiển nhiên chứ không phải rủi ro:
#    6 loại cho 92 clip ⇒ mỗi cái **15–16 lần** (user: *"hiệu ứng lặp lại nhiều quá"*).
#    24 accent × 16 nền = 384 cặp ⇒ mỗi cặp gần như không lặp trong 92 clip.
#    ⚠️ Và lấy theo BƯỚC NGUYÊN TỐ CÙNG NHAU (7/5) chứ không `i % n` — modulo thẳng làm chu
#    kỳ trùng với thứ tự scene nên mắt bắt ra quy luật ngay (bài học `x % N` ở CLAUDE.md §②).
# ⛔ KHO `ACCENT` ĐÃ BỎ HẲN 2026-09-14 (user: *"ở video mẫu tao gửi mày có hành động giấy
#    bay đâu. Toàn những người với vật chuyển động nó mượt mà chứ không giật giật"*).
#    Cả 24 mục đều là **mảnh giấy bay vào rồi dán** ("flicks in and sticks" · "sails across
#    the lens" · "pops and shrinks away") — mỗi cái là một CÚ NHÁY, và nháy chính là GIẬT.
#    Đo lại showcase: bản đồ chuyển động 3×3 cho ô nền (chỗ có tam giác/đĩa/zigzag) chỉ
#    **1,71** trong khi ô có người/bóng là **8–10** ⇒ đồ trang trí trong showcase ĐỨNG YÊN.
#    ⇒ Chuyển động thứ hai phải là NGƯỜI/VẬT khác đang làm việc, không phải giấy vụn.
SECOND = [
    "a second figure further back keeps at their own task, arms hinging slowly",
    "a second element nearby keeps shifting position, one step at a time",
    "a nearby cut-out keeps swinging through a wide tilt on its own weight, all shot long",
    "the fabric of the clothing keeps swaying with each movement",
    "a second figure at the edge of the frame keeps at their own small task",
    "the stack beside the subject keeps settling lower, one piece at a time",
    "a figure at the far side turns slowly toward the action and back",
    "the smaller objects drift a little each time the main one moves",
]
# ⛔ Kho `PAPER_BED` cũ (16 mục) cũng đã BỎ — toàn "slides sideways and snaps into place",
#    "slaps down flat", "rocks once as if knocked", "fan apart and slap back": mỗi mục là một
#    CÚ ĐẬP. Nền của showcase gần như bất động (ô nền 1,71/10). Thay bằng trôi rất chậm.
BED = [
    "behind them the background layers hold their places",
    "the flat colour field behind holds still while only the figures move",
    "the printed background stays put, steady under the movement",
    "the backdrop holds its place for the whole shot",
]

# Chủ ngữ của mảnh giấy chính, suy từ khuôn — để câu mô tả đọc ra "mảnh giấy", không phải người thật.
# Mỗi khuôn một DÃY biến thể, xoay theo chỉ số — bản một-câu-một-khuôn chỉ cho 46/92 câu
# khác nhau, tức gần nửa số clip động y hệt nhau.
# 🔴🔴 VIẾT LẠI 2026-09-14 SAU KHI XEM SHOWCASE. Bản cũ toàn **SỰ KIỆN MỘT LẦN**
#    ("flies in and sticks" · "drops and bounces" · "snaps into place") — mảnh giấy bay vào,
#    dán xuống, rồi KHUNG ĐỨNG YÊN nốt phần còn lại của clip. Showcase thì ngược hẳn: hai
#    nhân vật **đá bóng qua lại suốt 5 giây**, chân co duỗi, vạt áo tung, hạt bay liên tục.
#    Đó là cái user gọi là *"nhân vật chuyển động mượt mà"*.
# ⇒ Mỗi câu dưới đây phải là **MỘT VIỆC ĐANG LÀM, có KHỚP NỐI, và KHÔNG KẾT THÚC** trong shot.
KIND_MOVE = {
    "META":   ["the cut-out pieces keep cycling through the mechanism, one after another, "
               "without the flow ever stopping or resetting",
               "the shapes swing past each other in a steady back-and-forth that carries on "
               "through the last frame",
               "the arrangement keeps working — one part driving the next, over and over"],
    "GAUGE":  ["the needle sweeps up and eases back, again and again, while the dial face "
               "swings through a wide tilt on its mount",
               "the dial keeps breathing — the pointer drifting up, hanging, and sinking back"],
    "INFOG":  ["the blocks keep rising and settling in a slow relay that never finishes",
               "the connector arrows pulse along their length, one after another, continuously"],
    "CROWD":  ["the figures keep moving through the scene — one bends and straightens, another "
               "turns, a third steps forward — overlapping, never all still at once",
               "the group carries on its business the whole shot, arms hinging at the elbow, "
               "head strips turning, nobody freezing into a pose",
               "the queue keeps shuffling forward a step at a time, the front figure's arm "
               "rising and lowering again and again"],
    "VIZ":    ["the pieces keep stacking and re-settling in a steady rhythm that runs past the "
               "end of the shot",
               "the arrangement keeps rearranging itself, elements trading places continuously",
               "one piece after another moves along the arrangement from end to end, a steady stream, never a gap"],
    "HOLD":   ["the held sheet keeps turning over and back on the hinge of the wrist, the elbow "
               "opening and closing, the head strip tipping down to it and lifting again",
               "the paper sheet rocks and tilts in the hands the whole shot, caught and "
               "re-caught, never set down",
               # 🔴 "the hand cut-out" (tay rời, không thân) làm model trả về BÀN TAY NGƯỜI
               #    THẬT thò vào khung giấy — đúng luật đã ghi ở `feedback_ai_video_hong_thao_tac_tay`
               #    (cấm framing không có THÂN). Đo được ở clip_22a. Gọi tên cả nhân vật.
               "the figure keeps working the sheet forward and back in both hands, the thumb "
               "creasing the corner over and over"],
    "SCREEN": ["rows of cut-out strips keep sliding up the screen face, a continuous scroll",
               "the panel face keeps refreshing — strips lifting away and new ones settling"],
    "DESK":   ["the hands keep working across the desk — reaching, placing, smoothing, reaching "
               "again — one unbroken sequence",
               "papers keep passing under the hands, one after another, the head strip tipping "
               "down and up with each one",
               "the figure keeps leaning in and easing back over the desk, arms hinging"],
}


def _subject_move(kind: str, body: str, i: int) -> str:
    b = body.lower()
    if kind in KIND_MOVE:
        v = KIND_MOVE[kind]
        return v[i % len(v)]
    # 🔴 CẢNH KHÔNG CÓ NGƯỜI thì chuyển động cũng không được nhắc người. Nhánh dưới bám cue
    #    cơ thể (mắt/vai/cằm/tay) và rơi về mặc định "the figure cut-out leans…" — dán vào
    #    cảnh hai hộp hồ sơ / hai bậc thang giấy là **tự thêm người vào khung** (đo 3/92).
    #    Cùng bệnh với SHOT_FRAME ở trên: khối chung viết cho khuôn CÓ NGƯỜI, dán cho cả lô.
    if not _PPL.search(body) or "no people in frame" in body:
        OBJ = ["the two groups of cut-outs ease apart at a steady crawl, the bare gap between them widening",
               "the cut-outs glide along their paper tracks at a steady crawl, one following the next",
               "the pieces lower onto the backing sheet one after another, each easing into place",
               "the nearest cut-out rises a paper-thickness off the sheet and lowers again, breathing slowly"]
        return OBJ[i % len(OBJ)]

    # PERSON / SPLIT / PANEL — bám đúng hành động đã viết trong scene
    # 🔴 Kho phản ứng cũng phải PUNCHY. Bản đầu toàn "a few degrees and settles" — đúng
    #    nghĩa `calm`, và nó kéo 30% lô về lại vi-động dù biên độ đã đổi sang punchy.
    for cue, mv in (
        ("eyes", "the eye cut-outs widen and the brow strip rides up, then eases back, over and over"),
        ("mouth", "the mouth cut-out opens and closes while the head rocks slowly back and forward"),
        ("shoulders", "the shoulder cut-outs sink and lift again while the head strip swings slowly forward"),
        ("chin", "the chin cut-out rises and the whole figure straightens, then softens again, repeating"),
        ("palm", "the palm cut-out swings up in front of the face and lowers again on a smooth arc"),
        ("hands", "both hand cut-outs rise to the sides of the head and settle back down, again and again"),
        ("head", "the head cut-out turns toward the camera and back on a slow, even arc"),
        ("nods", "the head cut-out dips and lifts in a slow, steady nod that keeps going"),
        ("bow", "the whole figure hinges forward into a bow and rises again, unhurried"),
    ):
        if cue in b:
            return mv
    # 🔴 CÂU MẶC ĐỊNH — rơi vào MỌI scene không khớp cue nào, tức phần lớn lô. Bản cũ
    #    ("sways gently … weight shifting") là câu YẾU NHẤT trong cả tool mà lại được dùng
    #    nhiều nhất: đo được ở clip_4a, nó đứng ngay cạnh "WIDE arcs" và thắng.
    return ("the cut-out figure swings through a wide arc on its hinges — shoulders and arms "
            "opening out and folding back across a large part of the frame, over and over, "
            "never pausing")


# ── CHUYỂN ĐỘNG VIẾT TAY THEO TỪNG CẢNH ─────────────────────────────────────
# 🔴 Kho chung xoay theo KHUÔN nên nó MÙ với cảnh viết tay: cảnh "bà + sổ + số 0" nhận phải
#    câu "các mảnh xếp chồng bắn lên như biểu đồ cột". Cùng bệnh khối-chung-chọi-mô-tả, lần
#    thứ bảy. ⇒ Cảnh nào viết tay thì chuyển động cũng phải viết tay, bám đúng vật trong khung.
# ── CHUYỂN ĐỘNG VIẾT TAY THEO TỪNG CẢNH ─────────────────────────────────────
# 🔴🔴 **BỎ HẲN hai dict motion của video 23 (10 + 78 mục) — chúng khoá theo CHỈ SỐ SCENE,
#     và nội dung là VẬT CỦA VIDEO 23.** Bê sang video 26 thì beat 0 (「bà cụ cầm 通知書 +
#     số 33,000」) nhận phải câu của v23 「the **passbook** swings up … the huge red **0**
#     drops in」 — chuyển động gọi tên hai vật KHÔNG CÓ trong khung. Bắt được ngay ở prompt
#     đầu tiên của lô test, trước khi đốt một lượt gen.
#     ⇒ Đây là `feedback_prompt_khoi_chung_huy_mo_ta` ở dạng tệ nhất: khối chung không chỉ
#     mâu thuẫn, nó **mô tả một cảnh khác**. Và nó IM LẶNG — prompt vẫn xuất đủ, đúng độ dài.
# 📌 Muốn viết tay cho video 26 thì viết vào đây, khoá = CHỈ SỐ SCENE CỦA v26, và mỗi câu
#    phải gọi đúng vật có trong `_scenes26.SCENES[i]`. Chưa viết thì để trống — nhánh
#    `_subject_move()` bám `body` + `_PPL` nên không bao giờ gọi tên vật không có.
MOTION = {
    # Viet tay cho 10 beat cua lo LOT1 (2026-09-16). Moi cau ta MOT VIEC dang dien ra,
    # co KHOP NOI, CHAY SUOT shot — va chi goi ten vat CO THAT trong `_scenes26.SCENES[i]`.
    # ⚠️ ĐÃ BỎ cụm 「the big numeral between them … rocks on its tape」 (2026-09-16):
    #    scene 0 không còn con số đó nữa. Chuyển động gọi tên vật KHÔNG CÓ trong khung
    #    chính là bệnh docstring của khối MOTION này cảnh báo — lần thứ hai (sau scene 38).
    0:  "coins keep dropping onto both stacks at exactly the same rate so the two columns "
        "rise together and stay level; his head strip and her head strip turn toward the "
        "taped strip between them and back again, and the strip lifts at one end and settles",
    1:  "both front doors swing wide and ease shut again, one after the other, while the two "
        "cut-out figures step forward onto their doorsteps and back; the row of paper trees "
        "leans and rights itself all along the kerb",
    5:  "the front door of the right-hand house keeps swinging wide and easing back, and the "
        "two silhouettes inside shift closer together and apart each time; in the left-hand "
        "doorway the single silhouette turns slowly on the spot",
    6:  "her head keeps tipping to one side and coming back level while her paper palm hinges "
        "open and closes again, and the empty torn-paper bubble beside her swells a little and "
        "settles in a slow pulse",
    10: "he lifts the magnifier over the stack of documents and lowers it, then slides the "
        "paper paperweight aside and sets it back — one unbroken sequence; behind him the three bars of "
        "the wall chart rise and ease back in turn",
    12: "she keeps turning the cream envelope over and back on the hinge of her wrist, elbow "
        "opening and closing; behind her the letterbox flap lifts and lowers and the second "
        "envelope slides a little further out each time",
    26: "the right-hand bar keeps growing upward and easing back a little, over and over, "
        "while the left-hand bar stays exactly where it is and the dashed tape line stretches "
        "level across both of them and settles",
    35: "she raises the paper teacup toward her head strip and sets it down again, her elbow "
        "hinging through a wide arc and her head tipping as she does; the framed silhouette on "
        "the wall behind her swings through a wide tilt on its tape",
    # ⚠️ ĐÃ BỎ cụm 「the numeral 10,000 rocks on its tape」 (2026-09-16): scene 38 không còn
    #    con số đó nữa (AI vẽ rớt ký tự → 「10,00」). Chuyển động mà gọi tên một vật KHÔNG
    #    CÓ trong khung chính là bệnh docstring của khối MOTION này cảnh báo.
    38: "the tall column keeps creeping upward toward the dashed tape line and easing back "
        "down, never reaching it, while the torn wedge in the gap widens and closes again "
        "and the whole column rocks a little on its tape",
    46: "the three left-hand doors swing shut one after another and drift back open a little "
        "before closing again, a continuous rolling motion down the row, while the two doors "
        "on the right stay wide and the numeral 3 above them rocks on its tape",
}


# 🔴 Câu SUSTAIN là BẮT BUỘC, không phải trang trí. `clips.py` của vox-director dán guard
#    「ONE continuous move that does not loop, retract or reset」 — câu đó viết cho CÚ MÁY,
#    nhưng model đọc cả prompt nên nó ăn sang PHẦN TỬ và làm mọi thứ đứng hình sau 1 giây.
#    Showcase chạy chuyển động suốt 5s (MAD 8–10) ⇒ phải nói rõ phần tử KHÔNG dừng.
# 🔴 THUẦN TÍCH CỰC. Bản trước viết 「no snapping, no popping, no sudden bursts, nothing
#    flies into or out of frame」 — đúng thứ luật của chính file này cấm: *model đọc TỪ KHOÁ,
#    không đọc chữ "not"/"never"*, nên câu đó **gieo** popping/bursts/flies vào prompt.
#    Gate quét từ-giật bắt được 328 chỗ, và 100% là do hai câu phủ định tao tự viết.
# 🔴 VÒNG 3: bản trước viết 「even, unhurried speed」 ⇒ model hiểu là CHẬM VÀ NHỎ, MAD tụt
#    9,4 → 6,6 trong khi showcase là **21,9**. Mượt ≠ chậm: showcase vừa mượt (CV 0,18) vừa
#    biên độ RẤT lớn. Phải nói cả hai vế.
SUSTAIN = ("the movement is generous and full-bodied — limbs and objects swing through a wide arc "
           "well inside the frame — yet perfectly smooth and even, one continuous flowing motion "
           "from the first frame to the last, still going as the shot ends")


def element_motion(kind: str, body: str, i: int) -> str:
    return (f"{_subject_move(kind, body, i)}; {SECOND[(i * 5) % len(SECOND)]}; "
            f"{BED[(i * 3) % len(BED)]}; {SUSTAIN}")


# ── CẢM XÚC + NỀN MÀU theo CHƯƠNG (beat nào thuộc chương nào) ───────────────────
# Mốc = chỉ số scene mở chương, lấy từ chính bố cục `_scenes26.py`.
CHAPTERS = [
    # Moc = CHI SO SCENE cua `_scenes26.py`, doc tu chinh cac dong `# == ...` trong bang scene.
    (0,   "deep teal",           "quiet, close to home, faintly uneasy"),
    (10,  "warm ochre",          "matter-of-fact, documentary calm"),
    (16,  "deep teal",           "methodical, reading the one-line rule together"),
    (28,  "warm ochre",          "two different rulers for the same word"),
    (34,  "deep mustard ochre",  "personal, one woman and one kitchen table"),
    (40,  "deep red",            "a kindness that quietly costs money"),
    (58,  "warm ochre",          "a breath, then the second question"),
    (59,  "deep teal",           "clearing a myth, then what really moves"),
    (75,  "warm ochre",          "national figures, documentary calm"),
    (80,  "deep teal",           "summing up, warm and steady"),
    (88,  "deep mustard ochre",  "quiet resolution at the kitchen door"),
    (93,  "warm ochre",          "closing, calm and forward-looking"),
]


def chapter_of(i: int):
    bg, feel = CHAPTERS[0][1], CHAPTERS[0][2]
    for start, b, f in CHAPTERS:
        if i >= start:
            bg, feel = b, f
    return bg, feel


def main():
    # 🔴 Nuốt stdout để khỏi in lại bảng 118 scene — NHƯNG phải trả lại VÀ in ra khi gate đỏ,
    #    nếu không `plan26` gọi sys.exit(1) mà thông báo nằm trong buffer ⇒ tool chết IM LẶNG,
    #    exit 1 không một dòng chữ. Đã dính đúng thế 2026-09-12.
    real = sys.stdout
    buf = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", errors="replace")
    sys.stdout = buf
    try:
        rows = build()
    except SystemExit:
        sys.stdout = real
        buf.seek(0)
        print(buf.read())
        raise
    finally:
        sys.stdout = real

    # 🔴 CHIA ĐỀU TRONG KHỐI, KHÔNG THEO SCENE. Bài học 14 của video 22: neo từng khe vào
    #    scene chủ thì scene 12,5s được 1 clip ⇒ speed 0,64 = slow-motion nhìn ra ngay.
    #    Builder Remotion chia theo khối, nên `dur` ghi vào beats.json phải cùng đơn vị —
    #    nếu không user gen theo một con số mà bản dựng dùng con số khác.
    win = {}
    cur = []
    for r in rows + [dict(kind="_end", i=-1, dur=0.0, nshot=0)]:
        if r["kind"] == "art":
            cur.append(r)
        else:
            if cur:
                d = sum(x["dur"] for x in cur)
                n = sum(x["nshot"] for x in cur)
                for x in cur:
                    win[x["i"]] = d / n
            cur = []

    beats, nshot = [], 0
    for r in rows:
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        kind = flow23_full.classify(r["body"])
        body = r["body"].split(":", 1)[1].strip() if kind != "PERSON" else r["body"]
        bg, feel = chapter_of(r["i"])
        # telop là chữ của Remotion, KHÔNG vào ảnh — nó chỉ làm nhãn cho beat
        plain = r["telop"].replace("{", "").replace("}", "").replace("\n", " ")
        shots = []
        for k in range(r["nshot"]):
            dur = round(win[r["i"]], 1)
            shots.append({
                "id": chr(ord("a") + k),
                "dur": dur,
                # 🔴 title=False ở MỌI shot: headline do telop Remotion vẽ. Bật True là xin
                #    generator viết chữ Nhật lên poster — vùng nó hỏng nặng nhất.
                "title": False,
                "shot_size": (SHOT_SIZE.get(kind, "MEDIUM") if r["nshot"] == 1
                              else _FR(body)[k % 5][1]),
                "camera_move": _cam_for(kind, _close(body, r["nshot"], k), nshot),
                # scene 1 clip giữ nguyên cỡ theo khuôn; scene nhiều clip thì MỖI shot một
                # cách dựng khác, nếu không hai poster ra giống hệt nhau.
                "scene": (_enrich(body, kind, r["i"], nshot, _close(body, r["nshot"], k))
                          + ("" if r["nshot"] == 1 else _FR(body)[k % 5][0])
                          + GUARD),
                "element_motion": (MOTION[r["i"]] + "; "
                                   + SECOND[(nshot * 5) % len(SECOND)]
                                   + "; " + SUSTAIN
                                   if r["i"] in MOTION
                                   else element_motion(kind, r["body"], nshot)),
            })
            nshot += 1
        beats.append({"id": r["i"], "title_cn": plain, "title_en": f"SCENE {r['i']} · {kind}",
                      "bg": bg, "feel": feel, "shots": shots})

    doc = {
        "project": "nenkin-26",
        "topic": "介護保険料の段階は世帯で決まる — 第1〜3段階は世帯全員が非課税 / 同居で第3→第5段階、年3万7,900円",
        "language": "ja",
        "aspect": "16:9",
        "style": "collage",
        "theme": "newsprint-editorial",
        "collage_style": (
            "Vintage newsprint editorial paper collage in the style of a mid-century JAPANESE "
            "front-page news feature: bold cut-out photographs and illustrations laid over an "
            "aged broadsheet newspaper page, heavy halftone print dots, aged newsprint texture "
            "with slight ink misregistration, tactile editorial calm — reads like a newspaper "
            # 🔴 CHỈ giữ viền trắng die-cut (đo được trên từng cut-out của showcase). Câu "nền giữ
        # THƯA, chỉ vài mảnh accent" là tao SUY, và nó chọi thẳng khối mechanics của
        # vox-director ngay dưới ("scattered geometric paper accents…") — 92/92 prompt.
        "feature spread brought to life, not an advertisement. Every cut-out carries a thick "
            "white die-cut sticker border around its edge."),
        # 🔴 "max" (nấc cuối) — user: *"sinh động hơn tí nữa"*. Trước đó đã đi calm → punchy. Đo `assets/showcase-football.mp4`: MAD trung vị **5,15**,
        # **46,6% frame động mạnh**, bóng bay ngang nửa khung trong 3 giây. Hai showcase của
        # vox-director đều để trống khoá này ⇒ nhận mặc định **punchy**; còn theme
        # `newsprint-editorial` lại ép `calm` ⇒ để trống là dính calm. Phải khai tường minh.
        # 🔴 "max" = 「elements burst, scatter and fly boldly」 ⇒ ĐÚNG CÔNG THỨC RA GIẬT.
        # Đo showcase 2026-09-14: hệ số biến thiên MAD **0,18–0,19** = chuyển động ĐỀU,
        # và tỉ lệ dư/thô **104%** = toàn bộ nằm ở VẬT, không ở cú máy. ⇒ hạ về "punchy"
        # ("lively, energetic… clear, bold movement" — không có burst/scatter/fly).
        "motion_style": "punchy",
        "constraints": "strict",
        "note": ("Chi dung stage KEYFRAME + CLIPS (print_prompts.py / print_motion.py, duong "
                 "FREE). Voice/music/assemble cua vox-director KHONG dung: giong da co "
                 "(VOICEVOX 雀松朱司 + tag nhan nha), telop/phu de/CTA/watermark/the stat-genten "
                 "do Remotion cua nenkin lo. Nguon su that van la tools/_scenes26.py."),
        "beats": beats,
    }
    os.makedirs(OUT, exist_ok=True)
    with io.open(os.path.join(OUT, "beats.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    import collections
    kc = collections.Counter(b["title_en"].split("· ")[1] for b in beats)
    cam = collections.Counter(s["camera_move"] for b in beats for s in b["shots"])
    print(f"⭐ {len(beats)} beat · {nshot} shot -> {OUT}\\beats.json")
    print(f"   khuôn: {dict(kc)}")
    print(f"   cú máy: {dict(cam)}")
    print(f"   dur/shot: {min(s['dur'] for b in beats for s in b['shots']):.1f}"
          f"–{max(s['dur'] for b in beats for s in b['shots']):.1f}s")

    # ── chạy 2 dumper của vox-director rồi ĐỔ PROMPT VỀ FOLDER VIDEO ───────────
    # 🔴 Vì sao nối liền một lệnh thay vì bảo user chạy 3 bước: `beats.json` phải nằm trong
    #    `out/<project>/` thì script của vox-director mới đọc được, nhưng chỗ user LÀM VIỆC
    #    là `06_VIDEO/<slug>/`. Tách ba bước thì sớm muộn hai nơi lệch nhau, và không ai
    #    biết bản nào mới (đúng bệnh "tài liệu chỏi code" đã ghi ở CLAUDE.md §②).
    sync(doc)


VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai")
VOX = r"E:\vox-director"


# ── ② DÀN PHỤ TRONG KHUNG ───────────────────────────────────────────────────
# 🔴 Đo lô trước: **0,9 người/khung, chỉ 2/92 khung có ≥2 người**, và 78/92 là đúng một
#    "elderly man/woman" (user: *"nhân vật trong 1 khung hình cũng không đa dạng"*).
#    Mẫu showcase thì khung nào cũng có lớp người phía sau. ⇒ thêm 1 dàn phụ cho mọi
#    khung ĐÃ CÓ người; khung ẩn dụ vật thuần (META/GAUGE) thì KHÔNG — ở đó vắng người
#    chính là nghĩa.
# 🔴 GẮN CỜ XA/GẦN TƯỜNG MINH, đừng dò bằng cụm từ. Bản đầu dùng regex `_FAR` và nó hụt
#    "stands further back" · "at the far side" · "lines the back of the frame" ⇒ vẫn dán
#    người-đứng-xa vào khung cắt sát. Đúng bài học đã ghi ở khoá `_tbl`: **cụm-hoá một phép
#    thử vốn là "cái này ở xa hay gần" thì lần nào cũng thiếu một biến thể.**
#    (text, ở_XA) — ở_XA = chỉ dùng được khi khung KHÔNG cắt sát.
EXTRAS = [
    ("a second elderly woman with a grey bun cut from a bold vintage printed illustration waits a step behind", False),
    ("an elderly man in a flat cap cut from a bold vintage printed illustration stands further back, half turned away", True),
    ("a middle-aged daughter in a plain cardigan cut from a bold vintage printed illustration leans in from the edge", False),
    ("a young female clerk in a navy vest cut from a bold vintage printed illustration stands at the far side", True),
    ("two more elderly cut-out figures queue in the background, softly out of focus", True),
    ("a postman cut from a bold vintage printed illustration crosses the far background with a satchel", True),
    # 🔴 Bản cũ ghi "sit small in the deep background" — chọi thẳng câu bố cục
    #    「The main figures are LARGE: they fill most of the frame height」 ở 7/61 prompt.
    ("an elderly couple cut from a bold vintage printed illustration sit together further back", True),
    ("a grandchild cut from a bold vintage printed illustration stands at knee height beside the main figure", False),
    ("a row of four seated elderly cut-outs lines the back of the frame", True),
    ("an office worker in shirtsleeves cut from a bold vintage printed illustration passes behind, mid-stride", True),
    ("a neighbour in an apron cut from a bold vintage printed illustration stands just inside the frame edge", False),
    ("an elderly man's hand and shoulder cut-out enter from the near edge of the frame", False),
]
# ── ③ LỚP BIỂU ĐỒ + CON SỐ ─────────────────────────────────────────────────
# Biểu đồ KHÔNG cần số nên dán được ở mọi cảnh; CON SỐ thì ⚖️ chỉ lấy từ `_truenum23.json`
# (số trích từ CHÍNH lời đọc của cảnh đó) — không có số thật thì không dán số.
# 🔴🔴 TÁCH LÀM HAI KHO — bắt 2026-09-15 khi soi 9 clip gen lại.
#    Nhánh "CẤM SỐ" của guard chạy ĐÚNG, nhưng `_enrich` vẫn dán vào đúng những vật MANG
#    SẴN MỘT THANG SỐ: nhiệt kế · lưới lịch · cột xu đo chiều cao · vạch đếm. Model thấy
#    một cái thang thì vẽ số lên thang, bất kể câu cấm ở giữa prompt. Đo được 4/6 clip
#    "CẤM SỐ" hỏng, và CẢ BỐN đều là scene được dán một trong bốn vật đó:
#      30a nhiệt kế → 「75」 đỏ to + vạch 10/20/0 · 26a thước → 50/31/55/10
#      87a cột xu  → 「7」「2」 trên hai tấm thẻ · 22a lưới lịch → 「1人」
#    ⇒ Đây là lần thứ MƯỜI của bệnh khối-chung-chọi-mô-tả, và lần này nó chọi với chính
#      GUARD chứ không chọi mô tả cảnh. Câu cấm không thắng được một vật mời gọi.
CHARTS_NUMFREE = [                     # hình khối thuần, không có thang/ô để điền số
    "a small paper bar chart of three bars pinned flat on the background",
    "a paper pie wheel cut from two colours of card leaning against the wall behind",
    # ⛔ BỎ 2026-09-16: 「a paper flow arrow…」 CHIẾM LUÔN KHUNG ở cảnh thuần hình học —
    #    clip_26a trả về HAI mũi tên khổng lồ + vài khối màu, 0 người, 0 vật, không còn
    #    nghĩa gì (user: *"nhiều cái chỉ hiển thị mỗi hình mũi tên"*). Mũi tên là thứ rẻ
    #    nhất model vẽ được nên nó luôn thắng khi cảnh không có chủ thể.
]
CHARTS_SCALED = [                      # CHỈ dùng ở cảnh đã có số thật — chúng mang thang số
    "a row of paper tally marks torn into the background sheet",
    "a column of paper coins stacked as a height chart at the frame edge",
    # 🔴 HẠ XUỐNG ĐÂY vòng 2: "stepped line graph" nghe như hình khối thuần, nhưng biểu đồ
    #    đường thì model tự vẽ TRỤC, và có trục là có vạch chia mang SỐ (clip_22a ra
    #    「15 70 30 / 28 20」). Cùng lý do bar chart vẫn ở kho numfree: cột thì không cần trục.
    "a stepped paper line graph taped across the back wall",
]
# ⛔ BỎ HẲN khỏi cả hai kho, không chỉ hạ xuống SCALED:
#    · nhiệt kế  → model vẽ vạch chia CÓ SỐ (10/20/0) rồi thêm 「75」 đỏ to bên cạnh;
#    · lưới lịch → model điền đầu cột thành chữ Latin giả (「Mon Tue Tue Tue」) ở clip_16a
#      VÀ 「1人」 ở clip_22a — lịch là vật mà chữ/số là LÝ DO TỒN TẠI của nó.
#    Hai vật này mời gọi chữ-số mạnh hơn mọi câu cấm, kể cả khi câu cấm đứng đầu prompt.
CHARTS = CHARTS_NUMFREE + CHARTS_SCALED
_HAS_CHART = re.compile(r"(bar chart|gauge|calendar|stair|balance|timeline|grid|conveyor|"
                        r"channel|hourglass|tally|line graph|pie wheel|thermometer)", re.I)
try:
    _TRUENUM = json.load(io.open(os.path.join(os.path.dirname(__file__),
                                              # 🔴🔴 ĐÃ TỪNG TRỎ SANG `_truenum23.json` — BẢNG SỐ CỦA **VIDEO 23** (bắt 2026-09-15,
    #    user gửi một prompt lỗi). Mọi cụm 「a big numeral X」 trong 82 prompt đều mang con số
    #    của bài KHÁC: cảnh 生年月日 (đúng ra 806.700円) bị gán 「4」 — số đó lấy từ 四月一日
    #    của video 23; cảnh 研究室です bị gán 「60」; cảnh 中村さん 71歳 cũng 「60」.
    #    ⇒ Cùng họ với MOTION_V3 đã bắt hôm qua: **artifact của video 23 khoá theo chỉ số
    #    scene, bê sang video 26 thì sai hết mà không một cảnh báo nào.** Lần thứ CHÍN.
    # 🔴🔴 VÀ DÍNH LẠI LẦN THỨ MƯỜI Ở CHÍNH VIDEO 26 (2026-09-16): phép đổi tên hàng loạt
    #    `nenkin-25`→`nenkin-26` KHÔNG chạm tới chuỗi `_truenum25.json`, nên 26 prompt của
    #    video 26 mang số của video 25 (33.000 · 70.608 · 847.300 · 480 · 420 · 48…).
    #    Prompt vẫn xuất đủ, đúng độ dài, 0 cảnh báo — chỉ lộ khi ĐỌC LẠI prompt đã xuất.
    #    ⇒ Bảng mới sinh bằng `tools/make_truenum26.py` (đọc thẳng timeline của video 26).
    # ⚖️ Bảng mới dựng từ CHÍNH lời đọc video 26, và CHỈ nhận số đi với 円 hoặc か月 —
    #    ngày tháng (四月一日 · 令和八年) bị loại, đúng luật đã ghi ở `check_pace.py`
    #    (「月/年/歳 KHÔNG tính — đó là mốc lịch, không phải con số của bài」).
    "_truenum26.json"), encoding="utf-8"))
except Exception:
    _TRUENUM = {}


# 🔴 CẢNH MÀ SỰ VẮNG MẶT LÀ NGHĨA — cấm cả dàn phụ lẫn biểu đồ.
#    Dính ở beat 104 「生活費の空白」: lời viết *"một hình người nhỏ đứng MỘT MÌNH trong
#    khoảng trống"* rồi lớp làm-giàu nhét thêm ba người và một mũi tên vào đúng chỗ trống đó.
#    Cô độc + khoảng trống chính là thứ cảnh ấy bán. Đây là lần thứ TÁM của bệnh
#    khối-chung-chọi-mô-tả — cứ thêm một lớp tự động là phải hỏi "lớp này huỷ nghĩa của
#    cảnh nào không?".
_SOLO = re.compile(r"(standing alone|alone in|no people in frame|only one|by himself|"
                   r"by herself|a single figure|empty|bare stretch|deserted)", re.I)


def _enrich(body: str, kind: str, scene: int, i: int, close: bool = False) -> str:
    """Thêm dàn phụ · biểu đồ · con số THẬT vào mô tả cảnh."""
    out = body.rstrip(". ")
    solo = bool(_SOLO.search(body))
    # dàn phụ: chỉ cho khung đã có người, không phải ẩn dụ vật thuần, và KHÔNG phải cảnh cô độc
    if kind not in ("META", "GAUGE", "INFOG") and _PPL.search(body)             and "no people in frame" not in body and not solo:
        out += ", and " + _extra_for(close, i)
    # biểu đồ: cảnh nào chưa có quan hệ trực quan thì thêm — trừ cảnh sống bằng khoảng trống
    # 🔴 CHỈ dán biểu đồ vào cảnh ĐÃ CÓ CHỦ THỂ (người hoặc vật thật). Cảnh thuần hình học
    #    (VIZ/META/GAUGE tả bằng cột-vạch-khối) mà dán thêm một hình trừu tượng nữa thì
    #    khung chỉ còn hình trừu tượng — đo được ở clip_26a vòng 1.
    if not _HAS_CHART.search(body) and not solo and _PPL.search(body):
        # cảnh có số THẬT mới được dán vật mang thang số; còn lại chỉ hình khối thuần
        pool = CHARTS if (_TRUENUM.get(str(scene)) or "numeral" in body) else CHARTS_NUMFREE
        out += ", with " + pool[(i * 5) % len(pool)]
    # con số: CHỈ số có thật trong lời đọc của chính cảnh đó
    if "numeral" not in body:
        ns = _TRUENUM.get(str(scene)) or []
        if ns:
            v = f"{ns[-1]:,}"
            out += f", and a big numeral {v} cut from coloured card pasted flat on the background"
    return out + "."


# 🔴 KHUNG QUYẾT ĐỊNH TRƯỚC — máy quay và dàn phụ phải CHỌN THEO NÓ, không rút độc lập.
#    Rút độc lập sinh hai cặp vô lý, đo được trên lô: ③ crop SÁT mà máy "pull-out revealing
#    the FULL scene" (7/92) · ④ crop SÁT mà dàn phụ đứng ở "far background" (2/92).
#    Cùng họ với bẫy "quyết định sớm bằng dữ liệu chưa đủ" đã dính ở khoá `_tbl`.

def _close(body: str, nshot_scene: int, k: int) -> bool:
    """Shot này có phải khung CẮT SÁT không — suy từ chính biến thể bố cục sẽ dùng."""
    if nshot_scene == 1:
        return False
    return _FR(body)[k % 5][1] == "CLOSE"


def _cam_for(kind: str, close: bool, i: int):
    pool = CAM.get(kind, ["static"])
    if close:                      # crop sát thì KHÔNG lùi máy để lộ toàn cảnh
        pool = [c for c in pool if c != "pull_out"] or ["push_in"]
    return pool[i % len(pool)]


def _extra_for(close: bool, i: int) -> str:
    pool = [t for t, far in EXTRAS if not (close and far)]
    return pool[(i * 3) % len(pool)]


def _FR(body: str):
    """Chọn dãy bố cục theo CẢNH CÓ NGƯỜI hay KHÔNG — xem ghi chú ở SHOT_FRAME_OBJ."""
    return SHOT_FRAME if _PPL.search(body) and "no people in frame" not in body         else SHOT_FRAME_OBJ


def merge_prompt(beat, shot) -> str:
    """Gộp prompt POSTER + prompt CHUYỂN ĐỘNG thành MỘT prompt t2v (user chốt 2026-09-12).

    ⚖️ ĐÁNH ĐỔI, ghi thẳng để sau không "phát hiện lại": README của vox-director nói nguyên
       tắc số 1 của nó là *"The look is born in the image step — if the poster isn't a rich
       collage, nothing downstream saves it"*. Đi một bước t2v là **mất cửa duyệt poster
       trước khi animate**: hỏng chất giấy thì chỉ biết sau khi clip đã ra. Đổi lại: 92 lượt
       gen thay vì 92 ảnh + 92 i2v, và không phải upload ảnh làm start-frame.
       ⇒ Bù bằng LOT1: gen 10 clip phủ đủ khuôn, soi chất giấy, rồi mới chạy 82 cái còn lại.

    🔴 BA CÂU PHẢI BỎ khi gộp — chúng đều GIẢ ĐỊNH CÓ ẢNH ĐẦU VÀO, giữ lại là prompt tự nói
       về một tấm ảnh không tồn tại (đúng bệnh "khối chung chọi mô tả" đã dính 4 lần):
         · "Animate this still into …"            → đổi thành lời khai đây là shot ĐỘNG
         · "Animate the motion only; don't re-render the picture."  → bỏ
         · AESTHETIC + COLOR của khối motion      → bỏ, khối collage đã tả giàu hơn hẳn
    """
    kf = shot["keyframe_prompt"].strip()
    tail = " Aspect ratio 16:9."
    if kf.endswith(tail):
        kf = kf[: -len(tail)]

    cam = elem = feel = guard = ""
    for ln in shot["motion_prompt"].split("\n"):
        ln = ln.strip()
        if ln.startswith("CAMERA"):
            cam = ln
        elif ln.startswith("ELEMENT MOTION"):
            elem = ln
        elif ln.startswith("FEEL:"):
            feel = ln
        elif ln.startswith("CONSTRAINTS:"):
            guard = ln.replace(" Animate the motion only; don't re-render the picture.", "")
    out = ("A mixed-media paper-collage MOTION GRAPHIC — a MOVING SHOT, not a still image; "
           "everything in frame is printed, hand-cut paper, never photoreal live action. "
           f"{kf} {cam} {elem} {feel} {guard} Aspect ratio 16:9.")
    # 🔴 Hai cụm SÓT LẠI của đường hai-bước, quét ra 92/92: cả hai đều trỏ tới một tấm ảnh
    #    không tồn tại trong t2v. Dịch sang ngôn ngữ VIDEO, đừng để prompt tự nói về poster.
    # 🔴 "Keep the layout stable" là guard của `constraints: strict`, viết cho explainer
    #    NHIỀU CHỮ. Ở biên độ `max` (*"elements burst, scatter and fly boldly"*) nó chọi thẳng
    #    — bảo bung toé rồi lại bảo giữ nguyên bố cục. Bỏ ĐÚNG câu đó, GIỮ ba guard còn lại
    #    (phẳng 2D · không xoay 3D · giấy cứng không morph/melt) vì chúng bảo vệ chất giấy.
    # 🔴🔴 CÂU NÀY LÀ THỦ PHẠM CHÍNH CỦA "GIẬT GIẬT" (bắt 2026-09-14, user chỉ):
    #    `clips.py` dán cứng 「Elements move as paper cut-outs (slide, flap, hinge, pop,
    #    scatter, fly).」 — nó **bảo thẳng model cho giấy bay và pop**, đúng hai thứ user nói
    #    showcase KHÔNG có. Mọi công sửa ở kho motion đều vô ích khi câu này còn đứng đó.
    #    ⇒ Thay bằng câu mô tả đúng cái đo được: khớp nối chuyển động mượt, biên vẫn là giấy.
    out = out.replace(
        "Elements move as paper cut-outs (slide, flap, hinge, pop, scatter, fly).",
        "The figures and objects are paper cut-outs animated LIKE PUPPETS — limbs, hands and "
        "held objects hinge and swing on smooth arcs at one steady speed, the way a cut-paper "
        "puppet animation moves. The paper accents and the background hold their places while "
        "the people and the objects they handle carry all of the movement.")
    # ══════════════════════════════════════════════════════════════════════════
    # 🔴🔴 SỬA "KHÔ" — 2026-09-14, sau khi ĐO 10 clip test đầu tiên cạnh showcase.
    #   clip tao:  sáng 180-199 · bão hòa 64-113 · biên 21-33% · RẬM KẾT CẤU 14.000-27.000
    #   showcase:  sáng 147-175 · bão hòa 100-108 · biên 16-19% · rậm  3.500- 4.400
    # ⇒ Chênh 4-7 lần ở "độ rậm" là cái user gọi là KHÔ: nền của tao là **một bức tường chữ
    #   báo Nhật dày đặc**, nhân vật bé đứng giữa; showcase là **MỘT mảng màu phẳng lớn** với
    #   nhân vật TO cắt ngang khung.
    # 🔴 Và nền chữ báo còn phá thẳng GUARD ② ("no Japanese lettering anywhere"): chữ Nhật giả
    #   phủ kín nền ở 10/10 clip. Chuỗi STYLE đòi `aged broadsheet newspaper page` còn guard
    #   cấm chữ — hai câu chọi nhau, và STYLE thắng. Lần thứ TÁM của bệnh khối-chung-chọi-nhau.
    # ⇒ Bỏ nền báo, thay bằng MẢNG MÀU PHẲNG. Hết nền báo là hết chữ giả, và hết luôn 4-7 lần
    #   độ rậm thừa.
    for a, b in [
        ("laid over an aged broadsheet newspaper page, heavy halftone print dots, aged "
         "newsprint texture with slight ink misregistration",
         "laid over ONE large flat field of deeply saturated colour that fills the whole "
         "background, with at most one small torn paper scrap as an accent, and any such scrap "
         "shows only abstract grey rules and blocks, never readable characters"),
        ("on a bold flat aged cream newsprint paper background",
         "on one bold flat field of deeply saturated colour"),
        ("Halftone print dots, newspaper-clipping scraps, paper-stencil shapes, aged paper "
         "texture, slight print misregistration, scattered geometric paper accents",
         "A few large paper-stencil shapes and a small number of bold geometric paper accents"),
        ("Print finish: aged paper, heavy halftone dots, high contrast, slight print "
         "misregistration.",
         "Print finish: rich saturated ink on flat colour, deep shadows, high contrast. "
         "The background is one clean flat colour field — no printed text, no newspaper "
         "columns, no dense pattern behind the figures."),
        ("Palette: cream white, deep red, mustard yellow, charcoal black.",
         "Palette: one dominant deeply saturated ground colour plus deep red, mustard yellow "
         "and charcoal black; rich ink coverage, mid-dark overall, never pale or washed out."),
    ]:
        out = out.replace(a, b)
    # 🔴 NHÂN VẬT PHẢI TO. Đo showcase: hai người choán gần trọn khung (cắt ngang đùi).
    #    Clip tao để người bé giữa khung ⇒ mắt không có gì để bám, và đó là nửa còn lại của "khô".
    out += (" The main figures are LARGE: they fill most of the frame height and are cropped by "
            "the frame edges, the way a close poster crop works."
            # 🔴🔴 SỬA VÒNG 3 (2026-09-14) — hai câu vòng trước làm KHUNG RỖNG:
            #   「few big bold shapes rather than many small busy ones」 + 「background stay
            #   still and settled」 ⇒ model dựng một sân khấu TRỐNG rồi cho đồ bay vào lắp dần.
            #   Đo được: MAD tụt 9,4 → 6,6 (showcase 21,9) và frame đầu của task_004 gần như
            #   rỗng. Đúng cái user gọi là *"nền không nổi bật, chuyển động như robot"*.
            # ⭐ Đếm showcase: MỘT khung có ~15 vật (5 người + bàn + đèn + bóng + 2 tờ báo +
            #   biển tiêu đề + 6 hình trang trí) — DÀY, và **đầy đủ ngay từ frame 1**.
            # 🔴🔴 SỬA VÒNG 4 (2026-09-16) — ĐO 10 clip LOT1 của video 26: **MAD 1,2–2,25 ở
            #   10/10 clip** (showcase 21,9 · mốc vòng 3 là 9,4). User: *"nhiều video ít
            #   chuyển động"*. Hai câu 「the arrangement never changes」 + 「Nothing enters the
            #   frame and nothing leaves it」 viết để chặn đồ BAY VÀO, nhưng model đọc thành
            #   **"dựng một tấm poster TĨNH"** — và chúng đứng ở ~78% prompt, tức SAU mọi lời
            #   xin chuyển động, nên chúng thắng. Giữ ý đồ (không có gì bay vào/ra) nhưng
            #   nói thẳng: BỐ CỤC đứng yên, PHẦN TỬ thì không bao giờ đứng yên.
            " THE LAYOUT IS COMPLETE IN THE VERY FIRST FRAME: every person, object and paper "
            "accent is already in place when the shot opens — nothing flies in from outside the "
            "frame and nothing leaves it. Fill the frame richly — around a dozen distinct "
            "cut-out elements, layered and overlapping, so no large area of bare background is "
            "left empty. BUT NOTHING IN THE FRAME IS EVER STILL: from the first frame to the "
            "last, every figure and every object it handles is in continuous motion on the "
            "spot — arms and heads hinging through wide arcs, held objects swinging, turning "
            "and tilting across a large part of the frame — while each element keeps its own "
            "place in the layout. There is never a moment where the picture holds as a static "
            "poster.")
    # ══════════════════════════════════════════════════════════════════════════
    # 🎨 KHỐI TẢ NHÂN VẬT (thêm 2026-09-14, user: *"tao muốn vẽ nhân vật đẹp hơn tí"*).
    # Soi 1:1 nhân vật của lô test cạnh showcase:
    #   của tao   — áo quần gần như KHÔNG MÀU (xám/trắng nhợt), PHẲNG LÌ không sáng tối,
    #               nét viền mảnh, mặt nhợt ⇒ nhân vật CHÌM vào nền dù nền đã đậm.
    #   showcase  — áo đỏ thẫm / xanh lục đậm bão hoà, CÓ khối và nếp gấp, nét mực dứt khoát,
    #               ngũ quan rõ. Bão hoà 141 đo được của tao là do NỀN, không phải người.
    # 🔴 Chuỗi STYLE cũ chỉ nói "printed / illustrated cut-out … keep print grain" — đó là tả
    #    CHẤT LIỆU, không tả TAY NGHỀ VẼ. Thiếu hẳn một khối nói người được vẽ NHƯ THẾ NÀO.
    # ⚠️ Cố ý KHÔNG dùng chữ "lighting/3D/render" — guard phẳng-2D vẫn phải đứng; đổ bóng ở
    #    đây là bóng KIỂU IN (mảng phẳng + nét gạch), không phải bóng vật lý.
    out += (" CHARACTER ART — draw the people with real craft, the way a mid-century Japanese "
            "editorial illustrator of the 1970s would: a confident dark ink outline around every "
            "figure; "
            "faces with clearly drawn features and warm skin tone, expressive and specific "
            "rather than blank; hair and eyebrows in solid dark ink. Their clothing is in RICH "
            "SATURATED colour — deep indigo, crimson, forest green, warm ochre — with woven "
            "pattern printed into the cloth, so the figures read strongly against the flat "
            "background instead of fading into it. Give the cloth form with printed shading: "
            "flat shadow shapes and fine hatching in the folds, at the cuffs and under the "
            "collar, the way a printed poster shades. Hands are properly drawn with separate "
            # 🔴 ĐO 2026-09-16: 4/4 clip có người trả về **kimono + nét mộc bản Edo** (浮世絵).
            #    Khối cũ chỉ nói "mid-century Japanese editorial illustrator" — KHÔNG ghim
            #    thời trang, nên model trôi về tranh khắc gỗ; và guard của beats chỉ cấm
            #    "Western / American / 1950s retro", vô tình chừa đúng cửa Edo.
            "fingers. The figures are the richest, most detailed, highest-contrast thing in "
            "the frame. Everyone wears ORDINARY MODERN JAPANESE DAYWEAR — cardigan, knitted "
            "vest, plain blouse or shirt, slacks or a simple skirt, a kitchen apron, a light "
            "jacket, flat everyday shoes or slippers. The drawing style is printed editorial "
            "illustration, not a woodblock print: no kimono, no yukata, no hakama, no obi, no "
            "traditional topknot or Edo hairstyle, no ukiyo-e or Edo-period woodcut look "
            "anywhere.")
    # ══════════════════════════════════════════════════════════════════════════
    # 🔴🔴 GUARD SỐ PHẢI CÓ ĐIỀU KIỆN — bắt 2026-09-15 khi soi 10 clip vừa gen.
    #    Câu 「NUMERALS ARE WANTED: where the scene names a figure…」 là VÔ ĐIỀU KIỆN, và
    #    model đọc thành *"cảnh nào cũng nên có số to"* rồi BỊA: clip_9b hiện 60 · clip_49a
    #    hiện 05 · clip_52a hiện 4 · clip_112b hiện 75 75 — trong khi cả 4 cảnh đó KHÔNG có
    #    con số nào trong lời đọc. Đúng cảnh DUY NHẤT được phép có số (clip_65a) thì nó vẽ
    #    chuẩn 806,700 ⇒ model làm được, chỉ là mình chưa nói rõ khi nào KHÔNG.
    # ⚖️ Ở kênh YMYL tiền hưu, một con số to SAI trên màn hình là lỗi nặng nhất — nặng hơn
    #    khô, hơn giật. Nên guard tách làm hai nhánh theo CHÍNH cảnh đó.
    # 📌 Cùng khuôn với chính sách PAIR/ONE/NONE đã phải làm ở video 22 (CLAUDE.md §② mục 12).
    OLD_NUM = ("NUMERALS ARE WANTED: where the scene names a figure, cut it as BIG bold Arabic "
               "numerals from coloured card with visible scissor edges, pasted flat onto the "
               "page — they are a core part of this collage language, not decoration. But ")
    scene_txt = out.split("SCENE (as layered paper cut-outs):")[1].split("Any person shown")[0]         if "SCENE (as layered paper cut-outs):" in out else ""
    import re as _re
    _n = _re.findall(r"numeral ([\d,]+)", scene_txt)
    if _n:
        want = " and ".join(_n)
        # 🔴 ĐÁNH VẦN TỪNG CHỮ SỐ + cấm bản sao — đúng bài học vòng 2/3 của video 22
        #    (CLAUDE.md §② mục 12). Viết "SẮC NÉT" không đủ: crisp ≠ correct.
        spell = " and ".join(" ".join(x) for x in _n)
        # 🔴 ĐẾM SỐ CHỮ SỐ — đòn bẩy MỚI của vòng 3. Hai vòng trước đã thử "sắc nét" rồi
        #    "đánh vần từng chữ số" mà clip_36a vẫn ra 「130 000」 méo rồi 「13,000」 (RỚT
        #    một số 0). Đánh vần nói THỨ TỰ nhưng không nói ĐỘ DÀI, nên mất một ký tự thì
        #    chuỗi vẫn "đúng thứ tự". Thêm phép đếm là thêm một ràng buộc kiểm được.
        _dig = sum(c.isdigit() for x in _n for c in x)
        NEW_NUM = (f"EXACTLY ONE FIGURE IS ALLOWED IN THIS SHOT: the numeral {want}, cut as BIG "
                   "bold Arabic numerals from coloured card with visible scissor edges and "
                   f"pasted flat onto the page. Spell it out digit by digit: {spell} — every "
                   "digit present and in that order, with a comma as the thousands separator, "
                   f"never a full stop. Count them: {_dig} digits in total, so do not drop a "
                   "digit and do not add one. It appears ONCE only, in a clear area of the "
                   "page: it stands completely clear of every figure, prop and paper edge, and "
                   "no hand, tool, tape strip, torn edge or other cut-out overlaps, crosses or "
                   "covers any part of it. No other number, digit, tally mark, scale, dial or "
                   "counter appears anywhere in the frame. ")
        SHORT = f"Again: the numeral {want} appears once, unobscured, and no other digit exists in the frame. "
    else:
        NEW_NUM = ("NO FIGURES IN THIS SHOT: there is not a single digit anywhere in the frame — "
                   "no numerals, no dates, no prices, no page numbers, no tally marks, no ruler "
                   "or gauge markings, no clock or calendar faces bearing numbers. Every card, "
                   "sign, document, screen, dial and label surface is completely blank. ")
        SHORT = "Again: not one digit and not one letter anywhere in the frame. "
    # 🔴🔴 GUARD PHẢI ĐỨNG ĐẦU PROMPT, KHÔNG NẰM GIỮA — bắt 2026-09-15.
    #    Nhánh CẤM SỐ viết đúng từ vòng trước mà model vẫn vẽ 「75」「1人」「7」「2」, và câu
    #    cấm khi đó nằm ở ~55% độ dài prompt. Đây đúng cơ chế đã đo ở thumbnail
    #    (`ab-3title-3thumb.md` §3.1 Bước 3): **khối chữ đặt sau một loạt khối tả cảnh thì
    #    model bám tả cảnh và nuốt mất chỉ thị về chữ.** Ở đó gate là "TEXT trong 15% đầu";
    #    ở đây cùng một gate, cùng một lý do, chỉ đổi từ "xin chữ" sang "cấm chữ".
    #    ⇒ Đưa nguyên khối lên ngay sau câu khai mở, giữ một câu nhắc lại ở chỗ cũ.
    out = out.replace(OLD_NUM, SHORT)
    # 🔴🔴 VÒNG 2 (2026-09-15 khuya): hoist RIÊNG luật SỐ vẫn chưa đủ — 2/5 clip gen lại
    #    (30a · 87a) trả về NGUYÊN MỘT TƯỜNG BÁO đầy chữ Nhật GIẢ đọc được, có cả biển hiệu
    #    「曲業グッド会」 to giữa khung. Câu cấm chữ và câu "nền là một mảng màu phẳng" vẫn
    #    nằm ở 43% và 30% độ dài prompt — tức đúng cái vừa sửa cho luật số, nhưng cho luật
    #    CHỮ thì chưa sửa. ⇒ Gom CẢ BA (số · chữ · nền) vào MỘT khối đứng đầu.
    # 🔴 Vì sao 62 clip trước không dính mà đúng hai cái này dính: cả hai là cảnh MỎNG
    #    (3 phần tử), trong khi khối bố cục đòi "around a dozen distinct cut-out elements,
    #    no large area of bare background left empty" ⇒ model lấp chỗ trống bằng thứ rẻ nhất
    #    của phong cách này: giấy báo có chữ. **Cảnh càng ít vật thì áp lực bịa chữ càng cao.**
    _w0 = out.find("NO WORDS in any language")
    _w1 = out.find("Leave a narrow empty strip")
    WORDS = out[_w0:_w1].strip() if 0 <= _w0 < _w1 else ""
    if WORDS:
        out = out[:_w0] + "No words on any surface. " + out[_w1:]
    BG = ("The background behind everything stays ONE plain flat colour field and never "
          "becomes a printed newspaper page: no columns of type, no headlines, no printed "
          "sheets papering the wall. Any torn newsprint scrap is small and shows only "
          "abstract grey rules and blocks, never readable characters. Fill the frame with "
          "cut-out figures, objects and plain geometric paper shapes — never with text.")
    # 🔴🔴 VÒNG 4 (2026-09-16) — **CÙNG ĐỊNH LUẬT, LỚP CHƯA ĐƯỢC ÁP.** Vòng 2 đã nâng
    #    guard CẤM (số · chữ · nền) lên đầu prompt và nó ăn ngay. Nhưng khối XIN CHUYỂN
    #    ĐỘNG vẫn nằm ở **58–65%** độ dài prompt, và đo 10 clip LOT1 video 26 ra
    #    **MAD 1,2–2,25 / 10 clip** (showcase 21,9). ⇒ Nâng nốt nó lên đầu, để lại một câu
    #    nhắc ở chỗ cũ — y hệt cách đã làm cho khối số.
    #    📌 Bài học: "đưa lên đầu" là luật của MỌI chỉ thị phải được tuân, không riêng CẤM.
    # 🔴🔴 BẮT 2026-09-16 khi user dán một prompt ra đọc — MỘT lỗi đẻ ra BA triệu chứng,
    #    và cả ba đều IM LẶNG (prompt vẫn đủ độ dài, mọi gate cũ vẫn xanh):
    #    ① Câu GIẬT 「Elements move as paper cut-outs (slide, flap, hinge, pop, scatter,
    #       fly).」 nằm ở **ĐUÔI dòng ELEMENT MOTION**, nên `out.replace(...)` ở trên chỉ
    #       dọn được bản trong THÂN — bản hoist lấy `elem` RAW nên nó sống lại ở 61/61
    #       prompt, tức đúng câu docstring khoe là "đã bỏ".
    #    ② Vì `out` đã bị sửa (câu giật → câu PUPPET) nên `elem` không còn khớp `out`
    #       ⇒ `out.replace(elem, SHORT, 1)` **trượt 61/61**, câu nhắc ngắn chưa bao giờ xuất
    #       hiện ⇒ khối chuyển động bị **lặp NGUYÊN VĂN hai lần** (SUSTAIN đếm được 122 lần).
    #    ③ Khớp-chuỗi-chính-xác là cách sai để gỡ một khối đã qua tay nhiều phép replace.
    #    ⇒ Làm sạch `elem` TRƯỚC, rồi CẮT KHỐI theo mốc đầu/cuối thay vì so chuỗi.
    _JERK = "Elements move as paper cut-outs (slide, flap, hinge, pop, scatter, fly)."
    _em = elem.split(":", 1)[1].strip() if ":" in elem else elem
    _em = _em.replace(_JERK, "").strip()
    # 🔴 CHIA LÀM HAI: câu CHỐT đứng TRƯỚC khối cấm (1%), phần chi tiết đứng NGAY SAU nó.
    #    Nhét cả khối chuyển động lên trước thì guard 「NO WORDS」 bị đẩy từ 12% xuống 23%,
    #    tức phá đúng cái vòng 2 vừa sửa được. Hai chỉ thị cùng cần chỗ đầu ⇒ cái NGẮN đi
    #    trước, cái DÀI đi ngay sau khối cấm.
    MOVE_HEAD = ("THIS IS A MOVING SHOT, NOT A POSTER: every figure and every object moves "
                 "without pause from the first frame to the last, and is still moving as the "
                 "shot ends. ")
    MOVE = ("MOVEMENT IN DETAIL — the movement is the point of this shot. Arms, heads and held "
            "objects hinge, swing and travel through WIDE arcs that cross a large part of the "
            "frame, at one smooth steady speed. There is no moment where the picture settles "
            "into a still poster. " + _em)
    # cắt khối ELEMENT MOTION gốc (từ nhãn tới mốc " FEEL:") — không so chuỗi
    _i, _j = out.find("ELEMENT MOTION"), out.find(" FEEL:")
    if 0 <= _i < _j:
        out = (out[:_i] + "Again: nothing in the frame is ever still — the movement runs wide "
               "and unbroken all the way to the last frame." + out[_j:])
    out = out.replace(_JERK, "")
    POLICY = " ".join(x for x in (MOVE_HEAD.rstrip(), NEW_NUM.rstrip(), WORDS, BG,
                                  MOVE.rstrip()) if x)
    _A = "never photoreal live action."
    if _A in out:
        out = out.replace(_A, _A + " " + POLICY + " ", 1)
    else:
        out = POLICY + " " + out
    # 🔴 Đuôi câu guard chữ vẫn nói 「apart from those cut-out numerals」 — ở nhánh CẤM SỐ thì
    #    đó là tự chọi ngay trong một câu. Sửa đuôi theo đúng nhánh.
    if not _n:
        out = out.replace("stays blank apart from those cut-out numerals",
                          "stays completely blank")
    # 🔴 "Aspect ratio 16:9." do vox-director dan o cuoi khoi CONSTRAINTS, nhung minh con
    #    noi them 3 khoi (khung/bo cuc/nhan vat) SAU do ⇒ ty le nam giua cau. Dua ve cuoi.
    out = out.replace(" Aspect ratio 16:9.", " ") + " Aspect ratio 16:9."
    # 🔴 Guard 「ONE continuous move that does not loop, retract or reset」 viet cho CU MAY,
    #    nhung minh yeu cau phan tu 「keeps ... over and over」 ⇒ hai cau choi nhau. Thu hep
    #    guard ve dung pham vi cua no.
    # 🔴 29/61 prompt vừa nói 「a locked-off static camera (no camera move)」 vừa nói
    #    「The camera makes one continuous move」. Guard này viết cho cú máy ĐỘNG; ở cú máy
    #    TĨNH nó là câu tự chọi ⇒ đổi theo đúng loại cú máy của shot.
    _STATIC = "locked-off static camera" in out
    out = out.replace("ONE continuous move that does not loop, retract or reset.",
                      "The camera holds completely still for the whole shot." if _STATIC else
                      "The camera makes one continuous move that does not retract or reset.")
    # ⛔ Câu của vox-director nhắc tới HEADLINE trong một bài đã CẤM mọi chữ — bỏ hẳn.
    out = out.replace("No big headline in this shot (a small accent only); it is a cut-in "
                      "detail. ", "")
    return (out.replace("Keep the layout stable. ", "")
               .replace("anywhere in the image", "anywhere in the frame")
               .replace("camera parallel to the poster",
                        "the camera parallel to the flat paper surface"))


def sync(doc):
    """Chạy print_prompts + print_motion, rồi copy prompt + sinh TENFILE/LOT vào folder video."""
    import shutil
    import subprocess
    for tool in ("print_prompts.py", "print_motion.py"):
        r = subprocess.run([sys.executable, os.path.join("scripts", tool), "out/nenkin-26"],
                           cwd=VOX, capture_output=True, text=True)
        if r.returncode:
            print(f"🔴 {tool} lỗi:\n{r.stdout}\n{r.stderr}")
            sys.exit(1)

    doc = json.load(io.open(os.path.join(OUT, "beats.json"), encoding="utf-8"))
    shots = [(b, s, f"{b['id']}{s['id']}") for b in doc["beats"] for s in b["shots"]]

    os.makedirs(VD, exist_ok=True)
    shutil.copyfile(os.path.join(OUT, "beats.json"), os.path.join(VD, "vox26_beats.json"))

    # ── GỘP THÀNH MỘT PROMPT t2v DUY NHẤT (user chốt 2026-09-12) ──────────────
    merged = [merge_prompt(b, s) for b, s, _k in shots]
    io.open(os.path.join(VD, "vox26_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(p.replace("\n", " ") for p in merged) + "\n")

    # 🔴 TENFILE — vox-director KHÔNG sinh cái này, mà thiếu nó là hỏng đúng chỗ đã dính ở
    #    lô i2v video 22: *"Tên clip Flow KHÔNG mang shot-id, nó là caption sinh từ prompt"*
    #    ⇒ không có sổ dòng↔tên file thì lúc ingest phải map lại bằng mắt cả lô.
    io.open(os.path.join(VD, "vox26_TENFILE.txt"), "w", encoding="utf-8").write("\n".join(
        f"dong {i+1:>3} -> clips/clip_{k}.mp4   [beat {b['id']:>3} · "
        f"{b['title_en'].split('· ')[1]:<6} · {s['shot_size']:<6} · {s['camera_move']:<9} · "
        f"{s['dur']:>4.1f}s]  {b['title_cn']}"
        for i, (b, s, k) in enumerate(shots)) + "\n")

    md = ["# vox26 — prompt LỚP HÌNH video 26 (paper-collage, MỘT prompt/clip)", "",
          f"**{len(shots)} clip** · theme `newsprint-editorial` · 16:9 · t2v một bước "
          "(poster + chuyển động gộp chung, không có khâu ảnh trung gian).", "",
          "Bơm `vox26_FLOW.txt` vào extension theo đúng thứ tự; lưu ra tên ở "
          "`vox26_TENFILE.txt`. Loại ngay clip nào ra chất phim thật, có chữ, hoặc xoay 3D.",
          ""]
    for i, ((b, s, k), p) in enumerate(zip(shots, merged), 1):
        md += [f"### {i}. `clips/clip_{k}.mp4` — {b['title_cn']}  "
               f"({b['title_en'].split('· ')[1]} · {s['shot_size']} · {s['camera_move']} · "
               f"{s['dur']:.1f}s)", "", "```", p, "```", ""]
    io.open(os.path.join(VD, "vox26_PROMPTS.md"), "w", encoding="utf-8").write("\n".join(md))

    # ── LOT1: gen THỬ trước, phủ đủ mọi khuôn ────────────────────────────────
    # Lô 16 clip của video 21 hỏng CẢ LÔ vì lỗi cấp khuôn; ở collage rủi ro còn cao hơn vì
    # nếu poster không ra chất giấy thì KHÔNG khâu nào phía sau cứu được (README vox-director).
    # 🔴 LÔ DUYỆT PHẢI GHIM CỨNG, KHÔNG ĐƯỢC TỰ CHỌN LẠI MỖI LẦN CHẠY.
    #    Bản đầu chọn "scene đầu tiên của mỗi khuôn" ⇒ sửa nội dung làm khuôn đổi ⇒ LÔ ĐỔI
    #    THÀNH PHẦN theo. Vá 5 vòng vẫn không hội tụ: vá xong lô lại chọn cảnh chưa vá.
    #    Lô mà user đang duyệt thì phải đứng yên, nếu không "duyệt OK" chẳng nói về cái gì cả.
    #  0 SPLIT · 1 CROWD · 5 META · 6 PERSON · 10 DESK · 12 HOLD · 26 VIZ ·
    # 35 PERSON(cast 中村) · 38 GAUGE · 46 META  => phu DU 8 khuon cua video 26.
    LOT1_SCENES = [0, 1, 5, 6, 10, 12, 26, 35, 38, 46]
    lot, seen = [], {}
    for i, (b, s, k) in enumerate(shots):
        kd = b["title_en"].split("· ")[1]
        if b["id"] in LOT1_SCENES and b["id"] not in [x[1]["id"] for x in lot]:
            seen[kd] = 1
            lot.append((i, b, s, k))
    io.open(os.path.join(VD, "vox26_LOT1.txt"), "w", encoding="utf-8").write(
        "\n".join(merged[i].replace("\n", " ") for i, _b, _s, _k in lot) + "\n")
    io.open(os.path.join(VD, "vox26_LOT1_TENFILE.txt"), "w", encoding="utf-8").write("\n".join(
        f"dong {j+1:>2} -> clips/clip_{k}.mp4   [beat {b['id']} · "
        f"{b['title_en'].split('· ')[1]} · {s['shot_size']} · {s['dur']:.1f}s]  {b['title_cn']}"
        for j, (_i, b, s, k) in enumerate(lot)) + "\n")

    L = [len(p) for p in merged]
    print(f"\n📁 ĐÃ ĐỔ VỀ {VD}")
    print(f"   vox26_FLOW.txt        {len(merged):>3} prompt — MỘT prompt/clip (poster + "
          f"chuyển động gộp chung), {min(L)}–{max(L)} ký")
    print(f"   vox26_TENFILE.txt         sổ dòng ↔ clips/clip_<key>.mp4")
    print(f"   vox26_LOT1.txt            {len(lot)} shot GEN THỬ TRƯỚC (đủ "
          f"{len(seen)} khuôn: {' '.join(seen)})")
    print(f"   vox26_PROMPTS.md · vox26_beats.json")


if __name__ == "__main__":
    main()
