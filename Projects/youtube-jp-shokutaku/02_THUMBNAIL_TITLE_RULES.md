# Bộ quy tắc Thumbnail + Title — 60代からの食卓 (dùng chung health)

> **v5 WARNING-FIRST — 2026-07-21.** User chốt sau mổ đối thủ chuẩn 長生きの秘訣 (96,6K sub/12 tháng, chi tiết `CHANNEL_OPTIMIZE.md` Mục 5): CTR kênh 1,7–2,4% vì title/thumbnail khung 「良い」 phát tín hiệu sai rổ. Chuẩn mới: **KHUNG CẢNH BÁO mặc định + chữ khổng lồ đọc được ở rail 120px + giấu đáp án コレ/この**. Xem Phần E (chuẩn kênh v5) + Phần B (title cảnh báo).
> **Skill `script-shokutaku` Mục 15 B–E và health CLAUDE.md phải theo file này.** Compliance gốc: `.claude/rules/youtube-compliance.md`.
> Lịch sử: v3 MARKET-FIRST 2026-07-11 (chữ lớn 3 dòng MÓN/TWIST/STAKE — vẫn là xương phần A); chuẩn hình "FULL-BLEED tối moody" của v3/v4 → **hạ xuống làm biến thể phụ** từ v5 (đẹp nhưng thua meta rail — cùng bài học chouhen). Bản v2 cũ → git history; thumbnail đã render giữ nguyên file, KHÔNG xoá.

## 0.1 ⭐ v6 — ĐỢT LÀM LẠI 10 THUMBNAIL LIVE (2026-08-05)

> **Bộ prompt + khuôn khoá + bảng 10 video: `06_VIDEO/_thumb_audit/PROMPTS_v6.md`.** Đo bản live 12 video bằng máy → 3 video RỚT gate đọc được (04 牛乳 13,6% & sáng 38 · 06 16,7% · 05 19,4%), **6/12 nền tối** dù v5 đã hạ khuôn moody xuống biến thể phụ, **9/12 thiếu dấu nhận diện**.
> **Khuôn chuẩn = video 11 麦茶 + 12 ヨーグルト** (2 bản đo tốt nhất, được chừa lại): dải vàng mép trái 1,41% ngang #FFDE00 · badge tròn 食卓 #FF3D31 đường kính 25,7% cao, đặt góc ĐỐI DIỆN cột chữ · 3 dòng 袋文字, dòng 2 to nhất · ảnh SÁNG 1 chủ thể.
> 🔴 **Dải vàng + badge đóng bằng TOOL, không để AI bake** — nhận diện phải giống từng pixel: `tools/stamp_brand_shokutaku.py --corner tr|tl|br|bl`.
> ⚠️ Nhắc lại để không trôi: `CLAUDE.md` §CHIẾN LƯỢC đã đo được **thumbnail KHÔNG phải bệnh của kênh này** (BROWSE=0 cấp kênh; bệnh là rớt trước giây 45). Đợt v6 làm vì gate đọc được + nhận diện + A/B 3×3, KHÔNG phải để chữa CTR.

## 0. Nguyên tắc gốc: CHỮ LÀ THUMBNAIL

Ngách 60–80 tuổi Nhật click vì **lời hứa/cảnh báo cụ thể đọc được trong 0,5 giây**, không phải vì ảnh đẹp. Ảnh chỉ là nền + bằng chứng món ăn. Trước khi render phải trả lời được: *"Người xem đọc được GÌ trong 0,5 giây, và mất gì nếu không xem?"*

## 0.5 ⭐ 3 NGUYÊN TẮC GÁC CỔNG HÌNH (user chốt 2026-07-16 — áp MỌI kênh, quét trước khi render)

> **"Thumbnail không phải để đẹp — mà để người ta DỪNG LẠI."**

1. **Cắt bỏ chi tiết thừa:** 1 điểm nhấn duy nhất (mặt/vật thể) + 1 hình tương phản cao. Ảnh scene nhiều lớp (vườn + đèn + chậu + vòm…) = fail gate — crop chặt vào chủ thể hoặc đổi ảnh.
2. **Phóng đại cảm xúc:** người xem không phản ứng với THÔNG TIN — họ phản ứng với CẢM GIÁC. Video cảnh báo → làm rõ "nguy hiểm" (to, đáng sợ, sát mặt); video hướng dẫn → show KẾT QUẢ CUỐI (thành quả, trạng thái sau khi làm). Chữ cũng chọn từ cảm giác (大嫌い/危険/捨ててた) thay vì từ mô tả.
3. **Test mobile:** thu nhỏ 120px vẫn phải rõ — **nền đậm, chủ thể sáng**, tương phản cao. Không đạt = làm lại, không thương lượng.

