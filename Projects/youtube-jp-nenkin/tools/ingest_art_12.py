# -*- coding: utf-8 -*-
r"""ingest_art_12.py — nhận 8 ảnh AI của video 12 từ Downloads: đổi tên + CẮT watermark ✦.

    python tools\ingest_art_12.py
    python tools\ingest_art_12.py --restore     # trả lại bản gốc chưa cắt

VÌ SAO CẮT, KHÔNG VÁ (`.claude/rules/media-library.md` §2.10 ⑤ + ⑤b):
ảnh SLIDE thì cắt mép phải là sạch tuyệt đối, không artifact. Chỉ THUMBNAIL mới phải vá,
vì chữ hero chạy tới ~0,97W nên cắt là mất chữ. Ở đây không ảnh nào có chữ.

🔴 ĐO CỦA ĐÚNG LÔ NÀY (1376×768, tải 2026-08-14) — đừng bê số của lô khác:
  · ✦ có ở **8/8** ảnh, **CHỈ** ở góc dưới-phải. Ba góc còn lại đã soi 1:1: sạch.
  · Nhân ✦ nằm quanh **x 1265..1312 · y 655..700** (≈0,936W · 0,876H).
  · ⚠️ Ảnh `Service_counter` (nền XÁM, không phải kem) có ✦ **to hơn và có TIA DÀI**:
    x **1214**..1327 · y 622..740. Đây là ảnh quyết định mốc cắt, không phải 7 ảnh kia.
  ⇒ cắt phải tại **x = 1204 = 0,875W** (chừa 10px lề dưới mép trái tia của ✦).

🔴 MÁY ĐO ✦ THẤT BẠI 7/8 Ở LÔ NÀY — bằng chứng cho luật đã ghi:
quét "sáng hơn trung vị HÀNG > 14" chỉ bắt được **1/8** ảnh (đúng cái nền xám); 7 ảnh nền kem
trả về KHÔNG ĐO ĐƯỢC vì ✦ quá nhạt trên kem. ⇒ Vị trí phải chốt bằng **MẮT** trên ảnh crop
1:1 của góc, rồi ghi thành hằng số theo lô — đúng như `media-library.md` §2.10 ⑤b mục 5.

HỆ QUẢ TỈ LỆ (biết trước, không phải bỏ sót): 1204×768 = **1.568**, còn hộp ảnh của
`make_stage` là 1.607 (`img`) và 1.626 (`bgimg`) ⇒ cover-crop sẽ trim **~2,5% / ~3,6% CHIỀU
CAO** thay vì cắt mép phải. Vô hại: mọi chủ thể của lô này nằm trong 85% bên trái và không
chạm mép trên/dưới.
"""
import argparse
import io
import shutil
import sys
from pathlib import Path

from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "12_juminzei-koujo-shinkokusho-10gatsu"
DL = Path(r"C:/Users/tuana/Downloads/download")
ART = PROJ / "06_VIDEO" / STEM / "art"
BAK = ART / "_wm_orig"

CUT_X = 1204        # cắt phải tại đây (khung 1376) — xem đo ở docstring
SRC_W, SRC_H = 1376, 768

# (tiền tố tên file trong Downloads, tên file đích trong art/)
MAP = [
    ("Two_sealed_envelopes_on_table", "art_fuutou_futatsu.png"),
    ("Open_drawer_with_envelope_and", "art_hikidashi.png"),
    ("Paper_form_with_pen_on", "art_shinkokusho_fuyou.png"),
    ("Hand_resting_on_empty_notice", "art_tsuuchisho_ran.png"),
    ("Envelope_propped_against_ceramic", "art_shokutaku_fuutou.png"),
    ("Notebook_and_calendar_on_desk", "art_techo_calendar.png"),
    ("Japanese_room_illustration", "bg_daidokoro.png"),
    ("Service_counter_in_public_office", "bg_shiyakusho_akari.png"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--restore", action="store_true")
    a = ap.parse_args()
    ART.mkdir(parents=True, exist_ok=True)

    if a.restore:
        n = 0
        for _, dst in MAP:
            b = BAK / dst
            if b.exists():
                shutil.copy2(b, ART / dst)
                n += 1
        print(f"↩ trả lại {n} ảnh gốc (chưa cắt) từ {BAK}")
        return

    BAK.mkdir(parents=True, exist_ok=True)
    for pre, dst in MAP:
        hits = sorted(DL.glob(pre + "*"))
        if not hits:
            print(f"🔴 KHÔNG THẤY ảnh nguồn cho {dst}  (tiền tố {pre!r})")
            sys.exit(1)
        if len(hits) > 1:
            print(f"⚠️ {len(hits)} file khớp {pre!r} — lấy file MỚI NHẤT")
            hits.sort(key=lambda p: p.stat().st_mtime)
        src = hits[-1]
        im = Image.open(src).convert("RGB")
        if im.size != (SRC_W, SRC_H):
            # 🔴 Lô khác cỡ ⇒ toạ độ ✦ khác ⇒ mốc cắt ở trên KHÔNG còn đúng. Dừng, đo lại.
            print(f"🔴 {src.name} là {im.size}, không phải {SRC_W}×{SRC_H} — "
                  f"ĐO LẠI vị trí ✦ cho lô này trước khi cắt")
            sys.exit(1)
        # backup bản gốc CHƯA cắt (giữ đúng tên đích để --restore hoạt động)
        if not (BAK / dst).exists():
            im.save(BAK / dst)
        out = im.crop((0, 0, CUT_X, SRC_H))
        out.save(ART / dst)
        print(f"✅ {dst:30s} ← {src.name[:42]:42s}  {im.size} → {out.size}")

    print(f"\n→ đã cắt {len(MAP)} ảnh tại x={CUT_X} ({CUT_X/SRC_W:.3f}W), bản gốc ở {BAK.name}/")
    print("→ NGHIỆM THU: soi 1:1 góc dưới-phải bản ĐÃ CẮT (sheet _art_corner_after.png)")


if __name__ == "__main__":
    main()
