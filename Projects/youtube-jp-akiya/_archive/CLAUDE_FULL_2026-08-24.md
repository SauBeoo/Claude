# CLAUDE.md — youtube-jp-akiya

> Rule riêng cho kênh 「**実家とお金の整理ノート**」 (JP, con cái 50–65 lo TÀI SẢN nhà bố mẹ: 相続登記・固定資産税・実家じまいの費用・空き家特例・売却・解体・相続放棄・兄弟と分け方). Ghi đè/bổ sung CLAUDE.md toàn cục.
> Lập project 2026-07-23 · **chốt chiến lược 2026-07-26**. Số liệu nền: `CHANNEL_BENCHMARK_2026-07-26.md` · Persona/luật/cast/khung: `00_CHANNEL_BIBLE.md` · Đề tài: `02_CONTENT_STRATEGY.md` · Keyword/giờ: `01_KEYWORD_RESEARCH.md`.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-jp-akiya/`. Bằng chứng chọn ngách (2026-07-23): `SecondBrain/10_Projects/youtube-niche-research-2026/`.

## Trạng thái project (2026-07-26)

- **Tên kênh:** 「**実家とお金の整理ノート**」 (user chốt 2026-07-26)
- **Khán giả:** **con cái 50–65**, bố mẹ già/vừa mất, có nhà ở quê; còn đi làm hoặc vừa nghỉ hưu. Trẻ hơn tệp health/shokutaku ~10 tuổi, **già hơn** tệp kaigo ~5 tuổi.
- **Persona: 案内役 trung tính, VÔ DANH** — không tên, không nghề, không tuổi. Xưng 「このノートでは」「一緒に数えていきましょう」. Định vị: 「**制度を解説する人じゃない。あなたの実家に、これからいくらかかるのかを一緒に数える人。**」
- **Lõi nội dung (user chốt 2026-07-26):** khuôn **「届く紙・期限 × 実家の値段表」** — mỗi video = 1 tờ giấy hoặc 1 cái hạn của căn nhà bố mẹ + tính hộ số tiền mất nếu bỏ qua. Căn cứ: 4/4 hit lớn nhất của kênh faceless cùng tệp (きな子 167K sub) đều đúng khuôn này, gồm 固定資産税通知書 **1.061.815 view**.
- **Độ dài:** 18–25 phút.
- **✅ Giọng TTS CHỐT (user 2026-07-26): VOICEVOX `剣崎雌雄 / ノーマル` (speaker id 21) / speed 0.95 / intonation 1.1.** Demo duyệt: `00_VOICE_TEST/demo_21_kenzaki-mesuo_normal.wav`. Credit 概要欄: 「音声: VOICEVOX:剣崎雌雄」. Giọng **bất biến**, không đổi giữa các video, không rải tag đổi style giữa bài.
  - Đặc tính đo được: F0 trung vị **127Hz**, dải 10–90% **98–180Hz** — **nam trầm nhất trong 4 ứng viên**, chắc và bình tĩnh → hợp chủ đề thủ tục/hạn/tiền của tệp 50–65. ⚠️ Giọng trầm dễ nghe ra "phán quyết" → khi viết phải **giữ câu trung tính, không kết luận thay người xem** (bible §4.1); kịch tính đến từ CON SỐ.
  - ⚠️ Tên nhân vật VOICEVOX này là 「男性医師」 kiểu bác sĩ — **KHÔNG bao giờ để persona xưng hay ám chỉ là bác sĩ/chuyên gia**; credit chỉ ghi tên giọng, không ghi mô tả nhân vật.
  - 3 ứng viên loại: 玄野武宏 (id 11, F0 133Hz) · 麒ヶ島宗麟 (id 53, 142Hz, dải rộng nhất) · 冥鳴ひまり (id 14, nữ 253Hz). Không dùng lại 青山龍星 (health/co-dai/shokutaku) · 雀松朱司 (nenkin) · giọng của kaigo.
  - Tool: `tools/voice_demo.py` (xuất demo + file `demo_0_COMPARE_4voices.wav`) · `tools/calib_kypm.py` (đo hệ số).
- **✅ Hệ số ký/phút ĐO THẬT (2026-07-26): 308 ký/phút** — 剣崎雌雄/ノーマル @0.95, **đúng cấu hình render `--gap 0.6 --section-gap 1.1`**; mẫu 4.025 ký / 123 dòng → **13,07 phút** (`00_VOICE_TEST/calib_剣崎雌雄_4025.wav`).
  → **18′ ≈ 5.550 ký · 20′ ≈ 6.150 ký · 25′ ≈ 7.700 ký.** Dùng số này khi lên dàn ý, **cấm ước chay**. (Đo lại nếu đổi giọng/speed/gap. Lưu ý nenkin thấy render thực dài hơn ước 15–20% vì slide/CTA — kiểm lại sau video 01.)
- **Lịch đăng: 20:00 JST cố định, ⭐ T6 + T7, 2 video/tuần** (giờ + nhịp user chốt 2026-07-26; **NGÀY SỬA 2026-07-28: CN → T7**). Căn cứ đổi ngày (đo 50 video/kênh): きな子 đăng **T7 nhiều nhất 17/50** và median view **T6 65,7K > T7 29,4K > CN 18,9K** — CN là ngày yếu của chính kênh chuẩn; 税理士勝部 **khóa T7 47/50**. T7 là ngày của cụm 実家/相続 (khác cụm 介護/年金 = T3+T6). Căn cứ đo: `01_KEYWORD_RESEARCH.md` §3 + `.claude/rules/upload-schedule-measure-2026-07-28.md`.
- **CTA giữa video:** câu canonical mục **2.9** trong `.claude/rules/cta-midvideo.md`, chèn ngay sau khối 実家の値段表 (~50%).
- **Metadata 4 tín hiệu (đo 2026-07-26):** categoryId **26 = Howto & Style** (theo きな子 12/12 video; KHÔNG bê 27 của あまおう hay 22 của 勝部) · **rổ 12 tag nhận diện** đứng đầu mọi video: `実家とお金の整理ノート, 実家じまい, 実家 相続, 相続登記, 実家 固定資産税, 実家 売却, 相続放棄, 空き家 実家, 負動産, 相続 兄弟, 実家 解体費用, 50代 相続` + tag đề tài → tổng 25–35 · **3 hashtag cố định** cuối 概要欄: `#実家じまい #実家の相続 #実家とお金の整理ノート` + ≤3 topical.
- **Hạ tầng: ⏳ CHỜ USER CẤP GMAIL MỚI** (user chốt 2026-07-26: Gmail + Chrome profile MỚI, **KHÔNG rebrand Profile 3 của shokutaku** — shokutaku giữ nguyên). Khi có Gmail: tạo profile `yt-akiya` qua dashboard tab 🌐 Profiles → cập nhật `browser_profiles.json` + `.claude/rules/channel-browser.md` §1 → thêm entry `CHANNELS` (`upload_pack.py`) + `API_CFG` (`upload_api.py`) key `akiya`.

