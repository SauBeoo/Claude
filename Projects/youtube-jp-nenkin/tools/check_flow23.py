# -*- coding: utf-8 -*-
"""
check_flow23.py — GATE MÂU THUẪN cho lô prompt Veo của video 23 (số lớp in ra lúc chạy).

Chạy SAU `flow23_full.py`, TRƯỚC khi đưa file cho extension gen:

    python tools/check_flow23.py

Mỗi lớp là một lỗi **đã dính thật** ở video 21/22, không phải lo xa. Ba lớp đầu là cùng
một bệnh lặp lại ba lần: **một khối chung viết cứng, dán vào cả lô, rồi huỷ chính nội dung
mà mô tả scene yêu cầu.**

🔴 KHÁC `check_flow22.py` ở ĐÚNG MỘT CHỖ, và đó là chỗ đắt nhất: video 23 khai **chính sách
   số theo TỪNG KHE** (`_scenes23.NUM`), nên ⑱⑲ không còn đòi MỌI khe SCREEN/HOLD phải có
   số to nữa — chúng đọc chính sách của khe rồi mới gác. Và thêm ㉒ gác chiều ngược lại:
   khe KHÔNG có số mà prompt vẫn xin số to = đúng lỗi đã phải vá hai vòng ở video 22.
   ⚠️ Gate quét **bản thành phẩm**, không quét hằng nguồn — lỗi đó chỉ lộ khi đọc prompt
   ĐÃ XUẤT RA (sửa hằng nguồn xong hằng khác vẫn có thể nói ngược).
"""
import collections
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
from _scenes23 import NUM  # noqa: E402

D = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
     r"\23_nenkin-seikyusho-todokanai")
VN = re.compile(r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩị"
                r"óòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]")
NOPERSON = {"INFOG", "META", "GAUGE"}
GRAPHIC = {"INFOG", "META"}
ACT = "ACTION:"


