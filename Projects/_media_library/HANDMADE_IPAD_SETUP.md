# iPad + Apple Pencil → footage lớp thủ công (setup thực chiến)

> ⛔ **KHÔNG CÒN BẮT BUỘC (2026-08-09).** Lớp thủ công đã bỏ ở mọi kênh — `.claude/rules/handmade-layer.md`. File này giữ lại làm hướng dẫn **tùy chọn**, chỉ dùng khi user TỰ MUỐN quay. Không skill nào được xuất bảng cần quay nữa.


> Phụ lục thi hành của `.claude/rules/handmade-layer.md` §5. Chốt 2026-07-27 (user có iPad + Apple Pencil, chưa cài app).
> Mục tiêu: quay được lớp `notebook` (viết ノート thật) và `genten` (khoanh đỏ trang luật thật) — hai thứ đối thủ chạy AI pipeline không có.

## 1. APP — cài gì (đi đường miễn phí trước, đừng mua sớm)

| Lớp | Dùng gì | Giá | Ghi chú |
|---|---|---|---|
| **`genten` khoanh đỏ 原典** | **KHÔNG cần app nào** — Markup có sẵn trong **Files / Books / Safari** (mở PDF của 厚労省・国税庁・法務局 → nút bút → chọn **bút đỏ** → khoanh) | 0 | Đây là lớp rẻ nhất mà uy tín nhất. Làm ngay được hôm nay. |
| **`notebook` viết ノート** | **Freeform** (có sẵn iPadOS 16.2+, canvas vô hạn, thanh công cụ nhỏ) hoặc **Notes**. Cần giấy kẻ ô + template trang → **GoodNotes** | 0 / GoodNotes mua thêm | **Bắt đầu bằng Freeform.** Chỉ mua GoodNotes khi thật thấy thiếu (giấy kẻ ô, quản trang nhiều video). Giá đổi liên tục → xem App Store. |
| **`character` nhân vật** | **Procreate** (+ Procreate Dreams nếu muốn nhân vật động) | mua 1 lần | **Chưa làm bây giờ** — lối đắt nhất, để sau khi lối ① và ③ có data. |

## 2. SCREEN RECORD — cấu hình 1 lần

1. **Cài đặt → Trung tâm điều khiển → thêm "Ghi màn hình"**.
2. **BẮT BUỘC bật Focus/Không làm phiền trước mỗi lần quay** — 1 banner thông báo lọt vào khung là phải quay lại từ đầu. Thêm: **Cài đặt → Thông báo → Hiện bản xem trước → Không bao giờ**.
3. **Nhấn giữ nút ghi màn hình → TẮT micro** (giọng lấy từ TTS, tool cũng bỏ audio).
4. Bật **Từ chối lòng bàn tay** (palm rejection) trong app để tì tay không vẽ bậy.
5. Video ghi ra nằm trong **Ảnh** → chuyển sang PC bằng: **cáp USB** (iPad hiện trong File Explorer như thiết bị camera → copy từ `DCIM`) · hoặc **iCloud Drive cho Windows** · hoặc app LAN kiểu LocalSend. ⚠️ **AirDrop không sang được Windows** — đừng mất thời gian thử.

## 3. VÙNG AN TOÀN — chỗ nào KHÔNG được viết vào

Khung video 1920×1080 đã có 3 lớp đè lên sẵn:

```
┌─────────────────────────────────────────┐
│ [badge 第N位/その1]      [watermark kênh] │  ← 12% trên: TRỐNG
│                                         │
│        ★ VIẾT Ở DẢI GIỮA NÀY ★          │
│                                         │
│ [────── phụ đề hộp trắng ──────]        │  ← 20% dưới: TRỐNG
└─────────────────────────────────────────┘
```

- **Chừa trống ≥12% trên** (badge rank góc trái + watermark góc phải) và **≥20% dưới** (phụ đề đè lên).
- **Cỡ chữ tối thiểu trên khung 1080: 40px** (sàn tuyệt đối) — nên **≥55px** cho chữ thường và **≥90px cho số tiền** (khán giả 50–70 xem điện thoại; số là nhân vật chính, không phải chữ đẹp).
- Ước lượng nhanh trên iPad: **một dòng chữ phải cao ≥1/18 chiều cao vùng quay**. Nghĩ theo kiểu "viết cho người ngồi xa 3 mét đọc được", không phải "viết vào sổ tay".

