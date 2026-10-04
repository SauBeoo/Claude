# 25 — 年金の天引きと手取り（通帳の額は、あなたの年金額ではない）

> Viết 2026-09-14. Lời đọc: `25_nenkin-tenbiki-tetori-6man2sen_TTS.md`
> (121 dòng · **4.762 ký thân đọc · voice THẬT 16:28** — lọt dải chuẩn 13–17′). **Bản v3 MỘT GIỌNG**
> (sửa 2026-09-14, xem §VÒNG SỬA v2 và §VÒNG SỬA v3). Bản cũ: `_TTS.md.bak_v1` (2 vai, hook cũ) ·
> `_TTS.md.bak_v2_2voice` (2 vai, hook mới).
> Trụ **③税・社会保険料 × ②給付金**. Nối thẳng teaser cuối video 23 (伊藤さん 68・福岡・国民年金だけ).
> Slot đề xuất: **T3 2026-09-15 hoặc T5 09-17, 19:00 JST** (bộ ngày B — `upload-schedule.md` §0.9).

## SỔ KHUÔN (chống inauthentic)
- 3 video liền trước: **22 ④対決型 · 23 ①LOSS-REVEAL · 24 ②事件型** → bài này **①LOSS-REVEAL biến thể 物証**
  (mở bằng VẬT — 年金の振込通知書 — chứ không bằng mệnh đề).
  ⚠️ **Ghi thẳng chỗ lệch sổ:** v23 cũng là ① ⇒ chỉ cách 1 video, sát hơn mức thường. Chấp nhận có chủ ý
  vì hai bản khác nhau ở **cơ chế mở**, không chỉ ở chữ: v23 mở bằng mệnh đề trừu tượng
  (「請求しないかぎり一円も振り込まれません」), v25 mở bằng **vật cầm được + con số của người xem ở giây 0**.
  Bản v1 của bài này dùng ③質問型 (「あなたの年金は、月いくらですか」) và đã bị BỎ — xem §VÒNG SỬA v2.
- 計算タイム: **TIMELINE 一年分** (6 lần chuyển khoản của một năm) — v19 A-vs-B · v23 tính ngược ·
  v24 thang 3 bậc ⇒ không trùng ✓. Khuôn này mới hoàn toàn với kênh, và nó **chính là lời hứa của
  teaser** (「一年分を、まるごと計算してみます」).
- Closer: **まるばつクイズ 3問** (v23 và v24 đều dùng セルフチェック3問 → phải xoay).
- Cold open **v4** (`08_ANALYTICS_LOG.md` 09-10 §G): 物証+STAKE@0:00 · あなた@0:02 → cú lật 0:29
  (「この三万三千円は、今日の本題ではありません」) → số lớn hơn 0:34 → lộ trình 1:00 → 「まず、事実から」 → persona 1:14.
- Franchise: **モニター続きドラマ** (伊藤 nối v04/v10/teaser v23) + **明細を一緒に読む** (年金振込通知書)
  + **原典を見せる** (4 shot).

## GATE MÁY — ✅ **PASS 21/21** (`python tools/check_pace.py 25_nenkin-tenbiki-tetori-6man2sen`)
cold open 1:13 · G9 伊藤 3:11 · 8 số/30s · CTA 49% · STAKE 0:00 · あなた 0:00 · G10 1 tag/75s ·
G11 lộ trình 1:00 · **G12s MỘT GIỌNG — câu tự hỏi 19,8% (24/121)** · G13 0 khối chay ·
G14 payoff 数字 31% / 答え 69% · G15 CTA đăng ký 96% + câu định vị 1 lần · G16 0 外来語/60s ·
**G17 10 dữ kiện ở ký 50–150 (5·3·7·3, 0 cửa sổ rỗng)** — điểm G17 **cao nhất mọi script của kênh**
(nhóm đạt cũ: v14=10 · v16=8). Tag: 18 nhấn nhá, 0 tag lệch dòng, 0 tag đứng dòng riêng, 0 chữ `方`.

> ⭐ **G17 là điểm đáng chú ý nhất của bài này.** Gate cài 2026-09-10; trên 21 script cũ **chỉ v08/v10/v14/v16
> đạt** — đúng nhóm awr@30s 0,70 (so 0,57 của nhóm rớt). Đây là **script ĐẦU TIÊN được viết SAU khi có
> gate**, và cold open được dựng NGƯỢC từ nó: đặt cụm số vào ký 50–150 trước, rồi mới viết câu quanh chúng.
> ⚠️ Nhưng đọc cho đúng: G17 là tương quan n=9, **không phải nhân quả đã chứng minh**, và biến trội đo được
> vẫn là **chất lượng traffic** (browse AVP 15% vs RELATED 27%). Đừng kỳ vọng một bài viết lật được đường cong.

## Đo keyword — Google Trends chế độ YouTube Search, JP, 30 ngày (2026-09-14, pytrends)

