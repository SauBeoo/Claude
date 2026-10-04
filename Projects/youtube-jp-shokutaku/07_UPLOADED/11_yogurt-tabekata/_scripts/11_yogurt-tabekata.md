# 11 — そのヨーグルト、大損かも？六十代が避けたい食べ方3つと、毎朝続けたい食べ方3つ

- **Kênh:** 60代からの食卓 (persona みのり) · **Chế độ:** B · VIẾT MỚI · **Chủ đề:** ヨーグルトの食べ方 × 骨・カルシウム・血糖 (hàng đợi `03_CONTENT_PLAN.md` §2.8 — trục **血糖値**, đến lượt số `11_`)
- **Đúng luật xoay trục:** video 09 緑茶 và 10 麦茶 đều là **đồ uống** → video 11 là **món ăn**. ✅
- ⚠️ **KHÔNG phải video 食べ合わせ thứ 5** (kênh đã có 05 キャベツ · 06 ブルーベリー · 07 にんじん · 09 はちみつ): trục ở đây là **食べ方** — nội dung · nhiệt độ · lượng · **thứ tự**. きな粉 chỉ là 1 trong 3 mục.
- **Keyword dẫn (ĐO THẬT 2026-08-04 — §B1):** 🥇 **ヨーグルト + 食べ方** (med 719 v/ngày). `血糖値` med 719 nhưng **chữ 血 tắt ad → chỉ ở 概要欄 + tag**. `骨` med 48 → **không lên title**, chỉ làm trục cảm xúc trong bài.
- **Độ dài:** 5.806 ký ≈ **21,0 phút** @ 青山龍星/しっとり/速0.8 (4,60 ký/giây) — chuẩn kênh 15–25′.
- **⛔ GATE COLD OPEN: ✅ PASS — mục đầu ở giây 80** (`python tools\check_coldopen.py 11`, trần 90). 5/5 luật.
- **Bản đọc:** `11_yogurt-tabekata_TTS.md` — **BẢN CHUẨN CUỐI**. Phần A dưới **sinh tự động từ file đó** (`scratchpad/build_11_md.py`) nên không bao giờ lệch; sửa lời → sửa `_TTS.md` rồi chạy lại script, **và quét lại `match` trong SLIDES**.

## 🔴 VÒNG SỬA 2 (2026-08-04) — 7 lỗ giữ chân của bản 1 và cái đã đổi

Bản 1 PASS mọi gate máy (cold open 85s, chất người 6/6, YMYL sạch) — **nhưng gate không đo được độ QUAN TRỌNG của chủ đề.** Bảy lỗ tìm được:

| # | Lỗ của bản 1 | Đã sửa thành |
|---|---|---|
| 1 | **Câu 1 là câu GỌI TÊN, không phải stake:** 「毎朝、ヨーグルトを召し上がっている方。」 → 3 giây đầu trống. Đúng lỗi video 10 bản 1 đã mắc (chôn con số) | **Bắn con số đáng sợ ngay 3 câu đầu:** 「介護が必要になったきっかけの三番目に挙げられているのは、病気ではありません」→`[間0.6][抑揚1.3]`「骨折と、転倒です」→「およそ、七人に一人」→「その転倒がいちばん多い場所は、外ではなく、家の中」 (国民生活基礎調査, thật) |
| 2 | 🔴 **STAKE CỦA CẢ BÀI QUÁ NHẸ.** 「lãng phí / 大損」 là もったいない — không phải 怖い. Tệp 60–80 sợ **mất tự lập** (`script-shokutaku` Mục 4: dây nhạy nhất = 迷惑をかけたくない), không sợ lỗ tiền | **Đổi hẳn trục cảm xúc: カルシウム不足 → 骨 → 転倒 → 介護 → 迷惑をかけたくない.** Xuất hiện ở 4 điểm: cold open (con số) · phút 4:48 (ẩn dụ **貯金箱／入金／伝票**) · 第3位 (ẩn dụ **鉄筋とコンクリート**) · lớp cảm xúc cuối (「転ばずに、自分の足で台所に立てる。それは、ご家族に何も言わなくて済むということです」) |
| 3 | **3 câu triệu chứng không đâm:** お通じ・お腹が重い・甘すぎる = bực nhẹ | Đổi sang triệu chứng của **cùng một nỗi sợ**: 「若い頃より、背が少し縮んだ気がしませんか」「立ち上がる時、膝や腰に、手をつくようになっていませんか」「毎朝食べているのに、効いている手応えは、ないでしょうか」 |
| 4 | 🔴 **Bảng thiết kế bản 1 ghi SAI:** khai "3 lần được xác nhận あなたのせいではない" — **trong bài không có một câu xá tội nào** | Thêm **2 câu xá tội thật**: 「それは、皆さんの続け方が悪いのではありません。食べ方を、誰も教えてくれなかっただけです」 (cold open) · 「甘い方を選んでしまうのは、意志が弱いからではありません。売り場で、無糖と同じ顔をして、並んでいるからです」 (ワースト①) |
| 5 | **Open loop TỰ SPOIL:** 「夜ではありません」+「毎朝」 = đã chỉ ra buổi sáng → hết tò mò, và đáp án 「空っぽの胃」 đoán được | Loop mới **không đoán được**: 「時計の話では、ありません。順番の話です。」 Người xem sẽ đoán giờ trong ngày; đáp án là **thứ tự trong bữa** → cú lật thật. Reveal ở **78%** vẫn trả thêm câu hỏi 朝か夜か (nơi hit 578K của ngách nằm) làm lớp thưởng thứ hai |
| 6 | **3:45→5:36 trống payoff** (persona + 3 lý do + anecdote dính liền) — đúng lỗ #3 của video 10 mà bản 1 chỉ vá một nửa | Khối 3 lý do **đổi vai thành ĐỘNG CƠ SỢ** (không còn là đoạn giải thích trung tính): 目安 650〜750 → 平均 500台 → 「毎日およそ百五十ミリグラム足りていません」 → 骨=貯金箱, 崩して使われる → **「崩れた貯金は、ある日、台所で転んだ時に、はっきり分かります」** → ký ức người kể. Đoạn này giờ là chỗ căng nhất của nửa đầu |
| 7 | **Đầu chương phẳng** (「さて、二つ目です」) và **không có "cú làm ngay"** nào trong lúc nghe | Mỗi ワースト mở bằng một cái hố + **2 cú làm-ngay-trong-lúc-nghe**: ① 「今、台所のそばにいらっしゃったら…炭水化物の数字を見てください。百グラムで十グラムを超えていたら」 (phút 1:25) ② 「明日の朝、冷蔵庫から出して、顔を洗って、それから食べる」 (phút 8:20). Cú thứ ba là 第1位 (混ぜる) |

**Thêm 1 mũi "hồn" mạnh nhất bài** (không có ở bản 1): ký ức người kể về mẹ mình — 「私の母は、七十を過ぎてから、台所で一度、手をつきました。割れませんでした。ほんとうに、運が良かっただけです。あの時の音を、私は、まだ覚えています。」 Đây là cảm xúc + hành vi, **không phải claim y khoa** → hợp luật persona, và nó biến con số 「七人に一人」 thành một cái âm thanh trong bếp.

**Vì sao người xem ĐẾN:** thumbnail 「大損」 + title 「避けたい食べ方」 trên món **đã có sẵn trong tủ lạnh** (không phải món phải đi mua) · đáp án bị che. **Vì sao Ở LẠI:** ① giây thứ 5 đã biết bài này nói về chuyện **mất khả năng tự đi lại**, không phải chuyện ăn cho vui ② mỗi 60–90 giây có một thứ **làm được ngay trong lúc nghe** ③ được xá tội 2 lần ④ hai ẩn dụ chạy suốt bài (貯金箱・鉄筋) làm mọi mục sau đều "có nghĩa" ⑤ hai món nợ chưa trả: 第1位 và 「順番」.

