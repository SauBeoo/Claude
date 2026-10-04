# CHANNEL_BENCHMARK — ngách 実家じまい・空き家・相続登記 (JP), đo 2026-07-26

> Số liệu nền để lập kênh 「**実家とお金の整理ノート**」. **Mọi con số dưới đây là ĐO ĐƯỢC** (YouTube Data API v3, token readonly của nenkin + Google suggest API); chỗ nào không đo được ghi rõ ở §8.
> ⚠️ Bảng này **thay thế** phần "vì sao ngách này" trong `youtube-niche-research-2026.md` (đo 2026-07-23) — kết luận cũ "cung TRỐNG tuyệt đối" **đã sai** sau 3 ngày đo lại kỹ hơn (xem §1c).
> Đo lại toàn bảng **mỗi 6–8 tuần**.

## §0 Công cụ đo

- **API chính:** `youtube.googleapis.com/v3` — `search.list` (order=viewCount, publishedAfter=2024-01-01, regionCode=JP, relevanceLanguage=ja) → `videos.list` (snippet+statistics+contentDetails) → `channels.list` (statistics+brandingSettings).
- **Search demand:** `suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=ja&gl=jp&oe=utf-8&q=` (thiếu `oe=utf-8` → trả Shift-JIS lỗi).
- **Giờ đăng:** `publishedAt` (UTC) + 9h = JST. Lấy 12 video gần nhất/kênh.
- ⚠️ `search.list` chỉ trả video **YouTube xếp hạng theo query đó**, không phải toàn bộ ngách → trần view ở §2 là "trần đo được", không phải trần tuyệt đối.

---

## §1 Bản đồ cung

### §1a Ai đang ăn cụm này (không phải kênh chuyên đề)

| Kênh | Sub | #video | Tổng view | view/video | Mở | Vai |
|---|---|---|---|---|---|---|
| 脱・税理士スガワラくん | **1.720.000** | 1.672 | 543.325.052 | — | 12/2022 | **Kẻ ăn tất** — xuất hiện ở 9/10 keyword đo. Cùng kênh đang ăn cụm 介護 (xem benchmark kaigo) |
| 楽待 RAKUMACHI | 1.630.000 | 4.445 | 1.235.628.195 | — | 04/2009 | Kênh 不動産投資 — ăn cụm 相続登記義務化 (1,28M + 543K) |
| ケイト(Keito) | 49.000 | 94 | **19.625.727** | **208.784** | **01/2026** | ⭐ 6 tháng tuổi. Shorts 実家の解体費330万の回避術 = **2,53M** |
| 【円満相続ちゃんねる】税理士橘慶太 | 273.000 | 521 | 30.124.171 | 57.819 | 03/2016 | 税理士 mặt thật, lâu năm |
| 桃太郎オフィス 不動産事業部 | 203.000 | 268 | 199.805.195 | 745.541 | 12/2022 | Shorts 不動産, view/video cao nhất bảng |
| まるごと安全相続ch-あまおう税理士 | 41.800 | 260 | 7.188.865 | 27.649 | **10/2025** | ⚠️ **~1 video/NGÀY** → 12 video mới nhất chỉ **1.323–32.077 view** |
| 税理士勝部の相続チャンネル | 18.400 | 54 | 2.244.017 | 41.555 | **07/2025** | ⚠️ 1 video/tuần. Hit 550K nhưng đề mới lệch hẹp → **80–2.762 view** |
| 負動産の窓口│土地じまい専門 | 30.300 | 335 | 2.660.489 | 7.941 | 07/2021 | Chuyên 土地/山林 (không phải 実家) |

### §1b Kênh chuyên đề 実家じまい — **tất cả đều chết**

