# Render video LUÔN CHẠY NỀN — RULE TOÀN HỆ THỐNG

> **Nguồn sự thật DUY NHẤT** về cách khởi chạy mọi tác vụ render video/voice dài. Áp cho **nenkin** + **showa**.
> Rule này lo **CHẠY THẾ NÀO**; nội dung/style render xem skill `video-render` + CLAUDE.md từng project.

## 0. Ý ĐỒ
Render dài chạy foreground thì treo lượt chat, và gãy giữa đường là **im lặng** (không EXITCODE, không traceback). → Mọi lệnh render chạy nền, log ra file, tao chủ động báo khi xong.

## 1. LUẬT (bắt buộc, không hỏi lại)
1. **MỌI lệnh render/dựng video/synth voice dài chạy NỀN** (`run_in_background: true`):
   - **nenkin** — đường Remotion: `Projects/youtube-jp-nenkin/tools/render_chunks<NN>.py` (§2.6 ⑨–⑩).
   - **showa** — `Projects/youtube-jp-health/tools/video_render.py --channel showa` (+ `finalize.py`).
   - `cta_inject.py` chạy lẻ trên video dài, batch fetch ảnh/clip nhiều chục asset.
2. **Bọc trong `.cmd` + log ra `06_VIDEO/<slug>/render.log`** kèm `EXITCODE`. Log file là bằng chứng, không phải stdout của lượt chat.
3. **"Xong" = 3 thứ:** ① `EXITCODE=0` trong log ② mp4 tồn tại + `ffprobe` duration khớp `subs.srt` ③ **duyệt MẮT ≥4 frame rải đều**. `EXITCODE=0` một mình không chứng minh gì.
4. **Không sleep/poll.** Harness tự gọi lại khi tiến trình kết thúc. Xem tiến độ thì `tail` log 1 lần.
5. **Chết giữa đường** (không EXITCODE, log đứng im): đọc log tìm bước cuối → chạy lại **đúng lệnh cũ** (resume tự skip phần đã có). Đừng đổi tham số khi chưa biết nguyên nhân.
6. Việc <1 phút (thumbnail, 1 frame test, ffprobe, contact sheet) chạy foreground bình thường.
7. **Priority BELOW_NORMAL đã cài trong renderer** (`video_render.py`, `finalize.py`) — đừng cài lại ở `.cmd`. Tắt bằng `--normal-priority`. ⚠️ ctypes: `GetCurrentProcess.restype = c_void_p`, thiếu là fail im lặng trên 64-bit. Renderer mới: chép khối `_low_priority()` từ `video_render.py`.
8. **Nhiều video → XẾP HÀNG TUẦN TỰ, ⛔ cấm render 2 video song song** (máy 6 nhân: không nhanh hơn, máy đơ, tăng rủi ro OOM). Tool: `python E:\Claude\Projects\_media_library\render_queue.py <run1.cmd> <run2.cmd> …` (chạy nền 1 lần).
9. **Chunk bước A của `video_render.py` = `ultrafast` crf 16** (file trung gian, bước B re-encode lại). ⛔ Đừng áp ultrafast cho encode CUỐI.

## 1.5 🔴 ĐỦ ASSET MỚI ĐƯỢC RENDER
Thiếu **bất kỳ** ảnh/clip mà SLIDES/project khai báo → **KHÔNG render video**. Không có "bản tạm xem trước".
- Lý do phải thành gate máy: thẻ `art`/`photo` thiếu ảnh **vẫn ra clip** (ô vàng "CHƯA CÓ ẢNH") → video đầy ô vàng, exit 0.
- Đã cài: `make_stage.py` ghi `clips/_MISSING_ART.json` (đủ ảnh thì xoá); `video_render.py` preflight **④b** đọc sổ và **chặn cứng** (vượt chỉ bằng `--skip-preflight`).
- Thứ tự: `SLIDES → make_stage (ô chờ ảnh) → duyệt chữ/bố cục → đủ ảnh → make_stage lại → sổ RỖNG → render`. Dựng clip lúc chưa có ảnh là ĐÚNG; cái cấm là bước ghép video cuối.
- 🔴 **Thêm khoá asset mới** (`img`, `fill`, …) → **thêm vào tập `want` của sổ cùng lượt**. Cùng luật cho **chữ ký resume `_sig`**: mọi thứ ảnh hưởng hình (spec · asset · icon · palette · hằng số tool) phải nằm trong chữ ký.

