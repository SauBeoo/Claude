# CLAUDE.md — youtube-jp-nagaiki（長生きごはんの知恵袋）

Kênh faceless **食べ合わせ・食べ方 cho người Nhật 60–80 tuổi**. Sinh 2026-08-01 từ cái chết của kênh health (みんなの健康ノート) — project này tồn tại để **chạy lại ngách bằng đúng những gì đã chứng minh THẮNG, và không lặp lại bất kỳ sai lầm nào đã trả giá bằng số**.

- **Kênh:** 長生きごはんの知恵袋 · @nagaiki-gohan · `UCBkpkLFZoj5gl4NzKmOC3zQ` · Gmail saubeooo04 / Chrome **Profile 13** (brand thứ 2, kênh health cũ vẫn nằm cùng Gmail — ĐÓNG BĂNG, không đăng thêm)
- **categoryId 27 Education** (đo 2026-08-01: 2 kênh benchmark 5/5 video đều 27 — KHÔNG copy 26 của health)
- ⏸⏸ **KÊNH ĐÃ BỎ KHỎI LỊCH ĐĂNG — 2026-08-03** (user chốt: *"kênh 長生きごはんの知恵袋 bỏ đi"*). `slots: []` trong `upload_pack.py`. **health được bật lại 3/tuần T3·T5·CN 19:00 thay chỗ** (health dời vào ĐÚNG bộ ngày này để cân tải sau khi nagaiki rời lịch → bật lại nagaiki là đụng trực tiếp ngày+giờ của health) — hai việc này là MỘT quyết định (cùng tệp senior JP, **cùng Gmail saubeooo04 / Chrome Profile 13**), bật lại kênh này thì phải hạ health cùng lúc, không thì 2 kênh cùng nhà cùng đăng. Chưa có video nào lên sóng (`06_VIDEO/28_kuroyanagi-tetsuko` render xong, chưa đăng) → không có video mồ côi. Repo + `credentials/` + `channel_id` + branding GIỮ nguyên; bật lại = trả `slots` về `[(1,19),(3,19),(6,19)]`. 🔴 **Bệnh gốc không mất theo kênh:** lý do mở kênh này là retention 60 giây đầu của health ở đáy phân vị 10–20% — bỏ kênh mới thì health nhận 3 slot/tuần với đúng bệnh cũ. Nguồn: `.claude/rules/upload-schedule.md` §0.9c.
- ~~**Lịch:**~~ (đã bỏ) ⭐⭐ **T3·T5·CN 19:00 JST · 3 video/tuần** (ĐỔI 2026-08-03 — user chốt nhịp toàn hệ thống *"2 ngày 1 video cho tất cả các kênh"*, đè mốc 1/tuần khởi điểm ở §6/§2.2). Giữ T5 trong bộ vì đó là ngày duy nhất có căn cứ đo (若返りアカデミア 17/18 video); bộ ngày **B** để không chồng ngày với health (bộ A T2·T4·T6) — 2 kênh cùng tệp + cùng Gmail. ⚠️ Kênh 2 ngày tuổi, chưa có số phân phối nào → đây là **phép thử nhịp**, và §2.2 ("đăng dày vào kênh chưa mở vòi = tự đào hố") **vẫn đúng, chỉ là user chọn ưu tiên đều đặn**. Chỉ đăng nội dung CHƯA TỪNG public. Nguồn sự thật: `.claude/rules/upload-schedule.md` Mục 0.9
- Token API: `credentials/token.json` (đã auth đúng kênh brand 2026-08-01). ⚠️ Token của health trỏ kênh CŨ — đừng lẫn project khi upload.

---

## §1 TINH HOA — công thức 食べ合わせ (nguồn: `../youtube-jp-health/BENCHMARK_RIVALS_2026-07-29.md` §7)

Network 2 kênh cùng xưởng đo được 2026-07-29 — **cùng kênh, cùng tuần, chỉ khác đề tài**:

| Nhóm ĂN (5/5 nổ) | View | Nhóm CHẾT (5/5 xịt) | View |
|---|---|---|---|
| 納豆×5倍 | **45.151** | 腎臓に悪い5選 | 2.581 |
| にんじん×食べ方 | 38.802 | 血糖値7選 | **136** |
| はちみつ×食べ方 | 30.230 | ハミング血管 | 982 |
| 麦茶+〇〇 | 25.724 | 健康食品 | **14** |

Bằng chứng kênh mới sống được: **健康栄養研究室 lập 2026-07-20 → 9 ngày = 516 sub / 45K view** với đúng công thức này.

