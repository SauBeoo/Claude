# Nhân vật AI người dẫn — kênh shokutaku (60代からの食卓)

> # 🚫 PHẾ — KHÔNG DÙNG (user bỏ hẳn nhân vật AI HeyGen, 2026-07-25)
> File giữ lại làm tư liệu. Kênh này 100% ảnh tĩnh + pan, **không có footage người AI** → không phải tick "altered/synthetic content".

> Prompt gen avatar HeyGen. Người dẫn = persona **みのり** của kênh: ấm áp, kính ngữ mềm, gian bếp/bàn ăn. Phải ĐỘC NHẤT, khác health (tông mint, phòng khách) và đối thủ (bác sĩ áo blouse). Chốt 2026-07-23.
> ⚠️ Compliance: KHÔNG áo blouse/ống nghe/phòng khám, không xưng bác sĩ. Nhân vật hư cấu. Video có avatar → tick "altered/synthetic content" khi upload.

## Danh tính CHỐT (giữ cố định)
- **Ai:** みのり — phụ nữ Nhật ~60 tuổi, hiền hậu – ân cần – như người bà/người mẹ nấu ăn ngon.
- **Tông màu kênh:** kem / gỗ ấm / hổ phách (ấm cúng gian bếp) — khác hẳn mint-lạnh của health.
- **Bối cảnh:** gian bếp/bàn ăn Nhật ấm cúng, ánh sáng vàng dịu, có chút rau củ/bát đĩa mờ hậu cảnh.
- **Trang phục:** áo len/cardigan màu ấm + **tạp dề (apron)** vải mộc — dấu hiệu "gian bếp" nhận diện ngay.

## Prompt HeyGen — "Generate Photo Avatar" (dán ô mô tả, tiếng Anh)

**Bản chính:**
```
Photorealistic portrait of a warm, kind Japanese woman around 60 years old, gentle
motherly face with soft smile lines, natural light makeup, neatly styled short-to-
medium dark hair with a little grey, caring grandmotherly-yet-elegant vibe.
Wearing a warm-toned knit cardigan (cream/terracotta) with a simple natural-linen
apron. Background: cozy warm Japanese kitchen / dining nook, amber-cream tones,
softly blurred vegetables and tableware, warm window light. Upper-body medium shot,
facing camera, soft warm natural lighting, shallow depth of field, 16:9.
NEGATIVE: white lab coat, doctor coat, stethoscope, clinic, hospital, medical props,
restaurant chef uniform, text, letters, logo, watermark, overly young, cartoon, anime.
```

**Biến thể (đổi nhẹ giữa 3 clip/tháng — GIỮ NGUYÊN gương mặt):** đổi màu cardigan (kem ↔ nâu đất ↔ xanh rêu ấm), đổi góc bếp, có/không cầm nhẹ 1 bát gỗ.

## Cài đặt VIDEO trên HeyGen (mỗi clip 1 phút)
- **Tỉ lệ:** 16:9. **Khung:** medium shot ngang eo/ngực, nhìn thẳng camera.
- **Cử chỉ:** bật "natural gestures" (cần CHUYỂN ĐỘNG, không cần khớp miệng).
- **Voice:** giọng nữ Nhật (ja-JP) ấm, lớn tuổi. (Renderer bỏ tiếng clip, giữ giọng TTS mình → script không quan trọng.)
- **Script (filler chung ~60s, giọng みのり, KHÔNG lộ chủ đề):**
  ```
  こんにちは、みのりです。今日も、六十代からの食卓に、ようこそ。
  むずかしい話は抜きにして、毎日の食事で無理なくできる工夫を、ゆっくりお伝えしていきますね。
  お茶でも飲みながら、気楽に聞いてください。それでは、はじめましょうか。
  ```
- **3 clip/tháng:** giữ nguyên danh tính みのり, chỉ đổi nhẹ góc/màu cardigan/cử chỉ.

## Sau khi có clip
```
python E:\Claude\Projects\youtube-jp-health\tools\avatar_broll.py ingest <clip>.mp4 --channel shokutaku
```
