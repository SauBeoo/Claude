# 19 — たんぱく質：三回だけ開くゲート（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **たんぱく質 × 朝の空白 × 「一日三回しか開かないゲート」（工事現場の比喩）**
- **Bản đọc chuẩn:** `19_tanpakushitsu-asa_TTS.md` — **4.818 ký (thuần) · 225 dòng · ước 19′11** (mô hình CPS 4.40 + GAP 0.25/dòng). ⚠️ **NGOÀI dải 21–25′ của kênh — user chốt 2026-08-25 rút xuống <20′**, xem §0. Sửa lời thì sửa file này **và** quét lại `match` trong SLIDES khi có.
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 19` → ✅ **PASS, cold open 81 giây** (L1–L5 · S6 · S7 sạch, dư 9s so trần 90s) · **35 tag** (base `[しっとり][速0.8]` + 34 nhấn nhá, gồm 1 đỉnh bài `[間1.2][速0.8][後間1.0]`) · 0 tag giữa câu · 0 tag đứng dòng riêng ngoài base · blacklist Mục 7 = 0 · whitelist 11 loại · 7 câu 「〜ませんか」 (L5 cần ≥3) · S8 11 điểm (cảnh báo, không chặn) — **đã duyệt bằng mắt từng điểm, KHÔNG nhồi số để xanh gate**, xem §4.

---

## 0. ✂️ VÒNG CẮT — 22′51 → 19′11 (user chốt 2026-08-25: *"rút ngắn xuống dưới 20 phút"*)

⚠️ **Đi ngược phép đo của chính kênh, ghi thẳng để sau đọc số không lẫn nhân quả.** `CHANNEL_DIAGNOSIS_2026-08-11` đo được: cắt video 納豆 từ 29′ xuống 15′ làm **AVD phút TỤT 4′33 → 3′11**, và tích phân đường cong cho thấy cắt xuống 5 phút vẫn chỉ 43,5% — tức **độ dài không phải nút thắt**, nút thắt là cửa tử giây 20→40. `CLAUDE.md` §① vì vậy khoá dải 21–25′. Bản này nằm **ngoài dải** theo yêu cầu của user. Nếu AVD phút của video 19 thấp hơn video 17/18 thì **đây là biến đầu tiên xét lại**, không phải cold open (cold open giữ nguyên 81 giây, không đụng).

**Nguyên tắc cắt đã dùng — bỏ khối RỜI khỏi ẩn dụ trung tâm, không cắt phần đang chở mạch** (bài học §0c của video 18: 4 khối bị nhồi vào chỉ để đủ ký tự chính là thứ làm bài đọc như trang tạp chí):

| # | khối bị cắt/rút | ký | vì sao chọn nó |
|---|---|---|---|
| 1 | 「夏は筋肉が落ちやすい季節」 (cắt hẳn) | ~200 | phụ đề theo mùa, **không nằm trong ẩn dụ ゲート** — rời nhất trong bài |
| 2 | 「体を動かしてみてください」 (cắt hẳn) | ~120 | kéo thêm một chủ đề MỚI (vận động) vào một bài về ĂN |
| 3 | khối 「じゅうごパーセント以上」+「体重あたり」 | ~150 | lớp `genten` vẫn còn nguyên (厚労省 2025年版 + 推奨量 60g/50g) — chỉ bỏ con số thứ hai |
| 4 | 指輪っかテスト (rút, giữ phép đo) | ~130 | gộp 3 mức kết quả, bỏ câu lặp — **giữ nguyên phần "làm ngay trên ghế"** |
| 5 | FAQ プロテイン (rút còn 3 câu) | ~130 | giữ đúng câu dẫn vào 「冷蔵庫の扉」 |
| 6 | 3 câu trang trí ở 2 anecdote + đoạn tự thử của みのり | ~120 | giữ đủ thoại + chi tiết đời sống (mũi tiêm ②③④ còn nguyên) |
| 7 | しらす 3g · 「高い食品を買うことではありません」 · 「一つの食材に頼らない」 | ~100 | 3g là con số yếu nhất bài; 2 câu kia trùng ý với FAQ プロテイン đứng trước |
| 8 | 「この場所では…」 · 「最後にもう一度、申し上げます」 · 「そういう仕組みだと」 | ~90 | câu nối thừa; disclaimer cuối vẫn nhắc lại cảnh báo 腎臓 |

🔴 **Một khối được DỜI chứ không cắt** — 「六十代を過ぎると、お肉は重たい…たんぱく質はお肉だけのものではありません」 chuyển từ SAU payoff lên **TRƯỚC** nó. Hai lý do: ① mạch tốt hơn hẳn (bữa sáng thiếu → thịt thì nặng bụng → *vậy phải mua bột đạm à?* → không, đáp án rẻ và có sẵn → payoff) ② nó kéo **payoff từ 72,7% lên 75,4%**, vừa đủ ngưỡng "không trả loop sớm hơn 75%". Cắt thuần tuý sẽ làm payoff rơi xuống dưới ngưỡng vì phần bị cắt tập trung ở nửa sau.

**Cái KHÔNG đụng tới:** cold open (81s, đang là chỗ duy nhất có số đo nói rằng nó quyết định AVD) · 2 anecdote · ẩn dụ ゲート và mọi câu callback của nó · phép tính 60÷3=20 · cảnh báo 腎臓 (2 lần) · CTA giữa + checkpoint 「に」 · kết 4 lớp + disclaimer.


## 1. Người xem đến vì cái gì, ở lại vì cái gì

- **Đến vì:** thumbnail/title hứa "ăn đủ đạm rồi mà cơ vẫn teo" — đúng cái nghịch lý mà tệp 60–80 đang sống trong đó (bữa tối rất tử tế, nhưng chân yếu dần). Stake không phải lỗ tiền mà là **足腰 → 転倒 → 介護 → 迷惑をかけたくない**.
- **Ở lại vì:** một câu đố treo suốt bài — **「あと一品」の正体** (hứa ở giây ~70, trả ở 14′27 = **75,4%**), cộng **một phép đo tự làm được ngay trên ghế** (指輪っかテスト ở 05′39) và **một con số bị làm phép tính trước mặt** (ろくじゅうグラム ÷ 三回 = にじゅうグラム, rồi đối chiếu với ごグラム của bữa sáng bánh mì).

## 2. ĐO CẦU (API YouTube Data, 30 ngày, JP/ja, long-form ≥8′, đo **2026-08-25**)

> Hàng đợi `03_CONTENT_PLAN.md` §2.13 để lại `血液ドロドロ` (cùng trục video 17) + hai key cũ 内臓脂肪/血圧. Đo lại trong chính lượt viết (luật §2.10): `血液ドロドロ` med 932 **nhưng n=3** — cung quá mỏng, và 2/3 là kênh bác sĩ, không phải rổ 食卓. Trục thắng của lượt này đến từ chỗ khác: **swipe file `01_SWIPE_TITLES.md` (quét 08-21) có 4/15 video view/ngày cao nhất đều là trục タンパク質・筋肉** của 高齢者健康の真実 — đo lại thì đúng.

| keyword | n | med v/ngày | max | rổ |
|---|---|---|---|---|
| **高齢者 タンパク質** ⭐ dẫn title | 18 | **723** | 10.253 | rổ senior JP thuần: 人生と健康の知恵袋「卵より高たんぱくな食品ランキング」**82.127 view / 8 ngày** · 高齢者健康の真実「最強の高タンパク食品TOP5」40.596/15d |
| **高齢者 筋力低下** ⭐ stake | 17 | **292** | 10.253 | cùng rổ; thêm 漫画で学ぶシニアの人生CH「筋肉を減らす最悪な習慣7選」58.649/20d |
| 高たんぱく 食品 | 4 | 1.660 | 10.253 | n nhỏ, 1/4 là kênh công thức (DAIFUKU KITCHEN) |
| タンパク質 摂り方 | 13 | 129 | 2.147 | 3 video mạnh nhất là kênh Anh ngữ → rổ pha |
| タンパク質 不足 高齢者 | 20 | 54 | 1.859 | rổ đúng nhưng cầu/video thấp |
| サルコペニア | 17 | 56 | 2.697 | ⛔ 2/3 top là kênh Anh ngữ + manga |
| 血液ドロドロ | **3** | 932 | 1.921 | ⛔ cung quá mỏng, rổ bác sĩ |
| 骨粗しょう症 食べ物 | 11 | **0** | 64 | ⛔ cầu tắt |
| フレイル 予防 / 筋肉 落ちる 食べ物 | 4 / 7 | 19 / 9 | — | ⛔ rổ thể dục / cầu thấp |

⭐ **Điều đáng ghi nhất của lượt đo này:** §2.12 kết luận *"cột `<món> 食べ方` của ngách senior ĐÃ CẠN"* (không còn ứng viên nào >50 v/ngày) và §2.11 mở đường "đo STAKE thay vì đo MÓN". Lượt này đi thêm một bậc nữa: **đo DƯỠNG CHẤT**. `高齢者 タンパク質` = **723 v/ngày với n=18** — cao gấp 4–15 lần mọi cột `<món> 食べ方` từng đo (生姜 48 · りんご 171 · バナナ 189), và rổ sạch hoàn toàn. Lý do có thể giải thích được: dưỡng chất là thứ **nhiều món cùng phục vụ**, nên nó không bị kênh công thức chiếm (rổ công thức nói về MÓN, không nói về DƯỠNG CHẤT) — đúng cái bẫy mà §2.11/§2.12 đã phải loại 6/32 keyword vì nó.

⚠️ **Chống tự cạnh tranh:** video 12 (豆腐) cũng trục 筋肉・たんぱく質. Khác biệt đủ xa: 12 = MỘT MÓN mổ sâu (木綿/絹/高野豆腐), 19 = **CÁCH CHIA trong ngày**, và 豆腐 chỉ xuất hiện 2 lần như một ví dụ trong danh sách. Cách nhau 7 số.

## 3. STAKE & KHUÔN

1. **MỘT ẩn dụ duy nhất, được nuôi lớn suốt bài:** 筋肉 = 毎日建て替えられる家 · たんぱく質 = 材料を積んだトラック · 朝昼晩 = **一日に三回しか開かないゲート**. Ẩn dụ này trả lời được **cả ba** câu hỏi của bài (vì sao dồn bữa tối không được · vì sao bữa trưa chỉ có mì là mất một lần · vì sao sáng quan trọng nhất) nên không cần ẩn dụ thứ hai. Nó còn kéo được khối phụ vào cùng khung: ご飯 = **重機を動かす燃料** (ăn nhiều đạm mà bớt cơm thì nguyên liệu bị đốt làm nhiên liệu).
2. **Hero number được LÀM PHÉP TÍNH trước mặt người xem:** ろくじゅうグラム(推奨量) ÷ 三回 = **にじゅうグラム/食** → đối chiếu ごグラム(食パン一枚) → 「四分の一しか開いていない」. Và phép tính sốc mở bài: thiếu mỗi sáng × 三百六十五回 = **ごキロの袋ひと袋分** (cố ý nói rõ đây là **lượng NGUYÊN LIỆU không đến**, KHÔNG phải "5kg cơ bị mất" — YMYL).
3. **Khuôn: 「一日を、逆から歩く」** — 夜 → 昼 → 朝 (đích). Ba video liền kề không cùng dáng ✅ (17 = 時計を追う · 18 = 鎧 hai nhánh · **19 = đi ngược một ngày**).
4. **Một phép đo làm được ngay trên ghế:** 指輪っかテスト (東京大学の研究チームが考案) ở 05′39 — 30 giây, không cần cân, và có 3 mức kết quả nên ai xem cũng "trúng" một mức.
5. **Chất người ≥4/6 mũi tiêm:** ① みのり tự thú 「朝はコーヒーだけ」 ② 克己さん có thoại 「毎晩あんなに食べてるのに、なんでだ」 + chi tiết vô dụng-về-thông-tin (tưới chậu cây mỗi sáng) ③ ký ức giác quan 「炊きたてのご飯の湯気、焼き魚の匂いで目が覚めた朝」 ④ みのり tự luộc trứng để sẵn suốt 2 tuần ⑤ あや子さん đóng bằng cảm xúc 「孫を抱き上げるのが、こわくなくなったの」 ⑥ phá nhịp 「同じ量です。同じ食材です。違うのは、配り方だけ。」

**Mốc thời gian (ĐÃ CẬP NHẬT từ `subs.srt` thật sau render 2026-09-01 — lệch vài giây so ước mô hình, xem bản ước cũ trong git history):**

| mốc | khối | luật |
|---|---|---|
| 01:25 | **ITEM1 = 夜の食卓** | payoff #1 ≤4′ ✅ (cold open 81s) |
| 03:44 | khối persona + xin đăng ký | phải SAU mục đầu ✅ (L3) |
| ~04:15 | ⚠️ cảnh báo 腎臓 (lần 1/2) | YMYL — đặt TRƯỚC mọi lời khuyên tăng đạm |
| 04:55 | 原典: 厚労省 食事摂取基準 2025年版 + phép tính 60÷3=20 | lớp `genten` ✅ |
| 05:43 | 指輪っかテスト (làm ngay trên ghế) | |
| 06:54 | 昼の食卓：麺だけの一食 | |
| 08:29 | anecdote 1 (克己さん) | ~44% |
| 09:33 | **CTA giữa + checkpoint 「に」** | **49,5%** ✅ (`cta-midvideo.md` §2.2) |
| 10:08 | 朝 = 本題 · 12:17 落とし穴3つ | |
| 13:14 | お肉は重たい → FAQ プロテイン → ご飯は燃料 | khối được DỜI lên, xem §0 |
| 14:31 | **TRẢ OPEN LOOP: 「あと一品」= 卵** | **75,4%** ✅ (ngưỡng ≥75%) |
| 16:06 | anecdote 2 (あや子さん) | |
| 16:57 | recap + kết 4 lớp · 18:0x disclaimer | |
| 19:25 | hết | ⚠️ ngoài dải 21–25′ — user chốt, §0 |

## 4. S8 — 13 điểm cảnh báo, đã duyệt bằng mắt

Theo checklist 0c: *"trang trí thì CẮT, cơ chế thì chèn một con số THẬT, ⛔ đừng nhồi số vô nghĩa"*. Duyệt hết 11 vùng: **0 vùng là trang trí**, nên **không sửa gì**. Ba vùng dài nhất:
- `4′01` (6 câu) = khối persona + CTA + cảnh báo 腎臓 — nội dung bắt buộc của kênh; regex không tính là "đồng tiền" nhưng nó là hợp đồng với người xem.
- `7′02` (6 câu) = liệt kê そうめん/うどん/蕎麦 + câu giác quan 「つるっと食べられて」 — `つるっと` không nằm trong từ điển SENSE của gate: đây là **giới hạn của gate**, không phải lỗi của bài.
- `16′23` (9 câu) = đóng anecdote 2 bằng cảm xúc rồi chuyển sang recap — mũi tiêm ⑤ của rule humanize, cố ý không có số.

## 5. Bộ title A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代の落とし穴】たんぱく質は足りているのに筋肉が減る人｜朝の「あと一品」` | 40 | たんぱく質@11 | keyword volume cao nhất rổ (723 v/ngày) + khung cảnh báo P0 + nghịch lý |
| **A2** | `60歳を過ぎたら筋力低下が始まる朝ごはん3つ｜タンパク質は「量」より配り方` | 36 | 筋力低下@8 | đổi keyword dẫn sang stake (292 v/ngày) **và** đổi chính tả sang katakana — test luôn dạng chữ nào ăn hơn |
| **A3** | `夜にたくさん食べても筋肉は増えません｜60代が知らないたんぱく質の落とし穴` | 36 | — | đổi kiểu hook: P4 đảo nhận thức, dẫn bằng câu phủ định thẳng thói quen |

