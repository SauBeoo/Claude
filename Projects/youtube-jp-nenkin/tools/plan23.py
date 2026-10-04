# -*- coding: utf-8 -*-
"""
plan23.py — chốt SCENE PLAN video 23 và in ra con số thật phải gen.

Copy từ `plan22.py`. Chạy TRƯỚC khi xuất prompt (luật CLAUDE.md §②: **chốt số scene TRƯỚC,
rồi mới báo số asset** — video 17 làm ngược và phải gen bù 2 lô).

In ra:
  · từng scene: giây bắt đầu/kết, độ dài, kind, số shot cần
  · tổng số clip Veo phải gen
  · 5 gate: dòng timeline khớp · telop ≤11 ký · genten có trong sổ · scene liền mạch ·
    lặp khuôn + lặp động tác
"""
import io, json, math, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
from _scenes23 import SCENES, GENTEN, NUM  # noqa: E402

TL = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\23_nenkin-seikyusho-todokanai\timeline.json")
N_LINES = 124          # số dòng timeline lúc chốt bảng scene
SHOT = 8.0             # clip Veo dài đúng 8,000s
# 🔴 Chỉ được làm CHẬM clip, cấm làm nhanh (speed>1 đẩy người xem tới đoạn "AI hết đà").
SHOT_MAX = 8.7
NO_CLIP = ("stat", "formula", "genten", "gfx")   # kind KHÔNG cần footage Veo


