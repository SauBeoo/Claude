# -*- coding: utf-8 -*-
"""pick_real.py — tai BAN GOC cac ung vien anh/video that da chon (_plan/picks.py), dua vao video.

- Anh  -> cover-crop 1920x1080 -> slides_img/slide_NN.jpg (SLIDES: photo+static, nhu cu).
- Video-> cat dung _dur (+0.3s), 1920x1080 30fps, KHONG tieng -> clips/clip_NN.mp4, SLIDES: "video": true.
- Nhap kho _media_library (add_file + used_by) = ghi SO DEN, video sau khong tai lai (media-library.md §2).
- O con lai (AI) -> viet lai _plan/img_prompts_FLOW.txt + _TENFILE.txt chi cho o AI.
Chay: python tools/pick_real.py 01_danshari-kokoro
"""
import sys, io, json, subprocess, urllib.request
from pathlib import Path
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
import media_lib as ML
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def dl(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as f:
        f.write(r.read())


def cover(src, dest, W=1920, H=1080):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im.crop((x, y, x + W, y + H)).save(dest, quality=93)


def main():
    stem = sys.argv[1]
    vd = PROJ / "06_VIDEO" / stem
    sys.path.insert(0, str(vd / "_plan"))
    from picks import P
    sl_path = PROJ / "03_SCRIPTS" / f"{stem}_SLIDES.json"
    sl = json.load(open(sl_path, encoding="utf-8"))
    cand = json.load(open(vd / "_cand" / "cand.json", encoding="utf-8"))
    raw = vd / "_real_raw"; raw.mkdir(exist_ok=True)
    img, clips = vd / "slides_img", vd / "clips"
    img.mkdir(exist_ok=True); clips.mkdir(exist_ok=True)
    idx = ML.load_index()
    n_p = n_v = 0
    for i, k in sorted(P.items()):
        it = cand[str(i)]["items"][k]
        e = sl[i]
        if it["kind"] == "photo":
            src = raw / f"{i:02d}_pexels_{it['id']}.jpg"
            if not src.exists():
                dl(it["orig"], src)
            cover(src, img / f"slide_{i:02d}.jpg")
            e.update({"photo": True, "static": True, "real": {"src": "pexels", "id": it["id"], "url": it["url"]}})
            e.pop("video", None)
            ML.add_file(src, "photo", source="pexels", source_id=str(it["id"]), url=it["url"],
                        query=cand[str(i)]["q"], used_by=f"yawa/{stem}", idx=idx, autosave=False)
            n_p += 1
        else:
            f = sorted(it["files"], key=lambda f: abs(f["width"] - 1920))[0]
            src = raw / f"{i:02d}_pexelsv_{it['id']}.mp4"
            if not src.exists():
                dl(f["link"], src)
            dur = e["_dur"] + 0.3
            out = clips / f"clip_{i:02d}.mp4"
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", f"{dur:.2f}", "-an",
                                "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
                                "-c:v", "libx264", "-crf", "18", str(out)])
            if r.returncode:
                raise SystemExit(f"[LOI] ffmpeg slide {i}")
            got = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                                 "-of", "csv=p=0", str(out)]))
            if got + 0.05 < e["_dur"]:
                print(f"  ⚠️ slide {i}: clip goc chi {got:.1f}s < slide {e['_dur']:.1f}s -> renderer se lap")
            e.update({"video": True, "real": {"src": "pexels-video", "id": it["id"], "url": it["url"]}})
            e.pop("photo", None); e.pop("static", None)
            ML.add_file(src, "clip", source="pexels", source_id=str(it["id"]), url=it["url"],
                        query=cand[str(i)]["q"], used_by=f"yawa/{stem}", idx=idx, autosave=False)
            n_v += 1
        print(f"slide {i:3d} <- {it['kind']} pexels {it['id']}")
    ML.save_index(idx)
    json.dump(sl, open(sl_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # viet lai prompt AI chi cho o chua co anh that
    plan = vd / "_plan"
    old = io.open(plan / "img_prompts_FLOW.txt", encoding="utf-8").read().strip().split("\n")
    ten = io.open(plan / "img_prompts_TENFILE.txt", encoding="utf-8").read().strip().split("\n")
    by_slide = {int(t.split("slide_")[1].split(".")[0]): p for t, p in zip(ten, old)}
    (plan / "img_prompts_FLOW_all143.txt").write_text("\n".join(old) + "\n", encoding="utf-8")
    keep = [(s, p) for s, p in sorted(by_slide.items()) if s not in P]
    (plan / "img_prompts_FLOW.txt").write_text("\n".join(p for _, p in keep) + "\n", encoding="utf-8")
    (plan / "img_prompts_TENFILE.txt").write_text(
        "\n".join(f"dong {n + 1:3d} -> slide_{s:02d}.png" for n, (s, _) in enumerate(keep)) + "\n", encoding="utf-8")
    print(f"THAT: {n_p} anh + {n_v} video | AI con lai: {len(keep)} o -> img_prompts_FLOW.txt")


if __name__ == "__main__":
    main()
