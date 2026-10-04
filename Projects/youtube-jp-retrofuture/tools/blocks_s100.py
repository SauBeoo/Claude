# -*- coding: utf-8 -*-
"""
KHỐI PROMPT DÙNG CHUNG — kênh youtube-jp-retrofuture, thế giới 昭和100年.

Vì sao tách khỏi `gen_prompts_ep01.py`: mỗi lần đổi THẾ GIỚI là phải sửa cả tool sinh
40 cảnh lẫn tool sinh 3 cảnh thử. Hai bản khối = hai luật, và đó đúng là cách bài học
`_sig` của workspace đã dính. Một luật, một chỗ.

⭐ THẾ GIỚI v2 (2026-09-22) — viết lại theo video mẫu A (PUotm8YDbKM):
   TIỀN CẢNH: phố Showa Nhật CHẬT KÍN ở mặt đất — hẻm, 商店街 có mái, tiệm nhỏ, noren,
              chậu cây, xe đạp, dây điện, hòm thư đỏ, dây leo phủ tường.
   HẬU CẢNH: SIÊU ĐÔ THỊ CHỒNG TẦNG — hàng lớp nhà và cầu cạn xếp lên tận trời,
              tàu chạy ngang, mây tích trắng khổng lồ phía trên.
   ⛔ v1 (cột đá / biển mây / cầu treo / nhà trên cây) ĐÃ BỎ — không có trong mẫu.
"""

# -----------------------------------------------------------------------------
# (0) HEAD -- KHOI MO DAU, PHAI LA CAU DAU TIEN CUA MOI PROMPT
#
# Do duoc 2026-09-22: THE GIOI (TOWN/MEGACITY) nam o 58-69% do dai prompt, tuc dung
# cho ma `ai-video-regen.md` SS2 da do la model BO QUA. Do la ly do ban gen truoc
# "khong giong mau mot ti nao" -- khong phai vi chu ta sai, ma vi no nam qua sau.
#
# Prompt 12.000 ky thi KHONG the nhet moi thu vao 15% dau. Kien truc chon:
#   TUYEN BO SOM (khoi nay, ~1.300 ky, 4 thu cot tu) -> CHI TIET SAU (cac khoi cu).
# Cung co che "guard phan cap" da ghi o memory feedback_prompt_khoi_chung_huy_mo_ta.
# -----------------------------------------------------------------------------
HEAD = ("Live-action photography, a real photograph of a real place, NOT anime and NOT an illustration. "
"THE PLACE, and this matters more than anything else in this description: a small ordinary Japanese town "
"at street level, crowded with lived-in things — narrow streets, little family shops, noren, potted "
"plants, bicycles, overhead wires — AND BEHIND IT a COLOSSAL CITY STACKED IN LAYERS going up into the "
"sky further than you can see. Both must be in the picture: the little street near, the immense layered "
"city far. And the ordinary things in this street are NOT QUITE OURS — they are mechanical, brass and "
"glass and steam, one step further down their own path. THIS IS A MOVING PICTURE, NOT A PHOTOGRAPH: "
"something in the frame is moving in every single second of it. No distorted, melted or asymmetric faces "
"anywhere: any face that cannot be rendered cleanly must be turned away from the camera or left soft "
"and out of focus.")

# ─────────────────────────────────────────────────────────────────────────────
# ① CHỐNG ANIME / CHỐNG CG — giữ nguyên từ v1, đã đo là có tác dụng
# ─────────────────────────────────────────────────────────────────────────────
REAL = ("Live-action photography, shot on a real camera: real human skin with pores and stray hairs, real "
"woven cloth, real timber with grain and splits, real concrete and real peeling-free painted steel, real "
"dust in the air. This is a photograph of a real place, NOT an illustration, NOT anime, NOT a cartoon, NOT "
"a painting, NOT concept art, NOT a 3D render, NOT CGI, NOT a video game; no outlines around objects, no "
"flat blocks of colour, no cel shading, no stylised faces, no oversized eyes, no painterly brush strokes, "
"no glowing magical particles.")

PEOPLE = ("THE PEOPLE ARE REAL PHOTOGRAPHED HUMAN BEINGS, not characters: real skin with visible "
"pores and uneven tone, stray flyaway hairs, ordinary imperfect faces of ordinary ages, real cloth that "
"creases under its own weight. No smooth plastic skin, no enlarged eyes, no perfectly symmetrical "
"faces, no doll-like proportions. If the sky above them looks like a poster, the people below must "
"still look like a documentary photograph.")

