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

# --- Admin-Bereich -----------------------------------------------------------
# Passwort fuer den Admin-/Bearbeitungsbereich (dezentes Schloss-Icon unten auf der Startseite)
ADMIN_PW = "ftem26*"
# Cloud-Speicher (Supabase) fuer direkt gespeicherte, fuer alle sichtbare Aenderungen.
# Einmalig eintragen (siehe SETUP-ADMIN.md). Solange leer: Seite laeuft normal,
# Admin bietet dann Datei-Download als Rueckfall.
SUPABASE_URL = "https://xphbwnzyebbejsdeqled.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_"

# Live-Adresse der Seite (Netlify), z. B. "https://ftem-projekt.netlify.app".
# Wird fuer das Teilen-Vorschaubild (Open Graph) als absolute Bild-URL genutzt.
# Leer lassen = relative URL (funktioniert bei vielen, aber nicht allen Diensten).
SITE_URL = "https://ftemschneesport.netlify.app"

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
# Fallback, falls eine Datendatei keine "ages" enthaelt (Alterskategorien pro Sportart)
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
        if intro: out += '<p class="bi">'+esc(intro[0])+'</p>'
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

def render_cell(seg, lang, cid=None, edit=False):
    if edit:
        raw = seg.get("v") or ""
        return '<textarea class="cedit" data-cid="'+esc(cid or "")+'">'+esc(raw)+'</textarea>'
    txt = (tr(seg["v"], lang) or "").strip()
    link_texts = set(tr(l["text"], lang) for l in seg["l"] if l.get("text"))
    inner = ""
    if txt:
        blocks = re.split(r'\n\s*\n', txt)
        parts = [render_block(bl, link_texts) for bl in blocks]
        inner = "".join(p for p in parts if p)
    text_html = inner or '<div class="empty">–</div>'
    cidattr = (' data-cid="'+esc(cid)+'"') if cid else ''
    out = '<div class="ctext"'+cidattr+'>'+text_html+'</div>'
    if seg["l"]:
        seen=set(); btns=""
        for l in seg["l"]:
            key=l.get("href")
            if key in seen: continue
            seen.add(key)
            btns += '<a href="'+esc(l["href"] or "#")+'" target="_blank" rel="noopener">'+esc(tr(l.get("text"), lang) or "Dokument")+'</a>'
        if btns: out += '<div class="lks">'+btns+'</div>'
    return out

# --- Themen-Icons (Inline-SVG, offline) + dezente Bereichsfarben ---
GROUP_COLORS = {
    "Sport & Athlet:in":    ("#6274a0", "rgba(98,116,160,.15)"),   # gedaempftes Blaugrau
    "Material":             ("#9c8a70", "rgba(156,138,112,.16)"),  # Taupe / Sandton
    "Strukturen & Umfeld":  ("#8b7398", "rgba(139,115,152,.16)"),  # mattes Mauve
}
def group_accent(g):
    return GROUP_COLORS.get(g, ("#7a828c", "rgba(122,130,140,.15)"))

_ICONS = {
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "calendar": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>',
 "apple": '<path d="M12 8c1.4-2.2 5-1.8 5 1.6 0 3.6-2.4 8.4-5 8.4S7 13.2 7 9.6C7 6.2 10.6 5.8 12 8z"/><path d="M12 8c0-2 .9-3 2.2-3.4"/>',
 "moon": '<path d="M12 3a6.5 6.5 0 0 0 9 9 9 9 0 1 1-9-9z"/>',
 "mood": '<circle cx="12" cy="12" r="9"/><path d="M9 10h.01M15 10h.01M9 14.5c.9 1 2 1 3 1s2.1 0 3-1"/>',
 "activity": '<path d="M3 12h4l2.5 6 4-13 2.5 7H21"/>',
 "rotate": '<path d="M4.5 12a7.5 7.5 0 0 1 12.5-5.5L20 9M19.5 12a7.5 7.5 0 0 1-12.5 5.5L4 15"/><path d="M20 5v4h-4M4 19v-4h4"/>',
 "barbell": '<path d="M2 12h2M20 12h2M4 9v6M20 9v6M7 7.5v9M17 7.5v9M7 12h10"/>',
 "bolt": '<path d="M13 3 4 14h6l-1 7 9-11h-6l1-7z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
 "box": '<path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/>',
 "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5.5a2 2 0 0 0 2.5 3M16 6h2.5a2 2 0 0 1-2.5 3"/><path d="M10 15h4M9 20h6M11 15l-1 5M13 15l1 5"/>',
 "flag": '<path d="M6 21V4M6 4h12l-2.5 4L18 12H6"/>',
 "users": '<circle cx="9" cy="8" r="3"/><path d="M4 20c0-2.8 2.2-5 5-5s5 2.2 5 5"/><path d="M15 5.5a3 3 0 0 1 0 5M20 20c0-2-1.1-3.7-2.7-4.5"/>',
 "list": '<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4" cy="6" r="1" fill="currentColor" stroke="none"/><circle cx="4" cy="12" r="1" fill="currentColor" stroke="none"/><circle cx="4" cy="18" r="1" fill="currentColor" stroke="none"/>',
}
_KEYMAP = [
 (("trainingsstund","entwicklungsfokus","trainings","stunden","umfang"),"clock"),
 (("makroplan","periodis","jahresplan","planung"),"calendar"),
 (("ernähr","ernaehr","nutrition"),"apple"),
 (("schlaf","regenerat","erholung","recovery"),"moon"),
 (("psyche","mental","kopf"),"mood"),
 (("ausdauer","kondition","kapazit"),"activity"),
 (("mobilit","beweglich","flexib"),"rotate"),
 (("kraft","explosiv","power"),"barbell"),
 (("technik","taktik"),"target"),
 (("schnellig","agilit","speed"),"bolt"),
 (("material","ausrüst","ausruest"),"box"),
 (("förderge","foerderge","gefäss","gefaess","kader","talentpool"),"trophy"),
 (("wettkampf","wettkämpf","wettkaempf","selekt","rennen"),"flag"),
 (("umfeld","eltern","schule","beruf","management","betreu"),"users"),
]
def theme_icon(title):
    t = (title or "").lower()
    for keys, name in _KEYMAP:
        if any(k in t for k in keys):
            return '<svg viewBox="0 0 24 24" aria-hidden="true">'+_ICONS[name]+'</svg>'
    return '<svg viewBox="0 0 24 24" aria-hidden="true">'+_ICONS["list"]+'</svg>'

def theme_html(t, idx, stages, prefix, lang, ages, edit=False, group=None):
    title = tr(t["title"], lang)
    bar, chip = group_accent(group)
    # header row
    th = '<div class="r head"><div class="rl corner"></div>'
    for si,s in enumerate(stages):
        age = ages.get(s,"")
        th += '<div class="c hd ph-'+ph(s)+'" data-idx="'+str(si)+'" title="'+esc(tr("Spalte hervorheben", lang))+'"><span class="st">'+FULL[s]+'</span>'+('<span class="stf">'+age+'</span>' if age else '')+'</div>'
    th += '</div>'
    body = ""
    for ri, r in enumerate(t["rows"]):
        lbl = tr(r["label"], lang) or ""
        body += '<div class="r">'
        body += '<div class="rl">'+esc(lbl)+'</div>' if lbl else '<div class="rl nolbl"></div>'
        # render segs with spans; we lay out as 10 cells using grid-column span
        for si, seg in enumerate(r["segs"]):
            span = seg["to"] - seg["from"] + 1
            cls = "ph-"+ph(stages[seg["from"]])
            # if seg spans multiple phases, neutral
            phs = set(ph(stages[i]) for i in range(seg["from"], seg["to"]+1))
            if len(phs) > 1: cls = "ph-multi"
            cid = prefix+"|"+str(idx)+"|"+str(ri)+"|"+str(si)
            more = '' if edit else '<button class="more" hidden>'+esc(tr("mehr ▾", lang))+'</button>'
            body += '<div class="c cell '+cls+'" data-from="'+str(seg["from"])+'" data-to="'+str(seg["to"])+'" style="grid-column: span '+str(span)+'"><div class="cwrap">'+render_cell(seg, lang, cid, edit)+'</div>'+more+'</div>'
        body += '</div>'
    opn = ' open' if edit else ''
    return ('<details class="theme'+(' edit' if edit else '')+'"'+opn+' id="'+prefix+'-t'+str(idx)+'" data-title="'+esc(title.lower())+'" style="border-left-color:'+bar+'">'
            '<summary><span class="ticon" style="color:'+bar+';background:'+chip+'">'+theme_icon(title)+'</span>'
            '<span class="tt">'+esc(title)+'</span><span class="tchev"></span></summary>'
            '<div class="scroller"><div class="grid">'+th+body+'</div></div></details>')

def build_sections(d, prefix, lang, edit=False):
    themes = d["themes"]
    stages = d["stages"]
    ages = {k: v for k, v in (d.get("ages") or AGE).items() if v}
    seen = list(dict.fromkeys(t["group"] for t in themes))
    order = [g for g in GROUP_ORDER if g in seen] + [g for g in seen if g not in GROUP_ORDER]
    sections=""
    for g in order:
        items=[(i,t) for i,t in enumerate(themes) if t["group"]==g]
        if not items: continue
        gbar, gchip = group_accent(g)
        sections += '<h2 class="grp" style="--gc:'+gbar+'">'+esc(tr(g, lang))+'</h2>'
        for i,t in items:
            sections += theme_html(t,i,stages,prefix,lang,ages,edit,g)
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

