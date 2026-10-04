# 14 — かぼちゃ：量ではなく、濃さで食べる（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI · **Chủ đề:** かぼちゃ × 砂糖・糖質 × 追熟
- **⭐ PHÉP THỬ SẠCH ĐẦU TIÊN của spec v3** (`CHANNEL_DIAGNOSIS_2026-08-11.md`). Đổi **đúng 1 biến = cấu trúc**; giọng · độ dài · khuôn title · khuôn thumbnail giữ nguyên.
- **Độ dài ĐO THẬT sau render: 23′17** (5.984 ký · 255 dòng · 1.397 giây) — trong dải 21–25′.
- **⛔ GATE:** L2–L5 · S6 · S7 sạch · 26 tag · 0 tag giữa câu. **L1: 95 giây, VƯỢT trần 90 — xem §0b.**

### 0b. 🔴 GATE TỪNG BÁO PASS OAN — đã vá, và vì sao KHÔNG render lại

Trước render, gate chấm **88 giây → PASS**. Bản render thật cho **94 giây**. Gate sai 7%.

**Nguyên nhân — mô hình thiếu một biến, không phải hằng số lệch:** bản cũ dùng MỘT hằng số `4,60 ký/giây`, nhưng mỗi **DÒNG** trong `_TTS.md` được chèn một khoảng nghỉ khi synth ⇒ bài càng nhiều dòng càng chậm, thời lượng **không tỉ lệ thuần với số ký tự**. Đo từ chính bản render: 5.984 ký / 255 dòng / 1.397 giây → **`4,49 ký/giây thuần + 0,25 giây/dòng`**. Mô hình mới ước cold open **95s** vs thực tế **94s** (lệch 1s; mô hình cũ lệch −6s).
✅ Đã vá `tools/check_coldopen.py`. ⚠️ Hằng số 4,60 cũ đo từ video 05 và vẫn "đúng" cho riêng video đó vì nó tình cờ có tỉ lệ ký/dòng khác — **đừng quay lại mô hình một-hằng-số.**

**Quyết định: KHÔNG render lại vì 5 giây.** Lý do là phép đo, không phải lười:
- Trần 90s chỉ là **proxy** cho "vào việc sớm". Thứ **đo được** gây chết là **cửa sổ giây 20–40** (`CHANNEL_DIAGNOSIS_2026-08-11.md` §1).
- Cửa sổ đó trong bản đã render: `25,0s` triệu chứng → `29,6s` triệu chứng → **`34,4s` mệnh lệnh 「切り口を見てください」** → `40,5s` vào reveal → `44,8s` trả payoff. **Không câu tháo ngòi, không meta, không credential, không mục lục.** Tức thứ proxy muốn bảo vệ thì đã đạt.
- `feedback_bot_render_lai`: chỉ render lại khi video **hỏng thật** (mất tiếng/lệch sub/exit≠0). 5 giây vượt một proxy đã thoả mãn ở tầng dưới **không phải hỏng**.
- 📌 Script SAU viết cold open theo mô hình mới ngay từ đầu (≈ **380 ký / 18 dòng** cho 90 giây).

### 0c. ✅ ĐÃ RENDER — nghiệm thu 2026-08-11

`06_VIDEO/14_kabocha-tabekata/14_kabocha-tabekata.mp4` · **246 MB · 23′17**

| tiêu chí (`render-background.md` §1.3) | kết quả |
|---|---|
| ① `EXITCODE=0` | ✅ |
| ② duration khớp `subs.srt` | ✅ mp4 1397,11s ↔ srt cuối `00:23:17,401` |
| ③ duyệt ≥4 frame bằng mắt | ✅ 8 frame, **có chủ đích chọn frame nền SÁNG** (siêu thị đèn huỳnh quang · ấm nước cạnh cửa sổ · bí bên cửa sổ · phòng khám rèm sáng) |

**Mốc cấu trúc đo từ `subs.srt` thật** — khớp hoặc tốt hơn thiết kế: `# ITEM1` 01:34 (6,8%) · persona 03:51 (16,6%) · **CTA giữa 11:31 = 49,5%** · **trả loop 18:21 = 78,9%** (spec đòi ≥75%) · **đóng nhân vật 19:21 = 83,1%**.

