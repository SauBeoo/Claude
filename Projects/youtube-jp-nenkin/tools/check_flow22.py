# -*- coding: utf-8 -*-
"""
check_flow22.py — GATE MÂU THUẪN (21 lớp) cho lô prompt Veo của video 22.

Chạy SAU `flow22_full.py`, TRƯỚC khi đưa file cho extension gen:

    python tools/check_flow22.py          # lô VIDEO  (flow22_FULL_*)
    python tools/check_flow22.py --img    # lô ẢNH LƯNG (img22_FULL_*, nhãn khối là POSE:)

🔴 MỘT GATE CHO CẢ HAI LÔ, đừng viết bản thứ hai: prompt ảnh của `img22_prompts.py` dùng
   lại y nguyên khối cast/ánh sáng/màu/framing của lô video, nên 17 lớp mâu thuẫn này áp
   nguyên vẹn. Hai bản gate = sớm muộn lệch nhau và không biết bản nào đúng
   (`feedback_gate_va_builder_phai_cung_ten`).

Mỗi lớp dưới đây là một lỗi **đã dính thật** trong lô này, không phải lo xa. Ba lớp
đầu là cùng một bệnh lặp lại ba lần: **một khối chung viết cứng, dán vào cả 73 prompt,
rồi huỷ chính nội dung mà mô tả scene yêu cầu.**

🔴 Vì sao phải là gate máy chứ không phải đọc lại: 6/17 lớp này CHỈ lộ khi đọc trọn
   một prompt của TỪNG khuôn — mà lô có 73 prompt và 11 khuôn, nên vòng duyệt mắt lần
   nào cũng bỏ sót. Gate rẻ hơn một lượt gen hỏng 73 clip.
"""
import collections
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

D = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
VN = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
                r"óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]")
NOPERSON = {"INFOG", "META", "GAUGE"}   # khuôn mà khung có thể hoàn toàn không người
GRAPHIC = {"INFOG", "META"}             # khuôn vẽ 2D/3D, không phải quay thật


