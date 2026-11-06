# OZWEAR accessory detail-page generator (based on gen.py format; CS095-style)
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import CSS as BASECSS
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__))
STG = '/mnt/user-data/uploads/Documents/클로드/운영/20261101/ozw_prep/stage'
AS = D + '/assets_ozw'; OUT = D + '/out_ozw2'
os.makedirs(AS, exist_ok=True); os.makedirs(OUT, exist_ok=True)

CSS = BASECSS + '''
.szwrap{background:#fff;border-radius:16px;padding:34px 26px;margin-top:26px}
table.sz{width:100%;border-collapse:collapse;text-align:center;border:3px solid #6b4429}
table.sz th{background:#7a5236;color:#fff;padding:20px 6px;font-size:24px;font-weight:900;border:2px solid #6b4429}
table.sz td{padding:26px 6px;border:2px solid #6b4429;font-weight:900;font-size:34px;color:#3b2a1e;background:#f5e6d8}
table.sz td.s{font-size:24px;font-weight:800;background:#fff}
.sznote{font-size:18px;line-height:1.7;color:#5a4636;margin-top:22px;text-align:left}
'''

def prep(code, idx, pad=0.04, trim=True, maxw=1400, tag=''):
    p = f'{STG}/{code}/{idx:02d}.jpg'
    im = Image.open(p).convert('RGB')
    if trim:
        a = np.asarray(im).astype(int); m = (a.min(axis=2) < 232)
        ys, xs = np.where(m)
        if len(ys) and (xs.max()-xs.min()) > 50:
            im = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))
        w, h = im.size; e = int(max(w, h)*pad)
        A0 = np.asarray(Image.open(p).convert('RGB'))
        cs = [A0[3, 3], A0[3, -4], A0[-4, 3], A0[-4, -4]]
        if min(int(x.mean()) for x in cs) >= 215:
            bg = tuple(int(v) for v in np.median(np.array(cs), axis=0))
            c = Image.new('RGB', (w+2*e, h+2*e), bg); c.paste(im, (e, e)); im = c
        else:
            im = Image.open(p).convert('RGB')
    im.thumbnail((maxw, maxw*2))
    out = f'{AS}/{code}_{idx:02d}{tag}.jpg'; im.save(out, quality=92); return out

def L(x): return '<br>'.join(x) if isinstance(x, (list, tuple)) else x

def build(P):
    S = []
    S.append(f'''<div class="sec beige" style="padding:70px 40px 60px"><div class="eb">OZWEAR® UGG · {P['code']}</div><div class="en">{P['en']}</div><h1>{L(P['title'])}</h1><div class="div"></div><div class="p" style="font-size:18px">{L(P['mat'])}</div><div class="chips">{''.join(f'<span class="chip">{c}</span>' for c in P['chips'])}</div></div>''')
    S.append('<!--TOPBLOCK-->')
    S.append(f'''<div class="sec beige" style="padding:60px 40px 40px"><div class="eb">{P['tag_eb']}</div><h2>{L(P['tag_h'])}</h2><div class="div" style="margin:20px auto"></div><div class="p">{L(P['tag_p'])}</div></div>''')
    S.append(f'<div class="ph" style="padding:30px 30px 40px;background:#fff"><img src="file://{P["hero"]}"></div>')
    for blk in P['materials']:
        ph = blk.get('photos') or []
        h = f'''<div class="sec white" style="padding:50px 40px 30px"><div class="pill">{blk['pill']}</div><h2>{blk['h']}</h2><div class="p">{L(blk['p'])}</div>'''
        if blk.get('cards'): h += '<div class="cards3">'+''.join(f'<div class="card"><div class="t">{t}</div><div class="d">{d}</div></div>' for t, d in blk['cards'])+'</div>'
        S.append(h+'</div>')
        if len(ph) == 2: S.append('<div class="two" style="padding:0 40px 40px">'+''.join(f'<img src="file://{x}">' for x in ph)+'</div>')
        elif len(ph) == 1: S.append(f'<div class="ph" style="padding:0 40px 40px"><img src="file://{ph[0]}"></div>')
    S.append(f'''<div class="sec beige"><div class="eb">GENUINE AUSTRALIAN BRAND</div><h2>호주 브랜드 정품의 증거</h2><div class="p">호주 브랜드 <b>OZWEAR®</b>가 디자인하고<br>브랜드 기준에 맞춰 생산된 정품입니다.</div><div class="cards3"><div class="card"><div class="t">정품 로고</div><div class="d">{P.get('logo_where','제품에 달린<br>UGG 로고')}</div></div><div class="card"><div class="t">호주 디자인</div><div class="d">호주 브랜드가<br>직접 디자인한<br>오리지널 모델</div></div><div class="card"><div class="t">판매 인증</div><div class="d">브랜드에서<br>발급한<br>판매 인증서<br>보유 판매처</div></div></div></div>''')
    S.append(f'''<div class="sec dark" style="padding:80px 40px"><div class="eb">PREMIUM MATERIALS</div><h2>{P['dark_h']}</h2><div class="p">{L(P['dark_p'])}</div></div>''')
    S.append('<div class="sec beige"><div class="eb">POINT</div><h2>이 제품을 고르는 이유</h2><div class="grid2">'+''.join(f'<div class="g"><div class="t">{t}</div><div class="d">{d}</div></div>' for t, d in P['points'])+'</div></div>')
    n = len(P['colors'])
    if n == 1:
        k, e, img = P['colors'][0]
        S.append(f'<div class="sec sand"><div class="eb">COLOR</div><h2>컬러</h2><div class="colors" style="grid-template-columns:1fr;max-width:520px;margin:30px auto 0"><div class="cc"><img src="file://{img}"><div class="k">{k}</div><div class="e">{e}</div></div></div></div>')
    else:
        cols = 2 if n in (2, 4) else 3
        S.append(f'<div class="sec sand"><div class="eb">COLOR</div><h2>{n}가지 컬러</h2><div class="colors" style="grid-template-columns:repeat({cols},1fr)">'+''.join(f'<div class="cc"><img src="file://{img}"><div class="k">{k}</div><div class="e">{e}</div></div>' for k, e, img in P['colors'])+'</div></div>')
    if P.get('details'):
        S.append('<div class="sec white" style="padding-bottom:20px"><div class="eb">DETAIL</div><h2>디테일까지 꼼꼼하게</h2></div>')
        for row in P['details']:
            if len(row) == 2: S.append('<div class="two">'+''.join(f'<img src="file://{x}">' for x in row)+'</div>')
            else: S.append(f'<div class="ph" style="padding:16px 40px"><img src="file://{row[0]}"></div>')
        S.append('<div style="height:40px;background:#fff"></div>')
    S.append('<div class="sec beige"><div class="eb">INFORMATION</div><h2>제품 정보</h2><table class="info" style="background:#fff">'+''.join(f'<tr><td class="k">{k}</td><td class="v">{v}</td></tr>' for k, v in P['info'])+'</table></div>')
    sz = P['size']
    hdr = ''.join(f'<th>{a}</th>' for a in sz['opts'])
    row = ''.join(f'<td>{b}</td>' for b in sz.get('vals', sz['opts']))
    extra = ''
    if sz.get('row2'):
        extra = '<tr>'+''.join(f'<td class="s">{b}</td>' for b in sz['row2'])+'</tr>'
    S.append(f'''<div class="sec white"><div class="eb">SIZE GUIDE</div><h2>{sz.get('h','사이즈 안내')}</h2><div class="szwrap"><table class="sz"><tr>{hdr}</tr><tr>{row}</tr>{extra}</table><div class="sznote">{L(sz['note'])}</div></div></div>''')
    body = '\n'.join(S)
    return f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'

