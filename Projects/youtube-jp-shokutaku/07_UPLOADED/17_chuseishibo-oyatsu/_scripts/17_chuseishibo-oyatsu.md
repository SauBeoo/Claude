# 17 — 中性脂肪：一日は二十四時間、片づけは四十時間（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **中性脂肪 × 食後高脂血 × 食事の「回数」 × 動脈硬化**
- **Bản đọc chuẩn:** `17_chuseishibo-oyatsu_TTS.md` — **bản 2** · **5.892 ký (thuần) · 265 dòng · ước 23′24** — sửa lời thì sửa file này **và** quét lại `match` trong SLIDES.
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 17` → ✅ **PASS, cold open 89 giây** (L1–L5 · S6 · S7 sạch) · **46 tag** · 0 tag giữa câu · 0 tag đứng dòng riêng · blacklist 0 · YMYL cấm 0 · 8 loại whitelist · S8 19 cảnh báo.
- **Phép thử sạch thứ TƯ của spec v3.** Khác video 16 ở **KHUÔN** (16 = 犯人さがし → 17 = **算数: 四十時間 ÷ 二十四時間**) và **TRỤC** (16 = カリウム・むくみ → 17 = **脂質・食後・血管の内側**).

---

## 0. 🔴 VÒNG SỬA — bản 1 bị BỎ, sáu lỗi đều là lỗi CẤU TRÚC

> user: *"đánh giá kịch bản này giữ chân người xem và không rớt lúc đầu không?… người xem đến vì cái gì, ở lại vì cái gì?… kịch bản phải có hồn, hook phải ấn tượng, nội dung không được rời rạc"*

Bản 1 **PASS mọi gate máy** (cold open 90s · S6/S7 sạch · YMYL 0) và tự chấm chỉ **6,5/10**. Sáu lỗ, không lỗ nào sửa được bằng chữa câu chữ:

### 0a. 🔴 HOOK là MÔ TẢ, và cú xoắn của nó là một KHÁI NIỆM

Bản 1 mở: 「健康診断の紙で、中性脂肪のところだけ、毎年、印がついている」 — nói với người xem đúng **cái họ đã biết về chính mình**. Câu xoắn là 「理由は、食べたものではなく、食べた"あと"にあります」 — mà 「食べたあと」 là **khái niệm**, đúng thứ `CHANNEL_DIAGNOSIS_2026-08-11` §2.1 đo được là **không cứu nổi** cửa tử (納豆 thay bằng 「組み合わせ」, ブルーベリー thay bằng 「食べ方」 — cả hai vẫn rớt 50–55 điểm).

**Bản 2** mở bằng một cảnh có **giờ cụ thể**, và câu thứ tư là cú xoắn:

```
ゆうべ、夜の十時に、天ぷらを召し上がったとします。
その脂が、体から引くのは、いつだと思われますか。
今朝の、八時ごろです。
つまり、今朝の朝ごはんのとき。体はまだ、ゆうべの片づけを、していました。
```

⇒ Người nghe tự đối chiếu được bữa tối hôm qua của chính mình. Không một chữ trừu tượng.

### 0b. 🔴 CON SỐ HERO CHƯA THÀNH CÚ SỐC — 「十時間」 mới chỉ là một fact

Bản 1 dừng ở 「一回の食事につき十時間」. Hay, nhưng không đâm.
**Bản 2 làm phép nhân ngay trước mặt người xem**: 朝・昼・夕・三時のおやつ = **十時間 × 4 = 四十時間ぶん**, mà **一日は二十四時間**.

```
けれども、一日は、二十四時間しかありません。
入りきりません。
だから、片づけは、必ず重なります。
```

⇒ Cả bài thành **MỘT bài toán**, và loop lớn chính là câu hỏi của bài toán: 「四十時間を、二十四時間に、どう収めるのか」. Loop bản 1 (「một chỗ, thêm hai tiếng」) là loop **thủ tục**; loop bản 2 là loop **có đáp số**.

### 0c. 🔴 BỐN ẨN DỤ CHỒNG NHAU, và cái thứ tư LẶP lại cái thứ nhất

Bản 1: 流しの洗い物 (ITEM1) → 絹のような膜 → 濁った川 → 揚げ物のあとのぬめり. **Bốn** hình ảnh cho **một** ý, cái thứ tư quay về đúng cái bếp của cái thứ nhất. Khối 5:57–7:00 của bản 1 là **giảng bài**, không đẩy câu chuyện.

**Bản 2 giữ ĐÚNG MỘT ẩn dụ và cho nó lớn lên**: cái bếp không kịp rửa → 「油が、壁や、換気扇に、うっすらと染みていきます。一日では、何も起こりません。けれども、十年、二十年と続くと、指でこすっても取れなくなる」 → rồi mới nối sang mạch máu. Bỏ hẳn 絹の膜 và 濁った川.

### 0d. 🔴 PAYOFF chỉ giải MỘT trong ba cái 「つい」

Bản 1 chốt bằng 「おやつを食事のすぐあとにくっつける」 — chỉ chữa ①. ② và ③ phải chữa bằng hai lời dặn rời → **rời rạc đúng chỗ đắt nhất**, và người xem phải nhớ ba việc.

**Bản 2 chốt bằng MỘT quy tắc giải cả ba** — và nó mang chính tên kênh:

> **「口に入れるのは、食卓に器が出ている、そのあいだだけ」**

①おやつ → ăn khi bát đĩa bữa trưa còn trên bàn · ②寝る前 → ăn trước khi dọn mâm tối · ③朝食抜き → ngày không dọn mâm ra là ngày làm đỉnh sau cao hơn. **Không cần đồng hồ, không phải nhớ ba việc.** Và bài tự kết sổ: 片づけ 4 lần → 3 lần, tức **四十時間ぶん → 三十時間ぶん**.

### 0e. 🟡 「つい③ 朝食抜き」 đi NGƯỢC mạch mà không được đóng khung

Bài dạy 「khoảng nghỉ càng dài càng tốt」 rồi lại bảo nhịn sáng là sai → người xem thấy mâu thuẫn, bản 1 giải thích lướt qua.
**Bản 2 biến mâu thuẫn thành micro-hook**, nói hộ người xem: 「ここで、一つ、ひっかかった方がいらっしゃるはずです。休みは、長いほどいい。それなら、朝ごはんを抜けば…」 → 「ええ、そのとおりです」 → 「けれども、ここに、落とし穴があります」.

### 0f. 🟡 Không có chỗ nào GỠ LO trước lúc chốt

Tệp 60–80 nghe 15 phút về "ăn sai giờ" sẽ **thủ thế**: lại sắp bị cấm thêm một món. Bản 2 thêm một nhịp ngay trước payoff: 「食べるものを、また一つ、取り上げられるのだろうか。そう身構えながら、ここまで来てくださった方も、いらっしゃるはずです。取り上げるものは、一つもありません。」

---

## 1. NGƯỜI XEM ĐẾN VÌ GÌ · Ở LẠI VÌ GÌ (hai câu trả lời phải khác nhau)

| | |
|---|---|
| **ĐẾN vì** | Thumbnail nói `中性脂肪 / 40時間 / 3時のおやつ`. Người đi khám hằng năm nhận ra tờ giấy của mình trong nửa giây, và **`40時間` là con số không thể đoán ra** — phải bấm vào mới biết 40 tiếng là 40 tiếng gì |
| **Ở LẠI vì** | ⭐ **Một bài toán đang mở**: 四十時間ぶんの仕事 nhét vào 二十四時間. Bài trả từng lớp — 十時間 (1:28) → vì sao chồng lấn thì hại (5:57) → ba chỗ tự chồng thêm (9:13 → 12:00) → **vì sao không ai nhìn ra** (13:0x) → đáp số (16:51). Năm lần trả, không lần nào trả hết |
| **Ở LẠI vì (2)** | **Tự kiểm chứng được trên chính mình**: bữa tối hôm qua mấy giờ (câu 1) · tờ kết quả khám có ghi giờ lấy máu (7:05) · phép trừ hai mốc giờ trong năm giây (15:3x). Ba lần biến thứ họ đã sống chung thành **bằng chứng đọc được** |
| **BỎ ĐI nếu** | được cầm giải pháp quá sớm — ITEM1 ở đây **chỉ đưa phép tính, không đưa lời khuyên nào**, nó kết bằng câu hỏi 「では、どうやって収めるのか」 · nghe danh sách món thay vì một mạch · bị bảo phải nhịn ăn (bản 2 nói thẳng 「取り上げるものは、一つもありません」) |

---

## 2. XƯƠNG SỐNG — một hàng, mọi khối treo vào nó

> **一日は二十四時間。片づけは四十時間ぶん。だから、減らすのは量ではなく、回数。**

| khối | vai trong BÀI TOÁN | quy về hàng |
|---|---|---|
| Hook | ゆうべ十時の天ぷら → 今朝八時。朝ごはんのとき、体はまだ片づけ中 | đặt đề bài |
| ITEM1 **四十時間** | 十時間 × 4回 = 40 ⇒ 24 に入りきらない ⇒ **必ず重なる** | con số gốc |
| フサ子さん nhịp 1 | 三時のおやつが全部「正しい」のに印が消えない | vật chứng chưa giải |
| ẩn dụ DUY NHẤT lớn lên | 洗い残し → 壁と換気扇に油が染みる → 十年で取れなくなる | vì sao chồng lấn thì hại |
| 原典 | ガイドライン2022 thêm **随時 175** + 「健診の紙に採血時刻が書いてある」 | bằng chứng + việc tự làm |
| 三つの「つい」 | ①三時のおやつ ②寝る前 ③朝食抜き | ba chỗ tự cộng thêm một lần |
| なぜ見つからないか | cả ba đều là **hành vi được khen** | gỡ tội cho người xem |
| cú lật + gỡ lo | 「置いた、場所でした」 + 「取り上げるものは、一つもありません」 | — |
| 五秒で測る | phép trừ hai mốc giờ trên lịch ăn của chính mình | công cụ |
| **TRẢ LOOP** | **「口に入れるのは、食卓に器が出ている、そのあいだだけ」** → 4回 → 3回 → 四十 → 三十 | đáp số |

---

## 3. MỐC THỜI GIAN (ước theo CPS 4,40 — thay bằng số thật từ `subs.srt` sau render)

| mốc | thời điểm | % | luật đòi |
|---|---|---|---|
| **cú xoắn hook** | ~0:13 「今朝の、八時ごろです」 | — | câu xoắn = xương sống ✅ |
| **cửa tử 20–40s** | 「ある朝、湯呑みを持った手が、いうことを聞かなくなる」→「畳の上に、お茶がこぼれる音」→「お箸は、左手で持つ練習です」 | — | 🔴 tổn thương THÂN THỂ, **dựng cảnh chứ không tuyên bố** ✅ |
| `# ITEM1` (四十時間) | **1:28** | **6,3%** | ≤4:00 ✅ |
| persona みのり + CTA | 3:40 | 15,7% | SAU món #1 ✅ |
| フサ子さん nhịp 1 | 4:32 | 19,4% | ~1/3 ✅ |
| ẩn dụ lớn lên (壁の油) | 5:57 | 25,4% | — |
| 原典 + 採血時刻 | 7:05 | 30,3% | — |
| checkpoint 「に」 | 8:46 | 37,5% | tách khỏi CTA ✅ |
| つい① 三時のおやつ | 9:13 | 39,4% | — |
| つい② 寝る前のひと口 | 10:29 | 44,8% | — |
| **CTA giữa (canonical)** | **11:27** | **48,9%** | ~50% ✅ |
| つい③ 朝食抜き (micro-hook mâu thuẫn) | 12:00 | 51,3% | — |
| ⭐ CÚ LẬT + gỡ lo | 14:27 | 61,8% | — |
| checkpoint 「さん」 | 15:25 | 65,9% | ngay trước loop ✅ |
| 五秒で測る | ~15:3x | ~67% | — |
| **TRẢ LOOP = 器のルール** + đỉnh bài `[間0.6][速0.8][後間1.0]` | **16:51** | **72,1%** | ≥75% 🟡 thiếu 2,9 |
| YMYL 糖尿病の薬 điều kiện | 18:52 | 80,7% | trước mọi lời khuyên áp dụng ✅ |
| フサ子さん nhịp 2 | 19:20 | 82,7% | ~2/3+ ✅ |
| disclaimer | 22:24 | 95,8% | cuối ✅ |
| **TỔNG** | **23:24** | | 21–25′ ✅ |

