# 26 — 介護保険料の段階は「世帯」で決まる｜同居で年3万7,900円

> 🔴 **SỬA LỚN 2026-09-16 — trục bài đã đổi.** Bản v1 dựng hook trên 中村 vượt線148万
> (第3→第6, 差49,600) rồi gán nguyên nhân cho 「世帯」 — **SAI**: 第6段階 đòi 本人が課税,
> con gái dọn về không đụng tới nó. Và 第1〜5 KHÔNG phải 「世帯全員非課税」 (chỉ 第1〜3).
> Bản v2: 中村 giữ 年金147万 (非課税, 第3段階) · con gái đi làm dọn về → **第5段階** →
> **39,500 → 77,400 = 差 37,900円/năm ≒ 月3,158円**. Một cơ chế, một con số, title giữ nguyên.
> Beat 「5千円の税金が5万円近い保険料を連れてきた」 **đã cắt** (nó là trục của video 14).

### 対象者
年齢: 65+
就業: 不問
推定カバー率: 74.9%

> T-GATE (`02_CONTENT_PLAN.md` §T-GATE) — chấm ngày 2026-09-15:
> **T1** ✅ 65歳以上の第1号被保険者, 就業 不問 · **T2** ✅ 7月に**介護保険料決定通知書が自動で届く**,
> và 段階 bị **tự quyết lại mỗi năm** dù không làm gì · **T3** ✅ 7月通知 / 10月本徴収 ·
> **T4** ✅ 6,225円 · 39,500円 · 89,100円 (đã verify) · **T5** ✅ trụ ③ 税・社会保険料 ·
> **T6** ✅ フクロウ 10K view/2,3 ngày · さゆり 50K · 完全攻略 96K (`01_SWIPE_TITLES.md`)

---

## SỔ XOAY KHUÔN (chống inauthentic)

| | video 24 | video 25 | **video 26** |
|---|---|---|---|
| khuôn mở bài | ②事件型 | ①GAIN-REVEAL | **④対決型** (hai người cùng lương hưu, khác tiền đóng) |
| khuôn 計算タイム | thang 3 bậc | A-vs-B đối chiếu | **一人増えたら** (cùng một người, trước/sau khi世帯 đổi) |
| closer | 行動プラン | ○×クイズ | **セルフチェック 3問** |
| trụ | ② | ③ | ③ |

⚠️ Trụ ③ hai video liền — chấp nhận có chủ ý: đây là **trả teaser** của video 25
(「介護保険料は下がる？上越の中村さん・一年でいくら変わる」), và mùa 本徴収 tháng 10 chỉ mở
trong tháng 9. Video 27 bắt buộc đổi sang trụ ① hoặc ②.

---

## FACT SHEET — verify 2026-09-15, TRƯỚC khi viết chữ nào

