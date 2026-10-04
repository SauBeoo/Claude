# 地形と地名の日本史 — KHUÔN TITLE + THUMBNAIL

> Chốt 2026-09-16. Căn cứ: `00_CHANNEL_BIBLE.md` §1.4 (đo 50 video/kênh × 10 kênh ngách).
> Luật trên nó: `.claude/rules/ab-3title-3thumb.md` (3×3) · `audience-45plus.md` §1 ·
> `youtube-upload-seo.md` §0.5 (đo Trends TRƯỚC) · `youtube-compliance.md` mục 3.

## 1. TITLE — khuôn 「なぜ〜のか」

Hai khuôn thắng đo được trong ngách, **cả hai đều là CÂU HỎI**:

| khuôn | kênh chứng minh | số |
|---|---|---|
| `なぜ〜のか？` + 【歴史】【地形】【解説】 | 東京限定雑学 | median **87.748** view/video |
| `【地図でわかる】なぜ〜のか？` | 地図で読み解く歴史と経済ch · ジオトリ | hit lẻ 308–385K |

**Khuôn kênh mình:**

```
なぜ<ĐỊA DANH>は<ĐIỀU LẠ>なのか — <CÚ LẬT NGẮN>【地形】【歴史】
```
Ví dụ đúng khuôn:
- `なぜ渋谷は「谷」なのか — 60年前まで流れていた川の話【地形】【歴史】`
- `なぜ江戸は日本一の城を築けたのか — 台地と入江が決めた立地【地形】【歴史】`
- `利根川を東に曲げた60年 — 江戸を救った土木工事の全記録【地形】【歴史】`

**Sáu luật viết title:**
1. **Keyword đo được đứng trong 5–7 từ đầu** (`youtube-upload-seo.md` §2.1). Địa danh nổi
   tiếng (渋谷・江戸・利根川) **là** keyword — đừng nhường chỗ đầu cho chữ 「なぜ」 nếu phải chọn.
2. **Lọt ~30 ký full-width** trước khi bị cắt.
3. **Hậu tố 【地形】【歴史】 cố định** = nhận diện kênh + 2 keyword, đặt cuối.
4. **Câu hỏi phải có ĐÁP ÁN trong video** — `youtube-compliance.md` mục 4.
5. ⛔ Cấm ở title/thumbnail: 危険・住んではいけない・ヤバい・呪われた・事故物件 →
   vừa dính compliance vừa dính §5 Bible.
6. Con số trong title là **con số đo được** (`-22m`, `60年`, `43km`), không phải số làm tròn cho kêu.

### 3 TITLE A/B (bắt buộc mỗi video — `ab-3title-3thumb.md` §2)
| | vai | thử |
|---|---|---|
| **A1** ⭐ đăng | = Title CHỐT, trùng từng ký tự | keyword volume cao nhất |
| **A2** | đổi **keyword dẫn** | địa danh ↔ tên sông ↔ tên hiện tượng địa hình |
| **A3** | đổi **kiểu hook** | câu hỏi ↔ con số (`標高差22m`) ↔ mốc thời gian (`60年で消えた`) |

## 2. THUMBNAIL — khuôn **C-MAP**

⭐ **Lợi thế riêng của kênh: nền thumbnail là BẢN ĐỒ THẬT do `gsi_map.py` dựng**, không phải
ảnh AI. Người xem thấy ngay "video này có dữ liệu", và **kanji không bao giờ nát** vì chữ do
Noto Sans JP vẽ chứ không do model gen.

```
┌──────────────────────────────────────────┐
│ [chip trên-trái: 地名 hoặc 川名]           │  ~11% cao
│                                          │
│      なぜ、ここが「谷」なのか              │  dòng phụ, ~20%
│                                          │
│   ██  谷だった  ██                        │  HERO 3–5 ký, ≥30% cao, ≥55% rộng
│                                          │
│ ─────────────────────────────────────    │
│ ▌標高差 22m ─ 断面図でわかる              │  dải đỏ đáy, ~14%
└──────────────────────────────────────────┘
        nền: hillshade / relief / 空中写真1961
```