### 1.6 `.cmd` nối 2 bước phải chặn ở bước 1
```cmd
python make_stage.py slides ... > "%VD%\stage.log" 2>&1
set SE=%ERRORLEVEL%
echo STAGE_EXIT=%SE% >> "%VD%\stage.log"
if not "%SE%"=="0" ( echo STAGE GAY - BO QUA RENDER >> "%VD%\render.log" & exit /b 1 )
```
Bước 1 đổi hình → **xoá `slides\` (chunk/burn) trước khi render**, không thì resume ra hình cũ.

## 2. KHUÔN LỆNH CHUẨN (chép, đừng gõ lại)
```cmd
@echo off
chcp 65001 >nul
cd /d E:\Claude\Projects\<project>
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
python ..\youtube-jp-health\tools\video_render.py 04_SCRIPTS\<x>_TTS.md --channel showa > 06_VIDEO\<slug>\render.log 2>&1
echo EXITCODE=%ERRORLEVEL% >> 06_VIDEO\<slug>\render.log
```
Gọi: `cmd //c "E:\...\run_render.cmd"` với `run_in_background: true`. (`--channel` đọc hồ sơ kênh `tools/channels.py`; preflight chặn trước khâu voice nếu thiếu asset.)

## 2.5 🔴 RESUME PHẢI BIẾT ASSET ĐÃ ĐỔI
Mọi cơ chế skip-if-exists phải hỏi **"file còn ĐÚNG không"**, không phải "file đã tồn tại chưa": so **mtime output vs input**, hoặc đưa **danh tính nội dung** (tên + mtime + size) vào tên/khoá file trung gian. ⚠️ So **duration** KHÔNG bắt được đổi nội dung (timeline voice không đổi).
```python
if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
    rebuild(src, dest)
```
Đã vá ở `video_render.py` (chunk/trans) + `finalize.py` (burn). Thêm resume mới → áp cùng luật.
**Thao tác tay:** đổi asset xong, đọc log tìm dòng `CŨ HƠN … → render lại`. Không thấy = có gì sai.

## 2.6 🔴 BẪY `.cmd` — đều làm mất bằng chứng mà §1 mục 3 đòi
Chạy **đủ bộ kiểm dưới** mỗi lần tạo hoặc SỬA một `.cmd` (file đúng lần đầu hay hỏng ở bước sửa một dòng).

| # | Bẫy | Luật | Lệnh kiểm |
|---|---|---|---|
| ① | Ký tự ngoài ASCII → cmd đọc comment thành lệnh, exit 0, **không có log file** | `.cmd` **ASCII-only**, comment tiếng Anh không dấu | `python -c "d=open('run.cmd','rb').read();print(sum(b>127 for b in d))"` → 0 |
| ①b | LF-only (sửa bằng Python `newline=""`) → khối `for (...)` không chạy | giữ CRLF | `python -c "d=open('run.cmd','rb').read();print(d.count(b'\r\n'),d.count(b'\n'))"` → hai số bằng nhau |
| ② | `make_stage --still` chỉ ra PNG, không mp4; preflight ④ chỉ **cảnh báo** → video mất lớp động | `--still` → sửa → `make_stage` KHÔNG `--still` → mới render | `echo "png: $(ls clips/*.png\|wc -l) mp4: $(ls clips/*.mp4\|wc -l)"` |
| ③ | `echo X=%V%>> log` — chữ số dính `>>` thành file-handle → `EXITCODE=` rỗng | redirect đặt TRƯỚC: `>> "log" echo EXITCODE=%ERRORLEVEL%`, hoặc có dấu cách | `grep -nE 'echo[^>]*[0-9%]>>?[^>&]' run_*.cmd` → rỗng |
| ④ | Gọi từ Git Bash: coreutils của Git che `timeout`/`find`/`sort`/`tee`/`date`/`printf` | dùng `%SystemRoot%\System32\...` hoặc `ping -n N+1 127.0.0.1 >nul` | `grep -nE '^[[:space:]]*(timeout\|find\|sort\|tee\|date\|printf)[[:space:]]' run_*.cmd` → rỗng |
| ⑤ | Vòng chờ đọc log append-only → bắt dấu của **lần chạy trước** | tín hiệu chờ = chính file sản phẩm **tồn tại + size đứng yên** giữa 2 lần đo, hoặc file cờ `del` ở đầu | — |
| ⑥ | Sinh `.cmd` bằng heredoc Python: `\13` trong đường dẫn thành octal (dấu hiệu `SyntaxWarning: invalid escape`) | ghi bằng Write tool rồi đổi CRLF+ASCII, hoặc đưa phần số vào biến `set STEM=…` | — |
| ⑥b | `npx`/`npm`/`tsc`/`vite` là `.CMD` → thiếu `call` thì mọi dòng sau bị bỏ, mất `EXITCODE` | `call npx …` | `grep -nE '^[[:space:]]*(npx\|npm\|yarn\|pnpm\|tsc\|vite)[[:space:]]' run_*.cmd` → rỗng |
| ⑦ | Vòng chờ hết hạn (`exit 93`) trông y như render hỏng | đọc log của tiến trình ĐANG CHỜ trước khi kết luận; trần chờ tính theo bài DÀI NHẤT, đặt dư | — |

