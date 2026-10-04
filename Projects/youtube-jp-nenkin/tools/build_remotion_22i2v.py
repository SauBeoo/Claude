# -*- coding: utf-8 -*-
"""
build_remotion_22i2v.py — DEMO video 22 dựng bằng **CLIP i2v THẬT** (Veo qua Google Flow).

Khác hai demo trước (`22demo` · `22d2`) ở đúng một điểm bản chất: hai bản kia dùng **ẢNH
TĨNH** vì lô clip chưa có; bản này là lớp hình THẬT của khuôn video 22 — footage 8s toàn
khung + telop + fx "hoa lá cành" + 3 overlay dán cứng + phụ đề cháy.

CỬA SỔ DEMO: **scene 0–18 = 0,0→136,1s** (cold open + chương ĐỊNH VỊ/後払い).
  Chọn đúng khúc này vì đó là chỗ 12 clip đã gen phủ ĐÚNG NỘI DUNG từng scene. Kéo dài
  thêm thì phải lấp bằng clip lệch lời — thà giao ngắn mà khớp.

🔴 CLIP → SCENE lấy từ bảng `SHOTS`, là bản **đã soi mắt** từng cặp (frame clip ↔ ảnh
   start-frame), không phải fuzzy-match. Sổ map + mấy clip còn ngờ: `_MAP_I2V.md`.

📐 Nhịp: 12 khe footage / 2,27′ = **5,3 đổi hình/phút** (trần 6 — `audience-45plus.md` §2).
   Track `trk-genten` TÁCH khỏi `trk-video` để ảnh 原典 tĩnh không bị tính vào trần đó
   (`feedback_gate_va_builder_phai_cung_ten`).

🔴 fps = 24: clip Veo là 24fps, ép 30 thì 27% frame lặp ⇒ judder.
🔴 Khe dài hơn 8,000s ⇒ hạ `speed = 8,0/khe`, **chỉ được làm CHẬM** (CLAUDE.md §②).
"""
import io
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _scenes22 import SCENES                                       # noqa: E402
from plan22 import build                                           # noqa: E402

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-22i2v"
FPS, W, H = 24, 1920, 1080
VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
TL = os.path.join(VD, "timeline.json")
ASSETS = os.path.join(ROOT, "public", "projects", NAME, "assets")

SRC_SEC = 8.000              # độ dài THẬT của clip Veo
MASCOT_FRAMES = 192          # 8s × 24fps — số THẬT của lô PNG
FADE = 7                     # ~0,3s cross-dissolve
SCENE_LO, SCENE_HI = 0, 18   # cửa sổ demo (chỉ số scene trong _scenes22)

f = lambda s: max(0, int(round(s * FPS)))

# grading: lô clip đã sáng sẵn nhờ prompt (bright airy / white walls) nên để rất nhẹ.
# Nhân mạnh là cháy cửa sổ — đã dính ở lô ảnh trước.
GRADE = {"brightness": 1.04, "contrast": 1.0, "saturate": 1.08}

# ── KHE FOOTAGE: (scene đầu, scene cuối bao gồm) -> clip ──────────────────────
# scene cuối > scene đầu = một clip trải qua nhiều scene (đúng cách plan22 phân bổ:
# scene 1 và 12 có nshot=0 nên dùng chung clip với scene trước).
SHOTS = [
    ((0, 1),   "sb_03"),   # tay mở 通帳 — chủ thể của bài ở entry 0 (media-library §2.0)
    ((2, 2),   "sb_06"),   # cận dòng 360,000 trong sổ
    ((3, 3),   "sb_13"),   # split-screen HAI lần 36万 giống hệt
    ((4, 4),   "sb_05"),   # cận trang sổ — 見た目は同じ
    ((5, 5),   "sb_08"),   # vợ chỉ vào dòng, chồng nhìn
    ((6, 6),   "sb_14"),   # dấu ? nổi trên hai dòng — 線はどこに
    ((7, 7),   "sb_09"),   # hai vợ chồng — ご両親/ご主人/奥さま
    ((8, 8),   "sb_37"),   # bà cụ gọi điện — 黙っていても入る？
    ((11, 12), "sb_19"),   # quầy 年金事務所 — なぜ残る / 後払い
    ((15, 15), "sb_25"),   # dải thời gian trên bàn — 二か月前
    ((16, 16), "sb_10"),   # lịch tường — 必ず残る分
    ((17, 17), "sb_20"),   # nhân viên đưa tờ 請求書 — これが未支給年金
]

