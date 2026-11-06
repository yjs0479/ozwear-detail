import sys,os,json; HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import gen_ozw as G
import numpy as np
from PIL import Image
G.OUT=os.path.join(HERE,'out')
R=os.path.dirname(os.path.dirname(HERE))+'/'
MM={35:'225',36:'230',37:'235',38:'240',39:'245',40:'250~255',41:'260~265',42:'270~275',43:'280~285',44:'290~295'}
OPT={35:'225mm(EU35)',36:'230mm(EU36)',37:'235mm(EU37)',38:'240mm(EU38)',39:'245mm(EU39)',40:'250-255mm(EU40)',41:'260-265mm(EU41)',42:'270-275mm(EU42)',43:'280-285mm(EU43)',44:'290-295mm(EU44)'}
def TR(p,tag):
    im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int); m=a.min(axis=2)<235; ys,xs=np.where(m)
    if len(ys): im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    w,h=im.size; e=int(max(w,h)*0.05); c=Image.new('RGB',(w+2*e,h+2*e),'white'); c.paste(im,(e,e))
    os.makedirs(os.path.join(HERE,'out'),exist_ok=True); o=os.path.join(HERE,'out',f'as_{tag}.jpg'); c.save(o,quality=92); return o
CSSX='''
.p{font-size:21px}
.card .t{font-size:22px}.card .d{font-size:18px}
.g .t{font-size:22px}.g .d{font-size:18px}
table.info{font-size:20px}
table.info td{padding:20px 18px !important}
.cc .k{font-size:22px}
.chk{display:flex;gap:16px;align-items:center;font-size:21px;padding:18px 4px;border-bottom:1px dashed #e3d6c3;text-align:left;color:#3b2a1e}
.chk i{flex:none;width:30px;height:30px;border-radius:50%;background:#4a3326;color:#fff;font-style:normal;font-size:16px;display:flex;align-items:center;justify-content:center}
.chk b{color:#a5502b}
.szh{font-family:'Noto Serif CJK KR',serif;font-size:32px;margin:50px 0 26px;color:#3b2a1e}
table.vt{width:100%;border-collapse:collapse}
table.vt th{background:#4a3326;color:#fff;font-size:21px;font-weight:700;padding:22px 6px}
table.vt td{text-align:center;padding:20px 6px;border-bottom:1px solid #eee5d9;font-size:28px;font-weight:900;color:#3b2a1e}
table.vt td.r{color:#a5502b;font-size:24px}
.pin{margin-top:28px;background:#fff8e6;border:1px solid #f0e2c4;border-radius:14px;padding:22px 26px;font-size:19px;line-height:1.7;text-align:left;color:#3b2a1e}
'''
if CSSX not in G.CSS: G.CSS+=CSSX
def size_html(eus,h,chk,pin):
    rows=''.join(f'<tr><td>{MM[e]}</td><td>EU {e}</td><td class="r">{OPT[e]}</td></tr>' for e in eus)
    return ('<div class="sec white"><div class="eb">SIZE GUIDE</div><h2>사이즈 안내</h2>'+''.join(f'<div class="chk"><i>✓</i><span>{c}</span></div>' for c in chk)+
      f'<h3 class="szh">{h}</h3><table class="vt"><tr><th>평소 사이즈(mm)</th><th>제품 라벨</th><th>옵션 선택</th></tr>{rows}</table><div class="pin">{"<br>".join(pin)}</div></div>')
def run(P):
    h=G.build(P)
    h=h.replace('OZWEAR® UGG · '+P['code'],'AUSTRALIAN SHEPHERD® UGG · 에버어그').replace('호주 브랜드 <b>OZWEAR®</b>가','호주 브랜드 <b>AUSTRALIAN SHEPHERD®</b>가')
    k='<div class="sec white"><div class="eb">SIZE GUIDE</div>'; i=h.index(k)
    h=h[:i]+size_html(*P['sz'])+'</body></html>'
    od=G.OUT+'/'+P['code']; os.makedirs(od,exist_ok=True); open(od+'/CP.html','w').write(h)
    parts=G.render(h,780,od+'/CP')
    F=G.assemble(parts,os.path.join(HERE,'blocks','CP_top_noshoes.png'),os.path.join(HERE,'blocks','CP_bot_big.png'),780,od+'/FULL0.jpg')
    H=F.height; bh=1617; c=F.getpixel((5,H-bh+5))
    F2=Image.new('RGB',(780,H+60),c); F2.paste(F.crop((0,0,780,H-bh)),(0,0)); F2.paste(F.crop((0,H-bh,780,H)),(0,H-bh+60))
    F2.save(od+'/FULL.jpg',quality=92); return F2
SHEEP3=[('따뜻함','양털 사이<br>공기층이<br>체온을 지켜줘요'),('보송함','습기를 흡수하고<br>통기성이 좋아요'),('가벼움','덧댄 안감 없이<br>한 장으로 가볍게')]

