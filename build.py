import os
# -*- coding: utf-8 -*-
import json, re, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, "ftem_data.json"), encoding="utf-8"))
try:
    TR = json.load(open(os.path.join(BASE, "translations.json"), encoding="utf-8"))
except FileNotFoundError:
    TR = {}
LANGS = ["de", "fr", "it"]
FILES = {"de": "index.html", "fr": "fr.html", "it": "it.html"}
def tr(s, lang):
    if lang == "de" or s is None:
        return s
    return TR.get(lang, {}).get(s, s)
INTRO = {
 "de": 'Vollständige, strukturierte Übersicht des Ski-Alpin <b>Athlet:innen-Wegs</b> aus dem Swiss-Ski FTEM-Tool: <b>17 Themen</b> über die zehn Entwicklungsstufen <b>F1–M</b>. Links je Zeile eine fixe Beschriftung; lange Texte sind zusammengeklappt und mit «mehr» ausklappbar. Die Tabellen lassen sich seitlich scrollen.',
 "fr": 'Aperçu complet et structuré du <b>parcours de l&#x27;athlète</b> en ski alpin, issu de l&#x27;outil FTEM de Swiss-Ski : <b>17 thèmes</b> à travers les dix niveaux de développement <b>F1–M</b>. À gauche de chaque ligne, un intitulé fixe ; les textes longs sont repliés et dépliables via « plus ». Les tableaux défilent latéralement.',
 "it": 'Panoramica completa e strutturata del <b>percorso dell&#x27;atleta</b> nello sci alpino, dallo strumento FTEM di Swiss-Ski: <b>17 temi</b> lungo i dieci livelli di sviluppo <b>F1–M</b>. A sinistra di ogni riga un&#x27;etichetta fissa; i testi lunghi sono compressi ed espandibili con «altro». Le tabelle scorrono lateralmente.',
}
STAGES = d["stages"]
FULL = {"F1":"Foundation 1","F2":"Foundation 2","F3":"Foundation 3","T1":"Talent 1","T2":"Talent 2","T3":"Talent 3","T4":"Talent 4","E1":"Elite 1","E2":"Elite 2","M":"Mastery"}
AGE = {"F1":"U8","F2":"U8–U10","F3":"U10–U12","T1":"U12–U14","T2":"U14–U16","T3":"U16+","T4":"U18+","E1":"","E2":"","M":""}

POD_SVG = ('<svg viewBox="0 0 24 24" width="19" height="19" aria-hidden="true">'
'<circle cx="12" cy="12" r="11.5" fill="#1DB954"/>'
'<path d="M5.8 9.2c4-1.2 7.8-.8 11 1.1" stroke="#fff" stroke-width="1.7" fill="none" stroke-linecap="round"/>'
'<path d="M6.5 12.3c3.2-.9 6.2-.6 8.9 1.1" stroke="#fff" stroke-width="1.5" fill="none" stroke-linecap="round"/>'
'<path d="M7.2 15.2c2.4-.6 4.6-.4 6.7.9" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round"/>'
'</svg>')

def ph(st): return "foundation" if st[0]=="F" else "talent" if st[0]=="T" else "elite" if st[0]=="E" else "mastery"
def esc(s): return html.escape(s, quote=True)

SC_RE = re.compile(r'^(SC\s?\d+[a-z]?|SC|ST\s?\d*|ST)\s*[:.\)]\s*(.*)$', re.S)

