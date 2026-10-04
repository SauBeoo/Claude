# CLAUDE.md — youtube-jp-shokutaku

> Rule riêng kênh 「60代からの食卓」. Ghi đè/bổ sung CLAUDE.md toàn cục.

## Vault tương ứng

Tri thức/research/bài học: `E:\Claude\SecondBrain\10_Projects\youtube-jp-shokutaku\`.

## ⚠️ RULE BẮT BUỘC khi viết kịch bản

**Mọi lần viết kịch bản cho project này PHẢI nương theo skill `script-shokutaku`** (`~/.claude/skills/script-shokutaku/SKILL.md`) — chạy đủ 4 bước ngầm, đúng bộ xương Mục 10, giọng みのり, rà đủ 13 điểm checklist Mục 14 trước khi xuất.

**Chọn đề tài theo `03_CONTENT_PLAN.md` (user chốt 2026-07-19)** — hàng đợi 5 key 4 trụ (script 08–12), không tự đề xuất chủ đề "組み合わせ" lan man ngoài hàng đợi; hết hàng đợi → đo trend vòng mới rồi bổ sung file đó.

Đây là kênh **KHÁC** `youtube-jp-health`:
- Persona cố định **みのり**, có câu chào/kết/disclaimer cố định (Mục 10 skill) — chỉ sửa MỘT lần rồi giữ vĩnh viễn.
- Độ dài **mặc định 21–25 phút** (~5.800–6.900 ký tự @ 4,60 ký/giây) — ⭐⭐ **SIẾT DẢI 2026-08-11** (user chốt, §🎯 RETENTION): dải cũ 15–25′ bỏ mép dưới vì **cắt ngắn làm AVD PHÚT tụt** (納豆 29′→15′: 4′33 → 3′11) trong khi chỉ mua +6 điểm AVD%. Bật lại mép 15′ khi @40s đã ≥70%. ⤵ căn cứ cũ: 15–25′ ĐỔI 2026-07-21 theo `CHANNEL_OPTIMIZE.md` (video 14′ được đẩy mạnh nhất, 35′ bị bóp; đối thủ chuẩn 長生きの秘訣 cũng 20–30′). Bản 35–40 phút chỉ khi user yêu cầu rõ / kênh qua sandbox. Xem [[project_do_dai_video_theo_kenh]].
- Có **chế độ A·REMAKE** transcript (bám bộ xương retention bản gốc, viết lại 100% câu chữ) — health không có.

## 🎯 RETENTION — MỤC TIÊU AVD 60% (user chốt 2026-08-11)

> Bằng chứng đầy đủ: **`CHANNEL_DIAGNOSIS_2026-08-11.md`**. Gate máy: **`python tools\check_coldopen.py <NN>`** (thêm `--calib` để hiệu chuẩn lại). Spec viết: skill `script-shokutaku` MỤC 10 §v3 + MỤC 14 điểm 0/0b/0c.

**Hiện trạng (Analytics API 2026-08-11):** 14 video / 36 ngày → 72 view · **AVD 3′53″ = 17,0%** · `relPerf` 60s đầu **0,06–0,29** (phân vị đáy) · `BROWSE = 0` tuyệt đối.

🔴 **CỬA TỬ LÀ GIÂY 20 → 40.** Gần như không ai bỏ đi trong 17 giây đầu (95,8–100%), rồi mất **45–55 điểm trong 12–18 giây**. Cú rớt lớn nhất của từng video rơi đúng vào **một câu TỰ THÁO NGÒI LỜI HỨA**: 納豆 「納豆が悪者になったという話ではないのです」 **−55đ** · ブルーベリー 「悪いのはブルーベリーではありません」 **−50đ** · ゆで卵 「にわかには信じがたい」 **−38đ**. Thủ phạm phụ: **khối credential** 「私はこれまで長い間…」 (−8đ, và vi phạm persona みのり).

🟢 **Đuôi bài KHÔNG hỏng** — từ phút ~6 curve phẳng tuyệt đối tới hết. Ai sống qua phút 6 thì xem hết. Chữa chỗ RÒ, không phải chữa "bài chán".

🔴 **CẮT NGẮN KHÔNG MUA ĐƯỢC 60% — GIỮ 21–25′.** Tích phân curve thật: cắt xuống **5 phút** vẫn chỉ 43,5%; cắt về 15′ chỉ +6 điểm. Và cắt còn làm **AVD phút TỤT** (納豆 29′→15′: 4′33 → 3′11) — đi ngược đúng mục tiêu. Bật lại chuyện cắt khi @40s ≥70%. Chiều thứ hai: benchmark ngách 高齢者健康の真実 median **37′** vẫn ăn view.

✅ **GIẢ THUYẾT ĐÃ BỊ BÁC, đừng dựng lại:** "chuỗi 3 câu 「〜ませんか」 (luật L5) chiếm cửa tử nên phải bỏ" — **SAI**, ゆで卵 giây 21 đọc đúng 「少し気になりませんか?」 mà vẫn giữ 95,8%. **L5 giữ nguyên.**

**Hai con số phải đạt:** ① **@40s ≥85%** (nay 30,0 / 45,5 / 50,0%) ② **sàn thân bài ≥55%** (nay 9,1 / 10,0 / 20,8%).

⚠️ **60% chưa có tiền lệ trong workspace** — cao nhất từng đo là chouhen video 12 **51,6%**, và đó là DRAMA. Mốc chặng **30% → 40% → 50% → 60%**; 🛑 **3 video liên tiếp ≤25% AVD% → mốc 60% sai với ngách này, mổ lại chứ đừng vá tiếp.**

⚠️ **Sửa retention KHÔNG mở vòi phân phối** (`BROWSE = 0`). Đọc kết quả bằng `relPerf` giây 15–45 + AVD% của chính video mới, **không** bằng view. Mốc "8 video qua gate mà BROWSE vẫn 0 → mở kênh mới" (~08-25) **KHÔNG bị hoãn**.

## 🔴 KHÁM KÊNH 2026-08-09 — GIỮ chủ đề, cày nốt tới mốc 8 video (user chốt)

> User hỏi *"kênh mãi không được đề xuất, có nên đổi chủ đề không?"* → **KHÔNG.** Lý do: phép thử đó **đã chạy rồi**.

### Số đo (API, 2026-08-09)

| | |
|---|---|
| Kênh | 13 video / 34 ngày · **66 view · 1 sub** |
| Traffic 07-01→08-09 | SUBSCRIBER 24 · YT_CHANNEL 14 · RELATED_VIDEO 11 · NO_LINK 6 · EXT 5 · YT_SEARCH 2 · **BROWSE_FEATURES = 0 tuyệt đối** |
| 5 video đã chuyển hẳn sang luồng 食べ合わせ (07-31→08-07) | **0 · 0 · 0 · 0 · 2 view** |
| Index | search đúng title → video ra **#1** ⇒ không án phạt, không de-index |
| Ngách còn sống? | kênh gốc 高齢者健康の真実 (14.100 sub) tuần này vẫn **255–6.382 view/video mới** |
| Kênh COPY công thức | 知恵袋TV 63.155 (07-26) → **28–63** (08-02→08-08) · 栄養研究室 48.164 (07-21) → **48–128** |
| Cùng món cùng tuần | 知恵袋TV キャベツ食べ合わせ 08-03 = 63 view · mình 08-02 = **0** |

**Đọc đúng:** chủ đề KHÔNG phải bệnh — kênh đã đổi sang đúng luồng đang thắng từ 07-31 và vẫn 0 view. Bệnh vẫn là **vòi cấp kênh chưa từng mở**; chủ đề chỉ quyết định video được test ở RỔ nào, mà kênh chưa được test lần nào. Đồng thời: **kênh COPY công thức chết trong ~10 ngày, kênh GỐC vẫn sống** — đừng kỳ vọng copy công thức là mở được vòi.

⚠️ **Chỗ "đổi chủ đề" MỚI có nghĩa** (chưa làm, hoãn tới mốc 08-25): health và shokutaku đang **cùng ngách, cùng luồng 食べ合わせ, cùng tệp senior JP** — đổi để TÁCH shokutaku khỏi health thì có lý; đổi để đuổi theo món đang hot thì vô nghĩa (đó là chỗ 19 kênh đang chen, `youtube-jp-health/CHANNEL_DIAGNOSIS_2026-08-03.md` §4.1).

### ✅ ĐÃ LÀM 2026-08-09 — vá 3 lệch metadata trên 13 video LIVE

Script dùng một lần + sổ hoàn tác đầy đủ snippet cũ: `scratchpad/shokutaku_fix_2026-08-09.py` + `shokutaku_backup_before_fix.json`.

| # | Lệch | Trước | 3 kênh ngách | Đã sửa |
|---|---|---|---|---|
| 1 | categoryId | **22** (13/13) | **27** (真実 20/20 · 知恵袋TV 13/13 · 栄養研究室 9/9) | ✅ 27 ở 13/13 + `upload_api.py` API_CFG 26→**27** |
| 2 | số tag | 22–33 (median 32) | 44 (kênh gốc) | ✅ 36–42, bộ nhận diện 16 tag đứng đầu |
| 3 | tên kênh `" 60代からの食卓"` thừa dấu cách | — | — | ❌ **API KHÔNG đổi được** → user sửa tay Studio |

🔴 **Lỗi nặng nhất bắt được — 4 video mới nhất đeo lại 7 tag rác của video 腎臓** (`腎臓 食事 · 腎臓に悪い食べ物 · 60代 健康 · リン 腎臓 · バナナ 腎臓 · 漬物 腎臓 · 田中教授`), trong đó **`田中教授` = tên người thật**, vi phạm luật kênh. Đợt dọn 08-01 chỉ vá 2 video cũ mà **không tắt nguồn sinh ra chúng**.
→ **Nguồn = `アップロード動画のデフォルト設定` (default upload tags) ở cấp KÊNH trong Studio**, đặt vào khoảng 07-22. Bằng chứng: script của cả 4 video **sạch** (tag rác không có trong file), 7 tag rác bị **prepend** với **thứ tự y hệt nhau** ở cả 4, và mọi video đăng **từ 07-22 trở đi** đều nhiễm (緑茶 07-22 · はちみつ 07-31 nhiễm → đã dọn 08-01; 4 video sau nhiễm lại).
- ⛔ **Data API KHÔNG đọc/sửa được default upload settings** → phải sửa TAY: Studio → 設定 → アップロード動画のデフォルト設定 → 詳細設定 → タグ → xoá sạch. **Không xoá thì mọi video đăng sau vẫn nhiễm lại.** (user nhận việc 2026-08-09)
- ⚠️ Bài học: dọn hậu quả mà không tắt nguồn thì nó mọc lại sau đúng 1 video.

⚠️ **3 lệch trên KHÔNG phải thuốc chữa BROWSE=0** (browse không đọc categoryId để quyết định có test hay không). Sửa vì rẻ + đảo được + đang lệch so với 3/3 kênh ngách — không phải vì đã chứng minh nhân quả.

🟡 **Còn treo:** video `BKh-sdhsNUg` (腎臓) — `videos.update` trả về 38 tag ở cả 2 lần ghi, nhưng `videos.list` đọc lại vẫn ra **26 tag bản cũ** sau 20 giây. categoryId 27 thì vào bình thường. **Chưa xác nhận được**, soát tay trong Studio khi tiện.

### Việc 2 — cày nốt 4 video cho đủ mốc 8 (không đổi biến nào khác)

Điều kiện chuyển hướng ở §dưới ghi **8 video qua gate mà BROWSE vẫn 0**. Đã có 4 (08-02 キャベツ · 08-03 麦茶 · 08-05 ヨーグルト · 08-07 豆腐) → cần **4 nữa**, rơi vào ~08-11 · 08-13 · 08-15 · 08-18 theo lịch T2·T4·T6.

- Mọi script PASS `python tools\check_coldopen.py` trước khi render (gate hiện hành, **không siết thêm**).
- **Chọn món theo ĐỘ ĐÔNG, không theo món đang nổ** — ưu tiên cột trống (酢 · かぼちゃ · シナモン · 生姜 · 大根 · 味噌汁); ⛔ tránh 納豆 · 卵 · ブルーベリー (bão hoà). **Đo lại độ đông trước khi chốt món** (bảng §4.1 đo 08-03).
- Tồn kho: `06_blueberry-kumiawase` (đã render, hook fail → sửa là phải render lại) · `07_ninjin-kumiawase` · `08_jinzo-yoi-tabemono` (**rổ 臓器 = luồng chết median 24 v/ngày → re-angle sang MÓN làm chủ ngữ**).
- **Giữ nguyên mọi thứ còn lại** (giọng, độ dài, thumbnail, khuôn title) — đang chạy phép thử, mỗi lượt chỉ đổi 1 biến.

### Việc 3 — đọc kết quả ở video thứ 8 + 7 ngày (~2026-08-25)

`python analytics_report.py --channel shokutaku -n 10` + query `insightTrafficSourceType`.

| Kết quả | Làm gì |
|---|---|
| `BROWSE_FEATURES` > 0 lần đầu | vòi hé → tăng nhịp theo ramp + farm 3–5 góc của đúng món vừa ăn |
| `BROWSE` vẫn 0 | **điều kiện chuyển hướng CHẠM** → dừng cày, mở bàn 3 đường: đổi trục tách khỏi health / mở kênh mới / đóng băng dồn về health |

⚠️ **Không đọc CTR** (impressions quá nhỏ + API bị Google rút metric từ 07-30) · **không đọc view tuyệt đối** (66 view/34 ngày thì vài view là nhiễu).
⚠️ Đây là **phép thử có hạn**. Chạm mốc 8 mà BROWSE vẫn 0 thì **dừng thật**, đừng gia hạn thêm 4 video nữa.

## 🔴 CHIẾN LƯỢC ĐANG CHẠY — "CÁCH 1: cày tiếp, hook trước" (user chốt 2026-08-01)

### Số đo dẫn tới quyết định (đo 2026-08-01, `analytics_report.py`)

| Chỉ số | Giá trị |
|---|---|
| Nguồn traffic 9 video, cả tháng 7 | **BROWSE = 0** · SEARCH = 1 · SUGGESTED = 11 · khác 42 |
| Tổng | 59 view · 1 sub · video mới nhất (07-31) **0 view** |
| Retention ゆで卵 (21 view) | 95,2% @0'17" → **47,6% @0'44"** |
| Retention 腎臓 (11 view) | 54,5% @0'42" → **18,2% @1'45"** |

**Đọc đúng:** `BROWSE = 0` là trạng thái **CẤP KÊNH**, không phải cấp video — YouTube chưa từng đặt kênh này lên trang chủ ai. Nên **CTR (<4%) KHÔNG phải bệnh**: nó đang được tính trên vài chục impressions từ trang kênh + suggested, ở cỡ đó 1 click lệch là nhảy mấy điểm %. Sửa thumbnail lúc này là sửa vào không khí.
**Bệnh đo được:** một nửa khán giả bỏ đi **trước giây 45**. ⚠️ Cỡ mẫu 11–21 view → tín hiệu YẾU về thống kê, nhưng là tín hiệu duy nhất có và nó khớp với browse = 0.
⚠️ **Vòng phản hồi đang ĐỨT:** ở ~10 view/video YouTube còn không trả dữ liệu retention (ブルーベリー 7 view: "chưa có dữ liệu"). Đây mới là cái kẹt thật, không phải CTR.

### Cách 1 = làm gì

1. **Cày tiếp trên kênh hiện tại**, chấp nhận 4–8 tuần mù.
2. **MỌI video mới phải qua gate `python tools\check_coldopen.py`** — không PASS thì KHÔNG render. Đây là phần cốt lõi; thiếu nó thì cách 1 chỉ là bơm thêm mẫu retention xấu vào điểm kênh.
3. Đo ở **48 giờ** và **7 ngày** — nhìn **`BROWSE_FEATURES` có > 0 lần đầu tiên** và **retention @45s**, KHÔNG nhìn view.

### 🔴 ĐIỀU KIỆN CHUYỂN HƯỚNG (viết ra để không trôi)
**Sau 8 video có hook đạt gate mà `BROWSE` vẫn = 0 → dừng, chuyển sang mở kênh MỚI chạy song song** (cách 2). Căn cứ: kênh đối thủ **1 ngày tuổi** đã được phát 38K view, và chính network đó bỏ kênh nghẹt để làm lại từ đầu (`youtube-jp-health/BENCHMARK_RIVALS_2026-07-29.md` §2.7, §9.3).

### ⛔ GATE MÁY CHẠY: `python tools\check_coldopen.py` (khắc 2026-08-01)

```bash
python tools\check_coldopen.py            # quét mọi *_TTS.md
python tools\check_coldopen.py 05 08      # chỉ script chỉ định
python tools\check_coldopen.py --limit 120
```

- Hiệu chuẩn **4,60 ký/giây** (đo thật video 05 đã render: 7.146 ký / 1.557 giây). Trần mặc định **90 giây = 413 ký**.
- **MỐC MÁY ĐỌC: dòng `# ITEM1` ngay trước câu hé lộ mục đầu.** `parse_script()` bỏ qua dòng `#` → không ảnh hưởng giọng đọc lẫn cue slide. **Thiếu mốc = FAIL** (cố ý: bắt người viết tự khai; để tool đoán bằng regex 「〜です。」 thì nó ăn nhầm 「それだけの話です。」 trong hook và báo PASS oan).
- 5 luật: **L1** mục đầu ≤90s · **L2** không câu điều kiện/miễn trừ/dặn dò trong cold open · **L3** persona/tên kênh/都道府県/CTA nằm SAU mục đầu · **L4** case study nằm SAU mục đầu · **L5** ≥3 câu triệu chứng 「〜ませんか」 **riêng lẻ** (khuôn network đối thủ — mỗi câu tự đâm một lần; gộp 3 triệu chứng vào 1 câu hỏi cuối là KHÔNG đạt, lỗi đã dính ở bản đầu của script 05).

