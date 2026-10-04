# 18 — りんご：鎧と、一人ぼっち（60代からの食卓）

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI
- **Chủ đề:** **りんご × 血糖の上がり方（坂道の比喩） × 「鎧」（皮 と 食べる仲間）**
- **Bản đọc chuẩn:** `18_ringo-tabekata_TTS.md` — **bản 2** · **4.637 ký (thuần) · 145 dòng · ước 18′10** (mô hình CPS 4.40 + GAP 0.25/dòng, `tools/check_coldopen.py`) — sửa lời thì sửa file này **và** quét lại `match` trong SLIDES khi có.
- **⛔ GATE MÁY:** `python tools\check_coldopen.py 18` → ✅ **PASS, cold open 75 giây** (L1–L5 · S6 · S7 sạch, dư ~15s so trần 90s) · **38 tag** (base [しっとり][速0.8] + 36 nhấn nhá, gồm 1 đỉnh bài `[間1.2][速0.8][後間1.0]`) · 0 tag giữa câu · 0 tag đứng dòng riêng ngoài base · blacklist Mục 7 = 0 · S8 (cảnh báo, không chặn) ~10 điểm rải rác — đã giảm từ ~11 ở bản 1, KHÔNG cố nhồi số để xanh gate.

---

## 0. 🔴 VÒNG SỬA — bản 1 PASS mọi gate máy, nhưng chỉ đáng 6/10

> user: *"kịch bản có giữ chân người xem không? người xem đến vì cái gì, ở lại vì cái gì? kịch bản phải có hồn, hook phải ấn tượng, nội dung không được rời rạc"*

Bản 1 (5.364 ký, 21′00) **PASS cả 3 gate cứng** (L1–L5, S6, S7) và trông đầy đủ số liệu, nhưng khi tự soi bằng đúng 4 câu hỏi mà video 16/17 từng bị hỏi, nó lộ **đúng 4 lỗ giống nhau**:

### 0a. ITEM1 (皮) là một BÀI GIẢNG rời, không phải một CẢNH
Bản 1 mở ITEM1 bằng: 「りんごを、皮をむいて食べる。そう決めている方も、多いはずです」 — mô tả chung, không phải một khoảnh khắc cụ thể. Cú xoắn (「つるっとした光沢は農薬ではなく天然のろう質」) đúng hướng nhưng bị chôn giữa một loạt câu liệt kê (rửa thế nào / ngâm nước một đêm / muối). Đây đúng bệnh đã ghi ở `humanize-script-voice.md` §0a: twist hay nhưng bọc trong mô tả, không phải cảnh.

### 0b. KHÔNG có "hero number" nào được LÀM PHÉP TÍNH trước mặt người xem
Bản 1 có nhiều số (二百グラム, 四グラム, 二倍, スプーン五杯) nhưng tất cả chỉ là **fact được đọc ra**, không có khoảnh khắc nào giống 「十時間×4=四十時間, mà một ngày chỉ có二十四時間」 của video 17 — thứ khiến con số trở thành một cú sốc thay vì một dữ liệu.

### 0c. RỜI RẠC THẬT — 9 chủ đề không nối với nhau, chỉ nối bằng "và tiếp theo"
Đếm bản 1: ①皮/農薬 ②天然ワックス ③一日何個 ④カリウム/腎臓 ⑤血圧 ⑥りんごジュース ⑦品種(紅玉/ふじ/王林) ⑧保存(エチレンガス) ⑨FAQ 糖尿病 ⑩FAQ 変色. Ẩn dụ 坂道 chỉ sống ở đầu và giữa bài, biến mất suốt phần 品種/保存/FAQ — đúng lỗi §0c của video 16/17: nhiều lát cắt kiến thức đúng nhưng không có MỘT sợi chỉ nào xuyên suốt. ④③⑤ (量/カリウム/血圧) đã tốt vì nó phục vụ nhánh YMYL bắt buộc; ⑦⑧⑨⑩ là bốn thứ nhồi thêm **chỉ để đủ ký tự cho dải 21–25′**, và đó chính là cái làm bài đọc như một trang tạp chí, không như một câu chuyện.

### 0d. Payoff giải được 2 nhánh, nhưng KHÔNG kết nối với ITEM1
「りんごを一人ぼっちにしない」 giải đúng cả "khi nào" và "ăn cùng gì" (đạt bài học §0d của video 17) — nhưng nó đứng tách biệt hoàn toàn với nhánh 皮 ở đầu bài. Người xem không cảm được đây là MỘT bài học, mà là hai bài học khác nhau ghép lại.

### Bản 2 sửa bằng MỘT khái niệm duy nhất, không phải chữa từng câu

**「鎧」(áo giáp) — りんごの皮 = áo giáp CỦA CHÍNH NÓ · thức ăn ăn cùng = áo giáp NGƯỜI CHO MƯỢN.** Cả 皮 và 場面 giờ là HAI NỬA của cùng một ý, không phải hai bài học rời:

- Hook mở bằng CẢNH cụ thể + **phép tính sốc thật**: 「一日一個、りんごを三十年食べ続けると、その口は一万回を超えます」（365×30≈10.950, tính đúng, không bịa）— con số này được **callback lại 3 lần** (giữa bài, đỉnh bài, recap) để bài có một sợi chỉ chạy suốt, không phải một con số nói một lần rồi bỏ.
- ITEM1 mở bằng cảnh 「むいた皮が、くるくると、シンクに落ちていく」 rồi mới xoắn sang "đó là áo giáp, không phải nông dược" — và **kết bằng câu nối tới nhánh sau**: 「これは、りんご自身が持つ、鎧の話です。今日、一番お伝えしたいのは、もう一つの鎧の話です」 (thay câu mơ hồ 「入り口です」 của bản 1).
- **CẮT HẲN 4 khối nhồi số ký tự** (品種 3 loại, 保存/エチレンガス, cả 2 FAQ) — không thay bằng nội dung khác, mà thay bằng chiều sâu THẬT của đúng 2 nhánh: みのり **tự thử nghiệm** (ăn táo một mình vs cùng yogurt, cảm giác khác nhau — mũi tiêm ④), một dặn dò **cho người yếu răng** (không ép ăn cả vỏ), 焼きりんご và ジュース được **kéo vào cùng khung 鎧** thay vì đứng riêng, và một câu linh hoạt cho payoff cuối (không có yogurt thì dùng trứng/cơm) để quy tắc áp được vào đời thật.
- ⚖️ **Đánh đổi CÓ THẬT, không giấu:** bản 2 ngắn hơn bản 1 — **18′10 so với 21′00**, dưới dải 21–25′ đã siết cho kênh (`CLAUDE.md` §🎯 RETENTION). Đây là lựa chọn có chủ đích: bằng chứng "cắt ngắn không mua được AVD" trong `CHANNEL_DIAGNOSIS_2026-08-11` nói về việc **cắt bớt nội dung đang hay**, không nói về việc không nhồi nội dung rời rạc vào từ đầu. Giữa "21 phút rời rạc" và "18 phút liền mạch", ưu tiên đang chọn là mạch truyện — nhưng đây là đánh đổi CHƯA có số đo riêng cho kênh này, ghi lại để nếu AVD tụt thì đây là biến đầu tiên xét lại. Muốn kéo về ≥21′ mà không rời rạc lại thì cách đúng là làm SÂU hơn 2 nhánh còn lại (ví dụ thêm 1 anecdote hoặc mở rộng phần 鎧 ăn cùng), không phải thêm nhánh mới.

## 1. Người xem đến vì cái gì, ở lại vì cái gì (đọc theo yêu cầu)

- **Đến vì:** thumbnail/title hứa "đang ăn táo sai cách, có thể hại thận" — đúng nỗi lo tuổi 60+ đã có sẵn (khám sức khoẻ định kỳ, sợ transplant/mù mắt/mất tự lập).
- **Ở lại vì:** KHÔNG phải vì danh sách mẹo (đó chỉ giữ người tới hết mẹo họ cần), mà vì **một câu đố treo suốt bài**: "không phải vỏ, không phải lượng — vậy là gì?" + **một con số ám ảnh được nhắc lại** (一万回) + cảm giác **đang tự soi lại chính thói quen ăn sáng/ăn khuya của mình** qua 2 câu chuyện. Khi bài chỉ là chuỗi mẹo rời, người xem có thể rời đi ngay sau khi lấy được mẹo đầu tiên vì không còn gì "nợ" họ; khi bài là MỘT câu đố, họ ở lại để lấy đáp án.

---

## 2. ĐO CẦU (API YouTube Data, 30 ngày, JP/ja, long-form ≥8′, đo 2026-08-20)

> Hàng đợi §2.12 để lại `こむら返り` (đã CHẾT, 0 video/30 ngày), `血液ドロドロ` (cùng trục 17, không làm liền kề), `マグネシウム不足`/`チーズ` (đo lại: rổ SAI 100% — kênh Anh ngữ/ゆっくり解説/mukbang, không phải senior JP). Đo mở rộng thêm 20 candidate khác (痛風/尿酸値/しじみ/梅干し/黒酢/アーモンド/オリーブオイル…) — phần lớn cùng bệnh rổ sai. **りんご** là candidate đầu tiên trong lượt đo hôm nay có rổ senior JP thuần với nhiều kênh corroborate:

