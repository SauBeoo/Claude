# -*- coding: utf-8 -*-
"""Tai UNG VIEN Pexels cho vat trung tinh (khong lo nam) video 06 -> 1 sheet/query de duyet MAT.
Loc SO DEN: id da used_in o INDEX.json kho chung (media-library §2)."""
import io,sys,json,requests,time
from pathlib import Path
from PIL import Image, ImageDraw
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8",errors="replace")
KEY=open(r"E:\Claude\Projects\youtube-jp-health\tools\.pexels_key",encoding="utf-8").read().strip(); H={"Authorization":KEY}
OUT=Path(r"E:\Claude\Projects\youtube-jp-showa\06_VIDEO\06_shokyu-kakeibo\_px_candidates"); OUT.mkdir(parents=True,exist_ok=True)
idx=json.load(open(r"E:\Claude\Projects\_media_library\INDEX.json",encoding="utf-8"))
used=set()
for k,v in (idx.items() if isinstance(idx,dict) else []):
    if isinstance(v,dict) and v.get("used_in") and v.get("source")=="pexels": used.add(str(v.get("source_id")))
Q={
 "envelope":"brown paper envelope on wooden desk","envelope_hands":"hands holding brown envelope","coins_yen":"japanese yen coins closeup",
 "banknotes_count":"counting banknotes hands","passbook":"bank passbook open","stamp_inkpad":"rubber stamp ink pad wooden counter",
 "watch_vintage":"vintage wristwatch leather strap closeup","watch_case":"watch shop glass display case","tatami_room":"tatami room japan interior empty",
 "futon":"folded futon tatami","radio_vintage":"vintage valve radio","sento_faucet":"brass faucet tiled wall bathhouse","sento_basin":"yellow plastic basin bath japan",
 "sento_stool":"wooden bath stool japan","steam_bath":"steam bathhouse japan","rice_bowl":"bowl of white rice japanese","miso_soup":"miso soup bowl",
 "rice_sack":"rice sack burlap","meal_tray_japanese":"japanese meal tray rice fish miso","ramen_bowl":"ramen bowl steam closeup","ramen_yatai":"ramen stall night lantern japan",
 "chopsticks_noodles":"chopsticks lifting noodles steam","cinema_seats":"old cinema red seats empty","cinema_curtain":"theatre velvet curtain","projector_beam":"film projector light beam dark",
 "cigarette_match":"match flame cigarette dark","ashtray_glass":"glass ashtray cigarette","smoke_streetlight":"smoke under street light night","kissaten":"retro japanese coffee shop interior",
 "coffee_cup_saucer":"coffee cup saucer dark wood table","record_player":"vintage record player wooden","letter_paper":"handwritten letter paper hands","post_office_counter":"post office counter wooden japan",
 "sewing_machine":"vintage treadle sewing machine","tea_field":"tea plantation japan","country_station":"rural train station japan night","newyear_cards":"postcards stack table",
 "drawer_old":"old wooden drawer open","night_street_japan":"quiet night street japan lantern","dorm_corridor":"old wooden corridor japan house","shoes_entrance":"shoes lined up genkan japan",
}
for key,q in Q.items():
    r=requests.get("https://api.pexels.com/v1/search",params=dict(query=q,per_page=12,orientation="landscape"),headers=H,timeout=60).json()
    ph=[p for p in r.get("photos",[]) if str(p["id"]) not in used][:8]
    ims=[]
    for p in ph:
        dst=OUT/f"{key}__{p['id']}.jpg"
        if not dst.exists(): dst.write_bytes(requests.get(p["src"]["large"],timeout=60).content)
        ims.append((p["id"],dst))
    if not ims: print(key,"0"); continue
    W,Hh=320,180; sh=Image.new("RGB",(W*4,Hh*2),"black"); d=ImageDraw.Draw(sh)
    for i,(pid,dst) in enumerate(ims[:8]):
        im=Image.open(dst).convert("RGB"); im.thumbnail((W,Hh)); sh.paste(im,((i%4)*W,(i//4)*Hh)); d.rectangle(((i%4)*W,(i//4)*Hh,(i%4)*W+90,(i//4)*Hh+13),fill="black"); d.text(((i%4)*W+3,(i//4)*Hh+1),str(pid),fill="yellow")
    sh.save(OUT/f"sheet_{key}.jpg",quality=82); print(key,len(ims)); time.sleep(0.5)