| keyword | YT 30d (mean) | web 12m | ghi chú |
|---|---|---|---|
| **年金** | **81,97** (nz 32/32) | 76,25 | ⭐ từ dẫn — đứng ĐẦU title, lên banner thumbnail |
| **給付金** | **14,81** (nz 32/32) | 28,32 | ⭐⭐ **lần đầu kênh đo được một từ THỨ HAI có volume thật** — v21/22/23 chỉ có `年金` khác 0. Phải vào title |
| 国民年金 | 2,03 (nz 18/32) | 8,83 | sống, volume nhỏ → dùng ở nửa sau title + tag |
| 住民税非課税 | 0,47 | 1,34 | chỉ tag |
| 年金生活者支援給付金 | 0,44 | 1,28 | chủ thể chương 3 nhưng gần 0 → đẩy xuống 概要欄 + tag |
| 高額療養費 | 0,34 | 2,79 | không dùng — đã cắt khỏi script, lý do ở FACT SHEET |
| 介護保険料 | 0,12 | 2,34 | tag + teaser tập sau |
| 国民年金 だけ · 老後 生活費 · 付加年金 · 年金 少ない · 申請しないともらえない | **0,00** | 0,00 | ⛔ chết trên YouTube search — **cấm vào title/slug** |

**Related (YouTube, 30d):** top `年金 生活`(100) · `年金 暮らし`(79) · `年金 受給`(46);
rising **`年金 いくらもらってますか`(16.800)** ⭐ · `2026年 給付金`(70) · `年金生活者支援給付金とは わかりやすく`(237.850).
⚠️ Không nhét từ đo cao mà không có trong video (`youtube-upload-seo.md` §0.5 mục 4).
📌 Rising query số 1 `年金 いくらもらってますか` từng được dùng làm câu mở ở bản v1 — **đã bỏ**: nó đúng
về SEO nhưng sai về retention (bắt người xem *làm việc* ở giây 0). Ý định đó nay nằm ở **thumbnail + title**,
còn giây 0 của lời đọc trả tiền ngay. Xem §VÒNG SỬA v2.

## HÀNG XÓM MỤC TIÊU (`youtube-suggested-growth.md` §1)

| video hàng xóm | vì sao mình là next-watch |
|---|---|
| **カメ先生のもらえるお金** — cụm 【◯◯の方へ】＋給付金 (lập 08/2026, 31 ngày → 4.770 sub / 597K view) | Họ trả lời 「もらえる」. Mình trả lời câu hỏi còn lại ngay sau đó: **「じゃあ実際に通帳に入るのはいくら？」** — cùng tệp, cùng cỡ kênh, khuôn title gần mình nhất ngách |
| **定年前後のお金の教室** — 年金生活の手取り (30 ngày → 2.790 sub / 552K view) | Cùng chủ đề 手取り nhưng chưa mổ **tờ giấy nội dung** (年金振込通知書). Mình cho xem đúng dòng đó |
| **フクロウの年金・給付金解説室** — farm 年金生活者支援給付金 | Họ nói 「5.620円もらえる」. Mình là bản có **công thức chính thức hai vế** và chỉ ra 免除の単価が2倍以上 — thứ chưa kênh nào trong rổ nói |

⚠️ Đối chiếu `insightTrafficSourceDetail` sau 7–10 ngày: có trúng 3 rail này không. Mốc hiện tại
**RELATED cùng ngách 8/25** (09-10), mục tiêu 12/25.

## FACT SHEET — verify 2026-09-14 trong phiên (⭐ = có 原典ショット)

| # | Fact | Số | Nguồn (đã mở, đã đọc) | 原典ショット |
|---|---|---|---|---|
| 1 ⭐ | 老齢基礎年金 満額 令和8年度 | **年 847.300円 / 月 70.608円** | 年金機構「令和8年4月分からの年金額等について」 | `genten_847300_nenkin.png` — khoanh đỏ dòng 月額 |
| 2 | 昭和31年4月1日以前生まれの満額 | 年 844.900円 / 月 70.408円 | 同上 ＋「老齢基礎年金の受給要件…年金額」 | dùng chung #1 |
| 3 | 改定率 令和8年度 | 基礎年金 **+1,9%**（厚生年金 +2,0%） | 同上 | — |
| 4 | 満額の分母 | **480か月**（40年） | 年金機構「老齢基礎年金の…年金額」計算式 | dùng chung #1 |
| 5 | 支給日 | 偶数月15日・2か月分ずつ・年6回 | 年金機構（đã verify ở v15/v23） | — |
| 6 ⭐ | 介護保険料の特別徴収 | **65歳以上 ＋ 年金の年間受給額 18万円以上** | 年金Q&A「年金からの介護保険料などの徴収」(更新 2025-09-01) | `genten_18man_tenbiki.png` |
| 7 ⭐ | 国保料の特別徴収 | 65歳以上75歳未満 ＋ 年18万円以上。**介護＋国保が年金額の1/2を超えると国保は特別徴収にならない** | 同上（nguyên văn） | dùng chung #6 |
| 8 ⭐ | 介護保険料 第1号 全国加重平均 基準額 | **月 6.225円**（第9期＝令和6〜8年度。第8期 6.014円） | 厚労省「第9期…第1号保険料及びサービス見込み量等について」 | `genten_6225_mhlw.png` |
| 9 ⭐ | 支援給付金 支給要件3つ | ①65歳以上で老齢基礎年金受給 ②世帯全員が市町村民税非課税 ③前年の年金収入＋その他所得の合計が基準以下 | 年金機構「老齢（補足的老齢）年金生活者支援給付金の概要」(更新 2026-04-01) | `genten_shienkyufu_youken.png` |
| 10 ⭐ | 所得基準額 令和8年度 | **809.000円以下**（昭31.4.2以後）/ 806.700円以下（昭31.4.1以前） | 同上 | dùng chung #9 |
| 11 ⭐ | 給付額の計算式（2 vế） | ①**5.620円**×納付済月数÷480 ②**11.768円**×免除月数÷480（昭31.4.1以前は 11.734円） | 同上 | `genten_keisanshiki.png` — khoanh cả hai vế |
| 12 | 補足的老齢…の範囲 | 809.000円超〜**909.000円以下**（昭31.4.1以前は 806.700超〜906.700） | 同上 | dùng chung #9 |
| 13 | 給付基準額の改定率 | **+3,2%**（令和7→8年度） | 年金機構「令和8年4月分からの年金額等について」 | — |