**Phụ đề:** `sub_style = outline` (chữ trần viền đen, **không nền**) + `sub_size 22`. Duyệt trên 4 frame nền sáng: **không mất chữ** — phần dưới khung của mọi ảnh đều là bàn/sàn tối nhờ style prompt (ánh sáng từ trái + DOF nông) nên viền đủ ăn. Badge rank 「第1位」 đúng góc trên-trái.

**Lớp hình:** 74 ảnh AI 1920×1080; watermark ✦ đã vá (lệch chuẩn hoá 2,36 → 0,86); gán slot đã sửa 2 cặp hoán đổi (11↔20 · 57↔58). Nguồn: `_ai_raw/` (gốc) → `_ai_clean/` (đã xử lý) → `slides_img_photo/slide_00..73.jpg`; bản đồ gán ở `_map.json`.
- **Bản đọc:** `14_kabocha-tabekata_TTS.md` = **BẢN CHUẨN**. Sửa lời → sửa cả file này + quét lại `match` trong SLIDES.

---

## 0. 🔴 VÒNG SỬA 1 → 2 — vì sao bản 1 bị bỏ hẳn

Bản 1 PASS mọi gate máy (cold open 85s, S6/S7 sạch, chất người 6/6, YMYL sạch) — **và vẫn chỉ đáng 6/10 về giữ chân.** Gate đo được cửa tử 20–40s, nhưng **không đo được bài có xương sống hay không**. Bốn lỗ:

| # | Lỗ của bản 1 | Đã sửa thành |
|---|---|---|
| 1 | 🔴 **Stake là もったいない, không phải 怖い.** "Bạn đang vứt đi dinh dưỡng" = lỗ tiền. Đây là **lỗi đã ghi sổ** ở video 11 (`03_CONTENT_PLAN.md` §11) và [[feedback_stake_tu_lap_khong_phai_loi_tien]]: stake của tệp senior là **mất tự lập**, không phải lãng phí | Stake mới = **数字が上がっているのに、理由が見つからない**. 「甘いものは食べていません」と言う人の食卓に、砂糖大さじ二杯が三日に一度、名前を変えて載っている。Nỗi sợ = **cái mình tin là lành thì không ai đi nghi nó** — và lối ra là 「疑うところさえ分かれば、直せます」 = tự chữa được = đúng trục tự lập |
| 2 | 🔴🔴 **Xương sống là GIẢ.** Bản 1 dán nhãn "một hàng: 色が濃いところほど中身が濃い" nhưng **2/5 mục không nằm trên hàng đó** — 油 là chuyện tan trong dầu, 蒸す là chuyện kali tan trong nước. **Ba chất, ba cơ chế, một cái nhãn.** Đây đúng là "nội dung rời rạc" | Xương sống THẬT, dựa trên **một tính chất vật lý duy nhất**: かぼちゃ **追熟** trong lúc bảo quản → tinh bột chuyển thành đường **và** sắc tố vàng tăng **cùng lúc**. Nên **色 = 甘さ = 栄養**. Từ đó: chọn quả đậm màu ⇒ đủ ngọt ⇒ **không cần thêm đường** ⇒ và dinh dưỡng cũng đậm. Bỏ hẳn mục 蒸す/カリウム (khác chất, phá xương). Chốt bài: **「量ではなく、濃さで食べる」** — cả 5 mục đều nằm trên đúng câu đó |
| 3 | 🔴 **Hook không có cảnh, không có người, không có hành động.** 「煮物のお皿に、かぼちゃを一切れ」 là một cái đĩa. So với video 12 mở bằng 「横断歩道を渡り切る前に、青が点滅しはじめる」 (cảnh người xem vừa sống tuần này) thì yếu hẳn | Mở bằng **động tác tay người xem vừa làm, kèm con số**: 「かぼちゃの煮物に、砂糖を大さじ二杯。みりんも、同じくらい。」 → lật ngay ở giây 12: 「その一皿は、野菜のおかずというより、甘いお菓子に近いかもしれません。」 |
| 4 | 🟡 **Hai nhân vật RỜI, không ai mất gì.** Bà vứt vỏ bị cháu nhắc; ông không biết chọn bí. Không hậu quả trên thân thể, không cung truyện | **MỘT nhân vật, ba nhịp, chạy xuyên bài** (28% gieo → 67% cao trào → 82% đóng). Và **cung truyện trùng khít xương sống**: bà giữ đúng vị món chồng thích mà bỏ được nửa lượng đường = 「量ではなく濃さ」 nói bằng cảm xúc |