| keyword | n | med v/ngày | rổ |
|---|---|---|---|
| **りんご 腎臓** ⭐ stake | 15 | 1 (nhưng **max 869**, kênh senior JP thuần) | 健康雑学・老後の生活・シニア安心ライフ健康・大人の健康手帖・安らぎ健康ライフ — **5 kênh senior JP khác nhau cùng làm đúng góc 「りんごの食べ方×腎臓に負担」** trong 30 ngày |
| **りんご 食べ方** ⭐ dẫn title | 11 | 171 | rổ sạch, top hit chính là `健康雑学`「りんごの食べ方9選｜腎臓に負担をかける習慣」869 v/ngày |
| りんご 血糖値 | 12 | 8 | rổ senior JP (高齢者健康の真実・食で長生き…) nhưng med thấp — đúng bài học §2.8: giữ trục 血糖 trong nội dung, KHÔNG đưa chữ 血 lên title/thumbnail |
| りんご 食べ合わせ | 11 | 5 (max 1.012, nhưng đó là video シナモン không phải りんご thật) | không dùng làm khuôn — đã bão hoà 4 video 食べ合わせ (§2.6–§2.9) |

⭐ **Bài học áp dụng:** kho premise PROVEN của `03_CONTENT_PLAN.md` §2.5 đã ghi sẵn *"果物X個が腎臓を痛める + 助ける果物 → 519K/7 tháng"* — りんご chính là mảnh ghép món cụ thể cho premise đó, đo được bằng 5 kênh corroborate cùng lúc chứ không phải suy diễn.

## 3. STAKE & KHUÔN (bản 2, sau vòng sửa §0)

1. **Concrete SCENE + phép tính sốc**, không phải khái niệm: 「朝、りんごを一つ、そのまま、パクリ」 → 「一日一個、三十年で一万回」.
2. **MỘT ẩn dụ duy nhất, cho nó lớn lên và được callback**: 坂道 (急坂 ↔ なだらか坂) + con số 一万回 nhắc lại 3 lần (giữa bài, đỉnh bài, recap) — không chồng ẩn dụ khác.
3. **MỘT khái niệm gốc nối cả 2 nhánh**: 「鎧」(áo giáp) — 皮 = áo giáp của chính りんご, thức ăn ăn cùng = áo giáp người cho mượn. ITEM1 (皮) là một mảnh câu đố, kết bằng câu nối rõ ràng tới nhánh sau, không phải câu mơ hồ.
4. **MỘT quy tắc giải hết**: 「りんごを、一人ぼっちにしないこと」 giải cả nhánh THỜI ĐIỂM và nhánh KẾT HỢP — không phải 2 lời dặn rời.
5. **KHÔNG một câu nào phủ định 「りんごが悪い」** trong 90 giây đầu (S6) — khác 3 video đã đo mất 45–55 điểm ở giây 20–40. Không có khối credential (S7).
6. **Không nhồi nhánh nội dung mới để đủ ký tự** — thà ngắn hơn dải 21–25′ và liền mạch, còn hơn đủ ký tự và rời rạc (xem đánh đổi ở §0).

## 4. Bộ title A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代70代】りんごの食べ方でまちがえやすいこと3つ｜今日変えるのは一つだけ` | 38 | 食べ方@8 | keyword đo được cao nhất rổ đúng-ngách (med 171), nằm trong 25 ký đầu |
| **A2** | `【60代70代】りんごが腎臓を弱らせる食べ方｜正しい食べ方はこの一つ` | 34 | りんご@8・腎臓@12 | đổi keyword dẫn sang stake nặng hơn (5 kênh corroborate, max 869) |
| **A3** | `りんごを一人ぼっちにすると、坂が急になる｜60代からの食べ方` | 30 | 食べ方@27 | đổi kiểu hook: P0 cảnh báo → **P4 đảo nhận thức**, dẫn thẳng bằng ẩn dụ trung tâm của bài |

### Title CHỐT
```
【60代70代】りんごの食べ方でまちがえやすいこと3つ｜今日変えるのは一つだけ
```

## 5. TEXT THUMBNAIL — 🔴 ĐÃ ĐỔI 2026-08-21 (bản cũ RỚT GATE 7)

**Bản cũ (rớt):** `皮をむいて` / `腎臓が悲鳴` / `食べる場所で`. Che ảnh đi, đọc hết 3 dòng vẫn
**không biết video nói về りんご** — thiếu câu ① của gate 7 (`audience-45plus.md` §1), đúng lỗi
rule gọi là "nặng nhất". Và nó đặt `腎臓` lên hero trong khi bảng đo Trends ở §2 của chính file
này cho **`りんご 食べ方` med 171 = cao nhất rổ sạch**. Lỗi phụ: `場所` (địa điểm) đọc lệch —
payoff thật của bài là **THỜI ĐIỂM + ăn cùng gì**, không phải chỗ ngồi.

