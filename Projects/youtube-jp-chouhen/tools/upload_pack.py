# -*- coding: utf-8 -*-
"""
upload_pack.py — đóng gói bán tự động 1 video thành "gói upload" YouTube.

Gom mọi thứ cần cho 1 lần upload vào 06_VIDEO/<slug>/_upload/:
  - <ten-file-seo>.mp4   (hardlink từ bản render, đã rename theo slug keyword)
  - subs.srt             (upload tay, không dùng auto-caption)
  - thumbnail.png
  - METADATA.txt         (title / description / tags copy-paste + giờ hẹn đăng + checklist)

Nguồn metadata: mục "Đóng gói CTR" trong 03_SCRIPTS/<slug>.md (title CHỐT, tên file,
3 dòng đầu 概要欄, mô tả đầy đủ, タグ). Giờ hẹn tính theo .claude/rules/upload-schedule.md.

Dùng:
  python tools/upload_pack.py 07_amamidokoro-saikaihatsu
  python tools/upload_pack.py <slug> --channel chouhen --slot "2026-07-19 18:00" --open --force

Standalone — kênh khác gọi bằng đường dẫn tuyệt đối + --channel <key> (config CHANNELS dưới).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import webbrowser
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECTS_ROOT = Path(r"E:\Claude\Projects")

# Mapping kênh -> Chrome profile (nguồn sự thật: .claude/rules/channel-browser.md)
BROWSER_PROFILES = PROJECTS_ROOT / "yt-dashboard" / "browser_profiles.json"


def open_studio(channel: str):
    """Mở YouTube Studio bằng đúng Chrome profile của kênh; thiếu mapping/Chrome → browser mặc định."""
    try:
        cfg = json.loads(BROWSER_PROFILES.read_text(encoding="utf-8"))
        prof = cfg["profiles"][channel]["profile_dir"]
        chrome = cfg.get("chrome_exe", "")
        if not Path(chrome).exists():
            raise FileNotFoundError(chrome)
        subprocess.Popen([chrome, f"--profile-directory={prof}", "https://studio.youtube.com"])
        print(f"→ Studio mở bằng Chrome profile riêng của kênh: {prof}")
    except (OSError, KeyError, json.JSONDecodeError) as e:
        print(f"⚠️ Không mở được profile riêng ({e!r}) — dùng browser mặc định.")
        webbrowser.open("https://studio.youtube.com")

# Lịch theo .claude/rules/upload-schedule.md (chốt 2026-07-18).
# slots = list (weekday, giờ địa phương) HOẶC (weekday, giờ, phút) khi giờ đăng lẻ phút
# (vd shokutaku 17:30). Weekday: Mon=0 .. Sun=6. tz = UTC offset giờ.
# ⚠️ Mọi nơi đọc slots phải đi qua slot_hm() (ngay dưới dict) — đừng unpack `for wd, hour in ...`,
# tuple 3 phần tử sẽ nổ ValueError.
#
# ⭐⭐ ĐỔI TOÀN BỘ NHỊP 2026-08-03 (user chốt: "2 ngày 1 video cho tất cả các kênh, kênh nào
#    đang được đề xuất thì 1 ngày 1 video. Tao cần sự đều đặn"):
#    · **Kênh ĐANG ĐƯỢC ĐỀ XUẤT → 1 video/NGÀY (7/tuần).** Hiện chỉ **chouhen** (kênh duy nhất
#      ĐO ĐƯỢC rail mở: video 07-25 ăn 227 view với 95/97 view từ RELATED_VIDEO).
#    · **Mọi kênh còn lại → 2 ngày 1 video = 3 slot/tuần, THỨ CỐ ĐỊNH.** 7 không chia hết cho 2,
#      nên cách làm tròn đã chọn là "3 thứ cố định tuần nào cũng vậy" (khoảng cách 2-2-3 ngày) —
#      user ưu tiên ĐỀU ĐẶN/đoán được hơn là đúng 48h tuyệt đối (phương án xoay thứ theo tuần
#      đã cân nhắc và LOẠI vì khán giả không đoán được ngày).
#    · Hai bộ ngày SO LE để không dồn 5 video vào cùng một ngày sản xuất:
#         bộ A = T2·T4·T6 → co-dai (11:00) · shokutaku (12:00) · health (19:00)
#         bộ B = T3·T5·CN → nagaiki (19:00) · nenkin (19:00)
#      health ↔ nagaiki cùng tệp senior JP nên CỐ Ý đặt khác bộ ngày.
#    · GIỜ của mọi kênh GIỮ NGUYÊN (mỗi kênh 1 giờ cố định, căn cứ đo publishedAt đối thủ
#      2026-07-28 vẫn còn hiệu lực) — lượt này chỉ đổi NGÀY + SỐ LƯỢNG.
#    · Tải mới: 7 + 5×3 = **22 video/tuần** (trước đó 13). ⚠️ Đây là ràng buộc NĂNG LỰC, không
#      phải ràng buộc lịch: slot trống mà không có hàng qua gate thì BỎ SLOT, không đăng bù.
#    · ⚠️ Ghi để đọc số sau này KHÔNG bị lẫn: phép đo 2026-07-28/30 nói volume KHÔNG mở được
#      vòi ở cụm senior/tiền (co-dai · shokutaku · nenkin · health đều BROWSE=0), và health đang
#      bị đóng vòi cấp kênh từ 07-20. User biết và vẫn chọn nhịp đều 3/tuần cho cả 6 kênh.
#      Phanh nên dùng: 3 video liên tiếp <50 view HOẶC AVD tụt → hạ kênh đó về 1/tuần.
CHANNELS = {
    "chouhen": {
        "name": "真夜中の朗読便",
        "channel_id": "UCuzbgcFHVmAf4O6wU1wLyIQ",  # upload_api verify token đúng kênh; kênh khác: điền sau lần auth đầu
        "project": "youtube-jp-chouhen",
        # ⭐⭐ 4 VIDEO/TUẦN — T2·T4·T6·CN 09:00 JST (user chốt 2026-08-14: "giãn cách ra", chọn bộ ngày
        #   này). HẠ TỪ 7/tuần (1 video/ngày, chốt 2026-08-03). Giãn 2-2-2-1 ngày — cách đều nhất
        #   mà 4 slot làm được trong 7 ngày. Giờ 09:00 GIỮ NGUYÊN (đo thật benchmark 苦しみの物語,
        #   khán giả スカッと nghe buổi sáng).
        #   ✅ Giữ T2 = ngày mạnh ở CẢ HAI kênh đối thủ (嫁子 median 46,5K cao nhất bảng; 苦しみ hạng nhì).
        #   ✅ Bỏ T7 = ngày median BÉT của 苦しみ (4,6K).
        #   ⚠️ NHƯNG LẤY CN — ngày median bét của 嫁子 (23,7K = NỬA T2). Đây là đánh đổi có ý thức:
        #      4 ngày cách đều trong 7 ngày thì buộc phải chạm cuối tuần. Nếu muốn né cả T7 lẫn CN
        #      thì chỉ còn 3/tuần T2·T4·T6.
        #
        #   ⚠️ CÁI MẤT, biết trước: chouhen là kênh DUY NHẤT có rail đề xuất mở
        #   (CHANNEL_DIAGNOSIS_2026-07-28.md: video 07-25 ăn 227 view với 95/97 từ RELATED_VIDEO)
        #   và ngách này volume THẮNG (嫁子 233K sub = 8,75 video/tuần). Cắt 7→4 = mất 43% số vé/tuần,
        #   đúng lúc CHANNEL_DIAGNOSIS_2026-08-12 kết luận nút thắt là BAO BÌ + SỐ VÉ. Đánh đổi đã
        #   chọn: 4 video làm tử tế hơn 7 video làm vội — gate NĂNG LỰC (không có hàng qua gate thì
        #   BỎ SLOT) vốn đã phải thi hành bằng tay từ khi xoá _chouhen_slots().
        #   🛑 PHANH: trung vị view/video của 10 video kế TỤT so với lô 7/tuần trước đó → trả về
        #      7/tuần [(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9)]. Ghi vào 08_ANALYTICS_LOG.md.
        "slots": [],  # T2*T4*T6*CN 12:00 JST (= 10:00 VN). DO DUOC 2026-08-26 (measure_upload_hours.py): winner nganh 嫁子 (233K) khoa 12h o 41/50 video va 12h thang chinh 18h cua no 1,65x voi TUOI VIDEO KHOP (21d=21d) = phep so dang tin nhat ca bo. 3/3 phep so sach tuoi trong nganh deu noi sang-trua > 18h. Gio cu: 09:00 (xep 9/10 nganh) -> 17:00 (n=4, 1 kenh, co co recency) -> 12:00.  # TAM DUNG 2026-09-24 (chi lam nenkin+showa). Bat lai: [(0, 12), (2, 12), (4, 12), (6, 12)]
        "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "playlist": "スカッとする話・長編朗読",
        "checklist": [
            "Phụ đề: upload subs.srt thủ công (KHÔNG dùng auto-caption)",
            "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm",
            "Đối tượng: không dành cho trẻ em (made for kids = NO)",
            "Kiểm 概要欄 có disclaimer フィクション + credit giọng ĐÚNG VOICE ARM "
            "(A → AivisSpeech:morioki · B → VOICEVOX:青山龍星) + BGM",
        ],
    },
    "shokutaku": {
        "name": "60代からの食卓", "channel_id": "UCj_QueccfLclCHR5_0vys1Q", "project": "youtube-jp-shokutaku",
        # ⚠️ REBRAND 2026-09-30 -> 他人の目を気にしない心理学 (key `kinishinai`). Key nay giu cho tool cu; dung `kinishinai` cho video moi.
        # ⭐ BẬT LẠI + ĐỔI NHỊP 2026-07-30 (user chốt): 1 video/NGÀY, **12:00 JST** cố định cả 7 ngày.
        #    Giờ: 19:00 → 17:30 → 12:00 trong cùng ngày. Ý đồ user: TÁCH DAYPART giữa 2 kênh cùng tệp
        #    senior JP — health giữ TỐI 19:00, shokutaku sang TRƯA. 12:00 = khung nghỉ trưa 12–13h
        #    (SocialPilot: 12–15h là khung ăn nhì, 22%), không đụng co-dai 11:00 JST.
        #    Tiền lệ noon gần nhất trong ngách: ご長寿ご健康 đăng 13:00 × 42 video ở nhịp 7,14/tuần
        #    (median T6 27,7K) — muốn bám sát tiền lệ đó thì đổi 12 → 13.
        #    Lịch trước đó: T2·T3·CN 19:00 (3/tuần) — đo 50 video 長生きの秘訣: median view T2 81,8K
        #    > T3 42,7K > CN 32,1K, T4 3,2K + T6 5,5K là 2 ngày bét.
        #    ⚠️ Ghi để không quên khi đọc số sau này: đo ngách 2026-07-28 nói volume THUA ở đây
        #    (長生きの秘訣 3,4 video/tuần → sụp 45×; 若返りアカデミア 0,25/tuần → median 141K view).
        #    User biết và vẫn chọn 1/ngày. Phanh nên dùng: 3 video liên tiếp <50 view hoặc AVD tụt
        #    → hạ về 3/tuần T2·T3·CN.
        #    ⭐ HẠ NHỊP 2026-08-01 (user chốt): 7/tuần → **3/tuần T2·T3·CN**, GIỮ 12:00 JST.
        #    Lý do đo được, không phải cảm tính: nguồn traffic 9 video cả tháng 7 =
        #    BROWSE 0 · SEARCH 1 · SUGGESTED 11 → vòi CHƯA TỪNG mở, nên thêm video chỉ
        #    thêm mẫu retention xấu vào điểm kênh (bài học health). Cộng với năng lực:
        #    7 slot/tuần = 7 video render+đóng gói/tuần, tồn kho thực tế ~0 script sẵn sàng.
        #    Chọn T2·T3·CN theo median view 長生きの秘訣 (đo 50 video 2026-07-28):
        #    T2 81,8K > T3 42,7K > CN 32,1K; T4 3,2K + T6 5,5K là 2 ngày bét.
        #    Tăng lại chỉ khi BROWSE_FEATURES > 0 lần đầu (điều kiện ghi ở CLAUDE.md kênh).
        #    ⭐ ĐỔI NGÀY 2026-08-03 (nhịp 2 ngày/video toàn hệ thống): T2·T3·CN → **T2·T4·T6**,
        #    3/tuần GIỮ NGUYÊN, giờ 12:00 GIỮ NGUYÊN. T2·T3 sát nhau (cách 1 ngày) rồi nghỉ 4 ngày
        #    = không phải "2 ngày 1 video"; T2·T4·T6 giãn đều 2-2-3. Đánh đổi biết trước: T4 và T6
        #    là 2 ngày median view BÉT của benchmark 長生きの秘訣 (3,2K và 5,5K) — nhưng kênh này
        #    BROWSE=0 nên số median-theo-ngày của đối thủ chưa có tác dụng gì ở đây, đều đặn
        #    quan trọng hơn. Ngày mạnh nhất T2 vẫn giữ → dồn video mạnh nhất vào T2.
        "slots": [],  # T2*T4*T6 17:00 JST (= 15:00 VN). DO DUOC 2026-08-26: 17h thang 19h 16x TRONG CUNG kenh 健康長寿の知恵袋TV, va tuoi video chay NGUOC (33d vs 12d) nen ket luan cang chac; aggregate nganh 17h #1 (n=29, 3 kenh) va 19h BET (26 v/d); top nganh 若返りアカデミア khoa 17h o 18/18 video. Gio cu 12:00 -> 19:00 (bet nganh) -> 17:00.  # TAM DUNG 2026-09-24 (chi lam nenkin+showa). Bat lai: [(0, 17), (2, 17), (4, 17)]
        "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm", "made for kids = NO",
                      "概要欄 có miễn trừ y tế + credit giọng VOICEVOX/BGM/ảnh"],
    },
    "health": {
        "name": "health (JP senior)", "channel_id": "UCnoYb7aEKy1NgspYTKwhh1Q", "project": "youtube-jp-health",
        # ⚠️ REBRAND 2026-09-30 -> 定年後のこころ研究室 (key `teinengo`). Key nay giu cho tool cu; dung `teinengo` cho video moi.
        # ⭐⭐ NHỊP + NGÀY SỬA 2026-08-03 (user chốt "2 ngày 1 video cho tất cả các kênh"):
        #   1/tuần T5 → **3/tuần 19:00 JST** (ngày chốt sau 2 lần sửa trong ngày: **T3·T5·CN**,
        #   xem khối ⚠️ NGÀY SỬA LẦN 2 dưới). Giờ 19:00 GIỮ NGUYÊN.
        #   ⚠️ ĐÂY LÀ QUYẾT ĐỊNH CỦA USER, NGƯỢC VỚI 2 THỨ ĐÃ ĐO — ghi thẳng để sau đọc số không lẫn:
        #     ① health BỊ ĐÓNG VÒI cấp kênh từ 2026-07-20 (impressions/video 5.500 → 1;
        #        relativeRetentionPerformance@60s 0,10–0,14 = đáy phân vị 10–20% của YouTube).
        #     ② Kênh đã bị ĐÓNG BĂNG 2026-08-01 (CHANNEL_DIAGNOSIS_2026-08-01.md) và mở kênh brand
        #        MỚI `nagaiki` thay thế — video 22 chỉ được phát 3 impressions.
        #   Hệ quả cần theo: mỗi video đăng vào kênh đang tắt vòi = thêm 1 mẫu retention đáy vào
        #   điểm trung bình kênh. Phanh: 3 video liên tiếp 0 view organic → trả về [(3, 19)] 1/tuần.
        #   ⚠️ NGÀY SỬA LẦN 2 trong cùng ngày 2026-08-03: T2·T4·T6 → **T3·T5·CN** (bộ B), sau khi
        #   nagaiki bị BỎ khỏi lịch. Lý do: nagaiki rời đi để lại bộ B chỉ còn nenkin ⇒ tải lệch
        #   4 video ở T2/T4/T6 vs 2 ở T3/T5/CN. Dời health sang B thì cân đều **3 video mỗi ngày**
        #   (trừ T7 = 1 của chouhen) — đúng ý "đều đặn" ở cả tầng NGÀY SẢN XUẤT, không chỉ tầng
        #   nhịp từng kênh. Việc tách health khỏi shokutaku (cùng tệp senior JP) vẫn đạt vì 2 kênh
        #   đã lệch GIỜ: health 19:00 vs shokutaku 12:00 (daypart tách từ 2026-07-30) — không cần
        #   tách thêm bằng ngày. Giờ 19:00 GIỮ NGUYÊN.
        #   ⚠️ Nếu bao giờ BẬT LẠI nagaiki: nó cũng nằm ở bộ B + cùng Gmail saubeooo04/Profile 13
        #   ⇒ phải hạ health cùng lúc, đừng để 2 kênh cùng nhà cùng tệp đăng chung ngày+giờ.
        #   (Lịch cũ T5 1/tuần — NGÀY chốt 2026-07-28: benchmark long-form DUY NHẤT còn thắng ngách (みんなの若返りアカデミア, median 141K view) khóa THỨ NĂM 17/18 video → dời T7 → T5. Giờ 19:00 giữ (số view-theo-ngày của 長生きの秘訣 KHÔNG dùng làm căn cứ: kênh đang sụp 45× nên median theo ngày lẫn hiệu ứng thời gian). Nhịp 1/tuần giữ nguyên (user chốt 2026-07-27 sau mổ lần 3: kênh BỊ TẮT VÒI từ 07-20, impressions 5.500→1. Đăng vào kênh đang tắt vòi = 0 view + thêm 1 mẫu retention đáy vào điểm trung bình kênh. 1/tuần = mỗi video 1 phép thử SẠCH, đủ thời gian đọc số. Giữ 19:00 + giữ T7 (đã có trong bộ cũ) để KHÔNG đổi thêm biến. Bằng chứng: Projects/youtube-jp-health/CHANNEL_DIAGNOSIS_2026-07-27.md)
        "slots": [],  # T3·T5·CN 19:00 JST (= 17:00 VN)  # TAM DUNG 2026-09-24 (chi lam nenkin+showa). Bat lai: [(1, 19), (3, 19), (6, 19)]
        "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm", "made for kids = NO",
                      "概要欄 có miễn trừ y tế + credit giọng VOICEVOX/BGM/ảnh"],
    },
    "nagaiki": {
        # ⭐ KÊNH MỚI 2026-08-01 (user chốt sau mổ lần 4 health — CHANNEL_DIAGNOSIS_2026-08-01.md):
        #    health bị đóng vòi cấp kênh 12 ngày, video 22 chỉ được phát 3 impressions → mở kênh
        #    brand MỚI cùng Gmail health (saubeooo04, Profile 13), chạy thẳng công thức 食べ合わせ
        #    (BENCHMARK_RIVALS_2026-07-29.md §7 — 健康栄養研究室 lập 07-20, 9 ngày = 45K view).
        #    CHỈ đăng nội dung CHƯA TỪNG public (video 28 + script 23-27 render mới) — cấm bê video cũ.
        #    Slot T5 19:00 JST kế thừa căn cứ health (若返りアカデミア khóa T5 17/18 video); 1/tuần khởi điểm.
        # ⭐⭐ NÂNG NHỊP 2026-08-03 (user chốt "2 ngày 1 video cho tất cả các kênh"):
        #    1/tuần T5 → **3/tuần T3·T5·CN 19:00 JST**. Giờ 19:00 GIỮ NGUYÊN, T5 (ngày có căn cứ
        #    đo được: 若返りアカデミア khóa T5 17/18 video) GIỮ trong bộ, thêm T3 + CN để giãn đều 2-2-3.
        #    Đặt ở bộ ngày B trong khi health ở bộ A là CỐ Ý — 2 kênh cùng tệp senior JP + cùng Gmail
        #    saubeooo04/Profile 13, không đăng chồng ngày.
        #    ⚠️ Kênh mới lập 2026-08-01, chưa có số phân phối nào → 3/tuần là phép thử nhịp, không
        #    phải kết luận. Cần đủ hàng CHƯA TỪNG public (cấm bê video health cũ sang — inauthentic §1).
        # ⏸⏸ BỎ KHỎI LỊCH ĐĂNG 2026-08-03 (user chốt: "kênh 長生きごはんの知恵袋 bỏ đi").
        #    Kênh này được mở 2026-08-01 để THAY health đang bị đóng vòi; nay user chọn ngược lại —
        #    **bật lại health (3/tuần T2·T4·T6) và bỏ nagaiki** → 2 việc này là MỘT quyết định,
        #    đừng bật lại nagaiki mà không xét lại health, nếu không thì 2 kênh cùng tệp senior JP
        #    + CÙNG Gmail saubeooo04/Profile 13 lại cùng đăng.
        #    Chưa có video nào lên sóng (06_VIDEO chỉ có 28_kuroyanagi-tetsuko chưa đăng) nên bỏ lịch
        #    KHÔNG để lại video mồ côi. Repo + credentials + channel_id GIỮ nguyên.
        #    Bật lại = trả slots về [(1, 19), (3, 19), (6, 19)] (T3·T5·CN) và hạ health tương ứng.
        "name": "長生きごはんの知恵袋", "channel_id": "UCBkpkLFZoj5gl4NzKmOC3zQ", "project": "youtube-jp-nagaiki",
        "slots": [], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm", "made for kids = NO",
                      "概要欄 có miễn trừ y tế + credit giọng VOICEVOX/BGM/ảnh"],
    },
    "co-dai": {
        "name": "古代の秘訣", "channel_id": "UCVlmm1sz7cvTIQ3uSaSct_w", "project": "youtube-jp-co-dai",
        # ⚠️ REBRAND 2026-09-30 -> 心の距離の心理学 (key `kyori`). Key nay giu cho tool cu; dung `kyori` cho video moi.
        # ⭐⭐ NÂNG NHỊP 2026-08-03 (user chốt "2 ngày 1 video cho tất cả các kênh"):
        #    2/tuần T2·T6 → **3/tuần T2·T4·T6 11:00 JST** (thêm T4). Giờ 11:00 GIỮ NGUYÊN.
        #    ⚠️ NGƯỢC với chẩn đoán 2026-07-30 (kênh vòi đóng, BROWSE/SUGGESTED = 0 tuyệt đối,
        #    8 video/15 ngày = 36 view) và T4 chính là ngày median view yếu của benchmark (6,2K).
        #    Giữ nguyên điều kiện gate NỘI DUNG: script phải PASS tools/check_coldopen.py (≤75s)
        #    trước khi render — không đủ hàng qua gate thì BỎ SLOT, không đăng bù.
        "slots": [], "tz": 9, "tz_name": "JST", "cta_lang": "jp",  # T2*T4*T6 13:00 JST — 3/tuan. DO DUOC 2026-08-26: 昔の人の知恵 (15,2K) co 13h 5.627 v/d (n=4) > 11h 1.188 (n=23) = 4,7x, va tuoi video chay NGUOC (37d vs 24d) nen khong phai artifact recency; 驚きの世界 co 11h > 19h 2,9x => trua/dau chieu thang toi o CA HAI kenh. 18h la diem BET nganh (5,5 v/d). ⚠️ n=4 nen mong — moc day nhat la 11h (n=27, 2 kenh); tut view thi ve 11:00. Gio cu 11:00 -> 18:00 (bet nganh) -> 13:00. (Lịch cũ: T2·T6 2/tuần PHÉP THỬ SẠCH. HẠ 2026-07-30 (user chốt sau KHÁM KÊNH — CHANNEL_DIAGNOSIS_2026-07-30.md): 8 video/15 ngày = 36 view, BROWSE/SUGGESTED = 0 tuyệt đối → vòi chưa từng mở; đăng 4/tuần vào kênh vòi đóng = thêm mẫu xấu (bài học health/nenkin). Giữ T2 (ngày mạnh nhất benchmark, median 231K) + T6; tăng lại ≥3/tuần KHI thấy view BROWSE đầu tiên + cold open đạt gate check_coldopen.py. Giờ 11:00 GIỮ NGUYÊN. (Lịch cũ 4/tuần: [(0,11),(3,11),(4,11),(5,11)] T2·T5·T6·T7 — chốt 2026-07-28 theo đo ngày đối thủ.)  # TAM DUNG 2026-09-24 (chi lam nenkin+showa). Bat lai: [(0, 13), (2, 13), (4, 13)]
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm", "made for kids = NO",
                      "概要欄 có credit giọng VOICEVOX/BGM/ảnh"],
    },
    "kyori": {
        "name": "心の距離の心理学", "channel_id": "UCVlmm1sz7cvTIQ3uSaSct_w", "project": "youtube-jp-kyori",
        # Rebrand co-dai 2026-09-30 (CUNG channelId, token youtube-jp-co-dai/credentials). Project: Projects/youtube-jp-kyori/CLAUDE.md.
        # LICH 2026-09-30: T2*T4*T7 19:00 JST - do 3 kenh 【心理学】 (79 video): 18h=38 19h=33; median hieu suat T7 x1,48 T4 x1,45 T6 x1,31 CN x1,07 T2 x1,05 T5 x0,44 T3 x0,33. Xem upload-schedule.md §1.2c.
        "slots": [(0, 19, 0), (2, 19, 0), (5, 19, 0)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered/synthetic: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (youtube-compliance §2.1)", "made for kids = NO",
                      "概要欄 có miễn trừ (không thay tư vấn chuyên môn) + nguồn 心理学 + credit giọng/BGM/ảnh"],
    },
    "teinengo": {
        "name": "定年後のこころ研究室", "channel_id": "UCnoYb7aEKy1NgspYTKwhh1Q", "project": "youtube-jp-teinengo",
        # Rebrand health 2026-09-30 (CUNG channelId). Project: Projects/youtube-jp-teinengo/CLAUDE.md.
        # ⚠️ Token youtube-jp-health/credentials KHONG thuoc kenh nay (mine=True rong) -> can auth lai truoc khi upload API.
        # LICH 2026-09-30: T4*T6*CN 18:30 JST - do 3 kenh 【心理学】 (79 video): 18h=38 19h=33; median hieu suat T7 x1,48 T4 x1,45 T6 x1,31 CN x1,07 T2 x1,05 T5 x0,44 T3 x0,33. Xem upload-schedule.md §1.2c.
        "slots": [(2, 18, 30), (4, 18, 30), (6, 18, 30)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered/synthetic: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (youtube-compliance §2.1)", "made for kids = NO",
                      "概要欄 có miễn trừ (không thay tư vấn chuyên môn; không nêu số tiền 年金) + nguồn 心理学 + credit giọng/BGM/ảnh"],
    },
    "kinishinai": {
        "name": "他人の目を気にしない心理学", "channel_id": "UCj_QueccfLclCHR5_0vys1Q", "project": "youtube-jp-kinishinai",
        # Rebrand shokutaku 2026-09-30 (CUNG channelId, token youtube-jp-shokutaku/credentials DUNG kenh). Project: Projects/youtube-jp-kinishinai/CLAUDE.md.
        # LICH 2026-09-30: T2*T5*T7 18:30 JST - do 3 kenh 【心理学】 (79 video): 18h=38 19h=33; median hieu suat T7 x1,48 T4 x1,45 T6 x1,31 CN x1,07 T2 x1,05 T5 x0,44 T3 x0,33. Xem upload-schedule.md §1.2c.
        "slots": [(0, 18, 30), (3, 18, 30), (5, 18, 30)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered/synthetic: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (youtube-compliance §2.1)", "made for kids = NO",
                      "概要欄 có miễn trừ (không thay tư vấn chuyên môn) + nguồn 心理学 + credit giọng/BGM/ảnh"],
    },
    "chikei": {
        "name": "地形と地名の日本史", "channel_id": "UCfXuolJMQ-3CMpmTeQVkwKA",
        "project": "youtube-jp-chikei",
        # ⭐ KÊNH MỚI 2026-09-16 — CHUYỂN ĐỔI từ `사우 오디오` (kr-romfan). channelId GIỮ
        #   NGUYÊN, không lập kênh mới: kênh cũ 0 sub / 3 video / 56 view nên chuyển đổi
        #   gần như không mất gì, mà được cái tuổi kênh + đã xác minh.
        #
        # LỊCH T3·T6·CN 20:00 JST — 3 slot/tuần (nhịp chuẩn toàn hệ thống, user chốt
        #   2026-08-03). Vì sao bộ ngày này và giờ này (đo 10 kênh ngách 2026-09-16,
        #   youtube-jp-chikei/00_CHANNEL_BIBLE.md §1):
        #   · NGÀY: T3+T6 là 2 ngày mạnh nhất của kênh mẫu gần format nhất
        #     (地図で読み解く歴史と経済ch, 32K sub/9 tháng: T4=12 và T6=12 video nhiều
        #     nhất, median view T6 3.212 > T3 3.120). Bộ 2-2-3 duy nhất chứa CẢ T3 lẫn T6
        #     là T3·T6·CN. Trùng hợp: đúng bằng bộ ngày cũ của kr-romfan.
        #   · GIỜ: 20:00 là mốc CÓ BẰNG CHỨNG ngách (わくわく地理マップ khoá 20:00 ở 7/7
        #     video; ジオトリ 20–21h dày nhất) VÀ là giờ duy nhất còn trống trong
        #     workspace — 12/13/17/18/19h đã có chủ. Không trùng (ngày, giờ) với kênh nào.
        #   🛑 PHANH (00_CHANNEL_BIBLE.md §4 P1): 5 video đầu median <300 view và
        #     BROWSE/SUGGESTED = 0 → hạ về 1/tuần [(4, 20)] (T6), bám nhịp kênh hiệu suất
        #     cao của ngách (東京限定雑学 0,24 video/tuần → median 87.748 view/video).
        #   ⚠️ Biết trước: ngách này NHỊP CAO → VIEW/VIDEO THẤP (3,1/tuần ⇒ 324–8.284
        #     view; 0,24–1,0/tuần ⇒ 13K–88K). 3 slot/tuần là chọn kỷ luật sản xuất, không
        #     phải chọn theo số đo ngách.
        "slots": [],  # TAM DUNG 2026-09-24 (chi lam nenkin+showa). Bat lai: [(1, 20), (4, 20), (6, 20)]
        "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": [
            "Phụ đề: upload subs.srt thủ công (KHÔNG auto-caption)",
            "Altered content: video CÓ ảnh AI realistic thì PHẢI TICK "
            "(youtube-compliance §2.1). Bản đồ 地理院 KHÔNG phải AI → không tick vì nó",
            "Đối tượng: không dành cho trẻ em (made for kids = NO)",
            "概要欄 PHẢI có khối 出典 国土地理院 (điều kiện license!) + câu miễn trừ "
            "「個別の土地の安全性を判断するものではありません」 + credit giọng VOICEVOX + BGM",
            "Quét 00_CHANNEL_BIBLE.md §5: không phán xét đất/người, không '住んではいけない'",
        ],
    },
    "kr-romfan": {
        "name": "사우 오디오 (ĐÃ CHUYỂN THÀNH chikei)", "channel_id": "UCfXuolJMQ-3CMpmTeQVkwKA",
        "project": "youtube-kr-romfan",
        # 🔴🔴 2026-09-16: KÊNH NÀY ĐÃ ĐƯỢC CHUYỂN THÀNH 地形と地名の日本史 (key "chikei",
        #    project youtube-jp-chikei). `channel_id` ở đây TRÙNG với entry "chikei" — đó là
        #    CÙNG MỘT KÊNH YouTube, không phải hai. Giữ entry này CHỈ để tra lịch sử; đừng
        #    bật `slots` lại, và đừng dùng nó để upload — gói sẽ đi nhầm registry (cta_lang
        #    kr, checklist kr) lên một kênh giờ là kênh Nhật.
        # ⏸ Trước đó: NGƯNG HOẠT ĐỘNG 2026-07-28. Lịch cũ T3·T6·CN 21:00 KST.
        "slots": [], "tz": 9, "tz_name": "KST", "cta_lang": "kr",  # T3·T6·CN 21:00 KST — 3/tuần. SỬA 2026-07-28 (đo 50 video/kênh): 민트 오디오북 (116K, cùng format long audio-drama, khóa 21:00 ở 50/50 video) chỉ đăng CN=36/50 + T3=14/50 → CN là ngày lõi của ngách, thay T7; 사연튜브 (447K) median T3 39,8K > T6 38,5K củng cố T3+T6. Giờ 21:00 GIỮ NGUYÊN.
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm",
                      "made for kids = NO", "概要欄 có credit giọng Azure TTS/BGM"],
    },
    "stickman": {
        "name": "stickman (VN)", "project": "youtube-stickman",
        "slots": [], "tz": 7, "tz_name": "ICT", "cta_lang": "vn",  # BỎ khỏi lịch (user chốt 2026-07-22 — pilot VN tạm dừng đăng; config giữ lại, muốn chạy lại thì đặt [(4,17),(5,17),(6,17)])
        "checklist": ["subs.srt thủ công", "Ảnh AI stickman doodle = không realistic → KHÔNG tick",
                      "made for kids = NO", "Mô tả có credit giọng edge-tts/BGM"],
    },
    "nenkin": {
        "name": "年金と老後のお金研究室", "channel_id": "UC3MOM94mNkKzlp-9Sxz91bA", "project": "youtube-jp-nenkin",
        # ⭐ CHỐT LẠI 2026-07-28 (SAU khi khám kênh — CHANNEL_DIAGNOSIS_2026-07-28.md):
        #   T6 19:00 JST, **1 video/tuần**. T3 là slot PHỤ có điều kiện (支給日 / tin chính sách nóng),
        #   KHÔNG lấp cho đủ số — muốn bật thì dùng --slot "YYYY-MM-DD 19:00".
        #   Lý do hạ 2/tuần → 1/tuần: winner ngách 完全攻略 (lập 21/03/2026 → 132K sub / 12 video)
        #   lúc ramp chạy ~1 video/tuần (7–12 ngày/video), hit 3,84M đến ở video #3 ngày thứ 13;
        #   và nenkin phải nâng độ dài 15,5′ → 25–40′ (chuẩn ngách median 26–37,5′) = gấp đôi công/video.
        #   Thực tế 4 video đầu đã đăng 3,5/tuần mà 0 browse/suggested → volume không mở được vòi.
        #   Vì sao T6 (không phải T2/T4 như lịch gốc): 完全攻略 4/12 video đăng T6 và 2 hit lớn nhất
        #   đều T6 (3,84M · 1,05M, median ngày T6 = 742K) · T2 = 0 video suốt đời kênh; 速報 (114K)
        #   median T4 4.876 = THẤP NHẤT. Cả cụm tiền-senior khóa T6 (節約看護師 48/50 video).
        #   ⚠️ 4 mẫu + 2 hit là đề tài mega-evergreen → TƯƠNG QUAN, không phải nhân quả.
        #   Giờ 19:00 GIỮ NGUYÊN, nhưng biết rõ giờ KHÔNG mở được vòi: winner đăng rải 03:32–23:42.
        # ⭐⭐ NÂNG NHỊP + ĐỔI NGÀY 2026-08-03 (user chốt "2 ngày 1 video cho tất cả các kênh"):
        #    1/tuần T6 → **3/tuần T3·T5·CN 19:00 JST**. Giờ 19:00 GIỮ NGUYÊN.
        #    ⚠️ ĐÁNH ĐỔI LỚN NHẤT CỦA LƯỢT NÀY, ghi rõ để sau không tưởng là bỏ sót: bộ ngày B
        #    (T3·T5·CN) **KHÔNG chứa T6** — mà T6 là ngày lõi ĐO ĐƯỢC của cả cụm tiền-senior JP
        #    (完全攻略 median T6 742K, 節約看護師 T6 48/50 video). T3 vẫn là ngày mạnh thứ hai của
        #    ngách (速報 median T3 119K = cao nhất kênh đó), CN chưa có căn cứ ngách.
        #    → Muốn ưu tiên T6 hơn nhịp đều thì đổi bộ này sang [(1,19),(4,19),(6,19)] (T3·T6·CN,
        #      giãn 2-2-3 vẫn đạt) — đây là phương án thay thế đúng luật, chưa áp vì user chọn bộ B.
        #    ⚠️ Ràng buộc CÔNG vẫn còn: chuẩn độ dài ngách 25–30′ = gấp đôi công/video so với 15,5′.
        #    Không qua FACT SHEET / Retention Audit / 2 thumbnail → BỎ SLOT.
        #    Rule 支給日 giữ nguyên: video 給付金/年金生活 đăng 1–3 ngày TRƯỚC ngày 15 tháng chẵn,
        #    ghi đè bằng --slot (mốc kế: trước 14/08).
        "slots": [(1, 19), (3, 19), (6, 19)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm",
                      "made for kids = NO",
                      "概要欄 có disclaimer 「◯年◯月時点の情報」+ không phải tư vấn cá nhân + credit VOICEVOX:雀松朱司",
                      "Video 給付金/年金生活: ưu tiên đăng 1–3 ngày TRƯỚC 支給日 (15 tháng chẵn) — dùng --slot ghi đè"],
    },
    "kaigo": {
        "name": "親の介護とお金ノート", "channel_id": "", "project": "youtube-jp-kaigo",
        # 19:00 JST — ĐÃ ĐO XÁC NHẬN 2026-07-25 (API): cả 4 kênh benchmark đăng 17:48–20:00 JST;
        # 節約看護師りょう (748K sub, hiệu suất/video cao nhất nhóm) khóa 19:00 ở 49/50 video.
        # ⭐ NHỊP + NGÀY SỬA 2026-07-28 (user chốt sau đo lại 50 video/kênh): T6·T3, 2/tuần cố định.
        #   · 節約看護師りょう: T6 = 48/50 video, nhịp 1,02/tuần, median 105.975 view/video → T6 là ngày lõi cả cụm tiền-senior JP.
        #   · みんなの給付金・補助金 (551K): long-form CHỈ đăng T3 (15) + T6 (16), median T6 19,2K > T3 13,3K → T3 là ngày thứ hai.
        #   · BỎ nhịp "1 video/NGÀY từ video #6" (user chốt 2026-07-26, nay đảo lại): không có tiền lệ thắng nào ở ngách này
        #     — あまおう đăng 1/ngày → 12 video mới nhất chỉ 1,3–32K view. Hàm _kaigo_slots() đã xoá theo.
        # ⏸ NGƯNG HOẠT ĐỘNG 2026-07-28 (user chốt: chỉ 4 kênh active = chouhen/co-dai/health/nenkin).
        #    Lịch cũ: T3·T6 19:00 — chờ Gmail kênh, bật lại bằng giá trị này
        "slots": [], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm",
                      "made for kids = NO",
                      "概要欄 có 「◯年◯月時点の情報」+「制度は市区町村によって異なります」+ không phải tư vấn cá nhân/pháp lý + credit giọng + イラスト:いらすとや",
                      "GATE 5 ĐIỂM đã pass (số cast trước phút 2 · ≥2 原典ショット · なぜ · hành động có địa chỉ+hạn · khác trục+khác khuôn) — thiếu thì BỎ SLOT, không đăng bù"],
    },
    "akiya": {
        "name": "実家とお金の整理ノート", "channel_id": "", "project": "youtube-jp-akiya",
        # 20:00 JST — ĐÃ ĐO XÁC NHẬN 2026-07-26 (API): kênh faceless duy nhất chứng minh format ở tệp này
        # (きな子のシニアお金ゼミ 167K sub, view/video 146K) khóa 20:00 và đã DỜI từ 18:00 → 20:00; hit 固定資産税 1,06M đăng 20:00.
        # NGÀY SỬA 2026-07-28 (đo 50 video/kênh): T6 + T7, thay CN → T7.
        #   · きな子: T7 = 17/50 (ngày đăng nhiều nhất); median view T6 65,7K > T3 50,8K > T7 29,4K > CN 18,9K → CN là ngày yếu.
        #   · 税理士勝部: T7 = 47/50 video (khóa cứng thứ Bảy).
        # 2/tuần là TRẦN (あまおう đăng 1/ngày → view 1,3–32K; 勝部 rời lõi → 80 view). Điều kiện tăng nhịp: 08_ANALYTICS_LOG.md §0.
        # ⏸ NGƯNG HOẠT ĐỘNG 2026-07-28 (user chốt: chỉ 4 kênh active = chouhen/co-dai/health/nenkin).
        #    Lịch cũ: T6·T7 20:00 — chờ Gmail kênh, bật lại bằng giá trị này
        "slots": [], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công", "Altered content: video CÓ ảnh/cảnh AI realistic thì PHẢI TICK (luật đảo chiều 2026-08-09, youtube-compliance §2.1). Giọng TTS + thumbnail AI + script AI = KHÔNG cần tick. Tool chưa tự phát hiện — TỰ KIỂM slides_img_*/ trước khi bấm",
                      "made for kids = NO",
                      "概要欄 có 「◯年◯月時点の情報」+「制度は市区町村によって異なります」+ không phải tư vấn cá nhân/pháp lý + credit VOICEVOX:剣崎雌雄 + イラスト:いらすとや",
                      "GATE 5 ĐIỂM đã pass (số tiền của cast trước phút 2 · ≥2 原典ショット, shot đầu ≤3′ · なぜ · hành động có địa chỉ+hạn · khác trục+khác khuôn) — thiếu thì BỎ SLOT",
                      "Video trục 相続登記: ưu tiên đăng TRƯỚC 2027-03-31 (hạn ca hồi tố); 固定資産税納税通知書 chạy T4–T5"],
    },
    "yawa": {
        "name": "人生哲学の夜話", "channel_id": "UCuzbgcFHVmAf4O6wU1wLyIQ", "project": "youtube-jp-yawa",
        # Rebrand chouhen 2026-09-28 (CUNG channelId). Project: Projects/youtube-jp-yawa/CLAUDE.md.
        # ⭐ LICH 2026-09-30: do 8 kenh ngach 人生/60代 (youtube-jp-yawa/01_SOURCES/UPLOAD_SCHEDULE_MEASURE_2026-09-30.md):
        #    6/8 kenh dang 18:00 JST · hieu suat 水 x2,01 / 金 x1,77 / 月 x1,04.
        #    ⭐ USER CHOT 2026-09-30: 3/tuan T2·T4·T6, 18:15 JST (lui 15' sau gio doi thu 18:00 — video minh la video MOI NHAT).
        #    Khong trung showa (T3·T5·T7 18:00) / nenkin (T3·T5·CN 19:00).
        "slots": [(0, 18, 15), (2, 18, 15), (4, 18, 15)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công",
                      "Altered/synthetic: KHÔNG bắt buộc tick (youtube-compliance.md §2: ảnh AI anime không realistic + ảnh stock thật + giọng TTS không nhái người thật)",
                      "made for kids = NO",
                      "概要欄 có 「本作品は…創作物語です」 + 引用 古典 + credit 「VOICEVOX:東北イタコ」 + BGM",
                      "⛔ 34 video スカッと cũ vẫn 限定公開 — đừng đổi lại công khai"],
    },
    "showa": {
        "name": "昭和くらし図鑑", "channel_id": "UCT0CITcGxFErQk_YjQriZ_w", "project": "youtube-jp-showa",
        # Kênh LẬP THẬT 2026-08-14 (đổi tên brand channel "Gonn Sau" sẵn có).
        # 🔴 SỬA 2026-08-16 (user chốt): chủ kênh là gonnsau@gmail.com = Chrome "Profile 15" (tên: Gonn).
        #    Bản ghi cũ saubeo.killuaa@gmail.com / Profile 9 là SAI — killuaa chỉ CÓ QUYỀN quản lý.
        # Handle @showa-kurashi-zukan · country JP · cat 27 教育 · 22 channel keywords.
        # Chi tiết setup: Projects/youtube-jp-showa/07_CHANNEL_SETUP_2026-08-14.md
        # ⭐ LỊCH CHỐT 2026-08-14 sau khi ĐO 9 kênh cụm 昭和 (50 video/kênh, tách shorts):
        #    T3 · T5 · T7 @ 18:00 JST — 3 video/tuần, giãn 2-2-3 đúng nhịp Mục 0.9.
        #    Bằng chứng đầy đủ: .claude/rules/upload-schedule-measure-showa-2026-08-14.md
        #    · NGÀY: 伊東彩のほんのり昭和回顧 (142K, 0 shorts, đang đăng đều — kênh giống format nhất)
        #      đăng long-form CHỈ T3=19 · T7=19 · T5=11, median T7 23,9K > T3 21,5K; なつかし昭和
        #      median T5 148K (#1 kênh); 記憶装置 median T5 178K (#1) + T3 135K. T6/T2/T4/CN loại
        #      (伊東彩 CHƯA TỪNG đăng T4/T6/CN; T2 là ngày median bét ở 2/2 kênh có mẫu đủ).
        #    · GIỜ 18:00 (ngách đo được là 18–19h): chọn 18 thay 19 để KHÔNG chồng health+nenkin
        #      (cả hai 19:00 và cùng chạy T3·T5·CN → sẽ trùng showa 2 ngày/tuần). Lệch đúng 1h,
        #      giữ luật daypart ≥1h của Mục 0.9. 記憶装置 có 22/50 video đăng 18h nên vẫn trong dải.
        #    ⚠️ NGƯỢC tín hiệu nhịp của chính ngách: 3 kênh hiệu suất/video cao nhất đăng ≤1/tuần
        #      (記憶装置 0,32 · なつかし 0,98 · THEヤバイ 0,47) còn kênh 3,3/tuần chỉ 630–6.900 view.
        #      Giữ 3/tuần theo nhịp chuẩn user chốt 2026-08-03. 🛑 PHANH: 5 video đầu median ≤500 view
        #      và BROWSE_FEATURES vẫn 0 → hạ về 1/tuần [(3, 18)] (T5).
        "slots": [(1, 18), (3, 18), (5, 18)], "tz": 9, "tz_name": "JST", "cta_lang": "jp",
        "checklist": ["subs.srt thủ công",
                      "🔴🔴 Altered/synthetic content: TICK BẮT BUỘC — lớp hình của kênh có cảnh AI realistic. Từ video 16 kênh chạy REAL-FIRST v2 (~65% phim tư liệu PD + ảnh thật, ~35% AI, user chốt 2026-09-21) — tỉ lệ AI GIẢM KHÔNG bỏ được nghĩa vụ khai báo. Giọng TTS + thumbnail AI = KHÔNG cần tick, nhưng lớp hình thì CÓ",
                      "made for kids = NO",
                      "概要欄 có disclaimer nguồn tư liệu + credit ảnh PD/CC theo ATTRIBUTIONS.md + credit giọng (VOICEVOX:東北イタコ trục A / AivisSpeech:阿井田茂 trục B)",
                      "⛔ KHÔNG phát nhạc 昭和歌謡/CM song thật (Content ID) — kể VỀ nhạc thì được",
                      "Trục B (値段): mọi con số lên hình phải có nguồn 総務省統計局/日銀 + năm; quy đổi 今の価値 ghi cách tính trong script"],
    },
}


# ⚠️ Hàm _chouhen_slots() (ramp 5→6→7 slot/tuần theo BUFFER video đã render trong 06_VIDEO)
# đã XOÁ 2026-08-03: user chốt nhịp CỐ ĐỊNH toàn hệ thống — kênh đang được đề xuất 1 video/NGÀY,
# kênh còn lại 2 ngày 1 video — nên lịch không được tự nhảy theo tồn kho nữa ("tao cần sự đều đặn").
# Nhịp giờ nằm thẳng trong CHANNELS["chouhen"]["slots"] = 7 slot 09:00.
# Gate NĂNG LỰC vẫn đứng TRÊN lịch, chỉ là thi hành bằng tay: không có hàng qua gate thì BỎ SLOT,
# KHÔNG đăng bù (phanh: 3 video liên tiếp <50 view · retention mốc 2'54" <30% → hạ về 5/tuần T2–T6).
# Muốn khôi phục ramp → lấy lại hàm từ git history (bản trước 2026-08-03).


def slot_hm(slot) -> tuple[int, int, int]:
    """Chuẩn hoá 1 slot về (weekday, giờ, phút) — nhận cả (wd, h) lẫn (wd, h, m).

    Dùng ở MỌI chỗ đọc lịch (upload_pack, pipeline_status, dashboard) để giờ lẻ phút
    (shokutaku 17:30) không làm vỡ code cũ vốn unpack đúng 2 phần tử."""
    wd, hour = int(slot[0]), int(slot[1])
    minute = int(slot[2]) if len(slot) > 2 else 0
    return wd, hour, minute


def slot_key(slot) -> tuple[int, int]:
    """Khoá sắp xếp theo thời điểm trong ngày (giờ, phút)."""
    _, h, m = slot_hm(slot)
    return h, m

# ⚠️ Hàm _kaigo_slots() (tự nhảy lên 1 video/NGÀY khi 07_UPLOADED ≥ 5) đã XOÁ 2026-07-28:
# user chốt hạ kaigo về T3·T6 2/tuần cố định sau khi đo lại publishedAt 50 video của 4 kênh benchmark
# (節約看護師りょう 1,02 video/tuần → median 106K view/video; あまおう 1 video/ngày → 1,3–32K view).
# Nhịp giờ nằm thẳng trong CHANNELS["kaigo"]["slots"], không còn logic tự chuyển.
# GATE 5 ĐIỂM vẫn đứng TRÊN lịch: không đủ hàng qua gate thì BỎ SLOT, không đăng bù
# (ngưỡng phanh: Projects/youtube-jp-kaigo/08_ANALYTICS_LOG.md §0).

VN_TZ = 7
WEEKDAY_VN = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
# Từ nhóm nặng nhất (youtube-compliance.md mục 3) — chỉ quét phần HIỂN THỊ (title + 3 dòng đầu)
BANNED = ["血まみれ", "流血", "血だらけ", "死ね", "自殺", "レイプ", "虐待",
          "giết", "đẫm máu", "tự tử", "tự sát"]
_MEDICAL_BLOOD = ("貧血", "血圧", "血糖", "血管", "血液", "血流")  # thuật ngữ y khoa hợp lệ
_SAFE_KILL = ("殺菌", "殺虫", "相殺", "黙殺")  # từ ghép vô hại (khử trùng/thuốc muỗi…)


def scan_banned(title: str, desc3: str) -> list[str]:
    """Quét từ nhạy phần hiển thị. 殺 trần soi cả title+3 dòng (bỏ 殺菌/殺虫…);
    血 trần chỉ soi ở TITLE (rule mục 3), bỏ từ ghép y khoa (貧血/血圧…)."""
    visible = title + "\n" + (desc3 or "")
    hits = {w for w in BANNED if w in visible}
    v = visible
    for m in _SAFE_KILL:
        v = v.replace(m, "")
    if "殺" in v:
        hits.add("殺")
    t = title
    for m in _MEDICAL_BLOOD:
        t = t.replace(m, "")
    if "血" in t:
        hits.add("血 (trong title)")
    return sorted(hits)

MIN_LEAD_HOURS = 3  # video 60' cần thời gian upload + process trước giờ hẹn

# Heading thật (#...) hoặc bold label kiểu kr `**[3 dòng đầu — ...]**` đều tính là mốc section
_RE_HEAD = re.compile(r"^\s*#{1,6}\s")
# Nhãn-mốc đứng riêng một dòng: `**[1] TITLE**` (khuôn cũ) và `**Title CHỐT**` / `> **Tên file
# upload**` (khuôn co-dai/chouhen — bold trong blockquote). Vá 2026-08-17: trước đây chỉ nhận dạng
# có ngoặc vuông nên mọi mốc kiểu `> **Tên file upload**` KHÔNG được coi là mốc ⇒ find_block trả
# None ⇒ gói upload lấy tên mp4 = slug thô thay vì slug SEO, im lặng.
_RE_LABEL = re.compile(r"^\s*(?:>\s*)*\*\*[^*]+\*\*\s*:?\s*$")


def _is_heading(line: str) -> bool:
    return bool(_RE_HEAD.match(line) or _RE_LABEL.match(line))


def find_script(proj: Path, slug: str) -> Path | None:
    """Script nằm ở 0N_SCRIPTS/ — số N khác nhau theo kênh (01 stickman, 02 kr, 03 chouhen/co-dai, 04 health/shokutaku)."""
    for pat in (f"0[0-9]_SCRIPTS/{slug}.md", f"0[0-9]_SCRIPTS/{slug}*.md"):
        hits = sorted(p for p in proj.glob(pat) if not p.name.endswith("_TTS.md"))
        if hits:
            return hits[0]
    return None


def find_video_dir(proj: Path, slug: str) -> Path | None:
    """Folder video output: 06_VIDEO (JP) hoặc 04_VIDEO (kr/stickman)."""
    return next((p for p in sorted(proj.glob(f"0[0-9]_VIDEO/{slug}")) if p.is_dir()), None)


def find_srt(proj: Path, vdir: Path, slug: str) -> Path:
    """subs.srt cạnh video; kr-romfan để ở 0N_VOICE/<slug>/subs.srt."""
    srt = vdir / "subs.srt"
    if srt.exists():
        return srt
    alt = next(iter(proj.glob(f"0[0-9]_VOICE/{slug}/subs.srt")), None)
    return alt or srt


def find_scripts(proj: Path, slug: str) -> list[Path]:
    """MỌI file liên quan slug ở 0N_SCRIPTS/: bản sạch <slug>.md + <slug>_TTS.md + các phần <slug>_*.md
    + SLIDES/cấu hình <slug>_*.json (SLIDES/SLIDES_photo/SLIDES_video…) — gom hết để KHÔNG bỏ sót mồ côi ở folder khác.
    Match có dấu ngăn (_) để không dính slug khác cùng tiền tố."""
    hits: set[Path] = set()
    for pat in (f"0[0-9]_SCRIPTS/{slug}.md", f"0[0-9]_SCRIPTS/{slug}_*.md", f"0[0-9]_SCRIPTS/{slug}_*.json"):
        hits.update(p for p in proj.glob(pat) if p.is_file())
    return sorted(hits)


def find_voice_dir(proj: Path, slug: str) -> Path | None:
    """Folder voice riêng (kr-romfan): 0N_VOICE/<slug>/ (kênh JP để voice.wav trong folder video)."""
    return next((p for p in sorted(proj.glob(f"0[0-9]_VOICE/{slug}")) if p.is_dir()), None)


def move_related(proj: Path, slug: str, dest: Path) -> None:
    """Gom mọi thứ liên quan slug từ working folder vào kho 07_UPLOADED/<slug>/ (user chốt 2026-07-20):
       ① script .md -> _scripts/ (GIỮ lại — nhẹ, nguồn re-render)
       ② folder voice riêng kr (0N_VOICE/<slug>/) -> _voice/ (bị prune xóa cùng mp4/voice.wav — chỉ để dọn working dir)
    Gọi sau khi folder video đã move thành dest. Idempotent: chạy lại không lỗi (file đã move thì bỏ qua)."""
    # ① Scripts — bản sạch + _TTS + các phần; giữ lại trong kho làm nguồn re-render
    scripts = find_scripts(proj, slug)
    if scripts:
        sdir = dest / "_scripts"
        sdir.mkdir(exist_ok=True)
        moved = 0
        for s in scripts:
            tgt = sdir / s.name
            if tgt.exists():
                continue
            shutil.move(str(s), str(tgt))
            moved += 1
        if moved:
            print(f"📄 Chuyển {moved} file script -> {sdir.name}/ (giữ lại trong kho)")

    # ② Folder voice riêng kr -> _voice/ (dọn working dir; sẽ bị prune xóa như mp4)
    voice_src = find_voice_dir(proj, slug)
    if voice_src:
        vodir = dest / "_voice"
        vodir.mkdir(exist_ok=True)
        for f in voice_src.iterdir():
            tgt = vodir / f.name
            if not tgt.exists():
                shutil.move(str(f), str(tgt))
        try:
            voice_src.rmdir()  # dọn folder rỗng ở nơi cũ
        except OSError:
            pass
        print(f"🎙️ Chuyển voice -> {vodir.name}/ (sẽ dọn cùng mp4 ở bước prune)")


def _dequote(line: str) -> str:
    """Bỏ tiền tố blockquote '> ' (lồng nhiều cấp) — để fence nằm TRONG blockquote vẫn nhận ra.
    🔴 CHỈ bỏ đúng '>' + MỘT space ASCII, KHÔNG strip() cả dòng: nội dung 概要欄 dùng khoảng
    trắng full-width `　` để thụt lề (health 29 thụt dòng số liệu dưới tên nguồn) — strip là
    ăn mất thụt lề đó, và mô tả gói ra khác bản trong script mà không ai báo."""
    s = line
    while True:
        m = re.match(r"[ \t]*>[ \t]?", s)
        if not m or m.end() == 0:
            return s
        s = s[m.end():]


def find_block(text: str, *keywords: str, plain_fallback: bool = False,
               exclude: tuple = ()) -> str | None:
    """Tìm heading/bold-label chứa 1 trong keywords, trả code block ``` đầu tiên sau đó.
    plain_fallback: section khớp mà không có code fence → trả text thường tới mốc kế
    (format shokutaku/health/kr để nội dung ngoài fence hoặc blockquote).
    exclude: bỏ qua mốc chứa các chuỗi này (vd 해시태그 chứa 태그).

    ⚠️ So chuỗi KHÔNG phân biệt hoa/thường (vá 2026-08-08). Ca gốc: chouhen video 19 viết
    heading `### 概要欄 — 3 DÒNG ĐẦU` / `### 概要欄 — MÔ TẢ ĐẦY ĐỦ` (IN HOA) trong khi
    keywords là "3 dòng đầu"/"mô tả đầy đủ" → trả None → ô [3] DESCRIPTION của METADATA.txt
    TRỐNG RỖNG dù nội dung 概要欄 nằm nguyên trong script. Lỗi im lặng: chỉ có 1 dòng cảnh
    báo ở CUỐI file nên rất dễ trôi tới lúc đăng."""
    lines = text.splitlines()
    kw = tuple(k.casefold() for k in keywords)
    ex = tuple(x.casefold() for x in exclude)
    for i, line in enumerate(lines):
        low = line.casefold()
        if _is_heading(line) and any(k in low for k in kw) \
                and not any(x in low for x in ex):
            for j in range(i + 1, len(lines)):
                if _is_heading(lines[j]):  # gặp mốc kế mà chưa thấy block
                    break
                # ⚠️ Bỏ tiền tố blockquote '>' TRƯỚC khi nhận diện fence (vá 2026-08-17).
                # Ca gốc: co-dai video 20 viết `> **Tên file upload**` + fence THỤT TRONG
                # blockquote (```` > ``` ````) — nhánh này trả None nên METADATA gói mp4 bằng
                # tên slug thô thay vì slug SEO, im lặng (cùng họ lỗi với §4 youtube-upload-seo).
                if _dequote(lines[j]).strip().startswith("```"):
                    block = []
                    for k in range(j + 1, len(lines)):
                        if _dequote(lines[k]).strip().startswith("```"):
                            return "\n".join(block).strip()
                        block.append(_dequote(lines[k]))
            if plain_fallback:
                out = []
                for j in range(i + 1, len(lines)):
                    if _is_heading(lines[j]):
                        break
                    out.append(lines[j])
                if "\n".join(out).strip():
                    return "\n".join(out).strip()
    return None


def find_section_blocks(text: str, *keywords: str) -> list[str]:
    """Gom TẤT CẢ code block nằm dưới heading khớp keyword, tới heading THẬT kế tiếp.
    Format kr (설명란: 3 dòng + timeline + 본문 + hashtag) / stickman (概要欄 gộp 1 block).
    So chuỗi KHÔNG phân biệt hoa/thường — cùng lý do ở find_block."""
    lines = text.splitlines()
    kw = tuple(k.casefold() for k in keywords)
    for i, line in enumerate(lines):
        if _RE_HEAD.match(line) and any(k in line.casefold() for k in kw):
            blocks, j = [], i + 1
            while j < len(lines) and not _RE_HEAD.match(lines[j]):
                if lines[j].strip().startswith("```"):
                    block, j = [], j + 1
                    while j < len(lines) and not lines[j].strip().startswith("```"):
                        block.append(lines[j])
                        j += 1
                    if "\n".join(block).strip():
                        blocks.append("\n".join(block).strip())
                j += 1
            if blocks:
                return blocks
    return []


def parse_ctr(text: str) -> dict:
    """Bóc gói CTR từ script — hiểu cả format chouhen (Title CHỐT/code block)
    lẫn shokutaku-family (B. TIÊU ĐỀ VIRAL list số, E.1/E.2/E.3, khối cố định)."""
    import re

    # Bộ A/B title (bảng "3 TITLE A/B": | **A1** … | `title` | …)
    ab_titles = []
    mtab = re.search(r"###\s*3 TITLE A/B.*?\n(.*?)(?=\n###|\Z)", text, re.S)
    if mtab:
        for row in mtab.group(1).splitlines():
            mm = re.match(r"\s*\|\s*\*{0,2}(A\d)\*{0,2}[^|]*\|\s*`([^`]+)`\s*\|", row)
            if mm:
                # bảng markdown phải escape ống dẫn thành \| — title thật thì dùng | trần
                ab_titles.append((mm.group(1), mm.group(2).strip().replace("\\|", "|")))

    # Title: ưu tiên "Title CHỐT"/"Chốt metadata" (fence hoặc blockquote kr);
    # fallback = list số dưới heading TIÊU ĐỀ/TITLE, chọn mục N nếu có dòng "→ Đề xuất: #N" (stickman)
    title = find_block(text, "Title CHỐT", "Title chốt", "TITLE CHỐT", "Chốt metadata",
                       plain_fallback=True)
    if title:
        first = next((l for l in title.splitlines() if l.strip()), "")
        title = re.sub(r"^[>\s]+", "", first)                      # bỏ blockquote '>'
        title = re.sub(r"^\*\*(.+?)\*\*$", r"\1", title.strip()).strip()  # bỏ bold bao ngoài
    else:
        m = re.search(r"→\s*Đề xuất[^\d#\n]*#?(\d+)", text)  # stickman: "→ Đề xuất: #1"
        want = int(m.group(1)) if m else None
        lines = text.splitlines()
        for i, l in enumerate(lines):
            if _RE_HEAD.match(l) and ("TIÊU ĐỀ" in l.upper() or "TITLE" in l.upper()):
                items, raw = {}, {}
                for j in range(i + 1, min(i + 15, len(lines))):
                    mi = re.match(r"\s*(?:\*\*)?(\d+)[\.．]\s*(.+)", lines[j])
                    if mi:
                        n = int(mi.group(1))
                        raw[n] = mi.group(2)
                        # bỏ prefix bold dạng chú thích **(P1 · KHUYẾN NGHỊ)**, rồi bỏ marker ** còn lại
                        val = re.sub(r"\*\*\([^)]*\)\*\*", "", mi.group(2))
                        # dòng dạng `**title** (chú thích ngoài bold)` → chỉ lấy phần bold, vứt chú thích
                        mb = re.match(r"\s*\*\*(.+?)\*\*\s*(?:\([^)]*\))?\s*$", val)
                        if mb:
                            val = mb.group(1)
                        items[n] = val.replace("**", "").strip() or mi.group(2).strip()
                if items:
                    # ưu tiên: mục đánh dấu CHỐT > mục "→ Đề xuất #N" > mục KHUYẾN NGHỊ > mục 1
                    marked = next((n for n, v in raw.items() if "CHỐT" in v.upper()), None)
                    rec = next((n for n, v in raw.items() if "KHUYẾN NGHỊ" in v.upper()), None)
                    pick = marked or want or rec or 1
                    title = items.get(pick) or items.get(1) or next(iter(items.values()))
                    break

    if not title and ab_titles:
        # khuôn ab-3title-3thumb.md: chỉ có bảng "3 TITLE A/B", không có block "Title CHỐT"
        # riêng và không có list số dưới heading TIÊU ĐỀ/TITLE (2 nhánh trên đều trượt).
        # A1 luôn là bản CHỐT (`ab-3title-3thumb.md` §2 mục 1: "A1 phải trùng đúng từng ký tự
        # với block Title CHỐT") → dùng A1 làm title chính khi không có block riêng.
        a1 = next((t for lbl, t in ab_titles if lbl == "A1"), None)
        title = a1 or ab_titles[0][1]

    fname = find_block(text, "Tên file upload", "tên file upload", "Tên file video")
    if not fname:  # format health/kr: inline "**Tên file upload/video ...:** `xxx.mp4`"
        m = re.search(r"Tên file (?:upload|video)[^\n`]*`([^`\n]+\.mp4)`", text)
        fname = m.group(1) if m else None
    if not fname:
        # khuôn showa/chouhen: heading `### Tên file upload` rồi tên nằm ở DÒNG SAU, dạng `x.mp4`
        # (không fence, không cùng dòng) → find_block trả None và regex inline ở trên cũng trượt
        # vì `[^\n\`]*` không qua được xuống dòng. Ca gốc: showa 01_kyushoku (2026-08-17).
        m = re.search(r"Tên file (?:upload|video)[^\n]*\n(?:[ \t]*\n)*[^\n`]{0,40}`([^`\n]+\.mp4)`",
                      text, re.IGNORECASE)
        fname = m.group(1) if m else None
    desc3 = find_block(text, "3 dòng đầu", "Ba dòng đầu", "ba dòng đầu")
    descf = find_block(text, "mô tả đầy đủ", "Mô tả đầy đủ", "BẢN ĐẦY ĐỦ", plain_fallback=True)
    # format health: section chỉ là ghi chú trỏ sang file description_youtube.txt → bỏ, để caller đọc file
    if descf and "description_youtube.txt" in descf:
        descf = None
    if desc3 and "description_youtube.txt" in desc3:
        desc3 = None
    tags_raw = find_block(text, "タグ", "태그", "tags", "TAGS", plain_fallback=True,
                          exclude=("ハッシュタグ", "해시태그", "Hashtag", "hashtag"))

    # Khuôn chouhen: khối "mô tả đầy đủ" MỞ ĐẦU bằng chính 3 dòng SEO (cố ý — để copy lẻ vẫn đủ).
    # Nối thẳng desc3 + descf ⇒ 概要欄 lặp nguyên 3 dòng đầu 2 lần (video 14 đã lên sóng như vậy).
    # Vá 2026-08-02: descf đã chứa desc3 ở đầu → dùng luôn descf.
    def _first_line(s: str) -> str:
        return next((l.strip() for l in s.splitlines() if l.strip()), "")

    if desc3 and descf and _first_line(descf) == _first_line(desc3):
        description = descf
    else:
        description = "\n\n".join(x for x in (desc3, descf) if x)
    # Format kr/stickman: mô tả đầy đủ = (nhiều) code block dưới heading 설명란 / 概要欄 gộp
    if not descf:
        blocks = find_section_blocks(text, "설명란", "概要欄 /", "概要欄（説明")
        if blocks:
            description = "\n\n".join(blocks)
            descf = description
            desc3 = desc3 or (blocks[0] if len(blocks) > 1 else "\n".join(blocks[0].splitlines()[:3]))
    # Chốt cuối (2026-08-08): heading chỉ ghi 概要欄 trần, không có chữ "mô tả đầy đủ"
    # (shokutaku viết `## F. 概要欄 (draft)`) → vẫn phải đọc, thà lấy bản draft còn hơn ô [3] trống.
    # exclude các heading 3-dòng-đầu để không nhặt nhầm khối hook làm cả mô tả.
    if not descf:
        alt = find_block(text, "概要欄", plain_fallback=True,
                         exclude=("3 dòng", "ba dòng", "3 DÒNG"))
        if alt and "description_youtube.txt" not in alt:
            descf = alt
            description = "\n\n".join(x for x in (desc3, alt) if x) if _first_line(alt) != _first_line(desc3 or "") else alt
    # Khối cố định (出典/disclaimer/credit) tách riêng kiểu shokutaku → nối vào sau
    if description and "音声" not in description and "朗読音声" not in description:
        fixed = find_block(text, "khối cố định")
        if fixed:
            fl = fixed.splitlines()
            start = next((k for k, l in enumerate(fl) if l.startswith("【") or l.startswith("※")), None)
            if start is not None:
                description += "\n\n" + "\n".join(fl[start:]).strip()
    # Hashtag nằm ngoài mô tả → nối cuối.
    # 🔴 VÁ 2026-08-09: bản cũ nhận diện bằng `"ハッシュタグ" in l and "#" in l` rồi cắt từ
    # `l.index("#")`. Heading markdown `### ハッシュタグ` khớp CẢ HAI (dấu # là của ###) →
    # nó dán nguyên chuỗi "### ハッシュタグ" vào cuối 概要欄, còn dòng hashtag THẬT
    # (`#朗読 #スカッとする話 …`, không chứa chữ "ハッシュタグ") thì không bao giờ được lấy.
    # → Nhận diện bằng CHÍNH token hashtag (≥2 token), và bỏ qua mọi dòng là heading.
    if description and not re.search(r"(^|\n)#\S+", description):
        for l in text.splitlines():
            if _is_heading(l):
                continue
            toks = re.findall(r"#[^\s#]+", l)
            # 🔴 Vá 2026-08-28: script hay nhắc "đã dùng ở #19 và #22" (số VIDEO trong văn
            # xuôi, không phải hashtag) — 2 token đó cũng khớp regex trên và bị nhặt nhầm
            # TRƯỚC KHI quét chạm dòng hashtag thật ở cuối file (co-dai video 25, description
            # ra "...励みになります。\n\n#19 #22)."). Hashtag thật trong workspace luôn là
            # CỤM CHỮ (日本語/English), không bao giờ thuần số → loại token `#<digits>` trước
            # khi đếm.
            toks = [t for t in toks if not re.fullmatch(r"#\d+\W*", t)]
            if len(toks) >= 2:
                description += "\n\n" + " ".join(toks)
                break

    tags = [t.strip().strip("`").strip() for t in (tags_raw or "").replace("\n", ",").split(",")]
    tags = [t for t in tags if t and "#" not in t and "ハッシュタグ" not in t
            and not re.fullmatch(r"[-–—=_*]+", t)][:60]  # vứt dòng kẻ ngang --- lọt vào block tags
    if not desc3 and descf:  # format co-dai: khối đầy đủ MỞ ĐẦU bằng chính 3 dòng SEO
        desc3 = "\n".join(descf.splitlines()[:3])  # chỉ để scan/checklist, KHÔNG ghép lại vào description
    pinned = find_block(text, "Pinned comment", "pinned comment", "コメント固定", "固定コメント",
                        "Bình luận ghim", "고정 댓글", plain_fallback=True)
    return {"title": title, "fname": fname, "desc3": desc3, "descf": descf,
            "description": description, "tags": tags, "pinned": pinned, "ab_titles": ab_titles}


def append_image_credits(description: str, vdir: Path) -> tuple[str, int]:
    """Ảnh CC BY trong ATTRIBUTIONS.md của video BẮT BUỘC ghi credit (media-library.md §4).
    Tự nhét khối credit vào 概要欄 (trước dòng hashtag cuối). Trả (description, số ảnh thêm)."""
    import re
    cands = [p for p in vdir.glob("**/ATTRIBUTIONS.md")
             if not re.search(r"old|backup", str(p.relative_to(vdir)), re.I)]
    attrib = max(cands, key=lambda p: p.stat().st_mtime, default=None)
    if not attrib or "commons.wikimedia" in description:
        return description, 0
    cc_by = [re.sub(r"^[-\s]*slide_\d+:\s*", "", l).strip()
             for l in attrib.read_text(encoding="utf-8").splitlines()
             if "CC BY" in l.upper() and "CC0" not in l.upper()]
    if not cc_by:
        return description, 0
    credit = "画像出典（Wikimedia Commons）：\n" + "\n".join("・" + l for l in cc_by)
    lines = description.rstrip().splitlines()
    if lines and lines[-1].lstrip().startswith("#"):  # hashtag đứng cuối → chèn trước
        return "\n".join(lines[:-1]).rstrip() + "\n\n" + credit + "\n\n" + lines[-1], len(cc_by)
    return description.rstrip() + "\n\n" + credit, len(cc_by)


def _srt_end_seconds(srt: Path) -> float | None:
    """Timestamp kết thúc của cue cuối trong subs.srt (giây)."""
    try:
        ts = re.findall(r"-->\s*(\d+):(\d\d):(\d\d)[,.](\d+)", srt.read_text(encoding="utf-8", errors="ignore"))
        if not ts:
            return None
        h, m, s, _ = ts[-1]
        return int(h) * 3600 + int(m) * 60 + int(s)
    except OSError:
        return None


def _ffprobe_duration(mp4: Path) -> float | None:
    import subprocess
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", str(mp4)], capture_output=True, text=True, timeout=60)
        return float(out.stdout.strip())
    except Exception:
        return None


def preflight(mp4: Path, srt: Path, description: str, script: Path, cta_lang: str) -> list[str]:
    """Kiểm tra chất lượng gói TRƯỚC khi giao: duration, sync srt, CTA, chapter, độ tươi metadata."""
    warns = []
    dur = _ffprobe_duration(mp4)
    if dur is None:
        warns.append("Không đo được duration (ffprobe) — tự kiểm tra video bằng mắt")
        return warns
    if dur < 180:
        warns.append(f"⚠️ Video chỉ {dur/60:.1f} phút — render dở?")
    end = _srt_end_seconds(srt) if srt.exists() else None
    if end and abs(dur - end) > 90:
        warns.append(f"⚠️ subs.srt kết thúc {end/60:.1f}' nhưng video {dur/60:.1f}' — srt LỆCH bản render?")
    # CTA giữa video (rule cta-midvideo) — câu canonical phải nằm trong srt
    try:
        from cta_inject import PATTERNS
        if srt.exists():
            srt_text = srt.read_text(encoding="utf-8", errors="ignore")
            if not any(p in srt_text for p in PATTERNS.get(cta_lang, [])):
                warns.append("⚠️ KHÔNG thấy câu CTA giữa video trong subs.srt (rule cta-midvideo)")
    except ImportError:
        pass
    # Chapter 目次 trong description không được vượt duration (bắt re-render lệch timestamp)
    marks = [int(h or 0) * 3600 + int(m) * 60 + int(s)
             for h, m, s in re.findall(r"(?:(\d{1,2}):)?(\d{1,2}):(\d\d)\b", description)]
    if marks and max(marks) > dur + 5:
        warns.append(f"⚠️ 目次 có mốc {max(marks)//60}:{max(marks)%60:02d} VƯỢT duration {dur/60:.1f}' — chapter lệch bản render, cập nhật description")
    if mp4.stat().st_mtime > script.stat().st_mtime + 60:
        warns.append("⚠️ mp4 MỚI hơn script — video đã re-render sau khi chốt metadata? Soát lại timestamp/目次")
    return warns


def prune_uploaded(dest: Path) -> None:
    """Dọn folder đã vào kho (user chốt 2026-07-22): CẮT bỏ video nặng, chỉ giữ
    metadata + subs + ảnh (_upload không .mp4) + _scripts (nguồn re-render, vài KB) + UPLOADED.txt.
    XÓA: mp4, voice.wav, _voice/, và mọi rác render còn lại."""
    freed = 0

    def _size(p: Path) -> int:
        return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else p.stat().st_size

    # GIỮ: hồ sơ upload (metadata/subs/thumbnail) + scripts (nguồn re-render) + sổ. Còn lại (mp4/voice/_voice/rác) xóa sạch.
    keep = ("_upload", "_scripts", "UPLOADED.txt")
    for item in list(dest.iterdir()):
        if item.name in keep:
            continue
        freed += _size(item)
        shutil.rmtree(item, ignore_errors=True) if item.is_dir() else item.unlink()
    up = dest / "_upload"
    if up.exists():
        for mp4 in up.glob("*.mp4"):  # _upload chỉ là hardlink SEO → xóa để chỉ còn metadata/subs/thumbnail
            freed += mp4.stat().st_size
            mp4.unlink()
    print(f"🧹 Dọn kho {dest.name}: chỉ giữ metadata+subs+ảnh (_upload không mp4) + _scripts + UPLOADED.txt "
          f"— giải phóng ~{freed / 1024 / 1024:.0f} MB")


def finish_kho(dest: Path, channel: str) -> None:
    """Bước cuối sau khi folder đã vào kho (user chốt 2026-07-22: bỏ hẳn AI cắt TikTok):
    LUÔN prune ngay — xóa video nặng (mp4 + voice + rác render), chỉ giữ metadata + subs + ảnh
    (+ _scripts nguồn re-render + UPLOADED.txt). Không còn phụ thuộc clip TikTok/AI."""
    prune_uploaded(dest)
    # Tự vá sổ: UPLOADED.txt là hồ sơ bắt buộc của folder trong kho — thiếu thì ghi lại
    marker = dest / "UPLOADED.txt"
    if not marker.exists():
        marker.write_text(f"uploaded: (khôi phục {datetime.now():%Y-%m-%d %H:%M} — marker gốc bị mất)\n",
                          encoding="utf-8")
        print("⚠️ UPLOADED.txt bị thiếu — đã ghi lại marker.")


def mark_done(proj: Path, slug: str, channel: str = "chouhen") -> None:
    """Sau khi upload xong: ghi UPLOADED.txt + move folder video sang kho 07_UPLOADED/ (convention chung),
    gom nốt script (-> _scripts/, giữ làm nguồn re-render) + voice riêng kr (-> _voice/, sẽ bị prune xóa),
    rồi finish_kho: LUÔN cắt video nặng, chỉ giữ metadata + subs + ảnh (user chốt 2026-07-22, bỏ AI TikTok)."""
    vdir = find_video_dir(proj, slug)
    dest_root = proj / "07_UPLOADED"
    if not vdir:
        if (dest_root / slug).exists():
            print(f"ℹ️ {slug} đã nằm trong kho {dest_root} rồi — quét nốt script/voice còn sót ngoài working dir.")
            move_related(proj, slug, dest_root / slug)
            return
        sys.exit(f"❌ Không thấy folder video {slug} trong {proj}")
    publish_line = ""
    meta = vdir / "_upload" / "METADATA.txt"
    if meta.exists():
        m = re.search(r"HẸN GIỜ \(Schedule\):\s*(.+)", meta.read_text(encoding="utf-8-sig"))
        publish_line = f"publishAt: {m.group(1).strip()}\n" if m else ""
    (vdir / "UPLOADED.txt").write_text(
        f"uploaded: {datetime.now():%Y-%m-%d %H:%M} (đánh dấu bằng upload_pack --done)\n{publish_line}",
        encoding="utf-8")
    dest_root.mkdir(exist_ok=True)
    dest = dest_root / slug
    if dest.exists():
        sys.exit(f"❌ {dest} đã tồn tại — kho có bản trùng tên, xử lý tay")
    shutil.move(str(vdir), str(dest))
    print(f"✅ Đã ghi sổ + chuyển kho: {dest}")
    move_related(proj, slug, dest)
    finish_kho(dest, channel)


def next_slot(cfg: dict, now_utc: datetime) -> datetime:
    """Slot sớm nhất theo lịch kênh, cách hiện tại >= MIN_LEAD_HOURS. Trả datetime giờ ĐỊA PHƯƠNG kênh."""
    tz = timezone(timedelta(hours=cfg["tz"]))
    now_local = now_utc.astimezone(tz)
    best = None
    for d in range(0, 14):
        day = (now_local + timedelta(days=d)).date()
        for slot in cfg["slots"]:
            wd, hour, minute = slot_hm(slot)
            if day.weekday() != wd:
                continue
            cand = datetime(day.year, day.month, day.day, hour, minute, tzinfo=tz)
            if cand - now_local >= timedelta(hours=MIN_LEAD_HOURS) and (best is None or cand < best):
                best = cand
    return best


def fmt_slot(dt_local: datetime, cfg: dict) -> str:
    vn = dt_local.astimezone(timezone(timedelta(hours=VN_TZ)))
    wd = WEEKDAY_VN[dt_local.weekday()]
    s = f"{dt_local:%Y-%m-%d} ({wd}) {dt_local:%H:%M} {cfg['tz_name']}"
    if cfg["tz"] != VN_TZ:
        s += f" = {vn:%H:%M} giờ VN"
        if vn.date() != dt_local.date():
            s += f" ({vn:%Y-%m-%d})"
    return s


def _jpeg_width(p: Path) -> int:
    """Bề rộng JPEG đọc từ khung SOF — cùng vai với _png_width.

    ⭐ 2026-09-16: bộ A/B của các kênh bake chữ bằng AI sinh ra là .jpg, không có bản .png.
    Thiếu hàm này thì _png_width trả 0 và bản .jpg bị loại oan bởi bộ lọc bề rộng ≥1280.
    """
    try:
        with open(p, "rb") as f:
            if f.read(2) != b"\xff\xd8":
                return 0
            while True:
                b0 = f.read(1)
                while b0 == b"\xff":
                    b0 = f.read(1)
                if not b0:
                    return 0
                m, ln = b0[0], int.from_bytes(f.read(2), "big")
                if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                    f.read(1)
                    f.read(2)                       # height
                    return int.from_bytes(f.read(2), "big")
                f.seek(ln - 2, 1)
                while True:                          # tới marker kế
                    c = f.read(1)
                    if not c:
                        return 0
                    if c == b"\xff":
                        break
    except OSError:
        return 0


def _img_width(p: Path) -> int:
    """Bề rộng ảnh, PNG hay JPEG đều đọc được."""
    return _png_width(p) or _jpeg_width(p)


def _png_width(p: Path) -> int:
    """Bề rộng PNG đọc thẳng từ IHDR — dùng để loại bản xem thử thu nhỏ.

    Đọc header thay vì cài PIL: 8 byte magic + 8 byte chunk header, rồi 4 byte width.
    """
    try:
        with open(p, "rb") as f:
            head = f.read(24)
    except OSError:
        return 0
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return 0
    return int.from_bytes(head[16:20], "big")


def link_or_copy(src: Path, dst: Path):
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)  # hardlink cùng ổ E: — 0 byte tốn thêm
    except OSError:
        shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser(description="Đóng gói upload YouTube bán tự động")
    ap.add_argument("slug", help="vd 07_amamidokoro-saikaihatsu")
    ap.add_argument("--channel", default="chouhen", choices=sorted(CHANNELS))
    ap.add_argument("--slot", help='ghi đè giờ hẹn, "YYYY-MM-DD HH:MM" giờ địa phương kênh')
    ap.add_argument("--thumb", help="chỉ định file thumbnail (khi folder có nhiều bản vA/vB)")
    ap.add_argument("--open", action="store_true", help="mở folder gói + YouTube Studio")
    ap.add_argument("--force", action="store_true", help="ghi đè gói cũ")
    ap.add_argument("--done", action="store_true",
                    help="đánh dấu ĐÃ UPLOAD: ghi UPLOADED.txt + move sang 07_UPLOADED/ + gom script/voice từ mọi folder + CẮT video (giữ metadata+subs+ảnh)")
    ap.add_argument("--prune", action="store_true",
                    help="dọn lại folder ĐÃ ở kho: cắt video nặng, chỉ giữ metadata+subs+ảnh (+_scripts)")
    a = ap.parse_args()

    cfg = CHANNELS[a.channel]
    proj = PROJECTS_ROOT / cfg["project"]
    if a.done:
        mark_done(proj, a.slug, a.channel)
        return
    if a.prune:
        dest = proj / "07_UPLOADED" / a.slug
        if not dest.is_dir():
            sys.exit(f"❌ {a.slug} chưa nằm trong kho {proj / '07_UPLOADED'}")
        finish_kho(dest, a.channel)
        return
    warns: list[str] = []

    # --- 1. Script: gói CTR ---
    script = find_script(proj, a.slug)
    if not script:
        sys.exit(f"❌ Không thấy script {a.slug}.md trong {proj} (đã quét mọi 0N_SCRIPTS/)")
    text = script.read_text(encoding="utf-8")

    ctr = parse_ctr(text)
    title, description = ctr["title"], ctr["description"]
    if not title:
        sys.exit(f"❌ Không tìm thấy title chốt trong {script.name} — đóng gói CTR trước đã.")
    for key, label in (("fname", "Tên file upload"), ("desc3", "概要欄 3 dòng đầu"),
                       ("descf", "mô tả đầy đủ"), ("tags", "タグ")):
        if not ctr[key]:
            warns.append(f"Thiếu mục '{label}' trong script — bổ sung trước khi đăng")
    # GATE MÔ TẢ (2026-08-08) — đọc được mô tả KHÔNG có nghĩa là mô tả đủ chuẩn.
    # youtube-upload-seo.md §2.3 đòi 200–300 từ (JP/KR ≈ 400–600 ký) theo timeline + 目次/timestamp.
    # Ca gốc: shokutaku 07 chỉ có 1 đoạn draft ~170 ký, không 目次 → lên sóng là mất tín hiệu
    # topic-cluster mà YouTube dùng để xếp video vào đúng rổ đề xuất.
    # 🟡 SEO NHẸ — ngoại lệ CÓ THỜI HẠN của riêng chouhen (user chốt 2026-08-12).
    # Căn cứ: youtube-jp-chouhen/CHANNEL_DIAGNOSIS_2026-08-12.md §3.3 — bộ kênh peer CÙNG RAIL
    # (đo từ insightTrafficSourceDetail, không phải search) ăn 44K–205K view với 0 tag, và video
    # 105.183 view của 毎日スカッと có description RỖNG. Rail RELATED_VIDEO không tiêu thụ metadata.
    # Ngoại lệ ghi ở: .claude/rules/youtube-upload-seo.md §5 + ab-3title-3thumb.md §6.
    # Xét lại 2026-08-22. Kênh khác giữ nguyên gate cũ.
    light_seo = a.channel == "chouhen"
    _d = (description or "").strip()
    if _d and not light_seo:
        if len(_d) < 400:
            warns.append(f"⚠️ 概要欄 chỉ {len(_d)} ký — rule đòi 200–300 từ (≈400–600 ký JP/KR) "
                         "theo timeline (youtube-upload-seo.md §2.3)")
        if not re.search(r"(^|\n)\s*\d{1,2}:\d{2}", _d):
            warns.append("⚠️ 概要欄 KHÔNG có 目次/timestamp — thêm chapter (mốc 00:00 bắt buộc "
                         "để YouTube tạo chương)")
    elif _d and light_seo:
        # Gate ĐẢO CHIỀU: ở chouhen mô tả DÀI mới là lỗi. Nhưng 2 khối bắt buộc vẫn phải còn.
        if len(_d) > 700:
            warns.append(f"⚠️ SEO NHẸ (chouhen): 概要欄 đang {len(_d)} ký — khuôn mới là ~300 ký "
                         "(hook → disclaimer → credit giọng → 3 hashtag), youtube-upload-seo.md §5")
        if "フィクション" not in _d:
            warns.append("🔴 THIẾU disclaimer フィクション trong 概要欄 — đây là COMPLIANCE "
                         "(youtube-compliance.md §5), KHÔNG phải SEO, cấm cắt")
        if not re.search(r"(AivisSpeech|VOICEVOX)", _d, re.I):
            warns.append("🔴 THIẾU credit giọng (AivisSpeech: morioki / VOICEVOX:青山龍星) — đây là "
                         "điều khoản LICENSE, KHÔNG phải SEO, cấm cắt")
        if len(ctr.get("tags") or []) > 8:
            warns.append(f"⚠️ SEO NHẸ (chouhen): {len(ctr['tags'])} tag — khuôn mới 0–8 tag "
                         "(peer 44K–205K view đều 0 tag)")
    # GATE 3×3 (.claude/rules/ab-3title-3thumb.md, user chốt 2026-08-02): MỌI kênh phải có
    # 3 title A/B + 3 thumbnail A/B. Đếm bằng máy — luật kiểm bằng mắt thì sẽ trôi.
    # 🔴 GỠ COUPLING 2026-08-13: gate 3×3 TRƯỚC ĐÂY ăn theo cờ `light_seo`, tức ngoại lệ
    # SEO-nhẹ của chouhen kéo theo luôn ngoại lệ 1+1. Hai thứ đó là HAI quyết định khác
    # nhau — user bật lại 3×3 cho chouhen (2026-08-13) nhưng GIỮ SEO nhẹ. Từ nay 3×3 áp
    # cho MỌI kênh, không phụ thuộc light_seo.
    n_ab_titles = len(ctr.get("ab_titles") or [])
    _need_titles = 3
    if n_ab_titles < _need_titles:
        warns.append(f"🔴 GATE 3×3: chỉ có {n_ab_titles}/{_need_titles} title A/B — thêm bảng "
                     "'### 3 TITLE A/B' (A1/A2/A3, A1 = Title CHỐT) vào script "
                     "(.claude/rules/ab-3title-3thumb.md)")

    # GATE PINNED COMMENT (user chốt 2026-09-08: "sao lần nào cũng thiếu Pinned comment ở
    # nenkin nhỉ … từ lần sau lúc nào cũng phải có").
    # 🔴 VÌ SAO THIẾU ĐƯỢC: ô [9] vốn nằm trong `if ctr.get("pinned"):` — không có thì tool
    #    IM LẶNG bỏ qua ô đó. Không lỗi, không cảnh báo, `METADATA.txt` vẫn trông đầy đủ.
    #    Đo 2026-09-08: nenkin 15/20 script có, 5 thiếu (09·10·11·12 đã lên sóng + 21).
    #    Đúng họ với bẫy ô [3] rỗng ở `youtube-upload-seo.md` §4 — thứ chỉ CÓ KHI CÓ mà
    #    không ai đếm thì sẽ khuyết dần.
    # ⚠️ PHẠM VI: chặn ĐỎ ở nenkin (user chốt). Kênh khác cũng khuyết (chouhen 11/30 ·
    #    shokutaku 6/21 · co-dai 16/22 · health 16/22) nhưng chưa được yêu cầu siết, nên
    #    chỉ nhắc ⚠️ — muốn siết kênh nào thì thêm key vào `_PINNED_HARD`.
    _PINNED_HARD = {"nenkin"}
    if not (ctr.get("pinned") or "").strip():
        if a.channel in _PINNED_HARD:
            warns.append("🔴 GATE PINNED: thiếu bình luận ghim — thêm khối '### Pinned comment' "
                         "(code fence) vào script. Khuôn nenkin: lời cảm ơn + 研究ノート ①–⑤ + "
                         "'お手元で確かめる3つ' + câu hỏi mời comment + disclaimer 時点/年金事務所")
        else:
            warns.append("⚠️ Chưa có Pinned comment trong script — thêm khối "
                         "'### Pinned comment' (bình luận ghim là chỗ rẻ nhất để xin comment)")

    upload_name = (ctr["fname"] or f"{a.slug}.mp4").strip().splitlines()[0].strip()
    if not upload_name.endswith(".mp4"):
        upload_name += ".mp4"
    tags_line = ",".join(ctr["tags"])

    # --- 2. Assets ---
    vdir = find_video_dir(proj, a.slug)
    if not vdir:
        sys.exit(f"❌ Không thấy folder video {a.slug} trong {proj} (đã quét mọi 0N_VIDEO/)")
    mp4 = vdir / f"{a.slug}.mp4"
    if not mp4.exists():
        cands = [p for p in vdir.glob("*.mp4") if "_test" not in p.name]
        if not cands:
            sys.exit(f"❌ Không thấy .mp4 trong {vdir}")
        mp4 = max(cands, key=lambda p: p.stat().st_size)
    srt = find_srt(proj, vdir, a.slug)
    if a.thumb:
        thumb = Path(a.thumb) if Path(a.thumb).is_absolute() else vdir / a.thumb
        if not thumb.exists():
            sys.exit(f"❌ Không thấy thumbnail chỉ định: {thumb}")
    else:
        # Ưu tiên thumbnail.png (style TEXT-WALL v3) — MẶC ĐỊNH kênh từ 2026-07-21 theo mổ xẻ
        # meta ngách; thumbnail_scene.png (SCENE v2) chỉ là phương án B/A-B test.
        # (SỬA 2026-07-26: thứ tự cũ ưu tiên scene_ trước → gói upload video 09 lấy sai bản,
        #  lấy bản v2 vốn đã trượt cửa duyệt 120px. Muốn gói bản scene thì dùng --thumb.)
        thumb = next((p for p in (vdir / "thumbnail.png", vdir / "thumbnail_scene.png")
                      if p.exists()), None)
        # 🔴 TRẦN 2 MB CỦA YOUTUBE (ab-3title-3thumb.md §3 mục 4). PNG 1920×1080 nền ảnh
        # thật rất dễ vượt (video 27: 2,12 MB → YouTube TỪ CHỐI, không báo lỗi gì rõ ràng).
        # Nhánh bộ A/B thumb_T* bên dưới đã tự đổi sang .jpg từ lâu; nhánh thumbnail.png
        # ĐƠN thì chưa — bịt tại đây. Có sẵn .jpg cạnh nó thì dùng, không thì tự xuất q92.
        if thumb and thumb.stat().st_size > 2 * 1024 * 1024:
            alt = thumb.with_suffix(".jpg")
            if not alt.exists():
                try:
                    from PIL import Image
                    Image.open(thumb).convert("RGB").save(alt, "JPEG", quality=92, optimize=True)
                except Exception as e:                      # noqa: BLE001
                    warns.append(f"thumbnail {thumb.stat().st_size/1048576:.2f} MB > trần 2 MB "
                                 f"và không xuất được .jpg ({e}) — YouTube sẽ TỪ CHỐI")
                    alt = None
            if alt and alt.exists():
                warns.append(f"thumbnail.png {thumb.stat().st_size/1048576:.2f} MB > trần 2 MB "
                             f"→ đã gói bản .jpg ({alt.stat().st_size/1048576:.2f} MB) thay thế")
                thumb = alt
    if not srt.exists():
        warns.append("KHÔNG có subs.srt — sẽ phải dùng auto-caption (xấu SEO)")
    _ab_any = [t for pat in ("thumb_T[0-9]*.png", "thumb_T[0-9]*.jpg")
               for t in vdir.glob(pat) if "preview" not in t.name]
    if not thumb and not _ab_any:
        warns.append("KHÔNG có thumbnail — render make_thumb trước")
    if (vdir / "UPLOADED.txt").exists():
        warns.append("⚠️ Video này ĐÃ ĐÁNH DẤU UPLOADED — đóng gói lại = sắp đăng TRÙNG?")

    # Format health: mô tả hoàn chỉnh nằm ở file riêng cạnh video
    if not description and (vdir / "description_youtube.txt").exists():
        description = (vdir / "description_youtube.txt").read_text(encoding="utf-8").strip()
        ctr["desc3"] = "\n".join(description.splitlines()[:3])
        ctr["descf"] = description
        warns = [w for w in warns if "3 dòng đầu" not in w and "mô tả đầy đủ" not in w]

    description, n_credit = append_image_credits(description, vdir)
    if n_credit:
        warns.append(f"Đã tự thêm credit {n_credit} ảnh CC BY vào 概要欄 (từ ATTRIBUTIONS.md)")

    # --- 2.5 Pre-flight: chất lượng video/srt/CTA/chapter ---
    warns += preflight(mp4, srt, description, script, cfg.get("cta_lang", "jp"))

    # --- 3. Giờ hẹn ---
    tz = timezone(timedelta(hours=cfg["tz"]))
    if a.slot:
        slot = datetime.strptime(a.slot, "%Y-%m-%d %H:%M").replace(tzinfo=tz)
    else:
        slot = next_slot(cfg, datetime.now(timezone.utc))
        if slot is None:
            sys.exit("❌ Không tính được giờ hẹn (config slots của kênh trống/lỗi) — dùng --slot \"YYYY-MM-DD HH:MM\"")

    # --- 4. Compliance quét phần hiển thị ---
    hits = scan_banned(title, ctr["desc3"] or "")
    if hits:
        warns.append(f"⚠️ TỪ NHẠY trong title/3 dòng đầu: {', '.join(hits)} — thay theo youtube-compliance.md mục 3 TRƯỚC khi đăng")
    # placeholder chưa điền kiểu "[tên track] — [nguồn/license, điền khi chốt BGM]" lọt vào 概要欄
    ph = re.findall(r"\[[^\]\n]*(?:tên|nguồn|điền|TODO|TBD|xxx)[^\]\n]*\]", description, re.I)
    if ph:
        warns.append(f"⚠️ Mô tả còn PLACEHOLDER chưa điền: {' '.join(ph[:3])} — điền/xóa TRƯỚC khi đăng")

    # --- 5. Build gói ---
    pack = vdir / "_upload"
    if pack.exists() and not a.force:
        sys.exit(f"❌ {pack} đã tồn tại — thêm --force để ghi đè")
    pack.mkdir(exist_ok=True)
    for old in pack.glob("*.mp4"):  # dọn mp4 cũ khác tên (đổi tên SEO giữa 2 lần gói)
        if old.name != upload_name:
            old.unlink()
    link_or_copy(mp4, pack / upload_name)
    if srt.exists():
        link_or_copy(srt, pack / "subs.srt")
    # BỘ A/B THUMBNAIL: mọi thumb_T<N>_*.png trong vdir → thumbnail.png (N=1) + thumbnail_T<N>.png.
    # Chạy TRƯỚC và NGOÀI nhánh `if thumb:` — vì video dùng bộ A/B thì trong vdir KHÔNG có
    # thumbnail.png gốc, nên nếu để bên trong thì không bao giờ chạy (bug 2026-08-01).
    # YouTube "Test & compare" nhận tối đa 3 ảnh/video. So mtime để đổi bản là gói lại bản mới
    # (cùng luật chống resume-ra-hàng-cũ của render-background.md §2.5).
    ab_packed = []
    # ⚠️ LOẠI mọi bản XEM THỬ thu nhỏ do make_thumb tự sinh (*_preview*, *_preview120, *_168…) —
    # chúng cũng khớp glob thumb_T*, và vì cùng số N nên sorted() cho bản nhỏ ghi ĐÈ bản full
    # lên thumbnail.png. Lọc theo TÊN là chạy sau đuôi mới mãi (2026-08-01 chặn "_preview" rồi
    # 2026-08-02 vẫn lọt "_168": _upload gói đúng bản 168px 40 KB làm thumbnail upload).
    # → Lọc theo BỀ RỘNG THẬT: thumbnail YouTube tối thiểu 1280px, bản xem thử luôn nhỏ hơn.
    # gom theo SO T: mot vai co ca .png lan .jpg (PNG vuot tran thi lay .jpg) — chon
    # ban <=2 MB, khong thi ban to nhat. Loc be rong >=1280 giu nguyen (chan ban xem thu).
    _cand: dict[int, list[Path]] = {}
    for pat in ("thumb_T[0-9]*.png", "thumb_T[0-9]*.jpg"):
        for t in vdir.glob(pat):
            _m = re.search(r"thumb_T(\d+)", t.name)
            if _m and "preview" not in t.name and _img_width(t) >= 1280:
                _cand.setdefault(int(_m.group(1)), []).append(t)
    _pick = []
    for _n in sorted(_cand):
        _fits = [x for x in _cand[_n] if x.stat().st_size <= 2 * 1024 * 1024]
        _pick.append(min(_fits, key=lambda x: x.suffix != ".png") if _fits
                     else max(_cand[_n], key=lambda x: x.stat().st_size))
    for tp in _pick:
        mnum = re.search(r"thumb_T(\d+)", tp.name)
        if not mnum:
            continue
        n = int(mnum.group(1))
        # YouTube chặn thumbnail >2 MB. PNG của make_thumb hay vượt; bản .jpg q95 cạnh nó thì không.
        # Vá 2026-08-02: TỰ đổi sang .jpg thay vì chỉ cảnh báo "set tay". Trước đó việc set tay được
        # làm bằng cách copy .jpg ĐÈ lên tên .png → file JPEG mang đuôi .png nằm trong gói upload.
        src, ext = tp, tp.suffix
        alt = tp.with_suffix(".jpg")
        if tp.stat().st_size > 2 * 1024 * 1024 and alt.exists() and alt.stat().st_size <= 2 * 1024 * 1024:
            src, ext = alt, ".jpg"
        dest = pack / (f"thumbnail{ext}" if n == 1 else f"thumbnail_T{n}{ext}")
        # dọn bản cùng vai nhưng khác đuôi (đổi png<->jpg giữa 2 lần gói thì không để lại 2 file)
        other = dest.with_suffix(".jpg" if ext == ".png" else ".png")
        if other.exists():
            other.unlink()
        if not dest.exists() or dest.stat().st_mtime < src.stat().st_mtime:
            link_or_copy(src, dest)
        ab_packed.append(dest.name)
        if dest.stat().st_size > 2 * 1024 * 1024:
            warns.append(f"{dest.name} nặng {dest.stat().st_size/1048576:.2f} MB > trần 2 MB của YouTube"
                         " — xuất bản .jpg q95 cạnh file gốc rồi gói lại")
    # ⚠️ CHỈ dùng fallback khi bộ A/B KHÔNG cấp được bản T1 (bug 2026-08-02: video 15 có bộ A/B
    # nhưng folder còn sót `thumbnail.png` của bản render đầu ĐÃ BỊ LOẠI → dòng này ghi đè T1
    # bằng đúng bản bị loại, im lặng). Chỉ định tay bằng --thumb thì vẫn thắng.
    if thumb and (a.thumb or not {"thumbnail.png", "thumbnail.jpg"} & set(ab_packed)):
        # 🔴 GIỮ ĐÚNG ĐUÔI của nguồn. Trước đây ép cứng ".png" ⇒ khi nguồn là .jpg (nhánh
        # vượt trần 2 MB ở trên) thì gói ra file tên .png nhưng RUỘT LÀ JPEG — sai kiểu file.
        link_or_copy(thumb, pack / ("thumbnail" + thumb.suffix.lower()))

    # --- ghi chú bộ A/B (chỉ hiện khi thật có nhiều bản) ---
    ab_thumb_note = ""
    packed_thumbs = sorted(p for p in pack.iterdir()
                           if p.name.startswith("thumbnail") and p.suffix.lower() in (".png", ".jpg"))
    # T1 = bản đứng tên "thumbnail.*" (png hoặc jpg khi PNG vượt trần 2 MB)
    # 🔴 Vá 2026-08-28: fallback "thumbnail.png" nói dối khi KHÔNG có bản T1 — video chỉ có
    # T2/T3 thì gói ra "thumbnail_T2.jpg" (không có file nào tên thumbnail.png), nhưng
    # METADATA.txt [6] vẫn in "thumbnail.png trong folder này" → tìm sai tên. Fallback đúng
    # là bản ĐẦU TIÊN thật sự có trong gói (packed_thumbs đã sorted), không phải chuỗi cứng.
    main_thumb_name = next((p.name for p in packed_thumbs if p.stem == "thumbnail"),
                           packed_thumbs[0].name if packed_thumbs else "thumbnail.png")
    _need_thumbs = 3          # 3×3 bật lại cho mọi kênh 2026-08-13 (xem ghi chú gate title)
    if len(packed_thumbs) < _need_thumbs:
        warns.append(f"🔴 GATE 3×3: chỉ gói được {len(packed_thumbs)}/{_need_thumbs} thumbnail A/B — "
                     "render đủ thumb_T1_*.png / thumb_T2_*.png / thumb_T3_*.png (mỗi bản đổi ĐÚNG "
                     "1 biến) trong folder video (.claude/rules/ab-3title-3thumb.md)")
    if len(packed_thumbs) > 1:
        ab_thumb_note = ("\n    BỘ A/B — Studio → video → Thumbnail → \"Test & compare\", nạp cả "
                         + str(len(packed_thumbs)) + " ảnh:\n")
        for tp in packed_thumbs:
            ab_thumb_note += "         - " + tp.name + "\n"
        ab_thumb_note += ("       Test chỉ áp cho THUMBNAIL. GIỮ NGUYÊN TITLE suốt thời gian test\n"
                          "       (>=7 ngày) — đổi title giữa lúc test là lẫn 2 biến, kết quả vô nghĩa.")
    ab_title_note = ""
    if len(ctr.get("ab_titles") or []) > 1:
        ab_title_note = "\n\n    3 TITLE A/B (KHÔNG test song song được — đổi TUẦN TỰ, mỗi bản >=7 ngày):\n"
        for _i, (_tag, _t) in enumerate(ctr["ab_titles"]):
            ab_title_note += "       [" + _tag + "] " + _t + ("  <-- DÙNG KHI ĐĂNG" if _i == 0 else "") + "\n"

    # 🔴 GATE MÔ TẢ (2026-08-08) — ô [3] trống thì phải HÉT tại chỗ, không chỉ ghi ở cuối file.
    # Ca gốc: chouhen 19 gói ra ô [3] rỗng; 2 dòng cảnh báo nằm cuối METADATA.txt nên trôi mất,
    # suýt đăng một video 36' với 概要欄 trống (mất sạch tín hiệu SEO của youtube-upload-seo.md).
    if not (description or "").strip():
        description = (
            "🔴🔴 THIẾU MÔ TẢ — ĐỪNG ĐĂNG VỚI Ô NÀY TRỐNG 🔴🔴\n"
            "Parser không tìm thấy mục 概要欄 trong script. Cách sửa:\n"
            "  1. Trong file script, viết 2 heading + code fence ```:\n"
            "       ### 概要欄 — 3 dòng đầu     (nói về gì / cho ai / được gì — cấm lời chào)\n"
            "       ### 概要欄 — mô tả đầy đủ   (200–300 từ theo timeline + 目次 + credit + hashtag)\n"
            "  2. Chạy lại: upload_pack.py <slug> --channel <key> --force\n"
            "Rule: .claude/rules/youtube-upload-seo.md §2.2 (3 dòng vàng) + §2.3 (mô tả đầy đủ)")

    meta = pack / "METADATA.txt"
    with meta.open("w", encoding="utf-8-sig", newline="\n") as f:
        f.write(f"""====== GÓI UPLOAD — {a.slug} ======
