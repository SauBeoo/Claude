# 15 — 生姜：すりおろす前に、火を通す（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **生姜 × 食べる力（食欲・胃の動き）× たんぱく質・筋肉 × フレイル予防**
- **Bản đọc chuẩn:** `15_shoga-tabekata_TTS.md` (**bản 4**, 6.013 ký · 263 dòng · ước **23′24**) — sửa lời thì sửa file này **và** quét lại `match` trong SLIDES.
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 15` → ✅ **PASS, cold open 88 giây** (L1–L5 · S6 · S7 sạch) · 29 tag · **0 tag giữa câu** · S8 **16** cảnh báo (video 14: 16 · video 13: 18).
- **Phép thử sạch thứ HAI của spec v3** (`CHANNEL_DIAGNOSIS_2026-08-11.md`). Biến đổi so với video 14: **KHUÔN** (14 = countdown 第5位→第1位 · 15 = 四つの入れ方 + nghịch lý sức khoẻ giữa bài + payoff hai-chỗ).

### ✅ ĐÃ RENDER — nghiệm thu 2026-08-13

`06_VIDEO/15_shoga-tabekata/15_shoga-tabekata.mp4` · **237 MB · 23′52** · 1920×1080 h264 + aac

| tiêu chí (`render-background.md` §1.3) | kết quả |
|---|---|
| ① `EXITCODE=0` | ✅ (dòng 313 của `render.log`) |
| ② duration khớp `subs.srt` | ✅ mp4 1432,24s ↔ cue cuối `00:23:52,423` (lệch 0,18s) |
| ③ duyệt ≥4 frame bằng mắt | ✅ **8 frame**, **4 frame cố ý chọn nền SÁNG** (đĩa trắng 0:10 · bàn cạnh cửa sổ 8:40 · tô thuỷ tinh 10:12 · quầy bếp ban ngày 21:12) — phụ đề `outline` chữ trần **không mất chữ** ở chỗ nào |

Kiểm thêm trên frame: badge 「一つめ／三つめ」 đúng góc trên-trái · **CTA overlay hiện đúng ở 12:04** (log: `CTA @ 724.50s`) · **0 ô vàng thiếu ảnh** · ảnh khớp câu phụ đề ở cả 8 frame.

🔴 **HAI PROXY TRƯỢT SÁT — quyết định KHÔNG render lại, có bằng chứng:**

| proxy | gate ước | **thực tế** |
|---|---|---|
| cold open ≤90s | 88s PASS | **93s** (vượt 3s) |
| trả loop ≥75% | 75,0% | **74,7%** (thiếu 0,3 điểm ≈ 4s) |

Lý do không render lại — giống nguyên văn quyết định ở video 14 §0b, và lần này kiểm được bằng `subs.srt`:
**thứ mà trần 90s làm proxy CHO thì đã đạt.** Cửa sổ giây 20–40 của bản đã render chứa đúng thiết kế —
`24,1s` triệu chứng → **`28,3s` 「台所で立ち上がるとき、縁に手をつくようになった方」** → **`33,6s` 「食べる量が減ると、いちばん先に減るのは、筋肉です」** → `39,5s` vết thương sâu thêm.
**Không câu tháo ngòi, không meta, không credential, không mục lục** trong cửa tử. `feedback_bot_render_lai`: chỉ render lại khi video **hỏng thật**.

🔴 **HIỆU CHUẨN LẦN 2 — đã vá `check_coldopen.py`:** đo thật video 15 ra **4,40 ký/giây** (video 14: 4,49) ⇒ hằng số **không cố định giữa các video, ±2%**. Và sai số ấy đã làm gate **báo PASS OAN hai lần liên tiếp, cùng một chiều** (14: 88→94 · 15: 88→93). Với một gate TRẦN thì ước lạc quan là sai hướng ⇒ **hạ CPS về 4,40**. Chạy lại ngay sau khi vá: script 15 ra **90 giây** (sát trần, đúng thực tế 93s hơn hẳn). ⚠️ Đừng "tối ưu" ngược về 4,49 vì nó khớp video 14 — đó đúng là lỗi của hằng số 4,60 (video 05) đã ghi trong file gate.

### Mốc THẬT đo từ `subs.srt` (không phải số ước tính)

| mốc | thời điểm | % | luật đòi |
|---|---|---|---|
| `# ITEM1` | **1:32** | **6,5%** | ≤4′00 ✅ |
| persona みのり | 3:51 | 16,1% | SAU món #1 ✅ |
| checkpoint 「に」 | 4:35 | 19,2% | tách khỏi CTA ✅ |
| 二つめ | 4:47 | 20,1% | — |
| ヨシ子 nhịp 1 | 6:55 | 29,0% | — |
| 三つめ | 8:25 | 35,3% | — |
| khối 原典 | 10:20 | 43,3% | — |
| CTA giữa | **11:59** | **50,3%** | ~50% ✅ |
| 四つめ | 12:37 | 52,9% | — |
| cú lật 「量ではなく、火」 | 13:11 | 55,3% | — |
| ⭐ nghịch lý sức khoẻ | 13:56 | 58,4% | — |
| ヨシ子 nhịp 2 | 16:05 | 67,4% | — |
| checkpoint 「さん」 | 17:41 | 74,1% | — |
| TRẢ LOOP | **17:49** | **74,7%** | ≥75% 🟡 thiếu 0,3 |
| đỉnh bài | 18:52 | 79,1% | — |
| đóng nhân vật | 19:12 | 80,4% | ~83% ✅ |
| recap | 19:25 | 81,4% | — |
| lớp 長生き | 21:39 | 90,7% | — |
| disclaimer | 22:32 | 94,4% | cuối ✅ |

### Mốc ước ban đầu (mô hình `4,49 ký/giây + 0,25 s/dòng` — giữ để so sai số)

| mốc | thời điểm | % | luật đòi |
|---|---|---|---|
| `# ITEM1` | **1′27** | **6,3%** | ≤4′00 ✅ |
| persona みのり | ~3′5x | 16,9% | SAU món #1 ✅ |
| checkpoint 「に」 | 4′31 | 19,5% | tách khỏi CTA ✅ |
| khối 原典 (厚労省 たんぱく質・フレイル) | 10′09 | 43,8% | — |
| CTA giữa (canonical) | **11′46** | **50,7%** | ~50% ✅ |
| cú lật 「量ではなく、火」 | 12′58 | 55,9% | — |
| ⭐ **nghịch lý sức khoẻ** 「食べる力を削っていた」 | 13′41 | 59,0% | — |
| TRẢ LOOP | **17′33** | **75,0%** | ≥75% ✅ |
| đỉnh bài `[間1.2][速0.8][後間1.0]` | 18′30 | 79,0% | — |
| recap → 「明日、もうひと口、食べられること」 | ~18′5x | 81,1% | — |
| lớp 長生き | ~20′5x | 90,3% | — |
| disclaimer | ~21′5x | 94,2% | cuối ✅ |

