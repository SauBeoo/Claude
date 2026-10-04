# 27 — なぜ換気扇の油は、洗剤で落ちなくなるのか（灰汁と鹸化）

> **Chế độ B (viết mới)** · trục 🧹 **掃除** · 2026-08-31
> `TARGET_QUERY: 換気扇` · `INTENT: やり方`
> File đọc: `27_kankisen-abura-akujiru_TTS.md` — **gate `check_coldopen.py 27` = ✅ PASS 0 FAIL 0 WARN**

## 0. SPEC + GATE (v3 — 2026-09-01)

| | |
|---|---|
| Độ dài | **7.561 ký ≈ 24,8′** — ⭐ **đạt chuẩn kênh 25′ lần đầu sau 4 video** (25: 15,2′ · 26: 16,0′) |
| Gate | vào bài **~14s** · cửa sổ 5 câu / 1 câu không trả tiền · gap payoff max **2′17″** (trần 2′30″) |
| Sóng | **5 sóng** · **18 cú lật** · **9 câu MỞ** · loop lớn đóng ở **79%** |
| Tag nhấn nhá | **29 tag / 17 vị trí** (đỉnh bài `[間1.2][速0.8][後間1.0]`) · tag giữa câu 0 · tag dòng riêng 0 |
| Chất người | **6/6 mũi tiêm** — ① tự trào ×2 (chà 重曹 cả buổi chiều rồi ngồi xuống sàn · làm 灰汁 thất bại vì dùng tro còn nóng) ② 節子さん **9 lần xuất hiện**, 3 thoại (「耳が遠くなったのかしら」「耳じゃなかったのよ」「もう、あれには乗らないの」) + radio trên tủ lạnh ③ ký ức giác quan (mùi tro ẩm, lớp trắng trên tro còn ấm lúc sáng sớm, tiếng rao 灰買い) ④ người kể tự làm (treo khăn cũ ở mép giá) ⑤ đóng nhân vật bằng cảm xúc (ghế đẩu vào kho) ⑥ phá nhịp ≥3 lần |

### ⚠️ v1/v2 → v3: bốn lỗi đã sửa (gate PASS **không** bắt được chúng)

| # | Lỗi ở v2 | Sửa ở v3 |
|---|---|---|
| ① | **Hook mở bằng MỆNH LỆNH, không có cảnh** (「指先を押しつけてみてください」) — người xem đang ngồi xem tối, họ không đứng lên đi vào bếp | Mở bằng **CẢNH**: 節子さん đứng trên ghế đẩu, **đế chân hơi lung lay**, đã hoãn 3 lần |
| ② | **節子さん biến mất giữa bài** — xuất hiện phút 1, mất tích 10 phút kiến thức thuần, quay lại ở kết ⇒ đúng cái "rời rạc" | Cài **9 nhịp** xuyên suốt: ティッシュ không dính · bà đã thử 重曹 · điều lệ mà bà hoãn · radio · 3 năm âm thầm · kết |
| ③ | **Khối lịch sử ~4 phút là TRANG TRÍ** (吉野太夫, 近衛信尋, 蹴鞠, 金森宗和, にぎはひ草) — thú vị nhưng không phục vụ nỗi đau người xem | **Cắt sạch 5 chi tiết đó**, nén còn ~2 phút. Giữ đúng thứ chở nghĩa: tiếng rao (giác quan) · 3軒 (độc quyền) · 米より高い石けん (mắt xích logic) |
| ④ | **Sóng cuối là lời MẮNG** — "lẽ ra bạn nên lau sớm" ⇒ người đang bẩn nghe thấy bị trách | Đổi thành **GIẢI PHÓNG**: 10 giây = *không phải leo ghế đẩu nữa*, nối vào stake té. Và thêm câu 「10秒の布は、すでにできた板には効きません。今ある板は、一度だけ落としてください」 — trả lại hàng cho người đang bẩn |

### ⭐ STAKE KÉP — thứ v2 bỏ mất hoàn toàn

v2 chỉ có stake **tiền** (1万5千円). Đó là lý do nó chỉ đáng 6,5/10: quạt hút bẩn thì *sao*? v3 bổ sung hai stake có nguồn thật, và cả hai đều nối vào cùng một hành động 10 giây:

- 🔥 **CHÁY** — こんろ火災は住宅火災の原因**第1位**, **4割** do 「放置・忘れる」; 油脂 bám vào là **着火の危険**; và **火災予防条例** *bắt buộc* dọn định kỳ (điều gần như không ai biết — nó biến việc dọn từ sở thích thành nghĩa vụ).
- 🪜 **TÉ** — 20 năm **458件** té từ ghế/thang; **60歳以上 ≈ 2/3**; 60–70代 **236件**; **206件 nhập viện**; và 「そこから介護が必要になることもある」. ⇒ Khớp đúng memory `feedback_stake_tu_lap_khong_phai_loi_tien` (stake senior = mất tự lập, không phải mất tiền).

⇒ Vòng tròn khép kín: **mở bằng ghế đẩu lung lay → kết bằng ghế đẩu vào kho.**

## 1. XƯƠNG SỐNG + ĐÒN LOGIC TRUNG TÂM

**Xương sống:** 節子さん (66 tuổi) tưởng mình nặng tai vì radio trên tủ lạnh nghe không rõ. Thật ra là **tiếng quạt hút đã đổi** — dầu bám dày làm đường gió hẹp lại. Cả bài là vụ giải mã đó.

⭐ **Đòn logic trung tâm (cú lật kép):**
1. Thứ trên cánh quạt **không còn là dầu** — nó đã oxy hóa rồi **trùng hợp** thành nhựa, nên nước rửa bát (trung tính, sinh ra để bọc dầu **lỏng**) về nguyên tắc không thể xử lý.
2. Kiềm **không "hòa tan" dầu** — nó **biến dầu thành xà phòng** (鹸化). Tức bản thân vết bẩn trở thành chất tẩy.
3. Và kiềm mạnh nhất từng có trong bếp Nhật là **tro bếp** (灰汁, đo được pH14) — thứ mà thời Edo **người ta trả tiền để mua**, độc quyền chỉ **3 nhà** (紺灰座). Ngày nay ta **trả 1万5千円** để người khác mang dầu đi. **Chiều của dòng tiền đã đảo ngược.**
4. **Sóng cuối lật lại cả 5 sóng trước:** tất cả đều là xử lý *sau khi* màng đã thành nhựa. 重合 cần **thời gian + nhiệt** — bỏ một trong hai thì nhựa không sinh ra. Lau khi dầu còn lỏng: **10 giây, 0円**. Đây là chỗ đóng LOOP LỚN.

**Vì sao tro biến mất (mắt xích logic, không phải "vì tro kém"):** xà phòng nhập từ 1543 nhưng dân thường không mua nổi; quốc sản 1873 vẫn **đắt hơn cả gạo**; tới **1890年代** sản xuất lớn mới hạ giá. Tro **không bị đánh bại — nó thất nghiệp**. Cộng thêm: bếp không đun củi thì không còn tro.

## 2. NGUỒN THẬT ĐÃ FETCH (9 nguồn · WebSearch/WebFetch 2026-08-31 · KHÔNG bịa)