## Thiết kế nhịp (mốc tính từ `_TTS.md`, 4,60 ký/giây — đo lại từ `subs.srt` sau render)

| Mốc | % | Khối |
|---|---|---|
| 00:00 | 0% | Cold open: **骨折・転倒 = nguyên nhân 要介護 thứ 3, 七人に一人, ở TRONG NHÀ** → 3 câu triệu chứng 骨 → xá tội → hứa 3+3 + 「買い物は増えません」 → **loop 「時計ではなく、順番」** |
| **01:20** | **6%** | **ワースト①「甘みを加えたもの」** + cú làm ngay #1 (đọc nhãn 炭水化物) · 角砂糖換算 · xá tội #2 · tự trào いちご味 · ký ức 瓶+砂糖ひとさじ · loop nhỏ trỏ 第3位 |
| 04:08 | 20% | Persona みのり (nén ~40 giây) |
| **04:48** | **23%** | **Động cơ sợ: 骨は貯金箱** — 150mg thiếu mỗi ngày · 崩して使われる · 伝票 · 「台所で転んだ時に、はっきり分かります」 |
| 06:06 | 29% | **Ký ức người kể: mẹ trượt tay trong bếp** (đỉnh cảm xúc nửa đầu) |
| 06:21 | 30% | Anecdote 1 — 三浦ヨシエ (69, 福井, 元和裁): ăn 10 năm mà 骨の検査 vẫn thấp → đổi 3 thứ |
| 07:42 | 37% | ワースト②「冷たいまま」 + cú làm ngay #2 + ký ức 昔の朝ごはん |
| 08:59 | 43% | ワースト③「量を増やす」 (リン・カリウム · 濾し器 · **cảnh báo điều kiện 腎臓**) → 「量ではなく、入れ方」 |
| 10:18 | 49% | Nhắc lại loop 「時計ではなく、順番。いちばん最後に」 |
| **10:39** | **51%** | **CTA giữa video** (câu canonical shokutaku) |
| 11:12 | 53% | 第3位 きな粉 — **ẩn dụ 鉄筋とコンクリート** (chỗ "quan trọng nhất hôm nay") → checkpoint 「に」 (12:38) |
| 12:49 | 61% | 第2位 人肌に温める (nhắc lại bẫy ② + NG 熱くしすぎ) |
| **13:51** | **66%** | **第1位 上澄み(乳清)** — 「鉄筋とコンクリートが、いちばん濃く溶けている水」 · đỉnh bài `[間1.2][速0.8][後間1.0]たった、それだけです。` |
| 15:21 | 73% | Anecdote 2 — 岡部シゲル (74, 岩手, 元中学校事務) |
| 16:16 | 77% | checkpoint 「さん」 |
| **16:29** | **78%** | **Trả loop: 順番** — 空きっ腹に先に入れるのが惜しい → 正解「食事のあと」 → thưởng thêm: 朝か夜か (骨は夜に作り替えられる → 夕食後も一つの手) |
| 18:06 | 86% | Recap 3+3 → micro-commitment → 都道府県 + comment |
| 19:25 | 92% | **Lớp cảm xúc 迷惑をかけたくない** → CTA |
| 20:09 | 96% | Disclaimer cố định → câu kết cố định |

- **Chất người 6/6** — ① tự trào いちご味 + 「五十年近く、あれを捨てていました」 ② thoại 「私、毎朝食べてるのに。」「これ、罰みたいな味がするねえ」「お父さん、それ、捨てるものじゃないよ」 + chi tiết đời sống (器とスプーンを並べて待つ · 台所を汚さないのが自分の役目) ③ ký ức giác quan 瓶入りヨーグルトに砂糖ひとさじ · 温かいご飯と湯呑みのお茶 · **母が手をついた音** ④ người kể tự làm (「私も、寒い季節は、そうしています」) ⑤ đóng nhân vật bằng cảm xúc (お孫さんに編み物を教える時間が戻ってきた · 背筋が伸びる) ⑥ phá nhịp 「温度です。」「見た目は、固い。」「割れませんでした。」「不思議ですよね。」
- **Giọng:** **26 tag nhấn** (14 速 · 10 抑揚 · 2 後間) + **87 mốc 間**. Hai đỉnh dùng khuôn `[間1.2][速0.8][後間1.0]`: 「たった、それだけです。」 (第1位) và 「これが、いちばん惜しい入れ方です。」 (reveal). ✅ Verify: **0 tag giữa câu** · **0 dòng chỉ-có-tag** ngoài dòng base.
- **YMYL:** không 治る/完治/薬の代わり/絶対; **anecdote KHÔNG claim số liệu cải thiện** (「検査の数字が変わったかどうかは、まだ分かりません」 — cố ý để không hứa kết quả); 1 cảnh báo điều kiện tại chỗ (腎臓 × 乳製品 → かかりつけの先生); trần lượng 一日一つ 100〜200g; disclaimer + câu kết cố định.
- **Nguồn thật (4, đều số liệu công chuẩn):** 厚生労働省「国民生活基礎調査」 (要介護の原因に 骨折・転倒, ~1/7) · 厚生労働省「日本人の食事摂取基準」 (カルシウム 六十代 650〜750mg) · 厚生労働省「国民健康・栄養調査」 (平均 500mg台) · 日本食品標準成分表. Phần còn lại **hedge** 「〜とされています」「〜という報告があります」 (胃酸・腸の冷え・骨の作り替えが夜に進む — KHÔNG gắn tên tổ chức).

---

## A. KỊCH BẢN — PHẦN 1 (0:00 → CTA giữa 10:39)

国の調査で、介護が必要になったきっかけの三番目に挙げられているのは、病気ではありません。骨折と、転倒です。およそ、七人に一人。しかも、その転倒がいちばん多い場所は、外ではなく、家の中だとされています。台所と、廊下と、お風呂場です。その骨を毎日つくっているのが、朝の、あの一つかもしれません。若い頃より、背が少し縮んだ気がしませんか。立ち上がる時、膝や腰に、手をつくようになっていませんか。毎朝ヨーグルトを食べているのに、効いている手応えは、ないでしょうか。それは、皆さんの続け方が悪いのではありません。食べ方を、誰も教えてくれなかっただけです。今日は、六十代が避けたい食べ方三つと、毎朝続けたい食べ方三つ。どれも、買い物は増えません。そして、いちばん惜しい食べ方を、多くの方が毎朝なさっています。時計の話では、ありません。順番の話です。

まず、いちばん多い落とし穴から、お話しします。これが、いちばん真面目な方に、起こります。今、台所のそばにいらっしゃったら、一つ、確かめてみてください。毎朝食べているヨーグルトの、横の表示です。炭水化物、と書かれた数字を見てください。一つの目安として、百グラムあたりで十グラムを超えていたら、それは骨のための一杯ではありません。甘みを加えたヨーグルトです。無糖のものと、同じ棚に、同じ大きさで並んでいます。ですから、どちらも同じ、体にいいもの、だと思ってしまいます。けれども、中身は違います。百グラムで、角砂糖二個から三個分ほどの甘みが入っているものもあります。朝、四百グラムの大きな器のものを、半分。それだけで、角砂糖が四個や五個、体に入る日があります。食べ物なら、そこまで甘くはできません。けれどもヨーグルトは、噛まずに、するりと入ってしまいます。そして、空っぽの胃に、甘いものだけが先に入ると、体は急に忙しくなるという報告があります。だるい、眠い、また甘いものが欲しい。朝から、その繰り返しになります。甘い方を選んでしまうのは、意志が弱いからではありません。売り場で、無糖と同じ顔をして、並んでいるからです。白状しますと、私も長いあいだ、いちご味のものを、体にいいものとして食べていました。甘いのに、罪がない気がしていたのですね。昔は、ヨーグルトといえば、瓶に入った、少し酸っぱいものでした。上に砂糖をひとさじ、自分で振りかけて。どれだけ甘くしたかが、自分の目に、見えていました。今は、それが見えません。直し方は、簡単です。無糖のものを買って、甘みは、自分の手でひとさじ足す。その足すものは、第三位で、はっきりお伝えします。果物の味がついたものを、果物を食べたつもりにするのは、やめておきましょう。入っているのは、果物ではなく、たいてい甘みです。