📌 **Bài học rút ra (đáng ghi hơn cả script này):** gate máy S6/S7 chặn được **cửa tử 20–40 giây**, nhưng một bài **qua hết gate vẫn có thể là danh sách mẹo rời rạc**. Trước khi render, phải trả lời bằng chữ: *người xem ĐẾN vì gì · Ở LẠI vì gì · một hàng của bài là gì, và có đúng cho MỌI mục không*. Không trả lời được thì gate PASS cũng vô nghĩa.

---

## 1. Người xem ĐẾN vì gì · Ở LẠI vì gì

**ĐẾN:** thumbnail/title buộc tội **món họ tin là lành** (かぼちゃ = rau, tốt cho sức khoẻ) bằng một **động tác chính họ làm** (đổ hai thìa đường vào nồi). Không đòi mua gì mới.

**Ở LẠI — 5 cái móc, theo thứ tự người xem gặp:**
1. **Giây 33: họ đứng dậy nhìn quả bí nhà mình.** 「切り口を見てください。濃いオレンジに近い方。そのかぼちゃは、もう砂糖をほとんど必要としていません」 — tự chẩn đoán được ngay, không cần chờ hết bài.
2. **Một cái tên tội phạm bị giữ nguyên suốt bài.** Không có câu nào tháo ngòi (S6 = 0). Lời buộc tội 「甘いものは食べていない、とおっしゃる方の食卓に、それは、たしかに載っていません」 còn được **siết chặt thêm** ở 55%.
3. **Một hàng leo được, có số:** 追熟 → 色 → 甘さ → 砂糖いらない → 栄養も濃い. Mỗi mục sau nặng hơn mục trước, nên **không mục nào là "mục cuối đáng nghe"**.
4. **Ba cú làm-được-ngay:** nhìn 切り口 (0:33) · so わた với ruột (2:0x) · nhìn へた ở siêu thị (14:3x).
5. **Một người mà họ muốn biết kết cục.** スミ子さん bị treo ở 34% (「このお話の続きは、後半で」), vỡ ở 67%, đóng ở 82% — **nợ cảm xúc đáo hạn muộn hơn khúc dễ bỏ.**

---

## 2. Xương sống — và vì sao nó ĐÚNG chứ không phải nhãn dán

**Sự thật vật lý:** bí đỏ sau thu hoạch được **追熟** (ủ chín). Trong lúc đó tinh bột chuyển dần thành đường **và** lượng sắc tố vàng tăng lên. Hai việc xảy ra **cùng lúc, trên cùng một quả**.

⇒ **色 là chỉ dấu nhìn được của CẢ vị ngọt LẪN dinh dưỡng.** Từ đó suy ra được toàn bộ bài:

| mục | phục vụ xương sống thế nào |
|---|---|
| 第5位 わた を捨てない | わた đậm màu hơn ruột ⇒ **濃さ** tăng mà không tăng lượng. Hạt bí thì **không dính vị ngọt** ⇒ thêm được một món mà không thêm đường |
| 第4位 皮をむかない | vỏ nhiều chất xơ ⇒ làm chậm hấp thu đường ⇒ **bóc vỏ = ăn trần phần ngọt nhất** |
| 第3位 油をひとさじ | β-caroten tan trong dầu ⇒ **cùng một miếng, nhận được nhiều hơn** = 量ではなく濃さ |
| 第2位 砂糖・みりんを引く | quả đủ chín thì tự ngọt ⇒ **hai thìa đường là bù đắp cho việc chọn nhầm quả**, không phải nêm nếm |
| 第1位 色とへたで選ぶ | **chốt cả bốn mục trên bằng một hành động 5 giây ở siêu thị** — và trả loop |

🔴 **Cái đã CẮT khỏi bản 1: mục 蒸す/カリウム.** Nó đúng về mặt dinh dưỡng nhưng nói về **chất khác, cơ chế khác** (kali tan trong nước) → phá xương sống. Cắt một mục đúng để giữ bài liền mạch là đánh đổi có chủ ý. Kali cũng biến mất khỏi bài nên **cảnh báo 腎臓 không còn cần**; thay bằng cảnh báo đúng chủ đề: **糖尿病の治療中の方**.

---

