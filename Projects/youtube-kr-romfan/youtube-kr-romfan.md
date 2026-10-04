# youtube-kr-romfan

Project kênh YouTube audio truyện cho **thị trường Hàn Quốc** — nhân bản mô hình kênh audio drama (như youtube-jp-chouhen) sang ngách **로맨스 판타지 hiện đại / 사이다 복수** (계약결혼, 재벌가, 시월드), khán giả nữ Hàn 18–35.

## Mục tiêu

- Kênh: **이불속극장** — truyện audio nghe trước khi ngủ, giọng TTS nữ, video ~40 phút.
- Nội dung: transcreation từ transcript nguồn (Việt/Trung việt hóa) hoặc viết mới — chuẩn "người Hàn bản xứ nghe không nhận ra truyện dịch".
- Pipeline: script (skill `script-kr-romfan`) → TTS Azure (SunHi) → render video → đóng gói CTR + compliance.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `01_SOURCES/` | transcript gốc cần bản địa hóa, research thị trường |
| `02_SCRIPTS/` | kịch bản `NN_slug.md` + bản TTS sạch `NN_slug_TTS.md` |
| `03_VOICE/` | audio xuất từ Azure TTS |
| `04_VIDEO/` | video thành phẩm + thumbnail |

## Cách chạy

1. Dán transcript (chế độ A) hoặc premise (chế độ B) → skill `script-kr-romfan` tự kích hoạt, xuất 5 khối (kịch bản + tiêu đề + thumbnail text + prompt ảnh + watermark).
2. Voice: `python tools/azure_tts.py 02_SCRIPTS/NN_slug_TTS.md` — Azure Speech `koreacentral`, giọng chính `ko-KR-SunHiNeural`, nam `ko-KR-InJoonNeural` hạ tông; xuất `voice.wav + subs.srt + timeline.json` vào `03_VOICE/` — chi tiết trong `CLAUDE.md`.
3. Render: theo pipeline video-render (BGM -40 dB, mỗi video một nền riêng).

## Liên kết

- Luật vận hành: `CLAUDE.md` (cùng folder)
- Skill biên kịch: `~/.claude/skills/script-kr-romfan/SKILL.md`
- Compliance: `E:\Claude\.claude\rules\youtube-compliance.md`
- Vault tri thức: `E:\Claude\SecondBrain\10_Projects\youtube-kr-romfan\youtube-kr-romfan.md`
- Demo giọng: `E:\Claude\Projects\youtube-jp-chouhen\01_SOURCES\kr_voice_demo\`
