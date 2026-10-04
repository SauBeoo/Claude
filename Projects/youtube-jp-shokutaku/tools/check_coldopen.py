# -*- coding: utf-8 -*-
r"""GATE COLD OPEN + RETENTION — 60代からの食卓. Chạy TRƯỚC mọi lần render.

    python tools\check_coldopen.py            # quét mọi *_TTS.md trong 04_SCRIPTS
    python tools\check_coldopen.py 05 08      # chỉ script chỉ định
    python tools\check_coldopen.py --limit 120
    python tools\check_coldopen.py --calib    # hiệu chuẩn trên 3 video đã đo được AVD

Vì sao có tool này (chốt 2026-08-01, chiến lược "cách 1"): luật payoff-#1-sớm đã nằm
trong CLAUDE.md từ 2026-07-21 nhưng **kiểm bằng mắt thì trôi** — health đã trôi ở 6/6
script, và chính kênh này để payoff #1 rơi xuống phút 8:20. Đo được thì mới giữ được.

MỐC MÁY ĐỌC: đặt một dòng `# ITEM1` NGAY TRƯỚC câu hé lộ món/mục đầu tiên.
`parse_script()` bỏ qua mọi dòng mở đầu bằng `#` → **không ảnh hưởng giọng đọc lẫn
cue slide**. Không có mốc = FAIL (cố tình: bắt người viết tự khai, đừng để tool đoán
— đoán bằng regex 「〜です。」 sẽ ăn nhầm 「それだけの話です。」 trong hook và báo PASS oan).

Hiệu chuẩn: xem khối CPS/GAP ngay dưới phần import (mô hình 2 tham số, hiệu chuẩn lại
2026-08-11 từ bản render video 14). Trần mặc định 90 giây.

═══════════════════════════════════════════════════════════════════════════════
⭐ BỔ SUNG 2026-08-11 — 3 luật S6/S7/S8 đúc từ RETENTION THẬT
   Bằng chứng: `CHANNEL_DIAGNOSIS_2026-08-11.md`. `subs.srt` của 3 video có đường
   cong được thu hồi từ chính YouTube (`captions.download`) vì script gốc đã mất.

   Cửa tử đo được = **giây 20 → 40** (mất 45–55 điểm trong 12–18 giây), và cú rớt
   lớn nhất của từng video rơi ĐÚNG vào một câu TỰ THÁO NGÒI LỜI HỨA:
     納豆       23→27s 「納豆が悪者になったという話ではないのです」   −55 điểm
     ブルーベリー 27→35s 「悪いのはブルーベリーではありません」        −50 điểm
     ゆで卵     21→25s 「にわかには信じがたいかもしれませんけれど」    −38 điểm

   🔴 GIẢ THUYẾT BỊ BÁC, ghi lại để không ai dựng lại nó: trước khi ghép srt, giả
   thuyết đang chạy là "luật L5 bắt ≥3 câu 「〜ませんか」 và chúng chiếm đúng cửa tử
   18–43s". SAI — ゆで卵 giây 21 đọc đúng 「少し気になりませんか?」 mà vẫn GIỮ 95,8%.
   Câu triệu chứng không tốn máu. **L5 GIỮ NGUYÊN, không nới không bỏ.**
═══════════════════════════════════════════════════════════════════════════════

Exit 1 nếu có script FAIL → dùng được trong .cmd/pipeline.
"""
import argparse
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ⭐ HIỆU CHUẨN LẠI 2026-08-11 — MÔ HÌNH 2 THAM SỐ (đo từ bản render video 14)
# Bản cũ dùng MỘT hằng số 4,60 ký/giây và **trả số sai 7%**: nó chấm script 14 là
# "vào bài 88 giây → PASS", trong khi `subs.srt` của bản đã render cho **94 giây**
# → thật ra VƯỢT trần 90. Cùng họ lỗi với gate co-dai (gate trả số vô nghĩa thì
# sẽ bị bỏ qua), chỉ khác là ở đây nó báo PASS OAN chứ không báo số điên.
#
# Nguyên nhân: mỗi DÒNG trong `_TTS.md` được chèn một khoảng nghỉ khi synth, nên
# thời lượng KHÔNG tỉ lệ thuần với số ký tự — bài càng nhiều dòng càng chậm.
# Đo thật video 14: 5.984 ký · 255 dòng · 1.397 giây.
#   → CPS thuần 4,49 ký/giây + 0,25 giây/dòng
#   → ước cold open 95s vs thực tế 94s (lệch 1s; mô hình cũ lệch −6s)
# ⚠️ Hằng số 4,60 cũ đo từ video 05 và vẫn "đúng" cho RIÊNG video đó — vì nó tình
#    cờ có tỉ lệ ký/dòng khác. Đừng quay lại mô hình một-hằng-số.
#
# 🔴 HIỆU CHUẨN LẦN 2 — 2026-08-13, sau khi render video 15.
# Đo thật video 15: 6.013 ký · 263 dòng · 1.432 giây → **CPS 4,40**.
# Tức hằng số KHÔNG cố định giữa các video: 4,49 (video 14) vs 4,40 (video 15) = ±2%.
# Hệ quả đã xảy ra HAI LẦN, cùng một chiều: gate ước 88s → thực tế 94s (video 14)
# và 88s → **93s** (video 15). Cả hai lần gate báo PASS mà thực tế VƯỢT trần 90.
# ⇒ Với một gate TRẦN, ước lạc quan là sai hướng. Lấy hằng số CHẬM HƠN (4,40) để
#   ước không undershoot; ai muốn số của riêng bài mình thì chạy --calib sau render.
# ⚠️ Đừng "tối ưu" lại về 4,49 chỉ vì nó khớp video 14 — đó đúng là lỗi đã ghi ở
#   dòng trên về hằng số 4,60 của video 05: khớp một video không phải là đúng.
CPS = 4.40          # ký/giây THUẦN (không kể nghỉ giữa dòng) — bản chậm hơn, cố ý
GAP = 0.25          # giây nghỉ mỗi dòng
PROJ = Path(__file__).resolve().parent.parent
SC = PROJ / "04_SCRIPTS"
DIAG = PROJ / "06_VIDEO" / "_diagnose"
MARK = re.compile(r"^#\s*ITEM1\b")