POV = ("This is a first-person point of view: you are a resident of this town and the picture is exactly "
"what your own eyes see as you go about the day. No part of the viewer's own body is ever in the picture "
"— no hands, no arms, no legs, no feet, no lap, no shoulders, and no reflection of the viewer in any "
"glass, water, metal or mirror — and the viewer is never seen from outside. You never look down at your "
"own hands or feet: your eyes are always looking out, around, ahead or up. People may glance towards you "
"for a moment and then carry straight on with what they were doing, the way you glance at someone you "
"live beside, but nobody holds a long stare into the lens and nobody poses for you.")

# ─────────────────────────────────────────────────────────────────────────────
# ② THẾ GIỚI v2 — hai lớp, và LỚP XA LÀ CHỮ KÝ CỦA KÊNH
# ─────────────────────────────────────────────────────────────────────────────

# ⭐ Lớp GẦN: phố Showa mặt đất, CHẬT. Mẫu đo được: mọi khung ngoại đều kín đồ, không có
#    một mảng tường trống nào. Đây là thứ v1 thiếu nhất (v1 thưa, nhiều trời).
TOWN = ("This is an ordinary Japanese town at street level, and it is CROWDED WITH THINGS — every surface "
"lived on: narrow streets barely wide enough for two people to pass, small family shops opening straight "
"onto the road with their goods stacked out to the kerb, cloth noren hanging in the doorways, canvas and "
"corrugated-steel awnings out over the pavement, hand-painted enamel and timber signboards stacked one "
"above another up the shopfronts, paper lanterns, vending stands, wooden crates, bicycles leaning against "
"every wall, potted plants crowding every doorstep in their dozens, a red cylindrical post box, a "
"telephone pole with tangled overhead wires crossing the whole frame, drainage grates and worn kerbstones "
"underfoot. There is no empty wall anywhere: what is not shopfront is climbing ivy, a poster board, a "
"stacked crate or a bicycle.")

# ⭐⭐ Lớp XA: SIÊU ĐÔ THỊ CHỒNG TẦNG. Đây là signal riêng của kênh — thiếu nó thì cảnh chỉ là
#    phố Showa thường. Đo trên mẫu: có mặt ở 14/16 khung ngoại.
# 🔴 Ban dau chi noi "rank upon rank of buildings" => model ve NHA CAO TANG KINH HIEN DAI (W2, W3).
#    Phai goi ten HINH DANG khong ton tai o doi thuc: thap xoan, tang loe ra, cau noi tren cao.
MEGACITY = ("And behind the little town, filling the whole upper half of the distance, stands a COLOSSAL "
"LAYERED CITY, and it is NOT a modern city of glass office towers: its buildings are impossible spiralling ziggurats that widen as they rise, tier stacked on tier like a pagoda grown enormous, "
"their terraces planted green, joined to one another by slender bridges and elevated roadways and "
"steel railway viaducts high in the air, "
"stacked one above another and receding up into the sky, level after level of them going up further than "
"you can see, small trains crossing the high viaducts, everything softened by distance and pale haze so "
"that the far levels are almost silhouettes. It is built out of exactly the same honest materials as the "
"street you are standing in — painted concrete, corrugated steel, tile, timber and glass — only "
"unimaginably more of it, stacked impossibly high. It is enormous and calm, never threatening. "
"It is NOT a cyberpunk city: no neon, no holograms, no glass towers, no glowing signs, no flying cars, "
"nothing hovering; every level of it is rooted and physically supported on the one below.")