| # | Nguồn | Dùng ở | Số liệu lấy ra |
|---|---|---|---|
| 1 | **東京ガス「換気扇の油汚れの特徴と掃除方法」** `https://kaji.tokyo-gas.co.jp/column/detail_3539` | sóng 2 · 6 · an toàn | 酸化 → 熱で**重合** → **樹脂状**（プラスチックのような状態）· 「洗剤が浸透しにくいベタベタ・カチカチ汚れ」· 衣類の繊維+ホコリ が層になり「**油のコンクリート**」· つけ置き **45〜50℃ 30分** · パック **15分** · **アルミ素材には中性洗剤** · フィルター **1か月に1回**、ファン全体 **3か月〜半年に1回** |
| 2 | **石鹸百科「昔はアルカリ洗濯が基本」** `https://www.live-science.com/honkan/alkali/alklmanufact05.html` | sóng 4 · 5 | 江戸時代、桶に水を満たし灰を入れ**底の栓口から灰汁がしたたる「灰汁桶」が各戸に**、たらいで手洗い · 石鹸伝来 **天文12年(1543年)** ポルトガル船 · **明治**から庶民が石鹸利用 |
| 3 | **colocal「"灰"でつくるエコ洗剤」(糸島)** `https://colocal.jp/topics/lifestyle/itoshima/20210817_142620.html` | sóng 3 · 5 · an toàn | 灰汁の実測 **pH14**（試験紙）· 作り方=灰に**沸騰湯を灰の倍量**、分離まで放置（濃くするなら**2〜3日**）、上澄み=洗剤／残りペースト=**研磨剤** · **鹸化（けんか）**=アルカリ+油脂→一種の石けん · ⚠️**アルミは溶ける・皮膚も溶ける・ゴム手袋・目や口に入れない** |
| 4 | **江戸百「江戸のリサイクル2…灰買いとは」** `https://edo100.tokyo/recycle2/` | sóng 4 | 灰買いの呼び声「**へっつぅーいなおし…灰はたまってございませんか、灰屋でござい**」· 髪は灰だらけで年齢不明 · 用途 **藍染（アルカリで鮮やかな青）/肥料/濁り酒の澄清・酸味抑制/洗濯** · 灰小屋（湯屋・大店）· **川越に灰市＋灰問屋** · **灰屋紹由**=京都の元藍染め屋→巨万の富 |
| 5 | **テキスタイル・ツリー「巨富を築いた『灰屋』の話 Vol.3」** `https://textile-tree.com/tex/haiya-3/` | sóng 4 · dòng tiền | **紺灰座**（藍と灰の組合）の独占、灰屋として認められたのは **わずか3軒** |
| 6 | **Wikipedia「灰屋紹益」** `https://ja.wikipedia.org/wiki/灰屋紹益` | sóng 4 | **慶長15年(1610年)〜元禄4年11月12日(1691年)・82歳**（生年1607説あり）· 本名 **佐野重孝** · 幼くして灰屋紹由の養子 · **二代目吉野太夫**を身請け、**近衛信尋**に競り勝つ · 和歌を3人の師に、蹴鞠を飛鳥井家、茶を金森宗和 · 随筆『**にぎはひ草**』 |
| 7 | **石鹸百科／かずのすけ ほか（pH実測まとめ）** `https://www.live-science.com/honkan/partner/sesquicarbonate06.html` | sóng 1 | **重曹 pH8.2 · セスキ炭酸ソーダ 9.8 · 炭酸ソーダ 11.2** · pHが1上がると**アルカリ性は10倍** · 脱脂力 炭酸ソーダ>セスキ>重曹 |
| 8 | **石鹸百科「セスキ炭酸ソーダの使い方」** `https://www.live-science.com/honkan/partner/sesquicarbonate03.html` | sóng 6 | セスキ水=**水500mLに小さじ1〜2**（=水100mLに1g）· 頑固な汚れは**小さじ2** · キッチンペーパーで**パック** · 桶で浸けおき · 作った液は**1週間**目安 |
| 9 | **石鹸の普及史（BIOTIC／バイキョン ほか）** `https://biotic.co.jp/column50/` | sóng 5 | **1873年** 国産石鹸製造開始、なお高価で**主食の米よりはるかに高値** · **1890年代** 国産ブランド誕生・大量生産で値下がり · **コレラ流行**で衛生意識向上、伝染病予防として石鹸が推奨 · 洗濯板と粉石鹸は**明治〜昭和中頃** |
| 10 ⭐ | **東京消防庁「キッチンまわりの豆知識」** `https://www.tfd.metro.tokyo.lg.jp/lfe/kasai/kitchensknowledge.html` | hook · sóng 2 (STAKE cháy) | 「レンジフード内部に油脂が溜まっていると換気性能が低下する場合があり、コンロやレンジフードに油脂が付いていると、**着火して火災になる危険**があります」 · **コンロ火災は住宅火災の原因の第1位** · **コンロ火災の4割は「放置する・忘れる」** · **火災予防条例**で「レンジフード、コンロとその周囲は定期的に清掃すること」が定められている |
| 11 ⭐ | **国民生活センター「高齢者の脚立・はしごからの転落」** `https://www.kokusen.go.jp/news/data/n-20190328_2.html` | sóng cuối (STAKE té) | 20年間で**458件** · **60歳以上が約3分の2**、60〜70代が**約236件** · **206件が入院を必要とした** · 頭部外傷・脊椎損傷・四肢骨折、**要介護状態につながる可能性** · 自宅で**3メートル**の高さから落下した**70代女性**の例 |
| 12 | **消費者庁「換気扇で火災等24件の重大製品事故」** `https://www.caa.go.jp/notice/entry/036353/` | (dự phòng) | **24件**、公表 **2024年2月9日**、消費生活用製品安全法第35条第1項 |

