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
# Passwort fuer den versteckten Praesentationsmodus (dezentes ⛶-Symbol unten auf den Sportseiten)
PRES_PW = "FTEMP"
# Uebergeordnete Mission-Seite (Link folgt). Solange leer, oeffnet der Mission-Button
# eine Auswahl der Sportarten-Missionen (aus ftem_sports.json).
MISSION_URL = ""
PRES_TITLE = {"de": "Präsentationsmodus", "fr": "Mode présentation", "it": "Modalità presentazione"}
PRES_PWPH = {"de": "Passwort", "fr": "Mot de passe", "it": "Password"}
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
SEARCH_PH = {"de": "Suche…", "fr": "Rechercher…", "it": "Cerca…"}
EXPAND_ALL = {"de": "Alle öffnen", "fr": "Tout ouvrir", "it": "Apri tutto"}
COLLAPSE_ALL = {"de": "Alle schliessen", "fr": "Tout fermer", "it": "Chiudi tutto"}
CLEAR_LBL = {"de": "Leeren", "fr": "Effacer", "it": "Cancella"}
CHAT_BTN = {"de": "FTEM-Assistent (KI)", "fr": "Assistant FTEM (IA)", "it": "Assistente FTEM (IA)"}

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
        body_bl = bullets_from_text(rest)
        if body_bl:
            return '<p class="bh">'+esc(head)+'</p>'+body_bl
        return '<p class="bh">'+esc(head)+'</p><p>'+esc(rest).replace("\n","<br>")+'</p>'
    # label: value (single label line)
    m = re.match(r'^([^:\n]{2,46}):\s*(.+)$', b, re.S)
    if m and "\n" not in m.group(1):
        lab = m.group(1).strip(); val = m.group(2).strip()
        if len(val) > 55 or "\n" in val:
            vb = bullets_from_text(val)
            if vb:
                return '<p class="sh">'+esc(lab)+'</p>'+vb
            return '<p class="sh">'+esc(lab)+'</p><p>'+esc(val).replace("\n","<br>")+'</p>'
        return '<p><span class="lbl">'+esc(lab)+':</span> '+esc(val).replace("\n","<br>")+'</p>'
    pb = bullets_from_text(b)
    if pb:
        return pb
    return '<p>'+esc(b).replace("\n","<br>")+'</p>'

