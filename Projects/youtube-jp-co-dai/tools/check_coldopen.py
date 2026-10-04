# -*- coding: utf-8 -*-
r"""GATE COLD OPEN co-dai — CỬA SỔ GIÂY 0–45, nhắm AVD 60% (viết lại 2026-08-11).

    python tools\check_coldopen.py            # quét 03_SCRIPTS/*_TTS.md
    python tools\check_coldopen.py 14          # chỉ script chỉ định
    python tools\check_coldopen.py --all       # quét cả 07_UPLOADED (lấy bằng chứng / hiệu chuẩn)

════════════════════════════════════════════════════════════════════════════════
🔴 VÌ SAO VIẾT LẠI — BẢN CŨ CANH SAI CỬA VÀ TRẢ SỐ RÁC
════════════════════════════════════════════════════════════════════════════════

Bản cũ (2026-07-30) đo MỘT thứ: "chương/mẹo đầu tiên vào ≤75 giây". Đo retention
thật bằng Analytics API 2026-08-11 (`CHANNEL_DIAGNOSIS_2026-08-11.md`) cho thấy nó
canh cánh cửa nằm SAU chỗ khán giả đã chết:

  video          @15s    @30s    @45s   │ AVD     relPerf 60s đầu
  01 シロアリ     100%    50,0%   41,7%  │ 31,15%  0,38–0,46
  02 蚊の庭       88,9%   61,1%   50,0%  │ 22,38%  0,17–0,25
  07 すだれ       88,2%   52,9%   41,2%  │ 12,12%  0,25–0,38

**Gần như KHÔNG ai bỏ đi trong 15 giây đầu** (88–100%) ⇒ toàn bộ cú giết gói trong
~30 giây sau đó, mất nhiều điểm hơn cả 20+ phút còn lại.

Hai bằng chứng bản cũ không dùng được:
  ① Nó chấm video 07 là script TỐT NHẤT (~100s) — mà 07 là video retention TỆ NHẤT
     (12,12%). Gate xếp hạng NGƯỢC với thực tế đo được.
  ② `ITEM` không biết câu chuyển hiện hành 「さて、ここからが今日の核心です。」 nên
     3/6 script tồn kho báo ~1134–1189 giây (thật: 135–194 giây). Gate trả số vô
     nghĩa thì sẽ bị bỏ qua — đúng bệnh "luật kiểm bằng mắt thì sẽ trôi".

Đọc đúng giây 22–45 của video 07 (bản tệ nhất) thì thấy lỗi là gì:
  19,2s  熱のうち、およそ7割は、窓や開口部から入ってきます   ✅ fact mạnh nhất
  22,2s  住宅の断熱を調べた業界の試算です                    ❌ gán nguồn, 0 tin mới
  24,9s  壁でも、屋根でもなく、窓です                        ❌ nhắc lại lần 2
  30,0s  内側から布をかぶせても、熱はもう部屋の中に…         ❌ nhắc lại lần 3
  34,7s  そこで今日、いちばん先にお話しするのは、この二つです ❌ MỤC LỤC
Từ giây 22 → 45 KHÔNG có một thông tin mới nào. Đó là chỗ đường cong sụp.

⭐ Luật 15 giây đầu (2026-07-21, "stake + con số tiền nổ trong ~84 ký") ĐÃ CHẠY —
chính nó giữ 88–100% ở giây 15. Bản này XÂY TIẾP lên nó (O7), KHÔNG đảo nó.

⚠️ **KHÔNG copy nguyên R3b của chouhen** (`youtube-jp-chouhen/tools/check_retention.py`):
ở đó luật là "0 câu LỜI KỂ ≥25 ký trong giây 16–35" vì chouhen là drama CÓ THOẠI.
co-dai là kênh tài liệu — toàn bộ bài là lời kể ⇒ áp y nguyên sẽ fail 100% script.
Cái mượn từ chouhen là **cửa sổ giây + cơ chế hard-fail + khuôn in row()**, không
phải luật.

════════════════════════════════════════════════════════════════════════════════
🎯 MỤC TIÊU AVD 60% (user chốt 2026-08-11) — SỐ HỌC CỦA NÓ
════════════════════════════════════════════════════════════════════════════════

`AVD% ≈ chiều cao TRUNG BÌNH của đường cong retention`. Nên trước khi siết luật,
đã tích phân hình thang 3 đường cong thật để trả lời: *"nếu CHỈ cắt video ngắn thì
AVD được bao nhiêu?"*

  cắt tại │ 01 シロアリ │ 02 蚊の庭 │ 07 すだれ
    5′    │   45,0%    │   35,7%   │   36,7%
   12′    │   38,9%    │   24,8%   │   29,3%
   18′    │   37,0%    │   23,8%   │   23,8%
  nguyên  │   32,9%    │   25,1%   │   19,4%

🔴 **Cắt xuống 5 PHÚT vẫn chỉ 45%.** Vì đường cong đã tụt còn 50% ở giây 30–45 nên
mọi cửa sổ bắt đầu từ 0 đều bị cái vách đó kéo xuống. Độ dài đáng **+6 điểm**, không
phải +28 ⇒ **60% được mua TRỌN trong 45 giây đầu, KHÔNG mua bằng độ dài.**
(Khớp `CHANNEL_DIAGNOSIS_2026-08-11.md` §1e: benchmark median 21,9′ vẫn ăn 341K view
⇒ độ dài không phải biến. Hai kết luận này CÙNG CHIỀU, không mâu thuẫn.)

**Hai con số phải đạt để có 60%:**
  ① **@45s ≥ 85%**   (nay 41,2–50,0%)  ← đắt nhất, ăn ~+25 điểm AVD
  ② **sàn thân bài ≥ 55%** (nay tụt 41,7% @3′ → 33,3% @10′ → 16,7% @20′)

⚠️ **60% là mốc CHƯA có tiền lệ trong workspace** — cao nhất từng đo là chouhen video
12: **51,6% lifetime / 55,7% ngày 1**, và đó là DRAMA (lực kéo tự truyện). Kênh tài
liệu không có lực đó. Mốc chặng: **40% → 50% → 60%**; 3 video liên tiếp ≤30% thì mốc
60% sai với ngách này, mổ lại chứ đừng vá tiếp.

════════════════════════════════════════════════════════════════════════════════
BỘ LUẬT (siết theo mục tiêu 60% — cửa sổ mở rộng 15–45 → 0–45)
════════════════════════════════════════════════════════════════════════════════
  ── nhóm ① @45s ≥85% ────────────────────────────────────────────────────────
  O1 🔴 mẹo/hành động đầu tiên vào ≤30s (168 ký)      ← siết từ 45s; cũ là 75s
  O2 🔴 giây 0–45: 0 câu MỤC LỤC / tuyên bố            (câu giết 07 ở giây 34,7)
  O3 🔴 giây 0–45: 0 câu GÁN NGUỒN / nhắc lại          (khối 原典 thuộc THÂN BÀI)
  O4 🔴 câu chào 「古代の秘訣」 phải nằm SAU mẹo 1      ← nâng từ WARN lên FAIL
  O5 🔴 60s đầu: 0 câu miễn trừ / dặn dò an toàn        (giữ nguyên L2 cũ, đang đúng)
  O6 🔴 giây 0–45: ≤1 câu KHÔNG TRẢ TIỀN               ⭐ luật lõi của mốc 60%
  O7 🟡 stake + con số trong ~84 ký đầu (15s)          (giữ luật 2026-07-21)
  ── nhóm ② sàn thân bài ≥55% ────────────────────────────────────────────────
  O9 🔴 gap giữa 2 payoff ≤2′30″ xuyên thân bài        (mượn R7 chouhen)
  O10 🟡 tuyên bố "mẹo mạnh nhất để CUỐI" trong 60s đầu

⭐ **O6 là luật lõi.** "Trả tiền" = câu có ≥1 trong **NĂM đồng tiền**: ① con số/đơn vị
MỚI ② động tác ③ từ nghịch lý (ところが/じつは/逆に…) ④ **nhập giác quan** (羽音/ぬめり/
思い浮かべ…) ⑤ **câu hỏi kéo người xem vào** (〜ませんか/〜でしょうか). Video 07 có 4 câu
liên tiếp không trả tiền ở giây 22–45 (3 câu nhắc lại + 1 mục lục) — đúng chỗ đường cong
sụp. Trần 1 câu = cho phép đúng một câu cầu nối, không hơn.

🔴 **④ và ⑤ được thêm KHI HIỆU CHUẨN, không phải lúc thiết kế** — bản đầu chỉ có ①②③ và
nó xếp video 02 (AVD 22,38%) là 8 câu không-trả-tiền, TỆ HƠN video 07 (AVD 12,12%, 6 câu)
= **ngược với retention thật**. Sửa xong: 02 = 3 câu · 07 = 6 câu ⇒ đúng chiều. Đây là lý
do bước `--calib` là bắt buộc: gate cũ chết vì chưa ai đối chiếu nó với số thật lần nào.

⭐ **O9 là luật của SÀN.** chouhen đo được: MỌI hố retention của video 09 nằm trong một
gap ≥3′26″ (khớp 5/5). Đoạn dài không có số/động tác mới = một cái hố, bất kể viết hay.
Hai khối "giảng" của kênh (原典 + dòng tiền) nằm liền nhau là cách chắc chắn nhất để
tạo hố ⇒ đừng xếp cạnh nhau.

⭐ **O2/O3/O6 đo TRỰC TIẾP cửa sổ giây nên KHÔNG phụ thuộc vào việc dò được O1.**
Đó là chủ ý: bản cũ chết vì mọi luật đều treo vào một cái regex dò nhãn vào bài.
Dò không ra nhãn thì O1 in "KHÔNG DÒ ĐƯỢC", các luật còn lại vẫn chấm được.

🔴 O1 dò nhãn theo THỨ TỰ ƯU TIÊN: marker tay → câu chỉ dẫn 〜てください → nhãn
liệt kê 一つ目/まず → 第◯章 → 「さて、ここからが今日の核心」 → bước làm 〜ます.
Cách chắc chắn nhất vẫn là **đặt tay `<!-- GATE:本編 -->`** ngay trên dòng vào bài.
⚠️ Cố ý KHÔNG dò động từ ở thể thường (エアコンをつける。) — đó là câu TẢ việc người
ta đang làm SAI, không phải chỉ dẫn cho người xem; dòng 1 của video 07 chứa 「閉めて」
nên regex lỏng sẽ chấm sai giây 0 là "đã vào bài".

Exit code 1 nếu có FAIL → nhét được vào .cmd/pipeline.
"""
import re
import sys
from pathlib import Path

