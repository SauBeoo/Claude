# 05_SCRIPT_FORMULA — MỔ XẺ 3 KỊCH BẢN 100K+ → BỘ KHUÔN VIẾT SCRIPT (showa)

> Nguồn: `03_SCRIPTS/kichban1.md` · `kichban2.md` · `kichban3.md` — transcript **auto-caption** của 3 video >100K view trong ngách 昭和.
> Mọi con số dưới đây **đo bằng máy** (phân đoạn theo anchor + regex), không phải cảm giác. Đo ngày **2026-09-07**.
> Đối chiếu với: `CHANNEL_BENCHMARK_anokoro-showa_2026-08-29.md` (42 long-form cùng ngách) · `CHANNEL_DIAGNOSIS_2026-09-03.md` (retention của mình) · 2 script mình gần nhất (`10_tsugakuro_TTS.md`, `11_kyuryobukuro_TTS.md`).

## 0. KẾT LUẬN 1 DÒNG

Ba bản thắng **không** hơn mình ở câu văn, ở nguồn, hay ở chất người — mình hơn ở mấy khoản đó.
Chúng hơn ở **4 thứ đo được**: ① **đơn vị đề tài là ĐIỀU ĐƯƠNG NHIÊN (常識・風習), không phải VẬT** ② **mốc năm dày gấp 2–3 lần** (1/292–478 ký — và đó là "con số" duy nhất chúng dùng, không phải giá) ③ **mật độ ngũ quan dày gấp 5–7 lần** ở bản kể-cảnh ④ **mọi mục đóng bằng một câu mềm 「〜かもしれません」** — mình có **0 câu loại này trong cả 2 script gần nhất**.

Và một thứ nữa: chúng **dài hơn 46–70%** (5.776–6.724 ký so với 3.959–3.989 của mình).

⭐ **Phát hiện đắt nhất của lượt đo: có HAI động cơ, và chúng ĐÁNH ĐỔI nhau chứ không cộng dồn.**
**E-LIST** (K1) = mốc năm + luật + cơ chế, ngũ quan gần bằng 0 · **E-SCENE** (K3) = ngũ quan đặc, **0 câu 「なぜ」**, gần như không nhắc luật · K2 dùng cả hai. ⇒ Một bài chỉ cần đạt **một** trong hai. Gate máy phiên bản đầu đòi cả hai và **đánh trượt 3/3 bản thắng** — chi tiết ở §5.2.

### 0.1 Bảng số đo (mật độ = số ký / 1 lần xuất hiện · nhỏ = dày)

| | K1 常識20選 | K2 風習5つ | K3 母の料理5つ | MÌNH 10 通学路 | MÌNH 11 給料日 |
|---|---|---|---|---|---|
| Số ký (bỏ `[音楽]` + khoảng trắng) | **5.776** | **6.724** | **6.705** | 3.989 | 3.959 |
| Số mục | 20 | 5 | 5 | 20 điểm/8 khối | 20 điểm/10 khối |
| Mốc năm (昭和◯年/西暦) | 17 → **1/339** | 23 → **1/292** | 14 → **1/478** | 4 → 1/997 | 8 → 1/494 |
| Kim tiền (◯円) | **0** | 1 | 1 | 1 | 12 → 1/329 |
| Luật/chế độ (法・条・基準・禁止) | 19 → **1/304** | 7 | 2 | **0** | 5 |
| Đối chiếu nay–xưa (今では…) | 10 → 1/577 | 17 → **1/395** | 5 | 4 | 2 → 1/1.979 |
| Ngũ quan / tượng thanh | 2 (1/2.888) | 23 → **1/292** | 31 → **1/216** | 2 → 1/1.994 | 3 → 1/1.319 |
| ⤷ *cùng chỉ số, bộ từ ĐÃ NỚI của gate* | 6 (1/962) | 36 → **1/186** | 50 → **1/134** | 7 → 1/569 | 3 → 1/1.319 |
| Người kể (私・知人) | 5 → 1/1.155 | **0** | **0** | 3 | 0 |
| Đóng mềm (かもしれません・気がします) | 9 → 1/641 | 8 → 1/840 | 11 → **1/609** | **0** | **0** |
| Lời thuật lại (と言われ・と声をかけ) | 8 | 4 | 4 | 6 | 3 |
| Nhịp nghỉ — trung vị đoạn giữa 2 lần nghỉ | 19 ký | 30 ký | 34 ký | 17 ký | 19 ký |

📌 **Hai cột "MÌNH" là ảnh chụp lúc đo (2026-09-07 sáng), giữ nguyên làm mốc so — KHÔNG cập nhật.**
Sau lượt đo này: **video 11 đã viết lại** theo khuôn (4.871 ký · mốc năm 1/436 · **7 câu đóng mềm** · động cơ LIST — `03_SCRIPTS/11_kyuryobukuro.md` §7); **video 10 giữ nguyên** làm mẫu đối chứng của luật cũ (user chốt).

### 0.2 ⚠️ BỐN THỨ TRANSCRIPT NÀY **KHÔNG** ĐO ĐƯỢC — đừng kết luận từ chúng

1. 🔴 **Lời thoại `「」`: cả 3 file = 0 dấu ngoặc.** Đây là **artifact của ASR** (máy nhận dạng giọng không xuất dấu ngoặc), **không** phải bằng chứng họ không viết thoại — trong lời vẫn có `お前が悪い`, `まるまるさん電話だよ`, `お疲れさん`. Bản đầu của phép đo này kết luận sai *"3 bản thắng có 0 thoại"* rồi định khuyên bỏ thoại; **đếm lại bằng lời-thuật-lại thì mật độ của mình NGANG họ** (1/660–1.320 so với 1/720–1.680). ⇒ **Giữ thoại.** Cùng họ bẫy `feedback_do_pixel_cua_so_quet`: cửa sổ quét không khớp vật.
2. **Dấu câu của tác giả** — `。` do ASR chèn theo khoảng nghỉ. Nên hàng "nhịp nghỉ" ở trên đọc được (nó là nhịp NÓI thật), nhưng đừng đọc thành "họ viết câu dài 34 ký".
3. **Tag nhấn nhá / khoảng lặng có chủ ý** — không có trong transcript. Benchmark 08-29 đã đo trực tiếp video cùng ngách: **0 khoảng nghỉ ≥1,5s trong 15 phút**. Tức tệp này KHÔNG bỏ đi vì thiếu 間 — đây là chỗ mình hơn thật, giữ nguyên.
4. **Lỗi chính tả trong 3 file là của ASR** (衛生→衛星, 境界線→教会戦, 六甲→六光, 竜田揚げ→タ揚げ). Đừng chép chữ, chỉ chép cấu trúc.

