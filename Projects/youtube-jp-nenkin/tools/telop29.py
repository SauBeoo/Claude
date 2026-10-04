# -*- coding: utf-8 -*-
r"""telop29.py — chữ hiện trên khung cho 95 ô của video 29.

LUẬT VIẾT TELOP (giữ nguyên từ v27/v28, đừng sửa nếu chưa đọc):
  · Chữ rút TỪ CHÍNH lời đọc của ô đó. ⛔ Không thêm số mới, không thêm chế độ mới (YMYL).
  · Dòng chính ≤ 9 ký full-width/dòng, tối đa 2 dòng.
  · `circle=True` chỉ cho dòng CÓ SỐ và chỉ ở khoảnh khắc lật.
  · màu: NAVY mặc định · RED cho mất mát/cảnh báo · TEAL cho phần được/giải pháp.

🔴🔴 KHOÁ THEO **CUE VĂN BẢN**, KHÔNG THEO CHỈ SỐ Ô — bài học phải trả giá hai lần trong
cùng một buổi. Bản đầu của file này viết `OVERRIDE = {0: …, 1: …}` theo chỉ số ô đoán từ cấu
trúc chương; đo lại thì **41/57 entry nằm sai ô**, trôi dần về cuối — tức hơn 2/3 video sẽ hiện
chữ của đoạn khác. Và đúng lỗi này vừa được nêu ra ở `img29_prompts.py` vài giờ trước
(*"chỉ số ô do plan sinh từ timeline, đổi HOLD_TARGET là lệch hết"*), rồi vẫn lặp lại ở đây.
⇒ Cue là một mẩu lời đọc **có thật và duy nhất** trong ô đó; gate ở cuối file bắt cue trượt
hoặc cue khớp nhiều ô.

Phần không có cue → **tự rút từ chính lời đọc** (mệnh đề cuối câu đầu = vị ngữ). Lý do tự sinh:
`build*.py` tra `TELOP[k]` bằng chỉ số trực tiếp, thiếu một ô là **KeyError giữa lượt render**.
🔴 Gate bắt buộc: ô nào lời đọc có CHỮ SỐ mà không có cue ⇒ báo đỏ — bản tự sinh từng cắt
「85歳」 thành 「8」/「5歳」.
"""
import json
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
VD = PROJ / "06_VIDEO" / "29_shikaku-kakuninsho-8gatsu-85sai"

NAVY, RED, TEAL = (31, 56, 100), (192, 57, 43), (62, 124, 120)

