# -*- coding: utf-8 -*-
r"""remap_art29.py — ghép lại ảnh cho plan MỚI của video 29 (v2, viết lại 2026-09-24) từ bộ ảnh v1.

VÌ SAO: ảnh v1 gắn theo CHỈ SỐ Ô (art_final/shot_KKK.png), chỉ số ô sinh từ timeline. Viết lại
kịch bản ⇒ timeline đổi ⇒ chỉ số ô đổi hết. Gen lại 95 ảnh là mất cả ngày, trong khi phần lớn lời
đọc vẫn giữ. ⇒ ghép theo NỘI DUNG: ô mới lấy ảnh của ô v1 có lời đọc giống nhất.

LUẬT:
  · Mỗi ảnh v1 dùng TỐI ĐA 1 lần (media-library.md §2 mục 4 — trong cùng video không trùng ảnh).
  · Ghép tham lam theo điểm giảm dần (bigram ký tự, Jaccard).
  · Ô điểm < WEAK ⇒ in ra "SOI MẮT" — có ảnh gán tạm nhưng chưa chắc khớp lời.
  · Ảnh 原典 (screenshot) chỉ được về đúng ô có câu dẫn 原典 — kiểm bằng cue.

CHẠY:  python tools/remap_art29.py          → ghi art_final/ (bộ cũ đã cất ở _v1_backup/art_final)
       python tools/remap_art29.py --dry    → chỉ in bảng
"""
import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
VD = PROJ / "06_VIDEO" / "29_shikaku-kakuninsho-8gatsu-85sai"
OLD_PLAN = VD / "_v1_backup" / "plan29.json"
OLD_ART = VD / "_v1_backup" / "art_final"
NEW_PLAN = VD / "plan29.json"
OUT = VD / "art_final"
WEAK = 0.30

# ô mới → ô v1, CHỐT BẰNG MẮT trên contact sheet (2026-09-24). Ép trước, phần còn lại ghép tự động.
OVERRIDE = {1: 2,     # 「1割ではなく10割」 → hai chồng xu
            21: 56,   # 「資格確認書と書いてあったかたは、ご安心」 → form 資格確認書
            24: 22,   # đi khám hằng tháng → quầy + ông cụ mở ví
            33: 25,   # 「団地の四階まで取りに戻りました」 → cầu thang 団地
            34: 89,   # 「財布を開けて、確かめて」 → ví + thẻ
            35: 52,   # 「ありましたか」 → ví có thẻ đỏ
            56: 85,   # 小林さん lần đầu → bà cụ ở bàn
            57: 67,   # 「ベランダで朝顔」 → bà cụ + giàn 朝顔
            71: 81,   # 「市役所の窓口で申請」 → quầy + 資格確認書
            75: 74,   # 療養費・領収書・明細
            81: 91,   # 「もう40分は歩かなくていい」 → vợ chồng cụ cười
            22: 51,   # 「お知らせと書いてあったかた」 → 資格情報 + quầy
            52: 86,   # sau クイズ → cặp giấy tờ
            55: 66,   # 「入院のとき、もっと大きなお金」 → bảng tính + mũi tên tiền
            88: 50}   # 「受付で手が止まることは、もうありません」 → đưa thẻ, nhân viên cười   # 「もう40分は歩かなくていい」 → vợ chồng cụ cười

# câu dẫn 原典 → ô v1 chứa ảnh chụp màn hình tương ứng phải về ô mới chứa đúng câu này
GENTEN_CUES = ["こちらが、厚生労働省のページです", "千葉県の後期高齢者医療広域連合の案内",
               "限度区分の欄が空欄で記載がない"]


def norm(s):
    return re.sub(r"[\s、。「」（）・…？！]", "", s)


def grams(s):
    s = norm(s)
    return {s[i:i + 2] for i in range(len(s) - 1)}


def jac(a, b):
    return len(a & b) / max(1, len(a | b))


def main():
    dry = "--dry" in sys.argv
    old = json.load(io.open(OLD_PLAN, encoding="utf-8"))["shots"]
    new = json.load(io.open(NEW_PLAN, encoding="utf-8"))["shots"]
    og = [grams(s["text"]) for s in old]
    ng = [grams(s["text"]) for s in new]

    pairs = sorted(((jac(ng[i], og[j]), i, j) for i in range(len(new)) for j in range(len(old))),
                   reverse=True)
    # ép 原典 trước: ô mới có cue ↔ ô cũ có cùng cue
    assign, used = {}, set()
    for i, j in OVERRIDE.items():
        assign[i] = (j, 1.0)
        used.add(j)
    for cue in GENTEN_CUES:
        ni = [i for i, s in enumerate(new) if cue in s["text"]]
        oj = [j for j, s in enumerate(old) if cue in s["text"]]
        if len(ni) != 1 or len(oj) != 1:
            print(f"🔴 cue 原典 khớp {len(ni)} ô mới / {len(oj)} ô cũ: {cue}")
            return 1
        if ni[0] in assign or oj[0] in used:
            print(f"🔴 OVERRIDE đụng ô 原典: {cue}")
            return 1
        assign[ni[0]] = (oj[0], 1.0)
        used.add(oj[0])
    for sc, i, j in pairs:
        if i in assign or j in used:
            continue
        assign[i] = (j, sc)
        used.add(j)
    miss = [i for i in range(len(new)) if i not in assign]
    if miss:
        print(f"🔴 {len(miss)} ô không còn ảnh nào để gán (ô mới nhiều hơn ảnh cũ): {miss}")
        return 1

    weak = []
    for i in range(len(new)):
        j, sc = assign[i]
        flag = "  ← SOI MẮT" if sc < WEAK else ""
        if sc < WEAK:
            weak.append(i)
        print(f"ô {i:3d} ← v1 {j:3d}  {sc:.2f}  {new[i]['text'][:34]}{flag}")
    print(f"\nô mới {len(new)} · ảnh v1 {len(old)} · dùng {len(used)} · ảnh bị dùng lại: 0 · "
          f"ô khớp yếu (<{WEAK}): {len(weak)} {weak}")

    if not dry:
        if OUT.exists():
            import time
            OUT.rename(VD / f"_art_final_before_remap_{time.strftime('%H%M%S')}")
        OUT.mkdir()
        for i, (j, _) in assign.items():
            shutil.copy2(OLD_ART / f"shot_{j:03d}.png", OUT / f"shot_{i:03d}.png")
        json.dump({str(i): {"v1": j, "score": round(sc, 3)} for i, (j, sc) in assign.items()},
                  io.open(VD / "remap_art29.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ ghi {len(assign)} ảnh vào {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
