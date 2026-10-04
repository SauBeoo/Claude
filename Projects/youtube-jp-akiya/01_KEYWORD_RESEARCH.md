# KEYWORD RESEARCH — 実家とお金の整理ノート

> Đo 2026-07-26. Luật áp: `.claude/rules/youtube-upload-seo.md` §0.5 (đo trend TRƯỚC khi chốt title/desc/hashtag/tag).
> Điểm Google Trends là **tương đối trong rổ**, có hạn dùng → đo lại mỗi 6–8 tuần và trước mỗi video quan trọng.

---

## §1 Google Trends — YouTube Search, 30 ngày, geo=JP (đo 2026-07-26)

### 1a. Rổ 1 (`gprop=youtube`, `today 1-m`)

| Keyword | TB | Đỉnh trong kỳ |
|---|---|---|
| **実家じまい** | **12** | **100** (28/6) · 99 (30/6) |
| **相続放棄** | **9** | 93 (30/6) |
| **相続登記** | **5** | 18 (14/7) |
| 空き家 固定資産税 | **0** | 0 — dưới ngưỡng mẫu |
| 実家 売却 | **0** | 4 (20/7) |

### 1b. Rổ 2 (cùng chế độ, **anchor `相続登記` = 5** → ghép được về 1 thang)

| Keyword | TB | Đỉnh |
|---|---|---|
| **空き家** | **48** | 100 (9/7) |
| **固定資産税** | **22** | 68 (29/6) |
| 遺品整理 | 6 | 21 (14/7) |
| **相続登記** (anchor) | **5** | 18 (14/7) |
| 墓じまい | 5 | 18 (17/7) |

### 1c. Thang chung (quy về anchor 相続登記 = 5)

```
空き家 48  ██████████████████████████████████████████████
固定資産税 22 ██████████████████████
実家じまい 12 ████████████
相続放棄 9  █████████
遺品整理 6  ██████
相続登記 5  █████
墓じまい 5  █████
空き家 固定資産税 / 実家 売却 ≈ 0
```

### 1d. ⚠️ ĐỌC SỐ NÀY CHO ĐÚNG — volume cao ≠ đề tài đúng

| Keyword | Volume | Related queries đo được | Kết luận |
|---|---|---|---|
| **空き家** | 48 (cao nhất) | 空き家対策 · **田舎暮らし物件** · **空き物件** · 空き家特例 · マンション空き家 | 🚫 **Tệp NHÀ ĐẦU TƯ / tìm nhà rẻ để ở.** Chỉ `空き家特例` là đúng ngách. → Không dùng đơn lẻ; luôn ghép `実家`/`親の家` |
| **固定資産税** | 22 | **固定資産税 税理士試験** · **宅建 固定資産税** · ガレージ · カーポート · 償却資産税 | 🚫 Bị **dân thi 宅建/税理士** + chủ nhà hỏi carport chiếm. → chỉ dùng dạng `実家 固定資産税` / `空き家 固定資産税` |
| **実家じまい** | 12 | **世にも 実家じまい** · **世にも奇妙な物語** · 世にも奇妙な物語 実家じまい · 実家の片付け · 松本明子 実家じまい | ⚠️ **Spike 100/99 cuối tháng 6 là NHIỄU do phim 世にも奇妙な物語** (tập tên 実家じまい), không phải cầu chủ đề. Nền thật ~10–15. Vẫn dùng được (là tên gọi phổ thông của vấn đề) nhưng **đừng lấy spike làm bằng chứng cầu** |
| **相続放棄** | 9 | 遺産放棄と相続放棄の違い · 相続土地放棄 · **相続放棄 管理責任** · **相続放棄 兄弟** · 相続時精算課税制度 相続放棄 | ✅ **Intent sạch, khớp autocomplete.** 管理責任 + 兄弟 = đúng trục C/D |
| **相続登記** | 5 | **相続登記義務化** · 相続放棄の手続き · 生活保護 · 相続税対策 · **相続登記 期限** | ✅ **Volume nhỏ nhưng intent sạch nhất + có DEADLINE.** 「義務化」「期限」 nằm top related → đúng mũi nhọn trục A |
| 墓じまい | 5 | **徳川慶喜** · 墓じまい トラブル · 墓じまい 永代供養 | Nền nhỏ, spike theo news (徳川慶喜家 12/2025). Trục E — mở sau |
| 遺品整理 | 6 | 費用 · ゴミ屋敷 · 買取 · 特殊清掃 · (tên công ty) | Intent **thuê dịch vụ** → không phải đề tài của kênh, chỉ là dòng chi phí |

