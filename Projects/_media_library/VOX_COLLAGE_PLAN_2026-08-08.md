# MỔ VIDEO THAM CHIẾU + PHƯƠNG ÁN "COLLAGE HỒ SƠ" cho lớp vox (2026-08-08)

> User chê hiệu ứng vẽ bằng PIL: *"đường nét vẽ ra cũng xấu, mũi tên thô không mượt"*,
> đưa video https://www.youtube.com/watch?v=RaxX_Q7Apj0 (Jacksons AI, 18:40) bảo nghiên cứu.
> Đã xem trọn qua 117 frame storyboard L3 (playback + yt-dlp đều bị chặn; sprite
> `i.ytimg.com/sb/…` thì mở tự do — mẹo dùng lại được).

## 1. HỌ LÀM GÌ MÀ ĐẸP — kết luận mổ

**Không có một đường vector nào được code vẽ ra cả.** Toàn bộ "hiệu ứng" là VẬT THỂ
ANALOG nằm SẴN trong ảnh AI gen hoặc được ghép như đạo cụ thật:

| Thứ nhìn thấy | Bản chất |
|---|---|
| Mũi tên đỏ | nét **sáp/crayon vẽ tay** trên mảnh giấy xé — texture thật, đầu tù, nét run |
| Đường nối các ảnh | **DÂY CHỈ ĐỎ thật** căng giữa các đinh ghim (conspiracy board) |
| Khoanh tròn nghi phạm | vòng **bút sáp đỏ** nguệch tay, hở nét |
| Nhãn chữ (SCRAP/PARIS/LUSTIG) | chữ đóng trên **mảnh giấy XÉ** + băng dính + đinh ghim, có bóng đổ |
| Nhấn mạnh | **CON DẤU grunge** (ARCHIVED/SOLD) đóng chồm lên ảnh |
| Ảnh tư liệu | ảnh đen-trắng kiểu lưu trữ, viền trắng, dán lệch ±2–3°, bóng đổ thật |
| Nền | giấy kraft/bản đồ cũ, ố, gấp nếp |

**Pipeline của họ:** Claude viết beats + prompt hàng loạt → extension "ZAP FLOW" bơm
prompt vào **Google Flow (Veo/Imagen)** gen toàn bộ cảnh collage (ảnh + image-to-video
chuyển động nhẹ) → CapCut ghép + TTS CapCut + nhạc Suno. Chữ nhãn bake thẳng trong ảnh
AI — **ăn được vì tiếng Anh**; tiếng Nhật gen là nát chữ → mình KHÔNG bake chữ.

**Bài học gốc:** cái đẹp đến từ việc annotation là VẬT CÓ CHẤT LIỆU + BÓNG ĐỔ, không
phải nét vector 15px của PIL. Đường thẳng máy vẽ sạch đến mấy vẫn "PowerPoint".

## 2. PHƯƠNG ÁN CHỐT ĐỀ XUẤT — "PROP ENGINE" (collage hồ sơ, chữ thật)

Giữ phân công đã chốt (user gen ảnh, Claude hiệu ứng), đổi CÁCH làm hiệu ứng:

### 2a. Nền cảnh = ảnh AI (như đang làm, đổi style anchor)
Style anchor mới hướng "hồ sơ lưu trữ Nhật": 和紙/giấy kraft cũ + bản đồ/tài liệu cổ
làm nền, vật thể là ảnh cắt dán viền trắng lệch nhẹ, tông sepia + đỏ 朱色. Cấm chữ
trong ảnh như cũ.

### 2b. Đạo cụ (PROPS) — gen MỘT LẦN, dùng cả kênh
Bộ PNG trong suốt tại `_media_library/props/`, mỗi loại 3–5 biến thể (đỡ lặp):
- mũi tên **bút sáp đỏ** (thẳng/cong/gãy khúc) · vòng khoanh sáp đỏ · gạch chéo X
- **dây chỉ đỏ** + đinh ghim đầu tròn
- mảnh **giấy xé** trống (để tool ĐÓNG CHỮ THẬT Noto/handwriting lên) + băng dính washi
- khung **con dấu** trống (tròn/chữ nhật, mực đỏ lem) — tool đặt chữ vào giữa
- kẹp giấy, ghim, vệt ố cà phê
Nguồn: user gen theo prompt pack (nền trắng trơn) → rembg → sticker prep. Làm 1 lần.

