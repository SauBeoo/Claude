# 01_kyushoku VISUALS v2 — BẢN 4 (2026-08-07) · ~50 entry ≈ 3,6 đổi hình/phút

> Khớp script BẢN 4 trong `01_kyushoku.md`. Visual v3 của kênh: **ảnh AI TĨNH + pan** (không i2v/motion) · ảnh thật mỗi ảnh 1 LẦN · drawn card cho mọi số/chữ · 2 clip PD gia vị.
> **[GEN]** = gen ảnh (prompt block bên dưới, đã gộp sẵn STYLE + Avoid — copy nguyên block) · **[PHOTO]** = ảnh thật đã có trong `06_VIDEO/_asset_test/` · **[DRAWN]** = `make_drawn.py` kraft · **[PD]** = cắt từ phim PD đã tải.
>
> ## CÁCH GEN TAY (đường B)
> 1. Mở **aistudio.google.com** (model ảnh, vd Nano Banana / Gemini image) hoặc **gemini.google.com** — khổ **16:9**, mỗi cảnh gen **2–3 bản**.
> 2. Copy NGUYÊN một block prompt (đã có style + avoid) → dán → gen.
> 3. Lưu bản ưng nhất thành **`gen_G◯◯.png`** (đúng mã số entry) vào `06_VIDEO/01_kyushoku_v2/gen_raw/`.
> 4. Loại thẳng bản có: đồ hiện đại · chữ/ký hiệu đọc được · mặt người rõ · bàn tay dị dạng. Cảnh nào gen mãi vẫn hỏng → bỏ qua, báo tao hạ cảnh đó về ảnh thật/drawn.
> 5. Đủ ảnh → tao chạy `grade_vintage.py` (grain + vignette đồng bộ) + contact sheet duyệt lần cuối.
>
> STYLE đuôi mỗi prompt: `1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.`
> (các block dưới ĐÃ dán sẵn đuôi này — cứ copy nguyên block)

---

## MỞ BÀI (cold open + luật chơi + cài đố)

**G01** · match 「この揚げパン、覚えていますか」 · *hình đầu = chủ thể* ✅
```
Close-up of a dented aluminum school lunch tray on a wooden desk: one sugar and kinako coated fried bread roll on a small aluminum plate, a glass milk bottle with paper cap, aluminum bowl of pale stew, thin steam rising, warm window light, shallow depth of field, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**P02** · 「きなこの粉で、口のまわりを」 · PHOTO `agepan_orig.jpg` (CC0 — cú đấm thật sớm)

**G03** · 「昭和45年ごろ。あなたが、小学生だった頃」
```
Wide view of a 1970s Japanese elementary school classroom at lunchtime seen from the back corner, students in simple shirts seen from behind sitting at small wooden desks with aluminum trays, one student walking between desks carrying a tray, warm noon light through large sliding windows, old dark wooden floor, cloth bags hanging on desk hooks, no faces visible, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D04** · 「ルールは、ひとつだけ」 · DRAWN card kraft: title 「きょうのルール」 · lines 「おぼえていたら 1点」「全部で 10点満点」 · highlight dòng 1

**D05** · 「ひと月いくらだったか」 · DRAWN card: 「昭和の給食費　ひと月 ？円」 · ？ amber phóng to (giữ khuôn cũ)

## 一品目 揚げパン (1点)

**G06** · 「さて、一品目は、その揚げパンから」
```
A single kinako-dusted fried bread roll on a small dented aluminum plate photographed from a low angle on a wooden school desk, golden powder scattered around it, backlit steam, warm afternoon sun through a window behind, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G07** · 「生まれたのは、昭和27年ごろ」 (tông tối hơn, thời khó)
```
1950s Japanese school kitchen, an older cook in white apron seen from the side at waist level frying bread rolls in a large pot of oil, long cooking chopsticks lifting one golden roll, steam and faint smoke, dim warm tungsten light, slightly darker aged film look, tiled wall, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D08** · 「東京、大田区の嶺町小学校」 · DRAWN card: 「あげパンの誕生」 / 「昭和27年ごろ・東京 大田区」 / 「お休みの子への思いやりから」

