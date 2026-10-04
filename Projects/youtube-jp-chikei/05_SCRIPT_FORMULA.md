# 地形と地名の日本史 — KHUÔN KỊCH BẢN

> Chốt 2026-09-16. Kênh **chưa có skill `script-*` riêng** — file này là nguồn sự thật về cách
> viết. Luật trên nó: `humanize-script-voice.md` (chất người + tag giọng) ·
> `audience-45plus.md` (nhịp, độ dài) · `00_CHANNEL_BIBLE.md` §5 (rủi ro ngách).

## 0. KHUNG — 15–20′ ≈ **4.600–5.400 ký JP** (speed 0,90 ≈ 290 ký/phút)

| khối | thời lượng | việc phải làm |
|---|---|---|
| **COLD OPEN** | **≤60 giây** | Đặt người xem vào MỘT CHỖ HỌ BIẾT → nêu điều bất thường → hỏi `なぜ` → hứa trả bằng bản đồ. ⛔ Không tự giới thiệu, không "hôm nay chúng ta sẽ…" |
| **第1章 いまの地形** | 3–4′ | Bản đồ hiện tại + **断面図**. Cho thấy CON SỐ (「谷底は19メートル、台地は35メートル。差は16メートルです」) |
| **第2章 時間を巻き戻す** | 4–5′ | **空中写真1961 vs nay** / bản đồ cũ / 治水地形分類図. Cú lật thị giác của bài |
| ← **CTA giữa video** | ~50% | Câu canonical `.claude/rules/cta-midvideo.md` §2.11 — đặt NGAY SAU khối 断面図/1961 |
| **第3章 なぜ、そうなったのか** | 4–5′ | Con người + quyết định + năm tháng. Đây là chỗ bài thành LỊCH SỬ chứ không phải bài địa lý |
| **第4章 いまも残る痕跡** | 2–3′ | **Thứ người xem tự đi xem được**: con dốc, tên cầu không còn sông, lan can giữa phố, ranh giới phường lượn cong |
| **結び** | ~40 giây | Trả lại câu hỏi mở + 1 câu gieo cho video sau |

## 1. COLD OPEN — khuôn 4 câu (gate ≤60 giây)

```
① CHỖ QUEN     : 渋谷、スクランブル交差点。一日に、何十万人も渡る、あの場所です。
② ĐIỀU BẤT THƯỜNG: あそこに立つと、どちらを向いても、道が上り坂になっています。
③ CÂU HỎI なぜ  : なぜ、あの街だけが、四方を坂に囲まれているのか。
④ LỜI HỨA      : 地図を二百年、巻き戻してみます。答えは、いまはもう見えない一本の川にあります。
```

**Bốn luật:**
1. **Câu 1 phải là CHỖ, không phải khái niệm.** ⛔ Không mở bằng 「地形とは…」「日本には古くから…」.
2. **Điều bất thường phải KIỂM ĐƯỢC** — người xem đứng đó nhìn ra được, hoặc thấy được trên bản đồ.
3. ⛔ **Không spoil đáp án ở cold open**, nhưng **phải nói rõ mình sẽ trả bằng gì** (bản đồ/ảnh
   1961/độ cao) — đó là lời hứa mà kênh này có thể giữ mà đối thủ không giữ được.
4. **Drill cắt đôi ×2** trước khi tính là xong (`youtube-suggested-growth.md` §5).

## 2. CHẤT NGƯỜI — ngoại lệ riêng của kênh này

`humanize-script-voice.md` đòi **≥4/6 mũi tiêm**, trong đó có "người kể xuất hiện bằng trải
nghiệm". 🔴 **Ở kênh này, người dẫn KHÔNG được kể trải nghiệm đi thực địa** — vì mình không đi
thật, và một câu 「私が歩いてみたところ」 bịa ra sẽ hỏng đúng thứ kênh bán: **độ tin cậy của dữ
liệu**. Cùng dạng ngoại lệ của nenkin/kaigo/akiya (`humanize-script-voice.md` §1.1).

**Chất người đi qua 3 đường khác, mỗi bài dùng ≥2:**

| đường | mẫu |
|---|---|
| **NGƯỜI XƯA làm nhân vật** (có thật, có ghi chép) | 「伊奈忠治は、父の代からの仕事を引き継ぎました。完成を見たのは、孫の代です」 |
| **Cảm giác GIÁC QUAN của địa hình** (ai đi qua cũng có) | 「自転車で、あの坂を上ったことがある方なら、体が覚えているはずです」 |
| **Người kể thú nhận đã hiểu sai** (an toàn, không bịa số) | 「正直に言うと、私はずっと、地名というのは適当につけられたものだと思っていました」 |

Tag giọng: **15–25 tag/video**, đỉnh bài đặt ở lúc hiện con số 断面図:
`[間1.2][速0.8][後間1.0]その差、十六メートル。` — tag **dính liền câu, đầu dòng**.

## 3. SÁU GATE (tự kiểm trước khi giao)

| # | Gate | Vì sao |
|---|---|---|
| **G1** | **≥1 ô hình "chỉ kênh này có"** — 断面図 · 1961-vs-nay · 治水地形分類図 | Không có = video này ai cũng làm được |
| **G2** | **≥3 con số ĐO ĐƯỢC**, mỗi số nói được lấy từ đâu (`gsi_map.elev()`, 自治体史…) | Ngách này người xem biết địa phương hơn mình |
| **G3** | **≥1 「痕跡」 người xem tự đi xem được** | Biến video thành thứ họ mang đi kể |
| **G4** | **Cold open ≤60 giây** và có đủ 4 câu §1 | Retention |
| **G5** | **0 câu phán xét đất/người** — quét theo `00_CHANNEL_BIBLE.md` §5 | Rủi ro 差別地名 + vu khống tài sản |
| **G6** | Bài chạm rủi ro thiên tai → **có câu miễn trừ** ở cuối + trong 概要欄 | §5 Bible |

## 4. THUẬT NGỮ — được dùng, nhưng phải trả tiền ngay

`audience-45plus.md` §5.2 cấm 外来語 khó; ở đây **thuật ngữ địa lý là đúng chất** và không thay
được. Luật thay thế: **lần đầu xuất hiện, giải thích ngay trong CÙNG một câu, bằng chữ đời thường.**

> 「扇状地、つまり、山から出た川が土砂を扇のように広げた地面ですね」
> 「後背湿地、川の堤防の裏側にできる、水はけの悪い低い土地です」

⛔ Cấm thuật ngữ trong **60 giây đầu**, trong **title** và trên **thumbnail** — chỗ đó dùng chữ
đời thường (`谷`「川の跡」「低い土地」).

## 5. NGUỒN — phải ghi trong script, không phải nhớ trong đầu

Mỗi script có mục **`## 出典`** cuối file, liệt kê từng con số ↔ nguồn:
```
標高 19m / 35m        → 地理院タイル dem_png (tools/gsi_map.py elev)
利根川東遷 1594–1654  → 国土交通省 関東地方整備局 利根川上流河川事務所
渋谷川の暗渠化 1964年 → 東京都下水道局 / 渋谷区史
```
⛔ **Không có nguồn thì không nói con số đó.** Thà bỏ một câu hay còn hơn mất kênh vì một con số
người xem tra được là sai.