def render_block(block, link_texts):
    b = block.strip()
    if not b: return ""
    if b in link_texts:  # pure link-label token, shown as button instead
        return ""
    lines = [l for l in b.split("\n")]
    nonempty = [l.strip() for l in lines if l.strip()]
    # bullet list
    if any(l.strip().startswith("•") for l in lines):
        intro, items = [], []
        for l in lines:
            ls = l.strip()
            if ls.startswith("•"):
                items.append(ls.lstrip("•").strip())
            elif ls:
                if not items: intro.append(ls)
                else: items.append(ls)
        out = ""
        if intro: out += '<p class="bh">'+esc(intro[0])+'</p>'
        out += '<ul class="bl">'+"".join('<li>'+esc(i)+'</li>' for i in items if i)+'</ul>'
        return out
    # SC/ST list
    sc_hits = [l for l in nonempty if SC_RE.match(l)]
    if len(nonempty) >= 1 and len(sc_hits) >= 1 and len(sc_hits) >= max(1, len(nonempty)-1):
        out = '<ul class="sc">'
        for ls in nonempty:
            m = SC_RE.match(ls)
            if m:
                out += '<li><span class="badge">'+esc(m.group(1).strip())+'</span> '+esc(m.group(2).strip())+'</li>'
            else:
                out += '<li>'+esc(ls)+'</li>'
        out += '</ul>'
        return out
    # heading + body (short first line, no end punctuation, has more lines)
    if len(lines) >= 2 and lines[0].strip() and len(lines[0].strip()) <= 46 and not lines[0].strip().endswith((".",":",",",";")):
        head = lines[0].strip()
        rest = "\n".join(lines[1:]).strip()
        body = esc(rest).replace("\n","<br>")
        return '<p class="bh">'+esc(head)+'</p><p>'+body+'</p>'
    # label: value (single label line)
    m = re.match(r'^([^:\n]{2,46}):\s*(.+)$', b, re.S)
    if m and "\n" not in m.group(1):
        lab = m.group(1).strip(); val = m.group(2).strip()
        if len(val) > 55 or "\n" in val:
            return '<p class="sh">'+esc(lab)+'</p><p>'+esc(val).replace("\n","<br>")+'</p>'
        return '<p><span class="lbl">'+esc(lab)+':</span> '+esc(val).replace("\n","<br>")+'</p>'
    return '<p>'+esc(b).replace("\n","<br>")+'</p>'

def render_cell(seg, lang):
    txt = (tr(seg["v"], lang) or "").strip()
    link_texts = set(tr(l["text"], lang) for l in seg["l"] if l.get("text"))
    inner = ""
    if txt:
        blocks = re.split(r'\n\s*\n', txt)
        parts = [render_block(bl, link_texts) for bl in blocks]
        inner = "".join(p for p in parts if p)
    if not inner and not seg["l"]:
        return '<div class="empty">–</div>'
    if seg["l"]:
        seen=set(); btns=""
        for l in seg["l"]:
            key=l.get("href")
            if key in seen: continue
            seen.add(key)
            btns += '<a href="'+esc(l["href"] or "#")+'" target="_blank" rel="noopener">'+esc(tr(l.get("text"), lang) or "Dokument")+'</a>'
        if btns: inner += '<div class="lks">'+btns+'</div>'
    return inner or '<div class="empty">–</div>'

# build theme html
GROUP_ORDER = ["Sport & Athlet:in","Material","Strukturen & Umfeld"]
def theme_html(t, idx, lang):
    title = tr(t["title"], lang)
    # header row
    th = '<div class="r head"><div class="rl corner"></div>'
    for si,s in enumerate(STAGES):
        age = AGE.get(s,"")
        th += '<div class="c hd ph-'+ph(s)+'" data-idx="'+str(si)+'" title="Spalte hervorheben"><span class="st">'+s+'</span><span class="stf">'+FULL[s]+(' · '+age if age else '')+'</span></div>'
    th += '</div>'
    body = ""
    for r in t["rows"]:
        lbl = tr(r["label"], lang) or ""
        body += '<div class="r">'
        body += '<div class="rl">'+esc(lbl)+'</div>' if lbl else '<div class="rl nolbl"></div>'
        # render segs with spans; we lay out as 10 cells using grid-column span
        for seg in r["segs"]:
            span = seg["to"] - seg["from"] + 1
            cls = "ph-"+ph(STAGES[seg["from"]])
            # if seg spans multiple phases, neutral
            phs = set(ph(STAGES[i]) for i in range(seg["from"], seg["to"]+1))
            if len(phs) > 1: cls = "ph-multi"
            body += '<div class="c cell '+cls+'" data-from="'+str(seg["from"])+'" data-to="'+str(seg["to"])+'" style="grid-column: span '+str(span)+'"><div class="cwrap">'+render_cell(seg, lang)+'</div><button class="more" hidden>'+esc(tr("mehr ▾", lang))+'</button></div>'
        body += '</div>'
    return ('<details class="theme" id="t'+str(idx)+'" open data-title="'+esc(title.lower())+'">'
            '<summary><span class="tt">'+esc(title)+'</span></summary>'
            '<div class="scroller"><div class="grid">'+th+body+'</div></div></details>')