---

## 1. TÁCH CẤU TRÚC & THỜI LƯỢNG (BEAT SHEET)

### 1.1 K1 — 常識20選 (5.776 ký ≈ 15′ ở tốc độ của họ)

| mốc | % bài | dài | beat |
|---|---|---|---|
| 0:00–0:23 | 0–2,6% | 149 ký | **COLD OPEN — 3 cú sốc liên tiếp, không lời chào**: 「水を飲むとバてる…川の水を飲む」→ **「これ実話です」** → **「65の私の父の話です」** → 赤チン・ノーヘル・飲酒運転 → **「これが昭和です。猛烈な時代です」** |
| 0:23–0:29 | 2,6% | 39 ký | Lời chào + tên người dẫn (**đặt SAU cú sốc**) |
| 0:29–0:52 | 3,3% | 141 ký | **PROMISE**: 20選 + 「なぜ普通だったのか、そんなことも考えながら」 = hứa *cơ chế*, không chỉ hứa *danh mục* |
| 0:55 | 5,9% | — | **VÀO MỤC 1** (≈55 giây) |
| 5,9–85,2% | — | 20 mục | thân bài, **độ dài mục KHÔNG ĐỀU** (§1.4) |
| 89,8–96,4% | 380 ký | 58s | **TỔNG LUẬN — 認める→裏返す**: 「正直に言えば変わって良かったこともある」(nhận) → 「でも昭和を生きた人たちは強かった」(lật) → 3 lý do → 「令和にどれだけ願っても、多分もう届きません」 |
| 96,4–100% | 208 ký | 32s | CTA comment (体験談・思い出話) → outro kênh |

### 1.2 K2 + K3 — 5 mục × ~3 phút (6.7K ký ≈ 17–19′)

| | K2 風習 | K3 料理 |
|---|---|---|
| INTRO | 0–2,5% (169 ký ≈ 26s) | 0–3,3% (222 ký ≈ 34s) |
| PROMISE | 2,5–3,5% | 3,3–4,0% |
| **VÀO MỤC 1** | **3,5% ≈ 36s** | **4,0% ≈ 42s** |
| mục 1..5 | 1.032 · 1.150 · 1.370 · 1.478 · 1.197 ký (**2,6–3,8 phút**) | 1.325 · 1.157 · 1.164 · 1.078 · 1.181 ký (**2,8–3,4 phút**) |
| KẾT | 96,1% (260 ký) | 92,1% (529 ký) |
| ⚠️ | **không recap**, không đếm điểm, không cliffhanger | như trên |

**Ba mốc thẳng hàng ở cả 3 bản: vào mục đầu tiên ở giây 36–55.** Gate 「≤60s」 của kênh mình đúng — nhưng bản 5-mục vào ở **36–42s**, sớm hơn mình.

### 1.3 CẤU TRÚC BÊN TRONG MỘT MỤC — đo vị trí thiết bị (% chiều dài mục)

**K2 — khuôn 5 ô, 5/5 mục dùng y hệt:**

| ô | vị trí đo được | nội dung |
|---|---|---|
| ① TUYÊN BỐ | 0–8% | `<tên mục>。昭和30年から40年頃、今では<信じられない/考えられない>ことですが、<mệnh đề>でした。` — **5/5 mục nhắc lại mốc thời đại + 5/5 có cụm 今では** |
| ② THỰC CẢNH | 8–55% | 3–4 cảnh cụ thể, **leo thang phạm vi**: 満員電車 → バス → 映画館 → **病院の待合室** → 新幹線. Chốt bằng 「そして驚くべきはその範囲の広さです」. Ngũ quan cụm ở 15–20% và 44–56% |
| ③ CHỐT LẬT「では、なぜ」 | **42–57%** (4/5 mục) | 「ではなぜこんな光景が成立していたのか。最大の理由は〜」 — **đúng giữa mục** |
| ④ CƠ CHẾ + MỐC CHẾT | **54–87%** | chế độ/hạ tầng + **cụm mốc năm dồn ở nửa SAU**: 専売制 → ハイライト 1960 → 新幹線 昭和39 → 公衆衛生局長報告 1964 |
| ⑤ HẠ CÁNH | 88–100% | 「今の安心は大切です。ですが〜は少しずつ失われていきました」+ **「〜だったのかもしれません」(5/5 mục)** |

**K3 — khuôn 5 ô, thay ô ③ bằng "thực địa nhà bếp":**

| ô | vị trí | nội dung |
|---|---|---|
| ① TUYÊN BỐ | 0–6% | `<tên món>。昭和35年から40年頃の食卓で<よく見かけた/もう1つ忘れてはいけないのが>〜でした。` |
| ② VÌ SAO CÓ MẶT | 6–25% | giá cả/khan hiếm thời đó (牛肉が高かった · クジラが動物性タンパクの4割) |
| ③ **THỰC ĐỊA — HIỆN TẠI TIẾN HÀNH** | **25–60%** | ngũ quan dồn cụm: 金具を包丁の角でこじ開ける → キュキュっ → 醤油を回しかける → ソースの甘い匂い. **0 câu 「なぜ」 trong CẢ bài** — cơ chế được thay bằng *tái hiện* |
| ④ CALLBACK 給食/お弁当 | 60–90% | mọi mục đều vòng về **給食** hoặc **お弁当** — 2 ký ức dùng chung của cả tệp khán giả |
| ⑤ HẠ CÁNH | 90–100% | **「お母さんの工夫と<優しさ/知恵/愛情>が詰まっていたのかもしれません」 — 5/5 mục cùng một câu, chỉ đổi danh từ** |

### 1.4 ⭐ LUẬT SÓNG — mục KHÔNG được đều nhau (chỉ K1)

Độ dài 20 mục của K1 (ký): `432 · 226 · 193 · 302 · 265 · 421 · 384 · 167 · 200 · 190 · 107 · 92 · 117 · 218 · 221 · 198 · 178 · 152 · 514 · 269`

- Mục **ai cũng biết rồi** (11 タバコ · 12 飲酒運転 · 13 お茶は女性の仕事) → **14–18 giây**, xả cho nhanh.
- Mục **có cơ chế ẩn** (6 部活で水禁止 · 7 体罰 · 19 近所の大人) → **60–80 giây**.
- **Mục dài nhất cả bài (514 ký) nằm ở 76–85%** — ngay trước tổng luận. Đỉnh cảm xúc đặt ở CUỐI, không ở đầu.
- ⇒ Chênh lệch **5,6×** giữa mục ngắn nhất và dài nhất.

