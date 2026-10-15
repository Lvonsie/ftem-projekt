// Link-Check fuer my.ftem.swiss-ski.ch: prueft alle externen Links der Seite.
// Laeuft woechentlich per GitHub Action (.github/workflows/link-check.yml).
//
// Quellen:  - die 4 gebauten Sprachseiten im Repo (index/fr/it/en.html)
//           - die Admin-Texte aus der Datenbank (Supabase, nur Lesen;
//             Rueckfall: backup/ftem_overrides.json aus dem taeglichen Backup)
// Pruefung: GET mit Weiterleitungen, 20 s Timeout, Browser-Kennung.
//           Defekte Links werden nach 60 s ein zweites Mal geprueft.
//           Links ohne Antwort (Drosselung, z.B. Flink/J+S) werden nach 2 min
//           einzeln nachgeprueft.
// Defekt:   404/410, Serverfehler (5xx), Domain existiert nicht / Verbindung
//           abgelehnt / Zertifikat ungueltig.
// Nicht pruefbar (kein Alarm, nur im Protokoll): 401/403/429 sowie Zeitueber-
//           schreitungen - viele Seiten sperren oder drosseln automatische
//           Abrufe, obwohl der Link fuer Menschen geht.
// Ergebnis: Bei defekten Links Warn-Mail (Resend) mit Fundstelle + roter Lauf.

import fs from 'node:fs';
import { warnmail } from './_mail.mjs';