**Trạng thái tồn kho (quét 2026-08-01):**

| Script | Mục đầu | Ghi chú |
|---|---|---|
| 05 kyabetsu | ✅ **87 giây** | đã sửa + render lại |
| 06 blueberry-kumiawase | ~6 phút · **case study ngay giây 25** | ⚠️ ĐÃ RENDER chưa đăng → sửa là phải render lại |
| 08 jinzo | **7:42** · checklist 12 câu | chưa render, sửa rẻ. ⚠️ Đề tài 腎臓 = **tạng làm chủ ngữ = rổ ĐÃ CHẾT** (`BENCHMARK_RIVALS` §2.1: 腎臓5選 2,5K view; chính kênh này video 腎臓 được 11 view) → nên **re-angle sang món làm chủ ngữ** chứ không chỉ vá hook |

### ✅ ĐÃ LÀM 2026-08-01 — dọn metadata 4 video LIVE (ưu tiên rail ĐỀ XUẤT, user chốt)

> User: *"Tao muốn kênh ăn được đề xuất cái đã"* → dồn vào tầng metadata (sửa trong Studio/API, **không re-render, đảo lại được**), vì đó là thứ quyết định YouTube xếp video vào RỔ nào để test — chính là rail SUGGESTED, rail duy nhất từng cho kênh này view (11/54).

