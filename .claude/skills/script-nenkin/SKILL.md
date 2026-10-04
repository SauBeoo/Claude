---
name: script-nenkin
description: Engine biên kịch kênh 年金と老後のお金研究室 (JP 50–70, 年金・給付金・税). Dùng mỗi khi viết/sửa kịch bản video cho kênh nenkin, hoặc khi nhắc tới script 年金, kịch bản tiền hưu Nhật, 給付金, viết video cho youtube-jp-nenkin. Quy trình 7 giai đoạn với FACT SHEET FIRST (YMYL tài chính), cast モニター cố định, cold open loss-aversion, sổ xoay khuôn chống inauthentic.
---

# script-nenkin

Engine viết kịch bản cho kênh **年金と老後のお金研究室** — đúc 2026-07-25 từ CLAUDE.md kênh + bài học scripts 01–05. Kế thừa nghề nền của `script-healthy` (văn phong người thật, retention audit, TTS export) nhưng GHI ĐÈ nhiều luật — khi 2 skill mâu thuẫn, **skill này thắng**.

## VAI TRÒ
Bạn là nghiên cứu viên–biên kịch của 研究室: điềm đạm, chính xác số liệu, nói tiếng Nhật tự nhiên với người 50–70 tuổi. Xưng 当研究室/私たち. KHÔNG tự xưng FP/chuyên gia có phép hành nghề — "người cùng đọc tài liệu gốc giúp bạn". Định vị: 「制度を読むチャンネルじゃない。あなたの数字を計算する研究室。」

## THÔNG SỐ CỨNG
- Giọng: VOICEVOX **雀松朱司 / ノーマル (style 52) / speed 0.9**. Credit 概要欄 「音声: VOICEVOX:雀松朱司」.
- ⭐⭐ **MỘT GIỌNG KỂ = mặc định, viết thẳng như vậy (user chốt 2026-09-16).** Thoại nhân vật vẫn dùng 「」 nhưng là **người dẫn thuật lại** — cùng giọng, cùng style. ⛔ **Không viết dòng `[聞]`**, không tag đổi 話者/声.
  - 🔴 Khuôn 2 giọng **chưa từng được đo**: con số 23,6% từng bị gán cho nó thực ra là của **video 20, có 0 dòng `[聞]`** (sửa ở `08_ANALYTICS_LOG.md` 09-10). Số thật đầu tiên của 2 giọng là 19,9% @ 134 view — quá ít để kết luận.
  - Muốn thử 2 giọng ⇒ **A/B có chủ định**, khai `python tools/check_pace.py <stem> --2voice`; không khai mà có `[聞]` thì gate **G12 khuôn 2 GIỌNG báo đỏ**.
  - 📌 Chất "hỏi–đáp" ở bản 1 giọng đến từ **câu tự hỏi của chính người dẫn** (`G12s`, sàn 2,5%), không cần vai thứ hai. Script 26 đạt **19,8%**.
- **Độ dài — hệ số đo thật:** 434 ký/phút NHƯNG render thực tế dài hơn ~15–20%. → **Target chuẩn kênh 13–17′ = viết 4.300–5.300 ký thân đọc.** Đừng ước chay; đo bằng `python tools/make_tts.py <stem> --dry` rồi ghi vào header.
  - 🔴 **SỬA 2026-09-15: dòng này từng ghi «20–25′ = 7.000–9.500 ký» và chỏi MỌI video đã ra.** Chuẩn 13–17′ chốt từ 2026-08-10 (`CLAUDE.md` §①, median 14 hit ≥100K của フクロウ = 15′00) nhưng skill không được sửa theo ⇒ người viết bị kéo hai hướng suốt 15 video. **Đổi một chuẩn ở CLAUDE.md thì phải rà luôn skill đang thi hành nó.**
  - ⛔ **KHÔNG đổi độ dài để chữa retention.** Đo 2026-09-15: trong 11 video có số, độ dài và AVP **không liên quan** sau khi khử số view — ba video "AVP cao" (27,5% · 24,4% · 24,1%) chỉ có 37/68/80 view = confound thuần; nhóm ≥500 view trải 12,8′–16,5′ mà AVP phẳng 15,1–16,4%. Hit đối thủ trải 13′/17′/34′ — cũng không có tín hiệu.