# -----------------------------------------------------------------------------
# ⭐⭐ RETRO_TECH -- VAT VIEN TUONG PHAI O TIEN CANH, TRONG TAM VOI (2026-09-22)
#
# 🔴 LOI LOP do duoc tu 3 canh thu: toan bo yeu to vien tuong nam trong khoi MEGACITY
#    = HAU CANH XA. W1 (nhin doc hem) co thap xoan vi thap roi dung DIEM TU; W2 (nhin tu
#    tren xuong mai) va W3 (shoutengai co mai) thi model ve THANH PHO HIEN DAI THUONG
#    => mat SACH vien tuong. Hau canh la thu model tuy y bo; tien canh thi khong.
# => Vien tuong phai la VAT mình cham duoc, dat canh chu the. Cung dinh luat
#    `camera-language.md` §5.1: mau ruc phai den tu VAT, khong den tu grade.
#
# ⚖️ Moi vat duoi day la 昭和 + mot buoc ky thuat KHAC (hoi nuoc / khi nen / chan khong /
#    tu truong) -- KHONG phai dien tu hien dai. Va khong vat nao mang CHU/SO.
# -----------------------------------------------------------------------------
RETRO_TECH = ("And this is not quite our world: the ordinary Showa things here have gone one step "
"further down their own mechanical path, and several of those things are RIGHT HERE IN THE "
"FOREGROUND within arm's reach, not far away — a brass and glass vending stand with a pressure dial "
"and copper piping, a little three-wheeled delivery truck with a riveted boiler and a thin plume of "
"steam at its tailpipe, pneumatic message tubes running in bundles along the shopfronts with brass "
"caps where they turn, street lamps with fluted glass shades over visible glowing filaments, a "
"shopfront television in a timber cabinet with a deeply curved glass screen, an electric fan with a "
"brass cage, a mechanical cash register with rows of round keys, a slender monorail rail on concrete "
"piers threading between the buildings just above the rooftops with a single riveted carriage "
"gliding along it. None of these objects carries any writing, lettering or numbers of any kind. "
"Everything is metal, glass, timber and steam — never plastic, never electronic, never a screen "
"with an image on it, never neon, never a hologram, and nothing hovers or floats.")

# Phần xanh — đo được ở mẫu: cây và dây leo dày ở gần như mọi khung, và đó là thứ làm nó "dịu mắt"
GREEN = ("Growing things are everywhere and they are thriving, not overgrown ruins: ivy and creeper "
"climbing the concrete walls in broad healthy sheets, a large old tree leaning over the street, potted "
"plants and window boxes on every ledge and step, weeds green in the kerb cracks.")

# §5.1 v2 — "cũ được CHĂM". Đổi vật liệu từ gỗ/đá núi sang vật liệu phố Nhật.
MATERIALS = ("This is Japan in the year Showa 100, an alternate present where the Showa era never "
"ended. Everything is old but CARED FOR — swept, wiped down, kept in repair, worn smooth and glossy "
"from use rather than broken, paint faded soft and even rather than peeling, brass and copper kept "
"polished: painted concrete gone chalk-soft with age, corrugated steel in faded green and cream, "
"glazed wall tile, timber darkened by decades of hands, shop glass, canvas, paper, enamel.")

# ─────────────────────────────────────────────────────────────────────────────
# ③ MÁY QUAY — POV đi bộ, rung li ti (đã đo đạt: jitter 0,079 vs mẫu 0,05–0,24)
# ─────────────────────────────────────────────────────────────────────────────
WALK = ("You are on foot, and the picture carries the faint rise and fall of a person's slow gait — "
"but the movement is tiny, one soft settle about every second, never a jog and never a camera on a "
"shaking rig. No jolt, no swing, no bounce, and the background stays solid and does not warp as it "
"passes.")

STAND = ("You have stopped walking and are simply standing there looking, and the picture floats very "
"gently the way the view does when someone stands and breathes: it drifts up and down by less than a "
"centimetre, one slow rise and fall every three or four seconds, but it never jolts, never swings and "
"never bounces, and the background stays solid and does not warp.")

SIT = ("You are sitting down, and the picture is as steady as a seated person's gaze: it floats only with "
"your breathing, up and down by less than a centimetre, one slow rise and fall every three or four "
"seconds, but it never jolts, never swings and never bounces, and the background stays solid.")

HANDHELD = ("The picture is carried, not mounted: it has the faint natural unsteadiness of a camera held "
"in the hands of someone on foot rather than locked to a tripod or a dolly. The frame never sits "
"perfectly still — it breathes and settles by a hair, and there is the smallest live tremor in it the "
"whole time, the kind you feel rather than see. But it stays gentle: no jolt, no swing, no wobble, no "
"bounce, nothing sharp or sudden, and the tremor is always smaller than you would notice if you were not "
"looking for it.")