🔴 **Lỗi nặng nhất tìm được: 2 video MỚI NHẤT đeo tag của video khác.** 「はちみつ」 và 「緑茶」 cùng mở đầu bằng đúng 7 tag: `腎臓 食事 · 腎臓に悪い食べ物 · 60代 健康 · リン 腎臓 · バナナ 腎臓 · 漬物 腎臓 · 田中教授`. Một video mật ong đang khai với thuật toán rằng nó nói về thận/phốt-pho/chuối/dưa muối → **bị test ở sai rổ**. Đây đúng cơ chế đo được 07-21 (cùng 1 video: cạnh rổ アルデヒド xem 10 giây · cạnh rổ cảnh báo xem 96%).
⚠️ `田中教授` = **tên thật một người**, vi phạm luật kênh (cấm tên người/viện) và kéo video vào rổ của người đó.

| Video | Sửa gì | Sau khi sửa |
|---|---|---|
| はちみつ `LvBPBN1Jg4U` | bỏ 7 tag rác + 健康 食事 シニア, thêm bộ nhận diện + tag はちみつ | 26 tag, sạch |
| 緑茶 `ySxrtSzj8Bg` | bỏ 7 tag rác, thêm bộ nhận diện + tag 緑茶/内臓脂肪 | 24 tag, sạch |
| あずき `utNRgxBSf-8` | hashtag đang chiếm **dòng 1** 概要欄 (vùng hook) → đẩy xuống cuối | 871 ký |
| 牛乳 `DD_AED6woII` | 概要欄 chỉ 325 ký, thiếu đoạn topical → viết thêm | 717 ký |

