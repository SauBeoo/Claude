# -*- coding: utf-8 -*-
"""build_remotion_yawa.py — lop Remotion KIEU YAWA cho kinishinai (chep khuon youtube-jp-yawa/tools/build_remotion_demo.py).

User 2026-10-01: ban hop chu dan len anh "trong xau lam, tao muon giong remotion cua yawa".
Lop (giong yawa): ① the chuong toan khung `yawa-chapter` ② chip tien do `yawa-chip` 「その一 ／ 七」
③ cau chot / the so / the doi cau -> `yawa-reveal` (chu 明朝 hien dan tren giay kem, nen = anh truoc lam mo)
④ bui sang + vignette mem + hat phim ⑤ tu khoa `yawa-keyword` 1-2 lan/chuong ⑥ phu de do Remotion ve
(TAT trong luc the toan khung hien).
Khac yawa: footage la clip still_kb + clip nguoi dan SACH (khong o chu bake) — dung lai bang
tools/host_insert_01.py::build_clip(text=None) vao clips_clean/.
Asset chep vao THU MUC PUBLIC GON (public/ goc 5,7 GB bi chep lai moi lan bundle).
Chay: python tools/build_remotion_yawa.py 01_kuchiguse-hitonome --t0 100 --t1 215 --name kinishinai-01yawa
"""
import argparse, json, re, shutil, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(r"E:\Claude\Projects\youtube-jp-kinishinai")
RV = Path(r"E:\Claude\Projects\remotion-vox")
BGM = Path(r"E:\Claude\Projects\youtube-jp-health\06_VIDEO\bgm\Wholesome.mp3")
FPS, XF = 30, 24      # hoa mo 0,8s (0,4s cu: doi huong chuyen dong giua 2 anh nhin khung lai — user 2026-10-02 'giat')
KB = Path("E:/Claude/Projects/_media_library/still_kb.py")
KANJI = str.maketrans("0123456789", "〇一二三四五六七八九")
# tu khoa: (match dong timeline, chu hien, so dong timeline giu) — 1-2 / chuong, cum NGAN (mau yawa)
KEYWORDS = [("うれしいはずなのに", "「すみません」は、見張り番の声", 2),
            ("見張り番は、いつも、危ないほうに", "見張り番は、心配性", 1)]
