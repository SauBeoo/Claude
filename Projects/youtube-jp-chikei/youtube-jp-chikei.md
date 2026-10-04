# youtube-jp-chikei — 地形と地名の日本史

Repo sản xuất kênh YouTube JP **地形と地名の日本史**.
Câu bán: **「その地形が、その歴史を決めた」** — mỗi video trả lời MỘT câu hỏi `なぜ` bằng bản
đồ thật của 国土地理院.

## Kênh
- `UCfXuolJMQ-3CMpmTeQVkwKA` — **chuyển đổi từ `사우 오디오` (kr-romfan) 2026-09-16**, không
  lập kênh mới (kênh cũ 0 sub / 3 video / 56 view).
- Gmail `ladykiller301096@gmail.com` · Chrome `Profile 12` · lịch **T3・T6・CN 20:00 JST**.

## Đọc theo thứ tự
| file | dùng khi |
|---|---|
| `CLAUDE.md` | vận hành: render, giọng, upload, 3 luật không được phá |
| `00_CHANNEL_BIBLE.md` | bằng chứng ngách + phanh + **rủi ro 差別地名** |
| `02_CONTENT_PILLARS.md` | chọn đề tài (5 trục, 39 đề tài nạp sẵn, 6 video mở màn) |
| `03_THUMBNAIL_TITLE_FORMULA.md` | đóng gói (khuôn 「なぜ〜のか」 + C-MAP) |
| `05_SCRIPT_FORMULA.md` | viết kịch bản (khung 15–20′, 6 gate) |
| `01_SWIPE_TITLES.md` | mở TRƯỚC khi nghĩ đề tài mới |
| `08_ANALYTICS_LOG.md` | ghi mọi số đo + sổ xoay trục |

## Tool
- `tools/gsi_map.py` — **moat**: bản đồ 国土地理院 (13 lớp), 断面図 từ DEM, so ảnh 1961–nay.
  `python tools/gsi_map.py demo` dựng bộ 5 ảnh mẫu.
- `tools/make_thumb.py` — bộ 3 thumbnail A/B khuôn C-MAP.
- `tools/voice_demo.py` — dựng demo 4 giọng VOICEVOX.
- Render video: `youtube-jp-health/tools/video_render.py --channel chikei`.

## Đang mở
- ⏳ **Giọng chưa chốt** — nghe `00_VOICE_TEST/*.wav` rồi điền `speaker`/`style` vào
  `youtube-jp-health/tools/channels.py["chikei"]` (đang `None`, preflight sẽ chặn render).
- ⏳ Avatar + banner kênh (`09_BRAND/`), BGM riêng, shortcut `YT - chikei.lnk`.

Vault: `E:\Claude\SecondBrain\10_Projects\youtube-jp-chikei\youtube-jp-chikei.md`