| Kênh | Sub | #video | view/video | Mở | Vì sao chết |
|---|---|---|---|---|---|
| 実家じまい研究所 | 835 | 20 | 2.891 | 08/2025 | Nội dung đúng đề, thật (có case 農地付き実家 10 tháng) nhưng **đăng 12:00–16:00 giữa trưa T3**, không title/thumbnail đóng gói, 0 tag. View 139–699 (1 hit lẻ 17K) |
| 実家じまいの教科書📖 | 5 | 8 | 468 | **16/07/2026** | ⚠️ Mở 10 ngày trước ngày đo. Toàn shorts 1′15″, 20:00 mỗi ngày. **Bằng chứng có người khác đang thử ngách này** |
| 実家じまい相談室 | 0 | 4 | 41 | 04/2026 | Shorts 25 giây, đăng 01:00–02:00 sáng |
| 負動産の窓口 実家じまい専門 | 117 | **0** | — | 07/2025 | Đặt tên + channel keywords rồi bỏ, chưa đăng video nào |
| 空き家・実家問題 解決チャンネル | 2.200 | **1.383** | 625 | 12/2020 | Farm shorts của 1 công ty BĐS 稲沢市 — 3 video/ngày, view 19–963 |

### §1c Kết luận cung (SỬA kết luận 2026-07-23)

1. **Cửa faceless long-form vẫn TRỐNG** — không kênh nào chiếm được vị trí "kênh chuyên trị tiền + thủ tục của căn nhà bố mẹ, format giải thích 18–25 phút".
2. **NHƯNG "trống tuyệt đối" là sai.** 3 kênh 税理士 mặt thật mở trong 12 tháng gần đây (勝部 07/2025 · あまおう 10/2025 · ケイト 01/2026) đều tăng nhanh, và kênh chuyên đề mới mọc **hằng tháng** (実家じまいの教科書 mở 16/07/2026). → **Cửa sổ tính bằng quý, không phải năm.**
3. **Cách những kênh nhỏ chết đều giống nhau:** sai giờ đăng (giữa trưa/nửa đêm), làm shorts thay long-form, không đóng gói title/thumbnail, hoặc chạy volume. Không phải vì thiếu chuyên môn.

---

## §2 Trần view theo cụm đề tài (video từ 2024-01-01, đo 2026-07-26)

| Cụm | Trần đo được | Ví dụ (view · kênh) |
|---|---|---|
| **相続・実家 NG行為/期限** | 250K–**2,99M** | 父親が亡くなった時の相続は母と子どっちが得 **2.989.589** (スガワラ) · 母親名義の実家が税金地獄 **883.252** (あまおう) · 実家の相続で絶対にやってはいけない6つ **550.086** (勝部) · 実家を相続したらすぐ売るな **466.204** (スガワラ) · 実家の相続を共有名義にすると超危険 248.057 |
| **相続放棄・負動産** | 222K–**1,97M** | 相続放棄が過去最多・0円でも手放したい負動産 **1.972.802** (ABCテレビ) · 築40年10年放置のボロ空き家 処理に400〜500万 **1.525.685** (不動産Gメン滝島) · 親の空き家を相続してしまった人の末路 1.056.930 (shorts) · 相続人が110人 222.013 (読売) |
| **固定資産税・空き家の税** | 128K–**1,57M** | 空き家900万戸・理由1位は物置 **1.570.533** (MBS) · **4月に届く固定資産税は97%が間違っている 1.061.815 (きな子＝FACELESS)** · 固定資産税を大幅に抑える方法 556.214 (スガワラ) · 税金6倍？空き家解体の抜け道 493.895 (ケイト shorts) |
| **実家じまい (TV/vlog)** | 954K–**2,47M** | ⚠️ ep038 モノが多い実家の現状 **2.473.421** (ぐりーん) · 実家の片付け前編 **1.773.683** / 後編 1.563.662 (uchilog) · 【実家じまい】アベプラ 1.682.981 · 兄弟で骨肉の争い (MBS) 1.120.070 |
| **相続登記義務化** | 116K–**1,28M** | 不動産の相続登記義務化を理解してますか **1.282.129** (楽待) · 罰則に注意・遺産分割の新ルール 543.658 (楽待) · すでに義務化は始まってます 369.451 (スガワラ) · 自分で相続登記したい方へ 128.558 (司法書士きいちゃんねる) |
| **墓じまい** | 785K–**2,03M** | 徳川慶喜家も墓じまいへ **2.025.096** (FNN) · ひとり娘の墓じまい 1.835.789 · みんなのお墓チャンネル (127K sub, 774 video) chuyên trị cụm này **ở shorts** — long-form còn trống |
| **兄弟で分ける** | 275K–1,12M | 兄弟で骨肉の争い 1.120.070 (MBS) · 1つの不動産を2人でどう分ける 275.252 (そろそろ相続税) |
| **空き家3000万控除** | 41K–565K | 空き家撲滅へ！5つの法改正 165.472 (オタク会計士) · 老人ホーム入居前に確認・実家の相続税80%オフ 137.596 (円満相続) · 3000万控除が消える 41.905 (不動産売却ch) |

