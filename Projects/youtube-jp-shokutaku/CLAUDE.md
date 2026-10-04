# CLAUDE.md — youtube-jp-shokutaku (rút gọn 2026-08-24)

## ① Identity
- Kênh **60代からの食卓** — persona **みのり** (giọng gian bếp; KHÔNG xưng 医師・先生・管理栄養士・専門家; cấm 医師が解説/医師警告 ở script/title/thumbnail).
- Tệp: JP 60–80. **categoryId 27**. Vault: `SecondBrain\10_Projects\youtube-jp-shokutaku\`.
- **Độ dài: user chốt 2026-08-25 = DƯỚI 20 PHÚT** (video 19 = 19′11 · video 20 = 19′20). ⚠️ Đè dải cũ **21–25 phút** vốn dựa trên số đo (納豆 cắt 29′→15′ làm **AVD phút tụt 4′33 → 3′11**, `CHANNEL_DIAGNOSIS_2026-08-11`). ⇒ **Nếu AVD phút của 19/20 thấp hơn 17/18 thì độ dài là biến ĐẦU TIÊN xét lại**, không phải cold open. Cách cắt đã dùng: bỏ khối RỜI khỏi ẩn dụ trung tâm, giữ nguyên cold open + anecdote + callback; và **dời khối thay vì cắt** khi cần kéo payoff về ≥75%.
- **FORMAT CHỐT CỨNG (từ video 18):** minh hoạ AI kawaii pastel TĨNH + **khung sân khấu** (gradient + thẻ trắng bo góc + 2 cast cắt-nền + dải đen đáy) + dựng bằng **remotion-vox**. Motion `"none"`. KHÔNG stock-clip, KHÔNG HeyGen, KHÔNG tick altered/synthetic.

## ② Sản xuất
- Giọng: **VOICEVOX 青山龍星 / しっとり / speed 0.8** (dự phòng AivisSpeech 阿井田茂/まお).
- `_TTS.md`: **mỗi dòng = MỘT CÂU** (= 1 cue phụ đề).
- **Pipeline 6 bước** (đổi số `18` → số video mới):
```
1. py tools\build_slides_18.py        # PLAN + prompt FLOW → user gen ảnh
2. py tools\cutout_cast.py            # chỉ khi thêm cast mới (nền magenta #FF00FF)
3. py tools\ingest_slides_18.py       # trim viền + vá ✦ + dán khung sân khấu
4. py ...\remotion-vox\tools\import_pipeline.py    # slide+voice+srt → project.json
5. py ...\remotion-vox\tools\build_overlays_18.py  # wipe+overlay+siết phụ đề — KHÔNG BỎ
6. run_full18.cmd (chạy NỀN)          # chunk render → deliver --mp4 → cta_inject
```
- **Gate máy trước render:** `python tools\check_coldopen.py <NN>` — PASS mới render. 5 luật: L1 mục đầu ≤90s (413 ký) · L2 không câu miễn trừ/tháo ngòi · L3 persona/CTA sau mục đầu · L4 case study sau mục đầu · L5 ≥3 câu 「〜ませんか」 riêng lẻ. Mốc `# ITEM1` trước câu hé mục đầu — thiếu = FAIL.
- Thông số Remotion chốt: wipe 14 frame luân phiên hướng · phụ đề fontSize **38px thực**, cue ≤46 ký · watermark 「60代の食卓」 `#FFD24A (1586,40)` trọn bài · overlay chỉ nửa TRÁI, clamp `H_MAX 320` + `W_MAX 200` · render `--chunk 5000 --concurrency 2 --cache-mb 512`.
- 🔴 **3 thứ Remotion KHÔNG tự làm:** watermark kênh · CTA overlay (`cta_inject.py --in-place`, đã trong run_full18.cmd) · siết cue phụ đề. `deliver.py` PHẢI có `--mp4 out\<slug>.mp4` (thiếu = render lại từ đầu).
- Ảnh gen: trim viền + cắt dải trắng đáy trước khi pad (`media-library.md` §2.10 ⑧) · vá ✦ theo LÔ · cast có `POSE_MAP` đổi tư thế theo đoạn.
- 🔴 **`cta_inject.py` PHÁ VIDEO — BỎ HẲN khỏi đường remotion (chốt 2026-08-25, video 20).** Không chỉ "card CTA không hiện" như ghi trước: nó **XOÁ PHỤ ĐỀ trong cả đoạn re-encode**. Đo thật video 20: log báo `CTA @ 579.51s → overlay 579.31..587.31`, `re-encode [566.83..591.83]`, `CTA_EXIT=0` — nhưng frame 570/580/584/586 **mất sạch phụ đề** (0 pixel sáng trong dải đen) trong khi `subs.srt` có **6 cue** ở đúng vùng đó, và bản `remotion-vox/out/*.mp4` trước inject thì **có phụ đề**. Tức 25 giây video hỏng, exit 0, không một dòng cảnh báo.
  - **Cách chữa (rẻ, không render lại):** chạy lại `deliver.py --mp4 out\<stem>.mp4` — nó `-c:v copy` nên chỉ mất vài chục giây, và ghi đè bản hỏng. `run_full20.cmd` đã BỎ bước cta_inject; wrapper video sau chép từ file đó.
  - ⚖️ **Cái mất:** lớp hình CTA (card like/share/chuông + SFX) — nhưng **câu CTA vẫn được ĐỌC** vì nó nằm trong `_TTS.md` (`cta-midvideo.md` §1 mục 1: câu CTA là DÒNG trong TTS, overlay chỉ là lớp bổ sung). Video 20 vẫn có CTA giữa ở 09:23 bằng giọng + phụ đề.
  - ⚠️ Muốn bật lại lớp hình thì phải sửa `cta_inject.py` cho đường remotion (nó viết cho renderer cũ `video_render.py`), **không phải chỉnh toạ độ card** như phỏng đoán cũ.

