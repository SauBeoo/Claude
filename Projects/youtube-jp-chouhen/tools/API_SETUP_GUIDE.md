# Đăng ký YouTube Data API + audit — hướng dẫn từng bước (1 kênh / 1 Gmail / 1 project)

> Mô hình đã chốt (2026-07-18): **mỗi kênh 1 Google Cloud project riêng, do chính Gmail của kênh đó đứng tên** — cô lập hoàn toàn, kênh die không dính kênh khác. Làm cuốn chiếu: chouhen trước, đậu audit rồi lặp lại y hệt cho 5 kênh sau (đổi Gmail + tên).
> Toàn bộ thao tác làm bằng **Chrome profile đăng nhập đúng Gmail của kênh đó**. Mất ~30 phút + chờ Google duyệt (vài ngày → vài tuần).
> Trong lúc chờ: vẫn upload bằng `upload_pack.py` (bán tự động) như bình thường.

---

## ⭐ ĐƯỜNG TẮT: chỉ cần ANALYTICS (KHÔNG cần audit) — ~10 phút/kênh

> `analytics_report.py` chỉ ĐỌC số liệu (scope `youtube.readonly` + `yt-analytics.readonly`). **Đọc KHÔNG bị audit chặn** — audit chỉ khóa việc *upload công khai* qua API. Nên để bật analytics cho 1 kênh, chỉ cần **Bước 1 → 2 → 3 → 4** dưới đây rồi chạy `auth_test.py`. **BỎ QUA Bước 5, 6, 7** (form audit).
>
> Token tạo xong dùng được cho CẢ `analytics_report.py` (ngay lập tức) LẪN `upload_api.py` sau này (khi kênh đó đậu audit) — vì `auth_test.py` xin sẵn đủ 4 scope.

**Tóm tắt 5 bước cho analytics:**
1. **Google Cloud project** cho kênh (Bước 1) — hoặc tái dùng project đã có của kênh đó.
2. **Bật 2 API** (Bước 2): YouTube Data API v3 **+ YouTube Analytics API** (thiếu cái thứ 2 → 403 `accessNotConfigured` khi xem retention).
3. **OAuth consent** (Bước 3): tạo consent screen. Để analytics chạy dài lâu KHÔNG phải Allow lại mỗi 7 ngày → **Publish App → In production** (readonly < 100 user không cần verify). Không muốn publish cũng được: để "Testing" + thêm chính Gmail kênh vào **Test users**, token sống 7 ngày rồi chạy lại `auth_test.py`.
4. **OAuth Client (Desktop)** (Bước 4): tải `client_secret.json` về `Projects\<kênh>\credentials\client_secret.json` (folder đã tạo sẵn).
5. **Tạo token:** mở Chrome đúng Gmail kênh rồi chạy — **bảo Claude chạy hộ, hoặc gõ `!` trong phiên:**
   ```
   python E:\Claude\Projects\youtube-jp-chouhen\tools\auth_test.py --channel-dir E:\Claude\Projects\<project-kênh>
   ```
   Browser mở → chọn ĐÚNG tài khoản/kênh → "app chưa verify" thì **Advanced → Go to… (unsafe) → Continue** → Allow. Xong in ra `✅ ĐÃ CẤP QUYỀN CHO KÊNH: <tên kênh>` + tạo `credentials/token.json`.
   → Sau đó: `python tools/analytics_report.py --channel <key>` (hoặc `--all`) chạy được ngay. Kênh mới nhớ copy `channel id` in ra vào field `channel_id` của kênh trong `CHANNELS` (upload_pack.py).

Trạng thái hiện tại (2026-07-20): chỉ **chouhen** có token. 6 kênh còn lại (health/shokutaku/co-dai/kr-romfan/nenkin/stickman) đã tạo sẵn folder `credentials/`, chỉ thiếu `client_secret.json` + chạy `auth_test.py`.

---

