# CLAUDE.md — youtube-jp-co-dai (rút gọn 08-24)

## ① Identity
- Kênh **古代の秘訣** — ngách 生活の知恵・忘れられた技術, giọng phim tài liệu NHK. Tệp: JP 45–70, xem tối như nghe radio → script đứng được chỉ bằng âm thanh.
- **Độ dài chuẩn 25′.** Hệ số CÓ TAG (mặc định): 20′ ≈ 6.100 ký · 25′ ≈ 7.650 (305,4 ký/phút; không tag = 337,5). Tag ăn ~10% độ dài — sửa bằng viết ít ký, KHÔNG bỏ tag. Chế độ A giữ ×0,9–1,1 thời lượng gốc.
- **categoryId 27 (Education)** — ô mặc định Studio để 「Giáo dục」; 10 video cũ cat 22 GIỮ NGUYÊN.
- Format: ảnh thật + **lớp vox** (`make_vox.py --channel co-dai`, ảnh làm NỀN annotate đè) + **lớp chuyển động bằng hình `make_shot.py`** (soft/inset/focus/wipe — khung đứng yên, ⛔ không pan/zoom/Ken Burns). Vai theo ẢNH: macro → focus, cảnh → inset, ~1/3 entry cảnh để soft.

## ② Sản xuất
- Giọng: **VOICEVOX 青山龍星 / ノーマル / speed 0.9 / intonation 1.15**, port 50021 (KHÔNG có style 落ち着き).
- ⭐⭐ **TỪ VIDEO 25 (user chốt 2026-08-27: *"render theo dạng video mới nhất của nenkin"*): DỰNG BẰNG REMOTION theo khuôn nenkin** (`youtube-jp-nenkin/CLAUDE.md` §② QUY TRÌNH CHUẨN — đọc đó cho hằng số/luật, đừng dò lại). ⛔ Bỏ `make_vox` + `make_shot` + `video_render` cho lớp hình. Khung: 2 cast **ảnh thật cắt nền** của co-dai (`_media_library/avatars/co-dai/_cut/`, builder tự crop bbox + đo ratio) · hero photocard 1.132px · sticker 2 góc trên (ảnh) / làn phải bảng (stat) · chữ `papercut-banner` · số liệu `papercut-stat`/`-formula` (thay hết thẻ vox bar/stat/compare/process/source/timeline).
  ```
  ① check_coldopen.py NN → ② voice_only.py (voice.wav + subs.srt + timeline.json — đã có tool)
  ③ copy tools/build_remotion_25.py → build_remotion_NN.py, sửa SCENES/PUNCH/STAT (neo L=chỉ số dòng timeline)
  ④ python tools/art_prompts_collage25.py + sticker_prompts_collage25.py  ← đọc SCENES của builder, KHÔNG chép tay
  ⑤ user gen → make_photocard25.py --src … --apply · cutout_sticker25.py --src … --apply (điền MAP)
  ⑥ python tools/build_remotion_NN.py → 0 🔴 (gate: scene ≥6s · bảng≠hero · PUNCH có trong lời · sticker không lọt/đè · phụ đề ≤66 ký · asset đủ)
  ⑦ still ≥10 frame: npx remotion still VoxProject --props=projects/co-dai-NN/project.json --frame=N out/x.png
  ⑧ render nền: remotion-vox/run_cNN.cmd (có `call npx`) → soi frame ~10% + duration khớp
  ```
  ⭐ **STYLE = ANIME, KHÔNG cắt giấy** (user chốt cùng ngày: *"tao muốn dùng dạng anime"*): ảnh hero + sticker gen anime. ⭐ **KHÔNG CAST 2 mép** (user chốt 2026-08-28 phương án C: *"đỡ sử dụng lặp lại nội dung"* — 2 người đứng y hệt 47/47 scene và lặp qua mọi video): 2 dải bên thành **4 ô sticker** (2 mỗi bên, 4 cái sống cùng lúc), bảng số căn giữa khung phóng ×1,3. Hero vẫn 1.132px (trần theo CHIỀU CAO, không phải do cast). 5 cast anime đã gen (`06_VIDEO/25/cast/`) giữ làm kho, không dùng; chữ dùng preset `tag`/`punch` + bảng `flat-stat` (thêm mới vào remotion-vox, không đụng papercut của nenkin); nền phẳng kem, không vân giấy; hero bo viền trắng tròn (không giấy xé/tape/xoay). Khác nenkin còn: phụ đề **cỡ 48, trần 66 ký/khối**. Không tái dùng sticker giấy của nenkin. Probe khung khi chưa có cast anime: `--photo-cast`. ⚠️ Remotion KHÔNG tự làm watermark kênh + CTA overlay (bài học shokutaku) — nenkin cũng chưa làm, chờ user quyết có bù không.