# audience-45plus.md §2.0h: gate crash on cp1252 console => builder prints RED on a clean
# project. reconfigure() instead of wrapping stdout (2026-09-06).
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CPS = 5.625                      # 337,5 ký/phút — đo thật 2026-07-13 (CLAUDE.md ô C)
LIMIT_S = 30                     # O1: trần vào bài (75 → 45 → 30, siết theo mốc 60%)
LIMIT = int(LIMIT_S * CPS)       # 168 ký
WIN = (0, 45)                    # O2/O3/O6: cửa mua 60% AVD
HEAD60 = int(60 * CPS)           # O5: vùng cấm miễn trừ = 337 ký
STAKE_N = int(15 * CPS)          # O7: 84 ký đầu
FREE_MAX = 1                     # O6: trần câu KHÔNG TRẢ TIỀN trong cửa sổ
GAP_MAX = 150                    # O9: gap payoff tối đa = 2′30″ (mượn R7 chouhen)
PROJ = Path(r"E:\Claude\Projects\youtube-jp-co-dai")

MARKER = "<!-- GATE:本編 -->"

# ── O1 · nhãn VÀO BÀI ────────────────────────────────────────────────────────
# Chỉ dẫn cho NGƯỜI XEM (〜てください). Trừ các cụm chỉ là phép lịch sự/miễn trừ.
TELL = re.compile(r"(?:て|で)ください")
TELL_DENY = ("お使いください", "ご相談ください", "ご覧ください", "聞いてください",
             "教えてください", "ご注意ください", "控えてください", "お待ちください")
# Nhãn liệt kê / chương / câu chuyển chuẩn của kênh
ENUM = re.compile(
    r"^(?:さて[、,]?\s*)?(?:一つ目|ひとつ目|1つ目|その1|その一)"
    r"|^第[一二三四五六1-9]章"
    r"|^(?:では|それでは)[、,]?\s*(?:作り方|やり方|仕掛け|手順)"
    r"|^まず(?:は)?[、,]?\s*(?:容器|バケツ|用意|材料|準備|乾いた)"
    r"|^.{0,14}知恵の中身に入"
    r"|^では[、,]?\s*どうすれば"
    # ⭐ O8 — câu chuyển HIỆN HÀNH của kênh (script 09–13 dùng, bản cũ KHÔNG biết
    #    → báo 1134s trong khi thật là 153s). Đây chính là bug làm gate mất tin cậy.
    r"|^さて[、,]?\s*ここからが(?:今日の)?核心")
# Bước làm dạng 〜ます kèm danh từ dụng cụ/vật (「ぬるま湯を4リットルほど入れます」)
STEP = re.compile(r"(?:を|に|で|から)[^。]{0,24}"
                  r"(?:入れ|置き|開け|かけ|巻き|吊り|貼り|混ぜ|流し|撒き|拭き|挟み|"
                  r"沈め|加え|溶かし|外し|閉め|向け|休ませ|さし)ます")

# ── O2 · câu MỤC LỤC / tuyên bố (ăn giây mà không trả gì) ────────────────────
TOC = [
    re.compile(r"今日(?:は|、)?.{0,24}(?:お話し|ご紹介|お伝え|見ていき)"),
    re.compile(r"お話しするのは"),
    re.compile(r"ご紹介します"),
    re.compile(r"この(?:二|三|四|五|六|ふた|みっ)つ(?:です|を)"),
    re.compile(r"(?:一|二|三|四|五|六|\d)つ(?:を|、)?\s*(?:お話し|ご紹介|お伝え)"),
    re.compile(r"この動画では"),
    re.compile(r"最後までご覧"),
]
# ── O3 · gán nguồn / nhắc lại (đúng, nhưng thuộc THÂN BÀI) ───────────────────
CITE = ["試算", "と言われています", "が知られています", "という報告", "調査によ",
        "研究によ", "データによ", "とされています", "統計", "によれば", "の報告では"]

# ── O5 · miễn trừ / dặn dò an toàn ───────────────────────────────────────────
DISC = ["お断り", "ご注意", "注意してください", "熱中症", "エアコンをお使いください",
        "我慢するための話ではありません", "医師", "主治医", "ご相談", "自己責任",
        "換気を", "火気", "お薬", "控えてください", "禁物", "アレルギー", "妊娠"]

CHAN = "古代の秘訣"
# ── O6/O7 · con số + đơn vị (kịch bản kênh dùng chữ số Ả Rập — CLAUDE.md §💴) ─
NUM = re.compile(r"\d+(?:\.\d+)?\s*(?:円|℃|度|割|%|パーセント|分|秒|時間|日|枚|本|杯|"
                 r"リットル|ミリ|センチ|メートル|グラム|倍|年|人|回|個|袋|匹|時|"
                 # ⭐ thêm 2026-08-11 lúc hiệu chuẩn: thiếu 種類 làm 「たった10種類の植物」
                 #    của video 02 bị chấm là "không trả tiền" — trong khi đó chính là
                 #    lời hứa trung tâm của bài. Bỏ sót đơn vị = chấm oan.
                 # ⭐ thêm 2026-09-04 (script 29 包丁・砥石): thiếu 番 (số hiệu hạt mài
                 #    của砥石), 歳 và キロ làm CHÍNH những câu chở thông tin đắt nhất bị
                 #    chấm "không trả tiền": 「中砥石が600番から2000番」 (người xem cần đúng
                 #    con số này để đi mua đá) và 「30歳代で46キロ」 (số スポーツ庁 làm stake).
                 #    Cùng loại lỗi với 種類 ở lần hiệu chuẩn 2026-08-11 — BỎ SÓT ĐƠN VỊ =
                 #    CHẤM OAN. `\d+\s*番` chỉ khớp sau chữ số nên KHÔNG đụng 番茶/一番/交番.
                 # ⭐ thêm 2026-09-06 (04_FORMULA, sau khi rà 7 video): thiếu 月 và 冊 làm
                 #    「8月は74パーセント」/「1月は51パーセント」 (cú lật của #30) và 「11巻」
                 #    kiểu #20 bị chấm oan. `\d+\s*月` chỉ khớp sau chữ số nên KHÔNG đụng 月曜.
                 r"種類|種|通り|パターン|か月|ヶ月|週間|滴|つまみ|番|歳|キロ|キログラム|月|冊)")
