# 03 — KHUÔN THUMBNAIL kênh 昭和くらし図鑑 (showa)

> **Nguồn sự thật của kênh này** về prompt gen thumbnail. Chốt **2026-08-18** (user dán ảnh mẫu 「今では消えた昭和の食」 và nói *"cho tao prompt dạng như này"* → *"lưu lại rule để gen cho những lần sau"*).
> Luật toàn hệ thống vẫn đứng trên: `.claude/rules/ab-3title-3thumb.md` (bộ 3×3 + 4 file xuất) · `audience-45plus.md` §1 (gate chữ) · `media-library.md` §2.10 ⑤b (watermark) · `youtube-upload-seo.md` §0.5 (đo keyword). File này chỉ ghi **cái riêng của showa**.
> ⚠️ **Phạm vi: CHỈ kênh showa.** Kênh khác giữ khuôn của nó.
>
> 🔴 **HAI LUẬT NỘI DUNG CHỮ, thêm 2026-09-07 — đứng trên mọi khuôn hình trong file này:**
> ① **Hero là MỆNH ĐỀ có gap, KHÔNG phải DANH TỪ tên vật.** ⛔ Bỏ khuôn cũ của bible (「1 vật chụp to + 「覚えてる？」/「給食」」): 7/7 thumbnail đã đăng dùng hero danh từ, không video nào được rail đẩy; đối thủ ăn view dùng 「今では信じられない」「なぜ消えた？」 (`CHANNEL_DIAGNOSIS_2026-09-03.md` §3 mục 2, và 3/3 kịch bản >100K cùng khung — `05_SCRIPT_FORMULA.md` §4 E1).
> ② **Chữ hứa gì thì 30 GIÂY ĐẦU của lời phải trả cái đó.** Video 06 hứa 3 con giá, cold open kể tuỳ bút → **62% bỏ đi trước 0:30** dù CTR 3,5%. Sửa bao bì mà không sửa 30s đầu là làm lại đúng ca đó.

---

## 1. KHUÔN **K-COLLAGE** — chốt cho mọi video từ #1

**Nhìn thế nào:** collage nhiều ô ảnh tư liệu, ngăn nhau bằng khe trắng, viền trắng dày quanh khung · các ô **sepia/umber** trừ **đúng một ô MÀU RỰC** (món ăn / vật chính) · chữ đè lên trên, hero 2 dòng cắt ngang giữa khung.

**Vì sao khuôn này, không phải khuôn cream cũ:** ba lượt thử trong ngày 08-18 đi từ nền cream sáng → nền tối-ấm → collage. Collage thắng vì **hero không bị dòng phụ kẹp trên–dưới**, nên nó cao được **32,7%** khung (xem §5) — trong khi 13 ca đo trước của workspace đều mắc ở 20–31% đúng vì bị kẹp.

### 1.1 Số đo (đo bằng máy trên ảnh mẫu 550×312, ratio 1,763)

| Khối | Cao | Rộng | Ghi chú |
|---|---|---|---|
| banner tối trên | **17,9%** khung | **92,7%** — gần full-width | cao hơn banner khuôn cũ (15,6%) |
| chip đen bo góc | ~ bằng banner | nhỏ, nằm ở **đầu trái** hàng banner | |
| **HERO dòng 1** (trắng) | **26%** | — | viền đen dày |
| **HERO dòng 2** (ĐỎ) | **32,7%** ⭐ | **73,8%** | to nhất khung; bề ngang **trùng khít** khuôn kênh cũ (74,4%) |
| Cả khối hero | **~59%** chiều cao khung | | |

**Palette:** `#0f0f19` đen xanh · `#4b3015` nâu đậm · `#a07e57` sepia · `#e5d2a4` be · `#fff7dc` kem (chữ) · **`#c00f0c` đỏ tươi (hero dòng 2)**. Độ sáng trung vị **85/255**, p90 **253** → tối, nhưng highlight cháy ⇒ tương phản rất cao.

### 1.2 Bốn khối chữ — ánh xạ cố định, video nào cũng vậy

