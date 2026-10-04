# 09_VIDEO_PIPELINE — LUẬT DỰNG VIDEO kênh 古代の秘訣

> ⛔ **ĐÃ BỊ ĐÈ TỪ VIDEO 25 (2026-08-27):** kênh chuyển sang **Remotion khuôn nenkin** —
> xem `CLAUDE.md` §② (8 bước) + `tools/build_remotion_25.py`. File này giữ để tra cứu video ≤24
> (make_vox/make_shot/video_render). Bước ①② (check_coldopen · voice_only) vẫn dùng chung.

> **Nguồn sự thật DUY NHẤT** về việc từ `_TTS.md` ra file mp4 của kênh này. Chốt **2026-08-18**
> khi dựng video 21 (風呂のカビ) — bản đầu tiên có lớp chuyển động bằng hình + avatar + FX.
> Đổi quy trình → sửa file này. Nội dung/retention xem skill `script-co-dai`; đóng gói xem
> `.claude/rules/youtube-upload-seo.md`.

---

## 0. THỨ TỰ BẮT BUỘC — làm ngược là mất công gen lại ảnh

```
① script _TTS.md  →  check_coldopen.py   (0 FAIL mới đi tiếp)
② voice_only.py   →  voice.wav + subs.srt + timeline.json      [NỀN]
③ gen_slidesNN.py →  SLIDES.json + IMG_FLOW.txt + IMG_NAMES.txt
④ make_vox --still + make_shot --still  →  DUYỆT MẮT chữ/bố cục   ← rẻ, chưa cần ảnh
⑤ USER GEN ẢNH   →  placeNN.py --apply  →  strip_wm_crop.py
⑥ autofocus.py --apply        (vùng nhìn cho inset/focus)
⑦ add_fx.py --apply           (FX + avatar theo câu, cần timeline ở ②)
⑧ make_vox + make_shot  →  84 clip mp4                          [NỀN]
⑨ video_render.py --reuse  →  video hoàn chỉnh                   [NỀN]
```

🔴 **⑥ và ⑦ phải chạy SAU ⑤** — chúng đọc ảnh thật. Chạy trước thì `autofocus` không có gì để đo.
🔴 **⑦ phải chạy SAU ②** — `add_fx` cần `timeline.json` để biết câu nào vang ở giây nào.
🔴 **Chạy lại ③ là XOÁ kết quả của ⑥⑦** (gen_slides ghi đè SLIDES.json) ⇒ sửa gen_slides xong
phải chạy lại **⑥ rồi ⑦**, đúng thứ tự đó.

---

## 1. LỆNH TỪNG BƯỚC (chép, đừng gõ lại)

```bash
# ① gate cấu trúc
python tools\check_coldopen.py 21                      # phải 0 FAIL

# ② voice (NỀN, ~17 phút cho bài 20′)
python tools\voice_only.py 03_SCRIPTS\21_..._TTS.md --channel co-dai

# ③ SLIDES + prompt ảnh
python tools\gen_slides21.py

# ④ duyệt trước khi tốn ảnh
python E:\Claude\Projects\_media_library\make_vox.py  <SLIDES> <clips> --channel co-dai --still --sub-mock --force
python E:\Claude\Projects\_media_library\make_shot.py slides <SLIDES> <clips> --img-dir <VD> --still --force

# ⑤ ảnh về
python tools\place21.py --src "C:\Users\tuana\Downloads\<folder>"          # XEM TRƯỚC
python tools\place21.py --src "..." --apply
python tools\strip_wm_crop.py 06_VIDEO\<slug> --cut 0.900

# ⑥⑦ vùng nhìn + hiệu ứng
python E:\Claude\Projects\_media_library\autofocus.py <SLIDES> --img-dir <VD> --apply
python E:\Claude\Projects\_media_library\add_fx.py  <SLIDES> --timeline <VD>\timeline.json --min-gap 22 --apply

# ⑧⑨ dựng + render — LUÔN qua .cmd chạy nền (render-background.md)
06_VIDEO\<slug>\run_clips21.cmd        # make_vox rồi make_shot, chặn ở bước 1
06_VIDEO\<slug>\run_render21.cmd       # vá .sig lệch rồi video_render --reuse
```

