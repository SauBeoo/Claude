# CLAUDE.md — GlowUp Studio Project Context

> File này được Claude Code đọc tự động khi làm việc trong project.
> Mục đích: cung cấp full context để Claude hiểu dự án, ra quyết định nhất quán, không cần giải thích lại mỗi session.

---

## 🎯 PROJECT OVERVIEW

**Tên thương hiệu:** GlowUp Studio (gọi tắt "Glow")
**Tagline:** "Để spa của bạn tỏa sáng — online."
**Loại:** Dịch vụ web + tự động hoá + content cho ngành làm đẹp (freelance → studio 2 người)
**Bắt đầu:** Tháng 6/2026
**Giai đoạn hiện tại:** Phase 1 — dựng nền tảng (Tuần 1/12)

**Sứ mệnh:**
Giúp spa, thẩm mỹ viện, nail, salon tóc **lên đời online** — có website đẹp đúng tầm tiệm, tự động hoá
khâu vận hành (nhắc lịch, chăm khách, gom review) và nội dung thu hút khách trên mạng xã hội.

**Ngách chính (đã chốt — không pivot):**
Ngành làm đẹp tại Việt Nam: spa · thẩm mỹ viện · nail · salon tóc.

**Mục tiêu thật của founder (lý do dự án tồn tại):**
Tạo thu nhập thêm 5–10 triệu/tháng để rút thời gian trả khoản nợ ngân hàng 1 tỷ (lãi 8%/năm) từ ~7 năm
xuống 3–4 năm, đồng thời xây **dòng tiền lặp lại / bền vững** (hợp đồng bảo trì + automation), không ăn xổi.
Xem chi tiết tài chính trong `glowup-studio.md`.

---

## 👥 TEAM & ROLES

### Founder / Người dựng (chồng)
- Web developer fulltime, kỹ năng web mức khá, mạnh frontend/web.
- Phụ trách: dựng web cho khách, xây hệ thống tự động hoá (n8n), kỹ thuật, deploy.
- Tiếng Anh trung bình → tập trung thị trường trong nước (không cần Upwork giai đoạn đầu).
- Thời gian đầu tư: ~15 giờ/tuần ngoài giờ làm fulltime.
- Nỗi sợ ban đầu: "không ai thuê" → chiến lược giải: ngách hẹp + demo đẹp + bắt đầu từ khách quen.

### Co-founder / Người kể chuyện (vợ)
- Content creator — đây là **lợi thế lớn nhất** của cặp đôi (đa số dev chết ở khâu marketing).
- Phụ trách: nội dung TikTok/Facebook, quay dựng clip trước/sau, kịch bản, community, chốt khách qua Zalo.

### Phân vai rõ ràng (không lấn việc):
| Việc | Người làm |
|------|-----------|
| Dựng web cho khách, kỹ thuật | Chồng |
| Build automation n8n, deploy | Chồng |
| Demo site, portfolio, web cá nhân | Chồng |
| Content TikTok/Facebook, quay dựng | Vợ |
| Kịch bản, viết bài, lịch đăng | Vợ |
| Chốt khách qua Zalo, CSKH | Vợ (chồng hỗ trợ phần kỹ thuật) |
| Báo giá, brainstorm, quyết định pivot | Cả hai |

---

## 💰 CẤU TRÚC SẢN PHẨM (3 TẦNG — mũi nhọn = WEB)

Chi tiết đầy đủ + bảng giá: `01_SAN_PHAM_GIA.md`.

- **Tầng 1 · WEB (một lần) — mũi nhọn vào khách:** website trọn gói cho spa, 5–12 triệu, xong 7–10 ngày.
- **Tầng 2 · AUTOMATION n8n (upsell + phí tháng):** nhắc lịch, chăm khách, gom review, gom lead.
  Setup 3–8 triệu + duy trì 500k–1,5tr/tháng. Chi tiết: `02_N8N_AUTOMATION.md`.
- **Tầng 3 · BẢO TRÌ + CONTENT (retainer):** 500k–2tr/tháng.

> **Triết lý tiền:** web là *cửa vào*; tiền bền nằm ở Tầng 2 + 3 (dòng tiền lặp lại). 15–20 khách
> retainer ≈ 10–30 triệu/tháng gần như tự chảy — đây là mục tiêu thật, không phải số lượng web bán được.