⚠️ **Rào chữ đã cài trong lời đọc:** pH14 là **một phép đo bằng giấy thử tại gia** (nguồn 3), không phải nghiên cứu — script nói 「実際に紙で測った記録があります」 chứ không tuyên bố đó là hằng số của mọi loại tro. Giá thợ nêu **cả hai dải** (1万〜1万5千 và 1万5千〜2万) đúng như hai nguồn khác nhau ghi.

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜ換気扇の油は、洗剤で落ちなくなるのか――かまどの灰に隠れていた、ペーハー14の秘密` | 44 | 換気扇@3 | keyword volume cao nhất (換気扇 ≈137 thang kênh) + khuôn `なぜ` |
| **A2** | `なぜ重曹では、換気扇の油が落ちないのか――ペーハー8.2と14の差` | 33 | 重曹@3・換気扇@10 | đổi keyword dẫn sang 重曹 (≈130, gần bằng 換気扇) + đưa số vào vế phụ |
| **A3** ⭐mới v3 | `なぜ換気扇の掃除で、もう踏み台に乗らなくていいのか――0円10秒の昔の知恵` | 35 | 換気扇@3 | đổi **STAKE**: bán *sự an toàn của người già* thay vì bán *cách tẩy dầu*. Căn cứ: 転落 20年458件・206件入院・要介護 (nguồn 11) + memory `feedback_stake_tu_lap_khong_phai_loi_tien` |

<details><summary>A3 bản v2 (đã thay) — giữ để đối chiếu nếu A/B cần biến "lệnh cấm"</summary>

`換気扇の油に、重曹を使ってはいけない――0円で落とせた、江戸の灰の知恵` — khuôn LỆNH CẤM theo peer `絶対に〜してはいけない` (34.692 view/ngày). Thay vì bản này vì stake té mạnh hơn cho tệp 45–70, nhưng nếu muốn thử biến "lệnh cấm" thì đây là bản sẵn sàng.

</details>

**Title CHỐT**

```
なぜ換気扇の油は、洗剤で落ちなくなるのか――かまどの灰に隠れていた、ペーハー14の秘密
```

<details><summary>5 phương án gốc (trước khi chọn 3)</summary>

1. `なぜ換気扇の油は、洗剤で落ちなくなるのか――かまどの灰に隠れていた、ペーハー14の秘密`
2. `なぜ重曹では、換気扇の油が落ちないのか――ペーハー8.2と14の差`
3. `換気扇の油に、重曹を使ってはいけない――0円で落とせた、江戸の灰の知恵`
4. `なぜ江戸の商人は、かまどの灰を買いに来たのか――換気扇の油を溶かす、ペーハー14`
5. `なぜ10秒で済むものが、1万5千円になるのか――換気扇の油と、待ってしまう順番`

</details>

⚖️ **Compliance đã quét cả 5:** không từ nhóm cấm (殺/血/死/自殺). Mọi tình tiết nêu ra đều có trong video. Không modifier xác minh `効果`/`意味ある` ở 5–7 chữ đầu.

## 4. TEXT THUMBNAIL 3 TẦNG

| tầng | chữ | ký | vai |
|---|---|---|---|
| Tầng 1 (dẫn) | `換気扇の油` | 5 | ① VỀ CÁI GÌ — keyword đo được cao nhất |
| **Tầng 2 (HERO, TO NHẤT)** | `かまどの灰` | 5 | ③ PHẢI LÀM GÌ — tên VẬT, tiếng Nhật thuần |
| Tầng 3 (hệ quả) | `重曹では無理` | 6 | ② CHUYỆN GÌ XẢY RA — cú lật |
| badge | `0円` | 2 | luật kênh: LUÔN có badge giá |

✅ **Gate 7 (che ảnh vẫn biết bài nói gì):** ① quạt hút + dầu ② baking soda vô dụng ③ dùng tro bếp, 0 yên. Đủ 3 câu.
⛔ Không dùng `pH14` trên thumbnail — `ペーハー` là 外来語, luật `audience-45plus.md` §5.2 cấm 外来語 trên thumbnail/title 60s đầu. Số 14 để trong video và trong vế phụ của title.

**Khuôn: B1 (bright) lồng K7 (scale contrast)** — tránh K1 (#25) + K4 (#26), K7 xa nhất thư viện (lần cuối #04/#13). Giải pháp bé xíu 0円 (nắm tro) ↔ vấn đề khổng lồ (quạt hút đen kịt dầu). Bộ 3 T1/T2/T3 đầy đủ + PLATE no-text: `06_VIDEO/27_kankisen-abura-akujiru/thumb_prompts_{BLOCKS.md,FLOW.txt,TENFILE.txt,PLATE.txt}`. Đo máy: TEXT @6% (trần 15%) · 1.171–1.401 ký (trần 1.500) ✅. **Chờ user gen** → soi từng ký tự → vá watermark ✦ → `stamp_brand.py --pos tr`. Video kế tiếp tránh **K7 + K1**.

## 5. GÓI UPLOAD

**Tên file upload:** `kankisen-abura-akujiru-ph14.mp4`

**3 dòng đầu 概要欄:**

```
換気扇の油が洗剤で落ちないのは、それがもう油ではなく「樹脂」に変わっているからです。
この動画では、油を石けんに変えてしまうアルカリの仕組みと、かまどの灰から取れる灰汁の使い方、そして0円で10秒で終わらせる順番をお話しします。
重曹でこすっても落ちなかった方、業者に1万5千円を払う前に、ぜひ最後までご覧ください。
```

**目次（実測 2026-09-01、`06_VIDEO/27_.../timeline.json` から算出）:**

```
00:00 揺れる踏み台と、二つの代償
00:57 節子さんのラジオが聞き取りにくくなった理由
01:58 重曹をふりかけても落ちなかった話
03:24 その汚れは、もう油ではなかった
05:08 レンジフードの掃除は条例で決まっていた
05:58 アルカリは油を「石けんに変える」仕組み
07:51 かまどの灰汁、作り方
09:39 扱いの注意とセスキ炭酸ソーダ
12:37 ただの燃えかすではなかった灰
14:23 なぜ灰は台所から消えたのか
17:04 節子さんのラジオ、謎が解けた瞬間
18:25 本当の答えは、10秒でした
19:31 転落という、もう一つの代価
20:46 節子さんの結末
21:20 正直に言うと、灰汁は万能ではありません
```

**Mô tả đầy đủ:**

```
換気扇の油が洗剤で落ちないのは、それがもう油ではなく「樹脂」に変わっているからです。
この動画では、油を石けんに変えてしまうアルカリの仕組みと、かまどの灰から取れる灰汁の使い方、そして0円で10秒で終わらせる順番をお話しします。
重曹でこすっても落ちなかった方、業者に1万5千円を払う前に、ぜひ最後までご覧ください。

