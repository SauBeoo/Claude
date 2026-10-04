# -*- coding: utf-8 -*-
"""fetch_real_video_01.py — tim CLIP THAT (Pexels, free thuong mai) cho cac canh HOP chen video that vao ban minh hoa.

Chi chon canh KHONG can khuon mat nhan vat (do vat · khong khi · phong canh · dam dong nhin xa) — canh co Kieko/gia dinh
giu tranh 絵本 (video that = nguoi la, gay vo nhan vat). Moi canh 3 ung vien, tai THUMB de duyet, chua tai ban goc.
⛔ bo id Pexels da len song o video khac (so den _media_library, media-library.md §2).
Xuat 06_VIDEO/<stem>/_cand_video/: NN_cK.jpg + cand.json + sheet.png.
Chay: python tools/fetch_real_video_01.py 01_kuchiguse-hitonome
"""
import sys, io, json, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, r"E:\Claude\Projects\_media_library")
import media_lib as ML  # noqa: E402
KEY = Path(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key").read_text().strip()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# slide -> (cau dang doc ngan, query Pexels)
Q = {
    5: ("見張り番が、今も働いている", "japanese paper lantern night"),
    16: ("感謝の手紙を書いた人は", "writing letter fountain pen"),
    17: ("危ないほうに、多めに見積もる", "shadow on shoji paper screen"),
    23: ("もっと大勢の、名前も知らない人", "tokyo crosswalk crowd"),
    26: ("新しい眼鏡にした日は", "eyeglasses on table"),
    27: ("コーネル大学", "university hallway students walking"),
    76: ("一つずつ、ふたをしていく", "cardboard boxes shelf light"),
    79: ("一年かけて、手放していきました", "japanese village path"),
    94: ("お雑煮を温めなおして", "japanese soup steam bowl"),
    105: ("みかんを三つ食べて", "mandarin orange peel table"),
    106: ("見張り番は、あなたの敵ではありません", "sunrise through window curtain"),
    110: ("コメントで、そっと教えてください", "green tea steam cup window"),
}


def api(url):
    req = urllib.request.Request(url, headers={**UA, "Authorization": KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def dl(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    stem = sys.argv[1]
    cd = PROJ / "06_VIDEO" / stem / "_cand_video"; cd.mkdir(exist_ok=True)
    idx = ML.load_index()
    black = {str(e.get("source_id")) for e in idx.values() if e.get("source") == "pexels" and e.get("used_in")}
    cand, taken = {}, set()
    for sl, (line, q) in Q.items():
        r = api("https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
            {"query": q, "per_page": 15, "orientation": "landscape", "size": "medium"}))
        items = []
        for v in r.get("videos", []):
            files = [f for f in v["video_files"] if (f.get("width") or 0) >= 1280]
            if not files or v["duration"] < 6 or v["id"] in taken or str(v["id"]) in black:
                continue
            k = len(items)
            try:
                dl(v["image"], cd / f"{sl:03d}_c{k}.jpg")
            except Exception as ex:
                print("  tai loi", v["id"], ex); continue
            items.append({"id": v["id"], "url": v["url"], "dur": v["duration"], "user": v["user"]["name"],
                          "file": max(files, key=lambda f: f["width"] if f["width"] <= 1920 else 0)["link"]})
            taken.add(v["id"])
            if len(items) == 3:
                break
        cand[sl] = {"line": line, "q": q, "items": items}
        print(f"slide {sl:3d} {q!r}: {len(items)} ung vien")
        time.sleep(0.4)
    json.dump(cand, open(cd / "cand.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    f = ImageFont.truetype("C:/Windows/Fonts/YuGothB.ttc", 20)
    TW, TH, LW = 360, 203, 380
    keys = [k for k in cand if cand[k]["items"]]
    im = Image.new("RGB", (LW + 3 * TW + 20, len(keys) * (TH + 10) + 10), (30, 30, 30)); d = ImageDraw.Draw(im)
    for r, k in enumerate(keys):
        y = 10 + r * (TH + 10)
        d.text((10, y), f"#{k} {cand[k]['q']}", font=f, fill=(255, 220, 120))
        d.text((10, y + 30), cand[k]["line"], font=f, fill=(235, 235, 235))
        for c in range(len(cand[k]["items"])):
            t = Image.open(cd / f"{k:03d}_c{c}.jpg").convert("RGB"); t.thumbnail((TW - 10, TH))
            im.paste(t, (LW + c * TW, y)); d.text((LW + c * TW + 6, y + 4), f"c{c}", font=f, fill=(255, 80, 80))
    im.save(cd / "sheet.png")
    print("->", cd / "sheet.png")


if __name__ == "__main__":
    main()
