# -*- coding: utf-8 -*-
"""trend30.py — do Trends YouTube Search 30d + web 12m cho ro keyword video 30 (10月15日 支給日直前チェック)."""
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from pytrends.request import TrendReq

ROS = [
    ["年金", "年金振込", "年金支給日", "介護保険料", "年金 手取り"],
    ["年金", "年金振込通知書", "年金 天引き", "介護保険料 10月", "住民税 年金"],
]
def run(kws, gprop, tf, label):
    py = TrendReq(hl="ja-JP", tz=-540)
    py.build_payload(kws, cat=0, timeframe=tf, geo="JP", gprop=gprop)
    df = py.interest_over_time()
    print(f"\n### {label}  tf={tf} gprop={gprop or 'web'}")
    if df is None or df.empty:
        print("   (rong)"); return
    if "isPartial" in df: df = df.drop(columns=["isPartial"])
    for c in df.columns:
        nz = int((df[c] > 0).sum())
        print(f"   {c:<22} mean {df[c].mean():>6.2f} | max {df[c].max():>3} | nz {nz}/{len(df)}")

for ro in ROS:
    for gprop, tf, label in [("youtube", "today 1-m", "YouTube Search 30d"),
                             ("",        "today 12-m", "Web 12 thang")]:
        try:
            run(ro, gprop, tf, label)
        except Exception as e:
            print(f"   [LOI] {e}")
        time.sleep(3)
