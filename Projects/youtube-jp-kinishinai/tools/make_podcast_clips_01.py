# -*- coding: utf-8 -*-
"""make_podcast_clips_01.py — clip "nguoi ke noi podcast" (Flow/Veo cua user) -> clips/clip_NN.mp4 cho SLIDES.

Moi cho chen: (chi so SLIDES, clip nguon, zoom, tam mat x/y theo ti le khung goc, match tuy chon cho entry MOI).
  - cat ✦ (phai 0,87W + trim 16:9 chia doi) truoc moi viec — media-library §2.10 ⑤b
    ⚠️ ✦ cua clip Veo lech TRAI hon anh (mep trai ~0,885W, co clip 2 dau) — 0,905W cua anh de sot dau nhon
  - zoom quanh mat (1.0 = rong) -> cung mot clip dung lai o cho khac ra KHUNG KHAC
  - keo dai cho vua slot bang setpts (<=1,5x) + minterpolate mci len 30fps (ho so kenh 30fps,
    clip Veo 24fps: ep thang = judder — feedback_fps_clip_phai_khop_renderer)
  - cat tieng (giong VOICEVOX la tieng duy nhat)
SLIDES: entry cu duoc them "video": true; entry moi (match) duoc APPEND cuoi danh sach de khong xo lech
chi so slide_NN/clip_NN cu (build_slides tu sap theo thoi gian).
Chay: python tools/make_podcast_clips_01.py 01_kuchiguse-hitonome [--only 59,84] [--dry]
"""
import sys, io, json, argparse, subprocess, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
RAW = "_user_raw/zip_1001_1157"
CLIP = {
    "A": "Woman_speaking_into_microphone_20261001120535_3.mp4",   # 2 tay dat ban, noi + cuoi
    "B": "Woman_speaking_into_microphone_20261001120535_2.mp4",   # tay dat len nguc
    "C": "Woman_smiling_and_shaking_head_20261001120535.mp4",     # cuoi, lac dau (640x360)
    "E": "Woman_smiling_in_recording_room_20261001120535.mp4",    # tay dan, nham mat cuoi
}
FACE = {"A": (0.37, 0.24), "B": (0.36, 0.22), "C": (0.42, 0.20), "E": (0.36, 0.26)}
MAX_SLOW = 1.55

# (slot SLIDES, clip, zoom, match cho entry MOI hoac None = thay anh cua slot do, ghi chu)
PLACE = [
    (10,  "A", 1.00, None, "ラジオのように、気楽に聞いてくださいね"),
    (13,  "B", 1.00, None, "今年、六十八になります"),
    (59,  "C", 1.00, None, "「大丈夫よ」と、笑ってしまう — o thieu anh"),
    (79,  "E", 1.00, None, "駅弁を、二つ — anh cu la 2 nguoi, sai 「ひとり旅」"),
    (112, "B", 1.35, ("こうして、私は、一年かけて", 0.4), "doan 2 cua slot 79 (offset 0,4s -> slot 79 >= 6s)"),
    (84,  "A", 1.30, None, "いちばん大きな、見積もりちがい — o thieu anh"),
    (106, "A", 1.45, None, "いかがでしたでしょうか"),
    (111, "E", 1.45, None, "楽に過ごせますように"),
]


def probe(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout
    w, h = out.strip().split(",")[:2]
    return int(w), int(h)


def norm(s):
    return re.sub(r"[「」『』、。？！…・\s]", "", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("--only"); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    vd = PROJ / "06_VIDEO" / a.stem
    sp = PROJ / "03_SCRIPTS" / f"{a.stem}_SLIDES.json"
    sl = json.loads(sp.read_text(encoding="utf-8"))
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines, total = tl["lines"], tl["total"]
    only = {int(x) for x in a.only.split(",")} if a.only else None

    # 1) SLIDES: entry moi APPEND + co "video"
    for idx, key, z, match, note in PLACE:
        if match:
            match, off = match
            hit = [ln for ln in lines if match in ln["text"]]
            assert len(hit) == 1, f"match「{match}」khop {len(hit)} dong"
            if idx == len(sl):
                sl.append({"match": match, "offset": off, "_shot": f"pod{idx}"})
            assert sl[idx]["match"] == match, f"slot {idx} khong phai entry moi「{match}」"
        sl[idx]["video"] = True
        sl[idx].pop("photo", None)   # slot da la clip: preflight dem "photo" la can anh -> chan oan
        sl[idx]["static"] = True
        sl[idx]["_pod"] = f"{key} z{z}"
    # moc giay: cung cach build_slides (match dau tien), entry sau sap theo thoi gian
    st = []
    for i, e in enumerate(sl):
        hit = next(ln for ln in lines if e["match"] in ln["text"])
        st.append((hit["start"] + float(e.get("offset", 0.0)), i))
    st.sort(); st[0] = (0.0, st[0][1])
    dur = {i: (st[k + 1][0] if k + 1 < len(st) else total) - t for k, (t, i) in enumerate(st)}
    n_min = len(sl) / (total / 60)
    print(f"SLIDES {len(sl)} entry · {n_min:.2f} hinh/phut (tran 6,0)" + ("  🔴 VUOT TRAN" if n_min > 6.0 else ""))
    bad = [(i, round(d, 1)) for i, d in dur.items() if d < 6.0]
    if bad:
        print("⚠️ entry <6s:", bad)

    # 2) clip
    cd = vd / "clips"; cd.mkdir(exist_ok=True)
    for idx, key, z, match, note in PLACE:
        if only and idx not in only:
            continue
        src = vd / RAW / CLIP[key]
        need = dur[idx] + 0.25
        slow = max(1.0, need / 8.0)
        assert slow <= MAX_SLOW, f"slot {idx}: can keo {slow:.2f}x > {MAX_SLOW}"
        w, h = probe(src)
        # cat ✦: giu 0,87W ben trai, trim 16:9 chia doi tren/duoi
        cw = int(w * 0.87) // 2 * 2; ch = round(cw * 9 / 16) // 2 * 2; cy = (h - ch) // 2
        # zoom quanh mat (toa do theo khung goc -> khung da cat)
        fx, fy = FACE[key]
        zw = int(cw / z) // 2 * 2; zh = int(ch / z) // 2 * 2
        zx = min(max(int(fx * w - zw / 2), 0), cw - zw)
        zy = min(max(int(fy * h - ch * 0.0 - zh * 0.30) - cy, 0), ch - zh)
        vf = (f"crop={cw}:{ch}:0:{cy},crop={zw}:{zh}:{zx}:{zy},scale=1920:1080:flags=lanczos,"
              f"setpts={slow:.4f}*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
              f"trim=duration={need:.3f},setpts=PTS-STARTPTS,setsar=1,format=yuv420p")
        out = cd / f"clip_{idx:02d}.mp4"
        print(f"clip_{idx:02d} <- {key} ({w}x{h}) zoom {z} · slot {dur[idx]:.1f}s · keo {slow:.2f}x · {note}")
        if a.dry:
            continue
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", vf, "-an", "-c:v", "libx264",
                            "-preset", "medium", "-crf", "17", str(out)], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr[-800:]
    if not a.dry:
        sp.write_text(json.dumps(sl, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"OK -> {sp.name} + clips/")


if __name__ == "__main__":
    main()
