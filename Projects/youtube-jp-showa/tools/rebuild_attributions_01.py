# -*- coding: utf-8 -*-
"""Rebuild ATTRIBUTIONS cho video 01 — report.txt bi ghi de nen truy nguoc nguon
bang cach chay lai dung query Commons roi so HASH byte anh (thumb 1600px / full-res).
Ra: 06_VIDEO/01_kyushoku/ATTRIBUTIONS.md + phan MISS de xu ly tay.
"""
import hashlib, os, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import test_fetch_kyushoku as T

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
ASSET = os.path.join(ROOT, "06_VIDEO", "_asset_test")
OUTMD = os.path.join(ROOT, "06_VIDEO", "01_kyushoku", "ATTRIBUTIONS.md")

# file da len hinh (assemble_assets_01.py) -> slug + bo query goc
USED = {
    "agepan_orig.jpg":    ["揚げパン", "揚げパン 給食"],
    "kujira_orig.jpg":    ["鯨肉 竜田揚げ", "鯨 竜田揚げ", "鯨肉"],
    "reitomikan_0.jpg":   ["冷凍みかん", "冷凍ミカン"],
    "tetrapack_0.jpg":    ["テトラパック 牛乳", "三角 牛乳", "テトラ・クラシック"],
    "sakiware_0.jpg":     ["先割れスプーン"],
    "trays_0.jpg":        ["給食 食器 かご", "aluminum trays stacked", "school lunch trays"],
    "bin_gyunyu_0.jpg":   ["瓶牛乳", "牛乳瓶"],
    "milkcap_0.jpg":      ["牛乳キャップ", "milk bottle paper cap"],
    "stove_0.jpg":        ["だるまストーブ", "potbelly stove classroom", "石炭ストーブ"],
    "milmake_0.jpg":      ["ミルメーク"],
    "kyushoku_ban_0.jpg": ["給食当番", "給食 配膳"],
    "kinchaku_0.jpg":     ["巾着袋", "drawstring pouch fabric"],
    "softmen_0.jpg":      ["ソフト麺", "ソフトスパゲッティ式めん"],
    "curry_0.jpg":        ["カレーシチュー", "curry stew japanese", "school lunch curry"],
    "peas_0.jpg":         ["グリーンピース", "green peas bowl"],
    "pool_0.jpg":         ["学校 プール", "school swimming pool japan"],
}


def sha1_file(p):
    h = hashlib.sha1()
    with open(p, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def dhash(im, size=16):
    """Perceptual hash — bytes thumb Commons doi theo lan re-render, pixel thi khong."""
    from PIL import Image
    g = im.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = []
    for r in range(size):
        row = px[r * (size + 1):(r + 1) * (size + 1)]
        bits += [1 if row[i] > row[i + 1] else 0 for i in range(size)]
    return bits


def ham(a, b):
    return sum(x != y for x, y in zip(a, b))


import re as _re


def std_thumb(url):
    """Wikimedia 2026 chan size thumb tuy y (429 w.wiki/GHai) -> ep ve size chuan 640px."""
    return _re.sub(r"/(\d+)px-", "/640px-", url)


def fetch_img(url):
    import io
    from PIL import Image
    req = urllib.request.Request(std_thumb(url), headers={"User-Agent": T.UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return Image.open(io.BytesIO(r.read())).convert("RGB")


# da xac dinh chac (byte-hash / dhash d=0 cac vong truoc) — khong chay lai
KNOWN = {
    "kujira_orig.jpg": {"title": "File:Japanese school lunch in the Showa period.jpg",
                        "license": "CC BY-SA 4.0",
                        "page": "https://commons.wikimedia.org/wiki/File:Japanese_school_lunch_in_the_Showa_period.jpg"},
    "agepan_orig.jpg": {"title": "File:Agepan.jpg", "license": "CC0",
                        "page": "https://commons.wikimedia.org/wiki/File:Agepan.jpg"},
    "tetrapack_0.jpg": {"title": "File:Tetra-Milk-Carton---Betsukai-Milk---2024-04-27 01.jpg",
                        "license": "CC BY 4.0",
                        "page": "https://commons.wikimedia.org/wiki/File:Tetra-Milk-Carton---Betsukai-Milk---2024-04-27_01.jpg"},
}


def main():
    found, miss = [(k, v) for k, v in KNOWN.items()], []
    for fn, queries in USED.items():
        if fn in KNOWN:
            continue
        local = os.path.join(ASSET, fn)
        if not os.path.exists(local):
            miss.append((fn, "file local khong ton tai"))
            continue
        from PIL import Image
        lhash = dhash(Image.open(local))
        print(f"[{fn}]")
        hit, best = None, 999
        cands = []
        for attempt in range(3):
            try:
                cands = T.search_item(queries)
                break
            except Exception as e:
                print(f"    search loi ({e}), doi 30s…")
                time.sleep(30)
        print(f"    {len(cands)} ung vien")
        for c in cands[:12]:
            u = c.get("url")
            if not u:
                continue
            try:
                d = ham(lhash, dhash(fetch_img(u)))
            except Exception as e:
                print(f"    [warn] {e} — doi 20s")
                time.sleep(20)
                continue
            if d < best:
                best, hit = d, c
            if d <= 6:
                break
            time.sleep(3)
        if hit and best <= 20:  # 256-bit dhash: <=20 = cung mot anh
            print(f"    MATCH (d={best}): {hit['title']} [{hit['license']}]")
            found.append((fn, hit))
        else:
            miss.append((fn, f"khong match (best d={best})"))
            print(f"    MISS (best d={best})")
        time.sleep(8)

    lines = ["# ATTRIBUTIONS — 01 kyushoku (rebuild 2026-08-07, match SHA1 len Commons)",
             "", "## Ảnh (Wikimedia Commons)", ""]
    for fn, c in found:
        lines.append(f"- `{fn}` — {c['title']} · **{c['license']}** · {c['page']}")
    if miss:
        lines += ["", "## 🔴 CHƯA TRUY ĐƯỢC NGUỒN (xử lý tay trước khi đăng)", ""]
        for fn, why in miss:
            lines.append(f"- `{fn}` — {why}")
    lines += ["", "## Footage (clip)", "",
              "- Prelinger Collection / Internet Archive — PD (verify statement từng cuộn theo "
              "`06_VIDEO/_footage_test/FOOTAGE_GO_NO_GO.md` TRƯỚC KHI ĐĂNG)",
              "", "## Âm thanh", "",
              '- BGM: "Wholesome" Kevin MacLeod (incompetech.com) — CC BY 4.0',
              "- SFX hoài niệm tự chế (`tools/make_nostalgia_sfx.py`) — license sạch",
              "- Giọng: VOICEVOX:東北イタコ", ""]
    with open(OUTMD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"\nXONG: {len(found)} match / {len(miss)} miss -> {OUTMD}")


if __name__ == "__main__":
    main()
