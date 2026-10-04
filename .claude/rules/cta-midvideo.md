# CTA giữa video (like + share + comment) — RULE TOÀN HỆ THỐNG

> Nguồn sự thật DUY NHẤT cho câu CTA giữa video. Kênh đang chạy: **nenkin · showa**.

## 0. Ý ĐỒ
1 đoạn CTA ở **~50%**: ① 高評価 ② シェア (bọc "gửi cho người thân/bạn cùng thế hệ") ③ comment góp ý/gợi ý chủ đề. Là CTA **bổ sung**, không thay CTA cuối.
⛔ **yawa: KHÔNG có CTA giữa video** (user chốt 2026-09-29 — kênh thắng ngách 0/5 video có CTA giữa bài; chỉ comment + sub ở cuối, `youtube-jp-yawa/05_SCRIPT_FORMULA.md` §2 khối ⑦).

## 1. NGUYÊN TẮC KỸ THUẬT
1. CTA là **dòng trong `_TTS.md`** (đọc bằng TTS, ra phụ đề).
2. Chèn ở **ranh giới cảnh/khối gần 50%**, 1 dòng trống trước & sau; không cắt ngang cảnh.
3. Không đặt ngay trước một reveal đã hứa.
4. Sửa `_TTS.md` video đã render → xoá cache voice, render lại voice + video.
5. Quét compliance theo `youtube-compliance.md`.

## 2. CÂU CANONICAL

### 2.1 nenkin — 年金と老後のお金研究室
```
ここで、ひとつだけお願いです。今日の内容が分かりやすいと感じていただけたら、高評価と、同じように年金が気になるご家族やご友人へのシェアで、この研究室を応援していただけると嬉しいです。ご感想や、調べてほしいテーマがあれば、ぜひコメントでお寄せください。皆さまの声が、次の研究テーマになります。それでは、続きを見ていきましょう。
```

### 2.2 showa — 昭和くらし図鑑
```
ここで、ひとつだけお願いです。今日の献立が懐かしいと感じていただけたら、高評価と、同じ時代を過ごしたご家族やお友達へのシェアで、この図鑑を応援していただけると嬉しいです。あなたの学校の給食の思い出も、ぜひコメントで聞かせてください。皆さまの思い出が、次のページになります。それでは、続きをめくっていきましょう。
```
ⓘ 「あなたの学校の給食の思い出も」 là bản video #1 — video khác thay cụm chủ đề (「あなたの家の◯◯の思い出も」), giữ nguyên phần còn lại. Chữ ký kênh = 「次のページ」「めくっていきましょう」.

## 3. ĐIỂM CHÈN ~50%
| Kênh | Điểm chèn |
|---|---|
| **nenkin** | Ngay sau khối **case tính thử tiền** (~50%), trước phần 「hiểu lầm thường gặp」. |
| **showa** | Ngay sau khối **trả đáp án đố giá** (~50%), trước khi sang nửa sau. |

## 4. VIDEO ĐÃ CÓ
Mặc định KHÔNG tự re-render. Khi user chỉ định: chèn dòng canonical vào `_TTS.md` → xoá cache voice → render lại voice + video.

## 5. OVERLAY HÌNH + TIẾNG
Card glass góc dưới-trái: 高評価/シェア/コメント được "bấm" lần lượt + nút チャンネル登録 đỏ, kèm whoosh/pop/chime.
Tool (`Projects/youtube-jp-chouhen/tools/`, standalone): `gen_cta_overlay.py` · `gen_cta_sfx.py` · `cta_inject.py` (tìm câu CTA trong `subs.srt`, chỉ re-encode đoạn quanh CTA; không thấy → exit 2).

| Kênh | Đường render | Overlay |
|---|---|---|
| **nenkin** | Remotion | ⛔ **BỎ `cta_inject`** — hỏng ở đường Remotion (mất lớp ảnh, overlay không hiện; `render-background.md` §2.6 ⑧). Câu CTA vẫn còn trong giọng đọc. Muốn overlay → vẽ trong `project.json` (việc còn mở). |
| **showa** | `youtube-jp-health/tools/video_render.py` (nếu đi đường này) | tự chạy `cta_inject` ở bước cuối (`--lang jp`), tắt bằng `--no-cta`. Đi đường khác thì chạy tay: `python E:\Claude\Projects\youtube-jp-chouhen\tools\cta_inject.py <video.mp4> --srt <subs.srt> --lang jp --in-place` |

⛔ Đừng tin `CTA_EXIT=0` — trích frame trong cửa sổ re-encode mà tool in ra để kiểm.
