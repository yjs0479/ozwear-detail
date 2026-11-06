// 쿠팡 CDN 탭(image1.coupangcdn.com)에서 실행. 상세 이미지 글씨 줄 높이(가로 390 축소 기준) 측정.
// 판정(11/07 보정): 리스팅 전체 줄 높이 중앙값 med >= 11 = 로리 수준 OK / 10 = 조금 작음 / <= 9 = 작아서 안 읽힘 / 줄 15개 미만 = 글씨 거의 없음.
// 기준값: 로리 16430898234 med 12, 줄리아 med 13, 새 코린 v7 med 13, 옛 코린 v6 med 9, 좁은 틀 med 5~7.
function tx(p){return new Promise(ok=>{const im=new Image();im.onload=()=>{try{const W=390,H=Math.round(im.naturalHeight*W/im.naturalWidth);const c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d',{willReadFrequently:true});x.drawImage(im,0,0,W,H);const d=x.getImageData(0,0,W,H).data;
const row=new Uint8Array(H);for(let y=0;y<H;y++){let dark=0,light=0;for(let i=0;i<W;i++){const q=(y*W+i)*4;const v=(d[q]+d[q+1]+d[q+2])/3;if(v>215)light++;else if(v<150)dark++;}
 const lf=light/W,df=dark/W; row[y]=(lf>0.55&&df>0.004&&df<0.35)?1:((lf>0.9&&df<=0.004)?0:2);}
const bands=[];let s=-1;for(let y=0;y<H;y++){if(row[y]===1){if(s<0)s=y;}else{if(s>=0){const h=y-s;if(row[y]===0&&(s===0||row[s-1]===0))bands.push(h);s=-1;}}}
ok(bands);}catch(e){ok('E')}};im.onerror=()=>ok('ERR');im.src='https://image1.coupangcdn.com/image/'+p;});}
function stat(paths,TXT){let all=[];for(const p of paths){const b=TXT[p];if(Array.isArray(b))all=all.concat(b);}all=all.filter(h=>h>=4&&h<=30).sort((a,b)=>a-b);if(!all.length)return{n:0};return{n:all.length,p25:all[Math.floor(all.length*0.25)],med:all[Math.floor(all.length/2)]};}
