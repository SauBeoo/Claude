# Content Plan — 年金と老後のお金研究室 (gom về 3 TRỤ, chốt 2026-07-23)

> **Định vị khóa:** 「制度を読むチャンネルじゃない。あなたの数字を計算する研究室」 — kênh **TÍNH SỐ HỘ cụ già** về 年金・給付金・税. KHÔNG mở rộng ra ngoài 3 trụ dưới.
> Benchmark: 年金・給付金完全攻略 **12 video → 130K sub** = ngách hẹp này thắng bằng TRÚNG + đều, không cần cày rộng.

## ⛔ KHÔNG KHÔ KHAN — xương sống bắt buộc mọi video (user chốt 2026-07-23)

> Hẹp PHẠM VI nhưng KHÔNG hẹp cảm xúc. "Tính thuế/给付金" mà kể chay = chết CTR + retention.

Mỗi video BẮT BUỘC đủ 3 thứ (không có đủ → chưa được viết):
1. **1 CON SỐ đắt** làm nhân vật chính (số tiền lỗ/được cụ thể: 生涯○○万円 / 年6万7千円 / 大損).
2. **1 nhân vật モニター** (伊藤/佐藤/鈴木/高橋/山田/田中/松本) mang số đó vào đời thực — "giải thích chế độ chay" tối đa 45 giây rồi phải chen case/câu hỏi.
3. **1 hook 決断/損 (loss-aversion)** ở cold open + thumbnail (末路/大損/申請しないと消える/知らないと損) — đâm sợ ~25–30s rồi mới hé lối thoát (theo CLAUDE.md cold open + `.claude/rules/youtube-compliance`).
- Trần YMYL: số có nguồn thật (日本年金機構/厚労省/総務省), làm mềm 「〜の場合が多い」, không 絶対/必ず, không tên đảng/chính trị.
- Signature xoay vòng: 2 video liền nhau KHÔNG cùng khuôn mở bài / cùng trụ (sổ khuôn ở header mỗi script). 「視聴者の実験室」 = moat: mời khán giả gửi số → tính hộ.

## ⚠️ Mỗi chủ đề TRƯỚC KHI thành script: đo lại YouTube Search 30d (`gprop=youtube, geo=JP, date=today 1-m`) theo `youtube-upload-seo.md` mục 0.5.

---

---

# ⭐⭐ PLAN VIDEO 19–23 — LÁI THEO **HÀNG XÓM ĐO ĐƯỢC** (chốt 2026-08-30)

> User: *"Dựa vào các video được đề xuất của kênh đi theo hướng đó và lên plan cho những kịch bản tiếp theo."*
> Số gốc: `06_VIDEO/_diagnose/related_2026-08-30.txt` (tool mới `pull_related.py`, 90 ngày).
> Luật: `.claude/rules/youtube-suggested-growth.md` §1 + §1.5 · `CHANNEL_DIAGNOSIS_2026-08-29.md` §3.5.

## A. SỐ ĐO — và cảnh báo cỡ mẫu phải đọc TRƯỚC

⚠️ **90 ngày RELATED = 25 video dẫn / TỔNG 27 view.** Tức gần như mỗi video đúng **1 view**.
Ở cỡ này, **thứ hạng từng video là nhiễu** — đừng bao giờ nói "video X là hàng xóm mạnh nhất".
Thứ **đọc được** là **CỤM THỂ LOẠI**: một thể loại xuất hiện bằng **nhiều kênh độc lập** thì đó
là tín hiệu thật, vì nó không thể do một cú click may mắn tạo ra.

**Ba cụm đúng ngách nổi lên (8/25 video):**

| cụm | kênh dẫn (độc lập) | view kênh | AVD người sang |
|---|---|---|---|
| ⭐ **年金インタビュー đường phố** | 年金と暮らし · 年金額聞いてもいいですか · 老後のリアル街角 | 339K · 22K · 1,7K | **302s · 302s** · 80s |
| ⭐ **制度 gõ cửa / giấy đến nhà** | 元スマホ店員の暮らし守り隊 (NHK徴収強化・訪問員に絶対〇〇と言うな) | 827K | **206s** |
| **再雇用・シニア lao động** | 2chビジネス速報 (再雇用してあげたのに…) | 225K | 53s |

17/25 còn lại là nhiễu ngoài ngách (プロ野球 · SKE48 · 麻雀 · ラブホ · 車 · 禁煙…) — đúng chẩn
đoán §3.5: YouTube đang xếp kênh vào **"feed đàn ông 65+ nói chung"**.

🔴 **Phát hiện đáng giá nhất: cụm 年金インタビュー có BA kênh độc lập, và hai AVD cao nhất trong
nhóm đúng ngách (302s).** Người sang từ đó **ở lại gấp đôi** người sang từ nhiễu (~30–70s).
⇒ Đây là **khu phố đúng**, và nó cho biết **TRẠNG THÁI ĐẦU NGƯỜI XEM lúc họ tới**: họ vừa xem một
cụ già CÓ THẬT nói ra con số lương hưu của mình, và đang nghĩ *"vì sao lại ra con số đó / của tôi
thì bao nhiêu"*.

## B. CHIẾN LƯỢC — làm ĐÁP ÁN cho câu hỏi mà 年金インタビュー đặt ra

| | 年金インタビュー (hàng xóm) | 年金と老後のお金研究室 (mình) |
|---|---|---|
| cho | **MỘT CON SỐ** của người thật | **CƠ CHẾ** ra con số đó + số của CHÍNH bạn |
| thiếu | không giải thích vì sao | — |

Định vị sẵn có của kênh (`「あなたの数字を計算する研究室」`) **khớp đúng chỗ trống của họ** ⇒ mình là
"next watch" tự nhiên. Ba việc thi hành, không cái nào đòi đổi bản sắc:

1. **TITLE dẫn bằng SỐ TIỀN + TÌNH HUỐNG NGƯỜI, không dẫn bằng TÊN CHẾ ĐỘ.**
   Khuôn hàng xóm: `【年金いくら？】74歳「…」年金インタビュー` → khuôn mình:
   `<số tiền/tháng> + <ai bị> + <vì sao>`. Video 18 (`月4万3千円減ります`) **đã đúng hướng** — giữ.
   ⛔ Bỏ hẳn `【見逃し厳禁】` (7/9 video cũ) — tag chung chung đó đang bắt cả feed drama (§3.5).
2. ⭐ **MỞ FRANCHISE 「明細を一緒に読む」** — mỗi video có **một khối đọc GIẤY THẬT dòng-theo-dòng**
   (給料明細 · 通知書 · 決定通知 · 源泉徴収票). Nó cho đúng khoái cảm "lộ con số" của thể loại
   インタビュー **cộng** thứ họ không có (cơ chế), và tự đẻ ra 原典ショット mà YMYL đang bắt buộc.
   📌 Video 08 (通知書の6欄) đã chạy thử hình dạng này — nay nâng thành **kỳ lặp lại**, không phải một lần.
3. **Cụm "giấy đến nhà / người gõ cửa"** (NHK 827K, AVD 206s) là cụm mạnh thứ hai và **kênh đã
   thắng ở đó** (公金受取口座 — swipe 64,6× và 29,7×). Giữ nhịp 1 bài/tháng thuộc dạng này.

⛔ **KHÔNG làm:** chạy theo nhiễu (野球/麻雀/恋愛) để "hợp feed hiện tại" — đó là feed SAI, mục tiêu
là **thoát** nó. Cũng không tăng nhịp (§4.3): thêm video vào feed sai = thêm mẫu AVD đáy.

## C. BẢNG PLAN 19–23

Xoay trụ tiếp từ 18 (trụ ①): **② → ① → ③ → ② → ①**. Slot T3·T5·CN 19:00.
⚠️ Slot là **chỗ trống, không phải chỉ tiêu** — chưa qua gate thì bỏ slot, không đăng bù.

| # | Trụ | Title working | Hàng xóm mục tiêu (đo được) | Cú lật / vì sao |
|---|---|---|---|---|
| **19** | ② 給付金 | **高年齢雇用継続給付｜給料が下がった分を国が補う…はずが、率が変わりました** | ⭐ 2chビジネス速報 `再雇用してあげたのに…` (225K) · cụm 年金インタビュー | 🔒 **BỊ KHOÁ bởi lời hứa trên sóng** — video 18 kết bằng 「松本さんの給料明細を見ながら、次回の研究で、一緒に計算します」. Đây cũng là **kỳ ĐẦU của franchise 明細を一緒に読む** (B.2). Cast 松本 (nối tiếp 18). ⚠️ FACT SHEET phải verify **率 đổi từ 令和7年4月** — video 18 đã nói câu này trên sóng, sai là phải đính chính |
| **20** | ① 年金 | **遺族年金は「夫の年金の4分の3」ではありません｜入らない部分があります** | ⭐⭐ 年金と暮らし `74歳「ひとり暮らしの年金生活」` (339K, **AVD 302s**) — hàng xóm khớp nhất cả bộ | Swipe **5,6×** (お金の保健室 15.183 view/12 ngày). Người vừa xem một bà goá 74 tuổi sống một mình → câu hỏi kế đúng là "còn lại bao nhiêu". **Cú lật:** phần 4 phần 3 chỉ tính trên 厚生年金, **基礎年金 của chồng biến mất** |
| **21** | ③ 税 | **年金から引かれる額は「出す書類」で変わります｜158万円はもう古い基準** | 元スマホ店員 `訪問員に絶対〇〇と言ってはいけない` (827K, AVD 206s) — cùng dạng "giấy/người tới, có thứ phải làm" | Swipe **6,2×**. **Trả nợ trụ ③** (sổ ghi từ 08-10: "video 11 BẮT BUỘC trụ ③", vẫn đang lệch). Franchise: đọc **源泉徴収票** dòng-theo-dòng |
| **22** | ② 給付金 | **未支給年金｜亡くなった月の年金は、家族が請求できます** | cụm 年金インタビュー · 年金と暮らし (goá bụa) | 🔴 **ĐỔI 2026-08-30 — bản cũ (10月15日 支給日) TRÙNG VIDEO 15** (`15_nenkin-furikomi-10gatsu-honchoshu` = đúng 「10月振込・本徴収・介護保険料」). Bắt được lúc rà sổ trước khi viết. Thay bằng **未支給年金**: trụ ② thật (取り逃し), chưa làm, nối tiếp 20 nhưng đổi góc — 20 hỏi *"còn lại bao nhiêu"*, 22 hỏi *"khoản CUỐI CÙNG chưa ai lấy"*. Franchise: đọc **未支給年金・未支払給付金請求書** |
| **23** | ① 年金 | **年金の請求書が届かない人がいます｜届く人・届かない人の分かれ目** | お金の保健室 `請求書、今年届くのは3パターンだけ` (swipe **13,7×**) | Nối thẳng video 18 (請求書に丸をつける前に) nhưng đổi câu hỏi: 18 hỏi *"khoanh gì"*, 23 hỏi *"nếu không nhận được thì sao"* — **cùng khu phố, không trùng nội dung** |