| Khối | Nội dung | Vai (gate 7 của `audience-45plus` §1) |
|---|---|---|
| chip đen bo góc trên-trái | **số lượng** — `全10品` / `全12品` | đếm được, hứa cụ thể |
| banner tối full-width | **mốc thời gian** — `昭和40年〜50年代` | ③ MỐC |
| HERO dòng 1, trắng viền đen | **khung mất mát** — `今では消えた` | ② CHUYỆN GÌ XẢY RA |
| **HERO dòng 2, ĐỎ, TO NHẤT** | **chủ đề + keyword đo được cao nhất** — `昭和の給食` | ① VỀ CÁI GÌ |

🔴 **Keyword phải nằm ở HERO dòng 2, không nhét vào banner con.** Khuôn cũ đặt `給食` (460 điểm) vào banner nhỏ — sai chỗ; ở đây nó chiếm ô to nhất khung.
⛔ **Đừng ghi `総集編` như ảnh mẫu** trừ khi video **thật sự** là tổng hợp — ghi sai là misleading metadata (`youtube-compliance` mục 4).
⚠️ **Trần 4 khối, không thêm khối thứ 5.** Cả 3 ca bake chữ Nhật thành công trong workspace đều ≤4 dòng. Hệ quả: khuôn này **không có dải đáy** ⇒ mất câu hỏi ngược (`どれがあった？`) — bù bằng đuôi title A1 + pinned comment. Nát chữ thì **bỏ chip xuống 3 khối** trước khi bỏ cuộc.
📌 **Áp cho video KHÔNG phải đồ ăn (bổ sung 2026-08-20, ca video 02 商店街):** ánh xạ 4 khối giữ nguyên —
chip `全◯品` dùng được cho cả đồ vật (30 chi tiết = `全30品`) · mốc thời gian đổi theo bài (`昭和30年〜40年代`).
Câu **cơ chế tương tác** của bài (`何点わかる？`) cũng KHÔNG được lên thumbnail — nó là khối thứ 5; chỗ của nó là đuôi title + pinned comment.
📌 **Hero khi Trends bị chặn (429):** lấy tạm **keyword dẫn của Title A1** (đã qua phép đo proof-view) làm hero dòng 2, ghi rõ vào script + BLOCKS.md là *tạm* — **đo lại trước khi đăng**, rổ ra từ khác đứng top thì đổi chữ hero **và gen lại ảnh**, không đổi chữ suông.

### 1.3 Ba biến thử A/B (chữ GIỐNG NHAU, chỉ đổi HÌNH)

| | Biến | Bố cục ô |
|---|---|---|
| **T1** baseline | 3 ô | dọc trái sepia (hành lang/lớp học) · phải-trên **MÀU** (vật chính) · phải-dưới sepia |
| **T2** đổi 1 biến | **số ô + tỉ lệ** | chỉ 2 ô, 40/60 — ô MÀU chiếm nửa phải. 🔴 **CÙNG chủ thể với T1** — biến thử là LƯỚI; đổi cả chủ thể ảnh là lẫn 2 biến, thắng cũng không biết vì cái gì |
| **T3** đổi layout | **lưới** | 2×2 bốn ô đều nhau, 3 sepia + 1 MÀU ở dưới-phải |

### 1.4 Chọn Ô MÀU thế nào (bổ sung 2026-08-20, ca video 02)

Video đồ ăn thì ô MÀU hiển nhiên (món ăn). Video đồ vật thì chọn theo **hai điều kiện, đủ cả hai**:
1. **Vật có màu "appetising" nhất** trong danh sách của bài — thứ ăn được chữ `saturated appetising colour` của prompt (video 02: lọ thủy tinh kẹo 駄菓子屋, không phải cái kèn đồng hay 牛乳箱).
2. **Vật phải CÓ THẬT trong video** (video 02: 駄菓子屋 = mục 16〜18点目, phút 08:42) — thumbnail hứa gì video phải có (`youtube-compliance` mục 4), và frame đầu ↔ thumbnail phải cùng một mạch hình (`media-library` §2.0).
Các ô sepia còn lại lấy 2–3 vật/cảnh **cũng có trong bài**, ưu tiên vật mở bài (video 02: 牛乳箱 = cold open).

