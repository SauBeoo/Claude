# 22 — 未支給年金・三十六万円（同じ金額が、片方は受け取れて片方は返す）

> Gói CTR + metadata upload. Kịch bản đọc: `22_mishikyu-nenkin-36man_TTS.md`
> (226 dòng · 828,4s = 13:48). Video: `06_VIDEO/22_mishikyu-nenkin-36man/`
>
> ✅ Gói CTR đã đủ (2026-09-11): Title · 3 TITLE A/B · tên file · 概要欄 · タグ ·
> **Pinned comment** · HÀNG XÓM MỤC TIÊU — xem cuối file.
> 🔴 Còn thiếu **thumbnail T3** (mới có T1/T2) ⇒ gate 3×3 của `upload_pack.py` sẽ hét.

## Đo keyword — Google Trends chế độ YouTube Search, JP, 30 ngày (2026-09-11, pytrends)

| keyword | điểm TB | max | ghi chú |
|---|---|---|---|
| **年金** | **~73,8** ⭐ | 100 | quy về cùng thang qua anchor `遺族年金`; từ DUY NHẤT có volume thật |
| 遺族年金 | 35,1 | 100 | ⛔ **KHÔNG dùng** — xem dưới |
| **未支給年金** | **0,3** | 10 | chủ thể của bài · nz 1/32 |
| 年金 死亡 | 0,5 | 15 | |
| 年金 死亡 手続き | 0,4 | 14 | |
| 死亡届 · 未支給年金 請求 · 年金 返還 · 年金 いつまで | 0,0 | 0 | chết trên YouTube search |
| 相続 年金 | 0,3 | 11 | |

Đối chiếu web search 12 tháng (lọc nhiễu mẫu nhỏ): 未支給年金 **5,7** (nz 53/53 — từ sống,
chỉ là volume nhỏ) · 死亡届 11,6 · 遺族年金 57,8.
Related (YouTube, 遺族年金): `遺族年金 計算 方法` (rising 466.200) · `遺族年金 いくらもらえる`.

🔴 **`未支給年金` là CHỦ THỂ của bài nhưng đo gần 0** → đi đường **HÌNH** (thông kê mở, 2 dòng
giống nhau khoanh đỏ), còn **CHỮ** dùng `年金`. Đúng khuôn nenkin 10 + 21
(`ab-3title-3thumb.md` §3.1 bước 5: vật nhận diện đi đường hình, keyword đo được đi đường chữ).

⛔ **KHÔNG đặt `遺族年金` lên title/thumbnail** dù nó đo 35,1: từ đó **xuất hiện 0 lần trong
video 22** (video 20 mới là bài 遺族年金). Đặt vào = sai intent + misleading metadata
(`youtube-upload-seo.md` §0.5 mục 4 · `youtube-compliance.md` mục 4). Đây đúng loại bẫy
"volume cao nhưng sai intent" mà rule nêu tên.

## 3 THUMBNAIL A/B

**Bước 1 — khuôn lấy từ ẢNH ĐÃ LÊN SÓNG** (`07_UPLOADED/21_fuyo-shinkokusho-205man/_upload/`,
lên sóng 09-07), không lấy từ tài liệu.
🔴 Tài liệu video 21 ghi T2/T3 là *"khuôn カメ先生, nền navy trơn, 0 người, chữ do
`make_thumb_kame.py` vẽ"* — **3 file live thì khác hẳn**: cả 3 đều là TELOP **chữ BAKE**, nền
sáng, **CÓ người cắt-nền bên phải**, và có thêm một **DẢI ĐỎ DỌC mép trái** (không tool nào
trong repo vẽ nổi dải dọc có chữ dọc). ⇒ tin ẢNH (đúng §3.1 Bước 1).

**Bước 2 — đo bằng máy 3 ảnh live** (1376×768):

| | dải DỌC trái | banner trên | HERO cao | HERO rộng | băng đáy |
|---|---|---|---|---|---|
| T1 `205万円` | 4,8% | 19,7% | 16,1% | 62,4% | 17,4% |
| T2 | 3,9% | 16,5% | 17,3% | 55,5% | 13,9% |
| **T3 `損します`** | 4,4% | 14,1% | **47,0%** | **81,8%** | **0%** |

