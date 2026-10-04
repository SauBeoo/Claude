# YouTube Niche Research 2026 — 5 ngách nhỏ-mà-chất (JP + KR)

> Nghiên cứu 2026-07-23 theo yêu cầu: rời ngách đại trà, tìm ngách nhỏ nhưng khán giả đến VÌ chủ đề, trung thành.
> Tiêu chí chấm (user chốt): ① ít đối thủ thật sự (đo được) · ② khán giả trung thành · ③ RPM/tiền tốt · ④ bền dài hạn.
> Phương pháp: 5 research agent quét web JP/KR (Tầng 1, ~30 ứng viên) → thẩm định Tầng 2 bằng **YouTube Data API đo thật** (subs/views/cadence, ngày đo 2026-07-23, token readonly chouhen + kr-romfan; raw data: scratchpad `niche_results.json`/`phase2_results.json`/`phase3_kr_results.json`, ~350 video + ~260 kênh).
> Ký hiệu **v/s** = views video nổi ÷ subs kênh — v/s cao nghĩa là thuật toán đẩy đề tài bất chấp kênh nhỏ (cầu vượt cung).
> ⚠️ Chưa đo Google Trends cho từng ngách — Trends chỉ bắt buộc ở bước đóng gói metadata (rule `youtube-upload-seo.md` 0.5) khi lập kênh; quyết định cấp ngách dùng số views/subs thật của API (tín hiệu mạnh hơn).

## BẢNG TỔNG — 5 NGÁCH CHỐT

| # | Ngách 日本語/한국어 | Ngách (tiếng Việt) | Khán giả | Vì sao chọn (1 dòng) | Bằng chứng đo 2026-07-23 |
|---|---|---|---|---|---|
| 1 | 実家じまい・空き家・相続登記 | Dọn nhà bố mẹ để lại + nhà hoang + đăng ký thừa kế | Con cái 50–65 có bố mẹ già/mất | Cung TRỐNG tuyệt đối ở format faceless chuyên đề, cầu proven nhiều năm, RPM bất động sản 800–1.200円 | Video 1M–3,8M view rải 2021→2026 từ TV/vlog/shorts; v/s dị thường 497 (kênh 7,6K subs ăn 3,78M); 空き家 900万戸 kỷ lục |
| 2 | 親の介護とお金 | Tiền + thủ tục chăm bố mẹ già (cho gia đình, phi y tế) | Con cái 45–65 đang/sắp chăm bố mẹ | 2 agent độc lập cùng xếp #1; chưa có kênh faceless nào chuyên cho GIA ĐÌNH; affiliate 老人ホーム đơn giá cao nhất mảng senior | 653万 người chăm; chi phí bình quân 542万円/người; đề tài 介護費用 lên kênh tiền-senior ăn 700K–2,9M view; proof format: きな子 (VOICEVOX, 2024) 167K subs |
| 3 | 地名・地形・河川史 | "Ký ức của đất": nguồn gốc địa danh, sông ngòi, địa danh cảnh báo thiên tai | JP 45–70, local pride | Gap trống nhất + rủi ro thấp nhất: 2 kênh chuyên đều bỏ hoang mà video vẫn nổ view — cầu bị bỏ đói 4 năm | Kênh 9,5K subs bán bỏ hoang: hit 542K (v/s 57); kênh 4 video ngủ đông từ 2022: hit 1,52M vẫn hút; kênh mới 0-tuổi vào ăn ngay 142K |
| 4 | 睡眠用・長編歴史朗読 | Lịch sử Nhật kể thành truyện 2–3h nghe trước ngủ | JP 40–70 nghe đêm | Cửa sổ đang mở có số đo; khớp pipeline nhất (kịch bản dài + TTS là đúng vũ khí); loyalty kiểu thói-quen-hằng-đêm | ぐっすり眠れる歴史: lập 2026-03, sau 4,5 tháng = 40,5K subs / 54 video / 5,18M views, hit 江戸 3h = 621K; kênh thứ 2 cùng sóng 14,5K subs |
| 5 | 장기요양·요양원 (가족 가이드) | Thủ tục + tiền viện dưỡng lão Hàn — hướng dẫn cho NGƯỜI NHÀ | Con cái Hàn 40–60 lo cho bố mẹ | Ngách KR duy nhất (trong 3 ngách KR đã đo) vừa cầu triệu view lặp lại vừa cung đúng-format = 0; không phải đua tần suất với farm | Cầu: 요양원-chọn-thế-nào 3,40M; kênh 6K subs ăn 718K (v/s 119). Cung: kênh chuyên đề bé nhất (스마일시니어 4,3K) sắp tắt; 준희쌤 82,7K là LUYỆN THI chứng chỉ, không phải cho gia đình |