# §8.5 — toc do la SO DO. Don vi cho POV di bo la BUOC CHAN, khong phai met dolly.
#
# ⭐ THANG 4 MUC (2026-09-22) — user noi "toc do cham cham nhu video thoi" LAN THU HAI.
#   Lan dau tao clamp bua 30-80px, roi do mau ra "117px median" va noi tran len.
#   Lan nay khong clamp: do lai mau bang DUNG CONG THUC tool dang dung, va nhan ra
#   "117px" do tren CUA SO 8 GIAY BAT KY -- cua so nao chua CAT CANH thi dich khung
#   khong lo => median bi day len. Clip cua minh la MOT shot 8s khong cat.
#   => Phai so voi SHOT cua mau. So chot nam o PACE_MEASURED duoi day.
#
# Moi muc ta bang SO BUOC CHAN + QUAN HE VOI MEP KHUNG (media-library.md §2.10 ⑥:
# model nghe VI TRI, khong nghe ti le/con so tuyet doi).
PACE = {
 # gan nhu dung, chi nhich -- dung cho canh "tho"
 "creep": ("You are barely moving at all: over the whole eight seconds you take perhaps one slow "
   "step, and the framing only just begins to close in — the change is small enough that you feel it "
   "rather than see it. Whatever else moves in the frame moves more than you do."),
 # ⭐ MAC DINH -- di bo rat cham, dung muc user goi la "cham cham"
 "stroll": ("You are walking very slowly, the pace of someone with nowhere to be: over the whole "
   "eight seconds you take only two or three unhurried steps, and the nearest thing beside you — the "
   "post, the doorway, the bicycle — drifts gently back past the edge of the frame and out of it. "
   "That one object leaving the frame is the whole of the movement; nothing rushes towards you and "
   "nothing sweeps past. It is a slow amble, never a march."),
 # di bo binh thuong -- CHI dung khi canh doi (di qua het mot con hem)
 "walk":  ("You are walking at an ordinary unhurried pace: in these eight seconds you take five or "
   "six steps, and what was in the middle distance at the first frame is close in front of you by the "
   "last. It is a walk, not a drift."),
}
# do duoc tren video mau PUotm8YDbKM -- xem tools/measure_pace_ref.py
PACE_MEASURED = None      # dien sau khi do xong; dung de dat nguong cho check_test_world.py
# ⭐ MAC DINH = creep, doi tu "stroll" ngay 2026-09-22 sau khi do mau:
#   median 36,5px/8s tren khung 1280 = 2,8% be ngang => MAU GAN NHU KHONG DI MAY.
#   "Nhe nhang dap diu" cua mau den tu NGUOI+VAT dong trong khung gan nhu dung,
#   khong den tu viec may di. Canh W1 chay "stroll" do ra 100,9px = nhanh gap 2,8x.
SLOW_WALK = PACE["creep"]
PACE_MEASURED = {"median_px_per_8s": 36.5, "p25": 13.6, "p75": 100.2,
                 "pct_under_20px": 30, "pct_under_40px": 54,
                 "jitter_median": 0.032, "n_shot": 63,
                 "ref": "PUotm8YDbKM · tools/measure_pace_ref.py"}

SLOW_STAND = ("You are completely still. Over the whole eight seconds the framing barely changes at all "
"— your head leans or turns only a fraction, and nothing in the picture slides or drifts because of you. "
"Whatever moves in the frame is the people, the cloth, the steam or the traffic moving on their own, "
"never the viewpoint.")

# ⭐ ÉP ĐI THẬT — v1 đo được chỉ 24,7px vì mốc cuối neo vào NGƯỜI ĐANG ĐI.
#   Phố hẹp là lợi thế: tường hai bên trôi qua là bằng chứng hình học rất mạnh.
# ⚠️ Khoi nay CHI con lo mot viec: chung minh la MAY di, khong phai NGUOI di toi cho may.
#    Luong di bao nhieu la viec cua PACE. Ban cu noi ca hai => cong don => di qua nhanh.
GROUND = ("The movement is yours, not theirs: the ground passes slowly beneath you the whole time, so "
"that even if every person in front of you stood perfectly still the framing would still change. It is "
"never the people walking towards the camera that makes the view close in.")

EASE = ("you start moving gently and come to rest gently, with no sudden change of speed and no speed "
"ramping")

