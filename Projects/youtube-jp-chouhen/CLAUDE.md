# CLAUDE.md — youtube-jp-chouhen

Kênh **真夜中の朗読便** (key `chouhen`) — faceless **AI朗読 / スカッと系・長編朗読ドラマ**, thị trường JP. Khán giả: **nữ 45–70, NGHE không nhìn màn hình** → nhắc lại tên + vai vế nhân vật định kỳ. POV mặc định nữ 「私」 (nam 「俺」). Premise: ưu tiên **A·REMAKE từ premise proven-viral** (đổi ≥8/10 yếu tố + rewrite 100%, không trùng ≥25 ký). Đăng **4/tuần T2·T4·T6·CN 12:00 JST** (giờ ĐỔI 09:00 → 12:00 ngày 2026-08-26 THEO SỐ ĐO: winner ngách 嫁子 khoá 12h ở 41/50 video, và 12h thắng 18h của chính nó 1,65× với tuổi video khớp — `upload-schedule-measure-hours-2026-08-26.md`; 🛑 phanh 10 video → về 09:00) — không hàng qua gate thì BỎ SLOT.

## Độ dài & retention (LUẬT PHÚT)
- Độ dài = **11′ mở (CỐ ĐỊNH) + 3,5′×N sóng + 3′ kết** (N=4 ≈ 28′ = vùng đã chứng minh; mỗi sóng = một kẻ trả giá 逆転Ⓝ). Nhắm AVD >60%: `8′+3,5′×N+2′30` (24–26′, bỏ 回想).
- **Gate máy: `python tools/check_retention.py <slug>`** — 4 cửa cứng: **R3b** giây 16–35 ĐÚNG 0 câu LỜI KỂ ≥25 ký · **R7** gap 2 beat ≤2′45″ · **R8** SÓNG 1 ≤ phút 12 · **R11** loop cold open đóng ở ≥78% thời lượng.
- Cold open theo GIÂY: giấy tờ gọi tên ≤10s · anomaly ≤25s · liệt kê ≤60s · phản đòn ≤80s. 回想 ≤2′30, xong trước phút 11. Mở bài cấm lời chào/lai lịch/tả cảnh dài.
- 🛑 3 video liên tiếp AVD ≤28% → hạ về N=4–5. View do BAO BÌ + SỐ VÉ, không do retention.
- Ước độ dài: `tools/calib_duration.py` (±4%); ước thô 260 ký/phút (KHÔNG 300); **chốt CHỈ bằng `ffprobe voice.wav`**.

## Script — luật riêng
- Khung 9 nhịp: skill `script-chouhen` (MỤC 10 + 14). Thân bài: số bằng **漢数字**; title/thumbnail được số Ả Rập.
- ⭐⭐ **XOAY KHUÔN 5 TRỤC — BẮT BUỘC, chạy TRƯỚC khi viết một chữ** (user 2026-08-29: *"kịch bản giống nhau đến 90%, mở lên là biết mô típ"*). Đo máy 27 script: sân khấu 儀式 6/8 bài gần nhất · kẻ ác 家族 25/27 · vật chứng 紙 **27/27** · cơ chế 供給停止 ~24/27 · cấu trúc 直線+回想 27/27. Luật + menu 5 trục: skill `script-chouhen` **MỤC 11B**. Gate: `python tools/check_variety.py --table` (chọn khuôn) rồi `check_variety.py <slug>` (chặn cứng). Header script phải có dòng `- **Trục 5T:** T1=… · T2=… · T3=… · T4=… · T5=…`. 🔴 MỤC 11 (bảng 10 yếu tố) chỉ ép đổi CHI TIẾT — nó là lý do kênh trượt về cùng mô-típ suốt 27 video; 11B ép đổi LOẠI TRUYỆN. Hai tầng, không thay nhau.
- 🔧 **`check_retention.py` R2 đã mở nhóm vật chứng PHI-GIẤY** (2026-08-29): 5 lần bổ sung trước đều là "thêm một tờ giấy", khiến R2 — một gate CHẶN — trên thực tế **cưỡng chế mọi bài phải có giấy trong 10 giây đầu**. Nay nhận 録音/レコーダー/防犯カメラ/ベル/反射板/傷跡/点字… Keyword chọn bằng số đo (≤9/28 script cũ); **cấm thêm** 声・音・匂い (28/28, 28/28, 21/28) vì R2 sẽ luôn xanh = gate chết.
- ⛔ **CẤM đếm 1,2,3 trong LỜI KỂ** (khối loop = MỘT câu, 2 tag/khối) — gate: `python Projects/_media_library/check_enum.py <x>_TTS.md` (ngoại lệ: bản án trong 「」).
- Dòng TTS ≤40 ký; câu CTA giữa video (NHỊP 4→5) tách 2–3 dòng TTS.
- Header script ghi: chế độ A/B · nguồn REMAKE · VOICE ARM · nhân vật (không lặp video khác).

