# CLAUDE.md — youtube-jp-yawa

Kênh **人生哲学の夜話** (key `yawa`) — faceless **朗読 + 人生の話** (triết lý sống đời thường), thị trường JP.
**REBRAND từ kênh 真夜中の朗読便 (chouhen)** — user chốt phương án ② ngày 2026-09-28: cùng kênh, đổi tên/banner/logo, 34 video スカッと cũ chuyển 限定公開 (KHÔNG xoá).

- channelId: `UCuzbgcFHVmAf4O6wU1wLyIQ` (giữ nguyên) · Gmail `tuananh96freemail@gmail.com` · Chrome profile `Default`
- Mốc gốc lúc rebrand (API 2026-09-28): **34 video · 1.413 view · 4 sub** ⇒ kênh gần như không có tài sản để mất.
- Project cũ `Projects/youtube-jp-chouhen/` GIỮ NGUYÊN (có tool dùng chung: `upload_pack.py`, `scene_render.py`, `pick_bg20.py`…).

### Tên kênh — vì sao 人生哲学の夜話 (2026-09-28)
User muốn tên "thiên triết lý". Đã dò `search.list type=channel` 24 tên: trùng/gần trùng `人生の余白ラジオ` (có kênh thật) · 人生のしおり · 縁側ラジオ · 寝る前の人生の話 · 人生の灯り朗読館 · 眠れる偉人の哲学 · 真夜中の哲学書斎 · 人生の哲学. `人生哲学の夜話` không đụng kênh nào.
⚠️ Ngách ĐÔNG (人生の哲学 · 眠れる偉人の哲学 · 睡眠哲学朗読室 · 眠れない夜の哲学 · 心に刻みたい人生哲学のはなし) ⇒ có khán giả, và cũng là danh sách benchmark đầu tiên.

## Khán giả
Nữ + nam **50–70**, **NGHE không nhìn** (trước khi ngủ · làm việc nhà) — kế thừa tệp chouhen. Nhịp chậm, giọng một style, không nhạc dồn.

## Keyword — đo Trends gprop=youtube 30 ngày, JP (2026-09-28)
| từ | điểm (thang 人生) | intent | kết luận |
|---|---|---|---|
| **人生** | 92 | top related: **人生相談**(100) · テレフォン人生相談 | ✅ keyword dẫn — đầu tên kênh + đầu title |
| **朗読** | ~50 | 小説朗読 · 睡眠導入 · 眠れる朗読 | ✅ keyword phụ (định dạng) |
| 睡眠 | cao | ngủ | ✅ dùng ở hashtag/desc |
| **哲学** | cao (74 trong rổ nhỏ) | — | ✅ keyword thứ hai — trong tên kênh |
| 人生哲学 (cụm ghép) | 0,5 | — | ❌ đừng viết dính; để 人生 và 哲学 tách |
| 名言 | ~50 | **アニメ名言** · ワンピース | ❌ SAI intent — không đặt vào title |
| 聞き流し | cao | **英語** | ❌ SAI intent |
| 生き方 · 哲学 · ブッダ · 老後の生き方 · 人生の教訓 | ≈0–9 | — | ❌ volume ~0 |
Đo lại trước mỗi lô 5 video (`youtube-upload-seo.md` §0.5).

## Nội dung — khuôn v3 LIỆT KÊ (user chốt 2026-09-29)
- **Khuôn:** `05_SCRIPT_FORMULA.md` **v3** · skill `script-yawa` · bản mẫu `03_SCRIPTS/01_danshari-kokoro_TTS.md` (v5) · bằng chứng `01_SOURCES/HOT_FORMULA_2026-09-29.md` (1.077 video ≤30 ngày).
- Một câu: **nói với あなた suốt bài: khoảnh khắc người nghe đang sống + gỡ tội → その一…その七 (mô tả · vì sao · góc khác · làm ngay) → câu chuyện chốt của một người quen + câu 古典 thật.** Mục 1 ≤2:00. User: *"tao muốn liệt kê như kịch bản [ブッダの教え mẫu]"* — ⛔ không quay lại khuôn truyện xuyên bài.
- Vì sao bỏ khung cũ (古典 làm xương sống): kênh đọc 古典 賢者の朗読 có 19,4K sub mà chỉ **64 view/ngày**; khuôn truyện + list của シニアの人生寄り添い物語 được **886 view/ngày** (median 14,5K view/video).
- 18–22′ · categoryId 22 · một giọng · ⛔ đề sức khoẻ/ăn uống/thuốc · ⛔ số chế độ tiền · ⛔ funnel LINE.
- ⛔ **Danh ngôn phải có nguồn kiểm được** (bảng `### 古典ソース` + link 青空文庫). ⛔ Không slideshow đọc danh ngôn. Không persona thầy/chuyên gia.
- Nhịp đăng: **3 video/tuần T2·T4·T6 18:15 JST** (user chốt 2026-09-30, `.claude/rules/upload-schedule.md` §1.2b); 3 video thử đầu → đọc tỉ lệ video dẫn RELATED cùng ngách (`youtube-suggested-growth.md` §1.5).
- ✅ user chốt 2026-09-29: **lớp hình ANIME** (ngoại lệ riêng yawa) · **KHÔNG CTA giữa bài** · mũi ① đi qua người dẫn đường. Người kể = clip anime che mặt ở góc dưới-phải: **`09_BRAND/narrator/narrator_B_full.webm`** (trọn người nhìn 3/4 sau lưng, VP9 alpha, lặp 19,9s, cao ~360–420px sát đáy, cách mép phải ~30px; bản cắt cằm cũ `narrator_A_cutout.webm` bỏ vì user chê "mất đầu"; tool `tools/cut_narrator.py`; nghiệm thu ở `09_BRAND/narrator_prompts_TENFILE.txt`).