🔴 **Đã sửa một lỗi im lặng KẾ THỪA từ video 14:** ở 14, tag `[後間1.0]` **đứng một dòng riêng** → theo `humanize-script-voice.md` §2 bẫy thứ hai, `post_pause` **không nằm trong `defaults`** nên **bị bỏ hoàn toàn** ⇒ khoảng im lặng sau câu đỉnh bài của video 14 chưa bao giờ tồn tại. Bài này viết dính liền đầu dòng.

---

## 0. 🔴 BỐN VÒNG SỬA — bản 1, 2, 3 đều bị bỏ

### 0a. Bản 1 → 2: cửa tử (tao tự bắt)

Bản 1 PASS mọi gate máy **và vẫn chỉ đáng 6,5/10**: ① stake 「体を冷やす」 là **phần thưởng** giữa tháng Tám ② giây 30 trả về **phân loại** (「汗を出す側の生姜です」) chứ không phải vết thương — đúng lỗi §2.1 của chẩn đoán ③ hook mở bằng **một cái đĩa** (⚠️ **đúng lỗi đã ghi sổ ở video 14 §0 lỗ 3**) ④ checkpoint + CTA dính liền ở 50% ⑤ mục 2 lệch xương sống ⑥ cú lật bị bảng liều pha loãng.

### 0b. Bản 2 → 3: **BÀI LỆCH RỔ KÊNH** (user bắt)

> user: *"script này có liên quan gì đến chủ đề kênh, Bữa ăn tuổi 60 mà nó có liên quan gì đâu?"* + *"làm sao để sống lâu thì có đâu"*

**Bằng chứng — 原典 lệch rổ:** 7/9 video của kênh trích **日本食品標準成分表** (bảng thành phần **THỰC PHẨM**); bản 2 trích **日本薬局方** (sách **THUỐC**) + 葛根湯 → **zero tiền lệ**, và đó là địa bàn kênh 漢方. ⚠️ **Bảng đo của chính tao đã ghi rổ 生姜 là "hỗn hợp"** (440 v/ngày đến từ 漢方養生指導士ロン毛メガネ) — tao thấy rồi vẫn ghi đè bằng lý lẽ thẩm mỹ. Cộng thêm: payoff 蒸し生姜 mất **2 ngày** trong khi câu kết cố định của kênh hứa 「**今夜の**食卓」.

### 0c. 🔴🔴🔴 Bản 3 → 4: **SỬA QUÁ TAY SANG BÊN KIA — MÓN MẤT VAI CHỦ NGỮ** (user bắt)

> user: *"Cái tao quan tâm là món này ảnh hưởng như nào tới sức khỏe chứ không phải là thêm hương vị cho bàn ăn"*

**Đúng, và lỗi nằm ở chỗ sửa 0b làm quá tay.** Để kéo bài về bàn ăn, tao lấy **muối** làm đòn bẩy sức khoẻ (薄い → 塩を足す → 薬の数). Hệ quả: **chủ ngữ của bài thành MUỐI**, còn gừng tụt xuống làm *công cụ nêm nếm* — tức bài trở thành video **mẹo nấu ăn**, đúng cái user không muốn.

**Kiểm bằng khuôn của chính kênh:** 9 video trước đều là **MÓN × cái nó làm với CƠ THỂ** — 豆腐×たんぱく質・筋肉 · 緑茶×内臓脂肪 · ヨーグルト×血糖 · かぼちゃ×糖質 · 腎臓に良い食べ物. Không video nào lấy một **gia vị khác** làm trục.

| | bản 3 (lệch) | **bản 4** |
|---|---|---|
| Chủ ngữ | **塩** (gừng là công cụ giảm muối) | ⭐ **生姜** — cái nó làm với cơ thể |
| Cơ chế sức khoẻ | ❌ không có của gừng | **食欲＝胃の動き.** Gừng qua lửa đi **cùng nước canh xuống dạ dày** → dạ dày động → ăn được miếng tiếp. Gừng sống chỉ **dừng ở mũi** |
| Stake | 薄い → 塩を足す → 薬が増える | ⭐ **食が細る → たんぱく質が足りない → 筋肉が落ちる → 立つとき縁に手をつく → 出かけなくなる** (mất tự lập) |
| 原典 | 厚労省 食塩目標量 | ⭐ **厚労省「日本人の食事摂取基準」— 65歳以上のたんぱく質の下限を引き上げ、理由は「フレイル予防」**. Kèm bảng bếp: 体重1kg×1g · 魚一切れ≈20g · 卵1個≈6g · 豆腐半丁≈10g |
| Mục 4 | tăng liều = sai hướng (vị) | ⭐ **nghịch lý SỨC KHOẺ**: tăng liều → dạ dày bị kích → **ăn được ÍT hơn** → 「食べる力をつけようとして増やした結果、食べる力を削っていた」 |
| Payoff | 鍋二枚+椀一枚 = **hết nhạt** | 鍋二枚+椀一枚 = **香りが箸を動かし、奥の温かさが胃を動かす** (mùi thơm mở cơn thèm, hơi ấm mở dạ dày) |
| Nhân vật | bình nước tương vơi nhanh | ⭐ **bát cơm còn một nửa** + tay chống mép bếp khi đứng lên + **giảm 2 kg trong một mùa hè** |
| 減塩 | trục chính | ⛔ **bỏ hẳn** — cũng gỡ luôn rủi ro trùng video 13 (味噌汁の塩分) mà tao đã tự cảnh báo ở bản 3 |
| Thumbnail | `塩が増える` | `夏に食が細る` |

⚖️ **Cái mất, biết trước:** trục たんぱく質・筋肉 **trùng lãnh địa video 12 (`12_tofu-tabekata`, 豆腐×たんぱく質・筋肉)**. Phân biệt: **12 nói ĂN GÌ để có đạm** (nguồn đạm) · **15 nói LÀM SAO ĂN NỔI** (khả năng ăn — điều kiện trước cả việc chọn món). Nếu Analytics cho thấy hai video ăn lẫn nhau thì video sau phải rời trục 筋肉.