### 1.5 🟡 KHUÔN THỬ **K-PHOTO** — chạy song song từ video 08 (2026-09-03)

Lý do (`CHANNEL_DIAGNOSIS_2026-09-03.md` §3): 7/7 thumbnail K-collage đã đăng **cùng một khuôn**, hero là **DANH TỪ nhãn**, **0/7 có NGƯỒI**, tông nâu đều → trên feed 7 cái nhìn như 1. Hai kênh ăn view cùng ngách (あの頃の昭和 9,9K sub · あの頃の日本 40 sub/10,6K view) dùng **1 ảnh có người + 2 dòng đỏ 袋文字 ~50% khung + 1 chip năm**. CTR thật của kênh: 3,9% / 7.860 imp; video 06 được đẩy 4,9K imp thì rớt 62% trước 0:30 (thumbnail hứa số, 30s đầu kể mood) → khuôn nào cũng phải **khớp 30 giây đầu**.

| | K-COLLAGE (§1) | K-PHOTO (thử) |
|---|---|---|
| ảnh | 3–4 ô sepia + 1 ô MÀU, không người | **1 ảnh full-bleed sepia/đen-trắng, CÓ NGƯỜI** (mặt đọc ra biểu cảm ở 168px), người chiếm nửa PHẢI, đầu chạm mép trên, cắt ở eo/ngực; nửa trái tối để chữ |
| mốc năm | banner full-width ~1/6 khung | **chip navy nhỏ** góc trên-trái |
| HERO 1 | trắng viền đen, giữa khung | trắng viền đen, **nửa dưới**, canh trái |
| HERO 2 | đỏ, ~30% cao, ~3/4 rộng | đỏ 袋文字, **~1/3 cao, ~4/5 rộng**, ngay dưới HERO 1 |
| số lượng | chip `全N点` | **burst đỏ `N選` góc trên-PHẢI** (góc dưới-phải để cho timestamp) |
| ảnh phải | có trong video | **= cảnh 30 giây đầu** (T2) hoặc cảnh mục sớm nhất (T3) — thumbnail hứa gì thì cold open trả ngay |

Cách test: T1 collage · T2 K-PHOTO cảnh cold open · T3 K-PHOTO đổi CẢNH. Chữ 4 khối **cùng nội dung** cả 3 bản. Test & compare ≥7 ngày, giữ title. Mẫu prompt đầy đủ: `06_VIDEO/08_okane-joushiki/thumb_prompts_BLOCKS.md` (gate TEXT @ 7%, ~2.500 ký vì khối PHOTO tả người + bối cảnh).
Kết quả → ghi vào §5 và `08_ANALYTICS_LOG.md`; K-PHOTO thắng 2 video liên tiếp → thành khuôn chính, §1 xuống lưu trữ.

---

## 2. KHUNG PROMPT (copy, thay 4 chỗ in đậm)

Viết ở dạng khối để đọc; nén về **1 dòng** khi ghi vào `thumb_prompts_FLOW.txt`.

```
YouTube thumbnail, 16:9, a collage of vintage photo panels separated by clean white
gutters, the whole image framed by a thick white border, bold Japanese text burned on top.

TEXT, exactly these 4 blocks and nothing else:
chip, cream-white characters on a small black rounded box in the very top-left corner: 【SỐ LƯỢNG】
banner, cream-white characters on a dark bar running across the top: 【MỐC THỜI GIAN】
HERO line 1, thick white characters with a heavy black outline: 今では消えた
HERO line 2, the LARGEST element in the whole image, bright red characters with a thick
  white outline and a heavy black outline over it: 【CHỦ ĐỀ + KEYWORD】

LAYOUT: the banner sits across the top at about one sixth of the frame height with the
black chip at its left end; HERO line 1 sits just under it in the upper middle; HERO line 2
crosses the centre of the frame, starting near the very left edge and running about three
quarters of the way across, about one third of the frame height, taller and wider than
everything else, overlapping the panel edges.

PANELS: 【tả từng ô — ô nào sepia, ô nào MÀU】

COLOUR: rich warm sepia and umber for the archival panels, one panel in saturated
appetising colour, deep near-black shadows, cream highlights, very high contrast.
Crisp focus, photorealistic, no characters, captions or signage written inside the panels.

All Japanese text must be perfectly formed characters, crisp and legible, correct stroke
counts, no garbled glyphs. Keep the very bottom-right corner completely free of text.
No watermark, no logo, no signature, no additional text.
Avoid: derelict or abandoned building, ruins, horror mood, flat grey lighting, modern
objects, anime style, garbled lettering.
```

