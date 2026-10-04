# 08_ANALYTICS_LOG — sổ đo tuần kênh nenkin

> Ritual **sáng Thứ Hai hằng tuần (~15 phút, giờ VN, trước slot 17:00)**:
> 1. `python E:\Claude\Projects\youtube-jp-chouhen\tools\analytics_report.py --channel nenkin`
> 2. `... --video <slug|id>` cho từng video đã đăng ≥3 ngày (impressions trễ 2–3 ngày — video mới trống là bình thường)
> 3. Lưu snapshot: `... --channel nenkin > E:\Claude\Projects\yt-dashboard\history\nenkin\YYYYMMDD-HHMMSS_kenh.txt` (hoặc nút Analytics trên dashboard)
> 4. Ghi 1 block vào file này: ngày · per-video impr/CTR/AVD/nguồn · **chẩn bệnh 1/2/3 · hành động đã quyết**
> 5. Phụ: check 🔥 72h sau mỗi video mới (không cần đủ ritual)

## BẢNG NGƯỠNG → HÀNH ĐỘNG (khung 3 bệnh — dán đây để khỏi quên)

| Triệu chứng | Bệnh | Hành động |
|---|---|---|
| Impressions ≈ 0 khi đã ≥5 video live + tầng kênh đầy + 14 ngày | **1 — volume/tầng kênh** | ~~giữ nhịp 3/tuần~~ 🔴 **SỬA 2026-07-28:** cat 27 + desc/keywords đã verify sạch → **KHÔNG đổ thêm volume** (đã thử 3,5/tuần, vẫn 0 browse). Việc đúng: **1 video/tuần T6 + nâng độ dài lên chuẩn ngách 25–40′ + title 【】**, bám 支給日 (kế: **14/08** → đăng T3 11/08). Bằng chứng: `CHANNEL_DIAGNOSIS_2026-07-28.md` |
| Impr ≥500–1.000/video nhưng CTR <3% trong 7 ngày | **2 — packaging/rổ metadata** | Swap thumbnail variant B (`thumbnails.set`); rà title khung 大損/末路; rà rổ 12 tag + 3 hashtag. CTR 4–6% = tắt báo động. **CẤM swap khi impr <500** (noise) |
| CTR ≥4% nhưng intro-30s <70% hoặc vực phút 0–2 | **3 — script** | Siết cold open script kế (case+số trước phút 2); chạy lại Retention Audit; đối chiếu lời hứa thumbnail ↔ 70 ký đầu |
| Traffic toàn Search, Browse ~0 sau 1 tháng | 1 kéo dài | Bình thường ở cold-start (Browse ≈57% chỉ đến khi kênh có identity) — giữ nhịp đều + badge/ritual nhất quán |
| Comment hỏi case xuất hiện | tín hiệu TỐT | Kích hoạt tuyến 「視聴者の実験室」 |

**Kỳ vọng đúng (chống bẫy tâm lý):** benchmark 長生きの秘訣 flop 30 video/2 tháng trước khi khóa rổ; hit rate ngách ~1/5. **KHÔNG pivot trước mốc 15–20 video.** Checkpoint đọc data lớn đầu tiên: sau video ~15 (~cuối tháng 8).

---

## 📊 THEO DÕI YPP (thêm 2026-08-31 — mỗi lần đọc số ghi thêm 2 dòng này)

> Ngưỡng: **1.000 sub + 4.000 giờ công khai** (cửa sổ 12 tháng trượt). Số học đường đi (đo 08-31):
> 4.000h ≈ 62K view ở AVD 3:50 (85K ở AVD hiện tại) · 1.000 sub ≈ 150K view ở conversion 0,67%
> của kênh chuẩn (mình 0,22%). Kênh mới cùng cỡ trúng nhánh thì 1.000 sub trong 7–11 ngày
> (カメ先生 154 sub/ngày · 定年前後 93 · 保健室 89).

| ngày đo | giờ xem 12 tháng / 4.000 | sub / 1.000 | conversion (sub/view đời) |
|---|---|---|---|
| 2026-08-31 (số 08-29) | **~87h = 2,2%** | **6 = 0,6%** | 0,22% |

---

## 2026-09-15 (T3) — 🔬 KHÁM LẠI + THI HÀNH TRỤC PHÂN PHỐI · **AVP TỤT THEO VIEW** · nút thắt YPP là SUB

Baseline: `06_VIDEO/_diag/curves_2026-09-15.{txt,json}`.
Kênh **10.685 view · 7 sub · 24 video** (08-29: 2.705 → 09-10: 9.144 → nay 10.685).

### A. 🔴 AVP TỤT KHI VIDEO HÚT THÊM VIEW — mọi so sánh trước/sau phải khớp theo SỐ VIEW

| video | đọc 09-10 | đọc 09-15 |
|---|---|---|
| `jhRgcIiqd_w` 遺族年金 | **23,6% @ 102 view** | **16,4% @ 569 view** |
| `tsQwDqqreCM` 雇用継続 | 9,7% @ 777 | 11,5% @ 787 |

Cùng video, cùng chữ, cùng hình — AVP rơi **7 điểm** chỉ vì view mới toàn là feed lạnh. Nhìn
cả bảng: 37 view → 27,5% · 68 → 24,4% · 80 → 24,1% · **4.921 → 15,1%**.
⇒ **"Retention dưới 20%" phần lớn là HỆ QUẢ của việc được feed lạnh đẩy**, không phải bệnh
của kịch bản. ⛔ Từ nay **cấm so AVP trọn đời giữa hai video khác cỡ view**; A/B phải đọc
curve lúc video **chạm 500 view**, video không bao giờ đạt 500 thì **loại khỏi mẫu**.

### B. 🔴 NÚT THẮT CỦA YPP LÀ **SUB**, KHÔNG PHẢI GIỜ XEM

- 4.000 giờ ở AVD 2:20 ≈ **103.000 view**; ở AVD 3:50 ≈ **62.600 view**.
- 1.000 sub ở tỉ lệ **hiện tại 0,065%** ≈ **1,54 TRIỆU view**; ở mức thường 0,67% ≈ **150.000**.
- Tỉ lệ đổi sub **tệ đi 3,4×** (08-29: 6/2.705 = 0,22% → nay 7/10.685 = 0,065%). **8.000 view
  gần nhất đẻ ra đúng 1 sub.**
⇒ Sub và retention **cùng một gốc**: feed lạnh đưa sai người tới. Ưu tiên số 1 là tỉ lệ đổi sub.

### C. ĐÃ THI HÀNH (API) — `tools/apply_distribution_20260916.py`

| việc | kết quả |
|---|---|
| Gán lại playlist trụ | A 6→**9** · B 6→**9** · C 11→**6** (mọi video gần đây bị dồn sai vào trụ 手取り: 緑の封筒 đáng ra trụ B, 60歳繰上げ đáng ra trụ A) |
| Khối `▼関連する研究ノート` + 3 hashtag chuẩn | **24/24** video · link có `&list=` để autoplay kế tiếp cũng nằm trong ngách |
| Bình luận ghim (nội dung) | 8/8 đã đăng (7 có sẵn, `KmmbwuRHBAg` viết mới từ chính lời đọc) |
| Phụ đề `ja` | **0/24 thiếu** |

### D. 🔴🔴 BẪY IM LẶNG: `channels.update` KHÔNG GHI ĐƯỢC `keywords`

Gọi `channels().update(part="brandingSettings")` → **HTTP 200 và response echo ĐÚNG giá trị
mới**, nhưng `channels().list` đọc lại ngay sau đó vẫn ra **giá trị CŨ**. YouTube nuốt lệnh,
không một dòng lỗi. **Tin response là ghi vào sổ "đã xong" trong khi không có gì đổi.**
⇒ Cùng họ `media-library.md` §2.10 ⑤ (*số đo và exit code không chứng minh đã ghi*) — phép
nghiệm thu đúng là **đọc lại từ nguồn**, không phải đọc response.
⇒ Keywords chuyển sang việc TAY: `_MANUAL_STUDIO_20260916.md` mục 1.

