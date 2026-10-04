# KHÁM KÊNH 60代からの食卓 — 2026-08-11 · RETENTION + mục tiêu AVD 60%

> Phép đo: YouTube Analytics API (token readonly shokutaku, scope `yt-analytics.readonly`), 14 video đã đăng 07-06 → 08-10.
> `subs.srt` của 3 video có curve **thu hồi từ chính YouTube** (`captions.download`) vì script gốc đã mất — lưu ở `06_VIDEO/_diagnose/<videoId>.srt`.
> ⚠️ `impressions`/CTR vẫn bị Google rút khỏi API (từ 2026-07-30) → muốn số đó phải đọc tay Studio.
> Bổ sung, KHÔNG đè: `CHANNEL_OPTIMIZE.md` (07-21) và 2 khối khám kênh trong `CLAUDE.md` (08-01, 08-09) vẫn đúng về `BROWSE=0`, về metadata, về chuyện ngách không chết. File này chỉ nói về **retention**.

---

## 0. SỐ HIỆN TRẠNG

- **14 video / 36 ngày → 72 view · 1 sub · 256 phút xem.**
- **AVD kênh 3′53″ = AVD% 17,0%** trên video dài 14–35′.
- `BROWSE_FEATURES = 0` tuyệt đối (đã ghi 08-09). Retention **không** mở được vòi — đọc kết quả bằng `relPerf`, không bằng view.

**AVD từng video** (`averageViewPercentage`, xếp theo view):

| video | dài | view | AVD | AVD% |
|---|---|---|---|---|
| ゆで卵 | 14′45 | **24** | 4′02 | **27,4%** |
| 納豆 | 28′58 | **11** | 3′31 | 12,2% |
| ブルーベリー | 20′28 | **10** | 2′42 | 13,3% |
| 腎臓 | 35′07 | 8 | 4′35 | 13,1% |
| 牛乳 | 30′52 | 3 | 3′11 | 10,3% |
| あずき | 27′21 | 2 | 2′16 | 8,3% |
| 緑茶 | 14′22 | 2 | 7′24 | 51,6% ⚠️ n=2 |
| トマト | 16′50 | 1 | 1′00 | 6,0% ⚠️ n=1 |
| 豆腐 | 24′24 | 1 | 0′38 | 2,6% ⚠️ n=1 |
| キャベツ/麦茶/ヨーグルト/はちみつ/味噌汁 | 20–29′ | **0** | — | — |

⚠️ **Chỉ 3 video (ゆで卵 · 納豆 · ブルーベリー) đủ mẫu để API trả đường cong.** Video ≤3 view là nhiễu, không phải phép đo (緑茶 51,6% từ **2** view — đừng đem khoe).

🔴 **Và cả 3 đều là script CŨ** (07-06, 07-09, 07-17 — viết TRƯỚC gate `check_coldopen.py` ngày 08-01). **5 video chạy spec hiện hành có 0–6 view ⇒ spec đang dùng CHƯA TỪNG được đo.** Mọi kết luận dưới đây là về script cũ; phần áp cho spec mới là suy luận, ghi rõ ở §5.

---

## 1. CỬA TỬ LÀ GIÂY 20 → 40

`audienceWatchRatio` + `relativeRetentionPerformance` theo `elapsedVideoTimeRatio`:

| video | @9–17s | @25–27s | @35–37s | @52–62s | sàn thân bài | relPerf 60s đầu |
|---|---|---|---|---|---|---|
| ゆで卵 14′45 | 95,8% | 58,3% | **50,0%** | 41,7% | 20,8% | 0,48 → 0,29 |
| 納豆 28′58 | **100%** | 45,5% | 45,5% | 36,4% | 9,1% | 0,22 → **0,08** |
| ブルーベリー 20′28 | 100% | 80,0% | **30,0%** | 30,0% | 10,0% | 0,20 → **0,06** |

🔴 **Cả 3 mất 45–55 điểm trong 12–18 GIÂY, đều rơi vào cửa sổ 20–40s** — nhiều hơn cả 20 phút còn lại cộng lại.
⭐ **Gần như không ai bỏ đi trong 17 giây đầu (95,8–100%)** ⇒ hook mở đang chạy được, **đừng đảo nó**.
⚠️ `relPerf` 0,06–0,29 = phân vị đáy 6–29% của YouTube ở 60 giây đầu.

🟢 **Đuôi bài KHÔNG hỏng.** Từ phút ~6 curve đi **phẳng tuyệt đối** tới hết (ゆで卵 giữ 20,8% từ 5′57 → 13′16; ブルーベリー giữ 30,0% từ 0′35 → 19′26). Ai sống qua phút 6 thì xem tới cuối. Vấn đề là chỗ RÒ, không phải "bài chán".

---

## 2. 🔴 THỦ PHẠM ĐO ĐƯỢC: **CÂU TỰ THÁO NGÒI LỜI HỨA**

