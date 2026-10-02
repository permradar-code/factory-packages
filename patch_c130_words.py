import json
p='c130final/timings/words.json'; w=json.load(open(p))
def merge(seq, joined):
    global w
    out=[];i=0
    while i<len(w):
        if [x['word'] for x in w[i:i+len(seq)]]==seq:
            out.append({'word':joined,'start':w[i]['start'],'end':w[i+len(seq)-1]['end']}); i+=len(seq)
        else: out.append(w[i]); i+=1
    w=out
for seq,j in [(['four','engine'],'four-engine'),(['C','130'],'C-130'),(['touch','and','goes'],'touch-and-goes'),
              (['full','stop'],'full-stop'),(['121','000'],'121,000'),(['Lt'],'Lieutenant')]:
    merge(seq,j)
# garbled region: 'for','a','plane','cross' -> real words with timings from silence analysis
i=next(k for k,x in enumerate(w) if x['word']=='plane' and x['start']>83)
assert w[i-2]['word']=='for' and w[i+1]['word']=='cross', [x['word'] for x in w[i-3:i+3]]
def spread(words,t0,t1):
    L=sum(len(x)+1 for x in words);t=t0;r=[]
    for x in words:
        d=(t1-t0)*(len(x)+1)/L; r.append({'word':x,'start':round(t,3),'end':round(t+d-0.02,3)}); t+=d
    return r
new=[w[i-2]]+spread(['a','crowded','deck','every','single','day'],79.36,81.12)+spread(['Flatley','gets','the','Distinguished','Flying','Cross'],82.05,83.93)
w=w[:i-2]+new+w[i+2:]
json.dump(w,open(p,'w'),indent=0)
m=json.load(open('c130final/manifest.json'))
fix={'006':24.96,'017':82.05}
for s in m['scenes']:
    if s['shot_id'] in fix: s['start']=fix[s['shot_id']]
json.dump(m,open('c130final/manifest.json','w'),indent=1)
print([(s['shot_id'],round(s['start'],2)) for s in m['scenes']])