def main() -> int:
    f_flow = os.path.join(D, "flow23_FULL_FLOW.txt")
    f_ten = os.path.join(D, "flow23_FULL_TENFILE.txt")
    rows = [l.rstrip("\n") for l in io.open(f_flow, encoding="utf-8") if l.strip()]
    tens = [l for l in io.open(f_ten, encoding="utf-8") if "scene" in l]
    kinds = [re.search(r"scene\s*\d+\s*·\s*(\w+)", t).group(1) for t in tens]
    scenes = [int(re.search(r"scene\s*(\d+)", t).group(1)) for t in tens]
    if not (len(kinds) == len(scenes) == len(rows)):
        print("🔴 FLOW %d dòng nhưng TENFILE %d dòng" % (len(rows), len(kinds)))
        return 1
    print("LÔ VIDEO — " + os.path.basename(f_flow))

    bad = collections.OrderedDict()

    def chk(name, pred):
        hit = [i + 1 for i, r in enumerate(rows) if pred(r, kinds[i], scenes[i])]
        bad[name] = hit
        print(("  ✓ " if not hit else "  🔴 ") + name +
              (": %d dòng %s" % (len(hit), hit[:8]) if hit else ""))

    # ── nhóm A: khối chung huỷ nội dung scene ────────────────────────────────
    chk("① guard chữ tuyệt đối huỷ nội dung (no letters/no numbers/no text anywhere)",
        lambda r, k, s: any(x in r for x in ("no letters", "no numbers", "no text anywhere")))
    chk("② «the person … one action» ở khuôn KHÔNG NGƯỜI",
        lambda r, k, s: k in NOPERSON and "the person" in r)
    chk("③ hai câu FRAMING chọi nhau trong một prompt", lambda r, k, s: r.count("FRAMING:") > 1)
    chk("④ SPLIT/PANEL vẫn nhận FRAMING xoay vòng (NOTE của chúng đã khai khung)",
        lambda r, k, s: k in ("SPLIT", "PANEL") and "FRAMING:" in r)
    chk("⑤ HOLD bị khung rộng — tờ giấy/sổ teo mất",
        lambda r, k, s: k == "HOLD" and "wider shot" in r)
    chk("⑥ đồ hoạ 2D/3D bị tả nội thất PHÒNG KHÁCH",
        lambda r, k, s: k in GRAPHIC and any(x in r for x in
                                             ("sheer curtains", "wood furniture", "cushions")))
    chk("⑦ CROWD (công sở) bị tả nội thất NHÀ Ở",
        lambda r, k, s: k == "CROWD" and any(x in r for x in
                                             ("sheer curtains", "cushions", "home interior")))
    chk("⑧ META (3D) bị gọi là «flat artwork»",
        lambda r, k, s: k == "META" and "flat artwork" in r)
    # ㉓ CHIỀU DƯƠNG của ②: khuôn đồ hoạ phải THẬT SỰ mang câu style đồ hoạ.
    # 🔴 ② chỉ bắt được "the person" lọt vào; nó KHÔNG bắt được trường hợp `prompt_for`
    #    **thiếu hẳn nhánh** cho META/GAUGE/INFOG — đúng lỗi đã dính khi copy tool sang
    #    video 23 (prompt rơi xuống nhánh PERSON). Gate nào chỉ gác một chiều thì sẽ có
    #    ngày im lặng cho qua: phải hỏi cả "có đúng thứ cần có không".
    _GFX_SIG = {"META": "polished 3D illustration", "INFOG": "flat infographic panel",
                "GAUGE": "gauge dial"}
    chk("㉓ khuôn đồ hoạ THIẾU câu style của chính nó (nhánh prompt bị bỏ sót)",
        lambda r, k, s: k in _GFX_SIG and _GFX_SIG[k] not in r)

    # ── nhóm B: prompt tự chọi ───────────────────────────────────────────────
    chk("⑨ glow còn sống (ngoài «no glow»/«nothing glows»)",
        lambda r, k, s: bool(re.search(
            r"glow", r.replace("no glow", "").replace("nothing glows", ""))))
    # ⚠️ Hai cụm đỏ được MIỄN vì chúng là VẬT, không phải ngôn ngữ cảnh báo. Cái user cấm là
    #    đỏ NGUY HIỂM (CLAUDE.md §②: bài nói về tiền ĐƯỢC NHẬN, không phải mối nguy).
    _RED_OK = ("warm-red shirt", "deep red kettle")

    def _red(r, k, s):
        for w in _RED_OK:
            r = r.replace(w, "")
        return bool(re.search(r"\bred\b", r))

    chk("⑩ đỏ CẢNH BÁO còn trong prompt", _red)
    chk("⑪ «filmed straight on» chọi góc FRAMING three-quarter",
        lambda r, k, s: "filmed straight on" in r)
    chk("⑫ hành động THỨ HAI («At the same time») chọi câu khoá one-action",
        lambda r, k, s: "At the same time" in r)
    chk("⑬ bắt «hands stay apart» ở scene mà CHẮP TAY là nội dung",
        lambda r, k, s: "palms together" in r and "hands stay apart" in r)

    HAND_ACT = ("hand", "hands", "palms", "arm", "arms", "finger", "holds", "holding",
                "taps", "points", "propping", "lifting")
    HAND_POS = ("hand", "hands", "arm", "arms", "forearm")

    def _hand_clash(r, k, s):
        lab = "REACTION:" if "REACTION:" in r else "POSTURE:"
        if lab not in r or ACT not in r:
            return False
        act = r.split(ACT, 1)[1].split(lab)[0]
        pos = r.split(lab, 1)[1].split("FRAMING:")[0]
        return (any(re.search(r"\b%s\b" % w, act) for w in HAND_ACT)
                and any(re.search(r"\b%s\b" % w, pos) for w in HAND_POS))

    chk("⑰ REACTION/POSTURE chiếm TAY mà ACTION đã dùng tay", _hand_clash)

    # ── nhóm B2: CHÍNH SÁCH SỐ THEO KHE (bài học 12 của video 22) ────────────
    # 🔴 Khe CÓ khai số thì phải xin số to và phải là số CÓ THẬT trong bài; khe KHÔNG khai
    #    thì prompt tuyệt đối không được xin số to. Vá ở video 22 chỉ làm được vế đầu, và
    #    vế hai lọt (khối chung vẫn xin "printed large and crisp" ở khe NONE).
    def _want(s):
        p = NUM.get(s)
        return None if not p else ("PAIR" if p == "PAIR" else p.split(":", 1)[1])

    chk("⑱ khe CÓ khai số mà prompt KHÔNG xin số to",
        lambda r, k, s: _want(s) is not None and "EXACTLY ONCE" not in r and "TWO lines" not in r)
    chk("⑲ số trên đạo cụ KHÔNG phải số thật của bài",
        lambda r, k, s: (_want(s) not in (None, "PAIR")) and _want(s) not in r)
    # ㉒ chiều ngược lại — chỗ video 22 phải vá hai vòng mới sạch
    _BIG = ("printed large and crisp", "EXACTLY ONCE", "TWO lines are printed much larger",
            "printed much larger")
    chk("㉒ khe KHÔNG có số mà prompt vẫn xin số TO",
        lambda r, k, s: _want(s) is None and any(x in r for x in _BIG))

    # ⑳ MẬT ĐỘ — user đã phải nhắc HAI LẦN ở video 22 (*"cả 1 trang giấy trắng và cả 1 cái
    #    màn hình, hiển thị được 1, 2 dòng"*). Giấy tờ tiền của Nhật kín đặc.
    _DENSE_OK = ("more than twenty", "eighteen to twenty", "packed with data", "DENSELY filled")
    chk("⑳ đạo cụ giấy/màn hình THƯA — thiếu câu bắt kín đặc",
        lambda r, k, s: k in ("SCREEN", "HOLD") and not any(w in r for w in _DENSE_OK))
    chk("㉑ còn sót cụm làm THƯA («four or five rows» · «nothing else»)",
        lambda r, k, s: "four or five rows" in r or "nothing else" in r)

    # ── nhóm C: ngôn ngữ + danh tính ─────────────────────────────────────────
    chk("⑭ lẫn tiếng Việt", lambda r, k, s: bool(VN.search(r)))
    chk("⑮ SUBJECT lặp lại trong ACTION (Veo hiểu thành HAI người)",
        lambda r, k, s: "ACTION:" in r and bool(
            re.search(r"\ban elderly (man|woman|couple)\b", r.split("ACTION:", 1)[1])))

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

    # ㉕ KHỐI NOTE KÊ CHUYỂN ĐỘNG trong khi mô tả scene nói ĐỨNG YÊN.
    # 🔴 ⑧ và ㉓ chỉ hỏi "NOTE có mặt không" — chúng KHÔNG hỏi "NOTE có nói ngược mô tả
    #    không", nên cả hai đều xanh trên hai prompt tự mâu thuẫn (GAUGE scene 73 kim nằm im
    #    vs NOTE bảo kim quét; META scene 23 mười một khối đứng im vs NOTE bảo vật trôi-xoay).
    #    Chỉ lộ khi ĐỌC TRỌN prompt của TỪNG khuôn — đúng thứ CLAUDE.md nói 6/17 lớp mắc phải.
    _STILL = r"(?:stay(?:s|ing)? (?:there|still|perfectly still)|resting .{0,24}and staying|does not move|remains still)"
    _MOVE = r"(?:sweeps slowly|drift and orbit|fade in one after another|light up one after another|the objects drift)"
    chk("㉕ NOTE kê CHUYỂN ĐỘNG chọi mô tả scene ĐỨNG YÊN",
        lambda r, k, s: bool(re.search(_STILL, r)) and bool(re.search(_MOVE, r)))

    # ㉖ Cảnh có BÀN RIÊNG mà bối cảnh không có bàn (khu chờ ghế liền · quầy ngân hàng).
    #    Đo được 7/92 clip ở bản trước, nặng nhất khuôn DESK — nó luôn kèm `ON THE TABLE:`.
    _NOTABLE = ("public waiting area", "bank branch counter")
    chk("㉖ cảnh có BÀN nhưng bối cảnh KHÔNG CÓ BÀN",
        lambda r, k, s: any(x in r for x in _NOTABLE)
        and bool(re.search(r"\b(at the table|on the table|table top|table edge|ON THE TABLE)\b", r)))

    # ㉔ HAI PROMPT GIỐNG HỆT NHAU = hai clip giống hệt nhau đứng cạnh nhau trên timeline,
    #    và một lượt gen đốt đôi. Dính ở scene 9 (khuôn đồ hoạ không có biến xoay nào).
    #    Lỗi im lặng: mọi lớp khác đều xanh, file vẫn đủ dòng.
    _seen = {}
    dup = []
    for i, r in enumerate(rows, 1):
        if r in _seen:
            dup.append(i)
        _seen[r] = i
    bad["㉔ prompt TRÙNG HỆT prompt khác (gen đôi, hình lặp)"] = dup
    print(("  ✓ " if not dup else "  🔴 ") + "㉔ prompt TRÙNG HỆT prompt khác (gen đôi, hình lặp)"
          + (": %d dòng %s" % (len(dup), dup[:8]) if dup else ""))

    n = sum(len(v) for v in bad.values())
    print("\n%d prompt · dài %d–%d ký · khuôn %s"
          % (len(rows), min(map(len, rows)), max(map(len, rows)),
             dict(collections.Counter(kinds))))
    # 🔴 Số lớp ĐẾM ĐỘNG từ `bad`, đừng viết cứng: thêm một lớp mà quên sửa chuỗi
    #    thì tool tự báo sai phạm vi chính nó gác — loại lỗi rất khó nghi.
    print(("✅ SẠCH %d/%d lớp" % (len(bad), len(bad))) if not n
          else "🔴 %d LỖI — đừng đưa đi gen" % n)
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
