# -*- coding: utf-8 -*-
"""_patch_collage23.py — viết lại mô tả cảnh của `_scenes23.py` sang NGÔN NGỮ COLLAGE.

🔴 VÌ SAO: bản đầu bê nguyên mô tả của đường PHOTOREAL sang collage ⇒ giữ được style, mất
   nội dung. Đo được: **32% cảnh chở ý · 45% là người diễn không có vật nào trong khung**
   (user: *"phong cách thì oke nhưng video chưa thể hiện hết ý"*).
   Đối chiếu bản vox-director đã ra `final.mp4` (`out/pho-30s`): MỖI cảnh của họ LÀ một lập
   luận bằng giấy — lịch bóc ngược về 1900 · ba dòng chảy hợp vào một tô · bản đồ xé dọc vĩ
   tuyến 17 với hình người giấy đi theo vệt băng dính.
   ⇒ Collage là phương tiện GIẢI THÍCH: bức tranh phải lập luận, không phải minh hoạ cảm xúc.
      Ở đường photoreal, ý nằm ở telop + thẻ số; ở đây ý phải nằm TRONG hình.

Chạy MỘT LẦN: python tools/_patch_collage23.py  (có backup .bak_photoreal)
"""
import io
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"E:\Claude\Projects\youtube-jp-nenkin\tools\_scenes23.py"