| # | Fact | Số | Nguồn | 原典ショット |
|---|---|---|---|---|
| 1 | 第9期(令和6–8年度) 全国平均 第1号保険料 | **月6,225円** (第8期 6,014円, +3,5%) | 厚労省「第9期計画期間における介護保険の第1号保険料について」 | ✅ **có sẵn** `genten_kaigo*.png` (dùng lại từ video 25, 3 thẻ) |
| 2 | 第9期から標準段階が **9→13段階** | 13段階 | 厚労省 介護保険最新情報 Vol.1190 | ⏳ cần chụp |
| 3 | 🔴 **SỬA**: 第**1〜3**段階 = 世帯全員が住民税非課税<br>第4・5 = 本人非課税 **だが世帯員に課税者あり**<br>第6〜 = 本人が課税 | — | 新宿区「介護保険料の決まり方」 (đối chiếu chéo 延岡市 第9期段階表 — hai nguồn độc lập khớp nhau) | ⏳ cần chụp ⭐ **thẻ đắt nhất của bài** |
| 4 | 第1〜5段階の thước = **課税年金収入額＋その他の合計所得金額**<br>第6段階〜 = **本人の合計所得金額** | — | 新宿区 (同上) | ⏳ cùng thẻ với #3 |
| 5 | 段階数・乗率は **市区町村ごとに違う** | 新宿区 **18段階**, 基準額 年79,200円 (月6,600円) | 新宿区「第9期の保険料設定の考え方」 (cùng trang với #2) | ⏳ |
| 6 | 段階の判定材料 = ①基準日4/1の世帯 ②その年度の住民税課税状況 ③前年の合計所得金額・課税年金収入額 | — | 新宿区 (chú ◎「世帯状況」は年度当初の4月1日現在, cùng trang #3) | ⏳ cùng thẻ với #3 |
| **7** | ⭐ **MỚI** — 上越市 第9期 段階表 (17段階): 第3段階 **39,500円** · 第4 69,700円 · **第5 77,400円** · 第6 **89,100円** | — | 上越市「介護保険料」<br>`https://www.city.joetsu.niigata.jp/site/kaigo/hokenryou.html` (đã curl + grep HTML thật 2026-09-16) | ⏳ cần chụp ⭐ **thẻ chở con số của bài** |

**② 計算 tự (ghi およそ + show công thức trong bài):**
- 中村さん 年金147万 · 独居 · 世帯非課税 ⇒ **第3段階 = 39,500円**
- 娘（課税）が同一世帯に ⇒ 本人はまだ非課税だが世帯員に課税者 ⇒ 課税年金収入額147万 >
  **826,500円** ⇒ **第5段階 = 77,400円**  (cả ba số lấy từ bảng 上越市, fact #7)
- 77,400 − 39,500 = **37,900円/năm** · 37,900 ÷ 12 ≒ **3,158円/月**
  → hai phép tính lại từ số đã có trên bảng, không phải số mới.
- ⚠️ 39,500 và 89,100 là số cast đã chốt ở script 14 — **vẫn khớp bảng 上越市**, không đổi.
  89,100 (第6段階) **không dùng trong bài này** vì nó đòi 本人が課税.

**③ ballpark phụ thuộc 自治体 — BẮT BUỘC hedge trong thoại:**
- 全国平均 6,225円 → 「全国平均です。お住まいの市区町村で変わります」
- 上越市の非課税限度額 148万円 → 「3級地の場合です。級地で違います」
- 39,500 / 77,400 → 「上越市の場合です。お住まいの市区町村で金額が違います」
- 826,500円 → 「第4段階と第5段階の分かれ目です。国の標準の線です」
- 18段階/13段階 → 「新宿区は18段階。お住まいの市区町村で段階の数が違います」

⚠️ **RÀ LẠI TRƯỚC NGÀY ĐĂNG:** 第9期 kết thúc 令和8年度 (tức năm nay) — 第10期 sẽ công bố
基準額 mới. Nếu công bố trước 09-17 thì phải cập nhật số #1.

### ⛔ KHÔNG ĐƯA VÀO BÀI (đã cân và loại)

- **世帯分離 như một "mẹo" hạ phí** — đây là thủ tục 住民票 có điều kiện thực tế (sinh kế
  riêng), **không phải công tắc**. Và nó kéo theo: 高額介護サービス費 có trần **theo hộ**,
  補足給付(食費・居住費) bị loại nếu 配偶者が課税 hoặc tài sản vượt mốc — tức có thể **lỗ
  ròng**. Bài chỉ nói **một câu** rằng nó không phải việc làm vì tiền bảo hiểm, rồi trỏ cửa sổ.
- **医療費控除で段階が下がる** — ⛔ SAI, và nhiều video trong ngách nói sai chỗ này.
  医療費控除 là **所得控除**, nó hạ 課税所得 chứ **không hạ 合計所得金額** — mà 段階 xét
  合計所得金額. Bài **nói thẳng điều này** như một 誤解 để tạo khác biệt.

---

## HÀNG XÓM MỤC TIÊU (`youtube-suggested-growth.md` §1)

| video hàng xóm | vì sao mình là next-watch |
|---|---|
| **フクロウ**「介護保険料を安くする」 (10K view/2,3 ngày) | Họ trả lời 「安くする方法」. Mình trả lời câu đứng ngay trước nó: **「そもそも、あなたの段階はどう決まったのか」** — không biết cái đó thì mọi "cách" đều mù |
| **カメ先生**【◯◯の方へ】+ 通知書 | Cùng khuôn "tờ giấy đến tay"; mình cho xem **đúng ô 段階** trên 決定通知書 |
| Video 25 của chính kênh (天引きと手取り) | Đã hứa teaser 「上越の中村さん・一年でいくら変わる」 ⇒ đây là **tập trả lời**, end screen nối thẳng |

---

## Đo keyword — YouTube Search 30d, JP (2026-09-15, pytrends)

| keyword | YT 30d | ghi chú |
|---|---|---|
| **年金** | **81,97** | ⭐ từ dẫn, đứng đầu title |
| **介護保険料** | 0,12 | ⚠️ gần 0 trên YT search — **KHÔNG đứng đầu title**, nhưng là thực thể chính của bài ⇒ vào vị trí 2 + tag + thumbnail |
| 住民税非課税 | 0,47 | tag |
| 給付金 | 14,81 | không thuộc bài này, không nhét |

📌 `介護保険料` volume gần 0 nghĩa là **bài này không sống bằng search** — nó sống bằng
suggested từ hàng xóm フクロウ. Đúng lý do phải làm end screen/thẻ ở video 25.

---

### Title CHỐT

```
年金は同じなのに介護保険料が年3万7千円違う理由｜段階は世帯で決まります
```

36 ký · `年金` @1 (top-1 đo được) · `介護保険料` @9

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ | `年金は同じなのに介護保険料が年3万7千円違う理由｜段階は世帯で決まります` | 36 | 年金@1 · 介護保険料@9 | keyword top-1 dẫn + **nghịch lý có số** |
| **A2** | `介護保険料の段階は世帯で決まります｜7月の決定通知書、ここだけ見てください` | 36 | 介護保険料@1 | đổi keyword dẫn sang thực thể của bài — thử xem lọc tệp có thắng volume không |
| **A3** | `【65歳以上の方へ】同居のお子さんが働いていると、介護保険料は年3万7千円上がります` | 39 | — | đổi kiểu hook: **chip 対象 + ca cụ thể**, khuôn カメ先生 |

### 3 THUMBNAIL A/B (khuôn TELOP, `ab-3title-3thumb.md` §3.1)

Chữ **giống nhau cả 3 bản**:

| khối | chữ |
|---|---|
| chip 対象 / banner navy | `65歳以上の方へ` |
| dòng 2 | `介護保険料は世帯で決まる` (`世帯` đỏ) |
| **HERO** | `年3万7千円` |
| dải đỏ đáy | `同居した、それだけで` |

T1 baseline khuôn TELOP · T2 đổi 1 biến hình (nền bàn bếp) · T3 khuôn カメ先生 (0 người, navy).

### Tên file upload

```
kaigo-hokenryo-dankai-setai-3man7sen.mp4
```

### 概要欄 — 3 dòng đầu

```
年金額が同じでも、介護保険料は年3万7,900円違うことがあります。段階が「世帯」の住民税で決まるからです。
7月に届いた介護保険料決定通知書の「段階」の欄を見ながら、何がその段階を決めたのかを一つずつ確かめます。
上越市の中村さん（71歳）に働く娘さんが同居したら第3段階から第5段階へ。39,500円が77,400円になる計算を実額で追います。
```

### 概要欄 — mô tả đầy đủ

```
年金額が同じでも、介護保険料は年3万7,900円違うことがあります。段階が「世帯」の住民税で決まるからです。
7月に届いた介護保険料決定通知書の「段階」の欄を見ながら、何がその段階を決めたのかを一つずつ確かめます。
上越市の中村さん（71歳）に働く娘さんが同居したら第3段階から第5段階へ。39,500円が77,400円になる計算を実額で追います。

制度を読むチャンネルではありません。あなたの数字を計算する研究室です。

【目次】
00:00 年金は同じなのに、保険料だけが倍
01:19 7月に届く「介護保険料決定通知書」
01:57 段階を決める三つ（4月1日の世帯・その年度の課税状況・前年の所得）
02:33 第1〜第3段階の条件はたった一行「世帯全員が住民税非課税」
03:19 第5段階と第6段階のあいだで物差しが入れ替わる
03:59 原典：新宿区「介護保険料の決まり方」
04:07 計算タイム：上越市の中村さん（71歳・年金147万円・第3段階 年3万9,500円）
04:58 娘さんが同居したら、三つの扉が閉まる
05:54 課税年金収入額が826,500円超なら第5段階 年7万7,400円
06:26 原典：上越市「介護保険料」第9期の段階表
06:59 ここで、ひとつだけお願いです
07:31 よくある誤解：医療費控除では段階は下がりません
08:12 本当に動くものは三つ（前年の所得・世帯の課税状況・減免制度）
09:32 最後に、数字を三つだけ（第9期の全国平均 月6,225円／9段階→13段階／新宿区は18段階）
10:19 今日の研究ノート ①〜⑤
11:31 中村さんは、どうされたか
12:18 次回予告：税の扶養に入れていたら、どちらが大きいのか

介護保険料の段階は、ご自分の所得だけでは決まりません。基準日である4月1日時点の住民票の世帯、その年度の住民税の課税状況、そして前の年の所得。この三つで決まります。第1段階から第3段階に入る条件は「世帯全員が住民税非課税であること」。ご自分が非課税でも、同じ世帯に課税されているかたが一人でもいらっしゃれば、この三つには入れません。さらに第5段階と第6段階のあいだでは物差しそのものが取り替わり、第1〜第5段階は課税年金収入額とその他の合計所得金額を足した額で、第6段階からは本人の合計所得金額だけで見ます。同じ「所得」という言葉でも、中身が違います。

今回は、新潟県上越市にお住まいの中村さん（71歳・年金147万円）を例に、働く娘さんが同居した場合に第3段階から第5段階へ上がり、年3万9,500円が年7万7,400円になる過程を、上越市の段階表そのものを見ながら計算しました。差は年3万7,900円、ひと月あたりおよそ3,158円です。

※本動画は令和8年9月時点の情報です。段階の数・金額・軽減制度はお住まいの市区町村によって変わります。ご判断の前に、必ずお住まいの市区町村の介護保険担当窓口でご確認ください。

音声: VOICEVOX:雀松朱司

#年金 #年金生活 #老後のお金
```

### Pinned comment

```
ご視聴ありがとうございます。当研究室の、今日のノートです。

【研究ノート】
① 介護保険料の段階は、①基準日4月1日の世帯 ②その年度の住民税の課税状況 ③前年の所得、の3つで決まります。
② 第1段階から第3段階までは「世帯全員が住民税非課税」が条件です。ご自分が非課税でも、同じ世帯に課税の方が一人いれば、この3つには入りません（第4・第5段階に上がります）。
③ 第6段階からは「本人が課税」。物差しも変わり、第1〜5段階は課税年金収入額＋その他の合計所得、第6段階からは本人の合計所得金額で見ます。上越市の例では第3段階39,500円が第5段階77,400円、差は年37,900円でした。
④ 段階の数も金額も市区町村ごとに違います。第9期の全国平均は月6,225円、標準は13段階ですが、新宿区は18段階です。
⑤ 医療費控除では段階は下がりません。あれは所得控除なので、課税所得は下がっても合計所得金額は動かないからです。

お手元で確かめる3つ →
1. 7月に届いた「介護保険料決定通知書」を出す
2. 「段階」の欄に丸をひとつ
3. 同じ世帯に住民税が課税されている方がいるか数える

ご自分は第何段階でしたか。よければコメントで教えてください。皆さまの声が、次の研究テーマになります。


※令和8年9月時点の情報です。段階の数・金額・軽減制度はお住まいの市区町村によって変わります。ご判断の前に、必ずお住まいの市区町村の介護保険担当窓口でご確認ください。
```

### タグ

```
年金と老後のお金研究室, 年金, 年金生活, 介護保険料, 介護保険, 介護保険料 段階, 住民税非課税, 老後のお金, 年金受給額, 決定通知書, 特別徴収, 世帯分離, 65歳以上, 第9期, 年金手続き
```

3 hashtag cuối 概要欄: `#年金 #年金生活 #老後のお金`

---

## VIỆC CÒN LẠI TRƯỚC KHI RENDER

1. ✅ `check_pace.py` **sạch 23/23** (2026-09-16, bản v2).
2. ✅ `voice_full.wav` + `timeline.json` (`make_timeline_exact.py`) — lệch 0,000%.
3. ✅ `_scenes26.py` + `plan26.py` — 5 gate sạch.
4. ✅ **原典 XONG — 9 thẻ** (`shoot_genten_26.py` chụp → soi mắt → `make_genten_26.py` dựng,
   gate tại chỗ 9/9, ra `remotion-vox/public/projects/nenkin-26/assets/`):
   - `genten_sj_setai1/2` — 新宿区 bảng 18段階, khoanh cột 課税区分: 第1〜3「世帯全員 住民税
     非課税」 → 第4・5「本人が住民税非課税で世帯員が住民税課税」 (scene 33)
   - `genten_jt_dan3/5` — 上越市 bảng 17段階, khoanh cột 第9期保険料: **39,500円** → **77,400円**;
     thẻ 第5 còn hiện nguyên văn điều kiện 「826,500円を超える人（世帯内に市民税課税者がいる場合）」 (scene 52)
   - `genten_mhlw` + `_8ki` + `_9ki` — 厚労省 PDF trang 1: 6,014円 → **6,225円** (+3.5%) (scene 76)
   - `genten_9ki_13` + `_18` — 新宿区: 「標準段階を9段階から13段階へと改訂」 / 「16段階から18段階」 (scene 77)
   🔴 Hai bẫy lúc chụp, đã ghi vào docstring `make_genten_26.py`: 新宿区 trả **403** cho UA
   mặc định của chrome-headless-shell; có UA thật rồi thì bị đẩy sang **trang dịch máy
   J-SERVER** vì Accept-Language tiếng Anh. Cả hai lần đều `rc=0`, file >100KB — chỉ lộ khi soi mắt.
5. ✅ **PROMPT XONG — 59 clip** (`beats26.py` → `E:/vox-director/out/nenkin-26/beats.json`
   → `print_prompts.py` + `print_motion.py`), đổ về `06_VIDEO/26_.../`:
   `vox26_FLOW.txt` (59 prompt, 1 dòng/clip, 5.815–6.744 ký) · `vox26_TENFILE.txt` (sổ dòng↔tên
   file) · `vox26_LOT1.txt` (**10 shot GEN THỬ TRƯỚC**, phủ đủ 8 khuôn) · `vox26_PROMPTS.md`.
   ⭐ **Vòng 2 (user: "phải thể hiện được số liệu + thêm vài cảnh vật")** — đo phân bố thẻ số
   rồi mới sửa, không rải bừa: **3 khe >60s không có thẻ số nào** ⇒ scene 3 → `formula`
   (0:21), scene 48 → `formula` (điểm ra quyết định 147万 ＞ 82万6,500), scene 92 → `stat`
   (trả lại 3万7,900 ở đoạn kết, trước đó 118s cuối trống trơn). Và **4 khối INFOG trừu**
   **tượng → tĩnh vật giấy KHÔNG người** (15 ngăn kéo · 28 hai cây thước tráo nhau ·
   66 tấm thẻ xé đôi · 74 ô che nhà). Kết quả: thẻ số **22 → 25** · art 53 → 54 ·
   gfx 26 → 22 · clip **59 → 61** · nhịp 4,6/phút (trần 6) · PERSON 28% (trần 35%).
   ⛔ Ba khe >60s còn lại là **trung thực** — đoạn 誤解 y tế và đoạn 三つ動くもの không đọc
   con số nào, nhét số vào là phạm luật "thẻ số lấy TỪ CHÍNH LỜI ĐỌC".
   Gate đã chạy: guard `NO WORDS` nằm ở **≤13%** đầu mọi prompt · 0 chữ Nhật lọt vào prompt ·
   47 khe CẤM SỐ / 12 khe CÓ SỐ · 0 vật-mang-thang-số ở khe cấm số.
   🔴 **Bẫy bắt được khi đọc lại prompt đã xuất:** `_TRUENUM` vẫn trỏ `_truenum25.json` ⇒ 26
   prompt của video 26 mang **số của video 25**. Phép đổi tên hàng loạt không chạm tên file đó.
   Đã dựng `tools/make_truenum26.py` (đọc thẳng timeline v26 → 14 scene có số thật). Cùng lượt
   bỏ 3 vật mời gọi số khỏi scene body (lịch ×2, thước) và bỏ cặp numeral ở scene 25 (regex
   `numeral ` số ít không khớp `numerals` ⇒ prompt vừa xin vừa cấm số).
6. 🔴 **VÒNG 1 GEN (10 clip LOT1) — LOẠI CẢ LÔ, đã sửa prompt, phải gen lại.**
   Đo bằng máy (`MAD` frame-to-frame, 320×180): **1,2–2,25 trên 10/10 clip**, trong khi
   showcase của vox-director là **21,9** và mốc vòng 3 của video 25 là 9,4. Không phải vài
   clip xui — là một LỚP.
   | lỗi | quy mô | nguyên nhân (đo được) | đã sửa |
   |---|---|---|---|
   | gần như đứng yên | 10/10 | khối XIN chuyển động nằm ở **58–65%** prompt, trong khi khối CẤM chữ/số đã được nâng lên 12% từ vòng trước ⇒ cùng định luật, lớp chưa được áp | tách làm 2: câu chốt 「MOVING SHOT, NOT A POSTER」 @**1–2%**, chi tiết @20%; guard CẤM giữ @12% |
   | poster tĩnh | 10/10 | câu 「the arrangement never changes. Nothing enters the frame and nothing leaves it」 (viết để chặn đồ bay vào) đứng ở ~78% ⇒ model đọc thành "dựng poster tĩnh" và nó thắng mọi lời xin chuyển động | đổi thành 「LAYOUT đứng yên … BUT NOTHING IN THE FRAME IS EVER STILL」 |
   | **chỉ có mũi tên** | nặng nhất ở `clip_26a` (2 mũi tên khổng lồ, 0 người, 0 vật) | `_enrich` dán 「a paper flow arrow bent through two right angles」 vào cả cảnh THUẦN HÌNH HỌC ⇒ mũi tên thành chủ thể | bỏ mũi tên khỏi kho chart + **chỉ dán chart vào cảnh đã có người** |
   | kimono / mộc bản Edo | 4/4 clip có người | khối CHARACTER ART chỉ nói "mid-century Japanese editorial illustrator", không ghim thời trang; guard chỉ cấm Western/American/1950s ⇒ chừa đúng cửa 浮世絵 | thêm 「ORDINARY MODERN JAPANESE DAYWEAR … no kimono, no yukata, no ukiyo-e」 |
   | số rớt ký tự | `clip_38a` ra 「10,00」 ở 3/4 frame | AI vẽ số, dù prompt đã đánh vần + đếm chữ số | bỏ 10.000 khỏi ảnh (sổ đen `SKIP` trong `make_truenum26.py`) — telop 「一万円下」 tải
   ⚠️ **Giả thuyết chuyển động CHƯA được chứng minh** — chỉ chứng minh được sau khi gen lại
   LOT1 và đo lại MAD. Mốc nhận: **MAD ≥ 6**. Không đạt thì lỗi nằm ở `motion_style`
   (`punchy` → `max`), không nằm ở vị trí khối.
7. ⏳ Rà lại fact #1 nếu 第10期 công bố trước ngày đăng.
