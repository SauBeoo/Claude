# 21 — もち麦：もう一つの台所（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **もち麦（水溶性食物繊維／β-グルカン）× 腸内環境 × 「もう一つの台所（大腸）」の比喩**
- **Bản đọc chuẩn:** `21_mochimugi-choukatsu_TTS.md` — **V2 (đã sửa theo yêu cầu user), 4.117 ký (thuần) · 31 dòng có tag · ước 16′13** (mô hình CPS 4.40 + GAP 0.25/dòng, `tools/check_coldopen.py` 21).
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 21` → **✅ PASS**, cold open **74 giây** (trần 90s, dư 16s) — L1–L5 sạch · S6 tháo ngòi = 0 · S7 credential = 0 · **31 dòng có tag** · 0 tag giữa câu · 1 dòng tag-riêng (đúng = dòng base) · blacklist Mục 7 = 0 · whitelist Mục 8 = **9/15 loại** (cần ≥8) · 3 câu `「〜ませんか/ありませんか」` trong cold open (L5 cần ≥3) · S8 8 điểm cảnh báo (không chặn).

## 0. ⭐ VÒNG SỬA V2 — user chê "rời rạc, hook chưa ấn tượng", đây là sửa gì và vì sao

> User: *"kịch bản phải có hồn... lôi cuốn... hook mở đầu phải thật ấn tượng. Nội dung không được rời rạc."* Đọc lại bản V1 với con mắt phê bình thật (không tự chấm điểm cao) thì đúng — ba lỗi thật:

1. **Hook V1 dùng đúng khuôn "liệt kê triệu chứng" mà MỌI video sức khỏe senior JP đều dùng** (食後、眠くなる／お腹が張る) — không sai luật, nhưng không có gì khiến người xem dừng lại ở giây 3. **Sửa:** hook mới mở bằng một **nghịch lý cụ thể** (「体重は、増えていない。食べる量も、変えていない。それなのに、なぜか、体が、重い。」) — tạo căng thẳng nhận thức (cân nặng/khẩu phần không đổi mà người vẫn nặng nề) trước khi vào triệu chứng, và ẩn dụ "台所" được giới thiệu sớm hơn, gọn hơn ("誰も、教えてくれなかった台所です" — một câu, không dây dưa).
2. **V1 bị PADDING để đạt độ dài, và đúng như user cảm nhận, nó làm nội dung rời rạc.** Khi viết V1, sau khi có bản đủ ý (~14 phút) mà cần kéo lên gần 20 phút (chuẩn cũ lúc đó), tôi đã chèn thêm 4 khối KHÔNG PHỤC VỤ mạch truyện: so sánh もち麦 với オートミール, một câu hedge mơ hồ về khảo sát dinh dưỡng quốc gia, một đoạn liệt kê "cách dùng もち麦" (味噌汁/サラダ/スープ — như một danh sách công thức chen ngang), và một đoạn "cách chọn mua ở siêu thị + yên tâm về giá". Mỗi đoạn riêng lẻ đều có thật (không bịa), nhưng CỘNG LẠI thì đúng là một chuỗi tangent rời khỏi mạch chính (ẩn dụ 台所 → tại sao mệt → cách bắt đầu → tại sao người ta bỏ cuộc). **Sửa:** cắt sạch cả 4 khối này. Câu "dùng もち麦 trong món khác cơm" được giữ lại nhưng nén thành **1 dòng duy nhất**, gài đúng chỗ nó có tác dụng thật (phần hướng dẫn tăng dần liều lượng — 「ご飯に混ぜるのが続かない日は、お味噌汁に、大さじ一杯…」), không còn là một mục riêng.
3. **Thứ tự 2 câu ở đoạn みのり tự thú bị ngược mạch** ("続けやすさ là sức mạnh lớn nhất" rồi mới nói "続けるのは khó" — kết luận đến trước lý do). Đã đảo lại: khó trước, thú nhận sau, kết luận sau cùng.

**Đánh đổi đã chọn, nói thẳng:** V2 ngắn hơn V1 hẳn **~3 phút** (16′13 vs 19′02) vì cắt tangent thay vì thêm nội dung ăn theo trần độ dài. Đây là đánh đổi ĐÚNG hướng với lời phê bình "rời rạc" của user, nhưng nó cũng có nghĩa **payoff lớn (open loop) rơi xuống 68,9%**, dưới ngưỡng khuyến nghị 75–85% của `script-shokutaku` Mục 10 (xem §5 để đọc vì sao tôi KHÔNG cố kéo nó lên bằng cách nhồi lại nội dung).

## 1. Đánh giá trung thực bản V1 (trước khi sửa) — trả lời câu hỏi của user

- **Người xem đến vì cái gì?** Vì stake mơ hồ kiểu "mệt mỏi tuổi già không rõ nguyên nhân" — đúng tệp nhưng hook diễn đạt nó bằng đúng công thức mà 90% video cùng ngách dùng (danh sách triệu chứng). Không có gì SAI về mặt luật, nhưng cũng không có gì ấn tượng để phân biệt với hàng chục video khác đang cạnh tranh cùng một ánh nhìn lướt qua trên trang chủ.
- **Người xem ở lại vì cái gì?** Ẩn dụ 「もう一つの台所」 là điểm mạnh thật (độc đáo, không đối thủ nào tìm được dùng nó — xem §2), nhưng ở V1 nó bị chen ngang bởi các đoạn liệt kê tiện ích (cách chọn mua, cách dùng đa dạng) khiến mạch cảm xúc bị đứt quãng nhiều lần giữa bài — đúng cảm nhận "rời rạc" của user, có thể chỉ ra bằng cấu trúc: V1 có 6 "chủ đề phụ" chen giữa phần thân (β-グルカン, khảo sát quốc gia, cách dùng đa dạng, cách chọn mua, giá cả, rồi mới tới đoạn NG-habit) — quá nhiều để giữ một mạch cảm xúc liền lạc trong ~14 phút thân bài.
- **Điểm 9–10/10 nghĩa là gì, và tôi có đạt được không?** Trung thực: **tôi không thể tự chấm 9–10/10** vì điểm thật chỉ đo được bằng retention curve sau khi render + đăng (kênh này đã có 3 lần đo AVD thật — `CHANNEL_DIAGNOSIS_2026-08-11` — và bài học lớn nhất từ đó là **linh cảm về "hay" không khớp với số đo thật**, ví dụ câu tưởng vô hại `にわかには信じがたいかもしれませんけれど` đã làm rớt 38 điểm retention). Việc tôi làm được: sửa đúng 3 lỗi kỹ thuật+cảm nhận cụ thể mà user chỉ ra (hook nhạt, nội dung rời rạc, thứ tự logic ngược), giữ nguyên các phần đã đúng luật (ẩn dụ, nguồn thật, nhân vật có hồn), và **nói thẳng cái còn thiếu** (payoff dưới ngưỡng khuyến nghị) thay vì báo đã hoàn hảo.

## 1b. Vì sao chọn đề tài này (trong 2 trục user yêu cầu: tim mạch / đường ruột)

User yêu cầu 1 trong 2 trục **tim mạch** hoặc **đường ruột**. Chọn **đường ruột (腸活)** vì:

1. **Tránh trùng dáng 3 video liên tiếp.** Video 17 (`中性脂肪`) và video 20 (`動脈硬化・脳梗塞`, vừa đăng) đã phủ trục mạch máu/tim rất gần nhau. Trục ruột chưa có video nào làm riêng (natto video 03 = 食べ合わせ, yogurt video 11 = tabekata — cả hai đều khác góc và đã bão hoà theo `CLAUDE.md` §③ "tránh món bão hoà 納豆/卵/ブルーベリー").
2. **もち麦 chưa từng xuất hiện** trong `03_CONTENT_PLAN.md` hay `01_SWIPE_TITLES.md` — không tự cạnh tranh.
3. **Bằng chứng cạnh tranh còn sống (2026, WebSearch — xem §2):** một kênh cùng ngách vừa đăng 04/2026 đúng góc "もち麦/納豆 phản tác dụng nếu ăn sai cách" — xác nhận góc "sai lầm khi bắt đầu" (open loop của video này) là góc đang được thị trường khai thác thật, không phải tưởng tượng.
4. **Tận dụng thêm cầu nối sang trục血糖値** (thân bài §3) mà không cần đổi hẳn sang trục tim/mạch máu — chất xơ hoà tan làm chậm hấp thu đường, cho video một lớp lợi ích kép mà không phá kỷ luật "MỘT ẩn dụ duy nhất" (Mục 3 luật gốc).

- **Người xem đến vì:** stake không phải "giảm cân" (né hẳn khung ăn kiêng của rổ đối thủ — xem §2) mà là **mất khả năng tự lập kiểu âm ỉ**, và ở V2 được diễn đạt sắc hơn bằng nghịch lý mở đầu (cân nặng/khẩu phần không đổi mà người vẫn nặng nề) thay vì danh sách triệu chứng đơn thuần.
- **Người xem ở lại vì:** ẩn dụ **「もう一つの台所」(một cái bếp thứ hai, vô hình, trong bụng)** chạy xuyên suốt, không còn bị chen ngang bởi các đoạn tiện ích như ở V1 — vi khuẩn đường ruột là "đầu bếp", chất xơ hoà tan là "nguyên liệu", axit béo chuỗi ngắn là "thành phẩm nuôi thành ruột". Open loop lớn: **"lý do thật khiến phần lớn người bỏ cuộc với もち麦 trong vòng 1 tuần"** (hứa ở ~3:20, trả ở **11:10 = 68,9%** — xem §5 về khoảng cách so ngưỡng khuyến nghị).

## 2. ĐO CẦU — phương pháp & giới hạn (đọc trước khi dùng số)

> ⚠️ **Minh bạch về phương pháp:** phiên làm việc này **không có token YouTube Data API** để chạy phép đo 30-ngày chuẩn của `youtube-upload-seo.md` §0.5 / `03_CONTENT_PLAN.md` (vốn dùng `bench_channels.py` + Google Trends `gprop=youtube`). Đã thay bằng **WebSearch quét cảnh cạnh tranh thật trên YouTube** (không phải số đo view/ngày). Đây là bằng chứng **định tính**, không phải bảng đo có `n`/`med` như các script trước — nếu cần con số chính xác trước khi đăng, chạy lại `python tools/measure_upload_hours.py`-kiểu hoặc trend-keywords skill với API thật.

**Quan sát từ WebSearch (2026-08-27, `もち麦 腸活/便秘/免疫 60代 高齢者`):**

| Quan sát | Ý nghĩa |
|---|---|
| Nhiều kênh JP (看護師が解説する, ひるおび TBS, kênh 食物繊維系) đang làm về もち麦 × 腸活/便秘/血糖値 | Cầu có thật, không phải từ chết |
| Phần lớn video nghiêng về **ダイエット/痩せる** (giảm cân) | ⛔ Rổ SAI cho tệp 60–80 của kênh mình — không đua khung giảm cân |
| Video mới nhất tìm được (04/2026): 「納豆やもち麦が逆効果？腸活でお腹が張る原因と放置NGな人の特徴」 | ✅ Xác nhận góc "ăn sai cách → phản tác dụng, đầy bụng" đang được khai thác thật — **đúng góc open loop của script này** |
| Không có video nào trong kết quả nhắm rõ tệp 60–80 tuổi bằng khung 「もう一つの台所」/ẩn dụ | Ẩn dụ trung tâm KHÔNG bị trùng với bất kỳ đối thủ nào tìm thấy |

⚠️ **Không suy diễn số lượng cầu** (không có "n=…", "med=…v/ngày") — đây là giới hạn thật của phiên làm việc, ghi thẳng để không lẫn với các script trước có API.

## 3. STAKE & KHUÔN

1. **MỘT ẩn dụ duy nhất:** 大腸 = 「もう一つの台所」・腸内細菌 = 台所で働く「住人／料理人」・水溶性食物繊維（もち麦）= 「仕込みの材料」・短鎖脂肪酸（酪酸など）= 「壁を直す材料・住人の燃料」. Ẩn dụ này trả lời được cả 2 câu hỏi của bài: vì sao ăn đủ mà vẫn mệt/hay ốm (bếp thiếu nguyên liệu) và vì sao ăn quá nhanh lại phản tác dụng (đầu bếp chưa quen nguyên liệu mới).
2. **Hero number có phép tính/tra cứu thật:** 厚生労働省「食事摂取基準（2025年版）」 65歳以上 mục tiêu **にじゅうグラム (nam) / じゅうななグラム (nữ)**; もち麦 ひゃくグラム chứa khoảng **じゅうにグラム** (hedge `〜とされています`, không gắn tên tổ chức vì không có nguồn xác định cho riêng con số này); tỉ lệ trộn khuyến nghị phổ biến **白米三：もち麦一**.
3. **Khuôn:** không phải countdown-nhiều-món (khác video 08/14) mà là **một-món-mổ-sâu theo cơ chế**, cùng họ với video 11 (yogurt)/12 (tofu)/19 (protein) — 3 video liền kề gần nhất (19, 20, 21) KHÔNG cùng dáng: 19 = đi ngược một ngày (夜→昼→朝) · 20 = vòng đời かさぶた · **21 = ẩn dụ không gian (台所) + đồng hồ 2 tuần thích nghi**.
4. **Chất người ≥4/6 mũi tiêm (đạt 6/6):**
   ① みのり tự trào: 「じつは私も、最初は面倒に感じていました…」
   ② nhân vật case có thoại + chi tiết đời sống vô dụng-về-thông-tin: 恵子さん「お通じの調子が、いつもすっきりしなくて」+ thói quen tưới cây/nghe radio ở tiệm; 正雄さん「今年は、まだ、風邪をひいていないんだ」+ thói quen uống trà sau giờ làm
   ③ ký ức giác quan: 「湯呑みから立つ湯気を眺める」「鉢植えに水をやりながら」
   ④ みのり tự làm: 「大さじ一杯だけなら、洗うついでに、ぱらりと入れるだけ」
   ⑤ đóng nhân vật bằng cảm xúc: 「歳のせいだと、ずっと思ってたんだけどな」そう続けて、少し照れたように、笑っておられたそうです。
   ⑥ phá nhịp ≥3 lần: 「疲れが、なかなか取れない。」「風邪を、ひきやすくなった。」「体が、だるくなる。」

**Mốc thời gian V2 (ước từ mô hình, cập nhật lại từ `subs.srt` sau render):**

| mốc | khối | luật |
|---|---|---|
| 01:14 | **ITEM1 = もう一つの台所とは大腸のこと + もち麦の名前を明かす** | payoff #1 ≤4′ ✅ (cold open 74s) |
| ~04:40 | 皆さん、こんにちは（挨拶full）+ 都道府県 CTA | phải SAU mục đầu ✅ (L3) |
| ~05:0x | みのり tự thú (mũi tiêm①④), thứ tự đã sửa: khó trước → thú nhận → kết luận | |
| 08:40 | **CTA giữa + checkpoint「に」** | **53,5%** ✅ (`cta-midvideo.md` §2.2, gần 50%) |
| ~09:2x | 腎臓×カリウム/リン cảnh báo（YMYL）| |
| 10:58 | Checkpoint「さん」ngay trước khi trả loop | |
| 11:10 | **TRẢ OPEN LOOP: 「いきなり、たくさん食べてしまうこと」+ 1週間ステップ (gồm 1 dòng もち麦 trong味噌汁, không còn là mục riêng)** | **68,9%** — dưới ngưỡng khuyến nghị 75–85%, xem §5 |
| 12:42 | anecdote 2 (正雄さん), mở bằng câu chuẩn 「例えば、こんな方も、いらっしゃいます」 | 78,3% |
| 13:58 | recap + kết 4 lớp | |
| 15:16 | disclaimer cố định | 94,1% |
| 16:13 | hết | ngắn hơn V1 ~3′ vì cắt tangent, KHÔNG vì cắt nội dung cốt lõi |

⚠️ Các mốc đánh dấu `~` là ước tính từ mô hình CPS tại thời điểm viết tài liệu này. **Bắt buộc cập nhật lại toàn bộ cột này bằng `subs.srt` thật sau khi render** (đã nhắc lại ở §11 HANDOFF).

## 4. S8 — 8 điểm cảnh báo, đã soi (V2)

Theo checklist 0c ("trang trí thì CẮT, cơ chế thì chèn số thật"): điểm dài nhất (**13 câu liên tiếp từ ~1'27**) rơi đúng vào khối giải thích ẩn dụ 台所/腸内細菌/短鎖脂肪酸 ngay sau ITEM1 — nội dung cốt lõi cần thiết để dựng ẩn dụ trước khi vào số liệu, không phải trang trí. Sau khi cắt các khối tangent ở vòng V2, các điểm S8 còn lại đều nằm trong đoạn giải thích cơ chế (miễn dịch/đường huyết) hoặc mô tả cảm xúc anecdote — không còn điểm nào nằm trong các khối liệt kê tiện ích đã bị cắt.

## 5. Ghi chú tự đánh giá V2 (trung thực, không tự chấm điểm cao)

- **Payoff lớn rơi xuống 68,9%** (từ 74,4% ở V1), dưới ngưỡng khuyến nghị 75–85% của Mục 10. Đây là **hệ quả trực tiếp và đã lường trước** của việc cắt các khối tangent sau điểm CTA (§0 mục 2) — về mặt toán học, cắt nội dung SAU payoff luôn kéo payoff SỚM hơn về mặt tỉ lệ %, dù vị trí tuyệt đối (11:10) không đổi nhiều.
- **Vì sao KHÔNG cố kéo lại lên ≥75%:** cách rẻ nhất để làm vậy là thêm lại nội dung trước payoff hoặc trước CTA — tức đúng thứ vừa bị cắt vì user chê "rời rạc". Ưu tiên yêu cầu mới của user (hook ấn tượng + nội dung liền mạch) cao hơn việc chạm đúng một ngưỡng % vốn được hiệu chuẩn từ các video ~19–22 phút, không phải video 16 phút. Nếu user muốn ưu tiên ngược lại (đúng ngưỡng 75% hơn là gọn), nói rõ để tôi thêm nội dung THẬT (không phải tangent) vào đoạn giữa — ví dụ đào sâu thêm cơ chế miễn dịch bằng 1 ví dụ cụ thể, hoặc kéo dài anecdote 1.
- **§2 không có số đo API thật** (xem cảnh báo ở đó) — nếu kênh muốn đúng quy trình `youtube-upload-seo.md` §0.5 trước khi đăng, cần chạy lại phép đo bằng token thật.
- Đã tự sửa 1 lỗi blacklist (`ということです` → `のです`) và whitelist đạt 9/15 loại (≥8 yêu cầu) — không tự chấm cao hơn số đo thật.
- **Điểm số 9–10/10 mà user hỏi: tôi không tự cho được**, vì thứ đo được retention thật chỉ có sau khi render + đăng (xem §1 để đọc lý do đầy đủ).

## 6. Bộ title A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代の落とし穴】食物繊維は摂っているのに腸が老化する人｜もち麦、大さじ一杯の差` | 41 | 食物繊維@11 | khung cảnh báo P0 + nghịch lý "ăn đủ mà vẫn lão hoá ruột", khớp khuôn video19/20 đang chạy |
| **A2** | `60歳を過ぎたら腸内環境が乱れる本当の理由｜白米に足す「大さじ一杯」の腸活` | 37 | 腸内環境@9 | đổi keyword dẫn sang cụm 腸活/腸内環境 (stake ngách rõ hơn "食物繊維" chung chung) |
| **A3** | `白いご飯だけでは、腸はもう働けません｜60代からの「もう一つの台所」の整え方` | 38 | — | đổi kiểu hook: P4 đảo nhận thức + lộ ẩn dụ trung tâm ngay ở title, test xem ẩn dụ có tự nó là hook mạnh không |

