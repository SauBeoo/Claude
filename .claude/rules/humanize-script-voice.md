# YẾU TỐ CON NGƯỜI — kịch bản có hồn + giọng không đều đều (RULE TOÀN HỆ THỐNG)

> **Nguồn sự thật DUY NHẤT** về làm kịch bản & giọng đọc "ra người". Áp cho **nenkin** + **showa**.
> Chốt 2026-07-29 (user: *"kịch bản có hồn, có yếu tố con người… giọng đọc cũng vậy, không đều đều robot"*).
> Rule này lo **CHẤT NGƯỜI**; cấu trúc/retention xem skill/CLAUDE.md từng kênh, render xem `render-background.md`.

## 0. Ý ĐỒ
Gate cấu trúc (cold open, ẩn dụ, transition) **không đo được chất người** — một kịch bản đúng hết gate vẫn nghe như robot. Năm bệnh đo được: ① người kể vô hình ② nhân vật là hồ sơ (không thoại, không đời sống; chuỗi 「〜そうです」) ③ zero ký ức giác quan ④ nhịp câu đều tăm tắp ⑤ **giọng cả bài một tag style** — nặng nhất và rẻ nhất để chữa.

## 1. LUẬT — 6 mũi tiêm chất người (mỗi kịch bản ≥4/6)
1. **Người kể xuất hiện ≥1 lần bằng trải nghiệm thật** — tự trào an toàn nhất (thú nhận cùng một cái sai với người xem), không phải khoe uy tín.
2. **Nhân vật case có ≥1 CÂU THOẠI + 1 chi tiết đời sống** vô dụng-về-thông-tin.
3. **≥1 ký ức giác quan neo vào tệp khán giả** — âm thanh/mùi/xúc giác thời họ sống.
4. **Người kể tự NẾM/tự LÀM thứ mình khuyên.**
5. **Đóng nhân vật bằng CẢM XÚC**, không bằng kết luận.
6. **Phá nhịp câu ≥3 lần/bài**: câu cụt · cảm thán · tự cắt lời · câu 3 chữ đứng riêng.

**Cấm:** ⓐ bịa trải nghiệm dính số/nguồn ⓑ 「〜そうです」 quá 2 lần liên tiếp ⓒ nhân vật có tên mà không có thoại.

### 1.1 Ngoại lệ theo kênh (ngưỡng ≥4/6 giữ nguyên)
- **nenkin (YMYL tiền):** ⛔ người dẫn **cấm** kể trải nghiệm cá nhân (persona 案内役 vô danh). Mũi ① và ④ **chuyển sang CAST モニター** (hư cấu có nhãn — được kể trải nghiệm, được làm, sai rồi sửa). Người dẫn giữ vai quan sát + đồng cảm (「この書類、初めて見ると…分からないですよね」 — thấu cảm, không vi phạm). Mũi ②③⑤⑥ áp bình thường.
- **yawa (user duyệt 2026-09-29, khuôn liệt kê):** người kể **vô danh** nói với あなた, không kể chuyện mình. Mũi ① **tính là ĐẠT khi đi qua 証人 người quen** (「私の知人の、七十代の女性は…」 — hư cấu, một người xuyên bài) hoặc khi người quen **tự thú cái sai của họ**. Mũi ②④ cũng đi qua người quen. Khuôn: `youtube-jp-yawa/05_SCRIPT_FORMULA.md` §6.
- **showa:** mũi ① **tính là ĐẠT khi đi qua 証人** — người làm chứng có thật, nêu tuổi + quan hệ (「65の私の父の話です」/「七十代になる私の知人に聞いたところ」). Không đòi người dẫn kể chuyện mình, cũng không cấm. Mũi ④ đi qua nhân vật. Bằng chứng: `youtube-jp-showa/05_SCRIPT_FORMULA.md` §0.1, §2.

## 2. LUẬT — lớp NHẤN NHÁ GIỌNG (bắt buộc mọi `_TTS.md`)
**Giữ MỘT giọng, MỘT style nền** (cấm rải tag đổi style). Chất người đến từ **chênh lệch tốc độ/ngữ điệu/khoảng nghỉ giữa các đoạn**.
**Mật độ:** ~15–25 tag / video 15–20′. <10 = vẫn đều; mọi dòng đều tag = mất điểm nhấn.