⭐ **T3 live của 21 là bản AI-bake ĐẦU TIÊN của kênh vượt gate 2** (`audience-45plus.md` §1
gate 2, ≥33,3% chiều cao) — và cơ chế đo được rất rõ: **hero cao lên là nhờ BỎ BĂNG ĐÁY**
(T3 chỉ có 1 dòng kẹp trên hero, không có dòng nào dưới). Khớp đúng cơ chế "khe dọc bị chia"
mà §6.10 đã dựng giả thuyết qua 18 ca.
⚠️ **Số này chỏi số đã ghi ở `audience-45plus.md` §6.10 ca 19–20** (T2 38,7% · T3 39,8%, đo
trên bộ `make_thumb_kame`). Bộ kame **không còn trên đĩa** — file đã bị bộ AI-bake ghi đè.
Chưa sửa rule; cần user chốt lấy số nào làm bản ghi.

| | file đích | biến thử | chữ |
|---|---|---|---|
| **T1** | `thumb_T1_mishikyu-36man.png` | **baseline khuôn TELOP live** — dải dọc + banner đỏ 1/5 + hero vàng 2/3 bề ngang + băng đáy đỏ + người cắt-nền phải | 4 dòng |
| **T2** | `thumb_T2_mishikyu-36man.png` | đổi **ĐÚNG 1 biến HÌNH**: bỏ người → cận cảnh tay cầm thông kê (2 dòng khoanh đỏ), nền đổi sang xanh-xám lạnh. **Chữ giống hệt T1 từng ký tự** | 4 dòng |
| **T3** | `thumb_T3_mishikyu-36man.png` | đổi **LAYOUT**: bỏ băng đáy → hero chiếm nửa dưới khung + mặt cận trên-phải; **và chữ KHÔNG lặp title** (thử `youtube-suggested-growth.md` §6 mục 1) | 3 dòng |

**Bộ chữ — gate 7 `audience-45plus.md` §1** (che ảnh đi vẫn biết bài nói gì):

| | T1 / T2 | T3 |
|---|---|---|
| ① về cái gì | `年金を受け取るご家族へ` (banner) + `36万円` | `亡くなった月の年金` |
| ② chuyện gì xảy ra | `片方は返します` (băng đáy) | `返す分がある` (hero) |
| ③ phải làm gì / mốc | `請求が必要` (dải dọc) | `5年で消えます` (dải dọc) |

**File prompt** (`06_VIDEO/22_mishikyu-nenkin-36man/`) — sinh bằng
`python tools/thumb_prompts_22.py`, **đừng sửa tay**:

| file | vai |
|---|---|
| `thumb_prompts_FLOW.txt` | **1 prompt / 1 DÒNG** — bơm thẳng vào extension |
| `thumb_prompts_BLOCKS.md` | bản người đọc: khối + bảng số đo + bảng chữ |
| `thumb_prompts_TENFILE.txt` | thứ tự dòng FLOW ↔ tên file đích |
| `thumb_prompts_PLATE.txt` | 3 plate **KHÔNG chữ** — đường lui khi nát kanji (⛔ đừng bơm chung FLOW) |

Gate máy (in ra khi chạy tool): **TEXT @ 9% · 10% · 9%** — đều trong 15% đầu (gate CHÍNH) ✅.
Độ dài 1.781 / 1.538 / 1.670 ký, **vượt gate phụ ~1.500**. Giữ có chủ ý: prompt T1 của video
21 dài **1.734 ký, TEXT @9%** và cho ra **kanji hoàn hảo** trên ảnh live ⇒ với khuôn nenkin,
biến quyết định là **vị trí TEXT**, không phải độ dài; cắt số đo tỉ lệ để cứu 1.500 là lỗ
(đúng cảnh báo §3.1 Bước 3). Đây là ca "TEXT ở đầu + prompt dài + chữ SẠCH", ghi lại làm số đo.

### Nghiệm thu khi nhận ảnh về (chưa làm — cần ảnh)
1. **Soi TỪNG ký tự ở full-size** — `万`/`返`/`請`/`求`/`消` là kanji rậm, sai một nét là loại.
   Đặc biệt `36万円` và `5年で消えます`.
2. **Xoá watermark ✦** — `media-library.md` §2.10 ⑤b: thumbnail bake chữ thì **phải VÁ, không
   cắt** (hero chạy sát mép). Quét **cả lô** trong `~/Downloads`, soi 1:1 **cả 4 góc**.