ここで少しだけ、ご挨拶をさせてください。皆さん、こんにちは。六十代からの食卓へ、ようこそ。案内人の、みのりです。私は、お医者様でも、栄養の専門家でもありません。台所に立ちながら、公表されている資料を、少しずつ読み集めているだけです。短い診察の時間では、こういう細かい話まで、なかなか聞けませんよね。まだ登録なさっていない方は、よろしければ、また台所に戻ってきてくださいね。

では、なぜ、毎朝食べているのに、手応えがないのでしょうか。理由が、三つあります。一つ。厚生労働省が示している一日の目安は、六十代で、六百五十ミリグラムから七百五十ミリグラムほど。二つ。ところが国民健康・栄養調査では、日本人の平均は、五百ミリグラム台にとどまっていると報告されています。つまり、毎日およそ百五十ミリグラム、足りていません。三つ。そのカルシウムを腸から取り込む力そのものが、年とともに落ちていくとされています。骨は、カルシウムの貯金箱のようなものです。足りない日は、そこから崩して使われるとされています。毎朝の一つは、その貯金への、小さな入金です。入金しているつもりで、伝票が通っていない日がある。今日のお話は、その伝票の話です。そして、崩れた貯金は、ある日、台所で転んだ時に、はっきり分かります。私の母は、七十を過ぎてから、台所で一度、手をつきました。割れませんでした。ほんとうに、運が良かっただけです。あの時の音を、私は、まだ覚えています。

例えば、こんな方がいらっしゃるとします。三浦ヨシエさん、六十九歳。福井県で、長く和裁のお仕事をなさっていました。毎朝のヨーグルトは、十年以上、欠かしたことがなかったそうです。ところが去年、骨の検査で、同じ年頃の平均より少ない、と言われたそうです。私、毎朝食べてるのに。ご本人が、いちばん驚いたそうです。食べていたのは、いちご味の、小さな一つ。変えたのは、三つだけ。無糖に替える。きな粉をひとさじ。そして、食べるのを、朝ごはんのいちばん最後に回す。最初は、酸っぱくて敵わなかったそうです。これ、罰みたいな味がするねえ。そう言って、娘さんに笑われたそうです。半年ほどたって、正座から立ち上がるのが、少し楽になった気がする、と。検査の数字が変わったかどうかは、まだ分かりません。けれども、お孫さんに編み物を教える時間が、また戻ってきたそうです。

さて、二つ目の落とし穴です。これは、中身ではありません。温度です。冷蔵庫から出したまま、冷たいものを、そのまま流し込む。夏は、それが気持ちいいですよね。けれども冷たいものが一度に入ると、お腹は縮こまって、動きが鈍くなるとされています。縮こまった腸では、せっかくのカルシウムも、菌も、働きにくくなります。思い出してみてください。昔の朝ごはんに、冷たいものは、ほとんどありませんでした。温かいご飯、温かい味噌汁、湯呑みのお茶。体を温めてから、一日が始まりました。冷たいヨーグルトを、そのまま流し込む食べ方は、ここ何十年かの、新しい習慣です。明日の朝、一つだけ、試せることがあります。冷蔵庫から出して、顔を洗って、それから食べる。それだけで、十分ほど置いたことになります。もっと確かな直し方は、第二位でお話しします。

そして三つ目。これが、いちばん惜しい落とし穴です。骨のために、と、量を増やす。一日に二個、三個。大きな器のものを、朝と晩に。気持ちは、よく分かります。けれどもヨーグルトに入っているのは、カルシウムだけではありません。リンや、カリウムも、一緒に増えていきます。若い頃なら、余った分は、体が外に出してくれます。腎臓は、体の中の濾し器のようなものです。その濾し器も、年とともに、少しずつ目詰まりしやすくなっていきます。腎臓の働きが弱っていると言われている方は、乳製品を控えるように言われている場合があります。どうか、量を増やす前に、必ず、かかりつけの先生にご確認ください。そうでない方も、目安は、一日一つ。百グラムから二百グラムほどで、十分です。骨に届くかどうかは、量ではなく、入れ方で決まります。その入れ方を、これからお話しします。

それから、さきほどの、いちばん惜しい食べ方。時計ではなく、順番の話です。これは、この動画の、いちばん最後にお伝えします。お金も、手間も、かかりません。順番を変えるだけで、明日の朝から変わります。

ここまで聞いてくださって、ありがとうございます。今日のお話が良さそうだと思ってくださったら、良いねと、この動画を離れて暮らすご家族やお友達にも、そっと分けてあげてください。そして、気づいたことやご感想があれば、どうぞコメントで教えてくださいね。皆さんの声を励みに、もっと良いお話をお届けしていきます。

## A. KỊCH BẢN — PHẦN 2 (11:12 → hết)

さて、ここからは、その入金を、確かに通す食べ方です。三つ目から、いきましょう。台所の戸棚に、たいてい眠っているものです。節分でもないのに、袋の底に少し残っているもの。きな粉です。なぜ、きな粉なのか。ここが、今日いちばん大事なところです。骨は、カルシウムだけでできているのではありません。コンクリートだけの建物を、想像してみてください。見た目は、固い。けれども、揺れると、ぱきりと割れます。そこに通っている鉄筋が、たんぱく質です。カルシウムをいくら流し込んでも、鉄筋が足りない骨は、もろいままだとされています。きな粉は、大豆を炒って、挽いたもの。たんぱく質と、食物繊維が、一緒に入っています。ヨーグルトの菌は、その食物繊維を餌にするとされています。鉄筋と、菌の食べ物。ひとさじで、二つ入ります。量は、大さじ一杯ほど。入れすぎると、ぼそぼそして、飲み込みにくくなりますから、そこだけご注意ください。ここまでのお話が、お役に立っているようでしたら、コメント欄に、数字の、に、を書いていただけますか。

二つ目は、道具も、買い物も、いりません。冷蔵庫から出して、十分ほど、台所に置いておく。それだけです。人肌の温度です。先ほどの、二つ目の落とし穴を、覚えていらっしゃいますか。冷たいものを流し込むと、お腹が縮こまる、というお話でした。その、ちょうど反対をするわけです。急いでいる日は、器のまま、電子レンジで、二十秒ほど。ただし、熱くしては、いけません。熱を加えすぎると、せっかくの菌が弱ってしまうとされています。指を入れて、ぬるいと感じるくらいで、十分です。私も、寒い季節は、そうしています。温めたヨーグルトは、口当たりが変わって、まるでデザートのようになります。不思議ですよね。

そして、第一位です。これは、皆さんの冷蔵庫の中で、毎朝、捨てられているものです。蓋を開けたときに、上に溜まっている、うすい黄色の水。あの、上澄みです。邪魔なものだと思って、流しに捨てている方、いらっしゃいませんか。あれは、水ではありません。乳清と呼ばれるもので、たんぱく質やカルシウム、それにビタミンが溶け出しています。さきほどの言い方で申しますと、鉄筋とコンクリートが、いちばん濃く溶けている水です。それを流しに捨てて、残った白いところだけを召し上がっている。毎朝、いちばん大事なところだけを、捨てていることになります。やることは、一つ。捨てずに、スプーンで、十回ほど混ぜる。たった、それだけです。混ぜると、口当たりも、なめらかになります。正直に申しますと、私も、五十年近く、あれを捨てていました。今は、蓋を開けて、あの黄色い水を見ると、少し嬉しくなります。お金も、手間も、かかりません。続けやすいことだけが、続きます。

