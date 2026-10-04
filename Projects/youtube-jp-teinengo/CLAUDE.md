# CLAUDE.md — youtube-jp-teinengo

Kênh **定年後のこころ研究室** (key `teinengo`), faceless, thị trường JP, khán giả **60+**.
Chủ đề: **sau nghỉ hưu, tìm lại động lực sống** (cách sống qua ngày sau 定年 · lật ngược nửa sau cuộc đời · chỗ đứng · 生きがい · làm việc sau 60 theo góc tâm lý).
Kênh 2/3 trong bộ tâm lý 60+. Kênh anh em: `youtube-jp-kyori` (quan hệ, kênh 1).

- **REBRAND từ kênh みんなの健康ノート (health)**, user chốt 2026-09-30, cùng kênh. 21 video health cũ → **限定公開** (không xoá).
- channelId `UCnoYb7aEKy1NgspYTKwhh1Q` · handle `@teinengo-kokoro` · Gmail `saubeooo04@gmail.com` · Chrome `Profile 13`
- ⚠️ **Chưa có token API đúng kênh.** `youtube-jp-health/credentials/token.json` thuộc tài khoản khác ⇒ upload qua API phải auth lại (`tools/auth_test.py --channel-dir …`, chọn đúng kênh). Trước đó mọi thao tác ghi đi Studio.
- Mốc gốc lúc rebrand: 903 view · 3 sub.
- ⛔ Project `youtube-jp-health/` GIỮ NGUYÊN — có tool dùng chung (`video_render.py`, `channels.py`, `bench_channels.py`).

## Tên kênh — vì sao 定年後のこころ研究室 (user chốt 2026-09-30)
Đã dò 9 tên bằng `search.list type=channel`, không tên nào trùng y hệt.
- Sát nút nên loại: 定年後の心理学 (đã có 定年後の心理戦) · 第二の人生の心理学 (đã có 第二の人生の知恵) · 定年後を生きる心理学 (đã có 定年後の知恵 / 定年後の暮らし).
- Tên chốt có 定年後 đứng đầu; keyword này tăng ×8 trong 3 tháng.

## Bằng chứng ngách (`01_SOURCES/NICHE_RESEARCH_2026-09-30.md`)
- **Search:** 定年後 38 (3 tháng: 3,8 → 30,6) · related **breakout**: 定年後の暮らし · 定年退職後の過ごし方 · 定年後の仕事. 定年 138 ↑ · 生きがい 55 → (nửa là tên bài hát).
  - Cụm nguyên văn ≈0: 定年後の人生 · 定年後の再就職 · 定年うつ. ⇒ Keyword dẫn = **定年後**; view vẫn đến chủ yếu từ đề xuất.
- **Video thắng:** 「60代から人生逆転する人に共通する生き方」 131K · 「50代で人生が劇的に逆転する人とそのまま終わる人の決定的な違い7選」 119K (心がほっとする人生学) · 「人生は最後の10年で決まります」 42K.

## 5 ngách con
1. ⭐ **Cách sống qua ngày sau nghỉ hưu** (定年後の暮らし / 過ごし方, breakout) — mở màn
2. Lật ngược nửa sau cuộc đời (人生逆転 · 後半戦)
3. Chỗ đứng sau nghỉ hưu (定年後 居場所 ↑ nhỏ)
4. Lẽ sống (生きがい)
5. Làm việc sau 60 — ⛔ **không nói tiền/chế độ** (vùng của nenkin)

## Ranh giới
- **Với nenkin:** ⛔ không nêu số tiền 年金 hay chế độ; nói tâm lý và cách sống, không nói tiền.
- **Với yawa:** không dùng 古典 làm xương sống; dùng tâm lý học / nghiên cứu có nguồn.
- **Với kyori:** đề quan hệ (vợ chồng, con cái) thuộc kyori. teinengo chỉ chạm tới khi trục bài là "cuộc sống sau 定年".
- ⛔ Không làm đề sức khoẻ, bệnh, thuốc (YMYL; kênh health cũ đã ngừng).

## Việc mở
- [x] Setup kênh (2026-09-30), chi tiết ở `00_BRAND/CHANNEL_SETUP.md`
- [ ] Auth token API đúng kênh
- [x] `05_SCRIPT_FORMULA.md` (2026-10-01) — khuôn **đâm thẳng 語りかけ型, 7 cặp đối chiếu**; ⛔ không tâm sự/podcast
- [ ] Giọng TTS · lớp hình (⏳ Remotion chia đôi trái/phải) · khuôn thumbnail
- [ ] Lịch đăng: không trùng nenkin/showa/yawa/kyori
- [x] Key `teinengo` trong `youtube-jp-health/tools/channels.py` — giọng **麒ヶ島宗麟 ノーマル 0.90** (user chọn 2026-10-01)

Luật chung: `.claude/rules/`.
