import json,os,shutil,sys
from PIL import Image
B='C:/Users/permr/fl_work/wsb/'
d=json.load(open(B+'_variants/brief/shotlist.json',encoding='utf-8'))
T={t['id']:t for t in d['timeline']}
NAMES={}
for k,v in {**d['characters'],**d['props'],**d['locations']}.items():
    NAMES[k]=(v.get('name') if isinstance(v,dict) else None) or k
def label(base):
    key=base.rsplit('_',1)[0] if base.split('_')[-1] in ('front','full','34','B') else base
    key=base.replace('_full_B','').replace('_front','').replace('_full','').replace('_34','')
    nm=NAMES.get(key,key)
    if '_front' in base: return f'{nm}, FACE reference (use this exact face)'
    if '_full_B' in base: return f'{nm}, FULL-BODY reference, OUTFIT B (green gingham dress, low bun)'
    if '_full' in base: return f'{nm}, FULL-BODY reference' + (' (shows the ivory wedding dress = OUTFIT A; use it for face, hair and build, and wear that dress ONLY if the scene says OUTFIT A)' if key=='CHAR_ROSE' else '')
    return f'{nm}, reference image'
def stage(i):
    t=T[i]; out=B+f'_variants/stage/{i}/'
    shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
    refs=[os.path.basename(r)[:-4] for r in t['ref_files']]
    lines=[]
    for n,r in enumerate(refs,1):
        shutil.copy(B+f'_variants/up/{r}.jpg', out+f'{n:02d}_{r}.jpg'); lines.append(f'{n:02d}_{r}.jpg = {label(r)}')
    txt=('Create an image, wide 16:9 landscape format, photorealistic film still.\n'
     + ('The attached reference images (file names are numbered):\n'+'\n'.join(lines)+
        '\nUse the references: every person must have EXACTLY the face, hair and clothing of their reference; places and props must match their references. Do not put any of the reference files themselves into the picture; do not add any text or lettering.\n' if refs else '')
     + '\nSCENE:\n'+t['full_prompt']+'\n')
    open(out+f'00_prompt_{i}.txt','w',encoding='utf-8').write(txt)
    return sorted(os.listdir(out))
if __name__=='__main__':
    for i in sys.argv[1:]: print(i, stage(i))
