# 01_EPISODE_IDEAS — 12 tập đầu + shot list tập 1

> Kênh `youtube-jp-retrofuture` — **riêng hoàn toàn**, không dính `youtube-jp-showa`.
> Luật thế giới: `00_WORLD_BIBLE.md`. Bộ prompt: `04_VIDEOGEN_STYLE_S100.md`.

## 0. KHUÔN MỘT TẬP (4–6 phút, ~40–55 clip)

```
① khung mở — NHÌN LÊN / NHÌN RA (nhận diện thế giới ngay giây 0: thân long não khổng lồ có nhà gỗ chồng tầng, cầu ván dây, viaduct xếp lớp tan vào sương)
② một việc thường ngày bắt đầu
③ 3–4 nhịp — mỗi nhịp 1 bối cảnh, xen 1 cảnh thở không người
④ MỘT KHOẢNH KHẮC NHỎ (không cần plot: một cái vẫy tay, một cái đợi, một cái hỏng)
⑤ khung đóng — MOTIF: robot NHÌN THẲNG vào mày rồi đèn mắt mờ dần trong phòng đã tối
```

⭐ **Luật phủ mỗi cảnh** (`04_VIDEOGEN_STYLE_S100.md` §6.9): cảnh NGOẠI phải thấy **≥2 TẦNG**; mọi vật
phải có **địa chỉ trong khung** (tiền cảnh / giữa / lùi vào bóng / xa trong sương).
🔴 **KHÔNG còn luật "1 vật viễn tưởng ⇄ 1 vật đời thường"** — nó kéo nửa khung về lại 1975. Thay bằng:
**mọi vật đều có phiên bản 昭和100年 của chính nó**, và thứ giữ nó khỏi cyberpunk là **bảng màu + chất
liệu cũ kỹ + hành vi việc nhà**, không phải vật tầm thường.

## 1. MƯỜI HAI TẬP ĐẦU

| # | Tập | Khoảnh khắc (④) | Vật viễn tưởng chủ đạo |
|---|---|---|---|
| **01** ⭐ | **雲の上の一日** — buổi sáng ở thị trấn trên biển mây | bố vẫy tay, robot giơ tay đáp và **giữ lâu hơn cần thiết** | nhà gỗ ôm thân long não · tàu lơ lửng · nồi cơm cầu thép |
| 02 | **商店街のお使い** — đi chợ | robot xách quá nhiều, một quả cà chua lăn ra; bà hàng rau nhặt giúp mà không nhìn nó | arcade Showa chồng tầng · biển men 鮮魚・食堂 · xe ba bánh đệm khí |
| **03** ⭐ | **銭湯の外で** — đợi ngoài nhà tắm công cộng | robot **không vào được**, đợi dưới đèn lồng; hơi nước tràn ra cửa mỗi lần có người bước ra | noren ゆ · nồi hơi đồng khổng lồ · đèn lồng giấy |
| 04 | **給食当番** — trực bữa trưa ở trường | robot múc canh, tay run một nhịp, đèn mắt nháy | khay nhôm hâm nhiệt · trường gỗ trên cây · bảng từ quay tay |
| 05 | **台風の夜** — đêm bão | mất điện; **đèn mắt robot là nguồn sáng duy nhất** trong nhà | cây quật trong gió · cửa sổ gỗ bịt ván · đèn lồng tắt ngấm |
| 06 | **雲の上の夏** — mùa hè trên cây | dưa hấu, quạt, ve sầu; robot cầm ô che cho bé gái | ống làm mát đồng dọc thân cây · quạt 3 cánh lồng sắt |
| 07 | **運動会** — hội thao | robot chạy tiếp sức, **bánh xe trượt trên cát**, về chót, không ai cười nó | loa phễu đồng trên cột · dây cờ giăng giữa hai cây |
| 08 | **洗濯物と夕立** — mưa rào bất chợt | robot lao ra thu quần áo; tấm cuối cùng ướt sũng | máy giặt 2 lồng cửa tròn · monorail trong mưa |
| 09 | **デパートの屋上** — sân thượng bách hoá | đu quay; robot đứng dưới cầm bóng bay đợi | đu quay cơ khí · mái tôn gỉ · viaduct chạy sát bên |
| 10 | **大晦日** — đêm giao thừa | cả nhà ngủ gật trước TV; robot tắt TV, kéo chăn | TV gỗ màn cong · videophone quay số |
| 11 | **引っ越しの日** — ngày chuyển nhà | phòng trống; robot đứng giữa những vệt sáng trên tatami | xe tải đệm khí · ròng rọc hạ đồ xuống từ cành |
| **12** ⭐ | **修理の日** — ngày robot được sửa | thợ mở nắp ngực; **đèn mắt tắt hẳn 3 giây rồi sáng lại** | xưởng sửa cơ khí · ống khí nén · bàn nguội |

⭐ = tập cảm xúc mạnh, dành cho mốc quan trọng. **Đăng 01 trước** (giới thiệu trọn thế giới + gia đình + robot).

## 2. TẬP 01 「雲の上の一日」 — 40 CẢNH, 5:20