📌 **Bài học quy trình sau 4 vòng — tất cả đều là lỗi ĐỊNH VỊ, không phải lỗi câu chữ.** Trước khi render, trả lời bằng chữ **năm** câu:
① người xem **MẤT gì** ở giây 30 · ② họ **TỰ LÀM** được gì trong 60 giây đầu · ③ một hàng của bài có đúng cho **MỌI** mục không · ④ **原典 và payoff có nằm trong rổ kênh không** (bàn ăn / tối nay / 成分表-厚労省) · ⑤ ⭐ **MÓN có phải CHỦ NGỮ không, và cơ chế nói là cơ chế trên CƠ THỂ hay chỉ là mẹo nấu?**

---

## 1. Người xem ĐẾN vì gì · Ở LẠI vì gì

**ĐẾN:** thumbnail/title buộc tội **đúng thao tác họ làm VÌ SỨC KHOẺ** — mài gừng lên đậu phụ lạnh, thả vào trà lúa mạch đá, tin rằng đang tự chăm mình — và nói thẳng hậu quả trên cơ thể: 「その生姜は、いま、食欲を落とす側で働いています」.

**Ở LẠI — 7 cái móc, theo thứ tự gặp:**
1. ⭐ **Giây 15–25: ba câu tự chẩn đoán, đều là THÂN THỂ, không phải cảm giác** — 「ごはんが半分、残りませんか」「肉や魚が、重たく感じませんか」「台所で立ち上がるとき、縁に手をつくようになった方」. Câu thứ ba là thứ senior **tự biết ngay** và chưa ai nói cho họ nghe rằng nó liên quan tới bữa ăn.
2. ⭐ **Giây 25–45: mất mát có đường đi, kết thúc ở mất tự lập** — 「食べる量が減ると、いちばん先に減るのは、筋肉です」→「落ちるのが早く、戻すのに時間がかかります」→「足が弱れば、出かけなくなる」.
3. **Lời buộc tội KHÔNG bị tháo suốt bài** (S6 = 0). Bị buộc tội là **入れる場所と順番**, không phải củ gừng — nên câu gỡ friction vẫn giữ nguyên tội.
4. ⭐ **59,0% — nghịch lý khoá cả bài:** 「食べる力をつけようとして増やした結果、食べる力を削っていた。いちばんやってはいけない形が、いちばんまじめな方に起こります」. Người xem chăm chỉ nhất là người bị phạt nặng nhất — đây là chỗ 4 mục khoá vào nhau.
5. **Một hàng leo được:** rắc lúc bưng ra = chỉ tới mũi → lát dày = lửa không xuyên → đồ nguội = làm mát, dạ dày càng ngừng → tăng liều = **kích dạ dày, ăn ít hơn** → **chia gừng làm hai chỗ**. Mục sau nặng hơn mục trước.
6. **Bảy cú làm-được-ngay:** bỏ gừng vào **trước khi hoà miso** (1′28) · vắt tuýp gừng vào bát nóng (2′4x) · cắt mỏng bằng đồng xu (4′4x) · uống thử để thấy hơi ấm xuống tới ngực (5′2x) · chạm cổ chân (8′5x) · **uống một ngụm canh TRƯỚC khi ăn gừng lúc bụng rỗng** (13′3x) · **đọc dòng nguyên liệu số 1 trên gói 生姜湯** (15′2x).
7. **Một người muốn biết kết cục, nợ là VẬT THỂ.** ヨシ子さん treo ở 29,8% bằng 「あるものを三本、見つけます」, vỡ ở 68,4% (ba củ gừng mài dở, hai củ đã gọt vỏ, **không củ nào vào nồi** + **giảm 2 kg**), đóng ở 78,9% bằng 「あら、今日は、ごはんが残らなかったわ」.

---

## 2. Xương sống — một cơ chế trên CƠ THỂ, đúng cho cả bốn mục

**Cơ chế:** vị hăng của gừng ở dạng sống thì **bay lên mũi rồi hết**; qua lửa nó **chuyển thành thứ khác và đi vào nước canh** → theo nước canh **xuống dạ dày trong lúc còn ấm** → dạ dày động → ăn được miếng tiếp theo.
**Câu chốt bài:** 「食欲というのは、気持ちではなく、胃の動きです。」 ⇒ 「生姜は、鼻で嗅ぐものではなく、胃に届けるものでした。」

| mục | phục vụ xương sống thế nào |
|---|---|
| 一つめ 仕上げにのせない | rắc lúc bưng ra = **không qua lửa** ⇒ hương dừng ở mũi, **dạ dày không nhận được gì**. Bỏ vào trước khi hoà miso ⇒ đi cùng nước canh ấm xuống dạ dày |
| 二つめ 厚く切らない + 皮をむかない | ⭐ **hai việc, MỘT lý do: lửa có xuyên vào giữa hay không.** 「生姜は入っているのに、働いていない」. Vỏ: vị hăng nằm ngay dưới vỏ ⇒ gọt = ném đi chỗ làm việc |
| 三つめ 冷たいものにのせない | đồ nguội = không có lửa, mà vị hăng sống còn kéo cơ thể sang hướng **ra mồ hôi → lạnh người → dạ dày càng ngừng → không thấy đói → không ăn được**. Lối ra: **không bỏ món nguội, thêm một bát canh nóng** |
| 四つめ 効かないから増やさない | ⭐ nghịch lý: tăng liều lúc bụng rỗng ⇒ **kích niêm mạc dạ dày ⇒ nặng bụng ⇒ ăn ÍT hơn**. Cùng cơ thể, ngược hướng |
| **payoff 鍋に二枚、椀に一枚** | ⭐ giải đúng nghịch lý của bài (*vậy gừng mài sai hẳn à?*): **hai chỗ, hai việc** — hai lát trong nồi đi xuống dạ dày, một lát dưới đáy bát dựng mùi thơm khi rót canh nóng. 「香りは、箸を動かします。奥の温かさは、胃を動かします」 = **食べる気持ち + 食べる体**, xong trong bữa tối nay |

🔴 **Cố ý KHÔNG đưa vào:** 日本薬局方 · 葛根湯 · ショウキョウ/カンキョウ (rổ 漢方) · **減塩** (bỏ ở bản 4, gỡ rủi ro trùng video 13) · mọi nhánh 食べ合わせ · mọi claim 血流/代謝/デトックス.

⚠️ **Lệch spec có chủ ý (như video 14):** MỤC 10 đòi 2 anecdote; bài này dùng **1 nhân vật 3 nhịp** — mẫu thứ HAI của cùng phép thử (video 14 chưa có curve).

---

## 3. Đường dây bài

