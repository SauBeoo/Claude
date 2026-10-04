# stage_icons — KHO ICON DÙNG CHUNG cho lớp sân khấu (`make_stage.py`)

> Chốt **2026-08-17**, user: *"những ảnh nào tái sử dụng được thì bỏ ra khu vực dùng chung để
> tái sử dụng cho video sau nhé"*.

## Cách tool tìm icon (thứ tự)

`make_stage.py::icon_path()` tìm theo **ICON_DIRS**:

1. `<project>/assets/icons/<name>.png` — **riêng kênh**, GHI ĐÈ được
2. `_media_library/stage_icons/<name>.png` — **dùng chung mọi kênh** ← folder này

Kênh nào muốn icon riêng cho một tên thì bỏ file cùng tên vào `assets/icons/` của nó là thắng.

## ⚖️ RANH GIỚI — cái gì được vào kho này, cái gì KHÔNG

Đây **KHÔNG** phá `.claude/rules/media-library.md` §2 (*"KHÔNG TÁI DÙNG ASSET — làm video nào
tải ảnh của video đó thôi"*). Rule đó nói về **b-roll STOCK tải từ mạng**: lặp cảnh thật giữa
các video rơi vào "inauthentic content". Icon khái niệm thì **ngược lại** — nó là **bộ nhận
diện**, lặp lại là điều TỐT (lướt 1 giây biết kênh nào).

| ✅ VÀO kho chung | ⛔ Ở LẠI folder video |
|---|---|
| Vật trung tính, **không số, không chữ, không gắn năm**: ví, phong bì, đồng hồ, lịch, toà thị chính, cân, sổ ngân hàng | **原典ショット** — gắn chặt trang tài liệu + 年度 (`genten_*`), năm sau là số khác |
| Icon vector/PNG khái niệm dùng lại được ở mọi bài | Ảnh **cảnh thật** / b-roll (rule §2 cấm tái dùng) |
| Dấu ○×, khiên, mũi tên | Ảnh chứa **con số của đúng bài đó** |
| — | **`avatar_*`** — dàn モニター là nhân vật RIÊNG của từng kênh |

## Nội dung hiện có (28 icon, copy từ `youtube-jp-nenkin/assets/icons` 2026-08-17)

`bank · calc · calendar · cashcard · chart_down · chart_up · checklist · cityhall · clock ·
couple · docs · env · form · hanko · hospital · house · lock · magnifier · mailbox ·
money_pouch · nenkin_techo · passbook · person · phone · postcard · scale · wallet · warning`

⚠️ **Hiện có 2 bản** (nenkin/assets/icons và đây) — bản của nenkin thắng theo thứ tự tìm, nên
hành vi của video cũ **không đổi**. Muốn gọn thì xoá bản trong `nenkin/assets/icons` (trừ
`avatar_*`) — **chờ user cho phép**, luật gốc: không tự xoá file.

⚠️ `warning.orig` (bản còn watermark ✦ của Gemini) **không** được copy sang đây.

## ✅ 10 icon đạo cụ mới — ĐÃ CÓ (2026-08-17)

**Vì sao gen:** đo trên video 13 — icon hiện có **không thiếu cái nào** (30/30 có PNG thật), nhưng
bị **dùng lặp nhiều** (`person` ×10 · `couple` ×9 · `money_pouch` ×9 · `calendar` ×7 trong 16 phút)
và **thô hơn đạo cụ của kênh đối thủ**: họ dùng đồng hồ CÁT / ví MỞ có tiền lòi / quầy 窓口 có vách
kính, mình thay bằng `clock` tròn / `wallet` gập kín / `cityhall` khối nhà.

| # | file | thay cho | dùng ở beat |
|---|---|---|---|
| 1 | `hourglass.png` | `clock` | 期限・時効 |
| 2 | `wallet_open.png` | `wallet` | 立て替える・現金が要る |
| 3 | `receipt.png` | — (mới) | 領収書・請求 |
| 4 | `madoguchi.png` | `cityhall` | 窓口へ行く |
| 5 | `envelope_open.png` | `env` | 通知書が届く |
| 6 | `passbook_open.png` | `passbook` | ⭐ trục hình "số vào sổ" |
| 7 | `couple_senior.png` | `couple` | ご夫婦の場面 |
| 8 | `yen_coins.png` | — (mới) | nhấn TIỀN |
| 9 | `shield_check.png` | ghép `mark` | có quyền / có bảo hiểm |
| 10 | `shield_dash.png` | ghép `mark` | mất quyền / không có |

✅ **Đã gen + xử lý xong cả 10.** Phủ mực sau khi tách nền: `madoguchi` 72,7% · `envelope_open`
66,6% · `wallet_open` 66,0% · `yen_coins` 61,8% · `shield_check` 57,6% · `hourglass` 54,8% ·
`passbook_open` 54,1% · `couple_senior` 48,9% · `receipt` 47,5% · **`shield_dash` 9,3%** ⚠️ (khiên
nét đứt RỖNG nên phủ thấp là đúng bản chất — nhưng nét mảnh, **chỉ dùng ở cỡ ≥132px**, đừng đặt vào
cột icon 56px của `check`/`steps`).
📌 Ảnh thô giữ trong `_raw/` (không xoá) để chạy lại tool khi đổi tham số tách nền.

**Quy trình:** prompt 1 dòng ở **`_NEW10_prompts_FLOW.txt`** (bơm thẳng vào extension) · thứ tự dòng
↔ tên file ở **`_NEW10_prompts_TENFILE.txt`** → user gen → bỏ ảnh **THÔ** vào `_raw/` →
```
python E:\Claude\Projects\_media_library\ingest_stage_icons.py
```
Tool làm 4 việc: ① **cắt watermark ✦** (bỏ 12% mép phải + đáy — icon không có chữ nên cắt được,
không phải vá) ② **crop VUÔNG** (tool gen luôn xuất 16:9 dù prompt xin 1:1) ③ **tách nền trắng →
alpha bằng flood-fill TỪ BIÊN** — 🔴 không threshold toàn ảnh, nếu không thì mặt đồng hồ / tờ giấy /
ô kẻ của sổ bị khoét rỗng ④ trim sát vật + pad 6% → 512×512 RGBA. Xuất `_new_sheet.jpg` **nền kẻ ô**
để soi ngay chỗ nào còn nền trắng đục.

⚠️ Sau khi có icon mới: sửa `youtube-jp-nenkin/tools/build_slides_13.py` cho các beat tương ứng rồi
`build_slides_13.py` + dựng lại thẻ. `_sig` có tên+folder+mtime icon nên thẻ **tự dựng lại**.

## Thêm icon mới

1. Nền **trong suốt**, vuông, PNG, ≥256px. Đường nét navy `(26,42,74)`, nhấn vàng `(245,179,1)`.
2. Đọc được ở **56px** (cột icon của layout `check`/`steps` co về cỡ đó).
3. Tên **snake_case tiếng Anh**, đúng cái VẬT đó (`money_pouch`, không phải `okane`).
4. Bỏ vào đây → mọi kênh dùng được ngay, không phải sửa tool.
5. ⛔ Quét watermark trước (`.claude/rules/media-library.md` §2.10 ⑤b) — ảnh còn ✦ là chưa xong.

📌 Icon vào **chữ ký resume** `_sig` theo `tên + folder + mtime + size`, nên đổi file hoặc
chuyển icon giữa kho-chung/riêng-kênh thì thẻ **tự dựng lại**.
