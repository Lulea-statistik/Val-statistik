const GEO={
1970:'data/valdistrikt/1970/lulea_2580_valdistrikt_1970_preliminar_epsg4326.geojson',
1973:'data/valdistrikt/1973/lulea_2580_valdistrikt_1973_preliminar_epsg4326.geojson',
1976:'data/valdistrikt/1976/lulea_2580_valdistrikt_1976_preliminar_epsg4326.geojson',
1979:'data/valdistrikt/1979/lulea_2580_valdistrikt_1979_preliminar_epsg4326.geojson',
1982:'data/valdistrikt/1982/lulea_2580_valdistrikt_1982_preliminar_epsg4326.geojson',
1985:'data/valdistrikt/1985/lulea_2580_valdistrikt_1985_preliminar_epsg4326.geojson',
1988:'data/valdistrikt/1988/lulea_2580_valdistrikt_1988_preliminar_epsg4326.geojson',
1991:'data/valdistrikt/1991/lulea_2580_valdistrikt_1991_preliminar_epsg4326.geojson',
1994:'data/valdistrikt/1994/lulea_2580_valdistrikt_1994_preliminar_epsg4326.geojson',
1998:'data/valdistrikt/1998/lulea_2580_valdistrikt_1998_preliminar_epsg4326.geojson',
2002:'data/lulea_valdistrikt_2002.geojson',
2006:'data/valdistrikt/2006/lulea_2580_valdistrikt_2006_epsg4326.geojson',
2010:'data/valdistrikt/2010/lulea_2580_valdistrikt_2010_epsg4326.geojson',
2014:'data/valdistrikt/2014/lulea_2580_valdistrikt_2014_epsg4326.geojson',
2018:'data/valdistrikt/2018/lulea_2580_valdistrikt_2018_epsg4326.geojson',
2022:'data/valdistrikt/2022/lulea_2580_valdistrikt_2022_epsg4326.geojson'};
const FIELD_INVALID='med ogiltiga valsedlar';
const FIELDS=['OG varav blanka','OG varav ÖVR ogiltiga','OG varav EGEJ, ej anmälda part.'];
const fmt=new Intl.NumberFormat('sv-SE',{maximumFractionDigits:1});
const norm=s=>String(s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'')
 .replace(/[^a-z0-9]/g,'').replace(/(bergnaset|hertson|porson|sunderbyn)s(?=[123]$)/g,'$1');
const props=f=>f.properties||{};
const name=f=>props(f).valdistriktsnamn||props(f).VD_NAMN||props(f).VDNAMN||props(f).NAMN||props(f).Vdnamn||props(f).Valdistriktsnamn||'';
const special=s=>/^(lulea|uppsamlingsdistrikt)$/.test(norm(s));
const validNum=x=>typeof x==='number'&&Number.isFinite(x);
const num=(r,k)=>validNum(r[k])?r[k]:null;
function lookup(rows,year,kind){
 const selected=rows.filter(r=>Number(r['År'])===Number(year)&&r.Val===kind&&!special(r['Område']));
 const index=new Map();
 for(const r of selected){const key=norm(r['Område']);if(!index.has(key))index.set(key,[]);index.get(key).push(r);}
 return {selected,index};
}
function linked(geo,idx){
 const n=norm(name(geo));
 if(n==='sunderbyns1och2'||n==='sunderbyn1och2'){
  // Historical merge: only if both source districts exist, aggregate counts.
  return [...(idx.get('sunderbyn1')||[]),...(idx.get('sunderbyn2')||[]),...(idx.get('sunderbyn')||[])];
 }
 return idx.get(n)||[];
}
function aggregate(matches){
 if(!matches.length)return null;
 const keys=['Röstberättigade','VDT','med giltiga valsedlar',FIELD_INVALID,...FIELDS];
 const r={};
 for(const k of keys){
  const xs=matches.map(x=>num(x,k));
  r[k]=xs.every(x=>x!==null)?xs.reduce((a,b)=>a+b,0):null;
 }
 return r;
}
function vdt(r){
 return r&&num(r,'Röstberättigade')>0&&num(r,'VDT')!==null?
 100*r.VDT/r['Röstberättigade']:null;
}
function invalidRate(r){
 const field=document.getElementById('invalidCategory')?.value||FIELD_INVALID;
 return r&&num(r,field)!==null&&num(r,'VDT')>0?
 100*r[field]/r.VDT:null;
}
const palette=[ '#fff5f0','#fee0d2','#fcbba1','#fc9272','#fb6a4a','#de2d26','#a50f15' ];
function color(value,type){
 if(value===null||!Number.isFinite(value))return '#aeb6c2';
 const stops=type==='turnout'?[50,60,70,75,80,85]:[0.25,0.5,1,1.5,2,3];
 let i=0;while(i<stops.length&&value>=stops[i])i++;return palette[i];
}
const urlParams=new URLSearchParams(location.search);
const requestedMode=document.body.dataset.mode;
const map=L.map('map',{preferCanvas:true}).setView([65.58,22.15],10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
 attribution:'© OpenStreetMap contributors',maxZoom:19}).addTo(map);
const yearEl=document.getElementById('year'),voteEl=document.getElementById('vote'),
 districtEl=document.getElementById('district'),statusEl=document.getElementById('status');
