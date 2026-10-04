# 01_kyushoku — VISUAL PLAN + PROMPT từng đoạn (65% GEN · 25% PHOTO · 10% DRAWN)

> Mỗi entry: neo `match` = cụm trong dòng thoại (`01_kyushoku_TTS.md`) · loại · nguồn/prompt.
> **[GEN]** = gen ảnh master (prompt dưới **+ STYLE LOCK + NEGATIVE** trong `04_VIDEOGEN_PROMPTS.md` §1) → Kling i2v 6–8s.
> **[PHOTO]** = ảnh thật đã fetch (`06_VIDEO/_asset_test/`) hoặc fetch bổ sung — cú đấm "nhận ra".
> **[DRAWN]** = `make_drawn.py` giấy kraft.
> ⚠️ **SỬA 2026-08-02 (user bắt đúng): KHÔNG tái dùng clip giữa các video** — khớp luật no-reuse asset (media-library 2026-07-29) + né profile "video giống hệt nhau" (compliance §1). Ký hiệu ♻ cũ đã bỏ; mỗi video gen bộ clip mới 100%. Nhận diện kênh = STYLE LOCK + mô tả "cùng ngôi trường" trong prompt (cùng thế giới, cảnh luôn mới). Ngoại lệ duy nhất: end card 図鑑 (entry 53) = chữ ký kênh, cố định như watermark.
> Tổng: **28 GEN (trong đó 4 = demo D1–D4 đã có prompt) · 10 PHOTO · 8 DRAWN = 46 entry** ≈ 15′ video, ~3 đổi hình/phút — dưới trần 6/phút của rule 45+.

## MỞ BÀI (beat 1 — cold open + cài đố)

| # | match (câu thoại) | Loại | Nội dung |
|---|---|---|---|
| 01 | この揚げパン、覚えていますか | **GEN = D4** | Khay 揚げパン bốc hơi + bàn tay với vào (prompt D4 §3 file 04) — **hình đầu = đúng chủ thể ✅** |
| 02 | きなこと砂糖をまとった | **PHOTO** | `agepan_0.jpg` (CC0) — ảnh thật đầu tiên, đấm hoài niệm sớm |
| 03 | 四時間目の終わりに、廊下の向こうから | **GEN = D1** | Hành lang trưa nắng, hơi nước trôi (prompt D1) ♻ |
| 04 | 今日は、昭和40年代から50年代の給食を | **PHOTO** | `kujira_0.jpg` — khay 給食 昭和 nguyên bản (hero, CC BY-SA) |
| 05 | あの給食、ひと月いくらだったか | **DRAWN** | Card kraft: 「昭和の給食費　ひと月 ？円」 — ？ phóng to amber |

## KHUNG CẢNH TRƯA (beat 2–4)

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 06 | 給食室から立ちのぼる、大きな釜の湯気 | **GEN** ♻ `kyushoku_room` | `Large school kitchen in 1970s Japan, huge steel pots on gas burners, thick steam rising, two cooks in white uniforms and caps seen from behind stirring with long wooden paddles, tiled walls, morning light through high windows` · motion (8s): `one cook lifts the long paddle and taps it on the pot rim sending up a burst of steam; the second cook crosses the frame carrying an empty canister; the first resumes stirring as steam thickens` |
| 07 | カレーの日は、廊下に出た瞬間にわかる | **GEN** | `Point-of-view from a low waist-level camera height stepping out of a classroom sliding door into a wooden school corridor, sunlight, faint steam and dust in the air down the hall` · motion (8s): `the sliding door opens from the inside; camera steps out into the corridor and turns down the hall; at the far end two small figures cross carrying a tray, steam drifting after them` |
| 08 | 黒板の横には、その月の献立表 | **DRAWN** | Card kraft giả tờ 献立表 わら半紙: cột ngày + tên món, khoanh đỏ ngày 「あげパン」 (chữ do drawn lo — AI cấm gen chữ) |
| 09 | そして、給食当番 | **GEN = D2** | 2 đứa trẻ bê thùng nhôm (prompt D2) |
| 10 | シチューの食缶を、廊下でひっくり返した | **GEN** | `Wooden school corridor floor with a large aluminum canister tipped over, pale stew spilled across the boards, several students crouching around wiping the floor with cloths, seen from behind, afternoon light` · motion (8s): `one student wrings a cloth over a bucket; another slides a fresh cloth across the spill; a third comes running into frame and kneels to help as the steam from the stew fades out` |
| 11 | 机を動かして、班の形に | **GEN = D3** | Kéo bàn ghép nhóm (prompt D3) |
| 12 | お昼の放送が始まります | **GEN** ♻ `speaker_box` | `Old wooden wall-mounted school loudspeaker box near the ceiling of a 1970s Japanese classroom, viewed from below at an angle, warm light, dust particles in sunbeam, no text on the box` · motion (**3–4s, cảnh tĩnh — đừng ép 8s**): `camera tilts up slowly from the wall to the speaker box, dust drifting through the sunbeam` |
| 13 | お母さんが縫ってくれた給食袋 | **GEN** | `Close-up of small hands untying a hand-sewn drawstring cloth pouch with faded floral pattern on a wooden school desk, folded cloth napkin and gauze mask inside, warm window light` · motion (8s): `fingers untie the drawstring; hands pull out the folded napkin and shake it open; then smooth it flat on the desk, aligning the corners carefully` |

