# -*- coding: utf-8 -*-
"""
3 cảnh thử THẾ GIỚI — VÒNG 2 (2026-09-22).

VÒNG 1 đã gen và đo (3 clip, `F:/Youtube/Dự_án_mới_29`):
  ✅ thế giới GẦN đúng — phố chật, hòm thư đỏ, dây leo, dây điện, đèn lồng, đám đông mặt mờ
  ✅ ảnh thật, không anime; trời cobalt + mây trắng
  🔴 **W1 đi 100,9px/8s** — mẫu trung vị **36,5px** ⇒ nhanh gấp 2,8×, đúng lời user "vẫn nhanh"
  🔴 **W2/W3 mất sạch viễn tưởng** — chỉ W1 có tháp, vì nhìn dọc hẻm thì tháp rơi đúng điểm tụ;
      hai cảnh kia model vẽ thành phố kính hiện đại ⇒ **để viễn tưởng ở HẬU CẢNH là SAI TẦNG**
  🔴 **không một khoảnh khắc nào có cảm xúc** — cả ba là phong cảnh có người đi lại; W1 có bà cụ
      đan ở ô cửa たばこ tại frame 1 rồi **máy đi qua và mất hẳn** ở frame 4
  🔴 **chữ Nhật bịa 3/3** (苑忉朶 · 木脊筒専 · 余車圧) dù guard cấm đã nằm ở 5% prompt
  🔴 W3 có khẩu trang + đồ thời nay

VÒNG 2 sửa bốn thứ, mỗi thứ ở tầng nó thuộc về:
  ① tốc độ    → `PACE["creep"]`. Mẫu 36,5px trên khung 1280 = **2,8% bề ngang**, tức gần như
                KHÔNG di máy; "nhẹ nhàng dập dìu" đến từ NGƯỜI+VẬT động trong khung đứng.
  ② viễn tưởng → `RETRO_TECH` đặt VẬT vào TIỀN CẢNH (dán MỌI cảnh) + `MEGACITY` gọi tên tháp xoắn
  ③ cảm xúc   → `MOMENT` + kho `MOMENTS`, và **cảnh cảm xúc thì máy ĐỨNG** (đi thì vụt qua mất)
  ④ chữ      → đổi từ CẤM suông sang **XIN ≤2 biển một từ quen**, biển còn lại là mảng màu trơn

Chạy:  python tools/gen_test_world.py
Xuất:  06_VIDEO/01_kumo-no-ue/_test_world_FLOW.txt   ·   _test_world_TENFILE.txt
Luật:  tools/blocks_s100.py (nguồn sự thật của mọi khối)
"""
import io, re, sys, os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from blocks_s100 import (ALIVE, HEAD, REAL, PEOPLE, POV, TOWN, MEGACITY, RETRO_TECH, GREEN, MATERIALS,
                         WALK, STAND, SIT, HANDHELD, PACE, PACE_MEASURED, SLOW_STAND, GROUND,
                         EASE, CALM, MOMENT, MOMENTS, AVOID, NO_TEXT_NUM, SKY, LIGHT, OPTICS,
                         CROWD, TAIL, TAIL_SIGN, CAST, POSE_BLOCK)

