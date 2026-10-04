# -*- coding: utf-8 -*-
r"""telop31.py — chữ hiện trên khung cho các ô của video 31 (扶養親族等申告書 → 非課税世帯 domino).

Khuôn y nguyên `telop29.py` (đọc docstring ở đó trước khi sửa luật):
  · Chữ rút TỪ CHÍNH lời đọc của ô. ⛔ Không thêm số mới, không thêm chế độ mới (YMYL).
  · big ≤9 ký/dòng, ≤2 dòng · sub ≤14 ký, ≤3 thẻ · số viết Ả-rập (CLAUDE.md §② luật 7).
  · `circle=True` chỉ ở khoảnh khắc lật, chỉ dòng có số.
  · KHOÁ THEO CUE VĂN BẢN (mẩu lời đọc duy nhất của ô), không theo chỉ số ô.
Khác v29: viết thẳng dữ kiện thứ hai vào `sub` của từng cue — không tách bảng ENRICH (v29 tách
vì ENRICH là lượt vá sau). Ô nào sót cue thì tự rút từ lời đọc; gate báo ô CÓ SỐ mà thiếu cue.
"""
import json
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
VD = PROJ / "06_VIDEO" / "31_fuyo-shinkokusho-hikazei-domino"

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)

CUES = [
 # ── 0 はじめに ─────────────────────────────────────────────────────────
 ("再来年の7月。", dict(big=["再来年の7月", "通知が2通"], color=RED, size=104,
                       sub=["介護保険料", "ご夫婦それぞれに"])),
 ("二通とも、上がっています", dict(big=["2通とも", "上がる"], color=RED, circle=True,
                              sub=["ご夫婦で年に10万円あまり"])),
 ("ご夫婦で、年に10万円あまり", dict(big=["12月 給付金も", "年15万円あまり"], color=RED, circle=True,
                               sub=["保険料 年10万円あまり", "12月は給付金が入らない"])),
 ("合わせて、年に15万円あまり", dict(big=["年に", "15万円あまり"], color=RED, size=110, circle=True,
                              sub=["保険料＋給付金"])),
 # v3 (2026-09-27): stake người thứ hai + câu tự kiểm kéo lên cold open ⇒ plan gộp 3 câu
 # 「どの通知にも / 原因は / いま届いている」 thành MỘT ô (tách ra thì ô 申告書 chỉ 3,8s < sàn 6s).
 # Telop neo lời (SYNC_TELOP) nên 4 khối hiện lần lượt theo đúng 3 câu.
 ("そのうち7割は", dict(big=["損の7割は", "奥さまの分"], color=RED, circle=True,
                       sub=["年金148万円以上", "65歳以上のご夫婦", "夫を亡くされた方も"])),
 ("どの通知にも、理由は", dict(big=["理由は書いていない", "扶養親族等申告書"], color=NAVY,
                          sub=["原因は2年前の封筒", "いま届いている紙"])),
 ("所得税がかからないからと", dict(big=["古新聞と", "出してしまう"], color=RED, sub=["所得税がかからないから"])),
 ("ところが、この紙が決めるのは", dict(big=["決めるのは", "非課税世帯"], color=RED, circle=True,
                                  sub=["税金の額ではない", "住民税非課税世帯"])),
 ("税金のかからない紙一枚が", dict(big=["なぜ", "2年後の通帳？"], color=NAVY,
                              sub=["税金のかからない紙1枚"])),
 ("そして、なぜ損をするのは", dict(big=["損をするのは", "受け取らない人"], color=RED,
                               sub=["なぜ家族のほうが？"])),
 ("封筒から通帳までの2年間", dict(big=["封筒から", "通帳まで2年"], color=NAVY, sub=["順番にたどる"])),
 ("当研究室は", dict(big=["あなたの数字を", "計算する研究室"], color=NAVY,
                   sub=["制度を読むだけではなく"])),
 # ── 1 所得税の紙が住民税の紙に ──────────────────────────────────────────
 ("所得税のかからない人にまで", dict(big=["なぜ今年は", "届くのか"], color=NAVY,
                                sub=["所得税がかからない人にも"])),
 ("この紙は、もともと", dict(big=["もとは", "所得税の紙"], color=NAVY, sub=["配偶者控除などを受ける"])),
 ("変わったのは、令和8年度", dict(big=["令和8年度", "税制改正"], color=RED, sub=["ここで変わった"])),
 ("こちらが、日本年金機構のページ", dict(big=["日本年金機構"], color=NAVY, size=100,
                                  sub=["令和8年度の改正事項"])),
 ("年金受給者が個人住民税の各種控除", dict(big=["住民税の控除も", "この申告書で"], color=RED,
                                  sub=["令和8年度税制改正で"])),
 ("年金が214万円から上は", dict(big=["148万〜214万", "住民税のみ"], color=RED, size=90,
                              sub=["214万円以上は所得税"])),
 ("今年から、この帯のかたにも", dict(big=["この帯にも", "今年から届く"], color=TEAL,
                                sub=["148万円〜214万円"])),
 ("去年の送り先は", dict(big=["去年は", "205万円以上"], color=NAVY, sub=["65歳以上の送り先"])),
 ("つまり、税金の紙が来なかった", dict(big=["住民税の紙", "として届く"], color=TEAL,
                                 sub=["税金の紙が来なかった家に"])),
 # ── 2 148万円の線 ───────────────────────────────────────────────────────
 ("では、148万円という", dict(big=["148万円の", "正体"], color=NAVY, sub=["どこから来たのか"])),
 ("年金機構は、単身者の", dict(big=["単身者の", "非課税の線"], color=NAVY, sub=["最低額以上に送る"])),
 ("単身者の、です。", dict(big=["なぜ", "ひとり暮らし？"], color=RED, sub=["わざわざ単身者の線"])),
 ("ひとり暮らしでなければ", dict(big=["家族がいれば", "線が動く"], color=TEAL, sub=["ひとり暮らしでなければ"])),
 ("こちらが、大阪市の、住民税が課税されない", dict(big=["大阪市の表"], color=NAVY, size=100,
                                     sub=["いない：45万円以下", "1人：101万円以下"])),
 ("前の年の所得が、同一生計配偶者", dict(big=["いない 45万円", "1人 101万円"], color=RED, circle=True,
                                  sub=["前の年の所得", "同一生計配偶者・扶養親族"])),
 ("では、家族を1人数えるかどうか", dict(big=["1人数えると", "56万円動く"], color=RED, circle=True,
                                  sub=["45万→101万円"])),
 ("同じページには、寡婦", dict(big=["寡婦は", "135万円以下"], color=TEAL, circle=True,
                            sub=["同じ大阪市のページ"])),
 ("夫を亡くされた女性なら", dict(big=["寡婦の欄", "同じ役目"], color=TEAL, sub=["夫を亡くされた女性"])),
 ("年金の場合、65歳以上なら", dict(big=["年金−110万", "＝所得"], color=NAVY,
                               sub=["65歳以上の場合"])),
 ("所得45万円は、年金155万円", dict(big=["45万＝155万", "101万＝211万"], color=NAVY,
                                sub=["所得＝年金"])),
 ("あなたの年金から、110万円を", dict(big=["あなたの年金", "−110万円"], color=RED,
                                 sub=["いくらになりましたか"])),
 ("その数字が45万円を超えていて", dict(big=["非課税は", "紙1枚次第"], color=RED, circle=True,
                                  sub=["45万円を超え", "家族を数えれば線の下"])),
 ("反対に、この紙で受けられる控除", dict(big=["控除なしなら", "税額同じ"], color=TEAL,
                                  sub=["出しても出さなくても"])),
 ("では、線の下に入るお宅で", dict(big=["線の下の家で", "何が起きる"], color=NAVY, sub=["実際に計算"])),
 # ── 3 木村さんご夫妻 ─────────────────────────────────────────────────────
 ("冒頭の、通知が二通届いた", dict(big=["木村さん", "ご夫妻"], color=NAVY,
                               sub=["大阪市", "紙を出さなかった2年後"])),
 ("印刷会社を定年まで", dict(big=["ご主人68歳", "年190万円"], color=NAVY,
                          sub=["年金だけの暮らし"])),
 ("国民年金を400か月", dict(big=["奥さま66歳", "年70万6千円"], color=NAVY,
                          sub=["国民年金400か月"])),
 ("それに、年金生活者支援給付金を", dict(big=["給付金", "月4,683円"], color=TEAL, circle=True,
                                  sub=["年金生活者支援給付金"])),
 ("その給付金が振り込まれる12月", dict(big=["12月は", "お年玉袋"], color=TEAL, sub=["毎年の楽しみ"])),
 ("では、ご主人の所得は", dict(big=["190万−110万", "＝80万円"], color=NAVY,
                           sub=["ご主人の所得"])),
 ("奥さまを家族に数えれば", dict(big=["数えれば", "非課税"], color=TEAL, circle=True,
                              sub=["線は101万円", "80万円は線の下"])),
 ("数えなければ、線は45万円", dict(big=["数えなければ", "課税"], color=RED, circle=True,
                              sub=["線は45万円", "80万円は線の上"])),
 ("同じ年金で、紙を出したかどうか", dict(big=["紙1枚で", "入れ替わる"], color=RED,
                                  sub=["同じ年金で", "課税⇔非課税"])),
 ("以前の研究でお話しした東京の高橋", dict(big=["高橋さんは", "年240万円"], color=NAVY,
                                   sub=["所得税のため毎年出す"])),
 ("では、木村さんのご主人は", dict(big=["所得税は", "1円もなし"], color=NAVY,
                               sub=["だからこそ捨ててしまう"])),
 ("この話をしたとき", dict(big=["新聞と", "一緒にしとった"], color=RED, sub=["ご主人のひとこと"])),
 ("封筒は、古紙回収に出す", dict(big=["ひもの下に", "挟まっていた"], color=RED,
                             sub=["古紙回収の新聞の束", "会社勤めのころは"])),
 ("毎年、秋の終わりになると", dict(big=["総務の人が", "机に配った"], color=NAVY, sub=["秋の終わりの年末調整"])),
 ("配偶者の欄に、奥さまの名前を", dict(big=["配偶者の欄", "名前とはんこ"], color=NAVY,
                                 sub=["会社が集めてくれた"])),
 ("年金暮らしになると", dict(big=["集めに来る人", "もういない"], color=RED, sub=["年金暮らしになると"])),
 # ── 4 封筒から通帳までの2年 ───────────────────────────────────────────────
 ("では、もしこの封筒が", dict(big=["もし", "古紙回収に"], color=RED, sub=["来年から順番に"])),
 ("ご主人の年金からは、所得税が", dict(big=["来年", "何も起きない"], color=NAVY,
                                 sub=["所得税は引かれない", "214万円より少ない"])),
 ("何も起きないから", dict(big=["誰も", "思い出さない"], color=RED, sub=["次は再来年の6月"])),
 ("年金機構のよくある質問には", dict(big=["再来年6月", "住民税の通知"], color=RED,
                                sub=["翌年の住民税で", "配偶者控除なし"])),
 ("奥さまを数えてもらえない", dict(big=["非課税から", "課税へ"], color=RED, circle=True,
                               sub=["奥さまを数えてもらえない"])),
 ("ところが、住民税そのものの額", dict(big=["住民税の額は", "主役ではない"], color=NAVY,
                                 sub=["重いのはこの先"])),
 ("本当に重いのは", dict(big=["非課税世帯", "ではなくなる"], color=RED, circle=True,
                     sub=["木村さんのお宅"])),
 ("今日の内容が分かりやすい", dict(big=["高評価と", "シェアを"], color=TEAL, sub=["研究室を応援"])),
 ("それでは、続きを見ていきましょう", dict(big=["コメントで", "テーマを"], color=TEAL, sub=["次の研究テーマに"])),
 ("続いて、再来年の7月", dict(big=["再来年7月", "通知が2通"], color=RED, sub=["介護保険料"])),
 ("こちらが、大阪市の、介護保険料の表", dict(big=["大阪市の", "介護保険料"], color=NAVY,
                                   sub=["第9期 令和6〜8年度", "今の表で計算"])),
 ("一通目は、ご主人の分", dict(big=["1通目は", "ご主人の分"], color=NAVY,
                            sub=["同じ並びか見比べて"])),
 ("紙を出していれば、世帯全員が非課税で", dict(big=["出していれば", "第4段階"], color=TEAL, circle=True,
                                     sub=["年に7万6,027円", "世帯全員が非課税"])),
 ("出していなければ、ご主人ご本人が課税", dict(big=["出さなければ", "第7段階"], color=RED, circle=True,
                                     sub=["年に12万2,087円", "ご主人が課税"])),
 ("ご主人の分だけで", dict(big=["ご主人", "＋4万6,060円"], color=RED, circle=True,
                        sub=["年に", "2通目は奥さまの分"])),
 ("奥さまご自身の住民税は", dict(big=["奥さまの", "住民税は同じ"], color=NAVY,
                             sub=["紙も受け取っていない"])),
 ("二通目は、奥さまの分", dict(big=["2通目", "奥さまの分"], color=NAVY,
                            sub=["住民税は変わらない", "紙も受け取っていない"])),
 ("それなのに、第2段階", dict(big=["第2→第5段階", "＋5万7,159円"], color=RED, circle=True,
                           sub=["3万7,181→9万4,340円"])),
 ("奥さまの保険料は、2倍半", dict(big=["奥さまの分", "2倍半超え"], color=RED,
                              sub=["紙を受け取っていないのに"])),
 ("そして最後が、再来年の12月", dict(big=["再来年12月", "振込の日"], color=RED, sub=["冒頭の通帳"])),
 ("年金生活者支援給付金の条件の一つは", dict(big=["条件は", "世帯全員非課税"], color=NAVY,
                                    sub=["年金生活者支援給付金"])),
 ("判定の結果は、毎年10月分から", dict(big=["判定は", "10月分から"], color=NAVY,
                                  sub=["1年間反映", "12月の振込から"])),
 ("ご主人が課税になった年の10月分", dict(big=["12月から", "入らなくなる"], color=RED,
                                  sub=["条件を外れる"])),
 ("奥さまの、年に5万6千196円", dict(big=["給付金", "−5万6,196円"], color=RED, circle=True,
                               sub=["奥さまの分 年に"])),
 ("介護保険料が、二人で", dict(big=["保険料", "＋10万3,219円"], color=RED,
                            sub=["2人の分", "給付金 −5万6,196円"])),
 ("年に、15万9千415円。", dict(big=["年に", "15万9,415円"], color=RED, size=110, circle=True,
                            sub=["2年間で倒れたもの"])),
 ("冒頭の、15万円あまり", dict(big=["冒頭の", "15万円の正体"], color=RED, sub=["封筒1通から"])),
 ("今日の計算は、今の大阪市の表", dict(big=["今の表で", "計算した目安"], color=NAVY,
                                 sub=["2年後の額は未定", "自治体で変わる"])),
 ("ですが、非課税世帯から外れれば", dict(big=["段階は", "上に動く"], color=RED,
                                  sub=["非課税世帯から外れれば"])),
 # ── 5 損をするのはだれ ────────────────────────────────────────────────────
 ("では、冒頭の、もう一つの問い", dict(big=["損をするのは", "なぜ家族？"], color=NAVY,
                                 sub=["紙を受け取っていない"])),
 ("15万9千415円のうち", dict(big=["ご主人", "4万6,060円"], color=NAVY, size=100,
                          sub=["奥さま 11万3,355円"])),
 ("奥さまの分は、保険料と給付金を", dict(big=["奥さま", "11万3,355円"], color=RED, circle=True,
                                   sub=["保険料＋給付金"])),
 ("損の7割は", dict(big=["損の7割は", "奥さまの側"], color=RED, size=104, circle=True,
                  sub=["理由は1つの言葉"])),
 ("介護保険料も、給付金も", dict(big=["世帯"], color=RED, size=130,
                             sub=["同じ世帯に課税の人が", "いるかどうか"])),
 ("ご主人の紙一枚が決めていたのは", dict(big=["決めたのは", "世帯の印"], color=RED,
                                  sub=["ご主人の税金ではなく"])),
 ("そして、届いた通知のどれにも", dict(big=["どの通知にも", "封筒の話なし"], color=NAVY,
                                 sub=["物価のせい？", "手違い？"])),
 ("では、本当の理由は", dict(big=["古新聞の", "ひもの下"], color=RED, circle=True, sub=["本当の理由"])),
 ("木村さんのご主人は、その封筒を", dict(big=["封筒を", "抜き出した"], color=TEAL,
                                  sub=["ひもの下から"])),
 ("「妻の名前を書くのは", dict(big=["会社を辞めて", "以来です"], color=TEAL, sub=["妻の名前を書く"])),
 ("再来年の12月も、お年玉袋", dict(big=["お年玉袋は", "買えそう"], color=TEAL, sub=["再来年の12月も"])),
 ("期限に間に合わない場合でも", dict(big=["期限後も", "なるべく早く"], color=TEAL,
                                sub=["捨てていても慌てない", "なくした時の手続きも"])),
 ("それも過ぎてしまったときは", dict(big=["確定申告や", "住民税の申告"], color=TEAL,
                                sub=["控除を受けられる場合", "税の窓口に相談"])),
 # ── 6 研究ノート ─────────────────────────────────────────────────────────
 ("それでは、今日の研究ノート", dict(big=["研究ノート①"], color=NAVY, size=100,
                                sub=["申告書は今年から", "住民税の控除にも使う"])),
 ("二つ目は、今年届くのは", dict(big=["研究ノート②"], color=NAVY, size=100,
                              sub=["65歳以上", "年金148万円以上に届く"])),
 ("三つ目は、住民税がかからない線は", dict(big=["研究ノート③"], color=NAVY, size=100,
                                   sub=["家族を1人数えるか", "寡婦にあたるかで動く"])),
 ("四つ目は、出さなければ", dict(big=["研究ノート④"], color=NAVY, size=100,
                             sub=["翌年の住民税で控除なし", "非課税世帯でなくなる"])),
 ("五つ目は、そうなると", dict(big=["研究ノート⑤"], color=NAVY, size=100,
                           sub=["家族の保険料・給付金", "およそ2年後に動く"])),
 # ── 7 ○×クイズ ───────────────────────────────────────────────────────────
 ("最後に、○×で", dict(big=["○×3問", "第1問"], color=TEAL,
                     sub=["所得税がかからないなら", "出さなくていい？"])),
 ("所得税がかからなくても、住民税", dict(big=["第1問は×"], color=RED, size=110,
                                  sub=["住民税の控除に使う", "第2問 去年来なかった"])),
 ("送る範囲が、去年の205万円", dict(big=["第2問も×", "148万円以上"], color=RED, circle=True,
                                 sub=["去年は205万円以上", "第3問 期限を過ぎたら？"])),
 ("期限を過ぎたら、もう手遅れ", dict(big=["第3問も×"], color=RED, size=110,
                                sub=["期限後もなるべく早く", "確定申告・住民税申告"])),
 ("三問とも×だったかたは", dict(big=["封筒は", "食卓の上へ"], color=TEAL, sub=["今日のうちに"])),
 ("次の年金支給日の前にも", dict(big=["支給日の前に", "直前チェック"], color=NAVY, sub=["チャンネル登録で"])),
 ("次回は、10月15日", dict(big=["次回", "10月15日"], color=NAVY, sub=["8月と振込額が変わる"])),
 ("なお、今日お伝えした内容は", dict(big=["令和8年9月", "時点の情報"], color=NAVY,
                                sub=["線も額も市区町村で違う"])),
 ("ご自身の分は、市区町村の税の窓口", dict(big=["税の窓口か", "年金事務所で"], color=NAVY,
                                   sub=["また次回の研究で"])),
]