- ⭐⭐ **TỪ VIDEO 31 — LỚP HÌNH THEO SỐ ĐO CỦA ĐỐI THỦ ĐANG THẮNG NGÁCH** (bóc 7 video 昔の人の知恵 ngày 2026-09-06, bằng chứng `01_SOURCES/PEER_ANATOMY_2026-09.md` + `04_FORMULA.md` §6b; tool `tools/analyze_peer.py`). Kênh đó **90 ngày → 2,35 triệu view**, và lớp hình của nó là một chữ ký đo được, **7/7 video không ngoại lệ**:
  - 🔴 **TRẦN 9,7 GIÂY/CẢNH, không chỗ nào được đứng hình lâu hơn** — họ chạy **7,43–7,53 cắt/phút**, hold trung vị **8,0s**, cảnh dài nhất cả bài chỉ 8,1–9,7s, **kể cả video 52 phút**; 60 giây đầu có **7–8 cắt**. ⇒ Số ảnh/clip nhắm lúc thiết kế: `⌈giây_video ÷ 8,5⌉` (18′ ≈ 127 · 25′ ≈ 177). ⚠️ Đây là **trần cứng theo CẢNH**, khác với trần "≤6 đổi hình/phút" của `audience-45plus.md` §2 — xem ngoại lệ đã ghi ở rule đó; **chỉ áp cho co-dai**, kênh khác chưa có số của ngách mình.
  - 🔴 **0 thẻ chữ / 0 bảng số.** Số liệu đi bằng **lời + phụ đề**; hình LUÔN là **cảnh thật của chính cái vật đang nói** (ống nước cắt đôi, macro dầu đông trong ống, tay thao tác). ⇒ Bỏ dần `flat-stat`/bảng số của khuôn Remotion 25–30; giữ `punch`/`tag` ở mức tối thiểu.
  - **Phụ đề 1 dòng ~10–14 ký** (co-dai đang 48px/trần 66 ký — siết xuống). **Watermark góc TRÊN-TRÁI** (đang để trên-phải).
  - Thủ pháp đáng lấy: **collage 4–6 ô** so sánh nhiều trạng thái cùng lúc (họ dùng ở khối so sánh).
  - ⚠️ **Video ≤30 GIỮ NGUYÊN** (video 30 đã có 105 clip gen sẵn ≈ 5,9 đổi/phút) — đổi giữa chừng là bắt gen lại cả lô, không đáng.
  - ⚠️ **Cái này KHÔNG chứng minh giữ chân.** Nó là chữ ký sản xuất của kênh đang thắng, đo từ file video; không ai có retention của họ. Áp vì nó rẻ và nhất quán, không vì đã chứng minh nhân quả.
