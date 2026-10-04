# CHANNEL BACKFILL — 真夜中の朗読便 (2026-07-22)

> Kết quả audit kênh qua YouTube Data API (token chouhen, có quyền ghi force-ssl).
> Mục tiêu: vá **branding kênh rỗng (cold-start)** + **metadata nghèo của video cũ** — đúng bệnh "0 impressions" đã mổ 2026-07-21.
> Rổ keyword dùng lại từ 2 lần đo đã có: Google Trends 2026-07-16 (file 04_settai) + benchmark meta đo API 2026-07-22 (CHANNEL_OPTIMIZE mục 3.5). Video MỚI tiếp theo vẫn đo trend tươi theo rule.
> ⚠️ MỌI mục dưới đây chỉ được ghi lên kênh SAU khi user duyệt.

## PHÁT HIỆN (audit 2026-07-22)

| # | Lỗ hổng | Ảnh hưởng đề xuất |
|---|---|---|
| 1 | **Mô tả kênh: TRỐNG hoàn toàn** | Cold-start: thuật toán không biết kênh nói về gì → không biết chào ai (đúng bệnh co-dai "branding rỗng") |
| 2 | **Channel keywords: TRỐNG** | Mất 1 tín hiệu phân loại kênh |
| 3 | **Banner: KHÔNG có** | Trang kênh trần trụi → người bấm vào kênh không sub (trailer có rồi nhưng đang trỏ video yếu nhất) |
| 4 | **0 playlist public** (chỉ 1 Favorites private) | Mất topic-cluster + watch-next chain — playlist là đường ray đề xuất nội bộ |
| 5 | **Video 00 (video DUY NHẤT từng được rail phân phối, 89 view): desc RỖNG, tags 0, category 22 lệch, title chưa đổi theo bản CHỐT 07-11** | Video "đầu tàu" premise-matching mà không có metadata → rail không có gì để bám |
| 6 | **Video 01: tags 0, desc 35 ký (chỉ hashtag)** — gói 概要欄 đầy đủ NẰM SẴN trong script, chưa dán | Như trên |
| 7 | **Video 02: desc 27 ký, tags 3 cái SAI định dạng (dấu # trong tag), caption srt CHƯA upload** | Như trên + mất tín hiệu phụ đề |
| 8 | **Video 03: desc 32 ký, title HỎNG (thiếu 「 mở quote), caption srt chưa upload** — 概要欄 CHỐT + タグ 25 cái nằm sẵn trong script | Như trên |
| 9 | **Video 04: desc 138 ký (mới có 3 dòng SEO, thiếu body+credit), tags 6/20** — gói FINAL đo trend 07-16 nằm sẵn | Như trên |
| 10 | **Video 06 + 07: desc tốt nhưng THIẾU credit giọng AivisSpeech + BGM** | Vi phạm rule compliance (credit bắt buộc) |
| 11 | **Title 01/02/03/04/06 còn format quote-đầu** — luật kênh 2026-07-21 đã chốt TAG-ĐẦU 【スカッとする話】 | Lệch rổ meta của related rail |
| 12 | **Video 05 (musume-no-sakubun) CHƯA TỪNG LÊN KÊNH** — nằm nhầm trong `07_UPLOADED/` (không có UPLOADED.txt, không `_upload/`), mp4+srt+thumbnail nguyên vẹn | 1 video thành phẩm nằm chết kho; lịch 1 video/ngày đang cần hàng |
| 13 | Trailer kênh đang là video 02 (yếu nhất, desc 27 ký) | Đổi sang video 07 (chuẩn mới nhất) |

Không dính: án phạt (đã check 07-21), madeForKids OK, containsSyntheticMedia không cần tick (nền footage thật + giọng TTS chỉ cần credit).

---

## A. TẦNG KÊNH

### A1. Mô tả kênh (channels.update → brandingSettings.channel.description)

```
真夜中の朗読便へようこそ。

スカッとする話・因果応報・修羅場を、耳だけで楽しめる長編朗読ドラマでお届けするチャンネルです。
義母や夫、上司に耐え続けた主人公が、最後に必ず報われる――そんな逆転の物語を、毎朝9時に配信しています。
家事のお供に、通勤のひとときに、そして眠る前に。どうぞごゆっくりお聴きください。

※当チャンネルの物語はすべてフィクションです。実在の人物・団体とは一切関係ありません。
朗読音声:AivisSpeech(morioki/阿井田茂)
```

### A2. Channel keywords (brandingSettings.channel.keywords)

```
"スカッとする話" 朗読 長編朗読 スカッと 因果応報 修羅場 "睡眠用 朗読" 聞く小説 ざまぁ 復讐 朗読ドラマ "女性向け 朗読"
```

### A3. Trailer cho người chưa sub (unsubscribedTrailer)

`cnvvHK6Uo3s` (video 02) → **`em32flDMUHw` (video 07 — chuẩn mới, metadata đầy đủ nhất)**

### A4. Playlist public mới (playlists.insert + 7 video)

- Title: `【スカッとする話】長編朗読まとめ|真夜中の朗読便`
- Description:
  ```
  義母・夫・上司に耐え続けた主人公が、最後に必ず報われる。因果応報・修羅場のスカッとする話を、長編朗読ドラマでまとめました。家事のお供や睡眠用に、耳だけでお楽しみください。毎朝9時に新しい物語を配信しています。
  ```
- Thêm 7 video public theo thứ tự 00→07.

### A5. Banner kênh (channelBanners.insert)

Bản nháp PIL style text-wall của kênh: `06_VIDEO/_series_assets/channel_banner_draft.png` (duyệt xong mới upload; muốn ảnh AI thì gen sau, banner có thể thay bất cứ lúc nào).

---

## B. TẦNG VIDEO — metadata mới từng video

> Credit block chuẩn (chèn trước hashtag của mọi video 01–07):
> ```
> ――――――――――
> 朗読音声:AivisSpeech(morioki)   ← video 03 là「阿井田 茂」
> 映像素材:Pexels
> BGM:Kevin MacLeod「Anguish」(incompetech.com) - CC BY 4.0
> ――――――――――
> ```

### B0. Video 00 — KhrVO7pnbFw (時給1350円) — desc rỗng, tags 0, cat 22→24

**Title mới (bản CHỐT sẵn trong script 00, chưa từng áp):**
```
【スカッとする話】時給1350円の派遣を切った3日後、12億円の契約が消えた――ベトナム社長「K.A.さんは?」部長「誰…?」【朗読】
```

**Description mới:**
```
時給1350円で切り捨てられた派遣社員と、3日後に消えた12億円の契約――因果応報のスカッとする話・朗読ドラマです。
家事や寝る前のお供に、耳だけで楽しめる約44分の物語。
「K.A.さんは?」――ベトナムの社長が探し続けたその名前を、部長だけが思い出せませんでした。

◆あらすじ
コスト削減の名のもとに、たった一人の派遣社員を切り捨てた会社。だが、その静かな女性こそ、海外との巨額契約を陰で支え続けてきた立役者だった。3日後、12億円の契約が音を立てて消えていく。人を「時給」でしか見なかった部長の末路を、どうぞ最後までお聴きください。

※この物語はフィクションです。実在の人物・団体とは一切関係ありません。

――――――――――
朗読音声:合成音声(AI音声)
BGM・映像素材:フリー素材
――――――――――

#スカッとする話 #朗読 #因果応報
```
(Video 00 làm ngoài repo — không chắc giọng/nguồn ảnh cụ thể → credit ghi mức tổng quát, không bịa.)

**Tags (19):** スカッとする話, スカッと, 朗読, 長編朗読, 睡眠用, 聞く小説, 因果応報, 修羅場, ざまぁ, 復讐, 朗読 ドラマ, 女性向け 朗読, スカッとする話 最新, 派遣, 派遣切り, 職場 スカッと, 逆転劇, 会社, 契約

**categoryId:** 22 → 24 (Entertainment, đồng bộ kênh)

### B1. Video 01 — bnr-t3X5VCY (息子の披露宴) — tags 0, desc 35 ký

**Title mới (bản tag-đầu #1 sẵn trong script):**
```
【スカッとする話】息子の披露宴で夫が愛人を私の隣に…黙って末席へ移った直後、新婦の祖父・銀行頭取が私に90度の最敬礼→会場凍結【朗読】
```

**Description mới (KHỐI 4 sẵn có + 3 dòng SEO mở đầu):**
```
息子の披露宴で愛人を妻の隣に座らせた夫に、新婦の祖父・銀行頭取が下す因果応報――スカッとする話の長編朗読ドラマです。
家事や寝る前のお供に、耳だけで楽しめる約65分の物語。
二十八年「ただの専業主婦」を演じてきた妻の本当の顔が明かされる結末まで、どうぞごゆっくりお聴きください。

◆あらすじ
息子の結婚披露宴。夫は愛人を私の隣に座らせ、「母親は裏方で十分だ」と言い放ちました。――けれど、新婦の祖父である銀行の頭取が、私に深く頭を下げたその瞬間から、すべてが静かに動き始めたのです。
七年の介護、消えた老後資金、そして義母が遺した一通の遺言書。すべてが繋がった時、彼が失うものとは。

※この物語はフィクションです。実在の人物・団体とは一切関係ありません。

――――――――――
朗読音声:AivisSpeech(morioki)
映像素材:Pexels
BGM:Kevin MacLeod「Anguish」(incompetech.com) - CC BY 4.0
――――――――――

#スカッとする話 #朗読 #因果応報 #修羅場 #熟年離婚
```

**Tags (19):** スカッとする話, スカッと, 朗読, 長編朗読, 睡眠用, 聞く小説, 因果応報, 修羅場, ざまぁ, 復讐, 朗読 ドラマ, 女性向け 朗読, スカッとする話 最新, 披露宴, 愛人, 熟年離婚, 夫婦, 銀行, 専業主婦

### B2. Video 02 — cnvvHK6Uo3s (元夫の結婚式) — desc 27 ký, tags sai, THIẾU caption

**Title mới (bản A tag-đầu sẵn trong script):**
```
【スカッとする話】「元嫁のお前も式を祝えよw」離婚5か月で若い女を連れて来た元夫→腕の中の生後2か月の子を見た瞬間、顔面蒼白に…【朗読】
```

**Description mới (gói sẵn có + 3 dòng SEO + credit đầy đủ):**
```
離婚からわずか5か月、若い女を連れて元嫁の前に現れた元夫に下る因果応報――スカッとする話の長編朗読ドラマです。
家事や寝る前のお供に、耳だけで楽しめる約77分の物語。
腕の中の小さな命が明かす、十年間隠されていた真実の結末まで、どうぞごゆっくりお聴きください。

◆あらすじ
「来月、俺たちは式を挙げる。元嫁のお前も、一言くらい祝ってくれよ」
若い女を連れて玄関に現れた元夫は、得意げにそう言い放ちました。——けれど、私の腕の中で眠る小さな命の顔を見た瞬間、その顔は、みるみる蒼白になっていったのです。
十年の不妊治療、七年の介護、そして「不妊の嫁」と私をなじり続けた姑。すべてに耐え、静かに捨てられた私。けれど、彼らが最も幸せの絶頂にいるその日、一枚の検査結果通知書が、十年間隠されていた真実を明らかにします。

※この物語はフィクションです。実在の人物・団体とは一切関係ありません。

――――――――――
朗読音声:AivisSpeech(morioki)
映像素材:Pexels
BGM:Kevin MacLeod「Anguish」(incompetech.com) - CC BY 4.0
――――――――――

#スカッとする話 #因果応報 #朗読 #修羅場 #離婚
```

**Tags (19):** スカッとする話, スカッと, 朗読, 長編朗読, 睡眠用, 聞く小説, 因果応報, 修羅場, ざまぁ, 復讐, 朗読 ドラマ, 女性向け 朗読, スカッとする話 最新, 離婚, 元夫, 再婚, 結婚式, 姑, 不妊

**Caption:** upload `07_UPLOADED/02_moto-otto-no-kekkonshiki/subs.srt` (ja)

### B3. Video 03 — auzXquZJEQw (百貨店外商) — title HỎNG, desc 32 ký, THIẾU caption

**Title mới (sửa quote hỏng + chuyển tag-đầu):**
```
【スカッとする話】「中卒の爺さんが社長ごっこですかｗ」歳末の百貨店で作業着の私を追い出したエリート外商→数時間後、社長が土下座しフロアが凍りついた…【朗読】
```

**Description mới:** dùng nguyên 概要欄 CHỐT 2026-07-14 trong script (hook 2 dòng đầu + ▼khối CTA + disclaimer), chỉ chốt lại credit:
```
声:AivisSpeech(阿井田 茂)
映像素材:Pexels
BGM:Kevin MacLeod「Anguish」(incompetech.com) - CC BY 4.0
```

**Tags:** dùng nguyên block タグ 25 cái trong script (スカッとする話, スカッと, 朗読, 朗読ドラマ, 因果応報, 感動する話, いい話, 泣ける話, 逆転劇, ざまぁ, 報復, 見下す, 中卒, 会長, 社長 土下座, 百貨店 外商, 作業着の老人, 高齢者 スカッと, シニア 朗読, 人生 教訓, 修羅場, 睡眠用 朗読, 作業用 朗読, スカッとする話 朗読, 老舗 百貨店)

**Caption:** upload `07_UPLOADED/03_shimotsukiya-gaisho/subs.srt` (ja)

### B4. Video 04 — TB8U7SJdaUQ (接待) — desc thiếu body+credit, tags 6/20

**Title mới (chuyển tag-đầu từ bản CHỐT):**
```
【スカッとする話】「お前の底辺旦那を今すぐ呼べｗ」人によって態度を変えるエリート上司→料亭に現れた社長が作業着の夫に90度頭を下げた瞬間、個室が凍りついた…【朗読】
```

**Description mới (3 dòng hiện tại + body draft + credit theo gói FINAL 07-16):**
```
接待の席で「底辺の作業員」と夫を嘲った上司が、すべてを失うまでの長編スカッと朗読ドラマです。
人によって態度を変える人間に、静かに耐えてきた方へ。
作業着の夫の正体が明かされる瞬間まで、どうか結末をお楽しみください。

◆あらすじ
取引先との接待の席。作業着で現れた夫を「底辺の作業員」と嘲笑った、エリート気取りの上司。しかしその夫こそ、巨大企業・天堂グループの正当な跡取りだった――。見た目と肩書きで人を選別した男が、自らの裏金と、十年前に踏みにじった恩人の存在ごと崩れ落ちていく、因果応報の長編朗読ドラマ。

※この物語はフィクションです。実在の人物・団体とは一切関係ありません。

――――――――――
朗読音声:AivisSpeech(morioki)
映像素材:Pexels
BGM:Kevin MacLeod「Anguish」(incompetech.com) - CC BY 4.0
――――――――――

#スカッとする話 #朗読 #スカッと #修羅場 #因果応報 #ざまぁ #復讐 #御曹司
```

**Tags (20, theo gói FINAL):** スカッとする話, スカッと, 朗読, スカッと朗読, 長編朗読, 朗読 ドラマ, 修羅場, 因果応報, ざまぁ, 復讐, 御曹司, 身分を隠す夫, 作業着, 接待, 料亭, 上司, 人によって態度を変える上司, 夫婦, 睡眠用 朗読, 聞く小説

### B6. Video 06 — FFLfkAj_FNw (三回忌) — thiếu credit, title quote-đầu

**Title mới (chuyển tag-đầu):**
```
【スカッとする話】「あんたの部屋は、もうこの家にないの」義母の三回忌の夜、追い出された私。だが命日の深夜一時、亡き義母が遺した"声"に義父と義妹は崩れ落ちた【朗読】
```

**Description:** giữ nguyên, chỉ CHÈN credit block chuẩn (morioki) trước dòng hashtag.
**Tags:** giữ 13 + thêm: 長編朗読, 聞く小説, 女性向け 朗読, 遺産相続, 嫁姑, スカッとする話 最新 (→19)

### B7. Video 07 — em32flDMUHw (甘味処) — chỉ thiếu credit

**Description:** giữ nguyên, CHÈN credit block chuẩn (morioki) trước dòng hashtag. Title/tags giữ nguyên (chuẩn mới).

---

## C. VIỆC NGOÀI API (làm sau khi duyệt)

1. **Video 05 chưa từng đăng:** move `07_UPLOADED/05_musume-no-sakubun/` → `06_VIDEO/`, chạy `upload_pack.py 05_musume-no-sakubun --channel chouhen` → đăng slot 09:00 JST gần nhất còn trống (23/07). Tồn kho sau đó: 08_sokurikon (đã render) cho 24/07.
2. **Banner:** duyệt bản nháp → upload qua API (hoặc gen ảnh AI đẹp hơn nếu muốn).
3. Ghi chú vào script 00–04: "metadata đã áp lên YouTube ngày 2026-07-22".

## Trạng thái

- [x] User duyệt nội dung file này (2026-07-22, duyệt "Ghi TẤT CẢ")
- [x] Apply qua API — 2026-07-22: channel desc/keywords/trailer→07/banner + 7 video (title/desc/tags/category) + caption srt 02&03 + playlist public `PLNd98oXraBbI` (7 video) — TẤT CẢ 200 OK
- [x] Verify lại bằng channel_audit.py — sạch
- [x] Video 05: move về `06_VIDEO/`, script tách về `03_SCRIPTS/`, title chuyển tag-đầu, チャプター điền timestamp thật từ srt, đóng gói `_upload/` slot **2026-07-23 09:00 JST** — chờ user kéo thả Studio + `--done`
