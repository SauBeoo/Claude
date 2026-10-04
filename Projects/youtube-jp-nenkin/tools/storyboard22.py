# -*- coding: utf-8 -*-
"""
storyboard22.py — STORYBOARD đầy đủ của video 22, để user gen ảnh.

Khác ba file đã có, đừng lẫn:
  · `flow22_full.py`   → prompt VIDEO (Veo), chia theo trần clip 8,7s ⇒ 73 clip
  · `img22_prompts.py` → prompt ẢNH, **bám đúng 73 slot của lô video** (bản lưng 1-đổi-1)
  · `storyboard22.py`  → **storyboard theo NHỊP HÌNH**, chia theo **sàn 9s** của
    `audience-45plus.md` §2.0b ⇒ số ô hình là con số TÍNH ĐƯỢC, không phải con số kế thừa
    từ trần clip của Veo. Đây là bản để **gen ẢNH**, nên trần 8s của Flow không liên quan.

🔴 VÌ SAO KHÔNG DÙNG LẠI 73: hai con số trả lời hai câu khác nhau —
   «một clip Veo phủ được mấy giây» (8,7) vs «ảnh chính được đứng bao lâu» (9,0).
   Gộp lại là đúng cái bệnh `feedback_phan_bo_theo_tran`: chia theo trần SAI thì vi phạm
   nhảy sang chỗ khác chứ không mất đi.

⚖️ Scene `stat` / `formula` / `genten` **KHÔNG cần ảnh** (Remotion vẽ bảng số + ảnh 原典 chụp
   thật). Storyboard vẫn LIỆT KÊ chúng, ghi rõ «không gen» — để user thấy vì sao có khoảng
   trống trong dãy số, thay vì tưởng bị thiếu.

Xuất vào `06_VIDEO/22_.../_storyboard/`:
  STORYBOARD.md    — bản người đọc: bảng ô hình + lời đọc + telop + mô tả + prompt
  sb22_FLOW.txt    — 1 prompt/dòng, bơm extension
  sb22_TENFILE.txt — dòng ↔ tên file đích ↔ scene ↔ khe giây
"""
import io, json, math, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")

from _scenes22 import SCENES                      # noqa: E402
from flow22_full import classify                  # noqa: E402
from img22_prompts import build_prompt, MOTION     # noqa: E402

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
OUT = os.path.join(VD, "_storyboard")
FLOOR = 9.0          # ảnh chính được đứng tối đa 9,0s (audience-45plus §2.0b)