def sport_section(sport, d, lang, edit=False):
    sid = sport["id"]; name = tr(sport["name"], lang)
    if edit and d is not None:
        sections, _ = build_sections(d, sid, lang, edit=True)
        return '<section class="sport" data-sport="'+sid+'" hidden><div class="wrap">'+sections+'</div></section>'
    aw = esc(tr("Athlet:innen-Weg", lang))
    back = '<a class="back" href="#" title="'+esc(BACK_TITLE[lang])+'">'+esc(BACK[lang])+'</a>'
    if sport.get("icon"):
        back += '<img class="sicon" src="'+esc(sport["icon"])+'" alt="'+esc(name)+'" width="32" height="32" decoding="async">'
    if d is None:
        return ('<section class="sport" data-sport="'+sid+'" hidden>'
            '<header class="top"><div class="ht-l">'+back+'<h1>'+esc(name)+' · '+aw+'</h1></div>'
            '<div class="ht-r">'+lang_switch(lang)+'</div></header>'
            '<div class="wrap"><div class="placeholder">'
            '<div class="big">'+esc(name)+'</div>'
            +PLACE[lang].format(name=esc(name), file='ftem_data_'+esc(sid)+'.json')+
            '</div></div></section>')
    sections, jump_opts = build_sections(d, sid, lang)
    n_themes = len(d["themes"])
    return ('<section class="sport" data-sport="'+sid+'" hidden>'
        '<header class="top"><div class="ht-l">'+back+'<h1>'+esc(name)+' · '+aw+'</h1></div>'
        '<div class="ht-c"><input class="q" type="search" placeholder="Search"><span class="hits"></span></div>'
        '<div class="ht-r"><select class="jump"><option>'+esc(tr("Zu Thema springen…", lang))+'</option>'+jump_opts+'</select>'
        '<button class="exp">'+esc(tr("Alle öffnen", lang))+'</button><button class="col">'+esc(tr("Alle schliessen", lang))+'</button>'
        '<button class="pdf" title="'+esc(tr("Drucken / als PDF speichern", lang))+'" aria-label="'+esc(tr("Drucken / als PDF speichern", lang))+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="7" rx="1"/><circle cx="17.5" cy="12" r="1" fill="currentColor" stroke="none"/></svg></button>'
        +lang_switch(lang)+'</div></header>'
        '<div class="wrap">'
        +sections+'</div></section>')

# --- Startseite (Sportart-Auswahl) -----------------------------------------
# Positionen der Sternbild-Knoten (x%, y%) auf der Hero-Flaeche
# Entlang der Bergsilhouette von hero.jpg: unten links im Vorgelaende startend,
# ueber den linken Grat zum Gipfelbereich, rechts wieder abfallend.
# Strenges Zickzack (Gipfel/Tal im Wechsel): so laufen die Linien immer VON der
# Beschriftung weg und keine Schrift kreuzt eine Linie.
CONS_POS = [(7,74),(14,49),(22,71),(29,35),(37,64),(44,48),(55,72),(66,40),(77,67),(89,43)]
# durchgehende Linien (Sport-Indizes): Nordisch-Gruppe, Cross-Gruppe, Park&Pipe-Gruppe
# 0 ski-alpin,1 langlauf,2 biathlon,3 skispringen,4 nord.komb,5 skicross,
# 6 freeski-pp,7 sb-alpin,8 sb-cross,9 sb-pp
CONS_LINKS = [(1,2),(2,3),(3,4),(5,8),(8,7),(6,9)]

# --- Newsbox -----------------------------------------------------------------
# Neue Meldung? Einfach oben in diese Liste einen Block einfuegen (neueste zuerst).
#   "title"   : Ueberschrift
#   "body"    : Liste von Absaetzen (Text)
#   "bullets" : optionale Liste von Aufzaehlungspunkten
#   "url"     : Link -> wird als "Link"-Button gezeigt (leer lassen = kein Button)
NEWS = [
    {
        "title": "Neue Ausbildungsstruktur Ski Alpin",
        "body": ["Die Übersichtsseite zur neuen Ausbildungsstruktur ist live!",
                 "Entdecke den Ausbildungsweg bis hin zum «Swiss-Ski Trainer:in Spitzensport»."],
        "bullets": [],
        "url": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/ski-alpin-ab-2027/",
    },
    {
        "title": "Swiss-Ski Ausbildungsnews Juli 26",
        "body": ["Verschiedene News in folgenden Bereichen:"],
        "bullets": ["Gut zu wissen",
                    "Kurse: Ski Alpin | Langlauf | Biathlon | Ski Freestyle / Snowboard | Skispringen | Tourenwesen"],
        "url": "https://www.swiss-ski.ch/globale-datensammlung/mailings-neu/ausbildungsnews/saison-2026-2027/ausbildungsnews-juli-2026/",
    },
]

def news_html(lang):
    if not NEWS:
        return ""
    heading = {"de":"News","fr":"Actualités","it":"Notizie"}.get(lang, "News")
    cards = ""
    for it in NEWS:
        body = "".join('<p>'+esc(tr(p, lang))+'</p>' for p in it.get("body", []))
        if it.get("bullets"):
            body += '<ul>'+"".join('<li>'+esc(tr(b, lang))+'</li>' for b in it["bullets"])+'</ul>'
        link = ('<a class="news-link" href="'+esc(it["url"])+'" target="_blank" rel="noopener">Link ↗</a>') if it.get("url") else ''
        cards += ('<article class="news-card"><h3>'+esc(tr(it["title"], lang))+'</h3>'
                  '<div class="news-body">'+body+'</div>'+link+'</article>')
    return ('<section class="news"><h2 class="news-h">'+esc(heading)+'</h2>'
            '<div class="news-grid">'+cards+'</div></section>')

def home_html(datamap, lang):
    n = len(SPORTS)
    nodes = ""
    two_line = {"freeski-park-pipe","snowboard-alpin","snowboard-cross","snowboard-park-pipe","nordische-kombination"}
    for i, s in enumerate(SPORTS):
        name = tr(s["name"], lang)
        label = esc(name).replace(" ", "<br>", 1) if s["id"] in two_line else esc(name)
        x, y = CONS_POS[i % len(CONS_POS)]
        icon = s.get("icon")
        ticon = None
        if icon:
            cand = "assets/sporticons/" + os.path.splitext(os.path.basename(icon))[0] + ".png"
            if os.path.exists(cand):
                ticon = cand
        img_tag = ('<img class="nicon" src="'+esc(ticon)+'" alt="" width="200" height="200" loading="lazy" decoding="async">') if ticon else ''
        hover = '<span class="nhover">'+img_tag+'<span class="nname">'+label+'</span></span>'
        # "Gipfel"-Punkt (hoeher als beide Nachbarn) -> Text/Popup oben, sonst unten
        neigh = ([CONS_POS[i-1][1]] if i > 0 else []) + ([CONS_POS[i+1][1]] if i+1 < n else [])
        up = bool(neigh) and y < min(neigh)
        # Klick-Popup: Wahl zwischen Athlet:innen-Weg (intern) und Mission Swiss-Ski (FTEM-Tool)
        mission = s.get("mission")
        pop = ('<span class="npop">'
               '<a href="#'+s["id"]+'">'+esc(tr("Athlet:innen-Weg", lang))+'</a>'
               + (('<a class="np-mission" href="'+esc(mission)+'" data-title="'+esc(name)+' – Mission Swiss-Ski">Mission Swiss-Ski</a>') if mission else '')
               + '</span>')
        edge = ' edge-l' if x <= 24 else (' edge-r' if x >= 76 else '')
        nodes += ('<div class="node'+(' up' if up else '')+edge+'" tabindex="0" role="button" '
                  'aria-haspopup="true" data-sport="'+s["id"]+'" '
                  'style="left:'+str(x)+'%;top:'+str(y)+'%;--d:'+str(i*150)+'ms">'
                  + hover +
                  '<span class="dot"></span>'
                  '<span class="nlabel">'+label+'</span>'+pop+'</div>')
    chain = " ".join(str(CONS_POS[i][0])+","+str(CONS_POS[i][1]) for i in range(min(n, len(CONS_POS))))
    lines = ('<svg class="clines" viewBox="0 0 100 100" preserveAspectRatio="none">'
             '<polyline class="cl" points="'+chain+'" vector-effect="non-scaling-stroke"/>')
    for a, b in CONS_LINKS:
        if a < n and b < n:
            lines += ('<line class="cl2" x1="'+str(CONS_POS[a][0])+'" y1="'+str(CONS_POS[a][1])+
                      '" x2="'+str(CONS_POS[b][0])+'" y2="'+str(CONS_POS[b][1])+'" vector-effect="non-scaling-stroke"/>')
    lines += '</svg>'
    info = FTEM_INFO[lang]
    phase_cls = {"F":"p-f","T":"p-t","E":"p-e","M":"p-m"}
    phases = "".join('<div class="phase '+phase_cls[k]+'"><span class="pl">'+k+'</span>'
                     '<span class="pn">'+pn+'</span><span class="pr">'+pr+'</span>'
                     '<p>'+desc+'</p></div>' for k,pn,pr,desc in info["phases"])
    ftem_info = ('<div class="ftem-info">'
                 '<h2>'+info["title"]+'</h2>'
                 '<p class="lead">'+info["lead"]+'</p>'
                 '<div class="phases">'+phases+'</div></div>')
    fb_ph = {"de":"Dein Feedback …","fr":"Votre commentaire …","it":"Il tuo feedback …"}.get(lang, "Dein Feedback …")
    fb_send = {"de":"Senden","fr":"Envoyer","it":"Invia"}.get(lang, "Senden")
    fb = ('<button class="fb-btn" type="button" '
          'onclick="var p=this.nextElementSibling;p.hidden=!p.hidden;if(!p.hidden)p.querySelector(&#39;textarea&#39;).focus()">Feedback</button>'
          '<div class="fb-panel" hidden>'
          '<textarea class="fb-text" placeholder="'+esc(fb_ph)+'"></textarea>'
          '<button class="fb-send" type="button" '
          'onclick="location.href=&#39;mailto:forschung@swiss-ski.ch?subject=Feedback%20FTEM&amp;body=&#39;+encodeURIComponent(this.parentNode.querySelector(&#39;.fb-text&#39;).value)">'+esc(fb_send)+'</button>'
          '</div>')
    return ('<section id="home">'
            '<div class="home-hero">'
            '<div class="hero-top">'+lang_switch(lang)+fb+'</div>'
            '<div class="hero-head"><h1>'+FTEM+'</h1>'
            '<img class="hero-logo" src="assets/swiss-ski-logo.svg" alt="Swiss-Ski"></div>'
            '<div class="constellation">'+lines+nodes+'</div>'
            '<button class="scrolldown" type="button" aria-label="nach unten scrollen" '
            'onclick="document.querySelector(&#39;.home-info&#39;).scrollIntoView({behavior:&#39;smooth&#39;})">&#9662;</button>'
            '</div>'
            '<div class="home-info">'+news_html(lang)+ftem_info
            +'<div class="adminlink"><a href="admin.html" title="Admin-Login" aria-label="Admin-Login">&#128274;</a></div></div>'
            '</section>')