もう一つ、こんな話を、よく耳にします。岡部シゲルさん、七十四歳。岩手県で、中学校の事務を長く務めた方です。奥様に先立たれてから、朝は、パンとヨーグルトだけ。上澄みは、几帳面に、流しに捨てていたそうです。台所を汚さないのが、自分の役目だと思っていたそうです。ある日、娘さんに言われたそうです。お父さん、それ、捨てるものじゃないよ。それからは、混ぜてから召し上がっているそうです。今では、蓋を開ける前に、器とスプーンを並べて待つのが、朝の楽しみだそうです。一人の食卓にも、段取りがあると、背筋が伸びるものですね。

ここまで、お付き合いくださって、ありがとうございます。よろしければ、コメント欄に、数字の、さん、と書いていただけますか。さて、お約束した、いちばん惜しい食べ方です。時計の話ではありません、と申しました。順番です。朝、起きてすぐ。何も入っていないお腹に、ヨーグルトだけを、先に入れる。これが、いちばん惜しい入れ方です。空っぽの胃の中は、一日でいちばん酸が強い時間帯だとされています。せっかくの菌が、腸に着く前に、力を落としてしまいます。甘い味のものであれば、体の忙しさも、いちばん大きくなります。では、いつが良いのでしょうか。食事の、あとです。パンでも、ご飯でも構いません。少し召し上がったあと、いちばん最後にヨーグルト。胃の中が薄まって、菌が通りやすくなるとされています。買い替えるものは、何もありません。順番を、入れ替えるだけです。それから、朝がいいのか、夜がいいのか。その話も、よく耳にしますね。骨の作り替えは、夜のあいだに進むとされています。ですから、夕食のあとに回すのも、一つの手です。朝が習慣になっている方は、朝のままで結構です。大事なのは、時刻ではなく、空きっ腹に入れないこと。守るのは、その一つだけです。

今日のお話を、まとめます。避けたい食べ方は、三つ。甘みを加えたものを、無糖と同じつもりで毎日食べること。冷たいまま、流し込むこと。骨のためにと、量を増やすこと。続けたい食べ方も、三つ。第三位、きな粉をひとさじ。鉄筋を、一緒に入れる。第二位、人肌に温める。第一位、上澄みを捨てずに、混ぜる。そして、食べるのは、空きっ腹ではなく、食事のあと。明日の朝、一つだけ選ぶとしたら、上澄みを混ぜることから始めてみてください。一円も、一分も、かかりません。ところで、皆さんのヨーグルトには、何を入れていらっしゃいますか。きな粉、すりごま、それとも、ご自慢のものがおありでしょうか。コメント欄で、ぜひ教えてください。全て、読ませていただいております。それと、一つだけ教えてください。今日は、どちらの都道府県からご覧くださっていますか。毎朝の一つを、少し変えるだけです。その小さな入金が、十年先の、ご自分の足腰になります。転ばずに、自分の足で、台所に立てる。それは、ご家族に、何も言わなくて済むということです。迷惑をかけたくない、と口で言う代わりに、明日の朝、上澄みを混ぜる。いちばん静かな贈り物ではないでしょうか。今日のお話が良さそうだと思ってくださったら、高評価と、離れて暮らすご家族へのお知らせで、この食卓を応援していただけると嬉しいです。

最後に、一つだけ、大切なお願いです。この動画でお伝えした内容は、公表されている研究などをもとにした、健康に関する一般的な情報です。お一人おひとりに合わせた、医療のアドバイスではありません。持病のある方や、お薬を飲んでいる方は、食事を変える前に、必ず、かかりつけの先生にご相談ください。今日のお話が、先生との会話のきっかけになれば、何より嬉しいです。

今夜の食卓が、皆さんの明日の元気に、つながりますように。六十代からの食卓、みのりでした。どうか、ご自分の体を、大切になさってくださいね。

---

# B. ĐÓNG GÓI CTR / UPLOAD

### B1. 📊 ĐO CẦU KEYWORD — YouTube Data API, 30 ngày, JP/ja, long-form ≥8′ (2026-08-04)

> Đo bằng API thay Google Trends (Trends không render trên máy này). Lệnh tái chạy:
> `python tools\measure_kw_youtube.py "ヨーグルト 食べ方" "ヨーグルト 血糖値" "夜 ヨーグルト" "ヨーグルト 骨" --days 30`

| keyword | n (long-form/30d) | med view/ngày | max view/ngày | xử lý |
|---|---|---|---|---|
| **ヨーグルト 食べ方** | 17 | **719** | 4.833 | ⭐ **từ dẫn A1** — cầu cao nhất mà **sạch ad** |
| ヨーグルト 血糖値 | 19 | **719** | 33.680 | cầu đồng hạng + hit lớn nhất ngách, **nhưng chữ 血 tắt ad** → chỉ 概要欄 + tag |
| 夜 ヨーグルト | 15 | 395 | **33.679** | hit 578K/17 ngày nằm đúng đây → **A2** + lớp thưởng ở reveal (朝か夜か) |
| ヨーグルト 効果 | 20 | 601 | 33.680 | quá rộng, không phải từ dẫn |
| ヨーグルト 食べ合わせ | 22 | 123 | 2.518 | cung dày cầu thấp → **LOẠI** (và kênh đã có 4 video cùng họ) |
| **ヨーグルト 骨** | 21 | **48** | 2.255 | 🔴 **KHÔNG lên title** — nhưng vẫn là **trục cảm xúc của bài** (stake ≠ search intent) |
| カルシウム 不足 | 10 | 26 | 5.219 | top toàn kênh nước ngoài (Dr. Berg) → intent lệch, loại |
| 転倒 骨折 高齢者 | 8 | 11 | 1.362 | cầu thấp → chỉ dùng trong 概要欄/tag |
| ヘモグロビンa1c 下げる | 12 | 8 | 33.680 | **breakout cũ (đo 06-28) đã nguội** → giữ đề tài, bỏ cách gọi tên |
| 血糖値 下げる 食べ物 | 17 | 4 | 9.324 | bão hòa → loại |

⚠️ **Bài học ghi lại:** `骨` med 48 mà lại là thứ giữ chân mạnh nhất → **đừng lẫn "từ khóa để được tìm thấy" với "stake để người ta ở lại"**. Từ dẫn chọn theo volume; trục cảm xúc chọn theo nỗi sợ của tệp.

### 3 TITLE A/B (B2) — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `【60代は要注意】ヨーグルトの避けたい食べ方3つ｜毎朝続けたい正しい食べ方3つ` | 39 | ヨーグルト@9 · 食べ方@17 | P0 khung cảnh báo + cấu trúc kép 「X tránh + Y nên」 = format chủ lực của kênh |
| **A2** | `ヨーグルトは朝か夜か？60代が損している食べ方3つと、正しい食べ方3つ` | 36 | ヨーグルト@1 · 朝か夜@7 | đổi **keyword dẫn** sang 朝／夜 — nơi hit 578K/17 ngày của ngách đang nằm |
| **A3** | `そのヨーグルト、骨に届いていないかも｜60代が毎朝捨てている◯◯と正しい食べ方3つ` | 41 | ヨーグルト@3 | đổi **kiểu hook** sang P4 đảo nhận thức + ◯◯ giấu 第1位; kéo luôn stake 骨 lên title |

#### Title CHỐT

```
【60代は要注意】ヨーグルトの避けたい食べ方3つ｜毎朝続けたい正しい食べ方3つ
```

⚠️ Thứ tự chạy A/B (`ab-3title-3thumb.md` §1): đăng bằng **A1** → test 3 thumbnail ≥7 ngày → chốt ảnh → **rồi mới** xoay A2/A3, mỗi bản ≥7 ngày.

### B3. Tên file upload