**Phản ví dụ (đề đúng, đóng gói sai):** 勝部 12 video mới nhất — 国際相続 **80 view** · 帰化人の相続 173 · 相続時精算課税 2.762. Cùng kênh, cùng sub, **rời lõi "実家/親の家" sang chuyên môn hẹp → view sụp ~600 lần.** (Trùng khớp bài học ケアまど ở benchmark kaigo.)

---

## §3 ⭐ Proof-of-format: きな子のシニアお金ゼミ (faceless VOICEVOX)

| Chỉ số | Giá trị |
|---|---|
| Sub / video / tổng view | **167.000** / 117 / 17.139.532 → **view/video 146.491** |
| Mở | 2024-02-20 (2,4 năm) |
| categoryId | **26** (12/12 video gần nhất) |
| Giờ đăng | **20:00 JST** (11/12 video gần nhất; còn lại 19:01). Video cũ hơn: 18:00–18:01 → **kênh đã DỜI từ 18:00 sang 20:00** |
| Độ dài | 20′49″–28′12″ (hit lớn nhất 31′05″ và 35′03″) |
| Tag | **chỉ 4 tag**: 年金 / 老後 / 定年 / 60代. channel keywords 12 ký |
| Nhịp | ~1 video/2 ngày |
| Phân tán view | 1.575 → 131.780 trong cùng 12 video ⇒ **kênh này sống bằng vài quả trúng đậm, không phải view đều** |

**4/4 hit lớn nhất cùng MỘT khuôn:**

| View | Tiêu đề | Cấu trúc |
|---|---|---|
| **1.281.471** | 【緊急】10月に届く年金通知書のココを必ず確認しろ！ | tờ giấy + THÁNG + chỗ phải soi |
| **1.061.815** | 【警告】4月に届く固定資産税は97%が間違っている！？知らないと生涯で100万円以上損する | tờ giấy + THÁNG + số tiền mất |
| **534.693** | 【緊急速報】2026年の確定申告〇〇を記入してしまうと20万円の大損に！ | hạn + ô ghi sai + số tiền |
| **362.902** | 【超速報】2026年1月に届く源泉徴収票！申告漏れると14万円損します！ | tờ giấy + THÁNG + số tiền |

→ **Khuôn thắng của tệp senior-money JP = 「あなたの家に届いた1枚の紙 — ここが違うと◯万円」**, KHÔNG phải 「制度をわかりやすく解説」. Đây là lõi nội dung user chốt cho kênh akiya (2026-07-26).

---

## §4 Giờ đăng + metadata (đo publishedAt, 12 video gần nhất/kênh)

