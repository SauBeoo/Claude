# CLAUDE.md — youtube-jp-akiya (rút gọn 2026-08-24)

> Kênh **実家とお金の整理ノート** — TÀI SẢN nhà bố mẹ (相続登記・固定資産税・実家じまい・売却/解体・相続放棄・兄弟と分け方・墓じまい) cho con cái JP 50–65. Ghi đè/bổ sung CLAUDE.md toàn cục.
> ⏸ **Trạng thái: NGƯNG (`slots: []`) — CHỜ USER CẤP GMAIL MỚI** (⛔ không rebrand Profile 3 của shokutaku). Khi có Gmail: tạo profile `yt-akiya` qua dashboard 🌐 Profiles → cập nhật `browser_profiles.json` + `channel-browser.md` §1 + entry `API_CFG` (`upload_api.py`). Bật lại lịch = **T6·T7 20:00 JST, 2/tuần** (T7 = ngày cụm 実家/相続).

## Identity
- Persona: **案内役 trung tính VÔ DANH** — 「制度を解説する人じゃない。あなたの実家に、これからいくらかかるのかを一緒に数える人。」
- Lõi: khuôn **「届く紙・期限 × 実家の値段表」** — mỗi video = 1 tờ giấy/1 cái hạn + tính hộ số tiền mất nếu bỏ qua.
- Độ dài **18–25′** · categoryId **26 Howto & Style** · rổ 12 tag nhận diện + 3 hashtag cố định `#実家じまい #実家の相続 #実家とお金の整理ノート`.
- **5 trục KHÓA** (30 đề: `02_CONTENT_STRATEGY.md`): **A** 届く紙とその期限 (mũi nhọn) · **B** 実家の値段表 (signature: 持つ/貸す/売る/壊す/国庫帰属) · **C** やってはいけない · **D** 兄弟と分け方 · **E** その先 (墓じまい, mở từ video ~11).
- ⛔ CẤM: 不動産投資/空き家再生/空き家バンク/DIY リフォーム · 片付けノウハウ vật lý & ゴミ屋敷 before-after · 固定資産税 nói chung không ghép 実家 · 相続税の節税スキーム · 介護/年金 của người xem · 事故物件.
- 🚧 **Ranh giới:** tiền CỦA MÌNH → nenkin · chi cho việc CHĂM bố mẹ → kaigo · cho CĂN NHÀ/tài sản → akiya. (「親の家を売って施設費に」: bán nhà/thuế = akiya, chi phí 施設 = kaigo.)
- ⭐ **Luật mùa:** trục 相続登記 chạy trước **2027-03-31** · 固定資産税納税通知書 chạy **T4–T5** · 空き家3000万控除 trước **2027-12-31**.

## Sản xuất
- **Giọng:** VOICEVOX **剣崎雌雄/ノーマル (id 21)** · intonation 1.1 · **speed 0.90** (hạ từ 0.95 theo `audience-45plus.md` §5.2). Credit: 「音声: VOICEVOX:剣崎雌雄」 — chỉ ghi tên giọng, ⛔ KHÔNG bao giờ ám chỉ persona là bác sĩ/chuyên gia (nhân vật gốc là 「男性医師」). 1 giọng bất biến. Giọng trầm dễ nghe ra "phán quyết" → câu giữ trung tính, kịch tính đến từ CON SỐ.
- Hệ số **308 ký/phút** (đo thật, gap 0.6/1.1): 18′≈5.550 · 20′≈6.150 · 25′≈7.700 ký — **cấm ước chay**; đổi giọng/speed → `tools/calib_kypm.py`.
- **Render:** `python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\<x>_TTS.md --channel akiya` — LUÔN chạy nền (`render-background.md`). Bản sắc render (sub/màu/BGM −40dB) đọc từ `channels.py` (nguồn sự thật máy đọc — sửa Ở ĐÓ). Preflight tự chặn thiếu ảnh.
- **✅ GATE 5 ĐIỂM — thiếu 1 = BỎ SLOT, không đăng bù:** ① số tiền của cast trước phút 2 · ② ≥2 原典ショット (shot đầu ≤3′) · ③ trả lời なぜそうなるのか · ④ hành động có ĐỊA CHỈ + HẠN · ⑤ khác trục + khuôn 2 video liền trước. Bảng đầy đủ: `_archive/CLAUDE_FULL_2026-08-24.md`; ngưỡng: `08_ANALYTICS_LOG.md` §0.
- CTA giữa video: câu canonical `cta-midvideo.md` **§2.9**, chèn sau khối 実家の値段表 (~50%).

