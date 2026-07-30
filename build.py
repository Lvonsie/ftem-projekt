import os
# -*- coding: utf-8 -*-
import json, re, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Sportarten-Konfiguration: ftem_sports.json
#   id    -> interner Schluessel (auch fuer #hash-Navigation) und Standard-Datendatei
#   name  -> Anzeigename
#   short -> Kuerzel auf den Auswahl-Karten
#   file  -> (optional) Datendatei; sonst wird ftem_data_<id>.json gesucht
# Sprachen: uebersetzte Texte in translations.json (fr/it, Fallback = Deutsch).
# Ausgabe: pro Sprache EINE Datei (index.html = DE, fr.html, it.html) mit
# Startseite + allen Sportarten, Wechsel per JS/#hash.
# ---------------------------------------------------------------------------
SPORTS = json.load(open(os.path.join(BASE, "ftem_sports.json"), encoding="utf-8"))["sports"]
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

# Kurzbeschrieb "Was ist FTEM?" auf der Auswahlseite (mit Swiss Olympic)
FTEM_INFO = {
 "de": {
   "title": "Was ist FTEM?",
   "lead": 'FTEM ist das gemeinsame Rahmenkonzept von <b>Swiss Olympic</b> und <b>Swiss-Ski</b> für die langfristige Athlet:innen- und Sportentwicklung im Schneesport. Es beschreibt den ganzen Weg – vom ersten Schneekontakt bis zur Weltspitze – in vier Schlüsselphasen und zehn Entwicklungsstufen (F1–M).',
   "phases": [
     ("F","Foundation","F1–F3","Fundament legen: vielseitige Bewegungs- und Schneesport-Grundlagen erwerben, anwenden und festigen."),
     ("T","Talent","T1–T4","Potenzial zeigen und entwickeln: Talente bestätigen sich, trainieren gezielt und schaffen den Durchbruch."),
     ("E","Elite","E1–E2","Die Schweiz international vertreten: Weltcup, WM und Olympische Spiele auf Elite-Niveau."),
     ("M","Mastery","M","Die Weltspitze prägen: über Jahre nachhaltig Erfolge auf höchstem Niveau."),
   ],
 },
 "fr": {
   "title": "Qu&#x27;est-ce que FTEM ?",
   "lead": 'FTEM est le cadre de référence commun de <b>Swiss Olympic</b> et <b>Swiss-Ski</b> pour le développement à long terme des athlètes et du sport dans les sports de neige. Il décrit tout le parcours – du premier contact avec la neige jusqu&#x27;à l&#x27;élite mondiale – en quatre phases clés et dix niveaux de développement (F1–M).',
   "phases": [
     ("F","Foundation","F1–F3","Poser les bases : acquérir, appliquer et consolider des bases variées de mouvement et de sports de neige."),
     ("T","Talent","T1–T4","Révéler et développer le potentiel : les talents se confirment, s&#x27;entraînent de manière ciblée et percent."),
     ("E","Elite","E1–E2","Représenter la Suisse au niveau international : Coupe du monde, championnats du monde et Jeux olympiques."),
     ("M","Mastery","M","Marquer l&#x27;élite mondiale : des succès durables au plus haut niveau pendant des années."),
   ],
 },
 "it": {
   "title": "Che cos&#x27;è FTEM?",
   "lead": 'FTEM è il quadro di riferimento comune di <b>Swiss Olympic</b> e <b>Swiss-Ski</b> per lo sviluppo a lungo termine degli atleti e dello sport negli sport sulla neve. Descrive l&#x27;intero percorso – dal primo contatto con la neve fino all&#x27;élite mondiale – in quattro fasi chiave e dieci livelli di sviluppo (F1–M).',
   "phases": [
     ("F","Foundation","F1–F3","Costruire le basi: acquisire, applicare e consolidare basi motorie e di sport sulla neve variate."),
     ("T","Talent","T1–T4","Mostrare e sviluppare il potenziale: i talenti si confermano, si allenano in modo mirato e sfondano."),
     ("E","Elite","E1–E2","Rappresentare la Svizzera a livello internazionale: Coppa del Mondo, Mondiali e Giochi olimpici."),
     ("M","Mastery","M","Segnare l&#x27;élite mondiale: successi duraturi al massimo livello per anni."),
   ],
 },
}
PLACE = {
 "de": 'Der Athlet:innen-Weg für <b>{name}</b> ist noch nicht erfasst – Inhalte folgen.<br><br>Sobald die Daten vorliegen, kommen sie in die Datei <code>{file}</code> und die Seite wird mit <code>python3 build.py</code> neu erzeugt.',
 "fr": 'Le parcours de l&#x27;athlète pour <b>{name}</b> n&#x27;est pas encore saisi – contenus à venir.<br><br>Dès que les données seront disponibles, elles seront ajoutées au fichier <code>{file}</code> et la page sera régénérée avec <code>python3 build.py</code>.',
 "it": 'Il percorso dell&#x27;atleta per <b>{name}</b> non è ancora disponibile – contenuti in arrivo.<br><br>Non appena i dati saranno disponibili, verranno inseriti nel file <code>{file}</code> e la pagina sarà rigenerata con <code>python3 build.py</code>.',
}
HOME_SUB = {
 "de": "Swiss-Ski Entwicklungsstufen F1–M · Sportart auswählen",
 "fr": "Niveaux de développement Swiss-Ski F1–M · Choisir un sport",
 "it": "Livelli di sviluppo Swiss-Ski F1–M · Scegliere lo sport",
}
NODATA = {"de": "Inhalte folgen", "fr": "Contenus à venir", "it": "Contenuti in arrivo"}
BACK = {"de": "← Sportarten", "fr": "← Sports", "it": "← Sport"}
BACK_TITLE = {"de": "Zurück zur Auswahl", "fr": "Retour à la sélection", "it": "Torna alla selezione"}