Kênh   : {cfg['name']} ({a.channel})
Tạo lúc: {datetime.now():%Y-%m-%d %H:%M}
Nguồn  : {script}

[1] VIDEO — kéo thả file này vào YouTube Studio:
    {upload_name}

[2] TITLE — copy nguyên dòng giữa 2 vạch:
--------------------------------------------------
{title}
--------------------------------------------------{ab_title_note}

[3] DESCRIPTION (概要欄) — copy cả khối giữa 2 vạch:
--------------------------------------------------
{description}
--------------------------------------------------

[4] TAGS — dán vào ô Tags (đã là danh sách phẩy):
--------------------------------------------------
{tags_line}
--------------------------------------------------

[5] PHỤ ĐỀ: upload file subs.srt trong folder này (Subtitles → Add → Upload file).
[6] THUMBNAIL: {main_thumb_name} trong folder này.{ab_thumb_note}
[7] HẸN GIỜ (Schedule): {fmt_slot(slot, cfg)}
    (theo .claude/rules/upload-schedule.md — đăng trước peak 2–3h)

[8] CHECKLIST trước khi bấm Schedule:
""")
        for c in cfg["checklist"]:
            f.write(f"    [ ] {c}\n")
        if cfg.get("playlist"):
            f.write(f"    [ ] Playlist: {cfg['playlist']}\n")
        f.write("    [ ] End screen 20s cuối: trỏ 1 video cùng kênh + nút đăng ký (làm trong Studio, không có API)\n")
        # 🔴 Ô [9] LUÔN IN, kể cả khi rỗng. Trước đây nó nằm trong `if ctr.get("pinned")`
        #    nên thiếu là biến mất luôn khỏi METADATA.txt — người dán không có cách nào
        #    biết mình đang thiếu một bước. Cùng bài học ô [3] ở `youtube-upload-seo.md` §4:
        #    cảnh báo đặt cuối file dài thì trôi, nó phải nằm ĐÚNG Ô sắp copy.
        if ctr.get("pinned"):
            f.write(f"""
