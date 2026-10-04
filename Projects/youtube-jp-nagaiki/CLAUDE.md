# CLAUDE.md — youtube-jp-nagaiki（長生きごはんの知恵袋）

⏸⏸ **KÊNH ĐÃ BỎ KHỎI LỊCH ĐĂNG 2026-08-03** (user chốt) — `slots: []` trong `upload_pack.py`. Health được bật lại 3/tuần T3·T5·CN 19:00 thay chỗ. Nguồn: `.claude/rules/upload-schedule.md` §0.9c.

Kênh faceless **食べ合わせ・食べ方 cho JP 60–80**, sinh 2026-08-01 thay kênh health.

- **Kênh:** 長生きごはんの知恵袋 · @nagaiki-gohan · `UCBkpkLFZoj5gl4NzKmOC3zQ` · Gmail saubeooo04 / Chrome **Profile 13** (cùng Gmail với health)
- **categoryId 27 Education** (đo benchmark 2026-08-01, KHÔNG copy 26 của health)
- Token API: `credentials/token.json` (đã auth đúng kênh brand). ⚠️ Token của health trỏ kênh CŨ — đừng lẫn project khi upload.

## BẬT LẠI KÊNH — điều kiện (một quyết định, không sửa lẻ)

Bật lại nagaiki = trả `slots` về `[(1,19),(3,19),(6,19)]` **VÀ hạ health cùng lúc** (cùng tệp senior JP, cùng Gmail/Profile 13; health đang chiếm đúng bộ ngày T3·T5·CN 19:00). Xem `upload-schedule.md` §0.9c. Repo + `credentials/` + `channel_id` + branding GIỮ nguyên. Chưa có video nào lên sóng (`06_VIDEO/28_kuroyanagi-tetsuko` render xong, chưa đăng).

⛔ **CẤM tuyệt đối bê video đã public của health (05–22) sang**, kể cả đổi title — inauthentic content (`youtube-compliance.md` §1). Kênh chỉ nhận nội dung CHƯA TỪNG public: video 28 + script 23/25/27.

## §1 CÔNG THỨC 食べ合わせ (nguồn: `../youtube-jp-health/BENCHMARK_RIVALS_2026-07-29.md` §7)

Khuôn mỗi video, đủ 6 khóa:
1. **Đề tài = 1 MÓN quen, rẻ, có sẵn trong bếp** (納豆・にんじん・はちみつ・麦茶・きのこ・甘酒…) × 「cách ăn đang phí X% / phản tác dụng」. ⛔ CẤM đề tài theo TẠNG/CHỈ SỐ (腎臓・血糖値・血管・脳ランキング) — nhóm này đo được chết (136 view vs 45K của món quen).
2. **Title:** 【知らないと損】/【実は逆効果】/【9割が知らない】 + tên món + con số compliance-safe. Keyword = **TÊN VẬT** đứng đầu.
3. **Thumbnail:** đáp án CHE (hộp cyan/？) + khuôn 45+ (§3.4).
4. **Cold open ≤60s**, ruột = 3 triệu chứng 「〜ませんか？」 → 「実は、食べ方が間違っているんです」.
5. **Dài 22–27 phút.**
6. **≥1 khối genten** (厚労省/消費者庁/学会 — tên cơ quan + 年月 + số trích đúng); bảng số dùng `make_drawn.py` cặp hỏi→đáp (「？」 trong 60s đầu → khoanh đỏ ở 80%).

## §2 SAI LẦM ĐÃ TRẢ GIÁ — CẤM lặp lại (tóm)

1. Retention 60s đầu giết cả kênh (health bị khoá vòi cấp kênh) → gate cold open là sống còn.
2. Đăng dày vào kênh chưa mở vòi = tự đào hố.
3. Đề tài đúng ngách nhưng sai LOẠI vẫn chết → chỉ làn ĂN.
4. Benchmark kênh đang sụp = số rác → chỉ đo video ≤30 ngày.
5. Thumbnail moody/chữ mảnh bị kết án → khuôn 45+, gate 168px.
6. Đăng lại nội dung đã public = inauthentic (mất kênh).

Vận hành: `render-background.md` §2.5 (resume ra hình cũ) · `humanize-script-voice.md` §4 (sửa lời = 3 chỗ) · `upload-schedule.md` §1.5 (UPLOADED.txt không phải sự thật kênh).

## §3 GATE trước render/đăng (thiếu 1 = dừng)

1. Cold open: `python ../youtube-jp-health/tools/check_coldopen60.py <script>` — mục đầu ≤60s; cấm 外来語 trong 60s đầu + title + thumbnail.
2. Lớp hình: `check_slides_visual.py` (V1 「？」 60s đầu · V2 circle 70–95% · V3 genten).
3. Chất người: ≥4/6 mũi tiêm + 15–25 tag (`humanize-script-voice.md`); render demo voice trước.
4. Thumbnail 45+ (`audience-45plus.md` §1): ≤6 ký, ≥1/3 khung, ≤3 dòng, mặt biểu cảm, nền sáng, gate 168px. Claude đưa prompt → user gen → duyệt.
5. Asset tải MỚI 100% (sổ đen `media-library.md`), hình đầu = CHỦ THỂ món, người châu Á, duyệt contact sheet trước render.
6. Âm lượng -14 LUFS, BGM -40dB.
7. Trước mọi cú ghi lên kênh: trình user + đối chiếu kênh thật (`find_on_channel`).

## §4 PIPELINE LỆNH

```bash
cd E:\Claude\Projects\youtube-jp-nagaiki
python ..\youtube-jp-health\tools\video_render.py 04_SCRIPTS\<x>_TTS.md --channel nagaiki   # LUÔN chạy nền (render-background.md)
python ..\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel nagaiki
python ..\youtube-jp-chouhen\tools\upload_api.py <slug> --channel nagaiki --dry-run
python ..\youtube-jp-health\tools\channel_diag.py --start <date>
```
Hồ sơ render `nagaiki` trong `../youtube-jp-health/tools/channels.py`: giọng **青山龍星/しっとり/0.9**, watermark ごはんの知恵袋, ảnh tĩnh + pan ease. ⚠️ Palette/drawn kế thừa health — chốt lại cùng user khi duyệt demo video đầu.

## §5 TỒN KHO

23 きのこ×骨 · 25 にんじん×油 · 27 甘酒 (làn ĂN, script xong — trước render phải soát 6 khóa §1 + retitle + thumbnail mới) · 28 黒柳徹子 (人物 pilot, ĐÃ RENDER — chỉ đóng gói lại metadata).

## §6 LUẬT CHUNG (trỏ)

Compliance: `youtube-compliance.md` · 45+: `audience-45plus.md` · SEO: `youtube-upload-seo.md` · CTA giữa video (tạm dùng câu health mục 2.3): `cta-midvideo.md` · Media: `media-library.md` · Render nền: `render-background.md` · Chất người: `humanize-script-voice.md`. Disclaimer 概要欄: miễn trừ y tế + credit VOICEVOX 青山龍星 + BGM/ảnh.

Vault: `E:\Claude\SecondBrain\10_Projects\youtube-jp-nagaiki\` · chẩn đoán gốc: `../youtube-jp-health/CHANNEL_DIAGNOSIS_2026-08-01.md`.

> Bản đầy đủ: ./_archive/CLAUDE_FULL_2026-08-24.md