**Chi phí đã đo (video 21, 20′10″):** voice ~17′ · 84 clip ~50–60′ · render ~25–30′ ·
clip trung gian **~11 MB/clip ≈ 0,9 GB** (xoá khi `upload_pack --done`).

---

## 2. LỚP HÌNH — bốn mode, vai chọn THEO ẢNH

| mode | dùng cho | thứ hiện dần |
|---|---|---|
| `soft` | câu kể | chỉ thở ±1,5% sáng |
| `inset` | ảnh CẢNH — phóng một mảnh của chính nó | card ảnh trượt lên + mũi tên sáp |
| `focus` | ảnh ĐÃ MACRO — chỉ đích danh | vòng khoanh bút sáp + ngoài vòng tối 24% |
| `wipe` | đổi trạng thái (bẩn→sạch, ướt→khô) | ảnh B lộ dần, có vệt sáng ở mép |

🔴 **Ảnh macro KHÔNG được đi `inset`** — phóng to cái đã cận thì vỡ hạt. Ảnh cảnh KHÔNG đi
`focus` một mình vì vòng khoanh dễ trúng chỗ trống.
🔴 **Không hai `inset` liên tiếp** — hai tấm ảnh trượt vào liền nhau đọc thành "một khung lặp".
`autofocus.py` tự đổi cái thứ hai sang `focus`/`soft`.
🔴 **Khung có avatar → hạ về `soft`** — avatar + card inset + vòng khoanh = ba lớp chồng nhau.

**Tỉ lệ đã chạy ở #21:** inset 20 · focus 19 · soft 31 · wipe 2 · vox 12 (84 khung / 20′).

---

## 3. FX + AVATAR (chốt 2026-08-18: avatar ảnh thật · FX dày)

| câu nói | hiệu ứng | prop |
|---|---|---|
| 「…」 thoại | **avatar + bong bóng** | `avatars/co-dai/*` + `bubble_left/right` |
| 白状しますと / 正直に申し上げ | avatar `kataribe_wry` | — |
| 〜ではありません · 逆効果 | ✗ sáp đỏ | `cross_x` |
| số + 度/秒/分/時間 | con dấu tròn | `stamp_round` |
| 〜てください | nhãn giấy ghim | `label_tag` |

- **Mật độ thực tế: 28 FX / 20,2′ = mỗi 43 giây.** Hạ `--min-gap` xuống nữa **không ra thêm** —
  số FX bị chặn bởi số câu khớp luật, không bởi ngưỡng. Muốn dày hơn phải thêm LUẬT, đừng bịa chỗ đặt.
