import re,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
def load(f):
    out=[];last=''
    blocks=open(f,encoding='utf-8').read().split('\n\n')
    for b in blocks:
        m=re.search(r'(\d\d):(\d\d):(\d\d)\.\d+ -->',b)
        if not m: continue
        t=int(m[1])*3600+int(m[2])*60+int(m[3])
        lines=[re.sub(r'<[^>]+>','',l).strip() for l in b.split('\n')[1:]]
        lines=[l for l in lines if l and '-->' not in l]
        for l in lines:
            if l!=last and not last.endswith(l):
                out.append((t,l)); last=l
    return out
for f in sys.argv[1:]:
    seg=load(f); txt=''.join(l for _,l in seg)
    open(f.replace('.ja.vtt','.txt'),'w',encoding='utf-8').write('\n'.join('%02d:%02d %s'%(t//60,t%60,l) for t,l in seg))
    print(f,len(seg),'segs',len(txt),'chars', 'chars/min %.0f'%(len(txt)/(seg[-1][0]/60)))
