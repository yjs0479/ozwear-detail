import os, sys, json, math, html
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import os as _os; D=_os.path.dirname(_os.path.abspath(__file__)); SRC=D+'/src'; AS=D+'/assets'; OUT=D+'/out'
os.makedirs(AS,exist_ok=True); os.makedirs(OUT,exist_ok=True)
KIDS_CP='/mnt/user-data/outputs/kids/에버어그_아동사이즈_쿠팡_780px.jpg'
KIDS_NV='/mnt/user-data/outputs/kids/에버어그_아동사이즈_네이버_860px.jpg'

def prep(code,name,pad=0.04,maxw=1400):
    """trim white margins, add small even padding, save png in assets"""
    p=f'{SRC}/{code}/{name}'; im=Image.open(p).convert('RGB')
    a=np.asarray(im).astype(int); m=(a.min(axis=2)<238)
    ys,xs=np.where(m)
    if len(ys):
        im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    w,h=im.size; e=int(max(w,h)*pad)
    c=Image.new('RGB',(w+2*e,h+2*e),'white'); c.paste(im,(e,e)); c.thumbnail((maxw,maxw))
    out=f'{AS}/{code}_{os.path.splitext(name)[0][-40:]}.jpg'; c.save(out,quality=92); return out

CSS='''
*{box-sizing:border-box;margin:0;padding:0}
body{width:780px;font-family:'Noto Sans CJK KR','Noto Sans KR',sans-serif;color:#3b2a1e;background:#fff;-webkit-font-smoothing:antialiased}
.sec{padding:70px 40px;text-align:center}
.beige{background:#f8f1e7}.white{background:#fff}.dark{background:#3e2a1d;color:#fff}.sand{background:#efe5d6}
.eb{font-size:15px;letter-spacing:5px;font-weight:700;color:#b8925f;margin-bottom:14px}
.dark .eb{color:#c9a46c}
.en{font-family:'Noto Serif CJK KR','Noto Serif',serif;font-size:26px;letter-spacing:2px;color:#a9824f;margin-bottom:12px}
h1{font-size:40px;line-height:1.38;font-weight:900;color:#3b2a1e}
h2{font-size:34px;line-height:1.4;font-weight:900;color:#3b2a1e;margin-bottom:18px}
.dark h2{color:#fff;font-size:40px}
h2 em{font-style:normal;color:#c9a46c}
.div{width:60px;height:2px;background:#c9a46c;margin:26px auto}
.p{font-size:19px;line-height:1.75;color:#5a4636}
.dark .p{color:#e8dccb}
.p b{color:#3b2a1e}.dark .p b{color:#fff}
.chips{margin-top:26px}
.chip{display:inline-block;border:1.5px solid #b8925f;border-radius:30px;padding:9px 20px;font-size:17px;font-weight:700;margin:0 4px;background:#fff}
.photo{display:block;width:100%;margin:0 auto}
.ph{padding:30px 40px;background:#fff}
.ph img{width:100%;display:block}
.two{display:flex;gap:16px;padding:20px 40px;background:#fff}.two img{width:50%;display:block}
.cards3{display:flex;gap:14px;margin-top:34px}
.card{flex:1;background:#f8f1e7;border-radius:14px;padding:26px 12px;text-align:center}
.card .t{font-size:19px;font-weight:800;margin-bottom:10px}
.card .d{font-size:15px;line-height:1.6;color:#6b5646}
.white .card{background:#f8f1e7}.beige .card,.sand .card{background:#fff}
.pill{display:inline-block;background:#4a3324;color:#f0dcc0;border-radius:20px;padding:7px 18px;font-size:13px;letter-spacing:3px;font-weight:700;margin-bottom:16px}
table.cmp{width:100%;border-collapse:collapse;margin-top:34px;font-size:16px}
table.cmp th{background:#4a3324;color:#fff;padding:14px 8px;font-weight:700}
table.cmp th.hl{background:#c9a46c}
table.cmp td{padding:14px 8px;border-bottom:1px solid #eadfce;color:#5a4636}
table.cmp td.k{font-weight:700;text-align:left;padding-left:16px;color:#3b2a1e}
table.cmp td.hl{background:#f8f1e7;font-weight:700;color:#3b2a1e}
.note{font-size:13px;color:#9a8775;margin-top:14px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:30px;text-align:left}
.g{background:#fff;border-radius:14px;padding:24px 22px}
.g .t{font-size:19px;font-weight:800;margin-bottom:8px}.g .d{font-size:15px;color:#6b5646;line-height:1.6}
.colors{display:grid;gap:16px;margin-top:30px}
.cc{background:#fff;border-radius:16px;padding:18px 18px 22px}
.cc img{width:100%;display:block;margin-bottom:14px}
.cc .k{font-size:19px;font-weight:800}.cc .e{font-size:12px;letter-spacing:3px;color:#9a8775;margin-top:4px}
table.info{width:100%;border-collapse:collapse;margin-top:30px;font-size:16px;text-align:left;border-top:2px solid #4a3324}
table.info td{padding:16px 18px;border-bottom:1px solid #eadfce;line-height:1.5}
table.info td.k{width:30%;background:#f8f1e7;font-weight:700;color:#3b2a1e}
table.info td.v{color:#5a4636}
.szimg{display:block;width:100%}
.szbox{background:#fff;border-radius:16px;padding:30px 26px;margin-top:26px;text-align:left}
table.gs{width:100%;border-collapse:collapse;font-size:22px;text-align:center;border:3px solid #6b4429}
table.gs th{background:#7a5236;color:#fff;padding:18px 6px;font-size:20px;border:2px solid #6b4429}
table.gs td{padding:24px 6px;border:2px solid #6b4429;font-weight:900;font-size:30px}
table.gs tr:nth-child(odd) td{background:#f5e6d8}
'''

