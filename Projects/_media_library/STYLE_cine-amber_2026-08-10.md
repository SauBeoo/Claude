# BỘ KHOÁ STYLE 「CINE-AMBER」 — gen ảnh ĐỒNG NHẤT giữa nhiều video

> Bóc từ ảnh mẫu user đưa 2026-08-10: `Dust_motes_floating_in_bookstore_202608102305.jpeg`
> (hiệu sách cũ Nhật, luồng sáng xuyên bụi, tông hổ phách).
> Mục đích: **nhiều ảnh, nhiều video, mà nhìn như cùng một người quay** — không phải mỗi ảnh một style.

## 1. DNA đo được từ ảnh mẫu (đây là thứ phải giữ y nguyên)

| Yếu tố | Khoá |
|---|---|
| **Loại ảnh** | photoreal điện ảnh, như phim quay máy — KHÔNG minh hoạ, KHÔNG 3D render |
| **Bảng màu** | hổ phách / nâu sepia, **giảm bão hoà**, trắng ngả kem; không màu lạnh, không xanh lơ |
| **Ánh sáng** | **MỘT luồng sáng chéo** từ cửa sổ cao, thấy được khối sáng (volumetric), **bụi bay lấp lánh** trong luồng |
| **Tương phản** | góc tối sâu, **vignette** rõ ở 4 mép, sáng chỉ tập trung một dải |
| **Bố cục** | phối cảnh **một điểm tụ** — hành lang/lối hẹp, hai bên đối xứng dẫn mắt vào giữa |
| **Ống kính** | cảm giác anamorphic, méo nhẹ mép, nét sâu ở gần–mờ nhẹ ở xa, **hạt phim** mảnh |
| **Người** | **KHÔNG có người** (ảnh mẫu trống người — giữ vậy để dễ ghép, và né compliance mặt người) |
| **Khung** | 16:9 |

## 2. KHỐI STYLE CỐ ĐỊNH — dán vào ĐUÔI mọi prompt, không sửa một chữ

```
Cinematic photorealistic still, shot on 35mm film, single warm shaft of sunlight cutting
diagonally from a high window with visible volumetric light and glittering dust motes floating
in the beam, deep shadows and strong vignette in the corners, desaturated warm amber and sepia
palette with cream highlights and no cool tones, one-point perspective leading the eye into the
centre, slight anamorphic lens distortion, fine film grain, shallow depth of field falling off
into the background, no people, no text, no letters, no logo, no watermark. --ar 16:9
```

## 3. Cách viết một ảnh mới (chỉ đổi PHẦN ĐẦU)

`[CHỦ THỂ + KHÔNG GIAN, 1–2 câu, tả VẬT chứ đừng tả cảm xúc]` + khối §2.

**Ảnh mẫu viết lại theo khuôn này** (kiểm chứng rằng khối §2 tái tạo được ảnh gốc):

```
A narrow aisle inside an old Japanese second-hand bookshop, tall dark wooden shelves packed
with worn paperbacks and faded magazines on both sides, stacks of books piled on a scuffed
wooden plank floor, a single bare hanging bulb near the ceiling.
```
+ khối §2.

**Ba ví dụ khác cùng chất** (đổi chủ thể, giữ style):
- `An old Japanese post office counter at closing time, a wooden sorting rack full of envelopes, a rubber date stamp and an ink pad left on the worn counter top.`
- `A small tatami room with a low wooden table, an open ledger notebook, an abacus and a chipped teacup, sliding paper doors half open.`
- `The entrance of an old Japanese house, worn wooden step, a pair of sandals, a rusted mailbox mounted beside the door frame.`

## 4. Luật giữ ĐỒNG NHẤT (làm sai một cái là bộ ảnh vỡ)

1. **Cả bộ gen trong CÙNG MỘT LƯỢT, cùng một model.** Đổi model/đổi ngày = đổi chất, dù prompt y hệt.
2. **Đừng đổi từ trong khối §2** để "cho đa dạng". Đa dạng nằm ở CHỦ THỂ, không nằm ở style.
3. **Không thêm người** vào một số ảnh mà không thêm vào ảnh khác — có người/không người là hai chất khác nhau hẳn.
4. **Chỉ tả VẬT trong phần đầu.** Viết `lonely, nostalgic, melancholic` thì model tự đổi ánh sáng ⇒ vỡ đồng nhất.
5. **Duyệt bằng cách xếp cả bộ cạnh nhau** (contact sheet), không duyệt từng ảnh một — lệch chất chỉ lộ khi đặt cạnh nhau.

## 5. 🔴 ✦ WATERMARK — ảnh mẫu CÓ dấu ✦ ở góc dưới-phải

Ảnh mẫu `2000×1051` có ✦ ở góc dưới-phải. Cùng lò gen ⇒ mọi ảnh của bộ này sẽ có.
- **ĐO LẠI vị trí theo TỪNG LÔ**, đừng dùng số của lô trước (đã dính: lô `2752×1536` có ✦ ở
  `(2637,1422)`, **không** phải toạ độ gấp đôi của lô `1376×768`).
- **Xử bằng CROP**, không inpaint (`cv2.inpaint` để lại vết nhoè; median filter để lại vệt).
  Ảnh 16:9 crop mất dải phải thì crop cả 4 mép cho cân rồi resize về 1920×1080.

## 6. LIÊN QUAN
- Chính sách asset: `.claude/rules/media-library.md` (mỗi video tải/gen bộ riêng, kho là SỔ ĐEN)
- Ảnh AI trong video ⇒ **TICK "altered/synthetic content"** khi upload: `youtube-compliance.md` §2.1
- Ảnh AI chứa chữ Nhật hay nát nét ⇒ khối §2 đã ghi `no text`; cần chữ thì đốt bằng tool
