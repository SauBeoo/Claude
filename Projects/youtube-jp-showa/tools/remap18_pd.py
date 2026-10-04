# -*- coding: utf-8 -*-
"""Video 18: thay film_lines dokkoi (ban quyen chua het) bang phim PD moi.
--check : dung sheet kiem 3 moc/o (dau · giua · cuoi) o 480px, KHONG sua plan.
--apply : ghi lai visual_plan.json (backup .bak_dokkoi)."""
import sys, json, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(r"E:\Claude\Projects\youtube-jp-showa")
VD = ROOT / "06_VIDEO" / "18_hataraku-okane"
PD = ROOT / "06_VIDEO" / "_footage_pd"
A, B, C, D, E = ("usaf11018_way_of_life_tokyo_1945.mp4", "usaf11022_industrial_life_1946.mp4",
                 "npc14671_ruins_tokyo_1945.mp4", "npc14672_street_tokyo_1945.mp4", "univ_japan_today_1946.mp4")
# anchor (dung chuoi dang co trong visual_plan) -> (src, ss, note); None = chuyen sang aistill
MAP = {
    "母親の葬式の夜":           (C, 62, "pho do nat yen lang, cay tro troi"),
    "十五で東京へ出た兄":        None,
    "こんばんは。昭和くらし図鑑です": (B, 5, "toan canh Yawata, cau sat"),
    "封筒を開きながら":          (B, 484, "hang cong nhan di lam"),
    "昭和二十四年。戦争から戻った父": (D, 12, "ong gia giua do nat"),
    "朝六時。今では見かけなくなった光景": (B, 200, "dam dong cong nhan tap trung buoi sang"),
    "荷台の上は、風が冷たい":      (B, 650, "xe ngua cho hang"),
    "夕方、仕事が終わると":        (E, 24, "tay trao tien"),
    "二百四十円ほど":            (A, 644, "gia dinh nau an ngoai troi"),
    "戦争が終わって、仕事のない人が": (E, 60, "dam dong rat lon tren pho"),
    "この年、緊急失業対策法":      (B, 742, "nguoi cui boc go vao bao"),
    "その日の日当で、その日の米を買う": (A, 570, "xom lieu phoi do"),
    "父が初めてもらった日当":      (C, 320, "vo chong cuoi"),
    "日雇いの賃金は、少しずつ":     (C, 430, "tho dung khung go"),
    "前の晩、母が、柳行李":        None,
    "「体にだけは、気をつけるんだよ」": None,
    "兄が勤めたのは":            (A, 264, "may tien trong xuong"),
    "行き先は、東京の工事現場です":   (C, 455, "tho tren khung go"),
    "正月にも、帰れない年があります":  (A, 683, "nha go phoi quan ao"),
    "その一方で、東京では":        (B, 1153, "ben cang thuyen"),
    "自分の稼いだお金で":          None,
    "集団就職の列車、出稼ぎの冬":     (B, 306, "mat tho mo tre nhin may"),
    "道路の穴を埋める。川の土手に":   (B, 780, "nguoi xuc go"),
    "では、なぜ、国が毎日の仕事を":   (E, 9, "dam dong truoc toa nha"),
    "駅のホームには、同じ学生服の":   None,
    "列車は、夜通し走ります":       None,
    "家には、子どもを高校にやる余裕が": (E, 73, "cho troi"),
    "仕事中の事故で亡くなった人は":   (B, 410, "thep do ruc tren truc can"),
    "村に残るのは、母と":          (A, 1210, "phu nu khan trang ngoi co"),
    "当時の労働省の調べでは、昭和四十七年度": (B, 245, "dam dong tho mo"),
    "ところが翌年、オイルショック":   (B, 460, "cong nha may"),
    "十五で親元を離れることも":      None,
    "誰かが送ってくれたお金で":      (D, 45, "cau be ngoi tren dong sat vun"),
}

vp = json.loads((VD / "visual_plan.json").read_text(encoding="utf-8"))
plan = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
old = {f[0]: f for f in vp["film_lines"]}
assert set(MAP) == {k for k, f in old.items() if f[1].startswith("dokkoi")}, \
    sorted(set(MAP) ^ {k for k, f in old.items() if f[1].startswith("dokkoi")})

# do dai can cho moi anchor = tong dur cac o film thuoc dong do (+0,6)
need = {}
for k in MAP:
    rows = [r for r in plan if r["layer"] == "film" and r["text"].startswith(k[:6]) and r["src"].startswith("dokkoi")]
    need[k] = sum(r["dur"] for r in rows) + 0.6 if rows else 8

if "--check" in sys.argv:
    out = VD / "_remap_check"; out.mkdir(exist_ok=True)
    tiles = []
    for k, v in MAP.items():
        if v is None: continue
        src, ss, note = v
        for j, t in enumerate((ss + 0.3, ss + need[k] / 2, ss + need[k] - 0.3)):
            f = out / ("%s_%d.jpg" % (abs(hash(k)) % 10**6, j))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.2f" % t, "-i", str(PD / src), "-frames:v", "1",
                            "-vf", "scale=480:-2", str(f)], check=True)
            tiles.append((f, "%s | %s %.0f+%.1f" % (k[:10], src[:9], ss, need[k])))
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
    shutil.copy(VD / "visual_plan.json", VD / "visual_plan.json.bak_dokkoi")
    fl = []
    for f in vp["film_lines"]:
        if f[0] in MAP:
            v = MAP[f[0]]
            if v is None: continue
            fl.append([f[0], v[0], v[1], v[2]])
        else:
            fl.append(f)
    vp["film_lines"] = fl
    (VD / "visual_plan.json").write_text(json.dumps(vp, ensure_ascii=False, indent=1), encoding="utf-8")
    print("film_lines:", len(fl), "| chuyen aistill:", sum(1 for v in MAP.values() if v is None))
