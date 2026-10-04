# CLAUDE.md — youtube-jp-nenkin

> Rule riêng cho kênh 年金・老後資金 (JP 50–70). Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research → `SecondBrain/10_Projects/youtube-jp-nenkin/`.

## Trạng thái project — ĐÃ CHỐT ĐỦ (2026-07-19)

- **Tên kênh:** 「年金と老後のお金研究室」
- **Persona:** nghiên cứu viên điềm đạm của "研究室" — mở bài bằng case đời thường rồi mổ chế độ bằng số liệu; xưng 当研究室/私たち; KHÔNG tự xưng FP/chuyên gia có phép hành nghề ("người cùng đọc tài liệu gốc giúp bạn").
- **Giọng TTS:** VOICEVOX **雀松朱司 / ノーマル (style 52) / tốc 0.9** — demo chốt: `00_VOICE_TEST/demo_52_suzumatsu-akashi_normal.wav`. Credit 概要欄: 「音声: VOICEVOX:雀松朱司」.
- **読み của 方 trong `_TTS.md` (rule 2026-08-19, sau khi viewer bắt lỗi video 12 「148万円以上の方」 bị TTS đọc thành ほう):**
  - Nghĩa **ほう** (so sánh/phía) → **PHẢI viết hiragana ngay trong script**: 「住民税のほう」「出したほうがいい」.
  - Kanji 「の方/この方/その方/あの方/どの方(々)」 còn lại → `tts_render.py` (shared, `..\youtube-jp-health\tools`) **tự ép đọc かた/かたがた** trước khi synth, log `🔤 読みfix`. Áp cho MỌI kênh dùng pipeline này.
  - 方 sau hiragana khác (「かかる方」「出した方が…」) máy không tự quyết được かた/ほう → render in `⚠ 方 chưa rõ かた/ほう`; thấy warning thì sửa script thành kana rõ nghĩa rồi render lại. Viết script mới: 方 nghĩa かた sau động từ thì viết thẳng kana 「〜されるかた」 cho khỏi dính warning.
- ⛔ **ĐỀ XUẤT NÀY ĐÃ CHẾT — 2026-08-10 user chốt độ dài 13–17′ (xem §ĐỘ DÀI).** Giữ đoạn dưới làm
  hồ sơ vì sao từng định làm ngược lại: nó dựa trên median 26–37,5′ đo trên **bộ kênh khác**, còn
  hai kênh nổ mạnh nhất hôm nay có median hit **15′00**. ⤵ (nguyên văn đề xuất cũ)
