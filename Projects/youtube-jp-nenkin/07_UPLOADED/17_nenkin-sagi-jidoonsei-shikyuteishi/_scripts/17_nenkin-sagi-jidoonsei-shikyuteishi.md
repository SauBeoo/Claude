# 17 — 日本年金機構をかたる詐欺｜自動音声で「支給停止」と言われたら

> Kênh: 年金と老後のお金研究室 · **Trụ ② 給付金・取り逃し**（trust-builder / bảo vệ, KHÔNG tính tiền — đổi nhịp, đúng phân loại `02_CONTENT_PLAN.md` 🟩TRỤ②）
> Viết 2026-08-26 · **Trả lời hẹn tập ĐÍCH DANH đã nói trên sóng cuối video 16**: 「日本年金機構をかたる詐欺が、この一年で、急に増えています。本物の通知と、偽物の電話。その見分け方を、次回の研究で、一緒に確かめます。」
> Khuôn: **②事件型（電話が鳴る）+ đối chiếu 本物/偽物**
> Độ dài đích: **13–17 phút** (`CLAUDE.md` §ĐỘ DÀI, hệ số 5,72 ký/giây + 0,45s/dòng + 1,0s/đoạn) — **v2** (sau lượt sửa) đo tay trên `_TTS.md`: 59 đoạn ≈ **14,5 phút**, CTA rơi đúng **46,1%** timeline, mốc "xác nhận là giả" rơi ở **23%** (so v1: CTA lệch 37,8%, payoff lộ ở 15%). ⚠️ Phép đo tay xấp xỉ công thức, KHÔNG thay thế `python tools/make_tts.py 17_nenkin-sagi-jidoonsei-shikyuteishi --dry` — vẫn phải chạy tool thật trước khi render.
> Lớp hình: SÂN KHẤU `make_stage --channel nenkin` (theo tiền lệ video 15/16) — SLIDES/ảnh AI/render **CHƯA làm ở lượt này**, xem mục "CHUẨN BỊ RENDER" cuối file.

## GĐ0a — LỌC TRỤ

Đề tài: cảnh báo lừa đảo mạo danh 日本年金機構. Nằm nguyên trong trụ ② (取り逃し・給付金 mở rộng thành "bảo vệ tiền đã có", đã được `02_CONTENT_PLAN.md` liệt kê sẵn ở bảng 🟩TRỤ② mục 🥈 「日本年金機構をかたる詐欺｜手口と見分け方」). Không đụng 不動産/金融商品/介護 sâu. **PASS.**

## GĐ0c — KHẢO SÁT ĐỐI THỦ + ĐO TREND (làm TRƯỚC khi chọn đề tài, theo đúng yêu cầu)

**1) Quét swipe file (`tools/swipe_titles.py --group nenkin`, chạy lại 2026-08-26 — số liệu tươi, không phải bản 08-21):**
- Top-growth toàn ngách 5 tuần qua đều là khuôn **cảnh báo phong bì/thời hạn** (`8月から年金口座が"公金受取口座"に自動登録｜断るなら45日以内` — 64,4× sub kênh; `【期限切れ注意】8月から届くこの封筒、放置すると…自動登録されます` — 1,3M view/38 ngày). ⇒ khuôn **事件型/cảnh báo** là khuôn thắng ổn định nhất của cả ngách, không phải khuôn riêng của kênh mình.
- Có 1 video mới xuất hiện (9 ngày tuổi, 4,6×): `遺族年金は「夫の年金の4分の3」ではありません｜入らない部分があります` — góc "đính chính hiểu lầm" hay nhưng **trùng đề tài đã làm ở video 13** (遺族年金) → không chọn, tránh cannibalize.
- Có 2 video "2027年に年金制度が大激変" (7.821 view/ngày, 36 ngày & 4 ngày tuổi) — hot thật, nhưng đó là **trụ ①** (cải cách tương lai, rủi ro YMYL cao vì luật chưa ban hành đầy đủ) và sẽ phá lời hẹn đã nói trên sóng ở video 16. Ghi vào hàng đợi cho video sau, không dùng lượt này.
- **Không có kênh nào trong rổ 7 kênh benchmark hiện đang làm video chuyên đề "詐欺" cho 年金** trong 60 ngày qua (rà cột title toàn bộ 27 video quét được) → đây là **khoảng trống thật**, không phải cửa đã đông người.

**2) Đo Trend YouTube Search 30d (`gprop=youtube`, `geo=JP`):** Google Trends trả **HTTP 429** (rate-limit) — đúng lỗi đã ghi nhận trước đó ở script 03 (rổ 繰り下げ/給付金 từng bị chặn 6 lần liên tiếp). **Không đo được số điểm lần này.** Thay bằng nguồn thay thế được luật 0b cho phép ("báo lớn cho số thị trường"):
- 警察庁 SOS47 (`npa.go.jp`) công bố: 令和7年(2025) 特殊詐欺 被害総額 toàn quốc **約3.257億4.258万7.000円**; riêng **還付金詐欺 2.087件** (nguồn chính thức, đã verify — xem FACT SHEET).
- Báo lớn dẫn 警察庁: **2026年上半期(1–6月) đã là 1.816億2.000万円, tăng 51,7% so cùng kỳ, mức tệ nhất từ trước tới nay, ~10億円/ngày** — xác nhận đây là vấn đề đang NÓNG LÊN trong chính năm nay, không phải tin cũ.
- ⚠️ Ghi lại để không quên: **đo lại Trends khi hết rate-limit** trước khi chốt title cuối cùng lúc đóng gói CTR (nếu điểm khác dự đoán thì đổi keyword dẫn).

**Kết luận GĐ0: chọn đề tài "日本年金機構をかたる詐欺の手口と見分け方"** — vừa là lời hứa đã nói trên sóng, vừa đúng trụ đang nợ (② sau 3 video liền trụ③: 14·15·16), vừa là khoảng trống thật trong ngách (không ai đang làm), vừa có số liệu 2026 tươi để neo YMYL.

## GĐ0b — FACT SHEET (verify TRƯỚC khi viết chữ nào, 2026-08-26)