def build_sections(lang):
    s = ""
    for g in GROUP_ORDER:
        items=[(i,th) for i,th in enumerate(d["themes"]) if th["group"]==g]
        if not items: continue
        s += '<h2 class="grp">'+esc(tr(g, lang))+'</h2>'
        for i,th in items:
            s += theme_html(th, i, lang)
    return s

def build_jump(lang):
    return "".join('<option value="t'+str(i)+'">'+esc(tr(th["title"], lang))+'</option>' for i,th in enumerate(d["themes"]))

CSS = r"""
:root{--red:#d52b1e;--ink:#1d2630;--mut:#697080;--line:#e4e8 ec;--line:#e4e8ec;--bg:#eef1f4;--card:#fff;
--found:#1f8fa6;--found-t:#0d5e6e;--found-bg:#ecf6f8;
--talent:#e2a900;--talent-t:#8a6a00;--talent-bg:#fdf7e4;
--elite:#e8772e;--elite-t:#a8511a;--elite-bg:#fdefe5;
--mast:#d52b1e;--mast-t:#9c1d14;--mast-bg:#fce9e7;
--colw:200px;--lblw:146px;--top:54px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45;font-size:13px}
header.top{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:10px 18px;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;height:var(--top)}
header.top h1{font-size:16px;margin:0;font-weight:800;color:var(--red);white-space:nowrap;letter-spacing:.2px}
header.top h1 b{color:var(--ink);font-weight:700}
header.top h1 .fF{color:var(--found)}header.top h1 .fT{color:var(--talent)}header.top h1 .fE{color:var(--elite)}header.top h1 .fM{color:var(--mast)}header.top h1 .fF,header.top h1 .fT,header.top h1 .fE,header.top h1 .fM{font-weight:900}
header.top h1 .sk{color:var(--ink)}
.langsw{display:flex;gap:2px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:2px}
.langsw a{font-size:11.5px;font-weight:800;color:var(--mut);text-decoration:none;padding:4px 9px;border-radius:6px;letter-spacing:.03em}
.langsw a.active{background:var(--red);color:#fff}
.langsw a:hover:not(.active){background:#fff;color:var(--ink)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-left:auto}
.tools input,.tools select,.tools button{font:inherit;font-size:13px;padding:7px 11px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
.tools input{min-width:210px}
.tools button{cursor:pointer;font-weight:600}
.tools button:hover{background:var(--bg)}
.tools .cnt{font-size:12px;color:var(--mut);font-weight:600;white-space:nowrap}
.wrap{max-width:1500px;margin:0 auto;padding:14px 18px 90px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:8px;font-size:13px;color:var(--mut)}
.intro b{color:var(--ink)}
.legend{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}
.legend span{font-size:11.5px;padding:4px 11px;border-radius:30px;font-weight:700}
.lg-f{background:var(--found-bg);color:var(--found-t)}.lg-t{background:var(--talent-bg);color:var(--talent-t)}.lg-e{background:var(--elite-bg);color:var(--elite-t)}.lg-m{background:var(--mast-bg);color:var(--mast-t)}
.hint{font-size:12px;color:var(--mut);margin:14px 2px 2px;display:flex;align-items:center;gap:6px}
h2.grp{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin:22px 0 9px;font-weight:800}
details.theme{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--red);border-radius:9px;margin-bottom:8px;scroll-margin-top:66px;overflow:hidden}
details.theme>summary{cursor:pointer;padding:9px 14px;list-style:none;display:flex;align-items:center;gap:10px}
details.theme>summary:hover{background:#fafbfc}
details.theme>summary::-webkit-details-marker{display:none}
summary .tt{font-size:14px;font-weight:800;display:flex;align-items:center;gap:9px}
summary .tt::before{content:'';width:7px;height:7px;border-right:2px solid var(--red);border-bottom:2px solid var(--red);transform:rotate(-45deg);transition:transform .15s;margin-left:1px}
details[open] summary .tt::before{transform:rotate(45deg)}
.scroller{overflow-x:auto;overflow-y:hidden;padding:0 12px 13px}
.grid{min-width:max-content;display:flex;flex-direction:column;gap:6px}
.r{display:grid;grid-template-columns:var(--lblw) repeat(10,var(--colw));gap:6px;align-items:start}
.rl{position:sticky;left:0;z-index:5;align-self:stretch;background:var(--card);font-weight:700;font-size:11.5px;color:var(--ink);display:flex;align-items:flex-start;padding:9px 10px;border-radius:8px;border:1px solid var(--line);box-shadow:0 0 0 7px var(--card),-14px 0 0 7px var(--card),9px 0 9px -6px rgba(0,0,0,.2)}
.rl.nolbl{background:var(--card);border:1px dashed #e9ecef}
.r.head{position:relative;z-index:2}
.r.head .rl.corner{position:sticky;left:0;z-index:6;background:var(--card);border:none}
.c.hd{border-radius:8px;padding:6px 6px;text-align:center;display:flex;flex-direction:column;gap:0;justify-content:center}
.c.hd .st{font-size:13.5px;font-weight:800}
.c.hd .stf{font-size:9px;font-weight:600;opacity:.92}
.c.hd[data-idx]{cursor:pointer;transition:box-shadow .12s}
.c.hd[data-idx]:hover{box-shadow:inset 0 0 0 2px rgba(255,255,255,.7)}
.c.hd.active{box-shadow:inset 0 0 0 3px rgba(0,0,0,.45)}
.cell.hl-foundation{background:var(--found-bg)}
.cell.hl-talent{background:var(--talent-bg)}
.cell.hl-elite{background:var(--elite-bg)}
.cell.hl-mastery{background:var(--mast-bg)}
.ph-foundation{background:var(--found);color:#fff}.ph-talent{background:var(--talent);color:#3b2e00}.ph-elite{background:var(--elite);color:#fff}.ph-mastery{background:var(--mast);color:#fff}
.cell{background:#fff;border:1px solid var(--line);border-radius:8px;position:relative;overflow:hidden;align-self:start}
.cell .cwrap{padding:8px 10px;font-size:11.5px;max-height:210px;overflow:hidden;transition:max-height .25s ease}
.cell.expanded .cwrap{max-height:4000px}
.cell::after{content:'';position:absolute;left:0;right:0;bottom:0;height:32px;background:linear-gradient(180deg,transparent,#fff);pointer-events:none;opacity:0;transition:opacity .2s}
.cell.clamped::after{opacity:1}
.cell.expanded::after{opacity:0}
.cell.ph-foundation{border-top:3px solid var(--found)}.cell.ph-talent{border-top:3px solid var(--talent)}.cell.ph-elite{border-top:3px solid var(--elite)}.cell.ph-mastery{border-top:3px solid var(--mast)}.cell.ph-multi{border-top:3px solid #b6c0cc}
.cwrap p{margin:0 0 6px}.cwrap p:last-child{margin-bottom:0}
.cwrap .bh{font-weight:800;color:var(--ink);font-size:11.5px;margin-bottom:1px}
.cwrap .sh{font-weight:800;color:var(--found-t);font-size:11px;margin:8px 0 1px;letter-spacing:.01em}
.cwrap .sh:first-child{margin-top:0}
.cwrap .lbl{font-weight:700;color:var(--found-t)}
.cwrap ul{margin:2px 0 6px;padding-left:15px}
.cwrap ul.bl li{margin-bottom:2px}
.cwrap ul.sc{list-style:none;padding-left:0}
.cwrap ul.sc li{margin-bottom:4px;padding-left:0}
.cwrap ul.sc .badge{display:inline-block;background:var(--ink);color:#fff;font-size:9.5px;font-weight:700;border-radius:4px;padding:1px 5px;margin-right:4px}
.cwrap .empty{color:#c2c8d0;text-align:center;font-size:14px}
.lks{margin-top:7px;display:flex;flex-direction:column;gap:4px}
.lks a{font-size:11px;color:var(--red);text-decoration:none;font-weight:700;background:var(--mast-bg);padding:5px 8px;border-radius:6px;display:flex;align-items:center;gap:5px}
.lks a::before{content:'📄'}
.lks a:hover{background:#f9d9d5}
.more{position:absolute;bottom:6px;right:8px;z-index:3;font:inherit;font-size:10.5px;font-weight:700;color:var(--red);background:#fff;border:1px solid var(--line);border-radius:20px;padding:2px 9px;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.more:hover{background:var(--mast-bg)}
mark{background:#ffe08a;border-radius:2px;padding:0 1px}
.hidden{display:none!important}
footer{text-align:center;color:var(--mut);font-size:12px;padding:24px}
footer a{color:var(--red)}
@media(max-width:700px){:root{--colw:200px;--lblw:128px}}
"""

