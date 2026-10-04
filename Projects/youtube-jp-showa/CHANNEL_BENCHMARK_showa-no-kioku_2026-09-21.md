# CHANNEL_BENCHMARK — 昭和の記憶 (3 video user tải về, mổ 2026-09-21)

> Nguồn: `C:\Users\tuana\Downloads\Showa` — 3 file mp4 720p/24fps. Mọi số dưới đây **đo bằng máy từ chính file**
> (ffmpeg/numpy) hoặc từ **YouTube Data API**. Đối chiếu kênh mình: `06_VIDEO/16_omiai-kekkon/16_omiai-kekkon.mp4`
> (17:47, chưa đăng) + 15 video đã đăng.
> Đọc cùng: `CHANNEL_BENCHMARK_stills_2026-09-08.md` (2 kênh ảnh-tĩnh 191–232K) · `CHANNEL_DIAGNOSIS_2026-09-03.md` ·
> `05_SCRIPT_FORMULA.md` · `.claude/rules/audience-45plus.md` §2.0-ter.

## 0. KẾT LUẬN 1 DÒNG

Kênh này **không hơn mình ở kỹ thuật** — nó dùng cùng một công cụ (t2v photoreal), độ dài NGẮN HƠN một nửa,
ít lớp hơn (0 badge, 0 thẻ chữ, 0 sơ đồ), SEO gần như không có (4 tag lặp, 0 目次).
Nó hơn mình ở **3 thứ, và cả 3 đều đo được**:

1. ⭐⭐ **ĐƠN VỊ ĐỀ TÀI**: nó bán **MỘT KHOẢNG THỜI GIAN RIÊNG TƯ ai cũng từng sống** (夏休み・日曜日・修学旅行・遠足・好きな人・子どもの部屋).
   Chính kênh nó chứng minh cái ngược lại chết: mọi video về **VẬT / CHẾ ĐỘ / DANH MỤC** (給食・校則・朝礼・部活・学ラン・駄菓子屋・特撮) đều **431–5.400 view**.
   🔴 **15/15 video của mình nằm đúng trong cái rổ chết đó.**
2. ⭐ **KIẾN TRÚC = MỘT NGÀY KỂ THEO THỨ TỰ**, không phải danh sách 「◯選」. 11 chương × ~47 giây, mỗi chương một khoảnh khắc ngũ quan.
3. ⭐ **KHUNG HÌNH SỐNG**: chỉ **3,3–3,8% khung đứng yên**; của mình **42,1%**. Và **không có vignette** (viền/tâm 0,88–1,00 vs **0,61** của mình).

⚠️ **Ba giới hạn của phép đo, đọc trước khi coi là nhân quả:** ① **kênh nó cũng chủ yếu FLOP** — trung vị **5.275 view**, chỉ **6/35 video** vượt 75K;
tức đây là mẫu "top 10% gánh kênh" đúng như `youtube-suggested-growth.md` §0, không phải "công thức nào cũng nổ"
② **không có Analytics của nó** — mọi số dưới đây là *chữ ký sản xuất + phân bố đề tài*, KHÔNG phải retention
③ n = **1 kênh**. Trong ngách 昭和 đã đo được **hai công thức hình trái ngược nhau cùng thắng** (ảnh tĩnh giữ 16–18s ở
`CHANNEL_BENCHMARK_stills_2026-09-08.md` · clip động liên tục ở đây) ⇒ **lớp hình không phải biến quyết định**; đề tài thì có.

---

## 1. SỐ CỦA KÊNH (API, 2026-09-21)

`昭和の記憶` · `UCmv9P_aGds57GmaeUQp7e6g` · lập **2026-02-07** (7,5 tháng) · **5.870 sub · 35 video · 1.154.939 view** · cat **24** · 4 tag lặp cho mọi video.

| | 昭和の記憶 | **昭和くらし図鑑 (mình)** |
|---|---|---|
| tuổi kênh | 7,5 tháng | 1,1 tháng |
| video | 35 | 15 |
| sub | 5.870 | **26** |
| tổng view | 1.154.939 | **10.482** |
| trung vị view/video | **5.275** | **169** |
| trung vị view/ngày | 59 | ~10 |
| video >75K | **6** | 0 |
| trung vị độ dài | **6,8 phút** | **15,2 phút** |
| bình luận / 1.000 view (trung vị) | **3,11** | ~0,5 |

