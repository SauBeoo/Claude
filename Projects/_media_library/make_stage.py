# -*- coding: utf-8 -*-
r"""
make_stage.py — SÂN KHẤU CỐ ĐỊNH + BUILD-ON ANIMATION, kiểu 「お金の保健室」.
v0.2 · 2026-08-08 (v0.1 chỉ ra ảnh tĩnh; user: "tao muốn nó chuyển động như video vox").

VÌ SAO CÓ TOOL NÀY (đọc trước khi sửa)
────────────────────────────────────────────────────────────────────────────────
Đo storyboard 175 frame của video 152.452 view (`bRwKrvXxD3o`, 29 phút): **cả video chỉ có
ĐÚNG MỘT bố cục**. Không phải slideshow trộn ảnh/diagram/card như pipeline hiện tại —
mà là một sân khấu: 2 nhân vật đứng cố định hai mép, giữa là MỘT TẤM BẢNG đổi nội dung,
đáy là thanh phụ đề đen 1 dòng. Nhận diện tức thì; lướt 1 giây biết là kênh nào.

🔴 CHUYỂN ĐỘNG Ở ĐÂY LÀ *BUILD-ON*, KHÔNG PHẢI CAMERA
────────────────────────────────────────────────────────────────────────────────
Khung KHÔNG pan, KHÔNG zoom, KHÔNG Ken Burns (luật kênh: `feedback_video_no_motion...`).
Cái động duy nhất là **phần tử hiện dần theo lời đọc** — đúng thứ đối thủ làm và đúng
thứ giữ mắt người 60+: họ nhìn thấy câu trả lời được LẮP RA, không phải màn hình trôi.
  · sân khấu (nền + card + 2 nhân vật) có mặt từ frame 0, đứng yên tuyệt đối
  · tiêu đề → các phần tử → mũi tên/khoanh: mỗi thứ trượt lên 26px + hiện dần 0,42s
  · hết chuỗi build-on thì **ĐỨNG IM** tới hết clip (tpad clone frame cuối)

⚠️ CLIP DÀI 30s VÀ CUE KHÔNG BAO GIỜ >30s → renderer không bao giờ loop lại.
   Nếu loop, build-on sẽ chạy lại từ bảng trống = hỏng nhịp. Giống luật của make_vox.py.

BỐ CỤC 1920×1080
────────────────────────────────────────────────────────────────────────────────
    ┌──────┬────────────────────────────────────────────────┬──────┐  y=0
    │ 先生 │  ╭──────── CARD trắng, bo 28, đổ bóng ───────╮  │ 生徒 │
    │(trái)│  │  TIÊU ĐỀ (navy, Black, canh giữa)         │  │(phải)│
    │      │  │  ── thân bảng theo `layout`, hiện dần ──  │  │      │
    │      │  ╰────────────────────────────────────────────╯  │      │  y=902
    ├──────┴────────────────────────────────────────────────┴──────┤  y=928
    │ ███████ dải phụ đề (renderer burn đè, tool chỉ CHỪA CHỖ) ████ │
    └───────────────────────────────────────────────────────────────┘  y=1080

5 LAYOUT (đủ phủ những gì đối thủ dùng trong 29 phút)
────────────────────────────────────────────────────────────────────────────────
  check    ✓/✗  cái ĐƯỢC và cái KHÔNG nằm cùng khung (✗ xám mờ) — layout đắt nhất
  flow     3 hộp + mũi tên vẽ dần, có băng thời gian phía trên
  compare  2 panel đối nhau + 2 dòng chốt phía dưới
  timeline trục ngang, thanh tiến trình chạy + các chặng
  source   thẻ 原典: tên cơ quan + tên văn bản đầy đủ (lớp genten, `handmade-layer.md`)
  pict     1–3 panel màu: label + ẢNH AI TO — style 節約看護師りょう (thêm 2026-08-19, đo từ
           video 6DN88wQyBFg 970K view). Cùng lượt: keyword màu 《…》 trong title/cap/label ·
           pin "badge" (punch tròn đặc màu) · khoá "beats"/"beat" = phần tử pop theo GIÂY THẬT
           của lời đọc (đo được 3–6s/pop ở kênh mẫu) — thiếu khoá thì nhịp dồn cũ giữ nguyên

CHẠY
────────────────────────────────────────────────────────────────────────────────
    python make_stage.py demo <out_dir>                  # 4 clip mẫu + contact sheet
    python make_stage.py clip out.mp4 --spec spec.json   # 1 clip 30s
    python make_stage.py still out.png --spec spec.json  # 1 khung tĩnh (frame cuối)

✅ TRẠNG THÁI 2026-08-09 — dùng thật được
────────────────────────────────────────────────────────────────────────────────
  1. ✅ style phụ đề `bar` đã có trong `video_render.py::SUB_STYLES`; `maxlen` tự siết 26
     (luôn 1 dòng). Hồ sơ kênh nenkin đã đổi `sub_style: "bar"`.
  2. ✅ Bộ nhân vật riêng: `sensei_*` 8 · `kikite_*` 8 · `josei_*` 8 + 28 icon
     (`assets/icons/`). Prompt + bài học ở `youtube-jp-nenkin/04_CAST_STAGE_PROMPTS.md`.
  3. ✅ `python make_stage.py slides <clips_dir> --slides <SLIDES.json>` → `clip_XX.mp4`
     + `.sig` (resume theo nội dung + mtime cast) + `_stage_sheet.jpg` để duyệt mắt.
     KHÔNG phải mổ renderer — entry chỉ cần `{"video": true, "stage": {...}}`.
  ⚠️ Preflight của `video_render.py` đã vá cùng lượt: video 100% clip thì KHÔNG đòi folder
     ảnh nữa (trước đó chặn oan, vì sân khấu không có ảnh nào).
"""
import io, sys, json, math, copy, shutil, hashlib, argparse, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

W, H = 1920, 1080
FPS = 30
CLIP_SEC = 30.0
VERSION = "stage-2.8"   # 2.8 (2026-09-06): pin `frame` (khung do MOC DAN quanh khoi chu 原典, toa do tu genten_boxes.json — thay `circle` vi ellipse bet an vao dong tren/duoi) + pin `quote` (trich nguyen van duoi anh, keyword 《》 do, chu do FONT ve nen sac net) — do tu フクロウ 1,63M. Ca hai OPT-IN: the cu khong khai thi khong doi mot pixel; bump VERSION chi de truy vet, video da xong khong ai dung lai nen khong ton gi.   # 2.7 (2026-08-26): icon_path() doc CAST.parent thay vi ICON_DIRS[0] dong bang luc import — moi kenh KHAC nenkin truoc do khong bao gio tim thay sticker rieng-kenh (roi vao stage_icons dung chung hoac None), im lang, khong bao loi   # 2.6 (2026-08-26): build_end tinh ca props/props_top t0 + _sig ghi file icon cua props (missing/mtime) — sticker okura-demo gan theo loi khong con bi cat/khong rebuild im lang   # 2.5 (2026-08-25): pins_card beat chia PACE (truoc bi tre 1,35x nen sticker khong hien)   # 2.4 (2026-08-25): build_end tinh ca `pins_card` — sticker beat muon khong con bi cat mat   # 2.3 (2026-08-25): `pins_card` — sticker chu/so (badge/stamp/num+burst) dung duoc o MOI layout, khong chi art   # 2.2 (2026-08-25): fit_ar TU TINH de panel lap ~86% khung (het trong)   # 2.1 (2026-08-25): panel fit co `fit_ar` (crop nhe ve ~1.3) + le/gap mong hon -> anh to hon ~40%   # 2.0 (2026-08-25): panel `pict` co khoa `fit` (thay ovan cover-crop) — anh minh hoa 16:9 vao hop doc khong con bi cat mat 2/3   # 1.9 (2026-08-24): sổ chỗ dải bên ghi MỌI vật (kể cả vật không bị đẩy) — hết chồng chéo   # 1.8 (2026-08-24): props/props_top dùng CHUNG sổ chỗ khi tránh cast — hết chồng nhau   # 1.7 (2026-08-24): props tự tránh VÙNG NHÂN VẬT (dải bên dưới CH_TOP) — sticker không còn bị tay/vai cast đè   # 1.6 (2026-08-24): `props_top` — lớp sticker vẽ SAU nội dung, nổi trên ảnh chính (thẻ art/pict trước đó bị ảnh đè mất props)   # 1.5 (2026-08-24): khoá `props` — rải NHIỀU đồ rời (bộ 38 icon PNG dùng chung) quanh thẻ, vẽ trước nội dung nên không che chữ; chữa bệnh 60% thẻ trơ chữ. Dùng `props`, KHÔNG dùng `fill` cho `big` (fill đã đo là cắt mất `cap`).   # 1.4 (2026-08-24): lối hiện `pop` — phần tử CO TỪ TO VỀ CỠ THẬT (app_pop + blend(scale=)), đúc từ video đối thủ đang được đề xuất; opt-in bằng cờ `pop` nên kênh cũ không đổi. Hằng số POP_FROM/POP_DUR nằm trong VERSION này ⇒ đổi chúng thì bump tiếp, nếu không .sig không hết hạn và thẻ giữ hình cũ.   # 1.3 (2026-08-19): label zu 2 DÒNG (khung bao đủ, tw_ml) + L_source org FIT + hộp cao theo doc — 2 lỗi user bắt trên video 14; kèm lượt りょう: layout pict · keyword 《…》 · pin badge · beats   # 1.2 (2026-08-18): 13 gate bố cục — xem `.claude/rules/stage-zu-layout.md` (cân dọc+ngang · mũi tên đều/thẳng · đích cuối to nhất · bong bóng chạm đích · node lơ lửng · bw ô cố định)   # 1.1: + `zu_fit` cân dọc + gate đồ trang trí mồ côi   # 1.0 (2026-08-17): + layout `zu` (SƠ ĐỒ tự do: node/edge/bubble/✗/tia) · 0.9: chữ mờ đậm lên khi có bgimg (mut()) · 0.8: + card_bg/bgimg · giãn 3 cột L_steps · palette theo kênh   # bump khi đổi HẰNG SỐ/bố cục → mọi .sig hết hạn, dựng lại
FONTS = Path(__file__).resolve().parent / "fonts"
CAST = Path(r"E:\Claude\Projects\youtube-jp-nenkin\assets\cast")

# ── bảng màu (đo từ frame đối thủ) ─────────────────────────────────────────────
INK, INK2 = (26, 42, 74), (60, 72, 96)
AMBER = (245, 179, 1)
GREY = (168, 174, 184)
# Bộ màu signature kênh (nenkin/CLAUDE.md §VISUAL): XANH an toàn · ĐỎ bị cắt · VÀNG sát ranh
RED, GREEN = (206, 68, 62), (32, 142, 104)
LINE = (222, 226, 233)
CARDC = (255, 255, 255)
BG_TOP, BG_BOT = (247, 249, 251), (232, 236, 242)
BAR = (17, 17, 19)

# ── khung ──────────────────────────────────────────────────────────────────────
CARD_X0, CARD_Y0, CARD_X1, CARD_Y1 = 272, 56, 1648, 902
SUB_Y0 = 928
CH_H = 560
# 🔴🔴 LUẬT SỐ 1 — ĐẶT PHẦN TỬ PHẢI **ĐO**, TUYỆT ĐỐI KHÔNG ĐOÁN (user chốt 2026-08-09:
#      "sửa lại cho cùng 1 khuôn hình nhé. Sau không được vi phạm nhé")
#   Mọi toạ độ phụ thuộc chữ phải lấy từ `font.getlength()` / `font.getbbox()`.
#   CẤM: suy vị trí từ `font.size`, cấm hằng số offset đoán tay như `vy + 118`.
#   VÌ SAO: hai lỗi lọt tới bản render 25 phút của video 09 đều cùng gốc này —
#     ① `unit` đặt ở `cx + fv.size*0.9` → `size` là CỠ FONT không phải BỀ RỘNG chữ
#        ⇒ hero 5 ký (「口座の情報」) bị chữ 「の紙」 ĐÈ vào giữa thân.
#     ② gạch chân đặt cứng `vy + 118` ⇒ hero cỡ lớn có đáy glyph tụt xuống dưới mốc
#        ⇒ gạch CẮT NGANG thân chữ thành gạch xoá (thẻ 「次回」).
#   Cả hai chỉ lộ khi hero DÀI; test bằng hero 1–2 ký (45日 · 4つ · 160) đều qua sạch.
#   ⇒ **Thêm/sửa layout thì phải test cả hero NGẮN NHẤT và DÀI NHẤT có thật trong SLIDES**,
#     không test bằng ví dụ tự bịa.
#
# 🔴 LUẬT BỐ CỤC — nhân vật ĐỨNG ĐÈ mép card (giống đối thủ), nên:
#    · nội dung DƯỚI y=CH_TOP phải nằm trong [CONTENT_X0, CONTENT_X1]
#    · tiêu đề / băng thời gian ở TRÊN y=CH_TOP thì dùng trọn bề ngang card
#    Bỏ luật này là chữ chui xuống dưới nhân vật (bệnh v0.1: dấu ✗ bị che).
CH_TOP = SUB_Y0 - CH_H          # 368
CONTENT_X0, CONTENT_X1 = 520, 1400
RISE = 26                        # độ trượt lên của phần tử khi hiện
APP = 0.42                       # thời lượng 1 lần hiện (đơn vị GỐC, trước khi nhân PACE)
# 🔴 PACE — núm chỉnh nhịp DUY NHẤT. >1 = chậm hơn. Nó giãn CẢ thời lượng hiện lẫn khoảng
# cách giữa các phần tử, nên chỉ sửa số này, đừng đi sửa từng mốc t0 rải trong layout.
# 1.35 chốt 2026-08-09 (user: "hiệu ứng chậm tí, hơi nhanh so với người Nhật").
PACE = 1.35
NL = chr(10)                     # ký tự xuống dòng — viết thế này để khỏi lệ thuộc escape


# ══════════════════════════════════════════════════════ chữ & hình cơ bản
def F(weight, size):
    f = {"black": "NotoSansJP-Black.otf", "bold": "NotoSansJP-Bold.otf",
         "med": "NotoSansJP-Medium.otf"}[weight]
    return ImageFont.truetype(str(FONTS / f), int(size))


def fit(text, weight, max_w, start, floor=28):
    """Thu cỡ chữ tới khi lọt max_w — chữ Nhật dài ngắn thất thường, đừng ép cứng."""
    s = start
    while s > floor:
        f = F(weight, s)
        if f.getbbox(text)[2] - f.getbbox(text)[0] <= max_w:
            return f
        s -= 2
    return F(weight, floor)


def tw(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def fit_ml(text, weight, max_w, start, floor=28):
    """fit() cho chuỗi CÓ XUỐNG DÒNG.
    🔴 Bẫy đã dính: `fit()` đo CẢ chuỗi kèm ký tự xuống dòng → bề ngang tính ra dài gần
    gấp đôi → tự thu cỡ chữ xuống sát sàn. Đó là lý do nhãn trong hộp `flow` chỉ còn ~22px
    trong khi trần là 44. Phải đo theo DÒNG RỘNG NHẤT."""
    probe = F(weight, 100)
    widest = max(text.split(NL),
                 key=lambda ln: probe.getbbox(ln)[2] - probe.getbbox(ln)[0])
    return fit(widest, weight, max_w, start, floor)


def tw_ml(d, xy, text, font, fill, leading=1.34):
    """Vẽ nhiều dòng, canh giữa cả khối theo xy. PIL không giãn dòng tử tế khi có anchor."""
    ls = text.split(NL)
    step = font.size * leading
    y0 = xy[1] - step * (len(ls) - 1) / 2
    for i, ln in enumerate(ls):
        d.text((xy[0], y0 + i * step), ln, font=font, fill=fill, anchor="mm")


# ── keyword màu inline (style りょう, 2026-08-19) ────────────────────────────
# Chữ ký mạnh nhất của kênh mẫu 節約看護師りょう (video 6DN88wQyBFg, 970K view): headline
# đen có 1–2 CỤM ĐỎ ngay trong câu; label trên nền navy thì cụm VÀNG. Marker: 《…》.
# ⚠️ Chỉ đường vẽ MỚI khi text CÓ marker — text không marker đi đường cũ từng byte,
# nên KHÔNG bump VERSION, .sig thẻ cũ còn nguyên.
import re as _re
_KW_RE = _re.compile("(《[^》]*》)")
KW_ON_LIGHT = (198, 40, 34)      # đỏ keyword trên nền card sáng (đo từ frame りょう)
KW_ON_DARK = (255, 213, 79)      # vàng keyword trên panel navy (「切り崩す」)


def plain(text):
    """Bỏ marker 《》 để ĐO bề rộng — fit() phải đo bản sạch, không đo cả marker."""
    return text.replace("《", "").replace("》", "")


def runs(text):
    """'あ《い》う' → [('あ',0),('い',1),('う',0)] — 1 = keyword được tô màu."""
    out = []
    for part in _KW_RE.split(text):
        if not part:
            continue
        if part.startswith("《") and part.endswith("》"):
            out.append((part[1:-1], 1))
        else:
            out.append((part, 0))
    return out


def tw_kw(d, xy, text, font, fill, kw=KW_ON_LIGHT, anchor="mm"):
    """Vẽ 1 DÒNG có marker keyword màu. Anchor hỗ trợ 'mm' và 'lm' (đủ cho chỗ đang dùng).
    Bề rộng từng run đo bằng getlength — LUẬT SỐ 1: đo, không đoán."""
    rs = runs(text)
    if len(rs) == 1 and not rs[0][1]:
        tw(d, xy, text, font, fill, anchor)
        return
    total = sum(font.getlength(s) for s, _ in rs)
    x = xy[0] - (total / 2 if anchor[0] == "m" else 0)
    for s, hot in rs:
        d.text((x, xy[1]), s, font=font, fill=(kw if hot else fill), anchor="l" + anchor[1])
        x += font.getlength(s)


def tw_ml_kw(d, xy, text, font, fill, kw=KW_ON_LIGHT, leading=1.34):
    """tw_ml() bản có keyword màu — canh giữa cả khối, từng dòng tự xử marker."""
    ls = text.split(NL)
    step = font.size * leading
    y0 = xy[1] - step * (len(ls) - 1) / 2
    for i, ln in enumerate(ls):
        tw_kw(d, (xy[0], y0 + i * step), ln, font, fill, kw, anchor="mm")


def ease_out(x):
    """smoothstep — vào mềm, ra mềm. Trước dùng cubic-out (bật nhanh rồi hãm) nghe "snappy"
    kiểu quảng cáo; tệp 60–70 hợp nhịp êm hơn. Đổi 2026-08-09 cùng lượt với PACE."""
    return x * x * (3 - 2 * x)


def app(t, t0, dur=APP):
    """→ (alpha, dy). Chưa tới lượt thì alpha=0; tới thì trượt lên RISE px + hiện dần.
    Chia t cho PACE ở ĐÂY = giãn toàn bộ dòng thời gian bằng một chỗ duy nhất."""
    t = t / PACE
    if t <= t0:
        return 0.0, RISE
    e = ease_out(min((t - t0) / dur, 1.0))
    return e, RISE * (1 - e)


def prog(t, t0, dur):
    """→ 0..1 tiến trình tuyến-tính-đã-ease, cho mũi tên / thanh chạy."""
    t = t / PACE
    if t <= t0:
        return 0.0
    return ease_out(min((t - t0) / dur, 1.0))


_LAYER = None      # lớp đang vẽ dở — `icon()` cần nó để alpha_composite ảnh PNG


def blend(im, alpha, dy, fn, dx=0, scale=1.0):
    """Vẽ `fn(d)` lên lớp riêng rồi ghép với alpha + lệch (dx, dy).
    Vẽ thẳng lên nền thì không fade được — PIL không có opacity cho từng nét.
    Trong lúc gọi `fn`, lớp được treo ở `_LAYER` để hàm nào cần DÁN ẢNH thì dùng.

    `scale` (mặc định 1.0 = KHÔNG đổi gì, kênh cũ không bị ảnh hưởng một byte): co/giãn
    lớp QUANH TÂM KHỐI MỰC của chính nó, dùng cho lối hiện `app_pop` (xem hàm đó).
    Tâm lấy từ bbox alpha nên không phải truyền toạ độ — layout nào cũng dùng được.
    Chỉ tốn một phép transform trong ~0,4s đầu của phần tử; xong hiệu ứng thì scale==1.0
    và nhánh này bị bỏ qua hoàn toàn."""
    global _LAYER
    if alpha <= 0.004:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    _LAYER = lay
    fn(ImageDraw.Draw(lay))
    _LAYER = None
    if abs(scale - 1.0) > 1e-3:
        bb = lay.getchannel("A").getbbox()
        if bb:
            cx, cy = (bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0
            s = max(0.05, scale)
            # 🔴 TỰ KẸP: phóng to mà không kẹp thì hero dài tràn RA NGOÀI card và đè lên
            # 2 nhân vật hai mép. Đã đo thật: hero 866px ở POP_FROM=1,8 ⇒ 1.559px > card
            # 1.376px. Kẹp ở đây (tầng TOOL) chứ không hạ hằng số, vì bề rộng hero khác
            # nhau từng thẻ — bắt người viết builder tự nhớ là kiểu luật sẽ trôi.
            # Chừa lề 40px mỗi bên so với card.
            if s > 1.0:
                mx = 40.0
                # 🔴 Kẹp theo KHOẢNG CÁCH TÂM→TỪNG MÉP, không theo bề rộng. Scale quanh tâm
                # bbox nên sau khi phóng: [cx-(cx-x0)s , cx+(x1-cx)s]. Bản đầu kẹp bằng
                # (R-L)/(x1-x0) và ĐÃ TRÀN THẬT 41px sang trái ở thẻ hero 「7,000円」 — hero
                # canh giữa cùng `unit` nên tâm bbox của nó LỆCH khỏi tâm card, phóng đối
                # xứng quanh tâm lệch thì mép gần hơn vượt trước.
                lim = []
                for c0, lo, hi, e0, e1 in ((cx, CARD_X0 + mx, CARD_X1 - mx, bb[0], bb[2]),
                                           (cy, CARD_Y0 + mx, CARD_Y1 - mx, bb[1], bb[3])):
                    if c0 - e0 > 1:
                        lim.append((c0 - lo) / (c0 - e0))
                    if e1 - c0 > 1:
                        lim.append((hi - c0) / (e1 - c0))
                if lim:
                    s = max(1.0, min(s, min(lim)))
            # AFFINE map output→input: input = (out - c)/s + c  ⇒ scale quanh (cx,cy).
            # Dùng transform (không resize+paste) để chịu được offset ÂM khi s>1.
            lay = lay.transform((W, H), Image.AFFINE,
                                (1.0 / s, 0, cx - cx / s, 0, 1.0 / s, cy - cy / s),
                                resample=Image.BICUBIC)
    if alpha < 0.999:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    im.alpha_composite(lay, dest=(int(round(dx)), int(round(dy))))


FLY = {"up": (0, 1), "down": (0, -1), "left": (1, 0), "right": (-1, 0), "none": (0, 0)}
"""Hướng BAY VÀO của phần tử (tên = hướng nó bay TỚI). Chốt 2026-08-09, user:
"có thể dùng hiệu ứng bay bay vào để nhìn nó trực quan hơn".

🔴 ĐỪNG NHẦM VỚI KEN BURNS. Đây là phần tử BAY VÀO CHỖ rồi ĐỨNG IM — khung hình vẫn
bất động tuyệt đối. Luật `feedback_video_no_motion_mot_giong` cấm CAMERA (pan/zoom/rung),
không cấm phần tử xuất hiện. Ngày nào thấy cả khung trôi là đã làm sai."""


POP_FROM = 1.80        # phần tử `pop` bắt đầu to gấp mấy lần cỡ thật
POP_DUR = 0.62         # thời lượng co về cỡ thật (đơn vị GỐC, trước khi nhân PACE)
POP_FADE = 0.30        # tỉ lệ của POP_DUR dành cho hiện rõ — xem chú thích trong app_pop


def app_pop(t, t0, dur=POP_DUR, s0=POP_FROM):
    """→ (alpha, scale) — phần tử hiện ra bằng cách **CO TỪ TO VỀ CỠ THẬT** + mờ dần vào.

    Đúc 2026-08-24 từ video đối thủ đang được đề xuất (シニアのお金相談所, 64:26). Đo frame
    liên tiếp 10fps: chữ đòn 「絶対」 vào khung ở 4,5s dưới dạng RẤT TO + mờ, rồi co về cỡ
    thật trong ~0,9s; khối bảng ở 15,5s cũng scale-in + fade trong ~0,5s.

    🔴 ĐÂY KHÔNG PHẢI KEN BURNS, và đã KIỂM CHỨNG bằng máy trước khi viết hàm này: đo bề
    rộng khối mực của video đó ở 13,0s / 14,1s / 15,2s ra **y hệt 960px**, vùng mực
    x 75–1174 không đổi một pixel ⇒ khung hình của họ BẤT ĐỘNG, chỉ phần tử động.
    Nên hàm này KHÔNG chạm luật `feedback_video_no_motion_mot_giong` (luật đó cấm CAMERA
    pan/zoom/rung, không cấm phần tử xuất hiện) — cùng lý lẽ đã ghi ở `FLY` phía trên.
    ⚠️ Cảm giác "cả khung to dần" khi xem contact sheet thu nhỏ là ẢO GIÁC — lại một ca
    của bài học "sheet thu nhỏ không dùng để nghiệm thu".
    """
    t = t / PACE
    if t <= t0:
        return 0.0, s0
    x = (t - t0) / dur
    # 🔴 ALPHA và SCALE phải là HAI đường cong khác nhau. Bản đầu dùng chung một `e`:
    # đo lại clip ra **chỉ thấy 1,16×** (1007→866px) dù POP_FROM=1,42 — vì lúc chữ còn to
    # thì nó vẫn đang mờ, mắt không kịp thấy pha "to". demo2 làm ngược: chữ HIỆN RÕ ngay
    # khi còn to rồi mới co, nên cú punch mới đọc được.
    a = ease_out(min(x / max(POP_FADE, 1e-3), 1.0))     # rõ hẳn trong 30% đầu
    e = ease_out(min(x, 1.0))                           # co suốt cả quãng
    return a, s0 + (1.0 - s0) * e


def app_fly(t, t0, dirn="up", dist=RISE, dur=APP):
    """→ (alpha, dx, dy) — như app() nhưng bay vào theo hướng, quãng đường tuỳ chỉnh."""
    t = t / PACE
    ux, uy = FLY.get(dirn, FLY["up"])
    if t <= t0:
        return 0.0, dist * ux, dist * uy
    e = ease_out(min((t - t0) / dur, 1.0))
    return e, dist * ux * (1 - e), dist * uy * (1 - e)


# ══════════════════════════════════════════════════════ sân khấu (đứng yên)
_BG_CACHE = {}


def stage_base():
    """Nền + card + bóng — dựng 1 lần rồi tái dùng cho cả 900 frame."""
    if "b" in _BG_CACHE:
        return _BG_CACHE["b"].copy()
    im = Image.new("RGB", (W, H), BG_TOP)
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * k) for i in range(3)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [CARD_X0, CARD_Y0 + 10, CARD_X1, CARD_Y1 + 10], 28, fill=(20, 30, 50, 46))
    im = Image.alpha_composite(im.convert("RGBA"),
                               sh.filter(ImageFilter.GaussianBlur(26)))
    ImageDraw.Draw(im).rounded_rectangle(
        [CARD_X0, CARD_Y0, CARD_X1, CARD_Y1], 28, fill=CARDC)
    _BG_CACHE["b"] = im
    return im.copy()


SCENE_CAST = {"kenkyuin_happy", "ito_cafe", "suzuki_exec", "takahashi_work",
              "seniors_work_group", "prop_tsucho", "yamada_happy"}
"""Ảnh là CẢNH (bàn/kính hiển vi/quầy) chứ không phải người cắt nền — đặt ở mép sân
khấu thì lòi cả bối cảnh vào khung. (Bộ いらすとや cũ; bộ riêng sensei_*/kikite_* thì sạch.)"""
FALLBACK = {"left": "sensei_present", "right": "kikite_listen"}
# Nhân vật dùng khi thẻ KHÔNG khai `left`/`right`. Trước 2026-08-17 hai tên này ghi cứng ở
# `render_frame()`; bộ cast của kênh khác không có chúng ⇒ thẻ ra KHÔNG NHÂN VẬT mà chỉ in
# "[!] thiếu …" (lỗi im lặng). Kênh khai `stage_cast_default` trong channels.py thì ghi đè.
CAST_DEFAULT = {"left": "kenkyuin", "right": "tanaka_think"}

