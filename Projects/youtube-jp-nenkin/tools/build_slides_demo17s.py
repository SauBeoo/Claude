# -*- coding: utf-8 -*-
r"""build_slides_demo17s.py — SLIDES demo video 17: KHUNG SÂN KHẤU + ảnh vox + LỚP STICKER.

⭐ USER CHỐT 2026-08-26 (lần 3, sau 2 lần tao hiểu sai):
  ① **GIỮ khung sân khấu cũ** (card kem + 2 cast hai mép + dải phụ đề) — bản `demo17fb`
     full-bleed là SAI hướng, bỏ.
  ② **Ảnh ở giữa dạng vox** (paper-collage) — giữ, đã đúng ở `demo17`.
  ③ ⭐ **Chữ/số phải vào như STICKER — "nó đến nó mới hiển thị ra"**, không hiện sẵn.
  ④ ⭐ **Các con số / số liệu PHẢI hiển thị** thành sticker.

🔴 CÁI TAO ĐÃ BỎ QUÊN Ở `build_slides_demo17.py`: khoá **`sync`** — cơ chế này ĐÃ CÓ SẴN
trong `CLAUDE.md` §② LỚP STICKER (chốt 2026-08-24, khuôn mẫu `build_slides_16.py`) mà bản
demo trước không dùng **một cái nào**. Nên demo đó ra thẻ trơ chữ — đúng cái bệnh
「60% thẻ trơ chữ」 mà lớp sticker sinh ra để chữa. Bản này dùng đủ 4 kind pin.

CƠ CHẾ (chép nguyên `sync_layer` từ `build_slides_16.py`):
  sync=[{"ph": "<cụm từ CÓ THẬT trong lời của chính thẻ đó>", ...}]
    · khoá "icon" → `props_top` (sticker hình nổi trên ảnh), t0 = giây cụm từ đó được ĐỌC
    · khoá "pin"  → `pins` (art/photo) hoặc `pins_card` (layout khác), beat = giây đó
      kind: `num`+`burst` số hero có 集中線 · `stamp` dấu đỏ nghiêng · `badge` bong bóng đặc
            · `zoom` vòng phóng đại
  🔴 GATE: cụm từ không có trong lời ⇒ exit 1. Không cho gắn vật trang trí không khớp sub.

ĐOẠN DEMO = 第1章 + 第2章 + 第3章 + 第8章 (~4:46) — cố ý ghép 第8章 vào để demo có CẢ
sticker chữ (hook/cao trào) VÀ sticker SỐ LIỆU (3,257億円 / 2,087件 / 1,816億円 / 10億円).

CHẠY:  python tools/build_slides_demo17s.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\_media_library")

PROJ = Path(__file__).resolve().parents[1]
TTS = PROJ / "03_SCRIPTS" / "demo17s_TTS.md"
OUT = PROJ / "03_SCRIPTS" / "demo17s_SLIDES.json"

NL = "\n"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0
MIN_SEC = 6.0


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


CARDS = [
    # ═══ entry 0: chủ thể = cuộc gọi. Sticker: điện thoại + badge 「震えた」 ═══
    C("その電話は、机の上のスマートフォンを、震わせました。", "art",
      title="その電話は、《震えて》いました",
      img="art_denwa_furueru.png", fly="up",
      cap="平日の昼下がり。テレビでは、お昼のニュース",
      sync=[{"ph": "机の上のスマートフォン", "icon": "phone",
             "at": [0.075, 0.26], "s": 130, "rot": -9},
            {"ph": "震わせました", "pin": {"kind": "stamp", "t": "震えた",
                                           "at": [0.74, 0.12], "rot": -8, "size": 54}}],
      left="sensei_serious", right="kikite_listen"),

    # ═══ giọng máy: 3 câu thoại giả, mỗi câu 1 sticker vào ĐÚNG lúc đọc ═══
    C("機械の声が、言います。", "check",
      title="機械の声が、こう言いました", bgimg="bg_tsukue_denwa.png",
      no=[("phone", "「書類の提出が確認できない」"),
          ("warning", "「来月から、年金の支給が停止されます」"),
          ("clock", "「至急、1を押してください」")],
      sync=[{"ph": "支給が停止されます", "pin": {"kind": "badge", "t": "支給" + NL + "停止",
                                                 "at": [0.86, 0.17], "tone": "red",
                                                 "r": 0.115, "size": 48}},
            {"ph": "1を押してください", "pin": {"kind": "stamp", "t": "1を押せ？",
                                                "at": [0.70, 0.85], "rot": -7, "size": 46}}],
      left="sensei_caution", right="kikite_worried"),

    # ═══ SỐ HERO đầu: 「1」 — num + burst (集中線) ═══
    # ⚖️ NGOẠI LỆ CÓ Ý THỨC của luật "big = không sticker" (CLAUDE.md §② mục 7): ở đây
    # `value` là một CÂU (「1を、押した」), không phải số to lấp giữa card ⇒ còn chỗ bên
    # phải, và pin chở SỐ 1 — khác vai với câu, không lặp. Soi still đã xác nhận sạch.
    C("そして鈴木さんは——1を、押しました。", "big",
      title="そして鈴木さんは", value="1を、押した", unit="", pop=True,
      cap="物語は、ここから始まります",
      sync=[{"ph": "1を、押しました", "pin": {"kind": "num", "t": "1", "burst": True,
                                              "at": [0.84, 0.30], "size": 150}}],
      left="sensei_serious", right="kikite_surprised"),

    # ═══ 4 câu hỏi leo thang — CHẺ 2 THẺ ═══
    # 🔴 Bản đầu để 1 thẻ giữ 71,7s → sticker beat rơi ở 67,5s, VƯỢT trần clip 30s của
    # make_stage ⇒ "phần tử cuối KHÔNG kịp hiện" (tool báo thẳng). Chẻ 2 vừa hết lỗi,
    # vừa đúng nghĩa hơn: leo thang có 2 BƯỚC (an toàn → nguy hiểm), và nâng mật độ
    # đổi hình (bản 1 thẻ chỉ 1,78/phút = quá thoáng, thẻ đứng 1 phút rưỡi là tẻ).
    C("1を押すと、少しの保留音のあと、今度は、人の声が出ました。", "check",
      title="ここまでは、まだ《ふつう》", bgimg="bg_tsukue_denwa.png",
      ok=[("calendar", "生年月日"), ("cityhall", "住所の一部")],
      sync=[{"ph": "人の声が出ました", "pin": {"kind": "badge", "t": "人の声" + NL + "に交代",
                                               "at": [0.87, 0.15], "tone": "amber",
                                               "r": 0.115, "size": 42}},
            {"ph": "生年月日を聞かれ", "icon": "calendar",
             "at": [0.075, 0.30], "s": 118},
            {"ph": "違和感もなかった", "pin": {"kind": "stamp", "t": "違和感なし",
                                               "at": [0.70, 0.86], "rot": -7,
                                               "size": 46}}],
      left="sensei_explain", right="kikite_think"),

    C("「では、支給停止を解除するために、ご登録の口座番号を、確認させてください」", "check",
      title="ここから、《渡してはいけない》もの", bgimg="bg_tsukue_denwa.png",
      no=[("passbook", "ご登録の口座番号"),
          ("docs", "マイナンバーカードの写真")],
      sync=[{"ph": "口座番号を、答えました", "icon": "passbook",
             "at": [0.075, 0.34], "s": 124},
            {"ph": "マイナンバーカードの写真", "pin": {"kind": "stamp", "t": "ここが限界",
                                                      "at": [0.68, 0.86], "rot": -9,
                                                      "size": 50}}],
      left="sensei_caution", right="kikite_worried"),

    # ═══ CAO TRÀO: zoom vào chỗ tay dừng ═══
    C("——ここで、手が、止まりました。", "art",
      title="——ここで、手が《止まった》",
      img="art_te_tomaru.png", fly="up",
      cap="あと少し遅ければ、その先まで進んでいました",
      sync=[{"ph": "手が、止まりました", "pin": {"kind": "zoom", "at": [0.60, 0.46],
                                                 "r": 0.17}},
            {"ph": "手が、止まりました", "pin": {"kind": "stamp", "t": "止まった",
                                                 "at": [0.79, 0.13], "rot": -10,
                                                 "size": 58}}],
      left="sensei_caution", right="kikite_surprised"),

    # ═══ 第3章: gọi lại số thật ═══
    C("年金手帳を取り出しました。裏表紙に、本物の相談窓口の番号が、印刷されています。そこに、かけ直しました。", "pict",
      title="切って、《本物の番号》にかけ直す",
      fit=True,
      panels=[{"label": "年金手帳の\n裏表紙の番号", "img": "art_tsucho_kakenaosu.png"}],
      cap="折り返しの番号は、相手が用意した番号かもしれません",
      sync=[{"ph": "年金手帳を取り出しました", "icon": "nenkin_techo",
             "at": [0.075, 0.28], "s": 132},
            {"ph": "かけ直しました", "pin": {"kind": "badge", "t": "自分で" + NL + "調べた番号",
                                             "at": [0.87, 0.20], "tone": "blue",
                                             "r": 0.115, "size": 40}}],
      left="sensei_point", right="kikite_nod"),

    # ═══════════════ 第8章 — SỐ LIỆU, đây là chỗ user muốn thấy nhất ═══════════════
    # 3 số của 警察庁, mỗi số vào ĐÚNG lúc giọng đọc tới nó. Số ĐẮT NHẤT (1,816億円)
    # mới được `burst` — nhấn hết thì không còn gì nhấn (CLAUDE.md §② mục 3).
    # 🔴 BA LỖI ĐÃ VÁ, và lỗi thứ ba đổi cả LỰA CHỌN LAYOUT (soi still `clip_07/08`, 2026-08-26):
    #  ① pin `num` LẶP LẠI chính `value` của `big` ⇒ cùng một số hiện HAI LẦN (navy giữa card
    #     + vàng góc phải). `big` đã là "thẻ số hero".
    #  ② badge/stamp ở `y 0.64–0.86` ĐÈ chữ `cap` (cap của `big` ở ~y 0.72).
    #  ③ ⭐ Dời lên `y 0.16 / 0.68` VẪN ĐÈ — lần này đè số hero và tiêu đề. ⇒ Kết luận thật:
    #     **layout `big` KHÔNG có vùng trống nào đủ cho sticker.** Số hero chiếm giữa, title
    #     chiếm đỉnh, cap chiếm đáy — hết chỗ. Nhồi sticker vào `big` là phá thẻ.
    #     ⇒ Khối NHIỀU SỐ chuyển sang **`check`** (khuôn đã chứng minh sạch ở `clip_04`):
    #     mỗi số một dòng, và vì `check` KHÔNG có số hero nên pin `num` không còn trùng gì.
    #     📌 Luật rút ra cho video thật: `big` = ĐÚNG MỘT số, không sticker · `check`/`zu` =
    #     khối nhiều số, sticker thoải mái.
    C("警察庁の統計です。令和7年、1年間の特殊詐欺の被害総額は、全国で、およそ3,257億円。", "check",
      title="令和7年・1年間の被害（警察庁）",
      # ⚠️ `ok=`, KHÔNG `no=`: đây là số liệu TRUNG TÍNH, không phải "điều sai".
      # `audience-45plus.md` §2.1 — thẻ toàn dòng `no` thì chữ ra xám (168,174,184) trên
      # nền kem ⇒ "vừa trống vừa nhạt, tệ nhất với tệp 45+". Bản đầu tao để `no`, sai.
      ok=[("chart_up", "特殊詐欺 ぜんたい 3,257億円"),
          ("phone", "うち 還付金をかたる詐欺 2,087件")],
      sync=[{"ph": "3,257億円", "pin": {"kind": "num", "t": "3,257億", "burst": False,
                                        "at": [0.82, 0.22], "size": 88}},
            {"ph": "警察庁の統計です", "icon": "shield_check",
             "at": [0.075, 0.26], "s": 118},
            {"ph": "2,087件", "pin": {"kind": "stamp", "t": "還付金だけで",
                                      "at": [0.72, 0.88], "rot": -7, "size": 44}}],
      left="sensei_present", right="kikite_listen"),

    C("そして、今年——令和8年の上半期、1月から6月までの被害額は、およそ1,816億円。", "check",
      title="令和8年・上半期（1〜6月）は",
      ok=[("chart_up", "半年で 1,816億円"),
          ("clock", "前の年の同じ時期より 5割以上"),
          ("calc", "1日あたり およそ10億円")],
      sync=[{"ph": "1,816億円", "pin": {"kind": "num", "t": "1,816億", "burst": True,
                                        "at": [0.82, 0.20], "size": 96}},
            {"ph": "5割以上", "pin": {"kind": "stamp", "t": "＋5割以上",
                                      "at": [0.70, 0.89], "rot": -8, "size": 48}},
            {"ph": "10億円の被害", "icon": "money_pouch", "at": [0.075, 0.62], "s": 120}],
      left="sensei_serious", right="kikite_worried"),

    # hedge YMYL: số là TOÀN BỘ đặc thù lừa đảo, không riêng vụ mạo danh 年金機構
    C("これは、あらゆる手口を合わせた、特殊詐欺全体の数字です。", "check",
      title="この数字の《読み方》", bgimg="bg_tsukue_denwa.png",
      ok=[("checklist", "特殊詐欺 ぜんたいの数字です")],
      no=[("magnifier", "年金機構をかたる手口だけの数字ではない")],
      sync=[{"ph": "特殊詐欺全体の数字です", "pin": {"kind": "stamp", "t": "全体の数字",
                                                     "at": [0.72, 0.13], "rot": -7,
                                                     "size": 48}},
            {"ph": "確かに含まれています", "pin": {"kind": "badge",
                                                   "t": "その中に" + NL + "この電話も",
                                                   "at": [0.86, 0.70], "tone": "red",
                                                   "r": 0.12, "size": 40}}],
      left="sensei_explain", right="kikite_nod"),
]


def secs(lines, i, j):
    tot = 0.0
    for k in range(i, j):
        t = lines[k]
        tot += GAP_PARA if not t else len(t) / CH_PER_SEC + GAP_LINE
    return tot


def sync_layer(cards, lines, idx, holds):
    """Chép nguyên từ build_slides_16.py — xem docstring đầu file."""
    bad = []
    for k, c in enumerate(cards):
        v = c["stage"]
        spec = v.pop("sync", None)
        if not spec:
            continue
        a = idx[k]
        b = idx[k + 1] if k + 1 < len(cards) else len(lines)
        hold = holds[k]
        _pk = "pins" if v.get("layout") in ("art", "photo") else "pins_card"
        props, pins = list(v.get("props_top") or []), list(v.get(_pk) or [])
        for it in spec:
            ph = it["ph"]
            hit = None
            for m in range(a, b):
                if lines[m] and ph in lines[m]:
                    hit = (m, lines[m].index(ph))
                    break
            if hit is None:
                bad.append(f"  [{k:02d}] cụm {ph!r} KHÔNG có trong lời thẻ {c['match'][:24]!r}")
                continue
            m, pos = hit
            t = secs(lines, a, m) + pos / CH_PER_SEC
            t = max(0.35, min(t, hold - 0.45))
            if "icon" in it:
                props.append({kk: vv for kk, vv in it.items() if kk not in ("ph", "pin")}
                             | {"t0": round(t, 2)})
            elif "pin" in it:
                pins.append(dict(it["pin"], beat=round(t, 2)))
        if props:
            v["props_top"] = props
        if pins:
            v[_pk] = pins
    if bad:
        print("🔴 SYNC: vật không khớp lời — chưa ghi file:")
        print(NL.join(bad))
        sys.exit(1)
    ns = sum(len(c["stage"].get("props_top") or []) for c in cards)
    np_ = sum(len(c["stage"].get("pins") or []) + len(c["stage"].get("pins_card") or [])
              for c in cards)
    print(f"[sync] {ns} icon + {np_} pin khớp đúng cụm từ trong lời đọc")


def main():
    raw = TTS.read_text(encoding="utf-8").split(NL)
    lines = [re.sub(r"^(\[[^\]]*\])+", "", l).strip() for l in raw]
    plain = [re.sub(r"\[[^\]]+\]", "", l).strip() for l in raw]

    idx, bad = [], []
    for c in CARDS:
        m = c["match"]
        hits = [i for i, p in enumerate(plain) if m in p]
        if len(hits) != 1:
            bad.append(f"match {len(hits)} dòng: {m[:44]}")
            idx.append(None)
        else:
            idx.append(hits[0])
    if bad:
        for b in bad:
            print(f"🔴 {b}")
        return 1
    if idx != sorted(idx):
        print(f"🔴 thứ tự match KHÔNG tăng dần: {idx}")
        return 1

    holds = []
    for k in range(len(idx)):
        nxt = idx[k + 1] if k + 1 < len(idx) else len(raw)
        holds.append(secs(raw, idx[k], nxt))
    for k, d in enumerate(holds):
        if d < MIN_SEC:
            print(f"🔴 entry {k} chỉ {d:.1f}s (< {MIN_SEC}s)")
            return 1
        print(f"   entry {k}: {d:5.1f}s  ·  {CARDS[k]['stage'].get('title','')[:32]}")

    total = secs(raw, 0, len(raw))
    dens = len(CARDS) / (total / 60)
    print(f"\n   tổng {total:.0f}s ({total/60:.2f}′) · {len(CARDS)} thẻ · "
          f"{dens:.2f} đổi hình/phút (trần 6)")
    if dens > 6:
        print("🔴 mật độ vượt trần")
        return 1

    sync_layer(CARDS, lines, idx, holds)

    art = PROJ / "06_VIDEO" / "17_nenkin-sagi-jidoonsei-shikyuteishi" / "art"
    want = set()
    for c in CARDS:
        v = c["stage"]
        for k in ("img", "bgimg", "fill"):
            if v.get(k):
                want.add(v[k])
        for p in v.get("panels", []):
            if p.get("img"):
                want.add(p["img"])
    missing = sorted(f for f in want if not (art / f).exists())
    print(f"   ảnh: {len(want)-len(missing)}/{len(want)} có sẵn")
    for m in missing:
        print(f"🔴 THIẾU ẢNH: {m}")
    if missing:
        return 1

    OUT.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n✓ {OUT.name}: {len(CARDS)} thẻ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