S = lambda **k: k
SCENES = [
 # ── W1 ── MÁY ĐỨNG + khoảnh khắc. Vòng 1: bà cụ hiện frame 1 rồi bị vụt qua mất ─────
 S(id="W1_tabako", pose="stand", pace="creep", sky="day", light="day", crowd="few",
   cast=[], mega=True, moment="tabako_ba", act=None,
   you="standing in the narrow back lane where it widens by the tobacconist's, the spot where people "
       "stop for a moment on their way through",
   set="A view down a narrow back lane barely two people wide, the shopfronts close enough on both "
       "sides to touch, and you are standing still beside the tiny tobacconist's on the left: a small "
       "sliding window open onto the lane, its counter crowded with boxes, an electric fan with a brass "
       "cage turning slowly on the counter, and an old woman sitting just inside it. On the right a "
       "bicycle leans against a glazed-tile wall beside a red cylindrical post box, potted plants crowd "
       "every doorstep in their dozens, and a bundle of pneumatic message tubes runs along the "
       "shopfronts with brass caps where it turns the corner. Tangled overhead wires cross above you, a "
       "street lamp with a fluted glass shade hangs from the wall, and at the far end of the lane, "
       "beyond the roofs, the spiralling tiered towers of the great city stand up into the sky with a "
       "slim monorail threading between them.",
   cam="the view holds steady on the open window with the lane and the far towers beyond it"),

 # ── W2 ── cảnh THỞ, không người: test viễn tưởng ĐẬM nhất ───────────────────────────
 S(id="W2_miharashi", pose="stand", pace="creep", sky="day", light="day", crowd="none",
   cast=[], mega=True, moment=None,
   you="standing at the concrete parapet at the top of the worn steps above the town, where everyone "
       "stops to look out",
   set="A wide view out over the whole town from a concrete parapet: below you the tiled and "
       "corrugated-steel roofs of the little streets packed close together with their aerials and water "
       "tanks and washing lines, a big old tree leaning over them, ivy climbing the parapet in a broad "
       "healthy sheet at the left edge of the frame, and a plain painted signboard on a post with "
       "nothing written on it. Beyond the roofs stand the spiralling tiered towers of the great city, "
       "tier widening above tier like pagodas grown enormous, their terraces planted green, joined to "
       "one another by slender bridges and elevated roadways high in the air.",
   act="Nobody is in the shot. A single riveted monorail carriage glides slowly along its rail between "
       "the towers, a thin plume of white steam drifts up from somewhere among the roofs below and "
       "leans away on the wind, the washing on the lines lifts and falls, and the shadows of the clouds "
       "move slowly across the tiers of the city.",
   cam="the view holds steady out over the roofs with the tiered towers and the piled white cumulus "
       "above them"),

 # ── W3 ── đi bộ CHẬM NHẤT + khoảnh khắc trao tay ────────────────────────────────────
 S(id="W3_shoutengai", pose="walk", pace="creep", sky="window", light="interior", crowd="busy",
   cast=[], mega=False, moment="trao_tien", act=None,
   you="walking very slowly into the covered shopping arcade in the middle of the afternoon",
   set="A view down the middle of a covered shopping street: a translucent corrugated roof high "
       "overhead letting the daylight down in long pale bars, shopfronts opening onto the walkway on "
       "both sides with their goods stacked out to the edge, plain unlettered painted boards above the "
       "frontages, cloth noren and canvas awnings hanging low, paper lanterns strung along above, "
       "bicycles parked in rows against the pillars. Just ahead on the left is a grocer's sloping stand "
       "of vegetables in wooden crates with a brass and glass vending machine beside it, a pressure "
       "dial on its front and copper piping down its side, and one small board above the stand carrying "
       "the single word 氷 in large clean brush strokes.",
   cam="the shot begins framed on the vegetable stand just ahead with the arcade running away beyond "
       "it, the camera then edges forward barely at all, and the shot ends with the stand still in "
       "front of you and only a little more of the arcade opened out past it"),
]

# ── POV hoá (làm ở TẦNG HÀM — replace trên source Python đã trượt 3 lần) ──
_POVIFY = [
    (r"the camera then lifts",  "you then raise your eyes"),
    (r"the camera then tilts",  "you then raise your eyes"),
    (r"the camera then edges",  "you then move"),
    (r"the camera then drifts", "you then draw"),
    (r"the camera then turns",  "you then turn your head"),
    (r"the camera then",        "you then"),
    (r"the camera",             "you"),
]


def povify(t):
    for a, b in _POVIFY:
        t = re.sub(a, b, t)
    return t