```
yogurt-tabekata-machigai-60dai.mp4
```

### B4. 概要欄

#### 3 dòng đầu 概要欄 (vùng hook — không lời chào, keyword 1 lần)

```
毎朝のヨーグルト、無糖と同じつもりで「果物味」を食べていませんか。その一杯が、骨のためではなく、砂糖の時間になっているかもしれません。
この動画は、60代・70代の方に向けて、ヨーグルトの避けたい食べ方を3つ、毎朝続けたい食べ方を3つ、台所にあるものだけでお話しします。
見終わったあと、明日の朝すぐできることが1つ残るように作りました。第1位は、いま冷蔵庫の中で「捨てられているもの」です。
```

#### Mô tả đầy đủ (dán tiếp ngay dưới 3 dòng trên)

```
国民生活基礎調査では、介護が必要になったきっかけの上位に「骨折・転倒」が挙げられています。およそ7人に1人。しかも高齢の方の転倒がいちばん多い場所は、外ではなく家の中だとされています。その骨をつくる材料は、毎日の食事から入ってきます。厚生労働省の食事摂取基準では、カルシウムの1日の目安は60代でおよそ650〜750mg。ところが国民健康・栄養調査では、日本人の平均摂取量は500mg台にとどまっていると報告されています。無糖ヨーグルト100gのカルシウムはおよそ120mg。毎朝の1つは、その足りない分への小さな「入金」です。ただし、食べ方を間違えると、その入金の伝票が通らないことがあります。

前半は、60代が避けたい食べ方を3つ。①甘みを加えたもの（果物味）を無糖と同じつもりで毎日食べること：100gで角砂糖2〜3個分ほどの甘みが入っているものもあります。空腹の胃に甘いものだけが先に入ると、体は急に忙しくなるという報告があります。②冷蔵庫から出したまま冷たいまま流し込むこと：お腹が縮こまり、動きが鈍くなるとされています。③骨のためにと量を増やすこと：カルシウムだけでなくリンやカリウムも一緒に増えます。腎臓の働きが弱っていると言われている方は乳製品を控えるよう言われている場合がありますので、必ずかかりつけの先生にご確認ください。目安は1日1つ、100〜200gほどです。

後半は、毎朝続けたい食べ方を3つ。第3位はきな粉をひとさじ：骨はカルシウムだけでできているのではありません。コンクリートだけの建物は揺れると割れます。そこに通る鉄筋がたんぱく質です。きな粉は大豆のたんぱく質と食物繊維が一緒に入っていて、ヨーグルトの菌は食物繊維を餌にするとされています。第2位は人肌に温める：冷蔵庫から出して10分、または電子レンジで20秒ほど。熱くしすぎると菌が弱ってしまうとされていますので、ぬるいと感じるくらいで。第1位は、蓋を開けたときに上に溜まっているうすい黄色の水＝乳清を、捨てずに10回ほど混ぜること。たんぱく質やカルシウム、ビタミンが溶け出している部分です。

そして最後に、いちばん惜しい食べ方をお話しします。時計の話ではありません。順番の話です。朝か夜かで悩んでいる方にも、ひとつの答えをお伝えします。

【目次】
00:00 介護のきっかけ3番目は病気ではない／骨折と転倒
01:22 避けたい食べ方①：果物味・加糖を無糖と同じつもりで
04:07 このチャンネルについて
04:48 骨は「カルシウムの貯金箱」／毎日150mg足りていない
06:23 体験談：10年毎朝食べていたのに（69歳・元和裁）
07:43 避けたい食べ方②：冷たいまま流し込む
09:00 避けたい食べ方③：骨のためにと量を増やす
11:09 続けたい食べ方 第3位：きな粉（骨の「鉄筋」を入れる）
12:43 第2位：人肌に温める（熱くしすぎないコツ）
13:47 第1位：上澄み（乳清）を捨てずに混ぜる
15:19 体験談：几帳面に上澄みを捨てていた（74歳・元中学校事務）
16:28 いちばん惜しい食べ方は「順番」／朝か夜かの答え
18:08 今日のまとめ／明日の朝できること1つ

※この動画の内容は、公表されている研究や公的機関の資料をもとにした、健康に関する一般的な情報です。個々の方への医療アドバイスではありません。持病のある方、お薬を飲んでいる方、カリウムやリン、乳製品の量を控えるように言われている方は、食事を変える前に必ずかかりつけの先生にご相談ください。

【出典】
・厚生労働省「国民生活基礎調査」介護が必要になった主な原因（骨折・転倒）
・厚生労働省「日本人の食事摂取基準（2020年版）」カルシウムの推奨量
・厚生労働省「国民健康・栄養調査」カルシウム摂取量の平均
・文部科学省「日本食品標準成分表」ヨーグルト（全脂無糖）100gあたりのカルシウム量

【音声】VOICEVOX:青山龍星

#ヨーグルト #ヨーグルトの食べ方 #60代
```

✅ **目次 là mốc THẬT, đo từ `subs.srt` sau render 2026-08-05** (không còn là mốc tính). Lệch lớn nhất so với bản dự tính chỉ 4 giây.

### B5. タグ (26 — 3 tag đầu là bộ nhận diện kênh, cố định mọi video)

```
60代 食べてはいけない, 60代 食事, 60代からの食卓, ヨーグルト, ヨーグルト 食べ方, ヨーグルト 血糖値, ヨーグルト 骨, 夜 ヨーグルト, 朝 ヨーグルト, 加糖ヨーグルト, 無糖ヨーグルト, ヨーグルト 乳清, ホエー 栄養, きな粉 ヨーグルト, ホットヨーグルト, カルシウム 不足, カルシウム 高齢者, 骨折 転倒 予防, 転倒 高齢者, 食べる順番, 血糖値 食べ方, 食事摂取基準 カルシウム, 60代 健康, 70代 健康, シニア 健康, 高齢者 食事
```
⚠️ Bài học 2026-08-01: KHÔNG bê tag video khác sang (麦茶/熱中症/腎臓/リン/漬物), KHÔNG tag tên người thật.

### B6. Thumbnail — 3 bản A/B (khuôn v5 TEXT-DOMINANT cảnh báo)

**Xoay vòng chống lặp:** video 10 麦茶 dùng **cột chữ PHẢI + HẬU QUẢ VÀNG** → video này **cột chữ TRÁI + HẬU QUẢ ĐỎ**.

| | dòng 1 (trắng) | dòng 2 **ĐIỂM NHẤN KHỔNG LỒ** (đỏ) | dòng 3 (vàng) | biến thử |
|---|---|---|---|---|
| **T1** baseline | `毎朝これ？` (5) | **`大損`** (2) | `捨てないで` (5) | mốc so — khuôn kênh, cột chữ TRÁI, HẬU QUẢ đỏ |
| **T2** đổi 1 biến HÌNH | y hệt T1 | y hệt T1 | y hệt T1 | **chỉ đổi ảnh**: bàn ăn sáng → **cận hộp yogurt mở nắp thấy lớp nước vàng** (vật đáp án của dòng 3). Chữ không đổi 1 ký |
| **T3** đổi LAYOUT | `毎朝これ？` | **`大損`** (to hơn T1) | — bỏ dòng 3 | 2 dòng + **mặt cận** biểu cảm まさか, cột chữ đảo sang **PHẢI** |

🔴 **Vì sao dòng chính là `大損` (2 ký):** gate `audience-45plus.md` §1 đòi dòng chính **≤6 ký VÀ cao ≥1/3 khung**. Cột chữ ~50% bề ngang (960 px) → 4 ký bị trần bề ngang chặn ở ~22% chiều cao, không đạt gate; 2 ký thì đạt thoải mái (bài học §6.4: dòng chính phải về 2–4 ký).
🟡 **Claim đọc-rời-ra phải đúng** (bài học video 10 `その麦茶`→`麦茶だけ`): `大損` một mình = "đang lỗ", đúng nội dung (đổ bỏ 乳清 + trả tiền cho đường). **KHÔNG** viết `ヨーグルトは大損` — video nói yogurt tốt, cái sai là cách ăn.

