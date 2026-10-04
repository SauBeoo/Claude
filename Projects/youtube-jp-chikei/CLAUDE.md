# youtube-jp-chikei — CLAUDE.md

Kênh **地形と地名の日本史** (JP). Bán một câu: **「その地形が、その歴史を決めた」** — trả lời
MỘT câu hỏi `なぜ` mỗi video, bằng **bản đồ thật của 国土地理院**.

- **Kênh:** `UCfXuolJMQ-3CMpmTeQVkwKA` · **`@chikei-chimei`** — **chuyển đổi từ `사우 오디오` (kr-romfan) 2026-09-16**,
  KHÔNG phải kênh mới. Gmail `ladykiller301096@gmail.com` · Chrome **`Profile 12`**
  (`.claude/rules/channel-browser.md`).
- **Lịch:** **T3・T6・CN 20:00 JST** (3 slot/tuần) — `upload-schedule.md` §0.9.
- **Độ dài:** **15–20′** (trung vị ngách 13–21′, `00_CHANNEL_BIBLE.md` §1.3).
- Bằng chứng ngách + phanh: `./00_CHANNEL_BIBLE.md` · trục & rổ đề tài: `./02_CONTENT_PILLARS.md`
  · bao bì: `./03_THUMBNAIL_TITLE_FORMULA.md` · viết: `./05_SCRIPT_FORMULA.md`
  · sổ đo: `./08_ANALYTICS_LOG.md`

## ⛔ BA LUẬT KHÔNG ĐƯỢC PHÁ (đọc trước mọi việc)

1. **出典 là điều kiện license, không phải trang trí.** Mọi ảnh bản đồ phải mang dòng
   `出典：国土地理院ウェブサイト（…）` — `gsi_map.py` tự đóng, **không có cờ nào tắt**. 概要欄
   cũng phải có (mẫu §SEO dưới).
2. **KHÔNG bịa số/toạ độ/địa danh.** Mọi con số độ cao lấy từ `gsi_map.elev()`; mọi mốc lịch sử
   phải dẫn được nguồn (自治体史・国交省・河川事務所・地理院). Ngách này người xem biết địa
   phương của họ hơn mình — sai một chi tiết là mất sạch uy tín.
3. 🔴 **KHÔNG phán xét đất đai và con người** — `00_CHANNEL_BIBLE.md` §5. Bán 「土地の履歴」và
   「なぜ」. ⛔ Cấm "đừng ở đây", cấm danh sách địa danh kèm phán xét, cấm suy đoán xuất thân
   cư dân (部落差別). Video chạm rủi ro thiên tai **bắt buộc** có câu chốt ở §5 Bible.

## ① LỚP HÌNH — `tools/gsi_map.py` (moat của kênh)

```bash
python tools/gsi_map.py demo                                        # bộ 5 ảnh mẫu
python tools/gsi_map.py map  --lat 35.6595 --lon 139.7005 --z 15 --layers pale,hillshade --out x.jpg
python tools/gsi_map.py then --lat 35.6595 --lon 139.7005 --z 16    # 1961 vs nay
python tools/gsi_map.py sect --a 35.672,139.696 --b 35.650,139.708  # 断面図
python tools/gsi_map.py elev --lat 35.6595 --lon 139.7005           # độ cao 1 điểm
```

**13 lớp tile** (`LAYERS` trong tool): `pale`/`std`/`blank` nền · `hillshade` 陰影起伏図 ·
`relief` 色別標高図 · `slope` 傾斜量図 · `chisui` **治水地形分類図** · `condition` 土地条件図 ·
`air1961`/`air1974`/`airold10` ảnh hàng không cũ · `photo` ảnh vệ tinh nay · `dem` 標高タイル.

**Ba loại ô hình đắt nhất, dùng ít nhất 1 cái mỗi video:**
| ô | hàm | vì sao đắt |
|---|---|---|
| **断面図** | `card_section` | Cho thấy thung lũng bằng CON SỐ (代々木 35m → đáy 19m). **Không đối thủ nào trong ngách có.** |
| **1961 vs nay** | `card_then_now` | Cú đấm thị giác mạnh nhất — 60 năm đổi mặt trong một khung |
| **治水地形分類図** | `card_map(..., ("pale","chisui"))` | 旧河道 hiện ra ngay trên khu dân cư hôm nay |

⚠️ **Ba bẫy đã đo được khi dựng tool (đừng tự "sửa cho gọn"):**
- **`MAG = 2.0`** — bản đầu (mag=1) chữ địa danh ~11px trên khung 1920, đọc không nổi
  (`audience-45plus.md` §1). `pin()` **phải dùng cùng `mag`** với `mosaic()`, quên là pin lệch
  chỗ và lệch NHẸ nên duyệt mắt rất dễ cho qua.
- **Bước trục 断面図 phải ra 5–8 nhãn.** Bản đầu tính step bằng `log10` tròn → range 34m ra
  step 1m = **34 nhãn chồng nhau**.
- **Cache `_tilecache/` là bắt buộc** — một video ~20 ô hình là vài nghìn tile. Bỏ cache = tự
  đi spam server 国土地理院.