### E. CÒN LẠI PHẢI BẤM TAY (~25′) → `_MANUAL_STUDIO_20260916.md`
keywords · ghim 8 bình luận · **thẻ @1:30–2:00 ×6** · **end screen ×7** (bắt buộc có phần tử
ĐĂNG KÝ + video CỤ THỂ, cấm để 「視聴者に最適な動画」).
⚖️ Thẻ được ưu tiên hơn end screen: ở AVP 15% trên video 14′, người xem trung bình rời ở
**~2:06**, rất ít ai tới được end screen.

### F. MỐC ĐỌC 2026-10-15 — ĐỨNG YÊN, không đổi thêm biến phân phối nào

| | metric | baseline 09-15 | ngưỡng |
|---|---|---|---|
| **M0** ⭐ | sub/view biên (cửa sổ 14 ngày) | **0,0125%** | ≥0,3% ăn · <0,1% sai người xem |
| M1 | (RELATED+END_SCREEN+PLAYLIST+YT_CHANNEL)÷view | ~2,4% | ≥6% ăn · 3–6% mơ hồ · <3% bỏ |
| M2 | RELATED cùng ngách /25 | **8/25** | ≥12 tiếp · ≤8 trục này cạn |
| M3 | AVP **tách theo nguồn**, cùng video, cửa sổ vs cửa sổ | browse 15,4 / RELATED 26,7 | ⛔ không bao giờ so AVP gộp |

🛑 Phanh: M0 <0,1% **và** M2 ≤8/25 → cả trục phân phối lẫn trục lời mời đều không ăn ⇒ việc
còn lại là chọn đề tài theo hàng xóm, và phải nói thẳng YPP là bài toán nhiều tháng.

---

## 2026-09-10 (T5) — 🔬 ĐỌC SỐ (trễ 5 ngày so mốc 09-05) · **4 GIẢ THUYẾT BỊ BÁC** · biến trội = CHẤT LƯỢNG TRAFFIC

Số tươi: `06_VIDEO/_diag/curves_2026-09-10.{txt,json}` (tool **viết lại** — bản cũ `pull_curves.py`
nằm trong `06_VIDEO/_diagnose/` nên đã bị `upload_pack --done` dọn mất; nay đặt ở **`tools/pull_curves.py`**.
⇒ Bài học: tool KHÔNG BAO GIỜ để trong `06_VIDEO/`).
Kênh: **9.144 view** (08-29: 2.705) · sub **7** · 13 video ≥15 view có curve.

### A. Vách 10→30s: có ở **13/13** video, −21…−64 điểm, KHÔNG DỊCH sau 4 lượt sửa

| video | ngày | view | AVP | drop 10→30s | ghi chú biến đã thử |
|---|---|---|---|---|---|
| v12 | 08-16 | 1.461 | 16,0% | −31 | khuôn cũ |
| v15 | 08-23 | **3.713** | 15,2% | −39 | あなた@0:03 + stake@0:03 |
| v18 | 08-30 | 713 | 15,2% | **−51** | cold open v3 + Remotion |
| v24 | 09-01 | 977 | 15,3% | −34 | hook "nỗi sợ" @0:00 |
| v19 | 09-03 | 777 | **9,7%** | −39 | モニター @3:10 (phép đo モニター sạch) |
| ~~v21~~ → **v20** | 09-06 | 102 | 23,6% | −35 | ~~2 giọng hỏi–đáp~~ → **1 giọng** (🔴 xem dưới) |

🔴 **SỬA GÁN NHẦM VIDEO (bắt 2026-09-15).** Dòng trên vốn ghi *"v21 · 2 giọng hỏi–đáp (18 dòng
`[聞]`)"*, và con số 23,6% đã được trích đi nhiều chỗ làm bằng chứng cho khuôn 2 giọng — kể cả
header script 25. Nhưng `jhRgcIiqd_w` (video ăn 23,6%) là **video 20 遺族年金, `_TTS.md` có
ĐÚNG 0 dòng `[聞]`**. Video 21 (2 giọng thật, `T69O1_ejplE`) lên sóng **09-10**, tức **đúng
ngày đọc số này nó chưa có dữ liệu nào**.
⇒ **Khuôn 2 giọng CHƯA TỪNG được đo.** Số đầu tiên của nó là 2026-09-15: **AVP 19,9% @ 134
view** — và với confound "AVP tụt theo view" (mục 09-15 bên dưới) thì 134 view chưa nói được gì.
📌 Bài học: bảng này neo theo **số thư mục**, mà số thư mục **không phải thứ tự đăng**
(v24 đăng 09-01, trước v19 ngày 09-03). Mọi dòng phải neo bằng **videoId**.

⭐ **Hệ quả đã chốt 2026-09-16 (user):** vì khuôn 2 giọng chưa từng có số, **MỘT GIỌNG
trở thành mặc định của kênh** (`CLAUDE.md` §②). Đã cài gate **G12 khuôn 2 GIỌNG** trong
`check_pace.py`: có dòng `[聞]` mà không khai `--2voice` thì báo đỏ. Muốn thử 2 giọng thì
phải là A/B có chủ định, không để nó trôi vào vì người viết thấy hay.

⇒ **BÁC 4 giả thuyết** (mỗi cái từng là "lời giải" của một lượt trước):
1. ❌ **chữ cold open** — 3 khuôn mở khác hẳn nhau, drop y nguyên.
2. ❌ **lớp hình** — v18+ đã Remotion, hình khác hẳn `make_stage`; v19 gate nhịp hình SẠCH 3/3 mà AVP browse **9,2%** (tệ nhất kênh). Đây đúng là phép thử mà `CHANNEL_DIAGNOSIS_2026-08-29` §3.2 mục 2 đã định trước ⇒ hình bị loại.
3. ❌ **モニター trong 0–120s** — v19 dời 松本 ra 3:10 (G9 sạch) mà vẫn tệ nhất.
4. ❌ **"nói loãng, nạp thông tin chậm"** (§3.2 mục 3) — đo transcript 2 hit hàng xóm (`カメ先生 B09fiNc4fcw` · `定年前後 65pB-DvLXpU`): họ **144–153 ký/30s**, mình **141–196**. Mình DÀY HƠN.

### B. ⭐ BIẾN TRỘI ĐO ĐƯỢC: **cùng một video, retention theo NGUỒN chênh 2,3–2,6×**

| nguồn | view | AVD | AVP |
|---|---|---|---|
| `SUBSCRIBER` = **what-to-watch** (home feed) | **7.943 (94,7%)** | 2:21 | **15,4%** |
| `RELATED_VIDEO` | 186 (2,2%) | 4:03 | **26,7%** |
| `YT_SEARCH` | 149 | 3:32 | 16,7% |

Từng video, browse vs RELATED: v12 **15,6% vs 40,5%** · v15 14,8% vs 34,9% · v18 14,4% vs 23,0%.
`subscribedStatus`: **8.387 UNSUBSCRIBED / 3 SUBSCRIBED** ⇒ bucket `SUBSCRIBER` **KHÔNG phải sub thật**, nó là home feed.
Device: MOBILE 14,0% (6.105 view) vs DESKTOP 20,3% · TV 24,4%.
⇒ Xác nhận §3.5 (08-30): **95% traffic là feed lạnh sai sở thích.** Cùng chữ, cùng hình, chỉ đổi người xem → retention gấp 1,7–2,6×. **Không có bản viết lại nào bù được khoảng đó.**

### C. 🆕 BIẾN SCRIPT DUY NHẤT ĐO ĐƯỢC: mật độ dữ kiện ở cửa sổ **ký 50–150** (≈ giây 10–30)

corr(số dữ kiện ở ký 50–150 , awr@30s) = **+0,76…+0,83** (n=9) · corr với cửa sổ 0–50 ký = **−0,70**.