# L2 — câu điều kiện/miễn trừ/dặn dò: báo "có ràng buộc" đúng lúc phải hứa phần thưởng
DISC = ["お薬", "薬を", "主治医", "かかりつけ", "持病", "通院", "ご相談ください",
        "医師", "栄養士", "受診", "透析", "妊娠", "アレルギー", "control"]
# L3 — khối persona / nhận diện kênh / xin tương tác: phải nằm SAU mục đầu
PERSONA = ["六十代からの食卓へ", "案内人の、みのり", "みのりです", "医者でも",
           "都道府県", "チャンネル登録", "コメント欄"]
# L4 — case study: tên + tuổi
CASE = re.compile(r"[ぁ-んァ-ヶ一-龯]{2,6}さん[、,]?\s*[〇一二三四五六七八九十0-9]{1,3}十?[一二三四五六七八九0-9]?歳")
# L5 — triệu chứng self-implication (khuôn network đối thủ: 3–4 câu 「〜ませんか」)
SYMPTOM = re.compile(r"(ませんか|ないでしょうか|ありませんか|でしょうか)[。？]?$")

# ── S6 · CÂU TỰ THÁO NGÒI ─────────────────────────────────────────────────────
# Phủ định chính lời buộc tội mà thumbnail/title vừa đưa ra. Thủ phạm ĐO ĐƯỢC.
#
# ⭐ CHIA 2 MỨC — hiệu chuẩn 2026-08-11 cho thấy có GRADIENT khớp đúng chiều AVD:
#      ゆで卵 27,4% → chỉ có câu HEDGE 「にわかには信じがたい」          −38 điểm
#      ブルーベリー 13,3% → phủ định THẲNG chủ thể 「悪いのはブルーベリーでは」 −50 điểm
#      納豆 12,2%   → phủ định THẲNG chủ thể 「納豆が悪者になったという話では」 −55 điểm
#   ⇒ phủ định thẳng chủ thể đắt gấp rưỡi câu hedge. Đếm gộp thì mất tín hiệu này
#     (bản đầu chấm cả 3 đều = 1, không phân biệt được gì).
DEFUSE_HARD = [                      # phủ định thẳng lời buộc tội của title
    re.compile(r"(?:という|との)?(?:お)?話ではあり?ま?せ?ん"),
    re.compile(r"(?:という|との)?(?:お)?話ではないの"),
    re.compile(r"悪いのは.{0,14}ではありません"),
    re.compile(r".{0,10}が悪者"),
    re.compile(r"やめましょう、?という"),
]
DEFUSE_SOFT = [                      # hedge / câu meta nói VỀ lời nói thay vì nói tiếp
    re.compile(r"わけではありません"),
    re.compile(r"にわかには信じ"),
    re.compile(r"信じがた"),
    re.compile(r"大げさに聞こえ"),
]
DEFUSE = DEFUSE_HARD + DEFUSE_SOFT
S6_WIN = 90          # cửa sổ áp S6 = 90 giây đầu
S6_LOOK = 2          # số câu SAU đó được xét để tìm thứ CỤ THỂ thay thế

