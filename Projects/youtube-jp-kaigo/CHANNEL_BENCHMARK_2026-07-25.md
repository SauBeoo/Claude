# CHANNEL_BENCHMARK — ngách 介護×お金 (JP), đo 2026-07-25

> Số liệu nền để lập kênh 「親の介護とお金ノート」. **Mọi con số dưới đây là đo được, có nguồn** — chỗ nào không đo được đã ghi rõ ở §7.
> Đo lại bảng này **mỗi 6–8 tuần** (như `youtube-jp-nenkin` đang làm).

## §0 Công cụ đo (vì sao không dùng nguồn thường)

`youtube.com` bị chặn WebFetch; `socialblade`/`yutura`/`noxinfluencer` trả 403/paywall. Thay thế:
- **View thật từng video:** `returnyoutubedislikeapi.com/votes?videoId=` (field `viewCount` lấy từ YouTube API).
- **Tên video/kênh:** `noembed.com/embed?url=`.
- **Sub / tổng view / số video:** `socialcounts.org` (đọc YouTube Data API trực tiếp).
- **Demand search YouTube:** `suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=ja&gl=jp&oe=utf-8&q=` (thiếu `oe=utf-8` → trả Shift-JIS lỗi).
- ⚠️ Field `dateCreated` của RYD API là ngày ghi vào DB của RYD, **KHÔNG phải ngày upload** — không dùng làm tuổi video.

## §1 Bản đồ đối thủ

| Kênh | Sub | Tổng view | #video | Ngách | Ghi chú |
|---|---|---|---|---|---|
| 脱・税理士スガワラくん | **1.720.616** | 543.437.425 | 1.670 | Thuế/tiền, **lấn 相続・後見人・親の預金** | Mở 12/2022, đạt 100万 sau 2 năm 2 tháng. **Kẻ đang ăn cụm này** |
| 節約看護師りょう | 748.294 | 75.788.062 | 158 | 給付金・老後のお金 | Hit 1,98M là 給付金 cho 高齢者 |
| みんなの給付金・補助金ちゃんねる | 551.909 | 72.296.045 | 429 | 給付金・年金・税, **có phủ 介護** | Chủ kênh là **cựu công chức thành phố**; Gakken mô tả tệp gồm 「親の年金や介護、医療費」 |
| シニア貯蓄ラボ | 144.000 | 20.742.423 | 154 | 年金・給付金・社会保険 | |
| ケアきょう | 144.000 | 35.281.804 | 1.668 | ⚠️ **B2B — cho NHÂN VIÊN 介護** | Lệch tệp hoàn toàn, không phải đối thủ |
| 兄のぼる【父の介護クエスト】 | 85.526 | 99.353.863 | 345 | Documentary chăm bố đột quỵ | Mở 12/02/2021, đã ra 最終回 03/06/2025 |
| みんなの介護 | 45.900 | 7.901.751 | **14.746** | Corporate, chủ yếu Shorts | Site 資料請求 có TVCM |
| 親ケア.com公式【介護講座】 | ~40.000 | 3,5M+ | **864** | ⭐ **Đúng ngách nhất** | Chủ kênh 横井孝治 (介護アドバイザー thật), đăng **hàng tuần**, relaunch 30/11/2020 → **view 42–1.276/video** |
| 介護の窓口ケアまど | **7.090** | 4.208.868 | 198 | ⭐ Series 【介護とお金】 | Cty giới thiệu 老人ホーム (Nagoya) — **view/sub tốt nhất ngách** |
| 税金・社会保障教育ちゃんねる | (không đo được) | | | 世帯分離 × 介護保険料 | |
| ゆるっとかいご | (không đo được) | | | Đúng ngách 100% | Không tra ra channel ID |