- **FX luôn nằm phía ĐỐI DIỆN** vùng đang khoanh / card inset (`free_spot()` trong `add_fx.py`).
- **Nhãn lấy từ BẢNG ĐỘNG TỪ**, không cắt chuỗi trước ください.
- **Cùng một con dấu phải cách ≥180 giây** — `50度` từng đóng 3 lần trong 90 giây.
- ⛔ **`smudge` (vệt mực) ĐÃ BỎ** — soi frame thật thì chỉ là vết bẩn, không tải nghĩa.
- **Avatar: người vào sớm (t≤1,6s), bong bóng vang đúng giây câu thoại** (`bubble_t`). Buộc chung
  một `t` thì màn hình chết 12 giây rồi người mới nhảy vào (đã dính ở #21).
- **Avatar chân CHẠM ĐÁY KHUNG**, không kẹp ở `safe_bottom` — kẹp thì người lơ lửng giữa ảnh.
- **Bong bóng nằm hẳn phía đối diện avatar**, chừa 24px — không thì che mặt nhân vật.

### ⚠️ Nghĩa vụ khai báo
Avatar là **ảnh AI người** ⇒ mọi video có avatar **phải tick "altered/synthetic content"** khi
upload (`youtube-compliance.md` §2.1). `upload_pack.py` chưa có cờ này ⇒ **tick TAY trong Studio**.
Thumbnail vẫn giữ luật cũ: **không mặt người**.

---

## 4. ẢNH — ba việc luôn phải làm

1. **Khớp ảnh ↔ slot bằng `placeNN.py`, rồi ĐỌC BẢNG.** Matcher tham lam gán sai thật: ở #21 nó
   nhét ảnh **"cửa sổ mở, gió vào"** vào slot **"phòng tắm KHÔNG có cửa sổ"** — ngược hẳn nghĩa,
   không gate nào bắt được. Sai chỗ nào thì ghim vào `FORCE`, đừng để đoán.
2. **Watermark ✦ — định vị bằng CHỒNG ẢNH, không bằng residual/template.**
   Quét local-contrast trên từng ảnh trả về **mép trái = biên vùng quét ở 84/84 ảnh** = số rác.
   Cách chạy được: cộng trung bình cả lô → ✦ ở cùng chỗ nên nổi lên, nội dung khác nhau thì mờ đi.
   Lô 1376×768 của #21: ✦ ở **x 1255–1302 (0,912W)** → cắt `--cut 0.900`. **Đo lại mỗi lô.**
3. **Ảnh "SAU" của cặp `wipe` không nằm trong vòng lặp sinh prompt** — phải xuất riêng, nếu không
   user gen thiếu và `wipe` tự hạ về `soft` (mất đúng cú trước→sau đắt nhất bài).

---

## 5. LEGIBILITY — chỗ đã cháy

- 🔴 **`room` và `timeline` là 2 kind DUY NHẤT vẽ kicker/head TRẦN trên ảnh** → chữ ink chìm vào
  nền xám. Đã vá trong `make_vox.py`: `kicker(on_photo=…)` + `head_line(highlight=…)`. Kind khác
  đã có dải vàng từ trước. **Thêm kind mới thì kiểm lại đúng chỗ này.**
- 🔴 **`collage` cũng vẽ kicker/title TRẦN — §5 dòng đầu ghi THIẾU một kind** (bắt được ở #24).
  `k_collage` gọi `head_line(...)` **không có `highlight=True`** và title là **mực ĐEN** ⇒ chìm trên
  ảnh SÁNG, và chìm luôn trên ảnh TỐI. `photo_style: "duotone:ink"` **không cứu được** (đã thử).
  ⇒ Cách chạy được mà không đụng tool: **cho `collage` về NỀN PHẲNG** (bỏ `bg:"photo"`) — nó đẹp
  và đọc rõ ở nền kem. Vẫn qua X2 nếu các kind khác đủ ≥50% (ở #24: 15/18 = 83%).
  ✅ **`duotone:ink` LẠI cứu được `timeline` và `source`** (title của 2 kind đó có dải vàng / chữ
  trắng) — nên đừng áp một cách cho cả ba. Sửa đúng tầng = thêm `highlight=True` vào `k_collage`
  trong `make_vox.py`, **chưa làm** vì đó là tool dùng chung với nenkin/kaigo/akiya.
- 🔴 **`bar`: nhãn TRÀN RA NGOÀI KHUNG khi thẻ chỉ có 2 THANH** (bắt được ở #24, soi 1:1). Cỡ chữ nhãn
  co theo SỐ THANH (2 thanh → hàng cao hơn → font to hơn), còn mốc phải của nhãn thì cố định ở đầu
  thanh ⇒ nhãn dài bị đẩy ra khỏi mép trái. Đo được: **3 thanh chịu được 6 ký** (`最も細かい網` ✅)
  nhưng **2 thanh thì 6 ký bị cắt** (`飛んでくる時期` → hiện `んでくる時期`, mất hẳn chữ đầu).
  ⇒ **thẻ `bar` 2 thanh: nhãn ≤4 ký.** Sheet thu nhỏ KHÔNG thấy lỗi này — chỉ soi 1:1 mới thấy.
  📌 Chữa đúng tầng là ở `make_vox.py` (nó biết cỡ font thật) — nhưng đó là tool DÙNG CHUNG với
  nenkin/kaigo/akiya, nên **chưa sửa**; hiện chặn bằng cách viết nhãn ngắn.
- **Bong bóng thoại phải có RUỘT ĐỤC** (chữ đen đọc trên ảnh tối). `prep_bubble.py` giữ ruột bằng
  cách chỉ bỏ vùng sáng **liên thông với mép ảnh**; rembg KHÔNG dùng được ở đây (nó ăn mất ruột).
- Ảnh gen về có thể **cùng một hướng đuôi bong bóng** → lật ngang để có bản còn lại.

---

## 6. BẪY KỸ THUẬT (đã dính thật, đừng đi lại)

| bẫy | dấu hiệu | cách tránh |
|---|---|---|
| `.cmd` có ký tự ngoài ASCII | log **không được tạo**, exit 0 | `python -c "print(sum(1 for b in open(f,'rb').read() if b>127))"` phải = 0 |
| `echo X=%V%>> log` | dòng `EXITCODE=` **rỗng** | đặt redirect TRƯỚC `echo`, hoặc chèn dấu cách |
| sinh `.cmd`/`.py` bằng heredoc | `SyntaxError: unterminated string` · `\N escape` | dùng **Write tool**, không heredoc |
| `TextIOWrapper` không `write_through` | log **0 byte** suốt lần chạy, nhìn như treo | `line_buffering=True, write_through=True` |
| filter `subtitles=` với đường dẫn tuyệt đối Windows | ffmpeg vỡ filtergraph | chạy `cwd=` thư mục chứa srt, dùng tên file trần |
| `make_*.py --still` | **không tạo mp4**, renderer âm thầm fallback ảnh tĩnh | `ls clips/*.mp4 | wc -l` phải = số entry `video:true` |
| **ghi `.cmd` bằng `open(...,'w',encoding='ascii')`** | file **RỖNG 0 byte**, `.cmd` chạy exit 0 mà **không làm gì**, không tạo log nào | `'w'` truncate NGAY rồi mới ném `UnicodeEncodeError` ở ký tự đầu tiên ngoài ASCII (dấu `—`). ⇒ ghi ra **file .tmp rồi `os.replace`**, và kiểm **`size > 0`** chứ không chỉ `byte>127 == 0` — phép kiểm đó **PASS trên file rỗng** |
| 🔴🔴 **marker `<!-- GATE:本編 -->` KHÔNG có `#` đứng trước** | **TTS ĐỌC NÓ THÀNH LỜI** và nó vào cả `subs.srt` — **đã lên sóng thật ở video 16** (`07_UPLOADED/16_tsukemono-shio-no-dan/_upload/subs.srt` dòng 91, phụ đề 01:12–01:14 là `<!-- GATE:本編 -->`) | `tts_render.py` dòng 139 chỉ bỏ qua dòng bắt đầu bằng **`#`** hoặc **`>`** — nó **không biết cú pháp comment HTML**. Còn `check_coldopen.cues()` dò bằng `if MARKER in raw` **trước** bộ lọc `startswith`, nên **`# <!-- GATE:本編 -->` thoả CẢ HAI**. ⇒ **luôn viết marker có `#` đứng trước.** Quét: `python -c "print(sum(1 for l in open(f,encoding='utf-8') if 'GATE' in l and not l.strip().startswith(('#','>'))))"` phải = 0. 📌 Cùng họ bẫy với 2 dòng header `TARGET_QUERY:`/`INTENT:` (skill `script-co-dai` Bước 0) — **một dữ liệu đi qua HAI parser, và cái thứ hai mới ra tới video** |
| chạy 2 tiến trình dựng cùng lúc | clip trộn spec cũ/mới | kill sạch trước khi chạy lại: `Get-CimInstance Win32_Process … make_shot` |

---

## 7. NGHIỆM THU TRƯỚC KHI GIAO

1. **Soi ≥4 frame rải đều** (`EXITCODE=0` không chứng minh gì).
2. **`ffprobe` duration khớp `subs.srt`.**
3. **Dựng demo 90–120 giây trước bản đầy đủ** — `06_VIDEO/_demo21/` là mẫu: dựng clip của các entry
   đầu vào thư mục riêng, ghép voice thật + phụ đề thật. Ở #21 chính demo này bắt được **avatar vào
   muộn 12 giây** và **hai khung inset lặp** — hai lỗi không gate nào đo được.
4. Soi frame **giữa animation**, không chỉ frame cuối: nhiều lỗi (inset rỗng, mũi tên trỏ hụt) chỉ
   thấy khi build-on đang chạy.

---

### 🔴 BẪY: thẻ `process` TRÀN CHỮ khi n=3 — trần **10 ký** cho `label` (bắt 2026-08-26, video 24)

`k_process` co chữ bằng `_fit(lab,"black", bw-48, 92, SZ_LABEL_MIN)` — **có SÀN font 44**. Quá sàn thì
chữ **tràn ra ngoài hộp, không co thêm**, và **không renderer nào báo lỗi**: `SHOT_EXIT=0`,
`EXITCODE=0`, video ra bình thường. Chỉ lộ khi soi frame 1:1.

Toán trần (W=1920, MARGIN_X=120, gap=56):

| n cột | bề rộng cột | `label` (pad 48, sàn 44) | `sub` (pad 30, sàn 30) |
|---|---|---|---|
| 2 | 812 | **17 ký** | 26 ký |
| 3 | 522 | **10 ký** | 16 ký |
| 4 | 378 | **7 ký** | 11 ký |

Ca gốc: video 24 e37 có label 12·12·8 ký ⇒ hai cột đầu tràn, đúng ở khung trả 3 bước cốt lõi của bài.
**Sửa ở TEXT** (rút nhãn), ⛔ đừng hạ `SZ_LABEL_MIN` — sàn 44 là sàn cỡ chữ cho tệp 45+.

⚠️ Cột **tràn khỏi ĐÁY khung là CỐ Ý** (`yb_col = H + 40`) — đừng "sửa" cái đó.

🔧 Quét máy trước mỗi lượt render (cùng họ với `check_zu_layout` của nenkin):
```python
cap = lambda n,pad,floor: ((1920-240-56*(n-1))//n - pad)//floor
# process: label cap(n,48,44) · sub cap(n,30,30)
```

## 8. FILE & TOOL

| file | việc |
|---|---|
| `_media_library/make_shot.py` | build-on bằng HÌNH (4 mode) |
| `_media_library/shot_fx.py` | lớp FX + avatar |
| `_media_library/add_fx.py` | gán FX/avatar theo câu + nhịp |
| `_media_library/autofocus.py` | tìm vùng đáng nhìn, chống inset lặp |
| `_media_library/prep_bubble.py` | ảnh bong bóng → prop PNG ruột đục |
| `_media_library/make_vox.py` · `check_vox.py` | thẻ vox + gate X1–X5 |
| `tools/gen_slidesNN.py` · `placeNN.py` · `strip_wm_crop.py` | SLIDES · khớp ảnh · cắt ✦ |
| `avatars/co-dai/` | 5 cast (`kataribe_talk/point/wry` · `haha_talk/back`) |
| `props/` | 22 prop PNG (mũi tên · vòng · ✗ · dấu · nhãn · 2 bong bóng) |
| `06_VIDEO/_cast/CAST_PROMPTS.md` | prompt gen cast, dùng lại khi mở nhân vật mới |