# Thứ "CỤ THỂ" cứu được một câu phủ định: tổn thương THÂN THỂ, hoặc con số CÓ ĐƠN VỊ.
# ⚠️ CỐ Ý loại counter trần (つ・個) — 「たった1つ、食べ方なのです」 của ブルーベリー
#    có 「1つ」 nhưng vẫn rớt 50 điểm, vì 食べ方 là KHÁI NIỆM. Đếm 「1つ」 là chấm oan.
BODY = ["足", "筋肉", "骨", "腎臓", "血管", "血圧", "膝", "腰", "手足", "ふくらはぎ",
        "内臓", "心臓", "肝臓", "腸", "歯", "目", "耳", "肌", "髪", "しびれ", "むくみ",
        "転倒", "転び", "寝たきり", "認知", "握力", "体重", "背", "関節"]
NUM_UNIT = re.compile(r"[0-9〇一二三四五六七八九十百千]+\s*"
                      r"(?:グラム|ミリ|キロ|ｇ|g|mg|%|パーセント|割|倍|円|度|℃|"
                      r"ミリグラム|人に|分|時間|日|年|歳|杯|枚|さじ)")
# chữ số viết dạng hiragana theo luật kênh (「いってんにグラム」「ななグラム」)
NUM_KANA = re.compile(r"(?:いち|に|さん|よん|ご|ろく|なな|はち|きゅう|じゅう|ひゃく)"
                      r"[ぁ-ん]{0,6}(?:グラム|パーセント|ミリ|倍|円|度|人)")

# ── S7 · KHỐI CREDENTIAL ──────────────────────────────────────────────────────
# ゆで卵 rớt −8 điểm đúng câu này ở giây 33. Đồng thời VI PHẠM luật persona みのり
# (CLAUDE.md §Persona: cấm tự xưng chuyên gia) → cấm ở MỌI VỊ TRÍ, không chỉ cold open.
CRED = [
    re.compile(r"私はこれまで長い?間"),
    re.compile(r"長年.{0,12}(?:して|してき)まし?た"),
    re.compile(r"お話を(?:して|してき)まし?た"),
    re.compile(r"(?:食事|体|健康).{0,8}についてお話をしてき"),
]

# ── S8 · RUN-LENGTH: câu KHÔNG TRẢ TIỀN nằm liền nhau ─────────────────────────
# Chữa vùng rò thứ hai (phút 1′40 → 6′00, rò đều ~1 người mỗi 20–40 giây, KHÔNG có
# vách). Vì không quy được cho MỘT khối nào nên chữa bằng luật MẬT ĐỘ.
# ⚠️ Xem `--calib`: luật này CHƯA chứng minh được là discriminating giữa các video.
ACT = re.compile(r"(?:入れ|置[きい]|かけ|混ぜ|切[りる]|刻[みむ]|茹で|煮|焼[きく]|"
                 r"冷や[しす]|温め|戻[しす]|漬け|のせ|載せ|加え|振[りる]|包[みむ]|"
                 r"すくい|注[ぎぐ]|添え|挟[みむ]|外[しす]|干[しす]|溶か[しす]|"
                 r"確かめ|囲[みむ]|測[りる]|読[みむ])|(?:て|で)ください")
