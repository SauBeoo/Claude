# 01_KEYWORD_RESEARCH — 親の介護とお金ノート

> Đo **2026-07-25**. Điểm Trends là **tương đối trong rổ** → có hạn dùng, đo lại khi lên kế hoạch quý sau.
> Bổ trợ: `CHANNEL_BENCHMARK_2026-07-25.md` (view thật + autocomplete + đối thủ).

---

## §1 GOOGLE TRENDS — WEB SEARCH, JP, 12 THÁNG (rổ 1, đo được)

URL: `trends.google.com/trends/explore?date=today 12-m&geo=JP&q=親の介護,介護費用,介護保険,老人ホーム 費用,家族信託&hl=ja`
⚠️ WebFetch bị **HTTP 429** (2 lần, cả 2 phiên) — **phải đo bằng Chrome + `get_page_text`**, và phải đợi ~30s cho widget render. Ghi lại để lần sau khỏi mò.

| Keyword | Điểm TB | Dải | Đọc ra |
|---|---|---|---|
| **介護保険** | **76** | 33–100 | Khổng lồ, gấp ~15 lần các từ còn lại. ⚠️ **NHƯNG intent bị dân hành nghề chiếm** (autocomplete: 法 覚え方 / 法第5条 / 審査会 / 事業計画) → **KHÔNG dùng làm keyword chính của title**; chỉ dùng làm tag phủ + trong thân desc |
| 介護費用 | 5 | 3–6 | Ổn định, không mùa vụ; intent 100% "giảm tiền" |
| 親の介護 | 4 | 3–5 | Ổn định; intent = **xung đột gia đình** (autocomplete) |
| 老人ホーム 費用 | 3 | 2–4 | Nhỏ, ổn định |
| 家族信託 | 3 | 2–4 | Nhỏ nhưng **đang lên** (2025/07: 2 → 2026 nhiều tuần: 4) |

- **Đỉnh của 介護保険:** 2026/06/14 = 100, 2026/01/18 = 97, 2026/07/12 = 95 → nhịp theo **kỳ 通知/改定 (tháng 1 và tháng 6–7)**, đúng lúc giấy 介護保険料決定通知書 về nhà. → **mùa vụ có thật: tháng 6–7 và tháng 1** là 2 cửa sổ đẩy video trục B.
- Vùng lõm duy nhất: tuần 2025/12/28 (Tết) — mọi keyword rơi.
- **Vùng địa lý 「親の介護」 top 5:** 奈良県 · 山口県 · 福島県 · 新潟県 · 滋賀県 (tỉnh có dân số già + con cái ở xa).

## §2 ⭐ BREAKOUT / RELATED QUERIES (giá trị nhất — đây là đề tài có cầu ĐANG TĂNG)

| Từ gốc | Query liên quan (注目 = đang tăng) | Mức tăng | Áp vào đâu |
|---|---|---|---|
| 介護費用 | **家族信託** | **+200%** | Trục A — đề #15 lên hạng, có thể kéo lên nhóm 5 video đầu |
| 介護費用 | **特定入所者介護サービス費** (= chính là 負担限度額認定証) | **+190%** | **Trục B — xác nhận đề #02 đúng thời điểm** |
| 親の介護 | **介護休業給付金** | **+190%** | Trục E — đề #05/#12, cầu đang lên mạnh |
| 親の介護 | 要介護3 · 介護休暇とは | +180% | Trục B/E — long-tail cho desc/tag |
| 介護費用 | 介護認定を受けるには | +160% | Cửa vào cho người mới (video "bắt đầu từ đâu") |
| 介護費用 | **高額介護サービス費とは** | **+70%** | Trục B — đề #13 |
| 老人ホーム 費用 | 軽費老人ホームとは | +200% | Trục C — biến thể giá rẻ, ít ai làm |
| 介護保険 | 介護情報基盤 · 後期高齢者医療資格確認書 | +450% / +400% | Tin chế độ 2026 — hàng cho video timely |
| 家族信託 (人気) | 家族信託 100 · 信託 100 · 信託とは 19 · 家族信託とは 19 · 信託銀行 13 | — | Rổ tag cho video trục A |
| ⚠️ 介護保険 | 子ども子育て支援金 +2050% · 朝日生命介護保険 +130% · 社会保障審議会介護保険部会 +90% | — | **NHIỄU** — không phải tệp mình (chính sách con nhỏ / sản phẩm bảo hiểm / hội đồng) → loại |

