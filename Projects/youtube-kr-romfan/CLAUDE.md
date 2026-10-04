# youtube-kr-romfan — CLAUDE.md

# ⏹⏹ DỰ ÁN ĐÃ ĐÓNG — kênh này nay là `地形と地名の日本史` (2026-09-16)

> **Kênh YouTube `UCfXuolJMQ-3CMpmTeQVkwKA` (사우 오디오) đã ĐỔI NGÀNH** thành
> **`地形と地名の日本史`** — repo mới: **`E:\Claude\Projects\youtube-jp-chikei\`**.
> Cùng một kênh, cùng Gmail `ladykiller301096@gmail.com`, cùng Chrome `Profile 12`.
>
> 🔴 **ĐỪNG upload/đăng gì từ repo này nữa** — `upload_pack.py --channel kr-romfan` sẽ gắn
> `cta_lang: kr` + checklist Hàn lên một kênh giờ là kênh Nhật.
> Repo giữ lại để tra: script cũ, tool Azure TTS, khuôn FX radio-drama, `credentials/`
> (token đã được copy sang repo mới).
>
> 3 video Hàn đã đăng: đặt **private** khi chuyển đổi (user chốt) — reset tín hiệu chủ đề.
>
> ⚠️ Kế hoạch cũ trong `yt-dashboard/projects.json` định biến kênh này thành kênh Hàn
> `장기요양·요양원 가족 가이드` (key `yoyang`). **Suất đó nay mất vật chủ, trạng thái `on-hold`** —
> muốn làm thì phải cấp kênh/Gmail khác.

---

⏸ **KÊNH NGƯNG LỊCH ĐĂNG** (`slots: []` — `upload-schedule.md` Mục 0.9; lịch cũ T3·T6·CN 21:00 KST ghi trong comment `upload_pack.py`, bật lại = trả về giá trị đó).

Kênh audio truyện Hàn **사우 오디오** — 로맨스 판타지 hiện đại: 계약결혼, 재벌가, 사이다 복수. Khán giả **nữ KR 18–35**, nghe thụ động. (Tên 이불속극장 là nháp cũ, đừng dùng lại.)

⚠️ **Ngoại lệ 45+:** tệp KR 18–35 → KHÔNG làm sạch 외래어/tiếng trẻ (`audience-45plus.md` §6.4b); các mục chữ to/phụ đề/nhịp vẫn áp.

## Skill & luật

- **`script-kr-romfan`** — nguồn chân lý về NỘI DUNG (2 chế độ A·bản địa hóa / B·viết mới, checklist, 5 khối output). File này = VẬN HÀNH (voice, thư mục, quota).
- Title/thumbnail đóng gói xong quét `youtube-compliance.md` (chỉ title/thumbnail/설명란 hiển thị, KHÔNG làm nhạt thoại thân bài).

## Voice — Azure Speech TTS (CHỐT)

Region `koreacentral`, tier F0 (500k ký/tháng — canh `03_VOICE/QUOTA.log`). Key: env `AZURE_SPEECH_KEY`/`AZURE_SPEECH_REGION`, fallback `tools/.azure_key` (KHÔNG commit).

- **Narration nữ (ngôi 나): `ko-KR-SunHiNeural`** — user đã re-test 10 giọng và CHỐT, đừng đề xuất đổi.
- **Nam chính: `ko-KR-InJoonNeural` hạ tông** (`<prosody pitch="-15%">`). Vai khác chọn từ demo: SeoHyeon/JiMin/YuJin (nữ trẻ), SoonBok (bà lớn tuổi), BongJin/GookMin (회장님). Demo: `youtube-jp-chouhen/01_SOURCES/kr_voice_demo/`.
- Mặc định **1 giọng SunHi toàn bài**; multi-voice chỉ khi user yêu cầu — tag đầu đoạn `[남]` `[시모]` `[회장]` `[여2]`.
- **Prosody chuẩn kênh (mặc định của `azure_tts.py`): rate -12% · gap 0.35s · pgap 1.0s · comma 250ms** (≈236 ký/phút).
- Tag `[속]` (nội tâm): SunHi pitch -10Hz — PHẢI gắn đầu các đoạn nội tâm khi viết script.
- Tag `[감]` (nhịp cảm xúc/cao trào): chậm + ngắt nghẹn + nghỉ dài — chỉ gắn nhịp thật sự cảm động, KHÔNG rải toàn bài. Định nghĩa trong `VOICES["감"]` của `azure_tts.py`.
- Bẫy: gọi REST bằng Python `urllib`, KHÔNG curl git-bash (hỏng encoding Hàn). Cache `segs/` theo index câu → **sửa lời thì xoá cache tay** (`render-background.md` §2.5).

## Render

```bash
cd E:\Claude\Projects\youtube-kr-romfan
python tools/azure_tts.py 02_SCRIPTS/NN_slug_TTS.md          # → 03_VOICE/NN_slug/{voice.wav, subs.srt}
python tools/fetch_bg.py                                      # nạp ~22 clip CHƯA dùng trước mỗi video
python tools/scene_render.py NN_slug                          # → 04_VIDEO/NN_slug/NN_slug.mp4
python tools/scene_render.py NN_slug --scenes 3 --suffix _test
```

- Render dài LUÔN chạy nền theo `render-background.md` (.cmd + log + EXITCODE).
- Visual: **20–25 cảnh nền động luân phiên/giờ**, mood cozy/romance, shuffle theo slug. Asset: tải MỚI theo `media-library.md` (sổ đen `skip_ids` + `rejected/`), cấm lặp nguyên bộ.
- **BGM: `04_VIDEO/bgm/Heartwarming.mp3`** (Kevin MacLeod CC BY 4.0 — BẮT BUỘC credit trong 설명란), gain `--bgm-gain -40`.
- Phụ đề Malgun Gothic trắng viền đen, sync từ subs.srt.
- Số trong script: giữ chữ số Ả Rập + đơn vị (100억 원, 4시) — Azure đọc chuẩn.
- Độ dài chuẩn ~40′ ≈ 9.000–10.500 ký hangul; batch viết ~4.500 ký/lượt. Dòng 모음 >60′ = video tổng hợp nối tập đã đăng, KHÔNG kéo dài tập lẻ (`audience-45plus.md` §4.1).

## Lớp FX radio-drama

Mỗi video có `02_SCRIPTS/<slug>_FX.json` (skill Mục 16 tự xuất) → `scene_render.py` tự thêm SFX + BGM động + quote card + phụ đề màu nhân vật (hero `#FFD75E`, villain `#8CEBFF`). Không có FX.json → render như cũ.
- Video đã render chưa đăng: `python tools/fx_mix.py <slug> --apply` (thay track audio, không re-render) — sau đó PHẢI `upload_pack --force` (mp4 đổi inode).
- SFX phải có tầng mid 200–600Hz; gain sting -5…-7, tim -8…-9, CTA -10.

