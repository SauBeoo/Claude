import sys, json, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pytrends.request import TrendReq
py = TrendReq(hl="ja-JP", tz=-540)
ANCHOR = "嫌われる勇気"
cands = ["人の目","人の目が気になる","他人の目","気にしない","期待しない","比べない","いい人","口癖","一人が好き","群れない","気にしすぎ","心理学 60代","自分らしく","八方美人"]
res = {}
for i in range(0, len(cands), 4):
    grp = [ANCHOR] + cands[i:i+4]
    py.build_payload(grp, timeframe="today 1-m", geo="JP", gprop="youtube")
    df = py.interest_over_time()
    for k in grp:
        if k in df: res.setdefault(k, []).append(round(float(df[k].mean()), 1))
    time.sleep(2)
anc = res[ANCHOR]
out = {}
for k, v in res.items():
    if k == ANCHOR: continue
    # rescale each group to anchor=27.2 scale (niche research scale, 自己肯定感=100)
    out[k] = v
for k in cands:
    print(k, res.get(k), "| anchor", anc)
rel = {}
for k in ["人の目","他人の目","気にしない","期待しない","いい人"]:
    try:
        py.build_payload([k], timeframe="today 1-m", geo="JP", gprop="youtube")
        r = py.related_queries()[k]
        rel[k] = {"top": r["top"].head(8).values.tolist() if r["top"] is not None else [], "rising": r["rising"].head(6).values.tolist() if r["rising"] is not None else []}
        print(k, rel[k])
    except Exception as e:
        print(k, "ERR", e)
    time.sleep(2)
json.dump({"anchor": ANCHOR, "anchor_vals": anc, "scores": res, "related": rel}, open("trends_2026-09-30.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
