# -*- coding: utf-8 -*-
r"""Anatomy of a competitor video: WHEN it enters, HOW it opens, how fast it cuts, what is on screen.

Why: co-dai has full numbers on ITSELF (retention curves, gates) but zero analysis of HOW the
winning peer (昔の人の知恵: 1.28M views / 22 videos / 65 days) actually builds a video. Two hit
transcripts sat in 01_SOURCES for a month unanalysed. This tool turns a downloaded mp4 into the
same metrics we gate our own scripts with, plus the visual layer transcripts cannot give.

Per video:
  1. audio -> faster_whisper (ja) -> segments with timestamps -> <stem>.srt + .words.json
  2. text metrics with the SAME machinery as check_coldopen.scan() (reads .srt):
       entry second · cold-open type · non-paying sentences in 0-45s · payoff gap · flips ·
       open-loop sentences · loop-close % · money/industry chapter % · CTA %
  3. visual metrics: scene cuts via ffmpeg scdet -> cuts/min, longest hold, first-60s cut count
  4. frame sheet: 1 frame every 30s -> _peer/<stem>_sheet.jpg (read with eyes: footage? AI? text cards?)
  5. one row appended to 01_SOURCES/PEER_ANATOMY.md (+ per-video block with the first 90s verbatim)

Usage:
    python tools\analyze_peer.py "F:\Youtube\peer\*.mp4"           # all
    python tools\analyze_peer.py path.mp4 --views 499441 --label hit
    python tools\analyze_peer.py path.mp4 --model small             # faster; default medium

Whisper timestamps are ~±0.5s. Good enough for "which second does it enter the body"; not for
1%-curve mapping (we have no curve for peer videos anyway - we only see what they SHOW).
"""
import argparse
import glob
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "01_SOURCES" / "_peer"
REPORT = ROOT / "01_SOURCES" / "PEER_ANATOMY.md"
sys.path.insert(0, str(ROOT / "tools"))
import check_coldopen as cc  # noqa: E402  (reuse scan(), MONEY_CH, OPEN_LOOP, FLIP ...)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)


def probe(mp4):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(mp4)])
    return float(json.loads(r.stdout)["format"]["duration"])


def transcribe(mp4, stem, model_size):
    """faster_whisper -> srt with real seconds. Cached: skip if .srt exists."""
    srt = OUT / f"{stem}.srt"
    if srt.exists():
        return srt
    from faster_whisper import WhisperModel
    wav = OUT / f"{stem}.wav"
    if not wav.exists():
        run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-vn", "-ac", "1", "-ar", "16000", str(wav)])
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(str(wav), language="ja", vad_filter=True, beam_size=5)
    lines, words = [], []
    for i, s in enumerate(segs, 1):
        def ts(x):
            h, m = divmod(int(x), 3600)
            m, sec = divmod(m, 60)
            return f"{h:02d}:{m:02d}:{sec:02d},{int((x - int(x)) * 1000):03d}"
        lines.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n")
        words.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
    srt.write_text("\n".join(lines), encoding="utf-8")
    (OUT / f"{stem}.words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0), encoding="utf-8")
    return srt


def scene_cuts(mp4, dur, thr=0.10):
    """ffmpeg scdet -> list of cut seconds.

    thr HIEU CHUAN 2026-09-06 tren 120s cua peer 排水口 (559K view): 5%/10%/15% deu tra
    15 cat/120s = 7,5 cat/phut, con 30% chi tra 2 = SO RAC (sheet 46 frame cho thay 46/46
    canh khac nhau). Peer chuyen canh bang DISSOLVE dai nen diff khung thap -> nguong cao
    bo sot gan het. Cung benh "cua so quet hep hon vat" (feedback_do_pixel_cua_so_quet).
    """
    r = run(["ffmpeg", "-v", "info", "-i", str(mp4), "-vf", f"scdet=threshold={thr*100:.0f}",
             "-an", "-f", "null", "-"])
    cuts = [float(m.group(1)) for m in re.finditer(r"lavfi\.scd\.time:\s*([\d.]+)", r.stderr)]
    if not cuts:  # older ffmpeg prints differently
        cuts = [float(m.group(1)) for m in re.finditer(r"scd\.time=([\d.]+)", r.stderr)]
    cuts = sorted(set(round(c, 1) for c in cuts))
    holds = [b - a for a, b in zip([0.0] + cuts, cuts + [dur])]
    return cuts, holds


def frame_sheet(mp4, stem, dur, every=30):
    """One frame every `every` seconds, tiled 6 per row -> jpg (read with eyes)."""
    tmp = OUT / f"_f_{stem}"
    tmp.mkdir(parents=True, exist_ok=True)
    n = 0
    for t in range(0, int(dur), every):
        run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1",
             "-vf", "scale=320:180", str(tmp / f"{n:03d}.png")])
        n += 1
    rows = max(1, -(-n // 6))
    sheet = OUT / f"{stem}_sheet.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-start_number", "0", "-i", str(tmp / "%03d.png"),
         "-vf", f"tile=6x{rows}:margin=4:padding=3", str(sheet)])
    for p in tmp.glob("*.png"):
        p.unlink()
    tmp.rmdir()
    return sheet, n


