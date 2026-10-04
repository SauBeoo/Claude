# -*- coding: utf-8 -*-
"""Video 18 lan 3: MOI o phim -> nguon MAU 720p (.mov goc archive.org). Bo het phim den trang/360p.
User 23/09: "thay toan bo nhung video mo nhieu la video mau sac net hon" + "video AI do dang loi".
--check : sheet 3 moc/o o 480px (khong sua plan)
--apply : ghi visual_plan.json (backup .bak_hd); bo cac anchor khoi list "ai" khi da thanh phim."""
import sys, json, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "18_hataraku-okane"
PD = ROOT / "06_VIDEO" / "_footage_pd"
K = "usaf11059_kyoto_home_1946_hd.mov"
O = "usaf11026_repatriates_otake_1946_hd.mov"
H78 = "usaf11078_hiroshima_life_1946_hd.mov"
H79 = "usaf11079_hiroshima_life_1946_hd.mov"
AG = "usaf11050_agri_1946_hd.mov"
B = "usaf11022_industrial_life_1946_hd.mov"
A = "usaf11018_way_of_life_tokyo_1945_hd.mov"
M = "usaf11068_industry_1946_hd.mov"
T = "usaf11069_transport_1946_hd.mov"
# anchor -> (src, ss, note). Tat ca la MAU 720p.
MAP = {
 "母親の葬式の夜":             (K, 1024, "me deo kappogi ben bon rua (Kyoto 1946)"),
 "中には、郵便局の封筒が":       (O, 648, "nguoi linh ve que ngoi viet thu"),
 "十五で東京へ出た兄":          (O, 824, "dong nguoi tre mang boc do roi di"),
 "三人のうち、封筒がいちばん多かったのは、誰なのか": (O, 928, "can mat phu nu, tre con giua dam dong"),
 "こんばんは。昭和くらし図鑑です":  (B, 5, "toan canh Yawata, cau sat"),
 "封筒を開きながら":            (B, 484, "hang cong nhan di lam"),
 "昭和二十四年。戦争から戻った父":  (O, 1284, "can mat linh phuc vien"),
 "朝六時。今では見かけなくなった光景": (B, 200, "dam dong cong nhan tap trung buoi sang"),
 "荷台の上は、風が冷たい":        (O, 100, "nguoi ngoi tren thung xe tai"),
 "夕方、仕事が終わると":          (H79, 468, "tay trao tien o cho"),
 "二百四十円ほど":              (A, 644, "gia dinh nau an ngoai troi"),
 "戦争が終わって、仕事のない人が":  (O, 892, "bien nguoi dan thuong"),
 "この年、緊急失業対策法":        (B, 742, "nguoi boc go giua bai do"),
 "その日の日当で、その日の米を買う": (A, 570, "xom lieu phoi do"),
 "父が初めてもらった日当":        (K, 774, "gia dinh an com ben chabudai"),
 "日雇いの賃金は、少しずつ":       (H78, 866, "cong nhan nha in ben may in"),
 "兄が勤めたのは":              (A, 264, "may tien trong xuong"),
 "行き先は、東京の工事現場です":     (AG, 212, "dan ong dao dat tren suon doi"),
 "正月にも、帰れない年があります":    (A, 683, "nha go phoi quan ao"),
 "その一方で、東京では":          (B, 1153, "ben cang thuyen"),
 "集団就職の列車、出稼ぎの冬":       (B, 306, "mat tho mo tre nhin may"),
 "道路の穴を埋める。川の土手に":     (B, 780, "nguoi xuc go"),
 "では、なぜ、国が毎日の仕事を":     (O, 868, "dam dong di bo"),
 "列車は、夜通し走ります":         (AG, 297, "nhin qua cua so tau, dong ruong luot qua"),
 "家には、子どもを高校にやる余裕が":  (H79, 430, "phu nu ban hang can cho"),
 "仕事中の事故で亡くなった人は":     (B, 410, "thep do ruc tren truc can"),
 "村に残るのは、母と":            (AG, 64, "phu nu cuoc dat"),
 "当時の労働省の調べでは、昭和四十七年度": (B, 245, "dam dong tho mo"),
 "ところが翌年、オイルショック":     (B, 460, "cong nha may"),
 "誰かが送ってくれたお金で":        (K, 1108, "cau be rua mat ben voi nuoc"),
}
SWAP = {"usaf11068_industry_1946.mp4": M, "usaf11069_transport_1946.mp4": T}   # giu moc, doi sang ban HD
DROP_AI = {"中には、郵便局の封筒が", "三人のうち、封筒がいちばん多かったのは、誰なのか"}

vp = json.loads((VD / "visual_plan.json").read_text(encoding="utf-8"))
plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
tl = json.loads((VD / "timeline.json").read_text(encoding="utf-8"))
lines = tl if isinstance(tl, list) else tl.get("lines", tl)

def need(k):
    for x in lines:
        if k in x["text"]:
            return x["end"] - x["start"] + 0.8
    raise SystemExit("🔴 anchor khong khop dong nao: " + k)

if "--check" in sys.argv:
    out = VD / "_remap_hd"; out.mkdir(exist_ok=True)
    tiles = []
    for k, (src, ss, note) in MAP.items():
        n = need(k)
        for j, t in enumerate((ss + 0.3, ss + n / 2, ss + n - 0.3)):
            f = out / ("%02d_%d.jpg" % (list(MAP).index(k), j))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % t, "-i", str(PD / src), "-frames:v", "1",
                            "-vf", "scale=480:-2", str(f)], check=True)
            tiles.append((f, "%s | %s %.0f+%.1f" % (k[:8], src[4:9], ss, n)))
    W, H = 480, 270
    for s in range(0, len(tiles), 30):
        ch = tiles[s:s + 30]
        sh = Image.new("RGB", (W * 3, H * ((len(ch) + 2) // 3)), "black"); d = ImageDraw.Draw(sh)
        for i, (f, lab) in enumerate(ch):
            im = Image.open(f).convert("RGB").resize((W, H)); x, y = (i % 3) * W, (i // 3) * H
            sh.paste(im, (x, y)); d.rectangle((x, y, x + W, y + 14), fill="black"); d.text((x + 3, y + 1), lab, fill="yellow")
        sh.save(out / ("check_%d.jpg" % (s // 30)), quality=85)
    print("sheets ->", out)
elif "--apply" in sys.argv:
    shutil.copy(VD / "visual_plan.json", VD / "visual_plan.json.bak_hd")
    fl, seen = [], set()
    for f in vp["film_lines"]:
        if f[0] in MAP:
            v = MAP[f[0]]; fl.append([f[0], v[0], v[1], v[2]]); seen.add(f[0])
        elif f[1] in SWAP:
            fl.append([f[0], SWAP[f[1]], f[2], f[3]])
        else:
            raise SystemExit("🔴 film_line chua co nguon HD: %s (%s)" % (f[0], f[1]))
    for k, v in MAP.items():
        if k not in seen:
            fl.append([k, v[0], v[1], v[2]])
    vp["film_lines"] = fl
    vp["ai"] = [x for x in vp["ai"] if x not in DROP_AI]
    (VD / "visual_plan.json").write_text(json.dumps(vp, ensure_ascii=False, indent=1), encoding="utf-8")
    print("film_lines:", len(fl), "| ai:", len(vp["ai"]))