- *(Đường CŨ, chỉ tra cứu cho video ≤24)* **Dựng theo `09_VIDEO_PIPELINE.md`** — 9 bước: `check_coldopen` → `voice_only` → `gen_slidesNN` → duyệt `--still` → user gen ảnh → `placeNN` + `strip_wm_crop` → `autofocus` → `add_fx` → dựng clip → `video_render --reuse --channel co-dai`. Bẫy: autofocus/add_fx SAU ảnh+voice · chạy lại gen_slides là XOÁ kết quả chúng · **dựng demo 90–120s trước bản đầy đủ**.
- Lớp hình: SLIDES → check_vox → preview TỪNG FRAME → USER DUYỆT → mới xuất prompt ảnh. Ảnh thẻ vox phải MACRO. ✦: đo bằng MẮT rồi CẮT (`strip_wm_crop.py`, backup `_wm_orig/`).
- **Gate máy:** ① `python tools\check_coldopen.py <NN>` — cửa sổ **giây 0–45** (trần ≤75s cũ đã chết), đọc header `TARGET_QUERY:` + `INTENT:`; intent nhóm ⛔ hoặc thiếu = FAIL → BỎ SLOT. **O17** (09-06): thiếu header 3 dòng `# FORMULA/# SELFCHECK/# CONFESS` hoặc `stake`/`frame` ngoài enum = FAIL. **O15 hạ WARN** (tạo động cơ nhồi — bị flag thì CẮT, cấm chèn số). **O6 nay chấm bằng 8 ĐỒNG TIỀN** (09-06): ⑥ CẢNH · **⑦ HẬU QUẢ** (命/奪う/壊れ/修理費) · **⑧ SO SÁNH** (よりも多い/合わせた/倍以上) nâng từ WARN lên FAIL — gate 5 đồng tiền cũ chấm HIT 蚊 499.000 view của đối thủ là 7/9 câu không trả tiền, tức đánh trượt video nửa triệu view; hiệu chuẩn sau khi nới vẫn giữ 02 (2 câu) trên 07 (6 câu) và 0 script co-dai đổi trạng thái. WARN còn lại: O18 (dòng tiền 70–82%) · O19 (`冒頭で` lặp). ② `check_vox.py <SLIDES> --channel co-dai --tts <TTS>`. ③ CTA: grep `高評価` trong `_TTS.md` — thiếu thì bổ sung trước synth (canonical `cta-midvideo.md` §2.4, ranh giới chương ~50%).
- ⛔ `tools/make_vox_codai.py` LẠC HẬU — chỉ dùng `_media_library/make_vox.py`. mp4 = số entry `video:true` trước render. `.cmd` ASCII-only. Clip trung gian ~1,5 GB — `--done` dọn.
- TTS: số Ả Rập (500円) · acronym → katakana · kanji khó → kana · hạn chế 「――」「…」.

