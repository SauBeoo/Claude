# -*- coding: utf-8 -*-
"""Demo giong cho kenh 地形と地名の日本史 — 4 ung vien nam."""
import io,sys,json,urllib.request,urllib.parse,subprocess
from pathlib import Path
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
HOST="http://127.0.0.1:50021"
OUT=Path(__file__).resolve().parents[1]/"00_VOICE_TEST"; OUT.mkdir(exist_ok=True)
TEXT=[
 "東京、渋谷。スクランブル交差点の、あの人混みです。",
 "あそこが、なぜ「谷」と呼ばれるのか、考えたことはありますか。",
 "地図を、二百年、巻き戻してみます。",
 "そこには、川が流れていました。渋谷川です。",
 "町の名前は、消えた川の、最後の住所録なんです。",
]
CAND=[("kigashima_sourin",53,0.90,1.10),("aoyama_ryusei",13,0.90,1.05),
      ("no7_announce",30,0.90,1.05),("kurono_takehiro",11,0.90,1.10)]
def synth(text,sid,speed,into):
    q=json.load(urllib.request.urlopen(urllib.request.Request(
        f"{HOST}/audio_query?text={urllib.parse.quote(text)}&speaker={sid}",method="POST"),timeout=30))
    q["speedScale"]=speed; q["intonationScale"]=into; q["prePhonemeLength"]=0.1; q["postPhonemeLength"]=0.3
    return urllib.request.urlopen(urllib.request.Request(
        f"{HOST}/synthesis?speaker={sid}",data=json.dumps(q).encode(),
        headers={"Content-Type":"application/json"},method="POST"),timeout=120).read()
for name,sid,sp,it in CAND:
    parts=[]
    for i,t in enumerate(TEXT):
        p=OUT/f"_{name}_{i}.wav"; p.write_bytes(synth(t,sid,sp,it)); parts.append(p)
    lst=OUT/f"_{name}.txt"
    lst.write_text("\n".join(f"file '{p.name}'" for p in parts),encoding="utf-8")
    dst=OUT/f"demo_{name}.wav"
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0",
                    "-i",str(lst),"-c","copy",str(dst)],check=True)
    for p in parts: p.unlink()
    lst.unlink()
    print("OK",dst.name)
