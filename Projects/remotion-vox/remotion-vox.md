# remotion-vox — video editor kiểu CapCut trên nền Remotion

Nâng cấp lớn **2026-08-15** (từ repo demo 1 file JSX): giờ là **tool dựng video
data-driven + editor web local**. State của video = **1 file `project.json`**
(Zod-validated) — một composition Remotion generic (`VoxProject`) render mọi
project. Editor chỉ đọc/ghi JSON, **cấm write-back vào JSX** (bài học Studio
drag-edit ghi transform rác vào `OkuraDemo.jsx` cũ — bản đó còn ở `legacy/`).

## Chạy

```cmd
run_editor.cmd            :: double-click — server API (7788) + editor (5599)
```
hoặc tay:
```bash
npm run server            # Express API  http://127.0.0.1:7788
npm run editor            # Vite editor  http://localhost:5599
npm run typecheck         # tsc --noEmit
npx remotion render VoxProject --props=projects/<name>/project.json out/<name>.mp4
npx remotion still  VoxProject --props=projects/<name>/project.json --frame N x.png
```

## Cấu trúc

```
projects/<name>/project.json     # state — nguồn sự thật duy nhất (+ .bak, assets_manifest.json)
public/projects/<name>/assets/   # asset per-project (staticFile resolve cả Player lẫn render)
public/sfx/                      # 11 SFX numpy dùng chung
templates/<channel>.json         # 9 template kênh, SINH từ channels.py (đừng sửa tay)
src/schema/project.ts            # ⭐ hợp đồng trung tâm — Zod schema
src/compositions/VoxProject.tsx  # composition generic duy nhất (+ calculateMetadata)
src/components/                  # Background · Sticker · TextClip · Footage · CaptionLayer
src/effects/                     # entrances (9 variant + exits) · textAnimations
apps/editor/                     # editor React: timeline drag/trim/snap, Player, Inspector,
                                 #   AssetBin, wizard New, template picker, undo/redo (zundo)
server/                          # Express: projects/assets/render/import + job nền (log+EXITCODE)
tools/                           # importer + delivery (python/node, xem bảng dưới)
legacy/                          # JSX cũ (OkuraDemo) — chỉ để tham chiếu
```

## Schema project.json (tóm)

- `tracks[]` — thứ tự mảng = z-order. Track `type`: background · video · sticker · text · audio · caption.
- Clip chung: `{id, from, durationInFrames}` + theo kind:
  - `background`: paper/tint/grid/dots/splash[2]
  - `sticker`: asset PNG cutout, layout{x,y,w,rotation,opacity}, entrance{variant}, idle, shadow
  - `text`: preset tag|punch|plain, animation, color
  - `video` (footage): ảnh HOẶC mp4 full-bleed/boxed, motion pan, `fadeInFrames` (dissolve)
  - `audio`: voice/SFX, volume, trimStartFrames
- `captions`: `lines[]` (nguồn subs.srt SẠCH) + `words[]` (karaoke) + style preset
- `sceneMarkers[]` — semantic, để navigate + auto-edit; `theme` — palette/fonts.

## Tools (pipeline → editor → pipeline)

| Tool | Việc |
|---|---|
| `tools/import_pipeline.py --stem X --channel health --out N` | video pipeline (timeline.json + SLIDES.json + channels.py) → project.json, copy asset kèm sha1 manifest, dissolve theo hồ sơ kênh |
| `tools/auto_collage.py --audio a.mp3 --srt s.srt --out N [--plan p.json]` | audio+srt → draft collage: scene/tag/punch/SFX/entrance xoay vòng; plan có `heroQuery` thì tự Pexels+rembg (gọi script của skill vox-collage-video) |
| `tools/import_caption_job.py --video v.mp4 --srt s.srt --out N [--whisper-words]` | job chỉ-làm-phụ-đề |
| `tools/auto_vlog.py --clips <folder> --out N [--music x.mp3] [--bpm N] [--seconds 15] [--size 1080x1920] [--title ...] [--stickers <folder png>]` | ⭐ **TỰ dựng VLOG beat-sync kiểu CapCut** (công thức reel Edit Không Khó): dò BPM từ nhạc (onset-flux + autocorrelation, numpy — đo thật: track 120bpm dò ra 119.95), cắt clip theo beat, xoay hiệu ứng speed 2.0↔0.5 / mirror / split 3 dải wipe / zoom, tự đặt title + đếm ngược + SFX. Không nhạc → tự synth beat. Wizard editor: tab "VLOG beat-edit" |
| `tools/vv_word_timing.py --project N --channel health` | ⭐ karaoke word-timing từ **mora VOICEVOX** (audio_query, cache sha1, không re-synth) — chính xác hơn Whisper, $0 |
| `tools/export_srt.py --project N` | xuất subs.srt SẠCH (không tag) từ captions.lines |
| `tools/deliver.py --project N --channel K --stem S` | round-trip: render → loudnorm −14 LUFS → đặt mp4+srt vào `06_VIDEO/<stem>/` — **chạy NỀN theo render-background.md** |
| `tools/sync_channel_templates.py` | sinh lại templates/ khi channels.py đổi (so hash) |
| `tools/convert_okura.mjs` | one-off: SEGMENTS cũ → project.json (giữ làm tham chiếu mapping) |

