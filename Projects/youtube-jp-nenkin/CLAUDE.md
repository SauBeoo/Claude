# CLAUDE.md — youtube-jp-nenkin (bản rút gọn 2026-08-24)

## ① IDENTITY
- Kênh **年金と老後のお金研究室** — tệp JP 50–70, đề tài 年金・給付金・税 của CHÍNH người xem.
- Persona: **案内役/nghiên cứu viên điềm đạm** (研究室, xưng 当研究室/私たち); KHÔNG xưng FP/chuyên gia có phép.
- **3 trụ khóa, không mở rộng:** ① 年金 tính số ② 給付金・取り逃し ③ 税・社会保険料. ⛔ Cắt 不動産/金融商品/iDeCo/NISA; 介護 tiền CỦA BỐ MẸ → kênh `kaigo` (nenkin chỉ giữ 介護保険料 của người xem).
- **Cast モニター cố định** (tái xuất xuyên video, số liệu đời không tự đổi — muốn đổi phải có lý do cốt truyện): 田中(67 横浜) · 佐藤(66 仙台) · 鈴木(65 名古屋) · 高橋(65 東京) · 山田夫妻(67&65 大阪) · 伊藤(68 福岡) · 松本(60 千葉) · 渡辺(66 新潟市, thu nhập thấp/支援給付金) · 中村(71 上越市3級地, dải biên 非課税) · **小林(75 埼玉県川口市, 74歳まで会社員の息子の健康保険の被扶養者 ⇒ 保険料0円、75歳で元被扶養者の5割軽減、2年で切れる — thêm ở v28)**. Hồ sơ số chi tiết: `_archive/CLAUDE_FULL_2026-08-24.md` §SIGNATURE.
  - ⭐ **Thêm ở v29 (cặp 対決, dùng chung cho mọi đề 保険証/医療):** **原田(84・千葉県船橋市, 団地4階, 高血圧で月1回通院, マイナ保険証を毎回利用 ⇒ 資格情報のお知らせ)** · **小川(84・同じ階, ほとんど通院なし・去年2回 ⇒ 資格確認書)**. Hai người **cùng tuổi, cùng toà nhà, khác đúng MỘT biến** (số lần dùng) — lập ra để chạy ranh giới 「6回」 mà không cần bịa thêm dữ kiện nào.
  - ⭐ **Thêm ở v30:** **加藤(72・新潟市, 年金 年132万=1回22万, 本人非課税; tới 2026年3月 sống cùng 次男 (会社員・課税) → 3月末 次男 chuyển công tác lên 東京, chuyển cả 住民票 ⇒ 4月1日 hộ một mình ⇒ 介護保険料 第5段階 82.500 → 第3段階 53.700, tháng 10 nhận NHIỀU hơn 9.600円)**. Chi tiết đời: vẫn nấu 3合 cơm rồi chia đông lạnh · lịch bếp, 次男 gọi điện Chủ nhật. Cast dùng lại cho mọi đề **世帯の変化 × 保険料/非課税**. ⓘ Lý do lập mới: case "phía TĂNG" cần đổi hộ trước 4/1; 渡辺 canon (v10) chỉ có lý do bỏ part-time, và tính đúng chú thích bảng 新潟市 (給与所得 −10万 cho 第1–5段階) thì 渡辺 ở 第2段階 cả hai năm ⇒ không dùng được.
  - ⭐ **Thêm ở v31:** **木村さんご夫妻(大阪市・1級地)** — ご主人 **68**, 元・印刷会社勤め, 年金 **年190万** (chỉ lương hưu ⇒ 所得80万) · 奥さま **66**, 国民年金 **400か月** ⇒ **年706.083円** (所得0), nhận **支援給付金 月4.683円**. Hộ **世帯全員非課税** nhờ khai vợ (đường 大阪市 1人 = 101万); không khai thì đường 45万 ⇒ ご主人 課税 ⇒ 介護 第4→第7 (+46.060) · 奥さま 第2→第5 (+57.159) · 給付金 −56.196 ⇒ **年15万9千415円** (7割 phía vợ). Chi tiết đời: phong bì kẹp dưới dây buộc bó báo cũ · viết bằng kính lão ở bàn ăn · vợ lặng lẽ rót trà. Cast dùng lại cho mọi đề **夫婦 × 非課税判定 / 配偶者控除 / 支援給付金**. ⓘ Lý do lập mới: roster không có cặp vợ chồng nào mà chồng **không đi làm** và 所得 nằm giữa 45万–101万 (山田 chồng còn tái tuyển dụng · 高橋 所得130万).
  - 🔴 **Thêm cast thì PHẢI thêm cả vào tuple `CAST` của `tools/check_pace.py`.** Bản sao tay đó đã trôi: 小林 lập ở v28 mà không được thêm, nên v28 chỉ qua G9 nhờ 中村; thiếu thì G9 báo `0:00 = không thấy nhân vật nào`. Đã vá 2026-09-21 (thêm 小林・原田・小川).
  - ⓘ **Vì sao thêm cast mới ở v28:** bảng cũ **không có ai ≥75 tuổi** (già nhất là 中村 71), mà v28 nhắm đúng mốc 75歳. Bịa tuổi mới cho cast cũ là phá luật "số liệu đời không tự đổi" ⇒ lập nhân vật mới. 小林 là cast **dùng lại được** cho mọi đề 後期高齢者医療 · 資格確認書 · 高額療養費 70歳以上 về sau.
