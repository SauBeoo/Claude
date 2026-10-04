---
tags: [project, youtube, korea, romfan, saida]
status: active
started: 2026-07-10
---

# youtube-kr-romfan

Folder note tri thức cho project kênh YouTube Hàn **이불속극장** — audio truyện 로맨스 판타지 hiện đại / 사이다 복수 cho nữ Hàn 18–35.

**Repo code:** `E:\Claude\Projects\youtube-kr-romfan\` (luật vận hành trong `CLAUDE.md` ở đó; luật biên kịch trong skill `script-kr-romfan`).

## Vì sao ngách này

- Nhân bản mô hình đã chạy ở kênh Nhật (chouhen) sang thị trường Hàn — cùng format audio drama nghe thụ động, khác đối tượng (nữ trẻ 18–35 thay vì trung–cao niên).
- Insight lõi: khán giả Hàn nghiện **사이다 전개** (kẻ xấu bị trừng phạt ngay trong tập), dị ứng 고구마 (ức chế kéo dài); fantasy bán được là "được yêu vô điều kiện khi cứ là chính mình, kể cả lười".
- Nghe trong chăn trước khi ngủ → tên kênh 이불속극장.

## Quyết định đã chốt

- **2026-07-10 — Voice:** Azure Speech F0 `koreacentral`; giọng chính nữ `ko-KR-SunHiNeural`, nam ưu tiên `ko-KR-InJoonNeural` hạ tông (demo_ko_injoon_deep), còn lại tùy vai. Gọi REST bằng Python urllib (curl git-bash hỏng encoding tiếng Hàn).
- **2026-07-10 — Skill:** `script-kr-romfan` — transcreation 2 chế độ, 한다체 narration, blacklist dấu vết dịch máy, số giữ chữ số Ả Rập + đơn vị đếm (khác chouhen dùng 漢数字).

## Research / bài học

(ghi dần)

## Việc tiếp theo

- [ ] Viết module Azure TTS gắn vào pipeline video-render (throttle ~20 req/phút, đo hệ số ký tự/phút thật của SunHi)
- [ ] Kịch bản đầu tiên (chế độ A hoặc B) để test end-to-end
- [ ] Thiết kế nền video + watermark theo persona 이불속극장
