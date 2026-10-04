---
name: video-render
description: Dựng video YouTube hoàn chỉnh từ kịch bản TTS (file _TTS.md) bằng pipeline tự động VOICEVOX + ffmpeg — voice đúng tag nhấn nhá, phụ đề sync từng câu, slide/ảnh minh họa, BGM, thumbnail, credit đầy đủ. Trigger khi người dùng nói "làm video", "dựng video", "render video", "tạo video từ kịch bản", "xuất video từ script", hoặc sau khi hoàn thành một kịch bản bằng script-healthy/script-viral và muốn ra video. Hỗ trợ 2 style — card (nền tối wa-modern + illustration いらすとや) và photo (ảnh thật full màn hình + phụ đề chữ trần viền đen).
---

# video-render

Biến `04_SCRIPTS/<x>_TTS.md` thành MP4 hoàn chỉnh. Tool sống ở `Projects/youtube-jp-health/tools/` nhưng dùng được cho mọi project cùng cấu trúc (script TTS 1 dòng = 1 nhịp đọc, tag `[...]` đầu dòng).

⚠️ **Kênh chouhen (`youtube-jp-chouhen`) KHÔNG dùng pipeline slide này** → render bằng `Projects/youtube-jp-chouhen/tools/ambient_render.py`: nền = 1 clip ambient lặp **+ SCENES 20–25 ảnh minh họa AI theo nhịp truyện** (config `<x>_SCENES.json`, ảnh ở `06_VIDEO/<x>/scenes/`, tool tự nhận & tự prep bo góc/fade; thiếu ảnh nào bỏ cảnh đó — format chốt 2026-07-10). Luật nền: **mỗi video 1 clip KHÁC NHAU, không tái dùng** — tool tự chọn clip chưa dùng từ `06_VIDEO/_bg/` (log `_bg/USAGE.log`), đừng truyền `--bg`. Test nhanh: `--limit 120`. Chi tiết: CLAUDE.md của project đó.

## ĐIỀU KIỆN TRƯỚC KHI CHẠY (check đủ 3, thiếu cái nào báo user ngay)

1. **VOICEVOX đang mở** — test: `curl -s -m 3 http://127.0.0.1:50021/version`. Không chạy → nhờ user mở app (engine chạy nền cùng app).
2. **ffmpeg** trong PATH (`ffmpeg -version`).
3. **Pillow** (`python -c "import PIL"`, thiếu thì `pip install pillow`).

Mọi lệnh python chạy qua Bash tool phải có `PYTHONIOENCODING=utf-8` (console Windows vỡ tiếng Nhật). Script inline có tiếng Nhật → viết bằng python heredoc/inline, tránh echo tiếng Nhật trực tiếp trong bash.

## CHỌN STYLE (hỏi user nếu chưa rõ, kèm khuyến nghị)

| | `card` (mặc định tool) | `photo` (kiểu kênh ảnh thật) |
|---|---|---|
| Hình | Illustration いらすとや trên card trắng, nền navy wa-modern (sóng 青海波 + khung vàng) | Ảnh chụp thật full màn hình, badge 第◯位 vàng góc trái |
| Phụ đề | `--sub-style outline` (trắng viền đen) | ⭐ **`--sub-style outline` — MỌI KÊNH** (user chốt **2026-08-10**: chữ trần có viền, **KHÔNG background**). Đè lệnh cũ "pill hộp trắng, chốt 2026-07-23". `pill`/`glass`/`bar`/`telop` **không dùng nữa**. Luật gốc + đánh đổi: `audience-45plus.md` §3.1. Dùng `--channel <key>` thì hồ sơ kênh tự điền, khỏi truyền cờ. |
| Config | ~14 slide theo section | ~40-45 cue, đổi ảnh mỗi 20-30s |
| Công gom ảnh | Nhanh (irasutoya ≤20 hình/video) | Lâu (phải duyệt mắt nhiều vòng) |

**PHỤ ĐỀ: TỐI ĐA 2 DÒNG/khối (user CHỐT — đã nhắc nhiều lần).** Mỗi phụ đề phải là 1 câu ngắn, KHÔNG bao giờ hiện nguyên đoạn 4-5 dòng. `write_srt` trong `video_render.py` tự tách mỗi dòng TTS thành nhiều cue theo câu (。！？), câu dài tách tiếp theo 、, mỗi cue ≤ `SUB_MAXLEN=42` ký (≈2 dòng), timing chia theo tỉ lệ ký tự trong khoảng của dòng. Nếu render bằng đường khác (finalize.py per-chunk), phải dùng cùng `subs.srt` đã tách này. Đổi độ dài → sửa `SUB_MAXLEN`, KHÔNG để phụ đề dài trở lại.

`video_render.py` **mặc định slide TĨNH** (motion off, toàn cục). Cờ `--motion` giờ = **pan chậm MƯỢT kiểu crop-pan** (scale nhẹ 1.18× → zoompan z=1 → crop trượt tuyến tính 4 hướng luân phiên) — **KHÔNG còn shimmer** (thủ phạm cũ là zoompan-ZOOM upscale 1.5×, đã bỏ). **health/shokutaku CHỐT dùng `--motion`** (phong cách đối thủ, user chốt 2026-07-23). Kênh khác vẫn tĩnh mặc định trừ khi tự thêm cờ. ⚠️ Đừng khôi phục nhánh zoompan-zoom cũ (rung).