【目次】
00:00 揺れる踏み台と、二つの代償
00:57 節子さんのラジオが聞き取りにくくなった理由
01:58 重曹をふりかけても落ちなかった話
03:24 その汚れは、もう油ではなかった
05:08 レンジフードの掃除は条例で決まっていた
05:58 アルカリは油を「石けんに変える」仕組み
07:51 かまどの灰汁、作り方
09:39 扱いの注意とセスキ炭酸ソーダ
12:37 ただの燃えかすではなかった灰
14:23 なぜ灰は台所から消えたのか
17:04 節子さんのラジオ、謎が解けた瞬間
18:25 本当の答えは、10秒でした
19:31 転落という、もう一つの代価
20:46 節子さんの結末
21:20 正直に言うと、灰汁は万能ではありません

換気扇の油汚れは、空気に触れて酸化し、こんろの熱で重合することで、樹脂に近い「油のコンクリート」に変わります。中性の食器用洗剤は液体の油を包んで流す仕組みのため、こうなった汚れには効きません。効くのはアルカリです。アルカリは油を溶かすのではなく、鹸化という反応で油そのものを石けんに変えてしまいます。台所で使うアルカリには強さの差があり、重曹はペーハー8.2、セスキ炭酸ソーダは9.8、炭酸ソーダは11.2ですが、かまどの灰から取れる灰汁は、糸島での実測でペーハー14。目盛り1つで10倍変わる世界で、灰汁は群を抜いて強い薬でした。