## Bước 1 — Tạo Google Cloud project (~3 phút)

1. Mở https://console.cloud.google.com (đăng nhập Gmail của kênh). Lần đầu sẽ hỏi đồng ý Terms → tick → Agree.
2. Thanh trên cùng → chọn ô project → **New Project**.
3. Project name: `chouhen-uploader` (kênh khác đổi tên: `shokutaku-uploader`…). Location để nguyên "No organization" → **Create**.
4. Chờ vài giây, chọn vào project vừa tạo (kiểm tra tên project hiện trên thanh trên cùng).

## Bước 2 — Bật API (~2 phút, bật CẢ HAI)

1. Menu ☰ → **APIs & Services → Library**.
2. Tìm `YouTube Data API v3` → bấm vào → **Enable** (upload/đọc video).
3. Tìm `YouTube Analytics API` → **Enable** luôn (retention/traffic/keyword — cho analytics_report --video; quên bật sẽ dính 403 accessNotConfigured như chouhen 2026-07-19).

## Bước 3 — OAuth consent (Google Auth Platform) (~5 phút)

1. Menu ☰ → **APIs & Services → OAuth consent screen** (giao diện mới tên là **Google Auth Platform** → Get started).
2. Điền:
   - **App name:** `Chouhen Studio Uploader` — ⚠️ KHÔNG nhét chữ "YouTube" vào tên app (dính trademark, dễ bị từ chối).
   - **User support email:** Gmail của kênh.
   - **Audience / User type:** **External**.
   - **Contact email:** Gmail của kênh.
   - Đồng ý policy → **Create / Finish**.
3. Tab **Audience** → bấm **Publish App** → xác nhận chuyển sang **In production**.
   - ⚠️ BẮT BUỘC bước này. Để ở "Testing" thì token hết hạn sau 7 ngày, phải Allow lại hoài.
   - Sẽ có cảnh báo kiểu "app needs verification" — **kệ nó, không cần verify OAuth** (app dưới 100 user, tự mình dùng). Lúc bấm Allow sau này màn hình sẽ hiện "Google hasn't verified this app" → bấm **Advanced → Go to … (unsafe)** → Continue. Bình thường.

## Bước 4 — Tạo OAuth Client (Desktop) (~2 phút)

1. **APIs & Services → Credentials** (hoặc Google Auth Platform → tab **Clients**) → **Create Credentials → OAuth client ID**.
2. Application type: **Desktop app**. Name: `uploader-desktop` → **Create**.
3. Bấm **Download JSON** → lưu file thành:
   `E:\Claude\Projects\youtube-jp-chouhen\credentials\client_secret.json`
   (kênh khác: `Projects\<project-kênh>\credentials\client_secret.json`)
   - ⚠️ File này là chìa khóa — KHÔNG commit git (folder `credentials/` + `tokens/` đã nằm trong `.gitignore` gốc), không gửi ai.

## Bước 5 — Ghi lại 2 con số cho form audit (~1 phút)

1. Menu ☰ → **IAM & Admin → Settings** → copy **Project number** (dãy số, khác Project ID).
2. Ở Credentials → copy **Client ID** (dạng `xxxx.apps.googleusercontent.com`).
3. Ghi tạm 2 số này vào Notepad.

## Bước 6 — Nộp form audit (~10 phút)

- Form: **https://support.google.com/youtube/contact/yt_api_form** (YouTube API Services — Audit and Quota Extension Form). Mở bằng đúng Gmail chủ project.
- Câu đầu (loại yêu cầu): chọn phương án **compliance audit** (audit lần đầu / "have not yet completed an audit"). KHÔNG chọn quota extension — mình không xin thêm quota.
- Điền thông tin liên hệ = Gmail kênh, tên thật.
- **Project number / Client ID:** dán 2 số ở Bước 5.
- Phần mô tả use case — dán bản viết sẵn dưới (sửa tên kênh cho đúng):

