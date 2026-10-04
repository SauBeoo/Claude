# -*- coding: utf-8 -*-
"""Dựng SLIDES + prompt ảnh AI cho video 14 かぼちゃ. Tự verify mọi `match`."""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(r"E:\Claude\Projects\youtube-jp-shokutaku")
SC = PROJ / "04_SCRIPTS"
TTS = SC / "14_kabocha-tabekata_TTS.md"
STEM = "14_kabocha-tabekata"

STYLE = ("photorealistic documentary photography, Japanese home kitchen, warm natural window light "
         "from the left, soft shadows, muted earthy palette with deep navy and warm amber accents, "
         "shallow depth of field, calm gentle mood, 16:9. "
         "No text, no letters, no numbers, no watermark, no logo, no signature. --ar 16:9")
SUMIKO = ("a Japanese woman in her mid-seventies, silver hair in a low bun, gentle round face, "
          "muted indigo blouse and beige linen apron")
HANDS = "the wrinkled hands of an elderly Japanese woman"

# (match, prompt_core, rank)
E = [
 # ── COLD OPEN ──────────────────────────────────────────────────────────────
 ("かぼちゃの煮物に、砂糖を大さじ二杯",
  "extreme close-up, a wooden tablespoon heaped with white granulated sugar being tipped into a "
  "simmering pot of orange pumpkin chunks, steam rising, dark enamel pot", ""),
 ("健康診断のたびに",
  "a health checkup result sheet lying on a kitchen table beside folded reading glasses, the print "
  "completely blurred and unreadable, morning light", ""),
 ("野菜は食べているのに",
  "a Japanese home dinner table seen from above, generously covered with vegetable side dishes, "
  "simmered vegetables, a salad, pickles and greens, everything looking virtuous and healthy", ""),
 ("今、台所にかぼちゃがある方は、切り口を見てください",
  "extreme close-up of a kabocha squash cut in half on a wooden board, the cut face a deep vivid "
  "orange, seeds and fibrous centre clearly visible", ""),
 ("そのかぼちゃは、もう、砂糖をほとんど必要としていません",
  "a small ceramic sugar jar with its wooden lid closed, pushed to the far edge of a kitchen counter, "
  "out of focus kitchen behind", ""),
 ("かぼちゃは、置いておくあいだに、でんぷんが甘みに変わっていきます",
  "three whole kabocha squashes resting in a wooden crate in a dim cool storeroom, dust motes in a "
  "single shaft of light", ""),
 ("量ではなく、濃さで食べる",
  "one single small piece of deeply orange simmered kabocha on a small dark ceramic dish, lit by one "
  "soft beam, everything else in shadow", ""),
 ("買い方に、コツが一つあるだけです",
  "a Japanese supermarket vegetable shelf with whole and quarter-cut kabocha squashes wrapped in film, "
  "even fluorescent light, slightly wide shot", ""),
 # ── 第5位 わた ─────────────────────────────────────────────────────────────
 ("第五位は、わたを、捨てないことです",
  "overhead view of a kabocha squash cut cleanly in half on a wooden board, the seeds and the stringy "
  "fibrous centre still intact and glistening", "第5位"),
 ("多くの方が、あそこを、いちばん先に捨てます",
  f"{HANDS} scraping the seeds and stringy centre out of a halved kabocha with a metal spoon, the "
  "scrapings falling into a small waste bowl", "第5位"),
 ("けれども、あの黄色は、ベータカロテンという色の成分です",
  "macro shot of the fibrous orange centre of a kabocha squash, threads and pulp, intensely saturated "
  "orange, water droplets", "第5位"),
 ("次に切る時、捨てる前に、わたと実を、並べて見比べてみてください",
  "a white plate with two portions side by side, on the left the stringy kabocha centre in vivid deep "
  "orange, on the right a slice of the paler flesh, flat overhead comparison", "第5位"),
 ("種だけを、指でつまんで外してください",
  "close-up of the fingers of an elderly Japanese woman plucking the pale seeds one by one out of the "
  "fibrous centre of a halved kabocha, leaving the orange stringy part untouched", "第5位"),
 ("洗って、水気をよく拭いて、フライパンで、から炒りする",
  "pumpkin seeds toasting in a dry cast-iron frying pan on a gas stove, a few seeds mid-air from a "
  "gentle toss, warm browning edges", "第5位"),
 ("わたのほうは、そのまま、実と一緒に切って、煮てください",
  "a pot of kabocha chunks simmering in clear dashi broth, the pieces still holding their shape, "
  "gentle steam", "第5位"),
 ("捨てるところを減らすだけで、同じ一切れが、濃くなる",
  "a single thick piece of simmered kabocha on chopsticks lifted above a bowl, deep orange interior "
  "visible at the broken edge", "第5位"),
 # ── PERSONA ────────────────────────────────────────────────────────────────
 ("ここで少しだけ、ご挨拶をさせてください",
  "a quiet Japanese kitchen in the morning, a kettle steaming softly on the stove, a folded cloth and "
  "a single teacup on the counter, nobody present", ""),
 ("台所に立ちながら、公表されている資料を、少しずつ読み集めているだけです",
  "an open notebook and two thick reference booklets stacked on a kitchen table beside a teacup, all "
  "printed pages blurred and unreadable, warm lamp light", ""),
 # ── 第4位 皮 ───────────────────────────────────────────────────────────────
 ("第四位は、皮を、むかないことです",
  f"{HANDS} peeling thick dark green skin off a kabocha squash with a kitchen knife, curls of removed "
  "skin piling on the board", "第4位"),
 ("けれども、かぼちゃの皮は、実よりも硬いぶん、中身が詰まっています",
  "extreme macro of the dark green ridged skin of a kabocha squash, texture and faint pale mottling, "
  "raking side light", "第4位"),
 ("つまり、皮をむくというのは、いちばん甘い部分だけを、裸で食べるということです",
  "a plate holding pieces of kabocha with all skin removed, pale and bare, next to a small heap of the "
  "discarded green peel", "第4位"),
 ("一つは、皮を全部むくのではなく、ところどころだけ、ピーラーで薄く筋を入れる",
  f"{HANDS} drawing a vegetable peeler down a kabocha in stripes, leaving alternating bands of dark "
  "green skin and exposed orange flesh", "第4位"),
 ("もう一つは、煮る前に、電子レンジで二分ほど温めてから、鍋に入れることです",
  "kabocha chunks arranged in a shallow heatproof glass dish loosely covered with cling film, sitting "
  "inside a small home microwave, warm interior light", "第4位"),
 ("皮が残っていると、噛む回数も、自然に増えます",
  "chopsticks lifting a piece of simmered kabocha with the dark green skin still attached, glossy "
  "broth dripping, bowl below", "第4位"),
 # ── スミ子 nhịp 1 ──────────────────────────────────────────────────────────
 ("片桐スミ子さん、七十六歳",
  f"portrait of {SUMIKO}, standing in her own small kitchen, hands resting on the counter, looking "
  "slightly away from camera, quiet dignified expression", ""),
 ("お店をたたんだ今でも、指ぬきだけは、針箱に入れていらっしゃるそうです",
  "close-up of an old wooden sewing box opened on a tatami floor, a worn metal thimble, spools of "
  "thread and needles inside, soft afternoon light", ""),
 ("スミ子さんの家では、かぼちゃの煮物は、三日に一度、必ず出ていました",
  "a small dining table set for one person, a bowl of simmered kabocha, rice and miso soup, one pair "
  "of chopsticks, quiet empty room", ""),
 ("砂糖は、大さじ二杯",
  f"{HANDS} levelling two heaped tablespoons of white sugar over a simmering pot, the sugar catching "
  "the light as it falls", ""),
 ("ご主人が亡くなって、三年",
  "a framed photograph of an elderly man on a wooden shelf, softly out of focus, a small cup of tea "
  "and a single flower placed in front of it", ""),
 ("去年の健康診断で、血糖の数字に、初めて印がつきました",
  "a health checkup form on a table with one row circled in red pen, all printed characters blurred "
  "and unreadable, a pen resting beside it", ""),
 ("先生に、心当たりはありますかと聞かれて、何も浮かばなかったそうです",
  f"{SUMIKO}, sitting alone on a chair in a quiet clinic waiting area, handbag on her lap, looking "
  "down at her hands, soft neutral light", ""),
 # ── 第3位 油 ───────────────────────────────────────────────────────────────
 ("第三位は、油と、一緒に食べることです",
  "a thin stream of golden sesame oil being drizzled from a small bottle over a plate of steamed "
  "kabocha, droplets glistening on the orange surface", "第3位"),
 ("水には、溶けません",
  "macro split composition, on one side clear water beads sitting on an orange kabocha surface without "
  "spreading, on the other side golden oil spreading into a smooth sheen", "第3位"),
 ("蒸したものなら、マヨネーズを少しだけ",
  "a small dab of mayonnaise beside a mound of steamed kabocha on a plain white plate, simple and "
  "homely, overhead", "第3位"),
 ("私も、蒸したかぼちゃに、すりごまをかけるようになりました",
  "ground toasted sesame being sprinkled from a small bowl over warm steamed kabocha, fine powder "
  "caught in the light, steam rising", "第3位"),
 ("油は、かぼちゃの敵ではなく、運び役です",
  "a small glass oil cruet standing beside a plate of orange kabocha on a dark wooden table, warm "
  "backlight through the oil", "第3位"),
 # ── CƠ CHẾ + 原典 ──────────────────────────────────────────────────────────
 ("ベータカロテンは、体の中で、必要な分だけビタミンAに変わるとされています",
  "extreme macro of the flesh of a kabocha squash backlit so the deep orange glows, fibrous structure "
  "visible, almost abstract", ""),
 ("そのビタミンAは、目の粘膜や、鼻や喉の粘膜を、しっとり保つ材料になります",
  "soft close-up of the eye area of an elderly Asian person behind reading glasses, gentle window "
  "light, calm expression, shallow focus", ""),
 ("かぼちゃには、もう一つ、ビタミンEも多く入っています",
  "a small wooden bowl of toasted pumpkin seeds beside a wedge of kabocha on a linen cloth, warm "
  "overhead light", ""),
 ("この成分の量は、文部科学省が公表している、日本食品標準成分表という資料に、野菜ごとに載っています",
  "a thick official reference volume lying open on a wooden table under a desk lamp, a magnifying "
  "glass resting on the page, all print blurred and unreadable, authoritative quiet mood", ""),
 # ── CTA GIỮA ───────────────────────────────────────────────────────────────
 ("ここまで聞いてくださって、ありがとうございます",
  "two teacups of green tea steaming side by side on a kitchen table by a bright window, warm "
  "welcoming atmosphere", ""),
 ("そして、気づいたことやご感想があれば、どうぞコメントで教えてくださいね",
  "an elderly person's hand resting beside a smartphone on a kitchen table next to a teacup, screen "
  "dark and blank, soft light", ""),
 # ── 第2位 砂糖 ─────────────────────────────────────────────────────────────
 ("第二位は、砂糖とみりんを、引くことです",
  "a ceramic sugar jar and a bottle of mirin standing side by side on a kitchen shelf, both catching "
  "warm light, simmering pot blurred behind", "第2位"),
 ("かぼちゃは、野菜の顔をしていますが、成分表で見ると、いも類に近い食べ物です",
  "a kabocha squash placed on a wooden board between potatoes and sweet potatoes, all raw and whole, "
  "flat overhead arrangement", "第2位"),
 ("大きめに三切れ、およそ百五十グラムで、ご飯茶碗の、半分ほどの糖質が入ってきます",
  "a direct side-by-side comparison on a dark table, on the left three thick chunks of simmered "
  "kabocha on a small plate, on the right a rice bowl filled exactly halfway with white rice, "
  "even light, clean composition", "第2位"),
 ("そこへ、砂糖を大さじ二杯",
  "two heaped tablespoons of white sugar poured out into two neat mounds on a dark slate surface, "
  "hard side light making the crystals sparkle", "第2位"),
 ("甘いものは食べていない、とおっしゃる方の食卓に、それは、たしかに載っていません",
  "a modest Japanese dinner table with only savoury dishes, grilled fish, pickles, rice and miso soup, "
  "no sweets or cake anywhere, warm evening light", "第2位"),
 ("熟したかぼちゃは、もともと甘いのです",
  "a fully ripened kabocha cut open to reveal an intensely deep orange, almost amber cut face, sitting "
  "on a wooden board in warm light", "第2位"),
 ("まず、砂糖を、大さじ二杯から、一杯に減らしてください",
  "one single level tablespoon of white sugar held over a pot, with a second empty spoon lying beside "
  "it on the counter", "第2位"),
 ("そして、だしを、少し濃いめにとってください",
  "dried kombu seaweed and katsuobushi flakes beside a pot of golden dashi being strained through a "
  "fine mesh, steam rising", "第2位"),
 ("それでも足りないと感じた日は、砂糖ではなく、かぼちゃを疑ってください",
  f"{HANDS}, hesitating over an open sugar jar, fingers just above the spoon, not yet taking any, "
  "thoughtful pause", "第2位"),
 # ── スミ子 nhịp 2 ──────────────────────────────────────────────────────────
 ("娘さんが、台所で、砂糖の袋を見つけたそうです",
  "a large half-empty paper bag of sugar standing in a kitchen cupboard among other dry goods, "
  "discovered under a torch of daylight from an opened door", ""),
 ("スミ子さんは、しばらく黙っていらっしゃったそうです",
  f"{SUMIKO}, sitting silently at her kitchen table, hands folded together on the tabletop, gaze "
  "lowered, soft grey daylight", ""),
 ("お父さんの好きな味を、やめたくなかったのよ",
  "close-up of the folded wrinkled hands of an elderly Japanese woman resting on a worn wooden table, "
  "a wedding ring on one finger, everything else dark", ""),
 # ── 第1位 選び方 ───────────────────────────────────────────────────────────
 ("第一位は、切り口の色と、へたで、選ぶことです",
  "a Japanese supermarket produce display of kabocha squashes, some whole, some cut into quarters and "
  "wrapped in clear film, viewed from a shopper's height", "第1位"),
 ("切ってあるものなら、切り口を見てください",
  "two quarter-cut kabocha pieces lying side by side under supermarket light, the left one a deep "
  "vivid orange, the right one a pale lemon yellow, clear direct comparison", "第1位"),
 ("薄い、レモンのような黄色",
  "a pale yellow quarter-cut kabocha in the foreground with a heaped tablespoon of sugar standing "
  "behind it, slightly ominous side light", "第1位"),
 ("丸ごとのものなら、へたを見てください",
  "extreme close-up of the stem of a whole kabocha squash, dried, corky and cracked, the skin around "
  "it slightly sunken", "第1位"),
 ("青くて、みずみずしいへたは、まだ早い、という合図です",
  "extreme close-up of a whole kabocha with a fresh green moist stem, still plump and unshrunken, "
  "cool light", "第1位"),
 ("風通しのいいところに置いておけば、ひと月ほど持ちます",
  "a whole kabocha squash resting on a wooden shelf near a slightly open window with a breeze-moved "
  "curtain, quiet domestic corner", "第1位"),
 ("今、お店に多いのは、西洋かぼちゃという、ほくほくした種類です",
  "two different whole squashes side by side on a wooden table, one dark green with a smooth rounded "
  "shape, the other paler and deeply ridged and flattened", "第1位"),
 ("同じ売り場で、同じ値段で、五倍",
  "a stark side-by-side macro of two kabocha cut faces filling the frame, the left glowing deep "
  "saturated orange, the right washed-out pale yellow, dramatic even light", "第1位"),
 ("濃い黄色を、選ぶ",
  f"{HANDS} reaching out and picking up the deeply orange quarter-cut kabocha from a supermarket "
  "shelf, the pale one left behind in soft focus", "第1位"),
 # ── スミ子 nhịp 3 ──────────────────────────────────────────────────────────
 ("娘さんが、次の週、山形のお店で、いちばん切り口の濃いものを選んで、持ってきたそうです",
  "a younger woman's hands passing a deeply orange quarter-cut kabocha to the wrinkled hands of an "
  "elderly woman across a kitchen counter", ""),
 ("スミ子さんは、いつもの鍋で、いつもの手順で",
  "an old well-used enamel pot on a gas stove with kabocha simmering inside, the pot visibly worn at "
  "the rim from decades of use", ""),
 ("それから、これ、お父さんの味だわ、と",
  f"{SUMIKO}, tasting a piece of simmered kabocha from a small dish, eyes closed, a faint moved smile, "
  "warm kitchen light, deeply emotional quiet moment", ""),
 # ── RECAP + KẾT ────────────────────────────────────────────────────────────
 ("今日のお話を、まとめます",
  "a neat overhead flat lay on a linen cloth of the five elements of the video, the stringy kabocha "
  "centre, a strip of green skin, a small oil cruet, a tablespoon of sugar, and a quarter-cut kabocha, "
  "arranged in a row", ""),
 ("たくさん食べるほど体にいい、という食べ物は、案外、多くありません",
  "one modest bowl of simmered kabocha placed alone on a large empty wooden table, restrained "
  "composition, single soft light", ""),
 ("明日、一つだけ選ぶとしたら、売り場での五秒にしてください",
  "a shopper's point of view looking down at two kabocha pieces on a supermarket shelf, hand hovering "
  "in the moment of deciding", ""),
 ("ところで、皆さんのお宅では、かぼちゃの煮物に、砂糖は何杯入れていらっしゃいますか",
  "a tablespoon standing upright in a jar of white sugar on a kitchen counter, warm domestic light, "
  "inviting quiet question mood", ""),
 ("体にいいと信じているものほど、疑う機会が、ありません",
  "a wholesome looking Japanese home dinner table seen from above, everything appearing healthy and "
  "correct, one dish of glossy simmered kabocha slightly closer to camera", ""),
 ("誰かに直してもらう前に、自分で直せる",
  f"{HANDS}, confidently working at her own kitchen counter, chopping board and knife, morning light, "
  "a sense of capability and independence", ""),
 ("持病のある方や、お薬を飲んでいる方は、食事を変える前に、必ず、かかりつけの先生にご相談ください",
  "a quiet empty clinic consultation corner, two chairs facing each other beside a small desk, soft "
  "daylight through blinds, no people", ""),
 ("今夜の食卓が、皆さんの明日の元気に、つながりますように",
  "a warm evening dinner table under a low hanging lamp, a bowl of simmered kabocha at the centre, "
  "rice and soup beside it, peaceful golden light", ""),
]

