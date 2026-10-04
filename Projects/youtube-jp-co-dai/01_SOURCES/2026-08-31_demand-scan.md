# PHÉP ĐO CẦU ĐỀ TÀI — co-dai, 2026-08-31 (chọn đề cho video 27–29)

> **Cách đo:** YouTube Data API `search.list` · `regionCode=JP` · `relevanceLanguage=ja` ·
> `order=viewCount` · `publishedAfter` = 365 ngày · **`videoDuration=long` (>20′)** → rồi
> `videos.list` lấy view + tuổi. Script: `scratchpad/scan_demand.py` (token co-dai).
> **45 keyword đã quét.**

## 🔴 ĐỌC TRƯỚC — ĐÂY KHÔNG PHẢI GOOGLE TRENDS

Phép đo này trả lời **「đề này đã có video ăn view chưa」**, KHÔNG trả lời 「bao nhiêu người
search」 ⇒ **TARGET_QUERY vẫn phải đo Trends ở Bước 0 lúc viết script**
(`youtube-upload-seo.md` §0.5). Bài học video 25 v1: 15 keyword quanh địa nhiệt đều ~0 trên
YT Search dù đề tài hay.

### ⭐⭐ CẬP NHẬT CÙNG NGÀY — ĐO TRENDS ĐƯỢC **KHÔNG CẦN CHROME** (pytrends)

Bản đầu của file này ghi *"session không có Chrome tool nên chưa đo được Trends"*. **Sai — đo
được.** `pip install pytrends` rồi gọi thẳng; chỉ có **một** bẫy:

```python
py = TrendReq(hl="ja-JP", tz=-540, timeout=(10, 30))   # ⛔ ĐỪNG truyền retries/backoff_factor
```
Truyền `retries=` thì pytrends dựng `urllib3.Retry(method_whitelist=...)`, mà **urllib3 v2 đã bỏ
tham số đó** ⇒ `TypeError: Retry.__init__() got an unexpected keyword argument 'method_whitelist'`
ở **mọi** lời gọi. Nhìn như "Trends chặn", thực ra là lỗi thư viện.
Script: `scratchpad/trends.py` (interest_over_time + related_queries, anchor bridging).

📌 Skill `trend-keywords` mô tả đường **browser + get_page_text**; đường pytrends này **rẻ hơn nhiều**
và đọc được cả `related_queries`. ⚠️ Nhưng nó vẫn là API không chính thức — bị 429 thì quay lại browser.

🔴 **Và related_queries là bước KHÔNG được bỏ.** Volume một mình không đủ để loại nhiễu tên riêng:
`灰` đo **mean 52,3 / max 100** (cao gần bằng anchor `フライパン`) nhưng related toàn **黛灰 (VTuber
Nijisanji) · 灰宮先輩 · コナン灰原哀 · 灰谷兄弟 · エルデンリング遺灰 · 灰と幻想のグリムガル**. Nếu chỉ
đọc con số thì đã đưa `灰` lên title.

**Số đo được (thang kênh, bridge qua `フライパン` = 585 của video 22):**

| keyword | mean (rổ) | ≈ thang kênh | đọc |
|---|---|---|---|
| **換気扇** | **18,1** (31/32 điểm >0) | **≈137** | ⭐ mạnh hơn mọi TARGET_QUERY kênh từng dùng trừ 熱中症(296)/フライパン(585). So: `排水口 掃除` 37 · `すだれ` 42 · `障子` 37–55 |
| 重曹 | 12,9 | ≈130 | gần bằng 換気扇 — dùng làm A2 |
| 換気扇 掃除 | 4,5 | ≈34 | related top #1 của 換気扇 (=100) |
| 油汚れ | 3,7 | ≈28 | related rỗng (volume quá nhỏ) |
| レンジフード | 2,3 | ≈17 | yếu hơn 換気扇 8× — đừng dẫn bằng từ này |
| セスキ · 換気扇 油 | 0,7 · 0,6 | ≈1 | quá nhỏ, chỉ để làm tag |