### 2c. make_vox chuyển "vẽ" → "DÁN + LÀM ĐỘNG đạo cụ"
- `arrow()` → chọn prop mũi tên, xoay/scale theo 2 điểm, **reveal bằng mask wipe dọc
  thân** (nhìn như đang vẽ tay) — hết thô ngay vì nét là texture sáp thật.
- pin nhãn → chữ thật đóng lên giấy-xé prop + băng dính, **thả rơi 0.4s + bóng đổ
  co lại** (vật "đáp" xuống bàn).
- nhấn số/kết luận → **con dấu SLAM**: scale 1.6→1.0 overshoot + xoay ±4° + bụi mực.
- nối 2 vật → dây chỉ đỏ **căng dần** giữa 2 đinh ghim.
- khoanh đáp án → vòng sáp reveal theo góc quay.
- Chữ kicker/head/số: GIỮ font thật như hiện tại (không bao giờ bake chữ AI).
- Idle loop giữ nguyên kiến trúc (dây chỉ rung nhẹ, con dấu thở, bóng nhãn lắc ±0.3°).

### 2d. Vì sao hơn cả 2 đường cũ
- Hơn PIL vector: chất liệu + bóng + nét tay = hết "PowerPoint".
- Hơn bake-hết-vào-AI (kiểu video tham chiếu): chữ Nhật sạch 100%, annotation đặt
  ĐÚNG toạ độ theo lời thoại, sync cue được, deterministic + resume được, và không
  phải gen lại cả cảnh khi đổi 1 chữ.
- Compliance: giấy/dây/dấu là đồ hoạ, ảnh nền là minh hoạ/vật — không realistic người
  thật, không phải tick synthetic. Kênh kể chuyện co-dai hợp chất "hồ sơ cũ" sẵn.

## 3. VIỆC LÀM — ✅ XONG 2026-08-08 (cùng ngày)
1. ✅ Prompt pack: `props/PROPS_PROMPTS.md` + bản 1-dòng-1-prompt cho extension Flow
   `props/PROPS_PROMPTS_FLOW.txt` (20 prompt). User gen đủ 20/20.
2. ✅ Prep: `props/props_prep.py` → 20 PNG + INDEX.json (anchor tail/head cho mũi tên).
   ⚠️ Bài học: prop MỰC ĐỎ key theo **ĐỘ ĐỎ** (R − avg(G,B)) — key khoảng-cách-màu
   dính "bóng ma tờ giấy" khi raw gen trên giấy xám (2 vòng mới bắt được); vật đặc
   mới đi rembg. ⛔ Đừng rembg vết mực — nó ăn nét mảnh.
3. ✅ make_vox VERSION `vox-2026-08-08-props`: `prop_arrow` (chọn thẳng/cong theo bend,
   flip theo dấu, reveal wipe dọc trục = "đang vẽ tay") · `prop_label` (chữ thật trên
   giấy xé + pin/tape, thả rơi ease_back + bóng) · `prop_stamp` (slam 1.7→1 + chữ đục
   lỗ noise cho lem như dấu thật) · `prop_mark` ✗○ sáp · `prop_circle` reveal theo góc
   · `prop_string` dây chỉ + 2 đinh · `prop_decor` vết đời sống dưới SB. Thiếu props
   → tự rơi về vector cũ (kênh khác không gãy).
4. ✅ Demo 6 thẻ `youtube-jp-co-dai/06_VIDEO/_vox_ai_demo/` dựng lại bằng props —
   flow (nhãn ghim + mũi tên sáp) · timeline (2024 dấu chữ nhật) · source (169人 dấu
   tròn) · compare (✗○ sáp) duyệt mắt đạt.

## 4. Ghi chú kỹ thuật lượm được
- Xem video YouTube bị chặn playback/yt-dlp: lấy sprite storyboard
  `ytInitialPlayerResponse.storyboards…spec` → `https://i.ytimg.com/sb/<id>/storyboard3_L3/M<n>.jpg?sqp=…&sigh=rs$…` (tên file `M<n>`, không phải `<n>`).
- Video tham chiếu còn 1 video liên quan đáng xem sau: "AI Vox Style Motion Graphics
  Are Finally Usable (Gemini Omni)" — FRMWRKD-EXPLAINED.
