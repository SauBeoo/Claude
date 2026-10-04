# -*- coding: utf-8 -*-
r"""build_slides_demo17.py — SLIDES cho ĐOẠN DEMO video 17 (cold open + cao trào).

MỤC ĐÍCH DUY NHẤT: cho user soi tận mắt **ảnh paper-collage nằm trong card kem
(255,250,238) của khung sân khấu nenkin** có ăn nhau không, TRƯỚC khi gen cả lô ~25 ảnh.
Đây KHÔNG phải SLIDES thật của video 17 — bản thật sẽ là `build_slides_17.py`.

Đoạn demo = 第1章 + 第2章 + 第3章 (~3:47), dùng 4/5 ảnh của lô probe. Ảnh thứ 5
(`art_tsuri_nakama`, beat 第11章) không nằm trong đoạn này → xuất still riêng để soi.

CHẠY:  python tools/build_slides_demo17.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\_media_library")

PROJ = Path(__file__).resolve().parents[1]
TTS = PROJ / "03_SCRIPTS" / "demo17_TTS.md"
OUT = PROJ / "03_SCRIPTS" / "demo17_SLIDES.json"

NL = "\n"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0
MIN_SEC = 6.0


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


CARDS = [
    # ── entry 0: CHỦ THỂ của bài = cuộc gọi (§2.0 + §2.10 ⑦) ──────────────────
    C("その電話は、机の上のスマートフォンを、震わせました。", "art",
      title="その電話は、《震えて》いました",
      img="art_denwa_furueru.png", fly="up",
      cap="平日の昼下がり。テレビでは、お昼のニュース",
      left="sensei_serious", right="kikite_listen"),

    # giọng máy đọc lời thoại giả — thẻ chữ, nền nhạt (bgimg có chữ đè)
    C("機械の声が、言います。", "check",
      title="機械の声が、こう言いました", bgimg="bg_tsukue_denwa.png",
      no=[("phone", "「書類の提出が確認できない」"),
          ("warning", "「来月から、年金の支給が停止されます」"),
          ("clock", "「至急、1を押してください」")],
      left="sensei_caution", right="kikite_worried"),

    C("そして鈴木さんは——1を、押しました。", "big",
      title="そして鈴木さんは", value="1を、押した", unit="", pop=True,
      cap="物語は、ここから始まります",
      left="sensei_serious", right="kikite_surprised"),

    # ── 第2章: 4 câu hỏi leo thang ────────────────────────────────────────────
    C("1を押すと、少しの保留音のあと、今度は、人の声が出ました。", "check",
      title="《人の声》が、順番に聞いたこと", bgimg="bg_tsukue_denwa.png",
      ok=[("calendar", "生年月日"), ("cityhall", "住所の一部")],
      no=[("passbook", "ご登録の口座番号"),
          ("docs", "マイナンバーカードの写真")],
      left="sensei_explain", right="kikite_think"),

    # ── CAO TRÀO: ảnh nền đỏ, khoảnh khắc đắt nhất bài ───────────────────────
    C("——ここで、手が、止まりました。", "art",
      title="——ここで、手が《止まった》",
      img="art_te_tomaru.png", fly="up",
      cap="あと少し遅ければ、その先まで進んでいました",
      left="sensei_caution", right="kikite_surprised"),

    # ── 第3章: gọi lại số thật (panel pict, fit=True để thấy trọn ảnh) ────────
    C("年金手帳を取り出しました。裏表紙に、本物の相談窓口の番号が、印刷されています。そこに、かけ直しました。", "pict",
      title="切って、《本物の番号》にかけ直す",
      fit=True,
      panels=[{"label": "年金手帳の\n裏表紙の番号", "img": "art_tsucho_kakenaosu.png"}],
      cap="折り返しの番号は、相手が用意した番号かもしれません",
      left="sensei_point", right="kikite_nod"),
]


def secs(lines, i, j):
    ch = sum(len(re.sub(r"\[[^\]]+\]", "", lines[k])) for k in range(i, j))
    return ch / CH_PER_SEC + (j - i) * GAP_LINE + GAP_PARA


def main():
    raw = TTS.read_text(encoding="utf-8").split("\n")
    plain = [re.sub(r"\[[^\]]+\]", "", l).strip() for l in raw]

    # ── GATE: match phải khớp ĐÚNG 1 dòng, và thứ tự phải tăng dần ───────────
    idx, bad = [], []
    for c in CARDS:
        m = c["match"]
        hits = [i for i, p in enumerate(plain) if m in p]
        if len(hits) != 1:
            bad.append(f"match {len(hits)} dòng: {m[:40]}")
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

    # ── GATE: khoảng cách entry ≥ MIN_SEC (audience-45plus §2 mục 2) ─────────
    for k in range(len(idx) - 1):
        d = secs(raw, idx[k], idx[k + 1])
        if d < MIN_SEC:
            print(f"🔴 entry {k} chỉ {d:.1f}s (< {MIN_SEC}s) — gộp lại")
            return 1
        print(f"   entry {k}: {d:5.1f}s  ·  {CARDS[k]['stage'].get('title','')[:34]}")
    dlast = secs(raw, idx[-1], len(raw))
    print(f"   entry {len(idx)-1}: {dlast:5.1f}s  ·  {CARDS[-1]['stage'].get('title','')[:34]}")

    # ── GATE: mật độ đổi hình ≤6/phút ───────────────────────────────────────
    total = secs(raw, 0, len(raw))
    dens = len(CARDS) / (total / 60)
    print(f"\n   tổng {total:.0f}s ({total/60:.2f}′) · {len(CARDS)} thẻ · "
          f"{dens:.2f} đổi hình/phút (trần 6)")
    if dens > 6:
        print("🔴 mật độ vượt trần 6 đổi hình/phút")
        return 1

    # ── GATE: ảnh khai báo phải TỒN TẠI (render-background §1.5) ────────────
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
