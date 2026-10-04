# -*- coding: utf-8 -*-
r"""build_remotion_28 — video 28 (断熱・天井の放射熱).

⭐ KHAC MOI VIDEO TRUOC CUA KENH: lop hero khong con la photocard tinh ma la
**82 CLIP VIDEO THAT, FULLSCREEN**. Nen kem + khung 1132px bi bo o scene co clip;
bang so lieu van giu, ve DE LEN video (co scrim mo).

Vi sao fullscreen: clip gen 1920x1080; nhet vao khung 1132px la vut 40% do phan giai
va lam video trong nhu slideshow — dung cai user muon tranh.

    python tools\build_remotion_28.py            # -> remotion-vox/projects/co-dai-28/project.json
    python tools\build_remotion_28.py --stats    # chi in thong ke scene, khong ghi
"""
import argparse
import collections
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                              errors="replace", line_buffering=True, write_through=True)

PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")
RV = Path(r"E:\Claude\Projects\remotion-vox")
STEM = "28_dannetsu-tenjo-alumi"
NAME = "co-dai-28"
FPS = 30
NL = chr(10)
INK, RED, AMBER = "#1C2A4A", "#A82026", "#F2B84B"
TAG_BG = "#F5D58A"

CAP_SIZE = 48
CAP_MAX = 66
CAP_CUT = "。、」）"

# clip 8s @24fps -> sau ingest la 30fps, van 8,00s
CLIP_S = 8.0
# 0.5 -> 0.28 -> 0.15. Ly do ha tiep: scene dai nhat 43,9s; o 0.28 clip 8s chi phu
# 28,6s => con 15,3s DUNG HINH. San 0.15 phu toi 53s nen khong scene nao dung hinh.
# Danh doi: 7/82 scene chay cham 3-6x. Canh deu la tripod/troi cham nen mat kho
# nhan ra, con man dung hinh 15 giay thi ai cung thay.
SPEED_MIN = 0.15

# ── BANG SO LIEU (de len video) ──────────────────────────────────────────────
# khoa = tim thay o dong nao (substring) -> noi dung bang
# 🔴 DANG VIET DA DOI (user 2026-09-04: *"tao không muốn cái nền trắng tinh như thế"*).
#    Truoc: `nhan|so` -> nhan la CHU TRAN (mau den dong cung trong preset) nen phai
#    co nen sang phia sau moi doc duoc => sinh ra mang kem lon, dung cai user bac.
#    Nay: `|nhan so` -> label RONG, tat ca nam trong O CO NEN cua preset.
#    Ket qua: chi con vai O CHU noi tren video, KHONG con mang nen nao.
STAT = {
    "根拠になっている数字": ("|窓・ドア 73%" + NL + "|屋根 11%" + NL + "|外壁 7%" + NL
                             + "|換気 6%" + NL + "*|床 3%", 44),
    "岩手県のある家で": ("|外気 33〜34度 → 小屋裏 50度" + NL + "*|外気 37度 → 小屋裏 60度", 46),
    "空気が27度": ("|空気 27度" + NL + "|天井の表面 35度" + NL + "*|体感 31度", 46),
    "みがいたアルミの面は": ("|みがいたアルミ 0.04〜0.06" + NL + "*|黒い紙 0.90" + NL
                             + "|差は 約20倍", 44),
    "かやの外側の表面と": ("|かやの表と裏 約40度の差" + NL + "|屋根の室内側 外気より10度低い"
                           + NL + "*|室内の空気 外気より5度低い", 40),
    "その日、壁の外側の表面は": ("|西壁の外面 最高52.9度" + NL + "|3時間で外面 +17.8度" + NL
                                 + "*|同じ時間 室内面 +0.9度", 40),
    "その予算の内訳に": ("|高断熱窓 1125億円" + NL + "*|壁・天井など躯体 300億円", 46),
}

# ── TAG chuong (dong bat dau -> nhan) ────────────────────────────────────────
TAGS = [
    ("去年の夏、二階の寝室に", "天井に触れた夜"),
    ("暑さ対策と聞けば", "「窓が7割」の但し書き"),
    ("翌日の夕方、私は押し入れ", "天井裏 60度"),
    ("窓を閉めきって", "風のない部屋でも届く熱"),
    ("夏になると、分厚い遮光", "アルミと紙で20倍"),
    ("ここで、私の失敗を白状", "貼ってはいけない場所"),
    ("かやぶき屋根、というものが", "かやぶきと土壁の記録"),
    ("遅れて届いた熱は", "跳ね返した熱の行き先"),
    ("さて、ここで一つ、不思議", "なぜ誰も売りに来ないのか"),
    ("最後にとっておいたのは", "押し入れの45センチ"),
    ("正直に申し上げます", "万能ではありません"),
]