# -----------------------------------------------------------------------------
# ⭐⭐ MOMENT -- CAM XUC. user 2026-09-22: "no khong co cam xuc, kieu bi voi ay"
#
# 🔴 Ba canh thu deu la PHONG CANH CO NGUOI DI LAI -- khong ai lam gi de minh quan tam.
#    W1 co ba cu dan len o cua たばこ o frame 1, roi may DI QUA va mat han o frame 4.
#    => Hai nguyen nhan, va chung CONG DON:
#       (a) khong co khoanh khac nao duoc thiet ke
#       (b) may di nen co thi cung vut qua
# => Luat: canh nao cho CAM XUC thi may PHAI DUNG (pose=stand + PACE creep).
#    Canh di bo la canh CHUYEN, khong phai canh cam xuc. Dung doi mot clip 8s lam ca hai.
#
# Khuon lay tu camera-language.md §6.2 (trao doi) + §6.6 (vong cung 3 nhip, ta bang CO THE).
# -----------------------------------------------------------------------------
MOMENT = ("This shot exists for one small human moment and the camera stays with it to the end. What "
"happens has three beats and the middle one is the peak: something leads up to it, it comes out, and "
"then it settles again. Describe it only through the body — where the eyes go, what the hands are "
"doing, which way the head tilts, how the breath changes — never by naming the feeling. And it must "
"be an exchange: something passes between two people, or between a person and the thing in their "
"hands. Nobody performs it for the camera; it would have happened exactly the same if you had not "
"been standing there. There is quiet time left at the end of the shot after it is over.")

# Kho khoanh khac dung duoc -- moi cai la MOT vong cung 3 nhip, ta bang co the
MOMENTS = {
 "tabako_ba":   ("The old woman in the tobacconist's window has her head down over her knitting; she "
   "reaches the end of a row, stops, holds the work out at arm's length to look at it, and her eyes "
   "narrow into two creases as the corners of her mouth go up — then she lowers it back into her lap "
   "and her hands start again."),
 "trao_tien":   ("A woman holds out a coin to the shopkeeper with both hands; he takes it, and while "
   "his fingers are still closing on it he is already reaching behind him for the parcel, and he sets "
   "it into her hands with a small nod that she answers with a smaller one."),
 "tre_con":     ("A boy stops dead in front of the vending stand and tips his head right back to look "
   "up at the pressure dial, his mouth open; his mother's hand comes into the frame and rests on the "
   "top of his head, and he lets himself be steered away still looking back over his shoulder."),
 "quat_dien":   ("An old man sits in the doorway with the brass-caged fan turning beside him; the fan "
   "reaches his end of its arc and the air lifts the hem of his shirt and the newspaper on his knee, "
   "he flattens the paper with one hand without looking up, and the fan turns away again."),
 "chia_kem":    ("Two schoolgirls share one ice from a paper cup on the kerb, and the one holding it "
   "turns it round so the other gets the side that has not been eaten yet."),
 "nhin_thap":   ("A man stops in the middle of the lane with his shopping bag still in his hand, looks "
   "up at the spiralling towers for a moment the way you look at weather, and then walks on."),
}

# -----------------------------------------------------------------------------
# ⭐⭐ ALIVE — KHUNG PHAI SONG. Do duoc 2026-09-22 tren lo 40 clip:
#   % khung DUNG YEN TUYET DOI: trung vi 43,5%, 27/40 clip >10%, va 4 clip 97-100%
#   (task_039 = 100%: hai frame lien tiep GIONG HET NHAU suot 8 giay = mot tam anh).
#   Mau do duoc 3,0-3,8%.
#
# 🔴 Nguyen nhan KHONG phai may dung yen — mau cung gan nhu khong di may (36,5px = 2,8%
#    be ngang). Nguyen nhan la TRONG KHUNG khong co gi dong. Khoi canh tho cu viet
#    "Nothing happens but the mist" — noi KHONG CO GI XAY RA thi model lam dung the.
#    May tinh + vat dong = tinh lang.  May tinh + vat tinh = ANH CHET.
#
# => Ep NGUOC: phai co >=2 thu dong LIEN TUC suot 8 giay, va goi ten chung.
# -----------------------------------------------------------------------------
ALIVE = ("This is a moving picture, not a photograph: SOMETHING IN THE FRAME IS ALWAYS MOVING, from "
"the first frame to the last, without a single second in which the picture could be mistaken for a "
"still image. At least two separate things move continuously and independently of each other for the "
"whole eight seconds — a cloth or a noren or hanging washing lifting and falling in the moving air, "
"steam or smoke rising and leaning away, leaves and potted plants stirring, a paper lantern turning "
"slowly on its cord, dust and pollen drifting through a bar of light, the filament of a lamp flickering, "
"an electric fan turning, water dripping, a monorail carriage crossing far behind, a person passing "
"through the far end of the frame. Even in a shot where nobody is present, the air itself is in motion "
"and everything light enough to move is moving. Nothing in this picture is frozen.")