| dòng | chữ | ký | vai (gate 7) | màu |
|---|---|---|---|---|
| 1 | `そのりんご` | 5 | **① VỀ CÁI GÌ** — keyword りんご; khớp khuôn kênh 「そのバナナ」 (bản 16 live) | kem/trắng ngà |
| 2 | `半分捨ててる` | 6 | **② CHUYỆN GÌ XẢY RA** — hero, con số + loss-aversion | **ĐỎ, to nhất** |
| 3 | `正解は食後` | 5 | **③ PHẢI LÀM GÌ** — khớp khuôn kênh 「正解は時間」 (bản 16 live) | vàng kim |

- Cơ sở của `半分捨ててる`: 文部科学省 食品成分データ — chất xơ vỏ-có vs vỏ-bỏ chênh **gần 2 lần**
  (đã nói trong bài). Không phải claim bịa, không hứa khỏi bệnh, bỏ hẳn `腎臓`/`血` khỏi thumbnail.
- Cả 3 dòng ≤6 ký (gate 1) · đúng 3 dòng (gate 3) · nền sáng (gate 6). Chữ **GIỐNG NHAU ở T1/T2/T3**
  — biến thử là HÌNH (`ab-3title-3thumb.md` §3 mục 6).

- Không chữ 血/透析/腎臓 (compliance §3 + Mục 15 E1). Không claim chữa khỏi.

## 6. PROMPT ẢNH THUMBNAIL — ✅ ĐÃ XUẤT 4 FILE (2026-08-21)

🔴 **Khuôn lấy từ ảnh ĐÃ LÊN SÓNG của chính kênh, KHÔNG từ tài liệu** (`ab-3title-3thumb.md`
§3.1 Bước 1). Đo 2 bản live `07_UPLOADED/17_chuseishibo-oyatsu` + `16_banana-yoru-toire`:

| thành phần | khuôn thật đang chạy |
|---|---|
| ảnh | **photorealistic** (KHÔNG phải minh hoạ), nền **SÁNG** phòng ăn Nhật ban ngày |
| người | bà cụ ~68, tóc bạc ngắn, **tạp dề be** trên áo xanh, mặt LO/nhíu mày, bưng đĩa món |
| nhận diện | **con dấu tròn ĐỎ 「食卓」** góc trên + **dải vàng kim** ở mép |
| chữ | 3 dòng 袋文字 viền **nâu đậm** + halo trắng, chiếm **một nửa khung** |
| màu | kem/trắng ngà → **hero ĐỎ** → vàng kim |
| hero đo được | cao **23–24%** khung · rộng **48–61%** ← thứ mua được legibility |

⚠️ **Đè mô tả cũ trong `02_THUMBNAIL_TITLE_RULES.md` Phần E** ("nền tối moody") — khuôn live
đã là nền SÁNG (đúng gate 6 của `audience-45plus.md` §1). Prompt bản đầu của file này viết theo
mô tả cũ (dim kitchen at dusk, low-key) nên đã bị thay.

**4 file trong `06_VIDEO/18_ringo-tabekata/` (§3.1 Bước 4 — mỗi file một việc, đừng gộp):**

| file | vai |
|---|---|
| `thumb_prompts_FLOW.txt` | **bản DÙNG** — 3 prompt, mỗi prompt 1 DÒNG, bơm thẳng extension |
| `thumb_prompts_BLOCKS.md` | bản người đọc: khung khối + bảng số đo + bảng chữ + 5 việc nghiệm thu |
| `thumb_prompts_TENFILE.txt` | thứ tự dòng FLOW ↔ `thumb_T1/T2/T3_ringo.png` |
| `thumb_prompts_PLATE.txt` | 🛟 3 plate **KHÔNG chữ** (đường lui nếu kanji nát) — ⛔ để RIÊNG, đừng trộn vào FLOW |

**Ba bản, mỗi bản đổi ĐÚNG 1 biến** (chữ giống nhau cả 3):
- **T1** baseline khuôn kênh (theo bản 17): chữ nửa PHẢI, badge trên-TRÁI, dải vàng mép TRÁI, người bán thân trái bưng đĩa táo + vỏ xoắn.
- **T2** đổi **1 biến hình = CROP**: close-up sát mặt, cầm nửa quả táo cạnh má. Giữ nguyên chữ/badge/dải vàng/layout.
- **T3** đổi **LAYOUT**: đảo trục theo bản 16 — chữ nửa TRÁI, người PHẢI, badge trên-PHẢI, dải vàng mép PHẢI.

**Gate prompt đã đo (§3.1 Bước 3):** TEXT nằm ở **7–8%** đầu prompt (trần 15% — gate CHÍNH) ·
độ dài **1.489 / 1.480 / 1.352 ký** (trần 1.500 — gate phụ). Cỡ hero ép bằng **quan hệ với MÉP
KHUNG** (`reaching from the centre of the frame all the way to the right edge`), không tả phần
trăm — model nghe VỊ TRÍ, không nghe TỈ LỆ (`media-library.md` §2.10 ⑥).

