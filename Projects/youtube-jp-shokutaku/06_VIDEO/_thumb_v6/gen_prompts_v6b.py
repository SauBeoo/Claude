# -*- coding: utf-8 -*-
"""Sinh 9 prompt khuôn v6b (SINH ĐỘNG) vào PROMPTS_v6.md.

Khuôn đúc từ bản video 04 user gen 2026-08-05: cụm món (+ mô hình tạng) một bên,
BẢNG ĐEN đặt chữ bên kia, đúng 1 hệ hiệu ứng hạt phát sáng mang nghĩa của bài.
Định mức hiệu ứng khoá bằng SỐ (5-7 hạt, mỗi hạt >=3% cao khung, 1 đường) — vì
"ít thôi" nói bằng lời thì mỗi lần gen một kiểu.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V = [
 ("01", "mQevRS1qBbk", "halved boiled eggs with glossy yolks in a small ceramic dish",
  "a single gentle arc of 5 to 7 soft glowing warm-white spheres drifting UP AND AWAY from the "
  "eggs and out of the frame - the nutrition being lost",
  "left", "right", "top-right", "そのゆで卵", "半分ムダ", "原因はコレ"),
 ("02", "31KXwgHbLY0", "a white bowl of fresh blueberries with a few frosted frozen ones beside it",
  "a single gentle arc of 5 to 7 soft glowing deep-violet spheres drifting UP AND AWAY from the "
  "frozen berries and out of the frame - the goodness escaping",
  "left", "right", "top-right", "凍ったまま？", "恵み半分", "正解はコレ"),
 ("03", "BKh-sdhsNUg",
  "a realistic anatomical model of a human kidney (clean matte medical teaching model, bean-shaped, "
  "muted red-brown, one half cut open to show the inner structure) standing upright, with fresh "
  "cucumber, a cabbage wedge and a tomato low around its base",
  "a single gentle arc of 5 to 7 soft glowing pale-green spheres travelling FROM the vegetables "
  "INTO the kidney model - support flowing in",
  "right", "left", "top-right", "体にいいのに", "腎臓が疲れる", "5つの食べ物"),
 ("05", "BL7KtdXpl_A",
  "a bowl of natto topped with chopped spring onion, a banana and half an avocado beside it, and "
  "directly behind them a realistic anatomical model of a human kidney (clean matte medical "
  "teaching model, bean-shaped, muted red-brown, one half cut open)",
  "a single gentle arc of 5 to 7 soft glowing amber spheres travelling FROM the food and SETTLING "
  "ON the kidney model, the ones nearest the kidney slightly larger - a burden piling up",
  "right", "left", "top-right", "納豆と一緒", "腎臓に負担", "7つの組合せ"),
 ("06", "dabD8WcvXu8", "a tall glass of tomato juice with a plain unlabelled bottle blurred behind it",
  "a single narrow stream of 6 or 7 small bright-white salt crystals falling from above INTO the "
  "glass, catching the light - salt being added without you noticing",
  "left", "right", "top-right", "毎朝の一杯", "食塩入り！?", "ラベル一行"),
 ("07", "utNRgxBSf-8", "a rustic bowl heaped with cooked azuki beans with a wooden spoon",
  "a single gentle arc of 5 to 7 soft glowing warm-gold spheres rising FROM the bowl and spreading "
  "outward - goodness being released",
  "left", "right", "top-right", "あずき一さじ", "体が変わる", "6つの変化"),
 ("08", "ySxrtSzj8Bg", "a Japanese teacup of bright green tea beside a small kyusu teapot",
  "a single wisp of steam rising from the cup carrying 5 to 7 soft glowing pale-green spheres UP "
  "AND AWAY out of the frame - the benefit escaping with the heat",
  "left", "right", "top-right", "毎日の緑茶", "半分ムダ", "NGは4つ"),
 ("09", "LvBPBN1Jg4U", "a glass jar of golden honey with a wooden dipper lifting a thread of honey",
  "a single gentle arc of 5 to 7 soft glowing warm-amber spheres rising from the honey thread, the "
  "highest ones fading out - the goodness weakening",
  "left", "right", "top-right", "はちみつに", "働き半分", "避ける3つ"),
 ("10", "Iazj6ey7gyI",
  "a half cabbage with its cut face toward the camera showing the layers, on a bright cutting board",
  "a single wisp of steam rising from the cut face carrying 5 to 7 soft glowing pale-yellow spheres "
  "UP AND AWAY out of the frame - the vitamin C boiling off",
  "left", "right", "top-right", "茹でてる？", "4割 逃げる", "正解はコレ"),
]

TPL = """Bright high-key photograph, 16:9. Sunlit Japanese kitchen, soft warm daylight from a window,
pale wood and light walls - the whole frame reads bright, airy and clean, never moody, never dark.

LEFT-RIGHT LAYOUT, two zones only:

(1) SUBJECT ZONE - the {img} side of the frame:
    {cluster}
    Sharply focused, appetising, standing on the sunlit surface. Nothing else competes with it:
    no hands, no people faces, no extra props, no readable labels, no brand names, no text on
    any packaging.

(2) TEXT ZONE - the {txt} side of the frame: a real dark green chalkboard in a plain wooden
    frame, hanging on the wall, photographed in place inside the same scene, its surface
    slightly chalk-dusted. It must look like a physical object in the room - NOT a flat graphic
    panel pasted on top, no hard cut-out edge, no drop-shadow rectangle.

