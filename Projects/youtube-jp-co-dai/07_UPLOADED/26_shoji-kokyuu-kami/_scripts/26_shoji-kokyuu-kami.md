# 26_shoji-kokyuu-kami — なぜ障子を手放した家に、あとからカビが生えるのか

# TARGET_QUERY: 障子
# INTENT: なぜ

> **Chế độ B (viết mới) · v2 2026-08-30 (SỬA THEO YÊU CẦU: giữ chân người xem, có hồn, hook 30s ấn
> tượng, hết rời rạc)** · **5.388 ký ≈ 16,0′** @337,5 ký/phút (không tag; render thật khả năng ~18–19′)
> · gate `check_coldopen.py 26` = **PASS 0 FAIL 0 WARN**.
> Bản đọc TTS: `26_shoji-kokyuu-kami_TTS.md` — **render bằng file đó**, bản này là bản người đọc + gói CTR.
> Trục: 🏠 **家の手入れ** (sau video 25 = signature; 家の手入れ lần cuối #24 vùng lân cận, không liền kề).

## 🔧 v2 — TỰ ĐÁNH GIÁ + 3 LỖI ĐÃ SỬA (user yêu cầu chấm điểm thật, không tự khen)

**Điểm tự chấm v1: ~6–6,5/10.** Đạt mọi gate máy (PASS 0 FAIL) nhưng "qua gate" ≠ "hay" — bài đọc như
tài liệu tổng hợp kiến thức hơn là một câu chuyện. Ba lỗi cụ thể:

1. **Cold open KỂ chứ không CHO XEM, và LỆCH LỜI HỨA CỦA TIÊU ĐỀ.** v1 mở bằng "ある家で、部屋じゅうの
   障子を外し…" — giọng báo cáo vô danh, không cảnh cụ thể. Tệ hơn: tiêu đề hứa **カビ** (mốc) nhưng
   45 giây đầu chỉ nói "nhiệt độ giảm 2-3℃" — hệ quả yếu hơn nhiều so với lời hứa. Đúng lỗi promise-
   payoff mismatch mà gate của kênh từng bắt ở video 07. **v2:** mở thẳng vào cảnh — ミツエさん sờ tay
   vào bệ cửa sổ ẩm, thấy vệt đen, biết ngay là **カビ** — đúng từ tiêu đề, đúng trong 10 giây đầu.
2. **Nhân vật ミツエさん chỉ là minh họa phụ, không phải xương sống.** v1: cô xuất hiện rời rạc vài lần.
   **v2:** biến TOÀN BỘ video thành vụ giải mã của cô — mọi chương sau đều trả lời "vậy chuyện gì đã
   xảy ra với cửa sổ của cô ấy", không phải "đây là một sự thật thú vị về 障子". Thêm chi tiết con mèo
   tránh né góc ẩm TỪ ĐẦU (biết trước cả người) để cài cắm sự trở lại ở đoạn kết — một vòng khép kín.
3. **Vài đoạn là trivia rời** (hoa văn 縦繁/横繁 theo vùng) — đúng, có nguồn thật, nhưng không phục vụ
   câu hỏi trung tâm nào. **v2:** CẮT HẲN — dồn chỗ đó cho việc làm sâu thêm mạch chính (đối lập
   "破れない・色あせない・長持ちする — số liệu không có lý do gì để không chọn" trước khi lật ngược).

**Việc giữ nguyên (đã đủ tốt):** đòn logic trung tâm (内窓 quốc gia trợ giá = cùng nguyên lý không khí
mà 障子 làm miễn phí), toàn bộ nguồn thật, cấu trúc sóng leo thang, gate cấu trúc.

## 🎯 LÝ DO CHỌN ĐỀ + TRÁNH TRÙNG VIDEO 07

User yêu cầu viết về **rèm che truyền thống**, ban đầu nhắm すだれ. Nhưng đối chiếu `07_UPLOADED/
07_natsu-denkidai-suzumi/` cho thấy video 07 (v3) đã khai thác すだれ **cực sâu** — đúng những góc user
liệt kê (cơ chế ngoài/trong cửa sổ, khoảng cách treo cách kính để khí nóng thoát, thứ tự treo hướng
Tây trước, so sánh với rèm dày, cơ chế 軒 theo góc mặt trời). Viết thêm 1 video すだれ mới sẽ trùng lặp
nặng — đúng thứ user không muốn ("kiến thức tầm thường/đã biết"). Đã hỏi lại user 3 phương án
(暖簾/障子/đào sâu thêm すだれ) → **user chọn 障子** (cửa giấy shoji).

⚠️ **Lưu ý mùa vụ:** `00_TOPIC_LOG.md` từng đo `障子` = 37–55 điểm và ghi "để dành mùa thu" vì related
`障子紙 張り替え` breakout +160% — mùa cao điểm 張り替え thật là 10–12月 (năm cuối 大掃除). Video này viết
**cuối tháng 8**, hơi sớm cho đỉnh mùa search, nhưng nội dung được thiết kế **evergreen** (xoay quanh cơ
chế + lịch sử + mẹo bảo quản, không neo cứng vào "làm sạch cuối năm") nên vẫn đứng được ở thời điểm khác.
Nếu muốn tối ưu mùa vụ, có thể giữ slot này lùi sang 10月.

```
TARGET_QUERY: 障子
INTENT: なぜ
```

## 🧭 XƯƠNG SỐNG

```
Nhà bỏ hết 障子, thay rèm nhựa dễ vệ sinh → mùa đông đó bị mốc quanh cửa sổ
→ vì sao? 障子紙 là "màng hô hấp": dẫn nhiệt kém + lớp không khí giữa giấy-kính = cách nhiệt
  (6.0 → 4.8 W/m²K khi thêm 障子; ガラス90% nhiệt xuyên qua → 障子 hạ còn 40-50%)
  + xơ giấy có khe hở li ti cho ẩm thấm qua từ từ = điều hòa độ ẩm, giấy nhựa "không rách" bịt kín
  khe đó → mất khả năng thở → đọng sương → mốc (đúng cái đã xảy ra ở cold open)
→ phản trực giác: giấy ướt CO GIÃN — dán xong CHỦ ĐỘNG xịt nước để giấy co lại căng như mặt trống,
  đây là kỹ thuật DIY thật, không phải lỗi
→ mẹo thất truyền: sáp nến bôi rãnh trượt (không hút bụi như xịt silicon) — nhưng phải lau sạch bụi
  trước; hướng Tây phai màu nhanh hơn hướng Bắc/Nam (lignin phản ứng UV) → thứ tự thay giấy theo hướng
→ lịch sử: chỉ nhà giàu/samurai mới có được tới giữa Edo, phổ biến dân thường cuối Edo, công nghiệp
  hóa Taisho/Showa mới rẻ — CÀNG RẺ CÀNG DỄ MẤT kỹ năng bảo quản đi kèm; nghề 表具師 (thợ dán giấy)
  đang suy giảm theo đà chung của thủ công truyền thống (28 vạn → 6 vạn thợ, 1983→2016)
→ dòng tiền: chính phủ trợ giá tới 14万円/cửa (100万円/nhà) cho 内窓 hiện đại — cơ chế cách nhiệt của nó
  (2 lớp kính + lớp không khí giữa) VỀ NGUYÊN LÝ giống hệt lớp không khí mà 障子 tạo ra miễn phí khi
  treo cách kính — cấu trúc, không cáo buộc công ty cụ thể
→ kết: không phải chọn giấy hay kính, mà là hiểu cả hai nguyên lý rồi kết hợp theo nhà mình
```

## 📐 KẾT QUẢ GATE — `python tools\check_coldopen.py 26`

**✅ PASS 0 FAIL 0 WARN.** Vào bài ~15s (marker — NHANH HƠN v1 nhờ mở thẳng vào cảnh) · cửa 45s 0 câu
không trả tiền · gap payoff max 1′37″ · dài **16,0′** ≈ 4 sóng (mô hình leo thang) · **7 cú lật** ·
**11 câu MỞ** · loop lớn đóng ở **88%** (trần ≥78%).

⚠️ **Độ dài 16,0′ ngắn hơn v1 (18,6′) và ngắn hơn chuẩn kênh 25′** — CỐ Ý, vì mục tiêu lượt sửa này là
CHẤT LƯỢNG (hook/mạch truyện/hồn), không phải số phút. Đã cắt hẳn 1 đoạn trivia (hoa văn 縦繁/横繁 theo
vùng) không phục vụ mạch chính, và nén nhiều đoạn diễn giải rời thành câu ngắn/thoại. **Việc còn mở nếu
muốn kéo lên 25′ mà KHÔNG làm loãng lại:** thêm 1 nhân vật/case thứ hai (nhà khác, vấn đề khác của cùng
cơ chế 障子) thay vì kéo dài phần giảng, hoặc mở rộng đoạn lịch sử Edo bằng chi tiết khu phố cụ thể hơn.

Chất người: **6/6** — ① tự trào (đóng nhầm mặt trước-sau, bị mẹ chê cười) ② nhân vật ミツエさん có 3 lượt
thoại + chi tiết đời sống vô dụng (con mèo tránh né rồi quay lại góc cửa sổ — cài từ đầu, khép vòng ở
kết) ③ ký ức giác quan (ánh sáng chiều tà qua giấy, lỗ thủng bị mắng thời nhỏ) ④ tự thử kỹ thuật xịt
nước làm căng giấy ⑤ đóng nhân vật ミツエさん bằng cảm xúc + hình ảnh con mèo (không kết luận) ⑥ ≥3 chỗ
phá nhịp câu (câu cụt liên tiếp "破れない。色あせない。長持ちする。", "ぴんと張った、あの瞬間。").

**9+ nguồn thật đã fetch/verify (WebSearch 2026-08-30), KHÔNG bịa:**
1. くらしのマーケットマガジン/uchimado-club — 熱貫流率: 単板ガラス**6.0**W/m²K → アルミサッシ+ガラス+障子**4.8**
   (Low-E複層参考: 1.6) · 障子閉めると体感温度**2〜3℃**上昇
2. tori-matsu.jp/madokara — 太鼓張り(組子両面貼り、雪国の二重窓的工夫) · ガラス通過率**約9割** → 障子で
   **4〜5割**まで抑制（別測定・別出典、ソフトに併記）
3. DIYドア通販/前田畳店 — 障子紙は水で伸縮、貼り替え後に霧吹きで水を与えて陰干し→乾燥収縮でピンと張る
4. 国立国会図書館レファレンス/Wikipedia「障子」 — 語源（障=遮る・子=もの）、平安末期「明かり障子」誕生、
   南北朝時代に和紙生産増で普及
5. LIFULL HOME'S PRESS等 — 江戸中期まで武家・裕福な商人層のみ、江戸中期以降庶民へ、大正〜昭和に機械量産
6. くらしのマーケット「障子の裏表」 — 組子（細かい桟）を室内側に見せ外側はなめらか（日本の慣習、一説として軟表現）
   ⚠️ **v2: KHÔNG dùng trong bài** — cùng đợt fetch với nguồn #7 (横繁/縦繁 vùng miền), cả hai bị CẮT khỏi
   script vì là trivia không phục vụ mạch chính ミツエさん. Giữ ở đây làm tư liệu dự phòng nếu sau này
   viết video riêng về 建具の意匠.
8. DIYドア通販/敷居すべりコラム — 敷居にろうそくの蝋を塗ると滑りが改善（脂肪酸が木目に浸透、伝統的知恵）
9. curama.jp/DIYドア通販 — プラスチック障子紙は破れにくく耐候性◎・寿命約10年だが**通気性低く結露・カビの
   リスク**あり；和紙糊は水溶性(でんぷん糊)で水で剥がせる、プラスチック紙は水を弾きアイロン/ドライヤーで
   加熱して剥がす
10. meetsmore.com/コメリ/前田畳店 — 障子紙価格: ダイソー100円〜、ホームセンター980〜4000円；業者張り替え
    1枚2000〜15000円目安；和紙の寿命は3〜4年
11. 環境省 先進的窓リノベ2026事業（公式サイト） — 内窓設置1箇所あたり最大**14万円**、戸建て最大**100万円**、
    申請は窓リノベ事業者が代行
12. curama.jp/金沢屋 — 障子紙の変色はリグニン成分の紫外線反応、西向きの部屋は劣化が早い
13. journal.thebecos.com（伝統工芸の後継者不足） — 伝統工芸職人**1983年28万人→2016年6万人**、生産額
    **5400億円→960億円**（※表具師固有の数字ではなく伝統工芸全体の統計と明記して使用——本文でも「伝統工芸
    全体で見ると」と限定して言及、対象を誤魔化さない）

⛔ **KHÔNG dùng lại nguồn của video 07** (業界試算7割/軒/太陽高度/緑のカーテン蒸散) — hoàn toàn khác vật,
khác cơ chế, đã kiểm tra không trùng.

---

## 🎬 KHỐI 2 — 3 TITLE A/B

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜ障子を手放した家に、あとからカビが生えるのか――紙一枚に隠された「呼吸」の仕組みでした` | 44 | 障子@2 | vật cụ thể + なぜ + hệ quả sốc, đúng khuôn kênh |
| **A2** | `なぜ国は、窓一つに14万円を払ってでも、あの薄い紙の仕組みを取り戻そうとしているのか` | 41 | 障子@ẩn(「紙」thay) | đổi keyword dẫn: mở bằng con số tiền của nhà nước thay vì hậu quả cá nhân |
| **A3** | `紙1枚とろうそく1本――祖父母の家が、電気なしで涼しく暖かかった理由` | 33 | 障子@ẩn | đổi kiểu hook: liệt kê vật cụ thể + hành động tối giản, thay vì câu hỏi なぜ trực tiếp |

## 🖼️ KHỐI 3 — TEXT THUMBNAIL 3 TẦNG

- Tầng 1 (dẫn, 6字): 「知らずに外した」
- Tầng 2 (từ khóa chính, TO NHẤT, 2字): 「障子」
- Tầng 3 (hệ quả, 6字): 「紙は呼吸してた」
- Badge: 「0円の断熱」

## 🎨 KHỐI 4 — PROMPT ẢNH THUMBNAIL (3 bản T1/T2/T3, khuôn **B1 lồng K4 Before/After split dọc**)

Tránh **K1** + **K6** (2 khuôn của video 25 và chỉ thị "video kế tiếp tránh K1+K6"). K4 lần cuối lên
sóng ở #16, cách 9 video → hợp lệ. K4 khớp tự nhiên với xương sống: **before** (障子 đã bị tháo, cửa sổ
trần trụi có vệt mốc mờ ở góc kính) ↔ **after** (障子 nguyên vẹn, ánh sáng dịu qua giấy, khô ráo).

✅ **Đã xuất đủ 4 file** theo `ab-3title-3thumb.md` §3.1 Bước 4, thư mục
`06_VIDEO/26_shoji-kokyuu-kami/`:
- `thumb_prompts_FLOW.txt` — 3 prompt, mỗi prompt 1 dòng, import thẳng extension (T1→T2→T3)
- `thumb_prompts_BLOCKS.md` — bản khối để đọc/sửa (đầy đủ 3 prompt + số đo)
- `thumb_prompts_TENFILE.txt` — thứ tự dòng FLOW ↔ `thumb_T1/T2/T3_shoji.png`
- `thumb_prompts_PLATE.txt` — 3 plate KHÔNG chữ dự phòng khi bake chữ nát kanji (**file riêng**,
  đừng trộn vào FLOW.txt)

Đo máy: **TEXT block @8–9%** (trần 15%) · **1.225–1.478 ký** (trần 1.500) ✅ cả 3 bản.

**T1 (baseline):** trái = khung cửa mốc (hệ quả) · phải = 障子 ấm áp.
**T2 (đổi ĐÚNG 1 biến hình, chữ y nguyên):** trái đổi thành tay đang treo rèm nhựa (đưa NGUYÊN NHÂN
vào khung thay vì chỉ hệ quả), 障子 cũ bị tháo dựng cạnh tường · phải giữ nguyên.
**T3 (đổi layout):** bỏ chia đôi dọc → macro giọt nước đọng trên giấy washi (ẩn dụ "hô hấp"), chữ
dồn cột trái chiếm 1/3 khung, ảnh chiếm 2/3 phải.

🚫 Không mặt người (luật kênh 2026-08-05) — chỉ bàn tay được phép.
⚠️ Sau khi gen: xoá watermark ✦ theo `media-library.md` §2.10⑤b (bake chữ ⇒ **VÁ, không cắt**) →
`stamp_brand.py --pos tr` → duyệt 3 cửa (che chữ / cạnh sheet cũ / preview 168px + 120px).

## 📌 KHỐI 5 — PINNED COMMENT

```
今日の話、最後までご覧いただきありがとうございます。ご紹介した中で、まず今日試してみたいと思われたのは、
敷居のろうそくでしたか、それとも障子を光にかざして確かめる方法でしたか。よろしければ、コメントで教えてください。
そして、ご実家に障子の貼り替えの記憶が残っていましたら、ぜひ聞かせてください。
皆さまの記憶を参考に、これからの内容も深めてまいります。
```

## 📁 Tên file upload

```
shoji-kokyuusuru-kami-kabi-danshitsu.mp4
```

## 📋 3 dòng đầu

```
窓のふちを指でなぞると、じっとりと湿っていました。よく見ると、黒い点々——カビでした。半年前、障子を
外して洗える樹脂のカーテンに替えた、その窓です。紙一枚が消えただけで、なぜここまで変わってしまったのか。
呼吸する紙という、ほとんど知られていない仕組みを、古代の秘訣がご紹介します。国が今、14万円をかけて
取り戻そうとしている仕組みは、あなたの家にすでにあった紙一枚と、同じ原理でした。
```

## 📋 Mô tả đầy đủ

```
窓のふちを指でなぞると、じっとりと湿っていました。よく見ると、黒い点々——カビでした。半年前、障子を
外して洗える樹脂のカーテンに替えた、その窓です。紙一枚が消えただけで、なぜここまで変わってしまったのか。
呼吸する紙という、ほとんど知られていない仕組みを、古代の秘訣がご紹介します。国が今、14万円をかけて
取り戻そうとしている仕組みは、あなたの家にすでにあった紙一枚と、同じ原理でした。

【目次】※render済みprojectのsceneMarkers実測値（推定ではありません）
00:00 窓辺に生えたカビの謎
01:28 障子の隠れた性能——数字で分かる断熱
02:58 「破れない障子紙」に隠された見落とし
05:14 水が紙を生き返らせる仕組み
06:59 自分で貼り替える方法と道具
08:56 敷居のろうそくという知恵
10:14 障子の歴史——安さと引き換えに消えたもの
13:08 国が14万円で売る仕組みの正体
15:11 まとめ——紙とガラス、両方を知るということ

障子紙は、ただ光を通すだけの紙ではありません。繊維のあいだの目に見えないすきまが、部屋の湿気を少しずつ
外へ逃がし、ガラスとのあいだにできる空気の層が、熱の出入りをやわらげています。「破れない」プラスチック
障子紙は便利な一方、この呼吸を失い、結露やカビを招くことがあります。

障子紙は、水を含むと伸び、乾くと縮みます。貼り替えたあと、あえて霧吹きで水を与えて陰干しにすると、
太鼓の皮のようにぴんと張った仕上がりになります。敷居の滑りが悪いときは、ろうそくの蝋を溝に塗るという、
昔からの知恵も残っていました。

明かり障子が生まれたのは平安時代の終わりごろ。当時は武家や裕福な商人だけのものでしたが、江戸時代の
半ばを過ぎてから庶民の家にも広がりました。安く手に入るようになった今のほうが、貼り方や手入れの知恵は、
かえって忘れられやすくなっているのかもしれません。

※本動画は、暮らしの中の生活の知恵・忘れられた技術をご紹介する情報コンテンツです。ご紹介した数値・統計は、
各種公開情報・業界記事にもとづく目安であり、住宅の構造や環境により差があります。刃物を扱う作業では、
お子様の周囲には十分ご注意ください。

ご感想や、ご実家に残る障子の記憶があれば、ぜひコメントで教えてください。高評価やシェアで「古代の秘訣」を
応援していただけると、今後の内容もより深めてまいります。
```

## 🏷️ タグ (rổ 12 cố định + riêng)

`古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, 障子, 障子紙, 断熱, 結露, カビ対策, 内窓, 表具師, 和紙`

#生活の知恵 #昔の知恵 #古代の秘訣 (3 hashtag cuối desc)

---

## ⚠️ VIỆC CÒN LẠI TRƯỚC KHI RENDER

1. **Độ dài 16,0′ (v2) ngắn hơn cả v1 (18,6′) và chuẩn kênh 25′** — CỐ Ý đánh đổi lần sửa này: ưu tiên
   siết chặt mạch truyện/hook, cắt trivia, không kéo dài bằng cách pha loãng. Nếu muốn vừa dài vừa chặt,
   cách đúng là thêm 1 case/nhân vật thứ hai (xem gợi ý ở mục KẾT QUẢ GATE), không phải nhồi thêm diễn giải.
2. ✅ **Dựng bằng REMOTION (không phải SLIDES/make_vox cũ)** — `voice_only.py` xong (16,76′, 49
   dòng) → `build_remotion_26.py` (46 scene) → **`check_frame_pace.py`: SẠCH 3/3** (khe dài nhất
   5,5s, trần đổi hero 2,45/phút, 0 scene nền trống — đã sửa bằng cách xoay vòng 2 sticker/scene
   qua 4 vị trí mỗi ~5,5s, KHÔNG thêm ảnh mới, KHÔNG tăng đổi hero). Còn thiếu: **41 photocard +
   92 sticker** (prompt đã xuất ở `06_VIDEO/26_.../art_prompts_photocard_FLOW.txt` +
   `sticker_prompts_FLOW.txt`) → user gen → `make_photocard26.py --apply` +
   `cutout_sticker26.py --apply` → chạy lại `build_remotion_26.py` tới khi hết 🔴 THIẾU asset.
3. 3 thumbnail (user gen theo Khối 4) → xoá watermark → `stamp_brand.py` → duyệt 3 cửa.
4. Sau khi đủ asset: still ≥10 frame (`npx remotion still`) duyệt mắt → render nền (`.cmd` có
   `call npx`) → đo giây thật, sửa lại 目次 trong mô tả cho khớp.
5. Cân nhắc thời điểm đăng: nội dung evergreen nhưng cầu search thật của `障子` mạnh nhất 10–12月 (mùa
   張り替え cuối năm) — có thể giữ slot này cho 10月 nếu muốn tối ưu, hoặc đăng ngay nếu cần lấp lịch.