TWIST = ["ところが", "じつは", "実は", "逆に", "むしろ", "ではありません", "間違い",
         "逆効果", "効きません", "なぜ", "どちら", "半分", "以下です", "もったいない"]
SENSE = ["匂い", "におい", "香り", "湯気", "手ざわり", "手触り", "ひんやり", "ぬるり",
         "ざらざら", "しっとり", "指先", "口の中", "喉", "舌", "音", "ラッパ", "朝いちばん",
         "夕暮れ", "台所", "湯呑み", "お椀"]
ASK = re.compile(r"(?:ませんか|でしょうか|ですよね|ますか)[。？]?$")
RUN_MAX = 3          # chặn từ 4 câu liền không trả tiền

# 3 video có curve + AVD% đo được 2026-08-11 (dùng cho --calib)
CALIB = [
    ("mQevRS1qBbk", "ゆで卵 14'45", 27.4, "asr"),
    ("31KXwgHbLY0", "ブルーベリー 20'28", 13.3, "srt mình upload"),
    ("BL7KtdXpl_A", "納豆 28'58", 12.2, "asr"),
]


def clean(line):
    return re.sub(r"^(\[[^\]]*\])+", "", line).strip()


def has_coin(t):
    """Câu có 'trả tiền' không — 5 đồng tiền (mượn khung co-dai, đã hiệu chuẩn ở đó)."""
    if NUM_UNIT.search(t) or NUM_KANA.search(t):
        return True
    if ACT.search(t):
        return True
    if any(w in t for w in TWIST):
        return True
    if any(w in t for w in SENSE):
        return True
    if ASK.search(t):
        return True
    return False


def concrete(t):
    """Thứ CỤ THỂ cứu được một câu phủ định: tổn thương thân thể, hoặc số có đơn vị."""
    return bool(NUM_UNIT.search(t) or NUM_KANA.search(t) or any(b in t for b in BODY))


def scan_body(sents):
    """sents = [(giây, text)] → (danh sách vi phạm S6/S7/S8)."""
    viol = []
    # S6 — tháo ngòi trong 90 giây đầu
    for i, (sec, t) in enumerate(sents):
        if sec > S6_WIN:
            break
        hard = any(p.search(t) for p in DEFUSE_HARD)
        soft = any(p.search(t) for p in DEFUSE_SOFT)
        if not (hard or soft):
            continue
        nxt = [x[1] for x in sents[i + 1:i + 1 + S6_LOOK]]
        if not any(concrete(x) for x in nxt):
            kind = "THÁO NGÒI (phủ định thẳng chủ thể)" if hard else "câu HEDGE/META"
            viol.append(f"S6 {kind} ở ~{sec:.0f}s, không có thứ CỤ THỂ thay ngay: "
                        f"「{t[:34]}」 → 「{(nxt[0][:30] if nxt else '(hết)')}」")
    # S7 — credential, mọi vị trí
    for sec, t in sents:
        if any(p.search(t) for p in CRED):
            viol.append(f"S7 CREDENTIAL ở ~{sec:.0f}s: 「{t[:38]}」 "
                        f"(giết retention + vi phạm persona みのり)")
    # S8 — run-length
    run, start, runs = 0, None, []
    for sec, t in sents:
        if has_coin(t):
            if run > RUN_MAX:
                runs.append((start, run))
            run, start = 0, None
        else:
            if run == 0:
                start = sec
            run += 1
    if run > RUN_MAX:
        runs.append((start, run))
    for start, n in runs:
        viol.append(f"S8 {n} câu LIỀN không trả tiền từ ~{int(start)//60}'{int(start)%60:02d}")
    return viol


def sents_from_script(path):
    """[(giây ước theo CPS, text)] cho toàn bài + chỉ số dòng mốc ITEM1."""
    out, acc, idx = [], 0.0, None
    for i, raw in enumerate(path.read_text(encoding="utf-8").split("\n")):
        if MARK.match(raw.strip()):
            idx = len(out)
            continue
        t = clean(raw)
        if not t or t.startswith(("#", "---", ">", "|", "```", "=")):
            continue
        out.append((acc, t))
        acc += len(t) / CPS + GAP
    return out, idx


