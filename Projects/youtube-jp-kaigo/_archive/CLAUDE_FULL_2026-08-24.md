# CLAUDE.md — youtube-jp-kaigo

> Rule riêng cho kênh 「**親の介護とお金ノート**」 (JP, con cái 45–65 đang lo tiền cho bố mẹ già). Ghi đè/bổ sung CLAUDE.md toàn cục.
> Lập 2026-07-25. Nguồn số liệu nền: `CHANNEL_BENCHMARK_2026-07-25.md`. Chiến lược nội dung: `02_CONTENT_STRATEGY.md`.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-jp-kaigo/`.

## Trạng thái project (2026-07-25)

- **Tên kênh:** 「親の介護とお金ノート」 (user chốt 2026-07-25)
- **Khán giả:** **con cái 45–65** (thế hệ sandwich), 72% nữ (厚労省: người chăm chính 72,2% nữ; cụm 50–59 chăm 80–89 = 31,4%). ⚠️ KHÔNG phải người già 65+ như health/shokutaku/nenkin — tệp này **còn đi làm**, xem trên điện thoại lúc nghỉ/tối muộn.
- **Persona: 案内役 trung tính, VÔ DANH** (user chốt 2026-07-25) — không tên, không nghề, không tuổi. Xưng 「このノートでは」/「一緒に見ていきます」. Định vị 1 câu: 「**制度を教える人じゃない。あなたの実家の数字を一緒に計算する人。**」
- **Độ dài:** 18–25 phút (chuẩn ngách: まゆみ 19′ · 税金・社会保障 18′ · 完全攻略 25–59′).
- **✅ Giọng TTS CHỐT (user 2026-07-26): VOICEVOX `No.7 / ノーマル` (speaker id 29) / speed 0.95 / intonation 1.1.** Demo duyệt: `00_VOICE_TEST/demo_29_no7_normal.wav`. Credit 概要欄: 「音声: VOICEVOX:No.7」. Giọng **bất biến**, không đổi giữa các video, không rải tag đổi style giữa bài.
  - Đặc tính đo được: F0 trung vị **242Hz**, dải 10–90% **183–304Hz** — **thấp nhất và trung tính nhất** trong nhóm nữ ứng viên → chất tường thuật/đọc tin, khớp 案内役 bình tĩnh của bible §3 (không ngọt, không bi). Kịch tính đến từ CON SỐ, không từ giọng.
  - 3 ứng viên loại: WhiteCUL (id 23, F0 267Hz, dải rộng nhất = biểu cảm nhất — từng chốt rồi user đổi lại) · 冥鳴ひまり (id 14, 250Hz, dải hẹp nhất) · 玄野武宏 (id 11, nam 139Hz). Không dùng lại 青山龍星 (health/co-dai/shokutaku) hay 雀松朱司 (nenkin) — 2 kênh info JP không được nghe giống nhau.
  - Tool: `tools/voice_demo.py` (xuất demo) · `tools/voice_analyze.py` (đo F0/tốc độ) · `tools/calib_kypm.py` (đo hệ số, nhận `--speaker/--speed/--gap`).
- **✅ Hệ số ký/phút ĐO THẬT (2026-07-26): 315 ký/phút** — No.7/ノーマル @0.95, **đúng cấu hình render `--gap 0.6 --section-gap 1.1`**; mẫu 4.025 ký / 123 dòng → **12,79 phút** (`00_VOICE_TEST/calib_no7_4025.wav`).
  → **18′ ≈ 5.650 ký · 20′ ≈ 6.300 ký · 25′ ≈ 7.850 ký.** Dùng số này khi lên dàn ý, **cấm ước chay**. (Đối chiếu: WhiteCUL đo được 292 ký/phút — No.7 đọc nhanh hơn ~8%. Đổi giọng/speed/gap → chạy lại `calib_kypm.py`. Lưu ý nenkin từng thấy render thực dài hơn ước 15–20% vì slide/CTA — kiểm lại sau video 01.)
- **Lịch đăng: ✅ 19:00 JST cố định (ĐÃ ĐO XÁC NHẬN 2026-07-25 qua API)** — 4 kênh benchmark đều đăng 17:48–20:00 JST; kênh hiệu suất cao nhất nhóm (節約看護師りょう 748K sub/158 video) khóa **19:00 JST 19/20 video**. Giả định "tệp đi làm → peak 21–22h" đã bị số liệu phủ nhận. **Ngày mạnh nhất ngách = THỨ SÁU** (đo lại 2026-07-28: 節約看護師 **T6 = 48/50 video**) → dồn video mạnh nhất vào T6. ⭐ **NGÀY + NHỊP SỬA 2026-07-28 (user chốt): T3·T6, 2 video/tuần CỐ ĐỊNH** — **đảo** quyết định "1 video/NGÀY từ video #6" (chốt 2026-07-26). Căn cứ: 節約看護師りょう (748K, hiệu suất/video cao nhất nhóm) chạy **1,02 video/tuần** → median **105.975 view/video**; みんなの給付金 (551K) đăng long-form **CHỈ T3 (15) + T6 (16)**, ngày khác 0; phản ví dụ trong cùng cụm: あまおう **1 video/ngày → 1,3–32K view**. ⚙️ Hàm `_kaigo_slots()` trong `upload_pack.py` **ĐÃ XOÁ**, nhịp nằm thẳng trong `CHANNELS["kaigo"]["slots"]`. Bằng chứng: `.claude/rules/upload-schedule-measure-2026-07-28.md`. GATE 5 ĐIỂM vẫn đứng TRÊN lịch: không đủ hàng qua gate → **bỏ slot**, không đăng bù, không hạ chuẩn để lấp. Bằng chứng giờ/ngày: `01_KEYWORD_RESEARCH.md` §4.
- **CTA giữa video:** câu canonical mục **2.8** trong `.claude/rules/cta-midvideo.md`, chèn ngay sau khối 実家の家計簿 (~50%).
- **Metadata 4 tín hiệu (đo 2026-07-25):** categoryId **26 = Howto & Style** (theo 節約看護師りょう — cùng tệp, cùng format, hiệu suất/video cao nhất nhóm; KHÔNG dùng 24 của ケアまど đang chết, không bê 27 của nenkin sang) · **rổ 12 tag nhận diện** đứng đầu mọi video: `親の介護とお金ノート, 親の介護, 介護費用, 介護とお金, 介護保険, 老後のお金, 親の介護 お金, 介護 費用 軽減, 高額介護サービス費, 世帯分離, 老人ホーム 費用, 50代 親の介護` + tag đề tài → tổng 25–35 · **3 hashtag cố định** cuối 概要欄: `#親の介護 #介護とお金 #親の介護とお金ノート` + ≤3 topical. (Chốt lại lần cuối khi đăng video 01.)