CSS = r"""
:root{--red:#d52b1e;--ink:#1d2630;--mut:#697080;--line:#e4e8ec;--bg:#eef1f4;--card:#fff;
--found:#1f8fa6;--found-t:#0d5e6e;--found-bg:#ecf6f8;
--talent:#e2a900;--talent-t:#8a6a00;--talent-bg:#fdf7e4;
--elite:#e8772e;--elite-t:#a8511a;--elite-bg:#fdefe5;
--mast:#d52b1e;--mast-t:#9c1d14;--mast-bg:#fce9e7;
--acc:#4a5563;--acc-line:#c6ced6;--acc-bg:#eef1f4;--acc-bg2:#e2e6ea;
--colw:200px;--lblw:146px;--top:54px}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:var(--bg);scrollbar-gutter:stable}
html.h #home{display:none}
html.noanim .grid-sports .card{animation:none}
[hidden]{display:none!important}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45;font-size:13px;-webkit-text-size-adjust:100%}
.langsw{display:flex;gap:2px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:2px}
.langsw a{font-size:11.5px;font-weight:800;color:var(--mut);text-decoration:none;padding:4px 9px;border-radius:6px;letter-spacing:.03em}
.langsw a.active{background:var(--red);color:#fff}
.langsw a:hover:not(.active){background:#fff;color:var(--ink)}
/* Startseite - Neon-Konstellation */
#home .home-hero{position:relative;min-height:100vh;overflow:hidden;color:#fff;display:flex;flex-direction:column;
  background:linear-gradient(180deg,rgba(9,14,24,.66),rgba(12,17,28,.5) 45%,rgba(7,11,20,.9)),url("assets/hero.jpg") center 32%/cover no-repeat}
#home .hero-top{position:absolute;top:16px;left:18px;z-index:7;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.fb-btn{background:var(--red);color:#fff;border:none;border-radius:8px;padding:6px 15px;font-size:11.5px;font-weight:800;letter-spacing:.04em;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.3);transition:filter .15s}
.fb-btn:hover{filter:brightness(1.12)}
.fb-panel{display:flex;flex-direction:column;gap:8px;width:250px;background:rgba(15,21,32,.93);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.18);border-radius:11px;padding:11px;box-shadow:0 16px 40px rgba(0,0,0,.5)}
.fb-text{width:100%;min-height:84px;resize:vertical;border-radius:7px;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.08);color:#fff;padding:8px;font:inherit;font-size:12.5px;line-height:1.4}
.fb-text::placeholder{color:rgba(255,255,255,.55)}
.fb-text:focus{outline:none;border-color:var(--red)}
.fb-send{align-self:flex-end;background:var(--red);color:#fff;border:none;border-radius:7px;padding:7px 16px;font-weight:800;font-size:12px;cursor:pointer;transition:filter .15s}
.fb-send:hover{filter:brightness(1.12)}
#home .home-hero .langsw{background:rgba(255,255,255,.13);border-color:rgba(255,255,255,.22);backdrop-filter:blur(6px)}
#home .home-hero .langsw a{color:rgba(255,255,255,.82)}
#home .home-hero .langsw a.active{background:var(--red);color:#fff}
#home .home-hero .langsw a:hover:not(.active){background:rgba(255,255,255,.22);color:#fff}
#home .hero-head{position:relative;z-index:6;text-align:center;padding:74px 20px 0;pointer-events:none}
#home .hero-head h1{font-size:clamp(46px,9vw,92px);margin:0;font-weight:800;letter-spacing:1px;text-shadow:0 3px 26px rgba(0,0,0,.6)}
#home .hero-head h1 b{color:#fff;font-weight:800}
#home .hero-head h1 .fF,#home .hero-head h1 .fT,#home .hero-head h1 .fE,#home .hero-head h1 .fM{animation:ftemglow 3.2s ease-in-out infinite}
#home .hero-head h1 .fF{color:#57cce4;text-shadow:0 0 12px rgba(87,204,228,.9),0 0 26px rgba(87,204,228,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fT{color:#ffd45c;text-shadow:0 0 12px rgba(255,212,92,.9),0 0 26px rgba(255,212,92,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fE{color:#ff9b57;text-shadow:0 0 12px rgba(255,155,87,.9),0 0 26px rgba(255,155,87,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fM{color:#ff6d60;text-shadow:0 0 12px rgba(255,109,96,.95),0 0 26px rgba(255,109,96,.65),0 2px 24px rgba(0,0,0,.5)}
@keyframes ftemglow{0%,100%{filter:brightness(1)}50%{filter:brightness(1.28)}}
#home .hero-logo{display:block;margin:6px auto 0;width:clamp(96px,14vw,150px);height:auto;filter:drop-shadow(0 4px 18px rgba(0,0,0,.5))}
.constellation{position:absolute;inset:0;z-index:3;will-change:transform;transition:transform .3s ease-out}
.clines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.clines .cl{fill:none;stroke:rgba(255,255,255,.30);stroke-width:1.3;stroke-linecap:round;stroke-dasharray:5 9;animation:flow 24s linear infinite}
.clines .cl2{stroke:rgba(255,255,255,.55);stroke-width:1.4;stroke-linecap:round}
@keyframes flow{to{stroke-dashoffset:-160}}
.node{position:absolute;transform:translate(-50%,-50%);text-decoration:none;padding:12px;line-height:0;
  animation:nodeIn .6s ease both;animation-delay:var(--d,0ms)}
@keyframes nodeIn{from{opacity:0;transform:translate(-50%,-50%) scale(.3)}to{opacity:1;transform:translate(-50%,-50%) scale(1)}}
.node .dot{display:block;width:13px;height:13px;border-radius:50%;position:relative;transition:transform .22s ease;
  background:conic-gradient(from 0deg,#57cce4,#ffd45c,#ff9b57,#ff6d60,#57cce4);
  box-shadow:0 0 0 1.5px rgba(255,255,255,.7),0 0 11px 3px rgba(255,255,255,.4),0 0 24px 8px rgba(255,150,80,.42);
  animation:spin 7s linear infinite}
.node .dot::after{content:"";position:absolute;inset:-4px;border-radius:50%;animation:twk 3.2s ease-in-out infinite;pointer-events:none}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes twk{0%,100%{box-shadow:0 0 6px 1px rgba(255,255,255,.22);opacity:.7}50%{box-shadow:0 0 16px 5px rgba(255,190,120,.5);opacity:1}}
.node{cursor:pointer}
.node:hover,.node:focus-visible{z-index:9;outline:none}
/* Klick-Popup: Athlet:innen-Weg oder Mission Swiss-Ski */
.npop{position:absolute;top:calc(100% + 6px);left:50%;transform:translate(-50%,8px);display:flex;flex-direction:column;gap:6px;width:176px;background:rgba(15,21,32,.95);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.25);border-radius:12px;padding:10px;opacity:0;pointer-events:none;transition:opacity .18s,transform .18s;z-index:14}
.node.up .npop{top:auto;bottom:calc(100% + 6px);transform:translate(-50%,-8px)}
.node.open{z-index:13}
.node.open .npop{opacity:1;pointer-events:auto;transform:translate(-50%,0)}
.node.edge-l .npop{left:0;right:auto;transform:translateY(8px)}
.node.edge-l.up .npop{transform:translateY(-8px)}
.node.edge-l.open .npop{transform:translateY(0)}
.node.edge-r .npop{left:auto;right:0;transform:translateY(8px)}
.node.edge-r.up .npop{transform:translateY(-8px)}
.node.edge-r.open .npop{transform:translateY(0)}
.node.open .nhover,.node.open .nlabel{opacity:0!important}
.npop a{display:block;text-align:center;background:rgba(255,255,255,.10);color:#fff;text-decoration:none;font-size:12.5px;font-weight:700;border:1px solid rgba(255,255,255,.22);border-radius:8px;padding:8px 10px;line-height:1.25}
.npop a:hover{background:var(--red);border-color:var(--red)}
/* Mission-Iframe-Overlay */
.mmodal{position:fixed;inset:0;z-index:120;background:rgba(8,12,20,.68);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:18px}
.mm-box{width:min(1240px,96vw);height:min(880px,92vh);background:#fff;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.mm-bar{display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--ink);color:#fff}
.mm-t{font-weight:800;font-size:13px;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.mm-ext{color:#fff;text-decoration:none;font-weight:700;font-size:12px;padding:4px 10px;border:1px solid rgba(255,255,255,.4);border-radius:16px;white-space:nowrap}
.mm-ext:hover{background:rgba(255,255,255,.15)}
.mm-x{background:none;border:none;color:#fff;font-size:17px;cursor:pointer;padding:2px 8px;line-height:1}
.mm-x:hover{color:var(--talent)}
.mm-frame{flex:1;border:0;width:100%;background:#fff}
@media(max-width:700px){.mmodal{padding:0}.mm-box{width:100vw;height:100vh;border-radius:0}}
.node:hover .dot,.node:focus-visible .dot{transform:scale(1.45)}
.node .nlabel{position:absolute;top:calc(100% + 5px);left:50%;transform:translateX(-50%);
  font-size:13.5px;font-weight:700;color:#fff;text-align:center;line-height:1.25;letter-spacing:.02em;
  text-shadow:0 1px 8px rgba(0,0,0,.92),0 0 4px rgba(0,0,0,.7);pointer-events:none;transition:opacity .18s}
.node.up .nlabel{top:auto;bottom:calc(100% + 5px)}
.node:hover .nlabel,.node:focus-visible .nlabel{opacity:0}
.node .nhover{position:absolute;top:calc(100% - 2px);left:50%;transform:translate(-50%,-8px);
  display:flex;flex-direction:column;align-items:center;gap:5px;width:124px;
  opacity:0;pointer-events:none;transition:opacity .22s,transform .22s}
.node.up .nhover{top:auto;bottom:calc(100% - 2px);transform:translate(-50%,8px)}
.node:hover .nhover,.node:focus-visible .nhover{opacity:1;transform:translate(-50%,0)}
.node .nicon{width:74px;height:74px;object-fit:contain;border-radius:16px;filter:drop-shadow(0 3px 12px rgba(0,0,0,.55))}
.node .nhover .nname{font-size:12.5px;font-weight:800;color:#fff;text-align:center;line-height:1.2;text-shadow:0 1px 8px rgba(0,0,0,.92)}
.scrolldown{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);z-index:8;color:rgba(255,255,255,.85);font-size:24px;line-height:1;background:none;border:none;cursor:pointer;padding:6px 14px;animation:bob 1.8s ease-in-out infinite}
.scrolldown:hover{color:#fff}
@keyframes bob{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(6px)}}
@media(prefers-reduced-motion:reduce){
*,*::before,*::after{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}
.node .dot{animation:none!important}.node .dot::after{animation:none!important}.clines .cl,.clines .cl2{animation:none!important}.scrolldown{animation:none!important}
}
.home-info{max-width:980px;margin:0 auto;padding:42px 24px 30px}
.ctext{display:contents}
.adminlink{text-align:center;margin-top:30px}
.adminlink a{opacity:.32;font-size:17px;text-decoration:none;transition:opacity .15s;filter:grayscale(1)}
.adminlink a:hover{opacity:.85}
/* Newsbox */
.news{margin:0 0 8px}
.news-h{margin:0 0 12px;font-size:17px;font-weight:800;color:var(--ink)}
.news-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.news-card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--red);border-radius:14px;padding:15px 17px;display:flex;flex-direction:column;transition:box-shadow .16s,transform .16s}
.news-card:hover{box-shadow:0 8px 20px rgba(0,0,0,.07);transform:translateY(-2px)}
.news-card h3{margin:0 0 8px;font-size:14.5px;font-weight:800;color:var(--ink);line-height:1.3}
.news-body{color:var(--mut);font-size:13px;line-height:1.55}
.news-body p{margin:0 0 8px}
.news-body ul{margin:6px 0 8px;padding-left:18px}
.news-body li{margin:2px 0}
.news-link{align-self:flex-start;margin-top:auto;background:var(--red);color:#fff;text-decoration:none;font-weight:800;font-size:12px;border-radius:20px;padding:6px 15px;transition:filter .15s}
.news-link:hover{filter:brightness(1.12)}
@media(max-width:640px){.node .nicon{width:58px;height:58px}.node .nhover{width:96px}.node .nlabel{font-size:12px}#home .hero-head{padding-top:56px}}
@media(max-width:480px){.node{padding:9px}.node .nlabel{font-size:10.5px;max-width:70px}.node .nhover{width:84px}.node .nicon{width:48px;height:48px}.node .dot{width:11px;height:11px}}
@media(max-width:350px){.node .nlabel{font-size:9.5px;max-width:60px}.node .dot{width:10px;height:10px}}
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
header.top{position:sticky;top:0;z-index:60;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:10px 18px;display:flex;flex-wrap:nowrap;gap:10px 14px;align-items:center;height:var(--top)}
header.top .back{flex:none;width:118px;text-align:center;font-size:12.5px;font-weight:700;color:var(--ink);text-decoration:none;background:var(--bg);border:1px solid var(--line);border-radius:20px;padding:6px 0;white-space:nowrap}
header.top .back:hover{background:#fff;border-color:var(--acc);color:var(--acc)}
header.top .sicon{width:34px;height:34px;border-radius:50%;object-fit:cover;flex:none}
header.top h1{font-size:16px;margin:0;font-weight:800;color:var(--ink);white-space:nowrap;letter-spacing:.2px;flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis}
header.top h1 b{color:var(--ink);font-weight:700}
h1 .fF{color:var(--found)}h1 .fT{color:var(--talent)}h1 .fE{color:var(--elite)}h1 .fM{color:var(--mast)}
h1 .fF,h1 .fT,h1 .fE,h1 .fM{font-weight:900}
h1 .sk{color:var(--ink)}
.ht-l{flex:1 1 0;min-width:0;display:flex;align-items:center;gap:10px}
.ht-c{flex:0 0 auto;position:relative;display:flex;align-items:center}
.ht-r{flex:1 1 0;display:flex;align-items:center;gap:8px;justify-content:flex-end}
header.top input,header.top select,header.top button{font:inherit;font-size:13px;padding:7px 11px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
header.top button{cursor:pointer;font-weight:600}
header.top button:hover{background:var(--bg)}
.ht-c input{width:280px;padding-right:96px}
.ht-c .hits{position:absolute;right:32px;top:50%;transform:translateY(-50%);font-size:11.5px;color:var(--mut);font-weight:700;white-space:nowrap;max-width:78px;overflow:hidden;text-overflow:ellipsis;pointer-events:none}
.ht-r select{width:170px}
.ht-r .exp{width:106px;padding:7px 0;text-align:center}
.ht-r .col{width:120px;padding:7px 0;text-align:center}
.ht-r .pdf{width:36px;padding:6px 0;display:inline-flex;align-items:center;justify-content:center;color:var(--acc)}
.ht-r .pdf svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ht-r .pdf:hover{border-color:var(--acc);color:var(--red)}
@media print{
  @page{size:A4 landscape;margin:9mm}
  :root{--colw:84px;--lblw:80px}
  html,body{background:#fff}
  #home,header.top,footer,.scrolldown,.adminlink,.news,.more,.hits,.fb-btn,.fb-panel{display:none!important}
  section.sport{display:block!important}
  section.sport[hidden]{display:none!important}
  .wrap{padding:0;max-width:none}
  h2.grp{margin:12px 0 6px;break-after:avoid}
  details.theme{break-inside:avoid;box-shadow:none!important;border:1px solid #bbb;margin-bottom:8px;transform:none!important}
  details.theme .scroller{overflow:visible!important;padding:0}
  .grid{min-width:0;gap:4px}
  .r{gap:3px;break-inside:avoid}
  .rl{position:static!important;box-shadow:none!important;font-size:8.5px;padding:5px 6px}
  .c.hd .st{font-size:9px}.c.hd .stf{display:none}
  .cell{break-inside:avoid;overflow:visible!important}
  .cell .cwrap{max-height:none!important;-webkit-line-clamp:unset!important;display:block!important;font-size:8.5px;line-height:1.35}
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
mark.cur{background:#f0a500;color:#1d2630;box-shadow:0 0 0 2px #f0a500}
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
h2.grp{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gc,var(--mut));margin:24px 0 10px;font-weight:800;display:flex;align-items:center;gap:8px}
h2.grp::before{content:'';width:9px;height:9px;border-radius:2px;background:var(--gc,var(--mut));flex:none}
h2.grp::after{content:'';flex:1;height:1px;background:var(--line)}
details.theme{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--acc-line);border-radius:9px;margin-bottom:8px;scroll-margin-top:66px;overflow:hidden;transition:box-shadow .16s}
details.theme:hover{box-shadow:0 5px 16px rgba(0,0,0,.08)}
details.theme[open]{box-shadow:0 6px 18px rgba(0,0,0,.06)}
details.theme>summary{cursor:pointer;padding:9px 14px;list-style:none;display:flex;align-items:center;gap:10px}
details.theme>summary:hover{background:#fafbfc}
details.theme>summary::-webkit-details-marker{display:none}
summary .ticon{flex:none;width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center}
summary .ticon svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
summary .tt{font-size:14px;font-weight:800;flex:1;min-width:0}
summary .tchev{flex:none;width:8px;height:8px;border-right:2px solid var(--mut);border-bottom:2px solid var(--mut);transform:rotate(-45deg);transition:transform .18s;margin-right:3px}
details[open]>summary .tchev{transform:rotate(45deg)}
.scroller{overflow-x:auto;overflow-y:hidden;padding:0 12px 13px;-webkit-overflow-scrolling:touch;overscroll-behavior-x:contain}
.grid{min-width:max-content;display:flex;flex-direction:column;gap:6px}
.r{display:grid;grid-template-columns:var(--lblw) repeat(10,var(--colw));gap:6px;align-items:start}
.rl{position:sticky;left:0;z-index:5;align-self:stretch;background:var(--card);font-weight:700;font-size:11.5px;color:var(--ink);display:flex;align-items:flex-start;padding:9px 10px;border-radius:8px;border:1px solid var(--line);box-shadow:0 0 0 7px var(--card),-14px 0 0 7px var(--card),9px 0 9px -6px rgba(0,0,0,.2);min-width:0;overflow:hidden;overflow-wrap:anywhere;word-break:break-word;hyphens:auto}
.rl.nolbl{background:var(--card);border:1px dashed #e9ecef}
.r.head{position:relative;z-index:2}
.r.head .rl.corner{position:sticky;left:0;z-index:6;background:var(--card);border:none}
.c.hd{border-radius:8px;padding:6px 6px;text-align:center;display:flex;flex-direction:column;gap:0;justify-content:center}
.c.hd .st{font-size:13.5px;font-weight:800}
.c.hd .stf{font-size:9px;font-weight:600;opacity:.92}
.c.hd[data-idx]{cursor:pointer;transition:box-shadow .12s}
.c.hd[data-idx]:hover{box-shadow:inset 0 0 0 2px rgba(255,255,255,.7)}
.c.hd.active{box-shadow:inset 0 0 0 3px rgba(0,0,0,.45)}
/* dezente Phasen-Toenung je Spalte - Orientierung F1-M beim Scrollen */
.cell.ph-foundation{background:#f4faf8}.cell.ph-talent{background:#fcf8ee}.cell.ph-elite{background:#fdf5ef}.cell.ph-mastery{background:#fcefef}.cell.ph-multi{background:#f7f8fa}
.cell.hl-foundation{background:var(--found-bg)}
.cell.hl-talent{background:var(--talent-bg)}
.cell.hl-elite{background:var(--elite-bg)}
.cell.hl-mastery{background:var(--mast-bg)}
/* Phasenfarben NUR fuer die Stufen-Koepfe - Inhaltszellen behalten dunkle Schrift */
.c.hd.ph-foundation{background:var(--found);color:#fff}.c.hd.ph-talent{background:var(--talent);color:#3b2e00}.c.hd.ph-elite{background:var(--elite);color:#fff}.c.hd.ph-mastery{background:var(--mast);color:#fff}
.cell{color:var(--ink)}
.cell{background:#fff;border:1px solid var(--line);border-radius:8px;position:relative;overflow:hidden;align-self:start}
.cell .cwrap{padding:9px 11px;font-size:11.5px;line-height:1.5;color:#33404d;max-height:212px;overflow:hidden;transition:max-height .25s ease}
.cell.clamped .cwrap,.cell.expanded .cwrap{padding-bottom:34px}
.cell.expanded .cwrap{max-height:4000px}
.cell::after{content:'';position:absolute;left:0;right:0;bottom:0;height:32px;background:linear-gradient(180deg,transparent,#fff);pointer-events:none;opacity:0;transition:opacity .2s}
.cell.clamped::after{opacity:1}
.cell.expanded::after{opacity:0}
.cell.ph-foundation{border-top:3px solid var(--found)}.cell.ph-talent{border-top:3px solid var(--talent)}.cell.ph-elite{border-top:3px solid var(--elite)}.cell.ph-mastery{border-top:3px solid var(--mast)}.cell.ph-multi{border-top:3px solid #b6c0cc}
.cwrap p{margin:0 0 5px;line-height:1.5}.cwrap p:last-child{margin-bottom:0}
.cwrap .bh,.cwrap .sh{font-weight:700;color:var(--found-t);font-size:9px;text-transform:uppercase;letter-spacing:.055em;margin:12px 0 4px;line-height:1.3}
.cwrap .bh:first-child,.cwrap .sh:first-child{margin-top:0}
.cwrap .bh:not(:first-child),.cwrap .sh:not(:first-child){border-top:1px solid #edf0f3;padding-top:10px}
.cwrap .bi{font-weight:700;color:var(--ink);font-size:11.5px;margin:0 0 3px;line-height:1.4}
.cwrap .lbl{font-weight:700;color:var(--found-t)}
.cwrap ul{margin:3px 0 6px;padding-left:15px}
.cwrap ul.bl li{margin-bottom:3px;line-height:1.45}
.cwrap ul.sc{list-style:none;padding-left:0}
.cwrap ul.sc li{margin-bottom:5px;padding-left:0;line-height:1.45}
.cwrap ul.sc .badge{display:inline-block;background:var(--ink);color:#fff;font-size:9.5px;font-weight:700;border-radius:4px;padding:1px 5px;margin-right:4px}
.cwrap .empty{color:#c2c8d0;text-align:center;font-size:14px}
.lks{margin-top:7px;display:flex;flex-direction:column;gap:4px}
.lks a{font-size:11px;color:#39424e;text-decoration:none;font-weight:700;background:var(--acc-bg);padding:5px 8px;border-radius:6px;display:flex;align-items:center;gap:5px}
.lks a::before{content:'📄'}
.lks a:hover{background:var(--acc-bg2)}
.more{position:absolute;bottom:6px;right:8px;z-index:3;font:inherit;font-size:10.5px;font-weight:700;color:var(--acc);background:#fff;border:1px solid var(--line);border-radius:20px;padding:2px 9px;cursor:pointer;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.more:hover{background:var(--acc-bg)}
mark{background:#ffe08a;border-radius:2px;padding:0 1px}
.hidden{display:none!important}
footer{text-align:center;color:var(--mut);font-size:12px;padding:24px}
footer a{color:var(--red)}
/* ---------- Responsive: Tablet ---------- */
@media(max-width:1180px){
header.top{flex-wrap:wrap;height:auto;padding:8px 14px;gap:8px 10px}
.ht-l{flex:1 1 100%}
.ht-c{flex:1 1 auto;order:3}
.ht-c input{width:100%;min-width:160px}
.ht-r{flex:1 1 auto;order:2;flex-wrap:wrap}
details.theme{scroll-margin-top:118px}
}
/* ---------- Responsive: Handy ---------- */
@media(max-width:760px){
:root{--colw:158px;--lblw:86px}
header.top .back{width:auto;padding:6px 11px}
header.top .sicon{width:28px;height:28px}
header.top h1{font-size:13.5px;min-width:0}
.ht-c{flex:1 1 100%;order:2}
.ht-c input{font-size:16px;padding:6px 96px 6px 10px}
.ht-r{flex:1 1 100%;order:3;gap:6px}
.ht-r select{flex:1 1 auto;width:auto;min-width:0;font-size:13px}
.ht-r .exp,.ht-r .col{flex:1 1 auto;width:auto;padding:7px 6px}
.ht-r .pdf{flex:none;width:40px}
.wrap{padding:10px 10px 60px}
.scroller{padding:0 8px 10px}
.rl{font-size:9.5px;padding:6px 6px;line-height:1.25;font-weight:600}
.rl{box-shadow:0 0 0 6px var(--card),-12px 0 0 6px var(--card),7px 0 8px -5px rgba(0,0,0,.22)}
.cell .cwrap{font-size:11px}
summary .tt{font-size:13px}
details.theme{scroll-margin-top:170px}
.home-info{padding:28px 14px 20px}
.ftem-info{padding:18px 14px 14px}
.phases{grid-template-columns:1fr}
footer{padding:16px;font-size:11px}
}
/* ---------- Responsive: sehr grosse Screens ---------- */
@media(min-width:1800px){
.wrap{max-width:1720px}
}
"""