**BỘ PROMPT ẢNH — chốt 2026-08-05.** Ý tưởng bán cú click: **thứ mà gần như ai cũng đang đổ xuống bồn rửa mỗi sáng.** Layout xoay theo A6 (video 10 dùng người → video 11 lấy **món macro** làm mặc định, mặt bà cụ chỉ ở T3).

```
T1 (baseline · MÓN MACRO · chủ thể PHẢI, trống nửa TRÁI) → 11_scene_ai.jpg
photorealistic macro food photo, an opened white tub of plain Japanese-style yogurt on a bright
wooden kitchen table, the lid just removed and resting beside it, a clear pool of pale yellow
watery liquid visible on the smooth white surface, a stainless steel spoon resting in the tub,
soft bright morning light from a window, shallow depth of field, creamy appetizing texture,
the tub and spoon LARGE on the RIGHT half of the frame filling most of the height, the LEFT half
is plain out-of-focus bright wooden table with empty space, high contrast, 16:9,
no text, no letters, no logo, no brand labels, no people

T2 (đổi ĐÚNG 1 biến hình: HÀNH ĐỘNG SAI · chữ giữ nguyên) → 11_scene_ai_sink.jpg
photorealistic close-up, an elderly person's hands tilting an opened white tub of plain yogurt
over a stainless steel kitchen sink, a thin stream of pale yellow watery liquid pouring out and
running toward the drain, the white yogurt still inside the tub, bright kitchen daylight,
hands and tub LARGE on the RIGHT half of the frame, LEFT half is a plain bright kitchen counter
with empty space, sharp focus, the feeling of wasting something valuable, 16:9,
no text, no letters, no logo, no brand labels, no face

T3 (đổi LAYOUT: GƯƠNG MẶT KÊNH · chủ thể TRÁI, trống nửa PHẢI) → 11_scene_ai_face.jpg
photorealistic close-up portrait of a Japanese woman in her late 60s, short gray hair, wearing a
beige apron over a blue floral patterned cardigan, standing in a bright home kitchen in the
morning, holding the lid of a yogurt tub in one hand and the opened tub in the other, looking
down at the pale yellow liquid on the yogurt surface, eyebrows raised and mouth slightly open in
a startled "have I been throwing this away" expression, warm bright morning light, her face and
the tub LARGE on the LEFT half of the frame filling most of the height, the RIGHT half is a plain
bright kitchen wall left empty, sharp focus, 16:9,
no text, no letters, no logo, no brand labels
```

### B6b. ⭐ PHƯƠNG ÁN ĐANG DÙNG — CHỮ GEN LUÔN TRONG ẢNH (user chốt 2026-08-05)

> User: *"tao muốn prompt có chữ luôn không cần mày đè chữ"*. → Không chạy `make_thumb.py` cho bộ này; chữ nằm sẵn trong ảnh gen. **Con dấu 「食卓」 VẪN đóng bằng tool** (`brand_stamp.py --style seal`) — nhận diện phải cố định từng pixel, không để AI vẽ lại mỗi video.

**Chữ chốt (cả 3 bản phải đúng từng ký tự):** dòng 1 `毎朝これ？` trắng · dòng 2 **`大損`** ĐỎ khổng lồ · dòng 3 `捨てないで` vàng. T3 bỏ dòng 3.

```
T1 (baseline · MÓN MACRO · món PHẢI, chữ TRÁI) → 11_thumb_ai.jpg
photorealistic macro food photo for a YouTube thumbnail, an opened white tub of plain
Japanese-style yogurt on a bright wooden kitchen table, lid just removed and resting beside it,
a clear pool of pale yellow watery liquid on the smooth white surface, a stainless steel spoon
resting in the tub, soft bright morning light, creamy appetizing texture, the tub and spoon LARGE
on the RIGHT half of the frame. On the LEFT half, bold Japanese poster typography stacked in three
lines, thick black outline around every character, slightly tilted for energy:
line 1 small white text "毎朝これ？",
line 2 GIANT bright red text "大損" filling more than one third of the frame height,
line 3 medium yellow text "捨てないで".
Keep the bottom-left corner of the frame free of text (reserved for a channel stamp).
Exactly these Japanese characters, correct stroke shapes, nothing misspelled, no other text
anywhere, no watermark, no logo, no brand labels, no people, 16:9

T2 (đổi ĐÚNG 1 biến hình: HÀNH ĐỘNG SAI · chữ y hệt T1) → 11_thumb_ai_sink.jpg
photorealistic close-up for a YouTube thumbnail, an elderly person's hands tilting an opened white
tub of plain yogurt over a stainless steel kitchen sink, a thin stream of pale yellow watery
liquid pouring out toward the drain, white yogurt still inside the tub, bright kitchen daylight,
hands and tub LARGE on the RIGHT half of the frame. On the LEFT half, bold Japanese poster
typography stacked in three lines with thick black outline:
line 1 small white text "毎朝これ？",
line 2 GIANT bright red text "大損" filling more than one third of the frame height,
line 3 medium yellow text "捨てないで".
Keep the bottom-left corner of the frame free of text (reserved for a channel stamp).
Exactly these Japanese characters, correct stroke shapes, no other text anywhere, no watermark,
no logo, no brand labels, no face, 16:9

T3 (đổi LAYOUT: GƯƠNG MẶT KÊNH · mặt TRÁI, chữ PHẢI, 2 dòng) → 11_thumb_ai_face.jpg
photorealistic close-up portrait for a YouTube thumbnail, a Japanese woman in her late 60s, short
gray hair, beige apron over a blue floral patterned cardigan, in a bright home kitchen in the
morning, holding a yogurt tub lid in one hand and the opened tub in the other, looking down at the
pale yellow liquid on the yogurt surface, eyebrows raised and mouth slightly open in a startled
expression, warm morning light, her face and the tub LARGE on the LEFT half of the frame. On the
RIGHT half, bold Japanese poster typography stacked in two lines with thick black outline:
line 1 white text "毎朝これ？",
line 2 GIANT bright red text "大損" filling more than one third of the frame height.
Exactly these Japanese characters, correct stroke shapes, no other text anywhere, no watermark,
no logo, no brand labels, 16:9
```

**Nhận ảnh về → tao làm 3 việc:**
```bat
rem 1) đóng dấu nhận diện (BẮT BUỘC, không bỏ)
python toolsrand_stamp.py 06_VIDEO	_yogurt-tabekata	_thumb_ai.jpg ^
       06_VIDEO	_yogurt-tabekata	humb_T1_yogurt.png --style seal
rem 2) xuất bản preview 168px + 120px để duyệt 4 cửa
rem 3) PNG >2MB thì xuất kèm .jpg q95
```

**✅ T1 ĐÃ XONG 2026-08-05** (user gen ảnh, tao hậu kỳ) — `thumb_T1_yogurt.png` 1,28 MB + `.jpg` q95 0,40 MB dự phòng.

| Gate | Kết quả |
|---|---|
| Glyph 3 dòng | ✅ `毎朝これ？` · `大損` · `捨てないで` đúng nét, không ký tự rác |
| Dòng chính ≤6 ký | ✅ `大損` = 2 ký |
| Dòng chính ≥1/3 khung (`audience-45plus.md` §1) | ✅ **412px = 38,1%** chiều cao (đo bằng mask pixel đỏ, không ước lượng) |
| ≤3 dòng | ✅ 3 |
| Chữ không đè món | ✅ chữ 45,6% bề ngang bên trái · hộp yogurt nguyên bên phải |
| Gate 168px | ✅ đọc được `大損`, `捨てないで`, và con dấu `食卓` |
| 120px | ✅ còn đọc được dòng đỏ |
| Trần 2 MB | ✅ 1,28 MB |
| Nhãn hiệu / chữ 血 / bác sĩ | ✅ hộp trắng trơn, không có |
| Claim đọc-rời-ra | ✅ `大損` + `捨てないで` = đúng 第1位 (乳清 bị đổ bỏ) |
| **≥1 mặt biểu cảm** | ❌ **KHÔNG có** — T1 là món macro. **T3 (gương mặt kênh) gánh gate này**; nếu chỉ đăng 1 bản thì phải dùng T3 |