**GIỮ NGUYÊN 100%:** title · thumbnail · categoryId 22 · ngôn ngữ · trạng thái. Không video nào bị re-upload.
→ Giờ **9/9 video** cùng mở đầu bằng `60代 食べてはいけない · 60代 食事 · 60代からの食卓`.
⚠️ **Bẫy khi verify:** YouTube **trả tag về theo thứ tự alphabet**, và độ dài description lệch ±1 ký do chuẩn hoá xuống dòng → so sánh "3 tag đầu" hay "len(desc)" sẽ báo LỖI oan. Phải kiểm bằng *"tag rác còn trong danh sách không"*.
⚠️ **Chưa làm được:** 目次 cho video 牛乳 — `subs.srt` đã bị dọn khi lưu kho nên **không có nguồn timestamp, và KHÔNG bịa**. Muốn có thì phải tải video về đo lại.

### ⏳ Việc còn mở
- ✅ **Nhịp đăng ĐÃ HẠ 2026-08-01 (user chốt): 7/tuần → T2·T3·CN 3/tuần**, giữ 12:00 JST. Đã sửa `upload_pack.py` slots + `.claude/rules/upload-schedule.md` (Mục 0.9 bảng trạng thái, bảng tải-theo-ngày, ghi chú CN, cột Mục 1) + **restart dashboard**.
  - **Điều kiện TĂNG LẠI: `BROWSE_FEATURES` > 0 lần đầu tiên** — không theo cảm giác, không theo view.
  - Tải toàn hệ thống sau khi hạ: T2=3 · T3=2 · T4=1 · T5=2 · T6=3 · T7=0 · CN=1 = **12 video/tuần**.
  - ⚠️ **Hệ quả tức thì:** hôm nay là **T7 — không còn là slot**. Video 05 đang gói sẵn với giờ hẹn cũ (T7 12:00) → `upload_pack` sẽ tự đẩy sang **CN 12:00 JST**. Muốn đăng ngay hôm nay thì ép bằng `--slot "2026-08-01 12:00"`.
- **06 và 08 ĐỂ NGUYÊN** (user chốt 2026-08-01: *"những bản script chưa render video thì để lại đã"*) — ưu tiên rail đề xuất trước. Khi quay lại: 06 sửa hook = phải render lại; 08 nên **re-angle khỏi rổ 腎臓** chứ không chỉ vá hook.
- Đo lại rail sau 48h/7 ngày: `BROWSE_FEATURES` và `RELATED_VIDEO` có nhích khỏi 0/11 không.