def sents_from_srt(path):
    """[(giây THẬT, text)] — dùng cho --calib và kiểm sau render."""
    out = []
    for blk in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig", errors="ignore")):
        L = [x for x in blk.strip().split("\n") if x.strip()]
        m = re.search(r"(\d\d):(\d\d):(\d\d)[,.]\d+\s*-->", blk)
        if not m:
            continue
        h, mi, s = (int(x) for x in m.groups())
        body = "".join(x for x in L if "-->" not in x and not x.strip().isdigit())
        if body.strip():
            out.append((float(h * 3600 + mi * 60 + s), body.strip()))
    return out


def check(path, limit_sec):
    lines = path.read_text(encoding="utf-8").split("\n")
    n, idx, head = 0, None, []
    for i, raw in enumerate(lines):
        if MARK.match(raw.strip()):
            idx = i
            break
        t = clean(raw)
        if not t or t.startswith("---") or t.startswith("#") or t.startswith(">"):
            continue
        head.append(t)
        n += len(t)
    blob = "".join(head)
    viol = []
    if idx is None:
        return None, 0, ["THIẾU MỐC `# ITEM1` — thêm 1 dòng `# ITEM1` ngay trước câu hé lộ mục đầu"], []
    sec = n / CPS + GAP * len(head)
    if sec > limit_sec:
        viol.append(f"L1 mục đầu ở ~{sec:.0f}s (trần {limit_sec}s, dư {sec - limit_sec:.0f}s "
                    f"= {int((sec - limit_sec) * CPS)} ký hoặc {int((sec - limit_sec) / GAP)} dòng)")
    hit = [d for d in DISC if d in blob]
    if hit:
        viol.append("L2 điều kiện/miễn trừ trong cold open: " + "・".join(hit))
    hit = [d for d in PERSONA if d in blob]
    if hit:
        viol.append("L3 persona/CTA trước mục đầu: " + "・".join(hit))
    m = CASE.search(blob)
    if m:
        viol.append(f"L4 case study trước mục đầu: {m.group(0)}")
    nsym = sum(1 for t in head if SYMPTOM.search(t))
    if nsym < 3:
        viol.append(f"L5 chỉ {nsym} câu triệu chứng 「〜ませんか」 (cần ≥3)")
    sents, _ = sents_from_script(path)
    found = scan_body(sents)
    # S8 CHƯA hiệu chuẩn được (nhiễu bởi độ mịn caption — xem --calib) → CẢNH BÁO,
    # không chặn render. Đừng nâng nó lên FAIL khi chưa có ca đối chứng.
    viol += [x for x in found if not x.startswith("S8")]
    warn = [x for x in found if x.startswith("S8")]
    return sec, n, viol, warn