**Kết luận keyword cho title/tag:**
1. **Đứng đầu title:** `相続登記` (khi làm trục A/deadline) hoặc `実家` + động từ (`実家を売る`/`実家を相続`) — intent sạch.
2. **`実家じまい`** giữ trong **tag + hashtag + desc** (tên gọi phổ thông, có volume), không nhất thiết đứng đầu title.
3. **`空き家` và `固定資産税` chỉ dùng dạng GHÉP** với 実家/親の家. Không bao giờ đứng một mình.
4. **Cấm vào title/slug:** `空き家 バンク` · `空き家 ビジネス` · `田舎暮らし` · `リフォーム` · `宅建` (kéo tệp sai).

### 1e. Vùng địa lý (interest by region — 相続登記)

Rổ 1: 石川県 · 静岡県 · 広島県 · 福岡県 · 兵庫県 — Rổ 2: 石川県 · 福岡県 · 埼玉県 · 千葉県 · 兵庫県.
→ 石川県 đứng #1 ở cả 2 rổ (nghi liên quan hậu quả 令和6年能登半島地震 → nhiều ca thừa kế/nhà hư hại; **chưa verify, đừng trích như nguyên nhân**). Không dùng để nhắm quảng cáo; chỉ để biết đề tài "nhà ở vùng quê/thiên tai" có cầu thật.

---

## §2 YouTube autocomplete (hl=ja&gl=jp, thứ tự = độ phổ biến truy vấn)

| Seed | Gợi ý theo thứ tự | Đọc ra |
|---|---|---|
| **相続登記** | **を自分で行う方法** / 義務化 / **必要書類** / **書類の綴じ方** / オンライン申請 / **申請書の書き方** / 費用 / 遺産分割協議書 / 原本還付 / **登録免許税 計算** / 自分でやってみた / とは / の仕方 | ⭐ Intent **CẦM TAY CHỈ VIỆC** — người ta định tự làm. Long-form faceless chưa ai phục vụ tử tế (kênh 司法書士 làm nhưng view 3 chữ số) |
| **相続放棄** | の手続き / **しても借金は消えず** / **管理責任** / 必要書類 / **空き家** / 兄弟 / 申述書書き方 / **失敗** / 生命保険 / 後 / 借金 / 全員 / 費用 | Intent **CẠM BẪY** → trục C |
| **実家じまい** | 片付け / **費用** / 業者 / 松本明子 / **自分で** / ゴミ屋敷 / マンション / **仏壇** / ガルちゃん / 断捨離 / 家具だらけ | Volume tốt; top result là vlog → dùng làm tag, không đua nội dung 片付け |
| **実家 相続** | 相続放棄 / **兄弟** / 売却 / 相続税 / 賃貸 / 税金 / 片付け | 兄弟 đứng #2 → trục D có cầu |
| **実家 片付け** | 人気 / 断捨離 / 娘 / 業者 / 捨てる / 息子 / **困ってます** / **喧嘩** / ぺこりん / メルカリ / 費用 / コツ / **50代** | Intent cảm xúc/xung đột → **chất liệu case**, không phải trục |
| **墓じまい** | **費用** / **流れ** / 永代供養 / **トラブル** / 自分で / お骨 / 服装 / とは / 代行 | Cấu trúc y hệt 実家じまい → trục E dễ nhân bản |
| **相続 不動産** | 評価 / 名義変更 / 売却 税金 / 登記 / 分割 / 売却 確定申告 / 土地売却 | Toàn thủ tục + thuế |
| **空き家 解体** | (chỉ 3) 解体 / diy / 建物解体費用 | Volume mỏng dạng ghép |
| ⚠️ **空き家** | **を手に入れた高校生** / リフォーム / バンク / 問題 / **ビジネス** / diy / 再生 / 特例 / **宅建** / 活用 | 🚫 Xác nhận tệp đầu tư/DIY |