### ⑧ `cta_inject.py` hỏng ở đường Remotion
Trên video Remotion nó làm **mất lớp ảnh** trong cửa sổ re-encode, `CTA_EXIT=0`, và overlay CTA **chưa từng hiện** ở đường này. ⇒ **nenkin (Remotion): BỎ bước `cta_inject`**, giao bản sau `loudnorm`; câu CTA vẫn có trong giọng đọc. Overlay muốn có thì vẽ trong `project.json`. `cta_inject` vẫn dùng cho `video_render.py` (showa). ⛔ Đừng tin `CTA_EXIT=0` — trích frame trong cửa sổ nó in ra.

### ⑨ Remotion không có resume ⇒ video >10′ render theo CHUNK
Dùng `youtube-jp-nenkin/tools/render_chunks<NN>.py` (mẫu mới nhất: `render_chunks26.py`), đừng `remotion render` một mạch. Tool chunk phải có:
1. `--concurrency=2` (không 4 — 4 bị kill vì RAM và còn chậm hơn).
2. Resume so **mtime chunk vs `project.json`**.
3. `--only 3,7` để render lại vài chunk — chỉ khi chắc thay đổi nằm gọn trong đó; đổi hằng số toàn cục thì render lại HẾT.
4. `FPS` là hằng số — port sang project khác fps phải sửa, không thì phép kiểm duration báo lệch 20%.
Chunk nối bằng `concat -c copy`. Muốn rẻ hơn thì dọn `remotion-vox/public/projects/` của project đã đăng.

### ⑩ Remotion bị kill "low memory": 2 nguyên nhân, `--concurrency` không phải một
1. **Cache khung video rò tuyến tính (~16 MB/frame)** → ép trần:
   `--offthreadvideo-cache-size-in-bytes=268435456 --media-cache-size-in-bytes=268435456` (không có trong `--help`; tra `BrowserSafeApis.options.<...>Option.cliFlag`).
2. **Tiến trình mồ côi sau mỗi lần kill** (ăn ~6 GB) → dọn **trước mỗi chunk** (`_kill_orphans()` trong `render_chunks25.py`): chỉ giết `remotion.exe` + `chrome-headless-shell.exe`; ⛔ không đụng `node.exe`, `chrome.exe`, `ffmpeg.exe`.
Kill lần thứ hai là lúc phải **ĐO** (`nenkin/tools/probe25.py`), không phải thử tiếp đường chữa có sẵn.

## 2.7 🔴 BẪY ĐO-LƯỜNG khi nghiệm thu bản render
1. **`drawtext` chết vì thiếu fontconfig**, 0 frame mà script vẫn in "xong" → đừng dùng `drawtext`; đếm file thực tế trước khi ghép.
2. **`volumedetect`/`ebur128`/`astats`/`blackdetect`/`silencedetect` in ở INFO** → `-v error` làm chúng câm. Dùng `-hide_banner -nostats`.
3. **`amix` mặc định chia âm lượng** → luôn `amix=inputs=N:normalize=0`.
4. **`alimiter` đẩy đỉnh sát trần** → `alimiter=limit=0.891`. Nghiệm thu âm = `I` −14 LUFS **và** true peak ≤ −1 dBTP (cụm nenkin ≤ −3 dBTP, `audience-45plus.md`): `ffmpeg -hide_banner -nostats -i x.mp4 -af ebur128=peak=true -f null -`.
5. **Mốc slide = cộng dồn `dur`**, đừng dò câu thoại; kiểm `sum(dur)` khớp độ dài file.
6. `video_render.py` xoá chunk sau concat ⇒ đổi 1 clip vẫn dựng lại **toàn bộ** chunk (~13′) — đừng hứa "chỉ 1 chunk".

## 2.8 🎚️ TRỘN TIẾNG GỐC CỦA CLIP AI (showa)
- ⛔ Tiếng người t2v sinh ra là tiếng bản xứ GIẢ → lọc bằng năng lượng bao 2–8 Hz / tổng: `mod ≥ 0,35` ⇒ loại. Đo trên **đúng đoạn sẽ phát**. Đây là phép đoán → dựng file audition cho user NGHE trước.
- Trộn: nền **−34 dBFS** (`gain = −34 − mean_đoạn`), fade 0,6s, `adelay` đúng mốc, `amix=normalize=0`, `alimiter=limit=0.891`, `-c:v copy`.
- 🔴 Luôn trộn lại **từ bản sạch**. Lô clip đổi ⇒ danh sách ứng viên hết hạn, đo lại từ đầu.

## 3. LIÊN QUAN
- Gate trước render + chính sách asset: `media-library.md` · CTA overlay: `cta-midvideo.md` §5.
- Cơ chế resume chunk của `video_render.py`: skill `video-render` (CHUNK=4 + `finalize.py`).
