import sys; sys.path.insert(0,'/home/claude/det/gen')
import gen_ozw as G
from PIL import Image
P0='/home/claude/corin/pp/'; A='/home/claude/ozwear-detail/corin1107/jade/add/'
G.OUT='/home/claude/corin/tpl/out'
def pp(n): return P0+n+'.jpg'
import numpy as np
def TR(p):
    im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int); m=a.min(axis=2)<235; ys,xs=np.where(m)
    im=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w,h=im.size; e=int(max(w,h)*0.05)
    c=Image.new('RGB',(w+2*e,h+2*e),'white'); c.paste(im,(e,e)); o='/home/claude/corin/tpl/heel_trim.jpg'; c.save(o,quality=92); return o
def ad(n): return A+n+'.jpg'
P=dict(code='CORIN',en='CLASSIC ULTRA MINI BOOTS',
 title=['호주 어그 스웨이드 천연양털','클래식 울트라 미니 부츠'],
 mat=['양면 양털(트윈페이스 쉽스킨) 갑피 · 안감','EVA 밑창 2.3cm'],
 chips=['여성 EU 35 – 41','2가지 컬러'],
 tag_eb='TWIN-FACE SHEEPSKIN · ULTRA MINI',tag_h=['겉도 속도 한 장의 양털,','가볍게 신는 울트라 미니'],
 tag_p=['겉가죽과 안쪽 양털이 한 장으로 된 통양털(트윈페이스 쉽스킨).','가장 많이 찾는 체스트넛 · 블랙 두 가지 컬러예요.'],
 hero=ad('h_both1'),
 materials=[
  dict(pill='MATERIAL 01 · TWIN-FACE SHEEPSKIN',h='양면 양털 (트윈페이스 쉽스킨)',p=['겉은 부드러운 스웨이드 결, 속은 <b>천연 양털</b>.','한 장의 양털이라 가볍고 따뜻해요.'],
       cards=[('따뜻함','양털 사이<br>공기층이<br>체온을 지켜줘요'),('보송함','습기를 흡수하고<br>통기성이 좋아요'),('가벼움','덧댄 안감 없이<br>한 장으로 가볍게')],photos=[pp('s06'),pp('s15')]),
  dict(pill='MATERIAL 02 · LOGO',h='뒤꿈치 UGG 로고 라벨',p=['뒤꿈치의 <b>UGG Australian Shepherd</b> 라벨이','정품을 보여줘요.'],photos=[TR(ad('w_bk_heel'))]),
  dict(pill='MATERIAL 03 · EVA SOLE',h='가벼운 EVA 밑창 2.3cm',p=['<b>2.3cm EVA 밑창</b>이라','가볍고 쿠션감 있게 편안해요.'],photos=[pp('s09'),pp('s18')]),
 ],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉과 속이 하나인 <b>양면 양털(트윈페이스 쉽스킨)</b>.','덧댄 안감이 아니라 양털 그대로라 더 따뜻하고 보송해요.'],
 points=[('통양털','겉과 속이 한 장의 쉽스킨.'),('울트라 미니 기장','발목 아래 짧은 데일리 부츠.'),('EVA 2.3cm','가볍고 편안한 밑창.'),('2가지 컬러','체스트넛 · 블랙.')],
 colors=[('체스트넛','CHESTNUT',pp('rep_ch')),('블랙','BLACK',pp('rep_bk'))],
 details=[[pp('s01')],[pp('s10')],[pp('s02'),pp('s14')],[pp('s05'),pp('s17')],[ad('w_ch_pair'),ad('w_bk_pair')],[pp('s04'),pp('s13')]],
 info=[('브랜드','AUSTRALIAN SHEPHERD® UGG<br>(에버어그)'),('모델','클래식 울트라 미니 부츠'),('브랜드 · 디자인','호주'),('제조국','중국 (OEM 생산)'),
       ('갑피 · 안감','양면 양털 (트윈페이스 쉽스킨)'),('밑창','EVA (약 2.3cm)'),('색상','체스트넛 / 블랙'),('사이즈','여성 EU 35 ~ 41')],
 size=dict(opts=['x'],note=['x']))
SIZE='''<div class="sec white"><div class="eb">SIZE GUIDE</div><h2>사이즈 안내</h2>
<div class="chk"><i>✓</i><span>정사이즈로 출시되었습니다.</span></div>
<div class="chk"><i>✓</i><span>발볼이 넓거나 발등이 높으면 <b>한 사이즈 업</b>을 추천드려요.</span></div>
<div class="chk"><i>✓</i><span>착화감은 개인차가 있으니 신중히 선택해 주세요.</span></div>
<h3 class="szh">여성 사이즈 가이드</h3>
<table class="vt"><tr><th>평소 사이즈</th><th>옵션 선택</th></tr>
'''+''.join(f'<tr><td>{mm}</td><td class="r">EU {eu}</td></tr>' for eu,mm in [(35,'225'),(36,'230'),(37,'235'),(38,'240'),(39,'245'),(40,'250~255'),(41,'260~265')])+'''</table>
<div class="pin">📌 제품 라벨에는 <b>EU 사이즈</b>로 표기되어 있어요.<br>에버어그 공식 여성 사이즈표 기준이에요.</div></div>'''
G.CSS+='''
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
table.vt th{background:#4a3326;color:#fff;font-size:22px;font-weight:700;padding:22px 8px}
table.vt td{text-align:center;padding:22px 8px;border-bottom:1px solid #eee5d9;font-size:30px;font-weight:900;color:#3b2a1e}
table.vt td.r{color:#a5502b}
.pin{margin-top:28px;background:#fff8e6;border:1px solid #f0e2c4;border-radius:14px;padding:22px 26px;font-size:19px;line-height:1.7;text-align:left;color:#3b2a1e}
'''
h=G.build(P)
h=h.replace('OZWEAR® UGG · CORIN','AUSTRALIAN SHEPHERD® UGG · 에버어그').replace('호주 브랜드 <b>OZWEAR®</b>가','호주 브랜드 <b>AUSTRALIAN SHEPHERD®</b>가')
k='<div class="sec white"><div class="eb">SIZE GUIDE</div>'
i=h.index(k); h=h[:i]+SIZE+'</body></html>'
import os; od=G.OUT+'/CORIN'; os.makedirs(od,exist_ok=True)
open(od+'/CP.html','w').write(h)
parts=G.render(h,780,od+'/CP')
F=G.assemble(parts,'/home/claude/det/blocks/CP_top_noshoes.png','/home/claude/det/blocks/CP_bot.png',780,od+'/CORIN_CP_FULL.jpg')
print(F.size)