- Signature: 「研究ノート」 slide tổng kết cuối · câu kết 「それでは、また次回の研究でお会いしましょう。」 · sổ xoay 5 khuôn mở bài + 5 khuôn 計算タイム (không lặp khuôn video liền trước).
- **categoryId 27** · 12 tag nhận diện + 3 hashtag cố định (`#年金 #老後のお金 #年金と老後のお金研究室`).
- **Độ dài chuẩn 13–17′** ≈ 4.300–5.300 ký thân đọc (~5,72 ký/s + 0,45s/dòng + 1,0s/đoạn). Đo: `python tools/make_tts.py <stem> --dry`. Lịch: T3·T5·CN 19:00 JST (`upload-schedule.md` §0.9).

## ② SẢN XUẤT — KHUÔN CHỐT TỪ VIDEO 27 (2026-09-17)

> 🔴 **Toàn bộ khuôn hình cũ ĐÃ XOÁ khỏi file này** (user: *"cái cũ thì xóa đi"*): lớp sân khấu
> `make_stage` · đường Remotion `remotion-vox` · vox paper-collage · footage Veo/i2v · khuôn
> telop-mascot. Chúng bị đè vì **số đo**, không phải vì chán: mổ 3 kênh 年金 đang thắng
> (`CHANNEL_BENCHMARK_3video_2026-09-17.md`) rồi đo lại v26 của mình cho ra bảng dưới.
> Cần tra lại bản cũ → `git log -p CLAUDE.md`.

| | v26 (khuôn cũ) | 3 kênh thắng | **v27 (khuôn này)** |
|---|---|---|---|
| clip AI | **61 clip × 8s = 62% thời lượng** | 0% | **0** |
| MAD (độ động khung) | **9,97** | 1,06–4,28 | **1,12** |
| giữ mỗi hình | 0,5s | 4,0–16,5s | 11,0s |
| nền sáng / lệch | 175 / 43,4 | 201–223 / 8–33 | **221 / 3,3** |
| true peak | −1,2 | −5,4…−6,3 | −3,6 |

### Chín bước, chạy đúng thứ tự

| # | Bước | Lệnh / file |
|---|---|---|
| 1 | Script + `_TTS.md` | skill `script-nenkin` → `python tools/check_pace.py <stem>` phải **đạt hết 23/23** |
| 2 | **Voice + timeline một lượt** | `06_VIDEO/<stem>/run_voice.cmd` → `tools/make_timeline_exact.py`. ⛔ Không dùng cặp `synth_voice_full`+`make_timeline` (lệch dồn +8,6s) |
| 3 | **Scene plan** | `tools/plan27.py` → `plan27.json`. Gom dòng thành **ô ~10s**, không cho ô vắt qua ranh giới chương, gộp ô <6s, chẻ ô >18s |
| 4 | **Prompt ảnh** | `tools/img27_prompts.py` → `img27_FLOW.txt` (1 prompt/dòng). Hai style: ô có giấy tờ dùng `STYLE_PRINT`, còn lại cấm chữ |
| 5 | **Xoá watermark** | ⭐ `tools/strip_wm_crop29.py` — **CẮT** 0,905W + trim 16:9, tự **chừa ảnh 原典**. ⛔ Đừng vá bằng snap-màu: 3 vòng đều hỏng (`media-library.md` §2.10 6e). Nghiệm thu = sheet crop 1:1 + MẮT, **log "đã vá N/N" là lời khai, không phải bằng chứng** |
| 6 | **Ghép ảnh vào ô** | `tools/ingest_art27.py` → `art_final/shot_KKK.png`. Phải in **"ảnh bị dùng lại: 0"** |
| 7 | **Telop** | `tools/telop27.py` — chữ rút TỪ CHÍNH lời đọc, ⛔ không thêm số mới. ⭐ **Số viết Ả-rập + mỗi ô một thẻ phụ** — xem luật 7 của Lớp hình |
| 8 | **Dựng** | `run_build27.cmd` → `tools/build27.py` (ffmpeg thuần, chạy nền). Rồi **`python ../_media_library/check_motion.py <mp4>` phải SACH 5/5** |
| 9 | **Đóng gói** | `upload_pack.py --channel nenkin --slot "<ngày> 19:00"`. 🔴 **Viết 目次 SAU khi render**, mốc lấy từ `subs.srt` của chính bản mp4 đó (`youtube-upload-seo.md` §6) + rà khối credit (§6.1) |