🟡 **Hai chỗ chưa hoàn hảo, ghi thẳng:**
1. **TRẢ LOOP 72,1%** thay vì ≥75% (v16: 73,8% · v15: 74,7%). Đã kéo từ 66,7% (bản 1) lên bằng **bồi/dời nội dung thật, không kéo đuôi**: thêm khối 「なぜ何十年も見つからなかったか」 · nhịp フサ子 thứ hai · khối gỡ lo · **dời 「五秒で測る」 lên TRƯỚC điểm trả** (đo trước, nhận lời giải sau — đúng hơn về kịch bản). Muốn chạm 75% phải cắt ~1′20 trong chính phần triển khai payoff, tức phá payoff để cứu một con số proxy. Không đổi.
2. **S8 = 19 cảnh báo.** Soi mắt: run dài nhất nằm ở khối phép tính 四十時間 (0′11) và khối つい③ — tức **cơ chế và cú lật**, không phải trang trí. Đã chèn đồng tiền THẬT (`四時間あけて出すのと二時間で出すのと` · `十七時間` · `六十時間ぶん` · `採血の時刻`). Tool tự ghi 「S8 đo ĐỘ MỊN CAPTION, không đo chất kịch bản」.

---

## 4. ⚠️ HAI CHỖ PHẢI XỬ LÝ BÊN TRONG BÀI

