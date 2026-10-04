# -*- coding: utf-8 -*-
"""Chuyển kịch bản sạch (sau '=== KỊCH BẢN HOÀN CHỈNH ===') → file _TTS.md.
1 dòng = 1 nhịp đọc (~<=MAXLEN ký tự), tách ở 。！？ rồi wrap ở 、.
Dòng trống giữ nguyên (nghỉ sâu). Bỏ header ##, （第...）, ===, >.
"""
import re, sys, io
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
MAXLEN = 38

def split_line(line):
    parts = [p for p in re.split(r'(?<=[。！？])', line) if p.strip()]
    out = []
    for p in parts:
        if len(p) <= MAXLEN:
            out.append(p); continue
        buf = ''
        for s in re.split(r'(?<=、)', p):
            if buf and len(buf) + len(s) > MAXLEN:
                out.append(buf); buf = s
            else:
                buf += s
        if buf:
            out.append(buf)
    return out

def main():
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    lines = src.read_text(encoding="utf-8").splitlines()
    # cắt sau marker
    try:
        start = next(i for i, l in enumerate(lines) if "KỊCH BẢN HOÀN CHỉNH" in l or "KỊCH BẢN HOÀN CHỈNH" in l)
    except StopIteration:
        start = -1
    body = lines[start+1:]
    out = ["# 01 息子の結婚披露宴 — TTS (morioki / AivisSpeech, speed 1.0)",
           "# 1 dòng = 1 nhịp đọc. Dòng trống = nghỉ sâu.", ""]
    prev_blank = True
    for l in body:
        s = l.strip()
        if not s:
            if not prev_blank:
                out.append(""); prev_blank = True
            continue
        if s.startswith("#") or s.startswith("＃") or s.startswith(">") or s.startswith("==") or s.startswith("（第") or s.startswith("(第"):
            continue
        # marker chia batch của skill script-chouhen: 【PHẦN 1/2】/【PHẦN 2/3】… + 【KHỐI n …】
        # KHÔNG phải lời kể → phải loại, nếu không TTS đọc luôn "phần một trên hai".
        if re.match(r"^【\s*(PHẦN|PHAN|KHỐI|KHOI)\b", s, re.IGNORECASE):
            continue
        for beat in split_line(s):
            out.append(beat)
        prev_blank = False
    dst.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    # thống kê
    body_lines = [x for x in out if x and not x.startswith("#")]
    chars = sum(len(x) for x in body_lines)
    print(f"OK -> {dst}")
    print(f"Số dòng đọc: {len(body_lines)} | ký tự: {chars}")

if __name__ == "__main__":
    main()