FULL = {"F1":"Foundation 1","F2":"Foundation 2","F3":"Foundation 3","T1":"Talent 1","T2":"Talent 2","T3":"Talent 3","T4":"Talent 4","E1":"Elite 1","E2":"Elite 2","M":"Mastery"}
AGE = {"F1":"U8","F2":"U8–U10","F3":"U10–U12","T1":"U12–U14","T2":"U14–U16","T3":"U16+","T4":"U18+","E1":"","E2":"","M":""}
GROUP_ORDER = ["Sport & Athlet:in","Material","Strukturen & Umfeld"]

def ph(st): return "foundation" if st[0]=="F" else "talent" if st[0]=="T" else "elite" if st[0]=="E" else "mastery"
def esc(s): return html.escape(s, quote=True)

# "FTEM" in den vier Phasenfarben (Anpassung von Luca, Commit "Farben FTEM")
FTEM = '<span class="fF">F</span><span class="fT">T</span><span class="fE">E</span><span class="fM">M</span>'

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

def theme_html(t, idx, stages, prefix, lang):
    title = tr(t["title"], lang)
    # header row
    th = '<div class="r head"><div class="rl corner"></div>'
    for si,s in enumerate(stages):
        age = AGE.get(s,"")
        th += '<div class="c hd ph-'+ph(s)+'" data-idx="'+str(si)+'" title="'+esc(tr("Spalte hervorheben", lang))+'"><span class="st">'+s+'</span><span class="stf">'+FULL[s]+(' · '+age if age else '')+'</span></div>'
    th += '</div>'
    body = ""
    for r in t["rows"]:
        lbl = tr(r["label"], lang) or ""
        body += '<div class="r">'
        body += '<div class="rl">'+esc(lbl)+'</div>' if lbl else '<div class="rl nolbl"></div>'
        # render segs with spans; we lay out as 10 cells using grid-column span
        for seg in r["segs"]:
            span = seg["to"] - seg["from"] + 1
            cls = "ph-"+ph(stages[seg["from"]])
            # if seg spans multiple phases, neutral
            phs = set(ph(stages[i]) for i in range(seg["from"], seg["to"]+1))
            if len(phs) > 1: cls = "ph-multi"
            body += '<div class="c cell '+cls+'" data-from="'+str(seg["from"])+'" data-to="'+str(seg["to"])+'" style="grid-column: span '+str(span)+'"><div class="cwrap">'+render_cell(seg, lang)+'</div><button class="more" hidden>'+esc(tr("mehr ▾", lang))+'</button></div>'
        body += '</div>'
    return ('<details class="theme" id="'+prefix+'-t'+str(idx)+'" open data-title="'+esc(title.lower())+'">'
            '<summary><span class="tt">'+esc(title)+'</span></summary>'
            '<div class="scroller"><div class="grid">'+th+body+'</div></div></details>')