Ghép `subs.srt` (giây thật) với curve, cú rớt lớn nhất của từng video rơi đúng vào **một câu**:

| video | giây | câu đang đọc | rớt |
|---|---|---|---|
| **納豆** | 23 → 27 | 「と言っても、**納豆が悪者になったという話ではないのです**」 | **−55 điểm** |
| **ブルーベリー** | 27 → 35 | 「**悪いのはブルーベリーではありません。**高い品でも少ない量でもない」 | **−50 điểm** |
| **ゆで卵** | 21 → 25 | 「**にわかには信じがたいかもしれませんけれど**、これは多くの方が…」 | **−38 điểm** |

**Cơ chế:** thumbnail/title buộc tội món X. Người xem bấm vào để biết X có sao không. Trong giây 20–40 script **tự gỡ lời buộc tội đó** → lý do ở lại biến mất → tắt.

### 2.1 Hai loại câu phủ định — phải phân biệt, đừng cấm nhầm

| | THÁO NGÒI (giết) | PIVOT (không giết) |
|---|---|---|
| phủ định cái gì | **chính chủ thể của title/thumbnail** | một mồi nhử phụ |
| thay bằng gì | **khái niệm trừu tượng** 「組み合わせです」「食べ方なのです」 | **tổn thương cụ thể trên thân thể** |
| ví dụ | 納豆 −55 · ブルーベリー −50 · `09_hachimitsu` 0′50 「やめましょう、というお話ではありません」 | `12_tofu` 0′08 「目や耳の話ではありません」→「足の筋肉が、少しずつ、減っている」 |

⚠️ Giả thuyết "thay ngay bằng đáp án mới thì cứu được" **KHÔNG đứng**: cả 納豆 lẫn ブルーベリー đều thay trong 7–9 giây (「組み合わせ」/「食べ方」) mà vẫn rớt 50–55. Cái cứu được phải **cụ thể** (vật · con số · tổn thương thân thể), không phải một khái niệm.

### 2.2 Thủ phạm phụ: KHỐI CREDENTIAL

ゆで卵 rớt tiếp **−8 điểm ở giây 33** đúng câu 「**私はこれまで長い間、ご高齢の方の食事と体についてお話をしてきました**」. ブルーベリー có đúng câu đó ở giây 59.
→ Vừa giết retention, vừa **vi phạm luật persona みのり** (`CLAUDE.md` §Persona: cấm tự xưng chuyên gia) và trùng đúng thứ health đã cấm từ 07-27 (*"bỏ hẳn đoạn credential 「私はこれまで長い間…」 — kênh faceless 0 sub, 30s chết"*).

### 2.3 ⭐ GIẢ THUYẾT CŨ BỊ BÁC — chuỗi 「〜ませんか」 KHÔNG phải thủ phạm

Trước khi thu srt, giả thuyết đang chạy là *"gate luật L5 bắt ≥3 câu 「〜ませんか」 riêng lẻ, chúng chiếm đúng cửa tử"*. **Sai.**
- ゆで卵 giây 21 đọc đúng 「少し気になりませんか?」 → **giữ 95,8%**, không rớt.
- Cú rớt đến ở câu KẾ TIẾP, là câu meta 「にわかには信じがたい…」.

⇒ **KHÔNG bỏ luật L5.** Câu triệu chứng không tốn máu; câu meta/tháo ngòi mới tốn.
📌 Bài học quy trình: giả thuyết này khớp về **vị trí** (18–43s) nên trông rất thuyết phục, và suýt được viết thẳng vào spec. Nó chỉ chết khi ghép với **giây thật của srt**. Giống hệt §4a của `co-dai/CHANNEL_DIAGNOSIS_2026-08-11.md`: *gate/giả thuyết chưa hiệu chuẩn thì chưa được tin.*

### 2.4 Vùng rò thứ hai: phút 1′40 → 6′00, RÒ ĐỀU, không có vách

ゆで卵 (n=24, mỗi khán giả ≈ 4,2 điểm): 41,7% @1′40 → 37,5% @2′42 → 33,3% @3′28 → 29,2% @4′51 → 25,0% @5′34 → 20,8% @5′57.
**Mất ~1 người mỗi 20–40 giây, không cú rớt nào ≥8 điểm.** Nội dung vùng đó: hướng dẫn luộc (7分半) · 血圧 · ビタミンC · anecdote 青木さん @4′51 · câu hedge 「もたらす可能性があると考えられています」 @5′57.
⇒ Không quy được cho MỘT khối nào. Đây là rò do **mật độ trả tiền thấp**, chữa bằng luật sàn (§4), không bằng cách xoá một khối.
⚠️ 納豆 (n=11) nhảy 9,1 ↔ 27,3% liên tục = 1 người → **không đọc được**, đừng diễn giải.

---

## 3. CẮT NGẮN **KHÔNG** MUA ĐƯỢC 60% — và còn hại AVD phút