⭐ **Tỉ số view/sub của video hit = 24–33×** ⇒ theo ngưỡng `youtube-suggested-growth.md` §2 (≥3×) thì đây là
**GROWTH VIDEO mạnh nhất từng gặp trong ngách này** — và `01_SWIPE_TITLES.md` hiện **không có một mục nào của kênh này**. Phải nạp.

### 1.1 🔴🔴 BẢNG QUYẾT ĐỊNH — 35 video của nó, xếp theo view/ngày

| view/ngày | view | dài | title | rổ đề tài |
|---|---|---|---|---|
| **2.786** | 181.099 | 9:02 | 昭和の夏休み、祖父母の家で過ごしたあの時間 | 🟢 thời gian riêng tư |
| 2.670 | 5.340 | 8:27 | 昭和50年代の男の子の部屋｜机の引き出しには宝物があった | 🟢 (mới 2 ngày) |
| **1.642** | 75.538 | 5:15 | 昭和の「好きな人」は、今よりずっと特別だった | 🟢 |
| **1.484** | 195.909 | 19:54 | 昭和の夏休みは、今よりずっと長く感じた | 🟢 |
| **1.209** | 137.855 | 5:24 | 昭和の女の子の部屋には、秘密の時間があった | 🟢 |
| **967** | 141.200 | 6:15 | 昭和の日曜日には、今では忘れた楽しさがあった | 🟢 |
| 925 | 35.158 | 16:15 | 昭和の家族旅行は、出発する前から楽しかった | 🟢 |
| **794** | 127.057 | 6:15 | 昭和の修学旅行、今とは違いすぎた5つの定番 | 🟢 |
| **616** | 85.622 | 8:17 | 昭和の遠足は、なぜあんなに楽しかったのか | 🟢 |
| 615 | 9.835 | 8:02 | 昭和の夕飯には、家族が集まる時間があった | 🟢 |
| 403 | 12.082 | 7:16 | 昭和の夏休みの終わりは、なぜあんなに寂しかったのか | 🟢 |
| 317 | 33.602 | 6:57 | 昭和のデパートは、特別な場所だった | 🟢 |
| 284 | 2.554 | 6:46 | 昭和の誕生日は、小さなケーキでも特別だった | 🟢 |
| 214 | 43.835 | 8:50 | 昭和の女子高校生｜制服はここまで変わった | 🟡 vật/danh mục |
| … | … | … | … | |
| 29 | 5.335 | 6:01 | 昭和の先生｜今では考えられない厳しさ | 🔴 chế độ |
| 21 | 3.659 | 4:47 | これが昭和の給食でした | 🔴 vật |
| 20 | 4.005 | 5:16 | あの日の学ラン｜長ラン、ボンタン、リーゼント | 🔴 vật |
| 17 | 1.968 | 2:45 | 昭和の駄菓子屋には、10円玉で楽しめる世界があった | 🔴 vật |
| 15 | 2.478 | 4:31 | 昭和の部活は、今では考えられないほど厳しかった | 🔴 chế độ |
| 13 | 1.974 | 5:22 | 昭和の朝礼は、今では考えられなかった | 🔴 chế độ |
| 10 | 764 | 9:35 | 昭和の特撮ヒーローは、なぜ子どもたちを熱狂させたのか | 🔴 danh mục |
| 8 | 1.291 | 5:10 | 今では考えにくい 昭和の校則トップ5 | 🔴 chế độ |
| **3** | 431 | 6:05 | 昭和のだんじり祭りには、町中が一つになる夜があった | 🔴 lễ hội vùng |

🔴 **CÙNG một khuôn hình, cùng một giọng, cùng một cách viết title — chênh 900×.** Biến duy nhất đổi là **ĐỀ TÀI**.
Nó đã thử đúng rổ đề tài của mình (給食・校則・朝礼・部活・学ラン・駄菓子屋・先生) và **rổ đó chết trên kênh nó**.

