# -*- coding: utf-8 -*-
"""
plan22.py — chốt SCENE PLAN video 22 và in ra con số thật phải gen.

Chạy TRƯỚC khi xuất prompt. Lý do có bước riêng này: ở video 17 tao ước 25 scene, báo user
gen 25 ảnh, rồi lúc viết builder lại chia 39 scene và **lấp 9 chỗ bằng ảnh dùng lại mà không
nói** — user tự phát hiện. Luật rút ra (CLAUDE.md §②): **chốt số scene TRƯỚC, rồi mới báo số
asset**. File này là bước "chốt" đó.

In ra:
  · từng scene: giây bắt đầu/kết, độ dài, kind, số shot cần
  · tổng số clip Veo phải gen
  · 4 gate: dòng timeline khớp · scene không hở/chồng · telop mọi scene · nhịp đổi hình
"""
import io, json, math, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
from _scenes22 import SCENES, GENTEN  # noqa: E402

TL = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man\timeline.json"
N_LINES = 113          # số dòng timeline lúc chốt bảng scene
SHOT = 8.0             # clip Veo dài đúng 8,000s
# 🔴 Chỉ được làm CHẬM clip, cấm làm nhanh (speed>1 đẩy người xem tới đoạn "AI hết đà").
#    speed tối thiểu 0,92 ⇒ một clip phủ được tối đa 8,0/0,92 = 8,7s.
SHOT_MAX = 8.7