Tích phân hình thang trên curve thật (giả định giữ nguyên hình dạng):

| cắt tại | ゆで卵 | 納豆 | ブルーベリー |
|---|---|---|---|
| 5′ | **43,5%** | 30,4% | 27,4% |
| 8′ | 35,5% | 25,3% | 21,9% |
| 10′ | 32,5% | 24,1% | 19,5% |
| 12′ | 30,6% | 23,6% | 17,9% |
| 14–16′ | 29,1% | 21,9% | 16,8% |
| nguyên bản | 28,3% | 15,7% | 14,7% |

🔴 **Cắt xuống 5 PHÚT vẫn chỉ 43,5%.** Vì `AVD% ≈ chiều cao TRUNG BÌNH của curve`, mà cái vách ở giây 20–40 kéo **mọi** cửa sổ bắt đầu từ 0 xuống.

⚠️ **Cắt ngắn còn đi NGƯỢC mục tiêu "AVD phút phải tăng":** 納豆 cắt 29′ → 15′ thì AVD% 15,7% → 21,9% nhưng **AVD phút tụt 4′33 → 3′11**. `AVD phút = AVD% × độ dài` — cắt chỉ có lãi SAU khi curve đã lên.

**Chiều thứ hai, độc lập:** benchmark ngách (`youtube-jp-health/CHANNEL_DIAGNOSIS_2026-08-03.md`) = 高齢者健康の真実 median **37′** vẫn ăn view ⇒ ngách này không thưởng video ngắn.

⇒ ⭐⭐ **60% mua TRỌN trong 40 giây đầu + sàn thân bài. GIỮ 21–25′** (user chốt 2026-08-11). Bật lại chuyện cắt khi @40s đã ≥70%.

---

## 4. HAI CON SỐ PHẢI ĐẠT

1. **@40s ≥ 85%** — nay 30,0 / 45,5 / 50,0%. Đắt nhất, ăn phần lớn số điểm AVD.
2. **Sàn thân bài ≥ 55%** — nay 9,1 / 10,0 / 20,8%.

⚠️ **60% chưa có tiền lệ trong workspace.** Cao nhất từng đo: chouhen video 12 **51,6% lifetime**, và đó là **drama** (lực kéo tự truyện). Kênh thông tin không có lực đó.
**Mốc chặng: 30% → 40% → 50% → 60%.**
🛑 **Phanh: 3 video liên tiếp ≤25% AVD% ⇒ mốc 60% sai với ngách này — mổ lại, đừng vá tiếp.**

⚠️ Ràng buộc song song **không bị hoãn**: `CLAUDE.md` §Việc 3 vẫn giữ mốc *8 video qua gate mà `BROWSE` vẫn 0 → dừng, mở kênh mới* (~2026-08-25). Kế hoạch này chỉ đổi RUỘT của 4 video còn lại.

---

## 5. ⚠️ GIỚI HẠN CỦA PHÉP ĐO — đọc trước khi trích dẫn

1. **Cỡ mẫu 72 view toàn kênh.** ゆで卵 n=24 (1 người = 4,2 điểm) · 納豆 n=11 (9,1 điểm) · ブルーベリー n=10 (10 điểm). Cú rớt −55 của 納豆 = **6 người**. **Mức** số là nhiễu; **hình dạng** thì 3/3 giống nhau nên đủ để hành động.
2. **3 video đo được đều là script CŨ.** Spec hiện hành (5 video) chưa có curve nào.
3. **Luật §2 suy từ 3 điểm dữ liệu.** Nó khớp cả 3 và có cơ chế giải thích được, nhưng chưa phải nhân quả đã chứng minh. Video 14 là phép thử.
4. **Traffic không sạch:** nguồn view là SUBSCRIBER/YT_CHANNEL/NO_LINK/EXT, **không** phải người tự chọn từ feed. Retention của khán giả browse thật có thể khác.
5. **Sửa retention KHÔNG mở vòi.** `BROWSE = 0`; CTR/thumbnail vẫn là cửa vào và lượt này cố ý không đụng.

---

## 6. LỆNH ĐO LẠI

```bash
# AVD + curve 1 video
cd E:\Claude\Projects\youtube-jp-chouhen\tools
python analytics_report.py --channel shokutaku --video <videoId>

# gate script trước render
cd E:\Claude\Projects\youtube-jp-shokutaku
python tools\check_coldopen.py <NN>
python tools\check_coldopen.py --calib     # hiệu chuẩn lại trên video đã lên sóng
```

Channel ID: `UCj_QueccfLclCHR5_0vys1Q` · 3 video hiệu chuẩn: `mQevRS1qBbk` (ゆで卵 27,4%) · `31KXwgHbLY0` (ブルーベリー 13,3%) · `BL7KtdXpl_A` (納豆 12,2%) · srt ở `06_VIDEO/_diagnose/`.
