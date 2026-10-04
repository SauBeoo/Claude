# -*- coding: utf-8 -*-
"""BAN 4: sinh 01_kyushoku_SLIDES.json (59 entry) + ghep anh vao slides_img/
+ grade vintage RIENG anh that (anh gen da co tong phim tu prompt).
Kiem: moi match phai la substring cua 1 dong TTS (da strip tag)."""
import json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = r"E:\Claude\Projects\youtube-jp-showa"
GEN = os.path.join(ROOT, "06_VIDEO", "01_kyushoku_v2", "gen")
PHOTO = os.path.join(ROOT, "06_VIDEO", "_asset_test")
DST = os.path.join(ROOT, "06_VIDEO", "01_kyushoku", "slides_img")
TTS = os.path.join(ROOT, "03_SCRIPTS", "01_kyushoku_TTS.md")
OUT = os.path.join(ROOT, "03_SCRIPTS", "01_kyushoku_SLIDES.json")

# (match, source) — source: ("gen","G01") | ("photo", file, crop|None) | ("drawn", spec) | ("pd",)
E = []
# "photo": True = anh FULL man hinh (thieu -> renderer nhet anh vao card navy,
# bug bat duoc 2026-08-07 khi duyet frame ban render dau)
def g(m, code): E.append({"match": m, "photo": True, "_src": ("gen", code)})
def p(m, f, crop=None): E.append({"match": m, "photo": True, "_src": ("photo", f, crop)})
def d(m, spec): E.append({"match": m, "drawn": spec, "_src": ("drawn",)})
def pd(m): E.append({"match": m, "video": True, "_src": ("pd",)})

g("この揚げパン、覚えていますか", "G01")
p("きなこの粉で、口のまわりを", "agepan_orig.jpg")
g("あなたが、小学生だった頃の", "G03")
d("ルールは、ひとつだけ", {"layout": "card", "paper": "kraft", "title": "きょうのルール",
   "lines": ["おぼえていたら 1点", "全部で 10点満点"], "highlight": [0]})
d("あの給食、ひと月いくらだったか", {"layout": "card", "paper": "kraft", "title": "昭和の給食費",
   "lines": ["ひと月\u3000？円"], "highlight": [0]})
g("さて、一品目は、その揚げパンから", "G06")
g("生まれたのは、昭和27年ごろ", "G07")
d("東京、大田区の嶺町小学校", {"layout": "card", "paper": "kraft", "title": "あげパンの誕生",
   "lines": ["昭和27年ごろ・東京 大田区", "お休みの子への思いやりから"], "highlight": [0]})
g("じつは私、大人になってから", "G09")
g("廊下の向こうから、あの匂い", "G10")
d("黒板の横には、わら半紙の献立表", {"layout": "table", "paper": "kraft", "title": "こんだて表",
   "rows": [["月", "コッペパン・シチュー"], ["火", "あげパン・牛乳"], ["水", "ソフトめん・カレー"],
            ["木", "くじらの竜田揚げ"], ["金", "コッペパン・おでん"]], "circle": 1})
g("二品目は、毎日の主役", "G12")
pd("戦後、海の向こうから届いた小麦粉")
g("その銀紙を、最後まで小さく折りたたむ", "G14")
p("食べきれなかったパンは", "koppepan_0.jpg")
g("そう、その週の給食当番です", "G16")
g("じつは私、シチューの食缶を", "G17")
g("まず、忘れられないのが、脱脂粉乳", "G18")
p("やがて教室には、瓶の牛乳が", "bin_gyunyu_0.jpg")
d("配達の牛乳が、1本25円", {"layout": "table", "paper": "kraft", "title": "牛乳のねだん",
   "rows": [["配達の牛乳（1本）", "25円"]], "circle": 0, "note": "※昭和45年・東京\u3000統計局の記録より"})
g("だるまストーブのそばに", "G21")
g("針で、そっと外して", "G22")
g("地域によっては、牛乳は瓶ではなく", "G23")
g("ストローの袋を、ぷっと飛ばして", "G24")
p("牛乳の救世主、ミルメークです", "milmake_0.jpg")
d("昭和42年、名古屋の会社から", {"layout": "card", "paper": "kraft", "title": "ミルメーク",
   "lines": ["昭和42年・名古屋うまれ", "牛乳が、ごほうびに変わる"], "highlight": [0]})
g("コーヒー牛乳色に変わっていく", "G27")
g("机をガタガタと動かして", "G28")
g("お昼の放送が流れていました", "G29")
g("そして机の上には、お母さんが縫ってくれた", "G30")
p("鯨の竜田揚げです", "kujira_orig.jpg", (0.48, 0.40, 0.92, 0.92))
g("しょうが醤油の下味に", "G32")
d("昭和35年、鯨のお肉は", {"layout": "table", "paper": "kraft", "title": "くじらのお肉",
   "rows": [["1キロ", "134円"], ["牛肉とくらべると", "4分の1"]], "circle": 1,
   "anim": True, "dur": 14, "cps": 6, "note": "※昭和35年\u3000旧総理府統計局の記録より"})
d("牛肉より、鯨のほうが多かった", {"layout": "table", "paper": "kraft", "title": "1年間に食べたお肉（ひとり）",
   "rows": [["くじら", "1.6キロ"], ["牛肉", "1.5キロ"]], "circle": 0,
   "note": "※昭和35年\u3000農水省 食料需給表より"})