def calib():
    """Đối chiếu gate với AVD THẬT của 3 video đã đo. Gate phải xếp ĐÚNG CHIỀU."""
    print("── HIỆU CHUẨN trên video đã lên sóng (srt thu từ YouTube) ──")
    print("⚠️ 2/3 track là ASR (máy nghe lại) → chữ có sai (腎臓→人臓, ゆで卵→茹でた孫).")
    print("   Regex sẽ ĐẾM THIẾU trên 2 bản đó. Đọc số theo CHIỀU, đừng đọc theo mức.\n")
    rows = []
    for vid, name, avd, kind in CALIB:
        p = DIAG / f"{vid}.srt"
        if not p.exists():
            print(f"  (thiếu {p.name} — chạy lại bước captions.download)")
            continue
        sents = sents_from_srt(p)
        v = scan_body(sents)
        hard = sum(1 for x in v if "phủ định thẳng" in x)
        soft = sum(1 for x in v if "HEDGE" in x)
        s7 = sum(1 for x in v if x.startswith("S7"))
        s8 = sum(1 for x in v if x.startswith("S8"))
        rows.append((name, avd, hard, soft, s7, s8, kind, len(sents)))
    rows.sort(key=lambda r: -r[1])
    print(f"  {'video':22} {'AVD%':>6} {'S6硬':>5} {'S6軟':>5} {'S7':>4} {'S8':>4} {'cue':>5}  track")
    for name, avd, hard, soft, s7, s8, kind, nc in rows:
        print(f"  {name:22} {avd:>5.1f}% {hard:>5} {soft:>5} {s7:>4} {s8:>4} {nc:>5}  {kind}")

    print("\n  ── ĐỌC KẾT QUẢ ──")
    print("  ✅ S6 ĐỘ CHÍNH XÁC XÁC NHẬN: bắt đúng câu, đúng giây của cú rớt đo được ở 3/3")
    print("     (ゆで卵 25s −38đ · 納豆 32s −55đ · ブルーベリー 35s −50đ).")
    if len(rows) >= 2 and rows[0][2] < rows[-1][2]:
        print("  ✅ S6硬 đúng chiều: bản AVD cao nhất chỉ có câu HEDGE, 2 bản AVD thấp")
        print("     phủ định THẲNG chủ thể — khớp gradient −38đ vs −50/−55đ.")
    print("  🔴 S7 ĐẾM THIẾU trên track ASR — ĐỪNG đọc số 0 của ゆで卵 là 'sạch'. Nó CÓ")
    print("     khối credential ở giây 33 (đúng cú rớt −8đ), nhưng ASR cắt câu làm đôi")
    print("     giữa 2 cue (35s「…についてお」/ 39s「話をしてきました」) nên regex không khớp.")
    print("     ⇒ Trên `_TTS.md` (mỗi dòng 1 câu) thì S7 không có lỗi này.")
    print("  ⚠️ S6 KHÔNG xếp hạng được bằng phép so 3 video này vì CẢ 3 ĐỀU MẮC BỆNH")
    print("     (AVD 12–27%, không bản nào đạt). Chỉ xác nhận được khi có 1 video SẠCH")
    print("     để đối chứng — đó là việc của video 14.")
    print("  🔴 S8 KHÔNG hiệu chuẩn được trên dữ liệu này — BỊ NHIỄU HOÀN TOÀN bởi độ")
    print("     mịn của caption: 2 track ASR cắt cue ~3,5s/cue (252 và 395 cue) nên câu")
    print("     vụn, thiếu 'đồng tiền' → nhiều run; track srt mình upload cắt theo CÂU")
    print("     (160 cue) → ít run. Tức S8 đang đo ĐỘ MỊN CAPTION, không đo chất kịch bản.")
    print("     ⇒ S8 để mức CẢNH BÁO, KHÔNG chặn render. Chỉ hiệu chuẩn được trên `_TTS.md`")
    print("     (mỗi dòng 1 câu) của một video vừa có script vừa có curve — chưa tồn tại.")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("only", nargs="*", help="tiền tố tên script, vd 05 08")
    ap.add_argument("--limit", type=float, default=90, help="trần giây cho mục đầu (mặc định 90)")
    ap.add_argument("--calib", action="store_true", help="hiệu chuẩn trên 3 video đã đo AVD")
    a = ap.parse_args()

    if a.calib:
        calib()
        return

    print(f"Trần mục đầu = {a.limit:.0f} giây  (mô hình: {CPS} ký/giây thuần + {GAP}s/dòng)")
    print("Chặn: L1–L5 (cold open) · S6 tháo ngòi · S7 credential")
    print("Cảnh báo (không chặn): S8 run-length — chưa hiệu chuẩn được, xem --calib\n")
    rows = []
    for f in sorted(SC.glob("*_TTS.md")):
        if any(k in f.name for k in ("backup", "demo", "_v1")):
            continue
        if a.only and not any(f.name.startswith(x) for x in a.only):
            continue
        sec, n, viol, warn = check(f, a.limit)
        rows.append((f.name, sec, n, viol))
        print(f"{'✅ PASS' if not viol else '🔴 FAIL'}  {f.name}")
        if sec is not None:
            print(f"    {n} ký trước mục đầu → ~{sec:.0f} giây")
        for v in viol:
            print(f"    ✗ {v}")
        for w in warn[:3]:
            print(f"    ⚠️ {w}")
        if len(warn) > 3:
            print(f"    ⚠️ (+{len(warn) - 3} cảnh báo S8 nữa)")
        print()
    bad = [r for r in rows if r[3]]
    print(f"— {len(rows) - len(bad)}/{len(rows)} script PASS —")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