- 🔴 ~~**ĐỀ XUẤT CHỜ USER CHỐT (2026-07-28) — NÂNG ĐỘ DÀI 15–25′ → 25–40′.**~~ Khám kênh đo được đây là **lệch format lớn nhất** so với ngách (`CHANNEL_DIAGNOSIS_2026-07-28.md` §2): median độ dài **完全攻略 ~36′ · 速報 37,5′ · 節約看護師 26′**, và **không kênh benchmark nào có video dưới 17′**; hit 3,84M dài 25,2′, hit 1,05M dài 36,4′. nenkin đang **13,5–20,3′ (median 15,5′) = bằng nửa chuẩn ngách**. Ở hệ số 434 ký/phút thì **25′ ≈ 10.850 ký · 30′ ≈ 13.000 ký · 36′ ≈ 15.600 ký** (gấp ~2× script hiện tại ~6.700 ký). **Chưa tự sửa chuẩn** vì đây là quyết định nội dung + gấp đôi công/video, phải user gật. Đi kèm: **title mở bằng 【】** (benchmark 51/52 video dùng, nenkin 1/4).
- **⚠️ Hệ số độ dài ĐO THẬT (2026-07-19, script 01 full):** ~4.900 ký tự → **11 phút 18 giây** (gap 0.45s/dòng + 1.0s/đoạn) ≈ **434 ký tự/phút** — 雀松朱司@0.9 đọc NHANH hơn ước lượng 300–350. → Muốn video 15–25 phút phải viết **~6.500–10.800 ký tự**. Dùng hệ số này khi lên dàn ý, đừng ước chay.
- **Lịch đăng:** ⭐⭐ **T3·T5·CN 19:00 JST — 3 video/tuần** (ĐỔI 2026-08-03, user chốt nhịp toàn hệ thống *"2 ngày 1 video cho tất cả các kênh"* — đè mốc 1/tuần bên dưới). Giờ 19:00 GIỮ NGUYÊN. 🔴 **ĐÁNH ĐỔI PHẢI BIẾT: bộ ngày này KHÔNG chứa T6** — mà T6 là ngày lõi ĐO ĐƯỢC của cụm tiền-senior (完全攻略 median T6 **742K**, 節約看護師 **48/50 video**), tức slot mũi nhọn cũ đã rời lịch. **Muốn giữ T6 mà vẫn đúng nhịp 2 ngày: đổi sang T3·T6·CN** = `[(1,19),(4,19),(6,19)]` trong `upload_pack.py` (giãn 2-2-3 vẫn đạt) — phương án này đúng luật, chưa áp vì user chọn bộ B. Rule 支給日 vẫn **đè lịch** bằng `--slot`. Gate FACT SHEET / Retention Audit / 2 thumbnail vẫn đứng TRÊN lịch: không qua → **bỏ slot**, và độ dài 25–30′ nghĩa là 3 slot/tuần = gấp ~6 lần công/tuần so với 1 video 15,5′. Nguồn sự thật: `.claude/rules/upload-schedule.md` Mục 0.9.
- (căn cứ cũ, giữ để tra) ⭐ **T6 19:00 JST — 1 video/tuần · T3 = slot PHỤ chỉ cho 支給日/tin chính sách nóng** (CHỐT LẠI 2026-07-28 sau khi KHÁM KÊNH — bằng chứng: **`CHANNEL_DIAGNOSIS_2026-07-28.md`**). Kênh 8 ngày tuổi: 4 video, 7 view, 0 sub, **0 view từ browse/suggested**, không án phạt (index tốt, 2 video hạng 1–2 long-tail). Hạ nhịp vì winner 完全攻略 lúc ramp chạy ~1 video/tuần (hit 3,84M ở **video #3, ngày thứ 13**) và vì độ dài phải tăng gấp đôi (xem mục Độ dài dưới). 🔴 **Giờ/ngày KHÔNG mở được vòi phân phối** — winner đăng rải 03:32–23:42 không giờ cố định vẫn ăn 3,84M; ưu tiên thật: **độ dài → title 【】 → đề tài**. (Ghi chú lịch cũ T3·T6 2/tuần, chốt sáng cùng ngày từ đo publishedAt: NGÀY SỬA 2026-07-28: đo publishedAt 50 video/kênh → lịch cũ T2·T4 trúng đúng 2 ngày yếu nhất ngách. 完全攻略 median view **T6 742K**, **T2 = 0 video suốt đời kênh**; 速報 median **T3 119,5K cao nhất · T4 4,9K thấp nhất**; cả cụm tiền-senior khóa T6 — 節約看護師 48/50. Bằng chứng: `.claude/rules/upload-schedule-measure-2026-07-28.md`. Giờ 19:00 giữ nguyên. **T6 = slot mũi nhọn, dồn video mạnh nhất.**) (chốt lại 2026-07-25 sau khi đo benchmark: 3 kênh tăng nhanh nhất ngách đăng ≤1,3/tuần; 完全攻略 12 video → 132K vs 給付金チャンネル 1.971 video → 87K = chênh 27 lần view/video → **volume là chiến lược thua**). Không qua FACT SHEET / Retention Audit / 2 bản thumbnail → **bỏ slot**, 1 video xuất sắc hơn 2 video nhạt. + rule 支給日 đè lịch. Bằng chứng: `CHANNEL_BENCHMARK_2026-07-25.md`.
- **Bộ nhận diện metadata 2.4 (chốt 2026-07-25, đã live trên kênh — nguồn sự thật: `CHANNEL_BACKFILL_2026-07-25.md`):** categoryId **27** · rổ 12 tag nhận diện đứng đầu mọi video: `年金と老後のお金研究室, 年金, 年金いくらもらえる, 老後のお金, 老後資金, 年金生活, 給付金, 65歳からの年金, 定年後のお金, 年金受給額, 60代, シニア 年金` · 3 hashtag cố định đầu dòng hashtag cuối 概要欄: `#年金 #老後のお金 #年金と老後のお金研究室` (+ ≤3 hashtag đề tài).
- **CTA giữa video:** câu canonical mục 2.7 trong `.claude/rules/cta-midvideo.md`, chèn sau khối case-tính-thử (~50%).

## ⚠️ RULE BẮT BUỘC — YMYL TÀI CHÍNH (nghiêm như YMYL y tế bên health)

1. **KHÔNG tư vấn đầu tư / sản phẩm tài chính cụ thể.** Chỉ giải thích chế độ công khai (年金, 給付金, thuế) + số trung bình có nguồn.
2. **KHÔNG bịa số/nguồn.** Mọi con số phải từ nguồn thật ghi rõ: 日本年金機構 / 厚生労働省 / 総務省家計調査 / 内閣府 — rà link trước khi đưa vào script. Cấm bịa 「専門家によると」.
3. **Chế độ có hạn dùng:** mỗi video ghi 「◯年◯月時点の情報です」 trong script + 概要欄; cuối video 1–2 câu khuyên xác nhận tại 年金事務所 (gọn như quy tắc disclaimer health — KHÔNG chèn block dài giữa bài).
4. **Không hứa hẹn:** cấm 「必ず」「絶対得」; dùng 「〜の場合が多い」「制度上は〜」「一般的には〜」.
5. **Không đảng phái:** không tên chính trị gia/đảng trong title/thumbnail/script.
6. **Story hóa 年金生活** (tuyến 2): nhân vật hư cấu 100%, tên+thành phố+tuổi mới mỗi script, disclaimer フィクション.

## 🧬 SIGNATURE KÊNH (user chốt 2026-07-19) — DNA cố định NHỎ + cách kể XOAY VÒNG

> Nguyên tắc gốc: cố định = thứ tạo NHẬN DIỆN (<10% thời lượng); mọi thứ còn lại BẮT BUỘC đổi giữa các video — "kịch bản nào cũng giống nhau" là lỗi (user cấm + luật inauthentic content).

**CỐ ĐỊNH (DNA):**
1. Video = 1 「研究」: luôn có tinh thần 仮説→計算→結論, nhưng dàn bài KHÔNG cố định.
2. **「研究ノート」** — slide tổng kết 1 trang cuối video, visual template cố định (kiểu trang sổ lab), người xem screenshot gửi người thân được. Câu dẫn: 「それでは、今日の研究ノートです。」
3. **Dàn モニター cố định** (hồ sơ dưới) — nhân vật TÁI XUẤT xuyên video, đời sống tiến triển dần; mỗi video chỉ lấy 2–3 người hợp chủ đề, xoay người đóng chính. ⚠️ GHI ĐÈ luật "nhân vật mới mỗi script" của health — kênh này cast cố định LÀ signature (moat tích lũy).
4. Câu kết cố định: 「それでは、また次回の研究でお会いしましょう。」 + CTA canonical 2.4b.
5. **Vòng lặp khán giả (cơ chế thật):** comment hỏi case → định kỳ video 「視聴者の実験室」 tính case thật (ẩn danh hóa) — 「皆さまの声が、次の研究テーマになります」 không phải câu sáo.

**XOAY VÒNG BẮT BUỘC (không dùng lại khuôn của video liền trước — ghi khuôn đã dùng vào header mỗi script, như sổ xoay thumbnail health):**
- **Khuôn mở bài (5):** ① GAIN-REVEAL (mặc định, xem mục Viết kịch bản) ② 事件型 — mở bằng tin nóng/vụ lừa đảo ③ 質問型 — 1 câu hỏi khán giả làm đề bài ④ 対決型 — A vs B (65歳で受け取る?70歳まで待つ?) ⑤ 物語型 — kể chuyện 1 モニター trước, số liệu sau.
- **Khuôn 計算タイム (5):** thang 3 bậc quanh ngưỡng / A-vs-B đối chiếu / mô phỏng timeline 10–20 năm / ○×クイズ / tính ngược (muốn nhận X thì cần Y).
- **Tuyến nội dung xen kẽ:** 改正・給付金 → evergreen いくらもらえる → cảnh báo lừa đảo → 視聴者の実験室 → story 年金生活 — 2 video liền nhau không cùng tuyến.

**Hồ sơ モニター (số liệu đời nhân vật KHÔNG tự đổi giữa các video — muốn đổi phải có lý do cốt truyện):**
| Tên | Tuổi | Nơi | Nghề | Lương/年金 (万円/tháng) |
|---|---|---|---|---|
| 田中さん | 67 | 横浜 | tái tuyển dụng, tuần 5 buổi; **vợ 64歳・元正社員 厚生年金22年(264月)** (公開 script 06) | 年金16 + パート15 (公開 script 03) |
| 佐藤さん | 66 (**昭和34年11月生** — chốt script 07) | 仙台 | part siêu thị (quầy rau); 単身, chồng mất sớm, 1 con trai | 23 + 14 (自立ライン月16, chủ đạo script 03) · **特別支給の老齢厚生年金 月2.7万 · 61歳(令和2年11月)受給権 → 令和7年9月に請求、時効2か月前でセーフ、約156万円を一括受給 (script 07)** |
| 鈴木さん | 65 | 名古屋 | 役員; có 退職金 lớn | 45 + 20 |
| 高橋さん | 64→**65** | 東京 | 部長 → **退職 (script 02)**; vợ **昭和41年6月生・60歳** (kém 5 tuổi) → **振替加算 対象外世代** (script 06); ⭐ **script 12: vợ 「いま、お勤めはされていません」** → thuộc diện **配偶者控除** (所得税38万/住民税33万) | 50 + 20 |
| 山田さんご夫妻 | 67 & 65 | 大阪 | chồng tái tuyển dụng / vợ part; vợ **昭和36年8月生・厚生年金12年(144月)** → 振替加算 **年16,335円**; ⭐ chồng **繰り下げ待機1年 (66歳から受給)** → 加給年金 2年分 85万 mất 1年分 = **42万円** (script 06, mở màn + khép màn) | chồng 26+16 · vợ 10+9 (年金-only ≈ 25/tháng) |
| 伊藤さん | 68 | 福岡 | tự doanh quán cà phê (không 厚生年金); 単身 | 国民年金のみ 月6.5 (年~78) — đối tượng 支援給付金, công bố script 04 · ⭐ **script 10: từng nhận 支援給付金 → một năm quán bán tốt → thu nhập vượt ngưỡng → BỊ CẮT → năm sau tụt lại → phải TỰ XIN LẠI (không tự phục hồi)** |
| 松本さん | 60 | 千葉 | メーカー課長, vừa 定年, được chào 継続雇用 (**script 05**); ⭐ **script 11 chốt open-loop: CHỌN 継続雇用** (残る) — nhưng vẫn 定年でいったん退職して退職金を受け取る形 · **勤続38年**(22歳入社) · **退職金 2,000万円** → 退職所得控除 2,060万 ⇒ 課税ゼロ | 現役 55 → 再雇用打診 28 · 年金見込 18 (từ 65) · vợ 55 パート |
| **渡辺さん** ⭐ MỚI script 10 | 66 | 新潟市 | 元・縫製工場のパート (期間 厚生年金 ngắn); **単身** | **年金 月7.2 (年86.4万)** — 国民年金 480月 nộp đủ + chút 厚生年金. Nằm đúng **dải 補足的** (80万9千〜90万9千) → 支援給付金 月2529円 ≈ 年3万. Bỏ part-time mùa thu năm trước ⇒ **năm nay mới thành đối tượng** |
| **中村さん** ⭐ MỚI script 14 | 71 | **新潟県上越市（3級地）** | 元・学校給食の調理員（勤続40年）; **単身**, 夫は10年前に他界; 姉が新潟市（2級地）に在住 | **年金 月12.5 (年150万)** — 去年までは147万。上越市の非課税限度額 **148万円** を今年から超え、住民税は均等割5千円のみ（所得割0）· 介護保険料が第3段階3万9500円→**第6段階8万9100円**。⭐ script 14: 「増えたのに手取りが減る」逆転帯の主役 |

> ⚠️ **Vì sao phải thêm 渡辺さん (2026-08-10) — ràng buộc SỐ HỌC, không phải thích:** điều kiện
> 支援給付金 là 年金収入＋その他所得 ≤ **90万9千円**. Rà cả 7 モニター cũ — 田中 月16万 · 佐藤 14万 ·
> 鈴木 45万 · 高橋 ~16万 · 山田夫妻 26万/9万 · 松本 18万 → **vượt ngưỡng hết**; chỉ 伊藤 (6,5万) nằm
> trong dải. Tức **roster đang thiếu hẳn một モニター thu nhập thấp**, và mọi đề tài trụ ② 給付金 đều
> bị dồn vào một mình 伊藤. 渡辺 vá lỗ đó lâu dài, và nằm ở **dải 補足的** — thứ chưa nhân vật nào chở.
>
>
> ⚠️ **Vì sao phải thêm 中村さん (2026-08-19) — cùng loại ràng buộc, lần này là ĐỊA LÝ:** đề tài 住民税非課税の境目 đòi một モニター **ở 3級地** và **nằm trong dải biên 148万〜155万**. Rà roster: 横浜・仙台・名古屋・大阪・千葉・福岡 đều **1級地**, 新潟市 **2級地** ⇒ không ai ở 3級地; và theo 年金額 thì 伊藤 78万 · 渡辺 86,4万 · 佐藤 168万 · 田中 192万 · 高橋 240万 ⇒ **không ai nằm trong dải biên**. Roster thiếu hẳn một trục: **地方の小さな市**. 中村 vá trục đó.
>
> Tiến triển cast: 高橋 nghỉ hưu ở script 02 (64→65, quyết 繰り下げ). Số 田中 công bố script 03. 松本 xuất hiện script 05 (ngã ba tuổi 60 定年→即退職 vs 継続雇用) — quyết định của 松本 để mở open-loop, dự kiến tái xuất các video 定年/働き方 sau. **Script 06 (加給年金): 高橋 ĐẢO quyết định của script 02 — phát hiện 繰下げ待機中は加給年金が出ない (212万円 sẽ bay) → đổi sang「老齢厚生年金は65歳から受け取り、老齢基礎年金だけ繰り下げる」. Đây là lý do cốt truyện hợp lệ; các video sau phải dùng trạng thái MỚI này, đừng quay lại "高橋 đang 繰り下げ toàn phần".** Đổi số tiếp phải có lý do cốt truyện.

**Định vị 1 câu:** 「制度を読むチャンネルじゃない。あなたの数字を計算する研究室。」

## 🔒 KÊNH KHÓA 3 TRỤ (user chốt 2026-07-23) — KHÔNG mở rộng ngoài đây

> Kênh = **TÍNH SỐ HỘ cụ già** về 年金・給付金・税. Benchmark 完全攻略 12 video→130K bằng ngách hẹp này. Chi tiết hàng đợi + bằng chứng: `02_CONTENT_PLAN.md`.
> - **① 年金 tính số** (funnel lõi): いくらもらえる / 何歳受給の末路 / 繰上げ繰下げ / 遺族年金
> - **② 給付金・取り逃し**: 支援給付金 / 定期便に載らない年金 / 通知書 / 詐欺
> - **③ 税・社会保険料** (an toàn YMYL nhất): 任意継続vs国保 / 介護保険料 / 退職金の税 / 住民税非課税
> **⛔ CẮT hẳn:** 不動産 (bán nhà/リバースモーゲージ) · 金融商品 (mua bảo hiểm/投資/iDeCo/NISA) — lệch trụ + đụng YMYL.
> **⛔ 介護 sâu → sang kênh `kaigo` (「親の介護とお金ノート」, ĐÃ MỞ 2026-07-25):** nenkin CHỈ giữ **介護保険料 của chính người xem** (slot #11). Mọi thứ thuộc tiền CỦA BỐ MẸ — 高額介護サービス費 / 負担限度額認定証 / 世帯分離 / 施設費用 / 認知症→資産凍結 / 家族信託 / 成年後見 / 寄与分 — là của `kaigo`. Test: "người xem đang tính tiền CHO AI?" → cho mình = nenkin, cho bố mẹ = kaigo. Xem `Projects/youtube-jp-kaigo/CLAUDE.md`.
> **⛔ KHÔNG KHÔ KHAN:** mỗi video BẮT BUỘC = 1 con số đắt + 1 nhân vật モニター + 1 hook 決断/損; "giải thích chế độ chay" ≤45s. (Xem đầu 02_CONTENT_PLAN.)

## Viết kịch bản

- **Dùng skill `script-nenkin`** (`E:\Claude\.claude\skills\script-nenkin\SKILL.md`, đúc 2026-07-25 từ CLAUDE.md này + bài học scripts 01–05) — quy trình 7 giai đoạn: GĐ0 lọc trụ + **FACT SHEET FIRST** (verify nguồn TRƯỚC khi viết) + đo trend → sổ xoay khuôn → cast モニター + dàn ý case-driven → cold open loss-aversion → viết trong 6 luật YMYL → retention audit + TTS → đóng gói CTR + compliance.
- 🔴 **GATE NHỊP GIỮ CHÂN — `python tools/check_pace.py <stem>` (thêm 2026-08-12, chạy TRƯỚC render).**
  Đo 5 mốc từ `_TTS.md`: hết cold open **≤1:15** · nhân vật đầu tiên **≤2:00** · số con SỐ trong 30s
  đầu **≤8** · cửa sổ 45s dày SỐ nhất **≤20** · CTA **42–58%** video.
  **Vì sao cần:** skill GĐ2 đã ghi *"case + số của nhân vật vào trước phút 2"* từ lâu, mà script 12 vẫn
  để nhân vật vào ở **2:39** và không ai bắt được — vì mốc đó **chưa bao giờ được ĐO**, chỉ ước bằng mắt
  lúc đọc dàn ý. Ngưỡng đúc từ phản hồi khán giả về **video 10** (mào đầu 1:19 · **24 con số/45s** ở phút 6).
  ⚠️ Mục *"khối số không nên nằm trong 3 phút đầu"* **chỉ CẢNH BÁO** — giả thuyết chưa có bằng chứng,
  và nó đánh nhau với việc kéo nhân vật vào sớm. Cái CÓ bằng chứng là **mật độ**, không phải vị trí.
- Khi skill và file khác mâu thuẫn: hồ sơ モニター + chuẩn visual lấy ở CLAUDE.md này (nguồn sự thật); quy trình viết lấy ở skill.
- Ghi chú gốc còn giá trị: tiền LUÔN là 円 ([[feedback_jp_script_yen_only]]) · cold open loss-aversion là luật user chốt 2026-07-20 ([[feedback_mo_dau_danh_vao_noi_so]]) · visual ~50%+ slide animation (make_motion CLIPS).

## 🎬🎬 VISUAL — ĐẢO SANG "SÂN KHẤU CỐ ĐỊNH" (user chốt 2026-08-09, ĐÈ toàn bộ mục VISUAL cũ bên dưới)

> **Căn cứ:** `CHANNEL_BENCHMARK_okane-hokenshitsu_2026-08-08.md` §2.3 — đo storyboard 175 frame
> video 152.452 view của kênh **cùng ngách, lập trước mình 6 ngày**: cả 29 phút chỉ có **ĐÚNG
> MỘT bố cục**. Kênh mình đang là slideshow trộn 4 loại asset → mỗi slide trông như của một
> kênh khác. Bộ asset + tool: `04_CAST_STAGE_PROMPTS.md`, demo duyệt: `06_VIDEO/_stage_demo/`.

**Khuôn khoá:** 2 nhân vật đứng cố định hai mép (案内役 trái · 聞き手 phải) · giữa là MỘT tấm
bảng đổi nội dung · đáy là dải đen phụ đề 1 dòng. Khung **KHÔNG pan, KHÔNG zoom**;
cái động duy nhất là **phần tử hiện dần theo lời đọc** (build-on), xong thì đứng im.

### 🎨 BẢNG MÀU SÂN KHẤU — nền NAVY đậm + card KEM (user chốt 2026-08-10, phương án D)

User: *"tao nhìn nền trắng nó không được thu hút lắm"*. Đã dựng 4 biến thể cùng một thẻ để chọn
bằng mắt (A trắng/xám-xanh hiện tại · B kem/be · C trắng/navy · D kem/navy) → **chốt D**.

| khoá `channels.py` | giá trị | vai |
|---|---|---|
| `stage_card` | `(255, 250, 238)` | card kem |
| `stage_bg_top` | `(32, 50, 84)` | nền navy trên |
| `stage_bg_bot` | `(16, 26, 48)` | nền navy dưới |

- **Thi hành:** `make_stage.py slides ... --channel nenkin` (cờ mới, thêm 2026-08-10). Thiếu cờ
  thì tool dùng mặc định trắng/xám-xanh → **hai kênh trong một video**. Cả `run_stage.cmd` của
  video và `_demo10/run_all.cmd` đã mang cờ này.
- ⛔ **Đừng sửa hằng số `CARDC`/`BG_TOP`/`BG_BOT` trong `make_stage.py`** — tool dùng chung mọi kênh.
- 🔴 **Lý do chọn kem (là số, không phải thẩm mỹ):** 12 ảnh minh hoạ AI của video 10 đều **nền kem**;
  card trắng làm lộ rõ mép vuông của ảnh, card kem thì ảnh hoà vào bảng. Bản C (card trắng + nền
  navy) đẹp nhưng vẫn lộ mép.
- ⚠️ **Đây là LỆCH khỏi phép đo.** Nền trắng-trên-sáng đến từ 175 frame video 152K của
  `お金の保健室` (`CHANNEL_BENCHMARK_okane-hokenshitsu_2026-08-08.md` §2.3). Đổi sang navy là đặt
  cược vào thẩm mỹ thay cho phép đo đó — đánh đổi đã biết, không phải bỏ sót. Nếu retention giữa
  bài tụt so với video 01–09 thì đây là một trong các biến phải xét lại.
- ⚠️ **Bảng màu nằm trong `.sig`** nên đổi màu ⇒ **dựng lại toàn bộ 73 thẻ** (~30 phút). Đổi màu
  TRƯỚC khi render video, đừng đổi sau.

- **Tool:** `E:\Claude\Projects\_media_library\make_stage.py` — layout `check · flow ·
  compare · timeline · source · big · bars · art/photo · steps · tree · **zu**`.
  Entry SLIDES: `{"match": "...", "video": true, "stage": {...}}`.

### ⭐⭐ `zu` — LỚP SƠ ĐỒ, CHỦ LỰC TỪ VIDEO 13 (user chốt 2026-08-17)

> user dán 3 frame của kênh cùng ngách (「消えるのは自分の道」・「今日は計算をしません」・「役所の窓口」):
> *"tao muốn sinh ra các hình như này chứ không thuần text nhé"*.

**Vấn đề của 10 layout cũ:** tất cả đều là **BẢNG** (hàng/cột/hộp xếp thẳng) — chữ là nội dung,
icon chỉ trang trí đầu dòng. Cái đối thủ làm là **SƠ ĐỒ**: vài vật đặt tự do, nối bằng mũi tên,
một bong bóng thoại, một dấu ✗ to. Người xem **hiểu bằng HÌNH** rồi mới đọc chữ.

**Cú pháp:** `{"layout":"zu", "title":…, "nodes":[…], "edges":[…]}`
- `nodes[]`: `{id, kind, at:[fx,fy], icon, label, s, lw, tone, …}` — `at` là **toạ độ PHÂN SỐ 0..1**
  của hộp sơ đồ (tool tự quy ra pixel; đổi khung là cả sơ đồ tự co theo).
  `kind` = `circle` (icon trong vòng) · `mark` (✓/✗ to) · `panel` (hộp có băng navy trên đầu) ·
  `label` (hộp chữ bo góc, `hero:true` = cỡ chữ 92px, `under:true` = gạch chân vàng) ·
  `bubble` (bong bóng thoại, `tail` = down/up/left/right) · `icon` (vật trần).
  Cờ thêm: `cross` (dấu ✗ to đè lên vật) · `spark` (3 tia vàng) · `dash` (viền nét đứt) · `dim` (xám).
- `edges[]`: `{from, to, style, tone, label}` — `style` = `arrow` (khối vàng) · `line` (mảnh, navy) ·
  `dot` (nét chấm = "không tự động/không áp dụng") · `elbow` (dọc rồi ngang, để rẽ nhánh) ·
  `fan` (dải nhạt toả ra). Edge **tự hiện SAU cả hai đầu**, không phải khai mốc thời gian.

🔴 **BA THỨ TOOL TỰ LO — ĐỪNG CHỈNH TAY:**
1. **Kẹp vị trí** (`_zu_place`): `at` là TÂM node, nên hộp to tự tràn vào nhân vật. Tool kẹp vào
   vùng an toàn — đo bằng máy trên cả bộ cast: trái `sensei_*` chạm **x=528**, phải hẹp nhất
   `tanaka_*` bắt đầu **x=1525**. Không kẹp thì gate báo **25 lỗi trên 52 thẻ**.
2. **Cắt mũi tên theo KÍCH THƯỚC THẬT** của node (`_zu_extent`), không theo hằng số.
3. **Nhãn tự lật lên trên** nếu tràn đáy card (`_zu_label`).

🔴 **GATE `zu_check()` — GỌI HÀM CỦA TOOL, ĐỪNG CHÉP CÔNG THỨC.** Nó bắt: node rộng/cao hơn vùng
an toàn · **hai node CHỒNG NHAU** (đo giao 2 hộp BẤT ĐỐI XỨNG — nhãn nằm hẳn ở dưới) · edge trỏ
tới node không tồn tại. ⚠️ Hộp bao phải gồm **NHÃN**: bản đầu chỉ đo VẬT ⇒ thẻ 02 video 13 ra
「ご主人／奧さ…／9万円」 **chồng chữ**, chỉ lộ khi soi frame.

### ⭐ ĐỢT 2 (2026-08-17) — 6 kind nữa + `zu_row`, sau khi user dán thêm 4 frame mẫu

> user: *"đây tao muốn có nhiều hình ảnh minh họa như này và nó có chuyển động nhé"*
> (4 frame: 「あとから戻る」・「74歳まで必ずどれかに加入」・「期限は1つ…3つ」・「5日＝扶養の届出」)

Ba thứ đợt 1 còn thiếu, giờ đã có:

| kind | là gì | khoá |
|---|---|---|
| **`group`** ⭐ | **HỘP LỚN nhóm nội dung**: viền + tiêu đề trên + icon TO giữa + dòng chốt dưới. Có `hero` = số trong **đĩa vàng** (「7〜8割」) | `w` `h` `head` `icon` `iconsize` `hero` `foot` `under` `tone` |
| **`banner`** ⭐ | **DẢI ĐÁY** full-width, nền vàng nhạt (hoặc trắng viền navy), icon nhỏ + câu chốt **gạch chân vàng** | `w` `icon` `label` `tone` `under` |
| **`ribbon`** | **CỜ ĐUÔI NHEO vàng** cho câu hero trên đầu | `label` `lw` |
| **`chip`** | nhãn nhỏ nền vàng ở góc (「5日以内」) + `spark` | `label` `lw` |
| **`oval`** | ellipse DỌC (cột lựa chọn) — dùng với `num` | `icon` `label` `num` `tone` |
| **`bigicon`** | vật TO không khung (đồng hồ cát, ví + hoá đơn) | `icon` `size` |

Thêm ở **edge**: `style: "arc"` (**vòng xuống dưới rồi quay lên** = "lối SAI") + cờ **`x: true`**
(dấu **✗ ĐỎ to** vắt qua giữa đường). `drop` = độ sâu vòng. Đi thẳng thì đường chồng lên chính
hàng node và ✗ đè lên một node — đó là lý do phải vòng dưới.
Thêm ở **node**: `num: N` = badge số ❶❷❸ ở góc trên-trái.

🔴 **`zu_row(items, y, x0, x1, wide, mingap)` — DÙNG NÓ, ĐỪNG GÕ `at[0]` TAY CHO MỘT HÀNG.**
Nó đo `_zu_extent` từng node rồi chia khe thành gap BẰNG NHAU, và **tự thu nhỏ** nếu không đủ chỗ.
- `mingap` **phải ≥96** khi hàng có **mũi tên nối liền** (`_zu_trim` chừa 18px mỗi đầu ⇒ khe thật
  = mingap − 36; dưới 60px là mũi tên teo thành dấu chấm). Hàng chỉ nhận mũi tên **DỌC** từ trên
  (ribbon → oval) thì `mingap=30` là đủ.
- Muốn một nhóm sát nhau cạnh một hộp lớn thì **gọi `zu_row` HAI LẦN** với `x0/x1` khác nhau,
  đừng hạ `mingap` chung (mẫu: `one_to_n()`).
- `wide=True` = hàng nằm **trên đỉnh nhân vật** ⇒ dùng trọn bề ngang card.
📌 `_zu_place` cũng tự chuyển sang biên CARD (rộng hơn) cho node nằm **trọn trên y=368** — đó là
lý do `ribbon`/`chip` rộng gần hết khung mà không chạm ai.

🎬 **CHUYỂN ĐỘNG đã có sẵn (build-on), nhưng chỉ thấy được ở MP4.** Vòng duyệt bằng `--still` chỉ
ra PNG **frame cuối** ⇒ trông như slide tĩnh. Đo thật trên `m2.mp4` (9s): 0,6s ribbon hiện dần →
1,8s mũi tên vàng **vẽ dần** + oval ①② → 3,2s đủ 3 nhánh + hộp 75歳 → **đứng im** từ 4,5s.
⇒ Muốn user duyệt chuyển động thì render **1–2 clip mp4** (`make_stage.py clip … --sec 9`), đừng
đưa PNG rồi nói "có chuyển động".

📌 **4 khuôn tái dùng đã đúc trong `build_slides_13.py`:** `two_ways()` (2 hộp lớn + banner chốt) ·
`one_to_n()` (1 hộp navy → N hộp amber + banner) · `chain()` (chuỗi ngang + lối sai ✗ đỏ + chip) ·
cộng `spine()`/`slots()` của đợt 1. Video sau **copy 4 hàm này**, đừng dựng lại từ node thô.

### 🔴 ĐỢT 3 (2026-08-17) — 4 LỖI HÌNH USER BẮT ĐƯỢC, sửa ở TẦNG TOOL

> user: *"các ảnh bị cắt mất 1 phần rồi… cho cái text ở dưới cao lên cho nó cân đối hình…
> hình mũi tên méo kìa… mũi tên lỗi"*. Cả 4 đều là **lỗi hệ thống**, không phải lỗi lẻ từng thẻ.

| # | Lỗi | Gốc bệnh | Sửa |
|---|---|---|---|
| ① | **Icon bị cắt mất một phần** (couple_senior mất vai + chân bàn · wallet_open mất đáy · passbook_open mất mép · yen_coins mất cọc) | `ingest_stage_icons.py` "cắt 12% mép phải+đáy để bỏ ✦" rồi "crop vuông ở GIỮA" — **cả hai giả định vật nằm giữa khung**, mà model đặt vật lệch TRÊN-TRÁI (đo được: vật chạy tới x=1046, y=690; hai bước cắt chỉ giữ x 267–942, y 0–675) | **KHÔNG cắt khung nữa.** Tách nền trước → ✦ thành một **đảo rời** → xoá blob (≤1,5% thành phần lớn nhất **VÀ** tâm ngoài 78% khung) → trim + **pad** thành vuông |
| ② | **Chữ dính đáy, hình lơ lửng giữa, hở một dải trống** | `at[1]` đặt TAY từng thẻ ⇒ mỗi thẻ hụt một kiểu | `polish()` thêm bước **CÂN ĐỐI DỌC theo hệ LƯỚI**: chia vùng (dưới tiêu đề → đỉnh banner) thành n dải bằng nhau, mỗi hàng vào TÂM dải. Áp cho 12 thẻ |
| ③ | **Mũi tên "méo"** — dài 260px mà thân 15px = cây kim, đầu mũi như cái chóp dính vào | `arrow()` cố định `w=15` cho MỌI độ dài | `w=None` mặc định → **tự cân theo chiều dài** (`L×0,10`, kẹp 14–30), đầu mũi `w×2,2` (cap `L×0,42`) |
| ④ | **Mũi tên khuỷu lỗi** | `elbow` lấy điểm đầu từ `_zu_trim` (cắt theo hướng **CHÉO** a→b) ⇒ mọc ra từ một góc chứ không từ giữa đáy hộp; rồi kết bằng mũi **NGANG** vào mép hông ⇒ **trùng đường với mũi tên khác cùng hàng** | **3 ĐOẠN: dọc → ngang → mũi chỉ XUỐNG vào đỉnh b** (đúng khuôn mẫu của đối thủ). Đáy của a lấy từ `_zu_box` (**có nhãn**), không `_zu_extent` — nếu không đoạn ngang cắt qua chữ 「2回目」 |

**Hai gate máy thêm cùng lượt** (`zu_check`): ⓐ mũi tên `arrow`/`line` có khe thật <60px → *"teo thành dấu chấm"* ⓑ `elbow` có khe DỌC (đã trừ nhãn hai đầu) <54px → *"đoạn ngang đè lên nhãn"*.
📌 **Bài học quy trình:** cả 4 lỗi này tao đã duyệt qua **contact sheet thu nhỏ 880×495** và cho qua. Luật §2.10 ⑥ của `media-library.md` (*"nghiệm thu phải soi 1:1, sheet thu nhỏ CHO QUA"*) áp y nguyên cho **thẻ sân khấu**, không chỉ cho ảnh AI.

### 🔴 ĐỢT 4 (2026-08-17) — CHỐNG **LỌT** (thẻ trống trên đầu) + đồ trang trí mồ côi

> user: *"sao lại có cái ảnh riêng lẻ ở góc trái thế"* (thẻ 04) · *"những ảnh kiểu này trình bày kiểu
> khác đi. Khoảng trống trên đầu thì nhiều mà lại cho text xuống dưới thế"* (thẻ 05).

🔴 **Bệnh gốc, và nó là một bệnh của TOÀN BỘ tầng `zu`:** tool có **ba** cơ chế chống **TRÀN**
(`_zu_place` kẹp · `_zu_box` bất đối xứng · `zu_check` báo chồng) mà **KHÔNG có một cơ chế nào chống
LỌT**. Gate báo 0 lỗi trong khi thẻ 05 dùng hết **47%** chiều cao band, phần trống dồn hết lên đầu,
và icon vẫn ở cỡ mặc định dù còn thừa chỗ ngang. **Lọt không phải lỗi hình học, nên gate hình học
không bao giờ thấy.** Đồ trang trí mồ côi chính là *triệu chứng*: tao lấy icon lấp chỗ trống thay vì
chữa chỗ trống.

| # | Sửa | Ở đâu |
|---|---|---|
| ① | **`zu_fit()`** — phóng to nội dung tới khi lấp ~86% band **+** chia đều khe dọc, hàng đầu bắt đầu ngay dưới tiêu đề. Chạy trước `_zu_place`, gọi từ **cả** `L_zu` và `zu_check` (idempotent qua cờ `_fit`) | `make_stage.py` |
| ② | **Tự LÙI cỡ**: thử k từ to xuống, lấy bản to nhất mà `_zu_geom` sạch; nến chót = đúng bản tác giả ⇒ `zu_fit` **không bao giờ làm xấu đi** | `make_stage.py` |
| ③ | **Gate đồ trang trí mồ côi**: icon không nhãn + không edge + một mình một hàng ⇒ 🔴. Đã bỏ 6 node, cho nhãn 2 node (thẻ 10 `大阪のお宅`, thẻ 11 `ご主人`) | `zu_check` |
| ④ | **`cols3()`** — 3 HỘP DỌC thay 3 vòng tròn: cùng 3 vật, lấp **45% → ~84%** band. Áp cho 4 thẻ (05·26·32·75) | `build_slides_13.py` |
| ⑤ | Lề đáy khi kẹp **12 → 26px**; `foot` của `group` đọc được **2 dòng**; elbow chia **30/70** thay 50/50 | `make_stage.py` |

📌 **Ba bài học đắt hơn cả bản vá:**
1. 🔴 **Phóng to mà không chia lại bề ngang = tự sinh lỗi mới.** Vòng đầu ra **21 lỗi** (khe mũi tên
   teo 24–48px) vì `zu_row` đã chia `at[0]` theo bề rộng ở cỡ CŨ. ⇒ Phải tách `_zu_geom` ra để bước
   phóng **đo bằng đúng phép đo của gate**, và thêm `_zu_respread`.
2. 🔴 **Cờ `fix` của builder là hợp đồng, đọc nó trước khi tự xếp lại.** Bản đầu bỏ qua `fix` ⇒ xếp
   4 hàng của thẻ hội tụ thành 4 tầng đều nhau, khe chéo teo còn 38px. Cờ đã có sẵn từ `polish()`.
3. 🔴 **Sửa ở tầng SAI thì số không đổi mà rất dễ tưởng "vá chưa ăn".** Siết lề đáy trong `zu_fit`
   **hai lần** đều vô hiệu, vì thứ quyết định là **kẹp trong `_zu_place`** (12px). Và lần đó tao còn
   gộp `span` (thang đổi `at[1]`↔pixel, phải TRÙNG `by1` của `_zu_place`) với `bot` (lề xếp hàng)
   thành một hằng số ⇒ toạ độ bị co dãn 14px. **Hai đại lượng khác vai thì đừng gộp.**

⚠️ Sau đợt này `VERSION = stage-1.1` ⇒ **mọi `.sig` hết hạn, 80 thẻ dựng lại** (đúng ý, vì hình đổi).

### 🔴 ĐỢT 5–6 (2026-08-17/18) — 13 GATE BỐ CỤC, ĐÃ TÁCH THÀNH RULE TOÀN HỆ THỐNG

> ⭐ **Luật đầy đủ: `.claude/rules/stage-zu-layout.md`.** Đọc file đó trước khi sửa bố cục thẻ `zu`.
> Mục này chỉ giữ **lịch sử** của kênh nenkin để tra; đừng chép luật ra đây (hai bản là lệch nhau).

**Chuyện đã xảy ra:** user chỉ lỗi bằng mắt **6 lượt liên tiếp** trên 80 thẻ của video 13 — mỗi lượt
ra một **LỚP** lỗi mới, không phải một thẻ. Tổng cộng **13 lớp**, và tao đã duyệt qua contact sheet
880×495 rồi cho qua **tất cả**.

| lượt | user nói | lớp lỗi tìm ra |
|---|---|---|
| 1 | *"ảnh riêng lẻ ở góc trái"* · *"khoảng trống trên đầu nhiều mà text xuống dưới"* | ① đồ trang trí mồ côi · ② lọt dọc → sinh `zu_fit` |
| 2 | *"text dưới căn giữa chứ, cách khung 10cm"* · *"không sắp xếp cho cân được à"* | ④ lề đáy · dải đáy căn giữa · đổi HÌNH (`cols3`, phép cộng) |
| 3 | *"2 mũi tên dài bằng nhau"* · *"khung text góc phải cho thấp xuống"* | ⑥⑦ mũi tên lép/lệch · ⑤ trần trên · khoá `bw` |
| 4 | *"còn rất nhiều ảnh lỗi"* | ③ phủ ngang → sinh `_zu_widen` · ⑩ đích cuối phải to nhất |
| 5 | *"vẫn lỗi vị trí mà"* | ⑪ mũi tên đơn phải thẳng · ⑫ đuôi bong bóng phải chạm · ⑬ node lơ lửng |
| 6 | *"ảnh này vẫn lỗi này"* (thẻ 53) | ⑪ bỏ sót `dot` — đường nét đứt cũng là liên kết đơn |

**Đã sửa trên 80 thẻ:** 13 thẻ thêm khối chốt đáy · 7 thẻ đổi bố cục (hợp lưu đối xứng 02/03/13 ·
mũi tên đơn thẳng 18 · `10年間` thành nhãn edge 44 · dòng tuyên bố xuống đáy 77 · 3 hộp dọc
05/26/32/75) · 6 thẻ đích cuối thành `hero` · 6 thẻ bỏ icon trang trí · 4 thẻ lưới 2×2 khoá `bw` ·
thẻ 53 điện thoại thành `bigicon` 300px.

**Kết quả đo:** `check_zu_layout.py` → ✅ SẠCH 13/13 lớp trên 55 thẻ `zu` · mực sát mép SẠCH 80/80.
`make_stage.py` ở **`stage-1.2`** (mọi `.sig` hết hạn).

### 🗂️ KHO ICON DÙNG CHUNG (user chốt 2026-08-17)

> *"những ảnh nào tái sử dụng được thì bỏ ra khu vực dùng chung để tái sử dụng cho video sau nhé"*

`make_stage.py::icon_path()` tìm theo thứ tự: **`<kênh>/assets/icons/` → `_media_library/stage_icons/`**.
Kho chung đã có **28 icon khái niệm** (bank · calc · calendar · clock · cityhall · docs · env ·
hospital · house · money_pouch · passbook · scale · wallet · warning …). Luật ranh giới + cách thêm
icon: **`Projects/_media_library/stage_icons/stage_icons.md`**.

⚖️ **KHÔNG phá `media-library.md` §2** (*"không tái dùng asset"*): rule đó nói về **b-roll STOCK tải
từ mạng** — lặp cảnh thật giữa các video là inauthentic content. Icon khái niệm thì ngược lại, nó là
**bộ nhận diện**, lặp lại là điều TỐT. Ranh giới: vật trung tính không số/không chữ/không gắn năm ⇒
kho chung · **原典ショット + ảnh cảnh thật + ảnh có con số của bài** ⇒ ở lại folder video.
⛔ `avatar_*` là dàn モニター **riêng kênh**, không đưa ra kho chung.

📌 **Mẫu dùng thật:** `tools/build_slides_13.py` — 79 thẻ, **54 thẻ `zu` (68%)**, có 2 khuôn tái dùng
được cho video sau: hàm `spine()` (số CŨ→MỚI, dùng 4 lần làm trục hình) và `slots()` (4 ô đếm
"đang ở lần viết lại thứ mấy", **lưới 2×2 chứ không phải 1 hàng** — 1 hàng 4 ô thì font tụt về 30px).
📌 Builder của video 13 còn **đổi gate nhịp sang đo bằng GIÂY**, không dùng số dòng làm proxy như
`build_slides_11.py` (2 dòng NGẮN vẫn <6s — đo thật cặp dòng 9→10 chỉ **3,9 giây** mà gate cũ cho qua).
- **Quy trình:** `python make_stage.py slides <clips_dir> --slides <SLIDES.json>` → xuất
  `clips/clip_XX.mp4` + `_stage_sheet.jpg` (**duyệt mắt trước khi render**) → rồi
  `video_render.py ... --channel nenkin` như thường. **Không phải mổ renderer.**
- **Phụ đề (user chốt 2026-08-19, duyệt video 14):** `outline` + **`sub_marginv: 12`** — chữ nằm **TRONG DẢI ĐEN y928–1080 của sân khấu, DƯỚI 2 nhân vật**, không cưỡi lên mép card kem. Cả hai khoá nằm trong hồ sơ `channels.py` (máy tự ăn, không phải gõ cờ); `maxlen` tự siết 26 = luôn 1 dòng trong dải. ⛔ Dòng cũ `--sub-style bar` hết hiệu lực từ 2026-08-10 (toàn hệ thống outline, `audience-45plus.md` §3.1).
- 🔴 **GATE MÁY BẮT BUỘC — tool sinh SLIDES, không viết JSON tay** (chốt 2026-08-12, sau khi user soi
  frame bắt 10 chỗ tràn + 2 lỗi bố cục). Mẫu: **`tools/build_slides_11.py`** — nó chặn **10 mục** trước
  khi ghi file: `match` khớp đúng 1 dòng · index tăng dần · **khoảng cách ≥2 dòng** (cách 1 dòng = entry
  <6s) · mật độ ≤6 đổi hình/phút · số HÀNG theo layout (compare **3**, check 6, steps/flow/timeline 5) ·
  **trần ký tự/dòng** (check 24 · compare 32 · steps 22 · source 23 · timeline hộp `880/n−52`÷26) ·
  **label timeline** `len×40 ≤ 880×prog` (font 40 CỐ ĐỊNH, không fit) · **`steps` cấm ký tự xuống dòng**
  (vẽ bằng `tw()` một dòng). Bảng trần đầy đủ: `.claude/rules/audience-45plus.md` §2.1.
  ⚠️ Viết tay thì 13 lỗi loại này chỉ lộ khi render gãy ở phút thứ 2, hoặc **không lộ gì cả**.
- 🔴 **ẢNH: dùng `bgimg` (nền), KHÔNG dùng `fill`** — hộp `fill` (1010–1400 × 536–852) **trùng vùng chữ**
  của `check`/`steps` ⇒ đè lên chữ. `fill` chỉ an toàn ở `big`/`art`. Khuôn viết prompt ảnh (tỉ lệ từng
  slot · luật "chừa 15% bên phải" · watermark cắt-không-vá · model nghe VỊ TRÍ không nghe TỈ LỆ):
  **`06_VIDEO/11_taishokukin-shinkokusho-junban-408man/art_prompts_SPEC.md`** + `.claude/rules/media-library.md` §2.10.
- ⚠️ **Dòng liệt kê TRUNG TÍNH phải để `ok`, đừng để `no`** — `no` render chữ **xám** `(168,174,184)`;
  thẻ toàn `no` thì vừa trống vừa nhạt (đo được 8 thẻ ở 0,2–0,4% phủ mực). `no` chỉ dành cho điều SAI.
- ⚠️ **Avatar nhân vật = PNG trong `assets/icons/`**, gọi bằng `"icon": "avatar_matsumoto"` — `icon()`
  nạp theo TÊN nên **không phải sửa tool**. Ảnh nguồn phải để đầu trong **55% bên trái** (ô vuông cắt từ
  `x=0`), và phải đọc được ở **132px**.
- ⭐ **BỘ 15 AVATAR (đủ roster, dựng 2026-08-14)** — tool `tools/make_avatar_icons.py`, cắt từ
  `assets/cast/` rồi ghép vào khuôn tròn của kênh (R=156 · nền 243,232,210 · vành navy 11px).
  Chạy 1 lệnh là dựng lại hết + xuất `assets/icons/_avatar_sheet.png` (có hàng **132px = cỡ thật**).
  · モニター: `avatar_tanaka` `avatar_takahashi` `avatar_sato` `avatar_watanabe` `avatar_ito`
    `avatar_yamada` `avatar_matsumoto` `avatar_suzuki` `avatar_suzuki_exec`
  · vai trò: `avatar_kenkyuin` `avatar_sensei` `avatar_kikite`
  · ○×/thế hệ: `avatar_maru` `avatar_batsu` `avatar_seniors`
- 🔴 **ĐẶT AVATAR Ở ĐÂU — đo bằng máy, đừng đoán:**
  · `compare` → `panels[].icon` = **132px** ✅ **chỗ duy nhất avatar dùng tử tế** (nhận ra mặt ngay)
  · `check`/`steps` → cột icon = **56px** 🟡 chỉ còn là "gợi ý có người", không phải chân dung
  · `big`/`art` → khoá `fill` (390×316) ⛔ **KHÔNG DÙNG ĐƯỢC**: `fill` **đè lên `cap`/`note`** của
    `L_big`, **và** `fill_art()` mở ảnh bằng `.convert("RGB")` ⇒ 4 góc trong suốt của PNG thành **ĐEN**.
  ⇒ Muốn モニター hiện MẶT TO thì **giới thiệu bằng `compare`** (avatar | icon tiền + 2–3 dòng fact),
  đừng dùng `check`. Mẫu: `tools/build_slides_12.py` thẻ [07] [25] [41] và thẻ trả vòng [59].
- ⚠️ **HAI HỌ VẼ, đừng để cạnh nhau trong CÙNG một thẻ:** `avatar_matsumoto` · `avatar_suzuki` ·
  `avatar_watanabe` · `avatar_sensei` · `avatar_kikite` thuộc họ vẽ **CHI TIẾT/đổ bóng**; còn
  `tanaka` · `takahashi` · `sato` · `ito` · `yamada` · `kenkyuin` · `maru/batsu` là họ **いらすとや PHẲNG**.
- 🔴 **Ảnh cast có NỀN ĐỤC** (vd `ito_cafe` có kệ chai) phải crop **ô VUÔNG quanh mặt** + `wf≈1.03`
  + `top 0.00` để phủ kín vòng tròn; làm như ảnh nền trong suốt (`wf 0.66–0.72`) thì thấy rõ **mép
  chữ nhật** của khối crop nằm trong vòng tròn. Và **tâm mặt phải đo bằng MÁY** (quét màu da
  `r>245 · 185<g<225 · 145<b<185` rồi lấy trọng tâm) — đọc lưới bằng mắt đã sai **93px** ở ảnh này.
- **Cast:** `sensei_*` 8 tư thế · `kikite_*` 8 · `josei_*` 8 (`assets/cast/`). Icon: 28 file
  `assets/icons/`. Biểu cảm phải khớp nhịp truyện (lo → hiểu → yên tâm).
- ⚠️ **Ảnh gen LẺ phải đo lại tỉ lệ đầu** rồi thêm vào `CAST_SCALE_FILE` — xem
  `04_CAST_STAGE_PROMPTS.md` §7.1b.
- ⛔ **Entry `stage` thì ĐỪNG gắn `"rank"`** — badge 「その1」 của renderer dán đè góc trên
  trái sân khấu, nhìn như miếng vá. Số mục thuộc về TIÊU ĐỀ của tấm bảng.
- ✅ **Đã chạy thử trọn dây chuyền 2026-08-09** (`06_VIDEO/_smoke/`): stage clips →
  `video_render --channel nenkin` → mp4 20,7s, EXITCODE=0, phụ đề nằm đúng trong dải đen.

🔴 **CÁI MẤT, ghi thẳng:** tỉ lệ cũ (cast 35–40% / diagram 35% / **ảnh thật 15%** / card 10%)
**BỎ — ảnh thật về 0%**. Nghĩa là kênh này thôi dùng `fetch_photos`, thôi duyệt contact sheet
ảnh, thôi lo license ảnh. Đổi lại **mất hẳn kết cấu ảnh thật** — mọi khung là đồ hoạ vẽ, nhìn
lâu dễ đơn điệu hơn. Đánh đổi đã biết trước; nếu 5–7 video mà retention giữa bài tụt so với
video 01–07 thì mở lại 1–2 entry ảnh thật cho beat cảm xúc, đừng đảo cả khuôn.
📌 Lớp `drawn` (研究ノート · case tính tiền · よくある誤解) **giữ nguyên**, không mâu thuẫn:
nó là nội dung TRONG tấm bảng, không phải bố cục khung.

<details><summary>(LƯU TRỮ) Chuẩn VISUAL cũ — slideshow 4 loại asset, chốt 2026-07-19 / sửa 2026-07-22</summary>

## 🎬 Chuẩn VISUAL kênh (chốt 2026-07-19; **SỬA 2026-07-22 — user: "kể chuyện kèm hình, NHIỀU ẢNH NHÂN VẬT, không nhìn toàn chữ"**)

- **Tỷ lệ MỚI (áp từ video 03):** cảnh NHÂN VẬT モニター ~35–40% (mọi khối case đều thấy NGƯỜI) · diagram số ~35% (câu chốt số vẫn thấy SỐ) · ảnh thật bối cảnh ~15% · card chữ ~10%. Video 01–02 (41/45 slide là chữ+sơ đồ) là phản ví dụ — đã đăng, không sửa.
- **🧑‍🤝‍🧑 LỚP CAST いらすとや (0 đồng, user chốt 2026-07-22):** bộ ảnh nhân vật cố định `assets/cast/` (25 file: 田中さん **8 biểu cảm nhất quán** smile/laugh/angry/cry/idea/shock/surprise/think · 佐藤さん 4 biểu cảm · 鈴木 exec/shock/年金手帳 · 高橋 laptop ×2 · 山田夫妻 · 伊藤 cafe · 研究員 ×2 · quiz ○× MC · đạo cụ 通帳 + nhóm senior đi làm). Tải/thêm nhân vật: `tools/fetch_irasutoya.py` (scraper: title-match qua search + ảnh lấy từ **Blogger JSON feed** `feeds/posts/default?alt=json&path=...` — trang thường render client-side, đừng parse HTML thô; né ảnh 1px tracker <10KB).
- **SLIDES entry cast:** `{"match":"...", "photo":true, "cast":"tanaka_shock", "label":"(tùy chọn)"}` → chạy `python tools/make_cast_slides.py <SLIDES.json> <slides_img>` **TRƯỚC fetch_photos** — tool vẽ slide nền giấy lab + nhân vật + name-tag navy (label mặc định theo hồ sơ モニター), lưu đúng `slide_XX.png` theo index; video_render dùng như ảnh thường. Biểu cảm phải KHỚP nhịp truyện (lo→hiểu→yên tâm).
- **⚠️ LICENSE いらすとや: ≤20 ảnh/video** — make_cast_slides tự đếm và cảnh báo khi vượt. Credit 概要欄 thêm dòng: `イラスト:いらすとや`. Sau này có kinh phí → thay bộ AI illustration riêng cùng tên file trong `assets/cast/`, toàn pipeline giữ nguyên. (Folder `assets/irasutoya/` cũ — 6 file 1-pose thời video 01, dùng bởi make_motion skin warm — GIỮ cho tương thích; bộ chuẩn từ video 03 là `assets/cast/`.)
- Tỷ lệ CŨ (tham khảo): diagram 60–70% / ảnh 25% / card 10%.
- **SLIDE MỞ MÀN (user chốt 2026-07-20): BẮT BUỘC là ảnh thật đẹp/cinematic + chữ hook vàng viền tối đè lên** (scene `a_hook_photo` trong make_motion — ảnh cover-crop, phủ tối vùng chữ, chữ phóng to có stroke). Ảnh chọn theo cảm xúc của hook (giải phóng/hy vọng/lo lắng), lấy qua kho media, silhouette/vùng tối để chữ nổi. Frame đầu video = ấn tượng hover-preview. Mẫu: video 01 (bình minh dang tay).
- **⭐ 原典スライド — MÓC NHẬN DIỆN SỐ 1 (bắt buộc ≥2 slide/video, chốt 2026-07-25):** slide chiếu **ảnh trang tài liệu gốc** (日本年金機構/厚労省/総務省/自治体/協会けんぽ) + **khung khoanh ĐỎ dày quanh con số đang đọc** + nhãn nguồn nhỏ góc dưới (tên cơ quan + 年月時点). Ảnh lưu `06_VIDEO/<slug>/genten/`. Đây là lớp bù cho việc kênh mình KHÔNG có móc uy tín kiểu 元ハロワ職員 (không được bịa tư cách) — và không đối thủ nào trong ngách làm. Shot đầu nên rơi trong **3 phút đầu**. Chỉ chiếu trang cơ quan công (không báo/blog/công ty); giấy tờ mẫu = tự dựng lại, không dùng giấy thật của người thật. Quy trình: skill `script-nenkin` GĐ0d.
- **Bộ màu signature (mọi video):** XANH = an toàn/nhận đủ · ĐỎ = bị cắt/vượt ngưỡng · VÀNG = sát ranh giới. Số đang được voice đọc = to nhất màn hình (khán giả 60+).
- **⭐ LỚP `drawn` — trang sổ tay viết tay, KHÓA BỘ NHẬN DIỆN (user chốt 2026-07-27, phương án B sau khi duyệt 3 mẫu bằng mắt):**
  - **Font `jp-pen` (KleeOne SemiBold, 楷書) + giấy `grid` (方眼ノート) — CỐ ĐỊNH mọi video, KHÔNG đổi.** Lý do: nét dày đọc được ở 120px cho khán giả 60+; 楷書 ra chất "sổ nghiên cứu" đúng persona 研究室; giấy kẻ ô là thứ người Nhật dùng để tính toán. (A = Zen Kurenaido quá mảnh, C = sổ kẻ dòng đánh nhau với dòng gạch của bảng.)
  - Tool: `../youtube-jp-health/tools/make_drawn.py` (luật gốc `.claude/rules/handmade-layer.md` §0.1 + §6). Chạy **TRƯỚC** `make_diagrams.py`/`fetch_photos.py`; entry SLIDES mang key `"drawn": {...}` — `video_render.py` tự render full-bleed.
  - **3 chỗ dùng (thay CARD CHỮ auto, không thay diagram/ảnh cast):** ① **khối case tính thử tiền ~50%** → `layout: "table"` + `"anim": true` (chữ hiện dần, khoanh đỏ dòng đáp án SAU khi viết xong — đúng nhịp giọng 「赤で囲んだところ」) ② **slide 「研究ノート」 tổng kết cuối video** (signature §DNA mục 2 — đây chính là "trang sổ lab" đã chốt, giờ có tool render thật, tĩnh để người xem screenshot) ③ khối 「よくある誤解」 → `{"layout":"checklist","mark":"cross"}` — **bắt buộc `mark: "cross"`**: tick ✓ vào một câu SAI là ngược nghĩa, khối phủ định phải là ✗ đỏ.
  - **Bộ màu ăn qua phần tử thứ 3 của row:** `["合計","40万円","warn"]` → vàng · `"ok"` → xanh · `"bad"` → đỏ; số mang `ok`/`bad` tự phóng to 22% (khớp luật "số voice đang đọc to nhất màn hình").
  - ⚠️ **KHÔNG thay 原典スライド.** ⛔ Gate lớp thủ công ĐÃ BỎ 2026-08-09 (`handmade-layer.md`) — nguồn thật vẫn bắt buộc qua §YMYL, nhưng KHÔNG còn ghi sổ hoãn / bỏ slot / bắt quay. Kênh này KHÔNG còn phải viết tay iPad (`notebook`) nữa.
- 4 mẫu diagram lõi: **thang ngưỡng** (bar vs vạch đỏ) · **card モニター** (avatar + số liệu, cố định xuyên video) · **quiz ○×** (Q rồi đóng dấu đáp án) · **研究ノート** (trang tổng kết signature).
- Tool: `tools/make_diagrams.py` (contract giống health: `python tools/make_diagrams.py <SLIDES.json> <outdir> [tên_test]`, thêm diagram = thêm hàm + entry `DIAGRAMS`).
- **Render (chốt lại 2026-07-27 — HỒ SƠ KÊNH):** `python ..\youtube-jp-health\tools\video_render.py 03_SCRIPTS\<x>_TTS.md --channel nenkin`. Bấy nhiêu là đủ — giọng 雀松朱司/ノーマル/0.9, `--sub-style glass`, BGM −40dB, palette, bộ `drawn` (jp-pen+grid), đường dẫn ảnh TUYỆT ĐỐI đều nằm trong `..\youtube-jp-health\tools\channels.py` (**nguồn sự thật máy đọc — đổi bản sắc render thì sửa Ở ĐÓ, đừng chép giá trị vào file này nữa**). Cờ gõ tay vẫn thắng hồ sơ khi cần thử. **PREFLIGHT tự chặn** trước khâu voice nếu thiếu ảnh / `rank` = 0 / thiếu clip `handmade` / BGM sai đường dẫn. Máy kill ffmpeg dài → `CHUNKS_ONLY=1` chạy trước (chunk tự resume), rồi chạy lại với `--reuse`.

</details>

## 📝📝 TITLE — BẬT LẠI `【】` MỞ ĐẦU (user chốt 2026-08-10, ĐÈ quyết định 08-09 bên dưới)

**Căn cứ mới, mạnh hơn hẳn căn cứ cũ** (`CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` §2.2):
hai kênh cùng ngách đang nổ dùng `【】` ở **41/41** và **~39/39** video, và ăn hit **1,3M · 1,0M**.
Quyết định 08-09 dựa trên **một** kênh (`お金の保健室`) vứt `【】`, và **chưa có video nào của mình
chạy đủ số để bảo vệ nó** — nên đảo.

**Khuôn thi hành:** `【cảnh báo/cảm xúc】＋ 事件 ＋ 月 ＋！＋ hậu quả`, **32–39 ký**.
Bộ 【】 đo được ở đối thủ: `【期限切れ注意】【警告】【絶対確認して！】【超朗報！】【申請忘れ続出】【見逃し厳禁】【2026年最新】`.
Ví dụ đã dựng (video 10): `【9月に届きます】年金生活者支援給付金、届かない人のほうが損をします`.

⚠️ **Cả hai lần đều là TƯƠNG QUAN, không phải nhân quả** — đừng ghi vào sổ như đã chứng minh.
⚠️ **Điều KHÔNG đổi:** quét compliance (`youtube-compliance.md` mục 3) · **mọi tình tiết trên title
phải CÓ THẬT trong video** · **cấm 外来語 ở title/thumbnail** · bộ **3 title A/B** (A1 chốt · A2 đổi
keyword dẫn · A3 đổi kiểu hook) · **keyword đo cao nhất đứng đầu** (`youtube-upload-seo.md` §0.5).

<details><summary>(ĐÃ ĐÈ 2026-08-10) TITLE — BỎ 【】, chốt 2026-08-09</summary>

**Căn cứ đo được:** kênh cùng ngách `お金の保健室` dùng `【…】` mở đầu ở **11 video đầu**, rồi
**bỏ hẳn ở 13/14 video sau** và rút gọn còn **32–39 ký**. Video 152K của nó nằm đúng ranh giới
đó. 7/7 title của mình đang mở bằng `【】` — đúng khuôn nó vừa vứt.

**Khuôn mới:** `[SỰ VIỆC + MỐC THỜI GIAN]｜[HẬU QUẢ hoặc HẠN CHÓT]`, **32–39 ký**, không `【】`
mở đầu. Ví dụ đã dựng: `年金の口座に届く簡易書留、開けないまま45日が過ぎると登録されます｜断る人の書き方`.
Biến thể thứ hai: `[CÂU NGƯỜI XEM ĐANG TIN]｜[VẾ PHỦ ĐỊNH]`.

⚠️ **Điều KHÔNG đổi:** vẫn phải qua quét compliance (`youtube-compliance.md` mục 3) và **mọi
tình tiết nêu trên title phải CÓ THẬT trong video**. Bộ **3 title A/B** (`ab-3title-3thumb.md`)
giữ nguyên — A1 = title chốt, A2 đổi keyword dẫn, A3 đổi kiểu hook.
⚠️ **Đây là tương quan, không phải nhân quả đã chứng minh** — nó đổi title CÙNG LÚC với cú nổ
152K nên không tách được biến. Căn cứ để tin: nó **giữ khuôn mới suốt 14 video sau đó**.

</details>

## 📏 ĐỘ DÀI — 13–17 PHÚT (user chốt 2026-08-10, ĐÈ mọi mốc độ dài cũ của kênh)

**Căn cứ** (`CHANNEL_BENCHMARK_fukurou-tanuki_2026-08-10.md` §2.1): median thời lượng của **14 hit
≥100K** bên `フクロウ` = **15′00**, dải áp đảo 13–16′. Và `タヌキ` **rút từ 18–32′ xuống 9–12′ trong
2 tháng gần nhất**, đúng các bản ngắn đó đang thắng (9:00→45K · 11:32→86K · 9:55→43K).

- **Chuẩn: 13–17 phút.** Đo bằng máy, **không ước chay**: `python tools/make_tts.py <stem> --dry`
  → dòng `ƯỚC dài`. Ngoài dải thì cắt/bù chữ, không "chấp nhận tạm".
- Hệ số thực tế của tool: **5,72 ký/giây đọc thuần + 0,45s/dòng + 1,0s/đoạn** ⇒ 13–17′ ≈
  **4.300–5.300 ký** thân đọc, mật độ ~28 ký/dòng. (Video 10 đo được: 5.024 ký → **16:06**.)
- ⛔ **Bỏ mốc cũ 25–30′** (`audience-45plus.md` §4 đã sửa cùng lượt) và bỏ luôn đề xuất treo
  「nâng 15–25′ → 25–40′」 của 2026-07-28 — nó dựa trên median 26–37,5′ đo trên **bộ kênh khác**
  (完全攻略・速報・節約看護師). Bộ đó không sai, nhưng hai kênh nổ mạnh nhất hôm nay chạy ngắn hơn một nửa.
- **Lợi phụ đáng kể:** giảm ~35–40% công/video ⇒ nhịp 3 slot/tuần mới thực sự thở được.
- ⚠️ **Cái mất, biết trước:** video ngắn chở được ít 制度 hơn → phải **hy sinh chiều rộng để lấy một
  cú lật**. Bài nào tham 3 chế độ sẽ tự vỡ khỏi dải. Nếu 5 video ngắn mà AVD tụt dưới mức của video
  01–08 thì xét lại, **đừng đảo ngay sau 1 video**.

## Lưu file

- Script → `03_SCRIPTS/<số>_<slug>.md`.
- ⚠️ **upload_pack.py bắt HEADING đúng chữ, không phải nội dung** (bẫy mất 1 vòng ở video 06): phải có heading `### Title CHỐT` (chuỗi đó nằm TRONG code fence thì parser KHÔNG thấy) · heading mô tả phải chứa `Mô tả đầy đủ`/`BẢN ĐẦY ĐỦ` (khớp **phân biệt hoa-thường** — `bản đầy đủ` viết thường bị trượt) · `Tên file upload` · `3 dòng đầu` · `タグ`. Gói lại đè bản cũ → thêm `--force`.
 Media qua kho chung `_media_library` theo rule. CTA giữa video: viết câu canonical riêng cho kênh này (chưa có — soạn khi chốt persona, thêm vào `.claude/rules/cta-midvideo.md` mục 2).

> 📦 Doc cũ (diagnosis/optimize/benchmark hết hạn, khuôn đã bị đè) đã dời vào `./_archive/` (dọn 2026-08-24) — đường dẫn cũ trong rules trỏ file nào không thấy ở gốc thì tìm ở đó.