## ⚠️ PLAYBOOK SANDBOX (chốt 2026-07-21 — đọc `CHANNEL_OPTIMIZE.md` trước khi viết/đóng gói)

- **Khung CẢNH BÁO là mặc định** cho title (P0 【tag】+ tránh/危険 + giấu đáp án) + thumbnail (v5: 3 dòng HÀNH VI/HẬU QUẢ/ĐÁP ÁN GIẤU, chữ khổng lồ + mũi tên đỏ) — luật `02_THUMBNAIL_TITLE_RULES.md` v5. Format chủ lực: 「X tránh + Y nên」 (4選+4選).
- **Payoff #1 (món đầu) TRƯỚC phút 4** — checklist rút còn 5–6 câu, khối persona みのり + đăng ký dời ra SAU món #1. Open loop lớn trả ở ~80–85%.
- **Nhịp đăng ⭐⭐ T2·T4·T6 — 3 video/tuần — 12:00 JST cố định (= 10:00 VN)** (**ĐỔI NGÀY 2026-08-03**, user chốt nhịp toàn hệ thống *"2 ngày 1 video"*: T2·T3·CN → **T2·T4·T6**, số lượng giữ 3, giờ giữ nguyên. Lý do đổi: T2·T3 cách nhau 1 ngày rồi nghỉ 4 ngày = không phải nhịp 2 ngày; T2·T4·T6 giãn đều 2-2-3. Đánh đổi biết trước: T4 + T6 là 2 ngày median view **bét** của benchmark 長生きの秘訣 (3,2K và 5,5K) — chấp nhận vì kênh đang **BROWSE=0** nên số theo ngày của đối thủ chưa có tác dụng ở đây; ngày mạnh nhất T2 vẫn giữ → **dồn video mạnh nhất vào T2**. Nguồn sự thật: `.claude/rules/upload-schedule.md` Mục 0.9.) ⤵ căn cứ cũ: T2·T3·CN (HẠ 7→3 ngày 2026-08-01, user chốt; giờ trưa giữ nguyên để tách daypart với health) (BẬT LẠI + ĐỔI 2026-07-30, user chốt; kênh vừa ngưng 2 ngày từ 07-28). Nguồn sự thật: `.claude/rules/upload-schedule.md` Mục 0.9 + Mục 1.
  - **Vì sao TRƯA:** user chốt tách daypart — health (cùng tệp senior JP) giữ **tối 19:00**, shokutaku lấy **trưa**, không để 2 kênh cùng tệp đăng chung khung. Căn cứ khung trưa: SocialPilot 12–15h = khung ăn nhì (22%); tiền lệ trong ngách là ご長寿ご健康 đăng **13:00 × 42 video** ở nhịp 7,14/tuần. Không đụng co-dai (11:00 JST).
  - ⚠️ **Nhịp này đi NGƯỢC số đo ngách, user biết và vẫn chọn:** 長生きの秘訣 đăng 3,37/tuần → sụp 45× (median 110K → 2,4K trong 7 tháng); 若返りアカデミア đăng 0,25/tuần (1 video/tháng) → median **141K view/video**. Ở ngách này chưa có tiền lệ nào volume thắng, nên coi đây là **phép thử có phanh**, không phải kết luận đã chứng minh.
  - 🛑 **Phanh:** 3 video liên tiếp <50 view · AVD <25% · bỏ ≥2 slot/tuần vì thiếu hàng → hạ về **T2·T3·CN 3/tuần** (lịch cũ chốt 2026-07-28: median view T2 81,8K > T3 42,7K > CN 32,1K; T4 3,2K + T6 5,5K bét). Thiếu hàng thì bỏ ngày khác trước, giữ T2·T3·CN.
  - ⚠️ 7 slot/tuần = **7 video render + đóng gói/tuần**. Tồn kho lúc bật lại: 2 bản `RENDER ✓` + 2 script = đủ ~2 ngày.

## ⚠️ COLD OPEN — bắt buộc mọi kịch bản (chốt 2026-07-12, từ data retention video trứng: 60% rớt trong 30s đầu, 80% rớt trước phút 4; sống sót qua phút 4 → xem đến hết)

- **Câu 1 = stake** (đúng lời hứa của thumbnail/title, có 「かもしれません」 làm mềm) — KHÔNG mở bằng tả cảnh/chào hỏi.
- **Mục 1 bắt đầu trước giây ~70.** Khối mở chỉ gồm: stake → 2-3 triệu chứng/self-implication → preview trụ cột + open loop → 1 câu xưng danh みのり.
- **Khối persona 「私は医者でも…」+ xin đăng ký → đặt SAU payoff đầu tiên** (cuối trụ 1 / sau checkpoint), không đặt trong 3 phút đầu.
- **Xin comment (都道府県, số 「に」「さん」…) không bao giờ đứng TRƯỚC một cú reveal đã hứa** — đặt sau payoff hoặc gộp vào khối お願い cuối.
- Mẫu áp dụng đầu tiên: `04_SCRIPTS/02_kenko-shokuhin-wana.md` (xem changelog trong header).

## Lớp THỦ CÔNG — `genten`, KHÔNG quay tay (chốt 2026-08-07)

⛔ **`tegami` (quay tay thật) đã được GỠ khỏi clause bắt buộc của kênh này** — `.claude/rules/handmade-layer.md` §3.3. **CẤM xuất bảng 撮影リスト trong script shokutaku.**

