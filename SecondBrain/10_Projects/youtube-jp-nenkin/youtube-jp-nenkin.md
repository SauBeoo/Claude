# youtube-jp-nenkin

Folder-note tri thức cho kênh YouTube **年金・老後資金** (JP 50–70). Repo code/script: `E:\Claude\Projects\youtube-jp-nenkin\`.

## Bối cảnh quyết định (2026-07-19)

- Ra đời từ vòng research "top 10 chủ đề JP 45–65": tiền hưu = nỗi bất an #1 (65%+ lo thiếu; 60代 91,4% nói tiết kiệm không đủ) mà hệ thống 6 kênh chưa phủ.
- Đo Trends JP cùng ngày: 年金 = 73 điểm thang 卵=78 (≈2,8× trụ 血圧 của kênh health) — chi tiết `Projects/youtube-jp-nenkin/01_KEYWORD_RESEARCH.md`.
- User chốt mở kênh mới thay vì chuyển hướng shokutaku; script 腎臓に良い食べ物 bên health tạm hoãn.

## Nguồn khảo sát nền (tra 2026-07-19)

- MONEY DESIGN — 65%+ bất an 老後資金: https://www.money-design.com/news/detail.php?id=325
- 松井証券 — 60代 91,4% "tiết kiệm không đủ": https://www.matsui.co.jp/company/research/20201022.html
- SBIエフィナンス — nỗi lo tuổi già #1 sức khỏe #2 tiền: https://www.sbi-efinance.co.jp/contents/anxiety_of_50s/
- DIA — báo cáo 老後資金 50/60/70代: https://dia.or.jp/disperse/research_report/pdf/research_report_87.pdf
- Đối thủ: 年金・給付金完全攻略チャンネル (giải thích chế độ faceless) · ひよっこシニア/ようこの年金暮らし (vlog) · 年金リアルどきゅめんと/梅子の年金トーク (phỏng vấn phố).

## Bài học / research

### 2026-07-23 — Khóa 3 trụ (pivot lớn nhất đời kênh)
Kênh = TÍNH SỐ HỘ cụ già: ① 年金 tính số · ② 給付金・取り逃し · ③ 税・社会保険料. ⛔ Cắt hẳn 不動産 + 金融商品 (iDeCo/NISA/bảo hiểm). Bằng chứng chọn precision-model: 年金・給付金完全攻略 **12 video → 130K sub**; きな子のシニアお金ゼミ 167K chỉ làm 年金/税. Ranh giới với ngách chờ kaigo: nenkin = tiền hưu CỦA MÌNH, kaigo = tiền chăm BỐ MẸ.

### 2026-07-25 — Kế hoạch nâng cấp "content là vua" (2 Plan agent độc lập nhất trí)
- **Phán quyết: kênh KHÔNG sai hướng** — 3 trụ phủ 100% topic viral đã proven của ngách; signature 研究室 (cast 7 モニター cố định + 研究ノート + 視聴者の実験室) là moat đối thủ không có. Bệnh = bệnh loại 1 (0 impressions, khâu phân phối/thực thi), không phải content.
- **Sửa 4 điểm thực thi:** front-load 7 topic proven trong 15 video đầu (定期便に載らない 3.79M = ưu tiên #1) · lịch 3/tuần T2·T4·T6 19:00 JST cold-start (sync 4 nguồn, desc kênh đã sửa qua API) · độ dài 18–25′ theo benchmark ngách (KHÔNG theo "shorter wins" của ngách food) · script 03 mổ bỏ chương NISA/iDeCo (viết 20/07 trước lệnh khóa trụ 23/07 — bài học: script cũ phải rà lại sau mỗi pivot).
- **Roadmap 90 ngày 33 video + 6 franchise** (⭐支給日直前チェック 6 kỳ/năm là franchise mạnh nhất — gắn nghi thức ngày tiền về, chưa đối thủ nào làm): `Projects/youtube-jp-nenkin/02_CONTENT_PLAN.md`.
- **Hạ tầng đúc thành khuôn:** skill `script-nenkin` (FACT SHEET FIRST — bài học script 03 kẹt kho vì viết xong mới verify) · tool `make_thumb.py` riêng + badge navy/vàng 「年金研究室」 + sổ xoay 8 khuôn · vòng đo tuần `08_ANALYTICS_LOG.md` với khung 3 bệnh (0 impr = volume; impr cao CTR <3% = packaging; CTR ok retention sập = script).
- **Chống bẫy tâm lý:** benchmark 長生きの秘訣 flop 30 video/2 tháng trước khi nổ; hit rate ngách ~1/5 → KHÔNG pivot trước video 15–20. Checkpoint đọc số lớn đầu tiên: sau video ~15 (~cuối tháng 8).
- Nguồn sự thật backfill tầng kênh (rổ 12 tag + 3 hashtag + cat 27): `Projects/youtube-jp-nenkin/CHANNEL_BACKFILL_2026-07-25.md`.

### 2026-07-25 (chiều) — ĐO BENCHMARK NGÁCH: 3 giả định bị lật
User hỏi *"ngách này nhiều kênh lớn làm rồi, đi hướng này ổn không?"* → đo API 9 kênh ngách, xếp theo **sub/tháng**. Hồ sơ: `Projects/youtube-jp-nenkin/CHANNEL_BENCHMARK_2026-07-25.md`.
1. **Ngách đang MỞ RỘNG, không bão hòa.** 3 kênh tăng nhanh nhất đều lập ≥2025-06 (完全攻略 31,8K sub/tháng · 元ハロワまゆみ 19,1K · 資産保全学 13,4K); 3 kênh chậm nhất lập 2018–2019. Cầu tăng nhanh hơn cung → kênh lập 2026-07 KHÔNG muộn.
2. **完全攻略 (12 video → 132K) chỉ mới 4,1 tháng tuổi (lập 2026-03).** Trước đây dùng nó làm bằng chứng precision-model mà không biết tuổi → hoá ra nó là *đối thủ cùng thời*, và video top 定期便に載らない 3,79M của nó đang KHỎE. → **Đổi chiến lược xếp hàng đợi: vòng sườn, không đánh trực diện** — GĐ A đi long-tail sâu (加給年金40万, 特別支給時効, 未支給年金) + nhịp chưa ai chiếm (支給日/書類が届く月); mega-evergreen lùi về GĐ C khi đã có uy tín.
3. **Volume là chiến lược THUA — chênh 27 lần hiệu suất/video:** 給付金チャンネル 1.971 video → 87K sub (17,8K view/video) vs 完全攻略 12 video → 132K (490K view/video). → **hạ nhịp 3/tuần → 2/tuần T2·T4**, dồn công vào chất lượng.

**Móc định vị — phát hiện quan trọng nhất:** kênh thắng nhanh nhất (元ハロワ職員まゆみ) thắng bằng **uy tín người trong hệ thống** ("tôi từng làm ở Hello Work") = dạng mạnh nhất của motif 役所が教えない. Mình KHÔNG được bịa tư cách (gian dối + YMYL rule #5). Lớp thay thế honest và không ai trong ngách làm: **⭐原典を見せる** — chiếu đúng trang 年金機構/厚労省 lên màn hình, khoanh đỏ con số đang đọc, ≥2 shot/video, shot đầu trong 3 phút đầu. Biến 「原典を一緒に読む」 từ lời nói thành bằng chứng thị giác; kênh persona-giả không dám copy. Đã khắc vào skill `script-nenkin` GĐ0d + chuẩn visual CLAUDE.md + khuôn thumbnail G.
**Phụ:** khung 「学」 của 資産保全学 (174K/13 tháng) validate định vị 研究室 — persona học thuật không lép ở ngách này. Góc 2026年改正 đã bị cày từ T3–4/2026 → dư địa ở mốc hiệu lực SAU (遺族年金 2028, 基礎年金底上げ, 標準報酬上限, 適用拡大).