## ⚠️ RULE BẮT BUỘC — YMYL kép (thuế + pháp lý bất động sản)

Chi tiết 6 luật: `00_CHANNEL_BIBLE.md` §4. Tóm tắt không được vi phạm:

1. **KHÔNG tư vấn cá nhân hóa** — không định giá nhà cụ thể, không khuyên bán/giữ.
2. **KHÔNG làm thay 士業** — không hướng dẫn điền đơn kiểu "thế là xong"; được nói **giấy gì / ở đâu / hạn nào / tại sao**.
3. **KHÔNG bịa số.** Nguồn hợp lệ: **法務省・法務局 · 国税庁 · 国土交通省 · 総務省統計局 · 各自治体 · e-Gov/法令データ · 法テラス**. Cấm báo/blog/công ty BĐS làm nguồn số.
4. **Hedge 自治体 mặc định** + mỗi video 「◯年◯月時点の情報です」 + cuối video khuyên xác nhận tại 管轄の法務局 / 市区町村の資産税課 / 税務署.
5. **Không hứa hẹn** — cấm 必ず売れる/絶対に損しない/非課税になります.
6. **Cast + căn nhà hư cấu 100%**; giấy tờ minh họa tự dựng lại, ảnh AI giấy tờ **không có chữ đọc được**.

