# -*- coding: utf-8 -*-
"""Xuất 4 wav demo giọng cho kênh kaigo (VOICEVOX :50021)."""
import io, sys, json, urllib.parse, urllib.request, wave
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:50021"
OUT = Path(r"E:\Claude\Projects\youtube-jp-kaigo\00_VOICE_TEST")
OUT.mkdir(parents=True, exist_ok=True)

TEXT = [
    "お母さんの通帳が、ある日、使えなくなります。",
    "認知症と診断された、その日からです。",
    "施設の見積りは、月十四万円。お母さんの年金は、九万円。",
    "差額の五万円は、あなたが払うことになります。",
    "ですが、その通帳が凍る前に、できることが三つあります。",
    "このノートでは、制度の説明ではなく、あなたのご実家の数字を、一緒に計算していきます。",
    "まず、こちらをご覧ください。厚生労働省のページです。赤で囲んだところ、ご覧ください。",
]

# ứng viên: 2 nữ + 2 nam, chưa dùng ở 6 kênh kia (đã dùng: 青山龍星, 雀松朱司)
WANT = [("No.7", "ノーマル"), ("冥鳴ひまり", "ノーマル"), ("玄野武宏", "ノーマル"), ("WhiteCUL", "ノーマル")]
SPEED = 0.95

sp = json.loads(urllib.request.urlopen(BASE + "/speakers", timeout=20).read())
ids = {}
for s in sp:
    for st in s["styles"]:
        ids[(s["name"], st["name"])] = st["id"]
print("Speaker khả dụng:", len(sp))

def synth(text, sid, speed):
    q = urllib.parse.urlencode({"text": text, "speaker": sid})
    aq = json.loads(urllib.request.urlopen(urllib.request.Request(BASE + "/audio_query?" + q, method="POST"), timeout=60).read())
    aq["speedScale"] = speed
    aq["intonationScale"] = 1.1
    aq["prePhonemeLength"] = 0.1
    aq["postPhonemeLength"] = 0.35
    req = urllib.request.Request(BASE + f"/synthesis?speaker={sid}", data=json.dumps(aq).encode("utf-8"),
                                headers={"Content-Type": "application/json"}, method="POST")
    return urllib.request.urlopen(req, timeout=180).read()

for name, style in WANT:
    sid = ids.get((name, style))
    if sid is None:
        cand = [k for k in ids if k[0] == name]
        print(f"⚠️ {name}/{style} không có. Style có: {cand}")
        if not cand:
            continue
        sid = ids[cand[0]]; style = cand[0][1]
    chunks = [synth(t, sid, SPEED) for t in TEXT]
    romaji = {"No.7": "no7", "冥鳴ひまり": "meimei-himari", "玄野武宏": "kurono-takehiro", "WhiteCUL": "whitecul"}[name]
    out = OUT / f"demo_{sid}_{romaji}_{'normal'}.wav"
    with wave.open(str(out), "wb") as w:
        for i, c in enumerate(chunks):
            with wave.open(io.BytesIO(c)) as r:
                if i == 0:
                    w.setparams(r.getparams())
                    sil = b"\x00" * int(r.getframerate() * r.getsampwidth() * r.getnchannels() * 0.45)
                w.writeframes(r.readframes(r.getnframes()))
            w.writeframes(sil)
    with wave.open(str(out)) as r:
        dur = r.getnframes() / r.getframerate()
    print(f"✅ {name}/{style} (id {sid}) -> {out.name}  {dur:.1f}s")
print("=== DONE ===")