## 揚げパン + コッペパン (beat 5–6)

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 14 | 揚げパンが生まれたのは、昭和27年ごろ | **DRAWN** | Card: 「あげパンの誕生　昭和27年ごろ・東京 大田区」 |
| 15 | 硬くなったパンを、おいしく届けたい | **GEN** | `1950s Japanese school kitchen, older cook in white apron seen from the side at waist level frying bread rolls in a large pot of oil, tongs lifting a golden roll, steam and faint smoke, dim warm tungsten light, slightly darker older film look` · motion (8s): `the cook lowers a pale roll into the oil with a burst of bubbles; turns it once with long chopsticks as it goldens; lifts it out dripping and sets it on the draining rack, steam rising` |
| 16 | 口のまわりを、きなこだらけにして | **GEN** | `Close-up from the side of a student's hands holding a half-eaten sugar-coated fried bread, kinako powder dusting the desk and fingertips, aluminum tray below, no face in frame` · motion (8s): `the fingers rotate the bread once; break off a small piece with a soft crumble, kinako powder falling to the tray; the piece is carried up out of frame while the crumbs settle` |
| 17 | 大人になってから、一度、家で作ってみた | **GEN** | `Modern-feeling but timeless home kitchen at dusk, adult hands rolling a fried bread in sugar on a plate, nostalgic warm lamp light, shallow focus` · motion (8s): `adult hands roll the bread through the sugar tray; lift it and pause mid-air as if remembering something; then set it down gently and dust the sugar off the fingertips` |
| 18 | 毎日の主役、コッペパン | **GEN** | `Close-up of a plain oval koppepan bread roll on a small aluminum plate on a school desk, a foil-wrapped margarine packet and a small jam packet beside it, warm light` · motion (8s): `a small hand peels open the foil margarine packet; spreads it across the split bread with a little wooden stick; presses the bread closed and lifts it toward camera` |
| 19 | マーガリンの銀紙を、最後まできれいに折りたたむ | **GEN** | `Extreme close-up of small fingers folding a shiny silver foil wrapper into a tiny neat square on a wooden desk, aluminum tray blurred in background` · motion (8s): `fingers fold the shiny foil in half, then in half again; press it flat with a thumbnail; then flick the tiny silver square across the desk like a game piece where it spins to a stop` |

## 脱脂粉乳 cài + SỮA (beat 7–9)

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 20 | 忘れられないのが、脱脂粉乳です | **GEN** | `A dented aluminum cup of pale warm milk on a wooden school desk, thin steam, harsh morning light, slightly desaturated colder tone than other scenes` · motion (**4s, tông lạnh**): `a small hand lifts the cup halfway, hesitates, and sets it back down; the milk surface ripples and the steam thins` |
| 21 | 瓶の牛乳に替わっていきました | **PHOTO** | `bin_gyunyu_0.jpg` — chai sữa thủy tinh thật (CC BY) |
| 22 | 瓶のフタを、針でそっと外して集めた | **GEN** | `Close-up of a student's hands prying a round paper cap off a glass milk bottle with a small pin, several colorful round paper caps scattered on the wooden desk like game pieces` · motion (8s): `the pin works under the paper cap until it pops off; the hand places it on top of the stack; then slides the whole stack together like cards and spins one cap on the desk` |
| 23 | あの三角形の牛乳 | **PHOTO** | `tetrapack_0.jpg` — sữa tam giác thật (CC BY) |
| 24 | だるまストーブのそばに、牛乳を並べる | **GEN** ♻ `daruma_stove` | `Round black potbelly stove (daruma stove) in the corner of a 1970s Japanese classroom, metal fence guard around it, several glass milk bottles lined up near its base, winter light, kettle on top steaming` · motion (8s): `a student kneels into frame and adds one more bottle to the row by the stove; the kettle on top puffs steam; the student warms both hands near the stove before standing up out of frame` |
| 25 | 救世主が、ミルメークです | **PHOTO** | `milmake_0.jpg` — gói ミルメーク コーヒー thật (CC BY-SA) |
| 26 | コーヒーの粉を入れた瞬間 | **GEN** | `Close-up of brown powder being poured from a small paper sachet into a glass milk bottle on a school desk, milk swirling slightly darker, aluminum tray background` · motion (8s): `the sachet tips and brown powder streams into the bottle; a small hand swirls the bottle and the milk turns caramel; the bottle is lifted and tilted toward camera in the light` |
| 27 | 昭和42年、名古屋の | **DRAWN** | Card: 「ミルメーク　昭和42年・名古屋うまれ」 |