MONEY = re.compile(r"数百円|数千円|ワンコイン|\d+\s*円|0\s*円|無料|タダ")
# 🔴 O7 NOI LONG 2026-08-11 — ban dau doi CON SO TIEN trong 84 ky dau. Bang chung
#    KHONG chong do dieu do: cold open video 02 la mot CANH GIAC QUAN thuan
#    (「夏の夕暮れを思い浮かべて」「耳元で響く羽音もない」) — KHONG mot con so nao —
#    ma giu 88,9% @15s, cao hon ca video 07 (co san 3000円/7割 ngay dau).
#    ⇒ Thu 15 giay dau can la STAKE CU THE CUA NGUOI XEM, tra bang so tien HOAC
#    bang canh giac quan/hau qua. Doi cung mot dong tien duy nhat la GATE BOP MEO
#    BAI VIET: no da nhet 3000円 lam cau 1 cho de tai 生ゴミ, trong khi noi dau thuc
#    la MUI + su ngai ngung, khong phai tien.

# ── O6/O9 · ĐỘNG TÁC (rộng hơn STEP: dùng để chấm "câu có trả tiền" + dò payoff)
# 🔴 2026-09-06 — nới dạng CHIA của động từ (て/っ/い-onbin). Ca thật: #30 viết 「叩いて
#    いきます」 → `叩[きく]` KHÔNG khớp → cả khối 打ち直し 5 câu bị chấm "không trả tiền", và
#    người viết đi bẻ câu thành 「叩きます」 cho vừa regex (2 lần trong cùng video, v1 và v2).
#    Cùng họ: #22 `焼く/炒める`, #21 `拭い` vs `拭き`. Gate ăn CHỮ không ăn Ý ⇒ bài đúng bị
#    chấm sai. Thêm `触れ` vì 「指先で天井に触れました」 (#28 v2, cold open được nhận) = 0/5.
ACT = re.compile(r"(?:入れ|置[きい]|開け|かけ|巻[きい]|吊[りるっ]|貼[りるっ]|混ぜ|流[しす]|"
                 r"撒[きくい]|拭[きくい]|挟[みむ]|沈め|加え|溶か[しす]|外[しす]|閉め|向け|"
                 r"休ませ|干[しす]|包[みむ]|しぼ|こす|磨[きくい]|削[りるっ]|研[ぎぐい]|漬け|"
                 r"煮|茹で|冷や[しす]|温め|叩[きくい]|振[りるっ]|塗[りるっ]|敷[きくい]|載せ|"
                 r"通[しす]|回[しす]|触[れっ])|(?:て|で)ください")
# ── O6 · từ NGHỊCH LÝ — câu đảo nhận thức cũng là câu "trả tiền" ─────────────
TWIST = ["ところが", "じつは", "実は", "逆に", "ではありません", "ありません",
         "むしろ", "なぜ", "どちらでしょう", "間違い", "効きません",
         "危ない", "やめましょう", "必要ありません", "もういらない",
         "ではなく"]   # 2026-09-06: 「殺す道具ではなく、乾かす道具」 (#30) = nghịch lý, chấm oan

# ── O6 · ĐỒNG TIỀN THỨ BA: NHẬP GIÁC QUAN (thêm 2026-08-11 khi hiệu chuẩn) ────
# 🔴 Bài học: bản đầu của O6 chỉ nhận 2 đồng tiền (số mới / động tác) nên nó chấm
#    video 02 (AVD 22,38%) là 8 câu không-trả-tiền, TỆ HƠN video 07 (AVD 12,12%,
#    6 câu) — tức xếp NGƯỢC với retention thật. Cold open của 02 là một CẢNH NHẬP
#    GIÁC QUAN (「夏の夕暮れを思い浮かべて」「耳元で響く羽音もない」) và nó giữ được
#    88,9% @15s · 61,1% @30s. ⇒ nhập giác quan LÀ trả tiền, chỉ không trả bằng số.
#    Đây đúng là mũi tiêm ③ của `humanize-script-voice.md` (ký ức giác quan) — luật
#    workspace đã biết nó quan trọng, chỉ là O6 bản đầu không đếm nó.
# ⚠️ Đừng gộp nó vào TWIST: nghịch lý đánh vào ĐẦU, giác quan đánh vào THÂN THỂ —
#    trộn lại thì lần sau không tách được cái nào đang thiếu.
SENSE = ["思い浮かべ", "想像し", "羽音", "におい", "匂い", "香り", "手ざわり", "手触り",
         "ひんやり", "ぬるり", "ぬめり", "ベタベタ", "指先", "足の裏", "ざらざら",
         "ひび", "湿った", "しっとり", "ちりちり", "夕暮れ", "朝いちばん", "肌"]
# 2026-09-06: thêm ませんでしたか/でしたか (#22, #25 chấm oan) + cho phép ？/? cuối câu.
ASK = re.compile(r"(?:ませんか|ませんでしたか|でしたか|でしょうか|ですよね)[。？?]?$")

# O7 — STAKE cua nguoi xem: so tien HOAC canh giac quan/hau qua (xem chu thich MONEY)
STAKE_OK = SENSE + ["つらい", "恥ずかし", "気まずい", "人が来る", "来客", "困っ"]

# ── O6 · ĐỒNG TIỀN THỨ SÁU: CẢNH (thêm 2026-09-06, 04_FORMULA §1.8) — ĐANG WARN, CHƯA FAIL ─
# 🔴 Bằng chứng: cold open được user nhận của #28 v2 là 「指先で天井に触れました」「ぬるい。」 —
#    gate cũ chấm cả hai là 0/5 đồng tiền ⇒ gate PHẠT đúng thứ giữ chân. Bản giữ chân tốt nhất
#    kênh (#02, 88,9% @15s) cũng là một CẢNH. ⇒ tính thêm đồng tiền ⑥ = người/vật + động tác
#    giác quan · câu tính-từ trần ≤6 ký · câu thoại 「」.
# ⚠️ Chưa đưa vào FAIL: thêm đồng tiền = gate LỎNG hơn; phải chắc nó không cho video 07 qua.
#    Điều kiện nâng lên FAIL: `--calib` với ⑥ vẫn xếp 02 trên 07 VÀ 07 vẫn ≥2 câu không trả.
#    Tới lúc đó gate chỉ IN `O6 với ⑥: N câu` cạnh O6 gốc để so.
SCENE_ACT = re.compile(r"(?:を|に|へ)[^。]{0,12}(?:触れ|触っ|見上げ|見つめ|覗|のぞ|握っ|持ち上げ|"
                       r"嗅|かい|なで|撫で|押し|めくっ|ひっくり返し|つまん|畳ん)(?:ました|た|て)")
SCENE_ADJ = re.compile(r"^.{0,4}(?:ぬるい|冷たい|熱い|重い|軽い|くさい|臭い|暗い|かゆい|痛い|硬い|"
                       r"柔らかい|ざらざら|べたべた)[。、]?$")
QUOTE = re.compile(r"「[^」]{2,40}」")

