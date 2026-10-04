# Upload Schedule — lịch đăng video (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về giờ + ngày đăng. Kênh đang chạy: **nenkin · showa · yawa · kyori · teinengo · kinishinai** (yawa + bộ 3 tâm lý thêm 2026-09-30).
> Metadata/SEO xem `youtube-upload-seo.md`; từ ngữ an toàn xem `youtube-compliance.md`.

## 0. NGUYÊN TẮC GỐC

1. **Đăng trước peak khán giả 2–3h** (thuật toán kịp index + test với sub). Nhưng **số đo kênh thắng NGÁCH đè baseline** — ngách mới phải đo giờ/ngày đối thủ trước khi đặt.
2. **Mỗi kênh đúng 1 giờ cố định, thứ cố định** — không range, không xoay thứ theo tuần.
3. **Chọn ngày đọc HAI chỉ số:** số video đối thủ đăng theo thứ (ngày họ CHỌN) và **median view theo thứ** (ngày khán giả PHẢN ỨNG) — cái sau mới là cái cần. Lệch nhau thì tin kênh có hiệu suất/video cao nhất. **Tách shorts** trước khi đếm. Median-theo-ngày của kênh đang sụp là số rác.
4. **Nhịp chuẩn (user chốt 2026-08-03):** kênh có rail đề xuất mở (`RELATED_VIDEO`/`SUGGESTED` là nguồn chính) → 7 slot/tuần; còn lại → **3 slot/tuần, thứ cố định** (giãn 2-2-3). Hiện cả nenkin lẫn showa đều **3/tuần**.
5. **Slot là chỗ trống, không phải chỉ tiêu** — không có hàng qua gate kênh thì BỎ SLOT, không đăng bù, không hạ chuẩn. Nhịp đều là để giữ kỷ luật sản xuất, **không mở được vòi phân phối**.
6. **Không trùng NGÀY+GIỜ** giữa các kênh. Mỗi lần sửa ngày của bất kỳ kênh nào → chạy lại phép kiểm trùng (§2).
7. Kênh đủ ~10–20 video → Studio Analytics ("When your viewers are on YouTube") đè bảng này.

## 1. LỊCH ĐANG CHẠY

JST = giờ VN + 2h.

| Kênh | Lịch | Giờ VN | Căn cứ + phanh |
|---|---|---|---|
| **nenkin** 年金と老後のお金研究室 | **T3·T5·CN 19:00 JST** — 3/tuần | 17:00 | Xem §1.1 |
| **showa** 昭和くらし図鑑 | **T3·T5·T7 18:00 JST** — 3/tuần | 16:00 | Xem §1.2 + `upload-schedule-measure-showa-2026-08-14.md` |
| **yawa** 人生哲学の夜話 | **T2·T4·T6 18:15 JST** — 3/tuần | 16:15 | Xem §1.2b + `youtube-jp-yawa/01_SOURCES/UPLOAD_SCHEDULE_MEASURE_2026-09-30.md` |
| **kyori** 心の距離の心理学 | **T2·T4·T7 19:00 JST** — 3/tuần | 17:00 | Xem §1.2c |
| **teinengo** 定年後のこころ研究室 | **T4·T6·CN 18:30 JST** — 3/tuần | 16:30 | Xem §1.2c |
| **kinishinai** 他人の目を気にしない心理学 | **T2·T5·T7 18:30 JST** — 3/tuần | 16:30 | Xem §1.2c |

### 1.1 nenkin
- **Giờ 19:00** = peak senior JP 19–20時台 (総務省 >50% 行為者率).
- **Căn cứ ngày cụm tiền-senior** (đo 2026-07-28, 50 video/kênh, tách shorts): **T6 là ngày lõi** — 年金・給付金完全攻略 median **T6 742K** (T2 = 0 video suốt đời kênh) · 節約看護師りょう đăng **T6 48/50**. シニアの年金・給付金速報 median **T3 119K cao nhất**, **T4 4,9K bét**. Kênh hiệu suất cao nhất đều **≤1,5 video/tuần**; kênh 1/ngày (あまおう) view chỉ 1/10.
- ⚠️ **Bộ T3·T5·CN MẤT ngày T6** (ngày lõi đo được). Muốn giữ T6 mà vẫn đúng nhịp: **T3·T6·CN** `[(1,19),(4,19),(6,19)]`. Chưa áp vì user chọn bộ hiện tại.
- ⭐ **Rule 支給日:** video 給付金/年金生活/いくらもらえる → đăng **1–3 ngày TRƯỚC ngày 15 tháng chẵn** (2·4·6·8·10·12; 15 rơi T7/CN/lễ → 支給日 dời lên ngày làm việc trước). Đè lịch bằng `--slot`.
- Gate FACT SHEET · Retention Audit · bộ A/B 3×3 đứng TRÊN lịch.
- Winner 完全攻略 đăng giờ rải bừa vẫn ăn 3,84M → **giờ/ngày không phải cái mở vòi**; ưu tiên thật là đề tài → title → bao bì → retention.