def build(sc):
    # ⭐⭐ THU TU KHOI = thu quyet dinh, va day la lan THU HAI phai sap lai.
    #   Do vong 2: RETRO_TECH (vien tuong TIEN CANH) roi xuong 67-75%, thap xoan 73-75%,
    #   luat chu 30-33% => dung 3 cho ma `ai-video-regen.md` §2 goi la "model bo qua".
    #   Tao them khoi moi roi lai NOI VAO CUOI — cung loi da sua o vong 1, lap o cho khac.
    # => Sap theo THU DANG HONG: vien tuong (hong 2/3) → chu (3/3) → cam xuc (3/3) → toc do (1/3).
    #   MEGACITY di TRUOC RETRO_TECH: thap xoan hong 2/3 canh, vat tien canh hong 3/3 nhung
    #   HEAD da nhac vat tien canh o 4%. Dat theo THU HONG NANG NHAT, khong noi nguong cho vua.
    P = [HEAD]
    if sc.get("mega"):
        P.append(MEGACITY)
    P += [RETRO_TECH, NO_TEXT_NUM, REAL, POV, ALIVE]
    for c in sc["cast"]:
        P.append(CAST[c])
    P.append("You are " + sc["you"] + ", and this is what you see.")
    P.append(sc["set"])

    # ⭐ CAM XUC: canh nao co moment thi dan MOMENT + khoanh khac cu the.
    #   Canh khong co moment phai la canh THO (khong nguoi) — dung bat MOT clip 8s lam ca hai.
    if sc.get("moment"):
        P.append(MOMENT)
        P.append(MOMENTS[sc["moment"]])
    elif sc.get("act"):
        P.append(sc["act"])

    if CROWD[sc["crowd"]]:
        P.append(CROWD[sc["crowd"]])
    P.append(CALM)

    pace = PACE[sc["pace"]]
    if sc["pose"] == "walk":
        P.append("Your movement, the only one in this shot: " + povify(sc["cam"]) + "; " + EASE
                 + ". " + pace + " " + GROUND + " " + WALK)
    else:
        P.append("The framing does not change at all from the first frame to the last: the shot holds "
                 "one single unmoving view for the whole eight seconds and the viewpoint never pushes "
                 "in, never pulls back, never pans and never drifts — " + povify(sc["cam"]) +
                 " for the whole shot. What changes is only what happens inside that unmoving frame. "
                 + SLOW_STAND + " " + POSE_BLOCK[sc["pose"]])

    # 🔴 HANDHELD tung BI MAT o ca hai tool: no nam trong list dau `P = [...]`, va luc sap lai
    #    thu tu khoi tao viet lai list do nen no roi ra ngoai — 0/3 va 0/34 prompt co no.
    #    Dat canh khoi tu the vi no noi ve MAY, va de lan sau sap lai thu tu thi no di theo.
    P.append(HANDHELD)
    P.append(TOWN)
    P.append(GREEN)
    P.append(MATERIALS)
    P.append(PEOPLE)      # ha xuong day: REAL o dau da chan CG, PEOPLE la lop bo sung
    P.append(AVOID)       # khoi dai nhat (1.678 ky) — de o dau thi no day moi thu khac xuong
    if SKY[sc["sky"]]:
        P.append(SKY[sc["sky"]])
    P.append(LIGHT[sc["light"]])
    P.append(OPTICS)
    has_sign = bool(re.search(r"[぀-ヿ一-鿿]", sc["set"] + (sc.get("act") or "")))
    P.append(TAIL_SIGN if has_sign else TAIL)
    return " ".join(x.strip() for x in P if x.strip())


# chi cho phep chu cua NHUNG TU QUEN da khai o NO_TEXT_NUM
JP_OK = tuple("ゆ氷たばこパンさかな")


def _at(lo, p, key, limit, label):
    """Tra (ten_gate, dat_khong) — ten SINH TU nguong nen khong bao gio lech voi phep kiem.
    🔴 Da dinh: doi ten thanh '<=20%' ma bieu thuc con '<= 12' => gate bao do kem thong tin SAI."""
    i = lo.find(key)
    pct = i * 100 // len(p) if i >= 0 else 999
    return (f"{label}<={limit}%", pct <= limit)