# scene_index -> mô tả collage mới. Khuôn đổi theo NỘI DUNG, không giữ khuôn cũ.
NEW = {
0:  'VIZ: a bank passbook cut from cream card lying open, every printed entry line torn away so the column is bare, and beside it a taped paper arrow pointing into an empty cut-out box where the money should be',
1:  'CROWD: a public service counter built from flat paper panels, a clerk cut-out sliding a plain document across it toward a seated elderly visitor, a row of waiting cut-out figures behind',
2:  'VIZ: on the left four torn calendar sheets stacked in a leaning pile, on the right a tall banded stack of paper banknotes of almost the same height, and bare newsprint between them with nothing joining the two',
3:  'VIZ: a long paper strip carrying a row of identical small cut-out coins running across the frame, and a pair of scissors cut from steel-grey card poised open over the strip two coins from its end',
4:  'an elderly woman cut-out with her brow strip pulled together, an empty torn-paper speech bubble taped beside her head',
5:  'META: a paper envelope slides into a slot in a flat machine built from layered card, and behind the slot a row of cut-out paper gears begins to turn',
8:  'DESK: a paper desk seen flat-on, covered with cut-out research tools — a magnifier, a folded ruler, a stack of plain documents and a small lamp, all in torn card',
9:  'META: a channel of cut-out coins flows steadily from left to right, a single small postcard drops into a slot above it, and a plain paper gate swings down across the channel and stops the flow dead',
10: 'HOLD: a large official envelope cut from cream card held up square-on to the camera, its address window a bare rectangle, tape across both corners',
13: 'VIZ: an opened paper form lying flat with five ruled boxes, each box already filled by a solid bar of charcoal ink, a strip of tape across the head of the sheet',
14: 'VIZ: a tall filing cabinet cut from grey card standing open on one side, its drawer pulled out and packed edge to edge with identical blank paper record cards',
15: 'SPLIT: two paper boxes side by side — the left one crammed with blank record cards, the right one completely empty — and the bare newsprint gap between them crossed by nothing at all',
16: 'VIZ: the same two paper boxes with a cut-out paper bridge between them severed in the middle, the two halves not meeting over the bare gap',
17: 'an elderly man cut-out leaning forward, one paper hand raised a little way from his chest',
18: 'CROWD: a street of flat paper houses seen head-on, a cut-out envelope landing on the doorstep of most of them, and four houses standing with nothing on their step',
19: 'DESK: a paper desk with a pocket calculator cut from grey card and a blank ruled notebook lying open beside it',
21: 'VIZ: two heavy law volumes cut from dark card standing open side by side, a torn ribbon bookmark hanging from each',
24: 'VIZ: forty-eight tiny identical paper coins laid out in four neat rows of twelve on bare newsprint',
26: 'VIZ: one paper coin cut large and standing in the foreground, and behind it the full grid of forty-eight small coins running off toward the back',
27: 'VIZ: a row of cut-out coins riding a paper conveyor strip, the leading coin tipping over the edge into a torn dark gap',
28: 'an elderly woman cut-out with her head tilted, an empty torn-paper thought bubble floating above her',
30: 'VIZ: one envelope at the top of the frame and four torn paper paths running down from it, three ending in bare cut-out boxes and the fourth crossed over with a strip of tape',
31: 'SPLIT: a thick cream envelope standing on the left and a single thin postcard on the right, both square-on, the thin one noticeably smaller',
32: 'an elderly man cut-out with his shoulder strips dropped and his head lowered a few degrees',
33: 'VIZ: the thin postcard cut large and standing in the foreground while the thick envelope sits small and dull behind it',
35: 'VIZ: a horizontal bar built of stacked paper squares with several squares missing, and a paper hand cut-out laying a fresh square into one of the gaps',
36: 'an elderly man cut-out with his chin lifted, his chest strip rising once',
37: 'HOLD: a blank application sheet held out flat toward the camera in both paper hands, one corner curling up',
39: 'VIZ: a long paper bar running across the frame with a clean scissor cut a third of the way along it, the severed longer piece lying discarded beside it',
41: 'VIZ: a paper timeline strip with two torn notches cut into it, a small postcard landing on each notch',
42: 'an elderly woman cut-out with her chin lowered, looking down at the bare paper surface in front of her',
43: 'VIZ: a paper balance scale cut from card, the pan holding a single thin postcard hanging low and the pan holding a thick envelope riding high',
44: 'VIZ: two different paper letterheads pinned side by side, each a plain block of a different colour, a taped arrow running from the second one out toward the frame edge',
45: 'CROWD: the sorting floor of a post office built from flat paper panels, three staff cut-outs at a long counter stacked with trays of envelopes',
46: 'VIZ: an envelope bouncing off the door of a paper house and flying back, while a second house of a different cut-out shape stands further along with an empty step',
47: 'CROWD: a ward office counter built from paper panels, a clerk cut-out and an elderly visitor cut-out facing each other across it, seated figures waiting behind',
48: 'an elderly man cut-out turning his head, his brow strip pulled together',
50: 'VIZ: a cut-out envelope flying over a torn paper sea toward a distant paper coastline, a dotted masking-tape line marking its path',
51: 'VIZ: four envelopes laid out in a row, each resting on a different flat colour block of paper',
52: 'DESK: a paper desk with a teacup cut-out and a small stack of documents, seen flat-on',
53: 'META: an envelope disappearing into a one-way slot in a flat paper wall, the slot sealed behind it with a strip of tape, and a second envelope stopped in front of the sealed slot',
55: 'an elderly man cut-out with both paper palms lifted a little way from the surface in front of him',
57: 'VIZ: a flat paper screen rectangle standing upright with a blank document sliding out of its lower edge and settling on the surface below',
58: 'VIZ: a paper telephone handset cut from dark card, its cord unrolling across the frame and turning into a line that ends at a small envelope',
59: 'CROWD: a pension office counter built from paper panels with a queue of cut-out figures waiting, rows of paper chairs behind them',
61: 'an elderly couple cut-outs seated side by side, both dipping their head strips once toward the camera',
62: 'DESK: a paper desk with an open blank notebook and a pencil cut from mustard card lying across it',
63: 'an elderly woman cut from grainy black-and-white photographic paper, seated square-on, a teacup cut-out beside her',
64: 'VIZ: four calendar sheets peeling off one after another and curling away, and lying face-down underneath them a single unopened envelope',
65: 'VIZ: a paper calendar strip running across the frame with the last two squares ringed in torn red paper',
66: 'an elderly woman cut-out with her eyelids lowered, her shoulder strips settling',
67: 'META: a large paper clock face with a bare dial and a single plain strip for a hand, and a small cut-out figure standing directly beneath it',
68: 'SPLIT: the same paper calendar strip shown twice, one above the other — the upper one whole, the lower one with its final two squares torn off',
69: 'VIZ: a banded stack of paper notes with its top third torn clean away and lying separate on the bare newsprint',
70: 'an elderly man cut-out with his head tilted and his mouth cut-out slightly open',
71: 'VIZ: two pension slips cut from cream card lying side by side, the right-hand one crossed out with a strip of dark tape',
74: 'VIZ: a stair of paper blocks rising step by step toward the right, each step a little taller than the last',
75: 'SPLIT: on the left a rising stair of paper blocks, on the right a perfectly flat row of identical blocks with a pair of scissors closing on its far end',
76: 'an elderly woman cut-out with her eye cut-outs wide and her mouth cut-out open',
78: 'HOLD: a blank written statement sheet held out flat toward the camera, a strip of tape along its top edge',
79: 'VIZ: a paper ledger with one of its lines lifted clean out and replaced by a brighter strip, and beside it a full untouched stack of paper notes',
80: 'CROWD: a consultation room built from flat paper panels, three desks in a row, a clerk cut-out and an elderly visitor cut-out at each',
81: 'HOLD: a single plain postcard held up square-on beside a paper face, its surface completely bare',
82: 'VIZ: a paper month grid of blank squares with a small postcard landing on the very first square',
84: 'an elderly man cut-out with both paper hands raised to the sides of his head',
87: 'META: a paper channel of cut-out coins with a plain gate lowered across it, the coins piling up motionless behind the gate and the channel beyond it empty',
89: 'VIZ: two paper slips set apart from a larger pile, each marked with a taped circle',
90: 'HOLD: a plain postcard held flat, a single bare square box on its face marked with a small torn paper tick',
91: 'DESK: a paper desk with a stack of plain documents, a teacup and a paper envelope, seen flat-on',
93: 'an elderly woman cut-out with her head tilted, her brow strip drawn together',
94: 'VIZ: two adjacent squares of a paper calendar grid cut large, the earlier one ringed with torn red paper and the later one left bare',
98: 'VIZ: two paper certificates lying side by side, the left one yellowed with a torn corner and pushed aside, the right one crisp and square',
99: 'VIZ: a small cut-out envelope crawling along a long paper calendar strip, still far from the marked square at its end',
100:'HOLD: a single plain certificate sheet held up square-on in both paper hands',
101:'an elderly woman cut-out with one paper palm resting flat on the surface, her face turned toward the camera',
104:'VIZ: two paper piles of coins standing apart with a wide stretch of bare newsprint between them, and a small cut-out figure standing alone in that gap',
105:'DESK: a paper desk with an open blank notebook, a teacup and a pencil, seen flat-on',
108:'an elderly woman cut-out dipping her head strip once, her hands out of frame',
112:'an elderly couple cut-outs seated side by side, both turning their head strips toward the camera',
113:'DESK: a paper desk with a blank notebook closed and a teacup beside it',
114:'CROWD: a small coffee shop built from flat paper panels seen from inside, a cut-out master standing behind the counter, two customer cut-outs at the paper tables',
115:'VIZ: five paper envelopes standing in a row on a paper shelf, three of them still sealed and dulled with grey halftone dust',
116:'DESK: a paper desk with a calculator cut from grey card and a fan of receipts spread beside it',
117:'an elderly couple cut-outs seated side by side, both bowing their head strips a few degrees',
}


