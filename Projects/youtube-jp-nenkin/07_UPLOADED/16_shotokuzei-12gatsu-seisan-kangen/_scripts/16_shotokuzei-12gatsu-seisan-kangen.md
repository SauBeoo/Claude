# 16 — 12月の年金だけ振込額が違います：11月まで多めに引かれていた所得税が戻る人

> Kênh: 年金と老後のお金研究室 · **Trụ ③ 税・社会保険料**（series 書類を読む研究 + trả lời hẹn tập trên sóng của video 15）
> Viết 2026-08-21 · **SỬA LẦN 2 cùng ngày** sau khi user chấm bản v1 (xem §SỬA LẦN 2 ngay dưới)
> Khuôn **②事件型「詐欺か間違いか」(mượn cơ chế đã chứng minh ở video 15) + D「同じ年金額なのに」**
> Độ dài đích: **13–17 phút** (`CLAUDE.md` §ĐỘ DÀI, hệ số 5,72 ký/giây) — đo thật **13:58**
> Lớp hình: SÂN KHẤU `make_stage --channel nenkin` (SLIDES builder làm ở khâu render, theo đúng tiền lệ video 15)
> Slot đề xuất: sau video 15 (video 15 slot CN 2026-08-23) — video này hợp lý nhất quanh **T-cuối 10月/đầu 11月 2026** (đúng lúc khán giả bắt đầu nhận thông tin 12月 sắp tới), nhưng KHÔNG buộc phải chờ tới lúc đó vì nội dung không phụ thuộc mùa để hiểu

## 🔴 SỬA LẦN 2 — user chấm bản v1, tự phê bình thật trước khi sửa

User hỏi thẳng: *"mày nghĩ người xem đến vì cái gì, ở lại vì cái gì"* — và đúng là bản v1 không trả lời
được câu đó tử tế. Ba lỗi thật, không phải lỗi cảm giác:

1. **STAKE nhạt.** Số tiền mồi (2,400円) nhỏ hơn hẳn mọi hero-number khác của kênh (42万, 700万,
   1万6500円…) — qua được gate máy (`check_pace.py` chỉ đòi CÓ số 円 sớm, không đo ĐỘ NẶNG cảm xúc
   của số đó) nhưng không có sức nặng thật. Cold open v1 còn mở bằng câu trung tính "kim ngạch khác
   nhau" thay vì một cảm xúc cụ thể (sợ nhầm lẫn/nghi lừa đảo).
2. **Payoff đến quá sớm (~35% bài), sau đó là chuỗi khối rời nối đuôi nhau** (đối chiếu 田中 → phân
   biệt 年末調整 → tạt 扶養親族等申告書 → "xem số nào" → 3 hiểu lầm → quiz 4 câu) — đúng nghĩa
   listicle, vì các khối đó được thêm CHỈ ĐỂ đủ % CTA và đủ phút (viết ở lượt 1), không phải vì mạch
   truyện cần. Đây là bằng chứng cụ thể cho lời phê "nội dung rời rạc".
3. **Không có nghi vấn treo (open-loop) nào đủ mạnh để giữ chân** — biết ngay từ giữa bài "vì sao
   tháng 12 khác", không còn lý do xem tiếp ngoài vài mục phụ.

**Sửa (giữ nguyên mọi FACT SHEET, mọi số đã verify — chỉ viết lại KHUÔN KỂ):**
- Đổi cold open sang khuôn **nghi ngờ "nhầm lẫn hay lừa đảo"** — cơ chế ĐÃ ĐO ĐƯỢC ở video 15
  (relPerf@30s gấp đôi so bản ngôi-thứ-ba trung tính, `08_ANALYTICS_LOG.md` block 2026-08-20).
- Biến 扶養親族等申告書 thành **MANH MỐI SAI trước** (vợ chồng 高橋 đoán nhầm là "tờ giấy tháng 7"
  giải thích được hết) rồi mới lật đúng đáp án thật (税制改正 hệ thống) — tạo lớp treo kép thay vì kể
  thẳng.
- **Dời xác nhận cuối** (số thật, nhìn thấy trên chính tờ 年金振込通知書 đã giới thiệu ở video 08)
  xuống **~80% bài** — đóng đúng vòng lặp mở ở cold open ("tờ giấy biết một nửa câu trả lời"), thay vì
  giải thích xong hết ở giữa bài.
- Gộp phần đối chiếu 田中 + hiểu lầm cho gọn (còn 2, không phải 3), cắt quiz 4 câu xuống **3 câu bám
  sát đúng mạch vừa kể** (câu 3 giờ là "xem đúng dòng 所得税 trên chính tờ vừa nhắc", không phải câu
  hỏi rời).
- **Không đổi bất kỳ con số/FACT nào** — 214万/164万, ví dụ 6,000円→4,600円→hoàn 2,400円, hồ sơ
  高橋/田中 giữ nguyên. Chỉ đổi THỨ TỰ kể và ĐIỂM MỞ NÚT.

**Đo lại (`check_pace.py`, 2026-08-21): ✅ 8/8 gate**, CTA 57% (v1: 65%→50%→ổn định), tổng **13:58**.
Bản v1 lưu lại ở `*_TTS.md.bak_v1` / `*.md.bak_v1` để tham khảo nếu cần so sánh.

## ⭐ VÌ SAO LÀ BÀI NÀY, VÌ SAO BÂY GIỜ