| mốc | % | khối |
|---|---|---|
| 0:00–0:10 | 0% | **thao tác làm VÌ SỨC KHOẺ**: 冷たいお豆腐にすりおろし生姜 · 冷やした麦茶にも → 「体にいいから、そうなさっていませんか」 |
| 0:10–0:15 | 0,5% | buộc tội: 「その生姜は、いま、**食欲を落とす側**で働いています」 |
| ⭐ **0:15–0:25** | **1%** | **3 câu tự chẩn đoán trên thân thể** — ごはんが半分残る · 肉や魚が重たい · **立ち上がるとき縁に手をつく** |
| 🔴 **0:25–0:48** | **2%** | 🔴 **CỬA TỬ = MẤT MÁT** 「食べる量が減ると、いちばん先に減るのは、筋肉です」→ 落ちるのは早い、戻すのは遅い → 「足が弱れば、出かけなくなる」 → gỡ friction giữ nguyên tội: 「生姜は、入れる場所と順番を、間違えただけです」 |
| 0:48–1:15 | 4% | cơ chế: 生 = 汗を出して涼しくする側 · 火を通すと **胃の側に届く** → 「大事なのは、すりおろす前に、火を通すかどうかでした」 |
| 1:15–1:27 | 6% | **loop lớn**: 「箸が進むようになる入れ方があります。**今夜の、お味噌汁から**」 |
| **1:27** | **6,3%** | `# ITEM1` → 一つめ 仕上げにのせない · **câu chốt bài 「食欲は、気持ちではなく、胃の動き」** · 70–80 độ · **チューブ生姜** · tự trào |
| ~3′5x | 16,9% | persona みのり (phủ định chuyên môn, KHÔNG credential) |
| 4:31 | 19,5% | checkpoint 「に」 — **tách khỏi CTA** |
| ~4′4x | 20,6% | 二つめ **厚く切らない + 皮をむかない (một lý do: lửa)** · 一円玉 · 「鼻で止まる vs 胸の奥まで下りる」 |
| **6:49** | **29,8%** | 🎭 **nhịp 1** — nấu một suất từ khi tiễn chồng · hè ăn kém · **お茶碗はいつも半分残る** · thịt cá thấy nặng · 娘: 「**立つとき、いつも台所の縁を持つのね**」 → treo bằng VẬT THỂ |
| 8:18 | 36,3% | 三つめ 冷たいものにのせない · **phép thử 足首/おなか** · 冷え → 胃が動かない → お腹が空かない → 食べられない · lối ra: 「冷たいものを減らすのではなく、温かいものを一つ足す」 |
| **10:09** | **43,8%** | **khối 原典** 厚労省 食事摂取基準: **65歳以上のたんぱく質の下限を引き上げ、理由は「フレイル予防」** → 「若い方より少なく、ではなく、若い方より、しっかり」 → bảng bếp (1kg×1g · 魚20g · 卵6g · 豆腐10g) → 成分表: 生姜 = **野菜類** |
| 11:46 | 50,7% | CTA giữa (canonical) — **đứng một mình** |
| 12:27 | 54,4% | 🔴 **四つめ** — con đường 「効かないから増やす」 |
| **12:58** | **55,9%** | 🔴 **CÚ LẬT** 「届く先を変えるのは、量ではなく、火です」 |
| ⭐ **13:41** | **59,0%** | ⭐ **NGHỊCH LÝ SỨC KHOẺ** 「食べる力をつけようとして増やした結果、食べる力を削っていた。いちばんやってはいけない形が、いちばんまじめな方に起こります」 (+ cú làm-ngay: uống ngụm canh trước) → bảng liều |
| ~15′2x | 67,4% | **đọc nguyên liệu số 1** gói 生姜湯 → 「甘いもので、おなかが先にいっぱいになる…おなかは満たされて、たんぱく質は入っていない」 |
| **15:38** | **68,4%** | 🎭 **nhịp 2** — 3 củ gừng mài dở, 2 củ đã gọt, **không củ nào vào nồi**, chỉ nằm trên đĩa lạnh · 「食べられるようになりたくてね。だから、だんだん、増やしていったの」 · **体重が二キロ減っていた** |
| ~16′5x | 73,9% | checkpoint 「さん」 |
| **17:33** | **75,0%** | ⭐ **TRẢ LOOP — 鍋に二枚、椀に一枚**: 香り→箸が動く · 奥の温かさ→胃が動く |
| **18:30** | **79,0%** | **đỉnh bài** `[間1.2][速0.8][後間1.0]火を、通してから。` → 「香りは、あとから。」 |
| ~18′3x | 78,9% | 🎭 **nhịp 3 — đóng bằng cảm xúc** 「あら、今日は、ごはんが残らなかったわ」 → 「やめたのは、量のほうだけです」 |
| ~18′5x | 81,1% | recap 4 mục → 「生姜は、すりおろす前に、火を通す」 → ⭐ **「この四つが向かっている先は、一つです。明日、もうひと口、食べられること」** → micro-commitment 鍋へ二枚とお椀へ一枚 |
| ~19′5x | 85% | **bonus 30 giây** 蒸し生姜 作り置き + ký ức ざる của bà |
| **~20′5x** | **90,3%** | ⭐ **lớp 長生き** 「長生きというのは、年の数のことではないのかもしれません。自分の足で、台所に立てる年数のことではないでしょうか」 → 「その年数を支えているのは、薬ではなく、毎日、口に入った分量です」 → 「食べられているうちに、食べられる形にしておく」 |
| ~21′5x | 94,2% | disclaimer (+ **腎臓の治療中はたんぱく質の指示を守る** + 胃腸/胃のお薬) → câu kết cố định |

**Chất người 6/6:** ① tự trào 「香りが立つほうが、効いている気がしていたのです」 ② thoại + chi tiết vô dụng-về-thông-tin (**濡らしたスポンジ** · 「体にいいものを選んでいるつもりでした」) ③ ký ức giác quan (祖母の台所、鍋の横のざる、日向の匂い) ④ người kể tự làm (夏の素麺に生姜たっぷり → 汗をかいて寒くなった) ⑤ đóng nhân vật bằng cảm xúc ⑥ phá nhịp 「これだけです。」「薄切りを、三枚。」「香りは、あとから。」「三枚は、続きます。三本は、続きません。」「五秒で済みます。」

