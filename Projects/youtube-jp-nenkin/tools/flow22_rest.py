# -*- coding: utf-8 -*-
"""
flow22_rest.py — lọc `flow22_FULL_FLOW.txt` xuống ĐÚNG phần còn thiếu để render FULL.

Bối cảnh (2026-09-10): demo đã dựng xong scene 0–18 bằng 12 clip i2v. Muốn render cả
828,4s thì còn thiếu clip cho **scene 19–90**. Bộ `flow22_FULL_FLOW.txt` có đủ 62 prompt
khớp 1-1 với 62 khe, nhưng bơm cả 62 là **gen lại cả phần đã có** ⇒ lọc theo scene.

🔴 VÌ SAO KHÔNG DÙNG 25 CLIP i2v CÒN DƯ CHO PHẦN NÀY: đối chiếu nội dung thì chúng là beat
   của NỬA ĐẦU câu chuyện (phòng khách · 通帳 · lịch tường · quầy 年金事務所 · giấy tờ + kính).
   Scene 19–90 là 中村さん case · 死亡届 · 請求手続き · マイナンバー · 期限 · 税金, với khuôn
   **SCREEN (18 khe) · CROWD · PANEL · VIZ** và hầu hết đòi **có NGƯỜI trong khung** — còn
   sb_22/23/24 là màn hình chụp từ trên xuống KHÔNG có người. Thay vào là lệch lời, đúng cái
   `_MAP_I2V.md` §7 đã cảnh báo.
   ⇒ Lô i2v dư giữ lại làm dự phòng, đừng nhét cho đủ số.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
FROM_SCENE = 19


def main() -> int:
    flow = io.open(os.path.join(VD, "flow22_FULL_FLOW.txt"), encoding="utf-8").read().splitlines()
    ten = io.open(os.path.join(VD, "flow22_FULL_TENFILE.txt"), encoding="utf-8").read().splitlines()
    if len(flow) != len(ten):
        print(f"🔴 FLOW {len(flow)} dòng nhưng TENFILE {len(ten)} dòng — hai file lệch nhau")
        return 1

    keep = []
    for i, (pr, tn) in enumerate(zip(flow, ten), 1):
        m = re.search(r"\[scene\s+(\d+)", tn)
        if not m:
            print(f"🔴 dòng {i} của TENFILE không có 'scene N': {tn[:60]}")
            return 1
        if int(m.group(1)) >= FROM_SCENE:
            keep.append((pr, tn))

    fp = os.path.join(VD, "flow22_REST_FLOW.txt")
    tp = os.path.join(VD, "flow22_REST_TENFILE.txt")
    io.open(fp, "w", encoding="utf-8").write("\n".join(p for p, _ in keep) + "\n")
    with io.open(tp, "w", encoding="utf-8") as fh:
        fh.write(f"# phan CON THIEU de render FULL — scene >= {FROM_SCENE}\n")
        fh.write(f"# scene 0-{FROM_SCENE-1} da co clip i2v, DUNG gen lai\n")
        for j, (_, tn) in enumerate(keep, 1):
            fh.write(re.sub(r"^dong\s+\d+", f"dong {j:>2}", tn) + "\n")

    print(f"✅ {fp}  ({len(keep)} prompt)")
    print(f"✅ {tp}")
    print(f"   bỏ {len(flow) - len(keep)} prompt của scene 0–{FROM_SCENE-1} (đã có clip i2v)")
    ln = [len(p) for p, _ in keep]
    print(f"   dài prompt: {min(ln)}–{max(ln)} ký")
    return 0


if __name__ == "__main__":
    sys.exit(main())
