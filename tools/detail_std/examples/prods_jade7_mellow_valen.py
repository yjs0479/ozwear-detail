import sys; sys.path.insert(0,'/home/claude/audit/tpl')
from build import *
J=R+'r1102j/AS3068_'; B=R+'r1102jc/AS3068BC_'; V=R+'r1102e/AS2056_'; PP='/home/claude/corin/pp/'
E35_44=list(range(35,45))
CHK_TS=['발길이를 재서 가장 가까운 사이즈를 골라 주세요.','천연 양털 안감이라 처음엔 꼭 맞고, 신을수록 발에 맞게 자리 잡아요.']
INFO0=[('브랜드','AUSTRALIAN SHEPHERD® UGG<br>(에버어그)'),('브랜드 · 디자인','호주'),('제조국','중국 (OEM 생산)')]
def info(model,rows): return [INFO0[0],('모델',model)]+INFO0[1:]+rows
PRODS={}
PRODS['JADE7']=dict(sid=16436790445,code='JADE7',en='JADE',title=['클래식 울트라 미니','양면 양털 털부츠','더블페이스 쉽스킨 2.3cm'],
 mat=['양면 양털(더블페이스 쉽스킨) 갑피 · 안감','EVA 밑창 2.3cm'],chips=['여성 EU 35 – 44','7가지 컬러'],
 tag_eb='TWIN-FACE SHEEPSKIN · ULTRA MINI',tag_h=['겉도 속도 한 장의 양털,','가볍게 신는 울트라 미니'],tag_p=['겉가죽과 안쪽 양털이 한 장으로 된 양면 양털(쉽스킨).','발목 아래 짧은 기장이라 어떤 옷에도 잘 어울려요.'],
 hero=J+'p01.jpg',
 materials=[dict(pill='MATERIAL 01 · TWIN-FACE SHEEPSKIN',h='양면 양털 (더블페이스 쉽스킨)',p=['겉은 부드러운 스웨이드 결, 속은 <b>천연 양털</b>.','한 장의 양털이라 가볍고 따뜻해요.'],cards=SHEEP3,photos=[J+'d02.jpg',J+'p05.jpg']),
  dict(pill='MATERIAL 02 · LOGO',h='뒤꿈치 UGG 로고 라벨',p=['뒤꿈치의 <b>UGG Australian Shepherd</b> 라벨이','정품을 보여줘요.'],photos=[J+'p04.jpg']),
  dict(pill='MATERIAL 03 · EVA SOLE',h='가벼운 EVA 밑창 2.3cm',p=['<b>2.3cm EVA 밑창</b>이라','가볍고 쿠션감 있게 편안해요.'],photos=[TR(J+'d01.jpg','j_d01')])],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉과 속이 하나인 <b>양면 양털(더블페이스 쉽스킨)</b>.','덧댄 안감이 아니라 양털 그대로라 더 따뜻하고 보송해요.'],
 points=[('양면 양털','겉과 속이 한 장의 쉽스킨.'),('울트라 미니 기장','발목 아래 짧은 데일리 부츠.'),('EVA 2.3cm','가볍고 편안한 밑창.'),('7가지 컬러','체스트넛 · 블랙 · 샌드 · 크림<br>라벤더핑크 · 토프 · 카키.')],
 colors=[('체스트넛','CHESTNUT',J+'o_CHESTNUT.jpg'),('블랙','BLACK',J+'o_BLACK.jpg'),('샌드(어도비그레이)','ADOBE GREY',J+'o_ADOBEGREY.jpg'),('크림(카놀라)','CANOLA',J+'o_CANOLA.jpg'),('라벤더핑크','DAWN PINK',J+'o_DAWNPINK.jpg'),('토프(피칸)','PECAN',J+'o_PECAN.jpg'),('카키(카리부)','CARIBOU',J+'o_CARIBOU.jpg')],
 details=[[J+'rep3.jpg'],[J+'p02.jpg',J+'p03.jpg'],[TR(J+'d03.jpg','j_d03'),TR(J+'d06.jpg','j_d06')],[TR(J+'rep2.jpg','j_rep2')]],
 info=info('Jade (제이드)',[('갑피 · 안감','양면 양털 (더블페이스 쉽스킨)'),('밑창','EVA (약 2.3cm)'),('색상','체스트넛 / 블랙 / 샌드(어도비그레이) / 크림(카놀라) /<br>라벤더핑크 / 토프(피칸) / 카키(카리부)'),('사이즈','여성 EU 35 ~ 44<br>색상별 사이즈는 옵션에서 확인')]),
 size=dict(opts=['x'],note=['x']),
 sz=(E35_44,'여성 사이즈 가이드',CHK_TS,['📌 <b>EU 42 ~ 44</b>는 <b>체스트넛 · 블랙</b>만 있어요.','색상별로 있는 사이즈가 달라요. 옵션에서 꼭 확인해 주세요.']))