**Kết luận §2:** 3 trong 5 đề video đầu (**負担限度額認定証, 家族信託, 介護休業給付金**) đều là **breakout +190–200%** ngay trong 12 tháng qua. Thứ tự đề ở `02_CONTENT_STRATEGY.md` §5 không cần đổi, chỉ **kéo 家族信託 (#15) lên sớm hơn** khi có chỗ.

## §3 AUTOCOMPLETE YOUTUBE (đo 2026-07-25, chi tiết ở benchmark §3)

`親の介護` → 記録 / したくない / **兄弟喧嘩** / ストレス / 費用(#8) / 退職 / **放棄** / **義務**
`介護費用` → **軽減制度** / 平均 / いくら / **確定申告** / **世帯分離** / 医療費控除
`介護 お金` → **お金がない** / 介護資金
`介護離職` → の現実 / **失業保険** / 独身 / 両立支援等助成金
⚠️ Nhiễm tệp nghề: `介護保険` (法 覚え方/法第5条/審査会) · `要介護認定` (ケアマネ/審査会教材) · `老人ホーム` (カジノ/歌/レク/川柳).

## §4 ⭐ ĐO BENCHMARK QUA YOUTUBE DATA API (2026-07-25, 20 video gần nhất/kênh)

Đo bằng token readonly của nenkin. Script: `scratchpad/measure_kaigo_bench.py` (giữ để đo lại).

| Kênh | Sub | GIỜ ĐĂNG | NGÀY | categoryId | Độ dài | #tag | Rổ tag cố định |
|---|---|---|---|---|---|---|---|
| **節約看護師りょう** | 748.000 | **19:00 JST — 19/20 video** | **T6 18/20** | **26** (Howto&Style) | 17–41′ | 9–25 | 年金/厚生年金/国民年金 ~mọi video |
| みんなの給付金・補助金 | 551.000 | **17:48 JST — 20/20** | T3+T6 (10/10) | 29 (Nonprofits) | 14–58′ | 24–75 | 10 tag × 20/20 video |
| 脱・税理士スガワラくん | 1.720.000 | **18:00 (long) + 12:00 (shorts)** — hằng ngày | mọi ngày | 25 (News&Politics) | 17–28′ | 31–43 | 25+ tag × 20/20 |
| 介護の窓口ケアまど | 7.090 | **20:00 — 16/20** | rải | 24→28 | **3–6′** | 6–11 | 6 tag × 20/20 (老人ホーム/高齢者/施設探し/介護/福祉/介護保険) |

### 4 kết luận rút ra (đè lên phần "chưa đo được" của plan)

**(a) GIỜ ĐĂNG 19:00 JST được XÁC NHẬN — không cần đổi.** Toàn bộ 4 kênh đăng trong dải **17:48–20:00 JST**, và kênh hiệu suất cao nhất nhóm so sánh (節約看護師りょう: 748K sub / chỉ 158 video / hit 2,3M) khóa **19:00 JST**. Giả định ban đầu "tệp đi làm → peak 21–22h" **sai**: ngách tiền-senior JP đăng cữ chiều-tối sớm. → bỏ dấu ⚠️ trong `CLAUDE.md` + `upload-schedule.md`.

**(b) THỨ SÁU là ngày mạnh nhất ngách.** 節約看護師りょう **18/20 video đăng T6**; みんなの給付金 dùng T3+T6. → **dồn video mạnh nhất vào T6**.
> ⭐ **ĐO LẠI 2026-07-28 (50 video/kênh thay 20) — kết luận này được củng cố và đã đổi lịch theo:** 節約看護師 **T6 = 48/50 video**, nhịp **1,02/tuần**, median **105.975 view/video**; みんなの給付金 long-form **CHỈ T3 (15) + T6 (16)**, ngày khác 0 long-form. → Lịch chốt lại **T3 + T6, 2 video/tuần cố định** (bỏ T2·T4 và bỏ nhịp 1 video/ngày). Bằng chứng: `.claude/rules/upload-schedule-measure-2026-07-28.md`.

**(c) categoryId = 26 (Howto & Style), KHÔNG phải 27.** Bằng chứng: 節約看護師りょう (cùng tệp 50–60代 tiền, cùng format long-form giải thích + số, hiệu suất/video cao nhất nhóm) dùng **26**. Kênh dùng 24 (ケアまど) đang chết; 29 của みんなの給付金 là lựa chọn lạ của riêng họ; 27 là lựa chọn của nenkin nhưng nenkin **chưa có kết quả chứng minh**. → chốt **26** cho kaigo (đã sửa `upload_api.py`).

**(d) 🔥 ĐỐI CHỨNG NỘI BỘ MẠNH NHẤT — ケアまど tự chứng minh luận điểm của kênh mình.** 20 video gần nhất của họ toàn **介護のきほん/y tế/ケア** dài 3–6′ (訪問入浴, 褥瘡, 傾聴, パーキンソン病) → view **43–594**. Trong khi series cũ **【介護とお金】** của CHÍNH kênh đó: 51.802 · 63.961 · 21.167 view. **Cùng một kênh, cùng lượng sub: chuyển từ "tiền" sang "cách chăm sóc/giảng chế độ" thì view sụp ~100 lần.** → Đây là bằng chứng cứng cho ranh giới trục ở `02_CONTENT_STRATEGY.md` (cấm 介護技術/ケア方法) và cho công thức "tiền + con số cụ thể".

### Việc khác đo được, đáng ghi
- **Khung title thắng:** 節約看護師りょう dùng 【知らないと大損】 ở 7/20 video, còn lại 【2026年新ルール】/【申請忘れ続出】/【衝撃】/【知らないと0円】 → **khối cảnh báo + số tiền + mốc năm** là khung chuẩn ngách. Khớp `03_THUMBNAIL_TITLE_FORMULA.md` §1.
- **Bằng chứng cụm "tiền của bố mẹ" ăn:** 節約看護師りょう làm 「65歳から介護保険料が倍増するってホント⁉」 → **522.575 view**; みんなの給付金 làm 「介護保険料が6万円安くなる裏技の世帯分離」 → topic 介護 nằm trong scope của họ. Ta phải nhanh hơn ở nửa "tiền của BỐ MẸ" trước khi họ lấn tiếp.
- **Channel keywords KHÔNG phải yếu tố thắng:** 節約看護師りょう để **rỗng** (0 ký) mà vẫn 748K sub; スガワラくん chỉ 9 ký; ケアまど 199 ký mà đang chết. → đừng đổ công vào ô đó; đổ vào tag từng video + đề tài.
- **Độ dài:** hit lớn nhất của 節約看護師 là 21′ (2,3M) và 41′ (1,38M) → **18–25′ của mình đúng dải**, flagship có thể kéo 30–40′.
- **Tần suất của kênh hiệu suất cao nhất: ~1 video/tuần** (158 video / 3,5 năm). Thêm một điểm dữ liệu cho ngưỡng phanh ở `08_ANALYTICS_LOG.md` §0.

## §5 RỔ TAG NHẬN DIỆN ĐỀ XUẤT (12 tag, đứng đầu mọi video — luật `youtube-upload-seo.md` §2.4)

```
親の介護とお金ノート, 親の介護, 介護費用, 介護とお金, 介護保険, 老後のお金,
親の介護 お金, 介護 費用 軽減, 高額介護サービス費, 世帯分離, 老人ホーム 費用, 50代 親の介護
```
+ tag đề tài riêng từng video (10–20 tag) → tổng **25–35 tag** (benchmark 9–75).
**3 hashtag cố định cuối 概要欄:** `#親の介護 #介護とお金 #親の介護とお金ノート` + ≤3 hashtag đề tài.
⏳ Chốt lần cuối khi đăng video 01 (kiểm lại bằng autocomplete).

## §6 CHƯA ĐO ĐƯỢC (mở)

1. **Rổ 2 Trends** (介護費用 anchor + 世帯分離 / 高額介護サービス費 / 成年後見 / 介護離職) — Trends throttle widget sau rổ 1 (page load nhưng chart rỗng, không có báo lỗi). Đo lại sau, hoặc đo từng đề lúc viết script (skill `script-kaigo` GĐ0c).
2. **Trends chế độ YouTube Search 30 ngày** (`gprop=youtube&date=today 1-m`) — bắt buộc theo luật §0.5 trước khi chốt title từng video, làm ở GĐ0c.
3. Search volume tuyệt đối (Keyword Planner) — không có nguồn công khai.
4. `publishedAt` của 親ケア.com (UCg4383PmvAEOZmdM83SlVMw) và ゆるっとかいご (UClhDDwxQrV_jhI_sRrUdW7w) — đã tra được channel ID, chưa đo (2 kênh này không phải mẫu để bắt chước, ưu tiên thấp).