---

## 🎨 BRAND (tóm tắt — chi tiết ở `00_BRAND.md`)

- **Tên:** GlowUp Studio · **Handle:** `@glowup.studio`
- **Định vị:** Studio giúp spa & thẩm mỹ lên đời online (web + tự động hoá + nội dung).
- **Nghĩa kép "glow up":** vừa làm đẹp, vừa nâng cấp/lên đời.
- **Hệ màu:** hồng pastel `#F4C2C2` + trắng kem `#FAF6F0` + champagne `#E8C9A0` + nâu trầm `#5B4636`.
- **Font:** heading *Playfair Display* (thanh, sang) + body *Be Vietnam Pro* (dễ đọc, tiếng Việt chuẩn).
- **Tông giọng:** thân thiện, tự tin, nói lợi ích cho chủ tiệm (thêm khách, đỡ mệt), tránh thuật ngữ kỹ thuật.

---

## 🛠️ TECH STACK

### Web cho khách & demo
- **Frontend:** HTML/Tailwind cho demo nhanh; **Astro** hoặc **Next.js + Tailwind** cho web khách thật.
- **Deploy:** Vercel / Netlify (free tier) cho landing; hosting trả phí khi khách cần domain riêng.
- **CMS nhẹ (nếu khách tự sửa):** cân nhắc một headless nhẹ; mặc định bàn giao + bảo trì (Tầng 3).

### Automation
- **n8n self-hosted** (founder tự deploy — miễn phí, kiểm soát data) — tái dùng know-how từ project `ai-luoi`.
- **Kênh nhắn tin:** Zalo OA / Zalo ZNS, SMS brandname (qua nhà cung cấp VN), email.
- **Lưu data:** Google Sheets (đơn giản, khách xem được) hoặc Supabase/Postgres khi scale.

### Công cụ content (vợ)
- CapCut (edit), Canva Pro (thumbnail/brand asset), ảnh stock đẹp.

---

## 📌 KEY DECISIONS & CONSTRAINTS

### Đã chốt (không bàn lại):
1. ✅ Ngách: **ngành làm đẹp** (spa/thẩm mỹ/nail/salon) — không pivot.
2. ✅ Thương hiệu: **GlowUp Studio**, mô hình **cặp đôi** (chồng dựng, vợ kể chuyện).
3. ✅ Mũi nhọn: bán **web** trước (dễ chốt), upsell **automation + bảo trì** sau (dòng tiền lặp lại).
4. ✅ Thị trường **trong nước trước** (tiếng Anh trung bình → chưa làm Upwork).
5. ✅ Bắt đầu từ **khách quen** + spa địa phương chưa có web; chốt qua **Zalo**.
6. ✅ Mỗi web khách làm xong → vợ quay 1 clip trước/sau làm content (content = sản phẩm phụ tự nhiên).

### Triết lý cốt lõi:
- **"Web là cửa vào, automation + bảo trì mới là tiền bền."**
- **"Khách đầu tiên không phải người lạ — là spa quanh mình đang thiếu web."**
- **"Người ta thuê khi NHÌN THẤY demo, không phải khi nghe mình nói."**
- **"Tốt > Hoàn hảo. Lấy cái 'yes' đầu tiên > tối ưu mãi."**

### Không làm:
- ❌ Nhận tràn lan mọi ngách (giữ ngách làm đẹp để thành chuyên gia).
- ❌ Hứa "làm giàu nhanh" / cam kết doanh thu ảo cho khách.
- ❌ Bán web rời rạc rồi bỏ — luôn hướng tới retainer (bảo trì/automation).
- ❌ Đốt tiền ads khi chưa có demo + portfolio + vài khách đầu.

---

## 🎯 CURRENT STATUS (update mỗi tuần)

**Tuần hiện tại:** 1 · **Phase:** 1 — Foundation

### Tasks Tuần 1:
- [ ] Dựng web demo spa đầu tiên (`portfolio/demo-spa-01/`) — đẹp, mobile-first.
- [ ] Check & đăng ký handle `@glowup.studio` trên TikTok, Facebook, Zalo; check domain `glowupstudio.vn`.
- [ ] Vợ: dựng kênh TikTok + Facebook theo `03_CONTENT_SOCIAL.md`, quay clip "dựng web spa từ 0".
- [ ] Lập danh sách 20 spa/salon tiềm năng theo `04_OUTREACH.md` (ưu tiên khách quen trước).

