# Thư viện prompt thumbnail — kênh 古代の秘訣 (co-dai)

> **Mục đích:** mỗi video dùng MỘT KHUÔN bố cục KHÁC video liền trước — tránh "video giống hệt nhau chỉ khác tiêu đề" (inauthentic content 07/2025) và đỡ nhàm mắt subscriber. Chốt 2026-07-17.
> **Cách dùng:** chọn khuôn chưa dùng gần đây (xem sổ cuối file) → điền [PROBLEM]/[SOLUTION]/[SCENE] → gen 2–3 bản, loại bản lỗi → duyệt 3 cửa (che chữ / cạnh mẫu chuẩn / 120px) + quét compliance.
> **Text:** ưu tiên **KHÔNG bake text** — gen nền sạch rồi đè chữ 3 tầng bằng hàm `make_diagram_3dan` (xem `06_VIDEO/02_niwa-mushiyoke-10/make_thumbs_02.py`), đổi chữ không phải gen lại. Chỉ bake text khi cần chữ nằm NGHIÊNG/3D theo vật thể.

## KHỐI BRAND CỐ ĐỊNH (dán vào cuối MỌI prompt)

```
Photorealistic, high saturation, dramatic studio lighting, flat dark navy background (#1e2437), macro detail, high contrast, clean minimal composition, 16:9. Leave the top 25% and bottom 20% of the frame empty (plain background) for text overlay. No text, no watermark, no logo, no human face.
```

- Đổi 「No text」→ chỉ định text bake khi cần (kèm phương án fallback no-text).
- 「No human face」= luật kênh: tay/bàn tay OK, mặt người KHÔNG (đồng bộ series + né nhận diện người thật).

## 8 KHUÔN BỐ CỤC (xoay vòng, không lặp 2 video liên tiếp)

### K1 — Arrow diagram (biến đổi A→B)
Khi dùng: video "đổi cách làm là đổi kết quả".
```
LEFT: [PROBLEM object/action, slightly dimmed]. A thick glossy red curved arrow sweeps from left to right. RIGHT (larger, brighter, hero): a hand holding [SOLUTION object], crisp macro.
```

### K2 — X-diagram (cấm/sai lầm)
Khi dùng: video "hành động quen thuộc hóa ra sai".
```
LEFT: [PROBLEM object/action]. CENTER: a large glossy red prohibition circle with X sign, 3D style. RIGHT: [SOLUTION object held in hand or standing], brighter than left.
```

### K3 — Macro hero (bí ẩn một vật)
Khi dùng: video xoay quanh MỘT nguyên liệu rẻ tiền (ホウ酸, 重曹, giấm…).
```
CENTER: extreme close-up of [OBJECT] as the single hero subject, filling 60% of frame, dramatic side lighting with deep shadows, a few particles floating, mysterious documentary mood.
```

### K4 — Before/After split dọc
Khi dùng: video có kết quả thị giác rõ (sạch/bẩn, tươi/héo, sáng/tối).
```
Vertical split composition. LEFT HALF: [BEFORE scene], desaturated, dim, slightly decayed mood. RIGHT HALF: same subject as [AFTER scene], vivid, warm bright light. A thin glowing dividing line in the middle.
```

### K5 — Flat-lay DIY nhìn từ trên
Khi dùng: video công thức pha chế nhiều nguyên liệu.
```
Top-down flat lay on dark rustic wood table: [INGREDIENT 1], [INGREDIENT 2], [INGREDIENT 3] arranged in a triangle, one hand entering from the right pointing at the center item, soft spotlight from above.
```

### K6 — Lịch sử × hiện tại
Khi dùng: video nặng chương lịch sử (kỹ thuật cổ, 江戸/minh họa cổ).
```
BACKGROUND: faded sepia vintage scene of [HISTORICAL SCENE], aged paper texture, blurred. FOREGROUND: [MODERN/REAL OBJECT] in full color sharp focus, dramatic rim light, bridging past and present.
```

### K7 — Scale contrast (bé vs khổng lồ)
Khi dùng: video "vài trăm yên thắng cả hệ thống đắt tiền".
```
LEFT: tiny [CHEAP OBJECT] on an open palm, spotlit. RIGHT/BACKGROUND: huge looming [BIG PROBLEM/EXPENSIVE ALTERNATIVE] towering in shadow. Exaggerated size contrast, cinematic.
```

### K8 — POV tay chìa về camera
Khi dùng: video "tôi trao cho bạn bí quyết".
```
First-person POV: a hand holding [SOLUTION object] extended toward the camera, sharp focus on the object, [PROBLEM scene] blurred bokeh in the dark background, shallow depth of field.
```

### B1 — BENCHMARK-BRIGHT (khuôn CHỦ LỰC từ 2026-07-30 — đúc từ khám kênh)

> **Nguồn:** `CHANNEL_DIAGNOSIS_2026-07-30.md` §3a — đặt 8 thumbnail mình cạnh 8 của 昔の人の知恵 (floor 4K view/video): nó **8/8 nền SÁNG + 1 vật thể + CON SỐ kết quả to (−21℃・6,000円・6か月) + mũi tên đỏ**; mình 6/8 nền tối moody + lời hứa văn chương → suy luận CTR chết ngay vòng test. **Từ 2026-07-30: B1 là mặc định cho video mới + thay dần thumbnail video cũ; nền tối moody CẤM quay lại** (cùng án với health 07-21).

Công thức: **[SCENE SÁNG high-key: trời xanh/ánh nắng/tường sáng] + [1 VẬT chủ thể rõ, chiếm ~1/3 khung, lệch phải] + chữ 3dan PIL (`tools/make_thumb_3dan.py`) trong đó tầng 2/3 có CON SỐ KẾT QUẢ + badge amber số tiền.** Mũi tên đỏ chỉ vào vật khi có quan hệ A→B (khuôn K1 lồng được vào B1).
- Prompt template (no-text, user gen): `bright high-key photograph, clear blue summer sky / sunlit bright wall, [VẬT] as single clear subject on the right third, crisp daylight, vivid colors, no people faces, no text, no brand logos, 16:9` + KHỐI BRAND.
- Fallback không gen được: ảnh thật SÁNG của chính video (đường video 07 đã đi) — chọn frame/slide sáng nhất, KHÔNG dim.
- Chữ: tối đa 3 tầng + badge; tầng 2 TO NHẤT ≥1/3 chiều cao; **phải có ≥1 con số** (数百円/300円/7割/◯分) ở tầng 2 hoặc 3 hoặc badge.
- Duyệt: 3 cửa cũ + **cửa mới "SÁNG"**: thumbnail đặt cạnh 8 bản benchmark (`06_VIDEO/_diag_thumbs/_bench_sheet.jpg`) không được là cái TỐI nhất hàng.

## ⚖️ HẠN MỨC ❌/✅ — tối đa ~1/3 video, KHÔNG 2 video liên tiếp (user chốt 2026-08-05)

> user: *"thi thoảng đổi prompt đừng cho dấu x vs o vào nữa"*. Đúng — sau loạt thay 2026-08-05, **❌/✅ đã chiếm 4/9 video** (01 · 04 · 06 · 08). Thành công thức = đúng cái `youtube-compliance.md` §1 gọi là "video giống hệt nhau chỉ khác tiêu đề", và mắt subscriber cũng chai.

**Luật:** cặp ❌/✅ là **một** thủ pháp trong nhiều, không phải khuôn mặc định. Trần ~1/3 tổng video, và **không dùng ở 2 video đăng liên tiếp**.

**Thủ pháp thay thế (đều đã có trong thư viện §8 khuôn, dùng xoay vòng):**
| thủ pháp | khi nào mạnh nhất | ví dụ đã áp |
|---|---|---|
| **K3 macro hero** — 1 vật duy nhất, không so sánh | bài xoay quanh 1 vật rẻ | 14 (chai bẫy) · 02 (chậu cây) |
| **K7 tương phản kích cỡ** — bé xíu ↔ khổng lồ | "vài trăm yên thắng vấn đề lớn" | 01 · 05 (tổ ong khổng lồ ↔ lọ bé) |
| **K1 mũi tên** — biến đổi A→B, KHÔNG cần ❌/✅ | có quan hệ nhân quả | 03 · 07 (nhiệt dội khỏi rèm) |
| **hướng chuyển động** — vật thể tự tránh/tự đi vào | côn trùng, luồng khí | 02 (muỗi ngoặt ra) · 14 (muỗi lao vào) |
| **K6 xưa × nay** — sepia hậu cảnh + hiện tại nét | bài nặng lịch sử | 07 |
| **before/after trần** — chia đôi, không dấu | kết quả nhìn thấy bằng mắt | 06 |

⚠️ Ghi ngày + thủ pháp vào SỔ THEO DÕI cuối file mỗi lần chốt, để biết còn cách bao nhiêu video.

## 🚫 KHÔNG DÙNG MẶT NGƯỜI TRÊN THUMBNAIL (chốt toàn kênh 2026-08-05)

> user chốt sau khi làm video 15 (扇風機) và video 08 v3.3 (梅干し): **thumbnail co-dai không dùng mặt người.**
> Đè phần "mặt ghép sau bằng ảnh stock ẩn danh" của spec v3.2 video 08 và mọi spec cũ có mặt người.

- **Hệ quả phải biết:** như vậy **cố ý KHÔNG đạt gate 4** của `audience-45plus.md` §1 (đòi ≥1 mặt biểu cảm đọc được ở 168px). Đây là **lệch luật có chủ ý**, không phải sót.
- **Thay mặt người bằng gì:** điểm nhấn cảm xúc phải do HÌNH gánh — ⓐ **tương phản nhiệt độ / lạnh-ấm** trong một khung (video 15: khí nóng cam ↔ khí lạnh cyan · video 08: tủ lạnh xanh lạnh ↔ lu mơ nắng vàng) ⓑ **cặp ❌/✅** ⓒ **kết cấu macro gây thèm/gây ghét** (mơ đỏ bóng nước ↔ rau thâm nhớt).
- ⚠️ **Nếu CTR đo được thấp thì BIẾN ĐẦU TIÊN nên đảo lại là đưa mặt người vào** — đừng đảo chữ hay đổi khuôn trước. Ghi ngày đảo vào `08_ANALYTICS_LOG.md`.
- 🚫 Vẫn giữ: **tuyệt đối không mô tả người trong prompt gen** — v3.1 của video 08 bị bộ gen **chặn thẳng** vì mô tả người kèm tuổi + dân tộc.

## 🔖 DẤU NHẬN DIỆN KÊNH (bắt buộc mọi thumbnail từ video 15 — user chốt 2026-08-04)