### Title CHỐT

```
【60代の落とし穴】食物繊維は摂っているのに腸が老化する人｜もち麦、大さじ一杯の差
```

**Tên file upload:** `mochimugi-daisaji1-choukatsu-60dai.mp4`

## 7. TEXT THUMBNAIL (chữ GIỐNG NHAU ở cả T1/T2/T3 — biến thử là HÌNH)

| dòng | chữ | ký | vai (gate 7 `audience-45plus` §1) | màu |
|---|---|---|---|---|
| 1 | `白米だけ？` | 5 | **① VỀ CÁI GÌ / TÌNH HUỐNG** — câu hỏi hành vi tự vấn | kem/trắng ngà |
| 2 | `腸が老化` | 4 | **② CHUYỆN GÌ XẢY RA** — hero, loss-aversion | **ĐỎ, to nhất** |
| 3 | `正解は1杯` | 5 | **③ PHẢI LÀM GÌ** — hành động cụ thể, số Ả Rập được phép ở thumbnail | **VÀNG KIM** |

- Che ảnh vẫn đọc ra: "chỉ ăn cơm trắng — ruột đang lão hoá — đáp án là 1 thìa" ✅ gate 7.
- Gate 1 (≤6 ký/dòng) ✅ · gate 3 (đúng 3 dòng) ✅ · gate 6 (nền sáng) — áp dụng khi gen ảnh.
- **Đảo biến so với video 20** (chống lặp nguyên bộ): 20 dùng khuôn TELOP/かさぶた; 21 quay lại khuôn cột chữ 3 dòng dọc (kiểu video 19) nhưng đổi màu hero từ VÀNG→**ĐỎ**, cột chữ đổi từ TRÁI→**PHẢI**, badge góc đối diện.
- Không chữ 血/透析 · không 医師/専門家 · không claim khỏi bệnh.