CALM = ("This is one small quiet moment and nothing else happens in it: no other event, no second thing "
"starting, nobody else arriving. The whole eight seconds are given to that one thing alone, unhurried, and "
"there is time left over at the end where no new event begins — but the air, the cloth and the light go "
"on moving through it: quiet never means frozen.")

# ─────────────────────────────────────────────────────────────────────────────
# ④ CẤM
# ─────────────────────────────────────────────────────────────────────────────
AVOID = ("Everyone is dressed for the Showa era — cotton shirts, work trousers, aprons, simple "
"dresses, school uniforms, a towel round the neck; NO face masks on anyone, no modern branded "
"clothing, no logo caps, no modern backpacks or handbags, no smartphone, no flat screen, no plastic "
"drink bottle, no sneakers with logos. Nothing here is rusted, flaking, grimy or derelict — this is a "
"well-kept working neighbourhood, not a ruin and not a slum. Nobody poses or performs for you and no "
"face fills the whole frame; every person in the crowd is turned away, seen from behind, looking down "
"at what they are doing, or standing well back and soft in the shallow focus — not one background face "
"is sharp, frontal and close enough to read. No distorted, melted or asymmetric faces and no warped "
"hands anywhere: if a background face cannot be rendered cleanly it must be turned away or left out of "
"focus rather than shown. No sepia or brown-washed colour, no faded washed-out look, no oversaturated "
"colour on the ground or on people, though the sky itself may be deep and vivid. No speed ramping, no "
"slow motion, no rubbery bending limbs, no feet sliding across the ground, no extra fingers. No frame "
"and no border of any kind around the picture, no film strip and no sprocket holes.")

# 🔴 CAM SUONG DA TRUOT 3/3 CLIP (2026-09-22): guard nay o 5% prompt ma ca ba clip van day chu
#    bia co doc duoc (苑忉朶 · 木脊筒専 · 余車圧). Vi sao: pho Nhat thi PHAI co bien hieu, nen cam
#    het thi model tu lap bang chu bia. Cung dinh luat "negative khong thang token phong cach"
#    (camera-language §0) -- phai CHO no thu dung thay vi cam thu sai.
# => Doi chien thuat: XIN it bien mang DUNG MOT TU quen, con lai la MANG MAU TRON.
NO_TEXT_NUM = ("About signs, and this is important: most of the shop signboards in this picture carry NO "
"writing at all — they are plain painted boards, clean flat panels of faded green, cream or dark red with "
"nothing written on them, or their writing is hidden behind an awning, turned edge-on to you, or so far "
"down the street that it is a soft blur. AT MOST TWO signs anywhere in the frame carry any writing, and "
"each of those two carries only ONE short common Japanese word in large clean brush strokes, correctly "
"formed: たばこ or ゆ or 氷 or パン or さかな. Nothing else in the picture carries any writing anywhere — not "
"the crates, not the awnings, not the lanterns, not the machines, not the posters, not the vehicles. And "
"no numbers, no digits, no prices, no timestamps, no counters and no clock faces anywhere in the picture, "
"least of all in the corners of the frame. A blank board is always right; an invented character is always "
"wrong.")