(3 nguyên tắc này là tầng LỌC HÌNH, chạy TRƯỚC các luật chữ A1–A5 bên dưới; không thay thế chúng.)

---

## Phần A — Thumbnail

### A1. 2–3 dòng chữ lớn, phủ 50–70% khung, KÍN CHIỀU CAO ⭐ ĐỔI so với v2
- Mỗi dòng ≤8 ký tự Nhật, font đậm (YuGothB), **cột chữ xếp dọc chiếm nửa trái** (hoặc phải) khung; món ăn/mặt người chiếm nửa còn lại.
- **Khối chữ phải kín ~86% chiều cao khung** (mẫu 1,3M: chữ chạm mép trên xuống mép dưới, không lề thừa) — tool flag `--fill` tự phóng. Khoảng trống trên/dưới nhiều = chưa đạt.
- **Nền tối nhưng MÓN phải RÕ** (bài học vòng 3, 2026-07-11): KHÔNG dim toàn ảnh đè chết chủ thể — ưu tiên **ảnh có nền tối sẵn / chủ thể lệch một bên** (`--focus left|right`), chữ chiếm phía "trống", món phía kia để nguyên sáng; side-scrim của tool chỉ tối phía cột chữ. `--dim` toàn ảnh chỉ dùng ≤0.15 khi ảnh quá sáng đều. Ảnh không có phía trống → tìm ảnh khác (Pexels), đừng cố dim.
- **Banner/box màu cho dòng neo** (mẫu 273K: banner đỏ chữ trắng dòng đầu) — `--box 1:red`; dùng cho 1 dòng, không lạm dụng cả 3.
- 2 dòng chỉ dùng khi 3 dòng không đủ ý ngắn gọn; 4 dòng = trần (theo mẫu 1,3M), không mặc định.

### A2. Cấu trúc 3 dòng — ⭐ v5: KHUNG CẢNH BÁO là mặc định
**Công thức mặc định (đúc từ bộ hit 長生きの秘訣 485K–695K): HÀNH VI QUEN → HẬU QUẢ → ĐÁP ÁN GIẤU**
1. **Dòng HÀNH VI** (trắng): thói quen người xem ĐANG làm — 「知らずに買う」「まだ食べてる？」「毎朝やってる？」「電子レンジ習慣」.
2. **Dòng HẬU QUẢ** (đỏ hoặc vàng, to): 「寿命を縮める」「腎臓が壊れる」「海外ではNG」「逆効果！?」.
3. **Dòng ĐÁP ÁN GIẤU** (màu còn lại): 「危険なパン」「この食品」「正解はコレ」「1位は◯◯」 — người xem PHẢI bấm mới biết là món nào.
- Biến thể cũ **MÓN → TWIST → STAKE** (v3) vẫn dùng được cho video khung lợi ích/minh oan — nhưng không quá 1/3 số video, và STAKE vẫn bắt buộc cụ thể.
- Claim mạnh phải có giới hạn đứng cạnh: 「!?」「かも」「半分」「9割」(số chỉ dùng khi có thật trong script).
- **Device mũi tên/khoanh đỏ (chuẩn thị trường):** mũi tên đỏ trỏ vào vật/vùng đáp án hoặc vòng khoanh đỏ trên món — thêm 1 lớp "nhìn vào đây". Dùng khi ảnh có vật đáp án rõ; tool chưa có flag thì ghép thủ công/Pillow khi render (nâng cấp make_thumb khi làm video v5 đầu tiên).

