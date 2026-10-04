# -*- coding: utf-8 -*-
r"""ingest_stage_icons.py — biến ảnh AI THÔ thành ICON dùng được cho `make_stage.py`.

VÀO:  `stage_icons/_raw/*.png|jpg`  (ảnh vừa gen, CHƯA sửa gì)
RA:   `stage_icons/<tên>.png` — 512×512, RGBA nền TRONG SUỐT, đã cắt watermark ✦

BA VIỆC TOOL LÀM:

① **TÁCH NỀN TRẮNG → ALPHA.** Icon phải trong suốt: `circle`/`oval` của layout `zu` tô nền màu
   rồi dán icon lên, nền trắng đục sẽ thành một ô vuông trắng giữa vòng tròn xanh nhạt.
   Cách tách: pixel gần trắng **VÀ nối liền với biên ảnh** (flood-fill từ 4 mép) → trong suốt.
   🔴 KHÔNG threshold toàn ảnh: làm thế thì mọi vùng trắng BÊN TRONG vật (giấy, mặt đồng hồ,
   ô kẻ của sổ) cũng bị khoét rỗng — lỗi kinh điển khi tách nền icon line-art.

② **XOÁ BLOB ✦, KHÔNG CẮT KHUNG.**
   🔴🔴 BẢN ĐẦU LÀM SAI VÀ USER BẮT ĐƯỢC (2026-08-17): nó "cắt 12% mép phải + đáy để bỏ ✦" rồi
   "crop vuông ở giữa". **Cả hai bước đều giả định vật nằm GIỮA khung** — mà model đặt vật lệch
   TRÊN-TRÁI. Đo lại trên 4 icon bị hỏng: vật của `couple_senior` chạy tới x=1046 và y=690, còn
   hai bước cắt kia chỉ giữ x 267..942 và y 0..675 ⇒ **mất vai bà + chân bàn + đáy ví + mép sổ**.
   ⇒ Nay: KHÔNG cắt khung. Sau khi tách nền, ✦ là một **đảo rời** trên nền trong suốt → tìm các
   thành phần liên thông rồi **xoá thành phần nhỏ nằm ở góc phải/đáy**. Vật giữ nguyên 100%.
   ⚠️ Chỉ xoá blob **nhỏ hơn 1,5% thành phần lớn nhất VÀ tâm nằm ngoài 78% khung** — icon nhiều
   mảnh rời hợp lệ (2 người + bàn, đồng xu + cọc) không bị mất mảnh nào.

③ **Trim sát vật → pad thành VUÔNG.** `icon()` của make_stage resize về ô vuông, nên phải pad
   cân hai chiều (không crop!) rồi mới resize — pad thì vật không bao giờ bị bóp méo hay mất mép.

CHẠY:  python ingest_stage_icons.py            # xử lý hết _raw/, tên file = tên ảnh nguồn
       python ingest_stage_icons.py --check     # chỉ in chẩn đoán, không ghi
"""
import sys
from collections import deque
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
RAW = HERE / "stage_icons" / "_raw"
OUT = HERE / "stage_icons"
SIZE = 512
NEAR_WHITE = 232             # min(r,g,b) ≥ ngưỡng ⇒ coi là nền (đo trên icon hiện có)
PAD = 0.06
BLOB_MAX = 0.015             # blob ≤1,5% thành phần lớn nhất mới được coi là rác
BLOB_ZONE = 0.78             # ... VÀ tâm phải nằm ngoài 78% khung (tức góc phải/đáy)


