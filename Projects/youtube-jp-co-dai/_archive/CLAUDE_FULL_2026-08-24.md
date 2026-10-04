# CLAUDE.md — youtube-jp-co-dai

Project: kênh faceless **生活の知恵・忘れられた技術** (mẹo đời sống + kỹ thuật bị lãng quên, giọng phim tài liệu NHK) thị trường Nhật.

## Bối cảnh

- **Tên kênh: 古代の秘訣** — dùng trong câu chào/câu kết cố định (xem skill).
- Thị trường đích: **Nhật** (geo=JP, hl=ja). Mọi tiêu đề/keyword viết **tiếng Nhật**; trao đổi với user bằng tiếng Việt.
- Khán giả: **Nhật 45–70 tuổi**, có nhà riêng/家庭菜園, tiết kiệm, cảnh giác hóa chất & quảng cáo doanh nghiệp lớn, hoài niệm 昔の暮らし. Xem 20–40 phút buổi tối **như nghe radio** → kịch bản phải đứng được chỉ bằng âm thanh.
- **Độ dài chuẩn: mặc định 25 phút → 7.500–8.200 ký tự** (lý thuyết 300–330 ký/phút — CHƯA đo trên giọng thật, xem ô C dưới). Chế độ A giữ thời lượng gần bản gốc (×0,9–1,1). Chia batch ~5.000 ký tự/lượt, dừng ở ranh giới chương.
- KHÁC kênh health (15–20 phút, YMYL) và chouhen/sukatto (truyện 朗読) — **đừng lẫn chuẩn**.

## 🎯 ĐỊNH VỊ & TRỤC ĐỀ TÀI (content là vua — chốt 2026-07-24)

> Nguồn ma trận đề tài + 8–10 đề đầu + bằng chứng cầu: **`02_CONTENT_STRATEGY.md`** (nguồn sự thật). Mục này là bản rút gọn bắt buộc tuân.

- **Lời hứa kênh:**「昔の人の知恵で、今の困りごとを根本から解決する」. Công thức mỗi video = **(nỗi đau hiện đại có cầu proven) × (lời giải「昔はどうしていたか + なぜ効くのか」)**. Cùng từ khoá đối thủ, sâu gấp đôi.
- **Luật trục (chống đóng khung — bệnh 5 video đầu dồn hết vào 害虫):**
  1. Video kế tiếp **KHÁC trục video liền trước** (8 trục ở `02_CONTENT_STRATEGY.md`).
  2. **害虫 ≤ ~1/4 tổng** — không để côn trùng chiếm sóng.
  3. **~4 video 1 lần trục signature 🔥 忘れられた技術** (giữ bản sắc 古代の秘訣).
  4. Ưu tiên đề có bằng chứng cầu (`CHANNEL_OPTIMIZE.md` 3.5); đề mùa vụ đăng đúng mùa.
- **⭐ GATE CONTENT (bắt buộc, là "chất" của kênh):** mỗi mẹo/chương phải trả lời **「なぜ効くのか」** kèm cơ chế khoa học / lịch sử người xưa / nguồn thật. Chỉ liệt kê "làm thế này là xong" = KHÔNG đạt, đó là AI-slop → mất moat + dính inauthentic. Skill `script-co-dai` MỤC 10 + checklist MỤC 14 enforce.
- **KHÔNG đụng khi nâng cấp:** voice, độ dài/hệ số ô C, tiền yen, thumbnail, metadata 📐 — giữ nguyên bên dưới.

## Voice (VOICEVOX)

- Engine: **VOICEVOX**, port **50021** (cùng engine kênh health, KHÔNG phải AivisSpeech 10101 của chouhen).
- **Speaker CHỐT (2026-07-13): 青山龍星, style ノーマル, speed 0.9, intonation 1.15.** ⚠️ 青山龍星 KHÔNG có style 落ち着き (từng chọn nhầm). Style hợp lệ: ノーマル・熱血・不機嫌・喜び・しっとり・かなしみ・囁き. Chọn ノーマル để điềm tĩnh + gravitas tài liệu, lệch khỏi shokutaku (しっとり/0.8). Credit 概要欄: "VOICEVOX:青山龍星".

## 💴 Đơn vị tiền (BẮT BUỘC)
Kênh cho khán giả Nhật → **mọi con số tiền là yen (円) bản địa, viết thẳng**. KHÔNG framing quy đổi 「日本円にして…」, KHÔNG ドル/USD/đồng/ngoại tệ. Số liệu Mỹ (thị trường/thiệt hại) → localize thẳng ra 円 (vẫn nêu ngữ cảnh "アメリカでは…" cho rõ là số Mỹ).
- Kịch bản tối ưu TTS: số chữ số Ả Rập (500円, 1934年), acronym → katakana (NASA→ナサ, EPA→イーピーエー, CO2→二酸化炭素), kanji khó → kana/từ dễ (忌避効果→寄せつけない効果), hạn chế 「――」「…」.

## ⚠️ Hệ số ô C — CALIBRATE độ dài (BẮT BUỘC đo thật)

Chuẩn lý thuyết **300–330 ký tự/phút**. Lần render đầu tiên:
1. Render thử ~4.000 ký bằng speaker đã chốt @ speed chuẩn.
2. Đo phút thực tế → tính hệ số thật (ký tự ÷ phút).
3. Ghi hệ số vào đây, dùng cho các bài sau.