## ⭐⭐ T-GATE — CỔNG CHỌN ĐỀ TÀI (chốt 2026-09-15, chạy TRƯỚC khi viết chữ nào)

**Lỗ hổng nó bịt:** `check_pace.py` có 17 gate và **tất cả đều soi CHỮ**. Không cái nào hỏi
*"bài này nói cho AI nghe?"* — nên **video 19** đi qua sạch mọi gate rồi ăn **AVP 11,5% (bét
kênh)**: đề tài 高年齢雇用継続給付 chỉ áp cho **60–64 tuổi và còn đi làm**, trong khi
**74,9% khán giả là 65+**. Chữ không sai gì cả; **đề tài sai NGƯỜI**.
Và đây không phải sai số nhỏ — rổ swipe đo được chênh **300×** giữa nhóm đề tài đúng và sai.

| | hỏi gì | cách chấm |
|---|---|---|
| **T1** ⚙️ | ≥70% khán giả đủ điều kiện? Có đòi *đang đi làm* không? | **MÁY** — gate `G18` |
| **T2** ⭐ | Có **tờ giấy tự đến**, hoặc **trạng thái tự đổi nếu không làm gì**? | người |
| **T3** | Có mốc ngày trên lịch? | người |
| **T4** | Có một con số 円 đã verify trong FACT SHEET? | người |
| **T5** | Trong 3 trụ, không nằm ⛔KHÔNG LÀM? | người |
| **T6** | Có dòng swipe ≥3× trong 60 ngày, hoặc median `bench_topic.py`? | người |

**Chốt: T1 + T5 CỨNG**, rồi **T2 + ít nhất một trong T3/T4**. T6 bắt buộc cho slot chính,
được miễn cho slot 実験室.

⭐ **Câu phân biệt của T2 — câu đắt nhất của cả cổng:**
> ***Không làm gì thì có chuyện gì xảy ra với họ không?***

公金受取口座 tự đăng ký = **CÓ** (1,67M view). Đi khai để được hoàn thuế = **KHÔNG**, chỉ là
bỏ lỡ — và cả nhóm đó chết: 控除証明書 9,4K · 源泉徴収票 7,6K · 年金の確定申告 2,4K.
Đúng một câu này tách được mọi video thắng khỏi mọi video chết trong sổ.

### Khối bắt buộc ở header mỗi script (`03_SCRIPTS/<stem>.md`)

```
### 対象者
年齢: 65+ / 60-64 / 55-64 / 全年齢
就業: 不問 / 在職必須 / 退職前後
推定カバー率: <%>
```

`python tools/check_pace.py <stem>` → **G18 in ĐẦU BẢNG** (đề tài sai người thì mọi mục dưới
vô nghĩa). Rớt nếu: thiếu khối · `カバー率 < 70%` · `就業 = 在職必須` · **hoặc khai khống**
(ghi `年齢: 60-64` mà khai `95%` → chặn bởi trần nhân khẩu 22,6%).
Nhân khẩu Studio 2026-08-29: **65+ 74,9% · 55–64 22,6% · 45–54 2,5%**.

⚠️ **CHƯA ĐƯỢC KIỂM CHỨNG.** Cổng này dựng từ **một** ca hỏng (v19) + bảng chênh 300×; chưa
video nào đi qua nó. **3–4 video pass T-GATE mà AVP vẫn ~15% ⇒ kết luận đúng là "đề tài cũng
không phải đòn bẩy"**, không phải "siết cổng chặt hơn".

### Chấm lại hàng đợi bằng T-GATE (2026-09-15)

| mục trong queue | T-GATE | hành động |
|---|---|---|
| 介護保険料を安くする | ✅ 65+ · 決定通知書 tự đến · 本徴収 9–10月 · có 円 | **đẩy lên slot kế** (mùa, hết tháng 9 là mất) |
| 後期高齢者医療保険料 (75歳以上) | ✅ coverage mạnh nhất | giữ cao |
| ゆうちょ銀行ルール変更 | ✅ 全年齢 · quy tắc tự đổi | giữ, slot 実験室 |
| マイナンバー／資格確認書 | ✅ | giữ |
| 支給日直前チェック | ✅ | giữ, khoá theo lịch |
| **106万円の壁が10月に消えます** | 🔴 **rớt T1** (在職必須) | **bỏ khỏi slot chính** |
| **退職金の受け取り方** | 🔴 **rớt T1** (退職前後 ≈ 60–65) | hạ xuống 実験室 |
| **定期便に載っていない年金・給付金5選** | ⚠️ **rủi ro T1** | xem dưới |

🔴 **Bản sao hit 452K của カメ先生 có cùng bệnh với v19.** `ねんきん定期便` là giấy gửi cho
người **ĐANG ĐÓNG** — phần lớn dưới 65. Giữ nội dung (5 khoản không nằm trên giấy), nhưng
**đổi neo sang 年金証書 / 年金振込通知書 に載っていない** — thứ tệp 65+ thật sự cầm trong tay.
⚠️ Tao **không đo được** nhân khẩu của カメ先生; đây là phán đoán theo cơ chế, không phải số đo.

## C.0 ⭐⭐ CHEN SÓNG THÁNG 9 + QUEUE 24–30 (đo tươi 2026-08-31, kế hoạch user duyệt — nguồn số: `01_SWIPE_TITLES.md` mục nạp 08-31 + `youtube-jp-health/06_VIDEO/_niche_scan/`)

**CHEN NGAY: farm v04/v10 góc mới 「9月・緑の封筒」 → ✅ ĐÃ VIẾT 2026-08-31 = VIDEO 24**
(`03_SCRIPTS/24_shien-kyufukin-midori-futo-9gatsu.md` + `_TTS.md`) — check_pace **PASS 11/11**
(bản đầu tiên qua đủ G9/G10/G11), ~13,3′, khuôn ②事件型 + thang 3 bậc, 渡辺+中村 nối v04/v10.
Slot đề xuất **CN 09-06 19:00** (sau v19 T5 09-03). Còn lại: rà 2 mục ⚠️ FACT + chụp 3 原典ショット
mới + gen ảnh/sticker + builder `build_remotion_24.py` (checklist cuối file script).
⚠️ Claim 「対象者拡大」 của フクロウ KHÔNG dùng (chưa verify) — script chỉ nói cơ chế đã verify.
📌 Đánh số: plan cũ ghi 19–23; bài chen này lấy số **24** vì script 20–23 đã viết sẵn trong
`03_SCRIPTS/` — THỨ TỰ ĐĂNG thì 24 đi trước 20–23 (sự kiện có kỳ hạn thắng thứ tự số).

**QUEUE 24–30** (xoay 3 trụ; mỗi đề khi thành script phải đo lại Trends §0.5 + ghi HÀNG XÓM MỤC TIÊU):

| ưu tiên | đề | trụ | số nguồn (08-31) | ghi chú |
|---|---|---|---|---|
| ⭐ cao | 定期便に載っていない年金・給付金5選 | ①② | カメ先生 **452K** (kênh 26 ngày tuổi!) · フクロウ 815K · 完全攻略 3,79M | 🔓 **MỞ KHOÁ SỚM** — lời khuyên "lùi tới GĐ C/khi có uy tín" (07-25, dòng MEGA-EVERGREEN dưới) bị số mới BÁC: kênh 4,7K sub 1 tuần tuổi vừa thắng bằng đúng đề này. Format N選, 20–30′ |
| ⭐ cao | ゆうちょ銀行ルール変更 — tiền của bạn bị đổi tự động | **Ô THỬ NGHIỆM** | 定年前後 **282K** · チャコラ 240K · さゆり 95K | user gật 2026-08-31 mở 1 ô thử ngoài 3 trụ. Góc 研究室 hoá: "quy tắc đổi → tiền/quyền của bạn đổi theo". Đọc số sau 2 tuần: ≥5× median kênh thì giữ ô, thua thì đóng; ⛔ không lan sang シニア割/旅行 khi chưa có số của mình |
| cao | 介護保険料を安くする | ③ | フクロウ 10K/2,3 ngày (**đang nổ**) · さゆり 50K · 完全攻略 96K | mùa 本徴収 9–10月, đăng trong tháng 9 |
| vừa | 106万円の壁が10月に消えます | ③ | カメ先生 3K/2,3d đang leo | tin tháng 10 — đăng cuối tháng 9 |
| vừa | マイナンバーカード×年金/保険証 | ② | フクロウ 396K+228K+193K (farm 4×) | |
| vừa | 後期高齢者医療保険料 — chọn tệp **75歳以上** | ③ | タヌキ 88K (bản 60歳+ chỉ 4,1K) | |
| vừa | 退職金は「受け取り方」で手取りが変わる | ③ | 保健室 22K, swipe 8,3× | họ hàng v11 nhưng góc khác |
| ⭐ lịch | 支給日直前チェック 15/10 (farm v15) | franchise | v15 của mình 1.116 view | đăng 12–13/10 theo rule 支給日 |
| lịch | 総集編 >60′ cụm 「届く紙」 | — | フクロウ có bản 1:18:19 cùng khuôn | nối 3 tập ĐÃ đăng + chương mục đầy đủ, slot CN đầu tháng 10 (`audience-45plus.md` §4.1) — máy kéo GIỜ XEM rẻ nhất cho ngưỡng YPP 4.000h |