# ── cue (mẩu lời đọc DUY NHẤT của ô) → telop. Số đều đã có trong `_TTS.md` ──
CUES = [
 # ── v2 (viết lại 2026-09-24, khuôn SỢ → LÀM → YÊN) — số đều có trong _TTS.md v2 ──
 ("この7月、あなたの家",       dict(big=["3千円が", "3万円に"], color=RED, size=120, circle=True,
                                sub=["7月の封筒の紙1枚で"])),
 ("並んだ人の前で",           dict(big=["カードは", "お持ちですか"], color=RED, sub=["「お預かりできません」"])),
 ("財布に、3万円",            dict(big=["財布に", "3万円ありますか"], color=RED,
                                sub=["分ける線は2本", "85歳と受付の回数"])),
 ("役所は、その回数",          dict(big=["役所は", "回数を数えた"], color=RED, sub=["一部のかたは入院で差"])),
 ("今日は、3つを順番に",        dict(big=["3つを", "確かめます"], color=NAVY,
                                sub=["①どちらの紙か", "②1枚で使えるか", "③空いている欄"])),
 ("封筒を手元に置いて",         dict(big=["封筒を", "手元に"], color=TEAL, sub=["3分で済みます"])),
 ("マイナ保険証を持っていないかた全て", dict(big=["厚生労働省"], color=NAVY, size=110,
                                sub=["申請によらず交付", "マイナ保険証なしの全員"])),
 ("ここで、手元の封筒を",        dict(big=["封筒を", "開けてください"], color=TEAL, sub=["いちばん上の紙の名前"])),
 ("資格確認書と書いてあった",      dict(big=["確認書なら", "ご安心を"], color=TEAL, sub=["1枚でそのまま使えます"])),
 ("資格情報のお知らせと書いて",     dict(big=["お知らせなら", "要注意"], color=RED, sub=["冒頭の受付はあなたの話"])),
 ("普段から機械で済ませて",       dict(big=["紙は要らない", "と判断"], color=TEAL, sub=["普段から機械のかた"])),
 ("先月のある朝",             dict(big=["入れてる", "つもりでした"], color=RED, sub=["受付で財布を開けて"])),
 ("受付のかたに頭を下げて",       dict(big=["往復", "40分"], color=RED, size=120, sub=["団地4階まで取りに"])),
 ("いま、あなたのカードは",       dict(big=["財布を", "開けてください"], color=TEAL, sub=["カードはどこですか"])),
 ("それなら、原田さんのような",     dict(big=["それなら", "大丈夫"], color=TEAL, sub=["ここまでが1本目の線"])),
 ("令和8年8月2日以降に85歳を迎える", dict(big=["8月2日以降", "85歳は"], color=RED, sub=["この理由では交付なし"])),
 ("答えは丸で、保険証として",      dict(big=["丸"], color=TEAL, size=170,
                                sub=["カードだけでよい", "機械不調でも通常負担"])),
 ("はじめて行く病院なら",        dict(big=["初めての病院", "お知らせも"], color=TEAL, sub=["4問目 去年の保険証"])),
 ("四問とも迷わなかった",        dict(big=["4問とも", "迷わなければ"], color=TEAL, sub=["受付で慌てません"])),
 ("冒頭で、もう一つ",           dict(big=["入院で", "大きなお金"], color=RED, sub=["一部のかたは"])),
 ("これに気づいたのは",          dict(big=["小林さん", "75歳"], color=NAVY, sub=["埼玉県川口市"])),
 ("ベランダで朝顔",            dict(big=["住民税", "かかっていない"], color=NAVY, sub=["年金だけで暮らす"])),
 ("この欄が関係するのは",         dict(big=["関係するのは", "全員ではない"], color=RED,
                                sub=["住民税非課税の世帯", "3割負担の一部"])),
 ("一割や二割の負担で",          dict(big=["1割・2割で", "課税のかた"], color=TEAL, sub=["入院の額は変わらない"])),
 ("住民税が非課税のご世帯のかたは、この先", dict(big=["非課税の", "かたは要注意"], color=RED,
                                sub=["マイナ保険証は登録済み"])),
 ("では、あなたの資格確認書のほうは", dict(big=["兵庫県", "広域連合"], color=NAVY, sub=["欄が空欄の場合"])),
 ("その翌週、市役所",           dict(big=["翌週", "申請しました"], color=TEAL, sub=["「慌てなくて済みます」"])),
 ("段階的に変わる途中",          dict(big=["来年また", "動きます"], color=NAVY)),
 ("いちばん下の、限度区分の欄を見て", dict(big=["限度区分の欄", "を見る"], color=TEAL, size=84,
                                sub=["白ければ申請できます"])),
 ("忘れたときに、困らない",        dict(big=["もう40分は", "歩かない"], color=TEAL, sub=["忘れても困らない"])),
 ("二つ目は、8月1日の時点で",      dict(big=["8月1日時点", "85歳以上"], color=NAVY, size=84, sub=["資格確認書が届きます"])),
 ("三つ目は、84歳以下で",         dict(big=["12か月に", "6回以上"], color=RED, size=110, sub=["84歳以下はお知らせ"])),
 ("四つ目は、資格情報のお知らせ",     dict(big=["1枚では", "使えません"], color=RED, sub=["カードと一緒です"])),
 ("五つ目は、住民税が非課税",       dict(big=["白いときは", "申請できます"], color=TEAL, size=84, sub=["非課税世帯などのかた"])),
 ("最後に、ご自分で三つだけ",       dict(big=["封筒は", "どこですか"], color=NAVY, sub=["セルフチェック 3問"])),
 ("二つ目は、出てきた紙の名前",      dict(big=["カードは", "どこですか"], color=NAVY, sub=["3つ目の確認"])),
 ("三つとも答えられた",          dict(big=["3つ答えられたら", "大丈夫"], color=TEAL, sub=["受付で手は止まりません"])),
 ("ご自身の分は、お住まいの広域連合か", dict(big=["また次回の", "研究で"], color=NAVY)),
 ("当研究室は、制度を",       dict(big=["まず、", "事実から"], color=NAVY)),
 ("75歳以上のかたは",       dict(big=["八月から", "分かれました"], color=NAVY)),
 ("手続きをした覚えが",       dict(big=["申請は", "要りません"], color=TEAL)),
 ("去年までの健康保険証",      dict(big=["去年の保険証", "もう使えません"], color=RED,
                                sub=["2025年12月1日で終了"])),
 ("そのかわりに配られていた",   dict(big=["資格確認書", "という紙"], color=NAVY)),
 ("令和8年の7月末まで",      dict(big=["全員に", "一律で"], color=NAVY, sub=["七月末まで"])),
 ("「去年は、黙っていても",     dict(big=["去年は", "そうでした"], color=NAVY)),
 ("暫定的な措置だった",       dict(big=["暫定的な", "措置でした"], color=NAVY)),
 ("そして、その暫定措置が",     dict(big=["八月一日から", "二つに"], color=RED)),
 ("並べてみると",           dict(big=["資格確認書"], color=TEAL, size=120, sub=["一枚で使える"])),
 ("二つ目が、資格情報の",      dict(big=["資格情報の", "お知らせ"], color=RED)),
 ("裏を返せば",            dict(big=["持っている人", "には違う"], color=NAVY)),
 ("これは、あなたの保険の情報",  dict(big=["知らせる", "ための紙"], color=NAVY)),
 ("ですから、一枚では",       dict(big=["カードと", "一緒に出す"], color=TEAL)),
 ("では、どちらが届くのか",     dict(big=["分ける線は", "二本"], color=NAVY)),
 ("団地の四階に",           dict(big=["原田さん", "84歳"], color=NAVY, sub=["月に一度の通院"])),
 ("受付で、いつもマイナンバー",  dict(big=["いつも", "機械にのせて"], color=NAVY)),
 ("小川さんは、どこも",       dict(big=["小川さん", "去年は二回"], color=NAVY)),
 ("よく病院に行っていた",      dict(big=["よく行く人ほど", "使えない紙"], color=RED, size=84)),
 ("過去12か月のあいだに",    dict(big=["12か月に", "6回以上"], color=RED, size=110, circle=True)),
 ("この二つを満たした",       dict(big=["あなたは", "何回でしたか"], color=NAVY)),
 ("ただ、その判断は",        dict(big=["手ぶらで", "出ない前提"], color=RED)),
 ("もう一本、年齢の線",       dict(big=["もう一本", "年齢の線"], color=NAVY)),
 ("令和8年8月1日の時点で85歳以上のかたには、マイナ",
                          dict(big=["8月1日時点で", "85歳以上"], color=NAVY, size=84)),
 ("赤で囲んだところを",       dict(big=["85歳以上は", "無条件"], color=TEAL,
                                sub=["千葉県広域連合"])),
 ("ご自身か、ご家族に",       dict(big=["ご家族に", "いますか"], color=NAVY)),
 ("ところが、その少し下に",     dict(big=["もう一行", "あります"], color=RED)),
 ("もう一度、読みます",       dict(big=["8月1日なら", "届きます"], color=TEAL)),
 ("8月2日に85歳に",       dict(big=["8月2日なら", "届きません"], color=RED, circle=True)),
 ("84歳以下のかたは、さきほど", dict(big=["二本で", "分かれています"], color=NAVY)),
 ("なお、この六回という",      dict(big=["広域連合ごと", "に違います"], color=NAVY, size=84)),
 ("では、ここで四問だけ",      dict(big=["四問だけ"], color=NAVY, size=130)),
 ("答えは丸で、これはそのまま",  dict(big=["丸"], color=TEAL, size=170, sub=["そのまま出せる"])),
 ("答えはばつで、この紙は",     dict(big=["ばつ"], color=RED, size=170, sub=["カードと一緒に"])),
 ("原田さんは、この二問目で",   dict(big=["三問目"], color=NAVY, size=130)),
 ("四問目、去年まで",        dict(big=["ばつ"], color=RED, size=170, sub=["2025年12月1日で終了"])),
 ("うっかり古い保険証を",      dict(big=["特別扱いも", "終わりました"], color=RED, size=84)),
 ("それでは、ここからが",      dict(big=["ここからが", "本題です"], color=NAVY)),
 ("表の下のほうに",          dict(big=["限度区分", "という欄"], color=NAVY)),
 ("昔は、限度額適用認定証",     dict(big=["昔は別の紙", "がありました"], color=NAVY, size=84)),
 ("その認定証は",           dict(big=["認定証は", "廃止されました"], color=NAVY, size=84)),
 ("マイナ保険証のかたは",      dict(big=["手続き不要で", "減額"], color=TEAL, size=84)),
 ("限度区分の欄が空欄で",      dict(big=["申請すると", "記載されます"], color=TEAL, size=84)),
 ("申請していなければ",       dict(big=["申請しなければ", "空いたまま"], color=RED, size=84)),
 ("あとから高額療養費を",      dict(big=["戻っては", "きます"], color=NAVY)),
 ("ですが、戻るまでの",       dict(big=["通帳から", "出たまま"], color=RED)),
 ("小林さんは、封筒を開けて",   dict(big=["いちばん下が", "白かった"], color=RED, size=84)),
 ("申請していないから",       dict(big=["書き忘れでは", "ありません"], color=RED, size=84)),
 ("入院したときの上限額",      dict(big=["上限額も", "見直されました"], color=RED, size=84)),
 ("ご自身の資格確認書の",      dict(big=["いちばん下", "白いですか"], color=RED)),
 ("もし、当日にどうにも",      dict(big=["いったん", "十割"], color=RED, size=130, circle=True)),
 ("ただ、そこで終わりでは",     dict(big=["療養費で", "戻ります"], color=TEAL)),
 ("必要になるのは",          dict(big=["領収書は", "捨てないで"], color=TEAL)),
 ("期限は、診療を受けた",      dict(big=["2年"], color=RED, size=170, circle=True, sub=["翌日から"])),
 ("ここだけは、覚えて",       dict(big=["領収書と", "2年"], color=RED)),
 ("7月に届いた封筒を",       dict(big=["封筒を", "出してください"], color=TEAL)),
 ("お知らせのほうだったら",     dict(big=["カードを", "財布に戻す"], color=TEAL)),
 ("窓口は、後期高齢者医療",     dict(big=["窓口は", "広域連合"], color=TEAL,
                                sub=["年金事務所ではない"])),
 ("原田さんは、あれから",      dict(big=["忘れたときに", "困るから"], color=NAVY, size=84)),
 ("それでは、今日の研究ノート",  dict(big=["今日の", "研究ノート"], color=NAVY)),
 ("次の年金支給日の前にも",     dict(big=["直前チェック", "をお届け"], color=TEAL, size=84)),
 ("なお、今日お伝えした",      dict(big=["令和8年", "9月時点"], color=NAVY)),
]

