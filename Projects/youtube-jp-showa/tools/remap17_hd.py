# -*- coding: utf-8 -*-
"""Video 17 lan HD (2026-09-23, user: "tuong tu cho video 17"): moi o phim -> MAU 720p.
 · 33 o den trang 320x240 (We the Japanese · You in Japan) + Color Story (KHONG co license tren archive.org) -> phim USAF mau 720p
 · 22 o USAF 640x360 -> cung moc, ban .mov 720p
 · 11 o Japan Today 1959 (mau, CC0) -> cung moc, ban .mpeg bitrate cao (neu da tai)
--check : sheet 3 moc/o (chi o thay moi)   --apply : ghi film_spec.json (backup .bak_hd)"""
import sys, json, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\_footage_pd")
VD = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\17_kaisha-ga-kureta")
OF = "usaf11078_hiroshima_life_1946_hd.mov"      # van phong, bao in, may in (08:56-15:20)
MI = "usaf11079_hiroshima_life_1946_hd.mov"      # cho, Miyajima, cong truong
KY = "usaf11059_kyoto_home_1946_hd.mov"
OT = "usaf11026_repatriates_otake_1946_hd.mov"
NEW = {  # id -> (src, ss, note)
 "clip_00": (OF, 548, "dan ong lam viec ben ban giay"),
 "clip_01": (OF, 648, "nhom nhan vien quanh ban dai"),
 "clip_02": (OF, 652, "nhom nhan vien quanh ban dai (tiep)"),
 "clip_03": (OF, 631, "can mat nhan vien deo kinh"),
 "clip_04": (OF, 640, "nam nu ben ban lam viec"),
 "clip_09": (MI, 540.5, "Miyajima torii"),
 "clip_12": (KY, 1195, "bo song Kamo"),
 "clip_13": (OT, 944, "mat nguoi cuoi giua dam dong"),
 "clip_16": (OF, 581, "nhan vien ben bang den co chu"),
 "clip_17": (OF, 672, "tay cam giay to"),
 "clip_18": (OT, 176, "dam dong nhin, mat nguoi"),
 "clip_22": (OF, 796, "khuon chu in"),
 "clip_23": (MI, 392, "cho: bat ngu coc, nguoi ban vai"),
 "clip_24": (OF, 696, "nu nhan vien xep chu in"),
 "clip_25": (OF, 705, "nu nhan vien xep chu in (tiep)"),
 "clip_28": (OF, 687.5, "giay to can"),
 "clip_39": (OF, 832, "truc may in quay"),
 "clip_40": (OF, 880, "keo to giay khoi may in"),
 "clip_61": (MI, 672, "nguoi ra vao cong truong"),
 "clip_70": (KY, 45, "ngo nha go Kyoto"),
 "clip_80": (KY, 50, "ngo nha go Kyoto (tiep)"),
 "clip_82": (MI, 598, "den da, den Miyajima"),
 "clip_83": (MI, 624, "torii va bien"),
 "clip_86": (OF, 774, "tay xep chu in"),
 "clip_90": (KY, 1070, "bep Kyoto"),
 "clip_94": (MI, 580, "den Itsukushima"),
 "clip_108": (OF, 720, "nu xep chu can mat"),
 "clip_110": (OF, 731, "nu xep chu (tiep)"),
 "clip_111": (OF, 838, "may in, giay chay"),
 "clip_112": (OF, 890, "giay in ra"),
 "clip_120": (KY, 1060, "bep, phu nu nau an"),
 "clip_121": (KY, 1248, "phu nu kimono di tren pho Kamo"),
 "clip_126": (OT, 845, "dong nguoi mang boc do di"),
}
SWAP = {"usaf11059_kyoto_home_1946.mp4": KY,
        "usaf11069_transport_1946.mp4": "usaf11069_transport_1946_hd.mov",
        "usaf11068_industry_1946.mp4": "usaf11068_industry_1946_hd.mov"}
JT_HD = PD / "japan_today_1959_hd_sq.mp4"
spec = json.loads((VD / "film_spec.json").read_text(encoding="utf-8"))

if "--check" in sys.argv:
    out = VD / "_remap_hd"; out.mkdir(exist_ok=True)
    dur = {c["id"]: c["dur"] for c in spec["cuts"]}
    tiles = []
    for k, (src, ss, note) in NEW.items():
        for j, t in enumerate((ss + 0.3, ss + dur[k] / 2, ss + dur[k] - 0.3)):
            f = out / ("%s_%d.jpg" % (k, j))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % t, "-i", str(PD / src), "-frames:v", "1",
                            "-vf", "scale=480:-2", str(f)], check=True)
            tiles.append((f, "%s | %s %.0f+%.1f" % (k, src[4:9], ss, dur[k])))
    W, H = 480, 270
    for s in range(0, len(tiles), 36):
        ch = tiles[s:s + 36]
        sh = Image.new("RGB", (W * 3, H * ((len(ch) + 2) // 3)), "black"); d = ImageDraw.Draw(sh)
        for i, (f, lab) in enumerate(ch):
            x, y = (i % 3) * W, (i // 3) * H
            sh.paste(Image.open(f).convert("RGB").resize((W, H)), (x, y))
            d.rectangle((x, y, x + W, y + 14), fill="black"); d.text((x + 3, y + 1), lab, fill="yellow")
        sh.save(out / ("check_%d.jpg" % (s // 36)), quality=85)
    print("sheets ->", out)
elif "--apply" in sys.argv:
    shutil.copy(VD / "film_spec.json", VD / "film_spec.json.bak_hd")
    n = {"new": 0, "swap": 0, "jt": 0}
    for c in spec["cuts"]:
        name = Path(c["src"]).name
        if c["id"] in NEW:
            src, ss, note = NEW[c["id"]]
            c["src"] = str(PD / src); c["ss"] = float(ss); c["grade"] = 0.0
            c["note"] = c["note"].split(" ", 2)[0] + " HD " + note + " · " + c["note"]; n["new"] += 1
        elif name in SWAP:
            c["src"] = str(PD / SWAP[name]); n["swap"] += 1
        elif name == "japan_today_1959.mp4" and JT_HD.exists():
            c["src"] = str(JT_HD); n["jt"] += 1
    left = sorted({Path(c["src"]).name for c in spec["cuts"]})
    (VD / "film_spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(n, "| nguon con lai:", left)
