import os
# -*- coding: utf-8 -*-
import json, re, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))

def asset_v(rel):
    """Asset-URL mit Inhalts-Hash (?v=...) - netlify.toml cached /assets/* ein Jahr
    "immutable"; ohne neuen URL-Parameter kaemen geaenderte Bilder nie bei den Nutzern an."""
    import hashlib as _hl
    p = os.path.join(BASE, rel)
    try:
        return rel + "?v=" + _hl.sha1(open(p, "rb").read()).hexdigest()[:8]
    except OSError:
        return rel


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
LANGS = ["de", "fr", "it", "en"]
FILES = {"de": "index.html", "fr": "fr.html", "it": "it.html", "en": "en.html"}

# --- Admin-Bereich -----------------------------------------------------------
# Passwort fuer den Admin-/Bearbeitungsbereich (dezentes Schloss-Icon unten auf der Startseite)
ADMIN_PW = "ftem26*"
# Passwort fuer den versteckten Praesentationsmodus (dezentes ⛶-Symbol unten auf den Sportseiten)
PRES_PW = "FTEMP"
# Uebergeordnete Mission-Seite (Link folgt). Solange leer, oeffnet der Mission-Button
# eine Auswahl der Sportarten-Missionen (aus ftem_sports.json).
MISSION_URL = ""
PRES_TITLE = {"de": "Präsentationsmodus", "fr": "Mode présentation", "it": "Modalità presentazione", "en": "Presentation mode"}
PRES_PWPH = {"de": "Passwort", "fr": "Mot de passe", "it": "Password", "en": "Password"}
# Cloud-Speicher (Supabase) fuer direkt gespeicherte, fuer alle sichtbare Aenderungen.
# Einmalig eintragen (siehe SETUP-ADMIN.md). Solange leer: Seite laeuft normal,
# Admin bietet dann Datei-Download als Rueckfall.
SUPABASE_URL = "https://xphbwnzyebbejsdeqled.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_"

# Live-Adresse der Seite (Netlify), z. B. "https://ftem-projekt.netlify.app".
# Wird fuer das Teilen-Vorschaubild (Open Graph) als absolute Bild-URL genutzt.
# Leer lassen = relative URL (funktioniert bei vielen, aber nicht allen Diensten).
SITE_URL = "https://ftemschneesport.netlify.app"

# Englische UI-Texte fuer tr()-Aufrufe (Inhalte aus den Excels bleiben vorerst deutsch)
TR_EN_UI = {
    "Athlet:innen-Weg": "Athlete pathway",
    "Zu Thema springen…": "Jump to topic…",
    "mehr ▾": "more ▾",
    "weniger ▴": "less ▴",
    "Spalte hervorheben": "Highlight column",
    "Stufe hervorheben": "Highlight stage",
    "Drucken / als PDF speichern": "Print / save as PDF",
    "Quelle:": "Source:",
    "aufbereitet am": "prepared on",
    "Themen mit Treffern": "Topics with hits",
    "Themen · F1–M": "Topics · F1–M",
    "Sport & Athlet:in": "Sport & athlete",
    "Material": "Equipment",
    "Strukturen & Umfeld": "Structures & environment",
}

def tr(s, lang):
    if lang == "de" or s is None:
        return s
    if lang == "en":
        return TR_EN_UI.get(s, TR.get("en", {}).get(s, s))
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
 "en": {
   "title": "What is FTEM?",
   "lead": 'FTEM is the shared framework of <b>Swiss Olympic</b> and <b>Swiss-Ski</b> for long-term athlete and sport development in snow sports. It describes the entire journey – from the first contact with snow to the world class – in four key phases and ten development stages (F1–M).',
   "phases": [
     ("F","Foundation","F1–F3","Building the foundation: acquiring, applying and consolidating versatile movement and snow-sport basics."),
     ("T","Talent","T1–T4","Showing and developing potential: talents confirm themselves, train purposefully and achieve the breakthrough."),
     ("E","Elite","E1–E2","Representing Switzerland internationally: World Cup, World Championships and Olympic Games at elite level."),
     ("M","Mastery","M","Shaping the world class: sustained success at the highest level over years."),
   ],
 },
}
PLACE = {
 "de": 'Der Athlet:innen-Weg für <b>{name}</b> ist noch nicht erfasst – Inhalte folgen.<br><br>Sobald die Daten vorliegen, kommen sie in die Datei <code>{file}</code> und die Seite wird mit <code>python3 build.py</code> neu erzeugt.',
 "fr": 'Le parcours de l&#x27;athlète pour <b>{name}</b> n&#x27;est pas encore saisi – contenus à venir.<br><br>Dès que les données seront disponibles, elles seront ajoutées au fichier <code>{file}</code> et la page sera régénérée avec <code>python3 build.py</code>.',
 "it": 'Il percorso dell&#x27;atleta per <b>{name}</b> non è ancora disponibile – contenuti in arrivo.<br><br>Non appena i dati saranno disponibili, verranno inseriti nel file <code>{file}</code> e la pagina sarà rigenerata con <code>python3 build.py</code>.',
 "en": 'The athlete pathway for <b>{name}</b> is not yet available – content coming soon.<br><br>Once the data is available, it will be added to <code>{file}</code> and the page rebuilt with <code>python3 build.py</code>.',
}
HOME_SUB = {
 "de": "Swiss-Ski Entwicklungsstufen F1–M · Sportart auswählen",
 "fr": "Niveaux de développement Swiss-Ski F1–M · Choisir un sport",
 "it": "Livelli di sviluppo Swiss-Ski F1–M · Scegliere lo sport",
 "en": "Swiss-Ski development stages F1–M · Choose a sport",
}
NODATA = {"de": "Inhalte folgen", "fr": "Contenus à venir", "it": "Contenuti in arrivo", "en": "Content coming soon"}
BACK = {"de": "← Sportarten", "fr": "← Sports", "it": "← Sport", "en": "← Sports"}
BACK_TITLE = {"de": "Zurück zur Auswahl", "fr": "Retour à la sélection", "it": "Torna alla selezione", "en": "Back to selection"}
SEARCH_PH = {"de": "Suche…", "fr": "Rechercher…", "it": "Cerca…", "en": "Search…"}
EXPAND_ALL = {"de": "Alle öffnen", "fr": "Tout ouvrir", "it": "Apri tutto", "en": "Open all"}
COLLAPSE_ALL = {"de": "Alle schliessen", "fr": "Tout fermer", "it": "Chiudi tutto", "en": "Close all"}
CLEAR_LBL = {"de": "Leeren", "fr": "Effacer", "it": "Cancella", "en": "Clear"}
CHAT_BTN = {"de": "FTEM-Coach (KI)", "fr": "Coach FTEM (IA)", "it": "Coach FTEM (IA)", "en": "FTEM Coach (AI)"}

FULL = {"F1":"Foundation 1","F2":"Foundation 2","F3":"Foundation 3","T1":"Talent 1","T2":"Talent 2","T3":"Talent 3","T4":"Talent 4","E1":"Elite 1","E2":"Elite 2","M":"Mastery"}
# Fallback, falls eine Datendatei keine "ages" enthaelt (Alterskategorien pro Sportart)
AGE = {"F1":"U8","F2":"U8–U10","F3":"U10–U12","T1":"U12–U14","T2":"U14–U16","T3":"U16+","T4":"U18+","E1":"","E2":"","M":""}
GROUP_ORDER = ["Sport & Athlet:in","Material","Strukturen & Umfeld"]

def ph(st): return "foundation" if st[0]=="F" else "talent" if st[0]=="T" else "elite" if st[0]=="E" else "mastery"
def esc(s): return html.escape(s, quote=True)

# "FTEM" in den vier Phasenfarben (Anpassung von Luca, Commit "Farben FTEM")
FTEM = '<span class="fF">F</span><span class="fT">T</span><span class="fE">E</span><span class="fM">M</span>'

SC_RE = re.compile(r'^(SC\s?\d+[a-z]?|SC|ST\s?\d*|ST)\s*[:.\)]\s*(.*)$', re.S)

# Einheitliche Titel-Erkennung (ueber alle Themen/Sportarten/Stufen gleich)
# "Label: Wert" nur mit Leerzeichen nach dem Doppelpunkt -> schuetzt Gender-Doppelpunkt
# (z.B. "Trainer:innen", "Athlet:innen" werden NICHT als Label erkannt).
LABELVAL_RE = re.compile(r'^([^:\n]{2,44}):[ \t\xa0]+(\S.*)$', re.S)

def _is_title_label(lab):
    lab = (lab or "").strip()
    if len(lab) < 2 or len(lab) > 44: return False
    if not (lab[0].isalpha() and lab[0].isupper()): return False   # Titel beginnen gross
    if lab.endswith((".", "!", "?")) or ". " in lab: return False  # keine ganzen Saetze
    return True

def _is_head_line(s):
    s = (s or "").strip()
    if len(s) < 2 or len(s) > 50: return False
    if s.endswith((".", ",", ";", "!", "?", ":")): return False
    if "," in s or ":" in s: return False
    if not (s[0].isalpha() and s[0].isupper()): return False       # Zahlen/Werte beginnen nicht gross
    return len(s.split()) <= 6

def _bodyhtml(txt):
    txt = (txt or "").strip()
    if not txt: return ""
    bl = bullets_from_text(txt)
    if bl: return bl
    return '<p>'+esc(txt).replace("\n", "<br>")+'</p>'

def render_block(block, link_texts):
    b = block.strip()
    if not b: return ""
    if b in link_texts:  # pure link-label token, shown as button instead
        return ""
    # "ON SNOW" / "OFF SNOW" als Kopfzeile -> Zonen-Chip wie im Athlet:innen-Weg
    _l0 = b.split("\n", 1)
    if _SNOW_RE.match(_l0[0].strip()):
        return _snow_zone_html(_l0[0].strip(), _l0[1] if len(_l0) > 1 else "")
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
    ne = [l.strip() for l in lines if l.strip()]
    # Fall A: mehrere "Label: Wert"-Zeilen -> jede Zeile Titel + Wert (z.B. Rot/Gelb/Gruen)
    ms = [LABELVAL_RE.match(l) for l in ne]
    if len(ne) >= 2 and all(ms) and all(_is_title_label(m.group(1)) for m in ms):
        out = ""
        for m in ms:
            out += '<p class="bh">'+esc(m.group(1).strip())+'</p>'
            val = m.group(2).strip()
            if val: out += '<p>'+esc(val)+'</p>'
        return out
    first = lines[0].strip()
    # Fall B: erste Zeile "Label: Wert" -> Titel + (Wert & restliche Zeilen als Text)
    mf = LABELVAL_RE.match(first)
    if mf and _is_title_label(mf.group(1)):
        head = mf.group(1).strip()
        rest = "\n".join([mf.group(2).strip()] + list(lines[1:])).strip()
        return '<p class="bh">'+esc(head)+'</p>'+_bodyhtml(rest)
    # Fall C: erste Zeile endet mit ":" -> reine Titelzeile + Rest
    if first.endswith(":") and 2 <= len(first) <= 60 and first[:1].isupper():
        head = first[:-1].strip()
        if head:
            return '<p class="bh">'+esc(head)+'</p>'+_bodyhtml("\n".join(lines[1:]))
    # Fall D: kurze Titelzeile ohne Satzzeichen + Rest als Text
    if len(lines) >= 2 and _is_head_line(first):
        return '<p class="bh">'+esc(first)+'</p>'+_bodyhtml("\n".join(lines[1:]))
    # Fall E: einzelne kurze Titel-Phrase (z.B. "Familie", "Belastungsvertraeglichkeit aufbauen")
    if len(ne) == 1 and _is_head_line(ne[0]):
        return '<p class="bh">'+esc(ne[0])+'</p>'
    return _bodyhtml(b)