**Related của `換気扇` (INTENT):** `換気扇 掃除` 100 · `換気扇の掃除 油汚れ` 30 · `換気扇 外し方` 25 ·
`キッチン換気扇 掃除` 15 ⇒ **INTENT = やり方**, sạch, 0 modifier `効果`.
⚠️ Nhánh phụ đáng biết: `トイレ換気扇` 30 · `お風呂/浴室換気扇` 15/14 · rising `屋根裏換気扇` · `床下換気扇`
⇒ 「換気扇」trần bị chia sang quạt toilet/phòng tắm/gác mái. **Title phải khóa nhánh bếp bằng chữ 油.**

**Hai bẫy của phép đo này, cả hai đã dính thật trong lượt quét:**

1. ⚠️ **view MAX to KHÔNG bằng cầu đúng tệp.** Phải đọc TITLE của top, nếu không sẽ chọn đề
   theo một cụm khán giả khác hẳn. Sáu ca bị loại chính vì lý do này (bảng §2).
2. ⚠️ **`n` nhỏ có HAI cách đọc ngược nhau.** `n=3` + MAX 245K = **thị trường long-form trống
   = cơ hội**; `n=0–1` + MAX thấp = **không có cầu**. Đừng gộp hai cái.

## 1. ✅ ĐỀ SỐNG — cầu thật, đúng tệp

| đề | view MAX | median | bằng chứng đúng tệp (title của top) |
|---|---|---|---|
| **換気扇/レンジフードの油** | **245.647** | 13.710 | `【大掃除前必見】レンジフードの油汚れが一番落ちる洗剤をプロが判定！最強洗剤決定` 245K (intent `最強` ✅) · `油汚れはなぜ落ちる？仕組み` **chỉ 470 view ⇒ intent「なぜ」GẦN NHƯ TRỐNG** · query hẹp `換気扇 油 落とし方` chỉ **n=5 long-form/năm** |
| **干し柿・渋柿** | 3.045.366 (nhiễu) | 26.619 | `甘柿と渋柿の違い／干し柿が甘くなる理由` **115K** (đúng format giải thích cơ chế) · `築160年の古民家の秋｜干し柿作り` 277K · `渋柿に日本の嫁が魔法を→NYタイムズも絶賛` 279K · có cả 朗読民話 49K. ⚠️ MAX 3,0M là nhóm nhạc M!LK — bỏ |
| **包丁と砥石** | 351.119 | **57.617** | `プロが伝授する包丁の研ぎ方！5つのポイント` 232K · ⭐ `荒砥を使おう！自作なら約200円で作れます…秘訣をお伝えします` **135K** (đúng khuôn 数百円+自作 của kênh) · `Japanese Master Knife Sharpener` 313K |

## 2. ❌ ĐỀ CHẾT / NHIỄU — đã loại, đừng đề xuất lại mà không đo lại

| keyword | số đo | vì sao loại |
|---|---|---|
| 樟脳 | MAX **34** | Chết hẳn. (Ý tưởng "Nhật từng số 1 thế giới về long não" hay nhưng **không ai tìm**) |
| 桐たんす | MAX 3.571 | top là DIY sơn lại tủ |
| 衣替え | MAX 434.449 | **NHIỄU**: comedy (タイムマシーン3号), VTuber "衣替え" = đổi trang phục avatar |
| たんす 虫 対策 · 米びつ 虫 · タオル 臭い · 畳 手入れ カビ | **0 long-form** | không có cầu long-form |
| **畳** | MAX 1,8M · median **402.168** ← cao nhất cả bộ | **NHIỄU NẶNG NHẤT**: 「畳」bị đọc là ĐƠN VỊ DIỆN TÍCH → `6畳の山小屋` `2畳小屋暮らし` `1畳の家` `40畳の大豪邸`. Cầu 0 cho 畳の手入れ |
| 七輪 | median 180.916 | **NHIỄU**: top toàn `ベランダ酒場 深夜の1人飲み` nướng thịt/BBQ/居酒屋 → cầu là ăn uống, không phải 防災/昔の道具 |
| ろうそく | MAX 3,9M | **NHIỄU**: 東海オンエア/Fischer's, **ローソク足** (nến chứng khoán), ASMR |
| 停電 | median 129.035 | **NHIỄU**: hoạt hình trẻ em BabyBus 1,2M, vlog Canada, tin Nga/Ukraine, prepper Mỹ. Cụm thật là 防災 (そなえるTV) = **tệp khác** |
| 台風 対策 家 | MAX 204.065 | top là **tin thời sự ABCテレビ** + vlog 沖縄/宮古島 |
| さつまいも 保存 | MAX 685.617 | cầu thật là **栽培/レシピ** (リュウジ, カーメン君, 栽培ガイド), không phải 保存 |
| 切り株 · 井戸水 | 5,5M · 949K | bushcraft/DIY **nước ngoài** (dugout under stump, đào giếng) |
| 部屋干し · 生乾き 臭い · 洗濯物 臭い | median 2.416 / **123** / 1.779 | **trục 洗濯 chết**: top toàn 2chガルちゃんまとめ + review nước giặt/除湿機 |
| 洗濯機 カビ | MAX 221.939 · median 674 | top là **review máy giặt 2026**; cụm đúng tệp chỉ 1 video (163K), phần còn lại 1.400–4.000 |
| ダニ 布団 | median 620 | top toàn **review máy hút bụi** → intent mua đồ |
| 梅干し · ぬか漬け | median 87.655 · 47.379 | cầu THẬT nhưng **sai mùa** (梅干し = tháng 6) / **trùng video 16** (漬物・塩の段) |
| こたつ · 薪ストーブ · 火鉢 | median 314K / 182K / 5.172 | mùa 11–12月 (quá sớm) · nhiễu 車中泊/キャンプ/猫vlog |
| 落ち葉 腐葉土 | MAX 199.372 · median 657 | 1 kênh 園芸 lớn chiếm đỉnh, phần còn lại chết |
| 窓 結露 | MAX 65.590 | mùa 11–12月, chưa tới |

