# HƯỚNG DẪN CHẠY TOOL — Flow Batch v2.4

> Chạy 3 shot của SCENE 01 (`PENSION RESEARCH LAB`) bằng tool thay vì bấm tay.
> Bản bấm tay: `youtube-jp-nenkin/06_VIDEO/_demo_i2v/HUONG_DAN_GEN_1_VIDEO_DEMO.md`.

## 0. 🔴 TOOL LÀM ĐƯỢC GÌ / KHÔNG LÀM ĐƯỢC GÌ — đọc trước

| việc trong quy trình | tool | ghi chú |
|---|---|---|
| quét & chọn tab Flow | ✅ | tự chẩn đoán khi không thấy tab (profile sai / chưa mở project / Flow đổi domain) |
| dò UI, in nhãn nút thật + **giá credit** | ✅ | nút 🔍 DÒ UI |
| **tắt chế độ Agent** | ✅ | `ensureClassicBar()` — không tắt thì không có slot `Start`/`End` |
| chọn **Video · Frames · 16:9 · x1** | ✅ | nút ⚙ CHỐT SETTINGS, bấm radio theo TEXT |
| **đặt 720p** | ❌ **TAY** | popover không có radio độ phân giải — tool không với tới |
| **chọn model** (Veo Lite / Quality) | ❌ **TAY** | là dropdown, chưa code |
| liệt kê tên asset trong project | ✅ | nút 📋 LIỆT KÊ ASSET |
| đính ảnh: slot Start → search → chọn hàng → Add to prompt | ✅ | search **scope trong hộp thoại** (trang có 2 ô search) |
| bắt buộc hàng khớp **DUY NHẤT** | ✅ | nhiều kết quả ⇒ **DỪNG**, không bấm bừa |
| kiểm chip ảnh **không bị disabled** | ✅ | disabled = sai mode ⇒ dừng |
| gõ prompt (trusted input, chống nối chuỗi) | ✅ | |
| bấm gửi + xác nhận đã gửi (2 điều kiện) | ✅ | |
| **chặn khi hết credit** | ✅ | đọc `Insufficient credits warning` |
| DRY-RUN (chạy khô, 0 credit) | ✅ | |
| sổ chống gen trùng | ✅ | theo `id` job |
| **tải clip về + đổi tên** | ❌ **TAY** | Phase 2, chưa làm |
| **nối clip thành video** | ❌ | dùng `ffmpeg` — xem doc bấm tay §4 |

⚠️ **Điều phải nói rõ: tool chưa từng chạy trọn một lượt trên UI thật.** Tao đã kiểm **từng bước
một** trên project thật (tắt Agent → slot Start → search → Add to prompt → chip sạch → gõ prompt →
nút gửi sáng) nhưng **bằng tay qua Claude-in-Chrome**, vì extension và Claude-in-Chrome
**không dùng chung một tab được** (`chrome.debugger` độc quyền). Nên:

- ✅ **Chuỗi bước và mọi selector là ĐO ĐƯỢC**, không đoán.
- ⚠️ **Phần chưa kiểm được:** cách tool phát hiện "job đang chạy" (`busyTxt`/`progressbar`).
  Giảm rủi ro: **`Trần job đang chạy = 1`** và **`Chờ giữa 2 job = 120` giây** cho lượt đầu.
- 🔴 Vì vậy **lượt đầu BẮT BUỘC chạy DRY-RUN**, và lượt thật đầu tiên để **Trần job/lượt = 1**.

---

## 1. Nạp extension (1 lần)

`chrome://extensions` → **Developer mode** ON → **Load unpacked** →
`E:\Claude\Projects\youtube-jp-showa\tools\flow_batch_ext`

🔴 Nạp ở **đúng Chrome profile đang đăng nhập account Flow có credit**. Extension chỉ thấy tab
**cùng profile** với nó, và project của account khác trả `/404?reason=project`.

Đã nạp rồi mà tao vừa sửa code → bấm **⟳ Reload** trên thẻ extension (bản hiện tại: **2.4**).

---

## 2. Sinh file việc

```bash
cd E:\Claude
python Projects/youtube-jp-nenkin/tools/story_extract.py ^
  "C:/Users/tuana/Downloads/PENSION RESEARCH LAB_ THE TWO PAYMENTS - 2026-09-10_00-29.json" ^
  "Projects/youtube-jp-nenkin/06_VIDEO/_demo_i2v/pension01" ^
  --dl "C:/Users/tuana/Downloads/Sep 09 - 22_34" --scenes 01
```

Kết quả đã chạy thật:
```
--scenes 01: 3/66 shot
ghép asset bằng MD5: 3/3 shot
-> jobs.jsonl · _MANIFEST.json · _REVIEW.md
⚠ shot phai duyet tay: 3/3  (doc _REVIEW.md)
```

- `--dl` = thư mục ảnh **bạn đã tải từ Flow**. Tool ghép tên asset bằng **MD5 byte ảnh**
  (khớp 66/66 khi thử cả bài) ⇒ tên asset **chính xác**, không phải đoán theo chữ.
- `--scenes 01` = chỉ lấy Scene 01. Bỏ cờ này là ra cả 66 shot.
- Tool cũng **cảnh báo tên asset trùng nhau** ngay lúc sinh file, thay vì để job chết giữa lô.