| nhóm | video | awr@30 | drop |
|---|---|---|---|
| ≥6 dữ kiện | v14 (12) · v16 (8) | **0,70** | −21 / −30 |
| <6 | v12·15·17·18·19·21·24 | **0,57** | −34…−51 |

🔴 **Ý nghĩa đắt nhất: bốn lượt "tối ưu cold open" trước đều DỒN LỰC VÀO GIÂY 0–10 — và chính việc dồn đó
làm CẠN cửa sổ 10–30s, đúng chỗ vách rơi.** v18 dồn 3 dữ kiện vào ký 0–50, còn 2 ở 50–150 → drop **−51**,
tệ nhất kênh. Cùng họ bài học *"giảm lặp sticker ≠ giảm số lượng"* (`audience-45plus.md` §2.0):
**tối ưu một chỉ số thì phải hỏi chỉ số nào là biến ĐÁNH ĐỔI của nó.**

✅ **Đã cài `G17` vào `check_pace.py`** (backup `check_pace.py.bak_20260910`): ≥6 dữ kiện ở ký 50–150 ·
0 cửa sổ 50 ký rỗng. Kiểm trên 21 script: chỉ v08/v10/v14/v16 đạt — đúng nhóm awr cao.

### D. 🔧 BA BẪY PHÉP ĐO GẶP TRONG CHÍNH LƯỢT NÀY (ghi để không lặp)

1. **`timeline()` của `check_pace` ĐẾM tag `[間]` mà không CỘNG thời gian.** Tổng thời lượng chỉ lệch
   ±2–5% (bù trừ nhau), nhưng **cửa sổ 30s đầu lệch 13,5%** (v24: ước 189 ký, thật 149) vì tag dồn hết
   vào cold open. Cộng tag vào chỉ hạ về 9,0% — vẫn quá lớn khi vách rơi ở giây 19–29.
   ⇒ G17 **neo theo KÝ TỰ** (30s = **148 ký**, trung vị 10 video có srt thật, dải 131–163).
   ⚠️ **VIỆC CÒN MỞ: G6 (stake ≤20s) · G7 (あなた ≤10s) · G11 (lộ trình ≤75s) VẪN chịu sai số đó** —
   mốc chúng báo "đạt" có thể thật ra 22–25s.
2. **Biến quyết định của phép đo C là REGEX, không phải nguồn.** Cùng dữ liệu: regex lỏng (đếm MỌI lần
   một con số xuất hiện) → **+0,85** (srt) / **+0,83** (script); `RE_NUM` cũ (cụm số+đơn vị đầy đủ) →
   **+0,52 / +0,47**. Nguồn srt-thật vs script-ước gần như không đổi kết quả ⇒ gate chạy được trên
   script CHƯA RENDER. ⇒ G17 dùng `RE_FACT` riêng. ⛔ Đổi regex thì **phải hiệu chuẩn lại ngưỡng**.
3. **Gán cả dòng vào bin theo vị trí ĐẦU DÒNG là sai** — dòng 41 ký gần bằng cả cửa sổ 50 ký, lệch tới
   một cửa sổ (bản đầu báo "50–100 rỗng" trong khi 月十八万円 nằm đúng đó). Vá: gán theo vị trí của
   CHÍNH con số. Cùng bẫy với việc dồn cả cue srt vào bin theo thời điểm cue bắt đầu.

### E. Hai thứ ĐỠ hơn tưởng

- **RELATED cùng ngách: 5/24 → 8/25** (đạt mốc >8/25 đặt ngày 08-30). YouTube **đang** học chủ đề.
  Hàng xóm mới xuất hiện: カメ先生 · あゆみ · 年金と暮らし · 元ハローワーク職員ケン · 歳月の足跡.
  Còn 17/25 là rác (プロ野球 · SKE48 · 不倫 drama · 詐欺師 · ダンベル).
- **Search toàn từ khoá đúng ngách** (公金受取口座 ×20, 年金支給日) và AVD search 3:32 > browse 2:21.

### F. ⚠️ v19 — bài học ĐỀ TÀI, không phải bài học cold open

v19 `高年齢雇用継続給付` browse AVP **9,2%** vs 14,4–15,6% của 4 video cùng nguồn. Đề tài này chỉ áp cho
người **còn đi làm 60–64 tuổi**, trong khi **74,9% khán giả là 65+**. ⇒ Sai đối tượng ở tầng **CHỌN ĐỀ TÀI**;
mọi gate script đều sạch mà vẫn tệ nhất. **Trục 在職/雇用継続 nên xuống ô thử nghiệm, không vào slot chính.**

### G. Đã làm / chờ user gật

✅ tool `tools/pull_curves.py` (viết lại, ra khỏi `06_VIDEO`) · ✅ gate **G17** + vá binning ·
✅ bản **cold open v4 cho video 22**: `03_SCRIPTS/_PROPOSAL_22_coldopen_v4_TTS.md` — PASS trọn bộ gate
30s đầu (STAKE 0:00 · あなた 0:00 · lộ trình 0:50 · G17 6 dữ kiện · 0 cửa sổ rỗng · cold open kết 1:03),
số liệu **lấy từ chính bài** (36万/18万/2か月/時効5年), không bịa.

⏳ **Chờ gật:**
1. **Thay cold open video 22** bằng bản v4. 🔴 Hệ quả: cold open cũ **20 dòng → mới 10 dòng**, mà
   `build_remotion_*` **neo scene theo CHỈ SỐ DÒNG** ⇒ phải dựng lại SCENES + `make_timeline_exact`
   + kiểm `len(timeline)` (memory `feedback_builder_neo_dong_kiem_timeline_truoc`). 12 clip i2v đã map
   theo lời cũ → phải rà `_MAP_I2V.md`.
2. **Script 22 còn rớt 7 gate THÂN BÀI** (G12 tỉ lệ 聞き手 1%/cần 12–25% · G13 4 khối chay >45s ·
   G14 hai marker payoff · G15 CTA đăng ký + câu định vị · CTA giữa 34%/cần 42–58%) — nó viết 08-30,
   TRƯỚC khi khuôn 2 vai được chốt 09-06. Đây là việc lớn hơn cold open.
3. **End screen + pin comment 5 video** (`06_VIDEO/_manual_studio_20260831.md`) — treo từ 08-31, phải
   bấm tay Studio. Đây là đòn bẩy đúng vào biến TRỘI (đưa người từ browse sang RELATED), rẻ nhất trong sổ.

📌 **MỐC ĐỌC:** giữ **AVD ≥3:50 · awr@120s ≥0,40**, thêm **awr@30s ≥0,65** (mức nhóm G17 đạt) và
**tỉ lệ RELATED cùng ngách** (8/25 → mục tiêu 12/25). Đọc lại **2026-09-20**.

---

## 2026-08-31 (CN) — THI HÀNH KẾ HOẠCH "tăng sub + retention → YPP" (user duyệt cùng ngày)

Đo tươi đối thủ trước khi làm (bench 3 kênh pin + quét 69 video ≥5K view tháng 8 + bench 3 kênh mới
lập — số ở `01_SWIPE_TITLES.md` mục nạp 08-31): ngách vẫn mở toang cho kênh mới (カメ先生 lập 01/08 →
597K view/31 ngày · 定年前後 lập 02/08 → 552K/30 ngày); sóng tháng 9 「給付金＋7万円案内開始」 nổ ≥5 kênh;
2 kết luận cũ bị bác (định期便5選 không cần chờ uy tín · シニア割/ゆうちょ nay là tin có kỳ hạn đang nổ).

