# -*- coding: utf-8 -*-
"""Demo giong cho kenh Showa Kurashi Zukan — 3 ung vien nam (khac Aoyama Ryusei).
Synth cung 1 doan kyushoku ~80s, speedScale 0.88, ra 06_VIDEO/_voice_demo/.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
import wave

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VOICEVOX = "http://127.0.0.1:50021"
AIVIS = "http://127.0.0.1:10101"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "06_VIDEO", "_voice_demo")
os.makedirs(OUT, exist_ok=True)

# Vong 2 (2026-08-02, user che vong 1 "chua tram am du"):
CANDIDATES = [
    ("VV", 118, "yogatari_tobari", "夜語トバリ — kể chuyện đêm, trầm sâu"),
    ("VV", 99, "rito", "離途 — nam trưởng thành trầm tĩnh"),
    ("VV", 94, "chubu_tsurugi", "中部つるぎ — nam dày tiếng"),
    ("AV", 1310138977, "aida_shigeru_calm", "阿井田茂 Calm (AivisSpeech) — trầm ấm tự nhiên ⚠️ cùng người nói với chouhen, khác style"),
]

# ~420 ky ~ 80s @ 0.88; moi dong = 1 nhip, nghi giua dong
LINES = [
    "昭和45年。あなたが、小学生だった頃のことです。",
    "四時間目の終わりごろ、教室の廊下に、あの香りが流れてきました。",
    "そう、揚げパンです。",
    "きなこをまとった、揚げたてのコッペパン。",
    "配られる数を、みんなが目で数えていましたね。",
    "アルマイトの食器に、少しへこんだお盆。",
    "先割れスプーンで食べた、あの給食の時間。",
    "瓶の牛乳は、冬になると、なかなか減らないのに、",
    "冷凍みかんの日だけは、教室が静かになりました。",
    "今日は、そんな懐かしい献立を、一つずつ、思い出していきます。",
    "じつは私も、揚げパンの日だけは、学校を休めなかった口です。",
]
PAUSE_SEC = 0.55


def synth_line(text, speaker, host):
    q_url = f"{host}/audio_query?" + urllib.parse.urlencode(
        {"text": text, "speaker": speaker})
    req = urllib.request.Request(q_url, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        query = json.loads(r.read())
    query["speedScale"] = 0.88
    query["postPhonemeLength"] = PAUSE_SEC
    s_url = f"{host}/synthesis?" + urllib.parse.urlencode({"speaker": speaker})
    req = urllib.request.Request(
        s_url, data=json.dumps(query).encode(), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    for engine, sid, slug, label in CANDIDATES:
        host = VOICEVOX if engine == "VV" else AIVIS
        dest = os.path.join(OUT, f"demo_{slug}.wav")
        if os.path.exists(dest):
            print(f"[{label}] da co, skip")
            continue
        print(f"[{label}] id={sid} ...")
        frames, params = [], None
        import io
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
    print("\nXONG — nghe 3 file trong 06_VIDEO/_voice_demo/ va chon.")


if __name__ == "__main__":
    main()
