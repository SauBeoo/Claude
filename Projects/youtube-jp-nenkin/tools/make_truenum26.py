# -*- coding: utf-8 -*-
r"""make_truenum26.py — bang SO THAT cua video 26, lay tu CHINH loi doc.

🔴 VI SAO CO FILE NAY: `beats26.py` doc `_TRUENUM` de dan cum 「a big numeral X」 vao canh
   chua co so. Ban dau no van tro sang **`_truenum25.json`** (bang so cua VIDEO 25:
   33.000 · 70.608 · 847.300 · 480 · 420 · 48…) vi phep doi ten hang loat khong cham toi
   ten file do => 26 prompt mang so cua bai KHAC ma khong mot canh bao nao.
   Day la lan thu MUOI cua benh "artifact video cu khoa theo chi so scene".

⚖️ YMYL: chi nhan so di kem 円 hoac か月 (mốc lịch 月/年/歳 KHONG tinh — cung luat voi
   `check_pace.py`). So lay tu dung nhung dong timeline ma scene do phu.

CHAY:  python tools/make_truenum26.py   ->  tools/_truenum26.json
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scenes26 import SCENES  # noqa: E402

TL = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\26_kaigo-hokenryo-dankai-setai\timeline.json")

DIG = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
       "六": 6, "七": 7, "八": 8, "九": 9}
SML = {"十": 10, "百": 100, "千": 1000}
BIG = {"万": 10**4, "億": 10**8}
NUM_RE = re.compile(r"[〇零一二三四五六七八九十百千万億]+(?=円|か月)")


def kan2int(s: str):
    """Doi so kanji -> int. Tra None neu khong doc duoc."""
    total, section, cur = 0, 0, 0
    for ch in s:
        if ch in DIG:
            cur = DIG[ch]
        elif ch in SML:
            section += (cur or 1) * SML[ch]
            cur = 0
        elif ch in BIG:
            total += (section + cur) * BIG[ch]
            section = cur = 0
        else:
            return None
    return total + section + cur


# 🔴 SỔ ĐEN — scene mà số ĐÃ ĐO là AI vẽ hỏng ⇒ bỏ khỏi bảng, để telop/font của Remotion
#    tải con số đó (`feedback_so_tren_hinh_phai_do_font_ve`). Bỏ ở ĐÂY chứ không sửa tay
#    `_scenes26.py`, vì `_enrich` đọc bảng này và sẽ TỰ DÁN SỐ LẠI nếu body không còn chữ
#    "numeral" — đã dính đúng thế: gỡ số khỏi body scene 38 xong prompt vẫn ra 10,000.
SKIP = {
    # vòng 1 (10 clip LOT1, 2026-09-16): clip_38a trả về 「10,00」 — rớt một chữ số, ở 3/4
    # frame, dù prompt đã đánh vần + đếm chữ số. Telop 「一万円{下}」 đã tải nghĩa này.
    "38",
    # 🔴 lô 61 clip (2026-09-16): clip_0a trả về 「1,46000」 — vừa sai chữ số vừa sai chỗ
    #    dấu phẩy, mà đây là ENTRY 0, khung hình đầu tiên của một video YMYL về tiền.
    #    User chốt đường (b): bỏ số khỏi ẢNH, telop 「どちらも{147万}」 tải nghĩa.
    #    ⚠️ Phải chặn Ở ĐÂY: gỡ số khỏi body mà quên sổ đen thì `_enrich` DÁN LẠI —
    #    đã dính đúng thế ở scene 38 (prompt vẫn ra 10,000 sau khi đã gỡ khỏi body).
    "0",
    # 🔴 cùng lô: clip_35a ra 「7」 VÀ 「71」 (hai bản, guard "appears ONCE only" thua) ·
    #    clip_36a ra 「4,0」 (tự thêm dấu phẩy vào số 2 chữ số). Cả hai là số TRANG TRÍ
    #    (tuổi 71 · 勤続40年), không phải số tiền của bài — lời đọc đã tải. Bỏ khỏi ảnh.
    #    ⇒ Khe CÓ SỐ còn 4/61: chỉ giữ số ĐÃ SOI LÀ ĐÚNG (1,470,000 · 37,900 ×2 · 3).
    "35", "36",
}


def main():
    tl = json.load(io.open(TL, encoding="utf-8"))["lines"]
    out = {}
    for k, (ln, kind, _telop, _body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        txt = "".join(r["text"] for r in tl[ln:nxt])
        vals = []
        for m in NUM_RE.finditer(txt):
            v = kan2int(m.group())
            # ⚖️ bo so qua nho (mot chu so) va so khong doc duoc
            if v and v >= 100 and v not in vals:
                vals.append(v)
        if vals and str(k) not in SKIP:
            out[str(k)] = vals
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_truenum26.json")
    json.dump(out, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✓ {len(out)} scene co so that -> {p}")
    for k, v in out.items():
        print(f"   scene {k:>3}: {v}")


if __name__ == "__main__":
    main()
