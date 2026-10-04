# -*- coding: utf-8 -*-
"""
REALISM BLOCKS — khối prompt DÙNG CHUNG cho clip AI "thật, êm" (chốt 2026-09-22, user duyệt vòng 3).

Kênh dùng: youtube-jp-retrofuture (thế giới 昭和100年) · youtube-jp-showa (lớp L3 AI lấp, thế giới 昭和 thật).
Mỗi kênh GIỮ thế giới / cast / đề tài của mình — file này chỉ lo: máy quay · ánh sáng · nhịp người · chất ảnh.

VÌ SAO (đo 2026-09-22 trên 異世界さんぽ pJPST9DG92I 32K view/11 ngày, cùng bộ Google Veo với mình):
    | | mẫu | lô mình cũ (109 clip) | vòng 3 (user: "tạm rồi") |
    | MAD trong shot p50        | 1,5   | 9,4  | 2,3–7,9 (theo cảnh) |
    | % diện tích khung ĐANG động| 10%   | 87%  | 10–34% |
    | tốc độ phần đang động     | 14 px/s | 37 | 14–16 |
    | máy ở shot có di          | trôi 8–10 px/s | tới 1000px/8s | trôi 37–43px/8s |
    | sáng ngày / ấm (R−B)      | 108 / +27 | 111 / lạnh | 116–122 / +34…+38 |
  ⇒ "Thật" = ít thứ động + thứ động thì chậm + máy đứng hoặc trôi một bước/8s + ánh sáng MỘT NGUỒN có haze.
  ⇒ "Giống" = thế giới của kênh phải ở TRONG KHUNG mọi cảnh ngoại + nắng vàng ban ngày, không xám lạnh.
  ⇒ Model KHÔNG phải biến (cùng Veo 3.1 Lite đo ra cả hai đầu). Prompt ngắn 1,2–2,3k ký, không 13k.

QUY TRÌNH (Flow, 09/2026): chế độ Image (Nano Banana 2) dán STILL → chọn ảnh (thế giới ở nửa trên? nhịp 1 của
hành động? không chữ bịa?) → ⋮ Animate → dán MOTION → Veo 3.1 (Quality nếu đủ credit). Đo: check_realism.py.

⚠️ Hai giới hạn còn mở (vòng 3): cháy trắng 3–6% ở cảnh nắng (mẫu 0,5%) · i2v vẫn tự trôi máy 2–6% ở cảnh khoá.
"""

# [1] mở đầu + cấm chữ/số gộp một câu, phải đứng ĐẦU prompt (≤15%)
REALISM_HEAD = ("Live-action footage of real people in a real place, photographed on a cinema camera — "
"not animation, not CGI, not a render. No writing, lettering or numbers anywhere in the picture "
"except at most one shop sign carrying a single correct Japanese word.")

STILL_HEAD = ("A single photorealistic still photograph, wide 16:9, shot on a cinema camera with a fine "
"film grain — real people, real place, not an illustration and not a render. No writing, lettering or "
"numbers anywhere except at most one shop sign carrying a single correct Japanese word.")


# [2] MÁY — hai chế độ, tỉ lệ mẫu ≈ 2 khoá : 1 trôi. `where` = chỗ một NGƯỜI đứng được (camera-language §1.1)
def LOCKED_CAM(where, height):
    return (f"The camera is locked off on a tripod and does not move at all for the whole shot — no push, "
            f"no pull, no pan, no tilt, no drift, no handheld shake, the framing identical in the first and "
            f"last frame. It stands exactly where {where} would stand, at {height}, and everything is seen "
            f"from that one fixed place.")


def DRIFT_CAM(where, height):
    """Đo mẫu: shot có di chỉ trôi 8–10 px/s, zoom ±3–8%/shot = một bước chân trong 8 giây."""
    return (f"The camera stands exactly where {where} would stand, at {height}. Over the whole eight seconds "
            f"it eases forward by no more than a single slow step — the framing tightens so little that you feel "
            f"it rather than see it — with no pan, no tilt, no handheld shake, and the background stays solid.")


def cam_block(mode, where, height):
    return (DRIFT_CAM if mode == "drift" else LOCKED_CAM)(where, height)