### Title CHỐT

```
【60代の落とし穴】たんぱく質は足りているのに筋肉が減る人｜朝の「あと一品」
```

**Tên file upload:** `tanpakushitsu-asa-kinniku-60dai.mp4`

## 6. TEXT THUMBNAIL (chữ GIỐNG NHAU ở cả T1/T2/T3 — biến thử là HÌNH)

| dòng | chữ | ký | vai (gate 7 `audience-45plus` §1) | màu |
|---|---|---|---|---|
| 1 | `たんぱく質` | 6 | **① VỀ CÁI GÌ** — keyword **top 1 bảng đo** (723 v/ngày) | kem/trắng ngà |
| 2 | `筋肉が減る` | 5 | **② CHUYỆN GÌ XẢY RA** — hero, loss-aversion, khớp keyword top 2 (筋力低下) | **VÀNG KIM, to nhất** |
| 3 | `正解は朝` | 4 | **③ PHẢI LÀM GÌ** — khớp khuôn kênh 「正解は食後」(18) 「正解は時間」(16) | **ĐỎ** |

- Che ảnh đi vẫn đọc ra: "đạm — cơ teo — đáp án nằm ở buổi sáng" ✅ gate 7.
- Gate 1 (≤6 ký/dòng) ✅ · gate 3 (đúng 3 dòng) ✅ · gate 6 (nền sáng) ✅.
- **Đảo biến so với video 18** (chống lặp nguyên bộ, Phần E luật): 18 = hero **ĐỎ** + cột chữ nửa **PHẢI** → 19 = hero **VÀNG KIM** + cột chữ nửa **TRÁI**, badge 「食卓」 trên-PHẢI, dải vàng mép PHẢI.
- Không chữ 血/透析 · không 医師/専門家 · không claim khỏi bệnh.