JS = r"""
const SPORT_IDS = __SPORT_IDS__;
const I18N = __I18N__;
const sections = [...document.querySelectorAll('section.sport')];
const home = document.getElementById('home');

// ---- Live-Overrides aus dem Admin-Bereich (Supabase) ----
const SUPA_URL="__SUPA_URL__", SUPA_KEY="__SUPA_KEY__";
function _esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
const SC_RE=/^(SC\s?\d+[a-z]?|SC|ST\s?\d*|ST)\s*[:.\)]\s*([\s\S]*)$/;
function structBlock(b){
  b=b.replace(/\s+$/,'');
  if(!b.trim())return '';
  const lines=b.split('\n');
  const nonempty=lines.map(l=>l.trim()).filter(Boolean);
  if(lines.some(l=>l.trim().startsWith('•'))){
    const intro=[],items=[];
    lines.forEach(l=>{const ls=l.trim();if(ls.startsWith('•'))items.push(ls.replace(/^•+/,'').trim());else if(ls){items.length?items.push(ls):intro.push(ls);}});
    let out='';if(intro.length)out+='<p class="bh">'+_esc(intro[0])+'</p>';
    out+='<ul class="bl">'+items.filter(Boolean).map(i=>'<li>'+_esc(i)+'</li>').join('')+'</ul>';return out;
  }
  const scHits=nonempty.filter(l=>SC_RE.test(l));
  if(nonempty.length>=1&&scHits.length>=1&&scHits.length>=Math.max(1,nonempty.length-1)){
    let out='<ul class="sc">';
    nonempty.forEach(ls=>{const m=ls.match(SC_RE);if(m)out+='<li><span class="badge">'+_esc(m[1].trim())+'</span> '+_esc(m[2].trim())+'</li>';else out+='<li>'+_esc(ls)+'</li>';});
    return out+'</ul>';
  }
  if(lines.length>=2&&lines[0].trim()&&lines[0].trim().length<=46&&!/[.:,;]$/.test(lines[0].trim())){
    return '<p class="bh">'+_esc(lines[0].trim())+'</p><p>'+_esc(lines.slice(1).join('\n').trim()).replace(/\n/g,'<br>')+'</p>';
  }
  const m=b.match(/^([^:\n]{2,46}):\s*([\s\S]+)$/);
  if(m&&m[1].indexOf('\n')<0){
    const lab=m[1].trim(),val=m[2].trim();
    if(val.length>55||val.indexOf('\n')>=0)return '<p class="sh">'+_esc(lab)+'</p><p>'+_esc(val).replace(/\n/g,'<br>')+'</p>';
    return '<p><span class="lbl">'+_esc(lab)+':</span> '+_esc(val).replace(/\n/g,'<br>')+'</p>';
  }
  return '<p>'+_esc(b).replace(/\n/g,'<br>')+'</p>';
}
function structCell(txt){
  txt=(txt||'').trim();
  if(!txt)return '<div class="empty">–</div>';
  return txt.split(/\n\s*\n/).map(structBlock).filter(Boolean).join('')||'<div class="empty">–</div>';
}
function loadOverrides(){
  if(!SUPA_URL||!SUPA_KEY)return Promise.resolve({});
  return fetch(SUPA_URL+'/rest/v1/ftem_overrides?select=cid,txt',{headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY}})
    .then(r=>r.ok?r.json():[]).then(rows=>{const m={};(rows||[]).forEach(x=>m[x.cid]=x.txt);return m;}).catch(()=>({}));
}
function applyOverrides(map){
  document.querySelectorAll('.ctext[data-cid]').forEach(el=>{
    const v=map[el.dataset.cid];
    if(v!=null){el.innerHTML=structCell(v);}
  });
}

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
  const hitEl = sec.querySelector('.hits');
  let marks = [], cur = -1;
  function updateHits(){
    if(!hitEl) return;
    const term = q.value.trim();
    if(!term){ hitEl.textContent=''; return; }
    if(!marks.length){ hitEl.textContent = I18N.noHits; return; }
    hitEl.textContent = (cur>=0 ? (cur+1)+'/' : '') + marks.length + ' ' + I18N.hitsWord;
  }
  function gotoMark(i){
    if(!marks.length) return;
    cur = ((i % marks.length) + marks.length) % marks.length;
    marks.forEach(x=>x.classList.remove('cur'));
    const m = marks[cur];
    m.classList.add('cur');
    const det = m.closest('details'); if(det && !det.open) det.open = true;
    const cell = m.closest('.cell');
    if(cell && cell.classList.contains('clamped') && !cell.classList.contains('expanded')){
      cell.classList.add('expanded');
      const btn = cell.querySelector('.more'); if(btn) btn.textContent = I18N.less;
    }
    m.scrollIntoView({block:'center', inline:'center', behavior:'smooth'});
    updateHits();
  }
  q.addEventListener('keydown', e=>{
    if(e.key==='Enter'){ e.preventDefault(); gotoMark(cur + (e.shiftKey ? -1 : 1)); }
  });
  function clearMarks(el){el.querySelectorAll('mark').forEach(m=>m.replaceWith(document.createTextNode(m.textContent)));el.normalize();}
  function run(){
    const term=q.value.trim().toLowerCase();
    themes.forEach(clearMarks);
    let vis=0;
    themes.forEach(t=>{
      if(!term){t.classList.remove('hidden');return;}
      const hit=t.textContent.toLowerCase().includes(term);
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
    marks = [...sec.querySelectorAll('mark')];
    cur = -1;
    updateHits();
  }
  q.addEventListener('input',run);
  sec.querySelector('.exp').onclick=()=>{themes.forEach(t=>t.open=true);setTimeout(setupClamp,50);};
  sec.querySelector('.col').onclick=()=>themes.forEach(t=>t.open=false);
  const pdfBtn=sec.querySelector('.pdf');
  if(pdfBtn)pdfBtn.onclick=()=>{themes.forEach(t=>t.open=true);setTimeout(()=>window.print(),160);};
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

// ---- Sportarten-Popup auf der Startseite (Athlet:innen-Weg | Mission Swiss-Ski) ----
const heroNodes=[...document.querySelectorAll('.node')];
function closePops(){heroNodes.forEach(n=>n.classList.remove('open'));}
heroNodes.forEach(n=>{
  n.addEventListener('click',e=>{
    if(e.target.closest('.npop'))return;      // Klicks auf die Popup-Links normal durchlassen
    e.stopPropagation();
    const was=n.classList.contains('open');
    closePops();
    if(!was)n.classList.add('open');
  });
  n.addEventListener('keydown',e=>{
    if(e.key==='Enter'||e.key===' '){e.preventDefault();const was=n.classList.contains('open');closePops();if(!was)n.classList.add('open');}
  });
});
document.addEventListener('click',e=>{if(!e.target.closest('.node'))closePops();});

// ---- Mission Swiss-Ski im Iframe-Overlay ----
const mm=document.querySelector('.mmodal');
function openMission(url,title){
  mm.querySelector('.mm-t').textContent=title;
  mm.querySelector('.mm-ext').href=url;
  mm.querySelector('.mm-frame').src=url;
  mm.hidden=false;document.body.style.overflow='hidden';
}
function closeMission(){mm.hidden=true;mm.querySelector('.mm-frame').src='about:blank';document.body.style.overflow='';}
mm.addEventListener('click',e=>{if(e.target===mm)closeMission();});
mm.querySelector('.mm-x').addEventListener('click',closeMission);
document.querySelectorAll('.np-mission').forEach(a=>a.addEventListener('click',e=>{
  e.preventDefault();e.stopPropagation();closePops();
  openMission(a.getAttribute('href'), a.dataset.title||'Mission Swiss-Ski');
}));
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){ if(!mm.hidden)closeMission(); else closePops(); }
});

// ---- Umschalten Startseite <-> Sportart (per #hash, Zurueck-Taste funktioniert) ----
function show(id){
  closePops();
  home.hidden = !!id;
  sections.forEach(s=>{s.hidden = s.dataset.sport!==id;});
  window.scrollTo(0,0);
  if(id){
    const sec=sections.find(s=>s.dataset.sport===id);
    if(sec&&sec.__clamp)setTimeout(sec.__clamp,60);
  }
}
function route(){
  document.documentElement.classList.remove('h'); // ab jetzt steuert JS die Sichtbarkeit
  const id=decodeURIComponent(location.hash.replace('#',''));
  show(SPORT_IDS.includes(id)?id:'');
}
window.addEventListener('hashchange',route);
route();
loadOverrides().then(map=>{applyOverrides(map);sections.forEach(s=>{if(s.__clamp)s.__clamp();});});
"""

