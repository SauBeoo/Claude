# -*- coding: utf-8 -*-
r"""add_fx.py — gán FX + AVATAR vào SLIDES.json THEO TỪNG CÂU NÓI, đúng giây câu đó vang lên.

user chốt 2026-08-18: avatar ảnh thật + **FX dày, mỗi 30–40 giây một cái**.
Chạy SAU `autofocus.py` (autofocus lo mode/focus; tool này chỉ thêm `fx`/`avatar`).

    python add_fx.py <SLIDES.json> --timeline <timeline.json> [--apply]

🔴 BÀI HỌC BẢN ĐẦU (2026-08-18): bản đầu duyệt theo ENTRY nên
  · chỉ ra 19 FX / 20 phút = mỗi 64 giây — không phải "dày"
  · và **mất avatar của mẹ**: câu thoại 「お客さんの来る家は…」 lặp 2 lần nên entry của nó
    bị SKIP trong gen_slides (không substring nào tách được hai dòng y hệt nhau)
⇒ Bản này duyệt **TỪNG DÒNG timeline**, tìm entry đang hiển thị lúc dòng đó vang lên, và
  đặt `t` = offset trong clip. FX bám đúng chữ, không bám câu đầu của khung.

LUẬT ÁNH XẠ
  「…」 thoại              → avatar + bong bóng (mẹ nói → haha_talk · còn lại kataribe_talk)
  白状します / 正直に申し上げ → avatar kataribe_wry (tự trào)
  〜ではありません / 逆効果   → ✗ sáp đỏ
  số + 度/秒/分/時間/日      → con dấu tròn mang chính con số đó
  〜てください               → nhãn giấy, chữ lấy từ BẢNG ĐỘNG TỪ (không cắt giữa từ)
  ところが / じつは          → vệt mực quét (đảo nhận thức)
"""
import argparse, io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                              line_buffering=True, write_through=True)

NUM = re.compile(r"(\d+(?:\.\d+)?)\s*(度|秒|分|時間|日|リットル|センチ)")
NEG = ("ではありません", "ではなく", "逆効果", "効きません", "間違い", "限りません")
TWIST = ("ところが", "じつは", "実は", "逆に")
VERB = [("閉め", "閉める"), ("開け", "開ける"), ("拭", "拭く"), ("なで", "なでる"),
        ("かけ", "かける"), ("落とし", "落とす"), ("流し", "流す"), ("外し", "外す"),
        ("持ち上げ", "持ち上げる"), ("巻い", "巻く"), ("戻し", "戻す"), ("沈め", "沈める"),
        ("入れ", "入れる"), ("止め", "止める"), ("置い", "置く"), ("当て", "当てる")]
MAX_OFF = 18.0          # FX không được đặt quá muộn trong clip (clip dài 30s)


def free_spot(s, high=True):
    """Chỗ TRỐNG của khung: tránh vòng khoanh (mode focus) và card inset.
    🔴 Bản đầu để cố định [0.72, 0.30] nên dấu ✗ đè thẳng lên vòng khoanh — soi frame
    mới thấy. FX và thứ nó chú thích phải ở hai phía."""
    mode = s.get("mode")
    if mode == "focus":
        fx = (s.get("focus") or [0.5, 0.5, 0.15])[0]
        return [0.24 if fx > 0.5 else 0.76, 0.26 if high else 0.62]
    if mode == "inset":
        pos = s.get("inset_pos", "bl")          # card ở nửa dưới
        return [0.74 if pos.endswith("l") else 0.26, 0.22]
    return [0.74, 0.26]


