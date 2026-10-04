# -*- coding: utf-8 -*-
"""
still22_prompts.py — prompt gen ẢNH TĨNH "ông già giơ giấy có chữ" cho video 22.

Quy trình user chốt 2026-09-07: **gen ẢNH TĨNH (chữ sắc) -> hoạt hoá thành clip**
(`Projects/_media_library/animate_still.py`), đúng cách bản mẫu ngách làm.
⛔ KHÔNG đưa ảnh này vào tool gen video làm reference: ảnh là *reference* chứ không
   phải *frame đầu*, model sẽ VẼ LẠI tờ giấy và chữ nát — mất đúng thứ ta vừa mua được.

CHỮ TRONG ẢNH — 4 luật đã đo (`ab-3title-3thumb.md` §3.1, `media-library.md` §2.9):
 ① Khối TEXT phải nằm trong **15% ĐẦU** prompt. Đặt cuối thì model bám tả cảnh và nuốt chữ
    (đã dính ở chouhen 21; 2 bản bake chữ Nhật thành công đều để TEXT ở đầu).
 ② Trần **4 dòng chữ**. 5 dòng gần như chắc méo kanji.
 ③ Mỗi dòng chữ nằm trên MỘT DÒNG RIÊNG dạng `line 1, black: 自動振込ではない` — nhồi hết
    vào một câu chạy dài thì model nuốt chữ.
 ④ Câu chốt `Text must be perfectly formed Japanese characters, crisp and legible`.
🔴 Soi TỪNG KÝ TỰ trước khi dùng. Kanji rậm (還暦・封筒・請求) là chỗ hay méo nhất; sai một
   nét là loại và gen lại, đừng "để tạm rồi sửa sau".

⚠️ Ảnh mẫu user gửi có chữ NHỎ trong bảng đã nát sẵn — mẫu chấp nhận vì mắt không đọc tới đó.
   Ta cũng chấp nhận, nhưng **chỉ ở chữ nhỏ**; dòng TO và các ô sơ đồ thì phải sạch.
"""
import io, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"

CAST = ("an elderly Japanese man in his late sixties with white hair, round glasses and a "
        "patterned knit cardigan")
CAST_W = ("an elderly Japanese woman in her late sixties with grey hair, round glasses and a "
          "soft green cardigan")

# Bố cục cố định của khuôn: giấy chiếm 2/3 TRÁI, mặt người ở 1/3 PHẢI, ngón tay chỉ vào giấy.
# 🔴 Ép cỡ bằng quan hệ với MÉP KHUNG, đừng tả phần trăm — model nghe VỊ TRÍ, không nghe TỈ LỆ
#    (`media-library.md` §2.10 ⑥).
LAYOUT = ("LAYOUT: {who} holds a large sheet of paper up toward the camera in his left hand and "
          "points at it with his right index finger. The paper is tilted slightly and fills the "
          "left two thirds of the picture, its top edge almost touching the top of the frame and "
          "its bottom edge cropped by the bottom of the frame. His face is in the right third, "
          "large and close to the camera, with a shocked open-mouthed expression, slightly out of "
          "focus behind the paper")

SCENE = ("BACKGROUND: a bright Japanese living room, white walls, warm morning sunlight from a "
         "window, a green houseplant behind his shoulder, soft and out of focus")

QUAL = ("photorealistic photograph, sharp focus on the paper, shallow depth of field, natural "
        "skin texture, warm natural colours. Text must be perfectly formed Japanese characters, "
        "crisp and legible. No watermark, no logo, no signature. Keep the bottom-right corner "
        "free of text.")

