# 29 — なぜ祖母の包丁は40年もったのか（砥石の面直し・研ぎ汁・かえり）

> **Chế độ B (viết mới)** · trục 🔥 **忘れられた技術** · 2026-09-04
> `TARGET_QUERY: 包丁` · `INTENT: やり方`
> File đọc: `29_hocho-togi-mennaoshi_TTS.md` — gate `check_coldopen.py 29` = ✅ **PASS 0 FAIL 0 WARN**

## 0. SPEC + GATE

| | |
|---|---|
| Độ dài | **5.661 ký ≈ 18′34″** (@305 ký/phút, đã trừ tag) |
| Gate | **v3**: vào bài **~28s** · cửa sổ 45s **0 câu không trả tiền** (v2: 1) · gap payoff max **0′43″** (trần 2′30″) |
| Sóng | **6 chặng ĐIỀU TRA** (không phải 5 mẹo) · **16 cú lật** (v2: 14) · **8 câu MỞ** · loop lớn đóng ở **90%** |
| Tag nhấn nhá | **32 tag** · tag giữa câu **0** · tag đứng dòng riêng **0** · đỉnh bài `[間1.2][速0.8][後間1.0]` ở 「新聞紙です。」 |
| Chất người | **6/6** — ① tự trào (không đợi nổi 10 phút ngâm đá) ② 研ぎ屋のご主人 thoại 「包丁じゃなくて、石を見せてごらん」 + radio bóng chày ③ ký ức giác quan (bà trải báo ở hiên cuối năm, tiếng シャッシャッ, nước đục trắng, mùi đá-sắt như sau mưa) ④ người kể tự làm ⑤ **đóng bằng VẬT**: con dao của bà mòn thành lá liễu quay lại ở câu áp chót ⑥ phá nhịp ≥3 lần |
| Trục | 🔥 忘れられた技術 — **đến hạn** (lần cuối #25, cách 4 video) · khác trục #28 (🏠 家の手入れ) ✅ · không phải 害虫 ✅ |
| Khuôn thumbnail | **B1 (bright) lồng K3 (macro hero)** — tránh **K6** (#28) + **K7** (#27) đúng chỉ thị |

## 0.1 ⭐ VÌ SAO ĐỀ NÀY — và 🔴 SỬA PHÉP ĐO (2026-09-04, cùng ngày)

### 🔴 ĐỌC TRƯỚC — bản đầu của mục này SAI THANG, đã sửa

Bản đầu ghi `包丁 ≈857 thang kênh` và gọi đề này là **"đang trend"**. **Cả hai đều sai**, và cách sai
đáng ghi lại vì nó sẽ lặp:

1. **Đo trên 30 ngày, mà 30 ngày đó có MỘT SPIKE.** Chuỗi 32 điểm của `包丁` là
   `2 3 3 3 3 3 3 3 2 3 3 3 **100** 3 3 2 3 …` — **31/32 điểm là 2–3**, đúng **một ngày**
   (2026-08-16) bằng 100. Google chuẩn hoá cả rổ theo đỉnh đó ⇒ **mọi con số trong rổ bị bóp méo**,
   kể cả anchor. `mean 5,9` chỉ là trung bình của một cột đơn độc.
   ⇒ Related 12 tháng cho biết spike là gì: `プリ姫ママ 包丁 振り回す` (kênh giải trí trẻ em) —
   **nhiễu ngoài ngách**, không phải cầu 研ぎ.
2. **"mean cao" ≠ "đang lên".** Mean đo **VOLUME**, không đo **SLOPE**. Muốn biết lên/xuống phải so
   nửa đầu ↔ nửa sau của một khung DÀI.

### Số ĐÚNG — đo lại trên khung 12 THÁNG (không bị spike bóp méo)

| keyword | mean 12m | ≈ thang kênh | **xu hướng 12m** | xu hướng 5 năm | đọc |
|---|---|---|---|---|---|
| フライパン (anchor, đề #22) | 40,6 | 585 | −10,6% | +54,6% | mốc so |
| **包丁** | **20,3** | **≈292** | **−2,6% = PHẲNG** | +3,9% | ⭐ **EVERGREEN, không phải trend** — gấp **2,1×** `換気扇` (137, đề #27) |
| カビ | 14,0 | ≈202 | −0,8% | — | 🟡 (bản đầu ghi nhầm 685) |
| さつまいも | 47,8 | ≈690 | **−36,4%** | — | ❌ cầu lớn nhưng **đang rơi mạnh** + intent `レシピ` = sai tệp |
| 換気扇 (đề #27, đo 2026-08-31) | — | 137 | −20,0% | +25,2% | mùa vụ 大掃除 |

⚠️ **Những từ bản đầu tuyên bố "= 0"** (`干し柿`・`渋柿`・`米 保存`・`押し入れ`・`秋 掃除`・`衣類 防虫`)
**cũng đo trong rổ có spike** ⇒ con số 0 đó **không đủ tin để kết luận là chết**. Muốn loại hẳn thì
phải đo lại trên 12 tháng. Hiện chỉ kết luận được: chúng **nhỏ hơn `包丁` nhiều lần**.

### Ổn định theo tháng — đây mới là lý do chọn

`包丁` mean theo tháng, 13/13 tháng liên tiếp: **18,8 – 21,8**, không tháng nào sụt.

```
2025-08 19,0 │ 2025-11 21,2 │ 2026-02 20,8 │ 2026-05 20,2 │ 2026-08 21,6
2025-09 19,2 │ 2025-12 21,8 │ 2026-03 18,8 │ 2026-06 19,2 │
2025-10 18,8 │ 2026-01 21,8 │ 2026-04 20,8 │ 2026-07 19,2 │
```

⭐ **Đỉnh là 11月–1月 (21,2 / 21,8 / 21,8) = 年末の包丁研ぎ**, đáy là 3月 và 6–7月.
Tháng 9 = **19,2**, tức **thấp hơn đỉnh 13%**. Chênh nhỏ, **không đáng đổi đề** — nhưng ghi rõ:
**đây là bài NÊN được đẩy lại (hoặc làm tập 2) vào giữa tháng 12.** Và nó tình cờ khớp với ký ức
trung tâm của bài (「年の暮れになると、母が縁側で…」).

### INTENT — thứ duy nhất KHÔNG đổi sau khi sửa thang

`包丁 研ぎ` đứng **#1 = 100** ở **CẢ HAI** khung (30 ngày lẫn 12 tháng) — đây là bằng chứng mạnh vì
nó không phụ thuộc spike:

- **top 12m:** `包丁 研ぎ`(100) · `おすすめ包丁`(21) · `包丁の研ぎ方`(16) · `出刃包丁`(14) · `包丁 使い方`(8) · `包丁 研ぐ`(6)
- **rising 12m:** `包丁 研ぎ職人`(40) · `三徳包丁`(50) · `柳刃包丁 おすすめ`(60)
- **rising 30d:** `包丁 研ぎ方 初心者`(48.100) · `燕三条 包丁`(19.900)

⇒ INTENT = **やり方**, 0 modifier `効果`/`意味ある` ⇒ qua gate O16. Người gõ `包丁` trên YouTube
**chủ yếu đang tìm cách mài** — đúng bài này.

### ⇒ Kết luận sau khi sửa: GIỮ ĐỀ, ĐỔI CÁCH NÓI

Lý do chọn **không phải** "từ khoá đang lên" mà là: **cầu lớn (2,1× đề #27), phẳng suốt 13 tháng,
intent trùng khít nội dung**. Với kênh đang sống bằng search (80% impressions — `CHANNEL_DIAGNOSIS_2026-08-12`),
một từ khoá evergreen **tốt hơn** một từ đang spike: video sống lâu, không phụ thuộc sóng tin tức.

### 🔧 LUẬT MỚI CHO MỌI LẦN ĐO SAU (bổ sung `youtube-upload-seo.md` §0.5)

1. **Luôn in cả chuỗi điểm, đừng chỉ đọc `mean`.** Một cột 100 giữa toàn số 2–3 = spike, không phải cầu.
2. **Thang kênh phải đo trên khung 12 THÁNG**, không phải 30 ngày. 30 ngày chỉ dùng để bắt mùa vụ tức thời.
3. **Muốn nói "đang lên" thì phải có SLOPE** = so nửa đầu ↔ nửa sau của khung 12m/5y. Không có slope thì
   chỉ được nói "cầu lớn/ổn định".
4. Kiểm **related trên khung 12 THÁNG** (ổn định hơn 30 ngày) để loại nhiễu ngoài ngách.

## 1. 🌊 BỘ XƯƠNG — MẠCH ĐIỀU TRA (v3 thay hẳn model "5 mẹo" của v2)

### 🔴 VÌ SAO PHẢI VIẾT LẠI — v2 PASS gate mà vẫn chỉ đáng 6,5/10

v2 qua sạch 10/10 gate. Nhưng chạy **phép thử của chính project** (topic log, đề Edo:
*"bỏ khối 3 đi thì khối 5 có còn hiểu được không?"*) thì lộ ra ngay: 5 sóng của v2 là
`面直し / 番手 / 水 / 角度 / かえり` — **bỏ sóng 番手 đi, sóng 角度 vẫn hiểu nguyên vẹn.**
⇒ Đó là **DANH SÁCH PHẲNG**, đúng thứ làm sàn tụt 41,7% → 16,7%, và gate **không đo được**.

Hai lỗi nữa v2 mắc mà gate cũng không thấy:
1. **Bài đứng sai sân.** v2 là một bài *hướng dẫn mài dao*. Trên YouTube, cửa đó đã có thợ thật
   quay cận cảnh tay — kênh faceless + TTS + ảnh **không thể thắng ở "hướng dẫn"**.
2. **Không có thứ gì "bị thất lạc".** 番手・水・角度 là kiến thức phổ thông, search 30 giây ra hết.

### ⇒ v3 đổi SÂN: không bán "cách mài", bán **"vì sao thứ này bị mất"**

```
0:00  COLD OPEN (45s) — HAI CON DAO ĐẶT CẠNH NHAU
      祖母の包丁40年: 刃が磨り減って幅はもとの3分の2、柳の葉のよう
        → それでも熟したトマトに、指先の力だけですっと入る
      私の包丁3年目: 形は買った日のまま → 皮の上を滑り、指先が白くなるほど押しても入らない
      ⭐「さて、だめなのは、どちらでしょうか」 ← nghịch lý + câu hỏi, KHÔNG giải thích ngay
      mẹo 1 vào ~28s: 砥石の真ん中に鉛筆で線を1本塗る → 10秒研ぐ → 真ん中だけ残ったら…
      LOOP LỚN:「いちばん効く道具は、砥石でも包丁でもありません。台所にある、紙です」
1:00  chào kênh + CTA đăng ký (SAU mẹo 1 — O4)

── MẠCH ĐIỀU TRA: loại từng nghi phạm, mỗi lần loại là một cú lật ──

1:10  ①「包丁のせいではない」
      「昔の鋼はよかった」→ ところが合わない: 買った日には切れていた (貝印 15度で出荷)
      = 刃は最初からついていた。減ったのではなく、丸くなった
      祖母の40年 = 何百回研いだ証拠 / 私の3年が形のまま = 研がれなかった証拠
      MỞ:「では研げばいいのか。ところが、いちばん"切れない"と嘆くのは、研いでいる人たち」
3:10  ②「腕のせいでもない」
      堺: 鍛冶/刃付け/柄付けの三職 · 刃付けだけで10以上の工程 · 鍛冶10〜15年
      1543年 鉄砲とたばこ → たばこ包丁 → 幕府の「堺極印」で専売
      ⭐ ここで話が合わなくなる: 祖母は職人ではない。畑と台所と縫い物の人だった
      MỞ:「職人と祖母が二人とも持っていて、私たちだけが持っていないものは何か」
5:30  ③ 砥石 — CÚ LẬT TRUNG TÂM
      石は必ず真ん中からへこむ (力が集まるのは中央 · あなたの手もそうではありませんか)
      → 刃先は谷に落ち、当たるのは刃の腹 → 研げば研ぐほど刃先は丸くなる
      =「研いでいる人ほど切れない」の正体
      確かめ: 鉛筆 / 定規・コップの縁を立てて光の筋 (髪の毛が数本入るかどうか)
      直し: 貝印「必ず面直し用砥石で平らになるまで」· 60番 (藤次郎も60番) · コンクリートで代用
      研ぐ前30秒 + 研ぎ後30秒
8:00  ④ ⭐⭐「なぜ誰も教えなかったのか」 — TRÁI TIM CỦA BÀI
      意地悪ではない。逆。職人には当たり前すぎた
      毎日研ぐ人は毎日直す → 職人はへこんだ砥石を見たことがない → 注意のしようがない
      家庭は年に一度 →「直す」という一手間だけが、誰の口にも上らないまま消えた
      ⭐「失われた技術は、難しいから失われるのではない。
         当たり前すぎて、誰も口に出さなかったから消える」
9:20  ⑤「毎回、二つ捨てている」
      一つ目 = 白い研ぎ汁 (石の粒 + 鉄の粉 = いちばん細かい研磨剤) → 流すな、指で伸ばせ
        ký ức: 祖母が縁側に新聞紙を敷いて研ぐ · シャッシャッ · 白く濁った水 · 石と鉄の雨上がりの匂い
      二つ目 = 10分の時間 (貝印: 気泡が出なくなるまで10〜20分沈める)
        乾いた石 = 熱を持たせるだけ / 含水 = 粒が崩れて新しい角が出続ける
        ⭐「減らないように大事に使う。それがいちばんの間違いでした」
      ついで: 番手 (荒80〜400 / 中600〜2000 / 仕上3000〜6000 · 80番は砂利、8000番は小麦粉)
        → 家庭は800〜1000の一本 (藤次郎) · 荒砥で削る = 祖母の40年を3年に縮める
      MỞ:「ところが、いちばん多い失敗はこの先。終わり方を知らないまま研ぎ続けること」
13:00 CTA giữa video (canonical §2.4) — đặt SAU câu MỞ (O14 ✅)
13:40 ⑥ 角度と、終わりの合図
      15度 = 10円玉2枚を差し込む · 小刃の幅が基準 (藤次郎) · しゃくり研ぎ · 肘で動かす
      握力 (スポーツ庁): 30歳代ピーク → 男性30代前半46キロ / 70代後半35キロ
        →「力が落ちていく手にとって、切れない包丁は食材の上を滑って指に当たる道具」
      かえり: 髪の毛1本分 (貝印・藤次郎とも同じ基準) · 指を通す · ない場所はあと10回
      残すと最初の2、3回で折れる =「研いだ直後だけ切れて3日で戻る」の正体
      [間1.2][速0.8][後間1.0]「新聞紙です。」 ← đỉnh bài
      新聞紙は落とす道具であり、確かめる道具でもある (垂らして刃を通す)
16:00 DÒNG TIỀN — 祖母の砥石は京都の石だった
      梅ヶ畑・鳴滝の合砥、鎌倉時代から → 昭和30年頃 人造砥石で需要消失 → 亀岡と熊本のみ
      研ぐ人はよい客ではない: 3,000円÷3年 = 10年で1万円 vs 数百円の砥石10年
      簡易研ぎ器 = ぎざぎざを作るだけ、角度を作り直していない
      → ĐÓNG LOOP (90%):「最後に置いておいた、あの一枚。
         新聞紙が家から消えかけているのも、同じ流れの中の話です」
17:20 KẾT 3 lớp
      ① 万能ではない (欠けた刃・波刃・セラミックは専門店へ)
      ② ⭐「失われたのは技術ではない。"直す"という一手間が当たり前だった、その当たり前のほう」
      ③ 研ぎ屋「包丁じゃなくて、石を見せてごらん」→ 去年、店じまい
        → 祖母の包丁は今も私の台所に →「あれは、すり減った包丁ではありませんでした。
           使い切られていた包丁でした」→ câu hỏi → 次回予告 → câu kết cố định
```

### ⭐ Ba thứ v3 có mà v2 không có

1. **Mạch nhân quả, không phải danh sách.** Phép thử: bỏ chặng ③ (砥石) thì chặng ④
   (なぜ誰も教えなかった) **mất nghĩa hoàn toàn**. ①②③ là chuỗi loại trừ nghi phạm — bỏ một cái
   là mất lý do tin cái sau.
2. **Có một thứ THẤT LẠC thật, và có lời giải thích vì sao nó thất lạc.** Đây là chỗ kênh này
   thắng được video của thợ: thợ dạy *cách làm*; không ai kể *vì sao ta đánh mất nó*.
3. **Vật xuyên bài thay cho khái niệm xuyên bài.** Con dao mòn thành lá liễu mở bài ở giây 0 và
   đóng bài ở câu áp chót. v2 mở bằng quả bí đỏ rồi bỏ quên nó luôn.

### Câu trả lời cho 2 câu hỏi user đặt

| | |
|---|---|
| **Người xem ĐẾN vì gì** | Gõ `包丁` / `包丁 研ぎ方` — họ đang bực: dao không cắt, hoặc mài rồi vẫn không sắc. Intent **やり方**. |
| **Người xem Ở LẠI vì gì** | ⛔ **Không phải vì hướng dẫn** — cửa đó thuộc về video quay tay thợ. Họ ở lại vì **một câu hỏi chưa được trả lời**:「なぜ祖母の包丁は40年もったのに、私のは3年でだめになったのか」, và vì cứ 2–3 phút lại có một nghi phạm bị loại. Thứ giữ chân là **mạch điều tra**, không phải danh mục mẹo. |

## 2. 📚 NGUỒN THẬT (đã fetch + verify 2026-09-04 — KHÔNG bịa)

| # | Fact dùng trong bài | Nguồn |
|---|---|---|
| 1 | 「へこんだ砥石は必ず面直し用砥石を使って、平らになるまで削りましょう」 | 貝印 包丁サイト — 包丁の研ぎ方 |
| 2 | かえり = 「髪の毛1本分ぐらいの引っかかり（バリ）を全体に感じれば、刃がついた」/ 新聞紙で両面をこすってバリを落とす | 貝印 (同上) |
| 3 | 人造砥石は「気泡がでなくなるまで(大体10〜20分程度)漬けておく」/ 天然砥石は水に漬ける必要なし | 貝印 (同上) |
| 4 | 番手: 荒砥#80–400 · 中砥#600–2000 · 仕上げ#3000–6000 · 超仕上げ#8000以上 / 初心者は#800–1000の中砥石のみで対応可能 | 藤次郎（燕三条）— 砥石の選び方 |
| 5 | 研げた基準 = 砥石の目による傷 + 反対側に出る「かえり」/ 小刃の幅 = その包丁の角度の基準 / 面直し砥石 #60 | 藤次郎 — 包丁の研ぎ方 |
| 6 | 両刃は約15度 ≒ 10円玉2枚分の隙間 / 貝印のステンレス両刃は15度で刃付けして出荷 | 貝印・和平フレイズ・堺實光（複数メーカー一致） |
| 7 | 握力は30歳代でピーク、以後加齢に伴い直線的に低下 / 男性 30–34歳 46.35kg · 65–69歳 39.70 · 75–79歳 35.20（女性 30–34歳 28.76 · 70–74歳 23.91） | **スポーツ庁「体力・運動能力調査」令和2年度報告書** 表1-1（本文「握力は…30歳代でピークレベルに達し」「ピーク以後加齢に伴い直線的に低下」） |
| 8 | 切れない包丁は力が要り、滑って手に当たる=大きなけがになりうる | 堺實光（明治33年創業）「切れない包丁は危ない！」 |
| 9 | 堺打刃物 = 鍛造・刃付け・柄付けの分業 / 刃付けは何種類もの砥石で10以上の工程 / 鍛造の習得10〜15年 / 1982年3月5日 伝統的工芸品指定 | **堺市 公式サイト** |
| 10 | 1543年 鉄砲とたばこ伝来 → 天正年間よりたばこ包丁 → 幕府が「堺極印」を附して専売 | **堺刃物商工業協同組合連合会** |
| 11 | 京都・梅ヶ畑（鳴滝の合砥・中山）は鎌倉時代から採掘 / 昭和30年頃 人造砥石の台頭で需要消失、ほとんど閉山 / 現在は京都府亀岡市と熊本県のみ | 天然砥石（各資料）— 本文で「記録によれば」と rào chữ |

⚠️ **令和2年度 là năm COVID nên mẫu nhỏ hơn thường lệ** (chính báo cáo tự ghi chú ở 留意点) → bài dùng số **làm tròn** (「およそ46キロ」「およそ35キロ」) và nêu rõ tên cơ quan.
⚠️ **消費者庁 Vol.612 (キッチンの刃物によるけが) đã tra và KHÔNG dùng** — dữ liệu là trẻ 1–4 tuổi, **sai tệp** 45–70. Ghi lại để lần sau không mất công tra lại.

## 3. 🖼️ ĐÓNG GÓI CTR

### Title CHỐT

```
なぜ祖母の包丁は40年もったのか――研いでも切れない、本当の原因
```

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜ祖母の包丁は40年もったのか――研いでも切れない、本当の原因` | 30 | 包丁@6 | keyword mạnh nhất trong rổ hợp tệp (**≈292** thang kênh, 12m) + khuôn `なぜ〜のか` + **con số 40年 dựng sẵn nghịch lý ngay ở title** |
| **A2** | `包丁研ぎで、絶対にやってはいけない3つのこと――3日で切れ味が戻る理由` | 33 | 包丁研ぎ@1 | đổi keyword dẫn sang `包丁 研ぎ` (related #1 = 100) + khuôn LỆNH CẤM |
| **A3** | `研ぎ屋はなぜ、包丁ではなく「石を見せろ」と言ったのか` | 25 | 包丁@8 | đổi kiểu hook: bí ẩn/nhân vật (câu thoại có thật trong bài) thay vì cơ chế |

### Tên file upload

```
hocho-togi-mennaoshi-toishi.mp4
```

### 概要欄 — 3 DÒNG ĐẦU

```
祖母の包丁は40年もったのに、私の包丁は3年で切れなくなりました。原因は包丁でも、腕でもありませんでした。
研いでも切れない・研いだ直後だけ切れて3日で戻る、という方へ。犯人を一つずつ消していく形で、砥石の面直しから、終わりの合図までをお話しします。
今夜、鉛筆1本で自分の砥石を確かめられます。かかるお金は数百円、時間は5分です。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ

```
祖母の包丁は40年もったのに、私の包丁は3年で切れなくなりました。原因は包丁でも、腕でもありませんでした。
研いでも切れない・研いだ直後だけ切れて3日で戻る、という方へ。犯人を一つずつ消していく形で、砥石の面直しから、終わりの合図までをお話しします。
今夜、鉛筆1本で自分の砥石を確かめられます。かかるお金は数百円、時間は5分です。

砥石は、使えば必ず真ん中からへこみます。力が集まるのが、いつも石の中央だからです。
へこんだ石で研ぐと、刃先は石の谷に落ち、当たっているのは刃の腹ばかりになります。
つまり、研げば研ぐほど刃先は丸くなる。これが「研いでも切れない」の正体です。

そして、いちばん不思議なのはここです。これほど簡単なことを、なぜ誰も教えてくれなかったのか。
答えは、意地悪だったからではありません。職人にとって、当たり前すぎたからでした。

この動画では、家庭の台所で今夜からできる形にして、次の順番でお話しします。
・砥石の面直し（60番の石、または平らなコンクリート面で。研ぐ前に30秒、研いだあとに30秒）
・番手の選び方（荒砥80〜400番／中砥600〜2000番／仕上げ3000〜6000番。家庭は800〜1000番の一本で足ります）
・水の入れ方（人造の砥石は、気泡が出なくなるまで10〜20分。白く濁った研ぎ汁は流さない）
・角度（10円玉2枚分の隙間、およそ15度。小刃の幅が、その包丁の基準です）
・終わりの合図（髪の毛1本分の「かえり」。落とすのは新聞紙一枚）

後半では、京都・梅ヶ畑で鎌倉時代から掘られてきた天然砥石が、昭和30年頃を境になぜ台所から消えたのか。
そして、大阪・堺で研ぎがなぜ「別の職人の一生の仕事」だったのかにも触れます。

【目次】
00:00 40年の包丁と、3年の包丁
01:22 ①包丁のせいではない ― 買った日には切れていた
02:36 ②腕のせいでもない ― 堺では研ぎは別の職人の仕事だった
03:59 ③犯人は砥石 ― 研げば研ぐほど刃先が丸くなる理由
06:04 ④なぜ誰も教えてくれなかったのか
07:02 ⑤毎回、二つ捨てているもの（白い研ぎ汁と10分）
10:44 ⑥角度は10円玉2枚 ― 力の落ちた手のために
13:08 終わりの合図「かえり」と、新聞紙一枚
15:09 なぜ、この技術は家庭から消えたのか
17:34 まとめ ― 失われたのは、技術ではありませんでした

【参考にした資料】
貝印「包丁の研ぎ方」／藤次郎「砥石の選び方」「包丁の研ぎ方」／堺市「堺打刃物」／堺刃物商工業協同組合連合会／スポーツ庁「体力・運動能力調査」令和2年度報告書

※刃物を扱う内容です。研ぐ際は手元に注意し、お子さまの手の届かない場所で作業してください。
※大きく欠けた刃、波刃のパン切り包丁、セラミック包丁は家庭用の砥石では戻りません。専門の店へご相談ください。
※本動画は生活の知恵をご紹介するものであり、特定の製品や事業者を批判する意図はありません。

#生活の知恵 #昔の知恵 #古代の秘訣
```

### タグ

```
古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, 包丁, 包丁 研ぎ方, 包丁研ぎ, 砥石, 面直し, 中砥石, 番手, かえり, バリ取り, 研ぎ方 初心者, 切れ味, 包丁 手入れ, 三徳包丁, 出刃包丁, 天然砥石, 鳴滝, 堺打刃物, 台所仕事, 道具の手入れ, 60代, シニア
```

## 4. 🎨 THUMBNAIL — B1 (bright) lồng K3 (macro hero)

**Vì sao K3:** cú lật của bài nằm **trong chính cái vật** (mặt đá lõm), nên một khung macro thuyết phục hơn mũi tên hay dấu ❌. Tránh **K6** (#28) + **K7** (#27) đúng chỉ thị sổ. K3 lần cuối lên sóng ở **#23, cách 5 video** ✅. Không mặt người (luật kênh 2026-08-05) — **bàn tay được phép**.

### Text 3 tầng (GIỐNG HỆT ở cả T1/T2/T3 — biến thử là HÌNH)

| tầng | chữ | vai |
|---|---|---|
| 1 (trên) | `包丁が切れない` | ① VỀ CÁI GÌ — chứa keyword dẫn `包丁` (**≈292** thang kênh đo trên 12m, gấp 2,1× đề #27) |
| 2 **HERO** | `砥石のへこみ` | ② CHUYỆN GÌ XẢY RA — 6 ký, cao nhất, rộng ~2/3 khung |
| 3 (dưới) | `研ぐほど鈍る` | nghịch lý |
| badge | `直しは30秒` | ③ PHẢI LÀM GÌ + mốc thời gian |

- **T1** baseline: đá mài macro nghiêng, thước thép đặt ngang, **khe sáng lọt ở giữa**.
- **T2** đổi ĐÚNG 1 biến hình: bỏ thước, thay bằng **lưới bút chì đã mài 10 giây — vệt giữa còn nguyên**, chữ y nguyên.
- **T3** đổi layout: panel chữ nửa trái / ảnh nửa phải (dao gác trên đá lõm, nhìn ngang), chữ y nguyên.

Prompt (bake chữ, 1 dòng/prompt): `06_VIDEO/29_hocho-togi-mennaoshi/thumb_prompts_FLOW.txt`
bản người đọc `_BLOCKS.md` · map tên file `_TENFILE.txt` · 3 plate KHÔNG chữ **file riêng** `_PLATE.txt`.
🔴 Gen xong **BẮT BUỘC xoá ✦ — bake chữ ⇒ VÁ, không cắt** (`media-library.md` §2.10⑤b) → `stamp_brand.py --pos tr`.
📌 **Video kế tiếp tránh K3 + K6.**

## 5. 📌 Pinned comment

```
最後までご覧いただき、ありがとうございます。今日の中で、まず試してみようと思われたのは、面直しでしたか、それとも新聞紙のほうでしたか。
皆さまのお宅に伝わる包丁や道具の手入れの仕方、「うちの父はこうしていた」というやり方があれば、ぜひ聞かせてください。皆さまの声を参考に、これからの内容も深めてまいります。
※刃物を扱う内容です。研ぐときは手元にご注意いただき、お子さまの手の届かない場所で作業なさってください。欠けた刃や波刃、セラミックの包丁は、無理をせず専門の店へご相談ください。🌿
```

## 6. ✅ COMPLIANCE (quét theo `youtube-compliance.md`)

- Title / thumbnail / 3 dòng đầu 概要欄: **0 từ nhóm cấm** (殺/血/死/自殺/レイプ/虐待). Từ 「切れない」「刃」 không thuộc danh sách; bài **không** đưa 「指を切る」 lên title/thumbnail.
- Không tên người/công ty kèm cáo buộc — chương dòng tiền nói **cấu trúc** (「売る側」「棚に並ぶのは」), tên hãng chỉ xuất hiện khi **trích nguồn kỹ thuật** (貝印・藤次郎・堺市) = trích dẫn, không phải cáo buộc.
- An toàn: đoạn dao/lưỡi + trẻ em có trong 概要欄 và pinned comment; giới hạn phương pháp nêu thẳng ở kết (lớp 1).
- Không cảnh AI realistic trong video ⇒ chưa cần tick synthetic ở lượt này; nếu dùng ảnh AI làm slide thì **tick** theo §2.1.

## 7. 🔴 CÒN LẠI (chưa làm)

1. **Render demo 1–2 đoạn** nghe trước (`humanize-script-voice.md` §3) — nhất là đỉnh bài 「新聞紙です。」 và đoạn ký ức mẹ.
2. **SLIDES + build Remotion** theo khuôn nenkin (`CLAUDE.md` §② — `build_remotion_25.py` → `build_remotion_29.py`).
3. ~~**3 thumbnail** T1/T2/T3~~ ✅ **XONG 2026-09-06** — user gen 3 bản → vá ✦ bằng `tools/strip_wm_star.py` (✦ lô này là NÉT TỐI, tool trung vị hàng cũ vá ra khối xám — `media-library.md` §2.10 mục 6c) → `stamp_brand.py --pos tr` → `thumb_T{1,2,3}_*.jpg|.png` trong `06_VIDEO/29_hocho-togi-mennaoshi/`.
4. ✅ **GÓI UPLOAD XONG 2026-09-06** — `_upload/` (mp4 SEO + subs.srt + 3 thumbnail + METADATA.txt), hẹn **2026-09-09 (T4) 13:00 JST**. 🔴 **目次 đã sửa theo `subs.srt` thật** (bản viết trước render lệch dần, chương cuối lệch ~60s: 16:38 → **17:34**). ⚠️ Khi bấm Schedule: **TICK Altered content** — slide là ảnh AI realistic (`youtube-compliance.md` §2.1); ô "概要欄 có credit giọng VOICEVOX" trong checklist của `upload_pack.py` **KHÔNG áp cho kênh này** (ngoại lệ co-dai: credit giọng để ở pinned comment).
5. Ghi đề vào `01_SOURCES/00_TOPIC_LOG.md` ✅ (đã ghi).
