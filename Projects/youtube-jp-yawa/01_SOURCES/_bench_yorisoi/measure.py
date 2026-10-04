import subprocess, numpy as np, sys, io, json
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
f=sys.argv[1]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
W,H,FPS=64,26,2   # crop 72% top (bo dai phu de), 2 frame/s
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'fps={FPS},crop=iw:ih*0.72:0:0,scale={W}:{H},format=gray','-f','rawvideo','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(np.float32)
d=np.abs(np.diff(a,axis=0)).mean(axis=(1,2)); t=np.arange(1,len(a))/FPS
res={'file':f,'dur':round(dur,1),'static_pct(MAD<0.5)':round(float((d<0.5).mean()*100),1),'mad_med':round(float(np.median(d)),2),'mad_mean':round(float(d.mean()),2)}
for th in (6,10,15,25):
    ev=[]
    for ti in t[d>th]:
        if not ev or ti-ev[-1]>1.5: ev.append(float(ti))
    holds=np.diff([0]+ev+[dur])
    res[f'th{th}']=dict(cuts=len(ev),per_min=round(len(ev)/(dur/60),2),hold_med=round(float(np.median(holds)),1),hold_p90=round(float(np.percentile(holds,90)),1),first60=sum(1 for e in ev if e<60))
print(json.dumps(res,ensure_ascii=False))