| # | Fact | Nội dung xác minh (nguyên văn/trích) | Nguồn | 原典ショット |
|---|---|---|---|---|
| 1 | ⭐⭐ **5 điều 年金機構 THẬT không bao giờ làm** | 「電話や訪問により、預貯金額や口座番号等をお聞きすることはありません」「自動音声ガイダンスにより年金の支給停止等をすることはありません」「ATMの操作や現金の振り込みを指示することはありません」「LINEで手続きについてご案内することはありません」「（相談・手続きに）手数料は一切かかりません」 | 日本年金機構『日本年金機構の職員や委託事業者などと称して、現金を詐取する「不審な電話や訪問」にご注意ください』(`nenkin.go.jp/oshirase/gochui/20140129.html`, trang ghi cập nhật gần đây) | ✅ shot #1 — khoanh đỏ cả 5 gạch đầu dòng |
| 2 | ⭐⭐ **Thủ đoạn tự động thoại giả 2026** | Kẻ gian dùng "tự động âm thanh hướng dẫn" tự xưng 年金機構/年金事務所, nói không xác nhận được thủ tục → giục bấm phím hoặc gọi lại; có biến thể hỏi số tài khoản/thẻ, xin ảnh chụp Mynumber; câu cảnh báo chính thức: cơ quan thật "không dùng tự động âm thanh liên hệ", "không yêu cầu ảnh thẻ", "không hỏi thông tin cá nhân", "không hướng dẫn ATM/chuyển tiền". Liên hệ khi nghi ngờ: **#9110** (tư vấn cảnh sát) / **188** (hotline người tiêu dùng) | 警察庁・SOS47特殊詐欺対策ページ (`npa.go.jp/bureau/safetylife/sos47/new-topics/250428/03.html`) | ✅ shot #2 — khoanh đỏ đoạn mô tả tự động thoại + 2 số điện thoại liên hệ |
| 3 | ⭐ **Số liệu thiệt hại 2025 toàn quốc (chính thức)** | 「合計被害額：約3,257億4,258万7,000円」; riêng **還付金詐欺 認知件数 2,087件** (toàn quốc, 令和7年) | 警察庁・SOS47統計ページ (`npa.go.jp/bureau/safetylife/sos47/circumstances/statistics/`) | ✅ shot #3 — khoanh đỏ dòng tổng thiệt hại + dòng 還付金詐欺 |
| 4 | **Số liệu 2026 nửa đầu năm (tăng vọt, qua báo lớn dẫn 警察庁)** | 2026年上半期(1〜6月) 特殊詐欺被害額 **1,816億2,000万円**、前年同期比 **+51.7%**、上半期として過去最悪、1日あたり約10億円の被害 | Báo lớn dẫn 警察庁 (ví dụ 山陰中央新報デジタル 2026-08 đưa tin) — dùng làm số thị trường bổ sung theo luật 0b, **KHÔNG chụp 原典** (không phải trang cơ quan công) | — (chỉ đọc lời thoại, ghi nguồn ở 概要欄) |
| 5 | **Biến thể email/SMS giả mạo (không tính vào 原典)** | Có email/SMS giả mạo 年金機構 nói "chưa đóng bảo hiểm quốc dân" rồi dụ chuyển tiền qua PayPay | 日本ファクトチェックセンター (qua Yahoo!ニュース) — nguồn kiểm chứng tin giả, KHÔNG phải cơ quan công → chỉ kể MIỆNG, không chiếu màn hình, hedge "đã có trường hợp được xác nhận là tin giả" | — |
| 6 | **鈴木さん hồ sơ (kế thừa canon `CLAUDE.md`)** | 65歳・名古屋・役員、退職金 lớn — KHÔNG có case tiền cụ thể trước đó (xác nhận ở header video 09: "鈴木 chưa từng có case tiền cụ thể") → hợp lý để dùng cho video KHÔNG cần con số tiền, chỉ cần tình huống | `CLAUDE.md` §モニター | — |
| 7 | **田中さん hồ sơ giấy tờ thật (callback)** | Đã có 「年金支給日」「公金受取口座 意向確認書」「12月の年金振込通知書」 xuất hiện ở video 08/09/16 — dùng làm đối chiếu "giấy thật trông như thế nào" | Script 08/09/16 (canon đã công bố) | — |

### Phân loại số (luật YMYL #2)
- **① Nguồn chính thức dùng thẳng:** #1, #2, #3 (nguyên văn 警察庁/年金機構).
- **② Không có số tự tính trong video này** (video không tính tiền cho ai).
- **③ Ballpark/hedge bắt buộc:** #4 (số 2026 nửa năm là thống kê chung TOÀN QUỐC mọi loại đặc thù lừa đảo, không riêng lừa mạo danh 年金機構 — phải nói rõ "toàn bộ đặc thù lừa đảo" chứ không gán hết cho riêng vụ mạo danh năm金機構) và #5 (chỉ 1 ca đã xác nhận, không suy ra tần suất).

### ⚠️ Đường lui nếu render sau khi có tin mới
Đề tài lừa đảo đổi thủ đoạn liên tục — nếu render cách ngày viết quá 4–6 tuần, rà lại 2 trang npa.go.jp xem còn đúng thủ đoạn được mô tả không trước khi giữ nguyên FACT #2.

## GĐ1 — SỔ XOAY KHUÔN (chống inauthentic)

| | Video 14 148万の境目 | Video 15 10月15日振込 | Video 16 12月精算 | **Video 17 (bài này)** |
|---|---|---|---|---|
| Khuôn mở | ⑤物語型 (2 phong bì 中村) | ②事件型 + trực-diện-あなた | ②事件型「間違いか詐欺か」 | **②事件型「電話が鳴る」** — lần đầu tiên hook là một cuộc gọi thật đang diễn ra (real-time), khác 3 video trước đều mở bằng số tiền/giấy tờ |
| Khối giữa | bảng so 147万/150万 | timeline 6 kỳ trong năm | A-vs-B đối chiếu 2 người | **checklist 対決 5 điều "本物は/偽物は"** — lần đầu dùng checklist làm khối giữa thay vì bảng số/timeline |
| Closer | 行動プラン 3 bước (điện thoại) | 1 tờ giấy 1 vòng tròn | ○×クイズ tự chấm 3 câu | **セルフチェック 3 câu ○×** (tái dùng cùng dạng ○×クイズ như 16 nhưng nội dung hoàn toàn khác — cảnh báo, không phải tính thuế) |
| Tuyến | 税・社会保険料 | 税・社会保険料 | 税・社会保険料 | **給付金・取り逃し (② — TRẢ NỢ TRỤ, dừng chuỗi 3 video liên tiếp trụ③)** |
| Cast chính | 中村 | 中村 | 高橋 + 田中 | **鈴木 (chính, nhận cuộc gọi) + 田中 (đối chiếu, callback giấy tờ thật từ video 08/09/16)** — 鈴木 lần đầu làm nhân vật chính |