## 3. Thiết kế nhịp (ước theo 4,60 ký/giây — đo lại từ `subs.srt` sau render)

| mốc | % | khối |
|---|---|---|
| 0:00–0:12 | 0% | **động tác + số**: 砂糖大さじ二杯・みりん二杯 → lật: 「野菜のおかずというより、甘いお菓子に近い」 |
| 0:12–0:33 | 1% | 3 câu triệu chứng (L5) — **đều buộc vào đúng stake**: 血糖の数字だけ上がる · 野菜は食べているのに · 昼のあと眠い |
| **0:33–0:50** | **2,7%** | 🔴 **CỬA TỬ** — mệnh lệnh 「切り口を見てください」 + reveal 「そのかぼちゃは、もう砂糖を必要としていません」 |
| 0:50–1:14 | 4% | cơ chế 追熟 (でんぷん→甘み, 色も同時に) → **câu chốt bài** 「量ではなく、濃さで食べる」 |
| 1:14–1:28 | 6% | **loop lớn**: 「砂糖を一切足さずに、あの甘い煮物を作る方法があります。買い方に、コツが一つ」 |
| 1:30 | 7% | `# ITEM1` → 第5位 わた・種 |
| 3:01 | 14% | persona みのり (40 giây) — SAU món #1 |
| 3:42 | 17% | 第4位 皮（食物繊維 → 糖の吸収） |
| **5:40** | **26%** | 🎭 **スミ子さん nhịp 1** — 三日に一度の煮物 · 亡くなったご主人 · 砂糖大さじ二杯は義母から · 健診で初めて印 · 「心当たりはありますか」に何も浮かばなかった → **treo: 「続きは、後半で」** |
| 7:03 | 33% | 第3位 油ひとさじ → 「一切れ増やすのではなく、一切れから多く受け取る」 |
| 8:2x | ~39% | **khối cơ chế + 原典** (β-カロテン→ビタミンA→粘膜 · ビタミンE · 文部科学省 成分表) + checkpoint 「に」 |
| **10:04** | **47%** | CTA giữa (câu canonical) |
| **10:37** | **50%** | 🔴 **第2位 = cú đấm giữa bài** — 150g ≈ ご飯茶碗半分の糖質 → 「もう半膳」 → 砂糖二杯 = 18g 乗る → 「甘いものは食べていない方の食卓に、それは載っていない。載っているのは、別のものです」 → lối ra: **2杯→1杯、ゼロにしない** |
| **13:2x** | **65%** | 🎭 **スミ子さん nhịp 2** — 娘が砂糖の袋を見つける → 「お父さんの好きな味を、やめたくなかったのよ」 |
| 13:5x | 67% | checkpoint 「さん」 |
| 14:05 | 68% | 第1位 色とへた |
| **15:48** | **77%** | **TRẢ LOOP** 「同じ売り場で、同じ値段で、五倍」 |
| **16:00** | **78%** | **đỉnh bài** `[間1.2][速0.8]濃い黄色を、選ぶ。[後間1.0]` |
| **16:40** | **82%** | 🎭 **スミ子さん nhịp 3 — đóng** 「これ、お父さんの味だわ」 → 「砂糖を半分にしても、味は残っていました。残っていなかったのは、埋め合わせのほうだけでした」 |
| 17:13 | 84% | recap 5 mục → in lại 「量ではなく、濃さで食べる」 → micro-commitment 「売り場での五秒」 |
| 18:3x | 90% | lớp cảm xúc: 「体にいいと信じているものほど、疑う機会がない」 → 「疑うところさえ分かれば、直せます」 → **「誰かに直してもらう前に、自分で直せる」** |
| 20:5x | 96% | disclaimer (+ 糖尿病治療中の方) → câu kết cố định |

✅ **Trả loop ở 77% và đỉnh ở 78%** — đúng luật skill MỤC 10 khối 6 (≥75%). Bản 1 trả ở 70,8%, đã sửa.

**Chất người 6/6:** ① tự trào 「私も長いあいだ、あそこは食べるところではない、と思っていました」 ② thoại + chi tiết đời sống vô dụng-về-thông-tin (**指ぬきだけは針箱に入れている** · 「あれを作っていると、台所に、誰かいる気がするのよ」) ③ ký ức giác quan (山吹色・香ばしい匂い・いつもの鍋) ④ người kể tự làm 「私も、蒸したかぼちゃに、すりごまをかけるようになりました」 ⑤ đóng nhân vật bằng cảm xúc, không bằng kết luận 「これ、お父さんの味だわ」 ⑥ phá nhịp 「水っぽいから。」「傷みやすいから。」「飲み込みにくい。」「最後に。」
**Giọng:** 26 tag · 0 tag giữa câu (verify máy) · đỉnh bài `[間1.2][速0.8][後間1.0]`.