**Năm câu bắt buộc có mặt, mỗi câu bịt một lỗi đã dính thật:**
1. `exactly these 4 blocks and nothing else` — chặn model tự thêm chữ rác.
2. `no characters, captions or signage written inside the panels` — 🔴 lỗi **đã dính** ở bản gen 08-18: model tự dán nhãn tủ kính, ra `鯨の竜田揚げ` **2 lần**, một lần gắn dưới cái 食缶 nhôm.
3. `Keep the very bottom-right corner completely free of text` — chỗ YouTube đóng timestamp.
4. `No watermark` — nhưng vẫn phải **đo lại vị trí ✦ theo từng lô** rồi xử (xem §4).
5. `taller and wider than everything else` + `about one third of the frame height` + `three quarters of the way across` — ép hero bằng **quan hệ với mép khung**, vì model **nghe vị trí, không nghe tỉ lệ** (`media-library.md` §2.10 ⑥).

---

## 3. NƯỚC MÀU — hoài cổ lấy từ đâu (và **không** lấy từ đâu)

🔴 **KHÔNG dùng `8mm / faded / vignette / washed-out` cho TOÀN khung.** `04_VIDEOGEN_PROMPTS_v2_TEST.md` §0 đo được: prompt gắn mấy từ đó → **4/4 ảnh ra trường BỎ HOANG tối om**, vì model hiểu "cũ = hỏng".

Ba đường được dùng:

| | Cách | Câu trong prompt |
|---|---|---|
| ① **Ô sepia** | chất ảnh in cũ **chỉ ở các ô tư liệu**, không phủ cả khung | `desaturated sepia and umber archival print tones` |
| ② **Một ô MÀU RỰC** | tương phản với sepia = thứ tạo cảm giác "xưa vs nay" | `bright FULL-COLOUR food photograph`, `saturated appetising colour` |
| ③ **Vật trong khung** | khay nhôm móp, chai sữa nắp giấy, thùng gỗ đựng sữa, 食缶, だるまストーブ, 白い割烹着 | tả thẳng trong khối PANELS |

**Vẫn cấm tuyệt đối:** `derelict`, `abandoned`, `ruins`, `horror mood`, `flat grey lighting`.

⚖️ **Ngoại lệ có chủ ý với gate 6 của `audience-45plus` §1** (*"nền sáng, moody/tối đã bị kết án ở health 2026-07-21"*): khuôn này tối. Nhận ngoại lệ vì gate đó thực chất bảo vệ **tương phản chữ–nền**, mà kem/đỏ trên sepia-đen cho tương phản **cao hơn** bản cream-trên-cream. Điều kiện bù, không được bỏ:
1. Hero dòng 2 **đỏ tươi + viền trắng dày + viền đen** — mất viền là mất ngoại lệ.
2. Ô MÀU phải **sáng rực**, không để cả khung xám đều.
3. **Soi 120px: hero phải là thứ đọc được đầu tiên.** Chìm ⇒ gen lại, ⛔ đừng bóp chữ nhỏ cho vừa.
4. CTR thua bộ nền-sáng ⇒ trả về khuôn cream, ghi ngày vào `08_ANALYTICS_LOG.md`.

---

## 4. QUY TRÌNH — 6 bước, không đảo