## 8. PROMPT ẢNH THUMBNAIL — 4 file trong `06_VIDEO/21_mochimugi-choukatsu/`

Khuôn lấy từ ảnh đã lên sóng gần nhất (video 18/19), theo `ab-3title-3thumb.md` §3.1: photorealistic, bà cụ ~68 tóc bạc ngắn + tạp dề be trên áo xanh (gương mặt kênh cố định), phòng bếp Nhật sáng ban ngày, một chén cơm trắng + một túi もち麦 làm vật đáp án, con dấu tròn ĐỎ 「食卓」, dải vàng kim mép, chữ 3 dòng 袋文字 viền nâu đậm + halo trắng.

| file | vai |
|---|---|
| `thumb_prompts_FLOW.txt` | bản DÙNG — 3 prompt, mỗi prompt 1 DÒNG, TEXT block ở ~10% đầu prompt |
| `thumb_prompts_BLOCKS.md` | bản người đọc: khung khối + bảng số đo + bảng chữ |
| `thumb_prompts_TENFILE.txt` | thứ tự dòng FLOW ↔ `thumb_T1/T2/T3_mochimugi.png` |
| `thumb_prompts_PLATE.txt` | 🛟 3 plate KHÔNG chữ (đường lui nếu kanji nát) — để RIÊNG |

