# -*- coding: utf-8 -*-
r"""redo_flow22.py — lọc RIÊNG lô prompt cần GEN LẠI của video 22, kèm 4 miếng vá chữ/số.

⭐ USER CHỐT 2026-09-10: *"tao thích những cái clip hiện số vs chữ như video. Mày thấy sai
   text hoặc sai chữ thì mới sửa lại thôi"* ⇒ **KHÔNG đổi hướng thiết kế**: giấy và màn hình
   VẪN hiện số đọc được (quyết định 2026-09-09 giữ nguyên). Chỉ sửa đúng chỗ SAI.

📊 Soi mắt 61/61 clip lô 2026-09-10 → **25 khe phải gen lại**, chia bốn nhóm:
   A. SỐ SAI GIÁ TRỊ (9) — nặng nhất, phạm YMYL: màn hình ghi `36,000` / `36.0000` /
      `180,0000` / `336,000` / `1860000` trong khi lời đọc nói **三十六万円 = 360,000**.
   B. CHỮ/SỐ NÁT trên ĐẠO CỤ CHÍNH (5) — thẻ nhựa và khối gỗ mà prompt xin **TRƠN** lại bị
      in `¥荒¥苹市 ↑8006円` / `¥2円 18300`; biển 「栢大麦光両」; điện thoại `¥5,899 ¥09300`.
   C. CHỮ NÁT ở NỀN (9) — biển tường, lịch, tờ rơi, bảng giá: `有15149` · 「189」 ·
      `¥1从 850 1000` · `26108` · `¥ 1 5 6 円円`.
   D. NỘI DUNG SAI (1) — `c22_37_3` là cảnh CTA 「応援おねがいします」 mà ra **bàn thờ + bảng
      giá tang lễ 円431000/円459000 + hai người mặc đồ tang**.
   E. THIẾU (1) — `c22_86` chưa có clip nào (lô về 61/62).

🔴 BÀI HỌC ĐO LƯỜNG của lượt này: `media-library.md` §2.9 ghi *"chữ số Latin gen ổn định hơn
   kanji nhiều"* — và đúng, số Latin ra **nét sắc, đọc được**. Nhưng **SẮC NÉT ≠ ĐÚNG GIÁ TRỊ**.
   Guard cũ được thiết kế để chống *không đọc được*, nên nó không chặn được *đọc được nhưng
   sai*. Hai thuộc tính khác nhau, tao đã gộp làm một.
   ⇒ Vá P1 thêm **phép tự kiểm** vào chính câu prompt (số dưới = gấp đôi số trên, dấu phẩy sau
     chữ số thứ ba) thay vì chỉ liệt kê hai con số.

📛 TÊN FILE ĐÍCH GIỮ NGUYÊN (`c22_<scene>.mp4`) ⇒ thả clip mới vào cùng thư mục rồi chạy lại
   ingest: nó so **mtime** nên chỉ ghi đè đúng 25 chỗ (`render-background.md` §2.5).

CHẠY:  python tools/redo_flow22.py                     # cả 25 khe
       python tools/redo_flow22.py c22_62_1,c22_28     # chỉ 2 khe
       python tools/redo_flow22.py A          # chỉ nhóm A (số sai giá trị)
       python tools/redo_flow22.py A,B,E
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import flow22_full as F                                             # noqa: E402

VD = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                  "06_VIDEO", "22_mishikyu-nenkin-36man")

# ── danh sách gen lại, ĐÃ SOI MẮT từng clip ──────────────────────────────────
GROUPS = {
    "A": {  # số sai GIÁ TRỊ — bắt buộc sửa
        "c22_02": "sổ ghi 36,000円 (đúng phải 360,000)",
        "c22_16": "màn hình 36,000 · 36.0/15",
        "c22_23": "tablet 36,000",
        "c22_29": "điện thoại 36,000",
        "c22_35": "sổ ghi 180,00円 (méo dấu phẩy)",
        "c22_38": "tờ khai 80000 / 1860000 / 336,000",
        "c22_46": "màn hình 36,000",
        "c22_58": "màn hình 36.0000",
        "c22_88": "màn hình 180,0000 (thừa một số 0)",
    },
    "B": {  # chữ/số nát trên ĐẠO CỤ CHÍNH
        "c22_05_2": "biển 「栢大麦光両」 + ¥50000, prompt xin phong bì TRƠN",
        "c22_08": "màn điện thoại ¥5,899 · ¥09300",
        "c22_48": "khối gỗ bị in ¥2円 18300…, prompt xin khối TRƠN",
        "c22_62_1": "thẻ in 「¥荒¥苹市 ↑8006円 甲001366900」, prompt xin thẻ TRƠN",
        "c22_62_2": "thẻ in 「¥宇兴元 ¥50000」, prompt xin thẻ TRƠN",
    },
    "C": {  # chữ nát ở NỀN
        "c22_20": "thùng giấy 「壮枝の来卟」「収帰関週」",
        "c22_28": "màn tường 有15149",
        "c22_33": "lịch để bàn 「189」",
        "c22_44": "màn hình hậu cảnh 17,000",
        "c22_55": "bảng giá 「¥1从 850 1000 / 760 3000」",
        "c22_56_1": "tờ rơi 26108",
        "c22_64": "bảng tường ¥15 13 50 3000 / 円60 60 50",
        "c22_69": "thẻ ¥1000 trong khung",
        "c22_74_1": "biển 「¥ 1 5 6 円円」",
    },
    "D": {"c22_37_3": "CẢNH CTA mà ra bàn thờ + bảng giá tang lễ + đồ tang"},
    "E": {"c22_86": "THIẾU — lô về 61/62"},
}

# ── BỐN MIẾNG VÁ ─────────────────────────────────────────────────────────────
# ⚠️ Vá bằng cách thay CHUỖI trong prompt ĐÃ DỰNG, không sửa hằng số của `flow22_full`:
#    `CAM_N`/`FORM`/`SCREEN_NOTE` được nối f-string LÚC IMPORT nên gán lại `TXT` không ăn.
#    Và làm ở tầng chuỗi thì thấy ngay miếng nào KHÔNG khớp (xem gate ở cuối).

# P1 — chống rơi/thừa số 0: thêm PHÉP TỰ KIỂM vào chính câu số.
P1_FROM = ("the two highlighted lines read 180,000 and 360,000 with the dates 4/15 and 6/15")
P1_TO = ("exactly two lines are highlighted and nothing else on the page is highlighted: the "
         "upper highlighted line reads 180,000 and the lower highlighted line reads 360,000. "
         "Both are six-digit figures written with a single comma after the third digit from the "
         "left, and the lower figure is exactly twice the upper figure. The dates 4/15 and 6/15 "
         "appear beside them. No other large figure appears anywhere in the frame")

# P2 — đạo cụ phải TRƠN thì phải nói TÍCH CỰC (model đọc từ khoá, không đọc chữ "plain").
P2 = (" The one prop the subject holds up or that the shot is built around — the card, the "
      "envelope or the wooden blocks — has a smooth bare surface with nothing printed, stamped "
      "or written on it: bare white plastic, bare white paper or bare pale wood. This applies "
      "ONLY to that held prop; every other document, file and screen in the room keeps its "
      "normal dense tiny print.")

# P3 — chữ NỀN: cấm hẳn chữ trên biển/lịch/tờ rơi hậu cảnh, giữ số ở CHỦ THỂ CHÍNH.
#      Đây là chỗ user KHÔNG phàn nàn về số — họ thích số ở màn hình/giấy chính; cái nát
#      toàn nằm ở đạo cụ nền. Nên vá đúng tầng nền, đừng vá tầng chủ thể.
P3 = (" Wall signs, notice boards, price boards, desk calendars, posters, leaflets and small "
      "table cards or tags are plain blank coloured panels with no writing and no figures on "
      "them. This applies ONLY to that background signage; papers, forms and computer screens "
      "keep their normal dense tiny print and must not be blank white.")

# P4 — cảnh CTA: khoá trang phục + bối cảnh, chặn bối cảnh tang lễ.
P4 = (" Both wear plain everyday knitwear — the man a plain grey cardigan, the woman a plain "
      "brown cardigan — in a bright ordinary living room. There is no altar, no memorial "
      "photograph, no funeral flowers and no formal black clothing anywhere in the frame.")

# 🔴🔴 P0 — KHỐI CHUNG CHỌI MIẾNG VÁ, và đó chính là thứ MỜI model bịa số.
#    Câu `TXT` của `flow22_full` dán vào MỌI prompt: *"the only characters meant to be read in
#    the frame are Arabic numerals — yen figures and dates — printed large and crisp"*.
#    Ở khe CÓ màn hình/tờ khai thì đúng (nhóm A). Nhưng ở khe **không có mặt số nào hợp lệ**
#    (khối gỗ trơn · thẻ trơn · phòng chờ · lịch để bàn) thì nó là một lời XIN số to — và
#    model đáp ứng bằng cách **tự bịa**: `¥2円 18300` trên khối gỗ, `有15149` trên màn tường,
#    `26108` trên tờ rơi. Nó còn chọi thẳng P2 (*"bare wood, nothing printed"*).
#    ⇒ Khe KHÔNG có khối số (`FIG`) thì **THAY** câu đó, đừng chỉ nối thêm.
#    📌 Cùng bệnh `feedback_prompt_khoi_chung_huy_mo_ta`.
P0_FROM = ("the only characters meant to be read in the frame are Arabic numerals — yen figures "
           "and dates — printed large and crisp in a clean sans-serif; any Japanese writing on "
           "signs, labels, book spines or form headings stays small and softly out of focus")
P0_TO = ("every document, form, ledger and screen in this shot is STILL densely covered in "
         "tiny print — many ruled rows and narrow columns of very small figures, a dense grey "
         "texture that fills the page or the display and leaves almost no empty white space; "
         "none of it is large enough to read, and no large crisp numeral and no large word "
         "appears anywhere in the frame")

# P5 — man hinh dien thoai/form co DAU TICH: giu tich, bo tien. `c22_08` bi model tu them
#      `¥5,899` va `¥09300` vao mot man hinh ma prompt chi xin "green check marks".
P5 = (" The phone screen is filled with a dense form: many narrow rows of very small "
      "illegible grey print with a short column of green tick marks down one side. It is busy, "
      "not blank — but no yen amount and no large figure is legible on it.")

PATCH = {"A": ["P1"], "B": ["P1", "P2"], "C": ["P1", "P3"],
         "D": ["P1", "P3", "P4"], "E": ["P1", "P3"]}
# khe rieng: them mieng va ngoai nhom
EXTRA = {"c22_08": ["P5"]}


def main() -> int:
    arg = sys.argv[1].split(",") if len(sys.argv) > 1 else list(GROUPS)
    # cho phép chỉ định THEO KHE (`c22_62_1,c22_28`) thay vì theo nhóm — user hay chỉ cần
    # gen lại đúng một, hai khe sau khi soi bản render.
    only = {a.strip() for a in arg if a.strip().startswith("c22_")}
    want = [g for g in arg if not g.strip().startswith("c22_")] or list(GROUPS)
    if only:
        want = [g for g in GROUPS if any(k in GROUPS[g] for k in only)]
        unknown = only - {k for g in GROUPS for k in GROUPS[g]}
        if unknown:
            print(f"🔴 khe không có trong bảng GROUPS: {sorted(unknown)}")
            return 2
    bad = [g for g in want if g not in GROUPS]
    if bad:
        print(f"🔴 nhóm không có: {bad}. Chọn trong {list(GROUPS)}")
        return 2

    # dựng lại `items` GIỐNG HỆT flow22_full.main() — phải cùng `idx` mới ra cùng
    # phòng/sáng/màu (setting() và gside() xoay theo idx)
    items = []
    for r in F.build():
        if r["kind"] != "art" or r["nshot"] == 0:
            continue
        for k in range(r["nshot"]):
            suf = f"_{k+1}" if r["nshot"] > 1 else ""
            items.append(dict(stem=f"c22_{r['i']:02d}{suf}", scene=r["i"],
                              kind=F.classify(r["body"]),
                              prompt=" ".join(F.prompt_for(r["body"], len(items)).split())))
    by_stem = {x["stem"]: x for x in items}

    rows, miss, no_p1, no_p0 = [], [], [], []
    for g in want:
        for stem, why in GROUPS[g].items():
            if only and stem not in only:
                continue
            if stem not in by_stem:
                miss.append(stem)
                continue
            x = by_stem[stem]
            p = x["prompt"]
            if "P1" in PATCH[g]:
                if P1_FROM in p:
                    p = p.replace(P1_FROM, P1_TO)
                else:
                    # khe không có mặt số hợp lệ ⇒ THAY câu xin-số-to bằng P0
                    no_p1.append(stem)
                    if P0_FROM in p:
                        p = p.replace(P0_FROM, P0_TO)
                    else:
                        no_p0.append(stem)
            for tag in list(PATCH[g]) + EXTRA.get(stem, []):
                if tag == "P1":
                    continue
                p += {"P2": P2, "P3": P3, "P4": P4, "P5": P5}[tag]
            rows.append((g, stem, x["scene"], x["kind"], why, " ".join(p.split())))

    if miss:
        print(f"🔴 stem không khớp `flow22_FULL` (bảng GROUPS sai tên): {miss}")
        return 1

    rows.sort(key=lambda r: (r[0], r[2]))
    io.open(os.path.join(VD, "flow22_REDO_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(r[5] for r in rows) + "\n")
    with io.open(os.path.join(VD, "flow22_REDO_TENFILE.txt"), "w", encoding="utf-8") as fh:
        fh.write("# GEN LAI — ten file dich GIU NGUYEN, tha vao cung thu muc roi ingest lai\n")
        for i, (g, stem, sc, kind, why, _) in enumerate(rows, 1):
            fh.write(f"dong {i:>2} -> {stem}.mp4   [{g} · scene {sc:>2} · {kind}]  {why}\n")

    print(f"✅ flow22_REDO_FLOW.txt      ({len(rows)} prompt)")
    print(f"✅ flow22_REDO_TENFILE.txt")
    for g in want:
        n = sum(1 for r in rows if r[0] == g)
        print(f"   nhóm {g}: {n} khe")
    ln = [len(r[5]) for r in rows]
    print(f"   dài prompt: {min(ln)}–{max(ln)} ký")
    # ── GATE: miếng vá phải THẬT SỰ khớp, không được im lặng trượt ───────────
    if no_p1:
        print(f"\n   ⓘ {len(no_p1)} khe không có mặt số hợp lệ ⇒ P1 bỏ qua, "
              f"P0 thay câu xin-số-to")
        p0_hit = sum(1 for r in rows if P0_TO in r[5])
        ok = p0_hit == len(no_p1) and not no_p0
        print(f"   {'✓' if ok else '🔴'} P0: áp {p0_hit}/{len(no_p1)} khe"
              + (f"  — KHÔNG khớp ở {no_p0}" if no_p0 else ""))
        left = [r[1] for r in rows if P0_FROM in r[5] and P1_TO not in r[5]]
        print(f"   {'✓' if not left else '🔴'} khe không-có-số mà còn câu xin-số-to: "
              f"{left or 'không'}")
    for tag, txt in (("P2", P2), ("P3", P3), ("P4", P4), ("P5", P5)):
        hit = sum(1 for r in rows if txt.strip() in r[5])
        need = sum(1 for r in rows if tag in list(PATCH[r[0]]) + EXTRA.get(r[1], []))
        flag = "✓" if hit == need else "🔴"
        print(f"   {flag} {tag}: áp {hit}/{need} khe")
    p1_hit = sum(1 for r in rows if P1_TO in r[5])
    print(f"   ✓ P1: áp {p1_hit}/{len(rows) - len(no_p1)} khe có khối số")
    return 0


if __name__ == "__main__":
    sys.exit(main())
