# 20 — 脳梗塞：その朝は、前の晩に決まっていた（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **脳梗塞・動脈硬化 × 血管の内側の「かさぶた」 × 前の晩の食卓**
- **Bản đọc chuẩn:** `20_nokosoku-kasabuta_TTS.md` — **bản 2** · **4.895 ký (thuần) · 240 dòng · ước 19′32** (CPS 4.40 + GAP 0.25/dòng). Dưới 20 phút theo yêu cầu user. Bản 1 lưu ở `_v1_20_nokosoku-kasabuta_TTS.md.bak`.
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 20` → ✅ **PASS, cold open 80 giây** (L1–L5 · S6 · S7 sạch, dư 10s) · **36 tag đặt CÓ CHỦ ĐÍCH** ở 36 khoảnh khắc (gỡ sạch rồi gắn lại — §0f), gồm 1 đỉnh bài `[間1.2][速0.8][後間1.0]` · 0 tag giữa câu · 0 tag đứng dòng riêng · blacklist Mục 7 = 0 · YMYL cấm = 0 · **ITEM1 01:20 · CTA giữa 47,4% · loop nhân vật khép 87,7%**.

---

## 0. 🔴 VÒNG SỬA — bản 1 PASS mọi gate máy nhưng chỉ đáng **6,5/10**

> user: *"kịch bản có giữ chân không, có rớt lúc đầu không? người xem đến vì cái gì, ở lại vì cái gì? phải có hồn, hook phải ấn tượng, nội dung không được rời rạc"*

### 0a. Giây 13 là câu TỰ THÁO NGÒI — gate S6 trượt vì lý do kỹ thuật
Bản 1: 「本当に怖いのは、塩そのものではありません」 ở giây 13. `DEFUSE_HARD` chỉ bắt khi phủ định **đúng chủ thể trên title**; chủ thể là 「その一皿」/カップ麺 còn câu phủ định là 「塩」 → **trượt gate, nhưng người xem cảm nhận y hệt** ba video đã đo được rớt 45–55 điểm ở đúng khung 20–40s.
⇒ **Bài học cho gate:** S6 đang đo *hình thức thi hành* (chuỗi chữ), không đo *cơ chế* (có gỡ lời buộc tội hay không). Cùng họ với `humanize-script-voice.md` §1.2 (ENUM_RE chỉ bắt `一つ。` đứng trơ) và `audience-45plus.md` §6.10 (gate đo sai chiều).

### 0b. Giây 25→49: SÁU câu liên tiếp giảng cơ chế
皮 → 傷 → かさぶた → 太る → はがれる → 脳梗塞. Đúng kiến thức, nhưng đặt ngay cửa tử thì người xem chưa có lý do nghe giảng. Đây đúng lỗi §0a của video 18 (*"ITEM1 là một BÀI GIẢNG rời, không phải một CẢNH"*) — đã biết mà vẫn dính.

### 0c. Triệu chứng SAI LOẠI
Bản 1 dùng `ふらっとする` / `手先が冷える` — **không phải dấu hiệu đột quỵ** (đó là tụt huyết áp tư thế và tuần hoàn ngoại vi). Vừa yếu về giữ chân vừa không đẹp về YMYL. Bản 2 thay bằng **前兆 thật của TIA**: `手が一瞬しびれる` · `ろれつが回りにくい` — đúng cầu đã đo (`脳梗塞 前兆` n=11) và đúng y học.

### 0d. LỖ LỚN NHẤT: loop bị ĐOÁN
Bản 1: 「三つ目を止める一品は、昔からお味噌汁の中にありました」 → người Nhật 60–80 đoán ra **わかめ** trong 2 giây. Loop bị đoán = loop chết, 14 phút giữa mất lực kéo. Video 11 đã học đúng bài này (§2.8: *"loop mới không đoán được"*).

### Bản 2 sửa bằng cách đổi SỢI CHỈ, không vá câu

⭐ **「その朝は、前の晩に決まっていた」**

Loop cũ hỏi *"món gì"* (đoán được). Loop mới hỏi ***"cái gì quyết định buổi sáng đó"*** — người xem đang chờ "sáng phải làm gì", đáp án là **"tối qua đã quyết rồi"**. Không đoán được, và nó gắn kết cả bài:

| bản 1 | bản 2 |
|---|---|
| mở bằng tô mì + con số muối | mở bằng **MỘT CẢNH**: 和夫さん với tay lấy kính, tay không nghe lời, 30 giây rồi hết → **hai ngày sau thì gục** |
| 和夫さん xuất hiện ở 09:06 rồi biến mất | 和夫さん có mặt **từ giây 0**, được nhắc 3 lần giữa bài, **khép vòng ở 17:08 (87,7%)** |
| ふみ江さん không liên quan gì tới 和夫さん | ふみ江さん là **mặt đối xứng**: 「ご主人が倒れてから、夜の食卓を変えました」 — cùng một bàn ăn tối, hai kết cục |
| 1 loop, trả ở 75% | **3 tầng loop**: 「二時間」(51%) → 「前の晩の三つ」(67%) → **「和夫さんはどうなったのか」(87,7%)** |
| わかめ là phần thưởng cuối | わかめ nằm trong **bộ ba của buổi tối** (nước · nửa bát nước súp · わかめ), cả ba làm xong trong 3 phút trước khi ngủ |

🔴 **Vì sao loop nhân vật ở 87,7% mới là loop LỚN, không phải loop nội dung ở 67%:** rule đòi trả loop lớn ở 80–85%. Bài này trả **nội dung** sớm (65–70%) là cố ý — phần cuối không phải phần thừa mà là **phần trả nợ cảm xúc**: người xem ở lại để biết 和夫さん ra sao. Cú chốt 「変わったのは、朝ではありません。前の晩でした。」 ở 17:08 đóng nhân vật và đóng luận điểm bằng cùng một câu.

### 0e. Thêm hai khối, đều nằm trên sợi chỉ 「前の晩」
- **塩と脂が同じお皿に載る日** (07:49) — ラーメン・揚げ物の惣菜・練り物: 「内側からすれば、二人がかりで攻められている」. Nối chặng ① với chặng ②, chúng thôi rời nhau.
- **夜の寒暖差** (12:31) — お風呂前に脱衣所を温める · 夜中のお手洗いに一枚羽織る. Đúng sợi chỉ (buổi tối), đúng mùa (sắp lạnh), và là nguy cơ thật của senior JP.

### 0f. Lớp nhấn nhá: gỡ SẠCH rồi gắn lại
Bản 1 có **88 dòng có tag** = rải đều = không có gì được nhấn. Đã gỡ hết rồi đặt lại **36 tag ở 36 khoảnh khắc cụ thể** (đỉnh bài · câu đấm của anecdote · reveal · im lặng sau câu chốt). Chất người đến từ **chênh lệch**, không từ mật độ (`humanize-script-voice.md` §2).

---

## 0.1 ⚠️ ĐỀ TÀI NÀY RỦI RO YMYL CAO NHẤT TỪ TRƯỚC TỚI NAY

Lần đầu kênh viết về một **bệnh cấp cứu**. Bốn lớp bảo vệ, **không được gỡ khi rút gọn**:

1. **Khối cấp cứu FAST ở 11:41** — 「片方の手に力が入らない／言葉が出にくい／顔の片側が下がる → 様子を見ないで、すぐ救急車」 + 「治まったあとに本番が来ることがあります」. Bản 2 nối thẳng vào nhân vật: 「和夫さんの三十秒が、まさにそれでした」 — vừa là điều đúng phải nói, vừa là chỗ bài đắt nhất.
2. **Ba cảnh báo tương tác ở 15:18** — 腎臓 × カリウム · **ワーファリン × 海藻/納豆 (ビタミンK)** · **昆布 × ヨウ素 × 甲状腺**. Rất ít kênh nói đủ ba. Cảnh báo đầu còn được nói **trước** ở 04:35 để người thuộc nhóm rủi ro biết sớm.
3. **Không hứa phòng được đột quỵ.** Toàn bài 守る・和らげる・なだらかにする; 0 lần 治る/完治/予防できる/絶対.
4. **Mọi con số verify được** — §8.

⚠️ **Về độ dài:** `CLAUDE.md` §① đã đổi theo user (dưới 20′), nhưng dải cũ 21–25′ dựa trên số đo (納豆 29′→15′ làm AVD phút tụt 4′33 → 3′11). Nếu AVD phút của 19/20 thấp hơn 17/18 thì **độ dài là biến đầu tiên xét lại**.

## 1. Người xem đến vì cái gì, ở lại vì cái gì

- **Đến vì:** nỗi sợ lõi và trực tiếp nhất của tệp 60–80 — **脳梗塞 → 半身が動かない → 寝たきり → 迷惑をかけたくない**. Không cần bọc.
- **Ở lại vì — ba thứ, không phải một:**
  1. **Một người có thật để lo cho.** 和夫さん xuất hiện ở giây 0 với bàn tay không nghe lời trong 30 giây. Người xem ở lại để biết anh ta ra sao — đó là loop mạnh nhất, và nó chạy suốt 17 phút.
  2. **Một câu đố không đoán được.** 「あの二時間を通り抜けられるかどうかは、前の晩に決まっている」 — không ai đoán ra "tối qua" khi đang chờ nghe "sáng làm gì".
  3. **Bốn việc làm được ngay, không tốn tiền** — để lại nửa nước súp · đặt đũa xuống · cốc nước trước khi ngủ · một nhúm wakame vào bát canh.

## 2. ĐO CẦU (API YouTube Data, 30 ngày, JP/ja, long-form ≥8′, đo **2026-08-25**, 3 vòng / 18 keyword)

| keyword | n | med v/ngày | max | rổ |
|---|---|---|---|---|
| **動脈硬化** | 14 | **1.103** | 16.551 | max là kênh Anh ngữ; #2 = 漫画で学ぶシニアの人生CH「血管が詰まって脳梗塞の原因になる高齢者が避けるべき食品7選」**277.287 view / 22 ngày** — rổ senior JP thuần |
| **脳梗塞 予防** ⭐ chọn | 12 | **1.006** | 43.939 | からわかラボ「脳梗塞で倒れた人が数日前に感じていた異変7選」**354.240 / 8 ngày** · やさしい予防医学 190.591/27d |
| 心筋梗塞 | 6 | 1.037 | 12.568 | rổ pha (1 drama + 1 vlog ung thư) |
| 血管 若返り | 16 | 783 | 2.401 | ⛔ rổ 整体/トレーナー, không phải 食卓 |
| 高血圧 食事 | 6 | 575 | 1.462 | rổ đúng (長寿の食卓TV) nhưng n nhỏ |
| 納豆 血管 | 7 | 478 | 8.502 | rổ đúng — ⛔ kênh đã có video 03 納豆 |
| **脳梗塞 前兆** | 11 | 27 | 43.937 | cầu dồn vào 2 video top — **nhưng chính nó cho bản 2 chất liệu cold open** |
| **脳梗塞 食べ物** | 14 | **5** | 43.937 | 🔴 xem ghi chú dưới |
| 血圧 下げる 食べ物 | 13 | **3** | 44 | 🔴 nguội hẳn (§2.9 đo 8 → nay 3) |
| コレステロール 下げる 食べ物 | 6 | 2 | 349 | 🔴 nguội |
| **血管を強くする食べ物** | **0** | **0** | — | 🔴 **0 video long-form/30 ngày** |
| 脳卒中 予防 食べ物 | 4 | 0 | 2 | 🔴 dùng 脳梗塞, đừng dùng 脳卒中 |
| さば缶 | 6 | 4.387 | 47.510 | ⛔ **rổ SAI 100%** (リュウジ · ゆかり · 毎日中華) |
| 減塩 高齢者 / 手足のしびれ / 青魚 EPA / 血栓 予防 | 19/4/3/3 | 3/6/3/61 | — | ⛔ cầu tắt hoặc cung mỏng |

🔴 **Phát hiện quyết định cách viết: cột "MÓN ĂN cho mạch máu" đã CHẾT, cầu nằm ở CẢNH BÁO + DẤU HIỆU.** `血管を強くする食べ物` = **0 video**, `血圧 下げる 食べ物` = 3, `コレステロール` = 2, `脳梗塞 食べ物` = 5 — trong khi `脳梗塞 予防` = 1.006 và hai video top của cụm ăn **354K/8 ngày** và **277K/22 ngày**. ⇒ Giữ đúng đề tài user yêu cầu (đồ ăn × tim mạch/đột quỵ), nhưng **vào bằng cửa STAKE**. Bước thứ ba của cùng một đường: §2.11 MÓN→STAKE · §2.14 STAKE→DƯỠNG CHẤT · §2.15 **→BỆNH**.

⚖️ **Ràng buộc riêng của kênh đã xử lý:** `youtube-compliance.md` §3 cấm chữ **血** trên title/thumbnail. `脳梗塞` và `動脈硬化` **không có chữ 血** → cửa chính để vào trục mạch máu (cùng cơ chế video 17 dùng `中性脂肪`). Chữ 血 vẫn dùng thoải mái trong thân bài + 概要欄 + tag.

⚠️ **Chống tự cạnh tranh với video 17 (中性脂肪 × 動脈硬化):** 17 = mỡ sau ăn + khoảng cách bữa ban ngày; 20 = lớp lót mạch máu + **buổi tối quyết định buổi sáng**. Món chốt khác hẳn (17 = おやつ · 20 = わかめ). 動脈硬化 ở 20 chỉ 1 câu, như tên gọi của cục vảy. Cách nhau 3 số.

## 3. STAKE & KHUÔN

1. **MỘT ẩn dụ, và nó là CƠ CHẾ THẬT:** 血管の内側 = 一枚の薄い皮 → 傷 → **かさぶた** → 太る → はがれる → 流れ着いて詰まる. Giải thích được **cả 動脈硬化 lẫn 脳梗塞 bằng một hình ảnh**, và chia bài thành 3 chặng tự nhiên. So sánh 膝をすりむいたとき để senior hình dung ngay.
2. **SỢI CHỈ: 前の晩 → 朝.** Mọi khối đều trả lời cùng một câu: *cái gì trong buổi tối hôm trước quyết định buổi sáng hôm sau*. Kể cả khối 寒暖差 (お風呂・夜のお手洗い) cũng là buổi tối.
3. **Khuôn: 「かさぶたの一生 × 前の晩」** — ① できる (塩 · 早食い) → ② 育つ (古い脂 · 色の濃い野菜) → ③ はがれる (朝の二時間) → **cú lật: nhưng buổi sáng thì không sửa được nữa**. Bốn video liền kề không cùng dáng ✅ (17 = 時計を追う · 18 = 鎧 · 19 = 逆から歩く một ngày · **20 = một đời của cục vảy + cú lật thời điểm**).
4. **Hai nhân vật là MỘT CẶP ĐỐI XỨNG**, không phải hai case rời: 和夫さん (30 năm uống cạn nước súp → buổi sáng đó) ↔ ふみ江さん (chồng gục → đổi bàn ăn tối → nửa năm bình yên). Cùng một bàn ăn tối, hai kết cục.
5. **Chất người ≥4/6 mũi tiêm:** ① みのり tự thú 「あの最後の一口が、いちばんおいしいんですよね」 ② 和夫さん có thoại 「もったいないだろう、あれが一番うまいんだから」 + chi tiết đời sống (chìa khoá xe luôn để cùng một cái đĩa nhỏ) ③ ký ức giác quan — miếng わかめ khô đen quắt nở lại thành xanh trong bát ④ みのり tự đổi thói quen ⑤ ふみ江さん đóng bằng cảm xúc 「主人と、まだ二人で歩けているのが、うれしくてね」 ⑥ phá nhịp 「三十年、その晩が続きました。その三十年が、あの朝の三十秒に、つながっていました。」

**Mốc thời gian (ước từ mô hình, cập nhật lại từ `subs.srt` sau render):**

| mốc | khối | luật |
|---|---|---|
| 00:00 | **CẢNH mở**: 和夫さん với tay lấy kính, tay không nghe lời, 30 giây | hook = một cảnh, không phải một con số |
| 00:18 | 「倒れたのは、その二日後の朝です」 | cú đấm |
| 00:24 | 前兆 thật (しびれ · ろれつ) — kéo người xem vào | thay triệu chứng sai loại của bản 1 |
| 00:40 | gieo loop 1 「たった二時間」 · 01:00 gieo loop 2 「前の晩に決まっている」 | |
| 01:20 | **ITEM1 = ① できる (塩 · 早食い)** | payoff #1 ≤4′ ✅ (cold open 80s) |
| 02:33 | 原典: 厚労省 食事摂取基準 2025年版 | lớp `genten` ✅ |
| 04:35 | persona + đăng ký + ⚠️ cảnh báo thuốc/thận (1/2) | phải SAU mục đầu ✅ (L3) |
| 05:43 | **② 育つ** · 07:49 塩と脂が同じお皿に | |
| 08:26 | **和夫さん — 三十年の晩** | 43% |
| 09:15 | **CTA giữa + checkpoint 「に」** | 47,4% |
| 09:55 | **TRẢ LOOP 1 = 目が覚めてからの二時間** | 51% |
| 11:41 | 🚑 **khối cấp cứu FAST** (+ 「和夫さんの三十秒が、まさにそれでした」) | không được cắt |
| 12:31 | 夜の寒暖差 (お風呂 · 夜中のお手洗い) | |
| 13:05 | **TRẢ LOOP 2 = 朝は前の晩に決まる** · 13:38 前の晩の三つ | 67% |
| 15:18 | ⚠️ 3 cảnh báo: 腎臓/ワーファリン/ヨウ素 | lớp uy tín |
| 16:24 | ふみ江さん (mặt đối xứng của 和夫さん) | 84% |
| 17:08 | ⭐ **KHÉP LOOP NHÂN VẬT** — 「変わったのは、朝ではありません。前の晩でした」 | **87,7%** ✅ |
| 17:26 | recap · 18:2x disclaimer | |
| 19:32 | hết | <20′ theo yêu cầu user |

## 4. Bộ title A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代の落とし穴】脳梗塞が起きる朝は、前の晩に決まっています｜寝る前の三つ` | 39 | 脳梗塞@11 | keyword có cầu cao nhất **không chứa chữ 血** + khung cảnh báo P0 + **cú lật của bài nằm ngay trong title** |
| **A2** | `動脈硬化は"かさぶた"｜60歳を過ぎたら、寝る前にやめたい習慣とやりたい三つ` | 38 | 動脈硬化@0 | đổi keyword dẫn (med 1.103 > 脳梗塞 1.006) và đưa lên đầu câu |
| **A3** | `その朝の三十秒を、見逃さないで｜60代の脳梗塞は、前の晩の食卓から始まります` | 38 | — | đổi kiểu hook: dẫn bằng **chi tiết của cold open** (30 giây bàn tay không nghe lời) thay vì bằng khái niệm |