### ⭐⭐ VIDEO 27 — ĐÃ CHỐT 2026-09-17 (user gật phương án A)

**Đề:** 「年金振込通知書に載っていない給付金5つ｜出さないと1円も来ません」 — 5 khoản KHÔNG nằm
trên bất kỳ tờ giấy nào người xem nhận, vì chế độ không gửi giấy cho người chưa đăng ký.
**Trụ ①②** (bắt buộc đổi khỏi ③ của v25/v26) · khuôn mở **③質問型** (v25 ①, v26 ④) ·
計算タイム = チェックリスト5問 · cast 渡辺 + 高橋 · **15–17′** (5 mục × ~2,5′).
Slot đề xuất: **T3 22/9 hoặc T5 24/9** (13/10 để dành 支給日直前チェック farm v15).

**Bằng chứng (đo 2026-09-17):**
1. **Hàng xóm mục tiêu = nguồn RELATED số 1 của chính kênh mình**: `カメ先生のもらえるお金 —
   【50歳以上】ねんきん定期便に載っていない年金・給付金5選` (4 view dẫn sang, cao nhất bảng
   90 ngày; 452.820 view / 4.770 sub = **94,9×**, kênh 26 ngày tuổi).
2. **Video HUB — lý do chính, không phải ratio.** 5 mục = 5 tập ĐÃ có (加給年金 v06 · 未支給 v22 ·
   支援給付金 v04/10/24 · 特別支給 v07 · 遺族 v13/20). Kênh đo được **AVP browse 15,2% vs
   RELATED 27,5%** mà `END_SCREEN` cả đời = **1 view** ⇒ hub trỏ nội kênh là đường rẻ nhất kéo
   browse → RELATED, đúng đòn bẩy `CLAUDE.md` §③ gọi là lớn nhất.
3. Format N選 kênh **chưa từng dùng** → chống inauthentic + đổi trụ đúng luật xoay.

**T-GATE:** T1 ✅ `65+ / 就業:不問 / カバー率 ~75%` — không mục nào đòi đang đi làm (khác hẳn v19) ·
T2 ✅ mỗi khoản *"không làm gì thì không bao giờ tới"* · T3 ✅ 時効 5年/2年 · T4 ✅ số verify sẵn
(423.700円 · 67.000円 · 36万) · T5 ✅ trụ ①② · T6 ✅ swipe 94,9×.

🔴 **SỬA NEO so với T-GATE 09-15** — đo Trends YouTube 30d (geo=JP, gprop=youtube, 2026-09-17):

| keyword | mean | đọc |
|---|---|---|
| **年金 給付金** | **10,9** | cao nhất rổ → **từ dẫn của title** |
| 年金 手続き | 8,5 | |
| 加給年金 | 6,0 | |
| **年金振込通知書** | 3,3 (spike max 100) | ✅ giữ làm NEO |
| **年金証書** | **0,2** | ⛔ **BỎ** — T-GATE 09-15 đề xuất neo này, đo ra gần 0 |
| ねんきん定期便 · 未支給年金 · もらい忘れ年金 | **0,0** | hit 452K của họ đến từ **browse/suggested, KHÔNG từ search** ⇒ đừng chép keyword của nó |

⏳ **Chưa verify, chưa được vào script:** mục thứ 5. Nghiêng **高額療養費の外来年間合算 (70歳以上)**
— thuần tiền y tế CỦA NGƯỜI XEM; ⛔ không lấy 高額介護合算療養費 vì chạm ranh giới ngách `kaigo`.

**Luật farm:** video của MÌNH vượt ~10× median kênh (hiện ≈ >1.000 view) → farm 2–3 góc trong 2 tuần
(カメ先生/フクロウ/タヌキ đều farm winner 3–4×). Ứng viên sẵn: v12 住民税・v15 振込.
⚠️ Sóng nổ ĐÃ ĐÔNG người vào (bài học 9月ハガキ: kênh 120K sub vào trễ 4 ngày chỉ ăn 743 view) —
chen sóng phải chen SỚM, trễ >1 tuần thì bỏ, quay về queue evergreen.

### ⭐⭐ VIDEO 28 — ĐÃ VIẾT 2026-09-18 (user gật đề "後期高齢者医療保険料")

**Đề:** 「年金の医療保険料、75歳の誕生月に計算し直されます｜2年で切れる軽減」 —
`03_SCRIPTS/28_kouki-75sai-tanjyotsuki-hokenryo.md` + `_TTS.md`. **check_pace ĐẠT HẾT 23/23**, 16:56,
trụ ③, khuôn mở **②事件型**, 計算タイム **thang 3 bậc**, closer **シェア用ノート** (kênh chưa dùng).
Cast: **小林 (75・埼玉県川口市) MỚI** + 中村 (71・新潟県). Slot: **CN 20/9 hoặc T5 24/9**.