## Tài sản tái dùng từ chouhen
Giọng AivisSpeech `morioki` (credit `AivisSpeech: morioki`) · `--frame radio` · `scene_render.py` · `pick_bg20.py` · BGM −40 dB.
⛔ Không dùng: skill `script-chouhen` · `check_retention.py` · khuôn title 修羅場 · thumbnail dàn người.

## Dựng video (từ bài 1, 2026-09-29)
- Hồ sơ renderer: `Projects/youtube-jp-health/tools/channels.py` key **`yawa`** — giọng **東北イタコ 0.90** (user chọn sau 7 demo `06_VIDEO/01_danshari-kokoro/demo_voice/`; ⚠️ trùng giọng chính của showa — user biết và vẫn giữ, 2026-09-29) · phụ đề outline 22 · ảnh ĐỨNG YÊN (`motion: False`) · 30 fps · BGM tạm −40 dB.
- Luồng: `_TTS.md` → `video_render.py --channel yawa --slides-only` (render giọng + `timeline.json`) → sinh SLIDES theo timeline THẬT (match = đoạn đầu ngắn nhất trỏ đúng dòng — renderer đổi chữ đọc, vd 方→かた) → `tools/make_cards.py <stem>` vẽ thẻ chương/古典/thư + dựng clip **chữ hiện dần** (`reveal`) → **ảnh/video THẬT trước** (`tools/fetch_real.py` → soi sheet → `_plan/picks.py` → `tools/pick_real.py`, user 2026-09-30) → ô còn thiếu mới gen ảnh anime (khớp câu, KHÔNG cần đồng nhất nhân vật) theo `06_VIDEO/<stem>/_plan/img_prompts_FLOW.txt` → xoá ✦ → `slides_img/slide_NN.png` → render.
- ⛔ Đừng dùng card chữ của `video_render.py` cho yawa (không xuống dòng → tràn khung, soi 2026-09-29).
- ⏳ Người kể góc dưới-phải (`09_BRAND/narrator/narrator_B_full.webm`) chưa có trong renderer — cần bước overlay sau render.

## Bộ nhận diện
- File gốc: `00_BRAND/` (logo 800×800, banner 2560×1440, safe area 1546×423 giữa). Tool dựng: `tools/make_brand.py`.
- Tầng kênh (mô tả, keywords, hashtag cố định): `00_BRAND/CHANNEL_SETUP.md`.

## Trạng thái setup kênh (2026-09-28, xác nhận bằng API read)
✅ Tên `人生哲学の夜話` · handle `@jinsei-tetsugaku-yawa` · logo · banner · mô tả · 24 keywords · mặc định upload sạch (tag trống).
✅ 34 video スカッと → **限定公開** (Studio sửa hàng loạt, lọc chỉ video Công khai để không đụng video riêng tư/nháp; API xác nhận 34/34 unlisted). Danh sách gốc: `00_BRAND/old_videos_before_rebrand.json`.
⚠️ API `videos.update` trả **403 Forbidden** với token này (app chưa được quyền sửa video) ⇒ mọi sửa metadata video phải đi Studio.
Tag cũ スカッと vẫn còn trên 33/34 video (đã ẩn nên gần như vô hại) — ⛔ KHÔNG thay bằng tag triết lý (metadata sai nội dung, `youtube-compliance.md` §4).

## Việc mở
- ✅ 2026-09-29 mổ kênh thắng → `05_SCRIPT_FORMULA.md` v1 + skill `script-yawa`. 3 việc chờ đã chốt 2026-09-29
- ✅ 2026-09-30 key `yawa` đã có trong `upload_pack.py` CHANNELS + `browser_profiles.json` + dashboard (`projects.json`, `channels_state.json`)
- ⏳ Sửa `analytics_report.py` (`mine=True` trả rỗng với token này → gọi theo channel ID)

Vault: `SecondBrain/10_Projects/youtube-jp-yawa/`