### Lớp hình — 7 luật

1. **0 clip AI.** Ảnh tĩnh, style **vector phẳng kiểu clip-art công ích Nhật**, nền kem `#F6F1E4`
   một tông, đúng 3 màu + kem (navy `#1F3864` · đỏ `#C0392B` · teal `#3E7C78`), không đổ bóng.
2. **CHỮ LÀ CHÍNH, ảnh là minh hoạ.** Cột chữ trái ~55% khung · ảnh gọn trong ô phải 45%.
   ⇒ Đây là điều **3 kênh thắng đều làm** và v26 làm ngược (ảnh phủ khung, telop nhỏ trên đỉnh).
3. **Ảnh ĐỨNG YÊN TUYỆT ĐỐI** (pan = 0). Hiệu ứng dồn vào lúc **chữ vào**: chữ trượt 26px + hiện
   dần 0,30s · thẻ phụ trượt 18px lệch nhau 0,45s · **vòng khoanh đỏ vẽ dần bằng 4 cung** ·
   chuyển ô **dissolve 0,35s**.
4. **Chip chương đánh số góc trên-trái MỌI khung** + màn 「本日の流れ」 nhắc 2–3 lần giữa bài.
   Thứ này 完全攻略 (445K view/video) có mà workspace chưa kênh nào có.
5. **Phụ đề đổi theo TỪNG DÒNG lời đọc**, không phải một câu cho cả ô. Căn giữa trong vùng
   **từ x=250** (nút SUBSCRIBE chiếm góc trái dải phụ đề).
6. **Canvas lấy đúng màu nền của chính ảnh** (`im.getpixel((6,6))`), không dùng hằng số — ảnh gen
   ra nền 244–245/234–238/212–216 còn hằng số là 246/241/228, lệch 10–16 ở kênh B là hiện **khung
   chữ nhật** quanh ảnh.

7. ⭐⭐ **SỐ LIỆU PHẢI VIẾT BẰNG CHỮ SỐ Ả-RẬP, VÀ MỖI Ô PHẢI CÓ THẺ PHỤ** (user chốt 2026-09-21:
   *"Video của tôi text nhiều quá số liệu ít quá"* → *"các ảnh thêm nhiều số liệu và chi tiết hơn"*).
   🔴 **Nguyên nhân gốc KHÔNG phải bài thiếu số — mà là CÁCH VIẾT số.** v29 viết telop theo lối văn:
   「八月一日」「三つ」「一割ではなく十割」「二本」. Lên hình, mắt đọc ra **CHỮ**, không nhìn ra **SỐ
   LIỆU**. Đo trên bản đầu: chỉ **16/93 ô** có chữ số Ả-rập, **15/93** có thẻ phụ — trong khi lời đọc
   đầy số. Đó là lý do v29 trông "ít số" hơn v27/v28 dù nó nói NHIỀU số hơn.
   ⇒ **① số là lượng/ngày/tỉ lệ thì viết Ả-rập**: `8月1日から / 2つに` · `1割ではなく10割` ·
   `12か月に / 6回以上` · `分ける線は 2本` · `4問だけ`.
   ⇒ **② mỗi ô thêm THẺ PHỤ chở dữ kiện thứ hai của CHÍNH câu đang đọc** — đây là chỗ duy nhất
   trong khuôn đặt được số thứ hai mà không phá trần 9 ký của dòng chính.
   ⚖️ **Mọi số lấy từ chính lời đọc của ô đó, ⛔ không một số mới nào** (YMYL §③ — telop là văn bản
   công khai y như 概要欄).
   📐 Trần đo trên khung 1920: **big ≤9 ký** (font 108; 9 ký chạm x≈1.068, mép ảnh phải ~x=1.050) ·
   **sub ≤14 ký** (font 50) · **tối đa 3 thẻ** (thẻ thứ 3 kết ở y=790, dải phụ đề bắt đầu y=930).
   ✅ Kết quả v29 sau khi áp: chữ số Ả-rập **16→47/95** · ô có thẻ phụ **15→88/95** · tổng thẻ **15→100**.
   🔧 Thi hành bằng bảng `ENRICH` ở cuối `tools/telop29.py` (khoá theo **cue văn bản**, không theo
   chỉ số ô), gate tự kiểm: `python tools/telop29.py` phải ra `dòng >9 ký: 0` và `ô CÓ SỐ mà không
   có cue: 0`.

