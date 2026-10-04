# -*- coding: utf-8 -*-
"""check_enum.py — GATE CHỐNG VĂN LIỆT KÊ.

🔴 PHAM VI: CHI kenh `youtube-jp-chouhen` (真夜中の朗読便) — user chot 2026-08-14.
⛔ KHONG chay cho kenh THONG TIN (health · nagaiki · shokutaku · co-dai · nenkin · kaigo ·
   akiya · showa): o do "五つ、申し上げます" roi dem tung meo la DUNG CHAT, nguoi xem can biet
   bai co may muc. Quet ca workspace 2026-08-14 bat 3 script kenh thong tin va CA BA deu
   KHONG phai loi.

Thi hành `.claude/rules/humanize-script-voice.md` §1.2 (chốt 2026-08-14, user phải nhắc
BA lần: 2026-08-13 ở chouhen 25, rồi hai lượt nữa ở chouhen 26).

Bắt ba thứ, theo đúng thứ tự quan trọng:

  E1  ≥2 dòng liên tiếp mở bằng SỐ ĐẾM (一つ。/ひとつは、/①/1./첫째/Thứ nhất) → LIỆT KÊ.
      Trong LỜI KỂ = 🔴 fail. Trong 「」 (nhân vật tuyên bố điều kiện) = ⚠️ E1b, hợp lệ.
  E2  ≥3 dòng liên tiếp có CÙNG chuỗi tag mở đầu (vd đều `[間0.4]`) → nhịp nghỉ đều nhau.
      🔴 Đây là THỦ PHẠM CHÍNH và là thứ dễ bỏ sót nhất: bỏ hết số đếm trong CHỮ mà vẫn
      để ba `[間]` đều nhau thì TTS vẫn nghỉ ba lần bằng nhau ⇒ tai vẫn nghe ra giọng đọc
      biên bản. Sửa văn mà không soi tag là sửa nửa vời.
  E3  câu TUYÊN BỐ SỐ LƯỢNG (「三つのことを」「五つの理由」…) → luật mới bỏ luôn cả con số.

CHẠY:
  python check_enum.py <file>_TTS.md            # hoặc bản .md sạch
  python check_enum.py <file>_TTS.md --quiet    # chỉ in tổng kết
Exit 1 nếu có E1 (liệt kê thật). E2/E3 in cảnh báo, exit 0.

⚠️ NGOẠI LỆ HỢP LỆ — tool tự phân biệt bằng dấu 「」: khối **nhân vật tuyên bố
điều kiện / đọc bản án** (`「一つ。この家の鍵は、もうありません」` — chouhen 25 phút 31) là
lời nói có tính thủ tục, được phép đếm. Cái bị cấm là **open-loop** và **lời kể**.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# JP · KR · VN · số · ký hiệu vòng
_HEADS = [r"一つ", r"二つ", r"三つ", r"四つ", r"五つ", r"六つ", r"七つ",
          r"ひとつ", r"ふたつ", r"みっつ", r"よっつ", r"いつつ",
          r"第[一二三四五六七八九十]", r"[①-⑳]", r"[1-9１-９]",
          r"첫째", r"둘째", r"셋째", r"넷째",
          r"[Tt]hứ nhất", r"[Tt]hứ hai", r"[Tt]hứ ba", r"[Mm]ột là", r"[Hh]ai là"]
HEAD_RE = re.compile(r"^\s*[「『]?\s*(?:" + "|".join(_HEADS) + r")(?:め|目)?\s*(?:は|には)?\s*[。、.):：]")
COUNT_RE = re.compile(r"(?:[一二三四五六七八九十\d２-９]+)\s*つ(?:のこと|の(?:もの|理由|場面|点|秘密))"
                      r"|(?:[三四五六七]|[3-7])\s*(?:つ|個)\s*(?:の)?(?:こと|理由|ポイント)")
TAG_HEAD_RE = re.compile(r"^((?:\[[^\]]*\])+)")


def strip_tags(s: str) -> str:
    return re.sub(r"\[[^\]]*\]", "", s)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    p = Path(sys.argv[1])
    quiet = "--quiet" in sys.argv
    if not p.exists():
        print(f"KHONG THAY FILE: {p}")
        return 2

    raw = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    # chỉ lấy phần thân kịch bản nếu có marker
    body = raw
    for mk in ("=== KỊCH BẢN HOÀN CHỈNH ===", "=== KICH BAN HOAN CHINH ==="):
        for i, l in enumerate(raw):
            if mk in l:
                body = raw[i + 1:]
                break

    lines = [(i + 1, l.rstrip()) for i, l in enumerate(body) if l.strip()]

    # ── E1: chuỗi ≥2 dòng liên tiếp mở bằng số đếm ────────────────────────────
    runs, cur = [], []
    for no, l in lines:
        if HEAD_RE.match(strip_tags(l)):
            cur.append((no, l))
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)

    # ── E2: ≥3 dòng liên tiếp cùng chuỗi tag mở đầu ───────────────────────────
    tagruns, cur = [], []
    for no, l in lines:
        m = TAG_HEAD_RE.match(l)
        tag = m.group(1) if m else None
        if tag and cur and cur[-1][2] == tag:
            cur.append((no, l, tag))
        else:
            if len(cur) >= 3:
                tagruns.append(cur)
            cur = [(no, l, tag)] if tag else []
    if len(cur) >= 3:
        tagruns.append(cur)

    # ── E3: tuyên bố số lượng ─────────────────────────────────────────────────
    decls = [(no, l) for no, l in lines if COUNT_RE.search(strip_tags(l))]

    print(f"══ GATE LIỆT KÊ · {p.name}")
    print(f"   luật: .claude/rules/humanize-script-voice.md §1.2 · 🔴 E1 = fail\n")

    # Phân biệt bằng máy: liệt kê trong 「」 = LỜI NÓI nhân vật (tuyên bố điều kiện / đọc bản
    # án — ngoại lệ hợp lệ, chouhen 25 phút 31) → ⚠️. Liệt kê ngoài 「」 = LỜI KỂ → 🔴 fail.
    hard = [r for r in runs if not all(strip_tags(l).lstrip().startswith(("「", "『")) for _, l in r)]
    soft = [r for r in runs if r not in hard]

    if hard:
        for r in hard:
            print(f"  🔴 E1 LIỆT KÊ TRONG LỜI KỂ — {len(r)} dòng liên tiếp mở bằng số đếm:")
            for no, l in r:
                print(f"       dòng {no}: {strip_tags(l)[:56]}")
            print()
    else:
        print("  ✅ E1  không có chuỗi liệt kê trong lời kể")
    for r in soft:
        print(f"  ⚠️  E1b LIỆT KÊ TRONG THOẠI — {len(r)} dòng (nhân vật tuyên bố điều kiện?):")
        for no, l in r:
            print(f"       dòng {no}: {strip_tags(l)[:56]}")
        print("       → hợp lệ nếu đây là khối đọc bản án/điều kiện. Nếu là open-loop thì SỬA.\n")

    if tagruns:
        for r in tagruns:
            print(f"  ⚠️  E2 NHỊP NGHỈ ĐỀU — {len(r)} dòng liên tiếp cùng tag {r[0][2]}:")
            for no, l, _ in r:
                print(f"       dòng {no}: {strip_tags(l)[:52]}")
            print("       → TTS nghỉ đều nhau = giọng đọc biên bản. Để 2 tag cho CẢ KHỐI:")
            print("         [間0.8][速0.9] ở câu mở · [速0.85][後間1.0] ở clause cuối.\n")
    else:
        print("  ✅ E2  không có chuỗi tag đều nhau (≥3 dòng)")

    if decls:
        for no, l in decls:
            print(f"  ⚠️  E3 TUYÊN BỐ SỐ LƯỢNG — dòng {no}: {strip_tags(l)[:56]}")
        print("       → luật mới bỏ luôn con số; ba clause treo dưới cùng một 知らなかった là đủ.\n")
    else:
        print("  ✅ E3  không tuyên bố số lượng")

    if not quiet and (hard or tagruns):
        print("\n  ── KHUÔN ĐÚNG (chouhen 25, bản đã lên sóng) ──")
        print("   この夜、義母はまだ何も知らなかった。")
        print("   玄関のインターホンが、いつから録画のできる機種だったのかも、")
        print("   その手に握りしめた鍵を、私がいつ誰に渡したのかも、")
        print("   二階の押し入れの、父の名前の封筒が十九年、何を待っていたのかも。")
        print("   → MỘT câu · 3 clause treo dưới cùng vị ngữ · đều là câu HỎI (〜のか) · 2 tag cả khối")

    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