0. 🔴 **KIỂM FOLDER TRƯỚC: có bộ prompt KHUÔN CŨ nằm sẵn không** (bổ sung 2026-08-20). Video 02 đã có sẵn `thumb_prompts_FLOW.txt` viết theo khuôn cream (chữ trái/ảnh phải) từ TRƯỚC ngày chốt K-collage 08-18 — ai bơm thẳng file đó vào extension là gen ra 3 ảnh sai khuôn kênh. Dấu nhận biết khuôn cũ: prompt có `photo occupies the RIGHT half` / `LEFT half kept clean for text`, không có chữ `collage`. Xử lý: **backup thành `*.bak_cream.txt` rồi viết đè** — đừng để hai bộ cùng tên tồn tại song song. Mọi bộ prompt viết trước 2026-08-18 đều thuộc diện này.
1. **Đo keyword trước** (`youtube-upload-seo.md` §0.5). Từ vào **HERO dòng 2** phải nằm **top 2** rổ đo. Vật đẹp mà volume thấp thì cho nó vào **ẢNH**, không cho vào chữ. Trends bị 429 → dùng tạm keyword dẫn Title A1, ghi chú *tạm*, đo lại trước khi đăng (§1.2).
2. **Chốt 4 khối chữ** theo bảng §1.2, kiểm gate 7 bằng cách che ảnh: trả lời được "về cái gì / chuyện gì / mốc nào" chưa?
3. **Xuất 4 file** vào `06_VIDEO/<slug>/` (`ab-3title-3thumb` §3.1 Bước 4): `thumb_prompts_FLOW.txt` (1 prompt/1 dòng) · `thumb_prompts_BLOCKS.md` (người đọc) · `thumb_prompts_TENFILE.txt` (dòng ↔ tên file) · `thumb_prompts_PLATE.txt` (3 bản KHÔNG chữ — ⛔ để **riêng**, trộn vào FLOW là ra 3 ảnh trắng chữ).
4. **Chạy gate máy:**
   ```bash
   cd Projects/youtube-jp-showa/06_VIDEO/<slug> && PYTHONIOENCODING=utf-8 python -c "
   import io
   for i,l in enumerate(io.open('thumb_prompts_FLOW.txt',encoding='utf-8')):
       l=l.rstrip()
       if not l: continue
       p=l.find('TEXT, exactly'); print('T%d: %d ky | TEXT @ %d%%'%(i+1,len(l),p*100//len(l)))"
   ```
   **TEXT phải ≤15%** (gate chính, có cơ chế: để cuối thì model bám tả cảnh và nuốt chữ). Độ dài khuôn này rơi **~2.100–2.200 ký** — vượt trần mềm 1.500 vì khối PANELS phải tả từng ô; **đừng cắt số đo để lấy con số đó**.
5. **User gen** (Nano Banana / Gemini image, 16:9, ≥3 bản/prompt). Claude **không tự gen rồi đăng** — trình duyệt trước (`feedback_chot_truoc_khi_dang`).
6. **Nghiệm thu — 4 việc, thiếu 1 là chưa xong:**
   - **Soi TỪNG ký tự 1:1.** Kanji rậm hay chết: `給食`・`昭和`. Sai một nét ⇒ **loại, gen lại**.
   - **Xoá watermark ✦.** Quét **CẢ LÔ** trong `~/Downloads`, không chỉ ảnh dán vào chat. Thumbnail có chữ chạy sát mép ⇒ **phải VÁ, không cắt** (`youtube-jp-shokutaku/tools/strip_wm_thumb.py`). Vị trí ✦ **chốt bằng MẮT theo từng lô kích thước** — đo bằng máy đã thất bại 4/4 lần ở ảnh có chữ. Lô **2752×1536** đã đo: ✦ ở **~(0,945W · 0,92H)**.
   - **Kiểm tỉ lệ:** lô 2752×1536 là **1,792**, không phải 16:9 → crop về **2730×1536**.
   - **Duyệt 168px + 120px**, hero đọc được mới giao.

---

## 5. SỔ CA ĐO (thêm vào đây mỗi lần đo, đừng đo lại từ đầu)

