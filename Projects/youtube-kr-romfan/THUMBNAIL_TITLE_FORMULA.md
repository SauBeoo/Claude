# Công thức TITLE + THUMBNAIL thắng — ngách 오디오 드라마 / 사이다 / 로맨스 (bóc từ đối thủ, xem tận mắt 2026-07-22)

> Nguồn: nhìn thật 20 thumbnail top-video của 5 kênh (톡톡사이다 111K 창작사이다, 민트 오디오북 116K, 랄라하 430K 성우드라마, 사연튜브 447K, 여왕의 로맨스 숏드라마). Tải `scratchpad/thumbs_kr/`.

## 1. NGÁCH CÓ 2 TRƯỜNG PHÁI THỊ GIÁC

### Trường phái A — 사연/사이다 (text-first, kéo click bằng drama)
- **Talking-head + text đáy** (톡톡사이다): mặt nữ narrator + mic ASMR trên nền lấp lánh xanh lá + tên kênh góc trên trái + **#회차** góc phải + **2 dòng chữ đáy** (trắng setup → **vàng punch** 「한방 먹였습니다!!」). Chữ 袋文字 viền đen dày.
- **KakaoTalk chat** (톡톡/사연튜브): nền xanh lá chat + bong bóng thoại lộ đúng câu 막장 nhất (시에미 đòi 전세금 → comeback vàng) — bán luôn "miếng drama" trong thumbnail.
- **Text-wall nhiều màu** (랄라하 shorts): panel kem giữa + chữ khổng lồ **mỗi dòng một màu** (vàng/cyan/xanh/tím) + 「충격」 đỏ đáy + badge **ON AIR** + logo kênh.
- Từ khóa hình: 충격 / 반전 / 참교육 / 막장 · màu vàng+đỏ+cyan viền đen · mặt nữ hoặc bong bóng chat.

### Trường phái B — 로맨스 드라마 (cinematic, bán FANTASY)
- **여왕의 로맨스** (đúng genre 사우 nhất): **cặp đôi thật đẹp** (nam chính 재벌 vest/áo sơ mi + nữ xinh) dưới ô, **phố đêm bokeh lãng mạn**, **tiêu đề SERIF VÀNG GOLD thanh lịch** trái (「처음부터 너였다」) + góc trên: `한국어 더빙 / 설렘 가득 로맨스` + `매일 업데이트`. Sang, mơ mộng — KHÔNG text-wall.
- Bán bằng: **nam chính đẹp + nữ chính xinh + không khí mơ**; chữ ít, elegant.

## 2. 사우 오디오 = LAI 2 TRƯỜNG PHÁI (계약결혼·재벌 = romance × 사이다 복수 = drama)

Công thức thắng cho 사우 = **nền cinematic cặp đôi/nữ chính đẹp (bán fantasy như 여왕) + 1 dòng HOOK 사이다 đỏ punch (kéo click như 톡톡)**. Khớp luôn CLAUDE.md kênh (Pexels/ảnh thật + make_thumb 3 tầng: băng trên trắng + dòng key đỏ double-stroke + băng đáy vàng).

**Chọn theo loại tập:**
- Tập nặng ROMANCE (계약결혼/재벌/정략결혼, twist 「남편이 먼저 빠졌다」): nghiêng **trường phái B** — cặp đôi cinematic + tiêu đề gold + 1 dòng twist đỏ nhỏ.
- Tập nặng 사이다 복수 (시월드/상간녀/참교육): nghiêng **trường phái A** — nữ chính + 2–3 dòng chữ to, punch đỏ 「~해버렸다」.

## 3. TITLE — công thức (đo từ top-video)
- **사이다:** 시월드/시모/며느리/상간녀 갈등 câu đầu + động từ mạnh 참교육/한방먹였다/갈아버렸다 + 충격/반전. Prefix `(반전신청사연)` kiểu 사연튜브.
- **로맨스:** 계약결혼/정략결혼/재벌 + twist tình cảm (「남편이 먼저 사랑에 빠졌다」「진짜 사랑이었다」).
- **사우 (lai):** câu đã set cho video 계약결혼 = `위자료 100억 받고 떠나려던 날, 남편이 이혼 서류를 갈아버렸다` — CHUẨN MẪU: tiền 사이다 (100억) + động từ sốc (갈아버렸다) + twist romance (남편이…). Giữ pattern này.

## 4. CHI TIẾT DÙNG ĐƯỢC NGAY
- **Nền:** cặp đôi/nữ chính ĐẸP (nam 재벌 lịch lãm + nữ thanh tú) — Pexels free-thương-mại HOẶC AI hư cấu (KHÔNG mặt sao thật). Phố đêm bokeh / nội thất sang / ánh gold.
- **Chữ:** băng/tiêu đề trên + **dòng hook đỏ double-stroke** (사이다 punch) + băng vàng phụ. Font Malgun Gothic Bold. Chừa mặt nhân vật.
- **Phụ kiện nhận diện (tùy chọn, học đối thủ):** badge `매일 업데이트` hoặc số 회차 góc, tag genre `설렘 로맨스` — tạo cảm giác series.
- **120px:** dòng hook đỏ phải đọc được; mặt nam/nữ đẹp phải nhận ra.
- **Compliance:** ảnh cặp đôi = Pexels/AI hư cấu (không sao thật); không từ cấm (殺/피/자살…) trên title/thumbnail; 이혼/위자료/복수 = OK.

## 5. TOOL
Kênh đã có `tools/make_thumb.py` (3 tầng, băng đỏ double-stroke) đúng hướng. Muốn kiểu khuôn-A/số-hero như nenkin thì port `make_thumb_khuonA.py`. Quy trình: **đưa prompt ảnh trước → user gen/Pexels → ghép chữ → duyệt 3 cửa** (theo [[feedback-chot-truoc-khi-dang]]).
