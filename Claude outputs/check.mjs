// Automatischer Funktions-Check der Live-Seite my.ftem.swiss-ski.ch.
// Laeuft alle 6 Stunden per GitHub Action (.github/workflows/seiten-check.yml).
// Jeder fehlgeschlagene Punkt wird nach 90 Sekunden noch zweimal wiederholt,
// bevor Alarm ausgeloest wird (kein Fehlalarm bei kurzen Wacklern).
// Bei bleibenden Problemen: Warn-Mail via Resend + roter Lauf auf GitHub.

import { warnmail } from './_mail.mjs';

// FTEM_BASE/FTEM_SUPA nur fuer lokale Tests mit Mock-Server uebersteuerbar
const BASE = process.env.FTEM_BASE || 'https://my.ftem.swiss-ski.ch';
const SUPA = process.env.FTEM_SUPA || 'https://xphbwnzyebbejsdeqled.supabase.co';
// Oeffentlicher Lese-Schluessel (steht auch im HTML der Seite - kein Geheimnis)
const ANON = 'sb_publishable_UQLqY8OqccllVy9t1FRlFQ_HZr_--D_';

const hole = (url, opt = {}) =>
  fetch(url, { redirect: 'follow', ...opt, signal: AbortSignal.timeout(30000) });

// Jede Pruefung: Name + Funktion, die bei Problem einen Fehlertext wirft.
const PRUEFUNGEN = [
  ...[['/', 'Startseite (DE)'], ['/fr.html', 'Seite FR'], ['/it.html', 'Seite IT'], ['/en.html', 'Seite EN']]
    .map(([p, name]) => [name, async () => {
      const r = await hole(BASE + p);
      if (!r.ok) throw `HTTP ${r.status}`;
      const t = await r.text();
      if (t.length < 1_000_000) throw `Seite unvollstaendig (nur ${Math.round(t.length / 1024)} kB)`;
      if (!t.includes('serviceWorker') || !t.includes('ph-sum')) throw 'erwarteter Inhalt fehlt';
    }]),
  ['Admin-Seite', async () => {
    const r = await hole(BASE + '/admin.html');
    if (!r.ok) throw `HTTP ${r.status}`;
    const t = await r.text();
    if (!t.includes('gatepw')) throw 'Login-Formular fehlt';
  }],
  ['Service-Worker (App/Cache)', async () => {
    const r = await hole(BASE + '/sw.js');
    if (!r.ok) throw `HTTP ${r.status}`;
    if (!/ftem-[0-9a-f]/.test(await r.text())) throw 'Inhalt unerwartet';
  }],
  ['App-Manifest', async () => {
    const r = await hole(BASE + '/manifest.webmanifest');
    if (!r.ok) throw `HTTP ${r.status}`;
  }],
  ['Datenbank (gespeicherte Admin-Texte lesbar)', async () => {
    const r = await hole(`${SUPA}/rest/v1/ftem_overrides?select=cid&limit=1`,
      { headers: { apikey: ANON, authorization: `Bearer ${ANON}` } });
    if (!r.ok) throw `HTTP ${r.status}`;
    if (!Array.isArray(await r.json())) throw 'Antwort unerwartet';
  }],
  ['Speicher-Funktion erreichbar', async () => {
    // Absichtlich OHNE Passwort: Erwartet ist eine saubere Abweisung (400/401/403).
    // 404 = Funktion nicht mehr deployt, 5xx = Funktion kaputt.
    const r = await hole(BASE + '/.netlify/functions/save',
      { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
    if (r.status === 404) throw 'Funktion nicht gefunden (404)';
    if (r.status >= 500) throw `Serverfehler ${r.status}`;
  }],
  ['KI-Funktion (Uebersetzen/Coach) erreichbar', async () => {
    const r = await hole(BASE + '/.netlify/functions/chat',
      { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
    if (r.status === 404) throw 'Funktion nicht gefunden (404)';
    if (r.status >= 500) throw `Serverfehler ${r.status}`;
  }],
];

async function lauf(nur) {
  const probleme = [];
  for (const [name, fn] of PRUEFUNGEN) {
    if (nur && !nur.has(name)) continue;
    try {
      await fn();
      console.log('OK  ', name);
    } catch (e) {
      probleme.push([name, typeof e === 'string' ? e : (e && e.message) || String(e)]);
      console.log('FEHLT', name, '-', probleme[probleme.length - 1][1]);
    }
  }
  return probleme;
}

const WARTE = process.env.FTEM_TEST ? 1000 : 90_000;   // im Test nicht 90 s warten
let probleme = await lauf();
for (let versuch = 2; versuch <= 3 && probleme.length; versuch++) {
  console.log(`\n${probleme.length} Problem(e) - warte ${WARTE / 1000} s, Versuch ${versuch}/3 ...`);
  await new Promise(r => setTimeout(r, WARTE));
  probleme = await lauf(new Set(probleme.map(p => p[0])));
}

if (probleme.length) {
  const zeilen = probleme.map(([n, f]) => `${n}: ${f}`);
  console.error('\nBLEIBENDE PROBLEME:\n' + zeilen.join('\n'));
  await warnmail('⚠️ FTEM-Seite: Prüfung fehlgeschlagen (' + probleme.length + ' Punkt(e))',
    zeilen.map(z => z + ' – blieb auch nach 3 Versuchen über ~3 Minuten bestehen.'));
  process.exit(1);
}
console.log('\nAlles in Ordnung.');