| Kênh | Giờ JST | Ngày | cat | #tag | Độ dài |
|---|---|---|---|---|---|
| **きな子 (faceless, cùng tệp)** | **20:00 × 11/12** | rải (T6×3, CN×2, T4×2) | **26** | 4 | 20–28′ |
| まるごと安全相続ch-あまおう | **18:00 × 12/12** | mọi ngày (1/ngày) | 27 | 30–32 | 12–24′ |
| 税理士勝部 | **19:00 × 12/12** | **T7 × 12/12** | 22 | 5 | 10–28′ |
| ケイトのコトノハ日和 (vlog 60代) | 18:00 × 11/12 | T5/T6 | 22 | 2–5 | 8–10′ |
| 負動産の窓口 | 20:00 × 9/12 | rải | 22 | 0 | 1–24′ |
| 実家じまい研究所 (chết) | ⚠️ 12:00–16:00 | T3 | 26 | 0 | 3–9′ |

**Kết luận §4:** dải chuẩn của ngách = **18:00–20:00 JST**. Chọn cho akiya: **20:00 JST** — theo kênh faceless duy nhất chứng minh được format (きな子), đồng thời tách khỏi 4 kênh workspace đang đăng 19:00. **categoryId 26**; **tag không phải yếu tố thắng** (kênh 4 tag ăn 1,06M, kênh 32 tag view 1,3K) nhưng vẫn giữ rổ nhận diện theo rule §2.4.

---

## §5 Search demand (YouTube autocomplete, hl=ja&gl=jp, thứ tự = độ phổ biến)

| Seed | Gợi ý theo thứ tự | Đọc ra |
|---|---|---|
| **相続登記** | を自分で行う方法 / 義務化 / **必要書類** / **書類の綴じ方** / オンライン申請 / **申請書の書き方** / 費用 / 遺産分割協議書 / 原本還付 / **登録免許税 計算** / 自分でやってみた | ⭐ Intent **CẦM TAY CHỈ VIỆC** — người ta định tự làm. Long-form faceless chưa ai phục vụ tử tế |
| **相続放棄** | の手続き / **しても借金は消えず** / **管理責任** / 必要書類 / **空き家** / **兄弟** / 申述書書き方 / **失敗** / 生命保険 / 借金 / 費用 | Intent **CẠM BẪY** — hợp trục C |
| **実家じまい** | 片付け / **費用** / 業者 / 松本明子 / **自分で** / ゴミ屋敷 / マンション / **仏壇** / 断捨離 | Volume tốt nhưng top result là vlog |
| **実家 相続** | 相続放棄 / **兄弟** / 売却 / 相続税 / 賃貸 / 税金 / 片付け | Trục D (兄弟) đứng #2 |
| **実家 片付け** | 断捨離 / 娘 / 業者 / 捨てる / 息子 / **困ってます** / **喧嘩** / 費用 / 50代 | Intent cảm xúc/xung đột — chất liệu case, không phải trục chính |
| **墓じまい** | **費用** / **流れ** / 永代供養 / **トラブル** / 自分で / お骨 / 代行 | Trục E, cấu trúc y hệt 実家じまい |
| **相続 不動産** | 評価 / 名義変更 / 売却 税金 / 登記 / 分割 / 確定申告 | Đều là thủ tục + thuế |
| ⚠️ **空き家** | **を手に入れた高校生 / リフォーム / バンク / 問題 / ビジネス / DIY / 再生 / 宅建 / 活用** | 🚫 **Tệp NHÀ ĐẦU TƯ + DIY, KHÔNG phải con cái lo nhà bố mẹ.** Cấm dùng 空き家 làm keyword trục đơn lẻ — luôn ghép 実家/親の家 |
| 空き家 税金 / 実家 売却 / 家 相続 手続き | chỉ 3–5 gợi ý | Volume mỏng ở dạng ghép — dùng làm long-tail, không làm keyword chính |

---

## §6 Hai cửa sổ deadline (verify 2026-07-26)

