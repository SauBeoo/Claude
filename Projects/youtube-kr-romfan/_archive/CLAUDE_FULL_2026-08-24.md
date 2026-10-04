# youtube-kr-romfan — CLAUDE.md

Kênh YouTube audio truyện Hàn **사우 오디오** — 로맨스 판타지 hiện đại: 계약결혼, 재벌가, 사이다 복수. Khán giả nữ Hàn 18–35, nghe thụ động (làm việc nhà, tàu điện, trước khi ngủ).

## Skill chính

- **`script-kr-romfan`** (`~/.claude/skills/script-kr-romfan/SKILL.md`) — toàn bộ luật biên kịch (2 chế độ A·bản địa hóa / B·viết mới, cấu trúc, blacklist dịch máy, checklist 13 điểm, 5 khối output). Skill là nguồn chân lý về NỘI DUNG; file này là nguồn chân lý về VẬN HÀNH (voice, thư mục, quota).
- Thumbnail/title đóng gói xong phải quét `E:\Claude\.claude\rules\youtube-compliance.md` (mục 12 skill + bảng từ demonetize; chỉ quét title/thumbnail/설명란 hiển thị, KHÔNG làm nhạt thoại trong thân bài).

## Voice — Azure Speech TTS (ĐÃ CHỐT 2026-07-10)

VOICEVOX không có tiếng Hàn → dùng **Azure Speech**, region `koreacentral`, tier **F0** (free 500k ký tự/tháng — 1 video 40′ ≈ 9.600 ký tự, dư dả nhưng retry cũng tính quota).

