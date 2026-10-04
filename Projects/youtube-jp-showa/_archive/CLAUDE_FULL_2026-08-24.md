# CLAUDE.md — youtube-jp-showa

> Kênh ký ức 昭和 cho JP 50–70. Đọc cùng: rules toàn hệ thống (`.claude/rules/*`), `00_CHANNEL_BIBLE.md` (concept), `01_KEYWORD_RESEARCH.md` (số đo).

## Trạng thái setup (cập nhật 2026-08-14 — KÊNH ĐÃ LẬP THẬT)

> Bản setup đầy đủ (mô tả kênh, 22 keywords, rổ tag, prompt ảnh): **`07_CHANNEL_SETUP_2026-08-14.md`**

| Hạng mục | Trạng thái |
|---|---|
| Tên kênh | ✅ **昭和くらし図鑑** (user chốt 2026-08-02) — **đã đặt trên kênh thật 2026-08-14** |
| **Kênh YouTube thật** | ✅ **`UCT0CITcGxFErQk_YjQriZ_w`** · handle **`@showa-kurashi-zukan`** · 0 video. Lập bằng cách đổi tên brand channel trống "Gonn Sau" có sẵn |
| Mô tả kênh + từ khoá | ✅ mô tả 432 ký (10 keyword) · 22 channel keywords · quốc gia 日本 |
| Default upload | ✅ private · **cat 27 教育** · ngôn ngữ video + tiêu đề/mô tả = 日本語 · 12 tag nhận diện kênh · không dành cho trẻ em · bình luận Bật |
| **Avatar + banner** | ✅ **ĐÃ LÊN KÊNH 2026-08-14.** File gốc: `09_BRAND/avatar_A_terebi_800.png` (TV gỗ, chữ 昭和 trên màn hình, nền đỏ) + `09_BRAND/brand_banner_2048.png`. Xử lý + khiếm khuyết còn lại: `07_CHANNEL_SETUP_2026-08-14.md` §6.1–6.2. ⚠️ Chữ banner rộng hơn vùng an toàn (mobile xén ~102px đuôi subtitle) — đã sửa prompt cho lần gen sau, chưa gen lại |
| Gmail + Chrome profile | ✅ **`gonnsau@gmail.com`** / Chrome **`Profile 15`** (tên profile: *Gonn*) — **SỬA 2026-08-16, user chốt**. ⛔ Bản ghi cũ `saubeo.killuaa@gmail.com` / `Profile 9` là **SAI**: killuaa chỉ **CÓ QUYỀN quản lý** (thấy kênh trong `channel_switcher`), không phải chủ. ⚠️ killuaa vẫn là manager của các brand channel khác → cô lập chỉ ở tầng browser (`channel-browser.md` Mục 1) |
| Giọng TTS | ✅ **CHỐT 2026-08-02 (user chọn sau 4 vòng/14 giọng demo): 2 giọng** — trục A (ký ức) = **東北イタコ**/ノーマル/0.90 (VOICEVOX, profile `showa`) · trục B (値段/số) = **阿井田茂**/Calm/0.90 (AivisSpeech port 10101, profile `showa-b` — ⚠️ cùng người nói chouhen, user chấp nhận vì khác style + khác tệp). **1 video 1 giọng** — chọn profile theo trục của video. Render trục B: mở app AivisSpeech trước |
| Entry `channels.py` | ✅ 2 profile `showa`/`showa-b` thêm 2026-08-02 (kèm khóa `engine` mới trong FLAG_KEYS — kênh cũ không ảnh hưởng). ⚠️ BGM đang mượn tạm Wholesome của health + drawn kraft là TẠM — chốt khi duyệt demo video #1 |
| Entry `upload_pack.py` | ✅ thêm 2026-08-14 (`CHANNELS["showa"]`, có `channel_id`) — nhưng **`slots: []`**, xem dòng Lịch đăng |
| Nguồn ảnh tư liệu | 🔴 BÀI TOÁN SỐ 1 — chưa giải, xem §3 |
| Lịch đăng | ✅ **T3 · T5 · T7 @ 18:00 JST — 3 video/tuần** (chốt 2026-08-14 sau khi ĐO 9 kênh cụm 昭和 × 50 video). Bằng chứng: `.claude/rules/upload-schedule-measure-showa-2026-08-14.md`; đã áp vào `upload-schedule.md` Mục 0.9 + Mục 1 và `upload_pack.py`. **Bộ ngày C** (không thuộc A/B). Giờ 18:00 chứ không 19:00 để không chồng health+nenkin. ⚠️ Nhịp 3/tuần **ngược tín hiệu ngách** (3 kênh hiệu suất cao nhất đăng ≤1/tuần) — 🛑 phanh: 5 video đầu median ≤500 view + BROWSE=0 → hạ về 1/tuần T5. Đè bỏ "tạm định 2/tuần 19–20h" cũ |

