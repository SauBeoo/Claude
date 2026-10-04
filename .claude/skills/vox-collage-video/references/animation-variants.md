# Animation variants — kho entrance cho Cutout hero

4 variant cơ bản đã code sẵn trong `example-scene.jsx`: `rise` · `grow` · `punch` · `flip`.
Dưới đây là 6 variant mở rộng, kèm note implement (Remotion `spring`/`interpolate`) và SFX
pairing tự nhiên. **Luật dùng:** không để 2 scene liên tiếp trùng variant; video >4 scene thì
phải với tới kho này thay vì xoay vòng 4 cái cơ bản. Và variant hay nhất là cái **tự chế theo
đúng động từ của câu** ("sụp đổ" → shatter/drop, "mở ra" → unfold, "lật lại" → peel) —
kho này là menu gợi ý, không phải trần.

Sau MỌI entrance, giữ idle bob/sway chạy tiếp (helper `idle()` trong example-scene) —
entrance xong mà đứng im là ảnh chết.

## shatter — vỡ mảnh rồi ghép lại (hoặc vào rồi vỡ)
SFX: `shatter`, thêm `riser` trước beat 0.5s nếu là khoảnh khắc reveal.
Implement: render cutout 4-6 lần trong các `div` có `clipPath: polygon(...)` chia mảnh
tam giác; mỗi mảnh spring riêng từ vị trí lệch (translate ±80-200px + rotate ±25°) về 0,
delay so le 2-3 frame. Chiều "vỡ ra" thì đảo interpolate.

## peel — bóc như sticker dán lên
SFX: `paper` (đúng chất nhất), hoặc `swipe`.
Implement: `rotateX` từ -70° về 0 với `transformOrigin: 'top center'` + translateY nhẹ
từ -40px; thêm 1 div bóng đen mờ (`opacity` interpolate 0.35→0) mô phỏng mặt sau sticker.
Spring damping ~11.

## unfold — mở ra như tờ giấy gấp đôi
SFX: `paper` + `pop` khi mở hết.
Implement: 2 nửa cutout (2 div `clipPath` trái/phải hoặc trên/dưới), nửa động `rotateY`
từ 180° về 0 với `transformOrigin` ở đường gấp, `perspective: 1400`. Nửa tĩnh hiện trước
3-4 frame. Hợp với chủ đề tài liệu/bản đồ/thư.

## spiral — xoáy vào từ xa
SFX: `whoosh` kéo dài, `thud` lúc đáp.
Implement: đồng thời `scale` 0.1→1, `rotate` 540°→0, translate từ góc khung về vị trí.
Dùng MỘT spring (damping 13) drive cả 3 kênh cho chuyển động dính nhau. Đừng lạm dụng —
1 lần/video là đủ, nhiều hơn thành chóng mặt.

## wobble-drop — rơi xuống nảy lật bật
SFX: `boing` (sinh ra cho nhau), hoặc `thud` + `boing`.
Implement: translateY spring damping thấp (6-7, stiffness 160) từ -500px — tự overshoot
thành nảy; cộng `rotate` sin tắt dần `Math.sin(frame/2.2) * 14 * Math.exp(-frame/12)`.
Hợp vật thể "nặng mà tinh nghịch": két tiền, hộp, con dấu.

## zoom-through — lao xuyên qua camera rồi lùi về đúng cỡ
SFX: `riser` dẫn vào + `thud`/`click` lúc khựng.
Implement: `scale` từ 3.5 (tràn khung, mờ `filter: blur(8px)` interpolate về 0) về 1,
opacity 0→1 trong 4 frame đầu. Spring damping 14 để khựng lại dứt khoát. Dùng cho
chủ thể "áp đảo": logo đối thủ, con số khổng lồ, gương mặt.

## Ghi chú chung
- Mọi variant drive bằng `spring()` của Remotion, đừng tự viết easing tay — spring cho
  cái chất "hơi quá đà rồi về" đúng vibe collage thủ công.
- Overshoot (damping thấp) là gia vị: 1-2 scene/video, không phải mọi scene.
- SFX đặt tại frame entrance THẬT của element (xem `Sfx` helper), volume 0.3-0.55.
- Support elements giữ entrance đơn giản (scale pop) — variant cầu kỳ là đặc quyền
  của hero, cả scene cùng múa thì không còn gì là điểm nhấn.