✅ Lớp bắt buộc thay thế: **`genten` ≥1 khối trích NGUỒN THẬT / video** — tên cơ quan (厚労省・文科省 成分表・消費者庁・自治体・学会) + **年版 hoặc 時点** + câu số trích đúng. Đây là **việc của Claude khi viết script**, không phải việc của user.
- Khối 原典 **không bắt buộc đọc thành lời** — được phép là **thẻ 出典 trên hình** đặt đúng cue câu đang nói con số đó (nhờ vậy vá được script đã viết xong mà không đụng `_TTS.md`, khỏi synth lại giọng + khỏi quét lại `match` trong SLIDES). Ghi trong 概要欄 thôi thì **KHÔNG tính**.
- ⛔ Gate lớp thủ công ĐÃ BỎ 2026-08-09 (`handmade-layer.md`) — nguồn thật vẫn bắt buộc qua §YMYL, nhưng KHÔNG còn ghi sổ hoãn / bỏ slot / bắt quay.

## Persona — ranh giới cứng

みのり KHÔNG bao giờ tự xưng 医師・先生・管理栄養士・専門家; không nói 「私が診察した患者」「相談を受けた方」; cấm cụm 医師が解説・医師警告 ở kịch bản/tiêu đề/thumbnail. Uy tín = nguồn thật + ngôn ngữ gian bếp + sự chăm chút dành thời gian.

## YMYL (chặt như health)

- **KHÔNG bịa nguồn/số** — lỗi nặng nhất. Nguồn thật giữ nguyên tên (厚労省・日本高血圧学会・国立健康・栄養研究所・久山町研究・SPRINT). Không chắc → hedge 「〜という報告があります」, KHÔNG gắn tên tổ chức.
- Cấm 治る・治す・完治・薬の代わりになる → dùng 守る・支える・整える・〜かもしれません.
- Không khuyên ngừng/đổi/giảm thuốc. Disclaimer cuối video BẮT BUỘC (câu cố định Mục 10). Cảnh báo điều kiện tại chỗ khi chạm nhóm rủi ro (kali × bệnh thận, natto × ワーファリン).
- Disclaimer nặng đặt **cuối**, không nhồi mỗi mục — giết retention.

## Nhân vật anecdote

Tên + tuổi + tỉnh + nghề cũ **mới hoàn toàn mỗi script**, không lặp giữa các video (và chế độ A: khác hẳn nhân vật bản gốc). Luôn mở bằng khung minh họa 「例えば、こんな方がいらっしゃるとします」.

## Voice / render (AivisSpeech)

- **File `_TTS.md`: mỗi dòng = MỘT CÂU, không phải cả đoạn văn.** Tool `video_render.py` lấy mỗi dòng làm 1 cue phụ đề — dòng dài cả đoạn → phụ đề 6–9 dòng tràn nửa màn hình (dính 2026-07-11, video 02). Chuẩn phụ đề: 1–2 dòng (~≤70 ký tự/câu). Nếu lỡ render với TTS mức đoạn → tách `timeline.json` theo câu (snap khoảng lặng voice.wav) rồi `--reuse`, không cần gọi VOICEVOX lại.

- Engine **AivisSpeech**, tốc độ **0.9–0.95** (đọc chậm cho người cao tuổi). Ngôi kể 私 trung tính → đổi model giọng nam/nữ không cần sửa kịch bản.
- **Speaker CHƯA chốt** → lần render đầu: thử 60 giây đầu, chọn giọng ấm hợp みのり, rồi ghi speaker id + hệ số ký-tự/phút thực đo vào đây (giống cách chouhen calibrate). Con số 300–320 ký/phút trong skill là lý thuyết.
- Thêm thuật ngữ hay đọc sai (クレアチニン, tên riêng) vào user dictionary.
- ⭐⭐ **STYLE VISUAL HIỆN HÀNH (user chốt 2026-08-21, từ video 18): MINH HOẠ AI KAWAII pastel TĨNH tuyệt đối, đặt trong KHUNG SÂN KHẤU** — 📌 **lớp DỰNG + HIỆU ỨNG + pipeline lệnh: xem §ĐỊNH DẠNG VIDEO CHUẨN ngay dưới** (mục này chỉ tả lớp HÌNH) (nền gradient + thẻ trắng bo góc + bóng đổ + 2 nhân vật cắt-nền 2 mép + **dải đen** đáy), phụ đề **chữ TRẮNG** trong dải đen.
  - ⭐ **VÒNG 3 cùng ngày** (user đưa ảnh frame health 36: *"thế mày làm cho tao cái khung như này còn đẹp hơn đó"*) — đè canvas trắng trơn của vòng 1–2. Dựng ở `ingest_slides_18.py::stage_canvas`, **gọi lại chính hàm của `_media_library/make_stage.py`** (`stage_base`/`put_cast`/`sub_bar`) nên khung khớp khít health/nenkin và không sinh bộ hằng số thứ hai. Ảnh **cover-crop phủ trọn thẻ, tự lùi về fit khi cắt >12% nội dung** (ca thật `slide_23` bị cắt mất một đĩa táo trong cảnh so sánh). `sub_style` đổi `kuro` → **`outline` + `sub_marginv 12`** (chữ đen chìm hoàn toàn trong dải đen). **Cast RIÊNG của kênh — 12 ảnh** ở `assets/cast/` (`minori_` talk/point/hold/stop/taste/smile · `kikite_` listen/worried/surprised/relieved/note/nod), gen nền **magenta `#FF00FF`** rồi tách bằng `tools/cutout_cast.py` — ⛔ không dùng chung cast health (line-art anime, lệch style pastel; và 2 kênh cùng tệp senior JP sẽ trông như một kênh). 🔴 **Và phải có `POSE_MAP` đổi tư thế theo đoạn bài** — bản đầu 4 tư thế dán một cặp cố định cho cả 82 thẻ, user gọi ngay: *"ít biểu cảm thế thôi à"*; **có 12 ảnh mà dán một cặp thì cũng như có 1 ảnh**. Chi tiết: `04_SCRIPTS/18_ringo-tabekata.md` §9.1.
  - ⤵ Vòng 1–2 (đã đè): minh hoạ trên canvas TRẮNG trơn, phụ đề ĐEN ở dải trắng đáy (`sub_style: "kuro"`). Đo từ mẫu: không ảnh thật, không pan/build-on, ~3–6 đổi hình/phút, nhân vật lặp nhất quán. Thi hành: `build_slides_18.py` (STYLE LOCK + PLAN từng cảnh + prompt FLOW cho user gen) → `ingest_slides_18.py` (cắt ✦ theo LÔ + **trim viền khung + cắt dải trắng/đường kẻ đáy** + pad canvas 1920×1080 trắng, ảnh 1920×890@y0, dải 190px dưới cho sub) → render `--channel shokutaku` (hồ sơ đã đổi `sub_style: "kuro"` — chữ đen viền trắng đáy khung, thêm vào `video_render.py` cùng ngày — + `sub_size 24`, motion False, dissolve 0,45s). Chữ bake trong hình: tối thiểu, nhãn ngắn/chữ số, soi từng ký tự (`media-library.md` §2.9). **Lợi compliance: cartoon không realistic → KHÔNG tick altered/synthetic.** Chi tiết + số đo: `04_SCRIPTS/18_ringo-tabekata.md` §9.
  - 🔴 **BẮT BUỘC trim trước khi pad — `media-library.md` §2.10 ⑧** (user bắt ở vòng 1 video 18: *"sao video nó có khung bao text thế… ảnh nhìn như bị đóng trong 1 cái khung"*). Ảnh gen có **viền khung 1–3px** (82/82) và **đường kẻ ngang + dải trắng đáy** (78/82, trung vị 88px) — trên canvas trắng chúng thành cái khung bao quanh cả vùng phụ đề. Gate máy trong `ingest_slides_18.py` đo **BẬC NHẢY** ở 3 mép (trái/phải/trên), phải ra `✅ 0/82`. ⚠️ Không chữa được từ prompt: chính câu xin "chừa dải trắng ở đáy" sinh ra đường kẻ → cứ xin, rồi cắt ở ingest.
