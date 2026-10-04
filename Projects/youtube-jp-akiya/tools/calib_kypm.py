# -*- coding: utf-8 -*-
"""Đo hệ số ký/phút THẬT của giọng kênh akiya với ĐÚNG cấu hình render
(gap 0.6 / section-gap 1.1 như video_render.py).

Dùng:
  python tools/calib_kypm.py                              # kênh chốt: id 21 = 剣崎雌雄/ノーマル @0.95
  python tools/calib_kypm.py --speaker 11 --tag kurono    # so sánh giọng khác
Mẫu văn: mặc định lấy ~4.000 ký thân bài script nenkin (cùng dạng giải thích tiền/chế độ);
khi akiya có script riêng thì trỏ --src vào `03_SCRIPTS/<x>_TTS.md` và chạy lại.
Đổi giọng/speed/gap → CHẠY LẠI và ghi số mới vào CLAUDE.md.
"""
import argparse, io, json, re, sys, urllib.parse, urllib.request, wave
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:50021"
DEF_SRC = Path(r"E:\Claude\Projects\youtube-jp-nenkin\03_SCRIPTS\05_60sai-teinen-taishoku-kiken_TTS.md")
OUTDIR = Path(r"E:\Claude\Projects\youtube-jp-akiya\00_VOICE_TEST")

ap = argparse.ArgumentParser()
ap.add_argument("--speaker", type=int, default=21, help="VOICEVOX speaker id (kênh chốt: 21 = 剣崎雌雄/ノーマル)")
ap.add_argument("--speed", type=float, default=0.95)
ap.add_argument("--intonation", type=float, default=1.1)
ap.add_argument("--gap", type=float, default=0.6)
ap.add_argument("--section-gap", type=float, default=1.1)
ap.add_argument("--chars", type=int, default=4000)
ap.add_argument("--src", type=Path, default=DEF_SRC)
ap.add_argument("--tag", default="")
a = ap.parse_args()

name = ""
try:
    for s in json.loads(urllib.request.urlopen(BASE + "/speakers", timeout=20).read()):
        for st in s["styles"]:
            if st["id"] == a.speaker:
                name = f"{s['name']}/{st['name']}"
except Exception as e:
    print(f"⚠️ không đọc được /speakers ({e!r}) — VOICEVOX (:50021) chạy chưa?")
print(f"Giọng: id {a.speaker} {name} @speed {a.speed} intonation {a.intonation} · gap {a.gap}/{a.section_gap}")

lines, nchar = [], 0
for ln in a.src.read_text(encoding="utf-8").splitlines():
    s = re.sub(r"\[[^\]]*\]", "", ln).strip()
    if s.startswith("#") or s.startswith("==="):
        continue
    if s == "---":
        lines.append("---"); continue
    if not s:
        lines.append(""); continue
    lines.append(s); nchar += len(s)
    if nchar >= a.chars:
        break
ndong = sum(1 for l in lines if l and l != "---")
print(f"Mẫu: {nchar} ký tự / {ndong} dòng ({a.src.name})")


def synth(text):
    q = urllib.parse.urlencode({"text": text, "speaker": a.speaker})
    aq = json.loads(urllib.request.urlopen(urllib.request.Request(BASE + "/audio_query?" + q, method="POST"), timeout=120).read())
    aq["speedScale"] = a.speed
    aq["intonationScale"] = a.intonation
    aq["prePhonemeLength"] = 0.1
    aq["postPhonemeLength"] = 0.1
    req = urllib.request.Request(BASE + f"/synthesis?speaker={a.speaker}", data=json.dumps(aq).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    return urllib.request.urlopen(req, timeout=300).read()


parts, params, done = [], None, 0
for ln in lines:
    if ln in ("", "---"):
        parts.append(("gap", a.section_gap if ln == "---" else a.gap)); continue
    with wave.open(io.BytesIO(synth(ln))) as r:
        if params is None:
            params = r.getparams()
        parts.append(("pcm", r.readframes(r.getnframes())))
    done += 1
    if done % 20 == 0:
        print(f"  ...{done}/{ndong} dòng")

tag = a.tag or (name.split("/")[0].replace(".", "") if name else str(a.speaker))
out = OUTDIR / f"calib_{tag}_{nchar}.wav"
fr, sw, ch = params.framerate, params.sampwidth, params.nchannels
with wave.open(str(out), "wb") as w:
    w.setparams(params)
    for kind, v in parts:
        w.writeframes(v if kind == "pcm" else b"\x00" * int(fr * sw * ch * v))
with wave.open(str(out)) as r:
    dur = r.getnframes() / r.getframerate()
kypm = nchar / (dur / 60)
print(f"\nWAV: {out.name}  {dur:.1f}s = {dur/60:.2f} phút")
print(f"➡️ HỆ SỐ THẬT: {kypm:.0f} ký/phút")
for m in (18, 20, 25):
    print(f"   {m} phút ≈ {int(kypm*m):,} ký")