PRODS['MELLOW']=dict(sid=16436793853,code='MELLOW',en='MELLOW MINI',title=['멜로우 미니','트윈페이스 통양털 울트라 미니','블랙 · 체스트넛'],
 mat=['양면 양털(트윈페이스 쉽스킨) 갑피 · 안감','EVA 밑창 2.3cm'],chips=['EU 35 – 44','2가지 컬러'],
 tag_eb='TWIN-FACE SHEEPSKIN · ULTRA MINI',tag_h=['겉도 속도 한 장의 양털,','가볍게 신는 울트라 미니'],tag_p=['겉가죽과 안쪽 양털이 한 장으로 된 통양털(트윈페이스 쉽스킨).','가장 많이 찾는 블랙 · 체스트넛 두 가지 컬러예요.'],
 hero=B+'cover3.jpg',
 materials=[dict(pill='MATERIAL 01 · TWIN-FACE SHEEPSKIN',h='양면 양털 (트윈페이스 쉽스킨)',p=['겉은 부드러운 스웨이드 결, 속은 <b>천연 양털</b>.','한 장의 양털이라 가볍고 따뜻해요.'],cards=SHEEP3,photos=[TR(B+'d01.jpg','b_d01'),TR(B+'d02.jpg','b_d02')]),
  dict(pill='MATERIAL 02 · LOGO',h='뒤꿈치 UGG 로고 라벨',p=['뒤꿈치의 <b>UGG Australian Shepherd</b> 라벨이','정품을 보여줘요.'],photos=[TR(B+'d05.jpg','b_d05')]),
  dict(pill='MATERIAL 03 · EVA SOLE',h='가벼운 EVA 밑창 2.3cm',p=['<b>2.3cm EVA 밑창</b>이라','가볍고 쿠션감 있게 편안해요.'],photos=[TR(B+'d03.jpg','b_d03')])],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉과 속이 하나인 <b>양면 양털(트윈페이스 쉽스킨)</b>.','덧댄 안감이 아니라 양털 그대로라 더 따뜻하고 보송해요.'],
 points=[('통양털','겉과 속이 한 장의 쉽스킨.'),('울트라 미니 기장','발목 아래 짧은 데일리 부츠.'),('EVA 2.3cm','가볍고 편안한 밑창.'),('2가지 컬러','블랙 · 체스트넛.')],
 colors=[('체스트넛','CHESTNUT',B+'o_CHESTNUT.jpg'),('블랙','BLACK',B+'o_BLACK.jpg')],
 details=[[PP+'s01.jpg'],[PP+'s11.jpg'],[PP+'s07.jpg',PP+'s15.jpg'],[TR(B+'d04.jpg','b_d04'),TR(B+'d06.jpg','b_d06')],[PP+'s04.jpg',PP+'s13.jpg']],
 info=info('Mellow Mini (멜로우 미니)',[('갑피 · 안감','양면 양털 (트윈페이스 쉽스킨)'),('밑창','EVA (약 2.3cm)'),('색상','블랙 / 체스트넛'),('사이즈','EU 35 ~ 44')]),
 size=dict(opts=['x'],note=['x']),
 sz=(E35_44,'사이즈 가이드',CHK_TS,['📌 제품 라벨에는 <b>EU 사이즈</b>로 표기되어 있어요.','블랙 · 체스트넛 모두 EU 35 ~ 44까지 있어요.']))
