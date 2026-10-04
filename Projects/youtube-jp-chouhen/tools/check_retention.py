# -*- coding: utf-8 -*-
"""
check_retention.py — GATE RETENTION cho kênh 真夜中の朗読便 (chouhen).

Đo 11 số của công thức RETENTION-A (`RETENTION_FORMULA_2026-08-11.md`), đúc từ Analytics API
2026-08-11 trên 9 video. Ý gốc: **đồng hồ khán giả chạy bằng PHÚT, không bằng phần trăm** —
6/6 video có cú lật đầu trước phút 16 thì retention TĂNG ở quãng 11′→16′; 6/6 video không có
thì GIẢM. Khung 9 nhịp cũ tính theo % nên ở bài 55′ nó đẩy thác trả thù tới phút 25–28 = trễ
16 phút so với lúc khán giả bỏ đi.

CHẠY:
  python tools/check_retention.py 12_gibo-rikontodoke              # sau render (đo srt thật)
  python tools/check_retention.py 21_hachinen-no-yachin --pre      # trước render (ước từ _TTS.md)
  python tools/check_retention.py <slug> --waves 11:41,14:44,18:21 --loop-close 21:59

HARD FAIL (exit 1): **R3b** (câu lời kể trong giây 16–35) · R7 (gap beat >2′45) · R8 (SÓNG 1 sau
phút 12) · R11 (loop cold open đóng trước 78%). Đó là các số có cơ chế nhân quả đo được. Còn lại
in cảnh báo — R3/R5 dò bằng từ khoá nên LUÔN phải duyệt mắt transcript 90 giây tool in ra.

🔴 **CỬA TỬ THẬT LÀ GIÂY 16–35** (retention 1%, đo 2026-08-11): video 12 giây 16 = **96,7%** →
giây 33 = **73,0%**; video 09 giây 24 = **100,6%** → giây 48 = **57,6%**. Gần như không ai bỏ đi
trong 16 giây đầu ⇒ toàn bộ cú giết gói trong ~17 giây. Câu giết video 09 ở giây 32 là một câu
LỜI KỂ giải thích. Và giây 82 của video 12 **hồi +3,3đ** ngay sau câu phản đòn ở giây 71 ⇒ R5
không chỉ giữ người, nó KÉO NGƯỜI QUAY LẠI.

⚠️ **HAI TẦNG NGƯỠNG, cố ý:** R6 và R8 chặn ở mức *đã chứng minh xấu* (回想 >2′30 · sóng 1 sau
phút 12) và chỉ **cảnh báo** ở mức *mục tiêu >60%* (回想 = 0 · sóng 1 ≤ phút 8). Lý do: video 12
CÓ 回想 2′20 và sóng 1 ở 11′41 mà vẫn đạt AVD 55,7% — chặn ở mức mục tiêu là **fail chính bản
thắng**, đúng cái bẫy đã mắc một lần với R11 (đặt 85% → fail video 12, phải hạ về 78%).

CẤU HÌNH NHẮM AVD >60% (dài 24–26′): bỏ HẲN 回想 → mở bài 8′ · SÓNG 1 phút 7–8 · phản đòn ~giây
50 · anomaly ≤giây 20 · kết 2′30. Căn cứ: video 12 ngày 1 đã có **15,34 phút xem**; bỏ 2′20 回想
đưa 27′34 → 25′14 ⇒ 15,34/25,23 = **60,8%** mà không cần giữ người giỏi hơn một giây nào.
⚠️ AVD 60% ở bài 52′ đòi **31,2 phút xem** = 2× kỷ lục kênh ⇒ **>60% và bài 50′+ loại trừ nhau.**

⚠️ R9/R10 cần biết SÓNG nằm ở đâu. Tool tự dò theo dấu 逆転 trong 目次 (khuôn video 09); bài
nào không đánh số thì truyền `--waves`. Đánh số 逆転①..⑤ trong 目次 chính là một phần của luật
(§3.5) nên "không dò được" là một phát hiện, không phải lỗi tool.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJ = Path(__file__).resolve().parent.parent

# ── Từ khoá dò cold open ──────────────────────────────────────────────────────
# R2 — vật chứng/giấy tờ. Đây là "vũ khí im lặng" của ngách: cả 2 video thắng đều
# document-driven (CLAUDE.md: cơ chế thắng = 供給停止型 + 書類で詰める).
DOCS = ("離婚届", "遺言", "登記", "委任状", "診断書", "通知", "ハガキ", "葉書", "手帳", "間取り帖",
        "契約", "領収", "明細", "証書", "通帳", "印鑑", "実印", "署名", "書類", "念書", "借用",
        "見積", "請求", "戸籍", "保険証", "定期預金", "注文控え", "予約確認", "当番表", "判こ", "判子",
        # bổ sung 2026-08-14 (video 26): R2 báo 🔴 oan vì bảng chỉ có 離婚届 mà không có
        # 退職届 — giấy tờ mở màn của bài đó được gọi tên ở giây 4, tool bắt nhầm 明細 ở giây 30.
        # Thêm keyword chỉ làm gate NHẠY HƠN, không nới lỏng bất kỳ ngưỡng nào.
        "退職届", "変更届", "届出", "許可証", "免許", "原簿", "引き継ぎ表", "発注書", "給与明細",
        "是正勧告", "納品書", "誓約書", "覚書", "取締役会議事録",
        # bổ sung 2026-08-18 (video 28): cùng lỗi với 退職届 ở trên — giấy tờ mở màn là
        # 履歴書 (gọi tên ở giây 0) nhưng tool bắt nhầm 手帳 ở giây 69. Thêm keyword chỉ làm
        # gate NHẠY HƠN, không nới ngưỡng nào.
        "履歴書", "出勤簿", "打刻記録", "謄本", "決裁書", "辞令", "不在票", "弁済金",
        # bổ sung 2026-08-25 (video 34): cùng lỗi với 退職届/履歴書 — giấy tờ mở màn là
        # 香典帳 (gọi tên ở giây 0) nhưng tool bắt nhầm 署名 ở giây 87. Thêm keyword chỉ
        # làm gate NHẠY HƠN, không nới ngưỡng nào.
        "香典帳", "香典袋", "集計票", "媒介契約", "調剤", "納税通知",
        # bổ sung 2026-08-27 (video 35): 退任届 (thư từ nhiệm chức vụ hội đồng quản trị) gọi tên
        # ở giây 6 nhưng KHÔNG có trong bảng — khác 退職届 (nghỉ việc nhân viên) đã có sẵn.
        # Thêm keyword chỉ làm gate NHẠY HƠN, không nới lỏng ngưỡng nào.
        "退任届", "決議書", "信託契約", "公正証書", "仮登記",
        # bổ sung 2026-08-27 (video 17 v2, 感動する話): 木型 là vật chứng trung tâm của thể loại
        # 馴れ初め — vật thể chứ không phải giấy tờ, nhưng đóng đúng vai R2 (được gọi tên sớm,
        # là mối liên kết xuyên suốt truyện). Thêm keyword chỉ làm gate NHẠY HƠN.
        "木型", "処分リスト", "目録",
        # ⭐⭐ bổ sung 2026-08-29 (video 36) — LẦN NÀY KHÁC 5 LẦN TRƯỚC, đọc trước khi sửa tiếp:
        # 5 lần bổ sung ở trên đều là "thêm MỘT TỜ GIẤY mới". Cộng lại, bảng DOCS thành ra
        # ĐỊNH NGHĨA vật chứng = giấy tờ, và vì R2 là gate CHẶN nên nó âm thầm CƯỠNG CHẾ mọi
        # kịch bản phải có giấy trong 10 giây đầu. Đo máy 2026-08-29: 27/27 script đã đăng đều
        # lấy vật chứng là giấy — tức gate này là một trong những nguyên nhân khiến kênh lặp
        # mô-típ tới mức user nói "giống nhau 90%" (MỤC 11B của skill script-chouhen).
        # ⇒ Mở nhóm PHI-GIẤY. Đây KHÔNG phải nới ngưỡng (vẫn ≤ giây 10) — nó chỉ thôi bắt
        # kịch bản phải chứng minh bằng đúng một loại chất liệu.
        # 🔴 Chọn keyword bằng SỐ ĐO, không bằng cảm giác: mỗi từ dưới đây xuất hiện ở ≤9/28
        # script cũ nên vẫn phân biệt được bài có/không có vật chứng sớm. CỐ Ý LOẠI
        # 声(28/28) · 音(28/28) · 匂い(21/28) · 足音(7/28) — thêm mấy từ đó thì R2 luôn xanh,
        # tức gate chết mà không ai biết. Thêm keyword mới phải đo lại tần suất trước.
        "録音", "レコーダー", "ボイスメモ", "防犯カメラ", "監視カメラ", "ドラレコ",
        "ベル", "反射板", "傷跡", "指紋", "点字", "白い杖", "しゃがれた咳",
        "指輪", "枕の下", "ICレコーダー")   # video 36: 指輪 1/28 · 枕の下 0/28 · ICレコーダー 4/28

# R3 — anomaly người nghe TỰ SOI RA. Không phải "có bí mật", mà là một chỗ KHÔNG KHỚP mà
# khán giả tự nhìn thấy: chữ của người lạ, ngày tháng sai, chìa khoá không ai đặt.
ANOMALY = ("見覚えのない", "見覚えのある", "覚えのない", "頼んでいない", "知らない字", "女の字",
           "誰の字", "日付", "おかしい", "はずの", "なのに", "違っていた", "違う", "早すぎた",
           "見たことのない", "一度も", "まだ", "すでに", "とっくに")

# R4 — open-loop ĐẾM ĐƯỢC. 15/18 video có 「まだ知らなかった」 nên bản thân device không phải
# lợi thế; lợi thế là ĐẶT SỚM + ĐẾM ĐƯỢC (「三つのことを知らなかった」 → 一つ/二つ/三つ).
LOOP_RE = re.compile(r"(?:[一二三四五六七八九十\d]+)つのこと.{0,12}知らな|知らな.{0,8}(?:[一二三四五六七八九十\d]+)つ")
TEASE_RE = re.compile(r"まだ.{0,6}知らな|知らなかった|知らずに")
# 🔴 SỬA 2026-08-14 (user: *"đừng viết kiểu liệt kê như thế"*). Bản cũ là
# `^\s*(?:一つ|二つ|三つ|…)[。、]?\s*$` — nó CHỈ đếm được khi 「一つ。」 đứng TRƠ một dòng,
# tức gate **cưỡng chế một lỗi văn phong**: mọi kịch bản của kênh buộc phải viết 3 loop
# thành danh sách kiểm kê khô (「一つ。二十四冊の大学ノート。」) thay vì thành câu có hình ảnh.
# Cái R4 thật sự đo là "khán giả BIẾT còn mấy món chưa mở" — điều đó do câu 「三つのことを」
# tuyên bố, và do từ đếm mở ĐẦU mỗi khoản; nó không đòi từ đếm phải đứng một mình.
# Nay nhận cả dạng gắn liền: 「ひとつは、…」「ふたつめは、…」「そして三つめは、…」.
# Vẫn đòi từ đếm ở ĐẦU DÒNG (cho phép 「そして」 dẫn) nên không nới lỏng bản chất.
ENUM_RE = re.compile(
    r"^\s*(?:そして|それから)?\s*"
    r"(?:一|二|三|四|五|ひと|ふた|みっ|よっ|いつ)つ(?:め|目)?"
    r"(?:は|には|[。、])")

# R5 — chính diện phản đòn lần đầu (không phải khóc/xin lỗi).
COUNTER = ("ありがとうございます", "ありがとう", "止めて", "やめて", "待って", "お断り", "結構です",
           "いいえ", "分かりました", "承知しました", "出しました", "サイン", "署名します",
           "止めてもらえますか", "確かめ")

KAISOU = ("回想", "flashback", "十六年", "あの頃", "思い出")


def resolve(slug: str) -> tuple[Path | None, Path | None]:
    """Trả (script.md, subs.srt). Tìm cả bản đang làm (0N_SCRIPTS/0N_VIDEO) lẫn bản đã archive
    (07_UPLOADED/<slug>/_scripts + _upload) — video đã đăng vẫn phải đo lại được để verify gate."""
    script = srt = None
    for pat in (f"0[0-9]_SCRIPTS/{slug}.md", f"07_UPLOADED/{slug}/_scripts/{slug}.md"):
        hits = sorted(p for p in PROJ.glob(pat) if not p.name.endswith("_TTS.md"))
        if hits:
            script = hits[0]
            break
    for pat in (f"0[0-9]_VIDEO/{slug}/subs.srt", f"07_UPLOADED/{slug}/_upload/subs.srt"):
        hits = sorted(PROJ.glob(pat))
        if hits:
            srt = hits[0]
            break
    return script, srt


def srt_cues(p: Path) -> list[tuple[int, str]]:
    """[(giây bắt đầu, text)] — 1 dòng _TTS.md = 1 cue nên đây cũng là nhịp câu."""
    out = []
    for blk in p.read_text(encoding="utf-8", errors="ignore").split("\n\n"):
        L = blk.strip().split("\n")
        if len(L) < 3:
            continue
        m = re.match(r"(\d\d):(\d\d):(\d\d)", L[1])
        if not m:
            continue
        h, mi, s = (int(x) for x in m.groups())
        out.append((h * 3600 + mi * 60 + s, "".join(L[2:])))
    return out


def chapters(script: Path) -> list[tuple[int, str]]:
    """目次 trong 概要欄 = bản đồ beat do chính tác giả khai. Timestamp phải trích từ srt thật."""
    t = script.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"◆チャプター(.*?)(?:\n※|\n◆|```)", t, re.S)
    if not m:
        return []
    return [(int(a) * 60 + int(b), c.strip())
            for a, b, c in re.findall(r"^\s*(\d{1,2}):(\d\d)\s+(.*?)\s*$", m.group(1), re.M)]


def tts_seconds(script: Path, slug: str, rate: float) -> list[tuple[int, str]]:
    """Chế độ --pre: ước giây từ _TTS.md theo hệ số ký/phút (bài tag dày ~260, thưa ~295).
    Tag [速0.8]/[間1.2] KHÔNG cộng ký nhưng CỘNG thời gian → đó là lý do hệ số tụt 303→258."""
    cand = list(PROJ.glob(f"0[0-9]_SCRIPTS/{slug}_TTS.md")) + \
           list(PROJ.glob(f"07_UPLOADED/{slug}/_scripts/{slug}_TTS.md"))
    if not cand:
        return []
    out, acc = [], 0.0
    for line in cand[0].read_text(encoding="utf-8", errors="ignore").splitlines():
        clean = re.sub(r"\[[^\]]*\]", "", line).strip()
        if not clean or clean.startswith(("#", ">", "|", "```", "【", "=")):
            continue
        out.append((int(acc), clean))
        acc += len(clean) / rate * 60
    return out


def fmt(sec: float) -> str:
    return f"{int(sec)//60}′{int(sec)%60:02d}"


def first_hit(cues, needles, limit=200) -> tuple[int | None, str]:
    for sec, txt in cues:
        if sec > limit:
            break
        if any(n in txt for n in needles):
            return sec, txt
    return None, ""


def row(ok, tag, name, got, want) -> bool:
    mark = {True: "✅", False: "🔴", None: "⚠️ "}[ok]
    print(f"  {mark} {tag:<4}{name:<34}{got:<22}{want}")
    return ok is not False


def main() -> None:
    ap = argparse.ArgumentParser(description="Gate retention chouhen (công thức RETENTION-A)")
    ap.add_argument("slug")
    ap.add_argument("--pre", action="store_true", help="trước render: ước giây từ _TTS.md")
    ap.add_argument("--rate", type=float, default=265.0, help="ký/phút khi --pre (tag dày 260, thưa 295)")
    ap.add_argument("--waves", help="mốc SÓNG thủ công, vd 11:41,14:44,18:21,21:59,25:04")
    ap.add_argument("--loop-close", help="mốc đóng loop cold open, vd 21:59")
    ap.add_argument("--kaisou", help="khối 回想 thật, vd 5:11-7:31 (目次 hay chia nó thành nhiều beat)")
    a = ap.parse_args()

    script, srt = resolve(a.slug)
    if not script:
        sys.exit(f"❌ Không thấy script của {a.slug} (0N_SCRIPTS/ hoặc 07_UPLOADED/{a.slug}/_scripts/)")

    if a.pre:
        cues = tts_seconds(script, a.slug, a.rate)
        src = f"_TTS.md ước @{a.rate:.0f} ký/phút"
        if not cues:
            sys.exit(f"❌ Không thấy {a.slug}_TTS.md — chế độ --pre cần file đó")
    else:
        if not srt or not srt.exists():
            sys.exit(f"❌ Không thấy subs.srt của {a.slug} — chưa render thì chạy với --pre")
        cues = srt_cues(srt)
        src = str(srt.relative_to(PROJ))

    dur = cues[-1][0] if cues else 0
    ch = chapters(script)

    def mmss(s: str) -> int:
        p = s.strip().split(":")
        return int(p[0]) * 60 + int(p[1])

    if a.waves:
        waves = [(mmss(x), "khai báo tay") for x in a.waves.split(",")]
    else:
        waves = [(s, t) for s, t in ch if re.search(r"逆転|反転", t)]

    print(f"\n══ GATE RETENTION · {a.slug}")
    print(f"   nguồn: {src} · dài {fmt(dur)} · {len(ch)} beat trong 目次 · {len(cues)} câu")
    print(f"   luật: RETENTION_FORMULA_2026-08-11.md · 🔴 = chặn render\n")
    print(f"  {'':<3}{'':<4}{'chỉ số':<34}{'đo được':<22}ngưỡng")
    ok = True

    # ── R1 độ dài khớp số sóng ────────────────────────────────────────────────
    if waves:
        # Hai cấu hình: CHUẨN 11′ mở bài + 3′ kết (= 14 + 3,5N) · >60% bỏ 回想, kết gọn
        # (= 10,5 + 3,5N). Khớp một trong hai là đạt.
        n_std = max(1, round((dur / 60 - 14) / 3.5))
        n_60 = max(1, round((dur / 60 - 10.5) / 3.5))
        lo, hi = min(n_std, n_60), max(n_std, n_60)
        ok &= row(len(waves) >= lo * 0.7, "R1", "độ dài khớp số sóng",
                  f"{len(waves)} sóng / {fmt(dur)}", f"cần {lo}–{hi} sóng (10,5|14 + 3,5N)")
    else:
        ok &= row(None, "R1", "độ dài khớp số sóng", fmt(dur), "chưa dò được sóng → xem R9")

    # ── R2..R5 cold open, tính bằng GIÂY ──────────────────────────────────────
    s2, t2 = first_hit(cues, DOCS, 200)
    ok &= row(s2 is not None and s2 <= 10, "R2", "vật chứng gọi tên (giấy HOẶC phi-giấy)",
              f"giây {s2}" if s2 is not None else "KHÔNG THẤY", "≤ giây 10")

    s3, t3 = first_hit(cues, ANOMALY, 200)
    ok &= row(None if (s3 is not None and s3 <= 25) else None, "R3", "anomaly người nghe tự soi",
              f"giây {s3}" if s3 is not None else "KHÔNG THẤY", "≤ giây 25 · CẦN DUYỆT MẮT")

    s4 = None
    for sec, txt in cues:
        if sec > 200:
            break
        if LOOP_RE.search(txt):
            s4 = sec
            break
    s4b, _ = first_hit(cues, ("知らなかった", "まだ知ら"), 200)
    n_enum = sum(1 for sec, txt in cues if sec <= 200 and ENUM_RE.match(txt))
    if s4 is not None:
        got4, ok4 = f"giây {s4} · {n_enum} loop", s4 <= 60 and n_enum >= 3
    elif s4b is not None:
        got4, ok4 = f"giây {s4b} · KHÔNG ĐẾM", False
    else:
        got4, ok4 = "KHÔNG THẤY", False
    ok &= row(ok4, "R4", "open-loop đếm được (3 loop)", got4, "≤ giây 60 · 一つ/二つ/三つ")

    # R3b — CỬA TỬ THẬT. Retention 1% của video 12: giây 16 = 96,7% → giây 33 = 73,0% (−23,7đ);
    # video 09: giây 24 = 100,6% → giây 48 = 57,6% (−43,0đ). Gần như KHÔNG ai bỏ đi trong 16
    # giây đầu ⇒ toàn bộ cú giết nằm trong ~17 giây này. Câu giết video 09 nằm ở giây 32:
    # 「床の耐荷重から換気の位置まで、私が二年かけて決めた部屋だった」 = LỜI KỂ giải thích.
    # Đo: số dòng KỂ (không có 「) dài ≥25 ký trong cửa sổ. Video 12 = 0 · video 09 = 1.
    expo = [(sec, txt) for sec, txt in cues if 16 <= sec <= 35 and "「" not in txt and len(txt) >= 25]
    ok &= row(len(expo) == 0, "R3b", "giây 16–35: câu LỜI KỂ ≥25 ký",
              f"{len(expo)} câu", "= 0 — CHẶN (cửa tử thật)")
    for sec, txt in expo:
        print(f"          ↳ giây {sec}: 「{txt[:40]}」 ← cắt hoặc đổi thành thoại")

    s5, t5 = first_hit(cues, COUNTER, 240)
    # Câu phản đòn KÉO NGƯỜI QUAY LẠI, không chỉ giữ: video 12 hồi +3,3đ ở giây 82 (62,3→65,6)
    # ngay sau 「ありがとうございます、お義母さん」 ở giây 71. Mục tiêu >60% → đẩy về ~giây 50.
    ok &= row(None if (s5 is not None and s5 <= 80) else None, "R5", "chính diện phản đòn lần đầu",
              f"giây {s5}" if s5 is not None else "KHÔNG THẤY", "≤80s · ~50s nếu nhắm >60%")

    # ── R6 回想 ────────────────────────────────────────────────────────────────
    # ⚠️ Đo tự động chỉ ra được khoảng cách tới BEAT KẾ, không ra độ dài thật của khối 回想 khi
    # nó trải qua nhiều beat (video 12: 目次 nói 5′11→6′06 = 55s, khối thật 5′11→7′31 = 2′20).
    # Nên R6 là CẢNH BÁO; muốn đo đúng thì truyền --kaisou 5:11-7:31.
    # HAI TẦNG: chặn ở mức ĐÃ CHỨNG MINH XẤU (video 09: 4′01 ở phút 10′10, mất 6,3đ và là 1
    # trong 5 hố của nó), cảnh báo ở mức MỤC TIÊU >60% (bỏ hẳn 回想). Không chặn ở "= 0" vì
    # video 12 CÓ 回想 2′20 mà vẫn đạt 55,7% ⇒ chặn ở 0 là fail chính bản thắng (đúng bẫy R11).
    if a.kaisou and "-" in a.kaisou:
        p, q = a.kaisou.split("-")
        st, ln = mmss(p), mmss(q) - mmss(p)
        if ln == 0:
            ok &= row(True, "R6", "回想", "KHÔNG CÓ — đạt cấu hình >60%", "0 là tối ưu")
        else:
            hard = ln <= 150 and st + ln <= 660
            ok &= row(hard if not hard else None, "R6", "回想 (dài · xong trước phút 11)",
                      f"mở {fmt(st)} · dài {fmt(ln)}",
                      "≤2′30 & <11′ CHẶN · nhắm >60% thì BỎ HẲN")
    else:
        ks = next((i for i, (s, t) in enumerate(ch) if any(k in t for k in KAISOU)), None)
        if ks is not None:
            st = ch[ks][0]
            ln = (ch[ks + 1][0] - st) if ks + 1 < len(ch) else 0
            ok &= row(None, "R6", "回想 (mở · tới beat kế)",
                      f"mở {fmt(st)} · +{fmt(ln)}", "≤2′30 · xong <11′ · dùng --kaisou")
        else:
            ok &= row(None, "R6", "回想", "không thấy trong 目次", "≤2′30 · xong trước 11′")

    # ── R7 gap beat — HARD ────────────────────────────────────────────────────
    if len(ch) >= 2:
        gaps = sorted(((ch[i + 1][0] - ch[i][0], ch[i][0], ch[i][1]) for i in range(len(ch) - 1)),
                      reverse=True)
        g, gs, gt = gaps[0]
        bad = [x for x in gaps if x[0] > 165]
        ok &= row(g <= 165, "R7", "gap dài nhất giữa 2 beat",
                  f"{fmt(g)} sau {fmt(gs)}", "≤2′45 — CHẶN")
        for g2, s2_, t2_ in bad[:6]:
            print(f"          ↳ hố {fmt(g2)} sau beat {fmt(s2_)} 「{t2_[:30]}」")
    else:
        ok &= row(None, "R7", "gap dài nhất giữa 2 beat", "目次 <2 beat", "≤2′45 — CHẶN")

    # ── R8 SÓNG 1 — HARD, biến mạnh nhất ──────────────────────────────────────
    # HAI TẦNG. Chặn ở phút 12 = mức chứng minh bằng 6/6 video (video 12 ở 11′41 phải PASS).
    # Cảnh báo ở phút 8 = MỤC TIÊU >60%, dựa trên: đáy retention của video 12 nằm ở 9′38–11′01,
    # tức DÍNH SÁT MẶT TRƯỚC sóng 1 ⇒ kéo sóng 1 lên thì trũng ngắn và cạn hơn. Chưa ai làm →
    # là GIẢ THUYẾT, không phải số đã chứng minh, nên không chặn.
    if waves:
        w1 = waves[0][0]
        ok &= row(w1 <= 720 if w1 > 480 else True, "R8", "SÓNG 1 (cú lật đầu)", fmt(w1),
                  "≤12′ CHẶN · ≤8′ nếu nhắm >60%")
        if 480 < w1 <= 720:
            print(f"          ↳ đạt cửa 12′ nhưng chậm hơn mục tiêu 8′ — trũng nằm sát trước sóng 1")
    else:
        ok &= row(None, "R8", "SÓNG 1 (cú lật đầu)", "chưa dò được",
                  "≤ phút 12 — đánh số 逆転Ⓝ trong 目次")

    # ── R9 / R10 sóng ─────────────────────────────────────────────────────────
    ok &= row(len(waves) >= 4 if waves else None, "R9", "số sóng đánh số 逆転Ⓝ",
              f"{len(waves)} sóng" if waves else "0 — thiếu dấu 逆転", "≥4")
    if len(waves) >= 2:
        wg = [(waves[i + 1][0] - waves[i][0], waves[i][0]) for i in range(len(waves) - 1)]
        mx, at = max(wg)
        ok &= row(mx <= 240, "R10", "gap giữa 2 sóng", f"{fmt(mx)} sau {fmt(at)}",
                  "≤4′ (video 12: 3,0–3,7)")
    else:
        ok &= row(None, "R10", "gap giữa 2 sóng", "<2 sóng", "≤4′")

    # ── R11 loop cold open — HARD ─────────────────────────────────────────────
    # Ngưỡng 78% HIỆU CHỈNH TỪ BẢN THẮNG, không phải số tròn tự chọn: video 12 (AVD 51,6%)
    # đóng loop cold open ở 21′59/27′30 = 80%. Bản đầu đặt 85% → FAIL chính video làm ra công
    # thức ⇒ gate sai, không phải video sai. Video 09 đóng ở 39% và mất đuôi (§3.3).
    lc = mmss(a.loop_close) if a.loop_close else (waves[-1][0] if waves else None)
    if lc is not None and dur:
        pct = lc / dur * 100
        ok &= row(pct >= 78, "R11", "loop cold open đóng ở",
                  f"{fmt(lc)} = {pct:.0f}%", "≥78% — CHẶN (video 12 = 80%)")
    else:
        ok &= row(None, "R11", "loop cold open đóng ở", "chưa khai báo", "≥78% (--loop-close)")

    # ── khuyến nghị ───────────────────────────────────────────────────────────
    avg = sum(len(t) for _, t in cues) / max(1, len(cues))
    print(f"\n  ⓘ  nhịp câu {avg:.1f} ký/câu (khuyến nghị ≤16 — tín hiệu yếu, không chặn)")
    if dur:
        for lab, need in (("33% mở rail", 0.33), ("50%", 0.50)):
            print(f"  ⓘ  AVD {lab:<12} cần {dur/60*need:5.1f} phút xem "
                  f"(kỷ lục kênh 15,6′ — video 07-17 54′49)")

    print("\n  ── 90 GIÂY ĐẦU (duyệt mắt R3 + R5) ──")
    for sec, txt in cues:
        if sec > 90:
            break
        flag = ""
        if s2 is not None and sec == s2:
            flag += " ←R2"
        if s3 is not None and sec == s3:
            flag += " ←R3?"
        if s5 is not None and sec == s5:
            flag += " ←R5?"
        print(f"   [{sec:>3}] {txt[:52]}{flag}")

    print()
    if ok:
        print("  ✅ QUA GATE — 3 số chặn (R7/R8/R11) đều đạt. R3/R5 vẫn phải duyệt mắt.\n")
    else:
        print("  🔴 CHƯA QUA GATE — sửa số 🔴 trước khi render.\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