# ⭐ VÒNG 2 (user: *"tao thấy nó còn vô tri hơn. Thêm các số liệu, biểu đồ, nhân vật vào"*).
# 🔴 Vòng 1 sửa đúng bệnh (hình không chở ý) nhưng CHỮA QUÁ TAY: bỏ sạch người và — vì GUARD
#    cũ cấm mọi chữ/số — còn lại mấy mảnh giấy trần. Đo bản vox-director đã ra `final.mp4`:
#    **33% cảnh có NGƯỜI** và con số nằm NGAY TRONG HÌNH (lịch bóc từ 2020 về 1900, số cắt
#    từ giấy mustard). Tức tao đã tự khoá mất cú đắt nhất của chính ngôn ngữ này.
# ⇒ Ba thứ thêm vào mỗi cảnh: ① NGƯỜI cắt từ giấy ảnh (nhân vật, không phải hình que)
#    ② CON SỐ to cắt từ giấy màu ③ BIỂU ĐỒ giấy (cột/đường/kim) khi cảnh có so sánh.
# ⚖️ YMYL: mọi con số đều lấy TỪ CHÍNH LỜI ĐỌC của cảnh đó — 0円 · 4年 · 3か月 · 10年 · 2か月.


V2 = {0: 'VIZ: an elderly Japanese woman cut from grainy black-and-white photographic paper sits on the right holding an open bank passbook whose entry column is torn away and bare; filling the left half a huge bold numeral 0 cut from deep red card is pasted flat on the newsprint, a taped paper arrow running from the empty column into it', 1: 'CROWD: a public counter built from flat paper panels, a clerk cut from photographic paper sliding a plain document across it to an elderly woman cut-out, and above them a big numeral 4 cut from mustard card with four small torn calendar sheets fanned beneath it', 5: 'META: an elderly man cut from photographic paper stands at the left pushing a paper envelope into the slot of a flat machine built from layered card; behind the slot a row of cut-out paper gears has begun to turn and a taped arrow curves from the envelope to the gears', 8: 'DESK: an elderly Japanese researcher cut from photographic paper sits behind a paper desk seen flat-on, a magnifier and a folded ruler and a stack of plain documents cut from card spread in front of him, and pinned on the flat wall behind him a small paper bar chart of three rising bars', 10: 'HOLD: an elderly woman cut from photographic paper holds a large cream envelope square-on to the camera, and beside her head a big numeral 3 cut from charcoal card sits above three torn calendar sheets laid in a row', 15: 'SPLIT: an elderly man cut from photographic paper stands between two paper boxes — the left one crammed with blank record cards, the right one completely empty — one paper hand pointing at the empty box, the bare newsprint gap between them crossed by nothing at all', 32: 'an elderly man cut from grainy photographic paper with his shoulder strips dropped and his head lowered, and behind him a paper bar chart whose single bar stops well short of a dashed tape line marked by a big numeral 10 cut from charcoal card', 65: 'VIZ: an elderly woman cut from photographic paper on the left looking at a paper calendar strip running across the frame, its last two squares ringed in torn red paper, and a big numeral 2 cut from red card pasted above those two squares', 73: 'GAUGE: an elderly man cut from photographic paper stands beside a large semicircular gauge dial cut from card, its needle resting flat in the middle of the arc and staying there, and a flat line of taped string runs level across the dial face from left to right', 75: 'SPLIT: two paper bar charts side by side with an elderly man cut from photographic paper standing between them — on the left the bars climb step by step, on the right every bar is the same height in a dead flat row, and a pair of card scissors closes on the far end of the flat row'}