⚠️ **Lệch spec có chủ ý:** MỤC 10 đòi **anecdote 1 + anecdote 2** (hai nhân vật). Bài này dùng **một nhân vật ba nhịp**. Lý do: user yêu cầu bài không rời rạc, và hai mẩu rời không tạo được nợ cảm xúc bắc qua đoạn 34%→82%. Vẫn giữ khung minh hoạ bắt buộc 「例えば、こんな方がいらっしゃるとします」 và luật nhân vật mới hoàn toàn mỗi video.

---

## 4. 原典 (genten) + YMYL

- **文部科学省「日本食品標準成分表」** — nêu ĐÍCH DANH trong lời đọc. Số dùng: 西洋かぼちゃ vs 日本かぼちゃ **カロテン ≈5 lần** · かぼちゃ ~150g ≈ **糖質 của nửa bát cơm** · **砂糖 大さじ2 ≈ 18g**.
- Hedge (không gắn tên tổ chức): 追熟 làm tăng ngọt + màu · β-caroten → vitamin A theo nhu cầu · vai trò 粘膜 · chất xơ làm chậm hấp thu đường · vitamin E thuộc nhóm cao nhất trong rau · nhai giữ sức nuốt.
- **Cảnh báo điều kiện tại chỗ:** 「血糖の治療を受けていらっしゃる方は、量を変える前に、必ず先生にご確認ください」 (thay cảnh báo 腎臓×カリウム của bản 1 — mục kali đã bị cắt).
- ⛔ Không 治る/完治/薬の代わり/絶対. Nhân vật **không hứa số liệu**: 「検査の数字が変わったかどうかは、分かりません」.
- ⚖️ **Lối ra không cực đoan:** cố ý **KHÔNG** bảo bỏ hẳn đường (「一度に、ゼロにしないでください。長年の味を、いきなり変えると、家族が箸を止めます」) — vừa đúng thực tế bếp, vừa tránh giọng ra lệnh.

## 5. Nhân vật (mới hoàn toàn, không lặp video khác)

| | tuổi | tỉnh | nghề cũ | chi tiết đời sống | vai |
|---|---|---|---|---|---|
| 片桐スミ子 | 76 | 山形県 | 和裁の仕立て | **指ぬきだけは、今も針箱に** | 3 nhịp: gieo 26% · cao trào 65% · đóng 82% |

## 6. Title — 3 bản A/B

Keyword dẫn = **tên vật + 食べ方** (`かぼちゃ 食べ方` med **136** v/ngày, cao nhất trong rổ giải thích sức khoẻ senior — đo 2026-08-11, bảng đầy đủ ở §7).

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代は要注意】かぼちゃの正しい食べ方5選｜その煮物、もう半膳かも` | 36 | かぼちゃ@9 | keyword volume cao nhất + hook = cú lật của bài |
| **A2** | `かぼちゃは色で選べば砂糖がいらない｜60代の正しい食べ方5選` | 32 | かぼちゃ@0 | đổi keyword dẫn — đưa đáp án #1 (色) lên đầu, bỏ 【】 |
| **A3** | `【知らないと損】かぼちゃに砂糖は要らない｜60代の正しい食べ方5選` | 35 | かぼちゃ@8 | đổi kiểu hook: cảnh báo → tuyên bố nghịch lý |

#### Title CHỐT
```
【60代は要注意】かぼちゃの正しい食べ方5選｜その煮物、もう半膳かも
```

#### Tên file upload
```
kabocha-tabekata-60dai.mp4
```

### 概要欄 — 3 DÒNG ĐẦU

> Vùng hiển thị trước nút もっと見る. Nói **về gì / cho ai / được gì**, keyword `かぼちゃ` xuất hiện tự nhiên. ⛔ Không lời chào.

```
かぼちゃの煮物に、砂糖を大さじ2杯。その一皿は、野菜のおかずというより、ご飯茶碗の半分ほどの糖質が入った「もう半膳」に近い一皿かもしれません。
この動画では、60代からの食卓で見直したい、かぼちゃの正しい食べ方を5つ。捨てているわた、むいている皮、足りていない油、そして砂糖を減らしても味が落ちない買い方まで、順にお話しします。
熟したかぼちゃは、もともと甘い。売り場での5秒で、大さじ2杯の砂糖が要らなくなります。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ

> 目次 **trích từ `subs.srt` của bản đã render** (`_chapters.txt`) — không phải số ước tính.

```
かぼちゃの煮物に、砂糖を大さじ2杯。その一皿は、野菜のおかずというより、ご飯茶碗の半分ほどの糖質が入った「もう半膳」に近い一皿かもしれません。
この動画では、60代からの食卓で見直したい、かぼちゃの正しい食べ方を5つ。捨てているわた、むいている皮、足りていない油、そして砂糖を減らしても味が落ちない買い方まで、順にお話しします。
熟したかぼちゃは、もともと甘い。売り場での5秒で、大さじ2杯の砂糖が要らなくなります。

【目次】
00:00 オープニング｜その煮物、野菜のおかずですか
01:37 第5位 わたを捨てない（種も）
04:38 第4位 皮をむかない
06:44 甘いものは食べていないのに｜ある方のお話
08:18 第3位 油をひとさじ
10:01 なぜ色の成分が大事なのか（出典つき）
12:09 第2位 砂糖とみりんを引く｜ご飯茶碗半分の糖質
15:48 第1位 切り口の色とへたで選ぶ
19:54 まとめ｜量ではなく、濃さで食べる

かぼちゃは野菜の顔をしていますが、文部科学省「日本食品標準成分表」で見ると、いも類に近い食べ物です。大きめに三切れ、およそ150グラムで、ご飯茶碗の半分ほどの糖質が入ってきます。そこへ砂糖を大さじ2杯、およそ18グラム。かぼちゃ自身の糖質に、その半分以上が上から乗ってくる計算になります。甘いものは食べていない、とおっしゃる方の食卓に、それはたしかに載っていません。載っているのは、野菜の煮物という名前をした、別のものです。

けれども、砂糖を抜いたら味気なくなるのかというと、そうではありません。かぼちゃは収穫してから置いておくあいだに、でんぷんが甘みに変わっていきます。同時に、あのオレンジ色のもとであるベータカロテンも増えていきます。つまり、色が濃いものほど、甘くて、中身も濃い。砂糖の大さじ2杯は、味つけではなく、甘くないかぼちゃを選んでしまったことへの埋め合わせだったのかもしれません。

動画では、捨てられがちなわたのほうが実より色が濃いこと、皮に多い食物繊維が糖の吸収をゆるやかにするとされていること、ベータカロテンが油に溶ける種類の栄養で小さじ一杯の油があるだけで受け取れる量が変わることを、順にお話しします。そして第1位は、売り場での選び方。切り口の濃いオレンジ色と、乾いてひび割れたへた。この二つを5秒見比べるだけで、砂糖の量も、受け取れる栄養も、いっぺんに変わります。西洋かぼちゃと日本かぼちゃでは、成分表の数字で色の成分がおよそ5倍ちがいます。

血糖の治療を受けていらっしゃる方は、食べる量を変える前に、必ずかかりつけの先生にご確認ください。

※この動画でお伝えする内容は、公表されている公的資料をもとにした、健康に関する一般的な情報です。個別の医療アドバイスではありません。持病のある方やお薬を飲んでいる方は、食事を変える前に必ずかかりつけの医師にご相談ください。

【出典】
文部科学省「日本食品標準成分表」

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニア健康 #健康長寿 #かぼちゃ #かぼちゃの食べ方
```

### タグ

> 16 tag nhận diện kênh **cố định đứng đầu** (giống 13 video trước) → 26 tag riêng video. Tổng **42**.
> ⛔ **Cố ý KHÔNG có `血糖値`** dù bài có nhắc: `CLAUDE.md` đo được `chỉ số × ◯選` là **luồng đã chết** (median 7 v/ngày), và tag quyết định YouTube xếp video vào RỔ nào để test (bài học 2026-07-21: video 腎臓 đặt cạnh rổ アルデヒド → người xem bỏ sau **10 giây**). Giữ rổ khoá ở かぼちゃ / 食べ方 / シニア健康.