**(a) Nhịn ăn — YMYL.** Bài nói 「nghỉ càng dài càng tốt」, cách 断食 đúng một bước — **nguy hiểm với tệp 60–80 và với người dùng thuốc tiểu đường**. Bốn lớp chặn:
- つい③ **khuyên ĂN sáng**, gọi thẳng bỏ bữa là một trong ba cái sai, kèm cơ chế (山が高くなる + 余分な一回を買う);
- payoff là **「やめません・減らしません・買い足しません」**;
- khối gỡ lo 「取り上げるものは、一つもありません」;
- **18:52**, trước mọi lời khuyên áp dụng: 「糖尿病のお薬や、注射をお使いの方は、食事の間隔をあけることが、かえって危ないことがあります…必ず、かかりつけの先生に、ご相談ください」.

**(b) Củng cố video 11 (ヨーグルト).** Video 11 khuyên ăn sữa chua **sau bữa**; quy tắc 器 của video 17 là bản tổng quát của đúng lời khuyên đó → hai video **nối được thành một nguyên tắc lớn hơn**, không mâu thuẫn.

---

## 5. NGUỒN THẬT (原典) — không bịa, giữ nguyên tên + 年版

| dùng ở | nguồn | số trích |
|---|---|---|
| 7:05 | **日本動脈硬化学会「動脈硬化性疾患予防ガイドライン2022年版」** | Bản 2022 lần đầu đặt chuẩn cho 中性脂肪 đo **KHÔNG lúc đói (随時)**: **175 mg/dL 以上** (lúc đói vẫn 150) |
| 7:05 | cùng nguồn | Lý do thêm: số đo **sau ăn** gắn với bệnh tim mạch chặt hơn số đo lúc đói → bài nói 「そう報告されてきたからだ、とされています」, **không** gắn tên nghiên cứu |
| 1:28 / 5:57 | — | 食後 中性脂肪: đỉnh **3–4 tiếng**, về mức cũ mất **~10 tiếng** → 「とされています」, **không gắn tên tổ chức** |

⚖️ **Chỗ cố ý KHÔNG gắn tên tổ chức:**
- 「十時間」「三時間か四時間」 → hedge 「とされています」 (con số lâm sàng phổ biến, không thuộc văn bản nhà nước có 年版).
- **Phép tính 四十時間 là phép NHÂN công khai trước mặt người xem** (10 × 4), không phải số trích từ nghiên cứu — và bài nói rõ hệ quả là **「重なる」**, không nói cơ thể "nợ 40 tiếng".
- 「空っぽの時間が長すぎたあとの食事では、山が高く立ち上がりやすい」 → 「考えられています」.
- **フサ子さん KHÔNG có con số kết quả** — chỉ có 「かわりに、庭に出るようになったの」 + 「数字がどうなったかは、私には分かりません」.
- Quét máy: 治る/治す/完治/薬の代わり/絶対 = **0 hit** · blacklist Mục 7 = **0 hit**.

---

## 6. CHẤT NGƯỜI (`humanize-script-voice.md`) — 6/6 mũi tiêm

| # | mũi | chỗ trong bài |
|---|---|---|
| ① | người kể xuất hiện bằng cảm nghĩ (KHÔNG credential) | 「三時のおやつは、日本の家では、行儀のいい習慣です…**私も、この時間そのものは、なくしてほしくないと思っています**」 — bản 1 thiếu hẳn mũi này |
| ② | nhân vật có THOẠI + chi tiết đời sống vô dụng | フサ子さん: 「先生には、様子を見ましょう、と言われるだけなのよ」 + **煮干しは娘さんが送ってくださるもの** + 「笑って、湯呑みを置いて、それから、また、三時にみかんをむく」 |
| ③ | ký ức giác quan đúng tệp | 泡だらけの手 · 玄関のチャイム · 換気扇に染みた油 · 指でこすっても取れない · 畳にこぼれるお茶 · くつ下のあと |
| ④ | người kể tự làm thứ mình khuyên | 「この三つを外したら、続きませんから」 + mũi ① |
| ⑤ | đóng nhân vật bằng CẢM XÚC | 「かわりに、庭に出るようになったの」 + 「夕方に、くつ下のあとを見るのが、少しだけ、こわくなくなった」 |
| ⑥ | phá nhịp câu ≥3 lần | 「十時間です。」「入りきりません。」「それだけです。」「みかん。／無糖のヨーグルト。」「置いた、場所でした。」「ええ、そのとおりです。」 |

**Lớp nhấn nhá:** 46 tag, 1 giọng 1 style nền `[しっとり][速0.8]`. Đỉnh bài `[間0.6][速0.8][後間1.0]` **dính liền câu** ở 16:51 — đúng câu quy tắc 器.