# 🔴 TỈ LỆ THEO NHÂN VẬT — cân theo CỠ ĐẦU, không theo chiều cao khung.
#    案内役 chụp tới hông (đầu ≈ 23% chiều cao ảnh), 聞き手 chụp tới ngực (≈ 34%).
#    Cho cả hai cùng cao 560px thì đầu ông già to gấp rưỡi → nhìn như hai thế giới.
CAST_SCALE = {"sensei": 1.00, "kikite": 0.78, "josei": 0.70, "_default": 0.86}
# Ảnh gen LẺ hay bị crop sát hơn ảnh cắt từ sheet → cùng nhân vật mà đầu to hơn giữa các
# cảnh. Đo bằng `cao dau / cao anh` rồi bù riêng từng file. sensei_explain đo 0.534 so với
# 0.452–0.480 của các tư thế cùng bộ ⇒ nhân 0.85 mới bằng đầu.
CAST_SCALE_FILE = {"sensei_explain": 0.85}


def cast_h(name):
    if name in CAST_SCALE_FILE:                       # bù riêng từng file thắng hệ số nhóm
        for k, v in CAST_SCALE.items():
            if name.startswith(k):
                return int(CH_H * v * CAST_SCALE_FILE[name])
    for k, v in CAST_SCALE.items():
        if name.startswith(k):
            return int(CH_H * v)
    return int(CH_H * CAST_SCALE["_default"])
_CAST_CACHE = {}


def put_cast(im, name, side):
    if name in SCENE_CAST:
        print(f"  [!] '{name}' là ẢNH CẢNH → thay bằng '{FALLBACK[side]}'")
        name = FALLBACK[side]
    key = (name, side)
    if key not in _CAST_CACHE:
        p = CAST / f"{name}.png"
        if not p.exists():
            print(f"  [!] thiếu {p.name} — bỏ qua")
            return
        ch = Image.open(p).convert("RGBA")
        h = cast_h(name)
        ch = ch.resize((int(ch.width * h / ch.height), h), Image.LANCZOS)
        _CAST_CACHE[key] = ch
    ch = _CAST_CACHE[key]
    x = -34 if side == "left" else W - ch.width + 34
    im.alpha_composite(ch, dest=(x, SUB_Y0 - ch.height))


def sub_bar(im, text=None):
    d = ImageDraw.Draw(im)
    d.rectangle([0, SUB_Y0, W, H], fill=BAR)
    if text:
        tw(d, (W / 2, (SUB_Y0 + H) / 2), text, fit(text, "bold", W - 240, 46, 28),
           (255, 255, 255), anchor="mm")


# ══════════════════════════════════════════════════════ icon vector
def ic_env(d, x, y, s, c=INK):
    d.rounded_rectangle([x, y, x + s, y + s * .68], 6, outline=c, width=5)
    d.line([x + 4, y + 6, x + s / 2, y + s * .42, x + s - 4, y + 6], fill=c, width=5)


def ic_house(d, x, y, s, c=INK):
    d.line([x + s / 2, y, x, y + s * .38], fill=c, width=5)
    d.line([x + s / 2, y, x + s, y + s * .38], fill=c, width=5)
    d.rectangle([x + s * .12, y + s * .36, x + s * .88, y + s * .9], outline=c, width=5)
    d.rectangle([x + s * .36, y + s * .58, x + s * .64, y + s * .9], outline=c, width=4)


def ic_doc(d, x, y, s, c=INK):
    d.rounded_rectangle([x + s * .12, y, x + s * .88, y + s], 6, outline=c, width=5)
    for i, yy in enumerate((.28, .46, .64)):
        d.line([x + s * .26, y + s * yy, x + s * (.74 - i * .1), y + s * yy], fill=c, width=4)


def ic_bank(d, x, y, s, c=INK):
    d.line([x, y + s * .3, x + s / 2, y + s * .06, x + s, y + s * .3], fill=c, width=5)
    for fx in (.2, .45, .7):
        d.line([x + s * fx, y + s * .38, x + s * fx, y + s * .78], fill=c, width=5)
    d.line([x, y + s * .88, x + s, y + s * .88], fill=c, width=5)


def ic_person(d, x, y, s, c=INK):
    d.ellipse([x + s * .3, y + s * .04, x + s * .7, y + s * .44], outline=c, width=5)
    d.arc([x + s * .1, y + s * .48, x + s * .9, y + s * 1.2], 180, 360, fill=c, width=5)


def ic_lock(d, x, y, s, c=INK):
    d.arc([x + s * .22, y + s * .06, x + s * .78, y + s * .62], 180, 360, fill=c, width=5)
    d.rounded_rectangle([x + s * .1, y + s * .38, x + s * .9, y + s * .92], 6, outline=c, width=5)


def ic_pin(d, x, y, s, c=AMBER):
    d.ellipse([x + s * .22, y + s * .06, x + s * .78, y + s * .62], outline=c, width=6)
    d.line([x + s / 2, y + s * .6, x + s / 2, y + s], fill=c, width=6)


VEC_ICONS = {"env": ic_env, "house": ic_house, "doc": ic_doc, "bank": ic_bank,
             "person": ic_person, "lock": ic_lock, "pin": ic_pin}
# 🔴 KHO ICON: tìm theo THỨ TỰ — riêng kênh TRƯỚC, dùng chung SAU (user chốt 2026-08-17:
#    *"những ảnh nào tái sử dụng được thì bỏ ra khu vực dùng chung để tái sử dụng cho video sau"*).
#    · `<kênh>/assets/icons/`      = riêng kênh (avatar_* của dàn モニター) — GHI ĐÈ được
#    · `_media_library/stage_icons/` = DÙNG CHUNG mọi kênh (icon khái niệm: bank, calc, clock…)
#  ⚖️ Đây KHÔNG phá `media-library.md` §2 ("không tái dùng asset"). Rule đó nói về **b-roll
#  STOCK tải từ mạng** — lặp cảnh thật giữa các video là inauthentic content. Icon khái niệm
#  thì NGƯỢC LẠI: nó là **bộ nhận diện**, lặp lại là điều TỐT (lướt 1 giây biết kênh nào).
#  Ranh giới: vật trung tính, không số, không chữ, không gắn năm ⇒ dùng chung. Ảnh cảnh thật /
#  原典ショット / ảnh có con số của bài ⇒ nằm trong folder video, không đưa ra kho.
SHARED_ICON_DIR = Path(__file__).resolve().parent / "stage_icons"      # dùng chung mọi kênh
ICON_DIRS = [CAST.parent / "icons", SHARED_ICON_DIR]   # 🔴 CHỈ ĐÚNG cho kênh mặc định lúc IMPORT —
# xem cảnh báo dưới `icon_path()`, đừng đọc ICON_DIRS[0] trực tiếp ở chỗ khác.
ICON_DIR = ICON_DIRS[0]               # giữ tên cũ cho code/`_sig` đang trỏ tới
ICON_ALIAS = {"doc": "docs"}          # tên cũ trong SLIDES vẫn chạy được
_ICON_CACHE = {}


def icon_path(name):
    """→ Path của icon `name`, tìm riêng-kênh trước rồi kho dùng chung. None nếu không có.

    🔴 VÁ 2026-08-26 (health 40, lô sticker el_saba_*): KHÔNG được đọc `ICON_DIRS[0]` — nó là
    `CAST.parent / "icons"` được TÍNH MỘT LẦN LÚC IMPORT (CAST khi đó = mặc định nenkin), còn
    `--channel` reassign `CAST` (`globals()["CAST"] = ...`) ở main() SAU khi ICON_DIRS đã đóng
    băng giá trị cũ — Python không tính lại biểu thức đã gán. Hậu quả: mọi kênh KHÁC nenkin
    luôn tìm icon riêng-kênh trong `youtube-jp-nenkin/assets/icons/` (rỗng với sticker của
    kênh khác) → 100% sticker của health rơi vào nhánh "None" và bị bỏ qua IM LẶNG — `make_stage`
    không báo lỗi, `sync_stickers.py` cũng không thấy gì sai (file sticker THẬT SỰ tồn tại,
    chỉ là tìm sai thư mục). Đọc `CAST.parent` TRỰC TIẾP ở đây thay vì `ICON_DIRS[0]` để luôn
    lấy giá trị CAST **hiện tại** (module global, cùng biến `--channel` vừa gán)."""
    n = ICON_ALIAS.get(name, name)
    for d in (CAST.parent / "icons", SHARED_ICON_DIR):
        p = d / f"{n}.png"
        if p.exists():
            return p
    return None


def icon(d, name, x, y, s, color=None):
    """Vẽ 1 icon. ƯU TIÊN file PNG trong `assets/icons/` (bộ gen, cùng họ với nhân vật);
    không có thì rơi về icon vector vẽ bằng code — nên thiếu file cũng không gãy render.
    `color=GREY` → hạ xám + giảm đục, dùng cho các dòng ✗ (cái KHÔNG được)."""
    key = (ICON_ALIAS.get(name, name), int(s), color == GREY)
    if key not in _ICON_CACHE:
        p = icon_path(name)
        if p is None:
            _ICON_CACHE[key] = None
        else:
            im = Image.open(p).convert("RGBA").resize((int(s), int(s)), Image.LANCZOS)
            if color == GREY:
                g = im.convert("L").convert("RGBA")
                g.putalpha(im.getchannel("A").point(lambda v: int(v * 0.5)))
                im = g
            _ICON_CACHE[key] = im
    im = _ICON_CACHE[key]
    if im is None or _LAYER is None:
        return VEC_ICONS.get(name, ic_doc)(d, x, y, s, color or INK)
    _LAYER.alpha_composite(im, dest=(int(x), int(y)))


def mark_ok(d, cx, cy, r=26):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AMBER)
    d.line([cx - r * .42, cy, cx - r * .08, cy + r * .36, cx + r * .46, cy - r * .38],
           fill=(255, 255, 255), width=7, joint="curve")


def mark_no(d, cx, cy, r=26):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(226, 229, 234))
    for a, b in (((-1, -1), (1, 1)), ((-1, 1), (1, -1))):
        d.line([cx + a[0] * r * .38, cy + a[1] * r * .38,
                cx + b[0] * r * .38, cy + b[1] * r * .38], fill=(255, 255, 255), width=7)


def arrow(d, x0, y0, x1, y1, p=1.0, c=AMBER, w=None, outline=INK, ow=4):
    """Mũi tên MỘT KHỐI ĐẶC có viền — cùng ngôn ngữ hình với nhân vật (viền dày, bo góc).

    🔴 KHÔNG thay bằng ảnh gen sẵn, ba lý do:
      ① nó phải VẼ DẦN từ đuôi ra đầu (`p` = tiến trình) — ảnh tĩnh không mọc dài được
      ② hình học đổi theo từng bảng (2 hộp vs 4 hộp vs cong) — PNG co giãn là méo nét
      ③ nó mang MÀU TRẠNG THÁI: vàng = dòng chảy · đỏ = bị cắt · xám = không áp dụng

    Bản cũ là `line` mảnh + tam giác nhọn rời → nhìn như wireframe cạnh nhân vật viền dày.
    Nay dựng 1 đa giác (thân + đầu) rồi tô + kẻ viền, bo đầu bằng `joint="curve"`.
    """
    if p <= 0.02:
        return
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 2:
        return
    # 🔴 BỀ DÀY PHẢI THEO CHIỀU DÀI (user bắt được 2026-08-17: "mũi tên méo").
    # Bản đầu cố định w=15 cho mọi độ dài ⇒ mũi tên 90px cân đối, mũi tên 260px thành CÂY KIM
    # (thân 15px trên chiều dài 260px = 1:17) và đầu mũi 28px trông như cái chóp dính vào.
    # Truyền `w` rõ thì tôn trọng; để None thì tự cân theo tỉ lệ ~1:10 — tỉ lệ mũi tên khối
    # trong bộ frame mẫu của kênh đối thủ.
    if w is None:
        w = max(14, min(L * 0.10, 30))
    cur = L * p
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    hl = min(max(w * 2.2, 30), L * 0.42)      # dài đầu mũi — dài hơn bản cũ (w*1.9, cap 0.55)
    hw = w * 1.4                               # nửa bề ngang đầu mũi
    tx, ty = x0 + ux * cur, y0 + uy * cur

    if cur <= hl:                              # mới nhú: chỉ có đầu mũi lớn dần
        s = cur / hl
        pts = [(tx, ty),
               (x0 + nx * hw * s, y0 + ny * hw * s),
               (x0 - nx * hw * s, y0 - ny * hw * s)]
    else:
        bx, by = x0 + ux * (cur - hl), y0 + uy * (cur - hl)
        pts = [(x0 + nx * w / 2, y0 + ny * w / 2),
               (bx + nx * w / 2, by + ny * w / 2),
               (bx + nx * hw, by + ny * hw),
               (tx, ty),
               (bx - nx * hw, by - ny * hw),
               (bx - nx * w / 2, by - ny * w / 2),
               (x0 - nx * w / 2, y0 - ny * w / 2)]
    d.polygon(pts, fill=c)
    if outline:
        # PIL chỉ kẻ viền 1px cho polygon → phải tự kẻ bằng line có joint bo
        d.line(pts + [pts[0]], fill=outline, width=ow, joint="curve")


# ══════════════════════════════════════════════════════ phần chung của card
def title(im, text, t, y=CARD_Y0 + 74):
    f = fit(plain(text), "black", CARD_X1 - CARD_X0 - 120, 62, 36)
    a, dy = app(t, 0.12, 0.5)
    if "《" in text:      # keyword màu style りょう — text không marker đi đường cũ y nguyên
        blend(im, a, dy, lambda d: tw_kw(d, ((CARD_X0 + CARD_X1) / 2, y), text, f, INK,
                                         KW_ON_LIGHT, anchor="mm"))
    else:
        blend(im, a, dy, lambda d: tw(d, ((CARD_X0 + CARD_X1) / 2, y), text, f, INK,
                                      anchor="mm"))
    return y + f.size


def pill(im, text, y, t, t0):
    f = fit(text, "bold", 900, 40, 24)
    w = f.getbbox(text)[2] - f.getbbox(text)[0] + 72
    cx = (CARD_X0 + CARD_X1) / 2
    a, dy = app(t, t0)

    def fn(d):
        d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + f.size + 26], 10, fill=AMBER)
        tw(d, (cx, y + (f.size + 26) / 2), text, f, (40, 34, 8), anchor="mm")
    blend(im, a, dy, fn)
    return y + f.size + 26


# ══════════════════════════════════════════════════════ LAYOUT (đều nhận t)
def held(t, t0, i, pre):
    """→ (alpha, dy) cho phần tử thứ `i`, biết `pre` phần tử ĐẦU đã có sẵn trên màn hình.

    🔴 VÌ SAO CÓ: từ 2026-08-09 một khối nội dung bị CHẺ thành nhiều thẻ ~10s (user:
    "7s chuyển ảnh 1 lần chứ, nó tĩnh hơi lâu" — đo được 50,8s/thẻ, thẻ tệ nhất 130,7s).
    Thẻ sau vẫn phải vẽ lại các dòng của thẻ trước, nhưng mỗi clip chạy build-on từ t=0
    → không có cờ này thì dòng cũ FADE-IN LẦN NỮA = nháy hình mỗi 10 giây.
    `pre` dòng đầu ⇒ hiện tức thì, đứng yên; chỉ dòng MỚI mới bay vào.
    """
    if i < pre:
        return 1.0, 0
    return app(t, t0)


def beat(v, i, default):
    """→ t0 (đơn vị TRƯỚC PACE) cho phần tử thứ `i` của thẻ.

    🔴 NHỊP THEO LỜI ĐỌC (đo từ kênh mẫu りょう 2026-08-19, beat sheet 1fps): phần tử
    cách nhau **3–6 GIÂY** — hiện đúng lúc giọng đọc chạm ý đó, không lắp hết trong 2s
    đầu rồi đứng im. Builder ghi khoá `"beats": [giây, ...]` = mốc GIÂY THẬT tính từ
    đầu clip cho từng phần tử (theo thứ tự xuất hiện chuẩn của layout, KHÔNG tính title).
    Thiếu khoá / thiếu phần tử → dùng nhịp dồn mặc định cũ (default) — thẻ cũ không đổi.
    ⚠️ beats tính bằng giây thật nên phải chia PACE ở đây; và mốc cuối phải < CLIP_SEC
    lẫn < độ dài cue của thẻ (builder tự lo — gate build-on của cmd_slides nhắc)."""
    b = v.get("beats")
    if b and i < len(b) and b[i] is not None:
        return float(b[i]) / PACE
    return default


def fill_art(im, v, t, t0):
    """ẢNH MINH HOẠ LẤP CHỖ TRỐNG — thêm khoá `"fill": "<tên ảnh>"` vào BẤT KỲ layout nào.

    🔴 user chốt 2026-08-09: *"nếu video có nhiều chỗ trống quá thì mình có thể bỏ hình
    minh họa vào chứ đừng để nó trống như thế"*. Đo thật trên 132 thẻ video 09: `check`
    phủ mực TB **4,2%** (thấp nhất 2,3%) và `steps` 4,9%, trong khi `photo` 46% · `art` 30%
    ⇒ thẻ liệt kê 1–2 dòng để trống hơn nửa bảng. Gate ở `cmd_slides` cảnh báo khi <4%.

    Ảnh đặt ở góc dưới-PHẢI vùng nội dung, KHÔNG chạm nhân vật (trong CONTENT_X0..X1).
    """
    if not v.get("fill"):
        return t0
    bx0, by0, bx1, by1 = 1010, 536, CONTENT_X1, 852
    bw, bh = bx1 - bx0, by1 - by0
    pth = _art_path(v["fill"])
    alpha, adx, ady = app_fly(t, t0, v.get("fill_fly", "up"), 70, 0.55)
    if pth is None:
        blend(im, alpha, ady, lambda d: (
            d.rounded_rectangle([bx0, by0, bx1, by1], 14, fill=(250, 246, 236),
                                outline=AMBER, width=4),
            tw(d, ((bx0 + bx1) / 2, (by0 + by1) / 2), "⚠ THIẾU ẢNH LẤP",
               F("bold", 34), AMBER, anchor="mm")), dx=adx)
        if v["fill"] not in _MISSING_SEEN:
            _MISSING_SEEN.add(v["fill"])
            print(f"       🔴 THIẾU ẢNH LẤP: {v['fill']}")
        return t0 + 0.4
    key = (str(pth), bw, bh, pth.stat().st_mtime, "fill")
    if key not in _ART_CACHE:
        art = Image.open(pth).convert("RGB")
        sc = max(bw / art.width, bh / art.height)
        art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                         Image.LANCZOS)
        art = art.crop(((art.width - bw) // 2, (art.height - bh) // 2,
                        (art.width - bw) // 2 + bw, (art.height - bh) // 2 + bh)).convert("RGBA")
        msk = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(msk).rounded_rectangle([0, 0, bw - 1, bh - 1], 14, fill=255)
        art.putalpha(msk)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(art, dest=(bx0, by0))
        _ART_CACHE[key] = lay
    if alpha > 0.004:
        lay = _ART_CACHE[key]
        if alpha < 0.999:
            lay = lay.copy()
            lay.putalpha(lay.getchannel("A").point(lambda q: int(q * alpha)))
        im.alpha_composite(lay, dest=(int(round(adx)), int(round(ady))))
    blend(im, alpha, ady,
          lambda d: d.rounded_rectangle([bx0, by0, bx1, by1], 14, outline=LINE, width=3), dx=adx)
    return t0 + 0.42


def L_check(im, v, t):
    pre = v.get("pre", 0)
    y = title(im, v["title"], t if pre == 0 else 99) + 46
    # Thẻ ít dòng thì khối bị dồn lên đỉnh, nửa dưới card trống hoác (đo thật trên 28 thẻ
    # của video 09: thẻ 2 dòng để trống ~45% chiều cao). Canh GIỮA khối theo chỗ còn lại.
    n_ok, n_no = len(v.get("ok", [])), len(v.get("no", []))
    blk = (n_ok + n_no) * 88 + (50 if n_ok and n_no else 0)
    y = max(y, y + ((CARD_Y1 - 60) - y - blk) / 2)
    x = CONTENT_X0
    t0 = 0.72
    # `ok` KHÔNG bắt buộc: có thẻ chỉ liệt kê cái KHÔNG (4 nhóm không nhận được thư,
    # 3 câu sai của ○×クイズ…). Bản đầu ép v["ok"] → KeyError giữa chừng lượt dựng 28 thẻ.
    gi = 0
    for row in v.get("ok", []):
        ic, txt = (row if isinstance(row, (list, tuple)) else ("doc", row))
        f = fit(txt, "bold", CONTENT_X1 - x - 148, 50, 30)
        tt = beat(v, gi, t0)                # nhịp theo lời đọc (style りょう) nếu có beats
        a, dy = held(t, tt, gi, pre); gi += 1
        blend(im, a, dy, lambda d, y=y, ic=ic, txt=txt, f=f: (
            mark_ok(d, x, y + 30),
            icon(d, ic, x + 62, y + 2, 56),
            tw(d, (x + 148, y + 30), txt, f, INK, anchor="lm")))
        y += 88
        t0 = tt + 0.40
    if v.get("ok") and v.get("no"):        # gạch ngăn chỉ có nghĩa khi có CẢ hai phía
        y += 18
        a, dy = held(t, t0, gi - 1, pre)
        blend(im, a, dy, lambda d, y=y: d.line([CONTENT_X0 - 20, y, CONTENT_X1, y],
                                               fill=LINE, width=3))
        y += 32
        t0 += 0.30
    for row in v.get("no", []):
        ic, txt = (row if isinstance(row, (list, tuple)) else ("doc", row))
        f = fit(txt, "bold", CONTENT_X1 - x - 148, 50, 30)
        tt = beat(v, gi, t0)
        a, dy = held(t, tt, gi, pre); gi += 1
        blend(im, a, dy, lambda d, y=y, ic=ic, txt=txt, f=f: (
            mark_no(d, x, y + 30),
            icon(d, ic, x + 62, y + 2, 56, mut(v)),
            tw(d, (x + 148, y + 30), txt, f, mut(v), anchor="lm")))
        y += 88
        t0 = tt + 0.38
    return fill_art(im, v, t, t0)


def L_flow(im, v, t):
    y = title(im, v["title"], t)
    if v.get("band"):
        y = pill(im, v["band"], y + 26, t, 0.58)
    n = len(v["steps"])
    gap = 65
    bw = (CONTENT_X1 - CONTENT_X0 - gap * (n - 1)) / n
    x, by = CONTENT_X0, y + 84
    t0 = 0.95
    for i, st in enumerate(v["steps"]):
        ic, txt = (st if isinstance(st, (list, tuple)) else ("doc", st))
        f = fit_ml(txt, "bold", bw - 36, 44, 30)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d, x=x, ic=ic, txt=txt, f=f: (
            d.rounded_rectangle([x, by, x + bw, by + 268], 14, fill=(252, 253, 255),
                                outline=LINE, width=3),
            icon(d, ic, x + bw / 2 - 44, by + 30, 88),
            tw_ml(d, (x + bw / 2, by + 190), txt, f, INK2)))
        if i < n - 1:
            p = prog(t, t0 + 0.30, 0.34)
            blend(im, 1.0, 0, lambda d, x=x, p=p: arrow(
                d, x + bw + 14, by + 134, x + bw + gap - 12, by + 134, p))
        x += bw + gap
        t0 += 0.50
    return t0


def L_compare(im, v, t):
    y = title(im, v["title"], t) + 40
    mid = (CONTENT_X0 + CONTENT_X1) / 2
    a, dy = app(t, 0.70)
    blend(im, a, dy, lambda d: d.line([mid, y + 10, mid, y + 300], fill=LINE, width=3))
    for k, (side, box) in enumerate(((v["panels"][0], (CONTENT_X0, mid - 40)),
                                     (v["panels"][1], (mid + 40, CONTENT_X1)))):
        cx = (box[0] + box[1]) / 2
        f = fit_ml(side["cap"], "bold", box[1] - box[0] - 16, 44, 30)
        a, dy = app(t, beat(v, k, 0.72 + k * 0.42))   # beats[0..1] = 2 panel
        blend(im, a, dy, lambda d, side=side, cx=cx, f=f: (
            icon(d, side.get("icon", "house"), cx - 66, y + 22, 132),
            tw_ml(d, (cx, y + 226), side["cap"], f, INK2)))
    yy = y + 336
    t0 = max(beat(v, 1, 1.28), 1.28) + 0.42
    for i, row in enumerate(v["rows"]):
        f = fit(row, "bold", CONTENT_X1 - CONTENT_X0 - 110, 40, 24)
        t0 = beat(v, 2 + i, t0)                       # beats[2..] = từng row
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d, yy=yy, row=row, f=f: (
            d.rounded_rectangle([CONTENT_X0, yy, CONTENT_X1, yy + 78], 10,
                                fill=(250, 251, 253), outline=LINE, width=2),
            d.rectangle([CONTENT_X0 + 24, yy + 26, CONTENT_X0 + 50, yy + 52], fill=AMBER),
            tw(d, (CONTENT_X0 + 74, yy + 39), row, f, INK2, anchor="lm")))
        yy += 96
        t0 += 0.42
    return t0


def L_timeline(im, v, t):
    y = title(im, v["title"], t) + 60
    x0, x1 = CONTENT_X0, CONTENT_X1
    ty = y + 110
    a, dy = app(t, 0.62)
    blend(im, a, dy, lambda d: (
        tw(d, (x0, y + 30), v["from"], F("bold", 34), INK2, anchor="lm"),
        tw(d, (x1, y + 30), v["to"], F("bold", 34), INK2, anchor="rm"),
        d.line([x0, ty, x1, ty], fill=(214, 219, 227), width=10)))
    p = prog(t, 0.95, 0.85)
    if p > 0.01:
        wfin = (x1 - x0) * v.get("prog", .62)
        blend(im, 1.0, 0, lambda d: d.rounded_rectangle(
            [x0, ty - 22, x0 + wfin * p, ty + 22], 22, fill=AMBER))
        if p > 0.9:
            blend(im, (p - .9) / .1, 0, lambda d: tw(
                d, (x0 + wfin / 2, ty), v["label"], F("black", 40), (40, 34, 8), anchor="mm"))
    n = len(v["steps"])
    t0 = 1.45
    for i, st in enumerate(v["steps"]):
        ic, txt = (st if isinstance(st, (list, tuple)) else ("doc", st))
        bw = (x1 - x0) / n - 26
        cx = x0 + (x1 - x0) * (i + .5) / n
        by = ty + 78
        f = fit_ml(txt, "bold", bw - 26, 38, 26)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d, cx=cx, ic=ic, txt=txt, f=f, bw=bw: (
            d.rounded_rectangle([cx - bw / 2, by, cx + bw / 2, by + 190], 12,
                                fill=(252, 253, 255), outline=LINE, width=3),
            icon(d, ic, cx - 36, by + 24, 72),
            tw_ml(d, (cx, by + 142), txt, f, INK2)))
        t0 += 0.40
    return t0


def L_source(im, v, t):
    y = title(im, v.get("title", "出どころは、こちらです"), t) + 40
    bx0, bx1 = CONTENT_X0 - 40, CONTENT_X1 + 40
    # 🔴 org phải FIT, không dùng cỡ cứng 46 (user bắt 2026-08-19 clip_24: org dài
    # 「新潟県上越市（掲載日 2025年1月27日）」 tràn qua mép phải khung vàng). Và hộp phải
    # CAO THEO SỐ DÒNG doc — doc 3 dòng cỡ 42 chạm sát đáy hộp cứng 330.
    fo = fit(v["org"], "black", bx1 - (bx0 + 200) - 36, 46, 28)
    f = fit_ml(v["doc"], "bold", bx1 - bx0 - 250, 42, 30)
    n_doc = len(v["doc"].split(NL))
    by1 = max(y + 330, y + 152 + f.size * 1.34 * (n_doc - 1) + f.size + 28)
    a, dy = app(t, 0.62)
    blend(im, a, dy, lambda d: d.rounded_rectangle(
        [bx0, y, bx1, by1], 16, fill=(252, 253, 255), outline=AMBER, width=4))
    a, dy = app(t, 0.95)
    blend(im, a, dy, lambda d: (
        ic_doc(d, bx0 + 56, y + 60, 96),
        tw(d, (bx0 + 200, y + 74), v["org"], fo, INK, anchor="lm")))
    a, dy = app(t, 1.30)
    blend(im, a, dy, lambda d: [
        d.text((bx0 + 200, y + 152 + j * f.size * 1.34), ln, font=f, fill=INK2, anchor="lm")
        for j, ln in enumerate(v["doc"].split(NL))])
    if v.get("note"):
        a, dy = app(t, 1.75)
        blend(im, a, dy, lambda d: tw(d, ((bx0 + bx1) / 2, by1 + 56), v["note"],
                                      F("med", 34), mut(v), anchor="mm"))
    return 1.95