**Whitelist Mục 8: 11 loại · Blacklist Mục 7: 0 · ませんか riêng lẻ: 3 (L5 ✅) · câu >55 ký: chỉ 1 dòng = câu CTA canonical (verbatim).**
**S8: 16 cảnh báo.** Đã đọc mắt 2 run dài nhất: đều là **khối nghịch lý sức khoẻ** và **hai nhịp nhân vật** — chỗ trả tiền bằng cơ chế và nợ cảm xúc, không phải trang trí ⇒ giữ (MỤC 14 điểm 0c: *đừng nhồi số vô nghĩa cho qua gate*). Đã chèn 1 cú làm-ngay vào run 8-câu để cắt nó.

---

## 4. 原典 (genten) + YMYL

- ⭐ **厚生労働省「日本人の食事摂取基準」** — nêu ĐÍCH DANH: **hạ trần dưới của mục tiêu đạm cho người từ 65 tuổi được NÂNG LÊN, và lý do ghi rõ là phòng フレイル**. Đây là **bằng chứng của chính stake**: 「若い方より少なく、ではなく、若い方より、しっかり」. Bảng bếp kèm theo: 体重1kg×1g/ngày · 魚一切れ≈20g · 卵1個≈6g · 豆腐半丁≈10g → 「食が細くなった夏に、これを満たすのは、なかなか大変です」.
- **文部科学省「日本食品標準成分表」** — 生姜 xếp ở **野菜類**, không phải ô gia vị: 「薬でも、香りづけでもなく、野菜として数えられている食べ物です」. Đúng rổ 7/9 video của kênh.
- Hedge (KHÔNG gắn tên tổ chức): vị hăng sống bay lên mũi / qua lửa chuyển thành thứ khác và tới phía dạ dày · vị hăng tập trung ngay dưới vỏ · vị hăng sống kéo về hướng ra mồ hôi · cơ thể lạnh thì dạ dày chậm · cơ bắp mất nhanh hồi lại chậm (「と言われます」).
- **Cảnh báo điều kiện tại chỗ:** 「空腹のときに、すりおろしを大量に…胃が重くなって、食べられる量が、さらに減ります」 + cú làm-ngay 「生姜より先に、汁をひと口」 + 「胃腸の弱い方、胃のお薬をお飲みの方は、なおさらです」 + 「お薬を飲んでいらっしゃる方は、量を増やす前に、必ず先生にご確認ください」.
- 🔴 **Disclaimer cuối có dòng MỚI, bắt buộc vì bài khuyên tăng đạm:** 「腎臓の治療を受けていらっしゃる方は、たんぱく質の量を医師から指示されている場合があります。その場合は、必ず、先生の指示を守ってください」 — người bệnh thận **không được tự tăng đạm theo video**.
- ⛔ Không 治る/完治/薬の代わり/絶対/死/透析. Nhân vật **không hứa số liệu** — chỉ 「ごはんが残らなかったわ」. Không claim gừng chữa/giảm bệnh gì.
- ⚖️ **Lối ra không cực đoan:** không bắt bỏ gừng mài, không bắt bỏ tuýp gừng, không bắt bỏ món nguội — chỉ đổi **chỗ** và **thứ tự**.

## 5. Nhân vật (mới hoàn toàn, không lặp video khác)

| | tuổi | tỉnh | nghề cũ | chi tiết đời sống | vai |
|---|---|---|---|---|---|
| 岩下ヨシ子 | 79 | 鳥取県 | 郵便局の窓口 | **切手を貼るときだけは、指を舐めずに濡らしたスポンジ** | 3 nhịp: gieo 29,8% · vỡ 68,4% · đóng 78,9% |

Cung truyện **trùng khít xương sống**: nấu một suất → hè ăn kém → đặt gừng lên đậu phụ lạnh (mục 3 sai) + rắc lúc bưng ra (mục 1 sai) + gọt vỏ (mục 2 sai) + tăng liều (mục 4 sai) → bát cơm còn nửa → **tay chống mép bếp khi đứng lên** → giảm 2 kg. Ba củ gừng mài dở **trên đĩa lạnh, không củ nào vào nồi** là toàn bộ bài nói bằng một cảnh. Kiểm chống lặp: video 14 dùng 片桐スミ子 (76・山形県・和裁).

---

## 6. Đo cầu keyword (2026-08-13, `tools/measure_kw_youtube.py`, 30 ngày, JP/ja, ≥8′)

| keyword | n | med v/ngày | rổ |
|---|---|---|---|
| **生姜 食べ方** ⭐ chọn | 10 | **48** | 🟡 **hỗn hợp** — 高齢者健康の真実 497 · **漢方養生指導士 440** · あやシェフ (recipe) 390 |
| シナモン 食べ方 | 16 | 41 | ✅ rổ senior sạch nhất — **nhưng 3/3 hit đều là góc 食べ合わせ** → để dành |
| 酢 食べ方 | 12 | 33 | 🟡 max 32.226 là kênh CÔNG THỨC |
| 大根 食べ方 | 6 | 15 | ✅ đúng rổ, cầu thấp |
| 生姜 冷え | 3 | 95 | n quá nhỏ → không làm keyword dẫn |
| ~~蒸し生姜~~ / ~~生姜 温める~~ / ~~乾姜~~ | 1 · 1 · 2 | 70 · 95 · 5 | ⛔ **n ≤ 2 = YouTube không coi là truy vấn sống** |
| ~~きのこ~~ / ~~サバ缶~~ / ~~さつまいも~~ | 3 · 12 · 5 | 10.281 · 40 · **1** | ⛔ 2 cái đầu rổ アレンジレシピ · さつまいも cầu tắt |

🔴 **Cảnh báo "rổ hỗn hợp" là thứ tao đã ghi đè ở bản 2** (§0b). Bản 4 xử lý bằng cách **kéo cả 原典 lẫn cơ chế về rổ sức khoẻ-bàn ăn** (厚労省 フレイル · 成分表), không đổi món.
⚠️ **Thật thà:** med 48 **thấp hơn nhiều** so với かぼちゃ 136 của video 14 — cầu vừa phải.
⚠️ Bảng đo 08-11 lệch sau **2 ngày** → luôn đo lại trong lượt viết.

---

## 7. Title — 3 bản A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代は要注意】生姜の正しい食べ方4選｜夏に食が細る本当の理由` | 33 | 生姜@9 | keyword cao nhất + hook = hậu quả trên cơ thể |
| **A2** | `その生姜が食欲を落としています｜60代の正しい食べ方4選` | 28 | 生姜@2 | đổi keyword dẫn sang 食欲 (hậu quả), bỏ 【】 |
| **A3** | `【知らないと損】生姜は増やすほど食べられなくなる｜60代の食べ方4選` | 36 | 生姜@8 | đổi kiểu hook: cảnh báo → nghịch lý (đòn 59,0%) |

