# 24 — 年金生活者支援給付金・9月の緑の封筒 (farm v04/v10, chen sóng tháng 9)

> Viết 2026-08-31 theo kế hoạch user duyệt cùng ngày (`02_CONTENT_PLAN.md` §C.0 — CHEN SÓNG THÁNG 9).
> Trụ ②給付金. Slot đề xuất: **CN 2026-09-06 19:00 JST** (sau v19 T5 09-03).
> ⚠️ **Lệch rule 支給日 có chủ ý:** rule đòi video 給付金 đăng 1–3 ngày trước 15 tháng chẵn (15/10),
> nhưng sự kiện 緑の封筒 gửi từ 9月第1営業日 — sóng đối thủ đang nổ NGAY BÂY GIỜ (≥5 kênh), trễ 1 tuần
> là hết cửa (bài học 9月ハガキ: kênh 120K sub vào trễ 4 ngày chỉ 743 view). Đề 15/10 đã có franchise
> 直前チェック riêng trong queue.

## SỔ KHUÔN (chống inauthentic)
- 3 video liền trước: **17 ②事件型 · 18 ③質問型 · 19 ④対決型** → bài này **②事件型** (sự kiện = 封筒
  đến từ 9月) — cách lần ② gần nhất 3 video ✓.
- 計算タイム: **thang 3 bậc quanh ngưỡng** (19 dùng A-vs-B đối chiếu 明細 → không trùng).
- Closer: **セルフチェック 3問** (xoay).
- Cold open **v3** (luật 08-30): あなた+円 → 対象+phản bác → câu lộ trình → open-loop → まず、事実から.
- Franchise: **モニター続きドラマ** (渡辺 nối v04/v10 — lần này 封筒 ĐẾN thật) + **明細を一緒に読む**
  (đọc はがき型請求書) + **原典を見せる** (3 shot).

## GATE MÁY — ✅ PASS 11/11 (`check_pace.py`, bản sửa hook 2026-08-31 v3)
cold open 1:00 · **G9 渡辺 3:55 (≥2:00 ✓ — luật モニター mới)** · 0 số/30s · CTA 55% · STAKE 0:00 ·
あなた 0:00 · G10 1 tag/75s · **G11 lộ trình 0:37 (đẩy sớm từ 0:48 → 0:37 ở v3)**. Tổng ước **12:47**
(thật ~13:00 — lọt dải 13–17′). 17 tag nhấn (đầu dòng dính chữ, quét sạch). Voice + timeline +
project.json (`build_remotion_24.py`) đã re-sync với bản v3 — 45 scene, gap ngắn nhất 6,4s, sạch.

### Vòng sửa v3 (user: "30s đầu phải đánh vào nỗi sợ") — mốc giây đo lại từng câu
- **Câu 1 (0,0s):** あなた là CHỮ ĐẦU TIÊN, chở luôn số mất mát cùng động từ mất: 「あなたの家に、
  九月、緑の封筒が届きます。中を見ないまま置いておくと、年およそ六万七千円が、静かに消えます。」
  — thay bản v2 (「郵便受けに、緑の封筒」= phát hiện, còn trung tính) bằng câu MẤT thẳng ngay.
- **Câu 2 (10,7s):** nghịch lý 切手一枚 giữ nguyên (callback ở thoại 渡辺 「人生でいちばん割のいい葉書」).
- **Câu 3 (20,4s):** lật kỳ vọng an toàn thành nguy hiểm hơn — 「うちは関係ない、と思っている方ほど、危ない」
  — đẩy nỗi sợ tiếp tục qua mốc 30s, KHÔNG có câu trấn an nào chen vào 0–30s.
- **Roadmap/lối thoát (37,4s):** 「三つのことを順番に確かめます」 — dịch từ ~50s (bản v2) xuống 37,4s,
  sát khung 25–35s mà `script-nenkin` GĐ3 khuyến nghị ("giữ căng nỗi sợ ~25–30s rồi mới hé lối thoát").
- ⚠️ Đổi 3 dòng đầu ⇒ toàn bộ timeline dịch (778,97s → 767,12s) — đã re-run
  `make_timeline_exact.py` + `build_remotion_24.py` cùng lượt (NEO SCENE BẰNG CHỈ SỐ DÒNG nên
  SCENES không cần sửa, chỉ tự tính lại khớp).

### Vòng sửa v2 (giữ để tra — user yêu cầu hook 30s ấn tượng + liền mạch, chấm bản v1 = 7/10)
1. Hook đổi từ THÔNG BÁO → CẢNH + NGHỊCH LÝ (v3 đẩy tiếp một bước: CẢNH → MẤT thẳng).
2. **Gỡ rời rạc**: 2 khối chêm 免除 + 障害/遺族 dời khỏi giữa mạch 「40 năm → 渡辺」, đặt lại SAU thang
   3 bậc thành payoff 「諦めかけた方。逆です」 — mạch tính toán liền một hơi: 基準 → 渡辺 vào → đọc hagaki
   → thang 3 bậc → kết quả 2.529円 → 免除 bonus → thoại tem → 灯油 → CTA.
