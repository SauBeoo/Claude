# -*- coding: utf-8 -*-
"""make_slides_07.py — sinh `07_..._SLIDES.json` từ SPEC theo SỐ DÒNG của `_TTS.md`.

VÌ SAO THEO SỐ DÒNG (không gõ tay `match`):
`video_render.py` FAIL ở phút thứ 2 nếu một `match` không còn là substring của TTS
(`[LỖI] Slide 20: không tìm thấy dòng chứa…`). Gõ tay chuỗi tiếng Nhật vào JSON là
cách chắc chắn nhất để sinh lỗi đó. Ở đây: SPEC trỏ **số dòng**, tool tự lấy text
dòng đó làm `match` (tự nới dài đến khi DUY NHẤT) + tự kiểm khoảng cách entry.

Sửa `.md` → chạy lại `make_tts.py` → chạy lại tool này (số dòng có thể xê dịch:
tool in ra dòng nó bắt được, ĐỌC LẠI trước khi render).

CHẠY:  python tools/make_slides_07.py         (ghi JSON + in bảng kiểm)
       python tools/make_slides_07.py --dry    (chỉ in)

GATE tự kiểm (audience-45plus.md §2): ≤6 lần đổi hình/phút · không entry <6s.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "07_tokubetsu-shikyu-rourei-kosei-nenkin"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"
CH_PER_SEC, GAP_LINE, GAP_PARA = 5.72, 0.45, 1.0

PEN = {"paper": "grid", "lang": "jp-pen"}


def P(q, src=None):
    d = {"photo": True, "q": q}
    if src:
        d["src"] = src
    return d


def C(name):
    return {"photo": True, "cast": name}


def G(label, quote, source):
    """原典 card — KHÔNG mô phỏng ảnh chụp trang web (đó là dựng giả hồ sơ).
    Đây là thẻ TRÍCH DẪN: tên cơ quan + câu trích + mốc thời điểm."""
    return {"photo": True, "genten": {"label": label, "quote": quote, "source": source}}


def D(layout, **kw):
    d = dict(PEN, layout=layout)
    d.update(kw)
    return {"drawn": d}


TABLE_ROWS = [["昭和34年生まれ", "61歳から"], ["昭和36年生まれ", "62歳から"],
              ["昭和38年生まれ", "63歳から"], ["昭和40年生まれ", "64歳から"]]

# ---------------------------------------------------------------- SPEC
# (số dòng trong _TTS.md, spec)  — xem bảng dòng: tools/make_tts.py in ra
SPEC = [
    # ---- cold open ----
    (1, P("plain white blank envelope on a wooden table")),          # ⭐ entry 0 = CHỦ THỂ: tờ 請求書
    (3, C("sato_smile")),
    (6, D("card", title="佐藤さんが受け取った額", lines=["156万円", "5年ぶん、一括で"])),
    (8, D("table", title="この年金がある方", rows=[["女性", "いま60〜68歳"], ["男性", "いま65歳以上"],
                                             ["厚生年金", "1年以上"]])),
    (13, D("flow", title="5年の時効", lines=["権利が発生", "5年経過", "受け取れない"])),
    (14, G("年金の時効", "5年を経過したときは、時効によって消滅します", "日本年金機構「年金の時効」")),
    (16, C("sato_cry")),
    (18, C("prop_tsucho")),
    (20, C("kenkyuin")),
    (22, D("card", title="今日の持ち帰り", lines=["あなたの期限は", "令和何年の何月？"])),
    # ---- 第1章 ----
    (25, D("card", title="特別支給の老齢厚生年金", lines=["65歳より前に", "始まっている年金"])),
    (28, P("old paper wall calendar hanging close up")),
    (31, C("kenkyuin")),
    (33, P("rows of filing cabinets with paper documents")),
    (36, D("card", title="申請主義", lines=["国は知っている", "でも、出すまで払わない"], mark="cross")),
    # ---- 第2章 điều kiện ----
    (39, D("checklist", title="対象になる3つの条件",
           lines=["生年月日が線の内側", "厚生年金に1年以上", "資格期間が10年"])),
    (42, D("table", title="生年月日の線", rows=[["女性", "昭和41年4月1日以前"],
                                          ["男性", "昭和36年4月1日以前"]])),
    (45, C("seniors_work_group")),
    (47, D("card", title="よくある誤解", lines=["20年でも10年でもない", "1年以上で対象"], mark="cross")),
    (49, P("hands folding laundry on a bed")),
    (53, D("table", title="この方は対象", rows=[["厚生年金", "合計8年"], ["資格期間", "10年超", "ok"]])),
    # ---- 第2章 bảng (khoanh đỏ chạy theo dòng đang đọc) ----
    (56, C("kenkyuin_happy")),
    (62, D("table", title="女性・受け取り開始年齢", rows=TABLE_ROWS, anim=True)),
    (67, D("table", title="あいだの年は分かれる", rows=[["4月1日まで", "上の年齢"],
                                              ["4月2日から", "下の年齢"]])),
    (69, D("card", title="昭和41年4月2日以後", lines=["この年金は", "ありません"], mark="cross")),
    (72, D("table", title="男性は5年前にずれる", rows=[["いま65歳以上", "対象"],
                                              ["それより下", "なし", "bad"]])),
    (75, G("受給開始年齢の表", "生年月日に応じて受け取り始める年齢が1歳ずつ引き上げられます",
           "厚生労働省「いっしょに検証！公的年金 50〜60代の皆さんへ」")),
    (81, D("table", title="佐藤さんの場合", rows=[["生まれ", "昭和34年11月"], ["開始年齢", "61歳", "ok"],
                                          ["権利発生", "令和2年11月"]])),
    (85, C("sato_cry")),
    # ---- ⭐ khối 期限 ----
    (88, C("kenkyuin")),
    (89, D("flow", title="期限の出し方", lines=["開始年齢の誕生日", "＋5年", "あなたの期限"], anim=True)),
    (90, D("table", title="佐藤さんの時効カレンダー", rows=[["61歳の誕生日", "令和2年11月"],
                                              ["5年後＝時効", "令和7年11月"],
                                              ["窓口に行った", "令和7年9月", "ok"]], circle=1, anim=True)),
    (93, D("card", title="残っていたのは", lines=["2か月"])),
    (95, D("table", title="昭和36年生まれの方", rows=[["開始", "62歳＝令和5年"],
                                            ["時効", "令和10年", "warn"], ["残り", "およそ2年", "warn"]],
           circle=2)),
    (98, D("checklist", title="いま、やってみてください",
           lines=["何歳から始まるか", "その誕生日は何年か", "＋5年＝期限の月"])),
    # ---- cứu 2 nhóm ----
    (100, P("calendar page with a date circled in red pen")),
    (103, C("kenkyuin_happy")),
    (105, D("card", title="取り逃しの最多は", lines=["対象なのに", "対象外だと思った方"])),
    (107, D("checklist", title="4つの思い込み（後半で潰します）",
            lines=["年金は65歳から", "置けば増える", "期間が短いから", "請求書が届かない"], mark="cross")),
    (110, P("two asian senior women sisters talking at home")),
    (114, P("smartphone lying on a wooden table next to a teacup")),
    # ---- 第3章 計算 ----
    (117, P("close up of printed numbers on a paper statement")),
    (118, D("table", title="佐藤さんの計算", rows=[["報酬比例部分", "月2万7千円"], ["さかのぼり", "58か月"],
                                          ["合計", "156万円", "ok"]], circle=2, anim=True)),
    (121, D("card", title="ご注意", lines=["これは当研究室の試算", "額は一人ひとり違います"])),
    (124, D("card", title="よくある勘違い", lines=["5年待ったから", "増えたのではない"], mark="cross")),
    (127, G("特別支給の手続き", "特別支給の老齢厚生年金には「繰下げ制度」はありません。受給権発生日以降に速やかに請求してください",
            "日本年金機構「特別支給の老齢厚生年金を受給するときの手続き」")),
    (131, D("table", title="待つと何が起きるか", rows=[["増える分", "0円", "bad"],
                                            ["5年を過ぎた分", "消える", "bad"]])),
    # ---- 山田妻 ----
    (134, C("yamada_happy")),
    (138, D("table", title="山田さんの奥様", rows=[["厚生年金", "12年＝144か月"], ["開始", "62歳"],
                                          ["権利発生", "令和5年8月"]])),
    (140, D("table", title="奥様の時効カレンダー", rows=[["権利発生", "令和5年8月"],
                                            ["時効", "令和10年8月", "warn"],
                                            ["残り", "2年", "warn"]], circle=2, anim=True)),
    (143, D("card", title="覚えて帰ってください", lines=["期限内なら", "さかのぼれる"])),
    (145, P("calculator notebook and pen on wooden table")),
    (147, D("table", title="奥様の試算", rows=[["月", "1万4千円"], ["36か月", "×"],
                                       ["合計", "およそ50万円", "ok"]], circle=2, anim=True)),
    # ---- 逆算 + lớp quan điểm ----
    (150, C("kenkyuin")),
    (152, D("table", title="令和10年8月を過ぎたら", rows=[["62歳〜65歳の3年分", "およそ50万円", "bad"],
                                              ["気づく機会", "なし", "bad"]])),
    (154, C("prop_tsucho")),
    (157, D("table", title="2つの損", rows=[["株・詐欺", "分かる損"], ["この年金", "分からない損", "bad"]])),
    (162, D("card", title="分からない損は", lines=["悔しがることすら", "できません"])),
    (164, C("kenkyuin")),
    # ---- クイズ ----
    (168, C("quiz_batsu")),
    (172, C("quiz_batsu")),
    (175, C("quiz_maru")),
    # ---- CTA ----
    (177, C("kenkyuin_happy")),
    (180, P("two teacups on a low table in a japanese room")),
    # ---- 第4章 思い込み ----
    (183, D("checklist", title="ここまでに出たもの", lines=["対象", "期限", "金額"])),
    (185, C("kenkyuin_happy")),
    (187, D("card", title="思い込み ①", lines=["年金は65歳から"], mark="cross")),
    (190, P("stack of mail envelopes in a drawer")),
    (191, C("sato_cry")),
    (193, D("card", title="思い込み ②", lines=["置いておけば増える"], mark="cross")),
    (196, D("table", title="繰下げが使えるか", rows=[["65歳からの年金", "使える", "ok"],
                                           ["この年金", "使えない", "bad"]])),
    (199, D("card", title="当研究室の見方", lines=["制度より", "伝え方の問題"])),
    (201, D("table", title="よく流れる数字", rows=[["ひと月", "0.7％"], ["70歳まで", "42％"]])),
    (205, D("card", title="結果", lines=["熱心な方ほど", "損をする"], mark="cross")),
    (207, D("card", title="思い込み ③", lines=["加入期間が短いから"], mark="cross")),
    (211, D("table", title="小さい額でしょうか", rows=[["月2万円", "×5年"], ["合計", "120万円", "warn"]],
            circle=1, anim=True)),
    (213, D("card", title="思い込み ④", lines=["請求書が届いていない"], mark="cross")),
    (216, P("cardboard moving boxes stacked in an empty room")),
    (219, D("card", title="判断するのは", lines=["封筒ではなく", "生年月日と加入期間"])),
    # ---- 第5章 ----
    (223, C("takahashi_think")),
    (226, D("table", title="高橋さんの奥様", rows=[["生まれ", "昭和41年6月"], ["線から", "2か月あと"],
                                          ["この年金", "なし", "bad"]])),
    (229, D("card", title="代わりに確認", lines=["加給年金", "（前回の研究）"])),
    (232, P("empty office desk with computer and paperwork")),
    (234, D("card", title="順番が逆です", lines=["止まるかもしれないから", "請求しない"], mark="cross")),
    (237, D("table", title="在職で止まる場合", rows=[["止まるのは", "給料が多い月だけ"],
                                           ["請求は", "先に済ませる", "ok"]])),
    # ---- 第6章 ----
    (241, P("japanese pension office reception counter")),
    (243, D("checklist", title="持っていくもの",
            lines=["年金請求書", "通帳かキャッシュカード", "戸籍謄本か住民票"])),
    (246, P("fountain pen resting on blank white paper")),
    (248, C("sato_laugh")),
    (251, D("table", title="かかった時間", rows=[["窓口", "30分"], ["受け取った額", "156万円", "ok"]],
            circle=0, anim=True)),
    # ---- 65歳のはがき ----
    (257, P("postcard in japanese mailbox close up")),
    (259, D("table", title="似ているのに逆", rows=[["65歳より前の封筒", "すぐ出す", "ok"],
                                          ["65歳のときの封筒", "少し考えて"]])),
    # ---- 第7章 3ステップ ----
    (264, D("checklist", title="今日からの3ステップ",
            lines=["表に当てはめて期限を出す", "引き出しと郵便物を見る", "電話を一本かける"])),
    (270, D("flow", title="ステップ①", lines=["開始年齢の誕生日", "＋5年", "紙に書く"], anim=True)),
    (274, P("japanese house mailbox with letters inside")),
    (280, P("old landline telephone on a side table")),
    (284, G("年金の時効", "やむを得ない事情により時効完成前に請求できなかった場合は、書面による申立てにより、基本権を時効消滅させない取扱いをしています",
            "日本年金機構「年金の時効」")),
    (289, P("empty hospital bed in bright room")),
    (292, D("card", title="窓口で言う言葉", lines=["事情を", "申し立てられますか"])),
    # ---- セルフチェック ----
    (294, D("checklist", title="セルフチェック 3問",
            lines=["生年月日は線の内側か", "厚生年金1年以上か", "期限の月が言えるか"])),
    (298, D("card", title="三問目", lines=["あなたの期限は", "令和何年の何月？"])),
    # ---- 研究ノート ----
    (301, D("card", title="今日の研究ノート",
            lines=["65歳より前に始まる年金がある", "女性S41.4.1／男性S36.4.1以前",
                   "待っても増えない（繰下げなし）", "5年で時効・期限内はさかのぼれる",
                   "期限＝開始年齢の誕生日＋5年"])),
    (307, D("card", title="いつつ", lines=["期限＝", "開始年齢の誕生日＋5年"])),
    (309, C("kenkyuin")),
    (313, D("table", title="申請主義の理屈", rows=[["ふつうの年金", "受け取る時期を選べる"],
                                          ["この年金", "選べない（繰下げなし）", "bad"]])),
    (320, D("card", title="当研究室の意見", lines=["年金は、知っている人に", "だけ優しくできています"])),
    (324, P("empty bed with white sheets in morning sunlight")),
    (330, C("sato_laugh")),
    (334, D("card", title="このノートを", lines=["ご家族に", "送ってあげてください"])),
]


def main():
    raw = [l for l in TTS.read_text(encoding="utf-8").split("\n")]
    lines, texts = [], []
    for l in raw:
        if l.strip():
            lines.append(l)
            texts.append(re.sub(r"\[[^\]]*\]", "", l).strip())

    # mốc thời gian từng dòng — ƯỚC từ ký tự (dùng khi chưa render lần nào)
    cum, acc = [], 0.0
    for t in texts:
        acc += len(re.sub(r"\s", "", t)) / CH_PER_SEC + GAP_LINE
        cum.append(acc)
    at = lambda no: (cum[no - 2] if no > 1 else 0.0)

    # 🔴 NGUỒN SỰ THẬT của thời gian là `subs.srt` SAU RENDER, không phải mô hình ký tự.
    # Đo bản render 3: mô hình ước cue THẤP hơn thật 2–15% → 6/9 clip anim ngắn hơn cue
    # → renderer LOOP (bảng bị xoá, viết lại từ đầu). Có srt thì dùng srt.
    srt = PROJ / "06_VIDEO" / STEM / "subs.srt"
    real = []
    if srt.exists():
        for blk in srt.read_text(encoding="utf-8").strip().split("\n\n"):
            ln = blk.split("\n")
            if len(ln) < 3:
                continue
            m = re.match(r"(\d\d):(\d\d):(\d\d),(\d+)", ln[1])
            if m:
                real.append((int(m.group(1)) * 3600 + int(m.group(2)) * 60
                             + int(m.group(3)) + int(m.group(4)) / 1000, "".join(ln[2:])))
        print(f"⏱  dùng subs.srt thật ({len(real)} cue) để tính độ dài clip anim")

    def real_start(txt):
        for t, tx in real:
            if txt[:10] in tx:
                return t
        return None

    out, rows = [], []
    for k, (no, spec) in enumerate(SPEC):
        if not (1 <= no <= len(texts)):
            sys.exit(f"❌ dòng {no} không tồn tại (TTS có {len(texts)} dòng)")
        t = texts[no - 1]
        n = 12
        while n < len(t) and sum(1 for x in texts if t[:n] in x) > 1:
            n += 4
        e = dict(spec)
        e["match"] = t[:min(n, len(t))]
        # ⚠️ CLIP anim PHẢI viết xong TRONG cue. make_drawn mặc định --anim-dur 30s;
        # cue thật ~12–20s → chữ hiện dần chưa tới đáp án thì đã sang slide khác
        # (khoanh đỏ/đáp án KHÔNG BAO GIỜ hiện = mất đúng cái người xem đợi).
        # Nên: dur = 0,8 × cue, và cps đủ nhanh để viết hết trong dur đó.
        if isinstance(e.get("drawn"), dict) and e["drawn"].get("anim"):
            cue = (at(SPEC[k + 1][0]) if k + 1 < len(SPEC) else acc) - at(no)
            d = dict(e["drawn"])
            # 🔴 HAI THỨ KHÁC NHAU, ĐỪNG GỘP (mỗi cái đã tự sinh 1 lỗi phải render lại):
            #   ① `dur` = ĐỘ DÀI CLIP → phải **≥ cue**. Ngắn hơn cue thì video_render
            #      LOOP clip: bảng viết xong rồi bị xoá, viết lại từ đầu ngay giữa lúc
            #      giọng đang đọc dòng 3 (đo được ở frame 5:14 bản render 2).
            #   ② `cps` = NHỊP VIẾT → phải khớp nhịp GIỌNG đọc các dòng, không liên quan
            #      tới độ dài clip. Đo thật từ srt: giọng đọc 1 dòng bảng ≈ 3,9s
            #      (4 dòng 昭和34→40 mất 15,6s), KHÔNG phải 2,8s như tao đoán vòng trước.
            n_items = len(d.get("rows") or d.get("lines") or []) or 1
            nch = sum(len(str(x)) for r in d.get("rows", []) for x in r) + \
                sum(len(str(x)) for x in d.get("lines", []))
            # cue THẬT từ srt nếu có (mô hình ký tự ước thấp → sinh loop)
            if real:
                s0 = real_start(e["match"])
                s1 = real_start(texts[SPEC[k + 1][0] - 1]) if k + 1 < len(SPEC) else None
                if s0 is not None and s1 is not None and s1 > s0:
                    cue = s1 - s0
            d["dur"] = round(cue + 2.0, 1)   # ① clip DÀI hơn cue — bị trim thì không mất gì,
            #                                     ngắn hơn 0,3s thôi là đã loop (đo bản 3)
            t_read = max(3.0, min(cue, n_items * 3.9))           # ② nhịp viết khớp nhịp giọng
            d["cps"] = round(max(2.0, nch / t_read), 1)
            e["drawn"] = d
        out.append(e)
        rows.append((no, t[:30]))

    # ---- kiểm khoảng cách (gate audience-45plus §2) ----
    cum, acc, par = [], 0.0, 0
    for i, t in enumerate(texts):
        acc += len(re.sub(r"\s", "", t)) / CH_PER_SEC + GAP_LINE
        cum.append(acc)
    total = acc + len(re.split(r"\n\s*\n", TTS.read_text(encoding="utf-8").strip())) * GAP_PARA
    marks = [cum[no - 2] if no > 1 else 0.0 for no, _ in SPEC]
    short = []
    for i in range(len(marks) - 1):
        d = marks[i + 1] - marks[i]
        if d < 6.0:
            short.append((SPEC[i][0], SPEC[i + 1][0], round(d, 1)))
    print(f"entry: {len(out)}   video ~{int(total)//60}:{int(total)%60:02d}"
          f"   đổi hình/phút = {len(out)/(total/60):.1f}  (trần 6)")
    from collections import Counter
    kinds = Counter("drawn" if "drawn" in e else "cast" if "cast" in e else
                    "genten" if "genten" in e else "photo" for e in out)
    print("mix:", dict(kinds),
          f"→ drawn {kinds['drawn']*100//len(out)}% · cast {kinds['cast']*100//len(out)}%"
          f" · ảnh {kinds['photo']*100//len(out)}% · 原典 {kinds['genten']}")
    if short:
        print("⚠️ entry < 6s (gộp lại):", short)
    else:
        print("✅ không entry nào <6s")
    dup = [e["match"] for e in out if sum(1 for x in texts if e["match"] in x) > 1]
    if dup:
        print("⚠️ match KHÔNG duy nhất:", dup)
    if "--dry" not in sys.argv:
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print("→ ghi", OUT)


if __name__ == "__main__":
    main()