**Đã làm hôm nay:**
1. ✅ Trailer kênh v12 → **v13** (`pn9Fi9Bx6_U`, AVP 27,5%) — `tools/apply_channel_fix_20260831.py --apply`.
2. ✅ Gate **G9/G10/G11 cài vào `check_pace.py`** (G9 = ĐẢO gate cũ: モニター phải SAU 2:00 · G10 ≤2 tag 間/速 trong 75s · G11 câu lộ trình ≤75s). Kiểm: v15 rớt 3 gate mới (đúng kỳ vọng) — và ⚠️ **v18 RỚT G9** (松本 vào ~1:20–1:24 thật) ⇒ v18 chưa thi hành trọn luật モニター; đọc 09-05 nhớ nó lẫn **3 biến** (cold open v3 chưa trọn + sticker 25 lượt + G9 rớt).
3. ✅ Soạn `06_VIDEO/_manual_studio_20260831.md` — end screen + pin comment 5 video (09/12/13/14/15), **chờ user bấm tay Studio (Profile 17)**.
4. ✅ Câu định vị verbatim + CTA đăng ký gắn franchise 支給日直前チェック vào khuôn (CLAUDE.md §③) — áp từ v19.
5. ✅ Nạp swipe file 3 kênh mới + khuôn **T3 紙が主体** (0 mặt + mũi tên đỏ) hồi sinh làm slot A/B T3 (`03_THUMBNAIL_TITLE_FORMULA.md`).
6. ✅ Queue 24–30 + chen sóng tháng 9 + ô thử nghiệm ゆうちょ (user gật) + 総集編 cụm 届く紙 → `02_CONTENT_PLAN.md` §C.0.

**Chờ:** user bấm tay end screen/pin (mục 3) · đọc số **09-05** (RELATED cùng ngách >8/25 ·
AVD/awr v18 · unique viewers v12).
7. ✅ (cùng ngày, tối) **Script farm tháng 9 = VIDEO 24** 「年金生活者支援給付金・9月の緑の封筒」 —
   check_pace PASS 11/11 (bản đầu qua đủ G9/G10/G11), ~13,3′, FACT SHEET kế thừa v10 (verify 08-10,
   số 令和8年度), gói CTR + 3 prompt thumbnail (T3 = 紙が主体 đầu tiên) đã xuất. Slot đề xuất CN 09-06.
8. ✅ (2026-09-01) **Dựng slides + hook v3** — `_scenes24.py` (45 scene) + `build_remotion_24.py`
   sạch 4 gate hình học ngay lần đầu (0 scene <6s, 0 chồng, peak hợp lệ, phụ đề ≤78 ký). Tái dùng
   21/24 sticker từ kho v19; sinh 34 prompt photocard + 3 prompt sticker mới (phong bì xanh/はがき/tem)
   → `06_VIDEO/24_.../art_prompts_photocard24_FLOW.txt` + `sticker_prompts_v24_FLOW.txt`.
   Sau đó user yêu cầu "30s đầu phải đánh vào nỗi sợ" — viết lại câu 1–3: あなた là chữ đầu tiên,
   câu 1 chở thẳng số mất mát (không còn khung "phát hiện" trung tính), roadmap/lối thoát dịch
   50s→**37,4s**. Re-run `make_timeline_exact.py` + `build_remotion_24.py` (NEO SCENE BẰNG CHỈ SỐ
   DÒNG nên SCENES không cần sửa tay). Vẫn PASS 11/11, project.json 45 scene/767s/172 sự kiện.
   **Chưa chụp 3 shot 原典** — không có tool Chrome/screenshot trong phiên; 2 đường còn treo: user
   tự chụp theo 3 từ khóa tìm kiếm đã đưa, hoặc dùng fallback genten của v10 cho 2/3 shot.
   Checklist sản xuất còn lại ở cuối file script.

**v19 (render 08-31, user báo gần xong — KHÔNG sửa bài, đo hậu kiểm):**
- ✅ Biến quyết định SẠCH: **G9 松本 @3:10** (ngoài 0–120s — phép đo モニター sạch đầu tiên) ·
  **nhịp hình 242 sự kiện/927,7s SẠCH 3/3** (v18: 25 lượt) · G10 1 tag · STAKE @0:06 ·
  câu định vị 「制度を読むだけの番組ではなく…計算する研究室」 đã nằm trong lời đọc (mục A4 tự đạt).
- 🟡 Lệch chuẩn, chấp nhận có chủ ý: cold open kết ~1:33–1:39 (chuẩn ≤1:15) · **KHÔNG có câu
  lộ trình tường minh (G11)** — mở ④対決型 open-loop kép thay 「◯つを順番に」 · あなた @0:38 (G7,
  gate đã bị bác vai thuốc) · CTA 59% (lệch 1 điểm, trong sai số ±4%).
- ⇒ Đọc số v19: nó test được **"モニター ra khỏi phút 1–3 + nhịp hình đủ"**, KHÔNG test được
  "câu lộ trình" — nếu awr@120s v19 vẫn thấp thì câu lộ trình là biến kế tiếp phải thử (v20 có),
  đừng vội kết luận モニター vô can.
- 🔧 Vá tool cùng lượt: detector cold-open của `check_pace.py` nhận cả 「研究室です」 (v19 bỏ
  こんにちは nên gate báo 0:00 giả).

## 2026-08-29 (T7) — 🔬 KHÁM LẠI: giả thuyết cold-open 08-20 BỊ BÁC · bệnh nằm ở PHÚT 1→3 (khối モニター)

Bản đầy đủ: **`CHANNEL_DIAGNOSIS_2026-08-29.md`**. Tóm:
- **Vòi mở, bao bì ăn, tệp đúng:** 28d **23,7K imp · CTR 7,7%** · browse 91,8% · **65+ 74,9% / 55–64 22,6%** · nam 88%. v15 nổ lần 2: 158 → **1.116 view** (98,7% browse). ⇒ KHÔNG đụng thumbnail/title/lịch để chữa retention.
- **v15 (khuôn mở MỚI あなた@3s) relPerf@60s = 0,14 — tệ nhất kênh** (v12 khuôn cũ 0,24). Cả 5 video rơi −30 điểm đúng giây 19→29 bất kể lời mở ⇒ vách 20–30s **không phải chữ cold open**. Studio: "52% @30s = như thông thường".
- **Chỗ mất thật: 60→120s.** 4 video có モニター vào ở 58–85s mất 13–22 điểm; **v09 (không モニター, đọc 3 mục + 第一章 sự thật) phẳng 0,37→0,37**. Đối chứng nội kênh duy nhất. 3 hit đối thủ (フクロウ 1,39M/1,36M · お金の保健室 37K) 60s đầu: mệnh lệnh + 対象 + lộ trình 3 mục + open-loop, **không nhân vật hư cấu**.
- **Mốc mới:** Studio đo AVD "bình thường" cho v15 = **3:51**, mình 2:32. Từ nay đọc **AVD ≥3:50 · awr@120s ≥0,40**, bỏ mốc relPerf@60s.
- ⚠️ v15: 1.116 view / **235 người xem riêng biệt** (4,7×) — nghi autoplay home feed tính view. ⏳ kiểm v12.
- ✅ **08-30 user gật 1–6, đã thi hành:** ① script 18 cold open v3 (松本 dời khỏi 0–120s, lộ trình <75s, 2 tag/75s) — `check_pace` PASS 8/8, voice v3 15:13 + timeline 115 dòng (lệch 0,93%), builder 5 gate sạch → `project.json`; **còn 18 asset chưa gen → chưa render** (luật 1.5) ② title A1 đổi keyword-đầu `年金を60歳から受け取ると月4万3千円減ります｜請求書に丸をつける前に`, 【取り消せません】 xuống A3 ③ 3 playlist theo trụ tạo public (PLSHjlM17Oamc · PLT4QEuxo4MWw · PLZVtF_edAA5s), playlist cũ giữ ④ v09/v11 cat 22→27 · credit VOICEVOX v01/02/04 · channel desc 火・木・日 (tool `tools/apply_channel_fix_20260830.py`) ⑤ ⏳ **end screen + pin comment CHƯA làm** — Data API không có endpoint, phải bấm tay trong Studio (5 video: 09/12/13/14/15).
- (cũ) ⏳ Chờ user gật: ① sửa script 18 (松本さん đang vào @18s — dời ra khỏi 0–120s, thêm câu lộ trình <75s, ≤2 tag 間/速 trong 75s đầu) ② gate G9–G11 vào `check_pace.py` ③ cat 22→27 cho v09/v11 · credit VOICEVOX v01/02/04 · đổi trailer v12→v13 ④ nhịp: khuyến nghị GIỮ 3/tuần (RELATED 3,2%, chưa đạt §0.9).
- ⭐ **08-30 kiểm 'sai tệp':** nhân khẩu ĐÚNG (JP 100%, 65+ nam) nhưng **sở thích SAI** — 19/24 video dẫn RELATED là bóng chày/SKE48/麻雀/不倫 drama/ラブホ; chỉ 5 cùng ngách. YouTube xếp kênh vào feed 'nam 65+ nói chung', chưa biết chủ đề ⇒ giải thích CTR cao + vách 20–30s + 4,7 view/người. Đề xuất: hàng xóm thật (あゆみ/フクロウ), keyword đứng đầu title thay 【見逃し厳禁】, end screen + 3 playlist theo trụ, sửa desc 月水金→火木日. Chi tiết §3.5.
- Tool mới: `06_VIDEO/_diagnose/pull_curves.py` — curve 0–100% + traffic cho mọi video ≥20 view.
- Mốc đọc lại: **2026-09-05** (v18 đủ 5 ngày).
- 🔴 **CẢNH BÁO ĐỌC SỐ NGÀY 09-05 — v18 LẪN HAI BIẾN, đừng quy hết cho cold open.** Ngoài cold open v3, v18 còn vô tình đổi **mật độ hình**: lượt sticker **186 (v17) → 25 (v18)**, thời lượng frame đứng yên >7s **67,7% → 87,2%**, thêm **5 scene "nền trống"** (không hero, không bảng) — user bắt bằng mắt 08-30. Nguyên nhân: lượt sửa "sticker đừng trùng nhau nhiều" giảm LẶP bằng cách giảm SỐ LƯỢNG (`audience-45plus.md` §2.0).
  ⇒ **AVD/awr@120s của v18 thấp KHÔNG chứng minh cold open v3 sai** — chán-vì-đứng-hình là nghi phạm ngang hàng. Muốn đọc sạch cold open thì phải chờ **video 19** (đã có gate nhịp hình chặn, biến mật độ được giữ cố định). v18 chỉ đọc như tín hiệu tham khảo.
  ⚖️ User chốt 08-30 **giữ nguyên v18, không render lại** (*"video 18 tao làm xong rồi, sửa lại cho những video tiếp theo thôi"*) — đánh đổi đã biết trước, không phải thiếu sót.

