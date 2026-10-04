# -*- coding: utf-8 -*-
"""
build_remotion_22demo.py — DEMO khuôn nenkin video 22: telop + hoa lá cành + mascot.

12 clip Veo THẬT (user gen 2026-09-07) × 8s = 96s. Nội dung hình khớp lời ở mức beat,
không khớp từng câu — đây là bản duyệt STYLE.

🔴 fps = 24, KHÔNG phải 30. Clip Veo trả về 24fps; ép lên 30 thì 27% frame bị lặp và ra
   judder (`feedback_fps_clip_phai_khop_renderer`). Đặt cả project về 24 là sạch nhất vì
   không có nguồn 30fps nào khác trong bài.

🔴 CHỮ TRÊN GIẤY TRONG CLIP LÀ NÁT (0/6 clip có chữ đúng — đo 2026-09-07). Đây là kết quả
   đã dự báo của đường "để Veo tự viết chữ". Demo này che bằng cách đặt telop TO ở nửa
   trên, đúng chỗ mắt nhìn trước. Đường sửa thật cho bản chính thức, chọn một:
     ⓐ gen lại 6 clip đó với giấy TRƠN rồi Remotion dán chữ đè (chữ sắc tuyệt đối)
     ⓑ gen ẢNH TĨNH có chữ rồi hoạt hoá (`_media_library/animate_still.py`) — chữ đứng
       yên tuyệt đối, đổi lại người không cử động
"""
import io, json, os, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"E:\Claude\Projects\remotion-vox"
NAME = "nenkin-22demo"
FPS, W, H = 24, 1920, 1080
TL = r"E:\Claude\Projects\youtube-jp-nenkin\06_VIDEO\22_mishikyu-nenkin-36man\timeline.json"
SEC = 8.0                      # mỗi clip Veo đúng 8,000s
MASCOT_FRAMES = 192            # SỐ THẬT do mascot_chroma.py in ra (8s × 24fps)

f = lambda s: max(0, int(round(s * FPS)))

# GRADING để rất nhẹ: clip mới đã sáng sẵn nhờ prompt. Nhân mạnh nữa là cháy — user đã
# bắt đúng lỗi đó ở vòng trước (bản 1,32× làm vùng cửa sổ trắng bệt).
GRADE = {"brightness": 1.04, "contrast": 1.0, "saturate": 1.08}

# (clip, kiểu telop, chữ telop, fx, tư thế mascot)  ·  `{...}` = cụm được nhấn màu
SCENES = [
    ("c22_futatsu",   "telop",      "{同じ}36万円",     None,             "13"),
    ("c22_kichou",    "telop-band", "通帳では{同じ}",    None,             "13"),
    ("c22_katahou",   "telop-gold", "片方は\n{返金}",    ("rays", 22),     "15"),
    ("c22_shibou",    "telop",      "{死亡日}で決まる",  None,             "13"),
    # 🔴 Hai scene CẢNH BÁO bỏ hẳn glow của Veo (nó tô đỏ thẳng lên da tay — clip task_005).
    #    Quầng đỏ ở RÌA + dấu ✗ đập xuống do Remotion vẽ đè: kiểm soát được, không chạm người.
    # ⚠️ `vignette` đang TẮT ở hai scene này, và đây là trạng thái TẠM.
    #    Clip task_005/008 hiện tại đã bị Veo tô đỏ sẵn (tay bà cụ, tờ giấy ông) ⇒ chồng
    #    thêm quầng đỏ là đỏ-chồng-đỏ, tệ hơn cả bản chưa sửa. Soi still frame 800/1400.
    #    ⇒ BẬT LẠI ngay khi thay xong 2 clip bằng bản gen từ `flow22_REDO.txt` (khuôn ALARM
    #      mới, không glow). Giữ `stampx` vì nó không cộng thêm đỏ vào nền.
    ("c22_kigen",     "telop-gold", "五年で\n{消える}",
     [("stampx", 1, {"x": 4, "y": 18, "w": 44, "h": 60})], "14"),
    ("c22_mishikyu",  "telop-band", "{未支給}年金",      None,             "15"),
    ("c22_dare",      "telop",      "請求できる{人}",    None,             "13"),
    ("c22_gonen",     "telop-gold", "期限は\n{五年}",    None,  "14"),  # vignette TẮT tạm — xem ghi chú ở c22_kigen
    ("c22_kakunin",   "telop",      "まず{通帳}を",      ("coins", 14),    "13"),
    ("c22_madoguchi", "telop-band", "{年金事務所}へ",    None,             "14"),
    ("c22_futsuu",    "telop",      "二つは{並ぶ}",      ("sparkle", 12),  "13"),
    ("c22_owari",     "telop-gold", "取り戻せる",        ("confetti", 16), "15"),
]

FADE = 7  # frame cross-dissolve (~0,3s @24fps)