🔴 **SÓNG CHỈ LÀ LUẬT CỦA E-LIST — đừng đòi ở khuôn 5 mục.** Đo K2/K3: tỉ số dài nhất/ngắn nhất chỉ **1,43×** và **1,23×**, tức khuôn 5 mục của bản thắng là **PHẲNG**. Gate vì thế miễn phép đo sóng khi bài có <8 mục; đòi 2,5× ở khuôn 5 mục là đòi thứ chính mẫu không có.

✅ **Đo lại script mình thì khoản này KHÔNG hỏng — đừng đi sửa nó.** Bản nháp đầu của tài liệu này viết *"script mình chia 20 điểm gần đều → không có sóng"*; gate đo ra **script 10 = 18,3×** (39–713 ký, mục dài nhất ở **82%** bài) và **script 11 = 5,2×** (76–394 ký, mục dài nhất ở **87%**). Tức mình đã có sóng, và đã đặt đỉnh đúng chỗ — cùng chiều với K1. Câu cũ là **đoán bằng mắt**, đã bỏ.

### 1.5 QUY ĐỔI SANG TỐC ĐỘ ĐỌC CỦA KÊNH MÌNH (`showa-b` = 4,93 ký/giây)

| | ký | ra phút ở 4,93 ký/s |
|---|---|---|
| K2/K3 nguyên bản | 6.700 | **22,6′** — vượt trần 13–18′ của kênh |
| **Dải phải nhắm** | **4.300–5.300** | **14,5–17,9′** |
| Script mình hiện tại | 3.960 | 13,4′ |

⇒ **Bản 5 mục cho kênh mình: 5 mục × 850–950 ký + intro 350 + kết 400 ≈ 4.900 ký ≈ 16,6′.**
⇒ Bản 20 mục: 20 mục trung bình 200 ký (sóng 90–500) + 800 ≈ 4.800 ký ≈ 16,2′.
🔴 Mọi mốc trên là **ƯỚC** — chỉ chốt sau render từ `timeline.json` (CLAUDE.md §Sản xuất).

---

## 2. ĐỘNG LỰC & NHỊP NHÂN VẬT (CHARACTER MAPPING)

Đây là phi hư cấu, nên "nhân vật" không nằm trong bài. **Nhân vật chính là NGƯỜI XEM.** Ba bản thắng đều dựng đúng 3 vai:

| vai | K1 | K2 | K3 | việc của vai |
|---|---|---|---|---|
| **案内人** (người dẫn) | 亀吉, có tên, có 私 | **vô hình** (0 lần 私) | **vô hình** | dẫn + phán một câu ở cuối mục |
| **証人** (người làm chứng) | **「65の私の父」・「60代の知人」×2** | — | — | nói hộ điều người dẫn không được phép khẳng định |
| **主人公 vắng mặt** | thế hệ 「あの時代を生きた人たち」 | 「町全体」 | ⭐ **お母さん** — có mặt ở **5/5 mục**, là chủ ngữ của mọi hành động | chỗ để khán giả gắn cảm xúc |

**Want / Need / rào cản — của người xem:**

| | |
|---|---|
| **WANT** (thứ làm họ bấm) | 「あっ、あった！」 — xác nhận ký ức của mình có thật |
| **NEED** (thứ làm họ ở lại tới cuối + comment) | **được nói rằng cái thời khổ đó có nghĩa** — 「めちゃくちゃだったけど、強かった」 |
| **RÀO CẢN** | chính hiện tại: tiện lợi, an toàn, nhưng nhạt và cô đơn. Cả 3 bản đều dựng hiện tại làm phản diện **mà không chê hiện tại** |

**Arc 5 mốc tâm lý — bê nguyên sang bất kỳ đề tài nào:**

1. **giật mình** (0–1′): 「そんなことしてたのか」 — cú sốc phải là điều *chính họ đã làm*
2. **được xác nhận** (1–8′): 「うちもそうだった」 — chuỗi cảnh cụ thể
3. **hiểu ra** (giữa mỗi mục): 「だからあの時代はそうだったのか」 — ô ③④, đây là chỗ khán giả bắt đầu *tôn trọng* bài
4. **chạnh lòng** (cuối mỗi mục): 「便利になったけど、なくなったものもある」
5. **được đền** (90–96%): 「あの時代を生きた自分は、強かった」 → chính lúc này mới xin comment

🔴 **Mốc 5 là chỗ mình đang mất trắng.** Script 10 và 11 của mình có **0 câu đóng mềm**; script 11 đóng bằng phân tích (「事件と、便利さに、負けたんです」) — sắc, đúng, nhưng nó trả lời cho **cái đầu**, không đền cho **cảm xúc**. Ba bản thắng đóng bằng cảm xúc **9–11 lần mỗi bài**.

---

## 3. PHÂN TÍCH DỰNG CẢNH (SCENE-BY-SCENE, 4 YẾU TỐ)

### 3.1 K2 mục 4 「緩すぎる防犯」 (1.478 ký — mục dài nhất K2)

| yếu tố | nội dung |
|---|---|
| **Mục tiêu cảnh** | không phải "kể là hồi đó không khoá cửa", mà **chứng minh: cái thay cho ổ khoá là CON NGƯỜI** |
| **Xung đột** | an toàn ↔ khoảng cách giữa người với người. Muốn cái này thì mất cái kia — không có lối thoát nào cả |
| **Điểm lật** | mở: 「鍵をかける習慣が薄かった」(nghe như bất cẩn) → đóng: 「無防備ではなく、信頼で成り立っていた社会の形」(**bất cẩn → tin nhau**) |
| **Subtext** | mọi ví dụ (縁側 · 呼び出し電話 · 醤油を借りる · 番犬 · 豆腐屋のラッパ) đều là **cùng một mệnh đề nói 5 lần**: *nhà mở thì người mới vào được*. Không câu nào tuyên bố mệnh đề đó — nó tự hiện ra |
| **Chuyển động vật lý** | dẫn theo **cấu trúc căn nhà**: 縁側 → 玄関 → 隣の家 → 町. Không dẫn theo danh mục |

### 3.2 K3 mục 1 「魚肉ソーセージ」 (1.325 ký)

| yếu tố | nội dung |
|---|---|
| **Mục tiêu** | biến một món **rẻ tiền** thành một món **được thương** |
| **Xung đột** | nghèo ↔ muốn cho con ăn thịt. Mẹ thắng bằng mẹo, không bằng tiền |
| **Điểm lật** | mở 「今ではおやつというイメージ」 → đóng 「立派なお肉料理」. Cùng một vật, **địa vị bị đảo** |
| **Subtext** | chi tiết ăn tiền nhất là **cái vô dụng về mặt thông tin**: mở kẹp nhôm bằng góc dao · xé vỏ bằng răng · **「キュキュっという音を聞くだけで、今日は魚肉ソーセージだなと分かった」** — không dạy gì cả, nhưng nó *là* ký ức |
| **Thủ pháp giữ chân trong mục** | dời cảnh: 台所 → 食卓 → **翌朝のお弁当** (mở hộp cơm thấy một khoanh hồng, thấy như được lời) — **thưởng thêm sau khi mục tưởng đã hết** |