---

## 2026-08-20 (T5) — 🔥 VÒI MỞ LẦN ĐẦU (video 12) + MỔ RETENTION 16%

### Số (API `diagnose_channel.py` + retention full-curve, đo 2026-08-20)

- **Video 12 `zr9uJbDFaoU`** (住民税の紙が10月に届きます, đăng CN 16/08): **1.451 view** lúc đo — analytics mới ghi tới 08-17 (246 view) ⇒ **~1.200 view đến trong 3 ngày 08-18→08-20, vòi CÒN ĐANG BƠM**.
- Nguồn: `SUBSCRIBER` = **233/246** (bucket API này gồm **home feed** — kênh chỉ có 5 sub nên đây là browse/trang chủ, không phải sub thật) · RELATED 9 · search 2. **Đây là lần đầu tiên trong đời kênh YouTube phát video lên trang chủ người lạ** — cuộc audition giống health từng có (~18,6K impressions) trước khi bị đóng vòi.
- **AVP 16,0% · AVD 158s/992s** — đúng con số user thấy trong Studio.

### Đọc retention CHO ĐÚNG — bệnh nằm ở 48 GIÂY, không phải cả video

| mốc | awr | relPerf |
|---|---|---|
| 10s | 96,6% | 0,27 |
| 20s | 94,5% | 0,23 |
| **30s** | **64,4%** | **0,20** ← vách đá: −30 điểm trong 10 giây |
| 50s | 46,2% | 0,22 |
| 60s | 43,2% | 0,24 (mốc khỏe ≥0,40 — health chết ở 0,10–0,14) |
| 3–7′ | 20–25% | **0,35–0,46** (leo dần) |
| cuối bài | 5,5% | **0,79** |

⇒ **Thân bài KHỎE** (relPerf giữa bài 0,4+, kết bài 0,79 = top). Toàn bộ tổn thất dồn vào **giây 20–50**. Không phải "video chán" — là "48 giây đầu đuổi khách".

### Cơ chế (giả thuyết CÓ đối chứng nội bộ, chưa phải nhân quả đã chứng minh)

Vách 20→30s rơi đúng đoạn 「もう一軒は、引き出しに入れます。去年は届かなかった紙だから、もう自分には関係ない…」:
1. **Khuôn mở NGỤ NGÔN NGÔI THỨ BA** ("hai ngôi nhà") — người xem browse-lạnh là khán giả đứng ngoài xem chuyện người khác; chữ **あなた không xuất hiện trong cả phút đầu**. Số đắt (5万2千円) đến ở 0:27 — **SAU** vách. Câu "ai bị liên quan" (税金を引かれていない方にまで届きます) đến tận **0:56**.
2. 0:38–0:50 còn chèn **12 giây nhượng bộ nuance** (「引き出しに入れたお宅の判断は去年までなら正しかった」) ngay trong cửa sổ quyết-định-ở-lại.
3. **Đối chứng:** video 09 (公金受取口座) mở 「いま、**あなたの**お宅に、一通の簡易書留が…」+ deadline 45日 ở 0:21 → relPerf@30s = **0,42, gấp đôi video 12**. ⚠️ Caveat: 09 ăn search-traffic (intent cao hơn browse) nên phép so không sạch 100% — nhưng chiều của nó khớp mọi bài học cold open đã có.
4. **Video 13 VÀ 14 lặp đúng khuôn ngôi-thứ-ba** (mở bằng 佐藤さん/中村さん; あなた-widening ở 0:31/0:57) — tức mẫu retention đáy sẽ **tự lặp** nếu không sửa khuôn.
5. Gate `check_pace.py` video 12 đều PASS (cold open xong 1:13, nhân vật 1:18) — gate đang đo MỐC vào bài, **chưa đo được "cắm stake cá nhân hoá trước giây 20"**. Đúng bài học `feedback_gate_pass_khong_phai_retention`.

### Rủi ro & cơ hội
- **Rủi ro:** 2–3 video kế vào test với cùng khuôn mở → điểm kênh ăn thêm mẫu retention đáy → vòi đóng đúng kịch bản health 07-20.
- **Cơ hội:** thân bài đã tốt — chỉ phải sửa ~50 giây đầu, và cụm đề tài 住民税・紙が届く vừa được chứng minh có cầu browse thật.