3. Ba cửa: đọc rõ **168px** · **120px** · **ô timestamp góc dưới-phải 0% mực**.
4. Đo lại hero cao/rộng bằng máy → ghi thêm ca đo vào `audience-45plus.md` §6.10.
5. Đặt tên đúng `thumb_T1/T2/T3_*.png`; ⛔ file trung gian (bản chưa vá ✦) phải đặt **ngoài**
   pattern `thumb_T*` (`media-library.md` §2.10 ⑤b mục 7).

### Compliance
- Quét từ nhạy title/thumbnail: **sạch** — không nhóm 殺/血/死ね/自殺. `返す`/`請求`/`消えます`
  là từ tiền/thủ tục, an toàn ad. ⚠️ Cố ý **không** đặt `死亡`/`死亡届` lên thumbnail (dùng
  `亡くなった月` như lời đọc), dù nó là thuật ngữ chính thức.
- Mọi tình tiết trên thumbnail **CÓ THẬT trong video**: `36万円` hai lần (dòng 5·7·62·72) ·
  `片方は返します` (dòng 11·76) · `請求が必要` (dòng 106 「請求しないかぎり、誰の手にも渡りません」) ·
  `5年` 時効 (dòng 164·202) · `亡くなった月の分まで受け取れます` (dòng 60) · 通帳 (dòng 78).
- Người trên thumbnail là **nhân vật AI hư cấu**, không phải người thật cụ thể.
- Ảnh AI realistic trong VIDEO → vẫn phải tick **altered/synthetic content** lúc upload
  (`youtube-compliance.md` §2.1). Thumbnail AI **không** cần tick.

## 3 THUMBNAIL — BỘ PHONG CÁCH CŨ (user yêu cầu 2026-09-11: *"prompt theo phong cách cũ nữa"*)

**Chữ giống hệt bộ T1/T3 ở trên** ⇒ biến thử duy nhất là **PHONG CÁCH**. Đây là bộ để chọn
khuôn, không phải bộ A/B thứ hai — chọn xong 1 phong cách rồi mới chạy 3×3 trong phong cách đó.

Hai khuôn cũ **khác nhau hẳn**, cả hai đều đo từ ảnh đã lên sóng:

| | khuôn | đo được | file đích |
|---|---|---|---|
| **O1** | **BAKE 9 KHỐI** (video 09/10) — `03_THUMBNAIL_TITLE_FORMULA.md` §KHUÔN ĐANG KHOÁ, user chốt 2026-08-10 bằng cách dán chính ảnh 09: giấy kẻ ô kem · banner navy · hero **VÀNG CHANH** viền đen dày · **3 vòng khoanh đỏ** · **mũi tên đỏ cong TO** từ góc dưới-trái · ruy-băng đỏ nghiêng · mặt **ngạc nhiên mạnh** | banner **21,2%** · hero cao **31,7%** rộng **63,2%** | `thumb_O1_mishikyu-36man.png` |
| **O2** | **NAVY-CREAM** (video 19/20) — cùng họ nhưng **nhã hơn**: hero vàng-cam gradient, 1 ellipse mảnh, mũi tên nhỏ, ruy-băng đỏ đáy-trái, không badge | banner **19,1%** · hero cao **18,2%** rộng **63,6%** · ruy-băng **10,7%** | `thumb_O2_mishikyu-36man.png` |
| **O3** | khuôn 9 KHỐI + **hero khổng lồ** (bỏ ruy-băng, hero chiếm nửa dưới) + chữ **không lặp title** | nhắm hero ~45–47% (theo cơ chế T3 của 21) | `thumb_O3_mishikyu-36man.png` |

⭐ **Hero 31,7% của khuôn 9 KHỐI là cao nhất trong họ "có dòng phụ"** đã đo trong workspace —
đúng đỉnh dải 20–31% mà `audience-45plus.md` §6.10 dựng qua 18 ca, và **cao gần gấp đôi** khuôn
live của 21 (16,1%). Tức nếu ưu tiên gate 2 thì **khuôn cũ 9 KHỐI đang tốt hơn khuôn live**.

File: `thumb_prompts_OLD_FLOW.txt` · `_OLD_BLOCKS.md` · `_OLD_TENFILE.txt` · `_OLD_PLATE.txt`
(gate: TEXT @ 9% cả 3 ✅ · độ dài 1.620–1.731 ký).