# clip 26 cua lo 2: cau trong TENFILE2 bi chen chu o script v2 -> map tay
MANUAL = {"v_K3_thatch-village": "花岡利昌"}


def split_caption(line):
    """1 dong thoai -> nhieu khoi phu de <= CAP_MAX ky, chia theo dau cau."""
    t, s, e = line["text"], line["start"], line["end"]
    if len(t) <= CAP_MAX:
        return [{"text": t, "start": s, "end": e}]
    parts, cur = [], ""
    for ch in t:
        cur += ch
        if ch in CAP_CUT and len(cur) >= CAP_MAX * 0.55:
            parts.append(cur)
            cur = ""
    if cur:
        if parts and len(parts[-1]) + len(cur) <= CAP_MAX:
            parts[-1] += cur
        else:
            parts.append(cur)
    out, tot, acc = [], sum(len(p) for p in parts), s
    for p in parts:
        d = (e - s) * len(p) / tot
        out.append({"text": p, "start": acc, "end": acc + d})
        acc += d
    return out


def read_tenfile(p):
    """-> [(ten_clip, cau_thoai)] theo thu tu dong.

    🔴 HAI FILE HAI FORMAT — dung mot regex la doc thieu mot nua (da dinh):
        TENFILE  (lo 1): `01 -> v_A1_xxx.mp4   | cau thoai`
        TENFILE2 (lo 2): `01 👤 v_G1_xxx.mp4   | L002 cau thoai`
    Nen bat theo `<ten>.mp4 ... | ...`, khong bat theo dau `->`.
    """
    out = []
    for ln in io.open(p, encoding="utf-8"):
        if "|" not in ln or ln.lstrip().startswith("#"):
            continue
        m = re.search(r"(\S+)\.mp4\s*\|\s*(.+)", ln)
        if m:
            out.append((m.group(1), re.sub(r"^L\d+\s*", "", m.group(2)).strip()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()

    vd = PROJ / "06_VIDEO" / STEM
    tl = json.loads((vd / "timeline.json").read_text(encoding="utf-8"))
    lines = tl["lines"]
    DUR = round(tl["total"] * FPS)
    txts = [l["text"] for l in lines]

    def find(q, clipname=""):
        if clipname in MANUAL:
            q = MANUAL[clipname]
        q = q.strip()
        for i, t in enumerate(txts):
            if q in t:
                return i
        k = re.sub(r"[。、！？]", "", q)[:12]
        for i, t in enumerate(txts):
            if k and k in re.sub(r"[。、！？]", "", t):
                return i
        return None

    # ── 1. gan 82 clip vao dong ────────────────────────────────────────────
    ten = read_tenfile(vd / "video_prompts_TENFILE.txt") + \
        read_tenfile(vd / "video_prompts_TENFILE2.txt")
    assert len(ten) == 82, f"TENFILE doc duoc {len(ten)} clip, phai 82"

    pairs = []
    for name, q in ten:
        i = find(q, name)
        if i is None:
            print("🔴 khong map duoc:", name, "|", q[:40])
            sys.exit(1)
        pairs.append((i, name))
    pairs.sort(key=lambda x: x[0])

    # bo trung dong (2 clip cung 1 dong) — day dan clip sau xuong dong ke tiep
    seen, fixed = set(), []
    for i, name in pairs:
        while i in seen and i + 1 < len(lines):
            i += 1
        seen.add(i)
        fixed.append((i, name))
    fixed.sort(key=lambda x: x[0])

    cdir = vd / "clips"
    miss = [n for _, n in fixed if not (cdir / f"{n}.mp4").exists()]
    if miss:
        print("🔴 THIEU %d CLIP trong %s:" % (len(miss), cdir))
        for m in miss[:8]:
            print("   ", m)
        sys.exit(1)

    # ── 2. dung scene = khoang giua 2 clip lien tiep ───────────────────────
    #
    # 🔴 HAI CACH DA THU, GHI LAI DE KHONG QUAY LAI CACH SAI:
    #  ⓐ ep khoang cach clip vao [6s,16s] cho phu kin timeline  -> clip LECH cau thoai
    #     trung vi 8,6s, lon nhat **56,9s** (clip mai tranh chay truoc khi loi dan nhac
    #     toi no gan mot phut). Hinh noi mot dang, loi noi mot neo => BO.
    #  ⓑ (dang dung) clip nam DUNG moc cau thoai cua no, dai toi da 16s (speed 0.5).
    #     Khe con lai giua cac clip = NEN KEM + bang so — dung khuon kenh, va do la
    #     cho dat bang so lieu von can nen phang de doc.
    #  Danh doi: video khong phai 100% footage. Nhung "hinh khop loi" > "phu kin".
    #  ⓒ (2026-09-04, user: *"sao có nhiều chỗ nền trắng tinh thế"*) — cach ⓑ de lai
    #     24 khe nen kem = 19% thoi luong, khe dai nhat 27,9s. Tao da TINH RA con so
    #     do roi tu cho la "chap nhan duoc" — user bac ngay khi xem.
    #     => BO HAN KHE: moi clip phu TRON toi clip ke, speed = 8s / do dai scene,
    #     san SPEED_MIN. Canh deu la tripod/troi cham nen cham 2-3x gan nhu khong
    #     thay khac; con hon nhieu so voi 28 giay man trang.
    F = lambda i: round(lines[i]["start"] * FPS)          # noqa: E731
    scenes = []
    for k, (i, name) in enumerate(fixed):
        f = F(i)
        nxt = F(fixed[k + 1][0]) if k + 1 < len(fixed) else DUR
        d = max(1, nxt - f)                                # PHU TRON, khong con khe
        scenes.append(dict(i=i, name=name, f=f, to=f + d, d=d, gap=0, drift=0.0))

    ds = sorted(s["d"] / FPS for s in scenes)
    cov = sum(s["d"] for s in scenes)
    print("clip: %d | ngan nhat %.1fs | trung vi %.1fs | dai nhat %.1fs"
          % (len(scenes), ds[0], ds[len(ds) // 2], ds[-1]))
    sp = [max(SPEED_MIN, min(1.0, CLIP_S / (s["d"] / FPS))) for s in scenes]
    froz = sum(1 for s, v in zip(scenes, sp) if s["d"] / FPS > CLIP_S / v + 0.05)
    print("speed: trung vi %.2f | cham nhat %.2f | scene con DUNG HINH: %d"
          % (sorted(sp)[len(sp) // 2], min(sp), froz))
    print("phu bang FOOTAGE: %.0fs / %.0fs = %.0f%%   (con lai = nen kem + bang so)"
          % (cov / FPS, DUR / FPS, cov * 100 / DUR))
    gaps = [s["gap"] / FPS for s in scenes if s["gap"] > 0]
    if gaps:
        gs = sorted(gaps)
        print("khe nen kem: %d chỗ | trung vi %.1fs | dai nhat %.1fs"
              % (len(gs), gs[len(gs) // 2], gs[-1]))
    if a.stats:
        for s in sorted(scenes, key=lambda x: -x["gap"])[:8]:
            if s["gap"] > 0:
                print("   khe %.1fs sau %s" % (s["gap"] / FPS, s["name"]))
        return

    # ── 3. tracks ───────────────────────────────────────────────────────────
    # 🔴🔴 NGUYEN NHAN THAT CUA "NEN TRANG" (tim ra 2026-09-04 khi soi frame 7:10 cua
    #     ban da render): KHONG phai khe. Clip CO phu, speed 1.0, moi chay 0,2s —
    #     nhung `fadeInFrames:12` lam clip MO DAN VAO TU TRONG SUOT, ma DUOI no khong
    #     co gi, nen 0,4s dau cua MOI lan doi clip deu lo nen kem. 82 clip = 82 lan
    #     chop kem. Do la thu user thay, va la ly do "bo khe" van chua het nen trang.
    # ⇒ FIX: clip sau BAT DAU SOM `FADE` frame, chong len clip truoc => fade dien ra
    #     TREN clip truoc (dissolve that), khong con lo nen. Gate chong nhau da noi
    #     dung `FADE` frame cho dung viec nay.
    FADE = 12
    vid, tag, stat = [], [], []
    for k, s in enumerate(scenes):
        f0 = s["f"] if k == 0 else s["f"] - FADE
        d0 = s["d"] if k == 0 else s["d"] + FADE
        dsec = d0 / FPS
        sp = max(SPEED_MIN, min(1.0, CLIP_S / dsec))
        vid.append({
            "id": f"v-{k}", "kind": "video", "from": f0,
            "durationInFrames": d0,
            "asset": f"assets/{s['name']}.mp4",
            "trimStartFrames": 0, "fit": "cover", "layout": {},
            "motion": "none", "speed": round(sp, 3), "mirror": False, "volume": 0,
            "fadeInFrames": 0 if k == 0 else FADE,
            "wipeInFrames": 0, "wipeDir": "left", "filter": {},
        })

    def txt(i, content, f, dur, preset, color=INK, layout=None, size=None):
        c = {"id": i, "kind": "text", "from": f, "durationInFrames": dur,
             "preset": preset, "content": content, "color": color,
             "entrance": {"variant": "rise", "delayFrames": 0, "params": {}},
             "exit": None}
        if layout:
            c["layout"] = layout
        if size:
            c["fontSize"] = size
        return c

    # tag chuong: song tu dong khop den tag ke tiep
    tg = []
    for q, label in TAGS:
        i = find(q)
        if i is not None:
            tg.append((i, label))
    tg.sort()
    for k, (i, label) in enumerate(tg):
        f = F(i)
        to = F(tg[k + 1][0]) if k + 1 < len(tg) else DUR
        tag.append(txt(f"tag-{k}", label, f + 4, min(to - f - 4, 210), "tag",
                       color=TAG_BG, layout={"x": 74, "y": 58}, size=54))

    # ── bang so lieu ────────────────────────────────────────────────────────
    # 🔴 BAN DAU: dat bang tai F(dong khop) + 8s co dinh. Soi still thay hai loi:
    #    ① bang roi DE LEN clip (nen anh dong, kho doc) hoac roi NGAY SAU khe
    #    ② khe nen kem 27,9s van TRONG TRON — 7 khe >8s = 144s = 13% video.
    #    SUA: moi bang tim KHE gan nhat va phu TRON khe do. Khe la nen phang,
    #    dung cho bang so — va bang lap khe. Mot cong doi viec.
    holes = []
    for k in range(len(scenes) - 1):
        a_, b_ = scenes[k]["to"], scenes[k + 1]["f"]
        if b_ - a_ >= 4 * FPS:
            holes.append([a_, b_, False])
    if scenes and scenes[-1]["to"] < DUR - 4 * FPS:
        holes.append([scenes[-1]["to"], DUR, False])

    # 🔴 SOI STILL LAN 2 — ba loi, deu da sua o day:
    #  ① bang DE LEN CLIP thi gan nhu khong doc duoc (nen anh sang loa: g5100 gac mai,
    #     g11700 tam nhom). => bang CHI dat trong KHE nen kem. Khong co khe gan thi BO
    #     bang do, tha thieu con hon de mot bang khong ai doc noi.
    #  ② chu trong o navy (dong danh dau *) BI CAT: 「体感 31度」「約20倍」「室温より5度低い」.
    #     Co chu 40-46 qua lon cho be ngang o. => ha ve 34.
    #  ③ the chu lap khe cat cau giua chung (「…ありが」) VA trung y nguyen phu de ngay
    #     duoi no. => BO HAN. Khe khong co bang thi de nen kem + phu de, sach hon.
    #  ⚠️ THU "chi dat bang trong khe" -> BO MAT 4/7 bang, va dung 4 con so DAT NHAT
    #     bai (60度 gac mai · 20 lan nhom · 40 do mai tranh · 52.9度 tuong dat).
    #     => giu bang DUNG moc cau thoai, va khi no de len clip thi bat LOP SCRIM
    #     toi mo o duoi. Do la cach phim tai lieu van lam; khe van duoc uu tien.
    # 🔴 SUA 2026-09-04 (user: *"số liệu text thì bé nằm trùng màu khó đọc và nằm
    #    thọt vào. Mày cho to ra cho nó cân bằng"*) — ba loi, deu do tao:
    #  ① BE: da ha 46 -> 34 de chua loi KHAC (chu vo hinh trong o navy), roi khi
    #     tim ra nguyen nhan that (mau nen, khong phai co chu) thi QUEN NANG LAI.
    #     => 52, va o so tu rong theo (minWidth = size*4.6 trong TextClip).
    #  ② TRUNG MAU — 🔴 TAO DA CHUA NGUOC HUONG MOT VONG:
    #     nhan trai la chu DEN (`color:'#2B2A28'` dong cung trong preset). Tao tang
    #     scrim TOI tu 0.72 -> 0.82 => nen cang toi thi chu den cang CHIM. Soi still
    #     thay 窓・ドア / みがいたアルミ / 外壁 mat han.
    #     => scrim phai SANG: nen kem #F5EFE3 @0.86. Chu den noi ro, o vang van noi,
    #     va nen kem dung mau khuon kenh. Bai hoc: truoc khi chinh do dam cua scrim,
    #     hoi "chu tren no la mau gi" — toi/sang la HAI huong nguoc nhau.
    #  ③ THOT VAO GOC: preset mac dinh `x=90, y=200` ma tao chua bao gio dat layout
    #     => bang dinh goc tren-trai. Nay CAN GIUA ngang + dat cao hon (y=210).
    #  ④ (user 2026-09-04, lan 2: *"tao không muốn để nền trắng như thế. Sửa lại nó
    #     thành video hoặc cái gì đi"*) — scrim `kind:background` phu TOAN KHUNG nen
    #     nen kem @0,86 van doc ra la "nen trang", du co mo mo hinh phia sau.
    #     => BO scrim toan khung. Thay bang PANEL kem bo goc CHI CHE DUNG VUNG BANG
    #     (~1268px rong, cao theo so dong). Phan con lai cua khung = VIDEO nguyen ven.
    #     Panel la anh PNG co alpha, dat bang `kind:sticker` (co layout x/y/w) —
    #     `kind:background` KHONG nhan layout nen khong lam duoc viec nay.
    # ⛔ PANEL DA BO (user bac ca panel kem lan scrim toan khung). Moi dong bang gio
    #    nam TRON trong o co nen cua preset (label rong) => khong con mang nen nao,
    #    chi vai o chu noi tren video. `panel` giu rong de track khong doi hop dong.
    STAT_SIZE = 52
    STAT_W = 1080
    STAT_LAYOUT = {"x": (1920 - STAT_W) // 2, "y": 230, "w": STAT_W}
    panel = []
    for k, (q, (body, _sz)) in enumerate(STAT.items()):
        i = find(q)
        if i is None:
            print("⚠️  STAT khong map duoc:", q)
            continue
        fs, ds = F(i) + 30, 9 * FPS
        # 🔴 color = MAU NEN cua dong danh dau `*`, KHONG phai mau chu.
        #    `TextClip.tsx` preset flat-stat: `background: hot ? clip.color : '#FFFFFF'`
        #    con `color: '#1A1A18'` DONG CUNG (luon den). Truyen INK (navy dam) =>
        #    chu den tren nen navy dam = VO HINH. Da soi still 3 vong moi ra:
        #    trong khong giong "chu bi cat", ma la chu chim han vao nen.
        #    => truyen AMBER: nen vang + chu den, dong nhan doc ro nhat bang.
        #    ⚠️ build_remotion_27.py cung truyen INK -> video 27 nhieu kha nang dinh
        #    cung loi; sua o day KHONG dung preset dung chung (mot viec mot tang).
        stat.append(txt(f"st-{k}", body, fs, ds, "flat-stat", color=AMBER,
                        layout=STAT_LAYOUT, size=STAT_SIZE))

    T = lambda i, n, ty, c: {"id": i, "name": n, "type": ty, "muted": False,   # noqa: E731
                             "hidden": False, "locked": False, "clips": c}
    tracks = [
        T("trk-video", "clip thật", "video", vid),
        # panel PHAI nam sau trk-video (z-order theo thu tu track) va truoc trk-stat
        T("trk-panel", "panel dưới bảng", "sticker", panel),
        T("trk-stat", "bảng số liệu", "text", stat),
        T("trk-tag", "tag", "text", tag),
        T("trk-voice", "giọng", "audio",
          [{"id": "v", "kind": "audio", "from": 0, "durationInFrames": DUR,
            "asset": "assets/voice.mp3", "volume": 1, "trimStartFrames": 0}]),
    ]
    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "co-dai", "templateRef": "co-dai", "fps": FPS,
                 "width": 1920, "height": 1080,
                 "createdAt": "2026-09-04T00:00:00.000Z",
                 "modifiedAt": "2026-09-04T00:00:00.000Z"},
        "timeline": {"durationInFrames": DUR},
        "sceneMarkers": [{"id": f"sc-{k}", "atFrame": s["f"], "label": s["name"]}
                         for k, s in enumerate(scenes)],
        "tracks": tracks,
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": CAP_SIZE,
                     "lines": [{"text": c["text"],
                                "startMs": round(c["start"] * 1000),
                                "endMs": round(c["end"] * 1000)}
                               for l in lines for c in split_caption(l)],
                     "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236",
                              "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F2EDE4"},
    }

    out = RV / "projects" / NAME
    out.mkdir(parents=True, exist_ok=True)
    (out / "project.json").write_text(json.dumps(proj, ensure_ascii=False, indent=1),
                                      encoding="utf-8")

    # ── 4. copy asset ──────────────────────────────────────────────────────
    ad = RV / "public" / "projects" / NAME / "assets"
    ad.mkdir(parents=True, exist_ok=True)
    n_cp = 0
    for _, name in fixed:
        src, dst = cdir / f"{name}.mp4", ad / f"{name}.mp4"
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy(src, dst)
            n_cp += 1
    wav = vd / "voice.wav"
    if wav.exists() and (not (ad / "voice.mp3").exists()
                         or (ad / "voice.mp3").stat().st_mtime < wav.stat().st_mtime):
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-c:a", "libmp3lame",
                        "-q:a", "2", str(ad / "voice.mp3")], check=True, capture_output=True)

    # ── 5. GATE ────────────────────────────────────────────────────────────
    bad = []
    want = {c["asset"].split("/")[-1] for c in vid} | {"voice.mp3"}
    m2 = sorted(w for w in want if not (ad / w).exists())
    if m2:
        bad.append(f"thiếu asset: {m2[:5]}")
    rep = [n for n, c in collections.Counter(s["name"] for s in scenes).items() if c > 1]
    if rep:
        bad.append(f"clip lặp: {rep}")
    # 🔴 KHE la CO CHU Y (nen kem + bang so) — chi CHONG nhau moi la loi.
    #    Gate ban dau bat ca khe => bao do tren mot project dung. Sua cho no do
    #    dung thu no muon do (cung benh `audience-45plus.md` §6.10).
    # chong DUNG `FADE` frame la CO CHU DINH (dissolve). Chong hon the moi la loi.
    ovl = []
    for k in range(len(vid) - 1):
        end = vid[k]["from"] + vid[k]["durationInFrames"]
        over = end - vid[k + 1]["from"]
        if over > FADE:
            ovl.append(f"{scenes[k]['name']}(+{over}f)")
    if ovl:
        bad.append(f"clip chồng QUÁ {FADE} frame: {len(ovl)} ({ovl[:3]})")
    # va phai KHONG con khe: moi diem tren timeline deu co clip phu
    holes2 = [k for k in range(len(vid) - 1)
              if vid[k]["from"] + vid[k]["durationInFrames"] < vid[k + 1]["from"]]
    if holes2:
        bad.append(f"còn KHE giữa clip: {len(holes2)} chỗ")
    over = [c["text"] for l in lines for c in split_caption(l) if len(c["text"]) > CAP_MAX]
    if over:
        bad.append(f"phụ đề >{CAP_MAX} ký: {len(over)} khối")
    # nhip hinh: tran 6 lan doi hinh/phut (`audience-45plus.md` §2 muc 1)
    per_min = len(scenes) / (DUR / FPS / 60)
    if per_min > 6.0:
        bad.append(f"đổi hình {per_min:.1f}/phút > trần 6")
    tiny = [s["name"] for s in scenes if s["d"] < 3 * FPS]
    if tiny:
        bad.append(f"clip <3s (quá chớp): {len(tiny)} ({tiny[:3]})")

    print("clip copy: %d | video %d · stat %d · tag %d | dur %.1f phút"
          % (n_cp, len(vid), len(stat), len(tag), DUR / FPS / 60))
    if bad:
        print("🔴 GATE:" + NL + NL.join("   " + b for b in bad))
        sys.exit(1)
    print("✅ GATE SẠCH → " + str(out / "project.json"))


if __name__ == "__main__":
    main()