### 3.3 K1 mục 6 「部活で水を飲ませてもらえなかった」 (421 ký — đỉnh chất lượng của cả 3 bản)

| yếu tố | nội dung |
|---|---|
| **Mục tiêu** | truy **NGUỒN GỐC** của một tập quán vô lý — chứ không chỉ kể là nó vô lý |
| **Xung đột** | y học ↔ tinh thần. Và **tinh thần thắng** — đó là chỗ đau |
| **Điểm lật** | 3 tầng: ① 「水を飲むとバてる」(nhắc lại từ cold open) ② truy ra **明治37年・武田千代三郎『理論実験 競技運動』**「余分な水を抜けば汗が減り血が濃くなって酸素をよく運ぶ」→ 「今の医学からしたらかなりぶっ飛んでますね」 ③ **cú lật thật**: 「ただ、同じ本にもこうあります —『この苦しさに耐えたものは己に勝った人間だ』。理屈より先に、この“己に勝つ”という精神が生き残りました」 |
| **Subtext** | cơ chế lan truyền được kể như một dòng máu: 「先生から生徒へ。その生徒が先生になってまた生徒へ」 — người xem tự hiểu *chính mình là một khâu trong chuỗi đó* |
| **Vì sao đây là bản mẫu cho kênh mình** | nó là **図鑑 đúng nghĩa**: có nguồn cấp 1, có năm, có trích nguyên văn, và cái nó giải thích là **một điều người xem đã tự trải qua bằng thân thể**. Không cần một đồng giá nào |

---

## 4. TRÍCH XUẤT "CÔNG THỨC ĂN TIỀN" (CORE ENGINE)

### E1 🔴 ĐƠN VỊ ĐỀ TÀI LÀ **ĐIỀU ĐƯƠNG NHIÊN**, KHÔNG PHẢI **VẬT**

Cả 3 bản 100K: 常識20選 · 風習5つ · 母の定番料理5つ. **Không bản nào là 「消えた◯◯N選」.**
Khớp đúng số đã đo ở benchmark 08-29: cùng một kênh, cùng khuôn, cùng giọng — 実家アイテム **143 v/ngày** vs お金の常識 **4.460 v/ngày** = **31×**.

| | VẬT (mình đang làm) | ĐIỀU ĐƯƠNG NHIÊN (3 bản thắng) |
|---|---|---|
| câu hỏi bật ra trong đầu người xem | 「覚えてる？」 → trả lời xong là hết | 「本当にやってたな…なんでだ？」 → còn nợ một lời giải thích |
| chỗ để cài cơ chế | ít (vật thì chỉ có công dụng) | nhiều (thói quen luôn có lý do + luôn có ngày chết) |
| comment | liệt kê tên vật | **kể chuyện của chính mình** ← thứ YouTube đọc là engagement |
| trần cảm xúc | hoài niệm | hoài niệm **+ tự hào + chạnh lòng** |

✅ **ĐÃ ÁP 2026-09-07 (user chốt).** Khung 「VẬT + CON SỐ」/「消えた◯◯N選」 hết hiệu lực ở `CLAUDE.md` §Identity · `00_CHANNEL_BIBLE.md` §1/§3 · `02_CONTENT_STRATEGY.md` §0/§0.1/§2 · `06_VIDEO_QUEUE` · `youtube-jp-showa.md`. Danh sách từng luật bị bỏ: §7.1.

### E2 「いつ死んだのか」— MỐC NĂM MÀ CÁI ĐƯƠNG NHIÊN CŨ CHẾT (1 lần / 300–480 ký)

Đây là **con số duy nhất** 3 bản thắng dùng. Không phải giá — mà là **ngày cái thói quen đó hết hợp pháp / hết tồn tại**:

`ミネラルウォーター phổ biến từ 昭和58年` · `食鳥処理法 平成2年` · `生食用食肉の規格基準 平成23年10月` · `赤チン ngừng sản xuất 令和2年 (水銀に関する水俣条約)` · `名簿と連絡網 biến mất sau 個人情報保護法 平成17年4月` · `セクハラ ra đời 平成元年` · `パワハラ 平成13年, luật 令和2年` · `酒の屋外自販機 ~平成12年` · `タスポ 平成20年7月` · `ヘルメット nghĩa vụ toàn tuyến 昭和61年` · `車庫法 昭和37年` · `公衆衛生局長報告 1964年`

**Vì sao nó mạnh:** nó biến "hoài niệm" thành "biên niên sử" — và nó cho người xem **một cái mốc để tự định vị mình** (「うちが車を買ったのはその後だ」). Đúng định vị 図鑑 của kênh mình, mà **không** cần tra giá.
✅ Mình đã có hạ tầng verify nguồn — đây là chỗ mình *dễ* hơn họ, chỉ là chưa làm dày.

### E3 「実は禁止されていた」— KHE GIỮA **LUẬT** VÀ **THỰC TẾ** (chỉ K1, 1 lần / 304 ký)

Thủ pháp mạnh thứ hai của K1 và **chưa kênh nào trong ngách khai thác**:

> 「補足として事実をお伝えしておきますが、学校での罰は**昭和22年**に定められた**学校教育法第11条**ではっきりと禁止されていました。つまり許されていたわけではありません。**禁止されていたけど、誰も問題にしなかった。それが当時の空気でした。**」

Ba lần dùng: 体罰 (学校教育法11条) · 未成年へのタバコ販売 (**明治33年 = 1900年** đã cấm!) · 荷台への乗車 (道交法55条).
**Cấu trúc:** ① kể như thể hồi đó được phép → ② lật: luật đã cấm từ trước rất lâu → ③ kết luận về *không khí thời đại*, không phải về luật.
⇒ Cú lật này **rẻ** (chỉ cần tra một điều luật), **an toàn** (fact công khai), và tạo đúng cảm giác 「へえ！」 mà thumbnail 「今では信じられない」 đã hứa.

### E4 THỰC ĐỊA — HIỆN TẠI TIẾN HÀNH + NGŨ QUAN (1 lần / 216–292 ký)

K3 đặc mùi và tiếng. Công thức của một khối thực địa (đo được ở 5/5 mục):

`dụng cụ + động tác của bàn tay` → `TIẾNG` → `MÙI` → `MÀU` → `một câu kết luận nhỏ`