## 4. CẮT UI KHI INGEST — số liệu cụ thể

Screen-record dính status bar (giờ/pin) + thanh công cụ app → cắt bằng `--crop-box`. **Chọn khung cắt đúng tỉ lệ 16:9 thì không mất thêm gì**; lệch 16:9 thì bước scale cắt tiếp (tool tự in ra chiều cao lý tưởng).

Công thức: `chiều cao khung cắt = chiều rộng ÷ 1,7778`

| iPad | Màn hình quay ra | Khung cắt 16:9 gợi ý |
|---|---|---|
| 11″ (2388×1668) | 2388×1668 | `--crop-box "0,160,2388,1503"` (cao 1343) |
| 10,9″ Air (2360×1640) | 2360×1640 | `--crop-box "0,150,2360,1478"` (cao 1328) |
| 12,9″ (2732×2048) | 2732×2048 | `--crop-box "0,270,2732,1807"` (cao 1537) |

- Không biết model → chạy `ingest` không kèm `--crop-box` một lần, tool in ra `▶ <file> WxH`, rồi tính theo công thức.
- Toolbar nằm bên trái/phải → thu hẹp cả `x0`/`x1`, tool sẽ nhắc lại chiều cao 16:9 tương ứng.
- Viết chậm thì thêm `--speed 1.3–1.6` (viết tay chậm hơn nhịp kể); **số tiền thì ĐỪNG tăng tốc** — khán giả cần kịp đọc số hiện ra.

## 5. MẪU TRANG ノート theo kênh (viết đúng khối ~50%, trùng chỗ CTA)

**nenkin — case tính thử tiền** (`cta-midvideo.md` §2.4b):
```
   在職老齢年金 ・ Aさん 64歳
   ─────────────────────
   給与    28万円
   年金    12万円   ← viết chậm
   合計    40万円
   ─────────────────────
   支給停止   □ 万円     ← để trống, viết SỐ sau khi giọng nói tới
```

**kaigo — 実家の家計簿** (§2.8): 3 cột `親の年金 / 介護にかかる分 / 足りない分` — cột thứ 3 viết **cuối cùng, khoanh tròn đỏ**.

**akiya — 実家の値段表** (§2.9): 4 dòng = 4 lối thoát của căn nhà (`売る / 貸す / 解体 / 放棄`), mỗi dòng một con số, **cái rẻ nhất khoanh đỏ ở cuối**.

Luật chung 3 mẫu: **ô đáp án để TRỐNG lúc bắt đầu quay**, chỉ viết vào khi giọng đọc tới. Cái người xem đợi là *thấy số hiện ra*, không phải trang giấy đã viết xong.

## 6. QUY TRÌNH 1 SHOT (5 phút)

1. Bật Focus → mở trang trắng → **bắt đầu ghi màn hình**.
2. **Đợi 1 giây rồi mới viết** (tool cắt đầu bằng `--trim` cần chỗ thở); viết xong **đợi 1 giây** rồi mới dừng.
3. Quay **dài hơn cue** trong 撮影リスト — ngắn hơn thì renderer LOOP, thấy rõ nhịp lặp.
4. Chuyển file sang PC → ingest:
   ```bash
   python E:\Claude\Projects\_media_library\ingest_handmade.py ingest "<file>" \
       --channel youtube-jp-nenkin --hm-kind notebook --tags "在職老齢年金 支給停止" \
       --crop-box "0,160,2388,1503" --speed 1.4 --trim 0:01,0:38
   ```
5. `place` vào video + `sheet` → **Read ảnh, duyệt mắt** trước khi render.

## 7. CHECKLIST DUYỆT (soi contact sheet)