**Ba bản, mỗi bản đổi ĐÚNG 1 biến:** T1 baseline (chữ cột PHẢI, bà cụ TRÁI đang múc もち麦 vào chén cơm) · T2 đổi **1 biến CROP** (close-up sát tay + muỗng もち麦 đang đổ vào chén, mặt bà cụ mờ hậu cảnh) · T3 đổi **LAYOUT** (đảo trục: chữ cột TRÁI, bà cụ PHẢI, badge góc trên-TRÁI).

Sau khi gen: soi từng ký tự (`腸`・`麦` rậm nét dễ nát) → vá watermark ✦ theo LÔ, soi 1:1 cả 4 góc → gate 168px → đặt tên `thumb_T1/T2/T3_*.png` → trần 2 MB.

## 9. QUÉT COMPLIANCE (`.claude/rules/youtube-compliance.md`)

1. **Title/thumbnail:** không có từ nhóm 殺/死/自殺/レイプ/虐待 · không có 血/透析 (chủ đề ruột không cần chạm trục máu) · không 医師が解説/医師警告. ✅
2. **Persona:** みのり không xưng 医師/管理栄養士/専門家; S7 credential = 0 điểm trong toàn bài (không riêng cold open). ✅
3. **Không tên thật** hãng/sản phẩm/người. Nguồn nêu đích danh: 厚生労働省「日本人の食事摂取基準（2025年版）」— duy nhất, còn lại đều hedge KHÔNG gắn tên tổ chức (xem §2, §3 mục 2). ✅
4. **YMYL:** 0 lần 治る/完治/薬の代わり/絶対 · cảnh báo 腎臓×カリウム/リン nói 1 lần trước điểm giữa bài + disclaimer cố định cuối video nhắc lại "食事を変える前に、必ず、かかりつけの先生にご相談ください". ✅
5. **Thumbnail** món ăn + nhân vật kênh cố định (không phải người thật cụ thể) → không cần tick synthetic cho thumbnail. Nếu SLIDE trong video dùng ảnh AI realistic (theo `youtube-compliance.md` §2.1, 2026-08-09) → **tick "altered/synthetic content"** khi upload (tool `upload_pack.py` chưa có cờ này — nhắc TAY trong METADATA.txt).
6. **Số liệu đã verify ở mức hedge phù hợp:** 65歳以上 目標量 男20g/女17g (厚労省, tin cậy cao — số phổ biến, ổn định qua các lần cải cách gần đây) · もち麦100g食物繊維12g前後 (hedge, KHÔNG gắn nguồn cụ thể vì không xác định được nguồn chính xác trong phiên này) · tỉ lệ trộn 白米3:もち麦1 (mô tả phổ biến của nhà sản xuất, hedge, không nêu tên hãng) · thời gian thích nghi hệ vi sinh ~2 tuần (hedge phổ biến trong tài liệu dinh dưỡng đại chúng, không gắn tên nghiên cứu cụ thể vì không xác định được).