#### Title CHỐT
```
【60代は要注意】生姜の正しい食べ方4選｜夏に食が細る本当の理由
```

#### Tên file upload
```
shoga-tabekata-60dai.mp4
```

### 概要欄 — 3 DÒNG ĐẦU

```
冷たいお豆腐に、すりおろした生姜。体にいいからと、そうなさっていませんか。その生姜は、いま、食欲を落とす側で働いているかもしれません。生の辛味は汗を出して体を涼しくする方に働き、体が冷えると胃の動きも落ちます。
この動画では、60代からの食卓で見直したい生姜の食べ方を4つ。仕上げにのせない、厚く切らない、冷たいものにのせない、そして「効かないから増やす」をやめる、という順にお話しします。
食べる量が減ると、いちばん先に減るのは筋肉です。生姜は、鼻で嗅ぐものではなく、胃に届けるもの。箸が進むようになる入れ方は、今夜のお味噌汁から試せます。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ

> 🔴 **目次 CHƯA ĐIỀN — phải trích timestamp từ `subs.srt` SAU khi render** (`upload_pack.py` gate sẽ hét nếu thiếu mốc `00:00`). ⛔ Không bịa từ số ước tính ở §3.

```
冷たいお豆腐に、すりおろした生姜。体にいいからと、そうなさっていませんか。その生姜は、いま、食欲を落とす側で働いているかもしれません。生の辛味は汗を出して体を涼しくする方に働き、体が冷えると胃の動きも落ちます。
この動画では、60代からの食卓で見直したい生姜の食べ方を4つ。仕上げにのせない、厚く切らない、冷たいものにのせない、そして「効かないから増やす」をやめる、という順にお話しします。
食べる量が減ると、いちばん先に減るのは筋肉です。生姜は、鼻で嗅ぐものではなく、胃に届けるもの。箸が進むようになる入れ方は、今夜のお味噌汁から試せます。

【目次】
00:00 オープニング｜その生姜、食欲を落としていませんか
01:32 ① すりおろしを仕上げにのせない
04:47 ② 厚く切らない・皮をむかない
06:55 食が細くなった、ある方のお話
08:25 ③ 冷たいものの上にのせない
10:20 65歳からのたんぱく質とフレイル（出典つき）
12:37 ④ 効かないからと量を増やさない
15:18 生姜湯の粉、袋の裏の一番目
17:49 鍋に二枚、お椀に一枚
19:25 まとめ｜すりおろす前に、火を通す
20:34 冬の作り置き｜蒸し生姜

生姜の辛味は、生のままだと鼻のほうに立ちのぼって、そこで終わります。ところが火を通すと、辛味は別のものに変わって、汁の側に移るとされています。その汁が温かいまま胃に入ると、冷えて動きの悪くなった胃が動きはじめ、次の一口が入るようになります。食欲というのは気持ちの問題ではなく、胃の動きです。仕上げにすりおろしてのせたお椀は、香りはしても、胃のほうにはほとんど何も届いていません。

夏に食が細くなるのを「年のせい」で終わらせないでいただきたいのです。食べる量が減ると、いちばん先に減るのは筋肉です。筋肉は落ちるのが早く、戻すのに時間がかかります。足が弱れば出かけなくなり、出かけなくなれば、また食が細くなります。厚生労働省の「日本人の食事摂取基準」では、65歳以上の方について、たんぱく質の目標の下限が引き上げられました。理由もはっきり書かれています。フレイル、つまり体が弱っていくのを防ぐため、です。若い方より少なく、ではなく、若い方より、しっかり、なのです。

台所の目安にすると、体重1キロあたり1グラム以上。体重50キロの方なら1日50グラム。お魚一切れでおよそ20グラム、卵1個でおよそ6グラム、お豆腐半丁でおよそ10グラム。並べてみると、食が細くなった夏にこれを満たすのは、なかなか大変です。だからこそ、食べる力が落ちること自体が、60代からのいちばんの心配ごとになります。なお、文部科学省の「日本食品標準成分表」では、生姜は薬味の欄ではなく、野菜類に入っています。薬でも香りづけでもなく、野菜として数えられている食べ物です。

動画では、味噌を溶かす前に入れること、厚さは一円玉ほどにすること（厚いままだと外側だけ火が通って真ん中は生のまま沈んでいます）、皮のすぐ下に辛味が多いのでたわしで洗って皮ごと使うこと、冷たいお豆腐や冷やしたお素麺の上ではなく温かいものの中へ入れること、そして「効かないから増やす」が逆効果になる理由を、順にお話しします。空腹時にすりおろしを大量に、を続けると胃が重くなって、食べられる量がさらに減ります。食べる力をつけようとして増やした結果、食べる力を削っていた、という形です。

最後にお伝えするのは、箸が進むようになる入れ方です。薄切りを3枚。2枚はお出汁と一緒に鍋へ、残りの1枚はお椀の底に先に置いて、そこへ熱い汁を注ぐ。鍋の2枚は汁と一緒に胃の奥まで下りていき、椀の1枚は注いだ瞬間に香りを立てます。香りは箸を動かし、奥の温かさは胃を動かす。食べる気持ちと食べる体、その両方に一度に届きます。冬の作り置きとして、薄切りを30分ほど蒸して日向に一日干す蒸し生姜の作り方も添えています。

生姜の辛味は胃の粘膜を刺激するものでもあります。空腹時にすりおろしを大量に、という食べ方は避けてください。胃腸の弱い方、胃のお薬をお飲みの方、その他お薬を飲んでいらっしゃる方は、量を増やす前に必ずかかりつけの先生にご確認ください。腎臓の治療を受けていらっしゃる方は、たんぱく質の量を医師から指示されている場合があります。その場合は必ず先生の指示を守ってください。

※この動画でお伝えする内容は、公表されている公的資料をもとにした、健康に関する一般的な情報です。個別の医療アドバイスではありません。持病のある方やお薬を飲んでいる方は、食事を変える前に必ずかかりつけの医師にご相談ください。