def render(htmlstr, W, path):
    parts = htmlstr.split('<!--TOPBLOCK-->'); outs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for i, part in enumerate(parts):
            if i == 1: part = '<html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+part
            if i == 0 and len(parts) > 1: part = part+'</body></html>'
            pg = b.new_page(viewport={'width': 780, 'height': 50}, device_scale_factor=W/780)
            hf = f'{path}_part{i}.html'; open(hf, 'w').write(part)
            pg.goto('file://'+hf); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(300)
            fn = f'{path}_part{i}.png'; pg.screenshot(path=fn, full_page=True); outs.append(fn)
        b.close()
    return outs

def assemble(parts, top, bot, W, out, hero=None, box=None):
    ims = [Image.open(p).convert('RGB') for p in parts]
    ims = [im.resize((W, round(im.height*W/im.width))) if im.width != W else im for im in ims]
    T = Image.open(top).convert('RGB')
    if hero and box:
        x0, y0, x1, y1 = box; T = T.copy()
        ImageDraw.Draw(T).rectangle((x0, y0, x1, y1), fill='white')
        h = Image.open(hero).convert('RGB'); h.thumbnail((x1-x0-40, y1-y0-30))
        T.paste(h, (x0+(x1-x0-h.width)//2, y0+(y1-y0-h.height)//2))
    Bt = Image.open(bot).convert('RGB')
    seq = [ims[0], T]+ims[1:]+[Bt]
    H = sum(i.height for i in seq); F = Image.new('RGB', (W, H), 'white'); y = 0
    for i in seq: F.paste(i, (0, y)); y += i.height
    F.save(out, quality=90); return F

def split(F, prefix, maxh=2000):
    H = F.height; n = (H+maxh-1)//maxh; outs = []
    for i in range(n):
        c = F.crop((0, i*maxh, F.width, min(H, (i+1)*maxh)))
        fn = f'{prefix}_{i+1:02d}.jpg'; c.save(fn, quality=90); outs.append(fn)
    return outs

def run(P):
    code = P['code']; od = f'{OUT}/{code}'; os.makedirs(od, exist_ok=True)
    h = build(P); res = {}
    for v, W in [('CP', 780), ('ND', 860)]:
        open(f'{od}/{v}.html', 'w').write(h)
        parts = render(h, W, f'{od}/{v}')
        if v == 'CP':
            os.makedirs(f'{od}/쿠팡_780px', exist_ok=True)
            F = assemble(parts, f'{D}/blocks/CP_top_noshoes.png', f'{D}/blocks/CP_bot.png', 780, f'{od}/쿠팡_780px/{code}_CP_FULL.jpg')
            res['CP'] = split(F, f'{od}/쿠팡_780px/{code}_CP')
        else:
            os.makedirs(f'{od}/네이버_새디자인', exist_ok=True); os.makedirs(f'{od}/호주직배송관_860px', exist_ok=True)
            F = assemble(parts, f'{D}/blocks/ND_top.png', f'{D}/blocks/ND_bot.png', 860, f'{od}/네이버_새디자인/{code}_ND_FULL.jpg', hero=P['hero'], box=(70, 620, 790, 1155))
            res['ND'] = split(F, f'{od}/네이버_새디자인/{code}_ND')
            F2 = assemble(parts, f'{D}/blocks/HJ_top.png', f'{D}/blocks/HJ_bot.png', 860, f'{od}/호주직배송관_860px/{code}_HJ_FULL.jpg', hero=P['hero'], box=(15, 445, 845, 1053))
            res['HJ'] = split(F2, f'{od}/호주직배송관_860px/{code}_HJ')
    return res