> 「金具の部分を包丁の角で器用にこじ開けたり、歯でピーッとビニールを剥いたり」 → 「まな板の上で斜めに切るとキュキュっと独特の音が台所に響きます」 → 「醤油を少し回しかける…ソースの甘く香ばしい匂いが広がると」 → 「つるりとしたピンク色」 → 「この音を聞くだけで、今日は魚肉ソーセージだなと分かった」

**Luật:** viết ở **thời hiện tại** (「〜します」「〜響きます」), không viết 「〜していました」. Quá khứ thì người xem *nghe kể*; hiện tại thì họ *đang ở đó*.
Mình đang ở **1/1.319–1.994** — thiếu **5–7×**. Đây là khoản rẻ nhất để sửa và không đụng gate nào.

### E5 「では、なぜ」— CHỐT LẬT ĐÚNG GIỮA MỤC (4/5 mục K2, ở 42–57%)

「ではなぜこんな光景が成立していたのか。**最大の理由は**〜」 · 「そこには現代とは大きく異なる社会の構造がありました」 · 「その理由の1つが住宅の構造にありました」

Nó chia mỗi mục thành **hai nửa khác chức năng**: nửa đầu *cho nhớ*, nửa sau *cho hiểu*. Người xem vượt được mốc giữa mục vì có một câu hỏi vừa được nêu ra thành lời.
✅ Mình có sẵn (`なぜ` 1/395–664) — nhưng chưa **đặt đúng chỗ**: phải là câu hỏi **nói ra thành lời, ở giữa mục**, không phải rải rác.

### E6 ĐÓNG MỀM 「〜かもしれません」 + 認める→裏返す (9–11 lần/bài · mình = 0)

Mọi mục và cả bài đóng bằng **suy đoán mềm**, không bằng khẳng định:

> 「それは昭和という時代そのものを象徴する空気だったの**かもしれません**」
> 「その大らかさとたくましさこそが、昭和という時代の一面だったの**かもしれません**」
> 「家計をやりくりしながら家族の食卓を支えていたお母さんの工夫と優しさが詰まっていたの**かもしれません**」
> 「便利になるほど隣の家に用がなくなる…少し**寂しい気がします**」

Và tổng luận theo **認める→裏返す**: 「正直に言えば、変わって良かったこともあります。体罰も飲酒運転も、なくなってよかった。**でも**、昭和を生きた人たちは強かった」
🔴 Vì sao phải mềm: khán giả 45+ **không chịu nổi ai đó dạy họ về thời của họ**. 「かもしれません」 trả quyền phán xét lại cho họ → và họ trả lời bằng comment. K1 xin comment ngay sau tổng luận, xin đúng thứ 「体験談でも思い出話でも」.

### E7 CỬA VÀO — COLD OPEN 23 GIÂY CỦA K1 (bản mạnh nhất trong 3)

```
①  水を飲むとバてる。そう言われて、練習中は一滴も飲ませてもらえない。   ← hành vi vô lý, KHÔNG giải thích
②  だから、先輩の目を盗んで川の水を飲む。                          ← hệ quả, có hình
③  これ、実話です。65の私の父の話です。                            ← BẢO ĐẢM CÓ THẬT + nhân chứng
④  転んですり剥けば赤チン。ノーヘルで原付。子供が父親のタバコを買う。飲酒運転もざらに。 ← 3 cú sốc dồn
⑤  これが昭和です。猛烈な時代です。                                ← DÁN NHÃN
```
- **Không lời chào cho tới giây 23.**
- Câu 1 là **HÀNH VI**, không phải mô tả tĩnh — đúng cái script 11 của mình tự chấm 🔴 (「茶色い封筒。手のひらより少し大きい」).
- ③ là thứ mình dùng được ngay: **một câu 「これ、実話です」 + một người làm chứng** (60代の知人/父) — hợp `humanize-script-voice.md` §1 mũi ②, và không phạm YMYL vì nó là ký ức, không phải số liệu.

### E8 THỦ PHÁP HÌNH THAY LỜI (VISUAL CUES) — đọc từ lời, để dựng prompt t2v

Cả 3 bản chỉ dùng **4 loại hình**, và đều là **người đang LÀM một việc**:

| loại | ví dụ trong lời | dịch sang prompt |
|---|---|---|
| bàn tay + dụng cụ | 包丁の角で金具をこじ開ける · 出席簿で頭を叩く | `ots`/`medium` — ⛔ không `hands only` (CLAUDE.md §Visual) |
| tranh giành / đối đầu | テレビの前で場所を確保 · 兄弟で取っ組み合い | 2 cast, ≤2/cảnh |
| đám đông cùng làm một việc | 水飲み場に行列 · 会議室が白く煙る | wide, có người |
| vật ĐANG hoạt động | バキュームカーのホース · ハエ取りリボン · 蚊帳 | vật chiếm ≥40% khung |

⇒ **Viết lời sao cho mỗi 8 giây có MỘT động tác dựng được.** Đây cũng là lời giải cho lỗi đã đo ở video 04: "phố vắng đẹp như phim Kurosawa nhưng không có gì để 「あっ、あった！」".

### E9 ⚠️ BA THỨ CHÚNG **KHÔNG** CÓ — và điều đó có nghĩa gì

| thứ | 3 bản thắng | mình | đọc |
|---|---|---|---|
| cliffhanger / mồi cài giữa bài | **0** | có (script 11 cài 2 mồi) | mình hơn — **giữ**, nhưng biết rằng nó không phải điều kiện để đạt 100K |
| đếm điểm / quiz giá | **0** | có | giữ như **đòn payoff giữa bài** (đúng `02_CONTENT_STRATEGY.md` §3), không làm nó thành chủ đề |
| recap cuối | 0 (K2/K3) | 0 | ✅ đừng thêm — kênh đối thủ 42 long-form recap 2′40″ là chỗ rớt |

---

## 5. BẢNG KIỂM TRA (CHECKLIST) & ÁP DỤNG NGƯỢC

### 5.1 15 câu tự vấn — chạy TRƯỚC khi viết ô nào

**Đề tài & khung**
1. Chủ đề là **điều người xem TỪNG LÀM** (常識・風習・当たり前) hay chỉ là **vật họ từng thấy**? (E1)
2. Có trả lời được 「なぜ、それが普通だったのか」 bằng **chế độ/hạ tầng/giá cả**, không phải bằng cảm tính?
3. Có **≥8 mốc năm** mà cái đương nhiên đó chết? (E2)
4. Có **≥1 khe LUẬT ↔ THỰC TẾ** (「実は禁止されていた」)? (E3)