【出典】
厚生労働省「日本人の食事摂取基準」
文部科学省「日本食品標準成分表」

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニア健康 #健康長寿 #生姜 #フレイル予防
```

### タグ

> 16 tag nhận diện kênh **cố định đứng đầu** (giống 14 video trước) → tag riêng video. Tổng **40**.
> ⛔ Đã bỏ sạch `日本薬局方` · `生薬` · `漢方` · `葛根湯` · `乾姜` (rổ kênh 漢方, §0b) và `減塩` · `塩分` · `食塩` (trục của bản 3, §0c — cũng gỡ trùng video 13).
> ⛔ **Cố ý KHÔNG có tag chỉ số** (血圧/血糖): `chỉ số × ◯選` là luồng đã chết (median 7 v/ngày), và tag quyết định YouTube xếp video vào RỔ nào để test (bài học 07-21: video 腎臓 đặt cạnh rổ アルデヒド → bỏ sau **10 giây**).

```
60代からの食卓, 60代 食事, 60代 食べてはいけない, 食べてはいけない, シニア 健康, シニアライフ, シニア 食事, 高齢者 食事, 高齢者 栄養, 健康長寿, 健康寿命, 食生活 改善, 生活習慣病 予防, 60代 健康, 70代 健康, 老後 健康, 生姜, 生姜 食べ方, しょうが, ショウガ, すりおろし生姜, チューブ生姜, 生姜 皮, 生姜 薄切り, 生姜 保存, 蒸し生姜, 干し生姜, 食欲不振, 食欲がない, 夏バテ, 夏の冷え, 胃の調子, たんぱく質, 高齢者 たんぱく質, 筋肉 落ちる, フレイル, フレイル予防, 食事摂取基準, 味噌汁 具材, 食品成分表
```

⚠️ **Compliance (`youtube-compliance.md`)** — đã tự quét, 5 điểm:
1. **Từ tắt-ad ở title/thumbnail:** sạch. Không 殺/死/自殺/虐待, **không chữ 血** ở bất kỳ đâu trong bài, không 透析.
2. **Persona:** không 医師/先生/管理栄養士/専門家; script **phủ định thẳng** 「私は、お医者様でも、栄養の専門家でもありません」. Không 医師が解説/医師警告.
3. **Tên thật:** không hãng/sản phẩm/người. 「市販の生姜湯の粉」 để generic. 厚労省/文科省 là cơ quan công.
4. **概要欄 đủ:** 医療免責 ✅ · credit giọng `VOICEVOX:青山龍星` ✅ · 出典 ✅ · **thêm dòng chỉ định đạm cho người bệnh thận** ✅.
5. **Tình tiết title/thumbnail có thật trong video:** 「夏に食が細る本当の理由」 = khối 0:00–0:48 + mục 3 · 「4選」 = đúng 4 mục · 「増やすほど食べられなくなる」 (A3) = đòn 59,0% ✅.

### 📌 固定コメント (pinned comment — ghim sau khi công khai)

```
最後まで見てくださって、ありがとうございます。案内人のみのりです。

今日は、生姜の「入れる場所と順番」を四つ、お届けしました。仕上げにのせない、厚く切らない・皮をむかない、冷たいものにのせない、そして、効かないからと増やさない。四つが向かっている先は、一つです。明日、もうひと口、食べられること。

今夜からできるのは、薄切りを三枚。二枚はお出汁と一緒に鍋へ、残りの一枚はお椀の底に置いて、そこへ熱い汁を注ぐ。それだけです。

よろしければ、二つ教えてください。
① 四つのうち、「あ、これ、うちでやっていた」と思われたのは、どれでしたか。
② 次に取り上げてほしい食べ物があれば、ぜひ。
コメントは全て読ませていただいております。皆さんの一言が、次の回の何よりの励みになります。

〔ひとつだけ、大切なお願い〕
今日のお話は、公表されている公的資料をもとにした、一般的な健康情報で、医療のアドバイスではありません。空腹のときに、すりおろしを大量に、という食べ方は避けてくださいね。胃腸の弱い方、胃のお薬をお飲みの方、その他お薬を飲んでいらっしゃる方は、量を増やす前に、必ずかかりつけの先生にご確認ください。腎臓の治療を受けていらっしゃる方は、たんぱく質の量を医師から指示されている場合があります。その場合は、必ず、先生の指示を守ってください。