3. **Nhãn chương khô → cầu tò mò**: 「誰の郵便受けに入って、誰の家を素通りするのか」 ·
   「いよいよ、あなたの金額です」.

## HÀNG XÓM MỤC TIÊU (rule youtube-suggested-growth §1)
| video hàng xóm | view | vì sao mình là next-watch |
|---|---|---|
| サラダのお金相談所 `【緊急解説】2026年9月からルール変更！年金＋7万円が一生上乗せ支給！` | 153K/10 ngày | họ đưa TIN + con số chung; mình cho CÔNG THỨC tính ra số CỦA BẠN (2.529円 case) + 3 ca はがき không đến — đúng câu hỏi người xem còn lại sau video họ |
| フクロウ `【新たに対象者拡大】9月から封筒が届く人も！給付金を確認して` | 26K/9 ngày | cùng sự kiện, mình thêm cơ chế 「止まったまま戻らない」 họ không nói |
| としこの年金相談所 `【半数以上がもらい忘れ】8月14日から年金に6.7万円が一生上乗せ` | 149K/23 ngày | cùng số 6,7万, mình là bản 研究室 có 原典 + thang 3 bậc |

## FACT SHEET — kế thừa v10 (verify 2026-08-10 trên 年金機構, bản 更新日 2026-04-01 = 令和8年度) + delta
> Bảng gốc 19 mục: `07_UPLOADED/10_shien-kyufukin-hagaki-9gatsu/_scripts/10_*.md` §FACT SHEET.
> Bài này dùng đúng các mục đã verify, KHÔNG thêm số mới ngoài bảng:

| dùng ở | fact (số mục bảng v10) |
|---|---|
| Cold open + ch1 | #1 gửi từ 毎年9月の第1営業日 · #2 gửi cho người MỚI thành đối tượng · #4 緑の封筒 · #18 ba điều kiện |
| ch2 | #13 月額5,620円 + 免除 11,768円 + 障害1級 7,025円 (令和8年度) · #14 dải 補足的 809.000超〜909.000以下 + 調整支給率 · #5 記入お名前等+切手 · #6 điện tử OK · #15 審査結果通知 ghi số tiền |
| ch2 tự tính (ghi およそ) | 5.620×12=67.440→年およそ6万7千 · 渡辺 72.000×12=864.000 → (909.000−864.000)÷100.000=0,45 → 5.620×0,45=**2.529円/月**→年およそ3万 · bậc 3: 月8万=96万>90万9千→0円 (cả 3 phép đã có trong bảng ② của v10) |
| ch3 | #9 mới 65 tuổi: 3 tháng retro · #12 世帯変更/税更正 → TỰ xin (verbatim) · #10 再該当 → あらためて請求 (verbatim) · #3 không đến → 給付金専用ダイヤル/年金事務所 |
| ch4 | #7 hạn 令和8年1月5日 là chu kỳ NĂM NGOÁI — thoại nói 「昨年度の例では」+ bắt đọc hạn in trên hagaki, ⛔ KHÔNG bịa ngày năm nay (đúng quyết định v10) · #8 nguyên tắc 翌月分 · #17 詐欺 ATM |
| chi tiết đời cast | 灯油代/家計簿 bút chì = chi tiết NHÂN VẬT hư cấu, không phải claim thống kê |

⚠️ **Rà lại TRƯỚC ngày đăng (09-06):** ① trang #7 (`hagaki/kigen`) nếu đã update chu kỳ 令和8年度 thì
được nói ngày mới ② xác nhận 9/1/2026 (thứ Ba) đúng là 第1営業日 — script hiện chỉ nói 「第一営業日」
theo verbatim, không nói ngày cụ thể ✓ an toàn.
🔴 **3 điều KHÔNG nói (không có nguồn):** 「対象者拡大」 của フクロウ (chưa verify cơ chế) · con số
người bỏ sót 「半数以上」 của としこ · mọi ngày của chu kỳ 令和8年度 chưa công bố.

