# CLAUDE.md — youtube-jp-chouhen

Project: kênh faceless **AI朗読 / スカッと系・長編朗読ドラマ (~2 tiếng)** thị trường Nhật.

## Bối cảnh

- **Tên kênh (chốt 2026-07-07): 真夜中の朗読便** — dùng thay `｟チャンネル名｠` ở câu kết NHỊP 9 và watermark thumbnail. (Cùng tên kênh với project youtube-jp-sukatto — 2 dòng format khác nhau chung 1 kênh.)
- Thị trường đích: **Nhật** (geo=JP, hl=ja). Mọi tiêu đề/keyword viết **tiếng Nhật**.
- Khán giả: **nữ 45–70 tuổi**, nghe (không nhìn màn hình), nhất là trước khi ngủ → nhắc lại tên + vai vế nhân vật định kỳ để người nghe lơ đãng 30s vẫn bám truyện.
- **Độ dài: KHÔNG còn là tham số đầu vào (user chốt 2026-08-11: *"cứ dựa vào công thức mà làm, ngắn hay dài đâu quan trọng"*).** Độ dài là **kết quả** của số SÓNG viết ra, theo luật scaling `RETENTION_FORMULA_2026-08-11.md` §2: **dài = 11′ mở bài (CỐ ĐỊNH) + 3,5′ × N sóng + 3′ kết**. N=4 → ~28′ (vùng đã chứng minh: video 12, AVD 51,6%) · N=8 → ~42′ · N=11 → ~52′ · N=13 → ~59′ (trần thực tế). Ký tự: **@260 ký/phút nếu tag dày (>400 tag), @295 nếu tag thưa** — xem khối hệ số bên dưới, ĐỪNG dùng 300. MỘT truyện xuyên suốt, chia batch ~4.500 ký/phần, kết mỗi phần ở cliffhanger; user gõ 「つづき」để nhận phần kế.
  - ⚠️ **Cái giá của bài dài, biết trước:** AVD 33% (ngưỡng mở rail) đòi **8,9 phút xem** ở bài 27′ · **13,4′** ở bài 40′ · **17,2′** ở bài 52′. Kỷ lục kênh là **15,6′** (video 07-17, 54′49). ⇒ bài ≤40′ nằm trong vùng đã làm được; bài 50′+ đòi vượt kỷ lục kênh ~+10%. Viết được theo công thức, nhưng đây là mục tiêu chưa có tiền lệ.
  - 🛑 **Phanh:** 3 video liên tiếp AVD ≤28% → hạ về N=4–5 (~28–31′), đừng cố lần thứ tư.
  - (căn cứ cũ, giữ để tra: chuẩn 30–40′ chốt 2026-07-21 từ mổ xẻ 0-view — cụm kênh nhỏ thắng ngách đăng 26–48′, 60–70′ rơi vùng trũng. Vẫn đúng về xu hướng, nhưng nó là **median bucket đối thủ**; số của CHÍNH kênh cho thấy độ dài chỉ ăn qua AVD% và biến thật là vị trí cú lật đầu theo PHÚT.)
- **Nhịp đăng: ⭐⭐ 4 video/tuần — T2 · T4 · T6 · CN, 09:00 JST cố định** (user chốt **2026-08-14**: *"giãn cách ra"* + chọn bộ ngày này). **HẠ TỪ 7/tuần** (1 video/ngày, chốt 2026-08-03). Giãn **2-2-2-1 ngày** — cách đều nhất mà 4 slot làm được trong 7 ngày. Giờ 09:00 **không đổi**.
  - ✅ Giữ **T2** = ngày mạnh ở CẢ HAI kênh đối thủ (嫁子 median 46,5K cao nhất bảng; 苦しみ hạng nhì). ✅ Bỏ **T7** = median bét của 苦しみ (4,6K).
  - ⚠️ **Nhưng lấy CN** — ngày median bét của 嫁子 (23,7K = **nửa** T2). Đánh đổi có ý thức: 4 ngày cách đều trong 7 ngày thì buộc chạm cuối tuần. Muốn né cả T7 lẫn CN thì phải xuống **3/tuần T2·T4·T6**.
  - ⚠️ **CÁI MẤT:** chouhen là kênh **DUY NHẤT có rail đề xuất mở** và ngách này **volume THẮNG** (嫁子 233K sub đăng 8,75 video/tuần). Cắt 7→4 = **mất 43% số vé/tuần**, đúng lúc `CHANNEL_DIAGNOSIS_2026-08-12.md` kết luận nút thắt là **BAO BÌ + SỐ VÉ**. Đổi lại: 4 video làm tử tế hơn 7 video làm vội.
  - 🛑 **PHANH:** trung vị view/video của 10 video kế **tụt** so với lô 7/tuần trước đó → trả về 7/tuần `[(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9)]`. Ghi vào `08_ANALYTICS_LOG.md`.
  - ⚙️ **Hàm ramp `_chouhen_slots()` ĐÃ XOÁ** — lịch không tự nhảy theo tồn kho, slot nằm thẳng trong `CHANNELS["chouhen"]["slots"]`. ⚠️ **Gate NĂNG LỰC thi hành bằng tay:** không có hàng qua gate thì **BỎ SLOT, không đăng bù** — 4 slot là trần lịch, không phải chỉ tiêu. Nguồn sự thật: `.claude/rules/upload-schedule.md` Mục 0.9 + Mục 1.
  - ⤵ *(trạng thái cũ 2026-08-03 → 08-14, giữ để tra: 7 video/tuần T2–CN 09:00, lấp cả T7+CN dù là 2 ngày median bét, chấp nhận để có nhịp đều 1 video/ngày — theo luật "kênh đang được đề xuất thì 1 ngày 1 video".)*