# ── O6 · ĐỒNG TIỀN ⑦ HẬU QUẢ và ⑧ SO SÁNH (thêm 2026-09-06 sau khi bóc 7 video peer) ──
# 🔴 Bằng chứng: HIT 蚊 của 昔の人の知恵 (499.000 view) bị gate cũ chấm **7/9 câu KHÔNG TRẢ TIỀN**
#    trong cửa sổ 0–45s — tức gate đánh trượt một video nửa triệu view. Đọc lại 2 câu đắt nhất
#    của nó thì thấy gate mù đúng hai thứ:
#      · 「時に人の命さえ奪います」            → HẬU QUẢ nặng, 0/5 đồng tiền
#      · 「サメや蛇、ライオン…すべて合わせた数よりも多い」 → SO SÁNH choáng KHÔNG có chữ số, 0/5
#    Cả hai đều là "trả tiền" theo đúng nghĩa của O6 (người xem nhận được thứ đáng ở lại), chỉ là
#    không trả bằng con số/động tác. Cùng loại lỗi với ④ giác quan (hiệu chuẩn 08-11) và ⑥ cảnh.
# ⚠️ Tách riêng ⑦ với ⑧, KHÔNG gộp — hậu quả đánh vào NỖI SỢ, so sánh đánh vào ĐỘ LỚN; trộn lại
#    thì lần sau không biết cold open đang thiếu cái nào.
# ⚠️ ĐANG WARN như ⑥: thêm đồng tiền = gate LỎNG hơn. Điều kiện nâng lên FAIL giống hệt ⑥ —
#    `--calib` phải cho thấy 02 vẫn xếp trên 07 VÀ 07 vẫn còn ≥2 câu không trả.
CONSEQ = ["命", "死ん", "亡く", "奪い", "奪う", "危険", "取り返し", "手遅れ", "壊れ", "壊し",
          "だめになる", "ダメになる", "使えなくな", "腐ら", "腐る", "傷め", "痛め", "傷つけ",
          "火事", "けが", "怪我", "病気", "修理費", "高額", "後悔"]
COMPARE = ["よりも多い", "より多い", "合わせた", "上回", "いちばん多い", "一番多い", "最も多い",
           "倍以上", "何倍", "半分以下", "けた違い", "桁違い", "比べものに"]

# ── O18 · vị trí chương "VÌ SAO BỊ MẤT" (dòng tiền) — WARN (thêm 2026-09-06) ────────────
# SKILL đòi 72–80% nhưng không có gate: #29 = 86%, #30 = 57%, cả hai PASS 0 FAIL. Bằng chứng
# vị trí chỉ có từ chouhen (loop đóng 39% → mất đuôi · 80% thắng), co-dai chưa có curve nào
# đối chiếu ⇒ WARN, không FAIL. Dò bằng cửa sổ 5 câu có ≥3 hit từ vựng ngành/tiền, sau 40% dur.
MONEY_CH = ["業界", "大手", "市場", "億円", "兆円", "利益", "メーカー", "売り上げ", "売り場",
            "買い替え", "買い直", "儲け", "商売", "広めてくれる", "宣伝"]
MONEY_LO, MONEY_HI = 0.70, 0.82

# ── O19 · cụm gọi lại lời hứa lặp — WARN (thêm 2026-09-06) ───────────────────────────────
# `冒頭で`/`お約束した`/`最後に置いておいた` là TỪ KHOÁ CÓ CHỨC NĂNG của O11. Dùng nó để MỞ một khối
# ở giữa bài ⇒ O11 tưởng loop đóng sớm. Đã dính 5 LẦN (#20 ×2, #21 ×2, #25, #30 v1, #30 v2) —
# sổ ghi "Ba lần rồi, coi như luật" mà vẫn dính thêm hai. Chưa đo lặp có gây rớt ⇒ WARN.

# ══ MODEL SÓNG LEO THANG (O11–O13, chốt 2026-08-11) ══════════════════════════
# Bệnh của model cũ: 「一つ目・二つ目・三つ目」 = LIỆT KÊ PHẲNG, mỗi mẹo tự đóng gọn
# ⇒ xong mẹo 1 là người xem đã có thứ cần ⇒ sàn tụt 41,7% @3′ → 16,7% @20′.
# Cơ chế thay thế lấy từ chouhen (9 video, chia đôi sạch 6/6): retention TĂNG ở
# quãng có CÚ LẬT, GIẢM ở quãng không có gì xảy ra. Người xem rời khi HẾT CHUYỆN
# CHƯA ĐƯỢC GIẢI QUYẾT — không phải khi bài dài.

# O12 — CÚ LẬT: bẻ một niềm tin/thói quen người xem ĐANG làm.
FLIP = ["逆効果", "逆でした", "反対も", "間違い", "効きません", "やめてください",
        "やめてみて", "ではありません", "が原因", "こそが原因", "要りません",
        "必要ありません", "いらない", "むしろ", "実は逆", "じつは逆"]
FLIP_S_MAX = 360        # cú lật đầu ≤ phút 6

# O13 — câu MỞ: đóng sóng bằng cách mở loop mới, KHÔNG đóng gọn.
OPEN_LOOP = ["まだ弱い", "まだ本題", "ところが", "本当に効くのは", "順番が逆",
             "もう一つ", "ここからです", "とっておきます", "後半で", "最後に",
             "奇妙なのはここから", "話はここで終わりません"]

# O11 — LOOP LỚN phải đóng ở ≥78% thời lượng (chouhen: đóng ở 39% → mất đuôi bài;
#       bản thắng đóng ở 80%). Dò bằng câu gọi lại lời hứa của cold open.
# ⚠️ Danh sach nay tung THIEU cach goi lai pho bien nhat: loi hua o cold open dang
#    "de danh den cuoi" (「その一つは、いちばん最後に置いておきます」) duoc dong bang
#    「いちばん最後に置いておいた、あの一つです」 — echo nguyen van, la cach dong loop
#    MANH hon 「冒頭でお約束した」. Gate bao FAIL trong khi bai lam DUNG.
CLOSE_BIG = ["冒頭で", "はじめにお約束", "お約束した", "最後の一つ", "最後に残した",
             "最後に置いておいた", "最後に置いた", "とっておいた"]
CLOSE_BIG_MIN = 0.78