def L_big(im, v, t):
    """SỐ ĐẮT — một con số/một chữ chiếm gần hết bảng.

    Sinh ra 2026-08-09: 20/28 thẻ của video 09 là `check` (danh sách gạch đầu dòng)
    → xem 24 phút chỉ thấy một kiểu. Thẻ này là NHỊP MẠNH.

    🔴 SỬA 2026-08-09 (user bắt được 2 lỗi trên video đã render):
      ① `unit` bị ĐÈ LÊN hero — bản đầu đặt nó ở `cx + fv.size*0.9`, mà `fv.size` là
         CỠ FONT chứ không phải BỀ RỘNG chữ hero. Hero 5 ký thì unit rơi vào giữa hero.
         → giờ đo bề rộng thật (`getlength`) và xếp hero+unit thành MỘT KHỐI canh giữa.
      ② Gạch chân cắt ngang thân chữ — bản đầu đặt cứng ở `vy+118`, hero cỡ lớn thì
         đáy chữ tụt xuống dưới mốc đó thành gạch xoá.
         → giờ lấy đáy glyph thật từ `getbbox` rồi đặt gạch DƯỚI nó.
    """
    y = title(im, v["title"], t) + 40
    val, unit = v["value"], v.get("unit", "")
    cx = (CONTENT_X0 + CONTENT_X1) / 2
    avail = CONTENT_X1 - CONTENT_X0
    # đo unit TRƯỚC để chừa chỗ, rồi mới co hero cho vừa phần còn lại
    fu = F("bold", 64) if unit else None
    uw = (fu.getlength(unit) + 22) if unit else 0
    # 🔴 hero CÓ THỂ NHIỀU DÒNG. `getbbox()` trên chuỗi có ký tự xuống dòng
    # chỉ trả khung MỘT dòng ⇒ gạch chân tính theo dòng 1 rồi rơi vào giữa dòng 2
    # (lỗi lọt tới bản render, thẻ 16:38). Phải đo theo DÒNG RỘNG NHẤT + đếm SỐ DÒNG.
    lines = val.split(NL)
    n_ln = len(lines)
    fv = fit_ml(val, "black", max(120, avail - (uw if n_ln == 1 else 0)), 300, 110)
    lw = [fv.getlength(ln) for ln in lines]
    vw = max(lw)
    lead = fv.size * 1.16
    blk_h = lead * (n_ln - 1) + (fv.getbbox(lines[0])[3] - fv.getbbox(lines[0])[1])
    vy = y + 190
    tone = v.get("tone", "amber")
    col = {"amber": AMBER, "ink": INK, "bad": RED, "ok": GREEN}.get(tone, AMBER)
    if n_ln == 1:
        x_left = cx - (vw + uw) / 2                 # khối hero+unit canh giữa
    else:
        x_left = None                               # nhiều dòng: canh giữa từng dòng
    bar_y = vy + blk_h / 2 + 26                     # LUÔN dưới đáy khối chữ thật
    bar_w = max(240, min(660, (vw + uw) * 0.62))
    y_top = vy - lead * (n_ln - 1) / 2
    tv = beat(v, 0, 0.72)                       # beats[0] = hero · [1] = cap · [2] = note
    # `pop: true` ⇒ hero CO TỪ TO VỀ CỠ THẬT thay vì trượt lên (app_pop, chốt 2026-08-24).
    # Chỉ dùng cho SỐ ĐẮT — layout này vốn đã là nhịp mạnh nhất của bài.
    if v.get("pop"):
        a, sc = app_pop(t, tv)
        dy = 0.0
    else:
        a, dy = app(t, tv)
        sc = 1.0
    blend(im, a, dy, lambda d: (
        d.rounded_rectangle([cx - bar_w / 2, bar_y, cx + bar_w / 2, bar_y + 14], 7, fill=col),
        [d.text((x_left if x_left is not None else cx, y_top + k * lead), ln, font=fv,
                fill=INK, anchor=("lm" if x_left is not None else "mm"))
         for k, ln in enumerate(lines)]), scale=sc)
    if unit and n_ln == 1:
        a, dy = app(t, tv + 0.24)
        blend(im, a, dy, lambda d: tw(d, (x_left + vw + 22, vy + 30), unit,
                                      fu, INK2, anchor="lm"))
    elif unit:
        a, dy = app(t, tv + 0.24)
        blend(im, a, dy, lambda d: tw(d, (cx, bar_y + 52), unit, fu, INK2, anchor="mm"))
    t0 = tv + 0.40
    if v.get("cap"):
        f = fit_ml(plain(v["cap"]), "bold", avail, 48, 32)
        t0 = beat(v, 1, t0)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw_ml_kw(d, (cx, bar_y + (150 if unit else 96)),
                                            v["cap"], f, INK2))
        t0 += 0.42
    if v.get("note"):
        t0 = beat(v, 2, t0)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw(d, (cx, CARD_Y1 - 58), v["note"],
                                      F("med", 34), mut(v), anchor="mm"))
        t0 += 0.36
    return fill_art(im, v, t, t0)


def L_bars(im, v, t):
    """BIỂU ĐỒ CỘT NGANG — chỗ duy nhất đặt được góc PHÂN TÍCH (so sánh định lượng).

    `rows`: [nhãn, số, tone?]  ·  tone: amber (mặc định) / ok / bad / grey.
    Bề rộng cột tỉ lệ với `max` (không cho thì lấy số lớn nhất).
    """
    rows = v["rows"]
    y = title(im, v["title"], t if not v.get("pre") else 99) + 50
    mx = v.get("max") or max((r[1] for r in rows), default=1) or 1
    lab_w = v.get("label_w", 300)
    x0 = CONTENT_X0
    bx0 = x0 + lab_w + 24
    bx1 = CONTENT_X1 - 150
    blk = len(rows) * 104
    y = max(y, y + ((CARD_Y1 - 70) - y - blk) / 2)
    # ⭐ VẠCH NGƯỠNG (2026-08-19, style りょう "một đường kẻ"): "vline": [giá_trị, "nhãn"].
    # Vẽ TRƯỚC các cột — cột mọc ra rồi vượt/không vượt vạch, đó chính là kịch của thẻ.
    if v.get("vline"):
        vv, vlab = v["vline"][0], (v["vline"][1] if len(v["vline"]) > 1 else "")
        xl = bx0 + (bx1 - bx0) * (vv / mx)
        y0v, y1v = y + 2, y + blk - 36
        a, dy = app(t, 0.58)
        blend(im, a, dy, lambda d: (
            _dash_line(d, xl, y0v, xl, y1v, RED, 7),
            tw(d, (xl, y0v - 26), vlab, fit(vlab, "black", 420, 34, 26),
               RED, anchor="mm") if vlab else None))
    t0 = 0.72
    pre = v.get("pre", 0)
    for bi, r in enumerate(rows):
        lab, val = r[0], r[1]
        tone = r[2] if len(r) > 2 else "amber"
        col = {"amber": AMBER, "ok": GREEN, "bad": RED, "grey": GREY}.get(tone, AMBER)
        fl = fit(lab, "bold", lab_w, 40, 26)
        wfull = (bx1 - bx0) * (val / mx)
        t0 = beat(v, bi, t0)                         # nhịp theo lời đọc (style りょう)
        p = 1.0 if bi < pre else prog(t, t0, 0.75)   # cột MỌC ra, không nhảy vào
        a, dy = held(t, t0, bi, pre)
        blend(im, a, dy, lambda d, y=y, lab=lab, fl=fl: (
            tw(d, (x0 + lab_w, y + 34), lab, fl, INK2, anchor="rm"),
            d.rounded_rectangle([bx0, y + 12, bx1, y + 56], 10, fill=(244, 246, 250))))
        if p > 0.01:
            blend(im, 1.0, 0, lambda d, y=y, p=p, wfull=wfull, col=col: (
                d.rounded_rectangle([bx0, y + 12, bx0 + max(14, wfull * p), y + 56],
                                    10, fill=col)))
        if p > 0.85:
            txt = f"{r[3] if len(r) > 3 else val}"
            blend(im, (p - .85) / .15, 0, lambda d, y=y, txt=txt: tw(
                d, (bx1 + 24, y + 34), txt, F("black", 46), INK, anchor="lm"))
        y += 104
        t0 += 0.44
    if v.get("note"):
        t0 = beat(v, len(rows), t0)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw(d, ((CONTENT_X0 + CONTENT_X1) / 2, CARD_Y1 - 54),
                                      v["note"], F("med", 34), mut(v), anchor="mm"))
        t0 += 0.36
    return t0


_ART_CACHE = {}
_MISSING_SEEN = set()
ART_ROOTS = []
"""Thư mục tìm ảnh minh hoạ của layout `art` — cmd_slides nạp vào lúc chạy."""


def _art_path(name):
    p = Path(name)
    if p.is_absolute():
        return p if p.exists() else None
    for r in ART_ROOTS:
        q = r / name
        if q.exists():
            return q
    return None


STK_RED = (206, 52, 40)          # đỏ khoanh/mũi tên/con dấu — chỉ dùng cho lớp sticker
STK_POP = 1.26                   # cỡ lúc bật ra, co về 1.0 (hiệu ứng "ドン")


def _pop(im, a, cx, cy, tile, pop=STK_POP):
    """Dán `tile` (RGBA) vào (cx,cy) với hiệu ứng NẢY: to hơn rồi co về đúng cỡ.

    Vì sao không dùng `blend()`: blend chỉ fade + dịch, không phóng được. Số hero cần
    NẢY mới ra chất telop Nhật — và cái nảy đó là thứ mắt bắt được ở nền tĩnh.
    """
    if a <= 0.004:
        return
    s = pop + (1.0 - pop) * a                       # a: 0→1 ⇒ s: pop→1.0
    w2, h2 = max(1, int(tile.width * s)), max(1, int(tile.height * s))
    tl = tile if s == 1.0 else tile.resize((w2, h2), Image.LANCZOS)
    if a < 0.999:
        tl = tl.copy()
        tl.putalpha(tl.getchannel("A").point(lambda vv: int(vv * a)))
    im.alpha_composite(tl, dest=(int(cx - w2 / 2), int(cy - h2 / 2)))