- (căn cứ cũ, giữ để tra) **5 video/tuần T2–T6, TỰ lên 7/tuần khi buffer ≥5 video render sẵn** (NÂNG 2026-07-28 chiều, user chốt sau khi đo **rail đề xuất ĐÃ MỞ**: video 07-25 (29'03) ăn **227 view với 95/97 view từ `RELATED_VIDEO`**, retention phẳng 34–44% suốt thân bài. Ngách này volume THẮNG — winner 嫁子 233K sub đăng 8,75 video/tuần. ⚙️ Cơ khí: `_chouhen_slots()` trong `tools/upload_pack.py` đếm folder `06_VIDEO` có `.mp4` chưa `--done`. 🛑 **PHANH:** 3 video liên tiếp <50 view · retention mốc 2'54" <30% · bỏ ≥2 slot/tuần → hạ về 3–4/tuần. ⚠️ **Tồn kho đang = 0 và `01_SOURCES` RỖNG → việc gấp nhất là nạp transcript nguồn để REMAKE**, vì cái ăn 227 view là bản remake premise proven-viral. Bằng chứng đầy đủ + ngưỡng: **`CHANNEL_DIAGNOSIS_2026-07-28.md`**. Lịch trước đó: 3 video/tuần T2·T3·T5, NGÀY SỬA 2026-07-28 sáng) — **09:00 JST cố định** (giờ đo thật benchmark 苦しみの物語, khán giả スカッと nghe buổi sáng; giờ KHÔNG đổi). Căn cứ đổi ngày: đo 50 video/kênh → winner ngách 嫁子のスカッと朗読劇場 (233K sub) median view **T2 46,5K ≈ T3 46,3K ≈ T5 44,1K** vs **CN 23,7K bét**; 苦しみの物語 **T7 4,6K bét**. Cả 2 dồn volume vào T7+CN nhưng đó là ngày view kém nhất — cuối tuần là chỗ họ **xả hàng**, không phải chỗ khán giả ăn. Nhịp 3/tuần giữ (SỬA 2026-07-22: giãn từ 1/ngày). Bằng chứng: `.claude/rules/upload-schedule-measure-2026-07-28.md`.
- **Chọn premise: ƯU TIÊN chế độ A·REMAKE từ premise proven-viral** — bằng chứng mổ xẻ 2026-07-21: video duy nhất được phân phối (00, 78 view RELATED_VIDEO) chính là bản remake truyện jikyu1350 nổi tiếng → premise-matching là cửa vào related rail của kênh 0-sub.
- KHÁC youtube-jp-sukatto (45–60 phút) và kênh health (15–20 phút) — **đừng lẫn 3 chuẩn**.

## Voice (AivisSpeech)

- Engine: **AivisSpeech** — API tương thích VOICEVOX, port **10101** (KHÔNG phải VOICEVOX 50021 của kênh health).
- **POV nữ (mặc định — 一人称「私」): morioki** — speaker id `497929760`. Giọng nữ trưởng thành, chất người thật.
- **POV nam (一人称「俺」): 阿井田 茂 — style Calm** — speaker id `1310138977`.
- Speed **1.0** (nhịp tự nhiên; thể loại này đọc chậm + ngắt nghỉ dài + BGM đã tạo cảm giác 朗読).
- License cả 2 model: **ACML 1.0** — thương mại OK, cấm mạo danh/bôi nhọ.
- Credit 概要欄: `AivisSpeech: morioki` hoặc `AivisSpeech: 阿井田茂` tùy giọng.

### 🎙 A/B GIỌNG — thêm giọng của 古代の秘訣 làm nhánh B (user chốt 2026-08-01)

Mục tiêu user: *"thêm giọng của kênh 古代の秘訣 vào giọng kể chuyện của 真夜中の朗読便… test xem cái nào được xem nhiều hơn"*.

| nhánh | engine | speaker | speed | 抑揚 | ghi chú |
|---|---|---|---|---|---|
| **A (đang dùng)** | AivisSpeech :10101 | `morioki` | 1.0 | 1.0 | giọng nữ, POV「私」 |
| **B (mới, CHỐT)** | **VOICEVOX :50021** | **`青山龍星` / ノーマル** | **0.80** | **1.15** | user chốt 2026-08-01: giữ giọng nam, **hạ 0.9 → 0.80** cho bằng nhịp morioki. Hồ sơ gốc co-dai là 0.9 (`youtube-jp-health/tools/channels.py["co-dai"]`) — chouhen cố ý lệch |

**Cơ khí — đổi giọng CHỈ đụng khâu 1, khâu 2 không biết gì:**
```bash
# nhánh B (giọng 古代の秘訣, đã hạ tốc) — thay cho dòng --engine aivis --speaker morioki
python tools/ambient_render.py 03_SCRIPTS/<x>_TTS.md --engine voicevox --speaker 青山龍星 --speed 0.80 --intonation 1.15 --voice-only
python tools/scene_render.py <x>          # y như cũ, ăn voice.wav vừa synth
```
Tên speaker là ký tự Nhật → **gọi qua wrapper `.py`, đừng đưa thẳng qua command line** (bẫy mangle đã ghi ở §Handoff). Wrapper A/B có sẵn: `python tools/run_voiceab.py <file>_TTS.md [A_morioki|B_aoyama|B85_aoyama|B83_aoyama|B80_aoyama]`.

**Đo 5 bản trên cùng cold open video 14 (305 ký), `06_VIDEO/_voice_ab/<arm>/voice.wav`:**

| arm | thời lượng | ký/phút | lệch nhịp vs A |
|---|---|---|---|
| A morioki 1.0 | 70,4 s | 260 | — |
| B 青山龍星 **0.90** | 64,9 s | 282 | **−7,9% (nhanh hơn)** |
| B 青山龍星 0.85 | 67,6 s | 271 | −4,1% |
| B 青山龍星 0.83 | 68,6 s | 267 | −2,6% |
| **B 青山龍星 0.80 ⭐ CHỐT** | **70,7 s** | **259** | **+0,4% — trùng nhịp morioki** |

⚠️ **0.80 là SÀN, không hạ tiếp** (`audience-45plus.md` §5.2: hạ nữa thì méo tiếng + phình độ dài). Ở 0.80 nhịp đọc bằng đúng morioki nên **hệ số độ dài của kênh giữ nguyên ~296–303 ký/phút** — không phải tính lại chuẩn script. (Con số 259–282 ký/phút ở bảng trên thấp hơn hệ số kênh vì đoạn demo toàn thoại ngắn + nhiều tag `[間]`; chỉ dùng cột **lệch %** để so, đừng dùng cột tuyệt đối để ước độ dài video.)

⚠️ **License: nhánh B PHẢI ghi credit `VOICEVOX:青山龍星` trong 概要欄** (điều khoản VOICEVOX). Ngoại lệ "không ghi credit" của co-dai là quyết định riêng kênh đó, **không bê sang chouhen** — chouhen là kênh đã đậu audit API, giữ nếp compliance.

⚠️ **Lệch giọng ↔ POV — nghe demo rồi quyết:** 青山龍星 là giọng nam trầm kiểu phim tài liệu, mà truyện chouhen mặc định POV nữ 「私」. Nghe `B_aoyama/voice.wav` (nó đọc đúng đoạn POV nữ) trước khi khoá. Nếu thấy chối thì nhánh B nên đi kèm kịch bản **POV nam 「俺」** — nhưng lúc đó POV thành biến thứ hai, phải ghi vào sổ đo.

### 🔴 ĐỌC KẾT QUẢ A/B GIỌNG BẰNG GÌ — KHÔNG PHẢI VIEW

**Giọng không thể tác động tới view một cách trực tiếp** — người xem không nghe được giọng trước khi bấm. Chuỗi nhân quả duy nhất là: giọng → **retention** → rail đề xuất mở → view. Nên:

1. **Metric chính = AVD% và retention tại mốc 2′54″** (cửa tử đã đo của kênh, `CHANNEL_DIAGNOSIS_2026-07-28.md`). Ngưỡng đang dùng: AVD ≥33% rail mở · ≤24% đóng.
2. **View là chỉ số TRỄ và bẩn** — nó ăn theo thumbnail/title/ngày đăng/premise. So view của 2 video khác truyện rồi kết luận về giọng là kết luận sai.
3. **Tối thiểu 3 video/nhánh, đăng xen kẽ** (A-B-A-B-A-B), cùng dải 29–32′, cùng khuôn thumbnail, cùng slot 09:00. Kênh này dao động 3–227 view/video → 1 video/nhánh là **nhiễu thuần tuý**, đọc ra số cũng không có nghĩa.
4. Ghi sổ mỗi tập: `slug · nhánh · AVD% · retention@2′54″ · view 72h` vào `06_VIDEO/_voice_ab/AB_LOG.md`.

📌 **Video kế tiếp (15) chạy nhánh B.** Ghi dòng `VOICE ARM: B (VOICEVOX 青山龍星 0.9/1.15)` vào header script + mục Đóng gói CTR để `upload_pack` và người render không dùng nhầm morioki.

## ⚠️ Hệ số ô C — CALIBRATE độ dài (BẮT BUỘC đo thật)

Engine mặc định **150 ký tự/phút** (chuẩn thể loại: đọc chậm + ngắt nghỉ dài + BGM, dải 140–160). **Con số này CHƯA đo trên giọng thật của kênh này** → lần render đầu tiên phải:
1. Render thử 1 phần (~4.500 ký) bằng morioki @ speed 1.0.
2. Đo phút thực tế → tính hệ số thật (ký tự ÷ phút).
3. Ghi hệ số đó vào đây và dùng cho các bài sau (điền vào ô C khi gọi skill).

> **Hệ số thực đo được (video 01, 2026-07-07): ≈ 303 ký tự/phút** — morioki @ speed 1.0, gap 0.5s / section-gap 1.1s. 19.597 ký tự → 64.7 phút. (Gần sukatto 323; các pause chỉ hạ nhẹ. Con số 150 trong master CHỈ là lý thuyết, KHÔNG đúng với giọng này.)
>
> ✅ **CHỐT (SỬA 2026-07-21): chuẩn kênh = 30–40 phút** (~9–12k ký tự) — đổi từ 60–70' sau mổ xẻ 0-view (cùng công sức ra gấp đôi video = gấp đôi lượt thuật toán test; khớp cụm thời lượng kênh nhỏ đang thắng). Video 00–06 đã đăng theo chuẩn cũ, không re-render. Muốn 60–70'/2h là trường hợp đặc biệt user chỉ định.
>
> 🔴🔴 **SỬA HỆ SỐ 2026-08-10 — 303 LÀ SỐ CỦA BÀI KHÔNG TAG. Bài có tag nhấn nhá thì hệ số là ~258–266.**
> Con số 303 đo trên **video 01 (2026-07-07)** — thời điểm đó kịch bản **chưa có lớp tag `速/抑揚/間`** (lớp đó mới bắt buộc từ `humanize-script-voice.md`, 2026-07-29). Mỗi `[間]`/`[後間]` cộng thêm im lặng mà **không cộng ký tự**, nên hệ số tụt. Ba mốc đo thật:
>
> | video | ký | render thật | ký/phút | tag / 1000 ký | ghi chú |
> |---|---|---|---|---|---|
> | 01 (07-07) | 19.597 | 64′42″ | **303** | ~0 | không tag |
> | **23 (08-11)** | **16.574** | **59′22″** | **279** | **9,4** | 155 tag |
> | 21 (08-09) | 9.349 | 35′06″ | **266** | 32,7 | 306 tag |
> | **22 (08-10)** | **9.296** | **36′01″** | **258** | 44,5 | **414 tag** |
>
> ⭐ **Số video 23 lấp khoảng trống và xác nhận quan hệ là ĐƠN ĐIỆU theo MẬT ĐỘ tag, không theo số tag tuyệt đối:** 0 → 303 · 9,4 → 279 · 32,7 → 266 · 44,5 → 258. ⇒ **ước hệ số bằng mật độ tag/1000 ký**, đừng ước bằng tổng số tag (bài 59′ có 155 tag vẫn chạy 279 vì nó dài; bài 35′ có 306 tag tụt về 266).
>
> 🔴🔴 **PHỦ ĐỊNH TÍNH ĐƠN ĐIỆU — số video 25 (2026-08-13, đo thật sau khâu voice):** 14.950 ký ·
> 308 tag · mật độ **20,6 /1000** → render ra **57′25** ⇒ hệ số thật **261 ký/phút**.
>
> | mật độ tag /1000 ký | 0 | 9,4 | **20,6** | 32,7 | 44,5 |
> |---|---|---|---|---|---|
> | ký/phút đo thật | 303 | 279 | **261** | 266 | 258 |
>
> **20,6 → 261 THẤP HƠN cả 32,7 → 266** ⇒ quan hệ **không đơn điệu**, và công thức `303 − 1,0 ×
> (tag/1000)` ước sai **+8,4%** ở bài này (đoán 282, thật 261). Bài nhắm 52′ ra **57′25**.
> ⇒ **Mật độ tag KHÔNG phải biến duy nhất.** Nghi phạm: bài 25 dùng rất nhiều `[間0.8]`/`[後間1.0]`
> (nghỉ dài) trong khi bài 21/22 phần lớn là `[間0.4]` — tức **tổng GIÂY im lặng** mới là biến thật,
> không phải **số** tag. Chưa đo được vì chưa có tool cộng giá trị tag.
> ⇒ **Cho tới khi đo được: ước bằng 260 ký/phút cho mọi bài có tag** (mốc thấp nhất quan sát được),
> và **coi độ dài là ±8% cho tới khi có `voice.wav`**. Muốn đúng phút mục tiêu thì đo `ffprobe` sau
> khâu voice rồi mới chốt, đừng chốt bằng con số ước.
> 🔴🔴 **ĐỌC MỤC 27 Ở CUỐI KHỐI NÀY TRƯỚC — công thức dưới đây ĐÃ BỊ OVERFIT, sai số thật là ±3–4%, không phải <1%.**
>
> ✅ **VIỆC ĐÓ ĐÃ LÀM XONG (2026-08-16, lúc viết video 27) — có công thức, ~~lệch <1% ở 4/5 video~~.**
> Tool: **`tools/calib_duration.py`** (cộng giây `間+後間`, fit bình phương tối thiểu trên các video đã có
> độ dài render thật). Fit trên 21 · 22 · 23 · 25 · 26:
>
> ```
> thời lượng(giây) = 0,1613 × ký  +  1,662 × (tổng giây 間+後間)  +  0,772 × số nhịp đọc
> ```
>
> | video | thật | mô hình | lệch |
> |---|---|---|---|
> | 21 | 35′06 | 34′13 | −2,5% |
> | 22 | 36′01 | 36′10 | **+0,4%** |
> | 23 | 59′22 | 59′54 | +0,9% |
> | 25 | 57′25 | 57′00 | −0,7% |
> | 26 | 43′19 | 43′41 | +0,8% |
>
> 🔴 **Ba điều nó nói ra, quan trọng hơn con số:**
> 1. **Tốc độ đọc THUẦN ≈ 372 ký/phút.** Mọi hệ số 258–303 ở bảng trên **không phải tốc độ đọc** — chúng
>    là tốc độ đã **pha loãng bởi im lặng**. Đó chính là lời giải cho nghịch lý video 25 (20,6/1000 →
>    261, thấp hơn cả 32,7/1000 → 266): **mật độ đếm SỐ tag, còn cái ăn thời lượng là GIÁ TRỊ tag.**
>    `[間1.2]` và `[間0.4]` đếm như nhau nhưng tốn gấp ba. Bài 25 dùng nhiều `[間0.8]`/`[後間1.0]`, đúng
>    như nghi ngờ đã ghi ở đoạn trên — nay đo được, không còn là nghi ngờ.
> 2. **Mỗi giây `[間]` khai báo tốn ~1,66 giây thật** — renderer cộng nghỉ của tag **lên trên** nghỉ sẵn
>    có, không thay thế.
> 3. ⭐ **Mỗi nhịp đọc tốn thêm ~0,77 giây gap** ⇒ **cách TÁCH DÒNG cũng là một biến độ dài**: cùng một
>    bài, tách nhỏ hơn thì video dài hơn. Trước nay chưa ai tính biến này.
>
> ⇒ **Từ nay ước độ dài bằng `calib_duration.py`, đừng ước bằng ký/hệ số.** Hệ số 260 vẫn dùng được để
> ước thô lúc đang viết prose (chưa có `_TTS.md`), nhưng khi đã có lớp tag thì chạy tool.
> ⚠️ Vẫn là **ước** — sau khâu voice vẫn phải `ffprobe voice.wav`; lệch >3% thì thêm video mới vào
> `cases` trong tool rồi fit lại.
> 📌 Ca dùng thật đầu tiên (video 27): bản dựng đầu rải `[間0.6]` vào đầu **mọi khối** (~130 chỗ) →
> 422 tag, mật độ **52,6/1000 = cao nhất lịch sử kênh**, 222 giây im lặng ⇒ mô hình cho **34′03**, vọt
> khỏi dải 25–32′. Bỏ lớp tự động, giữ nguyên 85 tag viết tay ⇒ 179 tag ⇒ **30′00**, **không cắt một chữ
> prose nào**. Bài học: **tag rải đều không phải nhấn nhá, nó là filler** — và nó ăn thời lượng thật.
> *(Bài học đó vẫn đúng; cái sai là ĐỘ CHÍNH XÁC của con số, không phải chiều của hiệu ứng — xem ngay dưới.)*
>
> ### 🔴 27 — ĐIỂM DỮ LIỆU ĐỘC LẬP ĐẦU TIÊN, VÀ NÓ NÓI MÔ HÌNH BỊ OVERFIT (2026-08-16, đo sau khâu voice)
>
> `voice.wav` video 27 = **3.176,4 s = 52′56**. Mô hình (fit trên 5 video, **không** có 27) ước **50′47**
> ⇒ **lệch −4,1%**, trong khi trên chính 5 video đã fit nó lệch −2,5% … +0,9%.
>
> ⚠️ **Vì sao 5 video kia đẹp: 5 điểm dữ liệu cho 3 tham số thì fit khít là chuyện đương nhiên, không phải
> bằng chứng.** Con số "<1%" là **sai số HUẤN LUYỆN**, đã bị trình bày nhầm thành sai số dự báo.
>
> **Giả thuyết đã thử và BÁC BỎ:** nghi `ambient_render` có hai loại nghỉ (`--gap 0.5` giữa hai dòng trong
> khối · `--section-gap 1.1` ở dòng trống) mà mô hình 3 biến gộp thành một, và video 27 gần như mỗi nhịp
> một khối (**86%** khối/nhịp, so với 66–99% ở bộ cũ). Tách thành **4 biến** cho hệ số **section-gap
> 0,852 s/khối · gap 0,584 s/dòng** — rất gần giá trị cấu hình thật, tức mô hình 4 biến **đúng về cơ chế**.
> **Nhưng video 27 vẫn lệch −3,0%.** ⇒ tỉ lệ section-gap **không phải** nguyên nhân; nguyên nhân còn lại
> chưa biết. (Fit lại với đủ 6 video: `0,1607 × ký + 1,721 × pause + 0,852 × khối + 0,584 × dòng-trong-khối`.)
>
> ⇒ **CÁCH DÙNG ĐÚNG TỪ NAY: coi nó là công cụ ±4%, không phải ±1%.**
> - Nhắm một **DẢI** (vd 50–60′) thì dùng tốt. Nhắm **đúng một con số** thì không dùng được.
> - Vẫn hơn hẳn hệ số ký/phút (sai +8,4% ở video 25), và vẫn bắt được lỗi lớn — nó chặn đúng **hai lần**
>   ở video 27 (bản 34′ do tag filler · bản thiếu mốc 50′), **cả hai trước khi render**.
> - 🔴 **Chốt độ dài CHỈ bằng `ffprobe voice.wav`.** Đừng ghi con số ước vào header như số chốt — đã dính
>   ở chính video 27 (header ghi 50′47, thật 52′56).
>
> 📐 Công thức xấp xỉ dùng được: `ký/phút ≈ 303 − 1,0 × (tag/1000 ký)`. Kiểm: 9,4 → 294 (thật 279, lệch −5%) · 32,7 → 270 (thật 266) · 44,5 → 259 (thật 258). Sai số lớn nhất ở dải mật độ thấp vì blank-ratio cũng ăn vào (video 23 ratio 0,66).
>
> ⇒ **Khi ước độ dài lúc viết, dùng 260 ký/phút, KHÔNG dùng 300.** Muốn video 30′ thì viết **~7.800 ký**, không phải 9.000. Bài nào tag dày (>400) thì lấy 255. Sai số của việc dùng 303 là **+16%** — đủ để một bài nhắm 30′ ra 35′, tức tự đẩy mình lên mép trần và hạ AVD% (mẫu số của AVD% là độ dài).
> 📌 Bảng ngân sách ký tự 9 nhịp trong skill `script-chouhen` MỤC 10 vẫn ghi theo hệ số 300 → **nhân 0,86 nếu muốn đúng phút mục tiêu.**
>
> ✅ **XÁC NHẬN BẰNG SỐ (2026-07-26):** video 08 (**29'03"**, premise サレ妻/即離婚) ăn **107 view trong <48h** — trong khi video 07 (52') và 05 (55') đăng liền trước, **cùng slot 09:00 JST + cùng title tag-đầu + đã backfill metadata**, chỉ được 4 và 2 view. Biến ăn = **độ dài + premise-matching**, không phải giờ đăng. Đo ngách 14 ngày (48 video top của kênh <3.000 sub): **≤32′ view TB 19.585 · >40′ view TB 13.140**, 5 video velocity cao nhất đều 23–29′.

## ⚠️⚠️ LUẬT PHÚT — CỬA GIÂY 60 **VÀ** CỬA PHÚT 12 (chốt 2026-08-11, đè "LUẬT 2 PHÚT ĐẦU")

> 🔴🔴 **ĐỌC TRƯỚC (2026-08-12): CÔNG THỨC NÀY GIỮ NGUYÊN, NHƯNG NÓ **KHÔNG** LÀ THỨ QUYẾT ĐỊNH VIEW.**
> Nó **đã chạy đúng** — AVD lên **49,7 / 49,8 / 53,1%** ở video 08-03 / 08-04 / 08-09 — và 3 video đó
> ăn đúng **2 / 2 / 5 view**, trong khi hit 367 view chỉ có AVD 32,2%.
> ⇒ **Ngưỡng "AVD ≥33% → rail mở" (`CHANNEL_DIAGNOSIS_2026-08-01.md` §1.1) đã bị phủ định — BỎ.**
> Công thức 12 số giữ chân **người ĐÃ vào**; nó **không kéo người vào**. Nút thắt view nằm ở **BAO BÌ**
> (title + thumbnail) và **SỐ VÉ** — xem `CHANNEL_DIAGNOSIS_2026-08-12.md`.
> ⚠️ **Đừng bỏ công thức** (AVD 50% là tài sản thật), nhưng **đừng đổ thêm công vào nó** để chữa view.
> 📌 Bài học chung: cả hai lần đặt ngưỡng sai đều là **lấy tương quan nội bộ kênh trên mẫu <20 video
> rồi dựng thành nhân quả**. Muốn đặt ngưỡng thì phải có mẫu NGOÀI kênh, hoặc chờ biến đó đổi mà kết
> quả đổi theo.

🔴 **ĐƠN VỊ LÀ PHÚT, KHÔNG PHẢI PHẦN TRĂM.** Nguồn sự thật đầy đủ: **`RETENTION_FORMULA_2026-08-11.md`** (Analytics API, 9 video, curve 20 mốc). Gate máy: `python tools/check_retention.py <slug>`.

**Bằng chứng chia đôi sạch 6/6, không ngoại lệ** — retention ở quãng phút 11 → phút 16:

| video | dài | AVD | phút xem | @~11′ | @~16′ | Δ | cú lật đầu |
|---|---|---|---|---|---|---|---|
| **12** | 27′34 | **51,6%** | **14,2′** | 52% | **59%** | **+7,0** | **11′41** |
| **09** | 40′42 | 32,0% | 13,0′ | 40,8% | 42,5% | +1,7 | 15′52 |
| 07-17 | 54′49 | 28,9% | **15,6′** | **45%** | **30%** | **−15,0** | ❌ không có |
| 07-22 | 51′48 | 16,1% | 8,1′ | 23,8% | 19,1% | −4,7 | ❌ không có |
| 07-19 | 67′03 | 18,2% | 12,0′ | 18,8% | 12,5% | −6,3 | ❌ không có |

**Cú lật đầu trước phút 16 → Δ dương. Không có → Δ âm.** Video 07-17 giữ **45% ở phút 11** (cao hơn cả video 09) rồi **mất 15 điểm trong 5 phút** vì không có gì xảy ra ⇒ 6 video 50′+ chết vì **cấu trúc**, không vì độ dài.

🔴 **Vì sao khung 9 nhịp tính theo % làm chết long-form:** NHỊP 5 (thác trả thù) ở 46–51% thời lượng ⇒ bài 27′ rơi phút 12–14 (**trúng cửa**), bài 55′ rơi phút 25–28 (**trễ 16 phút**). Cùng một khung, hai kết quả trái ngược.

⭐⭐ **LUẬT SCALING — mở bài ĐÓNG BĂNG 11 phút, dài thêm thì cộng SÓNG:**
```
Độ dài  =  11′ (mở bài, CỐ ĐỊNH)  +  3,5′ × N sóng  +  3′ (kết)
```
Bài 52′ cần **11 SÓNG**, không phải một thác dài hơn. (Gap giữa các sóng của video 12: **3,0 / 3,7 / 3,6 / 3,1 phút** — số của bản thắng.) Mỗi sóng = **một người/tổ chức trả giá**, đánh số 逆転Ⓝ.

**Cửa cứng (4 số chặn render):**
- **R3b — giây 16–35 phải có ĐÚNG 0 câu LỜI KỂ ≥25 ký.** ⭐⭐ **Cửa tử thật.** Retention 1%: video 12 giây 16 = **96,7%** → giây 33 = **73,0%**; video 09 giây 24 = **100,6%** → giây 48 = **57,6%**. Gần như không ai bỏ đi trong 16 giây đầu ⇒ **toàn bộ cú giết gói trong ~17 giây**, mất nhiều điểm hơn cả 26 phút còn lại. Câu giết video 09 ở **giây 32**: 「床の耐荷重から換気の位置まで、私が二年かけて決めた部屋だった」 — lời kể giải thích, còn câu đòn tới giây 39 mới nổ.
- **R7 — gap giữa 2 beat ≤2′45″.** MỌI hố retention của video 09 nằm trong một gap ≥3′26″ (5 chỗ, khớp 5/5).
- **R8 — SÓNG 1 (cú lật đầu) ≤ phút 12** tuyệt đối.
- **R11 — loop cold open đóng ở ≥78% thời lượng** (video 12 = 80%; video 09 đốt ở 39% → mất đuôi).

⭐ **Câu phản đòn KÉO NGƯỜI QUAY LẠI, không chỉ giữ:** video 12 hồi **+3,3đ** ở giây 82 ngay sau 「ありがとうございます、お義母さん」 (giây 71).

### ⭐⭐ NHẮM AVD >60% → `dài = 8′ + 3,5′×N + 2′30` (24–26′)

**Bỏ HẲN khối 回想** (đòn mạnh nhất, rẻ nhất): nó dài 2′20 và nằm đúng vùng trũng (retention 59→55%). Bỏ đi ⇒ 27′34 → **25′14**, giữ nguyên 15,34′ xem ⇒ **60,8%** — vượt 60% **mà không cần giữ người giỏi hơn một giây**. Kèm: SÓNG 1 về **phút 7–8** · anomaly ≤giây 20 · phản đòn ~giây 50.

🔴 **>60% và bài 50′+ LOẠI TRỪ NHAU:** AVD 60% đòi **15,0′ xem ở bài 25′** (kênh đã làm được — video 12 ngày 1 = 15,34′) nhưng **31,2′ ở bài 52′** = 2× kỷ lục kênh ⇒ ngoài tầm. Muốn >60% thì phải về **24–27′**.
📌 Video 12 đạt **55,7% ở NGÀY 1** (83 view); 51,6% là lifetime bị traffic nhỏ giọt kéo xuống ⇒ khoảng cách thật tới 60% chỉ **4,3 điểm**.
⚠️ Hai mục tiêu này **KHÔNG chặn** (回想=0 · sóng 1 ≤8′) vì video 12 vi phạm cả hai mà vẫn thắng — chặn ở mức mục tiêu là fail chính bản thắng (bài học R11: đặt 85% → fail video 12 → hạ về 78%).

**Cold open đo bằng GIÂY** (60s đầu của cả 18 video đều tải 265–345 ký ⇒ ngân sách ký KHÔNG phải chỗ khác nhau): giấy tờ gọi tên **giây ≤10** · anomaly người nghe tự soi **giây ≤25** · 「三つのことを知らなかった」+ liệt kê 一つ/二つ/三つ **giây ≤60** · chính diện phản đòn **giây ≤80**.
⚠️ Device 「まだ知らなかった」 có ở **15/18 video** ⇒ **có device không phải lợi thế, VỊ TRÍ mới là lợi thế.**

- **回想: ≤2′30″ và xong TRƯỚC phút 11** (video 12 = 2′20 · video 09 = 4′01 và nằm đúng vùng đáy). Luật cũ "không trước mốc 20%" ở bài 55′ đẩy nó tới phút 11 — vẫn được, nhưng phải xong kịp cho SÓNG 1.
- Trọn mở bài **CẤM** lời chào / lai lịch nhân vật / tả cảnh dài.
- Luật đầy đủ + checklist: skill `script-chouhen` MỤC 10 (NHỊP 1) + MỤC 14 điểm 1b.

<details><summary>(ĐÃ ĐÈ 2026-08-11) LUẬT 2 PHÚT ĐẦU — chốt 2026-07-26</summary>

Retention video 00 (API, 30 ngày): watch-ratio **1.00 tại mốc 1% → 0.36 tại mốc 6%** (≈2'40" của bản 44′) → rồi **phẳng 0.30–0.35 suốt phần còn lại**. relativeRetentionPerformance **0.48 đầu bài** nhưng **0.85–0.89 giữa bài**. → Thân truyện giữ người TỐT; kênh mất ~65% khán giả trong ~2 phút đầu.

- Trọn NHỊP 1 (600–700 ký ≈ 2 phút @300 ký/phút) phải cháy xung đột liên tục; bắt buộc **2 forward-tease**.
- Khối flashback NHỊP 3 **không bắt đầu trước mốc ~20%** thời lượng.

⚠️ Vẫn đúng về hướng (mất người ở đầu bài) nhưng **sai đơn vị**: nó suy từ MỘT video và tính theo %. Số 9 video cho thấy cửa tử là **giây 60** cho cold open **và phút 12** cho cú lật đầu — và mốc % là thứ đã giết cả 6 video 50′+.

</details>

## Quy tắc số trong kịch bản

- Thân kịch bản: TOÀN BỘ số bằng **漢数字** (五千万円・二十六年・午前十時・三日後). Không chữ số Ả Rập, không ký hiệu ％/㎞.
- Ngoại lệ: **tiêu đề video + text thumbnail** ĐƯỢC dùng số Ả Rập (không qua TTS, bắt mắt hơn).

## ⭐⭐ HÌNH NỀN: "VIDEO NHƯ NÀO CŨNG ĐƯỢC" — ĐỪNG ĐỐT THÊM LƯỢT RENDER VÌ HÌNH (user chốt 2026-08-08)

> user, sau khi tao render lại **3 lượt** cho video 20 vì lỗi hình nền: *"sau kênh này thì video như nào cũng được nhé"*.

**Đây là kênh NGHE.** Moat của nó là **giọng + văn** (`handmade-layer.md` §2 đã chốt từ 2026-07-27); hình nền chỉ là lớp đệm. Ba lượt render của video 20 tốn ~90 phút máy để chữa: ① 13 cảnh đen trơn ② 1 clip lộ mặt người ③ vài clip lệch tông. **Không cái nào trong đó đáng giá 30 phút render lại.**

### Từ nay THI HÀNH thế nào

| | |
|---|---|
| ✅ **GIỮ** (tự động, tốn ~0) | `check_bg_lum.py` (2 phút, chặn video trông như hỏng) · bất biến "cảnh lặp không kề nhau" (đã nằm trong `_spread_all`) · fetch clip MỚI mỗi video + sổ `rejected/` (đây là **compliance**, chống inauthentic content §1 — KHÔNG được bỏ) · nguồn free-thương-mại |
| ✅ **GIỮ, 1 lần duy nhất** | 1 contact sheet duyệt mắt **trước** render. Thấy gì chối thì loại luôn lượt đó |
| ⛔ **BỎ** | Duyệt nhiều frame/clip · soi lại toàn pool · **và nhất là: RENDER LẠI vì hình**. Clip lộ mặt / lệch tông / hơi tối mà đã render xong rồi → **CHO QUA, đăng luôn** |

🔴 **Lằn ranh duy nhất còn bắt render lại: video HỎNG THẬT** — mất tiếng, phụ đề lệch, thiếu part, exit code khác 0, thời lượng không khớp `subs.srt`. Đó là lỗi kỹ thuật, không phải thẩm mỹ.

### ⭐⭐ BỘ 20 CLIP / KHÔNG NGƯỜI / LẶP CÁCH ≥4 CẢNH — chốt 2026-08-16 (user)

> user: *"Không cần check video đâu nhé. Chỉ cần không có người là được, không cần quá nhiều video chỉ cần tầm 20 cái rồi lặp đi lặp lại. Nhưng video lặp lại phải cách nhau 3-4 video nhé."*

Đây là **bản thi hành cụ thể** của khối "video như nào cũng được" ở trên, và nó **đóng lại** phần tốn công nhất của khâu hình: fetch 200–230 clip mỗi video rồi duyệt contact sheet.

| | trước (video 26) | **từ video 27** |
|---|---|---|
| số clip mỗi video | fetch **2 lô = 231 clip**, loại 36 bằng mắt | **20 clip**, chọn bằng máy |
| duyệt mắt contact sheet | bắt buộc 1 lần | ⛔ **BỎ** |
| ràng buộc còn lại | mặt người · brand · tông màu · độ sáng | **CHỈ CÒN: không có người** |
| khoảng cách lặp | "không kề nhau" (`_spread_all`) | **≥4 cảnh, có gate máy** |

**Tool: `tools/pick_bg20.py`** (viết 2026-08-16 cùng lượt).

```bash
python tools/pick_bg20.py --slug <slug> -n 20 --per-theme 2     # chọn → 06_VIDEO/<slug>/bg_list.txt
python tools/scene_render.py <slug> --stage segs --plan-only --bg-only 06_VIDEO/<slug>/bg_list.txt
python tools/pick_bg20.py --slug <slug> --verify --min-gap 4    # GATE: đọc _render_plan.json
```

🔴 **Vì sao "không có người" phải bảo đảm BẰNG MÁY, và cơ chế của nó có giới hạn gì:** `INDEX.json`
của kho có `queries`/`tags` **RỖNG** với hầu hết clip chouhen — không lọc theo metadata được. Nhưng
**tên file CHÍNH LÀ query slug của Pexels** (`old-wooden-beam-text_4102353.mp4`) nên lọc theo từ trong
tên file. ⚠️ Đây là lọc **theo chủ đề đã đặt hàng**, KHÔNG phải nhận diện người trong hình — clip lọt
lưới vẫn có thể có người ở hậu cảnh. **Đó là cái giá đã chọn khi bỏ duyệt mắt**, đừng ngạc nhiên khi gặp.

🔴 **BA LỖ ĐÃ BỊT khi viết tool, mỗi lỗ bắt được bằng một lượt chạy thật:**
1. **Tên file bị CẮT CỤT ở 20 ký tự** ⇒ token cuối hay đứt giữa chừng: `cold-water-h` gần như chắc là
   `cold-water-hands`. Khớp nguyên token là cho lọt ⇒ **token cuối chỉ cần là TIỀN TỐ của một từ trong
   `PERSON` là loại**. Riêng vá này đưa số clip bị loại từ **99 → 320**.
2. **Đồ MẶC TRÊN NGƯỜI = có người trong khung** (`snow-on-coat`) → thêm coat/jacket/scarf/shoe/apron/
   kimono… vào `PERSON`.
3. **Động tác BẮT BUỘC có bàn tay** (`chopping-veg`, `dishwashing`) và **ảnh chụp trong khung**
   (`old-photogra` — ảnh cũ gần như luôn có mặt người) → cùng vào `PERSON`.

⭐ **`--seed` MẶC ĐỊNH = SỐ VIDEO trong slug** — thứ giữ cho luật này không đâm vào compliance. Nếu mọi
video rút cùng một bộ 20 thì đó **đúng profile "lặp NGUYÊN BỘ visual giống video trước"** mà
`youtube-compliance.md` §1 quét (kênh 朗読 nền loop + giọng AI đã bị enforce 01/2026). Seed theo số tập
⇒ mỗi video rút một bộ khác từ **~500 ứng viên sạch**. Đo thật: video 28 trùng **2/20** clip với 27,
video 29 trùng **3/20**. ⛔ **Đừng hardcode `--seed`**, và đừng copy `bg_list.txt` từ video khác.

⚙️ **Khoảng cách lặp ≥4 cảnh gần như tự đạt** — `_spread_all()` (vá 2026-08-08) rải đều trên TOÀN
chuỗi: 20 clip trên ~180 cảnh ⇒ khoảng cách tự nhiên ~20 cảnh, cao gấp 5 lần ngưỡng. Gate `--verify`
là để bắt ca **pool hụt** (clip quá ngắn, ít take) chứ không phải để bắt lỗi thường ngày.

⚠️ **Đây là NGOẠI LỆ của `media-library.md` §2** (*"làm video nào tải ảnh và video của video đó thôi"*,
chốt 2026-07-29) — **chỉ cho chouhen**, vì kênh này là kênh NGHE, moat nằm ở giọng + văn
(`handmade-layer.md` §3). ⛔ **Không suy rộng sang kênh THÔNG TIN** (health/co-dai/shokutaku/nenkin…) —
ở đó hình mang thông tin và §2.0 (*hình đầu tiên phải là chủ đề*) vẫn nguyên.

📌 **Cái mất, ghi thẳng:** clip **lệch nội dung truyện** giờ không ai chặn nữa. Video 16 từng phải cắt
lại vì clip tái dùng mang theo **đồ đạc của truyện khác** (két sắt, sóng biển trong truyện không có
biển). Lọc theo chủ đề trong `THEMES` giảm bớt, nhưng **không loại trừ** — và theo đúng lệnh
*"không cần check video"*, gặp thì **cho qua, không render lại**.

⚠️ **Cái đánh đổi, ghi thẳng:** sẽ có video lọt clip có mặt người hoặc lệch tông. User biết và chấp nhận. Đừng "cẩn thận giúp" rồi tự render lại — làm vậy là đi ngược lệnh này.

📌 Suy rộng hợp lý cho kênh NGHE khác (`kr-romfan`): áp cùng tinh thần. Kênh THÔNG TIN (health/co-dai/shokutaku/nenkin…) thì **KHÔNG** — ở đó hình mang thông tin, luật `media-library.md` §2.0 giữ nguyên.

## Visual video — CHUẨN MỚI kiểu kr-romfan (user chốt 2026-07-12, THAY chuẩn ambient+ảnh tĩnh 2026-07-10)

Visual mỗi video = **chuỗi cảnh nền luân phiên** (`tools/scene_render.py`): mỗi cảnh 1 asset từ `06_VIDEO/_bg/`, phủ tối nhẹ + vignette, chuyển cảnh crossfade 0.9s, phụ đề glass + BGM -40dB. Chống flag inauthentic "nền loop + giọng AI" (enforce 01/2026).

### ⭐⭐ KHUNG "RADIO ĐÊM KHUYA" — `--frame radio` LÀ CHUẨN MẶC ĐỊNH của kênh (chốt 2026-08-22)

> 🔴 **ĐÃ CHUYỂN TỪ "PILOT A/B" SANG BẮT BUỘC, đọc trước khi render bất kỳ video mới nào.**
> User: *"tao tưởng chốt làm video dạng như này rồi mà"* (video 33, `bunke-no-asa`) — bản render
> đầu tiên bị làm theo `--frame none` vì tool copy khuôn wrapper `.cmd` từ video 25 (viết TRƯỚC
> khi khung radio ra đời) mà quên tự thêm cờ `--frame radio`. Từ nay: **mọi lệnh
> `scene_render.py <slug> --stage segs` cho kênh này PHẢI có `--frame radio`**, trừ khi user nói
> rõ muốn khung cũ. Khi viết wrapper `.cmd` mới, **chép khuôn từ video ≥29** (đã dùng radio),
> đừng chép từ video ≤28 (khuôn `none` cũ).

Học từ format đối thủ (video uWTUB9BIWfk user đưa — cùng ngách スカッと, 2h03): hàng trên =
**typing-cam loop** (góc trái, 705×352) + **player UI + avatar tròn** (`frame_static.png`) +
**cột sóng showfreqs sinh THẬT từ voice.wav**; phụ đề đổi sang **chữ XANH #48AAFF viền đen,
FontSize 48, outline không hộp** (`SUB_STYLE_RADIO` — user chọn bản outline, đúng
`audience-45plus.md` §3.1). Khung này khớp brand 真夜中の朗読便 (bàn làm việc nửa đêm + radio).

```bash
python tools/make_radio_frame.py assets     # 1 lần: player UI + avatar + frame_static.png (đã có, khỏi chạy lại)
python tools/scene_render.py <slug> --stage segs --frame radio   # BẮT BUỘC từ 2026-08-22, mặc định code vẫn "none"
```

- **Asset cố định kênh** ở `06_VIDEO/_radio_frame/`: `typing_loop.mp4` (Pexels 27601321, 71s
  1080p, không mặt người — là logo động, KHÔNG thuộc pool `_bg`, không đụng luật cấm tái dùng) ·
  `frame_static.png` (player UI + avatar Pexels 31169640 crop tròn — ảnh stock nên **không
  phải tick altered/synthetic**) · layout ghi hằng ở `make_radio_frame.py` + `RADIO_*` trong
  `scene_render.py`. Đổi avatar/UI → chạy lại `assets`; part tự dựng lại (mtime check).
- **Cờ `--frame` ghi vào `_render_plan.json` ở stage segs** (một nguồn sự thật) — đổi khung
  thì phải chạy lại `--stage segs`, không chỉ parts.
- **`wave.mp4` pre-render ở stage segs** (per-video, theo voice.wav; ghi `.tmp` rồi rename —
  gãy giữa đường không để lại file rác). Part slice bằng `-ss/-t`.
- 🔴 **BẪY ĐÃ ĐO (2026-08-20), đừng làm lại:** ① đưa `showfreqs` **thẳng** vào filtergraph của
  stage_part (trộn nhánh audio→video với các nhánh video) → ffmpeg phình **7 GB RAM** rồi chết
  `Cannot allocate memory`; showfreqs đứng một mình thì sạch → phải tách thành pass `wave.mp4`
  riêng ② kích thước wave phải **CHẴN** (545 lẻ → libx264 "Could not open encoder") ③ FontSize
  60 làm câu kể ≥34 ký wrap 3 dòng khổng lồ **đè player UI** → chốt 48.
- **Dùng cho MỌI video mới từ 2026-08-22** (đã qua giai đoạn pilot A/B) + là skin tự nhiên cho
  dòng まとめ/総集編 >60′ (`audience-45plus.md` §4.1, việc 6.8 còn mở). Video cũ đã đăng (≤28,
  và 30–32 nếu đã lên sóng trước khi phát hiện thiếu cờ) giữ `--frame none` — không re-render
  chỉ vì thẩm mỹ, theo `render-background.md` §1 mục 3.
- 🔴 **DÒNG TTS >55 KÝ SẼ WRAP ≥4 DÒNG PHỦ LÊN KHUNG TRÊN** (bắt ở video 29, frame CTA:
  câu CTA canonical 74 ký → 5 dòng đè cả typing cam). Kịch bản chạy khung radio: giữ dòng
  TTS ≤40 ký như nếp cũ, và **tách câu CTA giữa video thành 2–3 dòng TTS** (vẫn đọc liền,
  chỉ đổi chỗ xuống dòng — nhớ sync `match` FX nếu có). Video 29 giữ nguyên theo luật
  "không render lại vì thẩm mỹ" — chỉ ~8 giây quanh CTA.

### ⭐ v3 — BỎ BOOMERANG, 2 chế độ `--motion` (user chốt 2026-07-28)

User xem bản render: *"video cứ quay ngược quay xuôi nhìn rất khó chịu"*. Nguyên nhân: v2 chỉ lấy **8 giây đầu** mỗi clip → ghép **xuôi + ngược** thành 16s → `-stream_loop` cho đủ **~95 giây/cảnh** ⇒ cùng một cảnh chạy tới-lui **~6 lần liên tiếp**. Bản `scene_render_v2_boomerang_backup.py` giữ lại để tra cứu.

| `--motion` | Cảnh trông thế nào | Pool | Dùng khi |
|---|---|---|---|
| **`clip` (MẶC ĐỊNH)** | Mỗi cảnh = clip chạy **TRỌN MỘT LẦN XUÔI**, hết clip thì hoà tan sang clip khác. Độ dài cảnh = độ dài clip (trần `--scene-max` 20s, sàn `--scene-min` 6s); clip dài bị cắt thành nhiều **take** khác nhau (0–20s, 20–40s…) nên tái xuất hiện cũng là **đoạn khác**, không phát lại y hệt. Không reverse, không loop. | `06_VIDEO/_bg/*.mp4` | mặc định mọi video |
| **`photo`** | **100% ảnh tĩnh**, mỗi ảnh `--photo-sec` (mặc định 16s) rồi hoà tan. Không pan, không zoom (user ghét Ken Burns). | `06_VIDEO/_bgphotos/` — `python tools/fetch_bg.py --photos --per-query 12 "<query>"…` | muốn tuyệt đối tĩnh / pool clip hụt |
| ~~`boomerang`~~ | kiểu v2 xuôi-ngược | `_bg/` | **KHÔNG dùng** — chỉ để re-render video cũ cho khớp |

### 🔁 ASSET LẶP LẠI THÌ ĐẢO THỨ TỰ, KHÔNG ĐỂ KỀ NHAU (user chốt 2026-08-04)

User: *"Nếu hình ảnh và video lặp lại thì đảo nó đi nhé, không được để nó cạnh nhau."*

Trước đó cả 2 chế độ rút asset bằng `items[i % len(items)]` → hết một vòng thì **phát lại đúng trình tự cũ**, nghe/nhìn 2 vòng là nhận ra vòng lặp. Đã thay bằng **`cycle_shuffled()`** trong `scene_render.py`:
- mỗi vòng mới **shuffle** (seed = slug + số vòng → render lại/resume ra **y hệt**, không phá `render-background.md` §2.5);
- **chặn kề nhau**: phần tử đầu vòng mới ≠ phần tử cuối vòng trước (hoán với phần tử kế trong cùng vòng);
- áp cho **cả `plan_scenes_clip` và `plan_scenes_photo`**.
- Log giờ nói rõ: `✓ N cảnh, KHÔNG cảnh nào phát lại (M take trong pool)` hoặc `⚠️ pool hết hàng: X/N cảnh là đoạn phát lại — đã ĐẢO thứ tự (K vòng) và chặn kề nhau`. **Đọc dòng này sau mỗi lần render.**

#### 🔴 VÁ 2026-08-08 — bản 08-04 chỉ chặn kề nhau ở ĐÚNG MỘT CHỖ (bug thật, đã đo)

Bản `cycle_shuffled` cũ chặn trùng **chỉ ở ranh giới vòng** (phần tử đầu vòng mới vs phần tử cuối vòng trước), rồi `shuffle()` toàn bộ phần còn lại → **hai take của CÙNG một clip vẫn rơi cạnh nhau ở GIỮA vòng**. Mô phỏng đúng cấu hình video 20 (15 clip × 3 take, 113 cảnh, 3 vòng) ra **1 chỗ dính ở vị trí 78**. Càng ít clip / càng nhiều vòng thì càng dính nhiều — mà "ít clip, lặp nhiều" chính là kiểu dựng user chốt 2026-08-08 (*"Kiếm khoảng 15 video rồi lặp đi lặp lại thôi… 1 cảnh lặp lại không được ở cạnh nhau"*).

**Đã thay bằng `_spread_all()` — và phải sửa BA lần mới đúng. Ghi cả ba để không ai đi lại đường cũ:**

| # | cách làm | kề nhau | khoảng cách lặp |
|---|---|---|---|
| gốc 08-04 | chặn ở ranh giới vòng + `shuffle()` phần còn lại | **1 chỗ** (cảnh 78) | — |
| sửa 1 | greedy "lấy nhóm nhiều phần tử nhất" | 0 ✅ | ❌ **18/114 lần lặp cách <2 phút**, gần nhất 4 cảnh |
| sửa 2 | round-robin theo lớp | 0 ✅ | ❌ **tệ hơn** — gần nhất 2 cảnh, 24/116 dưới 2 phút |
| **sửa 3 ⭐ đang dùng** | **rải theo BƯỚC ĐỀU trên TOÀN chuỗi, bỏ hẳn khái niệm vòng** | **0** ✅ | ✅ **0 gap <2 phút**; gap clip min 8 / trung vị 21, **gap cùng-một-đoạn min 21 (5,5 phút)** |

- **Gốc của cả hai lần hỏng là CHIA THEO VÒNG** — mối nối giữa hai vòng luôn dồn cùng một nhóm clip lại gần nhau. Bản cuối tính `N` = tổng số slot cả bài, mỗi clip có `c` bản thì đặt ở các mốc cách đều `N/c` (lệch pha ngẫu nhiên theo clip) rồi sắp toàn chuỗi theo mốc → khoảng cách lặp đều **ở mọi chỗ**, kể cả chỗ trước đây là mối nối.
- Thêm một tầng nữa **bên trong một clip**: các ĐOẠN khác nhau của cùng clip được đan xen (đoạn A, đoạn B, đoạn A…) nên hai lần phát lại **y hệt một đoạn** cách nhau gấp đôi. Không có bước này thì shuffle hay xếp 2 bản cùng đoạn sát nhau (đo được: 2 lần `snow-falling@20s` cách nhau 9 cảnh).
- **Verify bằng máy, 9 cấu hình** kể cả ca cực đoan **2 clip / 40 cảnh**: **0 chỗ kề nhau** ở tất cả, và `cycle_shuffled(...)==cycle_shuffled(...)` → vẫn deterministic nên **không phá resume** (`render-background.md` §2.5).

#### 🔴 VÁ kèm — cảnh CUỐI 1,9 giây (cùng lượt 2026-08-08)

Nhánh "cắt cảnh cuối cho vừa khít" có sàn `XF + 1.0` = **1,9 giây**, nên bài nào chia không chẵn cũng kết thúc bằng một cảnh chớp 1,9s — **đúng vào câu chữ ký đóng bài**, và vi phạm `audience-45plus.md` §2 mục 2 (*không entry nào <6 giây*). Đo ở video 20: đúng 1,9s. Đã sửa: cảnh cuối <`--scene-min` thì **gộp vào cảnh trước** (giữ nguyên tổng thời lượng; hết footage thì bật `loop`). Video vẫn dài hơn voice ~1s nhưng bước mux cuối dùng `-shortest` nên cắt đúng — đó là hành vi có sẵn, không phải lỗi mới.

#### 🎬 `--bg-only` / `--bg-limit` — khoá pool về đúng bộ clip của MỘT video (2026-08-08)

`pool_files` mặc định trả **cả `_bg/` (hiện 320+ clip)** → không kiểm soát được video ăn clip nào (đây cũng là gốc của ca video 09 và video 16 trong khối cảnh báo phía dưới). Hai cờ mới:

```bash
--bg-only 06_VIDEO/<slug>/bg_list.txt   # file 1 dòng 1 tên clip — KHOÁ đúng bộ đó (thắng --bg-limit)
--bg-limit 15                            # lấy 15 clip đầu của thứ tự đã ưu tiên-chưa-dùng
```
`--bg-only` **thoát ngay với lỗi** nếu có tên không nằm trong pool (hoặc đã bị đẩy vào `rejected/`) — nên nó cũng là gate chống việc clip đã loại lẻn lại vào bản render. Không truyền cờ nào = hành vi cũ, **không đụng video đã có**.

- Hệ quả: video 35′ giờ có **~110–130 cảnh** (v2: 22), tức mỗi video "ăn" nhiều clip hơn hẳn → luật tái dùng của `media-library.md` càng quan trọng, và phải **fetch_bg query MỚI thường xuyên hơn**. Tool tự cảnh báo khi pool hết hàng và phải phát lại đoạn cũ.
- Timeline chia thành **nhiều part** (≤22 cảnh / ≤12 phút mỗi part), mỗi part 1 ffmpeg ngắn + resumable (part nào có file `v_p<N>.mp4` rồi thì skip) — thay cơ chế nửa A/B của v2. Mối nối giữa 2 part là **hard-cut** (không xfade), như cũ.

> ⚠️ **CHÍNH SÁCH BỘ CLIP (SỬA 2026-07-16 — theo `.claude/rules/media-library.md`, thay luật cấm trùng cứng 2026-07-12):** ƯU TIÊN mỗi video một bộ clip khác nhau; **được tái dùng lẻ khi cần** (không còn cấm), chỉ cấm lặp NGUYÊN BỘ giống hệt video trước. `scene_render.py` giữ nguyên: đọc `_bg/USAGE.log`, ưu tiên clip chưa dùng, thiếu tái dùng kèm cảnh báo; bản chính thức tự ghi log, bản `_test` không tính. → **Trước MỖI video mới: chạy `python tools/fetch_bg.py "<query>"…` gom đủ ~35 clip chưa dùng — tool tự CHECK KHO CHUNG `Projects/_media_library` trước (hardlink, 0 tải), thiếu mới tải Pexels và nhập kho** (mood đêm khuya trầm: mưa cửa sổ, nến, trăng, tuyết, sương núi, phố đêm bokeh, vườn Nhật, tách trà, lò sưởi…).
>
> Duyệt clip BẰNG MẮT trước render (trích frame giữa mỗi clip, ghép contact sheet): loại clip có người nhận diện được, brand/chữ thương hiệu, màu rực phá mood (đã loại: đàn koi cam, đèn lễ hội Tanabata, người ngồi bàn hút thuốc — 2026-07-12, nằm trong `_bg/rejected/`).
>
> 🔴🔴 **DUYỆT 1 FRAME GIỮA CLIP LÀ KHÔNG ĐỦ — BÀI HỌC VIDEO 20 (2026-08-08), phát hiện SAU khi đã render xong 32 phút.**
> Contact sheet lấy **1 frame ở giữa clip**. `morning-sunl_15671645.mp4` đo ở giữa ra **sáng 54,9/255** → duyệt PASS bằng cả mắt lẫn máy. Nhưng renderer **cắt clip thành TAKE** (0–20s và 20–27,6s) và đúng hai đoạn đó tối, cộng lớp `eq brightness -0.08` + vignette ⇒ bản render có **13 cảnh là Ô ĐEN TRƠN chỉ có phụ đề**, tức **10% thời lượng video không nhìn thấy gì**.
> ⇒ **Gate máy mới: `python tools/check_bg_lum.py <slug> --bg-only <file>`** — đo **từng take, 3 mốc (đầu/giữa/cuối)**, và tiêu chí chính là **ĐỘ TƯƠNG PHẢN (stddev), không phải độ sáng**:
> · mean thấp + std **cao** = tối nhưng có điểm sáng (đèn lồng, nến) → **GIỮ**, đúng mood kênh (`japanese-pap`: sáng 8,2 / tương phản 28,7 — PASS)
> · std **thấp** = phẳng lì, không có gì để xem → **LOẠI**, bất kể sáng hay tối (`morning-sunl` đen trơn; `sunlight-on` sáng 80 mà tương phản 11,5 — cùng FAIL)
> Chạy gate này **TRƯỚC** `--stage segs`, cùng lượt với duyệt contact sheet. Sàn mặc định `--min-std 12` hiệu chỉnh từ đúng 2 ca thật ở trên.
>
> 🚨 **DUYỆT ĐÚNG CHỖ — BÀI HỌC VIDEO 09 (2026-07-26). Duyệt clip MỚI TẢI là KHÔNG ĐỦ.** `scene_render` chọn 26 clip từ TOÀN BỘ pool `_bg` (200+ clip), nên clip cũ chưa từng được soi vẫn lọt vào bản render. Bản render đầu của video 09 có cảnh **2 người áo blouse trắng, mặt nhận diện rõ, phòng thí nghiệm phương Tây** ở phút 10 → phải render lại từ đầu (~50 phút máy).
> **Quy trình BẮT BUỘC từ nay:**
> 1. `python tools/fetch_bg.py …` → `python tools/clip_sheet.py new --minutes 60 -o 06_VIDEO/<slug>/_sheet_new.jpg` → duyệt clip MỚI TẢI → loại.
> 2. ⭐ **`scene_render <slug> --stage segs --plan-only`** (cờ mới 2026-08-03) → lập kế hoạch + ghi `06_VIDEO/<slug>/_picks.json` rồi **DỪNG, CHƯA cắt segment nào** → `python tools/clip_sheet.py picks <slug> -o 06_VIDEO/<slug>/_sheet_picks.jpg` → duyệt bộ ĐƯỢC CHỌN bằng mắt. **Đây mới là vòng chặn thật** (renderer chọn từ CẢ pool, gồm clip cũ chưa ai soi).
> 3. Có clip trượt → chuyển vào `_bg/rejected/` + xoá bản trong `_bg/` (hardlink nên phải xoá cả 2) + **xoá dòng của slug trong `_bg/USAGE.log`** (nếu segs đã ghi) → chạy lại bước 2.
> 4. Sạch rồi chạy `--stage segs` (bỏ `--plan-only`, cắt một lần) → `--stage parts` → `--stage final`.
>
> 🔴 **VÌ SAO CÓ `--plan-only` (user bắt lỗi 2026-08-03: *"sao k duyệt clip trước khi render đi"*).** Trước đó `_render_plan.json` chỉ được ghi ở **CUỐI** stage segs → phải cắt xong 153 segment (~18 phút) mới biết renderer chọn clip nào. Ca gốc video 16: duyệt bộ chọn ra **13 clip phải loại, TẤT CẢ đều là clip TÁI DÙNG của video 13/14/15** — két sắt + băng cassette (đồ của video 15), sóng biển + cảng cá (video 13 クルーズ, truyện 16 không có một giọt biển), đan len + bánh mì (video 14), hoa cẩm tú cầu hồng rực (mùa mưa tháng 6, truyện là đầu thu) → phải cắt lại từ đầu. **Bài học tổng quát: clip tái dùng mang theo ĐỒ ĐẠC của truyện khác — nó không chỉ là "lặp hình", nó là hình SAI NỘI DUNG.** Và vòng duyệt phải đứng TRƯỚC mọi thao tác đắt tiền, không phải sau.
>
> 🚨 **Clip đã loại TỪNG TỰ QUAY LẠI POOL** (bug đã vá 2026-07-26): `fetch_bg` hardlink từ kho chung `_media_library` mà kho không ghi nhận "đã bị loại" → tên đã loại xuất hiện lại trong `_bg`. Phát hiện **5 clip đã loại đang nằm trong pool**, trong đó `6392245.mp4` **đã lên sóng ở video 08** (không sửa được, video đã đăng). Đã vá 2 tool: `scene_render.py` lọc mọi tên có trong `_bg/rejected/` khi chọn clip; `fetch_bg.py` không kéo lại từ kho và không tải lại clip/`source_id` đã bị loại. Cả 2 in ra số clip bị bỏ qua để kiểm.

Format cũ (1 nền ambient lặp + 20–25 ảnh SCENES tĩnh theo nhịp — `ambient_render.py` full pipeline + `<x>_SCENES.json` + `fetch_scene_photos.py`) vẫn dùng được làm phương án dự phòng/hybrid; video 00–02 đã đăng theo format đó, KHÔNG re-render lại.

- **Nguồn CC0 / free thương mại (không cần credit):**
  - **Pixabay Videos** (pixabay.com/videos) — Pixabay License, dùng thương mại free, KHÔNG cần ghi nguồn. Ưu tiên.
  - **Pexels Videos** (pexels.com/videos) — free thương mại, không bắt buộc credit.
  - **Mixkit / Coverr** — free, đọc kỹ license từng clip.
  - ⚠️ Tránh clip "royalty-free" trên các site bán/stock có điều khoản attribution; tránh tải lại từ YouTube.
- **Tiêu chí clip:** chuyển động chậm–êm (nước chảy đều, không cắt cảnh), tông tối/trầm hợp đêm khuya, 1080p+, loop mượt (đầu–cuối không giật). Clip 10–30s là đủ (loop lại).
- **Cách loop cho đủ 2 tiếng (ffmpeg):** `-stream_loop -1 -i loop.mp4` rồi cắt theo độ dài audio (`-shortest`), hoặc dựng qua skill `video-render`. Có thể phủ thêm gradient tối + vignette cho dễ đọc phụ đề.
- Lưu clip nền dùng chung: `06_VIDEO/_bg/` + ghi license/nguồn vào `06_VIDEO/_bg/SOURCES.md`.

## Thư mục & lưu file

- Transcript nguồn để REMAKE + log đề tài: `01_SOURCES/`
- Kịch bản sạch: `03_SCRIPTS/<NN>_<slug>.md` — bản đọc: `03_SCRIPTS/<NN>_<slug>_TTS.md`
- Header mỗi script ghi: chế độ (A/B), nguồn (nếu REMAKE), độ dài mục tiêu, danh sách nhân vật (KHÔNG lặp video khác), fiction disclaimer.

## Handoff → video (pipeline v3, chốt 2026-07-28 — clip chạy trọn xuôi + xfade; BỎ boomerang)

Xong `_TTS.md`:

> ```
> cd Projects/youtube-jp-chouhen
> # ⭐ Khâu 0 — PREFETCH TTS SONG SONG (chốt 2026-08-04): nút cổ chai của cả pipeline là TTS,
> #   không phải ffmpeg. Đo thật: synth tuần tự 3,46 s/câu → 734 câu ≈ 42 phút; 4 luồng còn
> #   2,14 s/câu = nhanh 1,61× (~26 phút). Tool chỉ ĐỔ CACHE `Projects/_tts_cache` rồi khâu 1
> #   đọc lại từ đĩa. KHÔNG sửa tts_render.py (tool dùng chung 7 kênh) nên không đụng kênh khác.
> python tools/tts_prefetch.py 03_SCRIPTS/<x>_TTS.md --engine voicevox --speaker 青山龍星 --speed 0.80 --intonation 1.15 --jobs 4
> # Khâu 1 — synth giọng (AivisSpeech chạy sẵn: E:\AivisSpeech\AivisSpeech-Engine\run.exe, port 10101)
> python tools/ambient_render.py 03_SCRIPTS/<x>_TTS.md --engine aivis --speaker morioki --speed 1.0 --voice-only
> # Khâu 2 — dựng video: mỗi cảnh 1 clip chạy TRỌN 1 LẦN XUÔI + xfade 0.9s + phụ đề glass + BGM -40dB
> python tools/scene_render.py <x>                 # = --motion clip, chạy segs→parts→final
> python tools/scene_render.py <x> --motion photo  # bản ảnh tĩnh 100% (pool _bgphotos/)
> ```
> Output: `06_VIDEO/<x>/<x>.mp4`. Chỉ đổi visual → chạy lại khâu 2 (voice.wav + subs.srt giữ nguyên).
> **Tự dọn rác (chốt 2026-07-17):** stage `final` render CHÍNH THỨC xong sẽ TỰ xoá file trung gian (`_seg/`, `_bm/`, `_cta/`, `v_p*.mp4`, `video_final.mp4`, `audio.m4a`, `subs_p*.srt`, `vlist.txt`, `_render_plan.json`) — mỗi video 60′ tiết kiệm ~4 GB, chỉ giữ `<slug>.mp4` + `subs.srt` + `voice.wav`. Cần giữ để debug/re-render biến thể → thêm `--keep-tmp`. Bản `--suffix` (test) KHÔNG bị dọn. `cta_inject.py` cũng tự xoá `_cta/` (tắt bằng `--keep-tmp`).
> **CTA overlay (2026-07-15):** stage `final` TỰ ghép hiệu ứng CTA giữa video (card 4 nút + SFX, rule `.claude/rules/cta-midvideo.md` §5) — tự tìm câu CTA trong subs.srt, chỉ re-encode đoạn đó; script chưa có câu CTA → tự skip; tắt bằng `--no-cta`. Tools: `gen_cta_overlay.py` / `gen_cta_sfx.py` / `cta_inject.py` (kênh khác gọi cta_inject bằng đường dẫn tuyệt đối, `--lang kr/vn` đổi chữ nút).
>
> ⚠️ **Render qua Claude / máy tự KILL ffmpeg chạy >~24' (sự cố 2026-07-14):** chạy khâu 2 THEO STAGE, mỗi ffmpeg <15' + resumable (skip file đã xong), qua wrapper `.cmd` detached:
> ```
> python tools/scene_render.py <x> --stage segs    # cắt segment từng cảnh + _render_plan.json
> python tools/scene_render.py <x> --stage parts   # ghép LẦN LƯỢT mọi part (skip part đã xong)
> python tools/scene_render.py <x> --stage parts --part 3   # ghép đúng 1 part
> python tools/scene_render.py <x> --stage final   # audio(voice+BGM) + concat part + mux + CTA
> ```
> Wrapper mẫu `tools/run_stage06.cmd %1` (copy đổi slug cho video mới) launch qua `Start-Process cmd /c ... -WindowStyle Hidden` (KHÔNG kèm `-RedirectStandardOutput/-Error` → param đó làm child chết non; wrapper tự redirect `> log 2>&1`). Mỗi part ≤12′ timeline nên mỗi ffmpeg ngắn; part nào bị kill thì chạy lại `--stage parts` (part đã có file thì skip). ⚠️ `--stage A`/`B` vẫn nhận (= part 0/1) cho wrapper cũ, nhưng v3 có nhiều hơn 2 part → **dùng `--stage parts`**. Nếu stage final fail → USAGE.log KHÔNG được ghi, ghi tay `<date>\t<slug>\t<clip,clip,...>`.
> Speaker có ký tự Nhật → gọi qua wrapper .py, đừng đưa non-ASCII qua command line `Start-Process` (bị mangle).
> Trước MỖI video: v3 ăn nhiều asset hơn v2 → gom **càng nhiều clip chưa dùng càng tốt** (video 35′ ≈ 110–130 cảnh; clip dài 40–60s cấp được 2–3 cảnh) — fetch_bg tự lấy từ kho chung trước, thiếu mới tải; thiếu nữa thì tái dùng được kèm cảnh báo (rule `media-library.md`).

- **Phụ đề (BẮT BUỘC, mọi video):** style glass (hộp đen mờ, chữ trắng Yu Gothic, sát đáy — hard-code `SUB_STYLE` trong `scene_render.py`). ⭐ **CỠ CHỮ 28 (user chốt 2026-08-03: "script ở video phải to để U45 còn dễ nhìn").** Trước đó **17** — vi phạm `.claude/rules/audience-45plus.md` §3 mục 1 (sàn ≥22 mọi kênh JP); chouhen bị bỏ sót vì nó dùng renderer RIÊNG, không đi qua `channels.py` như health/co-dai/shokutaku nên lệnh siết cỡ chữ 2026-07-30 chưa bao giờ tới nó. Đo thật: 17 → dòng 38 ký chỉ chiếm ~1/3 bề ngang khung; 28 → ~55% và tự xuống 2 dòng (đúng luật ≤2 dòng/khối). Nền hộp đục thêm (alpha 0x90→0x40), MarginV 16→30. Bằng chứng: `06_VIDEO/16_yuinou-no-sneaker/_sub_compare_phone.png`. Sync từng câu từ `_TTS.md` (1 dòng = 1 phụ đề). Kiểm sau render: trích 2 frame cách ~6s → phụ đề phải đổi theo lời.
- **Voice:** `--engine aivis --speaker morioki --speed 1.0` (POV nam → `--speaker "阿井田 茂"`). `--speaker` nhận TÊN, không phải id số.
- **BGM:** `06_VIDEO/bgm/Anguish.mp3`, gain -40dB (mặc định của `scene_render.py`).

## 🔊 Lớp FX radio-drama — ⛔ HẠ XUỐNG TUỲ CHỌN 2026-08-12 (trước là mặc định)

> **user chốt 2026-08-12** khi cắt chi phí/video: bỏ **FX.json viết tay** + **khai ambience bed**.
> Lý do: hai lớp này tốn công NGƯỜI nhiều nhất trong cả pipeline, và **chưa có một số nào chứng minh
> chúng ăn view** — trong khi 10 video gần nhất có đủ FX vẫn 0–17 view.

| lớp | trạng thái từ 2026-08-12 |
|---|---|
| `<slug>_FX.json` viết tay (SFX + card + phụ đề màu) | ⛔ **BỎ** — không có FX.json thì `scene_render` chạy y như cũ |
| khai `ambience` bed trong FX.json | ⛔ **BỎ** |
| **`--bgm auto` (vòng xoay 7 track)** | ✅ **GIỮ** — tự động, chi phí người = 0 |
| CTA overlay (`cta_inject`, stage `final`) | ✅ **GIỮ** — tự động |

⚠️ **Cái mất, biết trước:** FX + ambience là lớp chống "inauthentic content" **bằng TAI**, và kênh
朗読 giọng AI + nền loop là **đúng profile YouTube quét** (`youtube-compliance.md` §1). Giữ
`--bgm auto` bù được một phần (nhạc mỗi video một khác), nhưng rủi ro tăng **thật**. Đây là đánh đổi
đã chọn, không phải chỗ bị bỏ sót.

📌 Muốn bật lại cho một video đặc biệt thì cứ viết FX.json như cũ — toàn bộ cơ khí dưới đây còn nguyên.

<details><summary>Cơ khí FX (giữ nguyên, dùng khi cần)</summary>

### (nguyên văn khối cũ — user duyệt demo 2026-07-22 "video sinh động hơn")

Mỗi video có `03_SCRIPTS/<slug>_FX.json` (skill script-chouhen tự xuất từ video 09; format trong docstring `tools/fx_mix.py`) → pipeline tự thêm: **SFX đúng khoảnh khắc** (bank synth `tools/sfx_bank.py` → `06_VIDEO/_sfx/`, license sạch) + **BGM động** (dâng -40→-25dB trước reveal → CẮT PHỰT im lặng → tim đập; swell -26dB đoạn phe ác sụp) + **quote card** (câu đòn vàng-viền-đỏ / thoại phản diện cyan, style text-wall) + **phụ đề màu theo nhân vật** (hero vàng `#FFD75E` + tên, villain cyan `#8CEBFF`).
- **Render mới:** scene_render tự ăn FX.json ở cả 3 stage (segs: subs_fx.srt màu + card PNG; parts: burn card vào đúng part chứa nó; final: audio SFX+BGM động). Không có FX.json → chạy y như cũ.
- 🔴 **BA BẪY CỦA FX.json — vấp cả ba trong đúng một video (21, 2026-08-09):**
  1. **`"after"` là SỐ GIÂY, không phải chuỗi neo.** Đưa chuỗi vào → `TypeError: '>=' not supported between float and str`, chết ngay đầu stage segs.
  2. **`"after"` dính chặt vào timeline của GIỌNG.** Đổi arm B→A (38′04→35′01) làm mọi mốc giây trỏ sai chỗ. Kiểu hỏng nguy hiểm nhất **không phải** báo lỗi mà là **validate PASS nhưng trỏ nhầm sang lần xuất hiện thứ hai** — card lời trăng trối lẽ ra ở cold open 138s nhảy xuống 1012s, im lặng, không ai báo. → **Muốn lần xuất hiện ĐẦU thì BỎ HẲN `after`** (mặc định 0); chỉ dùng `after` cho lần thứ hai trở đi và chọn mốc ở **khoảng giữa hai lần** (video 21: chuông cửa ở 259s và 1615s → đặt 1000s) để chịu được đổi thời lượng. Đổi giọng/tốc độ/tag xong **phải validate lại trên `timeline.json` MỚI và soi từng mốc rơi đúng cảnh nào** — đếm "0 lỗi" là chưa đủ.
  3. **`offset` âm ở câu ĐẦU video** cho thời điểm phát < 0 → `adelay` báo `Delay must be non negative` và **giết khâu final SAU khi đã ghép xong 8 part**. Đã kẹp `max(0, …)` trong `fx_mix.py` (2 chỗ: SFX + ambience) nên nay chỉ lệch vài phần trăm giây thay vì đốt cả lượt render.
- **Video đã render chưa đăng:** `python tools/fx_mix.py <slug> --apply` = thay track audio (voice + BGM động + SFX, **tự tái tạo tiếng CTA** từ srt), -c:v copy vài phút, KHÔNG re-render; card + phụ đề màu không áp retro được. Đã áp video 08 (2026-07-22).
- SFX là synth ffmpeg (đủ tầng mid 200–600Hz nghe rõ trên loa nhỏ — bài học demo v1 bị chê "không rõ"); muốn foley thật hơn → thay wav trong `_sfx/`, mọi video sau tự ăn. Gain chuẩn: sting -5…-7, heartbeat/rung -8…-9, CTA -10; master alimiter 0.95.
- **KHÔNG áp cho kênh tài liệu** (health/co-dai/shokutaku/nenkin — phá persona); kr-romfan = ✅ áp (port fx_mix + sfx_bank sang `youtube-kr-romfan/tools/` khi làm video kr kế tiếp, card/style đổi hangul).

### 🎧 CHUẨN MỚI 2026-07-30 — lớp ÂM THANH chống "sản xuất hàng loạt" (user chốt)

> **Ca gốc:** user hỏi làm sao YouTube không đánh giá là hàng loạt + *"để người nghe có thể cảm nhận được"* khác biệt. Đo pipeline ra 3 con số: **1 file BGM duy nhất cho cả 13 video** (`Anguish.mp3` hardcode default), **1 giọng đọc mọi vai**, **6 SFX toàn tiếng SỰ KIỆN — 0 tiếng khung cảnh**. Khán giả kênh này **NGHE, không nhìn màn hình** → trên đúng kênh cảm nhận của họ, mọi video giống nhau gần tuyệt đối. Hình (vẽ tay/slide) **không chữa được** việc này: `handmade-layer.md` §3 đã chốt moat của kênh 朗読 là **giọng + văn** → công phải đổ vào TAI.
>
> ⚠️ **Giọng: GIỮ 1 giọng morioki cho mọi vai** (user chốt 2026-07-30, giữ nguyên memory `feedback_video_no_motion_mot_giong`) — phương án cho phản diện giọng riêng đã cân nhắc và **BỎ**. Khác biệt đến từ 3 lớp dưới, KHÔNG từ đổi giọng.

**① Tiếng khung cảnh (音の風景) — `tools/ambience_bank.py` → `06_VIDEO/_amb/`**
7 bed synth ffmpeg (license sạch, 32s, loop liền mạch): `blizzard` · `sea_deck` · `room_still` · `hospital_night` · `rain_window` · `night_snowplow` · `office_hum`. Khai trong `<slug>_FX.json`:
```json
{"type":"ambience","from":"<câu mở cảnh>","to":"<câu đóng cảnh>","name":"blizzard","gain":-29}
```
**gain mặc định `-24dB` — mức user DUYỆT BẰNG TAI 2026-07-30** (nghe demo video 13, chọn bản LOUD; bản -30dB bị đánh giá còn khẽ). Bed "phải im" (`room_still`) hạ thêm 3dB. · `fade` 2.0s · `lead`/`tail` 1.0s. **Mỗi video 2–5 bed cho các khung cảnh ĐỐI LẬP nhau** — đây là thứ làm video này "ở một chỗ khác" video kia. Video 13 = 6 bed (bão tuyết -23 / phòng thờ -27 / bệnh viện -25 / phố tuyết -26 & -27 / boong tàu -24).
- 🔎 **Phát hiện lúc đo demo:** khoảng nghỉ giữa các dòng của pipeline cũ là **im tuyệt đối -91dB (digital silence)** — không phải "im lặng trong một căn phòng". Đó là một phần thật của cảm giác "đọc trong phòng thu / robot" mà gate cấu trúc không bắt được. Lớp ambience lấp đúng chỗ này.
- 🔴 **GATE loa nhỏ, chạy sau MỖI lần sửa BANK: `python tools/ambience_bank.py --check`** — bed nào có dải 200–600Hz thấp hơn full-band >25dB thì **loa điện thoại không phát được gì**, mà khán giả nữ 45–70 nghe bằng đúng loa đó. Bản v1 fail **7/7** (gap 29–54dB) vì dồn hết năng lượng xuống <250Hz — đúng bài học `sfx_bank` v2.
- 🔴 **BẪY ffmpeg (ăn 2 lần trong 1 lượt): `bandpass` mặc định `width_type=q` (Q-factor), KHÔNG phải Hz.** `bandpass=f=500:w=800` = Q=800 = khe cộng hưởng ~1Hz (gần như im), không phải dải rộng 800Hz. Phải viết `bandpass=f=500:t=h:w=800`. ⚠️ **`tools/sfx_bank.py` còn 2 chỗ mắc lỗi này** (`door_knock` Q=260, `slap` Q=1600 → nghe thành "ping" cộng hưởng, không phải tiếng gõ cửa/tát) — **CHƯA sửa** vì user đã duyệt bằng tai ở v2 và video 08/09 đã lên sóng với tiếng đó; sửa = đổi bản sắc tiếng kênh → phải hỏi user.

**② Vòng xoay BGM — `tools/bgm_bank.py` + `--bgm auto` (mặc định MỚI)**
6 track pad synth (`pad_a_kan` La thứ · `pad_d_omoi` Rê thứ · `pad_e_hari` Mi thứ · `pad_f_shizu` Fa · `pad_g_fuka` Sol thứ · `pad_b_tsume` Si thứ) + `Anguish.mp3` cũ = **7 track trong vòng xoay**. `scene_render.py` và `fx_mix.py` giờ default `--bgm auto`: chọn track **ít dùng nhất** theo `06_VIDEO/bgm/ROTATION.log`.
- **Idempotent** (luật `render-background.md` §2.5): slug đã có trong log → LUÔN trả đúng track cũ, render lại/resume không đổi nhạc giữa các part. Log đã seed 8 video cũ = `Anguish.mp3`.
- ⭐ Muốn nhạc thật có melody: **bỏ file .mp3 vào `06_VIDEO/bgm/` là tự vào vòng xoay**, không sửa code (license free-thương-mại + credit 概要欄).

**③ Xoay biến thể khung 9 nhịp** (chữa tầng khuôn — thứ máy đọc được, không phải tai): cơ chế lật (供給停止 / 物証爆発 / 身分バレ / 内部告発), POV (私 nữ ↔ 俺 nam bằng 阿井田茂), độ dài 25′↔35′, sân khấu lễ nghi. Đừng để 5–7 video/tuần cùng một cơ chế lật.

⛔ **Nghe demo trước khi render cả bài** (`humanize-script-voice.md` §3): gain ambience **phải duyệt bằng TAI**. Số đo chỉ chứng minh bed nổ đúng chỗ + có dải nghe được trên loa nhỏ — KHÔNG chứng minh nó hay.

</details>

## Đóng gói upload (sau khi render + đóng gói CTR xong)

`python tools/upload_pack.py <slug> [--open]` → tạo `06_VIDEO/<slug>/_upload/` (mp4 rename SEO hardlink + subs.srt + thumbnail + METADATA.txt copy-paste + giờ hẹn theo `.claude/rules/upload-schedule.md`). User chỉ kéo thả + dán theo [1]→[8]. Tool standalone — kênh khác gọi bằng đường dẫn tuyệt đối + `--channel <key>`.

### ⭐⭐ SEO NHẸ — chốt 2026-08-12, CHỈ áp cho chouhen

> Bằng chứng: `CHANNEL_DIAGNOSIS_2026-08-12.md` §3.3. Video **105.183 view** của 毎日スカッと có
> **description RỖNG (0 ký) và 0 tag**. 語り茶屋 (top video **205.890 view**) và 孤独な桜の木 cũng **0 tag**.
> chouhen đang gánh 27–41 tag + 900–1.700 ký mô tả + 目次 mỗi video — **rail này không dùng cái nào.**

| | trước | **từ video 24** |
|---|---|---|
| mô tả 概要欄 | 900–1.700 ký + 目次 đầy đủ | **~300 ký** |
| 目次 timestamp | bắt buộc | **BỎ** |
| tag | 27–41 | **0–8** |
| bộ A/B | 3 title + 3 thumbnail | **1 + 1** |

**Khung mô tả mới (~300 ký), 4 khối, không hơn:**
1. 2–3 dòng hook (video kể chuyện gì, cho ai nghe) — giữ keyword chính 1 lần, tự nhiên.
2. `※この物語はフィクションです。実在の人物・団体とは一切関係ありません。`
3. Credit giọng: `AivisSpeech: morioki` / `VOICEVOX:青山龍星` tuỳ nhánh.
4. 3 hashtag nhận diện kênh.

🔴 **KHỐI 2 VÀ 3 CẤM BỎ** — disclaimer là compliance (`youtube-compliance.md` §5), credit giọng là
điều khoản license. Chúng **không phải SEO**, đừng cắt nhầm khi "cắt SEO".

⚙️ Gate của `upload_pack.py` (mô tả <400 ký · thiếu 目次 · GATE 3×3) **đã được nới cho riêng
`--channel chouhen`** — kênh khác giữ nguyên gate cũ.
📌 Ngoại lệ đã ghi vào chính file luật: `.claude/rules/youtube-upload-seo.md` §5 ·
`.claude/rules/ab-3title-3thumb.md` §6. **Đừng suy rộng sang kênh khác** — không kênh nào khác có
phép đo này.

## Thumbnail — quy tắc + prompt gen ảnh (TỰ ĐỘNG đưa, khỏi cần user hỏi)

> ⭐ **3 nguyên tắc gác cổng HÌNH (user chốt 2026-07-16, mọi kênh — mục 0.5 `youtube-jp-shokutaku/02_THUMBNAIL_TITLE_RULES.md`):** ① 1 điểm nhấn duy nhất, cắt chi tiết thừa, tương phản cao ② phóng đại CẢM GIÁC (cảnh báo→nguy hiểm rõ; hướng dẫn→kết quả cuối) ③ 120px vẫn rõ — nền đậm, chủ thể sáng.

### 🚨 LUẬT ĐO PACKAGING (chốt 2026-07-28 — đọc TRƯỚC khi so bất kỳ thứ gì với đối thủ)

Mọi so sánh thumbnail/title/độ dài **chỉ được dùng video ĐĂNG TRONG 30 NGÀY**, xếp theo **view/ngày**, đã **lọc Shorts (<8′)**. Dùng script `bench30` (đo 2026-07-28: 246 video long-form, dữ liệu thô `06_VIDEO/_ctr_2026-07-28/bench30_raw.json`); đo lại mỗi **4–6 tuần**.

**Vì sao thành luật:** cùng một lỗi 2 lần — bản đầu `CTR_PLAN_2026-07-28.md` đọc meta từ trang tìm kiếm mặc định (toàn video **3–4 năm tuổi**), và **v4 hiệu chỉnh theo `ハレバレ 428K`** trong khi kênh đó 8 ngày gần nhất chỉ ăn **157–3.341 view/video** — tức một **hit cũ của kênh đang chết**.

**Ba kênh view/video cao nhất rail KHÔNG dùng làm mốc** (だんご劇場 242K/video · スッキリ朝話 153K · ココロの引き出し 59K) — đều là **kênh Shorts 1–3′**, khác rail.

**Benchmark 30 ngày (2026-07-28), thay 苦しみの物語:**

| Kênh | slot trong top 50 view/ngày |
|---|---|
| **スカっとゼミ!** (`UC2b_fZ_quxsSl4Mn4w9X-1Q`) | **17/50** — lập kênh **2026-06-15**, 1.660 sub, **181 video**, 8 video/NGÀY cách 2h, độ dài **24–31′** |
| 嫁子のスカッと朗読劇場 | 11/50 (video 91–151′, view/ngày 12–15k — **thấp hơn** nhóm 25′) |
| 世界の中心でスカッと朗読 | 4/50 (5,7K sub, video 11–12′, 19k view/ngày) |
| 苦しみの物語 | **2/50** ← mốc cũ, đã lệch |

⚠️ Lợi thế lớn nhất của スカっとゼミ! là **số vé số** (181 video/6 tuần), KHÔNG phải thumbnail — đừng trộn 2 việc khi bàn CTR.

**Độ dài, median view/ngày (n=246):** 25–35′ **3.939** (đỉnh) · 8–15′ 2.928 · 35–50′ 1.832 · 15–25′ 1.764 · 70–200′ 1.053 · 50–70′ **757 (bét)**. → chuẩn kênh 30–40′ nằm ở rìa trên, **siết về 25–32′**.

### ⭐⭐ THUMBNAIL — LUẬT ĐANG THI HÀNH (chốt 2026-08-12). ĐỌC KHỐI NÀY TRƯỚC, MỌI KHỐI DƯỚI LÀ CHI TIẾT CŨ

> Bằng chứng: `CHANNEL_DIAGNOSIS_2026-08-12.md` §3.2 — soi tận ảnh thumbnail của 4 kênh peer cùng rail
> đặt cạnh thumbnail của chính mình.

🔴 **HAI ĐIỀU ĐÈ LÊN MỌI SỐ ĐO KHUÔN `m08` BÊN DƯỚI:**

**① BẮT BUỘC ≥2 NHÂN VẬT CÓ BIỂU CẢM RÕ ĐANG *DIỄN* ĐÚNG CẢNH TRUYỆN + ≥1 VẬT CHỨNG**
(phong bì · giấy tờ · chìa khoá · con dấu). Hai khuôn peer khác hẳn nhau về nền nhưng **giống nhau
đúng ở điểm này**. Thumbnail của video hit lớn nhất kênh (09, 367 view) là **một căn phòng trống
không có ai** — đó là cái đang thiếu, không phải cỡ chữ.

**② ⛔ BỎ `--bg-target 30/38` VÀ BỎ LUẬT "nền p20 ≤ 10/255".** Cái luật đó (chốt 2026-08-03) bắt dập
nền xuống gần đen tuyệt đối = **chủ động ném đi đúng thứ đang mua click cho peer**. Sàn mới: nền phải
đọc được ra **cảnh gì, ai đang làm gì**.

**Hai khuôn chạy A/B tuần tự — mỗi khuôn 5 video, so trung vị view (KHÔNG chạy song song 3 bản):**

| | khuôn | số đo | mẫu |
|---|---|---|---|
| **K1** | **text-wall + dàn người** | nền đen tuyền · **5–6 dòng chữ chiếm 65–70% bề ngang TRÁI** · cụm **3–5 người biểu cảm + vật chứng** dồn **30–35% PHẢI** · dòng đòn ĐỎ to nhất | 毎日スカッと **105.183v** |
| **K2** | **cảnh sáng kể chuyện** | ảnh cảnh photoreal **SÁNG chiếm 70–75% khung** · người diễn ở giữa · **chỉ 2–3 dải chữ** ở đáy/đỉnh | 語り茶屋 **205.890v** · 孤独な桜の木 **44.127v** |

Lệnh: `--preset k1` / `--preset k2` trong `tools/make_thumb_textwall.py` (thêm 2026-08-12).

**③ ⛔ ĐẢO LẠI 2026-08-13: QUAY VỀ BỘ 3 BẢN T1/T2/T3** (user: *"bật lại 3x3 đi"*) — ngoại lệ 1 bản/video sống đúng 1 ngày, đã hủy ở `.claude/rules/ab-3title-3thumb.md` §6. Ba bản chạy **SONG SONG** qua Studio "Test & compare".
- **Biến thử của bộ 3 giờ là LAYOUT, không phải 1-biến-hình:** T1 = text-wall (khuôn cũ) · T2 = **K2 toàn cảnh** · T3 = **K2 cận cảnh mặt**. Đây là chệch khỏi §3 mục "đổi ĐÚNG 1 biến" — **cố ý**, vì câu hỏi đang mở của kênh là *"khuôn nào"*, không phải *"nền sáng hay tối"*. Vòng sau, khi đã chốt khuôn, mới quay về 1-biến.
- 🔴 **Huy hiệu tròn: Ø KHÔNG còn cố định 124.** K2 có dòng chữ full-width bắt đầu ở y≈99 nên Ø124 **đè chữ**. Thi hành: **chọn Ø lớn nhất mà che 0 pixel chữ** (đo bằng máy) — video 24 ra T1 Ø110 · T2 Ø124 · T3 Ø96. Giữ nguyên vị trí góc trên-phải · lề 14 · màu kem/navy · hình trăng khuyết.
🔴 **Bù phép đo, KHÔNG được bỏ:** **đọc CTR TAY trong YouTube Studio (Chrome profile `Default`) mỗi
tuần 1 lần**, ghi vào `08_ANALYTICS_LOG.md`. Thumbnail vẫn là nghi phạm số 1 mà API đã mất metric —
mất luôn phép đo tay thì mù hoàn toàn.

⚠️ **Giới hạn của bằng chứng, ghi thẳng:** không có CTR để chứng minh nhân quả. Đây là **khác biệt
hình thái đo được** giữa bộ đang thắng và bộ đang thua **trong cùng một rail** — đủ để hành động,
chưa phải thí nghiệm.

**Cái GIỮ NGUYÊN từ các khối cũ:** bake chữ vào prompt ảnh AI (`ab-3title-3thumb.md` §3 mục 8) · vai
màu 5 dòng · 袋文字 viền đen + halo · huy hiệu tròn góc trên-phải (`--mark --mark-style circle`) ·
duyệt 168px + 120px · nhân vật hư cấu (không mặt người thật).

---

### ⭐ THUMBNAIL — TỪ 2026-07-29: QUAY VỀ TEXT-WALL RENDER BẰNG TOOL (đảo chốt 2026-07-28)

> 🔴 **ĐÈ 2026-08-10 — PROMPT PHẢI KÈM CẢ TEXT** (user: *"prompt phải kèm cả text"*; luật hệ thống `.claude/rules/ab-3title-3thumb.md` §3 mục 8). Từ nay chouhen **bake chữ vào prompt ảnh AI**; `make_thumb_textwall.py --preset m08` **hạ xuống ĐƯỜNG LUI**, chỉ chạy khi ảnh gen nát kanji (gen thêm 3 plate KHÔNG chữ).
> **Cái GIỮ NGUYÊN, chỉ đổi chỗ thi hành từ cờ tool → câu chữ trong prompt:** spec 5–6 dòng ≤14 ký · vai màu (trắng bối cảnh · hồng đúng 1 dòng · cyan quote phản diện ｗ · vàng twist · **ĐỎ dòng đòn cuối TO NHẤT**) · 袋文字 viền đen + halo trắng · dải đen ôm dòng 1 & dòng đòn · bộ 3 T1 tối / T2 nền SÁNG cùng chữ / T3 3 dòng + mặt · duyệt full-size + 168px + 120px.
> **Bẫy mới, phải soi:** kanji rậm (還暦・封筒) và cụm 「」ｗ hay nát nét → **soi từng ký tự trước khi giao**, sai một nét là loại. Mọi số đo khuôn 08 bên dưới vẫn là chuẩn để MÔ TẢ trong prompt và để chấm bản gen.
> Bản đầu tiên theo luật mới: `06_VIDEO/21_hachinen-no-yachin/thumb_prompts_FLOW.txt` (3 bản có chữ + 3 plate).

**User chốt 2026-07-29:** bỏ quy trình "xuất prompt gen chữ-trong-ảnh" (chỉ sống 1 ngày, 2026-07-28) — **quay về text-wall kiểu cũ như video 07 amamidokoro** (`07_UPLOADED/07_amamidokoro-saikaihatsu/_upload/thumbnail.png` = mẫu chuẩn): chữ do **tool vẽ** đè lên scene tối, **nhưng NHIỀU CHỮ hơn — 5–6 dòng** (bản cũ 4 dòng).

**Chuẩn render (mặc định mọi video mới):**
- Tool: `python tools/make_thumb_textwall.py <out.png> --lines "…" ×5–6 --colors auto --bg <ảnh scene AI KHÔNG chữ>` — có `--bg` là bgstyle tự vào `scene` (chữ đè ảnh, layout full-width v4). **KHÔNG dùng mặc định v5 flat/portrait, KHÔNG gen chữ bằng AI.**
- **5–6 dòng, mỗi dòng ≤14 ký** — layout kéo mọi dòng căng full-width nên dòng ngắn TỰ thành chữ khổng lồ; đừng viết dòng lê thê. Các dòng KỂ TRỌN setup như đọc title.
- **平体 tự động (v6, vá 2026-07-29 sau khi user bắt lỗi "chữ co rúm giữa khung"):** nhiều dòng vượt chiều cao khung → tool GIỮ chữ căng sát 2 mép và nén CHIỀU DỌC lớp chữ (sàn 0.66), KHÔNG co cỡ chữ cả khối như trước. Log in `平体 squash 0.XX` khi kích hoạt; 6 dòng thường rơi 0.78–0.90.
- **Vai màu (bộ 5 màu v3, user chốt lại đủ bộ 2026-07-29):** dòng 1 bối cảnh = TRẮNG · **dòng 2 bối cảnh nhấn = HỒNG (đúng 1 dòng)** · quote sốc = VÀNG · quote phản diện 「…ｗ」 = CYAN · dòng bồi = TRẮNG · **dòng ĐÒN cuối = ĐỎ double-stroke (halo trắng + viền đen), TO NHẤT**. Đỏ CHỈ dành cho dòng đòn cuối và **chỉ sống nhờ quầng trắng** (đo đỏ thuần 4,2x — tệ nhất bảng); hồng đo 4,8x nên chỉ đúng 1 dòng bối cảnh, không dùng cho quote/đòn; tím vẫn cấm.
- Nền scene: ảnh AI dàn cảnh không chữ (nhân vật hư cấu — khỏi tick disclosure); tool tự phủ scrim tối để chữ nổi. Không có ảnh → nền navy+sao vẫn chạy nhưng ưu tiên có scene.
- **Duyệt 2 cấp bắt buộc:** ① full-size — chữ không tràn mép/không đè mặt; ② 120px — đọc được dòng ĐỎ cuối.

**⭐ CHỐT 2026-08-01 (user, khi làm video 15): MẪU CHUẨN TEXT-WALL = THUMBNAIL VIDEO 08** (`07_UPLOADED/08_sokurikon-ichioku/_upload/thumbnail.png` — user: *"tôi thích có 1 thumbnail như này"*). Chất của mẫu 08 so với bản full-width nêm chặt:
- **Font = `--font yu` (YuGothB)** — user hỏi 2026-08-02 *"chữ mỏng mà sao vẫn dày thế"*: cái "dày" của 08 đến từ **袋文字 (viền đen + halo)**, không từ nét font. Mặc định M PLUS 1p Black (v4, dày hơn 63%) làm chữ nêm/bít so với 08 → **bản mẫu-08 đè mặc định đó, dùng yu**.
- **Nền scene CHÌM GẦN ĐEN** — thêm `--bg-target 48` (mặc định 88 làm nền nổi quá, tranh chữ).
- Quote có **nhãn vai ngoài ngoặc** (義母「…」/私「…」) như 08.

🔴 **SỐ ĐO THẬT CỦA MẪU 08 — đo 2026-08-02 sau khi user nói lại *"tao muốn cái thumbnail chữ mảnh như này"*** (bản weights 0.90–0.97 chốt hôm trước KHÔNG ra được chất 08, phải đo mới biết vì sao):

| | mẫu 08 | bản 6 dòng w0.90–0.97 (SAI) | bản 5 dòng w≤0.90 (ĐÚNG) |
|---|---|---|---|
| số dòng | **5** | 6 | **5** |
| **khe giữa dòng** | **42–70px** | **15–24px** ❌ | **60–66px** ✓ |
| cao dòng setup | 125–130px | 126–147px | 123–144px |
| rộng dòng / khung | 0.74–0.84 | 0.84–0.96 ❌ | 0.75–0.86 ✓ |

**Cái làm chữ "mảnh" là KHE GIỮA DÒNG, không phải nét font** (2026-08-02 là lần thứ hai đoán sai vào font: hôm trước kết luận 袋文字, vẫn không chữa được). Cơ chế: `size_for_width` cấp cỡ chữ theo bề ngang, `--block fill` chia **chỗ dư chiều cao** thành khe. Weights cao → dòng cao → hết chỗ dư → tool bật **平体 squash** nén dọc, khe tụt về `gap=6` ⇒ **tường chữ nêm kín = trông DÀY**. Hạ weights thì chỗ dư quay lại thành khe.
- **Gate máy đọc được:** log render **KHÔNG được in dòng `平体 squash`**. In ra = chữ đang bị nén = sai khuôn 08, hạ weights xuống.
### ✅ KHUÔN CHỐT = `--preset m08` (user duyệt bằng mắt 2026-08-03, dùng cho MỌI video sau)

```bash
python tools/make_thumb_textwall.py 06_VIDEO/<x>/thumb_T1_wall.png \
    --lines "d1" "d2" "d3" "d4" "d5" --preset m08 --bg 06_VIDEO/_series_assets/scene_<x>_ai.jpg
```

`--preset m08` gộp **toàn bộ khuôn** đã phải đo mất 5 vòng mới ra: `--font yu` · `--fat 0` · `--bg-target 38` · `--bg-sat 0.90` · `--bg-cool 0.75` · `--band ""` · weights `0.85,0.86,0.86,0.82,0.90` + colors `w,c,p,y,r` (5 dòng). **Cờ truyền tay luôn thắng preset** nên vẫn đè được từng biến. Mẫu wrapper: `06_VIDEO/15_gifu-no-kashikinko/run_thumb15.py`.

### 🏷 DẤU NHẬN DIỆN KÊNH trên thumbnail — `--mark --mark-style circle` (chốt 2026-08-04)

Mọi thumbnail của kênh mang **huy hiệu TRÒN góc TRÊN-PHẢI**: vòng kem 5px + lòng navy + vầng trăng khuyết (真夜中). Ø124, lề 14. Bật bằng `--mark 1 --mark-style circle` (chuỗi `--mark` chỉ cần khác rỗng; kiểu circle không dùng chữ).

- 🔴 **GIỮ NGUYÊN vị trí/màu/hình trên mọi video** — dấu nhận diện chỉ có giá trị khi không đổi. Video mới copy hằng `MARK` từ `06_VIDEO/16_yuinou-no-sneaker/run_thumb16.py`.
- ⚠️ Nó lọt vào **dải lề phải của dòng 1** (dòng 1 weight 0.86, căn giữa → chừa ~135px mỗi bên). **Nâng weight dòng 1 lên ~1.0 là đụng chữ** → kiểm lại nếu đổi weights.
- Đã thử và LOẠI: `bar` (vạch dọc + chữ quay dọc, thô) · `hanko` (con dấu đỏ góc dưới — **bị dòng đòn đỏ đè, đỏ chồng đỏ**) · `moon` (vành khung quanh ảnh, trông cũ) · `edge` (2 thanh mép, user chê xấu). Cả 4 vẫn còn trong tool nếu sau này muốn đổi bản sắc — nhưng đổi thì đổi ĐỒNG LOẠT, không đổi lẻ từng video.
- 📌 Bài học: khuôn text-wall phủ kín khung nên **mọi dấu ở góc DƯỚI đều đụng dòng đòn**; chỗ trống duy nhất là lề của dòng 1 → buộc phải góc TRÊN-phải.

### 🎯 BỘ 3 THUMBNAIL CHUẨN CỦA PROJECT (user chốt 2026-08-03): MỎNG · DÀY · FACE

| | vai | lệnh |
|---|---|---|
| **T1 MỎNG** `thumb_T1_thin` | baseline khuôn kênh — YuGothB nét mộc (đặc nét 0,383 như mẫu 08) | `--preset m08 --bg <scene>` |
| **T2 DÀY** `thumb_T2_bold` | **đổi ĐÚNG MỘT BIẾN = font** — M PLUS 1p Black (đặc nét ~0,61, kiểu video 14) | `--preset m08 --bg <scene> --font mplus` |
| **T3 FACE** `thumb_T3_face` | đổi LAYOUT — 3 dòng + mặt phản diện ~40% khung, chữ TO, đòn đỏ ≤6 ký giữ curiosity | `--preset m08 --bg <scene> --text-side right --text-w 0.63 --scrim 0.40 --colors w,c,r --weights "0.82,0.92,1.0"` |

- **T1 vs T2 chỉ được khác font.** Nền/chữ/màu/dải giữ y hệt — nếu không thì thắng thua không quy được cho nét chữ, mà đó chính là biến đáng thử nhất (kênh có 2 khuôn font đang cùng tồn tại).
- **T3 BẮT BUỘC `--scrim 0.40`.** Nhánh face để hở nửa khung cho mặt nên chữ nằm trên vùng nền chưa bị dập → bản đầu dòng 1 CHÌM vào ô cửa sáng. Nhánh full-width không cần vì nền đã tắt đều.
- Gate độ đặc nét **tự phân nhánh**: `--font yu` soi theo mẫu 08 (0,36–0,42, ngoài dải = LỆCH); `mplus/noto` chỉ in số kèm ghi chú "nhánh DÀY", không báo lỗi.

🔴 **GATE MÁY tự chạy sau mỗi lần render** (2026-08-03): tool đo **độ đặc nét glyph dòng vàng** ngay trên ảnh vừa xuất và in
`độ đặc nét glyph vàng = 0.387 (ĐẠT khuôn 08 = 0.383, dải 0.36–0.42)`. Ra **LỆCH** = nét đang bị bơm → hạ `--fat`. Nhánh nền SÁNG in `KHÔNG ĐO ĐƯỢC` (nền cùng tông chữ làm hỏng phép đo) — đó là bình thường, không phải fail.

### Nhánh T2 = TÔNG LẠNH (chốt 2026-08-03)

```bash
--preset m08 --bg <scene> --bg-sat 0.90 --bg-cool 0.75 --bg-target 38 --band ""
```

Hai cờ mới sinh ra từ lượt này, và cả hai đều đến từ việc **đọc sai chữ "trầm" hai lần**:
1. ❌ Đoán 1: trầm = TỐI HƠN. Sai — đo mẫu 14-T2 ra **p20 6 / median 14**, tức tối **bằng đúng T1**.
2. ❌ Đoán 2: trầm = RÚT BÃO HOÀ (`--bg-sat 0.40`). Sai — ra xám bệt, user: *"tông lạnh thôi chứ không đen trắng"*.
3. ✅ Đúng: **giữ bão hoà gần nguyên (0.90) rồi ĐỔI CÁN CÂN MÀU** — `--bg-cool` (cờ mới: nhân R×(1−0.30k), B×(1+0.16k), chạy TRƯỚC vòng gamma nên độ sáng vẫn về đúng `--bg-target`). 0.75 là mức chốt.

- `--bg-sat` (cờ mới) = bão hoà nền; **đừng hạ dưới 0.5** — đó là đường ra ĐEN TRẮNG, không phải tông lạnh.
- `--band ""` = bỏ HẾT dải đen sau chữ (user chốt cho nhánh T2). T1 **vẫn giữ** `--band "0,4"` của khuôn 08.
- ⚠️ Docstring `bg_scene` có câu "bỏ HẲN mọi can thiệp kênh màu" (bài học 2026-07-27 user chê ám xanh). **Không mâu thuẫn:** lần đó là ám xanh KHÔNG ai yêu cầu + có cộng offset làm đục vùng tối. `--bg-cool` là opt-in, chỉ NHÂN hệ số nên đáy vẫn về đen.
- Biến A/B của video 15 vì thế đổi từ *"nền sáng vs tối"* (bản sáng chữ chìm, gần như cầm chắc thua) thành **"nền RỰC vs TÔNG LẠNH"** — hai bản cùng đọc tốt thì thắng thua mới có nghĩa.

🔴 **VIDEO 14 KHÔNG PHẢI KHUÔN CHUẨN — đừng lấy nó làm mẫu** (chốt 2026-08-03 sau khi user đưa cả 2 ảnh). Hai thumbnail của chính kênh mình là **hai khuôn khác hẳn nhau**, đo ra:

| | **video 08 = CHUẨN** | video 14 (lệch) |
|---|---|---|
| font (IoU glyph 義/私) | **YuGothB 0,95** | M PLUS 1p Black 0,85 |
| độ đặc nét glyph 義 | **0,38** | 0,71 (dày gần gấp đôi) |
| nền p20 | **6** | 18 |
| dải đen dòng 1 + đòn | **có** | không |

Nguyên nhân lệch: video 14 render bằng **font mặc định của tool (`mplus`)**, còn video 08 render hồi tool chưa có `--font`/`--fat` nên ăn YuGothB mộc. → **Luôn dùng `--preset m08`**, đừng để rơi về mặc định.

🔴🔴 **NÉT CHỮ — `--fat 0` (chốt 2026-08-03, user: *"font chữ khác hẳn nhau"*).** Đây là biến CUỐI, và là chỗ **tao đã kết luận SAI 2 lần trước** (2026-08-02 ghi "cái dày của 08 là 袋文字, không phải nét font" → sai; 2026-08-01 đổ tại weights → chỉ đúng một nửa).

Phép đo dứt điểm — cắt riêng glyph 「私」 (có ở cả 2 ảnh), chuẩn hoá về cùng cỡ rồi so:

| | mẫu 08 | bản mình (mặc định `--fat` của yu = 0.02) | `--fat 0` |
|---|---|---|---|
| cao glyph | 137px | 134px | 128px |
| **độ đặc nét** (tỉ lệ pixel mực trong bbox glyph) | **0.383** | **0.528** ❌ *(béo hơn 38%)* | **0.387** ✓ |
| IoU hình chữ vs mẫu 08 | — | 0.73 | ~0.95 |

**Font KHÔNG sai — mẫu 08 đúng là YuGothB**, kiểm bằng IoU glyph 「私」 với 3 font của tool: **yu 0.949** · noto 0.732 · mplus 0.636. Cái làm mắt đọc thành "font khác hẳn" là **`--fat`**: cờ này ra đời SAU khi video 08 render (24/07), mặc định `yu: 0.02` làm phình nét đều mọi glyph → chữ mất chất mảnh và trông như một typeface nặng hơn.
- **Kiểm bằng máy, đừng nhìn:** cắt glyph kanji đầu dòng vàng, `mask.mean()` phải rơi **0.38–0.40**. >0.45 = đang béo, hạ `--fat`.
- ⚠️ `--fat 0` chỉ đúng cho `--font yu`. Đổi sang mplus/noto thì bản thân font đã nặng, `--fat` không cứu được.
- 📌 **Bài học quy trình (4 vòng, 4 lần đoán sai đều do NHÌN):** ① font/袋文字 ② weights ③ nền + dải ④ độ béo nét. Mỗi lần chỉ cần **cắt cùng một glyph ở 2 ảnh rồi so số** là ra ngay. Từ nay so khuôn thumbnail thì **đo glyph trước, bàn sau**.

🔴 **HAI THỨ CUỐI CÙNG CỦA MẪU 08, đo 2026-08-03 (user đưa lại ảnh 08 nói "làm cho tao 1 cái như này" — tức 2 vòng chỉnh trước vẫn chưa ra):** cả hai đều là **NỀN**, không phải chữ. Chỉnh chữ nữa là chỉnh sai chỗ.

| | mẫu 08 | T1 v15 bản cũ (`--bg-target 48`, không band) | T1 v15 bản mới |
|---|---|---|---|
| **nền p20** (p20 luminance từng hàng, lấy median — bỏ được ảnh hưởng của chữ) | **6** | 28 | **6** ✓ |
| median toàn khung | 21 | 93 | 16 ✓ |

1. **NỀN PHẢI GẦN TẮT HẲN: `--bg-target 30`, không phải 48.** Mẫu 08 có nền **p20 = 6/255** — tức gần đen tuyệt đối, cảnh chỉ còn vài mảng sáng lờ mờ. `--bg-target` chuẩn hoá **độ sáng TRUNG BÌNH**, nên ảnh scene có hot-spot (ô cửa cam của video 15) vẫn lọt sáng rực ở mức 48 → nền tranh chữ. **Cách kiểm bằng máy, đừng nhìn bằng mắt:** `np.median(np.percentile(gray, 20, axis=1))` phải **≤10**.
2. **`--band "0,4"` — dải đen đặc full-width ôm DÒNG 1 và DÒNG ĐÒN.** Mẫu 08 có 2 dải này; bản cũ chỉ có nền full-bleed nên dòng 1 nằm thẳng trên ô cửa cam. Cờ `--band` **trước đây chỉ làm được dòng đỏ** (`action="store_true"`), đã nới 2026-08-03: bỏ trống = hành vi cũ · `"0,4"` = theo chỉ số dòng · `"all"`. Dải kéo **hết bề ngang khung**, không bó theo `--text-w`.
- ⚠️ **T2 (nhánh nền sáng) dùng CÙNG `--band "0,4"` + cùng chữ** — nếu không thì biến thử không còn là "sáng vs tối" nữa mà lẫn cả cấu trúc dải.
- 📌 Lịch sử 3 vòng chỉnh khuôn 08, để không đoán lại vòng thứ tư: ① đoán do **font/袋文字** → sai ② đo ra do **khe giữa dòng** (5 dòng + weights ≤0.90, không để 平体 squash) → đúng nhưng chưa đủ ③ đo ra do **nền chưa tắt + thiếu dải** → đủ. Cả 3 lần cái sai đều là **đoán bằng mắt thay vì đo**.
- 6 dòng thoáng (w 0.72–0.86, khe 38–46px) đã thử và **loại**: full-size đọc được nhưng **dòng HỒNG mất ở 168px**. 6 dòng không thể vừa giữ cỡ chữ 08 vừa giữ khe 08 — 5×125+229+5×70 > 1080.
- **Lệnh: viết wrapper `.py` cạnh video** (mẫu `06_VIDEO/15_gifu-no-kashikinko/run_thumb15.py`) — chữ Nhật qua command line Windows bị mangle, và spec nằm trong file thì render lại không phải chép lại dòng lệnh dài.

**Bộ 3 bản A/B Test & Compare mỗi video (khuôn chốt ở video 14, giữ từ 15):** **T1** = text-wall mẫu 08 (trên) · **T2** = cùng chữ, đổi 1 biến NỀN SÁNG (lum ~110–115, `--scrim 0.30`) · **T3** = 3 dòng + MẶT biểu cảm (villain/heroine chiếm ~40% khung, `--text-side left|right`). ⭐ **T3 chữ phải TO (user chốt 2026-08-01 "chữ thumbnail face cho to lên"): `--text-w ≥0.63` + `--weights` sàn 0.72** (vd `"0.72,0.88,1.0"`) — bản 0.55/0.56 đầu tiên bị chê nhỏ. Đòn đỏ T3 ≤6 ký, giữ curiosity (không spoil đáp án).

**Prompt-gen chữ-trong-ảnh (`THUMBNAIL_PROMPT.md`) hạ xuống PHƯƠNG ÁN B** — chỉ dùng khi user chỉ định A/B test. Toàn bộ cờ tool + bản thử + số đo: `06_VIDEO/_thumb_v5_demo/V5_DEMO_2026-07-28.md`.

> ⚠️ **Nhóm chứng — KHÔNG thay thumbnail 07-25 / 07-27 / 07-06** (5.140 / 3.067 / 2.538 imp), baseline duy nhất để so. Video 10 đang mang bản `CHOT_v5_6` (render bằng tool, bảng màu đỏ/hồng cũ) — thay khi có bản gen theo chuẩn mới. Baseline CTR kênh **3,1%**; chi tiết `CTR_PLAN_2026-07-28.md`. **Đo lại 2026-08-17.**

### Title — ⭐⭐ KHUÔN MỚI 2026-08-12: CÂU VĂN TRẦN, BỎ TAG ĐẦU

> **Đảo chốt 2026-07-21 ("tag là ký tự số 1").** Bằng chứng: `CHANNEL_DIAGNOSIS_2026-08-12.md` §3.1 —
> đo 25 video mới nhất của **4 kênh peer cùng rail** (bộ kênh lấy từ chính `insightTrafficSourceDetail`
> của mình, không phải bộ tìm bằng search): **0/25 mở đầu bằng `【】`** ở cả 語り茶屋 · 毎日スカッと ·
> 裏話オーディオ · 孤独な桜の木. chouhen thì **24/24** mở bằng `【スカッとする話】`.

**Khuôn chuẩn — 60–90 ký, KHÔNG mở bằng `【】`:**

```
[tình huống cụ thể + hành vi ác của phản diện]。[だが/しかし/ところが] + [cú lật]―― | スカッとする話 | 修羅場
```

Ba bản mẫu đo được (view thật, 30 ngày):
- 毎日スカッと **105.183v**: 「両親が通院のため一晩うちに泊まっただけで、義母は見下して追い出した。夫は黙って見ていただけ。私はその場で夫と義母を家の外へ叩き出した――」
- 孤独な桜の木 **22.925v**: 「30億ドルを相続して帰宅した私に、夫と愛人が離婚届を突きつけた。「出ていけ！」私は微笑んだ――**| 感動する話 | スカッとする話**」
- 語り茶屋 **91.532v**: 「婚約者の女性にコーヒーを浴びせた姑――翌日、会社は跡形もなく消え去った。**#動エピソード #老後の物語**」

**Luật:**
- **Keyword ngách đẩy xuống ĐUÔI** bằng `| スカッとする話 | 修羅場` (khuôn 孤独な桜の木) hoặc hashtag
  đuôi (khuôn 語り茶屋) — vẫn giữ tín hiệu chủ đề mà **90 ký đầu là CÂU CHUYỆN**.
- **Kể trọn setup + hé cú lật rồi cắt bằng `――` / `…`.** Đừng dừng ở lời chửi của phản diện.
- Tình tiết + mốc thời gian phải **CÓ THẬT** trong thân truyện; không spoil lý do đòn; quét từ cấm
  theo `.claude/rules/youtube-compliance.md` mục 3. (2 luật này KHÔNG đổi.)
- **KHÔNG backfill title video cũ** — 24 video cũ giữ nguyên làm nhóm chứng để so trung vị.

⚠️ **Vì sao không copy 嫁子/スカっとゼミ! (2 kênh CÓ dùng 【】):** 嫁子 233K sub lập 2022, スカっとゼミ! đã có
thương hiệu. **Kênh 5 sub dùng khuôn của kênh 233K sub là copy sai thứ** — họ được bấm vì tên kênh,
mình thì chưa có gì ngoài dòng chữ.

<details><summary>(ĐÃ ĐÈ 2026-08-12) Khuôn tag-đầu — chốt 2026-07-21</summary>

`【スカッとする話】 + premise + 「quote sốc（ｗ）」 + đòn` → đóng `…した結果ｗ【修羅場】【朗読】`.
Căn cứ: đo 48 video top kênh <3.000 sub, 37/48 có 【修羅場】, 15/48 kết bằng 「〜した結果ｗ」.
⚠️ Bộ 48 video đó tìm bằng **search**; bộ kênh YouTube **thật sự ghép chouhen vào** thì ngược hẳn.

</details>

## Fiction & compliance

- Disclaimer 概要欄 (BẮT BUỘC, KHÔNG đọc trong kịch bản): 「この物語はフィクションです。実在の人物・団体とは一切関係ありません。」
- Không tên công ty/người/thương hiệu thật; trả thù qua kênh chính danh (luật sư/cảnh sát/kiểm toán/di chúc), chính diện không tự phạm pháp; tránh 自殺/mô tả tình dục/虐待 chi tiết (xem MỤC 12 trong skill).

## ⚠️ Tuân thủ YouTube → theo LUẬT GỐC toàn hệ thống

Luật đầy đủ (inauthentic/monetize, AI-disclosure, từ ngữ ad-friendly, metadata) nằm ở **`.claude/rules/youtube-compliance.md`** — dùng chung mọi kênh. Mỗi lần đóng gói video: quét checklist trong file đó & **báo ngay từ/điểm cần né**.

Áp riêng kênh chouhen (đã đạt sẵn):
- REMAKE biến hóa thật: đổi ≥8/10 yếu tố + rewrite 100% + không đoạn ≥25 ký trùng nguồn (chống "inauthentic").
- Nền = footage thật (green/river) → khỏi tick AI-disclosure; giọng AivisSpeech → ghi credit `AivisSpeech: morioki`.
- Disclaimer フィクション trong 概要欄; không tên thật; thumbnail nhân vật hư cấu (không mặt người thật).
- ⚠️ Tiêu đề/thumbnail né 殺/血/自殺/性/虐待 → thay 追い詰める/顔面蒼白/因果応報. (✅ 2026-07-09: đã quét & sửa hết 血 trong tiêu đề/thumbnail/概要欄 video 01–02 → 蒼白/顔面蒼白; thumbnail 02 đã render lại. Thân truyện GIỮ NGUYÊN theo rule 0.1.)

## Vault tương ứng

Tri thức/bài học/research: `E:\Claude\SecondBrain\10_Projects\youtube-jp-chouhen\`

## Engine

Công thức đầy đủ: skill `.claude/skills/script-chouhen/SKILL.md`.

> 📦 Doc cũ (diagnosis/optimize/benchmark hết hạn, khuôn đã bị đè) đã dời vào `./_archive/` (dọn 2026-08-24) — đường dẫn cũ trong rules trỏ file nào không thấy ở gốc thì tìm ở đó.