## Voice
- **A (mặc định):** AivisSpeech port **10101** — nữ `morioki` (497929760) · nam `阿井田 茂` Calm (1310138977) · speed **1.0**. Credit 概要欄: `AivisSpeech: morioki`.
- **B (A/B):** VOICEVOX :50021 `青山龍星`/ノーマル · speed **0.80** · 抑揚 **1.15** — BẮT BUỘC credit `VOICEVOX:青山龍星`. Wrapper: `python tools/run_voiceab.py <x>_TTS.md [A_morioki|B80_aoyama]`.
- Đọc A/B bằng **AVD% + retention@2′54″** (≥3 video/nhánh xen kẽ, KHÔNG bằng view); log `06_VIDEO/_voice_ab/AB_LOG.md`.

## Render (chạy NỀN qua wrapper `.cmd` — rule `render-background.md`)
```
python tools/tts_prefetch.py 03_SCRIPTS/<x>_TTS.md --engine voicevox --speaker 青山龍星 --speed 0.80 --intonation 1.15 --jobs 4  # nhánh B
python tools/ambient_render.py 03_SCRIPTS/<x>_TTS.md --engine aivis --speaker morioki --speed 1.0 --voice-only
python tools/pick_bg20.py --slug <x> -n 20 --per-theme 2       # 20 clip KHÔNG NGƯỜI → bg_list.txt (seed=số video, đừng hardcode)
python tools/check_bg_lum.py <x> --bg-only 06_VIDEO/<x>/bg_list.txt   # gate tương phản std ≥12
python tools/scene_render.py <x> --stage segs --frame radio --bg-only 06_VIDEO/<x>/bg_list.txt
python tools/pick_bg20.py --slug <x> --verify --min-gap 4      # gate lặp cách ≥4 cảnh
python tools/scene_render.py <x> --stage parts
python tools/scene_render.py <x> --stage final                 # + CTA overlay tự động
```
- 🔴 **`--frame radio` BẮT BUỘC mọi video mới** (chép wrapper video ≥29). Phụ đề radio: chữ xanh #48AAFF, cỡ 48, outline.
- Hình nền: clip lệch tông/lộ mặt đã render → CHO QUA. Chỉ render lại khi **HỎNG THẬT** (mất tiếng · lệch sub · thiếu part · exit≠0 · duration lệch srt).
- BGM `--bgm auto` (7 track, −40dB): GIỮ. FX.json + ambience bed: tuỳ chọn. Speaker tên Nhật → gọi qua wrapper `.py`.

## Đóng gói
- `python tools/upload_pack.py <slug> [--open]` → `_upload/`; đăng xong `--done`.
- **SEO NHẸ (chỉ chouhen):** desc ~300 ký = hook + `※この物語はフィクションです…` + credit giọng + 3 hashtag · 0–8 tag · bỏ 目次. 🔴 Disclaimer & credit giọng CẤM cắt (compliance/license).
- **Title: câu văn trần 60–90 ký, KHÔNG mở bằng 【】** — `[tình huống + hành vi ác]。[だが…cú lật]――｜スカッとする話｜修羅場` (keyword ở đuôi). Tình tiết phải CÓ THẬT; không backfill title cũ.
- **Thumbnail:** bộ 3 T1/T2/T3. Khuôn **K1 text-wall + dàn người / K2 cảnh sáng kể chuyện** — `tools/make_thumb_textwall.py --preset k1|k2` (đường lui `--preset m08`); prompt AI bake chữ; **≥2 nhân vật biểu cảm đang diễn + ≥1 vật chứng**; huy hiệu `--mark --mark-style circle` góc trên-phải; duyệt 168px + 120px.

## Trỏ chi tiết
- Script 9 nhịp: skill `script-chouhen` · Thumbnail/title CTR: skill `thumbnail-chouhen` · Retention: `RETENTION_FORMULA_2026-08-11.md` · Nguồn REMAKE + swipe: `01_SOURCES/` (`SWIPE_TITLES.md`) · Vault: `SecondBrain/10_Projects/youtube-jp-chouhen/`
- Rule toàn cục `.claude/rules/`: youtube-compliance · audience-45plus · humanize-script-voice §1.2 · media-library · render-background · youtube-upload-seo §5 · ab-3title-3thumb · upload-schedule · cta-midvideo · youtube-suggested-growth

> Bản đầy đủ (lịch sử quyết định + bằng chứng số đo): ./_archive/CLAUDE_FULL_2026-08-24.md · Doc cũ khác cũng ở ./_archive/