def build_sections(d, prefix, lang):
    themes = d["themes"]
    stages = d["stages"]
    seen = list(dict.fromkeys(t["group"] for t in themes))
    order = [g for g in GROUP_ORDER if g in seen] + [g for g in seen if g not in GROUP_ORDER]
    sections=""
    for g in order:
        items=[(i,t) for i,t in enumerate(themes) if t["group"]==g]
        if not items: continue
        sections += '<h2 class="grp">'+esc(tr(g, lang))+'</h2>'
        for i,t in items:
            sections += theme_html(t,i,stages,prefix,lang)
    jump = "".join('<option value="'+prefix+'-t'+str(i)+'">'+esc(tr(t["title"], lang))+'</option>' for i,t in enumerate(themes))
    return sections, jump

def sport_data(sport):
    f = sport.get("file") or ("ftem_data_"+sport["id"]+".json")
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return None

datestr = datetime.date.today().strftime("%d.%m.%Y")

def footer(lang):
    return ('<footer>'+esc(tr("Quelle:", lang))+' <a href="https://my.ftem.swiss-ski.ch" target="_blank" rel="noopener">my.ftem.swiss-ski.ch</a> · '
            +esc(tr("aufbereitet am", lang))+' '+datestr+'</footer>')

def lang_switch(active):
    out = '<div class="langsw">'
    for l in LANGS:
        cls = ' class="active"' if l == active else ''
        out += '<a'+cls+' data-f="'+FILES[l]+'" href="'+FILES[l]+'">'+l.upper()+'</a>'
    return out + '</div>'

def sport_section(sport, d, lang):
    sid = sport["id"]; name = tr(sport["name"], lang)
    aw = esc(tr("Athlet:innen-Weg", lang))
    back = '<a class="back" href="#" title="'+esc(BACK_TITLE[lang])+'">'+esc(BACK[lang])+'</a>'
    if d is None:
        return ('<section class="sport" data-sport="'+sid+'" hidden>'
            '<header class="top">'+back+'<h1>'+FTEM+' <span class="sk">'+esc(name)+'</span> <b>· '+aw+'</b></h1>'
            '<div class="tools">'+lang_switch(lang)+'</div></header>'
            '<div class="wrap"><div class="placeholder">'
            '<div class="big">'+esc(name)+'</div>'
            +PLACE[lang].format(name=esc(name), file='ftem_data_'+esc(sid)+'.json')+
            '</div>'+footer(lang)+'</div></section>')
    sections, jump_opts = build_sections(d, sid, lang)
    n_themes = len(d["themes"])
    return ('<section class="sport" data-sport="'+sid+'" hidden>'
        '<header class="top">'+back+'<h1>'+FTEM+' <span class="sk">'+esc(name)+'</span> <b>· '+aw+'</b></h1>'
        '<div class="tools">'+lang_switch(lang)+'<span class="cnt"></span>'
        '<input class="q" type="search" placeholder="'+esc(tr("In allen Inhalten suchen…", lang))+'">'
        '<select class="jump"><option>'+esc(tr("Zu Thema springen…", lang))+'</option>'+jump_opts+'</select>'
        '<button class="exp">'+esc(tr("Alle öffnen", lang))+'</button><button class="col">'+esc(tr("Alle schliessen", lang))+'</button></div></header>'
        '<div class="wrap">'
        +sections+footer(lang)+'</div></section>')