- ⤵ Style CŨ (đến video 17): ~~photo ảnh thật full màn hình + phụ đề outline + make_shot build-on~~ — thay bằng style trên. ⚠️ **KHÔNG stock-clip** vẫn giữ (user chốt 2026-07-23 — đừng gắn `"video": true`).
- **KHÔNG dùng nhân vật AI người dẫn (HeyGen) — user bỏ hẳn 2026-07-25.** Video KHÔNG có footage động nào (không stock-clip, không người AI) → **KHÔNG phải tick "altered/synthetic content"** khi upload; thumbnail AI + giọng TTS đều không cần khai báo (`.claude/rules/youtube-compliance.md` §2).

## 🎬 ĐỊNH DẠNG VIDEO CHUẨN — chốt 2026-08-22 từ video 18 (MỌI video sau làm theo)

> user duyệt demo 30s rồi chốt: *"Hiệu ứng oke rồi"* → *"làm đường B cho tao"* → *"ghi lại định dạng
> mới của video để video tiếp theo sẽ làm theo định dạng này"*.
> **Đây là định dạng MẶC ĐỊNH, không phải phương án.** Video sau **KHÔNG** phải soi lại video gần nhất
> hay hỏi lại — làm theo mục này. Muốn đổi thì user nói, và sửa Ở ĐÂY.

**Ba lớp, ba tool, đừng trộn:**

| lớp | là gì | tool |
|---|---|---|
| **A. NỘI DUNG HÌNH** | 82 minh hoạ AI pastel kawaii nền trắng, TĨNH tuyệt đối, 3 nhân vật cố định | `tools/build_slides_18.py` → prompt FLOW cho user gen |
| **B. KHUNG SÂN KHẤU** | gradient + thẻ trắng bo góc + 2 cast cắt-nền 2 mép + dải đen đáy | `tools/ingest_slides_18.py` (gọi lại hàm của `_media_library/make_stage.py`) |
| **C. DỰNG + HIỆU ỨNG** | wipe · overlay tag/pictogram · phụ đề karaoke | **`remotion-vox`** (đường B) |

### Pipeline 6 bước (video sau chỉ đổi số `18` → số mới)

```
1. py tools\build_slides_18.py                 # PLAN + prompt FLOW  → user gen ảnh
2. py tools\cutout_cast.py                     # chỉ khi bổ sung cast mới (nền magenta #FF00FF)
3. py tools\ingest_slides_18.py                # trim viền + vá ✦ + dán vào khung sân khấu
4. py E:\...\remotion-vox\tools\import_pipeline.py   # nạp slide + voice + srt → project.json
5. py E:\...\remotion-vox\tools\build_overlays_18.py # wipe + overlay + siết phụ đề  ⬅ BƯỚC RIÊNG CỦA KÊNH
6. run_full18.cmd  (chạy NỀN)                  # chunk render → deliver --mp4 → cta_inject
```

⛔ **Bước 4 KHÔNG được bỏ qua bước 5.** `import_pipeline.py` để mặc định `fontSize 48` + không tách cue
dài + không có overlay/wipe → ra video phụ đề tràn dải đen và hình cắt thẳng khô.

### Thông số CHỐT (đo trên video 18, dùng lại nguyên)

