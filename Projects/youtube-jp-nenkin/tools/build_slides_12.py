# -*- coding: utf-8 -*-
"""build_slides_12.py — sinh `12_..._SLIDES.json` cho video 12 (住民税の紙が10月に届く).

Chép khuôn từ `build_slides_11.py` (luật `render-background.md` §2.6: **chép khuôn, đừng gõ
lại từ đầu**). Toàn bộ 10 gate của bản 11 giữ nguyên, không sửa một dòng nào:
  ① mỗi `match` khớp ĐÚNG 1 dòng   ② index tăng dần   ③ khoảng cách ≥2 dòng
  ④ mật độ ≤6 đổi hình/phút        ⑤ label timeline không tràn thanh
  ⑥ `steps` cấm ký tự xuống dòng   ⑦ chữ trong hộp timeline
  ⑧ trần ký tự check/compare/steps/source

⭐ TRỤC HÌNH của video này: 「ポストか、引き出しか」 — hai cái nhà của cold open, mã hoá bằng
layout `compare` (2 cột) lặp **7 lần**: cold open · 第2章 去年/今年 · 第2章 紙の意味 · 第3章 二式
· 第3章 所得税/住民税 · 第3章 いま/来年の春 · 第4章 届く/届かない · 第6章 引き出し/目に入る所.
Đổi layout mấy thẻ đó là phá xương sống thị giác của bài (§GĐ5 mục ② của script).

⭐ TRỤC SỐ: layout `bars` — cái duy nhất vẽ được **cái "dải" (帯) tụt xuống 148万**, tức hình
ảnh trung tâm của bài. Dùng 4 lần: 帯 3 tầng · 205万→148万 · 240万 vs 214万 · phân tách 5万2千円.

CHẠY:  python tools/build_slides_12.py
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parents[1]
STEM = "12_juminzei-koujo-shinkokusho-10gatsu"
TTS = PROJ / "03_SCRIPTS" / f"{STEM}_TTS.md"
OUT = PROJ / "03_SCRIPTS" / f"{STEM}_SLIDES.json"
DUR_SEC = 16 * 60 + 38          # đo bằng make_tts --dry / check_pace

NL = "\n"

# ẢNH AI user gen — tên phải khớp `art_prompts_SPEC.md` của video này
A_FUTA = "art_fuutou_futatsu.png"      # entry 0: HAI phong bì giống nhau trên bàn
A_HIKI = "art_hikidashi.png"           # ngăn kéo hé mở, phong bì chưa mở bên trong
A_SHIN = "art_shinkokusho_fuyou.png"   # tờ đơn chung chung, ô kẻ TRỐNG, không chữ
A_TSU = "art_tsuuchisho_ran.png"       # tờ thông báo, bảng kẻ trống (số 0 do tool ghim)
A_SHOK = "art_shokutaku_fuutou.png"    # phong bì dựng trên bàn ăn
A_TECHO = "art_techo_calendar.png"     # sổ tay + lịch khoanh đỏ
B_DAI = "bg_daidokoro.png"             # nền phòng khách/bếp sáng, NHẠT (bgimg)
B_SHI = "bg_shiyakusho_akari.png"      # nền quầy hành chính sáng, NHẠT (bgimg)
# 原典ショット đã có sẵn trong 06_VIDEO/<slug>/genten/ — tool tự copy sang art/
G1 = "genten_01_shot.png"   # 3 file này do `tools/make_genten_12.py` dựng: crop vùng câu
G2 = "genten_02_shot.png"   # đang đọc + PHÓNG TO + KHOANH ĐỎ DÀY + nhãn nguồn, tỉ lệ 1.607
G3 = "genten_03_shot.png"   # khớp hộp `L_art` ⇒ cover-crop không cắt gì.


def C(match, layout, **kw):
    return {"match": match, "video": True, "stage": dict(layout=layout, **kw)}


CARDS = [
    # ───────────────────────── COLD OPEN（二軒の家。tên nhân vật CHƯA trả）
    C("日本年金機構から、まったく同じ封筒", "art", title="来月10月、まったく同じ封筒が二軒に",
      img=A_FUTA, fly="up",
      cap="中身は「扶養親族等申告書」という紙、1枚だけです",
      left="sensei_present", right="kikite_listen"),
    C("一軒は、名前とご家族", "compare", title="同じ紙。置いた場所だけが違います",
      panels=[{"icon": "mailbox", "cap": "一軒は"},
              {"icon": "docs", "cap": "もう一軒は"}],
      rows=["書いて、ポストに入れた", "引き出しに入れた"],
      left="sensei_explain", right="kikite_think"),
    C("この二軒の差は", "big", title="この二軒に生まれる差",
      value="5万2千円", unit="／年", tone="bad",
      cap="同じ年金額、同じご家族で、です",
      left="sensei_serious", right="kikite_surprised"),
    C("引き出しに入れたお宅の判断は", "check", title="ただ、その判断は「去年までなら」正解でした",
      bgimg=A_HIKI,
      ok=[["calendar", "去年、本当に届かなかった"],
          ["form", "去年は、出さなくてよかった"]],
      left="sensei_explain", right="kikite_nod"),
    C("その「届かなかった」が", "big", title="その「届かなかった」が",
      value="今年の落とし穴", tone="bad",
      cap="去年の正解が、今年の間違いになります",
      left="sensei_caution", right="kikite_worried"),
    C("税金を引かれていない人の家に", "big", title="今日の問いは、ひとつです",
      value="なぜ、届くのか", tone="amber",
      cap="年金から税金を1円も引かれていない方にまで、届きます",
      left="sensei_point", right="kikite_think"),
    C("こんにちは、年金と", "source", title="今日も、原典を一緒に読みます",
      org="年金と老後のお金研究室",
      doc="日本年金機構と総務省のページを" + NL + "画面に出して、一行ずつ確かめます",
      note="※出典は概要欄に記載しています",
      left="sensei_conclude", right="kikite_nod"),

    # ───────────────────────── 第1章 田中さん
    # 🔴 GIỚI THIỆU モニター = `compare`, KHÔNG phải `check`. Đo được: `check` vẽ icon **56px**
    # (khe dòng 88px), ở cỡ đó avatar chỉ còn là vệt màu — không nhận ra mặt ai. `compare` vẽ
    # panel icon **132px** ⇒ nhận ra người ngay. Xem §"BA CHỖ ĐẶT AVATAR" ở cuối file.
    C("横浜の田中さん", "compare", title="モニター・田中さん（横浜）",
      panels=[{"icon": "avatar_tanaka", "cap": "田中さん・67歳"},
              {"icon": "wallet", "cap": "年金 月16万円"}],
      rows=["再雇用で、週に5日 働いている", "1年で192万円", "この紙は、毎年届いていた"],
      left="sensei_present", right="kikite_listen"),
    C("ところが去年の9月", "big", title="ところが去年の9月",
      value="届かなかった", tone="amber",
      cap="手違いでも、書き忘れでもありません",
      left="sensei_serious", right="kikite_surprised"),
    C("年金から所得税を引く基準が", "bars", title="去年、所得税を引く基準が上がりました",
      rows=[["去年までの基準", 158, "grey", "158万円"],
            ["田中さんの年金", 192, "amber", "192万円"],
            ["去年からの基準", 205, "bad", "205万円"]],
      max=214, note="192万円は、線の下に出ました",
      left="sensei_explain", right="kikite_think"),
    C("その田中さんの家に、今年10月", "art", title="その田中さんの家に、今年また届きます",
      img=A_SHIN, fly="up",
      cap="「扶養親族等申告書」",
      left="sensei_point", right="kikite_surprised"),
    C("日本年金機構のページを、そのまま出します", "art", title="原典①：日本年金機構（更新日 6月17日）",
      img=G1, fly="up",
      cap="赤で囲んだところ ＝ 148万円以上・令和8年10月より順次",
      left="sensei_point", right="kikite_think"),
    C("令和8年10月より順次お送りします", "big", title="今年、紙が届く方",
      value="148万円", unit="以上", tone="bad",
      cap="65歳以上の場合。65歳未満は98万円以上です",
      left="sensei_serious", right="kikite_listen"),
    C("去年は線の下、今年は線の中", "bars", title="線が、57万円分だけ下に降りました",
      rows=[["去年の基準", 205, "grey", "205万円"],
            ["田中さんの年金", 192, "amber", "192万円"],
            ["今年の基準", 148, "bad", "148万円"]],
      max=214, note="年金額は、1円も変わっていません",
      left="sensei_explain", right="kikite_surprised"),
    C("では、なぜ148万円なのか", "bars", title="住民税がかからない上限（65歳・おひとり暮らし）",
      rows=[["1級地", 155, "amber", "155万円"],
            ["2級地", 151, "amber", "151.5万円"],
            ["3級地", 148, "bad", "148万円"]],
      max=155, note="お住まいの地域によって違います",
      left="sensei_explain", right="kikite_think"),
    C("機構は、そのいちばん低い148万円", "check", title="だから、いちばん低い線に合わせています",
      bgimg=B_DAI,
      ok=[["mailbox", "148万円に合わせて送る"],
          ["person", "取りこぼさないように、広めに"]],
      left="sensei_reassure", right="kikite_nod"),
    C("田中さんは、年金から所得税を", "art", title="ところが、田中さんの通知書は",
      img=A_TSU, fly="up",
      pins=[["所得税 ０円", 0.62, 0.50]],
      cap="年金から所得税は、引かれていません",
      left="sensei_point", right="kikite_think"),
    C("そのゼロの方に", "big", title="そのゼロの方に、なぜ税金の紙が来るのか",
      value="答えは1枚の図", tone="amber",
      cap="機構が出している図に、はっきり描いてあります",
      left="sensei_point", right="kikite_think"),

    # ───────────────────────── 第2章 帯の話（REVEAL 中心）
    C("もう一度、機構のページです", "art", title="原典②：提出対象の範囲拡大イメージ",
      img=G2, fly="up",
      cap="赤で囲んだところ ＝ 去年グレーだった帯が、オレンジに",
      left="sensei_point", right="kikite_think"),
    C("年金額を縦に積んだ棒が", "bars", title="年金額は、3つの帯に分かれます",
      rows=[["所得税もかかる", 214, "amber", "214万円〜"],
            ["住民税だけかかる", 192, "grey", "148〜214万円"],
            ["どちらもかからない", 148, "ok", "〜148万円"]],
      max=240, note="田中さんの192万円は、真ん中の帯です",
      left="sensei_explain", right="kikite_listen"),
    C("そのグレーが、今年", "compare", title="真ん中の帯が、今年から対象になりました",
      panels=[{"icon": "docs", "cap": "去年の図"},
              {"icon": "form", "cap": "今年の図"}],
      rows=["オレンジは、いちばん上だけ", "真ん中の帯も、オレンジに"],
      left="sensei_explain", right="kikite_surprised"),
    C("去年までのこの紙は", "compare", title="紙の意味が、変わりました",
      panels=[{"icon": "calc", "cap": "去年まで"},
              {"icon": "cityhall", "cap": "今年から"}],
      rows=["所得税のための紙", "住民税のための紙でもある"],
      left="sensei_present", right="kikite_nod"),
    C("これが、今日のいちばんの答え", "big", title="これが、今日のいちばんの答えです",
      value="住民税の紙", tone="bad",
      cap="所得税を引かれていない方にも届く、理由です",
      left="sensei_serious", right="kikite_surprised"),
    C("そして、その方の通知書には", "check", title="いちばん自然な判断が、いちばん危ない",
      bgimg=A_TSU,
      ok=[["docs", "通知書の所得税の欄は、ゼロ"]],
      no=[["warning", "「うちは関係ない」と判断する"]],
      left="sensei_caution", right="kikite_worried"),
    C("その、いちばん自然な判断を", "big", title="その判断をされた方が",
      value="いちばん損", tone="bad",
      cap="自然な判断であるほど、気づけません",
      left="sensei_serious", right="kikite_down"),

    # ───────────────────────── 第3章 計算タイム（ポストの家 ＝ 高橋）
    C("封筒を書いてポストに入れた", "compare", title="ポストに入れたお宅 ＝ 高橋さん（東京）",
      panels=[{"icon": "avatar_takahashi", "cap": "高橋さん・65歳"},
              {"icon": "wallet", "cap": "年金 月20万円"}],
      rows=["この春まで、メーカーの部長", "1年で240万円ほど"],
      left="sensei_present", right="kikite_listen"),
    C("あのときは、212万円が", "big", title="以前の研究の、あの高橋さんです",
      value="212万円", tone="amber",
      cap="年金の請求書で、奥さまの欄を飛ばしそうになった方",
      left="sensei_explain", right="kikite_nod"),
    C("1年で240万円ほどですから", "bars", title="高橋さんは、従来どおり所得税が引かれます",
      rows=[["源泉徴収の線", 214, "grey", "214万円"],
            ["高橋さんの年金", 240, "amber", "240万円ほど"]],
      max=260, note="214万円より上の帯です",
      left="sensei_explain", right="kikite_think"),
    C("奥さまは、昭和41年6月生まれ", "check", title="そして、奥さまのこと",
      bgimg=B_DAI,
      ok=[["couple", "60歳（昭和41年6月生まれ）"],
          ["person", "いまは、お勤めをされていない"],
          ["calc", "つまり、配偶者控除に当たる"]],
      left="sensei_explain", right="kikite_nod"),
    C("式は、機構が、はっきり2つ", "art", title="原典③：機構が並べて書いている、ふたつの式",
      img=G3, fly="up",
      cap="赤で囲んだところ ＝ 出さなかった場合の式",
      left="sensei_point", right="kikite_think"),
    C("同じように社会保険料を引いて", "compare", title="違うのは、引ける控除だけです",
      panels=[{"icon": "form", "cap": "出した場合"},
              {"icon": "warning", "cap": "出さなかった場合"}],
      rows=["基礎控除 ＋ 配偶者控除など", "基礎控除だけ"],
      left="sensei_explain", right="kikite_surprised"),
    C("差が出るのは、税率ではありません", "big", title="税率は、どちらも同じ 5.105％",
      value="引ける金額", tone="amber",
      cap="機構も「所得税率に差はありません」と書いています",
      left="sensei_point", right="kikite_nod"),
    C("配偶者控除は、所得税では38万円", "big", title="まず、所得税のぶん",
      value="1万9千円", tone="amber",
      cap="38万円 × 5.105％ ＝ およそ1万9千円",
      left="sensei_explain", right="kikite_listen"),
    C("住民税の配偶者控除は、33万円", "compare", title="同じ「配偶者控除」でも、額が違います",
      panels=[{"icon": "calc", "cap": "所得税"},
              {"icon": "cityhall", "cap": "住民税"}],
      rows=["配偶者控除 38万円 × 5.105％", "配偶者控除 33万円 × 10％"],
      left="sensei_explain", right="kikite_think"),
    C("ふたつ足すと", "bars", title="紙1枚で、1年にこれだけ変わります",
      rows=[["所得税のぶん", 19399, "amber", "1万9千円"],
            ["住民税のぶん", 33000, "bad", "3万3千円"],
            ["合計", 52399, "bad", "5万2千円"]],
      max=52399, note="配偶者控除ひとつ、1年分です",
      left="sensei_serious", right="kikite_surprised"),
    C("この5万2千円は、配偶者控除だけを", "check", title="ただし、固定の金額ではありません",
      bgimg=B_DAI,
      no=[["warning", "決まった金額ではない"]],
      ok=[["cityhall", "自治体やほかの控除で前後する"],
          ["magnifier", "通知書と市区町村でご確認を"]],
      left="sensei_caution", right="kikite_nod"),
    C("同じ状況が10年続けば", "big", title="同じ状況が10年続くと",
      value="およそ52万円", tone="bad",
      cap="単純に足した、目安の金額です",
      left="sensei_serious", right="kikite_surprised"),
    C("申告書を提出しない場合は", "source", title="機構が書いている、いちばん怖い一文",
      org="日本年金機構",
      doc="「確定申告を行わないと" + NL + "配偶者控除等を受けることができません」",
      note="※消えるのではなく、戻すのに確定申告が必要になります",
      left="sensei_serious", right="kikite_worried"),
    C("来年の春に、ご自分で確定申告を", "compare", title="どちらが楽か、という話です",
      panels=[{"icon": "calendar", "cap": "来年の春"},
              {"icon": "form", "cap": "いま"}],
      rows=["自分で確定申告をする", "届く紙に、名前を書く"],
      left="sensei_explain", right="kikite_nod"),

    # ───────────────────────── CTA
    C("ここで、ひとつだけお願い", "source", title="この研究室について",
      org="年金と老後のお金研究室",
      doc="高評価・シェア・コメントが" + NL + "次の研究テーマになります",
      note="※ご感想や、調べてほしいテーマをお寄せください",
      left="sensei_present", right="kikite_nod"),

    # ───────────────────────── 第4章 出さなくていい方
    C("機構は、出さなくていい方も", "check", title="出さなくていい方も、はっきりいます",
      bgimg=B_DAI,
      ok=[["person", "障害者・寡婦などに当たらない"],
          ["couple", "控除の対象になる家族もいない"],
          ["form", "この方は、出す必要がない"]],
      left="sensei_reassure", right="kikite_relieved"),
    C("新潟の渡辺さん", "compare", title="モニター・渡辺さん（新潟）",
      panels=[{"icon": "avatar_watanabe", "cap": "渡辺さん・66歳"},
              {"icon": "wallet", "cap": "年金 月7万2千円"}],
      rows=["新潟で、おひとり暮らし", "1年で86万4千円 ＝ 148万円より下"],
      left="sensei_present", right="kikite_listen"),
    C("148万円より下ですから", "big", title="渡辺さんの家には",
      value="届きません", tone="ok",
      cap="そして、何もしなくて大丈夫です",
      left="sensei_reassure", right="kikite_relieved"),
    C("ただ、渡辺さんのような方に", "big", title="ただ、ここに逆向きの穴があります",
      value="逆の落とし穴", tone="amber",
      cap="「届かない」の意味を、間違えないでください",
      left="sensei_caution", right="kikite_worried"),
    C("個人住民税の課税対象となる場合は", "source", title="機構は、こうも書いています",
      org="日本年金機構",
      doc="「住民税の申告が" + NL + "必要となる場合があります」",
      note="※詳しくは、お住まいの市区町村にご確認ください",
      left="sensei_serious", right="kikite_think"),
    C("つまり、「届かない」は", "compare", title="「届かない」が意味すること",
      panels=[{"icon": "calc", "cap": "所得税の紙"},
              {"icon": "cityhall", "cap": "住民税"}],
      rows=["届かない ＝ 出さなくていい", "何もしなくていい、とは限らない"],
      left="sensei_explain", right="kikite_nod"),
    C("気になる方は、市役所の税の窓口で", "steps", title="いちばん早くて、確かな方法",
      bgimg=B_SHI,
      steps=[["phone", "市役所の税の窓口へ"],
             ["magnifier", "「住民税の申告は要りますか」"]],
      left="sensei_point", right="kikite_nod"),
    # 🔴 bgimg KHÔNG phải để trang trí: thẻ toàn dòng `no` render chữ XÁM (168,174,184) trên
    # nền kem ⇒ nhạt nhất video, tệ nhất với tệp 45+ (`nenkin/CLAUDE.md` §VISUAL). Có `bgimg`
    # thì `mut()` đổi sang GREY_ON_BG (92,100,114) — đậm hơn rõ mà vẫn giữ nghĩa "điều SAI".
    C("よくある誤解を、3つだけ", "check", title="よくある誤解 3つ（すべて違います）",
      bgimg=B_DAI,
      no=[["calendar", "去年届かなかったから、今年も"],
          ["calc", "税金を引かれていないから関係ない"],
          ["scale", "税率が下がらないから、同じ"]],
      left="sensei_caution", right="kikite_think"),
    C("住民税のための紙でもあります。みっつ", "check", title="正しくは、こうです",
      bgimg=B_DAI,
      ok=[["form", "基準が、今年から変わった"],
          ["cityhall", "住民税のための紙でもある"],
          ["calc", "変わるのは、引ける金額"]],
      left="sensei_explain", right="kikite_nod"),

    # ───────────────────────── 第5章 期限（đoạn "thở"）
    C("では、期限に間に合わなかったら", "big", title="では、期限に遅れたら",
      value="取り戻せます", tone="ok",
      cap="ここは、思ったより優しい制度です",
      left="sensei_reassure", right="kikite_relieved"),
    C("その年の最初の年金のお支払いまで", "timeline", title="遅れても、さかのぼって計算し直されます",
      **{"from": "期限に遅れた", "to": "出した時点"},
      label="さかのぼって再計算", prog=0.82,
      steps=[["clock", "遅れて" + NL + "気づく"],
             ["form", "それでも" + NL + "提出する"],
             ["calc", "最初の支払い" + NL + "まで再計算"]],
      left="sensei_reassure", right="kikite_nod"),
    C("去年の分では、出していない方に", "big", title="去年は、もう一度お知らせが届きました",
      value="2月6日", tone="amber",
      cap="今年も同じ運用なら、2月にもう一度チャンスがあります",
      left="sensei_explain", right="kikite_listen"),
    C("昨年の申告書では、同封の返信用封筒に", "steps", title="紙で出す場合（昨年の申告書では）",
      steps=[["env", "同封の返信用封筒に入れる"],
             ["hanko", "自分で切手を貼る（110円）"],
             ["mailbox", "ポストに入れる"]],
      note="※今年の分は、同封の案内でご確認ください",
      left="sensei_explain", right="kikite_listen"),
    C("そして、切手もポストも要らない道", "compare", title="切手もポストも要らない道が、もう一本",
      panels=[{"icon": "mailbox", "cap": "紙で出す"},
              {"icon": "cashcard", "cap": "画面から出す"}],
      rows=["切手110円 ＋ ポストへ", "マイナポータル ＋ ねんきんネット"],
      left="sensei_present", right="kikite_think"),
    C("しかも、一度これで出した方には", "check", title="一度、画面から出しておくと",
      bgimg=B_DAI,
      ok=[["form", "翌年以降、紙が送られてこない"],
          ["calendar", "毎年、封筒を探す手間がなくなる"]],
      left="sensei_reassure", right="kikite_relieved"),
    C("書き方が分からないときは", "source", title="書き方が分からないときは",
      org="専用のお問い合わせダイヤル",
      doc="0570-081-240" + NL + "扶養親族等申告書の専用窓口です",
      note="※紙をなくした方は、機構のページから印刷できます",
      left="sensei_point", right="kikite_nod"),

    # ───────────────────────── 第6章 あの二軒の、その後（ĐÓNG VÒNG）
    C("封筒を書いて、ポストに入れたお宅", "big", title="ポストに入れたお宅は",
      value="高橋さん", tone="ok",
      cap="この春まで部長をされていた、あの高橋さんです",
      left="sensei_present", right="kikite_nod"),
    C("あのときは、妻の名前を書く欄を", "big", title="高橋さんは、少し笑って",
      value="「二回やる" + NL + "ところでした」", tone="amber",
      cap="年金の請求書と、この申告書は、別のものです",
      left="sensei_explain", right="kikite_relieved"),
    C("今年は、封筒を開けたら", "art", title="高橋さんが、手帳を出して言ったこと",
      img=A_TECHO, fly="up",
      pins=[["丸をつける", 0.50, 0.18]],
      cap="「妻の名前を書くまで、消しません」",
      left="sensei_reassure", right="kikite_relieved"),
    # ⭐ THẺ TRẢ VÒNG của cold open — hai cái nhà, giờ có MẶT cả hai, cạnh nhau.
    C("そして、引き出しに入れたお宅", "compare", title="あの二軒は、このお二人でした",
      panels=[{"icon": "avatar_takahashi", "cap": "ポストへ"},
              {"icon": "avatar_tanaka", "cap": "引き出しへ"}],
      rows=["高橋さん・65歳（東京）", "田中さん・67歳（横浜）"],
      left="sensei_conclude", right="kikite_nod"),
    C("今年は、引き出しじゃなくて", "art", title="田中さんが、今年決めたこと",
      img=A_SHOK, fly="up",
      pins=[["目に入るところに", 0.50, 0.16]],
      cap="「引き出しじゃなくて、食卓の上に置いておきます」",
      left="sensei_reassure", right="kikite_relieved"),
    C("今年10月から、扶養親族等申告書が届く方が", "check", title="研究ノート（1／2）",
      bgimg=A_SHIN,
      ok=[["form", "①10月から、148万円以上に"],
          ["cityhall", "②住民税の控除も、この紙で"],
          ["avatar_tanaka", "去年届かなかった方にも届く"]],
      left="sensei_conclude", right="kikite_nod"),
    C("出さないと、配偶者控除などが", "check", title="研究ノート（2／2）",
      bgimg=A_SHIN,
      ok=[["calc", "③控除ひとつで、年5万2千円"],
          ["clock", "④遅れても、さかのぼって再計算"]],
      no=[["warning", "出さないと、計算に入らない"]],
      left="sensei_conclude", right="kikite_nod"),
    C("そして最後に、3つだけ", "steps", title="セルフチェック 3問",
      steps=[["wallet", "年金額は、年148万円を超える？"],
             ["couple", "控除の対象になる家族はいる？"],
             ["mailbox", "届いた封筒を、どこに置く？"]],
      left="sensei_present", right="kikite_think"),
    C("封筒が届いたら、どこに置きますか", "compare", title="ここだけは、今日決めておいてください",
      panels=[{"icon": "docs", "cap": "引き出し"},
              {"icon": "mailbox", "cap": "目に入るところ"}],
      rows=["去年までの、正解", "今年の、正解"],
      left="sensei_conclude", right="kikite_nod"),
    C("なお、この動画は2026年8月時点", "source", title="ご確認のお願い",
      org="2026年8月時点の情報です",
      doc="金額と手続きは、年金事務所・" + NL + "ねんきんネット・市区町村でご確認を",
      note="※出典（日本年金機構・総務省）は概要欄に記載",
      left="sensei_conclude", right="kikite_nod"),
    C("さて、次回です", "steps", title="次回のお知らせ",
      steps=[["postcard", "12月の年金だけ、額が違う方"],
             ["calc", "11月まで多めに引かれた分を精算"]],
      left="sensei_present", right="kikite_nod"),
]


def main():
    # 🔴 3 thẻ 原典 phải là bản ĐÃ KHOANH ĐỎ của `make_genten_12.py`, không phải ảnh chụp
    # cả trang trong genten/ — ảnh cả trang thì chữ bé như hạt gạo và KHÔNG có khung đỏ,
    # trong khi thoại đọc đúng câu 「赤で囲んだところ」 (bắt được khi duyệt sheet 2026-08-14).
    vdir = PROJ / "06_VIDEO" / STEM
    art_dir = vdir / "art"
    art_dir.mkdir(parents=True, exist_ok=True)
    lack = [g for g in (G1, G2, G3) if not (art_dir / g).exists()]
    if lack:
        print("🔴 CHƯA DỰNG 原典ショット: " + ", ".join(lack))
        print("   chạy trước:  python tools/make_genten_12.py")
        sys.exit(1)

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

    # 🔴 GATE LABEL TIMELINE — `L_timeline` vẽ label bằng F("black",40) CỐ ĐỊNH (không fit).
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "timeline":
            continue
        barw = (1400 - 520) * v.get("prog", .62)
        txtw = len(v.get("label", "")) * 40
        if txtw > barw:
            errs.append(f"  [{k:02d}] label timeline TRÀN: {txtw}px chữ > {barw:.0f}px thanh "
                        f"(prog={v.get('prog', .62)}): {v.get('label')!r}")

    # 🔴 GATE `steps` 1 HÀNG — vẽ bằng tw() MỘT DÒNG, ký tự xuống dòng là tự chia hàng vô cớ.
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "steps":
            continue
        for j, row in enumerate(v.get("steps", [])):
            txt = row[1] if isinstance(row, (list, tuple)) else row
            if NL in txt:
                errs.append(f"  [{k:02d}] steps bước {j+1} có ký tự xuống dòng: {txt!r}")

    # 🔴 GATE CHỮ TRONG HỘP TIMELINE — `fit_ml` sàn font 26, quá sàn là TRÀN.
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("layout") != "timeline":
            continue
        cap = int(((1400 - 520) / len(v["steps"]) - 52) // 26)
        for j, row in enumerate(v["steps"]):
            txt = row[1] if isinstance(row, (list, tuple)) else row
            for ln in txt.split(NL):
                if len(ln) > cap:
                    errs.append(f"  [{k:02d}] timeline hộp {j+1} TRÀN: {len(ln)} ký > trần {cap}: {ln!r}")

    # 🔴 GATE CHUNG — trần ký tự = bề rộng khả dụng ÷ cỡ sàn font.
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

    # 🔴 GATE SỐ HÀNG theo layout (compare tối đa 3 hàng — hàng 4 vượt đáy card)
    ROWCAP = {"compare": ("rows", 3), "check": (None, 6), "steps": ("steps", 5),
              "timeline": ("steps", 5), "bars": ("rows", 5)}
    for k, c in enumerate(CARDS):
        v = c["stage"]
        spec = ROWCAP.get(v.get("layout"))
        if not spec:
            continue
        key, mx = spec
        n = len(v.get("ok", [])) + len(v.get("no", [])) if key is None else len(v.get(key, []))
        if n > mx:
            errs.append(f"  [{k:02d}] {v['layout']} có {n} hàng > trần {mx}")

    # 🔴 GATE `fill` — ảnh lấp góc dưới-phải ĐÈ LÊN CHỮ của check/steps (media-library §2.10 ④)
    for k, c in enumerate(CARDS):
        v = c["stage"]
        if v.get("fill") and v.get("layout") in ("check", "steps"):
            errs.append(f"  [{k:02d}] `fill` trên layout {v['layout']} → đè lên chữ, dùng `bgimg`")

    # 🔴 GATE `rank` — badge 「その1」 dán đè góc sân khấu, nhìn như miếng vá
    for k, c in enumerate(CARDS):
        if "rank" in c:
            errs.append(f"  [{k:02d}] entry `stage` không được có khoá `rank`")

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
    if per_min > 6:
        print(f"🔴 mật độ {per_min:.2f} đổi hình/phút > trần 6")
        sys.exit(1)
    OUT.write_text(json.dumps(CARDS, ensure_ascii=False, indent=1), encoding="utf-8")

    import collections
    dist = collections.Counter(c["stage"]["layout"] for c in CARDS)
    print(f"✅ ghi {OUT.name}  —  {n} thẻ")
    print(f"   nhịp: {per_min:.2f} đổi hình/phút (trần 6)  ·  TB {avg:.1f}s/thẻ (sàn 6s)")
    print(f"   khoảng cách dòng: min {min(gaps)} · TB {sum(gaps)/len(gaps):.1f} · max {max(gaps)}")
    print(f"   layout: {dict(dist)}")
    sp = [i for i, c in enumerate(CARDS) if c["stage"]["layout"] == "compare"]
    print(f"   thẻ trục `compare`: {len(sp)} thẻ ở vị trí {sp}")
    ba = [i for i, c in enumerate(CARDS) if c["stage"]["layout"] == "bars"]
    print(f"   thẻ trục số `bars`: {len(ba)} thẻ ở vị trí {ba}")
    art = sorted({c["stage"][k] for c in CARDS for k in ("img", "fill", "bgimg")
                  if c["stage"].get(k)})
    have = [f for f in art if (art_dir / f).exists()]
    miss = [f for f in art if f not in have]
    print(f"   ảnh cần có ({len(art)}): đã có {len(have)} · THIẾU {len(miss)}")
    for f in miss:
        print(f"     · {f}")


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════════════
# BA CHỖ ĐẶT AVATAR — đo bằng máy 2026-08-14, đừng đoán lại
#
#   `compare` → `panels[].icon`   **132px**  ✅ nhận ra mặt ngay. CHỖ DUY NHẤT dùng avatar tử tế.
#   `check`/`steps` → cột icon     **56px**  🟡 chỉ còn là "gợi ý có người", không phải chân dung.
#   `big`/`art` → khoá `fill`      390×316   ⛔ **KHÔNG DÙNG ĐƯỢC** cho avatar, 2 lý do đã dựng thử:
#        ① `fill` ĐÈ LÊN `cap` và `note` của `L_big` (cap ở y≈672, hộp fill 536–852) — rule
#           `media-library.md` §2.10 ④ nói fill "an toàn ở big/art", nhưng đó là với thẻ KHÔNG
#           có cap/note. Có cap là đè.
#        ② `fill_art()` mở ảnh bằng `.convert("RGB")` ⇒ 4 góc trong suốt của PNG avatar thành
#           ĐEN, ra một ô đen bọc mặt người.
# ⇒ Muốn một モニター hiện MẶT TO thì dùng `compare`, đừng cố nhét avatar vào `fill`.