**Gate (thiếu 1 = render lại, không giao):**
1. **Hero 3–5 ký full-width**, **rộng ≥55% khung** (bề ngang là thứ mua được legibility —
   `audience-45plus.md` §6.10 ca 10–12), viền đen dày + halo trắng.
2. **≤3 khối chữ** (dòng phụ + hero + dải đáy). Chip không tính.
3. **Đọc được dòng hero ở 168px VÀ 120px** — duyệt mắt trên `*_prev168.png`.
4. **Nền phải là bản đồ CÓ HÌNH DẠNG ĐỌC ĐƯỢC** — thung lũng/khúc sông/bờ biển phải nhìn ra
   ở 168px. Bản đồ đô thị dày chữ (`std` ở zoom cao) **không dùng làm nền thumbnail**.
5. **Chữ giống nhau ở cả T1/T2/T3** — biến thử là HÌNH (`ab-3title-3thumb.md` §3 mục 6).
6. **Góc dưới-phải chừa trống** (timestamp YouTube) · badge nhận diện ở góc dưới-TRÁI.
7. ⛔ Không badge thời lượng.

**Bộ A/B 3×3:**
| | biến đổi |
|---|---|
| **T1** baseline | nền `hillshade`+`relief`, khuôn C-MAP chuẩn |
| **T2** đổi 1 biến hình | đổi nền sang **空中写真1961** (giữ nguyên chữ, layout) |
| **T3** đổi layout | hero + **断面図** làm nền (đồ thị thay bản đồ), tỉ lệ chữ/hình đảo |

### 2.1 🟡 NGOẠI LỆ gate 4 của `audience-45plus.md` (≥1 khuôn mặt biểu cảm)

**Kênh này MIỄN gate mặt người.** Căn cứ: 10/10 kênh ngách đo được (東京限定雑学 112K,
地図で読み解く 32K, ジオトリ 145K, わくわく地理マップ, 楽しく地理…) **không kênh nào** dùng mặt
người trên thumbnail; thứ bán được ở đây là **HÌNH DẠNG ĐẤT**. Cùng dạng ngoại lệ đã cấp cho
nenkin (`audience-45plus.md` §1.2).
Gate 1・2・3・5・6 **giữ nguyên**, gồm bắt buộc đọc được ở 168px.
📅 **Xét lại sau 5 video:** CTR thấp hơn hẳn mức trung bình kênh → thử T3 có một bàn tay/bóng
người chỉ vào bản đồ, ghi vào `08_ANALYTICS_LOG.md`.

### 2.2 Chữ phải TẢI CHỦ ĐỀ (gate 7)
Che ảnh đi, đọc chữ vẫn phải trả lời đủ 3 câu: **① về cái gì** (địa danh — và phải là keyword
top 2 bảng Trends) **② chuyện gì xảy ra** (谷だった / 川が消えた / 22m) **③ vì sao nên xem**
(断面図でわかる / 1961年の写真).

## 3. QUY TRÌNH RENDER THUMBNAIL

```bash
python tools/make_thumb.py <slug> --lat .. --lon .. --z .. \
  --chip 渋谷 --sub "なぜ、ここが「谷」なのか" --hero 谷だった --band "標高差 22m ─ 断面図でわかる"
```
→ xuất `thumb_T1_<slug>.png` · `thumb_T2_<slug>.png` · `thumb_T3_<slug>.png` + bản `_prev168.png`.

📌 **Vì sao KHÔNG đi đường prompt-AI-bake-chữ** (`ab-3title-3thumb.md` §3 mục 8): luật đó sinh
ra để chống **tool vẽ chữ đè lên ảnh AI**, vì user cần thấy bộ mặt thật lúc gen. Ở kênh này nền
**không phải ảnh AI** — nó là dữ liệu bản đồ mình tự dựng, nên tool vẽ chữ là đường đúng và
còn tránh được bẫy nát kanji của model. Nếu bao giờ dùng nền ảnh AI thì quay lại luật gốc.