**Ranh giới rõ ràng:**
- 🟢 **THẮNG = một KHOẢNG THỜI GIAN mà người xem là NHÂN VẬT CHÍNH** — 夏休み, 日曜日, 修学旅行, 遠足, 家族旅行, 好きな人, 自分の部屋, 夕飯, 誕生日, デパートに行く日.
- 🔴 **CHẾT = thứ được ÁP LÊN người xem** — 給食, 校則, 朝礼, 部活, 先生, 制服 — cộng vật thuần (駄菓子屋, 学ラン) và văn hoá vùng (だんじり).
- Phép thử 5 giây: **「あれは自分の時間だったか、それとも与えられた時間だったか」**. 自分の時間 → làm. 与えられた → bỏ.

### 1.2 Khuôn TITLE của nó — câu văn trần, 0 số, 0 選, 0 【】

| | nó | mình |
|---|---|---|
| dạng | **câu kể có vị ngữ cảm xúc** | 【mốc】+ mệnh đề gap + `N選` + ｜liệt kê + 【昭和100年】 |
| dài | **17–28 ký** | **50–68 ký** |
| tag 【】 | **0/35** | 15/15 |
| số / `◯選` | **1/35** (5つの定番) | 15/15 |
| chủ ngữ | 「昭和の◯◯」 + **は/には** | tên vật/chế độ |

4 khuôn vị ngữ của nó, đều là **so sánh cảm xúc với hôm nay**:
`〜は、今よりずっと◯◯だった` · `〜には、◯◯があった` · `〜は、なぜあんなに◯◯だったのか` · `〜は、今とは違いすぎた`

⚖️ **ĐỪNG bê nguyên**: `youtube-upload-seo.md` §2.1 đòi keyword trong 5–7 từ đầu, và số đo Analytics của cụm mình
cho thấy **search vẫn cấp view** (`youtube-suggested-growth.md` §0). Title của nó **không có keyword đo được nào**
ngoài `昭和` — nó sống 100% bằng browse/suggested. Đường an toàn: **bỏ `N選` + bỏ 【】 đầu, giữ `昭和の◯◯` làm keyword dẫn,
đuôi giữ 1 tag SEO** → `昭和の夏休みは、今よりずっと長かった【昭和100年】` (26 ký, keyword `昭和の夏休み` ở vị trí 1).

---

## 2. LỚP HÌNH — bảng số đo (phần đắt nhất của lượt mổ)

Đo 4fps. `MAD blur` = làm mờ σ=2 để **bỏ hạt phim**, còn lại là **chuyển động thật**. `tiny32` = 32×18px, chỉ còn bố cục.

| | HO 9:02 (181K) | HO 6:15 (141K) | HO 19:54 (196K) | **MÌNH 16 (17:47)** |
|---|---|---|---|---|
| MAD160 sharp | 20,79 | 23,55 | 20,96 | **6,54** |
| **MAD160 blur = chuyển động thật** | **11,60** | **12,83** | **10,84** | **4,87** |
| hạt phim (std high-pass) | 25,05 | 21,69 | 21,43 | 18,06 |
| MAD tiny32 TB | 11,92 | 13,21 | 11,05 | **5,23** |
| **% khung ĐỨNG YÊN (tiny32 <2,0)** | **3,8%** | **3,3%** | ~3% | 🔴 **42,1%** |
| cắt/phút (tiny32 TH25) | 21,6 | 28,5 | — | **10,1** |
| cắt/phút (TH35) | 13,1 | 16,0 | — | **4,3** |
| giữ mỗi cảnh p50 (TH45) | 5,00s | 5,00s | — | 6,00s |
| sáng TB | 93,0 | 98,8 | 91,6 | 88,1 |
| **viền/tâm (vignette)** | **0,93** | **1,00** | **0,88** | 🔴 **0,61** |
| R−B | +20,4 | +23,1 | +22,1 | **+26,0** |
| **G (kênh xanh)** | **95,4** | **98,5** | **93,1** | 🔴 **84,6** |
| bão hoà | 36,2% | 32,7% | 35,8% | 34,6% |
| contrast (std luma) | 60,9 | 60,3 | 60,1 | 63,2 |
| LUFS tích hợp | −21,4 | −21,3 | — | **−14,5** |
| LRA | 4,4 | 5,1 | — | 3,0 |
| true peak | −4,5 | −4,5 | −3,2 | 🔴 **−1,0** |

