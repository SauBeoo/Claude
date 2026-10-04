# -*- coding: utf-8 -*-
"""build_storyboard_01.py — STORYBOARD dang kich ban phim (INT./EXT. + hanh dong + loi) cho kinishinai bai 1.

Sinh tu 3 nguon da khoa (khong go tay de khong lech): SLIDES (_t/_dur that) + timeline.json (loi doc
dung tung dong) + _plan/storyboard_src.py (bang nhan vat/boi canh co dinh + hanh dong moi shot + file anh).
Kiem: moi tien to file anh khop DUNG 1 file trong lo; khong file nao dung 2 lan.
Ghi 03_SCRIPTS/<stem>_STORYBOARD.md. Chay: python tools/build_storyboard_01.py 01_kuchiguse-hitonome
"""
import sys, io, json, importlib.util
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
BATCH = "_user_raw/zip_0228"


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sp = importlib.util.spec_from_file_location("sb", vd / "_plan" / "storyboard_src.py")
    sb = importlib.util.module_from_spec(sp); sp.loader.exec_module(sb)
    sl = json.loads((PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json").read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))["lines"]
    files = sorted(p.name for p in (vd / BATCH).rglob("*.jpg"))
    used, err = {}, []
    def resolve(pref):
        hit = [f for f in files if f.startswith(pref)]
        if len(hit) != 1:
            err.append(f"tien to「{pref}」khop {len(hit)} file"); return None
        if hit[0] in used:
            err.append(f"{hit[0]} dung 2 lan (shot {used[hit[0]]})")
        return hit[0]

    out = ["# THE WATCHMAN IN YOUR HEART — 見張り番がささやく七つの口ぐせ",
           "",
           "> STORYBOARD kinishinai bài 1 · sinh bằng `tools/build_storyboard_01.py` từ SLIDES + `timeline.json` + `_plan/storyboard_src.py`. "
           "**Sửa hình/hành động → sửa `storyboard_src.py` rồi chạy lại, đừng sửa file này bằng tay.**",
           f"> Giọng: 夜語トバリ (một giọng, người kể = KIEKO) · {tl[-1]['end']/60:.2f}′ · {len(sl)} shot · phong cách **ảnh người thật** (lô `{BATCH}`).",
           "> Mọi lời dưới đây là **lời đọc thật** của bản voice (KIEKO V.O.). Thoại trong 「」 là Kieko thuật lại — không có giọng thứ hai.",
           "", "## NHÂN VẬT (mô tả cố định — dán nguyên cụm vào prompt khi gen lại)", "",
           "| nhân vật | vai | mô tả gen (EN) |", "|---|---|---|"]
    out += [f"| **{n}** | {r} | {d} |" for n, r, d in sb.CAST]
    out += ["", "## BỐI CẢNH", ""] + [f"- `{k}` — {v}" for k, v in sb.LOC.items()] + ["", "---", ""]

    stat = {"ok": 0, "new": 0, "redo": 0, "card": 0, "reveal": 0}
    last_loc = None
    for i, e in enumerate(sl):
        t0, t1 = e["_t"], e["_t"] + e["_dur"]
        lines = [l["text"] for l in tl if t0 - 0.01 <= l["start"] < t1 - 0.01]
        tc = f"{int(t0//60):02d}:{int(t0%60):02d}"
        if "card" in e:
            c = e["card"]
            if last_loc != "CARD":
                out.append("ON-SCREEN CARD\n")
            out.append(f"**SHOT {i:03d}** · {tc} · {e['_dur']:.1f}s · 🟦 thẻ `{c['type']}`: " + " ／ ".join(c.get("lines", [])) + "\n")
            last_loc = "CARD"; stat["card"] += 1
        elif "reveal" in e:
            if last_loc != "CARD":
                out.append("ON-SCREEN CARD\n")
            out.append(f"**SHOT {i:03d}** · {tc} · {e['_dur']:.1f}s · 🟨 chữ hiện dần: " + " ／ ".join(e["reveal"]["lines"]) + "\n")
            last_loc = "CARD"; stat["reveal"] += 1
        else:
            if i not in sb.S:
                err.append(f"shot {i}: thieu trong storyboard_src.S"); continue
            loc, act, pref, note = sb.S[i]
            if loc != last_loc:
                out.append(f"### {sb.LOC[loc]}\n")
            last_loc = loc
            if pref:
                f = resolve(pref); used[f] = i
                mark = "🔁 " + note if note.startswith("🔁") else f"🖼 `{f}`"
                stat["redo" if note.startswith("🔁") else "ok"] += 1
            else:
                mark = note or "🆕 cần gen"; stat["new"] += 1
            nn = "" if (not note or note.startswith(("🔁", "🆕"))) else f" · _{note}_"
            out.append(f"**SHOT {i:03d}** · {tc} · {e['_dur']:.1f}s{nn}\n\n{act}\n\n{mark}\n")
        out.append("KIEKO (V.O.)\n\n" + "\n".join(lines) + "\n")
        out.append("")
    out += ["FADE TO BLACK.", "", "---", "",
            f"**Tổng:** {len(sl)} shot · ảnh có sẵn {stat['ok']} · cần gen mới {stat['new']} · cần gen lại {stat['redo']} · thẻ font {stat['card']} · chữ hiện dần {stat['reveal']}.",
            f"Ảnh lô chưa dùng: " + ", ".join(f"`{f}`" for f in files if f not in used)]
    (PROJ / "03_SCRIPTS" / f"{stem}_STORYBOARD.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(stat)
    if err:
        print("🔴 LOI:"); [print("  -", x) for x in err]; sys.exit(1)
    print("✅ moi file anh khop dung 1 lan · chua dung:", [f for f in files if f not in used])


if __name__ == "__main__":
    main()