## GĐ2 — DÀN Ý CASE-DRIVEN

- **Cast:** 鈴木さん (65, 名古屋, 役員 vừa nghỉ hưu, có 退職金 lớn) nhận điện thoại tự động giả mạo — vừa hoảng vừa nghi ngờ, suýt bấm nút, dừng lại kịp lúc, gọi số chính thức xác minh. 田中さん (67, 横浜) xuất hiện giữa bài làm đối chiếu: anh đã quen mặt giấy tờ thật (từ video 08/09/16) nên biết ngay cái gì KHÔNG giống giấy thật.
- **60–70% thân bài là tình huống sống + đối chiếu cụ thể**, phần giải thích chế độ (thống kê 警察庁, quy định 年金機構) mỗi khối ≤45 giây rồi quay lại tình huống/quiz.
- **Case #1 (鈴木, cuộc gọi) xuất hiện ngay ở cold open**, tức trước phút 2 — đạt yêu cầu retention.
- **Chất người (mũi tiêm, ngoại lệ nenkin — qua CAST, không qua người dẫn):**
  - ①④ (qua cast): 鈴木 tự trải nghiệm, suýt làm sai (định bấm nút) rồi tự sửa (dừng lại, gọi số thật xác minh) — cast tự nếm cả 2 mặt.
  - ② case có thoại + chi tiết đời sống vô dụng-về-thông-tin: 鈴木 đang xem tin trưa trên TV lúc chuông reo; thoại trực tiếp của giọng máy; sau đó kể lại cho vợ nghe trong lúc rót trà.
  - ③ ký ức giác quan tệp khán giả: tiếng chuông điện thoại bàn cũ, tiếng "ガチャ" khi dập máy, ánh nắng buổi trưa qua rèm.
  - ⑤ đóng nhân vật bằng cảm xúc: 鈴木 thở phào, không phải bằng một kết luận số liệu.
  - ⑥ phá nhịp câu ≥3 lần: câu cụt "支給停止。"; câu cảm thán trong thoại vợ; câu tự cắt lời khi 鈴木 định bấm nút.
  - → **6/6 mũi tiêm đạt** (vượt ngưỡng ≥4/6).

## GĐ3 — COLD OPEN: đã viết trong thân bài dưới, khuôn ②事件型「電話が鳴る」, giữ căng ~25–30s trước khi hé "hôm nay sẽ phân biệt được".

## 🔴 SỬA — user chấm bản v1, tự phê bình thật trước khi sửa (2026-08-26)

User hỏi thẳng: *"người xem đến với video này vì cái gì, ở lại vì cái gì"* — bản v1 không trả lời được
câu đó tử tế. Ba lỗi thật, không phải lỗi cảm giác:

1. **Cold open mở bằng tiểu sử ngôi thứ ba** (「鈴木さん、65歳。名古屋にお住まいです」) thay vì đâm thẳng
   あなた. Đây **đúng khuôn đã bị đo là YẾU HƠN** — header video 15/16 ghi rõ: *"relPerf@30s gấp đôi
   so bản ngôi-thứ-ba trung tính"* khi đổi sang khuôn trực-diện-あなた. v1 vô tình quay lại khuôn yếu.
2. **Payoff "đây là lừa đảo" lộ ở ~15% bài** (鈴木 gọi xác minh ngay sau khi cúp máy, phút 1:50/13:14)
   — sớm hơn cả lỗi ~35% mà video 16 v1 đã bị chê. Sau đó là chuỗi khối rời: 5 điều → cơ chế → đối
   chiếu giấy → số liệu → hành động — **đúng nghĩa listicle nối đuôi**, cùng bệnh với video 16 v1.
3. **Không có cao trào.** Xung đột duy nhất ("tay dừng ở nút 1") giải quyết trong <2 phút bằng 1 cuộc
   gọi xác minh. Trong khi chính FACT #2 (nguồn 警察庁) đã mô tả **cơ chế 2 GIAI ĐOẠN**: giọng máy →
   chuyển máy cho "nhân viên" người thật để moi số tài khoản/ảnh Mynumber — đoạn NGUY HIỂM NHẤT, và
   v1 không dựng nó thành cảnh nào cả, bỏ phí đúng chất liệu kịch tính nhất đã tra được.

**Sửa (giữ nguyên FACT SHEET — chỉ viết lại KHUÔN KỂ + kéo dài xung đột):**
- Cold open đổi sang **đâm thẳng あなた**, mở bằng cảm giác/hành động (điện thoại rung), không mở
  bằng tiểu sử. Nén phần lý lịch 鈴木 xuống 1 mệnh đề ngắn, cài GIỮA lúc căng nhất, không mở đầu.