**GIỌNG: chỉ nhấn nhá, KHÔNG đổi style.** User muốn 1 giọng nhất quán xuyên suốt. File `_TTS.md` chỉ dùng tag **nhấn nhá** `[速x][抑揚x][間x]` (tốc độ/lên xuống/ngắt) — TUYỆT ĐỐI không rải tag **đổi style** `[しっとり][ノーマル][喜び][囁き]` giữa bài (mỗi style là một chất giọng khác của 青山龍星 → nghe như "tự dưng đổi giọng"). Đặt giọng nền **1 lần** bằng 1 dòng tag-only ở đầu (sau `---` đầu tiên), vd `[しっとり]` — parse sticky nên áp xuyên suốt. Ngách シニア健康 → giọng nền `しっとり` (trầm ấm).

## QUY TRÌNH

> **CTA overlay giữa video — TỰ ĐỘNG (chốt 2026-07-15):** `video_render.py` (và scene_render chouhen/kr, stick_render stickman) ở bước cuối TỰ ghép hiệu ứng CTA (card 4 nút like/share/comment/subscribe + SFX pop/chime) vào đúng đoạn đọc câu CTA — tự tìm timestamp trong `subs.srt`, chỉ re-encode đoạn đó. Script chưa có câu CTA (rule `.claude/rules/cta-midvideo.md`) → tự skip, video giữ nguyên. Tắt: `--no-cta`. Tools gốc: `Projects/youtube-jp-chouhen/tools/{gen_cta_overlay,gen_cta_sfx,cta_inject}.py`.

### Bước 1 — Viết config slide `<x>_SLIDES.json` (hoặc `_SLIDES_photo.json`)

Mỗi entry (1 trong 3 loại hình): `{"match": "...", "rank": "第10位"|null, "lines": [...], "accent": true?, "photo": true?, "q": "search query"?, "diagram": "<tên>"?}`
- **Ảnh thật**: `"photo": true` + `"q": "..."` → `fetch_photos.py` tải `slide_XX.jpg`.
- **Diagram tự vẽ** (khái niệm trừu tượng: 血糖値/善玉菌/睡眠… không chụp được): `"photo": true` + `"diagram": "<tên>"` (KHÔNG `q`) → `make_diagrams.py` vẽ `slide_XX.png` (full-frame, đồng bộ tông; tự có badge rank). Thêm diagram mới = thêm hàm vào `DIAGRAMS` trong tool.
- **Card chữ**: `"photo": false` + `"lines": [...]` → render card wa-modern, khỏi cần ảnh.

Quy tắc `match`:
- Là substring của MỘT dòng đọc trong file TTS (sau khi bỏ tag) — tool lấy dòng ĐẦU TIÊN chứa nó làm mốc thời gian. Phải kiểm tra không có dòng nào TRƯỚC ĐÓ chứa trùng chuỗi.
- Thứ tự entry nên theo thứ tự thời gian trong script.
- Cú lật/úp mở của kịch bản (skill script-healthy hay có) → làm 2 slide: teaser (giấu đáp án) + reveal (`"accent": true` với card style).

### Bước 1b — Slide ĐỘNG bằng clip quay thật (Pexels Videos, user chốt 2026-07-10)

> ⚠️ **KHÔNG áp dụng cho health/shokutaku (user chốt 2026-07-23): 2 kênh sức khỏe render ẢNH TĨNH 100%** — clip trông xấu. Bước 1b này CHỈ dùng cho co-dai/chouhen/kr-romfan (nhóm clip-làm-xương). Với health/shokutaku bỏ qua toàn bộ mục này, đừng gắn `"video": true`.

Muốn cảnh chuyển động thay ảnh tĩnh: entry SLIDES thêm `"video": true` + `"qv": "<query video>"` (fallback `q`) → `python tools/fetch_clips.py <SLIDES json> 06_VIDEO/<x>/clips` tải `clip_XX.mp4` theo index → `video_render.py` thêm `--clips-dir 06_VIDEO/<x>/clips` là segment đó thành video (loop+trim theo cue, badge rank overlay); **thiếu clip → tự fallback ảnh tĩnh cùng index**, trộn thoải mái video/ảnh/diagram trong 1 bài.
- Clip Pexels license thương mại, KHÔNG cần credit, KHÔNG phải tick synthetic (footage thật) — nguồn log ở `clips/MANIFEST.json`.
- **Pexels dán nhãn resolution SAI** (link hd_2048 có thể serve 1366) → fetch_clips tự ffprobe verify ≥1280 và đổi rendition. API cần **User-Agent header**, thiếu là 403 cả key đúng.
- **VẪN duyệt montage bằng mắt** như ảnh (bệnh casting nặng hơn ảnh: "okra" ra biển PEACHES/máy gặt, "natto" ra gà rán, người trẻ lệch persona senior). Trích frame `-ss 4` từng clip → lưới PIL → Read.
- Cue dài hơn clip sẽ **loop (có cắt lặp)** — cue >30s nên ưu tiên clip dài khi chọn.
- Encode **theo chunk 8 segment** (tool tự làm) — 40+ input video 1 filtergraph là OOM "Cannot allocate memory", đừng gộp lại.