PRODS['VALEN']=dict(sid=16436781739,code='VALEN',en='VALEN',title=['자수 브레이드 슬립온','양털 어그슬리퍼','스웨이드 천연양털'],
 mat=['소가죽 스웨이드 · 천연 양털 안감 · 인솔','자수 브레이드 칼라 · EVA 고무 밑창'],chips=['EU 35 – 44','5가지 컬러','남녀공용'],
 tag_eb='SUEDE · BRAID · SLIP-ON',tag_h=['쏙 신는 양털 슬립온,','입구엔 포인트 자수 브레이드'],tag_p=['부드러운 스웨이드에 자수 브레이드 칼라.','실내외 모두 편하게 신는 데일리 슬리퍼예요.'],
 hero=TR(V+'rep1.jpg','v_rep1'),
 materials=[dict(pill='MATERIAL 01 · SHEEPSKIN',h='천연 양털 안감 & 인솔',p=['안감과 인솔 모두 <b>천연 양털</b>이라','맨발로 신어도 보송하고 따뜻해요.'],cards=[('따뜻함','양털 사이<br>공기층이<br>체온을 지켜줘요'),('보송함','습기를 흡수하고<br>통기성이 좋아요'),('폭신함','양털 인솔이<br>쿠션이 되어줘요')],photos=[V+'p03.jpg']),
  dict(pill='MATERIAL 02 · BRAID',h='자수 브레이드 칼라',p=['입구를 두른 <b>자수 브레이드</b>가','심플한 슬리퍼에 포인트가 돼요.'],photos=[TR(V+'d02.jpg','v_d02')]),
  dict(pill='MATERIAL 03 · SOLE',h='EVA + 고무 밑창',p=['가벼운 <b>EVA 고무 밑창</b>이라','실내외 모두 편하게 신어요.','※ 밑창 무늬는 구형 · 신형이 섞여 출고될 수 있어요.'],photos=[TR(V+'d05.jpg','v_d05')])],
 dark_h='좋은 어그는<br><em>소재</em>가 다릅니다',dark_p=['겉은 <b>소가죽 스웨이드</b>, 속은 <b>천연 양털</b>.','몸에 닿는 곳에 진짜 소재를 사용했습니다.'],
 points=[('자수 브레이드','입구 포인트 디자인.'),('천연 양털','안감 · 인솔 모두 양털.'),('남녀공용','EU 35 ~ 44.'),('5가지 컬러','체스트넛 · 블랙 · 초콜릿<br>브라운 · 샌드.')],
 colors=[('체스트넛','CHESTNUT',V+'o_CHESTNUT.jpg'),('블랙','BLACK',V+'o_BLACK.jpg'),('초콜릿','CHOCOLATE',V+'o_CHOCOLATE.jpg'),('브라운','BROWN',V+'o_BROWN.jpg'),('샌드','SAND',V+'o_SAND.jpg')],
 details=[[V+'p01.jpg'],[V+'p02.jpg'],[TR(V+'d01.jpg','v_d01'),TR(V+'d03.jpg','v_d03')],[TR(V+'d04.jpg','v_d04'),TR(V+'d06.jpg','v_d06')],[V+'p04.jpg']],
 info=info('Valen (발렌)',[('갑피','소가죽 스웨이드'),('안감 · 인솔','천연 양털 (쉽스킨)'),('밑창','EVA + 고무'),('색상','체스트넛 / 블랙 / 초콜릿 / 브라운 / 샌드'),('사이즈','EU 35 ~ 44 · 남녀공용')]),
 size=dict(opts=['x'],note=['x']),
 sz=(E35_44,'남녀공용 사이즈 가이드',CHK_TS,['📌 <b>샌드</b>는 <b>EU 36(230mm)</b>부터 있어요.','제품 라벨에는 EU 사이즈로 표기되어 있어요.']))
if __name__=='__main__':
    for k in sys.argv[1:]:
        F=run(PRODS[k]); print(k,F.size)