```
This API project is used solely by me, the owner and operator of the YouTube
channel "真夜中の朗読便", to upload my own original videos to my own channel.

The API client is a private command-line tool (Python + google-api-python-client)
that runs locally on my personal Windows computer. It is not a website, has no
other users, and is not distributed to anyone else.

Functionality (single user = channel owner):
- videos.insert: upload my finished video file with the title, description and
  tags that I wrote myself, and set a scheduled publish time (status.publishAt).
- captions.insert: upload my own subtitle (.srt) file for the video.
- thumbnails.set: set my own custom thumbnail image.

The tool does not access, collect, store or process any data belonging to other
users or other channels. It only writes content to my own channel through my own
authorized account. No analytics or reporting data is retrieved.

Expected volume: 1–2 video uploads per week (about 3,200–4,100 quota units per
week in total), far below the default 10,000 units/day. I am NOT requesting a
quota extension — this submission is for the compliance audit so that videos
uploaded through this project can be set to public visibility.
```

- Nếu form hỏi link demo/screenshot: ghi chú tool là CLI cá nhân, đính kèm screenshot cửa sổ console chạy tool + screenshot YouTube Studio của kênh (chứng minh mày là chủ kênh).
- Gửi xong sẽ có email xác nhận. **Google hay hỏi lại qua email** — trả lời nhanh, nhất quán với mô tả trên (tự dùng, kênh của mình, không có bên thứ ba).

### Form thực tế có 7 mục (bản 2026, đã đối chiếu khi nộp chouhen 2026-07-18) — đáp án từng mục

1. **Loại yêu cầu:** chọn option ĐẦU "Hoàn tất quy trình kiểm tra việc tuân thủ để yêu cầu hạn mức bổ sung" (option 2 chỉ cho người bị Google yêu cầu re-audit).
2. **Tổ chức & liên hệ:** tên thật, email = Gmail kênh, công ty: `Individual content creator (personal project, no company)`, website = link kênh.
3. **Mô hình kinh doanh & Danh bạ Google:** `I am an individual YouTube creator producing original long-form videos for my own channel. The channel is not yet monetized; planned future revenue is standard YouTube Partner Program ads. The API tool is not a product or service offered to anyone — it is a private script used only by me to upload my own videos to my own channel. I do not provide API functionality to any third party.` — Google contact: No.
4. **Tổng quan ứng dụng & truy cập:** Project number + Client ID (Bước 5); API: `YouTube Data API v3 — videos.insert, captions.insert, thumbnails.set`; URL/access: `Local command-line tool (Python) on my personal Windows computer. No website or public URL, not distributed. I can provide a screen recording or screenshots of the full upload flow on request.`
5. **Use case & hạn mức:** dán khối use case ở trên + `The default 10,000 units/day is sufficient (~3,200–4,100 units/week). I am not requesting additional quota — I am completing this compliance audit so that videos uploaded through this project can be set to public visibility.`
6. **Bằng chứng:** screenshot console chạy tool + screenshot YouTube Studio kênh; không có ô đính kèm thì ghi `Screenshots / screen recording available on request.`
7. **Chứng thực & gửi:** tick xác nhận, ký tên, Gửi.

### ⚠️ Kinh nghiệm điền thật (chouhen 2026-07-18) — các bẫy đã gặp