### Lớp brand — GIỮ NGUYÊN, chỉ đổi 3 số (user chốt 2026-09-17)

`BrandOverlay` của v26 có gì thì v27 có nấy: **logo 研究室 góc trên-phải (cao 110)** · **cú động
`owl_idle` 192 frame** · **SUBSCRIBE đỏ `#E12B2B` nảy 1,12× chu kỳ 4s**. Ba số đổi theo yêu cầu:
`OWL_H 300→210` · `BOT_MASCOT 186→158` · `BOT_SUBS 200→46` (nút gọn trong dải phụ đề), con trỏ
**đứng yên cạnh nút**, bỏ đoạn trượt.

### Prompt ảnh — luật đắt nhất

🔴 **CẤM CHỮ TOÀN CỤC LÀ SAI.** Bản đầu bắt mọi ảnh `NO TEXT` ⇒ tờ 通知書 trắng trơn không còn là
thông báo, sổ ngân hàng trắng trơn không còn là sổ — **vật mất lý do tồn tại**, người xem không
hiểu ảnh nói gì. Tách đúng hai loại chữ (`ai-video-regen.md` §1):

| | |
|---|---|
| ❌ vẫn cấm | chữ/số **đọc ra được** — kanji gen nát, số sai là vi phạm YMYL. Số liệu do **font** vẽ |
| ✅ **bắt buộc** ở ô có giấy tờ | **chữ texture li ti không đọc nổi** + dòng kẻ mờ + vài ô vuông. *"Tờ giấy trắng là SAI"* |

