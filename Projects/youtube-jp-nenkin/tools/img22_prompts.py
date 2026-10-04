# -*- coding: utf-8 -*-
"""
img22_prompts.py — CHUYỂN THỂ prompt VIDEO của video 22 thành prompt ẢNH TĨNH.

Vì sao có file này (user chốt 2026-09-09): gen video lỗi ⇒ cần bản lưng bằng ẢNH cho đúng
các shot đã lên kế hoạch, rồi hoạt hoá bằng `Projects/_media_library/animate_still.py`
(khung KHÔNG di chuyển, chỉ chuyển động cục bộ). Đường ảnh-tĩnh đã đo được ở ngách 昭和:
3 video 191K–232K view là ảnh tĩnh 100% (`audience-45plus.md` §2.0-ter).

🔴🔴 CÁCH LÀM ĐÃ ĐỔI 2026-09-09 (bản đầu sống đúng nửa ngày) — ĐỌC TRƯỚC KHI SỬA:
   Bản đầu **chép cấu trúc branch** của `flow22_full.prompt_for` rồi thay vài hằng số. Cùng
   ngày, `flow22_full` được sửa (POSTURE_BODY/HAND → REACT_FACE/HAND/CALM · TXT đổi sang
   «chỉ chữ số Ả Rập» · FORM thêm khối DENSE · thêm gate ⑱⑲ đòi ARABIC NUMERALS + bộ số thật)
   ⇒ bản chép **vỡ import ngay**. Và nếu import không vỡ thì còn tệ hơn: nó sẽ âm thầm sinh
   prompt theo LUẬT CŨ, gate mới báo đỏ mà không ai hiểu vì sao.
   ⇒ Nay file này **GỌI `F.prompt_for()`** rồi **BIẾN ĐỔI CHUỖI KẾT QUẢ**, thay đúng những
   khối do chính `flow22_full` định nghĩa (đọc constant từ module lúc chạy, không gõ lại).
   Thêm khuôn / đổi kho tư thế / siết guard bên kia thì bên này **tự ăn theo**.
   📌 Đây đúng là bài học `feedback_gate_va_builder_phai_cung_ten` — lần này tao tự dính.

Ba lớp bị biến đổi, và CHỈ ba lớp đó:
  ① MÁY QUAY   — `F.CAM_P` / `F.CAM_N` → bản ảnh (một khoảnh khắc đóng băng)
  ② KHUÔN      — mọi NOTE có chuyển động: needle sweeps · blocks fade in · objects drift ·
                 screen lights up · «for the whole shot» của HOLD · «live-action video»
  ③ MÔ TẢ CẢNH — 17 câu body có động từ chuyển động, sửa theo BẢNG TÊN (`DEMOTE`)

🔴 THÊM MỘT YÊU CẦU MÀ BẢN VIDEO KHÔNG CẦN: **ổ chuyển động cục bộ**. `animate_still.py` chỉ
   có steam/glow/sway/dustbeam/shimmer — cần trong ảnh có sẵn cửa sổ nắng, rèm mỏng, hơi trà
   hay vệt bụi để hiệu ứng bám vào; ảnh phẳng tuyệt đối thì hoạt hoá xong vẫn như đứng hình.
   Chỉ gắn cho khuôn CẢNH THẬT, và **theo NHÓM** (công sở không có chén trà bốc hơi).
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")

import flow22_full as F                            # noqa: E402
from flow22_full import classify, _cap             # noqa: E402
from plan22 import build                           # noqa: E402

OUT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"

# ── ① MÁY QUAY, bản ẢNH ─────────────────────────────────────────────────────
# Giữ nguyên phần đuôi (guard chữ + ánh sáng) mà flow22 đã viết; chỉ đổi vế nói về MÁY QUAY
# và vế «một hành động liên tục suốt shot».
_HEAD_IMG = "a single sharp still photograph, no motion blur"
_tail_p = F.CAM_P.split(F.CAM_BASE, 1)[-1].lstrip(", ")
_tail_p = _tail_p.replace("the person performs one single continuous action for the whole "
                          "shot and holds the posture above the rest of the time",
                          "the person is caught in one frozen instant and holds exactly the "
                          "posture described above")
CAM_P_IMG = f"{_HEAD_IMG}, {F.CAM_BASE.split(', ', 1)[1]}, {_tail_p}"
CAM_N_IMG = f"{_HEAD_IMG}, {F.CAM_N.split(', ', 1)[1]}"

# ── ② NOTE của từng khuôn — bỏ vế chuyển động, giữ nguyên phần HÌNH THỨC ────
NOTE_FIX = [
    ("the needle sweeps slowly from the left across the arc and settles, the rest of the "
     "panel stays perfectly still", "the needle sits in one fixed position along the arc"),
    ("Exactly the part described above lights up gently while the rest of the interface "
     "holds perfectly still", "Exactly the part described above is a little brighter than "
     "the rest of the interface"),
    ("the objects drift and orbit slowly", "the objects hang motionless in the air"),
    ("the blocks fade in one after another from left to right and then hold still, the "
     "camera never moves", "every block is fully drawn and equally visible"),
    ("; the camera stays locked off", ""),
    ("photorealistic live-action video", "photorealistic photograph"),
    ("infographic animation", "infographic illustration"),
    ("this shot will be placed", "this image will be placed"),
    # HOLD: giữ ý «đã ở tư thế cuối», bỏ ý «suốt cả shot»
    ("and it stays in exactly that same position for the whole shot, completely still and "
     "rigid", "and it is held flat and rigid, its face square to the camera"),
    ("in the very first frame", "in the frame"),
    # 🔴 SCREEN_NOTE bị viết lại 2026-09-09 (thêm khối bảng dày + số thật) — câu chốt cuối
    #    của nó mang chữ «for the whole shot». Gate bắt được vì nó quét prompt ĐÃ DỰNG.
    ("Neither the monitor nor the camera shifts by even a pixel for the whole shot, so the "
     "screen rectangle stays exactly where it starts",
     "The monitor and the camera are both perfectly still, so the screen reads as one "
     "crisp undistorted rectangle"),
]

# ── ③ BẢNG DEMOTION — câu body có chuyển động, sửa TỪNG CÂU ────────────────
# 🔴 CỐ Ý không regex chung: body là mô tả người viết, một regex "bỏ then/slowly" sẽ cắt giữa
#    câu ở chỗ không lường được. Bảng tên thì sai ở đâu thấy ở đó, và gate ở cuối quét lại
#    prompt ĐÃ DỰNG nên câu nào lọt bảng vẫn bị bắt (đã bắt 3 câu «lighting up» tao dò thiếu).
DEMOTE = [
 ("her hand comes to a stop and she looks down at the page",
  "her hand resting flat on the open page and her eyes looking down at it"),
 ("one date cell in each month lights up",
  "one date cell in each month is shaded in a soft colour"),
 ("a list of items whose green check marks light up one after another",
  "a list of items with a green check mark already beside every item"),
 ("the green tick boxes lighting up one after another",
  "every tick box already marked with a green tick"),
 ("three consecutive cells lighting up", "three consecutive cells shaded in a soft colour"),
 ("one row in its table lighting up", "one row in its table shaded in a soft colour"),
 ("the milestones lighting up from left to right", "all five milestones filled in a soft colour"),
 ("pushing his left hand forward toward the camera while drawing his right hand back "
  "toward his chest",
  "his left hand held out forward toward the camera and his right hand drawn back "
  "against his chest"),
 ("six evenly spaced round milestones that light up one after another from left to right",
  "six evenly spaced round milestones, all of them filled in a soft colour"),
 ("the blocks appearing one after another", "all three blocks fully drawn"),
 ("an envelope flies toward it and stops just in front of it, then the shield turns "
  "slightly and holds",
  "an envelope hangs frozen in the air just in front of it, the shield turned slightly"),
 ("and taps twice on the page with her index finger",
  "her index finger resting on one line of the page"),
 ("looks out through the window, then turns back toward the camera",
  "is turned back toward the camera, the bright window behind his shoulder"),
 ("shakes his head once, one palm turned upward",
  "has his head turned slightly to one side, one palm turned upward"),
 ("tilts her head, a faintly worried look on her face",
  "has her head tilted to one side, a faintly worried look on her face"),
 ("nods slowly, both forearms resting on the table",
  "has her chin lowered in a nod, both forearms resting on the table"),
 ("sand running slowly in both", "a thin stream of sand frozen in mid-fall in both"),
]

# ⑤ Ổ CHUYỂN ĐỘNG CỤC BỘ — mỗi ổ có KHOÁ để dò trùng (khối ánh sáng của flow22 đã tự nói
#    "window with sheer curtains", đạo cụ xoay vòng đã có "a green houseplant").
ANIM_HOME = [
    ("window",     "a sunlit window with a thin sheer curtain is visible at one side of the frame"),
    ("teacup",     "a teacup with a faint wisp of steam stands within the frame"),
    ("houseplant", "the leaves of a houseplant are visible at the edge of the frame"),
    ("dust",       "a shaft of daylight with fine dust in it crosses the back of the room"),
]
# 🔴 Kho riêng cho cảnh CÔNG SỞ: chén trà bốc hơi ở quầy bảo hiểm là vô lý (đã ra thật ở vòng
#    đầu). Cùng luật "ánh sáng/màu phải theo NHÓM khuôn" của flow22_full.
ANIM_PUB = [
    ("dust",  "a shaft of daylight with fine dust in it crosses the hall"),
    ("blind", "the slats of a window blind cast soft stripes on the wall"),
]
ANIM_KINDS = ("PERSON", "HOLD", "DESK", "SPLIT", "PANEL", "SCREEN", "GAUGE", "VIZ", "CROWD")

# gate: từ chuyển động còn sót trong prompt ĐÃ DỰNG ("explainer video" là tên thể loại)
MOTION = ("locked off", "does not move", "for the whole shot", "one continuous action",
          "lights up", "light up", "lighting up", "one after another", "sweeps", "drift",
          "orbit", "fade in", "appearing", "slowly", "then ", "comes to a stop",
          "live-action", "animation", "flies", "taps", "nods ", "shakes ", "tilts ",
          "running slowly", "pushing", "drawing his")


def pick_anim(idx: int, text: str, kind: str) -> str:
    pool = ANIM_PUB if kind == "CROWD" else ANIM_HOME
    low = text.lower()
    for k in range(len(pool)):
        key, clause = pool[(idx + k) % len(pool)]
        if key not in low:
            return f" {clause}."
    return ""


def build_prompt(body: str, idx: int = 0) -> str:
    """Prompt ẢNH = prompt VIDEO của flow22, biến đổi 3 lớp + gắn ổ chuyển động."""
    p = F.prompt_for(body, idx)
    p = p.replace(F.CAM_P, CAM_P_IMG).replace(F.CAM_N, CAM_N_IMG)     # ①
    for a, b in NOTE_FIX:                                             # ②
        p = p.replace(a, b).replace(_cap(a), (_cap(b) if b else ""))
    for a, b in DEMOTE:                                               # ③
        p = p.replace(a, b).replace(_cap(a), _cap(b))
    kind = classify(body)
    if kind in ANIM_KINDS:
        # 🔴 Guard chữ của flow22 KHÔNG kết thúc bằng dấu chấm ⇒ nối trực tiếp ra
        #    «…no watermark, no logo a teacup with a faint wisp of steam…»: câu ổ chuyển động
        #    dính vào danh sách cấm, model đọc thành một mệnh đề. Phải tự chấm câu.
        p = p.rstrip()
        if not p.endswith("."):
            p += "."
        p += pick_anim(idx, p, kind)
    return " ".join(p.split())


def main():
    rows = build()
    items = []
    for r in rows:
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        for k in range(r["nshot"]):
            suf = f"_{k+1}" if r["nshot"] > 1 else ""
            items.append(dict(stem=f"i22_{r['i']:02d}{suf}", clip=f"c22_{r['i']:02d}{suf}.mp4",
                              scene=r["i"], kind=classify(r["body"]),
                              prompt=build_prompt(r["body"], len(items))))

    io.open(os.path.join(OUT, "img22_FULL_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(x["prompt"] for x in items) + "\n")
    io.open(os.path.join(OUT, "img22_FULL_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1:>2} -> {x['stem']}.png   [scene {x['scene']:>2} · "
                  f"{x['kind']:<6} · thay {x['clip']}]" for i, x in enumerate(items)) + "\n")
    io.open(os.path.join(OUT, "img22_PROMPTS.md"), "w", encoding="utf-8").write(
        "# Prompt ẢNH TĨNH — video 22 (bản lưng của lô clip Veo)\n\n"
        "Gen ẢNH. Hoạt hoá: `python Projects/_media_library/animate_still.py <ảnh> "
        "--out clips/<clip>.mp4 --dur <giây> --preset tatami|kitchen|office|flat`\n\n"
        + "\n".join(f"### {x['stem']} — scene {x['scene']} · {x['kind']} · thay {x['clip']}\n\n"
                    f"```\n{x['prompt']}\n```\n" for x in items))

    errs = []
    for x in items:
        low = x["prompt"].lower().replace("explainer video", "explainer")
        for w in MOTION:
            if w in low:
                errs.append(f"{x['stem']}: còn từ chuyển động «{w.strip()}»")
    import collections
    print(f"\n⭐ {len(items)} prompt ẢNH -> img22_FULL_FLOW.txt")
    print(f"   khuôn: {dict(collections.Counter(x['kind'] for x in items))}")
    print(f"   dài prompt: {min(len(x['prompt']) for x in items)}–"
          f"{max(len(x['prompt']) for x in items)} ký")
    if errs:
        print("\n🔴 GATE:")
        for e in errs[:20]:
            print("  ", e)
        sys.exit(1)
    print("\n✓ GATE SẠCH: không còn từ chuyển động")


if __name__ == "__main__":
    main()