**Thứ tự ưu tiên nếu chỉ mở 1–2 kênh** (xếp hạng cuối của vòng thẩm định API): ① 実家じまい → ② 地名・河川史 → ③ 장기요양 KR → ④ 親の介護とお金 → ⑤ 睡眠用歴史 (con bài tốc độ — cửa sổ đang mở nhưng sẽ đông, vào là phải vào nhanh; 4 ngách kia là con bài trận địa, để 6 tháng nữa vẫn còn).

*(Chi tiết từng ngách + ngách bị loại và lý do ở dưới.)*

---

## NGÁCH 1 — 実家じまい・空き家 (JP) ⭐ đề cử số 1

**Là gì:** Kênh faceless chuyên "tài sản bố mẹ để lại": dọn/bán/giữ nhà bố mẹ (実家じまい), nhà hoang (空き家), đăng ký thừa kế bắt buộc (相続登記義務化), thuế nhà đất, phá dỡ, 3 lựa chọn bán/cho thuê/phá. Trục phụ nở được: 墓じまい (dọn mộ — 改葬 176.105 vụ 2024, kỷ lục, gấp 2 lần/10 năm), 老後の住み替え/リバースモーゲージ (đúng mảng đã cắt khỏi nenkin).

**Vì sao chọn (4 tiêu chí):**
- **Ít đối thủ — TRỐNG tuyệt đối (đo API):** không tồn tại kênh faceless chuyên đề nào. Cung hiện tại = phóng sự TV lẻ (MBS/ABC/ABEMA), vlog dọn nhà cá nhân (uchilog 195K — nhưng đã chuyển sang đồ 100均), kênh pháp lý view bèo (司法書士 41,6K subs, view 281–3.094/video).
- **Cầu proven lặp lại:** uchilog 実家の片付け 1,77M + 1,56M; MBS 実家じまい 1,12M; 楽待 相続登記義務化 1,28M; short trên kênh **7.600 subs ăn 3,78M view (v/s 497)**; short của kênh 17 subs ăn 1,83M. Thuật toán chủ động đẩy đề tài bất kể kênh to nhỏ.
- **Nền cầu vĩ mô:** 空き家 900万戸 = 13,8% tổng nhà ở, kỷ lục lịch sử ([総務省 令和5年住宅・土地統計調査](https://www.stat.go.jp/data/jyutaku/2023/pdf/kihon_gaiyou.pdf)). Hai luật dí: 改正空家特措法 12/2023 (quản lý kém → mất ưu đãi thuế) + 相続登記義務化 4/2024 (áp hồi tố, có phạt) — nỗi đau cưỡng bức, không phải sở thích.
- **Tiền:** RPM 不動産 800–1.200円/1.000 view ([UREBA Lab](https://ureba.jp/lab/current-youtube-ad-cpm/)); affiliate 不動産一括査定 **10.000–25.000円/case** + 遺品整理/買取.
- **Bền:** thuế/thủ tục/case từng tỉnh/chi phí phá dỡ/相続放棄… ≥100 đề tài; luật đổi liên tục = content tự sinh.

**Production:** faceless voice + slide — pipeline nenkin tái dùng nguyên. YMYL trung (tiền+BĐS): mọi con số trích 国交省/法務局, disclaimer hỏi chuyên gia.

**Rủi ro:** nói sai thuế/thủ tục bị comment bắt lỗi → fact-check nguồn chính phủ từng số. Format "giảng bài" đã chứng minh chết (kênh 親ケア kiểu 講座 view 3 chữ số) — phải đóng gói kiểu loss-aversion "nhà bố mẹ đang âm thầm ngốn tiền của bạn" đúng công thức cold-open sẵn có.

## NGÁCH 2 — 親の介護とお金 (JP)

**Là gì:** Tiền + thủ tục chăm bố mẹ già cho CON CÁI 45–65 (thế hệ sandwich): 要介護認定, 介護保険 từng dịch vụ, 高額介護サービス費, chọn viện theo giá, 介護離職, case tính thử tiền (format đang chạy tốt ở nenkin). KHÔNG y tế, chỉ tiền + chế độ.

**Vì sao chọn:**
- **Hai agent độc lập (góc RPM + góc demographic) cùng xếp #1** trước khi biết kết quả của nhau.
- **Ít đối thủ (đo API):** các kênh 介護 lớn đều lệch tệp — ケアきょう 10万+ cho NGƯỜI LÀM NGHỀ; 親ケア.com đúng đề nhưng kiểu 講座 hiệp hội: 864 video mà 42,9K subs, view 42–1.276/video; kênh vlog đầu ngách 兄のぼる 85K đã KẾT THÚC series (bố mất). **Kênh faceless chuyên "tiền 介護 cho gia đình": không tồn tại.**
- **Cầu:** 653万 người đang chăm gia đình (cứ 20 người Nhật có 1); ビジネスケアラー 262万 → 318万 (2030), thiệt hại kinh tế ~9兆円 (METI); chi phí bình quân **542万円/người** (一時 47,2万 + 9,0万/tháng × 55 tháng, [生命保険文化センター 2024](https://www.jili.or.jp/lifeplan/lifesecurity/1116.html)) — con số hook tự bán. Đề tài 介護費用/給付金 lên kênh tiền-senior tổng ăn 700K–2,94M view.
- **Proof format:** きな子のシニアお金ゼミ — faceless VOICEVOX, lập 2024-02 → 167K subs / 17,1M views, nhưng chỉ làm 年金/税, NÉ 介護 → khoảng trống nằm ngay cạnh kênh đã chứng minh công thức.
- **Tiền:** RPM 保険・金融 700–1.000円; affiliate 老人ホーム紹介/見積り = **nhóm đơn giá cao nhất mảng senior, trên cả 転職エージェント**.
- **Bền:** chế độ × tình huống (chăm từ xa, độc thân chăm, anh em cãi tiền) × 介護保険 sửa 3 năm/lần.

**Production:** giống nenkin nhất trong 5 ngách — chi phí học ngách ≈ 0. Khán giả trẻ hơn tệp senior hiện có 10–20 tuổi (45–65, đang đi làm) = mở rộng danh mục sang tệp mới mà vẫn cùng hệ tri thức.

**Rủi ro:** ranh giới với nenkin phải vạch rõ (nenkin = tiền hưu CỦA MÌNH; kênh này = tiền chăm BỐ MẸ). YMYL trung: chỉ nói chế độ công khai nguồn 厚労省.

## NGÁCH 3 — 地名・地形・河川史 (JP) — bet dài hạn đẹp nhất

**Là gì:** Documentary "ký ức của đất": vì sao chỗ này tên vậy, dòng sông này từng gây lụt giết bao người, địa danh cảnh báo thiên tai (蛇/滝/久保…), bản đồ cổ so với nay, 治水史. Giọng tài liệu nghiêm túc — KHÔNG đi nhánh 怖い地名 giật gân (nhánh đó đã bị nhóm kênh mystery 100K+ công nghiệp hóa: ミステリーナイトウ 116K đang cày series 怖い地名 từng tỉnh).

**Vì sao chọn:**
- **Gap trống nhất, verify 2 lớp (đo API 2 lần):** kênh chuyên duy nhất 日本地名の解説 chỉ 9.490 subs / 14 video / gần bỏ kênh — mà hit 542.299 view (v/s 57). Kênh いつか役に立つ教養 4 video, **ngủ đông từ 2022-08** — hit 東京の歴史 1.519.145 view vẫn hút sau 4 năm. Kênh mới 0-tuổi (数字は語る, lập 2025-11) vào ăn ngay 142K view. Nhánh 河川史/災害地名 nghiêm túc: **không đo thấy kênh chuyên nào**.
- **Trung thành đúng nghĩa "đến vì chủ đề":** local pride — người xem comment kể chuyện quê mình = engagement thật (đúng thứ luật inauthentic 07/2025 muốn thấy); đề tài 47 tỉnh × địa danh × sông × thảm họa = người xem chờ đến lượt quê mình.
- **Tiền:** RPM khối giáo dục/đời sống mức giữa; advertiser phòng chống thiên tai/BĐS (suy luận, chưa xác minh). Yếu hơn ngách 1–2 về đơn giá — đổi lại rủi ro thấp nhất.
- **Bền:** kho vô hạn + tự viral mỗi mùa mưa bão (地名 cảnh báo thiên tai); nguồn free: bản đồ cổ + 空中写真 各年代 của [国土地理院](https://www.gsi.go.jp/tizu-kutyu.html), 柳田國男『地名の研究』 public domain.
- **Khiên chống inauthentic mạnh nhất:** bản đồ so sánh xưa–nay tự dựng = visual gốc không kênh AI-slop nào nhái nhanh được.

**Production:** voice-over + bản đồ/không ảnh — pipeline hiện có + khâu dựng bản đồ so sánh (đầu tư mới, xứng đáng vì chính nó là moat). **Rủi ro:** thấp nhất bảng; duy nhất phải né tuyệt đối 差別地名 (địa danh dính 部落).

## NGÁCH 4 — 睡眠用・長編歴史朗読 (JP) — cửa sổ đang mở, khớp pipeline nhất

**Là gì:** Kể 1 chủ đề sử Nhật thành truyện dài 2–3 tiếng, giọng đều, cho người nghe trước ngủ + làm việc nhà: 江戸庶民の暮らし, 昭和史 đời thường, nhân vật, 地方史.

**Vì sao chọn:**
- **Cửa sổ có số đo (API):** ぐっすり眠れる歴史 lập **2026-03-08**, sau 4,5 tháng: 40.500 subs / 54 video / 5,18M views, đăng 3 ngày/video mỗi video ~3h, hit 江戸時代 621K. Kênh thứ 2 おやすみ歴史館 (lập 2025-12): 14,5K subs, video 2,5–7,5h đều 12K–67K view. Cả 2 đều sinh sau 12/2025 mà tăng tốc như vậy = cầu đang vượt cung rõ.
- **Trung thành kiểu thói quen:** nghe MỖI ĐÊM = loyalty hành vi mạnh nhất trong 5 ngách; khán giả sub để có gì nghe tối nay.
- **Khớp pipeline nhất:** kịch bản dài + TTS + visual tĩnh ukiyo-e/tư liệu PD = đúng bộ máy sẵn có; script 3h ≈ 45–50K ký tự (gấp ~3 chouhen), render dài đã có bài resume/chia chunk.
- **Tiền:** video 3h = mid-roll dày; RPM khối giải thích mức giữa (150–450円) — ăn bằng watch-time khổng lồ thay vì đơn giá.
- **Bền:** toàn bộ sử Nhật; kênh benchmark chạy tới đề tài hẹp (保元の乱, 刀伊の入寇) vẫn có view.

**Rủi ro (cao nhất trong 4 ngách JP — nói thẳng):**
- **Inauthentic 07/2025:** đúng profile "AI voice + nền tĩnh" bị quét. Khiên bắt buộc: kịch bản gốc dẫn nguồn sử liệu trong 概要欄, visual đổi từng video (kho _media_library), chương mục riêng, engagement device (học chiêu ぐっすり: giấu シークレットワード trong video kéo comment — bằng chứng người thật nghe thật).
- **Cửa sổ sẽ đông:** đây là ngách "đang nổ" — vào thì phải vào NHANH và thắng bằng chất kịch bản, không phải bằng tồn tại. Trong 5 ngách, đây là con bài tốc độ; 4 ngách kia là con bài trận địa.

## NGÁCH 5 — 장기요양·요양원 hướng dẫn cho gia đình (KR)

**Là gì:** Kênh faceless tiếng Hàn giải thích cho CON CÁI 40–60 đang lo cho bố mẹ già: 장기요양등급 xin thế nào (cấp 1–5 khác gì), 요양원 vs 요양병원 vs 방문요양 chi phí thật từng loại, 가족요양 nhận lương 2~90만원/tháng, 복지용구, mẹo khám 치매 등급 — combo "tiền + thủ tục + cảm giác tội lỗi" đúng công thức retention. Bản KR của ngách 2 (介護とお金) — cùng hệ tri thức, hai thị trường.

**Vì sao chọn (đo API 2026-07-23, token kr-romfan):**
- **Cung MỎNG + LỆCH VAI — chưa có ai đúng format:** toàn bộ cung hiện tại là (a) kênh luyện thi chứng chỉ 요양보호사 (준희쌤 82,7K sống khỏe — nhưng dạy người làm NGHỀ; 요양보호사TV chết từ 2020), (b) kênh công ty/center bán dịch vụ view 3–4 chữ số (케어링 22,9K nhưng shorts chỉ 1,4–1,8K view; 아들딸방문요양 114K nhưng view 35–2.891), (c) kênh chuyên đúng đề duy nhất thì bé và sắp tắt (스마일시니어 4.290 subs, video cuối 2025-11). **Kênh độc lập cho NGƯỜI NHÀ: không tồn tại.**
- **Cầu chứng minh nhiều lần:** 김작가 TV đề "chọn 요양원 thế nào" **3,40M view**; EBS 다큐 2,47M; kênh faceless mới 누룽지 (lập 2025-04 → 60,2K subs) video 「요양원 말고 이 두 곳」 **667.808 view**; kênh 6.040 subs ăn short 요양원 **718.041 view (v/s 118,9)**; 치매똑똑 「요양원 vs 요양병원 비용」 473K.
- **Nền vĩ mô:** Hàn vào 초고령사회 — 65+ = 20,3% dân số 2025, lên 30% năm 2036 ([통계청](https://www.kostat.go.kr/board.es?mid=a10301010000&bid=10820&tag=&act=view&list_no=438832)); 954만 베이비부머 đợt 2 đang vào tuổi hưu; thời gian xem video của người già Hàn tăng 6,3 lần trong 5 năm.
- **Tiền:** RPM long-form senior KR đo thật 5.719원/1.000 view (~gấp 3 kênh thường); advertiser 요양 platform (케어링…) đang đốt tiền marketing; quyết định chi tiêu của tệp = hàng triệu won/tháng tiền viện.
- **TTS hợp lệ ở tệp này:** khán giả 4060–5060 Hàn chấp nhận TTS (kênh AI lấy nút bạc 3 tháng; format 오디오북 là chuẩn ngách info senior); Azure SunHi (nữ ấm) sẵn có.
- **Bền:** ~100 đề khả thi + chính sách 노인장기요양보험 đổi hằng năm; nguồn số liệu công khai 건보공단.

**Production:** TTS Hàn + slide — pipeline kr-romfan (voice) + video_render (slide) ghép được; cần viết script INFO tiếng Hàn (khác audio-drama hiện tại — đầu tư mới chính là kịch bản info KR, không phải tool).

**Rủi ro:** YMYL nhẹ hơn health (né tư vấn y tế/pháp lý cụ thể, chỉ chế độ + tiền); workspace chưa có lợi thế production info-content KR — video đầu sẽ chậm hơn các ngách JP. Vì thế xếp sau 実家じまい và 地名 trong thứ tự ưu tiên.

---

## NGÁCH BỊ LOẠI Ở TẦNG 2 & LÝ DO (đừng đề xuất lại)

| Ngách | Lý do loại (số đo 2026-07-23) |
|---|---|
| 俳句・短歌 giảng giải | **Trap niche** — cung mỏng vì CẦU cũng mỏng: đầu ngách 夏井いつき (thương hiệu TV プレバト) chỉ 95,7K subs, video mới 1.391–2.879 view; faceless 短歌一期一会 199 video → 11,8K subs, view 229–862. Không có trần để ăn. |
| 城郭・山城・古戦場 | Cung VỪA→ĐÔNG: hệ sinh thái hoàn chỉnh — YUKIMURA 255K sống khỏe (186K–640K/video), 3D/thực địa/học giả đều có chủ. |
| 相続トラブル kể chuyện (JP) | Cầu rất mạnh (v/s 126 trên kênh 43 subs) nhưng スカッと tổng 693K subs đăng 2–3 video/NGÀY đã phủ đề tài công nghiệp; 士業 mặt thật cũng đông. Khe duy nhất "chuyên hóa 100% 相続-case" — hẹp, để làm TRỤC ĐỀ TÀI cho chouhen thay vì kênh mới. |
| 상속·증여 사연 (KR) | Cửa sổ ĐANG ĐÓNG THEO TUẦN: 반전극장 (3 tháng tuổi) + 황금빛사연 (5 tuần tuổi, 14,1M views) đang chiếm; toàn ăn ở SHORTS 참교육, bản long-form của chính họ chỉ 28–66 view — long-form chưa có bằng chứng sống. |
| 사연 Hàn thuần (고부갈등/황혼이혼…) | "블랙오션" — 11 kênh AI-slop gom 8,4 tỷ view, kênh mới chết sau 2–3 tháng, video 45′ thử nghiệm kiếm 2.911원 ([세컨드샐러리](https://www.secondsalary.co.kr/news/articleView.html?idxno=157)). |
| 국민연금·기초연금 info (KR) | Đo API: bão hòa kiểu CONTENT-FARM — 4 kênh lập trong 12 tháng đã bơm 1.000–1.600 video/kênh; view lẻ vẫn nổ (kênh 7,1K subs ăn 2,08M) nhưng view không chuyển thành subs, phải đua tần suất với farm + kênh chính phủ (보건복지부TV short 21,8M) + chuyên gia mặt thật (연금박사 438K); đúng vùng enforce inauthentic 01/2026. Ngược chiến lược chất-lượng-video-dài. |
| KR 야담・민담 audio | Cầu nổ thật (v/s 40–144, 구름야담 2 tháng → 88,8K subs) NHƯNG là gold-rush đông người vào cùng lúc, moat mỏng — ngược đúng đề bài "không theo số đông". Giữ làm quân bài nếu muốn đánh nhanh. |
| 仏教・法話 nghe đêm (JP) | Bão hòa đáy đã hiện: 夜の仏話 522 video → 1.320 subs, video 69 view; đúng nguyên mẫu inauthentic bị quét. |
| 青空文庫 朗読 thuần | Giọng người chuyên nghiệp thống trị (窪田等 296K, cựu NHK) — TTS đấu giọng NHK thật = thua chắc. |
| 廃村・限界集落 / 귀농귀촌 / 짠테크 | Giá trị nằm ở footage/đời thật của chính chủ — faceless không thay được (山적TV 121만, 강과장 29,6만). |
| 昭和ノスタルジー đồ vật | Đã có kênh chuyên + nghẽn ảnh tư liệu Showa bản quyền; CPM thấp. |
| M&A・事業承継 | Trống nhất nhưng tệp hẹp nhất (chủ DN không xem YouTube giải trí), cần chuyên môn tài chính DN thật — quân bài dài hạn. |
| 詐欺手口 mổ xẻ | Trống thật + hợp kể chuyện nhưng RPM trung bình + news-driven; làm TRỤC ĐỀ TÀI cho health/nenkin tốt hơn mở kênh. |
| おひとりさま老後 | A-rank Tầng 1 (cung chỉ có vlog + luật sư) nhưng chưa qua đo API Tầng 2; ứng viên dự bị số 1 nếu muốn kênh thứ 6. |

## SỐ NỀN RPM (đối chiếu khi chọn)

| Ngách JP | RPM (円/1.000 view, [UREBA Lab 2025](https://ureba.jp/lab/current-youtube-ad-cpm/)) |
|---|---|
| 不動産投資 | 800–1.200 |
| 保険・金融商品 | 700–1.000 |
| 転職・キャリア | 500–800 |
| 健康・サプリ | 400–650 |
| Giải thích/giáo dục chung | 150–450 |
| エンタメ | 100–300 |

KR: RPM long-form ngách senior đo thật **5.719원/1.000 view (~4,3 USD), gấp ~3 lần kênh thường** ([세컨드샐러리 case study](https://www.secondsalary.co.kr/news/articleView.html?idxno=157)). TTS được tệp 5060 Hàn chấp nhận (kênh AI 사연 lấy nút bạc 3 tháng; các kênh 연금 top tự dán nhãn 오디오북); tệp trẻ 2030 thì ghét TTS — né.

## BƯỚC TIẾP THEO KHI CHỌN NGÁCH LẬP KÊNH (chưa làm — chờ user chọn)

1. Đo Google Trends gprop=youtube (30 ngày + 12 tháng, geo JP/KR) cho rổ keyword ngách được chọn — rule `youtube-upload-seo.md` 0.5.
2. Mở 3–5 kênh benchmark bằng browser đọc bằng mắt: giờ đăng, format title/thumbnail, categoryId, rổ tag (playbook mổ benchmark như đã làm với 昔の人の知恵).
3. Chốt bộ nhận diện tầng kênh (rule 2.4) + tên kênh + persona + giọng TTS trước video đầu.