---

## 7. 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代70代】中性脂肪が下がらない人の「つい」3つ｜変えるのは一か所だけ` | 38 | 中性脂肪@9 | keyword đo được cao nhất rổ (med **2.111**) dẫn đầu, nằm trong 25 ký đầu |
| **A2** | `【60代70代】動脈硬化を静かに進める食卓の習慣3つ｜今日変えるのは一か所` | 37 | 動脈硬化@9 | đổi keyword dẫn sang stake nặng hơn (med 1.118, max 13.177 = video 198K của rổ) |
| **A3** | `一日は24時間、体の片づけは40時間｜60代の中性脂肪が下がらない本当の理由` | 37 | 24時間@4 · 中性脂肪@22 | đổi kiểu hook: P0 cảnh báo → **P4 đảo nhận thức**, dẫn thẳng bằng nghịch lý số học của bài |

### Title CHỐT

```
【60代70代】中性脂肪が下がらない人の「つい」3つ｜変えるのは一か所だけ
```

### Tên file upload

```
chuseishibo-sagaranai-tsui-3tsu-60dai.mp4
```

---

## 8. TEXT THUMBNAIL (v5 WARNING-FIRST) — dùng CHUNG cho cả T1/T2/T3

> 🔴 `ab-3title-3thumb.md` §3 mục 6: **chữ GIỐNG NHAU ở cả 3 bản**, biến thử là **HÌNH**.

| dòng | chữ | ký | vai | màu |
|---|---|---|---|---|
| 1 | `中性脂肪` | 4 | ① VỀ CÁI GÌ — keyword đo được cao nhất | trắng |
| 2 | `40時間` | 4 | ② CHUYỆN GÌ XẢY RA — **to nhất, rộng nhất**; con số KHÔNG đoán được ⇒ buộc phải bấm vào | **đỏ** |
| 3 | `3時のおやつ` | 6 | ③ PHẢI LÀM GÌ / mốc | **vàng** |

- **Gate 7 (`audience-45plus.md` §1):** che ảnh đi vẫn trả đủ 3 câu ✅. `40時間` là **lời hứa được nêu ở giây ~23 của video** và là tên của bài toán → thumbnail ↔ cold open liền mạch.
- **Đảo so với video 16 (luật Mục 15C):** 16 = cột chữ TRÁI · badge góc trên-PHẢI · HẬU QUẢ **vàng** → **17 = cột chữ PHẢI · người + vật bên TRÁI · badge 食卓 góc trên-TRÁI · HẬU QUẢ đổi sang ĐỎ, ĐÁP ÁN GIẤU đổi sang VÀNG**.
- **Vật hero:** đĩa quýt đã bóc cạnh **đồng hồ bàn chỉ đúng 3 giờ** — hai vật này chính là dòng 3.
- **Hero thắng bằng BỀ NGANG** (`ab-3title-3thumb.md` §3.1 Bước 2): prompt ép cỡ bằng **quan hệ với MÉP KHUNG**, cấm tả phần trăm.
- 🔴 **Trước khi viết prompt: mở `07_UPLOADED/16_banana-yoru-toire/_upload/thumbnail.png` ra NHÌN** rồi chép khuôn từ ảnh, **không** chép từ tài liệu (§3.1 Bước 1).

### Bộ 3 thumbnail A/B (mỗi bản đổi ĐÚNG 1 biến)

| | vai | biến |
|---|---|---|
| **T1** `thumb_T1_chuseishibo_base.png` | baseline khuôn kênh, đảo bên so với v16 | nền **tối moody**, bàn ăn chiều muộn |
| **T2** `thumb_T2_chuseishibo_bright.png` | đổi **1 biến hình** | **nền SÁNG** — bàn bên cửa sổ ban chiều. Chữ/layout/biểu cảm giữ y nguyên |
| **T3** `thumb_T3_chuseishibo_face.png` | đổi **layout** | mặt bà cụ to gần nửa khung (biểu cảm 「まさか」 nhìn tờ kết quả khám), bỏ hẳn quýt + đồng hồ |

⏳ **Chưa làm:** `thumb_prompts_FLOW.txt` / `_BLOCKS.md` / `_TENFILE.txt` / `_PLATE.txt` trong `06_VIDEO/17_chuseishibo-oyatsu/`. Sinh khi anh gật (mẫu: `tools/build_thumb_prompts_16.py`). Hai gate bắt buộc: **≤1.500 ký/prompt** · **khối `TEXT, exactly these N blocks` nằm trong 15% ĐẦU prompt**.

---

## 9. ⚠️ QUÉT COMPLIANCE (`youtube-compliance.md`)

| # | mục | kết quả |
|---|---|---|
| 1 | Từ tắt-ad ở **title/thumbnail** (殺/死/自殺/虐待 · **血** · 透析) | ✅ **0 hit**. `中性脂肪` và `動脈硬化` nói đúng trục mạch máu mà **không có chữ 血** — đây là lý do chọn từ dẫn này. Trong **lời đọc** có 「血管」「血の中の脂」 (được phép, §E1 chỉ cấm ở title/thumbnail) |
| 2 | Persona | ✅ không 医師/先生/管理栄養士/専門家. Gate S7 PASS. 「ここでは、お薬のお話は、いたしません」 |
| 3 | Tên thật hãng/người/viện | ✅ 0 tên người. 日本動脈硬化学会 là **tổ chức học thuật trích đúng tên + 年版**, hợp lệ và bắt buộc theo §YMYL |
| 4 | 概要欄 bắt buộc | ✅ ※医療免責 + credit `VOICEVOX:青山龍星` + 出典 (§11) |
| 5 | Tình tiết title/thumbnail **có thật trong video** | ✅ `「つい」3つ` = đúng 3 mục · `変えるのは一か所だけ` = quy tắc 器 trả ở 72,1% · `40時間` = ITEM1 ở 1:28 (10時間 × 4回) · `3時のおやつ` = つい① |
| 6 | Ảnh AI realistic trong video → **TICK "altered/synthetic content"** | 🔴 **CÓ** (nếu SLIDES dùng ảnh AI) — `upload_pack.py` chưa có cờ ⇒ **TICK TAY trong Studio** |
| 7 | Watermark ✦ ảnh AI | 🔴 **Xoá CẢ LÔ trước khi vào SLIDES**; soi 1:1 cả 4 góc (`media-library.md` §2.10 ⑤b) |