---

## §3 Giờ đăng — đo `publishedAt` thật (12 video gần nhất/kênh, 2026-07-26)

| Kênh | Giờ JST | Ngày mạnh | cat | Ghi chú |
|---|---|---|---|---|
| **きな子のシニアお金ゼミ** (faceless VOICEVOX, 167K sub) | **20:00 × 11/12** | T6/CN/T4 | **26** | Kênh đã **dời từ 18:00 → 20:00**; hit 1,06M đăng 20:00 |
| まるごと安全相続ch-あまおう | 18:00 × 12/12 | mọi ngày | 27 | 1 video/ngày → view 1,3–32K |
| 税理士勝部 | 19:00 × 12/12 | **T7 × 12/12** | 22 | 1 video/tuần |
| ケイトのコトノハ日和 | 18:00 × 11/12 | T5/T6 | 22 | vlog 60代 |
| 負動産の窓口 | 20:00 × 9/12 | rải | 22 | |
| 実家じまい研究所 (**chết**) | ⚠️ 12:00–16:00 | T3 | 26 | View 139–699 — phản ví dụ giờ đăng |

**✅ CHỐT cho akiya: 20:00 JST cố định (18:00 giờ VN), ⭐ T6 + T7, 2 video/tuần, categoryId 26.**
> **SỬA 2026-07-28 (đo lại 50 video/kênh, thay 20 video):** ngày thứ hai đổi **CN → T7**. きな子 đăng T7 nhiều nhất (**17/50**) và median view của chính nó xếp **T6 65,7K > T3 50,8K > T7 29,4K > CN 18,9K** → CN là ngày yếu; 税理士勝部 khóa **T7 47/50 video**. Bằng chứng đầy đủ: `.claude/rules/upload-schedule-measure-2026-07-28.md`.
Căn cứ: theo kênh **faceless duy nhất chứng minh được format ở tệp senior-money** (きな子); T6 là ngày mạnh nhất cụm tiền-senior (đo ở benchmark kaigo: 節約看護師 18/20 video T6); tách khỏi 4 kênh workspace đang đăng 19:00.

---

## §4 Bộ nhận diện metadata (chốt theo §1–§3)

- **categoryId:** `26` (Howto & Style) — きな子 12/12 video. Không bê 27 của あまおう (view thấp) hay 22 của 勝部.
- **Rổ 12 tag nhận diện** (đứng đầu mọi video):
  `実家とお金の整理ノート, 実家じまい, 実家 相続, 相続登記, 実家 固定資産税, 実家 売却, 相続放棄, 空き家 実家, 負動産, 相続 兄弟, 実家 解体費用, 50代 相続`
- **3 hashtag cố định:** `#実家じまい #実家の相続 #実家とお金の整理ノート`
- ⚠️ Số tag không phải yếu tố thắng: きな子 dùng **4 tag** ăn 1,06M; あまおう dùng **32 tag** view 1,3K.

---

## §5 CHƯA ĐO ĐƯỢC (đừng trích như đã đo)

1. **Trends chế độ WEB 12 tháng** — 3 lần thử đều bị throttle (trang trả rỗng sau khi rổ YouTube chạy). ⏳ **Còn mở** → cần đo để: ① tách nhiễu phim 世にも奇妙な物語 khỏi nền thật của `実家じまい` ② bắt **tính mùa** của 固定資産税 (t4–5) và 相続登記 (nước rút t1–3/2027). Đo lại sau ≥1 giờ, hoặc rổ ≤3 từ.
2. **Trends theo tháng cho từng đề tài cụ thể** (làm ở GĐ0c của từng video, luật §0.5).
3. Search volume tuyệt đối (không nguồn công khai cho các key này).
4. RPM/CPM riêng ngách 相続/空き家 — chỉ có proxy 不動産投資 800–1.200円/1.000view.
5. Demographics thật của tệp (chỉ có sau khi kênh chạy → Studio Analytics).