| Chế độ | Mốc | Ghi chú |
|---|---|---|
| **相続登記義務化** (2024-04-01 thi hành) | Thừa kế **trước** 2024-04-01 → hạn **2027-03-31**; sau đó là "3 năm kể từ khi biết mình được thừa kế". Quá hạn → **過料 10万円以下**. Van cứu: **相続人申告登記** (chỉ khai báo, không thay thế đăng ký chính thức) | ⏳ **Còn ~8 tháng tính từ ngày đo** → đây là mùa cao điểm của kênh |
| **空き家の譲渡所得3.000万円特別控除** | Bán trong khoảng 2016-04-01 → **2027-12-31** (令和9年). Từ 2024-01-01: được phá dỡ/耐震改修 đến **翌年2月15日** sau khi bán; **≥3 người thừa kế → trần còn 2.000万円** | Đề tài "bán trước hạn" có deadline thật |

Nguồn: [法務省](https://www.moj.go.jp/MINJI/minji05_00343.html) · [国税庁 No.3306](https://www.nta.go.jp/taxes/shiraberu/taxanswer/joto/3306.htm) · [国土交通省 空き家特例](https://www.mlit.go.jp/jutakukentiku/house/jutakukentiku_house_tk2_000030.html)
⚠️ **Mọi con số đưa vào script vẫn phải qua FACT SHEET riêng của video đó** — bảng này chỉ để xếp lịch đề tài.

---

## §7 Bài học rút ra cho kênh mình

1. **Khuôn 「届く紙 × 期限 × ◯万円」 là khuôn thắng** (§3) — đây là mũi nhọn 10 video đầu.
2. **Đừng đua footage đời thật** (§2 cụm 実家じまい): uchilog/ぐりーん ăn 1,7–2,4M bằng chính căn nhà của họ. Faceless đấu = thua. Dùng 片付け như một **dòng chi phí** trong bảng tính, không làm nội dung chính.
3. **Đừng lấy 空き家 làm keyword trục** (§5) — kéo về tệp đầu tư/DIY, thuật toán phân loại sai.
4. **Volume là chiến lược thua** (§1a): あまおう 1 video/ngày → 1,3–32K view. Trùng kết luận benchmark nenkin 2026-07-25.
5. **Rời lõi = chết** (§2 phản ví dụ): 勝部 chuyển sang 国際相続 → 80 view. Lõi của kênh mình phải luôn là **"căn nhà của bố mẹ bạn"**, không phải "luật thừa kế nói chung".
6. **Không có tư cách 士業 → không đấu uy tín bằng danh xưng.** Đấu bằng: tính hộ tiền (值段表) + cầm tay chỉ việc (đúng intent 相続登記 自分で ở §5) + chiếu 原典.

---

## §8 Điều KHÔNG đo được lần này (đừng trích như đã đo)

1. **Google Trends** — chưa đo (làm ở `01_KEYWORD_RESEARCH.md`, rule `youtube-upload-seo.md` §0.5). Autocomplete chỉ cho **thứ tự tương đối**, không cho volume.
2. **RPM/CPM riêng cho 相続/空き家** — chỉ có proxy ngành 不動産投資 800–1.200円/1.000view ([UREBA Lab](https://ureba.jp/lab/current-youtube-ad-cpm/)). Không phải số đo của ngách này.
3. **Demographics thật** (tuổi/giới của người xem cụm này) — không có API công khai; giả định 50–65 suy từ nội dung + tệp vlog đối chiếu.
4. **Đơn giá affiliate** 不動産一括査定 / 遺品整理 (số 10.000–25.000円/case trong file research cũ chưa verify lại).
5. **Retention/CTR của đối thủ** — API không trả.
6. **Sub thật của kênh <1.000** (YouTube làm tròn).
7. **Case kênh ngách này bị demonetize** — không tìm thấy dữ liệu.
8. `search.list` bỏ sót video hay ở query khác → trần §2 là sàn dưới của trần thật.
