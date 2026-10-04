# -*- coding: utf-8 -*-
"""Demo giong BAN 4 video 01 — 2 doan dat nhat (dinh tra do gia + okawari janken).
Tag semantics khop tts_render.py: gia tri TUYET DOI per-line (速0.85 -> speedScale=0.85),
間/後間 = silence truoc/sau (giay). Profile showa: VOICEVOX 109, speed 0.90, intonation 1.15.
"""
import io, json, os, re, struct, sys, urllib.parse, urllib.request, wave

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
VV = "http://127.0.0.1:50021"
SPEAKER = 109  # 東北イタコ ノーマル
BASE_SPEED, BASE_INTO = 0.90, 1.15
GAP = 0.55  # nghi giua dong (khop mac dinh renderer)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "06_VIDEO", "01_kyushoku_v2")
os.makedirs(OUT, exist_ok=True)

PASSAGE_A = """さて、ここで、最初の質問の答え合わせです。
あの給食、ひと月、いくらだったのか。
東京、府中市の記録に、残っています。
[間1.2][速0.8]昭和42年、小学校低学年の給食費は、ひと月、700円。
[速0.85][後間0.8]一食に直すと、およそ35円です。
この35円が、どれだけの値段だったのか。
さっきの牛乳を、思い出してください。
同じ昭和42年、配達の牛乳は、1本およそ21円。
つまり給食一食は、牛乳1本と、あまり変わらない値段だったんです。
牛肉なら、どうでしょう。
同じ年の東京で、牛肉のロースは、100グラム、202円。
[間0.8][抑揚1.25]給食の、およそ6食分です。
そして、翌年の大卒の初任給が、月に、およそ3万600円。
給食費は、お給料の、およそ40分の1。
牛乳1本ほどの値段で、パンと、おかずと、デザートまで。
[速0.85][後間1.0]あの一食に詰まっていた工夫が、数字から、伝わってきます。"""

PASSAGE_B = """最後の十品目は、品物ではなく、あの時間です。
給食でいちばん盛り上がった、おかわり。
揚げパンがひとつ余った日の、あの緊張感。
誰が手を挙げるのか。
[間0.5][速0.85]教室が、しんと静まりかえる。
隣の席の子が、小さな声で言うんです。
[間0.8][抑揚1.3][速0.95]「最後のひとつ、じゃんけんな」。
[間0.5][速0.85]私、勝てたことは、ありません。
あの子は、いつも強かった。
そういえば、風邪で学校を休んだ日。
同じ班の子が、家まで届けてくれました。
ナフキンに包まれた、少し冷めたコッペパン。
[速0.82][後間0.8]熱でぼんやりした頭で食べた、あの味。"""

TAG_RE = re.compile(r"^((?:\[[^\[\]]+\])+)")
NUM_RE = re.compile(r"^(速|抑揚|間|後間)([\d.]+)$")


def parse_line(raw):
    line = raw.strip()
    tags = {"speed": BASE_SPEED, "into": BASE_INTO, "pre": 0.0, "post": 0.0}
    m = TAG_RE.match(line)
    if m:
        for tag in re.findall(r"\[([^\[\]]+)\]", m.group(1)):
            n = NUM_RE.match(tag.strip())
            if n:
                k, v = n.group(1), float(n.group(2))
                tags[{"速": "speed", "抑揚": "into", "間": "pre", "後間": "post"}[k]] = v
        line = line[m.end():]
    return line, tags


def synth(text, speed, into):
    q = urllib.parse.urlencode({"text": text, "speaker": SPEAKER})
    req = urllib.request.Request(f"{VV}/audio_query?{q}", data=b"", method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        query = json.loads(r.read())
    query["speedScale"] = speed
    query["intonationScale"] = into
    req = urllib.request.Request(f"{VV}/synthesis?speaker={SPEAKER}",
                                 data=json.dumps(query).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def build(passage, name):
    frames, params = [], None
    for raw in passage.splitlines():
        if not raw.strip():
            continue
        text, tg = parse_line(raw)
        wav = synth(text, tg["speed"], tg["into"])
        with wave.open(io.BytesIO(wav)) as w:
            if params is None:
                params = w.getparams()
            sr, sw, ch = w.getframerate(), w.getsampwidth(), w.getnchannels()
            pre = b"\x00" * int(sr * (GAP + tg["pre"])) * sw * ch
            post = b"\x00" * int(sr * tg["post"]) * sw * ch
            frames.append(pre + w.readframes(w.getnframes()) + post)
        print(f"  ok [{tg['speed']:.2f}/{tg['into']:.2f}] {text[:24]}")
    out = os.path.join(OUT, name)
    with wave.open(out, "wb") as w:
        w.setparams(params)
        w.writeframes(b"".join(frames))
    print("->", out)


if __name__ == "__main__":
    print("A: dinh tra do gia")
    build(PASSAGE_A, "demo_A_kaitou.wav")
    print("B: okawari janken")
    build(PASSAGE_B, "demo_B_janken.wav")