**Hậu kỳ đã làm:** ① xoá watermark ✦ của generator ở góc dưới-phải — dùng đúng cách đã chốt (`connected-component + assert`, comp **787 px**, bbox không lan sang chủ thể) rồi **vá theo TỪNG DÒNG** (nội suy ngang) để giữ thớ gỗ, soi zoom ×4 xác nhận sạch ② ảnh gen ra **2752×1536 = 1,7917** ≠ 16:9 → crop 21px mép PHẢI (phía không có chữ) rồi resize 1920×1080 ③ đóng dấu `--style seal --corner tr`.

🔴 **Dấu phải dời lên góc TRÊN-PHẢI ở video này** vì cột chữ chiếm hết mép dưới-trái → dấu ở nhà mặc định đè mất 2 ký của 「捨てないで」. Đã thêm cờ `--corner` vào `brand_stamp.py` (mặc định vẫn `bl`) + ghi luật `02_THUMBNAIL_TITLE_RULES.md` §A5.5b: **prompt từ nay phải có câu `keep the bottom-left corner free of text`** — dời dấu là chữa cháy, chừa góc mới là cách đúng.

🔴 **Rủi ro đã biết của phương án này (kiểm ngay khi ảnh về, không đoán):**
1. **Glyph Nhật sai nét** — generator hay bịa kanji. Tao soi từng ký tự ở cỡ full; sai 1 nét là **loại**, gen lại. `大損` dễ đúng nhất (2 ký), `捨てないで` dễ sai nhất.
2. **Cỡ chữ không kiểm soát được** → có thể rớt gate `audience-45plus.md` §1 (dòng chính ≥1/3 khung). Prompt đã ghi `filling more than one third of the frame height` nhưng model không đảm bảo; **rớt 168px là loại**.
3. ⚠️ **Nhiễu bài test A/B:** luật `ab-3title-3thumb.md` đòi T2 khác T1 **đúng 1 biến**. Chữ gen ra thì mỗi lần một cỡ/một dáng → T1 vs T2 lẫn 2 biến (hình + chữ), CTR thắng cũng không biết vì cái gì. Muốn test sạch thì phải **cắt vùng chữ của T1 dán sang T2**, hoặc quay lại chữ-đè-bằng-tool (§B6c).
4. Chữ trong ảnh **không sửa lại được** khi muốn đổi wording — đổi chữ = gen lại ảnh.

### B6c. (DỰ PHÒNG) chữ đè bằng tool — dùng khi glyph gen bị sai

**Gate phải đạt khi nhận ảnh về** (đo trước khi ghép chữ, luật `02_THUMBNAIL_TITLE_RULES.md` A5): chủ thể **≤~50% bề ngang VÀ lệch hẳn một bên**, nửa còn lại trống → mới đặt được cột chữ. Ảnh fail gate mà vẫn muốn dùng → `--panel --panel-fade 340` (ảnh tan dần vào bóng, KHÔNG lộ mép cắt thẳng).

**Curiosity device = 「これ」** (A4, chọn 1/video): 「毎朝これ？」 ở dòng 1 + đáp án 「捨てないで」 ở dòng 3, còn **vật đáp án (lớp nước vàng) để NGUYÊN không mosaic** — vì chính nó là cú "ơ, cái đó là thứ tốt à?".

⚠️ **Bài học video 10 — đừng để generator từ chối:** cấm cụm bệnh lý (`suffering`, `sweat`, `flushed`) và **cấm liệt kê negative dính từ y tế** (`no doctors / no hospital / no medical equipment` tự kéo cờ). Bộ trên đã sạch. Thang gỡ nếu vẫn bị chặn: ① bỏ `startled`, giữ `looking down at the tub` ② đổi sang ông cụ ③ bỏ mặt, chỉ lấy **bàn tay + hộp + thìa**.

**Lệnh render (sau khi có ảnh về `06_VIDEO/11_yogurt-tabekata/`):**

```bat
rem T1 — baseline: cột chữ TRÁI, HẬU QUẢ đỏ
python tools\make_thumb.py 06_VIDEO\11_yogurt-tabekata\11_scene_ai.jpg ^
  06_VIDEO\11_yogurt-tabekata\thumb_T1_yogurt.png ^
  --stack l --focus right --maxw 0.50 --pop --size1 150 --size2 400 --size3 175 ^
  --line1 "毎朝これ？" --line2 "大損" --line3 "捨てないで" ^
  --color1 white --color2 red --color3 yellow

rem T2 — chỉ đổi ẢNH (hộp yogurt thấy lớp 乳清), chữ giữ nguyên
python tools\make_thumb.py 06_VIDEO\11_yogurt-tabekata\11_scene_ai_sink.jpg ^
  06_VIDEO\11_yogurt-tabekata\thumb_T2_sink.png ^
  --stack l --focus right --maxw 0.50 --pop --size1 150 --size2 400 --size3 175 ^
  --line1 "毎朝これ？" --line2 "大損" --line3 "捨てないで" ^
  --color1 white --color2 red --color3 yellow

rem T3 — đổi LAYOUT: 2 dòng + mặt cận, cột chữ PHẢI
python tools\make_thumb.py 06_VIDEO\11_yogurt-tabekata\11_scene_ai_face.jpg ^
  06_VIDEO\11_yogurt-tabekata\thumb_T3_face.png ^
  --stack r --focus left --maxw 0.50 --pop --size1 210 --size2 460 ^
  --line1 "毎朝これ？" --line2 "大損" --color1 white --color2 red
```

- 🏷️ Dấu nhận diện kênh cả 3 bản: `python tools\brand_stamp.py <file> --style seal` (con dấu 「食卓」 góc dưới **TRÁI** — góc dưới phải là của timestamp YouTube).
- ⚠️ **4 cửa duyệt** trước khi giao (che chữ ra đúng chủ đề / cạnh mẫu Phần E / 120px / 🔴 **168px đọc được `大損` + nhận ra biểu cảm**). Rớt 168px → render lại, không đem test A/B. PNG >2 MB → xuất thêm `.jpg` q95.

### B7. Lớp THỦ CÔNG — `tegami` 撮影リスト (2 clip, tay thật, KHÔNG lộ mặt)

> ⭐ Ca **rẻ nhất** của lớp thủ công từ trước tới giờ: không vào bếp, không nấu — 1 hộp yogurt + 1 thìa + 1 túi kinako, điện thoại chúc xuống bàn.

| # | slot (cue) | Thao tác quay | Câu thoại khớp | Dài |
|---|---|---|---|---|
| A | ~14:00 (第1位) | Mở nắp hộp yogurt để **thấy rõ lớp nước vàng nhạt** trên mặt → thìa khuấy đúng **10 vòng** cho tan hết vào phần trắng. Quay từ trên xuống, nền khăn/thớt trơn màu đậm | 「捨てずに、スプーンで、十回ほど混ぜる。」 | 12–18s |
| B | ~11:30 (第3位) | Múc **1 thìa canh きな粉** rắc lên mặt yogurt trắng → khuấy nhẹ 3–4 vòng thành màu nâu nhạt | 「ひとさじで、二つ入ります。」 | 12–18s |