# [3] ÁNH SÁNG — một nguồn, có haze, KHÔNG cháy. Ban ngày = NẮNG VÀNG (đo mẫu 108/+27), không "muted".
LIGHT = {
 "dawn": ("Light: the cold even blue of just before sunrise, no direct sun on the ground, one street lamp "
   "still burning warm, thin morning haze in the lane softening everything beyond a few metres; muted "
   "natural colour, nothing bright, nothing burnt out."),
 "day": ("Light: warm late-morning sunlight coming from one side, high and slightly behind, breaking "
   "through leaves and awnings into soft dappled patches on the ground and walls, the shaded parts open "
   "and full of bounced warm light, fine dust and haze glowing where the sun cuts through; rich natural "
   "colour, golden rather than grey, the greens deep and healthy, the brightest patches kept just short of "
   "white so that every highlight still holds colour and detail."),
 "interior": ("Light: one bright doorway or window is the main source, warm daylight falling across the "
   "timber and the people and dying away gently into the back of the room, a single warm bulb in the shade, "
   "steam and dust glowing where the light cuts through; warm natural colour, honey-coloured wood, the "
   "window itself bright but still showing what lies beyond it, nothing burnt to white."),
 "dusk": ("Light: the blue of dusk in the street against the warm orange of a few lamps just switched on, "
   "the two soft against each other, steam and haze catching the lamp light, most of the frame dim; "
   "muted natural colour, nothing glaring, nothing burnt out."),
 "night": ("Light: one low lamp is the only light, its glow falling off quickly into real darkness, the "
   "window a black rectangle, the picture allowed to be genuinely dark with the faces and hands lit "
   "only on one side; muted warm colour, nothing glaring, nothing burnt out."),
}

# [4] NHỊP NGƯỜI — đo mẫu 14 px/s: người cử động chậm, một động tác trải hết 8 giây
SUBJECT_GENTLE = ("Everyone moves gently and without hurry, the way people move early in the morning: each "
"gesture slow and deliberate, the one action spread across the whole eight seconds, nothing quick, nothing "
"sudden, nothing snapped or jerked. Only the person and the things they touch move; everything else in the "
"frame stays where it is.")

# [5] không nói · mặt ba-phần-tư · không nhìn máy
SILENT_REALTIME = ("No speed ramp and no slow-motion effect. Nobody speaks, mouths stay closed, the exchange "
"is in gesture and eyes only. Nobody looks at the camera and nobody performs for it; faces are seen in "
"three-quarter view or looking down at what the hands are doing, never frontal and never filling the frame.")

FACE_STILL = ("Faces in three-quarter view or looking down, nobody looking at the camera, no face filling "
"the frame.")

# [6] chất ảnh cuối
FILM_TAIL = ("Fine photographic film grain, shallow depth of field with one out-of-focus object at the near "
"edge of the frame, evenly exposed into all four corners, widescreen.")
STILL_TAIL = ("Shallow depth of field, one out-of-focus object at the near edge of the frame, evenly exposed "
"into all four corners, fine film grain.")


def build_pair(sc, world=""):
    """sc: dict(where, height, cam='locked'|'drift', light, still, act, alive[, extra])  → (still, motion, t2v).
    `world` = khối THẾ GIỚI của kênh (retrofuture: tháp tầng · showa: bối cảnh 昭和 thật) — rỗng nếu cảnh nội.
    Thứ tự khối là thứ quyết định (ai-video-regen.md §2): guard chữ → máy → cảnh/hành động → nhịp → ánh sáng."""
    cam = cam_block(sc.get("cam", "locked"), sc["where"], sc["height"])
    light = LIGHT[sc["light"]]
    still = " ".join(x for x in [STILL_HEAD, sc["still"], light, FACE_STILL, world, STILL_TAIL] if x)
    motion = " ".join(x for x in [REALISM_HEAD, cam,
                                   "Starting from exactly the framing of the first frame: " + sc["act"],
                                   SUBJECT_GENTLE, sc.get("alive", ""), light, SILENT_REALTIME] if x)
    # 🔴 t2v: hành động ĐẦY ĐỦ ghi MỘT lần (`act_full`). Nếu ghép still(=nhịp 1)+act(=phần tiếp) như motion
    #    thì với cảnh không tách được nhịp, cả hành động xuất hiện HAI lần → model diễn hai lần (showa 17 c013).
    act_t2v = sc.get("act_full") or sc["act"]
    still_t2v = sc.get("still_t2v") or sc["still"]
    t2v = " ".join(x for x in [REALISM_HEAD, cam, still_t2v, act_t2v, SUBJECT_GENTLE, sc.get("alive", ""),
                                light, SILENT_REALTIME, world, FILM_TAIL] if x)
    return still, motion, t2v


BAD_TOKENS = ("dolly", "handheld", "35mm", "16mm", "vivid", "hdr", "sunny", "bright blue sky", "cinematic",
              "masterpiece", "8k", "push in", "pull back", "tracking shot", "slow motion")
LIMIT = {"still": (900, 2000), "motion": (1300, 2100), "t2v": (1800, 3300)}
# showa: luat kenh bat ta KHUON MAT tung cast + chu ky bieu cam => dai hon ~1k ky, tran rieng
LIMIT_SHOWA = {"still": (900, 2600), "motion": (1300, 3500), "t2v": (1800, 5000)}


def _strip_neg(lo):
    import re
    BS = chr(92)
    return re.sub(BS + "b(?:no|never|not|nothing)" + BS + "b[^,.;—]*", " ", lo)


BS_ = chr(92)


