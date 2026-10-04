---
tags: [project, youtube, jp, dia-ly, lich-su]
status: active
created: 2026-09-16
---

# youtube-jp-chikei — 地形と地名の日本史

Kênh YouTube Nhật về **địa hình · địa danh · lịch sử sông ngòi**. Lập 2026-09-16 bằng cách
**chuyển đổi kênh `사우 오디오`** (audio drama Hàn, 0 sub) chứ không mở kênh mới.

Repo code: `E:\Claude\Projects\youtube-jp-chikei\` → xem `CLAUDE.md` ở đó.

## Vì sao ngách này
Đo 2026-09-16 (940 video ứng viên, API): ngách **không khoá cửa với kênh mới** — một kênh
**2.340 sub** ăn 72K view, một kênh **81 sub** ăn 25K view. Đây là thứ các ngách health/nenkin
trong workspace không có.

## Bài học mang đi được (không riêng kênh này)
- **地理院タイル của 国土地理院** free cả thương mại, chỉ cần ghi 出典 — cho cả **DEM độ cao
  thật** (dựng được 断面図) và **ảnh hàng không 1961** (so xưa/nay). Bất kỳ kênh nào cần bản đồ
  Nhật đều gọi được `gsi_map.py`.
- Lớp tile chuyên đề (治水地形分類図…) **chỉ phủ một phần lãnh thổ**; ngoài vùng phủ server vẫn
  trả 200 với tile **trong suốt** ⇒ "có tile" ≠ "có dữ liệu". Phải đo tỉ lệ phủ từ alpha.
  Cùng họ với bài học *gate hỏi "có file chưa" thay vì "có đúng không"*.
- Nền **thumbnail** khác nền **slide**: slide cần địa danh đọc được, thumbnail chỉ cần MỘT hình
  dạng đọc được trong 0,3 giây → bỏ lớp có chữ, lùi 1 mức zoom.

## Rủi ro riêng phải nhớ
Nội dung "địa danh này nguy hiểm" là trục view to nhất ngách **và** là trục dễ chạm
**部落差別** + vu khống giá trị bất động sản. Kênh bán 「土地の履歴」 và 「なぜ」, **không bao giờ**
nói "đừng ở đây". Chi tiết: `00_CHANNEL_BIBLE.md` §5.

## Liên quan
- [[youtube-kr-romfan]] — kênh gốc trước khi chuyển đổi
- [[youtube-jp-co-dai]] — từng được lên kế hoạch mang ngách này, đã huỷ 2026-09-16