## ③ Luật riêng còn hiệu lực
- **Script PHẢI theo skill `script-shokutaku`** (4 bước ngầm, bộ xương Mục 10, checklist Mục 14). Đề tài theo `03_CONTENT_PLAN.md`, hết hàng đợi → đo trend vòng mới.
- **Chế độ A·REMAKE** transcript: giữ xương retention, viết lại 100% câu chữ; nguồn → `01_SOURCES/`.
- **Cold open:** câu 1 = stake (+かもしれません) · mục 1 trước giây ~70 · khối persona + xin đăng ký đặt SAU payoff đầu · CẤM câu tự tháo ngòi lời hứa (cửa tử giây 20→40). Mục tiêu AVD 60%: @40s ≥85% · sàn thân bài ≥55%. Payoff #1 trước phút 4. Đọc bằng relPerf 15–45s + AVD%, không bằng view.
- **YMYL (chặt như health):** KHÔNG bịa nguồn/số · nguồn thật giữ nguyên tên (厚労省…), không chắc → 「〜という報告があります」 · cấm 治る・完治・薬の代わり → 守る・支える・整える・〜かも · không khuyên ngừng/đổi thuốc · disclaimer cố định CUỐI video · cảnh báo điều kiện tại chỗ (kali×腎臓, 納豆×ワーファリン).
- **Lớp `genten`:** ≥1 khối trích NGUỒN THẬT/video (cơ quan + 年版/時点 + số trích đúng) — được phép là thẻ 出典 trên hình đúng cue; ghi 概要欄 thôi KHÔNG tính. Việc của Claude, không bắt user quay.
- **CẤM slide-chữ (drawn/card/vox chữ)** — 100% ảnh: `media-library.md` §2.9. Thiếu ảnh số liệu → viết prompt cho user gen.
- Anecdote: tên+tuổi+tỉnh+nghề MỚI mỗi script, mở 「例えば、こんな方がいらっしゃるとします」.
- **Thumbnail+Title:** spec `02_THUMBNAIL_TITLE_RULES.md` (Phần D DESIGN-FIRST + Phần E ảnh full-bleed moody + cột MÓN/TWIST/STAKE). Tool: `compose_thumb_bg.py` → `make_thumb.py`. 3 cửa tự duyệt + 120px. KHÔNG bác sĩ/áo blouse/claim khỏi bệnh.
- Lịch: **T2·T4·T6 17:00 JST, 3/tuần** (giờ ĐỔI 12:00 → 17:00 ngày 2026-08-26 THEO SỐ ĐO: 17h thắng 19h **16×** trong cùng kênh 健康長寿の知恵袋TV với tuổi video chạy ngược, 19h là giờ BÉT ngách, top ngách 若返りアカデミア khoá 17h 18/18 — `upload-schedule-measure-hours-2026-08-26.md`; 🛑 phanh 10 video → về 12:00) — nguồn sự thật `upload-schedule.md` §0.9.
- Trục đang chạy: luồng **食べ合わせ** (món làm chủ ngữ; ⛔ tránh rổ tạng-làm-chủ-ngữ + món bão hoà 納豆/卵/ブルーベリー). Mốc "8 video qua gate mà BROWSE=0 → mở bàn 3 đường" (~08-25) còn hiệu lực.
- Studio: từng dính **default upload tags** sinh tag rác — API không sửa được, kiểm tay khi thấy tag lạ.

## ④ Trỏ
- Skill: `script-shokutaku` · `video-render` · `vox-collage-video`.
- Doc project: `02_THUMBNAIL_TITLE_RULES.md` · `03_CONTENT_PLAN.md` · `04_SCRIPTS/18_ringo-tabekata.md` §9 (chi tiết format).
- Rules toàn cục (`.claude/rules/`): youtube-compliance · audience-45plus · humanize-script-voice · media-library · render-background · upload-schedule · youtube-upload-seo · ab-3title-3thumb · cta-midvideo · youtube-suggested-growth.

> Bản đầy đủ: ./_archive/CLAUDE_FULL_2026-08-24.md · Doc cũ khác cũng ở ./_archive/
