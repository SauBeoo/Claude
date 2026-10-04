# Channel ↔ Browser Profile — cô lập kênh (RULE TOÀN HỆ THỐNG)

> Nguồn sự thật về kênh nào quản bằng Chrome profile + Gmail nào. Mapping máy đọc: `Projects/yt-dashboard/browser_profiles.json`.
> Dashboard `http://127.0.0.1:8765` → tab **🌐 Profiles**.

## 0. Ý ĐỒ
Mỗi kênh 1 Chrome profile riêng → không đăng nhầm kênh. Tách profile là **vệ sinh thao tác**, không phải thuốc tăng view. Tầng quyết định liên đới là **Gmail**.

## 1. DANH BẠ (kênh đang chạy)

| Key | Kênh | Gmail CHỦ | Chrome profile | Shortcut |
|---|---|---|---|---|
| nenkin | 年金と老後のお金研究室 | saugonn331@gmail.com | `Profile 17` | YT - nenkin.lnk |
| kyori | 心の距離の心理学 (`UCVlmm1sz7cvTIQ3uSaSct_w`, rebrand từ 古代の秘訣 2026-09-30) | saubeo.killua@gmail.com | `Profile 6` | YT - co-dai.lnk |
| teinengo | 定年後のこころ研究室 (`UCnoYb7aEKy1NgspYTKwhh1Q`, rebrand từ みんなの健康ノート 2026-09-30) | saubeooo04@gmail.com | `Profile 13` | YT - health.lnk |
| kinishinai | 他人の目を気にしない心理学 (`UCj_QueccfLclCHR5_0vys1Q`, rebrand từ 60代からの食卓 2026-09-30) | tokyohot96@gmail.com | `Profile 3` | YT - shokutaku.lnk |
| yawa | 人生哲学の夜話 (`UCuzbgcFHVmAf4O6wU1wLyIQ`, rebrand từ 真夜中の朗読便/chouhen 2026-09-28) | tuananh96freemail@gmail.com | `Default` | YT - chouhen.lnk |
| showa | 昭和くらし図鑑 (`UCT0CITcGxFErQk_YjQriZ_w`) | gonnsau@gmail.com | `Profile 15` | ⏳ `YT - showa.lnk` chưa tạo |

⚠️ **Quyền quản lý chéo:** `saubeo.killuaa@gmail.com` (Profile 9) có quyền quản lý nhiều brand channel (gồm cả showa) ⇒ các kênh vẫn chung một tầng liên đới; muốn cô lập thật phải gỡ quyền quản lý trong từng Brand Account (cần user quyết).
Xác định chủ kênh bằng **Studio → 設定 → 権限** (Gmail SỞ HỮU), không bằng "profile nào mở được kênh".

## 2. NGUYÊN TẮC THAO TÁC
1. Mọi thao tác browser dính kênh nào → mở đúng profile kênh đó (shortcut / tab Profiles / `upload_pack.py --open`).
2. Không login Gmail kênh này vào profile kênh khác.
3. Kênh mới: tạo profile qua tab Profiles (bỏ trống ô → tạo `yt-<key>` + shortcut), rồi login Gmail kênh.
4. Claude in Chrome gắn theo profile — cần điều khiển kênh nào thì cài extension vào profile đó.
5. Đổi mapping → sửa `browser_profiles.json` + bảng §1 cùng lúc.

## 3. TOOL ĂN THEO MAPPING
- `upload_pack.py --open` → mở Studio đúng profile của `--channel`; thiếu mapping → fallback browser mặc định (có cảnh báo).
- Dashboard `/api/open what=studio` → cùng logic.
- Dashboard `/api/profiles` → đối chiếu Gmail mapping vs Gmail đang login thật (đọc `Local State`, readonly); lệch → ⚠️.