**Sau khi gen, 5 việc trước khi giao** (chi tiết trong `_BLOCKS.md` §3): soi TỪNG ký tự (`捨` rậm
nét, dễ nát nhất) → **VÁ watermark ✦, KHÔNG cắt** (`tools/strip_wm_thumb.py`, đo ✦ bằng MẮT theo
LÔ, soi cả 4 góc ở 1:1) → gate **168px** → đặt tên `thumb_T1/T2/T3_*.png` → trần 2 MB.

## 7. QUÉT COMPLIANCE (`.claude/rules/youtube-compliance.md`)

1. Title/thumbnail: không có từ nhóm 殺/死/自殺/レイプ/虐待; không có 血/透析 (đã né, dùng 腎臓が悲鳴 thay 血糖急上昇). ✅
2. Persona: みのり không tự xưng 医師/栄養士/専門家; trong script chỉ khuyên "hỏi かかりつけの先生/栄養士さん CỦA NGƯỜI XEM", không tự nhận vai đó. ✅
3. Không tên thật người/hãng/viện — chỉ 文部科学省・日本高血圧学会 (tên cơ quan thật, giữ nguyên theo luật nguồn thật, không phải "tên người"). ✅
4. Tình tiết trên title/thumbnail có thật trong video: 皮 (ITEM1) ✅ · 腎臓/カリウム (đoạn giữa) ✅ · 「食べる場所」/一人ぼっち (payoff cuối) ✅.
5. Không claim chữa khỏi / tuyệt đối; disclaimer cố định đã có ở cuối script; cảnh báo kali cho người bệnh thận đã cài đúng chỗ chạm nhóm rủi ro (Mục 12 skill).

## 8. TAG + HASHTAG + 概要欄 (đóng gói CTR)

**Tên file upload:** `ringo-tabekata-60dai-shokutaku.mp4`

### タグ

26 tag: 16 tag nhận diện kênh (đứng đầu, cố định mọi video) + 10 tag riêng video.

```
60代からの食卓, 60代 食べてはいけない, 60代 食事, シニア 健康, 60代 健康, シニア 食事, 60代 レシピ, 高齢者 食事, 老後の健康, 健康長寿, 食生活改善, シニアライフ, 60代からの暮らし, 60代 一人暮らし, 健康な食事, 長生きの食事, りんご, りんごの食べ方, りんご 腎臓, りんご 皮, りんご 食べ過ぎ, カリウム, 血糖値が気になる, 食物繊維, りんごポリフェノール, 果物の食べ方
```

**3 hashtag nhận diện kênh (đứng đầu) + hashtag đề tài (đặt cuối 概要欄, không chiếm 3 dòng đầu):**
```
#60代からの食卓 #シニアの健康 #60代の食事 #りんごの食べ方 #腎臓に優しい食事
```

**3 dòng đầu 概要欄 (SEO hook — về gì/cho ai/được gì, 1 lần từ khóa, không lời chào):**
```
りんごの食べ方一つで、体への働きかたが大きく変わるかもしれません。60代からの食卓が、皮のむき方・一日の量・そして「一人ぼっちにしない」食べ方を、じっくりお伝えします。今夜のデザートから、すぐに試せる内容です。
```

**目次:**
```
00:00 一日一個、三十年で一万回──坂道の話
01:15 りんごの「鎧」皮をむくべきか問題
06:10 一日何個まで？カリウムと血圧の話
07:40 静岡・道子さんの体験談
09:40 一番大事な、もう一つの「鎧」
13:00 私も試してみた話／りんごジュース・焼きりんごの場合
15:20 宮城・元トラック運転手さんの体験談
17:30 まとめ──二つの鎧
```

**Mô tả đầy đủ（続き）:**
```
00:00 一日一個、三十年で一万回──坂道の話
01:15 りんごの「鎧」皮をむくべきか問題
06:10 一日何個まで？カリウムと血圧の話
07:40 静岡・道子さんの体験談
09:40 一番大事な、もう一つの「鎧」
13:00 私も試してみた話／りんごジュース・焼きりんごの場合
15:20 宮城・元トラック運転手さんの体験談
17:30 まとめ──二つの鎧

りんごは体にいいと聞いて、皮をむいて、決まった量を食べていれば安心。そう思っている方も多いのではないでしょうか。

実は、りんごの善し悪しを分けるのは、皮でも、量だけでもなく、「鎧があるかどうか」という、ほんの小さな習慣かもしれません。りんごには、皮という自分自身の鎧と、一緒に食べる仲間という、もう一つの鎧があります。空っぽの胃に一人で入ってくるりんごと、ご飯のあとに入ってくるりんごとでは、体の受け止め方がまるで違うと言われています。

今日は、① りんごの皮をむくべきかどうか（文部科学省の食品成分データより） ② 一日に食べる適量とカリウム・血圧の話（腎臓の治療中の方への注意も） ③ 今日一番大切な「りんごを一人ぼっちにしない」食べ方、の順にお伝えします。静岡県の道子さん、宮城県の元トラック運転手さんの体験談も交えながら、今夜からすぐに試せる形でお話しします。

※この動画でお伝えした内容は、公表されている研究などをもとにした、健康に関する一般的な情報です。個別の医療アドバイスではありません。持病のある方、お薬を飲んでいる方は、食事を変える前に、必ずかかりつけの先生にご相談ください。

音声：VOICEVOX（青山龍星）
出典：文部科学省 食品成分表、日本高血圧学会などの一般的な情報を参考にしています。

#60代からの食卓 #シニアの健康 #60代の食事 #りんごの食べ方 #腎臓に優しい食事
```

