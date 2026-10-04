# -*- coding: utf-8 -*-
"""
ingest_i2v_22.py — nhận lô clip i2v (Google Flow / Veo) của video 22 vào project Remotion.

Ba việc, đúng thứ tự:
  ① ĐỔI TÊN theo shot — tên Flow đặt là caption tiếng Anh, không mang shot-id. Bảng
     `CLIPS` dưới đây là bản ĐÃ SOI MẮT từng cặp (frame clip ↔ ảnh start-frame), không
     phải kết quả fuzzy-match. Cách dựng bảng: gán 1-1 toàn cục (hình + chữ) rồi duyệt
     sheet cặp 1:1 — chi tiết ở `_MAP_I2V.md`.
  ② XOÁ WATERMARK ✦ bằng CẮT KHUNG (`media-library.md` §2.10 ⑤b: slide thì CẮT, chỉ
     thumbnail mới phải vá vì chữ hero chạy sát mép).
     🔴 Vị trí ✦ KHÔNG cố định giữa các clip — đo bằng mắt trên lưới toạ độ, 11 clip thấy
        rõ: x 1130–1225 · y 578–680 (clip 26 thấp hơn clip 03 tới 45px).
        ⇒ delogo một hộp cố định KHÔNG đủ (đã thử: sạch ở clip 3/32/36, còn đuôi ở 26).
     ⇒ Cắt `1120×630` (đúng 16:9, không méo): riêng cú cắt NGANG đã loại sạch vì mọi ✦
        đều có x ≥ 1130. Cắt dọc chỉ để giữ 16:9, và canh GIỮA (y=45) cho khỏi mất chân
        khung. Giá: mất 12,5% khung + upscale 1,71× (nguồn Flow chỉ 720p).
  ③ SCALE 1920×1080 @24fps, bỏ audio. 🔴 GIỮ 24fps — clip Veo là 24fps, ép 30 thì 27%
     frame lặp ⇒ judder (`feedback_fps_clip_phai_khop_renderer`).
"""
import glob
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DL = r"C:\Users\tuana\Downloads\Sep 09 - 22_34 (5)"
OUT = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-22i2v\assets"

# ── hộp cắt: đo bằng mắt trên lưới, xem docstring ②
CW, CH, CX, CY = 1120, 630, 0, 45

# caption Flow (không dấu thời gian) → shot id. ĐÃ SOI MẮT từng cặp.
CLIPS = {
    "Hands_lifting_passbook":            "sb_03",
    "Light_moving_across_paper":         "sb_06",
    "Light_moving_across_desk_pages":    "sb_13",
    "Thumb_presses_paper_flat":          "sb_05",
    "Woman_taps_screen_and_looks":       "sb_08",
    "Question_mark_drifts_over_text":    "sb_14",
    "Katsuo_and_Mitsue_shaking_head":    "sb_09",
    "Mitsue_using_phone_by_window":      "sb_37",
    "Clerk_folding_hands_on_counter":    "sb_19",
    "Arrows_slide_along_timeline_dates": "sb_25",
    "Woman_looks_at_calendar_page":      "sb_10",
    "Clerk_pushes_form_forward":         "sb_20",
    # ── ngoài cửa sổ demo, nhận luôn để bản dựng thật dùng lại ────────────────
    "Man_looking_at_passbook":           "sb_01",
    "Man_staring_intently_at_text":      "sb_02",
    "Hands_placing_passbook_on_table":   "sb_07",
    "Hand_lifting_calendar_page":        "sb_11",
    "Finger_selects_date_on_calendar":   "sb_12",
    "Man_holding_calculator_on_mats":    "sb_16",
    "Man_turns_head_toward_window":      "sb_17",
    "Man_sitting_inside_room":           "sb_18",
    "Fingertip_tapping_and_tracing_box": "sb_21",
    "Monitor_band_brightens_and_dims":   "sb_22",
    "Cursor_slides_onto_link":           "sb_23",
    "Table_rows_brighten_on_screen":     "sb_24",
    "Glowing_date_and_drifting_arrows":  "sb_26",
    "Man_tapping_pen_on_paper":          "sb_28",
    "Pen_writes_on_paper":               "sb_29",
    "Woman_nods_and_looks_up":           "sb_30",
    "Figure_crosses_behind_chair":       "sb_33",
    "Shadow_stretches_across_floor":     "sb_32",
    "Light_moving_across_documents":     "sb_34",
    "Reading_glasses_lowering_toward":   "sb_35",
    "Glasses_settle_onto_certificate":   "sb_36",
    "Clerk_slides_brochure_across_cou":  "sb_46",
    "Finger_pressing_printed_paper":     "sb_47",
    "Hands_tightening_on_passbook":      "sb_04",
    "Katsuo_sliding_sheet_to_Mitsue":    "sb_28b",   # ⚠ trùng nội dung sb_28, xem _MAP_I2V.md
}


def caption(path: str) -> str:
    """Bỏ dấu thời gian + hậu tố '_2' + ký tự '…' của Flow."""
    s = os.path.splitext(os.path.basename(path))[0]
    s = re.sub(r"_\d{14}(_\d+)?$", "", s)
    return s.replace("\u2026", "").rstrip("_")


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    mp4s = sorted(glob.glob(os.path.join(DL, "*.mp4")))
    if not mp4s:
        print(f"🔴 không thấy mp4 nào trong {DL}")
        return 1

    done, miss, rows = 0, [], []
    for p in mp4s:
        cap = caption(p)
        sid = CLIPS.get(cap)
        if not sid:
            miss.append(cap)
            continue
        dst = os.path.join(OUT, sid + ".mp4")
        # resume ĐÚNG: so mtime, không chỉ hỏi "đã có chưa" (render-background §2.5)
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(p):
            rows.append((sid, cap, "bỏ qua (đã mới)"))
            continue
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", p,
             "-vf", f"crop={CW}:{CH}:{CX}:{CY},scale=1920:1080:flags=lanczos",
             "-r", "24", "-an", "-c:v", "libx264", "-preset", "medium",
             "-crf", "18", "-pix_fmt", "yuv420p", dst], check=True)
        done += 1
        rows.append((sid, cap, "dựng lại"))

    for sid, cap, what in sorted(rows):
        print(f"  {sid:<7} ← {cap[:44]:<46} {what}")
    print(f"\n✅ {len(rows)} clip vào {OUT}  ({done} dựng mới)")
    print(f"   cắt {CW}×{CH}+{CX},{CY} → 1920×1080 @24fps, bỏ audio")
    if miss:
        print(f"\n🔴 {len(miss)} clip KHÔNG có trong bảng CLIPS — thêm vào rồi chạy lại:")
        for m in miss:
            print("  ", m)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
