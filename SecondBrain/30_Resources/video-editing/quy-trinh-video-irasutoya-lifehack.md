# Quy trình làm video style いらすとや (kiểu ライフハック雑学)

> Đúc 2026-07-30 từ việc mổ video mẫu user gửi: https://www.youtube.com/watch?v=UXKsDX7nkgA
> 【雑草対策】夏に生える雑草はこれをすると勝手に簡単に全滅します — kênh **【毎日を快適に】ゆるっとライフハック雑学** (69K sub).
> Số đo tại thời điểm mổ: **547K view / 3 tuần · outlier 33,3x · dài 10:22**. Kênh này có hồ sơ đối thủ trong `Projects/youtube-jp-co-dai/CHANNEL_OPTIMIZE.md` §3 (hit 黄ばみ 982K · 雑草100円 525K · ムカデ 685K).

## 1. Giải phẫu format (xác minh bằng mắt qua storyboard, không đoán)

Đây **KHÔNG phải hoạt hình chuyển động** — là **slideshow hình minh họa いらすとや** với cấu trúc khung hình cố định:

| Thành phần | Cụ thể |
|---|---|
| Nền | **Trắng phẳng** toàn khung, không texture, không khung viền |
| Telop trên | Chữ **đen to 1–2 dòng phía TRÊN** = chính câu thoại đang được đọc (thay luôn vai trò phụ đề — không có phụ đề đáy) |
| Hình giữa | 1 illustration **いらすとや** (PNG nền trong) đặt giữa khung, cỡ nhỏ ~1/3 chiều cao; thi thoảng kèm caption nhỏ ngay dưới hình |
| Nhịp | Đổi hình mỗi **~5 giây**, bám sát từng câu thoại (storyboard 126 khung/10 phút) |
| Âm thanh | Giọng TTS + BGM nhẹ |
| Thumbnail | いらすとや 2 panel trước/sau (khổ→sạch) + mũi tên đỏ + chữ đen to + **ô đỏ ？ che đáp án** |

**Vì sao format này ăn:** hình đổi liên tục theo lời thoại giữ mắt (chống rớt retention kiểu "1 ảnh đứng 30 giây"), いらすとや là ngôn ngữ thị giác quen thuộc với MỌI người Nhật (độ tin + dễ hiểu tức thì), và chi phí sản xuất gần bằng 0 — không quay, không AI-gen, không bản quyền phức tạp.

## 2. Bảng công cụ — map vào đồ CÓ SẴN trong workspace

Toàn bộ khâu đã có tool, KHÔNG cần mua/cài gì mới:

| Khâu | Công cụ | Đường dẫn |
|---|---|---|
| Kịch bản (ngách 生活の知恵) | skill `script-co-dai` — chế độ A rewrite transcript đối thủ / B viết mới, gate 「なぜ効くのか」 | `.claude/skills/script-co-dai/` |
| Kịch bản (ngách khác) | skill `script-viral` (pipeline trend→script tổng quát) hoặc skill của kênh tương ứng | `.claude/skills/script-viral/` |
| Đo trend/keyword | skill `trend-keywords` + luật đo YouTube Search 30 ngày | `.claude/rules/youtube-upload-seo.md` §0.5 |
| Tải hình いらすとや | `fetch_irasutoya.py` — mode tải lẻ: `python tools/fetch_irasutoya.py "検索語" out.png` (scraper qua Blogger JSON feed, tự né ảnh tracker) | `Projects/youtube-jp-nenkin/tools/fetch_irasutoya.py` |
| (thủ công bổ sung) | Search `https://www.irasutoya.com/search?q=<query>`, lấy URL ảnh đổi `/s72-c/` → `/s800/` | skill `video-render` Bước 2 |
| Voice | VOICEVOX (E:\VOICEVOX, port 50021) qua `tts_render.py` — tag nhấn nhá 速/抑揚/間 theo rule humanize | `Projects/youtube-jp-health/tools/tts_render.py` |
| Render video | `video_render.py --channel <key>` — renderer chung, hồ sơ kênh trong `channels.py`; **LUÔN chạy nền** theo rule | `Projects/youtube-jp-health/tools/video_render.py` |
| Slide cast nhân vật (nếu có nhân vật) | `make_cast_slides.py` (nenkin) — vẽ slide nhân vật いらすとや + name-tag | `Projects/youtube-jp-nenkin/tools/make_cast_slides.py` |
| Card số/bảng vẽ tay (tùy chọn) | `make_drawn.py` — bảng/checklist/flow "trông như viết tay" | `Projects/youtube-jp-health/tools/make_drawn.py` |
| CTA giữa video | tự động qua `cta_inject.py` ở cuối render | `.claude/rules/cta-midvideo.md` |
| Thumbnail | Khuôn hỏi→đáp (che đáp án bằng ？ đỏ) — trùng triết lý khuôn sẵn có của co-dai/health | `Projects/youtube-jp-co-dai/02_THUMBNAIL_PROMPTS.md` |
| Đóng gói + upload | `upload_pack.py <slug> --channel <key>` + dashboard | `Projects/youtube-jp-chouhen/tools/upload_pack.py` |

## 3. ⚠️ License いらすとや — điểm sống còn