# --- Startseite (Sportart-Auswahl) -----------------------------------------
def home_html(datamap, lang):
    cards = ""
    for i, s in enumerate(SPORTS):
        has = datamap[s["id"]] is not None
        name = tr(s["name"], lang)
        # Logo-Platz: sobald ein Sportarten-Logo vorliegt, in ftem_sports.json
        # z. B. "icon": "logos/ski-alpin.svg" ergaenzen -> wird statt Kuerzel gezeigt
        ico = s.get("icon")
        ico_html = ('<img src="'+esc(ico)+'" alt="" loading="lazy">') if ico else esc(s["short"])
        cards += ('<a class="card'+('' if has else ' nodata')+'" href="#'+s["id"]+'" style="animation-delay:'+str(i*50)+'ms">'
                  '<span class="ab'+(' has-img' if ico else '')+'">'+ico_html+'</span>'
                  '<span class="cn">'+esc(name)+'</span>'
                  +('' if has else '<span class="tag">'+esc(NODATA[lang])+'</span>')+'</a>')
    info = FTEM_INFO[lang]
    phase_cls = {"F":"p-f","T":"p-t","E":"p-e","M":"p-m"}
    phases = "".join('<div class="phase '+phase_cls[k]+'"><span class="pl">'+k+'</span>'
                     '<span class="pn">'+pn+'</span><span class="pr">'+pr+'</span>'
                     '<p>'+desc+'</p></div>' for k,pn,pr,desc in info["phases"])
    ftem_info = ('<div class="ftem-info">'
                 '<h2>'+info["title"]+'</h2>'
                 '<p class="lead">'+info["lead"]+'</p>'
                 '<div class="phases">'+phases+'</div></div>')
    return ('<section id="home"><div class="home-hero">'
            '<h1>'+FTEM+' <b>'+esc(tr("Athlet:innen-Weg", lang))+'</b></h1>'
            '<p class="sub">'+esc(HOME_SUB[lang])+'</p>'
            '<div class="hero-lang">'+lang_switch(lang)+'</div>'
            '<div class="grid-sports">'+cards+'</div>'
            +ftem_info+footer(lang)+'</div></section>')

