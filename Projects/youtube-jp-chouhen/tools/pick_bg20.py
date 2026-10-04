# -*- coding: utf-8 -*-
"""pick_bg20.py — chọn bộ clip nền NHỎ (mặc định 20) cho MỘT video chouhen.

Luật thi hành (user chốt 2026-08-16, ghi ở CLAUDE.md §HÌNH NỀN):
  ① **KHÔNG CÓ NGƯỜI** trong clip — đây là ràng buộc DUY NHẤT còn phải kiểm.
  ② ~20 clip, lặp đi lặp lại (không fetch 200+ clip mỗi video nữa).
  ③ Hai lần phát lại CÙNG một clip phải **cách nhau ≥4 cảnh**.
  ④ Không duyệt clip bằng mắt.

⚠️ Vì bỏ duyệt mắt nên ① phải được bảo đảm bằng MÁY. Cơ chế: `INDEX.json` của kho
có `queries`/`tags` RỖNG với hầu hết clip chouhen, nhưng **tên file CHÍNH LÀ query
slug của Pexels** (`old-wooden-beam-text_4102353.mp4`) → lọc bằng từ trong tên file.
Đây là lớp lọc *theo chủ đề đã đặt hàng*, không phải nhận diện người trong hình:
clip lọt lưới vẫn có thể có người ở hậu cảnh. Đánh đổi đã chọn khi bỏ duyệt mắt.

Chạy:
    python tools/pick_bg20.py --slug 27_boshi-no-namae            # chọn + ghi bg_list.txt
    python tools/pick_bg20.py --slug 27_boshi-no-namae --verify   # kiểm _render_plan.json
"""
import argparse
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
PROJ = Path(__file__).resolve().parents[1]
BG = PROJ / "06_VIDEO" / "_bg"

# ── ① CẤM: bất kỳ token nào dưới đây trong tên file = loại thẳng ──────────────
PERSON = {
    "people", "person", "man", "men", "woman", "women", "girl", "boy", "child",
    "children", "kid", "family", "couple", "crowd", "elderly", "senior", "adult",
    "hand", "hands", "finger", "arm", "face", "portrait", "head", "shoulder",
    "worker", "staff", "employee", "businessman", "businesswoman", "doctor",
    "nurse", "patient", "monk", "priest", "customer", "chef", "cook", "farmer",
    "student", "teacher", "walking", "sitting", "standing", "praying", "holding",
    "talking", "smiling", "crying", "sleeping", "eating", "drinking", "writing",
    "typing", "reading", "cleaning", "washing", "cutting", "pouring", "wearing",
    "silhouette", "figure", "body", "leg", "feet", "foot", "skin", "hair", "eye",
    # đồ MẶC TRÊN NGƯỜI = trong khung có người (bắt được ở lượt chọn đầu: `snow-on-coat`)
    "coat", "jacket", "sweater", "scarf", "glove", "gloves", "hat", "cap",
    "shoe", "shoes", "boot", "boots", "sock", "dress", "suit", "uniform",
    "apron", "sleeve", "kimono", "clothes", "clothing", "collar", "pocket",
    # động tác BẮT BUỘC có bàn tay (bắt được: `chopping-veg`)
    "chopping", "knitting", "sewing", "stirring", "folding", "carrying",
    "opening", "closing", "touching", "grabbing", "wiping", "sweeping",
    "dishwashing", "handwashing", "scrubbing", "kneading", "peeling",
    # ẢNH CHỤP trong khung = mặt người trong khung (bắt được: `old-photogra`)
    "photo", "photos", "photograph", "photography", "picture", "album", "selfie",
}

# ── Nhóm chủ đề hợp truyện 27 (11月・霊園・石・線香・実家古い・雪・雨・紙) ──
#    Mỗi nhóm lấy TỐI ĐA `--per-theme` clip → bộ 20 không bị 8 cái tuyết giống nhau.
THEMES = {
    "snow":     ["snow", "snowfa", "snowy", "blizzard", "frost", "ice"],
    "rain":     ["rain", "raindrop", "wet", "puddle", "drizzle", "condensation"],
    "steam":    ["steam", "stea", "kettle", "boiling", "vapor"],
    "tea":      ["tea", "cup", "teapot", "teacup"],
    "incense":  ["incense", "smok", "smoke", "candle", "flame", "ember"],
    "wood":     ["wooden", "wood", "beam", "plank", "timber", "sawdust", "lumber"],
    "tatami":   ["tatami", "tat", "shoji", "fusuma", "engawa"],
    "temple":   ["temple", "buddhist", "shrine", "lantern", "torii", "stone"],
    "paper":    ["paper", "envelope", "envelop", "docume", "letter", "calendar", "ledger"],
    "night":    ["night", "moon", "star", "dusk", "twilight", "streetlight"],
    "window":   ["window", "curtain", "glass", "blind", "pane"],
    "clock":    ["clock", "watch", "pendulum", "tin", "box"],
    "kitchen":  ["kitchen", "sink", "dishwashing", "faucet", "tofu", "chopping"],
    "autumn":   ["autumn", "leaf", "leaves", "ginkgo", "maple", "fallen"],
    "road":     ["asphalt", "road", "bus", "stop", "train", "rail", "station"],
    "house":    ["old", "aged", "empty", "abandoned", "corridor", "cor", "hall", "room"],
    "wind":     ["wind", "grass", "field", "fog", "mist", "cloud"],
    "lamp":     ["lamp", "light", "bulb", "glow", "shadow"],
    "fabric":   ["cloth", "fabric", "laundry", "futon", "thread", "knit"],
    "water":    ["water", "river", "stream", "drop", "ripple", "well"],
}


