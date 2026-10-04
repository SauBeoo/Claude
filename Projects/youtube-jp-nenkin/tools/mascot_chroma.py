# -*- coding: utf-8 -*-
"""
mascot_chroma.py — tách nền xanh khỏi clip mascot, xuất **PNG SEQUENCE có alpha**.

⚠️ Docstring cũ nói "xuất WebM VP9" và "DESPILL LÀ BẮT BUỘC" — **cả hai đã sai**, sửa
   2026-09-10. Giữ lý do trong hàm `key_out()` để không ai bật lại:
     · WebM alpha: build ffmpeg trên máy này vứt kênh alpha, IM LẶNG (xem key_out).
     · despill: nó bóc kênh green khỏi MỌI pixel nên **màu ẤM thành HỒNG** — cú nâu-kem
       ra cú hồng phấn mà mọi phép đo vẫn báo "0 px ngả xanh".
   📌 Bài học nằm ngoài đồ hoạ: **tài liệu chỏi code thì tin CODE, và sửa tài liệu ngay** —
      cùng bệnh `ab-3title-3thumb.md` §3.1 Bước 1 (tin ẢNH đã lên sóng, không tin tài liệu).

Chọn filter theo NỀN, không theo thói quen:
    nền xanh ĐỀU        → `colorkey` (RGB), sim ~0.30
    nền xanh KHÔNG ĐỀU  → **`--yuv`** (`chromakey`, so trong UV, bỏ qua độ sáng), sim 0.08–0.14
`probe_bg()` in ra "lệch giữa 4 góc"; >18 là không đều ⇒ dùng `--yuv`.

Dùng:
    python tools/mascot_chroma.py --probe in.mp4               # đo màu nền thật
    python tools/mascot_chroma.py in.mp4 outdir --yuv --sim 0.12 --blend 0.03
    # tuỳ chọn: --despill 0.6 (CHỈ nhân vật màu lạnh) · --erode 1 (co alpha 1px)
"""
import argparse, json, os, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def probe_bg(src):
    """Đo màu nền thật ở 4 góc frame đầu.

    🔴 ĐỪNG đoán màu key. Veo không trả đúng #00B140 mà ra một sắc xanh lệch tuỳ
       ánh sáng nó tự thêm; lấy hằng số thì key chừa lại vành xanh nhạt quanh vật.
    """
    from PIL import Image
    import tempfile
    tmp = os.path.join(tempfile.gettempdir(), "_mascot_probe.png")
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-frames:v", "1", tmp, "-y"], check=True)
    im = Image.open(tmp).convert("RGB")
    w, h = im.size
    pts = [(6, 6), (w - 7, 6), (6, h - 7), (w - 7, h - 7)]
    cols = [im.getpixel(p) for p in pts]
    avg = tuple(sum(c[i] for c in cols) // len(cols) for i in range(3))
    spread = max(max(c[i] for c in cols) - min(c[i] for c in cols) for i in range(3))
    print(f"  4 góc: {cols}")
    print(f"  trung bình: RGB{avg} -> key 0x{avg[0]:02X}{avg[1]:02X}{avg[2]:02X}")
    print(f"  lệch giữa 4 góc: {spread}" +
          ("  ⚠️ >18 = nền KHÔNG đều, key sẽ để lại mảng" if spread > 18 else "  ✓ nền đều"))
    return "0x%02X%02X%02X" % avg


def key_out(src, outdir, key, sim, blend, height=460, despill=0.0, erode=0,
            yuv=False):
    """Tách nền xanh -> **PNG SEQUENCE có alpha** (không phải WebM).

    🔴 VÌ SAO KHÔNG DÙNG WEBM ALPHA: build ffmpeg trên máy này liệt kê `yuva420p` trong
       "Supported pixel formats" của cả libvpx-vp9 lẫn libvpx, nhưng xuất ra vẫn là
       **yuv420p** — alpha bị vứt, IM LẶNG, exit 0. Đã thử đủ: `-pix_fmt yuva420p` ·
       `-auto-alt-ref 0` · bỏ despill · hạ về VP8. Trích frame rgba ra đo thì alpha
       min=max=255 ⇒ mất thật, không phải ffprobe báo nhầm.
    ⇒ PNG sequence là đường không thể hỏng: mỗi frame là một file RGBA riêng.
       Giá phải trả: nhiều file. Bù bằng cách hạ chiều cao về đúng cỡ dùng thật
       (mascot chỉ cao ~460px trên khung 1080) ⇒ mỗi PNG ~40-60KB.

    ⚠️ Bài học đo lường, ghi vì tao đã đổ lỗi nhầm hai lần trong một lượt:
       lần 1 gate báo đỏ -> tao nghi phép đếm (SAI, phép đếm đúng);
       lần 2 tao nghi ffprobe báo nhầm (SAI, alpha mất thật).
       Thứ tự đúng: **kiểm cái RẺ NHẤT và CHẮC NHẤT trước** — trích một frame rgba ra
       đo alpha. Ba phút đó lẽ ra cắt được cả hai vòng đoán mò.
    """
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith(".png"):
            os.remove(os.path.join(outdir, f))
    # 🔴🔴 `despill` PHÁ MÀU NÂU — bắt được 2026-09-10 ở lô mascot CÚ.
    #    Nâu/kem = R cao, G trung, B thấp. `despill=type=green` bóc kênh green ra khỏi
    #    MỌI pixel (không chỉ pixel viền), nên nâu mất G thành **HỒNG**: cú nâu-kem gốc
    #    ra một con cú hồng phấn, và nó vẫn "sạch" theo mọi phép đo (0 px ngả xanh) —
    #    đúng loại lỗi mà số đo không thấy, chỉ mắt thấy.
    #    ⇒ Mặc định `despill = 0` (tắt). Viền xanh mỏng thì chữa bằng `--erode`, đừng
    #      chữa bằng cách bóp màu toàn nhân vật.
    #    ⚠️ Lô nào có nhân vật màu LẠNH (xám/xanh/trắng) thì bật lại `--despill 0.6` được;
    #      nhân vật màu ẤM thì đừng bao giờ.
    # 🔴🔴 `colorkey` (RGB) KHOÉT MẤT PHẦN TỐI CỦA NHÂN VẬT khi nền xanh không đều.
    #    Đo trên lô cú (nền lệch 85 giữa 4 góc — xanh đậm ở trên, xanh sáng ở dưới):
    #      colorkey sim0.30 → **48% diện tích trong hình là LỖ** (mất lông nâu đậm + nơ navy)
    #      colorkey sim0.12 → 64% lỗ, và góc khung còn alpha 70 (nền chưa sạch)
    #      chromakey sim0.12 → **7,8% lỗ** (chỉ là khe giữa hai chân/chỏm tai), 3 px xanh sót
    #    ⇒ `chromakey` so trong **không gian UV**, bỏ qua ĐỘ SÁNG — đúng thứ cần khi nền
    #      xanh bị dải sáng-tối. `colorkey` so trong RGB nên độ sáng trộn vào khoảng cách.
    #    ⚠️ Nhưng `chromakey` có CỬA SỔ HẸP: quét sim 0,08→0,18 thấy cao nguyên ổn định ở
    #      **0,08–0,14** (6–10% lỗ) rồi **SỤP** ở 0,16 (38%) và 0,18 (79%). Đừng nới sim
    #      cho "sạch nền hơn" — nó ăn luôn nhân vật.
    kf = "chromakey" if yuv else "colorkey"
    parts = [f"{kf}={key}:{sim}:{blend}"]
    if despill > 0:
        parts.append(f"despill=type=green:mix={despill}:expand=0.4")
    parts.append("format=rgba")
    vf = ",".join(parts)
    print(f"  filter: {vf}")
    subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", vf,
                    os.path.join(outdir, "raw_%04d.png"), "-y"], check=True)

    # ── CROP về BBOX của nhân vật ────────────────────────────────────────────
    # 🔴 Không crop thì mỗi PNG vẫn là cả khung 1920x1080 mà nhân vật chỉ chiếm phần
    #    giữa. Đặt `mascotH: 300` khi đó cho ra thân mascot chỉ ~180px và trông như bị
    #    cắt ngang bụng — đã dính ở lượt still đầu của demo 22.
    # 🔴 BBOX phải là HỢP của MỌI frame, không phải bbox từng frame: crop riêng từng
    #    frame thì nhân vật NHẢY vị trí mỗi frame vì khung tham chiếu đổi liên tục.
    from PIL import Image
    import numpy as np
    raws = sorted(f for f in os.listdir(outdir) if f.startswith("raw_"))
    if not raws:
        print("  🔴 không xuất được frame nào"); sys.exit(1)
    # 🔴 LỌC BLOB LỚN NHẤT trước khi đo bbox. Ngưỡng màu KHÔNG loại được các đốm đục
    #    rải rác (mép khung, vệt sáng, logo "Veo" generator đóng ở góc) ⇒ bbox phình ra
    #    gần hết khung (đo thật: 1288x1033 trên khung 1920x1080) và mascot co lại tí xíu.
    #    Cùng bài học với `cutout_sticker.py` ③: lọc theo màu xong PHẢI lấy lại blob lớn nhất.
    import cv2
    x0 = y0 = 10 ** 9; x1 = y1 = -1
    for fn in raws:
        al = np.array(Image.open(os.path.join(outdir, fn)))[:, :, 3]
        m = (al > 128).astype(np.uint8)
        nlab, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
        if nlab > 1:
            ar = st[1:, cv2.CC_STAT_AREA]
            # 🔴 "GIỮ BLOB LỚN NHẤT" LÀ SAI Ở ĐÂY và cắt cụt nhân vật. Đo thật frame 96
            #    của ojii_13: mask chẻ làm 93 blob, trong đó HAI blob là người —
            #    đầu+vai 223.503px (y 28-560) và thân dưới 90.873px (y 558-873) —
            #    dính nhau qua một cổ áo mảnh bị key đứt. Giữ một blob ⇒ mất nửa dưới,
            #    và vết cắt PHẲNG NGANG nên nhìn như crop chứ không như lỗi tách nền.
            # ⇒ Giữ MỌI blob ≥5% blob lớn nhất: đủ để gom các mảnh của người, vẫn loại
            #    sạch nhiễu (nhiễu lớn nhất ở đây 335px = 0,15%).
            keep = {i + 1 for i, v in enumerate(ar) if v >= 0.05 * ar.max()}
            al = np.where(np.isin(lab, list(keep)), al, 0)
        # 🔴 Ngưỡng phải ĐỦ CAO. Ở `al > 24` bbox bắt cả vệt spill mờ quanh mép ⇒ hộp
        #    rộng hơn thân thật (đo: 573x460 cho một nhân vật cao gầy) ⇒ khi đặt
        #    `mascotH` thì thân co lại vừa cái hộp thừa và trông nhỏ tí.
        ys, xs = np.where(al > 128)
        if len(xs) == 0:
            continue
        x0 = min(x0, xs.min()); x1 = max(x1, xs.max())
        y0 = min(y0, ys.min()); y1 = max(y1, ys.max())
    if x1 < 0:
        print("  🔴 mọi frame đều trong suốt — key ăn mất nhân vật"); sys.exit(1)
    pad = 6
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    for i, fn in enumerate(raws, 1):
        im = Image.open(os.path.join(outdir, fn))
        im = im.crop((x0, y0, min(im.width, x1 + pad + 1), min(im.height, y1 + pad + 1)))
        # ⭐ `--erode`: co alpha N px — cách chữa viền xanh mỏng mà KHÔNG bóp màu nhân vật.
        #    Đây là thứ thay cho `despill` (xem ghi chú đầu hàm): despill sửa ở tầng MÀU nên
        #    nó chạm vào mọi pixel; erode sửa ở tầng HÌNH HỌC nên chỉ mất N px ngoài cùng —
        #    mà N px ngoài cùng đúng là chỗ bị nhiễm.
        if erode > 0:
            arr = np.array(im.convert("RGBA"))
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode + 1, 2 * erode + 1))
            arr[:, :, 3] = cv2.erode(arr[:, :, 3], k, iterations=1)
            im = Image.fromarray(arr)
        w = max(1, round(im.width * height / im.height))
        im.resize((w, height), Image.LANCZOS).save(os.path.join(outdir, f"f_{i:04d}.png"))
        os.remove(os.path.join(outdir, fn))
    print(f"  bbox hợp: {x1-x0+1}x{y1-y0+1} -> cao {height}px")

    pngs = sorted(f for f in os.listdir(outdir) if f.startswith("f_"))
    a = np.array(Image.open(os.path.join(outdir, pngs[len(pngs) // 2])).convert("RGBA"))
    al = a[:, :, 3]
    opq = (al > 250).mean() * 100
    # viền xanh sót: pixel ĐỤC mà ngả lục. Đo pixel bán trong suốt là SAI — alpha ở đây
    # gần nhị phân (cùng bài học với viền tím ở cutout_sticker.py).
    m = (al > 250)
    spill = int(((a[:, :, 1].astype(int) - a[:, :, 0]) > 34)[m].sum() and
                (((a[:, :, 1].astype(int) - a[:, :, 0]) > 34) &
                 ((a[:, :, 1].astype(int) - a[:, :, 2]) > 34) & m).sum())
    print(f"  {len(pngs)} frame · đục {opq:.1f}% · viền xanh sót {spill} px")
    if opq > 85:
        print("  🔴 key trượt — chạy --probe"); sys.exit(1)
    if opq < 3:
        print("  🔴 key ăn mất cả nhân vật — hạ --sim"); sys.exit(1)
    if spill > 400:
        print("  ⚠️ còn viền xanh — tăng despill mix")
    else:
        print("  ✓ số đo ổn — VẪN PHẢI soi 1:1 (số đo không chứng minh sạch)")
    return len(pngs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--key", default=None)
    ap.add_argument("--sim", type=float, default=0.30)
    ap.add_argument("--blend", type=float, default=0.10)
    ap.add_argument("--height", type=int, default=460)
    ap.add_argument("--yuv", action="store_true",
                    help="dung chromakey (khong gian UV) thay colorkey — BAT khi "
                         "nen xanh khong deu. Cua so sim hep: 0.08-0.14")
    ap.add_argument("--despill", type=float, default=0.0,
                    help="0 = TAT (mac dinh). Chi bat khi nhan vat mau LANH — "
                         "xem ghi chu trong key_out()")
    ap.add_argument("--erode", type=int, default=0,
                    help="co alpha N px — chua vien xanh mong mà KHONG bop mau")
    ap.add_argument("--probe", action="store_true")
    a = ap.parse_args()

    print(f"── {os.path.basename(a.src)}")
    key = a.key or probe_bg(a.src)
    if a.probe:
        return
    if not a.dst:
        a.dst = os.path.splitext(a.src)[0] + "_seq"
    n = key_out(a.src, a.dst, key, a.sim, a.blend, a.height, a.despill, a.erode,
                a.yuv)
    print(f"  → {a.dst}/f_%04d.png")
    print(f"  ⭐ mascotVideoFrames = {n}  (SỐ FRAME THẬT — đừng đoán, đoán ngắn thì clip "
          f"bị cắt giữa động tác, đoán dài thì nó đứng hình chờ hết vòng)")


if __name__ == "__main__":
    main()
