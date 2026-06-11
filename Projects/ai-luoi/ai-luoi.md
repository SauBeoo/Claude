# AI Lười — Project Repository

Side project MMO của vợ chồng dev + content creator, ngách AI/Automation cho TikTok seller VN.

## 📁 Cấu trúc file

```
ai-luoi/
├── CLAUDE.md              # ⭐ Context file chính cho Claude Code
├── ROADMAP-90DAYS.md      # Roadmap chi tiết theo tuần
├── CONTENT-IDEAS.md       # 30 ý tưởng video + 3 script mẫu
└── README.md              # File này
```

## 🚀 Cách dùng với Claude Code

### Bước 1: Clone/copy folder này vào máy local

```bash
# Tạo thư mục dự án trên máy bạn
mkdir ~/projects/ai-luoi
cd ~/projects/ai-luoi

# Copy 4 file vào thư mục này
```

### Bước 2: Khởi tạo git (optional nhưng nên làm)

```bash
git init
git add .
git commit -m "Initial: import project context"
```

### Bước 3: Mở Claude Code trong thư mục

```bash
cd ~/projects/ai-luoi
claude
```

Claude Code sẽ tự động đọc `CLAUDE.md` và hiểu toàn bộ context dự án.

### Bước 4: Bắt đầu làm việc

Ví dụ các lệnh bạn có thể dùng ngay:

```
> Hãy giúp tôi build landing page lead magnet "5 template n8n free" theo guidelines trong CLAUDE.md

> Tạo 1 workflow n8n template số 1 - "Auto reply tin nhắn Pancake bằng ChatGPT"

> Setup Next.js project cho landing page với Tailwind + form thu email tích hợp MailerLite

> Tôi đang ở tuần 2, hãy review xem tôi cần build những gì kỹ thuật để chuẩn bị tuần 3
```

Claude Code sẽ hiểu:
- Bạn là dev fulltime, vợ là content creator
- Project name là "AI Lười", ngách seller VN
- Stack ưu tiên: Next.js + Tailwind + n8n + Supabase
- Bạn đang ở Phase 1 Tuần 1/12
- Không bán hàng cứng, focus build audience trước

## 🔄 Update Cycle

**Mỗi cuối tuần (CN):**
1. Update `CURRENT STATUS` trong CLAUDE.md với progress + bottleneck mới
2. Update `Change Log` với decisions quan trọng
3. Tick checkbox đã làm trong ROADMAP-90DAYS.md
4. Update bảng tracking với KPIs thực tế

**Mỗi cuối tháng:**
1. Review lại pricing, monetization tier
2. Update CONTENT-IDEAS.md với topic mới phát hiện viral
3. Document tech decisions vào file mới (`TECH-DECISIONS.md`)

## 📌 Quan trọng

- `CLAUDE.md` là single source of truth — Claude Code đọc file này mỗi khi start session
- Khi pivot/đổi quyết định lớn → update CLAUDE.md NGAY, không để memory drift
- Founder thích communication style: tiếng Việt, data-driven, technical analogies, không motivational fluff

## 🎯 Quick Reference

| Cần làm gì | Đọc file nào |
|------------|--------------|
| Hiểu tổng quan dự án | CLAUDE.md |
| Tuần này làm gì | ROADMAP-90DAYS.md → Phase 1 |
| Tìm ý tưởng quay | CONTENT-IDEAS.md |
| Quyết định brand/style | CLAUDE.md → Brand Guidelines |
| Quyết định tech stack | CLAUDE.md → Tech Stack |

## 🔗 Liên kết nội bộ

- [[ai-luoi/CLAUDE|CLAUDE.md — context dự án]]
- [[ai-luoi/ROADMAP-90DAYS|Roadmap 90 ngày]]
- [[ai-luoi/CONTENT-IDEAS|Ý tưởng content + script mẫu]]

---

*Generated 2026-05-25. Phase 1, Week 1.*
