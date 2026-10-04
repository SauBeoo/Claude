# -*- coding: utf-8 -*-
"""Sinh _TTS.md từ script .md: 1 dòng = 1 nhịp (câu), dòng trống = nghỉ sâu, '---' = ranh giới chương."""
import io, re, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = Path(r"E:\Claude\Projects\youtube-jp-kaigo\03_SCRIPTS\01_ninchisho-koza-toketsu.md")
OUT = SRC.with_name(SRC.stem + "_TTS.md")
MAXLEN = 84  # 2 dòng phụ đề × SUB_MAXLEN 42

t = SRC.read_text(encoding="utf-8")
body = t.split("## === KỊCH BẢN HOÀN CHỈNH ===")[1].split("## === HẾT KỊCH BẢN ===")[0]

def split_sentences(p):
    parts = re.findall(r"[^。]*。|[^。]+$", p)
    out = []
    for s in parts:
        s = s.strip()
        if not s:
            continue
        while len(s) > MAXLEN:
            # cắt ở 、 gần giữa nhất
            cands = [m.end() for m in re.finditer("、", s) if 20 <= m.end() <= MAXLEN]
            if not cands:
                break
            cut = min(cands, key=lambda c: abs(c - MAXLEN * 0.75))
            out.append(s[:cut]); s = s[cut:]
        out.append(s)
    return out

lines, first_chapter = [], True
for raw in body.splitlines():
    s = raw.strip()
    if not s:
        continue
    if s.startswith("###"):
        if not first_chapter:
            lines += ["", "---", ""]
        first_chapter = False
        continue
    for sent in split_sentences(s):
        lines.append(sent)
    lines.append("")   # nghỉ sâu cuối đoạn

txt = "\n".join(lines).strip() + "\n"

# tag nhấn nhá tiết chế (chỉ 速/抑揚/間 — không đổi style)
tags = [
    ("お父さんの通帳から、一円も出せなくなる日があります。", "[間1]お父さんの通帳から、一円も出せなくなる日があります。"),
    ("1400万円が、その日から、一円も動きません。", "[速0.92][間1]1400万円が、その日から、一円も動きません。"),
    ("ここが、今日いちばんお伝えしたい逆転です。", "[間1][抑揚1.2]ここが、今日いちばんお伝えしたい逆転です。"),
    ("三問とも×でした。", "[間1]三問とも×でした。"),
    ("そこは、最後まで聞いてください。", "[抑揚1.2]そこは、最後まで聞いてください。"),
    ("赤で囲んだところ、ご覧ください。", "[速0.9]赤で囲んだところ、ご覧ください。"),
    ("お母さんの口座には、お母さんのお金がちゃんと入っています。", "[間1]お母さんの口座には、お母さんのお金がちゃんと入っています。"),
    ("桁が一つ違います。", "[速0.9][抑揚1.2]桁が一つ違います。"),
    ("期限は、日付ではありません。", "[間1]期限は、日付ではありません。"),
    ("それでは、また次のノートでお会いしましょう。", "[速0.9]それでは、また次のノートでお会いしましょう。"),
]
n = 0
for a, b in tags:
    if a in txt:
        txt = txt.replace(a, b, 1); n += 1
    else:
        print(f"  ⚠️ không thấy dòng để gắn tag: {a[:24]}…")

OUT.write_text(txt, encoding="utf-8")
spoken = [l for l in txt.splitlines() if l.strip() and l.strip() != "---"]
nchar = sum(len(re.sub(r"\[[^\]]*\]", "", l)) for l in spoken)
print(f"✅ {OUT.name}: {len(spoken)} dòng đọc · {nchar} ký · tag gắn {n}/{len(tags)}")
print(f"   dòng dài nhất: {max(len(l) for l in spoken)} ký")
print(f"   ước {nchar/315:.1f} phút @315 ký/phút")
