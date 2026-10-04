# 08 — SỔ THEO DÕI SỐ · 真夜中の朗読便

> Mở 2026-08-12 cùng lượt khám kênh (`CHANNEL_DIAGNOSIS_2026-08-12.md`).
> Sổ này tồn tại vì **hai phép đo đã bị bỏ khỏi tự động** và nếu không có chỗ ghi thì chúng sẽ trôi:
> ① CTR (Google rút khỏi API 2026-07-30 → phải đọc TAY trong Studio) ② bộ A/B thumbnail (chouhen tạm
> về 1 bản, `.claude/rules/ab-3title-3thumb.md` §6 → A/B giờ chạy tuần tự theo lô, phải tự so).

---

## 0. VIỆC ĐỊNH KỲ — không làm thì ngoại lệ 1+1 thành "bỏ đo"

| việc | nhịp | cách làm |
|---|---|---|
| **Đọc CTR tay trong Studio** | **1 lần/tuần** | Mở Chrome profile `Default` (`.claude/rules/channel-browser.md`) → Studio → Content → cột "Impressions click-through rate". Ghi vào §2 |
| Đo view/AVD/traffic toàn kênh | 1 lần/tuần | `python tools/channel_diag.py --traffic` |
| Đo lại bộ peer cùng rail | 4–6 tuần | `python tools/channel_diag.py --peers` (bỏ trống `--peer-name` = tự suy từ RELATED) |
| **Gom lại kho premise** | 4–6 tuần | `python tools/channel_diag.py --premises --days 30` → cập nhật `01_SOURCES/PREMISE_BANK_*.md` |

📦 **Kho premise hiện hành:** `01_SOURCES/PREMISE_BANK_2026-08-12.md` — 40 premise từ 246 video peer
≤30 ngày; **15 bản dùng ngay** (POV nữ, sạch compliance), 7 bản POV nam, 6 bản trùng video cũ, 12 loại.

---

## 1. MỐC GỐC — 2026-08-12 (trước khi đổi bao bì)

Nhóm chứng để so. **Không sửa title/thumbnail của 24 video này** (`CLAUDE.md` §Title).

| chỉ số | giá trị |
|---|---|
| kênh | 5 sub · 1.044 view · 24 video |
| **trung vị view/video, 10 video 07-31→08-12** | **2** |
| view/video cao nhất | 367 (07-27) |
| số video có RELATED ≥50 | **0/11** (10 video gần nhất) |
| `BROWSE_FEATURES` | **0 tuyệt đối, 24/24 video, suốt đời kênh** |
| AVD 3 video gần nhất có số | 49,7 · 49,8 · 53,1% ← **cao mà vẫn 2–5 view** |
| CTR | ⛔ chưa đo (Google rút khỏi API) |

**Ngưỡng "ăn" ở lần đo 2026-08-22** (sau 10 video bao bì mới):

| chỉ số | ngưỡng |
|---|---|
| trung vị view/video 10 video mới | **≥20** |
| số video có RELATED ≥50 | ≥2/10 |
| `BROWSE_FEATURES` > 0 | **>0 lần đầu = mốc quan trọng nhất** |

🛑 **Phanh:** trung vị vẫn ≤5 → bao bì KHÔNG phải nguyên nhân → mở GĐ4 (thử độ dài 90–150′),
đừng làm vòng bao bì thứ hai.

---

## 2. NHẬT KÝ ĐO

### 2.1 CTR đọc tay (Studio)

| ngày đo | video | CTR | impressions | ghi chú |
|---|---|---|---|---|
| *(chưa có — lần đầu: 2026-08-19)* | | | | |

### 2.2 Lô A/B thumbnail (tuần tự, mỗi khuôn 5 video)

| lô | khuôn | video | ngày | trung vị view | trung vị CTR |
|---|---|---|---|---|---|
| **L1** | **K1** text-wall + dàn người (mẫu 毎日スカッと 105K) | 24–28 | từ 2026-08-13 | — | — |
| **L2** | **K2** cảnh sáng kể chuyện (mẫu 語り茶屋 205K) | 29–33 | — | — | — |

⚠️ **GIỮ NGUYÊN khuôn title suốt cả 2 lô** — đổi title giữa chừng là lẫn 2 biến, cả phép đo thành vô nghĩa.

### 2.3 🔴 MẪU ĐỔI NHIỀU BIẾN — đọc RIÊNG, đừng gộp vào trung vị GĐ1

| video | ngày | biến đổi kèm | thuộc về |
|---|---|---|---|
| **24** `gencho-no-nagagutsu` | dự kiến 2026-08-13 | **độ dài 59′59** (bao bì mới **+** độ dài) | **GĐ4 (thử độ dài)**, KHÔNG phải mẫu sạch của GĐ1 |