```
60代からの食卓, 60代 食事, 60代 食べてはいけない, 食べてはいけない, シニア 健康, シニアライフ, シニア 食事, 高齢者 食事, 高齢者 栄養, 健康長寿, 健康寿命, 食生活 改善, 生活習慣病 予防, 60代 健康, 70代 健康, 老後 健康, かぼちゃ, かぼちゃ 食べ方, かぼちゃ 煮物, かぼちゃ 栄養, かぼちゃ 選び方, かぼちゃ わた, かぼちゃ 皮, かぼちゃ 種, 西洋かぼちゃ, 日本かぼちゃ, ベータカロテン, ビタミンA, ビタミンE, 脂溶性ビタミン, 追熟, 野菜 糖質, 糖質 多い 野菜, 砂糖 減らす, 砂糖 控える, 煮物 砂糖, みりん 使い方, だし うまみ, 食物繊維 糖の吸収, 冷凍かぼちゃ, 食品成分表, かぼちゃ 保存
```

⚠️ **Compliance title/thumbnail:** chữ **血糖 được phép ở TITLE và 概要欄/tag nhưng CẤM lên THUMBNAIL** (chữ 血 → auto-review dễ đọc thành gore, `youtube-compliance.md` + SKILL MỤC 15). Chữ thumbnail dùng **砂糖・大さじ2・もう半膳** thay cho 血糖.

## 7. Đo cầu keyword (2026-08-11, `tools/measure_kw_youtube.py`, 30 ngày, JP/ja, ≥8′)

| keyword | n | med v/ngày | rổ |
|---|---|---|---|
| **かぼちゃ 食べ方** | 18 | **136** | ✅ đúng rổ (健康の道しるべ · 健康の習慣 · 健康な老後の生き方) |
| シナモン 食べ方 | 16 | 49 | ✅ đúng rổ |
| 酢 食べ方 | 12 | 40 | ✅ đúng rổ |
| 生姜 食べ方 | 11 | 24 | hỗn hợp |
| 大根 食べ方 | 6 | 16 | đúng rổ, cầu thấp |
| ~~オクラ 食べ方~~ | 7 | 8.783 | ⛔ **rổ CÔNG THỨC NẤU ĂN** (毎日中華 · シクロエの家) — cầu to nhưng sai rổ, đúng bệnh đã đo 07-21 |
| ~~玉ねぎ 食べ方~~ | 10 | 637 | ⛔ cũng rổ công thức (リュウジ · ゆかり) |
| ~~かぼちゃ 食べ合わせ~~ | 14 | **15** | ⛔ góc 食べ合わせ bão hoà |

🔴 **Bảng "cột trống" đo 08-03 đã hết hạn sau 8 ngày** (酢 n=4→12 · かぼちゃ n=3→18 · シナモン n=3→16). **Phải đo lại trước mỗi lần chọn món**, đừng bê số cũ.

⚠️ **Đổi KHUÔN:** video 11+12 dùng 「避けたい3つ＋続けたい3つ」, 13 dùng khuôn hành trình → 14 dùng **countdown 第5位→第1位** (khuôn của ゆで卵, video AVD cao nhất kênh 27,4%). Ba video liền kề không cùng dáng.

## 8. LỚP HÌNH — 74 slide, **100% ảnh AI do user gen** (chốt 2026-08-11)

`04_SCRIPTS/14_kabocha-tabekata_SLIDES_photo.json` — **74 entry, `photo: true`, `q: "AI-GEN"`**.
⛔ **KHÔNG chạy `fetch_photos.py` cho video này** — `q` là nhãn đánh dấu, không phải query. Ảnh do user gen rồi đặt tay.

| | |
|---|---|
| Nhịp | **17,6 giây/ảnh · 3,41 lần đổi hình/phút** — trong luật `audience-45plus.md` §2 (≤6/phút) · **0 entry <6 giây** |
| `rank` | 第5位 8 · 第4位 6 · 第3位 5 · 第2位 9 · 第1位 9 · 37 entry ngoài mục (cold open · persona · スミ子 · cơ chế · kết) |
| Verify máy | 74/74 `match` là substring có thật trong `_TTS.md` · 0 trùng · đúng thứ tự |
| ⭐ Entry 0 | 「かぼちゃの煮物に、砂糖を大さじ二杯」 → thìa đường đổ vào nồi bí — **chủ thể của bài ngay giây 0** (`media-library.md` §2.0) |