### 1.2 showa
- **Ngày T3·T5·T7** (đo 9 kênh cụm 昭和, 2026-08-14): 伊東彩 (format gần nhất, 0 shorts) chỉ đăng T3/T7/T5; なつかし + 記憶装置 median T5 cao nhất. Loại T6/T2/T4/CN.
- **Giờ 18:00**: ngách là 18–19h; chọn 18 để không trùng nenkin 19:00 ở T3·T5.
- ⚠️ Ngược tín hiệu nhịp của ngách (kênh hiệu suất cao đăng ≤1/tuần). 🛑 **Phanh:** 5 video đầu median ≤500 view + `BROWSE_FEATURES` vẫn 0 → hạ về **1/tuần T5 18:00** `[(3,18)]`.

### 1.2b yawa (đo 2026-09-30, 8 kênh ngách 人生/60代, 50 long-form/kênh)
- **Giờ 18:00**: 6/8 kênh đăng 18:00 (寄り添い 50/50 · 人間のトリビア 50/50 · 老後の物語 41/50); hiệu suất 18h ×0,95 vs 19h ×1,00 ⇒ giờ không phải đòn bẩy, theo số đông.
- **Ngày T4·T6**: hiệu suất theo ngày (view/ngày ÷ trung vị kênh) 水 ×2,01 · 金 ×1,77 cao nhất; 木 ×0,62 bét. Né được showa (T3·T5·T7) và nenkin (T3·T5·CN). ⚠️ view/ngày lệch theo tuổi video — xu hướng, không định luật.
- ⭐ **User chốt 2026-09-30: 3/tuần T2·T4·T6, giờ 18:15** — lùi 15′ sau giờ số đông 18:00 để video mình là video MỚI NHẤT khi người xem mở YouTube (user chọn 18:15 thay vì 17:45). T2 ×1,04 = ngày đối thủ đăng nhiều nhất. Slot `(0,18,15),(2,18,15),(4,18,15)`.
- 🛑 Phanh: 5 video đầu median ≤500 view + BROWSE_FEATURES = 0 → hạ về 2/tuần T4·T6.

### 1.2c Bộ 3 kênh tâm lý 60+ — kyori · teinengo · kinishinai (đo 2026-09-30)
- **Nguồn:** 3 kênh 【心理学】 60代 (ユウリの優しい心理学 · 心理のコトノハ · 心がほっとする人生学), 79 video dài (`youtube-jp-health/06_VIDEO/_niche_scan/bench_channels.json`).
- **Giờ:** 18h = 38 video · 19h = 33 ⇒ ngách đăng 18–19h.
- **Ngày** (trung vị view/ngày ÷ trung vị kênh): T7 ×1,48 · T4 ×1,45 · T6 ×1,31 · CN ×1,07 · T2 ×1,05 · **T5 ×0,44 · T3 ×0,33**. ⚠️ n nhỏ, và trung bình bị méo vì ユウリ vừa nổ (1,17M) ⇒ chỉ đọc trung vị, coi là xu hướng.
- **Cách xếp:** mỗi kênh 1 giờ cố định, 3 slot giãn 2-2-3, không trùng ngày+giờ, mỗi tối ≤3 kênh của mình.
  - kyori (triển vọng nhất) lấy bộ điểm cao nhất `{T2,T4,T7}` = 3,98, giờ 19:00.
  - teinengo lấy `{T4,T6,CN}` = 3,83, giờ 18:30.
  - kinishinai (yếu nhất, phanh sẵn) lấy `{T2,T5,T7}` để giãn khỏi hai kênh kia; ⚠️ T5 là ngày yếu.
- Slot trong code: kyori `(0,19,0),(2,19,0),(5,19,0)` · teinengo `(2,18,30),(4,18,30),(6,18,30)` · kinishinai `(0,18,30),(3,18,30),(5,18,30)`.
- 🛑 **Phanh (mỗi kênh):** 5 video đầu median ≤500 view + `BROWSE_FEATURES` = 0 → hạ về 2/tuần, giữ 2 ngày điểm cao nhất của bộ.

### 1.3 Kênh khác
Mọi kênh khác trong `upload_pack.py` `CHANNELS` **phải để `slots: []`** (không còn làm). Không tự sửa code trong rule này — kiểm bằng §2.

## 2. KIỂM LỊCH BẰNG MÁY

```bash
cd Projects/youtube-jp-chouhen/tools && python -c "from upload_pack import CHANNELS; [print(k, c['slots']) for k,c in CHANNELS.items() if c['slots']]"
# trùng ngày+giờ:
python -c "from upload_pack import CHANNELS, slot_hm; import collections; s=collections.defaultdict(list); [s[slot_hm(x)].append(k) for k,c in CHANNELS.items() for x in c['slots']]; [print(kk,v) for kk,v in sorted(s.items()) if len(v)>1]"
```
Slot hỗ trợ phút lẻ `(wd, giờ, phút)` — mọi chỗ đọc lịch phải qua `slot_hm()`, đừng unpack `for wd, hour in ...`.

## 3. TOOL ĐÓNG GÓI UPLOAD

