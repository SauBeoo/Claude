# -*- coding: utf-8 -*-
"""credits_from_plan.py — dung khoi credit 概要欄 tu clips/_PLAN.json cua BAN RENDER CUOI x real_<NN>/MANIFEST.json.

    python tools/credits_from_plan.py <slug>

Vi sao: ATTRIBUTIONS_*.md viet tay/theo mot ban render truoc se lech khi dung lai o (video 20: hook v3 doi o sau
khi ATTRIBUTIONS viet). Credit la loi khai nguon goc (youtube-upload-seo.md §5.1) -> doc tu PLAN cua ban dang dang.
In ra: ① dem theo license (kiem tra) ② khoi credit tieng Nhat dan thang vao 概要欄 ③ ma nao KHONG tim thay license.
"""
import html
import json
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VD = Path(r"E:/Claude/Projects/youtube-jp-showa/06_VIDEO") / sys.argv[1]
nn = sys.argv[1].split("_")[0]
PLAN = json.loads((VD / "clips" / "_PLAN.json").read_text(encoding="utf-8"))
MAN = json.loads((VD / f"real_{nn}" / "MANIFEST.json").read_text(encoding="utf-8"))


# Truong author cua MANIFEST hong o vai file (HTML cat cut, "Own work", %u-escape) -> tra Commons API
# (extmetadata Artist + user upload) roi ghi de theo TEN FILE o day. Them dong moi khi tool in ra ten rac.
OVERRIDE = {
    "Old_cash_register": "TANAKA Juuyoh（田中十洋）",
    "Head_of_1_yen_coin": "Yappakoredesho", "Tail_of_1_yen_coin": "Yappakoredesho",
    "Furoshiki_designed_by_Friedensreich_Hundertwasser": "W.（写真）",
    "Old_Haifukiya_Pharmacy_Building": "Jkr2255", "Kawaramachi_danchi": "Jkr2255",
    "Hanko,_japanese_seal": "Culture Japon",
    "商店街のシャッター_(30492827175)": "Sandra Vallaure",
    "SONY_Trinitron_(Showa)_at_Namba_Walk": "Mr.ちゅらさん",
    "Geta_footwear": "作者不詳",
    "Setron_TV_Set": "Mycommunitysg",
}


def author_of(m):
    page = m.get("page") or ""
    for k, v in OVERRIDE.items():
        if k in page:
            return v
    return clean_author(m.get("author"))


def clean_author(a):
    a = html.unescape(re.sub(r"<[^>]*>?", "", a or "")).strip()
    a = re.sub(r"\s+", " ", a)
    return a or "作者不詳"


NEED = ("CC BY",)  # CC BY / BY-SA *: credit bat buoc
by_lic = defaultdict(OrderedDict)
count = defaultdict(int)
missing, ai = [], 0
for p in PLAN:
    code = p["code"]
    if code.startswith("AI:") or p["layer"] in ("ai", "aistill"):
        ai += 1
        continue
    m = MAN.get(code)
    if not m:
        missing.append(code)
        continue
    lic = (m.get("license") or "?").strip()
    count[lic] += 1
    a = author_of(m)
    by_lic[lic][a] = by_lic[lic].get(a, 0) + 1

print(f"# o AI: {ai} · o that: {sum(count.values())} · thieu license: {len(missing)} {sorted(set(missing))[:10]}")
for k, v in sorted(count.items(), key=lambda x: -x[1]):
    print(f"#   {k}: {v}")
print()
lines = []
for lic in sorted(by_lic, key=lambda k: (not k.startswith("CC BY"), k)):
    if not lic.startswith(NEED):
        continue
    names = "／".join(by_lic[lic].keys())
    lines.append(f"　{lic} — {names}")
pexels = [lic for lic in by_lic if "pexels" in lic.lower()]
pd = [lic for lic in by_lic if lic.lower().startswith(("public domain", "cc0", "pdm"))]
print("※写真・映像（Wikimedia Commons ほか）：")
print("\n".join(lines))
if pd:
    print("　パブリックドメイン／CC0 — " + "・".join(sorted({a for l in pd for a in by_lic[l]})))
if pexels:
    print("※一部の映像・写真：Pexels（Pexels License）")
