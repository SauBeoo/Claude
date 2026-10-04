# -*- coding: utf-8 -*-
"""tts_prefetch.py — đổ CACHE giọng SONG SONG trước khi chạy khâu synth.

Vì sao có file này (đo thật 2026-08-04, video 17):
    Khâu 1 (`ambient_render.py --voice-only`) gọi `tts_render.synthesize()` **tuần tự**
    → đo được **3,46 giây/câu** trên VOICEVOX. Kịch bản 42 phút = 734 câu ⇒ ~42 phút chỉ
    để synth, trong khi cả khâu dựng hình chỉ mất ~25 phút. Nút cổ chai nằm ở TTS.
    Gọi 4 request đồng thời: **2,14 giây/câu → nhanh 1,61×** (VOICEVOX xử lý được song song).

Cách làm — KHÔNG sửa `tts_render.py` (tool dùng chung của 7 kênh, sửa là đụng cả 7):
    tool này dùng CHÍNH `parse_script()` + `synthesize()` của tts_render, nên khoá cache
    trùng khít 100%. Nó chỉ ghi vào `Projects/_tts_cache/`. Sau đó chạy khâu 1 như thường:
    vòng lặp tuần tự thấy mọi câu đã có trong cache → đọc từ đĩa, gần như tức thì.

    python tools/tts_prefetch.py 03_SCRIPTS/17_sakura-no-kigata_TTS.md \
        --engine voicevox --speaker 青山龍星 --speed 0.80 --intonation 1.15 --jobs 4

An toàn:
  * Chạy lại = idempotent (câu đã cache thì bỏ qua ngay, không gọi engine).
  * Câu nào prefetch fail → bỏ qua, khâu 1 tự synth lại tuần tự như cũ. Không chặn render.
  * Tag `[速…][抑揚…][間…]` được parse bằng đúng parser của tts_render → không lệch tham số.
"""
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / "youtube-jp-health" / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import tts_render as T  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--engine", default="voicevox", choices=list(T.ENGINE_PRESETS))
    ap.add_argument("--speaker", default="青山龍星")
    ap.add_argument("--speed", type=float, default=0.80)
    ap.add_argument("--intonation", type=float, default=1.15)
    ap.add_argument("--gap", type=float, default=0.5)
    ap.add_argument("--section-gap", type=float, default=1.1)
    ap.add_argument("--jobs", type=int, default=4,
                    help="số request đồng thời (đo: 4 = nhanh 1,61× so với 1; >6 không lợi thêm)")
    args = ap.parse_args()

    base = T.ENGINE_PRESETS[args.engine]
    if not T.check_engine(base):
        sys.exit(f"[LỖI] không kết nối engine {base} — mở app "
                 f"{'VOICEVOX' if args.engine == 'voicevox' else 'AivisSpeech'} rồi chạy lại")

    events = T.parse_script(args.input, args.gap, args.section_gap)
    speech = [e for e in events if "text" in e]
    speakers = T.api(base, "GET", "/speakers")

    style_cache = {}

    def style_of(name):
        if name not in style_cache:
            _, st_name, st_id = T.resolve_style(speakers, args.speaker, name)
            style_cache[name] = (st_name, st_id)
        return style_cache[name]

    jobs = []
    for e in speech:
        st_name, sid = style_of(e["style"])
        volume = e["volume"]
        if volume is None:
            volume = next((v for k, v in T.STYLE_VOLUME_BOOST.items() if k in st_name), None)
        jobs.append({
            "text": e["text"], "sid": sid,
            "speed": e["speed"] if e["speed"] is not None else args.speed,
            "into": e["intonation"] if e["intonation"] is not None else args.intonation,
            "pitch": e["pitch"], "volume": volume,
        })

    todo = []
    for j in jobs:
        key = T._cache_key(base, j["text"], j["sid"], j["speed"], j["into"],
                           j["pitch"], j["volume"])
        if not (T.CACHE_DIR / f"{key}.wav").is_file():
            todo.append(j)

    print(f"{len(jobs)} câu | đã có cache {len(jobs) - len(todo)} | cần synth {len(todo)} "
          f"| {args.jobs} luồng")
    if not todo:
        print("cache đã đủ — chạy thẳng khâu 1")
        return

    done = [0]
    fail = []
    t0 = time.time()

    def work(j):
        try:
            T.synthesize(base, j["text"], j["sid"], j["speed"], j["into"],
                         j["pitch"], j["volume"])
        except Exception as ex:                    # noqa: BLE001 — khâu 1 sẽ synth lại
            fail.append((j["text"][:20], str(ex)[:60]))
        done[0] += 1
        n = done[0]
        if n % 25 == 0 or n == len(todo):
            el = time.time() - t0
            eta = el / n * (len(todo) - n)
            print(f"  {n}/{len(todo)}  {el/60:.1f}m trôi qua, còn ~{eta/60:.1f}m "
                  f"({el/n:.2f}s/câu)", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        list(ex.map(work, todo))

    print(f"XONG prefetch {len(todo)} câu trong {(time.time()-t0)/60:.1f} phút")
    if fail:
        print(f"⚠️ {len(fail)} câu prefetch fail (khâu 1 sẽ tự synth lại tuần tự):")
        for t, e in fail[:5]:
            print(f"   {t}… → {e}")


if __name__ == "__main__":
    main()