ADMIN_TMPL = r'''<!DOCTYPE html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>FTEM Admin</title>
<style>
__MAINCSS__
/* ---- Admin-Zusatz ---- */
#gate{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:#eef1f4;padding:20px}
.gatebox{background:#fff;border:1px solid #e4e8ec;border-radius:16px;padding:30px 28px;width:340px;max-width:100%;text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.08)}
.gatebox h1{font-size:19px;margin:0 0 6px}
.gatebox p{color:#697080;font-size:13px;margin:0 0 18px}
.gatebox input{width:100%;padding:10px 12px;border:1px solid #cfd6dd;border-radius:9px;font-size:14px}
.gatebox button{margin-top:12px;width:100%;background:#d52b1e;color:#fff;border:none;border-radius:9px;padding:10px;font-weight:800;font-size:14px;cursor:pointer}
.gateerr{color:#d52b1e;font-size:12.5px;margin-top:10px;min-height:16px}
.abar{position:sticky;top:0;z-index:90;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border-bottom:1px solid #e4e8ec;padding:9px 16px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.abar h1{font-size:15px;margin:0;font-weight:800}
.abar label{font-size:12.5px;font-weight:700;display:flex;align-items:center;gap:6px}
.abar select{padding:6px 9px;border:1px solid #cfd6dd;border-radius:8px;font-size:13px;font-weight:700}
.abar .sp{flex:1}
.astatus{font-size:12.5px;color:#697080}
.asave{background:#d52b1e;color:#fff;border:none;border-radius:8px;padding:8px 16px;font-weight:800;font-size:13px;cursor:pointer}
.asave:disabled{opacity:.5;cursor:default}
.agloss{background:#5a6b8f;color:#fff;border:none;border-radius:8px;padding:8px 14px;font-weight:800;font-size:13px;cursor:pointer}
.agloss:hover{filter:brightness(1.08)}
.asite{text-decoration:none;font-size:13px;font-weight:700;color:#d52b1e}
#glosspanel{max-width:900px;margin:0 auto;padding:8px 18px 60px}
.glosbar{display:flex;align-items:center;gap:12px;margin:10px 0 6px}
.glosbar input{flex:1;padding:9px 12px;border:1px solid #cfd6dd;border-radius:9px;font-size:14px}
.glosnote{font-size:12.5px;color:#697080;margin:0 0 10px}
.glosadd{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 12px;background:#fff;border:1px solid #e4e8ec;border-radius:10px;padding:10px 12px}
.glosadd input{padding:8px 10px;border:1px solid #cfd6dd;border-radius:8px;font-size:13px;min-width:150px}
.glosadd button{background:#5a6b8f;color:#fff;border:none;border-radius:8px;padding:8px 14px;font-weight:800;font-size:13px;cursor:pointer}
.glosadd button:hover{filter:brightness(1.08)}
.glostab{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border:1px solid #e4e8ec;border-radius:12px;overflow:hidden}
.glostab th{text-align:left;background:#f2f4f7;color:#546a8c;font-weight:800;font-size:11.5px;letter-spacing:.04em;padding:9px 12px;position:sticky;top:0}
.glostab td{padding:8px 12px;border-top:1px solid #eef1f4;vertical-align:top}
.glostab tr:hover td{background:#fafbfc}
.note{max-width:1100px;margin:12px auto 0;padding:0 18px;color:#8a6a00;font-size:12.5px}
#app .wrap{padding-bottom:70px}
#app .cell .cwrap{max-height:none!important;overflow:visible!important;display:block!important;-webkit-line-clamp:unset!important}
#app .cell{height:auto}
.cedit{width:100%;min-height:42px;border:1px solid #d4dae1;border-radius:6px;background:#fff;padding:6px 7px;font:inherit;font-size:11.5px;line-height:1.42;color:#1d2630;resize:vertical;overflow:hidden}
.cedit:focus{outline:none;border-color:#d52b1e;box-shadow:0 0 0 2px rgba(213,43,30,.14)}
.cedit.changed{border-color:#d52b1e;background:#fff8f7}
</style></head>
<body>
<div id="gate"><form id="gateform" class="gatebox">
  <h1>&#128274; FTEM Admin</h1>
  <p>Bitte Passwort eingeben, um Inhalte zu bearbeiten.</p>
  <input id="gatepw" type="password" placeholder="Passwort" autocomplete="current-password">
  <button type="submit">Anmelden</button>
  <div id="gateerr" class="gateerr"></div>
</form></div>
<div id="app" hidden>
  <header class="abar">
    <h1>&#128274; FTEM &ndash; Inhalte bearbeiten</h1>
    <label>Sportart: <select id="sportsel">__SPORT_OPTIONS__</select></label>
    <span class="sp"></span>
    <span id="astatus" class="astatus"></span>
    <button id="asave" class="asave" disabled>Speichern</button>
    <button id="glossbtn" class="agloss" type="button">Glossar</button>
    <a href="index.html" class="asite">&#8617; Zur Seite</a>
  </header>
  <div id="note" class="note"></div>
  <div id="glosspanel" hidden>
    <div class="glosbar"><input id="glosq" type="search" placeholder="Begriff suchen (Deutsch oder Französisch) …"><span id="gloscount" class="astatus"></span></div>
    <p class="glosnote">Feste Übersetzungen DE&nbsp;&rarr;&nbsp;FR. Diese Begriffe werden bei der Übersetzung der Inhalte einheitlich verwendet.</p>
    <div class="glosadd">
      <input id="gde" type="text" placeholder="Deutsch">
      <input id="gfr" type="text" placeholder="Français">
      <button id="gaddbtn" type="button">Hinzufügen</button>
      <span id="gaddmsg" class="astatus"></span>
    </div>
    <div id="glostable"></div>
  </div>
  <div id="editwrap">__ADMIN_SECTIONS__</div>
</div>
<script>
const ORIG=__ADMIN_ORIG__, GLOSS=__GLOSSARY__, PW="__ADMIN_PW__", SUPA_URL="__SUPA_URL__", SUPA_KEY="__SUPA_KEY__";
const gate=document.getElementById('gate'),app=document.getElementById('app');
function gesc(s){return String(s).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
function renderGloss(q){
  q=(q||'').trim().toLowerCase();
  const rows=GLOSS.filter(function(g){return !q||g.de.toLowerCase().indexOf(q)>=0||g.fr.toLowerCase().indexOf(q)>=0;});
  document.getElementById('gloscount').textContent=rows.length+' Begriffe';
  let h='<table class="glostab"><thead><tr><th>Deutsch</th><th>Français</th></tr></thead><tbody>';
  rows.forEach(function(g){h+='<tr><td>'+gesc(g.de)+'</td><td>'+gesc(g.fr)+'</td></tr>';});
  document.getElementById('glostable').innerHTML=h+'</tbody></table>';
}
const glosDe=new Set(GLOSS.map(function(g){return g.de;}));
function loadGlossAdditions(){
  if(!SUPA_URL||!SUPA_KEY)return Promise.resolve();
  return fetch(SUPA_URL+'/rest/v1/ftem_glossary?select=de,fr',{headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY}})
    .then(function(r){return r.ok?r.json():[];}).then(function(rows){
      (rows||[]).forEach(function(x){ if(!glosDe.has(x.de)){glosDe.add(x.de);GLOSS.unshift({de:x.de,fr:x.fr});} });
    }).catch(function(){});
}
function addGloss(){
  const de=document.getElementById('gde').value.trim(), fr=document.getElementById('gfr').value.trim();
  const msg=document.getElementById('gaddmsg');
  if(!de||!fr){msg.textContent='Bitte beide Felder ausfüllen.';return;}
  if(!SUPA_URL||!SUPA_KEY){msg.textContent='Cloud-Speicher nicht eingerichtet – Begriff kann nicht gespeichert werden.';return;}
  msg.textContent='Speichere …';
  fetch(SUPA_URL+'/rest/v1/ftem_glossary',{method:'POST',
    headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY,'Content-Type':'application/json',Prefer:'resolution=merge-duplicates,return=minimal'},
    body:JSON.stringify([{de:de,fr:fr}])})
   .then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);
     if(glosDe.has(de)){GLOSS.forEach(function(g){if(g.de===de)g.fr=fr;});}else{glosDe.add(de);GLOSS.unshift({de:de,fr:fr});}
     document.getElementById('gde').value='';document.getElementById('gfr').value='';
     msg.textContent='✓ hinzugefügt';renderGloss(document.getElementById('glosq').value);
   }).catch(function(e){msg.textContent='Fehler: '+e.message;});
}
function toggleGloss(){
  const gp=document.getElementById('glosspanel'),ew=document.getElementById('editwrap'),sw=document.getElementById('sportsel').parentNode;
  const show=gp.hidden;
  gp.hidden=!show; ew.hidden=show; sw.style.visibility=show?'hidden':'';
  document.getElementById('glossbtn').textContent=show?'← Bearbeiten':'Glossar';
  if(show&&!gp.dataset.done){gp.dataset.done='1';renderGloss('');
    loadGlossAdditions().then(function(){renderGloss(document.getElementById('glosq').value);});
    document.getElementById('glosq').addEventListener('input',function(e){renderGloss(e.target.value);});
    document.getElementById('gaddbtn').addEventListener('click',addGloss);}
}
const statusEl=document.getElementById('astatus'),saveBtn=document.getElementById('asave'),sel=document.getElementById('sportsel');
const base=Object.assign({},ORIG);
function autosize(ta){ta.style.height='auto';ta.style.height=(ta.scrollHeight+2)+'px';}
document.getElementById('gateform').addEventListener('submit',function(e){
  e.preventDefault();
  if(document.getElementById('gatepw').value===PW){gate.style.display='none';app.hidden=false;init();}
  else document.getElementById('gateerr').textContent='Falsches Passwort.';
});
function showSport(id){
  app.querySelectorAll('section.sport').forEach(function(s){s.hidden=s.dataset.sport!==id;});
  app.querySelectorAll('section.sport[data-sport="'+id+'"] .cedit').forEach(autosize);
  window.scrollTo(0,0);
}
function changed(){
  const out=[];
  app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){
    const cid=ta.dataset.cid;if((base[cid]||'')!==ta.value)out.push({cid:cid,txt:ta.value});
  });
  return out;
}
function updateCount(){const n=changed().length;saveBtn.disabled=n===0;statusEl.textContent=n?(n+' ungespeichert'):'Alles gespeichert';}
function init(){
  sel.addEventListener('change',function(){showSport(sel.value);});
  app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){
    ta.addEventListener('input',function(){autosize(ta);ta.classList.toggle('changed',(base[ta.dataset.cid]||'')!==ta.value);updateCount();});
  });
  saveBtn.addEventListener('click',save);
  document.getElementById('glossbtn').addEventListener('click',toggleGloss);
  if(SUPA_URL&&SUPA_KEY){
    fetch(SUPA_URL+'/rest/v1/ftem_overrides?select=cid,txt',{headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY}})
      .then(function(r){return r.ok?r.json():[];}).then(function(rows){
        const m={};(rows||[]).forEach(function(x){m[x.cid]=x.txt;});
        app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){const cid=ta.dataset.cid;if(m[cid]!=null){ta.value=m[cid];base[cid]=m[cid];}});
        showSport(sel.value);updateCount();
      }).catch(function(){});
  }else{
    document.getElementById('note').textContent='Hinweis: Cloud-Speicher (Supabase) ist noch nicht eingerichtet – Änderungen können bearbeitet und als Datei heruntergeladen, aber noch nicht direkt live gespeichert werden. Siehe SETUP-ADMIN.md.';
    saveBtn.textContent='Herunterladen';
  }
  showSport(sel.value||(sel.options[0]&&sel.options[0].value));
  updateCount();
}
function save(){
  const ch=changed();if(!ch.length)return;
  if(!SUPA_URL||!SUPA_KEY){
    const blob=new Blob([JSON.stringify(ch,null,2)],{type:'application/json'});
    const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='ftem-aenderungen.json';a.click();return;
  }
  saveBtn.disabled=true;statusEl.textContent='Speichere …';
  fetch(SUPA_URL+'/rest/v1/ftem_overrides',{method:'POST',
    headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY,'Content-Type':'application/json',Prefer:'resolution=merge-duplicates,return=minimal'},
    body:JSON.stringify(ch)})
   .then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);
     ch.forEach(function(x){base[x.cid]=x.txt;});
     app.querySelectorAll('.cedit.changed').forEach(function(t){t.classList.remove('changed');});
     statusEl.textContent='Gespeichert ✓ – Änderungen sind jetzt live.';saveBtn.disabled=true;
   }).catch(function(err){statusEl.textContent='Fehler beim Speichern: '+err.message;saveBtn.disabled=false;});
}
</script></body></html>'''