## Render & cache

- Nút 🎬 Render trong editor → server spawn `npx remotion render` **nền**, log
  `jobs/<id>/log.txt` + file `EXITCODE`. Cache render: sha1(project JSON) +
  (size,mtime) mọi asset → `out/.render_cache.json` — đổi 1 asset là render lại,
  không bao giờ skip-vì-file-tồn-tại (luật §2.5).
- Thiếu asset mà project khai → server **chặn render** trả `blocked+missing`
  (luật render-background §1.5).

## Bài học build (2026-08-15)

- **zod v4**: `.partial()` trên field có `.default()` vẫn TỰ ĐIỀN default → layout
  override phải là schema optional thuần (`LayoutOverrideSchema`), không `.partial()`.
- **zundo**: push state-TRƯỚC-lần-set-kế-tiếp → group undo cho drag phải: giữ ref
  project lúc pointerdown → revert ngầm khi thả → resume → apply state cuối.
- **--props = CHÍNH project.json** (props không bọc `{project}}`) — nếu bọc, Remotion
  merge defaultProps và render nhầm sang demo (dính thật, đã sửa).
- Node 21.6: vite 7 (rolldown) đòi `util.styleText` → **pin vite 5.4** +
  `@vitejs/plugin-react-swc@3` + config `.mts`; spawn `.cmd` phải qua `cmd.exe /d /s /c`.
- Pexels 403 nếu thiếu User-Agent (giữ từ bản cũ). Font JP: `"Yu Gothic","Meiryo"`.
- Drag bằng CDP automation flaky (pointer synthetic) — kiểm tay khi nghi ngờ, đừng
  kết luận handler hỏng từ automation.
- **@remotion/player mặc định chỉ cho 5 thẻ audio mount CÙNG LÚC** (shared audio
  tags chống autoplay-block) — project beat-edit (nhạc + SFX chồng dày) vượt ngay
  → Player crash **màn đen**, trong khi render headless vẫn ra mp4 bình thường
  (bắt được 2026-08-16 ở vlog-auto). Fix: `numberOfSharedAudioTags={32}` trên
  `<Player>`. Component định nghĩa TRONG render (bug F của NewProject) cũng bắt
  cùng ngày: input mất focus mỗi keystroke vì React remount — khai báo module-level.

## Bổ sung cùng ngày (vòng 2)

- **Thanh ➕ trên timeline**: Text / Tag / Punch / Nền / BGM — chèn clip mới tại
  playhead, tự tạo track nếu thiếu. BGM upload file → clip audio volume 0.01 (−40dB).
- **Filter màu cho footage** (CapCut-style): `filter{brightness,contrast,saturate,
  grayscale,sepia,blur}` trong schema + slider trong Inspector.
- Inspector footage có field `dissolve (frames)`; không chọn clip → panel Project
  chỉnh phụ đề (bật/tắt · style · font size · đếm dòng/từ karaoke).

## Việc còn mở

- Caption word retime/split trong UI (sửa được qua JSON).
- Entrance `shatter`/`unfold` (cần clipPath multi-element) chưa implement — 9/11 đã có.
- `@remotion/transitions` đã cài nhưng chưa wire track-transition (dissolve hiện đi
  qua `fadeInFrames` — đủ cho luật 45+).
- Chưa có waveform audio trên timeline (`@remotion/timeline-utils` sẵn trong deps).
- vox-collage-video SKILL.md: flow mới (auto_collage + editor) là đường ưu tiên;
  flow JSX cũ vẫn chạy nhưng đừng dùng cho video mới.
```