**G09** · 「じつは私、大人になってから、家で作ってみた」
```
Adult hands rolling a fried bread roll through kinako powder on a plate in a dim timeless home kitchen at dusk, nostalgic warm lamp light, shallow focus, quiet mood, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G10** · 「四時間目の空腹」「廊下の向こうから、あの匂い」
```
Empty wooden school corridor in a Japanese elementary school, long row of sliding wooden-framed windows on one side, warm noon sunlight casting window shadows on polished wooden floor, faint steam drifting from the far end of the corridor, small indoor shoes neatly lined at a classroom entrance, view down the corridor from a low waist-level camera height, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D11** · 「わら半紙の献立表」 · DRAWN table わら半紙: cột thứ + món, khoanh đỏ 「あげパン」 (giữ spec cũ)

## 二品目 コッペパン (2点)

**G12** · 「二品目は、毎日の主役、コッペパン」
```
A plain oval koppepan bread roll lying on a small aluminum plate on a wooden school desk, a foil-wrapped margarine packet beside it, aluminum tray at the edge of frame, warm side light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**PD-A** · 「戦後、海の向こうから届いた小麦粉」 · PD clip *You in Japan* (1957) — cảnh đời sống hậu chiến/cảng, 6–8s, MUTE (đoạn không nhạc)

**G14** · 「銀紙を、最後まで小さく折りたたむ」
```
Extreme close-up of small fingers folding a shiny silver foil wrapper into a tiny neat square on a wooden school desk, aluminum tray blurred in the background, warm window light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**P15** · 「食べきれなかったパンは、そっと机の中へ」 · PHOTO `koppepan_0.jpg`

## Interlude 給食当番

**G16** · 「その週の給食当番です」
```
Two Japanese students seen from behind, wearing white cooking aprons, white caps and gauze masks, carefully carrying a large dented aluminum food canister together down a wooden school corridor, steam rising from the canister, warm light from windows, other students' silhouettes far in the background, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G17** · 「シチューの食缶を、廊下でひっくり返した」
```
Wooden school corridor floor with a large aluminum canister tipped over on its side, pale cream stew spilled across the floorboards, several students crouching around it wiping the floor with cloths, seen from behind at floor level, afternoon light, no faces visible, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 三品目 瓶牛乳 (3点) — cài 脱脂粉乳

**G18** · 「忘れられないのが、脱脂粉乳」 (tông lạnh hơn nền)
```
A dented aluminum cup of pale warm milk on a wooden school desk, thin steam, harsh flat morning light, slightly desaturated colder tone, quiet and austere mood, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**P19** · 「瓶の牛乳がやってきました」 · PHOTO `bin_gyunyu_0.jpg`

**D20** · 「1本25円。統計局の記録に」 · DRAWN table: 「牛乳（配達・瓶）」/「1本 25円」/ note 「※昭和45年・東京　統計局の記録より」

**G21** · 「だるまストーブのそばに、ずらりと並べて」
```
Round black potbelly daruma stove in the corner of a 1970s Japanese classroom, metal fence guard around it, several glass milk bottles with paper caps lined up near its base, a steaming kettle on top, winter morning light, heat shimmer in the air, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G22** · 「瓶のフタ。針で、そっと外して」
```
Close-up of a student's hands prying a round paper cap off a glass milk bottle with a small pin, a stack of colorful round paper milk caps beside it on the wooden desk like game pieces, warm window light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 四品目 三角牛乳 (4点)

**G23** · 「牛乳は瓶ではなく、あの三角形」 ⚠️ AI hay vẽ sai khối tứ diện — gen 3–4 bản, chọn bản ĐÚNG hình kim tự tháp 4 mặt; hỏng cả thì báo tao fetch ảnh thật thứ 2
```
Several white tetrahedron-shaped paper milk cartons (triangular pyramid shape, tetra classic package) stacked in a wooden crate on a school table, one carton in front with a thin paper straw stuck in its corner, warm noon light, plain packaging without any text, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G24** · 「ストローの袋を、ぷっと飛ばして」
```
A thin paper straw wrapper flying through the air above wooden school desks, blurred classroom background with students seen from behind, frozen playful moment, warm afternoon light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 五品目 ミルメーク (5点)

**P25** · 「牛乳の救世主、ミルメーク」 · PHOTO `milmake_0.jpg` (CC BY-SA)

**D26** · 「昭和42年、名古屋の会社から」 · DRAWN card: 「ミルメーク」/「昭和42年・名古屋うまれ」/「牛乳が、ごほうびに変わる」

**G27** · 「コーヒー牛乳色に変わっていく」
```
Close-up of brown cocoa-like powder streaming from a small torn paper sachet into a glass milk bottle on a school desk, the milk swirling into caramel color, aluminum tray blurred behind, warm window light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## Interlude 教室の風景