- **"Bạn đăng ký:" → chọn "người dùng cá nhân"**, KHÔNG chọn tổ chức (tổ chức bị đòi giấy tờ pháp nhân). "Tên pháp lý tổ chức" → ghi `Myself` (form hint: "bản thân"), KHÔNG ghi tên kênh.
- **Quy mô/Loại tổ chức → "Nhà phát triển độc lập/Doanh nghiệp tư nhân"** (không phải "Công ty khởi nghiệp").
- **"Tên Ứng dụng API" = TÊN app** (`Chouhen Studio Uploader`), không phải project number. Project number điền ở Mục 5 sau khi chọn "thêm 1 mã số dự án".
- Quốc gia: chọn đúng nước trong dropdown, tránh "Khác".
- Người liên hệ kỹ thuật/kinh doanh: tick "Giống như người liên hệ chính".
- Kiếm tiền: tick "Khác" + `The API application itself generates no revenue — free private tool used only by me. Future channel revenue would be standard YouTube Partner Program ads, unrelated to the API tool.`
- **"URL truy cập chính"** = link kênh YouTube. **"URL chính sách bảo mật" (bắt buộc)** = tạo Google Sites 5 phút bằng Gmail kênh, dán Privacy Policy mẫu dưới, Publish, lấy URL. "Truy cập công khai?" → Không.
- Mục 6: bằng chứng ảnh PNG/JPEG/PDF, ≥720p, <10MB/tệp — screenshot console chạy tool + YouTube Studio kênh.
- Mục 7: tick hết các ô *.

### Privacy Policy mẫu (dán vào Google Sites — đổi tên app/kênh theo từng kênh)

> Bản đầy đủ (đã bổ sung mục **Data deletion policy** + khối **Terms of Service** — bằng chứng audit Mục 5 đòi thấy: nhắc YouTube API, link Google Privacy Policy, chính sách xóa):

```
Privacy Policy — <App Name>

Last updated: <ngày>

<App Name> ("the tool") is a private command-line application used exclusively
by its owner to upload videos to the owner's own YouTube channel. It is not
distributed to, or usable by, anyone else.

1. Use of YouTube API Services. The tool uses YouTube API Services. By using
   the tool, its user (the owner) agrees to be bound by the YouTube Terms of
   Service (https://www.youtube.com/t/terms). Google's handling of data is
   described in the Google Privacy Policy (https://policies.google.com/privacy).

2. Data the tool accesses. Through OAuth 2.0 authorization granted by the
   owner, the tool accesses only the owner's own YouTube channel in order to:
   upload video files, set titles/descriptions/tags, upload subtitle (.srt)
   files, set custom thumbnails, and set scheduled publish times. It also reads
   the channel's basic profile (name) to confirm the authorized channel.

3. No third-party data. The tool does not access, collect, share, or sell any
   data belonging to any other user or channel. It has no analytics, no
   advertising, no cookies, and no tracking. Data is never transferred to any
   third party.

4. Data storage. The only data stored is the OAuth token (authorization
   credential), saved locally on the owner's personal computer. It is never
   transmitted anywhere except to Google's official API endpoints over HTTPS.
   No YouTube user data is stored by the tool.

5. Data deletion policy. Stored authorization data can be deleted at any time
   by deleting the local token file (credentials/token.json) on the owner's
   computer. The tool keeps no other stored data, so this removes all data
   held by the tool. To request deletion of any data or ask questions, contact
   the email below; requests are honored immediately.

6. Revoking access. In addition to deleting the token file, API access can be
   revoked at any time via Google security settings:
   https://myaccount.google.com/permissions

Contact: <Gmail của kênh>

Terms of Service — <App Name>

This is a private, non-commercial tool used solely by its owner to upload the
owner's own videos to the owner's own YouTube channel. The tool uses YouTube
API Services. By using this tool, the user (its owner) agrees to be bound by
the YouTube Terms of Service (https://www.youtube.com/t/terms) and acknowledges
the Google Privacy Policy (https://policies.google.com/privacy).
```

