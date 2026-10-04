# -*- coding: utf-8 -*-
"""Xuất wav demo giọng cho kênh akiya (実家とお金の整理ノート) — VOICEVOX :50021.

Đoạn mẫu = cold open khuôn 期限型 của video 01 (相続登記 2027-03-31) + 1 câu 原典ショット,
để nghe đúng chất giọng lúc đọc SỐ và lúc đọc câu dẫn tài liệu.
Ứng viên: KHÔNG dùng lại 青山龍星 (health/co-dai/shokutaku), 雀松朱司 (nenkin),
WhiteCUL/No.7 (kaigo) — 2 kênh info JP không được nghe giống nhau.
"""
import io, sys, json, urllib.parse, urllib.request, wave
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:50021"
OUT = Path(r"E:\Claude\Projects\youtube-jp-akiya\00_VOICE_TEST")
OUT.mkdir(parents=True, exist_ok=True)

TEXT = [
    "お父さんが亡くなって、三年。ご実家の名義は、まだ、お父さんのままではありませんか。",
    "その手続きの期限は、二千二十七年三月三十一日です。",
    "過ぎると、十万円以下の過料の対象になります。",
    "そして、名義が変わっていない家は、売ることも、貸すこともできません。",
    "ですが、間に合わない人のために、三か月でできる手続きもあります。",
    "このノートでは、制度の説明ではなく、あなたのご実家に、これからいくらかかるのかを、一緒に数えていきます。",
    "まず、こちらをご覧ください。法務省のページです。赤で囲んだところ、ご覧ください。",
]

# 3 nam trung tính + 1 nữ điềm đạm (đều chưa dùng ở 7 kênh kia)
WANT = [("玄野武宏", "ノーマル"), ("麒ヶ島宗麟", "ノーマル"), ("剣崎雌雄", "ノーマル"), ("冥鳴ひまり", "ノーマル")]
ROMAJI = {"玄野武宏": "kurono-takehiro", "麒ヶ島宗麟": "kigashima-sourin",
          "剣崎雌雄": "kenzaki-mesuo", "冥鳴ひまり": "meimei-himari"}
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
    out = OUT / f"demo_{sid}_{ROMAJI.get(name, name)}_normal.wav"
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