## 9. 🖼️ VISUAL — ⭐ ĐỔI STYLE 2026-08-21: MINH HOẠ AI KAWAII theo video mẫu `sA59aiPJYLA`

> user đưa `YTSave_YouTube_Media_sA59aiPJYLA_002_720p.mp4` (30′07, kênh đối thủ ngách 60代, bài trứng):
> *"tôi muốn tạo video như này. Xem và sửa cách tạo video cho tôi"* → video 18 là bản đầu tiên chạy style mới.

**Đo bằng máy từ video mẫu (không đoán):**
- 100% minh hoạ AI pastel nền TRẮNG — không một ảnh thật nào.
- **Tĩnh tuyệt đối**: diff 2 frame cách 2s → thân hình 0,5 (nhiễu jpeg), vùng sub 10,8 (chỉ phụ đề đổi). Không pan, không build-on.
- ~3–6 đổi hình/phút (đếm scene-change threshold 0.3: 13 lần/5phút).
- Phụ đề **đen trần to** ở **dải trắng dưới đáy khung** (ngoài vùng hình).
- Nhân vật lặp nhất quán xuyên video (ông cụ tạp dề, bà, cô gái áo trắng) + nhãn/bubble chữ Nhật bake trong hình.

**Pipeline video 18 (đã dựng đủ tool cùng ngày):**

| bước | lệnh / file | ghi chú |
|---|---|---|
| 1. Sinh prompt + SLIDES | `python tools\build_slides_18.py` ✅ đã chạy | **82 minh hoạ** · 4,51 đổi hình/phút · gap min 6,2s · STYLE LOCK (pastel + nét nâu ấm + nền trắng) · 3 nhân vật cố định (ông cụ áo sọc tạp dề olive / 道子さん cardigan vàng / bác tài flannel kẻ) · **6 cảnh có chữ bake** (`1万回`×2 · `×2` · `200g` · `2` · `3`) — soi từng ký tự khi ảnh về |
| 2. User gen 82 ảnh | `06_VIDEO/18_ringo-tabekata/slide_prompts_FLOW.txt` (1 dòng/prompt, bơm extension) | bản người đọc: `_BLOCKS.md`, map tên: `_TENFILE.txt` |
| 3. Ingest | `python tools\ingest_slides_18.py <folder> --cut-x <đo mắt> --apply` | cắt ✦ theo LÔ (tool TỪ CHỐI chạy nếu thiếu `--cut-x`/`--no-cut`) → trim viền + cắt dải trắng/đường kẻ → **đặt vào KHUNG SÂN KHẤU** (xem §9.1) |
| 4. Duyệt contact sheet | mắt, cả 4 góc, 1:1 với 6 ảnh có chữ | `media-library.md` §2.10 ⑤b/⑥ |
| 5. Render | `python E:\Claude\Projects\youtube-jp-health\tools\video_render.py 04_SCRIPTS\18_ringo-tabekata_TTS.md --channel shokutaku --slides 04_SCRIPTS\18_ringo-tabekata_SLIDES_photo.json --reuse` (chạy NỀN, `.cmd` + log) | ⚠️ renderer nằm ở **health/tools**, dùng chung 6 kênh — KHÔNG có bản trong `shokutaku/tools`. Hồ sơ kênh: **`sub_style: "outline"` + `sub_marginv 12`** (chữ TRẮNG trong dải đen sân khấu) + `sub_size 24` · motion False · dissolve 0,45s |

### 9.1 ⭐⭐ VÒNG 3 — KHUNG SÂN KHẤU (user chốt 2026-08-21)

> user đưa ảnh frame của health video 36: *"thế mày làm cho tao cái khung như này còn đẹp hơn đó"*.

Bỏ canvas trắng trơn. Minh hoạ nay nằm trong **khung sân khấu** của `_media_library/make_stage.py`:
nền gradient → **thẻ trắng bo góc** → bóng đổ → **2 nhân vật cắt-nền** 2 mép → **dải đen** đáy.