### Bằng chứng Mục 5 (bắt buộc, mỗi ô 1 ảnh PNG ≥720p <10MB, URL thanh địa chỉ phải lọt vào ảnh)
- a) Privacy: chụp mục 1+4+5 của trang Sites (thấy "YouTube API Services", link Google Privacy Policy, "Data deletion policy").
- b) Homepage: chụp đầu trang Sites (tiêu đề app + đoạn có chữ YouTube).
- c) Terms: chụp khối Terms of Service cuối trang.
- Bằng chứng CÓ ĐIỀU KIỆN (OAuth=Có + use case tải video): chạy `python tools/auth_test.py --channel-dir <project>` → chụp màn hình consent + console "ĐÃ CẤP QUYỀN CHO KÊNH" + console `upload_pack.py` → ghép 1 ảnh.
- Mục 5 các ô khác: danh mục use case = "Tải video lên và quản lý tài khoản"; khối lượng = mức thấp nhất; endpoint = videos.insert + captions.insert + thumbnails.set; tổng hạn mức = "Không thay đổi/mặc định".

## Bước 7 — Sau khi đậu audit

> Trạng thái chouhen: **form audit ĐÃ NỘP 2026-07-18** (project 441152731951, đủ bằng chứng privacy/terms/OAuth/CLI). OAuth token đã tạo & verify (`auth_test.py` → 真夜中の朗読便). `upload_api.py` ĐÃ VIẾT + dry-run OK — chỉ chờ email kết quả audit.

Uploader full-auto: **`tools/upload_api.py`** (dùng chung mọi kênh, token theo từng project):
```
python tools/upload_api.py <slug> [--channel <key>] [--dry-run] [--slot "YYYY-MM-DD HH:MM"]
```
- 1 lệnh = upload video (resumable) + title/description/tags + thumbnail + subs.srt + **hẹn giờ công khai** (publishAt) tự tính theo `.claude/rules/upload-schedule.md`.
- Quota ~2.050 units/video (videos.insert 1600 + captions 400 + thumbnail 50) — mặc định 10k/ngày dư sức.
- ⚠️ Trước khi audit đậu: video upload qua API bị khóa private → chỉ `--dry-run`/test. Audit đậu → dùng thay `upload_pack.py`.
- Quét từ nhạy tự động (chặn upload nếu title/3 dòng đầu dính từ cấm); `--no-publish` = video test private trơn.
- **Hàng rào an toàn (audit code 2026-07-18):** chặn double-upload qua `UPLOADED.txt` (gỡ bằng `--again`) · verify token đúng kênh qua `channel_id` trong CHANNELS (token nhầm Gmail → dừng ngay, in hướng dẫn) · validate trước upload: title ≤100 ký / description ≤5000 / tags tự cắt ≤460 ký · retry 10 lần có backoff cho cả lỗi server 5xx lẫn đứt mạng (upload resumable, không chết giữa chừng).
- Kênh mới đậu audit → chạy `auth_test.py --channel-dir <project>` lần đầu, copy channel id in ra vào field `channel_id` của kênh đó trong CHANNELS.

## Checklist nhân bản cho 5 kênh còn lại (mỗi kênh làm lại Bước 1–6)

| Kênh | Gmail đăng nhập | Project name | App name (không chữ YouTube) |
|---|---|---|---|
| shokutaku | Gmail kênh 60代からの食卓 | `shokutaku-uploader` | `Shokutaku Studio Uploader` |
| health | Gmail kênh health | `health-uploader` | `Kenko Studio Uploader` |
| co-dai | Gmail kênh 古代の秘訣 | `codai-uploader` | `Chie Studio Uploader` |
| kr-romfan | Gmail kênh 사우 오디오 | `saou-uploader` | `Saou Audio Uploader` |
| stickman | Gmail kênh stickman | `stickman-uploader` | `Stickman Story Uploader` |

- Mô tả use case: dùng nguyên bản trên, đổi tên kênh + tần suất nếu khác.
- ⚠️ Nhớ mục tiêu cô lập: mỗi form nộp bằng đúng Gmail kênh đó; không nhắc kênh khác trong form; recovery email/SĐT từng Gmail tách riêng (mày nói sẽ sửa sau — sửa TRƯỚC khi nộp form các kênh sau càng tốt).