**G28** · 「机をガタガタと動かして、班の形に」
```
Interior of a 1970s Japanese elementary school classroom, students in simple shirts seen from behind and from the side pushing small wooden desks with metal legs together into island groups, warm afternoon light through large windows, old dark wooden floor, cloth school bags hanging on desk hooks, no faces clearly visible, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G29** · 「お昼の放送が流れていました」
```
Old wooden wall-mounted school loudspeaker box near the ceiling of a 1970s Japanese classroom, viewed from below at an angle, warm light, dust particles drifting in a sunbeam, plain box without any text, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G30** · 「お母さんが縫ってくれた給食袋」
```
A small hand-sewn drawstring cloth pouch with a faded tiny floral pattern lying on a wooden school desk, a folded white cloth napkin and a gauze mask peeking out, warm window light, shallow depth of field, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 六品目 鯨の竜田揚げ (6点)

**P31** · 「鯨の竜田揚げです」 · PHOTO `kujira_orig.jpg` crop bát 竜田揚げ (CC BY-SA)

**G32** · 「しょうが醤油の下味に、カリッとした衣」
```
Close-up of dark golden-brown tatsuta-age fried meat chunks piled in a dented aluminum bowl on a school lunch tray, crispy coating with visible texture, faint steam, warm side light, shallow depth of field, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D33** · 「昭和35年、鯨のお肉は、1キロ、およそ134円」 · DRAWN table + anim: 「くじらのお肉　1キロ 134円」/「牛肉の 4分の1」/ note 「※昭和35年　旧総理府統計局の記録より」 · circle dòng 2

**D34** · 「牛肉より、鯨のほうが多かった」 · DRAWN table: 「1年間に食べたお肉（ひとり・昭和35年）」/「くじら 1.6キロ」「牛肉 1.5キロ」/ note 「※農水省 食料需給表より」 · circle dòng くじら

## 七品目 ソフト麺 (7点)

**P35** · 「あのソフト麺」 · PHOTO `softmen_0.jpg`

**P36** · 「カレーシチューに、ひと切れずつ沈めていく」 · PHOTO `curry_0.jpg` (crop)

**D37** · 「ご飯の給食が正式に始まったのは、昭和51年」 · DRAWN flow: 「給食の主食」/「パンの時代 → ごはん給食　昭和51年〜」

**P38** · 「グリンピースが苦手で」 · PHOTO `peas_0.jpg`

## TRẢ ĐỐ GIÁ (đỉnh 1) + CTA

**D39** · 「答え合わせです」 · DRAWN card: 「昭和の給食費　ひと月 ？円」 (lặp lại card D05 — cùng ảnh, hợp lệ vì drawn tự render)

**D40** · 「ひと月、700円」 · DRAWN table **anim** (viết dần): 「昭和42年の給食費」/「ひと月 700円」「一食あたり 約35円」/ note 「※東京・府中市の記録より」 · circle dòng 700円

**D41** · 「さっきの牛乳を、思い出してください」 · DRAWN table **anim**: 「35円で、なにが買えた？」/「牛乳（配達） 1本 約21円」「給食 一食 35円」「牛肉ロース 100g 202円 ＝ 給食6食分」/ note 「※昭和42年・東京　統計局の記録より」 · circle dòng 牛肉

**D42** · 「翌年の大卒の初任給が」 · DRAWN table **anim**: 「お給料とくらべると」/「大卒の初任給 30,600円」「給食費 700円」「割合 約40分の1」/ note 「※初任給は昭和43年・賃金構造基本統計」 · circle dòng 割合

**G43** · nền CTA 「ここで、ひとつだけお願いです」
```
A 1970s Japanese elementary school classroom bathed in golden afternoon light, empty desks with aluminum trays cleared away, long window shadows across the wooden floor, peaceful and warm, seen from the doorway, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 八品目 冷凍みかん (8点)

**G44** · 「八品目、冷凍みかん」
```
Four frosted frozen mandarin oranges covered in white ice crystals in a small aluminum bowl on a school lunch tray, condensation droplets, cold fresh look against warm wooden desk, window light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**P45** · 「プールの授業のあとの日は」 · PHOTO `pool_0.jpg`

**P46** · 「フルーツポンチ。さくらんぼが入っていた日」 · PHOTO `fruitponchi_0.jpg`

## 九品目 道具 (9点)

