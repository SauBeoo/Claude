# Ma trận KEY — [Món] × [Tạng/Chỉ số]

> Tạo 2026-06-29. Mục tiêu: bắt chéo 2 trục để lọc ra key đáng làm trước.
> Nguồn data: `01_KEYWORD_RESEARCH_NHAT.md` (Google Trends Japan, đo 2026-06-28). KHÔNG bịa số.
> ⚠️ Đây là **bảng ưu tiên**, không phải volume tuyệt đối. Combo cụ thể cần đo lại trên Trends khi muốn chắc.

---

## 1. Cách chấm điểm (KEY SCORE)

```
KEY SCORE = Độ phủ món (0–5) + Độ nóng chỉ số (0–5) + Bonus cầu-đã-chứng-minh (+3)
```

- **Độ phủ món** (từ thang thống nhất 卵=78 ở file 01):
  卵 = 5 · 玉ねぎ/酢玉ねぎ = 4* · ヨーグルト = 3 · 納豆 = 3 · ブルーベリー = 2 · (rau củ chưa đo = ?)
  *玉ねぎ cao một phần do mùa 新玉ねぎ (T4–6) → sẽ hạ, đừng tin tuyệt đối.
- **Độ nóng chỉ số:**
  腎臓 = 5 (breakout +800%, đang lên) · 血圧 = 4 · 認知症 = 3 (volume to nhưng nhiễu tin tức) · 血糖値 = 3 (volume bé, intent cực cao) · 筋肉/サルコペニア = 2 · 血管・コレステロール = 2 · 腸 = 2.
- **Bonus +3:** giao điểm ĐÃ có breakout query thật trong data → người ta đang search đúng combo đó.

---

## 2. Ma trận (món × chỉ số)

Ký hiệu: ◎ = có breakout query thật (+3) · ○ = hợp lý, đáng thử · △ = yếu/chuyên môn · — = không hợp.

| Món \ Chỉ số | 腎臓 (thận) | 血圧 (áp) | 血糖値 (đường) | 認知症 (trí) | 筋肉 (cơ) | Ghi chú |
|---|---|---|---|---|---|---|
| **[ranking món hại]** | ◎ +800% | ○ | ○ | ○ | — | Format "食べてはいけない/ランキング" — mạnh nhất |
| **納豆** | ◎ 朝と夜 +300% | ○ | ○ | ○ | ○ | Bản địa, cực hợp DNA kênh |
| **酢玉ねぎ/玉ねぎ** | ○ | ◎ +150% | ◎ | △ | — | Mạnh huyết áp/đường; lưu ý mùa |
| **ヨーグルト** | ○ | ○ | ◎ HbA1c bùng nổ | △ | ○ | Combo "thêm thứ này" |
| **ゆで卵/卵** | △* | ○ | ○ | ○ | ◎ +90% | *thận: trứng nhiều đạm → góc thận phải cẩn thận |
| **ブルーベリー** | — | △ | ○ | ○ | — | Nghiêng 目/記憶, LỆCH 4 trụ chính |
| **トマト** | ○ | ○ | ○ | ○ | — | Chưa đo volume JP |
| **きゅうり/大根** | ○ | ○ | ○ | — | — | Chưa đo |
| **わかめ/海藻** | ○ | ○ | ○ | ○ | — | Chưa đo |
| **きのこ** | ○ | ○ | ○ | ○ | ○ | Chưa đo |
| **生姜/にんにく** | △ | ○ | ○ | ○ | — | Chưa đo |
| **キャベツ/ブロッコリー** | ○ | ○ | ○ | ○ | ○ | Chưa đo |
| **にんじん/かぼちゃ** | △ | ○ | ○ | ○ | — | Chưa đo |
| **バナナ/りんご** | △ | ○ | △ | ○ | — | Quả ngọt: góc đường huyết phải khéo |

---

## 3. 🎯 Shortlist làm trước (đã có breakout query thật)

| Hạng | Key | Bằng chứng | Trạng thái |
|---|---|---|---|
| 🥇 | **[món] × 腎臓 — 食べてはいけない/ランキング** | 腎臓に悪い食べ物ランキング +800%, 一覧表 +700% | chưa viết |
| 🥈 | **納豆 × 血管/腎臓 (朝と夜)** | 納豆朝と夜どっちがいい +300% | có draft cũ (chat), chưa lưu file |
| 🥉 | **酢玉ねぎ × 血圧・血糖** | 酢玉ねぎの作り方 +150% | chưa viết |
| 4 | **ヨーグルト × 血糖 (HbA1c)** | ヘモグロビンa1c ヨーグルト — bùng nổ | chưa viết |
| 5 | **ゆで卵 × 筋肉** | ゆで卵タンパク質量 +90% | ✅ `04_SCRIPTS/01_yude-tamago.md` |
| (phụ) | **ブルーベリー × 目/記憶** | — (lệch trụ) | ✅ `04_SCRIPTS/02_blueberry.md` (bài luyện format) |

---

## 4. Lưu ý chiến lược

- **Trục mạnh nhất là 腎臓** (breakout +800%) → ưu tiên các script neo vào thận, đặc biệt format "ranking món nên/không nên ăn".
- **Món rau củ quả mới (cà rốt, bí đỏ, bắp cải, rong biển, gừng, tỏi...)**: CHƯA có volume đo cho thị trường Nhật → trước khi đổ công viết, cần 1 vòng đo Google Trends JP (geo=JP, 12-m, mốc nối 卵 hoặc 認知症).
- **Bẫy:** 玉ねぎ cao do mùa (sẽ hạ); 認知症 rising bị nhiễu tin tức/người nổi tiếng → với 認知症 dùng góc evergreen "món phòng bệnh".
- **YMYL:** mọi key vẫn dính rủi ro `03_RUI_RO_YMYL.md` → làm mềm claim, không bịa nguồn/số, có disclaimer hỏi bác sĩ.

---

## 5. Việc tiếp theo (gợi ý)

1. Viết script 🥇 "腎臓に悪い食べ物ランキング" (key mạnh nhất, chưa có).
2. Lưu lại script 納豆 朝と夜 (đang có draft trong chat) thành file.
3. Đo Trends JP cho nhóm rau củ quả mới để điền volume vào cột "Chưa đo".