### Hành động đề xuất (chờ user chốt phần có dấu ⏳) — cập nhật tối 08-20 sau khi thi hành
1. ✅ **KHÔNG đụng video 12** — đang giữa cuộc test, sửa/re-upload là phá phép đo + mất momentum.
2. ✅ **Farm cụm đang nổ — ĐỀ ĐÃ ĐỔI khi soi kỹ:** ⛔ 「扶養親族等申告書の書き方」 HOÃN (form 令和9年分 chưa tồn tại — script 12 FACT #20, viết cách điền trên form cũ = rủi ro YMYL). Thay bằng **N6 「10月15日の年金振込、8月より少ない」** — chính là lời hẹn ĐÍCH DANH cuối video 14 (đã lên sóng) + pocket 「介護保険料 10月 増える」 median 71K/cung mỏng (bench 08-05). **Script 15 VIẾT XONG 08-20:** `03_SCRIPTS/15_nenkin-furikomi-10gatsu-honchoshu.md` + `_TTS.md` (13:35, 28/28 tag, PASS 8/8 gate check_pace). Slot CN 23/08. Còn lại để lên sóng: builder SLIDES (`build_slides_15.py` theo khuôn 14) + gen ảnh/genten (2 shot: 世田谷区 仮徴収/本徴収 · 上越市 段階表 khoanh 第6段階) + thumbnail (prompt 4 file đã viết ở `06_VIDEO/15_…/thumb_prompts_*.txt`, TEXT @8–10%, gate §3.1 pass) + render.
3. ✅ **Khuôn cold open MỚI đã chạy ở video 15:** あなた @0:03 · stake @0:03 · 対象 @~0:25 · モニター @0:58 · không nuance 60s đầu. Đây là **phép đo đầu tiên của khuôn** — khi 15 có số retention, so relPerf@60s với video 12 (0,24).
4. ✅ **3 gate máy ĐÃ CÀI vào `check_pace.py` 08-20:** G6 STAKE (円/日, loại trừ ngày tháng) ≤22s · G7 あなた ≤10s · G8 モニター trước あなた trong 30s đầu → 🔴. Test hồi tố: video 09 xanh 3/3 · video 12 rớt G6+G7 · video 14 rớt G7+G8 — gate bắt đúng bệnh từng video.
5. ⏳ **Nhịp đăng:** video 12 đã vượt mốc ramp ">1.000 view organic/72h" (`upload-schedule.md` §0.9b mục 2 — viết cho health nhưng cùng cơ chế). Tăng lên 1/ngày hay giữ 3/tuần + 1–2 slot farm = **user quyết** (nguồn chính là browse chứ chưa phải RELATED/SUGGESTED nên chưa auto-đạt điều kiện "đang được đề xuất" của Mục 0.9).
6. ⏳ Việc treo cũ nay thành gấp: 01/02/04 thiếu credit 「音声: VOICEVOX:雀松朱司」 — kênh sắp có mắt người lạ, nên vá (cú ghi lên kênh, chờ gật).

### Mốc đọc lại: **2026-08-23** — ① video 12 còn được bơm không ② video 13/14 có vào test không, relPerf@60s của chúng ③ video đầu tiên mang khuôn mở mới so với khuôn cũ.

---

## 2026-08-10 (T2) — ĐO 2 KÊNH ĐỐI THỦ ĐANG NỔ → ĐỔI 3 BIẾN CÙNG LÚC

**Không đo số của chính kênh lượt này** (mốc đọc lại vẫn là **2026-08-17** như block 08-03 đã đặt —
đừng đọc sớm, impressions còn quá nhỏ). Lượt này đo **bên ngoài**: kênh user chỉ ra
`フクロウの年金・給付金解説室` (45,4K sub, **+792.386 view/7 ngày**) + kênh clone tôi tìm thêm
`タヌキの年金相談室` (47K sub). Bằng chứng đầy đủ: **`CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md`**.

### Ba biến đổi cùng lúc (user chốt) — và vì sao chấp nhận bundle

| # | Biến | Từ → thành | Căn cứ |
|---|---|---|---|
| 1 | **Độ dài** | 25–30′ → **13–17′** | median 14 hit ≥100K của フクロウ = **15′00**; タヌキ rút 18–32′ → 9–12′, các bản ngắn thắng |
| 2 | **Title `【】`** | bỏ (08-09) → **bật lại** | フクロウ **41/41** · タヌキ **~39/39** video dùng `【】`, hit 1,3M/1,0M |
| 3 | **Thumbnail** | TELOP → thêm khuôn **I「紙が主体」** | bản **1,0M view** không có mặt người, chủ thể là **cái phong bì** |

🔴 **Đổi 3 biến một lượt thì KHÔNG tách được attribution** — nhưng ở mức **114 impressions/28 ngày**
thì **không tách được kể cả khi đổi 1 biến**. Ghi rõ ở đây để sau đừng gán công/gán tội cho một biến.
**Cái đọc được** khi có số: impressions nhóm mới vs nhóm cũ → YT_SEARCH → SUGGESTED ≠ 0. **Chưa đọc CTR
khi impressions <500/video.**

### Phát hiện đắt nhất — ranh giới sống–chết trong lớp「紙が届く」
Cùng khuôn "tờ giấy về nhà", chênh tới **300 lần**: giấy mà **tiền bị lấy tự động** hoặc **給付金 có số
yên cụ thể** thì 86K–1,3M; **giấy thuế tự khai để xin giảm trừ** thì 2,4K–9,4K.
⇒ Đã phân lớp lại toàn bộ hàng đợi (`02b_QUEUE_4KHUON_2026-08-08.md` §cập nhật 08-10) và **hạ N3
扶養親族等申告書** — vẫn làm (video 11, giữ lời hứa của video 09 + trả nợ trụ ③) nhưng **không kỳ vọng
nó mở vòi**, và **không xếp thêm đề cùng họ**.

### Cảnh báo thị trường — cửa vào đang chật
Trong **4 ngày** qua có ≥5 kênh đăng đúng đề tài 9月ハガキ: タヌキ 11K/2 ngày · 年金・給付金完全攻略
7,5K/1 ngày · 定年後のお金の学校 1,5K/2 ngày · **天村くん (120K sub) chỉ 743 view/4 ngày**. Các bản
triệu view đều là **bản cũ**. ⇒ Cầu có thật, nhưng đừng đọc "1M view" như thứ sẽ tự tới.

### Việc đã làm trong lượt này
- `CLAUDE.md`: §TITLE bật lại `【】` · **§ĐỘ DÀI 13–17′ mới** · cast thêm **渡辺さん** + cập nhật 伊藤.
- `.claude/rules/audience-45plus.md` §4 + §4.2 mới: nenkin 25–30′ → 13–17′ (kèm cảnh báo **không suy rộng**).
- `03_THUMBNAIL_TITLE_FORMULA.md`: thêm **khuôn I「紙が主体」** + bảng "khuôn đang khoá" (A-45 hạ xuống đường lui).
- Video 10 viết xong: script + `_TTS` + `_SLIDES` (73 thẻ) + 4 原典ショット + 4 file prompt thumbnail.

### Việc còn treo (không tự quyết)
1. 🔎 **Altered/synthetic content: tick hay không?** Cast sân khấu là **ảnh AI người trong video** →
   `youtube-compliance.md` §2.1 (chốt 08-09) đòi **TICK**; bảng compliance của script 09 ghi **không
   tick**. Video 09 lên sóng 08-11 và video 10 ngay sau → **hai video liền nhau khai khác nhau là tệ
   nhất**. Cần user chốt một lần.
2. 3 video live (01·02·04) vẫn **thiếu dòng credit 「音声: VOICEVOX:雀松朱司」**; 04 thiếu luôn 出典.
3. A2/A3 title để dành, chỉ xoay khi impressions ≥500/video.

---

## 2026-08-03 (CN) — KHÁM KÊNH #2 + ĐỔI THUMBNAIL 3 video (khuôn 原典 mới)

### Số (Studio, khung 28 ngày 6/7–2/8, đọc bằng browser — API đã bị rút metric impressions)

| | 07-28 | **08-03** |
|---|---|---|
| view | 7 | **13** |
| **impressions** | 50 | **114** |
| **CTR** | 6,0% | **3,5%** (= đúng **4 click**) |
| AVD | 9:04 | **10:44** |
| suggested | 0% | **0%** |

Traffic: browse 38,5% · trang kênh 38,5% · search 15,4% · ngoài 7,7%. Funnel: 114 impr → 4 view → 0,63 giờ.

- **Chẩn đoán GIỮ NGUYÊN so với 07-28: bệnh là "CHƯA ĐƯỢC PHÁT".** 114 impressions/28 ngày = chưa hề có cuộc thử nghiệm nào.
- ⚠️ **CTR 3,5% KHÔNG đọc được**: n=114 với **4 click** → CI95 ≈ 1–9%. Việc nó "tụt từ 6,0%" cũng vô nghĩa thống kê (trước đó là 3/50). **Cấm dùng con số này làm bằng chứng thumbnail tốt/xấu.**

### Trend YouTube Search JP 30 ngày (đo 08-03, `gprop=youtube`, `geo=JP`)

| keyword | điểm |
|---|---|
| **加給年金** | **24** |
| 年金改正 | 10 |
| 在職老齢年金 | 7 |
| 働きながら 年金 | 2 |
| 年金 カット | **0** (không có dữ liệu) |

Breakout: 「在職老齢年金 改正」・「在職老齢年金 支給停止」 急激増加 · 「加給年金」 +350% trong related của 年金改正.

- 🔴 **Title video 01 đang chứa 年金カット = từ 0 điểm** (từ chết ở YouTube search 30 ngày).
- 🔴 **加給年金 là từ mạnh nhất cả rổ — và đó chính là video 06, video đang để làm ĐỐI CHỨNG.** Ghi lại để 14 ngày nữa đọc số không nhầm nhân quả.
- ⚠️ **Rổ 2 (繰り下げ) và rổ 3 (給付金) CHƯA đo được** — Google Trends rate-limit chặn, thử 6 lần đều trả biểu đồ trắng. Đo lại khi hết chặn.

### Đã làm: đổi 3 thumbnail sang **khuôn 原典** (user chốt khuôn 08-03)

| video | ID | thumbnail |
|---|---|---|
| 01 在職老齢年金 | `bWl2jE9l8z4` | 原典 · hero `65万` · nhãn 支給停止調整額 |
| 02 繰り下げ | `uPlyzkGYfCs` | 原典 · hero `何歳?` · nhãn 繰り下げの損益分岐点 |
| 04 支援給付金 | `MfEKhbXdTXY` | 原典 · hero `6万円` · nhãn 年間の上乗せ額 |
| 05 · 06 | `xWyfoi59uSs` · `TTwuFmKa3T8` | **KHÔNG ĐỤNG — nhóm đối chứng** |

- **Chỉ đổi 1 biến: THUMBNAIL.** Title / 3 dòng đầu 概要欄 / tag **giữ nguyên** (verify sau khi ghi: cat 27, `ja/ja`, tag 32/28/27 không đổi). Đúng `ab-3title-3thumb.md` §1 — đổi title giữa chừng là lẫn 2 biến.
- Tool mới: `tools/make_thumb_genten.py` (khuôn) + `tools/update_live.py` (ghi lên video đã live, dry-run mặc định, backup snippet cũ → rollback được: `06_VIDEO/_repack_2026-08-03_backup.json`).
- Gate 45+: dòng chính **34,2 / 34,3 / 34,2%** khung · 3 khối chữ · nền giấy sáng · mặt cắt tròn mắt nhìn thẳng.
- 🔴 **Lỗi bắt được SAU khi đã đăng lần 1: badge `年金研究室` đặt góc dưới PHẢI bị YouTube đè timestamp thời lượng.** Đã dời sang **góc dưới TRÁI** và đăng lại. `make_thumb_genten.py` khoá `--badge-pos` mặc định `bl`. **Áp cho mọi khuôn thumbnail của mọi kênh: góc dưới phải là của YouTube, đừng đặt gì vào đó.**

### Đã làm (lần 2, cùng ngày): ĐỔI LUÔN TITLE + 3 dòng đầu 概要欄 + tag

User chốt áp tiếp sau khi thumbnail xong ⇒ **3 video này giờ đổi 2 BIẾN cùng lúc** (thumbnail + title).
⚠️ **Hệ quả cho việc đọc số 17/08: không tách được công của thumbnail và của title.** Chấp nhận có chủ ý — ở mức 4 click thì attribution vốn đã vô nghĩa; mục tiêu lượt này là *sửa cho đúng*, không phải *đo cho sạch*. Nhóm đối chứng 05·06 vẫn nguyên nên vẫn còn mốc so ở cấp kênh.

| video | title mới | ký | đổi gì |
|---|---|---|---|
| `bWl2jE9l8z4` | 【2026年 年金改正】在職老齢年金の支給停止は月65万円から｜働きながら年金をもらう方へ | 45 | bỏ 「激変」+「年金カット」(**0 điểm** trên YouTube search), dẫn bằng **年金改正** (10 điểm) + 支給停止 (breakout) |
| `uPlyzkGYfCs` | 【70歳まで待つ前に】年金の繰り下げ受給で損をする人の共通点｜損益分岐点は何歳? | 40 | **thôi khai đáp án 82歳 ngay trên tiêu đề** (bản cũ tự spoil → người tra xong khỏi bấm) |
| `MfEKhbXdTXY` | 【申請しないと0円】年金生活者支援給付金、年6万円超を受け取る3つの条件 | 36 | thêm 【】 + con số 年6万円超 |

- Cả 3 giờ đều mở bằng 【】 (benchmark ngách 51/52 video). Tag: 32 / **28→30** (+損益分岐点, 年金 70歳) / 27.
- Verify sau khi ghi: `cat 27` · `ja/ja` · 目次 + disclaimer + hashtag còn nguyên · desc 749/821/719 ký.

### 🔴 Lỗi CÓ SẴN vừa lòi ra khi verify (KHÔNG do lượt này gây ra)

**3/3 video thiếu dòng credit giọng 「音声: VOICEVOX:雀松朱司」 trong 概要欄.** Đối chiếu backup snippet cũ: bản trước khi sửa cũng không có ⇒ thiếu từ lúc đăng, không phải do `update_live.py` cắt mất.
- Ràng buộc thật: `CLAUDE.md` nenkin yêu cầu dòng credit này, và **điều khoản VOICEVOX đòi ghi 「VOICEVOX:キャラ名」** ở đâu đó (概要欄 / pinned comment / cuối video).
- Thêm: video 04 `MfEKhbXdTXY` **thiếu luôn dòng 出典** (01 và 02 có).
- ⏳ Chưa sửa — là cú ghi lên kênh mới, chờ user gật. Sửa bằng `update_live.py` sau khi thêm cơ chế chèn cuối mô tả (hiện tool chỉ thay được 3 dòng đầu).

### Mốc đọc lại: **2026-08-17 (14 ngày)** — đọc theo thứ tự

1. **Impressions nhóm đổi (01+02+04) vs nhóm giữ (05+06)** — câu hỏi thật của lượt này.
2. `YT_SEARCH` có tăng không (nhưng lượt này KHÔNG đổi title nên không kỳ vọng).
3. `SUGGESTED` lần đầu khác 0 → tín hiệu rail mở, **không được quy công cho thumbnail**.
4. CTR: **chỉ đọc khi impressions/video ≥500**. Dưới mức đó là nhiễu.

### Lệch rule CÓ CHỦ Ý (ghi sổ, không giấu)

- Bảng ngưỡng đầu file **cấm swap thumbnail khi impr <500**. Lệch vì lý do khác CTR: 4 bản live đang rớt gate 45+ đã ghi nợ từ 08-01 (gate 4 mặt, gate 6 nền sáng). Đây là **trả nợ packaging**, và kết quả CTR sau đó sẽ **không** được dùng làm bằng chứng.
- `ab-3title-3thumb.md` đòi 3 thumbnail/video: lượt này **1 bản/video**, không bật Studio "Test & compare" — chia 114 impressions cho 3 bản thì không bao giờ kết luận được.

### Còn treo

1. ✅ **Title ĐÃ áp cùng ngày** (xem mục "lần 2" ở trên). Còn lại: **A2/A3 của mỗi video để dành**, chỉ xoay tuần tự ≥7 ngày/bản khi impressions đủ để CTR có nghĩa (≥500/video). ⚠️ **Title 02 và 04 chốt bằng nguyên tắc, CHƯA bằng số** — Trends rate-limit chặn 6 lần ngày 08-03; đo lại rổ 繰り下げ + 給付金 khi hết chặn, lệch thì sửa.
2. Khoá khuôn 原典 thành khuôn chính của kênh trong `03_THUMBNAIL_TITLE_FORMULA.md` (đang chờ user gật) — hiện §6 vẫn ghi A-45 là khuôn chốt.
3. 🔴 **Thứ duy nhất trong đống này dính tới việc kênh chưa được phát: độ dài 15,5′ median vs ngách 26–37′.** Thumbnail/title không mở được vòi.

---

## 2026-08-01 (T6) — check nhanh theo yêu cầu user + đóng việc treo defaultLanguage

- **Số:** 12 ngày tuổi · 5 video · **8 view · 0 sub** (+1 view so với 07-28). Video 06 加給年金 (30′50″, title 【】 — video ĐẦU TIÊN đúng chuẩn format ngách) lên T6 31/07 19:00, mới 1 ngày → **chưa đọc được gì, đừng kết luận**.
- ✅ **`defaultLanguage` cấp KÊNH đã sửa `en` → `ja`** (channels.update part brandingSettings, user gật qua plan 2026-08-01; verify lại bằng channels.list: title/country/description giữ nguyên). Đóng việc treo `CHANNEL_DIAGNOSIS_2026-07-28.md` §5.3.
- **Phương án đã chốt với user (plan `noble-swinging-pine`):** ① đọc số video 06 sau 72h vào T2 03/08 (ritual) ② T6 07/08 = script 03 nâng lên 25–30′ ③ ⭐ T3 11/08 = 支給日回 #1 【8月14日振込】振込通知書 (cú đánh search chính của tháng) ④ checkpoint ~17/08 + cuối T8 (~9–10 video) ⑤ **van thoát:** video 10–12 vẫn <500 impressions tổng → kéo mega 定期便に載らない bản 原典 từ GĐ C lên sớm. KHÔNG đổ volume / đổi giờ / sửa thumbnail / pivot.

---

## 2026-07-28 (T3) — KHÁM KÊNH #1 → ĐỔI LỊCH + tìm ra lệch format

> Hồ sơ đầy đủ: **`CHANNEL_DIAGNOSIS_2026-07-28.md`** · tool đo: `python tools\diagnose_channel.py`

- **Số:** 8 ngày tuổi · 4 video public · **7 view · 0 sub**. Traffic: `YT_CHANNEL` 2 · `SUBSCRIBER` 2 · `YT_SEARCH` 1 → **0 view từ browse/suggested**.
- **KHÔNG án phạt, KHÔNG deindex:** video #4 hạng **1** cho 「60歳 即退職 老後資金 700万円」, video #3 hạng **2** cho 「年金生活者支援給付金 申請 消える」. Cấp video: `ja/ja` · srt tự tải · thumb maxres · **cat 27 khớp benchmark 23/24 video**.
- **Chẩn: BỆNH 1 (0 phân phối) — GIỮ NGUYÊN chẩn đoán 07-25, nhưng hành động thì ĐẢO:** bảng ngưỡng phía trên ghi *"giữ nhịp 3/tuần"*; số nói ngược. Thực tế đã đăng **3,5 video/tuần** (4 video/8 ngày, ngày rải T2·T4·T7·T3, 1 video lệch giờ 16:44) mà vẫn 0 browse ⇒ **volume không phải cái mở vòi**.
- ✅ **Lịch chốt lại: T6 19:00 JST — 1 video/tuần · T3 = slot PHỤ** (chỉ 支給日/tin chính sách nóng; mốc kế **T3 11/08** trước 支給日 14/08). Đã sync `upload_pack.py` + `.claude/rules/upload-schedule.md` + `CLAUDE.md`.
- 🔴 **Lệch format ngách (phát hiện nặng nhất, CHƯA sửa — chờ user chốt):** độ dài **15,5′ median vs ngách 26–37,5′** (không benchmark nào <17′) · title mở 【】 **1/4 vs 51/52**.
- 🔴 **Sửa 1 giả định của luật lịch đăng:** winner 完全攻略 (132K sub) đăng giờ **rải bừa 03:32–23:42, không giờ cố định**, vẫn ăn hit 3,84M ⇒ **giờ/ngày KHÔNG mở được vòi phân phối**. Giữ giờ cố định vì thói quen khán giả, đừng trông nó chữa 0-view.
- **Kỳ vọng chuẩn lại:** winner video #1 = 4.799 view, #2 = 12.000, **hit 3,84M ở #3 ngày thứ 13**; hit rate ~4/12. → 4 video đầu ít view là bình thường; **cái đáng lo là 7 view, không phải 4.000**.
- ✅ **ĐÃ ĐỌC STUDIO (cùng ngày, browser, Chrome Default) — số quyết định:**

| Video | Dài | view | **Impressions** | **CTR** |
|---|---|---|---|---|
| 在職老齢年金 | 13'30 | 3 | **23** | **8,7%** |
| 年金生活者支援給付金 | 15'16 | 2 | **14** | **7,1%** |
| 繰り下げ受給 | 15'39 | 2 | **6** | 0% |
| **TỔNG** | | **7** | **50** | **6,0%** |

  Nguồn view: browse 42,9% · trang kênh 42,9% · search 14,3% · **suggested 0,0%**. AVD 9:04 (~58% AVP).
- 🔴 **Chẩn đoán CHỐT: bệnh là "CHƯA ĐƯỢC PHÁT", không phải "phát mà không ai bấm".** 50 impressions/28 ngày = chưa hề có cuộc thử nghiệm nào (health được ~18.600 impressions rồi mới bị tắt vòi → **2 kênh 0-view, 2 bệnh khác nhau hoàn toàn**). CTR 7–8,7% trên n=14–23 → **trên mốc ngách 4–6% nhưng vô nghĩa thống kê**; chỉ đọc được là "chưa có dấu hiệu thumbnail là vấn đề".
- ➡️ **Hệ quả:** đổ công vào thumbnail lúc này = đổ vào không khí. Hai cửa ra cold-start: **① SEARCH** (đề tài có cầu tìm kiếm thật — đo trend, không chọn theo cảm giác) **② BROWSE/SUGGESTED** (cần watch-time/impression cao → đúng chỗ độ dài 15′ vs 26–37′ đang tự bó tay).
- ⏳ **CÒN MỞ (cần user gật):** `defaultLanguage` cấp KÊNH đang `en` (nên `ja`) — sửa bằng `channels.update` nhưng là **ghi lên kênh**. ⚠️ Lệch tài liệu: `channel-browser.md` map nenkin ↔ `Profile 17` nhưng lần đo này chạy trên **Default**.
- **Đo lần sau (khi có ≥50 view/video):** `relPerf@60s` — ngưỡng khỏe **≥0,40** (health chết ở 0,10–0,14).

---

## 2026-07-25 (T7) — baseline #0, ngày kích hoạt kế hoạch 90 ngày

- Kênh: **0 sub · 5 view · 3 video public** (04 給付金 vừa lên 19:00 JST hôm nay).
- Video 01 (在職老齢年金, đăng 07-20): 3 view · 1 cmt · xem TB 5'46" = **42.8%** · nguồn: channel page 2 + search 1. Chưa có impressions/retention (thiếu data).
- Video 02 (繰り下げ, đăng 07-22): 2 view · xem TB 8'12" = **52.5%** · nguồn: subscriber 2. Chưa có impressions.
- **Chẩn: BỆNH 1 thuần (0 phân phối)** — đúng dự đoán. %xem 42–52% trên mẫu nhỏ = script khỏe, không phải vấn đề.
- Hành động đã quyết hôm nay: ✅ vá nốt tầng kênh (dòng lịch desc + rổ tag/hashtag 02/04 — xem `CHANNEL_BACKFILL_2026-07-25.md`) · ✅ lịch 3/tuần T2·T4·T6 19:00 sync 4 nguồn · ✅ video 05 đóng gói slot T2 27/07 · tiếp theo = ĐỔ VOLUME theo roadmap `02_CONTENT_PLAN.md` (ưu tiên #1: 定期便に載らない).
- Snapshot: `yt-dashboard\history\nenkin\20260725-192500_kenh.txt` (đầu tiên của kênh).
- Đọc lại lần tới: **T2 27/07** (check 🔥72h video 04 + xác nhận 05 đã lên đúng slot).