NEW.update(V2)

# ⭐ VÒNG 3 — áp công thức đã duyệt ở LOT1 cho 78 cảnh còn lại.
from _collage_full23 import SCENES_V3
NEW.update(SCENES_V3)


def main():
    src = io.open(P, encoding="utf-8").read()
    # 🔴 CHỈ backup LẦN ĐẦU. Bản trước ghi đè mỗi lượt chạy ⇒ sau vòng thứ hai cái gọi là
    #    "backup" chính là bản đã vá, và phép so trước/sau trả về hai dòng giống hệt nhau.
    #    Backup mà bị ghi đè thì không còn là backup — nó chỉ là bản sao của hiện tại.
    import os as _os
    if not _os.path.exists(P + ".bak_photoreal"):
        shutil.copyfile(P, P + ".bak_photoreal")
    out, n = [], 0
    # dò từng dòng của bảng SCENES: `(<idx>, A, "telop", "body"),`
    idx_art = -1
    for line in src.splitlines(True):
        m = re.match(r'(\s*\(\d+,\s+A,\s+"[^"]*",\s+)"(.*)"\),\s*$', line)
        if m:
            idx_art += 1
        # chỉ số scene = vị trí trong SCENES, phải đếm CẢ dòng không phải art
        out.append(line)
    # đếm lại cho chắc: dùng chính module
    sys.path.insert(0, r"E:\Claude\Projects\youtube-jp-nenkin\tools")
    from _scenes23 import SCENES
    body_of = {k: b for k, (l, ki, t, b) in enumerate(SCENES) if ki == "art"}
    miss = [k for k in NEW if k not in body_of]
    if miss:
        print(f"🔴 {len(miss)} khoá không phải scene art: {miss}"); sys.exit(1)
    todo = [k for k in body_of if k not in NEW]
    # --only 0,1,2 : chỉ vá một lô (user duyệt LOT1 trước rồi mới vá hết)
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = {int(x) for x in a.split("=", 1)[1].split(",")}
    if only is None and todo:
        print(f"🔴 CÒN {len(todo)} scene art CHƯA viết lại: {todo}"); sys.exit(1)

    for k, new in list(NEW.items()):
        if only is not None and k not in only:
            continue
        old = body_of[k]
        # thay đúng chuỗi body, có bọc ngoặc kép — old là duy nhất trong file?
        cnt = src.count('"' + old + '"')
        if cnt != 1:
            print(f'🔴 scene {k}: chuỗi cũ xuất hiện {cnt} lần, không thay an toàn được')
            sys.exit(1)
        src = src.replace('"' + old + '"', '"' + new + '"', 1)
        n += 1
    io.open(P, "w", encoding="utf-8").write(src)
    print(f"✅ viết lại {n}/{len(body_of)} mô tả cảnh sang ngôn ngữ collage")
    print(f"   backup: {P}.bak_photoreal")


if __name__ == "__main__":
    main()
