import json,os,shutil,sys
from PIL import Image
sys.path.insert(0,'C:/Users/permr/fl_work/wsb/_variants')
import build_stage as b
B=b.B
def stage(cid,kind):
    t=b.T[cid]; key='start_frame_full_prompt' if kind=='first' else 'end_frame_full_prompt'
    out=B+f'_variants/stage/{cid}_{kind}/'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
    refs=[os.path.basename(r)[:-4] for r in t['ref_files']]
    files=[]; lines=[]
    if kind=='last':
        im=Image.open(B+f'visuals/images/{cid}_first.png').convert('RGB'); im.thumbnail((1024,1024)); im.save(out+'01_FIRST_FRAME.jpg',quality=88)
        lines.append('01_FIRST_FRAME.jpg = the FIRST FRAME of this same shot: keep exactly the same people, faces, costumes, place, light and style; only the moment is later')
        n0=2
    else: n0=1
    for n,r in enumerate(refs,n0):
        shutil.copy(B+f'_variants/up/{r}.jpg',out+f'{n:02d}_{r}.jpg'); lines.append(f'{n:02d}_{r}.jpg = {b.label(r)}')
    txt=('Create an image, wide 16:9 landscape format, photorealistic film still.\nThe attached reference images (file names are numbered):\n'+'\n'.join(lines)+
     '\nUse the references: every person must have EXACTLY the face, hair and clothing of their reference; places and props must match their references. Do not put any of the reference files themselves into the picture; do not add any text or lettering.\n\nSCENE:\n'+t[key]+'\n')
    open(out+f'00_prompt_{cid}_{kind}.txt','w',encoding='utf-8').write(txt)
    return sorted(os.listdir(out))
if __name__=='__main__':
    for a in sys.argv[1:]:
        cid,kind=a.split(':'); print(a,stage(cid,kind))
