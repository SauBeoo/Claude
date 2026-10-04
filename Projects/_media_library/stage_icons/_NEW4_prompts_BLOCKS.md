# 4 ĐỒ RỜI "CẢM XÚC" — bổ sung bộ 38 icon sân khấu (2026-08-24)

> Đúc từ frame user chỉ ra ở video đối thủ `シニアのお金相談所` (64:26). Frame đó chở **~14 vật**
> trên một khung; kho ta đã có gần hết **vật danh từ** (通知書 · 年金手帳 · máy tính · túi tiền ¥ ·
> xu · ví · phong bì…) nhưng **không có vật cảm xúc** nào — đó là 4 cái dưới đây.
>
> Prompt: `_NEW4_prompts_FLOW.txt` (mỗi prompt 1 dòng) · tên file: `_NEW4_prompts_TENFILE.txt`

## Bảng

| # | file | vật | dùng ở beat nào | vì sao cần |
|---|---|---|---|---|
| 1 | `money_fly.png` | tờ tiền **có cánh** đang bay, nghiêng 15°, có 2 vệt chuyển động | 引かれる · 損する · 取り逃す | kho chỉ có tiền **nằm yên** (`money_pouch`, `yen_coins`, `wallet_open`). Không có vật nào diễn được "tiền ĐANG mất đi" — mà đó là cảm xúc trung tâm của mọi bài nenkin |
| 2 | `burst.png` | bong bóng **nổ RỖNG**, 14 gai, trong trắng trơn, viền navy + 1 nét amber | dán cạnh hero để nhấn | demo2 dùng nó đóng khung chữ đòn 「絶対」. Ta gen **RỖNG, không chữ** — chữ Nhật gen hay nát nét, và tool đã có node `chip`/`label` vẽ chữ bằng font Noto nên luôn sắc |
| 3 | `sparkle.png` | chùm 3 tia 4 cánh, amber, viền navy | 戻ってくる · 還付 · 助かる | kho không có vật nào mang nghĩa TÍCH CỰC. Bài 16 nói về tiền **được hoàn lại** mà không có gì để reo |
| 4 | `arrow_red.png` | mũi tên **cong vẽ tay**, nét bút đỏ thô, đầu mũi tam giác đặc | 増える · 上がる · 急増 | kho có `chart_up`/`chart_down` (biểu đồ, lạnh) nhưng không có mũi tên **cảm xúc**. Cặp đối lập với `chart_down` |

## 🔴 ĐIỀU KIỆN SỐNG CỦA LÔ NÀY: VIỀN NAVY KHÉP KÍN

`ingest_stage_icons.py` tách nền bằng **flood-fill từ 4 mép** (không threshold toàn ảnh — đúng,
vì threshold sẽ khoét rỗng mọi vùng trắng bên trong vật). Hệ quả: **vùng trắng trong vật chỉ an
toàn khi nó bị viền navy khép kín ngăn khỏi nền trắng.** Hở một chỗ là nền "chảy" vào trong và
khoét mất ruột vật.

Ba trong bốn vật này có phần trắng (ruột bong bóng, thân tờ tiền, cánh) ⇒ prompt đã khoá bằng câu:
`every part of the object must be fully enclosed by a closed unbroken dark navy outline, so that
no white area inside the object touches the white background anywhere`.

⚠️ **Nghiệm thu phải soi đúng chỗ này**: sau khi ingest, mở PNG trên nền MÀU (không phải nền
trắng) và xem ruột bong bóng / thân tiền có bị trong suốt không. Trên nền trắng thì lỗi này **vô
hình** — cùng họ với bài học "dán cast lên đúng màu nền khung rồi mới soi".

## Quy trình

1. Bơm `_NEW4_prompts_FLOW.txt` vào extension → gen 4 ảnh.
2. Bỏ ảnh **THÔ** vào `stage_icons/_raw/` (đừng sửa gì, đừng cắt watermark tay — tool tự xoá blob ✦).
3. `python _media_library/ingest_stage_icons.py --check` xem chẩn đoán, rồi chạy thật.
4. Soi trên nền màu (mục ⚠️ trên) + soi 1:1 cả 4 góc tìm ✦ sót.
5. Dùng: thêm vào `props` của thẻ, ví dụ
   `{"icon": "money_fly", "at": [0.10, 0.64], "s": 165, "rot": -8}`.

## Ghi chú màu

`arrow_red` là **màu ĐỎ đầu tiên** trong bộ icon (38 cái hiện có chỉ navy/amber/beige/grey).
Đỏ hợp lệ vì `make_stage` đã có `RED = (214,40,40)` cho tone `bad`. Nhưng **dùng dè**: đỏ trong
bộ này là màu báo động, rải nhiều thì mất tác dụng nhấn.