def _tile_text(txt, f, fill, stroke, sw, pad=26, shadow=True):
    """Chữ có viền dày (+ bóng mềm) trên tile RGBA trong suốt, cắt sát nét."""
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    x0, y0, x1, y1 = d0.textbbox((0, 0), txt, font=f, stroke_width=sw)
    tile = Image.new("RGBA", (x1 - x0 + pad * 2, y1 - y0 + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    ox, oy = pad - x0, pad - y0
    if shadow:
        d.text((ox + 7, oy + 7), txt, font=f, fill=(20, 18, 12, 70),
               stroke_width=sw, stroke_fill=(20, 18, 12, 70))
    d.text((ox, oy), txt, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return tile


_PROP_CACHE, _AIMG_CACHE = {}, {}


def _prop(name, w, rot=0):
    """PNG nền TRONG (cutout) trong art/ → tile RGBA rộng `w`px, xoay `rot` độ.
    Cache theo (tên, w, rot, mtime) — mtime để thay ảnh là tự dựng lại (§2.5)."""
    p = _art_path(name)
    if p is None:
        if name not in _MISSING_SEEN:
            _MISSING_SEEN.add(name)
            print(f"       🔴 THIẾU ĐẠO CỤ: {name} — bỏ PNG nền trong vào art/")
        return None
    key = (str(p), w, rot, p.stat().st_mtime)
    if key not in _PROP_CACHE:
        im = Image.open(p).convert("RGBA")
        h = max(1, int(im.height * w / im.width))
        im = im.resize((max(1, w), h), Image.LANCZOS)
        if rot:
            im = im.rotate(rot, Image.BICUBIC, expand=True)
        _PROP_CACHE[key] = im
    return _PROP_CACHE[key]


def _art_img(name, bw, bh):
    """Ảnh nền của thẻ, đã cover-crop về (bw,bh) — để `zoom` cắt lại vùng cần phóng."""
    p = _art_path(name)
    if p is None:
        return None
    key = (str(p), bw, bh, p.stat().st_mtime)
    if key not in _AIMG_CACHE:
        a = Image.open(p).convert("RGB")
        sc = max(bw / a.width, bh / a.height)
        a = a.resize((max(1, int(a.width * sc)), max(1, int(a.height * sc))), Image.LANCZOS)
        _AIMG_CACHE[key] = a.crop(((a.width - bw) // 2, (a.height - bh) // 2,
                                   (a.width - bw) // 2 + bw, (a.height - bh) // 2 + bh))
    return _AIMG_CACHE[key]


def _burst(im, a, cx, cy, r, box, n=14, col=None):
    """集中線 — tia tụ toả ra sau con số. Vẽ procedural, KHÔNG cần ảnh.

    🔴 PHẢI KẸP TRONG `box` (ô ảnh): bản đầu vẽ thẳng lên khung nên tia chạy lên đè tiêu đề
    và vượt cả mép thẻ — soi sheet mới thấy. Tia là hiệu ứng CỦA ẢNH, không phải của cả khung.
    """
    if a <= 0.004:
        return
    col = col or AMBER
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        th = 2 * math.pi * i / n + 0.13
        r0, r1 = r * 0.44, r * (0.62 + 0.38 * a)
        wid = max(3, int(r * 0.045))
        d.line([cx + r0 * math.cos(th), cy + r0 * math.sin(th),
                cx + r1 * math.cos(th), cy + r1 * math.sin(th)],
               fill=col + (int(150 * a),), width=wid)
    msk = Image.new("L", (W, H), 0)
    ImageDraw.Draw(msk).rounded_rectangle(list(box), 16, fill=255)
    lay.putalpha(Image.composite(lay.getchannel("A"), Image.new("L", (W, H), 0), msk))
    im.alpha_composite(lay)


def _prog_rect(d, x0, y0, x1, y1, p, col, w=9):
    """Vẽ DẦN chu vi một khung chữ nhật theo tỉ lệ p (0→1), từ góc trái-trên, chiều kim đồng hồ.

    Vẽ 4 cạnh liền một mạch chứ không fade cả khung: mắt phải thấy nét bút ĐANG chạy —
    đó là thứ nói "chỗ này, ngay đây" mà một khung hiện tức thì không nói được.
    """
    W_, H_ = x1 - x0, y1 - y0
    per = 2 * (W_ + H_)
    run = per * max(0.0, min(1.0, p))
    segs = [((x0, y0), (x1, y0), W_), ((x1, y0), (x1, y1), H_),
            ((x1, y1), (x0, y1), W_), ((x0, y1), (x0, y0), H_)]
    for (ax, ay), (bx, by), ln in segs:
        if run <= 0:
            break
        k = min(1.0, run / ln) if ln else 1.0
        d.line([ax, ay, ax + (bx - ax) * k, ay + (by - ay) * k], fill=col, width=w)
        run -= ln


def draw_pin(im, pin, t, t0, bx0, by0, bw, bh):
    """Một sticker đè lên ảnh. Trả về t0 cho sticker kế.

    Hai dạng spec, CỐ Ý giữ cả hai:
      · list  ["68%", fx, fy]                → viên thuốc amber cũ (nenkin/kaigo/akiya dùng)
      · dict  {"t","at":[fx,fy],"kind",...}  → lớp mới: num · circle · arrow · stamp
    Thêm kind mới KHÔNG đổi cách vẽ của spec cũ ⇒ KHÔNG bump VERSION ⇒ .sig của kênh khác
    còn nguyên, không phải dựng lại clip cũ.
    """
    if not isinstance(pin, dict):                                    # ---- spec CŨ
        txt, fx, fy = pin[0], pin[1], pin[2]
        px, py = bx0 + bw * fx, by0 + bh * fy
        f = fit(txt, "black", 520, 40, 28)
        a, dy = app(t, t0)
        wp = f.getlength(txt) + 46
        blend(im, a, dy, lambda d, px=px, py=py, txt=txt, f=f, wp=wp: (
            d.rounded_rectangle([px - wp / 2, py - 30, px + wp / 2, py + 30], 30,
                                fill=AMBER, outline=(255, 255, 255), width=4),
            tw(d, (px, py), txt, f, (40, 34, 8), anchor="mm")))
        return t0 + 0.40

    kind = pin.get("kind", "num")
    fx, fy = pin.get("at", [0.5, 0.5])
    px, py = bx0 + bw * fx, by0 + bh * fy
    a, _ = app(t, t0)

    if kind == "num":                    # SỐ HERO — to, amber, viền navy, nảy vào
        f = fit(str(pin["t"]), "black", int(bw * pin.get("w", 0.52)),
                pin.get("size", 148), 72)
        tile = _tile_text(str(pin["t"]), f, AMBER + (255,), INK + (255,), 9)
        if pin.get("burst"):             # 集中線 toả sau số — chỉ bật ở số ĐẮT NHẤT của thẻ
            _burst(im, a, px, py, max(tile.width, tile.height) * 0.92,
                   (bx0, by0, bx0 + bw, by0 + bh))
        _pop(im, a, px, py, tile)

    elif kind == "stamp":                # CON DẤU nghiêng — 「もったいない！」
        f = fit(str(pin["t"]), "black", int(bw * 0.46), pin.get("size", 62), 34)
        txt = str(pin["t"])
        d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        x0, y0, x1, y1 = d0.textbbox((0, 0), txt, font=f)
        pw, ph = x1 - x0 + 76, y1 - y0 + 52
        tile = Image.new("RGBA", (pw + 24, ph + 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(tile)
        d.rounded_rectangle([12, 12, pw + 12, ph + 12], 18, fill=(255, 252, 245, 245),
                            outline=STK_RED + (255,), width=7)
        tw(d, ((pw + 24) / 2, (ph + 24) / 2), txt, f, STK_RED + (255,), anchor="mm")
        _pop(im, a, px, py, tile.rotate(pin.get("rot", -8), Image.BICUBIC, expand=True))

    elif kind == "badge":                # BONG BÓNG TRÒN đặc màu — 「最大24%減」 kiểu りょう
        # PUNCH của thẻ (đo kênh mẫu 節約看護師りょう 2026-08-19, beat sheet 1fps):
        # vòng tròn ĐẶC xanh đậm/đỏ, chữ TRẮNG 1–2 dòng, pop-scale vào đúng lúc giọng đọc
        # nói con số đó. Mỗi thẻ chỉ nên có MỘT badge — nó là điểm nhấn, nhiều là loãng.
        tone = pin.get("tone", "blue")
        col = {"blue": (23, 88, 166), "red": RED, "green": GREEN,
               "navy": INK, "amber": AMBER}.get(tone, (23, 88, 166))
        r = int(bw * pin.get("r", 0.155))
        lines = str(pin["t"]).split(NL)
        f = fit_ml(str(pin["t"]), "black", int(r * 1.56), pin.get("size", 84), 34)
        side = r * 2 + 26
        tile = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        d = ImageDraw.Draw(tile)
        d.ellipse([8, 8, side - 9, side - 9], fill=col + (250,),
                  outline=(255, 255, 255, 255), width=9)
        step = f.size * 1.16
        cy0 = side / 2 - step * (len(lines) - 1) / 2
        txt_col = (40, 34, 8) if tone == "amber" else (255, 255, 255)
        for j, ln in enumerate(lines):
            d.text((side / 2, cy0 + j * step), ln, font=f, fill=txt_col, anchor="mm")
        _pop(im, a, px, py, tile, pop=1.18)
        return t0 + 0.50

    elif kind == "prop":                 # ĐẠO CỤ CUTOUT bay vào (PNG nền trong, để ở art/)
        tile = _prop(pin["img"], int(bw * pin.get("w", 0.30)), pin.get("rot", 0))
        if tile is not None:
            _, dx, dy = app_fly(t, t0, pin.get("from", "right"),
                                pin.get("dist", 190), 0.52)
            _pop(im, a, px + dx, py + dy, tile, pop=pin.get("pop", 1.10))
        return t0 + 0.44

    elif kind == "zoom":                 # VÒNG PHÓNG ĐẠI — cắt chính ảnh đó rồi thổi to
        # Khong can anh moi: lay dung vung (at) cua anh nen, phong `z` lan, dat trong hinh tron
        # co vien amber. Dung cho chi tiet nho (bo xo, mat cat) ma anh goc thay qua be.
        r = int(bw * pin.get("r", 0.17))
        src = _art_img(v_img, bw, bh) if (v_img := pin.get("_img")) else None
        if src is not None and a > 0.004:
            z = pin.get("z", 2.2)
            sx, sy = int(bw * fx), int(bh * fy)
            half = int(r / z)
            box = (max(0, sx - half), max(0, sy - half), min(bw, sx + half), min(bh, sy + half))
            crop = src.crop(box).resize((r * 2, r * 2), Image.LANCZOS)
            msk = Image.new("L", (r * 2, r * 2), 0)
            ImageDraw.Draw(msk).ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=255)
            # vành TRẮNG ngoài + vành amber trong: không có vành trắng thì cái vòng chìm vào
            # ảnh nền và người xem không đọc ra là "phóng đại" (soi sheet mới thấy)
            pad = 22
            tile = Image.new("RGBA", (r * 2 + pad * 2, r * 2 + pad * 2), (0, 0, 0, 0))
            dt = ImageDraw.Draw(tile)
            dt.ellipse([4, 4, r * 2 + pad * 2 - 5, r * 2 + pad * 2 - 5],
                       fill=(255, 255, 255, 235))
            tile.paste(crop, (pad, pad), msk)
            dt.ellipse([pad - 5, pad - 5, r * 2 + pad + 4, r * 2 + pad + 4],
                       outline=AMBER, width=9)
            ox, oy = pin.get("to", [fx, fy])
            tx, ty = bx0 + bw * ox, by0 + bh * oy
            if a > 0.3:                  # đường dẫn từ chỗ được phóng tới vòng
                blend(im, min(1.0, (a - 0.3) / 0.7), 0,
                      lambda d, sx=px, sy=py, tx=tx, ty=ty: d.line(
                          [sx, sy, tx, ty], fill=AMBER, width=6))
            _pop(im, a, tx, ty, tile)
        return t0 + 0.44

    elif kind == "bubble":               # BONG BÓNG THOẠI mọc từ phía nhân vật
        side = pin.get("side", "left")
        # cỡ 56 của bản đầu đọc không nổi ở tệp 45+ (soi sheet) → 78, rộng tới 0,56 ô ảnh
        f = fit(str(pin["t"]), "bold", int(bw * 0.56), pin.get("size", 78), 44)
        txt = str(pin["t"])
        d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        x0, y0, x1, y1 = d0.textbbox((0, 0), txt, font=f)
        pw, ph = x1 - x0 + 72, y1 - y0 + 56
        tile = Image.new("RGBA", (pw + 40, ph + 34), (0, 0, 0, 0))
        d = ImageDraw.Draw(tile)
        d.rounded_rectangle([20, 0, pw + 20, ph], 26, fill=(255, 255, 255, 250),
                            outline=INK + (255,), width=6)
        tail = [(30, ph - 8), (30 + 42, ph - 8), (10, ph + 30)] if side == "left" else \
               [(pw - 10, ph - 8), (pw - 52, ph - 8), (pw + 30, ph + 30)]
        d.polygon(tail, fill=(255, 255, 255, 250), outline=INK + (255,))
        tw(d, ((pw + 40) / 2, ph / 2), txt, f, INK + (255,), anchor="mm")
        _pop(im, a, px, py, tile, pop=1.14)
        return t0 + 0.46

    elif kind == "circle":               # KHOANH ĐỎ vẽ dần quanh một chỗ trên ảnh
        r = bw * pin.get("r", 0.16)
        ry = r * pin.get("ry", 0.78)
        _, p = app(t, t0, 0.62)[0], min(max((t / PACE - t0) / 0.62, 0.0), 1.0)
        if p > 0:
            blend(im, 1.0, 0, lambda d, p=p: d.arc(
                [px - r, py - ry, px + r, py + ry], -96, -96 + 360 * p,
                fill=STK_RED, width=11))
        return t0 + 0.40

    elif kind == "frame":
        # ⭐ 2.8 — KHUNG ĐỎ CHỮ NHẬT vẽ dần quanh một KHỐI CHỮ trên ảnh 原典.
        # Vì sao không dùng `circle`: khoanh ellipse quanh một dòng chữ DÀI thì nó phải
        # rất bẹt, và hai đầu cung ăn vào dòng trên/dưới — đã dính thật ở video 21
        # (padding đoán 6px đè lên chữ dòng dưới ở 2/2 thẻ đầu). Khối chữ là hình chữ
        # nhật ⇒ khoanh bằng hình chữ nhật, và toạ độ lấy từ `genten_boxes.json` do
        # tool chụp đo được, KHÔNG đoán bằng mắt.
        # ⚖️ Khoanh MỌC DẦN (không vẽ sẵn vào ảnh) để nó xuất hiện đúng lúc lời đọc
        # 「赤で囲んだ」 — đây là cả lý do tách khoanh ra khỏi ảnh.
        fx0, fy0, fx1, fy1 = pin.get("box", [0.08, 0.10, 0.92, 0.30])
        rx0, ry0 = bx0 + bw * fx0, by0 + bh * fy0
        rx1, ry1 = bx0 + bw * fx1, by0 + bh * fy1
        prog = min(max((t / PACE - t0) / 0.62, 0.0), 1.0)
        if prog > 0:
            wd = pin.get("w", 9)
            blend(im, 1.0, 0, lambda d, prog=prog, wd=wd: _prog_rect(
                d, rx0, ry0, rx1, ry1, prog, STK_RED, wd))
        return t0 + 0.46

    elif kind == "quote":
        # ⭐ 2.8 — TRÍCH NGUYÊN VĂN đặt DƯỚI/TRÊN ảnh 原典, keyword trong 《》 tô ĐỎ.
        # Đo từ フクロウ 1,63M (`plan` §I.7): thẻ 原典 của nó = screenshot + nhãn TO +
        # **trích nguyên văn, keyword đỏ**, giữ 25–30s. Thẻ 原典 của mình trước đây chỉ
        # có screenshot + khoanh ⇒ chữ web nhỏ, tệp 65+ trên điện thoại không đọc nổi.
        # 🔴 Chữ ở ĐÂY do FONT vẽ nên luôn sắc nét — đó là lý do phải trích lại thành
        # text thay vì trông chờ người xem đọc chữ trong ảnh chụp.
        txt = str(pin["t"])
        maxw = int(bw * pin.get("w", 0.94))
        f = fit_ml(txt, "bold", maxw, pin.get("size", 46), 30)
        pad = 22
        ls = txt.split(NL)
        step = f.size * 1.34
        th = step * (len(ls) - 1) + f.size * 1.20
        tile = Image.new("RGBA", (maxw + pad * 2, int(th) + pad * 2), (0, 0, 0, 0))
        dd = ImageDraw.Draw(tile)
        dd.rounded_rectangle([0, 0, tile.width - 1, tile.height - 1], 14,
                             fill=(255, 253, 247, 250), outline=STK_RED + (255,), width=4)
        tw_ml_kw(dd, (tile.width / 2, tile.height / 2), txt, f, INK + (255,),
                 kw=STK_RED + (255,))
        _pop(im, a, px, py, tile, pop=1.06)
        return t0 + 0.50

    elif kind == "arrow":                # MŨI TÊN ĐỎ trỏ vào một chỗ trên ảnh
        # Cỡ đo theo tệp 45+: bản đầu (len 210 · w 15 · chữ 54) soi ở sheet thì mũi tên
        # mảnh như que và chữ đọc không nổi ⇒ nâng lên. `audience-45plus.md` §1: cái gì
        # nhỏ thì coi như vô hình với nhóm tuổi này.
        L = pin.get("len", 260)
        ux, uy = FLY.get(pin.get("from", "left"), FLY["left"])
        x0, y0 = px + L * ux, py + L * uy
        p = min(max((t / PACE - t0) / 0.50, 0.0), 1.0)
        if p > 0:
            blend(im, 1.0, 0, lambda d, p=p: arrow(
                d, x0, y0, px, py, p, STK_RED, w=pin.get("w", 24)))
        if pin.get("t"):
            f = fit(str(pin["t"]), "black", 440, pin.get("size", 78), 44)
            _pop(im, app(t, t0 + 0.30)[0], x0, y0 - 62,
                 _tile_text(str(pin["t"]), f, STK_RED + (255,), (255, 255, 255, 255), 8))
        return t0 + 0.46

    return t0 + 0.42


def L_art(im, v, t):
    """ẢNH MINH HOẠ LỚN đặt trong bảng trắng — chỗ để tranh AI do user gen.

    ⚠️ Ảnh AI realistic trong video ⇒ phải TICK "altered/synthetic content" lúc upload
    (`.claude/rules/youtube-compliance.md` §2.1). Ảnh THIẾU thì vẽ ô gạch + tên file để
    contact sheet lộ ra ngay, KHÔNG render im lặng ra bảng trống.
    """
    y = title(im, v["title"], t) + 26
    bx0, bx1 = CONTENT_X0 - 30, CONTENT_X1 + 30
    has_cap = bool(v.get("cap"))
    by1 = CARD_Y1 - (104 if has_cap else 44)
    box = (bx0, y, bx1, by1)
    bw, bh = bx1 - bx0, by1 - y
    p = _art_path(v["img"])
    # Ảnh BAY VÀO (mặc định từ dưới lên, quãng dài hơn chữ để thấy rõ là ảnh mới vào)
    t_img = beat(v, 0, 0.70)                # beats[0] = ảnh · pin có khoá "beat" riêng
    alpha, adx, ady = app_fly(t, t_img, v.get("fly", "up"), v.get("fly_dist", 96), 0.60)
    if p is None:
        blend(im, alpha, ady, lambda d: (
            d.rounded_rectangle(box, 16, fill=(250, 246, 236), outline=AMBER, width=5),
            tw(d, ((bx0 + bx1) / 2, y + bh / 2 - 34), "⚠ CHƯA CÓ ẢNH",
               F("black", 56), AMBER, anchor="mm"),
            tw(d, ((bx0 + bx1) / 2, y + bh / 2 + 40), v["img"],
               F("med", 38), mut(v), anchor="mm")), dx=adx)
        # L_art chạy MỖI FRAME (900 frame/clip) → in trần là 900 dòng rác một thẻ.
        if v["img"] not in _MISSING_SEEN:
            _MISSING_SEEN.add(v["img"])
            print(f"       🔴 THIẾU ẢNH: {v['img']} — bỏ file vào art/ rồi dựng lại thẻ này")
    else:
        key = (str(p), bw, bh, p.stat().st_mtime)
        if key not in _ART_CACHE:
            art = Image.open(p).convert("RGBA")
            sc = max(bw / art.width, bh / art.height)      # cover-crop, không méo
            art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                             Image.LANCZOS)
            art = art.crop(((art.width - bw) // 2, (art.height - bh) // 2,
                            (art.width - bw) // 2 + bw, (art.height - bh) // 2 + bh))
            msk = Image.new("L", (bw, bh), 0)
            ImageDraw.Draw(msk).rounded_rectangle([0, 0, bw - 1, bh - 1], 16, fill=255)
            art.putalpha(msk)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            lay.alpha_composite(art, dest=(int(bx0), int(y)))
            _ART_CACHE[key] = lay
        if alpha > 0.004:
            lay = _ART_CACHE[key]
            if alpha < 0.999:
                lay = lay.copy()
                lay.putalpha(lay.getchannel("A").point(lambda vv: int(vv * alpha)))
            im.alpha_composite(lay, dest=(int(round(adx)), int(round(ady))))
        blend(im, alpha, ady,
              lambda d: d.rounded_rectangle(box, 16, outline=LINE, width=3), dx=adx)
    t0 = max(t_img + 0.35, 1.05)
    for pin in v.get("pins", []):
        # `zoom` cần biết ảnh nền của CHÍNH thẻ này để cắt lại vùng phóng đại
        if isinstance(pin, dict) and pin.get("kind") == "zoom":
            pin = dict(pin, _img=v.get("img"))
        # nhịp theo lời đọc: pin dict có khoá "beat" = GIÂY THẬT nó phải hiện (style りょう)
        if isinstance(pin, dict) and pin.get("beat") is not None:
            t0 = float(pin["beat"]) / PACE
        t0 = draw_pin(im, pin, t, t0, bx0, y, bw, bh)
    if has_cap:
        f = fit(plain(v["cap"]), "bold", bx1 - bx0, 44, 30)
        t0 = beat(v, 1, t0)                 # beats[1] = cap (nếu builder ghi)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw_kw(d, ((bx0 + bx1) / 2, by1 + 46), v["cap"],
                                         f, INK2, anchor="mm"))
        t0 += 0.40
    return t0


def _box_art(im, name, box, alpha, adx, ady, v, rad=12):
    """Dán 1 ảnh cover-crop vào hộp bo góc (dùng cho panel của L_pict).
    Thiếu ảnh → ô cảnh báo + ghi _MISSING_SEEN, giống fill_art — KHÔNG im lặng."""
    bx0, by0, bx1, by1 = [int(q) for q in box]
    bw, bh = bx1 - bx0, by1 - by0
    if bw < 8 or bh < 8:
        return
    p = _art_path(name) if name else None
    if p is None:
        blend(im, alpha, ady, lambda d: (
            d.rounded_rectangle([bx0, by0, bx1, by1], rad, fill=(250, 246, 236),
                                outline=AMBER, width=4),
            tw(d, ((bx0 + bx1) / 2, (by0 + by1) / 2 - 20), "⚠ CHƯA CÓ ẢNH",
               F("black", min(40, bh // 6)), AMBER, anchor="mm"),
            tw(d, ((bx0 + bx1) / 2, (by0 + by1) / 2 + 34), str(name or "?"),
               F("med", min(28, bh // 9)), GREY, anchor="mm")), dx=adx)
        if name and name not in _MISSING_SEEN:
            _MISSING_SEEN.add(name)
            print(f"       🔴 THIẾU ẢNH PANEL: {name}")
        return
    # 🔴 `fit`: THẤY TRỌN ảnh thay vì cover-crop. Panel của `pict` là hộp DỌC (~0,53) còn
    # ảnh gen luôn 16:9 ⇒ cover-crop cắt mất ~2/3 bề ngang: ATM không còn nhận ra được, tờ
    # giấy chỉ còn mấy dòng kẻ (đo trên thẻ 今日のお願い, 2026-08-25). Đúng bệnh
    # `media-library.md` §2.10 ②. Với ảnh MINH HOẠ (cần hiểu nội dung) phải fit; ảnh
    # mood/không khí thì cover vẫn tốt hơn nên giữ cover làm mặc định.
    fit_mode = bool(isinstance(v, dict) and v.get("fit"))
    key = (str(p), bw, bh, p.stat().st_mtime,
           ("pbox_fit%.2f" % float(v.get("fit_ar", 16 / 9) if isinstance(v, dict) else 16 / 9))
           if fit_mode else "pbox")
    if key not in _ART_CACHE:
        art = Image.open(p).convert("RGB")
        if fit_mode:
            # `fit_ar`: cắt cover NHẸ về tỉ lệ này TRƯỚC khi fit. Ảnh gen luôn 16:9 (1,78)
            # nên fit vào panel dọc thì rất DẸT ⇒ nhỏ so với khung, thừa trống (user
            # 2026-08-25: "ảnh cho to lên, trông nó nhỏ so với khung"). Cắt về ~1,3 thì
            # cùng bề rộng mà CAO hơn ~37%, chỉ mất ~27% bề ngang — chủ thể ảnh minh hoạ
            # nằm giữa nên không mất nội dung. 1,78 = giữ nguyên như trước.
            ar = float(v.get("fit_ar", 16 / 9)) if isinstance(v, dict) else 16 / 9
            if ar > 0.2 and art.width / art.height > ar:
                nw = int(art.height * ar)
                art = art.crop(((art.width - nw) // 2, 0,
                                (art.width - nw) // 2 + nw, art.height))
            sc = min(bw / art.width, bh / art.height)
            iw, ih = max(1, int(art.width * sc)), max(1, int(art.height * sc))
            pad = Image.new("RGB", (bw, bh), CARDC)
            pad.paste(art.resize((iw, ih), Image.LANCZOS), ((bw - iw) // 2, (bh - ih) // 2))
            art = pad.convert("RGBA")
        else:
            sc = max(bw / art.width, bh / art.height)
            art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                             Image.LANCZOS)
            art = art.crop(((art.width - bw) // 2, (art.height - bh) // 2,
                            (art.width - bw) // 2 + bw,
                            (art.height - bh) // 2 + bh)).convert("RGBA")
        msk = Image.new("L", (bw, bh), 0)
        ImageDraw.Draw(msk).rounded_rectangle([0, 0, bw - 1, bh - 1], rad, fill=255)
        art.putalpha(msk)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        lay.alpha_composite(art, dest=(bx0, by0))
        _ART_CACHE[key] = lay
    if alpha > 0.004:
        lay = _ART_CACHE[key]
        if alpha < 0.999:
            lay = lay.copy()
            lay.putalpha(lay.getchannel("A").point(lambda q: int(q * alpha)))
        im.alpha_composite(lay, dest=(int(round(adx)), int(round(ady))))


# tone panel → (nền, màu chữ label, màu keyword trong label)
PICT_TONES = {"navy": (INK, (255, 255, 255), KW_ON_DARK),
              "red": (RED, (255, 255, 255), KW_ON_DARK),
              "green": (GREEN, (255, 255, 255), KW_ON_DARK),
              "amber": (AMBER, (40, 34, 8), (166, 32, 26)),
              "paper": ((252, 253, 255), INK, KW_ON_LIGHT)}


def L_pict(im, v, t):
    """1–3 PANEL MÀU: label (keyword màu) + ẢNH AI TO — khuôn chủ lực của kênh mẫu りょう.

    Đo từ video 6DN88wQyBFg (節約看護師りょう, 970K view; frame 5:04 · 10:00, 2026-08-19):
    headline hiện TRƯỚC rồi từng panel pop vào theo lời đọc — label 5–10 ký có keyword
    tô màu, dưới là MỘT illustration chiếm ~2/3 panel. HÌNH là nhân vật chính của thẻ,
    không phải icon 132px. Đây là layout cho beat cảm xúc/tình huống; sơ đồ cơ chế vẫn
    là việc của `zu`.

    spec:
      {"layout": "pict", "title": "75歳までは《年金が1円も貰えない》",
       "panels": [{"label": "貯金を《切り崩す》", "img": "art_chokin.png", "tone": "navy"},
                  {"label": "人によって《寿命は違う》", "img": "art_jumyou.png"}],
       "beats": [2.5, 6.0],           # giây thật panel thứ i pop (title không tính)
       "cap": "減額率は《一生続く》"}   # dòng chốt đáy, tuỳ chọn — mốc = beats[n]
    tone: navy (mặc định) · red · green · amber · paper. `pre`: n panel đầu đứng sẵn
    (thẻ nối tiếp không nháy — cùng cơ chế held của check).
    """
    y = title(im, v["title"], t if v.get("pre", 0) == 0 else 99) + 34
    pre = v.get("pre", 0)
    ps = v["panels"][:3]
    n = len(ps)
    has_cap = bool(v.get("cap"))
    by1 = CARD_Y1 - (112 if has_cap else 44)
    gap = 28 if v.get("fit") else 40
    x0, x1 = CONTENT_X0, CONTENT_X1
    if n == 1:                          # 1 panel đứng giữa, co bớt cho khỏi thô
        w1 = (x1 - x0) * 0.66
        x0 = (x0 + x1) / 2 - w1 / 2
        x1 = x0 + w1
    pw = (x1 - x0 - gap * (n - 1)) / n
    # cỡ label ĐỒNG NHẤT giữa các panel — để mỗi panel tự co thì thẻ 2 panel ra 2 cỡ chữ,
    # nhìn như lỗi (kênh mẫu để các label cùng cỡ). Lấy cỡ của label DÀI NHẤT.
    _fs = [fit_ml(plain(pn.get("label", "")), "bold", pw - 48, 52, 30)
           for pn in ps if pn.get("label")]
    f_lab = F("bold", min(f.size for f in _fs)) if _fs else None
    t0 = 0.85
    # 🔴 CANH GIỮA khối panel khi `fit`: khung co lại bao sát ảnh nên khối panel chỉ cao
    # ~40% vùng nội dung ⇒ dồn hết lên trên, nửa dưới card trắng trơn. Dịch xuống cho khối
    # nằm giữa (luật BA KHỐI của `stage-zu-layout.md` §2 nói cùng một chuyện: khoảng trống
    # dồn về MỘT khe là lỗi bố cục, không phải chuyện thẩm mỹ).
    if v.get("fit"):
        _lh = (f_lab.size * 1.28 + 34) if any(pn.get("label") for pn in ps) else 0
        # ⭐ TỰ TÍNH `fit_ar` để khối panel lấp ~86% vùng nội dung. Khai tay một con số thì
        # thẻ 2 panel và thẻ 3 panel ra hai cỡ ảnh khác nhau, và mỗi lần đổi số lại phải
        # dựng lại để nhìn. Kẹp ≥1,05 (crop quá vuông thì mất mép chủ thể) và ≤16/9
        # (không phóng quá ảnh gốc). Khai `fit_ar` tay thì tôn trọng số của builder.
        if not v.get("fit_ar"):
            _avail = (by1 - y) * 0.86 - _lh - 24
            if _avail > 40:
                v["fit_ar"] = max(1.05, min(16 / 9, (pw - 24) / _avail))
        _ph = _lh + 24 + (pw - 24) / max(0.2, float(v.get("fit_ar", 16 / 9)))
        y += max(0.0, (by1 - y - _ph) / 2)

    for i, pn in enumerate(ps):
        tt = beat(v, i, t0)
        if i < pre:
            alpha, adx, ady = 1.0, 0, 0
        else:
            alpha, adx, ady = app_fly(t, tt, pn.get("fly", "up"), 84, 0.55)
        px0 = x0 + i * (pw + gap)
        fill_c, lab_c, kw_c = PICT_TONES.get(pn.get("tone", "navy"), PICT_TONES["navy"])
        lab = pn.get("label", "")
        lab_lines = lab.split(NL) if lab else []
        f = f_lab if lab else None
        lab_h = (len(lab_lines) * f.size * 1.28 + 34) if lab else 0
        # 🔴 KHUNG BAO SÁT ẢNH khi `fit`: hộp panel cao tới đáy card, còn ảnh fit chỉ chiếm
        # dải giữa ⇒ thừa hai khối trắng trên/dưới (đo trên thẻ 今日のお願い). Khi fit thì
        # co khung xuống đúng chiều cao ảnh (bề rộng trong × 9/16 vì ảnh gen luôn 16:9).
        pb1 = by1
        if v.get("fit"):
            _ar = float(v.get("fit_ar", 16 / 9))
            pb1 = min(by1, y + lab_h + 24 + (pw - 24) / max(0.2, _ar))
        blend(im, alpha, ady, lambda d, px0=px0, fill_c=fill_c, lab=lab, f=f, pb1=pb1,
              lab_lines=lab_lines, lab_c=lab_c, kw_c=kw_c, lab_h=lab_h: (
            d.rounded_rectangle([px0, y, px0 + pw, pb1], 18, fill=fill_c,
                                outline=LINE if fill_c == PICT_TONES["paper"][0] else None,
                                width=3),
            [tw_kw(d, (px0 + pw / 2, y + 34 + j * f.size * 1.28), ln, f, lab_c, kw_c,
                   anchor="mm") for j, ln in enumerate(lab_lines)] if lab else None),
              dx=adx)
        _m = 12 if v.get("fit") else 18      # fit: lề mỏng hơn để ảnh to hết chỗ
        _box_art(im, pn.get("img"), (px0 + _m, y + lab_h + _m, px0 + pw - _m, pb1 - _m),
                 alpha, adx, ady, v)
        t0 = tt + 0.55
    if has_cap:
        f = fit(plain(v["cap"]), "bold", CONTENT_X1 - CONTENT_X0, 46, 30)
        t0 = beat(v, n, t0)
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw_kw(d, ((CONTENT_X0 + CONTENT_X1) / 2, by1 + 52),
                                         v["cap"], f, INK, anchor="mm"))
        t0 += 0.42
    return t0


def L_steps(im, v, t):
    """BẬC THANG DỌC — số thứ tự chạy XUỐNG, có đường nối dọc.

    Sinh 2026-08-09 (user: "đừng trình bày rập khuôn theo kiểu hàng ngang… trình dữ liệu
    hàng dọc, nhánh cây các kiểu"). Trước đó 59/132 thẻ là `check` (danh sách ngang) và
    `flow`/`bars`/`timeline` cũng ngang ⇒ gần như cả video một hướng đọc.
    Dùng cho: chuỗi THAO TÁC có thứ tự (4 bước gửi trả đơn), không dùng cho liệt kê rời.
    """
    pre = v.get("pre", 0)
    y = title(im, v["title"], t if pre == 0 else 99) + 54
    rows = v["steps"]
    n = len(rows)
    # 🔴 GIÃN 3 CỘT (user chốt 2026-08-10: "các số thứ tự cách các hình ra tí cho có khoảng trống").
    # Đo bản cũ: badge 534–598px · icon 592–648px ⇒ **chồng nhau 6px**, và icon cách chữ chỉ 22px.
    # Bản mới: badge 528–592 · khe 34 · icon 626–682 · khe 36 · chữ từ 718.
    x_dot = CONTENT_X0 + 40
    x_ic = x_dot + 32 + 34          # mép trái icon = mép phải badge + khe
    x_txt = x_ic + 56 + 36          # chữ = mép phải icon + khe
    gap = min(132, (CARD_Y1 - 70 - y) / max(1, n))
    t0 = 0.72
    for i, row in enumerate(rows):
        ic, txt = (row if isinstance(row, (list, tuple)) else ("doc", row))
        cy = y + gap * i + gap / 2
        f = fit(txt, "bold", CONTENT_X1 - x_txt - 20, 48, 30)
        a, dy = held(t, t0, i, pre)
        # đường nối DỌC vẽ trước, tới đốt kế tiếp
        if i < n - 1:
            p2 = 1.0 if i < pre - 1 else prog(t, t0 + 0.18, 0.34)
            if p2 > 0.01:
                blend(im, 1.0, 0, lambda d, cy=cy, p2=p2: d.line(
                    [x_dot, cy + 34, x_dot, cy + 34 + (gap - 68) * p2], fill=LINE, width=6))
        blend(im, a, dy, lambda d, cy=cy, i=i, ic=ic, txt=txt, f=f: (
            d.ellipse([x_dot - 32, cy - 32, x_dot + 32, cy + 32], fill=AMBER),
            tw(d, (x_dot, cy), str(i + 1), F("black", 40), (40, 34, 8), anchor="mm"),
            icon(d, ic, x_ic, cy - 28, 56),
            tw(d, (x_txt, cy), txt, f, INK, anchor="lm")))
        t0 += 0.44
    if v.get("note"):
        a, dy = app(t, t0)
        blend(im, a, dy, lambda d: tw(d, ((CONTENT_X0 + CONTENT_X1) / 2, CARD_Y1 - 54),
                                      v["note"], F("med", 34), mut(v), anchor="mm"))
        t0 += 0.36
    return fill_art(im, v, t, t0)


def L_tree(im, v, t):
    """NHÁNH CÂY — gốc bên TRÁI, các nhánh xoè xuống bên PHẢI.

    Dùng cho ngã rẽ quyết định (làm gì → hệ quả gì) và cho "một gốc, nhiều trường hợp".
    Đây là hướng đọc THỨ BA của bộ layout (ngang · dọc · toả nhánh).
    """
    pre = v.get("pre", 0)
    y = title(im, v["title"], t if pre == 0 else 99) + 40
    br = v["branches"]
    n = len(br)
    x_root, w_root = CONTENT_X0 - 10, 250
    x_br = CONTENT_X0 + 330
    top = y + 30
    bot = CARD_Y1 - 90
    gap = (bot - top) / n
    cy_root = (top + bot) / 2
    a, dy = (1.0, 0) if pre else app(t, 0.68)
    fr = fit_ml(v["root"], "black", w_root - 24, 44, 28)
    blend(im, a, dy, lambda d: (
        d.rounded_rectangle([x_root, cy_root - 74, x_root + w_root, cy_root + 74], 18,
                            fill=INK),
        tw_ml(d, (x_root + w_root / 2, cy_root), v["root"], fr, (255, 255, 255))))
    t0 = 1.02
    for i, b in enumerate(br):
        cy = top + gap * i + gap / 2
        tone = b.get("tone", "amber")
        col = {"amber": AMBER, "ok": GREEN, "bad": RED, "grey": GREY}.get(tone, AMBER)
        p = 1.0 if i < pre else prog(t, t0 - 0.22, 0.36)   # cành MỌC ra từ gốc
        if p > 0.01:
            xm = x_root + w_root + 40
            blend(im, 1.0, 0, lambda d, cy=cy, p=p, col=col, xm=xm: (
                d.line([x_root + w_root, cy_root, xm, cy_root], fill=col, width=7),
                d.line([xm, cy_root, xm, cy_root + (cy - cy_root) * p], fill=col, width=7),
                d.line([xm, cy, xm + (x_br - xm) * max(0.0, (p - .6) / .4), cy],
                       fill=col, width=7)))
        f = fit(b["label"], "black", CONTENT_X1 - x_br - 40, 52, 32)
        a, dy = held(t, t0, i, pre)
        blend(im, a, dy, lambda d, cy=cy, b=b, f=f, col=col: (
            d.rounded_rectangle([x_br, cy - 62, CONTENT_X1 + 20, cy + 62], 14,
                                fill=(252, 253, 255), outline=col, width=4),
            d.rounded_rectangle([x_br, cy - 62, x_br + 12, cy + 62], 6, fill=col),
            tw(d, (x_br + 36, cy - 20), b["label"], f, INK, anchor="lm"),
            tw(d, (x_br + 36, cy + 26), b.get("cap", ""),
               fit(b.get("cap", ""), "bold", CONTENT_X1 - x_br - 60, 36, 24), INK2, anchor="lm")))
        t0 += 0.46
    return t0


# ══════════════════════════════════════════════════════ zu — SƠ ĐỒ TỰ DO
# 🔴 VÌ SAO CÓ LAYOUT NÀY (user chốt 2026-08-17, dán 3 frame của kênh cùng ngách:
#    「消えるのは自分の道」・「今日は計算をしません」・「役所の窓口」):
#    *"tao muốn sinh ra các hình như này chứ không thuần text nhé"*.
#    Mười layout trước đều là BẢNG (hàng/cột/hộp xếp thẳng) — chữ là nội dung chính, hình chỉ
#    là icon trang trí đầu dòng. Cái đối thủ làm là **SƠ ĐỒ**: vài vật đặt tự do, nối bằng mũi
#    tên, một bong bóng thoại, một dấu ✗ to. Người xem HIỂU BẰNG HÌNH rồi mới đọc chữ.
#
# CÁCH ĐẶT — TOẠ ĐỘ PHÂN SỐ, không phải pixel:
#    "at": [fx, fy] với fx,fy ∈ 0..1 của HỘP SƠ ĐỒ. Đổi hộp (vì title dài hơn, vì cast rộng
#    hơn) thì cả sơ đồ tự co theo, không phải đi sửa từng con số như bản pixel.
#
# 🔴 BỀ NGANG: [ZU_X0, ZU_X1] = [530, 1480] RỘNG HƠN [CONTENT_X0, CONTENT_X1] = [520, 1400].
#    Đo bằng máy chứ không đoán (LUẬT SỐ 1): cast phải hẹp nhất trong bộ là `tanaka_*` bắt đầu
#    ở x=1525 ⇒ 1480 còn chừa 45px. Chỉ được nới tới đây; nới nữa là chữ chui xuống dưới người.
#
# BUILD-ON: node hiện theo THỨ TỰ trong list; edge tự hiện SAU cả hai đầu của nó
#    (t0 = max(t0[from], t0[to]) + 0.22) ⇒ không phải khai mốc thời gian tay.
ZU_X0, ZU_X1 = 530, 1480
ZU_PALE = (238, 243, 250)      # nền tròn xanh-nhạt (đo từ frame đối thủ)
ZU_DASH = (198, 205, 216)


def _dash_line(d, x0, y0, x1, y1, c, w=6, on=16, off=14, p=1.0):
    """Đường KẺ CHẤM — PIL không có dash, phải tự chia đoạn."""
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1:
        return
    ux, uy, cur = (x1 - x0) / L, (y1 - y0) / L, L * p
    s = 0.0
    while s < cur:
        e = min(s + on, cur)
        d.line([x0 + ux * s, y0 + uy * s, x0 + ux * e, y0 + uy * e], fill=c, width=w)
        s = e + off


def _dash_ellipse(d, box, c, w=6, seg=26):
    """Vòng tròn nét đứt (image 4: 保険なし = khiên viền đứt = 'cái KHÔNG có')."""
    x0, y0, x1, y1 = box
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    cx, cy = x0 + rx, y0 + ry
    n = max(int(math.pi * (rx + ry) / seg), 8)
    n -= n % 2
    for i in range(0, n, 2):
        a0, a1 = 360 * i / n, 360 * (i + 1) / n
        d.arc([cx - rx, cy - ry, cx + rx, cy + ry], a0, a1, fill=c, width=w)


def _spark(d, cx, cy, r=44, c=AMBER):
    """Ba tia vàng — 'chỗ này đấy' (image 2 quanh cửa sắt, image 3 quanh 土俵)."""
    for a in (-38, 0, 38):
        ra = math.radians(a - 90)
        d.line([cx + math.cos(ra) * r * .52, cy + math.sin(ra) * r * .52,
                cx + math.cos(ra) * r, cy + math.sin(ra) * r], fill=c, width=9)


def _cross(d, cx, cy, r, c=AMBER):
    """Dấu ✗ TO đè lên vật — 'cái này không dùng' (image 3: máy tính bị gạch)."""
    for a, b in (((-1, -1), (1, 1)), ((-1, 1), (1, -1))):
        d.line([cx + a[0] * r, cy + a[1] * r, cx + b[0] * r, cy + b[1] * r],
               fill=c, width=18, joint="curve")


def _bubble(d, cx, cy, text, f, tail="down", pad=26):
    """Bong bóng thoại — đuôi chỉ về phía vật nó đang nói."""
    ls = text.split(NL)
    wmax = max(f.getbbox(l)[2] - f.getbbox(l)[0] for l in ls)
    bw, bh = wmax + pad * 2, f.size * 1.34 * len(ls) + pad * 1.4
    x0, y0, x1, y1 = cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2
    d.rounded_rectangle([x0, y0, x1, y1], 22, fill=CARDC, outline=INK, width=5)
    t = {"down": [(cx - 22, y1 - 3), (cx + 22, y1 - 3), (cx - 4, y1 + 32)],
         "up": [(cx - 22, y0 + 3), (cx + 22, y0 + 3), (cx - 4, y0 - 32)],
         "left": [(x0 + 3, cy - 20), (x0 + 3, cy + 20), (x0 - 32, cy + 2)],
         "right": [(x1 - 3, cy - 20), (x1 - 3, cy + 20), (x1 + 32, cy + 2)]}[tail]
    d.polygon(t, fill=CARDC)
    d.line([t[2], t[0]], fill=INK, width=5)
    d.line([t[2], t[1]], fill=INK, width=5)
    tw_ml(d, (cx, cy), text, f, INK)


AMBER_PALE = (255, 244, 214)     # nền banner đáy (đo từ frame đối thủ)
XRED = (231, 76, 60)             # dấu ✗ ĐỎ vắt qua "đường sai"


def _zu_badge(d, cx, cy, hw, hh, num):
    """Số ❶❷❸ trong vòng navy, dán góc TRÊN-TRÁI node — thứ tự đọc của cột lựa chọn."""
    bx, by, r = cx - hw + 6, cy - hh + 6, 30
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=INK)
    tw(d, (bx, by - 2), str(num), F("black", 36), (255, 255, 255), anchor="mm")


def _zu_group(d, n, cx, cy, s):
    """HỘP LỚN: viền + tiêu đề trên + icon TO giữa + dòng chốt dưới (± hero tròn vàng).

    🔴 Đây là thứ 3/4 frame mẫu đều có mà `zu` bản đầu KHÔNG có: một khung bo góc **nhóm**
    nhiều phần tử thành MỘT ý, thay vì rải node rời khắp bảng. Không có nó thì bảng nhìn
    như danh sách vật, không ra "hai lối" / "một cái này → ba cái kia"."""
    w, h = n.get("w", 440) * s, n.get("h", 330) * s
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    col = ZU_TONE.get(n.get("tone", "ink"), INK)
    d.rounded_rectangle([x0, y0, x1, y1], 20, fill=(253, 252, 247), outline=col, width=5)
    y = y0 + 26
    if n.get("head"):
        f = fit_ml(n["head"], "black", w - 44, int(40 * s), 28)
        nl = len(n["head"].split(NL))
        tw_ml(d, (cx, y + f.size * 1.34 * (nl - 1) / 2 + f.size * 0.5), n["head"], f, INK)
        y += f.size * 1.34 * nl + 14
    foot_h = 0
    if n.get("foot"):
        # 🔴 `foot` phải NHIỀU DÒNG như `head` (vá 2026-08-17): cột dọc dùng `foot` chở nhãn
        # vật, và nhãn thật có xuống dòng (「ご近所への\nお付き合い」). Bản `fit` một dòng vẽ
        # nguyên cả ký tự xuống dòng thành hình chữ nhật rỗng — lỗi im lặng, chỉ lộ khi soi 1:1.
        lines = n["foot"].split(NL)
        ff = fit_ml(n["foot"], "black", w - 44, int(40 * s), 26)
        nlf = len(lines)
        foot_h = ff.size * 1.34 * (nlf - 1) + ff.size + 22
        tw_ml(d, (cx, y1 - 22 - foot_h / 2 + 11), n["foot"], ff, INK)
        if n.get("under"):
            wl = max(ff.getlength(x) for x in lines)
            d.line([cx - wl / 2, y1 - 12, cx + wl / 2, y1 - 12], fill=AMBER, width=9)
    mid_y = (y + (y1 - foot_h - 18)) / 2
    if n.get("hero"):            # số hero trong ĐĨA VÀNG (「戻る 7~8割」)
        r = min(w * 0.3, (y1 - foot_h - 18 - y) * 0.48)
        d.ellipse([cx - r, mid_y - r, cx + r, mid_y + r], fill=AMBER)
        fh = fit(n["hero"], "black", r * 1.7, int(r * 0.95), 30)
        tw(d, (cx, mid_y), n["hero"], fh, (40, 34, 8), anchor="mm")
    elif n.get("icon"):
        ss = n.get("iconsize", 150) * s
        icon(d, n["icon"], cx - ss / 2, mid_y - ss / 2, ss)


def _zu_banner(d, n, cx, cy):
    """DẢI ĐÁY: nền vàng nhạt (hoặc trắng viền navy) + icon nhỏ + câu chốt gạch chân vàng."""
    w = n.get("w", 950)
    x0, x1 = cx - w / 2, cx + w / 2
    y0, y1 = cy - 52, cy + 52
    if n.get("tone") == "ink":
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill=CARDC, outline=INK, width=5)
    else:
        d.rounded_rectangle([x0, y0, x1, y1], 16, fill=AMBER_PALE)
    # 🔴 CĂN GIỮA CẢ NHÓM (icon + chữ), KHÔNG dán chữ vào mép trái (user bắt 2026-08-17:
    # *"text dưới thì căn giữa chứ"*). Bản đầu vẽ `anchor="lm"` tại `x0+30` ⇒ câu ngắn thì
    # chữ nằm lệch hẳn về trái trong một dải rộng 950px, hở một khoảng trống bên phải —
    # nhìn như dải bị tràn ra khỏi chữ. Dải là KHUNG, chữ phải ở tâm khung.
    lab = n.get("label", "")
    ic_w = 90 if n.get("icon") else 0
    f = fit(lab, "black", (x1 - x0) - 60 - ic_w, 48, 30)
    grp = ic_w + f.getlength(lab)
    tx = cx - grp / 2
    if n.get("icon"):
        icon(d, n["icon"], tx, cy - 34, 68)
        tx += 90
    tw(d, (tx, cy), lab, f, INK, anchor="lm")
    if n.get("under", True):
        d.line([tx, cy + f.size * 0.62, tx + f.getlength(lab), cy + f.size * 0.62],
               fill=AMBER, width=9)


def _zu_ribbon(d, n, cx, cy):
    """CỜ ĐUÔI NHEO vàng — câu hero trên đầu, hai đầu khuyết hình chữ V."""
    f = fit(n.get("label", ""), "black", n.get("lw", 900), 62, 38)
    hw = f.getlength(n["label"]) / 2 + 96
    x0, x1, y0, y1 = cx - hw, cx + hw, cy - 52, cy + 52
    d.polygon([(x0, y0), (x1, y0), (x1 - 40, cy), (x1, y1), (x0, y1), (x0 + 40, cy)],
              fill=AMBER)
    tw(d, (cx, cy), n["label"], f, (40, 34, 8), anchor="mm")


def _zu_chip(d, n, cx, cy):
    """Nhãn nhỏ nền vàng ở góc + tia — 「5日以内」「74歳まで」."""
    f = fit(n.get("label", ""), "black", n.get("lw", 300), 42, 28)
    hw = f.getlength(n["label"]) / 2 + 34
    d.rounded_rectangle([cx - hw, cy - 36, cx + hw, cy + 36], 12, fill=AMBER)
    tw(d, (cx, cy), n["label"], f, (40, 34, 8), anchor="mm")


ZU_TONE = {"amber": AMBER, "pale": ZU_PALE, "grey": (233, 235, 239),
           "ink": INK, "ok": GREEN, "bad": RED, "none": None}
# 🔴 EDGE dùng BẢNG MÀU RIÊNG. Màu `grey` của node là màu TÔ NỀN tròn (233,235,239) — kẻ
# thành ĐƯỜNG trên card kem (255,250,238) thì chênh 22 mức, mắt không thấy (bắt được ở
# mẫu t3: nhánh 「20年ない」 vô hình). Đường cần màu đủ tối, nền cần màu đủ nhạt — hai vai
# khác nhau, không dùng chung một hằng số.
ZU_ETONE = {**ZU_TONE, "grey": ZU_DASH, "pale": (214, 222, 234)}


def _zu_box(n):
    """(nửa bề ngang, cao LÊN, cao XUỐNG) của node **KỂ CẢ NHÃN dưới nó**.
    Dùng để KẸP vị trí và để phát hiện CHỒNG NHAU.

    🔴 VÌ SAO TÁCH KHỎI `_zu_extent`: bản đầu chỉ đo VẬT ⇒ hai `circle` xếp dọc (`at[1]`
    0.30 và 0.86) trông "không chồng" theo gate, nhưng **nhãn 2 dòng của cái trên đâm vào
    cái dưới**. Ca thật: thẻ 02 video 13 hiện 「ご主人／奧さ…／9万円」 chồng chữ, chỉ lộ khi soi
    frame. Mũi tên thì vẫn cắt theo VẬT (`_zu_extent`), không theo nhãn.

    🔴 VÀ PHẢI BẤT ĐỐI XỨNG. Bản vá đầu trả hộp đối xứng `hh = shape + blk/2` — sai, vì nhãn
    nằm HẲN Ở DƯỚI. Kẹp theo hộp đối xứng vẫn để đáy nhãn tràn 50px, `_zu_label` bèn LẬT nhãn
    lên trên, và nó hạ cánh đúng vào nhãn của node phía trên ⇒ **lỗi y như cũ, chỉ đổi chỗ**.
    Đây là lần thứ hai trong cùng một buổi mà "đo gần đúng" đẻ ra lỗi mới; đo đúng thì hết."""
    hw, hh = _zu_extent(n)
    up = down = hh
    lab = n.get("label", "")
    if lab and n.get("kind", "circle") in ("circle", "mark", "icon", "bigicon"):
        s = n.get("s", 1.0)
        f = fit_ml(lab, "bold", n.get("lw", 300) * s, int(38 * s), 26)
        nl = len(lab.split(NL))
        down = hh + 20 + f.size * 1.34 * (nl - 1) + f.size + 6
        hw = max(hw, max(f.getlength(x) for x in lab.split(NL)) / 2)
    return hw, up, down


def _zu_extent(n):
    """(nửa bề ngang, nửa chiều cao) của riêng HÌNH VẼ (không gồm nhãn) — để cắt mũi tên.

    🔴 LUẬT SỐ 1 áp vào đây: bản đầu cắt mũi tên bằng hằng số `shrink=92` đoán tay, nên
    edge tới một `panel` (330×210) vẫn đâm vào giữa hộp, và nhãn edge nằm đè lên băng navy
    của hộp đó (dính ở mẫu t3: 「自分で見る」 bị 「ねんきん定期便」 ăn mất một nửa).
    Cắt theo KÍCH THƯỚC THẬT thì mọi cặp node tự đúng, không phải chỉnh tay từng edge."""
    s = n.get("s", 1.0)
    k = n.get("kind", "circle")
    if k == "circle":
        return 92 * s, 92 * s
    if k == "mark":
        return 78 * s, 78 * s
    if k == "panel":
        return 165 * s, 105 * s
    if k == "icon":
        return 95 * s, 95 * s
    if k == "label":
        # `hero: true` = hộp SỐ ĐẮT của thẻ spine — cỡ chữ gấp đôi (92 vs 46).
        base = 92 if n.get("hero") else 46
        # 🔴 LABEL CÓ THỂ 2 DÒNG (ZU_CAP cho phép, khuôn `line()` video 14 dùng thật) —
        # bản cũ đo 1 dòng ⇒ khung bao dòng 1, dòng 2 LÒI RA (user bắt 2026-08-19 clip_12).
        # Cao: cộng leading từng dòng thêm. Ngang: dòng DÀI NHẤT, không phải tổng ký cả chuỗi.
        ls_ = n.get("label", "").split(NL)
        hh = base * s * 0.82 + (len(ls_) - 1) * base * s * 0.61
        # 🔴 `bw` = BỀ NGANG HỘP CỐ ĐỊNH. Vì sao cần: hộp `label` tự co theo SỐ KÝ TỰ, nên hai
        # hàng song song (lưới 2×2 · hai nhánh của một sơ đồ) có ô rộng khác nhau ⇒ khe còn lại
        # khác nhau ⇒ **mũi tên dài khác nhau** (đo được ở thẻ 65: 371px vs 117px). Mắt đọc ngay
        # ra "không đều" mà không biết vì sao. Ô cùng vai thì phải cùng bề ngang — như ô bảng.
        if n.get("bw"):
            return n["bw"] * s / 2, hh
        return (min(n.get("lw", 470) * s, max(len(x) for x in ls_) * base * s) / 2 + 30,
                hh)
    if k == "bubble":
        return n.get("lw", 340) * s / 2 + 26, 60 * s
    # ── kind thêm 2026-08-17 (user dán 4 frame nữa: "nhiều hình minh hoạ như này") ──
    if k == "group":            # HỘP LỚN nhóm nội dung: tiêu đề + icon to + dòng chốt
        return n.get("w", 440) * s / 2, n.get("h", 330) * s / 2
    if k == "banner":           # DẢI ĐÁY full-width, câu chốt gạch chân vàng
        return n.get("w", 950) / 2, 54
    if k == "ribbon":           # CỜ ĐUÔI NHEO vàng, câu hero trên đầu
        f = fit(n.get("label", ""), "black", n.get("lw", 900), 62, 38)
        return f.getlength(n.get("label", "")) / 2 + 96, 56
    if k == "chip":             # nhãn nhỏ nền vàng ở góc (「5日以内」)
        f = fit(n.get("label", ""), "black", n.get("lw", 300), 42, 28)
        return f.getlength(n.get("label", "")) / 2 + 34, 40
    if k == "oval":             # ellipse DỌC — cột 3 lựa chọn của ảnh mẫu
        return 96 * s, 132 * s
    if k == "bigicon":          # vật TO không khung (đồng hồ cát, ví + hoá đơn)
        return n.get("size", 250) * s / 2, n.get("size", 250) * s / 2
    return 92 * s, 92 * s


ZU_CAST_L, ZU_CAST_R = 528, 1525
"""x mà nhân vật hai mép có thể chạm tới — ĐO BẰNG MÁY trên cả bộ `assets/cast`:
trái `sensei_*` (rộng nhất, 562px) tới x=528 · phải hẹp nhất `tanaka_*` bắt đầu ở x=1525.
Đổi bộ cast ⇒ đo lại, đừng đoán.

🔴 VÌ SAO KHÔNG TỰ ĐO Ở RUNTIME (thử và LOẠI 2026-08-17): công thức
`L = -34 + w_rộng_nhất` tái tạo ĐÚNG 528, nhưng `R = 1920 - w_hẹp_nhất + 34` ra **1723**,
không phải 1525 — vì 1525 lấy theo `tanaka_*` (bộ thật dùng ở bên phải), còn `josei_down`
hẹp hơn nhiều lại không dùng bên phải. Bật auto-measure ⇒ nới biên node nenkin thêm 198px
sang phải, có thể đè lên nhân vật. ⇒ Giữ hằng số này làm MẶC ĐỊNH (nenkin không đổi một
byte) và cho kênh khác ghi đè bằng `stage_zu_cast` trong `channels.py`."""

# Ảnh chụp MẶC ĐỊNH, chốt TRƯỚC khi `--channel`/`--cast-dir` kịp ghi đè. `_sig()` so với bộ
# này để biết kênh có lệch mặc định hay không → chỉ kênh LỆCH mới có thêm phần tử trong chữ
# ký, nhờ vậy sig của nenkin/kaigo/akiya bất biến và clip cũ không phải dựng lại.
# ⚠️ Phải đặt SAU cả `CAST_SCALE` (≈L256) và `ZU_CAST_L/R` — đặt cạnh `CAST_DEFAULT` ở trên
#    thì NameError vì hai cái đó chưa tồn tại.
_CAST_DEFAULT_DIR = str(CAST)
_CAST_SCALE_DEFAULT = dict(CAST_SCALE)
_ZU_CAST_DEFAULT = (ZU_CAST_L, ZU_CAST_R)


def _zu_place(v):
    """→ {id: (cx, cy)} đã **TỰ KẸP** để hộp bao node không đụng nhân vật / tràn card.

    🔴 VÌ SAO PHẢI KẸP, KHÔNG PHẢI BẮT NGƯỜI VIẾT SLIDES CHỈNH TAY:
    `at` là TÂM node, nên cùng một `at[0]=0.10` thì hộp `label` 6 ký (rộng 290px) tràn vào
    người còn `circle` (184px) thì không. Bản đầu không kẹp ⇒ gate báo **25 lỗi** trên 52 thẻ,
    tức người viết phải nhớ bề rộng của từng kind — đúng kiểu luật "kiểm bằng mắt thì sẽ trôi".
    Kẹp xong thì `at` trở thành "chỗ tao MUỐN đặt", tool lo phần không đụng ai.
    Hàm này là NGUỒN SỰ THẬT DUY NHẤT cho cả `L_zu` (vẽ) và `zu_check` (gate)."""
    y0 = CARD_Y0 + 74 + 62 + 34 if v.get("title") else CARD_Y0 + 40
    by1 = CARD_Y1 - 34
    out = {}
    for n in v["nodes"]:
        hw, up, down = _zu_box(n)
        # ① kẹp DỌC trước — vì biên NGANG phụ thuộc việc node có nằm trên đầu nhân vật hay không
        cy = y0 + (by1 - y0) * n["at"][1]
        # 🔴 LỀ ĐÁY 44px (12 → 26 → 44, siết dần theo đúng hai lần user chỉ). 12px là "vừa đủ
        # không tràn", và MỌI hàng có `at[1]` 0,8–0,99 đều bị kẹp về đúng mốc đó ⇒ dải kết/nhãn
        # NGỒI TRÊN MÉP card. Đây là chỗ SỬA ĐÚNG (kẹp), không phải `zu_fit` — hai lần trước tao
        # siết lề trong `zu_fit` mà số không đổi, vì kẹp mới là thứ quyết định vị trí cuối.
        # ⚠️ Đổi số này thì lưới 2×2 của builder phải hạ `at[1]` theo (hàng 2 + `cap` cùng bị đẩy
        # lên) — xem `build_slides_13.py::slots`. Đừng đổi lẻ một bên.
        # 🔴 TRẦN TRÊN = `y0` (đáy tiêu đề), KHÔNG PHẢI mép card + 12 (user bắt 2026-08-17:
        # *"cái khung text trên cùng góc phải cho thấp xuống chứ"*). `y0` là thang mà mapping
        # dùng, nhưng kẹp lại cho phép node leo tới `CARD_Y0+12` ⇒ bong bóng `at[1]=0,04` ngồi
        # cách chữ tiêu đề 22px, đọc thành hai dòng chữ dính nhau. Kẹp bằng `y0` thì band và
        # kẹp NHẤT QUÁN: `at[1]=0` nghĩa là "cao nhất được phép", không ai vượt lên trên nữa.
        lo, hi = (y0 if v.get("title") else CARD_Y0 + 12) + up, CARD_Y1 - 44 - down
        cy = (lo + hi) / 2 if lo > hi else min(max(cy, lo), hi)
        # ② node nằm TRỌN TRÊN đỉnh nhân vật (y=CH_TOP=368) thì được dùng TRỌN BỀ NGANG CARD.
        # 🔴 Đây là lý do `ribbon`/`chip` của frame mẫu rộng gần hết khung mà không chạm ai:
        # nhân vật chỉ cao 560px tính từ đáy, phần trên card là đất trống. Không có nhánh này
        # thì cờ vàng bị bó vào khe 950px giữa hai người, hết ra "biển hiệu".
        # 🔴 CHỈ CỜ/BONG BÓNG ĐƯỢC DÙNG KHUNG RỘNG (siết 2026-08-17). Bản đầu chỉ hỏi
        # "node có nằm trọn trên đỉnh nhân vật không", mà mốc đó RĂNG DAO: thẻ 30 có hàng 1 ở
        # y=366,4 — trên `CH_TOP=368` đúng **1,6px** ⇒ hàng 1 lấy khung 312–1608, hàng 2 lấy
        # khung 540–1505, cùng `at[0]=0,14` mà ra cx 512 vs 740 ⇒ **mũi tên 336px vs 108px**.
        # Cùng bẫy đã dính ở lưới 2×2 (thẻ 65). Với HÀNG NỘI DUNG, `at[0]` phải nghĩa một điều
        # duy nhất trong cả thẻ, nên chốt: khung rộng chỉ dành cho thứ SINH RA để trải ngang.
        if cy + down < CH_TOP and (n.get("kind", "circle") in ("ribbon", "chip", "banner",
                                                              "bubble")
                                   or n["at"][1] <= 0.08):
            bx0, bx1 = CARD_X0 + 40, CARD_X1 - 40
        else:
            bx0, bx1 = ZU_CAST_L + 12, ZU_CAST_R - 20
        cx = ZU_X0 + (ZU_X1 - ZU_X0) * n["at"][0] if cy + down >= CH_TOP else \
            bx0 + (bx1 - bx0) * n["at"][0]
        lo, hi = bx0 + hw, bx1 - hw
        cx = (lo + hi) / 2 if lo > hi else min(max(cx, lo), hi)
        out[n["id"]] = (cx, cy)
    return out


def zu_row(items, y, x0=0.0, x1=1.0, wide=False, mingap=96):
    """Phân bố `items` thành MỘT HÀNG NGANG, khoảng cách đều, TÍNH THEO BỀ RỘNG THẬT.

    🔴 VÌ SAO CÓ: gõ `at[0]` tay cho một hàng 3–4 node là **đoán bề rộng**, và đoán sai thì
    node chồng nhau — dính ngay ở 2/4 khuôn mới (3 oval của 「74歳まで」 và 3 hộp amber của
    「表の中身を変えるものが3つ」 đều đè lên nhau). Hàm này đo `_zu_extent` từng node rồi chia
    khe còn lại thành các gap BẰNG NHAU ⇒ không bao giờ chồng, và tự cân khi đổi cỡ chữ.

    `wide=True` = hàng nằm TRÊN đỉnh nhân vật (dùng trọn bề ngang card).
    Trả về chính `items` (đã set `at`) để viết gọn trong SLIDES."""
    bx0, bx1 = ((CARD_X0 + 40, CARD_X1 - 40) if wide else (ZU_CAST_L + 12, ZU_CAST_R - 20))
    L, R = bx0 + (bx1 - bx0) * x0, bx0 + (bx1 - bx0) * x1
    ws = [_zu_extent(n)[0] * 2 for n in items]
    # 🔴 GAP TỐI THIỂU 96px khi hàng có mũi tên nối: `arrow()` cần ~26px cho đầu mũi, cộng
    # 18px chừa mỗi đầu (`_zu_trim`) ⇒ dưới 60px là mũi tên teo thành dấu chấm. `zu_row` bản
    # đầu chỉ chia đều rồi cảnh báo, nên vẫn ra 24–40px và gate phải hét 4 lần.
    # Nay TỰ THU NHỎ node cho đủ chỗ — người viết khai "4 node một hàng có mũi tên", tool lo cỡ.
    need = mingap * max(len(items) - 1, 0)
    if len(items) > 1 and sum(ws) + need > (R - L):
        k = max((R - L) - need, 120) / sum(ws)
        for n in items:
            n["s"] = round(n.get("s", 1.0) * k, 3)
        ws = [_zu_extent(n)[0] * 2 for n in items]
        print(f"  [zu_row] {len(items)} node → thu nhỏ ×{k:.2f} để chừa gap {mingap}px")
    gap = ((R - L) - sum(ws)) / max(len(items) - 1, 1) if len(items) > 1 else 0
    x = L
    for n, w in zip(items, ws):
        # `at` là phân số của HỘP mà `_zu_place` dùng ⇒ phải quy ngược đúng hệ đó
        cx = x + w / 2
        base0, base1 = ((CARD_X0 + 40, CARD_X1 - 40) if wide else (ZU_X0, ZU_X1))
        n["at"] = [(cx - base0) / (base1 - base0), y]
        x += w + gap
    return items


# ══════════════════════ CÂN DỌC — chống LỌT (bổ sung 2026-08-17) ═══════════════════════
ZU_FILL = 0.86     # nội dung phải lấp ~86% chiều cao band còn lại
ZU_KMAX = 1.75     # trần phóng to (trên mức này bong bóng/số nuốt cả bảng)
ZU_ROWTOL = 0.07   # `at[1]` lệch dưới mức này = CÙNG MỘT HÀNG
ZU_SCALABLE = ("circle", "mark", "icon", "bigicon", "label", "bubble", "oval",
               "panel", "group")
"""`s` chỉ đổi cỡ được ở các kind này. `banner`/`ribbon`/`chip` tự đo theo chữ và BỎ QUA
`s` (xem `_zu_extent`) ⇒ phóng `s` cho chúng là đổi chữ ký mà hình y nguyên."""


def _zu_rows(v):
    """Gom nodes thành các HÀNG NGANG theo `at[1]`.

    Gom theo `at[1]` chứ không theo pixel: cùng hàng thì tác giả đặt cùng `at[1]`, và
    `zu_row` cũng ghi cùng một giá trị — gom theo pixel thì hai hàng sát nhau bị dính
    thành một qua hiệu ứng chuỗi."""
    ns = sorted(v["nodes"], key=lambda n: n["at"][1])
    rows, cur = [], [ns[0]]
    for n in ns[1:]:
        if n["at"][1] - cur[-1]["at"][1] <= ZU_ROWTOL:
            cur.append(n)
        else:
            rows.append(cur)
            cur = [n]
    rows.append(cur)
    return rows


def _zu_rowh(row):
    """(cao LÊN, cao XUỐNG) của một hàng tính từ tâm hàng — lấy max vì cùng hàng cùng `cy`."""
    return (max(_zu_box(n)[1] for n in row), max(_zu_box(n)[2] for n in row))


def _zu_kw(row, mingap=104):
    """Trần phóng to theo BỀ NGANG: hàng phóng xong vẫn phải lọt vùng an toàn + đủ khe mũi tên."""
    avail = (ZU_CAST_R - 20) - (ZU_CAST_L + 12)
    w = sum(_zu_box(n)[0] * 2 for n in row)
    if w <= 0:
        return ZU_KMAX
    return max(min((avail - mingap * (len(row) - 1)) / w, ZU_KMAX), 1.0)


def _zu_respread(row, lo, hi, wide, mingap=104):
    """Chia lại `at[0]` của một hàng sau khi phóng to.

    🔴 BẮT BUỘC ĐI KÈM bước phóng: `zu_row` đã chia `at[0]` theo bề rộng ở cỡ CŨ, nên phóng
    `s` mà không chia lại thì các node ăn vào nhau — đúng cái lỗi `zu_row` sinh ra để chặn.
    Giữ TÂM hàng, chỉ nới bề ngang khi cần, và kẹp trong vùng an toàn."""
    if len(row) < 2:
        return
    bx0, bx1 = ((CARD_X0 + 40, CARD_X1 - 40) if wide else (ZU_CAST_L + 12, ZU_CAST_R - 20))
    row = sorted(row, key=lambda n: n["at"][0])
    ws = [_zu_box(n)[0] * 2 for n in row]
    w = min(max(hi - lo, sum(ws) + mingap * (len(row) - 1)), bx1 - bx0)
    c = min(max((lo + hi) / 2, bx0 + w / 2), bx1 - w / 2)
    L = c - w / 2
    gap = (w - sum(ws)) / (len(row) - 1)
    base0, base1 = ((CARD_X0 + 40, CARD_X1 - 40) if wide else (ZU_X0, ZU_X1))
    x = L
    for n, wn in zip(row, ws):
        n["at"] = [(x + wn / 2 - base0) / (base1 - base0), n["at"][1]]
        x += wn + gap


def _zu_widen(v, free, rows):
    """KÉO NGANG: dàn nội dung cho phủ hết khung ngang, không dồn về một nửa.

    🔴 VÌ SAO CÓ (user 2026-08-17, dán 4 thẻ liền: *"còn rất nhiều ảnh lỗi"*): `zu_fit` cân
    được chiều DỌC nhưng chiều NGANG thì vẫn là `at[0]` tác giả gõ tay. Và `_zu_respread` chỉ
    chạy cho hàng có **≥2 node** — nên sơ đồ 2 CỘT viết thành 4 hàng MỘT-NODE (trái: hai vật
    xếp dọc · phải: kết quả) **không có tầng nào chạm tới**: nội dung dồn 60% bên trái, nửa
    phải trống trơn, và hộp kết quả bé tí. Đây là lớp lỗi đông nhất trong bộ 80 thẻ.

    Cách làm giống hệt phép cân dọc, chỉ đổi trục: tìm mép trái/phải THẬT của cả khối rồi ánh
    xạ affine tâm các node sao cho mép trái chạm `bx0`, mép phải chạm `bx1`. Không đụng:
      · node `fix` (khuôn helper đã tự xếp — kéo là phá đối xứng vừa dựng)
      · `banner`/`ribbon` (vốn full-width, không phải nội dung định vị)
    Chỉ kéo RA (k ≥ 1,05), không bao giờ nén vào — nén là việc của bước lùi cỡ."""
    ns = [n for i in free for n in rows[i]
          if not n.get("fix") and n.get("kind", "circle") not in ("banner", "ribbon")]
    if len(ns) < 2:
        return
    pos = _zu_place(v)
    box = {n["id"]: _zu_box(n)[0] for n in ns}
    lo_n = min(ns, key=lambda n: pos[n["id"]][0] - box[n["id"]])
    hi_n = max(ns, key=lambda n: pos[n["id"]][0] + box[n["id"]])
    cxl, cxr = pos[lo_n["id"]][0], pos[hi_n["id"]][0]
    if cxr - cxl < 40:
        return
    bx0, bx1 = ZU_CAST_L + 12, ZU_CAST_R - 20
    k = ((bx1 - box[hi_n["id"]]) - (bx0 + box[lo_n["id"]])) / (cxr - cxl)
    if k < 1.05:
        return
    c = bx0 + box[lo_n["id"]] - k * cxl
    for n in ns:
        cx = k * pos[n["id"]][0] + c
        n["at"] = [round((cx - ZU_X0) / (ZU_X1 - ZU_X0), 4), n["at"][1]]


def zu_fit(v):
    """PHÓNG TO + CHIA ĐỀU theo chiều DỌC. Chạy MỘT LẦN, trước cả `_zu_place`.

    🔴 VÌ SAO CÓ (user bắt được 2026-08-17, thẻ 05: *"khoảng trống trên đầu thì nhiều mà lại
    cho text xuống dưới thế"*): tool có đủ cơ chế chống **TRÀN** (`_zu_place` kẹp · `zu_check`
    báo chồng) mà **không có một cơ chế nào chống LỌT**. Thẻ 3 icon + 1 dải đáy dùng hết
    **47%** chiều cao band, toàn bộ phần trống dồn lên đầu bảng, và icon vẫn ở cỡ mặc định
    dù còn thừa chỗ ngang. Gate hình học báo 0 lỗi — vì lọt không phải lỗi hình học.

    Hai việc phải làm CÙNG LÚC, làm lẻ là vô ích:
      ① **PHÓNG TO** (`s`) tới khi lấp ~`ZU_FILL` band — trần lấy theo bề ngang THẬT của hàng
      ② **CHIA ĐỀU** khe dọc, hàng đầu bắt đầu ngay dưới tiêu đề
    Làm ① mà không ③ `_zu_respread` thì node chồng ngang; làm ② mà không ① thì khoảng trống
    chỉ **dời chỗ** từ trên xuống giữa, nhìn không khá hơn.

    Hàng GHIM giữ nguyên chỗ: `at[1] ≥ 0.86` = dải đáy · `≤ 0.12` = cờ/bong bóng trên đầu.
    Chỉ các hàng ở GIỮA bị chia lại — nếu không thì dải đáy bị kéo lên lơ lửng."""
    if v.get("_fit") or not v.get("nodes"):
        return v
    v["_fit"] = True
    Y0 = CARD_Y0 + 74 + 62 + 34 if v.get("title") else CARD_Y0 + 40
    # 🔴 HAI HẰNG SỐ KHÁC NHAU, ĐỪNG GỘP (mất một vòng vì gộp):
    #  · `span` = thang mà `_zu_place` dùng để đổi `at[1]` ↔ pixel ⇒ **phải TRÙNG** `by1` của
    #    hàm đó (`CARD_Y1 - 34`). Gộp làm một với lề đáy thì `at[1]` tính ra bị co dãn 14px,
    #    và triệu chứng y hệt lỗi cần chữa nên rất dễ tưởng là "vá chưa ăn".
    #  · `bot` = LỀ ĐÁY khi xếp hàng, siết hơn (48px). `_zu_place` chỉ kẹp cho KHỎI TRÀN (12px),
    #    nên hàng cuối rơi xuống 34px là "nhãn ngồi trên mép card" — nhìn như bị cắt dù không
    #    cắt. Bắt được ở thẻ 18 (nhãn 報酬比例 9万円) sau khi bật cân dọc.
    span, pos, rows = (CARD_Y1 - 34) - Y0, _zu_place(v), _zu_rows(v)
    top, bot, free, spans = Y0, CARD_Y1 - 48, [], {}
    for i, r in enumerate(rows):
        a = sum(n["at"][1] for n in r) / len(r)
        up, dn = _zu_rowh(r)
        cy = sum(pos[n["id"]][1] for n in r) / len(r)
        # 🔴 CỜ `fix` CỦA BUILDER PHẢI ĐƯỢC TÔN TRỌNG. Builder đặt `fix` cho đúng những sơ đồ
        # mà khoảng dọc CHÍNH LÀ nội dung (toả 2 lối · lưới 2×2 nối bằng elbow · hội tụ chéo).
        # Bản đầu của `zu_fit` bỏ qua cờ này ⇒ xếp lại 4 hàng của thẻ hội tụ thành 4 tầng đều
        # nhau và khe chéo w→t teo còn 38px. Cờ đã có sẵn, chỉ là tao không đọc.
        if any(n.get("fix") for n in r):
            (top, bot) = ((max(top, cy + dn + 34), bot) if a <= 0.12 else
                          ((top, min(bot, cy - up - 34)) if a >= 0.86 else (top, bot)))
        elif a >= 0.86:                     # ghim ĐÁY (dải kết) — không kéo lên lơ lửng
            bot = min(bot, cy - up - 34)
        elif a <= 0.12:                     # ghim ĐỈNH (cờ/bong bóng)
            top = max(top, cy + dn + 34)
        else:
            free.append(i)
            spans[i] = (min(pos[n["id"]][0] - _zu_box(n)[0] for n in r),
                        max(pos[n["id"]][0] + _zu_box(n)[0] for n in r))
    if not free or bot - top <= 40:
        return v
    # 🔴 HÀNG SONG SONG PHẢI DÙNG CHUNG MỘT KHUNG NGANG (2026-08-17, user: *"nhìn cho nó đều"*).
    # `_zu_respread` bản đầu lấy span RIÊNG của từng hàng (mép ngoài trước khi phóng), nên hai
    # hàng cùng cấu trúc mà tác giả gõ `at[0]` lệch nhau một chút là ra hai khung rộng khác nhau
    # ⇒ **mũi tên hàng trên dài 600px, hàng dưới 185px** (đo ở thẻ 30). Mắt đọc ngay ra "không
    # đều". Gộp span theo SỐ NODE của hàng: cùng số ô = cùng vai = cùng khung.
    byn = {}
    for i in free:
        byn.setdefault(len(rows[i]), []).append(i)
    for grp in byn.values():
        if len(grp) > 1:
            lo, hi = (min(spans[i][0] for i in grp), max(spans[i][1] for i in grp))
            for i in grp:
                spans[i] = (lo, hi)
    avail = bot - top
    H0 = sum(sum(_zu_rowh(rows[i])) for i in free)
    # 🔴 HAI CHIỀU, KHÔNG CHỈ PHÓNG TO. Bản đầu chỉ biết phóng (`max(..., 1.0)`), nên thẻ nào
    # nội dung CAO HƠN band thì `zu_fit` bó tay: giữ `at[1]` tác giả, hàng cuối đè lên dải kết.
    # Dính thật ở thẻ 30 (hai hàng vòng-tròn-có-nhãn = 496px trong band 490px ⇒ chồng 4px).
    # Thu nhỏ chỉ nhắm 0,90 band (vừa đủ lọt), không nhắm 0,86 như khi phóng — thu quá tay là
    # tự bỏ mất cỡ chữ, mà đây là tệp 45+. Sàn 0,70 để không bao giờ ra chữ nhỏ hơn sàn font.
    tgt = avail * (ZU_FILL if H0 <= avail else 0.90) / max(H0, 1)
    k0 = (min([tgt] + [_zu_kw(rows[i]) for i in free]) if tgt >= 1.0
          else max(tgt, 0.70))

    def build(k, spread):
        """Thử một cỡ trên BẢN SAO → (spec thử, list lỗi hình học). Không đụng `v`."""
        p = copy.deepcopy(v)
        prow = _zu_rows(p)
        if abs(k - 1.0) > 0.02:
            for i in free:
                for n in prow[i]:
                    if n.get("kind", "circle") in ZU_SCALABLE:
                        n["s"] = round(n.get("s", 1.0) * k, 3)
        hs = [_zu_rowh(prow[i]) for i in free]
        if spread:
            gap = (avail - sum(u + d for u, d in hs)) / (len(free) + 1)
            # sàn 8px (không phải 30): khi nội dung lấp gần hết band thì khe nhỏ là ĐÚNG.
            # Sàn 30 làm nhánh THU NHỎ vô hiệu — thu xong khe còn 20px nên bước xếp bị bỏ,
            # `at[1]` tác giả giữ nguyên, và thẻ vẫn chồng y như chưa thu.
            if gap >= 8:
                y = top
                for i, (u, d) in zip(free, hs):
                    y += gap
                    for n in prow[i]:
                        n["at"] = [n["at"][0], round((y + u - Y0) / span, 4)]
                    y += u + d
        for i, (u, d) in zip(free, hs):
            cy = Y0 + span * prow[i][0]["at"][1]
            _zu_respread(prow[i], *spans[i], cy + d < CH_TOP)
        _zu_widen(p, free, prow)
        return p, _zu_geom(p)

    # 🔴 TỰ LÙI CỠ: thử từ to xuống, LẤY BẢN TO NHẤT MÀ HÌNH HỌC SẠCH. Cách này thay cho việc
    # đoán trần bằng công thức — trần thật phụ thuộc cả edge CHÉO giữa hai hàng khác nhau, thứ
    # mà `_zu_kw` (chỉ đo bề ngang trong CÙNG hàng) không thấy được.
    # Nến chót là (k=1, không xếp lại) = **đúng bản tác giả** ⇒ `zu_fit` không bao giờ làm xấu đi.
    lo_k = 1.0 if k0 > 1.0 else 0.70
    ks = [round(k0 - i * 0.07, 3) for i in range(max(int((k0 - lo_k) / 0.07), 0) + 1)] + [1.0]
    for k in ks:
        got, bad = build(k, True)
        if not bad:
            break
    else:
        got, bad = build(1.0, False)
        if bad:
            return v
    fitted = {n["id"]: n for n in got["nodes"]}
    for n in v["nodes"]:
        n["at"] = fitted[n["id"]]["at"]
        if "s" in fitted[n["id"]]:
            n["s"] = fitted[n["id"]]["s"]
    if k > 1.02:
        H = sum(sum(_zu_rowh(_zu_rows(v)[i])) for i in free)
        print(f"  [zu_fit] phong x{k:.2f} -> lap {H / avail * 100:.0f}% band")
    return v


def _zu_trim(a, b, na, nb, extra):
    """Cắt đoạn a→b khỏi hộp bao của hai node (+ `extra` px chừa thoáng)."""
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L

    def reach(n):
        hw, hh = _zu_extent(n)
        cand = []
        if abs(ux) > 1e-6:
            cand.append(hw / abs(ux))
        if abs(uy) > 1e-6:
            cand.append(hh / abs(uy))
        return min(cand) if cand else hw
    da, db = reach(na) + extra, reach(nb) + extra
    if da + db > L - 24:                     # hai node quá sát → chia đôi khe còn lại
        k = max(L - 24, 0) / max(da + db, 1)
        da, db = da * k, db * k
    return (a[0] + ux * da, a[1] + uy * da), (b[0] - ux * db, b[1] - uy * db), ux, uy


def _dash_rect(d, box, col, w=6, on=22, off=16):
    """Khung chữ nhật NÉT ĐỨT — ô "còn trống" của một lưới, cùng bề ngang với ô đã điền.

    🔴 Vì sao cần: ô trống trước đây vẽ bằng `circle` nét đứt (rộng 147px) cạnh ô đã điền là
    `label` (rộng 300px) ⇒ khe còn lại khác nhau ⇒ mũi tên hai hàng dài 188 vs 311px (lệch 40%).
    Cùng một lưới thì mọi ô phải cùng khuôn, chỉ khác TRẠNG THÁI (đã điền / còn trống)."""
    x0, y0, x1, y1 = box
    for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        _dash_line(d, a[0], a[1], b[0], b[1], col, w, on=on, off=off)


def _zu_label(d, cx, cy, half, lab, fl, color):
    """Nhãn của node, đặt DƯỚI vật — nhưng TỰ LẬT LÊN TRÊN nếu tràn đáy card.

    🔴 Bắt được ở mẫu t2 (badge ở `at:[0.95,0.92]`): nhãn 「遺族年金」 rơi ra ngoài card,
    bị cắt mất nửa dưới. Kiểu lỗi này chỉ lộ khi node nằm sát đáy ⇒ tự lật là cách duy
    nhất không phải nhớ luật lúc viết SLIDES."""
    nl = len(lab.split(NL))
    hblk = fl.size * 1.34 * (nl - 1) + fl.size
    y = cy + half + 20 + hblk / 2
    if y + hblk / 2 > CARD_Y1 - 12:
        y = cy - half - 20 - hblk / 2
    tw_ml(d, (cx, y), lab, fl, color)
ZU_FAN = (247, 226, 178)      # dải toả — đo trên card kem, KHÔNG dùng (252,244,222) (vô hình)


def L_zu(im, v, t):
    """SƠ ĐỒ: nodes đặt tự do + edges nối + bong bóng/✗/tia. Xem khối chú thích ở trên."""
    if v.get("title"):
        title(im, v["title"], t)
    zu_fit(v)                          # ⬅ cân dọc TRƯỚC khi kẹp (idempotent)
    nodes = v["nodes"]
    pos = _zu_place(v)                 # ⬅ tự kẹp; xem chú thích của `_zu_place`
    t0s, nmap = {}, {}
    base = 0.62 if v.get("title") else 0.20
    bts = v.get("beats") or []
    for i, n in enumerate(nodes):
        # nhịp theo lời đọc (style りょう): beats[i] = GIÂY THẬT node thứ i hiện.
        # Thiếu/None → nhịp dồn cũ. Edge tự theo (max hai đầu + 0.22), không phải khai.
        if i < len(bts) and bts[i] is not None:
            t0s[n["id"]] = float(bts[i]) / PACE
        else:
            t0s[n["id"]] = base + i * 0.44
        nmap[n["id"]] = n

    # ── edges vẽ TRƯỚC node để mũi tên chui xuống dưới vật, không cắt qua mặt icon
    for e in v.get("edges", []):
        a, b = pos[e["from"]], pos[e["to"]]
        te = max(t0s[e["from"]], t0s[e["to"]]) + 0.22
        col = ZU_ETONE.get(e.get("tone", "amber"), AMBER)
        st = e.get("style", "arrow")
        p = prog(t, te, 0.40)
        if p <= 0.01:
            continue
        (x0, yy0), (x1, yy1), ux, uy = _zu_trim(a, b, nmap[e["from"]], nmap[e["to"]],
                                                e.get("gap", 18))
        if st == "arrow":
            blend(im, 1.0, 0, lambda d, p=p, x0=x0, yy0=yy0, x1=x1, yy1=yy1, col=col:
                  arrow(d, x0, yy0, x1, yy1, p, col, w=e.get("w", 15)))
        elif st == "line":
            blend(im, 1.0, 0, lambda d, p=p, x0=x0, yy0=yy0, x1=x1, yy1=yy1, col=col:
                  arrow(d, x0, yy0, x1, yy1, p, col, w=e.get("w", 11), outline=None))
        elif st == "dot":
            blend(im, 1.0, 0, lambda d, p=p, x0=x0, yy0=yy0, x1=x1, yy1=yy1, col=col: (
                _dash_line(d, x0, yy0, x1, yy1, col, e.get("w", 7), p=p)))
        elif st == "elbow":       # đi DỌC trước rồi NGANG — nhánh kiểu ảnh mẫu 「役所の窓口」
            # 🔴 TÍNH HÌNH HỌC RIÊNG, KHÔNG DÙNG (x0,yy0) CỦA `_zu_trim` (user bắt được
            # 2026-08-17: "mũi tên lỗi"). `_zu_trim` cắt theo hướng CHÉO a→b, nên với a ở
            # trên-phải và b ở dưới-trái thì điểm bắt đầu lệch khỏi tâm a cả hai chiều ⇒ đoạn
            # dọc không mọc ra từ GIỮA ĐÁY hộp mà từ một góc, nhìn như vẽ trượt.
            # Elbow đúng: **giữa đáy (hoặc giữa đỉnh) node a → cùng cao độ tâm b → mép hông b**.
            # 🔴 BA ĐOẠN: dọc → ngang → **mũi chỉ XUỐNG vào ĐỈNH b**. Bản 2 đoạn (kết bằng mũi
            # tên NGANG vào mép hông b) sai hai chuyện: ① đoạn ngang chạy đúng cao độ TÂM b nên
            # **trùng đường với mũi tên khác của cùng hàng** (dính ở thẻ 65: elbow s1→s2 chồng
            # lên mũi tên s2→s3) ② mẫu của kênh đối thủ luôn kết bằng mũi chỉ xuống — nhánh rẽ
            # đọc là "từ trên đi xuống", mũi ngang đọc là "đi qua".
            ax, ay = pos[e["from"]]
            bx2, by2 = pos[e["to"]]
            # 🔴 dùng `_zu_box` (CÓ nhãn) cho ĐÁY của a — `_zu_extent` chỉ đo hình, nên đoạn
            # ngang chạy ĐÈ QUA NHÃN dưới node (dính ở thẻ 14: cắt ngang chữ 「2回目」).
            # Còn ĐỈNH của b thì lấy `up` (nhãn của b nằm ở dưới b, không cản đường).
            _, _, a_dn = _zu_box(nmap[e["from"]])
            bhw, b_up, _ = _zu_box(nmap[e["to"]])
            g = e.get("gap", 18)
            ys = ay + a_dn + g                    # mọc từ giữa ĐÁY (đã tính nhãn) của a
            ye = by2 - b_up - g                   # dừng trên ĐỈNH của b
            # 🔴 CHIA 30/70, KHÔNG PHẢI 50/50 (vá 2026-08-17, soi 1:1 thẻ 08): chia đôi thì
            # đoạn xuống chỉ được nửa khe, và ở lưới 2×2 (khe ~60px) nửa đó còn 30px — ngắn hơn
            # đầu mũi (26px) ⇒ ra **mũi tên cụt quay ngang**, đọc thành "đi sang trái" chứ không
            # phải "đi xuống". Đoạn dọc đầu chỉ cần đủ thấy là gãy khúc; đoạn CUỐI mới chở nghĩa.
            ymid = ys + max(14, (ye - ys) * 0.30)
            ew = int(e.get("w") or max(10, min(abs(ye - ys) * 0.10, 20)))   # PIL width: int
            blend(im, 1.0, 0, lambda d, p=p, ax=ax, ys=ys, ymid=ymid, bx2=bx2, ye=ye,
                  col=col, ew=ew: (
                d.line([ax, ys, ax, ys + (ymid - ys) * min(p / .34, 1)], fill=col, width=ew),
                d.line([ax, ymid, ax + (bx2 - ax) * min(max(p - .34, 0) / .33, 1), ymid],
                       fill=col, width=ew) if p > .34 else None,
                arrow(d, bx2, ymid, bx2, ye, max(0.0, (p - .67) / .33), col, outline=None)
                if p > .67 else None))
        elif st == "arc":         # VÒNG XUỐNG DƯỚI rồi quay lên — "lối SAI" của ảnh mẫu 4.
            # Đi thẳng thì đường chồng lên chính hàng node, và dấu ✗ rơi đè lên một node.
            dp = e.get("drop", 150)
            ym = max(yy0, yy1) + dp
            blend(im, 1.0, 0, lambda d, p=p, x0=x0, yy0=yy0, x1=x1, yy1=yy1, ym=ym, col=col: (
                _dash_line(d, x0, yy0, x0, ym, col, e.get("w", 7), p=min(p / .25, 1)),
                _dash_line(d, x0, ym, x1, ym, col, e.get("w", 7),
                           p=max(0.0, min((p - .25) / .5, 1))),
                arrow(d, x1, ym, x1, yy1, max(0.0, (p - .75) / .25), col,
                      w=e.get("w", 7) + 4, outline=None) if p > .75 else None))
        elif st == "fan":         # dải nhạt toả ra — 「消えるのは自分の道」
            blend(im, 1.0, 0, lambda d, p=p, a=a, b=b: d.line(
                [a[0], a[1], a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p],
                fill=ZU_FAN, width=e.get("w", 34)))
        if e.get("x"):
            # ✗ ĐỎ vắt qua giữa đường — "lối này KHÔNG đi được" (ảnh mẫu 4: 本人 → 保険者).
            # Với `arc` thì ✗ phải nằm trên ĐOẠN NGANG DƯỚI, không phải giữa hai node.
            mx = (x0 + x1) / 2
            my = (max(yy0, yy1) + e.get("drop", 150)) if st == "arc" else (yy0 + yy1) / 2
            ax_, dy_ = app(t, te + 0.30)
            blend(im, ax_, dy_, lambda d, mx=mx, my=my: [
                d.line([mx - 44, my - 44, mx + 44, my + 44], fill=XRED, width=17,
                       joint="curve"),
                d.line([mx - 44, my + 44, mx + 44, my - 44], fill=XRED, width=17,
                       joint="curve")])
        if e.get("label"):
            # 🔴 Nhãn phải LỌT KHE GIỮA 2 NODE, và ngồi CAO hơn đường hẳn 70px.
            # Bản đầu cho nhãn 300px cố định + offset 40 ⇒ 「自分で見る」 bị băng navy của
            # `panel` đè lên một nửa (mẫu t3). Khe = đoạn đã trừ `shrink` hai đầu.
            gap = max(math.hypot(x1 - x0, yy1 - yy0) - 20, 110)
            f = fit(e["label"], "bold", min(gap, 320), 36, 22)
            # 🔴 Nhãn edge NGANG đặt TRÊN ĐỈNH của node CAO NHẤT trong hai đầu, không phải
            # "trên đường −58px". Bản trước dùng offset cố định ⇒ với node `panel` (cao 210px,
            # băng navy chiếm 62px trên) thì nhãn rơi ĐÚNG VÀO băng navy: dính 2 lần —
            # thẻ 「ねんきん定期便」 của mẫu t3 và thẻ 48 của video 13. Đo theo node thì hết.
            top = min(pos[e["from"]][1] - _zu_extent(nmap[e["from"]])[1],
                      pos[e["to"]][1] - _zu_extent(nmap[e["to"]])[1])
            ox, oy = ((0, max(top - 26, CARD_Y0 + 46) - (yy0 + yy1) / 2)
                      if abs(ux) >= abs(uy) else (f.getlength(e["label"]) / 2 + 26, 0))
            a2, dy = app(t, te + 0.20)
            blend(im, a2, dy, lambda d, f=f, x0=x0, yy0=yy0, x1=x1, yy1=yy1: tw(
                d, ((x0 + x1) / 2 + ox, (yy0 + yy1) / 2 + oy), e["label"], f, INK2,
                anchor="mm"))

    # ── nodes
    for n in nodes:
        cx, cy = pos[n["id"]]
        s = n.get("s", 1.0)
        k = n.get("kind", "circle")
        col = ZU_TONE.get(n.get("tone", "pale"), ZU_PALE)
        a, dy = app(t, t0s[n["id"]])
        lab = n.get("label", "")
        # cỡ chữ nhãn: đo TRƯỚC khi vào closure (LUẬT SỐ 1 — không đoán từ font.size)
        fl = fit_ml(lab, "bold", n.get("lw", 300) * s, int(38 * s), 26) if lab else None

        def draw(d, n=n, cx=cx, cy=cy, s=s, k=k, col=col, lab=lab, fl=fl):
            if k == "circle":
                r = 92 * s
                if n.get("dash"):
                    _dash_ellipse(d, [cx - r, cy - r, cx + r, cy + r], INK, 7)
                else:
                    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
                if n.get("icon"):
                    ss = 112 * s
                    icon(d, n["icon"], cx - ss / 2, cy - ss / 2, ss,
                         GREY if n.get("dim") else None)
                if lab:
                    _zu_label(d, cx, cy, r, lab, fl, mut(n) if n.get("dim") else INK)
            elif k == "mark":
                r = 78 * s
                if n.get("tone") == "grey":
                    _dash_ellipse(d, [cx - r, cy - r, cx + r, cy + r], ZU_DASH, 7)
                    mark_no(d, cx, cy, r * .62)
                else:
                    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=AMBER)
                    mark_ok(d, cx, cy, r * .62)
                if lab:
                    _zu_label(d, cx, cy, r, lab, fl, mut(n) if n.get("dim") else INK)
            elif k == "panel":        # hộp có băng navy trên đầu — 「役所の窓口」
                w_, h_ = 330 * s, 210 * s
                d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2],
                                    14, fill=(252, 253, 255), outline=LINE, width=3)
                d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy - h_ / 2 + 62 * s],
                                    14, fill=INK)
                if n.get("icon"):
                    ss = 104 * s
                    icon(d, n["icon"], cx - ss / 2, cy - h_ / 2 + 76 * s, ss)
                if lab:
                    tw(d, (cx, cy - h_ / 2 + 31 * s), lab,
                       fit(lab, "black", w_ - 36, int(38 * s), 26), (255, 255, 255),
                       anchor="mm")
            elif k == "label":        # hộp chữ bo góc, có thể gạch chân vàng
                # 🔴 LABEL 2 DÒNG (2026-08-19): bản cũ fit/tw 1 dòng ⇒ khung bao dòng 1,
                # dòng 2 lòi ra ngoài (user bắt ở clip_12 video 14, khuôn `line()`).
                # Đường 1 dòng giữ NGUYÊN TỪNG SỐ như cũ — thẻ cũ không đổi một pixel.
                ls_ = lab.split(NL)
                f = fit_ml(lab, "black", n.get("lw", 470) * s,
                           int((92 if n.get("hero") else 46) * s), 30)
                wmax = max(f.getbbox(x)[2] - f.getbbox(x)[0] for x in ls_)
                bw = n.get("bw", wmax + 56) * (s if n.get("bw") else 1)
                lead = f.size * 1.22
                bh = f.size + 40 + lead * (len(ls_) - 1)
                # `frame: False` = CHỮ TRẦN, không hộp — cho ký hiệu toán (＋ ＝ →) và chú thích.
                # Đóng khung một dấu ＋ thì nó đọc thành "một ô nội dung" ngang hàng với hai hộp
                # số, trong khi vai của nó là TOÁN TỬ giữa hai ô đó.
                if n.get("dash"):
                    _dash_rect(d, [cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], INK, 6)
                elif n.get("frame", True):
                    d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                                        14, fill=CARDC, outline=INK, width=5)
                if n.get("under"):
                    yb = (cy + f.size * 0.62) if len(ls_) == 1 else (cy + bh / 2 - 17)
                    d.line([cx - bw / 2 + 34, yb, cx + bw / 2 - 34, yb], fill=AMBER, width=11)
                col_ = mut(n) if n.get("dim") else INK
                if len(ls_) == 1:
                    tw(d, (cx, cy), lab, f, col_, anchor="mm")
                else:
                    tw_ml(d, (cx, cy), lab, f, col_, leading=1.22)
            elif k == "bubble":
                _bubble(d, cx, cy, lab, fit_ml(lab, "bold", n.get("lw", 340) * s,
                                               int(40 * s), 26), n.get("tail", "down"))
            elif k == "icon":         # vật trần, không khung
                ss = 190 * s
                icon(d, n["icon"], cx - ss / 2, cy - ss / 2, ss, GREY if n.get("dim") else None)
                if lab:
                    _zu_label(d, cx, cy, ss / 2 - 4, lab, fl,
                              mut(n) if n.get("dim") else INK)
            # ── kind thêm 2026-08-17 ──────────────────────────────────────────
            elif k == "group":
                _zu_group(d, n, cx, cy, s)
            elif k == "banner":
                _zu_banner(d, n, cx, cy)
            elif k == "ribbon":
                _zu_ribbon(d, n, cx, cy)
            elif k == "chip":
                _zu_chip(d, n, cx, cy)
            elif k == "oval":         # ellipse DỌC + icon + nhãn dưới (cột lựa chọn)
                rx, ry = 96 * s, 132 * s
                d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                          fill=col if n.get("tone") else CARDC, outline=INK, width=5)
                if n.get("icon"):
                    ss = 104 * s
                    icon(d, n["icon"], cx - ss / 2, cy - ss / 2 - 18 * s, ss)
                if lab:
                    tw_ml(d, (cx, cy + ry - 46 * s),
                          lab, fit_ml(lab, "bold", rx * 1.9, int(34 * s), 24), INK)
            elif k == "bigicon":      # vật TO (đồng hồ cát, ví + hoá đơn)
                ss = n.get("size", 250) * s
                icon(d, n["icon"], cx - ss / 2, cy - ss / 2, ss, GREY if n.get("dim") else None)
                if lab:
                    _zu_label(d, cx, cy, ss / 2 - 4, lab, fl,
                              mut(n) if n.get("dim") else INK)
            if n.get("num"):
                hw_, up_, _ = _zu_box(n)
                _zu_badge(d, cx, cy, hw_, up_, n["num"])
            if n.get("spark"):
                _spark(d, cx, cy - _zu_extent(n)[1] - 8, 46 * s)
            if n.get("cross"):
                _cross(d, cx, cy, 92 * s)
        blend(im, a, dy, draw)
    # end = node MUỘN NHẤT + 0.74 — trùng đúng công thức cũ khi không có beats
    # (base + (n-1)*0.44 + 0.74 = base + n*0.44 + 0.30), và ăn theo beats khi có.
    return (max(t0s.values()) if t0s else base) + 0.74


def zu_check(v):
    """→ list lỗi HÌNH HỌC của một thẻ `zu`, ĐO SAU KHI ĐÃ KẸP (`_zu_place`).

    🔴 VÌ SAO Ở ĐÂY, KHÔNG Ở BUILDER: công thức bề rộng/cao của từng `kind` nằm trong
    `_zu_extent` + `L_zu` của file này. Chép sang builder là hai bản số sẽ lệch nhau ngay
    lần sửa layout đầu tiên — đúng loại lỗi im lặng mà `_sig`/`_MISSING_ART` đã dính 3 lần.

    Vì đã có kẹp, gate chỉ còn báo hai thứ mà kẹp KHÔNG cứu được:
      ① node RỘNG/CAO HƠN cả vùng an toàn (phải giảm `s`/`lw`/số ký tự)
      ② hai node CHỒNG NHAU (phải giãn `at` ra — kẹp không biết dời cái nào)
    """
    out = []
    zu_fit(v)                 # 🔴 gate phải đo ĐÚNG cái sẽ được vẽ — `L_zu` cũng gọi hàm này
    pos = _zu_place(v)
    ids = [n["id"] for n in v["nodes"]]
    avail_w = (ZU_CAST_R - 20) - (ZU_CAST_L + 12)
    avail_h = (CARD_Y1 - 12) - (CARD_Y0 + 12)
    # ── ĐỒ TRANG TRÍ MỒ CÔI: icon KHÔNG nhãn + KHÔNG edge + ĐỨNG MỘT MÌNH trong hàng.
    # 🔴 user bắt được 2026-08-17 (thẻ 04): *"sao lại có cái ảnh riêng lẻ ở góc trái thế"*.
    # Nó vào bài vì tao lấy đồ trang trí để LẤP KHOẢNG TRỐNG — chữa triệu chứng của đúng
    # cái bệnh mà `zu_fit` mới chữa được tận gốc. Với tệp 45+, một vật không nhãn không nối
    # với gì thì chở 0 thông tin và hút mắt khỏi con số hero ⇒ phải bỏ, không phải thu nhỏ.
    # Cặp/hàng ≥2 vật (○ và × của thẻ đố) hoặc vật có nhãn thì KHÔNG tính — đó là nội dung.
    linked = {i for e in v.get("edges", []) for i in (e["from"], e["to"])}
    for r in _zu_rows(v):
        for n in r:
            if (len(r) == 1 and n["id"] not in linked and not n.get("label")
                    and n.get("kind", "circle") in ("circle", "icon", "bigicon", "mark")):
                out.append(f"node {n['id']!r} ({n.get('icon')}) là ĐỒ TRANG TRÍ MỒ CÔI "
                           f"(không nhãn, không edge, một mình một hàng) — bỏ đi, hoặc "
                           f"cho nhãn / nối edge để nó chở thông tin")
    for n in v["nodes"]:
        hw, up, down = _zu_box(n)
        if hw * 2 > avail_w:
            out.append(f"node {n['id']} RỘNG {hw*2:.0f}px > vùng an toàn {avail_w}px "
                       f"— giảm `lw`/`s` hoặc bớt ký tự")
        if up + down > avail_h:
            out.append(f"node {n['id']} CAO {up+down:.0f}px > vùng an toàn {avail_h}px")
    out += _zu_geom(v)
    return out


def _zu_geom(v):
    """Lỗi HÌNH HỌC của thẻ `zu`: node chồng nhau · khe mũi tên · nhãn edge. Đo SAU kẹp.

    🔴 TÁCH KHỎI `zu_check` để `zu_fit` dùng **đúng phép đo này** khi thử cỡ. Không tách thì
    bước phóng to tự sinh ra đúng những lỗi mà gate sắp báo — đo thật lần đầu: **21 lỗi mới**
    trên 80 thẻ (khe mũi tên teo còn 24–48px). Một phép đo, hai người dùng."""
    out = []
    pos = _zu_place(v)
    ids = [n["id"] for n in v["nodes"]]
    for i, a in enumerate(v["nodes"]):
        for b in v["nodes"][i + 1:]:
            ax, ay = pos[a["id"]]
            bx, byy = pos[b["id"]]
            ahw, aup, adn = _zu_box(a)
            bhw, bup, bdn = _zu_box(b)
            # giao nhau THẬT của 2 hình chữ nhật bất đối xứng
            ox = min(ax + ahw, bx + bhw) - max(ax - ahw, bx - bhw)
            oy = min(ay + adn, byy + bdn) - max(ay - aup, byy - bup)
            if ox > -6 and oy > -6:
                out.append(f"node {a['id']} và {b['id']} CHỒNG NHAU "
                           f"(giao {ox:.0f}×{oy:.0f}px) — giãn `at` ra")
    for e in v.get("edges", []):
        for s in ("from", "to"):
            if e[s] not in ids:
                out.append(f"edge {s}={e[s]!r} không có node")
    # nhãn edge: đo KHE THẬT (sau kẹp, sau khi trừ hộp 2 node) — nhãn bị bó vào sàn font 22px
    # thì đọc không nổi ở tệp 45+. Phải đo SAU kẹp: `at` thô nói khe 361px, thật chỉ còn 190px.
    nm = {n["id"]: n for n in v["nodes"]}
    for e in v.get("edges", []):
        if e["from"] not in ids or e["to"] not in ids:
            continue
        p0, p1, _, _ = _zu_trim(pos[e["from"]], pos[e["to"]], nm[e["from"]], nm[e["to"]],
                                e.get("gap", 18))
        khe = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        # ⚠️ mũi tên ngắn hơn 60px nhìn như một cái GẠCH, không ra mũi tên — `arrow()` cần
        # ~26px riêng cho đầu mũi. Ca thật: thẻ 46 video 13, khe 9px ⇒ ra một dấu chấm navy.
        # 🔴 SÀN TƯƠNG ĐỐI THEO CỠ NODE (2026-08-17, sau khi user nói *"nhìn cho nó đều"*).
        # Sàn tuyệt đối sai cả hai đầu: 60px thì mũi tên 68px giữa hai hộp số 450px đọc ra "hai
        # hộp dính nhau"; mà nâng phẳng lên 100px thì lại giết hàng 4 vòng tròn nhỏ (bắt được:
        # 9 thẻ rớt, trong đó chuỗi 4 node phải thu về s=0,72 ⇒ chữ 27px, dưới sàn tệp 45+).
        # Cái mắt đo là TỈ LỆ mũi-tên / cỡ hai vật hai đầu, nên gate phải đo đúng thứ đó.
        need_len = max(60, 0.28 * (_zu_extent(nm[e["from"]])[0] + _zu_extent(nm[e["to"]])[0]))
        if e.get("style", "arrow") in ("arrow", "line") and khe < need_len:
            out.append(f"edge {e['from']}→{e['to']}: khe thật {khe:.0f}px < {need_len:.0f}px "
                       f"(28% cỡ 2 node) ⇒ mũi tên lép so với hai hộp. Giãn `at` ra hoặc "
                       f"giảm `s`/`lw`/`w` của 2 node")
        if e.get("style") == "elbow":
            # elbow 3 đoạn cần khe DỌC ≥ đáy-có-nhãn của a + đỉnh của b + 3 lần gap; thiếu thì
            # đoạn ngang chạy ĐÈ QUA NHÃN của node trên (dính ở thẻ 8/14 khi 2 hàng cách 0,34).
            ay2 = pos[e["from"]][1]; by3 = pos[e["to"]][1]
            _, _, adn = _zu_box(nm[e["from"]])
            _, bup, _ = _zu_box(nm[e["to"]])
            free = (by3 - bup) - (ay2 + adn)
            if free < 54:
                out.append(f"edge {e['from']}→{e['to']} (elbow): khe DỌC còn {free:.0f}px "
                           f"< 54px ⇒ đoạn ngang đè lên nhãn. Giãn `at[1]` hai hàng ra")
        if e.get("label"):
            need = len(e["label"]) * 30 + 20      # 30px = cỡ chữ nhỏ nhất còn đọc được
            if khe < need:
                out.append(f"nhãn edge {e['label']!r}: khe thật {khe:.0f}px < {need}px "
                           f"⇒ chữ tụt về sàn 22px. Giãn 2 node ra hoặc bỏ nhãn")
    out += _zu_even(v, pos, nm)
    out += _zu_terminal(v, pos)
    out += _zu_align(v, pos)
    return out


def _zu_align(v, pos):
    """Ba lỗi VỊ TRÍ mà mọi gate trước đều cho qua (user 2026-08-17: *"vẫn lỗi vị trí mà"*).

    ⑪ **Mũi tên ĐƠN phải THẲNG.** Thẻ chỉ có một mũi tên thì hai đầu phải cùng hàng (|dy|≤70)
       hoặc cùng cột (|dx|≤70). Một mũi tên chạy CHÉO qua giữa bảng đọc ra "bay ngang qua chỗ
       trống", và nó tự sinh hai vùng rỗng ở hai góc còn lại (thẻ 18: dy=140 ⇒ mũi tên chéo
       630px qua đúng vùng trắng nhất của thẻ). Sơ đồ toả/hợp lưu (≥2 mũi tên) thì chéo là ĐÚNG,
       nên gate chỉ soi thẻ 1 mũi tên.
    ⑫ **Đuôi bong bóng phải CHẠM thứ nó chú thích** (≤140px theo hướng đuôi). Bong bóng treo ở
       góc với cái đuôi chỉ vào không khí là lỗi nặng nhất về mặt đọc: người xem không biết câu
       đó nói về cái gì. Miễn cho bong bóng đã được nối bằng edge (`dot` kiểu "lời từ điện thoại").
    ⑬ **Node LƠ LỬNG.** Thẻ có mạch mũi tên, mà một node nội dung **không nối gì và một mình một
       hàng** ⇒ nó không thuộc mạch nào. Khác gate ① (đồ trang trí không nhãn): cái này CÓ nhãn
       nên trước giờ lọt sạch — thẻ 44 để 「10年間」 nằm lẻ góc dưới-trái trong khi nó là **hệ số
       của phép nhân trên mũi tên** (đúng chỗ của nó là NHÃN EDGE)."""
    out = []
    nm = {n["id"]: n for n in v["nodes"]}
    # 🔴 TÍNH CẢ `dot` (vá 2026-08-18, thẻ 53): đường nét đứt cũng là MỘT liên kết đơn, chạy
    # chéo qua bảng thì cũng sinh hai góc rỗng y như mũi tên đặc — bản đầu chỉ đếm arrow/line
    # nên thẻ "điện thoại ⇢ bong bóng" lọt sạch. `elbow`/`arc` thì CỐ Ý gãy khúc, không tính.
    eg = [e for e in v.get("edges", []) if e.get("style", "arrow") in ("arrow", "line", "dot")]
    linked = {i for e in v.get("edges", []) for i in (e["from"], e["to"])}
    # ⑪
    if len(eg) == 1:
        e = eg[0]
        if e["from"] in pos and e["to"] in pos:
            dx = abs(pos[e["from"]][0] - pos[e["to"]][0])
            dy = abs(pos[e["from"]][1] - pos[e["to"]][1])
            if dy > 70 and dx > 70:
                out.append(f"mũi tên ĐƠN {e['from']}→{e['to']} chạy CHÉO (dx={dx:.0f} dy="
                           f"{dy:.0f}) ⇒ bay qua vùng trống, sinh 2 góc rỗng. Cho hai đầu CÙNG "
                           f"HÀNG (|dy|≤70) hoặc CÙNG CỘT (|dx|≤70)")
    # ⑫
    for n in v["nodes"]:
        if n.get("kind") != "bubble" or n["id"] in linked:
            continue
        t = n.get("tail", "down")
        bx, by = pos[n["id"]]
        bhw, bup, bdn = _zu_box(n)
        best = None
        for m in v["nodes"]:
            if m is n or m.get("kind") in ("banner", "ribbon"):
                continue
            mx, my = pos[m["id"]]
            mhw, mup, mdn = _zu_box(m)
            if t in ("down", "up"):
                if abs(mx - bx) > bhw + mhw:
                    continue
                d = (my - mup) - (by + bdn) if t == "down" else (by - bup) - (my + mdn)
            else:
                if abs(my - by) > bup + mup + 40:
                    continue
                d = (bx - bhw) - (mx + mhw) if t == "left" else (mx - mhw) - (bx + bhw)
            if d >= -20 and (best is None or d < best):
                best = d
        if best is None or best > 140:
            out.append(f"bong bóng {n['id']!r} có đuôi {t!r} nhưng "
                       + ("KHÔNG có node nào ở hướng đó" if best is None
                          else f"cách node gần nhất {best:.0f}px (> 140)")
                       + " ⇒ đuôi chỉ vào không khí, người xem không biết câu đó nói về cái gì")
    # ⑬
    if eg:
        rows = _zu_rows(v)
        for ri, r in enumerate(rows):
            for n in r:
                # ⚖️ MIỄN "đề bài": một dòng chữ đứng ở HÀNG TRÊN CÙNG, trên toàn bộ mạch
                # (`at[1] ≤ 0,30`) là khuôn hợp lệ — thẻ đố ○× nêu câu hỏi rồi mới tới hai đáp
                # án. Cái bị cấm là dòng chữ nằm GIỮA hoặc DƯỚI mạch mà không nối vào đâu.
                if ri == 0 and n["at"][1] <= 0.30:
                    continue
                if (len(r) == 1 and n["id"] not in linked and n.get("label")
                        and n.get("kind", "circle") not in ("banner", "ribbon", "chip",
                                                            "bubble")):
                    out.append(f"node {n['id']!r} ({n.get('label','')!r}) LƠ LỬNG — có nhãn "
                               f"nhưng không nối edge và một mình một hàng, trong khi thẻ có "
                               f"mạch mũi tên. Đưa nó vào mạch (nhãn edge / cùng hàng) hoặc bỏ")
    return out


def _zu_terminal(v, pos):
    """Node CUỐI của sơ đồ (mọi mũi tên chỉ VÀO, không đi ra) phải là thứ TO NHẤT trên thẻ.

    🔴 user bắt được 2026-08-17 ở thẻ 18: `4分の3` là ĐÁP ÁN của thẻ mà nó là hộp chữ **nhỏ
    nhất**, trong khi hai nguồn là vòng tròn icon 190px. Mắt đọc theo cỡ: cái to nhất là cái
    quan trọng nhất. Sơ đồ mà đích nhỏ hơn nguồn thì nó **kể ngược** — người xem nhìn vào hai
    thứ bị bỏ đi thay vì nhìn vào kết luận.
    ⇒ Chữa bằng `hero: true` (label) hoặc tăng `s`/`w`, KHÔNG bằng cách thu nhỏ nguồn."""
    out = []
    # 🔴 TÍNH CẢ `fan`/`dot`/`arc` khi xét "có đi ra hay không" — nếu chỉ tính arrow/line/elbow
    # thì node toả ra bằng `fan` (thẻ 06: src→hub→l/r) bị coi là ĐÍCH cuối, báo lỗi giả.
    eg = [e for e in v.get("edges", [])
          if e.get("style", "arrow") in ("arrow", "line", "elbow", "fan", "dot", "arc")]
    if not eg:
        return out
    src = {e["from"] for e in eg}
    dst = {e["to"] for e in eg}
    nm = {n["id"]: n for n in v["nodes"]}
    # `mark` (○/×) có cỡ CỐ ĐỊNH theo thiết kế và thường đi thành CẶP hai kết cục — không
    # phải "đích kết luận" nên miễn. Ngưỡng 0,70 (không phải 0,90): 82–88% mắt không thấy lệch.
    body = [n for n in v["nodes"]
            if n.get("kind", "circle") not in ("banner", "ribbon", "chip", "bubble")]
    if not body:
        return out
    area = {n["id"]: (lambda b: b[0] * 2 * (b[1] + b[2]))(_zu_box(n)) for n in body}
    big = max(area.values())
    for i in dst - src:
        if (i in area and area[i] < big * 0.70
                and nm[i].get("kind", "circle") != "mark"):
            out.append(f"node {i!r} là ĐÍCH cuối của sơ đồ mà chỉ {area[i] / big * 100:.0f}% "
                       f"diện tích của node to nhất ⇒ thẻ kể ngược, mắt đọc vào nguồn thay vì "
                       f"vào kết luận. Cho `hero: true` (label) hoặc tăng `s`/`w`")
    return out


ZU_EVEN = 0.15
"""Trần lệch độ dài giữa hai mũi tên CÙNG VAI. 15% chốt 2026-08-17 (user: *"2 cái mũi tên dài
bằng nhau đi… nhìn cho nó đều"*) — dưới mức này mắt không phân biệt được, trên thì đọc ra
"cái này quan trọng hơn cái kia" trong khi hai nhánh vốn ngang vai."""


def _zu_even(v, pos, nm):
    """Mũi tên CÙNG VAI phải DÀI GẦN BẰNG NHAU. Hai loại "cùng vai", đo được:

      ① **CHUNG MỘT ĐẦU** — toả ra (1→N) hoặc hợp lưu (N→1). Hai nhánh của cùng một ý.
      ② **CÙNG HƯỚNG** (cos ≥ 0,985 ≈ lệch <10°) — hai hàng song song của một lưới/bảng.

    🔴 Vì sao phải là GATE MÁY: lệch độ dài là thứ **mắt bắt ngay mà gate hình học không thấy** —
    cả 80 thẻ đều "không chồng, không tràn, mũi tên không teo" mà vẫn có thẻ một nhánh 600px một
    nhánh 185px. Ba nguyên nhân đã đo được, đều KHÔNG phải lỗi thi hành:
      · đích không nằm ở trung điểm dọc của hai nguồn (thẻ 02)
      · hộp chữ tự co theo số ký tự ⇒ ô cùng vai khác bề ngang (thẻ 65 — dùng `bw` để khoá)
      · hai hàng nằm hai bên mốc `CH_TOP` ⇒ dùng hai khung ngang khác nhau (thẻ 65)
    """
    out = []
    segs = []
    for e in v.get("edges", []):
        if e.get("style", "arrow") not in ("arrow", "line"):
            continue
        if e["from"] not in nm or e["to"] not in nm:
            continue
        p0, p1, ux, uy = _zu_trim(pos[e["from"]], pos[e["to"]], nm[e["from"]], nm[e["to"]],
                                  e.get("gap", 18))
        segs.append((e, math.hypot(p1[0] - p0[0], p1[1] - p0[1]), ux, uy))
    for i, (ea, la, uxa, uya) in enumerate(segs):
        for eb, lb, uxb, uyb in segs[i + 1:]:
            share = len({ea["from"], ea["to"]} & {eb["from"], eb["to"]}) > 0
            same_dir = (uxa * uxb + uya * uyb) >= 0.985
            if not (share or same_dir):
                continue
            hi, lo = max(la, lb), min(la, lb)
            if hi > 0 and (hi - lo) / hi > ZU_EVEN:
                out.append(
                    f"mũi tên {ea['from']}→{ea['to']} ({la:.0f}px) và {eb['from']}→"
                    f"{eb['to']} ({lb:.0f}px) CÙNG VAI mà lệch {(hi - lo) / hi * 100:.0f}% "
                    f"(> {ZU_EVEN * 100:.0f}%) ⇒ nhìn không đều. Cách chữa: đích ở TRUNG ĐIỂM "
                    f"dọc của 2 nguồn · các ô cùng vai khoá `bw` bằng nhau · 2 hàng cùng phía "
                    f"mốc CH_TOP={CH_TOP}")
    return out


LAYOUTS = {"check": L_check, "flow": L_flow, "compare": L_compare,
           "timeline": L_timeline, "source": L_source,
           "big": L_big, "bars": L_bars, "art": L_art, "photo": L_art,
           "steps": L_steps, "tree": L_tree, "zu": L_zu, "pict": L_pict}


# ══════════════════════════════════════════════════════ frame & clip
GREY_ON_BG = (92, 100, 114)
"""Màu chữ MỜ khi thẻ có `bgimg`. GREY (168,174,184) là màu de-emphasis cho nền kem trơn;
đặt lên ảnh trung tính thì chữ TRÙNG MÀU NỀN và mất hẳn (user bắt được ở clip_53 「待たずに、聞く」
— dòng ✗ xám nằm trên cái điện thoại xám). Vẫn mờ hơn INK rõ rệt nên giữ đúng ý de-emphasis."""


def mut(v):
    """Màu cho chữ/icon 'mờ' — tự đậm lên khi thẻ có ảnh nền."""
    return GREY_ON_BG if v.get("bgimg") else GREY


def card_bg(im, v):
    """ẢNH LÀM NỀN TẤM BẢNG — khoá `"bgimg": "<file>"`, dùng được ở MỌI layout.

    🔴 user chốt 2026-08-10: *"tao muốn cái ảnh túi tiền làm background luôn cho text"*.
    Khác `fill` (ảnh NHỎ ở góc dưới-phải): `bgimg` phủ TRỌN thân bảng, chữ đè lên trên.
    Có màn che màu card (`bg_veil`, mặc định 0.78) để chữ navy vẫn đọc được — không có nó
    thì chữ chìm vào hình, và tệp 60+ là tệp mất chữ trước tiên.

    ⚠️ KHÔNG build-on: nền phải có mặt từ frame 0 như một phần sân khấu, nếu fade vào thì
    khung nhảy màu giữa clip. ⛔ `bgimg` phải nằm trong `_sig` VÀ trong sổ `_MISSING_ART`
    (bài học 3 lần ngày 2026-08-10 — khoá asset mới không tự vào gate).
    """
    name = v.get("bgimg")
    if not name:
        return
    cw, ch = CARD_X1 - CARD_X0, CARD_Y1 - CARD_Y0
    p = _art_path(name)
    if p is None:
        return
    key = (str(p), cw, ch, p.stat().st_mtime, "bg")
    if key not in _ART_CACHE:
        art = Image.open(p).convert("RGB")
        sc = max(cw / art.width, ch / art.height)
        art = art.resize((max(1, int(art.width * sc)), max(1, int(art.height * sc))),
                         Image.LANCZOS)
        art = art.crop(((art.width - cw) // 2, (art.height - ch) // 2,
                        (art.width - cw) // 2 + cw, (art.height - ch) // 2 + ch))
        _ART_CACHE[key] = art
    art = _ART_CACHE[key]
    veil = float(v.get("bg_veil", 0.78))
    lay = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    lay.paste(art, (0, 0))
    lay.alpha_composite(Image.new("RGBA", (cw, ch), CARDC + (int(255 * veil),)))
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], 28, fill=255)
    im.paste(lay.convert("RGB"), (CARD_X0, CARD_Y0), mask)


PROP_ZONES = ("GIUA card (x 520-1400) o moi do cao, hoac hai dai ben NHUNG chi TREN dinh nhan vat (y < CH_TOP = 368). Dai ben duoi 368 la cho 2 cast dung - dat o do se bi tay/vai de len; draw_props TU DAY LEN nhung nen khai dung tu dau.")


def draw_props(im, v, t, stack=None):
    """ĐỒ RỜI rải quanh thẻ — `"props": [{"icon","at","s","rot","t0"}...]`.

    Đúc 2026-08-24 từ frame user chỉ ra ở video đối thủ (シニアのお金相談所): MỘT frame của
    họ chở **~14 vật rời** (通知書 · bong bóng 絶対 · chip tháng · máy tính + tiền + xu ·
    2 quyển 年金手帳 nghiêng · 2 nhân vật · túi tiền ¥ · mũi tên đỏ · 2 tia · tờ tiền có
    cánh · nét vẽ tay). nenkin đo được **35/58 thẻ (60%) KHÔNG có một hình nào** ⇒ user:
    *"có text thuần nhìn frame hơi nhạt"*.

    ⚠️ Đây KHÁC `bgimg` (ảnh nền mờ nằm DƯỚI màn che) và khác `fill` (một ảnh trong hộp
    góc dưới-phải, đã đo là **cắt mất `cap` của layout `big`**). Props là NHIỀU vật nét
    đậm, nền trong suốt, đặt tự do — dùng lại bộ 38 icon PNG dùng chung, KHÔNG cần gen ảnh.

    Vẽ NGAY SAU card và TRƯỚC nội dung ⇒ chữ luôn nằm trên, prop không bao giờ che chữ.
    `at` là toạ độ tương đối trong CARD (0..1). Vùng nên dùng: {zones}.
    """
    # 🔴 TRÁNH VÙNG NHÂN VẬT (user chốt 2026-08-24: "sửa lỗi tay đè lên ảnh").
    # Hai dải bên trong card (x < CONTENT_X0 hoặc x > CONTENT_X1) là chỗ 2 nhân vật ĐỨNG,
    # từ y = CH_TOP (368) xuống đáy. Sticker đặt ở đó bị tay/vai cast đè lên — đã dính thật
    # ở thẻ 前回の約束 (calendar y=581 · passbook y=792 · clock y=614, cả 3 trong vùng cast).
    # ⚠️ Chú thích PROP_ZONES bản đầu ghi SAI đúng chỗ này ("dải bên + dải đáy") — đã sửa.
    # Ở đây TỰ ĐẨY LÊN trên đỉnh cast, xếp chồng lần lượt để không trùng nhau. Không đổi
    # prop nằm giữa card (x trong CONTENT) — chỗ đó cast không với tới.
    # 🔴 SỔ CHỖ DÙNG CHUNG cho CẢ HAI lớp (`props` dưới + `props_top` trên). Hai lớp đếm
    # chỗ riêng thì vật của lớp này bị đẩy lên trúng vật của lớp kia — đã dính: clock (lớp
    # dưới) leo lên chồng đúng chart_up (lớp trên) ở thẻ 前回の約束.
    # 🔴 Sổ chỗ phải ghi MỌI vật ở dải bên, không chỉ vật bị đẩy. Bản đầu chỉ ghi vật bị
    # đẩy ⇒ vật KHÔNG đè cast (chart_up y=293) vẫn giữ chỗ cũ và bị vật vừa leo lên (clock)
    # trùng vào. Nay mỗi vật dải bên đều đăng ký khoảng [top,bottom]; ai chồng thì lùi lên.
    if stack is None:
        stack = {"L": [], "R": []}
    fixed = []
    for p in (v.get("props") or []):
        s_ = float(p.get("s", 150))
        ax, ay = p.get("at", [0.5, 0.75])
        cx = CARD_X0 + ax * (CARD_X1 - CARD_X0)
        cy = CARD_Y0 + ay * (CARD_Y1 - CARD_Y0)
        side = "L" if cx < CONTENT_X0 else ("R" if cx > CONTENT_X1 else None)
        if side:
            h = s_ / 2
            if cy + h > CH_TOP:                      # đè vùng nhân vật → lên trên đỉnh cast
                cy = CH_TOP - 10 - h
            for _ in range(12):                      # lùi lên tới khi không chồng vật nào
                hit = next(((t0, b0) for t0, b0 in stack[side]
                            if cy - h < b0 + 14 and cy + h > t0 - 14), None)
                if not hit:
                    break
                cy = hit[0] - 14 - h
            cy = max(cy, CARD_Y0 + h + 6)            # không trồi khỏi mép trên card
            stack[side].append((cy - h, cy + h))
        fixed.append((p, cx, cy))

    for k, (p, cx, cy) in enumerate(fixed):
        nm = p.get("icon")
        if not nm:
            continue
        s = float(p.get("s", 150))
        t0 = float(p.get("t0", 0.30 + 0.14 * k))
        a, dx, dy = app_fly(t, t0, p.get("fly", "up"), 44, 0.50)
        if a <= 0.004:
            continue
        pth = icon_path(nm)
        if pth is None:
            continue
        key = ("prop", str(pth), int(s), int(p.get("rot", 0)))
        if key not in _ICON_CACHE:
            g = Image.open(pth).convert("RGBA")
            g.thumbnail((int(s), int(s)), Image.LANCZOS)
            if p.get("rot"):
                g = g.rotate(float(p["rot"]), expand=True, resample=Image.BICUBIC)
            _ICON_CACHE[key] = g
        g = _ICON_CACHE[key]
        if a < 0.999:
            g = g.copy()
            g.putalpha(g.getchannel("A").point(lambda q: int(q * a)))
        im.alpha_composite(g, dest=(int(cx - g.width / 2 + dx),
                                    int(cy - g.height / 2 + dy)))


draw_props.__doc__ = draw_props.__doc__.replace("{zones}", PROP_ZONES)


def frame(spec, t):
    im = stage_base()
    card_bg(im, spec)
    _pstack = {"L": [], "R": []}
    draw_props(im, spec, t, _pstack)
    end = LAYOUTS[spec.get("layout", "check")](im, spec, t)
    # LỚP STICKER TRÊN: `"props_top": [...]` vẽ SAU nội dung ⇒ sticker NỔI LÊN TRÊN ảnh
    # chính, chồng mép ảnh được — đúng cách video đối thủ xếp ~14 vật quanh một hình lớn.
    # `props` (vẽ trước) dùng cho thẻ CHỮ; `props_top` cho thẻ `art`/`pict` vốn đã có ảnh
    # giữa card, vì ở đó lớp dưới sẽ bị chính ảnh đó che mất.
    # ⚠️ props_top có thể che CHỮ — đặt ở góc/mép, đừng đưa vào dải title hay cap.
    if spec.get("props_top"):
        draw_props(im, {"props": spec["props_top"]}, t, _pstack)
    # ⭐ STICKER CHỮ/SỐ TRÊN CẢ THẺ (`pins_card`) — mở `pins` ra MỌI layout, không chỉ `art`.
    # `pins` gốc chỉ được L_art gọi, nên thẻ `pict`/`check`/`big`… không dùng được badge tròn
    # đặc, dấu đỏ nghiêng, số hero + 集中線 (user 2026-08-25: *"thêm sticker dạng remotion,
    # có thể cho text hoặc con số vào"*). `at` tính theo KHUNG CARD (0..1), `beat` = giây thật.
    for _pin in (spec.get("pins_card") or []):
        # 🔴 `beat` là GIÂY THẬT của lời đọc, còn app()/prog() so sánh với t/PACE ⇒ phải
        # chia PACE, đúng như L_art làm với `pins` (dòng ~1327). Bản đầu truyền beat thô:
        # PACE=1,35 nên sticker trễ 1,35× (beat 15,1 → hiện ở 20,3s) và ở clip 30s thì
        # gần như không thấy. Lỗi im lặng: clip vẫn đủ giây, exit 0.
        draw_pin(im, _pin, t, float(_pin.get("beat", 1.0)) / PACE, CARD_X0, CARD_Y0,
                 CARD_X1 - CARD_X0, CARD_Y1 - CARD_Y0)
    # ⭐ 2.8 — `src`: DÒNG NGUỒN nhỏ ở đáy-phải card. Vẽ ở frame() nên chạy được ở MỌI
    # layout, không phải nhét vào từng L_*.
    # Vì sao thành luật (T6: thẻ có số ⇒ phải có `src`): cả 3 kênh thắng đều ghi nguồn
    # ngay trên thẻ (カメ 「日本年金機構『繰上げ請求の注意点』」 dưới headline · フクロウ
    # 「(参考:日本年金機構HP2026年7月1日時点ページ)」 góc dưới · 保健室 「出典：デジタル庁」).
    # Ở ngách YMYL tiền, nguồn hiện trên màn là thứ mua được lòng tin mà lời nói không mua nổi.
    # ⚠️ KHÔNG thay khối 原典 — đây là dòng ghi công 1 dòng, 原典 vẫn phải là ảnh chụp thật.
    if spec.get("src"):
        _sf = fit(str(spec["src"]), "med", CARD_X1 - CARD_X0 - 260, 26, 18)
        ImageDraw.Draw(im).text((CARD_X1 - 74, CARD_Y1 - 18), str(spec["src"]),
                                font=_sf, fill=(150, 156, 168), anchor="rd")
    put_cast(im, _cast_at(spec, "left", t), "left")
    put_cast(im, _cast_at(spec, "right", t), "right")
    sub_bar(im, spec.get("sub"))
    return im.convert("RGB"), end


def _cast_at(spec, side, t):
    """Tên ảnh cast của MỘT bên tại giây t — có `cast_beats` thì đổi tư thế giữa thẻ.

    ⭐ 2.8 (2026-09-06). Vì sao cần: sàn nhịp đổi đơn vị từ "đổi ẢNH CHÍNH ≤9s" sang
    "SỰ KIỆN HÌNH ≤9s" (`audience-45plus.md` §2.0b, ngoại lệ lớp sân khấu). Đo trên file
    thật của 2 kênh thắng: カメ先生 khe median **3,0s** (1/340 khe >9s) · お金の保健室
    **2,8s** (0/587) — và thứ đổi mỗi ~3s KHÔNG phải cái thẻ (thẻ giữ 20–58s), mà là
    dòng phụ đề + **tư thế cast** + một phần tử mọc thêm. Không có khoá này thì thẻ giữ
    25s là 25s hai nhân vật đứng chết trân.

    Spec:  "cast_beats": {"right": [[0, "kikite_listen"], [6.5, "kikite_surprised"]]}
    Mốc = GIÂY THẬT của lời đọc (cùng đơn vị `beat` của pins) ⇒ phải chia PACE khi so
    với `t`, đúng bẫy đã dính ở `pins_card` 2.5 (bản đầu quên chia ⇒ trễ 1,35×).
    Không khai → trả về `left`/`right` như cũ ⇒ mọi thẻ cũ không đổi một pixel.
    """
    base = spec.get(side, CAST_DEFAULT[side])
    beats = (spec.get("cast_beats") or {}).get(side)
    if not beats:
        return base
    cur = base
    for b in beats:
        at, name = (b[0], b[1]) if isinstance(b, (list, tuple)) else (b["at"], b["name"])
        if t / PACE >= float(at):
            cur = name
    return cur


def build_end(spec):
    """Thời điểm phần tử CUỐI hiện xong — để biết cần dựng bao nhiêu frame.

    🔴 PHẢI tính cả `pins_card`: nó do frame() vẽ, KHÔNG qua LAYOUTS, nên build_end không
    thấy. Hậu quả đã dính (2026-08-25): thẻ pict có build_end ~8s mà sticker beat 15s ⇒
    render_clip chỉ dựng 8s frame rồi PAD bằng frame cuối ⇒ dấu đỏ 「上乗せ、だけ」 và số
    「5分」 KHÔNG BAO GIỜ xuất hiện, clip vẫn 30s và exit 0 — im lặng hoàn toàn.
    Cùng họ với bẫy "thiếu một biến ảnh hưởng tới hình thì tool báo xong mà hình sai".
    """
    im = Image.new("RGBA", (W, H))
    e = LAYOUTS[spec.get("layout", "check")](im, spec, -99)
    for pn in (spec.get("pins_card") or []):
        if isinstance(pn, dict) and pn.get("beat") is not None:
            e = max(e, float(pn["beat"]) / PACE + 0.55)
    # 🔴 VÁ 2026-08-26 (health 40, lớp sticker kiểu okura-demo): `props`/`props_top` cũng do
    # frame() vẽ ngoài LAYOUTS, và `t0` của nó là GIÂY THẬT (app_fly so t/PACE với t0) — tức
    # cùng đơn vị với `e` ở đây. Không tính ⇒ sticker gắn theo cụm từ đọc muộn trong thẻ
    # (sync_layer) rơi sau build_end ⇒ clip đóng băng trước khi nó hiện, đúng lỗi pins_card
    # 2.4 đã dính, chỉ ở khoá khác. Đây là lỗ ② của "3 chỗ phải đăng ký" (nenkin CLAUDE §②.6).
    for k, pr in enumerate((spec.get("props") or []) + (spec.get("props_top") or [])):
        if isinstance(pr, dict):
            e = max(e, float(pr.get("t0", 0.30 + 0.14 * k)) + 0.1)
    # 🔴 LỖ ② của "3 chỗ phải đăng ký" (nenkin CLAUDE §②.6), lần thứ TƯ ở khoá khác:
    # `cast_beats` do frame() đọc, KHÔNG qua LAYOUTS ⇒ build_end không thấy ⇒ clip chỉ
    # dựng tới lúc layout xong rồi PAD frame cuối ⇒ tư thế đổi ở giây 12 KHÔNG BAO GIỜ
    # hiện, clip vẫn đủ giây, exit 0. Đúng bệnh pins_card 2.4 và props 2.6 đã dính.
    for _bs in (spec.get("cast_beats") or {}).values():
        for b in (_bs or []):
            at = b[0] if isinstance(b, (list, tuple)) else b["at"]
            e = max(e, float(at) + 0.35)
    return (e + APP + 0.25) * PACE


def render_clip(spec, out, sec=CLIP_SEC, quiet=False):
    intro = min(build_end(spec), sec)
    n = max(int(intro * FPS), 2)
    tmp = Path(tempfile.mkdtemp(prefix="stage_"))
    try:
        for i in range(n):
            im, _ = frame(spec, i / FPS)
            im.save(tmp / f"f_{i:04d}.png")
        pad = max(sec - n / FPS, 0.1)
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS),
             "-i", str(tmp / "f_%04d.png"),
             "-vf", f"tpad=stop_mode=clone:stop_duration={pad:.2f}",
             "-c:v", "libx264", "-r", str(FPS), "-pix_fmt", "yuv420p",
             "-crf", "20", "-preset", "medium", str(out)], capture_output=True)
        if r.returncode:
            print(r.stderr.decode("utf-8", "replace")[-1200:])
            raise SystemExit("ffmpeg FAIL")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not quiet:
        print(f"  ✓ {Path(out).name}  (build-on {intro:.1f}s → đứng im tới {sec:.0f}s)")
    return out


# ══════════════════════════════════════════════════════ nối vào SLIDES.json
def _sig(spec):
    """Chữ ký nội dung của 1 thẻ → sidecar .sig.
    🔴 `render-background.md` §2.5: resume phải hỏi "file còn ĐÚNG không", KHÔNG phải
    "file có tồn tại không". Đổi spec/ảnh nhân vật/hằng số tool ⇒ dựng lại; y hệt ⇒ skip.
    Ảnh nhân vật vào chữ ký bằng mtime+size vì đổi bộ cast mà giữ tên là chuyện thường."""
    h = hashlib.md5(json.dumps(spec, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    # 🔴 BẢNG MÀU phải nằm trong chữ ký (thêm cùng lượt với `--channel`, 2026-08-10).
    # Không có dòng này thì đổi màu sân khấu ⇒ sig không đổi ⇒ "dựng 0 thẻ" ⇒ clip giữ màu cũ,
    # đúng lỗi đã dính 3 lần trong ngày (sổ thiếu ảnh · img/fill · icon). Đừng để lần thứ tư.
    parts = [VERSION, h, f"pal:{CARDC}{BG_TOP}{BG_BOT}"]
    # 🔴 BỘ NHÂN VẬT vào chữ ký cùng lượt với `--cast-dir` (2026-08-17). Cùng một thẻ, đổi
    # bộ cast / hệ số cỡ / biên zu ⇒ HÌNH ĐỔI, nên sig PHẢI đổi — đúng bài học "sổ thiếu ảnh
    # · img/fill · icon · palette" đã dính 4 lần: chữ ký thiếu một biến ảnh hưởng tới hình
    # thì tool báo "dựng 0 thẻ" và giữ clip cũ, im lặng.
    # ⚠️ CHỈ thêm khi LỆCH mặc định → sig của nenkin/kaigo/akiya không đổi một byte, khỏi
    #    phải dựng lại toàn bộ clip cũ.
    if str(CAST) != _CAST_DEFAULT_DIR:
        parts.append(f"cast:{CAST}")
    if CAST_SCALE != _CAST_SCALE_DEFAULT:
        parts.append(f"cscale:{sorted(CAST_SCALE.items())}")
    if (ZU_CAST_L, ZU_CAST_R) != _ZU_CAST_DEFAULT:
        parts.append(f"zucast:{ZU_CAST_L},{ZU_CAST_R}")
    for side in ("left", "right"):
        n = spec.get(side)
        if not n:
            continue
        f = CAST / f"{n}.png"
        if f.exists():
            st = f.stat()
            parts.append(f"{n}:{int(st.st_mtime)}:{st.st_size}")
    # 🔴 VÁ 2026-08-10 — chữ ký CÓ ảnh nhân vật nhưng THIẾU ảnh nội dung (`img`/`fill`),
    # tức đúng loại ảnh mà đời thật đến MUỘN (gen sau khi đã dựng thẻ lần đầu).
    # Chuỗi hỏng đã đo được ở video 10 nenkin: bỏ 4 ảnh `fill` vào art/ → chạy lại →
    # "dựng 0 thẻ, skip 73" vì spec không đổi ⇒ clip vẫn chứa ô vàng 「⚠ THIẾU ẢNH LẤP」.
    # Nguy hơn nữa là lúc ĐỦ ảnh: sổ `_MISSING_ART.json` tự xoá → preflight ④b cho qua →
    # video render ra với ô vàng và EXITCODE=0. Đúng thảm hoạ §1.5 đi vào bằng cửa sau.
    # Ảnh CHƯA CÓ cũng phải vào chữ ký (dạng `missing`) để lúc nó xuất hiện thì sig ĐỔI.
    for k in ("img", "fill", "bgimg"):
        n = spec.get(k)
        if not n:
            continue
        p = _art_path(n)
        if p is None:
            parts.append(f"{k}:{n}:missing")
        else:
            st = p.stat()
            parts.append(f"{k}:{n}:{int(st.st_mtime)}:{st.st_size}")
    # 🔴 VÁ 2026-08-26 — ICON của `props`/`props_top` cũng là ảnh ĐẾN MUỘN (sticker gen sau
    # khi thẻ đã dựng lần đầu, y hệt chuỗi hỏng img/fill ở trên). Không vào chữ ký ⇒ bỏ file
    # sticker vào assets/icons/ rồi chạy lại → "dựng 0 thẻ" → clip vẫn không có sticker,
    # im lặng. Lỗ ① của "3 chỗ phải đăng ký". Ghi `missing` để lúc file xuất hiện thì sig đổi.
    for pr in (spec.get("props") or []) + (spec.get("props_top") or []):
        nm = pr.get("icon") if isinstance(pr, dict) else None
        if not nm:
            continue
        p = icon_path(nm)
        if p is None:
            parts.append(f"icon:{nm}:missing")
        else:
            st = p.stat()
            parts.append(f"icon:{nm}:{int(st.st_mtime)}:{st.st_size}")
    # 🔴 Ảnh NESTED cũng phải vào chữ ký (2026-08-19, cùng lượt thêm layout `pict`):
    # `panels[].img` (pict) và `pins[kind=prop].img` được spec trỏ trong dict con →
    # vòng 3 khoá tầng thẻ ở trên KHÔNG thấy ⇒ thay ảnh mà thẻ không dựng lại — đúng họ
    # lỗi "sổ thiếu ảnh · img/fill · icon · palette" đã dính 4 lần. Quét đệ quy, nhưng
    # GIỮ vòng cũ nguyên thứ tự: thẻ không có ảnh nested thì sig không đổi một byte.
    nested = set()

    def _walk_art(node):
        if isinstance(node, dict):
            for kk, vv in node.items():
                if kk == "img" and isinstance(vv, str):
                    nested.add(vv)
                else:
                    _walk_art(vv)
        elif isinstance(node, (list, tuple)):
            for x in node:
                _walk_art(x)

    for kk, vv in spec.items():
        if kk not in ("img", "fill", "bgimg"):
            _walk_art(vv)
    for n in sorted(nested):
        p = _art_path(n)
        if p is None:
            parts.append(f"nimg:{n}:missing")
        else:
            st = p.stat()
            parts.append(f"nimg:{n}:{int(st.st_mtime)}:{st.st_size}")
    # 🔴 VÁ 2026-08-10 (lần thứ BA cùng họ lỗi trong một buổi) — ICON cũng phải vào chữ ký.
    # Icon được spec trỏ tới bằng TÊN (`["warning", "..."]`, `panels[].icon`…), nên sửa FILE
    # icon không đổi md5 của spec ⇒ thẻ không dựng lại. Ca thật: `warning.png` còn nguyên
    # watermark ✦ của Gemini (user bắt được), dùng ở 13/73 thẻ; vá icon xong mà không có
    # dòng này thì mọi thẻ vẫn giữ bản có watermark.
    # Quét ĐỆ QUY mọi chuỗi trong spec và nhận ra chuỗi nào là tên icon có thật → khoá này
    # tự phủ các layout thêm về sau, không phải liệt kê tay từng chỗ chứa icon.
    seen = set()

    def walk(v):
        if isinstance(v, str):
            if v not in seen and icon_path(v) is not None:
                seen.add(v)
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x)

    walk(spec)
    for n in sorted(seen):
        ip = icon_path(n)
        st = ip.stat()
        # đường dẫn vào chữ ký luôn: icon đổi từ kho CHUNG sang bản RIÊNG kênh (hoặc ngược
        # lại) thì hình đổi mà mtime/size có thể trùng ⇒ không có nó là thẻ không dựng lại.
        parts.append(f"ic:{n}:{ip.parent.name}:{int(st.st_mtime)}:{st.st_size}")
    return "|".join(parts)


def cmd_slides(a):
    """Đọc SLIDES.json → dựng clip cho mọi entry có khoá `stage`.

    Hợp đồng với `video_render.py` (KHÔNG phải mổ renderer): entry cần
        {"match": "...", "video": true, "stage": {...}}
    và clip ra đúng `clips/clip_<index>.mp4` — renderer đã biết đường dùng.
    """
    slides = Path(a.target)
    clips = Path(a.clips_dir)
    clips.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(slides.read_text(encoding="utf-8"))
    ART_ROOTS[:] = [clips.parent / "art", slides.parent, clips]
    (clips.parent / "art").mkdir(parents=True, exist_ok=True)
    only = set(a.only or [])
    made, skipped, missing_flag = [], 0, []
    for i, e in enumerate(cfg):
        v = e.get("stage")
        if not v or (only and i not in only):
            continue
        if not e.get("video"):
            missing_flag.append(i)
        out = clips / f"clip_{i:02d}.mp4"
        sig_p = clips / f"clip_{i:02d}.sig"
        sig = _sig(v)
        if not a.still and not a.force and out.exists() and sig_p.exists()                 and sig_p.read_text(encoding="utf-8") == sig:
            print(f"  [{i:02d}] {v.get('layout','check'):9s} — không đổi, skip")
            skipped += 1
            made.append(clips / f"clip_{i:02d}.png")
            continue
        png = clips / f"clip_{i:02d}.png"
        frame(v, 99)[0].save(png)          # frame cuối → để duyệt mắt
        if not a.still:
            render_clip(v, out, a.clip_sec, quiet=True)
            sig_p.write_text(sig, encoding="utf-8")
        be = build_end(v)
        print(f"  [{i:02d}] {v.get('layout','check'):9s} → "
              f"{out.name if not a.still else png.name}  (build-on {be:.1f}s)")
        has_beats = bool(v.get("beats")) or any(
            isinstance(p, dict) and p.get("beat") is not None
            for p in (list(v.get("pins", [])) + list(v.get("pins_card") or [])))
        if has_beats and be > a.clip_sec - 1.0:
            print(f"       🔴 beats đẩy build-on tới {be:.1f}s ≥ trần clip {a.clip_sec:.0f}s "
                  f"— phần tử cuối KHÔNG kịp hiện. Hạ mốc beats hoặc tăng --clip-sec.")
        elif not has_beats and be > 6.0:
            print(f"       ⚠️ build-on {be:.1f}s — nếu cue của câu này NGẮN hơn thì thẻ chưa "
                  f"lắp xong đã chuyển hình. Bớt dòng, hoặc cho thẻ ôm nhiều câu hơn.")
        made.append(png)
    # 🔴 SỔ THIẾU ẢNH — để `video_render.py` CHẶN được. Clip thiếu ảnh vẫn TỒN TẠI
    # (chứa ô "CHƯA CÓ ẢNH"), nên gate "file có chưa" của preflight cho qua tuốt →
    # render xong exit 0, ra video đầy ô vàng. Luật: đủ ảnh mới render (user chốt
    # 2026-08-09), và luật phải có chỗ cho máy đọc.
    miss_p = clips / "_MISSING_ART.json"
    want = {v["img"] for _, v in ((i, e.get("stage")) for i, e in enumerate(cfg))
            if v and v.get("layout") in ("art", "photo") and v.get("img")}
    # 🔴 VÁ 2026-08-10 — LỖ CÙNG HỌ VỚI CHÍNH BÌNH LUẬN Ở TRÊN, bắt được ở video 10 nenkin.
    # Khoá `fill` thêm ngày 2026-08-09 (chạy trên check/big/steps) nhưng sổ này KHÔNG đếm nó
    # → thiếu ảnh lấp thì `fill_art()` vẫn vẽ ô vàng "⚠ THIẾU ẢNH LẤP", clip vẫn tồn tại,
    # sổ vẫn rỗng, preflight ④b của video_render cho qua → video ra với ô vàng, EXITCODE=0.
    # Đúng cái lỗ mà sổ sinh ra để bịt, chỉ ở một khoá mới hơn. `fill` ăn ở MỌI layout nên
    # KHÔNG lọc theo `layout` như dòng trên.
    want |= {v["fill"] for v in (e.get("stage") for e in cfg) if v and v.get("fill")}
    want |= {v["bgimg"] for v in (e.get("stage") for e in cfg) if v and v.get("bgimg")}
    # 🔴 ĐẠO CỤ `pins[kind=prop].img` cũng là ảnh — phải vào sổ CÙNG LƯỢT với lúc thêm kind
    # (`render-background.md` §1.5 luật phái sinh). Thiếu đạo cụ thì `_prop()` chỉ in cảnh báo
    # rồi vẽ tiếp, clip vẫn ra, sổ vẫn rỗng, preflight ④b cho qua ⇒ đúng cái lỗ mà §1.5 sinh ra
    # để bịt, chỉ ở một khoá mới hơn. Đã dính y hệt ở khoá `fill` (nenkin video 10).
    want |= {p["img"] for v in (e.get("stage") for e in cfg) if v
             for p in (list(v.get("pins", [])) + list(v.get("pins_card") or []))
             if isinstance(p, dict) and p.get("kind") == "prop" and p.get("img")}
    # 🔴 PANEL của layout `pict` (2026-08-19, style りょう) — khoá ảnh mới vào sổ CÙNG LƯỢT
    # với lúc thêm layout (`render-background.md` §1.5 luật phái sinh, đã dính ở `fill`).
    # ⚠️ khoá spec cũng tên "panels" ở layout `compare` nhưng panel đó không có "img" →
    # comprehension này tự bỏ qua, không cần lọc theo layout.
    want |= {p["img"] for v in (e.get("stage") for e in cfg) if v
             for p in v.get("panels", [])
             if isinstance(p, dict) and p.get("img")}
    still = sorted(f for f in want if _art_path(f) is None)
    if still:
        miss_p.write_text(json.dumps(still, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"🔴 THIẾU {len(still)}/{len(want)} ẢNH — CHƯA ĐƯỢC RENDER VIDEO:")
        for f in still:
            print(f"     · {f}")
        print(f"   bỏ file vào {clips.parent / 'art'} rồi chạy lại lệnh này")
    elif miss_p.exists():
        miss_p.unlink()
    # ── GATE THẺ TRỐNG (user chốt 2026-08-09) ────────────────────────────────
    # "nếu video có nhiều chỗ trống quá thì bỏ hình minh hoạ vào, đừng để trống".
    # Đo MỨC ĐỘ PHỦ MỰC trong vùng CARD của frame cuối. Ngưỡng 4% suy từ số thật của
    # video 09 (132 thẻ): p25 = 4,4% · `check` TB 4,2% · `photo` 46% · `art` 30%.
    # Sửa bằng cách thêm dòng nội dung, HOẶC thêm khoá `"fill": "<ảnh>"` vào thẻ đó.
    thin = []
    for pth in made:
        if not pth.exists() or pth.suffix != ".png":
            continue
        try:
            import numpy as _np
            a = _np.asarray(Image.open(pth).convert("RGB"))[56:902, 272:1648].astype(_np.int16)
            ratio = float((_np.abs(a - 255).max(axis=2) > 18).mean())
        except Exception:
            continue
        if ratio < 0.040:
            thin.append((int(pth.stem.split("_")[1]), ratio))
    if thin:
        print(f"⚠️  {len(thin)}/{len(made)} THẺ QUÁ TRỐNG (phủ mực <4% vùng bảng) — "
              f"thêm dòng nội dung hoặc khoá \"fill\": \"<ảnh>\":")
        for i, r in sorted(thin, key=lambda x: x[1])[:14]:
            v = (cfg[i].get("stage") or {})
            print(f"     [{i:02d}] {r:4.1%}  {v.get('layout',''):7s} {v.get('title','')[:34]}")
        if len(thin) > 14:
            print(f"     … và {len(thin) - 14} thẻ nữa")

    print(f"— dựng {len(made) - skipped} thẻ, skip {skipped} —")
    if missing_flag:
        print(f"🔴 GATE STAGE: entry {missing_flag} có 'stage' nhưng THIẾU \"video\": true "
              f"→ renderer sẽ bỏ qua clip và rơi về ảnh tĩnh. Thêm cờ vào SLIDES.json.")
    if made:
        ps = [p for p in made if p.exists()]
        if ps:
            sheet = Image.new("RGB", (960 * 2, 540 * ((len(ps) + 1) // 2)), (255, 255, 255))
            for k, f_ in enumerate(ps):
                sheet.paste(Image.open(f_).resize((960, 540), Image.LANCZOS),
                            ((k % 2) * 960, (k // 2) * 540))
            sheet.save(clips / "_stage_sheet.jpg", quality=90)
            print("  ✓ _stage_sheet.jpg — DUYỆT MẮT trước khi render video")


# ══════════════════════════════════════════════════════ DEMO
DEMO = [
    {"layout": "flow", "title": "いつ、どうやって届くのか",
     "band": "2026年8月頃　〜　2027年2月頃",
     "steps": [("env", "簡易書留で\n一通の封筒"), ("bank", "差出人は\n日本年金機構"),
               ("doc", "中身は\n意向確認書")],
     "left": "sensei_point", "right": "kikite_listen",
     "sub": "日本年金機構から、一通の封筒が順次、送られます。"},

    {"layout": "check", "title": "登録されるのは、振り込みに必要な情報だけ",
     "ok": [("bank", "金融機関の名前"), ("doc", "口座の番号"), ("person", "ご本人のお名前など")],
     "no": [("doc", "残　高"), ("doc", "取引履歴")],
     "left": "sensei_present", "right": "kikite_surprised",
     "sub": "私の考えではなく、制度をつくった側が、明記しています。"},

    {"layout": "compare", "title": "住所を伝えても、家の中は見えない",
     "panels": [{"icon": "mailbox", "cap": "住所を伝える＝\nどこへ届けるかが分かる"},
                {"icon": "lock", "cap": "家の中の様子は\n見えない"}],
     "rows": ["口座情報 ＝ 振り込み先が分かるだけ", "残高・取引履歴 ＝ まったく別の話"],
     "left": "sensei_reassure", "right": "kikite_think",
     "sub": "「中にいくら入っているか」は、まったく別の話です。"},

    {"layout": "source", "title": "出どころは、デジタル庁の案内です",
     "org": "デジタル庁",
     "doc": "「年金受給者の方へ：年金振込口座で\n給付金等が受け取れるようになります」",
     "note": "※制度の内容は2026年7月時点の公表情報です",
     "left": "sensei_conclude", "right": "kikite_nod",
     "sub": "ぜひ、その言い方で伝えてさしあげてください。"},
]


def demo(outdir, sec=None):
    o = Path(outdir)
    o.mkdir(parents=True, exist_ok=True)
    stills = []
    for i, s in enumerate(DEMO):
        render_clip(s, o / f"stage_{i:02d}_{s['layout']}.mp4",
                    sec or CLIP_SEC)
        im, _ = frame(s, 99)                      # frame cuối → sheet duyệt mắt
        p = o / f"stage_{i:02d}_{s['layout']}.png"
        im.save(p)
        stills.append(p)
    sheet = Image.new("RGB", (960 * 2, 540 * 2), (255, 255, 255))
    for i, f_ in enumerate(stills[:4]):
        sheet.paste(Image.open(f_).resize((960, 540), Image.LANCZOS),
                    ((i % 2) * 960, (i // 2) * 540))
    sheet.save(o / "_stage_sheet.jpg", quality=92)
    print("  ✓ _stage_sheet.jpg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["demo", "clip", "still", "slides"])
    ap.add_argument("out", help="thư mục ra (demo/slides) hoặc file ra (clip/still)")
    ap.add_argument("--spec", help="file JSON 1 thẻ (clip/still)")
    ap.add_argument("--slides", help="đường dẫn SLIDES.json (bắt buộc với lệnh 'slides')")
    ap.add_argument("--only", nargs="*", type=int, help="chỉ dựng vài slot")
    ap.add_argument("--force", action="store_true", help="bỏ qua .sig, dựng lại hết")
    ap.add_argument("--still", action="store_true", help="chỉ xuất PNG (duyệt nhanh)")
    ap.add_argument("--sec", type=float, default=CLIP_SEC)
    ap.add_argument("--pace", type=float, help="giãn nhịp build-on (>1 = chậm hơn)")
    ap.add_argument("--channel", help="đọc bảng màu + BỘ NHÂN VẬT sân khấu từ channels.py "
                                      "(stage_card / stage_bg_top / stage_bg_bot / "
                                      "stage_cast_dir / stage_cast_scale / stage_cast_default / "
                                      "stage_zu_cast)")
    ap.add_argument("--cast-dir", help="ghi đè thư mục ảnh nhân vật (thắng cả --channel). "
                                      "Mặc định: assets/cast của nenkin.")
    a = ap.parse_args()
    if a.pace:
        globals()["PACE"] = a.pace   # ghi vào module để app()/prog() thấy
    if a.channel:
        # 🔴 Bảng màu là BẢN SẮC KÊNH → nguồn sự thật là `channels.py`, KHÔNG phải hằng số ở
        # đây (tool này dùng chung mọi kênh). Kênh không khai khoá nào thì giữ mặc định.
        # Khoá thiếu ⇒ im lặng dùng mặc định; đó là chủ ý, để kênh cũ không phải sửa gì.
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                               "youtube-jp-health" / "tools"))
        try:
            from channels import CHANNELS  # noqa: PLC0415
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"[LỖI] không đọc được channels.py: {e}")
        if a.channel not in CHANNELS:
            raise SystemExit(f"[LỖI] channels.py không có kênh {a.channel!r}")
        ch = CHANNELS[a.channel]
        for key, gname in (("stage_card", "CARDC"), ("stage_bg_top", "BG_TOP"),
                           ("stage_bg_bot", "BG_BOT")):
            if ch.get(key):
                globals()[gname] = tuple(ch[key])
        _BG_CACHE.clear()   # nền được cache 1 lần cho cả 900 frame — không xoá thì đổi màu vô hiệu
        # 🔴 BỘ NHÂN VẬT cũng là BẢN SẮC KÊNH (user chốt 2026-08-17: "khung nenkin riêng,
        # khung project này riêng"). Kênh KHÔNG khai khoá nào thì giữ mặc định của nenkin ⇒
        # nenkin và kaigo/akiya không phải sửa gì, và `_sig` của chúng không đổi một byte.
        if ch.get("stage_cast_dir"):
            globals()["CAST"] = Path(ch["stage_cast_dir"])
            _CAST_CACHE.clear()      # cache theo (tên, side) — đổi thư mục mà không xoá là lấy ảnh cũ
        if ch.get("stage_cast_scale"):
            CAST_SCALE.update(ch["stage_cast_scale"])   # THÊM prefix mới, không xoá prefix cũ
        if ch.get("stage_cast_default"):
            CAST_DEFAULT.update(ch["stage_cast_default"])
        if ch.get("stage_cast_fallback"):
            FALLBACK.update(ch["stage_cast_fallback"])
        if ch.get("stage_zu_cast"):
            globals()["ZU_CAST_L"], globals()["ZU_CAST_R"] = ch["stage_zu_cast"]
        print(f"[KÊNH] {a.channel} · card={CARDC} nền={BG_TOP}→{BG_BOT}")
        print(f"[CAST] {CAST}  scale={ {k: v for k, v in CAST_SCALE.items()} }")
        print(f"[CAST] mặc định L/R = {CAST_DEFAULT['left']} / {CAST_DEFAULT['right']}"
              f"  ·  ZU_CAST = {ZU_CAST_L}/{ZU_CAST_R}")
    if a.cast_dir:                    # cờ dòng lệnh THẮNG channels.py
        globals()["CAST"] = Path(a.cast_dir)
        _CAST_CACHE.clear()
        print(f"[CAST] ghi đè bằng --cast-dir: {CAST}")
    if not CAST.exists():
        raise SystemExit(f"[LỖI] thư mục nhân vật không tồn tại: {CAST}")
    a.clip_sec = a.sec
    if a.cmd == "slides":
        if not a.slides:
            raise SystemExit("[LỖI] lệnh 'slides' cần --slides <SLIDES.json>")
        a.target, a.clips_dir = a.slides, a.out
        cmd_slides(a)
    elif a.cmd == "demo":
        demo(a.out, a.sec)
    else:
        sp = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        if a.cmd == "clip":
            render_clip(sp, a.out, a.sec)
        else:
            frame(sp, 99)[0].save(a.out)
