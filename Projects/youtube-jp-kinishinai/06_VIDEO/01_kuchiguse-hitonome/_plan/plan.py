# -*- coding: utf-8 -*-
"""Ke hoach hinh — kinishinai bai 1 (v4b, 19,3′). Chia shot BANG TAY theo y cau (hinh khop cau dang doc).

Moi entry: "at" = chi so dong trong _TTS.md (bo dong trong / comment, bo tag) — shot bat dau o dong do,
keo toi shot sau. Loai:
  img  : anh (AI photoreal; "q" = tu khoa Pexels neu stock co the khop -> tim anh that truoc)
  card : the ve bang FONT (make_cards_k.py) — chapter / stat / swap / seven / asch / concept / two / quote
  reveal: chu hien dan tung dong (clip, can _dur tu voice -> dung sau khi co timeline.json)
Motif xuyen bai: 「見張り番」 = MOT CAI DEN LONG GIAY (andon) — shot 5, 19, 52, 73, 87, 100, 109.
Nhan vat: {K} = NGUOI KE (v5 ke ngoi 1 — 68, cuu nhan vien quay 呉服), mo ta co dinh; khong khoa mat (t2i khong co character-lock).
"""

K = "a Japanese woman of about 68 with short soft silver hair in a neat bob, small pearl earrings and a navy cardigan"
KY = "a Japanese woman in her late thirties with neat dark hair in a low bun, wearing a 1990s department-store uniform (navy jacket, white blouse, small scarf)"
D = "her daughter, a Japanese woman in her early forties with shoulder-length dark hair and a beige sweater"
ANDON = "a small traditional Japanese paper floor lantern (andon) with a warm glowing paper shade"