[9] PINNED COMMENT — sau khi video công khai, dán làm bình luận ghim:
--------------------------------------------------
{ctr['pinned']}
--------------------------------------------------
""")
        else:
            f.write("""
[9] PINNED COMMENT
--------------------------------------------------
🔴🔴 THIẾU — ĐỪNG ĐĂNG MÀ BỎ TRỐNG Ô NÀY.
Thêm vào script một khối:

    ### Pinned comment
    ```
    <nội dung bình luận ghim>
    ```

rồi chạy lại lệnh đóng gói. Bình luận ghim là chỗ RẺ NHẤT để xin comment,
và comment sớm là tín hiệu của cú đẩy 24–48h đầu (rules/cta-midvideo.md §0).
--------------------------------------------------
""")
        if warns:
            f.write("\n⚠️ CẢNH BÁO:\n")
            for w in warns:
                f.write(f"    - {w}\n")

    # --- 6. Báo cáo ---
    print(f"✅ Gói upload: {pack}")
    print(f"   video    : {upload_name} ({mp4.stat().st_size/1024/1024:.0f} MB, hardlink)")
    print(f"   srt      : {'OK' if srt.exists() else 'THIẾU'}   thumbnail: {'OK' if thumb or ab_packed else 'THIẾU'}{f' (bộ A/B {len(ab_packed)} bản)' if len(ab_packed)>1 else ''}")
    print(f"   title    : {title[:60]}…")
    print(f"   hẹn giờ  : {fmt_slot(slot, cfg)}")
    for w in warns:
        print(f"   ⚠️ {w}")
    if a.open:
        os.startfile(pack)  # noqa — Windows only
        open_studio(a.channel)
    # [9] = PINNED COMMENT, dán SAU khi video công khai — đừng để nó ngoài dòng hướng dẫn,
    # vì người dán làm đúng theo dòng này và sẽ dừng ở [8] (đó là cách nó khuyết bấy lâu).
    print("→ Mở METADATA.txt, kéo thả + copy-paste theo thứ tự [1]→[8], "
          "rồi dán [9] PINNED COMMENT sau khi video công khai. ~2–3 phút/video.")


if __name__ == "__main__":
    main()