_TAIL = re.compile(r"[、。]")


def _auto(text: str):
    """Rút chữ từ chính lời đọc: mệnh đề CUỐI của câu đầu (vị ngữ), chẻ ≤9 ký, ≤2 dòng."""
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


# ── LỚP SỐ LIỆU (thêm 2026-09-21, user: "thêm nhiều số liệu và chi tiết hơn") ──
# Đo trên bản trước khi thêm: chỉ **16/93 ô** có chữ số Ả-rập trên màn hình, **15/93** có thẻ
# phụ — trong khi lời đọc đầy số. Hai việc, cả hai lấy TỪ CHÍNH câu đang đọc của ô đó, ⛔ không
# một con số mới nào (YMYL §③ CLAUDE.md):
#   ① **chữ số Ả-rập thay số viết bằng kanji.** 「八月一日」 lên hình đọc ra là CHỮ; 「8月1日」
#      mới nhìn ra là SỐ LIỆU. Đây là lý do v27/v28 trông "nhiều số" hơn v29 dù v29 nói nhiều số
#      hơn — khác nhau ở CÁCH VIẾT, không ở nội dung.
#   ② **thẻ phụ chở chi tiết/số của đúng câu ấy** — chỗ duy nhất trong khuôn này để đặt dữ kiện
#      thứ hai mà không phá trần 9 ký của dòng chính.
# Trần đo trên khung 1920 (đừng nới nếu chưa đo lại):
#   big ≤9 ký (font 108 = size 92 × 1,18 ⇒ 9 ký chạm x≈1.068, mép ảnh phải ~x=1.050)
#   sub ≤14 ký (font 50) · tối đa 3 thẻ (thẻ thứ 3 kết ở y=790, dải phụ đề bắt đầu y=930)
ENRICH = {
 "75歳以上のかたは":       dict(big=["8月から", "分かれました"],
                            sub=["75歳以上のかた", "74歳以下も同じ仕組み"]),
 "手続きをした覚えが":       dict(sub=["自動で分けられました"]),
 "そのかわりに配られていた":   dict(sub=["申請なしで届いていた"]),
 "令和8年の7月末まで":      dict(sub=["令和8年7月末まで", "後期高齢者医療の全員"]),
 "「去年は、黙っていても":     dict(sub=["この夏、窓口で何度も"]),
 "暫定的な措置だった":       dict(sub=["去年の夏も同じ封筒"]),
 "そして、その暫定措置が":     dict(big=["8月1日から", "2つに"], sub=["令和8年7月末で終了"]),
 "並べてみると":          dict(sub=["1枚でそのまま出せる"]),
 "二つ目が、資格情報の":      dict(sub=["名前は似て役割は違う"]),
 "裏を返せば":           dict(sub=["カードありの人は別"]),
 "これは、あなたの保険の情報":  dict(sub=["資格を証明する紙ではない"]),
 "ですから、一枚では":       dict(sub=["1枚では使えません"]),
 "では、どちらが届くのか":     dict(big=["分ける線は", "2本"], sub=["原田さん 84歳 船橋市"]),
 "団地の四階に":          dict(sub=["団地4階", "月に1度の通院"]),
 "受付で、いつもマイナンバー":  dict(sub=["届いたのはお知らせ"]),
 "小川さんは、どこも":       dict(big=["小川さん", "去年は2回"],
                            sub=["同じ階 同じ84歳", "届いたのは資格確認書"]),
 "よく病院に行っていた":      dict(sub=["線はここに引かれた"]),
 "過去12か月のあいだに":     dict(sub=["直近3か月にも実績"]),
 "この二つを満たした":       dict(sub=["2つとも満たすこと"]),
 "ただ、その判断は":        dict(sub=["カードは財布の中ですか"]),
 "もう一本、年齢の線":       dict(big=["もう1本", "年齢の線"], sub=["千葉県広域連合の案内"]),
 "令和8年8月1日の時点で85歳以上のかたには、マイナ":
                        dict(sub=["カードの有無に関わらず"]),
 "ご自身か、ご家族に":       dict(sub=["8月1日時点で85歳"]),
 "ところが、その少し下に":     dict(big=["もう1行", "あります"], sub=["8月2日以降は対象外"]),
 "もう一度、読みます":       dict(sub=["その時点で85歳"]),
 "8月2日に85歳に":       dict(sub=["誕生日が1日違うだけ"]),
 "84歳以下のかたは、さきほど": dict(big=["2本で", "分かれています"],
                            sub=["84歳以下は6回の線", "85歳以上は年齢の線"]),
 "なお、この六回という":      dict(sub=["ご自身の分は窓口で"]),
 "では、ここで四問だけ":      dict(big=["4問だけ"], size=120, sub=["1問目 資格確認書1枚"]),
 "答えは丸で、これはそのまま":  dict(sub=["そのまま出せる", "2問目 お知らせ1枚"]),
 "原田さんは、この二問目で":   dict(big=["3問目"], size=120, sub=["カードだけ 紙は家"]),
 "四問目、去年まで":        dict(sub=["4問目 去年の保険証", "2025年12月1日で終了"]),
 "うっかり古い保険証を":      dict(sub=["令和8年7月31日で終了"]),
 "表の下のほうに":         dict(sub=["入院時のお金を決める"]),
 "昔は、限度額適用認定証":     dict(big=["昔は別の紙", "がありました"], sub=["限度額適用認定証"]),
 "その認定証は":          dict(sub=["いまは欄に書き込む"]),
 "マイナ保険証のかたは":      dict(sub=["区分が登録済み"]),
 "限度区分の欄が空欄で":      dict(sub=["市区町の窓口で"]),
 "申請していなければ":       dict(sub=["入院時は高いほうを払う"]),
 "あとから高額療養費を":      dict(sub=["高額療養費を申請"]),
 "ですが、戻るまでの":       dict(sub=["小林さん 75歳 川口市"]),
 "小林さんは、封筒を開けて":   dict(sub=["「書き忘れかと思って」"]),
 "申請していないから":       dict(sub=["申請していないから白い"]),
 "入院したときの上限額":      dict(sub=["この8月に見直し"]),
 "ご自身の資格確認書の":      dict(sub=["何か書いてありますか"]),
 "もし、当日にどうにも":      dict(big=["いったん", "10割"], sub=["3千円が3万円に"]),
 "ただ、そこで終わりでは":     dict(sub=["自己負担分を除いた額"]),
 "必要になるのは":         dict(sub=["領収書と診療の明細"]),
 "期限は、診療を受けた":      dict(size=120, sub=["診療の翌日から2年", "過ぎると戻りません"]),
 "ここだけは、覚えて":       dict(sub=["ここだけは覚えて"]),
 "7月に届いた封筒を":       dict(sub=["紙の名前を声に出して"]),
 "お知らせのほうだったら":     dict(sub=["今日のうちに"]),
 "原田さんは、あれから":      dict(sub=["カードと2つ折りで重ねて"]),
 "それでは、今日の研究ノート":  dict(sub=["令和8年7月末で終了"]),
 "なお、今日お伝えした":      dict(sub=["運用は広域連合ごと"]),
}