# ══ CLIFF THỨ HAI (O14–O15, thêm 2026-08-11 sau khi soi 3 curve NGOÀI 45s đầu) ═
# Bài học từ script CŨ — 3 chỗ rớt nặng nhất SAU cold open, đo bằng subs.srt thật:
#
#  ① −14,7đ · video 07 phút 5 (giây 311) — khối CTA/登録 đặt NGAY SAU payoff:
#     308s「今日の夕方から、始められます」← vừa trả xong mẹo 1
#     311s「この番組を初めてご覧になる方は」→ 314s「登録のボタンを押して」
#     Người xem vừa nhận hàng, đáng lẽ phải bị đẩy vào chuyện tiếp, lại bị hỏi
#     một câu ⇒ đóng tab. ⇒ O14: CTA phải nằm ở chỗ có LOOP ĐANG MỞ.
#
#  ② −11,8đ · video 07 phút 11 (giây 695–709) — khối LỊCH SỬ/VĂN HOÁ thuần,
#     4 câu liền không có số/động tác:「場を清め、木々の葉を生き返らせ」
#    「もてなしの作法として」「実利と礼儀が、一つになっていた習わしでした」
#     Câu MỞ「ところが、落とし穴があります」tới ở 709s = SAU khi đã mất người.
#
#  ③ −11,1đ · video 02 (giây 1215) — chi tiết phụ/mô tả trang trí:
#    「秋には鮮やかな紫色の実をつけ…庭の景色を豊かに」(bài đang nói chống muỗi).
#
# 🔴 O9 đo gap theo PHÚT (≤2′30″) nên KHÔNG bắt được 4 câu liền ≈ 18 giây.
#    O15 là luật RUN-LENGTH: cấm ≥3 câu LIỀN không trả tiền, ở BẤT KỲ đâu trong
#    bài — cùng cơ chế đã giết cold open của 07, chỉ khác chỗ.
# 🔴 RUN_MAX = 3 (tức chặn từ 4 câu liền) — HIỆU CHUẨN theo ca thật, không đoán:
#    cả 3 cú rớt đo được đều là ĐÚNG 4 câu liền (07 cold open 21–35s · 07 phút 11
#    683–700s · 02 ~1215s). Đặt trần 2 (chặn từ 3 câu) đã thử và LOẠI: nó bắt cả
#    khối reveal cơ chế của script 18 ở giây 331/378/1006 — 3 câu liền là nhịp
#    BÌNH THƯỜNG của văn dày, không phải hố.
# ⚠️ GIỚI HẠN 1: O15 KHÔNG phân biệt được "khối tả cảnh trang trí" (thứ đã giết
#    video 07) với "khối reveal cơ chế" (thứ làm nên chất kênh). Cả hai đều không có
#    số/động tác. ⇒ chỗ nào bị flag thì phải ĐỌC BẰNG MẮT rồi quyết: là trang trí thì
#    CẮT, là cơ chế thì chèn một con số THẬT (đừng nhồi số vô nghĩa cho qua gate —
#    làm vậy là tự làm hỏng phép đo).
#
# 🔴 GIỚI HẠN 2 — QUAN TRỌNG, ĐỪNG ĐỌC O15 QUÁ MẠNH. Bước `--calib` cho thấy O15
#    **KHÔNG discriminating giữa 2 video**: 02 có **27** run @ AVD 22,38% · 07 có
#    **24** run @ AVD 12,12% ⇒ nhiều run hơn mà retention TỐT HƠN. Và 24 run ×
#    11,8đ thì vượt 100%, tức **phần lớn run 4 câu KHÔNG gây cú rớt đo được nào.**
#    Bằng chứng của O15 là **CỤC BỘ** (một run 4 câu trùng đúng cú −11,8đ ở giây
#    683–700 của video 07), không phải bằng chứng so-giữa-video.
#    ⇒ **Một run là NGHI PHẠM, không phải BỊ KẾT ÁN.** Giữ nó ở mức FAIL vì (a) rẻ
#    để thoả — script 18 đi từ 7 run về 0 chỉ với 6 sửa, 4 trong đó THÊM nội dung
#    thật — và (b) nó buộc văn phải dày. Nhưng **đừng dùng số run để so 2 script**,
#    và đừng kết luận "cắt hết run là AVD lên". Thứ đã chứng minh được là cold open
#    (O1/O6) và vị trí CTA (O14).
#
# 🔴 GIỚI HẠN 3 — HẠ O15 XUỐNG WARN (2026-09-06, 04_FORMULA §3). Ở mức FAIL, O15 tạo động
#    cơ NHỒI: #30 v1 thừa nhận 2 khối chèn "chỉ để lấp thời lượng và qua O15" — đúng 2 khối
#    bị cắt ở v2, và 7/7 bản v2 được user nhận đều NGẮN HƠN v1. Cộng GIỚI HẠN 2 ở trên
#    (không discriminating) ⇒ đây là BỚT một gate chưa hiệu chuẩn, không thêm. Nâng lại FAIL
#    chỉ khi 08_ANALYTICS_LOG §6 có curve cho thấy run 4 câu gây rớt thật.
RUN_MAX = 3             # O15: trần số câu KHÔNG TRẢ TIỀN nằm LIỀN nhau (WARN, không FAIL)
CTA_MARK = "高評価"      # O14: câu CTA canonical co-dai
CTA_LOOK = 3            # O14: phải có ≥1 câu MỞ trong 3 câu trước CTA

# ── O16 — INTENT của query đích (chốt 2026-08-12, `CHANNEL_DIAGNOSIS_2026-08-12.md` §2ⓑ)
#
#    Đo TAY trong Studio (API không còn cấp impressions/CTR từ 2026-07-30): **80% impressions
#    của kênh đến từ SEARCH**, và AVD theo nguồn là **search 3:09** vs browse 9:49 vs trang
#    kênh 8:48 — tức cửa duy nhất YouTube mở cũng là cửa cho ra tín hiệu bẩn nhất, bẩn gấp ~3.
#
#    Soi từng query thì rõ vì sao: query XÁC MINH một thủ pháp hẹp bỏ đi trong 3–17 giây
#      ハチの巣 0:03 · ゴキブリ対策 0:11 · 室外機 日除け 効果 0:16 · 土用干し 0:17
#    còn 2 query xem lâu là intent "cái nào nhất / kể tao nghe về vật này"
#      蚊除け 最強 19:17 · すだれ 7:51
#
#    🔴 ĐÂY LÀ LỖI **CHỌN** TỆP, KHÔNG PHẢI LỖI **GIỮ** TỆP. Người gõ 「室外機 日除け 効果」
#    cần 20 giây rồi đi, dù 20 giây đó viết hay tới đâu ⇒ O1..O15 (cửa 45 giây) sửa một việc
#    KHÁC và vẫn phải làm. Đừng coi O16 là bản thay thế.
#
#    ⚠️ Giới hạn của bằng chứng: mỗi query chỉ 1–2 view (n=20). Bằng chứng CHÍNH là con số
#    TỔNG HỢP theo nguồn (62 view search @3:09 vs 10 @9:49 vs 15 @8:48); danh sách query chỉ
#    là cơ chế giải thích. Đừng trích một query lẻ.
#
#    Luật bản người đọc: `../CLAUDE.md` §📐 điểm 7b. KHÔNG đảo điểm 7 (nó nói về VOLUME và vẫn
#    đúng) — O16 là tầng thứ hai, về CHẤT của cùng cái cầu đó.
INTENT_OK = ("最強", "なぜ", "やり方", "順番", "比較", "単体")
INTENT_BAD = ("効果", "意味")   # modifier xác minh — cấm ở keyword DẪN, vẫn giữ làm TAG được
INTENT_HEAD = 40               # chỉ soi header script, không quét cả bài


def clean(line: str) -> str:
    """Bỏ tag nhấn nhá [速0.85]/[間1.2] — chúng KHÔNG cộng ký tự khi ước giây."""
    return re.sub(r"\[[^\]]*\]", "", line).strip()


def cues_srt(path: Path):
    """→ [(giây, text)] từ TIMELINE GIỌNG THẬT. Dùng cho hiệu chuẩn + kiểm sau render.

    Chính xác hơn `cues()` (ước theo CPS) vì nó là giây thật của bản đã lên sóng.
    Cần thiết vì script của video 01/02 KHÔNG còn (đăng trước khi có flow gom script
    vào `_scripts/`) — `_upload/subs.srt` là dấu vết duy nhất còn lại của chúng.
    """
    out = []
    for blk in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="ignore")):
        L = [x for x in blk.strip().split("\n") if x.strip()]
        if len(L) < 3:
            continue
        m = re.match(r"(\d\d):(\d\d):(\d\d)", L[1])
        if not m:
            continue
        h, mi, s = (int(x) for x in m.groups())
        out.append((float(h * 3600 + mi * 60 + s), "".join(L[2:]).strip(), 0))
    return out


def cues(path: Path):
    """→ [(giây bắt đầu, text)] + chỉ số dòng, ước theo CPS. Trả cả marker."""
    out, acc = [], 0.0
    for i, raw in enumerate(path.read_text(encoding="utf-8").split("\n")):
        if MARKER in raw:
            out.append((acc, "\x00MARKER", i))
            continue
        t = clean(raw)
        # 🔴 `TARGET_QUERY:`/`INTENT:` là HEADER của luật O16 (thêm 2026-08-12), KHÔNG phải lời
        #    đọc. Bỏ sót chúng thì chính 2 dòng đó bị đếm vào cửa sổ 0–45s và làm O6 FAIL oan —
        #    bug đã dính thật ngay ở script đầu tiên dùng O16 (video 19).
        # 2026-09-06: + 3 header của O17 (04_FORMULA §5) — cùng bẫy video 19: quên `#` thì
        #    TTS đọc header thành lời VÀ gate đếm nó vào cửa sổ 0–45s.
        if not t or t.startswith(("#", "---", ">", "|", "```", "=",
                                  "TARGET_QUERY", "INTENT",
                                  "FORMULA", "SELFCHECK", "CONFESS")):
            continue
        out.append((acc, t, i))
        acc += len(t) / CPS
    return out


def intent_of(path: Path):
    """O16 — đọc header `TARGET_QUERY:` + `INTENT:`. → (query, intent), None nếu thiếu."""
    q = it = None
    for raw in path.read_text(encoding="utf-8", errors="ignore").split("\n")[:INTENT_HEAD]:
        m = re.search(r"TARGET_QUERY\s*[:：]\s*(.+)", raw)
        if m and q is None:
            q = m.group(1).strip().strip("`*_ ")
        m = re.search(r"INTENT\s*[:：]\s*(.+)", raw)
        if m and it is None:
            it = m.group(1).strip().strip("`*_ ")
    return q, it


