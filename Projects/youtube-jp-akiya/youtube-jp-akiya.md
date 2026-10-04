# youtube-jp-akiya — 実家とお金の整理ノート

> Kênh faceless JP về **tài sản bố mẹ để lại**: thủ tục & tiền của căn nhà quê (相続登記, 固定資産税, 実家じまいの費用, 空き家特例, 売却/解体/国庫帰属, 相続放棄, 兄弟と分け方). Trục mở rộng: 墓じまい, 仏壇, 親の住み替え.
> Ngách #1 của đợt niche research 2026-07-23 · **chiến lược chốt 2026-07-26** sau khi đo lại benchmark.

## Trạng thái

| Mục | Trạng thái |
|---|---|
| Tên kênh | ✅ 「実家とお金の整理ノート」 (2026-07-26) |
| Lõi nội dung | ✅ khuôn 「届く紙・期限 × 実家の値段表」 |
| 5 trục + 30 đề | ✅ `02_CONTENT_STRATEGY.md` |
| Persona / luật YMYL / cast / khung video | ✅ `00_CHANNEL_BIBLE.md` |
| Benchmark ngách | ✅ `CHANNEL_BENCHMARK_2026-07-26.md` |
| Keyword + giờ đăng | ✅ `01_KEYWORD_RESEARCH.md` (Trends web-12m còn mở) |
| Title/thumbnail | ✅ `03_THUMBNAIL_TITLE_FORMULA.md` |
| Ngưỡng phanh analytics | ✅ `08_ANALYTICS_LOG.md` §0 |
| Skill viết script | ✅ `.claude/skills/script-akiya/` |
| Giọng TTS | ⏳ 4 demo ở `00_VOICE_TEST/` — **chờ user nghe chốt** |
| Hệ số ký/phút | ⏳ đo thật sau khi chốt giọng |
| Gmail + Chrome profile | ⏳ **chờ user cấp Gmail mới** (blocker duy nhất để lập kênh) |
| Script video 01 | ⏳ chưa viết |

## Vì sao ngách này (số đo 2026-07-26)

- **Cửa faceless long-form vẫn trống**, nhưng KHÔNG còn "trống tuyệt đối" như đánh giá 2026-07-23: 3 kênh 税理士 mặt thật mở trong 12 tháng gần đây đều lên nhanh (勝部 07/2025 → 18,4K sub · あまおう 10/2025 → 41,8K · ケイト 01/2026 → 19,6M view/6 tháng), và kênh chuyên đề 実家じまい mọc thêm **hằng tháng** — nhưng tất cả kênh chuyên đề đều chết (view 41–2.900/video). **Cửa sổ tính bằng quý.**
- **Proof-of-format:** きな子のシニアお金ゼミ (faceless VOICEVOX, 167K sub, view/video 146K) — 4/4 hit lớn nhất cùng khuôn 「◯月に届く紙のココ + ◯万円」, gồm 固定資産税 **1,06M**.
- **Deadline cưỡng bức:** 相続登記 ca hồi tố hết hạn **2027-03-31** (過料 ≤10万円) → 8 tháng tới là mùa cao điểm. 空き家3000万円控除 hết **2027-12-31**.
- **Tiền:** RPM proxy 不動産 800–1.200円/1.000view (chưa có số riêng cho ngách).

## Tập trung vào 3 thứ

1. **Khuôn 「届く紙・期限」 + tính hộ tiền** — mỗi video 1 tờ giấy/1 cái hạn + số tiền mất nếu bỏ qua.
2. **原典ショット + fact-check tuyệt đối** — không có tư cách 士業 nên không đấu danh xưng; đấu bằng chiếu trang gốc 法務局/国税庁/国交省 khoanh đỏ. Vừa là moat, vừa là lá chắn policy AI-persona YMYL.
3. **Cưỡi cửa sổ 2027-03-31.**

**Ba thứ KHÔNG làm:** đua 実家の片付け với vlog mặt thật · lấy 空き家 làm keyword trục (kéo tệp đầu tư/DIY) · chạy volume (1 video/ngày ở ngách này = view 1–3K).

## Khán giả

Con cái **50–65**, bố mẹ già/vừa mất, có nhà ở quê. Còn đi làm hoặc vừa nghỉ hưu. Trẻ hơn tệp health/shokutaku ~10 tuổi.

## Format & hạ tầng

- Voice VOICEVOX + **ảnh tĩnh 100% + pan** (`--motion`), 18–25 phút, render `youtube-jp-health/tools/video_render.py`.
- Lịch: **20:00 JST, T6 + T7, 2 video/tuần** (ngày sửa 2026-07-28 theo đo thật: CN → T7) · categoryId **26**.
- Chrome profile riêng (chờ Gmail) — rule `.claude/rules/channel-browser.md`.

## Lộ trình

Plan đầy đủ: `C:\Users\tuana\.claude\plans\glimmering-foraging-naur.md`.

1. ✅ **GĐ1 — nền nội dung** (2026-07-26): benchmark, keyword, bible + cast, strategy 30 đề, thumbnail formula, analytics ngưỡng, skill `script-akiya`, voice demo.
2. ⏳ **GĐ0 — hạ tầng** (cần Gmail): lập kênh + branding, profile, entry `CHANNELS`/`API_CFG`, dòng trong `channel-browser.md`.
3. ⏳ **GĐ2 — 5 video pilot** theo thứ tự đề #01–05 (cưỡi deadline 2027-03).
4. ⏳ **GĐ3 — checkpoint tuần 4** (8 video): đối chiếu ngưỡng ở `08_ANALYTICS_LOG.md` §0.
5. ⏳ **GĐ4** — giữ 2/tuần đến khi ≥3 video >10K view; mở trục E (墓じまい long-form).

## Ranh giới với kênh cùng cụm

`nenkin` = tiền hưu CỦA MÌNH · `kaigo` = tiền CHĂM bố mẹ khi còn sống · **`akiya` = TÀI SẢN bố mẹ (nhà/đất/mộ/thủ tục thừa kế)**. Chi tiết: `CLAUDE.md`.