---

## 10. BẢNG ĐO KEYWORD (2026-08-18, API 30 ngày, JP/ja, long-form ≥8′)

`python tools\measure_kw_youtube.py "<kw>" --days 30` — 7 vòng, 32 keyword.

| keyword | n | med v/ngày | rổ | phán |
|---|---|---|---|---|
| **中性脂肪** ⭐ chọn làm từ dẫn | 19 | **2.111** | 脂質異常症・健診・シニア | ✅ cao nhất trong các rổ dùng được, **không có chữ 血** |
| **動脈硬化** ⭐ A2 | 11 | **1.118** | max = 漫画で学ぶシニアの人生CH **198.140 view/15 ngày** | ✅ rổ senior JP thuần |
| 動脈硬化 食べ物 | 7 | 55 | cùng video 198K ở trên | 🟡 cụm dài thì cầu loãng |
| 脳梗塞 前兆 | 11 | 22 | max **1.702.859**/25 ngày (整骨院) | 🟡 premise proven nhưng là **triệu chứng**, không phải 食卓 |
| 揚げ物 | 7 | **16.992** | 大食い · ドッキリ · Fischer's | ⛔ rổ SAI |
| 鶏むね肉 / そうめん / なす / トマト / ご飯 / オクラ | 6–15 | **5.506–15.189** | リュウジ · 笠原将弘 · タサン志麻 | ⛔ rổ SAI (đo 08-16, không đổi) |
| 認知症 食べ物 | 11 | 2.928 | vlog chăm 認知症 (ポジティブおばあちゃん · ミトログ) | ⛔ rổ SAI |
| 便秘 食べ物 | 4 | 2.316 | チベット体操 · 消化器医師 · 腸活コーチ | ⛔ rổ lệch |
| 眠りが浅い | 4 | 1.550 | 528Hz睡眠音楽 · ADHD配信者 | ⛔ rổ SAI |
| パン 食べ方 | 5 | 1.389 | ギャル曽根 · ホロライブ切り抜き | ⛔ rổ SAI |
| 足のむくみ | 7 | 894 | 足つぼ · 整体 · ASMR | ⛔ rổ SAI (và không có vật trên bàn ăn) |
| マグネシウム 不足 | 10 | 851 | ゆっくり食堂 105K + kênh tiếng Anh | 🟡 để dành |
| マーガリン | 3 | 512 | 内科医 · 陰謀系 | 🟡 để dành |
| 疲れが取れない 60代 | 8 | 403 | 旅行vlog · 筋トレ | ⛔ rổ SAI |
| チーズ 健康 | 5 | 264 | 内科医 · ゆっくり解説 | 🟡 |
| 物忘れ | 1 | 199 | — | ⛔ cung ~0 |
| 脳 食べ物 60代 | 13 | 148 | 脳トレ体操ch (không phải 食卓) | ⛔ |
| こむら返り / 足がつる | 3–4 | 105–121 | ⭐ có 1 video ĐÚNG rổ: ナースあおい「夏によく足がつる人は〇〇不足」1.219 view | 🟡 **ứng viên tốt cho video sau** — rổ đúng, góc còn trống, chỉ thiếu cầu |
| 寝つきが悪い | 2 | 143 | 睡眠音楽 | ⛔ |
| 血液ドロドロ | 3 | 91 | 医師 · 食で長生き | 🟡 cùng trục 17, để dành |
| くるみ 効果 | 1 | 54 | — | ⛔ |
| サラダ油 | 2 | 56 | あるあるチューブ (comedy) | ⛔ |
| 冷え性 食べ物 | 1 | 52 | — | ⛔ (sai mùa) |
| 手のしびれ | 3 | 33 | kênh tiếng Anh · 医師 | ⛔ |
| 中性脂肪 下げる | 7 | 31 | ダイエット系 | ⛔ cụm dài lệch sang giảm cân |
| 酢 食べ方 | 11 | 28 | 酢納豆 → đụng video 03 | ⛔ (không đổi so với 08-16) |
| 便秘 高齢者 | 17 | 18 | top 2 là kênh tiếng Anh; có 60歳以上のための健康情報CH 462 | 🟡 |
| 夜中 トイレ 高齢者 | 20 | 13 | rổ đúng nhưng **video 16 vừa làm** | ⛔ tự cạnh tranh |
| 夏バテ 高齢者 | 14 | 12 | 脳トレクイズ · 体操 | ⛔ |
| **シナモン 食べ方** | 15 | **9** | 3/3 video mạnh vẫn là 食べ合わせ | ⛔ **tụt từ 41 (08-13) → 9**, xác nhận bảng đo hết hạn trong vài ngày |
| 青魚 DHA | 3 | 6 | 高齢者健康の真実 621 view | ⛔ cầu tắt |
| 骨粗しょう症 食べ物 / 膝の痛み 食べ物 | 16 / 16 | 4 / 0 | 食べる健康習慣 (rổ đúng, view thấp) | ⛔ |
| おやつ 太らない | 2 | 5 | レシピ | ⛔ |

⭐ **Ba bài học của lượt đo này:**
1. **Cột `<món> 食べ方` của ngách senior đã cạn** — không còn ứng viên nào >50 v/ngày. Từ video 18 trở đi, **mặc định đo STAKE trước, món sau**.
2. **Bẫy rổ công thức là trạng thái mặc định, không phải ngoại lệ** — 6/32 keyword có med 5.500–17.000 và **không cái nào dùng được**. Bắt buộc mở tên kênh của top 3 trước khi chốt.
3. **Stake mở ra một bậc cầu khác hẳn món** (2.111 vs 9–48), nhưng **phải là stake có VẬT đặt được lên bàn ăn** — `足のむくみ` và `眠りが浅い` cầu cao mà không có vật nào để quay, nên rơi sang rổ massage/nhạc.