## ③ Luật riêng còn hiệu lực
- **Lời hứa:** 「昔の人の知恵で、今の困りごとを根本から解決する」. **GATE CONTENT:** mỗi mẹo trả lời 「なぜ効くのか」 kèm cơ chế/lịch sử/nguồn thật — chỉ liệt kê = KHÔNG đạt.
- **Luật trục** (8 trục, `02_CONTENT_STRATEGY.md`): video kế KHÁC trục liền trước · 害虫 ≤ ~1/4 · ~4 video 1 lần trục 忘れられた技術 · đề mùa vụ đăng đúng mùa.
- **Tiền: mọi số là 円 viết thẳng** — cấm 「日本円にして」/ドル; số Mỹ localize ra 円 (giữ アメリカでは).
- **YMYL/nguồn:** chế độ A rewrite 100%, không chuỗi ≥7 chữ trùng gốc; fact/nguồn/năm GIỮ NGUYÊN — bịa nguồn = chết kênh; DIY/hóa chất có đoạn an toàn; claim chưa kiểm chứng → 「歴史的な記録によれば」; chạm y tế → 「医師にご相談ください」; không cáo buộc đích danh.
- **Credit giọng: KHÔNG ghi VOICEVOX trong 概要欄** (ngoại lệ compliance §2; sạch license → pinned comment, user quyết).
- **Title:** vế DẪN = câu hỏi `なぜ` hoặc LỆNH CẤM cụ thể (`絶対に〜してはいけないNつ`), `数百円` là vế phụ sau 「――」. Keyword dẫn = **TÊN VẬT có volume đo được** (khái niệm ~0 cầu — phải đo). **Intent:** ✅ `最強/なぜ/やり方/順番/比較` · ⛔ `効果/意味ある/thủ pháp hẹp` — nhóm ⛔ giữ làm tag, cấm lên title.
- **Metadata:** rổ 12 tag cố định đứng đầu (`古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損`) + tag riêng, tổng ~25–35 · 3 hashtag `#生活の知恵 #昔の知恵 #古代の秘訣` CUỐI desc · desc 800–1.800 ký (hook → 目次 → topical → disclaimer) · srt tự upload.
- **Thumbnail:** CONCEPT-DIAGRAM — nền PHẲNG, [vấn đề] → mũi tên đỏ → [giải pháp], text 1 dòng 5–7 ký ≥1/3 khung, LUÔN badge giá tiền (数百円/0円). Claude chỉ ĐƯA PROMPT, user gen, duyệt 3 cửa + 120px. Spec + 8 khuôn xoay vòng: `02_THUMBNAIL_PROMPTS.md`.
- **Retention:** mục tiêu AVD 60% — cửa tử giây 15→45; @45s ≥85% · sàn thân bài ≥55%. Cắt ngắn KHÔNG mua được 60% — giữ 25′. Đọc bằng relPerf 15–45s, không bằng view. CTR kênh ĐÃ ĐẠT — đừng đổ công thumbnail; biến chính là INTENT query search.
- Lịch: **T2·T4·T6 13:00 JST, 3/tuần** (giờ ĐỔI 11:00 → 13:00 ngày 2026-08-26 THEO SỐ ĐO: 昔の人の知恵 có 13h thắng 11h 4,7×, tuổi video chạy ngược nên không phải artifact — `upload-schedule-measure-hours-2026-08-26.md`; ⚠️ n=4 nên mỏng, 🛑 phanh 10 video → về 11:00 (n=27)) (`upload-schedule.md` §0.9). Fail gate → BỎ SLOT, không đăng bù.
- Lưu file: nguồn A + log đề tài → `01_SOURCES/` · script `03_SCRIPTS/<NN>_<slug>.md` + `_TTS.md` (header: chế độ, nguồn, độ dài, ngày) · voice `05_VOICE/` · render `06_VIDEO/`.

## ④ Trỏ
- Skill: `script-co-dai` (chế độ A·REWRITE / B·VIẾT MỚI, checklist 13 điểm) · `video-vox` · `video-render`.
- ⭐ **`04_FORMULA.md` — THỨ TỰ VIẾT kịch bản (đọc TRƯỚC skill)**: 8 ô quyết định trước khi viết chữ nào · 8 bước viết · 3 câu tự hỏi → header `# FORMULA/# SELFCHECK/# CONFESS` (gate O17) · sổ hiệu lực §7. Chốt 2026-09-06 sau 7 video liên tiếp gate PASS 10/10 mà v1 vẫn bị trả.
- Doc project: `02_CONTENT_STRATEGY.md` · `02_THUMBNAIL_PROMPTS.md` · `09_VIDEO_PIPELINE.md` · `08_ANALYTICS_LOG.md` (§6 sổ retention, tool `tools/pull_retention.py`) · `01_SOURCES/00_TOPIC_LOG.md`.
- Rules toàn cục `.claude/rules/`: youtube-compliance · audience-45plus · humanize-script-voice · media-library · render-background · upload-schedule · youtube-upload-seo · ab-3title-3thumb · cta-midvideo · youtube-suggested-growth. Vault: `SecondBrain\10_Projects\youtube-jp-co-dai\`.

> Bản đầy đủ: ./_archive/CLAUDE_FULL_2026-08-24.md · Doc cũ khác cũng ở ./_archive/