**Khuôn mỗi video (bám đủ 6 khóa):**
1. **Đề tài = 1 MÓN quen, rẻ, có sẵn trong bếp** (納豆・にんじん・はちみつ・麦茶・きのこ・甘酒…) × **「cách ăn đang phí X% / đang phản tác dụng」**. ⛔ CẤM đề tài theo TẠNG/CHỈ SỐ (腎臓・血糖値・血管・脳ランキング) — nhóm CHẾT có số ở trên.
2. **Title:** 【知らないと損】/【実は逆効果】/【9割が知らない】 + tên món + con số compliance-safe (5倍/半分/3割). Keyword = **TÊN VẬT** đứng đầu (đo thật: すだれ 42 vs 電気代節約 5).
3. **Thumbnail:** đáp án CHE (hộp cyan/？) + khuôn 45+ (§3.4).
4. **Cold open ≤60s** nhưng ruột là **3 triệu chứng 「〜ませんか？」 → 「実は、食べ方が間違っているんです」** — đâm vào người xem, không giảng.
5. **Dài 22–27 phút.**
6. **≥1 khối genten** (厚労省/消費者庁/学会 — tên cơ quan + 年月 + số trích đúng) = moat + giá trị gốc; bảng số dùng `make_drawn.py` cặp hỏi→đáp (「？」 trong 60s đầu → khoanh đỏ ở 80%).

## §2 SÁU SAI LẦM ĐÃ TRẢ GIÁ — mỗi cái một con số, CẤM lặp lại

1. **Retention 60 giây đầu giết cả kênh.** Health relPerf@60s = 0,10–0,14 → YouTube đốt 18,6K impressions test rồi khoá vòi CẤP KÊNH: 5.500 → 61 → 10 → **1** impressions/video trong 8 ngày. Video sau đó dù sửa hết (video 22) chỉ được phát **3 impressions** — phép thử không bao giờ được chấm nữa. → **Gate cold open là sống còn, không phải thủ tục.**
2. **Đăng dày vào kênh chưa mở vòi = tự đào hố.** Health 4/tuần, shokutaku 7/tuần (BROWSE=0 tuyệt đối), co-dai 8 video/15 ngày = 36 view. Mỗi video thêm 1 mẫu retention xấu vào điểm trung bình kênh. → **1/tuần cho đến khi rail mở (§6).**
3. **Đề tài đúng ngách nhưng sai LOẠI vẫn chết.** Cùng kênh đối thủ: món quen 45K view, listicle tạng 136 view, cách nhau 330 lần. → chỉ làn ĂN (§1.1).
4. **Benchmark số cũ / kênh đang sụp = số rác.** 長生きの秘訣 median 110K (01/2026) → 2.430 (07/2026), sụp 45× không đổi gì; nhìn video 3-4 năm tuổi của nó mà học là học xác chết. → **chỉ đo video ≤30 ngày, xếp theo view/ngày, lọc Shorts, đo lại mỗi 4–6 tuần.**
5. **Thumbnail đúng gu mình, sai mắt người 60-80.** Moody/tối bị kết án 07-21; chữ mảnh 4 dòng (R1 SLIM) bị luật 45+ đảo 07-30. → khuôn §3.4, gate 168px không nhân nhượng.
6. **Đăng lại nội dung đã public = inauthentic (mất kênh).** Đây là lý do kênh này CHỈ nhận video 28 + script 23/25/27 (chưa từng public) — **cấm tuyệt đối bê video 05–22 của health sang**, kể cả đổi title.

Bài học vận hành đi kèm (đã thành rule chung, chỉ trỏ): bẫy resume render ra hình cũ (`render-background.md` §2.5 — đọc log tìm dòng `CŨ HƠN → render lại`) · sửa lời = sửa 3 chỗ (`humanize-script-voice.md` §4) · UPLOADED.txt không phải sự thật của kênh (`upload-schedule.md` §1.5) · "đẩy lên kênh" = đẩy đúng thứ vừa làm.

## §3 GATE BẮT BUỘC trước khi render / đăng (thiếu 1 = dừng)

1. **Cold open:** `python ../youtube-jp-health/tools/check_coldopen60.py <script>` — mục đầu ≤60s (≤306 ký trước nhãn mục đầu); 60s đầu cấm câu điều kiện/miễn trừ/credential; **cấm 外来語 trong 60s đầu + title + thumbnail** (trừ từ đã ngấm: ビタミン・スマホ…).
2. **Lớp hình mang thông tin:** `check_slides_visual.py` — V1 trang drawn có 「？」 trong 60s đầu · V2 `circle` đáp án ở 70–95% · V3 ≥1 khối genten.
3. **Chất người:** ≥4/6 mũi tiêm + 15–25 tag 速/抑揚/間 (đầu dòng!) — `humanize-script-voice.md`. **Render demo voice 1–2 đoạn nghe trước** khi render cả bài.
4. **Thumbnail 45+:** dòng chính ≤6 ký, cao ≥1/3 khung, ≤3 dòng, ≥1 mặt biểu cảm rõ, nền sáng, đáp án che; mở `*_preview168.png` đọc được chữ + biểu cảm mới giao. Quy trình: Claude đưa prompt → user gen → duyệt 3 cửa.
5. **Asset:** tải MỚI 100% (sổ đen `_media_library`), hình đầu tiên = CHỦ THỂ món, người trong ảnh = châu Á, **duyệt contact sheet bằng mắt trước render**.
6. **Âm lượng:** chuẩn -14 LUFS, BGM -40dB.
7. **Trước mọi cú ghi lên kênh:** trình user + được gật trong lượt đó; đối chiếu kênh thật (`find_on_channel`) trước upload.