def gate_prompt(kind, p, limit=None):
    """Trả list lỗi (rỗng = sạch). Quét token cấm SAU KHI bỏ mệnh đề phủ định (ai-video-regen.md §6)."""
    import re
    probs = []
    lo = p.casefold()
    lo_, hi_ = (limit or LIMIT)[kind]
    if not (lo_ <= len(p) <= hi_):
        probs.append(f"do dai {len(p)} ngoai {lo_}–{hi_}")
    i = lo.find("no writing")
    if i < 0 or (i > 300 and i * 100 // len(p) > 15):      # guard o dau: <=300 ky HOAC <=15%
        probs.append("guard chu/so khong o 15% dau")
    if kind != "still":
        j = max(lo.find("locked off"), lo.find("eases forward by no more than"))
        if j < 0 or j * 100 // len(p) > 30:
            probs.append("khoi may khong o 30% dau")
    pos = _strip_neg(lo)
    probs += [f"token cam: {b!r}" for b in BAD_TOKENS
              if re.search(BS_ + "b" + re.escape(b) + BS_ + "b", pos)]      # bien tu: 'hdr' khong bat 'withdraw'
    if re.search(chr(92) + "d", p.replace("16:9", "")):
        probs.append("co chu so trong prompt (model hay in so len hinh)")
    return probs


# =============================================================================
# GATE HÀNH ĐỘNG — 5 kiểu lỗi đo được trên 14 clip t2v showa 17 (user: "hành động lỗi tùm lum", 2026-09-22)
#   ① ĐÁM ĐÔNG phải DI CHUYỂN / TỤ LẠI  → model dựng sẵn đám đứng im, 3/3 cảnh không ai đi (c001 c003 c010)
#   ② ĐẠI TỪ không có chủ ("his hand…" mà cảnh không khai ai) → ra người khác + bàn tay lạ (c005)
#   ③ VẬT NHỎ trên tay (đinh ghim, tờ giấy) → giấy bay khỏi bảng (c013); cùng họ feedback_ai_video_hong_thao_tac_tay
#   ④ HÀNH ĐỘNG NÓI ("says something short") → không quay được, model bịa (c003)
#   ⑤ >2 nhịp trong 8s → đã cắt ở _tighten
#   Cái chạy: MỘT người · MỘT động tác TO · đám đông ĐỨNG YÊN (c006 c008 c010 c011 c013 của lô đó).
# =============================================================================
PRONOUN_START = ("he", "she", "his", "her", "they", "their", "him", "them")
# ⚠️ ban dau: "pen " an vao open/pendant · "shift" an vao "shift the basin to the other hand" · "one after another"
#    an vao cua troi qua trong canh tho => 40 bao do gia. Bien tu + danh sach hep, va bo menh de phu dinh truoc.
CROWD_MOVE = ("gather", "gathers", "come along the corridor", "from both ends", "shift closer", "shifts closer",
              "shift one pace", "shifts one pace", "press closer", "presses closer", "crowd forward",
              "rise onto their toes", "lean in all together", "grows until", "put their heads up one after another",
              "file in", "stream in", "pour in")
SPEECH = ("says something", "say something", "speaks to", "tells him", "tells her", "asks him", "asks her",
          "calls out", "answers", "replies", "mutters", "whispers")
SMALL_OBJ = ("drawing pin", "drawing pins", "thumbtack", "pins a", "pins the", "pins up", "pencil", "the pen",
             "a pen", "his pen", "coin", "coins", "needle", "chopsticks", "cigarette", "matchstick", "rubber stamp",
             "stamps it", "folded slip", "slip of paper")
HOLD_CLAUSE = ("Every object stays in the hand that holds it or exactly where it lies: nothing is dropped, nothing "
               "floats, nothing slides off, nothing multiplies, and hands keep the same number of fingers.")


def gate_action(act, has_cast=True):
    """Trả list (kind, msg): kind ① đám đông di · ② đại từ không chủ · ③ vật nhỏ · ④ hành động nói.
    Quét TRÊN HÀNH ĐỘNG đã bỏ mệnh đề phủ định ("neither of them speaks" không phải hành động nói)."""
    import re
    BS = chr(92)
    lo = act.casefold().strip()
    pos = re.sub(BS + "b(?:no|nobody|neither|never|not|nothing|without)" + BS + "b[^,.;]*", " ", lo)
    def has(words):
        return any(re.search(BS + "b" + re.escape(w) + BS + "b", pos) for w in words)
    probs = []
    if not has_cast and re.match("(?:" + "|".join(PRONOUN_START) + ")" + BS + "b", lo):
        probs.append(("②", "dai tu khong co chu — khai ro NGUOI lam"))
    if has(CROWD_MOVE):
        probs.append(("①", "dam dong phai DI/TU — doi thanh dam dong DUNG YEN, mot nguoi lam"))
    if has(SPEECH):
        probs.append(("④", "hanh dong NOI — doi thanh cu chi (liec, nghieng dau, gat)"))
    if has(SMALL_OBJ):
        probs.append(("③", "vat nho tren tay — da them HOLD_CLAUSE; van soi 4 frame khi gen"))
    return probs