**G47** · 「先割れスプーン、あの一本で」
```
Close-up of a well-used stainless steel spork (combination spoon with short fork tines at the tip) lying diagonally on a dented aluminum school lunch tray, small scratches on the metal, warm window light reflecting softly, wooden desk beneath, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**P48** · 「アルマイトの食器」 · PHOTO `almite_0.jpg`

**G49** · 「三角食べ、なんて言葉も」
```
Overhead flat-lay view of a complete Japanese school lunch on a dented aluminum tray: koppepan bread on a plate, aluminum bowl of stew, glass milk bottle, small bowl of vegetables, spork laid neatly, on a wooden desk, soft warm light, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## 十品目 おかわりじゃんけん (10点)

**G50** · 「揚げパンがひとつ余った日の、あの緊張感」
```
One last kinako fried bread roll left alone in the center of a large dented aluminum serving tray on a table at the front of a 1970s Japanese classroom, blurred students' silhouettes gathered around the edges of frame, dramatic warm light on the bread, shallow depth of field, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G51** · 「最後のひとつ、じゃんけんな」
```
Two small fists meeting in the air above a wooden school desk playing rock-paper-scissors, seen from the side at desk level, blurred warm classroom background, afternoon light, hands only, no faces, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**G52** · 「風邪で学校を休んだ日」「ナフキンに包まれた」
```
A koppepan bread roll wrapped in a white cloth napkin lying on a small wooden tray beside a futon on tatami flooring, soft afternoon light through paper shoji screen, quiet sickday mood, folded blanket edge visible, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

## TRẢ 脱脂粉乳 (đỉnh 2)

**G53** · 「大きな釜で溶かした、あの匂い」
```
A huge steel pot of pale milk being stirred with a long wooden paddle in a dim 1950s Japanese school kitchen, thick steam rising, cook seen only as a silhouette from behind, single bare light bulb, austere postwar mood, slightly desaturated, 1970s Japan (Showa era), shot on 8mm home movie film, faded Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**PD-B** · 「ララ物資に、ユニセフ」 · PD clip *You in Japan* (1957) — cảnh trẻ em/đời sống hậu chiến, 6–8s, MUTE

**D54** · 「昭和50年。給食費は、ひと月1900円に」 · DRAWN table **anim**: 「給食費のあゆみ」/「昭和42年 700円」「昭和50年 1,900円」「約2.7倍に」/ note 「※東京・府中市の記録より」 · circle dòng 昭和50

## KẾT

**G55** · 「昼休みの校庭へ、みんな駆け出して」
```
A sunlit dirt schoolyard of a 1970s Japanese elementary school seen from a classroom window, students running away from camera toward a steel jungle gym and swings in the distance, long midday shadows, wooden school building edge in frame, no faces visible, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, soft afternoon sunlight, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D56** · 「あなたは、何点でしたか」 · DRAWN card: 「10点満点」/「あなたは何点でしたか？」/「コメントで教えてください」

**G57** · 「お母さんが縫ってくれた給食袋は、もう、どこにもないけれど」
```
A small faded floral drawstring cloth pouch resting alone on a windowsill in deep golden evening light, long soft shadows, dust in the light beam, elegiac quiet mood, shallow depth of field, 1970s Japan (Showa era, around 1970), shot on 8mm home movie film, faded warm Fujicolor palette, gentle film grain, slight vignette, nostalgic documentary photography, muted greens and ochres, natural imperfect framing, 16:9. Avoid: modern objects, smartphones, LED lights, plastic bottles, air conditioner, modern clothing, readable text or signage, brand logos, western faces, anime style, oversaturated colors, HDR look, clean digital sharpness, close-up faces.
```

**D58** · 「昭和くらし図鑑、今日はこのページまで」 · DRAWN end card cố định (chữ ký kênh): 「昭和くらし図鑑」/「今日は、このページまで」「また、次のページで」

---

## Tổng kê

| Loại | Số | Ai làm |
|---|---|---|
| GEN (ảnh AI) | **26** | gen theo block trên (tay hoặc API) → `gen_raw/gen_G◯◯.png` |
| PHOTO (thật) | 10 | có sẵn `_asset_test/` — Claude gắn |
| DRAWN | 12 | `make_drawn.py` — Claude render |
| PD clip | 2 | cắt từ *You in Japan* — Claude làm |
| **Tổng** | **50** | ≈ 3,6 đổi hình/phút (trần 6) ✅ |

Ảnh thật nào đã lên bản render CŨ (video 9′21″ chưa đăng) → video chưa public nên KHÔNG tính là đã dùng; bộ này vẫn hợp lệ. G01 = hình đầu = đúng chủ thể ✅. Không mặt cận, không chữ trong khung AI (chữ để DRAWN lo) ✅.