> **Hệ số thực đo được (2026-07-13, 青山龍星/ノーマル/0.9, tts_render intonation 1.15, gap mặc định):**
> - **337.5 ký/phút** (gồm ~0.22s nghỉ/dòng trống) — bài 7.257 ký = 21分30秒.
> - Thuần đọc (trừ nghỉ): ~350 ký/phút.
> - **Áp cho bài sau:** 20 phút ≈ 6.750 ký · 25 phút ≈ 8.450 ký · 30 phút ≈ 10.100 ký.

> ⭐ **ĐO LẠI 2026-08-13 — LỚP TAG NHẤN NHÁ ĂN ~10% ĐỘ DÀI. Hệ số 337.5 ở trên chỉ đúng cho
> script KHÔNG TAG.** Video 19 (`19_haisuiko-naze-tsumaru`): **6.491 ký (đã trừ tag) → 21分15秒
> = 305.4 ký/phút**, với **79 tag ≈ 12,2 tag/1000 ký**. Tao viết bài nhắm 19,2′ theo hệ số cũ và
> ra video **21,25′** — lệch **+2 phút**, tức bài nào nhắm trần 25′ sẽ tự vọt qua 27′.
> - **Áp cho bài CÓ TAG (mặc định từ nay, vì `humanize-script-voice.md` bắt buộc 15–25 tag… và
>   thực tế bài dày sóng ăn 60–80 tag):** 20 phút ≈ **6.100 ký** · 22 phút ≈ **6.700 ký** ·
>   25 phút ≈ **7.650 ký**.
> - Cơ chế: mỗi `[間N]`/`[後間N]` thêm khoảng lặng thật vào timeline; `[速0.8]` kéo dài câu đó ra.
>   Bài càng nhiều cú lật → càng nhiều tag đỉnh → càng chậm. **Đừng "sửa" bằng cách bỏ tag** —
>   tag là thứ mua chất người; sửa bằng cách **viết ít ký hơn**.
> - ⚠️ n=1. Số 305.4 đúng cho **mật độ ~12 tag/1000 ký**; bài 20 tag/bài (mật độ ~3) sẽ nằm giữa
>   305 và 337. Bài sau đo lại rồi ghi thêm dòng để có đường cong thật, đừng coi 305.4 là hằng số.

## Thư mục & lưu file

- Transcript nguồn để REWRITE (Chế độ A) + log đề tài chống trùng: `01_SOURCES/` — đặt tên `YYYY-MM-DD_<slug>.txt`
- Kịch bản sạch: `03_SCRIPTS/<NN>_<slug>.md` — bản đọc TTS: `03_SCRIPTS/<NN>_<slug>_TTS.md`
- Header mỗi script ghi: chế độ (A/B), nguồn (nếu rewrite), độ dài mục tiêu, ngày viết.
- Mẫu giọng/cấu hình VOICEVOX: `05_VOICE/` — output render + thumbnail: `06_VIDEO/`

## ✅ CTA giữa video — BẮT BUỘC từ video 03 (user chốt 2026-07-16)

Mọi `_TTS.md` mới PHẢI chứa câu CTA canonical co-dai (`.claude/rules/cta-midvideo.md` §2.4 — 高評価+シェア+コメント), đặt ở ranh giới chương gần 50%, bọc dòng trống. **Gate trước khi render:** grep `高評価` trong `_TTS.md` — không có → BỔ SUNG rồi mới synth voice (renderer chỉ cảnh báo mềm khi thiếu, không tự chèn được). Video 01–02 viết trước rule, đã render không CTA — không tự re-render.

## 🎥 LỚP HÌNH KIỂU VOX (chốt 2026-08-06 — kênh đầu tiên được bật)

Quy trình: skill **`video-vox`** (`.claude/skills/video-vox/SKILL.md`). Tool dùng chung:
**`Projects/_media_library/make_vox.py --channel co-dai`** · Gate: **`_media_library/check_vox.py`**.

- ⛔ **`tools/make_vox_codai.py` LẠC HẬU, đừng gọi nữa.** Bệnh đo được của nó ở video 16: **39 thẻ `title` trên 62 thẻ vox (63%)** = 39 khung giống hệt nhau (PowerPoint + rủi ro *inauthentic content*), chỉ **1 thẻ** có ảnh thật + annotation, còn 58 ảnh full-khung KHÔNG có annotation nào.
- **Đổi cấu trúc chính: ẢNH THẬT LÀ NỀN của thẻ**, chữ/mũi tên/số đè lên chính nó (`"bg": "photo"`). 12 kind: `flow · collage · stat · bar · line · dot · compare · room · process · timeline · source · title`.
- Hồ sơ khoá trong `channels.py`: palette **bright** (`#F7F6F2`+`#FFD200`+`#E03A3A`) · font **Noto Sans JP** · **`title_cap` 4**. `safe_bottom` **tự suy** từ `sub_style`/`sub_size` → phụ đề `pill`/26 hai dòng ⇒ **y=588**, vùng chữ chỉ ~400px ⇒ **MỘT ý mỗi thẻ**.
- Gate trước render (chạy cùng `check_coldopen.py`): `python E:\Claude\Projects\_media_library\check_vox.py 03_SCRIPTS\<n>_..._SLIDES.json --channel co-dai --tts 03_SCRIPTS\<n>_..._TTS.md`

## 🎬 DỰNG VIDEO — luật đầy đủ ở `09_VIDEO_PIPELINE.md`

> **Mọi video của kênh này dựng theo `09_VIDEO_PIPELINE.md`** (chốt 2026-08-18, đúc từ video 21 —
> bản đầu tiên có lớp chuyển động bằng hình + avatar + FX). Đọc nó TRƯỚC khi dựng, đừng tự chế lại
> thứ tự: chạy sai thứ tự là mất công gen lại ảnh.