### Title CHỐT

```
【60代の落とし穴】脳梗塞が起きる朝は、前の晩に決まっています｜寝る前の三つ
```

**Tên file upload:** `nokosoku-maenoban-kasabuta-60dai.mp4`

## 5. TEXT THUMBNAIL (chữ GIỐNG NHAU ở cả T1/T2/T3)

| dòng | chữ | ký | vai (gate 7) | màu |
|---|---|---|---|---|
| 1 | `昨日の晩` | 4 | ① VỀ CÁI GÌ — **thời điểm**, và đó chính là cú lật của bài | kem/trắng ngà |
| 2 | `脳梗塞` | 3 | ② CHUYỆN GÌ XẢY RA — **hero, to nhất**, keyword có cầu | **ĐỎ** |
| 3 | `正解は寝る前` | 6 | ③ PHẢI LÀM GÌ — khớp khuôn kênh 「正解は食後」(18)「正解は朝」(19) | vàng kim |

- Che ảnh đi vẫn đọc ra: "tối qua — đột quỵ — đáp án nằm ở trước khi đi ngủ" ✅ Bộ chữ này **nói đúng cú lật** của bài; bản 1 để `正解は海藻` — vừa spoil payoff vừa lệch sợi chỉ.
- Gate 1 (≤6 ký) ✅ · gate 3 (3 dòng) ✅ · gate 6 (nền sáng) ✅
- **Không một chữ 血** ở title lẫn thumbnail ✅
- **Đảo biến so với video 19:** 19 = hero VÀNG + cột chữ TRÁI → 20 = hero **ĐỎ** + cột chữ **PHẢI**, badge 「食卓」 trên-TRÁI.