### A3. Màu: trắng nền + vàng + đỏ, viền đen dày ⭐ ĐỔI so với v2
- Cho phép **2 màu nhấn cùng lúc** (vàng #FFDE00 + đỏ #FF3E30) như chuẩn thị trường — hết luật "1 màu duy nhất".
- Mọi dòng 袋文字 viền đen dày; nền sau cột chữ scrim tối để nổi trên mọi ảnh.
- Vẫn cấm: cầu vồng >3 màu chữ, hộp nền che quá nửa món.

### A4. Thiết bị curiosity — chọn 1 mỗi video
- **「これ」 device** (chuẩn thị trường, đã kiểm chứng 33K + 1,3M): giấu đáp án bằng chữ これ ở dòng TWIST — 「これを混ぜると」「これと食べると」. Đáp án phải có thật trong video.
- **Mosaic + viền + 「？」** (kế thừa v2): khi có "vật đáp án" chụp được — mosaic vật + viền màu nhấn + ？ to. Dùng cho layout có món hero rõ.
- **Benefit đánh số ①②** (mẫu 273K): video dạng list lợi ích — 2 dòng stake đánh số tròn.
- ❌ **Bỏ hook 「そのN、あなたも」 làm mặc định** — số thứ tự không ai hiểu khi chưa xem video (bằng chứng: 2 video dùng nó đều chết CTR). Chỉ còn dùng làm biến thể thử nghiệm khi đã có video khác cùng công thức chạy tốt.

### A5. Ảnh nền: món ăn macro là mặc định, mặt người là gia vị
- **Mặc định: món ăn close-up/macro, sáng, thèm mắt hoặc kịch tính**, phủ full khung 16:9, `--pop` bơm màu — mẫu thắng của ngách đa số không cần mặt người.
- ⭐ **GATE ảnh nền (CHỐT 2026-07-11, sau 4 vòng chỉnh video trứng): đo ảnh GỐC trước khi render — chủ thể phải ≤~50% bề ngang VÀ lệch hẳn một bên, phía còn lại là vùng trống/tối đặt được cột chữ.** Đo bằng code (bbox pixel sáng), không ước lượng bằng mắt. Chủ thể choán khung (kiểu trứng chiếm 18–70% bề ngang) = KHÔNG cứu được bằng crop/focus/dim → fetch ảnh khác (Pexels → lưu `06_VIDEO/<x>/_thumb_candidates/`).
- ⭐ **Ảnh fail gate mà vẫn muốn dùng → chế độ `--panel` NHƯNG PHẢI MANG VIBE v23 (sửa 2026-07-11 sau khi user chê "panel cứng" ở video jinzo):** ảnh món một bên + vùng đen đặt chữ bên kia, **bắt buộc `--panel-fade ≥340`** để ảnh TAN DẦN vào bóng tối như ảnh low-key tự nhiên — KHÔNG lộ mép cắt thẳng đứng kiểu 2 ô ghép. Kèm **banner đỏ dòng 1 (`--box 1:red`) + trắng + vàng** = bộ nhận diện chuẩn v23. Chữ KHÔNG BAO GIỜ đè món. Fade nhỏ (mép rõ kiểu 1,3M) chỉ dùng khi user yêu cầu riêng.
- **Chữ và món KHÔNG được đè nhau** — chữ chiếm phía trống, món nguyên độ sáng phía kia; side-scrim của tool chỉ tối phía chữ.
- Mặt người cao tuổi (gương mặt kênh cố định: bà cụ tạp dề be = shokutaku; ông cụ cardigan be = health) dùng để **xoay vòng chống trùng layout**, biểu cảm phải MẠNH (sốc/tiếc của), crop sát.
- ⭐ **Video ORGAN-TOPIC (chủ đề chính là TẠNG: 腎臓/肝臓/心臓…, món chỉ là ví dụ) → HÌNH phải có TẠNG (chốt 2026-07-11 sau 3 vòng feedback video jinzo):** chữ đã gánh tên món thì ảnh chỉ có món = thiếu ý chính. **Cách làm chuẩn: tạng = ẢNH MÔ HÌNH GIẢI PHẪU THẬT cắt nền (cutout), grade theo tông ảnh (brightness ~0.8 + phủ ấm) + bóng đổ, đặt CHÌM VÀO CẢNH như vật thật** — nền vẫn full-bleed moody v23 một ảnh liền. ❌ CẤM sticker いらすとや/hoạt hình đè lên ảnh photo-moody (user chê "khác hẳn chuẩn kênh" — collage phá vibe; いらすとや chỉ hợp nếu cả thumbnail theo style card). ❌ CẤM lấy nguyên ảnh mô hình sáng trắng làm nền (lệch tông moody). Nguồn tạng: Wikimedia CC0/stock, né logo hãng trên model. (Mẫu chốt: `01_jinzo-tabemono/thumbnail_v6_moody.png` + script tái tạo `design_thumb_v6.py` cùng folder.)
- **CẤM:** áo blouse trắng, ống nghe, phòng khám, mặt người thật cụ thể. Ảnh AI nhân vật hư cấu = production assistance, không cần tick synthetic.
- Prompt gen ảnh phải khóa bố cục: `food LARGE right half / left half simple-dark for big text column / no text, no doctors`.

### A5.5 ⭐ DẤU NHẬN DIỆN KÊNH — bắt buộc mọi thumbnail (user chốt 2026-08-03)

> User: *"tôi muốn thumbnail sao để những lần sau họ biết đó là kênh của mình"*.

**KHÓA: style `seal`** — **dải dọc vàng 26px bên trái + con dấu tròn ĐỎ viền trắng chữ 「食卓」 ở góc dưới-trái.** Đóng bằng tool, chạy SAU `make_thumb.py`:

```bat
python tools\brand_stamp.py <thumb.png> <thumb.png> --style seal
```

- **Vì sao là con dấu 2 ký chứ không phải tên kênh:** ở **168px** (cỡ thẻ mobile thật) chuỗi 「60代からの食卓」 7 ký **teo mất chữ**, chỉ còn một vệt màu — đo thật 2026-08-03 khi so 3 phương án (`bar` dải chân trang · `frame` viền vàng + tag đỏ · `seal`). Chỉ **2 ký tự cỡ lớn** mới còn đọc được ở cỡ đó. Nhận diện phải sống ở cỡ nhỏ, không phải ở cỡ full.
- **Vì sao không lấy vị trí cột chữ làm nhận diện:** A6 buộc xoay layout trái↔phải giữa các video (chống lặp) → nhận diện phải là dấu **CỐ ĐỊNH cùng chỗ/cùng màu mọi video**, tách khỏi biến layout.
- **Không được đè cột chữ chính** — dấu nằm ở dải mép dưới-trái, cao ≤27% chiều cao ở góc, không ăn vùng chữ (gate `audience-45plus.md` §1 vẫn phải đạt: dòng chính ≥1/3 khung).
- 2 phương án bị loại giữ trong `brand_stamp.py` (`--style bar|frame`) để đối chiếu sau; **đừng đổi style giữa các video** — đổi dấu = mất nhận diện, đúng cái luật này ra đời để chống.

#### A5.5b 🔴 CHỖ ĐẶT DẤU vs CHỮ GEN TRONG ẢNH — ca thật video 11 (2026-08-05)

Thumbnail có **chữ gen sẵn trong ảnh** (user chốt 2026-08-05: *"tao muốn prompt có chữ luôn không cần mày đè chữ"*) → tool không còn biết cột chữ nằm đâu, và ở video 11 cột chữ nằm **bên TRÁI, 3 dòng chạy tới sát mép dưới** → con dấu ở nhà mặc định (dưới-trái) **đè mất 2 ký đầu của 「捨てないで」**, đọc thành 「…てないで」.

- ✅ **Đã thêm cờ `--corner bl|tl|tr`** vào `brand_stamp.py`. **Mặc định vẫn `bl`** (nhà của dấu, giữ nhận diện). `tr` là **ngoại lệ** khi cột chữ chiếm hết mép dưới-trái. ⛔ **KHÔNG bao giờ `br`** — góc dưới-phải là chỗ YouTube in timestamp thời lượng.
- ⚠️ **Đánh đổi phải biết:** dời dấu = mất một phần nhận diện "luôn cùng một chỗ". Nên **cách đúng về lâu dài là ép PROMPT chừa trống góc dưới-trái**, không phải dời dấu mỗi video.
- ➡️ **Bổ sung bắt buộc vào mọi prompt gen chữ-trong-ảnh từ nay:** thêm câu
  `keep the bottom-left corner of the frame free of text (reserved for a channel stamp)`
  — và khi cột chữ ở bên trái thì để **dòng cuối kết thúc trên ~78% chiều cao**.
- Video ĐÃ đăng: đóng dấu dần khi sửa metadata trong Studio, không re-render.

### A6. Xoay vòng layout (chống inauthentic + chống nhàm)
Giữ nhận diện (font, bộ màu trắng-vàng-đỏ) nhưng video liền kề không dùng cùng layout:
- **Layout A (mặc định):** món macro full nền + cột 3 dòng chữ trái.
- **Layout B:** mặt người biểu cảm + món + cột chữ (chữ vẫn ≥50% bề ngang).
- **Layout C:** chia đôi ✅/❌ hoặc mosaic ？ + 2–3 dòng chữ.
Ghi layout đã dùng vào block Đóng gói CTR của từng script.

### A7. Bài test 120px + 🔴 GATE 168px (siết 2026-07-27 — áp MỌI kênh food/health)
Thu về 120px: phải đọc được **dòng STAKE** + nhận ra món trong 1 giây. Tool tự xuất preview **480 / 168 / 120** — không đạt thì tăng cỡ chữ, đừng giảm số dòng.

**🔴 GATE 168px bắt buộc (chốt 2026-07-27):** mở `*_preview168.png` (168×95 = cỡ thẻ mobile/sidebar THẬT). **Không đọc được DÒNG CHÍNH → LÀM LẠI, không được giao.** Phải MỞ FILE RA XEM, không được "chắc là đọc được".

> **Vì sao thêm gate dù đã có 120px:** audit health 2026-07-27 (`youtube-jp-health/CHANNEL_DIAGNOSIS_2026-07-27.md` §2.6 + contact sheet `_audit_thumbs_2026-07-27/`) đặt 6 thumbnail live cạnh 8 video top của 若返りアカデミア + 長生きの秘訣 ở cỡ browse thật. Kết quả: **thumbnail MỚI NHẤT không đọc được chữ nào ở 168px** (khối tối + dấu ❌), một cái nữa có 4 dòng cùng cỡ không dòng nào nổi. Tức **gate 120px có trong luật từ 07-11 nhưng đã bị bỏ qua trên thực tế** — nên gate mới đi kèm tool tự xuất file, để không thể "quên".

**3 luật hình bổ sung, đúc từ 8 thumbnail thắng của ngách (áp cùng gate):**
- **ĐÚNG 1 điểm nhấn khổng lồ, ưu tiên là 1 CON SỐ**, to gấp 2–3 mọi thứ còn lại (mẫu 若返り: 「94歳」+「5つ」 mỗi cái ~1/3 khung). 3–4 dòng cùng trọng lượng = không dòng nào thắng.
- **Dòng chính cao ≥1/4 chiều cao khung.** Đo thật: winner ~1/4 khung/dòng; health ~1/10 → nhỏ hơn 2–2,5×. Đây là lỗi phổ biến nhất.
- **Phải có vật/người NHẬN DIỆN ĐƯỢC ở 168px** — mặt người thật (若返り) hoặc **bao bì thật** (長生き dùng むぎ茶, ブルガリア yogurt). Ảnh món stock chung chung ở 168px chỉ thành "đồ ăn nào đó".

### A8. Title–thumbnail: món được lặp, câu không lặp ⭐ NỚI so với v2
Thị trường lặp tên món ở cả hai (1,3M: title 卵や豆腐より… + thumb 卵・豆腐より) — **tên món ĐƯỢC lặp** để nhận diện ngay. Chỉ cấm lặp nguyên cụm câu: title nói góc A (5つの習慣/間違い) thì thumbnail đánh stake B (hậu quả cụ thể).

---

## Phần B — Title (giữ khung v2, cập nhật 2 điểm)

### B1. Từ khóa món/chủ đề trong 25 ký tự đầu
Mobile cắt ~40–45 ký tự. Mỗi title ≤ ~40 ký tự. Chữ số Ả Rập OK (7選、1位). Gắn 60代／60歳を過ぎたら khi hợp.

### B2. Công thức xoay vòng — ⭐ v5: P0 CẢNH BÁO là MẶC ĐỊNH (shokutaku — không 医師)
- **P0 (MẶC ĐỊNH từ 2026-07-21)** — 【tag cảnh báo】+ hành vi/món + hậu quả + giấu đáp án. Tag đầu xoay vòng: 【60歳以上必見】【高齢者は要注意】【知らずに損】【実は間違い】【今すぐ確認】. Mẫu: 「【60歳以上必見】絶対に避けたい◯◯4選！毎日食べたいおすすめ◯◯4選」「【高齢者は要注意】その◯◯、腎臓が悲鳴を上げているかも」「知らずに買うと逆効果！60代が避けたい◯◯と正解の選び方」. Lead bằng khung nghi vấn/cảnh báo, payoff tích cực đặt vế sau (bằng chứng Analytics: khung 「その体にいいが…?」 hút được rổ retention 96%).
- **P1** — Món quen + cách dùng sai + cơ quan bị hại: 「◯◯の食べ方を間違えると腎臓が危険！60代が今すぐ知るべき真実」
- **P2** — [Số] dấu hiệu/món + đừng bỏ qua: 「60歳を過ぎたら見逃さないで！◯◯に現れる危険サイン7選」
- **P3** — Ngưỡng số/đáp án dứt khoát: 「60歳を過ぎたら◯◯は『いくつから危険』？研究でわかった本当のライン」
- **P4** — Đảo ngược nhận thức: 「◯◯は腎臓の味方だった？」「その◯◯、年のせいではありません」
- **P5** — Câu hỏi trực diện: 「バナナ、朝食べるのは正解？間違い？」
- ⭐ Nhịp kênh v5: **≥2/3 số video dùng P0/P1 (khung cảnh báo)**, P4–P5 làm biến tấu xen kẽ; cấu trúc kép 「X tránh + Y nên」 (4選+4選) là format chủ lực — sợ mở màn, kết dương, hợp compliance + persona みのり.
- Mẫu directive 「…はこれを選びなさい」 → shokutaku dùng dạng mềm 「…を選んでください」.

### B3. Một cảm xúc chủ đạo mỗi video
Chọn 1: **sợ** (危険・注意), **tò mò** (実は・まさか), hoặc **lợi ích** (効果2倍・若返る). Nhịp kênh: không quá 2 video "sợ" liên tiếp.
⭐ Cập nhật theo dữ liệu 26 video kênh health: video nổ (33K) là fear+curiosity; tone thuần ấm chưa có mẫu thắng → shokutaku vẫn giữ persona ấm TRONG video, nhưng title/thumbnail đi theo cường độ thị trường.

### B4. Title + Thumbnail = 1 câu chuyện, kết thúc bằng câu hỏi
Đọc title xong nhìn thumbnail phải sinh ra câu hỏi. Xem cả hai mà đã biết hết nội dung → khỏi click.

### B5. Không hứa quá nội dung
Tình tiết trên title/thumbnail phải THẬT SỰ có trong video. Hook không được trả lời → retention sập → đề xuất tắt.
⚠️ Mẫu thị trường có kiểu 「糖尿病がほぼ消える!?」 — **KHÔNG bắt chước claim khỏi bệnh** (medical misinformation, mục 5 compliance). Học cường độ, không học claim: thay bằng hậu quả/lợi ích sinh hoạt (眠れない/栄養半分/体力が戻る).

---

## Phần C — Quét compliance trước khi giao (giữ nguyên v2)

Đối chiếu `.claude/rules/youtube-compliance.md` + các điểm riêng:
1. Title/thumbnail KHÔNG chứa: 殺・死・自殺・レイプ・虐待 **và 血 (血圧/血管/血糖/血液)・透析** → thay bằng 太る／落とし穴／もったいない／眠れない／逆効果／知らないと損. 血/透析 chỉ ở 概要欄/tag (title health được dùng 血糖値 làm keyword, thumbnail thì không).
2. KHÔNG 医師・先生・管理栄養士・専門家 ở mọi đâu (shokutaku); health cũng đang bỏ dần cụm 医師が解説 (risk persona).
3. KHÔNG tên thật hãng/sản phẩm/người/viện. KHÔNG mặt người thật cụ thể trên thumbnail.
4. KHÔNG claim chữa khỏi (治る・消える・完治) trên title/thumbnail — kể cả dạng !?
5. 概要欄: ※医療免責 + credit giọng + 出典.
6. Mỗi tập một góc + một layout khác video liền trước (chống inauthentic).

---

## Phần D — QUY TRÌNH SẢN XUẤT + TOOL (v4 DESIGN-FIRST, 2026-07-11 — đúc kết 3 vòng feedback video jinzo)

> **Gốc rễ các bản hỏng: LẮP TEMPLATE trước khi NGHĨ.** Làm đúng thứ tự dưới đây, và **KHÔNG giao bản nào chưa qua đủ 3 CỬA tự duyệt (bước 5) — đừng để user làm QA thay.**

**Bước 0 — Ý CHÍNH phải nằm trong HÌNH (quyết định trước mọi thứ):**
Hỏi: video này về CÁI GÌ — tạng? một món? thói quen? Che chữ đi, hình 0,5 giây phải ra đúng cái đó. Chữ và hình chia vai: dòng MÓN đã gánh tên món → HÌNH gánh phần còn lại của ý chính (organ-topic → tạng, xem A5; món đơn → món hero; thói quen → cảnh hành động). Sai bước này thì render đẹp mấy cũng vứt (bài học: "chủ đề thận mà toàn chuối").

**Bước 1 — Câu chuyện 1 khung:** bộ 3 dòng MÓN/TWIST/STAKE (A2) + thiết bị curiosity (A4) + layout (A6). Ghi vào block Đóng gói CTR của script TRƯỚC khi render.

**Bước 2 — Ảnh nền:** `tools/fetch_photo.py` với query kèm **"dark background / moody / low key"**. Kiểm bằng code trước khi dùng: **kích thước THẬT của file** (nhiều khi ≠ số Pexels ghi — crop vượt khung là PIL độn đen, đã dính 1 lần) + bbox chủ thể (gate A5). Chuẩn kênh = MỘT ảnh liền full-bleed tối; ảnh sáng trắng thì loại từ đầu, đừng dim cứu.

**Bước 3 — Thiết kế nền khi ảnh thô chưa đạt bố cục: `tools/compose_thumb_bg.py`** (đúc từ mẫu jinzo v6):
   ```
   python tools/compose_thumb_bg.py <ảnh> <bg.jpg> [--mirror] [--crop x0,y0,x1,y1] \
     --grad l|r [--grad-reach 1280 --grad-max 243] \
     [--cutout-src <model.jpg> --cutout-box x0,y0,x1,y1 --obj-w 620 --obj-x 1275]
   ```
   - `--mirror/--crop`: đưa chủ thể về một phía. `--grad`: **gradient tối phía đặt chữ (low-key relight)** — nội dung phía chữ còn silhouette mờ như mẫu trứng; thay HẲN cho `--panel` (panel đen cứng chỉ khi user yêu cầu riêng).
   - `--cutout-*`: ghép vật thể phụ (tạng, vật chứng) = **cắt từ ẢNH THẬT (HSV+BFS) + grade tối/ấm + unsharp + bóng đổ → chìm vào cảnh như vật thật**. CẤM sticker いらすとや/hoạt hình lên ảnh photo, CẤM collage 2 hộp. Vật thể phải TO + NÉT (mặc định 620px/unsharp — bản 470px mờ đã bị chê "khó nhìn").
**Bước 4 — Chữ: `tools/make_thumb.py`** (3 dòng + 2 màu):
   ```
   python tools/make_thumb.py <bg> <out.png> --stack l|r --fill \
     --line1 "<MÓN>" --line2 "<TWIST>" --line3 "<STAKE>" [--box 1:red] [--maxw 0.48] [--pop] [--dim 0.15]
   ```
   Nền đã compose thì thường KHÔNG cần `--pop/--dim`. Xoay bộ màu giữa video liền kề. (Flags v2 cũ vẫn chạy; `make_thumb_compare.py` = layout C chia đôi.)

**Bước 5 — 3 CỬA TỰ DUYỆT (tự chạy đủ TRƯỚC khi đưa user; thiếu 1 cửa = tự làm lại):**
   1. **Cửa Ý CHÍNH** — mở full-size, che chữ: hình có ra đúng chủ đề video trong 0,5s không? Chủ thể ý-chính TO + NÉT + đủ sáng chưa? Chữ có đè chủ thể không?
   2. **Cửa ĐỒNG BỘ KÊNH** — mở CẠNH mẫu chuẩn Phần E: cùng một ngôn ngữ hình chưa (một ảnh liền, tối moody, không mép ghép, không sticker)? Được phép khác ẢNH/tông/bộ màu; **không được khác "KIỂU"** (bài học: bản chuối-panel + hoạt hình đặt cạnh mẫu trứng "khác hẳn nhau").
   3. **Cửa 120px** — đọc được STAKE + nhận ra chủ thể (organ-topic: nhận cả món LẪN tạng).
   4. **🔴 Cửa 168px (BẮT BUỘC, thêm 2026-07-27)** — mở `*_preview168.png`: đọc được DÒNG CHÍNH. Không đọc được = làm lại. Xem A7.

**Bước 6 — Compliance Phần C + ghi vào script:** file paths, **lệnh tái tạo ĐẦY ĐỦ cả 2 tool** (compose_thumb_bg → make_thumb), layout đã dùng, nguồn + license ảnh (Pexels/CC0, né logo hãng trên model).

## Phần E — MẪU CHUẨN ĐÃ CHỐT (user duyệt 2026-07-11, video sau bám theo)

| Video | File | Công thức |
|---|---|---|
| Trứng (health 01) | `youtube-jp-health/06_VIDEO/01_yude-tamago/thumbnail_v23_ajitama.png` | Ảnh FULL-BLEED tối ấm: bát trứng lòng đào kiểu quán Nhật lệch PHẢI (Pexels 34684827) + chữ kín chiều cao vùng tối trái: banner ĐỎ 「そのゆで卵」/ trắng 「栄養の半分」/ vàng to 「捨ててた!?」 |
| Blueberry (shokutaku 06) | `youtube-jp-health/06_VIDEO/02_blueberry_shokutaku/thumbnail_v6_moody.png` | Ảnh FULL-BLEED tối moody: xô kim loại đổ việt quất lệch PHẢI (Pexels 9367686) + chữ vùng đen trái: vàng 「ブルーベリー」/ trắng 「夜に食べると」/ đỏ to 「眠れない!?」 |
| Jinzo (shokutaku 01, ORGAN-TOPIC) | `youtube-jp-shokutaku/06_VIDEO/01_jinzo-tabemono/thumbnail_v6_moody.png` | Nền COMPOSE (compose_thumb_bg): giỏ chuối nền đen mirror + gradient tối trái + **mô hình thận CC0 cắt ghép chìm vào cảnh** (620px, unsharp) góc dưới phải + banner đỏ 「バナナ、」/ trắng 「毎日食べると」/ vàng 「腎臓が悲鳴!?」 |

**Chuẩn kênh v5 (user chốt 2026-07-21, thay chuẩn moody 07-11): style TEXT-DOMINANT CẢNH BÁO theo meta 長生きの秘訣** — ảnh thật **SÁNG RÕ vật thể** (không cần moody; món/vật chiếm 1/3–1/2 khung, phía còn lại đặt chữ), **cột chữ 3 dòng khổng lồ kín ~86% chiều cao chiếm ~55–65% bề ngang**, 袋文字 viền đen dày, bộ màu trắng+đỏ+vàng (2 màu nhấn), khung chữ theo A2 v5 (HÀNH VI → HẬU QUẢ → ĐÁP ÁN GIẤU), kèm **mũi tên/khoanh đỏ** khi có vật đáp án. Tiêu chí duyệt tối thượng: **ở 120px đọc được cả 3 dòng + nhận ra vật thể** — độ "đẹp cinematic" xếp sau độ ĐẬP VÀO MẮT.
- Mẫu chuẩn v5 (của đối thủ, để đối chiếu "kiểu"): 「知らずに買う／寿命を縮める／危険なパン」 (ảnh bánh mì sáng + mũi tên đỏ) · 「まだ食べてる？／海外ではNG／この食品」 · 「卵１日１個／実は間違い！／腎臓が壊れる」. Thumbnail v5 đầu tiên của kênh render xong thì thay bảng này bằng mẫu nhà.
- 3 thumbnail moody cũ (Phần E bảng trên) giữ nguyên file làm tư liệu; video ĐÃ đăng đổi thumbnail dần theo v5 khi sửa metadata trong Studio (playbook `CHANNEL_OPTIMIZE.md` Mục 1c).
- Giữa các video: đổi ẢNH + màu dòng HẬU QUẢ (đỏ↔vàng) + vị trí cột chữ (trái↔phải) — chống lặp nguyên bộ. Claim có giới hạn (半分/!?) · lệnh render lưu trong block Đóng gói CTR từng script.