## おかず (beat 10–12)

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 28 | おかずの王様の登場です | **PHOTO** | `kujira_0.jpg` crop cận đĩa 竜田揚げ trong khay hero |
| 29 | しょうが醤油の下味に、カリッとした衣 | **GEN** | `Close-up of dark golden fried meat chunks (tatsuta-age) piled on a small dented aluminum plate, glossy fried coating, chopsticks lifting one piece, warm light, school desk` · motion (8s): `chopsticks lift one glossy piece into the light; it is carried up out of frame; the chopsticks return and hover over the plate choosing the next piece` |
| 30 | 袋に入った、あのソフト麺 | **PHOTO** | `softmen_0.jpg` — gói ソフト麺 thật (CC BY-SA) |
| 31 | 袋の上から四つに割ってから | **GEN** | `Small hands pressing and dividing noodles inside a clear plastic pouch into four parts over an aluminum bowl of curry stew, seen from above, school desk` · motion (8s): `hands press a cross into the pouch splitting the noodles into four; tear the corner open; drop the first block into the stew with a small splash and ripple` |
| 32 | カレーシチューに沈めた瞬間 | **GEN** | `Overhead close-up of soft white noodles being pushed into a bowl of pale yellow curry stew with a split-tip spoon (spork), stew rippling, steam` · motion (8s): `the spork pushes the noodles under the surface; they bob back up coated in pale curry; the spork lifts a tangled bite trailing sauce as steam puffs` |
| 33 | ご飯の給食が正式に始まったのは | **DRAWN** | Card timeline: 「パンの時代 → ごはん給食　昭和51年〜」 |
| 34 | あとひと口だけ、と先生に言われて | **GEN** | `A lone small figure in school clothes seen from behind sitting at a desk in an emptying classroom, tray with unfinished food in front, long afternoon shadows, other desks already cleaned, melancholic warm light` · motion (8s): `the student pokes at the tray with the spork; pauses and turns the head toward the window (face away from camera); the curtain billows once and the shadows stretch a little longer across the floor` |
| 35 | グリンピースを、パンの下に | **GEN** | `Extreme close-up of a student's fingers sliding three green peas under the edge of a bread roll on an aluminum plate, secretive angle from desk level` · motion (8s): `the first pea is nudged under the bread; the second escapes and rolls, caught just before the tray edge; the third is pushed under and the fingers pat the bread flat before darting away` |

## ĐỈNH BÀI — trả đố giá (beat 12) + CTA

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 36 | 最初の質問の答え合わせ | **DRAWN** | Card 「昭和の給食費　ひと月 ？円」 (card 05 lặp lại — nhắc lời hứa) |
| 37 | ひと月、700円 | **DRAWN** | Card đáp án: 「昭和42年　ひと月 700円　（一食 およそ35円）」 — số phóng to, khoanh đỏ SAU khi viết xong (anim) |
| 38 | 大卒の初任給は、月に、およそ3万600円 | **DRAWN** | Card so sánh 2 dòng: 「初任給 30,600円／給食費 700円 ＝ お給料の 約40分の1」 |
| 39 | (CTA canonical) | GEN nền ♻ `classroom_wide` | `Wide shot of a 1970s Japanese classroom during lunch, groups of students at joined desks seen from the back of the room, steam from trays, sunlight through windows` · motion (8s): `students eat in groups; one student stands and crosses toward the serving table with a bowl; sunlight brightens then softens as if a cloud passes` — CTA overlay tự đè lên |

## NỬA SAU (beat 14–18)

