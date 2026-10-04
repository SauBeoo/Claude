# CLAUDE.md — youtube-jp-kaigo (rút gọn 2026-08-24)

> Kênh **親の介護とお金ノート** — tiền chăm BỐ MẸ già, cho con cái JP 45–65 (thế hệ sandwich, ~72% nữ, còn đi làm). Ghi đè/bổ sung CLAUDE.md toàn cục.
> ⏸ **Trạng thái: NGƯNG lịch đăng (`slots: []`) — chờ user cấp Gmail mới** (`channel-browser.md`). Bật lại = trả slots về **T3·T6 19:00 JST, 2/tuần** (T6 = ngày lõi ngách).

## Identity
- Persona: **案内役 trung tính VÔ DANH** — không tên/nghề/tuổi. Định vị: 「制度を教える人じゃない。あなたの実家の数字を一緒に計算する人。」
- Độ dài **18–25′** · categoryId **26 Howto & Style** · rổ 12 tag nhận diện + 3 hashtag cố định `#親の介護 #介護とお金 #親の介護とお金ノート`.
- **5 trục KHÓA, không mở rộng** (chi tiết + đề tài: `02_CONTENT_STRATEGY.md`): **A** 凍る前のお金 (認知症→口座凍結・家族信託・成年後見) · **B** 取り戻せるお金 (高額介護サービス費・負担限度額認定証・世帯分離・医療費控除) · **C** 施設とお金 · **D** 兄弟・義務・相続 (民法877・寄与分904条の2) · **E** 自分の家計を守る (介護離職).
- ⛔ CẤM: 介護技術/ケア方法 · giải thích y khoa 認知症 · 介護保険料 của CHÍNH người xem (→ nenkin) · 金融商品/投資/保険 · thực vụ 要介護認定 cấp hành nghề.
- 🚧 **Ranh giới nenkin:** hỏi "người xem tính tiền CHO AI?" — cho mình → nenkin · cho bố mẹ → kaigo.

## Sản xuất
- **Giọng:** VOICEVOX **No.7/ノーマル (id 29)** · intonation 1.1 · **speed 0.90** (hạ từ 0.95 theo `audience-45plus.md` §5.2). Credit 概要欄: 「音声: VOICEVOX:No.7」. 1 giọng bất biến, không rải tag đổi style.
- Hệ số **315 ký/phút** (đo thật, gap 0.6/1.1): 18′≈5.650 · 20′≈6.300 · 25′≈7.850 ký — **cấm ước chay**; đổi giọng/speed → chạy lại `tools/calib_kypm.py`.
- **Render:** `python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\<x>_TTS.md --channel kaigo` — LUÔN chạy nền (`render-background.md`). Bản sắc render (sub/màu/BGM −40dB) đọc từ `channels.py` (nguồn sự thật máy đọc — sửa Ở ĐÓ). Preflight tự chặn thiếu ảnh.
- **✅ GATE 5 ĐIỂM — thiếu 1 = BỎ SLOT, không đăng bù:** ① số tiền của cast trước phút 2 · ② ≥2 原典ショット (shot đầu ≤3′) · ③ trả lời なぜそうなるのか · ④ hành động có ĐỊA CHỈ + HẠN · ⑤ khác trục + khuôn 2 video liền trước. Bảng đầy đủ: `_archive/CLAUDE_FULL_2026-08-24.md`; ngưỡng checkpoint: `08_ANALYTICS_LOG.md` §0.
- CTA giữa video: câu canonical `cta-midvideo.md` **§2.8**, chèn sau khối 実家の家計簿 (~50%).