def analyze(mp4, views, label, model_size):
    stem = re.sub(r"[^\w\-]+", "_", Path(mp4).stem)[:60]
    OUT.mkdir(parents=True, exist_ok=True)
    dur = probe(mp4)
    print(f"\n── {Path(mp4).name} · {dur/60:.1f}′ · {views or '?'} view · {label}")

    srt = transcribe(mp4, stem, model_size)
    r = cc.scan(srt)                      # same gate machinery as our own scripts
    body = [(s, t) for s, t, _ in cc.cues_srt(srt)]
    text = "".join(t for s, t in body)
    cps = len(text) / dur if dur else 0

    cuts, holds = scene_cuts(mp4, dur)
    cut_min = len(cuts) / (dur / 60) if dur else 0
    first60 = sum(1 for c in cuts if c <= 60)
    sheet, nf = frame_sheet(mp4, stem, dur)

    # scan() đã tính money_pos / n_close / n_flip / n_open bằng đúng regex của gate — dùng thẳng,
    # đừng tính lại bằng bản sao (hai bản số lệch nhau là bẫy đã dính ở _sig của make_stage)
    mp = r["money_pos"]
    cta = next((s for s, t in body if any(k in t for k in ("高評価", "チャンネル登録", "登録"))), None)
    first90 = [(s, t) for s, t in body if s <= 90]
    flips = [s for s, t in body if any(w in t for w in cc.FLIP)]
    close = r["close"]
    n_free45 = r["n_free"]

    rec = dict(file=Path(mp4).name, stem=stem, views=views, label=label, dur=round(dur, 1),
               chars=len(text), cps=round(cps, 2),
               entry_s=r["entry_s"], entry_t=r["entry_t"], n_free45=n_free45, n_win=r["n_win"],
               gap_payoff_s=round(r["gap"], 1), n_flip=len(flips), first_flip_s=flips[0] if flips else None,
               n_open=r["n_open"], n_wave=r["n_wave"], loop_close_pct=(round(close / dur * 100) if close else None),
               money_pct=(round(mp * 100) if mp is not None else None),
               cta_pct=(round(cta / dur * 100) if cta is not None else None),
               cuts=len(cuts), cuts_per_min=round(cut_min, 2), cuts_first60=first60,
               hold_max_s=round(max(holds), 1) if holds else None,
               hold_median_s=round(sorted(holds)[len(holds) // 2], 1) if holds else None,
               fails=r["fails"], warns=r["warns"], sheet=str(sheet), frames=nf)
    (OUT / f"{stem}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")

    e = f"{rec['entry_s']:.0f}s" if rec["entry_s"] is not None else "KHÔNG DÒ"
    print(f"   lời: {len(text)} ký · {cps:.2f} ký/s · vào bài {e} 「{rec['entry_t'][:26]}」 · "
          f"0–45s: {n_free45}/{r['n_win']} câu không trả tiền · gap payoff max {rec['gap_payoff_s']:.0f}s")
    print(f"   sóng: {len(flips)} cú lật (đầu @{(flips[0] if flips else 0):.0f}s) · {r["n_open"]} câu MỞ ({r["n_wave"]} sóng) · "
          f"loop đóng @{rec['loop_close_pct']}% · dòng tiền @{rec['money_pct']}% · CTA @{rec['cta_pct']}%")
    print(f"   hình: {len(cuts)} cắt · {cut_min:.2f} cắt/phút · 60s đầu {first60} cắt · "
          f"hold trung vị {rec['hold_median_s']}s · dài nhất {rec['hold_max_s']}s · sheet {nf} frame → {sheet.name}")
    print("   90s đầu:")
    for s, t in first90:
        print(f"      {s:5.1f}s  {t[:60]}")
    return rec, first90


def append_report(rec, first90):
    hdr = ("# PEER_ANATOMY — bóc video đối thủ (昔の人の知恵 …) bằng `tools/analyze_peer.py`\n\n"
           "> Cùng thước với gate của mình (`check_coldopen.scan` trên srt whisper) + lớp hình (scdet). "
           "Whisper ±0,5s. KHÔNG có curve retention của họ — chỉ đo được cái họ LÀM, không đo được "
           "khán giả họ Ở LẠI bao lâu.\n\n"
           "| video | view | dài | ký/s | vào bài | 0–45s không trả | gap payoff | cú lật (đầu) | câu MỞ | loop đóng | dòng tiền | CTA | cắt/phút | 60s đầu cắt | hold TV / max |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    if not REPORT.exists():
        REPORT.write_text(hdr, encoding="utf-8")
    s = REPORT.read_text(encoding="utf-8")
    e = f"{rec['entry_s']:.0f}s" if rec["entry_s"] is not None else "—"
    row = (f"| {rec['label']} `{rec['file'][:28]}` | {rec['views'] or '?'} | {rec['dur']/60:.0f}′ | {rec['cps']} | {e} | "
           f"{rec['n_free45']}/{rec['n_win']} | {rec['gap_payoff_s']:.0f}s | {rec['n_flip']} (@{(rec['first_flip_s'] or 0):.0f}s) | "
           f"{rec['n_open']} | {rec['loop_close_pct'] or '—'}% | {rec['money_pct'] or '—'}% | {rec['cta_pct'] or '—'}% | "
           f"{rec['cuts_per_min']} | {rec['cuts_first60']} | {rec['hold_median_s']}s / {rec['hold_max_s']}s |\n")
    # insert row after table header (keep table together), then per-video block at end
    parts = s.split("\n|---|", 1)
    if len(parts) == 2:
        head, rest = parts
        rest_lines = rest.split("\n", 1)
        s = head + "\n|---|" + rest_lines[0] + "\n" + row + (rest_lines[1] if len(rest_lines) > 1 else "")
    else:
        s += row
    block = [f"\n\n## {rec['label']} · `{rec['file']}` · {rec['views'] or '?'} view · {rec['dur']/60:.1f}′\n",
             f"- sheet hình: `{Path(rec['sheet']).relative_to(ROOT)}` ({rec['frames']} frame, 1/30s) — **đọc bằng mắt**: footage thật / AI / thẻ chữ / người dẫn?",
             f"- gate của mình chấm họ: {'; '.join(rec['fails']) or '0 FAIL'}",
             "- **90 giây đầu (nguyên văn whisper):**"]
    block += [f"  - `{s_:5.1f}s` {t}" for s_, t in first90]
    REPORT.write_text(s.rstrip("\n") + "\n".join(block) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--views", type=int, default=None)
    ap.add_argument("--label", default="hit")
    ap.add_argument("--model", default="medium", help="faster_whisper size: small|medium|large-v3")
    a = ap.parse_args()
    files = []
    for p in a.paths:
        files += glob.glob(p)
    if not files:
        sys.exit("không thấy mp4")
    for f in sorted(files):
        rec, f90 = analyze(f, a.views, a.label, a.model)
        append_report(rec, f90)
    print(f"\n✅ {len(files)} video → {REPORT}")


if __name__ == "__main__":
    main()