## 10. TAG + HASHTAG + 概要欄

### タグ
```
60代からの食卓,シニアの健康,60代の食事,もち麦,腸活,腸内環境,食物繊維,水溶性食物繊維,便秘,免疫力,短鎖脂肪酸,酪酸,血糖値スパイク,60代 腸活,高齢者 食物繊維,もち麦 効果,もち麦 食べ方,白米 もち麦 割合,腸内フローラ,健康長寿,60歳からの健康,70代 健康,シニア 食事,健康雑学,シニアライフ,老後の健康,みのり,60代からの食卓 みのり,和食,台所の知恵
```

### 概要欄 — 3 DÒNG ĐẦU
```
「食べているのに、なぜか元気が出ない」——それは、体の中の「もう一つの台所」に、材料が届いていないサインかもしれません。
この動画では、大腸で働く見えない住人たちと、白いご飯にたった大さじ一杯足すだけの、続けやすい腸活のお話をします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ
```
「食べているのに、なぜか元気が出ない」——それは、体の中の「もう一つの台所」に、材料が届いていないサインかもしれません。
この動画では、大腸で働く見えない住人たちと、白いご飯にたった大さじ一杯足すだけの、続けやすい腸活のお話をします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。

大腸には、目に見えない菌たちが住んでいて、私たちが消化しきれなかった食べ物のカスを、毎日発酵させています。
その仕込みの材料になるのが、もち麦に多く含まれる、水に溶けるタイプの食物繊維です。
材料が足りないままだと、台所は空っぽで働き続けることになり、疲れやすさや、風邪のひきやすさにつながっているのかもしれません。