- [ ] Không lọt status bar / thanh công cụ / banner thông báo
- [ ] Chữ đọc được ở cỡ 120px preview? Số tiền có to nhất khung?
- [ ] Nội dung không lấn 12% trên / 20% dưới (badge + phụ đề sẽ đè)
- [ ] Không lộ: tên thật, địa chỉ, giấy tờ thật của mình, tên app/nhãn hiệu đọc được
- [ ] `genten`: trang luật đúng cơ quan + **thấy rõ nét khoanh đỏ đang được vẽ** (không phải ảnh đã khoanh sẵn)

## 8. 🔴 HEALTH — làm từng bước, KHÔNG cần nguyên liệu, KHÔNG cần biết quay

> ⚠️ **KHÔNG CÒN BẮT BUỘC cho health (sửa 2026-07-28).** User chất vấn đúng rằng `make_drawn.py` làm được đúng beat đó — xem `.claude/rules/handmade-layer.md` §3.1. Trang ノート của health nay do tool sinh. **Giữ §8 này cho ai muốn làm thật** (nét bút thật vẫn nhịnh hơn về cảm giác) và cho việc **khoanh đỏ `genten` trên iPad** khi đã có screenshot trang cơ quan.

> Viết cho tình huống thật của user (2026-07-27): *"tao không biết quay như nào, và nguyên liệu đôi khi không có luôn"*. Đường này bỏ hẳn nhu cầu camera + nguyên liệu. Toàn bộ là **ghi màn hình iPad**. Lần đầu mất ~20 phút để quen, từ lần 2 còn **~5 phút/video**.

### 8.1 Chuẩn bị 1 lần duy nhất — GOODNOTES (user có sẵn, chốt 2026-07-28)

**iPad:**
1. Cài đặt → Trung tâm điều khiển → thêm **Ghi màn hình**.
2. Cài đặt → Thông báo → **Hiện bản xem trước → Không bao giờ**. Bật **Không làm phiền** trước mỗi buổi quay.
3. Nhấn giữ nút Ghi màn hình → **tắt Micro** (giọng lấy từ TTS).
4. **Xoay iPad NGANG** và khóa hướng — trang dọc quay ra khung dọc, crop mất gần nửa chữ.

**GoodNotes:**
5. Tạo notebook mới tên `健康ノート`: **Orientation = Landscape (ngang)** · **Paper = Squared/方眼 (kẻ ô)** · màu giấy trắng hoặc kem.
6. Bút: **Fountain pen** hoặc **Ball pen**, màu đen/xanh đen, **độ dày đặt mức to nhất trong 3 preset** (hoặc slider ~1,0–1,4mm). Dày hơn cảm giác "đẹp" — chữ phải đọc được trên điện thoại.
7. Đặt sẵn **1 preset bút ĐỎ** ở ô bút thứ 2 (để khoanh đáp án, khỏi phải mò màu lúc đang quay).
8. Bật **wrist guard / palm rejection** trong cài đặt GoodNotes.
9. **Dọn UI trước khi bấm quay** (đây là bước hay bị bỏ): đóng **sidebar thumbnail trang** bên trái · **thu gọn thanh công cụ** (nút mũi tên/chevron ở đầu thanh) · pinch để trang **vừa khít bề ngang**. Không dùng **Zoom Window** (ô viết phóng to) — nó hiện dải UI vào giữa khung.
10. ⚠️ UI GoodNotes đổi theo phiên bản. Không tìm ra nút thu gọn thanh công cụ thì **cứ quay có thanh công cụ** — `--crop-box` cắt được phần trên; nhưng khi đó phải chừa trống nhiều hơn ở đỉnh trang.

### 8.2 Chuẩn bị mỗi video (~1 phút)
Tao sẽ đưa mày bảng `収録リスト` kèm script. Mày chỉ cần **viết sẵn phần khung**, chưa viết đáp án:

```
        長寿の食卓 TOP5                 ← tiêu đề, viết sẵn
   5位  ______________               ← để trống hết
   4位  ______________
   3位  ______________
   2位  ______________
   1位  ？                            ← ĐỂ DẤU ? , đây là cái giữ người xem
```