FORMULA_STAKE = ("能力", "体面", "安全")
FORMULA_FRAME = ("時計", "数え", "捜査", "仕掛け")


def formula_of(path: Path):
    """O17 — header 3 dong cua 04_FORMULA §5. -> dict(formula, selfcheck, confess) hoac None.

    Chi kiem CO MAT + enum, KHONG cham noi dung: 3 cau tu hoi (open-loop la cau hoi? trao khoi
    nhan ra? phut 10 con nghi van?) khong may hoa duoc — nhung KHONG ghi ra thi se troi (luat
    kiem bang mat thi troi). Day la kiem HINH THUC nhu O16, nen FAIL duoc.
    """
    got = {}
    for raw in path.read_text(encoding="utf-8", errors="ignore").split("\n")[:INTENT_HEAD]:
        for key in ("FORMULA", "SELFCHECK", "CONFESS"):
            m = re.search(rf"^#\s*{key}\s*[:：]\s*(.+)", raw)
            if m and key not in got:
                got[key] = m.group(1).strip()
    return got


def find_entry(cs):
    """O1 — dò nhãn vào bài theo thứ tự ưu tiên. Trả (giây, mô tả) hoặc (None, '')."""
    for sec, t, _ in cs:
        if t == "\x00MARKER":
            return sec, "(marker GATE:本編 — đặt tay)"
    for sec, t, _ in cs:
        if t == "\x00MARKER":
            continue
        if TELL.search(t) and not any(d in t for d in TELL_DENY):
            return sec, t[:30]
        if ENUM.match(t):
            return sec, t[:30]
        if STEP.search(t):
            return sec, t[:30]
    return None, ""