_TAIL = re.compile(r"[、。]")


def _auto(text: str):
    """Rút chữ từ chính lời đọc: mệnh đề CUỐI của câu đầu, chẻ ≤9 ký, ≤2 dòng (như telop29)."""
    s = re.sub(r"^(?:\[[^\]]*\])+", "", text).strip().split("。")[0]
    parts = [p for p in _TAIL.split(s) if p]
    body = parts[-1] if parts else s
    if len(body) < 6 and len(parts) > 1:
        body = parts[-2] + body
    body = body[:18]
    if len(body) <= 9:
        return [body]
    cut = 9
    for i in range(9, max(4, len(body) - 4), -1):
        if body[i - 1] in "はがをにでとのも":
            cut = i
            break
    return [body[:cut], body[cut:18]]


def _build():
    shots = json.loads((VD / "plan31.json").read_text(encoding="utf-8"))["shots"]
    hit = {cue: [k for k, s in enumerate(shots) if cue in s["text"]] for cue, _ in CUES}
    out, taken = {}, set()
    for cue, tel in CUES:
        for k in hit[cue]:
            if k not in taken:
                out[k] = tel
                taken.add(k)
                break
    for k, s in enumerate(shots):
        out.setdefault(k, dict(big=_auto(s["text"]), color=NAVY))
    return out, hit, shots