### 🛡️ Policy AI-persona YMYL (YouTube 15–16/07/2026) — 3 lớp phòng
- **CẤM persona xưng:** 税理士 · 司法書士 · 行政書士 · 宅建士 · FP · 不動産屋 · 元役所職員 · 専門家.
- **CẤM 「私も実家を片付けまして」** — persona TTS kể trải nghiệm "của tôi" = vùng xám gian dối. Cảm xúc dồn vào **cast**.
- **Lớp bù uy tín hợp pháp = 原典を見せる** (≥2 原典ショット/video, shot đầu ≤3 phút).

## 🚧 RANH GIỚI VỚI nenkin & kaigo (ghi ở cả 3 project)

| | `nenkin` 年金と老後のお金研究室 | `kaigo` 親の介護とお金ノート | **`akiya` (kênh này)** |
|---|---|---|---|
| Tiền của ai | **CỦA MÌNH** (年金・給付金・税) | Của **bố mẹ khi CÒN SỐNG** (介護費用) | **TÀI SẢN bố mẹ** — nhà, đất, mộ, thủ tục thừa kế |
| Người xem | 50–70 chính chủ | 45–65 con cái | 50–65 con cái |
| Thuộc kênh này | — | 施設費用, 世帯分離, 認知症→凍結, 寄与分 (phần chăm) | 相続登記, 固定資産税, 空き家特例, 実家売却/解体, 相続放棄, 国庫帰属, 墓じまい |

Đề lưỡng nghĩa → hỏi: **"tiền này chi cho việc CHĂM bố mẹ (kaigo) hay cho CĂN NHÀ/tài sản (akiya)?"** Ví dụ 「親の家を売って施設費に充てる」: phần bán nhà/thuế = akiya; phần chi phí 施設 = kaigo.

## 🔒 KÊNH KHÓA 5 TRỤC — không mở rộng ngoài đây

Chi tiết + trần view proven + 30 đề: **`02_CONTENT_STRATEGY.md`** (nguồn sự thật về đề tài).

- **A 📄 届く紙とその期限** (mũi nhọn) — 固定資産税納税通知書 · 相続登記 2027-03-31 · 3/4/10ヶ月 · 空き家特措法の勧告 · 登録免許税免税 (proven 1,06M–1,28M)
- **B 🧮 実家の値段表** (signature) — 持つ/貸す/売る/壊す/国庫帰属 tổng chi phí (proven 187K–1,57M)
- **C ⚠️ やってはいけない** — 相続放棄の管理責任・借金 · 共有名義 · 更地で税6倍 · 慌てて売る (proven 248K–1,97M)
- **D 👨‍👩‍👧 兄弟と分け方** — 換価/代償/現物 · 10年ルール · 誰が払う (proven 275K–1,12M)
- **E 🪦 その先** (mở từ video ~11) — 墓じまい · 仏壇 · 家財 · 住み替え (long-form còn trống)

**⛔ CẤM tuyệt đối:** 不動産投資/空き家再生ビジネス/空き家バンク/DIY リフォーム (keyword `空き家` kéo tệp đầu tư — đo Trends related: 田舎暮らし物件/空き物件/ビジネス) · 片付けノウハウ vật lý & ゴミ屋敷 before-after (sân vlog mặt thật uchilog 1,77M / ぐりーん 2,47M — faceless đấu là thua; 片付け chỉ là **dòng chi phí** trong 値段表) · 固定資産税 nói chung (bị dân thi 宅建/税理士 chiếm — luôn ghép 実家) · 相続税の節税スキーム · 介護/年金 của người xem · 事故物件/怖い話.

## ✅ GATE 5 ĐIỂM — điều kiện để một video được đăng

