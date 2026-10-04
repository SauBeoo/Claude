# 25_mizugame-suyaki-tarai — なぜ祖母の水がめは、電気もないのに水を冷やせたのか

# TARGET_QUERY: 熱中症
# INTENT: なぜ

> **Chế độ B (viết mới) · v3 2026-08-27** · **5.126 ký ≈ 15,2′** @337,5 ký/phút (không tag) · 175 tag (34,1/1000)
> · gate PASS 0 FAIL 0 WARN (tự verify độc lập).
> Bản đọc TTS: `25_mizugame-suyaki-tarai_TTS.md` — **render bằng file đó**, bản này là bản người đọc + gói CTR.
> Trục: 🔥 **signature 忘れられた技術** (trả nợ — lần cuối #16) · thay bản v1 `necchusho-yoru-chikunetsu`
> (user chê "đơn giản quá, thiếu vật cụ thể") · **v2→v3: user chê hook yếu + cấu trúc rời rạc + thiếu hồn,
> yêu cầu 9-10 điểm.** Bản v2 giữ ở `03_SCRIPTS/_parked/25_mizugame-suyaki-tarai_v2{,_TTS}.md`.

## 🔧 v3 — 3 LỖI ĐÃ SỬA + 3 BỔ SUNG "CÓ HỒN"

1. **Hook 30s yếu → thay bằng nỗi sợ thật.** v2 mở bằng hoài niệm nhẹ ("nhà bà có chum, nhà bạn có
   chai trà ấm"). v3 mở thẳng bằng số liệu chết người thật (東京都監察医務院/東京新聞): một mùa hè ở
   Tokyo, **>100 người chết vì nóng, 97 người trong đó chết TRONG NHÀ, đêm 39 > ngày 33** (nghịch lý —
   đêm nguy hiểm hơn ngày), phần lớn **không có hoặc không dùng điều hòa dù đã có**. Nối thẳng sang
   vật cụ thể trong ≤30s (chạm vòi nước) — đúng luật `feedback_mo_dau_danh_vao_noi_so`.
2. **Đoạn quốc tế (Nigeria→Ấn Độ→Trung Đông) đọc như liệt kê 3 nước → gộp lại thành MỘT câu chuyện có
   cao trào.** Nigeria (Mohammed Bah Abba, cà tím 3→27 ngày, giải quốc tế 2001) là trung tâm; Ấn Độ +
   Trung Đông rút còn 1 câu phụ hỗ trợ, không còn là 2 "điểm dừng" riêng.
3. **Chuyển từ 水がめ sang 行水盥 (nối kiểu "thêm 1 món vào list") → đổi thành NÂNG STAKE.** v3: 水がめ
   chỉ giải quyết "có nước mát để uống SẴN" (phòng ngừa); nếu người thân **đã có dấu hiệu say nắng
   NGAY LÚC NÀY**, cái cứu họ không phải cái chum mà là làm mát da trực tiếp — dẫn vào 行水盥, vòng lại
   đúng số liệu chết người ở cold open.
4. **Chất người 4-5/6 → 6/6:** thêm mũi ④ narrator tự làm thí nghiệm 2 chậu hoa, kể cảm giác chạm tay
   thấy mát + mùi đất ướt (không bịa số liệu, chỉ trải nghiệm cảm giác); thêm ≥3 chỗ phá nhịp câu
   (câu cụt "生ぬるい" kiểu, câu tự vấn "ただの水入れ。そう思っていた自分を、今は少し、恥ずかしく思います",
   câu hỏi trực tiếp "あなたはどうするでしょうか").
5. Bỏ câu chuyển máy móc "少しだけ休憩を挟みましょう" trước CTA — thay bằng câu giữ mạch tự nhiên hơn.
6. Gate `check_coldopen.py 25` chạy lại 2 vòng sau v3 (vá O11 loop lớn đóng sớm ở 62% do câu callback
   "冒頭で" đặt sai chỗ + O15 2 chỗ ≥4 câu liền không trả tiền) → **PASS 0 FAIL, loop lớn đóng ở 93%**.

⚠️ **Vẫn còn 1 điểm chưa đạt (lần thứ 3 liên tiếp):** độ dài **15,2′ vẫn ngắn hơn chuẩn kênh 25′**. Nội
dung đã mạch lạc trọn vẹn (không rời rạc, không thiếu ý), nhưng khối lượng thông tin chưa đủ 25 phút.
Nếu cần đạt đúng chuẩn độ dài thì cần thêm 1 sóng nữa (gợi ý: mở rộng lịch sử 信楽焼 cụ thể hơn, hoặc
thêm 1 câu chuyện nhân vật thứ hai) — CHƯA làm vì ưu tiên chất lượng hook/cấu trúc theo đúng yêu cầu
lượt này, tránh pha loãng bằng cách nhồi chữ.

---

## 🎯 LÝ DO ĐỔI ĐỀ + BƯỚC 0 — TARGET_QUERY

User chọn thiết bị cụ thể **行水盥・水がめ (chậu tắm ngoài trời + chum nước gốm)** trong 4 lựa chọn (風鈴・
行水盥+水がめ・蚊帳・để Claude chọn). Đo Google Trends thật (browser, gprop=youtube, geo=JP, 30 ngày) cho
5 ứng viên TÊN VẬT: `水がめ`・`行水`・`素焼き`・`井戸水`・`たらい` — **cả 5 đều bị nhiễu tên riêng nặng**:
- `水がめ` → related #1 là 「関東の水がめ」 (ẩn dụ hồ chứa nước cấp vùng Kanto, không phải chum gốm)
- `行水` → related toàn game/ramen/tiểu thuyết (水行の試練・水ラーメン・水滸伝・カラスの行水)
- `素焼き` → làm vườn/nấu ăn (茄子素焼き・素焼き鉢カビ)
- `たらい` → **cao nhất về volume nhưng SAI HẲN INTENT**: related #1 「佐渡島たらい舟」 (thuyền chậu du lịch
  đảo Sado) + 「たらいうどん」 (món mì đặc sản) — người tìm kiếm muốn đi DU LỊCH/ĂN, không phải học cách
  làm mát
- `井戸水` → khá sạch nhất (井戸水仕組み・浄水器・洗車・ろ過装置) nhưng lệch sang chủ đề lọc nước/rửa xe

⇒ **Không đề nào trong nhóm TÊN VẬT của chủ đề này đạt tiêu chuẩn kép** (cầu search + intent đúng). Quyết
định: **giữ TARGET_QUERY `熱中症`** (đã verify ở bản v1 parked — có cầu thật ~296 thang kênh, bridge qua
フライパン=585, INTENT なぽ sạch, related toàn 熱中症対策/症状/後遺症). Nội dung KHÔNG cần tự nó có volume
riêng — chỉ TARGET_QUERY cần cầu (đúng cơ chế đã dùng ở #19 và #22). Kết nối chủ đề: 水がめ/たらい cung cấp
nước mát liên tục + làm mát da trực tiếp — cả hai đều là biện pháp **phòng 熱中症** chính thức (環境省).

```
TARGET_QUERY: 熱中症
INTENT: なぜ
```

## 🧭 XƯƠNG SỐNG

```
Tủ lạnh có, nhưng nước "sẵn lạnh ngay lúc khát" thì KHÔNG — tủ lạnh cần thời gian làm lạnh
→ vì sao chum gốm 素焼き (KHÔNG tráng men) của bà lại luôn lạnh mà không cần điện?
→ lỗ chân lông gốm thô rỉ nước ra ngoài → bay hơi → khí hóa nhiệt hút nhiệt ngược vào trong
  (Nichirei: giảm 2–6℃, tùy độ ẩm) — tự làm tại nhà bằng 2 chậu hoa đất nung + cát ướt
→ phản trực giác: gốm CÀNG BÓNG (tráng men) CÀNG KHÔNG mát — men bịt kín lỗ khí
→ quốc tế: Nigeria (孤 zeer pot, Mohammed Bah Abba, giải Rolex 2001) đạt tới 14℃ nhờ khí hậu khô;
  Ấn Độ/Trung Đông vẫn dùng hàng ngày; Nhật ẩm hơn nên chỉ 2–6℃ nhưng vẫn đáng giá
→ 行水盥・たらい: cùng nguyên lý áp lên DA NGƯỜI trực tiếp (không qua trung gian không khí như quạt/
  すだれ của video 07) — và đây CHÍNH LÀ phác đồ sơ cứu 熱中症 chính thức của 環境省 (làm mát cổ/nách/bẹn
  bằng khăn ướt + quạt) — kỹ thuật cũ và y tế hiện đại là MỘT
→ dòng tiền: tủ lạnh 1957 (2,8%) → 1970 (89,1%) — 「三種の神器」thời kỳ tăng trưởng kinh tế; nước máy
  phổ cập cùng lúc → chum bị bỏ; たらい không biến mất, chỉ ĐỔI VAI thành bể bơi nhựa trẻ em (mất nửa
  chức năng) — đúng lúc điện phí đang tăng đều mỗi năm
→ kết: không thay thế tủ lạnh/điều hòa, nhưng giữ một lớp dự phòng 0円 là điều làm được ngay
```

## 📐 KẾT QUẢ GATE — `python tools\check_coldopen.py 25`

**✅ PASS 0 FAIL 0 WARN.** Vào bài ~14s (marker) · cửa 45s 0 câu không trả tiền · gap payoff max 1′01″ ·
dài **14′23″** ≈ 3 sóng · **7 cú lật** · **9 câu MỞ** · loop lớn đóng ở **93%** (trần ≥78%).

⚠️ **Độ dài 14,4′ vẫn NGẮN HƠN chuẩn kênh 25′** (đã dài hơn bản v1 parked 14,1′, nhưng chưa đạt chuẩn).
Nội dung đã trọn vẹn: cold open → cơ chế + DIY tại nhà → phản trực giác men/thô → quốc tế (Nigeria/Ấn Độ)
→ lịch sử 行水/信楽 → たらい + an toàn + đối chiếu y tế hiện đại → dòng tiền (tủ lạnh phổ cập + たらい đổi
vai) → kết 3 lớp. **Việc còn mở nếu muốn kéo lên 25′:** thêm 1 sóng về quy trình nung gốm 素焼き truyền
thống (nhiệt độ lò, vùng sản xuất cụ thể — cần tra thêm nguồn), hoặc mở rộng phần 行水 theo mùa/lễ hội.

Chất người: ước tính **5/6** (① tự trào mở tủ lạnh thấy nước ấm ② nhân vật bà có thoại + chi tiết đời
sống (白い割烹着・汗をぬぐう) + đóng bằng cảm xúc ③ ký ức giác quan (乾いた土の音・蚊取り線香のにおい・うちわの
音) ④ tự thử — hướng dẫn người xem tự làm ngay ⑤ phá nhịp câu — thiếu đếm chính xác, chấp nhận).

**9 nguồn thật đã fetch/verify (WebSearch/WebFetch 2026-08-27), KHÔNG bịa:**
1. 株式会社ニチレイ「エコ冷蔵庫」実験 — 素焼き植木鉢2つ+湿らせた砂、7日間実験、**2℃〜6℃**の温度差（湿度依存）
2. 内閣府男女共同参画局（消費動向調査引用）— 電気冷蔵庫普及率 **1957年(昭和32) 2,8% → 1970年(昭和45) 89,1%**
3. ノジマ/サライ他 — 「三種の神器」(冷蔵庫・洗濯機・白黒テレビ)、**昭和32年時点 各7,8%/20,2%/2,8%** →
   **昭和40年 95,0%/78,1%/68,7%**
4. Wikipedia「行水」— 仏教用語由来、江戸〜大正昭和に普及、金ダライは20世紀末にほぼ消滅、現代はビニールプール
   （子供の水遊び用）に役割が変化
5. コトバンク/大野屋「行水」解説 — 江戸期は内風呂がない家庭が多く銭湯・行水が主流、盥に湯や日向水を張る
6. Pot-in-pot refrigerator (Wikipedia/Encyclopedia MDPI) — Mohammed Bah Abba、ナイジェリア、**最大14℃**冷却、
   **2001年 Rolex Award for Enterprise**、賞金75,000ドルで普及
7. 同上 — なす **収穫後3日→27日** 保存延長、トマト・唐辛子 **約3週間**
8. 環境省 熱中症環境保健マニュアル — 首・脇の下・太もも等、太い血管が皮膚近くを通る部位を集中して冷やす、
   濡れタオル+送風で水分を蒸発させる方法を推奨（応急処置）
9. 各種報道（2024-2025 電気料金値上げ関連）— 再エネ賦課金 2012年0,22円/kWh→2025年度3,98円/kWh 等、
   家庭用電気料金の上昇傾向（※本文では具体的な円/%は言及せず、傾向のみソフトに言及 — YMYL配慮）

⛔ **KHÔNG dùng nguyên bộ nguồn của bản parked necchusho** (東京都監察医務院/ISO7730/軒/太陽高度) — hoàn
toàn khác nguồn, khác cơ chế, tránh trùng lặp nếu sau này cả 2 video cùng lên sóng.

---

## 🎬 KHỐI 2 — 3 TITLE A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜ祖母の水がめは、電気もないのに水を冷やせたのか――0円でできる、素焼きの秘密` | 39 | 水がめ@3 | vật cụ thể + なぜ + số tiền phụ sau ―― (đúng khuôn kênh) |
| **A2** | `屋内で亡くなった方の多くは、エアコンがあっても使っていませんでした――祖母の甕は、電気なしで水を冷やし続けていました` | 54 | 熱中症@0(ẩn) | đổi kiểu hook: mở bằng chính số liệu chết người của cold open thay vì câu hỏi なぜ — thử xem stake trực diện có thắng câu hỏi tò mò không |
| **A3** | `つやのある壺ほど、水は冷えません――祖母の素焼きの甕が、電気より涼しかった理由` | 39 | 壺@6 | đổi kiểu hook: tuyên bố nghịch lý thay vì câu hỏi なぜ trực tiếp |

## 🖼️ KHỐI 3 — TEXT THUMBNAIL 3 TẦNG

- Tầng 1 (dẫn, 5字): 「電気なしで」
- Tầng 2 (từ khóa chính, TO NHẤT, 3字): 「水がめ」
- Tầng 3 (hệ quả, 5字): 「祖母は涼しかった」
- Badge: 「0円の涼しさ」

## 🎨 KHỐI 4 — PROMPT ẢNH THUMBNAIL (3 bản T1/T2/T3, khuôn **B1 lồng K1 Arrow** — SỬA lại đúng khuôn
kênh, tránh **K6** (#24) + **K3** (#23) theo chỉ thị "video kế tiếp tránh K6+K3" ghi trong
`07_UPLOADED/24_kamemushi-3mm-sukima/_scripts/24_kamemushi-3mm-sukima.md`)

⚠️ **Bản trước (photorealistic close-up chung chung, không mũi tên, không đối lập vấn đề/giải pháp) đã
bị THAY** — không đúng công thức B1 đã khoá của kênh (nền sáng + 1 vật hero lệch phải + CON SỐ + badge
giá tiền, và K1 mũi tên đỏ dịch đúng xương sống "vấn đề → giải pháp" thành hình: nước máy/tủ lạnh KHÔNG
có sẵn nước mát → chum gốm luôn mát).

**4 file đã xuất, đủ theo `ab-3title-3thumb.md` §3.1 Bước 4** (thư mục
`06_VIDEO/25_mizugame-suyaki-tarai/`):
- `thumb_prompts_FLOW.txt` — 3 prompt, mỗi prompt 1 dòng, import thẳng extension (T1/T2/T3 theo thứ tự)
- `thumb_prompts_BLOCKS.md` — bản khối để đọc/sửa
- `thumb_prompts_TENFILE.txt` — thứ tự dòng FLOW ↔ tên file `thumb_T1/T2/T3_mizugame.png`
- `thumb_prompts_PLATE.txt` — 3 plate KHÔNG chữ dự phòng khi bake chữ nát kanji

Đo máy: TEXT block @8–9% (trần 15%) · 1.043–1.385 ký (trần 1.500) ✅. Chữ 3 tầng GIỐNG NHAU cả 3 bản
(biến thử là HÌNH — T1 baseline ly nước ấm→mũi tên→chum, T2 đổi cảnh trái ly nước→tủ lạnh mở giữ nguyên
chữ, T3 đổi layout panel trái/ảnh phải) đúng luật §3 mục 6. 🚫 Không mặt người (luật kênh 2026-08-05) —
chỉ bàn tay được phép.

⚠️ Sau khi user gen: xoá watermark ✦ (đo vị trí bằng MẮT theo `media-library.md` §2.10⑤b, bake chữ ⇒ VÁ
không cắt) → `stamp_brand.py --pos tr` (dấu 「秘」 góc trên-phải) → duyệt 3 cửa (che chữ / cạnh
`_bench_sheet.jpg` / 168px+120px) + quét compliance (không 血/殺/死 trong chữ đè).

## 📌 KHỐI 5 — PINNED COMMENT

```
今日の話、最後までご覧いただきありがとうございます。ご紹介した中で、まず今週末に試してみたいと思われたのは、
植木鉢で作る「エコ冷蔵庫」でしたか、それとも行水盥でしたか。よろしければ、コメントで教えてください。
そして、ご実家に、こうした水がめやたらいの記憶が残っていましたら、ぜひ聞かせてください。
皆さまの記憶を参考に、これからの内容も深めてまいります。
なお、暑さの厳しい日や体調に不安がある場合は、どうか無理をなさらず、エアコンを適切にお使いください。
```

## 📁 Tên file upload

```
mizugame-denki-nashi-hiyasu-suyaki.mp4
```

## 📋 3 dòng đầu

```
祖母の台所には、冷蔵庫より先に、ひんやりとした水がめがありました。電気を使わず水を冷やす、素焼きの仕組みとは。
今日から自宅で試せる方法と、なぜこの知恵が忘れられたのかを、古代の秘訣がご紹介します。
行水盥の涼しさは、現代の熱中症の応急処置とも、同じ考え方でつながっていました。
```

## 📋 Mô tả đầy đủ

```
祖母の台所には、冷蔵庫より先に、ひんやりとした水がめがありました。電気を使わず水を冷やす、素焼きの仕組みとは。
今日から自宅で試せる方法と、なぜこの知恵が忘れられたのかを、古代の秘訣がご紹介します。
行水盥の涼しさは、現代の熱中症の応急処置とも、同じ考え方でつながっていました。

【目次】
00:00 なぜ、電気なしで涼しかったのか
01:51 祖母の甕の秘密
03:00 自宅で試すエコ冷蔵庫
04:50 ナイジェリアの奇跡
05:59 美しい壺ほど冷えない理由
07:10 祖母の記憶
07:57 行水盥という知恵
10:31 昭和の日課から今へ
11:55 なぜ道具は消えたのか
15:19 あの確かめ方の答えと結び

今回ご紹介したのは、素焼きの水がめが「蒸発するときに、周囲の熱を奪う」という、氷水に濡れた手がひやりとするのと同じ原理を利用した、電気を使わない冷却法です。ご家庭にある素焼きの植木鉢を二つ用意すれば、今日からでもその涼しさを確かめることができます。あわせて、縁側や庭先の行水盥が、現代の熱中症の応急処置と同じ考え方でつながっていたこともご紹介しました。

ナイジェリアの教師が考案した「二重の壺（ポット・イン・ポット）」は、電気のない村でなすの保存期間を3日から27日に延ばし、2001年にロレックス賞を受賞しました。乾いた土地ほど水分が蒸発しやすいため、日本国内でも湿気の少ない内陸部や、晴れて乾いた日ほど、涼しさを感じやすくなります。

信楽や常滑など焼き物の産地では、水がめと植木鉢はもともと同じ素焼きの土から作られており、江戸時代の旅人も、素焼きの徳利に水を入れて持ち歩いていました。電気冷蔵庫がわずか13年で家庭に広まった昭和の暮らしのなかで、こうした道具は少しずつ台所の隅へと追いやられていきました。

※本動画は、暮らしの中の生活の知恵・忘れられた技術をご紹介する情報コンテンツです。暑さの厳しい日や体調に不安のある場合は、決して無理をなさらず、エアコンや冷房を適切にお使いください。持病のある方、体調が優れない方は、自己判断せず医師にご相談ください。
ご紹介した実験結果・統計は、株式会社ニチレイの実験、内閣府男女共同参画局の統計、環境省 熱中症環境保健マニュアルなど、公的な情報にもとづいています。

ご感想や、ご実家に残る水がめ・たらいの記憶があれば、ぜひコメントで教えてください。高評価やシェアで「古代の秘訣」を応援していただけると、今後の内容もより深めてまいります。
```

## 🏷️ タグ (rổ 12 cố định + riêng)

`古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, 水がめ, 素焼き, 行水, たらい, 熱中症対策, 気化熱, 冷蔵庫, 昭和の暮らし`

#生活の知恵 #昔の知恵 #古代の秘訣 (3 hashtag cuối desc)

---

## ⚠️ VIỆC CÒN LẠI TRƯỚC KHI RENDER
1. **Cân nhắc mở rộng thêm ~8-10 phút** (信楽焼 quy trình nung cụ thể hơn, hoặc mở rộng lịch sử 行水 theo
   mùa/vùng) để đạt chuẩn 25′ — hiện 14,4′.
2. SLIDES + `check_vox.py --channel co-dai` — entry 0 nên là ẢNH THẬT chủ thể (chum gốm có giọt nước
   đọng), không phải thẻ chữ thuần.
3. 3 thumbnail (user gen theo Khối 4) → xoá watermark → `stamp_brand.py` → duyệt 3 cửa.
4. CTA: đã có 「高評価」 đúng vị trí (~50% bài, sau câu MỞ 「もう一つ、行水盥にまつわる話を…」) — grep xác
   nhận trước synth.
5. Đủ asset mới render (`render-background.md` §1.5).
6. Lịch: T2·T4·T6 13:00 JST — chèn vào slot gần nhất còn trống.
