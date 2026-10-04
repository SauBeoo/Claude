# -*- coding: utf-8 -*-
"""
sb_i2v_prompts.py — từ bản xuất JSON của **Storyboard Studio** (Google Flow) ra:
  ① prompt **image-to-video** cho từng frame (dán vào Flow, ảnh đã là frame đầu)
  ② sổ tên file ↔ scene/shot ↔ độ dài khe cần phủ
  ③ bảng chẩn: frame nào vượt trần 8s của Flow ⇒ cần mấy clip

Vì sao có file này: bản xuất JSON đã chứa **`motionDescription` cho từng frame** — tức phần
khó nhất của prompt i2v đã có sẵn, chỉ cần (a) bọc guard của kênh (b) khớp thứ tự với ảnh đã
bóc (c) đối chiếu với ĐỘ DÀI KHE thật trong `timeline.json`, vì Flow **trần 8,000s/clip**.

🔴 HAI THỨ PHẢI SỬA trong `motion` của Storyboard Studio trước khi đem đi gen:
 ① **Chuyển động MÁY QUAY** (`slow zoom in`, `pan across`, `dolly`, `quick cut`) — kênh này
    cấm Ken Burns/khung trôi (`feedback_video_no_motion_mot_giong`, và lớp Remotion đặt
    photocard tĩnh). ⇒ đổi sang **máy đứng, chủ thể động**. Cờ `--keep-camera` giữ nguyên
    nếu bao giờ user muốn thử.
 ② **`quick cut from A to B`** = MỘT LỆNH DỰNG, không phải chuyển động trong một shot; để
    nguyên thì Veo cắt cảnh giữa clip ⇒ ảnh nhân vật đổi giữa 8 giây, phá character-lock.
    ⇒ đổi thành "giữ đúng khung của ảnh, chỉ chủ thể động".

⚖️ Prompt i2v **KHÔNG tả lại nội dung ảnh** — ảnh đã là frame đầu. Tả lại là mời model vẽ lại
   (đúng bài học "ảnh là reference chứ không phải frame đầu" ở `still22_prompts.py`).
"""
import argparse, base64, collections, io, json, math, os, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

VD = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man"
SHOT_MAX = 8.0          # trần 1 clip Flow/Veo
FLOOR = 9.0             # sàn "ảnh chính đổi ≤9s" (audience-45plus §2.0b)

# ── guard của kênh, dán vào MỌI prompt i2v ──────────────────────────────────
GUARD = ("Keep the framing, composition, characters, clothing, props and colours of the "
         "given image exactly as they are; the camera stays locked off and does not move, "
         "no zoom, no pan, no cut to another shot. Only what is described above moves, "
         "once, slowly, and it holds still for the rest of the shot. Any printing on paper "
         "or screens stays exactly as in the image; no new text appears, no captions, "
         "no watermark, no logo.")

# ① máy quay → chủ thể (bảng TÊN, không regex chung: mỗi câu là một ý khác nhau)
CAM = [
    (r"\ba (?:slow|gentle|slow, gentle|gentle, slow)[^.]*zoom in[^.]*",
     "the subject holds the pose and only breathes and blinks"),
    (r"\bslow zoom[^.]*", "the subject holds the pose and only breathes and blinks"),
    (r"\ba quick cut from [^.]*", "the subject holds the pose while the hands settle"),
    (r"\bquick cut[^.]*", "the subject holds the pose while the hands settle"),
    (r"\b(?:a )?(?:slow )?pan (?:across|over|to)[^.]*",
     "the subject holds still and only the light and small details shift"),
    (r"\b(?:a )?(?:slow )?dolly[^.]*", "the subject holds still, breathing slowly"),
    (r"\b(?:the )?camera (?:slowly )?(?:pushes|moves|tracks|tilts|zooms)[^.]*",
     "the camera stays locked off and the subject moves once, slightly"),
    (r"\bcross[- ]?dissolve[^.]*", "the image holds and the subject moves once, slightly"),
    (r"\bcuts? to[^.]*", "the subject holds the pose"),
]
CAMWORD = re.compile(r"zoom|pan\b|dolly|camera (?:push|move|track|tilt)|cut to|quick cut|"
                     r"dissolve|truck|crane", re.I)


def demote_camera(motion: str) -> str:
    out = motion
    for pat, rep in CAM:
        out = re.sub(pat, rep, out, flags=re.I)
    return re.sub(r"\s+", " ", out).strip()


