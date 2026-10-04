# -*- coding: utf-8 -*-
"""
build_remotion_22d2.py — DEMO khuôn video 22 bản 2 (2026-09-09).

Khác demo bản 1 ở chỗ nó dựng từ **lô ảnh SAU khi sửa 5 lỗi cấu trúc prompt** (bối cảnh
9 nơi thay vì 1 phòng · cảm xúc · cỡ máy quay · chừa chỗ đồ hoạ · số liệu kín đặc), và
nó demo **cả hai tầng của phương án lai**:
  · tầng NGƯỜI  — ảnh photoreal do Veo/generator trả về
  · tầng ĐỒ HOẠ — khối `papercut-stat` do FONT vẽ, chữ Nhật luôn sắc (scene 9·10)

⚠️ ĐÂY LÀ DEMO STYLE, KHÔNG PHẢI BẢN DỰNG THẬT:
  · dùng **ẢNH TĨNH** vì lô clip Veo chưa gen — nhưng đó KHÔNG phải cách chữa cháy: đo
    video mẫu thì ảnh của nó **đứng yên tuyệt đối** (drift 0,01–0,07px), sinh động đến từ
    telop churn + nhịp cắt + lớp fx. Demo này chạy đúng cơ chế đó.
  · scene 2 và 8 **dùng lại** ảnh của scene 1 và 4 (thiếu ảnh, ghi rõ chứ không giấu).
  · nội dung hai khối `stat` lấy **verbatim** từ bảng scene đã khoá (`_scenes22.py` scene 16
    và 30) — không bịa số mới, YMYL.

🔴 fps = 24 (`feedback_fps_clip_phai_khop_renderer`): lô clip Veo là 24fps, để project 30fps
   thì 27% frame bị lặp ⇒ judder. Ảnh tĩnh thì fps nào cũng được, nhưng giữ 24 để demo này
   so sánh được trực tiếp với bản dựng thật sau này.
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plan22 import build                                    # noqa: E402
from _scenes22 import SCENES                                # noqa: E402

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-22d2"
FPS, W, H = 24, 1920, 1080
TL = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man\timeline.json"
MASCOT_FRAMES = 192                                          # 8s × 24fps, số THẬT của lô PNG
FADE = 7                                                     # ~0,3s cross-dissolve

f = lambda s: max(0, int(round(s * FPS)))

# grading để rất nhẹ — lô ảnh mới đã sáng sẵn nhờ prompt; nhân mạnh là cháy (đã dính)
GRADE = {"brightness": 1.03, "contrast": 1.0, "saturate": 1.06}

# scene → ảnh. `None` = khối ĐỒ HOẠ font vẽ, không có ảnh.
IMG = {
    0: "s00_bow", 1: "s02_passbook", 2: "s02_passbook", 3: "s03_calendar",
    4: "s21_tablet", 5: "s05_envelope", 6: "s16_barchart", 7: "s07_couple",
    8: "s21_tablet", 9: None, 10: None, 11: "s11_counter",
}
REUSED = {2, 8}                                              # ghi sổ chỗ dùng lại, đừng giấu

# hai khối đồ hoạ — nội dung VERBATIM từ bảng scene đã khoá, không thêm số mới
STAT = {
    9:  ["四月に入るお金|二月分と三月分", "つまり|二か月前の分", "*年金は|後払い"],
    10: ["ひと月|十八万円", "二か月分|三十六万円", "*これが|未支給年金"],
}

# kiểu telop + hiệu ứng, xoay vòng cho khỏi đơn điệu
PRESET = ["telop", "telop-band", "telop-gold"]
# ⚠️ Mật độ đo trên still: sparkle 12 ra ĐÚNG MỘT ngôi sao giữa khung, gần như không thấy.
# 🔴 BỎ `arrow`: ở cỡ toàn khung nó render thành một VỆT CAM to quét ngang mặt người
#    (soi frame 26s bản render đầu). Mũi tên to là việc của lớp đồ hoạ Remotion sắp dựng,
#    không phải của lớp hạt.
# 🔴 LẶP HIỆU ỨNG (user 2026-09-09: *"cách hiệu ứng lặp lại quá nhiều"*): bản trước dùng
#    `sparkle` 3/6 lần ⇒ xem một lúc là thấy đi thấy lại đúng một chùm sao.
# ⇒ Mỗi variant ĐÚNG MỘT LẦN, và thưa hơn hẳn: 4 lần trên 12 scene. Hạt là ĐIỂM NHẤN —
#   rải đều khắp thì không còn gì là nhấn (cùng bài học `audience-45plus.md` §2.0h).
FX = {0: None, 1: ("coins", 18), 2: None, 3: None, 4: ("rays", 14),
      5: None, 6: None, 7: ("confetti", 22), 8: None, 9: None, 10: None,
      11: ("sparkle", 26)}
POSE = ["13", "14", "15"]


def quiet_side(img_path: str) -> str:
    """Bên nào của khung ÍT BẬN hơn — đo, đừng đoán.

    🔴 Bản trước chọn bên đặt hạt bằng `n % 2` (số thứ tự scene). Sai: bên trống là thuộc
       tính của TỪNG TẤM ẢNH, không phải của thứ tự. Kết quả đo trên frame 14s: bà cụ nằm
       nửa PHẢI, hạt lại được nhốt vào nửa phải ⇒ xu vàng phủ kín mặt.
    ⇒ Đo mật độ biên (gradient) của 1/3 trái so với 1/3 phải, trả về bên nhẹ hơn.
    """
    from PIL import Image, ImageFilter
    im = Image.open(img_path).convert("L").resize((480, 270))
    e = im.filter(ImageFilter.FIND_EDGES)
    px = e.load()
    third = 480 // 3
    left = sum(px[x, y] for y in range(20, 250) for x in range(6, third))
    right = sum(px[x, y] for y in range(20, 250) for x in range(480 - third, 474))
    return "left" if left < right else "right"


def split_caption(text, maxlen=78):
    """Chẻ khối phụ đề ≤78 ký, cắt SAU dấu câu.

    🔴 Remotion KHÔNG chẻ hộ như `video_render.py` (SUB_MAXLEN=42): CaptionLayer lấy NGUYÊN
    dòng timeline làm một khối ⇒ dòng dài ra 4 dòng phụ đề che gần hết đáy khung, vi phạm
    `audience-45plus.md` §3 (≤2 dòng/khối).
    """
    if len(text) <= maxlen:
        return [text]
    out, cur = [], ""
    for ch in text:
        cur += ch
        if ch in "。、」）" and len(cur) >= maxlen * 0.55:
            out.append(cur); cur = ""
        elif len(cur) >= maxlen:
            out.append(cur); cur = ""
    if cur:
        out.append(cur)
    return out


def main():
    rows = {r["i"]: r for r in build()}
    idxs = sorted(IMG)
    t0, t1 = rows[idxs[0]]["t0"], rows[idxs[-1]]["t1"]
    total = t1 - t0

    trk_v, trk_fx, trk_t, trk_stat, markers, poses = [], [], [], [], [], []
    for n, i in enumerate(idxs):
        r = rows[i]
        s0, dur = r["t0"] - t0, r["t1"] - r["t0"]
        ext = FADE if n < len(idxs) - 1 else 0
        telop = r["telop"]
        markers.append({"id": f"m{i}", "atFrame": f(s0), "label": telop.replace("\n", " ")})
        poses.append({"atSec": s0, "asset": f"assets/ojii_{POSE[n % 3]}/f_%04d.png"})

        # 🔴 nshot == 0 nghĩa là scene này DÙNG CHUNG clip với scene trước (plan22 phân bổ
        #    theo khối art). Cho nó một ảnh riêng là tự đẩy nhịp đổi hình vượt trần 6/phút
        #    và demo sẽ cắt nhanh hơn bản dựng thật ⇒ nhìn không còn giống nhau nữa.
        share = r["nshot"] == 0 and trk_v and IMG[i]
        if share:
            trk_v[-1]["durationInFrames"] += f(dur)
        elif IMG[i]:
            trk_v.append({
                "id": f"v{i}", "kind": "video", "from": f(s0),
                "durationInFrames": f(dur) + ext,
                "asset": f"assets/{IMG[i]}.jpg", "fit": "cover", "motion": "none",
                "speed": 1.0, "volume": 0, "filter": GRADE,
                **({"curlInFrames": 13, "curlDir": ["br", "tr", "bl", "tl"][n % 4]}
                   if n % 2 == 1 else {"fadeInFrames": FADE if n else 0}),
            })
        else:
            # 🔴 Khối đồ hoạ KHÔNG có ảnh nền — `stage-zu-layout`/§2.0c: vùng giữa chở ĐÚNG
            #    một thứ, ảnh và bảng chồng nhau là mất đọc.
            trk_stat.append({
                "id": f"st{i}", "kind": "text", "from": f(s0) + 8,
                "durationInFrames": f(dur) - 12,
                "content": "\n".join(STAT[i]), "preset": "papercut-stat",
                # 🔴 Mặc định của preset là `x 90 · y 200 · fontSize 50` — mà dải telop trắng
                #    chiếm tới y≈250, nên bảng DÍNH VÀO dải nền và dồn hết sang trái (user:
                #    "text đang bị chèn vào background… cho thấp xuống, to ra, căn giữa").
                #    Đo trên ảnh user gửi: mực bảng chạy x 111→549 ở cỡ 50 ⇒ rộng ~438.
                #    Cỡ 76 ⇒ rộng ≈ 438×76/50 ≈ 666 ⇒ căn giữa left = (1920−666)/2 ≈ 627,
                #    trừ ~21 padding của preset ⇒ layout.x ≈ 606.
                #    Dọc: khoảng trống là 250 (đáy dải) → 860 (mép phụ đề); 3 dòng cỡ 76 cao
                #    ≈ 3×76×1,55 ≈ 353 ⇒ top = (250+860)/2 − 353/2 ≈ 380.
                "color": "#1C2A4A", "animation": "none",
                "layout": {"x": 606, "y": 380, "w": 1100}, "fontSize": 76,
            })

        if FX[i]:
            variant, dens = FX[i]
            # bên đặt hạt = bên ÍT BẬN của chính tấm ảnh đang chiếu (đo, không đoán)
            cur = trk_v[-1]["asset"].split("/")[-1] if trk_v else None
            side = quiet_side(os.path.join(ROOT, "public", "projects", NAME,
                                           "assets", cur)) if cur else "right"
            trk_fx.append({
                "id": f"fx{i}", "kind": "fx", "from": f(s0) + 6,
                "durationInFrames": max(12, f(dur) - 12),
                # 🔴 Hạt rải TOÀN KHUNG thì nó phủ lên MẶT người (frame 14s: xu vàng che
                #    má bà cụ). Prompt đã bắt chừa một phần ba khung trống — nhốt hạt vào
                #    đúng dải đó: vừa không che mặt, vừa dùng đúng chỗ được chừa.
                "variant": variant, "density": dens, "color": "#FFC83A",
                "seed": 100 + i * 7,
                # 🔴 Bên PHẢI-DƯỚI đã là chỗ của MASCOT (bottomOffset 250 + cao 300 ⇒ y≈530–830).
                #    Thả hạt kín cột phải là hạt rơi xuyên qua ông già — thấy ở frame 6s.
                #    ⇒ cột phải chỉ dùng NỬA TRÊN; cột trái mới được dùng trọn chiều cao.
                "area": ({"x": 2, "y": 8, "w": 32, "h": 84}
                         if side == "left" else {"x": 66, "y": 6, "w": 30, "h": 40}),
                "opacity": 1, "fadeInFrames": 8, "fadeOutFrames": 10, "dir": "upright",
            })

        # telop: khối đồ hoạ đã có bảng ở giữa ⇒ telop dùng dải trên, khỏi đè
        trk_t.append({
            "id": f"t{i}", "kind": "text", "from": f(s0) + 3,
            "durationInFrames": f(dur) - 5,
            "content": telop,
            "preset": "telop-band" if IMG[i] is None else PRESET[n % 3],
            "color": "#FFD34E", "animation": "pop", "layout": {}, "fontSize": None,
        })

    # phụ đề: cắt đúng cửa sổ demo rồi dời về gốc 0
    lines = json.load(io.open(TL, encoding="utf-8"))["lines"]
    cap = []
    for l in lines:
        if l["end"] <= t0 or l["start"] >= t1:
            continue
        parts = split_caption(l["text"])
        span = (l["end"] - l["start"]) / max(1, sum(len(p) for p in parts))
        t = l["start"]
        for p in parts:
            d = span * len(p)
            cap.append({"text": p, "startMs": round((t - t0) * 1000),
                        "endMs": round((t + d - t0) * 1000)})
            t += d
    bad = [c for c in cap if len(c["text"]) > 78]
    if bad:
        print(f"🔴 {len(bad)} khối phụ đề > 78 ký"); sys.exit(1)

    proj = {
        "version": 1,
        "meta": {"name": NAME, "channel": "nenkin", "templateRef": None,
                 "fps": FPS, "width": W, "height": H, "createdAt": "", "modifiedAt": ""},
        "timeline": {"durationInFrames": f(total)},
        "sceneMarkers": markers,
        "tracks": [
            {"id": "trk-video", "name": "footage", "type": "video", "clips": trk_v},
            {"id": "trk-fx", "name": "hoa la canh", "type": "fx", "clips": trk_fx},
            {"id": "trk-stat", "name": "bang so", "type": "text", "clips": trk_stat},
            {"id": "trk-telop", "name": "telop", "type": "text", "clips": trk_t},
            {"id": "trk-audio", "name": "voice", "type": "audio", "clips": [
                {"id": "a0", "kind": "audio", "from": 0, "durationInFrames": f(total),
                 "asset": "assets/voice.wav", "volume": 1,
                 "trimStartFrames": f(t0)}]},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44, "lines": cap, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236", "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#F3EAD8"},
        "brand": {
            "logo": "assets/brand_logo.png", "mascot": None, "mascotPoses": poses,
            "mascotVideo": poses[0]["asset"], "mascotVideoFrames": MASCOT_FRAMES,
            "mascotH": 300, "logoH": 110, "subscribe": True,
            # 🔴 ĐO ĐƯỢC trên still frame 420: ở 150 thì nút SUBSCRIBE chiếm y 879–1005 và
            #    dải phụ đề chiếm y 876–1009 ⇒ CHỒNG NHAU. Phải nâng lên trên mép phụ đề.
            "bottomOffset": 250,
        },
    }
    out = os.path.join(ROOT, "projects", NAME, "project.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(json.dumps(proj, ensure_ascii=False, indent=1))

    print(f"✅ {out}")
    print(f"   {len(idxs)} scene · {total:.1f}s @ {FPS}fps  (scene {idxs[0]}–{idxs[-1]} "
          f"của video thật, t={t0:.1f}→{t1:.1f}s)")
    print(f"   ảnh {len(trk_v)} · khối đồ hoạ font {len(trk_stat)} · fx {len(trk_fx)} · "
          f"phụ đề {len(cap)} khối")
    n_change = len(trk_v) + len(trk_stat)
    print(f"   nhịp: {n_change/(total/60):.1f} đổi hình/phút (trần 6) — đếm theo CLIP thật, không theo scene")
    print(f"   ⚠️ dùng lại ảnh ở scene {sorted(REUSED)} — thiếu ảnh, không giấu")


if __name__ == "__main__":
    main()