🔴 **PROMPT TỰ SINH CHỈ LÀ BẢN NHÁP — `_REVIEW.md` gắn ⚠ cho 3/3 shot.** Lý do: Flow tự soạn
`motionDescription` và nhét chuyển động máy vào cả 3 shot; tool bỏ được phần camera nhưng cái còn
lại nhiều khi chỉ là mô tả khung (`A medium close-up focusing on Katsuo`), không phải chuyển động.
⇒ **Mở `jobs.jsonl`, thay 3 prompt bằng 3 prompt viết tay ở §2 của doc bấm tay.** Sửa xong file
vẫn là 1 job/1 dòng.

---

## 3. Chạy

1. Bấm icon extension → panel mở ở tab riêng.
2. Chọn tab **`v2 · ẢNH → VIDEO`** (2 tab ở trên cùng).
3. **↻ quét** → chọn tab Flow (đang mở project).
4. **🔍 DÒ UI** → phải thấy:
   - `.base-prompt-box: ✓` · `Ô prompt: ✓ ProseMirror`
   - `Nút GỬI: ✓ «Start generation»` (mờ khi ô trống — **bình thường**)
   - `💰 CREDIT: …` — nếu có `🔴 HẾT CREDIT` thì dừng, chờ credit ngày mới.
5. **⚙ CHỐT SETTINGS** → nó bấm `Video → Frames → 16:9 → x1` rồi in `Slot frame: Start / End`.
   🔴 **Rồi TỰ TAY**: bấm chip `Video · … · 8s` → đặt **720p** + chọn **model**.
6. Nạp `jobs.jsonl` (nút chọn file).
7. Đặt: **Trần job/lượt = 1** · **Chờ giữa 2 job = 120** · **Trần job đang chạy = 1**.
8. **DRY-RUN vẫn tick** → **START**. Log phải ra:
   ```
   ── 1/3 · sb_01_s01sh01 · mode=frames ──
   ảnh: "Man sitting at table"
   prompt: 4xx/4xx ký đã vào ô
   🧪 nút gửi: ✓ sáng → KHÔNG bấm
   🧪 chip ảnh: 1 (disabled 0)
   ```
   **Không tốn credit ở bước này.**
9. Bỏ tick DRY-RUN → **START** → 1 clip thật. Xem credit tụt bao nhiêu.
10. Đạt thì nâng **Trần job/lượt = 3** để chạy nốt 2 shot còn lại.

---

## 4. Đọc log khi nó DỪNG

| log | nghĩa | làm gì |
|---|---|---|
| `Search "X" ra N kết quả … DỪNG để không đính sai ảnh` | 2 asset cùng tên | vào Flow **chọn tay bằng preview** cho shot đó, hoặc đổi `asset` trong `jobs.jsonl` sang tên khác đủ phân biệt |
| `Chip ảnh ở trạng thái DISABLED … SAI MODE` | đang ở `Ingredient` | bấm ⚙ CHỐT SETTINGS lại |
| `Không thấy slot «Start» hay nút thêm ảnh` | còn ở chế độ Agent, hoặc Flow đổi nhãn | 🔍 DÒ UI, xem danh sách nút, sửa ô «Nút thêm ảnh» ở mục 3 |
| `Flow báo HẾT CREDIT … DỪNG` | hết credit | chờ credit ngày, hoặc đổi account |
| `2 job liền không xác nhận được — DỪNG` | có thể là phép đo "đang chạy" sai | 🔍 DÒ UI; kiểm trong Flow xem clip **có thật sự đang chạy** không. **Đừng bấm START lại trước khi biết** — 100 credits/clip |
| `Chờ 6 phút queue vẫn đầy — DỪNG` | queue nghẽn, hoặc `busyTxt` báo sai | như trên |

⛔ Tool **không bao giờ tự bấm lại** một cú gen. Đó là cố ý: auto-retry = tự đốt credit.

---

## 5. Sau khi có 3 clip

Tải về **theo đúng thứ tự shot**, rồi:
```bash
printf "file 's01_1.mp4'\nfile 's01_2.mp4'\nfile 's01_3.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy demo_scene01.mp4
```
Nghiệm thu: **sheet 4 frame/clip** (0,5s · 2,6s · 5,0s · 7,4s) — xem doc bấm tay §5.

---

## 6. Tab `v1 · bơm CHỮ` — luồng cũ vẫn nguyên

Dùng khi gen ảnh / t2v hàng loạt như bản 1.1: dán prompt **mỗi dòng 1 cái**, tool tự tắt DRY-RUN,
bỏ trần job/lượt, chờ 18s, và **bỏ qua hết phần ảnh/mode/hàng đợi**.
Sổ đã-gửi ở tab này khoá theo **nội dung prompt** (không theo số dòng) nên nạp file khác không bị
bỏ qua oan.

---

## 7. Ba điều đừng làm

1. ⛔ **Đừng mở F12 trên tab Flow** đang chạy, đừng bấm *Hủy* trên dải vàng — đứt debugger.
2. ⛔ **Tab đã bị Claude-in-Chrome chạm vào thì extension attach chồng là chết im.** Mở tab Flow MỚI.
3. ⛔ **Đừng xoá sổ đã-gửi** (`🗑`) trừ khi thật sự muốn gen lại — `↺ tiến độ` không xoá sổ.