| | giá trị | vì sao là số này |
|---|---|---|
| Chuyển cảnh | **wipe tuyến tính 14 frame**, hướng luân phiên `left→up→right→down` | mềm hơn cắt thẳng, không phải dissolve nhoè; 0,47s ≥ mốc 0,4s (`audience-45plus` §2) |
| Motion | **`"none"` tuyệt đối** — không pan, không idle, không wobble/punch | [[feedback_video_no_motion_mot_giong]] |
| Mật độ hình | **4,51 đổi/phút** · entry ngắn nhất 6,2s | trần rule là ≤6 đổi/phút, không entry <6s |
| Phụ đề | `fontSize` **38** px thực · cue **≤46 ký** (`split_long_cues`) · 172 cue | dải đen chỉ **152px** ⇒ 38px mới vừa 2 dòng. ⚠️ **`sub_size: 24` trong `channels.py` là đơn vị ASS, KHÔNG dùng cho Remotion** |
| Overlay | **25 clip** = 1 watermark chạy trọn bài + 15 thẻ chữ + 9 pictogram | pictogram `entrance: peel` / `exit: fade` |
| Watermark | 「60代の食卓」 `#FFD24A`, `(1586, 40)`, size 40, `durationInFrames` = trọn video | xem 🔴 ngay dưới |
| Chỗ đặt overlay | tag `(330, 745)` · pictogram `(56, 148)`, **clamp `H_MAX 320` VÀ `W_MAX 200`** | clamp 1 chiều là chưa đủ — xem 🔴 dưới |
| Render | `--chunk 5000 --concurrency 2 --cache-mb 512` | video 18: **~6 phút**, 32.279 frame, 17′56″, 67,6 MB |

### 🔴 BA THỨ ĐƯỜNG REMOTION **KHÔNG** TỰ LÀM (renderer cũ làm hộ) — nhớ đủ, đừng phát hiện lại

Đây là **cùng một loại lỗi ba lần**, và là lý do video 18 phải render **3 lượt**. Bài học thật:
**đổi đường dựng thì phải đọc HẾT đường cũ trước, đừng dùng render làm công cụ khám phá.**

1. **Watermark kênh** — `video_render.py` dán ở step B. Remotion không biết ⇒ phải tự thêm clip watermark trọn bài (bước 5 đã làm).
2. **CTA overlay giữa video** — `cta-midvideo.md` §5, renderer cũ tự gọi. Đường Remotion phải gọi tay `cta_inject.py --in-place` (đã nằm trong `run_full18.cmd`).
3. **Siết phụ đề** — `video_render.py` tự cắt cue ≤42 ký (`SUB_MAXLEN`); Remotion **không tách gì**, cue dài nhất của bài là **174 ký** ⇒ 3 dòng tràn.

⚠️ **`deliver.py` PHẢI có cờ `--mp4 out\<slug>.mp4`.** Thiếu cờ là nó **render lại cả video từ đầu**
(mất thêm cả lượt) thay vì lấy bản `render_chunks.py` vừa nối.

### 🔴 Ba cái bẫy hình học của overlay (đã dính đủ ba, mỗi cái một lượt duyệt)

Góc trên–phải và góc dưới–phải **đã có chủ**: watermark kênh và timestamp của YouTube
([[feedback_thumbnail_goc_duoi_phai_cua_youtube]]). Overlay chỉ còn nửa trái.

1. Pictogram đè lên **chữ bake trong hình** → dời ra `(56, 148)`, **ngoài thẻ trắng**.
2. Pictogram cao đè lên **mặt nhân vật**: dấu `!` w=93 nên clamp-theo-cao đẩy h lên 321 → thêm `W_MAX`.
3. Pictogram bẹt (`ex_mukumi` 424×320) **đè vào thẻ** → clamp **cả hai chiều** + gate máy đo giao với hộp thẻ.

### ⏳ Việc còn mở
**Card CTA không hiện trên khung** dù `cta_inject.py` báo `DONE` và `CTA_EXIT=0` (soi frame 508,5 / 511 /
512,5 — không thấy card; **tiếng đọc CTA vẫn nguyên**). Giả thuyết: tool dựng cho khung **không có cast 2
mép và không có dải đen bake sẵn**. Video sau: hoặc chẩn đoán lại toạ độ card cho khung sân khấu, hoặc bỏ
lớp hình CTA và giữ lời đọc. **Đừng báo "đã có CTA" chỉ vì exit 0** — đúng bẫy `render-background.md` §2.6.

## Thumbnail + Title

**Luật CTR riêng kênh: `02_THUMBNAIL_TITLE_RULES.md` (Phần D = quy trình v4 DESIGN-FIRST, 2026-07-11)** — **chuẩn kênh user chốt (Phần E): ảnh FULL-BLEED tối moody MỘT ẢNH LIỀN, chủ thể trọn một bên, cột 3 dòng MÓN/TWIST/STAKE kín ~86% chiều cao đè vùng tối bên kia** (mẫu: trứng v23, blueberry v6, jinzo v6 organ-topic). Bắt buộc theo Phần D: **bước 0 "ý chính vào HÌNH"** (video về tạng → hình có tạng, mô hình thật cắt ghép chìm vào cảnh — CẤM sticker いらすとや lên ảnh photo, CẤM panel/collage) + **3 cửa tự duyệt trước khi giao** (che chữ 0,5s ra chủ đề / đặt cạnh mẫu Phần E không khác "kiểu" / 120px). Tool: `tools/compose_thumb_bg.py` (nền: mirror/crop + gradient low-key + cutout ghép) → `tools/make_thumb.py` (chữ). STAKE cụ thể, claim có giới hạn (!?/半分); KHÔNG bác sĩ/áo blouse/ống nghe, KHÔNG claim khỏi bệnh. Skill Mục 15 B–D theo file này.

## Lưu file

- Script → `04_SCRIPTS/<NN>_<slug>.md`, bản đọc `<NN>_<slug>_TTS.md`, đánh số tăng dần.
- Transcript nguồn REMAKE → `01_SOURCES/`.
- Header mỗi script: chế độ (A/B), nguồn nếu REMAKE, độ dài mục tiêu, danh sách nhân vật (không lặp video khác).
- **Ghi thật rồi verify** (Glob/Read) — không báo "đã lưu" khi chưa gọi tool. Xem [[feedback_khong_bao_lao_da_lam]].

> 📦 Doc cũ (diagnosis/optimize/benchmark hết hạn, khuôn đã bị đè) đã dời vào `./_archive/` (dọn 2026-08-24) — đường dẫn cũ trong rules trỏ file nào không thấy ở gốc thì tìm ở đó.