EFFECT - EXACTLY ONE, and this is the whole effect budget:
    {fx}
    Hard limits: 5 to 7 spheres, NO MORE; each sphere at least 3% of the frame height so it
    still reads when the picture is shrunk to 120 pixels wide; all of them on ONE single path,
    never scattered around the frame; soft glow only - no lens flare, no sparkle stars, no light
    rays, no motion-blur streaks. At most ONE sphere, the biggest, may carry a short label; the
    rest stay plain.
    NOTHING ELSE: no small numbered icon boxes, no little diagrams, no side badges, no arrows,
    no charts, no secondary illustrations anywhere in the frame.

TEXT written on the chalkboard, three lines stacked, heavy rounded Japanese gothic, each line
in outlined 袋文字 with a soft drop shadow. The three lines fill about 75% of the chalkboard
height:
  line 1, WHITE, smaller ........................  {l1}
  line 2, WARM GOLD with a dark red outline, THE BIGGEST - glyph height at least one third of
  the frame height, it should feel almost too big   {l2}
  line 3, BRIGHT YELLOW with a black outline ....  {l3}

Keep the {corner} corner free of important detail - no text there and no key part of the
subject - a channel badge is stamped there afterwards. Keep the bottom-right corner free of
text as well, YouTube puts its duration badge there. Do NOT draw any yellow stripe and do NOT
draw any circular badge; both are added later by tool.

No red prohibition mark, no green circle, no split screen, no watermark, not gory."""

TITLES = {"01": "ゆで卵", "02": "ブルーベリー", "03": "腎臓・野菜", "05": "納豆",
          "06": "トマトジュース", "07": "あずき", "08": "緑茶", "09": "はちみつ", "10": "キャベツ"}
CF = {"top-right": "tr", "bottom-left": "bl"}

HEADER = """## 2c. KHUÔN **v6b SINH ĐỘNG** — 9 prompt còn lại (soạn 2026-08-05, sau khi user gen video 04)

> user: *"cho tao cái prompt nó sinh động như này đi. Có cả hiệu ứng nhưng ít thôi nhé không nó sẽ rối mắt"*.
> **Bản mẫu = video 04 user đã gen** (`06_VIDEO/_thumb_v6/src/04_src.jpg`): ly sữa + mô hình xương + hạt Ca²⁺ phát sáng + **BẢNG ĐEN** đặt chữ.

**Đo bản mẫu ở 120px — cái gì sống, cái gì chết:**

| yếu tố | ở 120px |
|---|---|
| 3 dòng chữ trên **bảng đen** | **đọc rõ cả 3** — dù dòng vàng chỉ **19,5%** khung |
| ly sữa + mô hình xương | nhận ra được ✓ |
| hạt `Ca²⁺` | còn đốm sáng, **chữ Ca²⁺ mất hẳn** → hết là thông tin |
| dải icon **① ② ③** | **một vệt xám nhòe** = đúng chỗ rối mắt, lại lặp thông tin của chữ 「見直す3つ」 |
| sáng TB | **154** — sáng, đạt gate nền sáng ✓ |

⭐ **Phát hiện đưa thành khuôn: thứ làm chữ đọc được ở 120px là TẤM BẢNG ĐEN, không phải cỡ chữ.**
Chữ trên bảng đen thắng cả những bản chữ to hơn nhưng đặt trực tiếp lên ảnh (01 ゆで卵 dòng chính
48,6% mà vẫn khó đọc vì nền lẫn). Nên v6b khoá bảng đen làm vùng chữ cố định.

**Định mức hiệu ứng — khoá bằng SỐ, không nói "ít thôi"** (nói bằng lời thì mỗi lần gen một kiểu):
đúng **1 hệ hiệu ứng** · **5–7 hạt** · mỗi hạt **≥3% chiều cao khung** (sống được ở 120px) ·
**1 đường duy nhất** · chỉ **hạt to nhất** được mang chữ · **cấm** dải icon ①②③, sơ đồ nhỏ,
badge phụ, mũi tên, tia sáng, sparkle, motion-blur.

**Hiệu ứng phải MANG NGHĨA của bài, không trang trí** — mỗi video một cơ chế: mất chất bay đi
(01·02·08·09·10) · chất chảy VÀO tạng (03) · gánh nặng đọng lại trên tạng (05) · muối rơi vào ly
(06) · chất toả ra (07).

⚠️ **Video 04 GIỮ NGUYÊN, không gen lại** — nó tốt, chỉ dải icon là thừa; đừng lặp dải icon đó ở
9 bản còn lại.

"""


def main() -> None:
    out = [HEADER]
    for n, vid, cluster, fx, img, txt, corner, l1, l2, l3 in V:
        out.append(f"### {n} {TITLES[n]} — `{vid}` · badge `--corner {CF[corner]}`\n")
        out.append("```")
        out.append(TPL.format(cluster=cluster, fx=fx, img=img, txt=txt,
                              corner=corner, l1=l1, l2=l2, l3=l3))
        out.append("```\n")

    p = Path(__file__).resolve().parents[1] / "_thumb_audit" / "PROMPTS_v6.md"
    t = p.read_text(encoding="utf-8")
    anchor = "## 3. BẢNG 10 VIDEO"
    if "## 2c. KHUÔN" in t:
        t = t[:t.index("## 2c. KHUÔN")] + t[t.index(anchor):]
    p.write_text(t.replace(anchor, "\n".join(out) + "\n" + anchor, 1), encoding="utf-8")

    blk = p.read_text(encoding="utf-8").split("## 2c.")[1].split(anchor)[0]
    fences = re.findall(r"```(.*?)```", blk, re.S)
    leftover = [x for f in fences for x in re.findall(r"\{[a-z0-9_]+\}", f)]
    print(f"✅ ghi {len(fences)} prompt v6b vào {p.name} | token còn sót: {leftover or 'KHÔNG'}")


if __name__ == "__main__":
    main()