def scan(path: Path):
    cs = cues_srt(path) if path.suffix == ".srt" else cues(path)
    body = [(s, t) for s, t, _ in cs if t != "\x00MARKER"]
    entry_s, entry_t = find_entry(cs)

    win = [(s, t) for s, t in body if WIN[0] <= s < WIN[1]]
    head60 = [(s, t) for s, t in body if s < 60]
    pre15 = "".join(t for s, t in body if s < WIN[0])
    head_all = [(s, t) for s, t in body
                if entry_s is None or s < entry_s]

    fails, warns, notes = [], [], []

    # O1
    if entry_s is None:
        fails.append("O1 KHÔNG DÒ ĐƯỢC nhãn vào bài — ĐỪNG đọc con số nào ở đây. "
                     f"Thêm {MARKER} vào _TTS.md ngay trên dòng vào bài")
    elif entry_s > LIMIT_S:
        over = int((entry_s - LIMIT_S) * CPS)
        fails.append(f"O1 vào bài ở ~{entry_s:.0f}s (+{over} ký quá trần {LIMIT_S}s)")

    # O2
    toc = [(s, t) for s, t in win if any(p.search(t) for p in TOC)]
    if toc:
        fails.append(f"O2 giây {WIN[0]}–{WIN[1]} có {len(toc)} câu MỤC LỤC/tuyên bố")
        notes += [(s, t, "cắt — câu này chỉ hứa, không trả gì") for s, t in toc]

    # O3
    cite = [(s, t) for s, t in win if any(c in t for c in CITE)]
    if cite:
        fails.append(f"O3 giây {WIN[0]}–{WIN[1]} có {len(cite)} câu GÁN NGUỒN/nhắc lại")
        notes += [(s, t, "dời xuống thân bài (khối 原典)") for s, t in cite]

    # O4
    greet = next((s for s, t in body if CHAN in t), None)
    if greet is not None and (entry_s is None or greet < entry_s):
        fails.append(f"O4 câu chào 「{CHAN}」 ở ~{greet:.0f}s = TRƯỚC mẹo 1 "
                     "→ dời xuống SAU mẹo 1 (user chốt 2026-08-11)")

    # O5
    hits = sorted({d for s, t in head60 for d in DISC if d in t})
    if hits:
        fails.append("O5 miễn trừ/dặn dò trong 60s đầu: " + "・".join(hits))

    # O6 ⭐ luật lõi của mốc 60% — mọi câu trong cửa sổ phải TRẢ TIỀN
    # (cùng phép chấm dùng lại cho O15 trên TOÀN BÀI — xem `paid` bên dưới)
    def pay_scan(seq, ext=False):
        """→ [(giây, text, có trả tiền?)] · 5 đồng tiền, số MỚI tính theo thứ tự đọc.
        ext=True: tính thêm ⑥ CẢNH · ⑦ HẬU QUẢ · ⑧ SO SÁNH (đang WARN — chỉ để IN đối chiếu)."""
        seen: set[str] = set()
        out = []
        for s, t in seq:
            nums = {m.group(0).replace(" ", "") for m in NUM.finditer(t)}
            ok = (bool(nums - seen)                      # ① con số/đơn vị MỚI
                  or bool(ACT.search(t))                 # ② động tác
                  or any(w in t for w in TWIST)          # ③ nghịch lý
                  or any(w in t for w in SENSE)          # ④ nhập giác quan
                  or bool(ASK.search(t)))                # ⑤ câu hỏi kéo người xem vào
            if ext and not ok:
                ok = bool(SCENE_ACT.search(t) or SCENE_ADJ.match(t) or QUOTE.search(t)   # ⑥ CẢNH
                          or any(w in t for w in CONSEQ)                                  # ⑦ HẬU QUẢ
                          or any(w in t for w in COMPARE))                                # ⑧ SO SÁNH
            seen |= nums
            out.append((s, t, ok))
        return out

    paid5 = pay_scan(body)
    free5 = [(s, t) for s, t, ok in paid5 if not ok and WIN[0] <= s < WIN[1]]
    paid = pay_scan(body, ext=True)
    free = [(s, t) for s, t, ok in paid if not ok and WIN[0] <= s < WIN[1]]
    # 🔴 2026-09-06 — ⑥⑦⑧ NÂNG TỪ WARN LÊN FAIL. Điều kiện tự đặt lúc thêm chúng đã thoả:
    #    `--calib` với bộ 8 đồng tiền vẫn xếp 02 (AVD 22,4%) TRÊN 07 (AVD 12,1%) — 2 câu vs 6 câu
    #    không trả — và 07 vẫn ≥2 nên gate chưa mất khả năng chặn. Kiểm thêm trên toàn bộ script
    #    co-dai: KHÔNG script nào đổi trạng thái (04 vẫn 5 câu, 29/30 vẫn 0) ⇒ nới này chỉ ăn vào
    #    những dạng câu mà kênh mình chưa viết bao giờ, đúng dạng đã làm gate đánh trượt HIT 蚊
    #    499.000 view (7/9 → 3/9). `free5` giữ lại để in đối chiếu, đừng bỏ.
    free6 = free5
    if len(free) > FREE_MAX:
        fails.append(f"O6 giây {WIN[0]}–{WIN[1]} có {len(free)} câu KHÔNG TRẢ TIỀN "
                     f"(trần {FREE_MAX}) → đây là cái vách làm @45s tụt còn 41–50%")
        notes += [(s, t, "0/8 đồng tiền (số·động tác·nghịch lý·giác quan·câu hỏi·cảnh·hậu quả·so sánh) → cắt hoặc nhồi")
                  for s, t in free]

    # O7
    stake = "".join(t for s, t in body)[:STAKE_N]
    if not (MONEY.search(stake) or NUM.search(stake)
            or any(w in stake for w in STAKE_OK)):
        warns.append(f"O7 {STAKE_N} ký đầu (15s) chưa có STAKE cụ thể của người xem "
                     "— cần con số/giá HOẶC cảnh giác quan/hậu quả (luật 2026-07-21, "
                     "nới 2026-08-11: video 02 giữ 88,9% @15s bằng cảnh giác quan, 0 con số)")

    # O9 ⭐ luật của SÀN ≥55% — gap giữa 2 payoff xuyên thân bài
    pay = [s for s, t in body if ACT.search(t) or NUM.search(t)]
    gap_max, gap_at = 0.0, 0.0
    prev = entry_s if entry_s is not None else 0.0
    for s in pay + [body[-1][0] if body else 0.0]:
        if s < prev:
            continue
        if s - prev > gap_max:
            gap_max, gap_at = s - prev, prev
        prev = s
    if gap_max > GAP_MAX:
        fails.append(f"O9 gap payoff dài nhất {gap_max/60:.0f}′{int(gap_max)%60:02d}″ "
                     f"từ ~{gap_at/60:.0f}′{int(gap_at)%60:02d}″ (trần 2′30″) → đó là một cái hố")

    # O10
    if not any(re.search(r"最後|いちばん(?:手軽|簡単|効く)", t) for s, t in head60):
        warns.append("O10 60s đầu chưa tuyên bố 'mẹo mạnh nhất để CUỐI' "
                     "→ khán giả lấy được mẹo 1 rồi bỏ đi, sàn không lên nổi")

    # ══ MODEL SÓNG LEO THANG ═════════════════════════════════════════════════
    dur = body[-1][0] if body else 0.0

    # O11 — LOOP LỚN đóng ≥78% thời lượng
    close = next((s for s, t in body if any(c in t for c in CLOSE_BIG)
                  and s > dur * 0.4), None)
    if close is None:
        fails.append("O11 KHÔNG thấy chỗ đóng LOOP LỚN (câu gọi lại lời hứa cold open: "
                     "「冒頭でお約束した…」) → lời hứa mở mà không đóng = mất đuôi bài")
    elif dur and close < dur * CLOSE_BIG_MIN:
        fails.append(f"O11 LOOP LỚN đóng ở {close/dur*100:.0f}% thời lượng "
                     f"(trần ≥{CLOSE_BIG_MIN*100:.0f}%) → đóng sớm là mất đuôi bài")

    # O18 — vị trí chương "VÌ SAO BỊ MẤT" (WARN): cửa sổ trượt 5 câu, ≥3 hit MONEY_CH, sau 40% dur
    money_pos = None
    if dur:
        for i in range(len(body) - 4):
            s0 = body[i][0]
            if s0 < dur * 0.4:
                continue
            blob = "".join(t for s, t in body[i:i + 5])
            # tính cả số tiền (数百円/3000円): chương này nói bằng giá, không chỉ bằng từ ngành
            # (#29 viết 「数百円の砥石を10年 vs 3000円の包丁を3年ごと」 → 0 hit MONEY_CH → KHÔNG DÒ)
            hits = sum(1 for w in MONEY_CH if w in blob) + len(MONEY.findall(blob))
            if hits >= 3:
                money_pos = s0 / dur
                break
    if money_pos is None:
        warns.append("O18 KHÔNG dò được chương 「vì sao bị mất」 (dòng tiền) sau 40% bài — "
                     "thiếu chương, hoặc từ vựng ngoài MONEY_CH")
    elif not (MONEY_LO <= money_pos <= MONEY_HI):
        warns.append(f"O18 chương dòng tiền ở {money_pos*100:.0f}% (SKILL đòi 72–80%) — "
                     f"{'sớm: đóng LOOP NGÀNH trước khi đuôi bài có lý do ở lại' if money_pos < MONEY_LO else 'trễ: dồn 2 khối giảng về cuối'}")

    # O19 — cụm CLOSE_BIG xuất hiện >1 lần sau 40% dur (WARN)
    n_close = sum(1 for s, t in body if s > dur * 0.4 and any(c in t for c in CLOSE_BIG))
    if n_close >= 2:
        warns.append(f"O19 cụm gọi lại lời hứa ({'/'.join(CLOSE_BIG[:3])}…) xuất hiện {n_close} lần "
                     "→ có cụm đang MỞ khối thay vì ĐÓNG; dính 5 lần rồi (#20 #21 #25 #30)")

    # O12 — CÚ LẬT đầu ≤ phút 6
    flip = [s for s, t in body if any(w in t for w in FLIP)]
    first_flip = next((s for s in flip if entry_s is None or s >= entry_s), None)
    if first_flip is None:
        fails.append("O12 KHÔNG có CÚ LẬT nào — bài đang LIỆT KÊ, không leo thang. "
                     "Mỗi sóng phải bẻ một niềm tin người xem đang làm")
    elif first_flip > FLIP_S_MAX:
        fails.append(f"O12 cú lật đầu ở ~{first_flip/60:.0f}′{int(first_flip)%60:02d}″ "
                     f"(trần phút {FLIP_S_MAX//60}) → nửa đầu không có gì xảy ra")

    # O14 — CTA phải nằm ở chỗ có LOOP ĐANG MỞ, không phải ngay sau một payoff
    # (video 07: khối 登録+câu hỏi comment đặt ngay sau 「今日の夕方から始められます」
    #  → −14,7 điểm, cú rớt nặng NHẤT của cả bài sau cold open)
    idx_cta = next((i for i, (s, t, _) in enumerate(paid) if CTA_MARK in t), None)
    if idx_cta is None:
        warns.append(f"O14 KHÔNG thấy câu CTA (「{CTA_MARK}」) — CTA giữa video là bắt buộc "
                     "(`cta-midvideo.md` §2.4)")
    else:
        prev = [t for s, t, _ in paid[max(0, idx_cta - CTA_LOOK):idx_cta]]
        if not any(w in t for t in prev for w in OPEN_LOOP):
            s_cta = paid[idx_cta][0]
            fails.append(f"O14 CTA ở ~{s_cta/60:.0f}′{int(s_cta)%60:02d}″ đứng ngay sau một "
                         f"payoff, KHÔNG có câu MỞ loop trong {CTA_LOOK} câu trước → "
                         "đây là cú rớt −14,7đ của video 07")

    # O15 — cấm ≥3 câu LIỀN không trả tiền, ở BẤT KỲ đâu trong bài (cliff thứ hai)
    runs, run, start = [], 0, 0.0
    for s, t, ok in paid:
        if not ok:
            if run == 0:
                start = s
            run += 1
        else:
            if run > RUN_MAX:
                runs.append((start, run))
            run = 0
    if run > RUN_MAX:
        runs.append((start, run))
    if runs:
        warns.append(f"O15 có {len(runs)} chỗ ≥{RUN_MAX + 1} câu LIỀN không trả tiền "
                     "→ nghi phạm, ĐỌC BẰNG MẮT: trang trí → CẮT · cơ chế → giữ. ⛔ cấm chèn số")
        for s, k in runs:
            notes.append((s, f"{k} câu liền không trả tiền", "chèn số/động tác, hoặc cắt"))

    # O13 — số câu MỞ ≥ số sóng − 1 (số sóng suy từ độ dài: 3′30″/sóng)
    n_open = sum(1 for s, t in body if any(w in t for w in OPEN_LOOP))
    n_wave = max(1, round((dur - 45 - 150) / 210)) if dur else 1
    if n_open < n_wave - 1:
        fails.append(f"O13 chỉ {n_open} câu MỞ loop / cần ≥{n_wave - 1} "
                     f"(bài {dur/60:.0f}′ ≈ {n_wave} sóng) → có sóng đóng gọn, "
                     "không dẫn sang sóng kế")

    # O16 — INTENT của query đích. CHỈ áp cho script đang chờ render (`03_SCRIPTS`):
    #   · `--calib` đọc .srt → không có header, bỏ qua
    #   · `--all` đọc script ĐÃ ĐĂNG → viết trước khi có luật, chỉ ghi note, KHÔNG fail oan
    q = it = None
    if path.suffix == ".md":
        q, it = intent_of(path)
        old = "07_UPLOADED" in path.parts
        if not q or not it:
            msg = ("O16 THIẾU khai báo intent — thêm 2 dòng vào header script: "
                   "`TARGET_QUERY: <query đích>` + "
                   f"`INTENT: {'|'.join(INTENT_OK)}`  (luật CLAUDE.md §📐 7b)")
            (notes.append((0.0, "chưa khai TARGET_QUERY/INTENT", "script cũ, trước luật 08-12"))
             if old else fails.append(msg))
        else:
            if not any(k in it for k in INTENT_OK):
                v = (f"O16 INTENT 「{it}」 ngoài nhóm cho phép ({'|'.join(INTENT_OK)}) → "
                     "query kiểu này bỏ đi trong 3–17 giây (đo Studio 2026-08-12)")
                notes.append((0.0, v, "script cũ")) if old else fails.append(v)
            bad = [k for k in INTENT_BAD if k in q]
            if bad:
                v = (f"O16 TARGET_QUERY 「{q}」 chứa modifier XÁC MINH 「{'／'.join(bad)}」 → "
                     "cấm ở keyword DẪN (vẫn giữ làm tag được). Đo thật: "
                     "「室外機 日除け 効果」 = AVD 0:16 · 「蚊除け 最強」 = 19:17")
                notes.append((0.0, v, "script cũ")) if old else fails.append(v)

    # O17 — header 3 dòng của 04_FORMULA (kiểm CÓ MẶT + enum; nội dung là việc của người viết)
    #   · như O16: chỉ FAIL cho `03_SCRIPTS`; script đã đăng (07_UPLOADED) và .srt chỉ ghi note.
    fm = {}
    if path.suffix == ".md":
        fm = formula_of(path)
        old = "07_UPLOADED" in path.parts
        miss = [k for k in ("FORMULA", "SELFCHECK", "CONFESS") if k not in fm]
        if miss:
            msg = (f"O17 THIẾU header {'/'.join('# ' + k for k in miss)} — điền bảng §1 của "
                   "04_FORMULA.md rồi ghi 3 dòng (§5) vào 40 dòng đầu _TTS.md")
            (notes.append((0.0, "chưa có header 04_FORMULA", "script cũ, trước luật 09-06"))
             if old else fails.append(msg))
        else:
            f = fm["FORMULA"]
            m_st = re.search(r"stake\s*=\s*([^\s·]+)", f)
            m_fr = re.search(r"frame\s*=\s*([^\s·]+)", f)
            bad = []
            if not m_st or m_st.group(1) not in FORMULA_STAKE:
                bad.append(f"stake ∉ {'|'.join(FORMULA_STAKE)} (⛔ tiền không phải stake)")
            if not m_fr or m_fr.group(1) not in FORMULA_FRAME:
                bad.append(f"frame ∉ {'|'.join(FORMULA_FRAME)} (chỉ 4 khuôn đã chạy)")
            if bad:
                v = "O17 # FORMULA sai enum: " + " · ".join(bad)
                notes.append((0.0, v, "script cũ")) if old else fails.append(v)

    return dict(query=q, intent=it, formula=fm,
                n_free6=len(free6), money_pos=money_pos, n_close=n_close,
                entry_s=entry_s, entry_t=entry_t, n_win=len(win), n_free=len(free),
                gap=gap_max, dur=dur, n_flip=len(flip), n_open=n_open, n_wave=n_wave,
                close=close, fails=fails, warns=warns, notes=notes)



