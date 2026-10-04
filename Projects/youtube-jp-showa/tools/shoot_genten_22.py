# -*- coding: utf-8 -*-
r"""shoot_genten_22.py - chup anh 原典 THAT cho video 22 (kieta-shigoto).

Khac v21 (chup ca trang roi do toa do khung do BANG MAT): o day Playwright + chrome-headless-shell cua Remotion
mo trang that, TIM cau trich trong DOM (Range.getBoundingClientRect), chup mot vung quanh cau do o scale 2,
va ghi toa do cau (theo anh chup) vao genten_raw/boxes.json -> make_genten_22.py ve khung do dung cho.
Cau khong tim thay = FAIL, khong bia: doi substring ngan hon hoac bo the do.
CHAY: python tools/shoot_genten_22.py [key ...]
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

GT = Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\22_kieta-shigoto\genten_raw")
CHS = (r"E:\Claude\Projects\remotion-vox\node_modules\.remotion\chrome-headless-shell"
       r"\win64\chrome-headless-shell-win64\chrome-headless-shell.exe")
K = "https://kokkai.ndl.go.jp/txt/"
# key: (url, [cau trich — moi phan tu la danh sach ung vien, thu lan luot])
PAGES = {
 "k1959":    (K + "103313830X00619591126/69", [["八千人おります踏切警手"], ["五十円という五段階", "四十円、五十円"]]),
 "k1964":    (K + "104604748X00419640327/43", [["九千円くらいだと思います", "九千円くらい"]]),
 "k1966":    (K + "105104720X03619660527/80", [["十九・七歳", "十九・七"], ["一万八千九百四十八円"]]),
 "k1966b":   (K + "105113830X01619660331/69", [["約千八百名", "千八百名"], ["二千八百"]]),
 "kisoku15": (K + "105213830X00219661011/9",  [["車掌を乗務する必要がある"], ["車掌の乗務を省略してもいい", "省略してもいい"]]),
 "k1971":    (K + "106515266X00119710323/12", [["約八百円", "八百円"]]),
 "k1972":    (K + "106804816X01219720508/60", [["三十九年の七月から施行", "三十九年の七月"], ["首切りをするということはしない", "首切り"]]),
 "k1976":    (K + "107714889X00219760812/317", [["合計五百四十人", "五百四十人"], ["あとタイピスト", "タイピスト"]]),
 "k1980":    (K + "109104816X00119800305/6",  [["全国自動即時化"], ["ほぼ達成"]]),
 "k1981":    (K + "109404199X00519810320/178", [["三十年以上", "無事故で三十年"], ["約六百名"]]),
 "k1985":    (K + "110214410X02019850523/144", [["和文タイピストの場合十五万八千五百円", "十五万八千五百円"]]),
 "sekitan":  (K + "104804589X01219650324/33", [["石炭鉱業合理化臨時措置法（昭和三十年法律第百五十六号）", "昭和三十年法律第百五十六号"]]),
 "roki63":   ("https://laws.e-gov.go.jp/law/322AC0000000049", [["満十八才に満たない者を坑内で労働させてはならない", "満十八才に満たない者を坑内で"]]),
}
FIND_JS = r"""
(needle) => {
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = w.nextNode())) {
    const t = n.nodeValue; const i = t.indexOf(needle);
    if (i >= 0) {
      const r = document.createRange(); r.setStart(n, i); r.setEnd(n, i + needle.length);
      n.parentElement.scrollIntoView({block: 'center'});
      const rects = [...r.getClientRects()].map(q => [q.left, q.top, q.right, q.bottom]);
      return rects;
    }
  }
  return null;
}
"""


def main(keys):
    GT.mkdir(parents=True, exist_ok=True)
    bp = GT / "boxes.json"
    boxes = json.loads(bp.read_text(encoding="utf-8")) if bp.exists() else {}
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=CHS, args=["--no-sandbox"])
        pg = br.new_page(viewport={"width": 1100, "height": 1300}, device_scale_factor=2)
        for key in keys:
            url, quotes = PAGES[key]
            try:
                pg.goto(url, wait_until="networkidle", timeout=90000)
            except Exception as e:
                print("FAIL load", key, e); continue
            pg.wait_for_timeout(2500)
            found = []
            for cands in quotes:
                hit = None
                for q in cands:
                    r = pg.evaluate(FIND_JS, q)
                    if r: hit = (q, r); break
                if not hit:
                    print("FAIL  %-9s khong thay: %s" % (key, cands)); continue
                found.append(hit)
            if not found: continue
            # sau scrollIntoView cua cau cuoi, do lai rect cua TAT CA cau trong cung viewport
            rects = []
            for q, _ in found:
                rects += [(q, rr) for rr in pg.evaluate(FIND_JS.replace("n.parentElement.scrollIntoView({block: 'center'});", ""), q)]
            ys = [rr[1] for _, rr in rects] + [rr[3] for _, rr in rects]
            top = max(0, min(ys) - 140); bot = min(1300, max(ys) + 140)
            X0 = 255 if "e-gov" in url else 315          # bo cot muc luc ben trai -> chu to hon
            clip = {"x": X0, "y": top, "width": 1100 - X0, "height": bot - top}
            out = GT / (key + ".png")
            pg.screenshot(path=str(out), clip=clip)
            boxes[key] = {"url": url, "quotes": [q for q, _ in found],
                          "rects": [[(rr[0] - X0) * 2, (rr[1] - top) * 2, (rr[2] - X0) * 2, (rr[3] - top) * 2] for _, rr in rects]}
            print("OK    %-9s %s" % (key, " | ".join(q for q, _ in found)))
        br.close()
    bp.write_text(json.dumps(boxes, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:] or list(PAGES))