**Mở bài (≤60s, vào mục 1 ở 36–55s)**
5. Câu 1 là **HÀNH VI đang xảy ra**, không phải mô tả tĩnh?
6. Có câu 「これ、実話です」 + **một người làm chứng**?
7. Có câu **DÁN NHÃN** thời đại (「これが昭和です」)?
8. Lời chào đặt **SAU** cú sốc?

**Thân bài**
9. Mỗi mục có đủ **5 ô** (①TUYÊN BỐ ②THỰC CẢNH ③なぜ ④MỐC CHẾT ⑤HẠ CÁNH)? (§1.3)
10. Câu 「では、なぜ」 nằm ở **40–60% của mục**? (E5)
11. Khối thực địa viết ở **thời hiện tại**, đủ **tiếng + mùi + màu + động tác tay**? (E4)
12. Có **sóng độ dài**: mục ai-cũng-biết ≤20s, mục có cơ chế 60–80s, **mục dài nhất đặt ở ~80% bài**? (§1.4)
13. Mỗi 8 giây có **một động tác dựng được** thành clip? (E8)

**Kết**
14. Mỗi mục đóng bằng **một câu mềm** (かもしれません/気がします)? Cả bài **≥5 câu** loại này? (E6)
15. Tổng luận theo **認める→裏返す**, rồi **mới** xin comment (xin 体験談, không xin 「どれを覚えていますか」)?

### 5.2 DẢI SỐ MỤC TIÊU + GATE MÁY

```bash
python tools/check_script_formula.py 03_SCRIPTS/<slug>_TTS.md --truc A     # script mình
python tools/check_script_formula.py 03_SCRIPTS/kichban2.md --raw          # transcript đối thủ
```

🔴 **LUẬT HAI ĐỘNG CƠ — và bài học về chính cái gate này.** Bản đầu của gate đòi **cả** ngũ quan dày **và** cơ chế/luật dày → nó **đánh trượt 3/3 bản thắng**. Đo lại thì hai động cơ **ĐÁNH ĐỔI nhau, không cộng dồn**:

| | ngũ quan | pháp/chế độ | 「なぜ」 | động cơ |
|---|---|---|---|---|
| K1 | 1/2.888 ❌ | **19** ✅ | 3 | **E-LIST** (cơ chế + mốc năm + khe luật) |
| K3 | **1/209** ✅ | 2 ❌ | **0** | **E-SCENE** (tái hiện bằng ngũ quan) |
| K2 | 1/292 ✅ | 7 ✅ | 7 | cả hai |

⇒ Gate chỉ đòi **≥1 trong 2**. Cùng họ bài học `humanize-script-voice.md §1.2`: *gate đo HÌNH THỨC THI HÀNH của bản mẫu thay vì đo CƠ CHẾ*. Gate nào đánh trượt chính mẫu nó học từ đó thì **gate sai, không phải bài sai**.

**Tầng CHẶN** (sai = chưa đạt khuôn, exit 1):

| chỉ số | dải mục tiêu | căn cứ |
|---|---|---|
| **động cơ chính** | **≥1 trong 2**: `E-SCENE` ngũ quan ≥1/250 ký · `E-LIST` pháp/chế độ ≥8 lần + mốc năm ≥1/500 ký | K1 LIST · K3 SCENE · K2 cả hai |
| số ký | **14,5–18,0 PHÚT × tốc độ giọng** (miễn khi `--raw`) | trục B 4,93 ký/s → 4.289–5.324 · trục A ~3,98 → **3.465–4.301** |
| mốc năm | **≥8 lần và ≥1/500 ký** | K1 1/339 · K2 1/292 · K3 1/478 |
| đóng mềm かもしれません… | **≥5 lần** | K1 5 · K2 7 · K3 11 |
| kim tiền (trục A) | **≤6 lần** | 3 bản thắng: 0–1. Trục **B** miễn |
| vào mục 1 | **≤60s** (nhắm 40–50s) | 3/3 bản ở 36–55s |

**Tầng CẢNH BÁO** (đọc trước khi giao, không chặn — vì có bản thắng không dùng): ngũ quan ≥1/250 · nay–xưa ≥1/600 (K3 chỉ 1/1.341) · 「なぜ」 ≥1/mục (K3 = 0) · pháp/chế độ ≥3 (K3 = 2) · lời thuật lại ≥4 · người làm chứng ≥1 (chỉ K1 có) · sóng độ dài ≥2,5× + đỉnh ở ≥65% bài — **sóng chỉ kiểm khi bài ≥8 mục** (§1.4).

⚠️ **Hai lần tao phải sửa chính gate này, ghi lại để không ai bóp lại:**
- **Bộ từ ngũ quan đã NỚI** (thêm 味・冷た・湿った・煙・肌・舌・ぱき・つるり…) vì bộ từ đầu chỉ đúc từ K3 nên bắt trượt cách viết khác. **Nới xong phải hạ ngưỡng theo cùng 3 mẫu**: 350 → **250**, và kiểm lại rằng phân loại không đổi (K1 1/962 vẫn LIST · K2 1/186 · K3 1/134 vẫn SCENE). Nới bộ từ mà giữ ngưỡng cũ = tự nới gate cho vừa bài mình.
- **Dải độ dài phải tính theo PHÚT**, không phải số ký cố định: giọng trục A (東北イタコ ~3,98 ký/s) và trục B (阿井田茂 4,93) lệch **24%** ⇒ một dải ký cố định sẽ đánh trượt oan một trong hai trục.

**Kết quả chạy thật (2026-09-07):** 3/3 bản thắng **SẠCH tầng chặn**. Hai script mình **4 đỏ mỗi bản**:

| | script 10 通学路 | script 11 給料日 |
|---|---|---|
| động cơ chính | 🔴 **KHÔNG CÓ** (ngũ quan 1/1.994 · pháp 1) | 🔴 **KHÔNG CÓ** (ngũ quan 1/1.319 · pháp 7 — thiếu 1) |
| đóng mềm | 🔴 **0** | 🔴 **0** |
| mốc năm | 🔴 4 (1/997) | ✅ 8 (1/494) |
| số ký | 🔴 3.989 | 🔴 3.959 |
| vào mục 1 | ✅ 22s | ✅ 60,0s |
| sóng độ dài | ✅ 18,3× @82% | ✅ 5,2× @87% |
| lời thuật lại | ✅ 15 | ✅ 7 |

### 5.3 ÁP NGƯỢC — thứ tự làm

