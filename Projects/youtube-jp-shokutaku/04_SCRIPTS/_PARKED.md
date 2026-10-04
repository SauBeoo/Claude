# Tồn kho ĐÓNG BĂNG — 2026-08-11

> Lý do: cả 3 viết theo **spec cũ**, trước khi có luật v3 (cửa tử giây 20–40, S6 tháo ngòi, S7 credential — `CHANNEL_DIAGNOSIS_2026-08-11.md` + skill MỤC 10 §v3).
> Không xoá. Muốn dùng lại thì **viết lại cold open theo spec v3 + chạy `python tools\check_coldopen.py <NN>`**, không phải đem render thẳng.

| script | trạng thái | vướng gì |
|---|---|---|
| `06_blueberry-kumiawase` | **ĐÃ RENDER, chưa đăng** | Hook fail từ 08-01 (case study ngay giây 25). Gate v3: **thiếu mốc `# ITEM1`**. Sửa lời = phải render lại toàn bộ. Thêm: ブルーベリー nằm trong nhóm **bão hoà** (`CLAUDE.md` §Việc 2) |
| `07_ninjin-kumiawase` | script, chưa render | Viết theo spec cũ. にんじん là món ⭐ (median 2.083 v/ngày) → **đáng cứu**, nhưng phải viết lại cold open |
| `08_jinzo-yoi-tabemono` | script, chưa render | Gate v3: thiếu `# ITEM1`. **Vướng nặng hơn:** rổ 臓器 làm chủ ngữ = luồng ĐÃ CHẾT (median 24 v/ngày). Muốn dùng phải re-angle sang MÓN làm chủ ngữ, tức viết lại gần hết |

**Video 14 viết MỚI hoàn toàn** = phép thử sạch đầu tiên của spec v3. Đổi đúng 1 biến (cấu trúc), giữ nguyên độ dài / giọng / thumbnail / khuôn title.