# ---- 11/07 09:30: bigger text (Lori size) — render at CSS width 600, scale 1.3 -> 780px ----
from playwright.sync_api import sync_playwright
CW=590
BOT_HTML='''<div class="sec beige"><div class="eb">SHIPPING</div><h2>배송 안내</h2>
<div class="g" style="text-align:center;margin-top:24px"><div class="t" style="font-size:30px">약 1~2주</div><div class="d">호주에서 한국으로 해외 배송되는 상품으로,<br>결제 후 받아보시기까지 약 1~2주가 소요됩니다.<br>현지 물류 및 통관 상황에 따라 일부 지연될 수 있습니다.</div></div>
<div class="grid2" style="grid-template-columns:1fr 1fr;text-align:center">
<div class="g"><div class="e2">STEP 1</div><div class="t">결제 완료</div><div class="d">주문 확인</div></div>
<div class="g"><div class="e2">STEP 2</div><div class="t">상품 준비</div><div class="d">호주 현지 구매 · 발송</div></div>
<div class="g"><div class="e2">STEP 3</div><div class="t">통관</div><div class="d">한국 세관 통관 진행</div></div>
<div class="g"><div class="e2">STEP 4</div><div class="t">배송</div><div class="d">국내 택배 배송 완료</div></div></div>
<div class="g" style="margin-top:16px;text-align:left"><div class="t">개인통관고유부호를 꼭 확인해주세요</div><div class="d">주문자(수령인) 성함, 휴대폰 번호와<br>개인통관고유부호가 일치해야 통관이 진행됩니다.<br>정보가 다를 경우 통관이 지연될 수 있습니다.</div></div></div>
<div class="sec white"><div class="eb">CARE</div><h2>오래 쓰는 관리 방법</h2>
<div class="grid2">
<div class="g" style="background:#f8f1e7"><div class="t">물기는 바로 닦기</div><div class="d">젖었을 땐 마른 수건으로<br>가볍게 두드려 닦아요.</div></div>
<div class="g" style="background:#f8f1e7"><div class="t">그늘에서 건조</div><div class="d">통풍이 잘 되는 그늘에서<br>자연 건조해주세요.</div></div>
<div class="g" style="background:#f8f1e7"><div class="t">열은 멀리</div><div class="d">드라이기·히터·직사광선은<br>변형의 원인이 돼요.</div></div>
<div class="g" style="background:#f8f1e7"><div class="t">결 따라 브러싱</div><div class="d">스웨이드 전용 브러시로<br>한 방향으로 쓸어요.</div></div></div>
<div class="buy"><div class="t">구매 전 확인해주세요</div><ul>
<li>판매자 상호: 호주언니 (Hoju Sister) · A/S 문의 +61 405 600 382</li>
<li>해외구매대행 상품으로, 주문 시 개인통관고유부호가 필요합니다.</li>
<li>방수 제품이 아니므로 비나 눈이 많은 날에는 착용을 피해주세요.</li>
<li>천연 양털 특성상 초기에 털 빠짐이 있을 수 있어요.</li>
<li>천연 가죽 특성상 제품마다 색감과 결에 약간의 차이가 있을 수 있어요.</li></ul></div></div>'''
BIGCSS='''body{width:590px !important}
table.info td.k{width:36% !important;white-space:nowrap}
.e2{font-size:13px;letter-spacing:3px;font-weight:700;color:#b8925f;margin-bottom:6px}
.buy{border-top:2px solid #3b2a1e;margin-top:34px;padding-top:24px;text-align:left}
.buy .t{font-size:21px;font-weight:800;margin-bottom:10px}
.buy li{font-size:16px;line-height:1.7;color:#5a4636;margin-left:20px}
'''
def render_big(htmlstr,path):
    parts=htmlstr.split('<!--TOPBLOCK-->'); outs=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for i,part in enumerate(parts):
            if i==1: part='<html><head><meta charset="utf-8"><style>'+G.CSS+'</style></head><body>'+part
            if i==0 and len(parts)>1: part=part+'</body></html>'
            part=part.replace('</style>',BIGCSS+'</style>',1)
            pg=b.new_page(viewport={'width':CW,'height':50},device_scale_factor=780/CW)
            hf=f'{path}_big{i}.html'; open(hf,'w').write(part)
            pg.goto('file://'+hf); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(300)
            fn=f'{path}_big{i}.png'; pg.screenshot(path=fn,full_page=True); outs.append(fn)
        b.close()
    return outs
def bot_big(path):
    h='<html><head><meta charset="utf-8"><style>'+G.CSS+BIGCSS+'</style></head><body>'+BOT_HTML+'</body></html>'
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':CW,'height':50},device_scale_factor=780/CW)
        open(path+'.html','w').write(h); pg.goto('file://'+path+'.html'); pg.wait_for_timeout(300)
        pg.screenshot(path=path+'.png',full_page=True); b.close()
    return path+'.png'
def run_big(P, html_path=None):
    if html_path: h=open(html_path).read()
    else:
        h=G.build(P)
        h=h.replace('OZWEAR® UGG · '+P['code'],'AUSTRALIAN SHEPHERD® UGG · 에버어그').replace('호주 브랜드 <b>OZWEAR®</b>가','호주 브랜드 <b>AUSTRALIAN SHEPHERD®</b>가')
        k='<div class="sec white"><div class="eb">SIZE GUIDE</div>'; i=h.index(k); h=h[:i]+size_html(*P['sz'])+'</body></html>'
    od=G.OUT+'/'+P['code']; os.makedirs(od,exist_ok=True)
    parts=render_big(h,od+'/CP')
    os.makedirs(os.path.join(HERE,'out'),exist_ok=True); bot=bot_big(os.path.join(HERE,'out','bot_big'))
    F=G.assemble(parts,os.path.join(HERE,'blocks','CP_top_noshoes.png'),bot,780,od+'/FULLBIG.jpg')
    return F
