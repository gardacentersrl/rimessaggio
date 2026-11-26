# Genera prova.html (versione di prova senza cloud) a partire da gestionale.html.
# Va rilanciato dopo ogni modifica a gestionale.html:  python3 build_prova.py
import re
s=open('gestionale.html',encoding='utf-8').read()
i=s.index("<script>(function(){\n'use strict';\nvar U=")
s=s[:i]
s=s.replace('<script type="text/plain" id="appjs">','<script id="appjs">',1)  # sara' eseguito dopo il prologo
# l'app va eseguita DOPO il prologo: la spostiamo in un tag testuale e la avviamo da script
m=re.search(r'<script id="appjs">(.*)$',s,re.S)
app=m.group(1)
s=s[:m.start()]
PRO=r'''<script>
(function(){
 // 1) Memoria separata: tutto cio' che l'app salva finisce in chiavi "prova:..." e non tocca i dati veri
 var P='prova:',S=Storage.prototype,g=S.getItem,st=S.setItem,rm=S.removeItem;
 S.getItem=function(k){return g.call(this,P+k)};S.setItem=function(k,v){return st.call(this,P+k,v)};S.removeItem=function(k){return rm.call(this,P+k)};
 // 2) Ruolo da provare: prova.html?ruolo=operaio | trasportatore (altrimenti titolare)
 var q=new URLSearchParams(location.search).get('ruolo');window.ROLE=['operaio','trasportatore'].indexOf(q)>=0?q:'master';
 // 3) Nessun collegamento online: email e file sono solo simulati
 window.__rim={up:async function(p){return 'https://prova.invalid/'+p},del:async function(){},dbr:async function(){return[]},fn:async function(n,b){return{results:((b&&b.messages)||[]).map(function(){return{ok:true}})}}};

 // 5) Dati finti di partenza (solo se non c'e' ancora nulla)
 if(g.call(localStorage,P+'rim2')===null){
  var pos=['13C F3 POS5','13C F4 POS3','13C F3 POS1','13S F1 POS1','13C F1 POS2','C12 PORTONE A2','C12 AGRI A1','SALVA A1','SALVA B2','GELIO PORTA LARGA A1','13S F11 POS4','CHIOCCIOLA D3'];
  var nm=['Mario Rossi','Giulia Bianchi','Hans Müller','Jan de Vries','Luca Verdi','Anna Schmidt','Piet Jansen','Paola Neri','Franco Conti','Eva Bauer','Marco Gallo','Sofie Visser'];
  var ml=['mario.rossi','giulia.bianchi','hans.mueller','jan.devries','luca.verdi','anna.schmidt','piet.jansen','paola.neri','franco.conti','eva.bauer','marco.gallo','sofie.visser'];
  var na=['I','I','D','NL','I','D','NL','I','I','D','I','NL'],ti=['ROULOTTE','CAMPER','ROULOTTE','ROULOTTE','MOTOSCAFO','CAMPER','ROULOTTE','CARRELLO','ROULOTTE','CAMPER','MOTOSCAFO','ROULOTTE'];
  function ad(n){var x=new Date();x.setDate(x.getDate()+n);return x.getFullYear()+'-'+String(x.getMonth()+1).padStart(2,'0')+'-'+String(x.getDate()).padStart(2,'0')}
  var cl=pos.map(function(p,i){return{id:i+1,nome:nm[i],targa:'PR'+(100+i*7)+'XY',marca:['Hobby','Knaus','Dethleffs','Adria'][i%4],naz:na[i],mail:ml[i]+'@example.com',cod:String(111111*((i%9)+1)),sede:/SALVA|GELIO/.test(p)?'Camporengo':'Casalemenini',tipo:ti[i],lung:5+((i*7)%30)/10,acconto:i%3===0?200:0,pagato:i%2?300:0,lav:i%4===1?1:0,rit:0,ui:ad(-180+i*9),uo:'',pos:p}});
  var mv=[{d:ad(1),t:'uo',cid:3,pos:pos[2]},{d:ad(2),t:'uo',cid:1,pos:pos[0]},{d:ad(2),t:'uo',cid:2,pos:pos[1],lav:true},{d:ad(4),t:'uo',cid:5,pos:pos[4]},{d:ad(-6),t:'uo',cid:7,pos:pos[6],note:'uscita passata'}];
  st.call(localStorage,P+'rim2',JSON.stringify({cl:cl,mov:mv}));
 }
 // 4) Barra "PROVA" e pulsante per ricominciare
 document.title='PROVA - Rimessaggio';
 var d=document.createElement('div');d.id='provabar';
 d.style.cssText='position:sticky;top:0;z-index:9999;background:#b3261e;color:#fff;font:13px/1.35 system-ui,sans-serif;padding:6px 10px;text-align:center';
 var ro=window.ROLE==='master'?'titolare':window.ROLE;
 function L(r,n){return window.ROLE===(r==='titolare'?'master':r)?'<b style="text-decoration:underline">'+n+'</b>':'<a href="prova.html'+(r==='titolare'?'':'?ruolo='+r)+'" style="color:#fff">'+n+'</a>'}
 d.innerHTML='<b>MODALITÀ PROVA</b> · i dati sono finti e restano solo su questo dispositivo. Stai provando come: '+L('titolare','titolare')+' · '+L('operaio','operaio')+' · '+L('trasportatore','trasportatore')+' · <a href="#" id="provareset" style="color:#fff;font-weight:700">Azzera e ricomincia</a>';
 document.addEventListener('DOMContentLoaded',function(){document.body.insertBefore(d,document.body.firstChild);
  document.getElementById('provareset').onclick=function(e){e.preventDefault();if(!confirm('Cancello tutto quello che hai provato e riparto dai dati finti iniziali. Confermi?'))return;
   var raw=[];for(var j=0;j<window.localStorage.length;j++)raw.push(window.localStorage.key(j));raw.forEach(function(k){if(k.indexOf(P)===0)rm.call(localStorage,k)});location.reload()}});
})();
</script>
'''
START="<script>\nvar s=document.createElement('script');s.textContent=document.getElementById('appjs').textContent;document.body.appendChild(s);\n</script>\n"
s=s.replace('<title>','<meta name="robots" content="noindex"><title>',1)
out=s+PRO+'<script type="text/plain" id="appjs">'+app.replace('</body></html>','').replace('</script>','',1)+'</script>\n'+START+'</body></html>\n'
open('prova.html','w',encoding='utf-8').write(out)
print(len(out))