JS = r"""
const q=document.getElementById('q');
const themes=[...document.querySelectorAll('details.theme')];
const grps=[...document.querySelectorAll('h2.grp')];
// clamp detection
function setupClamp(){
  document.querySelectorAll('.cell').forEach(cell=>{
    const w=cell.querySelector('.cwrap');const btn=cell.querySelector('.more');
    if(!w||!btn)return;
    if(w.scrollHeight>w.clientHeight+6){cell.classList.add('clamped');btn.hidden=false;}
    else{cell.classList.remove('clamped');btn.hidden=true;}
    btn.onclick=()=>{const ex=cell.classList.toggle('expanded');btn.textContent=ex?I18N.less:I18N.more;};
  });
}
function clearMarks(el){el.querySelectorAll('mark').forEach(m=>m.replaceWith(document.createTextNode(m.textContent)));el.normalize();}
function run(){
  const term=q.value.trim().toLowerCase();
  themes.forEach(clearMarks);
  let vis=0;
  themes.forEach(t=>{
    if(!term){t.classList.remove('hidden');return;}
    const hit=t.innerText.toLowerCase().includes(term);
    t.classList.toggle('hidden',!hit);
    if(hit){vis++;t.open=true;
      const re=new RegExp('('+term.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','gi');
      t.querySelectorAll('.cwrap p,.cwrap li,.tt').forEach(node=>{
        const walk=document.createTreeWalker(node,NodeFilter.SHOW_TEXT,null);const tn=[];let n;
        while(n=walk.nextNode())tn.push(n);
        tn.forEach(x=>{if(x.nodeValue.toLowerCase().includes(term)){const sp=document.createElement('span');sp.innerHTML=x.nodeValue.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])).replace(re,'<mark>$1</mark>');x.replaceWith(sp);}});
      });
    }
  });
  document.getElementById('cnt').textContent=term?(vis+' '+I18N.hits):(themes.length+' '+I18N.themes);
  grps.forEach(g=>{let s=g.nextElementSibling,any=false;while(s&&s.classList.contains('theme')){if(!s.classList.contains('hidden'))any=true;s=s.nextElementSibling;}g.classList.toggle('hidden',!!term&&!any);});
}
q.addEventListener('input',run);
document.getElementById('exp').onclick=()=>{themes.forEach(t=>t.open=true);setTimeout(setupClamp,50);};
document.getElementById('col').onclick=()=>themes.forEach(t=>t.open=false);
document.getElementById('jump').onchange=e=>{const el=document.getElementById(e.target.value);if(el){el.open=true;setTimeout(()=>el.scrollIntoView(),30);}e.target.selectedIndex=0;};
themes.forEach(t=>t.addEventListener('toggle',()=>{if(t.open){const sc=t.querySelector('.scroller');if(sc)sc.scrollLeft=window.__sx||0;setTimeout(setupClamp,50);}}));
window.addEventListener('resize',()=>setTimeout(setupClamp,150));
// --- synchronized horizontal scrolling across all themes ---
const scrollers=[...document.querySelectorAll('.scroller')];
window.__sx=0;let __sy=false;
scrollers.forEach(s=>s.addEventListener('scroll',()=>{
  if(__sy)return;__sy=true;window.__sx=s.scrollLeft;
  scrollers.forEach(o=>{if(o!==s&&o.scrollLeft!==window.__sx)o.scrollLeft=window.__sx;});
  requestAnimationFrame(()=>{__sy=false;});
}));
// --- click a stage header to tint that column in all themes ---
const active=new Set();
function phaseIdx(i){return i<3?'foundation':i<7?'talent':i<9?'elite':'mastery';}
function applyHl(){
  document.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.classList.toggle('active',active.has(+h.dataset.idx)));
  document.querySelectorAll('.cell').forEach(c=>{
    c.classList.remove('hl-foundation','hl-talent','hl-elite','hl-mastery');
    const f=+c.dataset.from,t=+c.dataset.to;
    for(const i of active){if(i>=f&&i<=t){c.classList.add('hl-'+phaseIdx(i));break;}}
  });
}
document.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.addEventListener('click',()=>{
  const i=+h.dataset.idx;active.has(i)?active.delete(i):active.add(i);applyHl();
}));
run();setupClamp();
"""