1. Chọn đề tài theo **E1** (mở `01_SWIPE_TITLES.md` trước, `youtube-suggested-growth.md` §2).
2. Viết **FACT SHEET trước lời** (đã là luật kênh): mỗi mục **≥1 mốc năm + ≥1 chế độ/luật**, verify nguồn cấp 1. Không có mốc chết → **đổi mục**, đừng viết bù bằng cảm xúc.
3. Rải **sóng độ dài** trước khi viết câu nào: đánh dấu mục nào 20s, mục nào 80s, mục dài nhất ở ~80%.
4. Viết cold open theo **E7** (5 câu), rồi kiểm gate ≤60s.
5. Viết từng mục theo **5 ô**, ghi rõ tên ô trong bản `.md` (⛔ không đưa nhãn ô vào `_TTS.md`).
6. Rải tag nhấn nhá **sau khi văn đã xong** (~32 cụm ≈ 1/124 ký, chuẩn video 10/11) — ⛔ tag **dính liền câu**, không đứng một dòng riêng (`humanize-script-voice.md` §2).
7. Chạy `check_script_formula.py` + gate cũ của kênh, rồi mới render demo giọng.

---

## 6. VIẾT THỬ — CỬA VÀO + 1 MỤC HOÀN CHỈNH (đề tài #13 「昭和の夏、エアコンのない家」)

> Bê **bộ xương** của 3 bản thắng, thay **100% chất liệu**. Đây là bản mẫu để đối chiếu, chưa phải script giao.
> 🔴 Mọi chỗ `【要VERIFY】` là số/mốc **chưa tra** — theo luật YMYL của kênh, phải verify nguồn cấp 1 trước khi vào `_TTS.md`. Tao **không** điền số bịa vào đây.

**COLD OPEN (E7 — 5 nhịp, 158 ký ≈ 32 giây)**

```
[間0.6]夏の夜は、家じゅうの窓を、あけて寝ていました。
[速0.9]玄関も、あいたまま。
[間0.4]これ、不用心の話ではありません。涼むための、当たり前でした。
[抑揚1.25]昭和の夏に、エアコンはありません。
それでも、みんな、あの暑さを越していたんです。
[間0.5]これ、実話です。七十代になる、私の知人の話です。
```
→ 挨拶 (「こんばんは、昭和くらし図鑑です」) đặt **sau** khối này, rồi PROMISE 「今回は、エアコンのない家がどうやって夏を越したのか。今では信じられない、夏の当たり前を◯つ」→ **vào mục 1 ở ~48s**.

**MỤC 1 — 「窓は、あけて寝るもの」(5 ô, ~1.060 ký ≈ 3′35″ — cần cắt về 900 ký khi viết thật)**

| ô | lời |
|---|---|
| ① TUYÊN BỐ | 「一点目。窓は、あけて寝るもの。[間0.4]昭和三十年から四十年ごろ。**今では考えられませんが**、夏の夜に窓を閉める家は、ほとんどありませんでした。」 |
| ② THỰC CẢNH *(hiện tại tiến hành + ngũ quan)* | 「縁側のガラス戸を、いっぱいにあける。網戸のかわりに、蚊帳を吊る。[間0.3]鴨居に紐を回して、四隅をひっぱって、裾を布団の下に折り込む。この折り込みが甘いと、朝までに必ず一匹、入っています。[速0.88]蚊取り線香を、豚の陶器に立てる。あの、少し焦げたような匂い。**畳が汗を吸って、朝には少しひやりとしている**。団扇を持ったまま、寝てしまう。」 |
| ③ 「では、なぜ」*(đúng giữa mục)* | 「**では、なぜ、窓をあけたまま眠れたのか。**理由の一つは、家のつくりでした。木と紙と土でできた平屋は、風が通るように建てられています。閉めると、暑さが逃げない。**あける以外に、涼む方法がなかったんです。**」 |
| ④ MỐC CHẾT | 「変わり目は、ルームエアコンが家庭に入ってきたころです。【要VERIFY: 内閣府 消費動向調査 — 世帯普及率が◯%を超えた年】。[間0.4]窓を閉めて眠れるようになったのは、【要VERIFY】年ごろから。同じころ、【要VERIFY: アルミサッシ普及 / 網戸の一般化】…」 |
| ⑤ HẠ CÁNH *(mềm)* | 「いまは、窓を閉めて、ボタンを一つ押せば涼しくなります。ありがたいことです。[間0.6][速0.85]ただ、あけた窓から入ってきた音——風鈴、遠くの電車、隣の家の話し声——**あれも一緒に、閉めてしまったのかもしれません。**」 |

**Số đo của bản thử này:** 1.060 ký · mốc năm 2 (chờ verify) · ngũ quan **7** (1/151) · 今との対比 2 · đóng mềm 1 · 「なぜ」 ở **46%** của mục · 8 động tác dựng được thành clip.

---

## 7. ⚠️ BỐN CHỖ XUNG ĐỘT VỚI RULE ĐANG CHẠY

> ✅ **Mục 1 · 2 · 3: USER CHỐT 2026-09-07 — đã áp.** Mục 4 giữ nguyên rule cũ (không xung đột thật).
> Video đầu tiên chạy khuôn này: `03_SCRIPTS/12_natsu-atarimae.md` (昭和の夏の当たり前5つ).

| # | đang ghi ở đâu | phép đo nói gì | trạng thái |
|---|---|---|---|
| 1 | `CLAUDE.md` §Identity + `02_CONTENT_STRATEGY.md` §0: **「VẬT + CON SỐ」/「消えた◯◯N選」** | 3/3 bản 100K là **常識・風習・家庭料理**, 0 bản là 「消えた物」. Cộng số cũ: 実家アイテム 143 v/d vs お金の常識 4.460 v/d = **31×** | ✅ **CHỐT: đơn vị đề tài = 「今では信じられない〜の当たり前」.** Giữ tên kênh, giữ trục B, giữ 図鑑 (nguồn + mốc năm) làm lớp tin cậy. Đã sửa `CLAUDE.md` §Identity/§Luật 7 + `02_CONTENT_STRATEGY.md` §0 |
| 2 | `CLAUDE.md`: **mỗi vật ≥1 số có nguồn + đố giá** | 3 bản thắng có **0–1 lần nhắc tiền** trong ~6.700 ký; "số" của họ là **MỐC NĂM** (1/292–478) | ✅ **CHỐT: đổi LOẠI số** — mốc năm dày (≥1/500 ký) là bắt buộc; **giá giữ làm payoff giữa bài**, trần ≤6 lần ở trục A. Trục B (物価/給料) không đổi |
| 3 | độ dài **13–18′** ⇒ mình viết 3.960 ký (13,4′) | họ 5.776–6.724 ký | ✅ **CHỐT: nâng lượng chữ** — dải = **14,5–18,0 phút × tốc độ giọng** (trục A 3.465–4.301 ký · trục B 4.289–5.324) |
| 4 | `humanize-script-voice.md` §1: người kể xuất hiện + thoại | K2/K3 người kể **vô hình tuyệt đối** (0 lần 私), K1 chỉ 5 lần và qua **証人** | **Giữ nguyên rule** — nhưng chất người đi qua **証人 + nhân vật** (K1: 父/知人 · K3: お母さん), người dẫn không kể chuyện mình. Trùng đúng §1.1 của rule đó |