### Bottleneck hiện tại:
- Chưa có demo → chưa có gì để chào khách & làm content (việc số 1).
- Chưa chốt domain & handle.

### Next milestone:
- Cuối Tuần 4: chào đủ 20 khách, mục tiêu **1 khách đầu tiên** (xem `05_ROADMAP_90D.md`).

---

## 🤖 INSTRUCTIONS CHO CLAUDE CODE

- **Phong cách trò chuyện với founder (QUAN TRỌNG):** nói chuyện như **bạn thân / tri kỉ** —
  xưng **"tao – mày"**, thật lòng, gần gũi, cái gì cũng chia sẻ được. Đứng về phía founder, muốn
  điều tốt nhất cho cậu ấy. **Vì là bạn thân nên nói thẳng** — khi founder ảo tưởng hoặc định đi
  đường tắt nguy hiểm thì kéo lại, không nịnh, không giả lả. Vẫn giữ nội dung chính xác & trung thực
  (bạn thân = nói thật, kể cả điều khó nghe). Không dùng giọng trợ lý lịch sự xa cách.
  *Bối cảnh:* founder đang gánh nợ 1 tỷ, dựng GlowUp Studio để trả nợ + xây tương lai → cần một
  người đồng hành thật sự, không phải công cụ.
- **Giao tiếp:** tiếng Việt. Code/symbol/function name: tiếng Anh.
- **Web cho khách:** mobile-first (khách của spa 90% xem trên điện thoại), load nhanh, đẹp đúng tông spa,
  luôn có nút **Gọi / Zalo / Đặt lịch** nổi, gallery trước/sau, map, bảng giá rõ.
- **n8n templates:** mỗi flow có README import + setup; không hardcode key (dùng env/credential); comment
  từng node (người dùng cuối là chủ spa, không phải dev); test kỹ trước khi export JSON vào `templates/`.
- **Báo giá/kịch bản:** nói lợi ích cho chủ tiệm (thêm khách, đỡ no-show, đỡ mệt), tránh thuật ngữ kỹ thuật.
- **Decision style:** founder tư duy dev — đưa trade-off rõ ràng, data-driven, không "động viên suông".
  Khi không chắc → hỏi, đừng assume.

---

## 📚 REFERENCE FILES

> Sơ đồ liên kết đầy đủ xem ở hub: [[glowup-studio]]. Dưới đây liệt kê dạng tên file
> (không phải wiki-link) để CLAUDE.md không trở thành hub thứ 2 trong graph Obsidian.

- `00_BRAND.md` — Bộ nhận diện thương hiệu đầy đủ (cho vợ dùng làm content).
- `01_SAN_PHAM_GIA.md` — 3 tầng sản phẩm + bảng giá + mô tả gói.
- `02_N8N_AUTOMATION.md` — Playbook automation cho spa.
- `03_CONTENT_SOCIAL.md` — Kiến trúc kênh + lịch content + kịch bản.
- `content/kich-ban-clip-01-khai-truong.md` — Kịch bản clip TikTok #1 (khai trương).
- `04_OUTREACH.md` — Kịch bản chào khách + danh sách 20 khách + quy trình chốt.
- `05_ROADMAP_90D.md` — Lộ trình 90 ngày.
- `portfolio/demo-spa-01/` — Web demo spa đầu tiên.
- `templates/` — n8n workflow + mẫu báo giá.
- Vault note: `E:\Claude\SecondBrain\10_Projects\glowup-studio\`.

---

## 🔄 CHANGE LOG

| Date | Change | Note |
|------|--------|------|
| 2026-06-11 | Khởi tạo project GlowUp Studio | Phase 1, Tuần 1 — brand + scaffold + demo |
| 2026-06-12 | Thêm rule phong cách trò chuyện "bạn tri kỉ" (tao–mày) | Theo yêu cầu founder |

---

*Update mỗi cuối tuần với progress + bottleneck + decision mới. Quyết định lớn (đổi giá, đổi ngách) log vào Change Log.*
