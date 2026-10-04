# youtube-jp-chouhen

> Kênh faceless **AI朗読 / スカッと系・長編朗読ドラマ** cho thị trường Nhật — truyện trả thù hả dạ dạng radio-drama **~2 tiếng**, kể ngôi thứ nhất「私」. Hình ảnh: **1 nền video động ambient (sông/suối) không bản quyền, lặp suốt bài** + phụ đề (KHÔNG ảnh AI từng cảnh). Khán giả đích: **nữ Nhật 45–70 tuổi** (nghe trước khi ngủ).

**Trạng thái:** khởi tạo 2026-07-07. Tên kênh: **真夜中の朗読便** (cùng kênh với youtube-jp-sukatto, khác dòng format).

## Khác gì với youtube-jp-sukatto?

| | youtube-jp-sukatto | **youtube-jp-chouhen (này)** |
|---|---|---|
| Độ dài | 45–60 phút | **~120–135 phút (2 tiếng)** |
| Số ký tự | ~14.000–18.000 | **17.000–21.000** |
| Chế độ | chỉ viết mới | **REMAKE transcript + viết mới** |
| Skill | `script-sukatto` | **`script-chouhen`** |

Hai project **độc lập, song song** (user chốt 2026-07-07). Cùng ngách スカッと nhưng khác chuẩn độ dài & quy trình — đừng lẫn.

## Engine biên kịch

Toàn bộ công thức nằm trong skill **`.claude/skills/script-chouhen/SKILL.md`** (bộ khung 9 nhịp, 2 chế độ A·REMAKE / B·VIẾT MỚI, bảng hoán đổi 10 yếu tố chống trùng, checklist 14 điểm, định dạng đầu ra 4 khối). Claude tự gọi khi user dán transcript朗読 để làm lại hoặc yêu cầu truyện 2 tiếng.

- **A·REMAKE:** transcript nguồn → giữ nguyên bộ xương 9 nhịp, thay 100% da thịt (tên/nghề/lễ nghi/tài sản/vật chứng/thoại) → không nhận ra bản gốc + không bị YouTube gắn cờ tái sử dụng.
- **B·VIẾT MỚI:** premise 1 dòng → viết mới theo bộ khung.

## Bộ khung 9 nhịp (tóm tắt)

1. コールドオープン — thoại độc phản diện + đóng băng + forward-tease
2. 屈辱の儀式 — sỉ nhục công khai trên sân khấu lễ nghi
3. 献身の回想 — flashback "sổ ghi công" (chi tiết cảm quan)
4. 静かな布石 — chính diện bày binh ngầm / phản diện leo thang
5. 逆転の連鎖 — thác trả thù ≥5 tầng (vật chứng + cú sốc mỗi tầng)
6. 土下座と宣告 — phản diện quỳ, chính diện tuyên án
7. 因果の確定 — chốt số phận từng kẻ ác
8. 新しい朝 — nhảy thời gian, đời mới, câu kết đời
9. 締めの挨拶 — câu kết kênh cố định

## Cấu trúc repo

```
youtube-jp-chouhen/
├── youtube-jp-chouhen.md    # file này — tổng quan
├── CLAUDE.md                # config: voice, tên kênh, độ dài/hệ số ô C, thumbnail
├── 01_SOURCES/              # transcript nguồn để REMAKE + log đề tài chống trùng
├── 03_SCRIPTS/              # kịch bản sạch <NN>_<slug>.md + bản đọc _TTS.md
├── 05_VOICE/                # mẫu giọng, cấu hình AivisSpeech
└── 06_VIDEO/                # output render + thumbnail
```

## Vault tri thức

`E:\Claude\SecondBrain\10_Projects\youtube-jp-chouhen\`