**Cỡ chữ — đo bằng ô giấy, đừng đo bằng cảm giác:** cả trang ngang chỉ được **tối đa 7–8 dòng chữ**. Trang mẫu trên có 6 dòng (tiêu đề + 5 hạng) là vừa đẹp. Viết được 12 dòng lên 1 trang nghĩa là **chữ quá nhỏ**, phải viết to lại.

**Chừa trống:** ~**1 dòng ở đỉnh trang** (badge 第N位 + watermark 健康ノート sẽ đè) và ~**2 dòng ở đáy** (phụ đề hộp trắng). Viết lấn xuống đáy là bị phụ đề che.

### 8.3 Quay (5 lần bấm, mỗi lần ~15 giây)
Không quay 1 lần dài. Quay **từng đoạn ngắn**, mỗi đoạn = viết 1 hạng:

| Lần | Bấm ghi màn hình → | Rồi bấm dừng |
|---|---|---|
| 1 | đợi 1 giây, viết `5位 きのこ` | đợi 1 giây |
| 2 | viết `4位 納豆` | 〃 |
| 3 | viết `3位 鮭` | 〃 |
| 4 | viết `2位 味噌汁` | 〃 |
| 5 | **xóa dấu `？`, viết `1位 ◯◯` + khoanh đỏ** | 〃 |

Sai thì cứ quay lại đoạn đó, không ảnh hưởng đoạn khác. **Không cần chỉnh gì thêm** — tool tự cắt viền, tự tăng tốc, tự bỏ tiếng.

**Mẹo trong lúc quay (GoodNotes):** viết sai thì **chạm 2 ngón để Undo** ngay trong lúc đang ghi — rồi viết lại; tool sẽ `--trim` bỏ đoạn đầu nên nhịp sai bị cắt. Đừng thoát app ra sửa (mất mạch, lộ UI).

### 8.3b ⚠️ LẦN ĐẦU: quay 1 clip THỬ rồi gửi tao trước khi quay cả bộ
Đừng viết cả 5 hạng ngay lần đầu. Quay **1 đoạn ~15 giây** (viết đúng 1 dòng, vd `5位 きのこ`) → copy sang máy → đưa tao đường dẫn. Tao sẽ đo hộ và trả lời 3 câu:
1. Chữ có đủ to ở cỡ điện thoại chưa (đo bằng pixel thật, không đoán)?
2. Số `--crop-box` chính xác cho iPad của mày là bao nhiêu (thay vì tra bảng §4)?
3. Có lọt UI GoodNotes / status bar / thanh công cụ vào khung không?
Sai cỡ chữ mà quay xong cả bộ 5 clip thì phải quay lại cả bộ — 15 giây thử này tiết kiệm đúng chỗ đó.

### 8.4 Đưa sang máy + vào video (tao chạy, mày chỉ copy file)
File nằm trong **Ảnh**. Cắm cáp USB → iPad hiện trong File Explorer → copy từ `DCIM` sang một folder bất kỳ, rồi báo tao đường dẫn. Tao chạy:
```bash
python E:\Claude\Projects\_media_library\ingest_handmade.py ingest "<file>" \
    --channel youtube-jp-health --hm-kind notebook --tags "<món> ランキング" \
    --crop-box "0,160,2388,1503" --speed 1.4 --trim 0:01,
```
(`--crop-box` theo model iPad — bảng §4. Không biết model thì chạy 1 lần không kèm cờ đó, tool in ra kích thước rồi tính.)

### 8.5 Vì sao làm thế này thay vì quay món ăn
- **Không cần nguyên liệu** — kênh nói về 5 món nhưng trang giấy không cần món nào.
- **Đánh đúng chỗ đang hỏng:** 41–69% người xem bỏ đi trước giây 60. Ô `1位 ＝ ？` viết tay trong 30 giây đầu là lời hứa **nhìn thấy được**, mạnh hơn một câu thoại hứa suông.
- **Là lớp không copy được:** đối thủ chạy pipeline AI không có nét bút thật. Đồng thời là "giá trị gốc" theo đúng nghĩa policy inauthentic content.
- **Trả open loop bằng hình:** ô trống được điền ở ~80% thời lượng → lý do ở lại đến cuối.