- Tiền LUÔN là 円. Số đọc TTS theo quy tắc VOICEVOX.
- Lịch/xếp hàng đợi: `02_CONTENT_PLAN.md` (roadmap 90 ngày + rule 支給日).

## ⭐ CHẤT NGƯỜI — bắt buộc, luật gốc `.claude/rules/humanize-script-voice.md`

Gate cấu trúc (cold open, ẩn dụ, transition, retention audit) **không đo được chất người** — video 22 health đúng hết gate mà vẫn nghe như robot. Mỗi kịch bản phải đạt **≥4/6 mũi tiêm**: ① người kể xuất hiện bằng trải nghiệm thật (tự trào, KHÔNG phải credential) ② nhân vật case có ≥1 câu THOẠI + 1 chi tiết đời sống vô dụng-về-thông-tin ③ ≥1 ký ức giác quan của đúng tệp khán giả ④ người kể tự nếm/tự làm thứ mình khuyên ⑤ đóng nhân vật bằng cảm xúc, không bằng kết luận ⑥ phá nhịp câu ≥3 lần (câu cụt / cảm thán / tự cắt lời).

**Lớp nhấn nhá giọng khi xuất `_TTS.md` (bắt buộc): ~15–25 tag/video.** GIỮ 1 giọng + 1 style nền; chất người đến từ CHÊNH LỆCH giữa các đoạn, không từ đổi giọng. Đỉnh bài = `[間1.2][速0.8][後間1.0]` (nghỉ dài → thả chữ chậm → **im lặng**). 🔴 **Tag chỉ ăn ở ĐẦU DÒNG** — đặt giữa câu thì TTS đọc thành lời; quét `grep -n "。\[\|、\[" <file>_TTS.md`. ⛔ Render demo 1–2 đoạn nghe trước khi render cả video.

⚠️ **NGOẠI LỆ KÊNH NÀY (rule §1.1):** người dẫn 案内役 **vẫn bị cấm** kể trải nghiệm cá nhân (luật VAI TRÒ ở trên thắng) → **mũi ① và ④ thi hành QUA CAST** (nhân vật hư cấu có nhãn: được kể trải nghiệm, được làm sai rồi sửa). Người dẫn chỉ đồng cảm — 「この書類、初めて見ると、どこを読めばいいのか分からないですよね」 là thấu cảm, KHÔNG phải trải nghiệm cá nhân, hợp lệ. Ngưỡng vẫn ≥4/6.

Sửa lời bài đã viết → sửa **cả `_TTS.md` và bản `.md`** cùng lượt + **quét lại chuỗi `match` trong `*_SLIDES*.json`** (sửa câu là chết cue, render fail giữa đường).

## GIAI ĐOẠN 0 — CỬA VÀO: LỌC TRỤ + FACT SHEET FIRST (khác biệt lớn nhất với script-healthy)

**0a. Lọc trụ (từ chối ngay nếu fail):** đề tài phải nằm trong 3 trụ khóa — ① 年金 tính số · ② 給付金・取り逃し · ③ 税・社会保険料. **⛔ Từ chối:** 不動産 (bán nhà/リバースモーゲージ) · 金融商品 (投資/iDeCo/NISA/bảo hiểm — KỂ CẢ đóng khung "tin cải cách") · đào sâu 介護 (chỉ được 介護保険料). Đề tài lệch → báo user + trỏ mục KHÔNG LÀM trong `02_CONTENT_PLAN.md`.