# the PIL kieu khac (stat / swap / ...) -> yawa-reveal: (loai, ham doi card.lines -> dong reveal, tu khoa bat tung dong)
REVEAL_FROM_CARD = {
    # the so: dong tren -> dong duoi (+が) -> cap so thanh CAU (「約3割から、約6割へ」) — cau 明朝 khong de mui ten
    "stat": lambda L: [L[0], L[2] + "が", re.sub(r"\s*→\s*", "から、", L[1]).strip() + "へ"] if len(L) >= 3 else L,
    "swap": lambda L: [f"「{L[0]}」を、", f"「{L[1]}」に。"] if len(L) == 2 else L,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem"); ap.add_argument("--t0", type=float, required=True); ap.add_argument("--t1", type=float, required=True)
    ap.add_argument("--name", required=True); ap.add_argument("--public", default="public_k01yawa")
    a = ap.parse_args()
    VD = ROOT / "06_VIDEO" / a.stem
    tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))["lines"]
    slides = json.loads((ROOT / "03_SCRIPTS" / f"{a.stem}_SLIDES.json").read_text(encoding="utf-8"))
    PUB = RV / a.public
    OUT = RV / "projects" / a.name
    AS = PUB / "projects" / a.name / "assets"
    OUT.mkdir(parents=True, exist_ok=True); AS.mkdir(parents=True, exist_ok=True)
    # font 明朝 + nen giay cua preset yawa-* phai co trong public gon
    for sub in ("shared/fonts",):
        src = RV / "public" / sub
        if src.exists():
            shutil.copytree(src, PUB / sub, dirs_exist_ok=True)

    f = lambda sec: int(round((sec - a.t0) * FPS))
    NT = f(a.t1)

    def cp(src, name):
        dst = AS / name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        return "assets/" + name

    def img_of(i):
        return next(p for e in (".jpg", ".jpeg", ".png") if (p := VD / "slides_img" / f"slide_{i:02d}{e}").exists())

    def clip_of(i):
        s = slides[i]
        if s.get("_host"):
            c = VD / "clips_clean" / f"clip_{i:02d}.mp4"
            assert c.exists(), f"thieu clip nguoi dan SACH {c.name} — chay buoc clips_clean truoc"
            return c
        return VD / "clips" / f"clip_{i:02d}.mp4"

    def at_kw(n, kw):
        ln = tl[n]; i = ln["text"].find(kw)
        return ln["start"] + (max(i, 0) / len(ln["text"])) * (ln["end"] - ln["start"])

    # moc slide = luat renderer (dong timeline dau tien chua match + offset), sap theo thoi gian
    st0 = [next(l for l in tl if s["match"] in l["text"])["start"] + float(s.get("offset", 0.0)) for s in slides]
    order = sorted(range(len(slides)), key=lambda i: st0[i])
    starts = {i: st0[i] for i in order}; starts[order[0]] = 0.0
    nxt = {i: (starts[order[k + 1]] if k + 1 < len(order) else a.t1) for k, i in enumerate(order)}
    # lay CA slide dang chay do o moc dau (bat dau truoc t0, ket sau t0) — ban dau bo sot -> 5s dau demo trong tron
    idx = [i for i in order if starts[i] < a.t1 - 0.01 and nxt[i] > a.t0 + 0.01]
    print("slides", len(idx), "trong cua so")

    foot, text, cap_off = [], [], []
    skip_foot = set()     # canh dau chuong da nam trong clip nen cua the chuong
    prev_img = None
    for k, i in enumerate(idx):
        s, st = slides[i], starts[i]
        fr, to = f(st), min(NT, f(nxt[i]))
        trim = max(0, -fr); fr = max(0, fr)          # slide bat dau truoc cua so: cat dau clip
        lead = XF if k else 0
        cid = f"s{i}"
        card = s.get("card", {})
        ty = card.get("type")
        if ty == "chapter":
            # NEN THAT (user 2026-10-02: "nen xanh thay bang nen that"): mot clip still_kb cua CANH DAU CHUONG chay tu
            # luc the hien toi het canh do -> the mo di thi anh chay tiep, khong co cu cat. The = scrim navy trong suot.
            k2 = order.index(i) + 1
            j = order[k2] if k2 < len(order) else None
            if j is not None and not slides[j].get("card") and not slides[j].get("reveal") and not slides[j].get("_host"):
                pj = VD / "slides_img" / f"slide_{j:02d}.png"
                dur = nxt[j] - st + 0.6
                mode = (slides[j].get("_kb") or "zin").split()[0]
                out = AS / f"chbg_{i:02d}.mp4"
                if not out.exists() or out.stat().st_mtime < pj.stat().st_mtime:
                    subprocess.run([sys.executable, str(KB), str(pj), str(out), "--dur", f"{dur:.2f}", "--mode", mode,
                                    "--amount", "0.06", "--fps", str(FPS)], check=True)
                foot.append({"id": cid + "bg", "kind": "video", "from": fr - lead,
                             "durationInFrames": min(NT, f(nxt[j])) - fr + lead,
                             "asset": "assets/" + out.name, "fit": "cover", "motion": "none", "fadeInFrames": lead})
                skip_foot.add(j)
            text.append({"id": cid, "kind": "text", "from": fr, "durationInFrames": to - fr + 6, "preset": "yawa-chapter",
                         "content": "\n".join(card["lines"]), "animation": "none", "color": "#FFFFFF",
                         "animationParams": {"scrim": 0.64, "fadeIn": lead or 12}})
            cap_off.append((fr, to))
        elif s.get("reveal") or ty in REVEAL_FROM_CARD:
            if s.get("reveal"):
                lines, times = s["reveal"]["lines"], s["reveal"]["times"]
            else:
                lines = REVEAL_FROM_CARD[ty](card["lines"])
                # moi dong hien luc giong doc toi chu dau dong (noi suy theo ky tu trong cac dong timeline cua slide)
                ns = [n for n, l in enumerate(tl) if st - 0.05 <= l["start"] < nxt[i] - 0.05]
                times = []
                for ln_txt in lines:
                    key = re.sub(r"[「」、。→\s約]", "", ln_txt).translate(KANJI)[:2]   # giong doc 三割, the ghi 3割
                    hit = next((at_kw(n, key) for n in ns if key and key in tl[n]["text"]), None)
                    times.append(round((hit - st) if hit is not None else (times[-1] + 1.5 if times else 0.0), 2))
                times = [max(0.0, t) for t in times]
                times[0] = 0.3          # dong dau hien NGAY khi vao the — giay kem trong 7s la khung chet
                for q in range(1, len(times)):
                    times[q] = max(times[q], times[q - 1] + 0.6)
            bg = prev_img or img_of(i)
            foot.append({"id": cid + "bg", "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                         "asset": cp(bg, f"bg_{i:02d}{bg.suffix}"), "fit": "cover", "motion": "none",
                         "fadeInFrames": lead, "filter": {"blur": 14, "brightness": 0.62, "saturate": 0.85}})
            text.append({"id": cid, "kind": "text", "from": fr, "durationInFrames": to - fr + 6, "preset": "yawa-reveal",
                         "content": "\n".join(lines), "animation": "none", "color": "#3A2E24",
                         "animationParams": {"times": times}})
            cap_off.append((fr, to))
        elif ty:      # the PIL kieu khac (seven / asch / people / ...) — giu anh the
            png = img_of(i)
            foot.append({"id": cid, "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                         "asset": cp(png, f"slide_{i:02d}{png.suffix}"), "fit": "cover", "motion": "none", "fadeInFrames": lead})
        elif i in skip_foot:
            p = VD / "slides_img" / f"slide_{i:02d}.png"
            prev_img = p if p.exists() else prev_img
        elif s.get("_host"):
            # NGUOI DAN "dung canh" anh ke chuyen (user 2026-10-02: podcast "ghep cho co" -> lam ca (a) + (b)):
            # (a) nen = anh ke chuyen vua xong, van troi cham (still_kb), mo nhe + toi di; nguoi dan trong KHUNG BO GOC
            #     vien kem lech phai, day khung y <= 789 (phu de bat dau ~796)
            # (b) chinh mau phong nguoi dan sang tong AM cua anh ke chuyen (sepia nhe, giam bao hoa/tuong phan)
            bgsrc = prev_img or img_of(order[order.index(i) + 1])
            bgout = AS / f"hostbg_{i:02d}.mp4"
            if not bgout.exists() or bgout.stat().st_mtime < bgsrc.stat().st_mtime:
                subprocess.run([sys.executable, str(KB), str(bgsrc), str(bgout), "--dur", f"{(to - fr + lead) / FPS + 0.5:.2f}",
                                "--mode", "zin", "--amount", "0.04", "--fps", str(FPS)], check=True)
            foot.append({"id": cid + "bg", "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                         "asset": "assets/" + bgout.name, "fit": "cover", "motion": "none", "fadeInFrames": lead,
                         "filter": {"blur": 5, "brightness": 0.78, "saturate": 0.9}})
            c = clip_of(i)
            # 🔴 KHOP MIENG: clip bat dau SOM `lead` frame de kip hoa mo -> noi dung cung chay som 0,8s = mieng di TRUOC
            # giong (user 2026-10-02 "podcast khong khop voi loi"). Chen `lead` frame DUNG YEN (frame dau) vao dau clip:
            # hoa mo dung frame dung, mieng bat dau dung giay cau noi bat dau.
            padded = AS / f"clip_{i:02d}_pad{lead}.mp4"
            if not padded.exists() or padded.stat().st_mtime < c.stat().st_mtime:
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(c), "-vf", f"tpad=start={lead}:start_mode=clone",
                                "-an", "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-r", str(FPS), str(padded)], check=True)
            hw = 1100; hh = round(hw * 9 / 16)
            foot.append({"id": cid, "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                         "asset": "assets/" + padded.name, "fit": "cover", "motion": "none", "fadeInFrames": lead,
                         "trimStartFrames": trim,
                         "layout": {"x": 1920 - hw - 90, "y": 789 - hh - 6, "w": hw, "h": hh},
                         "frame": {"radius": 26, "border": 6, "borderColor": "#F6EEDE",
                                   "shadow": "0 18px 48px rgba(0,0,0,0.45)"},
                         "filter": {"sepia": 0.18, "saturate": 0.9, "contrast": 0.96, "brightness": 1.03}})
        else:
            c = clip_of(i)
            foot.append({"id": cid, "kind": "video", "from": fr - lead, "durationInFrames": to - fr + lead,
                         "asset": cp(c, f"clip_{i:02d}.mp4"), "fit": "cover", "motion": "none", "fadeInFrames": lead,
                         "trimStartFrames": trim})
            if not s.get("_host"):
                p = VD / "slides_img" / f"slide_{i:02d}.png"
                prev_img = p if p.exists() else prev_img

    # chip tien do theo chuong, an khi the chuong hien
    cards = [(i, starts[i]) for i in idx if slides[i].get("card", {}).get("type") == "chapter"]
    prev_ch = next((slides[j]["card"]["lines"][0] for j in reversed(order[:order.index(idx[0]) + 1])
                    if slides[j].get("card", {}).get("type") == "chapter"), None)
    segs, t = [], a.t0
    for i, st in cards:
        if prev_ch:
            segs.append((prev_ch, t, st))
        prev_ch = slides[i]["card"]["lines"][0]; t = nxt[i]
    if prev_ch and t < a.t1:
        segs.append((prev_ch, t, a.t1))
    for n, (ch, s0, s1) in enumerate(segs):
        if f(s1) - f(s0) > 40:
            text.append({"id": f"chip{n}", "kind": "text", "from": f(s0), "durationInFrames": f(s1) - f(s0),
                         "preset": "yawa-chip", "content": f"{ch} ／ 七" if ch.startswith("その") else ch,
                         "animation": "none", "color": "#F6EEDE"})
    # tu khoa
    for n, (m, word, nl) in enumerate(KEYWORDS):
        j = next((q for q, l in enumerate(tl) if m in l["text"] and a.t0 <= l["start"] < a.t1), None)
        if j is None:
            print("ngoai cua so / thieu keyword", m); continue
        s0, s1 = tl[j]["start"], tl[j + nl - 1]["end"] + 1.2
        if any(c0 - 3 <= f(s0) < c1 for c0, c1 in cap_off):
            print("BO keyword (trung the dang hien)", word); continue
        e1 = min([f(s1)] + [c0 for c0, _ in cap_off if c0 > f(s0)])
        text.append({"id": f"kw{n}", "kind": "text", "from": f(s0) + 8, "durationInFrames": e1 - f(s0) - 8,
                     "preset": "yawa-keyword", "content": word, "animation": "none", "color": "#3A2E24",
                     "layout": {"x": 140, "y": 150}, "fontSize": 58})
    # phu de: tat trong luc the toan khung hien. Cau dai (kenh nay dai hon yawa) -> tach khoi <= CAP_MAX ky o 「、」,
    # chia thoi gian theo so ky tu (khuon split_caption cua nenkin build_remotion_26) — tranh ngat 「…でしょ/う」。」
    CAP_MAX = 26
    def split_cap(t):
        out, cur = [], ""
        for part in re.findall(r"[^、。」]*[、。」]?", t):
            if not part:
                continue
            if cur and len(cur) + len(part) > CAP_MAX:
                out.append(cur); cur = part
            else:
                cur += part
        if cur:
            out.append(cur)
        merged = []
        for c in out:       # manh qua ngan (「。」 「」」) dinh vao manh truoc
            if merged and len(c) <= 2:
                merged[-1] += c
            else:
                merged.append(c)
        return merged
    caps = []
    for l in tl:
        if l["end"] <= a.t0 or l["start"] >= a.t1:
            continue
        parts = split_cap(l["text"]); tot = sum(len(p) for p in parts); acc = 0
        for p in parts:
            ps = l["start"] + (l["end"] - l["start"]) * acc / tot; acc += len(p)
            pe = l["start"] + (l["end"] - l["start"]) * acc / tot
            s0, s1 = max(0, f(ps)), min(NT, f(pe))
            if s1 <= s0 or any(c0 - 3 <= s0 < c1 for c0, c1 in cap_off):
                continue
            caps.append({"text": p, "startMs": round(s0 * 1000 / FPS), "endMs": round(s1 * 1000 / FPS)})
    # tieng: giong + BGM -40 dB tron SAN thanh assets/audio.wav (amix normalize=0, alimiter 0,891 — render-background §2.7)
    # -> tool render chunk gan lai dung file nay (noi chunk -c copy lech 0,35s)
    aud = AS / "audio.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a.t0:.3f}", "-t", f"{a.t1 - a.t0:.3f}", "-i", str(VD / "voice.wav"),
                    "-stream_loop", "-1", "-i", str(BGM), "-filter_complex",
                    "[1:a]volume=-40dB[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.891[o]",
                    "-map", "[o]", "-ar", "48000", "-ac", "2", str(aud)], check=True)
    audio_clips = [{"id": "a0", "kind": "audio", "from": 0, "durationInFrames": NT, "asset": "assets/audio.wav", "volume": 1}]
    proj = {
        "version": 1,
        "meta": {"name": a.name, "channel": "kinishinai", "fps": FPS, "width": 1920, "height": 1080},
        "timeline": {"durationInFrames": NT},
        "tracks": [
            {"id": "trk-foot", "name": "footage", "type": "video", "clips": foot},
            {"id": "trk-fx", "name": "fx", "type": "fx", "clips": [
                {"id": "dust", "kind": "fx", "variant": "dust", "from": 0, "durationInFrames": NT, "density": 22,
                 "color": "#FFE7B0", "seed": 7, "fadeInFrames": 20, "fadeOutFrames": 20},
                {"id": "vig", "kind": "fx", "variant": "vignette-soft", "from": 0, "durationInFrames": NT,
                 "color": "#0E0C14", "opacity": 0.40, "fadeInFrames": 0, "fadeOutFrames": 0}]},   # nen sang hon yawa: 0,55 -> 0,40
            {"id": "trk-text", "name": "text", "type": "text", "clips": text},
            {"id": "trk-grain", "name": "grain", "type": "fx", "clips": [
                {"id": "grain", "kind": "fx", "variant": "grain", "from": 0, "durationInFrames": NT, "opacity": 0.10,
                 "seed": 3, "fadeInFrames": 0, "fadeOutFrames": 0}]},
            {"id": "trk-audio", "name": "audio", "type": "audio", "clips": audio_clips},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True, "fontSize": 50, "lines": caps},
        "theme": {"fontFamily": '"Yu Gothic", "Meiryo", sans-serif'},
        "brand": None,
    }
    (OUT / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK {OUT / 'project.json'} | {NT} frames ({NT / FPS:.2f}s) | foot {len(foot)} · text {len(text)} · caps {len(caps)}")
    for x in text:
        print(f"  {x['preset']:13s} {x['from'] / FPS + a.t0:7.1f}s +{x['durationInFrames'] / FPS:5.1f}s  "
              f"{x['content'].replace(chr(10), ' / ')[:60]}  {x.get('animationParams', {}).get('times', '')}")


if __name__ == "__main__":
    main()