## 7. PROMPT ẢNH THUMBNAIL — 4 file trong `06_VIDEO/19_tanpakushitsu-asa/`

Khuôn lấy từ **ảnh đã lên sóng** của chính kênh (16/17/18), không lấy từ tài liệu (`ab-3title-3thumb.md` §3.1 Bước 1): photorealistic, phòng ăn Nhật **ban ngày sáng**, bà cụ ~68 tóc bạc ngắn + tạp dề be trên áo xanh, con dấu tròn ĐỎ 「食卓」, dải vàng kim ở mép, chữ 3 dòng 袋文字 viền nâu đậm + halo trắng.

| file | vai |
|---|---|
| `thumb_prompts_FLOW.txt` | **bản DÙNG** — 3 prompt, mỗi prompt 1 DÒNG |
| `thumb_prompts_BLOCKS.md` | bản người đọc: khung khối + bảng chữ + 5 việc nghiệm thu |
| `thumb_prompts_TENFILE.txt` | thứ tự dòng FLOW ↔ `thumb_T1/T2/T3_tanpaku.png` |
| `thumb_prompts_PLATE.txt` | 🛟 3 plate KHÔNG chữ (đường lui nếu kanji nát) — ⛔ để RIÊNG |

**Ba bản, mỗi bản đổi ĐÚNG 1 biến:** T1 baseline khuôn kênh (chữ nửa TRÁI, người PHẢI bưng khay bữa sáng) · T2 đổi **1 biến hình = CROP** (close-up sát mặt, tay cầm quả trứng luộc bóc dở) · T3 đổi **LAYOUT** (đảo trục: chữ nửa PHẢI, người TRÁI, badge trên-TRÁI).

