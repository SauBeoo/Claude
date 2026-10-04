# -*- coding: utf-8 -*-
r"""render_chunks_21b.py — render video 21 theo TUNG KHUC, co resume.

   Chep tu `render_chunks_20.py` (2026-09-04). Moi bai hoc trong docstring
   duoi day la cua video 20 va **van con hieu luc**: khong render mot mach,
   concurrency 2, thu lai 3 lan, tron tieng rieng bang ffmpeg.

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

CHAY:  python tools/render_chunks_21b.py            (render + noi + tron tieng)
       python tools/render_chunks_21b.py --status   (chi in trang thai)
"""
import io
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEM = "21_fuyo-shinkokusho-205man"
VD = os.path.join(PROJ, "06_VIDEO", STEM)
RV = os.path.join(os.path.dirname(PROJ), "remotion-vox")
PJ = os.path.join(RV, "projects", "nenkin-21b", "project.json")
CH = os.path.join(VD, "chunks21b")
# 🔴 4 -> 8 KHUC (2026-09-07). Lan render dau chet SACH: 0/4 khuc ra file, log day
# `memory allocation of 2073600 bytes failed` + `ERR_INSUFFICIENT_RESOURCES`, roi
# `kill EPERM` KHONG BAT DUOC lam sap luon Node (banner "Node.js v21.6.2" = fatal).
# May 23,9 GB nhung luc do chi con 7,8 GB tu do (PhpStorm + League giu ~2,7 GB).
# Nhieu khuc hon KHONG ha dinh bo nho tung frame, nhung Chrome duoc khoi dong lai
# thuong xuyen hon => bot ro, va khuc nao chet thi mat ~14 phut chu khong ~28.
TARGET_OFF_RE = r'"target_offset"\s*:\s*"([-0-9.]+)"'
I_RE = r"^\s+I:\s+([-0-9.]+) LUFS"
PK_RE = r"^\s+Peak:\s+([-0-9.]+) dBFS"
NCHUNK = 8
FPS = 30
CONC = 1      # ghi de bang `--conc N`


