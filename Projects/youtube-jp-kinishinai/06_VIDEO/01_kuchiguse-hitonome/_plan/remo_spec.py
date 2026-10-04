# -*- coding: utf-8 -*-
"""Noi dung lop Remotion — kinishinai bai 1 (build: tools/build_remotion_01.py).

CHAPTERS : (cau mo chuong, nhan, tieu de) — chip goc tren-trai tu het the chuong toi chuong sau.
CALLOUT  : (tien to cau, tu khoa trong cau -> moc hien, chu hien) — <= 1 o / slide anh, 3,5-4,5s.
           Chu = TOM Y, KHONG chep nguyen phu de (mau ku8qF5wrFxg). Vi tri do builder tu chon (cho trong nhat).
SOURCE   : (tien to cau, chu) — hien tu dau cau toi het slide.
STAT     : (tien to cau, noi dung kin-stat, [tu khoa: dong tren, TRUOC, SAU, dong duoi]).
"""

CHAPTERS = [
    ("その一。「すみません」", "その一", "「すみません」"),
    ("その二。「どう思われるかしら」", "その二", "「どう思われるかしら」"),
    ("その三。「みんな、そうしてるから」", "その三", "「みんな、そうしてるから」"),
    ("その四。「つまらない話で", "その四", "「つまらない話で、ごめんなさいね」"),
    ("その五。「こんなこと言ったら", "その五", "「こんなこと言ったら、恥ずかしい」"),
    ("その六。「いい年して」", "その六", "「いい年して」"),
    ("その七。「私さえ、我慢すれば」", "その七", "「私さえ、我慢すれば」"),
]

CALLOUT = [
    ("見張り番は、こうささやいています", "相手に", "見張り番の声：\n「迷惑をかけた」"),
    ("私が立っていたのは", "呉服売り場", "呉服売り場で\n三十四年"),
    ("いまでも、いただき物の包装紙", "包装紙", "包装紙まで\nていねいに"),
    ("売り場では、お客さまより先に", "先に", "お客さまより\n先に頭を下げる"),
    ("アメリカの研究では、感謝の手紙", "小さく", "相手の喜びは\n思うより大きい"),
    ("見張り番は、いつも、危ないほうに", "多めに", "見張り番は\n心配性"),
    ("このままだと、謝られた相手は", "親切が", "謝られると\n親切が止まる"),
]

SOURCE = [
    ("アメリカの研究では、感謝の手紙", "出典：Kumar & Epley (2018) Psychological Science"),
    ("アメリカの、グラントとジーノ", "出典：Grant & Gino (2010) Journal of Personality and Social Psychology"),
]

STAT = [
    ("アメリカの、グラントとジーノ", "「ありがとう」のひとことで\n約3割|約6割\n次も手伝ってくれた人",
     ["", "手伝って", "六割", "手伝って"]),   # tren: vao the · 約3割 + dong duoi: 「手伝って」 · mui ten + 約6割: 「六割」 (tranh giua the trong 8s)
]