**Kết luận §1:** **không kênh nào >100K sub chuyên trị 介護×お金.** Cụm đang bị 2 phía tấn công cơ hội: kênh thuế 1,72M sub làm video 707K rồi đi; kênh 介護 7K sub làm video 63K nhưng không đủ lực phân phối. **Vùng giữa trống.**

## §2 Đề tài — bảng view THẬT, xếp giảm dần

| # | Đề tài | View | Kênh | Cluster |
|---|---|---|---|---|
| 1 | 政府が高齢者へ50万円支給！申請しないと貰えない給付金5選 | **1.985.235** | 節約看護師りょう | 給付金 |
| 2 | 政府から高齢者へ40万円！60歳以降に申請すれば得する給付金 | **1.083.383** | シニア貯蓄ラボ | 給付金 |
| 3 | 相続対策：親の預金口座のお金を生前に引き出した方がいい理由 | **707.712** | スガワラくん | **相続×親の金** |
| 4 | 親族後見人が引き起こす家族崩壊のリスクと回避方法 | **437.198** | スガワラくん | **成年後見** |
| 5 | 【2026最新】払いすぎた医療費が戻る！医療費控除のやり方（5年遡及） | **193.882** | — | 医療費控除 |
| 6 | 介護保険制度とは？完全ガイド | 123.956 | みんなの介護 | 介護保険 |
| 7 | 「介護＝離職です」認知症の母と2人・両立は無理（年間10万人） | 112.874 | カンテレNEWS | **介護離職** |
| 8 | 【家族信託】親の資産が凍結される！？認知症になったら資産と不動産は | 104.436 | **SBI証券公式** | **認知症→凍結** |
| 9 | 世帯分離とは？保険料が〇万円安くなる？ | 96.609 | 税金・社会保障教育ch | 世帯分離 |
| 10 | 特別養護老人ホーム（特養）とは？費用・対象者・入居条件 | 69.352 | みんなの介護 | 特養 |
| 11 | 【介護とお金】介護施設の費用を"安く"する「負担限度額認定証」 | 63.961 | ケアまど | 負担限度額 |
| 12 | 【介護とお金】年金で老人ホームに入れる？施設費用の相場 | 51.802 | ケアまど | 年金 vs 施設 |
| 13 | 預金も年金も無い両親の介護を自分ひとりで支えられるか | 50.536 | 親ケア.com | Bố mẹ không tiền |
| 14 | 介護をする義務は誰にある？（民法・長男の嫁） | 47.757 | 親ケア.com | **義務** |
| 15 | 兄弟姉妹で介護の話し合いを避け続けると起きる悲劇 | 36.977 | 親ケア.com | **兄弟** |
| 16 | 高額介護サービス費とは（5分） | 25.509 | ゆるっとかいご | 高額介護 |
| 17 | 【5分で分かる】親の介護にかかる費用 | 23.356 | — | 介護費用 |
| 18 | 介護保険の自己負担割合の計算（所得別フローチャート） | 20.540 | みんなの介護 | 1〜3割負担 |
| 19 | 医療費控除：介護サービス費も対象 | 19.626 | — | 医療費控除×介護 |
| 20 | 親が介護や認知症になった時でもお金が使える対策 | 12.615 | — | 認知症対策 |
| 21 | 親の介護いくら用意すればいい？ | 10.931 | — | FP Q&A |
| 22 | 「介護を無視した兄弟」に遺産は渡さない！法定相続分を削る戦い方 | 4.458 | — | 寄与分 |

**Phản ví dụ (topic đúng, format sai — bằng chứng "topic một mình không cứu được"):**
- 「知らないと損！7分でわかる介護費用の負担を減らす4つのしくみ」 = **584 view**
- 「【2025年最新版】540万円？3300万円？平均的な介護費用」 = **3.410 view**
- 「図解でわかる介護保険制度」 = **809 view**

**Kết luận §2:** cụm 制度解説 trần 20K–120K · cụm "tiền của bố mẹ" (相続/後見/凍結/控除) trần 104K–707K · cụm cảm xúc-xung đột đạt 36–50K **ngay trên kênh chỉ 40K sub** (view/sub tốt nhất nhóm đúng ngách).