江戸の町には、灰を買い取って歩く「灰買い」がいて、灰屋として認められたのはわずか3軒だけだったと伝わっています。石けんが庶民に届く前、洗濯も台所の汚れ落としも、かまどの灰が支えていました。石けんが安くなり、薪のかまどが姿を消すと、灰は静かに台所から消えていきました。

※本動画は、暮らしの中の生活の知恵・忘れられた技術をご紹介する情報コンテンツです。灰汁や強いアルカリ性の洗剤を扱う際は、ゴム手袋を着用し、換気を行い、目や口に入らないよう十分ご注意ください。アルミ素材には使用しないでください。高い場所での作業は、安定した足場で、できればご家族と一緒に行ってください。
ご紹介した内容は、東京ガス・石鹸百科・国民生活センター・東京消防庁など、公的・専門的な情報にもとづいています。

ご感想や、ご実家の換気扇・かまどの記憶があれば、ぜひコメントで教えてください。高評価やシェアで「古代の秘訣」を応援していただけると、今後の内容もより深めてまいります。
```

**タグ**

```
古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, 換気扇, 換気扇 掃除, 換気扇 油汚れ, レンジフード, レンジフード 掃除, 油汚れ, 油汚れ 落とし方, 重曹, セスキ炭酸ソーダ, 炭酸ソーダ, アルカリ性, 鹸化, 灰汁, 木灰, 灰買い, 紺灰座, 灰屋紹益, 江戸時代, 台所, キッチン掃除, 大掃除, ハウスクリーニング, 50代, 60代
```

#生活の知恵 #昔の知恵 #古代の秘訣 (3 hashtag cuối desc)

## 6. ⚠️ VIỆC CÒN MỞ

1. ✅ **Độ dài ĐÃ ĐẠT: 24,8′** (v2 22,7′ → v3). Nới bằng nội dung thật, không câu đệm: ティッシュ tự kiểm · 火災予防条例 · コレラ · mùi tro · chuyện làm 灰汁 hỏng · 3 năm âm thầm của 節子さん. Còn nới thêm được thì lấy 藍染 (**cần nguồn có số, chưa có**) hoặc 釉薬.
2. **SLIDES + Remotion chưa làm** — từ video 25 kênh dựng bằng Remotion (`build_remotion_25.py` → copy thành `build_remotion_27.py`), 8 bước ở `CLAUDE.md` §②.
3. **Thumbnail: 4 file prompt chưa xuất** (`thumb_prompts_FLOW/BLOCKS/TENFILE/PLATE`) — theo `ab-3title-3thumb.md` §3.1 Bước 4.
4. **目次 phải đo lại từ `subs.srt` thật** sau render — mốc trên là dự kiến.
5. **Trends: chưa đo hết rổ.** Đã đo `換気扇` (mean 18,1 · 31/32 điểm >0 · ≈137 thang kênh), `重曹` (12,9), `換気扇 掃除` (4,5), `油汚れ` (3,7), `レンジフード` (2,3), `セスキ` (0,7), `換気扇 油` (0,6) — bằng **pytrends** (gprop=youtube, geo=JP, 30 ngày, anchor `フライパン`). ⭐ **Phát hiện: pytrends CHẠY ĐƯỢC, không cần Chrome** (chỉ cần không truyền `retries` vì urllib3 v2 bỏ `method_whitelist`). Ghi vào `01_SOURCES/2026-08-31_demand-scan.md`.
6. 🔴 **`灰` KHÔNG được lên title/tag làm keyword dẫn** — Trends mean 52,3 nhưng related toàn **黛灰 (VTuber) · コナン灰原哀 · 灰谷兄弟 · エルデンリング遺灰**. Nhiễu tên riêng, đúng bẫy đã ghi ở video 25.

## 7. 📌 Pinned comment

```
最後までご覧いただき、ありがとうございます。今日ご紹介した中で、まず試してみたいと思われたのは、どれでしたか。
お住まいの地域では、かまどや薪ストーブの灰を、どう使っていましたか。畑にまいた、洗い物に使った、そんなご家庭の知恵があれば、ぜひ聞かせてください。皆さまの声を参考に、これからの内容も深めてまいります。
🌿 灰汁や強いアルカリ剤を扱うときは、ゴム手袋を着け、換気をして、目や口に入らないようご注意ください。アルミ素材には使えません。お子さんやペットの手が届かない場所で保管をお願いします。
```