P = [
# ---------------- MO DAU ----------------
{"at": 0,   "k": "img", "d": "an older Japanese woman at a post office counter bowing her head apologetically again and again to the clerk, a small parcel in her hands, bright ordinary daytime"},
{"at": 2,   "k": "img", "d": "an older Japanese woman lying awake in a futon in a dark bedroom at night, eyes open, staring at the ceiling, a faint streetlight through the shoji"},
{"at": 4,   "k": "img", "d": "the same older woman sitting up in her futon at night, one hand pressed to her chest, worried, dim blue light"},
{"at": 6,   "k": "img", "d": KY + " at a department-store kimono counter in the 1990s, bowing deeply again and again to customers, a faded colour photograph look"},
{"at": 7,   "k": "card", "card": {"type": "stat", "lines": ["「見られている」と感じる量は", "実際の 約2倍", "心理学の実験より"]}},
{"at": 8,   "k": "img", "d": ANDON + " standing alone in a dark tatami room at night, its soft light quietly watching over the room, symbolic and calm"},
{"at": 10,   "k": "img", "d": "a faded 1980s colour photograph look: a young Japanese woman in an office uniform bowing politely to older colleagues, and beside it a young wife serving tea to her in-laws at a low table"},
{"at": 11,  "k": "card", "card": {"type": "seven", "open": 0, "lines": ["見張り番がささやく", "七つの口ぐせ"]}},
{"at": 13,  "k": "img", "d": "a mother and her adult daughter sitting at the same low table, a faint pane of frosted glass standing between them, both looking down, quiet distance"},
{"at": 14,  "k": "img", "d": "a Japanese living room on New Year's Day, a kotatsu with a lacquered osechi box, every seat filled with family except one empty cushion, an apron hanging by the kitchen doorway"},
{"at": 15,  "k": "img", "d": "an older Japanese woman folding laundry in a sunny living room, a small radio on the shelf, relaxed everyday afternoon"},
# ---------------- その一 ----------------
{"at": 17,  "k": "card", "card": {"type": "chapter", "lines": ["その一", "「すみません」"]}},
{"at": 19,  "k": "img", "d": "on a city pavement a young man hands a dropped knitted glove back to an older Japanese woman, and she bows deeply, apologising instead of smiling"},
{"at": 21,  "k": "img", "d": KY + " standing behind a kimono counter in a department store, bowing politely, rolls of kimono fabric on the shelves behind her"},
{"at": 22,  "k": "img", "d": "an open wooden drawer full of neatly folded used gift-wrapping paper, stacked by colour, careful hands smoothing one sheet", "q": "folded wrapping paper drawer"},
{"at": 24,  "k": "img", "d": KY + " bowing to a customer before the customer can speak, at the department store counter, gentle 1990s colour"},
{"at": 26,  "k": "img", "d": "a hand writing a letter with a fountain pen on plain cream notepaper at a wooden desk, no words visible, soft window light", "q": "hand writing letter fountain pen"},
{"at": 27,  "k": "img", "d": ANDON + " on the tatami casting a huge dark shadow on the shoji wall behind it, far bigger than the lantern itself, symbolic"},
{"at": 28,  "k": "img", "d": "a kind middle-aged man holding a door open, looking awkward and uneasy while an older Japanese woman keeps bowing and apologising to him"},
{"at": 29,  "k": "card", "card": {"type": "stat", "lines": ["「ありがとう」のひとことで", "約3割 → 約6割", "次も手伝ってくれた人"]}},
{"at": 30,  "k": "card", "card": {"type": "swap", "lines": ["すみません", "ありがとう"]}},
{"at": 32,  "k": "img", "d": "inside a city bus in spring, a high-school boy in a school uniform stands up to give his seat, " + K + " thanks him with a warm smile"},
{"at": 33,  "k": "img", "d": "a round Japanese anpan bun in a small paper bag held in two hands outside a neighbourhood bakery, soft spring light", "q": "anpan bread bakery"},
{"at": 34,  "k": "img", "d": "a busy pedestrian crossing in a Japanese city seen from behind, many anonymous people walking, no faces clear", "q": "tokyo crosswalk crowd"},
# ---------------- その二 ----------------
{"at": 36,  "k": "card", "card": {"type": "chapter", "lines": ["その二", "「どう思われるかしら」"]}},
{"at": 38,  "k": "img", "d": "an older Japanese woman in a new light-coloured coat walking down a shopping street, glancing nervously at passers-by who are all looking at their own phones and bags"},
{"at": 40,  "k": "img", "d": "a pair of new eyeglasses resting on a small table next to a hand mirror, morning light, nobody in the frame", "q": "eyeglasses on table"},
{"at": 42,  "k": "img", "d": "an ordinary American university corridor with students walking between classes, autumn light through tall windows, no signs", "q": "university hallway students"},
{"at": 43,  "k": "img", "d": "a college student in a bright T-shirt printed with a large cartoon face of a smiling man with a big hairstyle, stepping into a room where other students sit at desks and barely look up"},
{"at": 44,  "k": "card", "card": {"type": "stat", "lines": ["「気づかれた」と思った人数の", "ちょうど 半分", "実際に気づいた人"]}},
{"at": 47,  "k": "img", "d": "an older Japanese woman in plain grey clothes walking alone down the same narrow grey street, bright colourful clothes in the shop windows she passes without looking"},
{"at": 49,  "k": "card", "card": {"type": "swap", "lines": ["どう思われるかしら", "みんな、自分のことで忙しい"]}},
{"at": 50,  "k": "img", "d": K.replace("a navy cardigan", "a floral early-summer blouse") + ", walking with light steps along a sunny shopping arcade, nobody paying attention to her"},
{"at": 51,  "k": "img", "d": K + ", putting on her shoes at the front door with a handbag, smiling, ready to go out again, bright morning"},
{"at": 53,  "k": "img", "d": "a Japanese apartment complex courtyard where several older neighbours chat politely by the rubbish collection point, morning"},
# ---------------- その三 ----------------
{"at": 55,  "k": "card", "card": {"type": "chapter", "lines": ["その三", "「みんな、そうしてるから」"]}},
{"at": 57,  "k": "img", "d": "a neighbourhood association meeting in a community hall, older residents on folding chairs raising their hands together, one older woman raising hers last and slowly, uncertain"},
{"at": 59,  "k": "img", "d": "a faded 1970s colour photograph look: young housewives in aprons chatting together in a danchi courtyard, laundry drying on the balconies"},
{"at": 60,  "k": "card", "card": {"type": "asch", "lines": ["線の長さを比べる実験", "（アッシュ, 1950年代）"]}},
{"at": 62,  "k": "card", "card": {"type": "people", "n": 4, "hit": 3, "lines": ["周りに合わせて、まちがえた人", "4人に3人"]}},
{"at": 64,  "k": "img", "d": "in a meeting room one person quietly raises a hand for the other option while the rest of the group turns to look, and two others begin to lift their hands too"},
{"at": 66,  "k": "img", "d": "a community hall meeting seen from the side, several older residents sitting with arms folded and eyes lowered, clearly disagreeing in silence"},
{"at": 68,  "k": "img", "d": "an older Japanese woman at a neighbourhood gathering smiling and nodding along to everyone, her smile a little stiff, the others not really looking at her"},
{"at": 69,  "k": "card", "card": {"type": "swap", "lines": ["みんなそうしてるから", "私は、こうしたい"]}},
{"at": 71,  "k": "img", "d": "a summer-festival planning meeting in a community hall with paper lanterns stacked in the corner, " + K + " keeps her hands in her lap while others raise theirs"},
{"at": 72,  "k": "img", "d": "at the door of the community hall a neighbour leans in to whisper to " + K + ", both women smiling like conspirators, summer evening"},
{"at": 74,  "k": "img", "d": "two old friends in their late sixties sitting across a small table in a retro coffee shop, cups of coffee, laughing"},
# ---------------- その四 ----------------
{"at": 76,  "k": "card", "card": {"type": "chapter", "lines": ["その四", "「つまらない話で、ごめんなさいね」"]}},
{"at": 78,  "k": "img", "d": "an older Japanese woman walking home alone at dusk along a quiet residential street, lost in thought, replaying the conversation"},
{"at": 80,  "k": "img", "d": ANDON + " glowing on a low desk beside an open blank notebook and a red pencil, as if something is marking every page, night"},
{"at": 81,  "k": "img", "d": "two strangers, a man and a woman in their thirties, chatting on a park bench for the first time, friendly and a little shy"},
{"at": 82,  "k": "reveal", "lines": ["相手の好意を、", "実際より、低く見積もる。"]},
{"at": 83,  "k": "img", "d": "an older Japanese woman on her own way home after tea, smiling happily to herself on the train"},
{"at": 84,  "k": "img", "d": "an older Japanese woman at home holding the phone and politely declining an invitation, then looking down at the empty room, a little lonely"},
{"at": 85,  "k": "card", "card": {"type": "swap", "lines": ["つまらない話で、ごめんなさいね", "楽しかった、ありがとう"]}},
{"at": 86,  "k": "img", "d": K + ", talking on a home telephone by the window and laughing, red and yellow autumn leaves outside"},
{"at": 87,  "k": "img", "d": "two older Japanese women friends walking side by side on an autumn path, chatting happily about next time"},
{"at": 89,  "k": "img", "d": "an older Japanese woman standing alone at a window at dusk, one hand on her chest, holding something she has not said"},
# ---------------- その五 ----------------
{"at": 91,  "k": "card", "card": {"type": "chapter", "lines": ["その五", "「こんなこと言ったら、恥ずかしい」"]}},
{"at": 93,  "k": "img", "d": "an older Japanese woman forcing a bright smile at a friend across the table, waving a hand as if to say she is fine, her eyes a little sad"},
{"at": 95,  "k": "img", "d": "close-up of an older woman's hands clasped tightly together on her lap, knuckles pale, holding everything in"},
{"at": 96,  "k": "img", "d": "on a bench two older Japanese women sit close, one quietly confiding something, the other listening with a warm, open face"},
{"at": 98,  "k": "img", "d": "the listening friend's warm face, gently smiling, eyes kind, soft afternoon light"},
{"at": 99,  "k": "reveal", "lines": ["恥ずかしい打ち明け話は、", "相手には、あたたかく映る。"]},
{"at": 100,  "k": "card", "card": {"type": "stat", "lines": ["94の研究をまとめると", "打ち明ける人ほど 好かれやすい", "Collins & Miller, 1994"]}},
{"at": 101, "k": "img", "d": "several older Japanese women at a polite tea gathering, all smiling and nodding, yet each one's eyes turned slightly away, a surface-only conversation"},
{"at": 102, "k": "card", "card": {"type": "swap", "lines": ["こんなこと言ったら", "ちょっと、聞いてくれる？"]}},
{"at": 104, "k": "img", "d": K + ", sitting under a soft lamp on an October night, holding a phone to her ear, speaking quietly and honestly"},
{"at": 105, "k": "img", "d": "a Japanese woman in her mid sixties on the phone in her own kitchen, wiping away tears while smiling"},
{"at": 106, "k": "card", "card": {"type": "seven", "open": 5, "lines": ["ここまでで、", "いくつ当てはまりましたか"]}},
{"at": 108, "k": "img", "d": ANDON + " turned toward a dressing-table mirror, its light falling on an older woman looking at her own reflection"},
# ---------------- その六 ----------------
{"at": 109, "k": "card", "card": {"type": "chapter", "lines": ["その六", "「いい年して」"]}},
{"at": 111, "k": "img", "d": "an older Japanese woman holding a blank hula-dance class flyer in front of a community centre, then shaking her head at her own reflection in the glass door"},
{"at": 113, "k": "img", "d": "a faded 1960s colour photograph look: a teenage girl sitting in formal seiza on tatami while strict elders look on, a sense of rules"},
{"at": 114, "k": "img", "d": "an older Japanese couple walking slowly through an autumn park, choosing their own path, calm and content", "q": "elderly couple autumn park japan"},
{"at": 115, "k": "reveal", "lines": ["年を重ねるほど、", "人の目より、自分の心を選ぶ。"]},
{"at": 116, "k": "img", "d": "a row of closed boxes with their lids on, lined up on a shelf in a dim room, one small box slightly open with light inside"},
{"at": 118, "k": "card", "card": {"type": "swap", "lines": ["いい年して", "この年だから"]}},
{"at": 120, "k": "img", "d": K.replace("a navy cardigan", "a warm winter coat and scarf") + ", standing on a railway platform in December with a small suitcase, excited"},
{"at": 121, "k": "img", "d": "two ekiben lunch boxes open on a train window table, a snowy landscape passing outside", "q": "ekiben train window"},
{"at": 123, "k": "img", "d": "a kitchen apron hanging on a hook beside a dim kitchen doorway, quiet and a little heavy"},
# ---------------- その七 ----------------
{"at": 124, "k": "card", "card": {"type": "chapter", "lines": ["その七", "「私さえ、我慢すれば」"]}},
{"at": 126, "k": "img", "d": "an older Japanese woman standing alone in a kitchen holding a teacup, while laughter and warm light come from the living room beyond"},
{"at": 128, "k": "img", "d": "a family dinner with tension, a father and adult son arguing, and the mother bowing her head to calm them down"},
{"at": 130, "k": "img", "d": ANDON + " between two people seated at a low table, its shadow forming a soft dark wall on the shoji between them"},
{"at": 132, "k": "img", "d": "a plain psychology study room with two chairs facing each other across a small table, a notepad, nobody sitting yet", "q": "empty meeting room two chairs"},
{"at": 133, "k": "img", "d": "a woman keeping a carefully blank face while talking, and the person opposite her leaning back, uneasy, the conversation not flowing"},
{"at": 134, "k": "img", "d": D + " at the kotatsu glancing uneasily toward her mother standing in the kitchen, unable to relax"},
{"at": 136, "k": "card", "card": {"type": "concept", "lines": ["課題の分離", "アドラー心理学"]}},
{"at": 138, "k": "card", "card": {"type": "two", "lines": ["相手が、あなたを", "どう思うか", "相手の課題", "あなたが、", "どう生きるか", "あなたの課題"]}},
{"at": 141, "k": "img", "d": "an older Japanese woman on the phone at home, politely saying no, her shoulders dropping with relief"},
{"at": 143, "k": "img", "d": "two older Japanese women at a kitchen table laughing freely, shoulders relaxed, cups of tea"},
# ---------------- お正月 ----------------
{"at": 144, "k": "img", "d": "the front of a Japanese house on New Year's Day with a shimekazari on the door, a family with children arriving, bright winter sun"},
{"at": 146, "k": "img", "d": "a family seated around a kotatsu with a lacquered osechi box, and in the background " + K + " in an apron standing at the kitchen counter"},
{"at": 148, "k": "img", "d": "close-up of an older woman's hands ladling ozoni soup into lacquer bowls, steam rising, a voice calling from the next room"},
{"at": 150, "k": "img", "d": "a row of old family photographs of New Year gatherings across the decades on a shelf, in every one the mother is standing at the edge, never sitting"},
{"at": 151, "k": "img", "d": K + " in an apron turning toward the sink, and stopping halfway, one foot not yet moved"},
{"at": 152, "k": "img", "d": ANDON + " glowing softly behind " + K + " in the kitchen, her figure still, listening"},
{"at": 153, "k": "reveal", "lines": ["ありがとう。", "でも、今日は、休んでいいわ。"]},
{"at": 155, "k": "img", "d": K + " untying her apron and slipping her legs under the kotatsu beside her family"},
{"at": 157, "k": "img", "d": "a small Japanese grandchild at the kotatsu staring up with wide round eyes and an open mouth, surprised"},
{"at": 159, "k": "img", "d": "a whole family bursting into laughter around a kotatsu on New Year's Day, the grandmother laughing hardest"},
{"at": 161, "k": "card", "card": {"type": "quote", "lines": ["お母さんが台所に立ってるとね、", "私たち、座ってていいのか、", "ずっと、気をつかってたのよ。"]}},
{"at": 162, "k": "img", "d": K + " sitting at the kotatsu looking around at her family in quiet realisation, the empty kitchen visible behind her"},
{"at": 164, "k": "reveal", "lines": ["四十回のお正月、", "ずっと、立っていたんですね、私。", "……座っても、よかったんです。"]},
{"at": 165, "k": "img", "d": "mikan peels and an open old photo album on a kotatsu, two women's hands turning a page, warm evening lamp", "q": "mandarin orange kotatsu"},
# ---------------- KET ----------------
{"at": 166, "k": "img", "d": ANDON + " at dawn with its light turned low, pale morning coming through the shoji, peaceful"},
{"at": 169, "k": "reveal", "lines": ["ありがとう。", "もう、休んでいいよ。"]},
{"at": 170, "k": "img", "d": "a whole Japanese family around a kotatsu, the grandmother sitting in the middle this time, everyone relaxed and close"},
{"at": 172, "k": "card", "card": {"type": "seven", "open": 7, "lines": ["七つのうち、", "いくつ当てはまりましたか"]}},
{"at": 174, "k": "img", "d": "a cup of green tea by a sunny window, a gentle breeze moving the curtain", "q": "green tea cup window sunlight"},
{"at": 176, "k": "img", "d": "an older Japanese woman walking lightly along a sunny morning path, shoulders relaxed, seen from behind"},
]

SEVEN = ["すみません", "どう思われるかしら", "みんな、そうしてるから", "つまらない話で、ごめんなさいね",
         "こんなこと言ったら、恥ずかしい", "いい年して", "私さえ、我慢すれば"]
