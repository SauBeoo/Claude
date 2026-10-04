# Flow Batch v2 — cách dùng

> v1.1 bơm CHỮ vào Flow. **v2 thêm: đính ẢNH · dò UI · sổ chống gen trùng · dry-run.**
> Thiết kế + bằng chứng: `DESIGN_i2v_2026-09-09.md`. Backup v1.1: `panel.js.bak_v1.1_20260909`.

## ⓿ HAI TAB — v1 và v2 chạy song song

Panel có **2 tab** ở trên cùng, trạng thái được nhớ giữa các lần mở:

| tab | dùng khi | mặc định tự đặt |
|---|---|---|
| **v1 · bơm CHỮ** | gen ảnh / t2v hàng loạt (luồng bản 1.1, ~250 prompt/lượt) | DRY-RUN **tắt** · trần job/lượt **mở** · chờ **18s** · bỏ qua ảnh/mode/hàng đợi |
| **v2 · ẢNH → VIDEO** | `jobs.jsonl`, mode Frames | DRY-RUN **bật** · trần **5 job/lượt** · chờ **20s** |

🔴 **Sổ đã-gửi của v1 khoá theo NỘI DUNG prompt**, không theo số dòng — bản v2.0 khoá `line-N` nên
nạp một file prompt khác là `line-1` đã có trong sổ ⇒ **bỏ qua oan, im lặng**. Đã sửa.

🔴 **Sửa `panel.html` thì kiểm ngay `grep -c 'src="panel.js"' panel.html` phải ra ≥1.** Lượt viết lại
2026-09-09 làm mất thẻ `<script>` ⇒ panel.js không được nạp ⇒ **không nút nào có handler**, mà giao
diện vẫn hiện bình thường nên trông y như *"tool không quét được tab"*. Mất một vòng chẩn đoán.

## 0. Nạp extension
`chrome://extensions` → **Developer mode** ON → **Load unpacked** → chọn thư mục này.
🔴 Phải nạp ở **đúng Chrome profile đang đăng nhập account sở hữu project Flow** (account có gói
ULTRA). Profile sai thì Flow trả `/404?reason=project` — đã dính thật 2026-09-09 với
`saubeo.killuaa@gmail.com`.

## 1. Sinh file việc từ export của Flow
```bash
python Projects/youtube-jp-nenkin/tools/story_extract.py \
       "C:/Users/tuana/Downloads/Untitled Story - 2026-09-09_23-00.json" \
       "Projects/youtube-jp-nenkin/06_VIDEO/_demo_i2v/story"
```
Ra: `img/` (ảnh frame từng shot) · `ref/` (ảnh tham chiếu character/location/prop) ·
**`jobs.jsonl`** (1 job/1 dòng) · `_MANIFEST.json` · **`_REVIEW.md`**.

⚠️ **ĐỌC `_REVIEW.md` TRƯỚC KHI GEN.** Flow tự soạn `visual`/`motionDescription` và tự thêm 2 thứ
bị cấm — chuyển động máy (③) và framing chỉ-có-tay (④). Tool đã bỏ/đổi và ghi lại từng dòng, nhưng
**bản nháp vẫn phải duyệt bằng mắt**. Demo 2026-09-09: **6/7 shot** phải duyệt.

## 2. Mở panel
Bấm icon extension → panel mở ở tab riêng. Panel **không chiếm chuột/bàn phím thật** của bạn.

## 3. 🔍 DÒ UI — làm trước, luôn luôn
Chọn tab Flow (đang mở **một project**) → **🔍 DÒ UI**. Nó in ra: `.base-prompt-box` có không ·
ô prompt + placeholder · slot `Start`/`End` · số chip ảnh (và bao nhiêu chip *disabled*) ·
nút gửi / thêm ảnh khớp nhãn nào · **💰 giá credit** · **có đang hết credit không** ·
và **toàn bộ nút trong thanh prompt**.

Còn dòng `🔴 không khớp nhãn` → copy danh sách nút ở dưới, dán nhãn đúng vào ô ở mục 3 của panel
(tách nhau bằng `|`), dò lại. Còn 🔴 nữa thì gửi cả khối cho Claude.

## 3b. ⚙ CHỐT SETTINGS — một lần mỗi lô
Bấm **⚙ CHỐT SETTINGS**: tự bấm radio `Video → Frames → 16:9 → x1` rồi in giá credit.

🔴 **Phải là `Frames`, KHÔNG phải `Ingredient`.** Đo thật 2026-09-09: cùng một ảnh, ở mode
`Ingredient` thì chip ra `chip-container-disabled` + icon `error` **dù ảnh load tốt** = bị **từ chối**;
đổi sang `Frames` thì chip sạch và thanh prompt hiện **`Start ⇄ End`**. Tool tự chặn nếu chip disabled.

