# CLAUDE.md — youtube-jp-kyori

Kênh **心の距離の心理学** (key `kyori`), faceless, thị trường JP, khán giả **60+**.
Chủ đề: **quan hệ tuổi già nhìn qua tâm lý học** (người nên tránh xa · bản chất thật · vợ chồng sau 定年 · con cái · mệt vì quan hệ).
Mở ngày 2026-09-30. Là kênh 1 trong bộ 3 kênh tâm lý 60+; kênh 2 (定年後) và kênh 3 (嫌われる勇気) làm sau.

- **REBRAND từ kênh 古代の秘訣 (co-dai)**, user chốt 2026-09-30, cùng kênh. 24 video 古代 cũ chuyển sang **限定公開** (không xoá); danh sách gốc ở `00_BRAND/old_codai_before_rebrand.json`.
- channelId `UCVlmm1sz7cvTIQ3uSaSct_w` · handle `@kokoro-no-kyori` · Gmail `saubeo.killua@gmail.com` · Chrome `Profile 6`
- Token API: `Projects/youtube-jp-co-dai/credentials/token.json` (có scope upload + force-ssl ⇒ `videos.update`/`channels.update` chạy được). Key cũ `co-dai` vẫn còn trong tool; video mới dùng key `kyori`.
- Mốc gốc lúc rebrand: 354 view · 2 sub.
- Vault: `SecondBrain/10_Projects/youtube-jp-kyori/youtube-jp-kyori.md`

## Tên kênh — vì sao 心の距離の心理学 (user chốt 2026-09-30)
Đã dò 10 tên bằng `search.list type=channel`.
- Trùng y hệt: `大人の人間関係心理学`.
- Sát nút, loại: 人間関係の心理学ノート (đã có 心理学ノート) · ひとの本性心理学 (đã có 本性心理学) · 人付き合いの心理学 · 縁の心理学.
- Tên chốt chứa 心理学, keyword 395 và đang lên. "Khoảng cách lòng người" khớp thẳng với đề đang thắng ngách (離れるべき人).

## ⚠️ Ranh giới với yawa (人生哲学の夜話)
Đề của hai kênh chồng nhau (人間関係 · 夫婦 · 孤独), nên tách bằng LĂNG KÍNH:
| | yawa | kyori |
|---|---|---|
| xương sống | 古典 (徒然草・論語…) + câu chuyện người quen | **tâm lý học / nghiên cứu / thí nghiệm có tên, có nguồn** |
| thẻ title | không | **【心理学】** |
| giọng | chiêm nghiệm trước khi ngủ | nhận diện → giải thích cơ chế → làm gì |
⛔ Không dùng câu 古典 làm chốt bài. ⛔ Không lấy đề trùng với video yawa đã hoặc sắp đăng: soát `youtube-jp-yawa/03_SCRIPTS/` trước khi chọn đề.

## Bằng chứng ngách (chi tiết: `01_SOURCES/NICHE_RESEARCH_2026-09-30.md`)
- **Search:** cụm hẹp gần như bằng 0 (人間関係の断捨離 · 口癖 心理 · 親子の距離 = 0). Từ rộng đang lên: 心理学 395 ↑ · 人間関係 216 ↑ · 人間関係に疲れた 5,1 ↑ · 離れるべき人 2,9 ↑ · 子離れ (rising: 子離れできない親/母親). ⇒ **View đến từ ĐỀ XUẤT.** Keyword chỉ để dạy YouTube chủ đề, không phải để hứng search.
- **Video thắng (≤30 ngày):**
  - 「【心理学】一度でもされたら、その人からは離れてください｜本性が一度で分かる7つの行動」 **1,17M** (ユウリ, 5,3K sub) — cùng title 152K ở 心がほっとする人生学.
  - 「誰に聞かれても絶対に答えてはいけない質問7選」 161K / 170K.
  - 「60代でこの口癖を言う人は本当に性格がいい人」 97K · 「群れる人と群れない人」 63K · 「夫婦が絶対に一緒にしないほうがいい5つ」 41K.
- 🔴 Hai kênh đối thủ dùng CÙNG MỘT title ⇒ ngách đang chép nhau. Mình **không chép title**; phải khác ở góc nhìn (có tên nghiên cứu) và ở hình (`youtube-compliance.md` §1).

## 5 ngách con (xếp theo bằng chứng)
1. ⭐ **Người nên tránh xa / bản chất thật** (離れるべき人・本性) — mở màn
2. Những điều không được nói, không được trả lời
3. Vợ chồng sau nghỉ hưu
4. Cha mẹ không rời được con (子離れできない親)
5. Mệt vì quan hệ / không theo bầy

## Format đối thủ (bench 30 video, 2026-09-30)
- Dài 15–25′ (trung vị 18–22′).
- Liệt kê 5–7 mục: 「〜7選」「〜5つの…」.
- Đăng 18:00–19:00 JST; categoryId 27 (ユウリ, 心がほっとする) hoặc 22 (心理のコトノハ).
- Nhịp: 1,1 · 2,4 · 6 video/tuần.

## Việc mở (chưa chốt — hỏi user)
- [x] Setup kênh (2026-09-30), kiểm lại bằng API:
  - tên · handle · logo · banner (`tools/make_brand.py`) · mô tả · keywords (`00_BRAND/CHANNEL_SETUP.md`) · gỡ trailer 古代 · 24 video cũ → 限定公開
  - mặc định upload sạch (tag/mô tả trống), danh mục 27 教育, tiếng Nhật
- [ ] Giọng TTS · lớp hình (ảnh AI người thật hay minh hoạ) · khuôn thumbnail
- [ ] Khuôn kịch bản (`05_SCRIPT_FORMULA.md`) — mổ 3 video thắng trước
- [ ] Lịch đăng: slot không trùng nenkin/showa/yawa (`upload-schedule.md` §2), bắt đầu 1–2 video/tuần
- [ ] Thêm key `kyori` vào `youtube-jp-health/tools/channels.py` + `youtube-jp-chouhen/tools/upload_pack.py` `CHANNELS`
- [ ] categoryId: chọn 27 hay 22 (đo thêm)

Luật chung: `.claude/rules/` (compliance · audience-45plus · humanize · A/B 3×3 · SEO · render nền).