lines = [re.sub(r"\[[^\]]*\]", "", l).strip() for l in TTS.read_text(encoding="utf-8").split("\n")]
lines = [l for l in lines if l and not l.startswith("#")]
blob = lines

bad = [m for m, _, _ in E if not any(m in l for l in blob)]
if bad:
    print("🔴 MATCH KHÔNG TỒN TẠI TRONG TTS:")
    for m in bad:
        print("   ", m)
    sys.exit(1)

# thứ tự entry phải theo thứ tự xuất hiện trong TTS
pos = []
for m, _, _ in E:
    pos.append(next(i for i, l in enumerate(blob) if m in l))
if pos != sorted(pos):
    print("🔴 THỨ TỰ ENTRY LỆCH so với TTS:")
    for i in range(1, len(pos)):
        if pos[i] < pos[i - 1]:
            print(f"   entry {i} ({E[i][0][:24]}) đứng trước entry {i-1}")
    sys.exit(1)

# giây ước + kiểm ≥6s và ≤6 đổi hình/phút
sec, acc = [], 0.0
secmap = {}
for i, l in enumerate(blob):
    secmap[i] = acc
    acc += len(l) / 4.60
total = acc
starts = [secmap[p] for p in pos]
gaps = [starts[i + 1] - starts[i] for i in range(len(starts) - 1)] + [total - starts[-1]]
short = [(i, g) for i, g in enumerate(gaps) if g < 6]
print(f"entry: {len(E)} · video {int(total)//60}'{int(total)%60:02d} · "
      f"trung bình {total/len(E):.1f}s/ảnh · {len(E)/(total/60):.2f} đổi hình/phút")