def strip_bg(im):
    """Nền trắng NỐI LIỀN VỚI BIÊN → alpha 0. Vùng trắng bên trong vật thì GIỮ."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    q = deque()

    def push(x, y):
        i = y * w + x
        if not seen[i]:
            r, g, b, _ = px[x, y]
            if min(r, g, b) >= NEAR_WHITE:
                seen[i] = 1
                q.append((x, y))

    for x in range(w):
        push(x, 0); push(x, h - 1)
    for y in range(h):
        push(0, y); push(w - 1, y)
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                push(nx, ny)
    for y in range(h):
        for x in range(w):
            if seen[y * w + x]:
                r, g, b, _ = px[x, y]
                px[x, y] = (r, g, b, 0)
    return im


def drop_blobs(im):
    """Xoá các ĐẢO nhỏ ở góc phải/đáy = watermark ✦. → (ảnh, số blob đã xoá).

    Chạy SAU `strip_bg`, nên nền đã trong suốt và ✦ (màu kem, không đủ trắng để bị flood-fill)
    còn lại như một thành phần liên thông rời. Giữ mọi mảnh hợp lệ của vật, chỉ bỏ rác."""
    w, h = im.size
    a = im.getchannel("A").load()
    lab = [0] * (w * h)
    comps = []
    for sy in range(h):
        for sx in range(w):
            if a[sx, sy] <= 8 or lab[sy * w + sx]:
                continue
            cid = len(comps) + 1
            lab[sy * w + sx] = cid
            q, cells = deque([(sx, sy)]), []
            while q:
                x, y = q.popleft()
                cells.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not lab[ny * w + nx]                             and a[nx, ny] > 8:
                        lab[ny * w + nx] = cid
                        q.append((nx, ny))
            comps.append(cells)
    if not comps:
        return im, 0
    big = max(len(c) for c in comps)
    px = im.load()
    killed = 0
    for cells in comps:
        if len(cells) > big * BLOB_MAX:
            continue
        cx = sum(x for x, _ in cells) / len(cells) / w
        cy = sum(y for _, y in cells) / len(cells) / h
        if cx < BLOB_ZONE and cy < BLOB_ZONE:
            continue                     # blob nhỏ nhưng nằm trong vật → mảnh hợp lệ, GIỮ
        for x, y in cells:
            r, g, b, _ = px[x, y]
            px[x, y] = (r, g, b, 0)
        killed += 1
    return im, killed


def run(check=False):
    RAW.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in RAW.iterdir()
                   if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
    if not files:
        print(f"🔴 {RAW} RỖNG — bỏ ảnh thô vào đó rồi chạy lại.")
        print("   Prompt: stage_icons/_NEW10_prompts_FLOW.txt · tên file: _NEW10_prompts_TENFILE.txt")
        return
    for p in files:
        im = Image.open(p).convert("RGB")
        # ① tách nền (KHÔNG cắt khung — xem chú thích ② ở docstring)
        im = strip_bg(im)
        # ② xoá blob ✦
        im, killed = drop_blobs(im)
        # ③ trim sát vật rồi pad thành VUÔNG
        bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb is None:
            print(f"  🔴 {p.name}: KHÔNG tìm được vật (ảnh gần như trắng hết?) — bỏ qua")
            continue
        obj = im.crop(bb)
        side = int(max(obj.size) * (1 + PAD * 2))
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.alpha_composite(obj, ((side - obj.width) // 2, (side - obj.height) // 2))
        icon = canvas.resize((SIZE, SIZE), Image.LANCZOS)
        cov = sum(1 for a in icon.getchannel("A").tobytes() if a > 8) / (SIZE * SIZE)
        note = ""
        if cov < 0.10:
            note = "  ⚠️ vật chiếm <10% khung — nhìn 132px sẽ bé, cân nhắc gen lại"
        elif cov > 0.92:
            note = "  ⚠️ nền có thể CHƯA tách được (phủ >92%) — soi lại bằng mắt"
        print(f"  {'[check] ' if check else '✓ '}{p.stem + '.png':22s} phủ {cov:5.1%}"
              f"{f'  (xoá {killed} blob ✦)' if killed else ''}{note}")
        if not check:
            icon.save(OUT / f"{p.stem}.png")
    if not check:
        # sheet duyệt mắt: nền KẺ Ô để thấy ngay chỗ nào còn nền trắng đục
        names = [p.stem for p in files]
        cols, cell = 5, 200
        rows = (len(names) + cols - 1) // cols
        sh = Image.new("RGB", (cols * cell, rows * cell), (255, 255, 255))
        d = Image.new("RGB", (cell, cell), (222, 226, 233))
        for k in range(0, cell, 20):
            for j in range(0, cell, 20):
                if (k // 20 + j // 20) % 2 == 0:
                    d.paste(Image.new("RGB", (20, 20), (255, 255, 255)), (k, j))
        for i, n in enumerate(names):
            f = OUT / f"{n}.png"
            if not f.exists():
                continue
            base = d.copy()
            base.paste(Image.open(f).resize((176, 176), Image.LANCZOS).convert("RGBA"),
                       (12, 12), Image.open(f).resize((176, 176), Image.LANCZOS))
            sh.paste(base, ((i % cols) * cell, (i // cols) * cell))
        sh.save(OUT / "_new_sheet.jpg", quality=93)
        print(f"  ✓ _new_sheet.jpg — DUYỆT MẮT (nền kẻ ô: chỗ nào còn trắng đục là chưa tách xong)")


if __name__ == "__main__":
    run("--check" in sys.argv)