### Bước 1b-2 — Slide FOOTAGE TỰ LÀM (⛔ KHÔNG còn bắt buộc — bỏ 2026-08-09, TÙY CHỌN)

> ⛔ **Lớp thủ công ĐÃ BỎ (2026-08-09, user: "bỏ tất cả HANDMADE ở các project đi").** Bước này chỉ chạy khi user **tự muốn** đưa footage tự quay vào. **Không còn BỎ SLOT, không còn ghi sổ hoãn, không xuất bảng cần quay.** Lý do + cái mất: `.claude/rules/handmade-layer.md`.

Footage tự làm = tay thật làm thật (`tegami`) · iPad+Pencil viết ノート (`notebook`) · khoanh đỏ trang luật (`genten`) · nhân vật vẽ tay (`character`).

```bash
python E:\Claude\Projects\_media_library\ingest_handmade.py ingest "<file thô>" \
    --channel <kênh> --hm-kind tegami --tags "<từ khóa>" --speed 1.8 --trim 0:04,0:38
python E:\Claude\Projects\_media_library\ingest_handmade.py place 06_VIDEO/<x> \
    --map 03=<tên> 11=<tên> --slides <..._SLIDES.json> --used-by <kênh>/<x>
python E:\Claude\Projects\_media_library\ingest_handmade.py sheet 06_VIDEO/<x> -o sheet.jpg
```