def esc(s): return s
def build(P, W, sizechart_img):
    S=[]
    S.append(f'''<div class="sec beige" style="padding:70px 40px 60px"><div class="eb">AUSTRALIAN SHEPHERD® UGG · {P['code']}</div><div class="en">{P['en']}</div><h1>{'<br>'.join(P['title'])}</h1><div class="div"></div><div class="p" style="font-size:18px">{'<br>'.join(P['mat'])}</div><div class="chips">{''.join(f'<span class="chip">{c}</span>' for c in P['chips'])}</div></div>''')
    S.append('<!--TOPBLOCK-->')
    S.append(f'<div class="ph" style="padding:40px 30px 30px"><img src="file://{P["hero"]}"></div>')
    S.append(f'''<div class="sec beige"><div class="eb">{P['tag_eb']}</div><h2>{'<br>'.join(P['tag_h'])}</h2><div class="div" style="margin:20px auto"></div><div class="p">{'<br>'.join(P['tag_p'])}</div></div>''')
    S.append(f'''<div class="sec white"><div class="eb">GENUINE AUSTRALIAN BRAND</div><h2>호주 브랜드 정품의 증거</h2><div class="p">호주 브랜드 <b>AUSTRALIAN SHEPHERD®</b>가 디자인하고<br>브랜드 기준에 맞춰 생산된 정품입니다.</div><img class="photo" style="margin-top:36px" src="file://{P['proof']}"><div class="cards3"><div class="card"><div class="t">정품 로고</div><div class="d">제품에 새겨진<br>브랜드 로고</div></div><div class="card"><div class="t">호주 디자인</div><div class="d">호주 브랜드가<br>직접 디자인한<br>오리지널 모델</div></div><div class="card"><div class="t">판매 인증</div><div class="d">브랜드에서<br>발급한<br>판매 인증서<br>보유 판매처</div></div></div></div>''')
    S.append(f'''<div class="sec dark" style="padding:80px 40px"><div class="eb">PREMIUM MATERIALS</div><h2>{P['dark_h']}</h2><div class="p">{'<br>'.join(P['dark_p'])}</div></div>''')
    for blk in P['materials']:
        if blk.get('photos'):
            if len(blk['photos'])==2: S.append('<div class="two" style="padding:40px 40px 10px">'+''.join(f'<img src="file://{x}">' for x in blk['photos'])+'</div>')
            else: S.append(f'<div class="ph" style="padding:40px 40px 10px"><img src="file://{blk["photos"][0]}"></div>')
        h=f'''<div class="sec white" style="padding:40px 40px 60px"><div class="pill">{blk['pill']}</div><h2>{blk['h']}</h2><div class="p">{'<br>'.join(blk['p'])}</div>'''
        if blk.get('cards'): h+='<div class="cards3">'+''.join(f'<div class="card"><div class="t">{t}</div><div class="d">{d}</div></div>' for t,d in blk['cards'])+'</div>'
        if blk.get('cmp'):
            h+='<table class="cmp"><tr><th></th><th class="hl">'+blk['cmp'][0][0]+'</th><th>'+blk['cmp'][0][1]+'</th></tr>'+''.join(f'<tr><td class="k">{k}</td><td class="hl">{a}</td><td>{b}</td></tr>' for k,a,b in blk['cmp'][1:])+'</table><div class="note">※ 일반적인 소재 특성 비교입니다.</div>'
        S.append(h+'</div>')
    S.append('<div class="sec beige"><div class="eb">POINT</div><h2>이 제품을 고르는 이유</h2><div class="grid2">'+''.join(f'<div class="g"><div class="t">{t}</div><div class="d">{d}</div></div>' for t,d in P['points'])+'</div></div>')
    n=len(P['colors']); cols=2 if n in (2,4) else 3
    S.append(f'<div class="sec sand"><div class="eb">COLOR</div><h2>{n}가지 컬러</h2><div class="colors" style="grid-template-columns:repeat({cols},1fr)">'+''.join(f'<div class="cc"><img src="file://{img}"><div class="k">{k}</div><div class="e">{e}</div></div>' for k,e,img in P['colors'])+'</div></div>')
    S.append('<div class="sec white" style="padding-bottom:20px"><div class="eb">DETAIL</div><h2>디테일까지 꼼꼼하게</h2></div>')
    for row in P['details']:
        if len(row)==2: S.append('<div class="two">'+''.join(f'<img src="file://{x}">' for x in row)+'</div>')
        else: S.append(f'<div class="ph" style="padding:16px 40px"><img src="file://{row[0]}"></div>')
    S.append('<div class="sec white"><div class="eb">INFORMATION</div><h2>제품 정보</h2><table class="info">'+''.join(f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>' for k,v in P['info'])+'</table></div>')
    if sizechart_img: S.append(f'<img class="szimg" src="file://{sizechart_img}">')
    elif P.get('size_html'): S.append(P['size_html'])
    body='\n'.join(S)
    return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

def render(htmlstr, W, path):
    parts=htmlstr.split('<!--TOPBLOCK-->')
    outs=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for i,part in enumerate(parts):
            if i==1: part='<html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+part
            if i==0 and len(parts)>1: part=part+'</body></html>'
            pg=b.new_page(viewport={'width':780,'height':50},device_scale_factor=W/780)
            hf=f'{path}_part{i}.html'; open(hf,'w').write(part)
            pg.goto('file://'+hf); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(400)
            fn=f'{path}_part{i}.png'; pg.screenshot(path=fn,full_page=True); outs.append(fn)
        b.close()
    return outs

def assemble(parts, top, bot, W, out, hero_for_box=None, box=None):
    ims=[Image.open(p).convert('RGB') for p in parts]
    ims=[im.resize((W,round(im.height*W/im.width))) if im.width!=W else im for im in ims]
    T=Image.open(top).convert('RGB')
    if hero_for_box and box:
        x0,y0,x1,y1=box; T=T.copy()
        from PIL import ImageDraw
        ImageDraw.Draw(T).rectangle((x0,y0,x1,y1),fill='white')
        h=Image.open(hero_for_box).convert('RGB'); h.thumbnail((x1-x0-40,y1-y0-30))
        T.paste(h,(x0+(x1-x0-h.width)//2,y0+(y1-y0-h.height)//2))
    Bt=Image.open(bot).convert('RGB')
    seq=[ims[0],T]+ims[1:]+[Bt]
    H=sum(i.height for i in seq); F=Image.new('RGB',(W,H),'white'); y=0
    for i in seq: F.paste(i,(0,y)); y+=i.height
    F.save(out,quality=92); return F