**Bằng chứng chọn đề (đo 2026-09-18):**
1. `bench_topic.py`: median **199.536 view · 44 video ≥100K · 341 view/ngày` — **trần cao nhất** trong
   rổ 5 đề đo cùng lượt (資格確認書 49K · ゆうちょ 38K · 年金振込通知書 104K · マイナ保険証 24K).
2. Hàng xóm: `タヌキ 88.580 view`「75歳以上｜7月以降に届く後期高齢者医療保険料通知書」 +
   `フクロウ 100.034`「7月に届く介護保険料決定通知書」 — mình là **câu kế tiếp** của cả hai
   (họ dạy đọc giấy tháng 7, mình trả lời *tháng 10 số đổi và軽減 hết hạn lúc nào*).
3. Mùa: **10月 = 本徴収 1回目** ⇒ đăng trong tháng 9 là đúng cửa.

🔴 **Đã cắt khỏi queue:** mục `後期高齢者医療保険料 — chọn tệp 75歳以上` ở bảng QUEUE 24–30 → **XONG**.

🔴 **Hai thứ đề này để lại cho video sau, đừng làm mất:**
- **Hero 「同じ年金額でも住む県で年6万4千円違う」** (東京都 月10.352円 vs 青森県 月4.990円, verify từ
  bảng 47 tỉnh của PDF 厚労省). Số này **mạnh hơn** hero đang dùng, nhưng **lặp khuôn v26**
  (「年金は同じなのに介護保険料が年3万7千円違う」) ⇒ chỉ dùng làm beat phụ ở v28. **Mở lại khi cách
  v26 ≥4 video**, tức từ v30.
- **子ども・子育て支援金** (令和8年度 全国 月194円, 高齢者も拠出): v28 chỉ nêu cơ chế + số trong thân
  bài, **cố ý KHÔNG lên title/thumbnail** vì dễ bị đọc thành bình phẩm chính sách. Nếu bao giờ làm
  riêng thì phải giữ đúng nếp đó.

⚠️ **Điểm yếu đã biết trước của v28, ghi để đọc số cho đúng:** 決定通知書 chỉ gửi cho **75+**, nên
カバー率 72% là ước **lạc quan hơn v27** (v27: ai nhận 年金 cũng có 振込通知書). Nếu AVP browse < 14,4%
thì **nghi đề tài trước, không nghi chữ** — gate script đã sạch 23/23.

### ⭐⭐ ĐỀ MỚI CHO VIDEO 29 — đo tươi 2026-09-21 (`bench_topic.py`, 4 lượt, 12 rổ)

**Ràng buộc đã khoá trước khi đo** (v27 = trụ ①②/khuôn ③質問型 · v28 = trụ ③/khuôn ②事件型):
v29 **phải** trụ ① hoặc ②, khuôn mở **①LOSS-REVEAL** hoặc **④対決型**, 計算タイム khác
`チェックリスト5問` (v27) và `thang 3 bậc` (v28). Slot: **T5 24/9 hoặc CN 27/9 19:00**.

| | đề | trụ | median view | ≥100K | v/ngày (≤90d) | T-GATE |
|---|---|---|---|---|---|---|
| **A** ⭐ **CHỌN** | **資格確認書／マイナ保険証** | ② | **52.851** | **19** | 29,8 | **T1 ~100%** — cao nhất kênh từng có |
| **B** | ゆうちょ銀行ルール変更 | ô thử nghiệm | 46.431 | 14 | **551,9** | ✅ nhưng sóng đã 5 tuần |
| **C** | 2027年 年金制度改正 | ① | 78.072 | **39** | 395,6 | 🔴 **RỚT T1** — xem cảnh báo |
| D | 現況届 | ① | 1.007 | **0** | 44,1 | trần thấp → chỉ slot 実験室 |
| E | 高額療養費 70歳以上 | ② | 1.709 | 5 | 5,0 | T2 yếu + hit toàn của kênh 1,1M sub |
| F | 寡婦年金・死亡一時金 | ② | 164 | 1 | 1,5 | chết |
| — | マイナ保険証 高齢者 (rổ kiểm chéo của A) | ② | 25.024 | 13 | 8,7 | — |

🔴 **C là cái bẫy v19 lặp lại, đừng ham con số 39 video ≥100K.** Nội dung 年金制度改正法 2027年4月
gần như toàn bộ là **被用者保険の適用拡大 · 在職老齢年金の基準額 · 標準報酬月額上限 · 遺族厚生年金
(65歳未満の妻)** ⇒ **đòi đang đi làm hoặc dưới 65**, trong khi 74,9% khán giả là 65+. Đối thủ ăn view
bằng title chung chung 「年金が変わる」 rồi nội dung lệch tệp — mình copy là ăn đúng **AVP 11,5% của
v19**. Chỉ mảnh **マクロ経済スライド (改定率 4月)** là đúng tệp, mà mùa của nó là tháng 1–4, không phải
tháng 9.

⚠️ **Nhiễu query đã bắt được trong chính lượt đo này:** rổ `障害年金 65歳` trả về **đúng các video của
rổ `2027年改正`** (スガワラ 5,75M · サラダ 3,26M) ⇒ search khớp theo chữ 年金 chứ không theo intent.
Số của rổ đó **đã vứt**, không đưa vào bảng. Cùng bệnh đã ghi ở `youtube-upload-seo.md` §0.5 mục 4.
📌 Rổ `年金 口座 使えなくなる` đo ra median **277.973** nhưng **chỉ 10 long-form** và nội dung trùng
rổ ゆうちょ ⇒ đó là **một sóng đơn lẻ nhìn qua lỗ kim**, không phải một đề. Dùng B, không dùng nó.

#### A — spec đề nghị cho video 29

**Đề:** 「保険証がわりの紙が届かない人がいます｜窓口で一度、全額払うことになります」(working —
⚠️ **title phải đo Trends §0.5 trước khi chốt**, chưa đo lượt này).

- **Trụ ②** theo đúng cách sổ đã xếp nó (`QUEUE 24–30`: *マイナンバーカード×年金/保険証 | ②*) ⇒
  **không trùng trụ ③ của v28**.
- **T1 ✅ CỨNG, mạnh nhất kênh từng có:** `年齢 65+ / 就業 不問 / カバー率 ~100%` — mọi người có bảo
  hiểm y tế đều dính, khác hẳn v28 (72%, chỉ 75+) và v19 (đòi đang đi làm).
- **T2 ✅✅** *không làm gì thì sao?* → **thẻ hết hạn / không còn được gửi tự động** ⇒ ra viện phải
  **trả 10 phần 10 rồi đi xin hoàn sau**. Đây là hậu quả thật, không phải "bỏ lỡ" — đúng vế thắng
  của câu phân biệt T2.
- **T3 ✅** có mốc 有効期限 trên tờ giấy · **T4 ✅** số 円 đối chiếu 1割 ↔ 10割.
- **Khuôn mở ④対決型** (マイナ保険証 ↔ 資格確認書 — hai lối, chọn sai thì trả tiền) · **計算タイム
  ○×クイズ** (cả hai đều chưa dùng ở v27/v28).
- ⭐ **Cú lật (đắt nhất, và là chỗ kênh khác bỏ trống):** cùng MỘT lần nhập viện —
  người dùng **マイナ保険証** được áp 高額療養費 **tự động tại quầy**; người dùng **資格確認書** phải
  xin thêm **限度額適用認定証**, không xin thì **ứng trước cả trăm nghìn yên** rồi chờ hoàn.
  ⇒ Đây là「同じ病気・同じ病院・同じ日、払う額が違う」= khuôn 対決 có số, không cần bịa.
- **Cast:** 田中 (67・横浜) + 伊藤 (68・福岡); **callback 小林 (75・川口) một dòng** để nối thẳng v28
  → đúng đòn bẩy hub/END_SCREEN kéo browse → RELATED (`CLAUDE.md` §③).
- **Hàng xóm mục tiêu:** チャコラのお金研究所 `ﾏｲﾅﾝﾊﾞｰｶｰﾄﾞ廃止で届く資格確認書` **843.625** ·
  としこの年金相談所 `マイナンバーカード廃止→資格確認書が届く人の落とし穴` **715.084** ·
  オタク会計士 `保険証廃止まとめ` 859.010. Mình là câu kế tiếp: họ nói *giấy nào đến*, mình nói
  ***cầm tờ nào thì ở quầy phải trả bao nhiêu***.
- **Độ dài 13–17′.**

🔴 **Hai rủi ro phải xử TRƯỚC khi viết chữ nào:**
1. **YMYL — trạng thái 2026 của chế độ này đổi liên tục.** FACT SHEET bắt buộc verify tận nguồn
   厚労省/各広域連合: ① mốc 廃止 2024-12-02 + 経過措置 ② điều kiện được **職権交付** 資格確認書
   ③ 有効期限 và cách gia hạn ④ 資格確認書 có tự áp 限度額 không ⑤ thủ tục 利用登録解除.
   ⛔ Không được suy từ trí nhớ — đây đúng loại số mà `CLAUDE.md` §③ cấm bịa.
2. ⚖️ **Compliance — ngách này đầy title màu chính trị** (「政府が隠す罠」「〇〇しない人の末路」).
   Kênh CẤM (`youtube-compliance.md` §5 + §③ YMYL). Giọng 研究室: **cơ chế + số**, không một chữ
   đánh giá chính sách. Cùng nếp đã giữ với 子ども・子育て支援金 ở v28.

#### B — nếu muốn chen sóng thay vì evergreen

`ゆうちょ銀行ルール変更` = **ô thử nghiệm user đã gật 2026-08-31**, và 3 tuần sau vẫn nổ
(みんなの給付金 285K/13 ngày = **21.936 view/ngày**; さゆり 340K; 定年前後 344K).
⚠️ Nhưng sóng bắt đầu ~18/8 ⇒ vào bây giờ là **trễ 5 tuần**, ngược thẳng bài học 9月ハガキ
(*kênh 120K sub vào trễ 4 ngày chỉ ăn 743 view*). Chọn B là **cố ý nhận rủi ro đó** để đổi lấy
một phép thử ô ngoài-3-trụ; nếu chọn thì phải đăng trong tuần này, không lùi.

#### Đã có sẵn trong lịch, không phải đề mới

- **支給日直前チェック 15/10** (farm v15, trụ ①) — khoá đăng **12–13/10**, tức là v30/31 theo ngày.
- **総集編 >60′ cụm 「届く紙」** — nối 3 tập ĐÃ đăng (v09 · v24 · v28 đều là "giấy đến nhà"), slot
  CN đầu tháng 10. Không phải nội dung mới, nhưng là **cách rẻ nhất kéo giờ xem** cho ngưỡng YPP
  4.000h (`audience-45plus.md` §4.1 — bắt buộc có chương mục + nói rõ là 総集編).

### ⭐⭐ VIDEO 29 — ĐÃ VIẾT 2026-09-21 (đề A của bảng trên)

**Đề:** 「年金暮らしの方へ｜8月から、一枚では病院で使えない紙が届きます」 —
`03_SCRIPTS/29_shikaku-kakuninsho-8gatsu-85sai.md` + `_TTS.md`. **check_pace ĐẠT HẾT 23/23**,
**15:05**, trụ **②**, khuôn mở **④対決型**, 計算タイム **○×クイズ**, closer **セルフチェック3問**.
Cast **原田(84)・小川(84) MỚI** + 小林(75) callback v28. Slot: **T5 24/9 19:00**.

**Cú lật trung tâm (chỗ trống của ngách):** 令和8年8月1日 chế độ đổi — tới 7月末 thì **mọi**
後期高齢者 được cấp 資格確認書 một cách vô điều kiện; từ 8月1日 thì không. Ranh giới là
**85 tuổi TÍNH ĐẾN 8月1日** (sinh nhật 85 từ 8月2日 trở đi thì **không** được cấp vì lý do tuổi),
và với 84歳以下 là **過去12か月に6回以上 + 直近3か月に実績**. ⇒ Nghịch lý bán được: **người đi khám
NHIỀU lại nhận tờ không dùng được một mình.**
📌 **3 hàng xóm (843K · 715K · 859K) đều đăng 2025年10–11月**, tức nói về đợt chuyển TRƯỚC —
mốc 令和8年8月1日 **chưa kênh lớn nào làm lại**.

🔴 **Đã cắt khỏi queue:** mục `マイナンバーカード×年金/保険証` ở bảng QUEUE 24–30 → **XONG**.

🔴 **Hai thứ đề này để lại, đừng làm mất:**
- **Bảng 自己負担限度額（円）** cố ý KHÔNG đọc: 高額療養費 vừa sửa từ 令和8年8月, **2 đợt (8/2026 và
  8/2027) + 年間上限 mới** ⇒ số đang trôi. Khi đợt 2 chốt xong (sau 8/2027) thì đây là **một video
  riêng**, không phải phần bù của v29.
- **利用登録解除** (bỏ đăng ký マイナ保険証) mới chỉ nêu một dòng trong FACT SHEET, chưa vào script.

⚠️ **Điểm yếu biết trước:** ① quy tắc 85歳/6回 đo ở **2 広域連合 + 厚労省方針** nhưng vận hành khác
theo tỉnh ⇒ mọi chỗ nêu số đều phải hedge ② cast vào **4:50**, không phải ~3:10 như thiết kế (cold
open + chương 1–2 dài hơn dự tính) — vẫn sớm hơn v28 (6:10) 1,3 phút.

### ⭐⭐ VIDEO 30 — ĐÃ VIẾT 2026-09-24 (user chọn 支給日直前チェック 10/15 giữa 3 phương án)

**Đề:** 「年金、10月15日の振込が8月と違う人がいます｜介護保険料の紙で分かります」 —
`03_SCRIPTS/30_nenkin-furikomi-10gatsu-fueru-hito.md` + `_TTS.md`. **v2 (viết lại cùng ngày theo yêu cầu 9–10/10) —
check_pace ĐẠT HẾT 23/23**, ước 17:00 (render dự kiến ~15:30), trụ **③**, khuôn mở **①LOSS-REVEAL + khuôn ĐIỀU TRA** (3 nghi phạm → thủ phạm カレンダー; 3 loop trả ở 25%/69%/82%), 計算タイム **A-vs-B 明細 8月 vs 10月**, closer
**行動プラン3ステップ**. Cast **加藤(72・新潟市) MỚI** + 中村 callback v15. Slot: **T3 13/10 19:00** (rule 支給日).

**Hai phương án không chọn (đo 2026-09-24, `bench_topic.py`):** 加給年金→振替加算 (hàng xóm 306K/89K nhưng
T1 ~40% ⇒ chỉ ô 実験室) · ゆうちょ ô thử (cầu còn ~2.200 view/ngày nhưng trễ sóng 5+ tuần, nội dung đối thủ
「8月ルール変更」 không tìm được nguồn gốc ゆうちょ ⇒ YMYL cao). Rổ 「10月から変わる 年金」 median 101K nhưng
nội dung toàn 106万の壁/在職 ⇒ **bẫy v19**, không làm.

⭐ **Hai thứ mới đề này tìm ra, dùng lại được:**
- **令和8年度 みなし課税** (介護保険法施行令 sửa đổi, chỉ năm nay): lương 55万1千〜190万 năm 2025 ⇒ 住民税 非課税
  mà 介護保険料 vẫn tính như 課税. Chưa kênh lớn nào làm. Nếu v30 ăn view thì **farm riêng một bài** trước 3/2027
  (hết hiệu lực khi hết 令和8年度).
- 🔴 **Phía TĂNG có thể thành HOÀN TIỀN**: nếu 段階 giảm >50% thì 仮徴収 3 kỳ vượt cả 年額 ⇒ 本徴収 0 + 還付 (hoặc
  市区町村 hạ 8月 bằng 平準化). v30 **cố ý tránh** (case 加藤 giảm 34,9%) vì chưa verify thủ tục 還付. Đề tiềm năng:
  「介護保険料の還付のお知らせ」 — T2 mạnh (giấy tự đến, không làm thì mất sau 2 năm?) ⇒ **verify 時効 trước**.
- Tháng 10 NĂM SAU người như 加藤 lại bị trừ nhiều lên (仮徴収 năm sau = kỳ 2月 thấp) ⇒ đề farm tự nhiên cho 10/2027.

### ⭐⭐ VIDEO 31 — ĐÃ VIẾT 2026-09-26 (user chọn 扶養親族等申告書 domino giữa 3 phương án)

**Đề:** 「年金暮らしの方へ｜扶養親族等申告書、出さないと2年後に年15万円が消えることも」 —
`03_SCRIPTS/31_fuyo-shinkokusho-hikazei-domino.md` + `_TTS.md` (sinh bằng `make_tts.py`). **check_pace 22/23 — chỉ G18
đỏ (カバー率 40%, khai thật)**, **v2 viết lại cùng ngày (user đòi 9–10/10)**: mở bằng **cảnh 2 năm sau** (2 thư 介護保険料 + sổ tháng 12 thiếu 給付金), trục **住民税非課税世帯**, thêm nhánh **寡婦 135万**, PAYOFF 「損の7割は受け取っていない奥さま — 世帯」; ước 15:29, trụ **③(+②)**, khuôn mở **②事件型 (flash-forward)**, 計算タイム **timeline ドミノ年表 4札**, closer
**○×クイズ3問**. Cast **木村夫妻(大阪市) MỚI**. Slot đề xuất: **T3 29/9 19:00** (trễ nhất T5 1/10 — sóng hết cầu ~20/10).

**Bằng chứng chọn đề (bench 2026-09-26, 8 rổ):** `扶養親族等申告書 年金` — 完全攻略 **852K/15 ngày (56.820/ngày)** · スガワラ 1,36M ·
median 26.943 · 17 video ≥100K. Hai phương án không chọn: `住民税非課税世帯 給付金 2026` (median 186K nhưng trùng v14/v30 +
nhiều title giật tít YMYL) · 総集編 「届く紙」 (vẫn để dành).
⭐ **Phát hiện dùng lại được:** sơ đồ 年金機構 0617 — dải **148万〜214万「住民税のみ課税」** lần đầu thành 提出対象 ở 令和9年分;
đường 非課税 大阪市 **45万 ↔ 101万** theo số người trong hộ. ⚠️ **Chưa verify, đừng nói:** 令和8年分 không gửi cho 148–205万 thì
住民税 令和9年度 của họ được xử lý ra sao — đề tiềm năng nếu verify được.
🔴 **Phép thử T-GATE ngược chiều:** v31 rớt T1 nhưng cưỡi sóng. AVP browse ≥14,4% ⇒ T1 đo sai với đề hộ gia đình; ≤11,5% ⇒ T1 đúng.

## C.1 🔴 SỔ XOAY KHUÔN MỞ BÀI — và một khuôn vừa CHẾT

Khuôn 4 video gần nhất: **15 ②事件型 · 16 ②事件型 · 17 ②事件型 · 18 ③質問型**.
⇒ 19–23 phải tránh ③ (liền kề) và không quay lại ② quá sớm.

🔴 **⑤物語型 ĐÃ CHẾT — không dùng được nữa.** Định nghĩa của nó là *"kể chuyện một モニター
TRƯỚC, số liệu sau"*, mà luật cold open v3 (`CLAUDE.md` §③, chốt 2026-08-30) cấm モニター kể
chuyện trong **0–120s**. Hai thứ loại trừ nhau. ⇒ Sổ khuôn thực dụng còn **4**, không phải 5:
**①GAIN/LOSS-REVEAL · ②事件型 · ③質問型 · ④対決型**.
📌 Đây là hệ quả chưa ai ghi ra khi chốt cold open v3 — ghi vào đây để lần sau không mở sổ 5
khuôn rồi chọn nhầm cái đã chết.

| # | Khuôn mở | Khuôn 計算タイム | Cast chính |
|---|---|---|---|
| 19 | **④対決型** (継続給付 ↔ 繰上げ, hai thứ triệt tiêu nhau) | A-vs-B đối chiếu 明細 | 松本 (nối 18) |
| 20 | **①LOSS-REVEAL** (số tưởng ↔ số thật) | thang 3 bậc | 佐藤 (goá, 仙台) · 中村 |
| 21 | **②事件型** (giấy đến / không đến) | ○×クイズ | 高橋 · 田中 |
| 22 | **④対決型** (gia đình xin ↔ không xin) | tính ngược | 中村 · 佐藤 |
| 23 | **③質問型** (cách 18 đủ 5 bài) | timeline | 渡辺 · 伊藤 |

## D. ĐỔI TRONG QUY TRÌNH VIẾT (áp từ video 19)

1. 🆕 **Script phải có heading `### HÀNG XÓM MỤC TIÊU`** (`youtube-suggested-growth.md` §1) — ghi
   1–3 video hàng xóm + lý do mình là next-watch của nó. Lấy từ bảng C, hoặc chạy lại
   `python 06_VIDEO/_diagnose/pull_related.py` cho số mới.