⚠️ **Bẫy phép đo đã dính trong lượt này, ghi để không lặp:** `ffmpeg scdet` trả **450–1.255 cắt/phút** ở MỌI ngưỡng
0,05→0,40 trên 3 video của nó — **số rác**, vì camera động liên tục nên mọi frame đều khác frame trước.
⇒ Ở lô footage động, **scdet vô dụng**; phải đếm cắt bằng **MAD tiny32 vượt ngưỡng cao**, và phải báo **2 ngưỡng**
(chuyển mềm dissolve không tạo đỉnh đơn). Cùng họ `feedback_nguon_da_bi_bien_doi_truoc_khi_do`, lần thứ 5.

### 2.1 🔴 BỐN LỖI ĐO ĐƯỢC CỦA LỚP HÌNH BÊN MÌNH

**① 42,1% khung của mình ĐỨNG YÊN — đây chính là chữ "đơ" user nói từ 2026-09-06.**
Nó là **3,3–3,8%**. Chuyển động thật của nó gấp mình **2,4–2,6 lần** (MAD blur 11,6–12,8 vs 4,87).
⇒ Không phải lỗi grade, không phải lỗi nhịp cắt — **lỗi ở chính CLIP**: gần một nửa thời lượng là clip t2v gen ra
gần như tĩnh. Luật ACT ở `04_VIDEOGEN_PROMPTS.md` đòi "đúng 2 `then`" + "≥1 chuyển động phụ" — luật đó **đang không
được thi hành đủ**, hoặc nó đo sai thứ (**có `then` trong prompt ≠ có chuyển động trong clip**).
🔧 **Gate còn thiếu, và nó rẻ nhất trong cả lượt này:** `review_clips.py` soi 4 frame bằng MẮT, **chưa hề đo động**.
Thêm đúng một phép: clip nhận vào phải có **MAD blur ≥8** và **% khung đứng yên ≤10%**; rớt thì gen lại, đừng đưa vào SLIDES.
(Ngưỡng lấy từ 3 bản thắng, không phải số bịa.)

**② VIGNETTE 0,61 — khác biệt thị giác LỚN NHẤT, và nó nằm đúng một chỗ trong code.**
`tools/grade_showa.py` có `vignette=PI/5.2` (preset `showa16`), `PI/4.2` (`showa70`), `PI/3.8` (bản đậm).
Nó là **0,88–1,00 = gần như không vignette**.
🔴 **Nguyên nhân gốc, đáng ghi:** docstring của `grade_showa.py` ghi rõ mục tiêu là *"phim tư liệu THẬT (Japan Today 1959):
luma 66 · contrast 50 · sat 62 · grain 17,8"*. Mốc đó **đúng cho thời REAL-FIRST** (clip phim PD thật, hết hiệu lực 2026-09-04).
Sau khi đổi sang **100% t2v**, mốc tham chiếu lẽ ra phải đổi theo — **nhưng không đổi**. Đây đúng là bài học
*"đổi engine dựng hình thì phải rà lại mọi thứ neo vào engine cũ"* (`CLAUDE.md` §Visual), lần này thứ bị neo là **một con số hiệu chuẩn**.
⇒ Kênh đang thắng bằng AI **không** giả làm phim 1959; nó là **phim hiện đại kể về 昭和**.

**③ Kênh XANH bị bóp — đó là thứ làm khung của mình ra "nâu giấy cũ".**
G của mình **84,6** vs **93,1–98,5**. R−B thì gần như nhau (+26 vs +20…+23) ⇒ **không phải "ấm hơn", mà là "xanh chết".**
Cây cối, đồng lúa, trời — ba thứ chở nostalgia mạnh nhất — đều thành nâu. Thủ phạm: `eq=saturation=0.70…0.86` + `colorbalance` đè lên G.
📌 Bão hoà TỔNG thì gần bằng nhau (34,6 vs 32,7–36,2) — nên **đo bão hoà tổng sẽ KHÔNG bắt được lỗi này**; phải đo **G riêng**.