def toks(name: str):
    return re.sub(r"_\d+\.mp4$", "", name).split("-")


def has_person(name: str):
    """True nếu tên file gợi ý CÓ NGƯỜI.

    🔴 Tên file Pexels bị **cắt cụt ở 20 ký tự** nên token CUỐI hay bị đứt giữa chừng
    (`cold-water-h` gần như chắc là `cold-water-hands`). Khớp nguyên token là cho lọt.
    ⇒ token cuối chỉ cần là **TIỀN TỐ** của một từ trong PERSON là loại.
    Bắt được ở lượt chọn đầu: `cold-water-h` · `dry-leaves-o` (→ opening).
    Lọc thừa thì mất vài ứng viên; lọt một clip có người thì hỏng cả video.
    """
    t = toks(name)
    if set(t) & PERSON:
        return True
    tail = t[-1]
    return bool(tail) and any(w != tail and w.startswith(tail) for w in PERSON)


def pick(n: int, per_theme: int, seed: int):
    rejected = {p.name for p in (BG / "rejected").glob("*.mp4")}
    cands = defaultdict(list)
    n_all = n_person = n_rej = n_notheme = 0
    for p in sorted(BG.glob("*.mp4")):
        n_all += 1
        if p.name in rejected:
            n_rej += 1
            continue
        if has_person(p.name):
            n_person += 1
            continue
        t = set(toks(p.name))
        hit = [th for th, words in THEMES.items() if t & set(words)]
        if not hit:
            n_notheme += 1
            continue
        cands[hit[0]].append(p.name)

    rnd = random.Random(seed)
    chosen, order = [], sorted(cands, key=lambda k: -len(cands[k]))
    for rounds in range(per_theme):
        for th in order:
            if len(chosen) >= n:
                break
            pool = [x for x in cands[th] if x not in chosen]
            if pool:
                chosen.append(rnd.choice(pool))
        if len(chosen) >= n:
            break

    print("quet %d clip | loai: %d co NGUOI, %d da rejected, %d khong khop chu de"
          % (n_all, n_person, n_rej, n_notheme))
    print("ung vien sach: %d, thuoc %d chu de" % (sum(len(v) for v in cands.values()), len(cands)))
    return chosen, cands


def verify(slug: str, min_gap: int):
    plan = PROJ / "06_VIDEO" / slug / "_render_plan.json"
    if not plan.exists():
        sys.exit("[LOI] chua co %s — chay scene_render --stage segs --plan-only truoc" % plan)
    d = json.loads(plan.read_text(encoding="utf-8"))
    scenes = d.get("scenes") or d.get("picked") or d
    names = []
    for s in scenes:
        v = s.get("clip") or s.get("src") or s.get("file") if isinstance(s, dict) else s
        names.append(Path(str(v)).name)
    last, worst, worst_at = {}, 10 ** 9, None
    for i, nm in enumerate(names):
        if nm in last:
            g = i - last[nm]
            if g < worst:
                worst, worst_at = g, (nm, last[nm], i)
        last[nm] = i
    uniq = len(set(names))
    print("_render_plan: %d canh | %d clip khac nhau" % (len(names), uniq))
    print("khoang cach LAP nho nhat: %d canh %s" % (worst, worst_at if worst_at else ""))
    ok = worst >= min_gap
    print(("PASS" if ok else "FAIL") + " — nguong >=%d canh" % min_gap)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("-n", type=int, default=20)
    ap.add_argument("--per-theme", type=int, default=1)
    # 🔴 seed MẶC ĐỊNH = SỐ VIDEO trong slug → mỗi tập rút một bộ 20 KHÁC NHAU từ ~500
    # ứng viên sạch. Không có chỗ này thì mọi video dùng chung một bộ = đúng profile
    # "lặp NGUYÊN BỘ visual giống video trước" mà youtube-compliance.md §1 quét.
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--min-gap", type=int, default=4)
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    if a.verify:
        sys.exit(verify(a.slug, a.min_gap))

    seed = a.seed
    if seed is None:
        m = re.match(r"(\d+)", a.slug)
        seed = int(m.group(1)) if m else abs(hash(a.slug)) % 9973
        print("seed = %d (suy tu slug)" % seed)
    chosen, _ = pick(a.n, a.per_theme, seed)
    out = PROJ / "06_VIDEO" / a.slug / "bg_list.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(chosen) + "\n", encoding="utf-8")
    print("\nCHON %d clip -> %s" % (len(chosen), out))
    for i, c in enumerate(chosen, 1):
        print("  %2d. %s" % (i, c))


if __name__ == "__main__":
    main()