## 6. PROMPT ẢNH THUMBNAIL — 4 file trong `06_VIDEO/20_nokosoku-kasabuta/`

Khuôn lấy từ ảnh đã lên sóng của kênh (16/17/18/19): photorealistic, phòng ăn Nhật sáng, bà cụ ~68 tóc bạc ngắn + tạp dề be trên áo xanh, con dấu tròn ĐỎ 「食卓」, dải vàng kim mép, chữ 3 dòng 袋文字 viền nâu đậm + halo trắng.

**Ba bản, mỗi bản đổi ĐÚNG 1 biến:** T1 baseline (chữ nửa PHẢI, người TRÁI bưng tô mì + bát canh わかめ trên bàn) · T2 đổi **CROP** (close-up sát mặt) · T3 đổi **LAYOUT** (đảo trục).

⚠️ Sau khi gen: soi TỪNG ký tự (`脳`·`梗`·`塞` rậm nét nhất) → **VÁ watermark ✦, KHÔNG cắt** → gate 168px → đặt tên `thumb_T1/T2/T3_nokosoku.png` → trần 2 MB.

## 7. QUÉT COMPLIANCE (`.claude/rules/youtube-compliance.md`)

1. **Title/thumbnail:** 0 từ nhóm 殺/死/自殺/レイプ/虐待 · **0 chữ 血/透析** · không 医師が解説/医師警告. ✅
2. **Persona:** みのり không xưng 医師/管理栄養士/専門家; gate S7 = 0. Khối FAST = hướng dẫn an toàn phổ thông, KHÔNG phải chẩn đoán. ✅
3. **Không tên thật** hãng/sản phẩm/người. Nguồn đích danh duy nhất là cơ quan có thật: 厚生労働省「日本人の食事摂取基準（2025年版）」. Các số còn lại hedge 「〜という報告があります」「〜とされています」 không gắn tên. ✅
4. **YMYL:** 0 lần 治る/完治/薬の代わり/絶対 · cảnh báo tương tác nói **2 lần** (04:35 và 15:18) · disclaimer cuối + nhắc lại 救急車. ✅
5. Thumbnail nhân vật AI hư cấu → không tick synthetic; ảnh AI làm slide TRONG video → **có tick** (`youtube-compliance.md` §2.1).