def main() -> int:
    sb = "--sb" in sys.argv                     # lô STORYBOARD (chia theo sàn 9s)
    img = "--img" in sys.argv or sb
    stem = "sb22" if sb else "img22" if img else "flow22"
    _dir = D + r"\_storyboard" if sb else D
    _f_flow = "%s\\%s%s.txt" % (_dir, stem, "_FLOW" if sb else "_FULL_FLOW")
    _f_ten = "%s\\%s%s.txt" % (_dir, stem, "_TENFILE" if sb else "_FULL_TENFILE")
    # 🔴 Nhãn khối mô tả: dò theo NỘI DUNG FILE, đừng suy từ cờ. Lô ảnh bản đầu dùng "POSE:",
    #    nhưng từ 2026-09-09 nó gọi thẳng flow22.prompt_for nên nhãn lại là "ACTION:" ⇒ ghim
    #    cứng theo cờ là để 3 lớp ⑮⑯⑰ IM LẶNG cho qua (lần thứ ba của cùng một bệnh:
    #    gate nào chưa từng báo đỏ thì phải nghi nó).
    _probe = io.open(_f_flow, encoding="utf-8").read(4000)
    ACT = "POSE:" if "POSE:" in _probe else "ACTION:"
    print(("LÔ STORYBOARD" if sb else "LÔ ẢNH LƯNG" if img else "LÔ VIDEO")
          + " — " + os.path.basename(_f_flow))
    rows = [l.rstrip("\n") for l in io.open(_f_flow, encoding="utf-8") if l.strip()]
    tens = [l for l in io.open(_f_ten, encoding="utf-8") if "scene" in l]
    # 🔴 Dò khuôn bằng «scene N · KIND», KHÔNG bằng «· KIND]»: TENFILE của lô ảnh còn ghi
    #    thêm clip nó thay + preset hoạt hoá sau khuôn, nên dấu «]» không đứng ngay sau nữa.
    kinds = [re.search(r"scene\s*\d+\s*·\s*(\w+)", t).group(1) for t in tens]
    if len(kinds) != len(rows):
        print("🔴 FLOW %d dòng nhưng TENFILE %d dòng" % (len(rows), len(kinds)))
        return 1

    bad = collections.OrderedDict()

    def chk(name, pred):
        hit = [i + 1 for i, r in enumerate(rows) if pred(r, kinds[i])]
        bad[name] = hit
        print(("  ✓ " if not hit else "  🔴 ") + name +
              (": %d dòng %s" % (len(hit), hit[:8]) if hit else ""))

    # ── nhóm A: khối chung huỷ nội dung scene ────────────────────────────────
    chk("① guard chữ tuyệt đối huỷ nội dung (no letters/no numbers/no text anywhere)",
        lambda r, k: any(x in r for x in ("no letters", "no numbers", "no text anywhere")))
    chk("② «the person … one action» ở khuôn KHÔNG NGƯỜI",
        lambda r, k: k in NOPERSON and "the person" in r)
    chk("③ hai câu FRAMING chọi nhau trong một prompt", lambda r, k: r.count("FRAMING:") > 1)
    chk("④ SPLIT/PANEL vẫn nhận FRAMING xoay vòng (NOTE của chúng đã khai khung)",
        lambda r, k: k in ("SPLIT", "PANEL") and "FRAMING:" in r)
    chk("⑤ HOLD bị khung rộng — tờ giấy/sổ teo mất",
        lambda r, k: k == "HOLD" and "wider shot" in r)
    chk("⑥ đồ hoạ 2D/3D bị tả nội thất PHÒNG KHÁCH",
        lambda r, k: k in GRAPHIC and any(x in r for x in
                                          ("sheer curtains", "wood furniture", "cushions")))
    chk("⑦ CROWD (công sở) bị tả nội thất NHÀ Ở",
        lambda r, k: k == "CROWD" and any(x in r for x in
                                          ("sheer curtains", "cushions", "home interior")))
    chk("⑧ META (3D) bị gọi là «flat artwork»",
        lambda r, k: k == "META" and "flat artwork" in r)

    # ── nhóm B: prompt tự chọi ───────────────────────────────────────────────
    chk("⑨ glow còn sống (ngoài «no glow»/«nothing glows»)",
        lambda r, k: bool(re.search(r"glow", r.replace("no glow", "").replace("nothing glows", ""))))
    # ⚠️ Hai cụm đỏ được MIỄN vì chúng là VẬT, không phải ngôn ngữ cảnh báo:
    #    «warm-red shirt» = trang phục khoá nhận dạng cast ông · «deep red kettle» = đạo cụ
    #    bếp, chính thứ cho lô ảnh chút màu mạnh mà mẫu có còn lô cũ của mình thiếu.
    #    Cái user cấm là đỏ NGUY HIỂM (quầng đỏ, vùng đỏ đồng hồ đo, dấu ✗ đỏ) — xem
    #    CLAUDE.md §② "Đỏ: bài nói về tiền ĐƯỢC NHẬN, không phải mối nguy".
    _RED_OK = ("warm-red shirt", "deep red kettle")

    def _red(r, k):
        for w in _RED_OK:
            r = r.replace(w, "")
        return bool(re.search(r"\bred\b", r))

    chk("⑩ đỏ CẢNH BÁO còn trong prompt", _red)
    chk("⑪ «filmed straight on» chọi góc FRAMING three-quarter",
        lambda r, k: "filmed straight on" in r)
    chk("⑫ hành động THỨ HAI («At the same time») chọi câu khoá one-action",
        lambda r, k: "At the same time" in r)
    chk("⑬ bắt «hands stay apart» ở scene mà CHẮP TAY là nội dung",
        lambda r, k: "palms together" in r and "hands stay apart" in r)

    # ⑰ POSTURE nói về TAY trong khi ACTION đã cho tay làm việc khác — tay không làm hai
    #    việc cùng lúc, và Veo lại phải tự chọn bỏ vế nào (dòng 4: hai tay đang cầm phong bì
    #    đẩy ra/kéo về, POSTURE lại bảo một tay chống lên má).
    HAND_ACT = ("hand", "hands", "palms", "arm", "arms", "finger", "holds", "holding",
                "taps", "points", "propping", "lifting")
    HAND_POS = ("hand", "hands", "arm", "arms", "forearm")

    # 🔴 Nhãn khối đổi từ POSTURE: sang REACTION: (vá 2026-09-09) — gate phải nhận CẢ HAI,
    #    nếu không nó im lặng cho qua và ta lại tin một gate đã chết.
    #    Đúng bài học đã ghi: "gate nào chưa từng báo đỏ thì phải nghi nó, không phải tin nó".
    def _hand_clash(r, k):
        lab = "REACTION:" if "REACTION:" in r else "POSTURE:"
        if lab not in r or ACT not in r:
            return False
        act = r.split(ACT, 1)[1].split(lab)[0]
        pos = r.split(lab, 1)[1].split("FRAMING:")[0]
        return (any(re.search(r"\b%s\b" % w, act) for w in HAND_ACT)
                and any(re.search(r"\b%s\b" % w, pos) for w in HAND_POS))

    chk("⑰ REACTION/POSTURE chiếm TAY mà ACTION đã dùng tay", _hand_clash)

    # ⑱ MÀN HÌNH / GIẤY / SỔ PHẢI CÓ SỐ LIỆU ĐỌC ĐƯỢC (user chốt 2026-09-09:
    #    *"giấy phải có số liệu chứ, màn hình máy tính cũng phải có số liệu chứ"*).
    # 🔴 Lớp này ĐÃ BỊ ĐẢO CHIỀU một lần trong cùng ngày: bản đầu nó bắt màn hình phải RỖNG.
    #    Khi đổi hướng, chuỗi nó dò (`EMPTY TEMPLATE`) biến mất ⇒ gate **chết im lặng, vẫn
    #    báo xanh**. Đây là lần thứ hai trong một buổi — cùng bệnh với ⑰ (POSTURE→REACTION).
    #    ⇒ Đổi nội dung khối nào thì phải đi sửa gate đang dò khối đó, NGAY LƯỢT ĐÓ.
    chk("⑱ SCREEN/HOLD thiếu SỐ LIỆU đọc được (chữ số Ả Rập)",
        lambda r, k: k in ("SCREEN", "HOLD") and "ARABIC NUMERALS" not in r)

    # ⑲ Số trên đạo cụ phải là số CÓ THẬT trong bài — Veo vẽ số nào thì người xem đọc số đó,
    #    và đây là kênh YMYL tài chính (`CLAUDE.md` §③ cấm bịa số).
    chk("⑲ đạo cụ có số mà KHÔNG khai bộ số thật của bài",
        lambda r, k: "ARABIC NUMERALS" in r and "180,000 and 360,000" not in r)

    # ⑳ MẬT ĐỘ — user đã phải nhắc HAI LẦN (*"mỗi trang giấy trắng viết 1 dòng chữ trông điêu
    #    vãi"* → *"cả 1 trang giấy trắng và cả 1 cái màn hình, hiển thị được 1, 2 dòng"*).
    #    Giấy tờ tiền của Nhật kín đặc; vài dòng trên nền trắng nhìn ra giả ngay.
    # 🔴 Đây là thứ TRÔI ĐI HAI LẦN nên nó phải là gate, không phải điều cần nhớ: mỗi lần sửa
    #    khối SCREEN/FORM/BOOK là một lần có thể vô tình viết lại "four or five rows".
    _DENSE_OK = ("more than twenty", "eighteen to twenty", "packed with data", "DENSELY filled")
    chk("⑳ đạo cụ giấy/màn hình THƯA — thiếu câu bắt kín đặc",
        lambda r, k: k in ("SCREEN", "HOLD") and not any(w in r for w in _DENSE_OK))
    chk("㉑ còn sót cụm làm THƯA («four or five rows» · «nothing else»)",
        lambda r, k: "four or five rows" in r or "nothing else" in r)

    # ── nhóm C: ngôn ngữ + danh tính ─────────────────────────────────────────
    chk("⑭ lẫn tiếng Việt", lambda r, k: bool(VN.search(r)))
    chk("⑮ SUBJECT lặp lại trong ACTION (Veo hiểu thành HAI người)",
        lambda r, k: "ACTION:" in r and bool(
            re.search(r"\ban elderly (man|woman|couple)\b", r.split("ACTION:", 1)[1])))

    # giới tính: đại từ trong ACTION phải khớp cast khai ở SUBJECT
    WRONG = {"man": ("she", "her", "Her", "they", "their", "Their"),
             "woman": ("he", "his", "His", "they", "their", "Their"),
             "couple": ("he", "his", "His", "she", "her", "Her")}
    sex = []
    for i, r in enumerate(rows, 1):
        if ACT not in r:
            continue
        head, body = r.split(ACT, 1)
        w = ("man" if "Japanese man" in head else "woman" if "Japanese woman" in head
             else "couple" if "couple" in head else None)
        if w and any(re.search(r"\b%s\b" % x, body) for x in WRONG[w]):
            sex.append(i)
    bad["⑯ lệch giới tính giữa SUBJECT và ACTION"] = sex
    print(("  ✓ " if not sex else "  🔴 ") + "⑯ lệch giới tính giữa SUBJECT và ACTION" +
          (": %d dòng %s" % (len(sex), sex[:8]) if sex else ""))

    n = sum(len(v) for v in bad.values())
    print("\n%d prompt · dài %d–%d ký · khuôn %s"
          % (len(rows), min(map(len, rows)), max(map(len, rows)),
             dict(collections.Counter(kinds))))
    print("✅ SẠCH 21/21 lớp" if not n else "🔴 %d LỖI — đừng đưa đi gen" % n)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