### 7.1 SỔ LUẬT ĐÃ BỎ (user: *"luật cũ cái nào không hợp lý thì bỏ đi"* — 2026-09-07)

| luật cũ | ở đâu | bằng chứng bỏ | thay bằng |
|---|---|---|---|
| Định vị 「**VẬT + CON SỐ**」 | `CLAUDE.md` §Identity+header · `00_CHANNEL_BIBLE.md` §1 · `youtube-jp-showa.md` | 0/3 bản >100K là 「消えた物」 · 31× ở benchmark | 「**当たり前 + MỐC NĂM**」 |
| Khung 「**消えた◯◯N選**」 làm chủ đạo | `02_CONTENT_STRATEGY.md` §0/§0.1/§2.1 · `06_VIDEO_QUEUE` | hook 消えた = tầng bét ngách; 0/3 bản dùng | 「今では信じられない〜の当たり前N選」 (消えた còn dùng làm biến thể A3) |
| **Cơ chế ĐẾM ĐIỂM** 「覚えてたら1点」/「何点でしたか」 | `00_CHANNEL_BIBLE.md` §3 mục 6 | **0/3 bản** có đếm điểm; đuôi title 何点覚え đã bị bỏ từ 09-03 | comment bait xin **体験談/思い出話**, đặt sau tổng luận |
| **Quiz đố giá = "retention chủ lực"** | `CLAUDE.md` §Luật 4 · `00_CHANNEL_BIBLE.md` §3 | **0/3 bản** đố giá | ô ③「では、なぜ」 + mốc năm. Đố giá còn lại là **thủ pháp của riêng trục B** |
| "**Mọi video trục A cài ≥1 câu hỏi giá**" | `02_CONTENT_STRATEGY.md` §3 | 3 bản nhắc tiền **0–1 lần**/6.700 ký | trần **≤6 lần nhắc tiền/bài** ở trục A |
| "Mỗi vật **BẮT BUỘC ≥1 con số giá**" | `00_CHANNEL_BIBLE.md` §3 mục 7 | như trên | mỗi mục **≥1 MỐC NĂM** verify được (bài: ≥8 lần, ≥1/500 ký) |
| Cold open "**≤15s bắn thẳng 1 VẬT**" + câu neo 「昭和◯年、あなたが◯歳だった頃…」 | `CLAUDE.md` §Luật 1 · `00_CHANNEL_BIBLE.md` §3 mục 1 | K1 mở **23s không lời chào**; câu 1 của 3/3 bản là **HÀNH VI**, không phải tên vật | khuôn **E7** (§4) |
| Gate "**vào VẬT đầu tiên ≤60s**" | `CLAUDE.md` §Sản xuất | đơn vị đổi | "vào **MỤC** đầu tiên ≤60s, nhắm 40–50s" |
| Độ dài "**10–14′**" | `02_CONTENT_STRATEGY.md` §0.1 · `06_VIDEO_QUEUE` | 3 bản dài 5.776–6.724 ký = 15–19′ | **14,5–18,0′ × tốc độ giọng** |
| Thumbnail "**1 vật chụp to + chữ 「覚えてる？」/「給食」**" | `00_CHANNEL_BIBLE.md` §Title/Thumbnail | 7/7 hero danh từ, 0 video được rail đẩy | hero = **MỆNH ĐỀ có gap** + chữ phải khớp 30s đầu |
| Nhịp "**2 video/tuần**" | `02_CONTENT_STRATEGY.md` §5 | lạc hậu so với nguồn sự thật | `.claude/rules/upload-schedule.md` §0.9 (3/tuần T3·T5·T7) |
| Mũi ① humanize **qua người dẫn** | `.claude/rules/humanize-script-voice.md` §1.1 | K2/K3 **0 lần 私** | đạt bằng **証人** — ngoại lệ scoped chỉ cho showa |

⛔ **Cái KHÔNG bỏ, dù 3 bản thắng không có:** lời thoại/lời thuật lại (phép đo bị ASR làm hỏng — §0.2 mục 1) · tag nhấn nhá + khoảng lặng (không đo được từ transcript) · mồi cài giữa bài & CTA giữa video · nguồn cấp 1 + verify số (đó là moat, và là YMYL) · **không recap cuối** (giữ, cả 3 bản cũng không có).

✅ **Hai video đang dở — user chốt 2026-09-07: *10 đăng nguyên · 11 viết lại*.**
- **video 10 通学路** (đã render): **đăng nguyên**, coi là mẫu đối chứng của luật cũ (đếm điểm 30点, đơn vị VẬT). ⛔ Không re-render — `feedback_bot_render_lai`.
- **video 11 給料日**: **đã viết lại xong**, gate SẠCH tầng chặn (LIST · 4.871 ký/16′28″ · 7 câu đóng mềm · 0 đếm điểm · vào mục 1 ở 57,6s). Tám thay đổi + cái cố ý giữ: `03_SCRIPTS/11_kyuryobukuro.md` §7.
- ⇒ **Cặp 10/11 thành một phép so tự nhiên**: cùng kênh, cùng tệp, hai bộ luật khác nhau, đăng liền nhau. Ghi view/AVD/retention 60s của cả hai vào `08_ANALYTICS_LOG.md`.

⚠️ Và một cảnh báo về chính phép đo này: **3 mẫu là 3 mẫu.** Chúng khớp cùng chiều với 42 long-form đo ở benchmark 08-29, nên E1/E2/E6 đứng được; nhưng **E3 (khe luật–thực tế) chỉ có 1 mẫu** — dùng vì nó đúng và rẻ, không phải vì nó đã được chứng minh.

## 8. HẠN DÙNG
- Đọc lại **sau 5 video** chạy khuôn này, hoặc khi có video đầu tiên vượt 1.000 view organic/72h.
- Phép đo lặp lại được: đã gói thành `tools/check_script_formula.py` (chạy trên cả script mình lẫn transcript đối thủ).
- 🔴 Thứ khuôn này **KHÔNG** chữa được: CTR (thumbnail/title — `03_THUMBNAIL_FORMULA.md` §1.5) và **mismatch thumbnail ↔ 30 giây đầu** (`CHANNEL_DIAGNOSIS_2026-09-03.md` §5.3). Video 06 đã PASS gate 「vào vật ≤60s」 mà vẫn rớt 62% trước 0:30 — viết hay không cứu được một lời hứa sai.