- Cờ SLIDES là **`"handmade": true`** (KHÔNG phải `"video": true` = stock-clip), `place` tự bật hộ. Vẫn phải truyền `--clips-dir 06_VIDEO/<x>/clips` cho `video_render.py` — **kể cả health/shokutaku** khi video có lớp thủ công (đây là ngoại lệ duy nhất của luật "không --clips-dir cho 2 kênh này").
- `ingest` chuẩn hóa 1920×1080/30fps/**bỏ audio** (giọng từ TTS) — đừng ghép file .MOV thô từ iPad vào pipeline, lệch fps + méo khung dọc + lẫn tiếng phòng.
- `--speed 1.5–2.0` gần như luôn cần (tay thật chậm hơn nhịp kể). Cue dài hơn clip → **loop**, nên quay dài hơn cue.
- **Duyệt `sheet.jpg` bằng mắt trước render**: đúng thứ đang nói? tay rõ? **lộ mặt / nhãn hiệu / đồ bừa bộn không?**

### Bước 1b-3 — Slide "TRÔNG NHƯ VẼ TAY" (`make_drawn.py`, chốt 2026-07-27)

> Lớp **nhận diện**, dùng thay CARD CHỮ auto ở khối số/bảng/checklist/luồng. ⓘ Gate lớp thủ công đã bỏ (2026-08-09) nên không còn chuyện “chỉ có `drawn` là thiếu”. `drawn` dùng bình thường.

Entry SLIDES thêm `"drawn": {...}` (thay vì `"lines"` của card thường):
```json
{"match": "...", "drawn": {"layout": "table", "paper": "grid", "title": "実家の値段表",
 "rows": [["売る","1200万円"], ["解体","-180万円"]], "circle": 1, "anim": true, "dur": 30}}
```
```bash
python tools\make_drawn.py demo 06_VIDEO\_drawn_demo     # xem 7 mẫu trước khi dùng lần đầu
python tools\make_drawn.py slides 0N_SCRIPTS\<x>_SLIDES.json 06_VIDEO\<x>\slides_img \
       --clips-dir 06_VIDEO\<x>\clips --lang jp
```
- layout `card|table|checklist|flow` · paper `cream|grid|ruled|kraft|dark` · `circle: <index dòng>` khoanh đỏ đáp án · `highlight: [i]` tô marker.
- `"anim": true` → clip chữ hiện dần (`clip_XX.mp4`, renderer đọc cờ `"drawn"`) → **phải truyền `--clips-dir` cho `video_render.py`**, kể cả health/shokutaku.
- **Không ép `--size`** — cỡ chữ tự tính theo số dòng để lấp dải an toàn. Font khóa 1 cái/kênh (`--lang jp|jp-pen|jp-soft|jp-loud|kr|kr-thick|vn|vn-print`).
- Batch tự xuất `_drawn_sheet.png` → **Read duyệt mắt trước render**.

### Bước 1c — Nhân vật AI người dẫn (HeyGen b-roll): 🚫 ĐÃ BỎ (user chốt 2026-07-25)

Bước này **hủy**. health/shokutaku KHÔNG dùng footage người AI (cũng không stock-clip) → toàn bộ b-roll là **ảnh tĩnh + `--motion`**. Không đặt entry `"avatar"` trong SLIDES, không truyền `--clips-dir` cho 2 kênh này, không gọi `avatar_broll.py` (tool còn trong repo nhưng đã ngừng dùng).
Hệ quả compliance: **không video nào phải tick "altered/synthetic content"** — thumbnail AI + giọng TTS + script AI đều không cần khai báo (`.claude/rules/youtube-compliance.md` §2).

### Bước 2 — Gom ảnh

**Card style** — tải いらすとや (free ≤20 hình/video, thương mại OK):
- Search `https://www.irasutoya.com/search?q=<query>`, regex thumbnail `blogger.googleusercontent.com/img/...s72-c/...png`, thay `/s72-c/` → `/s800/` để lấy bản to. Ưu tiên ảnh có keyword trong TÊN FILE (tên file irasutoya mô tả nội dung), LOẠI file `thumbnail_*` và ảnh theo mùa (`tanabata`...).
- Lưu `06_VIDEO/<x>/slides_img/slide_<index 2 số>.png` theo index config.

**Photo style** — chạy `python tools/fetch_photos.py <SLIDES json> <folder ảnh>`:
- **Nguồn ưu tiên 1: Pexels API** (key ở `tools/.pexels_key`, gitignored; 200 req/giờ) — thương mại OK, KHÔNG cần credit, chất lượng cao, ~90-95% dùng được ngay vòng đầu. Fallback: Openverse + Wikimedia Commons (CHỈ CC0/CC BY/PD, KHÔNG BY-SA), tự ghi `ATTRIBUTIONS.md`.
- Batch nhiều video: để ý quota 200 req/giờ — mỗi video ~40 query, xen kẽ fetch với render là tự giãn.
- ⚠️ **VẪN BẮT BUỘC duyệt montage bằng mắt** (PIL lưới 8 cột đánh số, Read xem): Pexels tốt nhưng vẫn lệch kiểu — "raw egg rice" ra ikura donburi, "senior eating" ra con mèo, ảnh người già ra người Nepal/đen trắng. Ảnh sai → xóa + đổi query → chạy lại (tool skip ảnh đã có). Pexels thường chỉ cần 1 vòng sửa 3-7 ảnh.
- ⚠️ **2 tiêu chí bắt buộc khi duyệt (user chốt 2026-07-23): (1) ĐÚNG CHỦ ĐỀ từng câu** — ảnh khớp nội dung dòng thoại, không chỉ "đẹp chung chung"; **(2) SẮC NÉT** — ảnh phủ full-frame 1920×1080 (cover-crop), phóng 100% không được mờ/nhiễu/vỡ hạt. Ảnh gốc nhỏ hơn khung sẽ bị upscale mờ → `fetch_photos.py` đã nâng ngưỡng độ phân giải (Pexels ≥1920, dùng rendition `original`); ảnh nào vẫn mờ hoặc lệch chủ đề → đổi query tải lại.
- **Nhân vật case study CÓ TÊN (佐藤さん, フミコさん...)** → dùng illustration いらすとや thay ảnh người thật (tránh gán mặt thật vào nhân vật hư cấu + đồng bộ series).
- Slot bí → fallback: (a) dup ảnh cùng chủ đề (đặt xa nhau về thời gian), (b) illustration いらすとや (.png alpha — tool đặt lên nền kem). ⚠️ Khi đặt PNG fallback mà chạy lại fetcher, nó sẽ tải thêm .jpg cùng index (tool render ưu tiên .jpg) — nhớ xóa .jpg thừa.
- Search irasutoya bị chặn tạm sau nhiều request → nghỉ vài phút hoặc dùng ảnh Pexels cắt tròn thay icon.
- Chốt xong → dọn `ATTRIBUTIONS.md` khớp bộ ảnh cuối.

### Bước 3 — Render (1 lệnh)

> ✅ **TỪ 2026-07-27 — DÙNG HỒ SƠ KÊNH, ĐỪNG GÕ TAY BỘ CỜ NỮA:**
> ```
> python tools\video_render.py <0N_SCRIPTS>\<x>_TTS.md --channel <health|shokutaku|co-dai|nenkin|kaigo|akiya>
> ```
> `tools\channels.py` (nguồn sự thật máy đọc) tự điền: **giọng + style + speed + intonation · `--sub-style` · `--motion` · `--watermark` · BGM + gain · palette card riêng kênh · `--img-dir`/`--clips-dir` TUYỆT ĐỐI (tự suy theo stem)** · bộ `drawn` của kênh. Cờ gõ tay vẫn thắng hồ sơ khi muốn thử khác.
> **PREFLIGHT tự chạy TRƯỚC khâu voice** và CHẶN: `--img-dir` tương đối/không tồn tại · thiếu ảnh slide (in đúng slot thiếu) · `rank` = 0 · thiếu watermark ở kênh bắt buộc · thiếu clip của entry `handmade` (mất lớp thủ công) · BGM sai đường dẫn. Gãy ở đây tốn 2 giây thay vì 25 phút. Cố tình bỏ qua: `--skip-preflight`.
> **Đổi bản sắc render của 1 kênh → sửa `channels.py`, KHÔNG chép giá trị vào CLAUDE.md/`.cmd`.**
>
> ⛔ **GATE CŨ (vẫn phải tự kiểm khi KHÔNG dùng `--channel`) — 2 câu hỏi, sai cái nào là đốt cả lượt render (bài học video 20 goya, 2026-07-26: chạy 25 phút, exit code 0, ra file 79 MB TOÀN CARD NAVY TRỐNG):**
> 1. **`--img-dir` là ĐƯỜNG DẪN TUYỆT ĐỐI chưa?** `video_render.py` làm `Path(args.img_dir).resolve()` = giải theo **cwd**, mà lệnh render `cd` về gốc project → truyền tên trần (`slides_img_photo_v2`) hay đường dẫn tương đối sai gốc là nó trỏ vào folder KHÔNG tồn tại. Không thấy ảnh → mọi entry `photo:true` **âm thầm fallback về card chữ**, mà entry photo không có field `lines` → card trống trơn. **Tool KHÔNG báo lỗi, exit 0.** → luôn viết `E:\Claude\Projects\<project>\06_VIDEO\<x>\slides_img_photo...`, và `ls` folder đó đếm đủ ảnh trước khi chạy.
> 2. **Mọi entry SLIDES đã có field `rank` chưa?** (xem "Badge đồng bộ" bên dưới) — thiếu `rank` thì video chạy hết bài không có nhãn mục nào, trong khi giọng vẫn hô「第五位」. Đếm nhanh: `grep -c '"rank"' <SLIDES json>` phải xấp xỉ số entry, không được ra 0.

> 🔴 **CÁCH CHẠY — LUÔN CHẠY NỀN, KHÔNG BAO GIỜ FOREGROUND** (luật `.claude/rules/render-background.md`, user chốt 2026-07-26): viết lệnh dưới vào `06_VIDEO/<slug>/run_render.cmd` (UTF-8 + CRLF, `chcp 65001 >nul` ở đầu nếu có arg tiếng Nhật/Hàn như `--watermark`), redirect `> 06_VIDEO\<slug>\render.log 2>&1` + `echo EXITCODE=%ERRORLEVEL%`, rồi gọi `cmd //c "<đường dẫn .cmd>"` bằng Bash tool với **`run_in_background: true`**. Lý do: render 20–60 phút, foreground treo cả lượt chat và khi máy kill tiến trình thì **chết im, không EXITCODE** (video 21 health chết ở dòng 215/231 khâu voice). Không sleep/poll chờ — harness tự gọi lại khi xong; muốn xem tiến độ thì `tail render.log` một lần. Chạy lại sau khi gãy = **đúng lệnh cũ** (step A tự skip chunk đã có).

```
cd Projects/youtube-jp-health
# card style (motion TẮT mặc định — khỏi cần cờ):
python tools/video_render.py 04_SCRIPTS/<x>_TTS.md --bgm 06_VIDEO/bgm/Wholesome.mp3 --bgm-gain -40
# photo style (health/shokutaku — ẢNH thật + hộp trắng + pan mượt; KHÔNG --clips-dir, không clip nào):
python tools/video_render.py 04_SCRIPTS/<x>_TTS.md --slides 04_SCRIPTS/<x>_SLIDES_photo.json \
  --img-dir 06_VIDEO/<x>/slides_img_photo --sub-style outline --motion \
  --watermark 健康ノート \
  --bgm 06_VIDEO/bgm/Wholesome.mp3 --bgm-gain -40
#   (bỏ --motion nếu muốn tĩnh hẳn. --clips-dir chỉ dành cho kênh dùng stock-clip: co-dai/chouhen/kr)
```
- **`--watermark <chữ>` = badge nhận diện kênh overlay góc TRÊN-PHẢI mọi frame** (mẩu giấy note amber/navy, nghiêng 3°, mờ 0.85 — cùng ngôn ngữ hình với badge thumbnail; `--watermark-opacity` để chỉnh). Ghép ở step B nên KHÔNG bị pan kéo theo, không đè badge rank (trên-trái) lẫn phụ đề (đáy). **OPT-IN có chủ ý**: renderer dùng chung 6 kênh → mặc định bật sẽ đóng dấu chữ kênh này lên kênh khác. **health: BẮT BUỘC truyền `--watermark 健康ノート` từ video 21** (bible §8.5b). Kênh khác muốn dùng → tự chốt chữ badge của kênh đó rồi thêm vào lệnh + CLAUDE.md project.
- Slide diagram tự vẽ (khái niệm trừu tượng): thêm entry `{"match":"...", "photo":true, "diagram":"<tên>"}` (không `q`) → chạy `python tools/make_diagrams.py <SLIDES json> <slides_img_photo>` TRƯỚC fetch_photos. Diagram tự có badge rank, video_render đã bỏ vẽ badge đè lên nó.

- Chạy **run_in_background** (voice ~5-8 phút + encode ~5-10 phút).
- Lần đầu render voice + timeline; sửa slide/style/BGM về sau LUÔN thêm `--reuse` (khỏi gọi VOICEVOX lại).
- **BGM mặc định: `--bgm-gain -40` (CHỐT 2026-07-09, user thích nền rất khẽ).** Mặc định tool là -24 (hơi to với tai user). Số càng âm càng nhỏ: -35 khẽ vừa, -40 rất khẽ, -45 gần biến mất; -15/-20 = to. Chỉnh khác → đổi số này.
- ⚠️ Remix BGM sau khi đã render: **KHÔNG dùng `--bgm-only`** (nó mix chồng lên audio mp4 đã có nhạc → cộng dồn). Mix lại đúng = ffmpeg lấy `voice.wav` + BGM ở gain mới, `-c:v copy` (không encode lại, ~20 giây). Muốn xuất demo nhanh cho user chọn mức: cắt ~80 giây (`-ss 60 -t 80`) từ voice.wav + BGM rồi ghép video slice.
- Bật Ken Burns (hiếm khi, chỉ khi user yêu cầu): thêm `--motion` (slide tĩnh là MẶC ĐỊNH — KHÔNG có cờ `--no-motion`). Đổi speaker/tốc độ: `--speaker`, `--speed` (mặc định 青山龍星, 0.9). ⚠️ `--speaker` nhận **TÊN** (vd `morioki`, `青山龍星`, `阿井田 茂`) — KHÔNG phải id số; sai → lỗi "không tìm thấy speaker". Kênh sukatto: `--engine aivis --speaker morioki --speed 1.0`.
- Output: `06_VIDEO/<x>/` gồm `<x>.mp4`, `voice.wav`, `subs.srt`, `timeline.json`, `slides/`. ⚠️ **KHÔNG còn sinh `thumbnail.png`** (bỏ 2026-07-28, xem Bước 5) — renderer chỉ in trạng thái "đã có / CHƯA CÓ".
- Trước khi render đè bản cũ user đã duyệt → backup `<x>_<style>_style.mp4`.

### Bước 4 — VERIFY (bắt buộc, không báo xong khi chưa làm)

> ⚠️ **`EXITCODE=0` KHÔNG có nghĩa là video đúng.** Render hỏng kiểu "ảnh không lên, ra card trống" vẫn exit 0 (video 20 goya 2026-07-26). Bắt buộc soi mắt trước khi báo đạt.

1. `ffprobe` duration khớp voice; **file size hợp lý — so với video cùng kênh cùng độ dài**. Bản 15:40 có ảnh thật = ~149 MB; bản card trống cùng độ dài chỉ 79 MB → size hụt ~nửa là dấu hiệu ảnh không lên.
2. Trích 3-4 frame (`ffmpeg -ss <t> -i ... -frames:v 1`) tại: intro, giữa 1 mục ranking, cú lật #1 — Read xem bằng mắt: slide đúng nội dung, phụ đề không đè hình, **có badge 第◯位/その◯ ở góc**.
3. **Phụ đề phải chạy theo lời**: trích 2 frame cách nhau ~6s TRONG CÙNG 1 slide, phụ đề phải khác nhau.
4. **BGM có thật**: đo `volumedetect` 0.7s tại một khoảng nghỉ giữa section (tra `timeline.json` tìm gap >1s) — phải ra ~-40dB thay vì -91dB.

### Làm SERIES nhiều video (batch)

- **Dây chuyền**: viết config video N → fetch ảnh N (nền) → trong lúc chờ viết config N+1 → duyệt montage N → render N (nền, TUẦN TỰ từng video — VOICEVOX/CPU không chạy 2 render song song) → verify N khi có notification.
- **Badge đồng bộ** (⚠️ luật này áp cho **MỌI video**, không riêng batch — xem GATE ở Bước 3): format ranking → `第◯位`; format điểm/thói quen → `その1`…`その5` (trong SLIDES json, mọi cue trong section mang cùng rank).
- **Thumbnail series** (CHỈ kênh health): dùng `tools/make_series_thumb.py` — cùng công thức burst, cùng nhân vật cảm xúc (cặp vợ chồng già), chỉ đổi bubble icon chủ đề + badge (TOP10/5つの習慣/5つのコツ) + text. Sửa CONFIG trong file rồi chạy 1 lệnh ra cả loạt. ⚠️ Kênh khác KHÔNG chạy tool này với CONFIG sót — kiểm tra text CONFIG khớp script trước khi chạy.
- Script đời cũ chưa có PACKAGING → tự viết thumbnail text theo luật (≤6-7 chữ, curiosity gap, không lặp title).
- ⚠️ Luật chống spoil áp cho cả bubble icon: video ranking úp mở đáp án thì icon KHÔNG được là đáp án (đã dính: video kakure-dassui suýt để icon きゅうり = chính là 第1位).

### Bước 5 — Thumbnail GHÉP ẢNH (renderer KHÔNG sinh thumbnail nữa)

> 🔴 **SỬA 2026-07-28 — đã BỎ HẲN `make_thumbnail()` khỏi `video_render.py`.** Hàm đó vẽ chữ **HARDCODE 「腎臓が よろこぶ／1位は意外」** (video 03 kênh health) rồi ghi đè `thumbnail.png` ở **mọi lần render, mọi kênh** — đúng cái tên mà `upload_pack.py` tự bốc. Đã dính **2 lần**: 2026-07-04 video `01_haken-tsuyaku` (sukatto) và 2026-07-27 video `22_satsumaimo-cho` (health, bắt được lúc đóng gói). Giờ renderer chỉ in `Thumbnail: đã có … (GIỮ NGUYÊN)` hoặc `CHƯA CÓ → dựng bằng make_thumb.py`, và `upload_pack.py` báo `thumbnail: THIẾU` cho tới khi có bản thật.
>
> → **Thumbnail luôn dựng bằng tool riêng của kênh** (`tools/make_thumb.py` cho health/shokutaku/…), text lấy từ mục **Đóng gói CTR của chính script đang render**, qua gate 168px. Không có bước "bản nháp chữ-chay của tool" nữa.

⚠️ **CÔNG THỨC THEO KÊNH — không dùng chéo:**
- Kênh **health** (`youtube-jp-health`) → công thức "burst kiểu Nhật" bên dưới (nền sáng kem, vui). Tool: `tools/make_series_thumb.py`.
- Kênh **sukatto/朗読** (`youtube-jp-sukatto`) → công thức "drama đêm khuya" trong `E:\Claude\Projects\youtube-jp-sukatto\CLAUDE.md` (nền tối cinematic — NGƯỢC hẳn burst). Quy trình 2 tool trong repo sukatto:
  1. `python tools/fetch_portraits.py "<query>" ...` — casting nhân vật Pexels (portrait): tải ứng viên + montage duyệt 1 mắt → chốt em nào thì `--get <pexels_id> chara_woman_<tên>.jpg` + ghi `_series_assets/SOURCES.md`. Ảnh CẢNH đông người (パワハラ dàn cảnh, rừng ngón tay chĩa...) → `--scene "<query>"`, lưu `scene_*.jpg`, dùng làm NỀN với chara=None trong CONFIG (tool tự neo crop lên đỉnh giữ mặt người). ⚠️ CHỈ dùng scene khi mặt nhân vật RÕ và không bị text đè — video 01 thử rồi bị user loại vì "không thấy nữ chính"; mặc định vẫn là panel chân dung. Người thật CHỈ đóng vai chính diện (license Pexels cấm bôi xấu người mẫu); mức sexy trần = "quyến rũ có váy áo" (hở quá bị YouTube đè/age-restrict).
  2. `python tools/make_sukatto_thumb.py` — sửa CONFIG rồi chạy: nhân vật `.jpg` = panel phải blend mềm, `.png` (いらすとや) = paste cutout; tự xuất kèm `*_mobile_preview.png` (check chữ + mặt ở cỡ nhỏ) và các biến thể `thumbnail_b/c.png` cho A/B khi CTR <3%.
  - `tools/gen_face.py` (AI face, FLUX free): user ĐÃ LOẠI 2026-07-04 vì "không thật" — đừng đề xuất lại trừ khi có Nano Banana trả phí.
- **Text thumbnail LẤY TỪ mục Đóng gói CTR/PACKAGING của chính script đang render** — KHÔNG tái dùng CONFIG/text của video hay kênh khác (đã dính 2026-07-04: thumbnail `01_haken-tsuyaku` kênh sukatto bị render text 「腎臓がよろこぶ」 của kênh health).

Công thức "burst kiểu Nhật" — CHỈ kênh health (bản user chốt sau 3 vòng), ghép PIL:
- **Nền sunburst**: nền kem sáng (#FFF6DC) + tia pieslice vàng nhạt (#FFDE82) xoay quanh tâm lệch phải — KHÔNG dùng nền tối/ảnh trầm (v2 ảnh mâm cơm bị chê "chưa ấn tượng").
- **Nhân vật cảm xúc** いらすとや to bên phải (~500px): cảm xúc khớp lời hứa (よろこぶ → cặp già cười; dọa → mặt sốc). Có MẶT NGƯỜI thumbnail mới sống.
- **Icon chủ đề** (tạng/món) trên bong bóng tròn trắng viền đen phía trên.
- **Badge đỏ TOP10** góc trái trên (format ranking).
- **Chữ 袋文字 viền kép, nghiêng 2-3°** (render layer riêng rồi rotate): dòng title fill navy + stroke trắng 12 + stroke đen 24, ~98px; dòng đinh fill vàng #FFE600 + stroke đỏ #D7000F + stroke đen, ~180px.
- ⚠️ **LUẬT CHỐNG SPOIL**: hình KHÔNG được là đáp án của cú reveal (vd tease "1位は意外" mà nền là đống muối = tự phá curiosity gap — lỗi đã dính).
- Backup các bản cũ (`thumbnail_text.png`, `thumbnail_v2.png`...) làm biến thể A/B khi CTR thấp.

### Bước 6 — Giao hàng

Báo user: đường dẫn MP4, các file kèm, và NHẮC:
- Dán credit vào 概要欄: `VOICEVOX:青山龍星` + dòng BGM (Kevin MacLeod CC BY) + `ATTRIBUTIONS.md` nếu photo style + `Illustration: いらすとや` nếu card style.
- Title/概要欄/pinned comment lấy từ GIAI ĐOẠN 6 (PACKAGING) trong file script chính.
- User tự nghe lướt 1 lượt check phát âm từ y tế (VOICEVOX có thể đọc sai 蓄積型...) — AI không thay được tai người khâu này.

## 🔴 ĐỔI ASSET RỒI RENDER LẠI — luật gốc `.claude/rules/render-background.md` §2.5

Mọi renderer có cơ chế resume, và trước 2026-07-29 chúng hỏi *"file đã tồn tại chưa"* thay vì *"file còn ĐÚNG không"* → thay ảnh xong render lại vẫn ra **HÌNH CŨ**, `EXITCODE=0`, không cảnh báo (ca thật: video 22 health, log ghi `chunk 1..18 đã có, skip`, mp4 nhỏ bất thường 76 MB vs 165 MB). Đã vá 6 chỗ bằng so mtime / đưa danh tính asset vào tên file.

**Thao tác tay bắt buộc:** sau khi đổi ảnh/clip, đọc log tìm dòng `CŨ HƠN … → render lại`. **Không thấy dòng đó mà mình vừa đổi asset = có gì sai, đừng cho qua.** Bí thì xoá tay `06_VIDEO/<slug>/slides/chunk_*.mp4` (+ `burn_*.mp4`, `trans_*.png`) rồi render lại.

⚠️ Cũng lưu ý: `video_render.py` mặc định tìm `<stem>_SLIDES.json` — file tên `<stem>_SLIDES_photo.json` thì phải truyền `--slides` tay.

## AUDIT TIỀN-UPLOAD (chạy khi user hỏi "đủ hấp dẫn chưa / đánh giá video")

Nói thẳng trước: **chưa upload = KHÔNG có thông số lượt xem** — đừng bịa. Cái làm được là audit 3 cửa có bằng chứng:

1. **Cửa TÌM KIẾM**: đối chiếu key của video với `05_KEY_MATRIX.md` / trend update — key có breakout thật không, và **intent có khớp không** (vd breakout là「腎臓に悪い食べ物」mà video là「腎臓がよろこぶ習慣」= cùng trục nhưng lệch intent một nấc → gợi ý video sau ăn đúng breakout). Title: keyword trong 28 ký tự đầu.
2. **Cửa CLICK**: thumbnail đã ghép ảnh chưa (chữ-chay = fail), có spoil đáp án không, chữ đọc được ở cỡ mobile không.
3. **Cửa GIỮ CHÂN** — đo số thật từ `timeline.json` (python: tìm start của các câu mốc):
   - Hook vào đề <15s; **câu echo lời hứa packaging ≤15s** (script 3 dính 92s — điểm trừ);
   - Re-hook ~50%, reveal số 1 ở 70-80%, CTA ~95%;
   - Độ dài vs chuẩn user (15-20 phút, ~5500-6500 ký tự); nhịp đổi ảnh ~20s/cảnh;
   - Ghi rõ điểm trừ nào đáng sửa trước upload (thumbnail) vs điểm nào chỉ là bài học cho script sau (không thu âm lại vì 1 câu).

## ĐO SAU UPLOAD (48-72h, YouTube Studio) — dặn user mang số về

1. **CTR** theo impressions: chuẩn ngách 4-6%; <3% → thay thumbnail biến thể B (đã backup sẵn).
2. **Survival tại 0:30** (Engagement/intro): mục tiêu ≥70%.
3. Đường retention tại mốc re-hook (~50%) có đỡ được dip không; tại reveal (~76%) phải có bướu nhô (rewatch).
4. Traffic source → Search terms: query thật người ta gõ → mồi cho key video sau.

## BẪY KỸ THUẬT ĐÃ DÍNH (đừng lặp lại)

- **Filter phụ đề phải đứng SAU `fps=30`** trong filter chain — đặt trước thì mỗi slide chỉ có 1 frame gốc, phụ đề đông cứng nguyên đoạn (đã fix trong tool, đừng viết lại kiểu cũ).
- (Lịch sử) Style `pill`: `OutlineColour` phải trắng cùng `BackColour`, không thì viền đen thành cục đen trong hộp. ⛔ `pill` đã bỏ 2026-08-10 — mọi kênh dùng `outline`.
- PNG alpha mà `convert("RGB")` thẳng → nền ĐEN. Tool đã xử lý (đặt nền kem) — giữ nguyên hành vi này.
- Đường dẫn slide trong ffmpeg concat chạy với `cwd=video_dir` — truyền path tương đối từ video_dir hoặc tuyệt đối.
- yt-dlp phân tích video đối thủ: tải `worst[ext=mp4]` đủ soi style, trích frame rải 5-6 mốc.

## KHI USER MUỐN NÂNG CẤP

- Ảnh đẹp hơn (photo style): xin **Pexels API key** (free) → sửa `fetch_photos.py` thêm source pexels, ưu tiên trước Openverse.
- Giọng người thật hơn: VOICEPEAK (mua 1 lần ~¥23,800) hoặc ElevenLabs — xem `07_PRODUCTION_PIPELINE.md`.
- Cảnh nhân vật "bác sĩ AI": user tự sinh ảnh bằng tool AI ảnh, thả vào folder ảnh theo index slide, thêm entry config là thành cutaway.