⭐⭐ **ĐẢO CHIỀU 2026-09-18 (user: *"tao muốn prompt text phải có chữ đọc được. Bỏ hẳn cái
required text trắng trơn đi cho tao"*) — hàng ❌ ở trên KHÔNG còn áp cho CHỮ, chỉ còn áp cho SỐ.**

| | từ v28 |
|---|---|
| ô **KHÔNG** có giấy tờ | cấm chữ tuyệt đối — **giữ nguyên** |
| ô **CÓ** giấy tờ | ⭐ **XIN chữ Nhật ĐỌC ĐƯỢC**: `style_text(LABEL[k])` — 1 cụm/ảnh · **≤7 ký full-width** · danh từ (tên giấy tờ/cơ quan) · câu chốt `PERFECTLY FORMED, CRISP AND LEGIBLE` ở cuối |
| **SỐ / ngày / %** | ⛔ **VẪN CẤM ở MỌI ô** — do **font builder** vẽ đè |

🔴 **Vì sao giữ ranh giới SỐ khi đã mở cho CHỮ** (không phải dè dặt, là số đo): memory
`feedback_so_tren_hinh_phai_do_font_ve` — Veo/Flow sai dấu phẩy hoặc **rụng một chữ số ~1/3 lần**,
đã thử **4 vòng prompt không chữa được**. Chữ thì ngược lại: workspace đã bake kanji **đạt** ở
chouhen 20 · health 24 · co-dai 16/17 · nenkin 09. ⇒ Hai loại ký tự có tỉ lệ hỏng khác hẳn nhau,
nên tách. Muốn mở cả số thì phải có ca đo được, đừng suy từ việc chữ đã chạy.

📐 Trần lấy từ các ca bake chữ đã đạt (`ab-3title-3thumb.md` §3 mục 8): **1 cụm/ảnh, ≤7 ký**.
Kanji rậm (険・齢・額・徴) nát trước tiên ⇒ LABEL của v28 dài nhất chỉ **5 ký**.
🔧 Gate trong `img28_prompts.py`: ô PRINT thiếu LABEL · LABEL >7 ký · LABEL chứa số → **chặn cứng**.
⛔ **Nghiệm thu: soi TỪNG KÝ TỰ ở cỡ thật, sai một nét là LOẠI** (`media-library.md` §2.9) —
24 ô có chữ nghĩa là 24 lần soi, sheet thu nhỏ cho qua. Gen **lô thử 6 ô trước**, đừng bơm cả 92.
📌 Bản texture cũ giữ ở `tools/img28_prompts.py.bak_texture` nếu cần đối chiếu.

⛔ Và **bỏ hết `blank` / `empty` / `text-free` khỏi MỌI mô tả**, kể cả ô không có giấy tờ — mấy từ
đó kéo model về phía vẽ mảng trống. Tả **cái CÓ MẶT**: "ghế úp lên bàn" thay "ghế trống", "hai dấu
hỏi" thay "bong bóng rỗng". Guard đặt ở **8–11% đầu prompt**.

### Bốn bẫy đã dính, đừng lặp

1. 🔴 **Độ dài ô phải tính theo mốc BẮT ĐẦU của ô sau**, không phải `t1 − t0`. Giữa hai ô có khoảng
   lặng của giọng; lấy `t1−t0` thì mỗi ô hụt một ít và **hình trôi dần** — đo được: video 57,4s /
   tiếng 61,8s, frame cuối đen. ffmpeg không báo gì.
2. 🔴 **Index input ffmpeg phải ĐẾM THẬT** (`ins.count("-i")−1`). Input cú có 8 phần tử
   (`-stream_loop`/`-framerate`), input ảnh có 6 ⇒ chia cứng cho 6 là ghép nhầm nguồn.
3. 🔴 **Đếm ra 0 ở chỗ lẽ ra phải có gì đó ⇒ nghi PHÉP ĐẾM trước.** `find … | grep -vc` trả 0 trong
   khi `clips/` có 61 file — và kết luận sai đó suýt đảo ngược cả phương án.
4. 🔴 **Thử nghiệm phải chạy ĐÚNG CÁCH sẽ chạy thật.** `build27.py 3` chạy ngon, chạy full mới nổ
   `NameError: SHOTS` vì nhánh mặc định không được chạm tới.

### Còn giữ nguyên từ trước

- **Giọng:** VOICEVOX **雀松朱司 / ノーマル (style 52) / speed 0.9**. Credit 概要欄 「音声: VOICEVOX:雀松朱司」.
- ⭐⭐ **MỘT GIỌNG KỂ** (user chốt 2026-09-16): thoại nhân vật vẫn trong 「」 nhưng cùng giọng cùng
  style — người dẫn thuật lại. ⛔ Không dòng `[聞]`, không tag đổi 話者. Muốn thử 2 giọng phải là
  A/B có chủ định, khai bằng `check_pace.py --2voice`; không khai mà có `[聞]` ⇒ gate G12 đỏ.
- **読み方:** nghĩa ほう → viết hiragana trong script; thấy cảnh báo `⚠ 方` thì sửa kana rồi dựng lại.
- **Chạy nền** mọi lệnh dài theo `render-background.md`; `.cmd` phải ASCII-only + CRLF, redirect đặt
  trước `echo`.

## ③ LUẬT RIÊNG CÒN HIỆU LỰC
- **YMYL tài chính:** KHÔNG bịa số/nguồn — mọi số từ 日本年金機構/厚生労働省/総務省/国税庁/内閣府, verify link TRƯỚC khi viết; cấm 「専門家によると」「必ず」「絶対」; mỗi video ghi 「◯年◯月時点の情報です」+ khuyên xác nhận 年金事務所; không tư vấn đầu tư/sản phẩm; không đảng phái; story hư cấu → disclaimer フィクション.
- **Rule 支給日:** video 給付金/いくらもらえる đăng **1–3 ngày TRƯỚC ngày 15 tháng chẵn** (đè lịch bằng `--slot`).
- **Thumbnail:** khuôn **TELOP/A-45** (`03_THUMBNAIL_TITLE_FORMULA.md` §6 + tool `tools/make_thumb_45.py`) · **chip 対象** góc trên + dải đỏ đáy có nhiệm vụ riêng · **MIỄN gate mặt người** (ngoại lệ nenkin, `audience-45plus.md` §1.2) · gate 168px + chữ tải chủ đề + keyword đo top-2 giữ nguyên · bộ 3 thumbnail A/B.
- **Title:** `【cảnh báo/cảm xúc】＋事件＋月＋！＋hậu quả`, **32–39 ký**, keyword đo cao nhất đứng đầu, cấm 外来語, mọi tình tiết phải CÓ THẬT trong video, bộ 3 title A/B.
- Mỗi video = 1 con số đắt + 1 モニター + 1 hook 決断/損; giải thích chế độ chay ≤45s. Tiền LUÔN là 円. Cold open loss-aversion.
- ⭐⭐ **CỬA SỔ 0–120s KHÔNG CÓ モニター KỂ CHUYỆN (chốt 2026-08-30, `CHANNEL_DIAGNOSIS_2026-08-29.md` §1.2/§3.2).** Đo 5 video: 4 video đưa モニター + chi tiết đời vào 58–85s **mất 13–22 điểm retention trong 60→120s**; video 09 (không モニター, đọc lộ trình + 「まず、事実から」) **phẳng**. Đối thủ 1,3M view (フクロウ) tới giây 60 đã nói xong 対象·stake·lộ trình 3 mục·open-loop, không nhân vật hư cấu. Thi hành:
  1. **0–75s:** あなた+円 → **対象 + phản bác định kiến** → **câu lộ trình** (「三つの金額を順番に…」) → open-loop (câu hỏi lạ) → 「まず、事実から」. **≤2 tag `[間]/[速]`** trong 75s đầu (đối thủ dày chữ, mình thưa).
  2. **モニター vào sau khi trả câu hỏi chính (~phút 2,5–3)**, lần đầu **1 dòng** (tên・県・tuổi・số), tiểu sử/chi tiết đời dời xuống sau. Cast **vẫn giữ** — chỉ đổi chỗ, không bỏ (mũi tiêm humanize ①④ qua cast dồn về phút 3+).
  3. Thẻ hình ở 20–30s **không** là câu phủ định/nhượng bộ (「詐欺ではありません」「去年までは正しかった」).
  4. ⛔ **Giả thuyết 08-20 "あなた @0:03 chữa được vách 20–30s" ĐÃ BỊ BÁC** (v15 khuôn mới relPerf@60s 0,14 < v12 0,24). Vách 19→29s có ở mọi video bất kể lời — phần lớn là khán giả sai sở thích (§③ dòng dưới), không chữa bằng chữ. Gate G6/G7/G8 vẫn chạy nhưng **không được coi là thuốc retention**. ✅ **G9/G10/G11 ĐÃ CÀI vào `check_pace.py` 2026-08-31** (G9 = ĐẢO gate cũ "nhân vật ≤2:00" thành **≥2:00**). ⚠️ Chạy thử trên v18 lộ ra: **v18 RỚT G9** — 松本 vào ~1:20–1:24 thật, vẫn trong cửa sổ 0–120s ⇒ v18 chưa thi hành trọn luật モニター; đọc số 09-05 nhớ điều này (thêm 1 biến lẫn thứ ba ngoài cold open v3 + mật độ sticker).
  5. **Mốc đọc retention mới:** **AVD ≥3:50** (Studio đo "bình thường" 3:51 cho v15) · **awr@120s ≥0,40** · **awr@30s ≥0,65** (mức nhóm G17 đạt, thêm 09-10) · tỉ lệ video dẫn RELATED **cùng ngách** tăng (mốc 5/24). Bỏ relPerf@60s làm mốc chính. Phép đo A/B đầu tiên = video 18 (cold open v3), đọc 2026-09-05.
- ⭐⭐ **CỬA SỔ KÝ 50–150 (≈ giây 10–30) PHẢI CHỞ ≥6 DỮ KIỆN — biến script DUY NHẤT đo được (chốt 2026-09-10, `08_ANALYTICS_LOG.md` block 09-10).** Đo 9 video có curve: corr(dữ kiện ở ký 50–150 , awr@30s) = **+0,76…+0,83**; corr với cửa sổ ký 0–50 = **−0,70**. Nhóm ≥6 (v14=12 · v16=8) → awr@30 **0,70**; nhóm <6 (7 video) → **0,57**.
  1. 🔴 **BÀI HỌC ĐẮT NHẤT: bốn lượt "tối ưu cold open" trước đều DỒN LỰC VÀO GIÂY 0–10 — và chính việc dồn đó làm CẠN cửa sổ 10–30s, đúng chỗ vách rơi.** v18 dồn 3 dữ kiện vào ký 0–50, chỉ còn 2 ở 50–150 → drop 10→30s **−51**, tệ nhất kênh. Cùng họ *"giảm lặp sticker ≠ giảm số lượng"* (`audience-45plus.md` §2.0): **tối ưu một chỉ số thì phải hỏi chỉ số nào là biến ĐÁNH ĐỔI của nó.**
  2. ✅ **Gate `G17` đã cài** (`check_pace.py`, backup `.bak_20260910`): ≥6 dữ kiện ở ký 50–150 · **0 cửa sổ 50 ký rỗng**. Trên 21 script chỉ v08/v10/v14/v16 đạt — đúng nhóm awr cao.
  3. **Neo theo KÝ TỰ, không theo giây, có lý do đo được:** `timeline()` ước tổng chỉ lệch ±2–5% nhưng **cửa sổ 30s đầu lệch 13,5%** (v24: ước 189 ký, thật 149) vì tag `[間]` chỉ được ĐẾM mà không được CỘNG thời gian, và tag dồn hết vào cold open. 30 giây = **148 ký** (trung vị 10 video có srt thật, dải 131–163). ⚠️ **VIỆC CÒN MỞ: G6/G7/G11 (mốc giây) vẫn chịu sai số đó** — mốc chúng báo "đạt" có thể thật ra 22–25s.
  4. ⛔ **Đổi regex đếm thì phải hiệu chuẩn lại ngưỡng.** Biến quyết định của phép đo này là CÁCH ĐẾM, không phải nguồn: regex lỏng (mọi lần một con số xuất hiện) cho +0,83, `RE_NUM` cũ cho +0,47; còn srt-thật vs script-ước gần như không đổi (+0,85 vs +0,83) ⇒ gate chạy được trên script chưa render.
- 🔴🔴 **BIẾN TRỘI KHÔNG PHẢI CHỮ — LÀ CHẤT LƯỢNG TRAFFIC (đo 2026-09-10).** Cùng MỘT video, cùng chữ, cùng hình: browse (`what-to-watch`, **94,7%** traffic) cho AVP **14,4–15,6%**, còn `RELATED_VIDEO` cho **23,0–40,5%** — chênh **1,7–2,6×**. `subscribedStatus` = 8.387 UNSUBSCRIBED / 3 SUBSCRIBED ⇒ bucket `SUBSCRIBER` của API **là home feed, không phải sub thật**. Mobile 14,0% vs desktop 20,3%.
  ⇒ **Không bản viết lại nào bù được khoảng đó.** Việc có đòn bẩy lớn nhất là **đưa người từ browse sang RELATED/search**: end screen + pin comment + playlist theo trụ + keyword đo được đứng đầu title. Tiến độ đo được: RELATED cùng ngách **5/24 → 8/25** (09-10).
  ⛔ **Bốn giả thuyết đã BỊ BÁC bằng số, đừng đề xuất lại:** ① chữ cold open (3 khuôn mở khác hẳn, drop y nguyên) ② lớp hình (v18+ Remotion, v19 gate nhịp hình sạch 3/3 mà AVP browse 9,2% — ⚠️ nhưng đó là gate TRƯỚC render; khuôn mới v27 bị chặn bởi `check_motion` HẬU render, là phép đo khác) ③ モニター trong 0–120s (v19 dời ra 3:10 vẫn tệ nhất) ④ "nói loãng" (đo transcript 2 hit hàng xóm: họ 144–153 ký/30s, **mình 141–196 — dày hơn**).
- ⚠️ **ĐỀ TÀI PHẢI ĐÚNG TỆP 65+ (bài học v19, 09-10).** v19 `高年齢雇用継続給付` browse AVP **9,2%** vs 14,4–15,6% của 4 video cùng nguồn, dù **mọi gate script đều sạch**. Đề tài chỉ áp cho người **còn đi làm 60–64**, trong khi **74,9% khán giả là 65+**. ⇒ Trục 在職/雇用継続 xuống **ô thử nghiệm**, không vào slot chính. Sai đối tượng ở tầng CHỌN ĐỀ TÀI thì không gate script nào bắt được.
- **Title khi kênh chưa được YouTube hiểu chủ đề:** keyword đo được **đứng đầu**, tag 【】 hạ xuống bản A/B đối chứng; ⛔ **không lặp cùng một tag 【】 cảnh báo chung chung** (【見逃し厳禁】 7/9 video) — nó bắt cả feed drama/bóng chày. Đối thủ đổi tag đầu mỗi video (期限切れ注意／6月中に確認／50歳以上必見／申請忘れ続出). Lệch có chủ ý so khuôn 『【】＋事件』 ở trên, xét lại sau 5 video.
- ⭐ **CÂU ĐỊNH VỊ + CTA ĐĂNG KÝ (thêm 2026-08-31, kế hoạch user duyệt — học 保健室 lặp verbatim 1 câu định vị mọi 概要欄):** từ v19, mọi 概要欄 có câu định vị **nguyên văn** 「制度を読むチャンネルではありません。あなたの数字を計算する研究室です。」 (đặt sau 3 dòng SEO hook, trước 目次), và cuối script (trước câu kết chữ ký) 1 câu CTA đăng ký **có lý do quay lại** gắn franchise: 「次の年金支給日の前にも、『直前チェック』をお届けします。見逃したくない方は、チャンネル登録でお待ちください。」 — sub cần LÝ DO, franchise 支給日直前チェック (15 tháng chẵn) là lý do đó. Compliance: không hứa hẹn tuyệt đối, không 外来語.
- ⭐ **HÀNG XÓM MỚI NHẤT PHẢI CÓ TRONG RỔ NHẮM (đo 2026-08-31):** 2 kênh lập đầu 08/2026 đang được YouTube đẩy mạnh — **カメ先生のもらえるお金** (`UCapjcw3S4HvmLWBTTHndjWQ`, 31 ngày → 4.770 sub/597K view; title = chip 対象 【◯◯の方へ】+ sự việc + ｜kỳ hạn — GẦN KHUÔN MÌNH NHẤT ngách, 繰上げ 97K là hàng xóm trực tiếp của v18) và **定年前後のお金の教室** (`UCOn82fXXU5TbAXcZNydidPA`, 30 ngày → 2.790 sub/552K view). Đứng cạnh kênh mới cùng cỡ dễ hơn đứng cạnh フクロウ 46K sub.
- upload_pack.py bắt heading đúng chữ: `### Title CHỐT` · `Mô tả đầy đủ` · `Tên file upload` · `3 dòng đầu` · `タグ` · **`### Pinned comment`**.
- ⭐ **BÌNH LUẬN GHIM LÀ BẮT BUỘC, KHÔNG PHẢI TÙY CHỌN (user chốt 2026-09-08: *"sao lần nào cũng thiếu Pinned comment ở nenkin nhỉ… từ lần sau lúc nào cũng phải có"*).** Mọi script nenkin phải có khối `### Pinned comment` + code fence. **Gate máy đã cài**: `upload_pack.py` in `🔴 GATE PINNED` và ô `[9]` của `METADATA.txt` **luôn hiện** — thiếu thì ô đó là một khối cảnh báo đỏ thay vì biến mất.
  - **Khuôn nenkin** (theo 3 bản đã lên sóng 20·24·17): ① 「ご視聴ありがとうございます。当研究室の、今日のノートです。」 ② **研究ノート ①–⑤** nhắc lại đúng 5 điểm chốt ③ 「お手元で確かめる3つ →」 ④ **một câu hỏi mở mời comment** + 「皆さまの声が、次の研究テーマになります。」 ⑤ disclaimer 「◯年◯月時点の情報です」 + khuyên 税務署/年金事務所.
  - ⚖️ **Mọi con số trong bình luận ghim phải lấy TỪ CHÍNH LỜI ĐỌC** — nó là văn bản YMYL công khai y như 概要欄, không phải chỗ thêm số mới. ⛔ Không bịa link playlist (đã dính lỗi bịa URL ở khối 原典).
  - 🔴 **VÌ SAO KHUYẾT ĐƯỢC BẤY LÂU:** ô `[9]` nằm trong `if ctr.get("pinned")` nên thiếu là **biến mất khỏi METADATA.txt, không một dòng cảnh báo** — và dòng hướng dẫn cuối lệnh ghi 「theo thứ tự [1]→[8]」 nên người dán làm đúng tới [8] rồi dừng. Cùng họ với bẫy ô `[3]` rỗng ở `youtube-upload-seo.md` §4: **cảnh báo đặt cuối file dài thì trôi — nó phải nằm ĐÚNG Ô sắp copy.**

## ④ TRỎ
| Việc | File |
|---|---|
| Viết script | skill `script-nenkin` (quy trình thắng CLAUDE.md; hồ sơ cast/visual thì CLAUDE.md thắng) |
| Hàng đợi đề tài | `02_CONTENT_PLAN.md` · `01_SWIPE_TITLES.md` |
| Thumbnail/Title | `03_THUMBNAIL_TITLE_FORMULA.md` |
| Lớp hình (khuôn đang chạy) | §② file này · `tools/plan27.py` · `img27_prompts.py` · `ingest_art27.py` · `telop27.py` · `build27.py` |
| Bằng chứng khuôn hình | `CHANNEL_BENCHMARK_3video_2026-09-17.md` (mổ 3 kênh 年金 đang thắng) |
| ⛔ Cast/prompt sân khấu (HẾT HIỆU LỰC) | `04_CAST_STAGE_PROMPTS.md` · `STYLE_UPGRADE_PLAN_2026-08-19.md` — thuộc đường `make_stage`/Remotion đã bỏ 2026-09-17, chỉ tra lịch sử |
| Benchmark còn hiệu lực | `CHANNEL_BENCHMARK_okane-hokenshitsu_2026-08-08.md` · `CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` |
| Rules toàn cục | `audience-45plus` (§2.0-quater = trần động + gate `check_motion`) · `media-library` · `render-background` · `ai-video-regen` · `ab-3title-3thumb` · `youtube-upload-seo` · `youtube-compliance` · `upload-schedule` · `cta-midvideo` §2.4b |
| ⛔ `stage-zu-layout` | thuộc lớp thẻ `zu` của `make_stage` — **không còn áp cho nenkin** từ 2026-09-17 (kênh khác còn dùng thì giữ) |

> Bản đầy đủ: ./_archive/CLAUDE_FULL_2026-08-24.md · Doc cũ khác cũng ở ./_archive/