def main() -> None:
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    calib = "--calib" in sys.argv
    if calib:
        # HIỆU CHUẨN: đọc TIMELINE THẬT của video đã lên sóng để đối chiếu với AVD đo
        # được. Chỉ những video có curve retention thật mới dùng làm mốc.
        files = sorted(PROJ.glob("07_UPLOADED/*/_upload/subs.srt"))
    else:
        files = sorted((PROJ / "03_SCRIPTS").glob("*_TTS.md"))
        if "--all" in sys.argv:
            files += sorted(PROJ.glob("07_UPLOADED/*/_scripts/*_TTS.md"))

    print(f"\n══ GATE COLD OPEN co-dai · MỤC TIÊU AVD 60% · cửa mua = GIÂY {WIN[0]}–{WIN[1]}")
    print(f"   O1 vào bài ≤{LIMIT_S}s ({LIMIT} ký @ {CPS} ký/s) · O6 ≤{FREE_MAX} câu "
          f"không trả (8 đồng tiền: số·động tác·nghịch lý·giác quan·hỏi·cảnh·hậu quả·so sánh) · O9 gap payoff ≤{GAP_MAX//60}′{GAP_MAX%60:02d}″")
    print(f"   SÓNG: O11 loop lớn đóng ≥{CLOSE_BIG_MIN*100:.0f}% · O12 cú lật đầu ≤phút {FLIP_S_MAX//60} · O13 câu MỞ ≥ số sóng−1")
    print(f"   phải đạt: @45s ≥85% · sàn thân bài ≥55%  (nay 41–50% · 42→17%)")
    print(f"   O16 INTENT query đích ∈ {{{'|'.join(INTENT_OK)}}} · cấm modifier {'／'.join(INTENT_BAD)}"
          "  (search = 80% imp nhưng AVD 3:09)")
    print(f"   O17 header 04_FORMULA (# FORMULA stake∈{{{'|'.join(FORMULA_STAKE)}}} "
          f"frame∈{{{'|'.join(FORMULA_FRAME)}}} · # SELFCHECK · # CONFESS) · O15 nay là WARN")
    print(f"   luật: CHANNEL_DIAGNOSIS_2026-08-11.md + _2026-08-12.md + 04_FORMULA.md · 🔴 = chặn render\n")

    rows, n_fail = [], 0
    for f in files:
        if any(k in f.name for k in ("backup", "_demo", ".bak")):
            continue
        if f.suffix not in (".md", ".srt"):
            continue
        name = f.parent.parent.name if calib else f.name
        if only and not any(name.startswith(a) for a in only):
            continue
        rows.append((name, scan(f)))

    for f, r in rows:
        tag = "🔴 FAIL" if r["fails"] else ("🟡 WARN" if r["warns"] else "✅ PASS")
        n_fail += bool(r["fails"])
        e = f"~{r['entry_s']:.0f}s" if r["entry_s"] is not None else "KHÔNG DÒ ĐƯỢC"
        g = f"{int(r['gap'])//60}′{int(r['gap'])%60:02d}″"
        print(f"{tag}  {f}")
        print(f"    vào bài {e} 「{r['entry_t']}」 · cửa sổ {r['n_win']} câu / "
              f"{r['n_free']} câu không trả tiền · gap payoff max {g}")
        cl = f"{r['close']/r['dur']*100:.0f}%" if r["close"] and r["dur"] else "KHÔNG CÓ"
        print(f"    SÓNG: dài {r['dur']/60:.0f}′ ≈ {r['n_wave']} sóng · {r['n_flip']} cú lật · "
              f"{r['n_open']} câu MỞ · loop lớn đóng ở {cl}")
        mp = f"{r['money_pos']*100:.0f}%" if r["money_pos"] is not None else "KHÔNG DÒ"
        print(f"    WARN-đối-chiếu: dòng tiền @{mp} · O6 chỉ 5 đồng tiền cũ: {r['n_free6']} câu "
              f"(bộ 8 đang chấm: {r['n_free']}) · CLOSE_BIG ×{r['n_close']}")
        if not calib:
            iq = f"「{r['query']}」" if r["query"] else "CHƯA KHAI"
            ii = r["intent"] or "CHƯA KHAI"
            print(f"    INTENT: {ii} · query đích {iq}")
        for v in r["fails"]:
            print(f"    ✗ {v}")
        for v in r["warns"]:
            print(f"    ⚠ {v}")
        for s, t, why in r["notes"]:
            print(f"        ↳ giây {s:.0f}: 「{t[:38]}」 ← {why}")
        print()

    print(f"— {len(rows) - n_fail}/{len(rows)} script không FAIL —")
    if calib:
        print("\n🔴 HIỆU CHUẨN — đối chiếu với AVD ĐO ĐƯỢC (Analytics API 2026-08-11):")
        print("   02 蚊の庭 = 22,38%  ·  07 すだれ = 12,12%   ← 2 video duy nhất có CẢ")
        print("   curve retention thật LẪN subs.srt còn lưu. Gate phải xếp 02 TỐT HƠN 07")
        print("   (ít câu không-trả-tiền hơn, vào bài sớm hơn, gap nhỏ hơn).")
        print("   ⚠️ 01 シロアリ (31,15% — bản tốt nhất kênh) KHÔNG hiệu chuẩn được:")
        print("      `_upload/` của nó chỉ còn METADATA + thumbnail, mất cả script lẫn srt.")
        print("      ⇒ hiệu chuẩn 2 điểm, không phải 3. Đừng ghi là đã xác nhận 3 điểm.")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