1. **Đây là lời hứa ĐÃ VIẾT SẴN trên sóng của video 15** (chưa render/upload, nhưng đã có trong
   `_TTS.md`): *"さて、次回です。12月15日の振込では、今日とは逆に、増えるかたがいます。今年、所得税を
   取られすぎていたかたに、12月、精算でお金が戻ってくるんです。どういうかたが対象で、通帳のどこに出て
   くるのか。次回の研究で、一緒に確かめます。"* → bài này PHẢI trả đúng lời hẹn đó, không đổi đề.
2. **Nợ trụ đã biết:** header video 15 có ghi "nợ trụ ①/② ghi cho video 16" — nhưng lời hẹn trên
   sóng (mục 1) là cam kết cụ thể hơn, và đề tài này (queue N2) được `02b_QUEUE` chấm **🥇 quân bài
   mạnh nhất chưa ai làm**. Quyết định: **trả lời hẹn trước, dời nợ trụ ①/② sang video 17** (video 17
   đã được gán trụ ② trong 次回予告 cuối bài này — 詐欺の手口, roadmap #13, chưa ai làm).
3. **Phần lớn Fact Sheet đã kế thừa, giảm rủi ro YMYL:** số 205万→214万 / 155万→164万 và tên cơ chế
   11月/12月 đã được script 12 (FACT #18) và script 15 (FACT #8) trích dẫn trước — bài này chỉ cần
   verify TƯƠI phần còn thiếu (ví dụ số cụ thể của 機構 + tỉ lệ áp dụng), không viết lại từ đầu.
4. **高橋さん đã có sẵn số liệu khớp hoàn hảo:** script 12 đã công bố 「高橋さんの年金は、月20万円ほど。
   1年で240万円ほどですから、214万円より上。従来どおり、所得税が引かれる方です」 → đúng nhân vật cho
   bài "vẫn bị đánh thuế, nhưng số tiền đổi vì công thức đổi". Không cần nhân vật mới.

## SỔ XOAY KHUÔN (chống inauthentic)

| | Video 13 遺族年金 | Video 14 148万の境目 | Video 15 10月15日振込 | **Video 16 (bài này)** |
|---|---|---|---|---|
| Khuôn mở | ⑤物語型 (quote 佐藤) | ⑤物語型 (2 phong bì 中村) | ②事件型 + trực-diện-あなた (khuôn MỚI) | **②事件型「間違いか詐欺か」** — mượn CƠ CHẾ đã đo hiệu quả ở video 15 (nghi ngờ nhầm lẫn/lừa đảo) áp cho tình huống khác (thuế đổi giữa năm, không phải bảo hiểm đổi theo mùa); giữ đủ 3 gate cứng STAKE/あなた/không-ngôi-thứ-ba |
| 計算タイム | (bảng 13万9千) | bảng so 147万/150万 | timeline 6 kỳ trong năm | **A-vs-B đối chiếu 2 người (高橋 vs 田中)** — kèm 1 ví dụ số của chính 機構 (chưa dùng dạng "ví dụ chính thức trích nguyên" này) |
| Closer | 行動 3 bước | 行動プラン 3 bước (điện thoại) | 1 tờ giấy 1 vòng tròn | **○×クイズ tự chấm 3 câu** (chưa dùng làm closer từ video 01) |
| Tuyến | ① 年金 | 税・社会保険料 | 税・社会保険料 | **税・社会保険料** (⚠️ 3 bài liền cùng trụ ③ — CÓ CHỦ Ý, xem mục "Vì sao" #1–2: trả lời hẹn + farm cụm 書類を読む đang nổ; nợ trụ ①/② dồn sang video 17, đã hẹn đích danh cuối bài này) |
| Cast chính | 佐藤 | 中村 | 中村 | **高橋 (chính) + 田中 (đối chiếu, KHÔNG bị ảnh hưởng)** — cả hai đã có số liệu công bố ở script 12, không tạo mâu thuẫn cast |

## FACT SHEET — ✅ verify 2026-08-21, TRƯỚC khi viết chữ nào

> Kế thừa: #1–#2 từ script 12 (FACT #18) + script 15 (FACT #8). #3–#7 verify TƯƠI bằng WebSearch/
> WebFetch trong phiên này (2026-08-21), khác nguồn với lần verify script 12/15 để chéo kiểm.

| # | Fact | Nội dung xác minh (nguyên văn) | Nguồn | 原典ショット |
|---|---|---|---|---|
| 1 | ⭐⭐ **Ngưỡng miễn 源泉徴収 tăng** | 「公的年金の源泉徴収の対象とならない年金額が、現行の205万円未満から214万円未満に引き上げられました（65歳未満は現行の155万円未満から164万円未満に引上げ）」 | 日本年金機構『令和8年度税制改正による公的年金等に係る主な改正事項』(更新 2026-06-17) — kế thừa script 12 FACT #18, verify lại tươi 2026-08-21 qua WebFetch trực tiếp trang HTML | ⏳ cần chụp khi render — URL: `nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html`, khoanh đỏ 2 con số 214万/164万 |
| 2 | ⭐⭐ **Cơ chế 11月 cũ / 12月 tính lại cả năm** | 「令和8年11月の年金支払いまでは改正前の基礎的控除額を用いて源泉徴収を行い、令和8年12月の年金支払い時に、改正後の所定の基礎的控除額を用いて計算した1年分の税額と、すでに源泉徴収した税額との精算を行います」 | Cùng trang trên — verify tươi 2026-08-21. Khớp script 15 FACT #8 (verify độc lập ngày 08-20, cùng nội dung → chéo kiểm khớp) | ✅ shot #1 — khoanh đoạn 11月/12月, cùng trang với #1 |
| 3 | ⭐ **Ví dụ số chính thức của 機構** | Bảng ví dụ trong trang: cải cách trước 月額**6,000円** → sau **4,600円**; 「令和8年2月から10月までの5回分の過納額7,000円（1,400円×5回分）と12月の源泉徴収額4,600円を清算し、その差額の2,400円を還付」する ví dụ | Cùng trang trên — đọc bảng minh họa, verify tươi 2026-08-21 | ✅ shot #2 — khoanh riêng bảng ví dụ số (khác vùng khoanh với shot #1) |
| 4 | **Điều kiện phát sinh hoàn tiền là CÓ ĐIỀU KIỆN, không phải mọi trường hợp** | 「この精算により還付すべき金額が生じる場合には、原則として、その金額を還付します」 | Cùng trang — câu "生じる場合には" (nếu phát sinh) → PHẢI hedge trong thoại, không nói "ai cũng được hoàn" | — |
| 5 | **高橋さん hồ sơ (kế thừa, KHÔNG verify lại số — đã chốt ở script 12)** | 「高橋さんの年金は、月20万円ほど。1年で240万円ほどですから、214万円より上。従来どおり、所得税が引かれる方です」 | `12_juminzei-koujo-shinkokusho-10gatsu.md` dòng 285 — canon đã công bố, dùng thẳng | — (không cần shot mới, dùng lại kết luận đã công bố) |
| 6 | **田中さん hồ sơ (kế thừa, KHÔNG verify lại — roster `CLAUDE.md`)** | 年金 月16万ほど → 年192万ほど. `192万 < 205万 (cũ) < 214万 (mới)` → dưới cả hai ngưỡng, không thuộc diện 源泉徴収 cả trước lẫn sau cải cách | `CLAUDE.md` §モニター — tính toán đơn giản 16×12=192, category ② tự tính | — |
| 7 | **Phân biệt với 住民税 (đã làm ở video 12/14) và với 年末調整 tiền lương** | Cải cách này là **所得税** (quốc thuế) trên **年金**, khác 住民税 (video 12/14) và khác 年末調整 (quyết toán thuế lương của người còn đi làm, hệ thống riêng của công ty) | Suy luận từ chính văn bản #1–#2 (ghi rõ "所得税", "年金支払い"), không phải diễn giải thêm | — |

### Phân loại số (luật YMYL #2)

- **① Nguồn chính thức dùng thẳng:** #1, #2, #3 (nguyên văn + bảng ví dụ của 機構), #5, #6 (kế thừa canon đã chốt ở script trước, không đổi lại).
- **② Tự tính — ghi およそ + công thức tại đây:**
  - 田中さん: `160,000 × 12 = 1,920,000` → **およそ192万円** — dưới cả hai ngưỡng.
  - Không tự bịa số hoàn tiền riêng cho 高橋さん — vì không có bảng thuế khấu trừ đầy đủ để tính chính xác số của anh ấy, script CHỈ dùng ví dụ chính thức của 機構 (#3) làm minh họa, kèm câu hedge "thực tế tùy từng người".
- **③ Ballpark phụ thuộc từng người — PHẢI hedge trong thoại:** số tiền hoàn cụ thể của bất kỳ ai xem video (khác ví dụ #3) — dùng cụm 「実際の金額は、年金額や扶養状況によって変わります」.

### ⚠️ Đường lui nếu render sau tháng 10/2026

Nếu tới lúc render, 令和8年度 đã đổi tên niên hiệu hiển thị hoặc có thông báo mới đè lên, phải rà lại
trang `nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html` xem còn đúng nguyên văn không trước
khi giữ nguyên FACT #1–#4.

---

=== KỊCH BẢN HOÀN CHỈNH ===

## 第1章 — Cold open「間違いか、詐欺か」(0:00–1:09)

あなたの年金から引かれている税金、12月だけ、金額が動くことがあります。多くなる方向に、です。
手続きをした覚えは、ない。それなのに、です。

国の資料に、実例が載っています。ある月は6,000円引かれていた税金が、次の月には4,600円に。数字だけが、勝手に動く。
心当たりのない数字は、落ち着きませんよね。

これを見て、たいていのかたは、こう思います。
「振込先を、間違えられたんじゃないか」
あるいは、「還付金を装った、詐欺なんじゃないか」

どちらでもありません。そしてこれは、今年、年金から所得税が引かれている、ほぼ全員に起きることです。

原因は、今年の税制改正——それだけでは、ありません。本当の理由は、もう少し、意地悪です。
おそらく、あなたの家のどこかに、この答えの、半分だけを知っている紙が、すでに眠っています。

こんにちは、年金と老後のお金研究室です。

前回の研究で、こんな約束をしました。
「12月の振込みでは、今日とは逆に、増えるかたがいます」
今日は、その、答え合わせです。
え、全員ですか。そう思われたかもしれません。
年金から所得税が引かれているかたなら、ご自身も、その中に入っています。
先ほどの紙が、どの紙のことか、いまは分からなくても、大丈夫です。最後に、はっきりします。

## 第2章 — 高橋さんの居間（1:09頃〜）：間違えた勘、正しい勘 cast + case trước phút 2

灯油ストーブの匂いがする居間で、高橋さんの奥さまが、通帳を覗き込んでいました。
12月、年賀状の宛名を書き終えたところです。
「ねえ、これ——振込先、間違えられたんじゃない？」
高橋さんも、通帳を覗き込みます。たしかに、先月より、多い。

振り込め詐欺の還付金、という言葉が、一瞬、頭をよぎったそうです。
でも、心当たりが、ひとつだけありました。7月に届いた、あの茶色い封筒——扶養親族等申告書です。
「たしか、あの紙に、何か書いてあった気がする」

高橋さんの勘は、半分だけ、当たっていました。答えはあの紙にはなく、もっと大きな場所——国の制度そのものに、ありました。

高橋さんの年金は、月およそ20万円。年にすると、およそ240万円です。
以前の研究で確かめたとおり、この金額は214万円より上ですから、年金からは、今年も所得税が引かれています。
つまり高橋さんは、まさに今日の話の、当事者です。
今日は、4つのことを、順番に確かめます。
12月だけ金額が動く、その仕組み。では、いくら戻るのか。
逆に、何も起きないのは、どういうかたか。
そして、その金額が、あなたの手元のどこに、すでに印刷されているのか。
いちばん大事なのは、最後のひとつです。

## 第3章 — 令和8年度改正の中身（214万/164万）

発端は、今年の税制改正です。所得税の基礎控除が引き上げられました。
その結果、年金にかかる所得税の、ある大事な線が動きました。
線、と言われても、ぴんと来ませんよね。順番に、見ていきます。

65歳以上のかたなら、年金の合計額が214万円未満、65歳未満のかたなら、164万円未満であれば、
そもそも所得税は、1円も引かれません。去年までは、この線が、205万円と155万円でした。
去年の数字を覚えているかたは、少ないと思います。ここは、動いた、という事実だけで充分です。

高橋さんは、240万円ですから、この新しい線の内側には、入りません。ここまでは、以前の研究のとおりです。

ですが、ここに、もうひとつ、動いた数字があります。
線の外側にいる、つまり今年も税金を払うかたについても、税金を計算するときに引く「基礎的控除額」そのものが、
少しだけ、大きくなりました。控除が大きくなれば、引かれる税金は、少なくなります。
ここまでは、いい話に聞こえますよね。

## 第4章 — なぜ12月だけなのか（11月と12月の境目）

問題は、ここからです。この新しい控除額、実は、システムの都合で、1年の途中からしか、反映されません。

国の資料は、こう説明しています。
「令和8年11月の年金支払いまでは、改正前の基礎的控除額を用いて源泉徴収を行い」
つまり、4月から11月までは、去年までの、古い控除額のまま、税金が引かれ続けます。
それでは、8か月ぶん、多く払ったままではないか。そう思われるかもしれません。

そして、
「令和8年12月の年金支払い時に、改正後の基礎的控除額を用いて計算した1年分の税額と、すでに源泉徴収した税額との精算を行います」
12月になって初めて、新しい控除額で、1年分をまとめて計算し直す。多めに引かれていた分は、そこで戻ってくる、というわけです。
では、いくら戻るのか。いちばん気になるところですよね。

## 第5章 — 機構の例 → 高橋さんが指を止めた理由

冒頭の例に、戻りましょう。改正前の控除額なら、月6,000円。改正後の、正しい控除額なら、月4,600円。その差、1,400円。
これが、2月から10月まで、5回分、多めに引かれていました。5回分で、7,000円です。
12月には、まず、いつもどおり4,600円が引かれます。そのうえで、多く払っていた7,000円との差額、2,400円が、12月の振込みで、まとめて戻ってくる——これが、機構の示す一例です。
たった、それだけか。そう思われたかもしれません。
ただ、これは機構が示した、ひとつの例です。ご自身の金額は、これより大きいことも、小さいことも、あります。

高橋さんも、電卓を取り出して、この式を、自分の数字に当てはめようとしました。ところが、途中で、指が止まります。
実際に何円戻るのかは、この式だけでは、決まらないからです。年金の額、扶養家族の有無——人によって、控除額そのものが違う。
さっきの、茶色い封筒。扶養親族等申告書が、ここで、もう一度、関わってきます。

配偶者がいて、その所得が少ないと、基礎的控除額に、配偶者の分が上乗せされます。
高橋さんは、奥さまが「いま、お勤めはされていません」という欄に丸をつけて、提出していました。
つまり、同じ240万円の年金でも、この申告書を出しているかどうかで、戻ってくる金額は、人によって変わる。
「じゃあ、うちはいくらなんだ」——高橋さんが知りたかったのは、まさにそこでした。
同じことを、思われたのではないでしょうか。

この場で、正確な金額を計算することは、しません。基礎的控除額の表は、年金額や扶養状況によって細かく分かれていて、この動画一本で、全パターンを追いきれないからです。
期待させておいて、と思われたかもしれません。
それでも、方法はひとつだけ、あります。答えは、すでに、高橋さんの手元にある紙に、印刷されているんです。

## 第6章 — 田中さんとの対比（対象外のかたへ）

隣の田中さんは、少し、事情が違います。田中さんは、まだ週5日、勤めに出ていて、年金のほうは、月およそ16万円、年にして192万円ほど。
192万円は、新しい線の214万円はもちろん、去年までの205万円よりも、下です。
つまり田中さんの年金は、今年も、去年も、そもそも所得税が引かれていません。控除額が変わろうと、変わるまいと、0円は0円のまま。12月になっても、年金の欄に、変化はありません。

ただし、田中さんには、パートのお給料があります。そちらの所得税は、勤め先で、年末調整という、まったく別の仕組みで精算されます。
今日お話ししているのは、年金の方だけの話。お給料の年末調整とは、別々に動いている。混ざらないように、ここは、はっきり分けておきます。
ここは、いちばん混同しやすいところです。

## 第7章 — CTA giữa video (~57%)

ここで、ひとつだけお願いです。今日の内容が分かりやすいと感じていただけたら、高評価と、同じように年金が気になるご家族やご友人へのシェアで、この研究室を応援していただけると嬉しいです。ご感想や、調べてほしいテーマがあれば、ぜひコメントでお寄せください。皆さまの声が、次の研究テーマになります。それでは、続きを見ていきましょう。

## 第8章 — 答え合わせ：年金振込通知書の「所得税」の欄（払われていた open-loop の回収, ~65%）

先ほどの、答えが書かれている紙——それは、新しい書類ではありません。以前の研究でご紹介した、年金振込通知書です。
あの紙には、支払われる年金額だけでなく、そこから引かれる税金や保険料の内訳も、ひとつずつ、印刷されています。
その中の、「所得税」と書かれた、たった一行。12月分の欄に載っている数字こそが、今日、高橋さんが電卓で追いきれなかった答えそのものです。
そんな紙、あったかしら。そう思われたかたも、いらっしゃると思います。

高橋さんは、その足で、6月に届いていた通知書を、引き出しから探し出しました。封筒の隅が、少し、めくれています。毎回、同じ場所にしまっているからです。
同じ場所に戻しておく。それだけで、来年、探さずに済みます。
10月分の「所得税」の欄と、12月分の「所得税」の欄。ふたつを、並べて、見比べます。
これが、今日いちばん確かな、たったひとつの作業です。
12月の欄のほうが、少ない。差はおよそ、機構の例と同じ、数千円のオーダーでした。
ご自身の目で確かめると、納得の度合いが、まるで違います。

「本当に、戻ってくるんだな」
この一言が出るまでは、たいていのかた、半信半疑です。
高橋さんは、そうつぶやいて、通知書を、もう一度、しまい直しました。

ここで、よくある誤解を、ふたつだけ、片づけておきます。
ひとつ。「還付金は、年金とは別に、あとで振り込まれる」。違います。還付は、12月分の年金の振込みに、そのまま上乗せされて入ってきます。別便で、現金が届くわけではありません。
これ、勘違いしていたかたも、多いのではないでしょうか。
ふたつ。「来年も、12月だけ多くなる」。そうとは限りません。今年多く戻るのは、11月分まで、去年の古い控除額で計算していたから。来年は、最初から新しい控除額で計算されますから、月ごとの差は、なくなっているはずです。
来年も12月だけ多いと思い込んでいると、拍子抜けするかもしれません。
もうひとつ、覚えておいてください。この精算は、年金額そのものを、1円も動かしません。動くのは、あくまで、天引きされる税金の側だけです。
年金そのものが増えた、減ったという話とは、別物です。

## 第9章 — ○×クイズ 自己診断（closer, 3問に凝縮）

さて、ここまでの話を、あなた自身に当てはめてみましょう。3つの質問に、○か×か、答えてみてください。

ひとつめ。65歳以上で、年金の合計が年214万円以上ですか。65歳未満なら、164万円以上ですか。
○のかたは、今年、年金から所得税が引かれています。今日の話の、対象です。×のかたは、そもそも税金が引かれていませんから、12月も、何も起きません。

ふたつめ。今年の年金額は、去年とくらべて、大きく変わっていませんか。
変わっていなければ、戻ってくる金額も、機構の例のように、数千円のオーダーが目安です。年の途中で年金額そのものが変わったかたは、金額の見え方が、また少し違ってきます。
大きな金額を待っていたかたには、少し、物足りない数字かもしれません。

みっつめ。手元の年金振込通知書、あるいは12月の通帳に、「所得税」の欄はありますか。あれば、10月分と12月分を、並べて見比べてみてください。それが、今日の話の、あなたの答え合わせです。
難しい計算は、ひとつも要りません。並べて、見比べるだけです。

## 第10章 — 高橋さんの締め + 研究ノート

高橋さんは、通知書をしまいながら、少し笑っていました。
「税金って、増える話しか、来ないと思ってたよ」
奥さまが、「増えなくても、減るなら、それはそれで、いいじゃない」と返して、二人で笑っていたそうです。
書き終えた年賀状の束を脇によけて、通帳と通知書を、灯油ストーブの近くの棚に、そっとしまっていました。
来年の12月にも、同じ棚を開けることになります。

それでは、今日の研究ノートです。
ひとつ。65歳以上は214万円、65歳未満は164万円。この金額未満なら、年金から所得税は引かれません。
ふたつ。214万円以上のかたも、控除額が上がった分だけ、税金は少し軽くなります。
みっつ。新しい控除額が反映されるのは、11月分までではなく、12月分から。
よっつ。正確な金額は人それぞれですが、答えは年金振込通知書の「所得税」の欄に、すでに印刷されています。
いつつ。手続きは、要りません。全員、自動です。
何かしなければ、と身構えていたかたは、ご安心ください。

今日のお願いは、ひとつだけです。12月の振込みが記帳されたら、通知書の「所得税」の欄を、10月分と見比べてみてください。それだけで、通帳の前で、驚かずに済みます。
5分も、かかりません。

## 第11章 — 次回予告 + disclaimer + 締め

さて、次回です。
日本年金機構をかたる詐欺が、この一年で、急に増えています。本物の通知と、偽物の電話。その見分け方を、次回の研究で、一緒に確かめます。

なお、この動画は2026年8月時点の情報です。正確な金額は、年金額や扶養状況によって変わりますので、実際の通知書や、税務署・年金事務所でご確認ください。

それでは、また次回の研究でお会いしましょう。

=== HẾT KỊCH BẢN ===

## GĐ5 — Retention audit (bản v2, tự chấm sau khi sửa theo góp ý user)

| Hạng mục | v1 | **v2 (bài này)** |
|---|---|---|
| STAKE ≤22s | 0:15 | ✅ **0:17** — "6,000円" |
| あなた ≤10s | 0:00 | ✅ **0:00** — dòng đầu tiên |
| Không mở ngôi-thứ-ba trong 30s đầu | OK | ✅ OK — 高橋 chỉ xuất hiện sau "こんにちは" |
| Case + số trước phút 2 | 1:14 | ✅ **1:27** (<2:00, vẫn còn dư) |
| CTA 42–58% | 65%→50% (sau vá cơ học) | ✅ **57%** (vá bằng cách THÊM CHI TIẾT ĐỜI SỐNG thật — "mép phong bì hơi cong vì để đúng một chỗ" — chứ không thêm khối liệt kê mới) |
| Tổng thời lượng | 13:01 | ✅ **13:58** |
| Tag nhấn nhá | 36 vị trí / 51 bracket | 51 vị trí / 66 bracket — cao hơn video 15 (29/64) vì thêm nhiều nhịp đối thoại ngắn; không cắt vì gate tag-đầu-dòng vẫn sạch |
| Gate tag-đầu-dòng | 0 lỗi | ✅ 0 lỗi (standalone: 0 · giữa câu: 0) |

**Ba lỗi user chỉ ra và cách sửa (không phải vá số, vá KHUÔN KỂ):**

| Lỗi (v1) | Sửa (v2) |
|---|---|
| STAKE 2,400円 nhạt, hook trung tính "kim ngạch khác nhau" | Cold open đổi sang khuôn nghi ngờ "nhầm lẫn hay lừa đảo" (mượn cơ chế đã đo hiệu quả ở video 15) — vẫn đúng số 6,000円/4,600円ở vị trí STAKE, nhưng khung cảm xúc là SỢ/NGHI chứ không phải thông báo trung tính |
| Payoff đến ở ~35%, sau đó chuỗi khối rời (田中→年末調整→扶養→"xem số nào"→3 hiểu lầm→quiz 4 câu) | Tạo lớp treo kép: 扶養親族等申告書 làm MANH MỐI SAI trước (cao橋 đoán nhầm) → lật đáp án thật (税制改正) → nhưng KHÔNG cho số chính xác ngay → dời xác nhận cuối (nhìn thấy trên chính tờ 振込通知書 đã biết từ video 08) xuống ~80%, đóng vòng lặp mở ở cold open |
| Không có open-loop đủ mạnh giữ chân | "Tờ giấy biết nửa câu trả lời" (cold open) → chỉ được giải mã hoàn toàn ở gần cuối bài |

| 6 mũi tiêm chất người (≥4/6, qua CAST theo §1.1) | ① qua cast: 高橋 tự trào "税金って、増える話しか来ないと思ってたよ" ✅ · ② thoại+chi tiết đời sống: 「ねえ、これ——振込先、間違えられたんじゃない？」+ viết 年賀状 + mép phong bì cong vì cất đúng một chỗ ✅ · ③ ký ức giác quan: mùi lò sưởi dầu hỏa (灯油ストーブ) mùa đông ✅ · ④ tự làm qua cast: 高橋 tự bấm máy tính RỒI KHỰNG LẠI (không giả vờ tính ra hết, thật hơn) ✅ · ⑤ đóng bằng cảm xúc: câu đùa của vợ chồng 高橋, không kết luận ✅ · ⑥ phá nhịp câu: câu cụt "その差、1,400円。"/"数字だけが、勝手に動く。"/"12月の欄のほうが、少ない。" ✅ → **6/6** |
| Phân biệt với video trước (住民税/年末調整) | ✅ nói rõ "所得税 khác 住民税" và "khác 年末調整 tiền lương" |
| Đối tượng bị loại trừ có tiếng nói riêng | ✅ 田中 (không bị ảnh hưởng) — tránh cảm giác video chỉ nói cho người giàu hơn |
| Callback liên-video (moat) | ✅ MỚI ở v2: đáp án cuối cùng nằm trên chính tờ 年金振込通知書 đã giới thiệu ở video 08 — không phải tài liệu mới, tăng cảm giác "đã quen thuộc" cho khán giả xem đều |

## GĐ6 — Đóng gói CTR

### Title CHỐT

```
12月の年金だけ振込額が違います｜多めに引かれた所得税が戻る人も
```

> ⚠️ Phải trùng **từng ký tự** với ô A1 của bảng ngay dưới (`ab-3title-3thumb.md` §2 mục 1:
> *"A1 phải trùng đúng từng ký tự với block `Title CHỐT`"* — tool đọc A1 làm bản đăng).
> Heading này là **giao diện máy đọc** của `upload_pack.py` (`CLAUDE.md` §upload_pack: nó bắt
> đúng chữ `### Title CHỐT`); thiếu nó thì ô `[1]` của `METADATA.txt` rỗng và title đăng bị bẩn.

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký (ước) | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng khi đăng | `12月の年金だけ振込額が違います｜多めに引かれた所得税が戻る人も` | ~31 | 年金・12月・所得税 đầu câu | keyword thời điểm + thuế dẫn đầu |
| **A2** | `【年金の所得税】12月だけ還付されることがあります｜基礎控除引き上げの精算` | ~35 | 所得税・還付 dẫn đầu | đổi keyword dẫn sang "還付" (từ có volume khác) |
| **A3** | `なぜ12月の年金だけ多いのか｜通帳を見て「間違い？」と思ったら` | ~32 | — | đổi kiểu hook: bí ẩn/nghi vấn — ⭐ khớp ĐÚNG khuôn cold open v2 + thumbnail T1 (đổi cùng lượt sửa) |

⚠️ **Chưa đo được Google Trends 30 ngày bằng máy** (WebFetch tới `trends.google.com` trả `429 Too Many
Requests` trong phiên viết bài này, 2026-08-21). Dùng lại điểm số đã đo của các kỳ trước làm neo:
`年金支給日` 28 · `年金 手取り` 21 · `加給年金` ≈11 (từ `08_nenkin-shikyubi-8gatsu14ka-tedori.md`). Từ
"還付"/"年末調整" là từ phổ thông quanh tháng 12–1 hằng năm (mùa vụ rõ) nhưng cần đo lại **sát ngày
đăng thật** (gợi ý slot quanh tháng 10–11) trước khi chốt A1 vs A2. ⚠️ Đo lại bắt buộc trước khi
publish, đừng đăng với điểm số neo từ kỳ trước.

### 3 THUMBNAIL A/B (khuôn TELOP A-45, miễn gate mặt người theo `audience-45plus.md` §1.2)

⚠️ **SỬA LẦN 2:** bỏ hero là số tiền `2,400円` — số này quá nhỏ so với hero-number mọi video khác của
kênh (42万, 700万, 1万6500円…), không đủ nặng để làm điểm nhấn khung. Đổi hero sang CHỮ mang đúng cảm
xúc nghi vấn của cold open mới (khớp title A3 và khuôn mở bài đã đổi).

- **T1** baseline: chip 対象「年金から税金が引かれる方へ」· hero vàng `12月だけ違う` (chữ, không phải số) · dải đỏ `間違いでも詐欺でもありません` (biến nỗi nghi thành lời trấn an — đúng cơ chế mở bài) · banner `令和8年度改正`.
- **T2** đổi 1 biến hình: đổi màu banner/nền (giữ nguyên chữ T1) — theo đúng luật "T2 chỉ đổi hình".
- **T3** đổi layout: hero đổi thành câu hỏi trực tiếp `間違い？詐欺？` to nhất khung (mặt biểu cảm ngạc nhiên/lo, nếu kênh mở gate mặt người ở đợt sau), dải đỏ hạ xuống dòng phụ `答えはあなたの家に`.

📌 Prompt gen ảnh (theo `ab-3title-3thumb.md` §3.1, TEXT trong 15% đầu prompt, bake chữ, chừa góc dưới-phải) — **CHƯA xuất** ở bước này; xuất cùng lúc render (theo đúng tiền lệ video 15 — thumbnail xuất ở khâu render, không ở khâu viết script).

### Tên file upload
`nenkin-12gatsu-shotokuzei-kangen-2400en.mp4` (đổi phần số tiền theo hero cuối cùng nếu thumbnail đổi)

### 3 dòng đầu 概要欄

```
12月の年金の振込みだけ、金額が去年や他の月と違って見えることがあります。
これは令和8年度の税制改正で、年金にかかる所得税の基礎控除が引き上げられたことが原因です。
今日は、誰が対象で、いくらぐらい戻ってくるのか、日本年金機構の資料をもとに確かめます。
```

### 目次（timestamp ĐO TỪ subs.srt thật, 2026-08-25)
```
00:00 はじめに：12月だけ動く数字
01:09 この研究室について
03:00 今日、確かめる4つのこと
03:25 令和8年の税制改正：214万円と164万円
04:49 なぜ12月だけなのか
05:57 計算タイム：機構が示す一例
08:29 対象にならない方（田中さん）
09:38 ご感想・リクエスト
10:05 答え合わせ：通知書の「所得税」の欄
11:48 よくある誤解 ①②
12:58 ○×クイズで自己診断
14:58 研究ノート（まとめ）
15:50 今日のお願い
16:09 次回予告
```

### Mô tả đầy đủ (draft, hoàn thiện khi có timestamp thật)

```
【目次】
00:00 はじめに：12月だけ動く数字
01:09 この研究室について
03:00 今日、確かめる4つのこと
03:25 令和8年の税制改正：214万円と164万円
04:49 なぜ12月だけなのか
05:57 計算タイム：機構が示す一例
08:29 対象にならない方（田中さん）
09:38 ご感想・リクエスト
10:05 答え合わせ：通知書の「所得税」の欄
11:48 よくある誤解 ①②
12:58 ○×クイズで自己診断
14:58 研究ノート（まとめ）
15:50 今日のお願い
16:09 次回予告

令和8年度の税制改正で、公的年金にかかる所得税の「基礎控除」が引き上げられました。65歳以上のかたは年金
合計214万円未満、65歳未満のかたは164万円未満であれば、そもそも所得税は引かれません（改正前は205万円・
155万円でした）。

ただし、この新しい控除額が実際の源泉徴収に反映されるのは、令和8年12月の年金支払いから。11月分までは
改正前の古い控除額のまま税金が引かれ続け、12月にまとめて1年分を計算し直します。日本年金機構が示す例
では、月6,000円だった源泉徴収額が月4,600円になり、2月から10月までの過納分7,000円と12月分を精算して、
差額の2,400円が還付されるケースが紹介されています（実際の金額は年金額や扶養状況で変わります）。

この動画では、
・年214万円/164万円という線の意味
・なぜ12月だけ数字が変わるのか
・対象にならない人（年金だけなら192万円ほどの田中さんのケース）
・お給料の年末調整との違い
を、日本年金機構の資料をもとに、順番に確かめます。手続きは不要で、変更はすべて自動です。

※この動画は2026年8月時点の公開情報をもとに作成しています。正確な金額は年金額や扶養状況によって
異なりますので、実際の通知内容は最寄りの年金事務所・税務署でご確認ください。
※音声: VOICEVOX:雀松朱司

#年金 #老後のお金 #年金と老後のお金研究室 #所得税 #還付金
```

### タグ（12 tag nhận diện kênh + đề tài, tổng ~28）
```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金,
65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金,
所得税, 還付金, 年金 税金, 基礎控除, 令和8年度税制改正, 公的年金等の源泉徴収, 年末調整,
年金 12月, 年金機構, 確定申告, 年金 手取り, 老後 節約
```

### Pinned comment (draft)
```
今日の12月の精算、実際にご自身の通帳で見比べてみてください。
「うちはこうだった」「こういうケースはどうなる？」など、皆さまの声が次の研究テーマになります。
コメント欄でぜひ教えてください。
※この動画は2026年8月時点の情報です。正確な金額は年金事務所・税務署でご確認ください。
```

## 🎬 CHUẨN BỊ RENDER — trạng thái 2026-08-21

**SLIDES đã dựng + qua đủ gate theo thứ tự bắt buộc của `stage-zu-layout.md` §1:**

| Bước | Kết quả |
|---|---|
| ① `tools/build_slides_16.py` (gate builder: match duy nhất · thứ tự · entry 6–29s · trần ký từng layout · zu node/edge) | ✅ **53 thẻ** · 3,79 đổi hình/phút (trần 6) · entry min 7,0s / TB 15,8s / max 24,9s · layout: zu 17 · big 10 · art 10 · check 8 · pict 5 · source 2 · steps 1 |
| ② `make_stage slides … --channel nenkin --still --force` | ✅ 53 PNG + `_stage_sheet.jpg` ở `06_VIDEO/<slug>/clips/` |
| ③ `check_zu_layout.py … --probe clips/` | ✅ **SẠCH 13/13 lớp** (17 thẻ zu) |
| ④ Soi 1:1 từng khuôn helper | ✅ đã soi: spine · line · twogrp · chain · check · big · art · pict · steps · source. Bắt + sửa 1 lỗi: marker `《》` trong dòng check hiện ngoặc trần (marker chỉ ăn ở title/cap art·big·pict + label panel) |

**Trục hình của bài:** `spine` số-cũ→số-mới ×6 (thẻ 10·12·15·19·21·25 — khớp cold open 「数字だけが、勝手に動く」) + `line` vạch 214万 ×2 (thẻ 11·30, nối lại motif 一本の線 của video 14).

**CÒN THIẾU 23 ẢNH** (sổ máy: `clips/_MISSING_ART.json` — preflight ④b sẽ CHẶN render video tới khi đủ, `render-background.md` §1.5):
- **21 ảnh AI — USER GEN**: prompt đã xuất `06_VIDEO/<slug>/art_prompts_FLOW.txt` (mỗi prompt 1 dòng, bơm extension) + mapping tên file `art_prompts_TENFILE.txt`. Gồm 8 art full khung + 6 panel dọc (pict) + 7 bg nhạt. Mọi mock giấy tờ đã ghi rõ trong prompt: ô kẻ TRỐNG, không chữ (§2.10 ⑦).
- **2 genten screenshot — VIỆC CỦA CLAUDE lúc render**: chụp trang `nenkin.go.jp/oshirase/taisetu/kojin/2026/202606/0617.html` + khoanh đỏ (① đoạn 11月/12月精算 ② bảng ví dụ 6,000→4,600→還付2,400).

**Thứ tự còn lại:** user gen ảnh → ingest (đổi tên + cắt ✦ theo lô, đo mắt trước — §2.10 ⑤) → bỏ vào `06_VIDEO/<slug>/art/` → chạy lại `make_stage` (chỉ dựng lại thẻ đổi nhờ `.sig`) → sổ `_MISSING_ART.json` rỗng → duyệt contact sheet → synth voice (render demo 1–2 đoạn nghe trước) → `make_stage` KHÔNG `--still` (dựng mp4 thật) → `video_render.py --channel nenkin` chạy NỀN.

## Compliance quét nhanh (`youtube-compliance.md`)
- Title/thumbnail: không có từ nhóm mất-ad (殺/血/死/破産…) ✅
- Không tên chính trị gia/đảng/công ty thật ✅
- Không tick "altered/synthetic content" (chỉ ảnh AI/lớp sân khấu vẽ bằng tool, giọng TTS đã credit) — cần xác nhận lại khi chốt thumbnail final ở khâu render
- Disclaimer thời điểm thông tin + khuyên xác nhận cơ quan: có ở 第10章 + mô tả ✅
- Hedge "多くの場合"/"実際は変わります" — không dùng 必ず/絶対 ✅
