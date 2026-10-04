# -*- coding: utf-8 -*-
"""Demo doan 昭和の正月 (transcript doi thu, da lam sach) bang 4 giong vong 2."""
import io
import os
import sys
import wave

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demo_voice_showa import CANDIDATES, VOICEVOX, AIVIS, synth_line, OUT

# them lai 3 giong vong 1 de so du bo tren cung 1 doan
ALL_CANDIDATES = list(CANDIDATES) + [
    ("VV", 53, "kigashima_sorin", "麒ヶ島宗麟 — ông lão trầm khàn"),
    ("VV", 100, "kurosawa_saeha", "黒沢冴白 — nam trầm tĩnh"),
    ("VV", 11, "kurono_takehiro", "玄野武宏 — nam điềm đạm"),
    # vong 3: giong NU (2026-08-02) — ne No.7 (kaigo) va morioki (chouhen)
    ("VV", 109, "f_tohoku_itako", "東北イタコ — nữ trưởng thành, kể chuyện"),
    ("VV", 27, "f_goki_ningen", "後鬼 人間ver — nữ chín, dày tiếng"),
    ("VV", 14, "f_meimei_himari", "冥鳴ひまり — nữ dịu trầm"),
    ("VV", 16, "f_kyushu_sora", "九州そら — nữ mềm, phát thanh viên"),
    ("AV", 888753763, "f_mao_ochitsuki", "まお おちつき (AivisSpeech) — nữ điềm, tự nhiên"),
    # vong 4: "kieu ke chuyen, khong can gia" (user 2026-08-02)
    ("VV", 31, "no7_yomikikase", "No.7 読み聞かせ — style đọc truyện ⚠️ cùng người nói kaigo (đang ngưng)"),
    ("VV", 56, "f_nekotsuka_aru_ochitsuki", "猫使アル おちつき — nữ trẻ, điềm"),
]

LINES = [
    "昭和の正月、覚えていますか。",
    "昭和の大晦日の夜が、どれほど静かだったか、覚えていますか。",
    "街から、音が消えた瞬間を、覚えていますか。",
    "夜中でも、店が開いていなかった時代を、覚えていますか。",
    "あの夜、消えていた音を、覚えていますか。",
    "昭和の正月。",
    "大晦日の夕暮れは、とてもゆっくりと訪れました。",
    "古い家並みに残る光は、次第に弱まり、冬の澄んだ空気が、町を包みます。",
    "冷たい風は吹いていましたが、騒がしさはありません。",
    "車の音も、広告の音も、聞こえてきませんでした。",
    "町全体が、静かに、息を止めているようでした。",
    "その静けさの中で、小さな音だけが、際立ちます。",
]


def main():
    for engine, sid, slug, label in ALL_CANDIDATES:
        host = VOICEVOX if engine == "VV" else AIVIS
        dest = os.path.join(OUT, f"demo_shogatsu_{slug}.wav")
        if os.path.exists(dest):
            print(f"[{label}] da co, skip")
            continue
        print(f"[{label}] ...")
        frames, params = [], None
        for line in LINES:
            wav_bytes = synth_line(line, sid, host)
            with wave.open(io.BytesIO(wav_bytes)) as w:
                if params is None:
                    params = w.getparams()
                frames.append(w.readframes(w.getnframes()))
        with wave.open(dest, "wb") as out:
            out.setparams(params)
            for fr in frames:
                out.writeframes(fr)
        dur = sum(len(f) for f in frames) / (params.framerate * params.sampwidth * params.nchannels)
        print(f"    -> {dest}  ({dur:.1f}s)")


if __name__ == "__main__":
    main()