print("entry <6 giây:", short or "(không có)")

slides = []
for (m, core, rank) in E:
    d = {"match": m, "photo": True, "q": "AI-GEN"}
    if rank:
        d["rank"] = rank
    slides.append(d)
(SC / f"{STEM}_SLIDES_photo.json").write_text(
    json.dumps(slides, ensure_ascii=False, indent=1), encoding="utf-8")

flow, tenfile, blocks = [], [], []
blocks.append("# PROMPT ẢNH AI — video 14 かぼちゃ (75 slide)\n")
blocks.append(f"**Khối STYLE dán cuối MỌI prompt (giữ nguyên từng chữ để 75 ảnh đồng nhất):**\n\n```\n{STYLE}\n```\n")
blocks.append(f"**Nhân vật スミ子 (giữ nguyên từng chữ ở 4 slot có bà):**\n\n```\n{SUMIKO}\n```\n")
blocks.append("| # | file | rank | cue (giây) | mô tả |\n|---|---|---|---|---|")
for i, ((m, core, rank), st) in enumerate(zip(E, starts)):
    full = f"{core}. {STYLE}"
    flow.append(full)
    tenfile.append(f"slide_{i:02d}.jpg\t{int(st)//60}'{int(st)%60:02d}\t{rank or '-'}\t{m[:26]}")
    blocks.append(f"| {i:02d} | `slide_{i:02d}.jpg` | {rank or '—'} | {int(st)//60}'{int(st)%60:02d} | {core} |")

V = PROJ / "06_VIDEO" / STEM
V.mkdir(parents=True, exist_ok=True)
(V / "slide_prompts_FLOW.txt").write_text("\n".join(flow), encoding="utf-8")
(V / "slide_prompts_TENFILE.txt").write_text("\n".join(tenfile), encoding="utf-8")
(V / "slide_prompts_BLOCKS.md").write_text("\n".join(blocks), encoding="utf-8")
print("✅ ghi:", SC / f"{STEM}_SLIDES_photo.json")
print("✅ ghi:", V / "slide_prompts_FLOW.txt", "·", len(flow), "prompt")
print("   dài nhất:", max(len(x) for x in flow), "ký · ngắn nhất:", min(len(x) for x in flow))