# ─────────────────────────────────────────────────────────────────────────────
# ⑤ TRỜI / ÁNH SÁNG — mẫu đo được là NẮNG GẮT có bóng rõ, không dịu mờ như v1
# ─────────────────────────────────────────────────────────────────────────────
SKY = {
 "day": ("Above the layered city the sky is a deep saturated cobalt blue, deepening towards the top of the "
   "frame, and the cumulus clouds are pure brilliant white with crisp defined edges and clear sculpted "
   "volume, piled high and lit hard from one side — the blue and the white pushed strongly against each "
   "other, vivid and clean, the way a summer sky looks photographed on strong colour slide film, like an "
   "old railway travel poster. ONLY the sky and the clouds carry that heightened colour: everything below "
   "the skyline — the people, their skin and clothes, the concrete, the steel, the signboards — stays "
   "completely photographic and real."),
 "window": ("Through the window or the doorway the sky is a deep saturated cobalt blue over the stacked "
   "levels of the far city, the cumulus tops pure brilliant white with crisp defined edges and clear "
   "sculpted volume, vivid and clean, the way a summer sky looks photographed on strong colour slide "
   "film. ONLY the sky and the clouds carry that heightened colour: everything in the room — the people, "
   "their skin and clothes, the timber, the ceramic — stays completely photographic and real."),
 "dawn": ("The sky over the layered city is a clear deep blue still holding the last of the night at the "
   "top of the frame, the cumulus tops lit pink and gold where the low sun strikes them, crisp-edged and "
   "sculpted, vivid and clean, the way a sunrise looks photographed on strong colour slide film. ONLY the "
   "sky and the clouds carry that heightened colour: everything else stays completely photographic and real."),
 "dusk": ("The dusk sky over the layered city is a deep saturated indigo grading to warm gold at the "
   "skyline, the cumulus lit hard pink and white with crisp defined edges and clear sculpted volume, "
   "vivid and clean, the way a sunset looks photographed on strong colour slide film. ONLY the sky and the "
   "clouds carry that heightened colour: everything below the skyline stays completely photographic and real."),
 "night": "",
}

LIGHT = {
 "day": ("Clean bright summer daylight with the sun high and strong: hard clear sunlight falling in "
   "sharp-edged patches down the street and through the awnings, real shadows with defined edges but still "
   "open and filled with bounced light so that nothing goes black and nothing burns out, deep healthy "
   "green on the leaves, warm cream and faded green on the painted steel, and the far levels of the city "
   "fading gently into pale blue haze; strong and clear but never glaring, easy on the eyes."),
 # 🔴 THEM 2026-09-22: bang cu KHONG CO "dawn" nen 3 canh binh minh cua tap 01 phai dung
 #    light="day" = "sun high and strong" — choi thang voi SKY["dawn"] ("low sun", "last of the
 #    night"). Mot prompt tu mau thuan thi model chon mot ve, thuong la ve MANH hon (nang gat).
 "dawn": ("The cold blue light of just before sunrise, the lane still in shadow and the sun not yet "
   "down on the ground: no hard sunlight anywhere at street level, everything soft and even and "
   "slightly blue, the street lamps still burning warm against it, and only the highest roofs and the "
   "tops of the far towers catching the first low gold. Gentle contrast, nothing glaring."),
 "interior": ("Warm natural colour with honey-coloured timber; one window or open shopfront as the main "
   "source of light falling off gently into the shade of the room, the bright street visible beyond it, "
   "warm orange lamp light in the corners, shadows soft and filled with bounced light; nothing glaring, "
   "gentle contrast, easy on the eyes."),
 # 🔴 THEM 2026-09-22 (lan thu hai cung benh "buoi"): LIGHT["interior"] viet cho NOI THAT BAN
 #    NGAY ("the bright street visible beyond it"), nhung 4 canh dem cua tap 01 (28·29·30·33)
 #    deu dung no => prompt vua noi DEM vua noi pho SANG ngoai cua. Gate cu MIEN TRU moi canh
 #    interior nen no lot — mien tru qua rong cung la mot kieu gate hong.
 "interior_night": ("Warm lamplight is the only light in the room: one low lamp with a fluted glass "
   "shade, its glow falling off quickly into the dark corners, the window a flat black rectangle with "
   "nothing visible through it, the paper of the sliding screen faintly lit from the next room. The "
   "picture is allowed to be genuinely dark and quiet, with gentle contrast and nothing glaring."),
 "dusk": ("Warm natural colour, the deep blue of dusk against the warm orange of the shop lights and the "
   "paper lanterns, the two strong against each other but the light on the street itself soft and open, "
   "shadows staying filled, the stacked far city fading into blue haze with its windows coming on in tiny "
   "points; nothing glaring, easy on the eyes."),
 "night": ("Deep blue night, the shop windows and the paper lanterns the only warm light in the street, "
   "their glow falling off quickly into the dark, the far city standing black with thousands of tiny lit "
   "windows scattered up it; the picture is allowed to be genuinely dark and quiet, with gentle contrast "
   "and nothing glaring."),
}