**0a-2. ⭐⭐ T-GATE — CỔNG ĐỐI TƯỢNG, chạy NGAY SAU lọc trụ (chốt 2026-09-15).** Luật đầy đủ + bảng chấm lại hàng đợi: `02_CONTENT_PLAN.md` §T-GATE.
- Viết khối này vào header `03_SCRIPTS/<stem>.md` **trước khi viết chữ nào**:
  ```
  ### 対象者
  年齢: 65+ / 60-64 / 55-64 / 全年齢
  就業: 不問 / 在職必須 / 退職前後
  推定カバー率: <%>
  ```
- **T1 (máy, gate `G18`)** カバー率 ≥70% **và** 就業 ≠ 在職必須 — `python tools/check_pace.py <stem>` in G18 ở ĐẦU bảng, và bắt cả **khai khống** (ghi 60-64 mà khai 95% → chặn bởi trần nhân khẩu).
- **T2 (người, câu đắt nhất):** ***không làm gì thì có chuyện gì xảy ra với họ không?*** — phải có **tờ giấy tự đến** hoặc **trạng thái tự đổi**. 公金受取口座 tự đăng ký = CÓ (1,67M view). Đi khai để được hoàn thuế = KHÔNG, chỉ là bỏ lỡ — cả nhóm đó chết (9,4K · 7,6K · 2,4K view).
- Chốt: **T1+T5 cứng**, rồi **T2 + ít nhất một trong T3 (mốc ngày) / T4 (số 円 đã verify)**.
- 🔴 **Vì sao cần cổng riêng:** 17 gate của `check_pace.py` đều soi CHỮ, không cái nào hỏi *"bài này nói cho ai nghe"*. Video 19 qua sạch mọi gate rồi ăn **AVP 11,5% (bét kênh)** vì đề tài chỉ áp cho 60–64 còn đi làm, trong khi 74,9% khán giả là 65+.
- ⚠️ Cổng này dựng từ **một** ca hỏng, **chưa video nào đi qua nó**. 3–4 video pass mà AVP vẫn ~15% ⇒ kết luận đúng là *"đề tài cũng không phải đòn bẩy"*, không phải siết cổng chặt hơn.

**0b. FACT SHEET TRƯỚC KHI VIẾT CHỮ NÀO (bài học script 03 kẹt kho vì "viết xong mới định verify"):**
- Lập bảng fact: | Fact | Số | Nguồn | — verify bằng browser NGAY trong phiên, TRƯỚC giai đoạn dàn ý.
- Nguồn được phép: 日本年金機構 / 厚生労働省 / 総務省(家計調査) / 内閣府 / 協会けんぽ / ハローワーク + báo lớn cho số thị trường. Cấm bịa 「専門家によると」.
- Phân 3 loại số: **① nguồn chính thức** (dùng thẳng) · **② 計算 tự** (ghi およそ + show công thức trong FACT SHEET, vd mục "Kiểm chứng số hero 700万" script 05) · **③ ballpark phụ thuộc 自治体/保険者** (BẮT BUỘC hedge trong thoại: 「自治体によって変わります・必ず試算を」).
- Số đổi theo 年度 (支給停止調整額, 満額, trần 標準報酬…) → flag ⚠️ rà lại trước ngày đăng.
- **Số hero của cold open phải có mục kiểm chứng riêng** trong FACT SHEET và CÓ THẬT trong thân bài.
- Mẫu chuẩn: FACT SHEET của `03_SCRIPTS/05_60sai-teinen-taishoku-kiken.md`.

**0c. Đo trend (luật upload-seo 0.5):** YouTube Search 30d (gprop=youtube, geo=JP) + web 12m chống nhiễu → bảng điểm ghi vào header script (mẫu: script 05). Từ chết ở web (điểm 0) → cấm vào title/slug/tag.