> user: *"thêm 1 chút để nhận biết đó là kênh mình"*. **Dấu phải do PIL đè, KHÔNG để AI bake** —
> nhận diện chỉ có giá trị khi nó **giống hệt từng pixel qua mọi video**, mà AI thì mỗi lần vẽ một kiểu.

**Tool:** `tools/stamp_brand.py` — spec khoá cứng trong file, chạy không cần cờ:
```bash
python tools\stamp_brand.py <thumb>.jpg -o <thumb_final>.jpg --preview
```

| | spec (ĐÃ KHOÁ) |
|---|---|
| Vị trí | **góc TRÊN–PHẢI**. Dưới–phải là của YouTube (đè timestamp) · dưới–trái đã có badge số của khuôn B1 |
| Cấu tạo | khối bo góc ink `#16181D` (alpha 234) + **ô vuông vàng `#FFD200` bọc glyph 「秘」** + `古代の秘訣` chữ trắng |
| Cỡ | `PLATE_H = 0.120` (12% chiều cao khung) — **chốt sau khi so A/B 3 cỡ ở 168px**: 0,092 quá mờ · 0,143 nặng, đáy khối gần chạm mũi tên đỏ |
| Neo nhận diện | **1 glyph 「秘」 to**, không phải tên kênh. Ở 168px chữ nhỏ thành cháo; khối vàng + 1 glyph mới đọc ra là "kênh đó" |
| Màu | đúng bộ Vox của kênh → thumbnail và thẻ trong video cùng một họ |

⛔ **Đừng đổi spec giữa các video** — đổi là mất sạch giá trị nhận diện đã tích được.

## SỔ THEO DÕI — video nào đã dùng khuôn nào

| Video | Khuôn | Ghi chú |
|---|---|---|
| 01_hosan-shiroari | K1 (arrow) | mẫu chuẩn kênh `01/thumbnail_v3_final.jpg` |
| 02_niwa-mushiyoke-10 | K2 (X-diagram) + text 3dan | `02/thumbnail_i_3dan.png` |
| 03_natsu-zassou | **K5 (flat-lay) + text 3dan** | CHỐT 2026-07-17: `03/thumbnail_3dan_flatlay.png`; các bản K2 cũ để A/B. Video 04 tránh K5/K2 (gợi ý K3/K6/K7) |
| 04_gokiburi-yosetsukenai | **K7 (scale contrast) + text 3dan** | ảnh gen K7 (lọ dầu hero + gián + bình xịt) → `04/thumbnail_04.jpg`; chờ user chốt. Video 05 tránh K7/K5 |
| 05_suzumebachi-yosetsukenai | **Đối đầu (swarm vs tay xịt 木酢液) + text 3dan chữ TO** | CHỐT: `05/thumbnail_05.jpg` (tay xịt hổ phách + tổ ong đông; chữ trái, 数百円 đỏ, cỡ đại cho khán giả già). Prompt trong script 05 Khối 4. Video 06 tránh concept đối đầu/K7 |
| 06_mizumawari-numeri | **K4 (Before/After split dọc) + text 3dan + badge 50〜100円** | Prompt A (lỗ thoát nước bẩn→sạch) + phương án B (vòi đầy vảy nước→bóng) ở script 06 Khối 4. **Chờ user gen** rồi đè chữ 3 tầng bằng PIL. Chọn K4 vì đề tài có before/after đo được bằng mắt. Video 07 tránh K4 + đối đầu |

| 07_natsu-denkidai-suzumi | ✅ **CHỐT 2026-07-27 — K4 (Before/After split) + text 3dan + badge 「数百円 / すだれ・よしず」** | **KHÔNG đi đường AI-gen** (key Gemini mất cùng project stickman) → dựng từ **ảnh thật của chính video này** bằng tool mới `tools/make_thumb_3dan.py`. File chốt: `06_VIDEO/07_natsu-denkidai-suzumi/_thumb/thumb_B.png` — trái 室外機 (crop sát, cánh quạt rõ ở 120px) \| phải すだれ; chữ 「昔の涼み方 / **室外機に**日除け / エアコンの電気代が下がる」. Chọn bản này vì có **cả 2 keyword title** (すだれ 42 + 室外機の日除け 35); bản A (熱の7割は窓から) punch hơn nhưng thiếu 室外機 → giữ làm A/B test. ⚠️ Đã `--blur-box` xoá **logo hãng「Carrier」** trên dàn nóng (checklist mục 4). ⚠️ **K6 dự định KHÔNG dùng được** (K6 cần ảnh gen) → thực tế rơi về K4; **video 08 giờ phải tránh K4 + K7** (K7 vừa dùng ở 13). Video 08 nếu cũng không gen được ảnh thì chọn khuôn dựng-được-từ-ảnh-thật |

| 08_hozonshoku-shio-hosu-hakko | **K8 (POV tay chìa về camera) + text 3dan + badge 「捨てる食べ物 年6万円」** | Prompt A (ざる muối + 干し野菜, tủ lạnh mờ xanh lạnh phía sau) + phương án B (chỉ 1 hero = muỗng muối) ở script 08 Khối 4. **Chờ user gen.** K8 chưa dùng lần nào trong 7 video đầu; đề tài không có before/after nên K4 vô nghĩa. Tương phản ấm(昔)↔lạnh(冷蔵庫) làm điểm nhấn. Video 09 tránh K8/K6 |