2. 🆕 **Gate nhịp hình** (`audience-45plus.md` §2.0): **≥ tổng_giây/7 sự kiện hình** ⇒ 15′ cần ≥132.
   Builder đã tự chạy `check_frame_pace.py`. ⇒ Lúc chốt `SCENES` phải nhắm **≥1–2 sticker/punch mỗi
   scene**, scene ≥30s cần 3–4. **Ước số sticker cần gen NGAY Ở BƯỚC NÀY**, đừng để tới lúc builder.
3. **Cold open v3 giữ nguyên** (`CLAUDE.md` §③): 0–120s không có モニター kể chuyện; あなた+円 →
   対象 → câu lộ trình → open-loop → 「まず、事実から」; ≤2 tag trong 75s đầu.
4. **Title:** keyword đo được đứng ĐẦU (`youtube-upload-seo.md` §0.5), ⛔ không lặp tag 【】 chung chung.
5. **Voice+timeline:** `make_timeline_exact.py` (⛔ không dùng cặp tool cũ — bẫy trôi 8,6s).

## E. ĐO LẠI — thước đo của plan này KHÔNG phải view

📅 **2026-09-05** và mỗi 2 tuần: `python 06_VIDEO/_diagnose/pull_related.py`
→ **tỉ lệ video dẫn CÙNG NGÁCH** phải tăng từ mốc **8/25 (2026-08-30)**.
Đó là thước "YouTube đã hiểu chủ đề chưa". View/sub là hệ quả đến sau, và ở cỡ mẫu hiện tại thì
view **không đọc được**.

⚠️ Cùng lúc: **AVD ≥3:50 · awr@120s ≥0,40** (`08_ANALYTICS_LOG.md`). Nhưng **v18 lẫn hai biến**
(cold open v3 + mật độ hình tụt) ⇒ phép đo cold open sạch phải đợi **video 19**.

---

## ĐÃ LÀM (map vào 3 trụ — cập nhật **2026-08-10**)