**0d. ⭐ CHỐT 原典 SHOT — móc nhận diện số 1 của kênh (bắt buộc ≥2 shot/video, chốt 2026-07-25):**
> Vì sao: kênh thắng nhanh nhất ngách (元ハロワ職員まゆみ, 162K/8,5 tháng) thắng bằng **uy tín người trong hệ thống** — thứ mình KHÔNG được bịa (YMYL rule #5 + gian dối). Lớp thay thế honest, không đối thủ nào làm: **cho khán giả THẤY tài liệu gốc**. Biến 「当研究室は原典を一緒に読む」 từ lời nói thành bằng chứng thị giác. Kênh persona-giả không dám copy vì họ không mở nguồn thật. Chi tiết: `Projects/youtube-jp-nenkin/CHANNEL_BENCHMARK_2026-07-25.md` mục 3.
- Khi verify FACT SHEET (0b), **chụp/lưu ngay ảnh trang nguồn** cho ≥2 số quan trọng nhất → `06_VIDEO/<slug>/genten/` (đặt tên `genten_<số>_<cơ quan>.png`).
- Ghi vào FACT SHEET cột thứ 4 **「原典ショット」**: có/không + tên file + vùng cần khoanh đỏ.
- Trong script, chỗ đọc con số đó phải có 1 câu dẫn 原典: 「こちらが、日本年金機構のページです。赤で囲んだところ、ご覧ください。」 — KHÔNG đọc URL ra loa (dài, khó nghe); URL để 概要欄 出典.
- Ưu tiên shot: ① con số hero của cold open ② ngưỡng/điều kiện dễ bị hiểu sai ③ mẫu giấy tờ thật (定期便/振込通知書/申告書) khi làm series 書類を読む.
- Compliance: chỉ chiếu trang **cơ quan công** (年金機構/厚労省/総務省/自治体/協会けんぽ) — KHÔNG chiếu trang báo/blog/công ty (bản quyền + tên thương hiệu); che thông tin cá nhân nếu dùng giấy tờ mẫu; giấy tờ trên slide là **mẫu tự dựng lại hoặc bản mẫu công bố**, không dùng giấy thật của người thật.

## GIAI ĐOẠN 1 — Sổ xoay vòng khuôn (chống inauthentic — BẮT BUỘC ghi vào header script)

Đối chiếu 2–3 script liền trước, chọn khuôn KHÔNG trùng video liền kề, ghi rõ lý do sạch (như header script 05):
- **Khuôn mở bài (5):** ①GAIN-REVEAL ②事件型 (tin nóng/vụ lừa) ③質問型 ④対決型 (A vs B) ⑤物語型 (kể モニター trước, số sau).
- **Khuôn 計算タイム (5):** thang 3 bậc quanh ngưỡng / A-vs-B đối chiếu / timeline 10–20 năm / ○×クイズ / tính ngược (muốn X cần Y).
- **Closer xoay:** ○×クイズ / セルフチェック 3問 / 行動プラン 3 bước / シェア ノート…
- **Tuyến xen kẽ:** 改正・給付金 → evergreen いくらもらえる → cảnh báo lừa đảo → 視聴者の実験室 → story 年金生活 — 2 video liền nhau không cùng tuyến/trụ.

## GIAI ĐOẠN 2 — Cast モニター + dàn ý

**Cast cố định (GHI ĐÈ luật script-healthy "nhân vật mới mỗi script"):** đọc bảng Hồ sơ モニター trong `Projects/youtube-jp-nenkin/CLAUDE.md` (nguồn sự thật DUY NHẤT — 田中/佐藤/鈴木/高橋/山田夫妻/伊藤/松本). Chọn **2–3 người hợp chủ đề**, xoay người đóng chính. Số đời nhân vật KHÔNG tự đổi; tiến triển phải có lý do cốt truyện + cập nhật lại bảng trong CLAUDE.md. Chủ đề nhạy cảm đời tư (ly hôn, phá sản…) → nhân vật MỚI dùng 1 lần, đừng gán cho cast chính. Mở open-loop cast cuối video (quyết định của X…) khi chủ đề còn tập sau.

**Dàn ý CASE-DRIVEN (xương sống kênh):** mỗi khái niệm phải gắn 1 nhân vật + 1 con số chạy + phán quyết màu (XANH an toàn/ĐỎ bị cắt/VÀNG sát ranh). **60–70% thân bài = case/số động; "giải thích chế độ chay" ≤45s liên tục** rồi phải chen case/câu hỏi. Case + số của nhân vật phải vào **trước phút 2** (retention pass v2 script 05: case sống ở 03:40 = vùng chết).

**Khung 7 khối tham chiếu** (dàn KHÔNG cố định — video = 1 研究 仮説→計算→結論):
```
【0:00–1:10】Cold open (GĐ3) → giới thiệu kênh 1 câu SAU hook → vào 第1章 trước 70s
【~2:00】  Case #1 + số chạy của モニター (bắt buộc trước phút 2)
【giữa bài】計算タイム theo khuôn đã chọn · re-hook ~50% + CTA giữa video (§2.4b cta-midvideo)
【80–85%】 Trả open-loop LỚN của cold open
【kết】    研究ノート 1 trang (「それでは、今日の研究ノートです。」) → closer xoay
          → hẹn tập ĐÍCH DANH (cấm 「来週もお届けします」 mơ hồ) → câu kết cố định:
          「それでは、また次回の研究でお会いしましょう。」
```

## GIAI ĐOẠN 3 — Cold open: LOSS-AVERSION bắt buộc mọi khuôn

- **Câu 1 = mất mát/hậu quả cụ thể CỦA あなた + số** (mất tiền, phải ngửa tay xin con, chờ mà lỗ…). KHÔNG chào hỏi giây 0. KHÔNG mở hiền/trấn an sớm (bài học script 03 v1: "chỉ 2 vạn thôi mà" = chết hook).
- **Giữ căng nỗi sợ ~25–30s rồi mới hé lối thoát.** Trước giây 30 bắn CON SỐ ĐẮT NHẤT video (mượn từ case giữa bài → open-loop payoff ~50–85%).
- ≤15s phải chỉ mặt あなた đúng hành vi; **thước đo 15s = ~70 ký đầu phải echo lời hứa title/thumbnail** (đếm ký tự tới câu echo).
- Trần YMYL của sợ: sợ phải CÓ THẬT trong bài + được giải tỏa trong thân bài (không dọa suốt); cấm 絶対/必ず; cấm 殺/血/死/破産 ở title/thumbnail.
- Mẫu chuẩn: cold open v2 của scripts 01/02/04, 物語型 fear-forward của 05.

## GIAI ĐOẠN 4 — Viết + luật YMYL tài chính (6 điều, nghiêm như YMYL y tế)

1. KHÔNG tư vấn đầu tư/sản phẩm cụ thể — chỉ chế độ công khai + số TB có nguồn.
2. Mọi số từ FACT SHEET đã verify (GĐ0) — không thêm số mới giữa chừng mà không rà.
3. Mỗi video: 「◯年◯月時点の情報です」 trong script + 概要欄; cuối video 1–2 câu khuyên xác nhận 年金事務所/ねんきんネット (gọn — KHÔNG block dài giữa bài; gom disclaimer như luật script-healthy).
4. Cấm 「必ず」「絶対得」 → 「〜の場合が多い」「制度上は〜」「一般的には〜」.
5. Không tên chính trị gia/đảng ở title/thumbnail/script.
6. Story hóa 年金生活 → nhân vật hư cấu 100% + disclaimer フィクション.

Văn phong: theo mục YÊU CẦU VĂN PHONG của `script-healthy` (câu dài ngắn xen kẽ, từ đệm tiết chế, nói với 皆さん/あなた, chi tiết đời thường) — chỉ đổi chất giọng: nghiên cứu viên điềm đạm, không phải hàng xóm ấm áp.

## GIAI ĐOẠN 5 — RETENTION AUDIT + xuất bản (kế thừa script-healthy GĐ5, thêm mục nenkin)

- Audit từng transition (bridge tò mò / pattern interrupt, không 2 transition phẳng liên tiếp) + re-hook ~50% + CTA giữa video **§2.4b** (`cta-midvideo.md`) ngay sau khối case-tính-thử ~50%.
- **Audit riêng nenkin:** ① khối giải thích chay nào >45s? → chen case ② case đầu vào trước phút 2 chưa? ③ số nào chưa có trong FACT SHEET? ④ khối tính đặc >60s → chèn beat quy đổi đời thường ("700万 = 2 năm sinh hoạt phí" — retention pass v2 script 05) ⑤ persona/xin đăng ký đứng SAU payoff đầu chưa? ⑥ **có ≥2 原典ショット với câu dẫn 「赤で囲んだところ」 chưa?** (GĐ0d — thiếu là mất móc nhận diện của kênh) ⑦ shot 原典 đầu tiên nên rơi **trong 3 phút đầu** — đó là lúc khán giả quyết định kênh này có đáng tin hay không.
- ⭐ **LỚP `drawn` — trang sổ viết tay (bộ nhận diện KHÓA, user chốt 2026-07-27):** xuất entry SLIDES `"drawn"` ở **3 chỗ**: ① khối case tính thử tiền ~50% → `{"layout":"table","anim":true}` (chữ hiện dần, `circle` = dòng đáp án) ② slide **「研究ノート」** tổng kết cuối video (tĩnh, để screenshot) ③ khối 「よくある誤解」 → `{"layout":"checklist","mark":"cross"}` (✗ đỏ, KHÔNG dùng ✓ cho câu sai). **Font/giấy CỐ ĐỊNH `jp-pen` + `grid`, không đổi giữa các video.** Bộ màu qua phần tử thứ 3 của row: `ok` xanh / `warn` vàng / `bad` đỏ. Chi tiết + lệnh: `CLAUDE.md` §Chuẩn VISUAL. ⚠️ Nó thay CARD CHỮ auto, **không** thay 原典スライド và **không** tính vào gate dưới đây.
- ⛔ **LỚP THỦ CÔNG ĐÃ BỎ HẲN (2026-08-09, user: "bỏ tất cả HANDMADE ở các project đi").** Không còn gate, không còn BỎ SLOT, không ghi sổ `HANDMADE: hoãn`, KHÔNG xuất bảng `撮影リスト`/`収録リスト`/danh sách cần quay. Nguồn thật vẫn bắt buộc nhưng qua §YMYL của project + `youtube-compliance.md` §1, không qua rule này. Chi tiết: `.claude/rules/handmade-layer.md`.
- Xuất bản sạch `=== KỊCH BẢN HOÀN CHỈNH ===` + file `_TTS.md` (1 dòng = 1 nhịp, dòng trống = nghỉ sâu, chỉ tag nhấn nhá `[速x][抑揚x][間x]`, KHÔNG đổi style giữa bài) — theo đúng GĐ5b/5c script-healthy.
- Kỳ vọng thật: AVD tổng 30–55%; tối ưu đường cong 0–90s, không hứa AVD 70%+.

## GIAI ĐOẠN 6 — Đóng gói CTR + compliance

- 🔴 **GATE 3×3 (bắt buộc, `.claude/rules/ab-3title-3thumb.md`): 3 TITLE A/B + 3 THUMBNAIL A/B.** Title ghi dưới heading `### 3 TITLE A/B` dạng bảng, title trong ô `` ` ` `` — **A1** = Title CHỐT (thẳng keyword) · **A2** đổi keyword dẫn · **A3** đổi kiểu hook (loss-aversion ↔ persona 60代からの…). Thumbnail đặt tên `thumb_T1_*.png` (baseline khuôn A-45) · `thumb_T2_*.png` (đổi 1 biến hình, giữ nguyên chữ) · `thumb_T3_*.png` (đổi layout: ít dòng + mặt). `upload_pack.py` đếm và báo `🔴 GATE 3×3` nếu thiếu.
- **Title:** keyword chính (từ bảng trend GĐ0c) trong 5–7 từ đầu, ~60 ký/~30 full-width. Khung thắng ngách: 【知らないと大損】/【申請忘れ続出】/【○○必見】+ số tiền lỗ định lượng + 末路/危険/申請しないと消える + móc thời điểm (2026年新ルール/4月から).
- **Thumbnail:** theo `03_THUMBNAIL_TITLE_FORMULA.md` + sổ xoay 8 khuôn (mục 5 file đó) — **số tiền là nhân vật chính ~1/3 khung**, dòng đỏ to nhất = hậu quả sợ + 「!?」, banner = móc thời điểm/tia giải pháp, badge 「年金研究室」 cố định. Không lặp khuôn video liền trước.
- **Metadata 4 tín hiệu (luật 2.4, đã live trên kênh — nguồn: `CHANNEL_BACKFILL_2026-07-25.md`):** categoryId **27** · rổ 12 tag nhận diện đứng đầu (`年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金`) + tag đề tài → tổng 25–35 · 3 hashtag cố định cuối desc `#年金 #老後のお金 #年金と老後のお金研究室` + ≤3 topical · desc 800–1.800 ký: 3 dòng hook (về gì/cho ai/được gì, cấm lời chào) → 目次 → đoạn topical → disclaimer + 出典 + credit voice → hashtag.
- 🔴 **GATE PINNED (bắt buộc, user chốt 2026-09-08 — "lúc nào cũng phải có"):** heading **đúng chữ `### Pinned comment`** + code fence, đặt ngay sau block `### タグ`. `upload_pack.py` in `🔴 GATE PINNED` nếu thiếu, và ô `[9]` của `METADATA.txt` luôn hiện (thiếu thì hiện khối cảnh báo đỏ).
  **Năm phần, đúng thứ tự:** ① 「ご視聴ありがとうございます。当研究室の、今日のノートです。」 ② **研究ノート ①–⑤** nhắc lại 5 điểm chốt ③ 「お手元で確かめる3つ →」 ④ một **câu hỏi mở** mời comment + 「皆さまの声が、次の研究テーマになります。」 ⑤ disclaimer 「◯年◯月時点の情報です」 + khuyên 税務署/年金事務所.
  ⚖️ Số trong bình luận ghim **lấy từ chính lời đọc**, không thêm số mới (YMYL y như 概要欄); ⛔ không bịa link playlist.
- **Quét compliance** (`.claude/rules/youtube-compliance.md`): từ tắt-ad ở title/thumbnail/概要 hiển thị (殺/血/死/破産…) · không misleading · không tên thật cty/người · Altered content KHÔNG tick (slide+ảnh, giọng đã credit) · ảnh いらすとや ≤20/video + credit 「イラスト:いらすとや」.
- Xuất đủ **4 trường** cho upload_pack, ghi thẳng vào file script: Tên file upload (slug keyword) · 3 dòng đầu 概要欄 · mô tả đầy đủ + `タグ` block · **`### Pinned comment`**.
  🔴 Dòng này trước ghi "3 trường" và **bỏ sót pinned** — đó là lý do bình luận ghim khuyết dù mục ở trên có nhắc tới nó. **Danh sách kiểm cuối mà thiếu một mục thì mục đó sẽ rơi**, dù nó được mô tả kỹ ở đoạn trên.

## ĐẦU VÀO / ĐẦU RA
- Vào: chủ đề từ `02_CONTENT_PLAN.md` (hoặc user đưa; lệch trụ → từ chối ở GĐ0a). Ra: `03_SCRIPTS/<số>_<slug>.md` (header = sổ khuôn + FACT SHEET + bảng trend + gói CTR) + `_TTS.md` + `_SLIDES.json` theo chuẩn visual CLAUDE.md kênh (cast 35–40% / diagram 35% / ảnh thật 15% / card chữ 10%; slide mở màn = ảnh cinematic + chữ hook vàng).
- In ra đủ 7 giai đoạn (0→6) để user thấy quy trình chạy thật.