def scene_gaps():
    """Độ dài khe thật của từng scene `art` trong bảng scene của video 22."""
    tl = json.load(io.open(os.path.join(VD, "timeline.json"), encoding="utf-8"))["lines"]
    sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
    from _scenes22 import SCENES
    out = []
    for k, (ln, kind, telop, body) in enumerate(SCENES):
        nxt = SCENES[k + 1][0] if k + 1 < len(SCENES) else len(tl)
        t0 = tl[ln]["start"]
        t1 = tl[nxt]["start"] if nxt < len(tl) else tl[-1]["end"]
        if kind == "art":
            out.append((k, t1 - t0))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None, help="bản xuất Storyboard Studio (.json)")
    ap.add_argument("--dir", default=os.path.join(VD, "_sb63"), help="thư mục ảnh đã bóc")
    ap.add_argument("--keep-camera", action="store_true", help="giữ nguyên lệnh máy quay")
    a = ap.parse_args()

    man = os.path.join(a.dir, "_MANIFEST.json")
    if a.json:                      # bóc lại từ JSON gốc (ảnh + manifest)
        d = json.load(io.open(a.json, encoding="utf-8"))
        os.makedirs(a.dir, exist_ok=True)
        rows = []
        for i, f in enumerate(d["frames"], 1):
            stem = f"sb_{i:02d}_s{f['sceneNumber']}sh{f['shotNumber']}"
            b64 = (f.get("base64") or "").split(",")[-1]
            if b64:
                raw = base64.b64decode(b64)
                io.open(os.path.join(a.dir, stem + ".jpg"), "wb").write(raw)
            rows.append(dict(idx=i, file=stem + ".jpg", scene=f["sceneNumber"],
                             shot=f["shotNumber"], sceneTitle=f["sceneTitle"],
                             title=f["title"], visual=f["visualDescription"],
                             motion=f["motionDescription"], audio=f["audioDescription"],
                             kb=len(b64) // 1024))
        io.open(man, "w", encoding="utf-8").write(json.dumps(rows, ensure_ascii=False, indent=1))
        print(f"boc lai: {len(rows)} anh -> {a.dir}")
    rows = json.load(io.open(man, encoding="utf-8"))

    gaps = scene_gaps()
    flow, tens = [], []
    n_cam = 0
    for i, r in enumerate(rows):
        motion = r["motion"]
        if CAMWORD.search(motion):
            n_cam += 1
        if not a.keep_camera:
            motion = demote_camera(motion)
        flow.append(" ".join(f"{motion} {GUARD}".split()))
        # khe tương ứng: frame i ↔ scene art thứ i (63 frame ↔ 62 scene art, gần 1:1)
        gap = gaps[i][1] if i < len(gaps) else 0.0
        nclip = max(1, math.ceil(gap / SHOT_MAX)) if gap else 1
        tens.append(f"dong {i+1:>2} -> {r['file']:<22} S{r['scene']}-{r['shot']} · "
                    f"khe {gap:5.1f}s · {nclip} clip"
                    + ("  🔴 >9s: can chia them anh" if gap > FLOOR else ""))

    io.open(os.path.join(a.dir, "i2v_prompts.txt"), "w", encoding="utf-8").write("\n".join(flow) + "\n")
    io.open(os.path.join(a.dir, "i2v_TENFILE.txt"), "w", encoding="utf-8").write("\n".join(tens) + "\n")
    io.open(os.path.join(a.dir, "i2v_PROMPTS.md"), "w", encoding="utf-8").write(
        "# Prompt image-to-video — 63 frame Storyboard Studio (video 22)\n\n"
        "Ảnh đã là **frame đầu**; prompt chỉ nói CHUYỂN ĐỘNG. Trần Flow **8,000s/clip**.\n\n"
        + "\n".join(f"### {r['file']} — S{r['scene']}-{r['shot']} · {r['title']}\n\n"
                    f"```\n{p}\n```\n" for r, p in zip(rows, flow)))

    need = sum(math.ceil(g / SHOT_MAX) for _, g in gaps)
    over = [i + 1 for i, (_, g) in enumerate(gaps) if g > FLOOR]
    print(f"\n{len(flow)} prompt i2v -> {a.dir}\\i2v_prompts.txt")
    print(f"  cau lenh may quay da doi: {n_cam}/{len(rows)}"
          + ("  (giu nguyen theo --keep-camera)" if a.keep_camera else ""))
    print(f"  scene art: {len(gaps)} · tong {sum(g for _, g in gaps):.0f}s")
    print(f"  clip can neu tran 8s: {need}  (63 anh ⇒ thieu {need - len(rows)})")
    print(f"  khe >9s (san 45+): {len(over)} scene {over[:12]} ⇒ can them anh, khong keo dai anh cu")


if __name__ == "__main__":
    main()
