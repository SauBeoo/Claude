# 30 — 布団を干す日を、私たちは毎年まちがえている（ダニ × 寒干し）

- **Chế độ:** B — viết mới · **Ngày:** 2026-09-05 · **Độ dài (v2):** 5.662 ký ≈ **18′32″** (hệ số 305,4)
- **Trục:** 🐜 害虫 — **override có chủ ý, yêu cầu trực tiếp của user** (*"chủ đề các diệt 1 con vật nào đó có hại"*), giống ca #23. Khác trục #29 (🔥 signature) ✅
- **File đọc:** `03_SCRIPTS/30_futon-dani-uchinaoshi_TTS.md` · gate ✅ **PASS 0 FAIL**
- **Kênh:** 古代の秘訣 · slot T2·T4·T6 13:00 JST

```
# TARGET_QUERY: ダニ
# INTENT: やり方
```

---

## §0.1 ĐO TRENDS — pytrends, gprop=youtube, geo=JP, **12 tháng**, anchor `フライパン` (2026-09-05)

21 keyword đo trong 5 rổ. Bảng chỉ giữ ứng viên có tranh chấp:

| keyword | thang kênh | slope 6m | related → intent | phán |
|---|---|---|---|---|
| 布団 | 327,9 | — | `布団ちゃん` 100 · `布団ちゃん加藤純一` · `布団ちゃんダマスカス` | 🔴 **nhiễu tên riêng 100%** (streamer) |
| ネズミ | 87,2 | −14,3% | `ネズミ嫌がる音` 100 · `が嫌がる音` 95 | 🔴 intent = **tìm video phát âm thanh**, không nghe giảng |
| 冷蔵庫 | 75,6 | — | `おすすめ冷蔵庫` · `ニトリ` | 🔴 intent MUA |
| アリ | 67,8 | −11,2% | `着信アリ` · `アリさんマークの引越社` · `モハメド・アリ` · `アリエクスプレス` | 🔴 đồng âm, nhiễu ~100% |
| 畳 | 57,0 | — | `6畳部屋` · `6畳レイアウト` · `一畳間` | 🔴 là **đơn vị đo phòng** |
| 大根 | 174,8 | — | `大根レシピ` 100 · `切り干し大根` 26 | 🟡 intent レシピ (cùng lý do đã loại `さつまいも` ở #29) |
| 窓 | 112,3 | — | `窓掃除` 55 · `窓拭き` 33 · `社会の窓` 54 | 🟢 để dành — trục 掃除 đang 7/29 |
| ムカデ | 20,6 | +60,4% | `ムカデ人間` (phim) 100 · `ムカデ競争` | 🔴 nhiễu ~85%, slope là do phim |
| ⭐ **ダニ** | **16,0** | **+65,5%** | `ダニ退治` 100 · `布団ダニ` 91 · `ダニ刺され` 64 · `ダニ取り` 62 · `ダニ対策` 61 | ✅ **CHỌN** |
| クモ 9,9 · 土鍋 9,2 · 洗濯槽 8,9 · ハエ 8,5 · ナメクジ 7,0 · 障子 8,2 · 結露 3,7 · 押し入れ 0 | | | | ⛔ nhỏ, hoặc #26 đã làm (障子) |

### ⭐ Vì sao chọn `ダニ` dù volume KHÔNG cao nhất

1. **Intent sạch nhất trong 8 loài chưa làm** — 5/7 top query là `退治/対策/取り` = やり方 thuần. Nhiễu chỉ 2 cái và tách được (`ダニ・オルモ` cầu thủ, `ダニエル・パウター` ca sĩ).
2. 🔴 **SLOPE +65,5%** — nửa đầu năm 10,3 → nửa sau 17,0, và **6 tuần gần nhất là 19–26, cao nhất cả năm**. Đây là thứ hiếm: cầu đang lên thật **và** intent sạch.
3. **Sổ #24 từng loại `ダニ` vì *"mùa 6–8月 đang tàn"*** — đo lại hôm nay thì ngược hẳn, vì mùa của nó **không phải mùa con vật, mà là mùa XÁC con vật** (nguồn 3 dưới). Cảnh báo cũ *"cầu mang chữ 殺す"* cũng không còn: `ダニ 殺す` đã rơi khỏi top/rising.
4. Nhánh **布団ダニ** (91 điểm) đúng tệp 45–70 và né được nhánh YMYL da liễu `ダニ刺され`.

⚠️ **Giới hạn:** thang 16,0 = **1/3 của `包丁`** (#29 ≈ 49,9 quy cùng thang) và ~2/3 của `換気扇` (#27 ≈ 23,4). Bài này đổi **số vé** lấy **intent + đúng mùa**. Nếu view thấp, đừng đọc là "đề sai" trước khi tách được hai biến đó.

---

## §0.2 XƯƠNG SỐNG (v2 — viết lại 2026-09-05)

> **私たちは年に一度、いちばん間違った日に布団を干している。**

**LOOP LỚN đặt ở giây 32, đóng ở 84%:** 「1年のうち、たった一度だけ、布団を干すのに本当に向いた日があります。私たちは毎年、それとは正反対の日を選んでいます」 — người xem phải ở lại để biết **đó là ngày nào**.

### ⭐ Cú lật cuối — ghép 2 con số của 2 cơ quan khác nhau

| | số | nguồn |
|---|---|---|
| Độ ẩm TB Tokyo tháng **8** | **74%** | 気象庁 平年値 1991–2020 |
| Độ ẩm TB Tokyo tháng **1** | **51%** | 気象庁 平年値 1991–2020 |
| Mạt cần độ ẩm | **60–80%** | 大阪府茨木保健所 |

⇒ **Phơi chăn ngày hè nắng gắt = trải nó ra giữa không khí 74% — vẫn nằm TRONG dải mạt thích.** Phơi giữa tháng Giêng = 51%, **dưới ngưỡng**.
⇒ **Ngày phơi chăn tốt nhất trong năm là một ngày mùa đông.** Và người xưa có tên riêng cho nó: **寒干し**.

### 3 ngày phơi có tên — thứ "đã thất lạc" của bài

| tên | thời điểm |
|---|---|
| 土用干し | 7月下旬–8月 |
| 虫干し | 10月下旬–11月 |
| **寒干し** | **1月下旬–2月** ← cái không ai còn làm |

Gốc là **曝涼**, vào Nhật từ **đầu thời Heian**; **正倉院 vẫn làm đúng cuối tháng 10 suốt 1.200 năm**. Ta rút xuống một lần/năm, và chọn đúng ngày tệ nhất trong ba.

### Ba việc quen thuộc, hỏng theo ba kiểu khác nhau

| việc | tưởng là | thật ra |
|---|---|---|
| 天日干し | giết mạt | mặt chăn chỉ **43℃** (cần 50℃) → **8割 sống**. Nó lấy ĐỘ ẨM, không lấy mạng |
| 布団たたき | đánh bụi ra | **kéo xác + phân từ trong ra bề mặt** |
| 掃除機 | hút mạt | lớp sâu **0,06%** (chân mạt có giác hút). Nhưng nó **đúng** — vì hút được XÁC, tức chính thứ gây dị ứng |

**Câu "gài" ở 03:27, "nổ" ở 15:42:** 「殺す道具ではなく、住みにくくする道具。それが、天日干しの正体でした」 → 「乾かす道具なら、いちばん乾いた日に使う。じつは、当たり前のことでした」

**Hai câu trả lời của người xưa** (cầu nối ở 10:49): ① 職人に頼む = **打ち直し** ② 自分の手と日にちだけ = **寒干し**. Cái thứ hai miễn phí — và **chính vì miễn phí nên không ai đi quảng bá nó**, đó là chương dòng tiền.

**Câu chốt:** 失われたのは、寒干しや打ち直しという、やり方ではありません。布団は、季節に合わせて世話をして、中身を入れ替えながら、何十年も使うもの。その、あまりにも当たり前だった前提のほうです。

---

## §0.3 SÓNG (gate: 4 sóng · 10 cú lật · 10 câu MỞ · loop lớn **84%** · cửa 45s **0 câu không trả tiền**)

| # | ĐẢO | TRẢ | MỞ |
|---|---|---|---|
| 0 | **COLD OPEN 0–30s** — 400匹/4万匹 → **1000倍** → 「顔の30センチ先で畳んでいた、あなたです」 → mẹo 40秒 | | 「1年のうち、たった一度だけ…正反対の日を選んでいます」 |
| 1 | 「刺さない、血も吸わない」生き物がなぜ嫌われるのか | チリダニ90%超 · 0,3–0,5mm · 寿命2か月 · 200–300卵 | 「答えは、生きているあいだの話ではありません」 |
| 2 | 4時間干しても死なない | 43℃ vs 50℃ · 8割生存 · 布団は熱を逃がさない道具 | 「思っていた意味とは、まるで違っていました」 |
| 3 | 干すのは**湿度**を奪うため | 20–30℃/60–80% · 体の7割が水 · ⭐**「この一行を覚えておいてください」** | |
| 4 | 叩いてはいけない | 目黒区 · 母の物干し場の記憶 | 「順番が、逆だったのです」 |
| 5 | 掃除機は生きたダニの道具ではない | 77% ↔ **0,06%** · 吸盤 · 死骸のほうが刺激強い · 数6–8月 ↔ アレルゲン8–10月 · 40秒 | 「本当に効くのは、ここからです」 |
| 6 | 熱は**長さ**で効く | 50℃数時間/60℃15分 · 乾燥機/コインランドリー/黒いポリ袋 · 白状=温めてそのまましまっていた | 「では、あの人たちは、どうしていたのでしょうか。今日の本当の話は、ここからです」→ **CTA (51%)** |
| — | **dòng tiền (10:02)** | 買い直すもの ↔ 代金のかからないやり方 · 「広めてくれる人がいない」 | 「答えは、二つあります」 |
| 7 | **打ち直し** (11:01) | 語源=弓で綿を叩く · 4万匹→0 · 12800円〜 · 昭和30–50年は毎年 · 木綿80–100年 · 化繊は直せない | 「職人に頼めない家は、どうすれば」 |
| 8 | ⭐ **寒干し** (13:42) — 3 ngày có tên · 曝涼 · 正倉院1200年 | **74% vs 51% vs 60–80%** → **ĐÓNG LOOP LỚN 84%** → やり方 (1–2月、10時–14時、2時間、裏返し、叩かず40秒、30分冷ます) | |

**Chất người 6/6** — ① 白状しますと、布団乾燥機を買った最初の年 ② 母の thoại 「綿は、くたびれるだけよ。死にはせん」 ③ 乾いた綿のにおい・団地の物干し場・遠くで返ってくる同じ音 ④ 布団屋さんに一度だけ見せてもらった綿の層 ⑤ 「あれは、布団の話ではなかったのだと、いまになって思います」 ⑥ 「綿は死なない。」

---

## §0.4 NGUỒN CẤP 1 (đã fetch và verify 2026-09-05 — ⛔ không con số nào ngoài danh sách này)

| # | Nguồn | Số dùng trong bài |
|---|---|---|
| 1 | **日革研究所**「布団のダニ退治『天日干し』の効果を検証」 | 2017-08-31 · 気温31℃/湿度30% · 天日干し4時間 · 布団表面 **最高43℃** · 生存 **約8割**(夏) / **9割以上**(冬) · 冬季実験 2017-03-08 表面最高16℃ |
| 2 | **日革研究所**「ダニは掃除機で死ぬ？」 | サイクロン式 表面**77,37%** / 中間層 **0,70%** / 深部 **0,06%** · 脚に吸盤状の構造 · **50℃以上で数時間・60℃以上なら15分** · 体の約**7割**が水 |
| 3 | **大阪府健康医療部茨木保健所衛生課**「ダニとアレルギーの関係」 | チリダニ(ヒョウヒダニ)が屋内ダニの**90%以上** · 体長 **0,3–0,5mm** · 成虫寿命 **約2か月** · メス生涯 **200–300個**産卵 · 適温 **20–30℃**/湿度**60–80%** · 布団1枚 **400匹以上、多いとき40,000匹** · ダニ数ピーク **6–8月** ↔ アレルゲン量ピーク **8–10月** · 上げ下ろし時 空中濃度 **1,000倍**、睡眠中 **10倍** · 掃除機 畳1枚**30秒**、布団 週1回**1分30秒** |
| 4 | **目黒区**「住まいの衛生 ダニ対策」 | 布団掃除機がけ **片面約40秒・週1回**・吸引力 **200W以上** · シーツ週1回/毛布・敷きパッド月1回 · 叩いても効果は期待できず、**内部のアレルゲンを表面に出す** |
| 5 | **気象庁 平年値 (1991–2020, 東京)** | 月平均相対湿度 **1月51% · 2月52% · 8月74% · 7月76%(cao nhất)** · 月平均気温 1月5,4℃ / 8月26,9℃ |
| 6 | **コトバンク「虫干し」「土用干し」「曝涼」** + 季語と歳時記「正倉院曝涼」 | 虫干し＝夏の土用のころ衣類・調度・書籍を干す · 別名 虫振い・風入れ・土用干し · 古くは**曝涼** · **平安時代初期**に中国にならい正倉院で · 年3回=**土用干し(7月下旬–8月)・虫干し(10月下旬–11月)・寒干し(1月下旬–2月)** · 正倉院の風入れは10月下旬–11月上旬 |
| 7 | **櫻道ふとん店**「教えて布団の達人」 | 打ち直しの語源＝弓のようにしなる棒で綿を打った · **昭和30〜50年頃までほとんどの家庭が毎年** · 「敷いて3年、掛けて5年」 · 木綿の寿命 **80〜100年** · 木綿シングル **12,800円〜** |

**URL:**
1. https://nikkaku-j.com/laboratory/布団のダニ退治「天日干し」の効果を検証
2. https://nikkaku-j.com/danitorilabo/activity-report/dani-vacuumcleaner/
3. https://www.pref.osaka.lg.jp/o100130/ibarakihoken/eiseika/dani.html
4. https://www.city.meguro.tokyo.jp/seikatsueisei/kenkoufukushi/eisei/dani.html
5. https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php?prec_no=44&block_no=47662
6. https://kotobank.jp/word/虫干し-140455 · https://kotobank.jp/word/土用干し-585165 · https://kigosai.sub.jp/001/archives/10001
7. https://www.sakuramichi3776.co.jp/column/12/

⚖️ **YMYL:** ①「医師にご相談ください」đã có ở khối tự kiểm (vùng 10:00). ② không hứa chữa hen/dị ứng — chỉ nói cơ chế allergen. ③ không cáo buộc đích danh công ty ở chương dòng tiền (「誰かを責める話ではありません」). ④ nguồn 5 là cửa hàng, dùng cho **lịch sử nghề**, không dùng cho số y tế.

⛔ **Giả thuyết đã tra và BÁC BỎ:** *"nhà hiện đại kín hơn nên nhiều mạt hơn"* — tra ra **ngược**: nhà 高気密高断熱 ít 結露 nên **ít** mạt hơn nhà cũ. Bỏ hẳn hướng này, không đưa vào bài.

⛔ **Đã tra và KHÔNG dùng:** ダニのフンの大きさ「0,01mm」 (chỉ thấy ở blog thương mại, không có nguồn cấp 1) · 「布団から100万匹」 (bài báo, không phải cơ quan).

---

## §1 TITLE

### Title CHỐT
```
なぜ布団のダニは、真夏に干しても減らないのか――昔の人が知っていた「寒干し」
```

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜ布団のダニは、真夏に干しても減らないのか――昔の人が知っていた「寒干し」` | 38 | ダニ@4 | khuôn `なぜ` của kênh + tên kỹ thuật thất lạc ở vế sau |
| **A2** | `ダニ退治は、真冬がいちばん効きます――湿度51パーセントという答え` | 31 | ダニ@1 | đổi keyword dẫn sang `ダニ退治` (top query 100 điểm) + con số làm mồi |
| **A3** | `4時間干して43度――布団のダニが8割生き残る、たった7度の差` | 29 | ダニ@14 | đổi kiểu hook: nghịch lý số học thay câu hỏi |

✅ **Compliance:** không bản nào chứa 殺す/死ね/血. `減らない`/`生き残る` là phủ định/trung tính, ngoài nhóm cấm.

### Tên file upload
```
futon-dani-kanboshi-taiji.mp4
```

---

## §2 概要欄

### 3 dòng đầu (vùng hiển thị — cấm lời chào)
```
布団のダニは、よく晴れた夏の日に4時間干しても、約8割が生き残っています。研究所の実験では、布団の表面温度は43度どまりでした。
じつは、干すことでダニから奪えるのは熱ではなく、湿気のほうです。そして東京の平均湿度は、8月が74パーセント、1月が51パーセント。ダニが増えるのに必要なのは、60から80パーセントです。
昔の日本には、布団を干す日が1年に三度あり、そのうちの一つは真冬でした。「寒干し」と呼ばれていたその日のことと、叩かずにダニを追い出す順番をお話しします。
```

### 目次 (ĐÃ hiệu chỉnh theo `subs.srt` thật 2026-09-09 — bản viết trước render lệch tới **30s**)

```
【目次】
00:00 布団に何匹いるのか ― そして今朝の1000倍
00:39 1年でたった一度、干すのに向いた日
00:51 ごあいさつ
01:12 相手の顔 ― 刺さない、血も吸わない生き物
02:00 4時間干して43度、ダニが死ぬのは50度
03:07 干す意味は「殺す」ではなく「乾かす」
03:51 叩いてはいけない理由
04:50 掃除機の実験 ― 深部で0.06パーセント
06:04 数のピークと、アレルゲンのピークのずれ
06:35 かけ方の目安 ― 片面40秒、一方向に
07:17 熱は「高さ」ではなく「長さ」
07:42 家でできる三つの方法
09:36 なぜ、お金のかからない一手は広まらないのか
10:21 昔の人が持っていた、二つの答え
10:33 打ち直し ― 中身そのものを入れ替える
12:00 昭和30年から50年ごろ、毎年やっていたこと
13:07 干す日には、名前があった ― 土用干し・虫干し・寒干し
13:47 三つのうち、いちばん意外なのは
14:07 東京の湿度 ― 8月74パーセント、1月51パーセント
15:08 「乾かす道具なら、いちばん乾いた日に」
15:50 寒干しのやり方
16:27 母の言葉「綿は、くたびれるだけよ」
17:02 失われたのは、やり方ではなく前提
```

### Mô tả đầy đủ (ĐÃ gồm 目次 ở đầu — parser `upload_pack.py` chỉ đọc khối này)
```
【目次】
00:00 布団に何匹いるのか ― そして今朝の1000倍
00:39 1年でたった一度、干すのに向いた日
00:51 ごあいさつ
01:12 相手の顔 ― 刺さない、血も吸わない生き物
02:00 4時間干して43度、ダニが死ぬのは50度
03:07 干す意味は「殺す」ではなく「乾かす」
03:51 叩いてはいけない理由
04:50 掃除機の実験 ― 深部で0.06パーセント
06:04 数のピークと、アレルゲンのピークのずれ
06:35 かけ方の目安 ― 片面40秒、一方向に
07:17 熱は「高さ」ではなく「長さ」
07:42 家でできる三つの方法
09:36 なぜ、お金のかからない一手は広まらないのか
10:21 昔の人が持っていた、二つの答え
10:33 打ち直し ― 中身そのものを入れ替える
12:00 昭和30年から50年ごろ、毎年やっていたこと
13:07 干す日には、名前があった ― 土用干し・虫干し・寒干し
13:47 三つのうち、いちばん意外なのは
14:07 東京の湿度 ― 8月74パーセント、1月51パーセント
15:08 「乾かす道具なら、いちばん乾いた日に」
15:50 寒干しのやり方
16:27 母の言葉「綿は、くたびれるだけよ」
17:02 失われたのは、やり方ではなく前提

家の中にいるダニの9割以上は、チリダニ（ヒョウヒダニ）という種類です。体長は0.3ミリから0.5ミリ。刺すことも血を吸うこともなく、私たちが落とした皮膚のかけらを食べて増えていきます。成虫の寿命はおよそ2か月、メス1匹が生涯に200個から300個の卵を産みます。敷きっぱなしの布団では400匹以上、多いときには4万匹という数字も報告されています。

ところが、私たちを悩ませているのは、生きているダニではありません。死骸とフンのほうが、アレルゲンとしては刺激が強いと言われています。ダニの数そのものが増えるのは6月から8月ですが、アレルゲンの量がいちばん多くなるのは8月から10月。およそ2か月、遅れてやってきます。

天日干しは、ダニを殺す方法ではありませんでした。研究所の実験では、真夏に4時間干しても布団の表面温度は43度どまり。ダニが死ぬ50度には届かず、約8割が生き残っていました。干すことの意味は、ダニが好む湿度60から80パーセントを奪うことにあります。

そして、ここに昔の暮らしの知恵があります。かつての日本では、布団や着物を干す日に名前がついていて、1年に三度ありました。7月下旬から8月の「土用干し」、10月下旬から11月の「虫干し」、そして1月下旬から2月の「寒干し」です。もとは「曝涼」といい、平安時代のはじめに伝わった習わしで、奈良の正倉院ではいまも毎年、宝物に風を通しています。

気象庁の平年値によれば、東京の月平均湿度は8月が74パーセント、1月が51パーセント。ダニが増えるのに必要な湿度は60から80パーセントですから、真夏の晴れた日に干すことは、ダニにちょうどいい湿り気の中に布団を広げることでもありました。乾かす道具なら、いちばん乾いた日に使う。昔の人が数えていたのは、気温ではなく空気の乾き方のほうだったのです。

動画の後半では、取り込んだあとの掃除機のかけ方（片面およそ40秒、一方向に）、布団乾燥機やコインランドリーの使い方、そして昭和30年から50年ごろまでほとんどの家庭が毎年行っていた「打ち直し」についてもお話しします。

※この動画は、公的機関および専門研究機関が公開している資料をもとに構成しています。アレルギーの症状が続く場合は、自己判断せず医師にご相談ください。
※紹介する方法は一般的な家庭を想定したものです。寝具の素材や製品の指示が優先されます。

#生活の知恵 #昔の知恵 #古代の秘訣
```

### タグ (33個)
```
古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, ダニ, ダニ退治, ダニ対策, 布団 ダニ, ダニ取り, 布団 干し方, 天日干し, 寒干し, 虫干し, 土用干し, 布団たたき, 布団 掃除機, ハウスダスト, ダニ アレルゲン, チリダニ, 布団乾燥機, 打ち直し, 綿布団, 寝具 手入れ, 冬 布団, アレルギー対策
```

---

### Pinned comment

```
最後までご覧いただき、ありがとうございます。今夜さっそく試してみようと思われたのは、片面40秒の掃除機でしたか、それとも手帳に「1月の晴れて風のある日」と書き込むほうでしたか。
皆さまのお宅では、布団をどのくらいの間隔で干していらっしゃいますか。「うちの母は秋になると布団屋さんを呼んでいた」というような、ご家庭に伝わっていた手入れの仕方があれば、ぜひ聞かせてください。皆さまの声を参考に、これからの内容も深めてまいります。
※アレルギーの症状が続く場合は、自己判断せず医師にご相談ください。寝具の素材や製品の指示が優先されます。黒いポリ袋を使う方法は、真夏の直射日光の下でのみ行い、お子さまの手の届かない場所で作業なさってください。
※ナレーションは音声合成（VOICEVOX：青山龍星）を使用しています。🌿
```

---

## §3 THUMBNAIL — khuôn **B1 (bright) lồng K2 (X-diagram)**, 3 ban A/B

CHOT 2026-09-09. Tranh **K3** (#29) + **K6** (#28) dung chi thi so; ❌/✅ hop le (lan cuoi #21, cach 6 video dang).

**Bo chu (GIONG HET ca 3 ban — bien thu la HINH):** `布団のダニ` / **HERO** `干す日が逆` / `正解は1月` / badge `費用0円`.

| | bien thu |
|---|---|
| **T1** | baseline: he dimmed + vong cam do X (lop sau) ↔ dong sang net, suong gia tren tay vin (lop truoc) |
| **T2** | doi DUNG 1 bien HINH: doi chu the sang cai sai THU HAI cua bai — **dap chan**, bui no ra trong nang xien, vong cam do de len gay tre. Chu y nguyen |
| **T3** | doi LAYOUT: panel kem nua trai cho ca 4 khoi chu / anh chan phoi tren hien go nua phai. Chu y nguyen |

**File prompt (ban DUNG THAT):** `06_VIDEO/30_futon-dani-uchinaoshi/`
- `thumb_prompts_FLOW.txt` — 3 prompt **bake san chu**, moi prompt 1 dong, import thang extension
- `thumb_prompts_BLOCKS.md` — ban nguoi doc (khung khoi + bang so do + bang chu + 4 buoc sau khi gen)
- `thumb_prompts_TENFILE.txt` — thu tu dong ↔ ten file `thumb_T1/T2/T3_*.png`
- `thumb_prompts_PLATE.txt` — 3 plate **KHONG chu** (duong lui neu kanji gen nat) — **file rieng, dung tron vao FLOW**

Do may: **TEXT @6–7% (tran 15%) · 1.295–1.491 ky (tran 1.500)** ✅

⛔ **Bo prompt cu cua muc nay (kieu `No text, ... for text overlay`) DA HUY** — no vi pham
`ab-3title-3thumb.md` §3 muc 8 (bake chu vao anh, moi kenh, chot 2026-08-10).

🔴 Gen xong: soi TUNG ky tu (`逆`/`費` nhieu net) → **va ✦, KHONG cat** (bake chu ⇒ chu hero chay toi ~0,97W)
→ `stamp_brand.py --pos tr` → duyet 3 cua + 120px. Chi tiet o `thumb_prompts_BLOCKS.md`.

---

## §4 CÒN LẠI TRƯỚC KHI RENDER

1. **Render demo giọng 1–2 đoạn** (`humanize-script-voice.md` §3) — nghe khối đỉnh bài `[間1.2][速0.8][後間1.0]掃除機は、正しい。` và câu thoại mẹ 「綿は、くたびれるだけよ。死にはせん」 trước khi synth cả bài.
2. Dựng Remotion theo khuôn #25 (`build_remotion_30.py`) — style **anime**, không cast 2 mép.
3. **Tick "Altered or synthetic content"** khi upload (ảnh AI realistic trong video) — tool chưa có cờ, phải tick tay.
4. ✅ **Thumbnail T2 XONG + GÓI UPLOAD XONG 2026-09-09** — `_upload/` (mp4 SEO `futon-dani-kanboshi-taiji.mp4` + `subs.srt` + `thumbnail.png`/`thumbnail_T2.png` + `METADATA.txt` có 23 chương + pinned comment), hẹn **2026-09-11 (T6) 13:00 JST**.
   🔴 **CÒN THIẾU T1 + T3** → gate 3×3 hở 1/3, Test & compare không chạy được. Prompt sẵn ở dòng 1 và 3 của `06_VIDEO/30_.../thumb_prompts_FLOW.txt`.
   ⚠️ Khi bấm Schedule: **TICK Altered content** (slide là ảnh AI realistic) · credit giọng VOICEVOX nằm ở **pinned comment**, không ở 概要欄 (ngoại lệ co-dai).