⚠️ Sau khi gen: soi TỪNG ký tự (`質` và `減` rậm nét, dễ nát nhất) → **VÁ watermark ✦, KHÔNG cắt** (`tools/strip_wm_thumb.py`, đo ✦ bằng MẮT theo LÔ, soi cả 4 góc ở 1:1) → gate 168px → đặt tên `thumb_T1/T2/T3_*.png` → trần 2 MB.

## 8. QUÉT COMPLIANCE (`.claude/rules/youtube-compliance.md`)

1. **Title/thumbnail:** không có từ nhóm 殺/死/自殺/レイプ/虐待 · **không có 血/透析** (bài nói về 筋肉 nên trục mạch máu không cần chạm) · không 医師が解説/医師警告. ✅
2. **Persona:** みのり không xưng 医師/管理栄養士/専門家; không có khối credential (gate S7 = 0). ✅
3. **Không tên thật** hãng/sản phẩm/người. Nguồn nêu đích danh đều là **cơ quan/tạp chí có thật**: 厚生労働省「日本人の食事摂取基準（2025年版）」 · Journal of Nutrition 2014 (Mamerow et al.) · 東京大学の研究チーム (指輪っかテスト). ✅
4. **YMYL:** 0 lần 治る/完治/薬の代わり/絶対 · cảnh báo 腎臓×たんぱく質制限 nói **2 lần** (04:43 và trong disclaimer) · disclaimer cố định cuối video ✅.
5. **Thumbnail nhân vật AI hư cấu + món ăn** → không cần tick synthetic. Ảnh AI dùng làm slide TRONG video → **có tick** theo `youtube-compliance.md` §2.1.
6. **Số liệu đã verify** (không bịa): 65歳以上 推奨量 男60g/女50g · 目標量下限 15%エネルギー (đều 2025年版) · Mamerow 2014 ≈25% · 卵1個≈6g · 納豆1P≈7g · 牛乳200ml≈6,6g · 食パン1枚≈5g · ヨーグルト小1個≈4g. Số nào không chắc đã hạ xuống hedge 「〜という報告があります」 (tỉ lệ người đạt 20g ở bữa sáng).