## 1. Luật nội dung (khác chuẩn hệ thống ở đâu thì ghi ở đây)

1. **3 trục cố định** (chi tiết `00_CHANNEL_BIBLE.md`): A vật phẩm 60% · B vật giá/lương (moat, genten bắt buộc) 30% · C essay tentpole 10%. KHÔNG làm video nhạc.
2. **Cold open = nostalgia trigger, KHÔNG phải loss-aversion.** Câu 1 = bắn thẳng 1 vật gây 「あっ、あった！」 trong 15s. Đây là NGOẠI LỆ có chủ đích so với memory `feedback_mo_dau_danh_vao_noi_so` (khuôn sợ hãi là của kênh tiền/sức khỏe — ngách hoài niệm chạy bằng ấm áp + tò mò "còn nhớ không"). Gate vào vật đầu tiên ≤60s vẫn giữ.
3. **Title công thức (⭐ tag đầu ĐỔI 2026-08-20, user chốt: *"tôi muốn title có dạng showa 101"*):** **`【昭和101年】` + chủ đề + liệt kê tên vật phẩm** (lưới long-tail — mỗi tên vật là 1 cửa suggested; phần thân giữ nguyên công thức 記憶装置, chỉ đổi tag đầu từ 【懐かしい昭和】).
   - **Nghĩa của tag:** "nếu niên hiệu còn tiếp tục thì năm nay là năm 101" — cách đếm 昭和元年=1926 ⇒ 昭和N年 = 1925+N ⇒ **2026 = 昭和101年**. Bằng chứng khung: video **top-1 scan ngách 90 ngày** 「存在しないのに懐かしい、**昭和101年**の…空中都市」 = 577.610 view (`06_VIDEO/_niche_scan/scan_showa_90d.txt`).
   - 🔴 **Tag ăn theo NĂM ĐĂNG — 2027 phải đổi `【昭和102年】`.** Đây là title có hạn dùng; đầu mỗi năm sửa dòng này.
   - ⚠️ **Keyword ĐO ĐƯỢC của Trends vẫn là `昭和100年`** (breakout #1, đo 08-02) — `101年` là KHUNG title, không phải keyword; giữ `昭和100年` trong tag/hashtag/概要欄, đừng thay nó bằng 101年 ở các tầng SEO.
   - Tag là **FORMAT kênh** ⇒ cả 3 title A/B cùng mang tag, biến thử là phần thân (`ab-3title-3thumb` §2.2).
   - Video 01 (給食) đã đăng với title cũ — **không sửa video live** trừ khi user yêu cầu (đổi title = `videos.update`, phải chốt trước).
   - Ca áp đầu tiên: video 02 (`03_SCRIPTS/02_kieta-mise.md` §Title CHỐT).
4. **Tên sản phẩm/thương hiệu cũ (チェルシー・ビックリマン…): ĐƯỢC DÙNG** — retrospective trung tính là chuẩn ngách (benchmark 88 video công khai). Ranh giới: nói về SẢN PHẨM & ký ức; KHÔNG bôi nhọ/bịa chuyện về công ty; không nói gì về doanh nghiệp hiện tại. (Ngoại lệ có chủ đích so với câu "không tên thương hiệu" trong youtube-compliance §5 — câu đó nhắm drama bôi nhọ.)
5. **外来語 60s đầu:** tên vật katakana thời 昭和 là TÊN RIÊNG khán giả tự biết → dùng được, chính nó là trigger. Vẫn cấm 外来語 thuật ngữ hiện đại + tiếng trẻ (バズる…).
6. **Trục B bắt buộc nguồn:** số tiền nào lên hình phải có nguồn (総務省統計局・日銀・週刊誌 thời đó) + năm. (Lớp thủ công/notebook đã bỏ 2026-08-09 — yêu cầu nguồn giữ, cách thể hiện tự do.) Quy đổi 「今の価値で約◯円」 dùng CPI 総務省 — ghi cách tính vào script.
7. **Quiz/đố giá** là cơ chế retention chủ lực trục B: hỏi giá → giữ đáp án sau 2–3 beat → drawn card lật đáp án.

## 1.5 Thumbnail — khuôn **K-COLLAGE** (chốt 2026-08-18)

**Khuôn của kênh nằm ở `03_THUMBNAIL_FORMULA.md`** — đọc file đó trước khi viết prompt thumbnail, đừng tự chế khuôn mới. Tóm:

- **Collage nhiều ô** ngăn bằng khe trắng + viền trắng dày · các ô **sepia/umber** trừ **đúng 1 ô MÀU RỰC** (vật chính) · hero 2 dòng cắt ngang giữa.
- **4 khối chữ cố định:** chip `全◯品` (số lượng) · banner `昭和40年〜50年代` (mốc) · hero dòng 1 trắng `今では消えた` · **hero dòng 2 ĐỎ, TO NHẤT = chủ đề + keyword đo được cao nhất**. Trần 4 khối, **không có dải đáy** ⇒ câu hỏi ngược chuyển về đuôi title + pinned comment.
- Số đo: hero dòng 2 **cao ~1/3 khung · rộng ~3/4** · banner cao ~1/6 gần full-width. Ép bằng **quan hệ với mép khung**, không tả phần trăm.
- ⚖️ **Ngoại lệ có chủ ý với `audience-45plus` §1 gate 6** (nền tối) — 4 điều kiện bù ở `03_THUMBNAIL_FORMULA.md` §3, trong đó cứng nhất: soi 120px hero phải đọc được đầu tiên, chìm thì **gen lại**, không bóp chữ nhỏ.
- ⛔ Cấm `8mm/faded/vignette` phủ cả khung (đo được: ra trường bỏ hoang) · cấm để model tự viết nhãn trong ô (đã dính: nhãn lặp + gắn nhầm món) · cấm `総集編` nếu video không phải tổng hợp.

## 2. Compliance riêng ngách

- **⛔ CẤM phát nhạc 昭和歌謡/CM song thật** — kể VỀ nhạc thì được, phát thì không (Content ID + mất ad). BGM: orgel/acoustic free −40dB chuẩn hệ thống.
- **TÔNG CHỦ ĐẠO (user chốt 2026-08-02 sau khi so 3 bản demo): PHIM MÀU HOME-MOVIE THẬT kiểu Koshell (Ektachrome/Kodachrome)** — vỉa nguồn: Prelinger home movies Nhật (Koshell 1963 · Koura 1952–55 · Muraoka mid-50s, đều MÀU). Đen trắng nguyên bản = beat "thời khó"; AI tô màu (`tools/colorize_test.py`, cv2 4.11 + Zhang2016) = gia vị có nhãn 「※AIによりカラー化」. Kỹ thuật scan phim: **crop lọt lòng khung `crop=500:281:70:100` → scale 1920×1080** (bản scan Prelinger để nguyên lỗ răng phim); mẫu chuẩn: `06_VIDEO/_footage_test/koshell_japan/demo_koshell_matsuri_street.mp4`. ⚠️ License Prelinger home movies không ghi field → PHẢI verify statement trang item + credit ATTRIBUTIONS trước khi ĐĂNG.
- **Visual (ĐẢO LẦN 3 — 2026-08-07, user chốt sau khi xem bản render 01 và chê cả 4 mảng):** **~55% ảnh AI TĨNH** (Gemini gen master theo STYLE LOCK 8mm/Kodachrome `04_VIDEOGEN_PROMPTS.md` §1 + pan + `grade_vintage.py`) làm dòng chảy + **~25% ảnh THẬT PD/CC** đúng vật, mỗi ảnh 1 LẦN + **drawn card + thẻ genten + 2–3 clip PD** (Prelinger/phim chính phủ Mỹ — luật cũ về phim PD giữ nguyên: mute nhạc, verify statement từng cuộn). ⚠️ **Kênh này TICK "altered/synthetic" mọi video có ảnh AI** — là NGOẠI LỆ của trạng thái "không kênh nào phải tick" trong youtube-compliance §2 (user chấp nhận 2026-08-07). Lý do đảo: bản render 01 v2 footage-first chứng minh nguồn PD quá mỏng (16 ảnh/47 slide, ảnh lặp 5 lần, script cắt 15′→9′). SFX hoài niệm tự chế giữ nguyên; ⛔ NHẠC trong phim PD vẫn cấm.
- **Ảnh thật chỉ PD/CC** + credit đúng license vào ATTRIBUTIONS.md. ⛔ KHÔNG bốc ảnh blog/Twitter/まとめ hoài niệm — bẫy bản quyền lớn nhất ngách.
- ⭐⭐ **CỐT LÕI VISUAL (chốt 2026-08-21, TÁI XÁC NHẬN 2026-08-22 sau video 03, user: "ghép nhiều video thật là tốt nhất, mở đầu lúc nào cũng phải là video thật… phải có tiếng thật nhé"):** phim tư liệu THẬT (PD/CC0, `06_VIDEO/_footage_test/FOOTAGE_GO_NO_GO.md`) luôn là lựa chọn số 1, đứng trên ảnh AI. **Cold open của MỌI video BẮT BUỘC dùng clip phim thật** nếu kho đã có đoạn hợp cảnh — chỉ rơi về ảnh AI khi kho thật sự không có gì khớp (ghi rõ lý do vào Ghi sổ GĐ). Ngoài cold open, **ghép thêm phim thật ở càng nhiều chỗ càng tốt** — ảnh AI chỉ lấp chỗ kho thật không phủ tới. **Mọi clip phim thật PHẢI có SFX** (xem mục ngay dưới) — không có ngoại lệ "chỉ cold open mới cần tiếng". Đây từng chỉ là quyết định một-lần cho video 02, nay là luật đứng cho cả kênh.
  - **Quy trình đã chạy được ở video 03 (mẫu để lặp lại):** ① soi `FOOTAGE_GO_NO_GO.md` tìm clip đã verify license khớp cảnh ② **kho hiện có không đủ → chủ động MỞ VÒNG TÌM NGUỒN MỚI** (không dừng lại ở "kho không có" — quét thêm archive.org bằng `advancedsearch` API lọc `licenseurl`, quét frame 10s/20s/2s thu hẹp dần để tìm đoạn hợp cảnh trong 1 cuộn dài) ③ mỗi clip cắt xong PHẢI kiểm span thoại nó cần phủ (`subs.srt`) — span dài hơn clip → **KHÔNG dùng `-stream_loop`** (gây lặp lộ liễu), mà **trích khung hình tĩnh ngay từ chính clip đã grade** làm ảnh nối tiếp (đóng băng đúng màu/tông, không cần gen ảnh AI mới) ④ nếu 1 clip vẫn phải lặp thì tách nhỏ TTS line để giảm span cần phủ xuống gần bằng độ dài clip (lặp <1,5× coi là chấp nhận được, ≥2× thì phải sửa).
  - **Tỉ lệ đạt được ở video 03: 3 clip thật / 36 entry** (~8%, thấp — kho JP-classroom-1941 chỉ cho đúng 2 đoạn hợp cảnh dài khoảng 10s mỗi đoạn). Đây KHÔNG phải trần — chỉ là giới hạn của MỘT nguồn đã tìm; video sau nếu mở thêm vòng tìm nguồn (nhiều cuộn phim PD khác nhau, không chỉ 1–2 cuộn) thì phải đẩy tỉ lệ này lên, đừng dừng lại ở "đã có 1 clip cold open là đủ".
  - ⭐ **TRẦN ~6 GIÂY/FRAME (chốt 2026-08-22, user: "tầm 6s phải đổi frame 1 lần"):** không entry/khung hình nào (ảnh AI, ảnh tĩnh trích từ clip, hay một pha pan) được đứng yên quá ~6 giây — thấy TTS line nào cần phủ dài hơn thì **chia nhỏ thành nhiều entry/pan** thay vì để một hình kéo dài (video 03 từng có slide giữ tới 44,9s và 48,1s trong lúc build chunk — đúng kiểu phải tránh). ⚠️ **Đè trực tiếp lên trần hệ thống `audience-45plus.md` §2 ("≤6 lần đổi hình/phút" ≈ ≥10s/entry) — đây là NGOẠI LỆ CHỈ CHO showa**, vì ngách hoài niệm 昭和 cần nhịp đổi hình khá hơn (nhiều đồ vật/khoảnh khắc lướt qua) để không lê thê. Muốn giữ đúng "≤6 đổi hình/phút" đồng thời với trần 6s/frame thì phải bù lại bằng clip phim thật đủ dài xen giữa (đúng tinh thần "ghép phim thật càng nhiều càng tốt" ở trên) — hai luật này ăn khớp nhau nếu tỉ lệ phim thật đủ cao, xung đột nếu toàn ảnh AI tĩnh.
  - **Khi cold-open clip bị chê "giống clip khác" / lặp lại:** đổi sang đoạn khác trong CÙNG nguồn đã verify (nhanh hơn tìm nguồn mới) — quét lân cận theo bước 0.5s để tìm ranh giới cắt cảnh sạch (nhìn contact sheet nhiều khung liên tiếp, đừng tin 1 frame đơn lẻ vì có thể trúng giữa một pha chuyển cảnh nhanh).
- ⭐⭐ **MỌI CLIP PHIM TƯ LIỆU THẬT PHẢI ĐƯỢC GHÉP SFX (chốt 2026-08-22, user: "làm tương tự đi và làm cho những video sau đi").** `cut_archival.py` luôn MUTE phim gốc (`-an`, đúng luật — tiếng/nhạc gốc là quyền riêng, tách khỏi quyền hình PD). Nhưng KHÔNG được để clip câm lặng trong bản final — phải ghép SFX thật (không phải nhạc) khớp đúng nội dung cảnh, lấy từ **pocket-se.info** (đã dùng ở video 02: kèn đậu phụ + tiếng đặt chai; license: kiếm tiền OK, cắt/sửa OK, **bắt buộc credit** khi free — dò trực tiếp bằng URL dạng `pocket-se.info/se/<tên>.mp3`, đọc `ご利用規約` trước khi dùng). Quy trình chuẩn (video 03 là ca đầu áp full):
  1. Tìm ảnh/âm khớp NỘI DUNG cảnh (không phải mood chung chung) — vd cảnh học sinh đi trên đường sỏi gần đền/vườn → tìm đúng "tiếng bước chân trên sỏi" chứ không lấy tiếng bước chân bất kỳ.
  2. Trộn bằng post-process RIÊNG sau khi `video_render.py` xong (không sửa pipeline chính) — `-map 0:v -c:v copy` giữ nguyên hình, chỉ re-encode audio, amix SFX vào đúng timestamp (tra bằng `subs.srt`, tìm dòng khớp `match` của clip đó).
  3. Gain SFX thấp hơn giọng đọc rõ rệt (tham khảo video 02: mix ở mức nghe thấy nhưng không cạnh tranh với TTS) + fade in/out 0,5–1s để không giật cụt.
  4. **CREDIT BẮT BUỘC** vào 概要欄 + `ATTRIBUTIONS.md`: 「効果音：ポケットサウンド – https://pocket-se.info/」 (gộp chung 1 dòng dù dùng nhiều file).
  5. Không tìm được SFX khớp đúng cảnh → **để câm hơn là ghép SFX sai cảnh** (vd đừng lấy tiếng chim rừng cho cảnh trong nhà) — thà thiếu còn hơn lạc quẻ.
  6. 🔴 **ĐỔI CẢNH THÌ PHẢI ĐỔI SFX THEO — đừng để SFX cũ ăn theo cảnh mới đè lên.** Video 03: đổi cold open từ "học sinh đi bộ đông người" sang "kệ giày trống" mà quên đổi SFX (`sandougaya.mp3` — sỏi + tiếng người lao xao, hợp cảnh CŨ, sai hoàn toàn với cảnh MỚI) — phải đổi cả 2 cùng lúc, không chỉ đổi hình.
  7. 🔴🔴 **GAIN PHẢI TÍNH THEO HEADROOM CÒN LẠI CỦA TỪNG FILE NGUỒN, KHÔNG BOOST ĐỒNG LOẠT MỘT SỐ dB.** Bài học video 03: boost `volume=+8~+14dB` đồng loạt cho mọi SFX (để sửa lỗi "quá nhỏ") gây **CLIP THẬT** — đo `astats reset=0` ra `Peak level dB: +7,0` (vượt hẳn 0dBFS) vì 2 file SFX nguồn (`keyopen.mp3`/`dooropen6.mp3`) **đã có max_volume riêng gần 0dB** (transient ngắn, thu sát full-scale), cộng thêm dB dương là clip chắc chắn bất kể mix với gì.
     - **Cách làm đúng:** đo `ffmpeg -af volumedetect` (hoặc `astats reset=0`) từng file SFX TRƯỚC khi ghép để biết `max_volume`/`Peak level` — file nào đã gần 0dB thì **giữ nguyên hoặc chỉ trừ nhẹ** (0 đến −1dB), chỉ file nào còn nhiều đệm (vd max −6dB) mới boost, và boost ≤ đệm còn lại trừ hao 1–2dB an toàn.
     - **Luôn thêm `alimiter=limit=0.97` (hoặc tương đương) ở cuối chuỗi `amix`** làm lưới an toàn cuối — rẻ, không ảnh hưởng chất lượng khi không cần dùng tới, cứu được khi nhiều SFX chồng thời điểm cộng dồn vượt 0dB.
     - **Đo LẠI sau khi ghép** (không chỉ tin số gain đã đặt): `Peak level dB` phải **âm** (< 0), không chỉ nhìn `mean_volume` tăng lên là đủ — RMS tăng mà peak vượt 0dB vẫn là rè, tai người nghe ra ngay dù máy đo trung bình có vẻ "ổn".
- Chủ đề 事件/ヤンキー/校内暴力: viết được nhưng quét từ nhạy title/thumbnail gắt theo youtube-compliance §3.
- Video nói về người thật còn sống (nghệ sĩ CM…): chỉ facts công khai, không đời tư tiêu cực.

## 3. Bài toán mở — NGUỒN ẢNH 昭和 (chặn sản xuất, giải trước video #1)

Chưa có lời giải verify. Hướng dò: Wikimedia Commons (Category theo thập kỷ JP, PD-Japan), 国立国会図書館デジタルコレクション, Flickr Commons, 広報 ảnh chính quyền cũ, ảnh chụp sản phẩm cũ tự tạo, drawn card thay ảnh khi không có. **Việc đầu tiên của giai đoạn sản xuất: test fetch đủ ảnh cho 1 video 給食 → mới biết ngách này sản xuất được thật hay không.**

## 4. Nhắc chuẩn hệ thống áp nguyên (không chép lại)

45+ rules (thumbnail ≤6 ký/mặt-hoặc-vật to · nhịp ≤6 hình/phút · phụ đề pill ≥22 · 15–30′) · humanize ≥4/6 mũi + 15–25 tag giọng · CTA giữa video (viết câu canonical riêng kênh khi chốt persona, thêm vào cta-midvideo.md §2) · render nền + resume mtime · upload SEO (đo trend trước khi đóng gói) · media-library (không tái dùng asset, hình đầu = chủ đề — kênh này là kênh THÔNG TIN, áp §2.0).

> 📦 Doc cũ (diagnosis/optimize/benchmark hết hạn, khuôn đã bị đè) đã dời vào `./_archive/` (dọn 2026-08-24) — đường dẫn cũ trong rules trỏ file nào không thấy ở gốc thì tìm ở đó.
