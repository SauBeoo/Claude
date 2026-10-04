# -*- coding: utf-8 -*-
"""build_slides_13.py — sinh `13_..._SLIDES.json` cho video 13 (遺族年金・4回書き直す).

VÌ SAO CÓ TOOL NÀY: xem `build_slides_11.py`. Bản 13 thêm 2 thứ:

⭐ 1. LAYOUT `zu` (SƠ ĐỒ) LÀ LỚP CHỦ LỰC (user chốt 2026-08-17, dán 3 frame đối thủ:
     *"tao muốn sinh ra các hình như này chứ không thuần text nhé"*). 10 layout cũ đều là
     BẢNG — chữ là nội dung, icon chỉ trang trí đầu dòng. `zu` là vật đặt tự do + mũi tên
     + bong bóng thoại + dấu ✗, người xem HIỂU BẰNG HÌNH rồi mới đọc chữ.
     Engine: `_media_library/make_stage.py::L_zu`.

⭐ 2. GATE NHỊP ĐO BẰNG **GIÂY**, KHÔNG DÙNG SỐ DÒNG LÀM PROXY (sửa lỗi của bản 11).
     Bản 11 đòi "cách ≥2 dòng" để suy ra "entry ≥6s" — nhưng 2 dòng NGẮN thì vẫn <6s:
     đo thật ở bài này, cặp dòng 9→10 (「違うんです。」+「入るのは、13万9千円。」) chỉ
     **3,9 giây** mà vẫn qua gate cũ. Nay tính đúng công thức của `make_tts.py`
     (5,72 ký/giây + 0,45s/dòng + 1,0s/đoạn trống) rồi chặn ở 6,0s.

TRỤC HÌNH của video này: **một con số bị viết lại 4 lần**. Mã hoá bằng thẻ `zu` "SPINE"
(hộp số CŨ → mũi tên → hộp số MỚI, kèm bong bóng nói VÌ SAO) dùng **8 lần**:
21万 → 6万7千 → 4万8千 → 通帳13万9千 → +5万3千/0 → 2028年の線 → tổng kết → trả lời bà 山田.
Đổi layout mấy thẻ đó là phá xương sống thị giác của bài.

CHẠY:  python tools/build_slides_13.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, r"E:\Claude\Projects\_media_library")
from make_stage import zu_check as _zu_check      # noqa: E402  — hình học ở tool, không chép
from make_stage import zu_row as ROW              # noqa: E402  — tự phân bố hàng theo bề rộng thật
from make_stage import icon_path as _icon_path    # noqa: E402  — 🔴 icon tìm ở 2 root (riêng kênh
# + kho chung `_media_library/stage_icons`). Bản đầu builder tự glob `assets/icons` của kênh nên
# báo "KHÔNG CÓ FILE" cho 10 icon vừa thêm vào kho chung — đúng bài học: đừng chép logic của tool.

PROJ = Path(__file__).resolve().parents[1]
STEM = "13_izoku-nenkin-4bunno3-20nen"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"

NL = "\n"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0   # y hệt make_tts.py — đừng để lệch
MIN_SEC = 6.0                                      # audience-45plus.md §2 mục 2


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


def N(id_, kind, at, **kw):
    return dict(id=id_, kind=kind, at=at, **kw)


def E(a, b, style="arrow", **kw):
    return dict({"from": a, "to": b, "style": style}, **kw)


# ── thẻ SPINE: số CŨ → số MỚI, bong bóng nói VÌ SAO ────────────────────────────
def spine(match, title, old, new, why, close, sub=None, left="sensei_explain",
          right="kikite_think", old_dim=True, tone_new="amber"):
    # 🔴 `hero: true` — số của thẻ spine phải TO. Bản đầu dùng label cỡ thường (46px) nên
    # cả thẻ chỉ có 3 vật nhỏ giữa bảng, phủ mực ~3% (gate thẻ trống của make_stage bắt được).
    # Đây là con số đắt nhất bài ⇒ nó phải là thứ to nhất trên bảng.
    # 🔴 CHỈ MỘT số được `hero` — số MỚI. Bản đầu cho cả hai hero (92px) thì hai hộp rộng
    # 490px, cộng icon giữa là 1.100px trong khe 950px ⇒ gate hình học báo CHỒNG NHAU +
    # ĐỤNG NHÂN VẬT ở cả 4 thẻ spine. Số cũ là thứ bị bỏ đi, nó không cần to.
    # Icon giữa cũng bỏ: khe còn lại chỉ ~110px, nhét icon vào là mũi tên teo còn 20px.
    return C(match, "zu", title=title,
             nodes=[N("old", "label", [0.17, 0.40], label=old, lw=300),
                    N("new", "label", [0.75, 0.40], label=new, lw=400, hero=True,
                      under=True),
                    # 🔴 BA KHỐI DỌC. Hai khối (hàng số + bong bóng đáy) luôn để lại một khe
                    # ~185px ở giữa — không phải lỗi thi hành, là hình học: hai khối thì chỉ có
                    # một khe để nhận hết phần trống. Khối thứ ba (dải chốt) chia phần trống đó
                    # thành hai khe nhỏ. Bong bóng dời lên GIỮA, tail="up" vẫn trỏ vào hàng số.
                    N("bb", "bubble", [0.62, 0.62], label=why, tail="up", lw=480),
                    N("cl", "label", [0.50, 0.99], label=close, lw=560)],
             edges=[E("old", "new", "arrow", tone=tone_new)],
             left=left, right=right, sub=sub)


# ── thẻ 3 CỘT DỌC: 3 vật + câu chốt đáy ────────────────────────────────────────
def cols3(match, title, items, close, left="sensei_caution", right="kikite_worried"):
    """3 hộp DỌC (icon to giữa + nhãn dưới) + dải chốt đáy.

    🔴 VÌ SAO ĐỔI KHỎI "3 VÒNG TRÒN + NHÃN DƯỚI" (user chốt 2026-08-17, thẻ 05:
    *"những ảnh kiểu này trình bày kiểu khác đi"*): vòng tròn `r=92` + nhãn chỉ cao ~250px,
    trong band 522px ⇒ lấp **45%**, phần trống dồn thành hai dải nhìn rỗng. `zu_fit` phóng
    được tối đa ×1,20 vì trần là BỀ NGANG (3 vòng + 2 khe 104px đã gần hết khe 965px)
    — tức không thể chữa bằng cách phóng, phải đổi HÌNH: hộp **DỌC** ăn chiều cao mà không
    ăn thêm bề ngang ⇒ cùng 3 vật, lấp **~84%** band.
    📐 Số đo: 3×248 + 2×104 = 952 ≤ 965 (khe an toàn giữa hai nhân vật). Nhãn 5 ký tự
    được font (248−44)/5 = 41px, còn trên sàn 34px của tệp 45+."""
    ns = [N(f"c{i}", "group", [0.0, 0.42], w=248, h=430, icon=ic, foot=lab, iconsize=190,
            fix=True)
          for i, (ic, lab) in enumerate(items)]
    ROW(ns, 0.42, mingap=104)
    ns.append(N("x", "label", [0.50, 0.92], label=close, lw=560))
    return C(match, "zu", title=title, nodes=ns, left=left, right=right)


# ── thẻ 4 Ô: đếm được mình đang ở lần viết lại thứ mấy ─────────────────────────
def slots(match, title, filled, left="sensei_present", right="kikite_listen"):
    """`filled` = list 4 phần tử; None = ô còn trống (nét đứt)."""
    # 🔴 `s=0.78` bắt buộc: 4 hộp `label` cỡ thường (lw 250) rộng 290px, 4 cái là 1.160px
    # trong khe 950px ⇒ gate báo CHỒNG NHAU + ô thứ 4 ĐỤNG NHÂN VẬT (dính ở thẻ 65).
    # 🔴 LƯỚI 2×2, KHÔNG PHẢI 1 HÀNG 4 Ô — tính bằng máy, không chọn bằng mắt:
    # 4 hộp trên một hàng thì `hw ≤ 117px` ⇒ `s ≤ 0,63` ⇒ **font 30px**. Tệp 45+ là tệp mất
    # chữ trước tiên, nên đổi sang 2×2 để font về **46px (+53%)**. Thứ tự đọc do TIÊU ĐỀ chở
    # (「4回、書き直しました」) + mũi tên khuỷu nối hàng trên xuống hàng dưới.
    ns = []
    for i, v in enumerate(filled):
        # khoảng dọc siết lại (0,18/0,62 → 0,26/0,60): hai hàng cách xa quá thì giữa bảng hở
        # một dải trống, và mũi tên khuỷu phải băng qua nó — user bắt được ở thẻ 65.
        # 0,20/0,64 — đo bằng máy: elbow 3 đoạn cần khe dọc ≥ 54px sau khi trừ nhãn hai đầu;
        # 0,26/0,60 chỉ cho 218px thô ⇒ đoạn ngang cắt qua chữ 「1回目」「2回目」 (gate bắt).
        # 0,12/0,64 — GIÃN TỪNG khe dọc: elbow 3 đoạn cần **~70px tự do** (mỗi nửa ≥ 26px cho
        # đầu mũi), không phải 54px như gate đang đòi — ở 54px nó ra MŨI TÊN CỤT (soi 1:1 thấy
        # đầu mũi quay ngang, mất đoạn xuống). Lấy chỗ từ khe TRÊN (0,18→0,12), không lấy từ `cap`
        # (2026-08-17): hàng 2 và dòng `cap` cùng bị kẹp cao lên 14px nên dính nhau (gate báo
        # giao −2px). Nới KHE GIỮA HAI HÀNG chứ đừng nới `cap` xuống — `cap` đang ở đáy rồi.
        # 🔴 HÀNG TRÊN phải nằm DƯỚI đỉnh nhân vật (y≥368) — nếu không, `_zu_place` cho nó
        # dùng TRỌN bề ngang card (312–1608) còn hàng dưới bị bó vào khe giữa hai người
        # (540–1505) ⇒ cùng `at[0]` mà ra hai khung khác nhau, mũi tên hàng trên 338px
        # hàng dưới 112px. `at[1]=0,17` là mốc tối thiểu đo được để cả hai hàng cùng khung.
        x, y = (0.0, 0.87)[i % 2], (0.17, 0.60)[i // 2]
        if v is None:
            # ô CÒN TRỐNG = hộp nét đứt CÙNG BỀ NGANG với ô đã điền (không phải vòng
            # tròn nhỏ) — xem `_dash_rect` trong make_stage: cùng lưới thì cùng khuôn.
            ns.append(N(f"s{i}", "label", [x, y], dash=True, dim=True, bw=300,
                        label=f"{i+1}回目", lw=250, fix=True))
        else:
            ns.append(N(f"s{i}", "label", [x, y], label=v, lw=250, bw=300, fix=True,
                        under=(i == max(j for j, w in enumerate(filled) if w))))
    ns.append(N("cap", "label", [0.50, 0.99], label="通帳に入る、あの1つの数字", lw=580,
                fix=True))
    return C(match, "zu", title=title, nodes=ns,
             edges=[E("s0", "s1", "arrow", tone="amber", w=11),
                    E("s1", "s2", "elbow", tone="amber", w=9),
                    E("s2", "s3", "arrow", tone="amber", w=11)],
             left=left, right=right)


def two_ways(match, title, l_head, l_icon, r_head, r_hero, r_foot, close,
             close_icon="money_pouch", left="sensei_serious", right="kikite_worried"):
    """HAI LỐI + BANNER CHỐT — khuôn của frame mẫu 「あとから戻る。でも、その日は全額」.

    Hai `group` lớn cạnh nhau, mũi tên navy ở giữa, dải vàng nhạt ở đáy chở câu chốt.
    Đây là khuôn NẶNG NHẤT về mặt hình: một thẻ nói được cả cơ chế lẫn cảm xúc."""
    return C(match, "zu", title=title, nodes=[
        N("L", "group", [0.16, 0.34], w=386, h=330, tone="ink", head=l_head,
          icon=l_icon, iconsize=165, fix=True),
        N("R", "group", [0.84, 0.34], w=386, h=330, tone="ink", head=r_head,
          hero=r_hero, foot=r_foot, under=True, fix=True),
        N("B", "banner", [0.50, 0.97], w=950, icon=close_icon, label=close, fix=True)],
        edges=[E("L", "R", "arrow", tone="ink", w=18)], left=left, right=right)


def one_to_n(match, title, big, big_icon, items, close, left="sensei_point",
             right="kikite_think"):
    """MỘT → NHIỀU: hộp navy lớn bên trái, N hộp viền VÀNG bên phải, banner viền navy đáy.
    Khuôn của frame mẫu 「期限は1つ、表の中身を変えるものが3つ」."""
    # `fix=True` = "hàng này khuôn đã xếp rồi" → `polish()` bỏ qua. Không có cờ này thì
    # polish chạy `zu_row` LẦN HAI với mingap 104 lên cả 4 hộp ⇒ thu nhỏ ×0.84 ⇒ chữ tràn.
    L = ROW([N("L", "group", None, w=230, h=300, tone="ink", head=big, icon=big_icon,
               iconsize=140, fix=True)], 0.40, 0.0, 0.17)
    R = ROW([N(f"i{k}", "group", None, w=196, h=300, tone="amber", head=h, icon=ic,
               iconsize=100, fix=True) for k, (h, ic) in enumerate(items)],
            0.40, 0.38, 1.0, mingap=26)
    return C(match, "zu", title=title,
             nodes=[*L, *R, N("B", "banner", [0.50, 0.99], w=950, tone="ink", label=close, fix=True)],
             edges=[E("L", "i0", "arrow", tone="ink", w=16)], left=left, right=right)


def chain(match, title, steps, chip=None, wrong=None, close=None, left="sensei_caution",
          right="kikite_nod"):
    """CHUỖI NGANG + (tuỳ chọn) LỐI SAI VÒNG DƯỚI CÓ ✗ ĐỎ + chip vàng góc.
    Khuôn của frame mẫu 「5日 ＝ 扶養の届出」. `wrong=(id_từ, id_đến)`."""
    ns = ROW([N(f"n{k}", "circle", None, icon=ic, label=lb, fix=True,
                **({"tone": "amber"} if am else {}))
              for k, (ic, lb, am) in enumerate(steps)], 0.44, mingap=104)
    if chip:
        ns = [N("chip", "chip", [0.02, 0.02], label=chip, spark=True, fix=True)] + ns
    eg = [E(f"n{k}", f"n{k+1}", "arrow", tone="ink", w=16) for k in range(len(steps) - 1)]
    if wrong:
        eg.append(E(wrong[0], wrong[1], "arc", tone="ink", x=True, drop=200))
    if close:
        ns = ns + [N("cl", "label", [0.50, 0.99], label=close, lw=560)]
    return C(match, "zu", title=title, nodes=ns, edges=eg, left=left, right=right)


def polish(cards):
    """Áp khuôn của 4 frame mẫu cho **MỌI thẻ hợp** — bằng MÁY, không sửa tay 54 thẻ.

    🔴 user chốt 2026-08-17: *"áp cho tất cả thẻ hợp"*. Sửa tay từng thẻ vừa lâu vừa lệch
    tay nhau; hai phép biến đổi dưới đây thuần hình học nên áp được đại trà mà không đổi
    nội dung một chữ:

    ① **`label` nằm ở ĐÁY → `banner`.** Frame mẫu nào cũng có dải chốt ở đáy; ta đang vẽ nó
       bằng một hộp chữ nhỏ lệch giữa. Đổi sang `banner` là được nền vàng nhạt full-width +
       gạch chân vàng + icon — cùng nội dung, nặng hình hơn nhiều.
    ② **Hàng ≥3 vật cùng cao độ → chạy `zu_row`.** Tự chia gap bằng nhau theo bề rộng THẬT.
       `mingap` chọn theo việc hàng đó **có mũi tên nối liền hay không** (104 vs 40) — đây là
       đúng con số mà gate mũi-tên-teo đòi, nên không phải chỉnh lại lần nữa.

    ⚠️ CỐ Ý KHÔNG đổi: thẻ `slots` (lưới 2×2) và thẻ `fan` (toả 2 lối) — hàng của chúng chỉ
    có ≤2 vật mỗi cao độ nên tự động bị bỏ qua, không cần ngoại lệ tay.
    """
    nb = nr = 0
    for c in cards:
        v = c["stage"]
        if v.get("layout") != "zu":
            continue
        ns = v["nodes"]
        for n in ns:
            if n["kind"] == "label" and n["at"][1] >= 0.85 and not n.get("hero"):
                n.update(kind="banner", at=[0.50, 0.99], w=950)
                n.pop("lw", None)
                nb += 1
        cs = [n for n in ns if n["kind"] in ("circle", "mark", "icon", "oval", "group")]
        rows = {}
        for n in cs:
            rows.setdefault(round(n["at"][1], 2), []).append(n)
        for y, grp in rows.items():
            if len(grp) < 3:
                continue
            if any(n.get("fix") for n in grp):
                continue                       # hàng do khuôn helper xếp — đừng xếp lại
            ids = {n["id"] for n in grp}
            linked = any(e["from"] in ids and e["to"] in ids for e in v.get("edges", []))
            ROW(grp, y, mingap=104 if linked else 40)
            nr += 1
    # ⛔ BƯỚC ③ "CÂN ĐỐI DỌC" CỦA POLISH — ĐÃ BỎ 2026-08-17, CHUYỂN VÀO TOOL (`zu_fit`).
    # 🔴 Vì sao phải bỏ, không phải chỉ sửa: nó và `zu_fit` làm **CÙNG MỘT VIỆC bằng HAI BỘ
    # HẰNG SỐ KHÁC NHAU** — polish chia lưới theo phân số `at[1]` (đoán nửa banner = 0,115),
    # `zu_fit` chia theo PIXEL THẬT (đo `_zu_box`, biết lề kẹp của `_zu_place`). Hai tầng cùng
    # ghi `at[1]` thì tầng sau đè tầng trước, và mỗi lần đổi lề đáy trong tool là lại sinh lỗi
    # ở tầng builder: đúng như vậy — nới lề 26 → 44px làm thẻ 30 báo CHỒNG NHAU 382×5px, vì
    # polish đã đóng đinh `b` ở `at[1]=0,766` theo lề CŨ.
    # ⇒ Cân dọc là việc của TOOL (nó biết cỡ thật của từng kind + biết lề kẹp). Builder chỉ lo
    # NỘI DUNG và những khuôn mà khoảng dọc CHÍNH LÀ nghĩa (`fix`). Cùng bài học với `zu_check`:
    # công thức hình học ở một chỗ duy nhất.
    print(f"[polish] {nb} label đáy → banner  ·  {nr} hàng ≥3 vật → zu_row  ·  "
          f"cân dọc: do zu_fit của tool")
    return cards


CARDS = [
    # ═════════════════════════ COLD OPEN
    C("「悲しむ前に、書類だった", "art",
      title="「悲しむ前に、書類だったんですよ」",
      img="art_tsucho_tsuuchi.png", fly="up",
      cap="仙台・佐藤さん（66）。市役所、年金事務所、銀行",
      left="sensei_serious", right="kikite_listen"),

    C("市役所、年金事務所、銀行", "zu", title="泣いたのは、そのあとでした",
      nodes=[N("a", "circle", [0.10, 0.36], icon="cityhall", label="市役所"),
             N("b", "circle", [0.44, 0.36], icon="nenkin_techo", label="年金事務所"),
             N("c", "circle", [0.78, 0.36], icon="bank", label="銀行"),
             N("d", "label", [0.52, 0.92], label="三か所を回って、そのあと")],
      edges=[E("a", "b"), E("b", "c")],
      left="sensei_serious", right="kikite_down"),

    # 🔴 HỢP LƯU PHẢI ĐỐI XỨNG, nếu không hai mũi tên dài khác nhau (user bắt 2026-08-17:
    # *"2 cái mũi tên dài bằng nhau đi và cái ở giữa to ra"*). Điều kiện đủ, tính được:
    #   ① hai nguồn CÙNG `at[0]`  ② đích ở ĐÚNG trung điểm dọc của hai nguồn
    # ⇒ hai vector là ảnh gương của nhau ⇒ cùng độ dài, và `_zu_trim` cắt bằng nhau vì hai
    # nguồn cùng kind/cùng `s`. Bản cũ để 0,10/0,90/0,56: đích lệch khỏi trung điểm, cộng thêm
    # `zu_fit` thoát sớm (`bot < top` vì hai vòng tròn ăn gần hết band) ⇒ lệch hẳn.
    # `fix=True` cả ba: khoảng dọc ở đây CHÍNH LÀ đường mũi tên, không cho tầng nào xếp lại.
    # `hero` cho đích: nó là tổng của hai nhánh, phải to hơn hai nguồn mới đọc ra vai "kết quả".
    C("ご夫婦で、年金が月に25万円", "zu", title="ご夫婦で、年金が月に25万円",
      nodes=[N("h", "circle", [0.12, 0.162], icon="person", label="ご主人\n16万円", fix=True),
             N("w", "circle", [0.12, 0.645], icon="couple_senior", label="奥さま\n9万円",
               fix=True),
             N("t", "label", [0.78, 0.4035], label="世帯 25万円", lw=460, hero=True,
               under=True, fix=True)],
      edges=[E("h", "t", "arrow"), E("w", "t", "arrow")],
      left="sensei_explain", right="kikite_listen"),

    # 🔴 ĐỔI CÁCH TRÌNH BÀY, không chỉ dời node (user 2026-08-17: *"không sắp xếp lại bố cục cho
    # cân được à. Không được thì mày dùng cách khác chứ"*). Bản cũ là hợp lưu 2→1 với `at` gõ tay:
    # hai hộp trái ở 0,30/0,80, kết quả ở 0,74/0,55 ⇒ khối nội dung nằm CHÉO, trống hẳn góc
    # trên-trái và dưới-phải, mà `zu_fit` không cứu được vì cả 4 node đều `fix` (đúng — khoảng dọc
    # ở đây là đường mũi tên).
    # Cách mới: **cột trái = một PHÉP CỘNG hiện ra** (9万 ＋ 12万) → kết quả là số HERO bên phải.
    #  · dấu `＋` giữa hai hộp: vừa lấp khe dọc trống, vừa nói đúng cái người xem đang cộng nhầm
    #    — thẻ này là "điều nhiều người tưởng", nên phép cộng phải hiện ra mới có gì để phá.
    #  · `hero` cho 21万円: nó là ĐÁP ÁN của thẻ, phải to nhất (bản cũ nhỏ bằng hai hộp trái).
    #  · dải kết ở đáy: lấp khoảng trống dưới VÀ chốt đây là "thói tưởng", không thêm claim mới.
    C("多くの方は、21万円くらい", "zu", title="多くの方が、こう思っておられます",
      nodes=[N("w", "label", [0.10, 0.24], label="自分の9万円", lw=340, bw=396,
               fix=True),
             N("pl", "label", [0.20, 0.47], label="＋", lw=120, hero=True, frame=False,
               fix=True),
             N("p", "label", [0.10, 0.71], label="4分の3で12万円", lw=340, bw=396,
               fix=True),
             N("t", "label", [0.80, 0.47], label="21万円", lw=280, hero=True, under=True,
               fix=True),
             N("bb", "bubble", [0.78, 0.12], label="このまま乗る、\nと思われがちです", tail="down",
               lw=420, fix=True),
             N("x", "label", [0.50, 0.97], label="いちばん多い、思い違いです", lw=560, fix=True)],
      edges=[E("w", "t"), E("p", "t")],
      left="sensei_explain", right="kikite_nod"),

    C("違うんです", "zu", title="入るのは、13万9千円",
      # 🔴 Đây là con số ĐẮT NHẤT của cả video (cú đâm của cold open) ⇒ `hero` + `spark`.
      # Bỏ icon giữa: hero rộng 390px nên khe không còn chỗ, nhét vào là gate báo chồng.
      nodes=[N("a", "label", [0.13, 0.50], label="世帯 25万円", lw=330),
             N("b", "label", [0.80, 0.50], label="13万9千円", lw=330, hero=True,
               under=True, spark=True),
             N("bb", "bubble", [0.52, 0.12], label="およそ、半分です", tail="down", lw=380),
             N("cl", "label", [0.50, 0.99], label="減るのは、月11万1千円", lw=520)],
      edges=[E("a", "b", "arrow")],
      left="sensei_serious", right="kikite_surprised"),

    cols3("そして、家賃も、電気代も", "半分にならないもの",
          [("house", "家賃"), ("receipt", "電気代"), ("form", "固定資産税")],
          "どれも、同じ額で届きます"),

    C("65歳より前におひとりになられた場合は", "zu", title="この額に、上乗せがつく方とつかない方",
      # `at[1]` ở thẻ này ĐÓNG BĂNG (`fix`): đây là sơ đồ TOẢ 2 LỐI, khoảng dọc giữa `src` và
      # `hub` CHÍNH LÀ chỗ mũi tên đi. Để `polish` cân đối dọc thì hai node dồn lại còn 24px
      # ⇒ mũi tên teo thành dấu chấm (gate bắt được ngay).
      nodes=[N("hub", "icon", [0.50, 0.32], icon="envelope_open", s=1.0, spark=True, fix=True),
             N("l", "circle", [0.10, 0.12], icon="money_pouch", label="月5万3千円", fix=True),
             N("r", "circle", [0.90, 0.12], icon="warning", label="1円も\nつかない", fix=True),
             N("src", "label", [0.50, 0.99], label="65歳より前におひとりに", lw=520, fix=True)],
      edges=[E("src", "hub", "arrow"), E("hub", "l", "fan"), E("hub", "r", "fan")],
      left="sensei_caution", right="kikite_surprised"),

    C("分かれ目は、ご主人の厚生年金が20年", "big", title="分かれ目は、ここだけです",
      value="240", unit="か月", tone="bad",
      cap="ご主人の厚生年金が20年あるかどうか",
      left="sensei_serious", right="kikite_surprised"),

    slots("今日は、通帳に入るこの1つの数字を", "この1つの数字を、4回、書き直します",
          [None, None, None, None], left="sensei_present", right="kikite_listen"),

    # ═════════════════════════ 第1章 — 質問をされたのは奥さま
    C("大阪の山田さんご夫妻", "compare", title="モニター・山田さんご夫妻（大阪）",
      panels=[{"icon": "avatar_yamada", "cap": "ご主人 67歳" + NL + "再雇用で、まだお勤め"},
              {"icon": "couple", "cap": "奥さま 65歳" + NL + "パートを少し"}],
      rows=["年金は月16万円", "年金は月9万円"],
      left="sensei_present", right="kikite_listen"),

    C("「どっちかが先に逝ったら", "zu",
      # 🔴 HAI VẬT CÙNG HÀNG PHẢI CÙNG KIND. Bản đầu để `icon` (vật trần) cạnh `circle`
      # (vật trong đĩa xanh) ⇒ một bên có đĩa một bên không, đọc ra "hai loại thứ khác nhau"
      # trong khi ý là hai chi tiết của CÙNG một căn bếp. Và `ROW` để hai vật tự cân đối
      # xứng quanh tâm khe — gõ `at[0]` tay thì tâm hàng lệch sang phải (đo được: 0,53).
      nodes=[N("bb", "bubble", [0.46, 0.12],
               label="どっちかが先に逝ったら、\nこの25万はどうなるんやろね", tail="down", lw=620),
             *ROW([N("k", "circle", [0.0, 0.62], icon="house", label="大阪のお宅"),
                   N("c", "circle", [0.0, 0.62], icon="calendar", label="通院日の赤丸")],
                  0.62, mingap=104)],
      left="sensei_explain", right="josei_worried"),

    C("ご主人は、何と答えられたか", "zu", title="ご主人の答え",
      # 🔴 Bong bóng `tail="left"` phải NGANG HÀNG với người nó thuộc về. Bản đầu đặt lệch
      # 0,08 (0,36 vs 0,44) ⇒ `_zu_rows` xếp thành HAI hàng, đuôi bong bóng chỉ vào chỗ trống.
      nodes=[N("p", "circle", [0.20, 0.42], icon="person", s=1.1, label="ご主人"),
             N("bb", "bubble", [0.72, 0.42], label="わからん", tail="left", lw=300),
             N("x", "label", [0.50, 0.92], label="たいていのお宅が、そうです", lw=540)],
      left="sensei_reassure", right="kikite_nod"),

    C("今日は、その質問に答えます", "big", title="今日は、その質問に答えます",
      value="奥さまの通帳", tone="amber",
      cap="数字は山田さんの記録での話です。ご自分の家の額は、あとで必ずご確認ください",
      left="sensei_present", right="kikite_nod"),

    C("まず、多くの方が思っている額から", "zu", title="出発点は、21万円",
      nodes=[N("w", "label", [0.12, 0.28], label="奥さま 9万円", lw=320),
             N("p", "label", [0.12, 0.78], label="4分の3 12万円", lw=340),
             N("t", "label", [0.74, 0.53], label="21万円", lw=320, hero=True, under=True),
             # 🔴 Đuôi bong bóng phải CHẠM hero (≤140px). 0,03 để nó cách 145px = đuôi chỉ vào
             # không khí; hạ xuống 0,12 thì đuôi cắm đúng vào 21万円.
             N("bb", "bubble", [0.74, 0.12], label="ここから、書き直します", tail="down", lw=470)],
      edges=[E("w", "t"), E("p", "t")],
      left="sensei_present", right="kikite_listen"),

    slots("ここから、4回、書き直します", "1回目に、入ります",
          ["21万円", None, None, None], left="sensei_point", right="kikite_think"),

    # ═════════════════════════ 書き直し① 12万 → 6万7千
    C("日本年金機構の「遺族年金ガイド", "art", title="原典：日本年金機構『遺族年金ガイド』6ページ",
      img="genten_01_kikou_p6.png", fly="up",
      cap="赤で囲んだところ ＝「報酬比例部分の4分の3」",
      left="sensei_point", right="kikite_think"),

    C("つまり、会社勤めで積み上げた", "zu", title="報酬比例部分とは",
      nodes=[N("a", "circle", [0.22, 0.42], icon="person", label="会社勤めで\n積み上げた分"),
             N("b", "label", [0.70, 0.42], label="報酬比例部分", lw=430, hero=True,
               under=True),
             N("cl", "label", [0.50, 0.99], label="四分の三がかかるのは、ここだけ", lw=560)],
      edges=[E("a", "b", "arrow", label="ここだけ")],
      left="sensei_explain", right="kikite_nod"),

    C("およそ7万円が、老齢基礎年金", "zu", title="ご主人の16万円を、2つに分ける",
      nodes=[N("t", "label", [0.14, 0.50], label="16万円", lw=260),
             N("a", "circle", [0.68, 0.18], icon="nenkin_techo", label="老齢基礎\nおよそ7万円"),
             N("b", "circle", [0.68, 0.82], icon="chart_up", label="報酬比例\nおよそ9万円")],
      edges=[E("t", "a", "arrow"), E("t", "b", "arrow")],
      left="sensei_explain", right="kikite_listen"),

    C("4分の3がかかるのは、この9万円", "zu", title="4分の3がかかるのは、片方だけ",
      nodes=[N("a", "circle", [0.16, 0.14], icon="nenkin_techo", label="老齢基礎 7万円",
               dim=True, dash=True, cross=True, s=0.88),
             # 🔴 `b` và `r` CÙNG HÀNG: mũi tên ĐƠN không được chạy chéo qua giữa bảng (bản cũ
             # dx=570 dy=142 ⇒ bay qua đúng vùng trắng nhất, sinh 2 góc rỗng).
             # 🔴 `a` (bị gạch ✗) vào MẠCH bằng edge `dot` + `x`: nó là "lối KHÔNG đi được", phải
             # thấy nó cũng trỏ về `r` mới đọc ra "chỉ một bên chịu 4 phần 3".
             N("b", "circle", [0.16, 0.62], icon="chart_up", label="報酬比例 9万円"),
             N("r", "label", [0.76, 0.62], label="4分の3", lw=300, hero=True, under=True),
             N("bb", "bubble", [0.76, 0.30], label="基礎年金には、\nそもそもありません",
               tail="down", lw=470)],
      edges=[E("b", "r", "arrow"), E("a", "r", "dot", tone="grey", x=True)],
      left="sensei_point", right="kikite_surprised"),

    spine("だから、12万円が、6万7千円", "書き直し① 4分の3がかかる場所",
          "月12万円", "6万7千円", "かかるのは、\n報酬比例部分だけ",
          "基礎年金には、かかりません",
          left="sensei_present", right="kikite_surprised"),

    # ═════════════════════════ 書き直し② 6万7千 → 4万8千
    C("奥さま自身の年金と、重ならない", "zu", title="奥さま自身の年金と、重なりません",
      nodes=[N("a", "circle", [0.24, 0.40], icon="money_pouch", label="遺族厚生\n6万7千円"),
             N("b", "circle", [0.70, 0.40], icon="nenkin_techo", label="自分の老齢厚生\n1万8千円",
               dim=True),
             N("x", "label", [0.48, 0.92], label="重ねて受け取ることは、できません", lw=620)],
      edges=[E("a", "b", "dot", tone="grey")],
      left="sensei_explain", right="kikite_think"),

    C("同じガイドの7ページ", "art", title="原典：同ガイド 7ページ（65歳以降の調整）",
      img="genten_03_kikou_p7.png", fly="up",
      cap="赤で囲んだところ ＝ 2つの式と「支給停止」",
      left="sensei_point", right="kikite_think"),

    C("つまり、6万7千円のうち1万8千円は", "zu", title="1万8千円は、入れ替わるだけ",
      nodes=[N("a", "label", [0.14, 0.28], label="6万7千円", lw=300),
             N("b", "circle", [0.52, 0.62], icon="scale", label="1万8千円は\n入れ替わり"),
             N("c", "label", [0.86, 0.28], label="4万8千円", lw=340, hero=True, under=True)],
      edges=[E("a", "c", "arrow"), E("b", "c", "dot", tone="grey")],
      left="sensei_explain", right="kikite_surprised"),

    spine("6万7千円が、4万8千円になりました", "書き直し② 自分の年金は支給停止",
          "6万7千円", "4万8千円", "1万8千円は、\nもともと受け取っていた分",
          "引かれるのは、1万8千円",
          left="sensei_serious", right="kikite_down"),

    spine("これで、奥さまの通帳は、月9万円から", "通帳に入る額は、こうなります",
          "月9万円", "13万9千円", "思っていた21万円では、\nありません",
          "増えるのは、月4万9千円",
          left="sensei_present", right="kikite_surprised"),

    C("固定資産税の納付書は", "zu", title="収入は半分。では、出ていくほうは",
      nodes=[N("a", "circle", [0.10, 0.32], icon="form", label="固定資産税"),
             N("b", "circle", [0.36, 0.32], icon="house", label="電気の\n基本料金"),
             N("c", "circle", [0.62, 0.32], icon="wallet_open", label="水道・下水"),
             N("d", "circle", [0.88, 0.32], icon="phone", label="受信料"),
             N("x", "label", [0.50, 0.90], label="ご主人が亡くなっても、同じ額", lw=580)],
      left="sensei_caution", right="kikite_worried"),

    cols3("町内会費も、お墓の管理料も", "つづきます",
          [("couple", "町内会費"), ("hanko", "お墓の\n管理料"),
           ("postcard", "ご近所への\nお付き合い")],
          "急にやめられるものではありません",
          left="sensei_serious", right="josei_down"),

    C("一人になったから半分になる", "zu", title="はっきり減るのは、食費くらい",
      nodes=[N("a", "circle", [0.24, 0.42], icon="money_pouch", label="お米を炊く量が\n少し減る"),
             N("b", "circle", [0.72, 0.42], icon="chart_down", label="それくらい", s=1.35, dim=True)],
      edges=[E("a", "b", "line", tone="ink")],
      left="sensei_explain", right="kikite_nod"),

    two_ways("収入だけが、半分になる", "収入は半分。出ていくほうは、そのまま",
             "入ってくるお金", "passbook",
             "出ていくお金", "変わらず", "同じ額で届く",
             "痛いのは、収入だけが半分になること",
             left="sensei_serious", right="kikite_worried"),

    # ═════════════════════════ 計算タイム
    C("ここで、計算タイムです", "timeline", title="計算タイム：15年で、いくらずれるか",
      **{"from": "ご主人 70歳", "to": "奥さま 85歳"},
      label="15年", prog=0.55,
      steps=[["clock", "70歳"], ["calendar", "15年間"], ["person", "85歳"]],
      left="sensei_present", right="kikite_listen"),

    # ⛔ ĐÃ THỬ `two_ways` rồi TRẢ VỀ: khuôn đó có MỘT mũi tên L→R nên nó khẳng định
    # "13万9千 dẫn tới 3千780万" — ngược logic. Thẻ này là HAI TIỀN ĐỀ SONG SONG (không ai
    # dẫn tới ai), nên phải là 2 nhánh rời. Bài học: khuôn đẹp mà sai hướng nhân quả thì bỏ.
    C("月13万9千円だと、15年で", "zu", title="15年で、受け取る総額",
      nodes=[N("a", "label", [0.14, 0.16], label="13万9千円", lw=340, bw=400),
             N("b", "label", [0.14, 0.60], label="21万円の前提", lw=340, bw=400),
             N("c", "circle", [0.68, 0.14], icon="passbook_open", label="2千502万円"),
             N("d", "circle", [0.68, 0.58], icon="calc", label="3千780万円", dim=True),
             N("B", "banner", [0.50, 0.99], w=950, icon="calc",
               label="差は、およそ1千278万円")],
      edges=[E("a", "c", "arrow"), E("b", "d", "line", tone="grey")],
      left="sensei_explain", right="kikite_think"),

    C("差は、およそ1千278万円", "big", title="差は、これだけです",
      value="1278", unit="万円", tone="bad",
      cap="老後の計画を、1千300万円ずれたまま立てていたことになります",
      left="sensei_serious", right="kikite_surprised"),

    cols3("家の修繕や、入院や、施設に入る", "その差は、どこから出ていくのか",
          [("house", "家の修繕"), ("hospital", "入院"), ("cityhall", "施設")],
          "ぜんぶ、この行から出ます",
          left="sensei_serious", right="kikite_down"),

    C("この数字を、一度だけ、ご夫婦で", "zu", title="いまの暮らしは、変えなくていい",
      nodes=[N("a", "circle", [0.22, 0.42], icon="couple_senior", label="一度だけ、\nご夫婦で見る"),
             N("b", "label", [0.74, 0.42], label="決めておけること", lw=430, hero=True,
               under=True),
             N("cl", "label", [0.50, 0.99], label="変えるのでなく、知っておくこと", lw=560)],
      edges=[E("a", "b", "arrow")],
      left="sensei_reassure", right="kikite_relieved"),

    C("どちらの通帳から光熱費を", "check", title="口に出して、確かめておくこと",
      ok=[["passbook", "光熱費は、どちらの通帳から"],
          ["lock", "その通帳の場所を、お互い知っているか"],
          ["postcard", "年金の振込通知書は、どこか"],
          ["hospital", "入院のお金は、どちらの口座から"]],
      left="sensei_point", right="kikite_nod"),

    C("紙に書き出す必要も、ありません", "zu", title="紙に書き出す必要も、ありません",
      nodes=[N("a", "icon", [0.24, 0.46], icon="form", s=1.0, cross=True),
             N("b", "circle", [0.72, 0.44], icon="couple_senior", label="一度、口に出す"),
             N("bb", "bubble", [0.72, 0.02], label="それだけです", tail="down", lw=320)],
      edges=[E("a", "b", "arrow")],
      left="sensei_reassure", right="kikite_relieved"),

    # ═════════════════════════ CTA
    slots("ここまでで、まだ2回です", "ここまでで、まだ2回。次がいちばん大きい",
          ["21万円", "6万7千円", None, None],
          left="sensei_point", right="kikite_surprised"),

    C("ここで、ひとつだけお願いです", "source", title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    C("皆さまの声が、次の研究テーマ", "zu", title="皆さまの声が、次の研究テーマになります",
      nodes=[N("a", "circle", [0.18, 0.42], icon="phone", label="コメント"),
             N("b", "circle", [0.76, 0.42], icon="magnifier", label="次の研究")],
      edges=[E("a", "b", "arrow", label="そのまま")],
      left="sensei_present", right="kikite_nod"),

    # ═════════════════════════ 書き直し③ 240か月の線
    C("上乗せがあります", "zu", title="上乗せがあります",
      nodes=[N("a", "label", [0.50, 0.22], label="中高齢寡婦加算", lw=560, under=True),
             N("b", "circle", [0.24, 0.76], icon="money_pouch", label="月5万3千円"),
             N("c", "circle", [0.74, 0.76], icon="hourglass", label="65歳に\nなるまで")],
      edges=[E("a", "b", "arrow"), E("a", "c", "arrow")],
      left="sensei_present", right="kikite_listen"),

    C("ご主人が亡くなったとき、奥さまが40歳以上", "check", title="上乗せがつく条件",
      ok=[["person", "奥さまが40歳以上65歳未満"],
          ["couple", "18歳年度末までのお子さんがいない"]],
      no=[["clock", "65歳になると、そこで終わります"]],
      left="sensei_explain", right="kikite_think"),

    C("65歳になるまで、年63万5千500円", "big", title="令和8年度の額",
      value="63万5千500円", tone="amber", cap="月にすると、5万3千円ほどです",
      left="sensei_present", right="kikite_surprised"),

    C("65歳より前におひとりになられた奥さま", "zu", title="通帳に入る額そのものが、変わります",
      # 🔴 label–icon–label trên MỘT hàng không lọt khe 950px (gate báo mũi tên teo 24px).
      # Bỏ icon giữa, hạ xuống góc dưới-trái — đúng khuôn `spine()`.
      nodes=[N("a", "label", [0.13, 0.46], label="13万9千円", lw=300),
             N("b", "label", [0.82, 0.46], label="＋5万3千円", lw=320, hero=True, under=True),
             N("bb", "bubble", [0.52, 0.04], label="65歳より前に\nおひとりになられた場合",
               tail="down", lw=470),
             N("cl", "label", [0.50, 0.99], label="合わせて、月19万2千円", lw=520)],
      edges=[E("a", "b", "arrow")],
      left="sensei_explain", right="kikite_nod"),

    C("千葉の松本さん", "compare", title="モニター・松本さん（千葉）",
      panels=[{"icon": "avatar_matsumoto", "cap": "60歳" + NL + "この春、定年"},
              {"icon": "couple", "cap": "奥さま 55歳" + NL + "パートで働く"}],
      rows=["以前の研究に出てこられた方", "65歳まで、あと10年"],
      left="sensei_present", right="kikite_listen"),

    C("松本さんの奥さまなら、65歳になるまでの10年間", "zu", title="松本さんの奥さまなら",
      nodes=[N("a", "label", [0.13, 0.58], label="月5万3千円", lw=320),
             N("c", "label", [0.82, 0.58], label="635万5千円", lw=320, hero=True, under=True),
             # 🔴 「10年間」 là HỆ SỐ của phép nhân, chỗ đúng của nó là NHÃN EDGE — chứ không phải
             # một vòng tròn nằm lẻ ở góc dưới-trái, không nối vào mạch nào (gate ⑬).
             # KHỐI THỨ BA (luật §2 của `stage-zu-layout.md`): hai khối thì khe giữa luôn ~200px.
             N("bb", "bubble", [0.82, 0.12], label="10年で、これだけに", tail="down", lw=430),
             N("cl", "label", [0.50, 0.99], label="65歳になるまでの10年間", lw=560)],
      edges=[E("a", "c", "arrow", label="×10年")],
      left="sensei_present", right="kikite_surprised"),

    C("ところが、ここに条件があります", "art", title="原典：同ガイド 7ページ【ご注意ください】",
      img="genten_02_kikou_p7.png", fly="up",
      cap="赤で囲んだところ ＝「加入期間が20年以上なければ」",
      left="sensei_caution", right="kikite_worried"),

    C("たとえば、会社勤めが18年で", "zu", title="2年、足りないだけで",
      nodes=[N("a", "circle", [0.14, 0.20], icon="person", label="会社勤め\n18年"),
             N("g", "panel", [0.60, 0.18], icon="scale", label="240か月の線"),
                          N("y", "mark", [0.28, 0.88], label="635万5千円", tone="grey", dim=True, lw=280),
             N("n", "mark", [0.74, 0.88], label="0円", tone="grey", lw=240)],
      edges=[E("a", "g", "line", tone="ink"),
             E("g", "y", "elbow", tone="grey"), E("g", "n", "elbow", tone="ink")],
      left="sensei_serious", right="kikite_surprised"),

    C("2年、足りないだけで", "big", title="足りなかったのは",
      value="2年", tone="bad", cap="同じ月額の年金でも、同じ年齢の奥さまでも",
      left="sensei_serious", right="josei_down"),

    C("だから、確かめるのは2つだけです", "zu", title="確かめるのは、2つだけ",
      nodes=[N("src", "circle", [0.08, 0.30], icon="docs", tone="amber"),
             N("g", "panel", [0.52, 0.30], icon="nenkin_techo", label="ねんきん定期便"),
             N("net", "circle", [0.90, 0.30], icon="magnifier", label="ねんきん\nネット"),
             N("y", "mark", [0.32, 0.78], label="20年ある", lw=250),
             N("n", "mark", [0.66, 0.78], label="20年ない", tone="grey", lw=250)],
      edges=[E("src", "g", "line", tone="ink"),
             E("net", "g", "dot", tone="grey"),
             E("g", "y", "elbow", tone="ink"), E("g", "n", "elbow", tone="grey")],
      left="sensei_point", right="kikite_nod"),

    chain("奥さまがご自分で見ることは", "記録を見られるのは、ご主人だけ",
          [("couple", "奥さま", False), ("person", "ご主人", True),
           ("nenkin_techo", "定期便", False), ("magnifier", "加入月数", True)],
          chip="20年＝240か月", wrong=("n0", "n3"),
          close="奥さまからは、確かめられません",
          left="sensei_point", right="josei_talk"),

    C("なお、はじめの佐藤さんは", "compare", title="はじめの佐藤さんは、この線にかかりませんでした",
      panels=[{"icon": "avatar_sato", "cap": "ご主人が" + NL + "在職中に亡くなられた"},
              {"icon": "scale", "cap": "別の計算に" + NL + "なります"}],
      rows=["お子さんが小学生のときでした", "上乗せも、受け取られています"],
      left="sensei_explain", right="kikite_nod"),

    C("「あのとき、誰も教えてくれん", "zu",
      nodes=[N("bb", "bubble", [0.46, 0.16],
               label="あのとき、誰も教えてくれんかったからね。\n自分で聞きに行ったの", tail="down",
               lw=700),
             N("p", "icon", [0.28, 0.68], icon="avatar_sato", s=1.49),
             N("c", "circle", [0.76, 0.66], icon="madoguchi", label="自分で、窓口へ")],
      edges=[E("p", "c", "arrow")],
      left="sensei_reassure", right="josei_nod"),

    C("「しといたほうがええよ", "zu",
      nodes=[N("bb", "bubble", [0.50, 0.30],
               label="しといたほうがええよ。\nあのとき、私は何も分からんかったから",
               tail="down", lw=740),
             N("p", "icon", [0.24, 0.80], icon="avatar_sato", s=1.82),
             N("x", "label", [0.72, 0.84], label="聞きに行った人の、ことば", lw=480)],
      left="sensei_serious", right="josei_down"),

    # ═════════════════════════ 書き直し④ 2028年の線
    C("いま「遺族年金は5年で打ち切り", "zu", title="いま、流れている言葉",
      # điện thoại là MOTIF của thẻ (tin đang lan trên mạng) ⇒ `bigicon` 300px, không phải
      # `icon` 190px lọt thỏm; và nó phải NGANG HÀNG với bong bóng để đường nét đứt không chạy
      # chéo qua bảng (gate ⑪ tính cả `dot`).
      nodes=[N("a", "bigicon", [0.18, 0.44], icon="phone", size=300),
             N("bb", "bubble", [0.70, 0.44], label="遺族年金は\n5年で打ち切り", tail="left",
               lw=400),
             N("x", "label", [0.50, 0.90], label="ご自分のことだと思われた方も", lw=580)],
      edges=[E("a", "bb", "dot", tone="grey")],
      left="sensei_caution", right="josei_worried"),

    C("2028年4月から、遺族厚生年金の男女差", "timeline", title="施行は、2028年4月",
      **{"from": "去年、成立", "to": "2028年4月"},
      label="ここから", prog=0.45,
      steps=[["form", "法律の成立"], ["calendar", "2028年4月"], ["scale", "男女差の解消"]],
      left="sensei_explain", right="kikite_listen"),

    C("厚生労働省が、わざわざ1枚", "art", title="原典：厚生労働省『指摘への考え方』",
      img="genten_04_mhlw_p1.png", fly="up",
      cap="赤で囲んだところ ＝「見直しの影響を受けない方」",
      left="sensei_point", right="kikite_think"),

    one_to_n("1つ、すでに遺族厚生年金を受給", "見直しの影響を受けない方は、3つ",
             "影響" + NL + "なし", "checklist",
             [("すでに" + NL + "受給中", "money_pouch"),
              ("60歳以降に" + NL + "受給権", "clock"),
              ("2028年に" + NL + "40歳以上", "person")],
             "いま50代・60代の女性は、全員ここに入る",
             left="sensei_explain", right="kikite_listen"),

    C("3つめを、もう一度読みます", "zu", title="3つめを、もう一度",
      nodes=[N("a", "label", [0.50, 0.24], label="2028年度に40歳以上の女性", lw=760,
               under=True),
             N("b", "circle", [0.06, 0.76], icon="couple", label="いま50代"),
             N("c", "circle", [0.94, 0.76], icon="person", label="いま60代")],
      edges=[E("b", "a", "arrow"), E("c", "a", "arrow")],
      left="sensei_point", right="kikite_nod"),

    C("5年で打ち切りになるのは、あなたでは", "big", title="ですから",
      value="あなたでは", unit="ありません", tone="ok",
      cap="新しく対象になるのは、30代の女性がごく少数です",
      left="sensei_reassure", right="kikite_relieved"),

    C("ただ、あなたの線は、別にあります", "zu", title="ただ、あなたの線は、別にあります",
      nodes=[N("a", "icon", [0.20, 0.42], icon="calendar", s=1.0, cross=True),
             N("b", "icon", [0.68, 0.44], icon="yen_coins", s=1.0, spark=True),
             N("bb", "bubble", [0.70, 0.02], label="月5万3千円の\n上乗せのほう", tail="down",
               lw=420)],
      edges=[E("a", "b", "arrow", label="5年ではなく")],
      left="sensei_caution", right="kikite_surprised"),

    C("あれが、2028年4月1日以降に", "timeline", title="25年かけて、小さくなっていきます",
      **{"from": "2028年4月1日", "to": "令和35年度"},
      label="25年かけて縮小", prog=0.78,
      steps=[["money_pouch", "いまの額"], ["chart_down", "少しずつ"], ["warning", "廃止"]],
      left="sensei_serious", right="kikite_worried"),

    two_ways("一度受け取り始めた額は、変わりません", "線の手前と、向こう",
             "いま受け取って" + NL + "おられる方", "money_pouch",
             "受け取り始めた額は", "そのまま", "65歳まで",
             "いま受け取っている奥さまは、影響を受けません", close_icon="hourglass",
             left="sensei_reassure", right="kikite_relieved"),

    spine("5年ではなく、こちらです", "書き直し④ 2028年4月1日の線",
          "5年の話", "上乗せの額", "50代・60代に効いてくるのは、\nこちらです",
          "2028年度に40歳以上なら、上乗せのほう",
          left="sensei_serious", right="kikite_nod", tone_new="bad"),

    C("それから、いい話もあります", "zu", title="いい話も、あります",
      nodes=[N("a", "icon", [0.22, 0.42], icon="wallet", s=1.0, cross=True),
             N("b", "circle", [0.70, 0.42], icon="couple_senior", label="共働きのご家庭"),
             N("bb", "bubble", [0.70, 0.02], label="年収850万円未満の\n条件がなくなります",
               tail="down", lw=480)],
      edges=[E("a", "b", "arrow")],
      left="sensei_reassure", right="kikite_relieved"),

    C("それに、いまの制度では権利が1円も", "zu", title="男性が、増える話でもあります",
      nodes=[N("a", "circle", [0.22, 0.42], icon="person", label="いまは1円もなし",
               dim=True, dash=True),
             N("b", "circle", [0.70, 0.42], icon="person", label="2028年4月から")],
      edges=[E("a", "b", "arrow", label="道が開きます")],
      left="sensei_explain", right="kikite_nod"),

    # ═════════════════════════ まとめ・研究ノート・クイズ
    slots("書き直しは、以上です", "4回、書き直しました",
          ["21万円", "6万7千円", "4万8千円", "13万9千円"],
          left="sensei_conclude", right="kikite_nod"),

    two_ways("そこに上乗せがつけば、月5万3千円", "上乗せが、つくか つかないか",
             "厚生年金が20年ある", "checklist",
             "20年ないと", "0円", "上乗せはつきません",
             "分かれ目は、240か月だけです", close_icon="scale",
             left="sensei_conclude", right="kikite_think"),

    C("大阪の山田さんの奥さまが、台所で", "zu", title="あの台所の質問に、お答えします",
      nodes=[N("bb", "bubble", [0.44, 0.12], label="この25万は\nどうなるんやろね", tail="down",
               lw=440),
             N("k", "circle", [0.20, 0.54], icon="house", label="あの台所"),
             N("ans", "label", [0.74, 0.58], label="答えは 13万9千円", lw=480, under=True),
             N("h", "label", [0.60, 0.99], label="世帯の、およそ半分", lw=460)],
      edges=[E("k", "ans", "arrow")],
      left="sensei_conclude", right="josei_nod"),

    C("それでは、今日の研究ノートです", "check", title="研究ノート（1／2）",
      ok=[["docs", "遺族厚生年金は、報酬比例部分の4分の3"],
          ["scale", "自分の老齢厚生年金は、支給停止になる"]],
      no=[["nenkin_techo", "年金の全体に、4分の3ではありません"]],
      left="sensei_conclude", right="kikite_nod"),

    C("その上乗せは、ご主人の厚生年金が20年ないと", "check", title="研究ノート（2／2）",
      ok=[["clock", "上乗せは、65歳になるまで"],
          ["person", "「5年で打ち切り」は50代60代の話ではない"]],
      no=[["warning", "ご主人の厚生年金が20年ないと、つきません"]],
      left="sensei_conclude", right="kikite_nod"),

    C("遺族年金には、税金がかかりません", "zu", title="○×クイズ 第1問",
      nodes=[N("q", "label", [0.50, 0.26], label="遺族年金に、税金は", lw=620),
             N("m", "icon", [0.28, 0.76], icon="avatar_maru", s=1.22),
             N("b", "icon", [0.72, 0.76], icon="avatar_batsu", s=1.22)],
      left="sensei_caution", right="kikite_think"),

    C("しかも、配偶者控除や扶養の判定", "check", title="第1問の答えは ○",
      ok=[["form", "所得税も、相続税も、かかりません"],
          ["calc", "「合計所得金額」にも、入りません"]],
      no=[["docs", "前回の申告書のお話と、つながります"]],
      left="sensei_present", right="kikite_relieved"),

    C("ご主人の厚生年金が15年でも", "zu", title="○×クイズ 第2問",
      nodes=[N("q", "label", [0.50, 0.24], label="15年でも、上乗せはつく", lw=680),
             N("a", "mark", [0.28, 0.74], label="15年", tone="grey", lw=240),
             N("b", "mark", [0.72, 0.74], label="20年", lw=240)],
      edges=[E("a", "b", "dot", tone="grey")],
      left="sensei_caution", right="kikite_think"),

    C("いま55歳の奥さまは、2028年の改正で", "zu", title="○×クイズ 第3問",
      nodes=[N("q", "label", [0.50, 0.26], label="55歳の奥さまは、5年で終わる", lw=740),
             N("a", "circle", [0.30, 0.76], icon="person", label="いま55歳"),
             N("b", "circle", [0.70, 0.76], icon="calendar", label="2028年度")],
      edges=[E("a", "b", "dot", tone="grey")],
      left="sensei_caution", right="josei_worried"),

    C("2028年度に40歳以上になる女性は、影響を受けません", "big", title="第3問の答えは ×",
      value="影響を", unit="受けません", tone="ok",
      cap="2028年度に40歳以上になる女性は、全員この中に入ります",
      left="sensei_reassure", right="josei_relieved"),

    cols3("だから、通帳に入る額を、いまのうちに", "覚えて帰っていただきたいのは、これだけ",
          [("house", "家賃"), ("receipt", "電気代"), ("form", "固定資産税")],
          "半分にはなりません",
          left="sensei_conclude", right="kikite_nod"),

    C("今日の内容は、2026年8月時点の情報", "source", title="ご確認のお願い",
      org="2026年8月時点の情報です",
      doc="ご自分の記録と見込み額は、" + NL + "年金事務所かねんきんネットでご確認ください",
      note="※出典（日本年金機構・厚生労働省・国税庁）は概要欄に記載",
      left="sensei_conclude", right="kikite_nod"),

    C("次回は、いわゆる「106万円の壁」", "zu", title="次回は、106万円の壁",
      # dòng tuyên bố xuống thành DẢI CHỐT đáy: ở giữa bảng nó là một node lơ lửng không nối
      # vào mạch `b→c`; ở đáy nó thành khối kết, và mạch mũi tên lên trên thành trục chính.
      nodes=[N("b", "circle", [0.26, 0.40], icon="calendar", label="「いつ」は\nまだ"),
             N("c", "circle", [0.74, 0.40], icon="magnifier", label="施行日の表を\n並べます"),
             N("a", "label", [0.50, 0.99], label="なくなることは、決まりました", lw=700)],
      edges=[E("b", "c", "arrow")],
      left="sensei_present", right="kikite_listen"),

    C("ネットで見かける「2026年10月から」", "zu", title="その日付は、どこから来たのか",
      nodes=[N("a", "icon", [0.20, 0.42], icon="calendar", s=1.0, cross=True),
             N("b", "circle", [0.68, 0.42], icon="checklist", label="施行日の表"),
             N("bb", "bubble", [0.68, 0.02], label="次回、並べて" + NL + "確かめます",
               tail="down", lw=400)],
      edges=[E("a", "b", "arrow")],
      left="sensei_point", right="kikite_nod"),

    # ═════════════════════════ CTA チャンネル登録 (thêm 2026-08-17)
    # Đặt SAU 次回予告 vì 次回 chính là lý do để đăng ký. Cũng chẻ thẻ cuối (29,1s > trần 29s
    # ⇒ clip 30s sẽ LẶP LẠI build-on) — một thẻ giải hai việc.
    C("最後にひとつだけ", "zu", title="次の研究も、受け取れるように",
      nodes=[N("a", "circle", [0.10, 0.40], icon="checklist", label="チャンネル登録"),
             N("b", "circle", [0.82, 0.40], icon="envelope_open", label="新しい制度の話"),
             N("B", "banner", [0.50, 0.99], w=950, icon="clock",
               label="出たときに、いちばん早く届きます")],
      edges=[E("a", "b", "arrow", label="しておくと")],
      left="sensei_present", right="kikite_nod"),
]


# ══════════════════════════════════════════════════════════════ GATE
# Trần ký tự/dòng = bề rộng khả dụng ÷ cỡ SÀN font (chữ full-width ≈ 1 ô font).
# Layout bảng: y hệt build_slides_11 (đã đo). Layout `zu`: đo từ L_zu.
CAPS = {"check": (24, ("ok", "no")), "compare": (32, ("rows",)),
        "steps": (22, ("steps",)), "source": (23, ("doc",))}
# `zu` — trần theo KIND, tính từ (lw mặc định × s) ÷ sàn font:
#   label  lw 470, sàn 30 → 15 ký   ·   circle/mark/icon  lw 300, sàn 26 → 11 ký
#   panel  w 330−36, sàn 26 → 11 ký ·   bubble lw 340, sàn 26 → 13 ký, ≤2 dòng
ZU_CAP = {"label": (30, 1), "circle": (26, 2), "mark": (26, 2), "icon": (26, 2),
          "panel": (26, 1), "bubble": (26, 3),
          # kind thêm 2026-08-17 — sàn font của từng cái xem `L_zu`
          "banner": (30, 1), "ribbon": (38, 1), "chip": (28, 1),
          "oval": (24, 2), "bigicon": (26, 2), "group": (28, 2)}
ZU_LW = {"label": 470, "bubble": 340, "banner": 950, "ribbon": 900, "chip": 300,
         "oval": 182, "group": 400}     # lw mặc định để tính trần ký tự
ZU_MAX_NODES = 7        # build_end = (0.62 + n×0.44 + 0.30) × PACE 1.35 → n=7 là 5,4s (<6s)


def secs(lines, i, j):
    """Thời lượng đọc từ dòng i tới trước dòng j — công thức của make_tts.py."""
    tot = 0.0
    for k in range(i, j):
        t = lines[k]
        if not t:
            tot += GAP_PARA
        else:
            tot += len(t) / CH_PER_SEC + GAP_LINE
    return tot


def main():
    polish(CARDS)
    lines = [re.sub(r"^(\[[^\]]*\])+", "", raw).strip()
            for raw in TTS.read_text(encoding="utf-8").splitlines()]
    dur = secs(lines, 0, len(lines))

    idx, errs = [], []
    for c in CARDS:
        hits = [i for i, t in enumerate(lines) if t and c["match"] in t]
        if len(hits) != 1:
            errs.append(f"  match {'0 dòng' if not hits else f'{len(hits)} dòng {hits}'}"
                        f": {c['match']!r}")
            idx.append(None)
        else:
            idx.append(hits[0])
    if errs:
        print("🔴 MATCH KHÔNG DUY NHẤT — chưa ghi file:")
        print("\n".join(errs))
        sys.exit(1)

    for a, b in zip(idx, idx[1:]):
        if b <= a:
            errs.append(f"  thứ tự sai: dòng {a} → {b}")

    # ⭐ GATE MỚI — ĐỘ DÀI MỖI ENTRY TÍNH BẰNG GIÂY (không dùng số dòng làm proxy).
    holds = [secs(lines, a, b) for a, b in zip(idx, idx[1:])]
    holds.append(secs(lines, idx[-1], len(lines)))
    for k, s in enumerate(holds):
        if s < MIN_SEC:
            errs.append(f"  [{k:02d}] entry chỉ {s:.1f}s < {MIN_SEC}s "
                        f"(dòng {idx[k]}) — gộp với thẻ liền kề: {CARDS[k]['match']!r}")
        if s > 29.0:
            errs.append(f"  [{k:02d}] entry {s:.1f}s > 29s — clip 30s sẽ LẶP LẠI build-on. "
                        f"Chẻ thêm một thẻ: {CARDS[k]['match']!r}")

    # ── gate trần ký tự các layout BẢNG (y hệt build_slides_11)
    for k, c in enumerate(CARDS):
        v = c["stage"]
        spec = CAPS.get(v.get("layout"))
        if not spec:
            continue
        cap, keys = spec
        for key in keys:
            val = v.get(key)
            if not val:
                continue
            for j, row in enumerate([val] if isinstance(val, str) else val):
                txt = row[1] if isinstance(row, (list, tuple)) else row
                for ln in str(txt).split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] {v['layout']}.{key}[{j}] TRÀN: "
                                    f"{len(ln)} ký > trần {cap}: {ln!r}")

    # ── gate timeline (label vẽ font 40 CỐ ĐỊNH, không fit → tràn thanh vàng)
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "timeline":
            continue
        barw = (1400 - 520) * v.get("prog", .62)
        if len(v.get("label", "")) * 40 > barw:
            errs.append(f"  [{k:02d}] label timeline TRÀN: {len(v['label'])*40}px > "
                        f"{barw:.0f}px thanh — rút label hoặc tăng prog: {v['label']!r}")
        cap = int(((1400 - 520) / len(v["steps"]) - 52) // 26)
        for j, row in enumerate(v["steps"]):
            txt = row[1] if isinstance(row, (list, tuple)) else row
            for ln in txt.split(NL):
                if len(ln) > cap:
                    errs.append(f"  [{k:02d}] timeline hộp {j+1} TRÀN: {len(ln)} > {cap}: {ln!r}")

    # ── ⭐ GATE `zu`
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "zu":
            continue
        ns = v["nodes"]
        ids = [n["id"] for n in ns]
        if len(ns) > ZU_MAX_NODES:
            errs.append(f"  [{k:02d}] zu có {len(ns)} node > trần {ZU_MAX_NODES} "
                        f"(build-on vượt 6s)")
        if len(set(ids)) != len(ids):
            errs.append(f"  [{k:02d}] zu trùng id node: {ids}")
        for n in ns:
            fx, fy = n["at"]
            if not (0.0 <= fx <= 1.0 and 0.0 <= fy <= 1.0):
                errs.append(f"  [{k:02d}] zu node {n['id']} at={n['at']} ra ngoài 0..1")
            if n.get("icon") and _icon_path(n["icon"]) is None:
                errs.append(f"  [{k:02d}] zu node {n['id']} icon {n['icon']!r} KHÔNG CÓ FILE "
                            f"→ sẽ rơi về icon vector vẽ tay, lệch họa")
            # 🔴 `group` chở chữ ở BA KHỐI RIÊNG (head/hero/foot), mỗi khối có trần dòng
            # riêng — gộp thành một chuỗi rồi đếm dòng là báo lỗi GIẢ (bản đầu báo "3 dòng > 2").
            # ⚠️ CHỈ cho `group`: khoá `hero` ở kind `label` là CỜ BOOL (số to), không phải chữ
            # `foot` lên trần 2 dòng cùng lượt với việc `_zu_group` biết vẽ nhiều dòng
            # (2026-08-17) — cột dọc của `cols3` chở nhãn vật, mà nhãn thật có xuống dòng.
            for key, mx in ((("head", 2), ("hero", 1), ("foot", 2))
                            if n.get("kind") == "group" else ()):
                txt = n.get(key)
                if not txt:
                    continue
                if len(txt.split(NL)) > mx:
                    errs.append(f"  [{k:02d}] zu {n['id']}.{key} {len(txt.split(NL))} dòng "
                                f"> {mx}: {txt!r}")
                cap = int(n.get("w", 400) * n.get("s", 1.0) // (28 if key != "hero" else 40))
                for ln in txt.split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] zu {n['id']}.{key} TRÀN: {len(ln)} ký "
                                    f"> trần {cap} (w={n.get('w', 400)}): {ln!r}")
            lab = n.get("label", "")
            if lab:
                floor, maxln = ZU_CAP[n.get("kind", "circle")]
                lw = n.get("lw", ZU_LW.get(n.get("kind", "circle"), 300))
                cap = int(lw * n.get("s", 1.0) // floor)
                if len(lab.split(NL)) > maxln:
                    errs.append(f"  [{k:02d}] zu {n['id']} {len(lab.split(NL))} dòng > "
                                f"{maxln}: {lab!r}")
                for ln in lab.split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] zu {n['id']} ({n.get('kind','circle')}) "
                                    f"TRÀN: {len(ln)} ký > trần {cap} (lw={lw}): {ln!r}")
        for e in v.get("edges", []):
            for side in ("from", "to"):
                if e[side] not in ids:
                    errs.append(f"  [{k:02d}] zu edge {side}={e[side]!r} không có node đó")
        # ⭐ GATE HÌNH HỌC — gọi HÀM CỦA make_stage, KHÔNG chép công thức sang đây.
        # Chép là hai bản số lệch nhau ngay lần sửa layout đầu tiên (bài học `_sig`).
        for msg in _zu_check(v):
            errs.append(f"  [{k:02d}] zu {msg}")
        # (khe của nhãn edge do `zu_check` đo — nó có toạ độ SAU KẸP, ở đây chỉ có `at` thô)

    if errs:
        print("🔴 GATE:")
        print("\n".join(errs))
        sys.exit(1)

    OUT.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1), encoding="utf-8")

    import collections
    n = len(CARDS)
    dist = collections.Counter(c["stage"]["layout"] for c in CARDS)
    sp = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "old" for x in c["stage"]["nodes"])]
    sl = [i for i, c in enumerate(CARDS)
          if c["stage"]["layout"] == "zu" and any(x["id"] == "s0" for x in c["stage"]["nodes"])]
    art = sorted({c["stage"][x] for c in CARDS for x in ("img", "fill", "bgimg")
                  if c["stage"].get(x)})
    print(f"✅ ghi {OUT.name}  —  {n} thẻ  ·  video {int(dur)//60}:{int(dur)%60:02d}")
    print(f"   nhịp: {n/(dur/60):.2f} đổi hình/phút (trần 6)  ·  "
          f"entry: min {min(holds):.1f}s · TB {dur/n:.1f}s · max {max(holds):.1f}s")
    print(f"   layout: {dict(dist)}")
    print(f"   TRỤC HÌNH — spine (số cũ→mới): {sp}  ·  4 ô đếm lần: {sl}")
    print(f"   ảnh cần có ({len(art)}): {art}")


if __name__ == "__main__":
    main()