Tóm 9 bước: `check_coldopen` → `voice_only` → `gen_slidesNN` → **duyệt `--still`** → user gen ảnh →
`placeNN` + `strip_wm_crop` → **`autofocus`** → **`add_fx`** → dựng clip → `video_render --reuse`.
Ba việc hay quên nhất: ⓐ `autofocus`/`add_fx` phải chạy SAU khi có ảnh và SAU voice ⓑ chạy lại
`gen_slides` là XOÁ kết quả của chúng ⓒ **dựng demo 90–120 giây trước bản đầy đủ** — ở video 21
chính demo bắt được 2 lỗi mà không gate nào đo được.

## 🎞️ LỚP CHUYỂN ĐỘNG BẰNG HÌNH — `make_shot.py` (chốt 2026-08-18)

> user: *"tao muốn làm video dạng chuyển động kiểu gần như nenkin. Nhưng tao muốn chuyển động bằng hình ảnh."*

**Vấn đề đo được:** lớp vox chỉ phủ **12/83 entry** (#21) và **13/78** (#22). 70 entry còn lại là **ảnh TĨNH đứng yên ~15 giây** — đó là chỗ video chết, và nó không sửa được bằng cách thêm thẻ chữ (thêm nữa thì thành PowerPoint).

**Cơ chế mượn từ nenkin, đổi nội dung:** `make_stage.py` build-on bằng **chữ/hộp**; `make_shot.py` build-on bằng **HÌNH**. Khung vẫn **đứng yên tuyệt đối** — ⛔ không pan, không zoom, không Ken Burns (`feedback_video_no_motion_mot_giong` giữ nguyên). Cái động là **ảnh được lắp vào**.

| mode | dùng cho câu | thứ hiện dần |
|---|---|---|
| `soft` | câu KỂ | chỉ "thở" ±1,5% sáng (nhịp nghỉ cho mắt) |
| `inset` | câu PHÓNG TO CHI TIẾT | tấm ảnh macro trượt lên 26px + hiện dần, viền trắng đổ bóng, rồi mũi tên đỏ vẽ dần |
| `focus` | câu CHỈ ĐÍCH DANH | vòng khoanh đỏ vẽ dần (nét bút dạ, hơi quá một chút) + ngoài vòng tối 24% |
| `wipe` | câu ĐỔI TRẠNG THÁI | ảnh B lộ dần đè ảnh A, đường wipe có vệt sáng |

🔴 **VAI CHỌN THEO ẢNH, KHÔNG THEO THỨ TỰ** (bản đầu làm ngược, phải sửa): ảnh **đã macro** → `focus` (phóng to nữa thì vỡ hạt) · ảnh **cảnh** → `inset` (cắt một mảnh của chính nó). Cứ 3 entry cảnh thì 1 để `soft` — nhịp thở, không phải tiết kiệm.

**Phân bổ hiện tại:** #21 = focus 12 · inset 40 · soft 19 · vox 12 — #22 = focus 13 · inset 34 · soft 17 · wipe 1 · vox 13.

**Nhịp mỗi clip** (giống `make_vox`): nền có mặt từ frame 0 → 0,55s phần tử 1 → 1,70s phần tử 2 → **đứng im** tới hết clip; idle loop 4s thở, cycle nguyên ⇒ loop sạch.

```bash
python E:\Claude\Projects\_media_library\make_shot.py slides 03_SCRIPTS\<n>_SLIDES.json ^
    06_VIDEO\<slug>\clips --img-dir 06_VIDEO\<slug> [--still] [--force]
```
Entry ảnh giờ khai `{"photo": false, "video": true, "shot": {...}}` → renderer dùng `clips/clip_XX.mp4`. `.sig` theo nội dung spec + mtime ảnh ⇒ đổi ảnh là dựng lại (đúng `render-background.md` §2.5).

⚠️ **Cái phải biết trước:** mỗi clip 30s ≈ **19 MB** ⇒ một video ~83 clip ≈ **1,5 GB** clip trung gian. Xoá sau khi render xong (bước `--done` của `upload_pack.py` đã dọn `06_VIDEO/<slug>`).
⚠️ **`focus`/`inset` cần toạ độ vùng nhìn.** Hiện để mặc định giữa-lệch-phải; **sau khi có ảnh thật phải soi và chỉnh `focus: [cx, cy, r]`** cho những khung mà vòng đỏ rơi vào chỗ vô nghĩa — vòng khoanh sai chỗ tệ hơn không khoanh.

### ⭐⭐ QUY TRÌNH LỚP HÌNH — chốt lại 2026-08-12 (video 19), đọc trước khi làm video sau

**Thứ tự BẮT BUỘC** (làm ngược thì user phải gen lại ảnh — video 19 mất 36/81 ảnh):
```
SLIDES.json → check_vox → preview TỪNG FRAME → USER DUYỆT → mới xuất prompt ảnh → user gen
→ place → make_vox --still (duyệt lại) → quét watermark → make_vox (MP4 thật) → render
```

| tool (đều ở `tools/`) | việc |
|---|---|
| `gen_slides19.py` | sinh SLIDES + prompt ảnh. ⭐ **2 biến thể style: `STYLE` (bối cảnh) / `STYLE_MACRO` (thẻ vox)** + bảng **`VOXSUBJ`** (chủ thể ảnh theo TÊN THẺ, không theo dòng thoại) |
| `preview_frames.py` | xuất **PNG từng entry** + sheet phân trang — gọi thẳng `video_render.make_slide()` nên thấy đúng cái sẽ render |
| `place19.py` / `place19b.py` | khớp lô ảnh tải về ↔ slot (token-overlap), `b` ghi đè bản sai framing |
| `strip_wm_crop.py` | gỡ ✦ bằng **CẮT** 0,908W + trim 16:9, backup `_wm_orig/`, có `--restore` |
| `gen_vid19.py` | prompt **image-to-video** (khoá `LOCKED CAMERA`, chống Ken Burns) |
| `enable_clips19.py` | bật `"video": true` **chỉ khi** clip mp4 tồn tại |

🔴 **Bốn bẫy đã dính thật ở video 19, đừng lặp:**
1. **`make_vox --still` KHÔNG tạo mp4** → preflight chỉ **cảnh báo** rồi âm thầm fallback ảnh tĩnh ⇒ mất trọn lớp động mà vẫn `EXITCODE=0` (`render-background.md` §2.6②). Kiểm: `mp4` phải **= số entry `video:true`** (video 19: **26**).
2. **`.cmd` phải ASCII-ONLY** — comment tiếng Việt có dấu ⇒ cmd.exe hiểu thành lệnh rác, exit 0, **log không được tạo** (§2.6①).
3. **Ảnh thẻ vox phải MACRO** — vox annotate ĐÈ LÊN ảnh; style lock giữ tông nhưng **khoá luôn framing** (`media-library.md` §2.11).
4. **✦ watermark: đo bằng MẮT rồi CẮT** — `strip_wm_star --check` trượt 89/89 trên lô này (`media-library.md` §2.10⑤).

📌 **Vá `make_vox.py` 2026-08-12:** dải vàng highlight + nhãn chart có stroke cho `bar`/`line`/`compare`/`process` khi thẻ có ảnh → 4 kind này giờ **chạy được trên ảnh** (trước phải để nền phẳng). Chi tiết + bán kính ảnh hưởng: skill `video-vox` §THẺ TRÊN ẢNH.
- ⭐ **ĐẠI TU 2026-08-07** (user: *"video gen ra xấu quá"* — 4 bệnh: khung trống nửa dưới · ảnh nhợt vì scrim trắng · phẳng wireframe · động 4s rồi đứng 26s): layout 2 tầng (đồ hoạ/khối màu TRÀN dưới safe_bottom, chữ có nghĩa vẫn trên — X4 nguyên) + `treat_photo` darken/duotone + grain/ghost/sticker/highlight + **INTRO 30fps + IDLE LOOP 4s** thay đứng hình. Knob trong `channels.py` khối `"vox"`. Duyệt PNG bằng `--sub-mock`. **Bộ mẫu MỚI: `06_VIDEO/_vox_demo3/_vox_sheet.jpg`** (16 thẻ, có mock phụ đề + 3 thẻ nền ảnh + title tone accent).
- Bộ so trước/sau cũ (tham khảo lịch sử): `06_VIDEO/_vox_ab/clips/_vox_sheet.jpg` (12 slot của video 16) vs bản gốc video 16. Bộ 12 kind đời 08-06: `06_VIDEO/_vox_demo2/_vox_sheet.jpg`.

## Engine biên kịch

Toàn bộ công thức (2 chế độ A·REWRITE / B·VIẾT MỚI, bộ khung hook–chương–dòng tiền–kết 3 lớp, blacklist/whitelist, checklist 13 điểm, định dạng 5 khối gồm pinned comment) nằm trong skill **`.claude/skills/script-co-dai/SKILL.md`**. Claude tự gọi khi user dán transcript 生活の知恵 để viết lại hoặc đưa chủ đề mới cho kênh này.

## 🖼️ Thumbnail CHUẨN KÊNH (chốt 2026-07-16, video 01 shiroari — user loại bản scene+text stack)

Style = **CONCEPT-DIAGRAM sạch kiểu đối thủ ngách** (kênh 生活の知恵 7.5K sub, video 348K). **MẪU CHUẨN ĐÃ DUYỆT: `06_VIDEO/01_hosan-shiroari/thumbnail_v3_final.jpg`** (2026-07-16) — mọi thumbnail sau đặt cạnh ảnh này để so "kiểu".

> ⭐ **3 nguyên tắc gác cổng HÌNH (user chốt 2026-07-16, mọi kênh — mục 0.5 `youtube-jp-shokutaku/02_THUMBNAIL_TITLE_RULES.md`):** ① 1 điểm nhấn duy nhất, cắt chi tiết thừa, tương phản cao ② phóng đại CẢM GIÁC (cảnh báo→nguy hiểm rõ; hướng dẫn→kết quả cuối) ③ 120px vẫn rõ — nền đậm, chủ thể sáng. "Thumbnail không phải để đẹp mà để người ta dừng lại."
- **Nền PHẲNG sạch studio** (navy tối như mẫu chuẩn, hoặc trắng sáng) — KHÔNG dùng ảnh scene/bối cảnh, KHÔNG style stack 3 dòng của health/shokutaku.
- Bố cục sơ đồ: **[vấn đề bên trái] → mũi tên đỏ cong → [giải pháp bên phải, cầm trên tay]**; chủ thể cắt rời, to, macro.
- Text DUY NHẤT 1 dòng 5–7 ký (trắng/đen + từ đắt ĐỎ) — **AI bake text luôn** (gen 2–3 bản loại bản chữ lỗi), KHÔNG ghép bằng make_thumb. Luôn kèm 1 prompt fallback no-text.
- **⭐ Bổ sung 2026-07-21 (mổ 0-view, học từ 3 video hit của 昔の人の知恵):** ① dòng text chính phải chiếm **≥1/3 chiều cao khung** (vàng/trắng viền đen dày) ② **LUÔN có badge giá tiền** (数百円/500円/0円 — hình sao vàng hoặc khối đỏ góc) — yếu tố xuất hiện ở cả 3 hit đối thủ (約600円/電気代0円/500円でできる) mà thumbnail 01–02 của kênh còn thiếu ③ nếu đề tài có nhiệt độ/con số đo được → badge số liệu (34℃→21℃).
- **Quy trình chốt (user, 2026-07-16): Claude chỉ ĐƯA PROMPT** (chính + fallback, lưu vào script) → user tự gen → Claude duyệt 3 cửa (che chữ/cạnh mẫu chuẩn/120px) + quét compliance. Template prompt tổng quát: xem script 01 mục サムネ v3.
- **⭐ Thư viện 8 khuôn bố cục + sổ xoay vòng (chốt 2026-07-17): `02_THUMBNAIL_PROMPTS.md`** — mỗi video dùng khuôn KHÁC video liền trước (chống inauthentic content); text ưu tiên đè 3 tầng bằng PIL (hàm `make_diagram_3dan` của video 02), không bake. Chốt thumbnail xong phải cập nhật sổ trong file đó.
- Compliance thumbnail vẫn theo luật gốc (không 殺/血/死; 一掃/追い出す OK).

## ⚠️ Tuân thủ YouTube → theo LUẬT GỐC toàn hệ thống

Luật đầy đủ ở **`.claude/rules/youtube-compliance.md`** — mỗi lần đóng gói video (tiêu đề/thumbnail/概要欄/tag): quét checklist & báo ngay từ/điểm cần né.

Áp riêng kênh này:
- Chế độ A phải rewrite 100% câu chữ, không chuỗi ≥7 chữ trùng transcript gốc (chống "inauthentic/reused content"), anecdote + ví von thay mới toàn bộ.
- Fact/nguồn/năm tháng GIỮ NGUYÊN như gốc — bịa nguồn = chết kênh.
- DIY/hóa chất: bắt buộc đoạn an toàn; claim chưa kiểm chứng: rào chữ 「歴史的な記録によれば」; chạm y tế: khuyến cáo 「医師にご相談ください」.
- Chương dòng tiền: nói cấu trúc ngành, KHÔNG cáo buộc đích danh công ty.
- **Credit giọng: KHÔNG ghi VOICEVOX trong 概要欄** (user chốt 2026-07-22, đã gỡ khỏi 3 video đầu — ngoại lệ của luật gốc mục 2; benchmark ngách cũng không ghi). ⚠️ Lưu ý tồn đọng: điều khoản VOICEVOX yêu cầu ghi 「VOICEVOX:青山龍星」 ở đâu đó khi công khai — nếu muốn sạch license thì để 1 dòng trong pinned comment hoặc credit cuối video, user quyết.

## 📐 METADATA CHUẨN KÊNH (chốt 2026-07-22 — đúc từ benchmark 昔の人の知恵 8,5K sub/564K + 驚きの世界, đo API; áp TỰ ĐỘNG từ video 04)

Cả 2 kênh thắng ngách đồng nhất 4 tín hiệu, video hit 431K cũng y hệt:

1. **categoryId = 27 (Education)** — không phải 22/24.
   🔴🔴 **CÂU CŨ *"3 video đầu đã sửa 22→27 ngày 2026-07-22, áp TỰ ĐỘNG từ video 04"* LÀ SAI — đo API 2026-08-12: `22` ở 10/14 video.** Đúng 3 video đầu được sửa tay, rồi từ 07-23 **mọi video quay lại 22**; không có cơ chế tự động nào. Lỗi im lặng sống 20 ngày.
   **Gốc rễ:** `upload_api.py` ghi đúng 27 và video duy nhất đăng qua API (07-31) **là 27** — 10 video sai đều **ĐĂNG TAY**, ăn từ `Cài đặt → Chế độ mặc định cho video tải lên → Cài đặt nâng cao → Danh mục = 「Mọi người và blog」`. Cùng họ lỗi với memory `project_studio_default_upload_tags`.
   ⇒ **Thi hành: sửa ô mặc định đó MỘT LẦN sang 「Giáo dục」** (user chốt 2026-08-12) — rẻ, 1 click, chặn được sai lệch từ video 19 trở đi.
   ⛔ **10 video cũ GIỮ NGUYÊN cat 22** (user chốt). Lý do: mỗi `videos.update` phải gửi lại **đủ** snippet (thiếu field = **xoá** field), để chữa một tín hiệu **yếu**, trên 10 video gần như không có traffic để cứu → rủi ro > lợi. **Đừng "phát hiện lại" rồi đề xuất sửa.**
   ⚠️ **ĐỌC ĐÚNG MỨC:** benchmark để **27 ở 22/22** là số **đo được**; nhưng *"category sai làm YouTube xếp cụm sai"* là **cơ chế SUY RA, chưa đo được** — category là **tín hiệu YẾU** so với title/mô tả/nội dung/co-view. Nó **KHÔNG** ngang hàng với biến khuôn title (điểm 7c, có bằng chứng từ 2 nguồn độc lập). Chi tiết: `08_ANALYTICS_LOG.md` §4.
2. **RỔ 12 TAG NHẬN DIỆN KÊNH — cố định, đứng ĐẦU danh sách tag MỌI video** (benchmark lặp y hệt 10 tag đầu trên toàn bộ video, tổng 42–69 tag):
   `古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損`
   → sau rổ này mới đến tag riêng video (đề tài + long-tail), tổng ~25–35 tag.
3. **3 HASHTAG NHẬN DIỆN KÊNH cố định:** `#生活の知恵 #昔の知恵 #古代の秘訣` — đứng đầu dòng hashtag, đặt ở **CUỐI desc** (cấm đặt dòng 1 desc — chiếm mất vùng hook hiển thị); hashtag đề tài (2–3 cái) nối sau.
4. **Desc 800–1.800 ký:** 3 dòng hook → 目次 → đoạn topical dài nhồi keyword liên quan tự nhiên → disclaimer an toàn. (Benchmark còn lặp nguyên title làm dòng 1 — mình giữ 3 dòng hook theo rule SEO chung, không bắt chước điểm này.)
5. Caption srt tự upload = LỢI THẾ so benchmark (họ toàn auto-caption) — giữ.
6. **Playlist/trailer KHÔNG phải yếu tố thắng** (cả 2 benchmark đều không có playlist) — kênh đã set cho đủ bộ, không cần đầu tư thêm.
7. ⭐ **LUẬT CHỌN KEYWORD DẪN TITLE (đúc từ 3 lần đo Trends: video 06, 07, 08 — chốt 2026-07-26):** trên YouTube Search JP, **khái niệm/lợi ích gần như không có cầu; cầu nằm ở TÊN VẬT / TÊN MÓN cụ thể.** Bằng chứng đo thật (thang tương đối trong rổ):
   - `電気代 節約` **5** vs `すだれ` **42** → khung "tiết kiệm tiền điện" là khung SAI để dẫn keyword.
   - `干し野菜` **0** vs `切り干し大根` **33,5** → cùng một thứ, khác cách gọi, chênh vô cực.
   - `保存食` **3** · `発酵食品` **1,3** · `食中毒 予防` **0** · `弁当 傷まない` **0** — mọi từ khái niệm đều chết.
   - Ngoại lệ đã thấy: `排水溝 掃除` **46** vs `排水口 ぬめり` **0** → cùng vật nhưng SAI CHỮ cũng chết. Phải đo, không đoán.
   → **Cách áp:** title dẫn bằng 1–3 tên vật/món có volume đo được (đặt trong 5–7 chữ đầu), khái niệm/lợi ích đẩy về sau dấu 「――」 hoặc xuống desc. Từ khái niệm vẫn giữ làm tag (phủ topical) nhưng KHÔNG lên title.
7b. ⭐⭐ **LUẬT INTENT — TẦNG THỨ HAI trên điểm 7 (chốt 2026-08-12, đo TAY trong Studio).** Điểm 7 nói về **VOLUME** của cầu và **VẪN ĐÚNG NGUYÊN VẸN** (`すだれ` 42 vs `電気代 節約` 5) — 7b nói về **CHẤT** của đúng cái cầu đó. **Không cái nào đè cái nào: giữ TÊN VẬT làm keyword dẫn, chỉ đổi MODIFIER.**

   **Bằng chứng** (`CHANNEL_DIAGNOSIS_2026-08-12.md` §1c, §2ⓑ): AVD theo nguồn = **search 3:09** vs **browse 9:49** vs **trang kênh 8:48** ⇒ search bẩn gấp ~3, mà nó chiếm **80% impressions của kênh**. Soi từng query thì rõ vì sao:

   | ✅ DẪN ĐƯỢC — intent "cái nào nhất / tại sao / kể tao nghe" | ⛔ CẤM DẪN — intent "xác minh 1 thủ pháp hẹp" |
   |---|---|
   | `<vật> 最強` · `<vật> なぜ` · `<vật> やり方` · `<vật> 順番` · `<vật> 比較` · `<vật>` trần | `<vật> 効果` · `<vật> 意味ある` · `<vật>` + tên thủ pháp hẹp |
   | đo thật: **`蚊除け 最強` 19:17** · **`すだれ` 7:51** | đo thật: **`ハチの巣` 0:03** · **`ゴキブリ対策` 0:11** · **`室外機 日除け 効果` 0:16** · **`土用干し` 0:17** |

   🔴 **Vì sao đây KHÔNG phải chuyện cold open:** người gõ `室外機 日除け 効果` cần **20 giây** rồi đi — dù 20 giây đó viết hay tới đâu. Bài 25′ không phải hàng họ đến mua. Đây là lỗi **chọn tệp**, không phải lỗi **giữ tệp**; cửa 45 giây của `CHANNEL_DIAGNOSIS_2026-08-11.md` sửa việc khác và vẫn phải làm.
   → **Cách áp:** từ nhóm ⛔ **vẫn giữ làm tag** (phủ topical), **tuyệt đối không lên title**. Gate máy: `python tools\check_coldopen.py <NN>` đọc header `TARGET_QUERY:` + `INTENT:` của script, rơi vào nhóm ⛔ hoặc thiếu khai → **FAIL**.
   ⚠️ **Giới hạn:** mỗi query chỉ 1–2 view (n=20). Bằng chứng chính là **con số tổng hợp theo nguồn**, danh sách query là cơ chế giải thích — đừng trích một query lẻ làm bằng chứng.
7c. ⭐⭐⭐ **KHUÔN TITLE = CÂU HỎI `なぜ` hoặc LỆNH CẤM cụ thể (chốt 2026-08-12, đo 22 video peer).** Đây là biến **thứ hai và cuối cùng** còn khác nhau giữa co-dai và benchmark — chi tiết + bảng đầy đủ: `CHANNEL_DIAGNOSIS_2026-08-12.md` §6b.

   **Phép so gần như có đối chứng:** `昔の人の知恵` lập 2026-06-08 (**12.700 sub · 1,28M view / 65 ngày**) vs co-dai (**1 sub · 110 view / 38 ngày**) — **cùng ngách · cùng nhịp 3,2 vs 3 video/tuần · cùng median 22′ · cùng giờ 11h · cùng ngày T2/T4/T6 · keywords trùng nặng.** ⇒ **Loại sạch** giả thuyết lịch/độ dài/nhịp/giờ. Chỉ còn **category** (điểm 1) và **khuôn title**.

   | | khuôn | ví dụ + view/ngày đo được |
   |---|---|---|
   | ✅ **CÂU HỎI `なぜ`** (8/22 video peer, ăn hầu hết hit) | `なぜ〜のでしょうか？` · `なぜ〜は忘れられたのか` | `なぜ私たちは、家を冷やすために塩を使わなくなったのでしょうか？` **5.560** · `なぜ、4,000年の知恵は忘れられたのでしょうか` **2.248** |
   | ✅ **LỆNH CẤM cụ thể** | `絶対に〜してはいけないN つのもの` | `キッチンの排水口に絶対に流してはいけない5つのもの` **34.692 v/ngày · 357.815 view** |
   | 🔴 **khuôn co-dai đang dùng** | `<vật> + 数百円 + kết quả` | `すだれ数百円――熱の7割は窓から、昔の涼み方でエアコン代が下がる` → **hứa kết quả KIỂM TRA ĐƯỢC TRONG 20 GIÂY** = hút đúng tệp bỏ đi ở giây 16 |

   🔴 **KHÔNG phải cứ `なぜ`/danh sách là thắng** — 3 bản BÉT của peer đều là danh sách **chung chung**: `15の秘訣` **77 v/ngày** · `10のもの！` **49** · `〜の秘密` **194**. ⇒ Biến thật là **có hay không một điều CẤM / NGHỊCH LÝ cụ thể**, không phải cái vỏ 「Nつの」.
   ⭐ **Vì sao tin được:** hai nguồn dữ liệu **hoàn toàn độc lập** (query search của mình ở 7b · title của peer ở đây) chỉ về **cùng một cơ chế** — title hứa "giải thích" giữ người, title hứa "kết quả kiểm tra nhanh" thì không.
   → **Cách áp:** giữ `数百円` như một **vế phụ sau `――`**, còn **vế DẪN là câu hỏi `なぜ` hoặc lệnh cấm**. Áp cho cả 5 phương án ở Khối 2 của skill.
8. 🔴 **ĐÃ ĐO LẠI 2026-07-28 — điểm 8 cũ SAI, đừng dùng nữa.** Câu cũ: "benchmark 昔の人の知恵 từ 2026-07-15 đã tăng nhịp lên ~1 video/NGÀY → lịch 4/tuần của mình là SÀN, ngách đang đua volume". **Đo publishedAt qua API: 12 video / 32 ngày = 2,62 video/tuần**, và nó **chưa từng đăng Chủ Nhật** (0/12). → **không có cuộc đua volume nào** ở ngách này để đua. Median view benchmark theo ngày: **T2 231K** ≫ T7 24,4K > T6 17,1K > T5 14,9K > T4 6,2K → **dồn video mạnh nhất vào T2**. Bằng chứng: `.claude/rules/upload-schedule-measure-2026-07-28.md`.
9b. ⭐⭐ **LỊCH HIỆN HÀNH (2026-08-03, user chốt nhịp toàn hệ thống "2 ngày 1 video · kênh đang được đề xuất 1 ngày 1 video"): T2·T4·T6 11:00 JST — 3 video/tuần.** Thêm T4 vào bộ T2·T6 cũ để giãn đều 2-2-3 ngày. Giờ 11:00 GIỮ NGUYÊN. Đánh đổi biết trước: T4 là ngày median view yếu của benchmark (6,2K) — chấp nhận vì kênh đang BROWSE=0 nên số theo ngày của đối thủ chưa có tác dụng. ⚠️ **Gate nội dung KHÔNG được nới:** script không PASS `tools\check_coldopen.py` → **BỎ SLOT, không đăng bù**. ⚠️ Trần của gate **đã đổi 2026-08-11: ≤75s → cửa sổ giây 0–45** (xem §🎯 RETENTION ngay dưới) — dòng "≤75s" cũ là số ĐÃ CHẾT. Nguồn sự thật lịch: `.claude/rules/upload-schedule.md` Mục 0.9.
9. ⚠️ (căn cứ cũ, giữ để tra) **LỊCH HẠ 4/tuần → T2·T6 2/tuần PHÉP THỬ SẠCH (2026-07-30, user chốt sau KHÁM KÊNH `CHANNEL_DIAGNOSIS_2026-07-30.md`):** 8 video/15 ngày = 36 view, **BROWSE/SUGGESTED = 0 tuyệt đối** (vòi chưa từng mở), retention mất 50–71% trước giây 75, và **12/12 script vào bài ở giây 100–643** (đo `tools/check_coldopen.py`). Ngách KHÔNG chết — benchmark cùng tuổi 10K sub/726K view, trùng đề tài trực tiếp. **Script mới bắt buộc qua gate `python tools\check_coldopen.py` (vào bài ≤75s, không dặn dò an toàn trong 60s đầu) trước khi render**; thumbnail theo khuôn benchmark-bright (nền SÁNG + 1 vật + SỐ kết quả + mũi tên — xem `02_THUMBNAIL_PROMPTS.md` khuôn B1). Tăng lại ≥3/tuần khi có view BROWSE đầu tiên.

## 🎯 RETENTION — MỤC TIÊU AVD 60% (user chốt 2026-08-11)

> Bằng chứng đầy đủ: **`CHANNEL_DIAGNOSIS_2026-08-11.md`**. Gate máy: **`python tools\check_coldopen.py <NN>`** (thêm `--calib` để hiệu chuẩn lại trên video đã lên sóng). Spec viết: skill `script-co-dai` MỤC 10 + MỤC 14 điểm 1.

**Hiện trạng đo được (Analytics API 2026-08-11):** AVD kênh **5′09″ = 21,94%** / 95 view · `relPerf` 60s đầu **0,17–0,46** (phân vị đáy) · **BROWSE = 0 · SUGGESTED = 0** tuyệt đối.

🔴 **CỬA TỬ LÀ GIÂY 15 → 45.** Gần như không ai bỏ đi trong 15 giây đầu (88–100%), rồi mất **một nửa** khán giả ở giây 30–45. Video tệ nhất (07 すだれ, AVD 12,12%) có 4 câu liên tiếp không trả gì ở giây 22–45: gán nguồn → nhắc lại → nhắc lại → mục lục.

🔴 **CẮT NGẮN KHÔNG MUA ĐƯỢC 60%.** Tích phân đường cong thật: cắt video xuống **5 phút** vẫn chỉ **45,0%** (01) / 36,7% (07); cắt về 12′ chỉ **+6 điểm**. Vì `AVD% ≈ chiều cao TRUNG BÌNH của đường cong`, mà cái vách ở giây 30–45 kéo mọi cửa sổ xuống. ⇒ **60% mua TRỌN trong 45 giây đầu.** Khớp §1e: benchmark 昔の人の知恵 median **21,9′** vẫn ăn 341K view ⇒ **độ dài KHÔNG phải biến, giữ 25′.**

**Hai con số phải đạt:** ① **@45s ≥85%** (nay 41–50%) ② **sàn thân bài ≥55%** (nay 41,7% @3′ → 33,3% @10′ → 16,7% @20′).

⚠️ **60% chưa có tiền lệ trong workspace** — cao nhất từng đo là chouhen video 12 **51,6%**, và đó là DRAMA. Mốc chặng **40% → 50% → 60%**; **3 video liên tiếp ≤30% → mốc 60% sai với ngách này, mổ lại chứ đừng vá tiếp.**

⚠️ **Sửa retention KHÔNG tự mở vòi phân phối** — SEARCH là cửa organic duy nhất (58/95 view), CTR/thumbnail vẫn là cửa vào. Đọc kết quả bằng **`relPerf` giây 15–45**, KHÔNG bằng view.

### ⭐⭐ BỔ SUNG 2026-08-12 — đo TAY trong Studio (`CHANNEL_DIAGNOSIS_2026-08-12.md`)

Bộ số API ở trên **không nhìn thấy `impressions`/CTR** (Google rút từ 2026-07-30). Đọc tay ra 3 thứ đổi thứ tự ưu tiên — mục tiêu AVD 60% + cửa 45 giây ở trên **GIỮ NGUYÊN**, chỉ thêm vào:

1. ⛔ **CTR ĐÃ ĐẠT — ĐỪNG ĐỔ CÔNG VÀO THUMBNAIL.** Lifetime **1.397 imp / CTR 4,7%**; search 5,3%; bản tốt nhất **14,3%** (video 02), 11,4% (01), 9,0% (15). 🔴 **Đừng bê kết luận "kênh chết ở BAO BÌ" của `chouhen/CHANNEL_DIAGNOSIS_2026-08-12.md` sang** — chouhen không có CTR để đo, co-dai có và nó đạt. Chỉ vá **lẻ** 2 bản 0% CTR: **03 雑草** (142 imp) và **17 排水溝10円玉** (20 imp).
2. ⭐ **Biến mới = INTENT của query search** (xem §📐 điểm **7b**): 80% impressions từ search, và **AVD search 3:09** vs browse 9:49. Kênh đang tự kéo về tệp không xem hết bài.
3. 🔴 **Rail đề xuất chưa mở vì `「Kênh mà khán giả xem」 = không đủ dữ liệu`** — YouTube chưa dựng được cụm co-view nào ⇒ **không có chỗ đặt kênh cạnh**. `Video đề xuất` = **0 impressions suốt đời kênh**. Đây là hệ quả, **không kéo trực tiếp được**; đường vào là đề tài **trùng đích danh video peer đang hot** (`01_SOURCES/00_TOPIC_LOG.md`).
4. ⚠️ **KHÔNG phải throttle kiểu health.** Chuẩn hoá theo ngày sống: baseline **4–11 imp/ngày/video ổn định**, chỉ video 07 nhảy **36,6** (512 imp — cú test duy nhất, CTR 5,1% đạt / AVD **10,7%** trượt). Health đi tới **1 imp/video** — hình dạng khác hẳn, **đừng kê thuốc health cho ca này**.
5. ⚠️ **Spec cửa-45-giây hiện có 0 video đo được** (video 18 mới 4 imp / 1 view) ⇒ **đừng xếp pivot mới lên trên nó** trước khi nó có số.

## Vault tương ứng

Tri thức/bài học/research: `E:\Claude\SecondBrain\10_Projects\youtube-jp-co-dai\`

> 📦 Doc cũ (diagnosis/optimize/benchmark hết hạn, khuôn đã bị đè) đã dời vào `./_archive/` (dọn 2026-08-24) — đường dẫn cũ trong rules trỏ file nào không thấy ở gốc thì tìm ở đó.
