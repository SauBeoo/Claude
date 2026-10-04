---
name: vox-collage-video
description: Dựng video Vox-style paper-collage documentary bằng Remotion từ audio + script — không hỏi lại về style. Dùng khi user đưa file voiceover/narration (mp3/wav) kèm script và muốn ra video, hoặc nói "dựng video collage từ audio này", "make me a video from this audio", "video kiểu Vox collage", "same style as before", "làm video Remotion", hoặc nhắc tới video collage/cutout/paper-texture đã làm trước đó. Phủ trọn pipeline: timestamps (subs.srt sẵn có hoặc Whisper), chia scene, tải ảnh Pexels + cắt nền rembg thành sticker, synth SFX, build scene Remotion với kho entrance animation không lặp, đăng ký Root.jsx, preview bằng Remotion Studio (không render MP4 trừ khi user yêu cầu). ⚠️ KHÁC với skill `video-vox` (lớp thẻ annotate ffmpeg cho pipeline kênh YouTube) — cái này là video Remotion collage độc lập.
---

# Vox-collage video pipeline (Remotion)

> ⭐⭐ **CẬP NHẬT 2026-08-15 — repo `remotion-vox` đã nâng thành TOOL DATA-DRIVEN (kiểu CapCut).**
> Đường ƯU TIÊN cho video mới: **KHÔNG viết JSX per-video nữa** — chạy
> `py -3 tools/auto_collage.py --audio a.mp3 --srt s.srt --out <name> [--plan plan.json]`
> (plan JSON = tag/punch/heroQuery/supportQueries từng scene — chính là output của các bước
> 2–3 dưới đây, ghi thành file thay vì viết vào JSX). Ra `projects/<name>/project.json`,
> mở chỉnh trong **editor web** (`run_editor.cmd` → http://localhost:5599), render bằng nút
> 🎬 hoặc `npx remotion render VoxProject --props=projects/<name>/project.json out/x.mp4`.
> Đọc `remotion-vox.md` của repo để biết schema + toàn bộ tool. Các bước dưới đây vẫn là
> NGUỒN SỰ THẬT về style/tư duy chọn scene-ảnh-SFX; chỉ phần "viết scene JSX + Root.jsx"
> (bước 6–7) là lỗi thời — làm qua project.json + editor thay thế.

> Nguồn gốc: skill của kênh **Non-tech làm AI** (video "Chỉ 5 phút - Mình đã tạo Vox-style
> Video chỉ bằng Claude Code & Remotion", 2026), port + adapt cho workspace này 2026-08-15.
> ⚠️ **Đừng nhầm với skill `video-vox`** — đó là lớp thẻ annotate (make_vox.py, ffmpeg) nằm
> TRONG pipeline video kênh YouTube. Skill này dựng NGUYÊN một video collage bằng Remotion.

Đích visual là look "Vox explainer" collage: ảnh stock thật **đã cắt nền** (silhouette
của chủ thể, KHÔNG phải hình chữ nhật chứa chủ thể), viền sticker giấy trắng mỏng quanh
mỗi cutout, vài cutout xếp lớp trên nền graph-paper/giấy kraft, chip chữ vàng highlighter
đậm, và mọi thứ animate với năng lượng thủ công hơi lệch nhịp — không phải motion graphics
corporate mượt mà.

Làm tuần tự các bước dưới. **Không hỏi user về style** — style đã chốt. Chỉ đáng hỏi
2 thứ per-video: khung 16:9 hay 9:16, và (khi Pexels thật sự không có gì dùng được)
lấy ảnh gì cho một chủ thể không có ảnh stock tương đương.

## 0. Trước khi bắt đầu

**Remotion project:** dùng chung project `E:\Claude\Projects\remotion-vox\` — quy ước:
mỗi video 1 file scene JSX trong `src/`, export component + `SOMETHING_CANVAS` +
`SOMETHING_TOTAL_FRAMES`, đăng ký trong `src/Root.jsx` qua `<Composition>`. Chưa có
project (máy mới) thì scaffold:

```bash
cd E:\Claude\Projects && npx create-video@latest remotion-vox --blank
# hoặc scaffold tay: npm i remotion @remotion/cli react react-dom + src/index.jsx + Root.jsx
```

**Python deps:** kiểm `python -c "import rembg, scipy"` — thiếu thì
`pip install rembg onnxruntime scipy`. Whisper (`pip install openai-whisper`) chỉ cần
khi audio KHÔNG có srt đi kèm (xem bước 1). Tất cả chạy local, không API key trả phí.

## 1. Lấy timestamps của audio

Copy audio vào `public/` với tên ngắn (vd `audio.mp3`).

**Đường A — audio từ pipeline VOICEVOX của workspace (ưu tiên):** đã có sẵn `subs.srt`
sync từng câu cạnh `voice.wav` → **dùng thẳng srt, khỏi Whisper**. Mỗi block srt =
1 segment với start/end chính xác tuyệt đối (chính engine sinh ra nó).

**Đường B — audio lạ (không srt):** transcribe bằng Whisper lấy word-level timestamps:

```python
import whisper
model = whisper.load_model("base")
# language đặt theo audio THẬT: "ja" / "vi" / "en" — đừng hardcode
result = model.transcribe("public/audio.mp3", word_timestamps=True, language="ja")
```

In start/end/text từng segment + word list phẳng. Merge token `"%"` đứng lẻ vào từ
trước nó (Whisper hay tách "40%" thành "40" + "%").

Timestamps này là thứ MỌI CÁI KHÁC (cắt scene, timing punch-phrase, cue SFX) sync theo
— làm đúng bước này trước.

## 2. Chia script thành scenes

Dùng chính ranh giới segment (srt block / Whisper segment) làm ranh giới scene — chúng
đã theo nhịp thở/câu tự nhiên, đọc hơn hẳn chia đều máy móc theo thời lượng. Hook ~15s
thường ~4 scene; script dài hơn thì nhiều scene tỉ lệ thuận, nhưng đừng ép min/max —
để câu văn quyết.

Mỗi scene chốt:
- **tag** — MỘT từ/số ngắn treo cả scene dạng chip highlighter (năm, con số, dấu "?").
- **punch phrase** — MỘT câu highlight ngắn bám vào một TỪ cụ thể trong câu, không phải
  caption chạy. Chọn từ nó phải hiện lên, tính `appearAt` theo frame LOCAL của scene:
  `round(word.start * 30) - sceneStartFrame`. Đây là quyết định style lớn nhất mà draft
  đầu từng làm sai: caption bar chạy từng chữ dưới đáy đọc là "basic" — look Vox dùng
  pull-quote đơn lẻ, timing hoàn hảo.
- **hero image** — chủ thể visual trung tâm nhất của câu (cái điện thoại, cú bắt tay,
  gương mặt sốc).
- **2-4 support elements** — cutout nhỏ hơn, củng cố nội dung CỤ THỂ của câu, không
  trang trí chung chung. "Thị phần toàn cầu" xứng quả địa cầu + bar chart; "điều giới
  phân tích bỏ lỡ" xứng kính lúp + trang báo cáo. Nghĩ như một editor người thật sẽ với
  lấy cái gì.
- **variant** — xem bước 6; không để 2 scene liên tiếp trùng.

## 3. Tải ảnh

Với mỗi hero + support element, tìm Pexels. Hai đường:
- **Có API key** (workspace này có: `Projects/youtube-jp-health/tools/.pexels_key` hoặc
  env `PEXELS_API_KEY`) → gọi API search thẳng, nhanh nhất.
- **Không key** → duyệt browser: mở `https://www.pexels.com/search/<query url-encoded>/`,
  `read_page` — URL tải trực tiếp `images.pexels.com/.../pexels-photo-....jpeg` nằm ngay
  trong href. `curl` thẳng về `public/`.

**Chọn kết quả nào quan trọng hơn tưởng.** rembg (bước 4) đoán foreground/background —
nó làm tốt với chủ thể chụp trên nền màu trơn hoặc ngoài trời, và làm **tệ** với chủ thể
nằm trên giấy trắng / giữa các vật trắng khác (không biết chủ thể kết thúc ở đâu, "nền"
giấy bắt đầu ở đâu). Đã có ca: ảnh kính-lúp-trên-tài-liệu mất gần hết chỉ còn mẩu rác,
trong khi ảnh kính-lúp-nền-xanh-trơn gần giống hệt thì cắt hoàn hảo. Query trả cả hai
loại → chọn bản nền trơn/chủ thể tách bạch dù bản kia "đúng theme" hơn — crop chặt lại
sau vẫn đọc tốt.

Lấy thêm 1 ảnh texture giấy làm nền (query kiểu "white paper texture subtle background")
— ảnh thật + tint đọc chất tay hơn hẳn màu CSS phẳng, và chỉ cần tải 1 lần/video vì cùng
file lót dưới mọi scene.

Search thật sự không ra gì → gen ảnh bằng Google Flow trên browser thay vì dừng lại hỏi.
Chỉ hỏi user tự cấp ảnh khi cả hai nguồn đều bó tay.
⚠️ **Ảnh AI gen thì phải xoá watermark ✦ trước khi dùng** (luật workspace
`media-library.md` §2.10 ⑤b — mọi ảnh AI, không ngoại lệ).

## 4. Biến ảnh thành cutouts

Chạy mọi ảnh đã tải qua script đóng kèm skill:

```bash
python E:\Claude\.claude\skills\vox-collage-video\scripts\process_cutout.py ^
  public/raw_phone.jpg public/el_phone.png ^
  public/raw_globe.jpg public/el_globe.png
```

Script cắt nền, bỏ mảnh mask rời rembg để sót (bóng đổ, phản chiếu bị đoán nhầm là
foreground), thêm viền sticker giấy trắng mỏng, và — bước quan trọng nhất — **crop sát
nội dung thật** với margin nhỏ. Bỏ crop thì một chủ thể có 80% padding trong suốt xung
quanh (cực kỳ phổ biến thẳng từ rembg ra) sẽ nhìn bé bất kể layout box to cỡ nào; script
in cảnh báo nếu kết quả vẫn sparse sau crop để sanity-check.

**Soi vài output bằng mắt trước khi đi tiếp** — composite 1-2 cái lên màu trơn (PIL:
`Image.new("RGBA", im.size, (40,60,90,255))` rồi `alpha_composite`) và xem. Bắt cutout
hỏng ở đây rẻ hơn nhiều so với phát hiện sau khi cả scene đã wire xong.

## 5. Sinh SFX

```bash
python E:\Claude\.claude\skills\vox-collage-video\scripts\generate_sfx.py public/sfx
```

Synth 11 one-shot ngắn local — whoosh, pop, coin, thud, boing, swipe, click, riser,
drop, shatter, paper — docstring của script ghi mỗi cái để làm gì và pair tự nhiên với
variant nào. Wire vào qua helper `Sfx` trong scene mẫu, đặt tại đúng beat mỗi tiếng
thuộc về (frame entrance của hero, tag pop ở frame ~6, `appearAt` của punch-phrase,
`delay` của từng support) thay vì dồn hết vào frame 0. Volume giữ khẽ (0.3-0.55) —
chúng là texture dưới narration, không cạnh tranh với nó.

Coi pairing là điểm xuất phát, không phải luật: video mà scene nào cũng chơi đúng 2-3
tiếng thì flat y như video dùng 1 animation cho mọi scene. Chủ động rải cả bộ qua các
scene, và nếu nội dung một scene cần tiếng mà 11 cái này không gợi được — mở rộng script
bằng một one-shot numpy nữa thay vì đi tìm sample library ngoài.

## 6. Build scene

Copy `references/example-scene.jsx` (trong folder skill) thành `src/<VideoName>.jsx`,
đổi tên component + 2 hằng export, điền `SEGMENTS` bằng nội dung thật từ bước 2-5.
Comment trong file giải thích từng mảnh; bản ngắn:

- **GridBackground** — ảnh giấy thật + tint + lưới SVG + 2 blob màu mềm (màu đổi theo
  scene) + cụm chấm halftone. Tái dùng y hệt qua các scene.
- **TitleTag** — chip highlighter cố định, entrance khớp `variant` để vào nhịp với hero.
- **PunchPhrase** — MỘT highlight/scene (xem bước 2 — đừng biến ngược lại thành caption bar).
- **Cutout** — hero, box ~1300-1350px trong khung 1920x1080. Mỗi scene một entrance
  thật sự khác nhau, không bao giờ để 2 scene liên tiếp trùng. `rise`/`grow`/`punch`/
  `flip` code sẵn trong scene mẫu; `references/animation-variants.md` có thêm 6 cái
  (shatter, peel, unfold, spiral, wobble-drop, zoom-through) kèm note implement + SFX
  pairing — đọc nó trước khi quay lại 4 cái cũ, nhất là video >4 scene. Tự chế variant
  mới khớp đúng động từ của câu ăn đứt việc chọn từ menu cố định. Sau khi entrance xong,
  idle bob/sway/breathe biên độ nhỏ chạy LIÊN TỤC để cutout không thành ảnh chết.
- **SupportElement** — 2-4 cutout phụ, `delay` so le để chúng pop lần lượt, mỗi cái một
  phase idle riêng để không bao giờ bồng bềnh đồng bộ.

Giữ 1920x1080/30fps trừ khi user chỉ định tỉ lệ khác.

## 7. Đăng ký và preview

Thêm import + block `<Composition>` vào `src/Root.jsx`, bám đúng pattern các scene
khác trong đó.

Verify bằng Remotion Studio: chạy **nền** `npx remotion studio` trong project rồi mở
`http://localhost:<port>/<CompositionId>`, scrub qua timeline từng scene kèm screenshot.
**Không cần render MP4** — Studio preview chạy composition (cả audio lẫn mọi `<Sequence>`
SFX) trực tiếp, và bản live đó là deliverable trừ khi user đòi file xuất.

Tab Studio kẹt / không ăn scrub-click (đã quan sát thấy sau khi hot-reload lỗi vẽ lại
state lỗi cũ) → restart hẳn (kill process studio, chạy lại, mở lại URL composition) —
refresh tab đơn thuần không phải lúc nào cũng đủ. Chỉ fallback
`npx remotion render <CompositionId> out/<name>.mp4 --overwrite` + rút frame bằng
`ffmpeg -ss <giây> -i out/<name>.mp4 -frames:v 1 -update 1 <scratchpad>/check.jpg`
làm sanity-check cuối khi Studio thật sự không hợp tác sau restart, hoặc user muốn file.
(Kiểm nhanh không cần Studio: `npx remotion still <CompositionId> --frame N out.png`.)
⚠️ Render MP4 dài thì theo luật workspace `render-background.md`: chạy nền + log + EXITCODE.

## Những cái các bản thử trước làm SAI (đừng lặp lại)

- Card ảnh chữ nhật viền giấy xé KHÔNG phải look Vox — nền phải THẬT SỰ bị cắt để
  silhouette của chính chủ thể lộ ra, không phải một hình chữ nhật chứa chủ thể.
- Caption bar chạy từng chữ dưới đáy đọc là generic/basic. Dùng pattern tag cố định +
  punch-phrase đơn timing chuẩn thay thế.
- Tái dùng 1 entrance cho mọi scene đọc là flat. Chủ động đổi từng scene.
- Cutout đứng im sau khi entrance xong nhìn đông cứng/chết — luôn lót idle motion biên
  độ thấp chạy liên tục dưới bất kể animation riêng của scene đang làm gì.
- Element nhìn bé dù layout box rộng rãi nếu PNG nguồn còn nhiều padding trong suốt —
  luôn crop theo content bounds (bước 4 tự làm, nhưng double-check cái nào nhìn lệch).
- rembg làm tệ với chủ thể chụp trên giấy trắng/tài liệu — né từ khâu CHỌN ảnh (bước 3)
  chứ đừng vật lộn sửa sau.
- Video mà scene nào cũng cùng 1-2 tiếng SFX flat y như video dùng chung 1 entrance —
  rải cả bộ SFX qua các scene như cách đổi animation variant.
- Đừng lấy render MP4 làm cách kiểm tra mặc định — Studio preview đã chạy audio + SFX +
  mọi animation live, render chậm hơn mỗi vòng lặp. Chỉ render khi Studio kẹt thật sau
  restart, hoặc user muốn file xuất.