| 09_houchou-togikata-toishi | **K3 (Macro hero) + text 3dan + badge 「1000円で十年」** | Prompt A (lưỡi dao trên đá mài ướt + 研ぎ汁 trắng) + phương án B (thêm 2 đồng 10 yen kê sống dao = đúng cú hook) ở script 09 Khối 4. **Chờ user gen.** K3 chưa dùng lần nào; đề tài xoay quanh 1 vật rẻ (đá mài #1000) = đúng chỗ K3 mạnh. ⚠️ Prompt đã khoá `no hands` + `blade pointing away` (né hình dao chĩa vào người/thương tích). Video 10 tránh K3/K8 |

| 10_kankisen-abura-yogore | **K4 (Before/After) — bắt đầu VÒNG 2 + text 3dan + badge 「数百円で落ちる」** | ⚠️ **8 khuôn đã dùng hết một vòng ở video 01–09** (K1→01, K2→02, K5→03, K7→04, đối đầu→05, K4→06, K6→07, K8→08, K3→09) → từ #10 xoay lại vòng 2. Chọn K4 vì đề có before/after đo bằng mắt (cánh quạt dính dầu ↔ sạch bóng) và đã cách 4 video. Prompt A + phương án B (chậu nước nóng + bột) ở script 10 Khối 4. **Chờ user gen.** Video 11 tránh K4/K3 |

| 11_mado-sasshi-junban | **K2 (X-diagram) + text 3dan + badge 「割り箸と古布 0円」** | Phải tránh 4 khuôn của 4 video gần nhất (K6→07, K8→08, K3→09, K4→10); K2 dùng lần cuối ở **video 02**, cách 9 video. Chọn K2 vì nó **dịch đúng cú lật của title thành hình**: ❌ xịt nước vào rãnh đầy cát → ✅ đũa bọc vải khô miết rãnh. Phương án B = macro lỗ thoát nước bị tắc. **Chờ user gen.** Video 12 tránh K2/K4 |

| 13_veranda-mizu-nigemichi | **K7 (Scale contrast) + text 3dan + badge 「確認はコップ一杯」** | Tránh 4 khuôn gần nhất (K3→09, K4→10, K2→11, K1→12). K7 dùng lần cuối ở **video 04, cách 9 video**. K7 = "vật bé xíu ↔ hậu quả khổng lồ" = đúng cấu trúc bài (lỗ thoát nước cỡ đầu ngón ↔ nước tràn hỏng sàn). Phương án B = cốc nước đang rót vào lỗ. **Chờ user gen.** Video 14 tránh K7/K1 |
| 12_genkan-hakikata *(đổi tên)* | **K1 (Arrow diagram) + text 3dan + badge 「茶殻だけ 0円」** | Tránh 4 khuôn gần nhất (K8→08, K3→09, K4→10, K2→11). **K1 dùng lần cuối ở video 01, cách 11 video — xa nhất thư viện.** K1 dịch đúng cú lật: quét khô (bụi bay mù) → mũi tên đỏ → rắc bã trà ẩm (không khí trong). Phương án B = hero nắm bã trà. **Chờ user gen.** Video 13 tránh K1/K2 |

| 14_ka-hakko-trap | **K5 (Flat-lay DIY) + text 3dan + badge 「材料費300円」** | ⚠️ **Sổ này tính khuôn theo thứ tự VIẾT, nhưng luật xoay vòng phải tính theo thứ tự ĐĂNG.** User chốt 2026-07-30 đăng 14 ngay sau 07 (vượt 08–13 chưa render) → 4 khuôn gần nhất thực tế là **04→K7 · 05→đối đầu · 06→K4 · 07→K4**, nên dòng "video 14 tránh K7/K1" ở 13 KHÔNG còn áp dụng. K5 dùng lần cuối ở video 03, cách 4 video đăng → hợp lệ. Prompt A (4 vật + tay chỉ) + B (macro hero 1 điểm nhấn) ở script 14 Khối 4, **đã sửa mâu thuẫn nền** (bản cũ vừa đòi ván gỗ hiên nhà vừa đòi navy phẳng). 🔑 **Không gen được bằng AI** (key Gemini mất) → có sẵn đường ảnh thật: `slide_43` bọt macro + `slide_75` muỗi vằn, lệnh trong script. **Chờ user gen/chốt.** Video kế tiếp tránh K5 + K4 |

> Cập nhật bảng này mỗi lần chốt thumbnail. Prompt đã điền của từng video lưu trong mục サムネ của file script video đó.
| 15_senpuki-netsu-hakidashi | **B1 (benchmark-bright) lồng K1 (Arrow) + text 3dan + badge 「窓は2つ」** · ⭐ **bộ 3 A/B đầy đủ T1/T2/T3** | Tránh **K5 + K4** = 2 khuôn của 2 video ĐĂNG gần nhất (14→K5, 07→K4). **K1 lần cuối lên sóng ở video 01 — xa nhất thư viện.** K1 dịch đúng xương sống thành hình: 扇風機 →(mũi tên đỏ)→ ra ngoài cửa sổ. **T1** baseline (quạt + mũi tên ra cửa sổ) · **T2** đổi 1 biến hình = chai PET đóng đá thay quạt làm chủ thể, **chữ giữ y nguyên** (đúng breakout keyword `凍らせたペットボトル 扇風機`) · **T3** đổi layout = mặt ông lão ngạc nhiên + chỉ 2 dòng, dòng chính 「1円」 cao ≥1/3 khung → **đây là bản đạt gate `audience-45plus.md` §1**. 3 prompt + lệnh `make_thumb_3dan.py` (đường không cần AI) ở script 15 mục 🖼️. **Chờ user gen/chốt.** ⚠️ Ghi rõ để không trôi: **khuôn 3 tầng đang khoá của kênh KHÔNG đạt gate 45+** (dòng chính ≤6 ký + ≥1/3 khung + ≥1 mặt) — việc 6.4 của `audience-45plus.md` chưa làm; ở video này để chính phép A/B T1-vs-T3 trả lời, không tự đổi khuôn kênh. Video kế tiếp tránh **K1 + K5** |

| 16_tsukemono-shio-no-dan | **B1 (bright) lồng K4 (Before/After split dọc)** + chữ bake sẵn trong prompt + badge 「塩100円」 · ⭐ bộ 3 A/B đầy đủ | Tránh **K1** (#15) + **K5** (#14) + **K3** (vừa lên sóng ở bản 01 v4 ngày 08-05). K4 lần cuối ở #10, cách 6 video. **T1** split 3日 (lọ nhựa tủ lạnh, dưa NỔI trên nước) ↔ 3か月 (樽 + 重石, dưa CHÌM) · **T2** đổi 1 biến hình = 重石 macro thành chủ thể (đúng reveal 「潰す道具ではない」), **chữ y nguyên** · **T3** đổi layout = bỏ dòng phụ, `3か月` ≥40% khung + badge → **bản duy nhất có cửa đạt gate ≥1/3**. Prompt bake chữ (bản đang dùng) ở script 16 §⭐ PROMPT GEN; bộ no-text cũ giữ làm dự phòng. ✅ **T1 XONG 2026-08-06** — `06_VIDEO/16_.../thumb_T1_tsukemono.png` (+ .jpg + prev168/120), hero `3か月` **24,5%** khung (ca đo thứ 5 của §6.10), đọc rõ 168px & 120px, không watermark. T2/T3 **chưa gen** (user chỉ cần 1 bản). Video kế tiếp tránh **K4 + K3** |

| 17_haisuiko-numeri-10endama | **B1 (bright) lồng K1 (mũi tên NHÂN QUẢ)** + chữ bake trong prompt + badge 「130年前の科学」 · bộ 3 A/B | Tránh **K4 + K3** (chỉ thị của #16). Chọn **K1** vì thư viện ghi đúng ca này: *"biến đổi A→B — khi có quan hệ nhân quả"*, và user yêu cầu thẳng *"prompt thật ấn tượng có nguyên nhân và kết quả"* (2026-08-10). ⚠️ K1 lên sóng gần nhất ở **#15, cách 2 video** — luật chỉ cấm 2 video LIÊN TIẾP nên hợp lệ, nhưng là khoảng cách gần nhất từng dùng, ghi ra để không trôi. 🔴 **Bệnh của bộ prompt cũ (đã bỏ):** cả 6 bản chỉ có KẾT QUẢ (bồn sáng + xu đồng), **không khung nào có ぬめり** = không có nguyên nhân → không có lý do dừng lại; thiếu cả badge, cả góc trống cho 「秘」/timestamp, và 3 plate no-text bị để chung file FLOW (bẫy chouhen 21). **T1** giỏ cống NHỚT →(mũi tên đỏ)→ giỏ SẠCH + 5 đồng 10円 · **T2** đổi 1 biến hình = bỏ mũi tên, MỘT khung macro, nhớt phủ khắp lưới chỉ **lùi thành vòng sạch quanh mỗi đồng xu** (đúng F5), **chữ y nguyên** · **T3** đổi layout = bỏ dòng phụ, `10円` ≥40% khung → bản duy nhất có cửa đạt gate ≥1/3. Chữ đọc liền một câu nhân quả: `排水溝のぬめりが` → `10円` → `育たなくなる`. Prompt: `06_VIDEO/17_.../thumb_prompts_FLOW.txt` (có chữ) + `thumb_prompts_PLATE.txt` (nền không chữ, **file riêng**). ✅ **T1 XONG 2026-08-10** — `06_VIDEO/17_.../thumb_T1_haisuiko_final.jpg` (bản upload; PNG 2,81 MB vượt trần 2 MB), gốc AI `thumb_T1_raw.jpg`. Đã vá watermark ✦ dưới–phải (patch texture, không inpaint) · crop về 16:9 1920×1080 · dấu 「秘」 `--pos tr`. Hero `10円` **23,2%** khung = **ca đo thứ 6 của §6.10** (rớt trần ≥1/3 nhưng đọc rõ 168px **và** 120px — dải 6 ca giờ là 23–31%). T2/T3 **chưa gen** (user chỉ cần 1 bản). Video kế tiếp tránh **K1 + K4** |
| 19_haisuiko-naze-tsumaru | **B1 (bright) lồng K3 (macro hero)** + chữ bake trong prompt + badge 「道具は100円」 · bộ 3 A/B | Tránh **K1 + K4** (chỉ thị của #17). **K3** lần cuối ở bản **01 v4** (2026-08-05), cách 3 video đăng → hợp lệ. 🔴 **Điều kiện sống:** cụm 排水口 đã chết 2 lần ở đúng CTR (**06 = 1,0%**, **17 = 0%**), cả hai đều là **cận cảnh miệng cống** ⇒ bộ này đổi hẳn chủ thể sang **ống PVC cắt đôi + lớp mỡ sáp + nhiệt kế kim chỉ 60**, không khung nào nhìn từ trên xuống miệng cống. Chữ đọc liền một mạch: `排水口が詰まる理由` → **`60度`** → `熱いお湯は逆効果` + badge `道具は100円`. **T1** baseline · **T2** đổi ĐÚNG 1 biến = thêm nước sôi bốc hơi dội vào mà mỡ **không tan** (đưa NGUYÊN NHÂN vào khung), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / ảnh nửa phải, **chữ vẫn y nguyên**. ⚠️ **Lệch có chủ ý với #16/#17:** hai bản đó cho T3 bỏ dòng phụ để hero ≥40%; ở đây KHÔNG bỏ vì `ab-3title-3thumb.md` §3 mục 6 đòi chữ giống nhau cả 3 bản (biến thử là HÌNH) ⇒ chấp nhận rớt gate tỉ lệ ≥1/3, duyệt bằng legibility 168px/120px. Prompt: `06_VIDEO/19_.../thumb_prompts_FLOW.txt` (bake chữ) + `_BLOCKS.md` + `_TENFILE.txt` + `_PLATE.txt` (no-text, **file riêng**). Đo máy: TEXT @6% (trần 15%) · 1417–1489 ký (trần 1500) ✅. ✅ **T1 XONG 2026-08-14** — `thumb_T1_haisuiko-60do_final.jpg` (648 KB, dưới trần 2 MB; gốc AI `_raw_T1_haisuiko-60do.png` trong `_wm_orig/`). Chữ bake **đúng cả 4 khối, 0 ký tự nát** kể cả `逆効果`. Đã vá **2 dấu ✦** ở **(130,223)** và **(1327,55)** — ⚠️ **cả hai nằm GIỮA KHUNG, không phải góc dưới–phải**, nên quét-theo-góc bỏ sót sạch; định vị bằng MẮT. 🔴 **Hai bài học kỹ thuật:** ① **quét blob bằng máy trượt hoàn toàn** (top-10 local-contrast trúng toàn nét chữ `60度` — đúng cảnh báo `media-library.md` §2.10⑤) ② **vá bằng trung vị TỪNG HÀNG cũng hỏng** ở nền có gradient NGANG (để lại vệt chữ nhật đen, tệ hơn ✦ gốc) → cách chạy được là **nội suy Laplace từ 4 biên hộp** (Jacobi 400 vòng) + nhiễu ±1,1; kiểm `diff` phải = **0 pixel đổi ngoài 2 hộp**. Rồi `stamp_brand.py` đóng 「秘」 góc trên–phải. ⚠️ **Ảnh CÓ MẶT NGƯỜI (ông cụ góc trên–phải) = lệch luật "🚫 không mặt người" của kênh** — user gen theo hướng khác prompt (prompt ghi `NO people`). **Giữ, và coi là phép thử có chủ ý**: chính §🚫 ghi *"nếu CTR đo được thấp thì BIẾN ĐẦU TIÊN nên đảo lại là đưa mặt người vào"*, mà cụm 排水口 đã 1,0% (06) và 0% (17) → đây đúng chỗ để đảo. **Đọc CTR sau 7 ngày, ghi vào `08_ANALYTICS_LOG.md`.** T2/T3 **chưa gen** → gate 3×3 vẫn hở. ⛔ Bộ prompt cũ ở script 19 Khối 4 **BỎ** (kiểu "No text" + T3 mô tả **mặt người** = vi phạm luật cấm mặt người 2026-08-05). **Chờ user gen.** Video kế tiếp tránh **K3 + K1** |
| 22_furaipan-kuttsuku | **B1 (bright) lồng K1 (arrow)** + chữ bake trong prompt + badge 「3000円」 · bộ 3 A/B | CHỐT 2026-08-18. Tránh **K2** (#21) + **K8** (#20) = 2 video liền trước; **không ❌/✅** (đang cấm, đã chạm trần 1/3); không mặt người. ⚠️ K1 lần cuối ở **#17 (2026-08-10), cách 4 video** → hợp lệ; chỉ thị 「tránh K3+K1」 của #19 áp cho #20 và đã tuân (K8). Chữ đọc liền một câu: `くっつくフライパン` → **`10分で戻る`** → `油は敷くな` + badge `3000円`. **T1** chảo xỉn →(mũi tên đỏ)→ chảo đen bóng · **T2** đổi ĐÚNG 1 biến hình = macro **một giọt nước lăn tròn** trên mặt chảo nóng (chính phép thử của cold open), chữ y nguyên · **T3** đổi layout = nhìn từ trên, một chảo nửa xỉn nửa bóng, chữ dồn cột trái. Prompt: `06_VIDEO/22_furaipan-kuttsuku/thumb_prompts_FLOW.txt` (bake chữ) + `_BLOCKS.md` + `_TENFILE.txt` + `_PLATE.txt` (no-text, **file riêng**). Đo máy: **TEXT @7–8%** (trần 15%) · **1.071–1.152 ký** (trần 1.500) ✅. **Chờ user gen** → vá ✦ (bake chữ ⇒ VÁ, không cắt) → `stamp_brand.py --pos tr`. Video kế tiếp tránh **K1 + K2** |

| ⏸ ~~20_edo-jidai-kinun-shikumi~~ (B1+K6) | **ĐỀ ĐÃ PARK 2026-08-14** — thumbnail chưa từng gen ⇒ **K6 vẫn coi như CHƯA lên sóng, video sau dùng được.** Prompt giữ ở `06_VIDEO/_parked/edo-jidai-kinun-shikumi/` |
| **20_sentei-koshin-akinasu** | **B1 (bright) lồng K8 (POV tay chìa về camera)** + chữ bake trong prompt + badge 「今週だけ」 · bộ 3 A/B | Tránh **K1** (#15,#17) · **K4** (#16) · **K3** (#19) · K6 (đã ghi cho đề Edo). **K8 lần cuối ở #08 — cách 12 video, XA NHẤT thư viện.** K8 (「POV bàn tay chìa vật giải pháp về camera, vấn đề mờ phía sau」) **dịch đúng nghịch lý của bài thành hình**: bàn tay đeo găng trắng cầm kéo **đang kẹp một cành CÓ QUẢ tím**, cây cà mệt mờ phía sau. Bộ chữ `8月の剪定 / 実ごと切る (HERO, 5 ký, rộng ~2/3 khung) / 秋まで採れます` + badge `今週だけ`. **T1** POV kéo + quả · **T2** đổi ĐÚNG 1 biến = macro bông hoa **短花柱花** (nhụy ngắn hơn nhị), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái, ảnh nửa phải (cây cắt trụi + cành rụng còn quả). 🚫 không mặt người — **bàn tay thì được** (luật 2026-08-05). Đo máy: TEXT @7–8% (trần 15%) · 1190–1363 ký (trần 1500) ✅. 🔴 Gen xong **BẮT BUỘC xoá watermark** (`media-library.md` §2.10⑤b — thumbnail bake chữ ⇒ **VÁ**, không cắt). **Chờ user gen.** Video kế tiếp tránh **K8 + K3** |
| **21_furo-no-kabi-modoru** | **B1 (bright) lồng K2 (X-diagram)** + chữ bake trong prompt + badge 「洗剤代0円」 · bộ 3 A/B | Tránh **K8** (#20) + **K3** (#19). **K2 lần cuối lên sóng ở #11, cách 9 video.** K2 (「hành động quen thuộc hóa ra sai」) dịch đúng cú lật trung tâm: xịt thuốc tẩy → 10 ngày sau đen lại. Bộ chữ đọc liền một mạch: `風呂の黒カビ` → **`50度 90秒`** (HERO, 6 ký, rộng ~2/3 khung) → `漂白では戻る` + badge `洗剤代0円`. **T1** K2 trái xịt/phải vòi sen hơi nước · **T2** đổi ĐÚNG 1 biến = MỘT khung macro パッキン (nửa trên còn mốc, nửa dưới bị luồng nước nóng quét), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / ảnh nửa phải, chữ y nguyên. 🚫 không mặt người (bàn tay đeo găng thì được). Đo máy: **TEXT @6–7% (trần 15%) · 1321–1480 ký (trần 1500)** ✅. 🔴 Gen xong **BẮT BUỘC xoá watermark** — thumbnail bake chữ ⇒ **VÁ, không cắt** (`media-library.md` §2.10⑤b). **Chờ user gen.** ⚠️⚠️ **Video kế tiếp: tránh K2 + K8, VÀ CẤM ❌/✅** — cặp ❌/✅ sau bản này chạm trần ~1/3 (§⚖️), không được dùng ở 2 video liên tiếp |
| 23_kobae-kakurega | **B1 (bright) lồng K3 (macro hero)** | Tránh K1 (#22) + K2 (#21). Ghi đủ ở `07_UPLOADED/23_kobae-kakurega/_scripts/23_kobae-kakurega.md`. Video kế tiếp tránh K1 + K2 |
| 24_kamemushi-3mm-sukima | **B1 (bright) lồng K6 (lịch sử×hiện tại)** | Tránh K1+K3 (#23) + K2 (#21). K6 chưa lên sóng lần nào trong 23 video trước. Ghi đủ ở `07_UPLOADED/24_kamemushi-3mm-sukima/_scripts/24_kamemushi-3mm-sukima.md`. **Video kế tiếp tránh K6 + K3.** |
| 28_dannetsu-tenjo-alumi | **B1 (bright) lồng K6 (lịch sử × hiện tại)** + chữ bake trong prompt + badge 「110円」 · bộ 3 A/B | CHỐT 2026-09-03. Tránh **K7** (#27) + **K4** (#26) = 2 video ĐĂNG liền trước. **K6 lần cuối lên sóng ở #24 (2026-08-25), cách 3 video** → hợp lệ. K6 dịch đúng xương sống thành hình: **xưa chặn nhiệt bằng BỀ DÀY (mái tranh 50cm, sepia mờ) ↔ nay chặn bằng PHẢN XẠ (nhôm 0,2mm, nét căng)**. Bộ chữ đọc liền một mạch: `天井の断熱` → **`60度`** (HERO 3 ký, rộng ~2/3 khung) → `窓ではない` + badge `110円`. **T1** sepia かやぶき + tay cầm tấm nhôm & nhiệt kế · **T2** đổi ĐÚNG 1 biến hình = khoang gác mái thật nhìn qua nắp 点検口 đang mở (đưa hiện trường của bài vào khung), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / mặt cắt trần nửa phải (mái đỏ rực → lớp nhôm bạc → phòng xanh mát), chữ y nguyên. ⛔ Không đưa `アルミ` lên chữ dù nó là vật chính — 外来語, cấm ở thumbnail (`audience-45plus.md` §5.2); nó nằm trong ẢNH. 🚫 không mặt người (bàn tay được). Đo máy: **TEXT @8–9% (trần 15%) · 1.040–1.150 ký (trần 1.500)** ✅. Prompt: `06_VIDEO/28_dannetsu-tenjo-alumi/thumb_prompts_{FLOW.txt,BLOCKS.md,TENFILE.txt,PLATE.txt}` (PLATE no-text **file riêng**). 🔴 Gen xong **BẮT BUỘC xoá ✦ — bake chữ ⇒ VÁ, không cắt** → `stamp_brand.py --pos tr`. **Chờ user gen.** Video kế tiếp tránh **K6 + K7**
| **25_mizugame-suyaki-tarai** | **B1 (bright) lồng K1 (Arrow diagram)** + chữ bake trong prompt + badge 「0円の涼しさ」 · bộ 3 A/B | CHỐT 2026-08-27. Tránh **K6** (#24) + **K3** (#23) đúng chỉ thị. K1 lần cuối ở **#22, cách 3 video** → hợp lệ. K1 dịch đúng xương sống thành hình: ly nước máy ấm/tủ lạnh mở KHÔNG có nước mát sẵn (vấn đề, trái, mờ) →(mũi tên đỏ)→ chum gốm 素焼き đọng nước mát (giải pháp, phải, sáng nét). Chữ đọc liền một mạch: `電気なしで` → **`水がめ`** (HERO) → `祖母は涼しかった` + badge `0円の涼しさ`. **T1** ly nước ấm + bàn tay thất vọng →mũi tên→ chum · **T2** đổi ĐÚNG 1 biến hình = cảnh trái đổi thành tủ lạnh mở cửa với chai mugicha vẫn ấm (đúng nghịch lý "có tủ lạnh mà không có nước mát" của cold open), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / ảnh chum nửa phải. 🚫 không mặt người — chỉ bàn tay được phép. Prompt: `06_VIDEO/25_mizugame-suyaki-tarai/thumb_prompts_FLOW.txt` (bake chữ) + `_BLOCKS.md` + `_TENFILE.txt` + `_PLATE.txt` (no-text, **file riêng**). Đo máy: **TEXT @8–9%** (trần 15%) · **1.043–1.385 ký** (trần 1.500) ✅. **Chờ user gen** → vá ✦ (bake chữ ⇒ VÁ, không cắt) → `stamp_brand.py --pos tr`. Video kế tiếp tránh **K1 + K6** |
| **26_shoji-kokyuu-kami** | **B1 (bright) lồng K4 (Before/After split dọc)** · bộ 3 A/B | Tránh **K1** (#25) + **K6** (#24). Ghi đủ ở `07_UPLOADED/26_shoji-kokyuu-kami/_scripts/26_shoji-kokyuu-kami.md` §KHỐI 4. Đã đăng, `thumbnail_T2.jpg` trong `_upload/`. Video kế tiếp tránh **K4 + K1** |
| **27_kankisen-abura-akujiru** | **B1 (bright) lồng K7 (scale contrast)** + chữ bake trong prompt + badge 「0円」 · bộ 3 A/B | CHỐT 2026-09-01. Tránh **K1** (#25) + **K4** (#26). **K7 lần cuối ở #04/#13 — xa nhất thư viện.** K7 dịch đúng cấu trúc bài: giải pháp bé xíu 0円 (nắm tro trong lòng bàn tay) ↔ vấn đề khổng lồ (quạt hút đen kịt dầu, tốn 1万5千円/nguy cơ cháy+té). Chữ đọc liền một mạch: `換気扇の油` → **`かまどの灰`** (HERO) → `重曹では無理` + badge `0円`. **T1** nắm tro bé xíu ↔ quạt hút khổng lồ đen kịt · **T2** đổi ĐÚNG 1 biến hình = macro phản ứng 鹸化 (giọt灰汁 rơi vào lớp dầu đen, sủi bọt tan), chữ y nguyên · **T3** đổi layout = nhìn từ trên, chữ dồn cột trái, tô tro + cánh quạt đặt cạnh nhau. 🚫 không mặt người — chỉ bàn tay được phép (T1). Prompt: `06_VIDEO/27_kankisen-abura-akujiru/thumb_prompts_FLOW.txt` (bake chữ) + `_BLOCKS.md` + `_TENFILE.txt` + `_PLATE.txt` (no-text, **file riêng**). Đo máy: **TEXT @6%** (trần 15%) · **1.171–1.401 ký** (trần 1.500) ✅. **Chờ user gen** → soi từng ký tự → vá ✦ (bake chữ ⇒ VÁ, không cắt) → `stamp_brand.py --pos tr`. Video kế tiếp tránh **K7 + K1** |

> ⚠️ **Khi thứ tự đăng ≠ thứ tự viết, tính khuôn theo thứ tự ĐĂNG** — người xem chỉ thấy cái đã lên sóng (bài học 14, 2026-07-30).

### 🔄 ĐỢT THAY THUMBNAIL LIVE 2026-07-30 (khuôn B1 — khám kênh, user duyệt hướng)

| Video live | Thumbnail cũ | v2 (B1) | Trạng thái |
|---|---|---|---|
| 05_suzumebachi (4 view) | tối, tổ ong + tay xịt | B1: 軒下 nắng sáng + tổ ong + chữ số 数百円 — gói ở script 05 §サムネ v2 | ✅ **ĐÃ SET 2026-08-01** (user gen ảnh + gật; `thumbnails.set` lQ7P_jN9mqM; file `06_VIDEO/_thumb_v2/05_v2.png`; ✦ watermark xóa bằng mask hình sao + fill khuếch tán — src sạch `src/05_clean.jpg`) |
| 07_denkidai (12 view — video ĐANG LÊN) | K4 split tối (室外機\|すだれ) | B1: すだれ ngoài cửa sổ nắng gắt + 電気代が下がる + badge 数百円 — script 07 §サムネ v2 | ✅ **ĐÃ SET 2026-08-01** (`thumbnails.set` OZj3enOedQk; file `06_VIDEO/_thumb_v2/07_v2.png`, --bright 1.15). Ban đầu user định A/B qua Studio 「テストして比較」 rồi đổi ý cùng ngày → set thẳng. Bản cũ giữ ở `07_UPLOADED/07_.../_upload/thumbnail.png` — nếu 7 ngày tới view/giờ của 07 TỤT so với trước thì đảo lại được ngay |
| 14_ka-hakko-trap (1 view) | bàn tối + 材料は台所だけ | B1: bàn bếp sáng + chai bẫy PET + 蚊が自分から入る + badge 300円 — script 14 §サムネ v2 | ✅ **ĐÃ SET 2026-07-30** (user gen ảnh + gật; `thumbnails.set` Edfjmu-gRjg; file `06_VIDEO/_thumb_v2/14_v2.png`; ✦ watermark xóa bằng mask sáng-hơn-nền-median-blur trong hộp né chủ thể — bản đầu hộp rộng ăn lẹm mép đĩa, phải làm lại từ src) |
| 02_niwa-mushiyoke (15 view — NHIỀU VIEW NHẤT kênh, thêm vào đợt 2026-08-01) | muỗi+❌+cây, nhiều chi tiết, tối | B1: góc vườn nắng + chậu マリーゴールド/ハーブ + 蚊が寄りつかない + badge 数百円 — prompt ở khối ngay dưới (script gốc 02 không còn — đăng trước flow gom script) | ✅ **ĐÃ SET 2026-08-01** (user gen ảnh + gật; `thumbnails.set` NWPnrezfBDc; file `06_VIDEO/_thumb_v2/02_v2.png`; src sạch `src/02_clean.jpg`) |

⚠️ Các bản v2 dùng chung HỌ B1 nhưng khác vật/khác bối cảnh/khác màu accent tầng 2 — không lặp nguyên bộ.

#### Prompt v2 cho 02_niwa-mushiyoke-10 (soạn 2026-08-01 — script gốc thất lạc nên lưu tại đây)

> Title live: 蚊が寄りつかない庭は数百円で作れる――業界が広めたがらない10の植物の知恵. Cây trong video (đếm từ subs.srt): バジル 7 · シトロネラ 6 · マリーゴールド 5 · ローズマリー 4 · ラベンダー 4 · ミント 2.

**Prompt A (gen, no-text):**
```
bright high-key photograph, sunlit Japanese garden corner in summer morning light, terracotta pots of blooming orange marigold and green herbs (basil, rosemary) arranged as the single clear subject on the right third of frame, clear blue sky and warm sunlight, vivid saturated colors, sharp focus, no people, no faces, no insects, no text, no brand logos, 16:9
```
**Prompt B (dự phòng, hero 1 chậu):** như A nhưng chủ thể = `one terracotta pot of blooming orange marigold on a bright wooden veranda in strong sunlight, garden blurred in background`.

**Chữ 3 tầng + badge (PIL — KHÔNG bake bằng AI):**
```
python tools\make_thumb_3dan.py 06_VIDEO\_thumb_v2\02_v2.png --photo <ảnh gen> ^
  --line1 "置くだけでいい" --line2 "蚊が|w" "寄りつかない|y" ^
  --line3 "数百円・10の植物" --badge "数百円" --badge-sub "10の植物" --badge-size 84
```
> 🔴 **Bẫy cú pháp `--line2` (dính 2026-08-01):** mỗi khúc màu là **một argument riêng** `"chữ|màu"` — gộp thành 1 chuỗi `"蚊が|w寄りつかない|y"` thì chữ `|w` bị vẽ literal lên ảnh. Đã sửa spec ở cả script 05/07.
```
```
- Mọi yếu tố chữ đều có trong title live (蚊が寄りつかない・数百円・10の植物) — không hứa gì ngoài video. Compliance sạch (không 殺/駆除).
- ⚠️ Prompt A cố ý **no insects** — muỗi vẽ to trên thumbnail là chi tiết gây rối 120px (bài học bản cũ); lời hứa nằm ở chữ + cây.
- Duyệt cửa SÁNG cạnh `_bench_sheet.jpg` như 2 bản kia. Sau khi user gật: `thumbnails.set` (video ID lấy qua `pipeline_status.py --check` / uploads playlist) — KHÔNG đổi title/概要欄.

### 🔄 ĐỢT THAY THUMBNAIL LIVE **v3** 2026-08-05 (user gen ảnh mới, bake text bằng AI)

> User đưa 3 ảnh gen sẵn (đã bake chữ) cho 3 video ĐANG LIVE, yêu cầu sửa + cấp title khớp từng ảnh.
> Ảnh gốc: `06_VIDEO/_thumb_v3/src/<NN>_src.jpg` · bản sạch full-res `<NN>_clean.jpg` · **bản giao: `06_VIDEO/_thumb_v3/<NN>_v3_brand.png|.jpg`** (1920×1080, <1 MB) · tool `06_VIDEO/_thumb_v3/fix_v3.py` (chạy lại 1 lệnh) · gate sheet `_gate_sheet_v3.png`.
> ⚠️ **CHƯA set lên kênh** — chờ user gật (`feedback_chot_truoc_khi_dang`).

| Video live | Ảnh v3 nói gì | Đã sửa gì | Dòng chính |
|---|---|---|---|
| **05_suzumebachi** (thay v2 08-01) | split 春の巣 nhỏ → mũi tên đỏ → 夏の巣 千匹 · badge 春なら数百円 | xoá ✦ | 「千匹」 **31,6%** khung, 2 ký |
| **07_natsu-denkidai** (thay v2 08-01) | すだれ nắng gắt + 4 mũi tên nhiệt dội · badge すだれ 数百円 | xoá ✦ | 「熱の7割」 **21,9%**, 4 ký |
| **02_niwa-mushiyoke** (thay v2 08-01) | chậu マリーゴールド + muỗi ngoặt ra · badge 数百円 | xoá ✦ **+ xoá glyph ＝ lỗi** | 「10の植物」 **20,6%**, 5 ký |

**🔴 Ba bẫy đã dính khi làm sạch — ghi để lần sau không lặp:**
1. **Chữ do AI bake PHẢI soi từng ký tự trước khi dùng.** Ảnh 02 gen ra 「置くだけ＝でいい」 — thừa một dấu ＝ giữa câu, sai ngữ pháp, người Nhật nhìn là mất tin ngay. Đã xoá → còn 「置くだけ でいい」 (khoảng trống đọc thành dấu cách, ở 168px chỉ ~9px). **KHÔNG dời 「でいい」 sang trái bịt khoảng trống**: mép phải dòng 1 nằm đè cây đèn đá, dịch dải ảnh là xé đôi cái đèn.
2. **Xoá watermark ✦ KHÔNG dùng `cv2.inpaint`** dù 2 đợt trước ghi là "mask + fill khuếch tán". Nền chỗ ✦ có KẾT CẤU (thớ gỗ 05 / vân tường 07) → TELEA trả về một ô vuông phẳng **còn hằn nguyên bóng hình sao** (nó nội suy từ viền nên tự dựng lại chữ thập). Phải **clone-stamp** vùng sạch cùng thớ.
3. **Offset clone phải để MÁY tìm, đừng chọn bằng mắt.** Chọn tay: 05 clone phải tấm ván tối vân dọc, 02 **clone luôn một con muỗi** vào giữa nền bokeh. Hàm `best_offset()` chấm điểm bằng SSD của VÀNH quanh lỗ → tự ra `05:(-72,24) · 07:(-18,-132) · 02:(42,-114)`, cả 3 liền thớ.
4. Phụ: ảnh gen ra **2752×1536 = 1,7917, KHÔNG phải 16:9** → phải center-crop 2730×1536 rồi resize 1920×1080, không thì YouTube tự bóp.

**Gate `audience-45plus.md` §1:** ký tự dòng chính ≤6 ✅ (2/4/5) · tổng ≤3 dòng ✅ · nền sáng ✅ · dấu 「秘」 góc trên–phải ✅ · badge góc dưới–TRÁI (không đụng ô thời lượng YouTube) ✅ · **≥1/3 khung ❌ cả 3 (31,6 / 21,9 / 20,6%)** — đúng ca §6.10 đang mở: cả 3 vẫn ĐỌC RÕ ở 168px **và** 120px. · **mặt người ❌ có chủ ý** (luật kênh 2026-08-05).

**3 TITLE khớp 3 ảnh (mỗi title = bản thay cho video đó, KHÔNG phải 3 bản của cùng 1 video):**

| Video | Title mới (khớp ảnh v3) | fw | keyword dẫn | claim ở đâu trong video |
|---|---|---|---|---|
| 05 | `スズメバチの巣、夏には千匹――春の数百円で作らせない昔の知恵` | 29,0 | スズメバチ @1 (đo ~71) | 千匹 @04:44 「種類によっては千匹を超える蜂」 + @10:58 |
| 07 | `すだれ数百円――熱の7割は窓から、昔の涼み方でエアコン代が下がる` | 30,5 | すだれ @1 (đo 42) | 7割 @00:13 「熱のうち、およそ7割は、窓や開口部から」 |
| 02 | `蚊が寄りつかない庭は数百円――鉢を置くだけの10の植物の知恵` | 28,0 | 蚊 @1 (đo ~109, đỉnh mùa) | 10種類 @00:29 · 数百円 @00:54 |

- Điểm keyword lấy từ `01_TREND_KEYWORDS_2026-07-22.md` + CLAUDE.md §7 (đo 2026-07-22, **14 ngày trước, cùng mùa**) — **lượt này KHÔNG đo lại**, vì keyword dẫn của cả 3 y như title đang live, cái mới chỉ là phần hook. Muốn chốt 「蜂の巣」 vs 「スズメバチ」 hoặc 「マリーゴールド」 có cầu hay không thì phải đo thêm 1 rổ.
- ⚠️ **Hai chỗ nới claim, biết mà chấp nhận:** ⓐ video nói 千匹 là 「種類によっては」, title nói thẳng 夏には千匹 ⓑ 「置くだけ」 — video dạy cả 育て方 và 配置, nên đổi thành 「鉢を置くだけ」 cho sát (ảnh vẫn là 置くだけでいい, bản v2 live cũng vậy).
- ⚠️ **Trình tự chạy (`ab-3title-3thumb.md` §1):** đang test thumbnail thì **GIỮ NGUYÊN title**. Đổi cả hai cùng lúc = 2 biến lẫn nhau, kết quả vô nghĩa.
- ⚠️ **Cỡ mẫu:** 3 video này 4 / 12 / 15 view, `BROWSE`+`SUGGESTED` = 0 → Studio 「テストして比較」 gần như không đủ impressions để ra bản thắng. Xem đây là **thay bản đóng gói**, không phải phép đo.

### 🖼️ VIDEO 01 — PROMPT **v4** (soạn 2026-08-05, user yêu cầu "nổi bật, nhìn 1 phát muốn ấn, tập trung vào chủ đề")

> Title live: `シロアリ駆除に10万円払う前に――業者が語らない500円の白い粉、90年の知恵` · videoId `fHv_oPjO1t0`.
> **Khuôn: K3 MACRO HERO** (thư viện §8 ghi đúng ca này: *"video xoay quanh MỘT nguyên liệu rẻ tiền (ホウ酸, 重曹, 酢…)"*) **lồng B1 nền sáng**.

**Vì sao đổi — đo trên bản live (2731×1536), không phải cảm giác:**

| thành phần | % diện tích khung |
|---|---|
| **bột ホウ酸 + đĩa = CHỦ THỂ của bài** | **3,62%**, dồn sát đáy khung |
| vòng ✅ xanh (không mang thông tin nào) | 2,28% — khối 487×481px |
| dấu ❌ đỏ | 1,94% |

→ Hai dấu trang trí ăn **4,2%**, chủ thể được **3,6%**. Ở 120px chỉ còn "chữ vàng + vệt gỗ nâu + ✗ + ○", **không thấy bột trắng**. Vi phạm cả 「1 điểm nhấn duy nhất」 lẫn tinh thần §2.0 media-library (hình phải hiện đúng chủ thể). Cộng: ❌/✅ đã **4/9 video** → quá trần §HẠN MỨC, video này phải nhả ra.

✅ **ĐÃ SET LÊN KÊNH 2026-08-05** — `thumbnails.set` cho `fHv_oPjO1t0` qua `youtube-jp-nenkin/tools/update_live.py --only-thumb --apply` (title/概要欄/tag **giữ nguyên**, đã xác nhận bằng dry-run + `videos.list`). File live: `06_VIDEO/_thumb_v4/01_v4_brand.jpg`. Rollback: `plan_01_thumb_backup.json`. Bản cũ (❌/✅) còn ở `07_UPLOADED/01_hosan-shiroari/_upload/thumbnail.jpg`.
- ⚠️ **PNG 2,56 MB > trần 2 MB của YouTube** → phải giao bản `.jpg` q92 (0,66 MB). Đúng ca §3 mục 4 của `ab-3title-3thumb.md`.
- ⚠️ **Dấu 「秘」 phải đặt `--pos tl`** (trên–TRÁI, lệch spec khoá): bộ gen đưa bàn tay + thìa chiếm trọn góc trên–phải, khối dấu rơi đúng lên ngón tay và cán thìa. Muốn trả về trên–phải thì gen lại với tay vào từ mé trái hoặc từ dưới.

**🔴 GATE ≥1/3 KHUÔN: RỚT — 25,3%, và tao đã đoán sai ở vòng trước.** Lượt trước tao viết "đây sẽ là bản đầu tiên đạt gate". Lập luận hình học thì đúng (`500円` 4 glyph cao 356px chỉ rộng ~1.424/1920px, thừa chỗ ngang — bản gen thật chỉ dùng **45% bề ngang**), nhưng **thiếu một biến: chiều DỌC**. Đo bản gen: dòng 1 chiếm y 232–422, badge chiếm y 808–1020 ⇒ khe cho dòng chính chỉ **386px = 35,7% khung**. Nhồi 356px vào khe 386px thì hở 15px mỗi đầu = chật cứng, xấu.
→ **Kết luận thêm cho §6.10 `audience-45plus.md`: bố cục có 2 phần tử phụ (dòng phụ TRÊN + badge DƯỚI) thì trần vật lý của dòng chính là ~30%, bất kể dòng chính mấy ký.** Muốn thật sự đạt ≥1/3 thì phải **bỏ badge hoặc bỏ dòng phụ**, không phải phóng chữ to hơn. Đây là bằng chứng thứ ba (sau video 15 `0円` 30,5% và video 08 `何十年` 24,3%) nghiêng về phương án ⓐ: hạ trần xuống ~25% khi có dòng phụ.
Gate khác: ≤6 ký ✅ (4) · ≤3 dòng ✅ · nền sáng ✅ · badge dưới–trái không đụng ô thời lượng ✅ · mặt người ❌ có chủ ý · **đọc rõ ở 168px VÀ 120px ✅** (soi `_gate_v4.png`).

**PROMPT A (chính — bake sẵn chữ, đúng luồng user đang dùng)**
> ⭐ **SỬA 2026-08-05 vòng 2 (user: "tao muốn prompt rõ cái vấn đề mối ấy").** Bản đầu đẩy gỗ-bị-mối xuống làm nền mờ ở góc → người tìm 「シロアリ」 không nhận ra bài nói về mình, mất khớp chủ đề ngay ở vòng test.
> **Cách sửa mà KHÔNG phá luật 「1 điểm nhấn duy nhất」:** đừng để bột một góc / gỗ một góc (= 2 tiêu điểm đánh nhau, đúng bệnh bản live). Gộp thành **MỘT ĐIỂM TIẾP XÚC**: bột trắng đang rơi xuống đúng chỗ gỗ bị khoét, có mối bò trên đó. Trắng-nét đè lên gỗ-thâm là chỗ tương phản cao nhất khung → mắt dính đúng đó, mà vấn đề và lời giải nằm cùng một hình. Cũng khớp nguyên tắc gác cổng ③ 「nền đậm, chủ thể sáng」.
```
Bright high-key photograph, 16:9. Sunlit Japanese room, strong morning light from a
window; pale wall and light wooden floor keep the overall frame bright and clean.

ONE SINGLE FOCAL POINT, right 55% of the frame — the moment the powder hits the damage:

  · THE PROBLEM, unmistakable and well lit: a thick old wooden beam running diagonally,
    its surface torn open into termite galleries — deep dark tunnels, honeycombed
    channels, crumbling edges, a heap of pale powdery frass spilling at its foot. This
    damage must be LARGE and instantly readable, roughly one third of the frame, in
    clear light — not hidden in shadow, not blurred away.
  · THREE OR FOUR TERMITES, macro scale, each about one eighth of the image height, pale
    cream bodies with dark heads, crawling on and around the torn wood in ONE cluster
    near the damage. Big enough to recognise at a glance. Not a swarm, not scattered
    across the frame, no dead or crushed insects.
  · THE ANSWER, the brightest and sharpest thing in the picture: from the upper right, a
    bare hand (no face, no watch, no ring, no nail polish) tips a small wooden spoon and
    a stream of fine white powder falls onto that exact damaged spot, dusting the dark
    galleries white, individual grains lit by direct sunlight, crisp macro focus.

Hierarchy: the white powder stream is the brightest and sharpest element; the ruined wood
is the darkest mass; they touch. Everything else — wall, floor, window light — is bright,
soft and out of focus.

Palette: pure white powder, dark honeycombed wood, warm sunlight, natural wood tones.
NO red prohibition mark, NO green circle, NO arrows, NO icons, no people faces,
no brand logos, no watermark. Not gory.

TEXT baked in, left side, stacked, heavy rounded Japanese gothic, thick black outline +
soft drop shadow:
  upper line, white, smaller ......  10万円払う前に
  MAIN line, bright yellow #FFD200, VERY LARGE — glyph height at least ONE THIRD of the
  image height ..................  500円
  rounded amber pill badge at the BOTTOM-LEFT, white text ......  ホウ酸 90年
Leave the TOP-RIGHT corner empty (no text, no object of interest) — a channel mark is
stamped there afterwards. Leave the BOTTOM-RIGHT corner free of text — YouTube puts its
duration badge there.
```

**PROMPT B (dự phòng — 「đường bột chắn」, kịch tính hơn nhưng rủi ro ở 120px):** như A, đổi điểm tiếp xúc thành `a straight line of fine white powder poured across a sunlit wooden threshold like a protective barrier; on the far side, three or four macro termites on the torn honeycombed wood, none of them crossing the white line`. Kể được cơ chế 防蟻バリア bằng một hình, nhưng bắt người xem đọc một mẩu truyện — ở 120px dễ thành lốm đốm. Chỉ dùng nếu A gen ra nhạt.

**PROMPT C (chỉ HƯ HẠI, KHÔNG con mối)** — như A nhưng bỏ khối TERMITES, đổi thành `no insects anywhere in the frame; the damage alone tells the story`. Dùng khi: bản A gen ra mối trông giả/nhựa (bộ gen hay dựng sai chân–râu côn trùng), hoặc thấy 気持ち悪い quá mức với tệp 45–70.
⚠️ **Đánh đổi phải cân, không có bản nào thắng sạch:** có mối = khớp chủ đề 「シロアリ」 mạnh nhất + kích cảm xúc, nhưng ⓐ bộ gen dễ vẽ sai côn trùng ⓑ một phần khán giả né hình bọ ⓒ bài học video 02: côn trùng **nhỏ + rải khắp khung** thành lốm đốm ở 120px (nên A đã khoá **3–4 con, mỗi con ~1/8 chiều cao khung, dồn 1 chùm**). Không mối = sạch mắt nhưng chỉ còn "gỗ mục", yếu tín hiệu ngách. **Gen cả A và C rồi so ở 120px mà chọn** — đây đúng chỗ nên dùng T1/T2 của bộ A/B 3×3.

**Nếu chọn đường KHÔNG bake chữ** (an toàn hơn — xem bẫy ＝ ở đợt v3): bỏ khối TEXT trong prompt, thêm `no text`, rồi
```bash
python tools\make_thumb_3dan.py 06_VIDEO\_thumb_v4\01_v4.png --photo <ảnh gen> ^
  --line1 "10万円払う前に" --line2 "500円|y" --badge "ホウ酸" --badge-sub "90年" --badge-size 84
python tools\stamp_brand.py 06_VIDEO\_thumb_v4\01_v4.png --pos tl --preview
```
🔴 **Bẫy vị trí badge:** `make_thumb_3dan.py` vẽ badge **CỨNG ở góc trên–PHẢI** (`x0 = W - bw - 40`, y=24) — **trùng đúng chỗ dấu 「秘」** của `stamp_brand.py`. Dùng `--badge` của tool thì phải stamp brand bằng `--pos tl`; muốn giữ 秘 ở trên–phải theo spec đã khoá thì để AI bake badge ở dưới–trái (đường Prompt A).

**Kiểm trước khi giao:** soi từng ký tự chữ bake (bẫy ＝) · đo `500円` có thật ≥33,3% khung · duyệt 168px + 120px · đặt cạnh `06_VIDEO/_diag_thumbs/_bench_sheet.jpg` xem có phải bản tối nhất hàng · ⚠️ chỉ 1 vật hero, thấy 2 điểm nhấn là gen lại.
**Trùng khuôn:** 02_v3 (chậu cây) cũng là "1 vật hero" — khác chủ thể, khác bối cảnh, khác hành động (tay ĐANG rắc vs chậu tĩnh), không lặp nguyên bộ. Video kế tiếp tránh **K3 + K1**.

### 🖼️ VIDEO 04 — PROMPT **v4** (soạn 2026-08-05, user: "làm rõ vấn đề diệt gián hơn")

> Title live: `ゴキブリ対策が、こんなに簡単でいいのか――薬いらずの昔の知恵３つ、最後がいちばん手軽です` · videoId `7V_mTCRb8tw`.
> Nội dung 3 mẹo: ① ハッカ油 (北見の薄荷) ② ホウ酸団子 (シルクロード) ③ 乾いた台所の習慣. Trục là **寄せ付けない**, KHÔNG phải 殺す.
> **Khuôn: B1 nền sáng + 「HƯỚNG CHUYỂN ĐỘNG」** (con vật tự bỏ chạy — thủ pháp có sẵn trong bảng thay thế §HẠN MỨC). Cố ý tránh **K3** (vừa dùng ở 01 hôm nay), **mũi tên đỏ** (vừa dùng ở 05 + 07 bản v3) và **K7** (khuôn cũ của chính 04).

**Đo bản live — vì sao phải đổi:**

| thành phần | % khung | ở 120px |
|---|---|---|
| **con gián = thứ người ta gõ tìm** | **0,92%** (180×259px), mé trái, **tối trên gạch xanh tối**, còn bị bình xịt che | còn ~**8×11px** = một vết bẩn |
| vòng ○ xanh | 1,94% | |
| dấu ✗ đỏ | 2,92% | |

→ Hai dấu trang trí ăn **4,86% = gấp 5 lần con gián**. Khung lại chia đôi nên **7 vật tranh nhau** (bình xịt · gián · lọ tinh dầu · đĩa bột · lá bạc hà · ✗ · ○) = không còn tiêu điểm nào.
⭐ **Bài học craft đắt nhất ở ca này, khác ca 01:** con gián KHÔNG nhỏ về chiều cao (16,9% khung) — nó chết vì **TỐI TRÊN NỀN TỐI**. Bóng đen thu nhỏ xuống 120px thì tan vào gạch xanh xám. Muốn con vật đọc được ở kích thước duyệt thì phải **đặt nó trên mặt SÁNG** để còn cái silhouette. Ghi vào prompt thành yêu cầu cứng.

**PROMPT A (chính — bake sẵn chữ, bố cục ĐẠT gate ≥1/3):**
```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, strong daylight; pale cream
tiles and a light stainless steel sink edge keep the frame bright and clean.

ONE SINGLE FOCAL POINT, right 55% of the frame — the moment the smell drives it back:

  · THE PROBLEM, big and unmistakable: ONE large cockroach, macro scale, its body about
    one quarter of the image height, glossy dark brown, long antennae, seen clearly from
    above at a slight angle. It is BACKING AWAY — turned away from the mist, antennae
    swept back, legs mid-scramble toward the dark gap at the edge of the frame. Exactly
    one insect. No swarm, no dead or crushed insect, not gory.
  · CRITICAL: place the cockroach on a BRIGHT pale surface — sunlit cream tile or light
    stainless steel — so its dark silhouette stays sharp and readable even when the image
    is shrunk to 120 pixels wide. Never put it on dark tile or in shadow.
  · THE ANSWER, brightest and sharpest thing in the picture: a small amber glass dropper
    bottle of peppermint oil with fresh green mint leaves beside it, and a fine cool mist
    catching the sunlight, drifting from the bottle toward the cockroach. Crisp macro
    focus, water-fresh green, droplets visible in the light.

Hierarchy: the mint mist and bottle are the brightest, sharpest, most saturated element;
the cockroach is the darkest shape and sits fully inside the light; they face each other
across a short gap. Kitchen background bright, soft, out of focus.

Palette: cool mint green, warm amber glass, pale cream tile, bright daylight.
NO red prohibition mark, NO green circle, NO arrows, NO icons, NO split-screen, no people
faces, no watermark. The bottle must have NO readable label, NO text and NO brand name.

TEXT baked in, LEFT side, heavy rounded Japanese gothic, thick black outline + soft drop
shadow — only two elements, nothing else:
  MAIN line, bright yellow #FFD200, ENORMOUS — glyph height at least 40% of the image
  height, it should feel almost too big ......  薬なし
  rounded amber pill badge at the BOTTOM-LEFT, white text ......  ハッカ油 数百円
Leave the TOP-RIGHT corner empty (no text, no hand, no object of interest) — a channel
mark is stamped there afterwards. Leave the BOTTOM-RIGHT corner free of text.
```

🔴 **VÒNG GEN 1 (2026-08-05 16:14) BỊ LOẠI — KHÔNG ĐẨY.** File `06_VIDEO/_thumb_v4b/src/04_src.jpg`. Bộ gen ra **8–9 con gián, trong đó 4 con NẰM NGỬA chổng chân** giữa khung ⇒ hình hứa *"xịt là gián chết la liệt"*, trong khi video dạy **寄せ付けない** (bạc hà làm gián KHÔNG TỚI, không diệt) và title là 薬いらず ⇒ **mismatch thumbnail↔nội dung**, `youtube-compliance.md` §4. Kèm 2 lỗi phụ: thành ĐÀN (đúng bệnh clutter vừa bỏ) và hứa 「大量発生」 — promise khác hẳn bài.
- **Vá tay không đáng:** 4 con nằm trên **gạch sáng có grout chéo** = bề mặt tệ nhất để clone, sai là thấy ngay; mỗi con còn 2 sợi râu dài vươn ra sẽ để lại sợi lơ lửng. Crop cũng không cứu: cụm gián chết nằm đúng giữa lọ tinh dầu và chữ.
- ⭐ **LỖI Ở PROMPT, không chỉ ở bộ gen.** Ràng buộc PHỦ ĐỊNH (`no dead or crushed insect`, `exactly one`) bị phớt, trong khi mấy từ MÔ TẢ của tao lại gợi đúng dáng xấu: `legs mid-scramble` + `antennae swept back` ⇒ chổng chân. **Bài học dùng lại: đừng chỉ CẤM dáng xấu — hãy MÔ TẢ DƯƠNG cái dáng muốn có** (`all six legs flat on the tile, seen from above`), và ra lệnh về SỐ LƯỢNG bằng câu kiểm được (`if more than one cockroach appears, the image is wrong`).

**PROMPT A2 (vòng 2 — bản dùng, đã siết đúng chỗ vòng 1 vỡ):**
```
Bright high-key photograph, 16:9. Sunlit Japanese kitchen, strong daylight; pale cream
tiles and a light stainless steel sink edge keep the frame bright and clean.

EXACTLY ONE COCKROACH IN THE WHOLE IMAGE. If a second cockroach appears anywhere, the
image is wrong. Every other tile surface is empty, clean and bare.

THE ONE COCKROACH — the problem, big and unmistakable:
  · macro scale, its body about one quarter of the image height, glossy dark brown, long
    antennae, photographed from slightly above.
  · IT IS ALIVE AND WALKING AWAY: standing normally on the tile with ALL SIX LEGS FLAT ON
    THE GROUND, body level, head and antennae pointing away from the mist, walking toward
    the dark gap at the edge of the frame. A healthy live insect simply leaving.
  · NEVER on its back. NEVER upside down. NEVER with legs in the air. Not curled, not
    twitching, not dead, not dying, not crushed. No insect corpses anywhere in the frame.
  · CRITICAL: it stands on a BRIGHT pale surface — sunlit cream tile or light stainless
    steel — so its dark silhouette stays sharp when the image is shrunk to 120 pixels
    wide. Never on dark tile, never in shadow.

THE ANSWER — brightest and sharpest thing in the picture: a small amber glass dropper
bottle of peppermint oil with fresh green mint leaves beside it, and a fine cool mist
catching the sunlight, drifting from the bottle across the tile toward the cockroach.
Crisp macro focus, water-fresh green, droplets visible in the light.

Hierarchy: the mint mist and bottle are the brightest, sharpest, most saturated element;
the single cockroach is the darkest shape and sits fully inside the light; they face each
other across a short gap of empty clean tile. Background bright, soft, out of focus.

Palette: cool mint green, warm amber glass, pale cream tile, bright daylight.
NO red prohibition mark, NO green circle, NO arrows, NO icons, NO split-screen, no people
faces, no watermark. The bottle must have NO readable label, NO text and NO brand name.

TEXT baked in, LEFT side, heavy rounded Japanese gothic, thick black outline + soft drop
shadow — only two elements, nothing else:
  MAIN line, bright yellow #FFD200, ENORMOUS — glyph height at least 40% of the image
  height, it should feel almost too big ......  薬なし
  rounded amber pill badge at the BOTTOM-LEFT, white text ......  ハッカ油 数百円
Leave the TOP-RIGHT corner empty (no text, no hand, no object of interest) — a channel
mark is stamped there afterwards. Leave the BOTTOM-RIGHT corner free of text.
```
> ⓘ Vòng 1 làm đúng được 3 thứ, giữ lại: chữ `薬なし` + badge `ハッカ油 数百円` không lỗi glyph · lọ tinh dầu **không có nhãn** (sạch vụ nhãn hiệu cũ) · luồng sương bạc hà xanh nhìn ra ngay là "mùi".

**PROMPT B (giữ dòng phụ 「ゴキブリが出ない家」)** — như A, thêm dòng phụ trắng nhỏ phía trên và hạ dòng chính xuống `at least one third of the image height`. Dùng nếu muốn chữ ゴキブリ có mặt trên thumbnail cho khớp truy vấn. **Đánh đổi đo được: thêm dòng phụ là trần dòng chính tụt về ~28–30%** (ca video 01 v4: dòng phụ + badge ⇒ khe dọc chỉ còn 35,7% khung).

**Vì sao A bỏ dòng 「ゴキブリが出ない家」:** ⓐ chính nó là thứ chặn gate ≥1/3 — bỏ đi thì `薬なし` (3 glyph) phóng được tới ~40% ⓑ tín hiệu ゴキブリ giờ do **con gián to trong hình** gánh, mạnh hơn chữ ⓒ title đang live đã có `ゴキブリ対策` ở 5 chữ đầu. Nếu bấm A thì đây là **thumbnail co-dai đầu tiên thật sự đạt gate ≥1/3** — nhưng lần này đừng tin lời hứa, **đo bằng máy sau khi gen** (bài học 01 v4: tao đoán đạt, gen ra 25,3%).

⚠️ **Nhắc riêng cho 04:** bản trước của video này từng **vi phạm nhãn hiệu vì bình xịt in tên** (sổ `08_ANALYTICS_LOG.md` §3). Prompt A đã chặn thẳng `NO readable label, NO text, NO brand name` — kiểm lại bằng mắt trên lọ tinh dầu trước khi giao.

## PROMPT ĐÃ ĐIỀN CHO 3 VIDEO HIỆN CÓ (bản no-text, đè chữ 3dan bằng PIL)

### 01 — ホウ酸 chống mối (K1)
```
LEFT: a swarm of termites crawling on damaged wood beam, slightly dimmed. A thick glossy red curved arrow sweeps from left to right. RIGHT (larger, brighter, hero): a hand holding an open blue box of white boric acid powder, crisp macro, powder texture visible.
+ [KHỐI BRAND]
```

### 02 — 10 cây đuổi muỗi (K2)
```
LEFT: a highly detailed mosquito in flight, wings spread, slightly dimmed. CENTER: a large glossy red prohibition circle with X sign, 3D style. RIGHT: a hand holding a fresh branch of beautyberry with clusters of small purple berries and green leaves, vivid and bright.
+ [KHỐI BRAND]
```

### 03 — 夏の雑草 (K2 — đã dựng bản ghép; prompt AI dự phòng nếu muốn gen lại nền)
```
LEFT: a hand pulling a green weed out of dry cracked soil, roots exposed, dozens of tiny pale seeds scattering down, slightly dimmed. CENTER: a large glossy red prohibition circle with X sign, 3D style. RIGHT: a hand holding a small Japanese hand sickle (nejiri-gama) together with a white spray bottle, crisp macro, brighter than left.
+ [KHỐI BRAND]
```

## COMPLIANCE & 3 CỬA (nhắc nhanh)
- Quét từ cấm nhóm 殺/血/死 ở text đè (luật gốc `.claude/rules/youtube-compliance.md`); 一掃/追い出す/駆除 OK.
- 3 nguyên tắc gác cổng hình: ① 1 điểm nhấn ② phóng đại cảm giác ③ 120px vẫn rõ (nền đậm chủ thể sáng).
- Hình không được spoil đáp án nếu video úp mở ranking.
- Thumbnail AI = production assistance → KHÔNG cần tick disclosure; cấm mặt người thật cụ thể.
| **29_hocho-togi-mennaoshi** | **B1 (bright) lồng K3 (macro hero)** + chữ bake trong prompt + badge 「直しは30秒」 · bộ 3 A/B | CHỐT 2026-09-04. Tránh **K6** (#28) + **K7** (#27) đúng chỉ thị. **K3 lần cuối lên sóng ở #23, cách 5 video** ✅. Chọn K3 vì cú lật của bài nằm TRONG CHÍNH CÁI VẬT (mặt đá lõm) — một khung macro thuyết phục hơn mũi tên hay ❌/✅ (và ❌/✅ đang bị hạn mức §⚖️). Chữ đọc liền một mạch: `包丁が切れない` → **`砥石のへこみ`** (HERO 6 ký, rộng ~2/3 khung) → `研ぐほど鈍る` + badge `直しは30秒`. **T1** đá mài + thước thép + KHE SÁNG lọt ở giữa · **T2** đổi ĐÚNG 1 biến hình = nhìn từ trên, lưới bút chì đã mài 10 giây, **dải giữa còn nguyên** (đưa phép chẩn đoán của cold open vào khung), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / ảnh nửa phải (dao gác ngang bắc qua chỗ lõm, khe sáng lọt dưới lưỡi), chữ y nguyên. 🚫 không mặt người, không cả bàn tay ở bộ này. Đo máy: **TEXT @7% (trần 15%) · 1.297–1.395 ký (trần 1.500)** ✅. Prompt: `06_VIDEO/29_hocho-togi-mennaoshi/thumb_prompts_{FLOW.txt,BLOCKS.md,TENFILE.txt,PLATE.txt}` (PLATE no-text **file riêng**). ✅ **XONG 2026-09-06** — user gen 3 bản, đã vá ✦ + đóng dấu 「秘」 (`stamp_brand.py --pos tr`) + gói upload (hẹn 2026-09-09 13:00 JST). File chốt: `06_VIDEO/29_hocho-togi-mennaoshi/thumb_T{1,2,3}_*.jpg|.png`; bản gốc còn ✦ giữ ở `_thumb/_wm_orig/`, bản đã vá chưa đóng dấu ở `_thumb/_wm_clean/`. 🔴 **✦ của lô này vẽ bằng NÉT TỐI** nên `strip_wm_thumb.py` (trung vị hàng) vá ra **khối chữ nhật xám** — phải dùng tool mới `tools/strip_wm_star.py` (phép ĐÓNG/MỞ, cái gì dày hơn kernel thì trả nguyên giá trị cũ); bài học đã ghi vào `.claude/rules/media-library.md` §2.10 mục 6c. Đo máy: dòng hero `砥石のへこみ` cao **T1 15,4% · T2 21,9% · T3 16,1%** khung ⇒ **KHÔNG bản nào đạt gate ≥1/3 của `audience-45plus.md` §1** (ca đo thứ 6 của bệnh khuôn 3 tầng, sau video 16 = 24,5%); chữ do AI bake nên không phóng lại được — muốn đạt gate phải gen bản PLATE không chữ rồi đè chữ bằng PIL. Chữ bake soi từng ký tự: 4/4 khối đúng, không dính bẫy ＝. Video kế tiếp tránh **K3 + K6** |
| **30_futon-dani-uchinaoshi** | **B1 (bright) lồng K2 (X-diagram)** + chữ bake trong prompt + badge 「費用0円」 · bộ 3 A/B | CHỐT 2026-09-09. Tránh **K3** (#29) + **K6** (#28) đúng chỉ thị. **K2 lần cuối lên sóng ở #21, cách 6 video** ✅ (❌/✅ chưa chạm trần §⚖️). K2 dịch đúng cú lật trung tâm: phơi chăn ngày nắng to hóa ra là **ngày ẩm nhất** — đông 51% ↔ hè 74%. Chữ đọc liền một mạch: `布団のダニ` → **`干す日が逆`** (HERO 5 ký) → `正解は1月` + badge `費用0円`. **T1** hè dimmed + vòng cấm đỏ X ↔ đông sáng nét sương giá · **T2** đổi ĐÚNG 1 biến hình = **đập chăn**, bụi nổ ra, vòng cấm đỏ đè lên gậy tre (cái sai thứ hai của bài), chữ y nguyên · **T3** đổi layout = panel chữ nửa trái / ảnh hiên gỗ nửa phải, chữ y nguyên. 🚫 không mặt người — T2 có **một bàn tay + cẳng tay** (được phép). ⭐ **Phát hiện đáng ghi (Bước 1 của `ab-3title-3thumb.md` §3.1):** bản #21 sổ ghi K2 nhưng **ảnh đã lên sóng KHÔNG phải trái/X/phải** — nó sập về **chữ nửa trái + ảnh nửa phải**. Khi đã bắt bake chữ, generator luôn trả hình học đó ⇒ bộ prompt này giữ hình học đã chứng minh và **đưa nghĩa K2 vào BÊN TRONG tấm ảnh** (lớp sau dimmed + vòng cấm, lớp trước sáng nét), thay vì đánh nhau với generator. Đo máy: **TEXT @6–7% (trần 15%) · 1.295–1.491 ký (trần 1.500)** ✅. Prompt: `06_VIDEO/30_futon-dani-uchinaoshi/thumb_prompts_{FLOW.txt,BLOCKS.md,TENFILE.txt,PLATE.txt}` (PLATE no-text **file riêng**). ⛔ Bộ prompt `No text` cũ trong script §3 **đã huỷ** (vi phạm luật bake chữ 2026-08-10). 📌 Bản K7 「con mạt phóng đại」 **bỏ**: trộn 2 biến + sinh vật AI hay ra 6/10 chân. ✅ **T2 XONG 2026-09-09** — `thumb_T2_futontataki-hokori.png` (1,76 MB, dưới trần 2 MB; gốc còn ✦ ở `_thumb/_wm_orig/_raw_T2_futontataki.jpeg`, bản đã cắt chưa đóng dấu ở `_thumb/_wm_clean/`). Chữ bake **đúng cả 4 khối, 0 ký tự nát** (soi `逆`/`費`/`解` cạnh glyph YuGothB). 🔴 **✦ ở lô 2752×1536 này chỉ có MỘT dấu, tại (2630,1422) = 0,956W · 0,926H** — khớp hằng số thứ nhất của lô ở `media-library.md` §2.10 ⑤ mục 5, **nhưng dấu thứ hai (0,930W · 0,890H) KHÔNG có**; xác định bằng MẮT rồi template-match toàn ảnh xác nhận (peak 0,997 rồi tụt xuống ≤0,45). 🔴 **VÁ THẤT BẠI, phải CẮT** — `cv2.inpaint` NS r=27 + ghép vân kéo trời sáng vào dải ria futon, ra **vệt sáng tệ hơn cả ✦** (✦ nằm đúng trên biên chất liệu tan↔trời). Cắt được vì **chữ dừng ở 0,73W**, cách ✦ tới 22% bề ngang ⇒ đi nhánh CẮT của §2.10 ⑤b: cắt phải tại **2596 (0,943W)** + trim 76px chiều cao (38 trên / 38 dưới) về 2596×1460 = 16:9 → resize 1920×1080. Lề còn: trên 3,4% · dưới 2,6% (badge). Ô timestamp dưới-phải **0,0% mực**. Đo máy: hero `干す日が逆` cao **18,9%** khung, rộng **58,8%** ⇒ **KHÔNG đạt gate ≥1/3** của `audience-45plus.md` §1 (ca đo thứ 7 của bệnh khuôn 3 tầng ở kênh này); đọc rõ ở **168px và 120px**, ở 120px hero là thứ đọc được đầu tiên. ⚠️ **T1 + T3 CHƯA GEN → gate 3×3 vẫn hở 1/3**, và Studio *Test & compare* **không chạy được với 1 ảnh**. 📌 **目次 đã dựng lại từ `subs.srt` thật** — bản viết trước render lệch tới **30s** (đúng bài học #29), và 概要欄 trước đó **thiếu hẳn 目次** vì parser `upload_pack.py` chỉ đọc khối 「mô tả đầy đủ」 ⇒ đã nhét 【目次】 vào đầu khối đó. Video kế tiếp tránh **K2 + K3** |