```bash
python E:\Claude\Projects\_media_library\ingest_handmade.py ingest "<file thô>" ^
  --channel youtube-jp-shokutaku --hm-kind tegami --tags "ヨーグルト 乳清 きな粉 手元" --speed 1.6
python E:\Claude\Projects\_media_library\ingest_handmade.py place 06_VIDEO/11_yogurt-tabekata ^
  --map <slot>=<tên> --slides 04_SCRIPTS/11_yogurt-tabekata_SLIDES_photo.json --used-by youtube-jp-shokutaku/11_yogurt-tabekata
python E:\Claude\Projects\_media_library\ingest_handmade.py sheet 06_VIDEO/11_yogurt-tabekata -o sheet.jpg
```
- Cờ SLIDES là **`"handmade": true`** (KHÔNG phải `"video": true`). Tháo đồng hồ/nhẫn, nền trơn, **hộp yogurt phải bóc/che nhãn hiệu**.
- 🟡 Không quay được → ghi 1 dòng `HANDMADE: hoãn — <lý do> — <ngày>` (`handmade-layer.md` §1.1). **KHÔNG lấp bằng ảnh/clip stock.** ⚠️ 3 video liên tiếp hoãn → dừng đăng kênh.

### B8. ✅ Quét compliance (`.claude/rules/youtube-compliance.md`)

| Điểm | Kết quả |
|---|---|
| Từ tắt-ad ở title/thumbnail | ✅ sạch — không 殺/死/自殺/虐待, **không chữ 血** (血糖値 chỉ ở 概要欄 + tag). 「要注意」「大損」 an toàn. 骨折/転倒 **không nằm trong nhóm cấm** nhưng cũng không lên title/thumbnail |
| Persona | ✅ không 医師/先生/管理栄養士/専門家; có câu tự phủ. **Ký ức về mẹ** = cảm xúc + hành vi, KHÔNG phải trải nghiệm y khoa → hợp luật |
| Claim khỏi bệnh | ✅ không 治る/完治/薬の代わり/絶対. **Anecdote cố ý KHÔNG hứa số liệu cải thiện** (「検査の数字が変わったかどうかは、まだ分かりません」) — khác hẳn hit 578K của ngách vốn hứa 「下がる」 |
| Tên thật hãng/người/viện | ✅ không tên sản phẩm/thương hiệu; 4 nguồn nêu tên đều là cơ quan công (厚労省 ×3 · 文科省 成分表) |
| Nhóm rủi ro | ✅ cảnh báo điều kiện tại chỗ (腎臓 × 乳製品 → かかりつけの先生) + trần lượng 一日一つ + disclaimer cuối |
| Số liệu 骨折・転倒 | ✅ nói dạng 「上位に挙げられている」「およそ七人に一人」「〜だとされています」 — không bịa thứ hạng chính xác, không bịa % lẻ |
| altered/synthetic | ✅ không phải tick — không footage AI realistic; thumbnail AI nhân vật hư cấu + giọng TTS = production assistance |
| Inauthentic | ✅ góc riêng (食べ方 · 順番 chưa từng làm), KHÔNG phải 食べ合わせ thứ 5, layout thumbnail xoay (cột TRÁI + đỏ) |
| Tình tiết title/thumbnail có thật | ✅ 「避けたい食べ方3つ」= ワースト①②③ · 「捨てないで」= 第1位 上澄み · 「大損」= 角砂糖換算 + 乳清 bị đổ |

### B9. Lịch đăng đề xuất

`upload-schedule.md` §0.9: shokutaku **T2·T4·T6 — 12:00 JST (10:00 VN)**, 3 video/tuần. Hôm nay **2026-08-04 là T2** → slot khả thi gần nhất **T4 06/08 12:00 JST**. Đề tài không mùa vụ, không cần ép sớm.
⚠️ Chưa render thì chưa có `subs.srt` → chưa chốt được 目次 → **bỏ slot còn hơn đăng với 目次 lệch**.

### B10. ✅ SLIDES + ảnh (dựng 2026-08-04)

- File: `04_SCRIPTS/11_yogurt-tabekata_SLIDES_photo.json` — **99 entry, 100% ẢNH THẬT, 0 card chữ** (user chốt: *"chỉ có ảnh hoặc video, không có slide"*). Không entry nào `"video": true` → giữ bản sắc kênh (ảnh + pan chậm).
- **Nhịp dựng đạt gate `audience-45plus.md` §2:** **4,71 lần đổi hình/phút** (trần 6) · TB **12,7 giây/entry** · **ngắn nhất 6,1 giây** (sàn 6) · dài nhất 27,6s. Kiểm bằng code, không ước lượng.
- **Mọi `match` verify là substring DUY NHẤT** trong `_TTS.md` + thứ tự tăng dần theo kịch bản (script tự chặn, exit 1 nếu lệch). ⚠️ Sửa 1 câu = chết cue → chạy lại `scratchpad/build_11_slides.py`.
- ⭐ **Entry 0 = `close up bowl of plain white yogurt with a spoon on a bright kitchen table`** → `media-library.md` §2.0: frame đầu là **chủ thể ヨーグルト** (liền mạch thumbnail) dù giọng đang đọc con số 介護・転倒.
- **Badge `rank` 6 chỗ:** その1 (甘みを加えたもの) · その2 (温度) · その3 (量) · 第3位 (きな粉) · 第2位 (人肌) · 第1位 (上澄み).
- **Ảnh "cuốn hút" — ưu tiên macro + ẩn dụ vật thể** thay vì ảnh mood chung: 角砂糖 xếp trên thìa · **hộp yogurt mở nắp thấy lớp 乳清** · thìa khuấy xoáy macro · rót 乳清 xuống bồn rửa · **tường bê tông NỨT** + **khung thép rebar** (ẩn dụ 鉄筋) · **con heo đất + bỏ xu vào** (ẩn dụ 貯金箱) · phễu giấy lọc cà phê + rọ chắn bồn tắc (ẩn dụ 濾し器) · thìa rơi trên sàn bếp.
- ⚠️ **KHÔNG ép `src:commons`** cho vật Nhật (bài học video 10: Commons trả ảnh bách khoa) → mọi query là **mô tả CẢNH tiếng Anh**; query có người đều ép `asian/japanese` hoặc lấy **bàn tay** thay mặt (`feedback_anh_nguoi_chau_a_dong_tac`).
- Tải ảnh (chạy nền): `06_VIDEO	_yogurt-tabekata
un_fetch.cmd` → log `fetch.log`. Duyệt: `python tools\contact_sheet.py 06_VIDEO/11_yogurt-tabekata/slides_img_photo 04_SCRIPTS/11_yogurt-tabekata_SLIDES_photo.json -o 06_VIDEO/11_yogurt-tabekata/_sheet.jpg`
- ⛔ **Duyệt contact sheet bằng MẮT trước render** — ô đầu che chữ phải ra ngay "video nói về ヨーグルト"; ô lệch → đổi `q`, xoá `slide_XX.jpg` rồi tải lại đúng slide đó.

### B11. Handoff render

```bat
python tools\check_coldopen.py 11
python ..\youtube-jp-health\tools\video_render.py 04_SCRIPTS\11_yogurt-tabekata_TTS.md ^
  --channel shokutaku --slides 04_SCRIPTS\11_yogurt-tabekata_SLIDES_photo.json ^
  --img-dir 06_VIDEO\11_yogurt-tabekata\slides_img_photo
```
- Chạy **NỀN** qua `.cmd` + log `06_VIDEO/11_yogurt-tabekata/render.log` + `EXITCODE` (`render-background.md`).
- ⛔ **Render demo 3 đoạn nghe trước:** ① cold open 「骨折と、転倒です。」 ② ký ức mẹ 「あの時の音を、私は、まだ覚えています。」 ③ đỉnh bài 「たった、それだけです。」
- Đổi asset xong mới render lại → đọc log tìm dòng `CŨ HƠN … → render lại` (`render-background.md` §2.5).