### ② Số TỰ TÍNH của case 伊藤さん — công thức mở, kiểm được
Ràng buộc: hồ sơ cast khóa 伊藤 = **68歳・福岡市・単身・国民年金のみ・年およそ78万円 / 月6,5万**
(`_archive/CLAUDE_FULL_2026-08-24.md` §SIGNATURE). Bài này **không đổi số đời nhân vật** — chỉ mở ra
cấu trúc record để con số cũ lần đầu được giải thích:

| mục | công thức | kết quả |
|---|---|---|
| 記録 | 納付済 **420月** ＋ 全額免除 **48月** | — |
| 年金額 | 847.300 × (420 + 48×1/2) ÷ 480 = 847.300 × 444 ÷ 480 | **783.752円 ≈ 年78万3千円 / 月6万5千円** ✅ khớp hồ sơ cũ |
| 支援給付金 ① | 5.620 × 420 ÷ 480 | 4.918円/月 |
| 支援給付金 ② | 11.768 × 48 ÷ 480 | 1.177円/月 |
| 給付金 合計 | 4.918 ＋ 1.177 | **6.095円/月 → 年 73.140円** |
| 単価 đối chiếu | 5.620÷480 = 11,71円 · 11.768÷480 = **24,52円** | **免除の月 = 2,09倍** ⭐ payoff của bài |
| 所得判定 | 年金 783.752 ＋ 事業所得 20.000 = 803.752 vs 基準 809.000 | còn **5.248円** — sát mép, đúng arc v10 (từng bị cắt rồi phải tự xin lại) |

### ③ Số BALLPARK phụ thuộc 自治体 — đã hedge TRONG THOẠI (bắt buộc)
| mục | dùng trong bài | câu hedge trong lời đọc |
|---|---|---|
| 介護保険料 3.600円/回 ＋ 国保 1.900円/回 → **天引き 5.500円/回 = 年33.000円** | số hero thứ nhất | 「段階の刻みも、金額も、市区町村ごとに違います。全国平均は、あくまで目安です。ご自分の額は、お手元の通知書でお確かめください。」 |
| 手取り 年約75万円 / 月6万2千円 → ＋給付金 = 年82万3千円 / 月6万8千円 | số hero thứ hai | 同上 ＋「判定の細かい取り扱いは、お一人おひとりの記録で変わります。必ず年金事務所でお確かめください。」 |

⚠️ **Mục ĐÃ CẮT có chủ ý — 高額療養費.** Trang 厚労省 ghi 「令和8年8月診療分から」 và bảng
自己負担限度額 nằm trong **ẢNH**, máy không đọc được ⇒ **không verify được con số** ⇒ theo luật YMYL #2
thì không được đưa vào. Để dành thành video riêng khi có bản PDF đọc được.

## 原典ショット (5 khoá → 11 thẻ — GĐ0d đòi ≥2, shot đầu phải trong 3 phút đầu)
✅ **ĐÃ CHỤP + DỰNG XONG 2026-09-14 — 11 thẻ** → `remotion-vox/public/projects/nenkin-25/assets/`
Raw: `06_VIDEO/25_.../genten_raw/` · tool: `tools/make_genten_25.py` (gate tại chỗ **11/11 OK**).

| # | khoá | scene | dài | thẻ | vòng khoanh đỏ |
|---|---|---|---|---|---|
| ① | `nenkin_mangaku` | 14 (**1:46** ✓ trong 3 phút đầu) | 8,5s | 2 | **847,300円** |
| ② | `nenkin_tenbiki` | 44 (5:31) | 7,8s | 2 | đoạn 介護保険料 「65歳以上…18万円以上の方」 |
| ③ | `mhlw_kaigo` | 56 (7:10) | **14,0s** | **3** | không khoanh → nửa 第9期 → **6,225円** |
| ④ | `shienkyufu_youken` | 63 (8:31) | 9,3s | 2 | 3 điều kiện đánh số |
| ⑤ | `shienkyufu_keisan` | 70 (9:36) | 5,1s | 2 | 2 dòng công thức (**5,620円** và **11,768円**) |

**Vì sao ≥2 thẻ/khoá:** gate ② của `check_frame_pace.py` chặn khe đứng yên >9s. Chuỗi tiết lộ làm
bằng cách **đổi CHỖ KHOANH**, giữ nguyên khung ⇒ **không zoom, không mất nét**.

🔧 **Cách chụp (bước 6.7):** `chrome-headless-shell` của Remotion, `--window-size=2400,N`
(chữ to cho tệp 45+). Thẻ ③ là **PDF** ⇒ render bằng PyMuPDF @3,2× (2722×3849).
Upscale tất cả **≤1,60×** (đo được: 0,90× / 1,15× / 1,50× / 1,57× / 1,60×).