const SUPA = process.env.FTEM_SUPA || 'https://xphbwnzyebbejsdeqled.supabase.co';
const ANON = 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_'; // oeffentlicher Lese-Schluessel
const ROOT = process.env.FTEM_ROOT || '.';
const NUR = process.env.LINKCHECK_FILTER || '';            // nur fuer lokale Tests
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36';
const IGNOR = [/my\.ftem\.swiss-ski\.ch/, /supabase\.co/, /fonts\.(googleapis|gstatic)\.com/,
  /w3\.org/, /schema\.org/, /cdnjs|jsdelivr|unpkg/, /…/, /\$\{/, /[{}]/];
const SPRACHEN = { 'index.html': 'DE', 'fr.html': 'FR', 'it.html': 'IT', 'en.html': 'EN' };

const lies = f => { try { return fs.readFileSync(`${ROOT}/${f}`, 'utf8'); } catch { return null; } };
const json = f => { const t = lies(f); return t ? JSON.parse(t) : null; };
const sauber = u => u.replace(/&amp;/g, '&').replace(/[.,;:)\]'"\\]+$/, '');
const URL_RE = /https?:\/\/[^\s"'<>\\`)\]]+/g;

// ---------- 1. Fundstellen-Verzeichnis aus den Datenquellen (fuer die Mail) ----------
const wo = new Map();                                       // url -> Set(Fundstelle)
const merke = (u, s) => { u = sauber(u); if (!wo.has(u)) wo.set(u, new Set()); wo.get(u).add(s); };
const sports = Object.fromEntries((json('ftem_sports.json')?.sports || json('ftem_sports.json') || [])
  .map(s => [s.id, s.name || s.title || s.id]).filter(([k]) => k));
function stufen(stages, seg) {
  if (!stages || seg.from == null) return '';
  const n = i => (stages[i] && (stages[i].short || stages[i].code || stages[i].name || stages[i])) || i;
  return seg.from === seg.to ? ` · ${n(seg.from)}` : ` · ${n(seg.from)}–${n(seg.to)}`;
}
function sammleSegmente(rows, prefix, stages) {
  for (const row of rows || []) for (const seg of row.segs || []) {
    const ort = `${prefix}${row.label ? ' · ' + row.label : ''}${stufen(stages, seg)}`;
    for (const l of seg.l || []) if (l.href) merke(l.href, `${ort} · Knopf «${l.text || ''}»`);
    for (const u of String(seg.v || '').match(URL_RE) || []) merke(u, `${ort} · im Text`);
  }
}
for (const f of fs.readdirSync(ROOT).filter(f => /^ftem_data_.+\.json$/.test(f))) {
  const id = f.slice(10, -5), d = json(f);
  for (const t of d?.themes || []) if (t.rows) sammleSegmente(t.rows, `${sports[id] || id} · ${t.title || ''}`, d.stages);
}
for (const b of json('ftem_shared.json')?.blocks || [])
  sammleSegmente(b.rows, `Sportartübergreifend · ${b.title} (${b.label || b.id})`, null);
const lt = json('link_translations.json') || {};
for (const [de, v] of Object.entries(lt)) {
  if (de.startsWith('_') || typeof v !== 'object') continue;
  for (const sp of ['fr', 'it', 'en']) if (typeof v[sp] === 'string' && /^https?:/.test(v[sp]))
    for (const s of wo.get(sauber(de)) || [`Link «${v.text || de}»`]) merke(v[sp], `${s} (${sp.toUpperCase()}-Version)`);
}

// ---------- 2. Alle Links einsammeln ----------
const links = new Map();                                    // url -> Set(Sprache/Quelle)
const nimm = (u, q) => {
  u = sauber(u);
  if (IGNOR.some(r => r.test(u)) || (NUR && !u.includes(NUR))) return;
  if (!links.has(u)) links.set(u, new Set());
  links.get(u).add(q);
};
for (const [f, sp] of Object.entries(SPRACHEN)) {
  const t = lies(f);
  if (!t) throw new Error(`${f} fehlt im Repo`);
  for (const u of t.match(URL_RE) || []) nimm(u, sp);
}
let ov = null;
try {
  const r = await fetch(`${SUPA}/rest/v1/ftem_overrides?select=cid,txt`,
    { headers: { apikey: ANON, authorization: `Bearer ${ANON}` }, signal: AbortSignal.timeout(30000) });
  if (r.ok) ov = await r.json();
} catch { /* Rueckfall unten */ }
if (!Array.isArray(ov)) { ov = json('backup/ftem_overrides.json') || []; console.log('Admin-Texte aus Backup gelesen.'); }
for (const o of ov) {
  if (!o.cid || o.cid.startsWith('rev|')) continue;         // rev| = nur Pruef-Merker, nicht sichtbar
  for (const u of String(o.txt || '').match(URL_RE) || []) {
    nimm(u, 'Admin-Text');
    const sp = (o.cid.match(/\|(fr|it|en)$/) || [])[1];
    merke(u, `Admin-Text ${o.cid.replace(/^shared\|/, 'Sportartübergreifend|')}${sp ? '' : ' (DE)'}`);
  }
}
console.log(`${links.size} externe Links gefunden.`);

// ---------- 3. Pruefen ----------
async function pruefe(u) {
  try {
    const r = await fetch(u, { redirect: 'follow', signal: AbortSignal.timeout(20000),
      headers: { 'user-agent': UA, accept: 'text/html,application/pdf,*/*;q=0.8', 'accept-language': 'de-CH,de;q=0.9' } });
    r.body?.cancel?.().catch(() => {});
    return { code: r.status };
  } catch (e) {
    return { code: 0, fehler: (e.cause?.code || e.name || 'Fehler').toString() };
  }
}
// Zeitueberschreitung/abgebrochene Verbindung = meist Drosselung -> nicht pruefbar
const ZEIT = /TIMEOUT|Timeout|Abort|ECONNRESET|UND_ERR_SOCKET|EPIPE/;
const art = x => x.code === 0 ? (ZEIT.test(x.fehler) ? 'gesperrt' : 'defekt')
  : [401, 403, 429].includes(x.code) ? 'gesperrt' : x.code >= 400 ? 'defekt' : 'ok';
const warte = ms => new Promise(r => setTimeout(r, ms));
// Bis zu 6 Abrufe gleichzeitig (so drosselt Flink am wenigsten, siehe Lauf #1/#2).
async function alle(liste, n = 6) {
  const erg = new Map(); let i = 0;
  await Promise.all(Array.from({ length: n }, async () => {
    while (i < liste.length) { const u = liste[i++]; erg.set(u, await pruefe(u)); }
  }));
  return erg;
}
// Einzeln und langsam nachpruefen; bricht ab, wenn 3x in Folge keine Antwort kommt
// (Server drosselt weiterhin -> Rest bleibt "nicht pruefbar", kein Fehlalarm).
async function langsam(liste, pause) {
  const erg = new Map(); let still = 0;
  for (const u of liste) {
    if (still >= 3) break;
    const x = await pruefe(u); erg.set(u, x);
    still = x.code === 0 && ZEIT.test(x.fehler) ? still + 1 : 0;
    await warte(pause);
  }
  return erg;
}
const erg = await alle([...links.keys()]);
let defekt = [...erg].filter(([, x]) => art(x) === 'defekt').map(([u]) => u);
if (defekt.length) {
  console.log(`${defekt.length} Links fehlerhaft - zweiter Versuch in 60 s ...`);
  await warte(60000);
  for (const [u, x] of await langsam(defekt, 1000)) erg.set(u, x);
  defekt = defekt.filter(u => art(erg.get(u)) === 'defekt');
}
const zeit = [...erg].filter(([, x]) => x.code === 0 && ZEIT.test(x.fehler)).map(([u]) => u);
if (zeit.length) {
  console.log(`${zeit.length} Links ohne Antwort - in 2 min einzeln nachpruefen ...`);
  await warte(120000);
  for (const [u, x] of await langsam(zeit, 4000)) erg.set(u, x);
  defekt = [...new Set([...defekt, ...zeit])].filter(u => art(erg.get(u)) === 'defekt');
}
const gesperrt = [...erg].filter(([, x]) => art(x) === 'gesperrt').map(([u]) => u);
const grund = x => x.code ? `HTTP ${x.code}${x.code === 404 ? ' (nicht gefunden)' : ''}` : `nicht erreichbar (${x.fehler})`;
const zeile = u => {
  const fund = [...(wo.get(u) || [])].slice(0, 3).join(' | ') || 'Fundstelle unbekannt';
  return `${grund(erg.get(u))} – ${u} – Seiten: ${[...links.get(u)].join('/')} – ${fund}`;
};

// ---------- 4. Bericht ----------
const bericht = [
  `# Link-Check`, ``, `Geprüft: ${erg.size} · defekt: ${defekt.length} · nicht prüfbar (Zugriffsschutz/Drosselung): ${gesperrt.length}`, ``,
  ...(defekt.length ? ['## Defekte Links', '', ...defekt.map(u => `- ${zeile(u)}`), ''] : ['Alle Links funktionieren.', '']),
  ...(gesperrt.length ? ['## Nicht prüfbar (Seite sperrt/drosselt automatische Abrufe – bei Bedarf von Hand kontrollieren)', '',
    ...gesperrt.map(u => `- ${zeile(u)}`)] : []),
].join('\n');
console.log(bericht);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, bericht + '\n');

if (defekt.length) {
  await warnmail(`⚠️ FTEM-Seite: ${defekt.length} Link${defekt.length > 1 ? 's' : ''} funktionier${defekt.length > 1 ? 'en' : 't'} nicht`, [
    `Beim wöchentlichen Link-Check (${erg.size} Links) sind diese Links defekt. Korrigieren in build.py/JSON bzw. im Admin (Admin-Text):`,
    ...defekt.map(zeile),
  ]);
  process.exit(1);
}