- Key/region trong env var user: `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`.
- **Giọng chính (narration nữ, ngôi 나): `ko-KR-SunHiNeural`** — theo demo `azure_SunHi.mp3`. **Re-test 2026-07-11:** render cả 10 giọng native ko-KR bằng cold-open truyện thật ở rate -5 (`03_VOICE/_voice_demo_story/`), so trực tiếp với SeoHyeon (giọng duy nhất Azure tag Audiobook) → user vẫn CHỐT SunHi. Đừng đề xuất đổi giọng narration nữa.
- **Giọng nam ưu tiên (nam chính 차도윤, thoại nam nếu render multi-voice): `ko-KR-InJoonNeural` hạ tông** — theo demo `demo_ko_injoon_deep.mp3` (InJoon + prosody pitch hạ, ví dụ `<prosody pitch="-15%">`; tinh chỉnh theo tai khi render thật).
- Còn lại **tùy ngữ cảnh**, chọn từ demo folder: 서현 SeoHyeon / 지민 JiMin / 유진 YuJin (nữ trẻ khác vai — 백여우, bạn thân), 순복 SoonBok (mẹ chồng/bà lớn tuổi), 봉진 BongJin / 국민 GookMin (회장님, phát thanh viên), Hyunsu Multilingual (đa ngôn ngữ).
- Demo nghe thử: `E:\Claude\Projects\youtube-jp-chouhen\01_SOURCES\kr_voice_demo\`.
- Mặc định render **1 giọng SunHi đọc toàn bài** (chuẩn audio web novel); multi-voice chỉ khi user yêu cầu — khi đó file `_TTS.md` dùng tag đầu đoạn `[남]` (InJoon hạ tông), `[시모]` (SoonBok), `[회장]` (BongJin), `[여2]` (SeoHyeon); không tag = SunHi.
- **Prosody CHUẨN KÊNH (user chốt 2026-07-11 sau A/B -5/-12/-18): rate -12% · gap 0.35s · pgap 1.0s · comma-break 250ms** — đo cold open ≈ 236 ký/phút. Đây là **mặc định của `azure_tts.py`** → chạy không cần flag. (Lịch sử: -5% = 259 ký/phút bị chê nhanh; -18% = 217 ký/phút quá chậm.)
- **Tag `[속]` (nội tâm/속마음): SunHi pitch -10Hz** — mọi script `_TTS.md` PHẢI gắn `[속]` đầu các đoạn nội tâm (tính toán trong đầu, chửi thầm, tự nhủ) khi viết/bàn giao; bài 01 đã gắn 20 đoạn làm mẫu. Tag áp cả đoạn văn.
- **Tag `[감]` (nhịp cảm xúc 정/cao trào — user chốt 2026-07-15, bài 02): SunHi pitch -10Hz + đọc CHẬM hơn (rate_delta -7 → hiệu dụng -19%), ngắt nghẹn ở dấu phẩy 430ms, breath-in 180ms đầu câu, nghỉ dài +0.35s sau câu.** Chỉ gắn ở các nhịp thật sự cảm động (thoại rưng rưng, tiếng lòng khóc, kết ấm) — KHÔNG rải toàn bài, narration thường vẫn `[속]`/không tag để giữ nhịp kể. Định nghĩa trong `VOICES["감"]` của `azure_tts.py` (chỉnh cảm xúc mạnh/nhẹ → sửa rate_delta/comma_ms/gap_bonus ở đó). Bài 02 gắn 14 nhịp làm mẫu.

### Render voice — tool chính thức

```
cd E:\Claude\Projects\youtube-kr-romfan
python tools/azure_tts.py 02_SCRIPTS/NN_slug_TTS.md            # → 03_VOICE/NN_slug/{voice.wav, subs.srt, timeline.json}
python tools/azure_tts.py <file> --limit 10                    # test nhanh 10 câu đầu
```

- Tool tự split câu, gọi Azure từng câu (retry 429, delay 0.3s), cache `segs/` — chạy lại chỉ render câu thiếu (resume-safe, đỡ quota).
- Ký tự đã gửi API ghi vào `03_VOICE/QUOTA.log` — canh 500k/tháng.
- Key đọc từ env `AZURE_SPEECH_KEY` hoặc fallback `tools/.azure_key` (gitignored — KHÔNG commit).
- Bài học đã vấp: gọi REST bằng **Python `urllib`**, KHÔNG dùng curl trên git-bash — hỏng encoding tiếng Hàn (HTTP 200 nhưng 0 byte).
- Nghe mẫu pipeline (SunHi + InJoon đan nhau): `kr_voice_demo/pipeline_test_sunhi_injoon.wav`.

## Độ dài & định dạng

- Video chuẩn 40 phút ≈ **9.000–10.500 ký tự hangul** (±15%), công thức trong skill Mục 5. Batch viết ~4.500 ký tự/lượt. (Transcript nguồn dài hơn thì theo tỷ lệ nguồn — video 01 ≈ 13.2k ký ≈ 60′.)
- Số trong kịch bản: **giữ chữ số Ả Rập + đơn vị đếm** (100억 원, 4시, 300칼로리) — ngược với chouhen (漢数字), vì Azure đọc số Hàn chuẩn.

## Video render (chốt 2026-07-11 sau test video 01)

Pipeline: `azure_tts.py` (voice+subs) → `scene_render.py` (hình+BGM). KHÔNG dùng ambient_render của chouhen (dính engine AivisSpeech).

```
cd E:\Claude\Projects\youtube-kr-romfan
python tools/azure_tts.py 02_SCRIPTS/NN_slug_TTS.md --rate -5      # voice chuẩn kênh
python tools/fetch_bg.py                                            # tải thêm clip cozy nếu _bg chưa đủ
python tools/scene_render.py NN_slug                                # video full → 04_VIDEO/NN_slug/NN_slug.mp4
python tools/scene_render.py NN_slug --scenes 3 --suffix _test      # test ngắn
```

- **Visual chuẩn kênh (user chốt 2026-07-11): 20–25 cảnh nền ĐỘNG luân phiên / video ~1h** (`scene_render.py` mặc định ~22 cảnh/giờ, chia đều, fade 0.8s hai đầu mỗi cảnh) — chống flag inauthentic "nền loop + giọng AI". Mood clip: cozy/romance (mưa cửa sổ, phòng đèn ấm, nến, bokeh phố đêm, trăng mây, cà phê, fairy lights, hoa anh đào…), nguồn Pexels qua `tools/fetch_bg.py` → `04_VIDEO/_bg/` + `SOURCES.md` (free thương mại, không cần attribution). Thứ tự cảnh shuffle deterministic theo slug → mỗi video một chuỗi visual khác nhau.
- **CHÍNH SÁCH BỘ CLIP (SỬA 2026-07-16 — theo `.claude/rules/media-library.md`, thay luật cấm trùng cứng 2026-07-11):** ƯU TIÊN mỗi video một bộ clip khác nhau; **tái dùng lẻ được khi cần** (không còn cấm), chỉ cấm lặp NGUYÊN BỘ giống hệt video trước. `scene_render.py` giữ nguyên: đọc `_bg/USAGE.log`, ưu tiên clip chưa dùng, thiếu tái dùng kèm cảnh báo; bản chính thức tự ghi log (bản `_test`/`_demo` không tính). → **Trước MỖI video mới: chạy `python tools/fetch_bg.py` để có ~22 clip chưa dùng — tool tự CHECK KHO CHUNG `Projects/_media_library` trước (hardlink, 0 tải), thiếu mới tải Pexels và nhập kho** (mood đổi theo tông truyện: mưa/tuyết/biển đêm/lá thu/nến/đèn phố…).
- ⚠️ Render video full qua Claude: chạy DETACHED (Start-Process + log file) — bài học chouhen 2026-07-09, task nền harness bị kill ở phút 10.
- **BGM chuẩn kênh: `04_VIDEO/bgm/Heartwarming.mp3`** (Kevin MacLeod, CC BY 4.0 — BẮT BUỘC ghi credit trong 설명란: `Music: "Heartwarming" Kevin MacLeod (incompetech.com), CC BY 4.0`). Gain `--bgm-gain -40` (chuẩn toàn hệ thống). Muốn đổi track → xuất demo 80s nghe trước.
- Phụ đề: Malgun Gothic trắng + outline đen mềm, sync từng câu từ subs.srt (style trong `scene_render.py`).

## 🔊 Lớp FX radio-drama (port từ chouhen 2026-07-22 — user duyệt)

Mỗi video có `02_SCRIPTS/<slug>_FX.json` (skill script-kr-romfan Mục 16 tự xuất; format trong docstring `tools/fx_mix.py`) → `scene_render.py` tự thêm: **SFX** (bank `04_VIDEO/_sfx`, sinh bởi `tools/sfx_bank.py`) + **BGM động** (dâng -40→-25dB trước cú lật → cắt phựt im lặng + tim đập; swell -26dB đoạn 사이다 vỡ òa) + **quote card** (font Malgun Gothic; đòn của 나 vàng-viền-đỏ / thoại về 빌런 cyan) + **phụ đề màu nhân vật** (hero `#FFD75E` + tên, villain `#8CEBFF`). Không có FX.json → render y như cũ.
- Video đã render chưa đăng: `python tools/fx_mix.py <slug> --apply` — thay track audio (voice + BGM động + SFX, tự tái tạo tiếng CTA lang kr), -c:v copy, KHÔNG re-render; card + phụ đề màu không áp retro. **Đã áp video 03 (2026-07-22) + repack _upload.** ⚠️ Sau `--apply` PHẢI chạy lại `upload_pack --force` (mp4 đổi inode, hardlink gói cũ thành mồ côi).
- SFX synth ffmpeg có tầng mid 200–600Hz (bài học chouhen: chỉ dải trầm = "không rõ" trên loa nhỏ). Gain chuẩn: sting -5…-7, tim/rung -8…-9, CTA -10; master alimiter 0.95.