⚠️ **Hai lỗi tự bắt khi soi 1:1, đã sửa — đúng bài học "SNAP hộp vào ranh giới dòng chữ thật":**
mép dưới crop của ④ và ⑤ **cắt ngang dòng chữ kế tiếp** (hộp khoanh thì trúng, nhưng khung thì
cụt nửa chữ). Đã dời mốc cắt vào **khe trắng giữa hai dòng** (⑤ 1300→1252 · ④ 840→831 · ② 990→978).
📌 Sheet thu nhỏ **không** thấy lỗi này — chỉ lộ khi mở thẻ 1:1.


## VÒNG SỬA v2 (2026-09-14) — viết lại 30 giây đầu + bơm chất người cho cast

> user: *"kịch bản phải có hồn, lôi cuốn, gây tò mò, 30s đầu phải thật ấn tượng, nội dung không được rời rạc"*.
> Bản v1 **đạt 21/21 gate** nhưng đó chính là bài học `humanize-script-voice.md` §0: **gate đo CẤU TRÚC,
> không đo SỨC HÚT**. Tự chấm v1: **6/10**. Bản v1 giữ ở `_TTS.md.bak_v1` để còn đối chiếu.

### Sáu lỗi của v1 và cách chữa

| # | lỗi v1 | vì sao chết | chữa ở v2 |
|---|---|---|---|
| 1 | Câu 1 là **câu hỏi khảo sát** 「年金は月いくらですか」 | Bắt người xem *làm việc* (nhớ số) ở giây 0, trước khi trả cho họ thứ gì | Mở bằng **VẬT + tiền của họ**: 「年金の振込通知書。ここに、あなたが一年で引かれた三万三千円が書いてあります。」 |
| 2 | Cú lật đắt nhất bị **bỏ rơi sau 3 giây** (ngay sau nó là 満額 = thông tin trung tính) | Đà bị bẻ gãy đúng lúc vừa mở | Cú lật dời xuống **0:29** — đúng miệng vách 10→30s: 「ところが、この三万三千円は、今日の本題ではありません。」 |
| 3 | Câu 3 và 4 **cùng một ý**, lặp `七万六百八円` 2 lần / 12 giây | 12 giây chở 1 ý — quá đắt với tệp 65+ | Gộp còn 1 câu |
| 4 | 「危ないんです」 = **lời dọa trống**, bài không hề chứng minh | Vi phạm trần YMYL của chính skill (sợ phải CÓ THẬT trong bài) | **Bỏ hẳn.** Thay bằng con số thật 7万3千円 ở 0:34 |
| 5 | 「まず事実から」→ persona →「先に、ひとつだけ」 = **3 cú phanh liên tiếp** (1:01–1:30 chỉ nói *về việc sắp nói*) | Phanh ngay sau khi vừa mở loop | Bỏ khối 「先に、ひとつだけ」 (thừa — cold open đã trả 2 con số rồi) |
| 6 | **30 giây đầu không một VẬT nào** | Lớp hình collage không có gì để bám | 通知書 ở giây 0, và nó là vật xuyên suốt cả bài |

### Lỗi thứ bảy — cái NẶNG nhất, không nằm ở cold open

**伊藤 có 0 câu thoại, 0 chi tiết đời sống** trong suốt v1 → chất người ≈ **1/6 mũi tiêm**
(chuẩn `humanize-script-voice.md` = ≥4/6, và ở kênh này mũi ①④ **bắt buộc đi qua cast** vì 案内役 bị cấm
kể trải nghiệm cá nhân — §1.1). Đã thêm:

- **mũi ②③** — chi tiết đời sống vô dụng-về-thông-tin ＋ ký ức đúng tệp:
  「椅子が五つだけの、小さな店です。昼を過ぎると、常連さんが将棋を指しにきます。」
- **mũi ②** — câu THOẠI đầu tiên của 伊藤, đặt đúng chỗ đau: 「あのころは、払えなかった。払えなかったことが、ずっと引っかかっていてね」
- **mũi ⑤** — đóng nhân vật **bằng cảm xúc, không bằng kết luận**: 「払えなかった年が、いま返ってくるのか」／「そうおっしゃったきり、しばらく黙っていらっしゃいました。」

### ⭐ Cái chữa được bệnh "rời rạc" — một XƯƠNG SỐNG, không phải một danh sách

48 tháng 免除 giờ xuất hiện **ba lần, ba vai khác nhau**:

| ~3:12 | **món nợ lòng** — 4 năm quán ế, không đóng nổi bảo hiểm. 伊藤 coi đó là 負い目 |
|---|---|
| ~3:30 | **open-loop gieo tường minh**: 「覚えておいてください。この四十八か月が、あとで効きます。」 |
| ~10:50 → 11:21 | **món quà** — đúng 48 tháng đó có đơn giá 2,09× tháng đã đóng, và mang về 1万4千円 trong 7万3千円 |

⇒ Nửa đầu và nửa sau bị **khóa vào nhau bằng một đối tượng duy nhất**, thay vì là hai khối thông tin
nối đuôi. Đây là thứ v1 không có, và là lý do v1 nghe "rời rạc" dù đúng hết gate.

### Hệ quả số đo (v1 → v2)

| | v1 | v2 |
|---|---|---|
| **G17 dữ kiện ký 50–150** | 9 (2·5·4·1) | **10 (5·3·7·3)** — cao nhất mọi script của kênh |
| số trong 30s đầu | 6 | **8** (trần 8) |
| G14 payoff 答え | 66% | **69%** — và marker dời về **đúng chỗ**: đáp án của open-loop là lúc tính ra 7万3千円, không phải lúc giải thích cơ chế 2倍 |
| 伊藤 vào bài | 3:39 | **3:12** (vẫn ≥2:00) |
| câu thoại của cast | **0** | 2 |
| độ dài | 16:30 | 16:54 |