⚠️ Khác biệt kỹ thuật cần biết khi duyệt ảnh về:
- Khuôn 9 KHỐI có **mũi tên đỏ cong to** — đây là chi tiết AI hay vẽ **đè lên hero**; soi lại
  xem mũi tên có ăn vào chữ không, và đuôi mũi tên có chạm **góc dưới-phải** (vùng timestamp).
- Badge `年金研究室` của ảnh 09 **cố ý KHÔNG đưa vào prompt** — nó là dòng chữ thứ 5, vượt trần
  4 dòng của ảnh AI. Muốn có badge thì đóng bằng tool sau khi gen (`make_thumb_45.py::badge`).

---

# ĐÓNG GÓI UPLOAD (2026-09-11)

### Title CHỐT

```
【年金の未支給】亡くなった月の36万円は、請求しないと渡りません
```

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【年金の未支給】亡くなった月の36万円は、請求しないと渡りません` | 32 | 年金@1 | keyword đo cao nhất đứng đầu + hành động ở đuôi |
| **A2** | `【年金を受け取るご家族へ】同じ36万円が二回、片方は返します` | 29 | 年金@1 | đổi tag đầu sang **chip 対象** (khuôn カメ先生 — hàng xóm gần khuôn mình nhất) |
| **A3** | `年金は自動で止まります。でも36万円は請求しないと渡りません` | 30 | 年金@1 | đổi kiểu hook: **nghịch lý tự động ↔ thủ công**, bỏ hẳn tag 【】 |

⚠️ Cả 3 bản **không lặp tag 【見逃し厳禁】** — `CLAUDE.md` §③ cấm lặp tag cảnh báo chung chung
(7/9 video cũ dùng chung một tag, kéo kênh vào feed drama). A3 cố ý bỏ hẳn 【】 làm đối chứng.

### Tên file upload

```
nenkin-mishikyu-36man-seikyu.mp4
```

### 概要欄 — 3 dòng đầu

```
亡くなったご家族の年金は、亡くなった月の分まで受け取れます。その分を、未支給年金といいます。
ところが、その後に振り込まれた同じ金額は、返すお金です。通帳の見た目は、まったく同じです。
この動画では、その線がどこで引かれるのか、そして「止めるのは自動でも、受け取るのは自動ではない」という一点を、日本年金機構と国税庁の原典を画面で開きながら確かめます。
```

### 概要欄 — Mô tả đầy đủ

```
制度を読むチャンネルではありません。あなたの数字を計算する研究室です。

年金は、二か月分の後払いです。偶数月の15日に、その前月までの二か月分が振り込まれます。ですから、亡くなられた時点では、必ず、まだ振り込まれていない月の分が残ります。これが未支給年金で、亡くなったかたの相続財産ではなく、ご家族がご自身の権利として請求するお金です。

この動画の中村さんのお姉さまの場合、4月15日の振込（2月分と3月分）36万円は正当に受け取れるお金、6月15日の振込（4月分と5月分）36万円は返すお金でした。同じ金額、同じ印字。線は、通帳ではなく、亡くなった日で引かれます。

そして、いちばん取り逃されているのが次の一点です。マイナンバーが年金の記録に結びついているかたは、年金受給権者死亡届を原則省略できます。止めるほうは自動です。ですが、未支給年金の請求は省略できません。こちらから出さないかぎり、36万円は誰の手にも渡りません。

請求できる順番は、配偶者・子・父母・孫・祖父母・兄弟姉妹・三親等内の親族の七つ。加えて「生計を同じくしていたこと」が要ります。住所が違っても、施設の職員のかたに第三者として証明していただく道が用意されています。時効は五年、数えはじめは支払日の翌月初日から。似た名前の死亡一時金（時効二年）とは別の制度です。税金は、相続税ではなく一時所得。五十万円の特別控除があります。

【目次】
00:00 同じ36万円が、二回
01:00 なぜお金が残るのか（年金は二か月分の後払い）
02:19 数字で見る：4月15日の振込と6月15日の振込
04:28 線は、通帳ではなく亡くなった日で引く
05:06 答えは届出（10日・14日とマイナンバーの省略）
06:04 止めるのは自動、受け取るのは手続き
06:18 誰が請求できるのか（七つの順番と生計同一）
08:02 持っていく書類と、マイナンバーで減らせる分
09:16 死亡届と請求書は、一枚になっています
10:05 時効は五年（死亡一時金の二年と混同しない）
10:48 税金は一時所得、五十万円の特別控除
11:34 今日の研究ノート
13:13 次回予告