## 3. Peer `昔の人の知恵` — quét cùng ngày (`bench_channels.py`)

sub 16.100 · 35 video · **189 sub/ngày · 25.002 view/ngày** · median dài **25′** · cat 27 · tag median 59
🔴 **XU HƯỚNG: 5 video MỚI median 6.084 v/ngày vs 5 video TRƯỚC 743** — peer đang tăng tốc ~8×.

Peer đang dồn vào **năng lượng/kiến trúc**: `中庭住宅` 47K/**18.616 v/d** · `風力タービン` · `水力発電機
8.000円` · `地中熱パイプ` 194K · `土と水だけで空気を6〜8℃冷やす壁`.
⚠️ **Đã thử nhánh này ở video 25 v1 và THẤT BẠI** — 15 keyword kiến trúc/địa nhiệt đều ~0 cầu
JP, và user chê thiếu VẬT cầm nắm được. **Đừng bám peer ở nhánh này nếu chưa đo Trends.**

## 4. Ràng buộc luật trục lúc chọn (đối chiếu 2026-08-31)

- Video 26 = 🏠 **家の手入れ** ⇒ video 27 **phải khác** trục này (`02_CONTENT_STRATEGY.md` §3.1).
- 🐜 害虫 = **8/26 ≈ 31% > trần ~1/4** ⇒ đang QUÁ, tránh thêm.
- 🔥 signature lần cuối = video **25** ⇒ chưa tới hạn (~4 video/lần).
- Trục **ít dùng nhất**: 🥬 食品保存 (1 lần, video 08) · 💡 節約 (1 lần, video 07).
- Tháng 9 **không có đề mùa nào vừa mạnh vừa có cầu đo được** (防災の日 1/9 nhiễu tệp · 秋雨→洗濯 chết ·
  新米→0 long-form) ⇒ đề evergreen là lựa chọn đúng cho slot đầu tháng 9.

## 5. Kiểm trùng nội bộ đã làm

**換気扇の油 vs video 22 (フライパンがくっつく)** — cùng hiện tượng 油の熱重合, nhưng **VAI TRÁI NGƯỢC**:
ở 22 lớp màng polymer là thứ **cần nuôi** (油ならし・金属石けん・南部鉄器の金気止め); ở quạt hút nó là
**kẻ thù** (dầu hóa nhựa nên nước rửa bát vô dụng). Và `grep 重合` trong `22_..._TTS.md` = **0** — từ này
chỉ nằm ở phần nguồn của bản `.md`, **chưa bao giờ vào lời đọc** ⇒ khán giả chưa nghe.
⇒ **KHÔNG trùng**, và còn callback được sang 22 (tốt cho session watch).
