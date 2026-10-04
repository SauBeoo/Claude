# -*- coding: utf-8 -*-
r"""ingest_clips_23.py — nhan LO 92 CLIP t2v cua video 23 (年金請求書が届かない) vao Remotion.

NGUON: F:\Youtube\Du_an_moi_33_hj72unn2\task_001..task_092_1_1080p.mp4
  Lo do extension bom `vox23_FLOW.txt` (92 dong) theo DUNG THU TU => task_NNN = dong NNN.
  Khac han ca v22 (`ingest_c22.py`): o do ten file la CAPTION nen phai soi mat tung clip;
  o day ten file la SO THU TU cua chinh prompt, nen map la xac dinh, khong fuzzy.
  🔴 Van phai soi sheet nghiem thu — xem `--sheet`.

BA VIEC (va mot viec CO Y KHONG LAM):
  (1) DOI TEN theo khe: dong NNN cua `vox23_TENFILE.txt` ghi san `clips/clip_<beat><k>.mp4`.
      `beat` = CHI SO SCENE cua `plan23.build()` => builder va ingest khong the lech ten
      (`feedback_gate_va_builder_phai_cung_ten`).
  (2) BO AUDIO. Clip Veo co track AAC rac (tieng nen do model bia ra).
  (3) COPY STREAM, khong re-encode: da do ca 92 file = 1920x1080 @ 24/1 fps, 192 frame,
      8.000s — dung y khuon dich. Re-encode o day chi lam mat net, khong duoc gi.
      Neu lo sau khac spec thi nhanh `scale+fps` tu bat (xem `need_encode`).
  (4) ⛔ KHONG CAT WATERMARK — da soi 1:1 goc duoi-phai cua **ca 92 clip** (sheet
      `brsheet.png`, 10x10 tile @130x75) va ca 4 goc cua 3 clip: KHONG co dau (*) nao.
      Lo t2v thuan cua Flow khong dong (*) (giong lo `c22_*`); lo i2v thi CO vi (*) den tu
      anh start-frame. => Day la ket luan DO DUOC cho lo NAY, khong phai mien tru vinh vien:
      lo sau van phai soi lai (`media-library.md` §2.10 ⑤b — vi tri va co (*) doi theo lo).

RESUME so **mtime** nguon vs dich, khong so "da ton tai chua" (`render-background.md` §2.5).

CHAY:  python tools/ingest_clips_23.py            # tat ca
       python tools/ingest_clips_23.py --check    # chi kiem, khong dung ffmpeg
       python tools/ingest_clips_23.py --sheet    # xuat sheet nghiem thu 92 frame
       python tools/ingest_clips_23.py clip_0a clip_3b
"""
import glob
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 🔴 Thu muc nguon co ky tu tieng Viet co dau. KHONG go ten do vao code:
#    · chuoi RAW khong bung escape \uXXXX => ra ten sai, va sai IM LANG (tool bao
#      "thieu task_001" chu khong bao "khong thay thu muc").
#    · heredoc/f-string thi \1.. lai thanh escape octal (`render-background.md` §2.6 ⑥).
#    => Dinh vi bang GLOB theo phan ASCII (ma Flow tu sinh), khong go phan co dau.
_HITS = sorted(glob.glob(os.path.join("F:" + os.sep, "Youtube", "*33_hj72unn2")))
SRC = _HITS[0] if _HITS else ""
VD = (r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO"
      r"\23_nenkin-seikyusho-todokanai")
TENFILE = os.path.join(VD, "vox23_TENFILE.txt")
OUT = r"E:\Claude\Projects\remotion-vox\public\projects\nenkin-23\assets"

W, H, FPS, DUR = 1920, 1080, 24, 8.000
LINE_RE = re.compile(r"^dong\s+(\d+)\s*->\s*clips/(clip_[0-9a-z]+)\.mp4")