厚生労働省の「日本人の食事摂取基準（2025年版）」では、六十五歳以上の食物繊維の目標量は、男性でにじゅうグラム、女性でじゅうななグラムとされています。
もち麦は、白いご飯に大さじ一杯混ぜるだけで、無理なく続けられる、身近な選択肢の一つです。

【この動画でお話しすること】
00:00 体重は変わっていないのに、体が重い理由
01:14 大腸という、もう一つの台所の正体
04:xx 厚生労働省の目標量でみる、食物繊維の目安
09:xx ごあいさつと、大切なお願い／腸と免疫・血糖値の関係
10:xx 腎臓の治療を受けている方への注意点
11:10 多くの方が、もち麦をやめてしまう本当の理由
12:42 秋田県・正雄さんの話
13:58 今日のまとめ

【出典】
・厚生労働省「日本人の食事摂取基準（2025年版）」策定検討会報告書（食物繊維の目標量）

※この動画は、公表されている研究や公的資料をもとにした、健康に関する一般的な情報です。お一人おひとりに合わせた医療のアドバイスではありません。とくに腎臓の治療を受けている方は、食物繊維やカリウム・リンの量に、決まりがある場合があります。持病のある方やお薬を飲んでいる方は、食事を変える前に、必ずかかりつけの先生にご相談ください。

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニアの健康 #60代の食事 #もち麦 #腸活
```

⚠️ **目次のタイムスタンプは推定モデルの値です（V2 の概算）。** render 後、`subs.srt` の実際のタイムコードに置き換えること。

### 📌 固定コメント (pinned comment — ghim sau khi công khai)

```
最後まで見てくださって、ありがとうございます。案内人のみのりです。