**Hàng đợi sau video 17:** `こむら返り × 食材` (rổ ĐÚNG, góc trống, cầu thấp — đo lại trước khi viết) · `血液ドロドロ` (cùng trục 17, **không** làm liền kề) · `マグネシウム 不足` · `チーズ` · hai key cũ 内臓脂肪/血圧 đo lại sau 6–8 tuần.

---

## 11. GÓI CTR / UPLOAD

### 3 dòng đầu 概要欄 (vùng hook — cấm lời chào)

```
ゆうべ夜十時に天ぷらを召し上がったなら、その脂が体から引くのは、今朝の八時ごろです。つまり今朝、朝ごはんを召し上がったとき、体はまだ、ゆうべの片づけをしていました。
一回の食事の片づけに十時間。朝・昼・夕、それに三時のおやつを足すと、片づけは四十時間ぶん。ところが一日は二十四時間しかありません。だから片づけは、必ず重なります。
この動画では、その重なりを作っている三つの「つい」と、時計を見なくてもできる一つの決めごとを、順にお話しします。買い足すものはなく、食べる量も減らしません。
```

### 概要欄 — mô tả đầy đủ

```
ゆうべ夜十時に天ぷらを召し上がったなら、その脂が体から引くのは、今朝の八時ごろです。つまり今朝、朝ごはんを召し上がったとき、体はまだ、ゆうべの片づけをしていました。
一回の食事の片づけに十時間。朝・昼・夕、それに三時のおやつを足すと、片づけは四十時間ぶん。ところが一日は二十四時間しかありません。だから片づけは、必ず重なります。
この動画では、その重なりを作っている三つの「つい」と、時計を見なくてもできる一つの決めごとを、順にお話しします。買い足すものはなく、食べる量も減らしません。

【目次】
00:00 ゆうべの天ぷら、その脂が体から引く時刻
01:16 一回の食事に十時間、一日で四十時間
02:22 洗い終わらない流しに、次のお客さまが来る
04:07 中井フサ子さん（六十九歳）の、正しい三時
05:37 高いことより、高いままの時間が長いこと
06:38 出典：動脈硬化性疾患予防ガイドライン2022年版と「随時175」
07:41 健診の紙に小さく書いてある、採血の時刻
08:41 つい①　三時のおやつ
09:58 つい②　寝る前のひと口
11:20 つい③　朝ごはんを抜く
12:31 なぜ、何十年も見つからなかったのか
14:37 五秒でできる、ご自分の一日の測り方
15:19 覚えるのは一つだけ ―― 器が出ている、そのあいだ
17:33 糖尿病のお薬・注射をお使いの方へ
18:57 フサ子さんが動かしたのは、みかん一つ
20:43 ご注意（健康に関する情報について）

一回の食事で上がった血液中の脂は、食べはじめてから三時間から四時間で山になり、食べる前の高さまで戻るのに十時間近くかかるとされています。お客さまが帰ったあとの流しに洗い物が残ったまま、次のお客さまが玄関に立っている。体の中で起きているのは、これと同じことです。油を減らしても数字が動かない方は、量ではなく回数でつまずいているのかもしれません。
洗い残しが続くと、油は壁や換気扇にうっすらと染みていきます。一日では何も起こりませんが、十年、二十年と続くと指でこすっても取れなくなる。血管の内側で起きているのも、これに近いことです。脂が高いこと、そのものより、高いままの時間が長いことが内側を疲れさせていきます。
日本動脈硬化学会の「動脈硬化性疾患予防ガイドライン2022年版」では、それまで朝の空腹時だけだった中性脂肪の基準に、食事の時間に関係なく測った「随時」の基準として175mg/dL以上が新しく加わりました。食べていない時よりも、食べたあとの数値のほうが心臓や血管の病気と結びついていたと報告されてきたからだとされています。体を測る側の目も、「何を食べたか」から「食べたあと、どうなっているか」へ移ってきているのです。お手元に去年の健診の紙が残っていましたら、採血をした時刻が小さく書いてあるはずです。
そのうえで、重なりを作っている三つの「つい」を見ていきます。一つ目は三時のおやつ。昼と夜のあいだの七時間は一日でいちばん長い休みですが、そのまんなかで何かを口に入れると三時間と四時間に割れてしまいます。二つ目は寝る前のひと口。眠っているあいだの十二時間近い休みが、十時半のお茶うけひとつで八時間になります。三つ目は、朝ごはんを抜くこと。休みは長いほどいいはずなのに、なぜ抜いてはいけないのか。その落とし穴も動画の中でお話しします。
三つとも、まわりからほめられる行いです。甘いお菓子ではなくみかんを選ぶ。夜は軽くすませる。食べすぎた翌朝は抜いて調整する。だから何十年も見つかりませんでした。間違っていたのは中身でも努力の量でもなく、置いた場所でした。
最後に、覚えていただくのは一つだけです。取り上げる食べ物は一つもありません。買い足すものもなく、時計を見る必要もない決めごとを、動画の終わりでお伝えします。

【出典】
・日本動脈硬化学会「動脈硬化性疾患予防ガイドライン2022年版」

※糖尿病のお薬や注射をお使いの方は、食事の間隔をあけることがかえって危ない場合があります。おやつの時間を動かす前に、必ずかかりつけの先生にご相談ください。
※この動画は公表されている資料をもとにした健康に関する一般的な情報です。個別の医療アドバイスではありません。持病のある方、お薬を飲んでいる方は、食事を変える前に必ずかかりつけの先生にご相談ください。
※音声合成：VOICEVOX：青山龍星

#60代からの食卓 #シニアの健康 #中性脂肪 #60代 #食生活 #健康長寿 #動脈硬化 #健康診断 #おやつ
```

### タグ (bộ nhận diện kênh 16 tag đứng đầu, rồi tag riêng video)

```
60代 食べてはいけない, 60代 食事, 60代からの食卓, シニア 健康, 60代 健康, 70代 健康, 高齢者 食事, シニア 食事, 健康長寿, 老後 健康, 60歳から, 食生活 改善, 健康 食べ物, シニア 栄養, 60代 生活, みのり, 中性脂肪, 中性脂肪 下げる, 中性脂肪 食事, 動脈硬化, 動脈硬化 予防, 血管, 血管 若返り, 健康診断, 脂質異常症, 食後高脂血症, おやつ 時間, 間食, 3時のおやつ, 朝ごはん 抜く, 寝る前 食べる, 60代 おやつ, 食べる時間, 食事の間隔, 日本動脈硬化学会, ガイドライン 2022
```