**④ true peak −1,0 dBFS — vi phạm luật của chính mình** (`audience-45plus.md` §2.0-quater mục 5: ≤−3 dBTP). Nó để −4,5.
⚖️ Nhưng **ĐỪNG copy LUFS của nó**: nó xuất **−21,4 LUFS**, YouTube không kéo lên ⇒ tệp 65+ phải tự tăng loa.
**−14,5 của mình là ĐÚNG** (`project_loudness_14_lufs`). Chỉ hạ peak, không hạ LUFS.

### 2.2 LỚP CHỮ — nó tiến hoá, và bản mới nhất là bản thắng nhất

| | 6:15 (Apr, 141K) | 19:54 (May, 196K) | **9:02 (Jul, 181K — mới nhất)** |
|---|---|---|---|
| phụ đề | **1,9% khung = KHÔNG CÓ** | 0,8% = KHÔNG CÓ | **97,0% = ĐẦY ĐỦ** |
| chương (dải trên) | 2,0% · 4 lần | 6,8% · 22 lần | 7,2% · **15 lần** |
| view/ngày | 967 | 1.484 | **2.786** |

⇒ **Bản có phụ đề đầy đủ là bản mạnh nhất theo view/ngày.** Tức phụ đề **không** phải thứ phải bỏ —
`audience-45plus.md` §3 (phụ đề cháy sẵn) **giữ nguyên**, khỏi phải bàn.

**Đặc tả lớp chữ của bản 181K (đo trên frame 720p):**
- **Phụ đề**: trắng đậm 袋文字 viền đen dày, **CĂN GIỮA**, 1–2 dòng, y ≈ **600–700 / 720 (83–97%)**, cao ~38px = **5,3% khung** (≈57px ở 1080).
- **Chip chương**: **VÀNG** đậm 袋文字, **góc trên-TRÁI** (x≈30, y≈20–70), hiện **~2,5–3 giây** ở đầu mỗi chương rồi tắt.
- ⭐ **0 vật cố định**: không watermark, không logo, không mascot, không thanh tiến độ. **Mình có badge vàng 「くらし図鑑」 góc trên-PHẢI trên 100% khung** —
  đúng cái `audience-45plus.md` §2.0-quater mục 4 gọi là *vật cố định không chở thông tin nào của bài*.

---

## 3. KIẾN TRÚC BÀI — 11 CHƯƠNG × 47 GIÂY, KỂ THEO MỘT NGÀY

Đọc được **nguyên bộ chương** của bản 181K từ chip vàng:

| mốc | chip chương |
|---|---|
| 0:01 | 田舎の祖父母の家 |
| 0:46 | 祖父母の家へ向かう道 |
| 1:29 | 玄関を開けた瞬間 |
| 2:24 | 縁側とスイカと麦茶 |
| 3:16 | 親戚の子どもたちと遊ぶ |
| 4:05 | 祖母の台所と昼ごはん |
| 4:52 | 昼下がりの静けさ |
| 5:36 | 夕方の風呂と蚊取り線香 |
| 7:13 | 帰る日の寂しさ |
| 8:10 | 昭和の夏休みの特別な時間 |

⭐⭐ **Đây là MỘT NGÀY kể theo thứ tự thời gian, không phải danh sách.** Đường đi: *lên đường → tới → sáng → trưa → chiều → tối → ngày về*.
**Chip chương là DANH NGỮ đặt tên một khoảnh khắc ngũ quan**, không phải mục số, không phải fact, không có mốc năm.

🔴 **Vì sao cái này thắng 「◯選」 trên rail đề xuất:** danh sách có **điểm thoát tự nhiên** — xem hết món mình cần là đi.
Một ngày kể theo thứ tự **không có điểm thoát**: bỏ giữa bài là bỏ dở buổi chiều. Nó không cần open-loop nào ngoài *"trời sắp tối"*.

**Số đo nhịp**: phụ đề chạy thành **11 khối ~42–55 giây**, giữa hai khối là **~2 giây KHÔNG CÓ CHỮ** —
tức **một nhịp lặng có chủ ý ở mỗi ranh giới chương**, đúng chỗ chip vàng hiện lên.

### 3.1 COLD OPEN — đọc nguyên văn từ phụ đề (bản 181K)