> 🔴 **CẢNH BÁO TRỤ:** 07 → 08 → 09 → 10 đều **trụ ②**, bốn video liên tiếp. Luật xoay trụ đã bị lệch
> **có chủ ý** (lý do trong header script 10: lớp A+C là chỗ duy nhất có cầu đo được, và kênh mới 19
> view thì đa dạng trụ chưa phải nút thắt). **Nợ: video 11 BẮT BUỘC trụ ③.**
> ⭐ **Độ dài chuẩn đã đổi 25–30′ → 13–17′** (user chốt 2026-08-10, `CLAUDE.md` §ĐỘ DÀI) — nên đừng
> lấy 30′49 của video 06 hay 28′ của video 08 làm mẫu cho bài mới nữa.
| # | Chủ đề | Trụ | Khuôn / hook |
|---|---|---|---|
| 01 | 在職老齢年金 2026改正 (65万円の壁) | ① 年金 | GAIN-REVEAL · thang ngưỡng · quiz — ✅ LIVE 07-22 |
| 02 | 繰り下げ受給 65 vs 70 (損益分岐点) | ① 年金 | 対決型 · timeline · セルフチェック — ✅ LIVE 07-22 |
| 03 | 子どもに頼らない自立 (年金だけで暮らす) | ① 年金 | LOSS-REVEAL · 逆算 — ✅ **ĐÃ MỔ TRỤ 07-25** (bỏ NISA/iDeCo → レバー3 = もらい忘れ + 第4章 = 退職金その場で決めない; ~6.100 ký ≈ 16–18′). Còn: rà FACT SHEET → TTS/SLIDES → render. ⚠️ **cần chèn vào slot T5 06/08 hoặc CN 09/08** để không có 3 video liền nhau cùng trụ ② (07 → 03 → 08) |
| 04 | 年金生活者支援給付金 (申請しないと消える) | ② 給付金 | 事件型 · 累計損 — ✅ LIVE 07-25 19:00 |
| 05 | 60歳で即退職は危険 (空白5年+継続給付+税) | ①+③ | 物語型 · A-vs-B · ○×クイズ — 📦 ĐÃ GÓI, slot **T2 27/07 19:00** |
| 06 | 加給年金 年42万円 (配偶者が年下・届出しないと消える) | ② 給付金 | **質問型 · 年の差早見表 · カレンダーに丸** — ✅ **LIVE 07-31 19:00** (30′49, video đầu đúng chuẩn độ dài ngách) · ~~✍️ SCRIPT XONG 2026-07-30~~ (9.691 ký ≈ 26′20, FACT SHEET verify 13 mục, trend đo 30d: 加給年金 ≈11 điểm). ⚠️ Fact #10 (2028年4月 1割減) vẫn CHƯA verify được bằng nguồn 厚労省 (PDF ảnh, máy không đọc) — nếu video sau nhắc lại con số này thì phải rà trước |
| 07 | 特別支給の老齢厚生年金 (5年で消える) | ② 給付金 | 事件型(deadline) · timeline 時効 · セルフチェック3問 — ✅ LIVE 08-04 19:00 |
| 09 | 公金受取口座 意向確認書 (45日ルール) | ② 給付金 | **事件型(封筒) · セルフチェック該当表＋○× · 研究ノート5行** — ✅ ĐÃ GÓI + UPLOAD 2026-08-10, **publishAt 08-11 19:00**. Video đầu chạy lớp hình「sân khấu」. ⚠️ Đề tài đã có 1,4M+1,0M+45K+550K trong 6–21 ngày trước đó → **số của nó không đọc được như phép thử khuôn** |
| **10** | **9月に届く緑の封筒 (年金生活者支援給付金 はがき型 ＋ ふたつの期限)** | ② 給付金 | ⭐ **③質問型 · 3段の閾値 · シェアノート** — ✍️ **SCRIPT + TTS + SLIDES XONG 2026-08-10**, đo **16:06** (video đầu theo chuẩn 13–17′), slot đề xuất **CN 08-16 19:00**. Cast: **渡辺 (MỚI)** + 伊藤. Cú lật: người KHÔNG nhận được phong bì mới nguy hiểm. Chờ **4 ảnh AI** + render |
| 11 | 扶養親族等申告書が届かない人 (queue N3) | **③ 税** | ⚠️ **BẮT BUỘC trụ ③** để trả nợ xoay trụ; giữ lời hứa đích danh của video 09. Nằm nhánh **A-CHẾT** (`02b` §cập nhật 08-10) → không kỳ vọng mở vòi |
| 08 | 【8月14日の年金支給日】通知書の6欄・仮徴収と本徴収 (支給日回 #1) | ② 給付金 | **矛盾型 · 引き算の階段 · 穴埋め年間手取り表** — ✅ **LIVE 08-06 19:00** (28′13). ⤵ ghi chú cũ: ✍️ SCRIPT + TTS XONG 2026-08-05, slot **T3 11/08** (thực tế lên sớm 08-06). Chi tiết ở bảng GĐ A #09 dưới |

---

## 📅 ROADMAP 90 NGÀY (2026-07-25 → 10-23) — **v2, TÁI XẾP sau benchmark 07-25: "VÒNG SƯỜN, KHÔNG ĐÁNH TRỰC DIỆN"**

> ⚠️ **NHỊP + NGÀY ĐÃ ĐỔI 2026-07-28, roadmap dưới CHƯA xếp lại theo lịch mới** (`CLAUDE.md` §Lịch đăng + `CHANNEL_DIAGNOSIS_2026-07-28.md`): giờ là **T6 19:00 — 1 video/tuần**, T3 chỉ là slot phụ cho 支給日/tin chính sách nóng. Cột "Slot" trong bảng dưới là **thứ tự ưu tiên**, không còn là ngày thật — lấy ngày thật từ `upload_pack.py`. Độ dài chuẩn cũng nâng lên **25–30′** (`.claude/rules/audience-45plus.md` §4).
>
> ~~**2 video/tuần T2·T4 19:00 JST** (~26 video/90 ngày)~~ + 支給日 đè lịch. Xoay trụ ①→②→③, 2 video liền nhau không trùng trụ/khuôn; ⭐ = kỳ franchise. Mỗi video: đo trend 30d + FACT SHEET verify + **≥2 原典ショット** + 2 bản thumbnail.
>
> **⚠️ ĐỔI CHIẾN LƯỢC XẾP HÀNG (căn cứ `CHANNEL_BENCHMARK_2026-07-25.md`):** bản v1 định front-load 7 mega-topic proven. Nhưng đo ra: **完全攻略 lập 2026-03 (mới 4,1 tháng), 132K sub, và video 定期便に載らない 3,79M của nó là video MỚI đang khỏe.** Các mega-evergreen khác cũng bị video 1–2,5M của kênh 130–550K chiếm. Kênh 0 sub đánh trực diện query đó = chọn chỗ phòng ngự dày nhất.
> → **Nguyên tắc mới:** GĐ A đi bằng **long-tail SÂU + nhịp chưa ai chiếm (支給日/書類が届く月)** — nơi không có video 400K+ nào. Mega-evergreen (定期便に載らない / 何歳受給の末路 / いくらもらえる保存版) **lùi về GĐ C**, làm khi kênh đã có uy tín + có 原典 làm điểm khác biệt để đối đầu.
> **3 lợi thế thật của kênh 0 sub khi chọn long-tail:** ① 1 video 20′ chỉ về 加給年金 đào sâu gấp 10 lần đoạn 2 phút trong video tổng hợp của đối thủ ② query hẹp → cạnh tranh thấp, dễ có impressions đầu tiên ③ đúng chất 研究室 (nghiên cứu 1 chế độ đến cùng) → củng cố định vị thay vì pha loãng.

### GĐ A — tuần 1–5 (27/07–28/08): long-tail sâu + chiếm nhịp 支給日/書類 (10 video)
| # | Slot | Title working (JP) | Trụ | Cast | Vì sao chọn (chỗ trống) |
|---|---|---|---|---|---|
| 05 | T2 27/07 | (đã gói) 60歳の即退職で老後資金が約700万円減るワケ | ①+③ | 松本 | đã render, đi luôn |
| 06 | ~~T4 29/07~~ → **T6 07/08** | ✅ **VIẾT XONG** → 【年42万円】加給年金は届出しないと1円も入りません｜配偶者が年下の方へ | ② | 高橋 (chính) · 田中 (支給停止) · 山田夫妻 (振替加算) · 伊藤 (対象外, callback #04) | **long-tail giá trị cao**: 年42万 cụ thể, đối thủ chỉ nhắc 1–2 phút trong video tổng hợp. ⚠️ số 2026年度 **ĐÃ verify 2026-07-30** = 243,800 + 特別加算179,900 = **423,700円** (令和8年4月から). Script: `03_SCRIPTS/06_kakyu-nenkin-haiguusha-42man.md` |
| 07 | ~~T2 03/08~~ → **T5 07/08** | ✅ **VIẾT XONG 2026-08-03** → 【5年で消える年金】特別支給の老齢厚生年金｜女性は昭和41年4月1日以前生まれが対象 | ② | 佐藤 (chính) · 山田妻 (còn kịp) · 高橋妻 (ngoài diện) | **8.614 ký ≈ 27′** · FACT SHEET verify 13 mục (年金機構 + 厚労省) · 3 原典ショット. ⚠️ **Bảng năm sinh nữ đã verify tận nguồn 厚労省** — search AI trả SAI (gán mốc nam cho nữ), đừng tin snippet. ⚠️ Trùng trụ ② với 06 → chèn script 03 (trụ ①) vào T3 05/08. Còn: TTS/SLIDES + quay lớp thủ công. Script: `03_SCRIPTS/07_tokubetsu-shikyu-rourei-kosei-nenkin.md` |
| 08 | T4 05/08 | (03 đã mổ) 子どもに頼らず年金で自立する逆算 | ① 物語 | 佐藤・田中 | script sẵn, đổi nhịp |
| 09 | ~~T2 10/08~~ → **T3 11/08** | ⭐**支給日回 #1** ✅ **VIẾT XONG 2026-08-05** → 【8月14日の年金支給日】手取りが10月から1万2千円減る人｜通知書のどこを見るか | ② | **田中 (chính, lần đầu đóng chính)** · 高橋 (初振込, franchise) · 伊藤 (大判はがき, callback #04) | **nhịp CHƯA AI CHIẾM** — đăng 3 ngày trước 支給日 **14/08(金)**. Mở series 書類を読む + 3 nguồn 原典/4 lần chiếu. **8.576 ký ≈ 27′38** · FACT SHEET verify **22 mục** (年金機構/総務省/自治体) · `_TTS.md` đã sinh (30 tag, 0 tag giữa câu). ⚠️ **2 việc:** ① cast đổi từ 鈴木 → 田中 (鈴木 chưa từng có case tiền cụ thể, 田中 mới là người ở đúng chu kỳ 仮徴収→本徴収) ② **title working của roadmap DẪN BẰNG TỪ CHẾT** — đo 05/08: `年金振込通知書` **0 điểm** · `年金額改定通知書` **0 điểm** trên YouTube Search 30d → keyword dẫn đổi sang `年金支給日` **28** + `年金 手取り` **21**; 2 từ kia chỉ giữ ở tag/概要欄. Script: `03_SCRIPTS/08_nenkin-shikyubi-8gatsu14ka-tedori.md` |
| 10 | T4 12/08 | 【定年退職者必見】任意継続 vs 国民健康保険｜選び方で年○万円の差 | ③ | 松本 | continuity từ 05; trụ ③ ít bị mega-video chiếm |
| 11 | T2 17/08 | 【65歳の落とし穴】介護保険料が突然2倍になる仕組み | ③ | 高橋 (vừa 65, nhận giấy đầu) | cụm "phí sau nghỉ hưu", query hẹp. 🔴 **TRÙNG với script 08 — phải đổi góc trước khi viết:** 08 đã giải thích trọn **仮徴収→本徴収 (= chính cái "đột nhiên gấp đôi")** + 「65歳になったばかりは普通徴収」. Góc CÒN TRỐNG cho #11: **保険料が決まる仕組み** (段階別保険料・所得段階・自治体差 = tại sao nhà mình đắt hơn nhà bên) và **減免/猶予の申請**, KHÔNG phải nhịp thu tiền |
| 12 | T4 19/08 | 【遺族も申請を】未支給年金｜亡くなった月の分は請求しないと消える | ② | 山田夫妻 | long-tail, gần như không kênh nào làm riêng |
| 13 | T2 24/08 | 【被害急増】日本年金機構をかたる詐欺の手口と見分け方 | ② | 佐藤 | trust-builder + 原典ショット (trang cảnh báo 年金機構) |
| 14 | T4 26/08 | 【知らないと大損】住民税非課税世帯の"境目"｜1万円差で年○○万円 | ③↔② | 伊藤 | ranh giới cụ thể, trụ ③ |

→ **CHECKPOINT #1 (cuối T8, ~14 video):** đọc `08_ANALYTICS_LOG` — có impressions chưa? CTR? Video nào lọt rổ nào? Chưa pivot, chỉ đọc.

### GĐ B — tuần 6–9 (31/08–25/09): seasonal T9 + reform hậu-2026 + mở 実験室 (8 video)
- ⭐**seasonal** 【9月に届く】扶養親族等申告書を出し忘れると手取りが減る (③ · 高橋 · **đăng tuần đầu T9** — giấy về nhà đúng lúc; recurring hàng năm; 原典ショット = mẫu 申告書)
- ~~額面と手取りは別物｜年金から天引きされるお金をぜんぶ計算~~ 🔴 **ĐÃ BỊ SCRIPT 08 ĂN TRỌN — BỎ hoặc đổi hẳn đề.** 08 làm đúng việc này (6 欄 + 引き算の階段 + 高橋 lần chuyển khoản đầu). Làm lại = video trùng lặp. Nếu vẫn muốn 1 tập về 手取り thì đổi sang góc chưa có: **確定申告で戻るお金** (源泉徴収票の読み方・還付になる人) — đó là mảnh 08 KHÔNG chạm
- 【2028年改正】遺族厚生年金が変わる｜配偶者が亡くなった後の年金 (① · 山田夫妻+佐藤 · **reform mốc SAU — đối thủ chưa cày** · ⚠️ rà kỹ luật)
- 【税金の罠】退職金は一時金と年金どっちで受け取る？手取り差○○万円 (③ · 鈴木 · +750% · callback teaser script 03)
- 【パート必見】社会保険の適用拡大｜週20時間で年金はいくら増える？ (①+③ · 佐藤+山田妻 · reform · ⚠️ verify mốc hiệu lực)
- 国民年金だけで暮らせる？満額でも月約6.9万円のリアル＋付加年金の裏技 (① · 伊藤 · ⚠️ verify 満額 2026)
- ⭐**視聴者の実験室 #1** (xuyên trụ — comment chưa đủ → bản FAQ, ẩn danh + ghi rõ nguồn câu hỏi)
- 【65歳以上も対象】高年齢求職者給付金｜退職後にもらえる"失業手当" (② · 田中 · backlog trống)

### GĐ C — tuần 9–13 (21/09–23/10): 支給日 T10 + reform + đào sâu
- 【65歳以上も対象】高年齢求職者給付金｜退職後にもらえる"失業手当" (② · 田中 kịch bản "nếu nghỉ")
- 【2026年改正】基礎年金の底上げで誰がいくら増える？ (① · 伊藤 hưởng lợi nhất · reform · ⚠️ verify trạng thái luật)
- ⭐**支給日回 #2** 【10月15日振込前に】金額が変わる人の直前チェック (② · 鈴木 · đăng 13–14/10)
- 熟年離婚と年金分割｜「半分もらえる」は誤解です (① · nhân vật MỚI — không gán ly hôn cho cast chính; chỉ 制度)
- 【高収入ほど注意】標準報酬月額の上限引き上げ (③ · 鈴木・高橋 · reform · ⚠️ verify mốc hiệu lực)
- 【高額療養費】医療費が月○万円を超えたら戻ってくるお金 (③ · 山田夫妻 · CHỈ mặt tiền, không nói bệnh)
- 物価高で年金は実質目減り？マクロ経済スライドを計算する (①+③ · 佐藤 · ⚠️ đo trend trước)
- ⭐視聴者の実験室 #2 + teaser 年末調整×働く年金受給者 (chuẩn bị mùa T11)

#### 🎯 MEGA-EVERGREEN — mở khóa ở GĐ C (khi đã ~20 video + có uy tín + 原典 làm vũ khí)
> Đây là các query bị video 1–3,8M của kênh 130–550K chiếm (xem benchmark). Đánh khi kênh đã có baseline CTR/retention riêng + đủ nội lực làm bản SÂU HƠN + 原典ショット dày. Đánh sớm = thua trắng; đánh đúng lúc = ăn được vì mình có thứ họ không có (tài liệu gốc trên màn hình + cast + 研究ノート).
- 【申請しないと消える】ねんきん定期便に"載らない"年金 — **bản 原典**: chiếu đúng tờ 定期便, khoanh đỏ chỗ KHÔNG in ra (đối thủ 完全攻略 3,79M chỉ nói miệng). Đồng thời là tập trục của series 書類を読む.
- 誕生月に届く「ねんきん定期便」完全ガイド｜50歳からは見方が変わる (② · 田中 · evergreen quanh năm — cặp với bản trên)
- 【4人の末路】年金は60・65・70・75歳、何歳から受け取るのが正解か (① · 高橋+佐藤 · phải có bản tính 手取り sau thuế/phí mới hơn được đối thủ)
- あなたの年金はいくら？職業・加入年数別に自分で計算【保存版】 (① · cả dàn cast · funnel to nhất — làm khi đã có comment để gieo 実験室)
- 【一生−24%】60歳から繰り上げた人の生涯損失 (① · 松本 · đóng open-loop 松本)
- 高齢者世帯の平均貯蓄額｜あなたの位置は？【総務省家計調査】 (① · cả dàn cast)
- 【総まとめ】60代がやり忘れる手続き○選 (② listicle hub — làm CUỐI, link mọi video trước → tăng session time)

## ⭐ 6 SERIES/FRANCHISE (máy tạo return-viewer — nâng từ "rule" thành series có tên)
1. **⭐支給日直前チェック** (6 kỳ/năm, 13–14 mỗi tháng chẵn — kế: **14/08, 15/10, 15/12**): 「○月15日の振込前に確認する3つの数字」. Franchise MẠNH NHẤT — gắn vào nghi thức đời thực "ngày tiền về"; chưa đối thủ nào định kỳ hóa. Thumbnail template riêng.
2. **視聴者の実験室** (tháng 1 kỳ từ GĐ B): comment → tính hộ ẩn danh → 「皆さまの声が、次の研究テーマになります」. Moat cộng đồng, đối thủ không copy nổi.
3. **書類を読む研究** (giấy tờ về nhà = content calendar tự nhiên): 定期便 (sinh nhật — evergreen) → 振込・額改定通知書 (T6/T10/T12) → 扶養親族等申告書 (T9) → 源泉徴収票 (T1) → thân phận kênh = "nơi mang giấy tờ đến hỏi".
4. **改正カレンダー annual** (T12: 「2027年からこう変わる」+ mỗi mốc 4月/10月): nơi DUY NHẤT được nhắc iDeCo — 1 slide điểm tin + câu 「当研究室は投資のご相談は扱いません」.
5. **モニター続きドラマ**: cast tiến triển có cốt truyện (松本の決断 → đóng ở #15 · 高橋の初振込 → 額面vs手取り · 伊藤の給付金その後) + end-screen 「前回の研究」 trỏ chéo tập + **hẹn tập ĐÍCH DANH cuối video** (cấm 「来週もお届けします」 mơ hồ).
6. **研究ノート share**: cuối video thêm 「このノートをスクショして、ご家族に送ってあげてください」 — cơ chế share organic sạch YMYL.
7. ⭐ **原典を見せる** (thêm 2026-07-25 — MÓC NHẬN DIỆN SỐ 1, xuyên mọi video): ≥2 shot chiếu tài liệu gốc 年金機構/厚労省 + khoanh đỏ con số đang đọc, shot đầu trong 3 phút đầu. Đây là lớp bù cho việc mình KHÔNG có móc uy tín kiểu 元ハロワ職員 (không được bịa tư cách) — và không đối thủ nào trong ngách làm. Quy trình: skill `script-nenkin` GĐ0d · visual: CLAUDE.md · thumbnail: khuôn G.

---

## 🟦 TRỤ ① — 年金いくら？何歳？ (TÍNH SỐ — funnel lõi)
> Cụ già lo nhất: "tôi được bao nhiêu, nhận lúc nào là hơn". Đây là cửa vào rộng nhất.

| Ưu tiên | Chủ đề (working title) | Số đắt + nhân vật | Hook | Bằng chứng |
|---|---|---|---|---|
| 🥇 | **年金はいくらもらえる？自分で計算する** | 逆算 theo nghề/số năm đóng · 佐藤/伊藤 | 質問型「あなたはいくら？」 | 年金いくらもらえる **+130%**; funnel to nhất ngách |
| 🥇 | **何歳から受給が正解｜60/65/70/75で受け取った人の"末路"** | 生涯総額 chênh 数百万 · 高橋/佐藤 | 対決/末路 (đâm sợ chọn sai) | 看護師 1.37M · News65 4人の末路 757K — evergreen TO NHẤT |
| 🥈 | **60歳で早くもらうと損？繰り上げの落とし穴** | −24% một đời = 生涯○○万円 · 佐藤 | 対決 (60 vs 65) | 年金 何歳から +110% · 63歳 +120% |
| 🥈 | **遺族年金はいくら？配偶者が亡くなったあと** | 手取り激変 · 山田夫妻 | 物語型 (emotional) | 遺族厚生年金 所得制限撤廃 bùng nổ (⚠️ reform mới, rà kỹ) |
| 🥉 | **高齢者世帯、みんないくら貯めてる？** | 平均貯蓄 vs 必要額 · so cả dàn cast | 比較 "nhà người ta" | 高齢者世帯 平均貯蓄額 bùng nổ (家計調査, rà số) |
| 🥉 | **国民年金だけで暮らせる？満額でいくら＋自営の備え** | 月6.5万 · 伊藤 (tự doanh) | 質問型 | 国民年金 満額 +90% |

## 🟩 TRỤ ② — 給付金・申請しないともらえないお金 (取り逃し防止)
> "Tiền có quyền nhận mà không biết nên mất trắng" — đúng chất 事件型, share mạnh.

| Ưu tiên | Chủ đề | Số đắt + nhân vật | Hook | Bằng chứng |
|---|---|---|---|---|
| ✅ | ~~年金生活者支援給付金~~ = **script 04** | 年6万7千 · 伊藤 | 事件 | 給付金 申請が必要 +3.650% |
| 🥇 | **申請しないともらえない｜定期便に"載らない"年金** | 取り逃し 生涯○○万 · 田中 | 事件型 (取り逃す) | 完全攻略 **3.79M** (top ngách) · 看護師 539K |
| 🥈 | **年金通知書の読み方｜額改定・振込通知でいくら変わる** | 手取り差 · 鈴木 | 質問 (seasonal, quanh 6/10/12月 gửi thông báo) | 完全攻略 1.05M+244K |
| 🥈 | **日本年金機構をかたる詐欺｜手口と見分け方** | bảo vệ (không tính tiền — đổi nhịp) | 事件型 (cảnh báo) | 差し押さえメール bùng nổ — trust-builder rotation |
| 🥉 | **各種申請もの総まとめ｜60代がやり忘れる手続き** | 累計取り逃し · dàn cast | listicle + 事件 | nối mạch 04 |

## 🟨 TRỤ ③ — 税・社会保険料で損しない (định vị an toàn YMYL nhất)
> Trục THUẾ/PHÍ — giải thích chế độ, KHÔNG tư vấn đầu tư → sạch YMYL. Cụ già bị đòn kép thuế+phí sau nghỉ hưu.

| Ưu tiên | Chủ đề | Số đắt + nhân vật | Hook | Bằng chứng |
|---|---|---|---|---|
| 🥇 | **定年後の健康保険｜任意継続 vs 国保 でいくら損する** | 年○万差 · 松本/高橋 | 対決 (A vs B) | 看護師 615K |
| 🥈 | **65歳から介護保険料が倍増？** | 月○円→○円 · 田中 | GAIN-REVEAL (của bạn vừa tăng) | 看護師 509K |
| 🥈 | **退職金の賢い受け取り方｜一時金 vs 年金、税金で損しない** | 税差 生涯○○万 · 鈴木 (có 退職金) | 対決 (税トラップ) | 退職一時金 税制 +750% |
| 🥉 | **住民税非課税世帯になる条件・裏技** | ranh giới ○万円 · 伊藤/常連 | 事件 (境目1万で激変) | News65 578K · 速報 140K (giao thoa trụ ②) |
| 🥉 | **年金にかかる税金｜"手取り"はいくら？源泉徴収の仕組み** | 額面 vs 手取り · 高橋 | GAIN-REVEAL | 物価高×年金 lo thường trực (⚠️ đo trước) |
| 🥉 | **物価高で年金の手取りはどう減る？マクロ経済スライド** | 実質目減り · 佐藤 | GAIN-REVEAL (mềm) | (⚠️ đo trước) |

## ⭐ SIGNATURE xuyên trụ (moat, làm khi comment đủ ca)
- **視聴者の実験室｜"私の年金いくら？"みなさんのケースを計算** — format-driven, kích hoạt vòng lặp cộng đồng. Làm định kỳ, ẩn danh hóa comment thật.

---

## ⛔ KHÔNG LÀM (cập nhật 2026-07-25 — bẫy trông ngon nhưng chết)
- ❌ **家を売るべきか / リバースモーゲージ** — sang 不動産, đã cắt (ngách akiya nhận).
- ❌ **iDeCo/NISA/bảo hiểm — KỂ CẢ đóng khung "tin cải cách" làm video riêng** — (a) thuật toán gom kênh vào cụm 投資 → hút sai audience + comment đòi tư vấn = vùng YMYL đỏ; (b) 1 video lệch trụ khi <20 video làm nhiễu tín hiệu phân loại. Ngoại lệ DUY NHẤT: 1 slide điểm tin trong 改正カレンダー + câu miễn trừ.
- ❌ **退職金で保険・投資を買うべきか** — chỉ được khung "税・落とし穴 khi rút" (đã có trong GĐ B), KHÔNG khuyên mua.
- ❌ **老後2000万円問題 làm luận đề video** — topic 2019 bão hòa + câu trả lời tất yếu trượt sang 資産運用. Chỉ dùng làm 1 câu hook.
- ❌ **生活保護 làm mồi thumbnail** — stigma + comment war; 住民税非課税 là phiên bản an toàn cùng nhu cầu.
- ❌ **Đào sâu 介護費用/介護生活** — ranh giới ngách (nenkin = tiền hưu CỦA MÌNH; kaigo = tiền chăm BỐ MẸ, ngách nằm chờ riêng). Kênh này CHỈ giữ **介護保険料** (phí trên giấy báo của chính mình — đã có GĐ A #13).
- ❌ **Đổi format 漫画/phỏng vấn phố/vlog/Shorts** vì thấy News65・梅子 đông view — khác pipeline; cầu lớn ≠ mình nên đổi format.
- ❌ **Video thuần tâm sự** — tối đa 1/5 video là 物語型 và vẫn phải có lõi 計算 (bài học script 03 v1).
- ❌ **Tên chính trị gia/đảng, 絶対/必ず, số bịa** — luật kênh + YMYL.
- ❌ **PIVOT vì 0 view ở tuần 1–3** — bẫy tâm lý LỚN NHẤT. Cold-start 0 impressions là bình thường; basket cần 10–20 video (benchmark 長生きの秘訣 flop 30 video/2 tháng trước khi nổ). KHÔNG pivot trước video 15–20.
- ❌ **Rời ngách vì "nhiều kênh lớn làm rồi"** (user hỏi 2026-07-25 — đã đo trả lời): ngách đang **MỞ RỘNG**, 3 kênh tăng nhanh nhất đều lập từ 2025-06 trở lại đây, kênh già nhất tăng chậm nhất. Đông = cầu đã proven + không ai độc quyền. Xem `CHANNEL_BENCHMARK_2026-07-25.md`.
- ❌ **Bịa móc uy tín kiểu 「元○○職員」/「社労士」** để đối lại 元ハロワ職員まゆみ — gian dối + vi phạm YMYL rule #5 (persona không xưng tư cách hành nghề). Lớp thay thế honest đã chốt: **原典を見せる**.
- ❌ **Cày volume để bù** — dữ liệu bác bỏ trực tiếp: 1.971 video → 87K sub (17,8K view/video) vs 12 video → 132K sub (490K view/video).
- ❌ **Chế độ 在職必須 (đòi người xem CÒN ĐI LÀM) vào slot chính** — thêm 2026-09-15 từ ca v19: 高年齢雇用継続給付 chỉ áp cho 60–64 đang đi làm, trong khi **74,9% khán giả là 65+** ⇒ **AVP 11,5%, bét kênh**, dù mọi gate script đều xanh. Nay đã thành gate máy **G18**. Kéo theo: **106万円の壁** và **退職金の受け取り方** rời slot chính. Bài học của chính nó: **sai ở tầng CHỌN ĐỀ TÀI thì không gate script nào bắt được** — phải có cổng riêng, xem §T-GATE.

## Xếp lịch & checkpoint
- **Nhịp: 2/tuần T2·T4 19:00 JST là TRẦN** (chốt 2026-07-25 sau benchmark: 3 kênh tăng nhanh nhất ngách đăng ≤1,3/tuần; 完全攻略 12 video → 132K vs 給付金チャンネル 1.971 video → 87K = chênh **27 lần view/video**). Volume là chiến lược THUA ở ngách này.
- **Gác chất lượng (đè lên lịch):** video không qua FACT SHEET verify + **≥2 原典ショット** + Retention Audit + 2 bản thumbnail → **BỎ SLOT**. **1 video xuất sắc hơn 2 video nhạt** — nếu tuần nào chỉ kịp 1 video đủ chuẩn thì ra 1, đó không phải thất bại.
- Xoay **trụ ①→②→③** — 2 video cạnh nhau không trùng trụ/khuôn (sổ khuôn ở header script). Mỗi lần chốt script → đo trend 30d + ghi bảng điểm vào file script.
- **Checkpoint #1 (~14 video, cuối T8):** đọc `08_ANALYTICS_LOG` — impressions có chưa, CTR bao nhiêu, rớt vào rổ nào. CHƯA pivot, chỉ đọc. **Checkpoint #2 (~20 video, cuối T9):** topic nào CTR/retention nổi trội → nhân bản góc nhìn (chiến thuật 完全攻略: ít video, đào sâu topic thắng) + **mở khóa cụm MEGA-EVERGREEN**. Hit rate kỳ vọng ~1/5.
- **Đo lại benchmark ngách mỗi 6–8 tuần** (`CHANNEL_BENCHMARK_2026-07-25.md` mục 5) — nhất là xem 完全攻略 có giữ 31,8K sub/tháng hay đó chỉ là hiệu ứng sóng cải cách 4 tháng đầu.