def build():
    tl = json.load(io.open(TL, encoding="utf-8"))["lines"]

    # ── GATE 1: bảng scene neo theo CHỈ SỐ DÒNG ⇒ vỡ im lặng nếu timeline đổi ──
    if len(tl) != N_LINES:
        print(f"🔴 timeline có {len(tl)} dòng, bảng scene chốt theo {N_LINES}. "
              f"_TTS.md đã đổi ⇒ rà lại _scenes22.py TRƯỚC khi chạy tiếp."); sys.exit(1)

    rows, errs = [], []
    for k, (ln, kind, telop, body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        t0 = tl[ln]["start"]
        t1 = tl[nxt]["start"] if nxt < len(tl) else tl[-1]["end"]
        dur = t1 - t0
        nshot = 0  # tính sau, theo KHỐI — xem ghi chú dưới
        rows.append(dict(i=k, ln=ln, kind=kind, telop=telop, body=body,
                         t0=t0, t1=t1, dur=dur, nshot=nshot))

        # ── GATE 2: telop bắt buộc, và trần ~10 ký/dòng ─────────────────────
        if not telop:
            errs.append(f"scene {k}: thiếu telop")
        for seg in telop.split("\n"):
            plain = seg.replace("{", "").replace("}", "")
            if len(plain) > 11:
                errs.append(f"scene {k}: dòng telop {len(plain)} ký > 11 — «{plain}»")
        # ── GATE 3: genten phải có trong sổ GENTEN ──────────────────────────
        if kind == "genten" and body not in GENTEN:
            errs.append(f"scene {k}: genten «{body}» không có trong GENTEN")

    # ── CẤP CLIP THEO **KHỐI** ART LIỀN NHAU, không theo từng scene ──────────
    # 🔴 Bản đầu cấp `ceil(dur/8,7)` cho MỖI scene ⇒ scene 3,5s cũng ăn trọn một clip,
    #    ra 97 clip và nhịp 7,0 đổi hình/phút = VƯỢT trần 6 của `audience-45plus.md` §2.
    # ⇒ TELOP và CLIP không phải một-đối-một: một clip 8s chở được 2 telop ngắn liền nhau.
    #    Gom các scene `art` LIỀN KỀ thành một khối, cấp `ceil(tổng_khối / 8,7)` clip cho
    #    cả khối, rồi chia đều clip trong khối. Vừa hạ số clip phải gen, vừa về đúng trần.
    # ⚠️ Chỉ gom scene LIỀN KỀ: chen một thẻ stat/genten vào giữa là cắt khối, vì lúc đó
    #    footage thật sự bị ngắt trên màn hình.
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
        # chia n clip cho các scene trong khối theo tỉ lệ thời lượng, mỗi scene ≥0
        acc, given = 0.0, 0
        for j, r in enumerate(blk):
            acc += r["dur"]
            want = round(acc / d * n) - given
            r["nshot"] = max(0, want)
            given += r["nshot"]
        if given != n:      # bù sai số làm tròn vào scene dài nhất của khối
            max(blk, key=lambda r: r["dur"])["nshot"] += n - given

    # ── GATE 4: scene phải phủ liên tục, không hở không chồng ────────────────
    for a, b in zip(rows, rows[1:]):
        if abs(a["t1"] - b["t0"]) > 0.001:
            errs.append(f"scene {a['i']}→{b['i']}: hở/chồng {a['t1']:.2f} vs {b['t0']:.2f}")

    total = rows[-1]["t1"]
    art = [r for r in rows if r["kind"] == "art"]
    nshot = sum(r["nshot"] for r in rows)

    print(f"{'#':>3} {'giây':>14} {'dài':>6} {'kind':<7} {'shot':>4}  telop")
    print("─" * 78)
    for r in rows:
        print(f"{r['i']:>3} {r['t0']:>6.1f}-{r['t1']:>6.1f} {r['dur']:>6.1f} "
              f"{r['kind']:<7} {r['nshot'] or '·':>4}  {r['telop'].replace(chr(10),' / ')}")

    print("─" * 78)
    print(f"tổng {total:.1f}s = {total/60:.1f}′ · {len(rows)} scene "
          f"({len(art)} art · {sum(1 for r in rows if r['kind']=='stat')} stat · "
          f"{sum(1 for r in rows if r['kind']=='genten')} genten)")
    print(f"⭐ SỐ CLIP VEO PHẢI GEN: {nshot}")
    print(f"   {len(blocks)} khối art · scene dài nhất {max(r['dur'] for r in rows):.1f}s "
          f"(scene {max(rows, key=lambda r: r['dur'])['i']})")
    # scene art mà nhận 0 clip = nó DÙNG CHUNG clip với scene liền trước trong khối.
    share = [r['i'] for r in rows if r['kind'] == 'art' and r['nshot'] == 0]
    if share:
        print(f"   {len(share)} scene art dùng chung clip với scene trước: {share[:14]}"
              + (" …" if len(share) > 14 else ""))

    # nhịp đổi hình chính = số shot ÷ số phút. Trần 6/phút (`audience-45plus.md` §2).
    pace = nshot / (total / 60)
    print(f"   nhịp đổi hình: {pace:.1f}/phút " + ("✓" if pace <= 6.0 else "🔴 vượt trần 6"))

    # ── GATE 5: LẶP KHUÔN + LẶP ĐỘNG TÁC ────────────────────────────────────
    # 🔴 user 2026-09-08: *"cứ lặp đi lặp lại ông bà già nhìn chán đời quá"*. Đo lô 73 clip
    #    đầu: PERSON chiếm 52% và "nhìn ống kính"/"giơ tay" mỗi cụm 13 lần. Video mẫu thì
    #    ngược lại — rất ít khung "một cụ già ngồi nói", đa số là đám đông/biểu đồ/đống
    #    tiền/split/cận vật. ⇒ Gate này chặn cả HAI trục: tỉ lệ khuôn và cụm động tác.
    # 🔴 DÙNG CHUNG hàm `classify` của `flow22_full.py`, không tự phân loại lại. Bản đầu
    #    plan22 có bản sao logic riêng ⇒ nó báo PERSON 29% trong khi flow22 báo 27% trên
    #    CÙNG một bảng scene. Hai con số cho cùng một thứ = một trong hai sai, và không
    #    biết cái nào. Cùng bài học `feedback_gate_va_builder_phai_cung_ten`.
    import collections as _c
    import importlib
    _ff = importlib.import_module("flow22_full")
    bodies = [r["body"] for r in rows if r["kind"] == "art"]
    kinds = [_ff.classify(b) for b in bodies]
    kc = _c.Counter(kinds)
    ratio = kc.get("PERSON", 0) / max(1, len(kinds))
    if ratio > 0.35:
        errs.append(f"PERSON chiếm {ratio:.0%} scene art (trần 35%) — thêm CROWD/VIZ/MACRO")
    pbodies = [b for b, k in zip(bodies, kinds) if k == "PERSON"]
    # cụm tiếng ANH — mô tả đã dịch, dò tiếng Việt thì gate im lặng cho qua tất
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
    print("\n✓ 4 gate sạch")
    return rows


if __name__ == "__main__":
    build()
