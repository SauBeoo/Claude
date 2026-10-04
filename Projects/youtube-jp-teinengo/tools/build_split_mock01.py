# build_split_mock01.py — Remotion layout MOCK for teinengo split-screen (left 退屈になる人 / right 楽しくなる人).
# Placeholders only (no real AI images yet) -> render a still for layout approval. NOT for final render.
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RV = r"E:\Claude\Projects\remotion-vox"
NAME = "teinengo-01-splitmock"
ASSET_DIR = os.path.join(RV, "public", "projects", NAME, "assets")
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(os.path.join(RV, "projects", NAME), exist_ok=True)
FONT = r"C:\Windows\Fonts\YuGothB.ttc"

def placeholder(fn, top, bot, label):
    W, H = 1376, 768
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    f = ImageFont.truetype(FONT, 56)
    d.multiline_text((W // 2, H // 2), label, font=f, fill=(255, 255, 255), anchor="mm", align="center", spacing=18)
    im.save(os.path.join(ASSET_DIR, fn))

placeholder("A_left.png", (92, 98, 108), (58, 62, 70), "ẢNH A (AI người thật)\n布団の中で天井を見つめる\n薄暗い朝")
placeholder("B_right.png", (250, 214, 160), (214, 150, 92), "ẢNH B (AI người thật)\nカーディガンを着て\n朝日の玄関を出る")

FPS, DUR = 30, 30 * 8
W, H = 1920, 1080
BOX_W, BOX_H, BOX_Y, GAP = 900, 506, 170, 40        # two 16:9 boxes, no crop
LX = (W - 2 * BOX_W - GAP) // 2                      # 40
RX = LX + BOX_W + GAP                                # 980

def centered_x(box_x, text, size):
    return int(box_x + BOX_W / 2 - len(text) * size / 2)

def text(id_, content, preset, x, y, size, color, frm=0, anim="pop"):
    return {"id": id_, "kind": "text", "from": frm, "durationInFrames": DUR - frm, "content": content,
            "preset": preset, "color": color, "animation": anim, "layout": {"x": x, "y": y}, "fontSize": size}

L_LAB, R_LAB = "退屈になる人", "楽しくなる人"
L_Q, R_Q = "「起きても、することがない」", "「とりあえず、着替えるか」"
LAB, Q = 58, 54
proj = {
    "version": 1,
    "meta": {"name": NAME, "channel": "teinengo", "fps": FPS, "width": W, "height": H},
    "timeline": {"durationInFrames": DUR},
    "tracks": [
        {"id": "bg", "name": "bg", "type": "background", "clips": [
            {"id": "bg0", "kind": "background", "from": 0, "durationInFrames": DUR,
             "tint": "#1E2638", "tintOpacity": 1, "grid": False, "dots": False}]},
        {"id": "pics", "name": "pics", "type": "video", "clips": [
            {"id": "A", "kind": "video", "from": 0, "durationInFrames": DUR, "asset": "assets/A_left.png",
             "layout": {"x": LX, "y": BOX_Y, "w": BOX_W, "h": BOX_H},
             "filter": {"saturate": 0.35, "brightness": 0.9}, "fadeInFrames": 12},
            {"id": "B", "kind": "video", "from": 9, "durationInFrames": DUR - 9, "asset": "assets/B_right.png",
             "layout": {"x": RX, "y": BOX_Y, "w": BOX_W, "h": BOX_H},
             "filter": {"saturate": 1.12, "brightness": 1.04}, "fadeInFrames": 12}]},
        {"id": "labels", "name": "labels", "type": "text", "clips": [
            text("lab_l", L_LAB, "tag", centered_x(LX, L_LAB, LAB) - 34, 52, LAB, "#AEB9CB"),
            text("lab_r", R_LAB, "tag", centered_x(RX, R_LAB, LAB) - 34, 52, LAB, "#FFB547", frm=9)]},
        {"id": "quotes", "name": "quotes", "type": "text", "clips": [
            text("q_l", L_Q, "telop", centered_x(LX, L_Q, Q), BOX_Y + BOX_H + 34, Q, "#FFFFFF", frm=20),
            text("q_r", R_Q, "telop", centered_x(RX, R_Q, Q), BOX_Y + BOX_H + 34, Q, "#FFFFFF", frm=40)]},
    ],
    "captions": {"source": "none", "style": "outline", "enabled": True, "fontSize": 44,
                 "lines": [{"text": "たったこれだけの差が、一年後には、まるで別の人生になります。", "startMs": 0, "endMs": 8000}]},
}
p = os.path.join(RV, "projects", NAME, "project.json")
json.dump(proj, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", p, "| boxes", LX, RX, BOX_Y, BOX_W, BOX_H)