- **鈴木 KHÔNG cúp máy ngay** — anh bấm 1, bị chuyển sang "nhân viên" người thật (giai đoạn 2, đúng
  FACT #2), bị hỏi ngày sinh → địa chỉ → số tài khoản → **ảnh thẻ Mynumber**. Đây là cao trào thật:
  anh gần như định gửi ảnh, một chi tiết nhỏ (chính từ "マイナンバーカード") khiến anh khựng lại.
- **Payoff dời xuống ~28% bài** (sau khi đã đi qua cả 2 giai đoạn), và khối "5 điều không bao giờ
  làm" đóng vai **ĐÁP ÁN của đúng cái vừa xảy ra** (đối chiếu từng điều với từng bước cuộc gọi), thay
  vì một list khô đọc riêng.
- Thêm 1 subplot nhỏ (鈴木 định đi câu cá chiều đó, kể lại cho bạn câu cá nghe) để có beat chất người
  ở giữa bài, không dồn hết cảm xúc vào đầu/cuối, và tạo thêm 1 tiếng nói phụ ("俺だったら、たぶん、
  送ってたな") củng cố cảm giác "ai cũng có thể dính", không chỉ 鈴木.
- **Không đổi bất kỳ FACT/nguồn nào** — mọi câu trích 原典 (5 điều, mô tả giai đoạn 2, số liệu) giữ
  nguyên văn như FACT SHEET đã verify.

**Đo lại sau sửa:** xem lại mục "GĐ5 — RETENTION AUDIT" bên dưới (đã cập nhật số đo + vị trí CTA/payoff mới).

---

=== KỊCH BẢN HOÀN CHỈNH === (v2 — sau lượt sửa 2026-08-26, xem mục "🔴 SỬA" ở trên)

## 第1章 — Cold open「1を、押しました」(0:00–1:27)

その電話は、机の上のスマートフォンを、震わせました。

出ますか。それとも、出ませんか。

——出た、とします。
機械の声が、言います。
「こちらは、日本年金機構です。書類の提出が確認できないため、来月から、年金の支給が停止されます。至急、1を押してください」

支給停止。

その四文字が、頭の中で膨らんでいく間に、指は、もう1のボタンに向かっています。

これは、あなたの話かもしれません。実際にこの電話を受けたのは、鈴木さん、65歳。今年、会社を退職したばかりの、平日の昼下がりでした。

そして鈴木さんは——1を、押しました。

もし、物語がここで終わっていたら、この動画も、ここで終わっていました。けれど、これは、まだ、入り口に過ぎません。

年金と老後のお金研究室は、こうした話を、原典の資料とあわせて確かめる場所です。今日、確かめることは、3つ。この電話の先に、何が起きたのか。本物の年金機構が、絶対にしないこと。そして、もしあなたの電話が鳴ったら、すべきこと。

## 第2章 — 「オペレーター」という、もうひとつの声（1:27–2:43）

1を押すと、少しの保留音のあと、今度は、人の声が出ました。
機械ではありません。感じのいい、落ち着いた声でした。

「お電話ありがとうございます。本人確認のため、いくつかお伺いします」

生年月日を聞かれ、答えました。次に、住所の一部を聞かれ、これも、答えました。ここまでは、なんの違和感もなかったそうです。

「では、支給停止を解除するために、ご登録の口座番号を、確認させてください」

鈴木さんは、通帳を取りに、立ち上がりかけました。テーブルの上には、書きかけの、釣り仲間へのメモが置いてありました。今日の午後、二人で釣りに行く約束をしていたのです。ペンを持ったまま、いったん、それを脇にどけました。

口座番号を、答えました。

「ありがとうございます。念のため、マイナンバーカードの写真も、送っていただけますか」

——ここで、手が、止まりました。

## 第3章 — 止まった、ひと言（2:43–3:47）

なぜ、ここで止まったのか。鈴木さん自身、うまく説明できなかったそうです。ただ、「マイナンバーカードの写真」という言葉が、何か、引っかかった。

「少し、確認してから、かけ直します」

そう言って、電話を切りました。ガチャ、という音が、静かな部屋に響きました。

年金手帳を取り出しました。裏表紙に、本物の相談窓口の番号が、印刷されています。そこに、かけ直しました。

「そのような電話で、口座番号やマイナンバーカードの写真をお伺いすることは、ございません」

窓口の担当者は、そう答えたそうです。鈴木さんは、しばらく、受話器を握ったまま、動けなかったと言います。あと少し、手を止めるのが遅ければ——その先まで、進んでいたかもしれません。

## 第4章 — 答え合わせ：5つの「絶対にしないこと」（3:47–5:29）

日本年金機構自身が、公式サイトで、はっきりと宣言していることがあります。原典を、一緒に見てみましょう。

こちらが、日本年金機構の注意喚起のページです。赤で囲んだところ、ご覧ください。

こう書かれています。
ひとつ。電話や訪問により、預貯金額や口座番号などをお聞きすることはありません。
ふたつ。自動音声ガイダンスにより、年金の支給停止などをすることはありません。
みっつ。ATMの操作や、現金の振り込みを指示することはありません。
よっつ。LINEで、手続きについてご案内することはありません。
いつつ。相談や手続きに、手数料は一切かかりません。

鈴木さんが受けた電話は、この5つのうち、少なくとも3つに当てはまっていました。自動音声で始まったこと。支給停止を告げたこと。そして、口座番号を尋ねてきたこと。

警察庁も、こんな傾向を注意喚起しています。原典を、もうひとつ、お見せします。赤で囲んだところに、こうあります。「マイナンバーカードの写真を求めてくるケースも、報告されています」。まさに、鈴木さんが、あと少しで応じるところだった、あの言葉です。

年金機構自身が「しない」と公言していることを、3つも重ねてくる。それだけで、もう、答えは出ています。

## 第5章 — なぜ「もっともらしく」聞こえたのか（5:29–6:42）

機械の声から、人の声へ。そこに、この手口の、いちばん巧妙なところがあります。

機械の声だけなら、多くの人が、途中で不審に気づきます。けれど、人の声に切り替わった瞬間、警戒は、ゆるみます。感じのいい話しかた、生年月日を当てられる的中感——それだけで、「ちゃんとした窓口につながった」と、錯覚してしまうのです。

もうひとつ、気をつけたいことがあります。ちょうど、本物の年金機構から通知書が届く時期——支給日の前後や、書類の提出が求められる時期——を狙って、電話がかかってくることもあると言われています。「ちょうど、その話をしていたところだった」。そういう状況のときほど、電話は、本物らしく聞こえてしまうものです。

不審に思ったときの連絡先も、原典に書かれています。警察相談専用電話、シャープの9110。消費者ホットライン、188。この2つの番号は、覚えておく価値があります。

## 第6章 — CTA（応援のお願い）（6:42–7:10）

ここで、ひとつだけお願いです。今日の内容がお役に立ちそうだと感じていただけたら、高評価と、同じように心配なご家族やご友人へのシェアで、この研究室を応援していただけると嬉しいです。ご感想や、皆さまが実際に受けた不審な電話・メールがあれば、コメントでお寄せください。皆さまの声が、次の研究テーマになります。

## 第7章 — 本物の通知書は、こんな姿をしています（7:10–8:12）

では、本物の年金機構は、どんな姿で、あなたのところに来るのでしょうか。

この研究室では、これまで、いくつもの本物の通知書を、実際に画面でお見せしてきました。年金支給日の振込通知書。公金受取口座の、大きなはがき。12月の、税額の精算のお知らせ。

田中さんは、この研究室の常連です。何度も本物の書類を見てきたぶん、こう話していました。
「本物は、いつも、紙で来るんだよね。名前も、基礎年金番号も、ちゃんと印刷されてる。急かされたことは、一度もないよ」

本物の通知は、急ぎません。期限は、書いてあっても、たいてい数週間から、ときには45日というふうに、考える時間が用意されています。電話一本で、今すぐ口座番号を、というのは、その作法とは、まるで違うのです。

## 第8章 — 数字で見る、いまの規模（8:12–9:11）

最後に、数字を、確かめておきます。

警察庁の統計です。令和7年、1年間の特殊詐欺の被害総額は、全国で、およそ3,257億円。このうち、還付金をかたる詐欺だけで、2,087件が確認されています。

そして、今年——令和8年の上半期、1月から6月までの被害額は、およそ1,816億円。前の年の同じ時期と比べて、5割以上、増えています。1日あたり、およそ10億円の被害が、いまも出続けている計算です。

これは、あらゆる手口を合わせた、特殊詐欺全体の数字です。年金機構をかたる手口だけの数字ではありません。ただ、その中に、鈴木さんが受けたような電話が、確かに含まれています。数字が小さくなる気配は、いまのところ、ありません。

## 第9章 — もしも電話が鳴ったら、すること3つ（9:11–10:26）

では、もし、あなたのところに、似たような電話がかかってきたら。すべきことは、3つです。

ひとつ。口座番号や、マイナンバーカードの写真は、電話でもメールでも、渡さない。
ふたつ。少しでも迷ったら、その場で切る。年金手帳や、ねんきん定期便に印刷されている、本物の窓口番号に、あらためて、かけ直す。
みっつ。少しでも不審だと感じたら、警察相談専用電話、9110。あるいは、消費者ホットライン、188。ひとりで判断せず、相談する。

メールやSMSでも、似た手口が確認されています。「保険料の未納がある」として、決済アプリでの送金へ誘導しようとする、偽のメールです。これも、本物ではありません。年金機構が、メールやSMSで、支払いを求めることはないのです。

鈴木さんが助かったのは、特別な知識があったからでは、ありません。「マイナンバーカードの写真」という、たったひと言に、手を止めただけです。

## 第10章 — ○×クイズで自己診断（10:26–11:38）

それでは、ここまでの内容を、○×クイズで確認してみましょう。声に出さなくても大丈夫です。頭の中で、○か×か、考えてみてください。

ひとつめ。「年金機構から、自動音声で、支給停止のお知らせが来ることがある」。○でしょうか、×でしょうか。
[間] ×です。年金機構自身が、自動音声で連絡することは、ないと明言しています。

ふたつめ。「電話の相手が、生年月日や住所を正確に言い当てたら、それは本物の証拠と考えていい」。
[間] ×です。個人情報は、さまざまな方法で、外部に漏れていることがあります。正確に言い当てられたからといって、本物とは限りません。

みっつめ。「口座番号やマイナンバーカードの写真を求められたら、その場で応じず、いったん切って確認するのが安全」。
[間] ○です。本物の年金機構が、電話でそれらを尋ねることは、ありません。聞かれた時点で、それはもう、答えです。

## 第11章 — 鈴木さんのその後（11:38–12:40）

その日の午後、鈴木さんは、結局、釣りに出かけたそうです。竿を出しながら、隣の釣り仲間に、この話をしました。
「もう少しで、マイナンバーの写真、送るところだったよ」
仲間は、笑いながらも、少し青ざめていたといいます。
「俺だったら……たぶん、送ってたな」

その夜、奥さまにお茶を淹れてもらいながら、もう一度、この話をしたそうです。
「あのまま送ってたら、どうなってたんだろうな」
奥さまは、湯呑みを置きながら、こう返したといいます。
「でも、止まったんでしょう。それでいいじゃない」

鈴木さんは、少し笑って、頷いていました。退職金の話は、一言も出なかったそうです。ただ、電話を止めた、その一瞬の迷いだけが、その日、何度も話題になりました。

## 第12章 — 研究ノート＋今日のお願い＋次回予告（12:40–14:31）

それでは、今日の研究ノートです。

ひとつ。年金機構は、自動音声で連絡すること、口座番号やマイナンバーカードの写真を求めること、ATM操作を指示すること、LINEで案内すること、手数料を求めることは、ありません。
ふたつ。話が「もっともらしい」ことは、本物である証拠には、なりません。
みっつ。少しでも迷ったら、その場で切って、本物の番号にかけ直す。
よっつ。迷ったら、警察相談専用電話9110、または消費者ホットライン188。
いつつ。本物の通知は、たいてい紙で届き、急かしません。

今日のお願いは、ひとつだけです。この研究ノートをスクショして、離れて暮らすご家族に、一度、送ってあげてください。「こういう電話が来たら、途中でも切っていいからね」。そのひと言が、いざというときの、お守りになります。

さて、次回です。来年、60歳になる松本さんの話です。60歳、65歳、70歳。実際に受け取り始める年齢によって、生涯に受け取る総額は、どれくらい変わるのか。松本さんの決断を追いながら、次回の研究で、一緒に計算します。

なお、この動画は2026年8月時点の情報をもとに作成しています。手口は変化することがありますので、少しでも不審に感じたら、警察相談専用電話9110、または最寄りの年金事務所に、直接ご確認ください。

それでは、また次回の研究でお会いしましょう。

=== HẾT KỊCH BẢN ===

## GĐ5 — RETENTION AUDIT (v2, sau lượt sửa 2026-08-26)

1. **Hook 30 giây đầu có ấn tượng không?** ✅ v2 mở bằng cảm giác/hành động (điện thoại rung, câu hỏi trực diện "出ますか。それとも、出ませんか。") — KHÔNG mở bằng tiểu sử ngôi thứ ba như v1. あなた xuất hiện ở câu thứ 9 ("これは、あなたの話かもしれません"), lý lịch 鈴木 nén còn 1 mệnh đề, đặt SAU khi đã có tension.
2. **Có cao trào thật không?** ✅ — v1 chỉ có 1 xung đột nhỏ ("tay dừng ở nút 1", giải quyết <2'). v2 kéo dài thành 2 giai đoạn leo thang (giọng máy → giọng người thật moi thông tin → suýt gửi ảnh Mynumber) trước khi giải quyết — đúng yêu cầu "tính chất cao trào".
3. **Payoff có lộ quá sớm không?** v1: ~15% (quá sớm). v2: mốc "xác nhận 100% là giả" rơi ở **23%** — muộn hơn, và quan trọng hơn: sau mốc đó KHÔNG kết thúc câu chuyện, vì khối "5 điều" ngay sau (第4章) được đóng khung là **ĐÁP ÁN của đúng cú suýt-dính vừa xảy ra** (đối chiếu từng điều với từng bước cuộc gọi), không phải một danh sách đọc rời.
4. **Nội dung có rời rạc không?** So v1 (5 điều → cơ chế → đối chiếu giấy → số liệu → hành động = 5 khối tách biệt), v2 xâu chuỗi bằng callback liên tục tới CHÍNH cuộc gọi của 鈴木: 第5章 giải thích "vì sao nghe lọt tai" NỐI THẲNG từ chi tiết vừa xảy ra (giọng người thay giọng máy); 第7章 đối chiếu giấy thật vẫn giữ mạch "vậy cái gì mới là thật"; 第9章 hành động cụ thể đóng bằng callback "鈴木さんが助かったのは…"; 第11章 mở rộng bằng phản ứng của BẠN câu cá ("俺だったら、たぶん、送ってたな") + vợ — không có khối nào đứng lẻ.
5. **Case đầu trước phút 2?** ✅ — case (cuộc gọi) MỞ NGAY từ giây 0, còn tiếp diễn qua hết 第2章 (kết thúc ~2:43).
6. **Khối giải thích chay >45s?** 第4章 (5 điều, ~102s) và 第8章 (số liệu, ~59s) vẫn là khối trích nguyên văn dài nhất — chấp nhận vì cần giữ chính xác pháp lý, nhưng cả hai đều MỞ/ĐÓNG bằng câu callback trực tiếp tới câu chuyện (không đứng độc lập).
7. **Số nào chưa có trong FACT SHEET?** — không, mọi số/trích dẫn (3.257億, 2.087件, 1.816億, 9110, 188, 5 điều nguyên văn, mô tả giai đoạn 2 xin ảnh Mynumber) đều trong bảng GĐ0b, không có FACT mới phát sinh khi viết lại.
8. **≥2 原典ショット + câu dẫn 「赤で囲んだところ」?** ✅ — 2 câu dẫn ở 第4章 (nenkin.go.jp + npa.go.jp), câu dẫn thứ 2 giờ gắn trực tiếp với chi tiết Mynumber vừa xảy ra thay vì nói chung chung.
9. **Shot 原典 đầu tiên trong 3 phút đầu?** ⚠️ Dời nhẹ — shot #1 rơi vào đầu 第4章 (~3:47), hơi qua mốc 3 phút vì cao trào kéo dài thêm. Chấp nhận có chủ ý: đổi ~47 giây lấy cao trào mạnh hơn — nếu muốn siết lại đúng 3:00 thì rút bớt 1 câu thoại ở 第2章.
10. **CTA giữa video ~50%?** ✅ đo được — **46,1%** (v1: 37,8%, hơi sớm).
11. **Re-hook/pattern-interrupt?** ✅ 第2章→第3章 (khuỷu tay chuyển hướng bằng "手が、止まりました"); 第6章→第7章 (từ CTA quay lại bằng câu hỏi "では、本物の年金機構は…"); 第9章→第10章 (đổi định dạng sang quiz).
12. **Đóng nhân vật bằng cảm xúc?** ✅ 第11章 kết bằng nụ cười + gật đầu, MỞ RỘNG thêm 1 tiếng nói phụ (bạn câu cá) trước khi tới vợ — 2 lớp cảm xúc thay vì 1.

**Kỳ vọng thật:** video "bảo vệ/trust-builder" vẫn không có cú "mất tiền/được tiền" cuối bài — nhưng giờ có cao trào thật (suýt gửi ảnh Mynumber) nên kỳ vọng đường retention 0–3 phút phải DỐC HƠN v1 nếu cấu trúc mới thật sự ăn; đọc số thật sau khi đăng để xác nhận, đừng áp mốc cũ máy móc.

## Lớp `drawn` (3 chỗ, theo `CLAUDE.md`/khuôn cố định `jp-pen`+`grid`)
1. Khối 5 điều "本物は/偽物は" (第4章, ~3:47) → `{"layout":"checklist","mark":"cross"}` — 5 dòng, mỗi dòng ✗ đỏ cho hành vi của KẺ LỪA ĐẢO, có thể thêm dấu ✓ nhỏ cạnh 3 dòng khớp đúng cuộc gọi của 鈴木 (tăng cảm giác "đáp án", không chỉ liệt kê).
2. Slide 「研究ノート」tổng kết (第12章, tĩnh, để screenshot).
3. Khối ○×クイズ (第10章) → `{"layout":"table","anim":true}` — mỗi câu hiện dần, khoanh tròn đáp án đúng.

---

## GĐ6 — ĐÓNG GÓI CTR

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký (~) | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng khi đăng | `【急増中】日本年金機構をかたる詐欺｜自動音声で「支給停止」と言われたら` | 34 | 詐欺@6 | loss-aversion trực diện + trích nguyên văn thoại lừa đảo (đúng khuôn thắng nhất của kênh, khớp swipe file) |
| **A2** | `【被害1,816億円】年金事務所を名乗る詐欺の手口｜本物の通知書との違い` | 37 | 被害1,816億円@1（số liệu 2026 mới, chưa đối thủ nào dùng số này） | đổi keyword dẫn — thử số liệu SHOCK thay vì cảm xúc "急増中" |
| **A3** | `本物とニセモノ、どちらでしょう｜年金をかたる詐欺の電話を検証する` | 32 | — (không có 【】) | đổi kiểu hook — 質問型/mystery, không dùng ngoặc cảnh báo quen thuộc |

### 3 THUMBNAIL A/B (spec — ảnh AI CHƯA gen ở lượt này, xem mục CHUẨN BỊ RENDER)

| | vai | biến | chữ (giữ NGUYÊN ở cả 3, theo luật §3 mục 6) |
|---|---|---|---|
| **T1** | baseline khuôn TELOP/A-45 đang khoá | không đổi | banner trên: `急増中`；hero: `自動音声で詐欺`；dải đáy: `支給停止は嘘です` |
| **T2** | đổi 1 biến HÌNH (nền/tông màu — từ nền giấy sáng sang nền điện thoại/bàn làm việc tối hơn 1 bậc, giữ nguyên chữ) | hình | (giữ nguyên chữ T1) |
| **T3** | đổi LAYOUT (thay banner trên bằng khuôn "điện thoại đang đổ chuông" full khung + chữ đè, bỏ nhân vật) | layout | (giữ nguyên chữ T1) |

**Prompt gen (spec, viết ra để gen sau — theo `ab-3title-3thumb.md` §3.1, KHÔNG gen ảnh trong lượt này):**
- Chủ thể T1/T2: điện thoại bàn KIỂU CŨ hoặc smartphone đang đổ chuông trong tay người cao tuổi (mặt biểu cảm lo/nghi ngờ rõ — MIỄN gate mặt người của nenkin nhưng thêm mặt vẫn tốt hơn nếu có), nền giấy kem (T1) / nền phòng khách tối hơn (T2).
- Chủ thể T3: cận cảnh điện thoại đang đổ chuông + chữ "支給停止" hiện mờ như hologram cảnh báo, KHÔNG có mặt người — layout khác hẳn khuôn quen.
- Chữ bake theo đúng khuôn A-45 (banner+hero+dải đáy), font Noto Sans JP đậm viền đen. Cấm watermark. Chừa góc dưới-phải trống theo `media-library.md` §2.10 ⑤b mục 6.
- ⚠️ Compliance: điện thoại/tay người phải là NGƯỜI HƯ CẤU/stock ẩn danh (không mặt thật cụ thể); KHÔNG hiện logo 年金機構 thật trên màn hình điện thoại (tránh mạo danh hình ảnh cơ quan công — chỉ số 「機構」 dưới dạng chữ kênh tự viết, không copy logo thật).

### Tên file upload
`nenkin-kikou-kataru-sagi-jidoonsei-shikyuteishi.mp4`

### 3 dòng đầu 概要欄
```
自動音声から始まり、人の声に代わり、最後はマイナンバーカードの写真を求められる——実際にあった電話
の一部始終です。本物の年金機構は絶対にしないことが、公式サイトに明記されています。今日は、本物と
偽物の見分け方を、警察庁・年金機構の資料をもとに、一緒に確かめます。
```

### Mô tả đầy đủ (draft, hoàn thiện timestamp thật khi có video)
```
【目次】
00:00 電話が鳴った日：1を、押しました
01:25 「オペレーター」という、もうひとつの声
02:29 止まった、ひと言
03:49 答え合わせ：5つの「絶対にしないこと」
05:06 なぜ「もっともらしく」聞こえたのか
06:17 応援のお願い
06:44 本物の通知書は、こんな姿をしています
07:47 数字で見る、いまの規模
08:50 もしも電話が鳴ったら、すること3つ
10:05 ○×クイズで自己診断
11:16 鈴木さんのその後
12:12 研究ノート・今日のお願い・次回予告

日本年金機構や年金事務所を名乗る電話が増えています。「書類の提出が確認できないため、来月から年金の
支給が停止されます」——最初は機械の声。そのまま1を押すと、今度は人の声が出て、生年月日、住所、
口座番号、そして最後にマイナンバーカードの写真まで、順番に尋ねてきます。この動画は、実際にこの電話
を最後まで受けた方の話をもとに、どこで、なぜ立ち止まれたのかを、一緒にたどります。

日本年金機構は公式サイトで、電話や訪問で口座番号・預金額を尋ねること、自動音声で支給停止を知らせる
こと、ATMの操作や振込を指示すること、LINEで手続き案内をすること、手数料を求めることは、いずれも
「ない」と明言しています。

この動画では、
・実際の通話の流れ（自動音声→人の声→個人情報の聞き取り）
・年金機構自身が公表している「絶対にしないこと」5つ
・警察庁が注意喚起している手口の中身
・令和7年の被害総額（約3,257億円）と令和8年上半期の状況
・不審な電話を受けたときに、すぐできる3つの行動
を、公式資料をもとに、順番に確かめます。

※この動画は2026年8月時点の公開情報をもとに作成しています。手口は変化することがありますので、
少しでも不審に感じた場合は、警察相談専用電話（#9110）、消費者ホットライン（188）、または最寄りの
年金事務所に直接ご確認ください。
※音声: VOICEVOX:雀松朱司

#年金 #老後のお金 #年金と老後のお金研究室 #特殊詐欺 #還付金詐欺
```

### タグ（12 tag nhận diện kênh + đề tài, tổng ~28）
```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金,
65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金,
年金 詐欺, 特殊詐欺, 還付金詐欺, 日本年金機構 詐欺, 年金事務所 なりすまし, 自動音声 詐欺,
還付金, 年金 電話, 不審電話, 警察庁, オレオレ詐欺, 消費者ホットライン
```

### Pinned comment (draft)
```
皆さまのご家族の中にも、似たような不審な電話を受けたことがある方がいらっしゃるかもしれません。
「うちにもこんな電話が来た」「こういうケースはどうなの？」など、実際の体験談やご質問をコメントで
教えてください。皆さまの声が、次の研究テーマになります。
※この動画は2026年8月時点の情報です。少しでも不審に感じたら、警察相談専用電話（#9110）にご相談ください。
```

## Compliance quét nhanh (`youtube-compliance.md`)
- Title/thumbnail: không có từ nhóm mất-ad (殺/血/死/破産…) — 「詐欺」「被害」 là từ mô tả hiện tượng xã hội có ngữ cảnh cảnh báo, không phải bạo lực/gore ✅
- Không tên chính trị gia/đảng/công ty tư nhân thật; CHỈ nhắc tên cơ quan công (年金機構/警察庁) với vai trò TRÍCH NGUYÊN VĂN cảnh báo chính thức của chính họ — không bôi nhọ ✅
- Không dàn dựng nhân vật lừa đảo cụ thể có thật, không dùng giọng/hình ảnh thật của bất kỳ cá nhân nào — 鈴木/田中 là nhân vật hư cấu 100% theo canon kênh ✅
- Không tick "altered/synthetic content" (thumbnail AI + giọng TTS đã credit; nếu lớp sân khấu dùng ảnh AI người thì áp `youtube-compliance.md` §2.1 — xác nhận lại khi chốt SLIDES/render, đúng việc treo đã ghi ở `08_ANALYTICS_LOG.md`)
- Disclaimer thời điểm thông tin + khuyên xác nhận cơ quan (9110/188/年金事務所): có ở 第11章 + mô tả ✅
- Hedge: không dùng 絶対/必ず cho khuyến nghị của MÌNH; các câu 「ことはありません」 là TRÍCH DẪN NGUYÊN VĂN của chính 年金機構/警察庁 (khẳng định về hành vi vận hành của họ, không phải lời hứa lợi ích) — giữ nguyên vì đây là nội dung an toàn nhất có thể nói trong ngách YMYL (cảnh báo lừa đảo dùng nguồn công an/cơ quan công là hướng đi AN TOÀN nhất so với mọi trụ khác của kênh) ✅

---

## 🎬 CHUẨN BỊ RENDER — trạng thái 2026-08-26 (CHƯA làm ở lượt này)

Theo đúng tiền lệ các video trước (script sinh ra trước, SLIDES/ảnh/render là bước sau, cần user tham gia gen ảnh):

1. **SLIDES:** viết `tools/build_slides_17.py` copy khuôn từ `build_slides_16.py` (giữ khoá `sync`, `props`/`props_top`, `pins_card`, `pop`, `fit`/`fit_ar` — xem `CLAUDE.md` §② LỚP STICKER). Trục hình gợi ý: `zu` sơ đồ luồng cuộc gọi 2 GIAI ĐOẠN (giọng máy → giọng người → 4 câu hỏi leo thang → dừng lại, đúng 第2章/第3章 — đây là trục hình QUAN TRỌNG NHẤT bài, nên là chỗ đầu tư nhiều nhất) + `spine` cho chuỗi 5 điều 「本物は/偽物は」(第4章) + `check` cho ○×クイズ (第10章).
2. **原典 screenshot (việc của Claude lúc render, 3 shot):** chụp `nenkin.go.jp/oshirase/gochui/20140129.html` (khoanh đỏ 5 gạch đầu dòng) + `npa.go.jp/bureau/safetylife/sos47/new-topics/250428/03.html` (khoanh đỏ đoạn tự động thoại + #9110/188) + `npa.go.jp/bureau/safetylife/sos47/circumstances/statistics/` (khoanh đỏ tổng thiệt hại + 還付金詐欺 2.087件). **⚠️ Rà lại ngày cập nhật của cả 3 trang tại thời điểm chụp** — WebFetch lúc viết bài trả về ngày không khớp URL, cần xác nhận mắt thường trước khi khoanh đỏ.
3. ⭐ **Ảnh AI — ĐỔI STYLE sang PAPER-COLLAGE (user chốt 2026-08-26).** Khung sân khấu
   `make_stage --channel nenkin` **giữ nguyên**; chỉ style ảnh trong card đổi từ
   `Clean flat vector illustration` sang **newsprint paper-collage** (khuôn của
   `E:\vox-director`, preset `newsprint-editorial`).
   - Tool: **`python tools/art_prompts_collage.py 17_nenkin-sagi-jidoonsei-shikyuteishi`**
     → xuất `art_prompts_FLOW.txt` (1 prompt/dòng, bơm extension) + `art_prompts_BLOCKS.md`
     (bản người đọc) + `art_prompts_TENFILE.txt` (map dòng ↔ tên file).
   - **Lô PROBE đã xuất (5 ảnh, dùng cảnh THẬT của script nên gen xong dùng luôn):**
     `art_denwa_furueru` (entry 0 — chủ thể = cuộc gọi) · `art_te_tomaru` (cao trào, nền đỏ) ·
     `art_tsucho_kakenaosu` (panel `pict`) · `bg_tsukue_denwa` (nền nhạt có chữ đè) ·
     `art_tsuri_nakama` (beat chất người 第11章).
   - 🔴 **BA chỗ cố ý LỆCH khỏi vox-director** (lý do đầy đủ trong docstring của tool):
     ① **KHÔNG bake chữ vào ảnh** — vox-director bake vì nó không có lớp chữ nào khác; mình
     có `make_stage` vẽ Noto Sans JP sắc nét, còn kanji AI thì nát nét (`media-library.md`
     §2.9). ② `bgimg` phải **NHẠT** (có chữ navy đè + `bg_veil 0.78`), chỉ `img`/`pict` được
     dùng nền màu mạnh. ③ ghim **người Nhật cao tuổi** — style newsprint mid-century rất dễ
     trôi về Americana thập niên 50.
   - ⚠️ **Duyệt lô probe TRƯỚC khi gen cả lô ~25 ảnh** — cần thấy tận mắt ảnh collage nằm
     trong card kem `(255,250,238)` có ăn nhau không. Ăn thì mở rộng SPEC trong tool; không
     ăn thì sửa palette/nền trong `BG` (một chỗ, cả lô đổi theo).
   - Ràng buộc cũ **không đổi**: `--ar` bị bỏ qua (luôn ra 1376×768) · cover-crop cắt 11%
     mép phải slot `img` ⇒ **mọi thứ quan trọng trong 85% bên trái** · xoá ✦ watermark bằng
     cách **CẮT** mép phải (lô 1376×768) · giấy tờ trong ảnh phải ô kẻ TRỐNG, không chữ.
4. **`check_pace.py` + `check_zu_layout.py`** trước khi dựng mp4 — chưa chạy ở lượt này (chưa có SLIDES để chạy).
5. **`python tools/make_tts.py 17_nenkin-sagi-jidoonsei-shikyuteishi --dry`** để xác nhận số phút thật (ước lượng hiện tại trong header là suy đoán theo hệ số, CHƯA đo bằng tool).
6. **Đo lại Trend YouTube Search** (bị 429 lúc viết) trước khi chốt A1 làm title đăng chính thức.