## Thumbnail (chốt 2026-07-13 sau video 01)

- ⭐ **3 nguyên tắc gác cổng HÌNH (user chốt 2026-07-16, mọi kênh — mục 0.5 `youtube-jp-shokutaku/02_THUMBNAIL_TITLE_RULES.md`):** ① 1 điểm nhấn duy nhất, cắt chi tiết thừa, tương phản cao ② phóng đại CẢM GIÁC ③ 120px vẫn rõ — nền đậm, chủ thể sáng.
- Chuẩn kênh: **ảnh thật Pexels** (nhân vật/mood đúng fantasy cốt lõi truyện) + text 3 tầng theo KHỐI 3 của script — render bằng `tools/make_thumb.py` (băng trên trắng + dòng key cực to nhấn ĐỎ double-stroke, băng đáy vàng, font Malgun Gothic Bold, chừa mặt nhân vật). Ảnh ứng viên tải về `04_VIDEO/<slug>/_thumb_candidates/` + `SOURCES.md`, duyệt contact sheet bằng mắt rồi chọn.
- ⚠️ **KHÔNG in badge thời lượng góc thumbnail** (user chốt 2026-07-13 — YouTube tự hiện duration, in thêm là thừa). `make_thumb.py` mặc định tắt; đừng truyền `--dur` trừ khi user yêu cầu rõ.
- Tự duyệt trước khi giao: che chữ vẫn ra đúng chủ đề / preview 120px đọc được dòng key / quét từ demonetize theo `.claude/rules/youtube-compliance.md`. Credit 설명란: `영상·썸네일: Pexels (무료 상업용 라이선스)`.

## Thư mục

```
youtube-kr-romfan/
├── 01_SOURCES/    # transcript gốc (Việt/Trung việt hóa) cần bản địa hóa, research
├── 02_SCRIPTS/    # NN_slug.md (script + gói CTR) và NN_slug_TTS.md (bản sạch KHỐI 1)
├── 03_VOICE/      # mp3/wav xuất từ Azure TTS
├── 04_VIDEO/      # video render + thumbnail
└── CLAUDE.md      # file này
```

## Persona kênh

- Tên kênh: **사우 오디오** (CHỐT 2026-07-11 — tên thật kênh của user; 이불속극장 chỉ là persona nháp cũ, đừng dùng lại).
- Chào mở (sau cold open): "사우 오디오에 오신 걸 환영해요. 오늘도 편하게 누워서 들어주세요."
- Kết cố định: "오늘 이야기 여기까지예요. 재미있으셨다면 좋아요와 구독, 잊지 마세요. 사우 오디오였습니다."
- Mô tả video luôn kèm: "본 이야기는 허구이며 등장인물·단체는 실제와 무관합니다." + credit giọng TTS (Azure).

## Vault tương ứng

`E:\Claude\SecondBrain\10_Projects\youtube-kr-romfan\youtube-kr-romfan.md` — research thị trường, bài học, quyết định.