🔴 **Gọi lại CHÍNH hàm của `make_stage`** (`stage_base` / `put_cast` / `sub_bar`), không chép
hằng số — nếu không thì đổi khung ở tool kia là sinh hai bộ số lệch nhau (`stage-zu-layout.md`
§4 "một việc, một tầng"). Số đo: thẻ **1376×846 @ (272,56)**, bo góc 28, dải đen từ **y=928**
(cao 152), cast cao `CH_H=560`, chân dán đúng `SUB_Y0`.

**Ảnh trong thẻ — cover, có đường lui tự động** (user chốt cover; `LOSS_MAX = 0.12`):
- **75/82 ảnh phủ TRỌN thẻ** (cover-crop) → hết mọi đường mép, hình to nhất cho tệp 45+.
- **7 ảnh tự lùi về FIT** vì cover cắt >12% nội dung. Ca thật: `slide_23` (một đĩa 1 quả vs
  một đĩa 2 quả, đúng câu 「一日に何個までが目安なのか」) bị **cắt mất đĩa PHẢI** ⇒ hình nói
  ngược nội dung. Ảnh fit thì phần thừa là trắng trùng màu thẻ nên vẫn không thấy mép.
- Gate in ra: ảnh nào cover / ảnh nào lùi FIT / **6 ảnh có chữ bake luôn được liệt kê** để soi 1:1.

**Cast riêng của kênh — 12 ảnh** (user chốt: KHÔNG dùng chung cast health), ở `assets/cast/`:
- **みのり (mép trái, 6):** `talk` (nền) · `point` · `hold` (cầm táo) · `stop` (cảnh báo mềm) ·
  `taste` (tự nếm) · `smile` (kết)
- **người nghe (mép phải, 6):** `listen` (nền) · `worried` · `surprised` · `relieved` ·
  `note` (ghi sổ) · `nod`
- Prompt + tool tách nền: `cast_prompts_{FLOW,BLOCKS,TENFILE}.txt` + `tools/cutout_cast.py`.
  **Nền gen là MAGENTA thuần `#FF00FF`, không phải trắng** — cast là cụ già tóc bạc + áo kem,
  tách theo ngưỡng sáng sẽ ăn mất tóc và áo.
- Thiếu cast → khung vẫn dựng được, chỉ không có người; ingest in `⚠️ CHUA CO CAST n/12`.
- ✅ **ĐÃ CẮT XONG 12/12 (2026-08-21)** — `python tools\cutout_cast.py "<folder>" --apply`.
  Ba luật đúc từ lô này, đã ghi vào `media-library.md` §2.10 ⑨ (mọi kênh cần cast dùng lại):
  **① chữa vệt tím phải CO MASK 3px vào viền trắng sticker**, không "sửa màu" pixel viền
  (cách sai đã đo: hạ R/B theo G → 1.400/1.400 px vẫn tím, vì magenta có G≈0 nên ra
  `(145,0,90)` vẫn đỏ tím) — sau khi vá còn **0–24px** · **② lọc blob lớn nhất** vì dấu ✦
  là trắng nhạt trên magenta nên ngưỡng màu không loại, bbox sẽ phình tới góc ·
  **③ ghép tên phải khoá GIỚI TÍNH trước** (token-overlap từng cho `minori_smile` bắt vào
  `Man_listening_with_interested_smile`).

**Vòng 4 cùng ngày** (user: *"ảnh avatar gần khung tí chứ, với ảnh đang không đều nhau cao thấp
to nhỏ khác nhau, với lại thêm text hoặc hiệu ứng sticker gì đi chứ nhìn các frame nó bị tẻ
nhạt quá"*) — ba việc:

**a) Cân avatar theo CỠ ĐẦU, không theo chiều cao** (`HEAD_PX = 230`, `CAST_H = 478`).
Đo được: đầu chiếm **34%–48%** chiều cao ảnh, **lệch 1,41×** — đúng cái mắt thấy.
🔴 **Xung đột hình học, phải chọn:** ảnh gen crop khác nhau nên **không thể vừa đầu-bằng-nhau
vừa cao-bằng-nhau**. Chọn ĐẦU (make_stage cũng ghi: *"cân theo CỠ ĐẦU, không theo chiều cao
khung"*) → scale cho đầu = 230px → **cắt bớt phía dưới** cho mọi ảnh cao đúng 478 → dán đáy ở
`SUB_Y0`. Kết quả: đầu cùng cỡ, đỉnh đầu cùng độ cao, chân cùng mốc.
⚠️ **Phép đo đầu: dùng BỀ RỘNG đầu, không dùng mốc vai.** Cách mốc-vai (bề rộng tăng vọt) thất
bại vì **7/12 ảnh có tay đưa lên ngang đầu** → `minori_taste` báo "đầu = 99,8% chiều cao ảnh".
Cách đúng: bề rộng trung vị ở dải **y 6%–14%** từ đỉnh (chỉ có tóc), rồi suy chiều cao đầu
theo tỉ lệ 0,72.

**b) Sát thẻ** (`CAST_GAP = 8`): dán theo **mép TRONG** cách thẻ 8px, thay cho `x = ±34` cố
định của make_stage. Avatar rộng hơn dải 272px thì lòi ra ngoài mép khung ≤~30px — giống khuôn
mẫu, không đè lên thẻ.