def clean_ws(s):
    # nur fuer die Anzeige: Tabs zu Leerzeichen, Mehrfach-Leerzeichen und
    # riesige Luecken zusammenfassen, Zeilenenden trimmen. Absaetze (\n\n) bleiben.
    s = s.replace("\t", " ")
    lines = [re.sub(r" {2,}", " ", ln).rstrip() for ln in s.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()

# Off-Snow / On-Snow Zonen-Gruppierung: "Ziele Off-Snow: ..." -> Zone "Off-Snow"
ZONE_RE = re.compile(r'^(.{1,20}?)\s+(Off-Snow|On-Snow)\s*[:.]\s*(.*)$', re.S)

# Mehrsatz-Fliesstext -> Stichpunkte (ein Satz = ein Bullet), mit Abkuerzungs-Schutz
_ABBR = ["z.B.","z. B.","u.a.","u. a.","d.h.","d. h.","u.v.m.","o.ä.","u.ä.","ca.","bzw.",
         "inkl.","exkl.","max.","min.","Nr.","sek.","Sek.","Min.","Std.","etc.","usw.",
         "evtl.","ggf.","vs.","engl.","env.","p.ex.","p. ex.","c.-à-d.","ecc.","Bsp."]
_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[«"„(\[A-ZÄÖÜ0-9])')
def split_sentences(text):
    t = text
    for a in _ABBR:
        t = t.replace(a, a.replace(".", "\x00"))
    t = re.sub(r'(\d)\.(\d)', lambda m: m.group(1)+"\x00"+m.group(2), t)   # Dezimalzahlen
    t = re.sub(r'\b(\d{1,2})\.(?=\s[A-ZÄÖÜ])', lambda m: m.group(1)+"\x00", t)  # Ordinalzahlen
    parts = [p.strip() for p in _SENT_SPLIT.split(t) if p.strip()]
    out = []
    for p in parts:
        p = p.replace("\x00", ".").strip()
        if p.endswith(".") and not p.endswith(".."):
            p = p[:-1]
        out.append(p)
    return out
# Wörter nach einem Komma, die einen Nebensatz einleiten (kein Aufzählungsglied)
_CONNECTORS = {"um","damit","sodass","wobei","weil","da","wenn","falls","aber","sondern",
    "denn","dabei","während","bis","obwohl","indem","ohne","statt","anstatt","jedoch",
    "allerdings","sowie","respektive","resp","bzw","evtl","ggf","wodurch","womit",
    "welche","welcher","welches","was","also","dann","je","und","oder",
    "für","mit","im","in","auf","bei","von","zur","zum","nach","über","unter",
    "durch","gegen","an","am","aus","vor","als"}
def split_commas(s):
    # Trennung an Top-Level-Kommas; Klammern, Dezimalkommas (1,3) und Nebensatz-Kommas bleiben
    parts, depth, cur, n = [], 0, "", len(s)
    for i, ch in enumerate(s):
        if ch in "([{": depth += 1
        elif ch in ")]}": depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            prevc = s[i-1] if i > 0 else ""
            if prevc.isdigit() and i+1 < n and s[i+1].isdigit():
                cur += ch; continue          # Dezimalkomma
            j = i + 1
            while j < n and s[j] == " ": j += 1
            w = ""
            while j < n and s[j].isalpha(): w += s[j]; j += 1
            if w.lower() in _CONNECTORS:
                cur += ch; continue          # Nebensatz-/Konjunktions-Komma
            parts.append(cur); cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]

def sentence_bullets(text):
    # Satz- UND Komma-Aufzählungen -> Liste von Stichpunkten (oder None)
    if "\n" in text or "•" in text:
        return None
    items = []
    for s in split_sentences(text):
        parts = split_commas(s)
        if len(parts) >= 2:
            items.extend(parts)
        else:
            items.append(s)
    return items if len(items) >= 2 else None

def bullets_from_text(text):
    items = sentence_bullets(text)
    if items:
        return '<ul class="bl">'+"".join('<li>'+esc(s)+'</li>' for s in items)+'</ul>'
    return None

def _zone_body(text):
    lines = text.split("\n")
    if any(l.strip().startswith("•") for l in lines):
        items = [l.strip().lstrip("•").strip() for l in lines if l.strip().startswith("•")]
        intro = " ".join(l.strip() for l in lines if l.strip() and not l.strip().startswith("•"))
        html = (esc(intro)+" ") if intro else ""
        html += '<ul class="bl">'+"".join('<li>'+esc(i)+'</li>' for i in items if i)+'</ul>'
        return html, True
    bl = bullets_from_text(text)
    if bl:
        return bl, True
    return esc(text).replace("\n", "<br>"), False

def render_zone_groups(blocks):
    parsed = []
    for b in blocks:
        b = b.strip()
        if not b: continue
        head = b.split("\n", 1)
        m = ZONE_RE.match(head[0].strip())
        if not m: return None
        label, zone, rest = m.group(1).strip(), m.group(2), m.group(3).strip()
        tail = head[1] if len(head) > 1 else ""
        text = "\n".join(x for x in ([rest] if rest else []) + ([tail] if tail.strip() else [])).strip()
        parsed.append((zone, label, text))
    if len(parsed) < 2: return None
    order, buckets = [], {}
    for zone, label, text in parsed:
        if zone not in buckets: buckets[zone] = []; order.append(zone)
        buckets[zone].append((label, text))
    out = ""
    for zone in order:
        out += '<div class="zone"><span class="zlab">'+esc(zone)+'</span>'
        for label, text in buckets[zone]:
            body, is_list = _zone_body(text)
            if is_list:
                out += '<div class="zsub zsub-l"><span class="zk">'+esc(label)+'</span>'+body+'</div>'
            else:
                out += '<div class="zsub"><span class="zk">'+esc(label)+'</span> '+body+'</div>'
        out += '</div>'
    return out

def render_cell(seg, lang, cid=None, edit=False):
    if edit:
        raw = seg.get("v") or ""
        return '<textarea class="cedit" data-cid="'+esc(cid or "")+'">'+esc(raw)+'</textarea>'
    txt = clean_ws((tr(seg["v"], lang) or "").strip())
    link_texts = set(tr(l["text"], lang) for l in seg["l"] if l.get("text"))
    inner = ""
    if txt:
        blocks = re.split(r'\n\s*\n', txt)
        zoned = render_zone_groups(blocks)
        if zoned is not None:
            inner = zoned
        else:
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

def theme_toggle():
    return ('<button class="themebtn" type="button" onclick="toggleTheme()" '
            'title="Hell / Dunkel" aria-label="Hell/Dunkel umschalten">'
            '<svg class="ic-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
            '<svg class="ic-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/>'
            '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
            '</button>')

def stage_bar(stages, lang):
    btns = "".join('<button class="sb ph-'+ph(s)+'" data-si="'+str(i)+'" aria-pressed="false" '
                   'title="'+esc(FULL.get(s,s))+'">'+esc(s)+'</button>' for i, s in enumerate(stages))
    return ('<div class="stagebar" role="group" aria-label="'+esc(tr("Stufe hervorheben", lang))+'">'+btns+'</div>')

def sport_section(sport, d, lang, edit=False):
    sid = sport["id"]; name = tr(sport["name"], lang)
    if edit and d is not None:
        sections, _ = build_sections(d, sid, lang, edit=True)
        return '<section class="sport" data-sport="'+sid+'" hidden><div class="wrap">'+sections+'</div></section>'
    aw = esc(tr("Athlet:innen-Weg", lang))
    back = ('<a class="back" href="#" title="'+esc(BACK_TITLE[lang])+'" aria-label="'+esc(BACK_TITLE[lang])+'">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></a>')
    if sport.get("icon"):
        back += '<img class="sicon" src="'+esc(sport["icon"])+'" alt="'+esc(name)+'" width="32" height="32" decoding="async">'
    # Sportarten-Wechsel direkt im Titel (Dropdown statt fixer Ueberschrift)
    sport_opts = "".join('<option value="'+x["id"]+'"'+(' selected' if x["id"] == sid else '')+'>'
                         + esc(tr(x["name"], lang)) + '</option>' for x in SPORTS)
    title_sel = '<select class="sportsel2" aria-label="Sportart wechseln">'+sport_opts+'</select>'
    if d is None:
        return ('<section class="sport" data-sport="'+sid+'" hidden>'
            '<header class="top"><div class="ht-l">'+back+title_sel+'</div>'
            '<div class="ht-r">'+lang_switch(lang)+theme_toggle()+'</div></header>'
            '<div class="wrap"><div class="placeholder">'
            '<div class="big">'+esc(name)+'</div>'
            +PLACE[lang].format(name=esc(name), file='ftem_data_'+esc(sid)+'.json')+
            '</div></div></section>')
    sections, jump_opts = build_sections(d, sid, lang)
    n_themes = len(d["themes"])
    return ('<section class="sport" data-sport="'+sid+'" hidden>'
        '<header class="top"><div class="ht-l">'+back+title_sel+'</div>'
        '<div class="ht-c"><div class="qbox">'
        '<svg class="qic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20.5 20.5l-3.6-3.6"/></svg>'
        '<input class="q" type="search" placeholder="'+esc(SEARCH_PH[lang])+'" aria-label="'+esc(SEARCH_PH[lang])+'">'
        '<span class="hits"></span>'
        '<button class="qx" type="button" hidden title="'+esc(CLEAR_LBL[lang])+'" aria-label="'+esc(CLEAR_LBL[lang])+'">&times;</button>'
        '</div></div>'
        '<div class="ht-r"><select class="jump"><option>'+esc(tr("Zu Thema springen…", lang))+'</option>'+jump_opts+'</select>'
        '<button class="toggleall" type="button" title="'+esc(EXPAND_ALL[lang])+'" aria-label="'+esc(EXPAND_ALL[lang])+'" data-open="'+esc(EXPAND_ALL[lang])+'" data-close="'+esc(COLLAPSE_ALL[lang])+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 13l5 5 5-5"/><path d="M7 6l5 5 5-5"/></svg></button>'
        '<button class="pdf" title="'+esc(tr("Drucken / als PDF speichern", lang))+'" aria-label="'+esc(tr("Drucken / als PDF speichern", lang))+'"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9V3h12v6"/><path d="M6 18H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="7" rx="1"/><circle cx="17.5" cy="12" r="1" fill="currentColor" stroke="none"/></svg></button>'
        '<span class="hdiv" aria-hidden="true"></span>'
        +lang_switch(lang)+theme_toggle()+'</div></header>'
        '<div class="wrap">'
        +sections
        # Versteckter Praesentationsmodus: dezentes Symbol unten (wie Admin-Schloss), Passwort noetig
        +'<div class="preslink"><button class="presopen" type="button" title="'+esc(PRES_TITLE[lang])+'" aria-label="'+esc(PRES_TITLE[lang])+'">⛶</button>'
        '<span class="presask" hidden><input class="prespw" type="password" placeholder="'+esc(PRES_PWPH[lang])+'" autocomplete="off">'
        '<button class="presgo" type="button">OK</button></span></div>'
        '</div>'
        +stage_bar(d["stages"], lang)+'</section>')

# --- Startseite (Sportart-Auswahl) -----------------------------------------
# Positionen der Sternbild-Knoten (x%, y%) auf der Hero-Flaeche
# Entlang der Bergsilhouette von hero.jpg: unten links im Vorgelaende startend,
# ueber den linken Grat zum Gipfelbereich, rechts wieder abfallend.
# Strenges Zickzack (Gipfel/Tal im Wechsel): so laufen die Linien immer VON der
# Beschriftung weg und keine Schrift kreuzt eine Linie.
# Kammlinie des Hero-Fotos (automatisch + manuell nachgezeichnet), Koordinaten in Bildpixeln (1896x986)
RIDGE_PATH = "M0,986 L0,493 L0,493 L24,529 L48,524 L72,521 L96,512 L120,520 L144,529 L168,538 L192,553 L216,546 L240,552 L264,543 L288,522 L312,503 L336,478 L360,452 L384,425 L408,408 L432,399 L456,412 L480,397 L504,372 L528,349 L552,329 L576,337 L600,350 L624,361 L648,346 L672,330 L696,316 L720,326 L744,356 L768,374 L792,391 L816,394 L840,391 L864,381 L888,369 L912,353 L936,332 L960,308 L984,282 L1008,255 L1032,235 L1056,257 L1080,283 L1104,304 L1128,306 L1152,312 L1176,314 L1200,322 L1224,337 L1248,342 L1272,347 L1296,358 L1320,372 L1344,393 L1368,418 L1392,438 L1416,440 L1440,429 L1464,423 L1488,410 L1512,406 L1536,402 L1560,385 L1584,381 L1608,382 L1632,385 L1656,387 L1680,402 L1704,406 L1728,416 L1752,421 L1776,431 L1800,434 L1824,426 L1848,418 L1872,410 L1895,493 L1896,493 L1896,986 Z"

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

INSTALL_HINT = {
 "de": {"title": "Als App aufs Handy legen",
        "body": "Diese Seite lässt sich wie eine App speichern – ohne Download.<br>"
                "<b>iPhone (Safari):</b> «Teilen» <span class=\"ai-i\">&#8593;</span> → «Zum Home-Bildschirm».<br>"
                "<b>Android (Chrome):</b> Menü ⋮ → «App installieren»."},
 "fr": {"title": "Ajouter comme app",
        "body": "Cette page s'enregistre comme une app – sans téléchargement.<br>"
                "<b>iPhone (Safari) :</b> « Partager » <span class=\"ai-i\">&#8593;</span> → « Sur l'écran d'accueil ».<br>"
                "<b>Android (Chrome) :</b> menu ⋮ → « Installer l'application »."},
 "it": {"title": "Aggiungi come app",
        "body": "Questa pagina si salva come un'app – senza download.<br>"
                "<b>iPhone (Safari):</b> « Condividi » <span class=\"ai-i\">&#8593;</span> → « Aggiungi a Home ».<br>"
                "<b>Android (Chrome):</b> menu ⋮ → « Installa app »."},
}

def install_hint(lang):
    t = INSTALL_HINT.get(lang, INSTALL_HINT["de"])
    return ('<div class="appinstall">'
            '<img class="ai-icon" src="assets/icon-192.png" width="60" height="60" '
            'alt="FTEM App-Icon" decoding="async">'
            '<div class="ai-txt"><div class="ai-h">'+esc(t["title"])+'</div>'
            '<p>'+t["body"]+'</p></div></div>')

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
    # FTEM-Weg als Berg-Schichten (Design "Beispiel 2"): F unten -> M Gipfel, Talent dominant.
    # Farben bewusst entsaettigt/transparent, damit sie mit dem Bergfoto verschmelzen.
    band_lbl = {"de": ["FOUNDATION","TALENT","ELITE","MASTERY"],
                "fr": ["FOUNDATION","TALENT","ELITE","MASTERY"],
                "it": ["FOUNDATION","TALENT","ELITE","MASTERY"]}[lang]
    # FTEM-Zonen folgen der echten Bergsilhouette: SVG mit Foto + ClipPath auf der Kammlinie.
    # Die Farbbaender sind Hoehenzonen des Bergs (M = Gipfel, F = Basis).
    hero_svg = ('<svg class="heromt" viewBox="0 0 1896 986" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
        '<defs>'
        '<clipPath id="mtclip"><path d="'+RIDGE_PATH+'"/></clipPath>'
        '<linearGradient id="herodark" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="rgba(9,14,24,.66)"/><stop offset=".45" stop-color="rgba(12,17,28,.5)"/><stop offset="1" stop-color="rgba(7,11,20,.9)"/></linearGradient>'
        '</defs>'
        '<image href="assets/hero.jpg" x="0" y="0" width="1896" height="986" preserveAspectRatio="none"/>'
        '<rect x="0" y="0" width="1896" height="986" fill="url(#herodark)"/>'
        '<g clip-path="url(#mtclip)">'
        '<rect x="0" y="0" width="1896" height="375" fill="rgba(216,72,58,.46)"/>'
        '<rect x="0" y="375" width="1896" height="118" fill="rgba(222,140,80,.46)"/>'
        '<rect x="0" y="493" width="1896" height="227" fill="rgba(222,184,88,.48)"/>'
        '<rect x="0" y="720" width="1896" height="266" fill="rgba(86,158,178,.48)"/>'
        '</g>'
        '<path d="'+RIDGE_PATH+'" fill="none" stroke="rgba(255,255,255,.38)" stroke-width="2"/>'
        '</svg>')
    pyr = (hero_svg +
           '<div class="pyr" role="navigation" aria-label="FTEM-Stufen">'
           '<div class="pband pm" tabindex="0"><span class="pb-n">'+band_lbl[3]+'</span><span class="pb-s">M</span></div>'
           '<div class="pband pe" tabindex="0"><span class="pb-n">'+band_lbl[2]+'</span><span class="pb-s">E1 – E2</span></div>'
           '<div class="pband pt" tabindex="0"><span class="pb-n">'+band_lbl[1]+'</span><span class="pb-s">T1 – T4</span></div>'
           '<div class="pband pf" tabindex="0"><span class="pb-n">'+band_lbl[0]+'</span><span class="pb-s">F1 – F3</span></div>'
           '</div>')
    # Klick auf eine Stufe -> Sportarten-Auswahl -> Athlet:innen-Weg der Sportart
    choose_lbl = {"de": "Sportart wählen", "fr": "Choisir un sport", "it": "Scegli lo sport"}[lang]
    spitems = ""
    for s2 in SPORTS:
        nm = tr(s2["name"], lang)
        ic = s2.get("icon")
        inner2 = ('<img src="'+esc(ic)+'" alt="" loading="lazy">') if ic else ('<span class="spcode">'+esc(s2["short"])+'</span>')
        spitems += '<a href="#'+s2["id"]+'">'+inner2+'<b>'+esc(nm)+'</b></a>'
    spmodal = ('<div class="spmodal" hidden><div class="sp-box">'
               '<div class="sp-bar"><span>'+esc(choose_lbl)+'</span><button class="sp-x" type="button" aria-label="schliessen">✕</button></div>'
               '<div class="sp-grid">'+spitems+'</div></div></div>')
    # Meeting-Paket: News-Button oben rechts, Mission-Button unter dem Logo,
    # Startseite ohne Scrollen (News/Infos als Overlays), Admin-Schloss unten im Hero.
    news_label = {"de": "News", "fr": "Actualités", "it": "Notizie"}[lang]
    info_label = FTEM_INFO[lang]["title"].replace("&#x27;", "'")
    mission_items = "".join(
        '<a class="mission-item" href="'+esc(s2["mission"])+'" data-title="'+esc(tr(s2["name"], lang))+' – Mission Swiss-Ski">'
        + esc(tr(s2["name"], lang)) + '</a>'
        for s2 in SPORTS if s2.get("mission"))
    if MISSION_URL:
        mission_btn = '<a class="hcta np-mission" href="'+esc(MISSION_URL)+'" data-title="Mission Swiss-Ski">Mission Swiss-Ski</a>'
    else:
        mission_btn = '<button class="hcta" type="button" data-open="tpl-missions" data-t="Mission Swiss-Ski">Mission Swiss-Ski</button>'
    adminlk = ('<div class="adminlink adminlink-hero"><a href="admin.html" title="Admin-Login" aria-label="Admin-Login">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="url(#adminlk)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<defs><linearGradient id="adminlk" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#1f8fa6"/><stop offset=".4" stop-color="#e2a900"/><stop offset=".7" stop-color="#e8772e"/><stop offset="1" stop-color="#d52b1e"/></linearGradient></defs>'
            '<rect x="4.6" y="10.4" width="14.8" height="10.2" rx="2.4"/><path d="M8 10.4V7.4a4 4 0 0 1 8 0v3"/>'
            '<circle cx="12" cy="15" r="1.5" fill="url(#adminlk)" stroke="none"/></svg></a></div>')
    return ('<section id="home">'
            '<div class="home-hero">'
            '<div class="hero-top"><div class="lsrow">'+lang_switch(lang)+theme_toggle()+'</div>'
            '<select class="homesport" aria-label="'+esc({"de":"Sportart wählen","fr":"Choisir un sport","it":"Scegli lo sport"}[lang])+'">'
            + "".join('<option value="'+x["id"]+'">'+esc(tr(x["name"], lang))+'</option>' for x in SPORTS)
            + '</select>'
            +fb+'</div>'
            '<div class="hero-top-r"><button class="news-btn" type="button" data-open="tpl-news" data-t="'+esc(news_label)+'">'+esc(news_label)+'</button>'
            '<button class="info-btn" type="button" data-open="tpl-info" data-t="'+esc(info_label)+'">'+info_label+'</button></div>'
            '<div class="hero-head"><h1>'+FTEM+'</h1>'
            '<img class="hero-logo" src="assets/swiss-ski-logo.svg" alt="Swiss-Ski">'
            '<div class="hero-cta">'+mission_btn+'</div></div>'
            +pyr+adminlk+
            '</div>'
            '<template id="tpl-news">'+news_html(lang)+install_hint(lang)+'</template>'
            '<template id="tpl-info">'+ftem_info+'</template>'
            '<template id="tpl-missions"><div class="mlist">'+mission_items+'</div></template>'
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
body{margin:0;font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg);line-height:1.45;font-size:13px;-webkit-text-size-adjust:100%}
.langsw{display:flex;gap:2px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:2px}
.langsw a{font-size:11.5px;font-weight:800;color:var(--mut);text-decoration:none;padding:4px 9px;border-radius:6px;letter-spacing:.03em}
.langsw a.active{background:#3f4650;color:#fff}
.langsw a:hover:not(.active){background:#fff;color:var(--ink)}
/* Startseite - Neon-Konstellation */
#home .home-hero{position:relative;min-height:100vh;overflow:hidden;color:#fff;display:flex;flex-direction:column;
  background:linear-gradient(180deg,rgba(9,14,24,.66),rgba(12,17,28,.5) 45%,rgba(7,11,20,.9)),url("assets/hero.jpg") center 32%/cover no-repeat}
#home .hero-top{position:absolute;top:16px;left:18px;z-index:7;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
#home .hero-top .lsrow{display:flex;align-items:stretch;gap:8px}
#home .hero-top .lsrow .themebtn{width:33px;height:auto;align-self:stretch}
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
#home .home-hero .langsw a.active{background:#3f4650;color:#fff}
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
/* FTEM-Zonen in der echten Bergsilhouette (SVG) + transparente Klick-Streifen */
.heromt{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none}
.pyr{position:absolute;inset:0;z-index:3}
.pband{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;cursor:pointer}
.pband:hover .pb-n{transform:scale(1.06)}
.pm{top:20%;height:18%;align-items:flex-start;justify-content:flex-end;padding-left:20.5%;padding-bottom:1.5%}
.pe{top:38%;height:12%}
.pt{top:50%;height:23%}
.pf{top:73%;height:27%;justify-content:flex-start;padding-top:6.5%}
.pb-n{font-weight:800;letter-spacing:.2em;color:#fff;text-shadow:0 1px 10px rgba(0,0,0,.7);font-size:15px;transition:transform .18s}
.pt .pb-n{font-size:24px}
.pm .pb-n{font-size:14px}
.pb-s{font-size:11px;font-weight:700;color:rgba(255,255,255,.85);text-shadow:0 1px 8px rgba(0,0,0,.6);letter-spacing:.12em}
.pm .pb-s{font-size:10px;padding-left:14px}
/* Stufen-Klick -> Sportarten-Auswahl */
.pband{cursor:pointer}
.pband:hover{filter:brightness(1.18)}
.spmodal{position:fixed;inset:0;z-index:115;background:rgba(8,12,20,.68);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:18px}
.sp-box{width:min(760px,94vw);max-height:90vh;overflow:auto;background:var(--bg);border-radius:14px;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.sp-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 15px;background:var(--ink);color:#fff;font-weight:800;font-size:13px;letter-spacing:.06em}
.sp-x{background:none;border:none;color:#fff;font-size:17px;cursor:pointer;line-height:1}
.sp-x:hover{color:var(--talent)}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;padding:14px}
.sp-grid a{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 12px;text-decoration:none;color:var(--ink)}
.sp-grid a:hover{border-color:var(--red)}
.sp-grid a b{font-size:13px}
.sp-grid img,.sp-grid .spcode{width:34px;height:34px;border-radius:50%;object-fit:cover;flex:none}
.sp-grid .spcode{display:flex;align-items:center;justify-content:center;background:var(--red);color:#fff;font-size:10px;font-weight:800}
@media(max-width:760px){.pb-n{font-size:11px}.pt .pb-n{font-size:15px}.pb-s{font-size:8.5px}.pm{padding-left:4.5%;padding-bottom:0;justify-content:center}.pm .pb-n{font-size:9.5px;letter-spacing:.12em}.pm .pb-s{display:none}}
.adminlink{text-align:center;margin-top:26px}
.adminlink a{display:inline-flex;opacity:.42;text-decoration:none;transition:opacity .16s,transform .16s}
.adminlink a:hover{opacity:1;transform:translateY(-1px)}
.adminlink svg{width:22px;height:22px}
/* Meeting-Paket: Hero-Buttons, Overlays, Titel-Dropdown, Steady, Mobile-Header */
.homesport{font:inherit;font-size:12.5px;font-weight:700;color:#fff;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.22);border-radius:8px;padding:7px 10px;backdrop-filter:blur(6px);max-width:190px;cursor:pointer}
.homesport option{color:var(--ink)}
.hero-top-r{position:absolute;top:16px;right:18px;z-index:7}
.news-btn{background:var(--red);color:#fff;border:none;border-radius:8px;padding:6px 15px;font-size:11.5px;font-weight:800;letter-spacing:.04em;cursor:pointer}
.news-btn:hover{filter:brightness(1.12)}
.hero-top-r{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.info-btn{font:inherit;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.32);color:#fff;font-weight:800;font-size:11.5px;border-radius:8px;padding:6px 13px;cursor:pointer;backdrop-filter:blur(6px)}
.info-btn:hover{background:var(--red);border-color:var(--red)}
.hero-cta{display:flex;gap:10px;justify-content:center;margin-top:14px;pointer-events:auto}
.hcta{font:inherit;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.32);color:#fff;font-weight:800;font-size:13px;border-radius:20px;padding:8px 17px;cursor:pointer;backdrop-filter:blur(6px);text-decoration:none}
.hcta:hover{background:var(--red);border-color:var(--red)}
.hcta-sec{background:rgba(255,255,255,.07)}
.adminlink-hero{position:absolute;left:50%;bottom:10px;transform:translateX(-50%);z-index:7;margin:0}
.imodal{position:fixed;inset:0;z-index:112;background:rgba(8,12,20,.68);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:18px}
.im-box{width:min(900px,94vw);max-height:92vh;background:var(--bg);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.im-bar{display:flex;align-items:center;gap:10px;padding:9px 14px;background:var(--ink);color:#fff}
.im-t{font-weight:800;font-size:13px;flex:1}
.im-x{background:none;border:none;color:#fff;font-size:17px;cursor:pointer;padding:2px 8px;line-height:1}
.im-x:hover{color:var(--talent)}
.im-body{padding:16px;overflow:auto}
.im-body .news-h{display:none}
.im-body .ftem-info{margin-top:0}
.mlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.mlist .mission-item{display:block;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:13px 10px;font-weight:800;font-size:13px;color:var(--ink);text-decoration:none}
.mlist .mission-item:hover{border-color:var(--red);color:var(--red)}
header.top .sportsel2{font:inherit;font-size:15px;font-weight:800;color:var(--ink);max-width:280px;padding:6px 10px;border:1px solid var(--line);border-radius:9px;background:var(--card)}
.steady{position:fixed;right:18px;bottom:74px;z-index:95;display:flex;align-items:center;gap:9px;background:var(--red);color:#fff;border:none;border-radius:30px;padding:11px 19px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.28);animation:steadybob 3s ease-in-out infinite}
.steady:hover{filter:brightness(1.12)}
@keyframes steadybob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
body.pres .steady{display:none}
/* Versteckter Praesentationsmodus (Symbol unten wie Admin-Schloss, Passwort FTEMP) */
.preslink{text-align:center;margin-top:26px}
.presopen{background:none;border:none;font:inherit;font-size:20px;line-height:1;color:var(--mut);opacity:.42;cursor:pointer;transition:opacity .16s,transform .16s;padding:4px 8px}
.presopen:hover{opacity:1;transform:translateY(-1px)}
.presask{display:inline-flex;gap:6px;margin-left:8px;vertical-align:middle}
.presask input{font:inherit;font-size:12.5px;width:120px;padding:5px 9px;border:1px solid var(--line);border-radius:8px}
.presask input.bad{border-color:var(--red);animation:pshake .3s}
@keyframes pshake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.presask .presgo{font:inherit;font-size:12.5px;font-weight:700;padding:5px 12px;border:1px solid var(--line);border-radius:8px;background:#fff;cursor:pointer}
.presask .presgo:hover{background:var(--bg)}
body.pres{--colw:290px;--lblw:200px}
body.pres .ht-c,body.pres .chatbtn,body.pres .jump,body.pres .pdf,body.pres .hdiv,body.pres .preslink{display:none!important}
body.pres section.sport summary .tt{font-size:19px}
body.pres section.sport details.theme>summary{padding:10px 16px}
body.pres section.sport .cell .cwrap{font-size:15px;max-height:none}
body.pres section.sport .cell::after{display:none}
body.pres section.sport .more{display:none}
body.pres section.sport .rl{font-size:14px}
body.pres section.sport .c.hd .st{font-size:16px}
body.pres section.sport .c.hd .stf{font-size:11px}
body.pres section.sport h2.grp{font-size:15px}
/* App-Installations-Hinweis */
.appinstall{max-width:600px;margin:26px auto 0;display:flex;gap:15px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:15px 17px}
.appinstall .ai-icon{width:60px;height:60px;border-radius:14px;flex:none;box-shadow:0 5px 14px rgba(0,0,0,.16)}
.appinstall .ai-h{font-weight:800;font-size:14.5px;color:var(--ink);margin-bottom:4px}
.appinstall .ai-txt p{margin:0;font-size:12.5px;line-height:1.6;color:var(--mut)}
.appinstall .ai-txt b{color:var(--ink);font-weight:700}
.appinstall .ai-i{display:inline-block;transform:translateY(-1px);font-weight:800;color:var(--red)}
@media(max-width:520px){.appinstall{align-items:flex-start;padding:13px 14px;gap:12px}.appinstall .ai-icon{width:52px;height:52px}}
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
@media(max-width:640px){.node .nicon{width:58px;height:58px}.node .nhover{width:96px}.node .nlabel{font-size:12px}#home .hero-head{padding-top:128px}}
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
header.top .back{flex:none;width:33px;height:33px;display:inline-flex;align-items:center;justify-content:center;color:var(--ink);text-decoration:none;background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:0}
header.top .back svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
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
header.top input,header.top select,header.top button{font:inherit;font-size:13px;height:33px;padding:0 11px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}
header.top .langsw{height:33px;align-items:stretch;box-sizing:border-box;padding:3px}
header.top .langsw a{display:flex;align-items:center}
header.top button{cursor:pointer;font-weight:600}
header.top button:hover{background:var(--bg)}
.ht-c .qbox{position:relative;display:flex;align-items:center;width:280px;max-width:100%}
.ht-c .qbox .qic{position:absolute;left:10px;width:15px;height:15px;fill:none;stroke:var(--mut);stroke-width:2;stroke-linecap:round;pointer-events:none}
.ht-c input.q{width:100%;height:33px;padding:0 58px 0 30px}
.ht-c input.q::-webkit-search-cancel-button{-webkit-appearance:none;display:none}
.ht-c .hits{position:absolute;right:30px;top:50%;transform:translateY(-50%);font-size:11.5px;color:var(--mut);font-weight:700;white-space:nowrap;max-width:58px;overflow:hidden;text-overflow:ellipsis;pointer-events:none}
.ht-c .qx{position:absolute;right:6px;top:50%;transform:translateY(-50%);width:22px;height:22px;padding:0;border:none;background:none;color:var(--mut);font-size:17px;line-height:1;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;border-radius:50%}
.ht-c .qx:hover{color:var(--ink);background:var(--acc-bg)}
.ht-r select{width:170px}
.ht-r .toggleall{width:33px;height:33px;padding:0;display:inline-flex;align-items:center;justify-content:center;color:var(--acc)}
.ht-r .toggleall svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;transition:transform .2s}
.ht-r .toggleall.allopen svg{transform:rotate(180deg)}
.ht-r .toggleall:hover{border-color:var(--acc);color:var(--red)}
.ht-r .pdf{width:33px;height:33px;padding:0;display:inline-flex;align-items:center;justify-content:center;color:var(--acc)}
.ht-r .pdf svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ht-r .pdf:hover{border-color:var(--acc);color:var(--red)}
.ht-r .chatbtn{width:33px;height:33px;padding:0;display:inline-flex;align-items:center;justify-content:center;color:var(--red);border-color:var(--red)}
.ht-r .chatbtn svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ht-r .chatbtn svg path:last-child{fill:currentColor;stroke:none}
.ht-r .chatbtn:hover{background:var(--red);color:#fff}
.ht-r .hdiv{width:1px;height:22px;background:var(--line);flex:none;margin:0 3px}
@media print{
  @page{size:A4 landscape;margin:0}
  :root{--colw:84px;--lblw:80px}
  html,body{background:#fff}
  #home,header.top,footer,.scrolldown,.adminlink,.news,.more,.hits,.fb-btn,.fb-panel,.stagebar,.printpick,.lks{display:none!important}
  section.sport{display:block!important}
  section.sport[hidden]{display:none!important}
  .wrap{padding:8mm;max-width:none}
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
.wrap{max-width:1500px;margin:0 auto;padding:6px 18px 40px}
.intro{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:8px;font-size:13px;color:var(--mut)}
.intro b{color:var(--ink)}
.placeholder{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:64px 24px;margin-top:24px;text-align:center;color:var(--mut)}
.placeholder .big{font-size:20px;font-weight:800;color:var(--ink);margin-bottom:10px}
.placeholder code{background:var(--bg);border-radius:6px;padding:2px 6px;font-size:12px}
.legend{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}
.legend span{font-size:11.5px;padding:4px 11px;border-radius:30px;font-weight:700}
.lg-f{background:var(--found-bg);color:var(--found-t)}.lg-t{background:var(--talent-bg);color:var(--talent-t)}.lg-e{background:var(--elite-bg);color:var(--elite-t)}.lg-m{background:var(--mast-bg);color:var(--mast-t)}
.hint{font-size:12px;color:var(--mut);margin:14px 2px 2px;display:flex;align-items:center;gap:6px}
h2.grp{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--gc,var(--ink));margin:10px 0 5px;font-weight:800;display:flex;align-items:center;gap:8px}
h2.grp:first-child{margin-top:0}
.wrap>h2.grp:first-child{margin-top:6px}
h2.grp::before{content:'';width:9px;height:9px;border-radius:2px;background:var(--gc,var(--mut));flex:none}
h2.grp::after{content:'';flex:1;height:1px;background:var(--line)}
details.theme{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--acc-line);border-radius:9px;margin-bottom:3px;scroll-margin-top:66px;overflow:hidden;transition:box-shadow .16s}
details.theme:hover{box-shadow:0 5px 16px rgba(0,0,0,.08)}
details.theme[open]{box-shadow:0 6px 18px rgba(0,0,0,.06)}
details.theme>summary{cursor:pointer;padding:4px 12px;list-style:none;display:flex;align-items:center;gap:9px}
details.theme>summary:hover{background:#fafbfc}
details.theme>summary::-webkit-details-marker{display:none}
summary .ticon{flex:none;width:24px;height:24px;border-radius:7px;display:flex;align-items:center;justify-content:center}
summary .ticon svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
summary .tt{font-size:12.5px;font-weight:700;flex:1;min-width:0}
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
.cell.ph-foundation{background:#f4faf8;--zc:#0d5e6e;--zbg:#e1f0f3}.cell.ph-talent{background:#fcf8ee;--zc:#8a6a00;--zbg:#f7edcf}.cell.ph-elite{background:#fdf5ef;--zc:#a8511a;--zbg:#f8e2d3}.cell.ph-mastery{background:#fcefef;--zc:#9c1d14;--zbg:#f6dcd8}.cell.ph-multi{background:#f7f8fa;--zc:#5a6472;--zbg:#eceff3}
.cell.hl-foundation{background:#d6edf1;box-shadow:inset 0 0 0 2px var(--found)}
.cell.hl-talent{background:#faeab4;box-shadow:inset 0 0 0 2px var(--talent)}
.cell.hl-elite{background:#fbdcc6;box-shadow:inset 0 0 0 2px var(--elite)}
.cell.hl-mastery{background:#f8d2cb;box-shadow:inset 0 0 0 2px var(--mast)}
/* Sticky Stufen-Leiste (F1..M) - Inhalt einfaerben wie Spaltenkoepfe */
.stagebar{position:sticky;bottom:0;z-index:12;display:flex;gap:5px;justify-content:center;
  padding:7px 12px;padding-bottom:calc(7px + env(safe-area-inset-bottom));
  background:rgba(247,249,251,.92);backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);border-top:1px solid var(--line)}
.stagebar .sb{flex:1 1 0;min-width:0;max-width:58px;font:inherit;font-size:11.5px;font-weight:800;letter-spacing:.02em;
  color:var(--ink);background:#fff;border:1px solid var(--line);border-bottom:2.5px solid var(--phc,#b6c0cc);
  border-radius:7px;padding:6px 2px;cursor:pointer;text-align:center;transition:background .12s,color .12s,transform .08s}
.stagebar .sb:hover{background:var(--acc-bg)}
.stagebar .sb:active{transform:translateY(1px)}
.sb.ph-foundation{--phc:var(--found)}.sb.ph-talent{--phc:var(--talent)}.sb.ph-elite{--phc:var(--elite)}.sb.ph-mastery{--phc:var(--mast)}
.stagebar .sb.active{background:var(--phc);color:#fff;border-color:var(--phc)}
.stagebar .sb.ph-talent.active{color:#3b2e00}
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
/* farbige Zellen-Oberkanten entfernt (nur noch dezente Grundlinie) */
.cwrap p{margin:0 0 5px;line-height:1.5}.cwrap p:last-child{margin-bottom:0}
.cwrap .bh,.cwrap .sh{font-weight:700;color:var(--found-t);font-size:9px;text-transform:uppercase;letter-spacing:.055em;margin:12px 0 4px;line-height:1.3}
.cwrap .bh:first-child,.cwrap .sh:first-child{margin-top:0}
.cwrap .bh:not(:first-child),.cwrap .sh:not(:first-child){border-top:1px solid #e3e8ee;padding-top:10px}
.cwrap .bi{font-weight:700;color:var(--ink);font-size:11.5px;margin:0 0 3px;line-height:1.4}
/* Off-Snow / On-Snow Zonen */
.cwrap .zone{margin-top:11px}.cwrap .zone:first-child{margin-top:0}
.cwrap .zone+.zone{border-top:1px solid #e3e8ee;padding-top:10px}
.cwrap .zlab{display:inline-block;font-weight:700;font-size:9px;text-transform:uppercase;letter-spacing:.06em;color:var(--zc,#5a6472);background:var(--zbg,#eceff3);border-radius:5px;padding:2px 7px;margin:0 0 5px}
.cwrap .zsub{margin:0 0 4px;line-height:1.5}.cwrap .zsub:last-child{margin-bottom:0}
.cwrap .zk{font-weight:700;color:var(--ink)}.cwrap .zk::after{content:"·";margin:0 5px 0 4px;color:#b6c0cc;font-weight:400}
.cwrap .zsub-l .zk{display:block;margin:0 0 2px}.cwrap .zsub-l .zk::after{content:none}.cwrap .zsub-l ul{margin-top:2px}
.cwrap .lbl{font-weight:700;color:var(--found-t)}
.cwrap ul{margin:3px 0 6px;padding-left:15px}
.cwrap ul.bl li{margin-bottom:3px;line-height:1.45}
.cwrap ul.bl li::first-letter{text-transform:uppercase}
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
/* Stufen-Druck-Dialog */
.printpick{position:fixed;inset:0;z-index:60;background:rgba(15,22,34,.5);display:flex;align-items:center;justify-content:center;padding:20px}
.printpick[hidden]{display:none}
.pp-card{position:relative;background:#fff;border-radius:14px;padding:18px 18px 16px;max-width:344px;width:100%;box-shadow:0 14px 44px rgba(0,0,0,.32)}
.pp-h{font-size:14px;font-weight:800;color:var(--ink);margin:0 0 13px;padding-right:26px}
.pp-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:12px}
.pp-b{font:inherit;font-size:12.5px;font-weight:800;color:var(--ink);background:#fff;border:1px solid var(--line);border-bottom:2.5px solid var(--phc,#b6c0cc);border-radius:7px;padding:9px 0;cursor:pointer;transition:background .12s,transform .06s}
.pp-b:hover{background:var(--acc-bg)}.pp-b:active{transform:translateY(1px)}
.pp-b.ph-foundation{--phc:var(--found)}.pp-b.ph-talent{--phc:var(--talent)}.pp-b.ph-elite{--phc:var(--elite)}.pp-b.ph-mastery{--phc:var(--mast)}
.pp-all{width:100%;font:inherit;font-size:12px;font-weight:700;color:var(--acc);background:var(--acc-bg);border:none;border-radius:8px;padding:10px;cursor:pointer}
.pp-all:hover{background:var(--acc-bg2)}
.pp-x{position:absolute;top:9px;right:12px;background:none;border:none;font-size:22px;line-height:1;color:var(--mut);cursor:pointer;padding:2px 6px}
.pp-x:hover{color:var(--ink)}
/* KI-Assistent Chat-Panel */
.chatpanel{position:fixed;inset:0;z-index:70;background:rgba(15,22,34,.42);display:flex;justify-content:flex-end}
.chatpanel[hidden]{display:none}
.cp-card{width:min(430px,100%);height:100%;background:var(--card);display:flex;flex-direction:column;box-shadow:-10px 0 40px rgba(0,0,0,.28);animation:cpIn .25s ease}
@keyframes cpIn{from{transform:translateX(34px);opacity:.5}to{transform:none;opacity:1}}
.cp-head{display:flex;align-items:center;gap:10px;padding:13px 16px;border-bottom:1px solid var(--line)}
.cp-head .cp-ic{width:28px;height:28px;flex:none;border-radius:8px;background:var(--red);color:#fff;display:flex;align-items:center;justify-content:center}
.cp-head .cp-ic svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.cp-head .cp-ic svg path:last-child{fill:currentColor;stroke:none}
.cp-t{font-weight:800;font-size:14.5px;color:var(--ink);flex:1}
.cp-x{background:none;border:none;font-size:23px;line-height:1;color:var(--mut);cursor:pointer;padding:0 6px}
.cp-x:hover{color:var(--ink)}
.cp-msgs{flex:1;overflow-y:auto;padding:14px 16px;display:flex;flex-direction:column;gap:10px}
.cp-msg{max-width:90%;font-size:13px;line-height:1.5;padding:9px 12px;border-radius:13px;white-space:pre-wrap;overflow-wrap:anywhere}
.cp-msg.u{align-self:flex-end;background:#3f4650;color:#fff;border-bottom-right-radius:4px}
.cp-msg.a{align-self:flex-start;background:var(--bg);color:var(--ink);border-bottom-left-radius:4px}
.cp-msg.a a{color:var(--red);font-weight:600}
.cp-msg.think{color:var(--mut);font-style:italic}
.cp-form{display:flex;gap:8px;padding:10px 14px;border-top:1px solid var(--line)}
.cp-in{flex:1;height:40px;padding:0 12px;border:1px solid var(--line);border-radius:9px;font:inherit;font-size:13px;background:var(--card);color:var(--ink)}
.cp-in:focus{outline:none;border-color:var(--red);box-shadow:0 0 0 2px rgba(213,43,30,.14)}
.cp-send{width:40px;height:40px;flex:none;background:var(--red);color:#fff;border:none;border-radius:9px;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center}
.cp-send:hover{filter:brightness(1.08)}
.cp-send:disabled{opacity:.5;cursor:default}
.cp-note{font-size:10px;color:var(--mut);padding:2px 16px 10px;text-align:center;line-height:1.4}
@media(max-width:520px){.cp-card{width:100%}}
mark{background:#ffe08a;border-radius:2px;padding:0 1px}
.hidden{display:none!important}
footer{text-align:center;color:var(--mut);font-size:12px;padding:24px}
footer a{color:var(--red)}
/* ---------- Responsive: Tablet ---------- */
@media(max-width:1180px){
header.top{flex-wrap:wrap;height:auto;padding:8px 14px;gap:8px 10px}
.ht-l{flex:1 1 100%}
.ht-c{flex:1 1 auto;order:3}
.ht-c .qbox{width:100%;min-width:160px}
.ht-r{flex:1 1 auto;order:2;flex-wrap:wrap}
details.theme{scroll-margin-top:118px}
}
/* ---------- Responsive: Handy ---------- */
@media(max-width:760px){
:root{--colw:158px;--lblw:86px}
header.top{gap:6px 8px}
header.top .back{width:34px;height:34px;padding:0}
header.top .sicon{width:28px;height:28px}
/* Header genau 2 Zeilen: 1) Zurueck+Icon+Sportart+Sprachen  2) Suche+Springen+Chat */
.ht-r{display:contents}
.ht-l{order:1;flex:1 1 0;min-width:0}
header.top .sportsel2{flex:1 1 0;width:100%;min-width:0;font-size:14px;max-width:none}
.ht-r .langsw{order:2;flex:none}
.ht-r .themebtn{order:2;flex:none}
.ht-c{flex:1 1 55%;order:3}
.ht-c .qbox{width:100%}
.ht-c input.q{font-size:16px;padding:0 56px 0 30px}
.ht-r select.jump{order:4;flex:1 1 26%;width:auto;min-width:0;font-size:13px}
.ht-r .chatbtn{order:5;flex:none}
.ht-r .toggleall,.ht-r .pdf,.ht-r .hdiv{display:none}
.wrap{padding:10px 10px 60px}
.scroller{padding:0 8px 10px}
.rl{font-size:9.5px;padding:6px 6px;line-height:1.25;font-weight:600}
.rl{box-shadow:0 0 0 6px var(--card),-12px 0 0 6px var(--card),7px 0 8px -5px rgba(0,0,0,.22)}
.cell .cwrap{font-size:11px}
.stagebar{gap:3px;padding:5px 8px;padding-bottom:calc(5px + env(safe-area-inset-bottom))}
.stagebar .sb{font-size:10.5px;padding:6px 1px;border-bottom-width:2px;max-width:none}
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
/* ---------- Dark Mode (data-theme, automatisch + manuell umschaltbar) ---------- */
[data-theme="dark"]{--ink:#e7edf4;--mut:#98a4b3;--line:rgba(255,255,255,.11);--bg:#0d1420;--card:#172231;
 --found-t:#59c6dd;--talent-t:#f0c657;--elite-t:#f0975e;--mast-t:#f07e72;
 --found-bg:rgba(31,143,166,.16);--talent-bg:rgba(226,169,0,.15);--elite-bg:rgba(232,119,46,.15);--mast-bg:rgba(213,43,30,.16);
 --acc:#9aa6b4;--acc-line:rgba(255,255,255,.16);--acc-bg:#212d40;--acc-bg2:#2a3850}
[data-theme="dark"] header.top{background:rgba(16,24,38,.94)}
[data-theme="dark"] header.top input,[data-theme="dark"] header.top select,[data-theme="dark"] header.top button{background:#1c2740;color:var(--ink)}
[data-theme="dark"] header.top .back:hover{background:#243247;color:var(--ink)}
[data-theme="dark"] .langsw a:hover:not(.active){background:#243247;color:var(--ink)}
[data-theme="dark"] .ht-c .qx{background:none}
[data-theme="dark"] .ht-c .qx:hover{background:#243247}
[data-theme="dark"] .cell{background:#172231}
[data-theme="dark"] .cell.ph-foundation{background:#152731;--zc:#7fd6e8;--zbg:rgba(31,143,166,.20)}
[data-theme="dark"] .cell.ph-talent{background:#25220f;--zc:#f0cf72;--zbg:rgba(226,169,0,.18)}
[data-theme="dark"] .cell.ph-elite{background:#271c12;--zc:#f0a877;--zbg:rgba(232,119,46,.18)}
[data-theme="dark"] .cell.ph-mastery{background:#271413;--zc:#f09287;--zbg:rgba(213,43,30,.20)}
[data-theme="dark"] .cell.ph-multi{background:#1a2434;--zc:#aeb8c6;--zbg:rgba(255,255,255,.08)}
[data-theme="dark"] .cell.hl-foundation{background:rgba(31,143,166,.22)}
[data-theme="dark"] .cell.hl-talent{background:rgba(226,169,0,.20)}
[data-theme="dark"] .cell.hl-elite{background:rgba(232,119,46,.20)}
[data-theme="dark"] .cell.hl-mastery{background:rgba(213,43,30,.22)}
[data-theme="dark"] .cell::after{background:linear-gradient(180deg,rgba(23,34,49,0),#172231)}
[data-theme="dark"] .cwrap{color:#c2ccd8}
[data-theme="dark"] .cwrap .bh:not(:first-child),[data-theme="dark"] .cwrap .sh:not(:first-child){border-top-color:rgba(255,255,255,.10)}
[data-theme="dark"] .cwrap .zone+.zone{border-top-color:rgba(255,255,255,.10)}
[data-theme="dark"] .cwrap .zk::after{color:#5a6472}
[data-theme="dark"] .cwrap ul.sc .badge{background:#33425c;color:#e7edf4}
[data-theme="dark"] .cwrap .empty{color:#4a5568}
[data-theme="dark"] .more{background:#1c2740;color:var(--found-t);border-color:rgba(255,255,255,.14)}
[data-theme="dark"] .more:hover{background:#243247}
[data-theme="dark"] details.theme>summary:hover{background:#1c2740}
[data-theme="dark"] details.theme:hover{box-shadow:0 5px 16px rgba(0,0,0,.4)}
[data-theme="dark"] .stagebar{background:rgba(13,19,30,.92);border-top-color:rgba(255,255,255,.10)}
[data-theme="dark"] .stagebar .sb{background:#1c2740;color:var(--ink);border-color:rgba(255,255,255,.14)}
[data-theme="dark"] .stagebar .sb:hover{background:#243247}
[data-theme="dark"] .stagebar .sb.ph-foundation:not(.active){color:#6fd0e6;background:rgba(31,143,166,.15);border-color:rgba(89,198,221,.4)}
[data-theme="dark"] .stagebar .sb.ph-talent:not(.active){color:#f2c85f;background:rgba(226,169,0,.14);border-color:rgba(240,198,87,.4)}
[data-theme="dark"] .stagebar .sb.ph-elite:not(.active){color:#f2a06a;background:rgba(232,119,46,.14);border-color:rgba(240,151,94,.42)}
[data-theme="dark"] .stagebar .sb.ph-mastery:not(.active){color:#f28578;background:rgba(213,43,30,.15);border-color:rgba(240,126,114,.42)}
[data-theme="dark"] .stagebar .sb.active{background:var(--phc);color:#fff;border-color:var(--phc)}
[data-theme="dark"] .stagebar .sb.ph-talent.active{color:#3b2e00}
[data-theme="dark"] mark{color:#1d2630}
[data-theme="dark"] .pp-card{background:#172231}
[data-theme="dark"] .pp-h{color:var(--ink)}
[data-theme="dark"] .pp-b{background:#1c2740;color:var(--ink);border-color:rgba(255,255,255,.14)}
[data-theme="dark"] .pp-b:hover{background:#243247}
[data-theme="dark"] .pp-all{background:#212d40;color:var(--found-t)}
[data-theme="dark"] .pp-x{color:var(--mut)}
[data-theme="dark"] .abar{background:rgba(16,24,38,.96)}
[data-theme="dark"] .cedit{background:#141d2c;color:#e7edf4;border-color:rgba(255,255,255,.16)}
[data-theme="dark"] .cedit.changed{background:#2a1a18;border-color:var(--red)}
[data-theme="dark"] .glostab{background:#172231;border-color:rgba(255,255,255,.10)}
[data-theme="dark"] .glostab th{background:#1c2740;color:#9fb0d6}
[data-theme="dark"] .glostab td{border-top-color:rgba(255,255,255,.08)}
[data-theme="dark"] .glostab tr:hover td{background:#1c2740}
[data-theme="dark"] .glosadd{background:#172231;border-color:rgba(255,255,255,.10)}
/* diskreter Theme-Umschalter */
.themebtn{background:none;border:1px solid var(--line);border-radius:9px;width:33px;height:33px;padding:0;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;color:var(--mut);transition:color .15s,border-color .15s,background .15s}
.themebtn:hover{color:var(--ink);border-color:var(--acc-line)}
.themebtn svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.themebtn .ic-sun{display:none}
[data-theme="dark"] .themebtn .ic-sun{display:inline}
[data-theme="dark"] .themebtn .ic-moon{display:none}
#home .hero-top .themebtn{color:rgba(255,255,255,.82);border-color:rgba(255,255,255,.28)}
#home .hero-top .themebtn:hover{color:#fff;border-color:rgba(255,255,255,.5);background:rgba(255,255,255,.1)}
"""

JS = r"""
function toggleTheme(){var r=document.documentElement;var d=r.getAttribute('data-theme')==='dark'?'light':'dark';r.setAttribute('data-theme',d);try{localStorage.setItem('ftem-theme',d);}catch(e){}}
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
  const qx=sec.querySelector('.qx');
  if(qx){function qtog(){qx.hidden=!q.value;}q.addEventListener('input',qtog);qx.onclick=()=>{q.value='';qtog();run();q.focus();};}
  const toggleAll=sec.querySelector('.toggleall');
  if(toggleAll){toggleAll.onclick=()=>{const open=!toggleAll.classList.contains('allopen');themes.forEach(t=>t.open=open);toggleAll.classList.toggle('allopen',open);var lbl=toggleAll.getAttribute(open?'data-close':'data-open');toggleAll.title=lbl;toggleAll.setAttribute('aria-label',lbl);if(open)setTimeout(setupClamp,50);};}
  const pdfBtn=sec.querySelector('.pdf');
  if(pdfBtn)pdfBtn.onclick=()=>openPrintPicker(sec);
  const chatBtn=sec.querySelector('.chatbtn');
  if(chatBtn)chatBtn.onclick=()=>openChat(sec);
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
    sec.querySelectorAll('.stagebar .sb').forEach(b=>{const on=active.has(+b.dataset.si);b.classList.toggle('active',on);b.setAttribute('aria-pressed',on?'true':'false');});
    sec.querySelectorAll('.cell').forEach(c=>{
      c.classList.remove('hl-foundation','hl-talent','hl-elite','hl-mastery');
      const f=+c.dataset.from,t=+c.dataset.to;
      for(const i of active){if(i>=f&&i<=t){c.classList.add('hl-'+phaseIdx(i));break;}}
    });
  }
  function toggleStage(i){active.has(i)?active.delete(i):active.add(i);applyHl();}
  sec.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.addEventListener('click',()=>toggleStage(+h.dataset.idx)));
  sec.querySelectorAll('.stagebar .sb').forEach(b=>b.addEventListener('click',()=>toggleStage(+b.dataset.si)));
  run();
}
sections.forEach(initSport);

// ---- Stufendossier: erst Stufe waehlen, dann kompakt nur diese Stufe drucken ----
const DOSSIER_CSS = '@page{size:A4 portrait;margin:0}'
 +'body.ddoc{background:#fff!important;margin:0;padding:12mm 12mm 14mm;color:#1d2630;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}'
 +'.ds-head{border-left:5px solid #b6c0cc;padding:1px 0 9px 12px;margin:0 0 13px}'
 +'.ds-head.ph-foundation{border-color:#1f8fa6}.ds-head.ph-talent{border-color:#e2a900}.ds-head.ph-elite{border-color:#e8772e}.ds-head.ph-mastery{border-color:#d52b1e}'
 +'.ds-title{font-size:15px;font-weight:800;line-height:1.2}.ds-stage{font-size:12px;font-weight:700;color:#5a6472;margin-top:2px}'
 +'.ds-grp{font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:#5a6472;margin:13px 0 5px}'
 +'.ds-theme{break-inside:avoid;margin:0 0 8px;border:1px solid #dfe4ea;border-radius:6px;overflow:hidden}'
 +'.ds-theme h3{font-size:11.5px;font-weight:800;margin:0;padding:6px 9px;background:#f4f6f8;border-bottom:1px solid #dfe4ea;color:#1d2630}'
 +'.ds-row{display:grid;grid-template-columns:118px 1fr;gap:10px;padding:6px 9px;border-top:1px solid #eef1f4;break-inside:avoid}'
 +'.ds-row:first-of-type{border-top:none}'
 +'.ds-l{font-size:9.5px;font-weight:700;color:#39424e;line-height:1.3}'
 +'.ds-c{font-size:10px;line-height:1.42}.ds-c .cwrap{padding:0!important;max-height:none!important;overflow:visible!important;font-size:10px!important;line-height:1.42!important;color:#1d2630!important}'
 +'.ds-c .cwrap .zlab{background:#eef1f4!important;color:#4a5462!important}'
 +'.ds-empty{font-size:11px;color:#8a929c;padding:14px 2px}';

let ppSec=null;
const pick=document.createElement('div');
pick.className='printpick';pick.hidden=true;
pick.innerHTML='<div class="pp-card" role="dialog" aria-modal="true"><button class="pp-x" type="button" aria-label="'+I18N.printClose+'">&times;</button>'
  +'<div class="pp-h">'+I18N.printPick+'</div><div class="pp-grid"></div>'
  +'<button class="pp-all" type="button">'+I18N.printAll+'</button></div>';
document.body.appendChild(pick);
const ppGrid=pick.querySelector('.pp-grid');
function esc2(s){const d=document.createElement('div');d.textContent=(s==null?'':s);return d.innerHTML;}
function stageMeta(sec,i){
  const h=sec.querySelector('.c.hd[data-idx="'+i+'"]');
  const full=h?(h.querySelector('.st')||{}).textContent||'':'';
  const ph=h?([...h.classList].find(c=>c.indexOf('ph-')===0)||''):'';
  return {full:full,ph:ph};
}
function openPrintPicker(sec){
  ppSec=sec;ppGrid.innerHTML='';
  sec.querySelectorAll('.stagebar .sb').forEach(b=>{
    const i=+b.dataset.si,m=stageMeta(sec,i);
    const el=document.createElement('button');
    el.type='button';el.className='pp-b '+m.ph;el.dataset.si=i;
    el.textContent=b.textContent;el.title=m.full;
    ppGrid.appendChild(el);
  });
  pick.hidden=false;document.documentElement.style.overflow='hidden';
}
function closePrintPicker(){pick.hidden=true;document.documentElement.style.overflow='';}
pick.addEventListener('click',e=>{if(e.target===pick||e.target.closest('.pp-x'))closePrintPicker();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!pick.hidden)closePrintPicker();});
pick.querySelector('.pp-all').onclick=()=>{const s=ppSec;closePrintPicker();if(s){s.querySelectorAll('details.theme').forEach(t=>t.open=true);setTimeout(()=>window.print(),180);}};
ppGrid.addEventListener('click',e=>{const b=e.target.closest('.pp-b');if(!b||!ppSec)return;const s=ppSec,i=+b.dataset.si;closePrintPicker();setTimeout(()=>printStage(s,i),60);});
function buildDossier(sec,i){
  const sportName=(sec.querySelector('header.top h1')||{}).textContent||'';
  const m=stageMeta(sec,i);
  let out='<div class="ds-head '+m.ph+'"><div class="ds-title">'+esc2(sportName)+'</div><div class="ds-stage">'+esc2(I18N.dossier)+' · '+esc2(m.full)+'</div></div>';
  const wrap=sec.querySelector('.wrap');if(!wrap)return out+'<div class="ds-empty">–</div>';
  let any=false;
  [...wrap.children].forEach(ch=>{
    if(ch.matches&&ch.matches('h2.grp')){out+='<div class="ds-grp">'+esc2(ch.textContent)+'</div>';}
    else if(ch.matches&&ch.matches('details.theme')){
      const title=(ch.querySelector('.tt')||{}).textContent||'';
      let rows='';
      ch.querySelectorAll('.r').forEach(r=>{
        if(r.classList.contains('head'))return;
        const rl=r.querySelector('.rl');
        const label=(rl&&!rl.classList.contains('nolbl'))?rl.textContent.trim():'';
        const cell=[...r.querySelectorAll('.cell')].find(c=>i>=+c.dataset.from&&i<=+c.dataset.to);
        if(!cell)return;
        const cw=cell.querySelector('.cwrap');
        if(!cw)return;
        const clone=cw.cloneNode(true);
        clone.querySelectorAll('.lks').forEach(el=>el.remove());          // Dokument-Links raus
        clone.querySelectorAll('a').forEach(a=>a.replaceWith(document.createTextNode(a.textContent)));
        const plain=clone.textContent.trim();
        if(!plain||plain==='–')return;
        rows+='<div class="ds-row"><div class="ds-l">'+esc2(label)+'</div><div class="ds-c"><div class="cwrap">'+clone.innerHTML+'</div></div></div>';
      });
      if(rows){out+='<section class="ds-theme"><h3>'+esc2(title)+'</h3>'+rows+'</section>';any=true;}
    }
  });
  if(!any)out+='<div class="ds-empty">–</div>';
  return out;
}
function printStage(sec,i){
  const win=window.open('','_blank');
  if(!win){alert(I18N.popupBlocked);return;}
  const appcss=(document.querySelector('style')||{}).textContent||'';
  const body=buildDossier(sec,i);
  const doc=win.document;
  doc.open();
  doc.write('<!DOCTYPE html><html lang="'+document.documentElement.lang+'"><head><meta charset="utf-8"><title>'+esc2(I18N.dossier)+'</title><style>'+appcss+'</style><style>'+DOSSIER_CSS+'</style></head><body class="ddoc">'+body+'</body></html>');
  doc.close();win.focus();
  setTimeout(()=>{try{win.print();}catch(e){}},500);
}

// ---- KI-Assistent (Chat) ----
const chatPanel=document.createElement('div');
chatPanel.className='chatpanel';chatPanel.hidden=true;
chatPanel.innerHTML='<div class="cp-card" role="dialog" aria-modal="true" aria-label="'+_esc(I18N.chatTitle)+'">'
 +'<div class="cp-head"><span class="cp-ic"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.6-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M12 7.6l.85 2.05L15 10.5l-2.15.85L12 13.4l-.85-2.05L9 10.5l2.15-.85z"/></svg></span>'
 +'<span class="cp-t">'+_esc(I18N.chatTitle)+'</span><button class="cp-x" type="button" aria-label="Schliessen">&times;</button></div>'
 +'<div class="cp-msgs"></div>'
 +'<form class="cp-form"><input class="cp-in" type="text" autocomplete="off" placeholder="'+_esc(I18N.chatPh)+'"><button class="cp-send" type="submit" aria-label="Senden">&#10148;</button></form>'
 +'<div class="cp-note">'+_esc(I18N.chatNote)+'</div></div>';
document.body.appendChild(chatPanel);
const cpMsgs=chatPanel.querySelector('.cp-msgs'),cpForm=chatPanel.querySelector('.cp-form'),cpIn=chatPanel.querySelector('.cp-in'),cpSend=chatPanel.querySelector('.cp-send');
let chatSec=null,chatBusy=false;const chatHist=[];const chatWelcomed=new Set();
function openChat(sec){chatSec=sec;chatPanel.hidden=false;document.documentElement.style.overflow='hidden';
  const id=sec.dataset.sport;
  if(!chatWelcomed.has(id)){cpMsgs.innerHTML='';chatHist.length=0;addMsg('a',I18N.chatWelcome);chatWelcomed.add(id);}
  setTimeout(()=>cpIn.focus(),60);}
function closeChat(){chatPanel.hidden=true;document.documentElement.style.overflow='';}
chatPanel.addEventListener('click',e=>{if(e.target===chatPanel||e.target.closest('.cp-x'))closeChat();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!chatPanel.hidden)closeChat();});
function linkify(t){var d=document.createElement('div');d.textContent=t;var h=d.innerHTML;
  h=h.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  h=h.replace(/^\s*#{1,6}\s*(.+)$/gm,'<strong>$1</strong>');
  h=h.replace(/(https?:\/\/[^\s<)]+)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>');
  return h;}
function addMsg(role,text,think){const d=document.createElement('div');d.className='cp-msg '+role+(think?' think':'');
  if(role==='a'&&!think)d.innerHTML=linkify(text);else d.textContent=text;
  cpMsgs.appendChild(d);cpMsgs.scrollTop=cpMsgs.scrollHeight;return d;}
function gatherChatContext(sec){
  const parts=[];
  sec.querySelectorAll('details.theme').forEach(t=>{
    const title=((t.querySelector('.tt')||{}).textContent||'').trim();if(title)parts.push('## '+title);
    t.querySelectorAll('.r').forEach(r=>{if(r.classList.contains('head'))return;
      const rl=r.querySelector('.rl');const label=(rl&&!rl.classList.contains('nolbl'))?rl.textContent.trim():'';
      const seen=new Set();const txts=[];
      r.querySelectorAll('.cell .cwrap').forEach(c=>{const x=c.textContent.trim();if(x&&x!=='–'&&!seen.has(x)){seen.add(x);txts.push(x);}});
      if(txts.length){if(label)parts.push('### '+label);txts.forEach(x=>parts.push('- '+x));}
    });
  });
  let text=parts.join('\n');if(text.length>100000)text=text.slice(0,100000);
  const seenL=new Set();const links=[];
  sec.querySelectorAll('.lks a').forEach(a=>{const u=a.href;if(u&&!seenL.has(u)){seenL.add(u);links.push({t:(a.textContent||'').trim(),u:u});}});
  const name=(((sec.querySelector('header.top h1')||{}).textContent)||'').split('·')[0].trim();
  return {text:text,links:links,sport:name};
}
cpForm.addEventListener('submit',function(e){e.preventDefault();if(chatBusy||!chatSec)return;
  const qv=cpIn.value.trim();if(!qv)return;
  addMsg('u',qv);chatHist.push({role:'user',content:qv});cpIn.value='';
  chatBusy=true;cpSend.disabled=true;const thinking=addMsg('a','…',true);
  const ctx=gatherChatContext(chatSec);
  fetch('/.netlify/functions/chat',{method:'POST',headers:{'content-type':'application/json'},
    body:JSON.stringify({question:qv,context:ctx.text,links:ctx.links,sport:ctx.sport,lang:document.documentElement.lang,history:chatHist.slice(0,-1)})})
   .then(r=>r.json().then(j=>({ok:r.ok,j:j})).catch(()=>({ok:false,j:{}})))
   .then(function(res){thinking.remove();
     if(res.ok&&res.j.answer){addMsg('a',res.j.answer);chatHist.push({role:'assistant',content:res.j.answer});}
     else{addMsg('a',(res.j&&res.j.message)||I18N.chatErr);}})
   .catch(function(){thinking.remove();addMsg('a',I18N.chatErr);})
   .then(function(){chatBusy=false;cpSend.disabled=false;cpIn.focus();});
});

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

// ---- Inhalts-Overlay (News, Was ist FTEM?, Missions-Auswahl) ----
const im=document.querySelector('.imodal');
function openInfo(tplId,title){
  im.querySelector('.im-t').textContent=title;
  im.querySelector('.im-body').innerHTML=document.getElementById(tplId).innerHTML;
  im.hidden=false;
}
function closeInfo(){im.hidden=true;}
if(im){
  im.addEventListener('click',e=>{if(e.target===im)closeInfo();});
  im.querySelector('.im-x').addEventListener('click',closeInfo);
}
document.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>openInfo(b.dataset.open,b.dataset.t||'')));

// Alle externen Links (Dokumente, News, Missionen) im Iframe-Overlay oeffnen
document.addEventListener('click',e=>{
  const a=e.target.closest('.lks a, .news-link, .np-mission, .mission-item');
  if(!a)return;
  e.preventDefault();
  if(im&&!im.hidden)closeInfo();
  openMission(a.getAttribute('href'), a.dataset.title||a.textContent.replace('↗','').trim());
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&im&&!im.hidden)closeInfo();});

// ---- Sportarten-Dropdown im Titel + Steady-Chat-Knopf ----
sections.forEach(s=>{const ss=s.querySelector('.sportsel2');if(ss)ss.addEventListener('change',e=>{location.hash='#'+e.target.value;});});
const steadyBtn=document.querySelector('.steady');
if(steadyBtn)steadyBtn.addEventListener('click',()=>{const sec=sections.find(x=>!x.hidden);if(sec)openChat(sec);});

// ---- Stufen-Klick -> direkt zum Athlet:innen-Weg der im Dropdown gewaehlten Sportart ----
const homeSport=document.querySelector('.homesport');
document.querySelectorAll('.pband').forEach(bd=>{
  const go=()=>{location.hash='#'+(homeSport?homeSport.value:SPORT_IDS[0]);};
  bd.addEventListener('click',go);
  bd.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});

// ---- Versteckter Praesentationsmodus (Symbol unten, Passwort) ----
const PRES_PW='__PRES_PW__';
function presOff(){document.body.classList.remove('pres');if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});}
function presOn(){
  document.body.classList.add('pres');
  if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>{});
  const sec=sections.find(s=>!s.hidden);
  if(sec){const ths=[...sec.querySelectorAll('details.theme')];ths.forEach((t,i)=>t.open=i===0);if(ths[0])ths[0].scrollIntoView({block:'start'});if(sec.__clamp)setTimeout(sec.__clamp,80);}
}
document.querySelectorAll('.preslink').forEach(pl=>{
  const btn=pl.querySelector('.presopen'), ask=pl.querySelector('.presask'), pw=pl.querySelector('.prespw');
  btn.addEventListener('click',()=>{ask.hidden=!ask.hidden;if(!ask.hidden){pw.value='';pw.focus();}});
  function tryGo(){
    if(pw.value===PRES_PW){ask.hidden=true;presOn();}
    else{pw.classList.add('bad');setTimeout(()=>pw.classList.remove('bad'),500);pw.select();}
  }
  pl.querySelector('.presgo').addEventListener('click',tryGo);
  pw.addEventListener('keydown',e=>{if(e.key==='Enter')tryGo();});
});
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement)document.body.classList.remove('pres');});
document.addEventListener('keydown',e=>{
  if(!document.body.classList.contains('pres'))return;
  if(e.key==='Escape'){presOff();return;}
  const sec=sections.find(s=>!s.hidden); if(!sec)return;
  if(['ArrowRight','ArrowDown','PageDown','ArrowLeft','ArrowUp','PageUp'].includes(e.key)){
    e.preventDefault();
    const ths=[...sec.querySelectorAll('details.theme')];
    let idx=ths.findIndex(t=>t.open);
    const fwd=['ArrowRight','ArrowDown','PageDown'].includes(e.key);
    idx = idx<0 ? 0 : Math.min(Math.max(idx+(fwd?1:-1),0),ths.length-1);
    ths.forEach((t,i)=>t.open=i===idx);
    ths[idx].scrollIntoView({block:'start'});
    if(sec.__clamp)setTimeout(sec.__clamp,80);
  }
});

// ---- Umschalten Startseite <-> Sportart (per #hash, Zurueck-Taste funktioniert) ----
function show(id){
  closePops();
  presOff();
  sections.forEach(s=>{const sel=s.querySelector('.sportsel2');if(sel)sel.value=s.dataset.sport;});
  const stb=document.querySelector('.steady');if(stb)stb.hidden=!id;
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<script>try{document.documentElement.setAttribute("data-theme",localStorage.getItem("ftem-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"))}catch(e){}</script>
<style>
__MAINCSS__
/* ---- Admin-Zusatz ---- */
#gate{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;padding:20px;overflow:hidden;background:radial-gradient(1200px 720px at 50% -12%,#17263f,#0f1622 58%,#090d17)}
#gate::before,#gate::after{content:"";position:absolute;border-radius:50%;filter:blur(72px);opacity:.55;pointer-events:none;mix-blend-mode:screen}
#gate::before{width:520px;height:520px;left:-130px;top:-130px;background:radial-gradient(circle,#1f8fa6,transparent 70%);animation:gfloat1 16s ease-in-out infinite}
#gate::after{width:560px;height:560px;right:-150px;bottom:-170px;background:radial-gradient(circle,#e8772e,transparent 70%);animation:gfloat2 20s ease-in-out infinite}
@keyframes gfloat1{0%,100%{transform:translate(0,0)}50%{transform:translate(70px,46px)}}
@keyframes gfloat2{0%,100%{transform:translate(0,0)}50%{transform:translate(-56px,-44px)}}
.gmount{position:absolute;left:0;right:0;bottom:0;width:100%;height:230px;pointer-events:none;z-index:1}
.gatebox{position:relative;z-index:2;background:rgba(255,255,255,.06);backdrop-filter:blur(17px);-webkit-backdrop-filter:blur(17px);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:32px 30px 26px;width:374px;max-width:100%;text-align:center;color:#fff;box-shadow:0 26px 64px rgba(0,0,0,.5);animation:gIn .7s cubic-bezier(.2,.8,.2,1) both}
@keyframes gIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:none}}
.glock{width:62px;height:62px;margin:0 auto 15px;display:flex;align-items:center;justify-content:center;border-radius:17px;background:linear-gradient(150deg,rgba(255,255,255,.14),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.16);box-shadow:0 8px 22px rgba(0,0,0,.4)}
.glock svg{width:31px;height:31px}
.gtitle{font-size:27px;font-weight:800;letter-spacing:3px;margin:0;line-height:1}
.gtitle span{display:inline-block;text-shadow:0 0 20px currentColor;animation:gGlow 3.4s ease-in-out infinite}
.gtitle .fF{color:#38b6cf}.gtitle .fT{color:#f2bd1a;animation-delay:.3s}.gtitle .fE{color:#f0873d;animation-delay:.6s}.gtitle .fM{color:#e5382b;animation-delay:.9s}
@keyframes gGlow{0%,100%{filter:brightness(1)}50%{filter:brightness(1.4)}}
.gsub{color:rgba(255,255,255,.6);font-size:11.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;margin:7px 0 18px}
.gquote{margin:0 0 20px;padding:12px 15px;border-radius:12px;background:rgba(255,255,255,.05);border-left:3px solid #e2a900;text-align:left}
.gquote .gqlabel{font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase;color:#f2bd1a;margin:0 0 5px}
.gquote .gqtext{font-size:13px;line-height:1.5;color:rgba(255,255,255,.92);font-style:italic}
.gquote .gqby{display:block;font-style:normal;margin-top:5px;font-size:11px;color:rgba(255,255,255,.5)}
.gatebox input{width:100%;padding:12px 14px;border:1px solid rgba(255,255,255,.18);border-radius:11px;font-size:14px;background:rgba(255,255,255,.08);color:#fff;box-sizing:border-box;transition:border-color .15s,box-shadow .15s,background .15s}
.gatebox input::placeholder{color:rgba(255,255,255,.45)}
.gatebox input:focus{outline:none;border-color:#e2a900;box-shadow:0 0 0 3px rgba(226,169,0,.25);background:rgba(255,255,255,.13)}
.gatebox button{margin-top:14px;width:100%;background:linear-gradient(135deg,#e5382b,#c8241a);color:#fff;border:none;border-radius:11px;padding:13px;font-weight:800;font-size:14.5px;letter-spacing:.4px;cursor:pointer;transition:transform .08s,box-shadow .2s,filter .15s;box-shadow:0 8px 22px rgba(213,43,30,.4)}
.gatebox button:hover{box-shadow:0 12px 28px rgba(213,43,30,.55);filter:brightness(1.05)}
.gatebox button:active{transform:translateY(1px)}
.gateerr{color:#ff9c91;font-size:12.5px;margin-top:11px;min-height:16px;font-weight:700}
@media(prefers-reduced-motion:reduce){#gate::before,#gate::after,.gatebox,.gtitle span{animation:none!important}}
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
<div id="gate">
  <svg class="gmount" viewBox="0 0 1440 230" preserveAspectRatio="none" aria-hidden="true">
    <polygon points="0,230 250,74 520,230" fill="#1f8fa6" opacity=".16"/>
    <polygon points="290,230 620,28 950,230" fill="#e2a900" opacity=".17"/>
    <polygon points="700,230 1000,92 1300,230" fill="#e8772e" opacity=".16"/>
    <polygon points="1040,230 1330,52 1440,188 1440,230" fill="#d52b1e" opacity=".16"/>
  </svg>
  <form id="gateform" class="gatebox">
    <div class="glock">
      <svg viewBox="0 0 24 24" fill="none" stroke="url(#ftemlock)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <defs><linearGradient id="ftemlock" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#38b6cf"/><stop offset=".38" stop-color="#f2bd1a"/><stop offset=".7" stop-color="#f0873d"/><stop offset="1" stop-color="#e5382b"/></linearGradient></defs>
        <rect x="4.6" y="10.4" width="14.8" height="10.2" rx="2.4"/>
        <path d="M8 10.4V7.4a4 4 0 0 1 8 0v3"/>
        <circle cx="12" cy="15" r="1.55" fill="url(#ftemlock)" stroke="none"/>
      </svg>
    </div>
    <div class="gtitle"><span class="fF">F</span><span class="fT">T</span><span class="fE">E</span><span class="fM">M</span></div>
    <div class="gsub">Admin &middot; Inhalte bearbeiten</div>
    <div class="gquote"><div class="gqlabel">Spruch des Tages</div><div class="gqtext" id="gqtext"></div></div>
    <input id="gatepw" type="password" placeholder="Passwort" autocomplete="current-password">
    <button type="submit">Anmelden</button>
    <div id="gateerr" class="gateerr"></div>
  </form>
</div>
<div id="app" hidden>
  <header class="abar">
    <h1><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d52b1e" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:5px" aria-hidden="true"><rect x="4.6" y="10.4" width="14.8" height="10.2" rx="2.4"/><path d="M8 10.4V7.4a4 4 0 0 1 8 0v3"/></svg>FTEM &ndash; Inhalte bearbeiten</h1>
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
// Spruch des Tages (nach Kalendertag rotierend)
var FTEM_QUOTES=[
 {t:"Erfolg ist die Summe kleiner Anstrengungen, Tag für Tag wiederholt.",b:""},
 {t:"Wer aufhört besser zu werden, hat aufgehört gut zu sein.",b:""},
 {t:"Fällst du siebenmal, steh achtmal auf.",b:"Japanisches Sprichwort"},
 {t:"Der Weg ist das Ziel.",b:"Konfuzius"},
 {t:"Was du heute trainierst, bist du morgen.",b:""},
 {t:"Die härtesten Trainings machen die leichtesten Wettkämpfe.",b:""},
 {t:"Jeder Champion war einmal ein Anfänger, der nicht aufgegeben hat.",b:""},
 {t:"Kleine Fortschritte sind auch Fortschritte.",b:""},
 {t:"Talent eröffnet die Tür – Disziplin geht hindurch.",b:""},
 {t:"Nicht die Stärke entscheidet, sondern die Ausdauer.",b:""},
 {t:"Form ist vergänglich, Klasse bleibt bestehen.",b:""},
 {t:"Motivation bringt dich in Gang, Gewohnheit hält dich am Laufen.",b:""},
 {t:"Der beste Athlet ist der, der mit dem Gestern nie zufrieden ist.",b:""},
 {t:"Gib niemals auf, denn genau hier und jetzt beginnt der Wandel.",b:""},
 {t:"Ein Ziel ohne Plan ist nur ein Wunsch.",b:""},
 {t:"Aus jedem Sturz im Schnee wächst die nächste sichere Kurve.",b:""},
 {t:"Vertraue dem Prozess – grosse Wege beginnen mit kleinen Schritten.",b:""},
 {t:"Wer die Grundlagen liebt, meistert das Schwere.",b:""}
];
(function(){
  var el=document.getElementById('gqtext'); if(!el)return;
  var now=new Date();
  var doy=Math.floor((now-new Date(now.getFullYear(),0,0))/864e5);
  var q=FTEM_QUOTES[doy%FTEM_QUOTES.length];
  el.textContent='«'+q.t+'»';
  if(q.b){var by=document.createElement('span');by.className='gqby';by.textContent='— '+q.b;el.appendChild(by);}
})();
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
    imodal = ('<div class="imodal" hidden><div class="im-box">'
              '<div class="im-bar"><span class="im-t"></span>'
              '<button class="im-x" type="button" aria-label="schliessen">✕</button></div>'
              '<div class="im-body"></div></div></div>')
    assist_lbl = {"de": "FTEM-Assistent", "fr": "Assistant FTEM", "it": "Assistente FTEM"}[lang]
    steady_btn = '<button class="steady" type="button" hidden>💬 '+esc(assist_lbl)+'</button>'
    body = home_html(datamap, lang) + "".join(sport_section(s, datamap[s["id"]], lang) for s in SPORTS) + mmodal + imodal + steady_btn
    i18n = {"more": tr("mehr ▾", lang), "less": tr("weniger ▴", lang),
            "themes": tr("Themen · F1–M", lang), "hits": tr("Themen mit Treffern", lang),
            "hitsWord": {"de": "Treffer", "fr": "résultats", "it": "risultati"}[lang],
            "noHits": {"de": "keine Treffer", "fr": "aucun résultat", "it": "nessun risultato"}[lang],
            "printPick": {"de": "Stufe für das Dossier wählen", "fr": "Choisir le niveau pour le dossier", "it": "Scegli il livello per il dossier"}[lang],
            "printAll": {"de": "Ganze Sportart (Querformat)", "fr": "Tout le sport (paysage)", "it": "Tutto lo sport (orizzontale)"}[lang],
            "printClose": {"de": "Schliessen", "fr": "Fermer", "it": "Chiudi"}[lang],
            "dossier": {"de": "Stufendossier", "fr": "Dossier de niveau", "it": "Dossier di livello"}[lang],
            "popupBlocked": {"de": "Bitte Pop-ups für diese Seite erlauben, um das Dossier zu drucken.", "fr": "Veuillez autoriser les pop-ups pour imprimer le dossier.", "it": "Consenti i pop-up per stampare il dossier."}[lang],
            "chatTitle": {"de": "FTEM-Assistent", "fr": "Assistant FTEM", "it": "Assistente FTEM"}[lang],
            "chatPh": {"de": "Frage zum Athlet:innen-Weg…", "fr": "Question sur le parcours…", "it": "Domanda sul percorso…"}[lang],
            "chatWelcome": {"de": "Hallo! Ich beantworte Fragen zum Athlet:innen-Weg dieser Sportart und verweise dich auf passende verlinkte Dokumente. Was möchtest du wissen?", "fr": "Bonjour ! Je réponds aux questions sur le parcours des athlètes de ce sport et vous oriente vers les documents liés pertinents. Que voulez-vous savoir ?", "it": "Ciao! Rispondo alle domande sul percorso degli atleti di questo sport e ti indico i documenti collegati pertinenti. Cosa vuoi sapere?"}[lang],
            "chatErr": {"de": "Es gab ein Problem beim Beantworten. Bitte später erneut versuchen.", "fr": "Un problème est survenu. Veuillez réessayer plus tard.", "it": "Si è verificato un problema. Riprova più tardi."}[lang],
            "chatNote": {"de": "Antworten basieren auf den FTEM-Inhalten dieser Sportart und den verlinkten Dokumenten. Keine Rechtsberatung.", "fr": "Les réponses se basent sur les contenus FTEM de ce sport et les documents liés.", "it": "Le risposte si basano sui contenuti FTEM di questo sport e sui documenti collegati."}[lang]}
    js = (JS.replace("__SPORT_IDS__", json.dumps([s["id"] for s in SPORTS]))
            .replace("__I18N__", json.dumps(i18n, ensure_ascii=False))
            .replace("__SUPA_URL__", SUPABASE_URL).replace("__SUPA_KEY__", SUPABASE_ANON_KEY)
            .replace("__PRES_PW__", PRES_PW))
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
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">'
        '<title>FTEM – '+esc(tr("Athlet:innen-Weg", lang))+'</title>'
        +head_meta+
        # setzt Theme früh (gespeicherte Wahl oder Systemeinstellung) + verhindert Aufblitzen
        '<script>try{document.documentElement.setAttribute("data-theme",localStorage.getItem("ftem-theme")||(matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light"))}catch(e){}'
        'if(location.hash)document.documentElement.classList.add("h");'
        'try{if(sessionStorage.ftemSeen)document.documentElement.classList.add("noanim");sessionStorage.ftemSeen=1}catch(e){}</script>'
        '<style>'+CSS+'</style></head>'
        '<body>'+body+'<script>'+js+'</script>'
        '<script>if("serviceWorker"in navigator){addEventListener("load",function(){navigator.serviceWorker.register("sw.js").catch(function(){})})}</script>'
        '</body></html>')
    out = os.path.join(BASE, FILES[lang])
    open(out,"w",encoding="utf-8").write(page)
    print("written", FILES[lang], len(page.encode("utf-8")), "bytes")

open(os.path.join(BASE, "admin.html"), "w", encoding="utf-8").write(admin_html(datamap))
print("written admin.html")

# ---- PWA Service Worker (Offline) + SEO-Dateien ----
def _write_pwa_seo():
    import hashlib, glob as _glob
    # Cache-Version aus Inhalts-Hash -> bricht Cache bei jedem echten Deploy
    h = hashlib.sha1()
    for f in ["index.html","fr.html","it.html"]:
        p = os.path.join(BASE, f)
        if os.path.exists(p): h.update(open(p,"rb").read())
    ver = h.hexdigest()[:10]
    core = ["./","./index.html","./fr.html","./it.html","./admin.html",
            "./manifest.webmanifest","./assets/favicon.svg","./assets/icon-192.png",
            "./assets/icon-512.png","./assets/icon-180.png","./assets/hero.jpg",
            "./assets/og-image.jpg","./assets/swiss-ski-logo.svg"]
    core += ["./"+p.replace("\\","/") for p in _glob.glob("assets/sporticons/*.png")]
    sw = (
        'const CACHE="ftem-'+ver+'";\n'
        'const CORE='+json.dumps(core)+';\n'
        'self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));});\n'
        'self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});\n'
        'self.addEventListener("fetch",e=>{const req=e.request;if(req.method!=="GET")return;const url=new URL(req.url);if(url.origin!==location.origin)return;\n'
        '  e.respondWith(caches.open(CACHE).then(async c=>{const cached=await c.match(req);const net=fetch(req).then(res=>{if(res&&res.status===200)c.put(req,res.clone());return res;}).catch(()=>cached);return cached||net;}));});\n'
    )
    open(os.path.join(BASE,"sw.js"),"w",encoding="utf-8").write(sw)
    print("written sw.js (cache ftem-"+ver+")")

    base = SITE_URL.rstrip("/") if SITE_URL else ""
    urls = ""
    for fn in FILES.values():
        loc = (base+"/"+fn) if base else fn
        alts = "".join('<xhtml:link rel="alternate" hreflang="'+lg+'" href="'+((base+"/"+f2) if base else f2)+'"/>'
                       for lg,f2 in FILES.items())
        urls += ('<url><loc>'+loc+'</loc>'+alts+
                 '<xhtml:link rel="alternate" hreflang="x-default" href="'+((base+"/index.html") if base else "index.html")+'"/>'
                 '<changefreq>monthly</changefreq></url>')
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
               'xmlns:xhtml="http://www.w3.org/1999/xhtml">'+urls+'</urlset>')
    open(os.path.join(BASE,"sitemap.xml"),"w",encoding="utf-8").write(sitemap)
    robots = ("User-agent: *\nAllow: /\nDisallow: /admin.html\n"
              + (("Sitemap: "+base+"/sitemap.xml\n") if base else ""))
    open(os.path.join(BASE,"robots.txt"),"w",encoding="utf-8").write(robots)
    print("written sitemap.xml, robots.txt")

_write_pwa_seo()

print("Sportarten mit Inhalt:", ", ".join(ids_with_data) or "-")