## 8. SỐ LIỆU — nguồn & mức độ chắc chắn

| số trong bài | nguồn | cách nói trong bài |
|---|---|---|
| 食塩 目標量 男 7,5g未満 / 女 6,5g未満 | 厚労省「日本人の食事摂取基準（2025年版）」 | nêu **đích danh cơ quan + 年版** |
| 高血圧/CKD 重症化予防 6,0g未満 | cùng nguồn | đích danh |
| 汁を半分残す → 1〜2g giảm | quy đổi từ thành phần công bố của mì ăn liền | 「一グラムから、にグラムほど」 |
| モーニングサージ → 脳の血管の事故 にてんななばい | báo cáo lưu hành rộng về morning surge | **「〜という報告があります」, KHÔNG gắn tên tổ chức** |
| 脳梗塞 nhiều nhất 朝8〜12時 / trong 2 giờ sau khi thức | cùng nhóm nguồn | 「〜ともされています」 |
| 睡眠中 mất ~1 cốc nước | không cảm mất nước, kiến thức phổ thông | 「コップ一杯分ほど」 |
| わかめ: 水溶性食物繊維 + カリウム · 昆布 nhiều ヨウ素 | thành phần thực phẩm | 「〜とされています」 + 3 cảnh báo |
| TIA (30 giây tay không cử động được rồi hết) | biểu hiện điển hình của cơn thiếu máu não thoáng qua | kể như **chuyện của một người**, và bắt buộc kèm 「様子を見ないで救急車」 |