_ck = {c for c, _ in CUES}
assert not (set(ENRICH) - _ck), f"ENRICH co cue khong ton tai: {set(ENRICH)-_ck}"
for _c, _d in CUES:
    _e = ENRICH.get(_c)
    if _e:
        _d.update(_e)


def _build():
    shots = json.loads((VD / "plan29.json").read_text(encoding="utf-8"))["shots"]
    hit, out = {}, {}
    for cue, tel in CUES:
        ks = [k for k, s in enumerate(shots) if cue in s["text"]]
        hit[cue] = ks
    taken = set()
    for cue, tel in CUES:
        for k in hit[cue]:
            if k not in taken:
                out[k] = tel
                taken.add(k)
                break
    for k, s in enumerate(shots):
        if not s["text"].strip():
            # ô CHẺ ĐÔI (plan chẻ ô >18s) — không có lời riêng, lời là của ô trước
            out.setdefault(k, dict(big=["1割ではなく", "10割"], color=RED, size=120,
                                   sub=["いったん全額のことも"]) if k == 1 else
                           dict(big=out.get(k - 1, {}).get("big", [""]), color=NAVY))
        out.setdefault(k, dict(big=_auto(s["text"]), color=NAVY))
    return out, hit, shots


TELOP, _HIT, _SHOTS = _build()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    miss = [c for c, ks in _HIT.items() if not ks]
    multi = [(c, ks) for c, ks in _HIT.items() if len(ks) > 1]
    nocue = [k for k, s in enumerate(_SHOTS)
             if re.search(r"[0-9]", s["text"]) and k not in
             {kk for c, _t in CUES for kk in _HIT[c][:1]}]
    print(f"ô: {len(TELOP)} · cue {len(CUES)} · tự sinh {len(TELOP)-len(CUES)+len(miss)}")
    print(f"🔴 cue KHÔNG khớp ô nào: {len(miss)}")
    for c in miss[:10]:
        print(f"     «{c}»")
    print(f"⚠️ cue khớp NHIỀU ô: {len(multi)}")
    for c, ks in multi[:6]:
        print(f"     «{c}» -> {ks}")
    print(f"🔴 ô CÓ SỐ mà không có cue: {len(nocue)} {nocue[:12]}")
    over = [k for k, v in TELOP.items() if any(len(x) > 9 for x in v["big"])]
    print(f"🔴 dòng >9 ký: {len(over)} {over[:8]}")