| Khoảnh khắc | Tag (VOICEVOX, parser `youtube-jp-health/tools/tts_render.py`) |
|---|---|
| Câu đâm của hook | `[間0.5]` trước + `[抑揚1.25]` |
| Hoài niệm / tâm tình / tự trào | `[速0.85]` |
| Thoại nhân vật + cảm thán | `[抑揚1.25–1.3]` |
| Reveal giữa bài | `[間0.8]` trước câu chốt |
| **ĐỈNH BÀI** | `[間1.2][速0.8][後間1.0]` — im lặng sau đó là phần đắt nhất |
| Nghịch lý / đòn logic | `[速0.82][抑揚1.3]` |
| Chữ ký đóng | `[速0.85]` + `[間0.6]` |

Cú pháp: `[速0.85] [抑揚1.3] [高±N] [音量N] [間N] [後間N]`.

### 2.1 🔴 Hai bẫy cú pháp
**① Tag CHỈ ăn ở ĐẦU DÒNG.** Giữa câu → TTS **đọc thành lời**. Muốn nghỉ giữa câu: cắt thành 2 dòng, tag ở đầu dòng 2, **dính liền chữ** (`[間0.4]あの三千円は、`). Tag sau `「` cũng là giữa dòng.
**② Tag đứng MỘT DÒNG RIÊNG = đổi MẶC ĐỊNH VĨNH VIỄN.** `parse_script` coi dòng chỉ-có-tag là đổi `defaults` cho phần còn lại của bài → `速` trôi một chiều rồi ở đó, chênh lệch biến mất; `[後間N]` đứng riêng **bị bỏ hoàn toàn**; chỉ `[間N]` vẫn ăn nên nghe thử ngắn thấy "ổn". ✅ Khuôn đúng: `[間1.2][速0.8][後間1.0]「……知っていました」`. Gộp tag vào dòng câu ngay sau; `[後間N]` gộp vào dòng câu ngay trước.

**GATE MÁY (cả hai phải ra 0 dòng):**
```bash
# ① tag không ở đầu dòng
python -c "import re,sys;f=sys.argv[1];[print(i+1,l.rstrip()) for i,l in enumerate(open(f,encoding='utf-8')) for m in re.finditer(r'\[[^\]]*\]',l) if m.start() and not re.fullmatch(r'(\[[^\]]*\])+',l[:m.start()])]" <file>_TTS.md
# ② tag đứng một dòng riêng
python -c "import re,sys;print(sum(1 for l in open(sys.argv[1],encoding='utf-8') if re.fullmatch(r'(?:\[[^\]]+\])+\s*',l)))" <file>_TTS.md
```
⛔ Gate cũ `grep "。\[\|、\["` hỏng (không thấy tag sau `「`) — đừng dùng một mình.
⚠️ Kiểm `速` có ăn không bằng **thí nghiệm đối chứng** (synth cùng một câu 2 biến thể, so thời lượng; `速0.8` ≈ +20%), đừng đo ký/giây (nhiễu bởi 「」「……」).

## 3. QUY TRÌNH BẮT BUỘC — RENDER DEMO TRƯỚC
1. Tách 1–2 đoạn đắt nhất ra `06_VIDEO/<slug>/demo_humanize_TTS.md`.
2. Synth bằng thông số **đúng hồ sơ kênh** (`tools/channels.py`) → nghe. In bảng `dur/speed/intonation` từng dòng để thấy tag nào không ăn.
3. Duyệt xong mới áp vào bài + render đầy đủ.

## 4. SỬA BÀI ĐÃ CÓ THÌ SỬA ĐỦ 3 CHỖ
1. **`_TTS.md` VÀ bản `.md` sạch** cùng lượt.
2. **Quét lại chuỗi `match` trong SLIDES** (strip tag khỏi TTS rồi kiểm từng `match` còn là substring) — sửa câu là chết cue.
3. Ghi sổ vòng sửa trong file `.md` + chạy lại gate của kênh.
Video đã render mà sửa lời → re-render voice (cache theo nội dung dòng) + dựng lại video + đo lại `subs.srt`/目次.

## 5. LIÊN QUAN
- 1 giọng, không rải tag đổi style: memory `feedback_video_no_motion_mot_giong` · cache TTS: `project_tts_cache_retry`
- Bẫy resume khi render lại: `render-background.md` §2.5