| # | match | Loại | Prompt / nguồn |
|---|---|---|---|
| 40 | 冷凍みかん | **PHOTO** | `reitomikan_0.jpg` — 冷凍みかん thật (CC0) |
| 41 | プールの授業のあとの日は | **GEN** | `Outdoor school swimming pool in 1970s Japan seen from the poolside, sparkling water, students' silhouettes with wet hair seen from behind walking away wrapped in towels, strong summer light, school building in background` · motion (8s): `the group walks away along the poolside; one towel-wrapped student breaks into a run to catch up, wet footprints trailing; the water glitters and heat haze rises at the far end` |
| 42 | 手のひらで、ころころ転がして | **GEN** | `Close-up of a small hand rolling a frosted frozen mandarin orange on a wooden school desk, condensation droplets, reddened fingertips, summer light` · motion (8s): `the palm rolls the frosted orange back and forth twice; stops; the fingers peel one strip of frosted skin with a puff of frost mist and the fingertips flush red` |
| 43 | 月に一度のお楽しみ、フルーツポンチ | **GEN** | `Aluminum bowl of fruit punch on a school tray: canned mandarin segments, pineapple pieces and one bright red cherry in clear syrup, spoon beside, warm light` · motion (8s): `the spoon dips in and lifts the red cherry dripping syrup; holds it up to the light for a beat; then lets it drop back with a small splash, bobbing among the fruit` |
| 44 | 先割れスプーン | **PHOTO** | `sakiware_0.jpg` — thìa xẻ đầu thật (CC BY-SA) |
| 45 | アルマイトの食器 | **PHOTO** | `kujira_0.jpg` crop khay/bát nhôm (hoặc fetch bổ sung bát almite đơn) |
| 46 | 落とすと教室中に響く、あの音 | **GEN** | `An aluminum bowl bouncing on a wooden classroom floor between desk legs, motion blur, students' legs and indoor shoes around, dynamic low angle` · motion (8s): `the bowl drops into frame and bounces twice with a wobble; spins on its rim slowing down; small indoor shoes gather around it and one hand reaches down to pick it up` |
| 47 | カレーシチューの日は、食缶の前に、あっという間に行列 | **GEN** | `Line of students with aluminum bowls waiting at a serving table in a classroom, seen from behind from a low waist-level camera height, big food canister and ladle, steam, one student stretching neck to see the pot` · motion (8s): `the front student holds a bowl out and the ladle pours stew into it with steam; the student turns away carefully with both hands on the bowl; the line shuffles one step forward and the next bowl is raised` |
| 48 | 最後のひとつ、じゃんけんな | **GEN** | `Close-up of two students' fists face to face above a school desk, one fried bread on an aluminum plate between them below, tense framing, warm light, no faces` · motion (8s): `the two fists shake twice in rhythm; snap open into paper versus scissors; the winning hand darts down and grabs the bread while the losing hand drops flat on the desk in defeat` |
| 49 | 大きなやかんや食缶から、ひしゃくで | **GEN** | `A large aluminum kettle pouring pale milk from a ladle into lined-up cups on a wooden table, steam, harsh post-war era light, slightly desaturated` · motion (8s): `the ladle dips into the kettle and pours milk into the first cup; moves along and fills the second; a small hand slides the full cup away as steam trails the ladle` |
| 50 | 昭和50年。府中市の給食費は | **DRAWN** | Card dòng thời gian: 「昭和42年 700円 → 昭和50年 1,900円（約2.7倍）」 — số 1,900 phóng to |
| 51 | 食器をかごに戻して | **GEN** | `Stacks of aluminum trays and bowls being returned into a wire basket on a serving table, small hands placing the last bowl on top, afternoon light` · motion (8s): `small hands place the last bowl on top; the stack tips slightly and is steadied with both hands; the wire basket is dragged to the table edge and lifted out of frame` |
| 52 | 昼休みの校庭へ、みんな駆け出して | **GEN** ♻ `schoolyard` | `View from a classroom window of a dirt schoolyard in 1970s Japan, students running out to play seen from above and behind, long afternoon shadows, metal playground equipment in distance` · motion (8s): `students burst out of the building into the yard; they scatter toward the playground equipment; one circles back to wait for a slower friend as the curtain edge sways in the foreground` |
| 53 | 昭和くらし図鑑、今日はこのページまで | **DRAWN** | End card chữ ký kênh: 「昭和くらし図鑑」 + motif trang sách khép — dùng lại mọi video ♻ |

## Đếm & việc kế

- GEN fresh: 24 + 4 demo (D1–D4 = entry 01/03/09/11) = **28 clip, gen mới toàn bộ cho video này** (không kho tái dùng — trừ end card 53) · PHOTO: 10 · DRAWN: 8 (card 36 = card 05 hiện lại trong cùng video — nhắc lời hứa, hợp lệ).
- **Thứ tự làm:** ① mày gen 4 demo D1–D4 duyệt style → ② đạt thì gen nốt 24 clip theo bảng này (ảnh master trước, duyệt, rồi i2v) → ③ tao dựng SLIDES.json từ đúng bảng match này + render.
- Ảnh PHOTO cần fetch bổ sung: bát almite đơn (entry 45 nếu không crop khay) — còn lại đã có sẵn từ test 2026-08-02.