```
0:00  昭和の夏休みには／祖父母の家で過ごす／特別な時間がありました。
0:08  電車やバス、車に揺られて向かった田舎の家。
0:13  玄関を開けた瞬間の匂い。
0:18  親戚の子どもたちと遊んだ一日。
0:23  今思えば、何か大きな出来事があったわけではありません。
0:28  でも、なぜか／忘れられない夏の記憶があります。
0:33  今回は、そんな昭和の夏休み……
0:38  特別な場所ではないのに、子どもの頃は
0:43  そこだけ時間の流れが違って感じましたよね。
0:50  まず思い出すのは／祖父母の家へ向かう道です。   ← vào chương 1
```

**Bốn thứ nó làm mà khuôn E7 của mình KHÔNG có:**
1. ⭐ **Vòng lặp NGHỊCH LÝ về chính KÝ ỨC** (0:23→0:28): *「何か大きな出来事があったわけではありません。でも、なぜか忘れられない」*
   — phủ định kỳ vọng rồi lật lại. Nó không hứa thông tin, nó hứa **giải thích một cảm giác người xem đang có sẵn**.
   Khuôn E7 của mình hứa **cú sốc + chứng cứ** (`これ、実話です`+証人) — đúng cho trục 常識, **sai cho bài kể-ngày**.
2. ⭐ **`〜ましたよね` — câu hỏi xác nhận** (0:43), kéo người xem thành **người cùng làm chứng**, không phải người nghe giảng.
3. **3 mảnh ngũ quan RỜI RẠC, mỗi câu một dòng, không nối logic** (0:08–0:18) — 揺られて向かった / 開けた瞬間の匂い / 遊んだ一日.
   Nó không giải thích gì trong 20 giây đầu, chỉ **gọi tên mùi và tiếng**.
4. ⛔ **0 lời chào, 0 tên người dẫn, 0 tên kênh** trong cả cold open.

📌 **Vào chương 1 ở 0:50** — đạt gate 「≤60s」 của kênh mình, nhưng bằng đường hoàn toàn khác.

---

## 4. THUMBNAIL

Của nó (3 hit): **1 ảnh full-bleed** · **hero 2 dòng CỰC TO** (mỗi dòng ~25–30% chiều cao) · vàng+trắng 袋文字 viền đen dày,
1 bản thêm đỏ · chữ nửa khung, người nửa còn lại · **≥1 mặt biểu cảm rõ, gần** (bé ngoái lại, ông bà vẫy tay, bé ngồi trước TV) ·
**0 chip, 0 burst, 0 banner năm, 0 số, 0 選** · nền **sáng, nắng, trời XANH, cây XANH**.

Hero của nó là **MỆNH ĐỀ CẢM XÚC NGÔI THỨ NHẤT**: `帰りたく／なかった` (7 ký) · `日曜日／だけの／楽しみ` · `昭和の／夏休み`.

| | nó | mình (K-COLLAGE, video 14 — bản 4.936 view) |
|---|---|---|
| ô ảnh | **1**, full bleed | **3 ô collage** |
| khối chữ | **2** (hero 2 dòng + 1 dòng phụ nhỏ) | **4** (banner năm + trắng 2 dòng + hero đỏ + burst 5選) |
| mặt người đọc được | **có, gần** | 🔴 **không** (0/7, đã ghi ở `CHANNEL_DIAGNOSIS_2026-09-03` §3 lỗi 3) |
| bão hoà (đo) | **46,0 / 50,4 / 63,9%** | **42,2%** |
| R−B (đo) | +37 / +64 / +73 | +40,6 |
| hero là gì | mệnh đề cảm xúc | 🔴 **danh từ nhãn** 「昭和の職場」 |

⇒ Xác nhận độc lập **4/6 lỗi** mà `CHANNEL_DIAGNOSIS_2026-09-03.md` §3 đã tự bắt (hero danh từ · 0 người · tông nâu · nhiều khối phụ).
Cái **mới** là số: **bão hoà của nó cao hơn mình 4–22 điểm**, và **1 ảnh thắng 3 ô collage** ở đúng ngách này.