def admin_html(datamap):
    secs = ""; opts = ""; orig = {}
    for s in SPORTS:
        d = datamap[s["id"]]
        if not d: continue
        secs += sport_section(s, d, "de", edit=True)
        opts += '<option value="'+esc(s["id"])+'">'+esc(tr(s["name"], "de"))+'</option>'
        for ti, t in enumerate(d["themes"]):
            for ri, r in enumerate(t["rows"]):
                for si, seg in enumerate(r["segs"]):
                    orig[s["id"]+"|"+str(ti)+"|"+str(ri)+"|"+str(si)] = seg.get("v") or ""
    orig_js = json.dumps(orig, ensure_ascii=False).replace("</", "<\\/")
    gloss = []
    gpath = os.path.join(BASE, "glossary.json")
    if os.path.exists(gpath):
        gloss = json.load(open(gpath, encoding="utf-8"))
    gloss_js = json.dumps(gloss, ensure_ascii=False).replace("</", "<\\/")
    return (ADMIN_TMPL.replace("__MAINCSS__", CSS)
                      .replace("__ADMIN_SECTIONS__", secs)
                      .replace("__SPORT_OPTIONS__", opts)
                      .replace("__ADMIN_ORIG__", orig_js)
                      .replace("__GLOSSARY__", gloss_js)
                      .replace("__ADMIN_PW__", ADMIN_PW)
                      .replace("__SUPA_URL__", SUPABASE_URL)
                      .replace("__SUPA_KEY__", SUPABASE_ANON_KEY))