let voteRows=[],layer=null,municipalityBounds=null,busy=0;
fetch('data/lulea_kommungrans_2580.geojson').then(r=>r.json()).then(g=>{
 const boundary=L.geoJSON(g,{style:{color:'#243b53',weight:2,fill:false},interactive:false}).addTo(map);
 municipalityBounds=boundary.getBounds();map.fitBounds(municipalityBounds,{padding:[24,24],maxZoom:11});
}).catch(()=>{});
function desc(r){
 if(!r)return '<p>Ingen entydig matchning i röstdata.</p>';
 if(requestedMode==='turnout'){
  const rate=vdt(r);
  return '<p><strong>Valdeltagande: '+(rate===null?'Saknas':fmt.format(rate)+' %')+'</strong></p>'+
   '<p>VDT (antal röstande): '+(r.VDT===null?'Saknas':fmt.format(r.VDT))+'</p>'+
   '<p>Röstberättigade: '+(r['Röstberättigade']===null?'Saknas':fmt.format(r['Röstberättigade']))+'</p>';
 }
 const total=num(r,FIELD_INVALID);
 return '<p><strong>Med ogiltiga valsedlar: '+(total===null?'Saknas':fmt.format(total))+'</strong></p>'+
 '<p>Andel av VDT: '+(invalidRate(r)===null?'Saknas':fmt.format(invalidRate(r))+' %')+'</p>'+
 FIELDS.map((k,i)=>'<p>'+['OG varav blanka','OG varav ÖVR ogiltiga','OG varav EGEJ, ej anmälda partier'][i]+': '+(num(r,k)===null?'Saknas':fmt.format(r[k]))+'</p>').join('');
}
function updateInfo(info){
 document.getElementById('info').textContent=info;
}
async function render(){
 const request=++busy,year=Number(yearEl.value),kind=voteEl.value;
 statusEl.textContent='Läser valdistrikt och röstdata …';
 try{
  const response=await fetch(GEO[year]);if(!response.ok)throw Error('Geografi saknas');
  const geo=await response.json();
  if(request!==busy)return;
  const {selected,index}=lookup(voteRows,year,kind);
  const stats={mapped:0,missing:0,partial:0};
  const computed=new Map();
  for(const f of geo.features){
    const matches=linked(f,index);
    let aggregateRow=aggregate(matches);
    if(matches.length){stats.mapped++;if(aggregateRow&&Object.values(aggregateRow).some(x=>x===null))stats.partial++;}
    else stats.missing++;
    computed.set(f,aggregateRow);
  }
  const next=L.geoJSON(geo,{
   style:f=>{const r=computed.get(f),val=requestedMode==='turnout'?vdt(r):invalidRate(r);
    return {color:'#7a3240',weight:1,fillColor:color(val,requestedMode),fillOpacity:.78};},
   onEachFeature:(f,l)=>{
    const r=computed.get(f);
    l.bindPopup('<strong>'+name(f).replaceAll('&','&amp;').replaceAll('<','&lt;')+'</strong>'+desc(r),{autoPan:false});
    l.on('click',()=>{districtEl.value=name(f);const b=l.getBounds();map.flyTo(b.getCenter(),Math.min(15,map.getBoundsZoom(b,false,L.point(64,64))),{duration:.5});l.openPopup();});
   }});
  if(layer)map.removeLayer(layer);
  layer=next.addTo(map);
  districtEl.replaceChildren(new Option('Alla valdistrikt',''),...geo.features
   .map(f=>name(f)).sort((a,b)=>a.localeCompare(b,'sv')).map(n=>new Option(n,n)));
  statusEl.textContent=year+' · '+(kind==='RS'?'Riksdag':'Kommunfullmäktige')+(requestedMode==='invalid'?' · '+document.getElementById('invalidCategory').selectedOptions[0].textContent:'')+
   ' · '+stats.mapped+' av '+geo.features.length+' valdistrikt matchade'+(stats.partial?' · '+stats.partial+' med ofullständiga fält':'');
  updateInfo('Grå områden saknar tillräckliga uppgifter. Kommuntotaler och uppsamlingsdistrikt visas inte som polygoner. VDT är antal röstande. Ogiltig andel beräknas mot VDT.');
  if(Number(year)<=1991)updateInfo(document.getElementById('info').textContent+' För 1970–1982 saknar denna tabell röstdata. Kartans äldre geometrier är rekonstruktioner.');
 }catch(e){if(request===busy)statusEl.textContent='Kunde inte visa data: '+e.message;}
}
districtEl.addEventListener('change',()=>{
 if(!layer||!districtEl.value)return;
 layer.eachLayer(l=>{if(name(l.feature)===districtEl.value){const b=l.getBounds();map.flyTo(b.getCenter(),Math.min(15,map.getBoundsZoom(b,false,L.point(64,64))),{duration:.5});l.openPopup();}});
});
document.getElementById('reset').addEventListener('click',()=>{districtEl.value='';if(municipalityBounds)map.fitBounds(municipalityBounds,{padding:[24,24],maxZoom:11});});
yearEl.addEventListener('change',render);voteEl.addEventListener('change',render);
document.getElementById('invalidCategory')?.addEventListener('change',render);
fetch('data/roster/rostdata_v3.json').then(r=>{if(!r.ok)throw Error('Import av röstdata väntar på publicering');return r.json()}).then(j=>{
 voteRows=j.rows;
 const years=[...new Set(voteRows.map(r=>Number(r['År'])))].filter(y=>GEO[y]).sort((a,b)=>a-b);
 yearEl.replaceChildren(...years.map(y=>new Option(String(y),String(y))));
 yearEl.value=years.includes(2022)?'2022':String(years[years.length-1]);
 render();
}).catch(e=>{statusEl.textContent=e.message+' – ladda upp rostdata_v3.csv i GitHub för att aktivera kartan.';});