| Ngày | Ca | Hero cao | Kết luận |
|---|---|---|---|
| 2026-08-10 | khuôn cream cũ (tool render), video 01 | **24,6%** (rộng 74,4%) | đọc được 168+120px, rớt gate 33,3% — ca thứ 7 của `audience-45plus` §6.10 |
| 2026-08-18 | **ảnh mẫu đối thủ** 「今では消えた昭和の食」 (collage) | **32,7%** (rộng 73,8%) | ⭐ **gần chạm gate** — vì hero **không bị dòng phụ kẹp**. Lý lẽ cơ chế cho việc đổi sang K-collage |
| 2026-08-18 | bản gen "biển treo" (loại) | **12,6%** (9 ký/dòng) | 🔴 **mất chữ ở 120px** — bằng nửa khuôn kênh. Kèm 5 lỗi khác: sai bộ chữ, `フローズンヨーグルト` **sai thời kỳ + không có trong video**, nhãn lặp/gắn nhầm, ✦ còn nguyên, không có điểm nhấn |
| 2026-08-20 | **video 02 商店街** — bộ prompt viết theo khuôn này (chưa gen) | *(đo sau khi có ảnh)* | Ca đầu áp K-collage cho video KHÔNG-đồ-ăn: chip `全30品` · hero `昭和の商店街` (6 ký, keyword Title A1 vì Trends 429) · ô MÀU = lọ kẹo 駄菓子屋. Gate máy: 2.162–2.329 ký, TEXT @ 7–8% ✓ — xác nhận dải ~2,1–2,3k của §4.4. File mẫu: `06_VIDEO/02_kieta-mise/thumb_prompts_*` |
| 2026-09-07 | **09 外食 (live) + 08 T2/T3 (live)** — đo lại 3 ảnh đang chạy để viết bộ video 10 | *(xem cột phải)* | 🔴 **Ảnh thật KHÁC §1.1 hai chỗ:** ① nền **KEM SÁNG** (trung vị **169/255**), không phải tối 85 ② mốc năm là **chip navy nhỏ** (10,9% cao · 20,9% rộng), không phải banner tối full-width; và có thêm **burst đỏ `N選` góc trên-PHẢI** (29,3% cao · 19,3% rộng, x 80→99%) — tức K-collage trên kênh đã **hợp nhất** 2 khối của K-PHOTO. ⇒ Bộ video 10 viết theo ẢNH, không theo §1.1. **§1.1 cần sửa lại theo ảnh live.** ⚠️ **Hero KHÔNG đo được bằng máy ở khuôn này:** mask đỏ bắt cả **vật đỏ trong ảnh** (quốc kỳ giấy + cơm ketchup của bản 09) → trả "hero cao 66,8%" = số rác; ca thứ 5 của `feedback_do_pixel_cua_so_quet`. Đo bằng mắt: hero đỏ ~24% cao, y 26→46% (collage) / y 72→95% (photo) |
| 2026-09-07 | **video 10 通学路** — ĐÃ GEN, nghiệm thu: **T1 + T2 PASS, T3 LOẠI** | **T1 18,0%** (rộng 68,6%) · **T2 18,9%** (rộng 66,5%) | Đọc rõ 168px cả 3; **120px: T2/T3 rõ, T1 hero-1 TRẮNG chìm** trên nền kem (hero-2 đỏ vẫn đọc đầu tiên ⇒ pass gate §3 đk 3). **Lô 1376×768 KHÔNG có ✦** — soi mắt 4 góc 1:1 cả 3 ảnh, sạch; máy vẫn vô dụng (residual 8–24k px/góc do ảnh nhiều chi tiết + chữ). Crop 1,7917 → **1365×768 bằng cách bỏ 5px trái + 6px phải**: burst đỏ chạm mép PHẢI (x→1375) và chip chạm mép TRÁI ⇒ **cắt một bên là mất khối**. 🔴 **T3 loại vì 4 lỗi NỘI DUNG, không phải lỗi chữ**: mũ có **phù hiệu NGÔI SAO kiểu cảnh sát** · cờ có **vòng tròn = 日の丸** (緑のおばさん cầm cờ giao thông, không phải quốc kỳ; mũ-sao + quốc kỳ gợi thời chiến, lệch 昭和40〜50年 và lệch nội dung bài) · băng tay có **ký hiệu nát** · cột cạnh biển có **chữ dọc nát**. ⇒ Prompt T3 v2 + T1 đã thêm chặn: `no badge`, `no insignia`, `plain yellow hand flag with NO circle`, `no vertical lettering`, và Avoid `police or military uniform, peaked cap, cap badge, star insignia, national flag, hinomaru, wartime atmosphere`. ⚠️ T3 v2 dài **3.423 ký** (dải kênh 2,1–2,3k) — dài vì phải tả thêm 3 vật bị cấm; TEXT vẫn @5% | Ca đầu **hero = CHỦ ĐỀ chứ không phải keyword top rổ**: `昭和の通学路` (Trends 0,085) thắng `消えたもの` (0,54) vì danh mục không trả lời được "về cái gì" (gate 7 ①) và `消えた` là hook tầng bét ngách. Ca đầu **HERO 1 chở NGHỊCH LÝ có số** (`行き15分 帰り1時間`, 11 ô chữ) thay vì mệnh đề gap 9 ký — cũng là ca đầu **3 video liên tiếp không lặp hero 1**. Gate máy: **2.855–2.920 ký, TEXT @ 5–7%** ✓ — **dài hơn dải 2,1–2,3k** vì khối PHOTO tả người + bối cảnh; đừng cắt số đo để hạ ký. File: `06_VIDEO/10_tsugakuro/thumb_prompts_*` |