def main():
    os.makedirs(OUT, exist_ok=True)
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))["lines"]

    rows = []
    for k, (ln, kind, telop, body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        t0 = tl[ln]["start"]
        t1 = tl[nxt]["start"] if nxt < len(tl) else tl[-1]["end"]
        say = " ".join(x["text"] for x in tl[ln:nxt] if x.get("text"))
        rows.append(dict(i=k, kind=kind, telop=telop, body=body, t0=t0, t1=t1,
                         dur=t1 - t0, say=say))

    # ── chia ô hình: mỗi scene art cần ceil(dur / 9,0) ảnh, chia đều trong scene ──
    shots, idx = [], 0
    for r in rows:
        if r["kind"] != "art":
            shots.append(dict(r, n=0, stem=None, prompt=None, sub=0, nsub=0,
                              a=r["t0"], b=r["t1"]))
            continue
        n = max(1, math.ceil(r["dur"] / FLOOR))
        step = r["dur"] / n
        for j in range(n):
            a = r["t0"] + step * j
            b = a + step
            stem = f"sb22_{idx+1:02d}_s{r['i']:02d}" + (f"_{j+1}" if n > 1 else "")
            shots.append(dict(r, n=n, sub=j + 1, nsub=n, a=a, b=b, stem=stem,
                              prompt=" ".join(build_prompt(r["body"], idx).split())))
            idx += 1

    imgs = [s for s in shots if s["stem"]]

    # ── GATE ───────────────────────────────────────────────────────────────
    errs = []
    for s in imgs:
        low = s["prompt"].lower().replace("explainer video", "explainer")
        for w in MOTION:
            if w in low:
                errs.append(f"{s['stem']}: còn từ chuyển động «{w.strip()}»")
    for s in imgs:                     # mỗi ô hình phải ≤ sàn
        if s["b"] - s["a"] > FLOOR + 0.05:
            errs.append(f"{s['stem']}: ô hình {s['b']-s['a']:.1f}s > sàn {FLOOR}s")

    # ── xuất ───────────────────────────────────────────────────────────────
    io.open(os.path.join(OUT, "sb22_FLOW.txt"), "w", encoding="utf-8").write(
        "\n".join(s["prompt"] for s in imgs) + "\n")
    io.open(os.path.join(OUT, "sb22_TENFILE.txt"), "w", encoding="utf-8").write(
        "\n".join(f"dong {i+1:>2} -> {s['stem']}.png   [scene {s['i']:>2} · {classify(s['body'])}"
                  f" · {s['a']:6.1f}-{s['b']:6.1f}s ({s['b']-s['a']:.1f}s)"
                  + (f" · ô {s['sub']}/{s['nsub']}" if s["nsub"] > 1 else "") + "]"
                  for i, s in enumerate(imgs)) + "\n")

    md = ["# STORYBOARD — video 22 「消える三十六万円の謎」",
          "",
          f"Video **{rows[-1]['t1']:.0f}s = {rows[-1]['t1']/60:.1f}′** · **{len(rows)} scene** · "
          f"**{len(imgs)} ô hình phải gen** · khổ **16:9**.",
          "",
          "Chia ô theo **sàn 9,0s** (`audience-45plus.md` §2.0b — ảnh chính không được đứng lâu hơn). "
          "Scene `stat`/`formula`/`genten` **không gen ảnh**: Remotion vẽ bảng số bằng font, "
          "ảnh 原典 là screenshot thật.",
          "",
          "⚠️ Gen xong: **soi ✦ watermark cả 4 góc** (`media-library.md` §2.10 ⑤) và "
          "**không dùng lại một ảnh ở hai ô** (`feedback_slide_khong_trung_anh_trong_video`).",
          ""]
    cur = None
    for s in shots:
        if s["i"] != cur:
            cur = s["i"]
            md += ["", f"## Scene {s['i']:02d} · {s['t0']:.1f}–{s['t1']:.1f}s "
                       f"({s['dur']:.1f}s) · `{s['kind']}`"
                       + (f" · khuôn **{classify(s['body'])}**" if s["kind"] == "art" else ""),
                   "",
                   f"**Telop:** {s['telop'].replace(chr(10), ' / ')}", ""]
            if s["say"]:
                md += [f"**Lời đọc:** {s['say'][:400]}", ""]
        if not s["stem"]:
            what = ("thẻ số liệu `papercut-stat`" if s["kind"] == "stat"
                    else "thẻ công thức `papercut-formula`" if s["kind"] == "formula"
                    else f"ảnh 原典 `{s['body']}`")
            md += [f"— *không gen ảnh: {what}*", ""]
            continue
        md += [f"### `{s['stem']}.png` — {s['a']:.1f}–{s['b']:.1f}s ({s['b']-s['a']:.1f}s)"
               + (f" · ô {s['sub']}/{s['nsub']}" if s["nsub"] > 1 else ""),
               "",
               f"**Hình:** {s['body']}", "",
               "```", s["prompt"], "```", ""]
    io.open(os.path.join(OUT, "STORYBOARD.md"), "w", encoding="utf-8").write("\n".join(md))

    n_no = sum(1 for s in shots if not s["stem"])
    print(f"⭐ {len(imgs)} ô hình phải gen  ·  {n_no} scene không cần ảnh")
    print(f"   nhịp: {len(imgs)/(rows[-1]['t1']/60):.1f} đổi ảnh/phút (trần 6,0) "
          + ("✓" if len(imgs)/(rows[-1]['t1']/60) <= 6 else "🔴"))
    print(f"   ô dài nhất {max(s['b']-s['a'] for s in imgs):.1f}s (sàn {FLOOR}) · "
          f"ngắn nhất {min(s['b']-s['a'] for s in imgs):.1f}s")
    print(f"   dài prompt {min(len(s['prompt']) for s in imgs)}–"
          f"{max(len(s['prompt']) for s in imgs)} ký")
    print(f"   -> {OUT}\\STORYBOARD.md · sb22_FLOW.txt · sb22_TENFILE.txt")
    if errs:
        print("\n🔴 GATE:")
        for e in errs[:15]:
            print("  ", e)
        sys.exit(1)
    print("\n✓ GATE SẠCH: không từ chuyển động · mọi ô ≤ sàn 9s")


if __name__ == "__main__":
    main()