# ── 原典 scene 13 (79,7→100,9 = 21,1s): CHUỖI TIẾT LỘ, không một tấm đứng im ─────
# Mốc lấy từ chính lời đọc (timeline dòng 14–15), khoanh đỏ đổi chỗ theo câu:
#   79,7  「こちらが、日本年金機構のページです」          → chưa khoanh
#   82,8  「赤で囲んだところを、ご覧ください」            → khoanh CẢ BẢNG
#   88,8  「年六回…偶数月の十五日に支払われます」          → khoanh CỘT 支払月
#   94,8  「その前月までの二か月分の年金が支払われます」    → khoanh HÀNG 4月
# 🔴 Vì sao phải chẻ: một tấm 21,2s là khe đứng yên duy nhất mà `check_frame_pace` gate ②
#    bắt được trên project này — và đó là lỗi THẬT, không phải báo giả (khác gate ③, xem
#    ghi chú ở đầu file). Chẻ bằng cách đổi CHỖ KHOANH nên không zoom, không mất nét.
GENTEN = {13: [(79.72, "genten_shiharai.png"),
               (82.79, "genten_shiharai_all.png"),
               (88.80, "genten_shiharai_col.png"),
               (94.80, "genten_shiharai_row.png")]}

# ── KHỐI CHỮ do FONT vẽ (Veo không viết được tiếng Nhật) ─────────────────────
# ⚖️ YMYL: mọi dòng dưới đây lấy TỪ CHÍNH LỜI ĐỌC của scene đó, không thêm số/chế độ mới.
#    scene 14 dùng nguyên bảng đã khoá trong `_scenes22.py`.
BLOCKS = {
    9:  ["受け取っていい|お金", "返さなければ|ならないお金", "*見分けが|つかない"],
    10: ["日本年金機構|原典", "国税庁|原典", "*画面で|確かめます"],
    14: None,                                     # lấy từ _scenes22
    18: ["相続財産|ではない", "*ご家族の|固有の権利"],
}

