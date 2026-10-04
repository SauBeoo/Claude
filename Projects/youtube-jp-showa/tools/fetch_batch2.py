# -*- coding: utf-8 -*-
"""Fetch dot 2 cho video 01: cac beat con thieu anh. Tai ve _asset_test (duyet mat truoc)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import test_fetch_kyushoku as T

T.ITEMS = [
    ("kitchen",    ["給食センター", "学校給食 調理", "school kitchen cooking pots"], "gian bep truong hoc"),
    ("touban",     ["給食 配膳", "給食当番"], "truc nhat chia com"),
    ("kinchaku",   ["巾着袋", "drawstring pouch fabric"], "tui day rut me khau"),
    ("margarine",  ["マーガリン 給食", "margarine packet", "butter portion packet"], "goi margarine"),
    ("milkpowder", ["脱脂粉乳 粉", "milk powder spoon", "powdered milk"], "sua bot"),
    ("milkcap",    ["牛乳キャップ", "milk bottle paper cap"], "nap giay chai sua"),
    ("stove",      ["だるまストーブ", "potbelly stove classroom", "石炭ストーブ"], "lo suoi daruma"),
    ("curry",      ["カレーシチュー", "curry stew japanese", "school lunch curry"], "curry stew"),
    ("peas",       ["グリーンピース", "green peas bowl"], "dau ha lan"),
    ("pool",       ["学校 プール", "school swimming pool japan"], "be boi truong"),
    ("fruitpunch", ["フルーツポンチ 缶詰", "canned fruit cocktail cherry", "fruit cocktail"], "fruit punch"),
    ("trays",      ["給食 食器 かご", "aluminum trays stacked", "school lunch trays"], "khay xep chong"),
]
T.main()