今夜の食卓が、皆さんの明日の元気につながりますように。どうか、ご自分の体を大切に。
――みのり
```

---

## 8. TEXT THUMBNAIL (v5 WARNING-FIRST) — dùng CHUNG cho cả T1/T2/T3

> 🔴 Luật `ab-3title-3thumb.md` §3 mục 6: **chữ GIỐNG NHAU ở cả 3 bản**, biến thử là **HÌNH**.

| dòng | chữ | ký | vai | màu |
|---|---|---|---|---|
| 1 | `生姜は後入れ` | 6 | HÀNH VI (① về cái gì) | trắng |
| 2 | `夏に食が細る` | 6 | HẬU QUẢ — **to nhất** (② chuyện gì xảy ra) | **đỏ** |
| 3 | `入れ方4つ` | 5 | ĐÁP ÁN GIẤU (③ phải làm gì) | vàng |

- **Gate 7 (`audience-45plus.md` §1):** che ảnh đi vẫn trả lời được 3 câu ✅. Từ dẫn `生姜` là keyword đứng đầu rổ đo ở §6 ✅.
- 🔴 **Đã đổi 3 lần, ghi cả ba lý do** (mỗi lần là một lỗi định vị khác nhau):
  ① `その生姜 / 体を冷やす / 4つの直し方` — 「体を冷やす」 giữa tháng 8 **đọc lên nghe như một lợi ích**.
  ② `生姜なのに / 足が冷える / 直し方4つ` — đúng vết thương nhưng **vẫn thuộc rổ 冷え/漢方**.
  ③ `生姜は後入れ / 塩が増える / 入れ方4つ` — bàn ăn, nhưng **hậu quả là của MUỐI, không phải của gừng** (§0c).
  ④ Bản dùng: hậu quả **trên cơ thể do chính gừng gây ra** (食が細る), khớp title A1 và khớp stake.
- Vật hero: **お椀の底の薄切り生姜 + 半分残ったごはん茶碗** đặt cạnh (bát cơm còn nửa là bằng chứng của bài). Vật đáp án để mosaic: **お椀の底の一枚**.
- Layout: cột chữ **bên TRÁI**, ảnh bên phải. ⚠️ Đảo so với video liền trước — video 14 chưa render thumbnail (treo ở §8b của nó), khi làm thì chốt 14 = cột PHẢI.
- Badge góc **dưới-TRÁI** (góc dưới-phải là của timestamp YouTube — [[feedback_thumbnail_goc_duoi_phai_cua_youtube]]).

---

## 9. LỚP HÌNH — 80 slide, 100% ảnh AI do USER gen

`04_SCRIPTS/15_shoga-tabekata_SLIDES_photo.json` — **80 entry, `photo: true`, `q: "AI-GEN"`**.
⛔ **KHÔNG chạy `fetch_photo.py` cho video này** — `q` là nhãn đánh dấu, không phải query.
Dựng lại bằng: `python toolsuild_slides_15.py` (sửa PLAN trong file đó, đừng sửa JSON tay).

| | |
|---|---|
| Nhịp | **17,6 giây/ảnh · 3,42 lần đổi hình/phút** — trong luật `audience-45plus.md` §2 (≤6/phút) · **0 entry <6 giây** (gate của tool chặn cứng, đã bắt 5 chỗ vi phạm lúc dựng) |
| `rank` | 一つめ 8 · 二つめ 8 · 三つめ 7 · 四つめ 8 · **49 entry ngoài mục** (cold open · persona · ヨシ子 · 原典 · 生姜湯 · loop · recap · bonus · kết) |
| Verify máy | 80/80 `match` là substring **có thật và DUY NHẤT** trong `_TTS.md` · 0 trùng · đúng thứ tự tăng dần |
| ⭐ Entry 0 | 「冷たいお豆腐に、すりおろした生姜」 → gừng mài trên đậu phụ lạnh = **đúng thao tác bị buộc tội, ngay giây 0** (`media-library.md` §2.0) |

**Ba file prompt** (`06_VIDEO/15_shoga-tabekata/`, theo [[feedback_luu_prompt_vao_file]]):

| file | vai |
|---|---|
| `slide_prompts_FLOW.txt` | **80 prompt, mỗi prompt 1 DÒNG** — bơm thẳng vào extension |
| `slide_prompts_TENFILE.txt` | `slide_XX.jpg` ↔ mốc giây ↔ rank ↔ câu cue |
| `slide_prompts_BLOCKS.md` | bản người đọc: khối STYLE + từng slot |

**Đồng nhất 80 ảnh:** mọi prompt kết bằng **cùng một khối STYLE nguyên văn** (`photorealistic documentary photography, Japanese home kitchen, warm natural window light from the left … muted deep navy and warm amber accents`) — khớp bảng màu nhận diện kênh. Nhân vật **ヨシ子 dùng CÙNG MỘT câu tả ở cả 5 slot** (portrait · bát cơm còn nửa · chống mép bếp · con gái đặt tay lên vai · nếm thử) để nhận ra là một người.

**Đặt tên khi gen xong:** `slide_00.jpg` … `slide_79.jpg` → bỏ vào `06_VIDEO/15_shoga-tabekata/slides_img_photo/` (folder đã tạo sẵn). Renderer đọc theo **index 0-based đúng thứ tự entry** — sai thứ tự là sai hình cả bài.

### Ba việc bắt buộc khi dùng ảnh AI

1. 🔴 **Quét sạch watermark ✦ trước khi dùng** ([[feedback_anh_ai_quet_sach_watermark]]) — dấu ✦ **không cố định một chỗ**, phải **đo lại vị trí theo đúng lô ảnh** rồi crop/vá, ⛔ đừng `cv2.inpaint`, ⛔ đừng bê mốc crop của lô trước.
2. 🔴 **Mọi prompt đã có `no text, no letters, no numbers`** — chữ Nhật gen ra hay nát nét (`media-library.md` §2.9). Ảnh nào lỡ có chữ → **loại, gen lại**. 6 slot cố ý tả "giấy tờ/nhãn trống, chữ mờ không đọc được" (sách 食事摂取基準 · cân bếp · gói 生姜湯 · cân sức khoẻ) để không phải gen kanji.
3. 🔴 **PHẢI TICK "altered/synthetic content" khi upload** (`youtube-compliance.md` §2.1) — `upload_pack.py`/`upload_api.py` **chưa có cờ này → tick TAY trong Studio**.

### Việc còn lại trước render

1. **Gen 80 ảnh** từ `slide_prompts_FLOW.txt` → đặt tên đúng → **duyệt contact sheet bằng mắt** (`tools/contact_sheet.py`, `media-library.md` §2.1: soi bộ ĐƯỢC CHỌN).
2. **Đủ ảnh mới render** (`render-background.md` §1.5) — thiếu 1 ảnh cũng không render.
3. **Bộ A/B 3×3 thumbnail** (§8) — 3 prompt bake chữ + 3 plate không chữ ở **file RIÊNG** (⛔ đừng trộn PLATE vào FLOW).
4. **Render chạy NỀN** `--channel shokutaku --slides 04_SCRIPTS_shoga-tabekata_SLIDES_photo.json --img-dir 06_VIDEO_shoga-tabekata\slides_img_photo`. ⚠️ `.cmd` **ASCII-only** · redirect `>>` **có dấu cách** · **không gọi trần `timeout`/`find`/`sort`** · **tín hiệu chờ phải tự reset** (`render-background.md` §2.6 ①③④⑤).
5. Điền **目次** từ `subs.srt` → `upload_pack.py 15 --channel shokutaku`.

## 10. Đọc kết quả (sau ≥7 ngày)

```bash
cd E:\Claude\Projects\youtube-jp-chouhen\tools
python analytics_report.py --channel shokutaku --video <videoId>
```

Nhìn **@40s** (mục tiêu ≥85%; nay 30–50%) và **sàn thân bài** (≥55%; nay 9–21%). ⛔ Không đọc bằng view (`BROWSE = 0`). Mốc chặng AVD% **30 → 40 → 50 → 60**; 🛑 phanh ở **3 video liên tiếp ≤25%**.

🔬 **Ba phép thử riêng của bài này:**
1. **Ba câu tự chẩn đoán trên thân thể ở giây 15–25** (đặc biệt 「立ち上がるとき縁に手をつく」) — nếu curve giữ qua đó thì "triệu chứng vận động" mạnh hơn "triệu chứng cảm giác" cho tệp này.
2. **Nghịch lý sức khoẻ ở 59,0%** — nếu curve **không rớt** thì đặt đòn mạnh nhất quanh 55–60% là đúng; nếu rớt thì nó đang **giải phóng** người xem → lần sau dời về sau 70%.
3. **Trục たんぱく質・筋肉** — nếu video này ăn view mà video 12 (豆腐) tụt, thì hai video đang cạnh tranh và video sau phải rời trục 筋肉 (§0c).

⚠️ Kênh vẫn `BROWSE = 0`, và mốc **8 video qua gate mà BROWSE vẫn 0 → dừng, mở kênh mới (~2026-08-25)** KHÔNG bị hoãn. Video 15 là video thứ **6** trong đợt đếm (08-02 キャベツ · 08-03 麦茶 · 08-05 ヨーグルト · 08-07 豆腐 · 14 かぼちゃ · **15 生姜**).