**c) Lớp chữ + sticker** (`CHIP_MAP`, 15 đoạn): **chip nhãn đoạn** navy góc trên-trái thẻ
(「その一口の坂道」「① 皮という鎧」「私も試してみました」…) + **dấu nhấn** tròn **ngay CẠNH chip**
(`！` đỏ cảnh báo · `✓` xanh mẹo · `＋` vàng khối số). Vẽ bằng **font Noto của make_stage** nên
chữ Nhật luôn sắc nét — khác hẳn chữ bake bằng AI.
🔴 **Dấu nhấn KHÔNG đặt góc trên-PHẢI** — bản đầu đặt ở đó và bị **watermark 「60代の食卓」 đè**
(renderer dán watermark 328×133px ở góc trên-phải khung **SAU** khi ghép slide, nên tầng ingest
không thể "tránh" bằng cách vẽ trước). Bắt được bằng mắt trên frame render: một cục cam lòi ra
bên trái badge vàng. ⇒ Tầng ingest chỉ được dùng góc trên-TRÁI của thẻ.

🔧 **Thêm cờ `--from-orig`**: dựng lại 82 slide từ backup `_wm_orig/` khi chỉ đổi khung/cast,
khỏi cần folder Downloads (lô `download (8)` đã bị dọn giữa buổi và ingest trả "ghi 0 ảnh").
⚠️ Ở chế độ này **không copy2 backup** — nguồn chính là file trong `_wm_orig`, copy đè lên chính
nó ra `PermissionError WinError 32`.

🔴 **`POSE_MAP` — đổi tư thế 18 lần theo đoạn bài** (`ingest_slides_18.py`). Bản đầu chỉ có 4 tư
thế và dán **một cặp cố định cho cả 82 thẻ** → user: *"ít biểu cảm thế thôi à"*. Bài học: **có 12
ảnh mà dán một cặp thì cũng như có 1 ảnh** — biểu cảm phải đi theo nội dung. Bảng đọc theo dải
index của `PLAN` trong `build_slides_18.py`: cold open `talk+worried` → vỏ táo `hold+listen` →
số 2 lần `point+surprised` → cách rửa `stop+note` → persona `smile+listen` → cảnh báo kali
`stop+worried` → case 道子 `talk+listen` → payoff áo giáp 2 `point+surprised` → tự nếm
`taste+note` → case bác tài `talk+relieved` → recap/kết `smile+nod/relieved`.

⚖️ **Cái mất:** ① thẻ 1376×846 nhỏ hơn canvas cũ 1920×890 ⇒ minh hoạ hiển thị nhỏ hơn ~28% diện
tích, bù lại có chiều sâu + nhận diện kênh; ② cast lệch style là rủi ro thật — vì thế phải gen
riêng theo STYLE LOCK pastel, đừng lấy bộ line-art của kênh khác.

**Demo đã duyệt mắt:** `scratchpad/demo_kuro.jpg` — canvas trắng + minh hoạ giữa-trên + phụ đề đen to dưới đáy, khớp bố cục mẫu.

**Compliance (điểm lợi của style này):** minh hoạ cartoon **KHÔNG realistic** → **KHÔNG phải tick "altered/synthetic content"** (`youtube-compliance.md` §2 chỉ bắt nội dung realistic dễ lầm là thật) — né được nhãn "Altered content" ăn vào độ tin YMYL mà §2.1 đã cảnh báo.

**Cái mất, ghi thẳng:** ① 82 ảnh AI/video = công gen nặng hơn fetch ảnh thật (mẫu đối thủ chấp nhận giá này); ② kanji bake dễ nát — đã tối thiểu hoá còn 6 cảnh chữ ngắn; ③ luật cũ "entry 0 = ảnh chủ thể THẬT" (`media-library.md` §2.0) nay thi hành bằng minh hoạ táo — vẫn đúng tinh thần (che chữ vẫn biết video nói về táo).

## 10. HANDOFF

Đã xong: script + gate PASS + SLIDES 82 entry + bộ prompt FLOW/TENFILE/BLOCKS + tool ingest + hồ sơ kênh đổi sub. **Chờ user: gen 82 ảnh theo `slide_prompts_FLOW.txt`** → ingest (đo ✦ trước) → duyệt sheet → render nền. Thumbnail: prompt ở §6, user gen, quét ✦, gate 168px như cũ.
