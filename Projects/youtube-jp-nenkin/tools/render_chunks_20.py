# -*- coding: utf-8 -*-
r"""render_chunks_20.py — render video 20 theo TUNG KHUC, co resume.

🔴 VI SAO KHONG RENDER MOT MACH (bai hoc 2026-09-03):
   Lan dau chay `npx remotion render` mot mach: bo qua **24030/25348 frame
   (95%)** roi chet o buoc DON DEP —
       Error: kill EPERM ... at spawnedKill (execa/lib/kill.js)
   Remotion khong giet noi tien trinh ffmpeg con (Windows, errno -4048).
   Loi o khau ket thuc, KHONG phai o noi dung — nhung vi no chet truoc khi mux
   nen **khong co file nao ca**: 1h55 render bay sach.
   ⚠️ Va harness bao "exit code 0" — do la exit cua `.cmd`, khong phai cua
   render. Chi `RENDER_EXIT=1` trong log moi noi that (`render-background.md`
   §1 muc 3: EXITCODE mot minh khong chung minh gi).

📐 CACH LAM MOI:
   ① render 4 khuc `--frames=A-B`, **`--muted`** (video khong tieng)
   ② khuc nao da co file va MOI HON project.json thi BO QUA => resume that
   ③ noi 4 khuc bang `concat -c copy` (Remotion mo moi khuc bang keyframe nen
      noi khong can encode lai — khong mat doi nen nao)
   ④ tron tieng RIENG bang ffmpeg: voice_full.wav + bgm (-40dB, lap) roi
      loudnorm -14 LUFS, mux vao video
   ⇒ Khuc nao chet chi mat ~28 phut chu khong mat ca lo, va tieng thi minh
     kiem soat hoan toan (khoi phu thuoc Remotion mux).

CHAY:  python tools/render_chunks_20.py            (render + noi + tron tieng)
       python tools/render_chunks_20.py --status   (chi in trang thai)
"""
import io
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "20_izoku-nenkin-yonbunno-san"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
RV = os.path.join(os.path.dirname(PROJ), "remotion-vox")
PJ = os.path.join(RV, "projects", "nenkin-20", "project.json")
CH = os.path.join(VD, "chunks")
NCHUNK = 4
FPS = 30


def chunks(total):
    step = -(-total // NCHUNK)
    return [(i, min(i + step - 1, total - 1)) for i in range(0, total, step)]


def run(cmd, cwd=None):
    return subprocess.call(cmd, cwd=cwd)


def main():
    doc = json.load(io.open(PJ, encoding="utf-8"))
    total = doc["timeline"]["durationInFrames"]
    os.makedirs(CH, exist_ok=True)
    rng = chunks(total)
    pj_m = os.path.getmtime(PJ)
    status = "--status" in sys.argv

    todo = []
    for k, (a, b) in enumerate(rng):
        p = os.path.join(CH, f"c{k}.mp4")
        # 🔴 resume phai hoi "file con DUNG khong", khong phai "co ton tai khong"
        #    (render-background.md §2.5): project.json moi hon => khuc cu la rac
        ok = os.path.exists(p) and os.path.getmtime(p) > pj_m and os.path.getsize(p) > 10000
        print(f"  khuc {k}: frame {a}-{b} ({b - a + 1})  " + ("DA CO, bo qua" if ok else "CAN RENDER"))
        if not ok:
            todo.append((k, a, b, p))
    if status:
        return 0

    # 🔴 CONCURRENCY 4 -> 2 (2026-09-03): khuc 1 chet o 5384/6337 (85%) voi
    #    `kill EPERM`, va lan render mot mach truoc do chet o 24030/25348 (95%).
    #    Hai lan deu GIUA CHUNG, khong phai luc ket thuc => khong phai loi don
    #    dep ma la **qua tai**: may 6 nhan, RAM trong ~5GB, 4 luong chrome giai
    #    ma 88 clip 1080p cung luc. Khuc 0 qua duoc vi chay dau tien, bo nho con
    #    sach. Ha 2 luong cho nhe, doi lai lau hon.
    # 🔴 THU LAI TU DONG: loi nay khong on dinh (khuc 0 qua, khuc 1 khong), nen
    #    mot lan gay KHONG co nghia la khuc do khong render duoc.
    for k, a, b, p in todo:
        okc = False
        for attempt in (1, 2, 3):
            print(f"\n=== render khuc {k} ({a}-{b}) — lan {attempt} ===", flush=True)
            rc = run(["cmd", "/c", "npx", "remotion", "render", "VoxProject",
                      f"--props={PJ}", f"--frames={a}-{b}", "--muted",
                      "--concurrency=2", "--log=info", p], cwd=RV)
            if rc == 0 and os.path.exists(p) and os.path.getsize(p) > 10000:
                okc = True
                break
            print(f"  khuc {k} lan {attempt} GAY rc={rc}", flush=True)
            if os.path.exists(p):
                os.remove(p)          # file dang do la rac, xoa de lan sau khong tuong da xong
        if not okc:
            print(f"KHUC {k} GAY CA 3 LAN — dung lai, chay lai lenh nay de tiep tuc")
            return 2

    # ── noi 4 khuc, KHONG encode lai ───────────────────────────────────────
    lst = os.path.join(CH, "list.txt")
    io.open(lst, "w", encoding="utf-8").write(
        "".join(f"file '{os.path.join(CH, f'c{k}.mp4')}'\n" for k in range(len(rng))))
    mute = os.path.join(VD, "video_mute.mp4")
    rc = run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
              "-i", lst, "-c", "copy", mute])
    if rc != 0:
        print("noi khuc GAY")
        return 3

    # ── tron tieng: voice + bgm(-40dB, lap) -> loudnorm -14 LUFS -> mux ────
    voice = os.path.join(VD, "voice_full.wav")
    bgm = os.path.join(RV, "public", "projects", "nenkin-20", "assets", "bgm.mp3")
    out = os.path.join(VD, "video_final.mp4")
    if os.path.exists(bgm):
        fc = ("[1:a]aloop=loop=-1:size=2e9,volume=0.01[b];"
              "[0:a][b]amix=inputs=2:duration=first:dropout_transition=0,"
              "loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", bgm, "-i", mute,
               "-filter_complex", fc, "-map", "2:v", "-map", "[a]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", mute,
               "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-map", "1:v", "-map", "0:a",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    rc = run(cmd)
    if rc != 0:
        print("tron tieng GAY")
        return 4
    print("\nXONG:", out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