CSS = r"""
:root{--red:#d52b1e;--ink:#1d2630;--mut:#697080;--line:#e4e8ec;--bg:#eef1f4;--card:#fff;
--found:#1f8fa6;--found-t:#0d5e6e;--found-bg:#ecf6f8;
--talent:#e2a900;--talent-t:#8a6a00;--talent-bg:#fdf7e4;
--elite:#e8772e;--elite-t:#a8511a;--elite-bg:#fdefe5;
--mast:#d52b1e;--mast-t:#9c1d14;--mast-bg:#fce9e7;
--colw:200px;--lblw:146px;--top:54px}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
[hidden]{display:none!important}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45;font-size:13px}
.langsw{display:flex;gap:2px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:2px}
.langsw a{font-size:11.5px;font-weight:800;color:var(--mut);text-decoration:none;padding:4px 9px;border-radius:6px;letter-spacing:.03em}
.langsw a.active{background:var(--red);color:#fff}
.langsw a:hover:not(.active){background:#fff;color:var(--ink)}
/* Startseite */
#home .home-hero{max-width:980px;margin:0 auto;padding:60px 24px 30px;text-align:center}
#home h1{font-size:30px;margin:0 0 6px;font-weight:800;color:var(--red);letter-spacing:.2px}
#home h1 b{color:var(--ink);font-weight:800}
#home .sub{color:var(--mut);font-size:14px;margin:0 0 18px}
#home .hero-lang{display:flex;justify-content:center;margin:0 0 30px}
.grid-sports{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px;text-align:center}
@keyframes cardIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.grid-sports .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 12px 20px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;align-items:center;gap:9px;transition:box-shadow .18s,transform .18s,border-color .18s;animation:cardIn .45s ease both}
.grid-sports .card:hover{border-color:var(--red);box-shadow:0 10px 24px rgba(213,43,30,.14);transform:translateY(-4px) scale(1.02)}
.grid-sports .ab{width:60px;height:60px;border-radius:50%;background:var(--red);color:#fff;font-weight:800;font-size:17px;display:flex;align-items:center;justify-content:center;transition:transform .2s ease;overflow:hidden}
.grid-sports .card:hover .ab{transform:scale(1.12) rotate(-6deg)}
.grid-sports .ab.has-img{background:#fff;border:1px solid var(--line)}
.grid-sports .ab img{width:40px;height:40px;object-fit:contain}
.grid-sports .card.nodata .ab{background:#b6c0cc}
.grid-sports .card.nodata .ab.has-img{background:#fff;filter:grayscale(1);opacity:.6}
.grid-sports .cn{font-weight:800;font-size:13.5px}
.grid-sports .tag{font-size:10px;font-weight:700;color:var(--mut);background:var(--bg);border-radius:20px;padding:2px 9px}
/* "Was ist FTEM?" */
.ftem-info{margin-top:46px;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 26px 22px}
.ftem-info h2{margin:0 0 8px;font-size:17px;font-weight:800}
.ftem-info .lead{color:var(--mut);font-size:13px;line-height:1.6;margin:0 0 18px}
.ftem-info .lead b{color:var(--ink)}
.phases{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.phase{border:1px solid var(--line);border-radius:12px;border-top:4px solid;padding:13px 14px 11px;transition:transform .16s,box-shadow .16s}
.phase:hover{transform:translateY(-3px);box-shadow:0 8px 18px rgba(0,0,0,.08)}
.phase .pl{font-size:22px;font-weight:900;margin-right:7px}
.phase .pn{font-weight:800;font-size:13.5px}
.phase .pr{float:right;font-size:10.5px;font-weight:700;color:var(--mut);background:var(--bg);border-radius:20px;padding:2px 8px;margin-top:4px}
.phase p{margin:7px 0 0;font-size:12px;color:var(--mut);line-height:1.5}
.p-f{border-top-color:var(--found)}.p-f .pl{color:var(--found)}
.p-t{border-top-color:var(--talent)}.p-t .pl{color:var(--talent)}
.p-e{border-top-color:var(--elite)}.p-e .pl{color:var(--elite)}
.p-m{border-top-color:var(--mast)}.p-m .pl{color:var(--mast)}
/* Sport-Ansicht */
header.top{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:10px 18px;display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;height:var(--top)}
header.top .back{font-size:12.5px;font-weight:700;color:var(--ink);text-decoration:none;background:var(--bg);border:1px solid var(--line);border-radius:20px;padding:6px 13px;white-space:nowrap}
header.top .back:hover{background:#fff;border-color:var(--red);color:var(--red)}
header.top h1{font-size:16px;margin:0;font-weight:800;color:var(--red);white-space:nowrap;letter-spacing:.2px}
header.top h1 b{color:var(--ink);font-weight:700}
h1 .fF{color:var(--found)}h1 .fT{color:var(--talent)}h1 .fE{color:var(--elite)}h1 .fM{color:var(--mast)}
h1 .fF,h1 .fT,h1 .fE,h1 .fM{font-weight:900}
h1 .sk{color:var(--ink)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-left:auto}
.tools input,.tools select,.tools button{font:inherit;font-size:13px;padding:7px 11px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
.tools input{min-width:210px}
.tools button{cursor:pointer;font-weight:600}
.tools button:hover{background:var(--bg)}
.tools .cnt{font-size:12px;color:var(--mut);font-weight:600;white-space:nowrap}
.wrap{max-width:1500px;margin:0 auto;padding:14px 18px 90px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:8px;font-size:13px;color:var(--mut)}
.intro b{color:var(--ink)}
.placeholder{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:64px 24px;margin-top:24px;text-align:center;color:var(--mut)}
.placeholder .big{font-size:20px;font-weight:800;color:var(--ink);margin-bottom:10px}
.placeholder code{background:var(--bg);border-radius:6px;padding:2px 6px;font-size:12px}
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
const SPORT_IDS = __SPORT_IDS__;
const I18N = __I18N__;
const sections = [...document.querySelectorAll('section.sport')];
const home = document.getElementById('home');

// Sprachwechsel behaelt die aktuelle Sportart (#hash) bei
document.querySelectorAll('.langsw a').forEach(a=>a.addEventListener('click',()=>{a.href=a.dataset.f+location.hash;}));

// ---- pro Sportart gekapselte Interaktivitaet ----
function initSport(sec){
  const q = sec.querySelector('.q');
  const themes = [...sec.querySelectorAll('details.theme')];
  const grps = [...sec.querySelectorAll('h2.grp')];
  function setupClamp(){
    sec.querySelectorAll('.cell').forEach(cell=>{
      const w=cell.querySelector('.cwrap');const btn=cell.querySelector('.more');
      if(!w||!btn)return;
      if(w.scrollHeight>w.clientHeight+6){cell.classList.add('clamped');btn.hidden=false;}
      else{cell.classList.remove('clamped');btn.hidden=true;}
      btn.onclick=()=>{const ex=cell.classList.toggle('expanded');btn.textContent=ex?I18N.less:I18N.more;};
    });
  }
  sec.__clamp = setupClamp;
  if(!q) return; // Platzhalter-Seite ohne Werkzeuge
  const cnt = sec.querySelector('.cnt');
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
    if(cnt)cnt.textContent=term?(vis+' '+I18N.hits):(themes.length+' '+I18N.themes);
    grps.forEach(g=>{let s=g.nextElementSibling,any=false;while(s&&s.classList.contains('theme')){if(!s.classList.contains('hidden'))any=true;s=s.nextElementSibling;}g.classList.toggle('hidden',!!term&&!any);});
  }
  q.addEventListener('input',run);
  sec.querySelector('.exp').onclick=()=>{themes.forEach(t=>t.open=true);setTimeout(setupClamp,50);};
  sec.querySelector('.col').onclick=()=>themes.forEach(t=>t.open=false);
  sec.querySelector('.jump').onchange=e=>{const el=document.getElementById(e.target.value);if(el){el.open=true;setTimeout(()=>el.scrollIntoView(),30);}e.target.selectedIndex=0;};
  themes.forEach(t=>t.addEventListener('toggle',()=>{if(t.open){const sc=t.querySelector('.scroller');if(sc)sc.scrollLeft=sec.__sx||0;setTimeout(setupClamp,50);}}));
  window.addEventListener('resize',()=>{if(!sec.hidden)setTimeout(setupClamp,150);});
  // synchronisiertes Seitwaerts-Scrollen innerhalb der Sportart
  const scrollers=[...sec.querySelectorAll('.scroller')];
  sec.__sx=0;let sy=false;
  scrollers.forEach(s=>s.addEventListener('scroll',()=>{
    if(sy)return;sy=true;sec.__sx=s.scrollLeft;
    scrollers.forEach(o=>{if(o!==s&&o.scrollLeft!==sec.__sx)o.scrollLeft=sec.__sx;});
    requestAnimationFrame(()=>{sy=false;});
  }));
  // Stufen-Spalten hervorheben
  const active=new Set();
  function phaseIdx(i){return i<3?'foundation':i<7?'talent':i<9?'elite':'mastery';}
  function applyHl(){
    sec.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.classList.toggle('active',active.has(+h.dataset.idx)));
    sec.querySelectorAll('.cell').forEach(c=>{
      c.classList.remove('hl-foundation','hl-talent','hl-elite','hl-mastery');
      const f=+c.dataset.from,t=+c.dataset.to;
      for(const i of active){if(i>=f&&i<=t){c.classList.add('hl-'+phaseIdx(i));break;}}
    });
  }
  sec.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.addEventListener('click',()=>{
    const i=+h.dataset.idx;active.has(i)?active.delete(i):active.add(i);applyHl();
  }));
  run();
}
sections.forEach(initSport);

// ---- Umschalten Startseite <-> Sportart (per #hash, Zurueck-Taste funktioniert) ----
function show(id){
  home.hidden = !!id;
  sections.forEach(s=>{s.hidden = s.dataset.sport!==id;});
  window.scrollTo(0,0);
  if(id){
    const sec=sections.find(s=>s.dataset.sport===id);
    if(sec&&sec.__clamp)setTimeout(sec.__clamp,60);
  }
}
function route(){
  const id=decodeURIComponent(location.hash.replace('#',''));
  show(SPORT_IDS.includes(id)?id:'');
}
window.addEventListener('hashchange',route);
route();
"""

datamap = {s["id"]: sport_data(s) for s in SPORTS}
ids_with_data = [s["id"] for s in SPORTS if datamap[s["id"]] is not None]

for lang in LANGS:
    body = home_html(datamap, lang) + "".join(sport_section(s, datamap[s["id"]], lang) for s in SPORTS)
    i18n = {"more": tr("mehr ▾", lang), "less": tr("weniger ▴", lang),
            "themes": tr("Themen · F1–M", lang), "hits": tr("Themen mit Treffern", lang)}
    js = (JS.replace("__SPORT_IDS__", json.dumps([s["id"] for s in SPORTS]))
            .replace("__I18N__", json.dumps(i18n, ensure_ascii=False)))
    page = ('<!DOCTYPE html><html lang="'+lang+'"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>FTEM – '+esc(tr("Athlet:innen-Weg", lang))+'</title><style>'+CSS+'</style></head>'
        '<body>'+body+'<script>'+js+'</script></body></html>')
    out = os.path.join(BASE, FILES[lang])
    open(out,"w",encoding="utf-8").write(page)
    print("written", FILES[lang], len(page.encode("utf-8")), "bytes")

print("Sportarten mit Inhalt:", ", ".join(ids_with_data) or "-")
