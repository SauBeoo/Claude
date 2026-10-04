# -*- coding: utf-8 -*-
"""deliver.py — round-trip: render project → chuẩn pipeline 06_VIDEO/<stem>/.

Steps:
  1. render (npx remotion render) unless --mp4 given — LONG: run this whole
     tool in background per workspace rule render-background.md
  2. ffmpeg loudnorm I=-14:TP=-1.5:LRA=9 (video copy, audio re-encode aac)
  3. export clean subs.srt from captions.lines
  4. place <stem>.mp4 + subs.srt into <channel project>/06_VIDEO/<stem>/

Usage:
  py -3 tools/deliver.py --project cabbage-34 --channel health
      --stem 34_cabbage-asa-yoru [--mp4 out/cabbage-34.mp4] [--dest <dir>]
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CHANNELS_TOOLS = Path(r"E:\Claude\Projects\youtube-jp-health\tools")


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd))
    r = subprocess.run(cmd, **kw)
    if r.returncode != 0:
        raise SystemExit(f"[LOI] lenh exit {r.returncode}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--channel", required=True)
    ap.add_argument("--stem", required=True)
    ap.add_argument("--mp4", default=None, help="mp4 da render san (bo qua buoc render)")
    ap.add_argument("--dest", default=None, help="ghi de thu muc dich (mac dinh 06_VIDEO/<stem>)")
    args = ap.parse_args()

    proj_file = ROOT / "projects" / args.project / "project.json"
    project = json.loads(proj_file.read_text(encoding="utf-8"))
    fps = project["meta"]["fps"]
    total = project["timeline"]["durationInFrames"] / fps

    # 1. render
    if args.mp4:
        raw_mp4 = Path(args.mp4)
    else:
        raw_mp4 = ROOT / "out" / f"{args.project}.mp4"
        run(["npx.cmd" if sys.platform == "win32" else "npx",
             "remotion", "render", "VoxProject",
             f"--props={proj_file}", str(raw_mp4), "--overwrite"], cwd=ROOT, shell=False)
    if not raw_mp4.exists():
        raise SystemExit(f"[LOI] khong thay {raw_mp4}")

    # 2. Xu ly GIONG theo dung ho so kenh (chuan project_loudness_14_lufs)
    #
    # 🔴 VA 2026-08-16: truoc day cho o day la `loudnorm=I=-14:TP=-1.5:LRA=9` CUNG,
    # tuc duong remotion-vox AM THAM BO 2 lop ma renderer cua kenh co:
    #   (a) acompressor — nang cau tam tinh/thi tham len, "khong chi to dinh"
    #   (b) equalizer +4dB @3kHz — dai PHU AM, cho presbycusis mat truoc nhat
    #       (user chot 2026-07-31 sau khi duyet A/B BANG TAI, channels.py voice_af)
    # Do tren video 16 (doan 42s quanh dinh bai): p10 (doan NHO NHAT) -25.6 dBFS voi
    # loudnorm tran vs -23.2 dBFS voi voice_af cua kenh => chenh 2.4 dB dung o cho
    # nguoi gia nghe khong ro. Loudnorm tong the thi CA HAI deu ra -14, nen nhin
    # con so tong KHONG thay loi — phai do phan bo.
    # Tu nay: LAY voice_af CUA KENH; khong co thi moi fallback ve loudnorm tran.
    sys.path.insert(0, str(CHANNELS_TOOLS))
    import channels as CH  # noqa: E402
    prof = CH.get(args.channel)
    if args.dest:
        dest = Path(args.dest)
    else:
        dest = Path(CH.project_dir(args.channel)) / prof["video_dir"] / args.stem
    dest.mkdir(parents=True, exist_ok=True)
    final_mp4 = dest / f"{args.stem}.mp4"
    # Fallback phai la VOICE_AF cua video_render.py (co acompressor), KHONG phai
    # loudnorm tran: video_render lam `voice_af or VOICE_AF`, nen kenh khong khai
    # voice_af (health/co-dai/nenkin/showa...) van duoc nen dai dong. Lay thang tu
    # module do de hai duong khong bao gio lech nhau nua.
    import importlib
    _vr = importlib.import_module("video_render")
    af = prof.get("voice_af") or _vr.VOICE_AF
    print(f"[audio] voice_af ({args.channel}): {af}")
    run(["ffmpeg", "-y", "-i", str(raw_mp4),
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-af", af,
         str(final_mp4)])

    # 3. clean srt (bo qua neu project khong co phu de)
    if project.get("captions", {}).get("lines"):
        run([sys.executable, str(ROOT / "tools" / "export_srt.py"),
             "--project", args.project, "--out", str(dest / "subs.srt")])
    else:
        print("(khong co captions.lines — bo qua subs.srt)")

    # 4. verify duration khop
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(final_mp4)],
                       capture_output=True, text=True)
    dur = float(r.stdout.strip())
    drift = abs(dur - total)
    print(f"duration mp4 {dur:.1f}s vs timeline {total:.1f}s (lech {drift:.1f}s)")
    if drift > 2.0:
        print("⚠ LECH >2s — kiem tra lai truoc khi dang")
    print(f"OK → {final_mp4}")
    if (dest / "subs.srt").exists():
        print(f"OK → {dest / 'subs.srt'}")
    print("NHO: duyet >=4 frame bang mat + upload srt tay (khong auto-caption)")


if __name__ == "__main__":
    main()