**File prompt** (`06_VIDEO/14_kabocha-tabekata/`, theo [[feedback_luu_prompt_vao_file]]):

| file | vai |
|---|---|
| `slide_prompts_FLOW.txt` | **74 prompt, mỗi prompt 1 DÒNG** — bơm thẳng vào extension |
| `slide_prompts_TENFILE.txt` | `slide_XX.jpg` ↔ mốc giây ↔ rank ↔ câu cue |
| `slide_prompts_BLOCKS.md` | bản người đọc: khối STYLE + mô tả từng slot |

**Đồng nhất 74 ảnh** (đúng cái user muốn): mọi prompt kết bằng **cùng một khối STYLE nguyên văn** (`photorealistic documentary photography, Japanese home kitchen, warm natural window light from the left … deep navy and warm amber accents`) — khớp bảng màu nhận diện kênh. Nhân vật スミ子 dùng **cùng một câu tả ở cả 4 slot** (portrait · phòng chờ · ngồi im · nếm thử) để nhận ra là một người.

**Đặt tên khi gen xong:** `slide_00.jpg` … `slide_73.jpg`, bỏ vào `06_VIDEO/14_kabocha-tabekata/slides_img_photo/` (renderer đọc theo **index 0-based đúng thứ tự entry** — sai thứ tự là sai hình cả bài).

### ⚠️ Ba việc bắt buộc khi dùng ảnh AI

1. 🔴 **PHẢI TICK "altered/synthetic content" khi upload** (`youtube-compliance.md` §2.1, đảo chiều 2026-08-09: được dùng ảnh AI, đổi lại phải khai báo). **`upload_pack.py`/`upload_api.py` CHƯA có cờ này → tick TAY trong Studio.** Đánh đổi đã biết: video hiện nhãn "Altered or synthetic content", ở ngách YMYL sức khoẻ nhãn này ăn vào độ tin.
2. 🔴 **Quét sạch watermark** trước khi dùng ([[feedback_anh_ai_quet_sach_watermark]]) — dấu ✦ **không cố định một chỗ**, phải đo lại vị trí theo đúng lô ảnh rồi crop/vá, đừng `cv2.inpaint`.
3. 🔴 **Mọi prompt đã ghi `No text, no letters, no numbers`** — chữ Nhật gen ra hay nát nét (`media-library.md` §2.9). Ảnh nào lỡ có chữ → **loại, gen lại**, đừng để tạm. Ba slot cố ý tả "chữ mờ không đọc được" (giấy khám bệnh · sổ tay · sách thành phần) để không phải gen kanji.

## 8b. Việc còn lại trước render

1. Gen 74 ảnh → đặt tên đúng → **duyệt contact sheet bằng mắt** (`media-library.md` §2.1): soi bộ ĐƯỢC CHỌN, không phải bộ mới tải.
2. **Đủ ảnh mới được render** (`render-background.md` §1.5) — thiếu 1 ảnh cũng không render.
3. Render chạy NỀN, `--channel shokutaku`, `--slides 04_SCRIPTS\14_kabocha-tabekata_SLIDES_photo.json`.
4. **目次** trích timestamp **từ `subs.srt` sau render** — ⛔ không bịa.
5. **概要欄 + タグ + bộ A/B 3×3 thumbnail:** ⏸ cố ý CHƯA làm — phạm vi lượt này là retention (kế hoạch §5).

## 9. Đọc kết quả (sau ≥7 ngày)

```bash
cd E:\Claude\Projects\youtube-jp-chouhen\tools
python analytics_report.py --channel shokutaku --video <videoId>
```

Nhìn **@40s** (mục tiêu ≥85%, nay 30–50%) và **sàn thân bài** (≥55%, nay 9–21%). ⛔ Không đọc bằng view (`BROWSE = 0`). Mốc chặng AVD% **30 → 40 → 50 → 60**; phanh ở 3 video liên tiếp ≤25%.

🔬 **Phép thử riêng của bài này:** nếu curve **giữ được qua mốc 26% và 65%** (hai nhịp スミ子さん) thì cung truyện xuyên bài là thứ đáng nhân rộng; nếu rớt đúng ở đó thì nhân vật đang là chỗ trũng, quay về mẫu 2 anecdote ngắn.