## 🚧 RANH GIỚI VỚI KÊNH nenkin (bắt buộc, ghi ở cả 2 project)

| | `nenkin` — 年金と老後のお金研究室 | `kaigo` — 親の介護とお金ノート (kênh này) |
|---|---|---|
| Tiền của ai | **CỦA MÌNH** (người xem là chính chủ) | **CỦA BỐ MẸ** + của mình khi phải chăm bố mẹ |
| Khán giả | 50–70, sắp/đang nhận 年金 | 45–65, con cái, còn đi làm |
| Thuộc kênh kia | 介護保険料 65歳以上 của chính người xem (slot #11 nenkin) | 高額介護サービス費 · 負担限度額認定証 · 世帯分離 · 認知症→資産凍結 · 寄与分 · 施設費用 |

Đề nào lưỡng nghĩa → hỏi: "người xem đang tính tiền CHO AI?" Cho mình → nenkin. Cho bố mẹ → kaigo.

## ⚠️ RULE BẮT BUỘC — YMYL kép (tài chính + pháp lý gia đình)

1. **KHÔNG tư vấn cá nhân, KHÔNG tư vấn pháp lý cụ thể.** Luôn đóng khung 「一般的な制度の説明です」. Không phán "trường hợp của bạn thì…", không hướng dẫn viết đơn kiện/di chúc thay 弁護士/司法書士.
2. **KHÔNG bịa số/nguồn.** Chỉ: 厚生労働省 · 各自治体 介護保険課 · 日本年金機構 · 総務省家計調査 · 生命保険文化センター · e-Gov/法令データ (民法 877条 扶養義務 · 904条の2 寄与分). **Cấm** báo/blog/công ty làm nguồn số. Cấm 「専門家によると」 không dẫn nguồn.
3. **Hedge 自治体 là MẶC ĐỊNH, không phải ngoại lệ** — ngách này số nào cũng lệch theo địa phương + 所得段階. Mỗi video: 「◯年◯月時点の情報です」 + 「制度は市区町村によって異なります。必ずお住まいの市区町村の介護保険課、または地域包括支援センターでご確認ください。」
4. **Không hứa hẹn:** cấm 「必ず」「絶対」「得する」断定 → 「〜の場合が多い」「制度上は〜」.
5. **KHÔNG nói y tế.** 認知症/寝たきり chỉ được nhắc ở **hệ quả TIỀN và thủ tục**; cấm giải thích bệnh lý, triệu chứng, điều trị, phòng ngừa (medical misinformation policy → hình phạt là XÓA, không chỉ demonetize).
6. **Cast hư cấu 100%** + disclaimer 概要欄. Không tên thật người/công ty/施設/自治体 cụ thể trong tình huống tiêu cực.

### 🛡️ Policy AI-persona YMYL (15–16/07/2026) — 3 lớp phòng
YouTube cấm monetize "AI persona giả làm chuyên gia trên chủ đề YMYL (y tế, **pháp lý**, **tài chính**)"; 量産コンテンツ đổi tên 「一般的、または繰り返しの多いコンテンツ」.
- **CẤM tuyệt đối persona xưng:** 専門家 · FP · 介護アドバイザー · ケアマネ · 弁護士 · 社労士 · 元役所職員 · 看護師.
- **CẤM 「私も親を介護していて」** — persona AI kể trải nghiệm "của tôi" = vùng xám gian dối, đúng tầm ngắm policy. Cảm xúc dồn hết vào **cast hư cấu**, không vào người dẫn.
- **Lớp bù uy tín hợp pháp = 原典を見せる** (chiếu trang tài liệu gốc, xem SIGNATURE #2) — thay vì bịa tư cách.

## 🧬 SIGNATURE KÊNH — DNA cố định NHỎ (<10% thời lượng), còn lại XOAY VÒNG

> Nguyên tắc: cố định = thứ tạo NHẬN DIỆN; mọi thứ khác BẮT BUỘC đổi giữa các video ("video nào cũng một khuôn" = lỗi + đúng điều luật inauthentic nêu tên).

1. **「実家の家計簿」 (moat số 1)** — mỗi video có ĐÚNG 1 bảng tính tiền của MỘT gia đình cast: thu nhập bố mẹ → chi phí thật → **phần con phải bù mỗi tháng**. Đối thủ giảng chế độ; kênh này **tính hộ**.
2. **原典ショット ≥2/video** — ảnh trang thật (厚労省 / 自治体 介護保険課 / 年金機構 / e-Gov) + **khoanh ĐỎ dày quanh con số đang đọc** + nhãn nguồn góc dưới (cơ quan + 年月時点). Câu dẫn: 「赤で囲んだところ、ご覧ください。」 URL để 概要欄, KHÔNG đọc. Lưu `06_VIDEO/<slug>/genten/genten_<số>_<cơ quan>.png`. **Shot đầu trong 3 phút đầu.** Chỉ chiếu trang cơ quan công; giấy tờ mẫu = tự dựng lại, không dùng giấy thật của người thật.
3. **「うちの場合はどうなる？」** — mỗi chế độ phân **2–3 nhánh** theo thu nhập/世帯構成 (mỗi nhánh 1 cast khác nhau). Đây là cách hedge 自治体/所得段階 mà vẫn hữu ích.
4. **「兄弟に見せる1枚」** — slide tổng kết cuối video, dạng 1 tấm screenshot gửi được cho anh chị em. Đây là **lý do SHARE có thật** (đúng pain-point 兄弟喧嘩 đứng #3 autocomplete 親の介護), không phải xin share suông.
5. **Câu kết cố định:** 「それでは、また次のノートでお会いしましょう。」

**Bộ màu phán quyết (mọi video):** **XANH** = lấy được / giữ được · **ĐỎ** = mất trắng / quá hạn · **VÀNG** = sát ranh, phải xác nhận. Số đang được voice đọc = to nhất màn hình.

**XOAY VÒNG bắt buộc** (ghi khuôn đã dùng vào header script, đối chiếu 2 script liền trước):
- **5 khuôn mở bài:** ① 凍結型 (một ngày tài khoản đóng lại) ② 期限型 (giấy này có hạn, quá là mất) ③ 兄弟型 (cuộc gọi từ anh/chị) ④ 逆算型 (施設 tháng 14万, tiền mẹ 9万 — thiếu 5万 lấy đâu) ⑤ 通知型 (một phong bì từ 役所).
- **5 khuôn 計算タイム:** 実家の家計簿 3 cột / A-vs-B (申請 có vs không) / timeline 55 tháng (thời gian chăm bình quân) / ○×クイズ / tính ngược (muốn không phải bù thì cần điều kiện gì).
- **Trục xen kẽ:** 2 video liền nhau KHÔNG cùng trục (§ khóa 5 trục).

## 🔒 KÊNH KHÓA 5 TRỤC — không mở rộng ngoài đây

> Chi tiết + trần view proven + 15 đề đầu: **`02_CONTENT_STRATEGY.md`** (nguồn sự thật về đề tài).

- **A 💸 凍る前のお金** — 認知症→口座凍結 · 家族信託 · 成年後見の落とし穴 · 代理人カード (proven 104K/437K/707K)
- **B 🧾 取り戻せるお金** — 高額介護サービス費 · 負担限度額認定証 · 世帯分離 · 医療費控除×介護 · おむつ代 · 高額医療高額介護合算 · 介護休業給付金 (proven 25K–193K)
- **C 🏠 施設とお金** — 親の年金だけで入れるか · 特養 vs 有料の実費 · 入居一時金 · 相場と地域差 (proven 51K/69K)
- **D ⚖️ 兄弟・義務・相続** — 介護義務は誰に(民法877) · 寄与分(904条の2) · 介護した人が損する構造 · 話し合いを避けた末路 (proven 36K–707K + autocomplete top)
- **E 🧮 自分の家計を守る** — 介護離職の代償 · 両立の制度 · 「親の金で親を看る」原則 (proven 112K)

**⛔ CẤM tuyệt đối:** 介護技術/おむつ交換/ケア方法 (→ tệp B2B của ケアきょう) · 認知症の医学的説明・治療 (→ YMYL y tế) · 介護保険料 của chính người xem (→ nenkin) · 金融商品/投資/保険の勧め (→ policy AI-persona tài chính) · 要介護認定の実務詳細 kiểu 審査会/法第◯条 (→ demand này là dân hành nghề, không phải gia đình).

## ✅ GATE 5 ĐIỂM — điều kiện để một video được đăng

Thiếu 1 điểm → **BỎ SLOT, KHÔNG đăng bù.** Đây là phanh chống slop khi chạy nhịp cao (nhịp 1/ngày do user chốt, đi ngược benchmark "volume là chiến lược thua" — xem `CHANNEL_BENCHMARK_2026-07-25.md` §2c).

1. ≥1 **con số tiền cụ thể của 1 cast** xuất hiện **trước phút 2**.
2. ≥2 **原典ショット**, shot đầu trong 3 phút đầu.
3. Trả lời được 「**なぜそうなるのか**」 — cơ chế chế độ, không phải "cứ làm thế này là xong".
4. ≥1 **hành động có ĐỊA CHỈ + HẠN**: đi đâu (市区町村の介護保険課 / 地域包括支援センター / 年金事務所 / 税務署), xin giấy gì, trước hạn nào.
5. **Khác trục** video liền trước + khuôn mở bài/計算 khác 2 video liền trước.

## 👨‍👩‍👧 Dàn cast モニター gia đình (hư cấu 100%) — NGUỒN SỰ THẬT DUY NHẤT

> Số liệu đời nhân vật **KHÔNG tự đổi giữa các video** — muốn đổi phải có lý do cốt truyện, và cập nhật lại bảng này. Mỗi video lấy 2–3 người hợp chủ đề, xoay người đóng chính.

| Cast | Tuổi/Nơi/Nghề | Bố mẹ | Số cố định (万円/tháng) |
|---|---|---|---|
| **高木さん** (女) | 52, 東京, パート | 母 84, 要介護2, ở quê 静岡 | 母の年金 9 · 施設候補 14 → **con bù 5** · 高木 thu nhập 12, chồng 32 |
| **高木さんの兄** | 56, 大阪, 会社員 | (cùng mẹ trên) | 送金 2/tháng, về 2 lần/năm → mầm 寄与分 |
| **中村さん** (男) | 58, 名古屋, 課長 | 父 87, 認知症 giai đoạn đầu, sống một mình | 年収 620万 · đang cân 介護離職 · 父の預金 1.400万 (chưa đụng được) |
| **小林さんご夫妻** | 55 & 53, 埼玉 | Chăm cả 4 (2 bên) | 夫 年収 540万 · 4 người già → case 世帯分離 |
| **森さん** (女) | 49, 福岡, 独身, 派遣 | 母 81, 要介護3 | 年収 310万 · 母の年金 7 → case 負担限度額認定 |
| **岡田さん** (男) | 61, 千葉, đã nghỉ hưu | 母 90, 同居 | Chính chủ vừa hưu + chăm mẹ — chồng lấn nenkin, **dùng thưa** |

- Chủ đề nhạy cảm (bố mẹ không có tiền, anh em kiện nhau) → **nhân vật MỚI dùng 1 lần**, không dùng cast thường trực.
- Tiến triển cast ghi lại ở đây mỗi khi có video mới (như nenkin làm với 高橋/松本).

## Viết kịch bản

- **Dùng skill `script-kaigo`** (`E:\Claude\.claude\skills\script-kaigo\SKILL.md`) — 7 giai đoạn: lọc trụ + FACT SHEET FIRST + đo trend + 原典 shot → sổ xoay khuôn → cast + dàn ý case-driven → cold open loss-aversion → viết trong 6 luật YMYL → retention audit + TTS → đóng gói CTR.
- Khi skill và file khác mâu thuẫn: **bảng cast + chuẩn visual + ranh giới trụ lấy ở CLAUDE.md này** (nguồn sự thật); quy trình viết lấy ở skill. Skill `script-kaigo` ghi đè `script-nenkin`/`script-healthy` khi lệch.
- Tiền LUÔN là **円** ([[feedback_jp_script_yen_only]]). Cold open = loss-aversion ([[feedback_mo_dau_danh_vao_noi_so]]): câu 1 là mất mát cụ thể + số, giữ căng 25–30s rồi mới hé lối thoát, ~70 ký đầu phải echo lời hứa title/thumbnail.
- Giải thích chế độ chay **≤45 giây**; 60–70% thân bài là case/số động.

## 🎬 Chuẩn VISUAL kênh

- **ẢNH TĨNH 100% + pan mượt (`--motion`)** — KHÔNG stock-clip, KHÔNG avatar AI (rule `media-library.md` §3 + `youtube-compliance.md` §2) → **không phải tick altered/synthetic**.
- **Tỷ lệ:** diagram số + 実家の家計簿 **~35%** · cast いらすとや **~30%** · 原典ショット **≥2 shot** · ảnh thật bối cảnh ~20% · card chữ **≤10%** (nenkin video 01–02 với 41/45 slide chữ là phản ví dụ — đừng lặp lại).
- **Slide mở màn:** ảnh thật cinematic + chữ hook vàng viền tối (scene `a_hook_photo`) — ảnh chọn theo cảm xúc hook.
- **Cast いらすとや:** `assets/cast/`, **≤20 ảnh/video** (license), credit 概要欄 `イラスト:いらすとや`. Tải thêm: `youtube-jp-nenkin/tools/fetch_irasutoya.py`. Entry SLIDES: `{"match":"...", "photo":true, "cast":"takagi_shock"}` → chạy `make_cast_slides.py` **TRƯỚC** `fetch_photos.py`.
- **4 diagram lõi:** 実家の家計簿 (3 cột: 親の収入 / 費用 / 子の負担) · thang ngưỡng 所得段階 · ○×クイズ · 兄弟に見せる1枚 (trang tổng kết signature).
- **Render (chốt lại 2026-07-27 — HỒ SƠ KÊNH):** `python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\<x>_TTS.md --channel kaigo`. Giọng **No.7/ノーマル (id 29)/0.95/1.1**, `--sub-style pill --motion`, BGM −40dB, đường dẫn ảnh TUYỆT ĐỐI đều nằm trong `..\youtube-jp-health\tools\channels.py` (**nguồn sự thật máy đọc — sửa Ở ĐÓ**). ⚠️ Dòng cũ ở đây từng ghi `--speaker <chốt sau>` trong khi mục Giọng TTS đã chốt id 29 từ 2026-07-26 → đúng loại lỗi tài liệu-tự-đá-nhau mà hồ sơ kênh sinh ra để diệt. **PREFLIGHT tự chặn** trước khâu voice nếu thiếu ảnh / `rank` = 0 / thiếu clip `handmade`. Máy kill ffmpeg dài → `CHUNKS_ONLY=1` chạy trước rồi chạy lại kèm `--reuse`.
- **Duyệt contact sheet ảnh TRƯỚC render** ([[feedback_contact_sheet_truoc_render]]) — lệch thì đổi query, không render xong mới sửa.

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md` + `_TTS.md` + `_SLIDES.json`. Video → `06_VIDEO/<slug>/`. Đã đăng → `07_UPLOADED/<slug>/` qua `upload_pack.py --done`.
- Media qua kho chung `Projects/_media_library` theo rule `media-library.md`.
- Đóng gói upload: `python E:\Claude\Projects\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel kaigo`.
