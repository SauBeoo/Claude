# Trả lời email compliance review của YouTube API — mail + screencast (tái dùng mọi kênh)

> Sau khi nộp form audit (theo `API_SETUP_GUIDE.md`), đội **YouTube API Services Compliance Review** thường gửi email hỏi thêm — điển hình 3 thứ:
> ① script HOẶC screencast cho thấy cách upload video qua API + ② link kênh + ③ số video upload/ngày.
> File này là bộ trả lời chuẩn (đã dùng cho **chouhen 2026-07-21**). Kênh sau bị hỏi y hệt → đổi tên kênh + channel_id + tần suất rồi gửi lại.

---

## 0. Nguyên tắc vàng
- **Nhất quán tuyệt đối với form đã nộp.** Google đối chiếu chéo email vs form — lệch con số/mô tả = nghi ngờ. Use-case, tần suất, "tự dùng / không bên thứ ba" phải trùng khớp `API_SETUP_GUIDE.md`.
- Trả lời **trong 7 ngày làm việc** (deadline họ cho). Trả lời nhanh, gọn, đúng trọng tâm.
- Đính kèm **chính file `upload_api.py`** làm "script" — nó lộ rõ 3 lệnh `videos.insert` / `thumbnails.set` / `captions.insert`, minh bạch.

## 1. MAIL TRẢ LỜI (tiếng Anh — copy dán, đổi phần [đổi theo kênh])

```
Subject: Re: YouTube API Services Compliance Review — additional information

Hi,

Thank you for the follow-up. Please find below the requested information.

1. YouTube channel link(s)

The API client uploads only to my own single channel:
真夜中の朗読便 — https://www.youtube.com/channel/UCuzbgcFHVmAf4O6wU1wLyIQ
[đổi theo kênh: tên kênh + link https://www.youtube.com/channel/<channel_id>]

2. Number of videos uploaded per day

The channel publishes roughly 1-2 videos per week in total. On any given day
this means 0 uploads on most days, and at most 1 upload on an upload day. It is
a personal, low-volume channel - I do not do bulk or automated multi-video
uploads.
[đổi theo kênh nếu tần suất khác - nhưng phải khớp use-case trong form]

3. How videos are uploaded via the API (script)

The API client is a private command-line tool (Python + google-api-python-client)
that runs locally on my personal Windows computer. It is not a website or hosted
service, has no other users, and is not distributed to anyone. It authorizes only
my own channel via OAuth 2.0 and writes only to that channel.

For each of my own finished videos, one run of the tool performs, in order:
- videos.insert - uploads the video file (resumable upload) with the title,
  description and tags I wrote myself, and sets a scheduled publish time
  (status.publishAt).
- thumbnails.set - sets my own custom thumbnail image.
- captions.insert - uploads my own subtitle (.srt) file.

The tool does not read, collect, store or process any data belonging to other
users or channels. It only reads my own channel's basic profile (via
channels.list mine=true) to confirm the authorized channel before uploading.
No analytics or reporting data is retrieved, and nothing is shared with any
third party.

I have attached the source code of the tool (upload_api.py) so you can see the
exact API calls, together with a short screen recording of the full upload flow.
Please let me know if you need anything further.

Best regards,
[Tên thật]
Individual content creator - 真夜中の朗読便 [đổi theo kênh]
```

**Đính kèm:** `upload_api.py` + `screencast_api_upload.mp4` (mục 3).

## 2. KỊCH BẢN QUAY SCREENCAST (--dry-run, an toàn, ~60-90s)

Lệnh dry-run = xác thực OAuth thật + in toàn bộ upload plan, KHÔNG upload, KHÔNG đụng file. Đủ chứng minh cơ chế khi đi kèm source code.

**Chuẩn bị:** `Win + G` (Xbox Game Bar) hoặc OBS, quay cửa sổ PowerShell mở sẵn tại thư mục project.

| Cảnh | Thời lượng | Làm gì |
|---|---|---|
| 1 | ~10s | Mở `upload_api.py` trong editor, lướt qua các dòng có `videos().insert` (~195), `thumbnails().set` (~225), `captions().insert` (~231) — lộ 3 lệnh API. |
| 2 | ~40s | Gõ + chạy: `python tools/upload_api.py <slug> --dry-run` (kênh khác thêm `--channel <key>`). |
| 3 | ~15s | Dừng màn hình ở output — quay RÕ 2 dòng: `kênh auth: <tên kênh> (<channel_id>)` và `✅ DRY-RUN OK`, cùng khối `UPLOAD PLAN`. |
| 4 | +10s (tùy chọn) | Mở tab `studio.youtube.com` đã login đúng kênh → chứng minh là chủ kênh. |

Lưu `screencast_api_upload.mp4`.

> Muốn screencast MẠNH hơn (thấy transfer thật) → dùng `--no-publish` upload thật lên private. ⚠️ Nhưng tool sẽ tự move video sang `07_UPLOADED/` + cắt TikTok + xóa mp4 gốc sau đó (video vẫn an toàn trên YT, re-render được từ `_scripts/`). Cân nhắc trước khi chọn cách này.

## 3. Output dry-run mẫu ĐÃ VERIFY (chouhen, 2026-07-21)

```
── UPLOAD PLAN — 07_amamidokoro-saikaihatsu → 真夜中の朗読便 ──
  video    : 07_amamidokoro-saikaihatsu.mp4 (1406 MB)
  title    : 「土下座して泣きついてきたのは…【スカッと…
  tags     : 19 tag · category 24 · lang ja
  srt      : có   thumbnail: có
  公開      : 2026-07-24 (Thứ Sáu) 18:00 JST = 16:00 giờ VN
  kênh auth: 真夜中の朗読便 (UCuzbgcFHVmAf4O6wU1wLyIQ)
✅ DRY-RUN OK — auth + metadata + file đều sẵn sàng.
```

## 4. Channel_id các kênh (lấy từ CHANNELS trong upload_pack.py — điền vào mail mục 1)

| Kênh | Tên | channel_id | Link mục 1 |
|---|---|---|---|
| chouhen | 真夜中の朗読便 | UCuzbgcFHVmAf4O6wU1wLyIQ | youtube.com/channel/UCuzbgcFHVmAf4O6wU1wLyIQ |
| health | みんなの健康ノート | UCnoYb7aEKy1NgspYTKwhh1Q | youtube.com/channel/UCnoYb7aEKy1NgspYTKwhh1Q |
| co-dai | 古代の秘訣 | UCVlmm1sz7cvTIQ3uSaSct_w | youtube.com/channel/UCVlmm1sz7cvTIQ3uSaSct_w |
| shokutaku | 60代からの食卓 | UCj_QueccfLclCHR5_0vys1Q | youtube.com/channel/UCj_QueccfLclCHR5_0vys1Q |
| kr-romfan / nenkin / stickman | — | (điền sau lần auth đầu) | — |

> Kênh chưa có channel_id → sau khi chạy `auth_test.py` lần đầu, copy id in ra vào `CHANNELS` (upload_pack.py) rồi cập nhật bảng này.