### ⚠️ Điều KHÔNG được suy ra từ vòng sửa này

Bản v2 hay hơn v1 **về nghề viết** — đó là thứ tao dám khẳng định. Nhưng `08_ANALYTICS_LOG.md` 09-10 đã
**BÁC bằng số 4 giả thuyết** rằng chữ cold open chữa được vách 10→30s (3 khuôn mở khác hẳn nhau, drop y
nguyên −34…−51). Biến trội đo được vẫn là **chất lượng traffic** (browse AVP 15% vs RELATED 27%).
⇒ **Đừng đọc v2 như một liều thuốc retention.** Nó là: ① đặt cược vào G17 — biến script DUY NHẤT có tương
quan đo được (+0,83) ② trả đúng lời hứa của thumbnail ngay giây 0 ③ làm bài đáng xem hơn cho người ĐÃ ở lại.
Đòn bẩy lớn nhất vẫn nằm ngoài script: end screen + pin comment + playlist theo trụ (treo từ 08-31).

## VÒNG SỬA v3 (2026-09-14) — QUAY VỀ **MỘT GIỌNG** + gate được sửa theo

> user: *"tao muốn chuyển về 1 người nói thôi"*.

**Cách chuyển — không phải xoá vai, mà ĐỔI CÁCH THI HÀNH.** 19 cặp hỏi–đáp thành **tự vấn–tự đáp**
của chính người dẫn, giữ nguyên chức năng phá nhịp:

| bản 2 vai | bản 1 giọng |
|---|---|
| `[聞]十八万円以上。ほとんどのかたが、当てはまりますね。` | `十八万円以上。月にすれば、一万五千円です。あなたの年金も、まず当てはまります。` |
| `[聞]超えたら、引かれない。得をするんですか。` → `いいえ。逆です。` | `超えたら、引かれない。得をするのでしょうか。いいえ、逆です。` |
| `[聞]待ってください。免除されていた月のほうが、単価が高いんですか。` | `お待ちください。免除されていた月のほうが、単価が高いのではありませんか。` |

🔴 **Ràng buộc kỹ thuật đã tính:** mỗi câu chuyển phải giữ được thuộc tính **"alive"** mà G13 đo
(`か。`／`でしょうか`／`ですが・ところが・逆`／`てください`／`あなた＋số`) — nếu không, bỏ vai 聞き手
là **khối chay nổ ra ngay**. Đã dính 1 khối 58s ở 11:39 và chữa bằng cách biến đỉnh cảm xúc thành
hành động của người xem: 「ここで、ご自分の記録を思い出してみてください。免除の期間は、ありませんでしたか。」

### 🔧 GATE G12 ĐÃ ĐƯỢC SỬA, KHÔNG BỎ QUA