📌 **Bài học đắt nhất của lượt 08-18:** một tấm ảnh **đẹp** không phải một tấm thumbnail. Ảnh "biển treo" bị loại vẫn dùng tốt làm **slide mở bài**, đừng vứt — nhưng cũng đừng để cái đẹp thay chỗ của cái đo được.

---

## 6. LIÊN QUAN
- Bộ 3×3 + cách viết prompt bake chữ: `.claude/rules/ab-3title-3thumb.md` §3, §3.1
- Gate chữ/mặt/nền cho tệp 45+ + 13 ca đo tỉ lệ hero: `.claude/rules/audience-45plus.md` §1, §6.10
- Watermark ✦ · ảnh AI làm nền · model không nghe tỉ lệ: `.claude/rules/media-library.md` §2.10
- STYLE LOCK ảnh trong video (khác thumbnail): `04_VIDEOGEN_PROMPTS.md`, `04_VIDEOGEN_PROMPTS_v2_TEST.md`
- Tool đốt chữ (đường lui khi nát kanji): `tools/make_thumb_01.py`
- Ví dụ đủ 4 file đã viết: `06_VIDEO/01_kyushoku/thumb_prompts_*` · `06_VIDEO/02_kieta-mise/thumb_prompts_*` (ca không-đồ-ăn, kèm BLOCKS.md mẫu)


## 7. 🔴 HAI LUẬT VIẾT PROMPT RÚT TỪ VIDEO 12 (chốt 2026-09-12, 2 lô gen)

### 7.1 ⛔ NHÃN KHỐI BẰNG TIẾNG ANH BỊ MODEL **VẼ VÀO ẢNH**

**Ca đo:** T3 video 12 ra ảnh có thêm dòng chữ trắng **`HERO line 1`** nằm ngay trên hero thật —
tức khối chữ **thứ 5**, phá trần 4 khối của §1.2.

Nguyên nhân: khuôn §2 viết `HERO line 1, thick white characters ...: クーラーは100軒に2軒`.
Model không phân biệt được đâu là **nhãn** đâu là **nội dung** — cả hai đều đứng trước dấu hai chấm.
(T1/T2 cùng khuôn thì không dính ⇒ đây là **xác suất**, không phải tất định. Càng nguy hiểm: nó ngủ yên qua nhiều lô.)