⛔ **Đã CỐ Ý không dùng:** con số "tuần mấy lần cá" (không verify được mức khuyến nghị chính thức) · tỉ lệ % giảm nguy cơ đột quỵ của bất kỳ món nào (không nguồn đủ chắc, và nói ra là hứa hiệu quả).

## 9. TAG + HASHTAG + 概要欄

### タグ
```
60代からの食卓,シニアの健康,60代の食事,脳梗塞,脳梗塞 予防,脳梗塞 前兆,動脈硬化,血管,高血圧,減塩,食塩相当量,わかめ,海藻,青魚,さば缶,カップ麺 塩分,早食い,モーニングサージ,朝の血圧,寝る前 水分,ヒートショック,60歳からの健康,70代 健康,シニア 食事,健康長寿,老後の健康,高齢者 食事,寝たきり予防,介護予防,みのり
```

### 概要欄 — 3 DÒNG ĐẦU
```
脳梗塞が起きる朝は、その前の晩に決まっています。血管の内側にできた「かさぶた」がはがれやすいのは、目が覚めてからの二時間。けれど、その二時間は、朝になってからでは、もう変えられません。
この動画では、かさぶたが できる・育つ・はがれる 三つの場面と、寝る前の三分でできる三つのことを、台所の言葉だけでお話しします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた回です。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ
```
脳梗塞が起きる朝は、その前の晩に決まっています。血管の内側にできた「かさぶた」がはがれやすいのは、目が覚めてからの二時間。けれど、その二時間は、朝になってからでは、もう変えられません。
この動画では、かさぶたが できる・育つ・はがれる 三つの場面と、寝る前の三分でできる三つのことを、台所の言葉だけでお話しします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた回です。