- Điều khoản irasutoya.com/p/terms: **miễn phí thương mại tối đa 20 hình / 1 sản phẩm (1 video)**. Từ hình thứ 21 phải mua license.
- Video mẫu 10 phút đổi hình 5s/lần ≈ 100+ khung — nhưng họ TÁI DÙNG hình (1 hình xuất hiện nhiều cue). Dù vậy số hình unique của họ nhìn storyboard vẫn có vẻ >20 → đối thủ tự chịu rủi ro đó, **mình không bắt chước điểm này**.
- Cách mình làm sạch: **≤20 hình unique/video**, 1 hình gán vào nhiều cue (đếm theo hình, không theo cue). `make_cast_slides.py` đã có sẵn bộ đếm cảnh báo vượt 20. Credit 概要欄: `イラスト:いらすとや`.
- Hình thiếu (いらすとや không có đúng vật) → fallback ảnh thật Pexels/Commons cắt nền hoặc `make_drawn.py`.

## 4. Gate lớp thủ công vẫn áp

いらすとや là clipart máy tải — **KHÔNG tính là lớp thủ công** theo `.claude/rules/handmade-layer.md`. Video đăng kênh nào thì vẫn theo gate kênh đó (co-dai: `tegami`/`genten`; health: `genten` nguồn thật; hoãn thì ghi `HANDMADE: hoãn`).

## 5. Thiết kế style render mới `shiro` (bản vẽ — CHƯA code, chờ user gật)

Style `card` hiện tại của `video_render.py` là nền navy wa-modern + card trắng — KHÔNG giống video mẫu. Để giống hệt, thêm 1 profile visual (không viết renderer mới):

1. **`make_bg()`** (`video_render.py` ~dòng 282): thêm variant **nền trắng phẳng** — bỏ gradient navy, bỏ 青海波, bỏ vignette, bỏ khung vàng.
2. **`make_slide()`** (~dòng 309): layout mới —
   - **Telop đen to phía TRÊN**: 1–2 dòng, bold, ~70–90px, vùng an toàn 12% mép trên; nội dung = câu thoại của cue (lấy từ dòng TTS khớp `match`).
   - **PNG いらすとや alpha đặt giữa**: nhánh "PNG có alpha → đặt vừa khung trên nền kem" ĐÃ CÓ SẴN trong code — chỉ đổi nền kem → trắng theo profile.
   - Caption nhỏ dưới hình (tùy chọn, field mới `caption` trong SLIDES.json).
3. **Phụ đề**: telop trên đã là lời thoại → 2 phương án khi code: (a) tắt burn phụ đề đáy cho profile này, hoặc (b) thêm `SUB_STYLES["top-telop"]` để pipeline phụ đề hiện có render lên trên. Khuyến nghị (a) — đơn giản, đúng cấu trúc đối thủ.
4. **Nhịp cue**: SLIDES.json dày hơn chuẩn hiện tại (~5–8s/hình thay vì 20–30s) nhưng ≤20 hình unique → nhiều cue trỏ cùng 1 file hình.
5. **Hồ sơ kênh**: khai palette + cờ style trong `channels.py` (cơ chế `PALETTES` theo kênh đã có từ 2026-07-27) — bản sắc render sửa Ở ĐÓ.
6. **Bẫy resume** `.claude/rules/render-background.md` §2.5 áp nguyên: skip-if-exists phải so mtime asset.

Ước lượng công: ~1 buổi code + render 1 demo 2 phút duyệt mắt trước khi chạy video thật.

## 6. Quy trình end-to-end (từng bước)

1. **Đề tài/transcript** → lưu `01_SOURCES/YYYY-MM-DD_<slug>.txt` (nếu rewrite đối thủ), check chống trùng `00_TOPIC_LOG.md`.
2. **Đo trend** YouTube Search 30 ngày (geo=JP, gprop=youtube) — keyword dẫn title phải là TÊN VẬT có volume đo được, bảng điểm ghi vào file script.
3. **Viết script** bằng skill của kênh (`script-co-dai`…) → bản `.md` sạch + `_TTS.md` có tag nhấn nhá + CTA giữa bài; quét `grep -n "。\[\|、\[" <file>_TTS.md` bắt tag lạc giữa câu.
4. **SLIDES.json** cue dày ~5–8s, mỗi entry `match` = mẩu câu thoại + tên hình いらすとや.
5. **Tải hình**: `fetch_irasutoya.py "検索語" slide_XX.png` (≤20 unique) → **contact sheet duyệt bằng mắt** trước render (luật media-library §3).
6. **Demo voice** 1–2 đoạn đắt nhất nghe trước (rule humanize §3).
7. **Render nền**: bọc `.cmd` + log + EXITCODE, `run_in_background` (rule render-background). Xong = EXITCODE=0 + duration khớp srt + duyệt ≥4 frame mắt.
8. **Thumbnail**: khuôn 2 panel trước/sau + ？ đỏ che đáp án; Claude đưa prompt → user gen → duyệt 3 cửa.
9. **Đóng gói**: quét compliance (`youtube-compliance.md`) + gói CTR ghi vào file script (`youtube-upload-seo.md`) → `upload_pack.py` → đăng theo lịch kênh (`upload-schedule.md`) → `--done`.

## Liên hệ

- Hồ sơ đối thủ ライフハック雑学: `Projects/youtube-jp-co-dai/CHANNEL_OPTIMIZE.md` §3
- Luật license/asset: `.claude/rules/media-library.md` · lớp thủ công: `.claude/rules/handmade-layer.md`
- [[project_co_dai_content_upgrade]] · [[feedback_keyword_ten_vat_khong_khai_niem]]