### 📌 固定コメント (pinned comment — ghim sau khi công khai)

```
最後まで見てくださって、ありがとうございます。案内人のみのりです。

今日お伝えしたかったのは、一つだけです。一回の食事の片づけには十時間近くかかります。朝・昼・夕、それに三時のおやつを足すと四十時間ぶん。一日は二十四時間しかありませんから、片づけは必ず重なります。中性脂肪でつまずいている方の多くは、食べる「量」ではなく、食べる「回数」でつまずいています。

決めごとは一つだけ。口に入れるのは、食卓に器が出ている、そのあいだだけ。三時のみかんは、お昼の器がまだ出ているうちにむく。寝る前のお茶うけは、夕食の器を下げる前に一緒に出す。やめるのではなく、くっつける。それだけで、片づけは四回から三回に減ります。

よろしければ、二つ教えてください。
① 皆さんのお宅では、三時に何を召し上がっていますか。
② 次に取り上げてほしい食べ物があれば、ぜひ。
コメントは全て読ませていただいております。皆さんの一言が、次の回の何よりの励みになります。

〔ひとつだけ、大切なお願い〕
糖尿病のお薬や注射をお使いの方は、食事の間隔をあけることが、かえって危ないことがあります。おやつの時間を動かす前に、必ずかかりつけの先生にご相談ください。持病のある方、お薬を飲んでいらっしゃる方も同じです。今日のお話は、公表されている資料をもとにした一般的な健康情報で、医療のアドバイスではありません。

今夜の食卓が、皆さんの明日の元気につながりますように。どうか、ご自分の体を大切に。
――みのり
```

---

## 12. ✅ LỚP HÌNH v3 — 99 cảnh ẢNH THẬT + BUILD-ON (thiết kế lại 2026-08-18)

> **Vòng 1 (v2) đã bị BÁC.** Tao dựng thử 13 thẻ số liệu kiểu `vox` (nền kem, hộp chữ, mũi tên vẽ) — user xem sheet và chốt: *"tao không muốn dùng những ảnh viết bằng slides. Tao muốn dùng ảnh thật rồi thêm các ảnh minh họa hiệu ứng vào, bỏ hết dạng ảnh viết tay kiểu này đi."*
> ⇒ **Lớp thẻ chữ bị gỡ sạch.** `channels.py` đặt `"vox": None` cho shokutaku kèm lý do; palette thử nghiệm trong `make_vox.py` đã revert. `media-library.md` §2.9 (cấm mọi slide-chữ ở health+shokutaku) **giữ nguyên hiệu lực, không có ngoại lệ nào được mở**.

**Xương lớp hình = `_media_library/make_shot.py`** — build-on **bằng HÌNH**, mượn từ co-dai video 22 (66/79 entry). Khung **đứng yên tuyệt đối** (không pan, không Ken Burns — `feedback_video_no_motion_mot_giong`), cái động là **ảnh được lắp vào**:

| mode | cảnh nào dùng | trả lời kiểu câu nào | video 17 |
|---|---|---|---|
| `inset` | ảnh nền + tấm ảnh macro trượt lên 26px, viền trắng đổ bóng, rồi mũi tên đỏ vẽ dần tới điểm cần nhìn | "phóng to chỗ này" | **29** |
| `focus` | vòng khoanh đỏ vẽ dần như bút dạ, ngoài vòng tối đi 18% | "đây, chính chỗ này" | **27** |
| `soft` | ảnh đứng, chỉ thở ±1,5% sáng | câu kể — để vòng đỏ không lặp 60 lần | **39** |
| `wipe` | ảnh B lộ dần đè lên ảnh A, đường wipe dọc có vệt sáng | **đổi trạng thái**: bếp bừa→sạch, tường sạch→ám dầu, mâm bày→dọn | **4** |

**Nhịp mỗi cảnh:** 0s nền có mặt → 0,55s phần tử 1 → 1,70s phần tử 2 → 2,55s nhãn (nếu có) → **đứng im**, idle loop 4s thở.

### 12.1 Số liệu đi bằng ẢNH, không bằng thẻ chữ

13 điểm số của bài giờ là **ảnh thật có vật đếm được** + **nhãn ngắn đè lên** (hộp nhỏ của `make_shot`, ≤10 ký):

| mốc | ảnh (số nằm TRONG ảnh) | nhãn |
|---|---|---|
| 1:37 | 3 đĩa xếp hàng, cái thứ ba còn đầy | `3〜4時間で山` |
| 1:52 | đồng hồ cát, cát mới xuống 1/3 | `10時間` |
| 2:15 | **4 mâm cơm chen nhau trên bàn quá nhỏ** | `24時間しかない` |
| 3:05 | 4 đĩa trắng rỗng xếp hàng | `4回` |
| 7:32 | sổ guideline đóng + ống máu, bìa trắng không đọc được chữ | `175` |
| 9:33 | 2 mâm hai đầu bàn dài, 1 đĩa nhỏ đúng giữa | `3時間と4時間` |
| 11:06 | futon trải + đĩa bánh trên bàn đầu giường | `8時間` |
| 12:23 | bàn ăn trống trơn, đúng 1 cốc cà phê | `17時間` |
| 16:02 | 6 đĩa rải dọc bàn, không cái nào xa nhau | `4時間もない` |
| **16:53** | mâm cơm bày đủ, **quả quýt đặt trên vành mâm** | `器のあいだだけ` ⭐ |
| 18:08 | đúng 3 mâm, không có đĩa phụ nào | `4回 → 3回` |

⇒ Che nhãn đi thì **bức ảnh vẫn nói được con số** — đó là chỗ khác nhau giữa "ảnh minh hoạ" và "thẻ chữ".