## YMYL kép (thuế + pháp lý BĐS) — 6 luật đầy đủ ở `00_CHANNEL_BIBLE.md` §4
1. KHÔNG tư vấn cá nhân hóa — không định giá nhà cụ thể, không khuyên bán/giữ.
2. KHÔNG làm thay 士業 — chỉ nói **giấy gì / ở đâu / hạn nào / tại sao**.
3. KHÔNG bịa số. Nguồn hợp lệ: 法務省・法務局 · 国税庁 · 国土交通省 · 総務省統計局 · 各自治体 · e-Gov · 法テラス. Cấm báo/blog/công ty BĐS.
4. Hedge 自治体 mặc định + 「◯年◯月時点」 + khuyên xác nhận tại 法務局/資産税課/税務署.
5. Cấm 必ず売れる/絶対に損しない/非課税になります.
6. Cast + căn nhà hư cấu 100%; giấy tờ minh họa tự dựng, ảnh AI giấy tờ không có chữ đọc được.
- 🛡️ **Policy AI-persona:** CẤM xưng 税理士/司法書士/行政書士/宅建士/FP/不動産屋/専門家 · CẤM 「私も実家を片付けまして」 (cảm xúc dồn vào cast — humanize §1.1) · uy tín = 原典を見せる.

## Cast + căn nhà
Bảng cast ở **`00_CHANNEL_BIBLE.md` §9** — nguồn sự thật DUY NHẤT: 佐々木さん / 佐々木さんの弟 / 松永さん / 内田さん / 東さんご夫妻 / 川口家3兄弟. ⚠️ Mỗi cast gắn MỘT CĂN NHÀ thông số cố định (năm xây, diện tích, địa phương, 固定資産税, 評価額) — không đổi giữa các video.

## Visual + viết
- **ẢNH TĨNH 100% + pan (`--motion`)**, không stock-clip/avatar AI → không tick synthetic. Tỷ lệ: diagram+値段表 ~35% · cast いらすとや ~30% · 原典 ≥2 · ảnh thật ~20% · card chữ ≤10%. 4 diagram lõi: 実家の値段表 · 期限カレンダー · A-vs-B · 兄弟に見せる1枚.
- Viết bằng **skill `script-akiya`** (7 giai đoạn, FACT SHEET FIRST). Mâu thuẫn: cast/visual/ranh giới trục lấy ở `00_CHANNEL_BIBLE.md`; quy trình lấy ở skill; `script-akiya` ghi đè `script-kaigo`/`script-nenkin`. Tiền LUÔN 円. Cold open loss-aversion (~70 ký đầu echo title/thumbnail), giải thích chế độ chay ≤45s, 60–70% thân bài là case/số.
- Lưu file: script `03_SCRIPTS/` · 原典 `06_VIDEO/<slug>/genten/` · đăng xong `upload_pack.py <slug> --channel akiya --done`. Duyệt contact sheet TRƯỚC render. Media theo `media-library.md`.

## Trỏ
Skill `script-akiya` · `00_CHANNEL_BIBLE.md` (persona/luật/cast) · `02_CONTENT_STRATEGY.md` (đề tài) · `01_KEYWORD_RESEARCH.md` (keyword/giờ) · `03_THUMBNAIL_TITLE_FORMULA.md` · `CHANNEL_BENCHMARK_2026-07-26.md` · rules: `youtube-compliance` · `audience-45plus` · `ab-3title-3thumb` · `youtube-upload-seo` · `media-library` · `render-background` · `humanize-script-voice` §1.1.

> Bản đầy đủ: `./_archive/CLAUDE_FULL_2026-08-24.md`