## §4 PIPELINE LỆNH

```bash
# Viết/soát script (skill script-healthy làm nền + khuôn §1) → 04_SCRIPTS/<NN>_<slug>.md + _TTS.md + _SLIDES_photo.json
# Render (LUÔN chạy nền, bọc .cmd + log — render-background.md):
cd E:\Claude\Projects\youtube-jp-nagaiki
python ..\youtube-jp-health\tools\video_render.py 04_SCRIPTS\<x>_TTS.md --channel nagaiki
# Đóng gói + upload:
python ..\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel nagaiki
python ..\youtube-jp-chouhen\tools\upload_api.py <slug> --channel nagaiki --dry-run   # xem trước rồi mới bấm thật
# Khám kênh (traffic/retention; impressions đọc tay Studio):
python ..\youtube-jp-health\tools\channel_diag.py --start <date>
```
Hồ sơ render `nagaiki` trong `../youtube-jp-health/tools/channels.py`: giọng **青山龍星/しっとり/0.9**, pill 22, watermark ごはんの知恵袋, ảnh tĩnh + pan ease. ⚠️ Palette/drawn đang kế thừa health — **chốt lại cùng user khi duyệt demo video đầu.**

## §5 TỒN KHO & THỨ TỰ ĐĂNG

Chuyển từ health sang 2026-08-01 (làn ĂN + pilot 人物; 24/26 loại chết ở lại health):

| # | Script | Làn | Trạng thái | Thứ tự đề xuất |
|---|---|---|---|---|
| 23 | きのこ×骨 | ĂN | script xong, cold open đã vá — **soát lại theo §1 đủ 6 khóa + repackage title/thumbnail** | **video 1** |
| 25 | にんじん×油 | ĂN | như trên | video 2 |
| 27 | 甘酒 | ĂN | như trên | video 3 |
| 28 | 黒柳徹子 92歳 | 人物 (pilot) | **ĐÃ RENDER** (`06_VIDEO/28_kuroyanagi-tetsuko/`) — repackage metadata theo kênh mới | video 4 (đo format 人物 sau khi làn ĂN có số) |

⚠️ Script 23/25/27 viết trước khi có công thức §1 — trước khi render PHẢI: đối chiếu 6 khóa (nhất là ruột cold open 3 triệu chứng + đề tài đóng khung 「食べ方が間違っている」), retitle theo khuôn 【】, thumbnail mới theo §3.4. Video 28 đã render thì giữ nguyên ruột, chỉ đóng gói lại.

## §6 LỊCH & ĐIỀU KIỆN TĂNG NHỊP

- ⭐⭐ **THI HÀNH TỪ 2026-08-03: T3·T5·CN 19:00 JST, 3 video/tuần** (user chốt nhịp toàn hệ thống, đè mốc 1/tuần dưới đây). Điều kiện tăng ở dòng kế **không còn là cửa để tăng lên 2/tuần** — đã ở 3/tuần; nó đổi vai thành điều kiện để **giữ** nhịp: thiếu cả 3 điều mà view vẫn 0 → hạ về 1/tuần `[(3,19)]`.
- (căn cứ cũ) **T5 19:00 JST, 1 video/tuần.** Căn cứ: 若返りアカデミア (benchmark long-form duy nhất còn thắng ngách cũ) khóa T5 17/18 video; và sai lầm §2.2.
- **Tăng lên 2/tuần chỉ khi đủ 3 điều** (nguyên tắc đúc từ chouhen): ① rail mở (BROWSE/SUGGESTED > 0 ổn định) ② retention khỏe (còn ≥50% @60s trong Studio) ③ ngách thưởng volume (đối thủ đăng dày mà không sụt). Thiếu 1 = giữ 1/tuần.
- Mỗi video sau 72h: đọc số bằng `channel_diag.py` + Studio (impressions đọc tay — API đã bị Google rút metric này từ 2026-07-30). Ghi vào `08_ANALYTICS_LOG.md` (tạo khi có video đầu).

## §7 LUẬT CHUNG (trỏ, không chép)

Compliance từ ngữ/disclosure: `.claude/rules/youtube-compliance.md` · Khán giả 45+: `audience-45plus.md` · SEO upload + đo trend trước metadata: `youtube-upload-seo.md` · CTA giữa video (dùng câu canonical **health** mục 2.3 tạm — viết câu riêng cho kênh khi làm video đầu): `cta-midvideo.md` · Media/sổ đen: `media-library.md` · Render nền: `render-background.md` · Lớp thủ công: **ĐÃ BỎ 2026-08-09** (`handmade-layer.md`) · Chất người: `humanize-script-voice.md`.

Disclaimer 概要欄 mọi video: miễn trừ y tế + credit VOICEVOX 青山龍星 + BGM/ảnh.

## Vault tương ứng
`E:\Claude\SecondBrain\10_Projects\youtube-jp-nagaiki\` — hồ sơ vì-sao-có-kênh-này nằm ở đó; chẩn đoán gốc: `../youtube-jp-health/CHANNEL_DIAGNOSIS_2026-08-01.md`.