datestr = datetime.date.today().strftime("%d.%m.%Y")

def lang_switch(active):
    names = {"de": "DE", "fr": "FR", "it": "IT"}
    out = '<div class="langsw">'
    for lg in LANGS:
        cls = ' class="active"' if lg == active else ''
        out += '<a href="'+FILES[lg]+'"'+cls+'>'+names[lg]+'</a>'
    return out + '</div>'

def render_page(lang):
    sections = build_sections(lang)
    jump = build_jump(lang)
    i18n = json.dumps({"more": tr("mehr ▾", lang), "less": tr("weniger ▴", lang),
                       "themes": tr("Themen · F1–M", lang), "hits": tr("Themen mit Treffern", lang)}, ensure_ascii=False)
    aw = esc(tr("Athlet:innen-Weg", lang))
    return ('<!DOCTYPE html><html lang="'+lang+'"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>FTEM Ski Alpin – '+aw+'</title><style>'+CSS+'</style></head><body>'
    '<header class="top"><h1><span class="fF">F</span><span class="fT">T</span><span class="fE">E</span><span class="fM">M</span> <span class="sk">Ski Alpin</span> <b>· '+aw+'</b></h1>'
    +lang_switch(lang)+
    '<div class="tools"><span class="cnt" id="cnt"></span>'
    '<input id="q" type="search" placeholder="'+esc(tr("In allen Inhalten suchen…", lang))+'">'
    '<select id="jump"><option>'+esc(tr("Zu Thema springen…", lang))+'</option>'+jump+'</select>'
    '<button id="exp">'+esc(tr("Alle öffnen", lang))+'</button><button id="col">'+esc(tr("Alle schliessen", lang))+'</button></div></header>'
    '<div class="wrap">'
    '<div class="intro">'+INTRO[lang]+
    '<div class="legend"><span class="lg-f">F1–F3 · Foundation</span><span class="lg-t">T1–T4 · Talent</span><span class="lg-e">E1–E2 · Elite</span><span class="lg-m">M · Mastery</span></div></div>'
    '<div class="hint">'+esc(tr("↔ Tabellen lassen sich seitlich scrollen · 📄 = externes Dokument", lang))+'</div>'
    +sections+
    '<footer>'+esc(tr("Quelle:", lang))+' <a href="https://my.ftem.swiss-ski.ch/dashboard/alpine-ski" target="_blank">my.ftem.swiss-ski.ch</a> · '+esc(tr("aufbereitet am", lang))+' '+datestr+'</footer>'
    '</div><script>const I18N='+i18n+';'+JS+'</script></body></html>')

for lang in LANGS:
    page = render_page(lang)
    open(os.path.join(BASE, FILES[lang]), "w", encoding="utf-8").write(page)
    if lang == "de":
        open(os.path.join(BASE, "ftem-ski-alpin-uebersicht.html"), "w", encoding="utf-8").write(page)
    print("written", FILES[lang], len(page.encode("utf-8")), "bytes")
