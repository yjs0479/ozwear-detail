import sys,os
sys.path.insert(0,'/home/claude/ozwear-detail/tools/detail_std')
import build as B
G=B.G
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
from playwright.sync_api import sync_playwright
SC='/tmp/claude-0/-home-claude/914de15b-4ad2-5bd1-86d3-93c841f277ca/scratchpad/p1113/'
G.OUT=SC+'out'
IMG=SC+'img/'; os.makedirs(IMG,exist_ok=True)
U='/mnt/user-data/uploads/Documents/어그 상품 등록 사진/'
U4=U+'OB1104 Stella Charm Platform Mule/'
UK=U+'OB1145K Kid Heritage Sheepskin Clog/'
BLK=os.path.dirname(B.__file__)+'/blocks/'

def prep(src,name,trim=True,pad=0.07,maxw=1300,thr=232):
    o=IMG+name+'.jpg'
    if os.path.exists(o): return o
    im=Image.open(src); im.draft('RGB',(maxw*2,maxw*2)); im=im.convert('RGB')
    if trim:
        a=np.asarray(im).astype(int); m=a.min(axis=2)<thr; ys,xs=np.where(m)
        if len(ys):
            bg=tuple(int(v) for v in np.median(np.array([a[3,3],a[3,-4],a[-4,3],a[-4,-4]]),axis=0))
            c=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w,h=c.size; e=int(max(w,h)*pad)
            W=w+2*e; H=max(h+2*e,int(W*0.62))
            cv=Image.new('RGB',(W,H),bg); cv.paste(c,(e,(H-h)//2)); im=cv
    im.thumbnail((maxw,maxw*3)); im.save(o,quality=90); return o

def two(a,b): return f'<div class="two" style="padding:0 40px 24px">{"".join(f"<img src=\"file://{x}\">" for x in (a,b))}</div>'
def one(a,pad='0 40px 24px'): return f'<div class="ph" style="padding:{pad}"><img src="file://{a}"></div>'
def chk(lines): return ''.join(f'<div class="chk"><i>✓</i><span>{c}</span></div>' for c in lines)
STY_H='<div class="sec white" style="padding:50px 40px 24px"><div class="eb">STYLING</div><h2>{h}</h2><div class="p">{p}</div></div>'

SELLER={'ND':'판매자 상호: 호주슈퍼직구 (운영: Hoju Sister)','HJ':'판매자 상호: 호주직배송관'}
def bot_store(v,W):
    h=B.BOT_HTML.replace('판매자 상호: 호주언니 (Hoju Sister) · A/S 문의 +61 405 600 382',SELLER[v])
    assert '호주언니' not in h
    html='<html><head><meta charset="utf-8"><style>'+G.CSS+B.BIGCSS+'</style></head><body>'+h+'</body></html>'
    path=SC+f'out/bot_{v}'
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':B.CW,'height':50},device_scale_factor=W/B.CW)
        open(path+'.html','w').write(html); pg.goto('file://'+path+'.html'); pg.wait_for_timeout(300)
        pg.screenshot(path=path+'.png',full_page=True); b.close()
    return path+'.png'

def render_w(htmlstr,path,W):
    parts=htmlstr.split('<!--TOPBLOCK-->'); outs=[]
    with sync_playwright() as p:
        b=p.chromium.launch()
        for i,part in enumerate(parts):
            if i==1: part='<html><head><meta charset="utf-8"><style>'+G.CSS+'</style></head><body>'+part
            if i==0 and len(parts)>1: part=part+'</body></html>'
            part=part.replace('</style>',B.BIGCSS+'</style>',1)
            pg=b.new_page(viewport={'width':B.CW,'height':50},device_scale_factor=W/B.CW)
            hf=f'{path}_w{W}_{i}.html'; open(hf,'w').write(part)
            pg.goto('file://'+hf); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(300)
            fn=f'{path}_w{W}_{i}.png'; pg.screenshot(path=fn,full_page=True); outs.append(fn)
        b.close()
    return outs

def finish(P,h,size_html,inject_after_hero):
    hk=f'<div class="ph" style="padding:30px 30px 40px;background:#fff"><img src="file://{P["hero"]}"></div>'
    assert hk in h; h=h.replace(hk,hk+inject_after_hero,1)
    k='<div class="sec white"><div class="eb">SIZE GUIDE</div>'; i=h.index(k); h=h[:i]+size_html+'</body></html>'
    for bad in ('호주언니','스타일</','타즈','타스만','디스케트','코케트'):
        assert bad not in h.split('<!--TOPBLOCK-->')[-1] or bad=='호주언니', bad
    code=P['code']; od=G.OUT+'/'+code; os.makedirs(od,exist_ok=True)
    hp=od+'/src.html'; open(hp,'w').write(h)
    res={}
    # Coupang 780 (호주언니 top + big bottom)
    F=B.run_big(dict(P,code=code),html_path=hp)
    os.makedirs(od+'/쿠팡_780px',exist_ok=True); F.save(od+'/쿠팡_780px/FULL.jpg',quality=90)
    res['CP']=G.split(F,od+f'/쿠팡_780px/{code}_CP',maxh=2000)
    # Naver 호주슈퍼직구 / 호주직배송관 860
    parts=render_w(h,od+'/N',860)
    for v,top,box,folder in (('ND','ND_top.png',(70,620,790,1155),'네이버_호주슈퍼직구_860px'),('HJ','HJ_top.png',(15,445,845,1053),'호주직배송관_860px')):
        os.makedirs(od+'/'+folder,exist_ok=True)
        Fv=G.assemble(parts,BLK+top,bot_store(v,860),860,od+f'/{folder}/FULL.jpg',hero=P['hero'],box=box)
        res[v]=G.split(Fv,od+f'/{folder}/{code}_{v}',maxh=2000)
    for k,v in res.items(): print(code,k,len(v))
    return res

# ---------------- OB1104 STELLA CHARM PLATFORM MULE ----------------
def a4(n,**kw): return prep(U4+n,'ob1104_'+os.path.basename(n).split('.')[0].replace(' ','_'),**kw)
c=lambda n: a4(f'Chestnut/IMG_{n}-final.jpg')
s=lambda n: a4(f'Sand/IMG_{n}-final.jpg')
GPT1=a4('지피티 썸네일/OB1104_mix_01_LOGO_WHITE_20261028.png',trim=False)
GPT2=a4('지피티 썸네일/OB1104_mix_02_LOGO_WHITE_20261028(대문).png',trim=False)
P4=dict(code='OB1104',en='STELLA CHARM PLATFORM MULE',
 title=['호주 어그 소가죽 스웨이드','천연양털 퍼 트리밍','스텔라 참 플랫폼 뮬'],
 mat=['소가죽 스웨이드 · 천연 양털 안감 &amp; 인솔','EVA 플랫폼 밑창 · 굽높이 약 4.5cm'],
 chips=['여성 EU 35 – 41','굽 약 4.5cm','2가지 컬러'],
 tag_eb='COW SUEDE · SHEEPSKIN · PLATFORM',tag_h=['풍성한 양털 칼라에','반짝이는 메탈 참 한 줄'],
 tag_p=['부드러운 <b>소가죽 스웨이드</b>에 <b>천연 양털</b>을 두르고','발등에 <b>메탈 참</b>을 더한 4.5cm 플랫폼 뮬이에요.','뒤꿈치가 열려 있어 쓱 신고 벗기 편해요.'],
 hero=GPT2,
 materials=[
  dict(pill='MATERIAL 01 · SHEEPSKIN',h='풍성한 천연 양털 퍼 트리밍',
       p=['칼라, 안감, 인솔까지 <b>천연 양털(쉽스킨)</b>을 썼어요.','발을 감싸는 양털 칼라가 포근하고 보송해요.'],
       cards=[('따뜻함','양털 사이<br>공기층이<br>체온을 지켜줘요'),('보송함','습기를 흡수하고<br>통기성이 좋아요'),('폭신함','양털 인솔이<br>쿠션이 되어<br>발이 편안해요')],
       photos=[c(6284),s(6265)]),
  dict(pill='MATERIAL 02 · COW SUEDE &amp; CHARM',h='소가죽 스웨이드와 메탈 참',
       p=['결이 고운 <b>천연 소가죽 스웨이드</b>에','모카신 스티치와 <b>은색 메탈 참</b>을 더했어요.','데님, 니트, 스커트 어디에나 잘 어울려요.'],
       photos=[c(6279),s(6262)]),
  dict(pill='MATERIAL 03 · EVA PLATFORM',h='가벼운 4.5cm EVA 플랫폼',
       p=['약 <b>4.5cm 플랫폼 밑창</b>이라 키는 높아 보이고','EVA 소재라 생각보다 훨씬 가벼워요.'],
       photos=[c(6283),c(6290)]),
 ],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉은 <b>소가죽 스웨이드</b>, 속은 <b>천연 양털</b>.','발이 닿는 모든 곳에 진짜 소재를 썼어요.'],
 points=[('4.5cm 플랫폼','키는 높이고<br>발은 가볍게.'),('풍성한 양털 칼라','발등까지<br>포근하게.'),('메탈 참 포인트','단정한 뮬에<br>반짝이는 포인트.'),('뒤꿈치 오픈 뮬','쓱 신고<br>벗기 편해요.')],
 colors=[('체스트넛','CHESTNUT',c(6279)),('샌드','SAND',s(6262))],
 details=[[c(6288),s(6269)],[c(6282),s(6263)],[c(6289),s(6267)],[c(6285),s(6266)],[c(6290),s(6268)]],
 info=[('브랜드','OZWEAR® UGG<br>(오즈웨어 어그)'),('모델','스텔라 참 플랫폼 뮬 (OB1104)'),('브랜드 · 디자인','호주'),('제조국','중국 (OEM 생산)'),
       ('갑피','소가죽 스웨이드'),('안감 · 인솔','천연 양털 (쉽스킨)'),('밑창','EVA'),('굽 높이','약 4.5cm'),
       ('색상','체스트넛 / 샌드'),('사이즈','여성 EU 35 ~ 41')],
 size=dict(opts=['x'],note=['x']), logo_where='발등 메탈 참과<br>안쪽 UGG 로고')
H8=a4('화보/8db11df5-1817-4cb4-a19c-a404ef94f3ad.jpg',trim=False)
HC=a4('화보/Chestnut/OB1104 Chestnut .jpg',trim=False)
HS=a4('화보/Sand/ob04 sand.jpg',trim=False)
STY4=(STY_H.format(h='데일리로 포근하게',p='니트, 데님, 스커트 어디에나 툭 신기 좋아요.')+
      one(H8)+two(HC,HS)+one(GPT1,'0 40px 40px'))
CHK=['정사이즈로 출시되었어요.<br>평소 신는 사이즈(mm) 그대로 선택하세요.',
     '양털이 두툼해 처음엔 꼭 맞을 수 있어요.<br>신을수록 양털이 눌려 발에 맞게 편해져요.',
     '사이즈 사이에 있거나 발볼이 넓고 발등이 높다면<br><b>한 사이즈 업</b>을 추천드려요.',
     '착화감은 개인차가 있으니 신중히 선택해 주세요.']
ROWS=[('225','EU 35','225mm(EU35)'),('230','EU 36','230mm(EU36)'),('235','EU 37','235mm(EU37)'),('240','EU 38','240mm(EU38)'),('245','EU 39','245mm(EU39)'),('250 · 255','EU 40','250-255mm(EU40)'),('260 · 265','EU 41','260-265mm(EU41)')]
SIZE4=('<div class="sec white"><div class="eb">SIZE GUIDE</div><h2>사이즈 안내</h2>'+chk(CHK)+
 '<h3 class="szh">여성 사이즈 가이드</h3><table class="vt"><tr><th>평소 사이즈(mm)</th><th>제품 라벨</th><th>옵션 선택</th></tr>'+
 ''.join(f'<tr><td>{a}</td><td>{b}</td><td class="r">{c_}</td></tr>' for a,b,c_ in ROWS)+
 '</table><div class="pin">📌 제품 라벨에는 <b>EU 사이즈</b>로 표기되어 있어요.<br>칸이 묶인 두 사이즈는 <b>같은 제품</b>으로 발송돼요.<br>(250·255mm → EU 40 / 260·265mm → EU 41)</div></div>')

# ---------------- OB1145K KIDS HERITAGE CLOG ----------------
def ak(n,**kw): return prep(UK+n,'ob1145k_'+os.path.basename(n).split('.')[0].replace(' ','_'),**kw)
kc=lambda n: ak(f'원본사진_Toby1105/CHESTNUT/IMG_{n}-final.jpg')
ks=lambda n: ak(f'원본사진_Toby1105/SAND/IMG_{n}-final.jpg')
KH=ak('대문_추가이미지_1105toby/네이버_대문.jpg',trim=False)
KH2=ak('대문_추가이미지_1105toby/쿠팡_대문.jpg',trim=False)
PK=dict(code='OB1145K',en='KIDS HERITAGE SUEDE CLOG',
 title=['호주 어그 소가죽 스웨이드','천연양털 키즈','헤리티지 브레이드 클로그'],
 mat=['소가죽 스웨이드 · 천연 양털 안감 &amp; 인솔','EVA 밑창 · 굽높이 약 2cm'],
 chips=['아동 145 – 210mm','굽 약 2cm','2가지 컬러'],
 tag_eb='KIDS · COW SUEDE · SHEEPSKIN',tag_h=['어른 클로그 그대로,','아이 발에 꼭 맞게'],
 tag_p=['<b>자수 브레이드 칼라</b>와 발등 <b>끈 장식</b>을 그대로 담은','아이용 천연 양털 클로그예요.','가볍고 따뜻해 등원길, 나들이에 좋아요.'],
 hero=KH,
 materials=[
  dict(pill='MATERIAL 01 · SHEEPSKIN',h='발끝까지 천연 양털',
       p=['안감과 인솔에 <b>천연 양털(쉽스킨)</b>을 썼어요.','맨발로 신어도 보송하고 따뜻해요.'],
       cards=[('따뜻함','양털 사이<br>공기층이<br>체온을 지켜줘요'),('보송함','습기를 흡수하고<br>통기성이 좋아요'),('폭신함','양털 인솔이<br>쿠션이 되어<br>발이 편안해요')],
       photos=[kc(8571),ks(8579)]),
  dict(pill='MATERIAL 02 · COW SUEDE &amp; BRAID',h='소가죽 스웨이드와 자수 칼라',
       p=['부드러운 <b>천연 소가죽 스웨이드</b>에','알록달록 <b>자수 브레이드 칼라</b>를 둘렀어요.'],
       photos=[kc(8568),ks(8576)]),
  dict(pill='MATERIAL 03 · EVA SOLE',h='가볍고 폭신한 2cm 밑창',
       p=['약 <b>2cm EVA 밑창</b>이라 가볍고','아이가 오래 신어도 발이 편해요.'],
       photos=[kc(8570),kc(8574)]),
 ],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉은 <b>소가죽 스웨이드</b>, 속은 <b>천연 양털</b>.','아이 발이 닿는 곳에 진짜 소재를 썼어요.'],
 points=[('자수 브레이드 칼라','알록달록<br>포인트 칼라.'),('발등 끈 장식','귀여운<br>레이스 포인트.'),('천연 양털','안감·인솔까지<br>포근하게.'),('가벼운 EVA 밑창','약 2cm,<br>폭신하고 가볍게.')],
 colors=[('체스트넛','CHESTNUT',kc(8568)),('샌드','SAND',ks(8576))],
 details=[[kc(8575),ks(8583)],[kc(8569),ks(8577)],[kc(8573),ks(8581)],[kc(8572),ks(8580)],[kc(8574),ks(8582)]],
 info=[('브랜드','OZWEAR® UGG<br>(오즈웨어 어그)'),('모델','키즈 헤리티지 클로그 (OB1145K)'),('브랜드 · 디자인','호주'),('제조국','중국 (OEM 생산)'),
       ('갑피','소가죽 스웨이드'),('안감 · 인솔','천연 양털 (쉽스킨)'),('밑창','EVA'),('굽 높이','약 2cm'),
       ('색상','체스트넛 / 샌드'),('사이즈','아동 AU 5/6 ~ 2/3<br>(발 길이 145 ~ 210mm)')],
 size=dict(opts=['x'],note=['x']), logo_where='옆면에 새겨진<br>UGG 로고')
STYK=one(KH2,'0 40px 40px')
KCHK=['표의 mm는 <b>아이 발 길이</b> 기준이에요.<br>발 길이를 재서 그 길이가 들어가는 칸을 골라주세요.',
      '양털이 두툼해 처음엔 꼭 맞을 수 있어요.<br>신을수록 양털이 눌려 발에 맞게 편해져요.',
      '사이즈 사이에 있거나 발볼이 넓고 발등이 높다면<br><b>한 사이즈 업</b>을 추천드려요.',
      '아이 발은 빨리 자라니 신중히 선택해 주세요.']
KROWS=[('145','AU 5/6','145mm(AU 5/6)'),('150 · 155 · 160 · 165','AU 7/8','150-165mm(AU 7/8)'),('170 · 175 · 180','AU 9/10','170-180mm(AU 9/10)'),('185 · 190','AU 11/12','185-190mm(AU 11/12)'),('195 · 200','AU 13/1','195-200mm(AU 13/1)'),('205 · 210','AU 2/3','205-210mm(AU 2/3)')]
SIZEK=('<div class="sec white"><div class="eb">SIZE GUIDE</div><h2>아동 사이즈 안내</h2>'+chk(KCHK)+
 '<h3 class="szh">아동 사이즈 가이드</h3><table class="vt"><tr><th style="white-space:nowrap">아이 발 길이(mm)</th><th>옵션 선택</th></tr>'+
 ''.join(f'<tr><td style="white-space:nowrap">{a}</td><td class="r" style="line-height:1.3">{c_.split("(")[0]}<br><span style="font-size:20px;color:#3b2a1e">({c_.split("(")[1]}</span></td></tr>' for a,b,c_ in KROWS)+
 '</table><div class="pin">📌 제품 라벨에는 <b>호주(AU) 아동 사이즈</b>로<br>표기되어 있어요. 오즈웨어 공식 아동 사이즈표 기준이에요.<br>한 칸에 묶인 길이는 <b>같은 제품</b>으로 발송돼요.</div></div>')

if __name__=='__main__':
    which=sys.argv[1:] or ['4','k']
    if '4' in which: finish(P4,G.build(P4),SIZE4,STY4)
    if 'k' in which: finish(PK,G.build(PK),SIZEK,STYK)