TELOP, _HIT, _SHOTS = _build()


def _w(s):
    return sum(1.0 if ord(ch) > 0x2000 else 0.55 for ch in s)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    miss = [c for c, ks in _HIT.items() if not ks]
    multi = [(c, ks) for c, ks in _HIT.items() if len(ks) > 1]
    cued = {kk for c, _t in CUES for kk in _HIT[c][:1]}
    nocue = [k for k, s in enumerate(_SHOTS) if re.search(r"[0-9]", s["text"]) and k not in cued]
    longb = [(k, b) for k, t in TELOP.items() for b in t["big"] if _w(b) > 9.0]
    longs = [(k, b) for k, t in TELOP.items() for b in t.get("sub", []) if _w(b) > 14.0]
    many = [k for k, t in TELOP.items() if len(t.get("sub", [])) > 3 or len(t["big"]) > 2]
    arab = sum(1 for t in TELOP.values() if re.search(r"[0-9]", "".join(t["big"] + t.get("sub", []))))
    print(f"ô: {len(TELOP)}/{len(_SHOTS)} · cue {len(CUES)} · tự sinh {len(_SHOTS) - len(cued)}")
    print(f"🔴 cue KHÔNG khớp ô nào: {len(miss)} {miss[:6]}")
    print(f"⚠️ cue khớp NHIỀU ô: {len(multi)} {multi[:4]}")
    print(f"🔴 ô CÓ SỐ mà không có cue: {len(nocue)} {nocue[:12]}")
    print(f"🔴 dòng >9 ký: {len(longb)} {longb[:6]}")
    print(f"🔴 thẻ phụ >14 ký: {len(longs)} {longs[:6]}")
    print(f"🔴 >2 dòng chính / >3 thẻ: {len(many)}")
    print(f"ô có chữ số Ả-rập: {arab}/{len(TELOP)} · ô có thẻ phụ: "
          f"{sum(1 for t in TELOP.values() if t.get('sub'))}/{len(TELOP)}")
    sys.exit(1 if (miss or nocue or longb or longs or many or len(TELOP) != len(_SHOTS)) else 0)