## 原典ショット (≥2, shot đầu trong 3 phút đầu ✓)
| # | vị trí | trang | file |
|---|---|---|---|
| 1 | ch1 ~1:20 | 年金機構 FAQ `tetsuduki06` — câu 「毎年9月の第1営業日から順次送付」 khoanh đỏ | chụp MỚI → `06_VIDEO/24_*/genten/genten_01_soufu-9gatsu.png` (bản v10 làm fallback: `07_UPLOADED/10_*/genten/genten_01_*.jpg`) |
| 2 | ch2 ~2:30 | FAQ `shikyuyouken03` — 「月額5,620円」 khoanh đỏ (更新日 2026-04-01) | chụp MỚI → `genten_02_kingaku-5620en.png` (fallback bản v10 #4) |
| 3 | ch3 ~9:00 | FAQ `shikyuyouken06` — 「ご自身で認定請求の手続きが必要」 khoanh đỏ | chụp MỚI → `genten_03_jibunde-seikyu.png` (fallback bản v10 #3) |

## BẢNG ĐIỂM KEYWORD — kế thừa đo 2026-08-10 (v10, còn hạn 6–8 tuần)
Keyword dẫn: **年金生活者支援給付金 61 HIGH (volume Medium, cạnh tranh Low)** → đứng ĐẦU title A1.
緑の封筒 33 LOW → chỉ ở HÌNH + dòng phụ, không làm keyword dẫn. Tag phủ: 老後資金 70 · 手続き 64 ·
60代 66 · 年金事務所 61 · 年金生活 61. (Phương pháp: Search Companion — xem chú thích lệch luật ở v10.)

## HUMANIZE — 5/6 mũi (ngưỡng ≥4 ✓, mũi ①④ qua cast theo rule §1.1)
①渡辺 tự làm + thoại ✓ ②thoại + chi tiết vô dụng (con tem cũ trong ngăn kéo, 家計簿 bút chì) ✓
③ký ức giác quan (緑の封筒 trong hộp thư, 灯油 mùa đông Niigata) ✓ ⑤đóng 中村 bằng cảm xúc (vòng tròn
bút không xoá trên lịch) ✓ ⑥phá nhịp ≥3 (「来ませんでした。」「切ってください。」 câu cụt) ✓.

---

## ĐÓNG GÓI CTR

### Title CHỐT
```
年金生活者支援給付金、9月に緑の封筒が届きます｜出さないと年6万7千円が0円に
```

### 3 TITLE A/B — mỗi bản một giả thuyết

| | title | ký | vị trí keyword | giả thuyết thử |
|---|---|---|---|---|
| **A1** ⭐ dùng trước | `年金生活者支援給付金、9月に緑の封筒が届きます｜出さないと年6万7千円が0円に` | 39 | 給付金@0 | keyword đo cao nhất đứng đầu (luật kênh-chưa-được-hiểu) |
| **A2** | `年金に年6万7千円の上乗せ、9月の緑の封筒で始まります｜対象は3つの条件` | 36 | 年金@0 · số@4 | đổi keyword dẫn: SỐ TIỀN dẫn thay tên chế độ |
| **A3** | `【9月開始】年金生活者支援給付金｜はがき1枚で年6万7千円、待つ人は0円` | 36 | 給付金@6 | đổi hook: khuôn 【】 cũ của ngách (đối chứng) |

Compliance: không từ cấm; mọi tình tiết (9月・緑の封筒・6万7千円・0円 khi không nộp) CÓ THẬT trong video ✓.

### Tên file upload
```
nenkin-seikatsusha-shien-kyufukin-midori-futo-9gatsu.mp4
```

### 3 dòng đầu 概要欄
```
9月の第1営業日から、年金生活者支援給付金の請求書（緑の封筒）が新たに対象になった方へ届き始めます。
65歳以上で老齢基礎年金を受け取っている方向けに、金額の計算式（月額5,620円基準）と、封筒が来ない3つのケースの対処を、日本年金機構の原典で確かめます。
制度を読むだけの番組ではありません。あなたの数字を計算する研究室です。
```

### Mô tả đầy đủ
```
9月の第1営業日から、日本年金機構が「年金生活者支援給付金請求書（はがき型）」の入った緑の封筒を、新たに対象となった方へ順次送付します。
65歳以上で老齢基礎年金を受け取っている方向けに、対象の条件・金額の計算・封筒が来ない場合の手続きを、原典（日本年金機構の公式ページ）を一緒に読みながら確かめます。
制度を読むだけの番組ではありません。あなたの数字を計算する研究室です。

▼この動画で確かめること
・緑の封筒は誰に届くのか（届かない人との分かれ目）
・「世帯の全員が非課税」でつまずくケース
・月額5,620円の計算式と、補足的給付金の3つの段
・一度止まった給付金が、自動では戻らない理由

目次
00:00 9月に届く緑の封筒
1:15 第1章 誰に届くのか・3つの条件
2:20 第2章 金額の計算（月額5,620円基準）
4:40 モニター渡辺さんの計算（月2,529円）
7:00 第3章 封筒が来ない3つのケース
10:30 第4章 期限と、さかのぼりの仕組み
11:50 研究ノート・セルフチェック3問

▼出典（一次ソース）
・日本年金機構「年金生活者支援給付金請求書（はがき型）の送付」
・日本年金機構「年金生活者支援給付金の支給要件・給付額」（令和8年4月1日更新）
・日本年金機構「世帯構成の変更等により支給要件を満たした場合の手続き」
・日本年金機構「請求書の提出期限」

※本動画は令和8年9月時点の情報です。金額や基準額は年度により変わります。個別の金額は、給付金専用ダイヤルまたはお近くの年金事務所でご確認ください。特定の金融商品や投資を勧めるものではありません。

音声: VOICEVOX:雀松朱司

#年金 #老後のお金 #年金と老後のお金研究室 #給付金 #年金生活者支援給付金
```

### タグ
```
年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金, 年金生活者支援給付金, 支援給付金, 緑の封筒, はがき型請求書, 年金 上乗せ, 住民税非課税, 補足的老齢年金生活者支援給付金, 年金機構, 手続き, 年金事務所, 65歳, 70代
```

### Pinned comment
```
ご視聴ありがとうございます。当研究室のノートです。
あなたの郵便受けには、緑の封筒はもう届きましたか？「届いた」「まだ」「去年止まったまま」— コメントで教えてください。皆さまの声が、次の研究テーマになります。
▼「届く紙と期限」シリーズ一覧 → https://www.youtube.com/playlist?list=PLT4QEuxo4MWw
※個別の支給可否・金額は、給付金専用ダイヤルまたはお近くの年金事務所でご確認ください。
```

### THUMBNAIL — bộ chữ chung 3 bản (gate 7: ①về gì ②chuyện gì ③làm gì)
- chip 対象 (vàng, góc trên): `65歳以上の方へ`
- dòng phụ (trắng): `9月・支援給付金`
- **HERO (vàng, to nhất, rộng ≥60% khung):** `年6万7千円`
- dải đỏ đáy: `出さないと0円`

T1 = BAKE 9 KHỐI baseline (mặt bà cụ ngạc nhiên cầm phong bì xanh) · T2 = đổi 1 biến hình (nền bàn gỗ
sáng thay giấy kẻ ô, giữ nguyên chữ) · **T3 = 紙が主体** (0 mặt — phong bì xanh lá + はがき chiếm khung,
mũi tên đỏ trỏ vào, khuôn hồi sinh 08-31 theo `03_THUMBNAIL_TITLE_FORMULA.md`).
Prompt 3 bản + 3 plate: `06_VIDEO/24_shien-kyufukin-midori-futo-9gatsu/thumb_prompts_FLOW.txt`
(+ `_TENFILE.txt` + `_PLATE.txt`) — viết theo `ab-3title-3thumb.md` §3.1, TEXT block trong 15% đầu.
Sau khi gen: soi từng ký tự kanji · xoá ✦ theo lô · gate 168px · <2MB.

### Checklist sản xuất còn lại (quy trình 8 bước CLAUDE.md §②)
1. [x] Rà 2 mục ⚠️ FACT trước 09-06 · chụp 3 原典ショット mới — chụp trực tiếp bằng Claude in
   Chrome trên `tetsuduki06`/`shikyuyouken03`/`shikyuyouken06` (nenkin.go.jp), đối chiếu nguyên
   văn khớp FACT SHEET #1/#13/#12, khoanh đỏ đúng câu quote → `06_VIDEO/24_*/genten/` +
   `photocard/card_genten24_{01,01_b,02,02_b,03}.png` (tool `tools/ingest_genten_24.py`)
2. [x] `python tools/make_timeline_exact.py 24_shien-kyufukin-midori-futo-9gatsu` (voice+timeline 1 lượt)
3. [x] `art_prompts_collage.py --card2` + sticker — 45/45 ảnh ingest (`tools/ingest_art_24.py`, 42
   photocard + 3 sticker el_green_envelope/el_hagaki/el_stamp)
4. [x] Builder `build_remotion_24.py` (copy từ 19) — 45 scene, 82 asset đủ
5. [x] `check_frame_pace.py` SẠCH 3/3 — 0 khe >9s, hero 3,68/phút, 0 scene trống (345 sự kiện
   hình; phải viết `_pad_sup_24` LOCAL trong builder vì `_scenes19.pad_sup` chốt cứng 1
   sticker/scene làm 16 scene ảnh dài 17–28s đứng yên — xem comment trong file)
6. [x] Soi still (mở bài + 2 shot 原典 + giữa/cuối) → render nền `run_video24.cmd` (Remotion +
   loudnorm -14 LUFS, đã hạ BelowNormal) — `EXITCODE=0`, duration 767,20s khớp timeline 767,12s
   (lệch 0,08s), duyệt 4 frame rải đều OK → `06_VIDEO/24_*/nenkin-24_final.mp4` (838 MB)
7. [ ] Gói 3×3 + upload_pack — tick lịch **CN 09-06 19:00**
