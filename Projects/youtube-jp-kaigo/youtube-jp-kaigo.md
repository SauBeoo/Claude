# youtube-jp-kaigo — 親の介護とお金ノート (JP, con cái 45–65)

> Folder-note tổng quan project. Lập **2026-07-25**. Vault tri thức: `SecondBrain/10_Projects/youtube-jp-kaigo/`.
> **Tên kênh CHỐT (user, 2026-07-25): 「親の介護とお金ノート」.**
> Trạng thái: **SETUP T0** — còn chờ ① Gmail mới + Chrome profile ② chốt giọng TTS ③ đo giờ đăng thật.

## 1. Vì sao ngách này (số đo thật 2026-07-25)

Nguồn đo: `returnyoutubedislikeapi.com` (viewCount thật, 38 video) · `socialcounts.org` (YouTube Data API) · `suggestqueries.google.com` (autocomplete YouTube JP) · 厚労省 国民生活基礎調査 · ラッコM&A. Chi tiết đầy đủ: **`CHANNEL_BENCHMARK_2026-07-25.md`**.

1. **Cầu khổng lồ, cung lệch tệp.** 653万 người Nhật đang chăm bố mẹ (1/20 dân số); ビジネスケアラー 262万→318万 (2030), thiệt hại kinh tế ~9兆円 (METI). Chi phí bình quân **542万円/người** (一時 47,2万 + 9,0万/tháng × 55 tháng — 生命保険文化センター 2024).
2. **Lỗ trống thật:** kênh đúng ngách 介護×お金 lớn nhất chỉ **7K–45K sub**. 親ケア.com ~40K sub với **864 video** mà view 42–1.276/video (format 講座 đã chứng minh CHẾT). 介護の窓口ケアまど chỉ 7.090 sub nhưng series 【介護とお金】 đạt 51.802–63.961 view = **view/sub tốt nhất cả ngách**. **Không kênh nào >100K sub chuyên trị cụm này.**
3. **Cụm ăn nhất KHÔNG phải 介護費用.** 制度解説 thuần trần 20K–120K; cụm "tiền của bố mẹ" cao hơn 1–2 bậc: 親の預金を生前に引き出す **707.712** · 親族後見人が家族崩壊 **437.198** · 医療費控除 **193.882** · 認知症→資産凍結 **104.436** (SBI証券 tự làm). Kẻ đang ăn là 脱・税理士スガワラくん (1,72M sub) — kênh thuế tạt ngang rồi đi.
4. **Intent người search là XUNG ĐỘT, không phải chế độ.** Autocomplete `親の介護`: 記録 → したくない → **兄弟喧嘩** → ストレス → 費用 (#8) → 退職 → **放棄** → **義務**.
5. **Đơn giá cao nhất mảng senior.** RPM 保険・金融 700–1.000円 vs 健康・サプリ 400–650円. M&A seller-disclosed: kênh 老後・お金 faceless **11K sub → ¥460.000/tháng** trong khi kênh 健康 **32K sub → ¥147.000/tháng**. Advertiser dày: SBI証券, 信託銀行, 老人ホーム紹介ポータル, 民間介護保険, リースバック.
6. **Chi phí học ngách ≈ 0** — dùng lại nguyên pipeline của nenkin/health (ảnh tĩnh + slide + VOICEVOX + upload_pack + dashboard).

## 2. Concept kênh

- **Lời hứa lõi:** 「親のお金は、親のために使う。そのために、いま何を、どこで、いつ手続きするか。」
- **Công thức mỗi video:** (a) một khoản tiền **sắp mất / lấy lại được** mà người ta ĐANG search × (b) **con số thật của MỘT gia đình cụ thể + trang tài liệu gốc chiếu lên màn hình + 1 hành động có địa chỉ & hạn**.
  - (a) → được related-rail đặt cạnh video triệu view của kênh thuế/給付金.
  - (b) → moat: 親ケア.com giảng chế độ, スガワラくん nói khái quát — **không ai tính hộ**.
- **Format:** faceless, 案内役 vô danh + dàn cast gia đình hư cấu, ảnh tĩnh + diagram + pan, 18–25 phút.
- **5 trục nội dung:** A 凍る前のお金 · B 取り戻せるお金 · C 施設とお金 · D 兄弟・義務・相続 · E 自分の家計を守る → `02_CONTENT_STRATEGY.md`.
- **Định vị 1 câu:** 「制度を教える人じゃない。あなたの実家の数字を一緒に計算する人。」

## 3. Trạng thái chốt

1. ✅ **Tên kênh** (2026-07-25): 「親の介護とお金ノート」 — keyword 親の介護 + お金 nằm thẳng trong tên.
2. ✅ **Phạm vi**: 「親のお金」 mở rộng 5 trục (không bó ở 介護費用) — user chốt sau khi xem bảng trần view.
3. ✅ **Persona**: 案内役 trung tính vô danh + cast gia đình hư cấu (an toàn nhất với policy AI-persona YMYL 07/2026).
4. ✅ **Nhịp**: 5 video đầu cách 2–3 ngày → sau checkpoint tuần 4 lên **1 video/ngày**, có GATE 5 ĐIỂM + ngưỡng phanh (`08_ANALYTICS_LOG.md`).
5. ✅ **Giọng TTS (user chốt 2026-07-26)**: **VOICEVOX No.7 / ノーマル (id 29) / speed 0.95 / intonation 1.1** — demo duyệt `00_VOICE_TEST/demo_29_no7_normal.wav`. **Hệ số đo thật: 315 ký/phút** (4.025 ký → 12,79′ với gap 0.6/1.1) → 18′≈5.650 ký · 25′≈7.850 ký. (WhiteCUL 292 ký/phút — cân nhắc rồi loại.)
6. ✅ **Lịch đăng**: **19:00 JST cố định** (đo API 2026-07-25) · ⭐ **T3 + T6, 2 video/tuần cố định** (SỬA 2026-07-28 sau đo lại 50 video/kênh: 節約看護師 T6 48/50 & 1,02 video/tuần & median 106K view; 給付金 long-form chỉ T3+T6 → **bỏ nhịp 1 video/ngày** và xoá hàm `_kaigo_slots()`). T6 = slot mũi nhọn. Giả định "peak 21–22h vì tệp đi làm" đã bị số liệu phủ nhận (4/4 kênh benchmark đăng 17:48–20:00). categoryId chốt **26**. Chi tiết: `01_KEYWORD_RESEARCH.md` §4. Đo lại bằng `tools/measure_bench.py` mỗi 6–8 tuần.
7. ⏳ **Gmail + Chrome profile riêng**: cần user cấp 1 Gmail MỚI (cấm dùng chung với 6 kênh kia — tầng liên đới là Gmail, theo `channel-browser.md`).
8. ⏳ **Google Cloud project riêng** → `credentials/` → token cho `upload_pack`/`analytics_report`.

## 4. ⚠️ Compliance riêng ngách này (YMYL kép: tài chính + pháp lý gia đình)

- Không tư vấn cá nhân/pháp lý cụ thể; luôn 「一般的な制度の説明です」.
- **Hedge 自治体 là mặc định** — mọi con số 介護 lệch theo địa phương + 所得段階.
- **KHÔNG nói y tế** về 認知症 (chỉ hệ quả TIỀN + thủ tục) — medical misinformation policy phạt bằng XÓA.
- Persona **cấm** xưng 専門家/FP/介護アドバイザー/ケアマネ/弁護士/元役所職員; cấm 「私も親を介護していて」. Lớp bù uy tín = **原典を見せる**.
- Từ nhạy ở title/thumbnail: ngách này dễ trượt vào 死/介護殺人/虐待/共倒れ → thay 詰む/追い詰められる/家族崩壊/凍る/取り逃す. Thân bài giữ nguyên độ đanh (`youtube-compliance.md` §0.1).
- KHÔNG tick altered/synthetic (ảnh tĩnh + TTS + thumbnail AI = production assistance).

## 5. Cấu trúc tài liệu

| File | Nội dung |
|---|---|
| `youtube-jp-kaigo.md` | Folder-note này |
| `CLAUDE.md` | ✅ Rule riêng project (persona · cast · 5 trục · GATE · visual · YMYL) |
| `00_CHANNEL_BIBLE.md` | ✅ Bible định vị (lời hứa · khán giả · signature craft · KHÔNG-LÀM) |
| `01_KEYWORD_RESEARCH.md` | ⏳ Trend JP (Trends 429 lúc đo lần 1 — phải đo lại) + autocomplete đã có |
| `02_CONTENT_STRATEGY.md` | ✅ **Trái tim** — ma trận 5 trục + gate + 15 đề đầu có bằng chứng cầu |
| `03_THUMBNAIL_TITLE_FORMULA.md` | ✅ Công thức title/thumbnail + sổ xoay khuôn |
| `CHANNEL_BENCHMARK_2026-07-25.md` | ✅ Số đo ngách (9 kênh + 22 đề có view thật + autocomplete + RPM + policy) |
| `08_ANALYTICS_LOG.md` | ✅ Sổ đo tuần + ngưỡng checkpoint/phanh |
| `03_SCRIPTS/` | (chưa) kịch bản |