p("七品目は、袋に入った、あのソフト麺", "softmen_0.jpg")
p("カレーシチューに、ひと切れずつ", "curry_0.jpg", (0.12, 0.12, 0.88, 0.88))
d("ご飯の給食が正式に始まったのは", {"layout": "flow", "paper": "kraft", "title": "給食の主食",
   "lines": ["パンの時代", "ごはん給食\u3000昭和51年〜"]})
p("グリンピースが苦手で", "peas_0.jpg")
d("最初の質問の答え合わせです", {"layout": "card", "paper": "kraft", "title": "昭和の給食費",
   "lines": ["ひと月\u3000？円"], "highlight": [0]})
d("小学校低学年の給食費は", {"layout": "table", "paper": "kraft", "title": "昭和42年の給食費",
   "rows": [["ひと月", "700円"], ["一食あたり", "約35円"]], "circle": 0,
   "anim": True, "dur": 16, "cps": 6, "note": "※東京・府中市の記録より"})
d("さっきの牛乳を、思い出してください", {"layout": "table", "paper": "kraft", "title": "35円で、なにが買えた？",
   "rows": [["牛乳（配達・1本）", "約21円"], ["給食\u3000一食", "35円"], ["牛肉ロース 100g", "202円"]],
   "circle": 2, "anim": True, "dur": 18, "cps": 6, "note": "※昭和42年・東京\u3000統計局の記録より"})
d("そして、翌年の大卒の初任給が", {"layout": "table", "paper": "kraft", "title": "お給料とくらべると",
   "rows": [["大卒の初任給", "30,600円"], ["給食費", "700円"], ["割合", "約40分の1"]],
   "circle": 2, "anim": True, "dur": 16, "cps": 6, "note": "※初任給は昭和43年・賃金構造基本統計"})
g("ここで、ひとつだけお願いです", "G43")
g("八品目、冷凍みかん", "G44")
p("プールの授業のあとの日は", "pool_0.jpg")
p("月に一度のお楽しみ、フルーツポンチ", "fruitponchi_0.jpg")
g("先割れスプーン、あの一本で", "G47")
p("そして、アルマイトの食器", "almite_0.jpg")
g("三角食べ、なんて言葉も", "G49")
g("揚げパンがひとつ余った日の", "G50")
g("最後のひとつ、じゃんけんな", "G51")
g("そういえば、風邪で学校を休んだ日", "G52")
g("大きな釜で溶かした、あの匂い", "G53")
pd("ララ物資に、ユニセフ")
d("そして、時代は流れて、昭和50年", {"layout": "table", "paper": "kraft", "title": "給食費のあゆみ",
   "rows": [["昭和42年", "700円"], ["昭和50年", "1,900円"], ["", "約2.7倍に"]], "circle": 1,
   "anim": True, "dur": 16, "cps": 6, "note": "※東京・府中市の記録より"})
g("昼休みの校庭へ、みんな駆け出して", "G55")
d("さあ、10点満点", {"layout": "card", "paper": "kraft", "title": "10点満点",
   "lines": ["あなたは何点でしたか？", "コメントで教えてください"], "highlight": [0]})
g("お母さんが縫ってくれた給食袋は、もう", "G57")
d("昭和くらし図鑑、今日はこのページまで", {"layout": "card", "paper": "kraft", "title": "昭和くらし図鑑",
   "lines": ["今日は、このページまで", "また、次のページで"], "title_double": True})


def main():
    # 1) verify match vs TTS
    tag = re.compile(r"^(\[[^\[\]]+\])+")
    lines = [tag.sub("", l.strip()) for l in open(TTS, encoding="utf-8") if l.strip()]
    bad = [e["match"] for e in E if not any(e["match"] in l for l in lines)]
    if bad:
        print("🔴 MATCH KHONG KHOP TTS:")
        for b in bad:
            print("  -", b)
        sys.exit(1)
    print(f"match OK: {len(E)}/59 khop TTS")

    # 2) ghep anh
    from PIL import Image
    from grade_vintage import grade
    os.makedirs(DST, exist_ok=True)
    n_g = n_p = 0
    for i, e in enumerate(E):
        src = e.pop("_src")
        if src[0] == "gen":
            shutil.copyfile(os.path.join(GEN, f"gen_{src[1]}.jpg"),
                            os.path.join(DST, f"slide_{i:02d}.jpg"))
            n_g += 1
        elif src[0] == "photo":
            im = Image.open(os.path.join(PHOTO, src[1])).convert("RGB")
            if src[2]:
                w, h = im.size
                x1, y1, x2, y2 = src[2]
                im = im.crop((int(w*x1), int(h*y1), int(w*x2), int(h*y2)))
            dst = os.path.join(DST, f"slide_{i:02d}.jpg")
            im.save(dst, quality=95)
            grade(dst)  # anh that -> keo ve tong phim
            n_p += 1
    print(f"anh: {n_g} gen + {n_p} photo (da grade) -> slides_img/")

    # 3) xuat JSON
    json.dump(E, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"SLIDES v2: {len(E)} entry -> {OUT}")
    drawn = sum(1 for e in E if "drawn" in e)
    vid = sum(1 for e in E if e.get("video"))
    print(f"  gen {n_g} · photo {n_p} · drawn {drawn} · pd-clip {vid}")


if __name__ == "__main__":
    main()
