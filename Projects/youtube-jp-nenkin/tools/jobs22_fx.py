# -*- coding: utf-8 -*-
"""
jobs22_fx.py — viết lại `jobs.jsonl` của lô i2v video 22, **hiệu ứng ghép thẳng vào prompt**.

user chốt 2026-09-10: *"các hiệu ứng viết luôn trong prompt, mày không cần làm nữa, video tự
gen"*. ⇒ BỎ lớp `fx` của Remotion cho lô này; mô hình video tự dựng hiệu ứng.

    python tools/jobs22_fx.py 06_VIDEO/22_mishikyu-nenkin-36man/i2v

Đọc `_MANIFEST.json` + `jobs.jsonl` (do `story_extract.py` sinh), ghi đè `jobs.jsonl` với
prompt mới. Giữ nguyên `id · mode · first · duration` — chỉ đổi `prompt`.

─────────────────────────────────────────────────────────────────────────────────
🔴 BA RÀNG BUỘC KHÔNG ĐƯỢC PHÁ, đều là lỗi đã dính thật trong lô này:

① **KHÔNG chữ mới.** Veo dựng chữ Nhật NÁT (đo 0/6 clip). Mọi hiệu ứng ở đây là ÁNH SÁNG,
   HẠT, VẬT — không có nhãn, không con số bay, không bảng chữ. Số liệu đã nằm sẵn trong
   ảnh nền và do lớp telop của Remotion vẽ đè.

② **KHÔNG đỏ cảnh báo.** user chốt *"màu đỏ trong video không hợp hoàn cảnh"* — bài nói về
   tiền NGƯỜI XEM ĐƯỢC NHẬN, không phải mối nguy. Hiệu ứng dùng **hổ phách / vàng ấm /
   trắng ngà**. Ngoại lệ duy nhất: con dấu 実印 vốn là mực đỏ THẬT trong ảnh, không phải
   hiệu ứng mình thêm.

③ **KHÔNG lặp.** user kết án hai lần (*"cách hiệu ứng lặp lại quá nhiều"*). Tool tự chặn:
   không bao giờ hai shot liền nhau cùng hiệu ứng, và **trần 40% số shot** có hiệu ứng —
   hạt là ĐIỂM NHẤN, rải đều khắp thì không còn gì là nhấn.
─────────────────────────────────────────────────────────────────────────────────

⚠️ Vì sao câu đuôi phải ĐỔI khi có hiệu ứng: đuôi i2v gốc ghi *"only what is described
   above moves, once, slowly, and it holds still for the rest of the shot"* — câu đó CẤM
   luôn hiệu ứng chạy liên tục. Giữ nguyên nó rồi thêm mưa xu vào là hai vế chọi nhau, và
   mô hình sẽ bỏ một vế mà mình không biết vế nào (đúng bệnh đã ghi ở
   `feedback_prompt_khoi_chung_huy_mo_ta`).
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── ĐUÔI PROMPT ────────────────────────────────────────────────────────────────
KEEP = ("Keep the framing, composition, characters, clothing, props and colours of the given "
        "image exactly as they are; the camera stays locked off and does not move, no zoom, "
        "no pan, no cut to another shot.")
# 🔴🔴 ĐẢO CHIỀU 2026-09-10 (user: *"bỏ cái này đi. Tao muốn hành động nó phải nhiều lên
#    chứ không phải đứng im"*). Câu cũ là:
#      "Only what is described above moves, once, slowly, and it holds still for the rest…"
#    ⇒ nó biến 8 giây thành **1 động tác + 7 giây đứng hình**. Đúng thứ user chê.
#
# ⚠️ NHƯNG có một nửa của câu đó PHẢI GIỮ, và đây là chỗ đo được chứ không phải tao cẩn thận
#    thừa: `feedback_ai_video_hong_thao_tac_tay` — **58/73 clip của video 21 hỏng**, và hỏng
#    tập trung ở đúng một loại việc: **thao tác tay làm VẬT ĐỔI TRẠNG THÁI** (đeo kính rồi
#    kính biến mất · nắp hộp thư đóng rồi mở lại · phong bì biến mất · bút đỏ nhân đôi).
#    Càng nhiều thao tác kiểu đó trong 8 giây thì càng nhiều chỗ để vật nhảy trạng thái.
#
# ⇒ Cách chia đúng: **MỞ HẾT chuyển động của THÂN – ĐẦU – MẶT – TAY ĐANG CẦM** (chỗ mô hình
#   làm tốt, và là chỗ mắt đọc ra "đang sống"), **GIỮ khoá ở việc vật đổi trạng thái**
#   (nhặt lên / đặt xuống / mở / đóng / đeo vào / tháo ra). Được nhiều hành động mà không
#   bước vào vùng đã đo là hỏng.
_CHAIN = ("Fill the whole eight seconds with a continuous chain of small natural movements so "
          "that nothing ever freezes: the person shifts their weight, turns their head, their "
          "eyes move and blink, their chest rises and falls with a breath, their fingers adjust "
          "their grip, their eyebrows and mouth change with what they are feeling, and they "
          "settle into a different posture by the end than the one they started in. Whatever is "
          "already in their hands stays in their hands and stays in the same state throughout — "
          "nothing is picked up, put down, opened, closed, put on or taken off.")
ONE_MOVE = _CHAIN
# bản dùng khi CÓ hiệu ứng: chuỗi chuyển động y hệt, cộng lớp hiệu ứng chạy suốt shot
ONE_MOVE_FX = (_CHAIN + " The light effect described above runs gently for the whole shot "
               "alongside that movement, without changing the person, the room or any object "
               "already in the image.")
NO_TEXT = ("Any printing on paper or screens stays exactly as in the image; no new text appears, "
           "no numbers appear, no captions, no watermark, no logo.")

# ── KHO HIỆU ỨNG — 24 cái, chia 8 NHÓM NGHĨA, mỗi nhóm 3 biến thể ─────────────
# 🔴 user chốt 2026-09-10 (lần thứ HAI về lặp): *"mày có thể tự thêm nhiều hiệu ứng khác cho
#    nó hợp lý chứ đừng lặp đi lặp lại 1 hiệu ứng"*. Bản trước có 8 hiệu ứng nhưng `pulse` và
#    `coins` mỗi cái dùng **6 lần** — kho nhỏ thì chặn-liền-kề không cứu được, nó chỉ giãn ra
#    chứ vẫn lặp. ⇒ Ba tầng chặn: **kho to (24)** · **mỗi nhóm 3 biến thể xoay vòng** ·
#    **trần 2 lần/hiệu ứng cho cả video**.
# ⚠️ Ưu tiên HIỆN TƯỢNG CÓ THẬT (bụi trong nắng · rèm lay · bóng đổ dịch · hơi nước · nắng
#    trôi) hơn là đồ hoạ dán vào: ảnh nền là ảnh chụp thật, hiệu ứng vật lý hoà vào được,
#    còn đồ hoạ thì lộ ra "dán". Xu vàng là ngoại lệ có chủ ý — nó là ẩn dụ tiền của bài.
FX = {
    # ① TIỀN
    "coin_fall": ("a few small gold coins drift slowly down through the empty part of the frame, "
                  "turning as they fall, and fade out before they reach the bottom edge"),
    "coin_glint": ("a slow highlight travels across the metal of the coins so they catch the "
                   "light one after another"),
    "coin_rise": ("two or three gold coins float slowly upward out of the lower edge of the "
                  "frame and fade as they rise"),
    # ② SỔ / GIẤY TỜ
    "page_shimmer": ("a faint golden shimmer runs once along the edge of the paper and fades"),
    "page_breath": ("the corner of the paper lifts and settles very slightly, as if a breath of "
                    "air passed over the desk"),
    "line_glow": ("one printed line on the page brightens softly for a moment, then eases back "
                  "to normal without changing what it says"),
    # ③ THỜI GIAN / LỊCH
    "sweep": ("a soft band of warm light sweeps once across the surface from left to right and "
              "fades"),
    "shadow_creep": ("the shadow cast across the surface slides slowly, as if the sun were "
                     "moving over the course of the shot"),
    "cell_bloom": ("one square of the calendar warms and brightens gently, then settles back"),
    # ④ VỠ LẼ / NGHI VẤN
    "halo_pulse": ("a soft amber halo swells once around the subject and fades away"),
    "corner_dim": ("the corners of the frame darken very gradually, pulling the eye inward"),
    "focus_settle": ("the background softens a little further out of focus while the subject "
                     "stays sharp"),
    # ⑤ CÔNG SỞ / ĐÁM ĐÔNG
    "dust": ("fine motes of dust drift slowly through the bar of daylight, catching the light "
             "as they turn"),
    "bg_bokeh_move": ("the out-of-focus people far behind shift and pass slowly, keeping the "
                      "foreground exactly as it is"),
    "ceiling_wash": ("the overhead light brightens a touch across the room, then evens out"),
    # ⑥ NHẸ NHÕM / KẾT
    "warm_lift": ("the daylight in the frame warms and brightens very slightly, then settles"),
    "curtain_breeze": ("the curtain and the leaves outside the window sway once in a slow draught"),
    "bokeh_drift": ("warm out-of-focus points of light drift gently in the background"),
    # ⑦ MÀN HÌNH
    "screen_wake": ("the light thrown by the screen onto the desk and the face strengthens "
                    "slightly, then holds"),
    "screen_scan": ("a soft band of brightness passes down the screen once, the way a display "
                    "refreshes, without altering anything shown on it"),
    "reflect_slide": ("the reflection on the glass of the screen slides slowly as the light "
                      "outside changes"),
    # ⑧ HOÀN TẤT / ĐÓNG DẤU
    "sparkle": ("tiny warm golden sparkles bloom one after another just above the paper, each "
                "appearing and fading softly"),
    "settle_dust": ("a faint puff of fine dust lifts off the paper and drifts away"),
    "edge_light": ("a thin line of light traces the outline of the object once and fades"),
}

# ── NHÓM NGHĨA: regex → danh sách biến thể (xoay vòng) ────────────────────────
RULES = [
    (r"coin|money|deposit|amount|figure|payment|yen|balance|scale",
     ["coin_fall", "coin_glint", "coin_rise"], "TIỀN"),
    (r"passbook|bank entr|transaction|document|form|paper|brochure",
     ["page_shimmer", "page_breath", "line_glow"], "GIẤY TỜ"),
    (r"calendar|date|month|timeline|schedule|deadline|april|february",
     ["sweep", "shadow_creep", "cell_bloom"], "THỜI GIAN"),
    (r"realiz|shock|question|uncertain|weighty|contemplat|absence|disagree",
     ["halo_pulse", "corner_dim", "focus_settle"], "VỠ LẼ"),
    (r"office|hall|waiting|counter|window|overhead",
     ["dust", "bg_bokeh_move", "ceiling_wash"], "CÔNG SỞ"),
    (r"relief|peace|solidarity|light and order|bird|garden|shared",
     ["warm_lift", "curtain_breeze", "bokeh_drift"], "NHẸ NHÕM"),
    (r"glow|screen|nenkin net|website|link|tap|click",
     ["screen_wake", "screen_scan", "reflect_slide"], "MÀN HÌNH"),
    (r"stamp|seal|ink|final|finish|closing|storing",
     ["sparkle", "settle_dust", "edge_light"], "HOÀN TẤT"),
]
CAP = 0.45          # trần tỉ lệ shot có hiệu ứng
MAX_EACH = 2        # 🔴 trần MỖI hiệu ứng cho cả video — thứ chặn được cái user chê


def pick(text: str):
    for pat, key, why in RULES:
        if re.search(pat, text, re.I):
            return key, why
    return None, ""


def main() -> int:
    if len(sys.argv) < 2:
        print("dùng: python tools/jobs22_fx.py <thư mục i2v>"); return 1
    d = sys.argv[1]
    man = json.load(io.open(os.path.join(d, "_MANIFEST.json"), encoding="utf-8"))
    jobs = [json.loads(l) for l in io.open(os.path.join(d, "jobs.jsonl"), encoding="utf-8")
            if l.strip()]
    if len(man) != len(jobs):
        print("🔴 MANIFEST %d dòng ≠ jobs %d dòng" % (len(man), len(jobs))); return 1

    limit = int(len(jobs) * CAP)
    used, prev, log = 0, None, []
    turn = {}                       # nhóm -> con trỏ xoay vòng biến thể
    count = {}                      # hiệu ứng -> đã dùng mấy lần
    for j, m in zip(jobs, man):
        # 🔴 TOOL PHẢI IDEMPOTENT. Chạy lần hai trên chính file nó vừa ghi thì cụm
        #    "IN ADDITION: …" cũ vẫn nằm trong `head` ⇒ nó CHỒNG hiệu ứng thứ hai lên.
        #    Đã dính thật: 17/66 prompt có hai "IN ADDITION:" và gate lặp báo đỏ, trong
        #    khi luật gán không sai — sai ở chỗ tool đọc lại đầu ra của chính mình.
        head = j["prompt"].split(KEEP)[0].strip()
        head = re.sub(r"\s*IN ADDITION:.*?(?<=\.)\s*$", "", head, flags=re.S).strip()
        text = m["title"] + " " + m["sceneTitle"] + " " + (m["visual"] or "")
        key = why = None
        for pat, variants, cat in RULES:
            if not re.search(pat, text, re.I):
                continue
            # xoay vòng biến thể trong nhóm, bỏ qua cái đã chạm trần hoặc trùng shot trước
            for k in range(len(variants)):
                cand = variants[(turn.get(cat, 0) + k) % len(variants)]
                if cand != prev and count.get(cand, 0) < MAX_EACH:
                    key, why = cand, cat
                    turn[cat] = turn.get(cat, 0) + k + 1
                    break
            break
        if key and used >= limit:
            key, why = None, "bỏ — chạm trần %d%%" % int(CAP * 100)
        if key:
            j["prompt"] = " ".join([head, "IN ADDITION:", FX[key] + ".",
                                    KEEP, ONE_MOVE_FX, NO_TEXT])
            used += 1
            count[key] = count.get(key, 0) + 1
            prev = key
        else:
            j["prompt"] = " ".join([head, KEEP, ONE_MOVE, NO_TEXT])
            prev = None
        log.append((m["idx"], m["title"][:34], key or "—", why or "không khớp nhóm nào"))

    with io.open(os.path.join(d, "jobs.jsonl"), "w", encoding="utf-8") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")

    # sổ tay để soi bằng mắt — đừng bắt người đọc mở jsonl
    with io.open(os.path.join(d, "_FX_MAP.md"), "w", encoding="utf-8") as f:
        f.write("# Hiệu ứng gán cho từng shot (jobs22_fx.py)\n\n")
        f.write("| # | shot | hiệu ứng | vì sao |\n|---|---|---|---|\n")
        for i, t, k, w in log:
            f.write("| %d | %s | **%s** | %s |\n" % (i, t, k, w))

    import collections
    c = collections.Counter(k for _, _, k, _ in log if k != "—")
    print("✅ %s/jobs.jsonl — %d job" % (d, len(jobs)))
    print("   có hiệu ứng: %d/%d (%.0f%%, trần %.0f%%)"
          % (used, len(jobs), 100 * used / len(jobs), 100 * CAP))
    print("   phân bố: %s" % dict(c))
    print("   sổ tay: %s/_FX_MAP.md" % d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