次の年金支給日の前にも「直前チェック」をお届けします。

音声: VOICEVOX:雀松朱司
※令和8年8月時点の情報です。手続きや添付書類は、お一人おひとりの記録によって変わります。ご判断の前に、お近くの年金事務所でご確認ください。
```

### タグ

```
年金,老後のお金,年金と老後のお金研究室,未支給年金,未支給年金 請求,年金 死亡 手続き,年金受給権者死亡届,死亡届 年金,亡くなった 年金,36万円,生計同一,生計同一関係に関する申立書,時効 五年,死亡一時金,一時所得,特別控除,マイナンバー 年金,ねんきんネット,年金証書,戸籍謄本,住民票の除票,公金受取口座,年金事務所,遺族,相続,シニア,老後資金,65歳以上
```

### Pinned comment

```
ご視聴ありがとうございます。当研究室の、今日のノートです。

①年金は二か月分の後払い。だから、亡くなられたとき、必ず未支給年金が残ります
②亡くなった月の分までが受け取れる分。それより後の分は、返す分です（線は通帳ではなく、亡くなった日）
③年金受給権者死亡届は、厚生年金なら10日、国民年金なら14日以内。マイナンバー登録があれば原則省略できます
④ただし、未支給年金の請求は省略できません。こちらから出さないかぎり、渡りません
⑤時効は五年。数えはじめは、支払日の翌月初日から（死亡一時金の二年とは別です）

お手元で確かめる3つ → ご両親・ご主人・奥さまの年金月額の「二か月分」はいくらか／マイナンバーは年金の記録に結びついているか（ねんきんネットで確認できます）／離れて暮らしている場合、仕送りや定期的な連絡の記録は残っているか。

「もう止めてもらったはずなのに、どうしてまだ入ってくるの」— そんな経験はありましたか？　コメントで教えてください。皆さまの声が、次の研究テーマになります。

※令和8年8月時点の情報です。手続きや添付書類は、お一人おひとりの記録によって変わります。ご判断の前に、お近くの年金事務所でご確認ください。
```

### HÀNG XÓM MỤC TIÊU

- **video 20 遺族年金・四分の三** (chính kênh mình, đăng 09-06) — video này là **next-watch tự nhiên** của nó: cùng tình huống "người nhà mất", khác câu hỏi (20 hỏi *còn lại bao nhiêu*, 22 hỏi *khoản CUỐI CÙNG chưa ai lấy*).
- **カメ先生のもらえるお金** (`UCapjcw3S4HvmLWBTTHndjWQ`) — khuôn title `【◯◯の方へ】` + kỳ hạn; **A2 viết theo khuôn đó để đo**.
- Related query đo được: `年金 死亡 手続き` → `厚生年金 死亡 手続き` (top). Đây là khu phố long-tail; ⛔ **không** nhắm khu `遺族年金` vì bài không nói về chế độ đó.

### Trạng thái đóng gói

| | |
|---|---|
| video | `06_VIDEO/22_mishikyu-nenkin-36man/video_final.mp4` — **829,0s = 13:49** (hardlink từ `remotion-vox/out/n22full/final.mp4`) |
| phụ đề | `subs.srt` — **117 khối**, sinh bằng `tools/make_srt_22.py` từ `timeline.json`, kết ở 13:48,36 ✅ khớp |
| thumbnail | **2/3** — T1 (khuôn 9 KHỐI) · T2 (khuôn TELOP). 🔴 **thiếu T3** → gate 3×3 sẽ hét |
| tick upload | ⚠️ **altered/synthetic content** — video dùng footage AI người thật (`youtube-compliance.md` §2.1). Tool chưa có cờ, **tick TAY trong Studio** |

🔴 **Đường dẫn srt phải upload TAY** (`youtube-upload-seo.md` §1.2) — đường Remotion burn phụ đề vào
khung nhưng **không xuất srt**; đây là thứ `video_render.py` cũ làm hộ mà engine mới không làm.