def gate(prompts):
    bad = ["35mm", "16mm", "respectful distance", "hands only", "feet only", "pedestal",
           "crane down", "sink down", "floating island", "hovering city",
           "rock pillar", "sea of cloud", "suspension bridge", "treehouse", "16:9", "1920x1080"]
    fails = 0
    for i, (sc, p) in enumerate(prompts, 1):
        lo = p.casefold()
        # ⚠️ bo chinh cac cau CAM ra truoc khi quet — gate da doc trung van cua minh 7 lan
        scan = lo
        for kill in ("it is not a cyberpunk city: no neon, no holograms, no glass towers, no glowing "
                     "signs, no flying cars, nothing hovering",
                     "never electronic, never a screen with an image on it, never neon, never a "
                     "hologram, and nothing hovers or floats",
                     "and it is not a modern city of glass office towers"):
            scan = scan.replace(kill, "")
        anim = [m.group(0) for m in re.finditer(r"(?<!not )(?<!never )anim\w*", lo)]
        has_pace = sum(v.casefold()[:60] in lo for v in PACE.values())
        pos = dict([
            _at(lo, p, "impossible spiralling ziggurats", 10, "THAP-XOAN") if sc.get("mega") else ("THAP-XOAN<=10%", True),
            _at(lo, p, "right here in the foreground within arm's reach", 20, "VT-TIEN-CANH"),
            _at(lo, p, "no distorted, melted or asymmetric faces", 10, "CAM-MAT"),
            _at(lo, p, "most of the shop signboards", 26, "CAM-CHU"),
            _at(lo, p, "live-action photography, shot on a real camera", 34, "REAL"),
            _at(lo, p, "first-person point of view", 38, "POV"),
            _at(lo, p, "colossal city stacked in layers", 4, "THE-GIOI"),
            _at(lo, p, "not quite ours", 8, "VT-HEAD"),
        ])
        chk = dict(pos)
        chk.update({
            "HEAD@0":       lo.startswith("live-action photography, a real photograph of a real place"),
            "cam-than-nguoi-xem": "no part of the viewer's own body" in lo,
            "khong-nhin-tay":     "you never look down at your own hands or feet" in lo,
            "khai-cho-dung":      "and this is what you see" in lo,
            "khong-xin-anime":    not anim,
            "lop-gan-chat":       "there is no empty wall anywhere" in lo,
            "bien-tron":     "at most two signs anywhere in the frame carry any writing" in lo,
            "cam-do-hien-dai": "no face masks on anyone" in lo,
            # canh co nguoi phai co MOMENT; canh khong MOMENT phai la canh THO
            "cam-xuc-hay-tho": bool(sc.get("moment")) ^ (sc["crowd"] == "none"),
            "co-vong-cung":  ("three beats and the middle one is the peak" in lo) if sc.get("moment") else True,
            "mot-muc-toc-do": (has_pace == 1) if sc["pose"] == "walk" else ("you are completely still" in lo),
            "hai-moc": ("the shot begins" in lo and "the shot ends" in lo) if sc["pose"] == "walk"
                       else ("the framing does not change at all" in lo),
            "khoang-lang":      "nothing else happens in it" in lo,
            "cam-mat-dam-dong": "if a background face cannot be rendered cleanly" in lo,
            "khong-tu-cam":     not [b for b in bad if b in scan],
            "chu-chi-tu-quen":  all(ch in JP_OK for ch in re.findall(r"[぀-ヿ一-鿿]", p)),
            "cam-so-goc":       "no timestamps, no counters" in lo,
        })
        f = [k for k, v in chk.items() if not v]
        if f:
            fails += 1
            print(f"  🔴 {i} {sc['id']:<16} {f}")
    return fails


def main():
    prompts = [(sc, build(sc)) for sc in SCENES]
    vd = os.path.join(ROOT, "06_VIDEO", "01_kumo-no-ue")
    os.makedirs(vd, exist_ok=True)
    flow = os.path.join(vd, "_test_world_FLOW.txt")
    tenf = os.path.join(vd, "_test_world_TENFILE.txt")
    with io.open(flow, "w", encoding="utf-8") as fh:
        fh.write("\n\n".join(p for _, p in prompts) + "\n")
    with io.open(tenf, "w", encoding="utf-8") as fh:
        fh.write("# VONG 2 — toc do creep + vien tuong TIEN CANH + khoanh khac cam xuc\n")
        fh.write(f"# moc mau: {PACE_MEASURED}\n")
        for i, (sc, _) in enumerate(prompts, 1):
            fh.write(f"{i}\ttest_{sc['id']}.mp4\t{sc['pose']}/{sc['pace']} · "
                     f"crowd={sc['crowd']} · mega={'CO' if sc.get('mega') else '-'} · "
                     f"moment={sc.get('moment') or '-'}\n")

    L = [len(p) for _, p in prompts]
    print(f"\n3 canh thu VONG 2  ·  prompt {min(L)}–{max(L)} ky")
    for sc, p in prompts:
        print(f"  {sc['id']:<16}{len(p):>6} ky · {sc['pose']:<5}/{sc['pace']:<5} · "
              f"mega={'CO' if sc.get('mega') else '- '} · moment={sc.get('moment') or '-'}")
    print("\nGATE:")
    n = gate(prompts)
    print("  ✅ SACH 3/3" if not n else f"  🔴 {n} canh LOI")
    print(f"\n-> {flow}\n-> {tenf}")
    print(f"\nMOC DO (mau PUotm8YDbKM, {PACE_MEASURED['n_shot']} shot): trung vi "
          f"{PACE_MEASURED['median_px_per_8s']}px/8s · p25 {PACE_MEASURED['p25']}px · "
          f"{PACE_MEASURED['pct_under_20px']}% shot <20px · jitter {PACE_MEASURED['jitter_median']}")
    print("SOI: ① co VAT vien tuong o TIEN CANH khong  ② W2 co THAP XOAN khong"
          "  ③ co khoanh khac dang xem khong  ④ con chu bia khong")
    return 0


if __name__ == "__main__":
    sys.exit(main())