# ── fx "hoa lá cành": THƯA, mỗi variant ĐÚNG MỘT LẦN ─────────────────────────
# 🔴 Bài học video 22d2: dùng `sparkle` 3/6 lần nên xem một lúc là thấy đi thấy lại một
#    chùm sao (user: "cách hiệu ứng lặp lại quá nhiều"). Hạt là ĐIỂM NHẤN.
# 🔴 BỎ `arrow` ở cỡ toàn khung — nó render thành vệt cam quét ngang mặt người.
# 🔴 SỬA 2026-09-10 (user: *"hiệu ứng thì ít lặp lại thôi"*): dùng **CẢ 7 variant khả dụng,
#    mỗi cái ĐÚNG MỘT LẦN**, giãn ra ≥2 scene. `arrow` vẫn loại (ở cỡ toàn khung nó render
#    thành vệt cam quét ngang mặt người).
# ⚖️ Không tăng MẬT ĐỘ (5 → 7 trên 19 scene vẫn là thưa) — tăng ĐỘ ĐA DẠNG. Đúng bài học
#    `audience-45plus.md` §2.0h nhưng theo chiều ngược: ở đó lỗi là *giảm lặp bằng cách giảm
#    số lượng*; ở đây phải *giảm lặp bằng cách thêm LOẠI*, giữ nguyên độ thưa.
FX = {
    2:  ("coins",    18, None),          # tiền vào sổ
    6:  ("vignette", 10, "full"),        # 「線はどこに」 — bất an; ăn ở RÌA nên không che ai
    10: ("sparkle",  16, None),          # scene gfx dài nhất (13,1s), nền kem phẳng thì tẻ
    15: ("rays",     14, None),          # 集中線 lên dải thời gian
    17: ("glow",     22, None),          # 「これが未支給年金」 — định nghĩa đáp xuống
    18: ("stampx",    1, "gfxleft"),     # 「相続財産ではない」 — ✗ đúng nghĩa PHỦ ĐỊNH
}
# 🔴 `stampx` đập dấu ✗ vào **GIỮA `area`** ⇒ chỗ đặt phải là vùng THẬT SỰ trống.
#    Bản đầu để nó ở scene 5 (「片方は返金」) với ô góc trên-phải — ghép thử lên chính frame
#    t=31s thì dấu ✗ **đập trúng mặt ông cụ**: scene 5 là trung cảnh HAI NGƯỜI, không có góc
#    nào trống. ⇒ Dời sang **scene 18**, vừa trống thật (scene khối chữ, chữ ở x 606+) vừa
#    đúng nghĩa hơn hẳn: 「相続財産ではない」 là một câu PHỦ ĐỊNH.
#    📌 Bài học: chọn chỗ cho hiệu ứng phải **ghép thử lên frame thật**, đừng suy từ toạ độ ô —
#       ô "góc trên-phải" nghe như chỗ trống, nhưng nội dung từng cảnh mới quyết.
# ⛔ **BỎ `confetti`** dù nó là variant chưa dùng: cửa sổ demo (scene 0–18) là khúc DỰNG VẤN
#    ĐỀ, không có beat tin-vui nào cho nó. Nhét vào là trang trí vô nghĩa — đúng cái luật
#    「cấm bịa để lấp chỗ」 cấm. Dành cho nửa sau bài (scene 19+, 請求できる/受け取れる).
# ⚖️ Màu ✗ = **navy**, KHÔNG đỏ: bài này nói về tiền ĐƯỢC NHẬN nên đỏ lệch hoàn cảnh
#    (CLAUDE.md §② — user chốt *"màu đỏ trong video không hợp hoàn cảnh"*).
FX_COLOR = {"stampx": "#1C2A4A"}
FX_AREA = {"gfxleft": {"x": 6, "y": 26, "w": 24, "h": 30},
           "full":    {"x": 0, "y": 0, "w": 100, "h": 100}}
# ⭐ MASCOT = CÚ (user chốt 2026-09-10, thay ông già). Mới có ĐÚNG MỘT tư thế `idle`
#    nên mọi mốc trỏ cùng một sequence — khi có `nod`/`point` thì thêm vào đây và
#    `mascotPoses` tự xoay như cũ.
# 🔴 Cú RỘNG hơn ông già: PNG 404×460 ⇒ ở `mascotH 300` nó chiếm **x 1642–1905** (ông già
#    chỉ từ 1690). Đã hạ bảng thẻ 原典 xuống `DEST_W 1350` (mép phải 1625) cho khỏi bị đè.
#    Đổi `mascotH` hoặc đổi mascot ⇒ phải tính lại con số đó, đừng để nó trôi.
POSE = ["owl_idle"]
PRESET = ["telop", "telop-gold", "telop"]