血管の内側は、とても薄い一枚の皮です。塩の取りすぎと早食いは、その皮をこすって傷をつけます。傷あとに古くなった脂が入り込むと、こぶのように盛り上がる——これが動脈硬化です。
そして、そのこぶがはがれる力は、朝にそろいます。眠っているあいだ下がっていた血圧が一気に跳ね上がり、体の水はいちばん減っている。だから、備えるのは前の晩なのです。

【この動画でお話しすること】
00:00 その朝、手が動かなかった——和夫さんの三十秒
01:20 ① かさぶたは、こうして「できる」——塩と、食べる速さ
02:38 厚生労働省の食塩の目標量（2025年版）
03:55 早食いも、内側を傷つけています
04:43 ごあいさつと、大切なお願い
05:46 ② かさぶたが「育つ」——古い脂と、色の濃い野菜
07:55 塩と脂が、同じお皿に載る日
08:31 茨城・和夫さんの三十年
09:58 ③ かさぶたが「はがれる」——目が覚めてからの二時間
11:41 この症状が出たら、すぐ救急車を
12:29 夜の寒暖差——お風呂と、夜中のお手洗い
13:05 朝は、前の晩に決まっています
13:36 前の晩の三つ（水・汁・わかめ）
15:21 腎臓・ワーファリン・ヨウ素の注意
16:22 長野・ふみ江さんの半年
17:09 和夫さんの、その後
17:27 今日のまとめ
【出典】
・厚生労働省「日本人の食事摂取基準（2025年版）」策定検討会報告書（食塩相当量の目標量）