| | |
|---|---|
| SLIDES | `04_SCRIPTS/17_chuseishibo-oyatsu_SLIDES_photo.json` — **99 cảnh** · 14,2 giây/cảnh · **4,23 đổi hình/phút** (trần 6) · gap **6,2 – 34s** |
| Prompt | `slide_prompts_FLOW.txt` (1 dòng/prompt, bơm extension) · `_BLOCKS.md` · `_TENFILE.txt` (tên file ↔ mốc ↔ **mode** ↔ cue) |
| Hồ sơ kênh mới | `motion: False` (tắt pan — pan + build-on = hai chuyển động đánh nhau) · **`transition: dissolve 0.45s`** (trước đây **thiếu**, tức đang vi phạm `audience-45plus.md` §2 mục 3) · **`watermark: 60代の食卓`** |
| Giọng | ✅ **XONG** — `06_VIDEO/17_chuseishibo-oyatsu/voice.wav` · **21′05** · 60,7 MB · `VOICE_EXIT=0` · VOICEVOX **青山龍星 / しっとり / 速0.8** (style lấy từ base tag dòng 1 của `_TTS.md`) · chạy NỀN qua `run_voice17.cmd`, log `voice.log` |

### 12.1 🔴 ĐỘ DÀI THẬT 21′05, KHÔNG PHẢI 23′24 — hiệu chuẩn lại CPS

| | ước (`check_coldopen.py`) | **đo thật trên `voice.wav`** |
|---|---|---|
| tổng | 23′24 | **21′05** (−139s = **−9,9%**) |
| CPS gộp | 4,40 ký/s + 0,25s/dòng | **4,66 ký/s** |
| cold open | 89 giây | **~79 giây** |
| TRẢ LOOP | 16:51 | **~15:10** |

- **Vẫn nằm trong dải 21–25′** (`CLAUDE.md` §RETENTION) nhưng **sát mép dưới** — nếu vòng sửa sau có cắt gì thì rơi ra khỏi dải, phải bồi lại.
- **Mọi con số % ở §3 giữ nguyên** (bài co đều), chỉ cột phút lệch ~9,9%. **Số phút thật lấy từ `subs.srt` sau khi render**, đúng luật §12 mục 5 — đừng chép cột phút của §3 vào 【目次】.
- ⚠️ Mô hình 4,40 là bản **cố ý chậm để không undershoot** (ghi trong header `check_coldopen.py`). Nó undershoot ~10% ⇒ **gate cold open 90 giây thực chất đang siết ở ~80 giây thật** — chặt hơn ý định, chấp nhận được, nhưng đừng "sửa" nó về 4,66 chỉ vì khớp video này (đúng cái bẫy tool đã cảnh báo: *khớp một video không phải là đúng*).

### 12.2 ✅ KIỂM TAG NHẤN NHÁ CÓ ĂN THẬT KHÔNG (bắt buộc, `humanize-script-voice.md` §2)

| tag | cách kiểm | kết quả |
|---|---|---|
| `[後間1.0]` sau câu payoff | `silencedetect` quanh mốc payoff | ✅ **im lặng 1,31s** ngay sau 「…そのあいだだけ。」 (và 1,14s ở 「覚えていただくのは、一つだけです」) — đúng ý đồ "nghỉ → thả chữ → im lặng" |
| `[速0.8]` | **thí nghiệm đối chứng** — cùng một câu, base 1,0, có tag vs không tag | ✅ **4,33s → 5,50s = +27,1%** |

⛔ Không đo bằng ký/giây (luật ghi rõ số đó là **rác** vì 「」và「……」 tính là ký nhưng không phát âm).

**Demo để nghe trước khi render video:** `demo_hook.mp3` (0–48s, cold open + cửa tử) · `demo_payoff.mp3` (14:55–15:50, cú lật → quy tắc 器 → im lặng).

**Gate đã qua:** 0 cue trùng (mỗi `match` khớp **đúng một** dòng `_TTS.md`) · 0 entry cách nhau <6s · SHOT **không chỗ nào tả tỉ lệ** (tool chặn `%` / `two-thirds` — `media-library.md` §2.10 ⑥) · 100% ảnh, **0 slide-chữ** (§2.9) · giấy tờ trong ảnh đều ghi `print unreadable` (§2.10 ⑦).

⭐ **Ba thứ cố ý thiết kế:**
1. **Entry 0 = đĩa tempura + đồng hồ chỉ 10 giờ đêm** — đúng câu đầu tiên, đúng luật "hình đầu là chủ thể" (§2.0), và **đồng hồ nối thẳng sang thumbnail**.
2. **Ẩn dụ xuyên bài dùng CÙNG MỘT GÓC MÁY 3 lần** — chậu bát chưa rửa lúc mở khối (2:37) → cùng khung nhưng chồng cao hơn (6:05) → dọn mâm ở payoff. Mắt nhận ra là một mạch, không cần lời giải thích.
3. **Ống cao su cắt dọc quay lại đúng góc cũ** (0:33 → 6:19) với thành ống dày hơn — cho thấy "mười năm" bằng hình, không bằng chữ.

⚠️ **Ảnh chưa có** → `render-background.md` §1.5: **chưa được render video**. Thứ tự: gen 110 ảnh → xoá ✦ cả lô → duyệt contact sheet → mới ghép.

---

## 13. VIỆC CÒN LẠI

| # | việc | trạng thái |
|---|---|---|
| 1 | Anh duyệt bản 2 + Title CHỐT + bộ chữ thumbnail (`中性脂肪 / 40時間 / 3時のおやつ`) | ⏳ **chờ** |
| 2 | Gen 110 ảnh theo `slide_prompts_FLOW.txt` → xoá watermark ✦ cả lô → contact sheet duyệt mắt | ⏳ |
| 3 | `thumb_prompts_FLOW/BLOCKS/TENFILE/PLATE.txt` + 3 ảnh T1/T2/T3, xoá ✦ cả lô, soi 1:1 bốn góc | ⏳ |
| 4 | Render (chạy NỀN, `render-background.md`): `python tools\video_render.py 04_SCRIPTS\17_chuseishibo-oyatsu_TTS.md --channel shokutaku --slides ... --sub-style outline --bgm-gain -40` | ⏳ |
| 5 | Thay 【目次】 bằng timestamp thật từ `subs.srt` (**không** dùng số ước ở §3) | ⏳ |
| 6 | Slot đăng: T2·T4·T6 12:00 JST — video **thứ 5** của loạt "cày tới mốc 8" | ⏳ |
