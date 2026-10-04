# youtube-jp-co-dai

> Kênh faceless **生活の知恵・忘れられた技術** (mẹo đời sống + kỹ thuật bị lãng quên) cho thị trường Nhật — video ~25 phút giọng phim tài liệu NHK. **Lời hứa kênh:**「昔の人の知恵で、今の困りごとを根本から解決する」— mỗi video = nỗi đau hiện đại có cầu × lời giải「昔はどうしていたか + なぜ効くのか」(cơ chế/lịch sử/nguồn thật là "chất" tách khỏi lifehack AI-slop). Khán giả đích: **Nhật 45–70 tuổi** (nghe như radio buổi tối).

**Trạng thái:** khởi tạo 2026-07-13; **nâng cấp định vị "content là vua" 2026-07-24** (giữ ngách, mở từ 1 trục côn trùng lên 8 trục — xem `02_CONTENT_STRATEGY.md`). Tên kênh: **古代の秘訣**. Voice: VOICEVOX 青山龍星/ノーマル/0.9 (chốt).

## Khác gì các kênh JP khác?

| | youtube-jp-health | youtube-jp-chouhen | **youtube-jp-co-dai (này)** |
|---|---|---|---|
| Ngách | シニア健康 (YMYL) | truyện スカッと朗読 | **mẹo đời sống + kỹ thuật bị lãng quên** |
| Độ dài | 15–20 phút | 60–70 phút | **25 phút mặc định (20–40)** |
| Chế độ | viết mới | REMAKE + viết mới | **A·REWRITE transcript + B·viết mới** |
| Skill | `script-healthy` | `script-chouhen` | **`script-co-dai`** |

Nội dung là FACT thật (nguồn/năm/nhà khoa học giữ nguyên, không bịa) — khác các kênh truyện hư cấu.

## Engine biên kịch

Toàn bộ công thức nằm trong skill **`.claude/skills/script-co-dai/SKILL.md`** (2 chế độ, bộ khung hook–chương–dòng tiền–kết 3 lớp, blacklist sáo ngữ AI + vân tay kênh gốc, checklist 13 điểm, định dạng đầu ra 4 khối: kịch bản TTS + 5 tiêu đề + thumbnail text 3 tầng + prompt ảnh).

- **A·REWRITE:** transcript kênh đối thủ → giữ bộ xương retention + fact thật, viết lại 100% câu chữ (không chuỗi ≥7 chữ trùng) + thay toàn bộ anecdote/ví von → không nhận ra bản gốc, không bị Content ID bắt.
- **B·VIẾT MỚI:** chủ đề 1 dòng → viết mới theo bộ khung.

## Cấu trúc repo

```
youtube-jp-co-dai/
├── youtube-jp-co-dai.md    # file này — tổng quan
├── CLAUDE.md               # config: voice, độ dài/hệ số ô C, thư mục, compliance
├── 01_SOURCES/             # transcript nguồn để rewrite + log đề tài chống trùng
├── 03_SCRIPTS/             # kịch bản sạch <NN>_<slug>.md + bản đọc _TTS.md
├── 05_VOICE/               # mẫu giọng, cấu hình VOICEVOX
└── 06_VIDEO/               # output render + thumbnail
```

## Vault tri thức

`E:\Claude\SecondBrain\10_Projects\youtube-jp-co-dai\`