**Vì sao phải tách ra:** kế hoạch GĐ1 giữ **27–40′** chính là để phép đo bao bì sạch một biến. Video 24
đổi **cả hai** cùng lúc → view của nó **không quy được** cho bao bì hay cho độ dài.

Hai phép đo đang chỏi nhau ở đúng dải này, ghi cả hai để sau khỏi cãi:
- **CHỐNG:** 6/6 video 50′+ của chính kênh đều chết — 55′31→14 view · 51′48→26 · 1h07→16 · 1h00→6 ·
  1h17→5 · 1h04→4. Gate in ra: AVD 33% (mốc mở rail) ở bài 60′ đòi **19,8 phút xem**, kỷ lục kênh là
  **15,6′** ⇒ đòi vượt kỷ lục **+27%**, chưa có tiền lệ.
- **ỦNG HỘ:** bộ peer đo 2026-08-12 chạy **64–153′** và thắng (語り茶屋 bản **64′** = 4.591 view/ngày;
  毎日スカッと 148′ = 54.445 view/ngày).

📌 **Cách đọc ngày 22/08:** tính trung vị GĐ1 **trên các video 27–40′** (25, 26, 27, 28…); video 24 ghi
riêng một dòng. Nếu 24 ăn view mà mấy bản 27–40′ thì không → **độ dài** là biến ăn, không phải bao bì —
và kết luận đó đảo ngược thứ tự ưu tiên của cả kế hoạch.

⚙️ **Đã áp cho video 24 (2026-08-12):** câu **xin đăng ký** ở **54:18 = 90,7%** (chèn vào cả `_TTS.md`
lẫn `.md`), mốc chương dịch +35s, gate `check_retention` **12/12 qua**, 0 tag đặt sai. Đây là video
**đầu tiên của kênh có lời xin đăng ký trong tiếng đọc** — 21/22 bài trước đó không có (§4.1).

### 2.4 Đổi title (chỉ sau khi chốt xong khuôn thumbnail)

| ngày | bản | ghi chú |
|---|---|---|
| **2026-08-12** | **khuôn CÂU VĂN TRẦN** thay khuôn tag-đầu 【スカッとする話】…【修羅場】【朗読】 | áp từ video 24. Căn cứ: 0/25 video peer cùng rail mở bằng 【】 |

---

## 3. THAY ĐỔI ĐÃ ÁP (để sau đọc số không lẫn nhân quả)

| ngày | đổi gì | file |
|---|---|---|
| 2026-08-12 | TITLE → câu văn trần, keyword xuống đuôi | `CLAUDE.md` §Title · skill `script-chouhen` MỤC 15 |
| 2026-08-12 | THUMBNAIL → bắt buộc ≥2 người đang diễn + vật chứng; bỏ nền dập gần đen; 2 khuôn `--preset k1/k2` | `CLAUDE.md` §THUMBNAIL · `tools/make_thumb_textwall.py` |
| 2026-08-12 | SEO nhẹ: mô tả ~300 ký · 0–8 tag · bỏ 目次 | `.claude/rules/youtube-upload-seo.md` §5 · `tools/upload_pack.py` |
| 2026-08-12 | A/B 3×3 → 1 title + 1 thumbnail | `.claude/rules/ab-3title-3thumb.md` §6 |
| 2026-08-12 | Bỏ FX.json viết tay + ambience bed (GIỮ `--bgm auto`) | `CLAUDE.md` §Lớp FX |
| 2026-08-12 | **Thêm câu XIN ĐĂNG KÝ ở ~90%** (áp từ video 24) | `03_SCRIPTS/24_*_TTS.md` + §4.1 dưới |

🔴 **Sáu thay đổi này áp CÙNG MỘT LÚC** — nếu view lên thì **không tách được** cái nào ăn. Đó là đánh
đổi có chủ ý: kênh đang ở 2 view/video, tách biến từng cái một sẽ mất 6 lô × 10 video = quá chậm.
Lô L1 vs L2 là phép đo **sạch một biến** duy nhất trong đợt này (chỉ khác khuôn hình).

📌 **Ngoại lệ đọc riêng:** câu xin đăng ký (dòng cuối bảng) **không ảnh hưởng view** — nó chỉ ảnh hưởng
**sub/view**. Nên nó KHÔNG làm bẩn phép đo view của L1/L2; đọc nó bằng chỉ số riêng là **tỉ lệ chuyển
đổi sub** (mốc gốc **0,58%**, §4).

---

## 4. 🎯 MỤC TIÊU: BẬT KIẾM TIỀN — nút thắt là SUB, không phải giờ xem

User chốt 2026-08-12: mục tiêu của kênh là **bật kiếm tiền**. Số đọc thẳng từ Studio (tính đến 07/08):