✅ **Khuôn TEXT mới — bỏ mọi nhãn đọc được, đánh số:**
```
TEXT: the picture contains exactly four pieces of Japanese text and nothing else.
No English word, no Latin letter and no label of any kind may appear anywhere in the image.
(1) in the very top-left corner, cream-white characters on a small dark navy rounded box, reading: 【MỐC】
(2) in the top-right corner, cream-white characters on a bright red starburst badge, reading: 【N選】
(3) a line of thick white characters with a heavy black outline, reading: 【NGHỊCH LÝ / KHUNG MẤT MÁT】
(4) directly below it, the LARGEST element in the whole image, bright red characters with a thick
    white outline and a heavy black outline over it, reading: 【CHỦ ĐỀ + KEYWORD】
```
Trong khối LAYOUT cũng phải gọi là `the white line (3)` / `the red line (4)`, **không** gọi `HERO line 1/2`.
Thêm vào Avoid: `English words, Latin letters, any label or instruction word rendered as text`.

### 7.2 ⛔ CẤM "VIẾT CHỮ" KHÔNG ĐỦ — PHẢI CẤM **VẬT CÓ CHỮ**

**Ca đo:** T1 video 12 lô 1. Prompt đã có `no characters, captions or signage written inside the panels`,
nhưng ô MÀU tả `a watermelon split open on a sheet of newspaper` → model vẽ tờ báo **có chữ dọc nát**.

Model đọc câu cấm là "đừng *viết* chữ lên panel", không phải "đừng *đặt* vật mang chữ vào panel".
Tờ báo / sách / tạp chí / nhãn hộp / biển hiệu đều là vật **mặc định có chữ**.

✅ Hai việc cùng lúc:
1. **Đừng tả vật mang chữ.** `on a sheet of newspaper` → `on a plain unprinted bamboo tray`,
   và thêm `the tray and the wood around it completely blank`.
2. **Cấm theo VẬT, không cấm theo hành vi:**
   `there is no newspaper, no printed paper, no book, no magazine and no printed surface of any kind anywhere in the picture`
   + Avoid: `newspaper, printed paper, printed text on any surface, vertical lettering`.

📌 Cùng họ với lỗi đã loại T3 video 10 (`cột chữ dọc nát`) và lỗi 08-18 (`鯨の竜田揚げ` model tự dán nhãn tủ kính).
**Ba lần, ba video khác nhau, cùng một gốc: t2i luôn cố điền chữ vào bề mặt nào trông giống chỗ để chữ.**

### 7.3 Sổ ca đo — bổ sung

| Ngày | Ca | Kết luận |
|---|---|---|
| 2026-09-12 | **video 12 夏の当たり前** — 2 lô gen, 3 bản | **T1 v2 + T2 PASS, T3 LOẠI** (in nhãn `HERO line 1`). Lô **1376×768 không có ✦** (soi mắt 4 góc 1:1 cả 3 bản — lô này giống video 10). Crop **1376×768 → 1280×720** (bỏ 5px mỗi bên rồi scale) — chip trái và burst phải KHÔNG chạm mép nên cắt đối xứng được, khác video 10. Hero 1 `クーラーは100軒に2軒` (11 ô) — mốc lời trả ở **giây 28,6**, đo trên `_cue.json`, đạt luật ② "30 giây đầu phải trả". Hero 2 `昭和の夏` (4 ô) = ca thứ 2 **hero là CHỦ ĐỀ**, chưa đo Trends. 🟡 **T3 ra ảnh MÀU** thay vì sepia như §1.5 — giữ lại vì hợp tông sáng của 3 thumbnail đang chạy (xem ca 2026-09-07), đổi chỉ thị thành `warm nostalgic colour, slightly faded like a well-kept 1970s photograph`. 🔴 **Nền đẹp mà nửa trái SÁNG = giết chữ trắng**: T3 lô 1 hero-1 mờ nhất lô ở 120px; sửa bằng cách cho cây thông nghiêng vào từ góc trên-trái hắt bóng phủ **1/3 trái gần như đen** — vừa giữ nền đẹp vừa trả lại tương phản. Gate máy: **3.118–3.481 ký, TEXT @ 3–5%** ✓ (dài hơn dải cũ vì thêm khối `BACKGROUND` tả lớp sâu) |