## YMYL kép (tài chính + pháp lý) — bắt buộc
1. KHÔNG tư vấn cá nhân/pháp lý cụ thể — luôn 「一般的な制度の説明です」.
2. KHÔNG bịa số/nguồn. Chỉ: 厚生労働省 · 自治体 介護保険課 · 日本年金機構 · 総務省家計調査 · 生命保険文化センター · e-Gov. Cấm báo/blog làm nguồn số.
3. **Hedge 自治体 là MẶC ĐỊNH:** mỗi video có 「◯年◯月時点」 + 「制度は市区町村によって異なります…介護保険課・地域包括支援センターでご確認ください」.
4. Cấm 「必ず」「絶対」断定 → 「〜の場合が多い」「制度上は〜」.
5. KHÔNG nói y tế — 認知症/寝たきり chỉ ở hệ quả TIỀN + thủ tục.
6. Cast hư cấu 100% + disclaimer; không tên thật trong tình huống tiêu cực.
- 🛡️ **Policy AI-persona YMYL:** CẤM persona xưng 専門家/FP/ケアマネ/弁護士/社労士/看護師… và CẤM 「私も親を介護していて」 — cảm xúc dồn vào cast (humanize §1.1). Uy tín = 原典を見せる.

## Signature (DNA cố định <10%, còn lại XOAY VÒNG)
1. **実家の家計簿** (moat #1): 1 bảng/video — thu nhập bố mẹ → chi phí → **con bù mỗi tháng**. Kênh này TÍNH HỘ, không giảng.
2. **原典ショット ≥2/video** — trang cơ quan công + khoanh ĐỎ số + nhãn nguồn; URL để 概要欄.
3. **うちの場合はどうなる？** — mỗi chế độ 2–3 nhánh theo thu nhập/世帯構成.
4. **兄弟に見せる1枚** — slide tổng kết share được (pain-point 兄弟喧嘩).
5. Câu kết: 「それでは、また次のノートでお会いしましょう。」
- Màu phán quyết: XANH lấy được · ĐỎ mất · VÀNG sát ranh. Xoay vòng: 5 khuôn mở bài (凍結/期限/兄弟/逆算/通知型) + 5 khuôn 計算タイム; 2 video liền không cùng trục.

## Cast モニター (hư cấu, nguồn sự thật — số KHÔNG tự đổi)
高木さん (女52 東京 パート · 母84 要介護2 静岡 · 年金9万/施設14万→bù 5万) · 高木さんの兄 (56 大阪 · 送金2万→寄与分) · 中村さん (男58 名古屋 課長 · 父87 認知症 · 年収620万 · 預金1.400万 chưa đụng được) · 小林さんご夫妻 (55/53 埼玉 · chăm 4 người → 世帯分離) · 森さん (女49 福岡 派遣 · 母81 要介護3 · 年収310万 → 負担限度額) · 岡田さん (男61 千葉 hưu · 母90 同居 — chồng lấn nenkin, dùng thưa). Chủ đề nhạy cảm → nhân vật MỚI dùng 1 lần. Tiến triển cast ghi lại vào đây.

## Visual + viết
- **ẢNH TĨNH 100% + pan (`--motion`)**, không stock-clip/avatar AI → không tick synthetic. Tỷ lệ: diagram+家計簿 ~35% · cast いらすとや ~30% (≤20 ảnh/video, credit `イラスト:いらすとや`) · 原典 ≥2 · ảnh thật ~20% · card chữ ≤10%.
- Viết bằng **skill `script-kaigo`** (7 giai đoạn, FACT SHEET FIRST). Mâu thuẫn: cast/visual/ranh giới trụ lấy ở ĐÂY; quy trình lấy ở skill. Tiền LUÔN 円. Cold open loss-aversion, giải thích chế độ chay ≤45s, 60–70% thân bài là case/số.
- Lưu file: script `03_SCRIPTS/` · video `06_VIDEO/<slug>/` · đăng xong `upload_pack.py <slug> --channel kaigo --done`. Duyệt contact sheet TRƯỚC render.

## Trỏ
Skill `script-kaigo` · `00_CHANNEL_BIBLE.md` · `02_CONTENT_STRATEGY.md` · `03_THUMBNAIL_TITLE_FORMULA.md` · `CHANNEL_BENCHMARK_2026-07-25.md` · rules: `youtube-compliance` · `audience-45plus` · `ab-3title-3thumb` · `youtube-upload-seo` · `media-library` · `render-background` · `humanize-script-voice` §1.1 · `stage-zu-layout`.

> Bản đầy đủ: `./_archive/CLAUDE_FULL_2026-08-24.md`
