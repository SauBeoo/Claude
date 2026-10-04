# 19_haisuiko-naze-tsumaru — キッチンの排水口は「なぜ」詰まるのか（温度の話）

# TARGET_QUERY: キッチンの排水口
# INTENT: なぜ

- **Chế độ:** B (viết mới) — ⚠️ **KHÔNG rewrite.** User chốt 2026-08-12: *"tao không muốn viết giống nó, tao muốn có chính kiến riêng"*
- **Trục:** 🔥 **signature 忘れられた技術** (lần cuối #16 漬物, cách 3 video — trả nợ đúng luật ~4 video/lần)
- **Peer-target:** `キッチンの排水口に絶対に流してはいけない5つのもの` (`sqB200m33fw`, 昔の人の知恵, 357.815 view / 34.692 v/ngày, 23,0′) — bám **ĐỀ TÀI + CỤM**, KHÔNG bám khuôn câu chữ. Nguồn: `01_SOURCES/2026-08-12_haisuiko-nagashite-wa-ikenai.txt`
- **Độ dài:** **6.491 ký ≈ 19,2′** @337,5 ký/phút · **N=5 SÓNG** · **79 tag** nhấn nhá
  - ⚖️ Ngắn hơn mục tiêu 22,5′. Cố ý **không nhồi cho đủ phút**: `CHANNEL_DIAGNOSIS_2026-08-11.md` §3 đã tích phân đường cong thật → **độ dài KHÔNG phải biến**; 19,2′ vẫn trong dải thực của benchmark (**15,2–31,3′**). Nhồi chữ là đúng thứ O15 sinh ra để chặn.
- ✅ **GATE `check_coldopen.py 19` → PASS, 0 FAIL, 0 WARN** (16 luật, gồm **O16**). Vào bài **giây 18** · cửa 0–45s **0 câu không trả tiền** · gap payoff max **1′02″** · 10 cú lật · 11 câu MỞ · **loop lớn đóng 88%** · **0 tag lệch đầu dòng**

## 🔴 v2 — VIẾT LẠI TOÀN BỘ 2026-08-12 (user: *"giữ chân người xem, 9–10 điểm, phải có hồn, không rời rạc"*)

**Bản v1 tự chấm 6,5/10.** Bốn lỗi thật, và cả bốn đều là lỗi CẤU TRÚC chứ không phải câu chữ:

| lỗi v1 | v2 sửa thế nào |
|---|---|
| 🔴 **PAYOFF TƯỚC HY VỌNG.** Người xem đến vì *"cống nhà tôi đang chậm"*; v1 kết luận 「溶かす力はありません」 = **bạn đã thua rồi, đi gọi thợ**. Câu tự khen "đắt nhất" (「手を打つ道は、はじめから閉じていました」) thực chất giết retention ở phút 8 | **Tách nhiệt độ nóng chảy của DẦU khỏi TINH BỘT** → mỡ tan **40–50℃**, ống chết **60℃** ⇒ **CÓ khe 20 độ, và nó MỞ cho dầu**. Người xem có **việc làm ngay tối nay** (50℃ × 30 giây). Nghịch lý 60℃ vẫn còn nhưng chỉ áp cho tinh bột ⇒ **sắc hơn, không tước hy vọng** |
| **HOOK không có STAKE.** Bỏ hết số tiền (đúng) nhưng **không thay bằng gì**; 「温度です。」 là reveal không hậu quả | Stake mới **có cơ chế, không cần tiền**: 「あの遅さは、ひとりでに直ることはありません。今日より明日、必ず少しだけ遅くなります」 + 「一晩ごとに、その分が一枚、硬いほうへ移っていきます」 ⇒ **cửa sổ hết hạn theo THỜI GIAN** |
| 🔴 **GAME chính gate của mình.** O7 báo thiếu stake → v1 nhét chữ `におい` cho regex ăn. Regex hết kêu, vấn đề còn nguyên | Stake thật ở câu 2, không phải chữ mồi |
| 🔴 **Sóng 4 PHÁ xương sống.** Xương sống là nhiệt độ mà sóng 4 mở bằng 「温度に関係なく」 = tự nói "phần này không liên quan" → **rời rạc** | コーヒーかす thành **NGOẠI LỆ CHỨNG MINH QUY LUẬT**: 「かすには、溶ける温度がありません。50度でも90度でも同じ砂粒」 ⇒ 3 trạng thái sạch: **dầu戻せる · tinh bột戻せない · かす温度無関係**, và cả 3 chỉ về **một chỗ: cửa vào** |
| **Chất người tới phút ~16.** Cả bài 1 khoảnh khắc người, 15 phút đầu là bài giảng khô | Mẹ + 油こし器 + thoại 「まだ、匂いが立っていないでしょう。」 **dời lên phút ~5**; thêm callback đóng bài bằng cảm xúc (「母の缶は、もうありません」) = mũi ⑤ |

⭐⭐ **XƯƠNG SỐNG v2 — MỘT khe nhiệt độ, ba trạng thái:**
```
mỡ tan 40℃ ──────── khe 20 độ MỞ ──────── ống chết 60℃ ──── tinh bột cần >60℃ (khe ĐÓNG)
                                                              かす: không đổi pha (khe vô nghĩa)
```
⇒ **dầu cứu được sau khi đã đổ · tinh bột buộc chặn cửa vào · かす cũng chỉ có cửa vào** ⇒ ba tính chất khác nhau, **một kết luận duy nhất** → nối vào 昔の台所 (không có gì đi vào ống).

- **Ngày viết:** 2026-08-12
- **Voice:** VOICEVOX 青山龍星 / ノーマル / speed 0.9 / intonation 1.15

---

## 🧭 CHÍNH KIẾN — chỗ bài này KHÁC peer (đọc trước khi sửa bất cứ gì)

| | peer | bài này |
|---|---|---|
| khung | **5 mục CẤM rời nhau** (油/薬剤/カス/でんぷん/塗料) | **1 xương sống: NHIỆT ĐỘ** — 3 thứ tắc vì cùng một cơ chế đổi pha khi nguội |
| uy tín | 「30年以上携わってきた経験から」 (nghề) | **原典 thật** — persona 案内役 vô danh, cấm xưng nghề |
| số liệu | **0 nguồn** (10万円 · 35〜55万円 · 80〜150万円) | mọi số có nguồn, **không tra ra thì BỎ số** |
| thuật ngữ | `ファットバーグ` (chuyện London, không nguồn Nhật) | **`オイルボール`** — hiện tượng + thuật ngữ của 東京都下水道局 |
| kết luận | "đừng đổ 5 thứ này" | **"vì sao ta BẮT ĐẦU đổ"** — ống xưa không tắc vì **không có gì đi vào ống** |

⭐⭐ **ĐÒN LOGIC TRUNG TÂM (sóng 3) — nghịch lý có nguồn mà peer KHÔNG có.** Hai con số **60** ở hai lĩnh vực độc lập, và chúng chặn nhau:
- **でんぷんの老化（đóng cứng）gần như KHÔNG xảy ra trên 60℃**, càng nguội càng nhanh — 澱粉科学 19(2) 1972
- **ống 塩化ビニル thoát nước dùng tới 60℃**, quá thì mềm/biến dạng — クボタケミックス

⇒ Muốn tinh bột không đóng phải giữ **trên** 60. Ống chỉ chịu **tới** 60. **Không tồn tại nhiệt độ nào vừa an toàn cho ống vừa ngăn được tinh bột đóng.** ⇒ **Không chữa được bằng cách ĐỔ. Chỉ chữa được bằng cách KHÔNG ĐỔ.** → nối thẳng vào kết 昔の台所.

## ⛔ BA THỨ CẤM (tránh lặp kho video của chính kênh)
1. ⛔ Khối định lệ **重曹 + クエン酸/酢 → bọt → 30 phút** — **video 06 = 第二の知恵**, trùng gần trọn khối. Chỉ được **1 câu** nhắc chéo.
2. ⛔ **塩素系/薬剤クリーナー làm mục riêng** — video 06 dùng làm **HOOK**. Chỉ xuất hiện trong chương dòng tiền, ở tầng **cấu trúc ngành**.
3. ⛔ Mục **塗料・シンナー** của peer — lệch chủ đề bếp (là DIY), peer nhét cho đủ 5. Bỏ.

## 🌊 BỘ XƯƠNG v2 — 5 SÓNG

| | ĐẢO (niềm tin bị bẻ) | TRẢ | MỞ |
|---|---|---|---|
| **cold open** 0:45 | 「遅くなっただけ、まだ大丈夫」 | 50℃×30秒 ngay (giây 18) · khe **40→60 độ** | 「隙間が通用しないものが一つ」+ 何だと思われるでしょうか |
| **S1 油** | 「油を流すな」は**すでに流した人に無意味** | 脂は40–50℃で溶ける ⇒ **新しい層は戻せる** · 東京都下水道局 ふき取る · オイルボール · **母の油こし器** | 「隙間が通用しない相手がいる」 |
| **S2 でんぷん** | 「小麦粉は薄まる」→ 逆、濃くなる | 糊化60℃ / 老化 nhanh nhất **2–4℃** (澱粉科学 1972) ⇒ **khe ĐÓNG** · = 詰まりの接着剤 · ゴミ受け100円 | 「もっと熱くすれば?」 |
| **S3 熱湯** ⭐ | 「熱湯でまとめて流せる」 | đẩy dầu vào sâu rồi đông · ống 60℃ · 食洗機70℃→HT管90℃ · **chạm ống tự kiểm** | 「温度がまるで効かないものがある」 |
| **S4 かす** | 「細かい粒は流れる」 | **溶ける温度がない** — 50℃でも90℃でも砂粒 ⇒ ngoại lệ chứng minh quy luật · 濡れた砂 · 3枚の層 | 「三つを並べてみましょう」 |
| **S5 昔の台所** 🔥 | 「知恵を失った」→ **捨て場所を手に入れただけ** | 研ぎ汁=でんぷんが油を抱く(callback S2!) · 茶がら · dòng tiền · đóng LOOP LỚN | → kết |

- **CTA giữa video:** ranh giới **S3→S4**, ngay SAU câu MỞ → thoả **O14**
- **Chương dòng tiền:** trong S5 (~85%) → LOOP NGÀNH đóng muộn, giữ đuôi bài
- **Chất người 5/6:** ①自嘲×2 ②母+thoại+「コンロの右奥」(**phút ~5**) ③ゴボゴボ/研ぎ汁/濡れた砂 ④50℃を試した一週間 ⑤「母の缶は、もうありません」 ⑥câu cụt ×5

## 📚 原典 (đã fetch 2026-08-12 — mọi số trong bài phải truy về đây)
1. **東京都下水道局**「油・断・快適！下水道」 — 「台所から流れた油は下水道管内で冷えて固まり、下水道管のつまりや悪臭の原因になります」; mưa lớn → dầu đã đông bong ra → **オイルボール** → ra sông/biển. Ba việc: **ふき取る・吸い取る・使い切る**. https://www.gesui.metro.tokyo.lg.jp/living/sonota/oil
2. **横浜市 下水道FAQ**「なぜ油は下水道に流してはいけないのですか」 — 動植物油 vi sinh phân huỷ được nhưng 「分解速度は非常に遅く」; 「多量に流入すると冷えて固まって下水管が閉塞」. https://www.city.yokohama.lg.jp/kurashi/machizukuri-kankyo/kasen-gesuido/gesuido/gesuidofaq/suishitsu/014.html
3. **クボタケミックス** 硬質ポリ塩化ビニル管 使用温度範囲 — 排水用は **60℃以下**. https://www.kubota-chemix.co.jp/faq/common_field/design-6.html
4. **澱粉科学 第19巻第2号(1972)**「でんぷん糊の老化の温度依存性」檜作進ほか — 老化は **60℃以上ではほとんど起こらず**, nhiệt càng giảm càng nhanh. https://www.jstage.jst.go.jp/article/jag1972/19/2/19_2_70/_article/-char/ja/
5. **木下製粉**「でんぷんの老化現象」 — 糊化 ~60℃以上 → 網目構造; 老化 → 水が追い出される(**離水**), 硬くボソボソ. https://www.flour.co.jp/news/article/273/
6. **Panasonic / 積水化学** — 食洗機の排水は最高約70℃ → **耐熱塩化ビニル管(HT管, 約90℃)** を使う; VP管は約60℃以下. https://jpn.faq.panasonic.com/app/answers/detail/a_id/84435/
7. ⭐ **[v2] 肉の脂は40〜50℃で溶ける; 油汚れ対策のお湯は50〜60℃、熱湯は配管を傷める** — đây là nguồn mở ra khe 20 độ, tức đòn trung tâm của v2. https://allabout.co.jp/gm/gc/491471/ · https://www.lionchemical.jp/trivia/drain-grease-stain

⚠️ **Cấm chép số của peer.** Bài này **KHÔNG có con số chi phí sửa chữa nào** — không tra được nguồn công khai đủ tin, nên **bỏ hẳn**, để cơ chế tải bài (`CLAUDE.md` §YMYL).

---

## 【Khối 1】KỊCH BẢN (bản đọc — render bằng `19_haisuiko-naze-tsumaru_TTS.md`)

台所の流しが、少し遅くなった気がする。

あの遅さは、ひとりでに直ることはありません。今日より明日、必ず少しだけ遅くなります。

けれど今夜、洗い物のあとに30秒だけ手を動かせば、まだ間に合う部分があります。

洗い物が終わったすぐあとに、50度のお湯を、30秒だけ流してみてください。

熱湯では駄目です。60度を超えると、こんどは配管そのものが傷みます。

40度と、60度。この20度のあいだにだけ、あなたの台所の勝ち目があります。

そして、その隙間がまったく通用しないものが、台所に一つだけあります。毎朝、あなたが捨てているものかもしれません。何だと思われるでしょうか。

それは、いちばん最後にお話しします。

古代の秘訣へようこそ。今日もまた、時代に置き去りにされた知恵を一つ、掘り起こしていきます。

この番組では、こうした暮らしの知恵をお届けしています。よろしければ、チャンネル登録をしておいてください。お住まいの家では、流れが遅くなったと感じたことがありますか。よければ、あとでコメントで教えてください。

さて、ここからが今日の核心です。

油を流してはいけない。これは、たいていの方がご存じです。

ところが、この言葉には抜けているところがあります。すでに流してしまった人に、何の役にも立たないのです。

昨日の油。先月の油。三年前の油。それは、もう管の中にあります。

まず、そこから始めましょう。

流しから出ていく洗い物の水は、だいたい40度前後。手を入れて、少し温かいと感じるくらいですね。

ところが、その水が入っていく管は、床の下や壁の中を通っています。冬なら、20度を下回っていることもあります。

つまり油は、流された瞬間から冷やされ始めています。

東京都下水道局は、この現象をはっきり言葉にしています。台所から流れた油は下水道管の中で冷えて固まり、管の詰まりや悪臭の原因になる、と。

固まった油は、薄い膜になって管の内側に張り付きます。その膜の上に、次の日また新しい膜が重なる。

古い配管を切って中を見ると、ろうそくを塗り重ねたような、白っぽい層が出てきます。指でなぞれば、かたい手ざわりが残ります。

ここが、今日いちばん役に立つところです。

肉の脂は、40度から50度で溶けます。つまり、いちばん外側の、まだ新しい層なら、溶かせるのです。

だから、50度のお湯を30秒。洗い物のすぐあと、管がまだ温まっているうちに流します。

逆に言えば、溶かせるのは新しい層だけです。何年もかけて厚くなった芯は、もう動きません。

あなたが今夜取り戻せるのは、いちばん最近の分です。そして一晩ごとに、その分が一枚、硬いほうへ移っていきます。

もう一つ、面倒に見えて、いちばん効くことがあります。

フライパンにうっすら残った油を、洗う前に古新聞で拭き取る。東京都下水道局が都民に呼びかけている言葉は、三つだけです。ふき取る、吸い取る、使い切る。

白状しますと、私は長いあいだ、これをしていませんでした。面倒だと思っていたからです。

試しに、一週間だけ、拭いてから洗うことにしてみました。

変わったのは、流れの速さではありません。スポンジの持ちが良くなりました。油を先に取ってしまえば、洗剤もスポンジも、そんなに要らないのです。

私の母は、もっと徹底していました。揚げ物に使った油は、熱いうちにこし器で漉して、缶に取っておく。台所の、コンロの右奥。いつも同じ場所に、その缶がありました。

一度、それは古いから捨てたらどうかと言ったことがあります。母は、手を止めずに、こう答えました。

まだ、匂いが立っていないでしょう。

さて、ここまでは良い話です。40度から60度の隙間があって、油は溶ける。

ところが、この隙間がまるで通用しない相手がいます。しかも、油よりずっと厄介です。

小麦粉です。

天ぷらの下ごしらえをしたあとのボウル。お菓子の生地をこねたあとの手。まな板についた白い粉。

水に浸ける前に、ボウルの底を指でこすってみたことはありませんか。さらりとしていた粉が、もう別のものに変わっています。

小麦粉は、水で薄まりません。逆です。水を吸って、濃くなります。

でんぷんは、水と一緒に60度以上に温められると、粒がふくらみ、中の分子が外に飛び出して、網目のような構造を作ります。これを糊化と呼びます。とろみのついた、糊の状態ですね。

問題は、そのあとです。温度が下がると、飛び出していた分子がまた集まり、並び直そうとします。そのとき、網目の中に抱えていた水が、外へ押し出されます。

残るのは、硬く、ぼそぼそした塊。この現象には、老化という名前がついています。

冷やご飯が硬くなるのも、パンが翌日ぱさつくのも、同じ理屈です。

そして、この老化がもっとも早く進むのは、2度から4度のあたりだと報告されています。1972年の澱粉科学の研究です。ちょうど、冷蔵庫の中の温度ですね。

ここで、さきほどの隙間を思い出してください。

でんぷんを固めずに運びきるには、60度より上を保たなければなりません。

けれど、配管が耐えられるのは、60度まで。

隙間は、閉じています。

油には勝ち目がありました。でんぷんには、ありません。家庭の流しには、でんぷんを固めずに運びきる温度など、はじめから存在しないのです。

だから、でんぷんだけは、入れる前に止めるしかありません。ここには、あとでどうにかする、が使えません。

しかも、でんぷんの本当の役目は、詰まりの材料ではありません。

糊は、あとから流れてくる油の粒や、細かな食べ物のかすを、次々と貼り付けていきます。つまり、詰まりの接着剤です。

ご飯粒も、うどんの切れ端も同じ道をたどります。管の中で水を吸い、やわらかくなり、互いに貼り付いて、栓のようになります。

ですから、対策も一つで足ります。粉と、麺と、ご飯粒は、水をかける前に取り除く。

流しの排水口に、ゴミ受けを置いてください。100円ほどのもので構いません。

ただし、ゴミ受けは、置いただけでは働きません。溜まったものを、その日のうちに捨てる。それが、道具を道具にしています。

ここまで聞いて、こう思われた方がいるかもしれません。

60度で駄目なら、もっと熱くすればいい。熱湯なら、でんぷんも油もまとめて流れるはずだ、と。

私も、まったく同じことを考えていました。最後に熱湯をたっぷり流しておけば、中まできれいになるだろう、と。

これが、いちばんやってはいけないことでした。

理由は二つあります。一つは、油の側。もう一つは、管の側です。

まず、油の側。

熱湯を追いかけさせると、固まりかけていた油は、もう一度やわらかくなります。そして、水の勢いに押されて、管の奥へ運ばれていきます。

けれど、お湯が熱いのは、最初の1メートルか2メートルだけです。管を進むあいだに、お湯はどんどん冷えていきます。

つまり、やっているのは、油を取り除くことではありません。油を、手の届かない奥まで運んで、そこで固めることです。

流れが良くなったように感じるのは、本当です。詰まりの場所が、遠くなっただけですから。

そして、管の側。

日本の住宅で、台所の排水に使われている管の多くは、硬質の塩化ビニルという樹脂でできています。

一度、流しの下の扉を開けて、管を見てみてください。灰色か白の、少しくすんだ樹脂の管であれば、それがこの塩化ビニルです。

配管メーカーの資料では、この排水用の管の使用温度は、60度以下とされています。これを超え続けると、樹脂はやわらかくなり、わずかに形が変わって、継ぎ目の力が落ちます。水漏れは、その日ではなく、何年か経ってから出てきます。

食器洗い機のことを考えると、この数字の重さが分かります。

食器洗い機の排水は、最高で70度ほどになります。だからメーカーは、そこには普通の管ではなく、耐熱用の管を使うように指定しています。耐熱用の管は、90度ほどまで持ちます。

70度の水を流すためだけに、わざわざ別の管を用意する。それが、住宅の設計上の答えです。

試しに、お湯を流したあとで、流しの下をのぞいて、管に手を当ててみてください。ぬるいどころか、冷たいままのことがあります。熱は、あなたが思っているほど奥まで届いていません。

ところで、油にもでんぷんにも共通していたのは、温度で姿を変えるということでした。

冷やせば固まり、温めればゆるむ。だから、温度の話ができました。

ところが、台所には、温度がまるで効かないものがあります。話の初めに、一つだけあると申し上げたものです。

ここまで聞いてくださって、ありがとうございます。今日のお話が良さそうだと思ってくださったら、高評価と、この動画を離れて暮らすご家族やお友達にも、そっと分けてあげてください。そして、気づいたことやご感想があれば、どうぞコメントで教えてくださいね。皆さんの声を励みに、もっと良いお話をお届けしていきます。

それでは、続きを見ていきましょう。

コーヒーの、かすです。

朝、ドリッパーからフィルターを外す。あるいは、ポットの底に残った粉を、流しにあける。

粒がとても細かいので、水と一緒に流れていったように見えます。

けれど、コーヒーのかすは、水に溶けていません。溶けたのは、味と香りだけです。粒は、粒のまま残っています。

そして、ここが今日の話の中で、いちばん厄介な性質です。

かすには、溶ける温度がありません。冷やしても固まらず、温めてもゆるみません。50度でも、90度でも、まったく同じ砂粒のままです。

つまり、40度から60度の隙間は、この相手には初めから存在しないのです。

管の中で、粒が沈んで溜まりやすい場所は決まっています。管が曲がったところ。わずかに下がっているところ。別の管とつながる継ぎ目です。

そこに、毎朝、少しずつ積もっていきます。

濡れた砂を、手で握ったときのことを思い出してみてください。乾いた砂は指のあいだから落ちますが、濡れた砂は固まって、形が残ります。

管の底で起きているのは、それとよく似たことです。水を含んだ粒が、上から来る水の重さで押し固められていく。

そして、ここで三つがつながります。

管の内側に、油の膜がある。そこへ、でんぷんの糊が来る。糊の上に、コーヒーのかすが乗る。ざらざらした層が、順に3枚です。

油が接着面になり、でんぷんが糊になり、かすが中身を埋める。三つは別々の相手ではなく、一つの塊の、三つの材料だったのです。

対策も、もう決まっています。かすは、シンクへ落とさないでください。

フィルターごと取り出せるなら、そのまま水気を切って捨てる。ポットの底に残ったものは、スプーンで先にすくう。

不思議なことに、コーヒーのかすには、管の中よりずっと良い行き先があります。土です。

乾かしたかすは、庭やプランターの土に混ぜられます。においを吸う性質もあるので、生ゴミの受け皿に薄く敷いておく使い方もあります。

ただし、土に回すなら、必ず乾かしてからにしてください。濡れたままだとカビが出やすいので、新聞紙に薄く広げて、半日ほど置きます。

コーヒーのかすが役に立つのは、管の中ではありません。土の中です。

さて、ここで、三つを並べてみましょう。

油は、温度で戻せる。でんぷんは、戻せない。かすは、そもそも温度が関係ない。

性質は三つとも違います。ところが、対策は三つとも同じ場所を指しています。入り口です。

そして、この形には、先例があります。

昔の日本の台所には、排水口が詰まるという悩みが、ほとんどありませんでした。

理由は、良い道具を持っていたからではありません。良い洗剤があったからでもありません。

流すものが、なかったからです。

油は、さきほどの母のように、漉して取っておく。それでも残れば、炒め物に回す。

米を洗ったあとの研ぎ汁も、捨てませんでした。桶に取って、庭の木の根元にやる。あるいは、油の付いた皿を、それで先にすすぐ。

研ぎ汁には、細かなでんぷんと、米のぬかの成分が溶けています。今日のお話を思い出してください。でんぷんは、油を抱き込みます。

管を詰まらせる性質と、皿の油を落とす性質は、じつは同じ性質です。台所の外で使えば道具になり、管の中に入れれば詰まりになる。

お茶の出しがらも、そうでした。乾かして、玄関のたたきに撒いてから掃く。埃が舞い上がりません。あるいは、そのまま土に返す。

つまり、昔の台所では、油もでんぷんも茶がらも、まだ使えるものでした。

流しは、捨てる場所ではなかったのです。

そして、ここが、この話のいちばん静かなところです。

私たちは、知恵を失ったわけではありません。捨てる場所を、一つ手に入れただけです。

蛇口をひねれば、いくらでも水が出る。その水は、見えないところへ流れていく。それを手に入れた日から、台所には、あとで考えるという選択肢ができました。

管の中で起きていることは、その選択の、請求書のようなものです。

もう一つ、お伝えしたいことがあります。

なぜ、この地味な話が、あまり大きな声で語られないのでしょうか。

流しの詰まりを解決すると言われている商品は、たくさんあります。棚には、月に一度使うもの、週に一度使うものが並んでいます。

それらが悪いという話ではありません。以前この番組で、重曹と酢の使い方をお話ししたこともあります。

ただ、商いの形を考えてみてください。

繰り返し使うものは、繰り返し売れます。月に一度使う習慣が身につけば、それは毎月の収入になります。

一方、入れないという方法は、一度覚えたら終わりです。100円のゴミ受けと、古新聞が一枚あれば足ります。買い替えも、定期購入もありません。

つまり、誰も熱心に広めない理由は、効かないからではなく、売るものが無いからです。

これは、特定の会社の話ではありません。繰り返し買ってもらう形の商いは、どの業界にもあります。責める話ではなく、仕組みの話です。

ただ、仕組みを知っておくと、棚の前で迷う時間が短くなります。

さて、冒頭でお約束した、隙間が通用しない一つ。それが、コーヒーのかすでした。温度に手がかりがない相手は、入り口で止めるほかありません。

そのうえで、今夜からの順番をお伝えします。

一つ。洗い物の前に、油を古新聞で拭く。

二つ。粉と麺とご飯粒、そしてコーヒーのかすは、ゴミ受けへ。

三つ。洗い物のすぐあとに、50度のお湯を30秒。熱湯は使わない。

道具は、100円のゴミ受けと古新聞だけです。特別なものは、何も要りません。

正直に申し上げると、この方法は万能ではありません。

溶かせるのは新しい層まで。何年もかけて固まった芯には届きません。今すでに水がほとんど流れない、においが上がる、水が戻ってくる。そういう状態であれば、ご自分で薬剤や熱湯を試す前に、専門の業者にご相談ください。無理に押し込むほど、状態は悪くなります。

60度という数字も目安です。管の材質や築年数によって事情は変わります。

そして、もう一つ。

今日の話は、排水口の話のようでいて、じつは温度の話でした。

液体は冷えると固まる。糊は冷えると硬くなる。そして、砂は何度でも砂のまま。この三つを知っているだけで、台所の中の判断は、ずいぶん変わります。

昔の人は、糊化という言葉も、老化という言葉も知りませんでした。それでも、油を漉し、研ぎ汁を庭にやり、茶がらを土に返していました。

言葉を知らないまま、正しく扱っていたのです。私たちは言葉を手に入れて、扱いを忘れました。

母の缶は、もうありません。ただ、あの、まだ匂いが立っていないでしょう、という一言は、いまでも台所に立つと聞こえてきます。

もし、今夜の三つのうち、一つだけ試すとしたら、どれを選ばれますか。よければ、コメントで教えてください。

次にお話しする知恵は、今日よりもう少し、家の外側に関わる話になります。目に見えないところで、じわじわと家の寿命を削っているものについて、掘り起こしていきます。

古代の秘訣は、これからも暮らしの中に眠る宝を静かに掘り起こしていきます。それでは、次の知恵でまたお会いしましょう。

---

## 【Khối 2】5 TIÊU ĐỀ VIRAL

> Khuôn dẫn theo `CLAUDE.md` §📐 **7c**: vế dẫn = **câu hỏi `なぜ`** hoặc **lệnh cấm cụ thể**. `数百円` hạ xuống vế phụ sau `――`. Keyword dẫn = `キッチンの排水口` (thừa hưởng cầu `排水口 掃除` 37). 🔴 **Không dùng chữ 掃除.**

1. `なぜキッチンの排水口は詰まるのか――敵は汚れではなく「60度」でした` (44)
2. `キッチンの排水口に熱いお湯を流してはいけない――60度で決まる、詰まりの正体` (46)
3. `なぜ昔の台所は詰まらなかったのでしょうか――キッチンの排水口と、失われた三つの習慣` (48)
4. `キッチンの排水口を守るのは100円のゴミ受けと古新聞――なぜ誰も熱心に広めないのか` (48)
5. `小麦粉は詰まりではなく「接着剤」でした――なぜキッチンの排水口は静かに細くなるのか` (48)

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `なぜキッチンの排水口は詰まるのか――敵は汚れではなく「60度」でした` | 44 | キッチンの排水口@2 | khuôn `なぜ` + con số lạ 60度 làm curiosity gap |
| **A2** | `キッチンの排水口に熱いお湯を流してはいけない――60度で決まる、詰まりの正体` | 46 | キッチンの排水口@0 | đổi sang **lệnh cấm cụ thể** (khuôn hit 357K của peer), keyword lên vị trí 0 |
| **A3** | `なぜ昔の台所は詰まらなかったのでしょうか――キッチンの排水口と、失われた三つの習慣` | 48 | キッチンの排水口@18 | đổi kiểu hook: **bí ẩn lịch sử** (khuôn `なぜ〜のでしょうか？` = 5.560 v/ngày của peer) |

> **Title CHỐT**
> ```
> なぜキッチンの排水口は詰まるのか――敵は汚れではなく「60度」でした
> ```
> **Tên file upload**
> ```
> kitchen-haisuiko-naze-tsumaru-60do.mp4
> ```

**Quét compliance** (`youtube-compliance.md` mục 3): không từ nhóm 殺/血/死/自殺/虐待. Không tên công ty/thương hiệu (chương dòng tiền chỉ nói 「業界」「棚に並ぶ商品」). Mọi tình tiết trên title đều có trong video (60度 ở sóng 3 · 汚れではない ở sóng 1 · 三つの習慣 ở sóng 5). ✅

---

## 【Khối 3】TEXT THUMBNAIL 3 TẦNG

- **Tầng 1** (dòng dẫn): `排水口が詰まる理由`
- **Tầng 2** (CHỮ TO NHẤT): `60度`
- **Tầng 3** (hệ quả): `熱いお湯は逆効果`

🔴 **Điều kiện sống (`00_TOPIC_LOG.md` §spec 19):** cụm 排水口 đã chết 2 lần ở đúng CTR — video **06 = 1,0%**, video **17 = 0%**. Bộ thumbnail này **phải khác hẳn** 2 bản đó: 06/17 đều là ảnh **cận cảnh miệng cống**. Bản này lấy **nhiệt kế + ống cắt đôi**, tức đổi hẳn chủ thể. Đặt cạnh `06_VIDEO/_thumb_v4/` để so trước khi giao.

---

## 【Khối 4】PROMPT ẢNH THUMBNAIL

> ⛔ **BỘ PROMPT DƯỚI ĐÂY ĐÃ BỎ (2026-08-14).** Hai lỗi: ① kiểu `No text` rồi đốt chữ bằng tool — trái luật **prompt phải BAKE CHỮ** (`ab-3title-3thumb.md` §3 mục 8, chốt 2026-08-10) ② **T3 mô tả mặt người**, trái luật **cấm mặt người trên thumbnail co-dai** (`02_THUMBNAIL_PROMPTS.md`, chốt 2026-08-05).
> ✅ **Bản đang dùng — 4 file** trong `06_VIDEO/19_haisuiko-naze-tsumaru/`:
> `thumb_prompts_FLOW.txt` (bake chữ, mỗi prompt 1 dòng — bơm thẳng vào extension) · `thumb_prompts_BLOCKS.md` (bản người đọc + lý do khuôn + quy trình sau khi gen) · `thumb_prompts_TENFILE.txt` · `thumb_prompts_PLATE.txt` (3 plate KHÔNG chữ — đường lui, ⛔ đừng dán chung FLOW).
> Khuôn: **B1 (bright) lồng K3 (macro hero)** · chữ `排水口が詰まる理由` / **`60度`** / `熱いお湯は逆効果` + badge `道具は100円` · giữ bản cũ dưới đây làm lưu trữ.

### 🖼️ TRẠNG THÁI THUMBNAIL (cập nhật 2026-08-14) — **T1 xong, T2/T3 CÒN THIẾU**

User đã gen **1/3 bản** và thả vào `_upload/thumbnail.png` (2752×1536). Đã xử lý và đưa về đúng chỗ:

| việc | kết quả |
|---|---|
| Nguồn gốc (giữ nguyên, không ghi đè) | `_thumb_src/thumb_T1_haisuiko-60do.png` |
| Bản sạch đang dùng | `thumb_T1_haisuiko-60do.png` + `.jpg` (vdir) → pack thành `_upload/thumbnail.jpg` **646 KB** (PNG 2.405 KB **vượt trần 2 MB** của YouTube nên tool tự lấy bản jpg) |
| Chữ | ✅ soi 1:1 đủ 4 khối, **đúng nét từng ký tự**: `排水口が詰まる理由` · `60度` · `熱いお湯は逆効果` · `道具は100円` |
| Gate 168px / 120px | ✅ **PASS cả hai** — ở 120px `60度` là thứ đọc được đầu tiên |
| Hero `60度` | **cao 33,8% khung · rộng 49,8% bề ngang** |

⭐ **Đáng ghi vào `audience-45plus.md` §6.10:** hero **33,8% ≥ 33,3%** ⇒ đây là ca **ĐẦU TIÊN của workspace ĐẠT gate 2**, sau **12/12 ca liên tiếp rớt** (dải 20–31%). Cơ chế: bản gen vốn ~31%, phần vượt lên là do **cắt 127px mép TRÊN** khi trim về 16:9 (xem dưới) — tức tỉ lệ hero **mua được bằng cách cắt khoảng thừa phía trên**, không phải bằng phóng chữ. Đây là dữ liệu mới cho quyết định ⓐ/ⓑ đang treo, **chưa tự đổi gate**.

🔴 **XOÁ WATERMARK — đã làm, nhưng KHÔNG theo tool mặc định.** (`media-library.md` §2.10⑤b — luật *"lúc nào cũng xoá"*)
- `strip_wm_thumb.py` (đường VÁ cho thumbnail bake chữ) **chạy nhưng gần như không ăn**: chỉ vá **380 px** trong khi ✦ đo được **3.207 px**, ảnh ra chỉ bị **sứt một góc nhọn** của ngôi sao. Hai lý do: ① hằng số lô `(0.930, 0.890)` lệch **25px** so với vị trí thật ở ảnh này ② `is_glyph()` coi ✦ trắng là nét chữ nên **loại nó khỏi mặt nạ**. ⚠️ Tool còn **tự resize xuống 1920×1080** — suýt làm tao đọc nhầm ảnh "đen sì" khi so crop theo toạ độ 2752.
- ✅ **Đường chạy được ở ca này là CẮT**, dù luật nói thumbnail thường không cắt được. Lý do cắt được: chữ chỉ chạy tới **0,849W** (đo bằng máy), không tới ~0,97W như ca shokutaku. Cắt `x < 2505` (0,910W) **xoá sạch CẢ HAI** vị trí stamp đã ghi sổ của lô 2752×1536 — `(0.958W, 0.926H)` và `(0.930W, 0.890H)` — rồi trim **127px mép trên** để về đúng 16:9 (2505×1409 → 1920×1080). Mép dưới **không đụng được**: chữ chạm y=1484, chỉ còn 52px lề.
- ⚠️ **Phân biệt được ✦ stamp với ✦ trang trí:** ảnh này có **~8 ngôi sao 4 cánh giống hệt** rải khắp khung (trên nền mờ, trên mặt người, trên ống). Cái ở góc dưới–phải đo được **(0,929W · 0,874H)** — **trùng vị trí stamp đã ghi sổ ở CẢ hai lô** (1376 lô = 0,928/0,878) ⇒ **đó là watermark**, số còn lại là **model tự thêm** (prompt không hề xin sparkle). Số sao còn lại **giữ nguyên** vì chúng nằm trong bố cục, gỡ sẽ để vệt trên vùng có vân.

🔴 **HAI ĐIỀU USER PHẢI QUYẾT — tao KHÔNG tự xử lý:**
1. **Ảnh có MẶT NGƯỜI (ông cụ, góc trên–phải) ⇒ trái luật kênh** *"thumbnail co-dai không dùng mặt người"* (`02_THUMBNAIL_PROMPTS.md`, chốt 2026-08-05) — và đây chính là **đúng lỗi đã khiến bộ prompt cũ bị bỏ** ở đầu Khối 4 này. **Prompt `FLOW.txt` KHÔNG hề mô tả người** ⇒ model tự thêm.
   ⚖️ **Nhưng có đường hợp lệ để GIỮ:** `02_THUMBNAIL_PROMPTS.md` dòng 101 ghi *"nếu CTR đo được thấp thì BIẾN ĐẦU TIÊN nên đảo lại là đưa mặt người vào"* — mà cụm 排水口 đã **chết 2 lần đúng ở CTR** (video 06 = 1,0% · video 17 = **0%**). Tức bản có mặt này **có thể là phép thử đúng lúc**, nhưng phải là **quyết định có chủ ý + ghi ngày đảo vào `08_ANALYTICS_LOG.md`**, không phải tai nạn của model.
2. **Bộ A/B mới có 1/3** ⇒ gate `🔴 GATE 3×3` vẫn kêu. Cần gen **T2** (đổi đúng 1 biến hình: thêm nước sôi bốc hơi mà mỡ không tan) và **T3** (đổi layout: panel chữ nửa trái / ảnh nửa phải) — **chữ giữ Y NGUYÊN cả 3 bản** (`ab-3title-3thumb.md` §3 mục 6). Prompt sẵn ở `thumb_prompts_FLOW.txt` dòng 2–3, tên file đích ở `thumb_prompts_TENFILE.txt`.
   🔴 Gen xong **phải xoá watermark rồi mới dùng** — và **đo lại vị trí ✦ theo đúng lô**, đừng bê toạ độ của bản T1 này sang (lô khác ⇒ toạ độ khác, `media-library.md` §2.10⑤).

**T1 — baseline khuôn kênh (nền sáng + 1 vật + số)**
```
Photorealistic 16:9 kitchen close-up, bright clean daylight. A cutaway cross-section of a white PVC drain pipe lying on a pale wooden counter, its inner wall coated with a thick waxy yellow-white grease layer that visibly narrows the opening. A simple analog kitchen thermometer leans against the pipe, its red needle clearly pointing at the 60 mark. Shallow depth of field, high saturation, crisp macro detail on the grease texture. Leave generous empty space in the upper-left third and the lower band for text overlay. Keep the very bottom-right corner free. No text, no letters, no numbers other than the thermometer scale. No watermark, no logo. --ar 16:9
```

**T2 — đổi ĐÚNG 1 biến hình (giữ nguyên chữ): thêm dòng nước nóng bốc hơi**
```
Photorealistic 16:9 kitchen close-up, bright clean daylight. Same cutaway white PVC drain pipe on a pale wooden counter with a thick waxy yellow-white grease layer inside. A stream of steaming hot water pours into the pipe mouth from the top of the frame, visible steam curling upward, while the grease deeper inside stays solid and unmoved. Analog thermometer beside it, red needle at the 60 mark. High saturation, crisp macro detail. Leave empty space in the upper-left third and the lower band for text. Keep the very bottom-right corner free. No text, no letters. No watermark. --ar 16:9
```

**T3 — đổi LAYOUT: mặt biểu cảm + vật nhỏ hơn**
```
Photorealistic 16:9. Right half: a Japanese woman in her sixties at a bright kitchen sink, apron on, looking down into the drain with a worried, slightly startled expression, one hand still holding a frying pan. Left half: clean bright empty wall space for large text. Foreground lower-left: a cutaway PVC pipe section showing a thick waxy grease ring, and an analog thermometer with the needle at 60. Warm daylight, soft shadows, high clarity on faces and textures. Keep the very bottom-right corner free. No text, no letters. No watermark. --ar 16:9
```

**Fallback no-text plate** (nếu bản gen nát chữ → render bằng tool):
```
Photorealistic 16:9 bright kitchen counter, cutaway white PVC drain pipe with thick waxy grease layer inside, analog thermometer beside it. Composition deliberately empty across the top third and bottom band. Absolutely no text, no letters, no numerals anywhere. No watermark. --ar 16:9
```

⚠️ Theo `ab-3title-3thumb.md` §3 mục 8, prompt lẽ ra phải **bake chữ**. Ba prompt trên **cố ý để KHÔNG chữ** vì bộ chữ tầng 2 chỉ có `60度` (2 ký + số) — dạng **chữ số Latin**, an toàn nhất khi gen, nhưng `熱いお湯は逆効果` là 7 ký kanji rậm ⇒ rủi ro nát nét cao. **Quyết định: gen nền không chữ rồi đốt chữ bằng `make_thumb_3dan.py`** — và ghi rõ ở đây là ngoại lệ có lý do, không phải bỏ sót.

---

## 【Khối 4b】GÓI UPLOAD — tên file · mô tả · từ khoá (soạn 2026-08-14)

> 🔴 **ĐỪNG viết chữ `タグ` (hay `概要欄`, `3 dòng đầu`, `mô tả đầy đủ`) vào TIÊU ĐỀ của heading tổng này.**
> Bản đầu đặt tên `GÓI UPLOAD — tên file · 概要欄 · タグ` ⇒ `find_block(text,"タグ")` khớp **ngay heading tổng** (nó là heading thật, có chứa `タグ`), không tìm thấy code fence nào trước heading con kế tiếp, rồi `plain_fallback` **trả về đoạn blockquote ghi chú bên dưới** ⇒ ô `[4] TAGS` của `METADATA.txt` in ra nguyên văn *"Nguồn số keyword: bảng đo Trends…"* thay vì danh sách tag. Cùng họ bug hoa/thường đã vá ở `youtube-upload-seo.md` §4 — **heading là giao diện máy đọc, không phải chữ trang trí.**
> Kiểm nhanh sau mỗi lần đóng gói: mở `METADATA.txt`, ô `[4]` phải là **danh sách phẩy**, không có dấu `>` hay chữ tiếng Việt.

### Title CHỐT

```
なぜキッチンの排水口は詰まるのか――敵は汚れではなく「60度」でした
```

> ⓘ Heading này thêm 2026-08-14 để `find_block("Title CHỐT")` đọc **trực tiếp**. Trước đó title chỉ nằm trong **blockquote** ở Khối 2 (`> **Title CHỐT**`) — mà parser chỉ nhận heading thật ⇒ nó rơi xuống *đường vòng*: quét list số dưới heading `5 TIÊU ĐỀ VIRAL` rồi lấy mục 1. Ra đúng A1 **do may** (A1 tình cờ là mục 1), không do thiết kế — đảo thứ tự 5 title là đăng sai tiêu đề mà không có cảnh báo nào.

> **Nguồn số keyword:** bảng đo Trends YouTube JP (`gprop=youtube`, 30 ngày) **đo 2026-08-12**, ghi ở `01_SOURCES/00_TOPIC_LOG.md` §spec 19 — **KHÔNG đo lại** ở lượt đóng gói này (cùng cụm, cách 2 ngày, title đã chốt từ chính phép đo đó).
> Thứ tự tag/hashtag theo volume: `排水口 掃除` **37** > `台所 排水口 つまり` **33** > `キッチン 排水口 つまり` **29** > `キッチン 排水口 掃除` **13** > `排水口 つまり` **6** > `コーヒーかす` **4**.
> 🔴 **LOẠI `流してはいけない` (2 điểm) khỏi tag/hashtag** — related #1 của nó là `学校で流してはいけない曲` (100 điểm, nhạc học đường) ⇒ **sai intent hoàn toàn**, nhét vào là mời YouTube xếp nhầm cụm (`youtube-upload-seo.md` §0.5 mục 4). `排水口 油` = 0 điểm cũng bỏ khỏi tag dẫn, chỉ giữ dạng long-tail.

### Tên file upload
```
kitchen-haisuiko-naze-tsumaru-60do.mp4
```

### 概要欄 — 3 dòng đầu
```
キッチンの排水口が詰まる本当の理由は、汚れではなく「温度」でした。
油・でんぷん・コーヒーのかす――この三つが管の中で何をしているのかを、原典をたどって一つずつ確かめます。
今夜、洗い物のあとに30秒でできることまで、順番でお伝えします。
```

### 概要欄 — mô tả đầy đủ
```
キッチンの排水口が詰まる本当の理由は、汚れではなく「温度」でした。
油・でんぷん・コーヒーのかす――この三つが管の中で何をしているのかを、原典をたどって一つずつ確かめます。
今夜、洗い物のあとに30秒でできることまで、順番でお伝えします。

【目次】
00:00 今夜30秒でできること――50度と「20度の隙間」
01:22 「油を流すな」が、すでに流した人に届かない理由
02:53 脂は40〜50度で溶ける――戻せるのは、いちばん新しい層だけ
03:47 東京都下水道局の三つの言葉／オイルボール
04:16 母の油こし器と、コンロの右奥にあった缶
05:01 小麦粉は水で薄まらない――糊化60度と「老化」
07:45 100円のゴミ受けが、道具になる条件
08:03 熱湯なら、まとめて流せるのでしょうか
09:42 塩化ビニル管は60度まで／食器洗い機が70度である意味
11:44 コーヒーのかす――溶ける温度がない相手
13:14 油・でんぷん・かす、重なった三枚の層
14:36 三つを並べる――対策はすべて「入り口」を指す
15:02 昔の台所に詰まりがなかった理由（研ぎ汁・茶がら）
17:00 なぜ、この地味な話は大きな声で語られないのか
18:37 今夜からの順番（三つ）と、この方法にできないこと
20:29 母の缶は、もうありません

台所の流れが少し遅くなった、というとき、たいていは「汚れ」の話になります。けれど管の中で起きているのは、もっと単純なことでした。肉の脂が溶けるのは40度から50度。いっぽう、排水用の塩化ビニル管が使えるのは60度まで。この20度のあいだにだけ、まだ手が届く部分が残っています。

ところが、でんぷんは事情が違います。糊化するのは60度以上、そして冷えるほど速く硬くなる。つまり「管が耐えられる温度」と「でんぷんが固まらない温度」は重なりません。だから、でんぷんは流したあとで溶かすのではなく、入り口で止めるしかない。コーヒーのかすにいたっては、溶ける温度そのものがありません。

三つは性質がまるで違うのに、対策は同じ一点を指しています。そしてその形は、昔の日本の台所にすでにありました。油はこし器で漉して取っておき、米の研ぎ汁は流さず、茶がらは土に返す。詰まらなかったのは、良い道具があったからではなく、流すものが無かったからです。

【原典】
・東京都下水道局「油・断・快適！下水道」（ふき取る・吸い取る・使い切る／オイルボール）
・横浜市 下水道FAQ「なぜ油は下水道に流してはいけないのですか」
・クボタケミックス 硬質ポリ塩化ビニル管 使用温度範囲（排水用は60℃以下）
・澱粉科学 第19巻第2号(1972)「でんぷん糊の老化の温度依存性」檜作進ほか
・木下製粉「でんぷんの老化現象」（糊化・離水）
・Panasonic／積水化学（食器洗い機の排水は最高約70℃、耐熱管の指定）

※60度という数字は目安です。配管の材質や築年数によって事情は変わります。すでに水がほとんど流れない、においが上がる、水が戻ってくるという場合は、ご自分で薬剤や熱湯を試す前に、専門の業者にご相談ください。無理に押し込むほど状態は悪くなります。

音楽: "Heartwarming" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

#生活の知恵 #昔の知恵 #古代の秘訣 #排水口掃除 #キッチンの排水口
```

### タグ
```
古代の秘訣, 生活の知恵, 昔の知恵, 暮らしの知恵, 昔の人の知恵, 生活の裏ワザ, 日本の知恵, 家の知恵, 昔ながらの知恵, 節約術, DIY, 知らないと損, 排水口 掃除, 台所 排水口 つまり, キッチン 排水口 つまり, キッチン 排水口 掃除, 排水口 つまり, 排水口, キッチンの排水口, 台所 つまり, 排水管 つまり 予防, 油汚れ, 台所 油, 油こし器, でんぷん 老化, 小麦粉 排水, コーヒーかす, ゴミ受け, 熱湯 配管, 塩化ビニル管, 食洗機 排水, オイルボール, 東京都下水道局, 研ぎ汁, 茶がら, 昔の台所
```

**Quét compliance** (`youtube-compliance.md`): không từ nhóm 殺/血/死/自殺/虐待 ở title/thumbnail/3 dòng đầu ✅ · không tên công ty bị cáo buộc — 原典 nêu tên hãng chỉ để **dẫn nguồn kỹ thuật**, chương dòng tiền vẫn nói ở tầng 「業界」「棚に並ぶ商品」 ✅ · credit BGM CC BY đầy đủ ✅ · **KHÔNG ghi credit VOICEVOX trong 概要欄** (ngoại lệ kênh, `CLAUDE.md` §Tuân thủ, chốt 2026-07-22) · disclaimer an toàn có ✅.
🔴 **Video có ảnh AI realistic ⇒ lúc upload PHẢI TICK "altered/synthetic content"** (`youtube-compliance.md` §2.1, luật đảo chiều 2026-08-09). Tool chưa tự tick — làm tay trong Studio.

---

## 【Khối 5】📌 Pinned comment

```
最後までご覧いただき、ありがとうございました。🌿
今日ご紹介した四つの中で、まず試してみたいと思われたのは、どれでしたか。
そして、もしご家庭に「昔はこうしていた」という台所の習慣が残っていましたら、ぜひ聞かせてください。油こし器のこと、研ぎ汁の使い道、地域ごとの違い。皆さまの声を参考に、これからの内容も深めてまいります。
なお、すでに水の流れが悪い、においが上がるという場合は、熱いお湯や薬剤をご自分で試す前に、専門の業者にご相談ください。配管の材質や築年数によって事情が変わります。
```

---

## 🎬 SLIDES + ẢNH (soạn 2026-08-12)

**`19_haisuiko-naze-tsumaru_SLIDES.json`** — **89 entry** = 63 ảnh thường + **26 thẻ vox**
· **4,6 đổi hình/phút** (trần 6, `audience-45plus.md` §2) · mọi `match` **duy nhất & có thật** trong `_TTS.md`
· sinh bằng **`tools/gen_slides19.py`** (chạy lại được — sửa spec trong script rồi chạy, đừng sửa tay JSON)

| gate `check_vox.py --channel co-dai` | |
|---|---|
| X1 thẻ `title` | **2** / trần 4 · không 2 thẻ liền nhau ✅ |
| X3 lặp kind liên tiếp | max **2** (timeline×2) ✅ |
| X4 pin y max | **600** / safe_bottom **678** ✅ |
| X5 thẻ `source` | **3** (東京都下水道局 · 澱粉科学 1972 · 配管メーカー) ✅ |
| **X2 ảnh thật ≥50%** | **14/26 = 54%** ✅ |

✅ **GATE VOX PASS X1–X5 (2026-08-12)** · **81/81 ảnh đã vào chỗ** (vox 18/18 · slides 63/63) · 26 thẻ dựng xong, **0 thẻ nền phẳng vì thiếu ảnh**.

### 🔴 Bốn lỗi bắt được khi DUYỆT MẮT contact sheet — gate không thấy cái nào

Đây là bằng chứng mới cho luật *"gate PASS ≠ đúng"*: cả 4 lỗi đều lọt X1–X5.

| lỗi | nguyên nhân | sửa |
|---|---|---|
| 2 thẻ `flow` **NÁT CHỮ**, pin đè lên nhau | tao hạ pin xuống 250/340/430 để thoát cảnh báo safe_bottom → khe chỉ 90px, ngắn hơn chữ | pin **235/350/465** + rút ngắn nhãn (`内径が細る`, `分子が出る`, `漉して使う`) |
| Thẻ `熱が届く範囲` vẽ ra **`階段が煙突になる`** (cầu thang thành ống khói) | dùng `room` preset `stack` mà không kiểm nó trả về hình gì | đổi sang `stat` **`2メートル`** |
| **4 thẻ bị ảnh tối NUỐT tiêu đề** (`洗い物の、すぐあとに` · `熱は、届いていない` · `50度でも、90度でも` · `三つだけ`) | tiêu đề của `process`/`compare` vẽ bằng **mực đậm** (thiết kế cho nền phẳng) → ảnh tối nào cũng giết. `flow`/`timeline` không bị vì tự vẽ dải vàng | **bỏ `bg:photo`** khỏi 3 `process` + 1 `compare` (`NO_PHOTO` trong generator). ⚠️ Đã thử `duotone:ink` trước và nó **TỆ HƠN** — ảnh tối thêm; duotone chỉ cứu được 2 thẻ `stat` (chữ trắng), đó là lý do 2 thẻ đó giữ duotone |
| `slide_00` ghi vào folder rác **`ides_img`** | `read_text().strip()` xoá 2 space đầu **của cả file** ⇒ chỉ dòng 1 lệch, `l[5:]` cắt thành `ides_img` | parse tên bằng **regex** `^\s*\d+\s+` thay vì cắt theo vị trí, vá ở `place19.py` + `place19b.py` |

### 🔴 Bài học ĐẮT NHẤT về prompt ảnh — lỗi của Claude, không của tool

Lô ảnh 1 (82 ảnh) có **tông rất đồng nhất** nhưng **không một ảnh nào là macro thật**: mọi ảnh thành *"phòng washitsu đẹp + vật nhỏ ở đâu đó"* (ống **gốm** thay ống thoát nước · bã cà phê **rắc trên mép bàn** thay hạt phóng đại · thẻ `kitchen_sink_drain_opening` **không có miệng cống trong khung**).

**Nguyên nhân: chính STYLE string.** Cụm `Japanese home interior, soft natural daylight from a side window` **ép framing phòng vào MỌI ảnh**, kể cả khi đề bài là "bên trong lòng ống".
🔴 Với thẻ vox thì đây là **chí tử** — vox *annotate đè lên ảnh*, chủ thể không rõ thì pin/mũi tên trỏ vào không khí.

⇒ Đã tách **`STYLE_MACRO`** (bỏ `home interior`/`side window`, thêm `subject FILLS THE FRAME, tight crop, plain dark out-of-focus background, NO room, NO window, NO furniture`) và bảng **`MACRO_LINES`** + toàn bộ 18 ảnh vox. Lô 2 (36 ảnh) gen theo style mới → đúng framing.
📌 **Áp cho video sau:** ảnh cho thẻ vox **luôn** dùng STYLE_MACRO. Style lock giữ tông là tốt, nhưng nó cũng khoá luôn framing — phải có 2 biến thể.

### 🔧 VÁ `make_vox.py` — user chốt phương án ③ (2026-08-12)

**Vấn đề:** user chê 3 frame nền phẳng *"lệch so với các frame khác"*. Nhưng bật ảnh cho chúng thì tiêu đề + nhãn chart mất chữ. Đo được **3 cách xử lý ảnh đều thất bại**: `darken` (mất nhãn trục) · `scrim` top=0/195 (**không ăn**) · `duotone:ink` (line tạm được, **bar TỆ HƠN** — `普通の管`/`食洗機の排水` mất hẳn).

⇒ Nguyên nhân **không nằm ở ảnh mà ở CHÍNH NHÃN**: chúng vẽ bằng `P["muted"]`/`P["ink"]` cỡ 36–46 **không stroke**, đúng cho nền kem phẳng. Đã vá **6 chỗ** trong `_media_library/make_vox.py`:

| # | chỗ vá | nội dung |
|---|---|---|
| 1 | `head_line(..., highlight=on_ph)` cho **bar · line · compare · process** | dải vàng sau tiêu đề — trước đó chỉ `flow`/`timeline` có |
| 2 | helper mới **`_onph(on_ph, w)`** | trả kwargs stroke; `on_ph=False` → **kwargs rỗng**, nhánh cũ nguyên vẹn |
| 3 | `_bars()` + tham số `on_ph` | nhãn cột → chữ trắng + stroke ink; số giá trị → stroke trắng |
| 4 | `k_line` trục + nhãn mốc | trục sáng hơn (6px), nhãn mốc trắng + stroke, cỡ 36→40 |
| 5 | `kicker(..., on_photo=…)` cho 4 kind | chỉ 3/13 chỗ gọi từng truyền tham số này |
| 6 | `src_label(..., on_photo=…)` cho 4 kind | như trên (3/12) |

⭐ **BÁN KÍNH ẢNH HƯỞNG = 0 NGOÀI CO-DAI, đã kiểm bằng máy — và nó phủ định lo ngại ban đầu của tao:**
- `channels.py`: **`co-dai` là kênh DUY NHẤT có hồ sơ `vox`**; 8 kênh còn lại (health · nagaiki · shokutaku · nenkin · kaigo · akiya · showa · showa-b) **không có** → `make_vox` báo lỗi và từ chối chạy.
- **nenkin KHÔNG dùng `make_vox`** — nó dùng `make_stage.py` (66 PNG `clip_*` của nó là stage, không phải vox). Tao nhận việc này với điều kiện "test lại nenkin", và phép đo cho thấy **không có gì để test**.
- Mọi thay đổi đều gác sau `on_ph` (= `_photo and not _light`) → thẻ **không** khai `bg:photo` chạy y hệt bản cũ.
- Smoke test: `make_vox.py demo --channel co-dai --still` → **13/13 kind, exit 0**.

⚠️ **Một hệ quả biết trước:** video **17** (15 thẻ) và **18** (3 thẻ) đã ĐĂNG cũng có chart/compare/process mang ảnh → **nếu re-render thì trông khác bản đã lên sóng** (nhãn trắng có viền thay vì mực đậm). Không ảnh hưởng video đang live. Backup: `make_vox.py.bak_20260812` (trước vá 1) · `make_vox.py.bak2_20260812` (trước vá 3–6).

**Kết quả:** **26/26 thẻ vox có ảnh nền · 89/89 frame là ảnh · 0 frame nền phẳng** · gate vox PASS X1–X5.

### Tool đã lưu
`tools/gen_slides19.py` (sinh SLIDES + prompt) · `tools/gen_vid19.py` (prompt video) · `tools/place19.py` (khớp lô 1) · `tools/place19b.py` (khớp lô TODO, ghi đè bản sai framing) · `tools/enable_clips19.py` (bật `video:true` chỉ khi clip tồn tại)

**Phân bố kind:** compare 4 · flow 4 · source 3 · process 3 · timeline 3 · stat 2 · bar 2 · line 2 · title 2 · room 1
**Thẻ đắt nhất:** `stat 20度` (hook) · `bar 脂50/配管60` (khe MỞ) · `compare 二つの60度` (khe ĐÓNG) · `line 老化 2〜4度` · `compare 50度でも90度でも` (かす) · `process 今夜の順番`
⭐ **Entry 0 = `kitchen sink drain opening`** — đúng luật `media-library.md` §2.0 (ảnh đầu phải là CHỦ THỂ, không phải mood).

### Ảnh cần gen — 81 prompt
- **`19_haisuiko-naze-tsumaru_IMG_FLOW.txt`** — 81 prompt, **mỗi prompt 1 dòng**, style khoá đầu dòng → bơm cả file qua extension Flow (`project_flow_batch_ext`)
- **`19_haisuiko-naze-tsumaru_IMG_NAMES.txt`** — thứ tự dòng ↔ tên file đích
- Đích: `06_VIDEO/19_haisuiko-naze-tsumaru/slides_img/slide_NN.jpg` (63) + `.../ai_clean/<tên>.jpeg` (18)
- ⚠️ Prompt đã khoá `no text, no letters, no logos, no brand labels, no human faces, no watermark` — vẫn phải **quét watermark ✦ trước khi dùng** (`feedback_anh_ai_quet_sach_watermark`)
- ⚠️ **Ảnh AI realistic trong video ⇒ TICK "altered/synthetic content" lúc upload** (`youtube-compliance.md` §2.1). `upload_pack.py` chưa có cờ này → **tick TAY**.

## 📊 Đo & gate (điền sau khi chạy)

- [ ] `python tools\check_coldopen.py 19` → phải **0 FAIL** (gồm **O16** mới)
- [ ] Đếm ký tự bản `_TTS.md` (trừ tag) → mục tiêu 7.600 ±15%
- [ ] `python E:\Claude\Projects\_media_library\check_vox.py …` sau khi có SLIDES
- [ ] Thumbnail: duyệt 3 cấp (full · 168px · 120px) + **đặt cạnh 06/17 để so khác biệt**
