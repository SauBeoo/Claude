# -*- coding: utf-8 -*-
"""build_slides_11.py — sinh `11_..._SLIDES.json` cho video 11 (定年の順番).

VÌ SAO CÓ TOOL NÀY thay vì viết JSON tay:
`match` phải là substring của MỘT dòng trong `_TTS.md`. Viết tay thì sai chính tả
một chữ là chết cue giữa lượt render (`[LỖI] Slide 20: không tìm thấy dòng chứa…`),
và phát hiện ở phút thứ 2 của render. Tool này **tự kiểm 4 điều trước khi ghi file**:
  ① mỗi `match` khớp ĐÚNG 1 dòng (0 hoặc ≥2 → dừng)
  ② index dòng tăng dần nghiêm ngặt
  ③ khoảng cách dòng giữa 2 thẻ ≥2 (luật `audience-45plus.md` §2: không entry <6s)
  ④ mật độ ≤6 đổi hình/phút

⭐ TRỤC HÌNH của video này: 「出ていくのは早い／戻ってくるのは遅い」 mã hoá bằng layout
`compare` (2 cột) lặp **5 lần** — cold open · 第2章 · 第3章(cột phải RỖNG = khuôn bị phá)
· 第4章 · 第5章. Đổi layout của mấy thẻ đó là phá xương sống thị giác của bài.

CHẠY:  python tools/build_slides_11.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "11_taishokukin-shinkokusho-junban-408man"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"
DUR_SEC = 16 * 60 + 26          # đo bằng make_tts --dry

NL = "\n"
SP = "出ていく／戻ってくる"      # nhãn nội bộ cho thẻ trục


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


CARDS = [
    # ───────────────────────── COLD OPEN (trục lần 1)
    C("あなたの退職金から", "art", title="この紙を1枚、出さなかっただけで",
      img="art_shinkokusho.png", fly="up",
      pins=[["408万4千円", 0.52, 0.46]],
      cap="退職金から、口座に入る前に引かれます",
      left="sensei_serious", right="kikite_surprised"),
    C("しかも、引かれるのは", "big", title="しかも、引かれるのは",
      value="税金ゼロの人", tone="amber", cap="計算上は1円もかからない方から、です",
      left="sensei_caution", right="kikite_worried"),
    C("戻ってはきます", "compare", title="戻ってはきます。ただし——",
      panels=[{"icon": "chart_down", "cap": "出ていくのは"},
              {"icon": "clock", "cap": "戻ってくるのは"}],
      rows=["即日（口座に入る前）", "翌年（自分で確定申告したあと）"],
      left="sensei_explain", right="kikite_think"),
    C("408万円を、1年近く", "check", title="退職後、最初の1年に起きること",
      bgimg="bg_saifu.png",
      no=[["wallet", "408万円が手元にない"],
          ["calendar", "お金の出入りが、いちばん読めない1年"]],
      left="sensei_serious", right="kikite_down"),
    C("定年のときに出す紙は", "big", title="定年のときに出す紙は",
      value="5枚", unit="あります", tone="amber", cap="そして5枚とも、同じ形をしています",
      left="sensei_present", right="kikite_listen"),
    C("1枚だけ、戻ってこないものが", "big", title="1枚だけ、戻ってこないものがあります",
      value="20日", tone="bad", cap="期限は、退職日の翌日から20日",
      left="sensei_caution", right="kikite_surprised"),
    C("こんにちは、年金と", "source", title="今日も、原典を一緒に読みます",
      org="年金と老後のお金研究室",
      doc="国税庁・協会けんぽ・日本年金機構の" + NL + "ページを、画面に出して確かめます",
      note="※出典は概要欄に記載しています",
      left="sensei_conclude", right="kikite_nod"),

    # ───────────────────────── 第1章
    C("千葉の松本さん", "photo", title="モニター・松本さん（千葉）",
      img="photo_matsumoto.png", fly="right",
      cap="60歳。この春、38年勤めた会社を定年で離れました",
      left="sensei_present", right="kikite_listen"),
    C("会社から封筒を渡された", "art", title="退職金の書類、その中の1枚",
      img="art_kaban_shorui.png", fly="up",
      cap="「退職所得の受給に関する申告書」",
      left="sensei_point", right="kikite_think"),
    C("松本さんは、鞄に入れました", "check", title="松本さんがしたこと",
      bgimg="art_kaban_shorui.png",
      no=[["docs", "中身は見た。でも、鞄に入れた"],
          ["house", "そのまま、家に帰った"],
          ["clock", "思い出したのは、翌朝"]],
      left="sensei_serious", right="kikite_worried"),
    C("式は、国税庁が", "art", title="原典：国税庁 No.2732",
      img="genten_01_nta.png", fly="up",
      cap="赤で囲んだところ ＝ 申告書を出していない場合",
      left="sensei_point", right="kikite_think"),
    C("控除の額は、勤めた年数", "compare", title="退職所得控除は、勤めた年数で決まる",
      bgimg="bg_dentaku.png",
      panels=[{"icon": "calendar", "cap": "20年まで"},
              {"icon": "chart_up", "cap": "20年を" + NL + "超えた分"}],
      rows=["1年あたり 40万円", "1年あたり 70万円"],
      left="sensei_explain", right="kikite_listen"),
    C("800万円に、70万円かける", "big", title="松本さん（勤続38年）の控除額",
      value="2060万円", tone="ok", cap="800万円 ＋ 70万円 × 18年",
      left="sensei_present", right="kikite_surprised"),
    C("引き算をすると", "big", title="退職金2000万円 − 控除2060万円",
      value="ゼロ円", tone="ok", cap="課税される退職所得は、ありません",
      left="sensei_reassure", right="kikite_relieved"),
    C("では、出さなかったら", "big", title="出さなかった場合の税率",
      value="20.42", unit="％", tone="bad", cap="支給額そのものに、かかります",
      left="sensei_serious", right="kikite_surprised"),
    C("控除も、2分の1も", "check", title="出さないと、使われないもの",
      bgimg="art_shinkokusho.png",
      no=[["calc", "退職所得控除（2060万円）"],
          ["scale", "2分の1にする計算"]],
      left="sensei_caution", right="kikite_worried"),
    C("408万4千円です", "big", title="2000万円 × 20.42％",
      value="408万4千円", tone="bad", cap="税金ゼロの方から、引かれる額です",
      left="sensei_serious", right="kikite_surprised"),
    C("控除がいちばんよく効いて", "compare", title="なぜ、ゼロの人ほど差が大きいのか",
      panels=[{"icon": "avatar_matsumoto", "cap": "控除がよく" + NL + "効いていた人"},
              {"icon": "avatar_suzuki", "cap": "控除があまり" + NL + "効かない人"}],
      rows=["切り替わったときの落差が大きい", "落差は小さい"],
      left="sensei_explain", right="kikite_think"),
    C("翌朝、思い出して", "timeline", title="松本さんの、一晩",
      **{"from": "渡された日", "to": "翌朝"},
      label="思い出して、経理に持っていった", prog=0.85,
      steps=[["docs", "鞄に" + NL + "入れる"],
             ["house", "そのまま" + NL + "帰宅"],
             ["form", "翌朝、" + NL + "経理へ"]],
      left="sensei_reassure", right="kikite_relieved"),
    C("なお、松本さんは", "check", title="以前の研究の、あの松本さん",
      bgimg="photo_matsumoto.png",
      ok=[["person", "60歳で辞めるか、残るか——残るほうを選んだ"]],
      no=[["docs", "それでも、この紙は必要だった"]],
      left="sensei_explain", right="kikite_nod"),
    C("多くの会社では", "steps", title="多くの会社の、定年のかたち",
      bgimg="bg_dentaku.png",
      steps=[["form", "定年でいったん退職"],
             ["money_pouch", "退職金を受け取る"],
             ["hanko", "再雇用の契約を結ぶ"]],
      left="sensei_explain", right="kikite_listen"),

    # ───────────────────────── 第2章（trục lần 2）
    C("定年のまわりの紙を", "timeline", title="定年のまわりの紙を、時間の順に",
      **{"from": "退職金の前", "to": "65歳の3か月前"},
      label="先に来る期限のほうが短い", prog=0.72,
      steps=[["form", "①申告書" + NL + "退職金前"],
             ["hanko", "②保険" + NL + "20日"],
             ["cityhall", "③年金" + NL + "14日"],
             ["magnifier", "④求職" + NL + "申込前"],
             ["postcard", "⑤請求書" + NL + "3か月前"]],
      left="sensei_present", right="kikite_think"),
    C("先に来る期限のほうが", "big", title="いちばん短い2つが、いちばん前にある",
      value="20日と14日", tone="bad", cap="送別会と、荷物の片づけの時期です",
      left="sensei_caution", right="kikite_worried"),
    C("そして、5枚とも", "compare", title="5枚とも、同じ形をしています",
      panels=[{"icon": "chart_down", "cap": "出ていくのは"},
              {"icon": "clock", "cap": "戻ってくるのは"}],
      rows=["退職金 408万円 ＝ 即日 → 翌年",
            "年金 ＝ 翌月から止まる → 終わって3か月後",
            "健康保険 ＝ 選べるのは20日 → 戻らない"],
      left="sensei_explain", right="kikite_surprised"),
    C("制度が意地悪を", "check", title="なぜ、そうなっているのか",
      bgimg="bg_dentaku.png",
      ok=[["form", "届出を受け取ってから、計算する仕組み"]],
      no=[["clock", "だから、遅れた分だけ、遅れて戻る"]],
      left="sensei_reassure", right="kikite_nod"),
    C("ただ、その「遅れて戻る」", "check", title="その時期に、何をしているか",
      bgimg="bg_hikkoshi.png",
      ok=[["couple", "送別会と、挨拶回り"],
          ["house", "荷物を運ぶ"],
          ["calendar", "少し旅行にでも行こうか"]],
      left="sensei_explain", right="kikite_think"),

    # ───────────────────────── 第3章
    C("名古屋の鈴木さん", "check", title="モニター・鈴木さん（名古屋）",
      bgimg="photo_suzuki.png",
      ok=[["person", "65歳。役員をされていた方"],
          ["house", "この夏、完全に退職"]],
      left="sensei_present", right="kikite_listen"),
    C("鈴木さんは、20日目に", "big", title="鈴木さんが電話をかけた日",
      value="20日目", tone="amber", cap="協会けんぽの支部へ。ぎりぎりでした",
      bgimg="bg_denwa.png",
      left="sensei_point", right="kikite_think"),
    C("同じ会社を、1年前に", "timeline", title="1年前に辞められた、先輩の話",
      **{"from": "退職日", "to": "22日目"},
      label="間に合わなかった", prog=1.0,
      steps=[["env", "封筒は" + NL + "届いていた"],
             ["house", "2週間は" + NL + "片づけと挨拶"],
             ["warning", "気づいたのは" + NL + "22日目"]],
      left="sensei_serious", right="kikite_worried"),
    C("2日です", "big", title="2日、遅れただけで",
      value="2日", tone="bad", cap="選択肢がひとつ、消えました",
      left="sensei_serious", right="kikite_surprised"),
    C("その方は、いま", "compare", title="鈴木さんと、先輩",
      panels=[{"icon": "phone", "cap": "20日目に" + NL + "電話した"},
              {"icon": "warning", "cap": "22日目に" + NL + "気づいた"}],
      rows=["3つから選べた", "国民健康保険だけ"],
      left="sensei_explain", right="kikite_worried"),
    C("でも、比べる機会", "check", title="先輩が失ったもの",
      bgimg="bg_calendar_batsu.png",
      no=[["hanko", "任意継続という選択肢そのもの"],
          ["scale", "3つを比べる機会"],
          ["magnifier", "あとから、どちらが得だったか確かめる方法"]],
      left="sensei_serious", right="kikite_down"),
    C("協会けんぽは、3つ並べて", "art", title="原典：協会けんぽ「任意継続」",
      img="genten_02_kenpo.png", fly="up",
      cap="赤で囲んだところ ＝「比較の上」と「20日以内」",
      left="sensei_point", right="kikite_think"),
    C("「毎月納める保険料などを", "big", title="協会けんぽの言葉",
      value="比較の上", tone="amber", cap="選ぶ前に、3つとも金額を出しておく",
      left="sensei_point", right="kikite_nod"),
    C("この20日を過ぎたら", "check", title="20日を過ぎると、どうなるか",
      bgimg="bg_calendar_batsu.png",
      no=[["warning", "任意継続という選択肢そのものが、なくなる"],
          ["cityhall", "国民健康保険しか、残らない"],
          ["clock", "その状態が、2年続く"]],
      left="sensei_serious", right="kikite_down"),
    C("20日で失って", "compare", title="5枚の中で、これだけが直せません",
      panels=[{"icon": "clock", "cap": "選べるのは"},
              {"icon": "warning", "cap": "戻ってくるのは"}],
      rows=["20日", "——ありません（2年）"],
      left="sensei_serious", right="kikite_surprised"),
    C("しかも20日というのは", "steps", title="その20日に、やること",
      bgimg="bg_shiyakusho.png",
      steps=[["magnifier", "3つの金額を調べる"],
             ["scale", "比べる"],
             ["hanko", "決める"],
             ["form", "書類を出す"]],
      left="sensei_explain", right="kikite_think"),
    C("国民健康保険の保険料は", "check", title="国保の保険料が変わる理由",
      bgimg="bg_shiyakusho.png",
      ok=[["couple", "世帯の人数"],
          ["wallet", "前年の所得"],
          ["cityhall", "お住まいの市区町村"]],
      left="sensei_explain", right="kikite_think"),
    C("任意継続の保険料は", "big", title="任意継続の保険料",
      value="2倍", tone="bad", cap="会社が半分払っていた分が、なくなります",
      left="sensei_serious", right="kikite_surprised"),
    C("でも、任意継続には上限", "big", title="ただし、任意継続には上限があります",
      value="32万円", tone="ok", cap="標準報酬月額が32万円を超えていた場合は、32万円で計算",
      left="sensei_reassure", right="kikite_relieved"),
    C("国民健康保険のほうは", "compare", title="どちらが高く出やすいか",
      panels=[{"icon": "hanko", "cap": "任意継続"},
              {"icon": "cityhall", "cap": "国民健康保険"}],
      rows=["上限がある（32万円）", "前年の所得で決まる"],
      left="sensei_explain", right="kikite_think"),
    C("鈴木さんは役員でしたから", "steps", title="やることは、ひとつです",
      steps=[["calendar", "退職日が決まったら"],
             ["phone", "市区町村の窓口に電話"],
             ["calc", "「国保はいくらになりますか」"]],
      bgimg="bg_shiyakusho.png",
      left="sensei_point", right="kikite_nod"),
    C("松本さんは、この電話を", "compare", title="辞める方と、残る方",
      panels=[{"icon": "avatar_suzuki", "cap": "辞める方"},
              {"icon": "avatar_matsumoto", "cap": "残る方"}],
      rows=["3つから選ぶ（20日）", "会社の健康保険が、そのまま続く"],
      left="sensei_explain", right="kikite_nod"),

    # ───────────────────────── CTA
    C("ここで、ひとつだけお願い", "source", title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    # ───────────────────────── 第4章（trục lần 3）
    C("松本さんは、ハローワークにも", "check", title="松本さんの場合",
      ok=[["person", "働き続けるので、失業給付を受けない"],
          ["clock", "そもそも、まだ年金を受け取っていない"],
          ["magnifier", "だから、ハローワークには行かなかった"]],
      left="sensei_reassure", right="kikite_relieved"),
    C("もし、あなたが", "big", title="ひやりとする方がいます",
      value="65歳より前", unit="から年金を", tone="amber",
      cap="繰上げ受給・特別支給の老齢厚生年金を受け取っている方",
      left="sensei_caution", right="kikite_worried"),
    C("もう一度、機構の", "art", title="原典：日本年金機構「失業給付との調整」",
      img="genten_03_kikou.png", fly="up",
      cap="赤で囲んだところ ＝ 年金が全額支給停止",
      left="sensei_point", right="kikite_think"),
    C("止まり方も", "timeline", title="いつ止まって、いつ戻るのか",
      **{"from": "求職の申込み", "to": "3か月程度後"},
      label="止まるのは翌月、戻るのは3か月後", prog=0.85,
      steps=[["magnifier", "求職の" + NL + "申込み"],
             ["warning", "翌月から" + NL + "全額停止"],
             ["clock", "終わって" + NL + "3か月後"]],
      left="sensei_serious", right="kikite_worried"),
    C("また同じ形ですね", "compare", title="また、同じ形です",
      panels=[{"icon": "chart_down", "cap": "止まるのは"},
              {"icon": "clock", "cap": "戻るのは"}],
      rows=["申込みの、翌月", "終わってから、3か月後"],
      left="sensei_explain", right="kikite_nod"),
    C("ハローワークの窓口に座る前に、年金事務所に一本", "steps", title="順番は、こうです",
      steps=[["phone", "窓口に座る前に年金事務所へ電話"],
             ["magnifier", "そのあとハローワーク"]],
      bgimg="bg_denwa.png",
      left="sensei_point", right="kikite_nod"),
    C("窓口に座ってから聞くのでは", "big", title="座ってから聞くのでは、遅い",
      value="翌月から", tone="bad", cap="申込みをした月の、その翌月から止まります",
      left="sensei_serious", right="kikite_surprised"),

    # ───────────────────────── 第5章（trục lần 4）
    C("会社を辞めて、次にすぐ", "big", title="国民年金の手続き",
      value="14日以内", tone="bad", cap="退職日の翌日から。市区役所か町村役場です",
      left="sensei_caution", right="kikite_listen"),
    C("20日の健康保険と", "compare", title="同じ日に、まとめて行く",
      panels=[{"icon": "hanko", "cap": "健康保険" + NL + "20日"},
              {"icon": "cityhall", "cap": "国民年金" + NL + "14日"}],
      rows=["協会けんぽの支部", "市区町村の窓口"],
      bgimg="bg_shiyakusho.png",
      left="sensei_explain", right="kikite_nod"),
    C("これは、機構が送って", "big", title="年金請求書は、送られてきます",
      value="3か月前", unit="から", tone="ok", cap="受給開始年齢に到達する、3か月前から",
      left="sensei_reassure", right="kikite_relieved"),
    C("中の請求書には", "check", title="届いたら、ここを見てください",
      bgimg="bg_yubin.png",
      ok=[["docs", "年金の加入記録が、印字されています"]],
      no=[["magnifier", "抜けている期間がないか"],
          ["form", "転職の前と後が、つながっているか"]],
      left="sensei_point", right="kikite_think"),
    C("ただし、加入期間が10年", "check", title="事前送付が来ない方もいます",
      bgimg="bg_yubin.png",
      no=[["warning", "加入期間が10年に届かない方など"],
          ["phone", "来ないから対象外、とは限りません"]],
      left="sensei_caution", right="kikite_worried"),
    C("請求しないまま5年", "compare", title="5枚目もまた、同じ形です",
      panels=[{"icon": "postcard", "cap": "届くのは"},
              {"icon": "warning", "cap": "消えるのは"}],
      rows=["3か月前", "5年後（時効）"],
      left="sensei_serious", right="kikite_down"),

    # ───────────────────────── 第6章
    C("台所の壁に", "art", title="松本さんが、壁に貼った紙",
      img="art_kabe_a4.png", fly="up",
      cap="上から順に5つ。日付だけ書いて",
      left="sensei_reassure", right="kikite_relieved"),
    C("それでは、今日の研究ノート", "check", title="研究ノート（1／2）",
      bgimg="art_kabe_a4.png",
      ok=[["form", "①退職金の前に「申告書」を会社へ"],
          ["calc", "②控除は20年まで年40万円、超は70万円"]],
      no=[["warning", "出さないと、支給額全体に20.42％"]],
      left="sensei_conclude", right="kikite_nod"),
    C("任意継続を選べるのは、退職日の翌日から20日だけ", "check", title="研究ノート（2／2）",
      bgimg="art_kabe_a4.png",
      ok=[["cityhall", "④国民年金は、退職日の翌日から14日以内"],
          ["phone", "⑤65歳前に年金がある方は、先に年金事務所へ電話"]],
      no=[["hanko", "③任意継続は20日だけ。過ぎたら2年戻らない"]],
      left="sensei_conclude", right="kikite_nod"),
    C("退職金の税金がゼロの人は", "check", title="○×クイズ 第1問",
      no=[["scale", "税金ゼロなら、出さなくても損はしない"]],
      ok=[["warning", "ゼロの人ほど、いったん引かれる額が大きい"],
          ["calc", "控除がよく効いていた人ほど、落差が大きい"]],
      left="sensei_caution", right="kikite_think"),
    C("任意継続の期限を過ぎても", "check", title="○×クイズ 第2問",
      no=[["hanko", "あとから申し出れば任意継続にできる"]],
      ok=[["clock", "20日を過ぎたら、その選択肢はなくなる"],
          ["cityhall", "残るのは、国民健康保険だけ"]],
      left="sensei_caution", right="kikite_think"),
    C("失業給付を受け取っても", "check", title="○×クイズ 第3問",
      no=[["chart_down", "年金は一部だけ止まる"]],
      ok=[["warning", "65歳になるまでの老齢年金は、全額止まる"],
          ["clock", "再開は、終わってから3か月程度後"]],
      left="sensei_caution", right="kikite_surprised"),
    C("そして5枚とも、減るのは早くて", "compare", title="覚えていただきたいのは、これだけです",
      panels=[{"icon": "chart_down", "cap": "減るのは"},
              {"icon": "clock", "cap": "戻るのは"}],
      rows=["早い", "遅い"],
      left="sensei_conclude", right="kikite_nod"),
    C("なお、この動画は2026年8月時点", "source", title="ご確認のお願い",
      org="2026年8月時点の情報です",
      doc="金額と期限は、会社の担当部署・" + NL + "年金事務所・市区町村でご確認ください",
      note="※出典（国税庁・協会けんぽ・日本年金機構）は概要欄に記載",
      left="sensei_conclude", right="kikite_nod"),
    C("前回、「9月に届く扶養親族等申告書」", "steps", title="訂正と、次回のお知らせ",
      bgimg="bg_yubin.png",
      pre=1,
      steps=[["warning", "前回「9月」→ 正しくは10月からでした"],
             ["postcard", "次回：10月に届く住民税の紙"]],
      left="sensei_serious", right="kikite_nod"),
]


def main():
    lines = []
    for raw in TTS.read_text(encoding="utf-8").splitlines():
        t = re.sub(r"^(\[[^\]]*\])+", "", raw).strip()
        lines.append(t)

    idx, errs = [], []
    for c in CARDS:
        hits = [i for i, t in enumerate(lines) if t and c["match"] in t]
        if len(hits) != 1:
            errs.append(f"  match {'0 dòng' if not hits else f'{len(hits)} dòng {hits}'}: {c['match']!r}")
            idx.append(None)
        else:
            idx.append(hits[0])

    if errs:
        print("🔴 MATCH KHÔNG DUY NHẤT — chưa ghi file:")
        print("\n".join(errs))
        sys.exit(1)

    for a, b in zip(idx, idx[1:]):
        if b <= a:
            errs.append(f"  thứ tự sai: dòng {a} → {b}")
    # 🔴 GATE LABEL TIMELINE — `L_timeline` vẽ label bằng F("black",40) CỐ ĐỊNH (không fit)
    # và canh giữa thanh vàng rộng (CONTENT_X1-CONTENT_X0)*prog. Label dài hơn thanh ⇒ chữ
    # tràn ra ngoài vùng nội dung (đã dính ở thẻ 21 và 47, user bắt được khi duyệt frame).
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "timeline":
            continue
        barw = (1400 - 520) * v.get("prog", .62)
        txtw = len(v.get("label", "")) * 40
        if txtw > barw:
            errs.append(f"  [{k:02d}] label timeline TRÀN: {txtw}px chữ > {barw:.0f}px thanh "
                        f"(prog={v.get('prog', .62)}) — rút label hoặc tăng prog: {v.get('label')!r}")

    # 🔴 GATE `steps` 1 HÀNG — layout này vẽ bằng tw() MỘT DÒNG (khác timeline/flow dùng tw_ml
    # vì cột hẹp), nên ký tự xuống dòng trong text là tự bắt nó chia 2 hàng vô cớ — trong khi
    # fit() vốn co được chữ cho vừa 682px. Đã dính 11 chỗ ở 5 thẻ, user bắt được khi duyệt frame.
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "steps":
            continue
        for j, row in enumerate(v.get("steps", [])):
            txt = row[1] if isinstance(row, (list, tuple)) else row
            if NL in txt:
                errs.append(f"  [{k:02d}] steps bước {j+1} có ký tự xuống dòng → bỏ đi, "
                            f"để fit() co chữ: {txt!r}")

    # 🔴 GATE CHỮ TRONG HỘP TIMELINE — `fit_ml` có SÀN font 26; text dài quá sàn thì nó
    # KHÔNG co thêm mà TRÀN ra ngoài hộp. Hộp = (1400-520)/n - 26, chừa 26 padding.
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "timeline":
            continue
        cap = int(((1400 - 520) / len(v["steps"]) - 52) // 26)
        for j, row in enumerate(v["steps"]):
            txt = row[1] if isinstance(row, (list, tuple)) else row
            for ln in txt.split(NL):
                if len(ln) > cap:
                    errs.append(f"  [{k:02d}] timeline hộp {j+1} TRÀN: {len(ln)} ký > trần {cap} "
                                f"(n={len(v['steps'])} cột): {ln!r}")

    # 🔴 GATE CHUNG — mọi layout đều dùng fit()/fit_ml() CÓ SÀN font; quá sàn là TRÀN, không co
    # thêm. Trần ký tự = bề rộng khả dụng ÷ cỡ sàn (chữ full-width ≈ 1 ô font).
    #   check  : fit(…, CONTENT_X1-x-148 = 732, sàn 30) → 24 ký
    #   compare: fit(…, 880-110 = 770,        sàn 24) → 32 ký
    #   steps  : fit(…, 1400-718-20 = 662,    sàn 30) → 22 ký
    #   source : fit_ml(…, bx1-bx0-250 = 690, sàn 30) → 23 ký/dòng
    CAPS = {"check": (24, ("ok", "no")), "compare": (32, ("rows",)),
            "steps": (22, ("steps",)), "source": (23, ("doc",))}
    for k, c in enumerate(CARDS):
        v = c["stage"]
        cap_spec = CAPS.get(v.get("layout"))
        if not cap_spec:
            continue
        cap, keys = cap_spec
        for key in keys:
            val = v.get(key)
            if not val:
                continue
            items = [val] if isinstance(val, str) else val
            for j, row in enumerate(items):
                txt = row[1] if isinstance(row, (list, tuple)) else row
                for ln in str(txt).split(NL):
                    if len(ln) > cap:
                        errs.append(f"  [{k:02d}] {v['layout']}.{key}[{j}] TRÀN: {len(ln)} ký "
                                    f"> trần {cap}: {ln!r}")

    gaps = [b - a for a, b in zip(idx, idx[1:])]
    tight = [(i, g) for i, g in enumerate(gaps) if g < 2]
    if tight:
        errs.append("  thẻ cách <2 dòng (nguy cơ entry <6s): " + str(tight))
    if errs:
        print("🔴 GATE NHỊP:")
        print("\n".join(errs))
        sys.exit(1)

    n = len(CARDS)
    per_min = n / (DUR_SEC / 60)
    avg = DUR_SEC / n
    OUT.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1), encoding="utf-8")

    import collections
    dist = collections.Counter(c["stage"]["layout"] for c in CARDS)
    print(f"✅ ghi {OUT.name}  —  {n} thẻ")
    print(f"   nhịp: {per_min:.2f} đổi hình/phút (trần 6)  ·  TB {avg:.1f}s/thẻ (sàn 6s)")
    print(f"   khoảng cách dòng: min {min(gaps)} · TB {sum(gaps)/len(gaps):.1f} · max {max(gaps)}")
    print(f"   layout: {dict(dist)}")
    sp = [i for i, c in enumerate(CARDS) if c["stage"]["layout"] == "compare"]
    print(f"   thẻ trục `compare`: {len(sp)} thẻ ở vị trí {sp}")
    art = sorted({c["stage"][k] for c in CARDS for k in ("img", "fill", "bgimg")
                  if c["stage"].get(k)})
    print(f"   ảnh cần có ({len(art)}): {art}")


if __name__ == "__main__":
    main()