# ── 8 thẻ giấy: mỗi thẻ = 1 dòng tiêu đề TO + (tuỳ) sơ đồ 2 ô ────────────────
# ⚖️ YMYL: mọi chữ ở đây đều là mệnh đề CÓ TRONG SCRIPT, không bịa chế độ/số mới.
CARDS = [
 ("s22_01_futatsu", CAST,
  [("line 1, large bold black, across the top", "同じ36万円")],
  None),
 ("s22_02_kichou", CAST_W,
  [("line 1, large bold black, across the top", "通帳では同じ")],
  None),
 ("s22_03_katahou", CAST,
  [("line 1, large bold black, across the top", "片方は返金")],
  ("受け取れる", "返金する")),
 ("s22_04_shibou", CAST,
  [("line 1, large bold black, across the top", "死亡日で決まる")],
  None),
 ("s22_05_mishikyu", CAST,
  [("line 1, large bold black, across the top", "未支給年金")],
  ("請求が要る", "自動ではない")),
 ("s22_06_kigen", CAST_W,
  [("line 1, large bold black, across the top", "五年で消える")],
  None),
 ("s22_07_dare", CAST,
  [("line 1, large bold black, across the top", "請求できる人")],
  None),
 ("s22_08_kakunin", CAST_W,
  [("line 1, large bold black, across the top", "まず通帳を確認")],
  None),
 # thẻ 9 — CƠ CHẾ GỐC của cả bài: 8 thẻ trên nói *hậu quả* (36万/返金/期限/請求),
 # chưa thẻ nào nói *vì sao tiền còn lại*. Mệnh đề lấy nguyên từ 研究ノート mục 一
 # 「年金は二か月分の後払い」. Chữ số Latin cho chắc nét (luật ③ — kanji rậm mới hay méo).
 ("s22_09_atobarai", CAST,
  [("line 1, large bold black, across the top", "2か月分の後払い")],
  None),
]


def build_text_block(lines, zu):
    """Khối TEXT — đặt NGAY CÂU 2 của prompt (luật ①)."""
    # 🔴 Sơ đồ đóng góp BA khoản, không phải hai: ô trái + ô phải + mũi tên-có-X.
    #    Đếm 2 thì prompt tự mâu thuẫn ("exactly these 3" rồi liệt kê 4) và câu chặn
    #    model-tự-thêm-chữ-rác mất tác dụng.
    n = len(lines) + (3 if zu else 0)
    out = [f"TEXT printed on the paper, exactly these {n} items and nothing else:"]
    for role, s in lines:
        out.append(f"{role}: {s}")
    if zu:
        out.append(f"a rectangular box on the left containing: {zu[0]}")
        out.append(f"a rectangular box on the right containing: {zu[1]}")
        out.append("a thick black arrow pointing from the left box to the right box, "
                   "with a large red X drawn over the arrow")
    return "\n".join(out)


def main():
    flow, names, blocks = [], [], []
    for stem, who, lines, zu in CARDS:
        txt = build_text_block(lines, zu)
        p = (f"A photorealistic close-up photograph of {who} holding up a printed sheet of paper.\n\n"
             f"{txt}\n\n"
             f"{LAYOUT.format(who='he' if who is CAST else 'she')}\n"
             f"{SCENE}\n"
             f"{QUAL}")
        one = " ".join(p.split())
        pos = one.find("TEXT printed") * 100 // max(1, len(one))
        flow.append(one); names.append(f"{stem}.png")
        blocks.append(f"### {stem}\n\n```\n{p}\n```\n")
        print(f"  {stem:<20} {len(one):>4} ky | TEXT @ {pos}% "
              + ("✓" if pos <= 15 else "🔴 PHAI <=15%"))

    io.open(os.path.join(OUT, "still22_FLOW.txt"), "w", encoding="utf-8").write("\n".join(flow) + "\n")
    io.open(os.path.join(OUT, "still22_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1} -> {n}" for i, n in enumerate(names)) + "\n")
    io.open(os.path.join(OUT, "still22_PROMPTS.md"), "w", encoding="utf-8").write(
        "# Ảnh tĩnh 'giơ giấy có chữ' — video 22\n\n"
        "Gen ẢNH (không phải video). Xong tao hoạt hoá bằng `animate_still.py`.\n\n"
        + "\n".join(blocks))
    print(f"\n{len(flow)} prompt -> still22_FLOW.txt")


if __name__ == "__main__":
    main()