今日お伝えしたかったのは、一つだけです。大腸には、目に見えない菌たちが住んでいて、消化しきれなかった食べ物のカスを、毎日発酵させています。その仕込みの材料になるのが、もち麦に多く含まれる、水に溶けるタイプの食物繊維です。厚生労働省の目標量は、六十五歳以上で男性にじゅうグラム、女性じゅうななグラム。もち麦は、白いご飯に大さじ一杯混ぜるだけで、その材料を届けられます。

決めごとは一つだけ。増やすのは、大さじ一杯から。いきなりたくさん混ぜてしまうと、台所で働く菌たちが驚いて、かえってお腹が張ることがあります。まずは二週間、大さじ一杯だけを続けてみてください。富山県の恵子さんも、そうして気づかれたそうです。

よろしければ、二つ教えてください。
①もち麦を続けてみて、体の調子に変化はありましたか。
②次に取り上げてほしい食べ物があれば、ぜひ。
コメントは全て読ませていただいております。皆さんの一言が、次の回の何よりの励みになります。

〔ひとつだけ、大切なお願い〕
腎臓の治療を受けている方は、食物繊維やカリウム・リンの量に、決まりがある場合があります。もち麦を始める前に、必ずかかりつけの先生にご相談ください。持病のある方、お薬を飲んでいらっしゃる方も同じです。今日のお話は、公表されている資料をもとにした一般的な健康情報で、医療のアドバイスではありません。
```

## 11. HANDOFF

```
python tools\check_coldopen.py 21              # PASS — đã xác nhận
py tools\build_slides_21.py                     # PLAN + prompt FLOW -> user gen ảnh (AI kawaii pastel, theo CLAUDE.md §①)
py tools\cutout_cast.py                         # chỉ khi thêm cast mới (nền magenta #FF00FF)
py tools\ingest_slides_21.py                    # trim viền + vá ✦ + dán khung sân khấu
py ..\remotion-vox\tools\import_pipeline.py     # slide+voice+srt → project.json
py ..\remotion-vox\tools\build_overlays_21.py   # wipe+overlay+siết phụ đề
run_full21.cmd (chạy NỀN, render-background.md) # chunk render → deliver --mp4
```

⚠️ Theo `CLAUDE.md` §②: **KHÔNG chạy `cta_inject.py`** trên đường remotion (phá phụ đề, đã bỏ từ video 20) — câu CTA giữa video đã nằm sẵn trong lời thoại `_TTS.md` (dòng 「ここまでのお話が、お役に立っているようでしたら…」).

⚠️ Sau render: cập nhật lại 目次 ở §10 bằng mốc THẬT từ `subs.srt`, và điền nốt `11:xx` (mốc hiện tại là ước từ mô hình CPS, chưa có bản render để đối chiếu).

⚠️ **CHƯA thực hiện trong phiên này** (nằm ngoài phạm vi "viết kịch bản + đóng gói CTR" mà user yêu cầu): gen ảnh AI, cutout cast, render video, đo trend bằng API thật. Đây là kịch bản + gói CTR sẵn sàng để đưa vào pipeline sản xuất khi user quyết định render.