def clean_ws(s):
    # nur fuer die Anzeige: Tabs zu Leerzeichen, Mehrfach-Leerzeichen und
    # riesige Luecken zusammenfassen, Zeilenenden trimmen. Absaetze (\n\n) bleiben.
    s = s.replace("\t", " ")
    lines = [re.sub(r" {2,}", " ", ln).rstrip() for ln in s.split("\n")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()

# Off-Snow / On-Snow Zonen-Gruppierung: "Ziele Off-Snow: ..." -> Zone "Off-Snow"
ZONE_RE = re.compile(r'^(.{1,20}?)\s+(Off-Snow|On-Snow)\s*[:.]\s*(.*)$', re.S)

# "ON SNOW"/"OFF SNOW" als eigenstaendige Kopfzeile (Startseiten-Popups) -> gleicher Chip-Look
_SNOW_RE = re.compile(r'^(on|off)[\s -]?snow:?$', re.I)

def _snow_zone_html(first, rest):
    lab = 'On-Snow' if first.strip().lower().startswith('on') else 'Off-Snow'
    items, other = [], []
    for l in (rest or "").split("\n"):
        ls = l.strip()
        if not ls: continue
        if ls[:1] in "-–•":
            items.append(ls.lstrip("-–•").strip())
        elif items:
            items[-1] += " " + ls      # Zeilenumbruch innerhalb eines Punkts
        else:
            other.append(ls)
    body = ""
    if other: body += '<p>'+esc(" ".join(other))+'</p>'
    if items: body += '<ul class="bl">'+"".join('<li>'+esc(i)+'</li>' for i in items if i)+'</ul>'
    if not body and (rest or "").strip(): body = _bodyhtml(rest)
    return '<div class="zone"><span class="zlab">'+lab+'</span>'+body+'</div>'

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

def fnv36(s):
    """FNV-1a (32 Bit, base36) - identisch zur JS-Version (Math.imul). Fingerabdruck
    des deutschen Quelltexts: Overrides, die dem Quelltext entsprechen, werden im
    Frontend ignoriert (sie wuerden sonst die Uebersetzungen ueberdecken)."""
    h = 0x811C9DC5
    for _c in s:
        h ^= ord(_c)
        h = (h * 0x01000193) & 0xFFFFFFFF
    if h == 0: return "0"
    _d = "0123456789abcdefghijklmnopqrstuvwxyz"; _r = ""
    while h: _r = _d[h % 36] + _r; h //= 36
    return _r

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
    cidattr = (' data-cid="'+esc(cid)+'" data-bh="'+fnv36(seg.get("v") or "")+'"') if cid else ''
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
# Einheitlich neutral (Feedback Bjoern: keine unterschiedlichen/blauen Titel-Farben)
GROUP_COLORS = {
    "Sport & Athlet:in":    ("#4a5563", "rgba(74,85,99,.13)"),
    "Material":             ("#4a5563", "rgba(74,85,99,.13)"),
    "Strukturen & Umfeld":  ("#4a5563", "rgba(74,85,99,.13)"),
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
 "rom": '<path d="M12 19 5 12.5M12 19l7-6.5"/><path d="M5.5 10.5a9 9 0 0 1 13 0"/><path d="M5.5 10.5l.2-2.7M5.5 10.5l2.7.4M18.5 10.5l-.2-2.7M18.5 10.5l-2.7.4"/><circle cx="12" cy="19" r="1.4" fill="currentColor" stroke="none"/>',
 "barbell": '<path d="M2 12h2M20 12h2M4 9v6M20 9v6M7 7.5v9M17 7.5v9M7 12h10"/>',
 "bolt": '<path d="M13 3 4 14h6l-1 7 9-11h-6l1-7z"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
 "box": '<path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/>',
 "trophy": '<path d="M8 4h8v5a4 4 0 0 1-8 0V4z"/><path d="M8 6H5.5a2 2 0 0 0 2.5 3M16 6h2.5a2 2 0 0 1-2.5 3"/><path d="M10 15h4M9 20h6M11 15l-1 5M13 15l1 5"/>',
 "flag": '<path d="M6 21V4M6 4h12l-2.5 4L18 12H6"/>',
 "carve": '<path d="M8.5 3c7.5 2.5-7.5 6.5 0 9s-7.5 6.5 0 9"/><path d="M17 4.5v6.5"/><path d="M17 4.5l4 1.5-4 1.6"/>',
 "slzigzag": '<path d="M6 4l12 4L6 12l12 4-12 4"/>',
 "gscurve": '<path d="M5 4c13 2 13 6.5 7 8s-6 6.5 7 8"/>',
 "speedarrow": '<path d="M6 5l13 11.5"/><path d="M19 16.5l-3.7-.2M19 16.5l-.2-3.7"/><path d="M4 11.5l3.6 3.2M3.5 16.2l2.7 2.4"/>',
 "funnel": '<path d="M4 5h16l-6.2 7v5.6l-3.6 2.4v-8L4 5z"/>',
 "podium": '<rect x="9" y="9" width="6" height="11"/><rect x="3" y="13" width="6" height="7"/><rect x="15" y="15" width="6" height="5"/><path d="M12 3v3M10.6 4.5h2.8"/>',
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
 (("mobilit","beweglich","flexib"),"rom"),
 (("kraft","explosiv","power"),"barbell"),
 # Disziplin-spezifische Technik-&-Taktik-Themen VOR dem generischen carve-Icon
 # ("riesenslalom" vor "slalom" pruefen – der String enthaelt "slalom"!)
 (("riesenslalom",),"gscurve"),
 (("slalom",),"slzigzag"),
 (("sg/dh","speed (sg"),"speedarrow"),
 (("technik","taktik"),"carve"),
 (("schnellig","agilit","speed"),"bolt"),
 (("material","ausrüst","ausruest"),"box"),
 (("förderge","foerderge","gefäss","gefaess","kader","talentpool"),"trophy"),
 (("selekt",),"funnel"),
 (("förderstruktur","foerderstruktur","wettkampf","wettkämpf","wettkaempf","rennen"),"podium"),
 (("umfeld","eltern","schule","beruf","management","betreu"),"users"),
]
def theme_icon(title):
    t = (title or "").lower()
    for keys, name in _KEYMAP:
        if any(k in t for k in keys):
            return '<svg viewBox="0 0 24 24" aria-hidden="true">'+_ICONS[name]+'</svg>'
    return '<svg viewBox="0 0 24 24" aria-hidden="true">'+_ICONS["list"]+'</svg>'

def theme_html(t, idx, stages, prefix, lang, ages, edit=False, group=None, alt=False):
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
        # Gleiche benachbarte Zellen werden ueber Phasen hinweg zu einem Block verbunden
        # (nicht nur innerhalb F/T/E/M) – so entsteht bei identischem Inhalt eine Spalte.
        for si, seg in enumerate(merge_same_segs(r["segs"])):
            span = seg["to"] - seg["from"] + 1
            cls = "ph-"+ph(stages[seg["from"]])
            # Phasenuebergreifende Zellen: Farbverlauf ueber die enthaltenen Phasen
            phs = set(ph(stages[i]) for i in range(seg["from"], seg["to"]+1))
            grad = ""
            if len(phs) > 1:
                cls = "ph-multi"
                PHR = [("foundation",0,2,"--phf"),("talent",3,6,"--pht"),("elite",7,8,"--phe"),("mastery",9,9,"--phm")]
                a, b = seg["from"], seg["to"]; w = float(b - a + 1)
                stops = []
                for _nm, s0, s1, var in PHR:
                    if s1 < a or s0 > b: continue
                    cen = ((max(s0, a) + min(s1, b)) / 2.0 - a + 0.5) / w * 100.0
                    stops.append("var("+var+") %.0f%%" % cen)
                grad = "--mg:linear-gradient(90deg,"+",".join(stops)+");"
            cid = prefix+"|"+str(idx)+"|"+str(ri)+"|"+str(si)
            more = '' if edit else '<button class="more" hidden>'+esc(tr("mehr ▾", lang))+'</button>'
            body += '<div class="c cell '+cls+'" data-from="'+str(seg["from"])+'" data-to="'+str(seg["to"])+'" style="'+grad+'grid-column: span '+str(span)+'"><div class="cwrap">'+render_cell(seg, lang, cid, edit)+'</div>'+more+'</div>'
        body += '</div>'
    opn = ''  # auch im Bearbeitungsmodus eingeklappt starten (schnelleres Navigieren)
    if edit:
        # Titel des Abschnitts im Admin als eigenes Feld (cid: sport|ti|title)
        tt_span = '<span class="tt">'+esc(title)+'</span>'
        tfield = ('<div class="adm-home adm-title">'
                  + _adm_field("Titel des Abschnitts", prefix+"|"+str(idx)+"|title", t["title"])
                  + '</div>')
    else:
        tt_span = ('<span class="tt ovr-txt" data-cid="'+prefix+'|'+str(idx)+'|title" data-bh="'+fnv36(t["title"] or "")+'">'+esc(title)+'</span>')
        tfield = ''
    return ('<details class="theme'+(' edit' if edit else '')+(' alt' if alt else '')+'"'+opn+' id="'+prefix+'-t'+str(idx)+'" data-title="'+esc(title.lower())+'" style="border-left-color:'+bar+'">'
            '<summary><span class="ticon" style="color:'+bar+';background:'+chip+'">'+theme_icon(t["title"])+'</span>'
            + tt_span + '<span class="tchev"></span></summary>'
            + tfield +
            '<div class="scroller"><div class="grid">'+th+body+'</div></div></details>')

def merge_same_segs(segs):
    """Benachbarte Segmente mit identischem Inhalt (Text + Links) zu einem Block
    zusammenfassen – auch ueber Phasengrenzen (F/T/E/M) hinweg."""
    out = []
    for s in segs:
        if out:
            p = out[-1]
            same_v = (p.get("v") or "").strip() == (s.get("v") or "").strip()
            pl = [(l.get("href"), l.get("text")) for l in (p.get("l") or [])]
            sl = [(l.get("href"), l.get("text")) for l in (s.get("l") or [])]
            if same_v and pl == sl:
                out[-1] = {"v": p.get("v"), "from": p["from"], "to": s["to"], "l": p.get("l") or []}
                continue
        out.append(dict(s))
    return out

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
        for k2,(i,t) in enumerate(items):
            # Zebra startet pro Bereich neu; einzelne Themen bleiben weiss (Kontrast)
            sections += theme_html(t,i,stages,prefix,lang,ages,edit,g, alt=(len(items)>1 and k2%2==1))
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

CLOSE_W = {"de": "schliessen", "fr": "fermer", "it": "chiudi", "en": "close"}

def theme_toggle(lang="de"):
    tt = {"de": "Hell / Dunkel", "fr": "Clair / Sombre", "it": "Chiaro / Scuro", "en": "Light / Dark"}[lang]
    ta = {"de": "Hell/Dunkel umschalten", "fr": "Basculer clair/sombre", "it": "Commuta chiaro/scuro", "en": "Toggle light/dark"}[lang]
    return ('<button class="themebtn" type="button" onclick="toggleTheme()" '
            'title="'+esc(tt)+'" aria-label="'+esc(ta)+'">'
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
        return ('<section class="sport" data-sport="'+sid+'" hidden><div class="wrap">'
                + home_edit_html(sport, d) + sections + '</div></section>')
    aw = esc(tr("Athlet:innen-Weg", lang))
    back = ('<a class="back" href="#" title="'+esc(BACK_TITLE[lang])+'" aria-label="'+esc(BACK_TITLE[lang])+'">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></a>')
    if sport.get("icon"):
        back += '<img class="sicon" src="'+esc(sport["icon"])+'" alt="'+esc(name)+'" width="32" height="32" decoding="async">'
    # Sportarten-Wechsel direkt im Titel (Dropdown statt fixer Ueberschrift)
    sport_opts = "".join('<option value="'+x["id"]+'"'+(' selected' if x["id"] == sid else '')+'>'
                         + esc(tr(x["name"], lang)) + '</option>' for x in SPORTS)
    _chg = {"de": "Sportart wechseln", "fr": "Changer de sport", "it": "Cambia sport", "en": "Change sport"}[lang]
    title_sel = '<select class="sportsel2" aria-label="'+esc(_chg)+'">'+sport_opts+'</select>'
    if d is None:
        return ('<section class="sport" data-sport="'+sid+'" hidden>'
            '<header class="top"><div class="ht-l">'+back+title_sel+'</div>'
            '<div class="ht-r">'+lang_switch(lang)+theme_toggle(lang)+'</div></header>'
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
        +lang_switch(lang)+theme_toggle(lang)+'</div></header>'
        '<div class="wrap">'
        +sections
        # Praesentationsmodus nur noch ueber den ⛶-Knopf auf der Startseite
        +'</div>'
        +stage_bar(d["stages"], lang)+'</section>')

# --- Startseite (Sportart-Auswahl) -----------------------------------------
# Positionen der Sternbild-Knoten (x%, y%) auf der Hero-Flaeche
# Entlang der Bergsilhouette von hero.jpg: unten links im Vorgelaende startend,
# ueber den linken Grat zum Gipfelbereich, rechts wieder abfallend.
# Strenges Zickzack (Gipfel/Tal im Wechsel): so laufen die Linien immer VON der
# Beschriftung weg und keine Schrift kreuzt eine Linie.
# Kammlinie des Hero-Fotos (automatisch + manuell nachgezeichnet), Koordinaten in Bildpixeln (1896x986)
RIDGE_PATH = "M0,986 L0,563.6 L0,563.6 L8,564.9 L21,569.6 L28,569.9 L39,567.0 L65,556.2 L80,554.8 L94,557.6 L119,565.6 L161,583.3 L200,586.5 L234,591.7 L244,591.6 L253,589.6 L276,578.9 L313,552.0 L394,466.3 L410,452.1 L432,437.7 L440,428.7 L451,423.4 L476,414.9 L505,400.6 L519,390.1 L542,367.7 L558,355.6 L573,340.9 L578,340.9 L599,347.4 L611,344.9 L623,345.6 L635,342.9 L653,335.7 L662,328.0 L666,327.4 L678,330.0 L707,340.0 L749,356.4 L768,358.9 L773,358.2 L780,354.6 L791,351.6 L813,342.9 L824,343.5 L838,339.4 L854,342.0 L870,340.5 L878,338.0 L886,338.6 L896,334.8 L917,321.4 L924,316.4 L930,309.8 L936,309.0 L949,297.1 L967,285.2 L983,269.6 L997,253.8 L1014,230.1 L1018,227.3 L1026,225.8 L1034,230.4 L1039,229.9 L1047,237.4 L1069,249.2 L1080,261.8 L1090,277.0 L1102,284.5 L1113,302.4 L1120,307.7 L1127,317.3 L1133,320.8 L1141,323.3 L1149,331.3 L1168,341.2 L1176,341.9 L1184,345.0 L1197,355.2 L1208,360.6 L1216,370.5 L1230,373.8 L1238,378.3 L1246,377.3 L1255,380.7 L1262,384.5 L1269,391.4 L1276,393.0 L1289,400.7 L1299,408.8 L1307,413.1 L1311,413.6 L1325,427.9 L1333,433.5 L1339,435.3 L1345,445.1 L1351,451.2 L1360,464.2 L1387,473.7 L1423,477.4 L1437,474.9 L1457,474.0 L1465,468.2 L1480,461.4 L1488,455.6 L1498,450.4 L1502,450.6 L1508,453.9 L1516,454.7 L1528,451.9 L1542,440.7 L1552,435.4 L1566,420.4 L1572,417.7 L1579,409.0 L1589,406.6 L1600,412.6 L1607,411.4 L1613,414.3 L1628,414.8 L1632,412.1 L1639,402.4 L1646,399.7 L1677,412.5 L1684,418.5 L1693,430.5 L1723,452.1 L1735,455.0 L1749,456.3 L1766,463.9 L1780,472.3 L1792,476.1 L1807,474.9 L1820,471.1 L1840,460.4 L1858,454.6 L1879,438.2 L1895,432.0 L1896,432.0 L1896,986 Z"

# Himmel-Flaeche = Inverse der Bergsilhouette (gleiche Kammlinie, oben geschlossen).
# Dient als ClipPath fuer die Blau-Toenung des Himmels (freundlicherer Look).
SKY_PATH = "M0,0 " + RIDGE_PATH[len("M0,986 "):].rsplit("L1896,986", 1)[0] + "L1896,0 Z"

CONS_POS = [(7,74),(14,49),(22,71),(29,35),(37,64),(44,48),(55,72),(66,40),(77,67),(89,43)]
# durchgehende Linien (Sport-Indizes): Nordisch-Gruppe, Cross-Gruppe, Park&Pipe-Gruppe
# 0 ski-alpin,1 langlauf,2 biathlon,3 skispringen,4 nord.komb,5 skicross,
# 6 freeski-pp,7 sb-alpin,8 sb-cross,9 sb-pp
CONS_LINKS = [(1,2),(2,3),(3,4),(5,8),(8,7),(6,9)]

# --- Newsbox -----------------------------------------------------------------
# Neue Meldung? Einfach oben in diese Liste einen Block einfuegen (neueste zuerst).
#   "title"   : Ueberschrift
#   "date"    : Datum der Meldung (frei, z. B. "Juli 2026" oder "03.08.2026")
#   "body"    : Liste von Absaetzen (Text)
#   "bullets" : optionale Liste von Aufzaehlungspunkten
#   "url"     : Link -> wird als "Link"-Button gezeigt (leer lassen = kein Button)
NEWS = [
    {
        "title": "Neue Ausbildungsstruktur",
        "date": "Juli 2026",
        "body": ["Die Übersichtsseite zur neuen Ausbildungsstruktur ist live!",
                 "Entdecke den Ausbildungsweg bis hin zum «Swiss-Ski Trainer:in Spitzensport»."],
        "bullets": [],
        # Link je nach gewaehlter Sportart ("default" = Ski Alpin, gilt auch fuer NoKo & Co.)
        "url": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/ski-alpin-ab-2027",
        "urls": {
            "default": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/ski-alpin-ab-2027",
            "langlauf": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/langlauf-ab-2027-1-1/",
            "biathlon": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/biathlon-ab-2027-1-1/",
            "skispringen": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/skispringen/",
            "skicross": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/freestyle/",
            "freeski-park-pipe": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/freestyle/",
            "snowboard-alpin": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/freestyle/",
            "snowboard-cross": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/freestyle/",
            "snowboard-park-pipe": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/trainerin/freestyle/",
        },
    },
    {
        "title": "Swiss-Ski Ausbildungsnews Juli 26",
        "date": "Juli 2026",
        "body": ["Verschiedene News in folgenden Bereichen:"],
        "bullets": ["Gut zu wissen",
                    "Kurse: Ski Alpin | Langlauf | Biathlon | Ski Freestyle / Snowboard | Skispringen | Tourenwesen"],
        "url": "https://www.swiss-ski.ch/ueber-swiss-ski/ausbildung/ausbildungsnews/",
        "foot": "Im Archiv auf der verlinkten Webseite findest du alle bereits verschickten Newsletter.",
    },
]

# Einleitungssatz der schwarzen Fusszeile (im Admin editierbar: cid "start|footintro")
FOOT_INTRO = {"de": "Sportartübergreifende Grundlagen:",
              "fr": "Bases transversales :",
              "it": "Basi trasversali:",
              "en": "Cross-sport foundations:"}

def news_html(lang):
    if not NEWS:
        return ""
    heading = {"de":"News","fr":"Actualités","it":"Notizie","en":"News"}.get(lang, "News")
    upd = {"de":"Aktualisiert am ","fr":"Mis à jour le ","it":"Aggiornato il ","en":"Updated on "}.get(lang, "Aktualisiert am ")
    cards = ""
    for i, it in enumerate(NEWS):
        # Texte tragen data-cid -> im Admin-Bereich editierbar (Links/Struktur nicht)
        body = "".join('<p>'+esc(tr(p, lang))+'</p>' for p in it.get("body", []))
        if it.get("bullets"):
            body += '<ul>'+"".join('<li>'+esc(tr(b, lang))+'</li>' for b in it["bullets"])+'</ul>'
        if it.get("foot"):
            body += '<p>'+esc(tr(it["foot"], lang))+'</p>'
        _urls = (' data-urls=\''+json.dumps(it["urls"], ensure_ascii=False)+'\'') if it.get("urls") else ''
        link = ('<a class="news-link" href="'+esc(it["url"])+'"'+_urls+' target="_blank" rel="noopener">Link ↗</a>') if it.get("url") else ''
        date = ('<span class="news-date">'+esc(tr(it["date"], lang))+'</span>') if it.get("date") else ''
        new_badge = '<span class="news-new">NEU</span>' if i == 0 else ''
        cards += ('<article class="news-card"><div class="news-meta">'+date+new_badge+'</div>'
                  '<h3>'+esc(tr(it["title"], lang))+'</h3>'
                  '<div class="news-body">'+body+'</div>'+link+'</article>')
    return ('<section class="news"><h2 class="news-h">'+esc(heading)+'</h2>'
            '<div class="news-upd">'+esc(upd)+datestr+'</div>'
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
 "en": {"title": "Add as an app",
        "body": "This page can be saved like an app – no download needed.<br>"
                "<b>iPhone (Safari):</b> \u201cShare\u201d <span class=\"ai-i\">&#8593;</span> \u2192 \u201cAdd to Home Screen\u201d.<br>"
                "<b>Android (Chrome):</b> menu \u22ee \u2192 \u201cInstall app\u201d."},
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
    # "Was ist FTEM?" als aufsteigender Weg (F1 -> M) mit allen 10 Entwicklungsstufen (Luca)
    WEG_ENDS = {"de": ("Erster Schneekontakt", "Weltspitze"),
                "fr": ("Premier contact neige", "Élite mondiale"),
                "it": ("Primo contatto neve", "Élite mondiale"),
                "en": ("First snow contact", "World class")}[lang]
    PH_HEX = {"F": "#1f8fa6", "T": "#e2a900", "E": "#e8772e", "M": "#d52b1e"}
    weg_stages = ["F1", "F2", "F3", "T1", "T2", "T3", "T4", "E1", "E2", "M"]
    def _nx(i): return 60 + i * (840 / 9.0)
    def _ny(i): return 246 - i * (176 / 9.0)
    _pathd = "M" + " L".join("%.0f %.0f" % (_nx(i), _ny(i)) for i in range(10))
    _nodes = ""
    for i, st in enumerate(weg_stages):
        _nodes += ('<g class="wn"><circle cx="%.0f" cy="%.0f" r="16" fill="%s"/>'
                   '<text x="%.0f" y="%.0f" class="wn-t">%s</text></g>'
                   % (_nx(i), _ny(i), PH_HEX[st[0]], _nx(i), _ny(i), esc(st)))
    _groups = [(0, 2), (3, 6), (7, 8), (9, 9)]
    _plabels = ""
    for (a, b), (pk, pn, pr, desc) in zip(_groups, info["phases"]):
        xc = (_nx(a) + _nx(b)) / 2.0; yc = (_ny(a) + _ny(b)) / 2.0
        _plabels += ('<text x="%.0f" y="%.0f" class="wl" fill="%s" text-anchor="middle">%s</text>'
                     % (xc, yc - 34, PH_HEX[pk], esc(pn)))
    _ends = ('<text x="60" y="286" class="we" text-anchor="middle">' + esc(WEG_ENDS[0]) + '</text>'
             '<text x="884" y="104" class="we" text-anchor="middle">' + esc(WEG_ENDS[1]) + '</text>')
    _gondel = ('<g class="gondel" style="offset-path:path(\'' + _pathd + '\')">'
               '<line x1="-6" y1="-9" x2="-6" y2="-13" class="gcable"/>'
               '<line x1="6" y1="-9" x2="6" y2="-13" class="gcable"/>'
               '<rect x="-13" y="-9" width="26" height="16" rx="4" fill="#d52b1e"/>'
               '<rect x="-9" y="-6" width="18" height="5" rx="1.5" fill="rgba(255,255,255,.85)"/></g>')
    weg_svg = ('<svg class="fweg" viewBox="0 0 960 300" role="img" aria-label="FTEM Entwicklungsstufen F1 bis M">'
               '<polygon class="fmt2" points="0,300 250,150 480,300 720,120 960,300"/>'
               '<polygon class="fmt1" points="0,300 170,205 380,300 560,178 780,300 960,150 960,300"/>'
               '<path class="fweg-line" d="' + _pathd + '"/>'
               + _gondel + _plabels + _nodes + _ends + '</svg>')
    pc2 = {"F": "f", "T": "t", "E": "e", "M": "m"}
    _desc = "".join('<div class="fwd fwd-' + pc2[pk] + '"><span class="fwd-h"><b>' + pn + '</b> ' + pr + '</span>'
                    '<p>' + desc + '</p></div>' for pk, pn, pr, desc in info["phases"])
    ftem_info = ('<div class="ftem-info">'
                 '<h2>' + info["title"] + '</h2>'
                 '<p class="lead">' + info["lead"] + '</p>'
                 '<div class="fweg-wrap">' + weg_svg + '</div>'
                 '<div class="fweg-desc">' + _desc + '</div></div>')
    fb_ph = {"de":"Dein Feedback …","fr":"Votre commentaire …","it":"Il tuo feedback …","en":"Your feedback …"}.get(lang, "Dein Feedback …")
    fb_send = {"de":"Senden","fr":"Envoyer","it":"Invia","en":"Send"}.get(lang, "Senden")
    # Feedback als sichtbare Karte links im Hero (Bjoern-Mock: kein Hamburger mehr)
    fb_title = {"de":"Feedback geben","fr":"Donner un feedback","it":"Dare un feedback","en":"Give feedback"}.get(lang, "Feedback geben")
    fb_sub = {"de":"Deine Meinung zählt!","fr":"Ton avis compte !","it":"La tua opinione conta!","en":"Your opinion matters!"}.get(lang, "Deine Meinung zählt!")
    fb = ('<div class="fb-wrap">'
          '<button class="fb-card" type="button" '
          'onclick="var p=this.nextElementSibling;p.hidden=!p.hidden;if(!p.hidden)p.querySelector(&#39;textarea&#39;).focus()">'
          '<span class="fbc-ic"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12a8 8 0 1 0-3.1 6.3L21 20l-1-3.4A8 8 0 0 0 21 12z"/><path d="M8.5 10.5h7M8.5 13.5h4.5"/></svg></span>'
          '<span class="fbc-tx"><b>'+esc(fb_title)+'</b><small>'+esc(fb_sub)+'</small></span>'
          '<span class="fbc-ar">→</span></button>'
          '<div class="fb-panel" hidden>'
          '<button class="fb-x" type="button" aria-label="'+esc(CLOSE_W[lang])+'" '
          'onclick="this.closest(&#39;.fb-panel&#39;).hidden=true">&times;</button>'
          '<textarea class="fb-text" placeholder="'+esc(fb_ph)+'"></textarea>'
          '<button class="fb-send" type="button" '
          'onclick="location.href=&#39;mailto:forschung@swiss-ski.ch?subject=Feedback%20FTEM&amp;body=&#39;+encodeURIComponent(this.parentNode.querySelector(&#39;.fb-text&#39;).value)">'+esc(fb_send)+'</button>'
          '</div></div>')
    # FTEM-Weg als Berg-Schichten (Design "Beispiel 2"): F unten -> M Gipfel, Talent dominant.
    # Farben bewusst entsaettigt/transparent, damit sie mit dem Bergfoto verschmelzen.
    band_lbl = {"de": ["FOUNDATION","TALENT","ELITE","MASTERY"],
                "fr": ["FOUNDATION","TALENT","ELITE","MASTERY"],
                "it": ["FOUNDATION","TALENT","ELITE","MASTERY"],
                "en": ["FOUNDATION","TALENT","ELITE","MASTERY"]}[lang]
    # FTEM-Zonen folgen der echten Bergsilhouette: SVG mit Foto + ClipPath auf der Kammlinie.
    # Die Farbbaender sind Hoehenzonen des Bergs (M = Gipfel, F = Basis).
    # Beschriftungen liegen IM SVG (gleiche Bildkoordinaten) -> sie sitzen bei jeder
    # Fenstergroesse exakt auf ihrer Zone, alle zentriert in einer Linie.
    # preserveAspectRatio "YMin": bei breiten/flachen Fenstern wird unten (Wald) statt
    # oben (Himmel) beschnitten -> der Titel ueberlappt den Gipfel nicht mehr.
    # Labels auf der Vertikalen der Bergspitze (x=1018 im Bild), nicht in der Bildmitte.
    # viewBox oben um 110px beschnitten: in den Berg gezoomt, weniger Himmel sichtbar
    hero_svg = ('<svg class="heromt" viewBox="0 110 1896 876" preserveAspectRatio="xMidYMin slice" aria-hidden="true">'
        '<defs>'
        '<clipPath id="mtclip"><path d="'+RIDGE_PATH+'"/></clipPath>'
        '<clipPath id="skyclip"><path d="'+SKY_PATH+'"/></clipPath>'
        # Helle Startseite (Feedback Wala/Bjoern): weisser Schleier oben und unten
        # statt Abdunklung; das Foto bleibt natuerlich hell.
        '<linearGradient id="herodark" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="rgba(255,255,255,.40)"/><stop offset=".34" stop-color="rgba(255,255,255,.08)"/>'
        '<stop offset=".55" stop-color="rgba(255,255,255,0)"/><stop offset=".88" stop-color="rgba(255,255,255,.50)"/>'
        '<stop offset="1" stop-color="rgba(255,255,255,.72)"/></linearGradient>'
        # Durchgehender weicher FTEM-Verlauf ueber dem Berg (M Gipfel -> F Basis).
        # Die Stop-Offsets werden beim Hover ueber die FTEM-Knoepfe animiert (Zone waechst).
        # Zwei Ebenen wie im Mockup: kraeftige Farben im Overlay-Blend + leichte Deckschicht
        '<linearGradient id="zonegrad" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="rgba(213,43,30,.48)"/><stop offset=".355" stop-color="rgba(213,43,30,.48)"/>'
        '<stop offset=".406" stop-color="rgba(232,119,46,.48)"/><stop offset=".522" stop-color="rgba(232,119,46,.48)"/>'
        '<stop offset=".573" stop-color="rgba(226,169,0,.48)"/><stop offset=".755" stop-color="rgba(226,169,0,.48)"/>'
        '<stop offset=".848" stop-color="rgba(31,143,166,.45)"/><stop offset="1" stop-color="rgba(31,143,166,.45)"/>'
        '</linearGradient>'
        '<linearGradient id="zonegrad2" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="rgba(213,43,30,.14)"/><stop offset=".355" stop-color="rgba(213,43,30,.14)"/>'
        '<stop offset=".406" stop-color="rgba(232,119,46,.14)"/><stop offset=".522" stop-color="rgba(232,119,46,.14)"/>'
        '<stop offset=".573" stop-color="rgba(226,169,0,.14)"/><stop offset=".755" stop-color="rgba(226,169,0,.14)"/>'
        '<stop offset=".848" stop-color="rgba(31,143,166,.14)"/><stop offset="1" stop-color="rgba(31,143,166,.14)"/>'
        '</linearGradient>'
        '<linearGradient id="linegrad" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="986">'
        '<stop offset="0" stop-color="#ff6d60"/><stop offset=".355" stop-color="#ff6d60"/>'
        '<stop offset=".406" stop-color="#ff9b57"/><stop offset=".522" stop-color="#ff9b57"/>'
        '<stop offset=".573" stop-color="#ffd45c"/><stop offset=".776" stop-color="#ffd45c"/>'
        '<stop offset=".827" stop-color="#57cce4"/><stop offset="1" stop-color="#57cce4"/>'
        '</linearGradient>'
        '</defs>'
        '<image href="'+asset_v('assets/hero.jpg')+'" x="0" y="0" width="1896" height="986" preserveAspectRatio="none"/>'
        '<rect x="0" y="0" width="1896" height="986" fill="url(#herodark)"/>'
        # Zonen-Overlays unsichtbar (opacity 0), aber im DOM belassen: die Hover-
        # Animation (zoneAnim) greift weiter auf die Gradient-Stops zu.
        '<g clip-path="url(#mtclip)" opacity="0">'
        '<rect x="0" y="0" width="1896" height="986" fill="url(#zonegrad)"/>'
        '<rect x="0" y="0" width="1896" height="986" fill="url(#zonegrad2)"/>'
        '</g>'
        + '</svg>')
    # Die vier 3D-FTEM-Knoepfe (Wiedererkennung zur alten Landingpage): aufsteigend
    # von unten links nach oben rechts, F/T groesser als E/M; Klick -> Stufen-Popup.
    _fb = [("f", "Foundation", "F1–F3"), ("t", "Talent", "T1–T4"),
           ("e", "Elite", "E1–E2"), ("m", "Mastery", "M")]
    fbtns = '<div class="fbtns" role="navigation" aria-label="FTEM-Stufen">'
    for _k, _n, _r in _fb:
        fbtns += ('<button class="fbtnw w-'+_k+'" type="button" data-ph="'+_k+'" aria-label="'+_n+' '+_r+'">'
                  '<span class="fb3d fb-'+_k+'"><i class="fl">'+_k.upper()+'</i>'
                  '<span class="fbl">'+_n+'<small>'+_r+'</small></span></span></button>')
    fbtns += '</div>'
    pyr = hero_svg + fbtns
    # Klick auf eine Stufe -> Sportarten-Auswahl -> Athlet:innen-Weg der Sportart
    choose_lbl = {"de": "Sportart wählen", "fr": "Choisir un sport", "it": "Scegli lo sport", "en": "Choose a sport"}[lang]
    spitems = ""
    for s2 in SPORTS:
        nm = tr(s2["name"], lang)
        ic = s2.get("icon")
        inner2 = ('<img src="'+esc(ic)+'" alt="" loading="lazy">') if ic else ('<span class="spcode">'+esc(s2["short"])+'</span>')
        spitems += '<a href="#'+s2["id"]+'">'+inner2+'<b>'+esc(nm)+'</b></a>'
    spmodal = ('<div class="spmodal" hidden><div class="sp-box">'
               '<div class="sp-bar"><span>'+esc(choose_lbl)+'</span><button class="sp-x" type="button" aria-label="'+esc(CLOSE_W[lang])+'">✕</button></div>'
               '<div class="sp-grid">'+spitems+'</div></div></div>')
    # Meeting-Paket: News-Button oben rechts, Mission-Button unter dem Logo,
    # Startseite ohne Scrollen (News/Infos als Overlays), Admin-Schloss unten im Hero.
    news_label = {"de": "News", "fr": "Actualités", "it": "Notizie", "en": "News"}[lang]
    info_label = FTEM_INFO[lang]["title"].replace("&#x27;", "'")
    mission_items = "".join(
        '<a class="mission-item" href="'+esc(s2["mission"])+'" data-title="'+esc(tr(s2["name"], lang))+' – Mission Swiss-Ski">'
        + esc(tr(s2["name"], lang)) + '</a>'
        for s2 in SPORTS if s2.get("mission"))
    # "Mission Sportart": oeffnet direkt die Mission der oben vorgewaehlten Sportart
    misp_lbl = {"de": "Mission Sportart", "fr": "Mission du sport", "it": "Missione sport", "en": "Sport mission"}[lang]
    mission_btn = '<button class="mp-item mp-mission np-sportmission" type="button">'+esc(misp_lbl)+'</button>'
    # App-Hinweis als eigener Knopf (nicht mehr in den News)
    app_lbl = INSTALL_HINT.get(lang, INSTALL_HINT["de"])["title"]
    # "Athlet:innen Weg"-Knopf oben Mitte (Bjoern-Mock) + Piste im Berg
    aw_lbl = tr("Athlet:innen-Weg", lang)
    go_lbl = {"de": "Zum Athlet:innen-Weg", "fr": "Vers le parcours de l'athlète", "it": "Al percorso dell'atleta", "en": "To the athlete pathway"}[lang]
    aw_cta = ('<div class="aw-cta"><button class="aw-btn" type="button">'+esc(aw_lbl)+
              ' <span class="aw-ar">→</span></button></div>')
    # Stufen-Summaries (Klick auf Zone -> Kurzbeschrieb statt direkt Athletenweg).
    # Pro Sportart aus dem "homepage"-Sheet des Excels (data["home"]); generischer
    # FTEM-Text als Fallback, falls eine Sportart keine Zusammenfassung hat.
    PH_STAGES = {"f": ["F1","F2","F3"], "t": ["T1","T2","T3","T4"], "e": ["E1","E2"], "m": ["M"]}
    ph_tpls = ""
    for k, (letter, pname, prng, pdesc) in zip(["f","t","e","m"], info["phases"]):
        ph_tpls += ('<template id="tpl-ph-'+k+'" data-t="'+esc(pname)+' · '+esc(prng)+'">'
                    '<div class="ph-sum ps-'+k+'"><div class="ps-head"><span class="ps-badge">'+esc(letter)+'</span>'
                    '<div><div class="ps-name">'+esc(pname)+'</div><div class="ps-rng">'+esc(prng)+'</div></div></div>'
                    '<p class="ps-desc">'+pdesc+'</p>'
                    '<button class="aw-go" type="button">'+esc(go_lbl)+' →</button></div></template>')
    for s2 in SPORTS:
        d2 = datamap.get(s2["id"])
        hm = (d2 or {}).get("home")
        if not hm:
            continue
        ages2 = {kk: vv for kk, vv in ((d2.get("ages") or {}) if d2 else {}).items() if vv}
        for k, (letter, pname, prng, pdesc) in zip(["f","t","e","m"], info["phases"]):
            intro2 = (hm.get("intro") or {}).get(k) or pdesc
            secs = ""
            for si2, sec in enumerate(hm.get("sections", [])):
                cols = ""
                ncols = 0
                for st in PH_STAGES[k]:
                    cell = (sec.get("cells") or {}).get(st)
                    if not cell or not (cell.get("v") or cell.get("l")):
                        continue
                    # gleiche Aufbereitung wie die Zellen im Athlet:innen-Weg
                    # (data-cid -> im Admin-Bereich als Startseiten-Inhalt editierbar)
                    body2 = render_cell({"v": cell.get("v") or "", "l": cell.get("l") or []}, lang,
                                        cid="home|"+s2["id"]+"|"+str(si2)+"|"+st)
                    age2 = ages2.get(st, "")
                    ncols += 1
                    cols += ('<div class="ps-col"><div class="ps-st">'+st
                             + ('<i>'+esc(age2)+'</i>' if age2 else '') + '</div>'
                             + '<div class="cwrap">'+body2+'</div></div>')
                if cols:
                    # wie im Athlet:innen-Weg: einklappbare Themenzeile, standardmaessig zu
                    secs += ('<details class="theme ps-theme">'
                             '<summary><span class="ticon" style="color:#4a5563;background:rgba(74,85,99,.13)">'
                             + theme_icon(sec["title"]) + '</span>'
                             '<span class="tt ovr-txt" data-cid="home|'+s2["id"]+'|'+str(si2)+'|title" data-bh="'+fnv36(sec["title"] or "")+'">'+esc(tr(sec["title"], lang))+'</span><span class="tchev"></span></summary>'
                             '<div class="ps-secbody"><div class="ps-cols" style="--nc:'+str(ncols)+'">'+cols+'</div></div></details>')
            ph_tpls += ('<template id="tpl-ph-'+k+'-'+s2["id"]+'" data-t="'+esc(pname)+' · '+esc(prng)+' – '+esc(tr(s2["name"], lang))+'">'
                        '<div class="ph-sum ph-wide ps-'+k+'"><div class="ps-head"><span class="ps-badge">'+esc(letter)+'</span>'
                        '<div><div class="ps-name ovr-txt" data-cid="home|'+s2["id"]+'|'+k+'|ptitle" data-bh="'+fnv36(pname)+'">'+esc(pname)+'</div><div class="ps-rng">'+esc(prng)+' · '+esc(tr(s2["name"], lang))+'</div></div></div>'
                        '<p class="ps-desc ovr-txt" data-cid="home|'+s2["id"]+'|'+k+'|intro" data-bh="'+fnv36(intro2)+'">'+esc(tr(intro2, lang)).replace("\n", "<br>")+'</p>'
                        + secs +
                        '<button class="aw-go" type="button">'+esc(go_lbl)+' →</button></div></template>')
    # Drei Grundlagen-Links im "Was ist FTEM?"-Overlay
    fi_links = [
        ({"de":"Übersicht FTEM","fr":"Aperçu FTEM","it":"Panoramica FTEM","en":"FTEM overview"}[lang], "https://snowsports.flink.host/s/iFt05YOw/c5lG7vWX"),
        ("How to use FTEM", "https://snowsports.flink.host/s/iFt05YOw/CVg0efTY"),
        ({"de":"Leitsätze der Athlet:innen-Entwicklung","fr":"Principes du développement des athlètes","it":"Principi dello sviluppo degli atleti","en":"Guiding principles of athlete development"}[lang], "https://snowsports.flink.host/s/Ur9yhq2P/"),
    ]
    fi_html = ('<div class="mlist fi-links">'
               + "".join('<a class="mission-item" href="'+esc(u2)+'" data-title="'+esc(t2)+'">'+esc(t2)+'</a>' for t2, u2 in fi_links)
               + '</div>')
    # Unten im Hero: Admin-Schloss + Praesentations-Knopf nebeneinander, gemeinsam
    # zentriert, beide mit demselben Farbverlauf (#adminlk).
    adminlk = ('<div class="adminlink mp-admin preslink"><a href="admin.html" title="Admin-Login" aria-label="Admin-Login">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="url(#adminlk)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<defs><linearGradient id="adminlk" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#1f8fa6"/><stop offset=".4" stop-color="#e2a900"/><stop offset=".7" stop-color="#e8772e"/><stop offset="1" stop-color="#d52b1e"/></linearGradient></defs>'
            '<rect x="4.6" y="10.4" width="14.8" height="10.2" rx="2.4"/><path d="M8 10.4V7.4a4 4 0 0 1 8 0v3"/>'
            '<circle cx="12" cy="15" r="1.5" fill="url(#adminlk)" stroke="none"/></svg></a>'
            '<button class="presopen" type="button" title="'+esc(PRES_TITLE[lang])+'" aria-label="'+esc(PRES_TITLE[lang])+'">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="url(#adminlk)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M4 9V5.5A1.5 1.5 0 0 1 5.5 4H9"/><path d="M15 4h3.5A1.5 1.5 0 0 1 20 5.5V9"/>'
            '<path d="M20 15v3.5a1.5 1.5 0 0 1-1.5 1.5H15"/><path d="M9 20H5.5A1.5 1.5 0 0 1 4 18.5V15"/></svg></button>'
            '<span class="presask" hidden><input class="prespw" type="password" placeholder="'+esc(PRES_PWPH[lang])+'" autocomplete="off">'
            '<button class="presgo" type="button">OK</button></span></div>')
    # Folie "Die Website" fuer den Praesentationsmodus
    web_head = {"de": ("Die Website", "Alles zur Athlet:innen-Entwicklung im Schneesport – auf einer Seite:"),
                "fr": ("Le site web", "Tout sur le développement des athlètes dans les sports de neige – sur une seule page :"),
                "it": ("Il sito web", "Tutto sullo sviluppo degli atleti negli sport sulla neve – su un'unica pagina:"),
                "en": ("The website", "Everything about athlete development in snow sports – on one page:")}[lang]
    web_feats = {"de": [
        ("Athlet:innen-Weg", "Alle 10 Sportarten im Detail – Themen und Inhalte über die Stufen F1–M, mit Suche, Stufen-Fokus und PDF-Export."),
        ("Stufen-Überblick", "Kurz-Zusammenfassung pro Phase (Foundation, Talent, Elite, Mastery) direkt auf dem Titelberg – pro Sportart."),
        ("Mission Swiss-Ski", "Die Mission jeder Sportart als integrierte Ansicht, plus Grundlagen wie Übersicht FTEM und Leitsätze."),
        ("News & Dokumente", "Aktuelle Ausbildungsnews mit Datum sowie verlinkte Dokumente direkt aus den Inhalten heraus."),
        ("FTEM-Coach (KI)", "Dein KI-Coach – fragt, erklärt, findet. Z. B. «Material in F3?», «Kraft-Ziele in T2?», «Welche Kader?»."),
        ("3 Sprachen & App", "Komplett auf Deutsch, Französisch und Italienisch – und als App auf dem Handy installierbar."),
    ], "fr": [
        ("Parcours de l'athlète", "Les 10 sports en détail – thèmes et contenus sur les niveaux F1–M, avec recherche, focus par niveau et export PDF."),
        ("Aperçu des niveaux", "Résumé par phase (Foundation, Talent, Elite, Mastery) directement sur la montagne – par sport."),
        ("Mission Swiss-Ski", "La mission de chaque sport en vue intégrée, plus les bases comme l'aperçu FTEM et les principes."),
        ("Actualités & documents", "Actualités de la formation avec date et documents liés directement depuis les contenus."),
        ("Coach FTEM (IA)", "Ton coach IA – demande, explique, trouve. Ex. « Matériel en F3 ? », « Objectifs de force en T2 ? », « Quels cadres ? »."),
        ("3 langues & app", "Entièrement en allemand, français et italien – installable comme app sur le téléphone."),
    ], "it": [
        ("Percorso dell'atleta", "Tutti i 10 sport nel dettaglio – temi e contenuti sui livelli F1–M, con ricerca, focus per livello ed export PDF."),
        ("Panoramica dei livelli", "Riassunto per fase (Foundation, Talent, Elite, Mastery) direttamente sulla montagna – per sport."),
        ("Missione Swiss-Ski", "La missione di ogni sport in vista integrata, più le basi come panoramica FTEM e principi."),
        ("Notizie & documenti", "Notizie sulla formazione con data e documenti collegati direttamente dai contenuti."),
        ("Coach FTEM (IA)", "Il tuo coach IA – chiedi, spiega, trova. Es. «Materiale in F3?», «Obiettivi di forza in T2?», «Quali quadri?»."),
        ("3 lingue & app", "Completamente in tedesco, francese e italiano – installabile come app sul telefono."),
    ], "en": [
        ("Athlete pathway", "All 10 sports in detail – topics and content across stages F1–M, with search, stage focus and PDF export."),
        ("Stage overview", "Short summary per phase (Foundation, Talent, Elite, Mastery) directly on the mountain – per sport."),
        ("Mission Swiss-Ski", "Each sport's mission as an integrated view, plus fundamentals such as the FTEM overview and guiding principles."),
        ("News & documents", "Current education news with dates, and linked documents directly from the content."),
        ("FTEM Coach (AI)", "Your AI coach – ask, explain, find. E.g. 'Gear in F3?', 'Strength goals in T2?', 'Which squads?'."),
        ("4 languages & app", "In German, French, Italian and English – installable as an app on your phone."),
    ]}[lang]
    _wf = ""
    _acts = ["aw", "stages", "mission", "news", "coach", "app"]
    # Reihenfolge der Kacheln (hochkant, eine Spalte): Mission, Stufen, Weg, News, Coach
    # "Sprachen & App" entfaellt auf dieser Folie.
    _order = [2, 1, 0, 3, 4]
    for n, i in enumerate(_order):
        ft, fd = web_feats[i]
        _wf += ('<button type="button" class="fwd fwd-'+["f","t","e","m"][n % 4]+' pdw" data-act="'+_acts[i]+'" data-t="'+esc(ft)+'">'
                '<span class="fwd-h"><b>'+esc(ft)+'</b></span><p>'+esc(fd)+'</p></button>')
    pres_web = ('<template id="tpl-pres-web"><div class="pd-web"><h2>'+esc(web_head[0])+'</h2>'
                '<p class="lead">'+esc(web_head[1])+' <b>ftemschneesport.netlify.app</b></p>'
                '<div class="pd-feats">'+_wf+'</div></div></template>')
    # Schwarze Fusszeile: sportartuebergreifende Grundlagen (oeffnen als iframe-Overlay)
    foot_links = [
        ("FAPS", "FAPS – Strategie Swiss-Ski", "https://snowsports.flink.host/s/psBIwCuB"),
        ({"de": "Schneesport 2050", "fr": "Sports de neige 2050", "it": "Sport sulla neve 2050", "en": "Snow sports 2050"}[lang],
         "Schneesport 2050", "https://snowsports.flink.host/s/soSSzlmC"),
        ({"de": "Ethik-Kompass", "fr": "Boussole éthique", "it": "Bussola etica", "en": "Ethics compass"}[lang],
         "Ethik-Kompass für die Schneesport-Praxis", "https://snowsports.flink.host/s/NxOLBkit"),
        ({"de": "Nachhaltigkeit im Schneesport", "fr": "Durabilité dans les sports de neige", "it": "Sostenibilità negli sport sulla neve", "en": "Sustainability in snow sports"}[lang],
         "Nachhaltigkeit im Schneesport", "https://tool.jugendundsport.ch/modules/654e2b8784846dba7a0ad962?lang=de"),
    ]
    foot_intro = FOOT_INTRO[lang]
    # Fusszeile (Bjoern-Mock, aber in bestehender Farbwelt und mit bestehenden Labels):
    # Mission Sportart links · Grundlagen-Knoepfe · rechts Admin/Praesentation + Info
    footbar = ('<div class="bottombar">'
               '<button class="bb-mission np-sportmission" type="button">'
               '<b>'+esc(misp_lbl)+'</b>'
               '<img class="bb-mlogo" src="'+asset_v('assets/swiss-ski-logo.svg')+'" alt="Swiss-Ski">'
               '</button>'
               '<span class="bb-div" aria-hidden="true"></span>'
               '<span class="bb-intro">'+esc(foot_intro)+'</span>'
               '<div class="bb-links">'
               + "".join('<a class="bb-item np-mission" href="'+esc(u)+'" data-title="'+esc(t)+'">'+esc(l)+'</a>'
                         for l, t, u in foot_links)
               + '</div>'
               # "Als App installieren" nur auf dem Handy sichtbar
               '<button class="bb-item bb-app" type="button" data-open="tpl-app" data-t="'+esc(app_lbl)+'">'+esc(app_lbl)+'</button>'
               '<div class="bb-tools">'+adminlk+
               '<button class="aw-info" type="button" data-open="tpl-info" data-t="'+esc(info_label)+'" title="'+esc(info_label)+'" aria-label="'+esc(info_label)+'">i</button>'
               '</div></div>')
    nbadge = ''  # Zaehler-Badge entfernt (Wunsch Michael)
    # Sportartspezifische Mini-Icons (monoline) fuer den Home-Sportpicker
    SPORT_ICONS = {
        "ski-alpin": '<path d="M4 20h16"/><path d="M8 20V5"/><path d="M8 5l7 2-7 2"/>',
        "langlauf": '<path d="M3 16.5 19 7"/><path d="M5 19 21 9.5"/><path d="M19 7l1.6 1.2"/>',
        "biathlon": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.2"/>',
        "skispringen": '<path d="M3 20c8 0 13-5 17-16"/><path d="M11 12l6 3"/>',
        "nordische-kombination": '<path d="M2 19c6 0 10-4 13-11"/><circle cx="18" cy="15" r="3.4"/>',
        "skicross": '<path d="M6 20V6l5 1.6L6 9.2"/><path d="M15 20V6l5 1.6L15 9.2"/>',
        "freeski-park-pipe": '<path d="M5 4v9a7 5 0 0 0 14 0V4"/>',
        "snowboard-alpin": '<rect x="9.5" y="3" width="5" height="18" rx="2.5" transform="rotate(32 12 12)"/>',
        "snowboard-cross": '<rect x="8.5" y="4" width="4.6" height="15" rx="2.2" transform="rotate(32 11 12)"/><path d="M18 4v6"/><path d="M18 4l3 1-3 1"/>',
        "snowboard-park-pipe": '<rect x="7" y="4" width="4.6" height="15" rx="2.2" transform="rotate(32 9.5 12)"/><path d="M15 6v4a3 2.4 0 0 0 6 0V6"/>',
    }
    def sport_icon(sid):
        # Piktogramm-Figuren aus dem Athletenweg (schwarz, transparenter Hintergrund);
        # auf dem dunklen Knopf per CSS-Filter weiss invertiert.
        return '<img class="sp-ic" src="'+asset_v('assets/sporticons/mono-'+sid+'.png')+'" alt="" loading="lazy">'
    _sp0 = SPORTS[0]
    sportpick = ('<div class="sportpick">'
                 '<button class="sp-btn" type="button" aria-haspopup="listbox" aria-expanded="false" aria-label="'
                 + esc({"de":"Sportart wählen","fr":"Choisir un sport","it":"Scegli lo sport","en":"Choose a sport"}[lang]) + '">'
                 '<span class="sp-cur-ic">' + sport_icon(_sp0["id"]) + '</span>'
                 '<span class="sp-lbl">' + esc(tr(_sp0["name"], lang)) + '</span>'
                 '<svg class="sp-chev" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
                 '</button>'
                 '<ul class="sp-list" role="listbox" hidden>'
                 + "".join('<li class="sp-opt" role="option" data-val="'+x["id"]+'"'
                           + (' aria-selected="true"' if x is _sp0 else '') + '>'
                           + sport_icon(x["id"]) + '<span>' + esc(tr(x["name"], lang)) + '</span></li>'
                           for x in SPORTS)
                 + '</ul></div>')
    return ('<section id="home">'
            '<div class="home-hero">'
            +aw_cta
            +fb+
            '<div class="hero-top-r">'
            '<div class="top-row">'
            + sportpick +
            '<select class="homesport sr-only" tabindex="-1" aria-hidden="true">'
            + "".join('<option value="'+x["id"]+'">'+esc(tr(x["name"], lang))+'</option>' for x in SPORTS)
            + '</select>'
            '<div class="mr-row">'
            '<div class="lang-ic"><button class="lang-ic-btn" type="button" aria-expanded="false" aria-label="'+esc({"de":"Sprache","fr":"Langue","it":"Lingua","en":"Language"}[lang])+'">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/></svg></button>'
            '<div class="lang-ic-menu" hidden>'+lang_switch(lang)+'</div></div></div>'
            '</div>'
            +(('<div class="news-box" data-open="tpl-news" data-t="'+esc(news_label)+'" role="button" tabindex="0">'
              '<div class="nb-head">'+esc(news_label)+nbadge+'</div>'
              '<ul class="nb-list">'
              + "".join(
                  '<li><div class="nb-item"><span class="nb-t">'+esc(tr(it["title"], lang))+'</span>'
                  # Teaser: erster Satz des News-Texts
                  + (('<span class="nb-teaser">'+esc(tr((it.get("body") or [""])[0], lang))+'</span>') if (it.get("body") or [""])[0] else '')
                  # Direktlink (oeffnet extern, ohne News-Overlay-Umweg)
                  + (('<a class="nb-lnk" href="'+esc(it["url"])+'"'
                      + ((" data-urls='"+json.dumps(it["urls"], ensure_ascii=False).replace("'","&#39;")+"'") if it.get("urls") else '')
                      + ' target="_blank" rel="noopener">'
                      + esc({"de":"Mehr lesen","fr":"En savoir plus","it":"Leggi di più","en":"Read more"}.get(lang,"Mehr lesen"))+' →</a>') if it.get("url") else '')
                  + '</div></li>'
                  for it in NEWS[:3])
              + '</ul>'
              '<span class="nb-more">'+esc({"de":"Alle News ansehen","fr":"Voir toutes les actualités","it":"Vedi tutte le notizie","en":"See all news"}[lang])+' →</span>'
              '</div>') if NEWS else
             ('<button class="news-btn" type="button" data-open="tpl-news" data-t="'+esc(news_label)+'">'+esc(news_label)+'</button>'))
            +'</div>'
            # FTEM-Schriftzug entfernt (Knoepfe + Berg tragen die Farben); h1 bleibt fuer SEO unsichtbar
            '<div class="hero-head"><h1 class="sr-only">FTEM – '+esc({"de":"Athlet:innen-Weg Schneesport","fr":"Parcours de l’athlète sports de neige","it":"Percorso dell’atleta sport sulla neve","en":"Athlete pathway snow sports"}[lang])+'</h1>'
            '<a class="hero-logo-lnk" href="https://www.swiss-ski.ch/" target="_blank" rel="noopener" aria-label="swiss-ski.ch">'
            '<img class="hero-logo" src="'+asset_v('assets/swiss-ski-logo.svg')+'" alt="Swiss-Ski"></a></div>'
            +pyr+footbar+
            '</div>'
            +pres_web+
            '<template id="tpl-news">'+news_html(lang)+'</template>'
            '<template id="tpl-app">'+install_hint(lang)+'</template>'
            '<template id="tpl-info">'+ftem_info+fi_html+'</template>'
            '<template id="tpl-missions"><div class="mlist">'+mission_items+'</div></template>'
            +ph_tpls+
            '</section>')


CSS = r"""
:root{--red:#d52b1e;--ink:#1d2630;--mut:#697080;--line:#e4e8ec;--bg:#eef1f4;--card:#fff;
--phf:#f4faf8;--pht:#fcf8ee;--phe:#fdf5ef;--phm:#fcefef;
--mg:linear-gradient(rgba(0,0,0,0),rgba(0,0,0,0));
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
#home .home-hero{position:relative;min-height:100vh;min-height:100svh;overflow:hidden;color:var(--ink);display:flex;flex-direction:column;
  background:linear-gradient(180deg,rgba(255,255,255,.40),rgba(255,255,255,.08) 34%,rgba(255,255,255,0) 55%,rgba(255,255,255,.55) 88%,rgba(255,255,255,.72)),url("assets/hero.jpg") center 32%/cover no-repeat}
#home .hero-top{position:absolute;top:16px;left:18px;z-index:7;display:flex;flex-direction:column;align-items:flex-start;gap:8px}
#home .hero-top .lsrow{display:flex;align-items:stretch;gap:8px}
#home .hero-top .lsrow .themebtn{width:33px;height:auto;align-self:stretch}
.fb-btn{background:var(--red);color:#fff;border:none;border-radius:8px;padding:6px 15px;font-size:11.5px;font-weight:800;letter-spacing:.04em;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.3);transition:filter .15s}
.fb-btn:hover{filter:brightness(1.12)}
/* Feedback-Karte links im Hero (statt Hamburger-Menue) */
.fb-wrap{position:absolute;left:18px;top:170px;z-index:8}
.fb-card{font:inherit;display:flex;align-items:center;gap:11px;background:rgba(255,255,255,.94);border:1px solid rgba(29,38,48,.10);border-radius:16px;padding:11px 15px;cursor:pointer;box-shadow:0 8px 26px rgba(29,38,48,.14);backdrop-filter:blur(6px);text-align:left;transition:transform .15s,border-color .15s}
.fb-card:hover{transform:translateY(-1px);border-color:rgba(213,43,30,.45)}
.fbc-ic{flex:none;width:34px;height:34px;border-radius:10px;background:rgba(213,43,30,.09);color:var(--red);display:flex;align-items:center;justify-content:center}
.fbc-ic svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.fbc-tx{display:flex;flex-direction:column;gap:1px}
.fbc-tx b{font-size:13px;font-weight:800;color:var(--ink)}
.fbc-tx small{font-size:10.5px;font-weight:600;color:var(--mut)}
.fbc-ar{flex:none;color:var(--red);font-weight:800;font-size:15px;margin-left:4px}
.fb-wrap .fb-panel{position:absolute;top:calc(100% + 8px);left:0;z-index:20}
@media(max-width:760px){
  .fb-wrap{left:14px;top:66px}
  .fb-card{padding:6px;border-radius:50%;gap:0}
  .fbc-ic{width:28px;height:28px;background:none}
  .fbc-tx,.fbc-ar{display:none}
  .fb-wrap .fb-panel{width:min(270px,calc(100vw - 28px))}
}
.fb-panel{display:flex;flex-direction:column;gap:8px;width:270px;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border:1px solid rgba(29,38,48,.10);border-radius:14px;padding:11px;box-shadow:0 16px 40px rgba(29,38,48,.20)}
.fb-text{width:100%;min-height:84px;resize:vertical;border-radius:7px;border:1px solid var(--line);background:#fff;color:var(--ink);padding:8px;font:inherit;font-size:12.5px;line-height:1.4}
.fb-text::placeholder{color:#98a1ad}
.fb-text:focus{outline:none;border-color:var(--red)}
.fb-send{align-self:flex-end;background:var(--red);color:#fff;border:none;border-radius:7px;padding:7px 16px;font-weight:800;font-size:12px;cursor:pointer;transition:filter .15s}
.fb-send:hover{filter:brightness(1.12)}
#home .home-hero .langsw{background:none;border-color:transparent}
#home .home-hero .langsw a{color:#39424e}
#home .home-hero .langsw a.active{background:#243b53;color:#fff}
#home .home-hero .langsw a:hover:not(.active){background:#f2f4f6;color:var(--ink)}
#home .hero-head{position:relative;z-index:6;text-align:left;padding:20px 0 0 28px;pointer-events:none}
#home .hero-head h1{font-size:clamp(56px,10vw,118px);margin:0;font-weight:800;letter-spacing:1px;text-shadow:0 3px 26px rgba(0,0,0,.6)}
#home .hero-head h1 b{color:#fff;font-weight:800}
#home .hero-head h1 .fF{color:#57cce4;text-shadow:0 0 12px rgba(87,204,228,.9),0 0 26px rgba(87,204,228,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fT{color:#ffd45c;text-shadow:0 0 12px rgba(255,212,92,.9),0 0 26px rgba(255,212,92,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fE{color:#ff9b57;text-shadow:0 0 12px rgba(255,155,87,.9),0 0 26px rgba(255,155,87,.6),0 2px 24px rgba(0,0,0,.5)}
#home .hero-head h1 .fM{color:#ff6d60;text-shadow:0 0 12px rgba(255,109,96,.95),0 0 26px rgba(255,109,96,.65),0 2px 24px rgba(0,0,0,.5)}
@keyframes ftemglow{0%,100%{filter:brightness(1)}50%{filter:brightness(1.28)}}
#home .hero-logo-lnk{pointer-events:auto;display:inline-block;cursor:pointer}
#home .hero-logo{display:block;margin:6px 0 0 4px;width:clamp(104px,15vw,168px);height:auto;filter:drop-shadow(0 1px 6px rgba(255,255,255,.65));transition:transform .15s}
#home .hero-logo-lnk:hover .hero-logo{transform:translateY(-1px)}
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
.mmodal{position:fixed;inset:0;z-index:300;background:rgba(8,12,20,.78);display:flex;align-items:center;justify-content:center;padding:18px}
.mm-box{width:min(1240px,96vw);height:min(880px,92vh);background:#fff;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.mm-bar{display:flex;align-items:center;gap:10px;padding:8px 12px;background:rgba(255,255,255,.95);color:var(--ink);border-bottom:1px solid var(--line)}
.mm-bar .mm-ext{color:var(--ink);border-color:rgba(29,38,48,.25)}
.mm-bar .mm-ext:hover{background:#f2f4f6}
.mm-bar .mm-x{color:#98a1ad}
.mm-bar .mm-x:hover{color:var(--red)}
[data-theme="dark"] .mm-bar{background:#1d2630;color:#fff;border-bottom-color:transparent}
[data-theme="dark"] .mm-bar .mm-ext{color:#fff;border-color:rgba(255,255,255,.4)}
[data-theme="dark"] .mm-bar .mm-x{color:rgba(255,255,255,.8)}
.mm-frame{opacity:0;transition:opacity .3s ease;background:#fff}
.mm-frame.ld{opacity:1}
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
/* FTEM-Zonen in der echten Bergsilhouette (SVG); Labels im SVG = immer exakt auf der Zone */
.heromt{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none}
/* 3D-FTEM-Knoepfe (Wiedererkennung zur alten Landingpage) */
.fbtns{position:absolute;inset:0;z-index:6;pointer-events:none}
.fbtnw{pointer-events:auto;position:absolute;transform:translateX(-50%);background:none;border:none;padding:0;cursor:pointer;text-align:center;font:inherit}
/* Helle Karten (Feedback Wala): weisse abgerundete Knoepfe, Buchstabe in der
   FTEM-Phasenfarbe, farbiger Schimmer; Position/Groesse unveraendert */
.fb3d{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;margin:0 auto;border-radius:20%;font-weight:800;line-height:1;letter-spacing:1px;padding:10px 8px 9px;
  background:rgba(255,255,255,.93);border:1.5px solid currentColor;
  backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
  box-shadow:0 12px 34px -6px color-mix(in srgb,currentColor 55%,transparent),0 2px 8px rgba(29,38,48,.10),inset 0 1px 0 rgba(255,255,255,.85);
  transition:transform .28s cubic-bezier(.2,.8,.3,1.15),box-shadow .28s ease,border-color .28s ease}
.fb-f{color:var(--found)}
.fb-t{color:var(--talent)}
.fb-e{color:var(--elite)}
.fb-m{color:var(--mast)}
/* Hover/Fokus: kraeftigerer farbiger Schimmer am aktiven Knopf */
.fbtns.hv-f .w-f .fb3d{box-shadow:0 0 0 3px rgba(31,143,166,.30),0 16px 40px -6px rgba(31,143,166,.65),0 2px 8px rgba(29,38,48,.10)}
.fbtns.hv-t .w-t .fb3d{box-shadow:0 0 0 3px rgba(226,169,0,.30),0 16px 40px -6px rgba(226,169,0,.65),0 2px 8px rgba(29,38,48,.10)}
.fbtns.hv-e .w-e .fb3d{box-shadow:0 0 0 3px rgba(232,119,46,.30),0 16px 40px -6px rgba(232,119,46,.65),0 2px 8px rgba(29,38,48,.10)}
.fbtns.hv-m .w-m .fb3d{box-shadow:0 0 0 3px rgba(213,43,30,.30),0 16px 40px -6px rgba(213,43,30,.65),0 2px 8px rgba(29,38,48,.10)}
.w-f{left:26%;top:68%}.w-t{left:38.5%;top:52%}.w-e{left:51%;top:37%}.w-m{left:63.5%;top:24%}
.fb3d .fl{font-style:normal;display:block}
.w-f .fb3d{width:146px}.w-f .fl{font-size:58px}
.w-t .fb3d{width:146px}.w-t .fl{font-size:58px}
.w-e .fb3d{width:102px}.w-e .fl{font-size:38px}
.w-m .fb3d{width:80px}.w-m .fl{font-size:28px}
.fbl{display:block;font-size:14.5px;font-weight:800;color:var(--ink);letter-spacing:.02em;line-height:1.25}
.fbl small{display:block;font-size:12px;font-weight:700;color:var(--mut)}
.w-e .fbl{font-size:12.5px}.w-e .fbl small{font-size:10.5px}
.w-m .fbl{font-size:11px}.w-m .fbl small{font-size:9.5px}
/* Hover/Fokus: nur der eigene Knopf waechst (die anderen bleiben ruhig) */
.fbtns.hv-f .w-f .fb3d,.fbtns.hv-t .w-t .fb3d,.fbtns.hv-e .w-e .fb3d,.fbtns.hv-m .w-m .fb3d{transform:scale(1.12)}
.fbtnw:focus-visible .fb3d{outline:3px solid rgba(31,143,166,.85);outline-offset:3px}
@media(max-width:760px){
  /* etwas hoeher, damit der F-Knopf nicht mit dem Athlet:innen-Weg-Knopf kollidiert */
  .w-f{left:15%;top:55%}.w-t{left:28%;top:47%}.w-e{left:41%;top:39.5%}.w-m{left:54%;top:32.5%}
  .w-f .fb3d{width:94px}.w-f .fl{font-size:33px}
  .w-t .fb3d{width:94px}.w-t .fl{font-size:33px}
  .w-e .fb3d{width:68px}.w-e .fl{font-size:23px}
  .w-m .fb3d{width:57px}.w-m .fl{font-size:18px}
  .fbl{font-size:9.5px}.fbl small{font-size:8px}
  .w-e .fbl{font-size:9px}.w-m .fbl{font-size:8.5px}
}
/* Breite, flache Fenster: Titel+Logo kompakter, damit sie den Gipfel nicht ueberlappen */
@media(min-aspect-ratio:19/10){
  #home .hero-logo{width:clamp(78px,8.5vw,116px);margin-top:4px}
}
.spmodal{position:fixed;inset:0;z-index:115;background:rgba(8,12,20,.68);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:18px}
.sp-box{width:min(760px,94vw);max-height:90vh;overflow:auto;background:var(--bg);border-radius:14px;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.sp-bar{display:flex;align-items:center;justify-content:space-between;padding:10px 15px;background:#1d2630;color:#fff;font-weight:800;font-size:13px;letter-spacing:.06em}
.sp-x{background:none;border:none;color:#fff;font-size:17px;cursor:pointer;line-height:1}
.sp-x:hover{color:var(--talent)}
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;padding:14px}
.sp-grid a{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:10px;padding:9px 12px;text-decoration:none;color:var(--ink)}
.sp-grid a:hover{border-color:var(--red)}
.sp-grid a b{font-size:13px}
.sp-grid img,.sp-grid .spcode{width:34px;height:34px;border-radius:50%;object-fit:cover;flex:none}
.sp-grid .spcode{display:flex;align-items:center;justify-content:center;background:var(--red);color:#fff;font-size:10px;font-weight:800}
.adminlink{text-align:center;margin-top:26px}
.adminlink a{display:inline-flex;opacity:.42;text-decoration:none;transition:opacity .16s,transform .16s}
.adminlink a:hover{opacity:1;transform:translateY(-1px)}
.adminlink svg{width:22px;height:22px}
/* Meeting-Paket: Hero-Buttons, Overlays, Titel-Dropdown, Steady, Mobile-Header */
.homesport{font:inherit;font-size:13.5px;font-weight:700;color:#fff;background:rgba(15,21,32,.55);border:1px solid rgba(255,255,255,.42);border-radius:9px;padding:9px 14px;backdrop-filter:blur(6px);width:100%;cursor:pointer;text-shadow:0 1px 4px rgba(0,0,0,.4)}
.homesport{color-scheme:dark}
.homesport option{color:#1d2630;background:#fff}
.hero-top-r{position:absolute;top:16px;right:18px;z-index:7}
.news-btn{background:var(--red);color:#fff;border:none;border-radius:8px;padding:6px 15px;font-size:11.5px;font-weight:800;letter-spacing:.04em;cursor:pointer}
.news-btn:hover{filter:brightness(1.12)}
.hero-top-r{display:flex;flex-direction:column;align-items:stretch;gap:8px;width:265px}
.info-btn{font:inherit;background:rgba(15,21,32,.55);border:1px solid rgba(255,255,255,.42);color:#fff;font-weight:800;font-size:11.5px;border-radius:8px;padding:6px 13px;cursor:pointer;backdrop-filter:blur(6px);text-shadow:0 1px 4px rgba(0,0,0,.4)}
.info-btn:hover{background:var(--red);border-color:var(--red)}
.hero-cta{display:flex;gap:10px;justify-content:center;margin-top:14px;pointer-events:auto}
.hcta{font:inherit;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.32);color:#fff;font-weight:800;font-size:13px;border-radius:20px;padding:8px 17px;cursor:pointer;backdrop-filter:blur(6px);text-decoration:none}
.hcta:hover{background:var(--red);border-color:var(--red)}
.hcta-sec{background:rgba(255,255,255,.07)}
.imodal{position:fixed;inset:0;z-index:290;background:rgba(8,12,20,.68);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:18px}
.im-box{width:min(900px,94vw);max-height:92vh;max-height:92svh;background:var(--bg);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 24px 70px rgba(0,0,0,.45)}
.imodal.wide{background:rgba(8,12,20,.35)}
.imodal.wide .im-box{width:fit-content;min-width:min(640px,94vw);max-width:min(1300px,96vw);
  background:rgba(240,244,248,.58);backdrop-filter:blur(16px) saturate(1.15);-webkit-backdrop-filter:blur(16px) saturate(1.15);
  border:1.5px solid rgba(255,255,255,.55)}
.imodal.wide .im-body .ph-sum.ph-wide{max-width:none}
.imodal.wide .ps-theme{background:rgba(255,255,255,.6)}
.imodal.wide .ps-cols{grid-template-columns:repeat(var(--nc,1),minmax(220px,258px))}
[data-theme="dark"] .imodal.wide .im-box{background:rgba(20,30,44,.66);border-color:rgba(255,255,255,.18)}
[data-theme="dark"] .imodal.wide .ps-theme{background:rgba(23,34,49,.72)}
/* Stufen-Popup: standardmaessig nur so hoch wie noetig; waechst beim Ausklappen */
.imodal.wide .im-box.grown{height:92vh;height:92svh}
.im-bar{display:flex;align-items:center;gap:10px;padding:9px 14px;background:rgba(255,255,255,.95);color:var(--ink);border-bottom:1px solid var(--line)}
.im-t{font-weight:800;font-size:13px;flex:1}
.im-x{background:none;border:none;color:#98a1ad;font-size:17px;cursor:pointer;padding:2px 8px;line-height:1}
.im-x:hover{color:var(--red)}
[data-theme="dark"] .im-bar{background:#1d2630;color:#fff;border-bottom-color:transparent}
[data-theme="dark"] .im-x{color:rgba(255,255,255,.75)}
[data-theme="dark"] .im-x:hover{color:var(--talent)}
.im-body{padding:16px;overflow:auto;position:relative}
.im-body .news-h{display:none}
.im-body .ftem-info{margin-top:0}
.mlist{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.mlist .mission-item{display:block;text-align:center;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:13px 10px;font-weight:800;font-size:13px;color:var(--ink);text-decoration:none}
.mlist .mission-item:hover{border-color:var(--red);color:var(--red)}
header.top .sportsel2{font:inherit;font-size:15px;font-weight:800;color:var(--ink);max-width:280px;padding:6px 10px;border:1px solid var(--line);border-radius:9px;background:var(--card)}
.steady{position:fixed;right:18px;bottom:74px;z-index:95;display:flex;align-items:center;gap:11px;background:var(--red);color:#fff;border:none;border-radius:36px;padding:16px 27px;font:inherit;font-size:16.5px;font-weight:800;letter-spacing:.01em;cursor:pointer;box-shadow:0 12px 32px rgba(0,0,0,.36),0 0 0 5px rgba(213,43,30,.16);animation:steadybob 3s ease-in-out infinite}
.steady:hover{filter:brightness(1.12);transform:translateY(-1px)}
@media(max-width:760px){.steady{padding:13px 21px;font-size:14.5px;bottom:66px}}
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
a.news-btn{text-decoration:none;display:inline-block;text-align:center}
/* News-Badge + News-Overlay-Metadaten */
.nbadge{display:inline-block;background:var(--red);color:#fff;border-radius:9px;padding:0 6px;margin-left:7px;font-size:10px;font-weight:800;line-height:15px;vertical-align:1px}
/* News-Box: Knopf + Teaser-Titel in einem Feld */
/* News-Box (Vorschlag 5B): breiter, groessere Schrift, CTA-Balken im FTEM-Verlauf */
.news-box{width:308px;align-self:flex-end;background:rgba(255,255,255,.94);backdrop-filter:blur(6px);border:1px solid rgba(29,38,48,.10);border-radius:14px;overflow:hidden;cursor:pointer;text-align:left;transition:border-color .15s;box-shadow:0 14px 40px rgba(29,38,48,.16)}
.news-box:hover{border-color:rgba(213,43,30,.45)}
.news-box .nb-head{color:var(--ink);font-weight:800;font-size:13.5px;letter-spacing:.03em;padding:11px 14px 3px}
/* News-Eintraege als helle Pill-Knoepfe (Feedback Bjoern) */
/* News-Eintraege mit Teaser + "Mehr lesen" (Bjoern-Mock) */
.news-box .nb-list{list-style:none;margin:2px 0 4px;padding:0 14px;color:#39424e}
.news-box .nb-list li{position:relative;padding:8px 0 8px 15px;font-size:12px}
.news-box .nb-list li+li{border-top:1px solid #eef0f3}
.news-box .nb-list li::before{content:'';position:absolute;left:2px;top:14px;width:5px;height:5px;border-radius:50%;background:var(--red)}
.news-box .nb-item{display:flex;flex-direction:column;gap:2px}
.news-box .nb-t{font-weight:800;color:var(--ink);line-height:1.3}
.news-box .nb-teaser{font-size:11px;font-weight:500;color:#5b6472;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.news-box .nb-lnk{align-self:flex-end;font-size:11px;font-weight:800;color:var(--red);text-decoration:none;letter-spacing:.01em;margin-top:2px}
.news-box .nb-lnk:hover{text-decoration:underline}
.news-box .nb-more{display:block;text-align:center;font-weight:800;font-size:12px;color:var(--red);margin:6px 14px 13px;padding:8px 14px;border:1px solid rgba(29,38,48,.14);border-radius:999px;background:#fff;box-shadow:0 2px 8px rgba(29,38,48,.06);letter-spacing:.02em;transition:background .15s,border-color .15s}
.news-box:hover .nb-more{background:#fdf3f2;border-color:rgba(213,43,30,.5)}
@media(max-width:760px){
  .news-box{width:100%;align-self:stretch}
  .news-box .nb-teaser{display:none}
  .news-box .nb-list li{padding:6px 0 6px 15px}
  .news-box .nb-item{flex-direction:row;align-items:baseline;gap:8px}
  .news-box .nb-t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:11.5px}
  .news-box .nb-lnk{align-self:auto;flex:none}
  .news-box .nb-more{font-size:11px;padding:6px 12px;margin:4px 12px 10px}
}
/* Feedback unten rechts */
/* Hamburger-Menue oben rechts */
.menu-btn,.lang-ic-btn{width:40px;height:40px;padding:0;display:inline-flex;align-items:center;justify-content:center;background:rgba(255,255,255,.92);color:var(--ink);border:1px solid rgba(29,38,48,.12);border-radius:999px;cursor:pointer;backdrop-filter:blur(6px);flex:none;box-shadow:0 4px 14px rgba(29,38,48,.10)}
.menu-btn svg,.lang-ic-btn svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.menu-btn:hover,.lang-ic-btn:hover{background:#fff;border-color:rgba(29,38,48,.28)}
.lang-ic{position:relative}
.lang-ic-menu{position:absolute;top:calc(100% + 6px);left:0;z-index:9;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border:1px solid rgba(29,38,48,.10);border-radius:12px;padding:5px;box-shadow:0 12px 30px rgba(29,38,48,.20)}
.lang-ic-menu[hidden]{display:none}
.lang-ic-menu .langsw{background:none;border:none;padding:0;flex-direction:column;gap:2px}
.lang-ic-menu .langsw a{padding:6px 18px;text-align:center;border-radius:6px}
.menu-panel{position:relative;display:flex;flex-direction:column;gap:6px;width:100%;background:rgba(255,255,255,.97);backdrop-filter:blur(8px);border:1px solid rgba(29,38,48,.08);border-radius:16px;padding:30px 9px 9px;box-shadow:0 18px 50px rgba(29,38,48,.20);color:var(--ink)}
.mp-x{position:absolute;top:4px;right:7px;background:none;border:none;color:#98a1ad;font-size:18px;line-height:1;cursor:pointer;padding:3px 7px}
.mp-x:hover{color:var(--ink)}
.mp-item{font:inherit;display:block;width:100%;text-align:left;background:#fff;border:1px solid var(--line);color:var(--ink);font-weight:700;font-size:12.5px;border-radius:10px;padding:9px 12px;cursor:pointer;transition:border-color .12s,color .12s,background .12s}
.mp-item:hover{border-color:var(--red);color:var(--red);background:#fdf5f4}
.mp-app{display:none}
@media(max-width:760px){.mp-app{display:block}}
.menu-panel .fb-btn{width:100%;text-align:left;border-radius:10px;padding:9px 12px;font-size:12.5px;box-shadow:none;background:#fff;border:1px solid var(--line);color:var(--ink);letter-spacing:0}
.menu-panel .fb-btn:hover{filter:none;border-color:var(--red);color:var(--red);background:#fdf5f4}
.menu-panel .fb-panel{width:100%;background:rgba(255,255,255,.97);border:1px solid rgba(29,38,48,.10);box-shadow:0 16px 40px rgba(29,38,48,.18)}
.menu-panel .fb-text{background:#fff;border:1px solid var(--line);color:var(--ink)}
.menu-panel .fb-text::placeholder{color:#98a1ad}
.menu-panel .fb-x{color:#98a1ad}
.menu-panel .fb-x:hover{color:var(--ink)}
.mp-admin{display:flex;align-items:center;justify-content:center;gap:14px;margin:0;padding:0;border:none}
.mp-admin .presopen{display:inline-flex;padding:2px;opacity:.42}
.mp-admin .presopen:hover{opacity:1}
.mp-admin .presopen svg{width:20px;height:20px;display:block}
.mp-admin .presask{margin-left:0}
.mp-admin .presask input{width:104px}
@media(max-width:760px){
  .hero-top-r{width:232px}
  .hero-top-r .langsw a{padding:4px 7px}
  .homesport{font-size:12.5px;padding:7px 10px}
  .bottombar{flex-wrap:wrap;justify-content:center;gap:4px 8px;padding:6px 10px}
  .bb-div{display:none}
  .bb-intro{order:1;width:100%;text-align:center}
  .bb-links{order:2;flex:none;justify-content:center;width:100%}
  .bb-app{display:inline-block;order:3;font-size:10.5px;padding:4px 10px}
  .bb-mission{order:4;flex-direction:row;align-items:center;gap:7px;padding:3px 7px}
  .bb-mission b{font-size:11.5px}
  .bb-mission .bb-mlogo{height:10px}
  .bb-tools{order:5;margin-left:0}
  .bb-intro{margin-right:0;text-align:center;font-size:9.5px;line-height:1.25}
  .bb-links{flex-wrap:wrap;justify-content:center;gap:4px}
  .bb-item{padding:4px 10px;font-size:10.5px}
  .imodal{align-items:flex-start;padding:0}
  .im-box{width:100vw;max-height:100vh;max-height:100svh;border-radius:0}
  .imodal.wide .im-box{width:100vw;height:100vh;height:100svh}
  .im-bar{padding:10px 14px;padding-top:max(10px,env(safe-area-inset-top))}
  .im-x{font-size:22px;padding:8px 12px;margin:-6px -8px -6px 0}
}
.news-upd{font-size:11px;color:var(--mut);font-weight:600;margin:-2px 0 10px}
.news-meta{display:flex;align-items:center;gap:7px;margin-bottom:4px}
.news-date{font-size:10.5px;font-weight:700;color:var(--mut);background:var(--acc-bg);border-radius:5px;padding:2px 7px}
.news-new{font-size:9.5px;font-weight:800;letter-spacing:.06em;color:#fff;background:var(--red);border-radius:5px;padding:2px 6px}
/* Feedback-Panel: Schliessen-Knopf */
.fb-panel{position:relative}
.fb-x{position:absolute;top:4px;right:6px;z-index:2;background:none;border:none;color:#98a1ad;font-size:17px;line-height:1;cursor:pointer;padding:3px 6px}
.fb-x:hover{color:var(--ink)}
.fb-panel .fb-text{margin-top:14px}
/* "Athlet:innen Weg"-Knopf oben Mitte */
.aw-cta{position:absolute;top:16px;left:50%;transform:translateX(-50%);z-index:7;display:flex;align-items:center;gap:10px}
/* Info-Knopf rechts in der Fusszeile (Teil der bb-tools) */
.aw-btn{font:inherit;display:flex;align-items:center;gap:9px;background:var(--red);border:none;color:#fff;font-weight:800;font-size:13.5px;border-radius:24px;padding:10px 21px;cursor:pointer;box-shadow:0 8px 24px rgba(213,43,30,.35);letter-spacing:.02em;transition:transform .15s,filter .15s}
.aw-btn:hover{filter:brightness(1.1);transform:translateY(-1px)}
/* "Was ist FTEM?"-Info-Knopf (ohne Beschriftung) neben dem Athlet:innen-Weg */
.aw-info{width:32px;height:32px;border-radius:50%;background:#fff;border:1.5px solid rgba(213,43,30,.55);color:var(--red);font-weight:800;font-size:14.5px;font-family:Georgia,'Times New Roman',serif;font-style:italic;cursor:pointer;box-shadow:0 2px 8px rgba(29,38,48,.12);display:flex;align-items:center;justify-content:center;line-height:1;transition:border-color .15s,background .15s}
.aw-info:hover{border-color:var(--red);background:#fdf3f2}
.top-row{display:flex;gap:8px;align-items:stretch;width:100%}
.top-row .sportpick{flex:1;min-width:0}
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.sportpick{position:relative}
.sp-btn{display:flex;align-items:center;gap:9px;width:100%;font:inherit;font-size:13.5px;font-weight:700;color:var(--ink);background:rgba(255,255,255,.92);border:1px solid rgba(29,38,48,.12);border-radius:999px;padding:9px 14px;backdrop-filter:blur(6px);cursor:pointer;box-shadow:0 4px 14px rgba(29,38,48,.10)}
.sp-btn:hover{background:#fff;border-color:rgba(29,38,48,.28)}
.sp-cur-ic{display:flex;flex:none}
.sp-ic{width:19px;height:19px;flex:none;object-fit:contain}
[data-theme="dark"] .sp-opt .sp-ic{filter:invert(1) brightness(1.4)}
.sp-lbl{flex:1;min-width:0;text-align:left;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sp-chev{width:15px;height:15px;flex:none;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round;opacity:.85}
.sp-list{position:absolute;top:calc(100% + 6px);left:0;right:0;z-index:10;list-style:none;margin:0;padding:5px;max-height:58vh;overflow:auto;background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:11px;box-shadow:0 16px 42px rgba(0,0,0,.32)}
.sp-list[hidden]{display:none}
.sp-opt{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;color:#1d2630;font-size:13px;font-weight:600;cursor:pointer}
.sp-opt .sp-ic{width:20px;height:20px;color:#586474}
.sp-opt:hover,.sp-opt[aria-selected="true"]{background:var(--acc-bg,#eef2f6);color:var(--red)}
.sp-opt:hover .sp-ic,.sp-opt[aria-selected="true"] .sp-ic{color:var(--red)}
[data-theme="dark"] .sp-list{background:#1c2740;border-color:rgba(255,255,255,.14)}
[data-theme="dark"] .sp-opt{color:#e7edf5}
[data-theme="dark"] .sp-opt .sp-ic{color:#aeb8c6}
header.top select,.sportsel2,select.jump,.pd-sportsel,.abar select{-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%235b6672' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 13px center;background-size:13px;padding-right:34px}
[data-theme="dark"] header.top select,[data-theme="dark"] .sportsel2,[data-theme="dark"] select.jump,[data-theme="dark"] .pd-sportsel{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23c2ccd8' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E")}
.mr-row{display:flex;gap:8px;align-items:center;justify-content:flex-end;flex:none}
@media(max-width:760px){.aw-cta{top:auto;bottom:88px;left:18px;transform:none}.aw-btn{font-size:12px;padding:8px 16px}}
/* schlanke Fusszeile mit Mission Swiss-Ski */
.bottombar{position:absolute;left:0;right:0;bottom:0;z-index:8;display:flex;align-items:center;gap:14px;padding:8px 18px;background:rgba(255,255,255,.82);backdrop-filter:blur(10px);border-top:1px solid rgba(29,38,48,.08)}
/* Mission Sportart links in der Fusszeile (Bjoern-Mock, Farben wie gehabt) */
.bb-mission{font:inherit;flex:none;display:flex;flex-direction:column;align-items:flex-start;gap:2px;background:none;border:none;padding:4px 8px;cursor:pointer;border-radius:10px;transition:background .15s}
.bb-mission b{font-size:13px;font-weight:800;color:var(--ink);letter-spacing:.01em}
.bb-mission .bb-mlogo{height:12px;width:auto;display:block}
.bb-mission:hover{background:rgba(213,43,30,.06)}
.bb-mission:hover b{color:var(--red)}
.bb-div{flex:none;width:1px;height:30px;background:rgba(29,38,48,.14)}
.bb-intro{flex:none;color:#55606d;font-size:12px;font-weight:800;letter-spacing:.03em;line-height:1.3}
.bb-links{display:flex;align-items:center;flex:1;gap:10px;flex-wrap:wrap}
.bb-app{display:none}
.bb-tools{flex:none;display:flex;align-items:center;gap:10px;margin-left:auto}
.bb-tools .presask input{width:96px}
.bb-item{font:inherit;flex:none;white-space:nowrap;background:#fff;border:1px solid rgba(29,38,48,.14);border-radius:999px;color:var(--ink);font-weight:700;font-size:12.5px;padding:7px 16px;cursor:pointer;text-decoration:none;letter-spacing:.03em;box-shadow:0 2px 8px rgba(29,38,48,.06);transition:background .15s,border-color .15s,color .15s,transform .15s}
.bb-item b{color:var(--red);font-weight:800;margin-left:4px}
.bb-item:hover{border-color:var(--red);color:var(--red);transform:translateY(-1px)}
.aw-btn:hover{background:var(--red);border-color:var(--red)}
.aw-btn .aw-ar{display:inline-flex;width:20px;height:20px;border-radius:50%;background:rgba(255,255,255,.25);align-items:center;justify-content:center;font-size:13px}
/* Stufen-Summary-Overlay */
.ph-sum{max-width:560px;margin:0 auto}
.ph-sum .ps-head{display:flex;align-items:center;gap:13px;margin-bottom:11px}
.ph-sum .ps-badge{flex:none;width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:800;color:#fff;background:var(--psc,#4a5563)}
.ps-f{--psc:var(--found)}.ps-t{--psc:var(--talent)}.ps-e{--psc:var(--elite)}.ps-m{--psc:var(--mast)}
.ps-t .ps-badge{color:#3b2e00}
.ph-sum .ps-name{font-size:17px;font-weight:800}
.ph-sum .ps-rng{font-size:12px;font-weight:700;color:var(--mut)}
.ph-sum .ps-desc{font-size:13.5px;line-height:1.6;margin:0 0 15px}
.ph-sum.ph-wide{max-width:840px}
.ph-sum .ps-theme{border-left-color:#4a5563;margin-bottom:6px}
.ph-sum .ps-theme>summary{padding:8px 12px}
.ph-sum .ps-secbody{padding:4px 10px 10px}
.ph-sum .ps-desc{margin-bottom:14px}
.ph-sum .ps-cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:8px}
.ph-sum .ps-col{background:rgba(255,255,255,.88);border:1px solid rgba(255,255,255,.75);border-radius:9px;padding:0;font-size:11.5px;line-height:1.5;min-width:0;overflow:hidden}
.ph-sum .ps-col .cwrap{font-size:11.5px;line-height:1.5;color:#33404d;overflow-wrap:anywhere;padding:8px 11px 10px}
[data-theme="dark"] .ph-sum .ps-col{background:rgba(23,34,49,.85);border-color:rgba(255,255,255,.12)}
[data-theme="dark"] .ph-sum .ps-col .cwrap{color:#c2ccd8}
.ps-f .ps-col{--zc:#0d5e6e;--zbg:#e1f0f3}
.ps-t .ps-col{--zc:#8a6a00;--zbg:#f7edcf}
.ps-e .ps-col{--zc:#a8511a;--zbg:#f8e2d3}
.ps-m .ps-col{--zc:#9c1d14;--zbg:#f6dcd8}
.ph-sum .ps-st{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;
  background:var(--psc,#4a5563);color:#fff;font-weight:800;font-size:13.5px;text-align:center;padding:6px 6px}
.ph-sum .ps-st i{font-style:normal;color:rgba(255,255,255,.92);font-weight:600;font-size:9px;margin-left:0}
.ps-t .ps-st{color:#3b2e00}.ps-t .ps-st i{color:rgba(59,46,0,.85)}
.ph-sum .ps-desc{white-space:pre-line}
.ph-sum .ps-sec+.aw-go,.ph-sum .ps-sec:last-of-type{margin-bottom:14px}
.ph-sum .aw-go{font:inherit;font-size:13px;font-weight:800;color:#fff;background:var(--red);border:none;border-radius:9px;padding:10px 18px;cursor:pointer}
.ph-sum .aw-go:hover{filter:brightness(1.12)}
.fi-links{margin-top:16px}
/* Zebra im Darkmode: leicht aufhellen statt abdunkeln */
[data-theme="dark"] .grid .r:nth-child(odd):not(.head) .cell,[data-theme="dark"] .grid .r:nth-child(odd):not(.head) .rl{background-image:linear-gradient(rgba(255,255,255,.045),rgba(255,255,255,.045)),var(--mg)}
@media(max-width:760px){
  .aw-btn{font-size:12px;padding:8px 16px}
}
/* Praesentations-Deck (Vollbild-Folien) */
.presdeck{position:fixed;inset:0;z-index:200;background:var(--bg);display:flex;flex-direction:column}
.pd-top{display:flex;align-items:center;gap:14px;padding:9px 16px;background:#1d2630;color:#fff;flex:none}
.pd-name{font-weight:800;font-size:15px;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pd-sportsel{font:inherit;font-size:13px;font-weight:700;padding:6px 10px;border-radius:8px;border:none;background:#2a3644;color:#fff;cursor:pointer}
.pd-count{font-size:12.5px;font-weight:700;opacity:.75}
.pd-x{background:none;border:none;color:#fff;font-size:22px;cursor:pointer;padding:2px 8px;line-height:1}
.pd-x:hover{color:var(--talent)}
.pd-body{flex:1;overflow:auto;padding:34px 7vw 70px}
.pd-body.pd-hasifr{padding:0;overflow:hidden}
.pd-ifr{display:block;width:100%;height:100%;border:0;background:#fff}
.pd-body .ftem-info{max-width:1100px;margin:0 auto}
.pd-body .ftem-info h2{font-size:26px}
.pd-body .ftem-info .lead{font-size:16px;line-height:1.65}
.pd-body .fwd-h{font-size:14px}
.pd-body .fwd p{font-size:13px;line-height:1.55}
.pd-body .ph-sum,.pd-body .ph-sum.ph-wide{max-width:1200px;margin:0 auto}
.pd-body .ph-sum .ps-name{font-size:26px}
.pd-body .ph-sum .ps-rng{font-size:14px}
.pd-body .ph-sum .ps-badge{width:56px;height:56px;font-size:29px}
.pd-body .ph-sum .ps-desc{font-size:16.5px;line-height:1.6}
.pd-body .ph-sum .ps-col .cwrap{font-size:12.5px}
.pd-body .ph-sum .tt{font-size:15px}
.pd-body .aw-go{display:none}
.pd-body .fi-links{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;margin-top:22px}
.pd-body .fi-links .mission-item{flex:0 0 auto;min-width:210px;padding:15px 22px;font-size:13.5px}
.pd-web{max-width:1050px;margin:0 auto}
.pd-web h2{font-size:26px;margin:0 0 6px}
.pd-web .lead{color:var(--mut);font-size:16px;margin:0 0 22px}
.pd-web .lead b{color:var(--ink)}
.pd-feats{display:grid;grid-template-columns:1fr;gap:12px;max-width:640px}
.pd-feats .fwd{padding:13px 15px}
.pdw{font:inherit;text-align:left;width:100%;cursor:pointer;appearance:none;-webkit-appearance:none;transition:transform .14s,box-shadow .14s}
.pdw:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(0,0,0,.10)}
.pd-awslide{max-width:900px;margin:16vh auto 0;text-align:center}
.pd-awslide h2{font-size:32px;margin:0 0 12px}
.pd-awslide p{font-size:15px;color:var(--mut)}
.pd-prev,.pd-next{position:fixed;top:50%;transform:translateY(-50%);z-index:201;width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:26px;line-height:1;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.18)}
.presdeck[hidden]~.pd-prev{display:none}
.pd-prev{left:12px}.pd-next{right:12px}
.pd-prev:hover,.pd-next:hover{background:var(--acc-bg)}
body.deckon{overflow:hidden}
@media(max-width:760px){.pd-body{padding:22px 16px 60px}.pd-prev,.pd-next{width:38px;height:38px;font-size:21px;bottom:12px;top:auto;transform:none}}
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
@media(max-width:640px){.node .nicon{width:58px;height:58px}.node .nhover{width:96px}.node .nlabel{font-size:12px}#home .hero-head{padding-top:14px;padding-left:16px}#home .hero-head h1{font-size:42px}#home .hero-logo{width:80px;margin:-4px 0 0 4px}}
@media(max-width:480px){.node{padding:9px}.node .nlabel{font-size:10.5px;max-width:70px}.node .nhover{width:84px}.node .nicon{width:48px;height:48px}.node .dot{width:11px;height:11px}}
@media(max-width:350px){.node .nlabel{font-size:9.5px;max-width:60px}.node .dot{width:10px;height:10px}}
/* "Was ist FTEM?" */
.ftem-info{margin-top:46px;text-align:left;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:26px 26px 22px}
.ftem-info h2{margin:0 0 8px;font-size:17px;font-weight:800}
.ftem-info .lead{color:var(--mut);font-size:13px;line-height:1.6;margin:0 0 18px}
.ftem-info .lead b{color:var(--ink)}
/* Was ist FTEM? – aufsteigender Weg (Entwicklungsstufen F1–M) */
.fweg-wrap{margin:12px 0 8px}
.fweg{width:100%;height:auto;display:block}
.fweg-line{fill:none;stroke:#c3ccd6;stroke-width:2.5;stroke-linecap:round;stroke-dasharray:2 11;animation:fwflow 9s linear infinite}
@keyframes fwflow{to{stroke-dashoffset:-130}}
.fweg .wn circle{filter:drop-shadow(0 2px 5px rgba(0,0,0,.2))}
.fweg .wn-t{fill:#fff;font-size:13px;font-weight:800;font-family:Arial,sans-serif;text-anchor:middle;dominant-baseline:central}
.fweg .fmt1{fill:#e4e9ef}.fweg .fmt2{fill:#eef1f5}
.fweg .gcable{stroke:#8a94a0;stroke-width:1.4}
.gondel{offset-rotate:0deg;offset-distance:0%;animation:gondelup 8s ease-in-out infinite}
@keyframes gondelup{0%{offset-distance:0%}86%,100%{offset-distance:100%}}
[data-theme="dark"] .fweg .fmt1{fill:rgba(255,255,255,.06)}
[data-theme="dark"] .fweg .fmt2{fill:rgba(255,255,255,.035)}
.fweg .wl{font-size:13px;font-weight:800;font-family:'Inter',Arial,sans-serif;letter-spacing:.02em}
.fweg .we{fill:var(--mut);font-size:11px;font-weight:700;font-family:'Inter',Arial,sans-serif}
.fweg-desc{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:6px}
.fwd{background:var(--card);border:1px solid var(--line);border-top:3px solid;border-radius:10px;padding:9px 11px}
.fwd-f{border-top-color:var(--found)}.fwd-t{border-top-color:var(--talent)}.fwd-e{border-top-color:var(--elite)}.fwd-m{border-top-color:var(--mast)}
.fwd-h{font-size:12px;color:var(--ink)}.fwd-h b{font-weight:800}
.fwd p{margin:4px 0 0;font-size:11px;color:var(--mut);line-height:1.45}
[data-theme="dark"] .fweg-line{stroke:rgba(255,255,255,.28)}
@media(max-width:640px){.fweg-desc{grid-template-columns:1fr 1fr}}
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
/* Athlet:innen-Weg: Bergfoto dezent im Hintergrund (Vorschlag 2, abgeschwaecht) */
section.sport{background:linear-gradient(rgba(238,241,244,.94),rgba(238,241,244,.94)),url("assets/hero.jpg") center 30%/cover fixed no-repeat}
/* Alle Themenzeilen einheitlich weiss (kein Zebra mehr) */
section.sport details.theme{background:rgba(255,255,255,.97);backdrop-filter:blur(2px)}
section.sport .rl,section.sport .r.head .rl.corner{background:rgba(255,255,255,.94)}
[data-theme="dark"] section.sport{background:linear-gradient(rgba(13,20,32,.95),rgba(13,20,32,.95)),url("assets/hero.jpg") center 30%/cover fixed no-repeat}
[data-theme="dark"] section.sport details.theme{background:rgba(23,34,49,.90)}
[data-theme="dark"] section.sport .rl,[data-theme="dark"] section.sport .r.head .rl.corner{background:rgba(23,34,49,.96)}
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
.r{display:grid;grid-template-columns:var(--lblw) repeat(10,var(--colw));gap:6px;align-items:stretch}
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
.cell.ph-foundation{background:#f4faf8;--zc:#0d5e6e;--zbg:#e1f0f3}.cell.ph-talent{background:#fcf8ee;--zc:#8a6a00;--zbg:#f7edcf}.cell.ph-elite{background:#fdf5ef;--zc:#a8511a;--zbg:#f8e2d3}.cell.ph-mastery{background:#fcefef;--zc:#9c1d14;--zbg:#f6dcd8}.cell.ph-multi{background-color:#f7f8fa;background-image:var(--mg);--zc:#5a6472;--zbg:#eceff3}
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
.cell{background:#fff;border:1px solid var(--line);border-radius:8px;position:relative;overflow:hidden;align-self:stretch}
/* Zebra: jede zweite Inhaltszeile dezent abgedunkelt (Bjoern-Feedback) */
.grid .r:nth-child(odd):not(.head) .cell,.grid .r:nth-child(odd):not(.head) .rl{background-image:linear-gradient(rgba(29,38,48,.035),rgba(29,38,48,.035)),var(--mg)}
.cell .cwrap{padding:9px 11px;font-size:11.5px;line-height:1.5;color:#33404d;max-height:212px;overflow:hidden;transition:max-height .25s ease}
.cell.clamped .cwrap,.cell.expanded .cwrap{padding-bottom:34px}
.cell.expanded .cwrap{max-height:4000px}
.cell::after{content:'';position:absolute;left:0;right:0;bottom:0;height:32px;background:linear-gradient(180deg,transparent,#fff);pointer-events:none;opacity:0;transition:opacity .2s}
.cell.clamped::after{opacity:1}
.cell.expanded::after{opacity:0}
/* farbige Zellen-Oberkanten entfernt (nur noch dezente Grundlinie) */
.cwrap p{margin:0 0 5px;line-height:1.5}.cwrap p:last-child{margin-bottom:0}
.cwrap .bh,.cwrap .sh,.cwrap .bi{font-weight:700;color:var(--acc);font-size:9px;text-transform:uppercase;letter-spacing:.055em;margin:12px 0 4px;line-height:1.3}
.cwrap .bh:first-child,.cwrap .sh:first-child,.cwrap .bi:first-child{margin-top:0}
.cwrap .bh:not(:first-child),.cwrap .sh:not(:first-child),.cwrap .bi:not(:first-child){border-top:1px solid #e3e8ee;padding-top:10px}
/* Off-Snow / On-Snow Zonen */
.cwrap .zone{margin-top:11px}.cwrap .zone:first-child{margin-top:0}
.cwrap .zone+.zone{border-top:1px solid #e3e8ee;padding-top:10px}
.cwrap .zlab{display:inline-block;font-weight:700;font-size:9px;text-transform:uppercase;letter-spacing:.06em;color:var(--zc,#5a6472);background:var(--zbg,#eceff3);border-radius:5px;padding:2px 7px;margin:0 0 5px}
.cwrap .zsub{margin:0 0 4px;line-height:1.5}.cwrap .zsub:last-child{margin-bottom:0}
.cwrap .zk{font-weight:700;color:var(--ink)}.cwrap .zk::after{content:"·";margin:0 5px 0 4px;color:#b6c0cc;font-weight:400}
.cwrap .zsub-l .zk{display:block;margin:0 0 2px}.cwrap .zsub-l .zk::after{content:none}.cwrap .zsub-l ul{margin-top:2px}
.cwrap .lbl{font-weight:700;color:var(--acc)}
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
.chatpanel{position:fixed;inset:0;z-index:310;background:rgba(15,22,34,.42);display:flex;justify-content:flex-end}
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
.cp-chips{display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 2px;align-self:flex-start;max-width:96%}
.cp-chip{font:inherit;font-size:12px;font-weight:600;color:var(--red);background:var(--acc-bg);border:1px solid var(--line);border-radius:16px;padding:6px 12px;cursor:pointer;text-align:left;line-height:1.3;transition:background .12s,color .12s,border-color .12s}
.cp-chip:hover{background:var(--red);color:#fff;border-color:var(--red)}
@media(max-width:520px){.cp-card{width:100%}}
mark{background:#ffe08a;border-radius:2px;padding:0 1px}
/* Lange Woerter (z. B. Belastungsverträglichkeit) trennen statt abschneiden */
body{overflow-wrap:break-word}
.cwrap,.cwrap li,.rl,.ps-col,.im-body p,.im-body li,.fwd p,.phase p,.news-body,.mlist .mission-item,summary .tt{hyphens:auto;-webkit-hyphens:auto}
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
.ht-l{order:1;flex:1 1 auto;min-width:0}
header.top .sportsel2{flex:1 1 0;width:100%;min-width:118px;font-size:13.5px;max-width:none}
.ht-r .langsw a{padding:4px 6px;font-size:10.5px}
.ht-r .langsw{order:2;flex:none}
.ht-r .themebtn{order:2;flex:none}
.ht-c{flex:1 1 44%;order:3;min-width:0}
.ht-c .qbox{width:100%}
.ht-c input.q{font-size:16px;padding:0 56px 0 30px}
.ht-r select.jump{order:4;flex:1 1 44%;width:auto;min-width:172px;font-size:12px}
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
[data-theme="dark"] .cell.ph-foundation{background:#152731;--zc:#7fd6e8;--zbg:rgba(31,143,166,.14)}
[data-theme="dark"] .cell.ph-talent{background:#25220f;--zc:#f0cf72;--zbg:rgba(226,169,0,.18)}
[data-theme="dark"] .cell.ph-elite{background:#271c12;--zc:#f0a877;--zbg:rgba(232,119,46,.18)}
[data-theme="dark"] .cell.ph-mastery{background:#271413;--zc:#f09287;--zbg:rgba(213,43,30,.14)}
[data-theme="dark"] .cell.ph-multi{background-color:#1a2434;background-image:var(--mg);--zc:#aeb8c6;--zbg:rgba(255,255,255,.08)}
[data-theme="dark"]{--phf:#152731;--pht:#25220f;--phe:#271c12;--phm:#271413}
[data-theme="dark"] .cell.hl-foundation{background:rgba(31,143,166,.22)}
[data-theme="dark"] .cell.hl-talent{background:rgba(226,169,0,.14)}
[data-theme="dark"] .cell.hl-elite{background:rgba(232,119,46,.14)}
[data-theme="dark"] .cell.hl-mastery{background:rgba(213,43,30,.22)}
[data-theme="dark"] .cell::after{background:linear-gradient(180deg,rgba(23,34,49,0),#172231)}
[data-theme="dark"] .cwrap{color:#c2ccd8}
[data-theme="dark"] .cwrap .bh:not(:first-child),[data-theme="dark"] .cwrap .sh:not(:first-child),[data-theme="dark"] .cwrap .bi:not(:first-child){border-top-color:rgba(255,255,255,.10)}
[data-theme="dark"] .cwrap .zone+.zone{border-top-color:rgba(255,255,255,.10)}
[data-theme="dark"] .cwrap .zk::after{color:#5a6472}
[data-theme="dark"] .cwrap ul.sc .badge{background:#33425c;color:#e7edf4}
[data-theme="dark"] .cwrap .empty{color:#4a5568}
[data-theme="dark"] .more{background:#1c2740;color:var(--ink);border-color:rgba(255,255,255,.14)}
[data-theme="dark"] .lks a{background:#1c2740;color:#d6dee8}
[data-theme="dark"] .lks a:hover{background:#2a3a55;color:#fff}
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
const SPORT_MISSIONS = __SPORT_MISSIONS__;
const SPORT_NAMES = __SPORT_NAMES__;
const I18N = __I18N__;
const PAGELANG="__PAGELANG__";
const sections = [...document.querySelectorAll('section.sport')];
const home = document.getElementById('home');

// ---- Live-Overrides aus dem Admin-Bereich (Supabase) ----
const SUPA_URL="__SUPA_URL__", SUPA_KEY="__SUPA_KEY__";
function _esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
const SC_RE=/^(SC\s?\d+[a-z]?|SC|ST\s?\d*|ST)\s*[:.\)]\s*([\s\S]*)$/;
const SNOW_RE=/^(on|off)[\s-]?snow:?$/i;
function structBlock(b){
  b=b.replace(/\s+$/,'');
  if(!b.trim())return '';
  const lines=b.split('\n');
  const nonempty=lines.map(l=>l.trim()).filter(Boolean);
  // "ON SNOW" / "OFF SNOW" als Kopfzeile -> Zonen-Chip (gleich wie beim Seiten-Build)
  if(SNOW_RE.test(lines[0].trim())){
    const lab=/^on/i.test(lines[0].trim())?'On-Snow':'Off-Snow';
    const items=[],other=[];
    lines.slice(1).forEach(l=>{const ls=l.trim();if(!ls)return;
      if('-–•'.indexOf(ls[0])>=0)items.push(ls.replace(/^[-–•]+/,'').trim());
      else if(items.length)items[items.length-1]+=' '+ls;
      else other.push(ls);});
    let body='';
    if(other.length)body+='<p>'+_esc(other.join(' '))+'</p>';
    if(items.length)body+='<ul class="bl">'+items.filter(Boolean).map(i=>'<li>'+_esc(i)+'</li>').join('')+'</ul>';
    return '<div class="zone"><span class="zlab">'+lab+'</span>'+body+'</div>';
  }
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
function _fnv36(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)>>>0;}return h.toString(36);}
function applyOverrides(map){
  // Klartext-Ziele (Titel, Einleitungen, News): nur Text ersetzen, <b>/<i> erlaubt
  function plain(v){return _esc(v).replace(/&lt;(\/?)(b|i)&gt;/g,'<$1$2>').replace(/\n/g,'<br>');}
  // Sprachspezifische Overrides ("cid|fr" usw.) haben Vorrang und gelten nur auf
  // der jeweiligen Sprachseite. Deutsche Overrides (ohne Suffix) gelten als
  // Fallback auf allen Seiten - aber nur, wenn sie sich vom deutschen Quelltext
  // unterscheiden (data-bh), sonst wuerden sie die Uebersetzungen ueberdecken.
  const lm={},gm={};
  Object.keys(map).forEach(c=>{
    const m2=c.match(/^(.*)\|(fr|it|en)$/);
    if(m2){ if(m2[2]===PAGELANG) lm[m2[1]]=map[c]; }
    else gm[c]=map[c];
  });
  function pick(el){
    const cid=el.dataset.cid;
    if(lm[cid]!=null)return lm[cid];
    const v=gm[cid];
    if(v==null)return null;
    const bh=el.dataset.bh;
    if(bh&&_fnv36(v)===bh)return null;
    return v;
  }
  function patch(root){
    root.querySelectorAll('.ctext[data-cid]').forEach(el=>{
      const v=pick(el);
      if(v!=null){el.innerHTML=structCell(v);}
    });
    root.querySelectorAll('.ovr-txt[data-cid]').forEach(el=>{
      const v=pick(el);
      if(v!=null){el.innerHTML=plain(v);}
    });
  }
  patch(document);
  // Inhalte in <template> (Stufen-Popups, News-Overlay, "Was ist FTEM?") ebenfalls patchen
  document.querySelectorAll('template').forEach(t=>patch(t.content));
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
      btn.onclick=()=>{
        const ex=!cell.classList.contains('expanded');
        const row=cell.closest('.r')||cell.parentElement;
        row.querySelectorAll('.cell').forEach(c=>{
          c.classList.toggle('expanded',ex&&c.classList.contains('clamped'));
          const b2=c.querySelector('.more');if(b2&&!b2.hidden)b2.textContent=ex?I18N.less:I18N.more;
        });
      };
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
  sec.querySelector('.jump').onchange=e=>{
    const el=document.getElementById(e.target.value);
    if(el){
      el.open=true;
      const go=()=>{
        const hh=(sec.querySelector('header.top')||{offsetHeight:54}).offsetHeight;
        const y=el.getBoundingClientRect().top+window.scrollY-hh-12;
        window.scrollTo({top:Math.max(0,y),behavior:'smooth'});
      };
      setTimeout(go,80);setTimeout(go,550);  // zweiter Sprung nach dem Clamp-Layout
    }
    e.target.selectedIndex=0;
  };
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
      let hl=false;
      for(const i of active){if(i>=f&&i<=t){c.classList.add('hl-'+phaseIdx(i));hl=true;break;}}
      // Phasenuebergreifende Zellen: Farbverlauf bei Hervorhebung ausblenden
      if(c.__mg===undefined)c.__mg=c.style.getPropertyValue('--mg')||null;
      if(c.__mg)c.style.setProperty('--mg',hl?'linear-gradient(rgba(0,0,0,0),rgba(0,0,0,0))':c.__mg);
    });
  }
  function toggleStage(i){const had=active.has(i);active.clear();if(!had)active.add(i);applyHl();}
  sec.querySelectorAll('.c.hd[data-idx]').forEach(h=>h.addEventListener('click',()=>toggleStage(+h.dataset.idx)));
  function scrollToStage(i){
    const d=sec.querySelector('details.theme[open]');
    if(!d)return;
    // Auch verbundene Zellen komplett zeigen: fruehester Spaltenstart aller
    // Zellen, die Stufe i enthalten (z. B. F1-2 -> beim Sprung auf F2 ab F1)
    let j=i;
    d.querySelectorAll('.cell').forEach(c=>{const f=+c.dataset.from,t=+c.dataset.to;if(i>=f&&i<=t&&f<j)j=f;});
    const h=d.querySelector('.c.hd[data-idx="'+j+'"]');
    if(!h)return;
    const sc=h.closest('.scroller');if(!sc)return;
    // Erste Spalte: ganz nach links (kein Restversatz)
    const x=j===0?0:Math.max(0, sc.scrollLeft + h.getBoundingClientRect().left - sc.getBoundingClientRect().left
      - (sec.querySelector('.rl')?sec.querySelector('.rl').getBoundingClientRect().width:146) - 14);
    scrollers.forEach(o=>{o.scrollTo({left:x,behavior:'smooth'});});
    sec.__sx=x;
  }
  sec.querySelectorAll('.stagebar .sb').forEach(b=>b.addEventListener('click',()=>{const i=+b.dataset.si;toggleStage(i);if(active.has(i))scrollToStage(i);}));
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
 +'<span class="cp-t">'+_esc(I18N.chatTitle)+'</span><button class="cp-x" type="button" aria-label="'+_esc(I18N.printClose)+'">&times;</button></div>'
 +'<div class="cp-msgs"></div>'
 +'<form class="cp-form"><input class="cp-in" type="text" autocomplete="off" placeholder="'+_esc(I18N.chatPh)+'"><button class="cp-send" type="submit" aria-label="'+_esc(I18N.send)+'">&#10148;</button></form>'
 +'<div class="cp-note">'+_esc(I18N.chatNote)+'</div></div>';
document.body.appendChild(chatPanel);
const cpMsgs=chatPanel.querySelector('.cp-msgs'),cpForm=chatPanel.querySelector('.cp-form'),cpIn=chatPanel.querySelector('.cp-in'),cpSend=chatPanel.querySelector('.cp-send');
let chatSec=null,chatBusy=false;const chatHist=[];const chatWelcomed=new Set();
function openChat(sec){chatSec=sec;chatPanel.hidden=false;document.documentElement.style.overflow='hidden';
  const id=sec.dataset.sport;
  if(!chatWelcomed.has(id)){cpMsgs.innerHTML='';chatHist.length=0;addMsg('a',I18N.chatWelcome);addExamples();chatWelcomed.add(id);}
  setTimeout(()=>cpIn.focus(),60);}
function addExamples(){var ex=I18N.chatExamples||[];if(!ex.length)return;
  var wrap=document.createElement('div');wrap.className='cp-chips';
  ex.forEach(function(q){var b=document.createElement('button');b.type='button';b.className='cp-chip';b.textContent=q;
    b.onclick=function(){cpIn.value=q;if(cpForm.requestSubmit)cpForm.requestSubmit();else cpForm.dispatchEvent(new Event('submit',{cancelable:true}));};
    wrap.appendChild(b);});
  cpMsgs.appendChild(wrap);cpMsgs.scrollTop=cpMsgs.scrollHeight;}
function closeChat(){chatPanel.hidden=true;document.documentElement.style.overflow='';}
chatPanel.addEventListener('click',e=>{if(e.target===chatPanel||e.target.closest('.cp-x'))closeChat();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!chatPanel.hidden){closeChat();e._ovl=true;}});
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
  var _ch=cpMsgs.querySelector('.cp-chips');if(_ch)_ch.remove();
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
  const fr=mm.querySelector('.mm-frame');
  fr.classList.remove('ld');            // weich einblenden, sobald geladen (kein Flackern)
  fr.onload=()=>fr.classList.add('ld');
  fr.src=url;
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
  if(e.key==='Escape'){ if(!mm.hidden){closeMission();e._ovl=true;} else closePops(); }
});

// ---- Inhalts-Overlay (News, Was ist FTEM?, Missions-Auswahl) ----
const im=document.querySelector('.imodal');
function openInfo(tplId,title){
  im.querySelector('.im-body').innerHTML=document.getElementById(tplId).innerHTML;
  // Stufen-Popups: Titel aus dem (ggf. per Admin-Override angepassten) Inhalt ableiten
  if(tplId.indexOf('tpl-ph-')===0){
    const nm=im.querySelector('.im-body .ps-name'),rg=im.querySelector('.im-body .ps-rng');
    if(nm&&rg)title=nm.textContent.trim()+' · '+rg.textContent.trim();
  }
  im.querySelector('.im-t').textContent=title;
  im.classList.toggle('wide', tplId.indexOf('tpl-ph-')===0);
  im.querySelector('.im-box').classList.remove('grown'); // frisch geoeffnet = kompakt
  im.hidden=false;
}
// Stufen-Popup: Akkordeon + automatisch so skalieren, dass der offene
// Abschnitt ohne Scrollen komplett sichtbar ist
function fitSec(d){
  const cols=d.querySelector('.ps-cols'), body=d.querySelector('.ps-secbody');
  if(!cols||!body)return;
  cols.style.transform='';cols.style.width='';body.style.height='';body.style.overflow='';
  const imb=im.querySelector('.im-body');
  const avail=imb.clientHeight - d.querySelector('summary').getBoundingClientRect().height - 64;
  const need=cols.scrollHeight;
  if(need>avail&&avail>120){
    const r=Math.max(.5, avail/need);
    cols.style.transformOrigin='top left';
    cols.style.transform='scale('+r+')';
    cols.style.width=(100/r)+'%';
    body.style.height=Math.ceil(need*r+8)+'px';
    body.style.overflow='hidden';
  }
  setTimeout(()=>{imb.scrollTo({top:Math.max(0,d.offsetTop-10),behavior:'smooth'});},40);
}
im&&im.addEventListener('toggle',e=>{
  const d=e.target;
  if(!d.matches||!d.matches('.im-body details.ps-theme'))return;
  // Fenster nur so gross wie noetig: waechst, sobald ein Abschnitt offen ist
  const box=im.querySelector('.im-box');
  if(d.open)im.querySelectorAll('.im-body details.ps-theme').forEach(o=>{if(o!==d)o.open=false;});
  const anyOpen=!!im.querySelector('.im-body details.ps-theme[open]');
  if(box)box.classList.toggle('grown',anyOpen);
  if(!d.open)return;
  fitSec(d);
},true);
// Themen/Abschnitte: Auf-/Zuklappen zuverlaessig ueber die GESAMTE Balkenbreite
// (delegiert, gilt auch fuer nachgeladene Inhalte in Popups und Praesentation)
document.addEventListener('click',e=>{
  const su=e.target.closest('summary');
  if(!su)return;
  const d=su.parentElement;
  if(!d||!d.matches||!d.matches('details.theme,details.ps-theme'))return;
  if(e.target.closest('a,button,select,input'))return;
  e.preventDefault();
  d.open=!d.open;
});
function closeInfo(){im.hidden=true;}
if(im){
  im.addEventListener('click',e=>{if(e.target===im)closeInfo();});
  im.querySelector('.im-x').addEventListener('click',closeInfo);
}
document.querySelectorAll('[data-open]').forEach(b=>b.addEventListener('click',()=>{if(document.getElementById(b.dataset.open))openInfo(b.dataset.open,b.dataset.t||'');}));
// Direktlinks in der News-Box: extern oeffnen, ohne das News-Overlay auszuloesen
document.querySelectorAll('.news-box .nb-lnk').forEach(a=>a.addEventListener('click',e=>{
  e.stopPropagation();e.preventDefault();
  let href=a.getAttribute('href')||'';
  if(a.dataset.urls){try{
    const m=JSON.parse(a.dataset.urls);
    const sid=(typeof homeSport!=='undefined'&&homeSport&&homeSport.value)?homeSport.value:'';
    href=m[sid]||m['default']||href;
  }catch(_){}}
  window.open(href,'_blank','noopener');
}));

// Alle externen Links (Dokumente, News, Missionen) im Iframe-Overlay oeffnen
document.addEventListener('click',e=>{
  const a=e.target.closest('.lks a, .news-link, .np-mission, .mission-item');
  if(!a)return;
  e.preventDefault();
  let href=a.getAttribute('href')||'';
  // Sportart-abhaengige News-Links (data-urls: {sportId: url, default: url})
  if(a.dataset.urls){try{
    const m=JSON.parse(a.dataset.urls);
    const sec=sections.find(s=>!s.hidden);
    const sid=sec?sec.dataset.sport:((typeof homeSport!=='undefined'&&homeSport&&homeSport.value)?homeSport.value:'');
    href=m[sid]||m['default']||href;
  }catch(_){}}
  // www.swiss-ski.ch verbietet Einbettung (X-Frame-Options: deny) -> neuer Tab statt iframe
  let host='';try{host=new URL(href,location.href).hostname;}catch(_){}
  if(host==='www.swiss-ski.ch'||host==='swiss-ski.ch'){window.open(href,'_blank','noopener');return;}
  if(im&&!im.hidden)closeInfo();
  openMission(href, a.dataset.title||a.textContent.replace('↗','').trim());
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&im&&!im.hidden){closeInfo();e._ovl=true;}});

// ---- Sportarten-Dropdown im Titel + Steady-Chat-Knopf ----
sections.forEach(s=>{const ss=s.querySelector('.sportsel2');if(ss)ss.addEventListener('change',e=>{location.hash='#'+e.target.value;});});
const steadyBtn=document.querySelector('.steady');
if(steadyBtn)steadyBtn.addEventListener('click',()=>{const sec=sections.find(x=>!x.hidden);if(sec)openChat(sec);});

// ---- Startseite: Stufen-Klick -> Kurz-Summary; Piste/AW-Knopf -> Athlet:innen-Weg ----
const homeSport=document.querySelector('.homesport');
document.querySelectorAll('.sportpick').forEach(sp=>{
  const btn=sp.querySelector('.sp-btn'), list=sp.querySelector('.sp-list'),
        lbl=sp.querySelector('.sp-lbl'), curic=sp.querySelector('.sp-cur-ic'),
        sel=sp.parentNode.querySelector('.homesport');
  const closeL=()=>{list.hidden=true;btn.setAttribute('aria-expanded','false');};
  btn.addEventListener('click',e=>{e.stopPropagation();const o=list.hidden;list.hidden=!o;btn.setAttribute('aria-expanded',String(o));});
  list.querySelectorAll('.sp-opt').forEach(li=>li.addEventListener('click',()=>{
    const v=li.dataset.val;
    if(sel){sel.value=v;sel.dispatchEvent(new Event('change'));}
    lbl.textContent=li.querySelector('span').textContent;
    curic.innerHTML=li.querySelector('.sp-ic').outerHTML;
    list.querySelectorAll('.sp-opt').forEach(x=>x.setAttribute('aria-selected','false'));
    li.setAttribute('aria-selected','true');
    closeL();
  }));
  document.addEventListener('click',e=>{if(!list.hidden&&!sp.contains(e.target))closeL();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeL();});
});
function goAW(){location.hash='#'+(homeSport&&homeSport.value?homeSport.value:SPORT_IDS[0]);}
// AW-Knopf exakt ueber der Bergspitze; Hover blendet die Piste ein
const awCta=document.querySelector('.aw-cta'), heroEl=document.querySelector('.home-hero'), heroSvg=document.querySelector('.heromt');
function posAW(){
  if(!awCta||!heroEl)return;
  if(window.innerWidth<=760){
    awCta.style.left='';awCta.style.top='';
    const bb=document.querySelector('.bottombar');
    awCta.style.bottom=bb?(bb.offsetHeight+14)+'px':'';
    return;
  }
  awCta.style.bottom='';
  const w=heroEl.clientWidth,h=heroEl.clientHeight;
  if(!w||!h)return; // Startseite ausgeblendet (Sportart offen) -> keine falschen Positionen setzen
  // Desktop: rechts beschnittene viewBox (1600) -> Gipfel ruecken in die Mitte; Mobil volle Breite
  const VBW=window.innerWidth<=760?1896:1600;
  if(heroSvg)heroSvg.setAttribute('viewBox','0 110 '+VBW+' 876');
  const s=Math.max(w/VBW,h/876),ox=(w-VBW*s)/2;
  awCta.style.left=Math.round(1018*s+ox)+'px';
  awCta.style.top=Math.max(10,Math.round((227-110)*s-awCta.offsetHeight-12))+'px';
}
window.addEventListener('resize',posAW);posAW();

// Knopf exakt ueber der Bergspitze positionieren (Bild-x 1018 bei 1896x986, YMin-Slice)
// Hamburger-Menue (Mission, Was ist FTEM?, App, Feedback, Admin/Praesentation)
const menuBtn=document.querySelector('.menu-btn'), menuPanel=document.querySelector('.menu-panel');
if(menuBtn&&menuPanel){
  menuBtn.addEventListener('click',e=>{e.stopPropagation();menuPanel.hidden=!menuPanel.hidden;menuBtn.setAttribute('aria-expanded',String(!menuPanel.hidden));});
  document.addEventListener('click',e=>{if(!menuPanel.hidden&&!e.target.closest('.menu-panel')&&!e.target.closest('.menu-btn')){menuPanel.hidden=true;menuBtn.setAttribute('aria-expanded','false');}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menuPanel.hidden){menuPanel.hidden=true;menuBtn.setAttribute('aria-expanded','false');}});
  // Eintraege, die ein Overlay oeffnen, schliessen das Menue
  menuPanel.querySelectorAll('[data-open],.np-sportmission').forEach(b=>b.addEventListener('click',()=>{menuPanel.hidden=true;menuBtn.setAttribute('aria-expanded','false');}));
  const mpx=menuPanel.querySelector('.mp-x');
  if(mpx)mpx.addEventListener('click',()=>{menuPanel.hidden=true;menuBtn.setAttribute('aria-expanded','false');});
}
const langBtn=document.querySelector('.lang-ic-btn'), langMenu=document.querySelector('.lang-ic-menu');
if(langBtn&&langMenu){
  langBtn.addEventListener('click',e=>{e.stopPropagation();langMenu.hidden=!langMenu.hidden;langBtn.setAttribute('aria-expanded',String(!langMenu.hidden));});
  document.addEventListener('click',e=>{if(!langMenu.hidden&&!e.target.closest('.lang-ic')){langMenu.hidden=true;langBtn.setAttribute('aria-expanded','false');}});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!langMenu.hidden){langMenu.hidden=true;langBtn.setAttribute('aria-expanded','false');}});
}
// FTEM-Knoepfe: Klick -> Stufen-Popup; Hover -> Zone am Berg waechst, andere Knoepfe schrumpfen
const fbtns=document.querySelector('.fbtns');
const zstops=[...document.querySelectorAll('#zonegrad stop')],zstops2=[...document.querySelectorAll('#zonegrad2 stop')];
const ZN=[0,.355,.406,.522,.573,.755,.848,1];
function ztarget(k){
  const t=ZN.slice();
  if(k==='m'){t[1]=.455;t[2]=.506;}
  else if(k==='e'){t[1]=.245;t[2]=.296;t[3]=.632;t[4]=.683;}
  else if(k==='t'){t[3]=.412;t[4]=.463;t[5]=.848;t[6]=.905;}
  else if(k==='f'){t[5]=.652;t[6]=.718;}
  return t;
}
let zcur=ZN.slice(),zraf=0;
function zoneAnim(k){
  if(!zstops.length)return;
  const tgt=ztarget(k),from=zcur.slice(),t0=performance.now();
  cancelAnimationFrame(zraf);
  const step=n=>{
    const p=Math.min(1,(n-t0)/280),e=1-Math.pow(1-p,3);
    zcur=from.map((v,i)=>v+(tgt[i]-v)*e);
    zstops.forEach((s,i)=>s.setAttribute('offset',zcur[i].toFixed(4)));
    zstops2.forEach((s,i)=>s.setAttribute('offset',zcur[i].toFixed(4)));
    if(p<1)zraf=requestAnimationFrame(step);
  };
  zraf=requestAnimationFrame(step);
}
document.querySelectorAll('.fbtnw').forEach(bd=>{
  const k=bd.dataset.ph;
  const open=()=>{
    const sid=homeSport&&homeSport.value?homeSport.value:SPORT_IDS[0];
    let id='tpl-ph-'+k+'-'+sid, tpl=document.getElementById(id);
    if(!tpl){id='tpl-ph-'+k;tpl=document.getElementById(id);}
    if(tpl){openInfo(id, tpl.dataset.t||'');}else{goAW();}};
  bd.addEventListener('click',open);
  const on=()=>{if(fbtns)fbtns.className='fbtns hv-'+k;zoneAnim(k);};
  const off=()=>{if(fbtns)fbtns.className='fbtns';zoneAnim(null);};
  bd.addEventListener('mouseenter',on);
  bd.addEventListener('mouseleave',off);
  bd.addEventListener('focus',on);
  bd.addEventListener('blur',off);
});
document.querySelectorAll('.aw-btn').forEach(el=>{
  el.addEventListener('click',goAW);
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();goAW();}});
});
document.addEventListener('click',e=>{const g=e.target.closest('.aw-go');if(g){closeInfo();goAW();}});
// "Mission Sportart": Mission der vorgewaehlten Sportart direkt im Iframe
document.querySelectorAll('.np-sportmission').forEach(b=>b.addEventListener('click',()=>{
  const id=homeSport&&homeSport.value?homeSport.value:SPORT_IDS[0];
  const u=SPORT_MISSIONS[id];
  if(u)openMission(u,(SPORT_NAMES[id]||id)+' \u2013 Mission Swiss-Ski');
  else openInfo('tpl-missions','Mission Swiss-Ski');
}));

// ---- Versteckter Praesentationsmodus (Symbol unten, Passwort) ----
const PRES_PW='__PRES_PW__';
function presOff(){document.body.classList.remove('pres');if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});}
function presOn(){
  document.body.classList.add('pres');
  if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>{});
  const sec=sections.find(s=>!s.hidden);
  if(sec){const ths=[...sec.querySelectorAll('details.theme')];ths.forEach((t,i)=>t.open=i===0);if(ths[0])ths[0].scrollIntoView({block:'start'});if(sec.__clamp)setTimeout(sec.__clamp,80);}
}
// ---- Praesentations-Deck: Konzept -> Website -> Stufen -> Athlet:innen-Weg ----
const PDLBL=__PDLBL__;
const deck=document.createElement('div');deck.className='presdeck';deck.hidden=true;
deck.innerHTML='<div class="pd-top"><span class="pd-name"></span>'
 +'<select class="pd-sportsel" aria-label="'+_esc(PDLBL.sport)+'">'+SPORT_IDS.map(id=>'<option value="'+id+'">'+_esc(SPORT_NAMES[id]||id)+'</option>').join('')+'</select>'
 +'<span class="pd-count"></span><button class="pd-x" type="button" aria-label="Ende">&times;</button></div>'
 +'<div class="pd-body"></div>'
 +'<button class="pd-prev" type="button" aria-label="'+_esc(I18N.navPrev)+'">&#8249;</button>'
 +'<button class="pd-next" type="button" aria-label="'+_esc(I18N.navNext)+'">&#8250;</button>';
document.body.appendChild(deck);
const pdBody=deck.querySelector('.pd-body'),pdName=deck.querySelector('.pd-name'),
      pdCount=deck.querySelector('.pd-count'),pdSport=deck.querySelector('.pd-sportsel');
let pdIdx=0;
function deckSlides(){
  const sid=pdSport.value;
  const ph=['f','t','e','m'].map(k=>{
    const el=document.getElementById('tpl-ph-'+k+'-'+sid)||document.getElementById('tpl-ph-'+k);
    return {id:el?el.id:null,t:el?(el.dataset.t||''):''};
  }).filter(s=>s.id);
  // Letzte Seite = Athlet:innen-Weg als iframe IM Praesentationsmodus
  return [{id:'tpl-info',t:PDLBL.concept},{id:'tpl-pres-web',t:PDLBL.web}]
    .concat(ph)
    .concat([{ifr:true,t:PDLBL.aw+' – '+(SPORT_NAMES[sid]||sid)}]);
}
function pdRender(){
  const sl=deckSlides(),n=sl.length;
  if(pdIdx<0)pdIdx=0;
  if(pdIdx>=n)pdIdx=n-1; // letzte Seite: bleiben (Esc oder X beendet)
  const s=sl[pdIdx];
  pdBody.classList.toggle('pd-hasifr',!!s.ifr);
  if(s.ifr){
    const self=(location.pathname.split('/').pop()||'index.html');
    pdBody.innerHTML='<iframe class="pd-ifr" src="'+self+'#'+pdSport.value+'" title="'+_esc(s.t)+'"></iframe>';
  }else{
    pdBody.innerHTML=document.getElementById(s.id).innerHTML;
    // Phasen-Folien: Bereiche (WAS/WIE VIEL/Umfeld) starten zugeklappt
    pdBody.querySelectorAll('details:not(.ps-theme)').forEach(d=>d.open=true);
  }
  pdName.textContent=s.t;
  pdCount.textContent=(pdIdx+1)+' / '+n;
  pdBody.scrollTop=0;
}
function openDeck(){
  pdSport.value=(homeSport&&homeSport.value)?homeSport.value:SPORT_IDS[0];
  pdIdx=0;deck.hidden=false;document.body.classList.add('deckon');
  if(document.documentElement.requestFullscreen)document.documentElement.requestFullscreen().catch(()=>{});
  pdRender();
}
function closeDeck(exitFs){
  deck.hidden=true;document.body.classList.remove('deckon');
  if(exitFs&&document.fullscreenElement)document.exitFullscreen().catch(()=>{});
}
pdBody.addEventListener('click',e=>{
  const c=e.target.closest('.pdw');if(!c)return;
  const sid=pdSport.value,name=SPORT_NAMES[sid]||sid,t=c.dataset.t||'';
  const self=(location.pathname.split('/').pop()||'index.html');
  const act=c.dataset.act;
  if(act==='aw'){openMission(self+'#'+sid, t+' \u2013 '+name);}
  else if(act==='stages'){openMission(self, t);}
  else if(act==='mission'){const u=SPORT_MISSIONS[sid];u?openMission(u,name+' \u2013 Mission Swiss-Ski'):openInfo('tpl-missions','Mission Swiss-Ski');}
  else if(act==='news'){openInfo('tpl-news',t);}
  else if(act==='coach'){const sec=sections.find(s=>s.dataset.sport===sid);if(sec)openChat(sec);}
  else if(act==='app'){openInfo('tpl-app',t);}
});
deck.querySelector('.pd-x').addEventListener('click',()=>closeDeck(true));
deck.querySelector('.pd-prev').addEventListener('click',()=>{pdIdx--;pdRender();});
deck.querySelector('.pd-next').addEventListener('click',()=>{pdIdx++;pdRender();});
pdSport.addEventListener('change',pdRender);
document.addEventListener('keydown',e=>{
  if(deck.hidden)return;
  if(e._ovl)return; // Escape hat soeben ein Overlay geschlossen -> Deck bleibt offen
  if((typeof chatPanel!=='undefined'&&!chatPanel.hidden)||(im&&!im.hidden)||(mm&&!mm.hidden))return;
  if(e.target&&(e.target.tagName==='SELECT'||e.target.tagName==='INPUT'))return;
  if(e.key==='Escape'){closeDeck(true);return;}
  if(['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();pdIdx++;pdRender();}
  else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();pdIdx--;pdRender();}
});
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&!deck.hidden)closeDeck(false);});

document.querySelectorAll('.preslink').forEach(pl=>{
  const btn=pl.querySelector('.presopen'), ask=pl.querySelector('.presask'), pw=pl.querySelector('.prespw');
  btn.addEventListener('click',()=>{ask.hidden=!ask.hidden;if(!ask.hidden){pw.value='';pw.focus();}});
  function tryGo(){
    if(pw.value===PRES_PW){
      ask.hidden=true;
      if(typeof menuPanel!=='undefined'&&menuPanel){menuPanel.hidden=true;}
      openDeck();
    }
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
  if(home.hidden!==!!id)home.hidden = !!id;
  // Nur Sektionen anfassen, deren Zustand wirklich wechselt (grosses DOM -> weniger Ruckeln)
  sections.forEach(s=>{const w=s.dataset.sport!==id;if(s.hidden!==w)s.hidden=w;});
  window.scrollTo(0,0);
  // Zurueck auf die Startseite: AW-Knopf neu ueber der Bergspitze positionieren
  if(!id)requestAnimationFrame(posAW);
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
.cedit.curchg{box-shadow:0 0 0 3px rgba(213,43,30,.35);border-color:#d52b1e}
.chgnav{display:inline-flex;align-items:center;gap:5px}
.chgnav button{font:inherit;font-size:12px;font-weight:700;border:1px solid #d4dae1;border-radius:7px;background:#fff;padding:4px 9px;cursor:pointer}
.chgnav button:hover{background:#f2f4f6}
.chgnav #chgpos{font-size:12px;font-weight:800;color:#d52b1e;min-width:44px;text-align:center}
.chgnav #chgundo{color:#d52b1e;border-color:rgba(213,43,30,.4)}
/* Startseiten-Inhalte im Admin (Landingpage-Texte) */
.adm-home{padding:12px 14px 16px;display:flex;flex-direction:column;gap:12px}
.adm-field label{display:block;font-size:10.5px;font-weight:800;color:#546a8c;letter-spacing:.06em;text-transform:uppercase;margin:0 0 4px}
.adm-field label .adm-hint{display:block;font-style:normal;text-transform:none;letter-spacing:0;font-weight:600;color:#98a1ad;font-size:10.5px;margin-top:1px}
.adm-field .cedit{font-size:12.5px}
.adm-sec{border:1px solid #e4e8ec;border-radius:10px;padding:10px 12px;display:flex;flex-direction:column;gap:10px;background:#fafbfc}
.adm-sect{font-size:12.5px;font-weight:800;color:#1d2630}
.adm-tag{font-size:10.5px;font-weight:700;color:#697080;background:#eef1f4;border-radius:20px;padding:2px 9px;margin-left:8px;letter-spacing:.02em;vertical-align:2px}
.adm-note{margin:0;font-size:12px;color:#8a6a00;background:#fdf7e4;border:1px solid #f0e2ad;border-radius:8px;padding:7px 10px}
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
    <label>Sprache: <select id="langsel"><option value="de">Deutsch</option><option value="fr">Français</option><option value="it">Italiano</option><option value="en">English</option></select></label>
    <span class="sp"></span>
    <span id="astatus" class="astatus"></span>
    <span id="chgnav" class="chgnav" hidden>
      <button id="chgprev" type="button" title="Vorherige Änderung">&#9650;</button>
      <span id="chgpos"></span>
      <button id="chgnext" type="button" title="Nächste Änderung">&#9660;</button>
      <button id="chgundo" type="button" title="Diese Änderung rückgängig machen">&#8634; Rückgängig</button>
    </span>
    <button id="asave" class="asave" disabled>Speichern</button>
    <button id="glossbtn" class="agloss" type="button">Glossar</button>
    <a href="index.html" class="asite">&#8617; Zur Seite</a>
  </header>
  <div id="note" class="note"></div>
  <div id="glosspanel" hidden>
    <div class="glosbar"><input id="glosq" type="search" placeholder="Begriff suchen (DE, FR, IT oder EN) …"><span id="gloscount" class="astatus"></span></div>
    <p class="glosnote">Feste Übersetzungen DE&nbsp;&rarr;&nbsp;FR/IT/EN. Diese Begriffe werden bei der Übersetzung der Inhalte einheitlich verwendet. (Neue Begriffe unten werden vorerst nur mit DE/FR gespeichert.)</p>
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
const ORIGS=__ADMIN_ORIG__, GLOSS=__GLOSSARY__, PW="__ADMIN_PW__", SUPA_URL="__SUPA_URL__", SUPA_KEY="__SUPA_KEY__";
const ALANGS=['de','fr','it','en'], ALABEL={de:'DE',fr:'FR',it:'IT',en:'EN'};
let LNG='de';
const gate=document.getElementById('gate'),app=document.getElementById('app');
function gesc(s){return String(s).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
function renderGloss(q){
  q=(q||'').trim().toLowerCase();
  const rows=GLOSS.filter(function(g){
    if(!q)return true;
    return ['de','fr','it','en'].some(function(l){return (g[l]||'').toLowerCase().indexOf(q)>=0;});
  });
  document.getElementById('gloscount').textContent=rows.length+' Begriffe';
  let h='<table class="glostab"><thead><tr><th>Deutsch</th><th>Français</th><th>Italiano</th><th>English</th></tr></thead><tbody>';
  rows.forEach(function(g){h+='<tr><td>'+gesc(g.de)+'</td><td>'+gesc(g.fr)+'</td><td>'+gesc(g.it||'')+'</td><td>'+gesc(g.en||'')+'</td></tr>';});
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
const statusEl=document.getElementById('astatus'),saveBtn=document.getElementById('asave'),sel=document.getElementById('sportsel'),langSel=document.getElementById('langsel');
// Basiswerte pro Sprache (deutscher Quelltext bzw. dessen Uebersetzung; wird
// durch geladene Cloud-Overrides ersetzt) + ungespeicherte Eingaben pro Sprache
const base={}; ALANGS.forEach(function(l){base[l]=Object.assign({},ORIGS[l]);});
const edits={de:{},fr:{},it:{},en:{}};
function curVal(cid){return edits[LNG][cid]!==undefined?edits[LNG][cid]:(base[LNG][cid]||'');}
function refreshValues(){
  app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){
    ta.value=curVal(ta.dataset.cid);
  });
  const vis=app.querySelector('section.sport:not([hidden])');
  if(vis)vis.querySelectorAll('.cedit').forEach(autosize);
}
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
  // Alle ungespeicherten Aenderungen ueber ALLE Sprachen (fuer Speichern/Zaehler).
  // Deutsche Overrides ohne Suffix, andere Sprachen mit "|fr"/"|it"/"|en".
  const out=[];
  ALANGS.forEach(function(l){
    Object.keys(edits[l]).forEach(function(cid){
      if((base[l][cid]||'')!==edits[l][cid])out.push({cid:(l==='de'?cid:cid+'|'+l),txt:edits[l][cid]});
    });
  });
  return out;
}
function changedTas(){
  // Nur Felder der AKTUELL angezeigten Sprache (fuer die Sprung-Navigation)
  return Array.prototype.filter.call(app.querySelectorAll('.cedit[data-cid]'),function(ta){
    const cid=ta.dataset.cid;
    return edits[LNG][cid]!==undefined&&(base[LNG][cid]||'')!==edits[LNG][cid];
  });
}
let chgIdx=-1;
const chgNav=document.getElementById('chgnav'),chgPos=document.getElementById('chgpos');
function updateCount(){
  // Markierung mit dem echten Zustand synchronisieren (aktuelle Sprache)
  app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){
    const cid=ta.dataset.cid;
    ta.classList.toggle('changed',edits[LNG][cid]!==undefined&&(base[LNG][cid]||'')!==edits[LNG][cid]);
  });
  const n=changed().length;saveBtn.disabled=n===0;
  // Aufschluesselung pro Sprache, falls Aenderungen in mehreren Sprachen offen sind
  const parts=[];
  ALANGS.forEach(function(l){
    let c=0;Object.keys(edits[l]).forEach(function(cid){if((base[l][cid]||'')!==edits[l][cid])c++;});
    if(c)parts.push(ALABEL[l]+' '+c);
  });
  statusEl.textContent=n?(n+' ungespeichert'+(parts.length>1?' ('+parts.join(' · ')+')':'')):'Alles gespeichert';
  chgNav.hidden=changedTas().length===0;
  const tas=changedTas();
  if(chgIdx>=tas.length)chgIdx=tas.length-1;
  chgPos.textContent=tas.length?((chgIdx>=0?(chgIdx+1):'–')+' / '+tas.length):'';
}
function gotoChg(step){
  const tas=changedTas();if(!tas.length)return;
  chgIdx=(chgIdx+step+tas.length*99)%tas.length;
  const ta=tas[chgIdx];
  // Sportart der Aenderung einblenden (cid beginnt mit "<sportid>|...")
  const sec=ta.closest('section.sport');
  if(sec&&sec.hidden){sel.value=sec.dataset.sport;showSport(sec.dataset.sport);}
  // Thema der Aenderung aufklappen (Themen starten eingeklappt)
  const dth=ta.closest('details.theme');
  if(dth&&!dth.open){dth.open=true;dth.querySelectorAll('.cedit').forEach(autosize);}
  app.querySelectorAll('.cedit.curchg').forEach(function(t){t.classList.remove('curchg');});
  ta.classList.add('curchg');
  ta.scrollIntoView({block:'center',behavior:'smooth'});
  chgPos.textContent=(chgIdx+1)+' / '+tas.length;
}
function undoCur(){
  const tas=changedTas();if(!tas.length)return;
  if(chgIdx<0||chgIdx>=tas.length)chgIdx=0;
  const ta=tas[chgIdx];
  delete edits[LNG][ta.dataset.cid];
  ta.value=base[LNG][ta.dataset.cid]||'';
  ta.classList.remove('changed','curchg');
  autosize(ta);
  updateCount();
  // zur naechsten verbleibenden Aenderung springen
  if(changedTas().length){chgIdx=chgIdx%changedTas().length;gotoChg(0);}else{chgIdx=-1;}
}
function init(){
  sel.addEventListener('change',function(){showSport(sel.value);});
  // Beim Aufklappen eines Themas die Textfelder korrekt dimensionieren
  app.addEventListener('toggle',function(e){
    const d=e.target;
    if(d&&d.matches&&d.matches('details.theme')&&d.open)d.querySelectorAll('.cedit').forEach(autosize);
  },true);
  app.querySelectorAll('.cedit[data-cid]').forEach(function(ta){
    ta.addEventListener('input',function(){
      autosize(ta);
      const cid=ta.dataset.cid;
      if(ta.value===(base[LNG][cid]||''))delete edits[LNG][cid];else edits[LNG][cid]=ta.value;
      updateCount();
    });
  });
  langSel.addEventListener('change',function(){
    LNG=langSel.value;chgIdx=-1;
    refreshValues();updateCount();
  });
  saveBtn.addEventListener('click',save);
  document.getElementById('chgprev').addEventListener('click',function(){gotoChg(-1);});
  document.getElementById('chgnext').addEventListener('click',function(){gotoChg(1);});
  document.getElementById('chgundo').addEventListener('click',undoCur);
  document.getElementById('glossbtn').addEventListener('click',toggleGloss);
  if(SUPA_URL&&SUPA_KEY){
    fetch(SUPA_URL+'/rest/v1/ftem_overrides?select=cid,txt',{headers:{apikey:SUPA_KEY,Authorization:'Bearer '+SUPA_KEY}})
      .then(function(r){return r.ok?r.json():[];}).then(function(rows){
        (rows||[]).forEach(function(x){
          const m2=x.cid.match(/^(.*)\|(fr|it|en)$/);
          if(m2){base[m2[2]][m2[1]]=x.txt;}else{base.de[x.cid]=x.txt;}
        });
        refreshValues();
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
     ch.forEach(function(x){
       const m2=x.cid.match(/^(.*)\|(fr|it|en)$/);
       if(m2){base[m2[2]][m2[1]]=x.txt;}else{base.de[x.cid]=x.txt;}
     });
     ALANGS.forEach(function(l){edits[l]={};});
     app.querySelectorAll('.cedit.changed').forEach(function(t){t.classList.remove('changed');});
     statusEl.textContent='Gespeichert ✓ – Änderungen sind jetzt live.';saveBtn.disabled=true;
   }).catch(function(err){statusEl.textContent='Fehler beim Speichern: '+err.message;saveBtn.disabled=false;});
}
</script></body></html>'''

# --- Startseiten-Inhalte im Admin -------------------------------------------
# Gleiche Mechanik wie der Athlet:innen-Weg: nur TEXTE sind editierbar (textarea
# mit data-cid), die Struktur (Abschnitte, Links, Reihenfolge) bleibt fix.
PH_STAGES_ADM = {"f": ["F1","F2","F3"], "t": ["T1","T2","T3","T4"], "e": ["E1","E2"], "m": ["M"]}

def _adm_field(label, cid, val, hint=""):
    return ('<div class="adm-field"><label>'+esc(label)
            + ('<i class="adm-hint">'+esc(hint)+'</i>' if hint else '')
            + '</label><textarea class="cedit" data-cid="'+esc(cid)+'">'+esc(val or "")+'</textarea></div>')

def home_edit_html(sport, d):
    """Editierbare Startseiten-Popups (Stufen-Überblick F/T/E/M) einer Sportart."""
    hm = (d or {}).get("home")
    if not hm:
        return ""
    info = FTEM_INFO["de"]
    out = ('<h2 class="grp" style="--gc:#1f8fa6">Startseite &ndash; Stufen-Überblick '
           '<span class="adm-tag">Popups der FTEM-Knöpfe</span></h2>')
    # Abschnitts-Titel: gelten fuer alle Stufen, darum nur EINMAL editierbar
    # (doppelte cids wuerden die Aenderungs-Anzeige durcheinanderbringen)
    tblocks = ""
    for si, sec in enumerate(hm.get("sections", [])):
        tblocks += _adm_field("Abschnitt "+str(si+1), "home|"+sport["id"]+"|"+str(si)+"|title", sec["title"])
    if tblocks:
        out += ('<details class="theme"><summary>'
                '<span class="ticon" style="color:#4a5563;background:rgba(74,85,99,.13)">✎</span>'
                '<span class="tt">Abschnitts-Titel <span class="adm-tag">gelten für alle Stufen F&ndash;M</span></span>'
                '<span class="tchev"></span></summary>'
                '<div class="adm-home">'+tblocks+'</div></details>')
    for k, (letter, pname, prng, pdesc) in zip(["f","t","e","m"], info["phases"]):
        intro = (hm.get("intro") or {}).get(k) or pdesc
        blocks = _adm_field("Titel der Stufe", "home|"+sport["id"]+"|"+k+"|ptitle", pname,
                            "Der Stufen-Bereich ("+prng+") bleibt automatisch stehen")
        blocks += _adm_field("Einleitung", "home|"+sport["id"]+"|"+k+"|intro", intro)
        for si, sec in enumerate(hm.get("sections", [])):
            cols = ""
            for st in PH_STAGES_ADM[k]:
                cell = (sec.get("cells") or {}).get(st)
                if not cell or not (cell.get("v") or cell.get("l")):
                    continue
                cols += _adm_field(st, "home|"+sport["id"]+"|"+str(si)+"|"+st, cell.get("v") or "")
            if cols:
                blocks += '<div class="adm-sec"><div class="adm-sect">'+esc(sec["title"])+'</div>'+cols+'</div>'
        out += ('<details class="theme"><summary>'
                '<span class="ticon" style="color:#4a5563;background:rgba(74,85,99,.13)">'+letter+'</span>'
                '<span class="tt">'+esc(pname)+' &middot; '+esc(prng)+'</span><span class="tchev"></span></summary>'
                '<div class="adm-home">'+blocks+'</div></details>')
    return out

def admin_html(datamap):
    secs = ""; opts = ""; orig = {}
    for s in SPORTS:
        d = datamap[s["id"]]
        if not d: continue
        secs += sport_section(s, d, "de", edit=True)
        opts += '<option value="'+esc(s["id"])+'">'+esc(tr(s["name"], "de"))+'</option>'
        for ti, t in enumerate(d["themes"]):
            orig[s["id"]+"|"+str(ti)+"|title"] = t["title"] or ""
            for ri, r in enumerate(t["rows"]):
                # WICHTIG: gleiche Nummerierung wie theme_html (zusammengefuehrte
                # Segmente) – sonst zeigen Zellen nach Verschmelzungen faelschlich
                # "ungespeichert" an (Index-Verschiebung).
                for si, seg in enumerate(merge_same_segs(r["segs"])):
                    orig[s["id"]+"|"+str(ti)+"|"+str(ri)+"|"+str(si)] = seg.get("v") or ""
        # Startseiten-Popup-Inhalte dieser Sportart (Stufen-Überblick)
        hm = d.get("home")
        if hm:
            for k, (letter, pname, prng, pdesc) in zip(["f","t","e","m"], FTEM_INFO["de"]["phases"]):
                orig["home|"+s["id"]+"|"+k+"|ptitle"] = pname
                orig["home|"+s["id"]+"|"+k+"|intro"] = (hm.get("intro") or {}).get(k) or pdesc
            for si, sec in enumerate(hm.get("sections", [])):
                orig["home|"+s["id"]+"|"+str(si)+"|title"] = sec["title"] or ""
                for st, cell in (sec.get("cells") or {}).items():
                    if cell and (cell.get("v") or cell.get("l")):
                        orig["home|"+s["id"]+"|"+str(si)+"|"+st] = cell.get("v") or ""
    # Basiswerte pro Sprache: DE = Quelltext, FR/IT/EN = dessen Uebersetzung
    # (gleiche Logik wie auf den Live-Seiten: tr() ganzer Zellen)
    origs = {"de": orig}
    for _L in ("fr", "it", "en"):
        origs[_L] = {c: tr(v, _L) for c, v in orig.items()}
    orig_js = json.dumps(origs, ensure_ascii=False).replace("</", "<\\/")
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
    open_ext = {"de": "Im neuen Tab öffnen", "fr": "Ouvrir dans un nouvel onglet", "it": "Aprire in una nuova scheda", "en": "Open in new tab"}[lang]
    mmodal = ('<div class="mmodal" hidden><div class="mm-box">'
              '<div class="mm-bar"><span class="mm-t"></span>'
              '<a class="mm-ext" href="#" target="_blank" rel="noopener">'+esc(open_ext)+' ↗</a>'
              '<button class="mm-x" type="button" aria-label="'+esc(CLOSE_W[lang])+'">✕</button></div>'
              '<iframe class="mm-frame" src="about:blank" title="Mission Swiss-Ski"></iframe>'
              '</div></div>')
    imodal = ('<div class="imodal" hidden><div class="im-box">'
              '<div class="im-bar"><span class="im-t"></span>'
              '<button class="im-x" type="button" aria-label="'+esc(CLOSE_W[lang])+'">✕</button></div>'
              '<div class="im-body"></div></div></div>')
    assist_lbl = {"de": "FTEM-Coach", "fr": "Coach FTEM", "it": "Coach FTEM", "en": "FTEM Coach"}[lang]
    steady_btn = '<button class="steady" type="button" hidden>💬 '+esc(assist_lbl)+'</button>'
    body = home_html(datamap, lang) + "".join(sport_section(s, datamap[s["id"]], lang) for s in SPORTS) + mmodal + imodal + steady_btn
    i18n = {"more": tr("mehr ▾", lang), "less": tr("weniger ▴", lang),
            "themes": tr("Themen · F1–M", lang), "hits": tr("Themen mit Treffern", lang),
            "hitsWord": {"de": "Treffer", "fr": "résultats", "it": "risultati", "en": "hits"}[lang],
            "noHits": {"de": "keine Treffer", "fr": "aucun résultat", "it": "nessun risultato", "en": "no hits"}[lang],
            "printPick": {"de": "Stufe für das Dossier wählen", "fr": "Choisir le niveau pour le dossier", "it": "Scegli il livello per il dossier", "en": "Choose the stage for the dossier"}[lang],
            "printAll": {"de": "Ganze Sportart (Querformat)", "fr": "Tout le sport (paysage)", "it": "Tutto lo sport (orizzontale)", "en": "Entire sport (landscape)"}[lang],
            "printClose": {"de": "Schliessen", "fr": "Fermer", "it": "Chiudi", "en": "Close"}[lang],
            "dossier": {"de": "Stufendossier", "fr": "Dossier de niveau", "it": "Dossier di livello", "en": "Stage dossier"}[lang],
            "popupBlocked": {"de": "Bitte Pop-ups für diese Seite erlauben, um das Dossier zu drucken.", "fr": "Veuillez autoriser les pop-ups pour imprimer le dossier.", "it": "Consenti i pop-up per stampare il dossier.", "en": "Please allow pop-ups for this page to print the dossier."}[lang],
            "send": {"de": "Senden", "fr": "Envoyer", "it": "Invia", "en": "Send"}[lang],
            "navPrev": {"de": "zurück", "fr": "précédent", "it": "indietro", "en": "back"}[lang],
            "navNext": {"de": "weiter", "fr": "suivant", "it": "avanti", "en": "next"}[lang],
            "chatTitle": {"de": "FTEM-Coach", "fr": "Coach FTEM", "it": "Coach FTEM", "en": "FTEM Coach"}[lang],
            "chatPh": {"de": "Frage zum Athlet:innen-Weg…", "fr": "Question sur le parcours…", "it": "Domanda sul percorso…", "en": "Question about the pathway…"}[lang],
            "chatWelcome": {"de": "Hallo! Frag mich alles zum Athlet:innen-Weg dieser Sportart – zum Beispiel:", "fr": "Bonjour ! Pose-moi toutes tes questions sur le parcours de ce sport – par exemple :", "it": "Ciao! Chiedimi tutto sul percorso di questo sport – per esempio:", "en": "Hi! Ask me anything about this sport's athlete pathway – for example:"}[lang],
            "chatExamples": {"de": ["Welches Material brauche ich in F3?", "Kraft-Ziele in Stufe T2?", "Welche Kader gibt es?", "Trainingsphasen im Überblick"], "fr": ["Quel matériel en F3 ?", "Objectifs de force en T2 ?", "Quels cadres existe-t-il ?", "Aperçu des phases d'entraînement"], "it": ["Quale materiale in F3?", "Obiettivi di forza in T2?", "Quali quadri esistono?", "Panoramica delle fasi"], "en": ["What gear do I need in F3?", "Strength goals in T2?", "Which squads exist?", "Overview of training phases"]}[lang],
            "chatErr": {"de": "Es gab ein Problem beim Beantworten. Bitte später erneut versuchen.", "fr": "Un problème est survenu. Veuillez réessayer plus tard.", "it": "Si è verificato un problema. Riprova più tardi.", "en": "Something went wrong. Please try again later."}[lang],
            "chatNote": {"de": "Antworten basieren auf den FTEM-Inhalten dieser Sportart und den verlinkten Dokumenten. Keine Rechtsberatung.", "fr": "Les réponses se basent sur les contenus FTEM de ce sport et les documents liés.", "it": "Le risposte si basano sui contenuti FTEM di questo sport e sui documenti collegati.", "en": "Answers are based on this sport's FTEM content and the linked documents."}[lang]}
    js = (JS.replace("__SPORT_IDS__", json.dumps([s["id"] for s in SPORTS]))
            .replace("__SPORT_MISSIONS__", json.dumps({s["id"]: s.get("mission","") for s in SPORTS}))
            .replace("__SPORT_NAMES__", json.dumps({s["id"]: tr(s["name"], lang) for s in SPORTS}, ensure_ascii=False))
            .replace("__PDLBL__", json.dumps({
                "de": {"concept": "Das Konzept FTEM", "web": "Die Website", "aw": "Athlet:innen-Weg",
                       "awhint": "Weiter (→) öffnet die Themen des Athlet:innen-Wegs – Navigation mit den Pfeiltasten, Esc beendet.",
                       "sport": "Sportart"},
                "fr": {"concept": "Le concept FTEM", "web": "Le site web", "aw": "Parcours de l'athlète",
                       "awhint": "Continuer (→) ouvre les thèmes du parcours – navigation avec les flèches, Esc pour terminer.",
                       "sport": "Sport"},
                "it": {"concept": "Il concetto FTEM", "web": "Il sito web", "aw": "Percorso dell'atleta",
                       "awhint": "Avanti (→) apre i temi del percorso – navigazione con le frecce, Esc per terminare.",
                       "sport": "Sport"},
                "en": {"concept": "The FTEM framework", "web": "The website", "aw": "Athlete pathway",
                       "awhint": "Next (→) opens the pathway topics – navigate with the arrow keys, Esc to end.",
                       "sport": "Sport"},
            }[lang], ensure_ascii=False))
            .replace("__I18N__", json.dumps(i18n, ensure_ascii=False))
            .replace("__PAGELANG__", lang)
            .replace("__SUPA_URL__", SUPABASE_URL).replace("__SUPA_KEY__", SUPABASE_ANON_KEY)
            .replace("__PRES_PW__", PRES_PW))
    og_title = "FTEM – "+tr("Athlet:innen-Weg", lang)+" · Swiss-Ski"
    og_desc = {"de":"Der Athlet:innen-Weg von Swiss-Ski: alle Schneesportarten über die zehn FTEM-Entwicklungsstufen F1–M.",
               "fr":"Le parcours des athlètes de Swiss-Ski : tous les sports de neige à travers les dix niveaux de développement FTEM (F1–M).",
               "it":"Il percorso degli atleti di Swiss-Ski: tutti gli sport sulla neve lungo i dieci livelli di sviluppo FTEM (F1–M).",
               "en":"The Swiss-Ski athlete pathway: all snow sports across the ten FTEM development stages (F1–M)."}[lang]
    og_img = (SITE_URL.rstrip("/")+"/assets/og-image.jpg") if SITE_URL else "assets/og-image.jpg"
    og_locales = {"de":"de_CH","fr":"fr_CH","it":"it_CH","en":"en_GB"}
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
    for f in ["index.html","fr.html","it.html","en.html"]:
        p = os.path.join(BASE, f)
        if os.path.exists(p): h.update(open(p,"rb").read())
    # Auch Assets einrechnen: sonst bleibt der Cache-Name bei reinen Bild-Updates
    # gleich und der Service Worker liefert alte Bilder aus (z. B. Sport-Icons)
    for p in sorted(_glob.glob(os.path.join(BASE, "assets", "sporticons", "*.png"))) + \
             [os.path.join(BASE, "assets", x) for x in
              ("hero.jpg","swiss-ski-logo.svg","favicon.svg","og-image.jpg")]:
        if os.path.exists(p): h.update(open(p,"rb").read())
    ver = h.hexdigest()[:10]
    core = ["./","./index.html","./fr.html","./it.html","./en.html","./admin.html",
            "./manifest.webmanifest","./assets/favicon.svg","./assets/icon-192.png",
            "./assets/icon-512.png","./assets/icon-180.png","./assets/hero.jpg",
            "./assets/og-image.jpg","./assets/swiss-ski-logo.svg"]
    core += ["./"+asset_v(p.replace("\\","/")) for p in _glob.glob("assets/sporticons/*.png")]
    sw = (
        'const CACHE="ftem-'+ver+'";\n'
        'const CORE='+json.dumps(core)+';\n'
        'self.addEventListener("install",e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()));});\n'
        'self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});\n'
        'self.addEventListener("fetch",e=>{const req=e.request;if(req.method!=="GET")return;const url=new URL(req.url);if(url.origin!==location.origin)return;\n'
        '  const isPage=req.mode==="navigate"||url.pathname.endsWith(".html")||url.pathname.endsWith("/");\n'
        '  if(isPage){\n'
        '    // Seiten: immer zuerst frisch vom Netz (kein "alte Version"-Problem mehr), Cache nur offline\n'
        '    e.respondWith(caches.open(CACHE).then(async c=>{try{const res=await fetch(req);if(res&&res.status===200)c.put(req,res.clone());return res;}catch(_){const cached=await c.match(req);return cached||Response.error();}}));\n'
        '    return;\n'
        '  }\n'
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