※この動画は、公表されている研究や公的な資料をもとにした、健康に関する一般的な情報です。お一人おひとりに合わせた医療のアドバイスではありません。腎臓の治療を受けている方はカリウムに、ワーファリンなど血液を固まりにくくするお薬を飲んでいる方は海藻や納豆に、それぞれ制限がある場合があります。昆布はヨウ素が多いため、甲状腺に不安のある方もご注意ください。食事を変える前に、必ずかかりつけの先生にご相談ください。
※片方の手足に力が入らない、言葉が出にくい、顔の片側が下がる——このような症状が出たときは、たとえ数十秒で治まっても、様子を見ずに、すぐに救急車（119番）を呼んでください。

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニアの健康 #60代の食事 #脳梗塞 #動脈硬化
```

### 📌 固定コメント (pinned comment — bản NGẮN, ghim sau khi công khai)

```
最後まで見てくださって、ありがとうございます。みのりです。

朝の二時間は、朝になってからでは、もう変えられません。備えるのは前の晩。寝る前の三分で、三つだけです。
① 寝る前に、コップ一杯（ひと口でも構いません）
② 夕飯の汁を、半分残す
③ お椀に、わかめをひとつまみ

〔これだけは、覚えて帰ってください〕
片方の手足に力が入らない・言葉が出にくい・顔の片側が下がる。たとえ数十秒で治まっても、様子を見ずに、すぐ救急車（119番）を呼んでください。動画の和夫さんの三十秒が、まさにそれでした。

腎臓の治療を受けている方、血液を固まりにくくするお薬を飲んでいる方、甲状腺が気になる方は、始める前に必ずかかりつけの先生にご確認ください。

今夜から一つだけ始めるなら、水・汁・わかめ、どれになりますか。コメントは全て読ませていただいております。

今夜の食卓が、皆さんの明日の元気につながりますように。
――みのり
```

## 10. HANDOFF

```
python tools\check_coldopen.py 20          # PASS moi duoc di tiep
py tools\build_slides_20.py                # PLAN + prompt FLOW -> user gen anh
py tools\ingest_slides_20.py               # trim vien + va watermark + khung san khau
py ..\remotion-vox\tools\import_pipeline.py
py ..\remotion-vox\tools\build_overlays_20.py
run_full20.cmd                             # chay NEN (render-background.md)
```

✅ 目次 ở §9 đã cập nhật bằng mốc THẬT từ `subs.srt` sau render (2026-08-25) — lệch 0–6 giây so bản ước từ mô hình CPS.