## 9. TAG + HASHTAG + 概要欄

### タグ
```
60代からの食卓,シニアの健康,60代の食事,たんぱく質,タンパク質 高齢者,高齢者 タンパク質,筋力低下,サルコペニア 予防,筋肉 減る,朝ごはん,朝食 たんぱく質,たんぱく質 摂り方,卵 食べ方,納豆,60歳からの健康,70代 健康,シニア 食事,フレイル 予防,指輪っかテスト,食事摂取基準,健康長寿,老後の健康,高齢者 食事,たんぱく質不足,足腰 衰え,転倒予防,介護予防,健康雑学,シニアライフ,みのり
```

### 概要欄 — 3 DÒNG ĐẦU
```
「一日の合計は足りているのに、なぜか筋肉が減っていく」——六十代からのたんぱく質は、量ではなく「配り方」で決まります。
夜にどれだけ召し上がっても、朝の空白は埋まりません。この動画では、その理由と、朝の食卓に足すだけの「あと一品」を、ゆっくりお話しします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。
```

### 概要欄 — MÔ TẢ ĐẦY ĐỦ
```
「一日の合計は足りているのに、なぜか筋肉が減っていく」——六十代からのたんぱく質は、量ではなく「配り方」で決まります。
夜にどれだけ召し上がっても、朝の空白は埋まりません。この動画では、その理由と、朝の食卓に足すだけの「あと一品」を、ゆっくりお話しします。
六十代・七十代のご本人と、離れて暮らすご家族に向けた、台所の言葉だけでお伝えする回です。

筋肉は毎日少しずつ建て替えられていて、その工事現場のゲートは、朝・昼・晩の一日三回しか開きません。
朝のゲートが空っぽのまま閉じると、その回の工事は、材料がないまま休みになります。
夜にまとめて召し上がっても、置き場のないぶんは運び出されてしまう——二千十四年に発表された報告では、同じ量でも夕食に偏った食べ方をすると、一日でつくられる筋肉の量が約二十五パーセント低かったとされています。

【この動画でお話しすること】
00:00 「足りているのに減る」——朝の空白
01:25 夜の食卓：まとめ食いが貯金にならない理由
03:44 ごあいさつと、大切なお願い
04:55 厚生労働省「日本人の食事摂取基準（2025年版）」でみる目安
05:43 椅子に座ったまま三十秒：指輪っかテスト
06:54 昼の食卓：麺だけの一食
08:29 静岡県・克己さんの話
10:08 朝が、いちばん空いている理由
12:17 朝の落とし穴 三つ
13:14 粉のプロテインは要りません／ご飯を減らさないでください
14:31 お約束していた「あと一品」の正体
16:06 新潟県・あや子さんの話
16:57 今日のまとめ

【出典】
・厚生労働省「日本人の食事摂取基準（2025年版）」策定検討会報告書
・Mamerow MM et al., Journal of Nutrition, 144: 876-880, 2014
・東京大学の研究チームが考案した「指輪っかテスト」

※この動画は、公表されている研究や公的資料をもとにした、健康に関する一般的な情報です。お一人おひとりに合わせた医療のアドバイスではありません。とくに腎臓の治療を受けている方は、たんぱく質の量に決まりがある場合があります。持病のある方やお薬を飲んでいる方は、食事を変える前に、必ずかかりつけの先生にご相談ください。

音声：VOICEVOX:青山龍星

#60代からの食卓 #シニアの健康 #60代の食事 #たんぱく質 #筋力低下
```

## 10. HANDOFF

```
python tools\check_coldopen.py 19          # PASS moi duoc di tiep
py tools\build_slides_19.py                # PLAN + prompt FLOW -> user gen anh
py tools\ingest_slides_19.py               # trim vien + va watermark + khung san khau
py ..\remotion-vox\tools\import_pipeline.py
py ..\remotion-vox\tools\build_overlays_19.py
run_full19.cmd                             # chay NEN (render-background.md)
```

⚠️ Sau render: cập nhật lại 目次 ở §9 bằng mốc THẬT từ `subs.srt` (mốc hiện tại là ước từ mô hình CPS).