`python E:\Claude\Projects\youtube-jp-chouhen\tools\upload_pack.py <slug> --channel <nenkin|showa> [--open]` (standalone):
- Đọc gói CTR trong script (Title CHỐT / Tên file upload / 概要欄 3 dòng + đầy đủ / タグ) → gom `06_VIDEO/<slug>/_upload/`: mp4 rename SEO (hardlink) + subs.srt + thumbnail + `METADATA.txt`; tự tính giờ hẹn theo bảng §1 (in cả giờ VN); PRE-FLIGHT duration↔srt, CTA, 目次, đã-đăng. `--slot "YYYY-MM-DD HH:MM"` ghi đè giờ.
- **Vòng đời:** `pipeline_status.py` xem tồn kho → `upload_pack.py` → đăng theo METADATA → **`upload_pack.py <slug> --channel X --done`** (ghi UPLOADED.txt, move sang `07_UPLOADED/`, gom script + SLIDES vào `_scripts/`, xoá mp4/voice nặng) → `analytics_report.py` theo dõi 72h.
- **Full-auto:** `tools/upload_api.py <slug> --channel <key>` — kênh có `credentials/token.json` scope `youtube.upload` thì dry-run rồi bấm; đọc `status` API trả về, đừng suy "chưa đậu audit ⇒ không upload được".

**Dashboard** `Projects/yt-dashboard/` (`run_dashboard.cmd` → `http://127.0.0.1:8765`):
- Nạp `CHANNELS` **một lần lúc khởi động** → sửa `slots` xong phải restart. Restart bằng **tiến trình rời**, không bằng background task của phiên Claude (chết theo phiên):
  ```powershell
  Start-Process -FilePath "python" -ArgumentList "dashboard.py" -WorkingDirectory "E:\Claude\Projects\yt-dashboard" -WindowStyle Minimized
  ```
  Kiểm: `curl -s -m 8 http://127.0.0.1:8765/api/status -o /dev/null -w "%{http_code}"` → 200.
- 🔴 **`projects.json` ĐÈ `upload_pack.py`** — kênh có `slots` khác rỗng trong `Projects/yt-dashboard/projects.json` thì dashboard dùng giá trị đó, restart không cứu. Dấu hiệu: thẻ kênh ghi 「sửa tay (đè rule)」 → bấm 「↺ Về rule」. Kiểm trước khi sửa lịch:
  ```bash
  cd Projects/yt-dashboard && python -c "import json,io;[print(p['key'],p.get('slots')) for p in json.load(io.open('projects.json',encoding='utf-8'))['projects'] if p.get('slots')]"
  ```

**Bẫy ghi lên kênh:**
- 🔴 **"Đẩy lên kênh" ≠ upload** — đẩy đúng thứ vừa làm: đổi thumbnail → `thumbnails.set` · sửa metadata → `videos.update` · chỉ video mới chưa đăng mới là upload.
- 🔴 **`UPLOADED.txt`/`pipeline_status.py` không phải nguồn sự thật** — chỉ biết lần đăng qua tool. Trước mọi cú ghi: **đối chiếu kênh thật** (`pipeline_status.py --check`). `upload_api.py::find_on_channel()` chặn upload trùng (vượt bằng `--allow-duplicate`).
- 🔴 **Log upload phải nằm NGOÀI folder video** (`06_VIDEO/_upload_logs/<slug>.log`) — upload xong tool move folder video.
- 🔴 EXITCODE upload chỉ nói về khâu dọn kho. Thấy "failed" → đọc log / `videos.list` trước, **cấm chạy lại theo phản xạ** (trùng video không undo được).

## 4. SỐ LIỆU NỀN JP

- Long-form toàn cầu (Buffer, 1,8M video): CN 10:00 tốt nhất, T6 12:00 ba; khung creator 18–21h (24%), 12–15h (22%).
- Golden time YouTube JP 20–23h; khuyến nghị chung 18–21h.
- **Senior JP (総務省 令和6年度):** 60–70代 xem tối vượt mọi thế hệ ở **19–20時台 (>50%)**, xem sớm ngủ sớm; YouTube 66–71%.
- 年金支給日 = ngày 15 tháng chẵn (rơi T7/CN/lễ → dời lên ngày làm việc trước).

## 5. NGUỒN

- Buffer: https://buffer.com/resources/best-time-to-post-on-youtube/
- SocialPilot: https://www.socialpilot.co/insights/best-time-to-post-on-youtube
- HubSpot JP: https://blog.hubspot.jp/marketing/best-time-to-post-youtube
- 総務省 令和6年度: https://www.soumu.go.jp/menu_news/s-news/01iicp01_02000125.html
- 日本年金機構 支給日: https://www.nenkin.go.jp/section/faq/jukyu/uketori/uketori/shiharaiduki/20140421-01.html
- Đo ngày: `Projects/youtube-jp-chouhen/tools/measure_upload_days.py` (`--group showa`); đo giờ↔view: `measure_upload_hours.py`. Pin `channelId` trong `TARGETS` — search-by-tên hay trả kênh clone chết.