## §3 Search demand (YouTube autocomplete — thứ tự = độ phổ biến truy vấn)

| Seed | Gợi ý theo thứ tự | Đọc ra |
|---|---|---|
| **親の介護** | 記録 / の記録 / と自分の暮らし / **したくない** / **兄弟喧嘩** / **ストレス** / 費用(#8) / **退職** / 自分の生活 / で退職 / **放棄** / をしない兄弟 / **義務** | Intent chủ đạo = **cảm xúc & xung đột**; 費用 chỉ #8. 4/13 gợi ý về anh em/nghĩa vụ/bỏ mặc |
| **介護費用** | 軽減制度 / 平均 / いくら / **確定申告** / **世帯分離** / 医療費控除 | Chỉ 6 gợi ý (volume mỏng) nhưng **100% intent giảm tiền** |
| **介護 お金** | **お金がない** / お金 / のお金 / 介護資金 / 親 介護 お金 | Top = 「介護 お金がない」 |
| **介護離職** | の現実 / **失業保険** / 防止支援コース / **独身** / 両立支援等助成金 / 高市早苗 介護離職 | Có news-hook chính trị |
| **相続 介護** | 相続 介護 / 相続 認知症 / **遺産相続 介護** | Chỉ 3 gợi ý → cụm này sống bằng **browse/suggested, không phải search** (dù view 707K/437K) |
| ⚠️ **介護保険** | 制度 わかりやすい / 保険料 65歳以上 金額 / **法 覚え方** / **法第5条** / **審査会** / **事業計画** / 申請の流れ / 負担限度額認定証 | **Bị dân thi ケアマネ/介護福祉士 chiếm** |
| ⚠️ **要介護認定** | ケアマネ / 調査 / の流れ / 等基準時間 / 申請代行 / **審査会教材事例2** | Gần như toàn bộ là **dân trong nghề** |
| ⚠️ **老人ホーム** | **カジノ** / **歌** / **レクリエーション** / 殺人事件 / 費用(#6) / **川柳** / 体操 | Bị **レク/giải trí cho cơ sở** chiếm |

⚠️ **Google Trends KHÔNG đo được lần này** (HTTP 429 cả 2 lần) → phải đo lại, ghi vào `01_KEYWORD_RESEARCH.md`. Search volume tuyệt đối (Keyword Planner) không có nguồn công khai cho các key này.

## §4 Khán giả + monetization

- **Người chăm chính: 72,2% nữ / 19,5% nam.** Cụm "người chăm 50–59 chăm người 80–89" = **31,4%**. Quan hệ: vợ/chồng ~30% · con ~30% · dâu/rể ~30% (厚労省 国民生活基礎調査; số lấy từ snippet trang chính chủ, nên kiểm lại tay khi cần trích).
- Ngành quảng cáo 老人ホーム tự định nghĩa target B2C = **gia đình 40–70 tuổi, ~60% nữ** (media-radar).
- ⚠️ **Hai khán giả khác nhau tồn tại song song:** con (50代, nữ, lo tiền cho bố mẹ) vs chính người già (65+). Format Shorts kéo về 65+; long-form giải thích chế độ kéo về 50代. → Kênh này **long-form, nhắm 50代**.
- **RPM Nhật theo ngành (6/2025):** 金融・投資 800–1.200円 · **保険・金融商品 700–1.000円** · ビジネス・教育 400–700円 · **健康・サプリ 400–650円**. CPM trung bình toàn sàn 400–600円. ⚠️ Không có nguồn công bố RPM riêng cho 介護/相続 — 保険・金融 là **proxy suy luận**, không phải số đo.
- **Doanh thu thật (ラッコM&A, seller-disclosed) — bằng chứng mạnh nhất:**

| Kênh | Sub | Doanh thu/tháng | Mở | Giá bán |
|---|---|---|---|---|
| シニア lifestyle (暮らし・**老後・お金**), AI voice, 248 video | 11.000 | **TB ¥460.000 / đỉnh ¥660.000** | 9/2025 | ¥1.900.000 |
| 年金・給付金・社会保障, AI voice, 22–30 video | 9.100 | TB ¥50.190 / đỉnh ¥134.000 | 9/2025 | ¥1.240.000 |
| シニア健康 (đối chiếu), 263 video | 32.000 | TB ¥147.286 / đỉnh ¥388.352 | 5/2025 | ¥760.000 |

→ Kênh **老後・お金 11K sub kiếm gấp ~3 lần** kênh **健康 32K sub**. Hướng rất rõ: ngách tiền > ngách sức khỏe về đơn giá.
- **Advertiser dày, tự làm content trong ngách:** SBI証券 (video 家族信託 104K view) · 三井住友信託/三菱UFJ/SMBC · LIFULL介護 & みんなの介護 (老人ホーム 資料請求) · 朝日生命 民間介護保険 · リースバック. media-radar liệt kê sản phẩm nhắm tệp này: **介護施設紹介・住み替え支援・相続相談**.

## §5 Compliance — phát hiện nghiêm trọng nhất

- **15–16/07/2026 YouTube cập nhật chính sách kiếm tiền:** cấm monetize **"AI persona trên chủ đề nhạy cảm — sức khỏe, pháp lý, tài chính, chính trị"** (ví dụ nêu đích danh "AI doctor" chẩn đoán, "AI podcast host" khuyên đầu tư). Nguyên văn JP: 「AI生成のペルソナが人間の専門家を装って」. Nguồn: [yutura 159694](https://yutura.net/news/archives/159694) · [iscle](https://www.iscle.com/web-it/g-drive/youtube/ypp-policy-jul2026.html)
- Cùng đợt: 量産コンテンツ → 「**一般的、または繰り返しの多いコンテンツ**」; nêu tên 「ゆっくり解説 dựa trên copy Wikipedia」 là format nguy cơ cao. Yêu cầu: 「独自の解説や厳密な裏付け、情報源の信頼性」.
- **医学的に誤った情報ポリシー** — hình phạt là **XÓA** content/kênh, không chỉ demonetize ([YouTube Help 13813322](https://support.google.com/youtube/answer/13813322?hl=ja)).
- Nhãn "nguồn y tế đáng tin cậy" chỉ cấp cho tổ chức y tế/giáo dục/công quyền → creator cá nhân **không bao giờ được gắn**.
- **Đợt "収益化停止祭り" 02/2026:** 1 creator phân tích 100+ kênh bị tước — ~99% là reaction/2ch/量産/tái sử dụng. **Không nhắc kênh 年金/健康/シニア giải thích chế độ** → đợt đó ngách này chưa bị đánh.
- **Không tìm thấy case kênh 介護 nào bị demonetize** (không đo được). Nhưng thị trường biết rủi ro: có listing bán kênh senior faceless đặt tiêu đề 【**収益剥奪対策済み**】.

→ **Đối sách của kênh này:** persona 案内役 vô danh, không xưng nghề, không kể trải nghiệm "của tôi"; lớp **原典を見せる** thay cho việc bịa tư cách; GATE 5 ĐIỂM chống 「繰り返しの多いコンテンツ」.

## §6 Chồng lấn với ngách 年金

- Kênh 年金/給付金 lớn **có** phủ 介護: みんなの給付金 (551K) được Gakken mô tả tệp gồm 「親の年金や介護、医療費」; 税金・社会保障教育ch làm 世帯分離×介護保険料 (96.609).
- Kênh 相続/税 lấn **mạnh hơn cả kênh 介護**: スガワラくん 2 video đúng lõi "tiền của bố mẹ" (707K + 437K) — **mỗi video lớn hơn video lớn nhất của mọi kênh 介護 thuần**.
- Chiều ngược lại nhỏ: ケアまど 「年金で老人ホームに入れる？」 51.802; 親ケア.com 「預金も年金も無い両親」 50.536.

| | Ngách 年金/給付金 | **Vùng chồng lấn (chưa ai chiếm)** | Ngách 介護 thuần |
|---|---|---|---|
| Chủ đề | 繰上げ/繰下げ, 加給年金, 給付金申請, 社会保険料 | **年金で施設に入れるか · 世帯分離 · 高額介護サービス費 · 負担限度額 · 医療費控除×介護 · 認知症→凍結 · 家族信託 · 成年後見 · 寄与分** | 要介護認定の流れ, ケアプラン, 介護技術, 施設の種類, 認知症ケア |
| Sub kênh dẫn đầu | 552K–1,72M | **(trống)** | 40K–85K |
| Trần view/video | 1,98M | **51K–707K** | 20K–124K |
| Người xem | 65+ chính chủ + 50代 | **50代 con cái (nữ ~72%)** | 50代 con cái + dân trong nghề |

## §7 Điều KHÔNG đo được (đừng trích như thể đã đo)

1. **Google Trends** — HTTP 429 cả 2 lần → `01_KEYWORD_RESEARCH.md` phải đo lại.
2. Search volume tuyệt đối cho mọi keyword (không nguồn công khai).
3. RPM/CPM riêng cho 介護 hoặc 相続 (chỉ có proxy 保険・金融 700–1.000円).
4. Sub của ゆるっとかいご + 税金・社会保障教育ちゃんねる.
5. **Danh sách video + view của từng kênh** → chưa đo được tần suất đăng thật, độ dài TB, view TB 10 video gần nhất, và **giờ đăng (publishedAt)**. Tần suất duy nhất xác minh: 親ケア.com = hàng tuần (PR chính chủ).
6. Kênh <2 năm đúng ngách 介護×お金 — không tồn tại bằng chứng công khai.
7. Case kênh 介護 bị demonetize.
8. Disclaimer thực tế trong description của các kênh 介護 (WebFetch không đọc được).
9. Đơn giá affiliate 老人ホーム 資料請求/見学.

**Việc phái sinh:**
- ✅ **ĐÃ LÀM cùng ngày** (kết quả ở `01_KEYWORD_RESEARCH.md` §4): đo `publishedAt` + categoryId + rổ tag + độ dài của ケアまど/スガワラくん/みんなの給付金/節約看護師りょう qua YouTube Data API (script `scratchpad/measure_kaigo_bench.py`) → **khóa giờ 19:00 JST, ngày mạnh nhất T6, categoryId 26**. Đồng thời đo được Google Trends rổ 1 qua Chrome (WebFetch 429 nhưng browser + `get_page_text` chạy được, cần đợi ~30s render).
- ⭐ **Phát hiện thêm, quan trọng:** 20 video gần nhất của ケアまど chuyển sang 介護のきほん/ケア/y tế dài 3–6′ → view **43–594**, trong khi series cũ 【介護とお金】 của CHÍNH kênh đó đạt 21K–64K. **Cùng kênh, cùng sub: rời "tiền" sang "cách chăm sóc" thì view sụp ~100 lần.** Đây là đối chứng nội bộ mạnh nhất cho ranh giới trục của kênh mình.
- ⏳ **Còn mở:** Trends rổ 2 (bị throttle) · Trends chế độ YouTube 30d (làm ở GĐ0c từng video) · `publishedAt` của 親ケア.com (`UCg4383PmvAEOZmdM83SlVMw`) + ゆるっとかいご (`UClhDDwxQrV_jhI_sRrUdW7w`) — ưu tiên thấp vì không phải mẫu để bắt chước · **đo lại toàn bảng sau 6–8 tuần**.
