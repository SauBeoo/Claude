import sys
sys.path.insert(0,r'E:\Claude\Projects\youtube-jp-showa\tools')
import build_scenes_08 as B
B.REAL.mkdir(exist_ok=True)
ok=0
for k in B.PX:
    try: B.px_original(k); ok+=1
    except SystemExit as e: print('FAIL',k,e)
print('prefetched',ok,'/',len(B.PX))
