# E:\Claude\ — Hệ thống làm việc của tôi

Workspace tổng hợp gồm bộ não 2 (SecondBrain) + project repos (Projects) + cấu hình Claude Code (.claude-global).

## 🖥️ Clone về máy mới để làm video (cập nhật 2026-10-04)

Repo `git@github.com:SauBeoo/Claude.git` **chỉ chứa CÔNG THỨC**: code tool, rule/skill/CLAUDE.md, kịch bản `.md`/`_TTS.md`/SLIDES, prompt `.txt`, font.
**KHÔNG chứa** (chặn ở `.gitignore`): ảnh · video · âm thanh · `node_modules` · `_tts_cache` · output Remotion · model AI · `.exe` · `credentials/` · log.
⇒ Clone xong phải làm đủ các bước dưới mới dựng được video.

### 1. Clone đúng đường dẫn
```powershell
git clone git@github.com:SauBeoo/Claude.git E:\Claude
```
⚠️ Phải đặt ở **`E:\Claude\`** — rule, tool và `.cmd` dùng đường dẫn tuyệt đối `E:\Claude\...`.

### 2. Cài phần mềm nền
| Phần mềm | Dùng cho |
|---|---|
| Python 3.11+ | mọi tool trong `Projects/*/tools`, `_media_library` |
| Node.js LTS | Remotion (`Projects/remotion-vox`) — nenkin dựng bằng đường này |
| ffmpeg (có trong `PATH`) | ghép/encode, đo âm lượng, cắt clip |
| VOICEVOX (bật app, cổng `50021`) | giọng đọc TTS |
| Git + SSH key GitHub | pull/push |
| Chrome | upload Studio theo profile kênh (`.claude/rules/channel-browser.md`) |

### 3. Cài thư viện
```powershell
pip install pillow numpy opencv-python scipy requests pytrends rembg pymupdf onnxruntime faster-whisper openai-whisper playwright flask google-api-python-client google-auth-oauthlib
python -m playwright install chromium
cd E:\Claude\Projects\remotion-vox; npm install
pip install -r E:\Claude\Projects\yt-dashboard\requirements.txt
```

### 4. Chép tay từ máy cũ (git không mang theo)
| Chép folder/file | Vì sao cần |
|---|---|
| `Projects/*/assets/` (cast, icons, irasutoya, sfx_lab) | nhân vật + icon trên sân khấu |
| `Projects/*/00_BRAND/`, `09_BRAND/`, `branding/` | banner, narrator, bộ nhận diện kênh |
| `Projects/_media_library/props/`, `stage_icons/`, `avatars/` | đồ dùng chung của `make_stage` |
| `Projects/*/06_VIDEO/bgm/`, `06_VIDEO/_sfx/` | BGM + SFX |
| `Projects/remotion-vox/public/shared/`, `public/sfx/` | asset chung của Remotion (chỉ phần ảnh/âm thanh; font đã có trong git) |
| `Projects/_media_library/models/depth_anything_v2_small.onnx` | model độ sâu (hoặc tải lại từ HuggingFace) |
| `Projects/_tools/realesrgan/` (exe + `models/`) | upscale ảnh (hoặc tải `realesrgan-ncnn-vulkan` bản Windows) |
| `Projects/*/credentials/` | OAuth token từng kênh cho `upload_api.py` / analytics — **tuyệt đối không commit** |
| `**/.pexels_key` và các file `.*_key` | API key |
| `C:\Users\<user>\.claude\` (agents, skills toàn cục, `projects\E--Claude\memory\`) | memory + cấu hình Claude Code — nằm ngoài repo |

Không cần chép: `_tts_cache` (tự sinh lại khi synth), media trong `06_VIDEO/<slug>/` của video đã đăng.

### 5. Kiểm tra máy đã sẵn sàng
```powershell
ffmpeg -version
curl http://127.0.0.1:50021/version          # VOICEVOX đang chạy
cd E:\Claude\Projects\remotion-vox; npx remotion --version
```

### ⚠️ Lưu ý
- **Showa chưa render được từ repo**: renderer `video_render.py` + `channels.py` đang được dời khỏi `youtube-jp-health/tools/` (thư mục này đang rỗng) sang `Projects/_render/`. Dời xong phải commit + push thì máy mới có.
- `git add -A` giờ an toàn (~3.000 file, ~10 giây). Đừng gỡ khối chặn media cuối `.gitignore` — một lần add 47.000 file media từng làm treo git và để lại 25 GB rác trong `.git`.
- Workspace dùng nhiều phiên Claude cùng lúc → trước khi commit xem `git status` có file staged lạ không.

## 📂 Cấu trúc

```
E:\Claude\
│
├── SecondBrain\              # 🧠 Bộ não 2 — vault Obsidian
│   ├── 00_Inbox\             # Vùng đệm
│   ├── 10_Projects\          # Note về project đang chạy
│   ├── 20_Areas\             # Kinh nghiệm dài hạn
│   ├── 30_Resources\         # Tham khảo theo chủ đề
│   ├── 40_Archive\           # Đã hoàn thành
│   ├── 50_Atomic\            # Ý tưởng đã chắt lọc ⭐
│   ├── 60_Daily\             # Daily note
│   └── 99_Meta\              # Template, MOC
│
├── Projects\                 # 💻 Code repos
│   ├── research-llm-education-2026\   # Project nghiên cứu
│   └── student-grade-app\             # Project sản phẩm
│
└── .claude\           # ⚙️ Cấu hình Claude Code
    ├── CLAUDE.md
    ├── agents\               # 5 agents (researcher, teacher, coder, creator, librarian)
    └── skills\               # 5 skills