def pick_tag(text):
    if "ください" not in text:
        return None
    for key, lab in VERB:
        if key in text:
            return lab
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slides")
    ap.add_argument("--timeline", required=True)
    ap.add_argument("--min-gap", type=float, default=26.0)
    ap.add_argument("--channel", default="co-dai")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    sp = Path(a.slides)
    cfg = json.loads(sp.read_text(encoding="utf-8"))
    tl = json.loads(Path(a.timeline).read_text(encoding="utf-8"))["lines"]

    # entry -> giây bắt đầu (theo dòng đầu tiên chứa `match`)
    ent = []
    for i, e in enumerate(cfg):
        m = e.get("match", "")
        hit = next((l for l in tl if m and m in l["text"]), None)
        if hit:
            ent.append((hit["start"], i))
    ent.sort()

    def entry_at(sec):
        cur = None
        for st, i in ent:
            if st <= sec + 0.01:
                cur = (st, i)
            else:
                break
        return cur

    for e in cfg:
        s = e.get("shot")
        if isinstance(s, dict):
            s.pop("fx", None)
            s.pop("avatar", None)

    last = -999.0
    seen_stamp, run_cross = {}, 0
    n = {"avatar": 0, "cross": 0, "stamp": 0, "tag": 0}

    for line in tl:
        st, text = line["start"], line["text"]
        if st - last < a.min_gap:
            continue
        cur = entry_at(st)
        if cur is None:
            continue
        e_st, i = cur
        s = cfg[i].get("shot")
        if not isinstance(s, dict):       # thẻ vox tự có hiệu ứng, không chồng lên
            continue
        off = st - e_st
        if off > MAX_OFF:
            continue

        q = re.search(r"「([^」]{4,40})」", text)
        if q and not s.get("avatar"):
            body = q.group(1)
            who = "haha_talk" if ("のよ" in body or "わよ" in body) else "kataribe_talk"
            s["avatar"] = {"name": who, "side": "right",
                           "t": round(min(max(0.8, off), 1.6), 2),   # nguoi vao som
                           "bubble_t": round(max(1.4, off), 2),      # bong bong dung luc thoai
                           "bubble": body, "channel": a.channel}
            s["mode"] = "soft"          # 🔴 avatar + card inset + vong khoanh trong MOT khung
            s.pop("inset_pos", None)     #    = ba lop chong nhau; soi frame that da thay ro
            last, run_cross = st, 0
            n["avatar"] += 1
            print(f"  e{i:<3} {st/60:5.1f}′ +{off:4.1f}s  avatar {who:<14}「{body[:20]}」")
            continue

        if ("白状します" in text or "正直に申し上げ" in text) and not s.get("avatar"):
            s["avatar"] = {"name": "kataribe_wry", "side": "right",
                           "t": round(min(max(0.8, off), 1.6), 2), "channel": a.channel}
            s["mode"] = "soft"          # 🔴 avatar + card inset + vong khoanh trong MOT khung
            s.pop("inset_pos", None)     #    = ba lop chong nhau; soi frame that da thay ro
            last, run_cross = st, 0
            n["avatar"] += 1
            print(f"  e{i:<3} {st/60:5.1f}′ +{off:4.1f}s  avatar kataribe_wry (tự trào)")
            continue

        if s.get("fx"):
            continue

        if any(w in text for w in NEG) and run_cross < 2:
            s["fx"] = [{"kind": "cross", "at": free_spot(s), "t": round(max(1.2, off), 2)}]
            last = st
            run_cross += 1
            n["cross"] += 1
            print(f"  e{i:<3} {st/60:5.1f}′ +{off:4.1f}s  ✗ cross     {text[:26]}")
            continue

        mn = NUM.search(text)
        if mn:
            key = mn.group(0).replace(" ", "")
            if st - seen_stamp.get(key, -999.0) >= 180:
                seen_stamp[key] = st
                s["fx"] = [{"kind": "stamp", "text": key, "at": free_spot(s),
                            "t": round(max(1.2, off), 2)}]
                last, run_cross = st, 0
                n["stamp"] += 1
                print(f"  e{i:<3} {st/60:5.1f}′ +{off:4.1f}s  ⊙ stamp {key:<6} {text[:22]}")
                continue

        tag = pick_tag(text)
        if tag:
            s["fx"] = [{"kind": "tag", "text": tag, "at": free_spot(s), "size": 64,
                        "t": round(max(1.2, off), 2)}]
            last, run_cross = st, 0
            n["tag"] += 1
            print(f"  e{i:<3} {st/60:5.1f}′ +{off:4.1f}s  ▭ tag「{tag}」  {text[:22]}")
            continue

        # ⛔ `smudge` DA BO (2026-08-18): dung o 5 cho, soi frame that thi no chi la mot
        #    vet muc do giua khung — khong tai nghia gi, va lam ban anh. Cau ところが/じつは
        #    da co cu lat trong CHU va trong giong doc; khong can them vet.

    dur = tl[-1]["end"] if tl else 0
    tot = sum(n.values())
    print(f"\n{n} · tổng {tot} trên {dur/60:.1f}′ = mỗi {dur/max(tot,1):.0f} giây một hiệu ứng")
    if a.apply:
        sp.write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[OK] đã ghi {sp}")
    else:
        print("(xem trước — thêm --apply để ghi)")


if __name__ == "__main__":
    main()
