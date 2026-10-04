# -*- coding: utf-8 -*-
r"""redo25_5.py — gen LẠI 5 clip của video 25 bị hỏng ở vòng "MISSING9" (2026-09-15).

SOI 9 CLIP `F:\Youtube\Dự_án_mới_2_ss833w5b` ở 4 mốc, 1:1 — kết quả:

  ✅ NHẬN  clip_9a · clip_26a · clip_32a · clip_58a
     (26a còn vạch thước 50/31/… và 58a còn nhãn trục 06/5/36 — nhỏ, không phải số tiền,
      không đọc ra mệnh đề nào; nhận có chủ ý, ghi ra đây để sau không tưởng là bỏ sót)

  ❌ GEN LẠI 5 cái dưới đây:
     clip_16a  số ra 「44.900」 — MẤT chữ số đầu (bà đứng che) + dấu phân cách là DẤU CHẤM
     clip_22a  「1人」 + 「Pass Pass」 trên sổ + một BÀN TAY NGƯỜI THẬT thò vào khung giấy
     clip_30a  「75」 đỏ to góc trên-phải + nhiệt kế có vạch 10/20/0
     clip_36a  「130,000」 ba số 0 méo và ĐỔI HÌNH giữa các frame (frame 1 đọc ra 120,000)
     clip_87a  hai tấm thẻ trên bàn mang số 「7」 và 「2」

BA NGUYÊN NHÂN ĐÃ VÁ Ở `beats25.py` (không vá ở đây — vá ở đây là vá triệu chứng):
  ① `_enrich` dán vật MANG THANG SỐ (nhiệt kế · lưới lịch · cột xu · vạch đếm) vào cả cảnh
     "CẤM SỐ". 4/6 ca hỏng đều là cảnh được dán một trong bốn vật đó ⇒ tách kho, và BỎ HẲN
     nhiệt kế + lưới lịch.
  ② Guard số nằm ở ~55% độ dài prompt ⇒ model bám tả cảnh, nuốt chỉ thị. Cùng cơ chế đã đo ở
     thumbnail (`ab-3title-3thumb.md` §3.1 Bước 3) ⇒ hoist lên ngay sau câu khai mở.
  ③ "the hand cut-out" = framing KHÔNG CÓ THÂN ⇒ ra tay người thật
     (`feedback_ai_video_hong_thao_tac_tay`).

CHẠY:  python tools/redo25_5.py      → 06_VIDEO/25_.../vox25_REDO3.txt (+ _TENFILE)
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from beats25 import OUT, VD, merge_prompt          # noqa: E402

# ── VÒNG 2 (2026-09-15 khuya) — soi 5 clip gen lại ở 4 mốc ────────────────────
#   ✅ clip_16a  844,900 ĐÚNG, có dấu phẩy, không bị che, đứng yên cả 4 frame
#   ✅ clip_22a  hết bàn tay người thật; còn vạch trục 15/70/30 li ti — nhận, cùng mức 26a/58a
#   ❌ clip_30a  nền hoá TƯỜNG BÁO đầy chữ Nhật giả + biển hiệu 「曲業グッド会」 to giữa khung
#   ❌ clip_36a  ra 「13,000」 — RỚT một số 0 (lần hỏng thứ hai của đúng con số này)
#   ❌ clip_87a  nền cũng hoá trang báo, chữ giả đọc được chạy kín phía sau
REDO = ["30a", "36a", "87a"]
WHY = {"16a": "so ra 44.900 — mat chu so dau + dau cham",
       "22a": "1人 + Pass + ban tay nguoi that",
       "30a": "nen hoa tuong bao + bien hieu chu Nhat gia",
       "36a": "ra 13,000 — rot mot so 0 (hong lan 2)",
       "87a": "nen hoa trang bao, chu gia doc duoc"}
if len(sys.argv) > 1:
    REDO = sys.argv[1].split(",")


def main() -> int:
    doc = json.load(io.open(os.path.join(OUT, "beats.json"), encoding="utf-8"))
    shots = {f"{b['id']}{s['id']}": (b, s) for b in doc["beats"] for s in b["shots"]}
    miss = [k for k in REDO if k not in shots]
    if miss:
        print(f"🔴 khong thay shot: {miss}")
        return 1

    rows, names = [], []
    for k in REDO:
        b, s = shots[k]
        p = " ".join(merge_prompt(b, s).split())
        rows.append(p)
        names.append(f"clip_{k}.mp4   {b['title_cn']}   | {WHY[k]}")

    io.open(os.path.join(VD, "vox25_REDO3.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(rows) + "\n")
    io.open(os.path.join(VD, "vox25_REDO3_TENFILE.txt"), "w", encoding="utf-8",
            newline="\n").write("\n".join(
                f"dong {i+1} -> {n}" for i, n in enumerate(names)) + "\n")

    # ── GATE tại chỗ: guard phải đứng ĐẦU, và nhánh CẤM SỐ không được còn câu xin số ──
    bad = 0
    for k, p in zip(REDO, rows):
        head = p[: len(p) // 7]                       # ~15% đầu
        pos = p.find("FIGURE") if "EXACTLY ONE FIGURE" in p else p.find("NO FIGURES")
        pct = pos * 100 // len(p)
        numscene = "EXACTLY ONE FIGURE IS ALLOWED" in p
        ok_pos = pct <= 15
        ok_mix = numscene or ("NUMERALS ARE WANTED" not in p
                              and "apart from those cut-out numerals" not in p)
        # 🔴 QUÉT TRONG **MÔ TẢ CẢNH**, KHÔNG QUÉT CẢ PROMPT — bản đầu bắt được 3/5 và
        #    CẢ BA đều là chính câu CẤM của mình ("no tally marks…"). Đúng bẫy đã ghi:
        #    gate đọc lại văn của chính mình rồi báo đỏ. Lần thứ hai trong dự án này.
        _sc = p.split("SCENE (as layered paper cut-outs):")
        sc = _sc[1].split("Any person shown")[0] if len(_sc) > 1 else ""
        ok_obj = numscene or not any(w in sc for w in ("thermometer", "wall calendar",
                                                       "tally marks", "height chart"))
        ok_hand = "the hand cut-out keeps working" not in p
        flag = "✅" if (ok_pos and ok_mix and ok_obj and ok_hand) else "🔴"
        if flag == "🔴":
            bad += 1
        print(f" {flag} clip_{k:<4} {len(p):>4} ky · guard @ {pct:>2}% · "
              f"{'CO SO' if numscene else 'CAM SO'}"
              f"{'' if ok_obj else ' · CON VAT MANG THANG SO'}"
              f"{'' if ok_hand else ' · CON hand cut-out'}"
              f"{'' if ok_mix else ' · CON cau xin so'}")
    # f-string chua duong dan Windows = bay escape control (render-background §2.6 ⑥)
    print(chr(10) + "📁 " + os.path.join(VD, "vox25_REDO3.txt") + f"   ({len(rows)} prompt)")
    print("   " + os.path.join(VD, "vox25_REDO3_TENFILE.txt"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
