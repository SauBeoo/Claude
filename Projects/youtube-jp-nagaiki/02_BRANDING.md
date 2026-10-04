# 02_BRANDING — 長生きごはんの知恵袋 (avatar + banner)

> Quy trình chuẩn kênh health kế thừa: **Claude đưa prompt → user gen → duyệt cùng nhau → upload tay trong Studio** (Tùy chỉnh → Hồ sơ → Tải lên). Ảnh AI cho avatar/banner = production assistance, KHÔNG phải tick synthetic.
> Bảng màu đề xuất (khác health navy+山吹色 để 2 kênh không lẫn): **nền kem ấm (#F6EFE3) + đỏ gạch (#C0392B) + nâu trà (#6B4F3A)** — chốt khi user duyệt ảnh đầu.

## Avatar (98×98 hiển thị — phải rõ ở cỡ con tem)

**Prompt (gen vuông 1024×1024):**
```
Flat vector logo icon for a Japanese senior food & health YouTube channel. A warm steaming bowl of white rice (ごはん) drawn in thick clean outlines, the steam curling upward into the shape of a traditional Japanese drawstring pouch (巾着袋/知恵袋). Warm cream background (#F6EFE3), brick red and tea-brown accents, minimal detail, high contrast, no text, no human face, readable at very small size, centered composition, soft rounded style like a modern Japanese shop emblem.
```
- Gate duyệt: thu về 98px — vẫn nhận ra "bát cơm + túi"? Không chữ nào trong ảnh (chữ ở cỡ avatar là rác).

## Banner (2048×1152 — vùng an toàn mọi thiết bị chỉ 1235×338 Ở GIỮA)

**Prompt (gen 2048×1152, chữ để tool/Canva đè sau, KHÔNG gen chữ bằng AI):**
```
Wide YouTube banner background, warm Japanese kitchen table scene at golden hour: wooden table, a steaming bowl of rice, small side dishes (natto, pickles, miso soup), soft morning light, shallow depth of field, cream and warm brown tones, calm and cozy, empty space in the center band for text, no people, no text, no logos.
```
- Đè chữ sau khi gen (nằm TRỌN dải giữa 1235×338): dòng chính 「長生きごはんの知恵袋」 cỡ lớn; dòng phụ 「いつもの食材、食べ方で変わる」; cỡ chữ theo luật 45+ (to, tương phản cao, nền sáng).
- Gate duyệt: mở preview mobile trong Studio — cả 2 dòng chữ phải nằm trong vùng hiển thị điện thoại.

## Trạng thái
- [x] Avatar: XONG 2026-08-01 — user gen (Gemini), Claude cắt vòng tròn từ ảnh logo → `branding/avatar_1024.png`, gate 98px ĐẬU (bát cơm + túi nhận ra ngay), đã upload Studio
- [x] Banner: XONG 2026-08-01 — user gen, Claude xử lý: xoá title gốc (nằm ngoài vùng an toàn) bằng patch giấy washi tự tìm block sạch nhất, vẽ lại tên kênh font KleeOne-SemiBold 116px navy + halo trắng vào ĐÚNG dải an toàn 1235×338 → `branding/banner_2048x1152.png`, preview Studio xác nhận "tất cả thiết bị" thấy đủ tên + bát cơm, đã upload
- [x] Tên/handle/mô tả/country/keywords: XONG 2026-08-01 (Claude set qua Studio)
- Ghi chú: tagline trong logo có chữ ヘルシー (外来語) — chỉ là chữ trang trí nhỏ trong avatar/logo, không nằm ở title/thumbnail video nên không phạm luật 45+; nếu sau này regen logo thì thay bằng 「健康・伝統・知恵」 cho tròn vị
- File nguồn gốc user gen: `C:\Users\tuana\Downloads\Gemini_Generated_Image_1jer2t1jer2t1jer (1).png` (logo) + `Gemini_Generated_Image_bd2bv3bd2bv3bd2b.png` (banner); script xử lý banner: scratchpad phiên 2026-08-01 (logic chính: scale 2048 → patch title cũ → vẽ text vào strip)