G12 cũ đòi cứng ≥12% dòng `[聞]` ⇒ **mọi script 1 giọng đều 🔴, kể cả 20 bản đã lên sóng của chính
kênh này**. Đó là gate đo **hình thức thi hành của bản mẫu 2 vai**, không đo cơ chế — đúng bệnh
`humanize-script-voice.md` §1.2 và `audience-45plus.md` §2.0i (*thấy mình định viết "gate này đỏ
nhưng bỏ qua được" thì đó là lúc sửa GATE*).

- `check_pace.py` nay **tự nhận chế độ**: 0 dòng `[聞]` ⇒ chạy **G12s**; có `[聞]` ⇒ chạy G12 cũ.
- **Sàn G12s = 2,5% câu tự hỏi**, lấy từ ĐO THẬT 20 script 1 giọng của kênh:
  min 1,3 · bách phân 10 ≈ 2,7 · **trung vị 6,8** · max 14,2 ⇒ 2,5% cho qua 19/20 bản cũ.
  ⚠️ Đây là **sàn chống thoái lui, KHÔNG phải ngưỡng retention đã chứng minh** — chưa có số nào
  nối mật độ câu hỏi với awr. Đừng trích nó như bằng chứng.
- Gánh nặng pass/fail của cơ chế "không giảng một mạch" dồn về **G13**, vốn đo trực tiếp và
  không phụ thuộc số vai.
- ✅ **Hồi quy:** chạy lại trên v23 (2 vai) → vẫn ăn khuôn cũ, 13% (16/124), sạch.
- Backup: `tools/check_pace.py.bak_20260914`.

⚖️ **Số đo cần biết khi đọc kết quả sau này:** v25 đạt **19,8% câu tự hỏi — cao hơn mọi script
1 giọng từ trước của kênh** (max cũ 14,2). Và v21 — bản 2 vai duy nhất có số — đang giữ **AVP 23,6%,
cao nhất bảng 09-10**, nhưng chỉ **102 view** nên mẫu quá nhỏ để kết luận. Nếu v25 tụt dưới nhóm
1 giọng cũ thì **biến 2-vai-hay-1-vai là ứng viên đầu tiên xét lại**, không phải cold open.

---

## LỚP HÌNH — SCENE PLAN ĐÃ CHỐT (2026-09-14)

Đường dựng: **vox paper-collage `newsprint-editorial`** (CLAUDE.md §②, luật từ video 23).

| | |
|---|---|
| voice + timeline | ✅ `voice_full.wav` + `timeline.json` — **121 dòng · 988,6s = 16:28** (`make_timeline_exact.py`, lệch 0,000%) |
| bảng scene | ✅ `tools/_scenes25.py` — **117 scene**: art 79 · stat 18 · formula 7 · genten 5 · gfx 8 |
| gate scene | ✅ `tools/plan25.py` → **5/5 sạch** (dòng timeline khớp 121 · telop ≤11 ký · genten có trong sổ · scene liền mạch · lặp khuôn) |
| **số clip phải gen** | ⭐ **82 clip** · 21 khối art · scene dài nhất 28,0s |
| nhịp đổi hình | **5,0/phút** ✓ (trần 6 — `audience-45plus.md` §2) |
| phân bố khuôn | VIZ 23 · PERSON 17 · HOLD 10 · SPLIT 8 · DESK 7 · META 6 · CROWD 5 — PERSON **22%** (trần 35%) |
| prompt | ✅ `06_VIDEO/25_.../vox25_FLOW.txt` (82 prompt, 2.951–3.345 ký) · `vox25_TENFILE.txt` · `vox25_LOT1.txt` (**7 shot gen thử trước, đủ 5 khuôn**) · `vox25_PROMPTS.md` |

**Ba guard đã kiểm có mặt trong prompt:** ① người Nhật cao tuổi ② **mọi mặt giấy TRỐNG, không một
chữ/số nào** ③ chừa dải phải cho mascot + logo. Guard ② là lý do `NUM` rỗng — số chốt do
`papercut-stat`/`formula`/telop vẽ bằng **font** (`feedback_so_tren_hinh_phai_do_font_ve`).

**5 thẻ 原典** (4 URL, trang `rourei.html` dùng 2 lần khoanh 2 chỗ khác nhau) đã ghi trong
`_scenes25.GENTEN`, **y-range để `None` = CHƯA CHỤP** — phải chạy bước 6.7 (chrome-headless-shell)
rồi đọc bằng mắt mới chốt toạ độ. ⛔ Không bịa y.

### Việc kế tiếp, đúng thứ tự
1. **Gen `vox25_LOT1.txt` (7 shot) TRƯỚC** — lô 16 clip của video 22 hỏng cả lô vì lỗi cấp khuôn.
2. Duyệt mắt → gen nốt 75 prompt còn lại → `ingest` (đổi tên theo `vox25_TENFILE.txt`, soi ✦).
3. Chụp 5 thẻ 原典 (bước 6.7) → `make_genten_25.py`.
4. `build_remotion_25.py` (copy từ `build_remotion_23.py`) — **chỉ chạy được sau khi có clip**, vì nó
   lấy kho clip THẬT làm nguồn sự thật chứ không lấy `plan25.nshot`.
5. `check_frame_pace.py` → `SACH 3/3` (cần **≥ 988,6÷7 ≈ 142 sự kiện hình**).
6. Soi ≥10 still → render chunk (`render_chunks`, Remotion không có resume).

---

# ĐÓNG GÓI UPLOAD (2026-09-14)

### Title CHỐT

```
年金から引かれる3万3千円！もらえる給付金7万3千円｜国民年金だけの一年
```

36 ký · keyword đo cao nhất `年金` ở vị trí 1 · keyword thứ hai `給付金` ở vị trí 12 ·
⛔ không dùng tag 【】 cảnh báo chung chung (bài học 【見逃し厳禁】 7/9 video kéo về feed drama/bóng chày).

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `年金から引かれる3万3千円！もらえる給付金7万3千円｜国民年金だけの一年` | 36 | 年金@1 · 給付金@12 | keyword đo cao nhất đứng đầu ＋ **hai con số đối nghịch** (mất／được) |
| **A2** | `国民年金だけで月6万5千円｜通帳から消える3万3千円と、届かない7万3千円` | 37 | 国民年金@1 | đổi keyword dẫn sang `国民年金` — volume nhỏ hơn nhưng **lọc đúng tệp** |
| **A3** | `【通帳を見てください】年金額と振込額が違う理由｜68歳・国民年金だけの一年` | 37 | 年金@12 | đổi kiểu hook: mệnh lệnh ＋ **câu hỏi cơ chế**, bỏ hết con số — thử giả thuyết "số trên title hút sai tệp" |

### Tên file upload

```
nenkin-tenbiki-3man3sen-kyufukin-7man3sen.mp4
```

### 概要欄 — 3 dòng đầu

```
通帳に入る額は、あなたの年金額ではありません。65歳を過ぎると介護保険料などが天引きされるからです。
国民年金だけで暮らす68歳・伊藤さんの一年を、入る額・引かれる額・上乗せできる額の3つに分けて計算しました。
ご自分の年金振込通知書を手元に置いて、同じ順番で確かめられる内容です。
```

### 概要欄 — Mô tả đầy đủ

```
通帳に入る額は、あなたの年金額ではありません。65歳を過ぎると介護保険料などが天引きされるからです。
国民年金だけで暮らす68歳・伊藤さんの一年を、入る額・引かれる額・上乗せできる額の3つに分けて計算しました。
ご自分の年金振込通知書を手元に置いて、同じ順番で確かめられる内容です。

制度を読むチャンネルではありません。あなたの数字を計算する研究室です。

【目次】
00:00 通帳に入る額は、あなたの年金額ではない
00:29 引かれた3万3千円は、今日の本題ではありません
01:14 当研究室について
01:45 ① いくら入るのか — 令和8年度の満額と、480か月の分母
03:12 伊藤さん（68歳・福岡）と、免除の4年間
04:51 年金振込通知書の内訳 — 差の5,500円はどこへ
05:40 ② なぜ引かれるのか — 特別徴収のルール（65歳以上・年18万円以上）
07:30 介護保険料は、いくらが普通なのか（全国平均 月6,225円）
08:18 応援のお願い
08:48 ③ いくら上乗せできるのか — 年金生活者支援給付金
10:00 公式の計算式は、二つに分かれている
10:50 免除された月のほうが、単価が2倍以上
11:21 伊藤さんの給付金を計算する — そして、負い目だった4年間
13:16 所得がなくても「申告」が要る理由
13:54 今日の研究ノート（5点）
15:04 まるばつクイズ 3問
16:24 次回予告

令和8年度の老齢基礎年金の満額は、年847,300円、月70,608円です（昭和31年4月1日以前生まれのかたは年844,900円）。
ところが、この額がそのまま振り込まれるわけではありません。65歳以上で年金の年間受給額が18万円以上あるかたは、
介護保険料が年金から天引きされます（特別徴収）。65歳以上75歳未満のかたは、国民健康保険料も同じ扱いになります。
ただし介護保険料と国民健康保険料の合計が、その回の年金額の2分の1を超える場合、国民健康保険料は特別徴収の
対象になりません。その場合は納付書でご自分で納めることになります。

一方で、受け取れるお金もあります。年金生活者支援給付金は、65歳以上で老齢基礎年金を受けていること、
世帯全員の市町村民税が非課税であること、前年の年金収入とその他の所得の合計が809,000円以下であること
（昭和31年4月1日以前生まれのかたは806,700円以下）が条件です。給付額は、保険料を納めた期間に基づく額
（月額5,620円×納付済期間÷480月）と、保険料を免除された期間に基づく額（月額11,768円×免除期間÷480月）
の合計です。1か月あたりに直すと、免除された月のほうが単価が2倍以上になります。基準額を少し超えたかたには、
補足的老齢年金生活者支援給付金（809,000円超〜909,000円以下）があります。

なお、非課税かどうかは申告があってはじめて判定されます。収入が少ないから申告は不要と考えて何もしていないと、
給付金も保険料の軽減も止まることがあります。

※本動画は令和8年9月時点の公表情報をもとにした一般的な解説です。保険料の段階や金額はお住まいの市区町村に
よって異なります。個別のご判断の前に、必ず年金事務所、またはお住まいの市区町村の窓口でご確認ください。
※登場する伊藤さんは、制度を分かりやすく説明するための架空のモニターです。

【出典】
・日本年金機構「令和8年4月分からの年金額等について」
　https://www.nenkin.go.jp/oshirase/taisetu/kojin/2026/202604/0401.html
・日本年金機構「老齢基礎年金の受給要件・支給開始時期・年金額」
　https://www.nenkin.go.jp/service/jukyu/seido/roureinenkin/jukyu-yoken/20150401-02.html
・日本年金機構 年金Q&A「年金からの介護保険料などの徴収」
　https://www.nenkin.go.jp/section/faq/jukyu/seido/kyotsu/tenbiki/20140421-03.html
・厚生労働省「第9期介護保険事業計画期間における介護保険の第1号保険料及びサービス見込み量等について」
　https://www.mhlw.go.jp/stf/newpage_40211.html
・日本年金機構「老齢（補足的老齢）年金生活者支援給付金の概要」
　https://www.nenkin.go.jp/service/jukyu/seido/sonota-kyufu/shienkyufukin/rourei.html

音声: VOICEVOX:雀松朱司

#年金 #老後のお金 #年金と老後のお金研究室
```

### タグ

```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金, 国民年金, 老齢基礎年金, 年金 満額, 年金 手取り, 年金 天引き, 特別徴収, 介護保険料, 国民健康保険料, 年金振込通知書, 年金生活者支援給付金, 補足的老齢年金生活者支援給付金, 住民税非課税, 保険料免除, 令和8年度 年金額, 年金 偶数月, 68歳 年金, 年金 いくら引かれる, 年金 いくら入る
```

30 tag（12 tag nhận diện đứng đầu ＋ 18 tag đề tài）

### Pinned comment

```
ご視聴ありがとうございます。当研究室の、今日のノートです。

【研究ノート】
① 通帳の額は、年金額ではありません。65歳以上で年金が年18万円以上あれば、介護保険料は天引きされます（特別徴収）。
② 国民健康保険料も、65歳から75歳未満は天引きの対象です。ただし介護保険料との合計が年金額の2分の1を超えると、ご自分で納める側にまわります。
③ 令和8年度の満額は、年847,300円・月70,608円。納めた月数を480で割った分だけ受け取れます。
④ 年金生活者支援給付金は、納めた月より「免除された月」のほうが単価が高く、2倍以上です（5,620円と11,768円）。
⑤ 非課税の判定は、申告があってはじめて動きます。所得がなくても、申告は要ります。

お手元で確かめる3つ →
1. 年金振込通知書に、介護保険料・国民健康保険料がいくらと書かれていますか。
2. ご自分の記録に、保険料の免除期間はありませんか。あれば、給付金では有利に働きます。
3. 昨年の申告は出していますか。出していないと、非課税の証明が立ちません。

みなさんの通帳では、年金額と振込額の差はいくらでしたか。よろしければ、月いくら引かれていたかを教えてください。皆さまの声が、次の研究テーマになります。

※令和8年9月時点の情報です。保険料の段階や金額はお住まいの市区町村によって異なります。ご判断の前に、必ず年金事務所、またはお住まいの市区町村の窓口でご確認ください。
```

### 3 THUMBNAIL A/B (khuôn TELOP/A-45 — `03_THUMBNAIL_TITLE_FORMULA.md` §6)

Chữ **GIỐNG NHAU cả 3 bản** (biến thử là HÌNH — `ab-3title-3thumb.md` §3 mục 6);
bộ chữ qua gate 7 (che ảnh đi vẫn biết bài nói gì), và **CẢ HAI từ top-2 của bảng đo
đều có mặt**: `年金` (81,97) ở dòng 2 · `給付金` (14,81) ở dải đỏ.
🔴 Bản đầu của bảng này ghi dải đỏ là `もらえるのは7万3千円` — **đánh rơi `給付金`**, đúng
lỗi lặp ghi ở `audience-45plus.md` §1 gate 7 (video 09 đo keyword xong, áp cho title rồi
quên áp cho thumbnail). Bảng đo phải áp cho **CẢ title LẪN thumbnail**.

| khối | chữ | vai |
|---|---|---|
| chip 対象 (góc trên) | `国民年金だけの方へ` | tệp tự lọc trong 0,3 giây |
| banner | `年金から天引き` | keyword đo cao nhất |
| **HERO** | `3万3千円` | số hero — bề ngang ~60% khung |
| dải đỏ đáy | `給付金で7万3千円` | dấn thêm — **và chở keyword top-2 `給付金` (14,81)** |

| bản | biến đổi (đúng 1 biến) |
|---|---|
| **T1** baseline | nền kem sáng ＋ 年金振込通知書 cầm trên tay, không có mặt người (ngoại lệ nenkin miễn gate mặt — `audience-45plus.md` §1.2) |
| **T2** đổi 1 biến hình | giữ nguyên chữ ＋ layout, đổi nền sang **bàn bếp có 通帳 mở ＋ 封筒**, tông ấm hơn |
| **T3** đổi layout | bỏ chip, hero 2 dòng chiếm ~40% khung theo khuôn カメ先生 (`CHANNEL_BENCHMARK_takaichi-face_2026-09-07`) — **phép thử "bỏ cast／dòng phụ thì hero lên 38–40%"** đang chạy từ v21 |

⚠️ Prompt gen phải **bake chữ vào ảnh**, xuất 4 file theo `ab-3title-3thumb.md` §3.1 Bước 4:
`thumb_prompts_FLOW.txt` · `thumb_prompts_BLOCKS.md` · `thumb_prompts_TENFILE.txt` · `thumb_prompts_PLATE.txt`.
Khối `TEXT` phải nằm trong **15% đầu** prompt. Gen xong: **xoá ✦ watermark** rồi soi 1:1 cả 4 góc
(`media-library.md` §2.10 ⑤b).

### Compliance (`youtube-compliance.md`) — quét xong

| mục | kết quả |
|---|---|
| Từ tắt-ad ở title／thumbnail／概要 hiển thị (殺・血・死・破産…) | ✅ 0 |
| Misleading — tình tiết trên title có thật trong video | ✅ 3万3千円 (4:56) · 7万3千円 (11:17) · 国民年金だけの一年 (toàn bài) |
| Tên thật người／công ty／đảng phái | ✅ 0 |
| **Altered／synthetic** | ⚠️ **PHẢI TICK TAY** nếu lớp hình dùng ảnh／clip AI realistic (`youtube-compliance.md` §2.1) — `upload_pack.py` chưa có cờ này |
| Disclaimer YMYL | ✅ 「令和8年9月時点」 ＋ khuyên 年金事務所／市区町村 (lời đọc 12:52 và 概要欄) |
| Nhân vật hư cấu | ✅ 概要欄 ghi 「伊藤さんは架空のモニターです」 |
| Credit giọng | ✅ 「音声: VOICEVOX:雀松朱司」 |
| 断定表現 (必ず／絶対) | ✅ 0 — dùng 「目安です」「制度上は」「〜の場合が多い」 |

### Trạng thái đóng gói

- [x] Kịch bản `_TTS.md` **v2** — **gate 21/21 PASS**, 18 tag nhấn nhá, 0 tag lệch dòng, 0 tag đứng dòng riêng, 0 chữ `方` đọc sai
- [x] FACT SHEET verify (13 mục, 5 nguồn chính thức mở trong phiên)
- [x] Title CHỐT ＋ 3 TITLE A/B · tên file · 概要欄 3 dòng ＋ đầy đủ · タグ · **Pinned comment**
- [x] HÀNG XÓM MỤC TIÊU · sổ khuôn · bảng đo Trends
- [x] **5 khoá 原典 → 11 thẻ** đã chụp + dựng + soi 1:1 (`tools/make_genten_25.py`)
- [ ] `make_timeline_exact.py` → SCENES → `build_remotion_25.py` (copy từ `build_remotion_24.py`)
- [ ] Gen ảnh／clip ＋ xoá ✦ ＋ gate `check_frame_pace.py` (≥ 1.014÷7 ≈ **145 sự kiện hình**)
- [ ] 3 thumbnail ＋ gate 3×3 của `upload_pack.py`