def split_caption(text, maxlen=78):
    """Chẻ khối phụ đề ≤78 ký, cắt SAU dấu câu.

    🔴 Remotion KHÔNG chẻ hộ như `video_render.py` (SUB_MAXLEN=42): CaptionLayer lấy
    NGUYÊN dòng timeline làm một khối ⇒ dòng dài ra 4 dòng phụ đề che gần hết đáy khung,
    vi phạm `audience-45plus.md` §3 (≤2 dòng/khối).
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
    total = len(SCENES) * SEC
    lines = [l for l in json.load(io.open(TL, encoding="utf-8"))["lines"] if l["start"] < total]

    trk_v, trk_fx, trk_t, markers, poses = [], [], [], [], []

    for i, (clip, preset, telop, fx, pose) in enumerate(SCENES):
        s0 = i * SEC
        ext = FADE if i < len(SCENES) - 1 else 0
        trk_v.append({
            "id": f"v{i}", "kind": "video", "from": f(s0),
            "durationInFrames": f(SEC) + ext,
            "asset": f"assets/{clip}.mp4", "fit": "cover", "motion": "none",
            "speed": 1.0, "volume": 0, "filter": GRADE,
            # xen kẽ lật trang / dissolve cho chuyển cảnh khỏi đơn điệu
            **({"curlInFrames": 13, "curlDir": ["br", "tr", "bl", "tl"][i % 4]}
               if i % 2 == 1 else {"fadeInFrames": FADE if i else 0}),
        })
        markers.append({"id": f"m{i}", "atFrame": f(s0), "label": telop.replace("\n", " ")})
        poses.append({"atSec": s0, "asset": f"assets/ojii_{pose}/f_%04d.png"})

        # fx nhận MỘT tuple hoặc DANH SÁCH tuple — scene cảnh báo cần 2 lớp chồng nhau
        # (quầng đỏ ở rìa + dấu ✗ đập xuống), scene thường chỉ 1.
        fxs = [] if not fx else (fx if isinstance(fx, list) else [(*fx, None)])
        for j, item in enumerate(fxs):
            variant, dens, area = (item if len(item) == 3 else (*item, None))
            warn = variant in ("vignette", "stampx")
            trk_fx.append({
                "id": f"fx{i}_{j}", "kind": "fx",
                # dấu ✗ vào MUỘN hơn (giữa scene) để nó đóng vai "chốt hạ", không phải nền
                "from": f(s0) + (f(SEC) // 2 if variant == "stampx" else 6),
                "durationInFrames": (f(SEC) // 2 - 6) if variant == "stampx" else f(SEC) - 12,
                "variant": variant, "density": dens,
                # 🔴 BỎ ĐỎ (user chốt 2026-09-07: "màu đỏ đấy trong video không hợp hoàn
                #    cảnh"). Đỏ là ngôn ngữ NGUY HIỂM/CẤM, nhưng bài này nói về **tiền mà
                #    người xem ĐƯỢC NHẬN** — tin tốt bị bỏ sót, không phải mối nguy. Đỏ gắt
                #    còn chọi hẳn với tông kem–navy–vàng của kênh và với ánh sáng ấm của
                #    footage, nên nhìn ra "lắp vào" chứ không ra "thuộc về khung hình".
                # ⇒ Cảnh báo dùng **hổ phách đậm** (cùng họ với vàng của kênh, vẫn đủ
                #   nghiêm) và dấu ✗ dùng **navy** — cả hai đã có trong palette kênh.
                "color": ("#1C2A4A" if variant == "stampx"
                          else "#C8791E" if warn else "#FFC83A"),
                "seed": 100 + i * 7 + j,
                "area": area or {"x": 0, "y": 0, "w": 100, "h": 100},
                "opacity": 0.9 if variant == "vignette" else 1,
                "fadeInFrames": 8, "fadeOutFrames": 10, "dir": "upright",
            })

        trk_t.append({
            "id": f"t{i}", "kind": "text", "from": f(s0) + 3,
            "durationInFrames": f(SEC) - 5,
            "content": telop, "preset": preset, "color": "#FFD34E",
            "animation": "pop", "layout": {}, "fontSize": None,
        })

    cap = []
    for l in lines:
        parts = split_caption(l["text"])
        span = (l["end"] - l["start"]) / max(1, sum(len(p) for p in parts))
        t = l["start"]
        for p in parts:
            d = span * len(p)
            cap.append({"text": p, "startMs": round(t * 1000), "endMs": round((t + d) * 1000)})
            t += d
    cap = [c for c in cap if c["startMs"] < total * 1000]

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
            {"id": "trk-telop", "name": "telop", "type": "text", "clips": trk_t},
            {"id": "trk-audio", "name": "voice", "type": "audio", "clips": [
                {"id": "a0", "kind": "audio", "from": 0, "durationInFrames": f(total),
                 "asset": "assets/voice.wav", "volume": 1}]},
        ],
        "captions": {"source": "srt-interpolated", "style": "outline", "enabled": True,
                     "fontSize": 44, "lines": cap, "words": []},
        "theme": {"palette": {"bgTop": "#2A3A58", "bgBottom": "#182236", "accent": "#FFD700"},
                  "fontFamily": '"Yu Gothic", "Meiryo", Arial Black, sans-serif',
                  "canvasColor": "#101010"},
        "brand": {
            "logo": "assets/brand_logo.png",
            "mascot": None,
            "mascotPoses": poses,
            "mascotVideo": poses[0]["asset"],
            "mascotVideoFrames": MASCOT_FRAMES,
            "mascotH": 300, "logoH": 110,
            "subscribe": True,
            # 🔴 Nâng khỏi dải phụ đề (~110px ở đáy) VÀ khỏi góc timestamp của YouTube.
            "bottomOffset": 150,
        },
    }

    out = os.path.join(ROOT, "projects", NAME, "project.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(proj, ensure_ascii=False, indent=1))
    print(f"✅ {out}")
    print(f"   {len(SCENES)} scene × {SEC}s = {total:.0f}s @ {FPS}fps · "
          f"{len(trk_fx)} lớp fx · {len(cap)} khối phụ đề")
    print(f"   nhịp: {len(SCENES)/(total/60):.1f} đổi hình/phút (trần 6)")


if __name__ == "__main__":
    main()