def quiet_side(asset: str) -> str:
    """Bên nào của khung ÍT BẬN hơn — ĐO trên frame giữa của chính clip đang chiếu.

    🔴 Bản 22d2 từng chọn bên bằng `n % 2` (số thứ tự scene). Sai: bên trống là thuộc tính
       của TỪNG TẤM HÌNH. Kết quả đo hồi đó: bà cụ nằm nửa PHẢI mà hạt cũng nhốt nửa phải
       nên xu vàng phủ kín mặt.
    """
    p = os.path.join(ASSETS, asset)
    cap = cv2.VideoCapture(p)
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    cap.set(cv2.CAP_PROP_POS_FRAMES, n // 2)
    ok, fr = cap.read()
    cap.release()
    if not ok:
        return "right"
    g = cv2.cvtColor(cv2.resize(fr, (480, 270)), cv2.COLOR_BGR2GRAY)
    e = cv2.Laplacian(g, cv2.CV_64F)
    third = 480 // 3
    left = float(np.abs(e[20:250, 6:third]).sum())
    right = float(np.abs(e[20:250, 480 - third:474]).sum())
    return "left" if left < right else "right"


def enter_of(k: int, n_fam: dict) -> dict:
    """Lối VÀO của khe footage thứ `k` — xoay 3 HỌ, và trong mỗi họ xoay hướng/độ dài.

    🔴 BUG ĐÃ SỬA (bắt 2026-09-10 khi user nói *"hiệu ứng lặp lại"*): bản trước chọn lối vào
       bằng `n % 2 == 1` rồi lấy hướng cuộn bằng `["br","tr","bl","tl"][n % 4]`, với `n` là
       **chỉ số SCENE**. Nhưng chỉ scene có `n` LẺ mới được cuộn ⇒ `n % 4` chỉ nhận `{1, 3}`
       ⇒ **đúng 2 trong 4 hướng được dùng** (đo trên bản render: `tl` 4 lần, `tr` 2 lần, còn
       `br`/`bl` không bao giờ). Và 6 khe kia đều `fade7` y hệt nhau.
       ⇒ Chỉ số phải đếm theo **số lần HỌ ĐÓ đã dùng**, không theo chỉ số của vòng lặp ngoài.
       📌 Bài học chung: `x % N` chỉ phủ hết N giá trị khi `x` chạy LIÊN TỤC. Lọc `x` trước
          rồi mới `% N` là tự bóp dải — lỗi im lặng, chỉ lộ khi đếm bản render.

    Ba họ đều có sẵn trong `Footage.tsx`; `clipPath` chỉ nhận MỘT giá trị nên **curl và wipe
    không dùng chung được** (đã ghi trong component), vì vậy xoay chứ không cộng dồn.
    """
    if k == 0:
        return {}                                   # khe đầu: vào thẳng, không hiệu ứng
    fam = ["fade", "curl", "wipe"][(k - 1) % 3]
    j = n_fam[fam]
    n_fam[fam] += 1
    if fam == "curl":
        return {"curlInFrames": [13, 15, 11, 14][j % 4],
                "curlDir": ["br", "tr", "bl", "tl"][j % 4]}
    if fam == "wipe":
        return {"wipeInFrames": [10, 12, 9, 11][j % 4],
                "wipeDir": ["left", "up", "right", "down"][j % 4]}
    return {"fadeInFrames": [7, 10, 5, 8][j % 4]}   # đổi cả ĐỘ DÀI, không chỉ đổi họ


def split_caption(text: str, maxlen: int = 78):
    """Chẻ khối phụ đề <=78 ký, cắt SAU dấu câu.

    🔴 Remotion KHÔNG chẻ hộ như `video_render.py` (SUB_MAXLEN=42): `CaptionLayer` lấy
       NGUYÊN dòng timeline làm một khối nên dòng 151 ký ra 4 dòng phụ đề che gần hết đáy
       khung, vi phạm `audience-45plus.md` §3 (<=2 dòng/khối).
    """
    if len(text) <= maxlen:
        return [text]
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。、」）" and len(cur) >= maxlen * 0.55:
            out.append(cur)
            cur = ""
        elif len(cur) >= maxlen:
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out


def main() -> int:
    rows = {r["i"]: r for r in build()}
    idxs = [i for i in sorted(rows) if SCENE_LO <= i <= SCENE_HI]
    t0, t1 = rows[idxs[0]]["t0"], rows[idxs[-1]]["t1"]
    total = t1 - t0

    errs = []
    cover = {}
    for (a, b), clip in SHOTS:
        for i in range(a, b + 1):
            cover[i] = ((a, b), clip)

    trk_v, trk_g, trk_blk, trk_fx, trk_t, markers, poses = [], [], [], [], [], [], []
    # đếm riêng cho từng thứ hay lặp — xem `enter_of()` và khối `area` của fx
    n_fam = {"fade": 0, "curl": 0, "wipe": 0}
    n_side = {"left": 0, "right": 0}
    used = []

    for n, i in enumerate(idxs):
        r = rows[i]
        s0, dur = r["t0"] - t0, r["dur"]
        telop = r["telop"]
        markers.append({"id": f"m{i}", "atFrame": f(s0), "label": telop.replace("\n", " ")})
        poses.append({"atSec": s0, "asset": f"assets/{POSE[n % len(POSE)]}/f_%04d.png"})

        slot = cover.get(i)
        is_block = i in BLOCKS
        is_genten = i in GENTEN

        # ── GATE 1: mỗi scene phải có ĐÚNG MỘT thứ ở vùng giữa ───────────────
        if sum([bool(slot), is_block, is_genten]) != 1:
            errs.append(f"scene {i} ({r['kind']}): {sum([bool(slot), is_block, is_genten])} "
                        f"lớp ở vùng giữa (footage={bool(slot)} block={is_block} "
                        f"genten={is_genten})")
            continue

        # 🔴 Scene dùng CHUNG clip với scene trước thì KHÔNG mở khe footage mới, nhưng
        #    VẪN phải có telop riêng — khuôn video 22 là "telop ~100% thời lượng".
        #    Bản đầu `continue` ở đây và mất telop của scene 1 và 12 (17/19), lỗi im lặng:
        #    project vẫn hợp lệ, chỉ hai đoạn bị trống chữ.
        if slot and i == slot[0][0]:
            (a, b), clip = slot
            khe = rows[b]["t1"] - rows[a]["t0"]
            # ── GATE 2: khe dài hơn clip nguồn thì CHẬM lại; cấm làm nhanh ───
            speed = round(min(1.0, SRC_SEC / khe), 4)
            if speed < 0.85:
                errs.append(f"scene {a}-{b}: khe {khe:.1f}s cần speed {speed} < 0,85 "
                            f"nên trông như slow-motion. Cấp thêm clip cho khe này.")
            # cross-dissolve: kéo clip dài thêm FADE frame để nó lọt DƯỚI clip sau.
            # Chỉ kéo khi còn dư nguồn — kéo quá nguồn thì Remotion giữ frame cuối.
            head = SRC_SEC / speed - khe
            ext = FADE if head >= FADE / FPS and b < idxs[-1] else 0
            trk_v.append({
                "id": f"v{a}", "kind": "video", "from": f(s0),
                "durationInFrames": f(khe) + ext,
                "asset": f"assets/{clip}.mp4", "fit": "cover", "motion": "none",
                "speed": speed, "volume": 0, "filter": GRADE,
                **enter_of(len(trk_v), n_fam),
            })
            used.append(clip)

        elif slot:
            pass                                      # khe đã mở ở scene đầu của khối

        elif is_genten:
            # 原典 = ảnh chụp THẬT. Track RIÊNG để không bị tính vào trần 6 đổi-ảnh-chính
            # /phút — nó là một tấm đứng có pan, không phải một cú cắt cảnh
            # (`feedback_gate_va_builder_phai_cung_ten`).
            stages = GENTEN[i]
            for k, (at, asset) in enumerate(stages):
                end = stages[k + 1][0] if k + 1 < len(stages) else r["t1"]
                trk_g.append({
                    "id": f"g{i}_{k}", "kind": "video", "from": f(at - t0),
                    "durationInFrames": f(end - at), "asset": f"assets/{asset}",
                    "fit": "cover", "motion": "none" if k else "pan",
                    "speed": 1.0, "volume": 0,
                    "fadeInFrames": FADE if k == 0 else 0,
                })
            # ── GATE 2b: chuỗi 原典 phải phủ đúng scene, không hở không tràn ──
            if abs(stages[0][0] - r["t0"]) > 0.05:
                errs.append(f"scene {i}: 原典 mở ở {stages[0][0]:.2f}s "
                            f"nhưng scene bắt đầu {r['t0']:.2f}s")
            for k in range(len(stages) - 1):
                if not (r["t0"] <= stages[k][0] < stages[k + 1][0] <= r["t1"]):
                    errs.append(f"scene {i}: mốc 原典 {stages[k][0]:.2f}s không tăng dần "
                                f"hoặc ra ngoài khe [{r['t0']:.2f},{r['t1']:.2f}]")

        else:
            lines = BLOCKS[i] or SCENES[i][3]
            # 🔴 Vùng giữa chở ĐÚNG một thứ: scene có bảng thì KHÔNG có footage
            #    (CLAUDE.md §②: bảng vẽ ở y~240, ảnh chiếm y 150–706 nên ảnh che bảng).
            nl = len(lines)
            fs = {2: 84, 3: 76, 4: 66}.get(nl, 60)
            top = int((250 + 860) / 2 - nl * fs * 1.55 / 2)
            trk_blk.append({
                "id": f"b{i}", "kind": "text", "from": f(s0) + 8,
                "durationInFrames": max(12, f(dur) - 12),
                "content": "\n".join(lines), "preset": "papercut-stat",
                "color": "#1C2A4A", "animation": "none",
                "layout": {"x": 606, "y": top, "w": 1100}, "fontSize": fs,
            })

        # ── telop: khối chữ/原典 đã chiếm giữa khung nên dùng dải trên cho khỏi đè ──
        trk_t.append({
            "id": f"t{i}", "kind": "text", "from": f(s0) + 3,
            "durationInFrames": max(8, f(dur) - 5),
            "content": telop,
            "preset": "telop-band" if (is_block or is_genten) else PRESET[n % 3],
            "color": "#FFD34E", "animation": "pop", "layout": {}, "fontSize": None,
        })

        if i in FX:
            variant, dens, area_kind = FX[i]
            # 🔴 `quiet_side` chỉ có nghĩa khi scene ĐANG chiếu footage. Ở scene khối
            #    chữ/原典 thì `trk_v[-1]` là clip của một scene KHÁC ⇒ đo nó là đo sai
            #    tấm hình. Scene không footage: khối chữ nằm ở x 606+, nên cột TRÁI trống.
            if slot:
                cur = trk_v[-1]["asset"].split("/")[-1]
                side = quiet_side(cur)
            else:
                # scene khối chữ/原典: khối nằm ở x 606+ nên cột TRÁI trống. Xoay trái/phải
                # theo số lần đã dùng để hai scene gfx không đổ hạt vào cùng một chỗ.
                side = "left" if n_side["left"] <= n_side["right"] else "right"
            trk_fx.append({
                "id": f"fx{i}", "kind": "fx", "from": f(s0) + 6,
                "durationInFrames": max(12, f(dur) - 12),
                "variant": variant, "density": dens,
                "color": FX_COLOR.get(variant, "#FFC83A"),
                "seed": 100 + i * 7,
                # 🔴 Góc PHẢI-DƯỚI là chỗ của MASCOT (bottomOffset 250 + cao 300 => y~530–830):
                #    thả hạt kín cột phải là hạt rơi xuyên qua ông già.
                #    Cột phải chỉ dùng NỬA TRÊN; cột trái mới được dùng trọn chiều cao.
                #    `vignette` ăn ở rìa khung nên cho nó full.
                # `area_kind` khai tường minh thì dùng nó; không thì suy từ bên ÍT BẬN.
                # 🔴 Bản trước: 3/5 fx rơi vào ĐÚNG một ô `{66,6,30,40}` (cột phải-trên) vì
                #    `quiet_side` trả "right" cho 3 clip liền ⇒ hạt cứ hiện ở một góc, và
                #    đó là một trong những chỗ user thấy "lặp lại". Nay thêm biến thể ô theo
                #    số lần đã dùng mỗi bên, nên hai lần cùng bên vẫn khác chỗ.
                "area": (FX_AREA[area_kind] if area_kind else
                         ([{"x": 2, "y": 8, "w": 32, "h": 84},
                           {"x": 4, "y": 4, "w": 30, "h": 44},
                           {"x": 6, "y": 40, "w": 28, "h": 48}][n_side["left"] % 3]
                          if side == "left" else
                          [{"x": 66, "y": 6, "w": 30, "h": 40},
                           {"x": 64, "y": 34, "w": 32, "h": 52},
                           {"x": 68, "y": 14, "w": 26, "h": 62}][n_side["right"] % 3])),
                "opacity": 1, "fadeInFrames": 8, "fadeOutFrames": 10, "dir": "upright",
            })
            if not area_kind:
                n_side[side] += 1

    # ── GATE 3b: MỌI scene phải có telop ─────────────────────────────────────
    # Khuôn video 22 là "telop ~100% thời lượng". Bản đầu `continue` ở scene dùng chung
    # clip nên mất telop của scene 1 và 12 — lỗi IM LẶNG, project vẫn hợp lệ.
    if len(trk_t) != len(idxs):
        errs.append(f"chỉ {len(trk_t)}/{len(idxs)} scene có telop — "
                    f"scene thiếu: {sorted(set(idxs) - {int(c['id'][1:]) for c in trk_t})}")

    # ── GATE 3: không dùng lại clip trong cùng video ──────────────────────────
    dup = {c for c in used if used.count(c) > 1}
    if dup:
        errs.append(f"clip dùng lại trong cùng video: {sorted(dup)} "
                    f"(feedback_slide_khong_trung_anh_trong_video)")

    # ── GATE 4: asset phải CÓ THẬT — thiếu thì KHÔNG render (render-background §1.5) ──
    for c in trk_v + trk_g:
        p = os.path.join(ROOT, "public", "projects", NAME, c["asset"])
        if not os.path.exists(p):
            errs.append(f"thiếu asset {c['asset']}")

    # ── phụ đề: cắt đúng cửa sổ demo rồi dời gốc về 0 ─────────────────────────
    lines = json.load(io.open(TL, encoding="utf-8"))["lines"]
    cap = []
    for ln in lines:
        if ln["end"] <= t0 or ln["start"] >= t1:
            continue
        parts = split_caption(ln["text"])
        span = (ln["end"] - ln["start"]) / max(1, sum(len(p) for p in parts))
        t = ln["start"]
        for p in parts:
            d = span * len(p)
            cap.append({"text": p, "startMs": round((t - t0) * 1000),
                        "endMs": round((t + d - t0) * 1000)})
            t += d
    # ── GATE 5: <=2 dòng/khối phụ đề (audience-45plus §3) ────────────────────
    bad = [c for c in cap if len(c["text"]) > 78]
    if bad:
        errs.append(f"{len(bad)} khối phụ đề > 78 ký")

    if errs:
        print("\n🔴 GATE:")
        for e in errs:
            print("  ", e)
        return 1

    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": None,
                 "fps": FPS, "width": W, "height": H, "createdAt": "", "modifiedAt": ""},
        "timeline": {"durationInFrames": f(total)},
        "sceneMarkers": markers,
        "tracks": [
            {"id": "trk-video", "name": "footage i2v", "type": "video", "clips": trk_v},
            {"id": "trk-genten", "name": "genten", "type": "video", "clips": trk_g},
            {"id": "trk-fx", "name": "hoa la canh", "type": "fx", "clips": trk_fx},
            {"id": "trk-stat", "name": "khoi chu font", "type": "text", "clips": trk_blk},
            {"id": "trk-telop", "name": "telop", "type": "text", "clips": trk_t},
            {"id": "trk-audio", "name": "voice", "type": "audio", "clips": [
                {"id": "a0", "kind": "audio", "from": 0, "durationInFrames": f(total),
                 "asset": "assets/voice.wav", "volume": 1, "trimStartFrames": f(t0)}]},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44, "lines": cap, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236", "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F3EAD8"},
        "brand": {
            "logo": "assets/brand_logo.png", "mascot": None, "mascotPoses": poses,
            "mascotVideo": poses[0]["asset"], "mascotVideoFrames": MASCOT_FRAMES,
            "mascotH": 300, "logoH": 110, "subscribe": True,
            # ⭐ MASCOT hạ xuống (user chốt 2026-09-10 *"hình con cú thấp xuống tí nữa"*).
            #    Con số ĐO trên bản render, không đoán:
            #      phụ đề (2 dòng, mức tối đa)   : y 908–1013 · và rộng tới **x 1765**
            #      cú ở offset 250 (bản trước)    : y 530–830
            #      cú cao 300px + `bob` ±6px      ⇒ đáy tối đa = 908 − 8 lề − 6 bob = 894
            #    ⇒ **186**: cú xuống y 594–894, hạ **64px**, chừa 14px trước phụ đề.
            # 🔴 KHÔNG hạ tiếp: phụ đề rộng tới x 1765 nên nó CHỒNG cột của cú (1642–1905)
            #    theo chiều ngang ⇒ cú lấn vào dải phụ đề là che chữ, thứ tệp 45+ cần nhất
            #    (`audience-45plus.md` §3). Trần dưới nữa là timestamp YouTube (y 1045+).
            "bottomOffset": 186,
            # ⭐ SUBSCRIBE hạ xuống (user chốt 2026-09-10) — lề đáy RIÊNG, xem
            #    `BrandSchema.subscribeBottom`. Con số ĐO trên bản render, không đoán:
            #      dải phụ đề 2 dòng (mức cao nhất)  : y 908–1013
            #      nút ở offset 250 (bản trước)      : y 783–830
            #      con trỏ chuột nằm 18px DƯỚI nút, và nở ×1,12 lúc "bấm" ⇒ +20px
            #    ⇒ đáy con trỏ = 1080 − offset + 20. Muốn đáy ≤ 900 (chừa 8px trước phụ đề)
            #      thì offset ≥ 200. Chọn **200**: nút xuống y 833–880, hạ 50px so với trước.
            # 🔴 Đừng hạ tiếp: 908 là mép trên của phụ đề HAI dòng — mức tối đa luật cho phép
            #    (`audience-45plus.md` §3), nên không có biên nào để ăn thêm.
            "subscribeBottom": 200,
        },
    }
    out = os.path.join(ROOT, "projects", NAME, "project.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(json.dumps(proj, ensure_ascii=False, indent=1))

    print(f"\n✅ {out}")
    print(f"   scene {idxs[0]}–{idxs[-1]} của video thật · t {t0:.1f}->{t1:.1f}s "
          f"= {total:.1f}s ({total/60:.2f}′) @ {FPS}fps")
    print(f"   footage {len(trk_v)} khe · genten {len(trk_g)} · khối chữ font {len(trk_blk)} "
          f"· fx {len(trk_fx)} · telop {len(trk_t)} · phụ đề {len(cap)} khối")
    print(f"   nhịp đổi ảnh chính: {len(trk_v)/(total/60):.1f}/phút (trần 6) "
          f"— genten tính riêng track")
    slow = [(c["id"], c["speed"]) for c in trk_v if c["speed"] < 1]
    print(f"   khe phải làm chậm: {slow if slow else 'không'}")
    print(f"   clip dùng: {len(set(used))} khác nhau, không lặp")
    print("   ⚠️ 3 scene gfx (9·10·18) tạm dùng khối `papercut-stat`, lời lấy verbatim "
          "từ narration — bản dựng thật cần component SƠ ĐỒ (INFOG/GAUGE)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