⚠️ **Phép đo chiều cao hero THẤT BẠI** trên cả 4 ảnh (mask pixel tối bắt luôn bóng trong ảnh → trả 99,9% khung).
Đây đúng là giới hạn đã ghi ở `audience-45plus.md` §6.10 (*gate tỉ lệ chỉ đo được khi hero khác màu nền*) ⇒
số "25–30%" ở trên là **duyệt bằng MẮT**, không phải số máy. Đừng chép nó vào gate.

---

## 5. NÓ KHÔNG LÀM GÌ — và mình đang trả giá cho những thứ đó

| lớp mình có | nó | đọc |
|---|---|---|
| 目次 + mô tả 200–300 từ + SEO đầy đủ | **0 目次**, mô tả = **văn xuôi cảm xúc + 1 câu hỏi**, 4 tag lặp | nó sống bằng browse; SEO không phải nguyên nhân nó thắng — **nhưng cũng đừng bỏ SEO của mình** (`youtube-suggested-growth.md` §6 mục 3) |
| badge 「くらし図鑑」 100% khung | 0 vật cố định | ⇒ **BỎ badge** (`audience-45plus.md` §2.0-quater mục 4) |
| 15,2 phút | **6,8 phút trung vị**, 4/7 hit **<6:20** | ⇒ độ dài **không** phải điều kiện; 14,5–18′ đang tốn ~2,5× công/video mà không có bằng chứng đỡ |
| mốc năm ≥8 lần/bài + nguồn cấp 1 | hit của nó **gần như 0 mốc năm** | ⛔ chỉ đúng cho **bài kể-ngày**; trục B (YMYL tiền) **giữ nguyên luật nguồn** |
| grade "phim 1959" | grade nhẹ, không vignette | ⇒ đổi mốc hiệu chuẩn |

⭐ **Một thứ NÓ có mà mình không có, rẻ nhất trong cả lượt này:**
**MỘT CÂU HỎI DUY NHẤT, CỤ THỂ, đặt ở cuối mô tả VÀ (theo mô tả) ở cuối video** —
`あなたは、祖父母の家でどんな夏休みを過ごしましたか？` · `ラジオ体操、虫取り、川遊び、夜店、宿題の追い込み。ぜひコメントで教えてください。`
⇒ **3,11 bình luận/1.000 view** (mình ~0,5). Câu hỏi của nó hỏi **một kỷ niệm người ta ĐÃ CÓ**, không hỏi "bạn nhớ được mấy điểm".

---

## 6. VIỆC PHẢI LÀM — xếp theo (đòn bẩy ÷ công)

### 6.1 Rẻ + đòn bẩy cao nhất — làm ngay ở video kế
1. ⭐⭐ **ĐỔI RỔ ĐỀ TÀI sang「một khoảng thời gian riêng tư」.** 12 đề tài đã được chính nó chứng minh, mình chưa làm cái nào:
   夏休み · 日曜日 · 修学旅行 · 遠足 · 運動会の前の日 · 家族旅行 · 初恋／好きな人 · 自分の部屋 · 夕飯の時間 · 誕生日 · デパートに行く日 · 夏休み最後の日.
   ⛔ Và **dừng cấp slot cho rổ 物/制度** (給食・教室・商店街・駄菓子屋・通学路・職場・校則) — 15/15 video của mình ở rổ đó, và rổ đó chết cả trên kênh nó.
2. ⭐ **BỎ badge 「くらし図鑑」** khỏi mọi khung (1 cờ trong renderer).
3. ⭐ **HẠ vignette về ~0** (`vignette=PI/9` hoặc bỏ hẳn) và **NÂNG G**: `eq=saturation` 0,86 → **0,95–1,00**, bỏ phần `colorbalance` đè kênh G.
   Mục tiêu đo được: **viền/tâm ≥0,88 · G ≥93 · bão hoà 33–36%**. ⛔ Giữ hạt phim (mình 18,06 đã gần nó 21–25).
4. ⭐ **Hạ true peak về ≤−3 dBTP**, giữ nguyên −14 LUFS.
5. ⭐ **Thêm 1 câu hỏi kỷ niệm cụ thể** ở cuối video + cuối 概要欄 (không phải 「何点覚えていますか」).

