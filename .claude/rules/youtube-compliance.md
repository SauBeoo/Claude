# YouTube Compliance — RULE TOÀN HỆ THỐNG

> Áp cho **nenkin** + **showa** và mọi kênh mở sau. Cập nhật chính sách: 2026-07-08 (+ 2026-08-09 ảnh AI). YouTube đổi policy → sửa file này.

## 0. CÁCH DÙNG (bắt buộc)
Mỗi lần viết/đóng gói (kịch bản, **tiêu đề, thumbnail, 概要欄, tag, pinned comment**) → tự đối chiếu rule này và **BÁO NGAY từ/điểm nào cần né TRƯỚC khi giao**, kèm bản thay an toàn.

### 0.1 Phạm vi quét từ ngữ
- Quét & thay từ nhạy (mục 3) **CHỈ ở TIÊU ĐỀ, THUMBNAIL, phần 概要欄 hiển thị đầu** — chỗ quyết định mất ad.
- **KHÔNG tự làm nhạt THÂN kịch bản.** Từ nặng thật sự (slur) → BÁO user quyết.
- Ngoại lệ bắt buộc thay cả trong body: hướng dẫn phạm pháp cụ thể, gore/tình dục/tự sát chi tiết, slur chủng tộc.

## 1. "Inauthentic content" — rủi ro DEMONETIZE CẢ KÊNH (YPP 15/07/2025)
Nội dung hàng loạt / theo khuôn ít biến hoá → mất kiếm tiền **toàn kênh**. AI hỗ trợ OK nếu thêm **giá trị gốc đáng kể**.
- ✅ Mỗi video có giá trị gốc thực chất (narration/insight/dữ liệu riêng), không slideshow/template rỗng; mỗi video góc riêng, ví dụ khác nhau.
- ❌ Không một template intro/outro/cấu trúc máy móc cho hàng loạt (câu nhận diện kênh cố định thì OK).
- ❌ **Không lặp NGUYÊN BỘ visual** giữa các video. Chính sách asset: `media-library.md` (mỗi video tải bộ mới, kho = sổ đen).
- ❌ Không đăng lại video trùng / tập lẻ nguyên bản làm video mới.

## 2. Disclosure "altered/synthetic content"
- **Giọng TTS** (VOICEVOX, không nhái người thật cụ thể): không bắt buộc tick; ghi credit giọng trong 概要欄 (điều khoản VOICEVOX: 「VOICEVOX:キャラ名」).
- **Thumbnail AI + script/title/mô tả viết bằng AI** = production assistance → **không cần tick**. Nhưng thumbnail không dùng mặt người thật cụ thể / dàn dựng sự kiện–địa điểm có thật như thật (nhân vật AI hư cấu OK).
- **Cảnh/ảnh AI realistic TRONG video:** ⚠️ **BẮT BUỘC tick "altered/synthetic content"**.

### 2.1 Ảnh/clip AI trong video — ĐƯỢC dùng, và TICK (user chốt 2026-08-09)
Cái đổi là lựa chọn của mình, không phải yêu cầu YouTube: dùng ảnh AI + **tick ô khai báo** khi upload (nhánh hợp lệ, không phải lách).
- ✅ Được: ảnh/clip AI người/cảnh làm b-roll, **nhân vật HƯ CẤU** (giữ một dàn diễn viên cố định xuyên video).
- ⛔ Không đổi: cấm mặt **người thật cụ thể** · cấm dàn dựng **sự kiện/địa điểm có thật** như thật · cấm persona xưng chuyên gia/bác sĩ · cấm ảnh AI làm **bằng chứng** cho claim (số liệu/nguồn phải là 原典 thật).
- 📌 `upload_pack.py`/`upload_api.py` **chưa có cờ này** → tick TAY trong Studio, nhắc trong `METADATA.txt`.
- ⚖️ Cái mất biết trước: nhãn "Altered or synthetic content" ăn vào độ tin ở ngách YMYL.

## 3. Advertiser-friendly — TỪ NGỮ gây tắt/vàng quảng cáo (profanity update 07/2025)
- **TIÊU ĐỀ + THUMBNAIL = nghiêm nhất** → từ mạnh ở đây = mất SẠCH ad.
- **7 giây đầu:** 1 từ mạnh được nới; rải suốt bài → vẫn giới hạn.
- Máu me/bạo lực làm tâm điểm không ngữ cảnh → không ad-friendly.

| Nhóm | Nhật — tránh | Thay an toàn |
|---|---|---|
| Giết/chết literal | 殺す・殺人・死ね | 追い詰める・破滅・因果応報 |
| Máu me | 血まみれ・流血描写 (kể cả 血の気が引く ở title/thumb) | 顔面蒼白・真っ青 |
| Tự sát | 自殺・自ら命を | né hẳn; buộc thì gián tiếp, không mô tả |
| Tình dục | レイプ・性的描写・エロ | không dùng |
| Ngược đãi | 児童虐待・虐待 chi tiết | いじめ・冷遇 (kể gọn) |
| Ma tuý/vũ khí | 麻薬・銃 (tôn vinh) | chỉ trong ngữ cảnh phê phán |
| Kỳ thị/chửi tục | slur vùng/chủng/giới | KHÔNG dùng bao giờ |

✅ Ẩn dụ 社会的な死 thường không sao, nhưng hạn chế ở tiêu đề.

## 4. Metadata không gây hiểu lầm
Title + thumbnail được dramatize, NHƯNG **mọi tình tiết/con số nêu ra phải thực sự có trong video**.

## 5. Theo ngách
- **nenkin (YMYL tiền/pháp lý):** mọi số/chế độ phải từ nguồn chính thức (年金機構/厚労省/国税庁…), verify TRƯỚC khi viết; không hứa kết quả tuyệt đối ("chắc chắn nhận được"); không tư vấn cá nhân như chuyên gia; câu "tham khảo, hỏi 年金事務所/chuyên gia". Chi tiết: `youtube-jp-nenkin/CLAUDE.md` §YMYL.
- **showa (ký ức/lịch sử):** số/giá thời đó phải có nguồn; không trình bày ảnh/clip AI như tư liệu thật; ảnh/phim tư liệu phải đúng license + credit.
- **Mọi kênh:** không tên công ty/người/thương hiệu/nhạc có bản quyền thật (trừ trích nguồn chính thức); BGM/ảnh free-thương-mại + credit đúng license.

## ✅ CHECKLIST QUÉT NHANH trước khi giao
1. Tiêu đề/thumbnail có từ nhóm bảng mục 3? (báo + thay)
2. Có ảnh/cảnh AI realistic trong video → đã nhắc tick disclosure?
3. BGM/ảnh/footage có license free-thương-mại + credit?
4. Có tên thật (người/công ty/thương hiệu) không cần thiết?
5. Miễn trừ / câu tham khảo có trong 概要欄?
6. Tình tiết/con số trên title/thumbnail có thật trong video?
7. Video này có trùng khuôn/visual nguyên bộ với video trước?

Nguồn: YouTube Help — channel monetization policies (inauthentic, 07/2025); Disclosing GenAI content (2026); Advertiser-friendly guidelines + profanity update (07/2025).
