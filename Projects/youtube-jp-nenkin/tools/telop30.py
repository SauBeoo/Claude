# -*- coding: utf-8 -*-
r"""telop30.py — chữ hiện trên khung cho 98 ô của video 30 (10月15日の年金振込).

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
VD = PROJ / "06_VIDEO" / "30_nenkin-furikomi-10gatsu-fueru-hito"

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)

CUES = [
 # ── 0 はじめに ─────────────────────────────────────────────────────────
 ("10月15日の朝。あなたが通帳", dict(big=["10月15日", "振込が減る"], color=RED, size=110, circle=True,
                                  sub=["8月より1万6千円以上"])),
 ("年金が、こっそり減らされた", dict(big=["犯人は", "だれ？"], color=RED,
                                 sub=["①年金が減らされた？", "②はがきの間違い？", "③詐欺？"])),
 ("しかも同じ朝、別のお宅", dict(big=["別の家では", "9,600円増"], color=TEAL, circle=True,
                               sub=["同じ10月15日の朝"])),
 ("ところが、そのほっとした", dict(big=["来年10月に", "もう一度驚く"], color=RED, sub=["増えたかたのほう"])),
 ("答えは、7月ごろに", dict(big=["7月の紙に", "もう書いてある"], color=NAVY, sub=["見るのは3つの場所"])),
 ("その三つ目には", dict(big=["3つ目に", "今年だけの言葉"], color=RED, sub=["去年までの紙になかった"])),
 ("65歳以上のかたなら", dict(big=["65歳以上の", "かたへ"], color=NAVY, sub=["年金から介護保険料"])),
 ("あなたの数字を計算する研究室", dict(big=["疑わしいものを", "1つずつ消す"], color=NAVY,
                                  sub=["あなたの数字を計算"])),
 # ── 1 3つの容疑者 ───────────────────────────────────────────────────────
 ("一つ目の容疑者は", dict(big=["容疑者①", "年金そのもの"], color=NAVY, sub=["減らされた？→違います"])),
 ("年金の額が変わるのは", dict(big=["額が変わるのは", "4月分から"], color=NAVY,
                            sub=["4月分・5月分は6月に", "容疑者② 役所の間違い"])),
 ("6月に届いた、年金振込通知書", dict(big=["6月の", "振込通知書"], color=NAVY,
                                  sub=["10月の額も書いてあった"])),
 ("こちらが、日本年金機構のページ", dict(big=["日本年金機構"], color=NAVY, size=100,
                                   sub=["8月以降は予定額", "6月の額を記載"])),
 ("決定額は、市区町村から", dict(big=["決定額は", "市区町村から"], color=NAVY,
                              sub=["送付される通知書で確認"])),
 ("つまり、6月の紙の10月の欄", dict(big=["10月の欄は", "仮の数字"], color=TEAL, sub=["間違いではありません"])),
 ("振込の額が変わるかたには", dict(big=["詐欺でも", "ありません"], color=TEAL,
                                sub=["振込通知書があらためて届く", "何も求められていない"])),
 ("では、本当の犯人は", dict(big=["本当の犯人は", "引く時期"], color=RED, sub=["年金から引く介護保険料"])),
 ("介護保険料は、1年を前半と後半", dict(big=["前半", "4月・6月・8月"], color=NAVY,
                                   sub=["1年を前半と後半に分ける"])),
 ("10月、12月、2月が後半", dict(big=["後半", "10月・12月・2月"], color=NAVY, sub=["前半3回はいくら？"])),
 ("こちらが、世田谷区の", dict(big=["世田谷区の", "案内"], color=NAVY, sub=["仮徴収期間 4・6・8月"])),
 ("原則として、前年度の2月と同じ", dict(big=["前半3回は", "去年の値段"], color=RED,
                                  sub=["前年度2月と同じ金額", "4月〜8月"])),
 ("今年の値段が決まるのは、7月", dict(big=["7月に", "今年の値段"], color=NAVY,
                                 sub=["10月からの3回で", "残りを3で割って合わせる"])),
 ("町内のバス旅行", dict(big=["バス旅行の", "積立金"], color=NAVY, sub=["幹事さんが一軒ずつ"])),
 ("行き先が決まる前は", dict(big=["まず去年と", "同じ額"], color=NAVY,
                          sub=["足りなければ足す", "多すぎれば減らす"])),
 ("介護保険料の10月は、ちょうど", dict(big=["10月は", "精算の日"], color=RED, sub=["犯人はカレンダー"])),
 # ── 2 減る側 中村さん ───────────────────────────────────────────────────
 ("では、この精算で", dict(big=["まず", "減る側"], color=RED, sub=["中村さん 上越市"])),
 ("71歳、おひとり暮らし", dict(big=["3万9,500円", "→8万9,100円"], color=RED, size=84,
                             sub=["中村さん 71歳", "今年から住民税がかかる"])),
 ("前半の3回は、去年の値段のまま", dict(big=["上がった分は", "後半3回に"], color=RED,
                                  sub=["8月の振込 約24万3千円"])),
 ("10月は、およそ22万7千円", dict(big=["1万6,500円", "少ない"], color=RED, size=110, circle=True,
                              sub=["10月 約22万7千円"])),
 # ── 3 増える側 加藤さん ─────────────────────────────────────────────────
 ("では、反対に増える側", dict(big=["増える側", "加藤さん"], color=TEAL,
                            sub=["72歳 新潟市", "年金 年132万円"])),
 ("1回の振込は、22万円", dict(big=["1回", "22万円"], color=NAVY,
                            sub=["次男と2人暮らし", "3月末 次男が東京へ"])),
 ("住民票も、東京へ移して", dict(big=["住民票も", "東京へ"], color=NAVY, sub=["ご飯はつい3合"])),
 ("次男が出ていくと", dict(big=["変わるのは", "保険料の段階"], color=RED,
                         sub=["前の年の収入", "4月1日の世帯"])),
 ("去年度は、住民税を払う次男", dict(big=["去年度", "第5段階"], color=RED, sub=["年8万2,500円"])),
 ("今年度は、4月1日の時点で", dict(big=["今年度", "第3段階"], color=TEAL,
                              sub=["年5万3,700円", "4月1日にひとり世帯"])),
 ("こちらが、新潟市の、介護保険料の表", dict(big=["新潟市の", "保険料の表"], color=NAVY,
                                     sub=["第3段階 5万3,700円", "第5段階 8万2,500円"])),
 ("ところが、春から夏まで", dict(big=["春〜夏は", "1万3,750円"], color=RED, sub=["前年度最後の回と同じ"])),
 ("値段が下がったことは", dict(big=["下がった値段は", "まだ届かない"], color=NAVY,
                            sub=["明細を並べてみます"])),
 ("8月は、22万円から", dict(big=["8月", "20万6,250円"], color=NAVY, sub=["22万円−1万3,750円"])),
 ("10月は、1年分の5万3千700円", dict(big=["10月は", "1回4,150円"], color=TEAL,
                                  sub=["5万3,700−4万1,250", "残りを3回に"])),
 ("手元に入るのは、21万5千850円", dict(big=["9,600円", "多く入る"], color=TEAL, size=110,
                                   circle=True, sub=["10月 21万5,850円"])),
 ("「息子がいなくなって", dict(big=["「保険料まで", "変わるなんて」"], color=NAVY,
                            sub=["年金が上がったと思った"])),
 ("では、年金は上がったのでしょうか", dict(big=["年金は", "上がっていない"], color=NAVY,
                                    sub=["変わったのは引かれる側", "12月も2月も4,150円"])),
 ("同じ新潟県で、同じ10月15日", dict(big=["少ない人と", "多い人"], color=NAVY,
                                 sub=["年金は1円も変わらない"])),
 ("ただ、この話には", dict(big=["この話には", "続きがある"], color=RED, sub=["ほっとしたかたが来年"])),
 ("それは、今日の最後に", dict(big=["1年先の数字は", "最後に"], color=NAVY, sub=["今日は介護保険料だけ"])),
 ("国民健康保険料や端数", dict(big=["市区町村で", "変わります"], color=NAVY, sub=["国保・端数・8月の調整"])),
 # ── 4 あなたの紙 3つの場所 ──────────────────────────────────────────────
 ("では、あなたは、どちらの側", dict(big=["あなたは", "どちらの側？"], color=NAVY,
                                 sub=["7月ごろの紙を出して"])),
 ("名前は、決定通知書だったり", dict(big=["場所①", "10月の欄"], color=NAVY,
                               sub=["決定通知書・確定通知書", "月ごとの表"])),
 ("あなたの10月の欄には", dict(big=["8月と", "比べる"], color=NAVY,
                             sub=["小さい→加藤さんの側", "大きい→中村さんの側"])),
 ("減る側だと分かったかたも", dict(big=["慌てなくて", "大丈夫"], color=TEAL,
                               sub=["1年分は7月に決まった", "余計に取られていない"])),
 ("その差が、そのまま", dict(big=["その差が", "振込の増減"], color=NAVY, sub=["10月の振込で"])),
 ("住民税や医療の保険料も", dict(big=["場所②", "段階の欄"], color=NAVY, sub=["住民税・医療も同じく比べる"])),
 ("あなたは、第何段階", dict(big=["第何段階", "でしたか"], color=NAVY,
                          sub=["前の年の収入", "4月1日の世帯"])),
 ("4月2日より後に", dict(big=["場所③", "課税の欄"], color=RED, sub=["4月2日以降は変わらない"])),
 ("あなたや、同じ世帯のご家族が", dict(big=["今年だけ", "見方が違う"], color=RED,
                                  sub=["住民税を払っているか"])),
 ("ここで、ひとつだけお願い", dict(big=["高評価と", "シェアを"], color=TEAL, sub=["ご家族・ご友人へ"])),
 ("ご感想や、調べてほしい", dict(big=["コメントで", "お寄せください"], color=TEAL, sub=["次の研究テーマに"])),
 # ── 5 今年だけ みなし課税 ───────────────────────────────────────────────
 ("冒頭でお約束した、去年までの紙", dict(big=["課税の欄に", "見慣れない言葉"], color=RED,
                                   sub=["なぜ今年だけ？"])),
 ("パートなどの給料から", dict(big=["55万円→", "65万円"], color=NAVY, size=110,
                            sub=["給料から引ける最低額", "住民税がかからない人も"])),
 ("ところが、介護保険料は、3年", dict(big=["保険料は", "3年ごと"], color=NAVY, sub=["令和6〜8年度"])),
 ("その途中で、住民税のかからない", dict(big=["国は", "施行令を改めた"], color=NAVY,
                                   sub=["保険料の収入が足りない"])),
 ("令和8年度の介護保険料に限っては", dict(big=["令和8年度", "だけ"], color=RED, sub=["前のルールで判定"])),
 ("対象は、去年の給料が", dict(big=["55万1千円〜", "190万円未満"], color=RED, size=84,
                            sub=["去年の給料", "同じ世帯の家族も"])),
 ("東京都の練馬区", dict(big=["練馬区の例", "給料110万円"], color=NAVY, size=84,
                       sub=["今のルール 所得45万円", "区民税はかからない"])),
 ("ところが、前のルールで計算", dict(big=["前のルールで", "所得55万円"], color=RED,
                                sub=["保険料は課税の段階"])),
 ("その印が、紙のどこに", dict(big=["新潟市の", "ページ"], color=NAVY, sub=["みなし課税"])),
 ("市民税が非課税でも", dict(big=["みなし", "課税"], color=RED, size=120, sub=["保険料では課税とみなす"])),
 ("住民税は下がったのに", dict(big=["住民税↓でも", "保険料は下がらない"], color=RED,
                            sub=["課税の欄をもう一度"])),
 ("ご自分は年金だけで", dict(big=["家族のパートが", "響くことも"], color=RED,
                          sub=["同じ世帯の子・配偶者"])),
 ("ここで、救いが一つ", dict(big=["救いが", "1つ"], color=TEAL,
                          sub=["去年度も非課税なら", "非課税の段階のまま"])),
 ("新潟市では、非課税特例", dict(big=["非課税特例", "申請不要"], color=TEAL, sub=["新潟市の書きかた"])),
 ("ご本人にも、同じ世帯", dict(big=["給料がなければ", "関係なし"], color=TEAL, sub=["本人も家族も"])),
 ("そして、この扱いは、今年度", dict(big=["令和8年度", "だけ"], color=NAVY,
                                sub=["書きかたは市区町村で違う"])),
 ("みなし課税という言葉を使わない", dict(big=["介護保険の", "窓口で確認"], color=NAVY,
                                   sub=["言葉を使わない所も"])),
 # ── 6 来年の10月 ───────────────────────────────────────────────────────
 ("では最後に、冒頭の", dict(big=["なぜ来年", "もう一度驚く？"], color=RED)),
 ("加藤さんの数字で、1年先", dict(big=["1年先を", "計算"], color=NAVY, sub=["来年4月・6月・8月"])),
 ("前半の3回は、今年の2月と同じ額", dict(big=["来年前半", "4,150円"], color=TEAL,
                                   sub=["今年の2月と同じ額"])),
 ("つまり、来年の春から夏は", dict(big=["来年の春夏は", "多く入る"], color=TEAL)),
 ("では、来年も、1年分が", dict(big=["前半で払うのは", "1万2,450円"], color=NAVY, size=84,
                             sub=["1年分5万3,700円なら"])),
 ("残りを後半の3回で割ると", dict(big=["後半1回", "1万3,750円"], color=RED, sub=["残りを3回で割る"])),
 ("来年の10月の振込は", dict(big=["来年10月", "9,600円減"], color=RED, size=110, circle=True,
                           sub=["8月より少なくなる"])),
 ("今年の10月に増えた額と", dict(big=["向きが", "逆になる"], color=NAVY,
                              sub=["1年分は変わらない", "変わるのは払う時期"])),
 ("それでも、通帳を見る朝", dict(big=["通帳の朝に", "そのまま届く"], color=NAVY, sub=["増えた・減った"])),
 ("市区町村によっては、6月や8月", dict(big=["差を小さくする", "市区町村も"], color=NAVY,
                                   sub=["6月・8月で調整"])),
 ("この話を聞いて、カレンダー", dict(big=["来年10月に", "9,600円"], color=TEAL, circle=True,
                                sub=["鉛筆で書き込んだ"])),
 ("「年金が増えたんじゃなくて", dict(big=["払いすぎた分が", "戻っていた"], color=TEAL,
                                 sub=["10月の朝が少し静かに"])),
 # ── 7 研究ノート ───────────────────────────────────────────────────────
 ("それでは、今日の研究ノート", dict(big=["研究ノート①"], color=NAVY, size=100,
                                sub=["4・6・8月は去年の値段", "10・12・2月で合わせる"])),
 ("二つ目は、10月の振込の増減", dict(big=["研究ノート②"], color=NAVY, size=100,
                                 sub=["増減＝8月と10月の差"])),
 ("三つ目は、段階が", dict(big=["研究ノート③"], color=NAVY, size=100, sub=["前の年の収入", "4月1日の世帯"])),
 ("四つ目は、令和8年度に限り", dict(big=["研究ノート④"], color=NAVY, size=100,
                                sub=["令和8年度に限り", "55万1千〜190万円未満", "課税とみなされることも"])),
 ("五つ目は、今年の10月に", dict(big=["研究ノート⑤"], color=NAVY, size=100,
                              sub=["今年増えたかたは", "来年10月に同じだけ減る"])),
 # ── 8 やること3つ ──────────────────────────────────────────────────────
 ("今日から、三つだけ", dict(big=["やること①"], color=TEAL, size=100,
                          sub=["8月と10月の欄の差", "余白に書く"])),
 ("二つ目は、課税の欄に", dict(big=["やること②③"], color=TEAL, size=100,
                            sub=["課税の欄の言葉を確認", "差を来年10月に書く"])),
 ("10月15日の朝、通帳の数字", dict(big=["10月15日", "差だけ動けば"], color=TEAL, sub=["それで正解"])),
 ("次の年金支給日の前にも", dict(big=["支給日の前に", "直前チェック"], color=NAVY, sub=["チャンネル登録で"])),
 ("次回は、12月15日", dict(big=["次回", "12月15日"], color=NAVY, sub=["所得税の精算で動く額"])),
 ("なお、今日お伝えした内容は", dict(big=["令和8年9月", "時点の情報"], color=NAVY,
                                sub=["額・段階は市区町村で違う"])),
 ("ご自身の分は、市区町村の窓口", dict(big=["窓口か", "年金事務所で"], color=NAVY,
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
    shots = json.loads((VD / "plan30.json").read_text(encoding="utf-8"))["shots"]
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