def chunks(total):
    step = -(-total // NCHUNK)
    return [(i, min(i + step - 1, total - 1)) for i in range(0, total, step)]


def run(cmd, cwd=None):
    return subprocess.call(cmd, cwd=cwd)


def main():
    global CONC
    for i, a in enumerate(sys.argv):
        if a == "--conc" and i + 1 < len(sys.argv):
            CONC = int(sys.argv[i + 1])
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
            # 🔴 `--conc N` (them 2026-09-05): may 24 GB RAM van bi **he thong
            #    KILL** giua khuc 2 o lan render thu hai — Remotion + chrome an
            #    nhieu hon du toan. Ha ve 1 thi cham hon nhung khong chet giua
            #    chung, va resume da giu lai 2 khuc dau nen khong mat gi.
            rc = run(["cmd", "/c", "npx", "remotion", "render", "VoxProject",
                      f"--props={PJ}", f"--frames={a}-{b}", "--muted",
                      f"--concurrency={CONC}", "--log=info", p], cwd=RV)
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
    bgm = os.path.join(RV, "public", "projects", "nenkin-21b", "assets", "bgm.mp3")
    out = os.path.join(VD, "video_final_21b.mp4")
    if os.path.exists(bgm):
        # 🔴 PHAI CHOT `-ar 48000 -ac 2` (bat 2026-09-05): voice la 24kHz MONO,
        #    bgm la 44,1kHz STEREO => `amix` tu chon **96kHz MONO**, tuc vua dư
        #    (96kHz khong loi gi cho giong doc) vua MAT stereo cua bgm. Video 20
        #    ra 48kHz stereo nen lech chuan giua hai video cung kenh.
        #    YouTube khuyen nghi AAC-LC **48kHz stereo**; de 96kHz thi no
        #    transcode lai lan nua.
        # HAI PASS, KHONG MOT PASS — va ly do KHONG phai cai ghi o ban truoc
        #    (do lai 2026-09-07 tren ban 21b lan 2; ban cu chan SAI nguyen nhan):
        #    `loudnorm` cua ffmpeg **KHONG phai filter nhan qua theo dong** — no do ca
        #    file roi moi quyet, nen ket qua PHU THUOC DO DAI TOAN BAI. Bang chung:
        #    cung chuoi filter, cung doan 0-200s, render 240s ra **-14,2 LUFS** con
        #    render 808s ra **-15,7**, va md5 cua mau KHAC NHAU (08319013 vs e31b5175).
        #    => **MOI phep thu loudness tren doan TRICH deu vo gia tri.** Do dung la
        #    cach tao chan sai o vong truoc: test `-t 240` thay -14,23 roi tuong da chua.
        #    Tren ca bai loudnorm tu khai `target_offset: 1.82` va **khong tu bu**,
        #    nen phai cong tay o pass 2.
        #    ALIMITER DA BI BO, dung them lai:
        #      · dat TRUOC loudnorm -> do duoc la KHONG doi gi (ca hai chuoi ra
        #        I -15,8 / Peak -4,4 y het nhau) = bua, khong phai thuoc;
        #      · dat SAU loudnorm de "bao hiem TP" -> co HAI: keo I xuong -14,7 va
        #        giu peak -4,4, tuc dang NEN that. Peak sau khi cong 1,82dB chi
        #        -2,6 dBFS, con 1,1 dB dat toi tran -1,5 => khong can bao hiem.
        fc_base = ("[1:a]aloop=loop=-1:size=2e9,volume=0.01[b];"
                   "[0:a][b]amix=inputs=2:duration=first:dropout_transition=0,"
                   "loudnorm=I=-14:TP=-1.5:LRA=11")
        fc_tail = ",aresample=48000,aformat=channel_layouts=stereo[a]"
        pr = subprocess.run(["ffmpeg", "-v", "info", "-i", voice, "-i", bgm,
                             "-filter_complex", fc_base + ":print_format=json[a]",
                             "-map", "[a]", "-f", "null", "-"],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        m = re.search(TARGET_OFF_RE, pr.stdout + pr.stderr)
        off = float(m.group(1)) if m else 0.0
        print(f"  loudnorm target_offset = {off:+.2f} LU -> bu bang volume", flush=True)
        fc = fc_base + (f",volume={off}dB" if abs(off) >= 0.1 else "") + fc_tail
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", bgm, "-i", mute,
               "-filter_complex", fc, "-map", "2:v", "-map", "[a]",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", voice, "-i", mute,
               "-af", "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,aformat=channel_layouts=stereo", "-map", "1:v", "-map", "0:a",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out]
    rc = run(cmd)
    if rc != 0:
        print("tron tieng GAY")
        return 4
    print("\nXONG:", out)
    # GATE LOUDNESS: do lai FILE THAT, khong tin loi loudnorm tu khai
    #   (bai hoc cung luot: pass-1 bao "output_i -14,23" nhung file that ra -15,8)
    pr = subprocess.run(["ffmpeg", "-hide_banner", "-i", out,
                         "-af", "ebur128=peak=true:framelog=quiet", "-f", "null", "-"],
                        capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    txt = pr.stdout + pr.stderr
    mi, mp = re.findall(I_RE, txt, re.M), re.findall(PK_RE, txt, re.M)
    if mi and mp:
        I, PK = float(mi[-1]), float(mp[-1])
        print(f"  LOUDNESS do tren file: I {I:+.1f} LUFS - Peak {PK:+.1f} dBFS")
        if abs(I + 14.0) > 0.5:
            print(f"  GATE LOUDNESS DO: lech {I + 14.0:+.1f} LU so chuan -14")
        if PK > -1.5:
            print(f"  GATE LOUDNESS DO: Peak {PK:+.1f} vuot tran -1.5 dBFS")
    else:
        print("  canh bao: khong doc duoc ebur128 — kiem tay")
    return 0


if __name__ == "__main__":
    sys.exit(main())