datamap = {s["id"]: sport_data(s) for s in SPORTS}
ids_with_data = [s["id"] for s in SPORTS if datamap[s["id"]] is not None]

for lang in LANGS:
    open_ext = {"de": "Im neuen Tab öffnen", "fr": "Ouvrir dans un nouvel onglet", "it": "Aprire in una nuova scheda"}[lang]
    mmodal = ('<div class="mmodal" hidden><div class="mm-box">'
              '<div class="mm-bar"><span class="mm-t"></span>'
              '<a class="mm-ext" href="#" target="_blank" rel="noopener">'+esc(open_ext)+' ↗</a>'
              '<button class="mm-x" type="button" aria-label="schliessen">✕</button></div>'
              '<iframe class="mm-frame" src="about:blank" title="Mission Swiss-Ski"></iframe>'
              '</div></div>')
    body = home_html(datamap, lang) + "".join(sport_section(s, datamap[s["id"]], lang) for s in SPORTS) + mmodal
    i18n = {"more": tr("mehr ▾", lang), "less": tr("weniger ▴", lang),
            "themes": tr("Themen · F1–M", lang), "hits": tr("Themen mit Treffern", lang),
            "hitsWord": {"de": "Treffer", "fr": "résultats", "it": "risultati"}[lang],
            "noHits": {"de": "keine Treffer", "fr": "aucun résultat", "it": "nessun risultato"}[lang]}
    js = (JS.replace("__SPORT_IDS__", json.dumps([s["id"] for s in SPORTS]))
            .replace("__I18N__", json.dumps(i18n, ensure_ascii=False))
            .replace("__SUPA_URL__", SUPABASE_URL).replace("__SUPA_KEY__", SUPABASE_ANON_KEY))
    og_title = "FTEM – Athlet:innen-Weg · Swiss-Ski"
    og_desc = {"de":"Der Athlet:innen-Weg von Swiss-Ski: alle Schneesportarten über die zehn FTEM-Entwicklungsstufen F1–M.",
               "fr":"Le parcours des athlètes de Swiss-Ski : tous les sports de neige à travers les dix niveaux de développement FTEM (F1–M).",
               "it":"Il percorso degli atleti di Swiss-Ski: tutti gli sport sulla neve lungo i dieci livelli di sviluppo FTEM (F1–M)."}[lang]
    og_img = (SITE_URL.rstrip("/")+"/assets/og-image.jpg") if SITE_URL else "assets/og-image.jpg"
    og_locales = {"de":"de_CH","fr":"fr_CH","it":"it_CH"}
    base = SITE_URL.rstrip("/") if SITE_URL else ""
    # hreflang: verlinkt die drei Sprachvarianten gegenseitig (+ x-default)
    alt_links = ""
    for lg, fn in FILES.items():
        href = (base+"/"+fn) if base else fn
        alt_links += '<link rel="alternate" hreflang="'+lg+'" href="'+esc(href)+'">'
    alt_links += '<link rel="alternate" hreflang="x-default" href="'+esc((base+"/index.html") if base else "index.html")+'">'
    og_alt = "".join('<meta property="og:locale:alternate" content="'+og_locales[lg]+'">'
                     for lg in FILES if lg != lang)
    head_meta = ('<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">'
        '<link rel="icon" type="image/png" sizes="192x192" href="assets/icon-192.png">'
        '<link rel="apple-touch-icon" href="assets/icon-180.png">'
        '<link rel="manifest" href="manifest.webmanifest">'
        +alt_links+
        '<meta name="theme-color" content="#0f1622">'
        '<meta name="description" content="'+esc(og_desc)+'">'
        '<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="Swiss-Ski FTEM">'
        '<meta property="og:locale" content="'+og_locales[lang]+'">'
        +og_alt+
        '<meta property="og:title" content="'+esc(og_title)+'">'
        '<meta property="og:description" content="'+esc(og_desc)+'">'
        '<meta property="og:image" content="'+esc(og_img)+'">'
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
        +('<meta property="og:url" content="'+esc((base+"/"+FILES[lang]) if base else FILES[lang])+'">' if SITE_URL else '')+
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="'+esc(og_title)+'">'
        '<meta name="twitter:description" content="'+esc(og_desc)+'">'
        '<meta name="twitter:image" content="'+esc(og_img)+'">')
    page = ('<!DOCTYPE html><html lang="'+lang+'"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>FTEM – '+esc(tr("Athlet:innen-Weg", lang))+'</title>'
        +head_meta+
        # verhindert Aufblitzen der Startseite, wenn direkt eine Sportart (#hash) geladen wird
        '<script>if(location.hash)document.documentElement.classList.add("h");'
        'try{if(sessionStorage.ftemSeen)document.documentElement.classList.add("noanim");sessionStorage.ftemSeen=1}catch(e){}</script>'
        '<style>'+CSS+'</style></head>'
        '<body>'+body+'<script>'+js+'</script></body></html>')
    out = os.path.join(BASE, FILES[lang])
    open(out,"w",encoding="utf-8").write(page)
    print("written", FILES[lang], len(page.encode("utf-8")), "bytes")

open(os.path.join(BASE, "admin.html"), "w", encoding="utf-8").write(admin_html(datamap))
print("written admin.html")

print("Sportarten mit Inhalt:", ", ".join(ids_with_data) or "-")