### 6.2 Trung bình — áp từ video kế
6. ⭐⭐ **Kiến trúc 「MỘT NGÀY kể theo thứ tự」** cho trục A: **10–12 chương × ~45–50 giây**, chip chương = **danh ngữ ngũ quan**,
   **~2 giây lặng** ở mỗi ranh giới chương. Đây là **động cơ thứ ba**, cạnh `E-SCENE`/`E-LIST` của `05_SCRIPT_FORMULA.md` §5.2 — gọi nó là **`E-DAY`**.
7. ⭐ **Cold open đổi khuôn cho bài `E-DAY`**: 3 mảnh ngũ quan rời → **nghịch lý ký ức** (「大きな出来事はなかった。でも、なぜか忘れられない」)
   → **`〜ましたよね`** → vào chương 1 ≤50s, **0 lời chào**. (Khuôn E7 hiện tại **giữ nguyên cho trục 常識/B**.)
8. ⭐ **Rút độ dài xuống 7–10 phút** cho bài `E-DAY` — trả bằng **ít chương hơn**, không bằng chương ngắn hơn.
   ⚖️ Ngược luật độ dài đang chốt (14,5–18′) ⇒ đề nghị **chạy 3 video E-DAY ở 8–9′** rồi so AVD với lô 15′.
9. ⭐ **Thumbnail: thêm khuôn `K-DAY`** — 1 ảnh full-bleed + hero 2 dòng là **mệnh đề cảm xúc ngôi 1** + **1 mặt gần, biểu cảm rõ** +
   **0 chip/0 burst/0 số**, nền nắng-trời-xanh, bão hoà ≥46%. Chạy làm **T3** trong bộ 3×3 để đối chứng K-COLLAGE (`ab-3title-3thumb.md` §3).
10. ⭐ **Title: bỏ `N選` + bỏ 【】 mở đầu**, dùng `昭和の◯◯は、今よりずっと〜だった` (≤28 ký), giữ 1 tag SEO ở đuôi.

### 6.3 Gate máy còn thiếu (luật kiểm bằng mắt thì sẽ trôi)
11. 🔧 **Gate ĐỘNG cho từng clip t2v** — thêm vào `tools/review_clips.py`: mỗi clip phải **MAD blur ≥8** và **% khung đứng yên (tiny32<2,0) ≤10%**.
    Ngưỡng lấy từ 3 bản thắng (11,6–12,8 / 3,3–3,8%). Bản 16 của mình sẽ **rớt** — đó là điểm của gate.
12. 🔧 **Gate GRADE**: sau grade, đo lại **viền/tâm ≥0,88 · G ≥93** trên mẫu 20 clip. `grade_showa.py --measure` đang so với
    mốc "phim 1959" — **đổi mốc tham chiếu sang 3 video này** và ghi rõ trong docstring vì sao mốc cũ hết hiệu lực.
13. 🔧 **Nạp `01_SWIPE_TITLES.md`**: 6 hit của kênh này là GROWTH VIDEO 24–33× — sổ đang **rỗng phần GROWTH**.

### 6.4 ⛔ KHÔNG áp
- **Bỏ phụ đề** — 2/3 hit không có, nhưng **bản có phụ đề là bản mạnh nhất**, và `audience-45plus.md` §3 là luật cứng.
- **LUFS −21** — hại tệp 65+; giữ −14.
- **Bỏ SEO/目次/tag** — nó sống bằng browse, mình **chưa** (search vẫn cấp view ở cụm mình).
- **Bỏ mốc năm / nguồn cấp 1 ở trục B** — YMYL tiền không đổi.
- **Coi lớp hình là biến quyết định** — ngách này có **hai công thức hình trái ngược nhau cùng thắng** (§0 ⚠️③).

## 7. PHANH
3 video chạy `E-DAY` (đề tài 時間 riêng tư + 8–9′ + grade mới + K-DAY) mà **trung vị view/video không vượt lô 15 video hiện tại (169)**
→ trả về khuôn cũ và ghi vào `08_ANALYTICS_LOG.md`. Kênh đang **26 sub / trung vị 169 view**, nên mẫu sẽ nhỏ —
đọc thêm **impressions/video** và **nguồn browse có mở hay không**, đừng đọc riêng view.