def read_map():
    """dong NNN -> (ten khe, ghi chu). Nguon su that = vox23_TENFILE.txt."""
    rows = {}
    for ln in io.open(TENFILE, encoding="utf-8"):
        m = LINE_RE.match(ln.strip())
        if m:
            rows[int(m.group(1))] = (m.group(2), ln.strip())
    return rows


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate",
         "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.split()
    if not out:
        return None
    vid = out[0].split(",")
    dur = float(out[1]) if len(out) > 1 else 0.0
    num, den = vid[2].split("/")
    return int(vid[0]), int(vid[1]), int(num) / int(den), dur


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    sheet = "--sheet" in sys.argv

    rows = read_map()
    if len(rows) != 92:
        print(f"🔴 TENFILE doc duoc {len(rows)} dong, cho 92 — bang map da doi, DUNG.")
        return 1
    os.makedirs(OUT, exist_ok=True)

    miss, bad, done, skip = [], [], 0, 0
    plan = []
    for n in sorted(rows):
        stem, note = rows[n]
        if args and stem not in args:
            continue
        src = os.path.join(SRC, f"task_{n:03d}_1_1080p.mp4")
        dst = os.path.join(OUT, f"{stem}.mp4")
        if not os.path.exists(src):
            miss.append(f"dong {n} ({stem}): thieu {os.path.basename(src)}")
            continue
        p = probe(src)
        if p is None:
            bad.append(f"{stem}: ffprobe khong doc duoc")
            continue
        w, h, fps, dur = p
        if abs(dur - DUR) > 0.05:
            bad.append(f"{stem}: dai {dur:.3f}s (cho {DUR})")
        need_encode = (w, h) != (W, H) or abs(fps - FPS) > 0.01
        plan.append((n, stem, src, dst, need_encode))

    if miss or bad:
        print("🔴 LO NGUON CO VAN DE:")
        for e in (miss + bad)[:20]:
            print("  ", e)
        if miss:
            return 1

    if sheet:
        return make_sheet(plan, rows)

    for n, stem, src, dst, enc in plan:
        if (os.path.exists(dst)
                and os.path.getmtime(dst) >= os.path.getmtime(src)):
            skip += 1
            continue
        if os.path.exists(dst):
            print(f"   {stem}: dich CU HON nguon -> lam lai")
        if check:
            print(f"   [check] {stem} <- task_{n:03d}"
                  + ("  (RE-ENCODE)" if enc else "  (copy)"))
            continue
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-an"]
        if enc:
            cmd += ["-vf", f"scale={W}:{H}:flags=lanczos,fps={FPS}",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
                    "-pix_fmt", "yuv420p"]
        else:
            cmd += ["-c:v", "copy"]
        cmd += [dst]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print(f"🔴 {stem}: ffmpeg loi\n{r.stderr[:400]}")
            return 1
        done += 1
        print(f"   {stem:<12} <- task_{n:03d}"
              + ("  RE-ENCODE" if enc else ""))

    print(f"\n✓ {done} clip moi · {skip} giu nguyen (dich moi hon nguon) "
          f"· tong {len(plan)}")
    print(f"   -> {OUT}")
    if not check and done + skip != len(plan):
        print("🔴 so clip khong khop — dung lai, dung render")
        return 1
    return 0


def make_sheet(plan, rows):
    """Sheet nghiem thu: 1 frame/clip, in kem SO DONG de doi chieu voi TENFILE."""
    tmp = os.path.join(VD, "_sheet23")
    os.makedirs(tmp, exist_ok=True)
    for i, (n, stem, src, dst, _) in enumerate(plan, 1):
        f = os.path.join(tmp, f"s{i:03d}.png")
        if os.path.exists(f):
            continue
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "4", "-i", src,
                        "-frames:v", "1", "-vf", "scale=320:180", f],
                       capture_output=True)
    for k, lo in enumerate(range(0, len(plan), 24)):
        chunk = plan[lo:lo + 24]
        out = os.path.join(VD, f"_SHEET23_{k}.png")
        cmd = ["ffmpeg", "-y", "-v", "error"]
        for i in range(lo + 1, lo + len(chunk) + 1):
            cmd += ["-i", os.path.join(tmp, f"s{i:03d}.png")]
        n = len(chunk)
        fc = "".join(f"[{i}:v]" for i in range(n)) + f"xstack=inputs={n}:layout="
        fc += "|".join(f"{(i % 6) * 320}_{(i // 6) * 180}" for i in range(n))
        cmd += ["-filter_complex", fc, "-frames:v", "1", out]
        subprocess.run(cmd, capture_output=True)
        print(f"   sheet {k}: dong {lo+1}-{lo+len(chunk)} -> {out}")
        for n2, stem, _, _, _ in chunk:
            print(f"      {n2:>3} {stem:<12} {rows[n2][1].split(']')[-1].strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