def build():
    tl = json.load(io.open(TL, encoding="utf-8"))["lines"]

    # ── GATE 1: bảng scene neo theo CHỈ SỐ DÒNG ⇒ vỡ im lặng nếu timeline đổi ──
    if len(tl) != N_LINES:
        print(f"🔴 timeline có {len(tl)} dòng, bảng scene chốt theo {N_LINES}. "
              f"_TTS.md đã đổi ⇒ rà lại _scenes23.py TRƯỚC khi chạy tiếp."); sys.exit(1)

    rows, errs = [], []
    for k, (ln, kind, telop, body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        t0 = tl[ln]["start"]
        t1 = tl[nxt]["start"] if nxt < len(tl) else tl[-1]["end"]
        rows.append(dict(i=k, ln=ln, kind=kind, telop=telop, body=body,
                         t0=t0, t1=t1, dur=t1 - t0, nshot=0))

        # ── GATE 2: telop bắt buộc, trần 11 ký/dòng ─────────────────────────
        if not telop:
            errs.append(f"scene {k}: thiếu telop")
        for seg in telop.split("\n"):
            plain = seg.replace("{", "").replace("}", "")
            if len(plain) > 11:
                errs.append(f"scene {k}: dòng telop {len(plain)} ký > 11 — «{plain}»")
        # ── GATE 3: genten phải có trong sổ GENTEN ──────────────────────────
        if kind == "genten" and body not in GENTEN:
            errs.append(f"scene {k}: genten «{body}» không có trong GENTEN")
        # ── GATE 6: chính sách SỐ chỉ được khai ở scene CÓ MẶT PHẲNG IN SỐ ──
        # 🔴 Khai `NUM` cho PERSON/gfx/formula thì mệnh đề số không vào prompt nào cả —
        #    lỗi IM LẶNG: file prompt vẫn xuất bình thường, chỉ có con số biến mất.
        #    Đã dính 3/5 khoá ở bản đầu (khoá ghi theo SỐ DÒNG thay vì CHỈ SỐ SCENE).
        if k in NUM:
            import flow23_full as _f0
            if kind != "art" or _f0.classify(body) not in ("SCREEN", "HOLD"):
                errs.append(f"scene {k}: khai NUM nhưng không phải art/SCREEN|HOLD "
                            f"(kind={kind}) — số sẽ rơi vào hư không")

    # ── CẤP CLIP THEO **KHỐI** ART LIỀN NHAU, không theo từng scene ──────────
    # Cấp ceil(dur/8,7) cho MỖI scene thì scene 3,5s cũng ăn trọn một clip ⇒ vượt trần
    # 6 đổi hình/phút. Gom scene `art` LIỀN KỀ thành khối, cấp clip cho cả khối rồi chia.
    blocks, cur = [], []
    for r in rows:
        if r["kind"] == "art":
            cur.append(r)
        else:
            if cur: blocks.append(cur); cur = []
    if cur: blocks.append(cur)
    for blk in blocks:
        d = sum(r["dur"] for r in blk)
        n = max(1, math.ceil(d / SHOT_MAX))
        acc, given = 0.0, 0
        for r in blk:
            acc += r["dur"]
            r["nshot"] = max(0, round(acc / d * n) - given)
            given += r["nshot"]
        if given != n:      # bù sai số làm tròn vào scene dài nhất của khối
            max(blk, key=lambda r: r["dur"])["nshot"] += n - given

    # ── GATE 4: scene phải phủ liên tục, không hở không chồng ────────────────
    for a, b in zip(rows, rows[1:]):
        if abs(a["t1"] - b["t0"]) > 0.001:
            errs.append(f"scene {a['i']}→{b['i']}: hở/chồng {a['t1']:.2f} vs {b['t0']:.2f}")

    total = rows[-1]["t1"]
    nshot = sum(r["nshot"] for r in rows)

    print(f"{'#':>3} {'giây':>14} {'dài':>6} {'kind':<8} {'shot':>4}  telop")
    print("─" * 80)
    for r in rows:
        print(f"{r['i']:>3} {r['t0']:>6.1f}-{r['t1']:>6.1f} {r['dur']:>6.1f} "
              f"{r['kind']:<8} {r['nshot'] or '·':>4}  {r['telop'].replace(chr(10),' / ')}")

    print("─" * 80)
    import collections as _c
    kc0 = _c.Counter(r["kind"] for r in rows)
    print(f"tổng {total:.1f}s = {total/60:.1f}′ · {len(rows)} scene · {dict(kc0)}")
    print(f"⭐ SỐ CLIP VEO PHẢI GEN: {nshot}")
    print(f"   {len(blocks)} khối art · scene dài nhất {max(r['dur'] for r in rows):.1f}s "
          f"(scene {max(rows, key=lambda r: r['dur'])['i']})")
    share = [r['i'] for r in rows if r['kind'] == 'art' and r['nshot'] == 0]
    if share:
        print(f"   {len(share)} scene art dùng chung clip với scene trước: {share[:14]}"
              + (" …" if len(share) > 14 else ""))

    pace = nshot / (total / 60)
    print(f"   nhịp đổi hình: {pace:.1f}/phút " + ("✓" if pace <= 6.0 else "🔴 vượt trần 6"))

    # ── GATE 5: LẶP KHUÔN + LẶP ĐỘNG TÁC ────────────────────────────────────
    # 🔴 DÙNG CHUNG hàm `classify` của `flow23_full.py`, không tự phân loại lại —
    #    hai bản sao logic cho hai con số khác nhau trên cùng một bảng scene.
    import importlib
    _ff = importlib.import_module("flow23_full")
    bodies = [r["body"] for r in rows if r["kind"] == "art"]
    kinds = [_ff.classify(b) for b in bodies]
    kc = _c.Counter(kinds)
    ratio = kc.get("PERSON", 0) / max(1, len(kinds))
    if ratio > 0.35:
        errs.append(f"PERSON chiếm {ratio:.0%} scene art (trần 35%) — thêm CROWD/VIZ/SCREEN")
    pbodies = [b for b, k in zip(bodies, kinds) if k == "PERSON"]
    for phrase in ("at the camera", "nod", "palms together", "smil", "shakes his head",
                   "resting on the table", "sits at"):
        n = sum(1 for b in pbodies if phrase in b)
        if n > 3:
            errs.append(f'cụm «{phrase}» lặp {n} lần trong scene PERSON (trần 3)')
    print(f"   khuôn: {dict(kc)} · PERSON {ratio:.0%} (trần 35%)")

    if errs:
        print("\n🔴 GATE:")
        for e in errs[:20]:
            print("  ", e)
        sys.exit(1)
    print("\n✓ 5 gate sạch")
    return rows


if __name__ == "__main__":
    build()