| | hiện tại | ngưỡng |
|---|---|---|
| Người đăng ký | **5** | **500** |
| Giờ xem đủ điều kiện (365 ngày) | **194** | **3.000** |
| Video đăng trong 90 ngày | 3 | 3 ✅ |

⚠️ Đây là mốc **hội viên / Supers / mua sắm**, **KHÔNG phải quảng cáo**. Tiền quảng cáo ở mốc sau
(**1.000 sub + 4.000 giờ**) — Studio vẫn khoá, ghi "Cột mốc trong tương lai".

**Tỉ lệ đo được của kênh:** `0,58%` view → sub · `11,8` phút xem/view. Quy ra:
- **3.000 giờ** → chỉ cần **~15.300 view** tích luỹ
- **500 sub** → cần **~86.000 view** tích luỹ

🔴 **Giờ xem chạm đích trước sub 5,6 lần ⇒ ĐỪNG tối ưu giờ xem, nó tự đến. Chỉ số duy nhất cần theo
dõi là SUB, và đòn bẩy duy nhất là tổng VIEW.** So nhịp 14 ngày gần nhất: giờ xem cần ~2×, sub cần ~19×.

**Chuyển đổi 0,58% là BÌNH THƯỜNG của ngách** (裏話オーディオ 1,05% · 孤独な桜の木 0,45% · 毎日スカッと 0,41% ·
語り茶屋 0,35%) ⇒ **không phải chỗ sửa được nhiều**. Khoảng cách nằm hoàn toàn ở **view/video: chouhen 43
vs peer 9.975–70.850 (chênh 232×–1.648×)**.
⭐ 語り茶屋 chỉ **45 video / 11,5 tháng → 6.080 sub** ⇒ **không cần hàng nghìn video, cần view/video.**

### 4.1 🔴 Lỗ đã bắt được 2026-08-12: 21/22 kịch bản KHÔNG hề xin đăng ký

Câu CTA canonical của kênh (`cta-midvideo.md` §2.1) chỉ có **高評価 + シェア + コメント — không một chữ 登録**.
Đây là kênh **NGHE** (nữ 45–70, làm việc nhà / trước khi ngủ, không nhìn màn hình) ⇒ nút チャンネル登録 đỏ
trong CTA overlay gần như vô dụng. Mục tiêu duy nhất là sub, mà 24 video chưa từng mở miệng xin sub.
⚠️ Suýt đếm sai: `grep 登録` ra 8/14 file "có", nhưng đọc kỹ **toàn là từ trong truyện**
(「登録が消えています」「登録は取り直した」). Đếm đúng lời xin đăng ký: **1/22**.

**Đã sửa — chèn ở ~90%, KHÔNG ở cuối.** Căn cứ đo `audienceWatchRatio`:

| video | 50% (CTA hiện có) | **90%** | 100% |
|---|---|---|---|
| 07-30 | 53,7% | **52,0%** | 43,1% |
| 07-27 | 41,8% | **43,4%** | 28,1% |
| 07-25 | 35,2% | **31,5%** | 24,5% |
| 08-10 | 41,2% | **35,3%** | 11,8% |

Mốc 90% giữ gần bằng mốc 50%; mốc 100% mất **7–23 điểm**. Câu này còn kiêm **re-hook giữ người qua đoạn
vĩ thanh cuối** — đúng quãng 08-10 rơi từ 35,3% xuống 11,8%.
⚠️ **KHÔNG nhét 登録 vào CTA giữa bài** (đang cố ý rút gọn 2 câu để giữ immersion 朗読; xin 4 thứ một lúc
là loãng) và **KHÔNG đụng NHỊP 9** (chữ ký verbatim). **Một ask, một chỗ.**

### 4.2 Hai việc chưa làm, đánh thẳng vào nút thắt SUB
1. ⏳ **Đưa câu xin đăng ký vào `cta-midvideo.md` §2.1** thành CTA thứ hai chính thức của chouhen + vào
   skill `script-chouhen` để mọi bài sau tự có. *(hiện mới áp tay cho video 24)*
2. ⏳ **End screen + xâu chuỗi playlist cho 24 video cũ** — đo được **0 view đến từ video của chính kênh**;
   24 video không đỡ nhau. Làm hàng loạt trong Studio, tăng **cả** giờ xem **lẫn** sub. Không cần render.

## 5. LIÊN QUAN
- `CHANNEL_DIAGNOSIS_2026-08-12.md` — bằng chứng gốc của cả 5 thay đổi
- `RETENTION_FORMULA_2026-08-11.md` — giữ nguyên, nhưng **không phải thứ quyết định view**
- `.claude/rules/channel-browser.md` — chouhen = Chrome profile `Default`