```

**Lưu ý:** `.claude-global\` ở đây chỉ là **bản copy để bạn đọc**. Cài đặt thật phải copy vào `C:\Users\<tên-bạn>\.claude\` thì Claude Code mới nhận.

## 🚀 Bước cài đặt

### 1. Giải nén/copy vào E:\Claude\

```powershell
# Đặt 3 thư mục SecondBrain, Projects, .claude-global vào E:\Claude\
```

### 2. Install cấu hình Claude

```powershell
# Copy nội dung .claude-global\ vào ~/.claude/
mkdir $HOME\.claude -Force
Copy-Item -Recurse -Force E:\Claude\.claude-global\* $HOME\.claude\
```

### 3. Mở vault trong Obsidian

- Mở Obsidian → "Open folder as vault" → chọn `E:\Claude\SecondBrain\`
- Settings → Templates → Template folder: `99_Meta/templates`
- Settings → Daily notes → New file location: `60_Daily/YYYY/MM`

### 4. Init Git cho từng repo (tùy chọn)

```powershell
# Vault (private repo)
cd E:\Claude\SecondBrain
git init
git add .
git commit -m "init: vault structure"

# Project research
cd E:\Claude\Projects\research-llm-education-2026
git init
git add .
git commit -m "init: project skeleton"

# Project app
cd E:\Claude\Projects\student-grade-app
git init
git add .
git commit -m "init: project skeleton"
```

### 5. Test Claude Code

```powershell
cd E:\Claude\SecondBrain
claude
# Trong session, gõ:
> "Liệt kê các agent có sẵn"
```

Expected: Claude liệt kê 5 agent (researcher, teacher, coder, creator, librarian).

## 🎯 Workflow cơ bản

### Khi đọc paper

```
cd E:\Claude\Projects\research-llm-education-2026
claude
> "Tóm tắt paper trong D:\Downloads\new-paper.pdf"
```

Claude (đeo mặt nạ researcher) tóm tắt → lưu vào `SecondBrain\10_Projects\research-llm-education-2026\papers\` → đề xuất atomic notes.

### Khi soạn bài giảng

```
cd E:\Claude\SecondBrain
claude
> "/agent teacher
> Soạn buổi 9 môn Python về Debug"
```

Claude tìm atomic notes liên quan trong vault → tạo lecture note với link tham khảo.

### Khi code

```
cd E:\Claude\Projects\student-grade-app
claude
> "Review hàm calculate_gpa() trong app/services/grade.py"
```

Claude (đeo mặt nạ coder) review. Sau khi xong:
```
> "Lưu kinh nghiệm này vào bộ não"
```
→ Tạo note ở `SecondBrain\20_Areas\coding-practices\`.

### Khi dọn dẹp

```
cd E:\Claude\SecondBrain
claude
> "/agent librarian
> Dọn Inbox và đề xuất chắt lọc tuần này"
```

## 📚 Đọc thêm

- Cấu hình Claude: `.claude-global\README.md`
- Quy tắc vault: `SecondBrain\.claude\CLAUDE.md`
- Tag system: `SecondBrain\99_Meta\tag-system.md`
- Hướng dẫn từng thư mục vault: README.md trong mỗi thư mục