OPTICS = ("Shallow depth of field with the near subject sharp and the far city melting softly out of "
"focus, one out-of-focus object at the very edge of the near foreground so the picture has a near layer, "
"a middle layer and a far layer, fine photographic film grain over the whole picture, evenly exposed "
"right into all four corners with no darkening or shading at the edges, the picture is a clean rectangle "
"running right out to all four edges with nothing around it, horizontal landscape video, widescreen, "
"clearly wider than it is tall, not vertical and not square.")

CROWD = {
 "busy":  ("Beyond them a steady flow of thirty or more other people moves along the street and under the "
   "awnings, all of them small in the frame, mostly turned away, soft in the shallow focus, their faces "
   "never sharp — a sense of a busy town rather than a set of individual faces."),
 "some":  ("Behind them a dozen or so other people come and go, well back and soft in the shallow focus, "
   "nearly all seen from behind, none of their faces sharp."),
 "few":   ("One or two other people pass in the distance, seen from behind and soft in the shallow focus."),
 "none":  "",
}

TAIL = ("Remember three things above all: this is live-action photography and never anime or illustration; "
"the people must look like real photographed human beings, never 3D characters; and behind the little "
"street stands the colossal layered city going up into the sky.")
TAIL_SIGN = ("Remember three things above all: this is live-action photography and never anime or "
"illustration; the Japanese characters on the signs must be correctly formed and crisp; and behind the "
"little street stands the colossal layered city going up into the sky.")

# §4a CAST_LOCK
CAST = {
 "mother": ("THE MOTHER: a Japanese woman of about forty, small and slight, her hair pinned up in a low bun "
   "with a few strands loose at the temple, a pale blue short-sleeved cotton blouse and a small-flowered "
   "apron, plain dark trousers, no make-up, an ordinary tired kind face."),
 "daughter": ("THE DAUGHTER: a Japanese girl of about eight, a blunt bob cut to her jaw with a straight "
   "fringe, a white short-sleeved shirt under a pale yellow pinafore dress, white socks and worn leather "
   "shoes, a round face with slightly chapped cheeks."),
 "father": ("THE FATHER: a Japanese man of about forty-five, tall and lean, hair parted at the side and "
   "going grey above the ears, a white short-sleeved shirt with the collar open and grey work trousers, a "
   "squarish face with deep lines at the mouth."),
}

POSE_BLOCK = {"walk": WALK, "stand": STAND, "sit": SIT}
POSE_SLOW  = {"walk": SLOW_WALK, "stand": SLOW_STAND, "sit": SLOW_STAND}


# =============================================================================
# ⭐⭐ (⑥) REALISM — khối máy/ánh sáng/nhịp người DÙNG CHUNG với showa: `_media_library/realism_blocks.py`
#     (chốt 2026-09-22 sau 3 vòng thử `06_VIDEO/01_tou-no-fumoto/_realism/`). Kênh này chỉ giữ THẾ GIỚI.
# =============================================================================
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))), "_media_library"))
from realism_blocks import (REALISM_HEAD, STILL_HEAD, LOCKED_CAM, DRIFT_CAM, cam_block, LIGHT as LIGHT_MUTED,
                            SUBJECT_GENTLE, SILENT_REALTIME, FILM_TAIL, build_pair, gate_prompt)

# THẾ GIỚI bản ngắn — đặt vào MỌI cảnh ngoại (vòng 2: 2/3 clip không có gì viễn tưởng ⇒ "chưa giống")
WORLD_SHORT = ("And this street is not in our world: rising directly behind the roofs and filling the whole "
"upper half of the frame stand the tiered spiralling towers of a colossal old-fashioned city — terrace "
"stacked on terrace like pagodas grown enormous, planted green, joined by slender bridges with a small "
"train crossing one of them — built of the same concrete, tile and timber as the street, never glass, "
"never neon, softened by haze but unmistakably there and enormous in scale next to the little shops.")