## Thumbnail / Title

**Khuôn text 3 tầng + spec đầy đủ: `./THUMBNAIL_TITLE_FORMULA.md`.** Render bằng `tools/make_thumb.py` (ảnh thật Pexels + băng trắng/vàng, dòng key đỏ double-stroke, Malgun Gothic Bold). Gate: 1 điểm nhấn / phóng đại cảm giác / 120px đọc được; KHÔNG badge thời lượng; A/B 3×3 theo `ab-3title-3thumb.md`. Credit 설명란: `영상·썸네일: Pexels (무료 상업용 라이선스)`.

## Thư mục

`01_SOURCES/` transcript gốc · `02_SCRIPTS/` NN_slug.md + _TTS.md + _FX.json · `03_VOICE/` · `04_VIDEO/` · `07_UPLOADED/`.

## Persona

- Chào mở (sau cold open): "사우 오디오에 오신 걸 환영해요. 오늘도 편하게 누워서 들어주세요."
- Kết cố định: "오늘 이야기 여기까지예요. 재미있으셨다면 좋아요와 구독, 잊지 마세요. 사우 오디오였습니다."
- 설명란 luôn kèm: "본 이야기는 허구이며 등장인물·단체는 실제와 무관합니다." + credit giọng Azure TTS.

Vault: `E:\Claude\SecondBrain\10_Projects\youtube-kr-romfan\youtube-kr-romfan.md`.

> Bản đầy đủ: ./_archive/CLAUDE_FULL_2026-08-24.md