> 🔧 **KHÔNG sửa file prompt bằng tay.** Sinh bằng tool:
> ```
> python tools/gen_prompts_ep01.py
> ```
> → `videogen_ep01_FLOW.txt` (40 prompt, 1 dòng/prompt) + `videogen_ep01_TENFILE.txt` + **gate tự chạy**.
> 🔴 Đổi bất kỳ luật nào (trời · đám đông · cast · tốc độ máy · vật liệu) thì **sửa KHỐI trong tool**,
> cả 40 prompt cập nhật theo. Sửa tay từng prompt là sửa triệu chứng (`ai-video-regen.md` §0).

**Cấu trúc: một ngày, bốn khối 10 cảnh.**

| khối | cảnh | mạch |
|---|---|---|
| 🌅 **SÁNG** 01–10 | bình minh trên biển mây → mở cửa tiệm → mẹ mở cửa sổ → ăn sáng → bé đi học qua cầu → ga 雲上駅 → tàu vượt cầu thép → chợ mở hàng → đèn lồng tàn → mẹ quét cửa |
| ☀️ **TRƯA** 11–20 | chợ đông → **cà chua 180円** → quán mì → giờ cơm trưa → thợ siết cáp cầu → trẻ chơi bi → **mây dâng ngập phố** → phơi chăn trên vực → hiệu sách 森書房 → tiệm điện くすのき電器 |
| 🌇 **CHIỀU** 21–30 | nắng xiên → bé về → mẹ đón ở cửa → 松風湯 bốc khói → chén trà trên lan can → tàu chiều → người về nhà → thắp đèn lồng → hoàng hôn biển mây → cả thị trấn lên đèn |
| 🌙 **TỐI** 31–40 | cơm tối → bố về → TV nhiễu → bé ngủ → mẹ rửa bát → phố đêm → đom đóm trên vách → **mẹ ở lan can với đèn dầu** → toàn cảnh đêm → ô cửa cuối cùng tắt |

**Số đo bộ prompt (tool tự in):**
- 40 cảnh × 8s = **5:20** — đúng dải 4–6′
- prompt 6.409–8.126 ký, TB **7.232**
- **float: breath 31 / step 9 = 78% cảnh máy gần như đứng yên** (luật đòi ≥40% — `04…S100.md` §8)
- **đám đông: none 19 · few 10 · some 7 · busy 4** — chỉ 4 cảnh thật đông, đủ cảm giác tấp nập mà không
  rải mặt phụ khắp bài (§5.3)
- **cast khoá: mẹ 8 · bé gái 7 · bố 1** — bố chỉ một cảnh (về muộn), đúng vai
- trời: dawn 2 · day 17 · window 4 · dusk 7 · night 10

⚠️ **Ba cảnh dễ vỡ nhất, gen trước rồi hãy bơm cả lô:**
**12_tomato** (cận bé gái + chữ トマト180円) · **06_eki** (đám đông + biển 雲上駅) ·
**39_machi_yoru** (toàn cảnh đêm — dễ bệt).

## 3. NGHIỆM THU BỘ DEMO — làm đúng thứ tự này

1. Bơm 8 prompt → gen → tải về.
2. **Soi 4 mốc/clip (0,3 / 2,6 / 5,2 / 7,6s) ở CỠ THẬT.** ⛔ Sheet thu nhỏ cho qua chữ giả và tay hỏng.
3. Thang nhận/loại: `04_VIDEOGEN_STYLE_S100.md` §11, và đo màu theo mốc §0.1 (contrast 48–54 · R−B +18…+26 · bão hoà 33–40%). **Ghi ra sổ mọi thứ cố ý NHẬN.**
4. Gate máy: `% khung đứng yên ≤10%` · `MAD blur trong shot ≥8,2` (`camera-language.md` §8.1).
5. **Bốn câu hỏi quyết định kênh sống hay chết** — trả lời bằng mắt trên 8 clip:
   - ⭐⭐ Có trông như **ẢNH CHỤP THẬT** không, hay vẫn ra anime/tranh vẽ? (đây là câu hỏi số 1 — v1 đã rớt đúng chỗ này)
   - ⭐ Nhìn 3 giây có biết ngay **đây không phải Nhật thật** không? (nếu không → §6 chưa đủ đậm)
   - Biển hiệu chữ Nhật có **đúng nét từng ký tự** không? (sai một nét = loại clip, §3)
   - Robot có **giữ đúng một danh tính** qua cả 8 clip không?
   - Có ai **phản ứng với robot** không? (có = hỏng quy tắc 5)
   - Xem **không tiếng** có còn muốn xem tiếp không?
6. 🔴 **Prompt trượt 2 lần liên tiếp = lỗi ở PROMPT, không ở lượt gen.**

## 4. VIỆC CÒN MỞ TRƯỚC KHI LẬP KÊNH
- [ ] Gen + nghiệm thu 8 clip demo (§3)
- [ ] **Thử nhạc** — rủi ro lớn nhất, không-lời mà nhạc dở thì không cứu được (`00_WORLD_BIBLE.md` §7)
- [ ] Chốt tên robot + tên kênh (`00_WORLD_BIBLE.md` §3, §12)
- [ ] Chỉ khi demo đạt: lập kênh + Gmail + Chrome profile (`channel-browser.md`) + slot lịch (`upload-schedule.md`)