Thiếu 1 điểm → **BỎ SLOT, KHÔNG đăng bù.**
1. ≥1 **con số tiền cụ thể của 1 cast** trước **phút 2**.
2. ≥2 **原典ショット**, shot đầu trong 3 phút đầu.
3. Trả lời được 「**なぜそうなるのか**」 (cơ chế), không phải "cứ làm thế này là xong".
4. ≥1 **hành động có ĐỊA CHỈ + HẠN**.
5. **Khác trục** video liền trước + **khác khuôn** mở bài/tính tiền so với 2 video liền trước.

## 👨‍👩‍👧 Cast + căn nhà

Bảng cast (hư cấu 100%) ở **`00_CHANNEL_BIBLE.md` §9** — nguồn sự thật DUY NHẤT: 佐々木さん / 佐々木さんの弟 / 松永さん / 内田さん / 東さんご夫妻 / 川口家3兄弟.
⚠️ Đặc thù kênh này: **mỗi cast gắn MỘT CĂN NHÀ có thông số cố định** (năm xây, diện tích, địa phương, 固定資産税, 評価額) — không đổi giữa các video.

## Viết kịch bản

- **Dùng skill `script-akiya`** (`E:\Claude\.claude\skills\script-akiya\SKILL.md`) — 7 giai đoạn: lọc trục + FACT SHEET FIRST + đo trend + 原典 shot → sổ xoay khuôn → cast + dàn ý case-driven → cold open loss-aversion → viết trong 6 luật YMYL → retention audit + TTS → đóng gói CTR.
- Khi skill và file khác mâu thuẫn: **cast + chuẩn visual + ranh giới trục lấy ở `00_CHANNEL_BIBLE.md`**; quy trình viết lấy ở skill. `script-akiya` ghi đè `script-kaigo`/`script-nenkin` khi lệch.
- Tiền LUÔN là **円** ([[feedback_jp_script_yen_only]]). Cold open = loss-aversion ([[feedback_mo_dau_danh_vao_noi_so]]): câu 1 là mất mát cụ thể + số, giữ căng 25–30s, ~70 ký đầu echo lời hứa title/thumbnail.
- Giải thích chế độ chay **≤45 giây**; 60–70% thân bài là case/số động.

## 🎬 Chuẩn VISUAL

- **ẢNH TĨNH 100% + pan mượt (`--motion`)** — không stock-clip, không avatar AI → **không phải tick altered/synthetic**.
- Tỷ lệ: diagram số + 実家の値段表 **~35%** · cast いらすとや **~30%** · **原典ショット ≥2** · ảnh thật (nhà cũ/giấy tờ/法務局) ~20% · card chữ **≤10%**.
- 4 diagram lõi: **実家の値段表** · **期限カレンダー** · A-vs-B · **兄弟に見せる1枚**.
- **Render (chốt lại 2026-07-27 — HỒ SƠ KÊNH):** `python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\<x>_TTS.md --channel akiya`. Giọng **剣崎雌雄/ノーマル (id 21)/0.95/1.1**, `--sub-style pill --motion`, BGM −40dB, đường dẫn ảnh TUYỆT ĐỐI đều nằm trong `..\youtube-jp-health\tools\channels.py` (**nguồn sự thật máy đọc — sửa Ở ĐÓ**). ⚠️ Dòng cũ ở đây từng ghi `--speaker <chốt sau>` trong khi mục Giọng TTS đã chốt id 21 từ 2026-07-26. **PREFLIGHT tự chặn** trước khâu voice nếu thiếu ảnh / `rank` = 0 / thiếu clip `handmade`. Máy kill ffmpeg dài → `CHUNKS_ONLY=1` trước rồi `--reuse`.
- **Duyệt contact sheet ảnh TRƯỚC render** ([[feedback_contact_sheet_truoc_render]]).
- Media qua kho chung `Projects/_media_library` (rule `media-library.md`).

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md` + `_TTS.md` + `_SLIDES.json`. 原典 → `06_VIDEO/<slug>/genten/`. Video → `06_VIDEO/<slug>/`. Đã đăng → `07_UPLOADED/<slug>/` qua `upload_pack.py --done`.
- Đóng gói upload: `python E:\Claude\Projects\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel akiya` (sau khi thêm entry CHANNELS).