**Tỉ lệ ô hình mỗi video (~20 ô):** 12–14 ô bản đồ/đồ hoạ (tool dựng) + 6–8 ô **ảnh AI cảnh
lịch sử** (user gen) + 3 thumbnail A/B. Ảnh AI theo `media-library.md` §2.10 — và vì là ảnh AI
realistic trong video nên **PHẢI tick "altered/synthetic"** khi upload
(`youtube-compliance.md` §2.1).

## ② RENDER

Dùng renderer chung `youtube-jp-health/tools/video_render.py --channel chikei`
(hồ sơ trong `youtube-jp-health/tools/channels.py`). Ảnh tĩnh + pan chậm + phụ đề cháy + BGM +
watermark + CTA overlay.

```bash
python E:\Claude\Projects\youtube-jp-health\tools\video_render.py ^
  03_SCRIPTS\NN_slug_TTS.md --channel chikei
```

- 🔴 **LUÔN chạy nền** theo `.claude/rules/render-background.md` (.cmd ASCII-only + log +
  `EXITCODE`), **không bao giờ foreground**. Xong = `EXITCODE=0` **và** duration khớp srt
  **và** đã soi ≥4 frame bằng mắt.
- 🔴 **Đủ asset mới được render** (`render-background.md` §1.5).
- Nhịp hình: **≤6 đổi hình/phút** và **ảnh chính đổi ≤9,0s** (`audience-45plus.md` §2.0b).
  Bản đồ đứng yên 20 giây là khung chết — chẻ thành *toàn cảnh → zoom → chồng lớp → pin*, mỗi
  bước một ô.

## ③ GIỌNG — ✅ **麒ヶ島宗麟 / ノーマル / speed 0,90 / intonation 1,12** (chốt 2026-09-16)

4 bản demo ở `00_VOICE_TEST/` (VOICEVOX, cùng một đoạn cold open):
`demo_kigashima_sourin.wav` (麒ヶ島宗麟 53) · `demo_aoyama_ryusei.wav` (青山龍星 13) ·
`demo_no7_announce.wav` (No.7 アナウンス 30) · `demo_kurono_takehiro.wav` (玄野武宏 11).

⚠️ Cố ý KHÔNG lấy 青山龍星 dù nó hợp: giọng đó đang chạy ở health + shokutaku + co-dai, thêm
kênh thứ tư là mất nhận diện giọng. Bốn demo giữ lại ở `00_VOICE_TEST/` để so khi cần đổi.

Nhấn nhá giọng theo `.claude/rules/humanize-script-voice.md`: **15–25 tag/video**, tag **chỉ ăn
ở ĐẦU DÒNG và phải DÍNH LIỀN câu** — `[間1.2][速0.8][後間1.0]その川は、いまもあります。`
⛔ Tag đứng một mình một dòng = đổi mặc định vĩnh viễn, giết cả lớp nhấn nhá (§2 rule đó).

## ④ ĐÓNG GÓI / UPLOAD

```bash
python E:\Claude\Projects\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel chikei --open
```
- **A/B 3×3 bắt buộc** (`ab-3title-3thumb.md`): 3 title + `thumb_T1/T2/T3_*.png`.
- SEO đầy đủ (kênh này sống bằng search + suggested, **KHÔNG** thuộc diện SEO nhẹ):
  `youtube-upload-seo.md` — đo Trends trước, tên file slug romaji, `subs.srt` upload tay.
- **概要欄 bắt buộc có 2 khối:**
  ```
  ■ 出典・データ
  国土地理院ウェブサイト（淡色地図・陰影起伏図・色別標高図・治水地形分類図・標高タイル・空中写真）
  https://maps.gsi.go.jp/development/ichiran.html
  ※ 本動画は土地の成り立ちを紹介するものです。個別の土地の安全性を判断するものではありません。
  ```
  + credit giọng VOICEVOX + BGM.
- Checklist upload: tick **altered/synthetic** nếu video có ảnh AI realistic · made for kids =
  NO · `subs.srt` tay.

## ⑤ THƯ MỤC

`01_SOURCES/` nguồn + swipe · `03_SCRIPTS/` `NN_slug.md` + `_TTS.md` + `_SLIDES.json` ·
`06_VIDEO/<slug>/` · `07_UPLOADED/` · `09_BRAND/` avatar–banner · `_tilecache/` (⛔ đừng commit,
đừng xoá) · `credentials/` token YouTube — ⚠️ **token kế thừa CHỈ ĐỌC được** (`mine=True` trả 0 = cấp cho account cá nhân, không phải brand channel) ⇒ `channels.update` / `videos.update` / `thumbnails.set` đều 403. Đọc + Analytics thì chạy bình thường. Muốn upload tự động thì chạy `python tools/auth.py` và **chọn đúng kênh ở màn hình thứ hai**; `--check` phải in ra tên kênh.

Vault: `E:\Claude\SecondBrain\10_Projects\youtube-jp-chikei\youtube-jp-chikei.md`.