## 3c. 📋 LIỆT KÊ ASSET — lấy TÊN asset để ghép vào jobs.jsonl
Flow tự đặt caption cho từng asset (`Woman walking down hallway`), **không theo tên file của bạn**.
Bấm **📋 LIỆT KÊ ASSET** → copy danh sách → lưu thành `flow_assets.txt` → chạy lại:
```bash
python tools/story_extract.py "<...>.json" "<outdir>" "<...>/flow_assets.txt"
```
Nó ghép caption ↔ shot bằng **stem + IDF + gán 1-đối-1** (đo trên 7 shot: 5/7 đúng, 2 cái sai
**đều bị gắn ⚠**) và xuất **`_ASSETMAP.tsv`**. Sửa cột 2 ở dòng có ⚠ rồi chạy lại — **map tay THẮNG máy**.

## 4. 🧪 DRY-RUN trước, luôn luôn
Nạp `jobs.jsonl` → **DRY-RUN vẫn tick** → START. Nó làm **đủ mọi bước trừ cú bấm cuối**:
slot Start → gõ caption vào `Search assets` → chọn hàng khớp **duy nhất** → `Add to prompt` →
kiểm chip không disabled → gõ prompt → báo nút gửi sáng/mờ → xoá prompt.
**Không tốn một credit nào.**

🔴 Hàng search phải khớp **DUY NHẤT**. Nhiều kết quả mà cứ lấy hàng đầu = đính **sai ảnh** trong khi
prompt vẫn đúng ⇒ clip ra sai người, **100 credits**, không một dấu hiệu lỗi. Tool DỪNG và in danh sách.

## 5. Chạy thật
Bỏ tick DRY-RUN → **Trần job/lượt = 1** cho lần đầu → START. Xem credit tụt bao nhiêu, rồi mới nâng trần.

## Bốn lớp chặn credit (đừng tắt)
| | |
|---|---|
| **DRY-RUN** | mặc định bật |
| **Trần job/lượt** | mặc định 5, không có nút "chạy hết" |
| **Sổ đã-gửi** | theo `id` của job ⇒ bấm START lại **không bao giờ** gen trùng. `↺ tiến độ` KHÔNG xoá sổ; chỉ `🗑 xoá sổ` mới xoá |
| **Không auto-retry** | 2 job liền không xác nhận được là DỪNG. Video 1–3 phút và tốn credit ⇒ tự bấm lại là tự đốt tiền |

## Hai phép đo quyết định (đọc log để hiểu vì sao nó dừng)
1. **"đã đính ảnh"** = số thumbnail trong thanh prompt **tăng**, hoặc xuất hiện **nút gỡ**.
   ⛔ "đã bấm xong nút" không phải bằng chứng — Flow ở mode frames vẫn submit được với slot RỖNG
   và trả về **t2v thường**: tốn credit, sai loại video, **không một dấu hiệu lỗi nào**.
2. **"đã gửi"** = ô prompt sạch **HOẶC** có dấu hiệu bắt đầu chạy (busy/progressbar/video tăng).
   v1.1 chỉ đo ô prompt, và với video thì rất dễ "thấy chưa gửi" rồi bấm lại ⇒ 2 lần Veo/1 cảnh.

## Đính ảnh — đường ĐO ĐƯỢC, không phải đường đoán
⭐ **Không upload gì cả.** Ảnh đã nằm trong project ⇒ nút `+`
(`aria-label="Add ingredients to the prompt box"`) mở **bảng chọn asset** có `input.search-input`
+ danh sách asset có TÊN + nút `Add to prompt`. Đo bằng bẫy `showOpenFilePicker` +
`HTMLInputElement.prototype.click` + `MutationObserver`: bấm `+` cho ra
**`picker:0 · inputClick:0 · nFileInputs:0`** ⇒ **nó không hề mở hộp thoại file**.

Đường lui (chỉ dùng khi job khai `first` là đường dẫn đĩa): `Upload media` → chặn
`Page.fileChooserOpened` → `DOM.setFileInputFiles`, hoặc `input[type=file]` có sẵn.

## Bẫy đã dính, đừng lặp
- ⛔ **Đừng mở F12 trên tab Flow đang chạy** và đừng bấm *Hủy* trên dải vàng — debugger đứt.
- ⛔ Tab đã bị Claude-in-Chrome chạm vào thì extension **attach chồng là chết im**. Mở tab Flow MỚI.
- Project Flow phải bật **"Clear prompt on submit"** (⚙ của project). Tắt nó thì Flow giữ chữ lại
  sau khi gửi ⇒ mọi job bị chấm thất bại. (v2 còn dấu hiệu thứ hai nên đỡ hơn v1.1, nhưng vẫn nên bật.)
